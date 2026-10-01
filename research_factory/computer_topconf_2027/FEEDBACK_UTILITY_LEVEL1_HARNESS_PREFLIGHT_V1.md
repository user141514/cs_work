# Feedback Utility State — Level-1 Harness Preflight V1

date: 2026-10-02
status: REPAIR_NEGATIVE__EXIT_AT_STEP_INDEXING_CONTRACT_MISMATCH
candidate: Feedback Utility State
scientific_model_runs: 0
gpu_science_runs: 0
checkpoint_downloaded: false

## Decision

`FEEDBACK_UTILITY_LEVEL1_HARNESS_PREFLIGHT_V1 = REPAIR_NEGATIVE`

Tokenizer/data/manifest admission passed, but the frozen V1 Decision Contract contains an off-by-one mapping error between the scientific recurrence-depth symbol `t` and Ouro's runtime `exit_at_step` API.

No scientific metric was computed.

No candidate conclusion is allowed.

## 1. What passed

### Exact small assets

Model revision:
`574fa66cb8bf5abdc979642d01cf2b79b16bfab1`

Dataset revision:
`210d026faf9955653af8916fad021475a3f00453`

Exact small-file/data receipts are frozen in:
`FEEDBACK_UTILITY_LEVEL1_DATA_RECEIPT_V1.json`

No `model.safetensors` file was downloaded.

### ARC population

ARC-Challenge validation:
- 299 rows;
- 299 valid questions;
- 0 invalid questions;
- choice counts:
  - 3 choices: 3
  - 4 choices: 295
  - 5 choices: 1

Frozen fold counts:
- fold0: 58
- fold1: 67
- fold2: 53
- fold3: 75
- fold4: 46

Frozen primary units:
`299 * 2 depths * 3 epsilon = 1794`

### Tokenizer / answer scoring

The exact prompt terminates with:

`Answer:`

with:
- no trailing newline;
- no separator before the canonical answer label.

Across **all 299 real prompts**, appending the correct canonical label preserves the prompt token prefix and adds exactly one token.

Canonical answer token IDs:
- A -> 49
- B -> 50
- C -> 51
- D -> 52
- E -> 53

Therefore:

`ANSWER_SCORING_COMPATIBILITY = PASS`

The newline form is explicitly not allowed: `Answer:\nA` introduces two suffix tokens.

## 2. Frozen-manifest construction

Question fold:
`SHA256(question_id) mod 5`

Perturbation seed:
`SHA256(question_id || depth)`

The generated question/unit manifests are deterministic and their hashes are frozen in the data receipt.

These receipts may be reused after V2 repair.

## 3. Contract defect found before model execution

### Scientific depth semantics in V1

The Decision Contract freezes:

`t in {2,3}`

and states that:
- (P_t) requires a prior recurrent state;
- **both depths leave at least one future recurrent step**.

With Ouro's four recurrent steps, that makes `t` a **1-based recurrent depth**:
- scientific t=2 -> second recurrent step;
- scientific t=3 -> third recurrent step.

### Ouro runtime API semantics

Exact `modeling_ouro.py` revision `574fa66...`:

- recurrent loop:
  `for current_ut in range(self.total_ut_steps)`
- `hidden_states_list.append(hidden_states)` once per UT step;
- `exit_at_step` later selects:
  `hidden_states_list[exit_at_step]`

Therefore `exit_at_step` is a **0-based list index**:
- runtime index 0 -> scientific depth 1;
- runtime index 1 -> scientific depth 2;
- runtime index 2 -> scientific depth 3;
- runtime index 3 -> scientific depth 4.

Correct mapping:

`exit_at_step = t - 1`

### Frozen V1 error

V1 harness invariant says:

> applying lm_head to recorded step hidden state must reproduce the corresponding `exit_at_step=t` logits.

For scientific t=2/3, that compares:
- recorded depth2 against runtime depth3;
- recorded depth3 against runtime depth4.

This is structurally off by one.

Running the reduced/random hook under this V1 contract would therefore test the wrong invariant.

## 4. Why execution stops here

The frozen contract itself classifies tokenizer/harness incompatibility before primary science as REPAIR_NEGATIVE.

The factory's staged-execution invariant says:

`PREREQUISITE_INVALID -> DOWNSTREAM_EXECUTION_FORBIDDEN`

Therefore:
- do not instantiate the random reduced model under V1;
- do not download Ouro weights;
- do not run train smoke;
- do not run ARC validation science.

Continuing would create evidence under a known-invalid measurement contract.

## 5. Scientific scope

This result does **not** mean:
- Feedback Utility State is false;
- Ouro lacks the required recurrence interface;
- perturbation instrumentation is impossible;
- ARC scoring is invalid.

It means only:

> the V1 Decision Contract's scientific-depth-to-runtime-exit mapping is wrong and must be prospectively repaired before hook validation.

## 6. Exact repair scope

V2 must change only the indexing convention and all dependent wording/manifest fields.

Required repair:

1. explicitly define scientific depth `d in {2,3}` as 1-based;
2. define runtime UT/list index:
   `u = d - 1`;
3. replace every `exit_at_step=t` equivalence with:
   `exit_at_step=d-1`;
4. perturb recorded `hidden_states_list[d-1]`;
5. future recurrence set becomes scientific depths `d+1 .. 4`;
6. keep unchanged:
   - model/dataset revisions;
   - full validation population;
   - epsilon set;
   - cheap rival;
   - model classes;
   - headroom thresholds;
   - practical 10%/5% margins;
   - bootstrap rule;
   - negative scopes;
   - fold/seed manifest rules.

No other contract term may be changed during V2 repair.

## NEXT_STEP

`FEEDBACK_UTILITY_DECISION_CONTRACT_REPAIR_V2` only.

After V2 is frozen:
- rerun only the remaining reduced/random-model hook portion of Level-1;
- reuse the already-PASS tokenizer/data/manifests by frozen receipt;
- no checkpoint download until Level-1 V2 PASS.
