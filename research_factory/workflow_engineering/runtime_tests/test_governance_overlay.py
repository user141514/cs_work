from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "runtime_tests") not in sys.path:
    sys.path.insert(0, str(ROOT / "runtime_tests"))

import offline_gate as gate_mod
import local_runner
from test_local_runner import fixture, pin

try:
    import governance_overlay
except ImportError:
    governance_overlay = None


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2), encoding="utf-8")


class GovernanceOverlayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.assertIsNotNone(governance_overlay, "governance_overlay is not implemented")

    def tearDown(self):
        self.tmp.cleanup()

    def stopped(self, base=None):
        base = base or (self.base / "run")
        contract_path, state_dir, work, contract = fixture(base, modes=("ok",))
        state = local_runner.run_step(contract_path, state_dir)
        evidence = work / "out/a/result.json"
        self.assertEqual(state["phase"], "STOPPED")
        self.assertTrue(evidence.is_file())
        return contract_path, state_dir, work, contract, evidence

    def stopped_with_review(self, verdict, kind, reviewer, executor_family, reviewer_family,
                            base=None, receipt_identity=None):
        base = base or (self.base / ("review-" + kind.lower()))
        contract_path, state_dir, work, contract = fixture(base, modes=("ok",))
        evidence = work / "inputs/value.json"
        receipt_path = work / "inputs/review_receipt.json"
        receipt = {
            "schema": "aris-governance-review-receipt-v2",
            "claim_id": "claim:test",
            "claim_statement": "Frozen test claim",
            "claim_scope": "Only the frozen local-run evidence",
            "verdict": verdict,
            "kind": kind,
            "reviewer": reviewer,
            "verdict_id": "receipt-1",
            "executor_family": executor_family,
            "reviewer_family": reviewer_family,
            "source_identity": receipt_identity or contract["identity"],
            "evidence": [{
                "path": governance_overlay.normpath(evidence),
                "sha256": sha256(evidence).lower(),
            }],
        }
        dump(receipt_path, receipt)
        contract["inputs"].append(pin(work, "inputs/review_receipt.json"))
        dump(contract_path, contract)
        state = local_runner.run_step(contract_path, state_dir)
        self.assertEqual(state["phase"], "STOPPED")
        return state_dir, work, contract, evidence, receipt_path

    def request(self, contract, evidence, verdict="UNASSESSED", kind="NONE",
                reviewer="", verdict_id="", receipt_path=None, executor_family="",
                reviewer_family="", closed=False, projection_root=None):
        projection_root = projection_root or (self.base / "governance")
        receipt_path = Path(receipt_path) if receipt_path else None
        return {
            "schema": "aris-governance-request-v1",
            "projection_root": str(projection_root),
            "identity": contract["identity"],
            "claim": {
                "claim_id": "claim:test",
                "statement": "Frozen test claim",
                "scope": "Only the frozen local-run evidence",
                "verdict": verdict,
            },
            "review": {
                "kind": kind,
                "reviewer": reviewer,
                "verdict_id": verdict_id,
                "receipt_path": str(receipt_path) if receipt_path else "",
                "receipt_sha256": sha256(receipt_path) if receipt_path else "",
                "executor_family": executor_family,
                "reviewer_family": reviewer_family,
            },
            "evidence": [{"path": str(evidence), "sha256": sha256(evidence)}],
            "kill_boundary": {
                "closed": closed,
                "scope": "Exact frozen realization",
                "anti_repeat": ["no post-result parameter rescue"] if closed else [],
            },
        }

    def project(self, state_dir, request):
        req = self.base / "request.json"
        root = Path(request["projection_root"])
        out = root / "projection.json"
        dump(req, request)
        result = governance_overlay.project(state_dir, req, out)
        return result, out

    def denied(self, code, state_dir, request, output=None):
        req = self.base / "request.json"
        root = Path(request["projection_root"])
        out = output or (root / "projection.json")
        dump(req, request)
        with self.assertRaises(governance_overlay.OverlayError) as caught:
            governance_overlay.project(state_dir, req, out)
        self.assertEqual(caught.exception.code, code)
        return out

    def test_unassessed_projection_is_non_authoritative_and_copies_disabled_next_step(self):
        _, state_dir, _, contract, evidence = self.stopped()
        before = gate_mod.Gate(state_dir).status()
        result, out = self.project(state_dir, self.request(contract, evidence))
        after = gate_mod.Gate(state_dir).status()

        self.assertEqual(before, after)
        self.assertEqual(result["schema"], "aris-governance-projection-v1")
        self.assertFalse(result["authoritative"])
        self.assertTrue(result["projection_only"])
        self.assertEqual(result["execution"]["phase"], "STOPPED")
        self.assertEqual(result["claim"]["verdict"], "UNASSESSED")
        self.assertEqual(result["review"]["kind"], "NONE")
        self.assertFalse(result["next_step"]["authorized"])
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")), result)

    def test_same_family_supported_is_rejected_but_provisional_passes(self):
        state_dir, _, contract, evidence, receipt = self.stopped_with_review(
            "SUPPORTED", "SAME_FAMILY", "codex", "openai", "openai",
            base=self.base / "bad")
        bad = self.request(contract, evidence, verdict="SUPPORTED", kind="SAME_FAMILY",
                           reviewer="codex", verdict_id="receipt-1", receipt_path=receipt,
                           executor_family="openai", reviewer_family="openai",
                           projection_root=self.base / "bad-governance")
        self.denied("SELF_ACQUITTAL", state_dir, bad)

        state_dir, _, contract, evidence, receipt = self.stopped_with_review(
            "PROVISIONAL", "SAME_FAMILY", "codex", "openai", "openai",
            base=self.base / "good")
        good = self.request(contract, evidence, verdict="PROVISIONAL", kind="SAME_FAMILY",
                            reviewer="codex", verdict_id="receipt-1", receipt_path=receipt,
                            executor_family="openai", reviewer_family="openai",
                            projection_root=self.base / "good-governance")
        result, _ = self.project(state_dir, good)
        self.assertEqual(result["claim"]["verdict"], "PROVISIONAL")

    def test_independent_and_deterministic_final_verdicts_require_frozen_receipts(self):
        cases = (
            ("SUPPORTED", "INDEPENDENT", "claude-review", "openai", "anthropic"),
            ("REFUTED", "DETERMINISTIC", "deterministic:contract-check", "openai", "deterministic"),
        )
        for verdict, kind, reviewer, executor_family, reviewer_family in cases:
            with self.subTest(verdict=verdict, kind=kind):
                case = self.base / (verdict + kind)
                state_dir, _, contract, evidence, receipt = self.stopped_with_review(
                    verdict, kind, reviewer, executor_family, reviewer_family,
                    base=case / "run")
                req = self.request(
                    contract, evidence, verdict=verdict, kind=kind, reviewer=reviewer,
                    verdict_id="receipt-1", receipt_path=receipt,
                    executor_family=executor_family, reviewer_family=reviewer_family,
                    closed=(verdict == "REFUTED"), projection_root=case / "governance")
                req_path = case / "request.json"
                out = case / "governance/projection.json"
                dump(req_path, req)
                result = governance_overlay.project(state_dir, req_path, out)
                self.assertEqual(result["claim"]["verdict"], verdict)
                self.assertEqual(result["review"]["kind"], kind)

    def test_receipt_binds_claim_scope_evidence_and_source_identity(self):
        state_dir, work, contract, evidence, receipt = self.stopped_with_review(
            "SUPPORTED", "INDEPENDENT", "claude-review", "openai", "anthropic",
            base=self.base / "binding")

        valid = self.request(
            contract, evidence, verdict="SUPPORTED", kind="INDEPENDENT",
            reviewer="claude-review", verdict_id="receipt-1", receipt_path=receipt,
            executor_family="openai", reviewer_family="anthropic",
            projection_root=self.base / "binding-valid")
        self.project(state_dir, valid)

        for field, replacement in (
            ("statement", "Different claim text"),
            ("scope", "Broader unsupported scope"),
        ):
            req = self.request(
                contract, evidence, verdict="SUPPORTED", kind="INDEPENDENT",
                reviewer="claude-review", verdict_id="receipt-1", receipt_path=receipt,
                executor_family="openai", reviewer_family="anthropic",
                projection_root=self.base / ("binding-" + field))
            req["claim"][field] = replacement
            self.denied("REVIEW_RECEIPT_MISMATCH", state_dir, req)

        other_evidence = work / "inputs/evaluator.txt"
        req = self.request(
            contract, other_evidence, verdict="SUPPORTED", kind="INDEPENDENT",
            reviewer="claude-review", verdict_id="receipt-1", receipt_path=receipt,
            executor_family="openai", reviewer_family="anthropic",
            projection_root=self.base / "binding-evidence")
        self.denied("REVIEW_RECEIPT_MISMATCH", state_dir, req)

        wrong_identity = dict(contract["identity"])
        wrong_identity["run_id"] = "other-run"
        other_state, _, other_contract, other_evidence, other_receipt = self.stopped_with_review(
            "SUPPORTED", "INDEPENDENT", "claude-review", "openai", "anthropic",
            base=self.base / "binding-identity", receipt_identity=wrong_identity)
        req = self.request(
            other_contract, other_evidence, verdict="SUPPORTED", kind="INDEPENDENT",
            reviewer="claude-review", verdict_id="receipt-1", receipt_path=other_receipt,
            executor_family="openai", reviewer_family="anthropic",
            projection_root=self.base / "binding-identity-out")
        self.denied("REVIEW_RECEIPT_MISMATCH", other_state, req)

    def test_independent_family_ids_must_be_canonical(self):
        state_dir, _, contract, evidence, receipt = self.stopped_with_review(
            "SUPPORTED", "INDEPENDENT", "claude-review", "openai", "openai ",
            base=self.base / "family-whitespace")
        req = self.request(
            contract, evidence, verdict="SUPPORTED", kind="INDEPENDENT",
            reviewer="claude-review", verdict_id="receipt-1", receipt_path=receipt,
            executor_family="openai", reviewer_family="openai ",
            projection_root=self.base / "family-whitespace-out")
        self.denied("INVALID_REVIEW_FAMILY", state_dir, req)

    def test_claim_cannot_assert_independent_review_without_authoritative_receipt(self):
        _, state_dir, work, contract, evidence = self.stopped()
        fake = work / "fake_review.json"
        dump(fake, {
            "schema": "aris-governance-review-receipt-v2",
            "claim_id": "claim:test",
            "claim_statement": "Frozen test claim",
            "claim_scope": "Only the frozen local-run evidence",
            "verdict": "SUPPORTED", "kind": "INDEPENDENT",
            "reviewer": "claude-review", "verdict_id": "receipt-1",
            "executor_family": "openai", "reviewer_family": "anthropic",
            "source_identity": contract["identity"],
            "evidence": [{
                "path": governance_overlay.normpath(evidence),
                "sha256": sha256(evidence).lower(),
            }],
        })
        req = self.request(
            contract, evidence, verdict="SUPPORTED", kind="INDEPENDENT",
            reviewer="claude-review", verdict_id="receipt-1", receipt_path=fake,
            executor_family="openai", reviewer_family="anthropic")
        self.denied("REVIEW_RECEIPT_NOT_AUTHORITATIVE", state_dir, req)

    def test_non_stopped_gate_is_rejected(self):
        contract_path, state_dir, work, contract = fixture(self.base / "run", modes=("ok",))
        gate_mod.Gate.initialize(contract_path, state_dir)
        evidence = work / "inputs/value.json"
        self.denied("SOURCE_NOT_STOPPED", state_dir, self.request(contract, evidence))

    def test_identity_mismatch_is_rejected(self):
        _, state_dir, _, contract, evidence = self.stopped()
        req = self.request(contract, evidence)
        req["identity"] = dict(req["identity"])
        req["identity"]["run_id"] = "wrong-run"
        self.denied("IDENTITY_MISMATCH", state_dir, req)

    def test_evidence_must_be_authoritative_and_hash_matched(self):
        _, state_dir, work, contract, evidence = self.stopped()
        req = self.request(contract, evidence)
        req["evidence"][0]["sha256"] = "0" * 64
        self.denied("EVIDENCE_HASH_MISMATCH", state_dir, req)

        arbitrary = work / "posthoc.json"
        dump(arbitrary, {"invented": True})
        req = self.request(contract, arbitrary, projection_root=self.base / "other-governance")
        self.denied("EVIDENCE_NOT_AUTHORITATIVE", state_dir, req)

    def test_projection_root_cannot_overlap_gate_or_execution_workspace(self):
        _, state_dir, work, contract, evidence = self.stopped()
        req = self.request(contract, evidence, projection_root=Path(state_dir) / "governance")
        self.denied("OUTPUT_SCOPE_CONFLICT", state_dir, req)

        req = self.request(contract, evidence, projection_root=work / "governance")
        self.denied("OUTPUT_SCOPE_CONFLICT", state_dir, req)

    def test_projection_root_retarget_after_validation_is_rejected(self):
        _, state_dir, work, contract, evidence = self.stopped()
        projection_root = self.base / "safe-projection"
        projection_root.mkdir()
        req = self.request(contract, evidence, projection_root=projection_root)
        original_validate = governance_overlay.validate_request

        def retarget_after_validation(request, source):
            result = original_validate(request, source)
            projection_root.rmdir()
            if os.name == "nt":
                completed = subprocess.run(
                    ["cmd.exe", "/d", "/c", "mklink", "/J",
                     str(projection_root), str(work)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.assertEqual(completed.returncode, 0, completed.stderr.decode(errors="replace"))
            else:
                projection_root.symlink_to(work, target_is_directory=True)
            return result

        target = work / "projection.json"
        try:
            with patch.object(governance_overlay, "validate_request",
                              side_effect=retarget_after_validation):
                self.denied("OUTPUT_SCOPE_CHANGED", state_dir, req)
            self.assertFalse(target.exists())
        finally:
            if projection_root.exists() or projection_root.is_symlink():
                if os.name == "nt":
                    subprocess.run(["cmd.exe", "/d", "/c", "rmdir", str(projection_root)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    projection_root.unlink()

    @unittest.skipUnless(os.name == "nt", "Windows CP936 CLI regression")
    def test_cli_nonascii_output_path_is_cp936_safe_after_write(self):
        _, state_dir, _, contract, evidence = self.stopped()
        projection_root = self.base / "governance-📚"
        req = self.request(contract, evidence, projection_root=projection_root)
        req_path = self.base / "cp936-request.json"
        output = projection_root / "projection.json"
        dump(req_path, req)
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "cp936:strict"
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / "governance_overlay.py"),
             "--state-dir", str(state_dir), "--request", str(req_path),
             "--output", str(output)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("cp936", errors="replace"))
        completed.stdout.decode("cp936", errors="strict")
        self.assertTrue(output.is_file())
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertFalse(payload["authoritative"])
        self.assertFalse(payload["next_step"]["authorized"])

    @unittest.skipUnless(os.name == "nt", "Windows junction lock regression")
    def test_windows_scope_lock_blocks_retarget_while_held(self):
        _, state_dir, _, contract, evidence = self.stopped()
        projection_root = self.base / "locked-projection"
        projection_root.mkdir()
        req = self.request(contract, evidence, projection_root=projection_root)
        output = projection_root / "projection.json"
        source = gate_mod.Gate(state_dir).status()
        scope = governance_overlay.validate_output_scope(state_dir, source, req, output)

        with governance_overlay._stable_output_scope(scope, output):
            remove = subprocess.run(
                ["cmd.exe", "/d", "/c", "rmdir", str(projection_root)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertNotEqual(remove.returncode, 0)
            self.assertTrue(projection_root.is_dir())

        remove = subprocess.run(
            ["cmd.exe", "/d", "/c", "rmdir", str(projection_root)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(remove.returncode, 0, remove.stderr.decode(errors="replace"))

    def test_duplicate_output_is_rejected_atomically_without_mutating_gate(self):
        _, state_dir, _, contract, evidence = self.stopped()
        before = gate_mod.Gate(state_dir).status()
        req = self.request(contract, evidence)
        result, out = self.project(state_dir, req)
        original = out.read_bytes()
        self.assertFalse(list(out.parent.glob("*.tmp-*")))

        req_path = self.base / "request2.json"
        dump(req_path, req)
        with self.assertRaises(governance_overlay.OverlayError) as caught:
            governance_overlay.project(state_dir, req_path, out)
        self.assertEqual(caught.exception.code, "OUTPUT_EXISTS")
        self.assertEqual(original, out.read_bytes())
        self.assertEqual(before, gate_mod.Gate(state_dir).status())
        self.assertEqual(result, json.loads(out.read_text(encoding="utf-8")))

    def test_concurrent_writers_same_output_exactly_one_wins_with_typed_loser(self):
        _, state_dir, _, contract, evidence = self.stopped()
        before = gate_mod.Gate(state_dir).status()
        req = self.request(contract, evidence)
        req_path = self.base / "concurrent-request.json"
        dump(req_path, req)
        output = Path(req["projection_root"]) / "projection.json"
        ready_paths = [self.base / "writer-1.ready", self.base / "writer-2.ready"]
        release = self.base / "writers.release"

        worker = "\n".join([
            "import os",
            "import sys",
            "import time",
            "from pathlib import Path",
            "import governance_overlay as g",
            "ready = Path(sys.argv[1])",
            "release = Path(sys.argv[2])",
            "state_dir, request_path, output_path = sys.argv[3:6]",
            "target = os.path.normcase(os.path.abspath(output_path))",
            "original_lexists = g.os.path.lexists",
            "armed = [False]",
            "def rendezvous(path):",
            "    exists = original_lexists(path)",
            "    if not armed[0] and os.path.normcase(os.path.abspath(str(path))) == target and not exists:",
            "        armed[0] = True",
            "        ready.write_text('ready', encoding='ascii')",
            "        deadline = time.time() + 10.0",
            "        while not release.exists():",
            "            if time.time() > deadline:",
            "                raise RuntimeError('concurrency rendezvous timed out')",
            "            time.sleep(0.001)",
            "    return exists",
            "g.os.path.lexists = rendezvous",
            "raise SystemExit(g.main(['--state-dir', state_dir, '--request', request_path, '--output', output_path]))",
        ])

        processes = [
            subprocess.Popen(
                [sys.executable, "-B", "-c", worker, str(ready), str(release),
                 str(state_dir), str(req_path), str(output)],
                cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for ready in ready_paths
        ]
        try:
            deadline = __import__("time").time() + 10.0
            while not all(path.exists() for path in ready_paths):
                if any(process.poll() is not None for process in processes):
                    break
                if __import__("time").time() > deadline:
                    break
                __import__("time").sleep(0.001)
            self.assertTrue(all(path.exists() for path in ready_paths),
                            "both writers must reach the exclusive-create race")
            release.write_text("go", encoding="ascii")
            completed = [process.communicate(timeout=15) for process in processes]
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.wait()

        outcomes = []
        for process, (stdout, stderr) in zip(processes, completed):
            stdout_text = stdout.decode("ascii", errors="strict")
            stderr_text = stderr.decode("ascii", errors="strict")
            self.assertNotIn("Traceback", stderr_text)
            self.assertNotIn("PermissionError", stderr_text)
            if process.returncode == 0:
                payload = json.loads(stdout_text)
                self.assertEqual(payload["status"], "GOVERNANCE_PROJECTION_WRITTEN")
                self.assertEqual(stderr_text, "")
                outcomes.append("success")
            else:
                self.assertEqual(process.returncode, 2)
                self.assertEqual(stdout_text, "")
                self.assertEqual(stderr_text.strip(), "GOVERNANCE_OVERLAY_ERROR OUTPUT_EXISTS")
                outcomes.append("OUTPUT_EXISTS")

        self.assertEqual(sorted(outcomes), ["OUTPUT_EXISTS", "success"])
        projection = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(projection["schema"], "aris-governance-projection-v1")
        self.assertFalse(projection["authoritative"])
        self.assertTrue(projection["projection_only"])
        self.assertFalse(projection["next_step"]["authorized"])
        self.assertFalse(list(output.parent.glob("*.tmp-*")))
        self.assertEqual(before, gate_mod.Gate(state_dir).status())

    def test_authority_fields_in_request_are_rejected(self):
        _, state_dir, _, contract, evidence = self.stopped()
        req = self.request(contract, evidence)
        req["next_step"] = {"id": "illegal", "authorized": True}
        self.denied("INVALID_REQUEST_SCHEMA", state_dir, req)


if __name__ == "__main__":
    unittest.main()
