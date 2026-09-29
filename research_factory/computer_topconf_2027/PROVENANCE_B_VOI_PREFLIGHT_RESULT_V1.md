# Provenance Family-B Sequential VoI — Level-0 Structural Preflight

date: 2026-09-28
status: FAMILY_B_CURRENT_REALIZATION_DECISION_EQUIVALENT
parent_portfolio: PROVENANCE_MECHANISM_PORTFOLIO_V1.md
execution_level: Level 0 / existing-result computation only
heldout_provenance_outcomes_used: false
gpu_calls: 0
model_api_calls: 0

## Question

Can the first executable realization of Family B create a different K=5 audit decision from the already-killed static ERU/value-only family *before* any Tulu-3 held-out provenance outcomes are opened?

The realization uses only state that was already frozen before held-out auditing:

- Tulu-3 17 initially ambiguous sources and source masses;
- frozen ambiguity classes:
  - class 2 = multiple identifiable records;
  - class 3 = no direct record;
- TAGCOS development resolution counts:
  - class 2: 5 resolved / 6 audited;
  - class 3: 1 resolved / 4 audited;
- audit budget K=5.

No source-card outcome from the frozen Tulu-3 heldout audit is used.

## Minimum sequential model

For each ambiguity class, use the minimal exchangeable Bayesian state implied by the existing TAGCOS counts:

- class 2: Beta(5,1);
- class 3: Beta(1,3).

At each audit step, choose the remaining source that maximizes finite-horizon expected recovered provenance-resolved mass over the remaining K-step budget.

After a source audit:
- resolved -> increment that class's alpha;
- unresolved -> increment that class's beta;
- recompute the optimal next action.

This is strictly more sequential than ERU:
the policy is allowed to react to every audit result and update later choices.

It adds no new learned features or post-result source-specific priors.

## Reproducible implementation

Code:
`research_factory/computer_topconf_2027/provenance_voi_preflight.py`

Test:
`tests/test_provenance_voi_preflight.py`

TDD record:
- RED: test collection initially failed because the implementation module did not exist;
- first GREEN attempt exposed an irrelevant Python-3.7 typing compatibility issue;
- final focused test: 3 passed.

## Structural result

The exact dynamic program enumerates all binary audit-outcome paths through K=5.

Observed:

- reachable terminal K=5 audit sets: **1**;
- unique reachable set:
  - Aya
  - FLAN v2
  - Tulu 3 Persona MATH
  - Evol CodeAlpaca
  - NuminaMath-TIR
- frozen ERU K=5 set: exactly the same;
- frozen VALUE_ONLY K=5 set: exactly the same.

Therefore:

`SEQUENTIAL_VOI_K5_SET(outcomes) == ERU_K5_SET == VALUE_ONLY_K5_SET`

for every possible held-out binary provenance-resolution outcome under the frozen class-shared state model.

The internal audit order may adapt/tie-break, but the terminal set — and therefore recovered-mass endpoint at K=5 — cannot differ.

## Decision

Current Family-B realization:
**STRUCTURALLY_NON_DISCRIMINATING / DO_NOT_AUDIT_HELDOUT_FOR_THIS DECISION**.

The remaining Tulu-3 provenance source-card audit is unnecessary for deciding this realization.

This is a valid early kill by logical dominance / decision equivalence, not a scientific negative from held-out outcomes.

## Kill scope

Killed / deferred under current assets:

the minimal sequential information-acquisition realization whose transferable belief state is only the frozen ambiguity-class resolution posterior.

Not killed:

- all value-of-information methods;
- source-specific dependency/correlation models;
- richer provenance-state representations;
- the broader provenance-constrained curation interface.

However, those richer variants require new source-level state not present in the frozen assets. Introducing such state after seeing this result would be a new mechanism realization / topic-formation round, not an allowed rescue.

## Counterexample

If this judgment is wrong, there must exist at least one binary audit-outcome path under the same frozen class state and K=5 budget that changes the terminal audited source set away from the static ERU/value-only set.

The exhaustive dynamic program found none.

## Portfolio implication

Family A:
closed scientific negative.

Family B:
no decision-distinct executable realization under current frozen state.

Family C:
non-identifiable under current assets.

Family D:
cheap-precard asset blocked.

Therefore the prospective Synthetic Data portfolio ends as:

`PORTFOLIO_NO_EXECUTABLE_POSITIVE__INTERFACE_RETAINED`.

This is exactly the intended new-selector behavior:
do not falsely kill the interface, but also do not invent a fifth repair to keep it alive.
