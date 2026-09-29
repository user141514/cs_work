# RESEARCH-01 Contract — S3 Development Replay

Date: 2026-09-29
Status: AUTHORIZED_DEVELOPMENT_ONLY
Task: pi-mono-auto-93c17d3b
Purpose: first real bounded replay of the frozen workflow on one complex historical task.

## Claim owned by this replay

Question: can the new workflow process a real late requirement revision without discarding valid earlier work, while preserving task correctness and explicitly protecting lifecycle/UI invariants?

This replay is DEVELOPMENT_ONLY because the parent conversation has already seen historical task metadata and some outcomes. It may reveal workflow defects and produce a reusable baseline, but it is not held-out evidence and cannot support a publication-effectiveness claim by itself.

## Frozen task state

Repository: badlogic/pi-mono
Base commit: 5133697bc454da5595655cf4b0c70d3c2c725677
Execution checkout: isolated temporary checkout at this exact commit.
No initial dirty patch is admitted.

Frozen source assets:
- PRE_REVISION_REQUIREMENTS.md
  - SHA256: f1010e3e37e5ae5f042d5bd442840275cf00de0837dd496712edaea5f2211c30
  - user messages only, all indices <54
- LATE_REVISION.md
  - SHA256: f7635fb88bb2ce578ace71acbbe36d352a7888abf4e20b16ea9313d83a970ca7
  - user message index 54 only
- SOURCE_FREEZE.json
  - records the original_session source SHA256 and exclusion boundary.

Forbidden to the executing arm:
- assistant messages from original_session.json;
- oracle_intents.json;
- oracle_session.jsonl;
- reference_patch.json;
- fix_summary.md;
- verifier outcomes;
- S3 future results or any historical successful implementation.

## Execution policy

Model/runtime target for the fresh coding arm:
- provider: Codex
- model: GPT-5.6 Sol
- effort: xhigh
- one fresh session, then one continuation for the late revision;
- same checkout and same model session across pre-revision and late-revision phases;
- no use of historical outcome files.

Workflow hard constraints:
1. At the beginning of each phase, write the current goal and one bounded plan before changing code.
2. Decompose by independently checkable responsibility, not by arbitrary file count.
3. Declare the behavioral invariants that must survive the current change.
4. Reuse existing repository mechanisms before creating new infrastructure.
5. After each phase, inspect the actual diff/tests and write exactly one next action; do not pre-execute the next phase.
6. The late revision must preserve pre-revision functionality unless the user explicitly superseded it.
7. Do not read files outside the task repository except the explicitly named frozen requirement file for the current phase.

## Phase boundary

### Phase A — PRE_REVISION

Visible requirements:
PRE_REVISION_REQUIREMENTS.md only.

Goal:
produce the best implementation satisfying all user requirements available through source_message_index=51.

Stop after:
- implementation and local tests/checks;
- a concise record of implemented responsibilities, invariants, changed files and unresolved uncertainty;
- no knowledge of source_message_index=54.

### Phase B — LATE_REVISION

Only after Phase A is frozen, provide LATE_REVISION.md.

Goal:
address the streaming/UI-freeze complaint without unnecessarily discarding valid Phase-A behavior.

The late revision is the intervention under observation.

## Method-neutral endpoint evaluation

Parent-side only; not provided to the executing arm before completion.

A. Public task behavior:
- extension file exists and is loadable;
- registers an activation command and message handler;
- activation injects a signal protocol;
- reacts to open/close signal outputs;
- remains inert before activation;
- no normal tool registration is used for the signal carrier.

B. Requirement-derived lifecycle check:
- opening UI is caused by an explicit open signal;
- neutral streaming text deltas do not repeatedly recreate/open/close the UI;
- open state can persist across turns;
- a later explicit close signal closes it;
- late-revision change must not remove activation/protocol/inactive behavior.

The evaluator may adapt the published verifier to the local checkout path, but may not use the reference patch as an oracle.

## Evidence to record

- final git diff against frozen base;
- Phase-A snapshot/diff hash before revealing the late revision;
- Phase-B final diff hash;
- commands/tests actually run by the executing arm;
- independent parent-side endpoint checks;
- model/session identity when available;
- wall time / model usage when exposed;
- rework: Phase-A lines/hunks removed or changed during Phase B;
- failures and invalid runs remain in the denominator.

## Decision rule

REPLAY_VALID only if:
- Phase B did not see the late requirement before the Phase-A freeze;
- no forbidden historical outcome entered the arm;
- checkout identity stayed at the frozen task lineage;
- endpoint evaluation is independent from the arm;
- implementation/runtime failure is not mislabeled as workflow/scientific failure.

A positive developmental result only means this workflow survived one known historical task. It does not establish superiority over the old workflow.
