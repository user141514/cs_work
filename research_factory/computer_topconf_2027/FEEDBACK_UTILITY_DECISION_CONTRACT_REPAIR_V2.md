# Feedback Utility State — Decision Contract Repair V2

date: 2026-10-02
status: REPAIRED_INDEX_MAPPING__FROZEN_BEFORE_LEVEL1_HOOK_PREFLIGHT
candidate: Feedback Utility State
lifecycle_stage: PRECARD_LEVERAGE
formal_paper_candidate: false
parent:
- FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1.md/json
- FEEDBACK_UTILITY_LEVEL1_HARNESS_PREFLIGHT_V1.md/json
- FEEDBACK_UTILITY_LEVEL1_DATA_RECEIPT_V1.json
- DECISION_CONTRACT_GATE_V1.md
- EXECUTION_LEVERAGE_GATE_V1.md

## V2 repair boundary

V1 remains immutable historical authority.

V2 repairs one pre-science defect only:

- scientific recurrence depth is explicitly 1-based: `d in {2,3}`;
- Ouro runtime/list index is explicitly 0-based: `u = d - 1`;
- `hidden_states_list[u]` and `exit_at_step=u` refer to scientific depth d.

All other scientific terms are frozen unchanged from V1:
- model/dataset revisions;
- full validation population;
- epsilon set;
- deterministic fold/seed rules;
- cheap-rival features;
- nested model classes and lambda;
- headroom thresholds;
- 10% / 5% practical margins;
- bootstrap rule;
- verdict/kill scope;
- execution-cost ceiling.

No post-outcome scientific evidence exists; this is a prospective measurement repair.

## 0. Decision owned by this contract

This contract owns exactly one necessary-condition decision:

> On one frozen looped language model and one frozen objective task population, does the two-coordinate oracle Feedback Utility State — finite-horizon propagation risk plus extrinsic progress — contain materially more information about robust continuation utility than the strongest cheap target-native proxies, with nonredundant value from both coordinates?

This is a PRECARD discriminator.

It is **not**:
- a deployable controller evaluation;
- a learned feedback-risk estimator;
- a PAPER_CANDIDATE method result;
- a cross-model generality claim.

A PASS only establishes that the transferred two-coordinate state has enough local decision headroom to justify a later estimator/controller pilot.

## 1. CLAIM

### Exact claim

For recurrent inference state at 1-based scientific UT depth (d), define:

- **Propagation Risk (R)**:
  susceptibility of the carried recurrent hidden state to a bounded perturbation, measured by how strongly that perturbation propagates through the remaining recurrent steps.

- **Extrinsic Progress (P)**:
  task-relevant progress contributed by the current recurrence beyond the prior recurrent state.

The claim is:

> A joint state built from (R) and (P) predicts robust utility of continuing recurrence better than cheap native proxies, and both coordinates contribute nonredundant predictive value.

### Positive supports

A PASS supports:
- the ancestry-derived two-coordinate research object;
- paying for a later method/estimator admission review;
- keeping feedback-topology control (continue/damp/isolate/stop) scientifically alive.

### Negative falsifies

A valid CLAIM_NEGATIVE falsifies only:
- Feedback Utility State as the current two-coordinate top-conference bet on this primary Ouro/ARC substrate.

It does not falsify:
- recurrent inference;
- adaptive exit generally;
- all stability diagnostics;
- all iterative generative feedback research.

## 2. Frozen asset identities

### Model

Repository:
`ByteDance/Ouro-1.4B`

Revision:
`574fa66cb8bf5abdc979642d01cf2b79b16bfab1`

Small-file receipts at that revision:
- README.md SHA256:
  `b819245a8c6036917de6eeb2468f515619dfe25a00f5ecc01eae08dea9118bec`
- config.json SHA256:
  `ce9cc13da41591b8b4deca053d7dfee06424c0228628ee862ea86d725bc163f3`
- modeling_ouro.py SHA256:
  `c5c68fbb368ce2909c257ae2afc50719be8c91539333d3295e19312c4316f413`

Relevant frozen architecture:
- hidden_size = 2048
- total_ut_steps = 4
- recurrent loop explicitly returns `hidden_states_list`
- each step exposes an early-exit gate in `gate_list`
- `exit_at_step` is supported
- each step's hidden state can be passed through the same `lm_head`

### Primary task population

Dataset:
`allenai/ai2_arc`

Revision:
`210d026faf9955653af8916fad021475a3f00453`

Config:
`ARC-Challenge`

Split:
`validation`

Population rule:
- use the **entire valid validation split**;
- no outcome-based subsampling;
- exclude an example only for deterministic parse/tokenizer incompatibility documented before any scientific metric is computed.

Minimum valid-question count:
`N >= 200`

If fewer than 200 valid questions remain:
`PRIMARY_DECISION_NONIDENTIFIABLE__INSUFFICIENT_POPULATION`.

## 3. Frozen prompt / answer scoring

For each ARC question, preserve the original choice order but relabel choices canonically:

`A, B, C, D, E, ...`

Prompt:

```
Question: {question}
Choices:
A. {choice_0}
B. {choice_1}
...
Answer:
```

Map the ground-truth answer to the canonical label by choice index.

Primary answer score at 1-based scientific recurrent depth (d):

`M_d = logit(correct canonical label) - max logit(incorrect canonical labels)`

using the logits obtained by applying the frozen model's `lm_head` to the last prompt-token hidden state for that recurrent step.

### Tokenizer compatibility

Before scientific execution:
- every canonical label used by the population, when represented as the exact answer token after `Answer:`, must map to one deterministic single token under the frozen tokenizer.

If not:
- stop before scientific metrics;
- verdict = `REPAIR_NEGATIVE__ANSWER_SCORING_INCOMPATIBLE`;
- a V2 contract is required before any rerun.

Do not silently change to option-text scoring after seeing outcomes.

## 4. Scientific units

Primary recurrence depths:

`d in {2, 3}`

Reason:
- P_d requires an actual prior recurrent state;
- both depths leave at least one future recurrent step.

Indexing convention:
- scientific depth `d` is 1-based;
- Ouro runtime/list index `u` is 0-based;
- `u = d - 1`;
- `h_d = hidden_states_list[d-1]`;
- `exit_at_step=d-1` selects scientific depth d.

Perturbation scales:

`epsilon in {0.01, 0.03, 0.05}`

relative to the RMS magnitude of the last-token hidden state.

For each ((question, d, epsilon)):
- create one deterministic Rademacher vector (v) from SHA256(question_id || d);
- evaluate the symmetric pair (+delta, -delta);
- `delta = epsilon * RMS(h_d[last]) * v`.

All units from the same question stay in the same train/test fold and bootstrap cluster.

## 5. Perturbation hook / measurement semantics

The exact Ouro recurrence loop normalizes `hidden_states` after each UT step and then reuses that tensor as input to the next UT step.

For a perturbed arm at scientific depth (d):

1. run scientific depths 1 through d normally;
2. record `h_d = hidden_states_list[d-1]`, the gate at runtime index `d-1`, and answer score `M_d`;
3. add (+delta) or (-delta) **only to the last-token vector of `h_d` after depth-d normalization and before scientific depth d+1 begins**;
4. continue scientific depths `d+1 ... 4` unchanged;
5. record later scientific-depth hidden states and depth-4 answer margin.

Runtime mapping during instrumentation:
- scientific depth d corresponds to runtime/list index `u=d-1`;
- the first affected decoder pass after the perturbation is runtime UT index `u=d`, i.e. scientific depth `d+1`.

No weight updates.

### Harness validity invariants

Before primary science:
- epsilon=0 instrumented execution must reproduce uninstrumented step logits/margins within absolute tolerance `1e-5`;
- applying `lm_head` to recorded `hidden_states_list[d-1]` must reproduce the corresponding `exit_at_step=d-1` logits within `1e-5`;
- symmetric perturbation runs must leave all weights/configuration unchanged.

Failure:
`REPAIR_NEGATIVE__PERTURBATION_HARNESS_INVALID`.

No scientific candidate conclusion may be drawn from a harness-invalid run.

## 6. Frozen coordinates and target

### 6.1 Propagation Risk R

For each symmetric perturbation direction, track the last-token hidden-state deviation from the unperturbed run over all remaining recurrent steps.

`gain_s = ||h_s^delta - h_s||_2 / ||delta||_2`

for 1-based scientific depth (s > d), using runtime/list index `s-1`.

Direction-level finite-horizon gain:

`R_dir = max_{s=d+1..4} gain_s`

Primary (R):

`R = median(R_+delta, R_-delta)`

This is label-free.

### 6.2 Extrinsic Progress P

Oracle task-progress coordinate:

`P = M_d - M_{d-1}`

This is label-aware and is allowed here because this PRECARD tests whether the **state exists**, not whether a deployable estimator already exists.

A later method pilot must estimate progress without access to ground-truth labels.

### 6.3 Primary target Y — robust continuation utility

For each perturbation sign:

`Y_dir = M_4^delta - M_d`

Primary target:

`Y = median(Y_+delta, Y_-delta)`

Interpretation:
- (Y > 0): under the bounded carried-state perturbation, continuing to scientific depth 4 is better than exiting at depth d;
- (Y < 0): exiting at scientific depth d would have produced a better answer margin.

This target is not used as an input feature.

## 7. STRONGEST_CHEAP_RIVAL

All models receive:
- perturbation scale epsilon as an experimental-condition covariate;
- 1-based scientific recurrence depth d.

The frozen cheap target-native feature set (C):

1. current canonical-choice entropy;
2. current maximum canonical-choice probability;
3. current top1-top2 choice-logit gap;
4. Ouro early-exit gate at runtime index `d-1` (scientific depth d);
5. current last-token hidden-state norm;
6. normalized hidden residual:
   `||h_d - h_{d-1}||_2 / (||h_{d-1}||_2 + 1e-12)`.

No ground-truth answer label enters (C).

This is the strongest cheap rival for the first PRECARD.

## 8. MECHANISM_CONTROL / ablations

Freeze four nested predictive models:

- `C`: cheap rival only.
- `C+R`: propagation risk only beyond cheap rival.
- `C+P`: extrinsic progress only beyond cheap rival.
- `C+R+P+R*P`: full two-coordinate state.

Model class:
fixed L2-regularized linear regression after train-fold standardization.

L2 penalty:
`lambda = 1.0`

No hyperparameter tuning.

The interaction (R*P) is included only in the full joint model.

A secondary report may compare the joint model to `C+R+P` without interaction, but interaction significance is not required for PASS.

## 9. Evaluation protocol

Five-fold cross-validation.

Fold assignment:
`SHA256(question_id) mod 5`.

All depths/scales/perturbation signs derived from one question remain in that question's fold.

Primary error:
`NRMSE = RMSE / SD(Y)`
computed out-of-fold across all primary units.

Primary practical improvement relative to model A:

`I(A -> B) = (NRMSE_A - NRMSE_B) / NRMSE_A`.

Uncertainty:
question-cluster bootstrap, 2000 resamples, fixed seed `20261002`.

Report 95% percentile confidence intervals.

Secondary descriptive endpoint:
binary sign prediction for (Y > 0) versus (Y < 0), using fixed L2 logistic models with the same feature sets, only when both classes satisfy the headroom rule below.

Secondary metrics cannot rescue a failed primary endpoint.

## 10. HEADROOM / mechanism-exposure precheck

Define a practical neutral band:

`tau = 0.05` answer-margin units.

A primary unit is:
- beneficial if `Y >= +0.05`;
- harmful if `Y <= -0.05`;
- idle/near-neutral otherwise.

The full primary decision is identifiable only if:

1. valid questions >= 200;
2. pooled primary units contain:
   - >=10% beneficial;
   - >=10% harmful;
3. each 1-based scientific recurrence depth (d=2) and (d=3) contains:
   - >=5% beneficial;
   - >=5% harmful.

If these fail:

`PRIMARY_DECISION_NONIDENTIFIABLE__INSUFFICIENT_MIXED_UTILITY_HEADROOM`

Stop.
Do not reinterpret lack of headroom as candidate falsification.

## 11. VALUE_ESTIMAND_AND_PASS_PREDICATE

### Primary meaningful margin versus strongest cheap rival

The joint model must satisfy:

`NRMSE_joint <= 0.90 * NRMSE_C`

equivalently:
>=10% NRMSE reduction versus (C).

And the question-cluster bootstrap 95% CI for the improvement must have lower bound > 0.

### Nonredundancy of both coordinates

Let:

`best_single = min(NRMSE_C+R, NRMSE_C+P)`.

Require:

`NRMSE_joint <= 0.95 * best_single`

equivalently:
>=5% NRMSE reduction versus the best single-coordinate arm.

And its 95% cluster-bootstrap improvement CI must have lower bound > 0.

### PASS

`PRECARD_PASS__TWO_COORDINATE_FEEDBACK_UTILITY_STATE`

only if:
- measurement/harness valid;
- mixed-utility headroom passes;
- >=10% improvement versus cheap rival with CI lower >0;
- >=5% improvement versus best single-coordinate arm with CI lower >0.

A PASS authorizes:
`PAPER_CANDIDATE_ADMISSION_REVIEW`
—not automatic method implementation.

## 12. Alternative valid outcomes

### SINGLE_COORDINATE_ONLY

If either `C+R` or `C+P` achieves >=10% meaningful improvement versus (C) with CI lower >0, but the joint model fails the >=5% nonredundancy margin versus the best single:

`TWO_COORDINATE_TRANSFER_NEGATIVE__SINGLE_COORDINATE_SIGNAL_SURVIVES`

Consequence:
- close Feedback Utility State as the 2D object;
- return the surviving coordinate only to the higher-level selector/watchlist;
- do not call this a two-coordinate PASS.

### CLAIM_NEGATIVE

If measurement/headroom are valid but:
- the joint model fails the >=10% meaningful margin versus (C), and
- neither single coordinate reaches that >=10% margin with CI lower >0,

then:

`CLAIM_NEGATIVE__FEEDBACK_UTILITY_STATE_NO_INCREMENTAL_VALUE`

Consequence:
- close the current Feedback Utility State top-conference bet;
- return to higher-level selector;
- no controller/method pilot.

### REPAIR_NEGATIVE

Instrumentation/scoring incompatibility before primary metrics:
- tokenizer label incompatibility;
- epsilon=0 mismatch;
- hidden-state/exit-at-step mismatch;
- perturbation hook invalid.

These are repair negatives only.
They do not kill the candidate.

### ASSET / EXECUTION BLOCKER

Download/runtime failure:
operational blocker only.

No scientific verdict.

## 13. Counterexample audit

### PASS_WITHOUT_VALUE

Blocked by:
- strongest cheap rival (C);
- explicit >=10% practical margin;
- CI lower-bound requirement.

### WIN_WITHOUT_ATTRIBUTION

Blocked by:
- `C+R`;
- `C+P`;
- full joint;
- explicit >=5% joint-over-best-single requirement.

### FAIL_WITHOUT_IDENTIFICATION

Blocked by:
- minimum valid population;
- mixed beneficial/harmful headroom rule;
- harness validity checks.

### Label leakage

The oracle (P) coordinate is deliberately label-aware for state-existence testing.

Therefore a PASS does **not** claim deployability.

Any later method must estimate (P) without label access and own a new Decision Contract.

## 14. EXECUTION_LEVERAGE

Scientific execution level:
Level 2 — small-model inference-only.

Lower levels already exhausted:
- ancestry transfer;
- bounded direct-prior attack;
- G0 public asset/interface/resource preflight.

Why Level 0/1 cannot decide the claim:
the owned decision requires actual recurrent hidden states, perturbation propagation and task-conditioned recurrence utility under the trained Ouro weights.

Level 1 is still required for harness admission before Level 2.

No model/API training.

No LoRA.

No benchmark expansion.

## 15. Frozen execution order

1. `FEEDBACK_UTILITY_LEVEL1_HOOK_PREFLIGHT_V2`
   - reuse the PASSed V1 tokenizer/data/manifest receipt unchanged;
   - run only the remaining perturbation-hook validation on exact Ouro code with reduced/random weights or equivalent non-scientific fixture;
   - verify the repaired `d -> d-1` mapping, epsilon=0 identity, recorded-hidden vs `exit_at_step=d-1` identity, and +/-delta path;
   - no Ouro checkpoint required unless strictly necessary for compatibility.

2. If Level-1 PASS:
   - materialize exact Ouro checkpoint revision;
   - run a small **non-primary** smoke using ARC-Challenge train examples only;
   - verify epsilon=0 and fixed-step invariants on exact weights.

3. If exact-weight smoke PASS:
   - execute the frozen full ARC-Challenge validation PRECARD.

4. Stop immediately on:
   - population/headroom nonidentifiability;
   - harness repair negative;
   - valid CLAIM_NEGATIVE.

Do not run a controller pilot in the same experiment.

## 16. Full cost accounting

Primary PRECARD must record:
- checkpoint/data download bytes;
- GPU wall time;
- peak VRAM;
- number of base and perturbation forwards;
- CPU analysis time;
- any harness engineering/retries.

No API model calls are required.

If the exact-weight smoke projects >2.5 GPU-hours for the frozen primary run:
- stop before full primary execution;
- return to Execution Leverage;
- do not silently reduce the primary population after seeing timing or partial outcomes.

## 17. Frozen next step

`FEEDBACK_UTILITY_LEVEL1_HOOK_PREFLIGHT_V2` only.

Do not:
- rerun or alter the already-PASSed V1 tokenizer/data manifest;
- download the full Ouro checkpoint before Level-1 V2 admission;
- run ARC-Challenge validation science;
- tune thresholds/features after seeing scientific outcomes;
- activate N3 or BET-COMP-02;
- reopen BFSC.
