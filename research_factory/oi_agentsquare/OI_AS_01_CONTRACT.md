# OI-AS-01 — Outcome-Blind Module-Level Association

Date: 2026-09-29
Baseline: AgentSquare upstream commit 8f5b3fe5d8a32f9b59d20370823bef2a2c86928c
Status: CURRENT_STEP
Depends on: OI-AS-00 NONTRIVIAL_HEADROOM

## Question

The OI-AS-00 hard gate flags MemoryTP because upstream code lets a nominal memory module generate plans/strategy for the ongoing task (PLAN_CONTROL), violating the frozen memory boundary.

Before any live combination benchmark, do the upstream per-module performance labels at least point in the same direction?

## Frozen population

Primary population: non-None memory modules only:
- DILU
- Generative
- TP
- Voyager

Do not include None in the primary rank because it is absence of a memory module rather than a competing memory mechanism.

## Frozen exposure

Hard O+I violation:
- TP = exposed / violating
- DILU, Generative, Voyager = unexposed / admissible

This mapping was fixed from source behavior before reading/using the performance labels for this experiment.

## Outcomes

Use the exact performance field shipped in frozen memory_modules.json.

Report:
- each module value;
- rank of TP among the four non-None memory modules;
- TP minus admissible mean;
- TP minus admissible median;
- exact one-sided random-rank probability that one predesignated module is the minimum among four under exchangeability (= 1/4 if uniquely minimum);
- sensitivity including None as a descriptive-only row.

## Decision

This is a tiny-n directional screen, not proof.

- CONTRADICTORY: TP is not below the admissible median -> deprioritize the hard memory-boundary seam before live benchmark.
- DIRECTIONALLY_CONSISTENT: TP is below all admissible memories -> retain seam for one minimal controlled combination experiment.
- INCONCLUSIVE: any tie/missing/non-comparable label issue -> do not infer direction.

No p<0.05 criterion; no statistical-significance claim.

## Forbidden

- no model/API/benchmark run;
- no threshold changes after seeing values;
- no use of planning/reasoning labels to redefine the exposure;
- no claim that module-level labels establish combination-level causal benefit.
