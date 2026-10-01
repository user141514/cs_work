# S4 Mechanism Exposure Gate V1

date: 2026-10-02
status: FROZEN_ZERO_MODEL_EXPOSURE_ADJUDICATION
task: pi-mono-auto-d3b2130d
selector_gate: MECHANISM_EXPOSURE_GATE
parent:
- BFSC_SELECTOR_REPLAN_AFTER_S2_VERIFIER_INVALID_20261002.md
- S4_VERIFIER_COMPATIBILITY_GATE_V1.md
- SPEC_STAGE_A_TASK_FREEZE_V1.md
primary_source_scope:
- S4_MECHANISM_EXPOSURE_SOURCE_V1.json
- frozen S4 base source at 353ac792ebb99931c640ee55af90881d3a45c4d9
model_calls: 0

## Question

Before paying for S4 Stage-B execution, is the BFSC load-bearing relation actually source-proven?

For S4, exposure would require:

> a later authoritative requirement to invalidate or selectively revise a concrete pre-existing derived responsibility while leaving other pre-revision work valid and reusable.

Static requirement growth alone is not enough.

## Candidate revision boundary

The user-only trace evolves as:

1. npm-registry keyword discovery;
2. clarification about keyword-only search;
3. choose a unique keyword: `pi-package`;
4. correction: `no, add it to ../pi-doom/ ../pi-package-test/ and ../pi-gitlab-duo/`;
5. publish new versions;
6. document the keyword;
7. search again;
8. commit/push workflow request.

The only source-visible turn with correction semantics is message index 10.

Later publish/docs/search requirements are additive extensions of the task.

## Frozen predicate

S4 can pass `EXPOSURE_SOURCE_PROVEN` only if all are established from allowed evidence:

E1. Before message index 10, the source proves a concrete derived implementation/decision responsibility already exists rather than only a proposed keyword choice.

E2. Message index 10 identifies which concrete earlier responsibility is now invalid and what remains valid.

E3. The correction induces mixed validity:
- at least one prior derived unit must be changed/revalidated;
- at least one other prior derived unit remains reusable.

E4. This relation can be established without reading the assistant trajectory or future solution-bearing artifacts.

E5. Frozen base evidence does not contradict the claimed pre-existing derived state.

## Evidence

### E1 — NOT PROVEN

Before message index 10, user-only evidence establishes:
- discovery/search discussion;
- selection of the unique keyword name `pi-package`.

It does **not** establish:
- that the keyword has already been written to any concrete package;
- which repository/package targets were selected;
- that a package-metadata implementation state exists.

The phrase `we should ensure` is a requirement, but not proof that a derived artifact already exists before the later correction.

### E2 — NONIDENTIFIABLE FROM ALLOWED SOURCE

Message index 10 begins with:

> no, add it to ../pi-doom/ ../pi-package-test/ and ../pi-gitlab-duo/

The word `no` shows that the user is correcting something in the ongoing interaction.

However, the user-only trace does not state what prior concrete target/implementation is being rejected.

Determining the rejected state would require the assistant trajectory, which is explicitly forbidden for mechanism exposure adjudication.

Therefore the exact invalidated pre-existing derived responsibility is not source-identifiable.

### E3 — NOT SOURCE-PROVEN

The keyword choice `pi-package` clearly remains valid after message index 10.

But the gate requires a **derived-work** mixed-validity relation, not merely a requirement-token relation.

Because the source does not prove a concrete pre-message-10 implementation/target state, it cannot prove selective invalidation of already-created work.

Later requirements:
- publish;
- documentation;
- search;

are additive and do not themselves expose stale-state survival.

### E4 — PASS

This adjudication uses:
- ordered user messages only;
- frozen base static evidence.

No assistant trajectory, oracle, reference patch, canonical goals, post-result execution, or future successful solution is used.

### E5 — SUPPORTS NONIDENTIFIABILITY

Frozen base at `353ac792...` does not contain source-proven task-derived `pi-package` metadata state.

The three sibling directories named in message index 10 are absent from the frozen workspace:
- `../pi-doom/`
- `../pi-package-test/`
- `../pi-gitlab-duo/`

This does not prove that no transient implementation could have been created during the historical conversation.

It does show that the frozen base itself cannot supply the missing pre-existing derived state.

## Verdict

`S4_MECHANISM_EXPOSURE = EXPOSURE_NONIDENTIFIABLE`

Why not `EXPOSURE_SOURCE_PROVEN`:
- the allowed source cannot identify a concrete already-created implementation/target state invalidated by the correction.

Why not `NO_EXPOSURE`:
- the user says `no`, so the interaction plausibly contains a corrected prior decision;
- ruling out such a derived state would require inspecting the assistant trajectory, which is forbidden.

The scientifically correct result is therefore nonidentifiability, not a positive and not a negative.

## Kill-scope certificate

This result does **not** show:
- BFSC/selective rederivation is false;
- S4 final task is unsolvable;
- S4 verifier is invalid;
- S4 has no requirement evolution;
- S4 has no additive reusable work.

It shows only:

> under the frozen source policy, S4 cannot provide source-proven evidence that a late requirement acts on already-created derived state strongly enough to expose the BFSC stale-state/selective-invalidation mechanism.

## Authorization consequence

Paid S4 execution is **not authorized**.

Do not run:
- S4 common-prestate;
- S4 R2/R3/R0/R1;
- S2 R3/R0/R1.

Do not relax the source policy by reading historical assistant content to rescue exposure after this outcome.

## NEXT_STEP

`BFSC_SELECTOR_REPLAN_AFTER_S4_EXPOSURE_NONIDENTIFIABLE` only.

The selector must absorb the frozen portfolio:
- S5: V-negative;
- S3: V-ineligible / partial-adjudication gap;
- S2: valid R2 execution but primary correctness measurement structurally invalid;
- S4: verifier-compatible but mechanism exposure nonidentifiable under allowed source evidence.

Do not create a BFSC method negative from this gate alone.
