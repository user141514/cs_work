"""Run the entire offline gate suite; block network and subprocess launches.

Reports are written only to --output-dir; individual tests use temp directories.
This is a verifier, not a worker/model launcher or an auto-continuation service.
"""
import argparse
import ast
import hashlib
import io
import json
import platform
import socket
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="verification")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")
    transcript = io.StringIO()
    with patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
         patch.object(subprocess, "Popen", side_effect=AssertionError("process launch forbidden")):
        result = unittest.TextTestRunner(stream=transcript, verbosity=2).run(suite)
    hashes = {}
    syntax = "NOT_CHECKED"
    for source in sorted(root.rglob("*.py")):
        if "__pycache__" in source.parts:
            continue
        hashes[source.relative_to(root).as_posix()] = hashlib.sha256(source.read_bytes()).hexdigest()
        # Newer interpreters can parse the declared Python 3.7 grammar. On 3.7,
        # running these files itself checks that host's syntax/runtime subset.
        if sys.version_info >= (3, 8):
            ast.parse(source.read_text(encoding="utf-8"), filename=str(source), feature_version=(3, 7))
            syntax = "PYTHON_3_7_GRAMMAR_PASS_NOT_RUNTIME_PROOF"
    report = {
        "step": "WFE-02", "utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skipped": len(result.skipped),
        "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        "success": result.wasSuccessful(), "syntax_check": syntax,
        "network_and_subprocess_calls_blocked": True,
        "gate_has_model_or_network_client": False,
        "historical_fixture": "DEVELOPMENT_ONLY_SYNTHETIC_REGRESSION_NOT_REPLAY",
        "source_sha256": hashes,
        "scope": "Only the offline checker subsystem; not the whole bio_paper project or a live executor"
    }
    (output / "test_output.txt").write_text(transcript.getvalue(), encoding="utf-8")
    (output / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
