# S1 Stage-B Controlled Replay Result V1

date: 2026-09-28
status: VALID_S1_PILOT__R3_MATCHES_R2__RAW_HISTORY_DOMINATES_LOCALLY
parent:
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
- S1_STAGE_B_BOUNDARY_FREEZE_V1.md
- S1_R3_ORACLE_SCOPE_REPAIR_V2.md
task: dataclaw-anonymizer-tests
formal_stage_b_verdict: NOT_YET_ADJUDICATED
paper_candidate: false

## 1. Valid execution identities

Frozen task initial state:
- windows = 3c9474ef6aa1eb75deff170a05f33e9257aeb8fd

Frozen pre-U5 snapshot:
- tests/test_anonymizer.py only
- +32 / -0 lines
- worktree patch sha256 = 98f76b316ccd052c124f2eea2a59d6cf5c7032c590cf9e6286dd84954ffbab3f

Valid arms:
- R0 RAW_HISTORY: turn_e5044b6bb9244fee9c93101cc163773f
- R1 CONSOLIDATED_REFRESH: turn_276840e336a245e48903b5c672a35483
- R2 FULL_RESTART: turn_7574e2d220514f8a95e01461d3d21d30
- R3 ORACLE_DEPENDENCY_SCOPED_REDERIVATION: turn_7b43e3051aea4c97a1b538f798cf972a

All valid post-revision runs:
- GPT-5.6 Sol
- xhigh
- OMP process under lifetime
- isolated worktree
- Python 3.12 task runtime
- no extra skills/rules/extensions

## 2. Invalid runs excluded

Do not reuse or count:
- s1-pilot-r1-v1 / turn_04152059aece4114b031772c4796fb64 — cancelled.
- s1-pilot-r1-seq-v1 / turn_8c354e7e46534bfb979d2edbf9912f80 — INVALID: executed on R0 worktree after R0 rather than an independent pre-U5 branch.
- earlier R0/R1 clean-v2 attempts — INVALID for science: copied OMP history retained absolute old worktree cwd; edits landed outside the intended isolated worktree.
- R3 V1 / turn_059c38547c78439d8c9fa2b233f35f59 — REPAIR_NEGATIVE: outcome-blind scope omitted an existing pre-revision compatibility seam (_replace_username). It is not a scientific claim negative.

Infrastructure repairs:
- rebase_omp_session_workspace.py rewrites historical absolute workspace references when a native OMP session is cloned to another isolated worktree.
- R3 V2 preserves pre-revision symbol/signature compatibility while still invalidating the old helper implementation.

## 3. Frozen correctness endpoint

Published S1 verifier logic was reused through run_s1_local_verifier.sh.
The adapter changes only:
- container-local repo/log paths;
- Python executable -> frozen local Python 3.12 venv.

Adapter validation:
- original windows baseline reproduced reward 0.3500 exactly.

Final rewards:
| Arm | Reward | P2P |
|---|---:|---|
| R0 RAW_HISTORY | 1.0000 | PASS |
| R1 CONSOLIDATED_REFRESH | 0.8000 | PASS |
| R2 FULL_RESTART | 1.0000 | PASS |
| R3 ORACLE_SCOPED | 1.0000 | PASS |

R1 misses:
- underscore-prefix behavior;
- stateful extra-username underscore behavior.

## 4. Work / reuse accounting

Raw accounting:
- external/spec_stageb_accounting/s1/R0.json
- external/spec_stageb_accounting/s1/R1.json
- external/spec_stageb_accounting/s1/R2.json
- external/spec_stageb_accounting/s1/R3.json

| Arm | Model calls | Tool calls | Noncached input+output | Reported cost | Wall | Pre-U5 +32-line reuse |
|---|---:|---:|---:|---:|---:|---:|
| R0 | 10 | 11 | 55,639 | $0.5475 | 195.5 s | 100% |
| R1 | 7 | 7 | 56,718 | $0.5365 | 216.5 s | 100% |
| R2 | 12 | 27 | 69,192 | $0.6642 | 392.0 s | 0% credited |
| R3 | 14 | 24 | 52,712 | $0.5694 | 244.5 s | 100% |

R3 vs R2:
- correctness: equal, 1.0 vs 1.0;
- pre-revision preserved artifact segments: 3/3, 32/32 lines;
- tool calls: 24 vs 27 = 11.1% fewer;
- noncached input+output tokens: 23.8% fewer;
- reported cost: 14.3% lower;
- wall time: 37.6% lower.

Therefore S1 demonstrates a nontrivial R3-vs-R2 reuse/cost region.

## 5. Strongest cheap-rival audit

R0 RAW_HISTORY also achieves:
- verifier reward 1.0;
- 100% pre-U5 test-asset preservation;
- 11 tool calls;
- $0.5475 reported cost.

On S1, R0 is cheaper than R3 while matching correctness and preservation.

Therefore:
S1 does NOT establish that selective rederivation is necessary or valuable relative to simply continuing raw history.

This is a real counterexample to a broad method-value claim, but not a kill of the frozen transfer premise because the premise only requires a nontrivial regime across evolving-requirement tasks.

## 6. S1 verdict

S1_CONTROLLED_REPLAY_SEMANTICS = PASS.

S1_R3_VS_R2_HEADROOM = LOCAL_PASS.

S1_R3_VS_RAW_HISTORY_VALUE = FAIL_ON_THIS_TASK.

FULL_STAGE_B = UNRESOLVED.

No PAPER_CANDIDATE activation.

## 7. Execution-leverage consequence

Do not immediately pay for full four-arm S2-S5.

Remaining Stage-B should be sequenced:
1. use frozen public traces/metadata to order remaining tasks by expected falsification leverage;
2. generate one shared pre-revision snapshot per task;
3. run R2 + R3 first because these decide the necessary headroom conditions;
4. stop if the frozen correctness/reuse predicates become mathematically impossible;
5. only if R3 headroom survives, run R0/R1 for strongest-rival and refresh comparisons.

This changes execution order only, not task set, prompts, thresholds, or scientific predicates.
