# OI-AS-03 Result — Lexical-Nearest Conflict Gate

Date: 2026-09-30
Status: COMPLETED_NO_CONFLICT_EXPOSURE

## Deterministic fixture selection

From frozen AgentSquare `alfworld_3prompts.json`, eligible targets were tasks not duplicated in the corresponding PlanningIO few-shot.

The outcome-blind selector chose the maximum token-set Jaccard target-memory pair:

- target: `react_clean_1` — `clean some apple and put it in sidetable`
- memory: `react_put_1` — `find some apple and put it in sidetable`
- Jaccard: `0.7142857142857143`

This is intentionally a cross-task-type lexical-nearest stress proxy. It is not claimed to reproduce OpenAIEmbeddings retrieval.

## Frozen target-required signature

`ACQUIRE(apple) -> CLEAN(apple,sinkbasin) -> PLACE(apple,sidetable)`

## Valid PlanningIO result

The first planner attempt was excluded as `INVALID_HARNESS_CONTAMINATION` because Codex invoked a local planning skill and read skill files.

A clean rerun disabled user config/rules and the main execution/tool surfaces. Validity gate: zero tool events.

Valid clean PlanningIO:

`ACQUIRE(apple) -> CLEAN(apple,sinkbasin) -> PLACE(apple,sidetable)`

Tool events: `0`.

## Original TP result

Despite receiving a successful memory trajectory whose source task only required finding an apple and placing it on the sidetable, Original TP generated:

`ACQUIRE(apple) -> CLEAN(apple,sinkbasin) -> PLACE(apple,sidetable)`

It explicitly inserted the target-required cleaning step from the ongoing task.

## Verdict

Material conflict: **false**

Status: **NO_CONFLICT_EXPOSURE**

The first evaluator output that showed conflict was discarded as a parser bug: it mistook an incidental early mention of `sidetable` in the search-location list for a PLACE action. The corrected action-clause parser yields the aligned signature above. No model call was rerun for that correction.

## Scientific consequence

This is stronger negative evidence against the narrow mechanism assumption that MemoryTP's plan authority naturally creates macro-plan conflict with PlanningIO. It does NOT kill Orthogonality + Invariants as a broader search-space prior/gate.

## Exactly one next step — not executed

OI-AS-04: **MemoryTP conflict-prevalence screen**.

Apply the already-frozen outcome-blind target/memory selection procedure to all remaining eligible non-duplicated ALFWorld targets, using only the conflict-presence gate and no downstream OI-TP comparison.

Stop rule:
- if zero material conflicts are found across the complete eligible set, TERMINATE the `MemoryTP-plan-conflict` seam;
- if one or more conflicts are found, use the first deterministic conflict case as the only downstream mechanism test.

Status: `PLANNED_NOT_AUTHORIZED`.
