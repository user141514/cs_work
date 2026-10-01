# BFSC Selector Replan After S3 Partial-Adjudication Gap — 2026-10-01

date: 2026-10-01
status: CONTINUE_PRECARD__S2_MECHANISM_EXPOSURE_NEXT
scope: BFSC/selective-rederivation remaining frozen S2/S4 horizon
formal_paper_candidate: false
does_not_modify:
- SPEC_TRANSFER_G0_FALSIFIER_V1.md Stage-B PASS_HEADROOM
- BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md value gate V
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md arm identities
- S1/S3/S5 historical outcomes
- BFSC_MECHANISM_PORTFOLIO_V2_20260928.md family identities

## 1. Selector audit

The authorized S3 sequence is complete.

Observed prospective value evidence now is:

- S5:
  - R2/R3 local headroom = PASS;
  - R0 matches correctness and is much cheaper;
  - V = NEGATIVE.
- S3:
  - R2 valid but partial: frozen verifier reward 0.7650, full_success=false;
  - R3 valid, reuse threshold strongly passes, and is materially cheaper;
  - R3 frozen verifier reward 0.5850, full_success=false;
  - the pre-registered S3 local gate did not define partial-vs-partial `matches/approaches`;
  - local headroom therefore remains `INCONCLUSIVE_PRE_REGISTERED_RULE_GAP`;
  - R0/R1 were correctly not authorized.
- S1 remains calibration only for V and cannot satisfy V by contract.

Under the frozen V gate, S3 cannot become a V-positive witness because both V-A and V-B require R2 to reach the frozen verifier-success condition.

Therefore the only unobserved V-positive witness opportunities are now:

- S2 — `pi-mono-auto-a4fca584`;
- S4 — `pi-mono-auto-d3b2130d`.

The frozen pre-outcome execution order remains S2 before S4.

## 2. What the S3 result changes

S3 does **not** validly kill BFSC.

The new evidence changes the experiment-control model:

> a valid FULL_RESTART arm may itself finish as a partial verifier failure, leaving the local R2-vs-R3 phrase `matches/approaches` under-specified.

This is a measurement/adjudication contract defect, not a new scientific metric and not a reason to reinterpret S3 after the fact.

Progress kind:
- `MODEL_CHANGE`: the selector must model behavioral-reference qualification explicitly;
- `MEASUREMENT_REPAIR`: future task execution must avoid producing an unscorable local comparison when R2 is partial.

No historical result is rescored.

## 3. PARTIAL_REFERENCE_GUARD — prospective S2/S4 execution only

This guard changes execution authorization only.
It does **not** change the frozen Stage-B correctness endpoint, PASS_HEADROOM thresholds, value gate V, 10% cost margin, reuse threshold, task set, or mechanism families.

### PRG-1 — R2 validity

If R2 runtime/session/verifier is invalid:
- repair runtime only if bounded;
- no scientific verdict;
- no R3/R0/R1 until validity is restored.

Unchanged from existing protocol.

### PRG-2 — R2 behavioral-reference qualification

After a valid R2:

If `R2.full_verifier_success == true`:
- the existing task-local R2->R3 leverage logic may proceed unchanged;
- existing frozen V-A/V-B semantics remain available.

If `R2.full_verifier_success == false`:
- mark the task-local behavioral reference `PARTIAL_REFERENCE`;
- do not invent a scalar reward threshold, reward ratio, or gate-vector dominance rule to declare local R3 `matches/approaches`;
- the task cannot be V-positive under the already-frozen V-A/V-B contract because those require R2 frozen verifier success;
- no R0/R1 may be run for V on that task.

This rule is prospective for S2/S4 and is **not** retroactively applied to relabel S3.

### PRG-3 — whether R3 is still worth paying for after PARTIAL_REFERENCE

A partial R2 does not automatically authorize or forbid R3.

Before paying for R3, Execution Leverage must ask:

> Can this R3 outcome still change the original frozen Stage-B H decision through verifier-success count, median reuse, or another already-frozen endpoint?

- If no: stop that task after R2 as decision-irrelevant.
- If yes: R3 may run only for that pre-existing H endpoint; do not call its local comparison PASS/NEGATIVE unless the original contract already identifies it.

This prevents a second S3-style paid run whose local interpretation is undefined while preserving the original five-task H accounting when R3 evidence is genuinely necessary.

### PRG-4 — no post-hoc rescue

After any S2/S4 outcome:
- do not modify this guard;
- do not change H/V thresholds;
- do not rename verifier success;
- do not add a new cheap rival or mechanism family to rescue BFSC.

## 4. Portfolio decision

### Kill now?

NO.

Reason:
the frozen V gate requires at least one V-positive task among S2-S5. S5 is negative and S3 is ineligible, but S2 and S4 remain prospectively unobserved. Killing BFSC now would exceed the logical scope of current negative evidence.

### Pay for S2 now?

NO.

Reason:
the selector's MECHANISM_EXPOSURE_GATE must be applied before any new family-specific paid intervention, and S2 has not yet passed its task-specific exposure/boundary/leverage chain.

### Activate S4 now?

NO.

Reason:
the frozen expected-falsification ordering ranks S2 above S4. S4 is more additive and lower expected stale-state conflict. Parallel activation would spend budget without changing the next decision.

## 5. S2 hypothesis before any new paid run

Frozen S2 evolution:
`analyze-only -> implementation authorized -> revised settings.json-relative path semantics -> exercise/documentation follow-up`.

The only selector-relevant question to test next is:

> Did the late path-semantics revision act on already-created implementation/decision state strongly enough that stale-state survival or selective invalidation is actually exposed?

This is not yet assumed true.

Counterexample:
if the pre-revision state never instantiated the path-resolution decision that the late requirement changes, then S2 may have static requirement evolution but no active stale-state mechanism exposure. In that case paid R2/R3 is low leverage.

## 6. Exact next transition

`S2_MECHANISM_EXPOSURE_GATE_V1` only.

Use only:
- frozen Stage-A S2 identity;
- verbatim ordered user requirements available before the late revision;
- the late revision itself;
- task/base static source when needed to identify whether the changed semantic relation is executable.

Do not use:
- reference/gold patch;
- verifier outcome;
- future successful trajectory;
- S2 post-revision model result;
- S3/R2 implementation details as a solution template.

Expected output:
- `EXPOSURE_SOURCE_PROVEN`, `NO_EXPOSURE`, or `NONIDENTIFIABLE`;
- exact exposed state/relation if positive;
- kill-scope certificate;
- next authorization.

No S2 paid model arm is authorized by this selector replan.
