from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


F2P = [
    (
        "underscore_adjacent",
        0.15,
        """from dataclaw.anonymizer import anonymize_text
r = anonymize_text('config_alice_settings = True', 'alice', 'HASH')
assert 'alice' not in r and 'HASH' in r, r
""",
    ),
    (
        "underscore_prefix",
        0.10,
        """from dataclaw.anonymizer import _replace_username
r = _replace_username('Found in _alice folder', 'alice', 'HASH')
assert 'alice' not in r.lower() and 'HASH' in r, r
""",
    ),
    (
        "substring_safety",
        0.10,
        """from dataclaw.anonymizer import _replace_username
r1 = _replace_username('alexis is a good name', 'alex', 'HASH')
assert 'alexis' in r1, 'r1=' + r1
""",
    ),
    (
        "case_insensitive",
        0.10,
        """from dataclaw.anonymizer import _replace_username
r = _replace_username('Hello ALICE and Alice', 'alice', 'HASH')
assert 'ALICE' not in r and 'Alice' not in r, r
assert r.count('HASH') == 2, r
""",
    ),
    (
        "windows_backslash_short",
        0.15,
        r"""from dataclaw.anonymizer import anonymize_text
r = anonymize_text(r'C:\Users\bo\Documents\file.txt', 'bo', 'HASH')
assert 'HASH' in r, r
low = r.lower()
assert '\\users\\bo\\' not in low and '\\users\\bo' not in low.split('\\documents')[0]+'\\', r
""",
    ),
    (
        "custom_home_short",
        0.15,
        """from dataclaw.anonymizer import anonymize_text
r = anonymize_text('/opt/data/joe/project/file.py', 'joe', 'HASH', home='/opt/data/joe')
assert 'joe' not in r and 'HASH' in r, r
""",
    ),
    (
        "anonymizer_extras_underscore",
        0.10,
        """import dataclaw.anonymizer as mod
from dataclaw.anonymizer import Anonymizer, _hash_username
mod._detect_home_dir = lambda: ('/Users/owner', 'owner')
a = Anonymizer(extra_usernames=['alice', 'bob'])
out = a.text('hi alice and config_bob_settings, plus owner')
assert 'alice' not in out, out
assert 'bob' not in out, out
assert 'owner' not in out, out
assert _hash_username('alice') in out
assert _hash_username('bob') in out
""",
    ),
    (
        "compile_caching",
        0.15,
        """import re
import dataclaw.anonymizer as mod
mod._detect_home_dir = lambda: ('/Users/alice', 'alice')
from dataclaw.anonymizer import Anonymizer, anonymize_text
a = Anonymizer(extra_usernames=['bob', 'carol'])
a.text('hello alice and bob')
anonymize_text('hi alice', 'alice', 'HASH')
anonymize_text('/Users/bo/x', 'bo', 'HASH')
orig = re.compile
counter = {'n': 0}
def spy(*args, **kwargs):
    counter['n'] += 1
    return orig(*args, **kwargs)
re.compile = spy
try:
    for _ in range(50):
        a.text('alice did something with bob and carol in /Users/alice/x')
        anonymize_text('the user alice came by', 'alice', 'HASH')
        anonymize_text('/Users/bo/file', 'bo', 'HASH')
finally:
    re.compile = orig
assert counter['n'] <= 5, 'compile count too high: ' + str(counter['n'])
""",
    ),
]

P2P = [
    (
        "hash_determinism",
        """from dataclaw.anonymizer import _hash_username
h1 = _hash_username('alice'); h2 = _hash_username('alice'); h3 = _hash_username('bob')
assert h1 == h2 and h1 != h3
assert h1.startswith('user_') and len(h1) == 13
""",
    ),
    (
        "long_basic",
        """from dataclaw.anonymizer import anonymize_text
r = anonymize_text('hello alice', 'alice', 'HASH')
assert r == 'hello HASH', r
""",
    ),
    (
        "short_posix_path",
        """from dataclaw.anonymizer import anonymize_text
r = anonymize_text('/Users/bo/file.py', 'bo', 'HASH')
assert 'HASH' in r and '/Users/bo/' not in r, r
""",
    ),
    (
        "upstream_import",
        """from dataclaw.anonymizer import anonymize_text, anonymize_path, Anonymizer, _hash_username, _replace_username""",
    ),
]


def run_code(repo: Path, python: str, code: str) -> tuple[bool, str]:
    cp = subprocess.run(
        [python, "-B", "-c", code],
        cwd=str(repo),
        text=True,
        capture_output=True,
        timeout=30,
    )
    return cp.returncode == 0, (cp.stdout + cp.stderr).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--pytest", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    result: dict[str, object] = {
        "repo": str(repo),
        "python": args.python,
        "p2p": [],
        "f2p": [],
    }

    p2p_ok = True
    for gid, code in P2P:
        passed, detail = run_code(repo, args.python, code)
        result["p2p"].append({"id": gid, "passed": passed, "detail": detail})
        p2p_ok = p2p_ok and passed

    reward = 0.0
    for gid, weight, code in F2P:
        passed, detail = run_code(repo, args.python, code)
        result["f2p"].append(
            {"id": gid, "weight": weight, "passed": passed, "detail": detail}
        )
        if passed:
            reward += weight

    result["legacy_reward_before_p2p_cap"] = round(reward, 4)
    result["reward"] = round(reward if p2p_ok else 0.0, 4)
    result["p2p_all_pass"] = p2p_ok
    result["f2p_pass_count"] = sum(1 for x in result["f2p"] if x["passed"])

    if args.pytest:
        cp = subprocess.run(
            [args.python, "-B", "-m", "pytest", "-q"],
            cwd=str(repo),
            text=True,
            capture_output=True,
            timeout=120,
        )
        result["pytest"] = {
            "returncode": cp.returncode,
            "passed": cp.returncode == 0,
            "output": (cp.stdout + cp.stderr).strip(),
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
