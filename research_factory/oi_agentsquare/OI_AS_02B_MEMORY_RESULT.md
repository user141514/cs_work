# OI-AS-02B Memory Transform Pair

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Parent: OI-AS-02B checkpoint performance pilot

## Frozen condition

Both arms:
- Codex CLI
- GPT-5.6 Luna
- reasoning effort: medium
- stdin transport
- JSONL capture
- structured schema
- one memory-transform call
- same frozen success case and target task

## Original TP

Result:
`Plan: Find an apple ... Take the apple, go to microwave 1, and heat it. Then go to fridge 1 ... put the hot apple in/on fridge 1.`

Usage:
- input_tokens: 19986
- cached_input_tokens: 0
- output_tokens: 164
- reasoning_output_tokens: 73
- elapsed_seconds: 129.10

Interpretation:
Original TP operationally owns current-task planning.

## OI-TP

Result:
five bounded guidance/constraint items:
- preserve target identity;
- preserve hot-state constraint;
- search plausible receptacles systematically;
- verify final fridge containment relation;
- use accepted environment interactions / open closed appliance when needed.

Usage:
- input_tokens: 19980
- cached_input_tokens: 0
- output_tokens: 231
- reasoning_output_tokens: 93
- elapsed_seconds: 138.07

Interpretation:
OI-TP preserves useful memory-derived information without producing the current task's ordered plan.

## Validity

VALID_PAIR.

The intervention manipulation established in OI-AS-02A remains active on the real frozen AgentSquare fixture.

This is not yet a task-performance result.

## Exactly one next step

Run checkpoint C1 only:
- gold action: `open fridge 1`
- same frozen checkpoint prefix;
- inject frozen Original / OI memory outputs into the same ReasoningIO prompt template;
- GPT-5.6 Luna / medium;
- structured single-action output;
- exact normalized scoring fixed by OI_AS_02B_CONTRACT.md.

Do not execute C2-C5 until C1 is collected and validated.
