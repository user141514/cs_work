# OI-AS-02B C4 Result

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Checkpoint: C4
Gold action: `heat apple 1 with microwave 1`

## Frozen condition

Both arms:
- GPT-5.6 Luna
- reasoning effort: medium
- Codex stdin transport
- same structured action schema
- same frozen C4 checkpoint prefix
- same frozen paired memory outputs from OI-AS-02B

## Result

| Arm | Predicted action | Exact-normalized correct |
| --- | --- | --- |
| Original TP | `open microwave 1` | false |
| OI-TP | `open microwave 1` | false |

Checkpoint verdict: **TIE_BOTH_WRONG**

Paired difference (OI - Original): **0**

The frozen AgentSquare trajectory gold directly heats the apple while the microwave observation says it is closed. Both Luna/Medium arms instead chose `open microwave 1`. The pre-registered exact scorer is unchanged; the apparently reasonable shared deviation receives no post-hoc credit.

## Usage

Original:
- input_tokens: 19255
- output_tokens: 93
- reasoning_output_tokens: 73
- elapsed_seconds: 138.78

OI-TP:
- input_tokens: 19293
- output_tokens: 38
- reasoning_output_tokens: 18
- elapsed_seconds: 125.82

## Cumulative pilot state after C1-C4

- Original exact correct: 2 / 4
- OI-TP exact correct: 2 / 4
- cumulative paired difference: 0
- all four paired checkpoint differences so far: 0

No directional claim is supported.

## Exactly one next step — not executed

C5 only:
- gold action: `put apple 1 in/on fridge 1`
- same frozen memory outputs;
- same ReasoningIO action template;
- same GPT-5.6 Luna / medium condition;
- same exact-normalized scoring.
