"""Real-process acceptance tests; deliberately separate from the no-process suite."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import offline_gate as g
try:
    import local_runner as runner
except ImportError:
    runner = None

WORKER = '''import json, sys, time
from pathlib import Path
mode, source, target = sys.argv[1:]
start = time.monotonic()
if mode == "timeout": time.sleep(5)
if mode == "parallel": time.sleep(1)
if mode == "missing": sys.exit(0)
p = Path(target)
p.parent.mkdir(parents=True, exist_ok=True)
raw = json.loads(Path(source).read_text())
value = raw["value"] if isinstance(raw, dict) else raw
p.write_text(json.dumps({"value": value * 2, "start": start, "end": time.monotonic()}))
if mode == "fail": sys.exit(3)
'''


def dump(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def pin(root, name):
    return {"path": name, "sha256": g.file_hash(str(root / name), "MISSING_INPUT")}


def fixture(base, modes=("ok",), dependent=False, shared=False):
    work = base / "work"
    (work / "inputs").mkdir(parents=True)
    (work / "inputs/worker.py").write_text(WORKER, encoding="utf-8")
    (work / "inputs/value.json").write_text("7", encoding="utf-8")
    (work / "inputs/evaluator.txt").write_text("Require declared artifacts; no scientific verdict.", encoding="utf-8")
    units = []
    for i, mode in enumerate(modes):
        name = chr(97 + i)
        source = "out/a/result.json" if dependent and i else "inputs/value.json"
        output = ("out/shared/" if shared else "out/") + name
        units.append({"id": name, "depends_on": ["a"] if dependent and i else [],
                      "reads": ["inputs/worker.py", source],
                      "writes": ["out/shared" if shared else output],
                      "required_artifacts": [output + "/result.json"], "actions": ["offline_test"],
                      "reservation": {"tool_calls": 1, "model_calls": 0, "tokens": 0, "wall_ms": 15000},
                      "execution": {"script": "inputs/worker.py", "args": [mode, source, output + "/result.json"],
                                    "timeout_seconds": 1 if mode == "timeout" else 10, "log_dir": output + "/logs"}})
    contract = {"identity": {"task_id": "local-test", "task_version": 1, "workflow_id": "wfe",
                             "workflow_version": "0.2-local", "plan_id": "WFE-20260929", "plan_version": 5,
                             "step_id": "WFE-05", "run_id": base.name},
                "authorized": True, "status": "ACTIVE", "mode": "OFFLINE_ONLY", "workspace": str(work),
                "goal": "Run frozen local scripts once and collect actual evidence", "acceptance": "Declared outputs",
                "stop_condition": "STOP_AFTER_CURRENT_STEP", "parallel_limit": 2,
                "budget": {"attempts": len(units), "tool_calls": len(units), "model_calls": 0,
                           "tokens": 0, "wall_ms": 15000 * len(units)}, "protected_paths": [],
                "inputs": [pin(work, n) for n in ("inputs/worker.py", "inputs/value.json")],
                "evaluator": pin(work, "inputs/evaluator.txt"), "units": units,
                "runner": {"kind": "local-python-v1", "python_sha256": g.file_hash(sys.executable, "PYTHON_MISSING")},
                "next_step": {"id": "RESEARCH-01", "question": "Read actual evidence before choosing the next research step", "authorized": False}}
    path = base / "contract.json"
    dump(path, contract)
    return path, base / "control", work, contract


def verifier_fixture(base):
    path, control, work, contract = fixture(base)
    names = ("offline_gate.py", "executor_adapter.py", "verify_offline.py", "tests/__init__.py",
             "tests/test_offline_gate.py", "tests/test_executor_adapter.py", "fixtures/historical_wrong_workspace.json")
    for name in names:
        target = work / "inputs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(ROOT / name), str(target))
    contract["inputs"].extend(pin(work, "inputs/" + name) for name in names)
    unit = contract["units"][0]
    unit["reads"] = ["inputs/" + n for n in names]
    unit["execution"] = {"script": "inputs/verify_offline.py", "args": ["--output-dir", "out/a/checks"],
                         "timeout_seconds": 45, "log_dir": "out/a/logs"}
    unit["required_artifacts"] = ["out/a/checks/result.json", "out/a/checks/test_output.txt"]
    unit["reservation"]["wall_ms"] = 60000
    contract["budget"]["wall_ms"] = 60000
    dump(path, contract)
    return path, control, work, contract


class LocalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner, "local_runner is not implemented")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def run_case(self, modes=("ok",), **kwargs):
        path, control, work, contract = fixture(self.base, modes, **kwargs)
        return runner.run_step(path, control), work, control

    def test_real_execution_receipt_stop_and_no_relaunch(self):
        state, work, control = self.run_case()
        self.assertEqual(state["phase"], "STOPPED")
        self.assertEqual(state["next_step"]["authorized"], False)
        attempt = next(iter(state["attempts"].values()))
        self.assertEqual(attempt["status"], "ACCEPTED")
        self.assertEqual(attempt["scientific_conclusion"], "UNASSESSED")
        self.assertEqual(json.loads((work / "out/a/result.json").read_text())["value"], 14)
        self.assertEqual(attempt["submitted_receipt"]["process"]["returncode"], 0)
        with self.assertRaises(g.GateError) as error:
            runner.run_step(self.base / "contract.json", control)
        self.assertEqual(error.exception.code, "STATE_EXISTS")
        self.assertEqual(len(g.Gate(control).status()["attempts"]), 1)

    def test_real_independent_workers_overlap(self):
        state, work, _ = self.run_case(("parallel", "parallel"))
        a, b = [json.loads((work / ("out/" + n + "/result.json")).read_text()) for n in ("a", "b")]
        self.assertLess(max(a["start"], b["start"]), min(a["end"], b["end"]))
        self.assertTrue(all(x["status"] == "ACCEPTED" for x in state["attempts"].values()))

    def test_dependencies_wait_for_accepted_artifacts(self):
        state, work, _ = self.run_case(("ok", "ok"), dependent=True)
        self.assertEqual(json.loads((work / "out/b/result.json").read_text())["value"], 28)
        self.assertEqual(len(state["attempts"]), 2)

    def test_conflicting_scopes_are_serialized_not_dropped(self):
        state, work, _ = self.run_case(("ok", "ok"), shared=True)
        self.assertEqual(len(state["attempts"]), 2)
        a, b = [json.loads((work / ("out/shared/" + n + "/result.json")).read_text()) for n in ("a", "b")]
        self.assertLessEqual(a["end"], b["start"])

    def test_two_invocations_only_one_owns_the_run(self):
        path, control, work, _ = fixture(self.base)
        barrier = threading.Barrier(2)
        def invoke(_):
            barrier.wait(timeout=10)
            completed = subprocess.run([sys.executable, "-B", str(ROOT / "local_runner.py"),
                                        "--contract", str(path), "--state-dir", str(control)],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
            payload = json.loads(completed.stdout.decode("utf-8"))
            return payload.get("phase", payload.get("code"))
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(invoke, range(2))), ["STOPPED", "STATE_EXISTS"])
        self.assertEqual(len(g.Gate(control).status()["attempts"]), 1)

    def test_failure_missing_output_and_timeout_are_not_scientific_negatives(self):
        for mode, expected in (("fail", "EXECUTION_FAILED"), ("missing", "MISSING_ARTIFACT"), ("timeout", "EXECUTION_FAILED")):
            with self.subTest(mode=mode):
                path, control, work, _ = fixture(self.base / mode, (mode, "ok"), dependent=True)
                state = runner.run_step(path, control)
                attempt = next(iter(state["attempts"].values()))
                self.assertEqual(state["phase"], "STOPPED")
                self.assertEqual(attempt["status"], "INVALID")
                self.assertEqual(attempt["rejection_code"], expected)
                self.assertEqual(attempt["scientific_conclusion"], "UNASSESSED")
                self.assertFalse((work / "out/b/result.json").exists())
                if mode == "timeout":
                    self.assertTrue(attempt["submitted_receipt"]["process"]["timed_out"])

    def test_unauthorized_task_does_not_start(self):
        path, control, work, contract = fixture(self.base)
        contract["authorized"] = False
        dump(path, contract)
        with self.assertRaises(g.GateError):
            runner.run_step(path, control)
        self.assertFalse((work / "out").exists())

    def test_changed_command_after_freeze_does_not_start(self):
        path, control, work, contract = fixture(self.base)
        original = g.Gate.admit
        def drift(gate, request):
            contract["units"][0]["execution"]["args"][0] = "fail"
            dump(path, contract)
            return original(gate, request)
        with patch.object(g.Gate, "admit", drift):
            state = runner.run_step(path, control)
        self.assertEqual(state["phase"], "STOPPED")
        self.assertEqual(state["closure_validation_error"], "CONTRACT_CHANGED")
        self.assertFalse((work / "out").exists())

    def test_unfrozen_script_and_out_of_scope_logs_rejected(self):
        for case in ("script", "logs", "python"):
            with self.subTest(case=case):
                path, control, work, contract = fixture(self.base / case)
                if case == "script": contract["inputs"] = contract["inputs"][1:]
                if case == "logs": contract["units"][0]["execution"]["log_dir"] = "inputs/logs"
                if case == "python": contract["runner"]["python_sha256"] = "0" * 64
                dump(path, contract)
                with self.assertRaises(g.GateError): runner.run_step(path, control)
                self.assertFalse((work / "out").exists())

    def test_existing_offline_verifier_runs_as_real_child(self):
        path, control, work, _ = verifier_fixture(self.base)
        state = runner.run_step(path, control)
        report = json.loads((work / "out/a/checks/result.json").read_text())
        self.assertTrue(report["success"])
        self.assertGreaterEqual(report["tests_run"], 74)
        self.assertEqual(state["phase"], "STOPPED")
        self.assertEqual(next(iter(state["attempts"].values()))["status"], "ACCEPTED")


def smoke():
    """A persistent, inspectable example using the real existing offline verifier."""
    base = Path(tempfile.mkdtemp(prefix="wfe_closeout_"))
    path, control, work, _ = verifier_fixture(base)
    argv = [sys.executable, "-B", str(ROOT / "local_runner.py"), "--contract", str(path), "--state-dir", str(control)]
    completed = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    payload = json.loads(completed.stdout.decode("utf-8"))
    state = g.Gate(control).status()  # Fresh authoritative read after the CLI exited.
    report = json.loads((work / "out/a/checks/result.json").read_text(encoding="utf-8"))
    assert completed.returncode == 0 and payload["ok"] and report["success"]
    assert state["phase"] == "STOPPED" and state["next_step"]["authorized"] is False
    repeated = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    denial = json.loads(repeated.stdout.decode("utf-8"))
    assert repeated.returncode == 2 and denial["code"] == "STATE_EXISTS"
    evidence = {"platform": report["platform"], "python": report["python"], "command": argv,
                "phase": state["phase"], "attempts": len(state["attempts"]),
                "next_step_authorized": state["next_step"]["authorized"], "duplicate_denial": denial["code"],
                "verifier_tests": report["tests_run"], "verifier_passed": report["passed"],
                "verifier_failures": report["failures"], "verifier_errors": report["errors"],
                "verifier_skipped": report["skipped"], "artifact_report": str(work / "out/a/checks/result.json"),
                "state_db": str(control / "gate.sqlite3"),
                "source_sha256": {n: g.file_hash(str(ROOT / n), "MISSING_SOURCE")
                                  for n in ("local_runner.py", "offline_gate.py", "runtime_tests/test_local_runner.py")}}
    dump(base / "smoke_result.json", evidence)
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--smoke"]:
        smoke()
    else:
        unittest.main()
