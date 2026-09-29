# S3 Mechanism Exposure Gate — Before Paid Stage-B Arms

date: 2026-09-30
status: FROZEN_BEFORE_ANY_NEW_S3_PAID_ARM
task: pi-mono-auto-93c17d3b
selector_gate: MECHANISM_EXPOSURE_GATE
primary_source_scope:
- research_factory/computer_topconf_2027/SPEC_STAGE_A_TASK_FREEZE_V1.md
- research_factory/replays/RESEARCH_01_S3/PRE_REVISION_REQUIREMENTS.md
- research_factory/replays/RESEARCH_01_S3/LATE_REVISION.md

developmental_replay_scope:
- RESEARCH_01_S3 Phase-A/Phase-B artifacts are NOT used to determine the exposure verdict.
- They remain developmental workflow evidence only.

## Question

Before paying for S3 R2/R3, is the BFSC load-bearing relation actually exposed?

For S3, exposure means:

> an authoritative late requirement invalidates at least one concrete pre-existing behavior/derived responsibility while leaving at least one other pre-revision responsibility valid/reusable.

This is the minimum relation selective rederivation needs. If the late revision simply replaces the whole task, or touches no existing derived behavior, BFSC selective-rederivation value is not exposed.

## Frozen predicate

S3 passes `EXPOSURE_SOURCE_PROVEN` only if all are true from the named primary frozen artifacts:

E1. Before the late revision, the source trace already demonstrates an existing signal-driven UI behavior across turns rather than only a proposed feature.

E2. The late revision explicitly reports an endpoint defect involving that existing UI during output/streaming: the UI freezes and the user basically cannot type.

E3. The Stage-A frozen task identity says the subsequent correction changes lifecycle/UI behavior **after the extension path already exists**, while the verifier contract still covers command/handler behavior, protocol injection, distinct signals and loadable-extension behavior.

E4. Therefore the revision induces a mixed-validity relation:
- some existing UI/lifecycle behavior must be changed/revalidated;
- some pre-revision extension behavior remains part of the task contract and is potentially reusable.

E5. The exposure judgment uses no assistant trajectory, reference patch, Phase-B implementation/result, oracle, or post-revision successful solution.

## Verdicts

- `EXPOSURE_SOURCE_PROVEN`: E1-E5 all pass.
- `NO_EXPOSURE`: late revision does not invalidate any existing derived responsibility or wholly replaces the task so no selective-reuse relation remains.
- `EXPOSURE_NONIDENTIFIABLE`: named frozen artifacts cannot determine whether any existing responsibility is touched.

## Scope

A positive exposure verdict does NOT authorize a paper candidate and does NOT prove selective rederivation beats RAW_HISTORY.

It only permits the next already-frozen sequence:

S3 offline boundary freeze
->
S3 execution-leverage gate
->
decide whether paid S3 R2/R3 evidence is worth acquiring.

The exact next step after this gate is the offline boundary freeze. No paid arm is authorized by this file alone.
