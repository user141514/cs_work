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

Consolidated WFE-05 remains the frozen engineering baseline. `local_runner.py` executes one frozen step of audited local Python work, collects receipts and stops. Details: `research_factory/workflow_engineering/WFE05_RESULT.md`.

RESEARCH-01 is complete under `research_factory/replays/RESEARCH_01_S3/RESULT.md`. The final S3 implementation provides DEVELOPMENT_ONLY mechanism evidence: the same independent evaluator gives authoritative Phase-A public PASS/lifecycle FAIL and final Phase-B public PASS/lifecycle PASS after the UI projection changed from editor-replacing `ctx.ui.custom()` to keyed `setWidget()`. However, an unexplained extra provider turn after Phase-A completion changed the focused test by +20/-3 before the late revision; the actual Phase-B checkout inherited that drift. The valid `phase_a/` first-completion snapshot is authoritative, and the RESEARCH-01 workflow transition is boundary-contaminated. Do not use it as a treatment arm for superiority claims.

The engineering baseline stays FROZEN. The next planned step is RESEARCH-02: from the exact authoritative Phase-A bytes, run two isolated fresh GPT-5.6 Sol/xhigh late-revision arms—STRUCTURED vs RAW_AGENT—under the same requirements/runtime/evaluator, differing only in mandatory responsibility/invariant/counterexample/replanning scaffolding. Listing it does not authorize execution or model spending. Do not add WFE-06 or translate RESEARCH-01 into workflow superiority.

The historical BFSC / selector work in `research_factory/computer_topconf_2027/` is PAUSED_UNRESOLVED scientific evidence, not current launch authorization.

## Git discipline

Use short-lived branches and verified atomic commits. Preserve failed experiments and historical evidence. Do not rewrite old result files to make a new workflow look successful. Do not commit credentials, caches, runtime SQLite state, or generated local verification directories.
