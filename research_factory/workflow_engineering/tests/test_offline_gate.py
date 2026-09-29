"""Model-free behavioral tests. Fake workers only write temporary artifacts."""
import copy
import hashlib
import io
import json
import socket
import subprocess
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

try:
    import offline_gate as mod
except ImportError:
    mod = None

RESOURCES = ("tool_calls", "model_calls", "tokens", "wall_ms")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


class BootstrapTests(unittest.TestCase):
    def test_gate_module_exists(self):
        self.assertIsNotNone(mod, "offline_gate is not implemented yet")


class GateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(mod, "offline_gate is not implemented yet")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "workspace"
        (self.root / "inputs").mkdir(parents=True)
        (self.root / "inputs/task.txt").write_text("fixed real task", encoding="utf-8")
        (self.root / "inputs/evaluator.txt").write_text("frozen endpoint evaluator", encoding="utf-8")
        self.contract_path = self.base / "contract.json"
        self.state_dir = self.base / "control"
        self.identity = dict(task_id="task", task_version=1, workflow_id="wfe", workflow_version="0.1",
                             plan_id="plan", plan_version=1, step_id="S1", run_id="run-1")
        self.contract = {
            "identity": copy.deepcopy(self.identity), "authorized": True, "status": "ACTIVE", "mode": "OFFLINE_ONLY",
            "workspace": str(self.root), "goal": "Validate one offline step",
            "acceptance": "Read and verify declared artifacts", "stop_condition": "STOP_AFTER_CURRENT_STEP",
            "budget": {"attempts": 2, "tool_calls": 4, "model_calls": 0, "tokens": 0, "wall_ms": 2000},
            "parallel_limit": 2, "protected_paths": ["authority"],
            "inputs": [{"path": "inputs/task.txt", "sha256": digest(self.root / "inputs/task.txt")}],
            "evaluator": {"path": "inputs/evaluator.txt", "sha256": digest(self.root / "inputs/evaluator.txt")},
            "units": [self.unit("a"), self.unit("b")],
        }

    def unit(self, name, deps=None):
        return {"id": name, "depends_on": deps or [], "reads": ["inputs/task.txt"],
                "writes": ["out/" + name], "required_artifacts": ["out/" + name + "/result.json"],
                "actions": ["offline_test"],
                "reservation": {"tool_calls": 2, "model_calls": 0, "tokens": 0, "wall_ms": 1000}}

    def start(self):
        dump(self.contract_path, self.contract)
        return mod.Gate.initialize(self.contract_path, self.state_dir)

    def request(self, unit="a", **changes):
        req = {"identity": copy.deepcopy(self.identity), "unit_id": unit, "action": "offline_test",
               "session_paths": [str(self.root)]}
        req.update(changes)
        return req

    def receipt(self, lease, execution="SUCCEEDED", conclusion="UNASSESSED", write=True):
        unit = next(u for u in self.contract["units"] if u["id"] == lease["unit_id"])
        artifacts = []
        for name in unit["required_artifacts"]:
            path = self.root / name
            if write:
                dump(path, {"task_id": "task", "value": 42})
            artifacts.append({"path": name, "sha256": digest(path) if path.exists() else "0" * 64})
        return {"identity": copy.deepcopy(self.identity), "unit_id": lease["unit_id"],
                "attempt_id": lease["attempt_id"], "execution_status": execution,
                "reported_conclusion": conclusion, "artifacts": artifacts,
                "usage": {"tool_calls": 1, "model_calls": 0, "tokens": 0, "wall_ms": 1}}

    def finish_request(self, decision="KEEP"):
        return {"identity": copy.deepcopy(self.identity), "decision": decision,
                "next_step": None if decision == "TERMINATE" else {"id": "S2", "question": "Review the next boundary"}}

    def denied(self, code, fn, *args, **kwargs):
        with self.assertRaises(mod.GateError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_missing_contract_rejected(self):
        self.denied("MISSING_CONTRACT", mod.Gate.initialize, self.contract_path, self.state_dir)

    def test_missing_identity_rejected(self):
        del self.contract["identity"]["plan_id"]
        self.denied("INVALID_IDENTITY", self.start)

    def test_unapproved_contract_rejected(self):
        self.contract["authorized"] = False
        self.denied("NOT_AUTHORIZED", self.start)

    def test_nonoffline_contract_rejected(self):
        self.contract["budget"]["model_calls"] = 1
        self.denied("OFFLINE_ONLY", self.start)

    def test_cycle_rejected(self):
        self.contract["units"][0]["depends_on"] = ["b"]
        self.contract["units"][1]["depends_on"] = ["a"]
        self.denied("DEPENDENCY_CYCLE", self.start)

    def test_missing_dependency_rejected(self):
        self.contract["units"][0]["depends_on"] = ["ghost"]
        self.denied("UNKNOWN_DEPENDENCY", self.start)

    def test_missing_read_dependency_rejected(self):
        self.contract["units"][1]["reads"].append("out/a/result.json")
        self.denied("UNDECLARED_DEPENDENCY", self.start)

    def test_worker_cannot_write_authority(self):
        self.contract["units"][0]["writes"] = ["authority"]
        self.contract["units"][0]["required_artifacts"] = ["authority/result.json"]
        self.denied("PROTECTED_WRITE", self.start)

    def test_worker_cannot_write_frozen_input(self):
        self.contract["units"][0]["writes"] = ["inputs"]
        self.contract["units"][0]["required_artifacts"] = ["inputs/result.json"]
        self.denied("PROTECTED_WRITE", self.start)

    def test_wrong_step_rejected_before_admission(self):
        gate = self.start()
        req = self.request()
        req["identity"]["step_id"] = "S2"
        self.denied("STALE_IDENTITY", gate.admit, req)
        self.assertEqual(gate.status()["attempts"], {})

    def test_unlisted_action_rejected(self):
        gate = self.start()
        self.denied("UNAUTHORIZED_ACTION", gate.admit, self.request(action="launch_model"))

    def test_unlisted_unit_rejected(self):
        self.denied("UNKNOWN_UNIT", self.start().admit, self.request("future"))

    def test_changed_plan_rejected(self):
        gate = self.start()
        self.contract["identity"]["plan_version"] = 2
        dump(self.contract_path, self.contract)
        self.denied("CONTRACT_CHANGED", gate.admit, self.request())

    def test_changed_evaluator_rejected(self):
        gate = self.start()
        (self.root / "inputs/evaluator.txt").write_text("easier judge", encoding="utf-8")
        self.denied("EVALUATOR_CHANGED", gate.admit, self.request())

    def test_changed_input_rejected(self):
        gate = self.start()
        lease = gate.admit(self.request())
        receipt = self.receipt(lease)
        (self.root / "inputs/task.txt").write_text("new task", encoding="utf-8")
        self.denied("FROZEN_INPUT_CHANGED", gate.submit, receipt)
        self.assertEqual(gate.status()["attempts"][lease["attempt_id"]]["status"], "INVALID")

    def test_valid_independent_workers_admitted_together(self):
        gate = self.start()
        a = gate.admit(self.request("a"))
        b = gate.admit(self.request("b"))
        self.assertNotEqual(a["attempt_id"], b["attempt_id"])
        self.assertEqual(len([v for v in gate.status()["attempts"].values() if v["status"] == "RUNNING"]), 2)

    def test_overlapping_writes_reject_parallel(self):
        self.contract["units"][1]["writes"] = ["out/a/subdir"]
        self.contract["units"][1]["required_artifacts"] = ["out/a/subdir/result.json"]
        gate = self.start()
        gate.admit(self.request("a"))
        self.denied("RESOURCE_CONFLICT", gate.admit, self.request("b"))

    def test_dependency_must_be_accepted_before_admission(self):
        self.contract["units"][1]["depends_on"] = ["a"]
        self.contract["units"][1]["reads"].append("out/a/result.json")
        gate = self.start()
        self.denied("DEPENDENCY_NOT_READY", gate.admit, self.request("b"))
        a = gate.admit(self.request("a"))
        self.denied("DEPENDENCY_NOT_READY", gate.admit, self.request("b"))
        gate.submit(self.receipt(a))
        self.assertEqual(gate.admit(self.request("b"))["unit_id"], "b")

    def test_tampered_dependency_rechecked(self):
        self.contract["units"][1]["depends_on"] = ["a"]
        self.contract["units"][1]["reads"].append("out/a/result.json")
        gate = self.start()
        a = gate.admit(self.request())
        gate.submit(self.receipt(a))
        (self.root / "out/a/result.json").write_text("changed", encoding="utf-8")
        self.denied("DEPENDENCY_EVIDENCE_CHANGED", gate.admit, self.request("b"))

    def test_wrong_workspace_in_session_rejected(self):
        gate = self.start()
        self.denied("WORKSPACE_ESCAPE", gate.admit,
                    self.request(session_paths=[str(self.base / "old-arm/task.py")]))

    def test_path_traversal_rejected(self):
        gate = self.start()
        self.denied("WORKSPACE_ESCAPE", gate.admit, self.request(session_paths=["../old-arm"]))

    def test_symlink_escape_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.root / "link").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable on this host")
        self.denied("WORKSPACE_ESCAPE", self.start().admit, self.request(session_paths=["link/result.json"]))

    def test_portable_windows_path_guard(self):
        self.assertEqual(mod.scoped_path("d:\\ARM\\new\\src\\..\\result.json", "D:/arm/new").replace("\\", "/").casefold(),
                         "d:/arm/new/result.json")
        for path in ("D:/arm/old/result.json", "D:/arm/newish/result.json", "E:/arm/new/result.json"):
            self.denied("WORKSPACE_ESCAPE", mod.scoped_path, path, "D:/arm/new")

    def test_historical_wrong_workspace_fixture(self):
        fixture = json.loads((Path(__file__).parents[1] / "fixtures/historical_wrong_workspace.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture["evidence_class"], "DEVELOPMENT_RETROSPECTIVE")
        for path in fixture["wrong_session_paths"]:
            self.denied("WORKSPACE_ESCAPE", mod.scoped_path, path, fixture["expected_workspace"])
        for path in fixture["correct_session_paths"]:
            mod.scoped_path(path, fixture["expected_workspace"])

    def test_stale_receipt_does_not_overwrite_running_attempt(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["identity"]["plan_version"] = 0
        self.denied("STALE_IDENTITY", gate.submit, receipt)
        self.assertEqual(gate.status()["attempts"][a["attempt_id"]]["status"], "RUNNING")

    def test_missing_evidence_invalid_not_scientific_failure(self):
        gate = self.start()
        a = gate.admit(self.request())
        self.denied("MISSING_ARTIFACT", gate.submit, self.receipt(a, conclusion="NOT_SUPPORTED", write=False))
        record = gate.status()["attempts"][a["attempt_id"]]
        self.assertEqual(record["status"], "INVALID")
        self.assertEqual(record["scientific_conclusion"], "UNASSESSED")
        self.assertEqual(gate.status()["reserved"]["attempts"], 1)

    def test_tampered_evidence_rejected(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        (self.root / "out/a/result.json").write_text("tampered", encoding="utf-8")
        self.denied("ARTIFACT_HASH_MISMATCH", gate.submit, receipt)

    def test_exit_success_without_all_declared_evidence_rejected(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["artifacts"] = []
        self.denied("ARTIFACT_SET_MISMATCH", gate.submit, receipt)

    def test_failed_execution_never_scientific_negative(self):
        gate = self.start()
        a = gate.admit(self.request())
        self.denied("EXECUTION_FAILED", gate.submit, self.receipt(a, execution="FAILED", conclusion="NOT_SUPPORTED"))
        record = gate.status()["attempts"][a["attempt_id"]]
        self.assertEqual(record["scientific_conclusion"], "UNASSESSED")
        self.assertEqual(record["reported_conclusion"], "NOT_SUPPORTED")

    def test_hash_validity_does_not_promote_scientific_claim(self):
        gate = self.start()
        a = gate.admit(self.request())
        result = gate.submit(self.receipt(a, conclusion="SUPPORTED"))
        self.assertEqual(result["evidence_status"], "STRUCTURALLY_VALID")
        self.assertEqual(result["scientific_conclusion"], "UNASSESSED")

    def test_duplicate_admission_rejected(self):
        gate = self.start()
        gate.admit(self.request())
        self.denied("ALREADY_ADMITTED", gate.admit, self.request())
        self.assertEqual(gate.status()["reserved"]["attempts"], 1)

    def test_duplicate_receipt_rejected(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        gate.submit(receipt)
        self.denied("DUPLICATE_RECEIPT", gate.submit, receipt)

    def test_attempt_budget_reserved_before_dispatch(self):
        self.contract["budget"]["attempts"] = 1
        gate = self.start()
        gate.admit(self.request())
        self.denied("BUDGET_EXCEEDED", gate.admit, self.request("b"))

    def test_parallel_limit_enforced(self):
        self.contract["parallel_limit"] = 1
        gate = self.start()
        gate.admit(self.request())
        self.denied("PARALLEL_LIMIT", gate.admit, self.request("b"))

    def test_nonfinite_or_boolean_budget_rejected(self):
        for value in (-1, True, float("nan"), 1.5):
            with self.subTest(value=value):
                self.contract["budget"]["tokens"] = value
                self.denied("INVALID_BUDGET", self.start)

    def test_excess_usage_invalid_and_counted(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["usage"]["tool_calls"] = 3
        self.denied("USAGE_EXCEEDED", gate.submit, receipt)
        state = gate.status()
        self.assertEqual(state["reported_usage"]["tool_calls"], 3)
        self.assertEqual(state["reserved"]["attempts"], 1)
        self.denied("REPLAN_REQUIRED", gate.admit, self.request("b"))

    def test_preexisting_outputs_not_new_evidence(self):
        dump(self.root / "out/a/result.json", {"old": True})
        self.denied("PREEXISTING_ARTIFACT", self.start().admit, self.request())

    def test_admission_read_snapshot_revalidated_at_submission(self):
        extra = self.root / "inputs/extra.txt"
        extra.write_text("v1", encoding="utf-8")
        self.contract["units"][0]["reads"].append("inputs/extra.txt")
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        extra.write_text("v2", encoding="utf-8")
        self.denied("READ_SET_CHANGED", gate.submit, receipt)

    def test_finish_requires_all_evidence_for_keep(self):
        self.denied("STEP_INCOMPLETE", self.start().finish, self.finish_request())

    def test_finish_refuses_active_workers_even_for_termination(self):
        gate = self.start()
        gate.admit(self.request())
        self.denied("WORK_IN_PROGRESS", gate.finish, self.finish_request("TERMINATE"))

    def test_valid_step_stops_and_does_not_dispatch_next(self):
        gate = self.start()
        for name in ("a", "b"):
            gate.submit(self.receipt(gate.admit(self.request(name))))
        result = gate.finish(self.finish_request())
        self.assertEqual(result["phase"], "STOPPED")
        self.assertFalse(result["next_step"]["authorized"])
        self.assertEqual(len(result["attempts"]), 2)
        self.denied("STEP_STOPPED", gate.admit, self.request())
        self.denied("STEP_STOPPED", gate.finish, self.finish_request())

    def test_invalid_step_requires_modify_or_terminate(self):
        gate = self.start()
        a = gate.admit(self.request())
        self.denied("MISSING_ARTIFACT", gate.submit, self.receipt(a, write=False))
        self.denied("INVALID_EVIDENCE", gate.finish, self.finish_request())
        self.assertEqual(gate.finish(self.finish_request("MODIFY"))["phase"], "STOPPED")

    def test_next_step_cannot_self_authorize(self):
        gate = self.start()
        request = self.finish_request("MODIFY")
        request["next_step"]["authorized"] = True
        self.denied("NEXT_STEP_NOT_AUTHORIZED", gate.finish, request)

    def test_only_one_next_step(self):
        gate = self.start()
        request = self.finish_request("MODIFY")
        request["next_step"] = [{"id": "S2"}, {"id": "S3"}]
        self.denied("INVALID_NEXT_STEP", gate.finish, request)

    def test_state_survives_reopen(self):
        gate = self.start()
        a = gate.admit(self.request())
        other = mod.Gate(self.state_dir)
        self.denied("ALREADY_ADMITTED", other.admit, self.request())
        other.submit(self.receipt(a))
        self.assertEqual(gate.status()["attempts"][a["attempt_id"]]["status"], "ACCEPTED")

    def test_reinitialization_cannot_reset_budget(self):
        self.start().admit(self.request())
        self.denied("STATE_EXISTS", mod.Gate.initialize, self.contract_path, self.state_dir)

    def test_racing_conflicting_admissions_exactly_one_wins(self):
        self.contract["units"][1]["writes"] = ["out/a/sub"]
        self.contract["units"][1]["required_artifacts"] = ["out/a/sub/result.json"]
        self.start()
        barrier = threading.Barrier(2)
        def race(name):
            gate = mod.Gate(self.state_dir)
            barrier.wait(timeout=5)
            try:
                gate.admit(self.request(name))
                return "ADMITTED"
            except mod.GateError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(race, ("a", "b")))
        self.assertCountEqual(results, ["ADMITTED", "RESOURCE_CONFLICT"])
        self.assertEqual(mod.Gate(self.state_dir).status()["reserved"]["attempts"], 1)

    def test_no_network_or_process_during_full_fake_step(self):
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
             patch.object(subprocess, "Popen", side_effect=AssertionError("process launch forbidden")):
            gate = self.start()
            for name in ("a", "b"):
                gate.submit(self.receipt(gate.admit(self.request(name))))
            self.assertEqual(gate.finish(self.finish_request())["phase"], "STOPPED")

    def test_boolean_identity_version_is_not_integer_version(self):
        gate = self.start()
        req = self.request()
        req["identity"]["plan_version"] = True
        self.denied("STALE_IDENTITY", gate.admit, req)

    def test_inroot_write_scope_retargeted_after_init_rejected(self):
        gate = self.start()
        (self.root / "out").mkdir()
        try:
            (self.root / "out/a").symlink_to(self.root / "inputs", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable on this host")
        self.denied("SCOPE_CHANGED", gate.admit, self.request())

    def test_receipt_attempt_id_wrong_type_has_typed_denial(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["attempt_id"] = []
        self.denied("UNKNOWN_ATTEMPT", gate.submit, receipt)

    def test_malformed_usage_invalid_and_does_not_reset_attempt(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["usage"]["tool_calls"] = True
        self.denied("INVALID_USAGE", gate.submit, receipt)
        self.assertEqual(gate.status()["attempts"][a["attempt_id"]]["status"], "INVALID")
        self.assertEqual(gate.status()["reserved"]["attempts"], 1)

    def test_non_json_receipt_is_rejected_without_corrupting_state(self):
        gate = self.start()
        a = gate.admit(self.request())
        receipt = self.receipt(a)
        receipt["extra"] = float("nan")
        self.denied("INVALID_RECEIPT", gate.submit, receipt)
        self.assertEqual(gate.status()["attempts"][a["attempt_id"]]["status"], "RUNNING")

    def test_finish_rechecks_previously_accepted_evidence(self):
        gate = self.start()
        for name in ("a", "b"):
            gate.submit(self.receipt(gate.admit(self.request(name))))
        (self.root / "out/a/result.json").write_text("later edit", encoding="utf-8")
        self.denied("ARTIFACT_CHANGED_AFTER_SUBMIT", gate.finish, self.finish_request())

    def test_terminate_records_contract_drift_without_accepting_it(self):
        gate = self.start()
        self.contract["goal"] = "changed goal"
        dump(self.contract_path, self.contract)
        result = gate.finish(self.finish_request("TERMINATE"))
        self.assertEqual(result["phase"], "STOPPED")
        self.assertEqual(result["closure_validation_error"], "CONTRACT_CHANGED")
        self.assertEqual(result["contract"]["goal"], "Validate one offline step")
        self.assertIsNone(result["next_step"])

    def test_artifact_hardlinked_to_input_is_not_independent_evidence(self):
        import os
        gate = self.start()
        a = gate.admit(self.request())
        target = self.root / "out/a/result.json"
        target.parent.mkdir(parents=True)
        try:
            os.link(str(self.root / "inputs/task.txt"), str(target))
        except (OSError, NotImplementedError):
            self.skipTest("hardlink unavailable on this host")
        self.denied("LINKED_ARTIFACT", gate.submit, self.receipt(a, write=False))

    def test_cli_status_and_rejection_are_json(self):
        self.start()
        out = io.StringIO()
        with redirect_stdout(out):
            code = mod.main(["status", "--state-dir", str(self.state_dir)])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out.getvalue())["ok"])
        dump(self.base / "request.json", self.request(action="launch_model"))
        out = io.StringIO()
        with redirect_stdout(out):
            code = mod.main(["admit", "--state-dir", str(self.state_dir), "--request", str(self.base / "request.json")])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.getvalue())["code"], "UNAUTHORIZED_ACTION")


if __name__ == "__main__":
    unittest.main()
