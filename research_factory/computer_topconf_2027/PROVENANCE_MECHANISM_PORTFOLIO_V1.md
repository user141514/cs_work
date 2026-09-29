# Provenance-Constrained Data Selection — Mechanism Portfolio V1

date: 2026-09-28
status: PORTFOLIO_NO_EXECUTABLE_POSITIVE__INTERFACE_RETAINED
parent_backtest: SELECTOR_MECHANISM_SPACE_BACKTEST_20260928.md
source_interface: provenance-constrained post-training data curation under incomplete source metadata and finite audit effort
formal_paper_candidate: false

## Interface pressure retained

Frozen local evidence retained from the earlier Data Selection run:
- TAGCOS A0: provenance ambiguity intersects a large fraction of selected post-training mass;
- TAGCOS A1: active source auditing materially beats uniform random allocation;
- A1 attribution: auditability-first beats value-guided priority;
- ERU static product scoring is killed by frozen held-out dominance and is not eligible for rescue.

The interface remains scientifically open. This portfolio asks which causal mechanism family should receive the next bounded discriminator.

## Complete-claim prior boundary used here

Primitive-level matches do not veto a family.
A direct veto requires one concrete prior to match the full consumer/state/intervention/evidence contract.

Current 2026 anchor priors checked:
- Tracing the Roots, ACL 2026 / arXiv:2604.10480;
- RLVR Datasets and Where to Find Them / ATLAS, arXiv:2605.26971;
- Provenance-Grounded Gating and Adaptive Recovery, arXiv:2606.11127;
- Value of Information: A Framework for Human-Agent Communication, ACL 2026;
- Audit Me If You Can: Query-Efficient Active Fairness Auditing of Black-Box LLMs, Findings ACL 2026;
- MixtureVitae, arXiv:2509.25531;
- generic active-learning and distributionally robust data-selection work.

None is treated as a stitched veto.

---

## Family A — Static expected-recoverable-utility ranking

Causal object:
one-shot scalar ranking before any audit outcome is observed.

Frozen realization:
ERU_SCORE = source_mass * P(resolve | ambiguity_class).

Status:
SCIENTIFIC_NEGATIVE / CLOSED.

Reason:
held-out Tulu-3 ERU and VALUE_ONLY choose the same K=5 set, making the frozen required margin impossible for every possible audit outcome.

Forbidden:
coefficient/K/class-probability/cost/threshold rescue.

---

## Family B — Sequential information acquisition

Causal object:
audit outcomes change the belief state used to choose later audits.

Complete claim:
post-training mixed source pool + incomplete provenance state grouped by frozen auditability classes + finite sequential source-audit budget -> choose the next source by finite-horizon expected recovered provenance value, including information gained about remaining sources -> recover more provenance-resolved selected mass than static value/auditability/ERU policies at equal audit count.

Why this is not ERU:
ERU freezes all source scores before outcomes.
Family B is a closed-loop policy: audit result at step k changes the posterior state and can change action k+1.

Current-prior screen:
DIRECT_CONTRACT_OPEN_WITH_ADJACENT_PRIORS.

- generic VoI work uses decision-theoretic information acquisition in other consumers;
- active fairness auditing optimizes which model queries to inspect;
- ActiveLLM / active learning chooses examples/labels;
- Tracing the Roots and ATLAS reconstruct/use lineage for curation;
- none of the inspected concrete works matches the complete post-training provenance-audit sequential contract above.

Asset gate:
PASS for a Level-0 structural preflight; no held-out source-card outcomes are required.

Frozen state available before held-out auditing:
- TAGCOS class-level resolution counts;
- frozen ambiguity classes;
- Tulu-3 17-source ambiguous universe and source masses;
- K=5;
- static ERU/value/auditability rivals.

Logical-dominance / decision-distinctness screen:
**FAIL — CURRENT REALIZATION IS DECISION-EQUIVALENT.**

Authority:
`PROVENANCE_B_VOI_PREFLIGHT_RESULT_V1.md`.

The minimum class-shared sequential Bayesian realization uses Beta(5,1) for class 2 and Beta(1,3) for class 3, updates the relevant posterior after each binary audit result, and recomputes the finite-horizon optimal action.

An exhaustive dynamic program over all binary outcome paths shows exactly one reachable terminal K=5 audit set:
{Aya, FLAN v2, Tulu 3 Persona MATH, Evol CodeAlpaca, NuminaMath-TIR}.

That set is exactly the frozen ERU and VALUE_ONLY K=5 set. Therefore recovered mass at K=5 is identical for every possible held-out outcome. Completing the source-card audit cannot change the owned decision.

Status:
`NO_DECISION_DISTINCT_REALIZATION_UNDER_CURRENT_FROZEN_STATE`.

This does not kill all VoI methods. A richer source-specific belief/correlation state could create different actions, but that state is not present in the frozen assets and may not be invented post-result as a rescue.

---

## Family C — Robust/constrained selection under provenance uncertainty

Causal object:
choose the training subset/mix to maximize utility under an ambiguity set over unresolved provenance/admissibility states.

Current-prior screen:
DIRECT_CONTRACT_OPEN_BUT_NEAR_STRONG_ADJACENCY.

Adjacent:
- MixtureVitae already performs permissive-first, license-aware filtering and domain-aware mixing;
- generic DRO/data-pruning methods optimize worst-case distribution or group performance, but not unresolved provenance-state uncertainty.

Asset / identifiability screen:
NONIDENTIFIABLE_UNDER_CURRENT_FROZEN_ASSETS.

Reason:
the frozen TAGCOS/Tulu evidence contains source mass, ambiguity class and audit outcomes, but not a defensible source-level downstream utility function plus calibrated provenance-state ambiguity set that would distinguish robust optimization from hard traceable-only filtering, simple permissive-first corpus construction, or static value ranking.

Inventing a utility or uncertainty set now would create a new evaluation contract after seeing the earlier failures.

Status:
DEFERRED__NO_SCIENTIFIC_PRECARD.

---

## Family D — Constraint-aware replacement / recovery

Causal object:
after ordinary selection identifies high-value but provenance-ineligible/ambiguous mass, replace it with utility-equivalent traceable alternatives rather than simply dropping it.

Current-prior screen:
ADJACENT_PRIOR__NOVELTY_CONSTRAINED.

Strong adjacent:
Provenance-Grounded Gating and Adaptive Recovery (arXiv:2606.11127) already combines source-grounded provenance/faithfulness gating with targeted recovery/regeneration in synthetic post-training pipelines.

Why not direct veto:
that work assumes the generation-source relation is already available and repairs faithfulness/rejected synthetic samples.
The current family would require unknown source admissibility plus a substitute relation preserving training utility.

Asset gate:
ASSET_BLOCKED_FOR_CHEAP_PRECARD.

Missing:
- candidate substitute graph/pool;
- source-to-substitute equivalence representation;
- evaluator showing replacement preserves the downstream training-utility claim.

Building these now would exceed the current zero/low-compute provenance replay advantage.

Status:
DEFERRED__NO_SCIENTIFIC_PRECARD.

---

## Portfolio ranking after Level-0 screens

No family is currently authorized for a scientific PRECARD.

Family B — Sequential information acquisition:
- complete-claim runway: open;
- current minimum realization: structurally decision-equivalent at K=5;
- richer realization would require new state;
- status: deferred / no executable decision-distinct realization.

Family C — Robust provenance-uncertainty selection:
- novelty runway: open but close to permissive-first / DRO neighbors;
- current identifiability: insufficient;
- status: deferred.

Family D — Replacement/recovery:
- strong adjacent 2026 recovery prior;
- substitute/equivalence assets missing;
- status: asset blocked for cheap PRECARD.

Family A remains scientifically closed.

## Handoff tree

Family B Level-0 decision equivalence
-> do not complete the held-out source audit for B;
-> do not rescue B by adding source-specific priors/correlations after this result;
-> C/D remain deferred, not automatically activated;
-> return `PORTFOLIO_NO_EXECUTABLE_POSITIVE__INTERFACE_RETAINED`.

A future independently obtained asset may cause C or D to re-enter portfolio competition, but that would be a new topic-formation round rather than continuation of this one.

## Next exact action

Prospective validation of the mechanism-space selector on this Synthetic Data interface is complete.

The correct output is bounded abstention without scientific over-kill:
- the provenance-constrained interface remains open;
- no current family deserves PRECARD compute;
- no fifth family is generated.

Return control to the broader frozen interface portfolio / current Rank-1 research object and apply the same mechanism-space formation gate before resuming any method experiment.
