# S4 Mechanism Exposure Result V1

date: 2026-10-02
status: EXPOSURE_NONIDENTIFIABLE__SELECTOR_REPLAN_NEXT
task: pi-mono-auto-d3b2130d
model_calls: 0
formal_paper_candidate: false

## Decision

`S4_MECHANISM_EXPOSURE_GATE_V1 = EXPOSURE_NONIDENTIFIABLE`

The frozen S4 verifier is compatible, but the BFSC load-bearing stale-state/selective-invalidation relation is not source-identifiable under the frozen exposure evidence policy.

## Source facts

The user-only trace shows:

1. npm-registry keyword discovery;
2. question about keyword-only search;
3. selection of the unique keyword `pi-package`;
4. a correction:
   `no, add it to ../pi-doom/ ../pi-package-test/ and ../pi-gitlab-duo/`;
5. publish new versions;
6. document the keyword;
7. search again;
8. commit/push workflow request.

The only explicit correction is message index 10.

## Why exposure cannot be proven

Before message index 10, user-only evidence proves a **keyword requirement**, but not a concrete already-created implementation/target state.

Message index 10 begins with `no`, which strongly suggests some earlier assistant decision is being corrected.

However, the user message does not identify:
- what target the assistant had chosen;
- whether any package metadata had already been edited;
- which concrete derived artifact/responsibility is now invalid.

Answering those questions requires assistant trajectory evidence, which the frozen MECHANISM_EXPOSURE_GATE explicitly forbids.

Therefore the gate cannot establish:
- a concrete stale derived state;
- a precise invalidated prior unit;
- a source-proven mixed-validity derived-work relation.

## Why this is not NO_EXPOSURE

The correction marker `no` means it would be too strong to claim that no stale/corrected derived state existed historically.

The allowed evidence simply cannot determine it.

Hence:

`EXPOSURE_NONIDENTIFIABLE`

rather than:
- `EXPOSURE_SOURCE_PROVEN`;
- `NO_EXPOSURE`.

## Frozen base evidence

Base:
`353ac792ebb99931c640ee55af90881d3a45c4d9`

The frozen base:
- contains no source-proven task-derived `pi-package` keyword metadata state;
- does not contain the three sibling targets named by the correction.

This supports the conclusion that the missing pre-existing derived state cannot be recovered from frozen base evidence alone.

## Authorization consequence

S4 paid execution remains **not authorized**.

Do not run:
- S4 common-prestate;
- S4 R2/R3/R0/R1;
- S2 R3/R0/R1.

Do not read assistant history after this result to rescue exposure.

## Portfolio consequence

Current frozen portfolio becomes:

- S5: V-negative;
- S3: V-ineligible / partial-adjudication gap;
- S2: valid R2 execution, primary correctness measurement structurally invalid;
- S4: verifier-compatible, but mechanism exposure nonidentifiable.

This does not prove BFSC false.

It means the final unobserved V-witness slot cannot be prospectively admitted to paid Stage-B execution under the frozen mechanism-exposure policy.

## NEXT_STEP

`BFSC_SELECTOR_REPLAN_AFTER_S4_EXPOSURE_NONIDENTIFIABLE` only.

The selector must decide the PRECARD identifiability status of BFSC under the exhausted frozen Stage-B portfolio.

Do not create a method negative merely because the remaining witness is nonidentifiable.
