# S2 Mechanism Exposure Result V1

date: 2026-10-01
status: EXPOSURE_SOURCE_PROVEN__BOUNDARY_FREEZE_NEXT
task: pi-mono-auto-a4fca584

## Decision

`S2_MECHANISM_EXPOSURE_GATE = EXPOSURE_SOURCE_PROVEN`

The BFSC load-bearing relation is directly visible from frozen user-only source evidence.

## Evidence chain

### E1 — implementation state exists before the semantic correction

The initial contract explicitly says:
`Do NOT implement unless explicitly asked. Analyze and propose only.`

Later the user says:
`oki, implement concisely`

Therefore implementation is authorized before the path-semantics revision.

### E2 — the path-persistence decision is already active, not hypothetical

Before the authoritative late revision, the user asks:

`try it with pi-test.sh. i'm especially curious what happens with relative paths. are they resolved to absolute paths in settings.json?`

This is a runtime/behavior probe of an already implemented settings-path decision, not a proposal for future work.

### E3 — the late revision explicitly invalidates the current path base

The user then states:

`so, i guess when we write to settings.json, we need to make these paths relative to the settings.json, no? or how can they be resolved otherwise if we just have the cwd relative path in settings.json, both user and project?`

followed by the authoritative correction:

`i want the path to be resolved relative to the settings.json we write it to, anything else makes no sense.`

The changed semantic relation is therefore explicit:

`cwd-relative persisted path`
->
`path relative to the settings.json receiving the entry`.

### E4 — mixed-validity, not whole-task replacement

The revision does not revoke:
- local-package support;
- writing package paths into settings;
- add/remove behavior;
- user/project settings scopes;
- the prior implementation authorization.

It changes the path-origin / persistence-resolution semantics and any dependent logic.

Thus some pre-revision implementation/decision state becomes stale while surrounding feature responsibilities remain potentially reusable.

### E5 — outcome blind

The exposure verdict used:
- frozen Stage-A S2 identity;
- only selected user messages from the official original session.

It did NOT use:
- assistant trajectory content;
- oracle session/intents;
- canonical goals;
- reference patch;
- verifier result;
- post-revision successful solution.

## Mechanism statement

The exposed BFSC relation is:

> an implementation has already committed to a path persistence/resolution basis; a later authoritative requirement changes that basis from cwd-relative semantics to settings-file-relative semantics while preserving the broader package/settings feature.

This is a genuine stale-derived-state exposure for selective invalidation/rederivation.

## Scope

Supported:
- S2 is a valid mixed-validity revision regime for the BFSC question.
- S2 is eligible for offline boundary freezing.

Not supported:
- RAW_HISTORY fails on S2;
- R3 beats R2/R0/R1;
- H or V passes;
- paid S2 execution;
- PAPER_CANDIDATE activation.

## NEXT_STEP

`S2_STAGE_B_BOUNDARY_FREEZE_V1` only.

Freeze:
- exact TASK_INITIAL_STATE;
- authoritative pre-revision user requirement sequence;
- exact late revision boundary;
- consolidated pre/final specification;
- immutable common-prestate contract;
- outcome-blind R3 dependency rule.

Apply the prospective PARTIAL_REFERENCE_GUARD from
`BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md`.

Do not run any S2 paid model arm in the boundary-freeze step.
