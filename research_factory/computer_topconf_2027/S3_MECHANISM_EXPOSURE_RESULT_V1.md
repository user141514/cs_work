# S3 Mechanism Exposure Result V1

date: 2026-09-30
status: EXPOSURE_SOURCE_PROVEN
task: pi-mono-auto-93c17d3b

## Decision

The new live-selector `MECHANISM_EXPOSURE_GATE` passes for S3 using only frozen, source-visible evidence.

Pre-revision source trace already shows an existing multi-turn signal UI:
- UI opens and waits for the close signal;
- UI later closes;
- user explicitly asks for first-turn open / last-turn close across a multi-turn task.

The late authoritative revision then reports:
- output is arriving;
- the UI freezes;
- the user basically cannot type;
- the user questions the message/update-path lifecycle and UI recreation behavior.

The Stage-A task freeze independently records the same structure:
- extension path already exists;
- open/close behavior exists across turns;
- subsequent correction changes lifecycle/UI behavior;
- command/handler behavior, protocol injection, distinct signals and loadable-extension behavior remain part of the task contract.

Therefore the load-bearing BFSC relation is actually exposed:

> at least one pre-existing derived behavior is invalidated/requires revalidation by the late revision, while other pre-revision responsibilities remain valid and potentially reusable.

## Evidence boundary

Primary evidence:
- `SPEC_STAGE_A_TASK_FREEZE_V1.md`;
- verbatim `PRE_REVISION_REQUIREMENTS.md`;
- verbatim `LATE_REVISION.md`.

Not used to determine this verdict:
- RESEARCH-01 Phase-B implementation;
- RESEARCH-01 Phase-B endpoint result;
- reference patch;
- oracle;
- post-revision successful solution.

The development replay remains developmental evidence only.

## Scope

Supported:
- S3 is a valid mixed-validity revision regime for the BFSC/selective-rederivation question.

Not supported:
- RAW_HISTORY fails on S3;
- R3 beats R0/R1;
- the BFSC value gate V is positive;
- PAPER_CANDIDATE activation.

## Exact next step — not executed

S3 **offline boundary freeze** only:
- freeze authoritative pre-revision requirement sequence and late revision;
- freeze task-initial state identity;
- define the pre-revision derived-work boundary and immutable artifact requirements;
- freeze what counts as affected vs potentially reusable without post-revision outcomes.

Only after that freeze may the already-planned S3 execution-leverage gate decide whether paid R2/R3 evidence is justified.

No paid S3 arm is authorized yet.
