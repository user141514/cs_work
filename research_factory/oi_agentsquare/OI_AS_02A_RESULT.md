# OI-AS-02A Result — Luna/Medium Manipulation Check

Date: 2026-09-29
Parent: OI-AS-02
Status: COMPLETED_MANIPULATION_PASS

## Frozen condition

Both valid arms used:
- Codex CLI
- GPT-5.6 Luna
- reasoning effort: medium
- stdin prompt transport
- JSONL event capture
- one model call per arm

The earlier multiline command-line Original-TP attempt is retained separately as INVALID_TRANSPORT and is excluded from scientific interpretation.

## Original TP

Final response contains four ordered current-task action directives:

1. Check the fridge for a potato.
2. If none, search the countertop and take the potato.
3. Go to the microwave and heat the potato.
4. Go to the dining table and place the heated potato on it.

Frozen manipulation endpoint: PASS.

Usage from Codex JSONL:
- input_tokens: 18803
- cached_input_tokens: 8960
- output_tokens: 75
- reasoning_output_tokens: 17

## OI-TP

Final response contains:
- useful prior facts/patterns;
- one explicitly historical "successful interaction pattern";
- constraints/pitfalls for the planner/reasoner.

It contains no ordered CURRENT-TASK action directives under the pre-registered rule and does not claim to be a plan/subgoal/to-do list.

Frozen manipulation endpoint: PASS.

Usage:
- input_tokens: 19177
- cached_input_tokens: 18176
- output_tokens: 181
- reasoning_output_tokens: 66

## Paired result

PAIRED_MANIPULATION_PASS = true.

Supported:
- the same Luna/Medium model responds differently in the intended authority dimension;
- Original TP operationally generates a current-task plan;
- OI-TP can retain transferable sequential memory information while avoiding ownership of the current-task plan.

Not supported:
- no ALFWorld performance benefit has been measured;
- token usage is not equal because the intervention prompt/output is longer;
- no claim that OI-TP is cheaper;
- no task-success claim.

## Boundary revealed

The invariant is about decision authority, not information erasure. OI-TP is allowed to expose a prior successful sequence as memory evidence. It is forbidden to convert that evidence into the current task's authoritative plan.

This distinction is now operationally testable.

## Next smallest step — not executed

Before full ALFWorld:
- freeze fixed PlanningIO + ReasoningIO + tooluse=None;
- decide the cheapest task-performance pilot that keeps the Original-TP vs OI-TP authority intervention active;
- explicitly account for AgentSquare's OpenAIEmbeddings/Chroma dependency and Codex-per-call overhead without silently changing the primary ALFWorld endpoint.

Do not install a large runtime or replace ALFWorld with a proxy under the same run ID without a new pre-registered sub-run.
