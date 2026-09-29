# Stage-B Controlled Replay Protocol V1

date: 2026-09-28
status: FROZEN_BEFORE_POST_REVISION_SCIENTIFIC_OUTCOMES
parent:
- SPEC_TRANSFER_G0_FALSIFIER_V1.md
- SPEC_STAGE_A_TASK_FREEZE_V1.md
research_object: Behavioral Self-Adjustment / Behavioral From-Scratch Consistency for Coding Agents
scope: SWE-Together Stage-B oracle-upper-bound smoke
formal_paper_candidate: false

## 1. Why this protocol is required

The official SWE-Together user simulator is reactive: later user messages may be emitted only if an earlier agent action occurred.

That is useful for replaying a natural interaction, but it creates a causal confound for this experiment.

If R0/R1/R2/R3 receive different authoritative requirements because their earlier behavior triggers different simulator branches, an endpoint difference cannot be attributed to state reuse / refresh / restart / selective rederivation.

Therefore Stage B controls requirement exposure explicitly.

## 2. Owned decision

Question:

Under the same task initial state, same final authoritative requirement set and same coding-agent configuration, can oracle dependency-scoped selective rederivation approach a clean full-restart behavioral reference while preserving material pre-revision derived work?

This protocol changes only the execution semantics needed to identify that question. It does not change the frozen PASS_HEADROOM thresholds in SPEC_TRANSFER_G0_FALSIFIER_V1.md.

## 3. Core causal invariant

For one frozen task:

same task initial state
+
same ordered authoritative requirements
+
same model / tools / runtime / verifier
+
same pre-revision derived-state snapshot for R0/R1/R3
+
different post-revision state-reuse intervention
->
compare verifier behavior and recomputation/reuse.

Forbidden comparison:

different requirement exposure
->
different endpoint.

Requirement exposure is a controlled input, not an outcome of the arm.

## 4. Task initial state

TASK_INITIAL_STATE is the repository/project state visible to the agent at the first frozen user turn.

It is not automatically the dataset's upstream base_commit.

For S1 dataclaw-anonymizer-tests:
- upstream ancestry/base: main = 3c0991467af69675afa948c3ada45475a772fbeb;
- first-turn task state contains the pre-existing windows branch changes;
- frozen task initial checkout: windows = 3c9474ef6aa1eb75deff170a05f33e9257aeb8fd.

Evidence:
the original Turn 1 asks the agent to review `git diff main windows`, and the recorded Turn-1 tool result contains the already-existing windows patch.

Therefore R2 must start from the frozen task initial state (windows), not bare upstream main. Otherwise the experiment would confound restart cost with reconstruction of pre-existing authoritative project state.

For S2-S5, TASK_INITIAL_STATE must be adjudicated from the same outcome-blind rule before their runs.

## 5. Requirement-sequence rule

Source:
only the ordered user-facing requirement history allowed by SPEC_STAGE_A_TASK_FREEZE_V1.md.

Include:
- initial task instruction;
- later user messages that add, replace, clarify or constrain externally observable behavior;
- explicit test/verification requirements;
- implementation constraints explicitly requested by the user.

Exclude from the scientific requirement sequence:
- pure workflow requests such as commit/push/show/read-a-commit when they do not change the active behavioral contract;
- assistant interpretations not confirmed by user requirements;
- gold/reference patch;
- verifier outcomes;
- future successful trajectories.

Reactive trigger conditions may be used to understand the historical revision boundary, but may not suppress a frozen authoritative requirement from one arm.

## 6. Shared pre-revision snapshot

R0/R1/R3 must branch from one exact pre-revision snapshot rather than independently replaying the pre-revision interaction.

Snapshot identity includes:
- Git HEAD and complete dirty working-tree bytes;
- generated tests/artifacts inside the allowed task workspace;
- fixed OMP session history through the pre-revision turn;
- model/runtime/tool configuration;
- task requirement history seen so far.

Why:
independent pre-revision replays would inject agent stochasticity before the intervention and waste API budget.

R2 does not inherit this snapshot.

## 7. Arms

### R0 — RAW_HISTORY

Start from the shared pre-revision snapshot.

At the frozen revision boundary:
- deliver only the exact late requirement text;
- retain all prior session/implementation state;
- no consolidated-state refresh;
- no dependency invalidation hint.

### R1 — CONSOLIDATED_REFRESH

Start from the same shared pre-revision snapshot.

At the revision boundary:
- preserve workspace and session state;
- provide a frozen concise current-authoritative-spec refresh compiled only from allowed user requirements;
- then deliver/execute the late requirement.

No impact/dependency annotation is supplied.

### R2 — FULL_RESTART

Start a new agent session from TASK_INITIAL_STATE.

Supply the frozen consolidated final specification compiled from the same allowed user requirement set.

Do not reuse pre-revision agent session, generated reasoning, tests, edits or scratch artifacts beyond what belongs to TASK_INITIAL_STATE.

This is the clean behavioral reference.

### R3 — ORACLE_DEPENDENCY_SCOPED_REDERIVATION

Start from the same pre-revision project snapshot as R0/R1, but not the full stale reasoning state.

Provide a new session with:
- the frozen current authoritative specification;
- an outcome-blind oracle impact-scope annotation frozen before any post-revision arm result;
- a capsule of only pre-revision derived work declared independent of the changed requirement.

Impacted reasoning/decisions are omitted from the capsule and must be rederived.

Existing project bytes may remain present so the agent can inspect them; they are not declared valid merely because they exist.

No reference patch, verifier result, successful future diff or post-run trajectory may enter the impact scope or capsule.

## 8. Fixed agent/runtime contract

All scientific arms use:
- model: GPT-5.6 Sol;
- reasoning: xhigh;
- runner: OMP process under lifetime durable task identity;
- tools: read, bash, edit, write, grep, glob;
- auto-approve: enabled;
- extra skills: disabled;
- extra rules: disabled;
- extensions: disabled;
- correct task-specific runtime/venv;
- one writer per checkout;
- isolated checkout/session identity per arm.

The local equivalent harness is allowed only when the task's declared verifier/runtime can be reproduced. Runtime deviations are INVALID, not scientific negatives.

## 9. Preflight / invalidity rules

INVALID if any of the following occurs:
- arms receive different frozen authoritative requirements;
- task initial state differs across arms without a frozen intervention reason;
- model/reasoning/tools/runtime drift;
- multiple writers operate on one experimental checkout;
- a session continuation is lost or accidentally duplicated;
- gold/reference/verifier outcome leaks into R3 scope;
- task verifier cannot execute equivalently in the local runtime;
- a transport/runner failure is interpreted as an agent failure.

A task with no material pre-revision derived state at the frozen boundary is NONIDENTIFIABLE for the reuse endpoint, not CLAIM_NEGATIVE.

## 10. Work/reuse accounting

For every post-revision arm record:
1. model turns and tool calls after the revision;
2. tokens/model-call accounting when exposed;
3. files/hunks created or rederived after the revision;
4. wall time;
5. final verifier outcome.

Pre-revision artifact preservation:
- compute the fraction of pre-revision agent-derived file content/hunks that remains byte-identical in the final result;
- report this as an artifact-preservation component, not as the sole recomputation metric.

R3 reuse is credited only for derived work explicitly included in the frozen independent-work capsule or demonstrably preserved without rederivation.

## 11. S1 calibration boundary

The completed local S1 U0/T2 runs are HARNESS_CALIBRATION_ONLY and excluded from scientific counts.

They established:
- stable GPT-5.6 Sol/xhigh OMP continuation;
- correct Python 3.12 runtime;
- single-writer isolated worktree;
- original reactive triggering can diverge from requirement exposure under the fixed agent.

No R0/R1/R2/R3 scientific endpoint has yet been observed.

## 12. Execution order

1. Freeze each task's TASK_INITIAL_STATE.
2. Freeze each task's pre-revision requirement sequence and late revision.
3. Freeze R3 outcome-blind impact scope.
4. Produce exactly one shared pre-revision snapshot for R0/R1/R3.
5. Branch R0/R1/R3 from that snapshot.
6. Run R2 independently from TASK_INITIAL_STATE + consolidated final spec.
7. Run verifier and work/reuse accounting.
8. Do not tune prompts, impact scope or thresholds after post-revision outcomes.
9. After S1 local harness pilot validates arm semantics, execute the frozen S1-S5 Stage-B set.
10. Apply the original Stage-B PASS_HEADROOM / CLAIM_NEGATIVE logic only to the full frozen set.

## 13. Current first unresolved transition

Freeze S1's exact pre-revision boundary, consolidated spec and R3 oracle impact annotation
->
create shared pre-revision snapshot
->
run one S1 four-arm harness pilot
->
verify that only state-reuse intervention differs.

S1 pilot validates experiment semantics; it does not by itself adjudicate the five-task scientific claim.
