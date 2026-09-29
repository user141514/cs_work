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
- examine: ACQUIRE(object) -> FIND_USE(desklamp)
- puttwo: ACQUIRE(first object) -> PLACE(first,destination) -> ACQUIRE(second object) -> PLACE(second,destination)

## Stop rule

- If any material conflict appears, STOP the prevalence screen immediately. That first deterministic conflict case becomes the only candidate for a downstream OI-TP-vs-Original mechanism test.
- If all remaining targets complete with zero material conflicts, TERMINATE the `MemoryTP-plan-conflict` seam.

## First target completed

`react_cool_1` paired with `react_cool_0` completed `NO_CONFLICT_EXPOSURE` under the frozen rule.

## Completed targets

- `react_cool_1` paired with `react_cool_0`: `NO_CONFLICT_EXPOSURE`.
- `react_examine_1` paired with `react_examine_0`: `NO_CONFLICT_EXPOSURE`.

## Current target frozen before outputs

Current target: `react_heat_2` — `heat some bread and put it in countertop`.
Paired memory: `react_heat_0` — `heat some egg and put it in diningtable`.
Jaccard: `0.5`.
Required signature: `ACQUIRE(bread) -> HEAT(bread,microwave) -> PLACE(bread,countertop)`.
For this target, omission/replacement of HEAT, heating the wrong object, placing before heating, or using a final destination other than countertop is material conflict. Search-location details, optional open/close actions, and specific countertop index choice are not.

## Current execution bound

This continuation executes only `react_heat_2`. `react_put_1` and `react_puttwo_1` remain unexecuted.

### Examine-family correction before `react_examine_1` execution

The original generic line incorrectly listed an extra terminal `EXAMINE(object,desklamp)` macro. Frozen AgentSquare `planning_prompt['examine']` and the frozen successful `react_examine_*` trajectories both terminate by finding and using the desklamp while holding the target object; there is no separate planner-owned EXAMINE subtask/action. Before any `react_examine_1` model output, the required family signature is therefore corrected to `ACQUIRE(object) -> FIND_USE(desklamp)`. This correction does not affect the already-completed clean/cool gates.
