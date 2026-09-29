# OI-AS-00 — Offline Headroom Contract

Date: 2026-09-29
Baseline: AgentSquare upstream commit 8f5b3fe5d8a32f9b59d20370823bef2a2c86928c
Status: CURRENT_STEP

## Scientific question

Before paying for any predictor/model/benchmark run, does AgentSquare's existing four-module search space contain a nontrivial set of combinations whose module descriptions imply duplicated decision authority or violation of a simple composition invariant?

If no, O+I has no obvious leverage at this seam and this insertion point should be deprioritized.
If yes, proceed to a controlled search experiment in which O+I is only a candidate filter/reranker before AgentSquare's existing predictor/evaluator.

## Fixed intervention seam

AgentSquare:
recombination() -> filtered_recombination_agents -> predict_performance() -> test top predicted agent

Proposed:
recombination() -> OI compatibility gate -> predict_performance() -> test top predicted admissible agent

No other baseline component changes in OI-AS-00.

## Frozen responsibility signatures

The signatures are intentionally coarse and derived from the upstream module descriptions, not benchmark outcomes.

Responsibilities:
- DECOMPOSE: produces subtasks/sub-goals/to-do lists or otherwise decomposes the task.
- REASON: produces/chooses reasoning paths, principles, reflection or answer reasoning.
- TOOL_SELECT: selects/retrieves tools/APIs or explicitly plans tool choice.
- MEMORY_RETRIEVE: stores/retrieves/summarizes prior task trajectories.
- CURRENT_GUIDANCE: emits current-task guidance/heuristics from prior trajectories.

A module may own multiple responsibilities.

## Orthogonality rule

For a selected combination, compute each responsibility's active owners.

Hard overlap:
- DECOMPOSE may have at most one active control owner.
- TOOL_SELECT may have at most one active control owner.
- MEMORY_RETRIEVE may have at most one active control owner.

Soft overlap / coupling:
- Planning modules may emit reasoning instructions and tool-calling instructions. This is recorded as cross-boundary guidance, not automatically rejected.
- REASON or CURRENT_GUIDANCE may have multiple contributors; this contributes to a coupling score rather than automatic rejection.
- A memory module that produces a current-task plan is not merely guidance overlap: it is treated as DECOMPOSE/PLAN_CONTROL ownership for the hard memory-boundary invariant below.

None modules own nothing.

## Frozen invariants

I1 — Tool-selection authority:
If a dedicated non-None tooluse module exists, a different module that explicitly selects a concrete tool/API creates an authority conflict. Merely emitting tool-calling instructions is soft coupling, not sufficient for I1.

I2 — Decomposition authority:
A non-planning module that explicitly generates the current task plan/subgoal decomposition conflicts with a non-None planning module.

I3 — Memory boundary:
A memory module may retrieve, select or summarize prior trajectories and may expose bounded guidance, but it must not own the current task plan/subgoal decomposition or concrete tool selection. Upstream MemoryTP explicitly asks an LLM to generate plans/strategy for the ongoing task from retrieved experience, so TP is frozen as owning PLAN_CONTROL in addition to MEMORY_RETRIEVE/CURRENT_GUIDANCE.

These invariants are structural compatibility hypotheses only. They are not assumed to predict benchmark performance yet.

## Headroom outputs

Primary denominator: enumerate the actual static ALFWorld search space implied by upstream `agent_search.py`, which filters recombination/evolution candidates to `tooluse == None`: 6×7×1×5 = 210 combinations.

Secondary diagnostic only: the full catalog Cartesian product is 6×7×5×5 = 1050, but it must not be presented as the executable ALFWorld search denominator.

Report on the 210 executable combinations:
- soft responsibility-coupling count/rate;
- hard invariant-violation count/rate;
- union hard-inadmissible count/rate;
- distribution by conflict type;
- representative configurations;
- per-module conflict participation.

The 1050 full-catalog scan may be reported separately only to show whether the same structural issue extends beyond ALFWorld's `tooluse=None` restriction.

## Decision

Apply the triage bands to the 210 executable ALFWorld combinations, not the 1050 full catalog:
- ZERO/NEGLIGIBLE_HEADROOM: <5% hard-inadmissible -> do not spend benchmark budget on this seam.
- NONTRIVIAL_HEADROOM: >=5% and <25% -> retain seam; next run outcome-blind association against existing AgentSquare result archive if locally/publicly available.
- LARGE_HEADROOM: >=25% -> retain seam and first test whether existing high-performing configurations are disproportionately admissible before live search.

The 5%/25% bands are engineering triage thresholds for search-space leverage, not paper-effect thresholds and cannot be used later as scientific success criteria.

Forbidden in OI-AS-00:
- model/API calls;
- ALFWorld benchmark runs;
- using AgentSquare performance labels to define signatures/invariants;
- changing thresholds after seeing the scan.
