# cs_work Repository Authority

## Scope

This repository is the active engineering and evidence workspace for general computer-science / machine-learning / AI / software-systems top-conference research.

Molecular-generation and graduation-thesis portfolios remain outside this repository unless the user explicitly imports a bounded asset.

## Recovery order

For any continuation, recover in this order:

1. `AGENTS.md`
2. `research_factory/PROJECT_AUTHORITY.md`
3. `research_factory/workflow_engineering/MASTER_PLAN.md`
4. `research_factory/workflow_engineering/WORKFLOW_SPEC_V0_1.md`
5. `research_factory/computer_topconf_2027/LIVE_STATE.md`
6. only the exact experiment/result files needed for the current step.

Do not reconstruct current authority from older result files or from `D:/bio_paper`.

## Ownership after WFE-03.1

`D:/cs_work` is the sole active write authority for CS top-conference research and workflow-engineering state.

The corresponding directories retained under `D:/bio_paper/research_factory/` are historical migration sources only. They may be read for provenance, but no new CS execution state, plan update, result, or code change may be written there after WFE-03.1.

The copied root file `RESEARCH_MASTER_PLAN_DYNAMIC_V1.md` is historical provenance only. It is not an active execution plan.

## Workflow execution contract

Before execution:
- pin task / plan / workflow / step identity;
- read the active total plan;
- authorize exactly one current decision-changing step;
- preserve explicit dependencies, write isolation, frozen inputs/evaluator and stop conditions.

After that step:
- re-read real evidence;
- record supported and unsupported conclusions;
- KEEP / MODIFY / TERMINATE the total plan as warranted;
- write exactly one NEXT_STEP;
- STOP.

A planned next step is not authorization. An approximately 180-degree change terminates the old plan instead of silently rewriting it.

Workflow-policy changes require a new version. Scientific negative evidence only kills the frozen claim it validly identifies.

## Current execution state

WFE-04 is complete under `research_factory/workflow_engineering/WFE04_RESULT.md`: a real Stage-B launcher command can be prepared behind a revalidated gate lease without launching PowerShell/model/network, but live integration is BLOCKED because the historical launcher owns arm/venv/log paths outside the lease scope and atomic dispatch/parameter freezing are not yet gate-owned.

The next planned step is WFE-05: add a model-free immutable dispatch contract and atomic single-use claim inside the gate. It is not authorized merely by being listed. Do not launch or modify the historical Stage-B PowerShell runner in WFE-05.

The historical BFSC / selector work in `research_factory/computer_topconf_2027/` is PAUSED_UNRESOLVED scientific evidence, not current launch authorization.

## Git discipline

Use short-lived branches and verified atomic commits. Preserve failed experiments and historical evidence. Do not rewrite old result files to make a new workflow look successful. Do not commit credentials, caches, runtime SQLite state, or generated local verification directories.
