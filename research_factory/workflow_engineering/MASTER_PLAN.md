# Workflow Engineering — Dynamic Master Plan

Date: 2026-09-29
Plan ID: WFE-20260929
Status: ACTIVE
Authority: current user request to understand adjacent papers, integrate their mechanisms into our own workflow, retrospect historical tasks, and make the workflow binding.

## Goal / scope
Build and validate a reusable research-task workflow on the dedicated D:/cs_work substrate. Reuse verified mechanisms and existing tools; do not equate a collection of paper names with an implemented method. First engineer our own workflow, then evaluate it on the SAME complex historical task as the frozen original workflow. This is not an A²Flow reproduction claim, a new SOTA claim, or a new scientific candidate.

## Current user-directed engineering override — 2026-10-01

ID: WFE-06
Status: AUTHORIZED_IN_PROGRESS
Workflow policy: WORKFLOW_SPEC_V0_2_ARIS_OVERLAY.md
Branch/worktree: feat/aris-governance-overlay @ D:/cs_work_aris_overlay
Owner: current ARIS migration task
Exit condition: verified governance projection integrated or branch discarded; no idle retained worktree.

Why this step exists:
- two preregistered historical A/B replays were completed before implementation: JRAD negative/fragile case and C049 positive-success case;
- both current Research OS and Research OS + ARIS overlay scored 10/10 on frozen decision rubrics;
- ARIS overlay added no extra scientific action or blocking stage; its demonstrated incremental value is durable bounded-claim / acceptance / anti-repeat state;
- PC2 smoke proved ARIS Research Wiki can act as a derived projection and ARIS run-state preserves `done != accepted`;
- user explicitly authorized migration into current facilities.

Current single step:
implement the minimal non-authoritative ARIS governance projection defined in V0.2. Reuse existing Gate state; do not modify Gate/local_runner ownership, Watchdog, Observatory, selector lifecycle or scientific evidence. TDD + native verification + one fresh review are required.

The previously retained scientific next step `S2_STAGE_B_BOUNDARY_FREEZE_V1` is PAUSED_BY_USER_REDIRECTION, not killed or rewritten. WFE-06 completion does not automatically authorize resuming it.

## Plan
1. Verify the mechanisms and implementation seams of the selected papers; inspect existing local authority and execution assets; define one versioned integration and hard-constraint contract.
2. COMPLETE / FROZEN: gate, native verification and bounded real local execution are accepted through consolidated WFE-05. Historical Stage-B live integration is not a research prerequisite. Do not add another engineering stage without a concrete blocker in an actual research task.
3. Freeze one real complex task's initial information, old-workflow baseline, common resources, evaluator and stopping rules; label contaminated retrospective material as development-only.
4. Execute one bounded paired replay from isolated initial states; compare delivered-task correctness/quality, cost, wall time and rework under a method-neutral evaluator. Do not equate document quality or constraint counts with success.
5. Keep, modify or terminate this workflow version according to real evidence. Add further tasks only when the preceding decision justifies them.

Only the current step is authorized. Listing future steps is NOT execution authorization.

## CURRENT_STEP
ID: RESEARCH-01
Status: COMPLETED_DEVELOPMENTAL_MECHANISM_PASS__WORKFLOW_TRANSITION_BOUNDARY_CONTAMINATED
Authorization: user explicitly resumed research work in D:/cs_work and then continued the in-progress S3 replay.
Result authority: ../replays/RESEARCH_01_S3/RESULT.md.
Task: SWE-Together S3 `pi-mono-auto-93c17d3b`, base `5133697bc454da5595cf4b0c70d3c2c725677`, DEVELOPMENT_ONLY.
Observed: a fresh GPT-5.6 Sol/xhigh arm froze a six-responsibility/six-invariant Phase-A plan and implemented a functional signal UI. The authoritative first-completion Phase-A extension later calibrated as public-behavior PASS / lifecycle FAIL. After the late complaint, the arm localized the real cause to `ctx.ui.custom()` replacing/focusing away from the editor, not to `message_update` recreation, and the final implementation changed only the UI projection to keyed `setWidget()`, yielding public-behavior PASS / lifecycle PASS under the same evaluator.
Boundary contamination: after valid Phase-A completion an unexplained extra provider turn began before the late revision. It left the extension and Phase-A plan unchanged but changed the focused test by +20/-3 lines. The valid Phase-A snapshot captured before that turn is authoritative; the actual Phase-B checkout inherited the drifted test state. Therefore the final mechanism result is useful DEVELOPMENT_ONLY evidence, but the Phase-A→B workflow transition is not a clean controlled intervention.
Correct authoritative Phase-A→final rework: extension +14/-33 with 67% exact-line preservation; focused test +27/-3 with 97.89% exact-line preservation, but part of test rework is pre-late contamination and not attributable to the workflow intervention. Phase A also attempted an ordinary npx command that was blocked by the no-network environment. Hidden historical result files were not supplied; strict host-filesystem non-access was not mechanically sandboxed.
Decision: KEEP the workflow hypothesis, but do NOT compare a RAW_AGENT baseline against this contaminated treatment run. The next comparison must start both arms from the same authoritative Phase-A bytes.

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

## Historical WFE-02 acceptance (not current authorization)
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

## WFE-04 observations and decision

Result authority: WFE04_RESULT.md. The decisive result is not merely that argv construction works; it is that the existing historical launcher owns mutation paths outside the gate lease. Wrapping it more tightly without first moving dispatch/path authority upstream would preserve a bypass. Do not call it live yet.

Decision: KEEP the engineering plan, but insert one model-free dispatch-contract step before any live executor work.

## WFE-05 decision

The earlier plan to add another dispatch contract/state-machine layer is superseded. The existing gate primitive plus one direct runner closes the required trusted-local execution path. This is a simplification of implementation, not a changed research goal or a rewritten negative result.

Freeze the baseline. Repair engineering only when an actual research task exposes a decision-changing defect. Historical Stage-B revival, general agent-platform work, background services, and speculative sandbox/lease extensions are not automatic next steps.

## RESEARCH-01 observations and decision

Authority: `../replays/RESEARCH_01_S3/RESULT.md` plus the authoritative `phase_a/` freeze, retained post-completion incident snapshot, final Phase-B snapshot and endpoint JSON. The implementation demonstrates a real model→invariant→counterexample→local repair→independent endpoint loop, but the temporal workflow transition is boundary-contaminated and cannot establish comparative benefit.

The most important result is not merely endpoint PASS. The late complaint initially suggested repeated streaming recreation, but source inspection falsified that causal story: the extension had no message_update handler; the blocking behavior came from `ctx.ui.custom()` replacing/focusing away from the editor for the whole open interval. The workflow preserved independent protocol behavior and replaced only the UI projection responsibility.

Decision: KEEP the hypothesis for a clean paired late-revision replay; do not use this run as a treatment arm, add engineering, or extrapolate to paper value.

## NEXT_STEP
ID: RESEARCH-02
Status: SUPERSEDED_BY_USER_REDIRECTION
Action: from the exact authoritative first-completion `phase_a/` bytes, create two isolated identical late-revision arms. STRUCTURED receives the same pre-revision + late requirements plus mandatory goal/responsibility/invariant/counterexample/one-step replanning scaffolding; RAW_AGENT receives the same requirements and contamination boundary without that scaffolding. Both use fresh GPT-5.6 Sol/xhigh sessions, the same dependency-free constraints and the already-frozen evaluator. Do not expose the historical Phase-B plan/code/result to either arm.
Acceptance: compare final endpoint, provider wall time, process deviations, authoritative Phase-A→final rework and preservation of valid pre-revision behavior. Keep all attempts in the denominator.
Boundary: RESEARCH-02 is DEVELOPMENT_ONLY, isolates the late-revision workflow intervention only, and does not authorize publication claims, new engineering, benchmark expansion or a different task.
STOP: RESEARCH-01 is complete; RESEARCH-02 was not executed and is superseded by `../oi_agentsquare/MASTER_PLAN.md`.
