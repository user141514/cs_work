# Workflow Spec V0.2 — ARIS Governance Overlay

date: 2026-10-01
status: FROZEN_FOR_WFE06_IMPLEMENTATION
parent: WORKFLOW_SPEC_V0_1.md
plan: WFE-20260929
step: WFE-06
source_evidence:
- D:/bio_paper/research_factory/aris_replay/JRAD_20260917_AB/RESULT.json
- D:/bio_paper/research_factory/aris_replay/C049_POSITIVE_20260920_AB/RESULT.json

## 1. Objective

Add the useful ARIS governance primitives to the existing workflow without replacing any authority owner.

The overlay must make these distinctions durable:
- execution done != scientific/quality accepted;
- result != claim;
- claim verdict has explicit provenance and bounded scope;
- killed realizations retain an anti-repeat boundary;
- a resumable projection may be rebuilt from authoritative artifacts.

It is not a new scheduler, workflow engine, registry, candidate lifecycle, reviewer service, or research selector.

## 2. Authority and composition invariant

Authoritative owners remain:
- Research OS / project authority: research/scientific lifecycle and next-step choice;
- offline Gate + local_runner: frozen local execution admission, receipts and STOPPED state;
- Watchdog: continuation timing only;
- Observatory: runtime factual observation only.

ARIS governance state is a **derived projection**.

Hard invariant:

> Deleting the governance projection must not change what work is authorized, what the Gate executed, the scientific lifecycle state, or Watchdog/Observatory state. It may only remove an audit/index view that can be rebuilt from authoritative evidence.

The overlay therefore:
- MAY read a finished Gate state and explicitly supplied evidence files;
- MAY write only to its declared projection directory;
- MUST mark itself non-authoritative;
- MUST copy next-step information only as a pointer with `authorized=false`;
- MUST NOT call Gate.admit/submit/finish, local_runner, Watchdog, Observatory, model APIs, network clients, or reviewer clients;
- MUST NOT infer a claim verdict from execution success.

## 3. Minimal interface

New tool:

`research_factory/workflow_engineering/governance_overlay.py`

CLI:

```
python -B governance_overlay.py \
  --state-dir <finished Gate state directory> \
  --request <frozen governance request JSON> \
  --output <new projection JSON>
```

The output path is exclusive: an existing output is rejected.

### Request schema

```json
{
  "schema": "aris-governance-request-v1",
  "identity": {
    "task_id": "...",
    "task_version": 1,
    "workflow_id": "...",
    "workflow_version": "...",
    "plan_id": "...",
    "plan_version": 1,
    "step_id": "...",
    "run_id": "..."
  },
  "claim": {
    "claim_id": "...",
    "statement": "...",
    "scope": "...",
    "verdict": "UNASSESSED | PROVISIONAL | SUPPORTED | REFUTED"
  },
  "review": {
    "kind": "NONE | SAME_FAMILY | INDEPENDENT | DETERMINISTIC",
    "reviewer": "...",
    "verdict_id": "..."
  },
  "evidence": [
    {"path": "<declared file>", "sha256": "<64 hex>"}
  ],
  "kill_boundary": {
    "closed": false,
    "scope": "...",
    "anti_repeat": ["..."]
  }
}
```

## 4. Acceptance semantics

Execution state is read from the existing Gate:
- source Gate must be `STOPPED`;
- request identity must exactly equal the frozen Gate contract identity;
- evidence paths must exist and hashes must match;
- overlay never changes Gate state.

Claim rules:
- `UNASSESSED` requires `review.kind=NONE`;
- `PROVISIONAL` may use `SAME_FAMILY` and requires reviewer + verdict id;
- `SUPPORTED` or `REFUTED` require either:
  - `INDEPENDENT` with reviewer + verdict id; or
  - `DETERMINISTIC` with verifier identity + receipt id.
- same-family review can never produce `SUPPORTED` or `REFUTED`.

This imports ARIS's "a loop may drive but cannot acquit" boundary without forcing an extra review when the workflow already owns a deterministic decision contract.

## 5. Output schema

`aris-governance-projection-v1` contains:
- `authoritative: false`;
- `projection_only: true`;
- source identity and Gate contract fingerprint;
- source phase/decision and attempt summary;
- claim + review provenance;
- evidence hashes;
- kill boundary / anti-repeat state;
- copied next-step pointer with `authorized=false`;
- output content hash is not self-embedded; filesystem hash is the receipt.

No mutable wiki/database is required for V0.2. A future index may derive typed Paper/Idea/Experiment/Claim nodes from these immutable projections; the projection files remain the substrate.

## 6. Failure semantics

Reject before output creation when:
- source Gate is not STOPPED;
- identity mismatches;
- evidence is missing or hash-drifted;
- verdict/reviewer combination violates section 4;
- kill boundary is malformed;
- output exists;
- request tries to carry an authorized next step or another authority field.

Failure of the overlay never converts scientific PASS to FAIL or vice versa; it is a governance/integration error.

## 7. Windows/runtime boundary

The migrated production tool emits ASCII-only CLI status, avoiding the upstream ARIS Windows-GBK emoji failure observed in replay smoke tests.

If upstream ARIS CLI helpers are invoked manually, PC2 must set `PYTHONUTF8=1`.

No dependency on the cloned ARIS repository is required at runtime.

## 8. Testing

TDD acceptance:
1. RED before implementation.
2. Finished Gate + UNASSESSED claim -> projection, `authoritative=false`, next step remains unauthorized.
3. Same-family SUPPORTED -> reject.
4. Same-family PROVISIONAL -> pass.
5. Independent/deterministic SUPPORTED or REFUTED -> pass with provenance.
6. RUNNING/non-STOPPED Gate -> reject.
7. identity mismatch -> reject.
8. evidence hash drift -> reject.
9. duplicate output -> reject.
10. projection write cannot mutate Gate state.
11. existing WFE offline + local_runner suites stay green.
12. Native PC2 Python 3.7 compatibility is required.

## 9. Non-goals

Not in WFE-06:
- install/copy the ARIS skill catalog;
- replace Research State Map / Residual Graph / TOPIC_BET / PRECARD;
- add reviewer/model calls;
- add a daemon/database/service;
- modify Watchdog/Observatory;
- auto-run NEXT_STEP;
- auto-edit skills via meta-optimize/meta-apply.

## 10. Completion

WFE-06 is complete only when:
- the projection tool passes focused + existing workflow suites;
- a real existing stopped WFE local-run fixture can be projected and independently read back;
- source Gate state is byte/semantic unchanged;
- branch receives fresh whole-diff review;
- no authority owner changed.

After completion, exactly one next step may be proposed but remains unauthorized.
