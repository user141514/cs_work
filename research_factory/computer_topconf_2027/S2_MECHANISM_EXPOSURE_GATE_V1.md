# S2 Mechanism Exposure Gate V1

date: 2026-10-01
status: FROZEN_BEFORE_ANY_S2_PAID_ARM
task: pi-mono-auto-a4fca584
selector_gate: MECHANISM_EXPOSURE_GATE
parent:
- BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md
- SPEC_STAGE_A_TASK_FREEZE_V1.md
primary_source_scope:
- S2_MECHANISM_EXPOSURE_SOURCE_V1.json
- SPEC_STAGE_A_TASK_FREEZE_V1.md

## Question

Before paying for S2 Stage-B model arms, is the BFSC load-bearing relation actually exposed?

For S2, exposure means:

> after implementation has been authorized and path-persistence behavior is already active, a later authoritative requirement changes the semantic base used to persist/resolve those paths while leaving the surrounding local-package/settings feature valid.

This is the mixed-validity relation selective rederivation requires.

## Frozen predicate

S2 passes `EXPOSURE_SOURCE_PROVEN` only if all are true from user-only source evidence plus the frozen Stage-A identity:

E1. The trace changes from analysis-only to explicit implementation authorization before the late path-semantics revision.

E2. Before the late revision, the user is already probing concrete path-persistence behavior in `settings.json`, so the path decision is not merely hypothetical future work.

E3. The late revision explicitly identifies the currently problematic semantic state as a cwd-relative path persisted into settings and changes the authoritative rule to paths relative to the specific `settings.json` file being written.

E4. The late revision is mixed-validity rather than whole-task replacement:
- the local-package/settings feature remains required;
- implementation authorization remains valid;
- only the path base / normalization-resolution decision and dependent behavior must be changed or revalidated.

E5. The exposure verdict uses no assistant trajectory, oracle session/intents, reference/gold patch, canonical goals, verifier result or future successful implementation.

## Verdicts

- `EXPOSURE_SOURCE_PROVEN`: E1-E5 pass.
- `NO_EXPOSURE`: no concrete pre-existing derived responsibility is touched, or the late revision replaces the whole task.
- `EXPOSURE_NONIDENTIFIABLE`: frozen allowed sources cannot establish whether the late revision acts on prior derived state.

## Kill-scope certificate

A negative at this gate would establish only that S2 lacks a source-proven stale-derived-state exposure for BFSC.

It would NOT:
- kill BFSC across S4 or the full frozen Stage-B set;
- kill specification-state research generally;
- change any H/V threshold;
- turn S2 into a benchmark/methodology contribution.

A positive establishes only task/regime eligibility for the next offline boundary freeze.

## Scope

A positive result does not authorize:
- S2 R2/R3;
- S2 R0/R1;
- PAPER_CANDIDATE/TOPIC_BET promotion;
- changes to the PARTIAL_REFERENCE_GUARD.

Exact next step after a positive:
`S2_STAGE_B_BOUNDARY_FREEZE_V1` only.
