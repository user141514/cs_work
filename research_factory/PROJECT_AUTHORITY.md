# cs_work Project Authority

date: 2026-09-29
status: CURRENT_REPO_RECOVERY_ENTRY
repository: D:/cs_work
remote: user141514/cs_work
scope: general computer science / ML / AI / software systems top-conference research

## 1. Ownership

WFE-03.1 moves active CS research ownership from the mixed `D:/bio_paper` workspace into this Git repository.

Active write authority:
- `D:/cs_work/research_factory/workflow_engineering/`
- `D:/cs_work/research_factory/computer_topconf_2027/`
- this file and repo-level `AGENTS.md`.

Historical source only:
- `D:/bio_paper/research_factory/workflow_engineering/`
- `D:/bio_paper/research_factory/computer_topconf_2027/`
- mixed-domain project authority under `D:/bio_paper`.

The old root remains useful provenance, but it must not become a second live writer.

## 2. Recovery

Read:
1. `AGENTS.md`
2. this file
3. `workflow_engineering/MASTER_PLAN.md`
4. `workflow_engineering/WORKFLOW_SPEC_V0_1.md`
5. `computer_topconf_2027/LIVE_STATE.md`
6. exact current evidence only.

## 3. Current execution

Plan: `WFE-20260929`.

Completed before repository separation:
- WFE-01: mechanism/specification integration;
- WFE-02: minimal offline admission/receipt gate;
- WFE-03: native PC2 verification.

Completed repository transition:
- WFE-03.1: active CS substrate moved into `cs_work` with byte-parity checks and one active write authority.

Completed execution-boundary probe:
- WFE-04: added `Gate.validate_lease()` plus a dry-run adapter for the real historical `run_stageb_agent.ps1 -Action Launch` entry.
- Native PC2 final suite: 74/74 passed, 0 failures/errors/skips.
- No PowerShell/model/network launch occurred.
- Live launch remains BLOCKED: projected arm/venv/log paths fall outside the valid lease's declared path authority; the new repo also lacks the historical backend freeze receipt/source arm; atomic dispatch claim and gate-owned executor parameter freezing are not implemented.

Next planned step:
- WFE-05: model-free immutable dispatch contract + atomic single-use claim in the gate.
- Status: PLANNED_NOT_AUTHORIZED.

## 4. Retained scientific state

`computer_topconf_2027/LIVE_STATE.md` preserves the selector/BFSC research evidence.

Status remains:
`PAUSED_UNRESOLVED__EXECUTION_SUPERSEDED_BY_WFE_20260929`.

Do not infer a scientific PASS/KILL from the repository move. No historical R0/R3 arm becomes evidence for the new workflow by migration.

## 5. Project-level gates retained

- `DECISION_CONTRACT_GATE_V1.md`: logical identifiability, comparator, attribution and verdict scope.
- `EXECUTION_LEVERAGE_GATE_V1.md`: cheapest sufficient evidence level before escalation.
- `computer_topconf_2027/STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md`: same-task controlled replay requirements.
- `workflow_engineering/WORKFLOW_SPEC_V0_1.md`: workflow interfaces and invariants.

`RESEARCH_MASTER_PLAN_DYNAMIC_V1.md` at repository root is retained only because a historical result references that relative path. It is archived provenance and is not execution authority.

## 6. Migration invariant

A future agent starting from either old or new storage must converge on the same answer:

> active CS work is written only in `D:/cs_work`.

If an old `bio_paper` plan appears newer only because it was not redirected, treat that as stale authority and resolve against this repository before executing anything.
