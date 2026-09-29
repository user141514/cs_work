# OI-AS-03 — Conflict-Exposed Fixture Gate

Date: 2026-09-30
Status: AUTHORIZED_BY_USER_CONTINUATION

## Goal

Find one frozen AgentSquare ALFWorld target where the memory module has a plausible opportunity to import a materially incompatible plan, then test conflict presence BEFORE any Original-vs-OI downstream comparison.

## Outcome-blind fixture selection

Source bank: frozen `upstream/runtime/prompts/alfworld_3prompts.json`.

Eligible targets:
- target task must NOT occur verbatim inside the corresponding frozen `planning_prompt[task_type]` few-shot;
- target must have a valid successful trajectory in the source bank.

Memory-case selection:
- compare the eligible target's task text to every other successful task text in the same frozen prompt bank;
- tokenize lowercase alphanumeric words;
- remove only the stopwords: `a`, `an`, `the`, `some`, `to`, `in`, `on`;
- score set Jaccard similarity = |intersection| / |union|;
- choose the target-memory ordered pair with maximum similarity;
- ties break by `(target_key, memory_key)` lexicographic order;
- memory key must differ from target key.

This is a deterministic conflict-stress retrieval proxy, NOT a claim that it reproduces OpenAIEmbeddings nearest-neighbor retrieval.

## Frozen selected pair

The deterministic selector produced:
- target: `react_clean_1` — `clean some apple and put it in sidetable`;
- target type: `clean`;
- memory: `react_put_1` — `find some apple and put it in sidetable`;
- token-set Jaccard: `0.7142857142857143`.

Target-required canonical signature, frozen before model outputs:
`ACQUIRE(apple) -> CLEAN(apple,sinkbasin) -> PLACE(apple,sidetable)`.

For this selected target, omission or replacement of `CLEAN(apple,sinkbasin)`, placing before cleaning, operating on a different object, or using a different final destination is a material conflict. Search-location details and optional open/close actions are not.

## Gate execution

For the selected pair only:
1. run the actual frozen PlanningIO prompt for the target task/type;
2. run the actual Original-TP memory-transform prompt using the selected successful memory trajectory and the same target;
3. both use GPT-5.6 Luna / medium via Codex;
4. compare their ordered task-plan signatures under a pre-registered target-specific structural criterion.

## Conflict criterion

A MATERIAL_CONFLICT exists if the two outputs disagree on any task-required macro phase, its ordering, transformation, target object, or final destination. Low-level search hints, optional open/close actions, and lexical differences do not count.

For a target requiring a state transformation (clean/heat/cool), omission or replacement of that transformation is material conflict.

## Decisions

- CONFLICT_EXPOSURE_PRESENT: material conflict is observed; this fixture becomes eligible for a downstream Original-TP vs OI-TP comparison.
- NO_CONFLICT_EXPOSURE: plans are materially aligned; reject this fixture for conflict-repair testing.
- INVALID: either output cannot be parsed sufficiently to apply the frozen criterion.

No downstream action/episode comparison is authorized inside OI-AS-03.
