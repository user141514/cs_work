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

The engineering baseline stays FROZEN. RESEARCH-02 is SUPERSEDED_BY_USER_REDIRECTION and is not the active research line. The AgentSquare/ALFWorld Orthogonality + Invariants line under `research_factory/oi_agentsquare/MASTER_PLAN.md` is now TERMINATED_NO_ADMITTED_RESIDUAL_SEAM. OI-AS-00 found structural occupancy; OI-AS-01 was only tiny-n directional; OI-AS-02A proved the MemoryTP authority manipulation; OI-AS-02B was NULL_ON_PILOT; OI-AS-02C/OI-AS-03/OI-AS-04 found 0 material PlanningIO-vs-Original-TP macro conflicts across the complete 6-target eligible prevalence set and terminated `MemoryTP-plan-conflict`. OI-AS-00's hard union (42) equals I3_MEMORY_BOUNDARY (42), with I2_DECOMPOSITION_AUTHORITY=35 nested inside it, so no independent hard seam remains. OI-AS-05 Residual O+I Decision Gate found no residual soft seam that passes the pre-registered A-E admission criteria: planner-to-reasoner guidance is an explicit hierarchical handoff with no isolating frozen contrast or pre-existing harm signal; memory-to-reasoner guidance is the terminated TP seam; planning-to-tool guidance has zero executable ALFWorld exposure. Do not integrate an O+I hard gate, do not launch a strip-guidance soft intervention, and do not create OI-AS-06 without genuinely new external evidence. Control returns to the higher-level research selector/replanning layer. The live top-conference selector has now been mutated with MECHANISM_EXPOSURE_GATE (`STATIC_HEADROOM != MECHANISM_EXPOSURE`): when a causal story requires conflict/mismatch/competition/stale-state survival or another runtime relation, freeze and test actual exposure before a family-specific intervention. Calibration receipt: `research_factory/computer_topconf_2027/MECHANISM_EXPOSURE_GATE_CALIBRATION_20260930.md`. No new TOPIC_BET is activated by this mutation. Do not resume workflow-effectiveness RESEARCH-02 unless the user explicitly returns to it.

The BFSC/selective-rederivation line is CLOSED as `PRECARD_NONIDENTIFIABLE__FROZEN_STAGE_B_EXHAUSTED` and must not be reopened/rescued. Higher-level selector re-entry is COMPLETE from the frozen portfolio, with **Feedback Utility State = finite-horizon propagation risk + extrinsic progress** now live Rank 1. Its bounded direct-prior attack remains `DIRECT_VETO=false / TRANSFER_OPEN_BUT_CROWDED`, G0 asset/interface preflight PASSes, and `FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1` is now prospectively frozen before any checkpoint download/GPU science. The first PRECARD uses exact Ouro revision `574fa66...`, full valid `allenai/ai2_arc@210d026f... / ARC-Challenge / validation`, recurrence depths {2,3}, fixed perturbation scales {0.01,0.03,0.05}, strongest cheap rival C, and nested C/C+R/C+P/joint models. PASS requires >=10% NRMSE reduction vs C and >=5% vs best single-coordinate arm with positive question-cluster-bootstrap CI lower bounds; mixed useful/harmful headroom and harness-validity failures are NONIDENTIFIABLE/REPAIR_NEGATIVE rather than candidate negatives. No weights are downloaded and no GPU inference has run. Authority: `FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1.md/json` and `FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_RESULT_V1.md/json`. Exact next step is `FEEDBACK_UTILITY_LEVEL1_HARNESS_PREFLIGHT_V1` only; no checkpoint download or scientific inference before Level-1 admission.

## Git discipline

Use short-lived branches and verified atomic commits. Preserve failed experiments and historical evidence. Do not rewrite old result files to make a new workflow look successful. Do not commit credentials, caches, runtime SQLite state, or generated local verification directories.
