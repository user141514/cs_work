# Workflow Engineering — Dynamic Master Plan

Date: 2026-09-29
Plan ID: WFE-20260929
Status: ACTIVE
Authority: current user request to understand adjacent papers, integrate their mechanisms into our own workflow, retrospect historical tasks, and make the workflow binding.

## Goal / scope
Build and validate a reusable research-task workflow on the dedicated D:/cs_work substrate. Reuse verified mechanisms and existing tools; do not equate a collection of paper names with an implemented method. First engineer our own workflow, then evaluate it on the SAME complex historical task as the frozen original workflow. This is not an A²Flow reproduction claim, a new SOTA claim, or a new scientific candidate.

## Plan
1. Verify the mechanisms and implementation seams of the selected papers; inspect existing local authority and execution assets; define one versioned integration and hard-constraint contract.
2. Implement the smallest offline admission/receipt gate; use deterministic counterexamples and one historical audit fixture before any live wiring or paid replay.
   Native-verification insertion after WFE-02: verify the exact checker on PC2 before considering a real execution adapter; independent tests do not establish Windows runtime parity.
3. Freeze one real complex task's initial information, old-workflow baseline, common resources, evaluator and stopping rules; label contaminated retrospective material as development-only.
4. Execute one bounded paired replay from isolated initial states; compare delivered-task correctness/quality, cost, wall time and rework under a method-neutral evaluator. Do not equate document quality or constraint counts with success.
5. Keep, modify or terminate this workflow version according to real evidence. Add further tasks only when the preceding decision justifies them.

Only the current step is authorized. Listing future steps is NOT execution authorization.

## CURRENT_STEP
ID: WFE-03.1
Status: COMPLETED_REPOSITORY_MIGRATION
Authorization: explicit user request on 2026-09-29 to name and execute WFE-03.1.
Result authority: WFE03_1_RESULT.md.
Observed: the active CS/top-conference substrate was migrated from D:/bio_paper into the dedicated Git repository D:/cs_work; pre-authority-edit copy parity passed for 13 workflow-engineering files and 55 computer-topconf files; three directly referenced upstream process/provenance files were additionally preserved; obvious secret-pattern scan returned zero hits.
Ownership: D:/cs_work is now the sole active writer for CS/top-conference and workflow-engineering state. The corresponding D:/bio_paper copies are historical provenance only.
Predecessor: WFE-03 native PC2 verification remains valid under WFE03_RESULT.md.
Decision: KEEP the workflow-engineering plan. Repository separation changes ownership/location, not scientific conclusions or workflow-effectiveness evidence. No model/agent/API/GPU launch, Watchdog change, historical replay or live executor integration occurred.

## Previous completed step
ID: WFE-01
Status: COMPLETED_SPECIFICATION_ONLY
Question: Which verified mechanisms can compose through explicit interfaces into a minimally sufficient workflow on our existing substrate, and what must remain fixed while task-specific plans evolve?
Allowed: primary-paper and official-code inspection; local read-only recovery; writing this plan, mechanism/design evidence and scoped recovery pointers.
Forbidden: paid agent/model runs, GPU experiments, historical outcome claims for a new workflow, workflow search, broad new-topic scanning, automatic continuation, watchdog/runtime changes, and silently resuming BFSC S3.
Deliverable: WORKFLOW_SPEC_V0_1.md containing source-grounded mechanism boundaries, module interfaces, state transitions, invariants, replay contamination boundaries and exact enforcement status.

## State and evidence at start
- Read live AGENTS.md, PROJECT_AUTHORITY_20260929.md and RESEARCH_MASTER_PLAN_DYNAMIC_V1.md on PC2 workspace ws_597f47059c.
- D:/bio_paper is not a Git repository; no branch, rebase, commit or clean-tree claim is applicable to this root.
- The existing dynamic master plan points to BFSC S3 offline freeze, whereas the current user explicitly redirects execution to workflow engineering.
- Preserve all BFSC and molecular experiment evidence. Suspending/superseding execution authority is not a scientific KILL or a positive result.
- Existing instructions already require one-step execution, evidence-led replanning, bounded branching and no historical leakage. These must be reused, not rediscovered as novel contributions.

## Replanning and termination contract
Before each step: pin plan ID/version, workflow version, input evidence and step acceptance.
After each step: record observations, supported/unsupported conclusions, keep/modify/terminate decision and exactly one NEXT_STEP; stop.
Changing the goal or reversing the scientific strategy is TERMINATE old plan + new plan ID, not silently editing the old objective. Local implementation fixes and bounded plan changes require a recorded reason and new version.
Frozen run inputs/evaluator/comparators cannot be changed in response to its result. A changed contract creates a new run; retain the original.

## WFE-01 observations and decision

Observed:
- Verified the primary methods for AgentSquare, Flow, AFlow, A²Flow and EnCompass; inspected key public Flow/AFlow/AgentSquare code interfaces. This is mechanism/adapter analysis, not full reproduction.
- A²Flow's linked public repository currently exposes only README; its abstraction mechanism cannot yet be treated as a ready official-code replacement seam.
- Flow's public main combines standardized dependency/parallelism terms in code; do not assume the current implementation exactly reproduces the paper's described selection order.
- Local STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md already contains useful same-task/isolation invariants. Reuse these rather than inventing them again.
- rebase_omp_session_workspace.py was read and has destructive destination replacement in its CLI. run_stageb_agent.ps1's first 220 lines show a task-specific legacy launch path and setup side effects; neither was executed.
- scripts/r11_level01_replay.py was inspected and is molecular sampling-statistics replay, NOT a workflow replay executor. It is excluded.
- WORKFLOW_SPEC_V0_1.md now defines the integration, interfaces, counterexamples, contamination boundaries and exact enforcement status.
- AGENTS.md / PROJECT_AUTHORITY_20260929.md / legacy execution plan / BFSC LIVE_STATE now distinguish the current engineering authority from retained scientific evidence.

Decision: KEEP this engineering master plan. Adopt v0.1 as the implementation specification, not as a validated successful workflow. The old BFSC execution plan is TERMINATED_BY_USER_REDIRECTION; BFSC scientific evidence is PAUSED_UNRESOLVED. No 180-degree scientific rewrite has been disguised as a successful local mutation.

Unsupported: no superiority over any baseline, no historical counterfactual victory, no live runtime enforcement, no full reproduction, no publishable-method claim. No paid model/agent/GPU run or workflow search was started in WFE-01.

## Current-step acceptance (promoted from previous NEXT_STEP)
ID: WFE-02
Status: AUTHORIZED_BY_CURRENT_USER
Action: implement the smallest offline admission/receipt gate for the frozen v0.1 interfaces, using a fake dispatch/receipt driver first. Reuse local snapshot/accounting helpers only after inspection; do not call legacy launch/setup scripts for smoke.
Acceptance: reject missing/stale plan identity, invalid dependency graphs, unisolated conflicting work, wrong-workspace paths, missing/tampered evidence, invalid evidence misclassified as scientific failure, and repeated/unauthorized transitions; allow valid independent work; after a step produce NEXT_STEP but never dispatch it automatically.
Limit: no model/API/GPU launch, no Watchdog changes, no paid historical replay. Record the remaining preconditions for wiring a real existing executor rather than claiming all shell/MCP access is enforced.
WFE-02 evidence now supports keeping the minimal offline gate. PC2-native parity remains unverified because remote shell requests were platform-blocked. No live executor, scientific experiment or historical replay was started.

## WFE-02 observations and decision

Result authority: WFE02_RESULT.md and verification_independent/result.json.
Delivered: offline_gate.py, complete deterministic tests, synthetic historical-path fixture, verify_offline.py, README.md.
Independent verification: Linux / Python 3.13.5, 58/58 tests passing, 0 failures/errors/skips; 100/100 repeated conflicting-admission races passed using two separate SQLite connections in threads. Python 3.7 grammar check passed, not runtime parity.
Fixed from regression evidence: frozen path-alias retargeting, boolean version identities, malformed receipts, linked evidence, and explicit termination after contract drift. Reported resource use is not presented as independent metering.
PC2: files written with permitted file tools and core code/test sections read back; no remote test, model call, historical replay, Watchdog change, commit or push.
Decision: KEEP the master plan and minimal adapter approach; no effectiveness or scientific superiority claim. Insert native verification before live wiring. This is an implementation-plan revision, not an approximately 180-degree goal reversal.

## WFE-03.1 observations and decision

Result authority: WFE03_1_RESULT.md.
Raw migrated assets were committed separately before authority edits so historical evidence remains reviewable. The new repo-level AGENTS.md and research_factory/PROJECT_AUTHORITY.md define recovery and single-writer ownership. The old mixed-domain root must not receive further active CS state after this transition.

Decision: KEEP. The first unresolved engineering boundary remains live enforcement integration, not offline gate correctness or repository placement.

## NEXT_STEP
ID: WFE-04
Status: PLANNED_NOT_AUTHORIZED
Action: identify one current real execution entry and build the smallest gate-to-executor adapter in model-free dry-run mode. A valid admitted lease may resolve/prepare the existing command, but dry-run must not launch a model/agent. Invalid/stale/missing leases must block preparation/dispatch; expose the trusted workspace/session paths and receipt fields needed for later live use.
Acceptance: deterministic PC2 adapter tests prove reject-before-dispatch for invalid authority, one legal dry-run path, no automatic NEXT_STEP dispatch, and an explicit inventory of remaining bypasses/side effects before any live launch.
Forbidden: paid/model/API/GPU launch, historical replay, Watchdog changes, broad executor refactor, automatic WFE-05.
STOP: WFE-03.1 is complete; WFE-04 has not been executed.
