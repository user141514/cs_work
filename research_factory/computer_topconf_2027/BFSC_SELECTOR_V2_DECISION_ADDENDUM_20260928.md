# BFSC Selector V2 Decision Addendum — Strongest Cheap Rival Gate

date: 2026-09-28
status: FROZEN_AFTER_S1__BEFORE_S2_S5_SCIENTIFIC_OUTCOMES
scope: additional candidate-value / search-continuation gate
does_not_modify:
- SPEC_TRANSFER_G0_FALSIFIER_V1.md Stage-B PASS_HEADROOM
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md arm semantics
- S1_STAGE_B_CONTROLLED_REPLAY_RESULT_V1.md

## 0. Why this addendum exists

S1 established:
- R3 ORACLE_SCOPED matches R2 FULL_RESTART correctness;
- R3 preserves material pre-revision work and is cheaper than R2;
- R0 RAW_HISTORY also matches correctness and is cheaper than R3 on S1.

Therefore the first unresolved scientific pressure is no longer merely:
`can selective rederivation beat full restart?`

It is:
`is there a real evolving-requirement regime where selective rederivation adds value over the cheapest simple state-reuse rival?`

This is a post-S1 model update.
It must not retroactively change the original Stage-B claim or count S1 as prospective evidence for the new value gate.

## 1. Strongest cheap rival

Primary cheap-rival set:
- R0 RAW_HISTORY;
- R1 CONSOLIDATED_REFRESH.

R2 FULL_RESTART remains the behavioral reference, not the cheap rival.

Per task, the strongest cheap rival is the lowest reported post-revision model cost among R0/R1 arms that reach the same frozen verifier-success status as R2.

If neither cheap rival matches R2, the task exposes correctness pressure.

## 2. Prospective value gate V

Only S2-S5 may satisfy this gate.

A remaining task counts as a **V-positive pressure witness** if R3 is valid, preserves >=30% of pre-revision derived work, and one of the following holds.

### V-A — correctness rescue

- R2 reaches the frozen verifier-success condition;
- R3 reaches the same condition;
- at least one cheap rival R0/R1 does not;
- R3 is not strictly dominated by the other cheap rival on both correctness and reported model cost.

Interpretation:
stale/raw or refresh-only reuse creates behavioral pressure that dependency-scoped rederivation can repair.

### V-B — efficiency frontier

- R3 and the strongest correct cheap rival reach the same frozen verifier-success condition as R2;
- R3 reported post-revision model cost <= 0.90 * strongest-correct-cheap-rival cost;
- R3 preserves >=30% pre-revision derived work.

The 10% margin is a frozen practical relevance threshold for this pilot, not a universal scientific constant.

Fallback only if reported model cost is unavailable for a task:
use noncached input+output tokens with the same 10% margin; do not choose the cheaper metric after seeing the outcome.

## 3. Search-continuation rule

After S2-S5:

- Original Stage-B PASS_HEADROOM still uses its original frozen criteria.
- V is an additional requirement for authorizing family-specific method development.

Allowed outcomes:

### HEADROOM_FAIL
Original Stage-B necessary condition fails.
Close the selective-update portfolio in this frozen regime.

### HEADROOM_PASS__VALUE_FAIL
Original headroom passes, but no S2-S5 task is V-positive.
Conclusion:
selective rederivation can technically preserve BFSC/reuse but has not shown decision value over cheap rivals.
Do not train a dependency estimator or promote a PAPER_CANDIDATE.

### HEADROOM_PASS__VALUE_WITNESS
Original headroom passes and >=1 S2-S5 task is V-positive.
Conclusion:
a nontrivial pressure regime exists.
Proceed to complete-claim prior filters for the frozen mechanism families before any family-specific implementation.

This is still not PAPER_CANDIDATE admission.

## 4. Anti-drift rules

- S1 cannot satisfy V.
- Do not change the 10% margin after S2-S5 outcomes.
- Do not replace reported model cost with another metric after seeing an unfavorable result.
- Do not add a new family because R0 is strong; family identities are frozen separately from the rival gate.
- R0/R1 failure caused by INVALID runtime/session/requirement exposure is not a V-positive witness.
- A V-positive task must retain the same task/verifier/requirement contract as the frozen Stage-B protocol.

## 5. Next decision-changing action

Follow LIVE_STATE.md:
S5 offline freeze first.

Before paying for new model calls:
- freeze TASK_INITIAL_STATE;
- freeze pre-revision sequence / late revision;
- freeze outcome-blind R3 impact scope;
- confirm work headroom is nontrivial.

Then use Execution Leverage to decide the cheapest arm order that can still adjudicate the original Stage-B condition plus V.
