#!/usr/bin/env python3
"""Materialize non-authoritative ARIS-style governance state from a finished Gate run."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

import offline_gate as gate_mod

SCHEMA = "aris-governance-request-v1"
PROJECTION_SCHEMA = "aris-governance-projection-v1"
REVIEW_RECEIPT_SCHEMA = "aris-governance-review-receipt-v2"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
FAMILY_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
TOP_KEYS = {"schema", "projection_root", "identity", "claim", "review", "evidence", "kill_boundary"}
CLAIM_KEYS = {"claim_id", "statement", "scope", "verdict"}
REVIEW_KEYS = {
    "kind", "reviewer", "verdict_id", "receipt_path", "receipt_sha256",
    "executor_family", "reviewer_family",
}
RECEIPT_KEYS = {
    "schema", "claim_id", "claim_statement", "claim_scope", "verdict", "kind",
    "reviewer", "verdict_id", "executor_family", "reviewer_family",
    "source_identity", "evidence",
}
KILL_KEYS = {"closed", "scope", "anti_repeat"}
VERDICTS = {"UNASSESSED", "PROVISIONAL", "SUPPORTED", "REFUTED"}
REVIEW_KINDS = {"NONE", "SAME_FAMILY", "INDEPENDENT", "DETERMINISTIC"}


class OverlayError(Exception):
    def __init__(self, code, message=""):
        super().__init__(code + (": " + message if message else ""))
        self.code = code


def fail(condition, code, message=""):
    if not condition:
        raise OverlayError(code, message)


def read_json(path, code="INVALID_REQUEST"):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as error:
        raise OverlayError(code, str(error))
    fail(isinstance(value, dict), code)
    return value


def file_sha256(path):
    path = Path(path)
    fail(path.is_file(), "MISSING_EVIDENCE", str(path))
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def canonical_family(value):
    fail(nonempty(value), "INVALID_REVIEW_FAMILY")
    fail(value == value.strip() and value == value.casefold()
         and bool(FAMILY_RE.fullmatch(value)), "INVALID_REVIEW_FAMILY")
    return value


def canonical_evidence(items):
    result = []
    for item in items:
        fail(isinstance(item, dict) and set(item) == {"path", "sha256"},
             "INVALID_REVIEW_RECEIPT")
        result.append({
            "path": normpath(item["path"]),
            "sha256": str(item["sha256"]).lower(),
        })
    return sorted(result, key=lambda item: (item["path"], item["sha256"]))


def normpath(value):
    # Path.resolve() normalizes Windows 8.3 aliases (ADMINI~1) to the same
    # canonical spelling Gate.scoped_path() uses. strict=False keeps future
    # projection roots valid before their directory exists.
    return os.path.normcase(str(Path(value).resolve(strict=False)))


def inside(path, root):
    path = normpath(path)
    root = normpath(root)
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:
        return False


def overlaps(left, right):
    return inside(left, right) or inside(right, left)


def authoritative_evidence(source):
    contract = source["contract"]
    workspace = contract["workspace"]
    result = {}
    for item in list(contract.get("inputs", [])) + [contract.get("evaluator")]:
        if not isinstance(item, dict):
            continue
        path = gate_mod.scoped_path(item["path"], workspace)
        result[normpath(path)] = item["sha256"]
    for attempt in source.get("attempts", {}).values():
        if attempt.get("status") != "ACCEPTED":
            continue
        # Gate stores absolute artifact hashes after submit, while the frozen
        # submitted receipt retains the contract-relative artifact path.
        # On Windows those two views may differ only by an 8.3 short-path alias
        # (ADMINI~1 vs Administrator). Admit both Gate-owned spellings instead
        # of trying to guess filesystem alias equivalence.
        submitted = attempt.get("submitted_receipt", {})
        for item in submitted.get("artifacts", []):
            if not isinstance(item, dict):
                continue
            relative = item.get("path")
            digest = item.get("sha256")
            if nonempty(relative) and isinstance(digest, str):
                path = gate_mod.scoped_path(relative, workspace)
                result[normpath(path)] = digest
        for path, digest in attempt.get("artifact_hashes", {}).items():
            result[normpath(path)] = digest
    return result


def verify_authoritative_file(path, expected, allowed, not_authoritative_code):
    key = normpath(path)
    fail(key in allowed, not_authoritative_code, str(path))
    fail(isinstance(expected, str) and bool(SHA256_RE.fullmatch(expected)),
         "INVALID_EVIDENCE")
    authoritative_hash = allowed[key]
    fail(expected.lower() == authoritative_hash.lower(), "EVIDENCE_HASH_MISMATCH")
    actual = file_sha256(path)
    fail(actual.lower() == authoritative_hash.lower(), "EVIDENCE_HASH_MISMATCH")
    return actual


def validate_output_scope(state_dir, source, request, output):
    root_value = request.get("projection_root")
    fail(nonempty(root_value), "INVALID_REQUEST_SCHEMA")
    projection_root = Path(root_value)
    output = Path(output)
    fail(inside(output, projection_root) and normpath(output) != normpath(projection_root),
         "OUTPUT_OUTSIDE_PROJECTION_ROOT")
    fail(normpath(output.parent) == normpath(projection_root),
         "OUTPUT_OUTSIDE_PROJECTION_ROOT")
    workspace = source["contract"]["workspace"]
    fail(not overlaps(projection_root, state_dir)
         and not overlaps(projection_root, workspace), "OUTPUT_SCOPE_CONFLICT")
    return {
        "projection_root": projection_root,
        "projection_root_norm": normpath(projection_root),
        "output_norm": normpath(output),
        "state_dir": Path(state_dir),
        "workspace": Path(workspace),
    }


def _path_chain(path):
    path = Path(path).resolve(strict=False)
    return list(reversed(path.parents)) + [path]


@contextmanager
def _stable_output_scope(scope, output):
    output = Path(output)
    projection_root = Path(scope["projection_root"])
    projection_root.mkdir(parents=True, exist_ok=True)
    handles = []
    fds = []
    try:
        if os.name == "nt":
            from ctypes import wintypes
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            create_file = kernel32.CreateFileW
            create_file.argtypes = [
                wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
            ]
            create_file.restype = wintypes.HANDLE
            get_attrs = kernel32.GetFileAttributesW
            get_attrs.argtypes = [wintypes.LPCWSTR]
            get_attrs.restype = wintypes.DWORD
            close_handle = kernel32.CloseHandle
            close_handle.argtypes = [wintypes.HANDLE]

            invalid_handle = ctypes.c_void_p(-1).value
            for directory in _path_chain(projection_root):
                attrs = get_attrs(str(directory))
                fail(attrs != 0xFFFFFFFF and not (attrs & 0x400),
                     "OUTPUT_SCOPE_CHANGED", str(directory))
                handle = create_file(
                    str(directory),
                    0x0001 | 0x0080,  # FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES
                    0x1 | 0x2,  # SHARE_READ | SHARE_WRITE; deny DELETE retarget
                    None,
                    3,          # OPEN_EXISTING
                    0x02000000, # FILE_FLAG_BACKUP_SEMANTICS
                    None,
                )
                fail(handle != invalid_handle, "OUTPUT_SCOPE_CHANGED", str(directory))
                handles.append((handle, close_handle))
        else:
            flags = os.O_RDONLY
            flags |= getattr(os, "O_DIRECTORY", 0)
            flags |= getattr(os, "O_NOFOLLOW", 0)
            for directory in _path_chain(projection_root):
                try:
                    fds.append(os.open(str(directory), flags))
                except OSError as error:
                    raise OverlayError("OUTPUT_SCOPE_CHANGED", str(error))

        fail(normpath(projection_root) == scope["projection_root_norm"]
             and normpath(output) == scope["output_norm"],
             "OUTPUT_SCOPE_CHANGED")
        fail(not overlaps(projection_root, scope["state_dir"])
             and not overlaps(projection_root, scope["workspace"]),
             "OUTPUT_SCOPE_CHANGED")
        yield
    finally:
        for fd in reversed(fds):
            os.close(fd)
        for handle, close_handle in reversed(handles):
            close_handle(handle)


def validate_review(claim, review, allowed, source_identity, verified_evidence):
    fail(isinstance(review, dict) and set(review) == REVIEW_KEYS, "INVALID_REVIEW")
    kind = review.get("kind")
    fail(kind in REVIEW_KINDS, "INVALID_REVIEW_KIND")
    for key in ("reviewer", "verdict_id", "receipt_path", "receipt_sha256",
                "executor_family", "reviewer_family"):
        fail(isinstance(review.get(key), str), "INVALID_REVIEW")

    verdict = claim["verdict"]
    if verdict == "UNASSESSED":
        fail(kind == "NONE"
             and all(not review[key] for key in REVIEW_KEYS - {"kind"}),
             "INVALID_REVIEW")
        return None

    fail(kind != "NONE", "INVALID_REVIEW")
    for key in ("reviewer", "verdict_id", "receipt_path", "receipt_sha256"):
        fail(nonempty(review[key]), "INVALID_REVIEW")
    executor_family = canonical_family(review["executor_family"])
    reviewer_family = canonical_family(review["reviewer_family"])

    receipt_hash = verify_authoritative_file(
        review["receipt_path"], review["receipt_sha256"], allowed,
        "REVIEW_RECEIPT_NOT_AUTHORITATIVE")
    receipt = read_json(review["receipt_path"], "INVALID_REVIEW_RECEIPT")
    fail(set(receipt) == RECEIPT_KEYS
         and receipt.get("schema") == REVIEW_RECEIPT_SCHEMA,
         "INVALID_REVIEW_RECEIPT")
    expected_fields = {
        "claim_id": claim["claim_id"],
        "claim_statement": claim["statement"],
        "claim_scope": claim["scope"],
        "verdict": claim["verdict"],
        "kind": review["kind"],
        "reviewer": review["reviewer"],
        "verdict_id": review["verdict_id"],
        "executor_family": executor_family,
        "reviewer_family": reviewer_family,
        "source_identity": source_identity,
        "evidence": canonical_evidence(verified_evidence),
    }
    for key, expected in expected_fields.items():
        fail(receipt.get(key) == expected, "REVIEW_RECEIPT_MISMATCH")

    if verdict == "PROVISIONAL":
        fail(kind == "SAME_FAMILY" and executor_family == reviewer_family,
             "INVALID_REVIEW")
    else:
        if kind == "SAME_FAMILY":
            raise OverlayError("SELF_ACQUITTAL")
        fail(kind in ("INDEPENDENT", "DETERMINISTIC"), "INVALID_REVIEW")
        if kind == "INDEPENDENT":
            fail(executor_family != reviewer_family, "SELF_ACQUITTAL")
        else:
            fail(reviewer_family == "deterministic"
                 and review["reviewer"].startswith("deterministic:"),
                 "INVALID_REVIEW")
    return {"path": review["receipt_path"], "sha256": receipt_hash}


def validate_request(request, source):
    fail(set(request) == TOP_KEYS and request.get("schema") == SCHEMA,
         "INVALID_REQUEST_SCHEMA")
    fail(request["identity"] == source["contract"]["identity"], "IDENTITY_MISMATCH")

    claim = request["claim"]
    kill = request["kill_boundary"]
    fail(isinstance(claim, dict) and set(claim) == CLAIM_KEYS, "INVALID_CLAIM")
    fail(isinstance(kill, dict) and set(kill) == KILL_KEYS, "INVALID_KILL_BOUNDARY")
    fail(all(nonempty(claim[key]) for key in ("claim_id", "statement", "scope")),
         "INVALID_CLAIM")
    fail(claim.get("verdict") in VERDICTS, "INVALID_CLAIM_VERDICT")

    allowed = authoritative_evidence(source)
    verified = []
    evidence = request["evidence"]
    fail(isinstance(evidence, list) and evidence, "INVALID_EVIDENCE")
    for item in evidence:
        fail(isinstance(item, dict) and set(item) == {"path", "sha256"},
             "INVALID_EVIDENCE")
        fail(nonempty(item.get("path")), "INVALID_EVIDENCE")
        actual = verify_authoritative_file(
            item["path"], item.get("sha256"), allowed, "EVIDENCE_NOT_AUTHORITATIVE")
        verified.append({"path": item["path"], "sha256": actual})

    review_receipt = validate_review(
        claim, request["review"], allowed, source["contract"]["identity"], verified)

    fail(type(kill.get("closed")) is bool and nonempty(kill.get("scope")),
         "INVALID_KILL_BOUNDARY")
    anti_repeat = kill.get("anti_repeat")
    fail(isinstance(anti_repeat, list)
         and all(nonempty(item) for item in anti_repeat), "INVALID_KILL_BOUNDARY")
    if kill["closed"]:
        fail(bool(anti_repeat), "INVALID_KILL_BOUNDARY")
    return verified, review_receipt


def write_atomic_exclusive(output, result, scope):
    output = Path(output)
    with _stable_output_scope(scope, output):
        fail(not os.path.lexists(str(output)), "OUTPUT_EXISTS", str(output))
        temporary = output.with_name(output.name + ".tmp-" + uuid.uuid4().hex)
        raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
        try:
            with temporary.open("xb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            fail(normpath(output.parent) == scope["projection_root_norm"],
                 "OUTPUT_SCOPE_CHANGED")
            try:
                os.link(str(temporary), str(output))
            except FileExistsError:
                raise OverlayError("OUTPUT_EXISTS", str(output))
        finally:
            if temporary.exists():
                temporary.unlink()
        fail(output.read_bytes() == raw, "OUTPUT_READBACK_MISMATCH")


def project(state_dir, request_path, output_path):
    output = Path(output_path)
    gate = gate_mod.Gate(state_dir)
    source = gate.status()
    fail(source.get("phase") == "STOPPED", "SOURCE_NOT_STOPPED")

    request = read_json(request_path)
    output_scope = validate_output_scope(state_dir, source, request, output)
    projection_root = output_scope["projection_root"]
    evidence, review_receipt = validate_request(request, source)

    statuses = {}
    for attempt in source.get("attempts", {}).values():
        status = attempt.get("status", "UNKNOWN")
        statuses[status] = statuses.get(status, 0) + 1

    next_step = source.get("next_step")
    if isinstance(next_step, dict):
        next_step = dict(next_step)
        next_step["authorized"] = False

    result = {
        "schema": PROJECTION_SCHEMA,
        "authoritative": False,
        "projection_only": True,
        "projection_root": str(projection_root),
        "source": {
            "identity": source["contract"]["identity"],
            "contract_fingerprint": gate_mod.fingerprint(source["contract"]),
        },
        "execution": {
            "phase": source["phase"],
            "decision": source.get("decision"),
            "attempt_status_counts": statuses,
        },
        "claim": request["claim"],
        "review": request["review"],
        "review_receipt": review_receipt,
        "evidence": evidence,
        "kill_boundary": request["kill_boundary"],
        "next_step": next_step,
    }
    write_atomic_exclusive(output, result, output_scope)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        result = project(args.state_dir, args.request, args.output)
    except OverlayError as error:
        print("GOVERNANCE_OVERLAY_ERROR " + error.code, file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "GOVERNANCE_PROJECTION_WRITTEN",
        "output": str(args.output),
        "claim_verdict": result["claim"]["verdict"],
        "authoritative": result["authoritative"],
    }, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
