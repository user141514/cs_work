# BFSC Mechanism Portfolio V2 — Remaining-Horizon Freeze

date: 2026-09-28
status: FROZEN_AFTER_S1_CALIBRATION__BEFORE_S2_S5_SCIENTIFIC_OUTCOMES
parent:
- SPEC_ANCESTRY_TRANSFER_V1.md
- TRANSFER_PRIOR_ATTACK_20260928.md
- SPEC_TRANSFER_G0_FALSIFIER_V1.md
selector_contract:
- C:/Users/Administrator/.agents/skills/top-conference-topic-selection/training/live/MECHANISM_SPACE_FORMATION_GATE.md
- C:/Users/Administrator/.agents/skills/top-conference-topic-selection/training/live/FINAL_LIVE_RESEARCH_SELECTOR.md
- C:/Users/Administrator/.agents/skills/top-conference-topic-selection/training/live/DECISION_CONTRACT_GATE.md
candidate_value_addendum:
- BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md

## -1. Temporal / contamination boundary

S1 scientific outcome is already observed and fixed in `S1_STAGE_B_CONTROLLED_REPLAY_RESULT_V1.md`.

Therefore:
- this file is **not** a claim of pre-S1 prospective freezing;
- the mechanism family identities below are compiled only from the pre-S1 ancestry artifacts, which already explicitly contain Program Slicing A1, Self-Adjusting Computation B1 and Incremental View Maintenance C1;
- S1 may update family ranking / strongest-rival pressure, but may not create a new family;
- S2-S5 are the remaining prospective validation horizon.

S1 calibration:
- R3 matches R2 correctness and preserves work;
- R3 is cheaper than R2;
- R0 raw history also matches correctness and is cheaper than R3 on S1.

Thus strongest-rival value, not R3-vs-R2 feasibility alone, is now the upstream paper-value bottleneck.

## 0. Interface

Consumer:
coding agents operating under evolving requirements.

Pressure:
revision-history execution can diverge from execution from the consolidated final authoritative specification, while full restart discards potentially reusable work.

Complete claim graph:

requirement/spec delta
->
validity of previously derived decisions/tests/code/actions
->
bounded update/rederivation operator
->
verifier-observable Behavioral From-Scratch Consistency (BFSC)
+
material reuse/recomputation economy.

Current direct-prior boundary:
the bounded prior attack found diagnostics of path sensitivity, plan-dependency validation, spec/code impact analysis and provenance tooling, but no single inspected prior matching the full consumer/state/intervention/evidence graph above.

Lifecycle:
PRE_TOPIC_TRANSFER_PROBE.
No PAPER_CANDIDATE.

## 1. Shared interface-level necessary condition H

H is the original frozen Stage-B headroom condition:
there exists a nontrivial subset of pre-revision derived work that can be preserved across meaningful requirement revisions while an update procedure approaches the verifier behavior of a clean final-spec execution.

The original Stage-B PASS_HEADROOM criteria are unchanged.

S1 result:
`H_LOCAL_PASS` for R3-vs-R2, but the full S1-S5 H verdict remains unresolved.

This condition is intentionally shared by the three families below.
Sharing H does not make them one family; their family-specific state and update operators differ.

Post-S1, H is necessary but no longer sufficient for further method investment.
The additional strongest-cheap-rival value gate V is frozen in `BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md` and applies prospectively only to S2-S5.

## 2. Family F1 — Static Semantic Impact Slice

FAMILY_PROVENANCE_TICKET:
Program Slicing ancestor
+
frozen mismatch that coding-agent dependencies are semantic/cross-artifact
->
construct an outcome-blind semantic requirement-to-artifact impact slice before rederivation.

State:
current requirement/spec atoms + repository/spec/code structure + explicit verification obligations.

Operator:
compute a conservative affected closure from the changed requirement and rederive/recheck only that closure.

Distinct causal assumption:
useful dependency scope can be recovered primarily from authoritative/static semantic structure without requiring a full runtime derivation trace.

Family-specific failure mode:
safe slice recall requires an almost-global closure, or missing semantic edges make static impact analysis unsound even when dynamic provenance would have exposed them.

Current prior pressure:
SpecD occupies weak claims around spec/code graphs and impact analysis.
F1 remains eligible only if the complete BFSC + recomputation-economy contract is not directly occupied.

State:
SURVIVING_PENDING_FAMILY_PRIOR_FILTER.

## 3. Family F2 — Dynamic Behavioral Derivation Graph

FAMILY_PROVENANCE_TICKET:
Self-Adjusting Computation ancestor
+
frozen mismatch that agent dependencies are stochastic, semantic and partly latent
->
record runtime derivation lineage and selectively invalidate/reexecute affected derived state.

State:
runtime lineage spanning requirement -> decision/plan -> verification/test -> code/action artifact.

Operator:
record dynamic dependency edges during execution; on revision invalidate the transitive affected closure; rederive it; preserve independent nodes; update lineage as execution changes.

Distinct causal assumption:
runtime execution reveals decision dependencies that static structure cannot recover reliably enough.

Family-specific failure mode:
important dependencies remain latent/unrecorded, lineage capture becomes too coarse, or graph maintenance/reexecution cost erases reuse benefit.

Current prior boundary:
PlanFence and SpecD are adjacent but the bounded prior attack found no single prior owning runtime cross-artifact derivation + selective rederivation + BFSC + recomputation economy.

State:
SURVIVING; current strongest family.

## 4. Family F3 — Typed Requirement/Artifact Delta Propagation

FAMILY_PROVENANCE_TICKET:
Incremental View Maintenance / provenance ancestor
+
frozen mismatch that requirement changes should transform derived artifacts rather than force full history replay
->
represent add/remove/replace requirement deltas and propagate typed deltas through obligation/test/implementation state.

State:
authoritative requirement delta + typed derived artifact state + provenance relation.

Operator:
derive and apply artifact deltas, revalidating only affected typed obligations, instead of treating the update purely as invalidate-and-replay.

Distinct causal assumption:
some revision effects can be represented as compositional state transformations; explicit delta semantics can preserve correctness without reconstructing the whole agent trajectory.

Family-specific failure mode:
agent branch changes are too non-compositional/stochastic for useful delta algebra, so updates collapse back to broad rederivation.

Current prior pressure:
SpecD already occupies deterministic spec-delta handling at an engineering level.
F3 requires a stronger typed cross-artifact semantics + BFSC evidence contract to survive; otherwise it is DIRECT_VETO / PL-only watchlist.

State:
SURVIVING_PENDING_FAMILY_PRIOR_FILTER.

## 5. Why these three are orthogonal

F1 acquires dependency scope from static/authoritative structure.

F2 acquires dependency scope from the actual runtime derivation process.

F3 changes the update semantics itself from invalidation/reexecution to typed delta propagation.

They share H but do not share the same family-specific failure mode:
- static slice can fail while dynamic lineage succeeds;
- dynamic lineage can be costly/noisy while typed delta semantics succeeds on explicit artifact transitions;
- typed delta compositionality can fail while rederivation remains viable.

Parameter choices, dependency-model architectures, thresholds and benchmark swaps do not create additional families.

## 6. Reclassification of existing Stage-B oracle smoke

Existing arms:
- R0 RAW_HISTORY
- R1 CONSOLIDATED_REFRESH
- R2 FULL_RESTART
- R3 ORACLE_DEPENDENCY_SCOPED_REDERIVATION

V2 role:
R3 is not evidence that F2's eventual learned/runtime dependency estimator works.

R3 is a **shared necessary-condition / oracle-headroom discriminator** for H:
if a best-effort outcome-blind dependency scope cannot create a correctness/reuse region, do not spend work on F1/F2 dependency estimators and strongly demote F3's reuse premise.

Observed S1:
- R3-vs-R2 H headroom: local positive;
- R3-vs-R0 method value: local negative.

Therefore S1 does not select any family.
It only establishes that H is possible on one task while exposing R0 as the strongest cheap rival.

Positive scope on future tasks:
selective-update headroom exists; family-specific state/operator questions remain open.

Negative scope:
kills the selective-update economic premise in the frozen SWE-Together regime only if R3 is valid and the original shared-H predicate fails on the frozen Stage-B decision.
It does not prove all specification-state research is dead.

## 7. Execution order

1. keep this F1/F2/F3 portfolio frozen for S2-S5;
2. preserve existing exact asset/task freeze and all original Stage-B thresholds;
3. apply `BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md` prospectively to the remaining tasks;
4. execute only the minimum Stage-B evidence needed to adjudicate H plus the strongest-cheap-rival value gate V;
5. if H fails validly, close this portfolio for the frozen regime;
6. if H passes but V has no witness, close the current paper route for insufficient value over cheap rivals;
7. only if H passes and V has a witness, run complete-claim prior filters for F1/F2/F3 before family-specific implementation;
8. choose the surviving family with the best mechanism leverage / novelty runway / evidence latency;
9. no fourth/fifth family may be introduced from S2-S5 outcomes unless new evidence changes the interface model.

No learned dependency estimator, benchmark expansion or new field scan is authorized before H + V are adjudicated.
