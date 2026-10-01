# Feedback Utility State — Level-1 Hook Preflight V2

date: 2026-10-02
status: PASS_HOOK_VALIDATION__LEVEL1_HARNESS_ADMITTED__EXACT_WEIGHT_SMOKE_NEXT
candidate: Feedback Utility State
scientific_model_runs: 0
gpu_science_runs: 0
checkpoint_downloaded: false

## Decision

`FEEDBACK_UTILITY_LEVEL1_HOOK_PREFLIGHT_V2 = PASS`

Combined with the already-PASSed tokenizer/data admission from V1:

`FEEDBACK_UTILITY_LEVEL1 = PASS_HARNESS_ADMITTED`

The measurement chain is mechanically valid on the exact Ouro code path under a reduced/random non-scientific fixture.

This does not produce any scientific Feedback Utility result.

## 1. Exact environment

Ouro revision:
`574fa66cb8bf5abdc979642d01cf2b79b16bfab1`

Exact code receipts:
- config.json SHA256:
  `ce9cc13da41591b8b4deca053d7dfee06424c0228628ee862ea86d725bc163f3`
- configuration_ouro.py SHA256:
  `950443e32929047aa08d02abad2e1888bc1914b3db988d3d675f70787f65dafb`
- modeling_ouro.py SHA256:
  `c5c68fbb368ce2909c257ae2afc50719be8c91539333d3295e19312c4316f413`

Runtime:
- Python 3.11.13
- torch 2.8.0+cu128
- transformers 4.55.0
- execution device: CPU
- CUDA memory allocated before/after: 0

Transformers 4.55.0 wheel:
- SHA256:
  `29d9b8800e32a4a831bb16efb5f762f6a9742fef9fce5d693ed018d19b106490`

The temporary 4.55.0 overlay was used only to satisfy the exact Ouro code import.
No system/conda package was modified.

## 2. Fixture

Random reduced Ouro configuration:
- vocab_size = 128
- hidden_size = 32
- intermediate_size = 64
- num_hidden_layers = 1
- num_attention_heads = 4
- num_key_value_heads = 4
- total_ut_steps = 4
- use_cache = false
- deterministic seed = 20261002

The test uses the exact upstream `OuroModel.forward`.

It does **not** copy/reimplement the recurrence loop.

Instrumentation is injected only by temporarily monkeypatching the existing `OuroRMSNorm.forward` call:
- record the normalized state after each UT step;
- optionally alter only the last-token vector at the target scientific depth;
- immediately return control to the unchanged upstream recurrent loop.

Weights/config remain unchanged.

## 3. Repaired indexing validation

### Scientific depth d=2

Correct mapping:
- scientific depth d=2
- runtime/list index u=1
- `exit_at_step=1`

Recorded hidden -> lm_head versus `exit_at_step=1`:

`max_abs_diff = 0.0`

Historical V1 mapping `exit_at_step=2`:

`max_abs_diff = 0.1846059113740921`

### Scientific depth d=3

Correct mapping:
- scientific depth d=3
- runtime/list index u=2
- `exit_at_step=2`

Recorded hidden -> lm_head versus `exit_at_step=2`:

`max_abs_diff = 0.0`

Historical V1 mapping `exit_at_step=3`:

`max_abs_diff = 0.10771382600069046`

Therefore the V2 repair is not merely notational.
It maps to the actual Ouro runtime semantics.

## 4. No-op instrumentation identity

With recording enabled but no perturbation:

- final hidden max abs diff = 0.0
- recurrent hidden max abs diff = 0.0
- gate max abs diff = 0.0

Therefore:

`NOOP_INSTRUMENTATION_IDENTITY = PASS`

## 5. epsilon=0 identity

### d=2

- final hidden diff = 0.0
- all hidden diff = 0.0
- all gate diff = 0.0
- recorded pre-depth diff = 0.0
- delta norm = 0.0

### d=3

Same:
- all relevant diffs = 0.0
- delta norm = 0.0

Therefore the frozen V2 epsilon=0 invariant PASSes exactly, stronger than the required 1e-5 tolerance.

## 6. +/- perturbation locality and future propagation

Perturbation:
`epsilon = 0.03`

For both d=2 and d=3, both +delta and -delta:

- pre-depth state matches baseline exactly;
- all earlier recurrent states match baseline exactly;
- non-last-token coordinates at target depth remain unchanged;
- target last-token change matches the requested delta within ~2.3e-8;
- at least one future recurrent state changes nontrivially.

Observed future last-token max absolute effects:

### d=2

+delta:
- depth3: 0.0448746681
- depth4: 0.0367515087

-delta:
- depth3: 0.0456094742
- depth4: 0.0368826389

### d=3

+delta:
- depth4: 0.0288364887

-delta:
- depth4: 0.0285357237

Therefore:

`PERTURBATION_LOCALITY = PASS`

and:

`FUTURE_PROPAGATION_PATH = PASS`

## 7. State immutability

Model parameter/state digest before:

`71cddac9a6457ab7e7dcfbd13d60225f5fd89507402e208d437dd1246fe775ed`

after:

`71cddac9a6457ab7e7dcfbd13d60225f5fd89507402e208d437dd1246fe775ed`

Config digest before/after:

`c1f8593c192a23ac320e045688b1c810a81c1df24d80a48961b9da73a3c4d632`

Therefore:
- weights unchanged;
- config unchanged.

## 8. Reproducibility receipts

Executed hook script:
`tools/feedback_utility_hook_preflight_v2.py`

SHA256:
`b306b1612f7888e9e0d800e91f4d65533e63870f4e6bf8e682366c2157a430fe`

Raw report SHA256:
`05128a3643d7b5b52bc9c11f5bf5a3ba90e4e1d24b6c31abd7226666918c39a5`

The raw temporary report was transcribed into the structured JSON authority below; the temporary environment is not part of the repository.

## 9. Level-1 overall adjudication

V1 tokenizer/data admission:
PASS.

V2 hook admission:
PASS.

Therefore:

`FEEDBACK_UTILITY_LEVEL1 = PASS_HARNESS_ADMITTED`

This authorizes only the next frozen execution level:

> materialize the exact Ouro checkpoint revision and run a small non-primary exact-weight smoke on ARC-Challenge **train** examples.

The exact-weight smoke must verify:
- model loads at the frozen revision;
- no-op/epsilon=0 invariants still hold on exact weights;
- repaired d -> d-1 fixed-step equivalence holds;
- perturbation path remains active;
- projected runtime/VRAM stay within the frozen execution-leverage ceiling.

## 10. Still unauthorized

Do not yet run:
- ARC-Challenge validation scientific PRECARD;
- primary NRMSE models;
- headroom adjudication;
- controller pilot;
- N3 / BET-COMP-02;
- any BFSC rescue.

## NEXT_STEP

`FEEDBACK_UTILITY_EXACT_WEIGHT_SMOKE_V1` only.

Checkpoint download is now authorized **only** for this exact-weight smoke at revision `574fa66...`.
