# OI-AS-01 Result — Module-Level Directional Screen

Date: 2026-09-29
Plan: OI-AS-20260929
Status: COMPLETED_DIRECTIONALLY_CONSISTENT

## Frozen question

OI-AS-00 predesignated MemoryTP as the only memory module with a hard Memory Boundary violation because upstream code makes the memory module generate a current-task plan/strategy.

Does the frozen upstream per-module performance label at least point in the same direction before we spend live benchmark budget?

## Population and exposure

Primary non-None memory population:
- DILU — admissible
- Generative — admissible
- TP — hard O+I violation
- Voyager — admissible

None (performance 0) is descriptive only and excluded from the primary rank.

## Observed labels

| Module | O+I status | Upstream performance |
| --- | --- | ---: |
| Voyager | admissible | 0.78 |
| DILU | admissible | 0.74 |
| Generative | admissible | 0.64 |
| TP | violating | 0.36 |

TP rank: 4 / 4 (unique minimum).

Admissible mean: 0.72.
TP minus admissible mean: -0.36.

Admissible median: 0.74.
TP minus admissible median: -0.38.

For one predesignated module under exchangeable random ranks, the exact one-sided probability of being uniquely minimum among four is 1/4 = 0.25.

## Decision

DIRECTIONALLY_CONSISTENT.

This does NOT establish statistical significance, causality, or combination-level benefit. It only says the first hard O+I exposure does not immediately contradict the shipped module-level outcomes and is strong enough to justify one controlled intervention.

## Next experiment design implication

Do NOT compare TP directly against a different memory algorithm such as Voyager as the main causal experiment; that changes both invariant status and the memory algorithm.

Instead, OI-AS-02 should create an orthogonalized TP variant that preserves:
- TP retrieval source and top-k behavior;
- the same retrieved trajectories;
- comparable LLM-call budget;
- the same memory insertion point;

while changing only the load-bearing violation:
- original TP: retrieved memory -> generate current-task Plan -> return plan;
- OI-TP: retrieved memory -> generate bounded non-authoritative guidance/constraints -> return guidance, leaving current-task plan ownership to the planning module.

Then compare original TP vs OI-TP under a fixed non-None planning module, fixed reasoning, fixed tooluse=None, same model/tasks/seeds/budget.

This is the first experiment that can causally test the Memory Boundary invariant rather than merely correlate module identity with performance.

## Runtime boundary

PC2 currently does not have the required AgentSquare runtime Python dependencies or OPENAI_API_KEY in the active environment. This is an execution precondition, not a negative scientific result. Do not install/rewire the environment inside OI-AS-01.

## Evidence files

- OI_AS_01_CONTRACT.md
- oi_module_label_check.py
- OI_AS_01_RESULT.json
- frozen upstream/search/memory_modules.json
