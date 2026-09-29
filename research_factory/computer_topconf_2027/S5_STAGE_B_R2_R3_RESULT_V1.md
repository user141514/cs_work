# S5 Stage-B R2/R3 Result V1

date: 2026-09-28
status: VALID_S5_R2_R3__HEADROOM_LOCAL_PASS__AUTHORIZE_R0_R1
task: pi-mono-auto-ec7037ba
parent:
- S5_STAGE_B_BOUNDARY_FREEZE_V1.md
- S5_R3_ORACLE_SCOPE_FREEZE_V1.md
- S5_EXECUTION_LEVERAGE_GATE_V1.md
- S5_COMMON_PRE_REVISION_SNAPSHOT_V1.md
- S5_SCIENTIFIC_RUNTIME_IDENTITY_V1.md
formal_stage_b_verdict: NOT_YET_ADJUDICATED
paper_candidate: false

## 1. Valid scientific arm identities

Frozen agent/runtime:
- GPT-5.6 Sol
- xhigh
- OMP process under lifetime
- read/bash/edit/write/grep/glob
- no extra skills/rules/extensions
- isolated worktree per arm

R2 FULL_RESTART:
- request_key: s5-r2-full-restart-v1
- turn_id: turn_a2a103a1b8444067b69d80017f00b99b
- outcome: succeeded
- terminal: true
- quiescent: true
- worktree: C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-476da099

R3 ORACLE_SCOPED:
- request_key: s5-r3-oracle-scoped-v1
- turn_id: turn_c29e5e8ad26c4b47b0609b4ec3bebdbf
- outcome: succeeded
- terminal: true
- quiescent: true
- worktree: C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-439211c0

No R0/R1 S5 scientific outcome has been observed yet.

## 2. Local-equivalent verifier adapter validation

Authority:
- run_s5_local_verifier.sh
- public SWE-Together test.sh
- s5_autocomplete_evaluator_probe.mjs
- s5_verifier_postprocess.py

Two adapter-only defects were found before scientific scoring:
1. a v043 diagnostic prelude embedded /workspace/pi-mono inside base64 and escaped literal path substitution;
2. relative logdir paths became invalid after the public verifier changed cwd into the target repository.

Both were repaired only in the local path adapter.
No F2P/P2P gate, score weight, or scientific predicate changed.

Frozen base validation after repair:
- task initial repo: 69d02b8a5fce07041f77aba64c6ebbc8589827ab
- local-equivalent reward: 0.0000
- all four F2P gates: FAIL
- all four upstream P2P diagnostics: PASS

Therefore the repaired adapter preserves the intended initial failure state.

## 3. Correctness result

R2 reward:
1.0000

R3 reward:
1.0000

Both:
- changelog growth: PASS
- changelog attribution format: PASS
- directory completion no trailing space: PASS
- directory marker/continuation behavior: PASS
- upstream P2P diagnostics: PASS

Direct behavior in both arms:
- directory: @src/
- directory cursor column: 5
- terminal file: @README.md<space>
- terminal-file cursor column: 11

Therefore:
S5_R3_VS_R2_CORRECTNESS = EQUAL_PASS.

## 4. Post-revision work accounting

Accounting source:
- account_stageb_omp_session.py
- native OMP session JSONL

R2:
- model calls: 26
- tool calls: 102
- mutating tool calls: 2
- noncached input+output tokens: 326,305
- reported model cost: $2.7281256
- wall from numeric timestamps: 480.190 s

R3:
- model calls: 33
- tool calls: 74
- mutating tool calls: 2
- noncached input+output tokens: 183,767
- reported model cost: $2.4217048
- wall from numeric timestamps: 482.319 s

R3 relative to R2:
- correctness: equal
- tool calls: -27.45%
- noncached input+output: -43.68%
- reported cost: -11.23%
- wall: +0.44%

Interpretation:
R3 makes more model calls but with substantially smaller/reduced work per call.
The result is consistent with selective reuse reducing repository/context recomputation rather than merely reducing turn count.

## 5. Pre-revision reuse accounting

Frozen pre-U7 evidence source:
external/spec_stageb_sessions/s5_common_pre_v1/2026-09-28T13-04-59-466Z_01a0e81e-5e4a-7000-b1d3-5d1250dfbd7e/55.bash-original.log

This source records the exact U4 changelog diff:
- packages/ai/CHANGELOG.md: +1 / -0
- packages/coding-agent/CHANGELOG.md: +14 / -4
- packages/tui/CHANGELOG.md: +8 / -2
- aggregate: +23 / -6

The current common worktree is NOT used as the reuse denominator because it was later contaminated by two U7 completion-related changelog lines after the freeze.

Primary conservative metric:
byte-identical nonblank pre-U7 added lines retained inside the same file's final [Unreleased] section.

R3:
- meaningful pre-U7 added lines: 19
- byte-identical retained lines: 7
- credited reuse fraction: 7/19 = 36.84%

R2:
- reuse credit: 0 by definition of FULL_RESTART
- independently re-created matching text receives no reuse credit.

Auxiliary exact-contiguous-segment metric:
- R3: 0/5 complete added segments survive byte-identically.

Why the primary metric is used:
one rewritten line inside a contiguous changelog hunk should not erase credit for adjacent independently preserved attribution/provenance lines.
The line metric remains conservative because:
- blank lines are excluded;
- matching is restricted to the same file's final [Unreleased] section;
- deletions are not credited;
- semantic paraphrases are not credited.

Therefore:
S5_R3_PRE_REVISION_REUSE = 36.84% >= frozen 30% threshold.

## 6. S5 local headroom decision

Frozen necessary conditions relevant at this step:
- R3 approaches R2 correctness;
- R3 preserves >=30% meaningful pre-revision work.

Observed:
- R3 correctness = R2 correctness = 1.0000
- R3 credited reuse = 36.84%
- R3 reported cost is 11.23% lower than R2

Therefore:
S5_R3_VS_R2_HEADROOM = LOCAL_PASS.

This does NOT satisfy prospective value gate V by itself because V compares against the strongest correct cheap rival R0/R1.

## 7. Execution Leverage decision

Previous S5 gate authorized:
common prestate -> R2 -> R3 -> only then decide whether to pay for R0/R1.

That prerequisite now passes.

Therefore:
AUTHORIZE_S5_R0_R1 = YES.

Purpose:
determine whether S5 provides a V-positive pressure witness:
- correctness rescue over raw/refresh state; or
- >=10% reported-cost frontier against the strongest correct cheap rival.

Do not start S3/S2/S4 until S5 R0/R1 resolves this value question.

## 8. Infrastructure finding

A frozen experimental worktree is not itself an immutable snapshot.

Observed failure:
the worktree referenced by S5_COMMON_PRE_REVISION_SNAPSHOT_V1.md later acquired two U7 completion-related changelog lines.

Recovery was possible only because the exact U4 diff survived in the original OMP tool log and the freeze document recorded its identity/statistics.

New invariant:
PRE_REVISION_FREEZE must materialize an immutable patch artifact at freeze time, plus its content hash.
A worktree path is only a mutable execution location and must never be the sole recovery authority.

For future S2-S4:
- save exact binary/text patch artifact immediately at freeze;
- record SHA-256 or git hash-object;
- record HEAD;
- use that artifact, not the live worktree, for reuse accounting and branch reconstruction.

## 9. First unresolved transition

S5 R0 RAW_HISTORY + R1 CONSOLIDATED_REFRESH
->
same frozen verifier
->
same accounting
->
prospective value gate V.

No new mechanism family, topic scan, dependency-model training, molecular experiment, or S3/S2/S4 paid run is authorized before this transition.
