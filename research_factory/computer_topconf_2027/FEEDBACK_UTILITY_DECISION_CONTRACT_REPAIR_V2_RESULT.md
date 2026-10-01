# Feedback Utility State — Decision Contract Repair V2 Result

date: 2026-10-02
status: PASS_REPAIR_ONLY__LEVEL1_HOOK_PREFLIGHT_NEXT
candidate: Feedback Utility State
formal_paper_candidate: false

## Decision

`FEEDBACK_UTILITY_DECISION_CONTRACT_REPAIR_V2 = PASS`

The V1 measurement-contract defect was repaired prospectively before any scientific model execution.

## Historical V1

V1 remains immutable historical authority:

- MD SHA256:
  `ac691b22bd6024c06541d79987626bd5b4b7907e37ad5f7b37b89ca0ff17c024`
- JSON SHA256:
  `15272a0ad635a6c6947afab973614e7b94a7e50f3fe52bfb591ccbe029423d94`

Level-1 V1 correctly stopped as:

`REPAIR_NEGATIVE__EXIT_AT_STEP_INDEXING_CONTRACT_MISMATCH`

before reduced/random-model or exact-weight execution.

## V2 repair

V2 hashes:

- MD SHA256:
  `27dd5372f12668ed267770259836ae7edb94140df713ad1f7c2d3066382c3ea4`
- JSON SHA256:
  `653f5f56922c4c6ddb2f57eb8c209c78fdf45fb08da03f29ab8831cbfea1236b`

The repaired mapping is now explicit:

- scientific recurrence depth `d` is 1-based;
- `d in {2,3}`;
- Ouro runtime/list index `u` is 0-based;
- `u = d - 1`;
- `h_d = hidden_states_list[d-1]`;
- `exit_at_step=d-1`;
- the perturbation is injected after scientific depth d normalization and before scientific depth d+1 begins;
- future propagation is evaluated over scientific depths d+1 ... 4.

## Anti-drift validation

Structured V1/V2 comparison found no change outside the authorized repair fields.

Unchanged:
- model revision;
- dataset revision;
- full ARC-Challenge validation population;
- minimum population size;
- perturbation scales;
- deterministic fold/seed rule;
- cheap-rival features;
- C / C+R / C+P / joint model classes;
- fixed L2 lambda;
- NRMSE endpoint;
- 2000-resample cluster bootstrap rule;
- mixed-utility headroom thresholds;
- 10% joint-vs-cheap margin;
- 5% joint-vs-best-single margin;
- candidate-kill scope;
- execution-cost ceiling.

No scientific outcome existed when the repair was made.

## Reused Level-1 PASS evidence

The following V1 Level-1 evidence remains valid and must not be rerun:

- exact tokenizer/code/data receipts;
- 299/299 valid ARC-Challenge validation questions;
- 1794 deterministic primary units;
- canonical A–E single-token answer suffix compatibility;
- fold assignment;
- perturbation seed manifest.

Authority:
`FEEDBACK_UTILITY_LEVEL1_DATA_RECEIPT_V1.json`

## Authorization consequence

The only newly authorized work is the remaining reduced/random-model hook validation under V2.

Still unauthorized:
- full Ouro checkpoint download;
- exact-weight smoke;
- ARC-Challenge scientific PRECARD;
- controller pilot;
- N3 / BET-COMP-02 activation.

## NEXT_STEP

`FEEDBACK_UTILITY_LEVEL1_HOOK_PREFLIGHT_V2` only.
