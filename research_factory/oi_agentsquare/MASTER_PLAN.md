# O+I AgentSquare — Dynamic Master Plan

Date: 2026-09-29
Plan ID: OI-AS-20260929
Status: ACTIVE
Authority: explicit user redirection back to Orthogonality + Invariants as the scientific innovation and request to advance experiments.

## Goal

Test whether explicit responsibility orthogonality plus behavioral invariants can improve modular-agent search by rejecting structurally incompatible module compositions before AgentSquare's expensive predictor/evaluator.

Primary baseline:
- AgentSquare
- upstream commit: 8f5b3fe5d8a32f9b59d20370823bef2a2c86928c
- first task seam: ALFWorld recombination candidates -> predictor

## Scientific model

AgentSquare already standardizes module categories/interfaces, but recombination candidates are passed to the performance predictor without an explicit compatibility gate over:
1. duplicated decision authority;
2. cross-module responsibility overlap;
3. invariant violations at composition time.

Hypothesis:
A responsibility-orthogonality prior plus invariant gate can remove harmful compositions and/or improve search efficiency without reducing attainable task quality.

## Evidence sequence

1. OI-AS-00: static outcome-blind headroom scan of frozen module space.
2. OI-AS-01: tiny-n outcome-blind directional association using shipped per-module labels.
3. OI-AS-02: one controlled combination intervention isolating the strongest frozen invariant (memory boundary).
4. Only if OI-AS-02 supports the hypothesis: integrate gate before AgentSquare predictor and run paired search.
5. Only then consider broader tasks/ablations.

## Completed

### OI-AS-00
Status: COMPLETED_NONTRIVIAL_HEADROOM

Frozen ALFWorld executable static denominator:
- planning: 6
- reasoning: 7
- tooluse: None only (upstream search filters non-None tooluse)
- memory: 5
- total: 210

Result:
- hard-inadmissible: 42 / 210 = 20%
- soft-coupled: 182 / 210 = 86.67%
- dominant hard exposure: MemoryTP owns current-task PLAN_CONTROL despite being a memory module.
- triage: NONTRIVIAL_HEADROOM

This proves structural leverage exists, not performance benefit.

## CURRENT_STEP

ID: OI-AS-01
Status: COMPLETED_DIRECTIONALLY_CONSISTENT
Result authority: OI_AS_01_RESULT.md and OI_AS_01_RESULT.json.

Observed:
- TP = 0.36;
- admissible non-None memories = Generative 0.64, DILU 0.74, Voyager 0.78;
- TP is uniquely lowest (rank 4/4);
- TP minus admissible mean = -0.36;
- TP minus admissible median = -0.38;
- exact one-sided random-rank probability for a predesignated unique minimum among four = 0.25.

Decision: DIRECTIONALLY_CONSISTENT, but tiny-n and non-causal. Retain the memory-boundary seam for exactly one controlled intervention; do not claim significance or combination-level benefit.

## CURRENT_STEP_2

ID: OI-AS-02
Status: AUTHORIZED_BY_USER_CONTINUATION
Model condition: GPT-5.6 Luna via local Codex CLI, reasoning effort medium, identical for both arms.

OI-AS-02A manipulation check: COMPLETED_PASS. Static behavior test confirms OI-TP preserves k=1 retrieval, empty-memory behavior, inherited storage path and one memory-side LLM call while changing only output authority. Real Luna/Medium paired prompts then produced four ordered current-task directives for Original TP and zero current-task directives for OI-TP under the frozen deterministic evaluator. Authority manipulation is operationally valid; task performance remains unmeasured.

Create one orthogonalized MemoryTP variant (OI-TP) that preserves TP retrieval/top-k/memory insertion and comparable LLM-call budget, but removes current-task PLAN_CONTROL: it returns bounded memory-derived guidance while planning remains the sole current-plan owner. Compare original TP vs OI-TP under one fixed non-None planning module, fixed reasoning, tooluse=None, same model/tasks/seeds/budget.

Acceptance: verify the intervention changes only the memory-output responsibility before running any benchmark; then measure paired task outcome and cost. If runtime dependencies/model credentials are unavailable, record NEED_INPUT rather than substituting another benchmark/model.

STOP:
OI-AS-01 is complete. OI-AS-02A manipulation validity is complete. OI-AS-02B is COMPLETE_NULL_ON_PILOT: Original TP 2/5, OI-TP 2/5, paired difference 0, discordant pairs 0/5. OI-AS-02C is COMPLETE_NO_CONFLICT_EXPOSURE on the duplicated heat target. OI-AS-03 is also COMPLETE_NO_CONFLICT_EXPOSURE on a stronger cross-task lexical-nearest stress fixture selected outcome-blind from the frozen bank: target `clean some apple and put it in sidetable`, memory `find some apple and put it in sidetable`, Jaccard 0.7143. Clean PlanningIO and Original TP both reduced to `ACQUIRE(apple) -> CLEAN(apple,sinkbasin) -> PLACE(apple,sidetable)`; Original TP inserted the target-required CLEAN phase despite the misleading memory task. This weakens the narrow `MemoryTP-plan-conflict` mechanism assumption but does not kill broader O+I. Result authority: `OI_AS_03_RESULT.md` and `OI_AS_03_RESULT.json`. OI-AS-04 MemoryTP conflict-prevalence screen is ACTIVE under the hard stop rule and the complete pairing manifest remains frozen. `react_cool_1`, `react_examine_1`, `react_heat_2`, and `react_put_1` have each completed NO_CONFLICT_EXPOSURE. For `react_put_1` with frozen memory `react_clean_1`, clean PlanningIO and Original TP both reduce to `ACQUIRE(apple) -> PLACE(apple,sidetable)`; Original TP did not import the source memory task's CLEAN transformation. Across screened eligible targets so far (`react_clean_1`, `react_cool_1`, `react_examine_1`, `react_heat_2`, `react_put_1`), material conflicts = 0/5. Result authority: `OI_AS_04_PUT1_RESULT.md` and `oi_as04/react_put_1/RESULT.json`. Exactly one next step is the final target `react_puttwo_1` with frozen memory `react_puttwo_0`; it is NOT_EXECUTED. If that final target also has no material conflict, the pre-registered stop rule TERMINATES the `MemoryTP-plan-conflict` seam.
