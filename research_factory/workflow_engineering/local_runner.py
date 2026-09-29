"""Run one frozen step of trusted local Python work, collect receipts, then stop.

No new dispatcher: Gate.initialize owns the run; Gate.admit atomically claims
units. The runner never accepts a caller-supplied lease or mutable command.
This is not an OS sandbox. Only audited, bounded, childless local scripts are
supported; model clients, daemons and arbitrary shell commands are out of scope.
"""
import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import offline_gate as g


def _inside(path, roots):
    for root in roots:
        try:
            Path(path).relative_to(Path(root))
            return True
        except ValueError:
            pass
    return False


def _execution(contract, unit):
    root = contract["workspace"]
    cfg = unit.get("execution")
    g.require(isinstance(cfg, dict) and set(cfg) == {"script", "args", "timeout_seconds", "log_dir"}, "INVALID_EXECUTION")
    script = g.scoped_path(cfg["script"], root)
    frozen = g.artifact_map(contract["inputs"], root, "INVALID_CONTRACT")
    reads = [g.scoped_path(p, root) for p in unit["reads"]]
    g.require(script in frozen and script in reads and Path(script).suffix == ".py", "EXECUTOR_NOT_FROZEN")
    args = cfg["args"]
    g.require(isinstance(args, list) and all(isinstance(x, str) and "\x00" not in x for x in args), "INVALID_ARGUMENTS")
    timeout = cfg["timeout_seconds"]
    g.require(type(timeout) is int and 1 <= timeout <= 300, "INVALID_TIMEOUT")
    g.require(unit["reservation"]["wall_ms"] >= timeout * 1000 and unit["reservation"]["tool_calls"] >= 1,
              "EXECUTION_BUDGET")
    g.require("offline_test" in unit["actions"], "RUNNER_ACTION_REQUIRED")
    logs = g.scoped_path(cfg["log_dir"], root)
    writes = [g.scoped_path(p, root) for p in unit["writes"]]
    g.require(_inside(logs, writes), "RUNNER_LOG_SCOPE")
    g.require(not any(g.overlap(logs, p) for p in reads + list(frozen)), "RUNNER_LOG_SCOPE")
    return [sys.executable, "-B", "-s", script] + list(args), Path(logs), timeout


def _validate(contract):
    g.validate_contract(contract)
    g.require(contract["identity"]["workflow_version"] == "0.2-local", "RUNNER_VERSION")
    cfg = contract.get("runner")
    g.require(isinstance(cfg, dict) and set(cfg) == {"kind", "python_sha256"}
              and cfg["kind"] == "local-python-v1", "INVALID_RUNNER")
    g.require(cfg["python_sha256"] == g.file_hash(sys.executable, "PYTHON_MISSING"), "PYTHON_CHANGED")
    nxt = contract.get("next_step")
    g.require(isinstance(nxt, dict) and set(nxt) == {"id", "question", "authorized"}
              and nxt["authorized"] is False and isinstance(nxt["id"], str) and bool(nxt["id"].strip())
              and nxt["id"] != contract["identity"]["step_id"]
              and isinstance(nxt["question"], str) and bool(nxt["question"].strip()), "INVALID_NEXT_STEP")
    for unit in contract["units"]:
        _execution(contract, unit)


def _execute(gate, contract, unit, lease):
    started = time.monotonic()
    process = {"returncode": None, "timed_out": False, "error": None, "cwd": contract["workspace"]}
    execution_status = "FAILED"
    try:
        # Admission belongs to this invocation. Never recover/re-dispatch an old RUNNING lease.
        gate.validate_lease(lease)
        argv, logs, timeout = _execution(contract, unit)
        g.require(contract["runner"]["python_sha256"] == g.file_hash(sys.executable, "PYTHON_MISSING"), "PYTHON_CHANGED")
        process["argv"] = argv
        logs.mkdir(parents=True, exist_ok=True)
        stdout, stderr = logs / "stdout.txt", logs / "stderr.txt"
        process.update(stdout=str(stdout), stderr=str(stderr))
        # Exclusive logs do not truncate an earlier run's evidence.
        with stdout.open("xb") as out, stderr.open("xb") as err:
            completed = subprocess.run(argv, cwd=contract["workspace"], stdin=subprocess.DEVNULL,
                                       stdout=out, stderr=err, timeout=timeout, shell=False)
        process["returncode"] = completed.returncode
        execution_status = "SUCCEEDED" if completed.returncode == 0 else "FAILED"
    except subprocess.TimeoutExpired:
        # subprocess.run kills and waits for its direct child. Descendant-producing
        # scripts are not supported; do not claim whole-process-tree isolation.
        process["timed_out"] = True
        execution_status = "TIMED_OUT"
    except (g.GateError, OSError, ValueError) as error:
        process["error"] = getattr(error, "code", type(error).__name__) + ": " + str(error)
    artifacts = []
    for name in unit["required_artifacts"]:
        try:
            sha = g.file_hash(g.scoped_path(name, contract["workspace"]), "MISSING_ARTIFACT")
        except g.GateError:
            sha = "0" * 64  # Submit failure evidence; never silently omit an expected output.
        artifacts.append({"path": name, "sha256": sha})
    receipt = {"identity": contract["identity"], "unit_id": unit["id"], "attempt_id": lease["attempt_id"],
               "execution_status": execution_status, "reported_conclusion": "UNASSESSED", "artifacts": artifacts,
               "usage": {"tool_calls": 1, "model_calls": 0, "tokens": 0,
                         "wall_ms": max(1, int((time.monotonic() - started) * 1000))}, "process": process}
    try:
        gate.submit(receipt)
        return True
    except g.GateError:
        return False


def run_step(contract_path, state_dir):
    """Execute once. Existing run databases are never reset or automatically resumed."""
    contract = g.read_json(Path(contract_path), "MISSING_CONTRACT")
    _validate(contract)
    gate = g.Gate.initialize(contract_path, state_dir)
    frozen = gate.status()["contract"]
    g.require(g.fingerprint(frozen) == g.fingerprint(contract), "CONTRACT_CHANGED")
    pending = list(frozen["units"])
    failed = False
    # ponytail: one invocation owns the run; reuse the existing gate transaction
    # instead of adding lease redemption, a dispatcher service, or another state machine.
    with ThreadPoolExecutor(max_workers=frozen["parallel_limit"]) as pool:
        while pending and not failed:
            accepted = {a["unit_id"] for a in gate.status()["attempts"].values() if a["status"] == "ACCEPTED"}
            futures = []
            for unit in list(pending):
                if not set(unit["depends_on"]) <= accepted:
                    continue
                try:
                    lease = gate.admit({"identity": frozen["identity"], "unit_id": unit["id"],
                                        "action": "offline_test", "session_paths": [frozen["workspace"]]})
                except g.GateError as error:
                    if error.code in ("RESOURCE_CONFLICT", "PARALLEL_LIMIT"):
                        continue
                    failed = True
                    break
                pending.remove(unit)
                futures.append(pool.submit(_execute, gate, frozen, unit, lease))
            if not futures:
                failed = True
            # Wait for admitted siblings even when one fails. Never leave a background worker.
            for future in futures:
                if not future.result():
                    failed = True
    # This decision closes the execution contract, NOT the scientific hypothesis
    # or the global master plan. All scientific conclusions remain UNASSESSED.
    return gate.finish({"identity": frozen["identity"], "decision": "MODIFY" if failed else "KEEP",
                        "next_step": frozen["next_step"]})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--state-dir", required=True)
    args = parser.parse_args(argv)
    try:
        state = run_step(args.contract, args.state_dir)
        ok = (len(state["attempts"]) == len(state["contract"]["units"])
              and all(a["status"] == "ACCEPTED" for a in state["attempts"].values()))
        print(json.dumps({"ok": ok, "phase": state["phase"], "next_step": state["next_step"],
                          "attempts": state["attempts"], "state_db": str(g.Gate(args.state_dir).db)}, indent=2))
        return 0 if ok else 1
    except (g.GateError, OSError, ValueError) as error:
        print(json.dumps({"ok": False, "code": getattr(error, "code", type(error).__name__), "message": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
