"""WFE-02: model-free admission/receipt gate. Not an executor or an OS sandbox.

One SQLite database belongs to one frozen, explicitly authorized current step.
All checks and state reservations share a transaction. Trusted coordinator owns
contract/state files; workers may only use the future controlled adapter.
"""
import argparse
import copy
import hashlib
import json
import ntpath
import os
import sqlite3
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path, PureWindowsPath
from typing import Any, Dict, List, Optional

IDENTITY_KEYS = {"task_id", "task_version", "workflow_id", "workflow_version",
                 "plan_id", "plan_version", "step_id", "run_id"}
RESOURCES = ("tool_calls", "model_calls", "tokens", "wall_ms")
OFFLINE_ACTIONS = {"offline_read", "offline_test", "offline_write"}


class GateError(Exception):
    """A stable, machine-readable denial; never a scientific conclusion."""
    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        super().__init__(message or code)


def require(condition: bool, code: str, message: str = "") -> None:
    if not condition:
        raise GateError(code, message)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def read_json(path: Path, code: str = "INVALID_JSON") -> Dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as error:
        raise GateError(code, str(error))
    require(isinstance(value, dict), code, "Expected a JSON object")
    return value


def overlap(left: str, right: str) -> bool:
    """Conservative case-insensitive resource overlap, including directories."""
    a, b = left.replace("\\", "/").rstrip("/").casefold(), right.replace("\\", "/").rstrip("/").casefold()
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def scoped_path(value: str, workspace: str) -> str:
    """Resolve a declared path inside a root; check portable Windows fixtures too.

    On a non-Windows host, Windows paths get lexical checks only, not a claim
    about that machine's symlinks/junctions. Real gate workspaces must be native.
    """
    require(isinstance(value, str) and bool(value) and "\x00" not in value,
            "INVALID_PATH", "Expected a non-empty path")
    root = str(workspace)
    windows_root = bool(PureWindowsPath(root).drive)
    if windows_root and os.name != "nt":
        require(PureWindowsPath(root).is_absolute(), "INVALID_PATH")
        require(not PureWindowsPath(value).drive or PureWindowsPath(value).is_absolute(), "WORKSPACE_ESCAPE")
        base = ntpath.normcase(ntpath.normpath(root))
        candidate = ntpath.normcase(ntpath.normpath(ntpath.join(base, value)))
        try:
            valid = ntpath.commonpath([base, candidate]) == base
        except ValueError:
            valid = False
        require(valid, "WORKSPACE_ESCAPE", value)
        return candidate.replace("\\", "/")
    if os.name != "nt":
        require(not PureWindowsPath(value).drive and not value.startswith("\\"), "WORKSPACE_ESCAPE", value)
    try:
        base_path = Path(root).resolve()
        candidate_path = (base_path / value).resolve()
        candidate_path.relative_to(base_path)
    except (OSError, RuntimeError, ValueError) as error:
        raise GateError("WORKSPACE_ESCAPE", "{}: {}".format(value, error))
    return str(candidate_path)


def file_hash(path: str, code: str) -> str:
    try:
        target = Path(path)
        require(target.is_file(), code, "Not a regular file: " + path)
        hasher = hashlib.sha256()
        with target.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(block)
        return hasher.hexdigest()
    except OSError as error:
        raise GateError(code, str(error))


def identity_valid(identity: Any) -> None:
    require(isinstance(identity, dict) and set(identity) == IDENTITY_KEYS, "INVALID_IDENTITY")
    for key, value in identity.items():
        if key in ("plan_version", "task_version"):
            require(type(value) is int and value > 0, "INVALID_IDENTITY", key)
        else:
            require(isinstance(value, str) and bool(value.strip()), "INVALID_IDENTITY", key)


def numbers(value: Any, keys: Any, code: str) -> None:
    require(isinstance(value, dict) and set(value) == set(keys), code)
    require(all(type(v) is int and v >= 0 for v in value.values()), code)


def string_list(value: Any, code: str, nonempty: bool = False) -> None:
    require(isinstance(value, list), code)
    require(all(isinstance(v, str) and bool(v.strip()) for v in value), code)
    require(len(value) == len(set(value)) and (bool(value) or not nonempty), code)


def artifact_map(items: Any, workspace: str, code: str) -> Dict[str, str]:
    require(isinstance(items, list), code)
    result = {}
    for item in items:
        require(isinstance(item, dict) and set(item) == {"path", "sha256"}, code)
        path = scoped_path(item["path"], workspace)
        sha = item["sha256"]
        require(isinstance(sha, str) and len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), code)
        require(path not in result, code, "Duplicate artifact")
        result[path] = sha
    return result


def check_hashes(manifest: Dict[str, str], code: str) -> None:
    for path, expected in manifest.items():
        require(file_hash(path, code) == expected, code, path)


def validate_contract(contract: Dict[str, Any]) -> None:
    identity_valid(contract.get("identity"))
    require(contract.get("authorized") is True and contract.get("status") == "ACTIVE", "NOT_AUTHORIZED")
    for key in ("goal", "acceptance", "stop_condition", "workspace"):
        require(isinstance(contract.get(key), str) and bool(contract[key].strip()), "INVALID_CONTRACT", key)
    require(contract["stop_condition"] == "STOP_AFTER_CURRENT_STEP", "INVALID_CONTRACT")
    root = Path(contract["workspace"])
    require(root.is_absolute() and root.is_dir(), "INVALID_WORKSPACE")
    numbers(contract.get("budget"), ("attempts",) + RESOURCES, "INVALID_BUDGET")
    require(contract.get("mode") == "OFFLINE_ONLY" and contract["budget"]["model_calls"] == 0
            and contract["budget"]["tokens"] == 0, "OFFLINE_ONLY")
    require(type(contract.get("parallel_limit")) is int and 1 <= contract["parallel_limit"] <= 2,
            "INVALID_PARALLEL_LIMIT")
    frozen = artifact_map(contract.get("inputs"), str(root), "INVALID_CONTRACT")
    require(bool(frozen), "INVALID_CONTRACT", "Initial inputs required")
    evaluator = artifact_map([contract.get("evaluator")], str(root), "INVALID_CONTRACT")
    check_hashes(frozen, "FROZEN_INPUT_CHANGED")
    check_hashes(evaluator, "EVALUATOR_CHANGED")
    string_list(contract.get("protected_paths"), "INVALID_CONTRACT")
    protected = list(frozen) + list(evaluator) + [scoped_path(p, str(root)) for p in contract["protected_paths"]]
    units = contract.get("units")
    require(isinstance(units, list) and bool(units), "INVALID_UNITS")
    by_id = {}
    for unit in units:
        require(isinstance(unit, dict) and isinstance(unit.get("id"), str) and bool(unit["id"]), "INVALID_UNITS")
        require(unit["id"] not in by_id, "INVALID_UNITS", "Duplicate unit id")
        by_id[unit["id"]] = unit
        for key in ("depends_on", "reads", "writes", "required_artifacts", "actions"):
            string_list(unit.get(key), "INVALID_UNIT", nonempty=key in ("required_artifacts", "actions"))
        numbers(unit.get("reservation"), RESOURCES, "INVALID_BUDGET")
        require(unit["reservation"]["model_calls"] == 0 and unit["reservation"]["tokens"] == 0
                and set(unit["actions"]) <= OFFLINE_ACTIONS, "OFFLINE_ONLY")
        writes = [scoped_path(p, str(root)) for p in unit["writes"]]
        reads = [scoped_path(p, str(root)) for p in unit["reads"]]
        require(not any(overlap(w, p) for w in writes for p in protected + reads), "PROTECTED_WRITE")
        for path in unit["required_artifacts"]:
            resolved = scoped_path(path, str(root))
            require(any(resolved == w or resolved.startswith(w.rstrip(os.sep) + os.sep) for w in writes),
                    "ARTIFACT_OUTSIDE_WRITE_SCOPE", path)
    for unit in units:
        require(set(unit["depends_on"]) <= set(by_id), "UNKNOWN_DEPENDENCY")
    ancestry = {}
    visiting = set()
    def ancestors(name):
        require(name not in visiting, "DEPENDENCY_CYCLE")
        if name in ancestry:
            return ancestry[name]
        visiting.add(name)
        result = set(by_id[name]["depends_on"])
        for dep in by_id[name]["depends_on"]:
            result.update(ancestors(dep))
        visiting.remove(name)
        ancestry[name] = result
        return result
    for name in by_id:
        ancestors(name)
    for reader in units:
        for writer in units:
            if reader["id"] == writer["id"]:
                continue
            intersection = any(overlap(scoped_path(r, str(root)), scoped_path(w, str(root)))
                               for r in reader["reads"] for w in writer["writes"])
            require(not intersection or writer["id"] in ancestry[reader["id"]], "UNDECLARED_DEPENDENCY")


def scope_snapshot(contract: Dict[str, Any]) -> Dict[str, Any]:
    """Pin resolved aliases as well as the textual contract; aliases can change."""
    root = contract["workspace"]
    return {"root": str(Path(root).resolve()), "units": {
        unit["id"]: {key: [scoped_path(p, root) for p in unit[key]]
                     for key in ("reads", "writes", "required_artifacts")}
        for unit in contract["units"]}}


class Gate:
    """Transactional coordinator-side guard. Never dispatches a worker."""
    def __init__(self, state_dir: Any) -> None:
        self.state_dir = Path(state_dir).resolve()
        self.db = self.state_dir / "gate.sqlite3"

    @classmethod
    def initialize(cls, contract_path: Any, state_dir: Any) -> "Gate":
        path = Path(contract_path).resolve()
        contract = read_json(path, "MISSING_CONTRACT")
        validate_contract(contract)
        gate = cls(state_dir)
        root = str(Path(contract["workspace"]).resolve())
        require(not overlap(str(gate.state_dir), root) and not overlap(str(path), root), "CONTROL_INSIDE_WORKSPACE")
        gate.state_dir.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(gate.db), timeout=10, isolation_level=None)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), value TEXT NOT NULL)")
            require(connection.execute("SELECT id FROM state WHERE id=1").fetchone() is None, "STATE_EXISTS")
            state = {"schema_version": 1, "phase": "ACTIVE", "contract_path": str(path),
                     "contract_digest": fingerprint(contract), "contract": contract,
                     "scopes": scope_snapshot(contract),
                     "attempts": {}, "reserved": dict.fromkeys(("attempts",) + RESOURCES, 0),
                     "reported_usage": dict.fromkeys(RESOURCES, 0), "events": [], "next_step": None}
            connection.execute("INSERT INTO state(id,value) VALUES(1,?)", (canonical(state),))
            connection.execute("COMMIT")
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return gate

    @contextmanager
    def _transaction(self):
        require(self.db.is_file(), "NOT_INITIALIZED")
        connection = sqlite3.connect(str(self.db), timeout=10, isolation_level=None)
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT value FROM state WHERE id=1").fetchone()
            require(row is not None, "NOT_INITIALIZED")
            state = json.loads(row[0])
            yield state
            connection.execute("UPDATE state SET value=? WHERE id=1", (canonical(state),))
            connection.execute("COMMIT")
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def status(self) -> Dict[str, Any]:
        require(self.db.is_file(), "NOT_INITIALIZED")
        connection = sqlite3.connect(str(self.db), timeout=10)
        try:
            row = connection.execute("SELECT value FROM state WHERE id=1").fetchone()
            require(row is not None, "NOT_INITIALIZED")
            return json.loads(row[0])
        finally:
            connection.close()

    def validate_lease(self, lease: Dict[str, Any]) -> Dict[str, Any]:
        """Revalidate a currently RUNNING admitted lease without changing its state."""
        with self._transaction() as state:
            self._identity(state, lease)
            self._authority(state)
            require(isinstance(lease.get("attempt_id"), str), "UNKNOWN_ATTEMPT")
            attempt = state["attempts"].get(lease["attempt_id"])
            require(attempt is not None and attempt["unit_id"] == lease.get("unit_id"), "UNKNOWN_ATTEMPT")
            require(attempt["status"] == "RUNNING", "LEASE_NOT_ACTIVE")
            require(attempt["action"] == lease.get("action") and attempt["identity"] == lease.get("identity"),
                    "STALE_LEASE")
            check_hashes(attempt["read_hashes"], "READ_SET_CHANGED")
            return {"attempt": copy.deepcopy(attempt), "workspace": state["contract"]["workspace"]}

    @staticmethod
    def _identity(state, request):
        require(isinstance(request, dict), "STALE_IDENTITY")
        try:
            identity_valid(request.get("identity"))
        except GateError:
            raise GateError("STALE_IDENTITY")
        require(request["identity"] == state["contract"]["identity"], "STALE_IDENTITY")
        require(state["phase"] == "ACTIVE", "STEP_STOPPED")

    @staticmethod
    def _authority(state):
        current = read_json(Path(state["contract_path"]), "CONTRACT_CHANGED")
        try:
            same = fingerprint(current) == state["contract_digest"]
        except (ValueError, TypeError):
            same = False
        require(same, "CONTRACT_CHANGED")
        contract = state["contract"]
        require(scope_snapshot(contract) == state["scopes"], "SCOPE_CHANGED")
        root = contract["workspace"]
        check_hashes(artifact_map(contract["inputs"], root, "INVALID_CONTRACT"), "FROZEN_INPUT_CHANGED")
        check_hashes(artifact_map([contract["evaluator"]], root, "INVALID_CONTRACT"), "EVALUATOR_CHANGED")

    @staticmethod
    def _unit(state, name):
        units = [u for u in state["contract"]["units"] if u["id"] == name]
        require(len(units) == 1, "UNKNOWN_UNIT")
        return units[0]

    @staticmethod
    def _event(state, event, **fields):
        state["events"].append(dict(sequence=len(state["events"]) + 1, event=event, **fields))

    def admit(self, request: Dict[str, Any]) -> Dict[str, Any]:
        with self._transaction() as state:
            self._identity(state, request)
            self._authority(state)
            unit = self._unit(state, request.get("unit_id"))
            require(request.get("action") in unit["actions"], "UNAUTHORIZED_ACTION")
            attempts = list(state["attempts"].values())
            require(not any(a["unit_id"] == unit["id"] for a in attempts), "ALREADY_ADMITTED")
            require(not any(a["status"] == "INVALID" for a in attempts), "REPLAN_REQUIRED")
            root = state["contract"]["workspace"]
            string_list(request.get("session_paths"), "SESSION_PATHS_REQUIRED")
            session_paths = [scoped_path(path, root) for path in request["session_paths"]]
            for dependency in unit["depends_on"]:
                previous = [a for a in attempts if a["unit_id"] == dependency and a["status"] == "ACCEPTED"]
                require(bool(previous), "DEPENDENCY_NOT_READY", dependency)
                check_hashes(previous[0]["artifact_hashes"], "DEPENDENCY_EVIDENCE_CHANGED")
            active = [a for a in attempts if a["status"] == "RUNNING"]
            require(len(active) < state["contract"]["parallel_limit"], "PARALLEL_LIMIT")
            reads = [scoped_path(p, root) for p in unit["reads"]]
            writes = [scoped_path(p, root) for p in unit["writes"]]
            for other in active:
                conflict = any(overlap(w, p) for w in writes for p in other["reads"] + other["writes"])
                conflict = conflict or any(overlap(w, p) for w in other["writes"] for p in reads)
                require(not conflict, "RESOURCE_CONFLICT")
            reservation = dict(unit["reservation"], attempts=1)
            require(all(state["reserved"][k] + v <= state["contract"]["budget"][k]
                        for k, v in reservation.items()), "BUDGET_EXCEEDED")
            read_hashes = {path: file_hash(path, "MISSING_READ") for path in reads}
            for name in unit["required_artifacts"]:
                require(not Path(scoped_path(name, root)).exists(), "PREEXISTING_ARTIFACT", name)
            attempt_id = uuid.uuid4().hex
            record = {"attempt_id": attempt_id, "unit_id": unit["id"], "action": request["action"],
                      "identity": copy.deepcopy(request["identity"]), "status": "RUNNING",
                      "reads": reads, "writes": writes, "session_paths": session_paths,
                      "read_hashes": read_hashes, "reservation": reservation,
                      "scientific_conclusion": "UNASSESSED"}
            state["attempts"][attempt_id] = record
            for key, amount in reservation.items():
                state["reserved"][key] += amount
            self._event(state, "ADMITTED", attempt_id=attempt_id, unit_id=unit["id"])
            return copy.deepcopy(record)

    def submit(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        rejection = None
        result = None
        with self._transaction() as state:
            self._identity(state, receipt)
            try:
                canonical(receipt)
            except (TypeError, ValueError):
                raise GateError("INVALID_RECEIPT", "Receipt must be finite JSON")
            require(isinstance(receipt.get("attempt_id"), str), "UNKNOWN_ATTEMPT")
            attempt = state["attempts"].get(receipt.get("attempt_id"))
            require(attempt is not None and attempt["unit_id"] == receipt.get("unit_id"), "UNKNOWN_ATTEMPT")
            require(attempt["status"] == "RUNNING", "DUPLICATE_RECEIPT")
            unit = self._unit(state, attempt["unit_id"])
            attempt["reported_conclusion"] = receipt.get("reported_conclusion", "UNASSESSED")
            attempt["execution_status"] = receipt.get("execution_status", "UNKNOWN")
            attempt["submitted_receipt"] = copy.deepcopy(receipt)
            try:
                usage = receipt.get("usage")
                numbers(usage, RESOURCES, "INVALID_USAGE")
                for key in RESOURCES:
                    state["reported_usage"][key] += usage[key]
                attempt["usage"] = copy.deepcopy(usage)
                require(all(usage[k] <= attempt["reservation"][k] for k in RESOURCES), "USAGE_EXCEEDED")
                self._authority(state)
                root = state["contract"]["workspace"]
                # Re-resolve read paths to detect a symlink/junction target change.
                current_reads = [scoped_path(p, root) for p in unit["reads"]]
                require(current_reads == attempt["reads"], "READ_SET_CHANGED")
                check_hashes(attempt["read_hashes"], "READ_SET_CHANGED")
                require(receipt.get("execution_status") == "SUCCEEDED", "EXECUTION_FAILED")
                manifest = artifact_map(receipt.get("artifacts"), root, "INVALID_ARTIFACT_MANIFEST")
                required = {scoped_path(p, root) for p in unit["required_artifacts"]}
                require(set(manifest) == required, "ARTIFACT_SET_MISMATCH")
                for path, expected in manifest.items():
                    require(any(path == w or path.startswith(w.rstrip(os.sep) + os.sep) for w in attempt["writes"]),
                            "ARTIFACT_OUTSIDE_WRITE_SCOPE")
                    require(file_hash(path, "MISSING_ARTIFACT") == expected, "ARTIFACT_HASH_MISMATCH", path)
                    require(Path(path).stat().st_nlink == 1, "LINKED_ARTIFACT", path)
                attempt.update(status="ACCEPTED", evidence_status="STRUCTURALLY_VALID", artifact_hashes=manifest)
                self._event(state, "RECEIPT_ACCEPTED", attempt_id=attempt["attempt_id"])
            except GateError as error:
                rejection = error
                attempt.update(status="INVALID", evidence_status="INVALID", rejection_code=error.code,
                               scientific_conclusion="UNASSESSED")
                self._event(state, "RECEIPT_REJECTED", attempt_id=attempt["attempt_id"], code=error.code)
            result = copy.deepcopy(attempt)
        # Commit the failed attempt and its costs BEFORE reporting rejection.
        if rejection is not None:
            raise rejection
        return result

    def finish(self, request: Dict[str, Any]) -> Dict[str, Any]:
        with self._transaction() as state:
            self._identity(state, request)
            decision = request.get("decision")
            require(decision in ("KEEP", "MODIFY", "TERMINATE"), "INVALID_DECISION")
            try:
                self._authority(state)
            except GateError as error:
                if decision == "KEEP":
                    raise
                # Closing/replanning a broken run is not accepting its evidence.
                state["closure_validation_error"] = error.code
            next_step = request.get("next_step")
            if decision == "TERMINATE":
                require(next_step is None, "INVALID_NEXT_STEP")
            else:
                require(isinstance(next_step, dict), "INVALID_NEXT_STEP")
                require(next_step.get("authorized", False) is False, "NEXT_STEP_NOT_AUTHORIZED")
                require(set(next_step) <= {"id", "question", "authorized"}
                        and isinstance(next_step.get("id"), str) and bool(next_step["id"].strip())
                        and next_step["id"] != state["contract"]["identity"]["step_id"]
                        and isinstance(next_step.get("question"), str) and bool(next_step["question"].strip()),
                        "INVALID_NEXT_STEP")
                next_step = dict(next_step, authorized=False)
            attempts = list(state["attempts"].values())
            require(not any(a["status"] == "RUNNING" for a in attempts), "WORK_IN_PROGRESS")
            if decision == "KEEP":
                require(not any(a["status"] == "INVALID" for a in attempts), "INVALID_EVIDENCE")
                require(len(attempts) == len(state["contract"]["units"])
                        and all(a["status"] == "ACCEPTED" for a in attempts), "STEP_INCOMPLETE")
                for attempt in attempts:
                    check_hashes(attempt["artifact_hashes"], "ARTIFACT_CHANGED_AFTER_SUBMIT")
            state.update(phase="STOPPED", decision=decision, next_step=next_step)
            self._event(state, "STEP_STOPPED", decision=decision)
            return copy.deepcopy(state)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("init", "admit", "submit", "finish", "status"))
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--contract")
    parser.add_argument("--request")
    args = parser.parse_args(argv)
    try:
        if args.operation == "init":
            require(bool(args.contract), "MISSING_CONTRACT")
            result = Gate.initialize(args.contract, args.state_dir).status()
        else:
            gate = Gate(args.state_dir)
            if args.operation == "status":
                result = gate.status()
            else:
                require(bool(args.request), "MISSING_REQUEST")
                result = getattr(gate, args.operation)(read_json(Path(args.request)))
        print(canonical({"ok": True, "result": result}))
        return 0
    except (GateError, OSError, sqlite3.Error) as error:
        print(canonical({"ok": False, "code": getattr(error, "code", "STATE_IO_ERROR"), "message": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
