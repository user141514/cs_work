# OI-AS-02B C1 Result

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Checkpoint: C1
Gold action: `open fridge 1`

## Frozen model condition

Both arms:
- GPT-5.6 Luna
- reasoning effort: medium
- Codex stdin transport
- same action schema
- same frozen C1 checkpoint prefix
- memory output frozen from the paired OI-AS-02B memory-transform step

## Result

| Arm | Predicted action | Exact-normalized correct |
| --- | --- | --- |
| Original TP | `open fridge 1` | true |
| OI-TP | `open fridge 1` | true |

Checkpoint verdict: **TIE_BOTH_CORRECT**

Paired difference (OI - Original): **0**

## Usage

Original:
- input_tokens: 19388
- output_tokens: 52
- reasoning_output_tokens: 32
- elapsed_seconds: 139.23

OI-TP:
- input_tokens: 19426
- output_tokens: 51
- reasoning_output_tokens: 31
- elapsed_seconds: 141.23

## Interpretation

C1 provides no discriminating evidence between Original TP and OI-TP. It is neither supportive nor contradictory for the O+I hypothesis.

No prompt, normalization rule, gold action or model condition is changed in response.

## Exactly one next step — not executed

C2 only:
- gold action: `take apple 1 from diningtable 1`
- same frozen memory outputs;
- same ReasoningIO action template;
- same GPT-5.6 Luna / medium condition;
- same exact-normalized scoring.

C3-C5 remain unexecuted.
