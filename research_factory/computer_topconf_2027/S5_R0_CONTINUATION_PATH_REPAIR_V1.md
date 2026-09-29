# S5 R0 Continuation Path Repair V1

date: 2026-09-28
status: FROZEN_INFRASTRUCTURE_REPAIR_BEFORE_VALID_R0_OUTCOME
task: pi-mono-auto-ec7037ba
arm: R0 RAW_HISTORY

## Failure

Invalid attempt:
- request_key: s5-r0-raw-history-v1
- turn_id: turn_443ad4246e4149d6a5869049ae062e4c
- declared lifetime workspace: C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-11ee2ca4
- copied session history originated from: C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-0421b2d6

Observed invariant violation:
- OMP continuation retained absolute paths from the pre-revision session.
- Its first write targeted the old common worktree path ...-0421b2d6, not the declared ...-11ee2ca4 worktree.
- Therefore lifetime ownership and actual write ownership diverged.

Verdict:
INVALID_HARNESS.
No output, token/cost, edit, verifier result, or scientific conclusion from v1 is admissible.

The turn was cancelled and reached:
- outcome = cancelled
- phase = terminal
- quiescent = true

## Recovery evidence

Immutable logical pre-revision identity:
- task initial commit: 69d02b8a5fce07041f77aba64c6ebbc8589827ab
- exact binary common patch hash: 2a884cfb7425d810bc6965068f517459752c5588
- pristine U1-U4 session source: D:/bio_paper/external/spec_stageb_sessions/s5_common_pre_v1

Independent frozen workspace replica:
- C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-11ee2ca4
- verified binary diff hash: 2a884cfb7425d810bc6965068f517459752c5588
- this replica is no longer an experimental writer.

The original absolute common path was restored by:
1. reset to the frozen task initial commit;
2. reapply the exact saved binary patch;
3. require git diff --check PASS;
4. require binary diff hash = 2a884cfb7425d810bc6965068f517459752c5588.

Restored continuation path:
- C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-0421b2d6

## New invariant

A stateful coding-agent session is:

session transcript/state
+
workspace bytes
+
workspace absolute identity.

For RAW_HISTORY continuation:
- do not relocate the session to a different workspace path unless the session format is explicitly path-relocatable and this is verified;
- preserve an immutable independent snapshot/receipt first;
- continue the arm at the original absolute workspace identity;
- keep lifetime's declared workspace equal to the path the agent actually reads/writes.

Snapshot immutability is provided by the independent replica + exact patch/session receipts, not by requiring the historical physical path to remain forever unused.

## Valid R0 v2 plan

- source prestate bytes: restored ...-0421b2d6 at hash 2a884cf...
- immutable frozen replica: ...-11ee2ca4 at the same hash
- session source: pristine s5_common_pre_v1 copied to a fresh R0-v2 session directory
- continuation path: ...-0421b2d6
- late user turn: exact historical T7
- fixed runtime: GPT-5.6 Sol / xhigh / same tools / no skills/rules/extensions
