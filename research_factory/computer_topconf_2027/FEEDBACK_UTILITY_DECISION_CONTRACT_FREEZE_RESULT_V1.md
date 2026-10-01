# Feedback Utility State — Decision Contract Freeze Result V1

date: 2026-10-02
status: PASS_DECISION_CONTRACT_FROZEN__LEVEL1_HARNESS_NEXT
candidate: Feedback Utility State
formal_paper_candidate: false

## Decision

`FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1 = PASS`

The first Feedback Utility State PRECARD is now prospectively adjudicable before any checkpoint download or GPU science.

## Frozen scientific decision

Primary question:

> Does finite-horizon propagation risk + extrinsic progress jointly predict robust recurrence-continuation utility materially better than the strongest cheap target-native proxies, with nonredundant value from both coordinates?

Primary substrate:
- model: `ByteDance/Ouro-1.4B`
- revision: `574fa66cb8bf5abdc979642d01cf2b79b16bfab1`
- dataset: `allenai/ai2_arc`
- revision: `210d026faf9955653af8916fad021475a3f00453`
- config/split: `ARC-Challenge / validation`
- use entire valid validation split; no outcome-based subsampling.

Primary recurrence depths:
`t = {2,3}`

Perturbation scales:
`epsilon = {0.01, 0.03, 0.05}`

Strongest cheap rival:
- depth;
- perturbation scale;
- output entropy;
- max choice probability;
- top1-top2 choice-logit gap;
- Ouro exit gate;
- hidden norm;
- normalized hidden residual.

Frozen models:
- C
- C+R
- C+P
- C+R+P+R*P

Primary endpoint:
5-fold question-clustered out-of-fold NRMSE on robust continuation utility.

## Frozen practical margins

PASS requires:
- >=10% NRMSE reduction versus C;
- >=5% NRMSE reduction versus best single-coordinate arm;
- question-cluster bootstrap 95% lower bound >0 for both comparisons.

No threshold may be weakened after outcomes.

## Frozen identifiability rule

Before primary adjudication:
- >=200 valid questions;
- >=10% beneficial and >=10% harmful pooled units;
- both t=2 and t=3 each contain >=5% beneficial and >=5% harmful units;
- practical neutral band = +/-0.05 answer-margin units.

Failure of this headroom rule is:
`PRIMARY_DECISION_NONIDENTIFIABLE__INSUFFICIENT_MIXED_UTILITY_HEADROOM`

—not a candidate negative.

## Frozen attribution rule

The exact 2D transfer does not PASS merely because either risk or progress helps.

Joint state must beat the better of:
- C+R
- C+P

by the frozen >=5% margin with positive CI lower bound.

If a single coordinate survives but the joint does not add enough:
`TWO_COORDINATE_TRANSFER_NEGATIVE__SINGLE_COORDINATE_SIGNAL_SURVIVES`

## Frozen negative rule

A valid candidate-level CLAIM_NEGATIVE requires:
- valid measurement;
- sufficient mixed-utility headroom;
- joint fails the >=10% margin versus cheap rival;
- neither single coordinate reaches that margin with positive CI lower bound.

Only then:
`CLAIM_NEGATIVE__FEEDBACK_UTILITY_STATE_NO_INCREMENTAL_VALUE`

Harness/tokenizer/download failures cannot kill the candidate.

## Execution order

1. Level-1 harness/data/tokenizer preflight.
2. Exact-weight non-primary smoke on train examples only.
3. Full frozen ARC-Challenge validation PRECARD.
4. No controller pilot in the same experiment.

Checkpoint download remains unauthorized until Level-1 PASS.

## NEXT_STEP

`FEEDBACK_UTILITY_LEVEL1_HARNESS_PREFLIGHT_V1` only.

No checkpoint download or GPU science in the same supervisor step.
