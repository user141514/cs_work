# Feedback Utility State — G0 Asset / Interface Preflight V1

date: 2026-10-02
status: PASS_PUBLIC_ASSET__INTERFACE_OBSERVABLE__LOCAL_LEVEL2_FEASIBLE
candidate: Feedback Utility State
model_calls: 0
gpu_runs: 0
weights_downloaded: false

## Decision

`FEEDBACK_UTILITY_G0_ASSET_PREFLIGHT_V1 = PASS`

The exact public Ouro asset and local execution environment are sufficient to support a future bounded Level-2 inference-only discriminator.

This does not authorize the discriminator yet.
Decision Contract freeze remains mandatory first.

## 1. Public asset identity

Model:
`ByteDance/Ouro-1.4B`

Current exact public revision observed:
`574fa66cb8bf5abdc979642d01cf2b79b16bfab1`

Hub state:
- public: true
- gated: false
- disabled: false
- reported storage: 2,870,191,799 bytes

Required public files are present:
- `config.json`
- `configuration_ouro.py`
- `modeling_ouro.py`
- `model.safetensors`
- tokenizer assets
- README

License reported by public model card:
Apache-2.0.

## 2. Required recurrent-state interface

The public configuration exposes:
- `total_ut_steps = 4`
- `early_exit_threshold`

The public custom model code exposes the recurrent computation directly:
- loop over universal-transformer/recurrent steps;
- one normalized hidden state appended to `hidden_states_list` per UT step;
- one early-exit gate value appended to `gate_list` per UT step.

The causal-LM interface also supports:
- `exit_at_step`
- `exit_threshold`
- weighted exit.

Therefore the future discriminator can observe:
- per-step hidden states;
- target-native early-exit signal;
- fixed-depth outputs;
- counterfactual exit depth.

No architecture rewrite is required merely to expose the necessary variables.

## 3. Measurement-compatibility precheck

The asset can mechanically expose all variables required by the ancestry-derived state:

### Propagation-risk ingredients
- recurrent hidden state at step t;
- bounded hidden-state perturbation point;
- remaining recurrent computation after t;
- terminal/future output difference.

### Extrinsic-progress ingredients
- consecutive recurrent hidden states;
- fixed-step output/readout;
- target-native exit/confidence signals;
- held-out task endpoint can be attached later under the Decision Contract.

### Strong cheap rivals available in the same asset
- recurrence depth;
- output confidence / entropy;
- hidden-state residual/change magnitude;
- Ouro early-exit gate / adaptive-exit signal.

Thus the candidate is not blocked by the S2 failure mode where the primary evaluator could not reach the claimed behavior.

## 4. Local execution feasibility

PC2 current resources:
- GPU: NVIDIA GeForce RTX 5070 Ti
- VRAM total: 16,303 MiB
- VRAM free at preflight: 14,542 MiB
- driver: 616.92
- D: 71.2 GB free
- E: 79.9 GB free
- F: 65.6 GB free

A 1.4B BF16 inference-only model is within the intended small-model Level-2 resource class.

No GPU inference was run in this preflight.

## 5. Download path

Direct PC2 HTTPS to Hugging Face timed out.

This is not an asset negative.

Existing local proxy:
`http://127.0.0.1:7897`

Proxy HEAD to the Ouro config succeeded and returned:
- HTTP redirect/resolve success;
- repo commit:
  `574fa66cb8bf5abdc979642d01cf2b79b16bfab1`.

Therefore the asset has an operational materialization route on PC2.

No weights were downloaded.

## 6. Execution-Leverage classification

Current evidence level:
Level 0 — public/local metadata + code/interface/resource inspection.

Lower-level evidence is sufficient to answer G0 asset/interface feasibility.

Higher-level execution is forbidden until the Decision Contract is frozen.

If that contract survives:
- next execution level may be Level 1 for benchmark/evaluator/static harness checks;
- only then Level 2 bounded Ouro inference.

## 7. Evidence boundary

G0 PASS proves only:
- exact asset availability;
- recurrence/exit interfaces expose required observables;
- local hardware/storage are sufficient in principle;
- a network materialization route exists.

It does not prove:
- Feedback Utility State exists;
- risk+progress beats cheap proxies;
- causal attribution;
- method value;
- paper novelty.

## NEXT_STEP

`FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1` only.

Do not download the full checkpoint or run GPU inference before that contract is frozen.
