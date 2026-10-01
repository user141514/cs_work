# BFSC Selector Replan After S2 Verifier Invalidity — 2026-10-02

date: 2026-10-02
status: CONTINUE_PRECARD__S4_VERIFIER_COMPATIBILITY_NEXT
scope: BFSC/selective-rederivation remaining frozen S4 horizon
formal_paper_candidate: false

does_not_modify:
- SPEC_TRANSFER_G0_FALSIFIER_V1.md Stage-B PASS_HEADROOM
- BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md value gate V
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md arm identities
- BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md PARTIAL_REFERENCE_GUARD
- S1/S2/S3/S5 historical outcomes
- frozen task set or mechanism-family identities

## 1. Portfolio audit

Current prospective value evidence:

### S5
- R2/R3 local headroom survived;
- cheap RAW_HISTORY matched correctness at much lower cost;
- V = NEGATIVE.

### S3
- R2/R3 both valid but partial;
- reuse/cost improved under R3;
- pre-registered local `matches/approaches` rule did not cover partial-vs-partial;
- local verdict remains `INCONCLUSIVE_PRE_REGISTERED_RULE_GAP`;
- R2 did not reach frozen verifier success, so S3 cannot satisfy frozen V-A/V-B.

### S2
- mechanism exposure: PASS;
- common prestate: valid and immutably frozen;
- R2 FULL_RESTART execution: valid;
- R2 independently implemented the final settings-file-relative semantics with positive secondary tests/smoke;
- frozen primary verifier: structurally invalid for the frozen base before local-install behavior is evaluated;
- scientific R2 correctness endpoint:
  `NONIDENTIFIABLE_VERIFIER_STRUCTURAL_INVALIDITY`;
- PRG-1 applies, so no PARTIAL_REFERENCE classification and no R3/R0/R1.

### S1
- calibration only for V by frozen contract.

Therefore:
- S5 cannot supply V-positive evidence;
- S3 cannot supply V-positive evidence;
- S2 cannot currently supply a valid V-positive or V-negative correctness witness because its required primary measurement is invalid;
- **S4 is the only still-unobserved frozen V-witness opportunity.**

## 2. Kill BFSC now?

NO.

The frozen V gate requires at least one V-positive task among S2-S5.

S4 has not yet been observed.

Killing BFSC now would convert:
- one valid V-negative task,
- one V-ineligible partial task,
- one measurement-invalid task,

into a global scientific negative without observing the final frozen witness slot.

That would exceed the evidence scope.

BFSC therefore remains PRECARD, not PAPER_CANDIDATE and not killed.

## 3. Why S4 paid execution is not yet authorized

S2 exposed a new upstream failure mode:

> a task may have a valid runtime, valid agent execution and plausible implementation, while the frozen verifier itself is structurally incompatible with the frozen task architecture.

This is not the same as the S3 partial-reference problem.

It is a measurement-admission problem.

If S4 has the same class of verifier incompatibility, then:
- mechanism exposure,
- common-prestate construction,
- R2/R3 model spend,

cannot produce the frozen V/H evidence required by the existing contract.

Therefore the next selector action must test verifier compatibility before paying for S4 scientific execution.

## 4. VERIFIER_COMPATIBILITY_GATE — prospective S4 only

This gate changes execution admission only.

It does NOT:
- modify the frozen correctness endpoint;
- change H/V thresholds;
- replace the official verifier;
- repair S2;
- rescore S2;
- introduce a new metric;
- alter the task set.

### Gate question

> Does the frozen S4 verifier execute against the frozen S4 base architecture in a way that can actually reach and discriminate the task-specific behaviors it claims to measure?

### Allowed evidence

Zero-model, outcome-blind evidence only:
- frozen S4 task metadata;
- frozen S4 base commit/source;
- frozen verifier/test command/source;
- no-patch verifier execution if available;
- static import/export/API compatibility checks needed to establish whether the verifier can reach its behavioral assertions.

### Forbidden evidence

Do not use:
- S4 reference/gold patch;
- future successful trajectory;
- post-revision model output;
- oracle session/intents;
- canonical goals as solution hints;
- repaired verifier created after observing a scientific arm.

### PASS

`VERIFIER_COMPATIBLE` only if:
- verifier/runtime executes on the exact base;
- any expected no-patch task failure occurs inside the intended behavior under test, not because the harness calls a nonexistent API/class/path;
- the published task-specific gates are mechanically reachable under the frozen base architecture.

### FAIL

`VERIFIER_STRUCTURALLY_INVALID` if:
- the harness fails before task behavior because it imports/instantiates/calls an API that cannot exist in the frozen base;
- required test assets or commands are structurally incompatible with the frozen base/runtime;
- the purported primary endpoint cannot distinguish a correct from incorrect implementation without changing the verifier.

### NONIDENTIFIABLE

If static/no-patch evidence cannot establish compatibility without solution-bearing evidence:
`VERIFIER_COMPATIBILITY_NONIDENTIFIABLE`.

## 5. Consequences

### If S4 verifier compatibility PASS

Next:
`S4_MECHANISM_EXPOSURE_GATE_V1`

Only after exposure/boundary/leverage/runtime gates pass may S4 paid execution be considered.

PARTIAL_REFERENCE_GUARD remains binding prospectively.

### If S4 verifier structurally invalid

Do not repair it inside the same frozen Stage-B experiment.

Then all remaining V-witness slots are exhausted as:
- S5 negative;
- S3 ineligible;
- S2 measurement-invalid;
- S4 measurement-invalid.

Return to selector for a PRECARD identifiability decision.
Do not call that a BFSC method negative.

### If S4 verifier compatibility nonidentifiable

Stop before paid execution and return to selector.

## 6. Why this gate precedes S4 mechanism exposure

Previously, MECHANISM_EXPOSURE_GATE was the cheapest upstream falsifier.

After S2, verifier compatibility is even more upstream for S4:

- no valid measurement -> exposure cannot become decision-changing evidence;
- valid measurement + no exposure -> kill S4 before paid run;
- valid measurement + exposure -> proceed to boundary/leverage.

Thus the new shortest path is:

`S4_VERIFIER_COMPATIBILITY -> S4_MECHANISM_EXPOSURE -> boundary/leverage/runtime -> paid arms if still justified`.

This is a resource-ordering repair, not a scientific metric change.

## 7. Exact next transition

`S4_VERIFIER_COMPATIBILITY_GATE_V1` only.

Task:
`pi-mono-auto-d3b2130d`

Use zero model calls.

Do not activate:
- S4 common prestate;
- S4 R2/R3/R0/R1;
- S2 R3/R0/R1;
- any new topic family.

Do not repair or rescore the completed S2 verifier/R2.
