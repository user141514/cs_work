"""WFE-04: validate a gate lease and prepare the real Stage-B launcher command.

This module is deliberately dry-run only. It never imports subprocess, opens a
network client, launches PowerShell, invokes run_stageb_agent.ps1, or advances a
workflow step. The gate remains the sole authority owner.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

import offline_gate as gate_mod

EXECUTOR_ID = "stageb-agent-launch-v1"
EXECUTOR_RELATIVE = Path("research_factory/computer_topconf_2027/run_stageb_agent.ps1")
RESULT_FIELDS = ["Backend", "SessionId", "ExitCode", "TimedOut", "StdOutLog", "StdErrLog", "Arm"]
ARM_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SESSION_RE = re.compile(r"^[A-Za-z0-9_.:-]*$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_text(value: Any, code: str, allow_empty: bool = False) -> str:
    gate_mod.require(isinstance(value, str), code)
    gate_mod.require(allow_empty or bool(value), code)
    gate_mod.require("\x00" not in value, code)
    return value


def _runtime_root(repo_root: Path) -> Path:
    if repo_root.drive:
        return Path(repo_root.drive + "\\") / "stageb_agent_runtime"
    return repo_root.parent / "stageb_agent_runtime"


def _within(candidate: Path, roots) -> bool:
    resolved = candidate.resolve()
    for root in roots:
        try:
            resolved.relative_to(Path(root).resolve())
            return True
        except ValueError:
            pass
    return False


def prepare_stageb_dry_run(gate: gate_mod.Gate,
                           lease: Dict[str, Any],
                           request: Dict[str, Any],
                           repo_root: Any) -> Dict[str, Any]:
    """Return a deterministic launch plan after revalidating current authority."""
    gate_mod.require(isinstance(request, dict), "INVALID_ADAPTER_REQUEST")
    validated = gate.validate_lease(lease)
    attempt = validated["attempt"]
    gate_mod.require(attempt["action"] == "offline_test", "DRY_RUN_ACTION_REQUIRED")

    root = Path(repo_root).resolve()
    script = (root / EXECUTOR_RELATIVE).resolve()
    try:
        script.relative_to(root)
    except ValueError:
        raise gate_mod.GateError("EXECUTOR_OUTSIDE_REPO")
    gate_mod.require(script.is_file(), "MISSING_EXECUTOR")

    expected_hash = _require_text(request.get("executor_sha256"), "INVALID_EXECUTOR_HASH")
    gate_mod.require(bool(SHA256_RE.fullmatch(expected_hash)), "INVALID_EXECUTOR_HASH")
    actual_hash = _sha256(script)
    gate_mod.require(actual_hash.casefold() == expected_hash.casefold(), "EXECUTOR_HASH_MISMATCH")

    workspace = validated["workspace"]
    prompt_value = _require_text(request.get("prompt_file"), "INVALID_PROMPT_FILE")
    prompt = gate_mod.scoped_path(prompt_value, workspace)
    gate_mod.require(prompt in attempt["reads"], "PROMPT_NOT_DECLARED")

    arm_name = _require_text(request.get("arm_name"), "INVALID_ARM_NAME")
    gate_mod.require(bool(ARM_RE.fullmatch(arm_name)) and arm_name not in (".", ".."), "INVALID_ARM_NAME")

    session_id = _require_text(request.get("session_id", ""), "INVALID_SESSION_ID", allow_empty=True)
    gate_mod.require(bool(SESSION_RE.fullmatch(session_id)), "INVALID_SESSION_ID")

    timeout = request.get("timeout_seconds")
    gate_mod.require(type(timeout) is int and 1 <= timeout <= 3600, "INVALID_TIMEOUT")

    argv = [
        "powershell.exe", "-NoProfile",
        "-File", str(script), "-Action", "Launch",
        "-PromptFile", prompt, "-ArmName", arm_name,
        "-TimeoutSeconds", str(timeout),
    ]
    if session_id:
        argv.extend(["-SessionId", session_id])

    freeze_receipt = root / "external/spec_stageb_logs/stageb_backend_freeze.json"
    log_root = root / "external/spec_stageb_logs"
    runtime_root = _runtime_root(root)
    projected_arm = runtime_root / "arms" / arm_name
    projected_venv = runtime_root / "venvs" / arm_name
    if session_id:
        venv_python = projected_venv / "Scripts/python.exe"
        preconditions = [
            {"name": "backend_freeze_receipt", "path": str(freeze_receipt), "exists": freeze_receipt.is_file()},
            {"name": "resume_arm", "path": str(projected_arm), "exists": projected_arm.is_dir()},
            {"name": "resume_python", "path": str(venv_python), "exists": venv_python.is_file()},
        ]
    else:
        source_arm = root / "external/spec_stageb_s1_local"
        preconditions = [
            {"name": "backend_freeze_receipt", "path": str(freeze_receipt), "exists": freeze_receipt.is_file()},
            {"name": "source_arm", "path": str(source_arm), "exists": source_arm.is_dir()},
        ]

    path_alignment = {
        "arm_within_declared_session_paths": _within(projected_arm, attempt["session_paths"]),
        "log_root_within_declared_writes": _within(log_root, attempt["writes"]),
    }
    gaps = ["atomic_dispatch_claim", "executor_parameters_not_frozen_in_gate"]
    if not all(path_alignment.values()):
        gaps.append("executor_path_ownership")
    if session_id:
        gaps.append("session_identity_not_bound_to_gate")

    return {
        "mode": "DRY_RUN",
        "would_launch": False,
        "executor_id": EXECUTOR_ID,
        "executor_script": str(script),
        "executor_sha256": actual_hash,
        "attempt_id": attempt["attempt_id"],
        "unit_id": attempt["unit_id"],
        "task_workspace": workspace,
        "session_paths": list(attempt["session_paths"]),
        "prompt_file": prompt,
        "argv": argv,
        "working_directory": str(root),
        "expected_executor_result_fields": list(RESULT_FIELDS),
        "projected_executor_paths": {
            "runtime_root": str(runtime_root),
            "arm": str(projected_arm),
            "venv": str(projected_venv),
            "log_root": str(log_root),
        },
        "path_alignment": path_alignment,
        "live_preconditions": preconditions,
        "live_ready": all(item["exists"] for item in preconditions) and not gaps,
        "side_effects_if_live": [
            "create or modify drive-level stageb_agent_runtime state",
            "create or modify repository external/spec_stageb_logs",
            "initialize or resume an isolated Stage-B arm and virtualenv",
            "start a Codex or Claude process selected by the frozen backend receipt",
            "write stdout/stderr execution logs",
        ],
        "remaining_enforcement_gaps": gaps,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--lease", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args(argv)

    try:
        lease = gate_mod.read_json(Path(args.lease), "INVALID_LEASE_JSON")
        request = gate_mod.read_json(Path(args.request), "INVALID_ADAPTER_REQUEST")
        plan = prepare_stageb_dry_run(
            gate=gate_mod.Gate(args.state_dir),
            lease=lease,
            request=request,
            repo_root=args.repo_root,
        )
        print(json.dumps({"ok": True, "plan": plan}, indent=2, sort_keys=True))
        return 0
    except gate_mod.GateError as error:
        print(json.dumps({"ok": False, "code": error.code, "message": str(error)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
