# Decision Contract Gate V1

Date: 2026-09-27
Status: AUTHORITATIVE_PROJECT_GATE
Applies to: every PRECARD_LEVERAGE discriminator, candidate-admission rule, GAP gate that can kill a claim, and METHOD_PILOT.

## Purpose

Compile research invariants into the executable decision boundary of each concrete experiment.

This gate owns logical identifiability and verdict scope.
Execution-cost escalation is owned separately by research_factory/EXECUTION_LEVERAGE_GATE_V1.md.

A high-level rule in a Skill, OS, project card, or prose paragraph does not count unless it changes:
- the arm set;
- the pass/fail predicate;
- the execution order;
- or the allowed verdict.

Before execution, both gates must pass:
- Decision Contract: is the experiment logically valid for the owned decision?
- Execution Leverage: is this the minimum sufficient evidence level for that decision?

## Required contract

Before execution, freeze:

1. CLAIM
   - exact claim;
   - lifecycle stage;
   - positive scope;
   - negative scope.

2. STRONGEST_CHEAP_RIVAL
   - required when the owned decision includes method/value comparison;
   - named executable/reconstructable rival and endpoints used for dominance;
   - otherwise freeze `N/A` with the reason.

3. MECHANISM_CONTROL
   - required when attribution to a named mechanism is part of the owned decision;
   - otherwise freeze `N/A` with the reason.

4. HEADROOM
   - required when the success predicate needs an improvement/recovery/dynamic-range threshold;
   - record baseline error/recoverable mass/dynamic range and the minimum headroom needed to make success reachable;
   - otherwise freeze `N/A` with the reason.

5. VALUE_ESTIMAND_AND_PASS_PREDICATE
   - for method/value claims, freeze what counts as a meaningful frontier/utility improvement, including practical margins and uncertainty handling;
   - strict non-domination is necessary but not sufficient;
   - include all material inference, estimation, routing, and runtime costs used by the claimed method.

6. NEGATIVE_PREDICATE
   - distinguish exactly:
     - INVALID_OR_NONIDENTIFIABLE;
     - REPAIR_NEGATIVE;
     - CLAIM_NEGATIVE;
     - CANDIDATE_KILL.

7. EXECUTION_ORDER
   - cheapest prerequisites first;
   - stop when a prerequisite makes the downstream PASS condition unreachable.

8. ATTRIBUTION_CHECK
   - use a claim-appropriate estimand against the matched control;
   - for a simple mechanism main effect, this may be a paired no-M contrast;
   - for an interaction claim, require a factorial interaction / difference-in-differences or equivalent interaction estimand rather than a simple winner comparison.

9. COUNTEREXAMPLE_WITNESSES
   - PASS_WITHOUT_VALUE?
   - FAIL_WITHOUT_IDENTIFICATION?
   - WIN_WITHOUT_ATTRIBUTION?

Any unresolved witness blocks execution.

## Hard invariants

### I1 — Reachability
A preregistered primary success threshold must be achievable on the population/sample that owns that primary decision under the frozen headroom rule.

If the realized frozen primary sample makes the threshold mathematically unreachable: `PRIMARY_DECISION_NONIDENTIFIABLE__INSUFFICIENT_HEADROOM`.

If headroom itself is stochastic/estimated, freeze an independent preflight or an uncertainty/power rule before reveal; do not condition a scientific conclusion on an opportunistic tiny baseline screen.

A non-identifiable primary decision does **not** imply that all secondary/held-out arms have zero information value. Secondary arms may still run only when they own separately preregistered questions (e.g. harm, generalization, or future-substrate selection); they cannot rescue or convert the non-identifiable primary verdict.

### I2 — Meaningful frontier gain
When the owned decision is a method/value comparison, strict non-domination by the strongest cheap rival is only a floor. PASS additionally requires the preregistered meaningful frontier expansion / utility / non-inferiority margins with uncertainty handling and full method cost accounting.

### I3 — Attribution
When the owned decision attributes benefit to a named mechanism, the claim requires a matched control and a claim-appropriate contrast. Interaction claims require an interaction estimand (factorial contrast / difference-in-differences or equivalent), not merely `method > no-mechanism control`.

### I4 — Kill scope
Candidate-level KILL requires:
- a valid necessary-condition falsifier; or
- a valid direct-method negative for the activated claim.

Proxy/oracle/ranking negatives only change repair ranking unless an explicit logical implication was frozen.

### I5 — Staged execution
If A is a prerequisite for B, run/inspect A before spending on B.
A prose kill rule that is not bound to execution order is not considered enforced.

## Minimal template

DECISION_CONTRACT_ID:
LIFECYCLE_STAGE:
CLAIM:
POSITIVE_SUPPORTS:
NEGATIVE_FALSIFIES:
STRONGEST_CHEAP_RIVAL:
DECLARED_ENDPOINTS:
MECHANISM_CONTROL:
HEADROOM_MEASURE:
REQUIRED_HEADROOM:
HEADROOM_PRECHECK:
VALUE_ESTIMAND:
PRACTICAL_MARGINS:
UNCERTAINTY_RULE:
FULL_COST_ACCOUNTING:
PASS_PREDICATE:
INVALID_OR_NONIDENTIFIABLE_PREDICATE:
REPAIR_NEGATIVE_PREDICATE:
CLAIM_NEGATIVE_PREDICATE:
CANDIDATE_KILL_PREDICATE:
EXECUTION_ORDER:
PRIMARY_VS_SECONDARY_QUESTIONS:
EARLY_STOP_RULES:
COUNTEREXAMPLE_AUDIT:
- PASS_WITHOUT_VALUE:
- FAIL_WITHOUT_IDENTIFICATION:
- WIN_WITHOUT_ATTRIBUTION:

## Paper-02 calibration example

If the primary pass rule requires >=2 A->C recoveries on a frozen main set:
- compute the reachable recovery count on that same primary set;
- if the realized primary Arm A has <2 false accepts, the primary >=2-recovery decision is NONIDENTIFIABLE on that set;
- do not reinterpret C<2 there as a direct failure of the evidence-diversity claim.

Separately preregistered held-out/generalization or harm arms may still provide useful evidence, but they do not rescue or overturn the non-identifiable primary decision. Portfolio closure for poor substrate economics may still occur, but it must be labeled separately from scientific falsification.

## Current Bet-B calibration example

For a cost-accuracy correlation-aware stopping claim, the contract must include:
- strongest single model (TOP1);
- fixed committee;
- matched adaptive stopping without correlation information;
- correlation-aware stopping.

PASS requires:
- a preregistered meaningful expansion of the cost-accuracy frontier or utility relative to TOP1 and the strongest matched stopping baseline, not merely non-domination;
- practical margins and uncertainty handling frozen before execution;
- correlation-estimation/routing/runtime overhead included in cost;
- if the claim attributes value specifically to correlation, a matched no-correlation control evaluated with the same value estimand.
