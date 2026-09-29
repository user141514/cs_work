# OI-AS-02B C2 Result

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Checkpoint: C2
Gold action: `take apple 1 from diningtable 1`

## Frozen condition

Both arms:
- GPT-5.6 Luna
- reasoning effort: medium
- Codex stdin transport
- same structured action schema
- same frozen C2 checkpoint prefix
- same frozen paired memory outputs from OI-AS-02B

## Result

| Arm | Predicted action | Exact-normalized correct |
| --- | --- | --- |
| Original TP | `take apple 1` | false |
| OI-TP | `take apple 1` | false |

Checkpoint verdict: **TIE_BOTH_WRONG**

Paired difference (OI - Original): **0**

The gold action includes the source receptacle:
`take apple 1 from diningtable 1`.

The pre-registered scorer gives no fuzzy/semantic partial credit, so both predictions remain incorrect.

## Usage

Original:
- input_tokens: 19552
- output_tokens: 52
- reasoning_output_tokens: 32
- elapsed_seconds: 132.10

OI-TP:
- input_tokens: 19590
- output_tokens: 41
- reasoning_output_tokens: 21
- elapsed_seconds: 132.10

## Cumulative pilot state after C1-C2

- Original exact correct: 1 / 2
- OI-TP exact correct: 1 / 2
- cumulative paired difference: 0

No directional claim is supported.

## Exactly one next step — not executed

C3 only:
- gold action: `go to microwave 1`
- same frozen memory outputs;
- same ReasoningIO action template;
- same GPT-5.6 Luna / medium condition;
- same exact-normalized scoring.

C4-C5 remain unexecuted.
