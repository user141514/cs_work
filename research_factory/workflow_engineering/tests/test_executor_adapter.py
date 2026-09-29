"""WFE-04 dry-run adapter tests. No executor/model/network launch is allowed."""
import copy
import hashlib
import io
import json
import socket
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import offline_gate as gate_mod

try:
    import executor_adapter as adapter
except ImportError:
    adapter = None


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(adapter, "executor_adapter is not implemented yet")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.workspace = self.base / "task"
        (self.workspace / "inputs").mkdir(parents=True)
        self.prompt = self.workspace / "inputs/prompt.txt"
        self.prompt.write_text("frozen task prompt", encoding="utf-8")
        self.evaluator = self.workspace / "inputs/evaluator.txt"
        self.evaluator.write_text("frozen evaluator", encoding="utf-8")

        self.repo = self.base / "repo"
        self.script = self.repo / "research_factory/computer_topconf_2027/run_stageb_agent.ps1"
        self.script.parent.mkdir(parents=True)
        self.script.write_text("[CmdletBinding()]\nparam([string]$Action='Inspect')\n", encoding="utf-8")

        self.identity = {
            "task_id": "task", "task_version": 1,
            "workflow_id": "wfe", "workflow_version": "0.1",
            "plan_id": "WFE-20260929", "plan_version": 4,
            "step_id": "WFE-04", "run_id": "run-dry-1",
        }
        self.contract_path = self.base / "contract.json"
        self.state_dir = self.base / "control"
        self.contract = {
            "identity": copy.deepcopy(self.identity),
            "authorized": True, "status": "ACTIVE", "mode": "OFFLINE_ONLY",
            "workspace": str(self.workspace),
            "goal": "Prepare one real executor command without launching it",
            "acceptance": "Dry-run plan only",
            "stop_condition": "STOP_AFTER_CURRENT_STEP",
            "budget": {"attempts": 1, "tool_calls": 1, "model_calls": 0, "tokens": 0, "wall_ms": 1000},
            "parallel_limit": 1,
            "protected_paths": ["authority"],
            "inputs": [{"path": "inputs/prompt.txt", "sha256": digest(self.prompt)}],
            "evaluator": {"path": "inputs/evaluator.txt", "sha256": digest(self.evaluator)},
            "units": [{
                "id": "adapter",
                "depends_on": [],
                "reads": ["inputs/prompt.txt"],
                "writes": ["out/adapter"],
                "required_artifacts": ["out/adapter/result.json"],
                "actions": ["offline_test"],
                "reservation": {"tool_calls": 1, "model_calls": 0, "tokens": 0, "wall_ms": 1000},
            }],
        }
        dump(self.contract_path, self.contract)
        self.gate = gate_mod.Gate.initialize(self.contract_path, self.state_dir)
        self.lease = self.gate.admit({
            "identity": copy.deepcopy(self.identity),
            "unit_id": "adapter",
            "action": "offline_test",
            "session_paths": [str(self.workspace)],
        })
        self.request = {
            "executor_sha256": digest(self.script),
            "prompt_file": "inputs/prompt.txt",
            "arm_name": "s1-r0",
            "session_id": "",
            "timeout_seconds": 240,
        }

    def denied(self, code, fn, *args, **kwargs):
        with self.assertRaises(gate_mod.GateError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def prepare(self, lease=None, request=None):
        return adapter.prepare_stageb_dry_run(
            gate=self.gate,
            lease=self.lease if lease is None else lease,
            request=self.request if request is None else request,
            repo_root=self.repo,
        )

    def test_valid_lease_builds_nonlaunching_plan(self):
        plan = self.prepare()
        self.assertEqual(plan["mode"], "DRY_RUN")
        self.assertFalse(plan["would_launch"])
        self.assertEqual(plan["executor_id"], "stageb-agent-launch-v1")
        self.assertEqual(plan["executor_sha256"], digest(self.script))
        self.assertEqual(plan["task_workspace"], str(self.workspace))
        self.assertEqual(plan["session_paths"], [str(self.workspace.resolve())])
        self.assertEqual(plan["prompt_file"], str(self.prompt.resolve()))
        self.assertEqual(plan["argv"][0], "powershell.exe")
        self.assertNotIn("-ExecutionPolicy", plan["argv"])
        self.assertIn("-Action", plan["argv"])
        self.assertIn("Launch", plan["argv"])
        self.assertNotIn("next_step", plan)
        self.assertEqual(
            plan["expected_executor_result_fields"],
            ["Backend", "SessionId", "ExitCode", "TimedOut", "StdOutLog", "StdErrLog", "Arm"],
        )

    def test_missing_identity_lease_rejected_before_plan(self):
        bad = copy.deepcopy(self.lease)
        del bad["identity"]["plan_id"]
        self.denied("STALE_IDENTITY", self.prepare, bad)

    def test_consumed_lease_rejected_before_plan(self):
        artifact = self.workspace / "out/adapter/result.json"
        dump(artifact, {"ok": True})
        self.gate.submit({
            "identity": copy.deepcopy(self.identity),
            "unit_id": "adapter",
            "attempt_id": self.lease["attempt_id"],
            "execution_status": "SUCCEEDED",
            "reported_conclusion": "UNASSESSED",
            "artifacts": [{"path": "out/adapter/result.json", "sha256": digest(artifact)}],
            "usage": {"tool_calls": 1, "model_calls": 0, "tokens": 0, "wall_ms": 1},
        })
        self.denied("LEASE_NOT_ACTIVE", self.prepare)

    def test_changed_prompt_after_admission_rejected(self):
        self.prompt.write_text("mutated after admission", encoding="utf-8")
        self.denied("FROZEN_INPUT_CHANGED", self.prepare)

    def test_prompt_must_be_in_declared_read_scope(self):
        other = self.workspace / "inputs/other.txt"
        other.write_text("undeclared", encoding="utf-8")
        request = dict(self.request, prompt_file="inputs/other.txt")
        self.denied("PROMPT_NOT_DECLARED", self.prepare, request=request)

    def test_executor_hash_mismatch_rejected(self):
        request = dict(self.request, executor_sha256="0" * 64)
        self.denied("EXECUTOR_HASH_MISMATCH", self.prepare, request=request)

    def test_unsafe_arm_or_timeout_rejected(self):
        self.denied("INVALID_ARM_NAME", self.prepare, request=dict(self.request, arm_name="../escape"))
        self.denied("INVALID_TIMEOUT", self.prepare, request=dict(self.request, timeout_seconds=0))

    def test_dry_run_surfaces_missing_live_preconditions(self):
        plan = self.prepare()
        self.assertFalse(plan["live_ready"])
        by_name = {item["name"]: item for item in plan["live_preconditions"]}
        self.assertFalse(by_name["backend_freeze_receipt"]["exists"])
        self.assertFalse(by_name["source_arm"]["exists"])
        self.assertTrue(plan["side_effects_if_live"])

    def test_live_readiness_requires_executor_paths_to_match_gate_scope(self):
        plan = self.prepare()
        self.assertFalse(plan["path_alignment"]["arm_within_declared_session_paths"])
        self.assertFalse(plan["path_alignment"]["log_root_within_declared_writes"])
        self.assertFalse(plan["live_ready"])
        self.assertIn("executor_path_ownership", plan["remaining_enforcement_gaps"])
        self.assertIn("atomic_dispatch_claim", plan["remaining_enforcement_gaps"])

    def test_prepare_never_connects_or_starts_process(self):
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
             patch.object(subprocess, "Popen", side_effect=AssertionError("process forbidden")):
            plan = self.prepare()
        self.assertFalse(plan["would_launch"])

    def test_cli_emits_json_plan_without_launch(self):
        lease_path = self.base / "lease.json"
        request_path = self.base / "request.json"
        dump(lease_path, self.lease)
        dump(request_path, self.request)
        out = io.StringIO()
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
             patch.object(subprocess, "Popen", side_effect=AssertionError("process forbidden")), \
             redirect_stdout(out):
            code = adapter.main([
                "--state-dir", str(self.state_dir),
                "--lease", str(lease_path),
                "--request", str(request_path),
                "--repo-root", str(self.repo),
            ])
        self.assertEqual(code, 0)
        payload = json.loads(out.getvalue())
        self.assertTrue(payload["ok"])
        self.assertFalse(payload["plan"]["would_launch"])


if __name__ == "__main__":
    unittest.main()
