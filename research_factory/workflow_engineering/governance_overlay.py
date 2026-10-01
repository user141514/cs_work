#!/usr/bin/env python3
"""Materialize non-authoritative ARIS-style governance state from a finished Gate run."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import offline_gate as gate_mod

SCHEMA = "aris-governance-request-v1"
PROJECTION_SCHEMA = "aris-governance-projection-v1"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
TOP_KEYS = {"schema", "identity", "claim", "review", "evidence", "kill_boundary"}
CLAIM_KEYS = {"claim_id", "statement", "scope", "verdict"}
REVIEW_KEYS = {"kind", "reviewer", "verdict_id"}
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


def read_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as error:
        raise OverlayError("INVALID_REQUEST", str(error))
    fail(isinstance(value, dict), "INVALID_REQUEST")
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


def validate_request(request, source):
    fail(set(request) == TOP_KEYS and request.get("schema") == SCHEMA,
         "INVALID_REQUEST_SCHEMA")
    fail(request["identity"] == source["contract"]["identity"], "IDENTITY_MISMATCH")

    claim = request["claim"]
    review = request["review"]
    kill = request["kill_boundary"]
    fail(isinstance(claim, dict) and set(claim) == CLAIM_KEYS, "INVALID_CLAIM")
    fail(isinstance(review, dict) and set(review) == REVIEW_KEYS, "INVALID_REVIEW")
    fail(isinstance(kill, dict) and set(kill) == KILL_KEYS, "INVALID_KILL_BOUNDARY")
    fail(all(nonempty(claim[key]) for key in ("claim_id", "statement", "scope")),
         "INVALID_CLAIM")
    verdict = claim.get("verdict")
    kind = review.get("kind")
    fail(verdict in VERDICTS, "INVALID_CLAIM_VERDICT")
    fail(kind in REVIEW_KINDS, "INVALID_REVIEW_KIND")

    reviewer = review.get("reviewer")
    verdict_id = review.get("verdict_id")
    fail(isinstance(reviewer, str) and isinstance(verdict_id, str), "INVALID_REVIEW")
    if verdict == "UNASSESSED":
        fail(kind == "NONE" and not reviewer and not verdict_id, "INVALID_REVIEW")
    elif verdict == "PROVISIONAL":
        fail(kind != "NONE" and nonempty(reviewer) and nonempty(verdict_id),
             "INVALID_REVIEW")
    else:
        if kind == "SAME_FAMILY":
            raise OverlayError("SELF_ACQUITTAL")
        fail(kind in ("INDEPENDENT", "DETERMINISTIC")
             and nonempty(reviewer) and nonempty(verdict_id), "INVALID_REVIEW")

    fail(type(kill.get("closed")) is bool and nonempty(kill.get("scope")),
         "INVALID_KILL_BOUNDARY")
    anti_repeat = kill.get("anti_repeat")
    fail(isinstance(anti_repeat, list)
         and all(nonempty(item) for item in anti_repeat), "INVALID_KILL_BOUNDARY")
    if kill["closed"]:
        fail(bool(anti_repeat), "INVALID_KILL_BOUNDARY")

    evidence = request["evidence"]
    fail(isinstance(evidence, list) and evidence, "INVALID_EVIDENCE")
    verified = []
    for item in evidence:
        fail(isinstance(item, dict) and set(item) == {"path", "sha256"},
             "INVALID_EVIDENCE")
        expected = item.get("sha256")
        fail(nonempty(item.get("path")) and isinstance(expected, str)
             and bool(SHA256_RE.fullmatch(expected)), "INVALID_EVIDENCE")
        actual = file_sha256(item["path"])
        fail(actual.lower() == expected.lower(), "EVIDENCE_HASH_MISMATCH")
        verified.append({"path": item["path"], "sha256": actual})
    return verified


def project(state_dir, request_path, output_path):
    output = Path(output_path)
    fail(not output.exists(), "OUTPUT_EXISTS", str(output))

    gate = gate_mod.Gate(state_dir)
    source = gate.status()
    fail(source.get("phase") == "STOPPED", "SOURCE_NOT_STOPPED")

    request = read_json(request_path)
    evidence = validate_request(request, source)

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
        "evidence": evidence,
        "kill_boundary": request["kill_boundary"],
        "next_step": next_step,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError:
        raise OverlayError("OUTPUT_EXISTS", str(output))
    fail(json.loads(output.read_text(encoding="utf-8")) == result, "OUTPUT_READBACK_MISMATCH")
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
    print("GOVERNANCE_PROJECTION_WRITTEN " + str(args.output))
    print(json.dumps({"claim_verdict": result["claim"]["verdict"],
                      "authoritative": result["authoritative"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
