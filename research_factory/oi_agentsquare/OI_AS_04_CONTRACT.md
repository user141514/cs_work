# OI-AS-04 — MemoryTP Conflict-Prevalence Screen

Date: 2026-09-30
Status: AUTHORIZED_BY_USER_CONTINUATION

## Purpose

Complete the remaining eligible AgentSquare ALFWorld targets under the same conflict-presence gate, with a hard stop rule. This tests the narrow seam `MemoryTP-plan-conflict`; it does not test broader O+I efficacy.

## Frozen eligible set

Eligibility is inherited unchanged from OI-AS-03:
- target exists in frozen `alfworld_3prompts.json`;
- target task is not duplicated verbatim in the corresponding `planning_prompt[task_type]` few-shot.

`react_clean_1` was already screened in OI-AS-03 and is excluded from the remaining set.

Remaining targets are executed in lexicographic key order.

## Frozen memory pairing per target

For each remaining target independently:
- compare target task text to every other frozen successful task text;
- lowercase alphanumeric token sets;
- remove only stopwords: `a`, `an`, `the`, `some`, `to`, `in`, `on`;
- choose the distinct memory task with maximum set Jaccard similarity;
- ties break by memory key lexicographic order.

Pairing is frozen for the complete remaining set before any OI-AS-04 model call.

## Per-target gate

For the current target only:
1. build actual frozen PlanningIO prompt for its task type;
2. build actual Original-TP memory-transform prompt using its frozen paired memory trajectory;
3. run both with GPT-5.6 Luna / medium;
4. PlanningIO must use the clean inference-only harness with zero tool events;
5. compare ordered task-required macro signatures under the target-specific pre-registered criterion.

## Generic material-conflict criterion

A material conflict exists if the two plans disagree on any required macro phase, its ordering, state transformation, target object, required multiplicity, required inspection/light action, or final destination.

Low-level search hints, optional open/close actions, and lexical differences do not count.

Task-family required signatures:
- put: ACQUIRE(object) -> PLACE(object,destination)
- clean: ACQUIRE(object) -> CLEAN(object,sinkbasin) -> PLACE(object,destination)
- heat: ACQUIRE(object) -> HEAT(object,microwave) -> PLACE(object,destination)
- cool: ACQUIRE(object) -> COOL(object,fridge) -> PLACE(object,destination)
- examine: ACQUIRE(object) -> FIND_USE(desklamp) -> EXAMINE(object,desklamp)
- puttwo: ACQUIRE(first object) -> PLACE(first,destination) -> ACQUIRE(second object) -> PLACE(second,destination)

## Stop rule

- If any material conflict appears, STOP the prevalence screen immediately. That first deterministic conflict case becomes the only candidate for a downstream OI-TP-vs-Original mechanism test.
- If all remaining targets complete with zero material conflicts, TERMINATE the `MemoryTP-plan-conflict` seam.

## First target frozen before outputs

Current target: `react_cool_1` — `put a cool mug in shelf`.
Paired memory: `react_cool_0` — `cool some pan and put it in stoveburner`.
Jaccard: `0.25`.
Required signature: `ACQUIRE(mug) -> COOL(mug,fridge) -> PLACE(mug,shelf)`.
For this target, omission/replacement of COOL, cooling a different target object, placing before cooling, or using a final destination other than shelf is material conflict. Object-specific adaptation from pan to mug and destination adaptation from stoveburner to shelf are required.

## Current execution bound

This continuation executes only `react_cool_1` after the full pairing manifest is frozen. Later targets remain unexecuted until a subsequent continuation.
