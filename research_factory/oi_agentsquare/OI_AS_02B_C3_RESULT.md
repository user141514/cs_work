# OI-AS-02B C3 Result

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Checkpoint: C3
Gold action: `go to microwave 1`

## Frozen condition

Both arms:
- GPT-5.6 Luna
- reasoning effort: medium
- Codex stdin transport
- same structured action schema
- same frozen C3 checkpoint prefix
- same frozen paired memory outputs from OI-AS-02B

## Result

| Arm | Predicted action | Exact-normalized correct |
| --- | --- | --- |
| Original TP | `go to microwave 1` | true |
| OI-TP | `go to microwave 1` | true |

Checkpoint verdict: **TIE_BOTH_CORRECT**

Paired difference (OI - Original): **0**

## Usage

Original:
- input_tokens: 19606
- output_tokens: 45
- reasoning_output_tokens: 24
- elapsed_seconds: 132.92

OI-TP:
- input_tokens: 19644
- output_tokens: 40
- reasoning_output_tokens: 19
- elapsed_seconds: 132.92

## Cumulative pilot state after C1-C3

- Original exact correct: 2 / 3
- OI-TP exact correct: 2 / 3
- cumulative paired difference: 0

No directional claim is supported.

## Exactly one next step — not executed

C4 only:
- gold action: `heat apple 1 with microwave 1`
- same frozen memory outputs;
- same ReasoningIO action template;
- same GPT-5.6 Luna / medium condition;
- same exact-normalized scoring.

C5 remains unexecuted.
