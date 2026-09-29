You are an outcome-blind dependency-scope annotator for a controlled coding-agent experiment.

Your ONLY job is to classify which pre-revision derived work can be safely reused after a late requirement change, and which reasoning must be rederived.

You are deliberately NOT given any benchmark verifier, hidden tests, reference patch, gold solution, canonical goals, post-revision run, or successful future trajectory. Do not infer or invent them.

## Frozen user requirement history

U1:
Read `git diff main windows` for the changes in this branch. Review them.

U2:
Is there any visible issue in the changes?

U4:
Add tests in tests/test_anonymizer.py to cover the changes.

LATE REVISION U5:
Compile the regexes in the anonymizer. How else can we speedup the anonymizer?

Historical workflow-only requests are omitted because they do not change the product contract.

## Frozen task state before U5

Current production source:

```python
"""Anonymize PII in Claude Code log data.

NOTE: This is the buggy intermediate state for the `windows` branch in the
Harbor task. It unifies ``anonymize_path`` into ``anonymize_text`` and adds
partial Windows support, but intentionally contains the bugs the agent is
expected to surface and fix:

  * ``\\b`` word boundaries — fails when the username is adjacent to an
    underscore (``config_alice_settings``).
  * ``re.sub`` is called with a fresh pattern on every call — no caching.
  * ``_replace_username`` does a plain ``str.replace`` — matches substrings,
    so ``alex`` also replaces inside ``alexis``.
  * No ``\\Users\\`` backslash support for short (<4 char) usernames.
  * ``home`` parameter is accepted but never used for custom home dirs.
  * No case-insensitive matching for short-username ``Users``/``home`` paths.
"""

import hashlib
import os
import re

def _hash_username(username: str) -> str:
    return "user_" + hashlib.sha256(username.encode()).hexdigest()[:8]

def _detect_home_dir() -> tuple[str, str]:
    home = os.path.expanduser("~")
    username = os.path.basename(home)
    return home, username

def anonymize_text(text: str, username: str, username_hash: str, home: str | None = None) -> str:
    if not text or not username:
        return text
    escaped = re.escape(username)
    if len(username) >= 4:
        return re.sub(rf"\b{escaped}\b", username_hash, text)
    text = re.sub(
        rf"([/\-]+(?:Users|home)[/\-]+){escaped}(?=[^a-zA-Z0-9]|$)",
        rf"\g<1>{username_hash}",
        text,
    )
    return text

anonymize_path = anonymize_text

class Anonymizer:
    def __init__(self, extra_usernames: list[str] | None = None):
        self.home, self.username = _detect_home_dir()
        self.username_hash = _hash_username(self.username)
        self._extra: list[tuple[str, str]] = []
        for name in extra_usernames or []:
            name = name.strip()
            if name and name != self.username and len(name) >= 3:
                self._extra.append((name, _hash_username(name)))

    def path(self, file_path: str) -> str:
        return self.text(file_path)

    def text(self, content: str) -> str:
        result = anonymize_text(content, self.username, self.username_hash, self.home)
        for name, hashed in self._extra:
            result = _replace_username(result, name, hashed)
        return result

def _replace_username(text: str, username: str, username_hash: str) -> str:
    if not text or not username or len(username) < 3:
        return text
    return text.replace(username, username_hash)
```

Pre-revision agent-derived work after U4:
- Only tests/test_anonymizer.py changed.
- Production code is unchanged.
- Six new behavioral regression tests were added:
  1. long username between underscores;
  2. short username in Windows backslash path;
  3. case-insensitive short-username path;
  4. short username under custom home;
  5. case-insensitive configured username replacement;
  6. preservation of longer names when replacing a shorter name.
- Current test result after these additions: 7 failed, 25 passed.
- The seventh failure is an already-existing case-insensitive long-username test.
- No performance/caching test was added.
- No production implementation was changed.

Exact pre-revision patch:

```diff
diff --git a/tests/test_anonymizer.py b/tests/test_anonymizer.py
index c195077..c66c8bc 100644
--- a/tests/test_anonymizer.py
+++ b/tests/test_anonymizer.py
@@ -75,6 +75,11 @@
+def test_long_username_between_underscores():
+    assert anonymize_text("config_alice_settings", "alice", HASH) == \
+        f"config_{HASH}_settings"
@@ -96,6 +101,23 @@
+def test_short_username_windows_path():
+    assert anonymize_text(
+        r"C:\Users\bo\Documents\file.txt", "bo", HASH,
+    ) == rf"C:\Users\{HASH}\Documents\file.txt"
+
+def test_short_username_path_is_case_insensitive():
+    assert anonymize_text("/USERS/BO/work", "bo", HASH) == \
+        f"/USERS/{HASH}/work"
+
+def test_short_username_custom_home():
+    assert anonymize_text(
+        "/srv/accounts/bo/work", "bo", HASH, home="/srv/accounts/bo",
+    ) == f"/srv/accounts/{HASH}/work"
@@ -126,6 +148,16 @@
+def test_replace_username_is_case_insensitive():
+    assert _replace_username("Alice and ALICE", "alice", HASH) == \
+        f"{HASH} and {HASH}"
+
+def test_replace_username_preserves_larger_names():
+    assert _replace_username("alex met alexis", "alex", HASH) == \
+        f"{HASH} met alexis"
```

## Classification target

The late requirement U5 changes the implementation/performance contract:
1. regexes should be compiled/cached rather than rebuilt each call;
2. at least one further concrete speedup should be considered, and possibly implemented.

Classify the PRE-REVISION derived work into exactly three sets:

INDEPENDENT_REUSABLE:
work whose validity does not depend on how U5 is implemented and can be carried forward unchanged.

IMPACTED_RECHECK:
work that is still potentially useful but must be revalidated after U5 because the new implementation can affect it.

MUST_REDERIVE:
reasoning/decisions that directly depend on the old per-call-regex implementation or must be recomputed to satisfy U5.

Then give:
- MINIMAL_R3_CAPSULE: the smallest text/artifact capsule a fresh post-revision agent may receive while still legitimately reusing independent prior work.
- INVALIDATION_RULE: what must be omitted from that capsule.
- COUNTEREXAMPLE: one observation that would prove your dependency classification too optimistic.

Do not propose a solution patch. Do not use hidden benchmark knowledge.