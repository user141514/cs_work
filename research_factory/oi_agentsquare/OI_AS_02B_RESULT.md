# OI-AS-02B Result — Frozen Checkpoint Performance Pilot

Date: 2026-09-29
Status: COMPLETED_NULL_ON_PILOT
Parent: OI-AS-02
Model condition: GPT-5.6 Luna / medium / Codex

## Primary result

| Checkpoint | Gold | Original TP | OI-TP | Pair |
| --- | --- | --- | --- | --- |
| C1 | open fridge 1 | correct | correct | tie |
| C2 | take apple 1 from diningtable 1 | wrong | wrong | tie |
| C3 | go to microwave 1 | correct | correct | tie |
| C4 | heat apple 1 with microwave 1 | wrong | wrong | tie |
| C5 | put apple 1 in/on fridge 1 | wrong | wrong | tie |

Exact-normalized score:
- Original TP: **2 / 5**
- OI-TP: **2 / 5**
- paired difference sum: **0**
- discordant pairs: **0 / 5**

Decision under the pre-registered contract: **NULL_ON_PILOT**.

## Cost / process

Action calls only:
- Original input tokens: 97,499
- OI input tokens: 97,689
- Original output tokens: 323
- OI output tokens: 214
- Original reasoning tokens: 218
- OI reasoning tokens: 109
- Original summed wall time: 672.93 s
- OI summed wall time: 655.95 s

Memory transform:
- Original input tokens: 19,986
- OI input tokens: 19,980
- Original output tokens: 164
- OI output tokens: 231

These are descriptive; no efficiency claim is supported.

## What this validly says

On this one frozen same-task heat trajectory, replacing TP's current-task-plan output with bounded memory guidance changed the memory representation but did **not** change the predicted next action at any of five frozen checkpoints.

The checkpoint probe therefore provides no ranking evidence between Original TP and OI-TP.

## Why this does NOT kill the O+I hypothesis

This run is a proxy/checkpoint probe, not a full METHOD_PILOT.

More importantly, the frozen fixture's planner-owned macro structure is:

1. Find and take the apple.
2. Heat the apple with microwave 1.
3. Put the heated apple in/on fridge 1.

The Original TP memory transform independently returned essentially the same macro structure:

- find apple;
- take apple;
- heat in microwave;
- put in fridge.

Thus the adverse condition motivating the invariant — competing modules issuing materially conflicting current-task plans — was not obviously activated in this fixture.

Under the kill-scope invariant, a null result from a compatible-plan proxy cannot be promoted into a candidate-level kill.

## Unsupported

No evidence yet that:
- O+I improves full ALFWorld success;
- O+I improves search efficiency;
- O+I helps when planner and memory plans actually conflict;
- O+I generalizes across tasks;
- O+I is publication-ready.

## Exactly one next step — not executed

OI-AS-02C: **conflict-presence gate**.

Before any further downstream task calls, run the actual frozen PlanningIO path under the same Luna/medium condition for the same target task and compare its generated current-task plan against Original TP's frozen memory plan using a pre-registered structural conflict criterion.

Decision:
- if the two plans are materially aligned, mark OI-AS-02B as `NO_CONFLICT_EXPOSURE` and stop using this fixture to test the mechanism;
- if they materially conflict, then the zero-discordance checkpoint result becomes stronger evidence against the current intervention.

Do not choose a new fixture or launch another task until this conflict-presence gate is evaluated.
