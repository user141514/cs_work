# OI-AS-00 Result — Static O+I Headroom Scan

Date: 2026-09-29
Plan: OI-AS-20260929
Status: COMPLETED_NONTRIVIAL_HEADROOM
Baseline: AgentSquare commit 8f5b3fe5d8a32f9b59d20370823bef2a2c86928c

## Executable ALFWorld denominator

Upstream `agent_search.py` filters candidates to `tooluse == None`, so the relevant static space is:

- planning: 6
- reasoning: 7
- tooluse: 1 (None)
- memory: 5
- total: 210

The 1050 full-catalog Cartesian product is diagnostic only, not the ALFWorld execution denominator.

## Frozen O+I scan result

Executable 210:
- hard-inadmissible: 42 / 210 = 20.00%
- soft-coupled: 182 / 210 = 86.67%
- verdict: NONTRIVIAL_HEADROOM

Hard conflicts:
- I3_MEMORY_BOUNDARY: 42
- I2_DECOMPOSITION_AUTHORITY: 35

The hard exposure is concentrated in MemoryTP. Upstream TP retrieves prior trajectories and then explicitly asks an LLM to generate plans/strategy for the ongoing task, so it owns current-task PLAN_CONTROL despite being a memory module.

Planning modules' reasoning/tool instructions are recorded as soft coupling rather than automatically rejected.

## Supported claim

There is enough structural headroom at the AgentSquare recombination→predictor seam to justify one further discriminating experiment.

## Unsupported claims

This scan does not show:
- performance improvement;
- causal harm from a conflict;
- search efficiency gain;
- statistical significance;
- novelty over all adjacent work.

No model/API/benchmark was run.
