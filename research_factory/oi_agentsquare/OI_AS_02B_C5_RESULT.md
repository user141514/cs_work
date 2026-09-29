# OI-AS-02B C5 Result

Date: 2026-09-29
Status: COMPLETED_VALID_PAIR
Checkpoint: C5
Gold action: `put apple 1 in/on fridge 1`

## Result

| Arm | Predicted action | Exact-normalized correct |
| --- | --- | --- |
| Original TP | `put apple 1 in fridge 1` | false |
| OI-TP | `put apple 1 in fridge 1` | false |

Checkpoint verdict: **TIE_BOTH_WRONG**

Paired difference (OI - Original): **0**

The scorer remains exact-normalized. The frozen gold token `in/on` is not post-hoc relaxed to `in`.

## Cumulative pilot state after C1-C5

- Original exact correct: 2 / 5
- OI-TP exact correct: 2 / 5
- cumulative paired difference: 0
- discordant checkpoint pairs: 0 / 5

OI-AS-02B is therefore complete and must be summarized as a null checkpoint pilot, not as evidence that O+I is ineffective.
