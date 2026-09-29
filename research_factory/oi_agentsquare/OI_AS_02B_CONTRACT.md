# OI-AS-02B — Frozen Checkpoint Performance Pilot

Date: 2026-09-29
Parent: OI-AS-02
Status: AUTHORIZED_BY_USER_CONTINUATION

## Purpose

Measure whether Original TP vs OI-TP changes downstream next-action correctness on five frozen checkpoints from AgentSquare's own ALFWorld heat-task prompt trajectory.

This is a checkpoint pilot, NOT a full ALFWorld episode benchmark.

## Frozen source

- AgentSquare commit: 8f5b3fe5d8a32f9b59d20370823bef2a2c86928c
- source prompt file: upstream/runtime/prompts/alfworld_3prompts.json
- memory case: react_heat_0
- target case: react_heat_1
- fixture: OI_AS_02B_FIXTURE.json
- five checkpoints C1..C5 and gold actions are frozen before any OI-AS-02B model call.

## Arms

Original:
- Original TP memory-transform prompt from oi_as02b_prompts/memory_original.txt

OI:
- OI-TP memory-transform prompt from oi_as02b_prompts/memory_oi.txt

Both:
- one memory-transform call;
- same success case and ongoing task;
- same model/backend/effort;
- memory output then remains frozen across all five action checkpoints.

## Model condition

- Codex CLI
- GPT-5.6 Luna
- reasoning effort: medium
- stdin transport
- JSONL capture
- no web/tools/files requested from model
- same retry and timeout policy for both arms

## Reasoning checkpoint prompt

For each arm/checkpoint, use the AgentSquare ReasoningIO surface form:

Interact with a household to solve a task. Your instructions must follow the examples.
Here are some examples.
{memory_text}
Here is the task:
{checkpoint_prefix}

The checkpoint prefix is frozen verbatim from OI_AS_02B_FIXTURE.json.

The model must return structured JSON:
{"action":"<single ALFWorld action>"}

No additional planning prompt is introduced at this stage. The trajectory prefix already contains the frozen planner/reasoner history up to the checkpoint.

## Scoring

Normalize prediction and gold by:
- strip whitespace;
- remove leading ">";
- remove trailing period;
- collapse internal whitespace;
- lowercase.

Primary:
- exact normalized action match per checkpoint;
- total correct / 5 for each arm;
- paired checkpoint difference.

Secondary:
- invalid/missing structured outputs;
- token usage and wall time descriptively.

No fuzzy semantic scoring after outcomes are seen.

## Decision

- SUPPORTIVE_DIRECTION: OI-TP > Original TP correct count.
- NULL_ON_PILOT: equal correct count.
- CONTRADICTORY: OI-TP < Original TP correct count.
- INVALID: transport/output failures prevent fair paired comparison.

No significance claim at n=5.

## Boundary

This pilot only tests whether the memory-authority intervention changes next-action behavior on one frozen trajectory. It cannot establish full-episode ALFWorld success, search efficiency, generalization or publication value.
