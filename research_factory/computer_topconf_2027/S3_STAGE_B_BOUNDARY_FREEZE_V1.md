# S3 Stage-B Offline Boundary Freeze V1 — pi-mono-auto-93c17d3b

date: 2026-09-30
status: OFFLINE_BOUNDARY_FROZEN__COMMON_PRESTATE_PENDING__R3_EXACT_SCOPE_PENDING
parent:
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
- S3_MECHANISM_EXPOSURE_GATE_V1.md
task: pi-mono-auto-93c17d3b
scientific_post_revision_arm_observed: false
paid_s3_arm_authorized: false

## 1. Task identity

repo: badlogic/pi-mono

authoritative official task environment:
- docker image: `ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-93c17d3b:2f7d1992e60d`
- official Dockerfile hard-checkout: `5133697bc454da5595655cf4b0c70d3c2c725677`

Frozen `TASK_INITIAL_STATE`:

`5133697bc454da5595655cf4b0c70d3c2c725677`

Reason:

Unlike S1, the first S3 user turn does not reference or require a pre-existing branch/dirty project patch. It supplies external extension code/context in the message and asks for explanation. The official task environment hard-checks out the base commit and supplies no task-initial dirty patch. Therefore the task initial project state is the hard-checkout commit.

Frozen substrate hashes:
- official task.toml: `4676cc1660709cd1da6030a9e1e47cebc741409e96b8fb19ddbf1fc7d4d6c8e3`
- official environment/Dockerfile: `1c9f85e457efd7fdee80c2b81c5d9b3c8cd620addad86a9b8056b9b9225dca40`
- Stage-A task freeze: `e34ceeb68d5de194add6079b44ac2457c0283776c7d11fde600cc1af3d213181`
- frozen raw user requirements: `2d1a65f1df329e90ded685ac9b7a183be03f07d67b8a3d34a7d27bda62af1b89`

No reference patch, canonical goals, oracle trajectory, verifier result, RESEARCH-01 Phase-B implementation/result, or successful future solution participates in this boundary freeze.

## 2. Controlled authoritative sequence

The original simulator/user trace is reactive. Requirement exposure is therefore controlled explicitly and does not depend on whether a fixed agent reproduces historical intermediate successes.

### C0 — source_message_index 0 — CONTEXT_ONLY

The user supplies a separate extension example/Discord discussion and asks for an ELI5 explanation of the mechanism.

Role:
- motivates the extension/message-control use case;
- does not itself require a repository implementation.

Do not require a Stage-B arm to reproduce the pasted go-to-bed extension.

### U1 — source_message_index 2 — AUTHORITATIVE_PRE_REVISION_REQUIREMENT

Verbatim core:
`can we write a test extension ... /start ... injects a hidden custom message ... listen for message_end and react accordingly, e.g. by showing ui, or closing ui`

Behavioral contract:
- implement a test extension;
- expose a slash-command activation entry point;
- activation injects a hidden custom session message;
- completed assistant messages drive UI reactions through the message/event path;
- opening and closing are signal-driven behaviors.

### U2 — source_message_index 31 — AUTHORITATIVE_LOCATION_CONSTRAINT

Verbatim:
`move that to cwd/.pi/extensions so i can relaod`

Behavioral/implementation constraint:
- the extension must live in the repository-local loaded-extension directory so it can be reloaded as an extension.

### W1 — source_message_index 34 — WORKFLOW_ONLY

`alright do things`

This triggers execution but adds no externally observable product contract. It is excluded from the scientific requirement sequence.

### U3 — source_message_index 36 — AMBIGUOUS_BEHAVIORAL_CLARIFICATION__CONSERVATIVELY_INCLUDED

Verbatim:
`ok, if you do it all in one message then the ui will not open i guess`

Frozen interpretation:
- the useful behavior requires the UI to remain meaningfully open rather than collapse open+close inside one assistant response;
- open and close must be separable across turns/messages.

This is conservatively included before execution under the Stage-A ambiguity rule.

### O1/O2 — source_message_index 38 / 40 — HISTORICAL_OBSERVATIONS

The user observes that the signal UI is open/waiting, then later closed.

These are useful exposure witnesses but do not independently add a new requirement. They do not gate later requirement delivery.

### U4 — source_message_index 42 — AUTHORITATIVE_MULTI_TURN_VERIFICATION_REQUIREMENT

Verbatim core:
`... do a bunch of turns, in the first turn open the ui, in the last turn clos eit`

Contract:
- signal UI must support a multi-turn interval;
- first relevant turn opens;
- later/final relevant turn closes;
- intermediate work can occur while the UI remains open.

### U5 — source_message_index 44 — AUTHORITATIVE_CORRECTION_AND_VERIFICATION_REQUIREMENT

Verbatim core:
`if you output open and close, close is also executed. let's try again. 10 turns ... open on first turn, close on last turn`

Contract:
- do not collapse both signals into one assistant message;
- preserve ordered signal separation;
- support a sustained 10-turn-style workload between open and close.

The specific README-reading workload is a verification scenario, not a durable product requirement.

### W2/W3 — source_message_index 48 / 51 — WORKFLOW_ONLY

`next`
`just do all 10 turns`

These advance the historical interaction but add no new extension behavior. They are excluded from the scientific requirement sequence and may not determine whether the late revision is delivered.

### REVISION_BOUNDARY

Freeze immediately after the controlled pre-revision contract U1-U5 has been implemented and its pre-revision state/session has been persisted once by the fixed scientific agent configuration.

Historical W1/W2/W3 and O1/O2 do not alter this boundary.

Every post-revision arm receives the late requirement regardless of whether its pre-revision execution would have naturally triggered the historical simulator branch.

### U6 — source_message_index 54 — AUTHORITATIVE_LATE_REVISION

Verbatim:
`hm, when you output shit, the ui kinda freezes. i see markdown coming in, but i basically can't type. is the ui code int he message_end/update path foobar? do we recreate ui all the time?`

Controlled behavioral requirement:
- while assistant output/streaming occurs with the signal UI active, the user must retain usable input/editor responsiveness;
- the UI projection/lifecycle must not be repeatedly recreated or otherwise steal/block input as output arrives;
- retain the existing activation, hidden protocol, distinct signal handling, multi-turn open state and later close behavior unless a narrower implementation change is required.

The endpoint requirement is responsiveness/lifecycle correctness; a specific API-level repair is not frozen.

## 3. Consolidated active spec before U6

Derived only from the controlled user-facing sequence:

1. Provide a repository-local test extension under `.pi/extensions`.
2. Provide a slash-command activation path such as `/start`.
3. Activation injects a hidden custom/session control message rather than exposing the control protocol as normal visible transcript content.
4. Completed assistant messages can emit distinct open and close signals that the extension observes.
5. Open and close are separate events; combined same-response open+close does not satisfy the contract.
6. The UI can remain open across multiple intervening turns/work while the final/later signal closes it.
7. The extension remains inactive until explicitly activated.

The 10-turn README workload is retained as a verification scenario, not as a permanent extension feature.

## 4. Consolidated final spec for R2

Derived only from the controlled requirements:

1. Start from `TASK_INITIAL_STATE = 5133697bc454da5595655cf4b0c70d3c2c725677`.
2. Satisfy the complete pre-revision extension contract in §3.
3. Preserve a multi-turn signal-driven open state and later explicit close.
4. Fix the late UI lifecycle defect so normal assistant output/streaming does not freeze user typing/input while the signal UI is active.
5. Avoid update/projection behavior that repeatedly recreates or replaces the interactive input surface in a way that causes the reported freeze.
6. Preserve command activation, hidden protocol injection, distinct signal semantics, extension loadability and inactive-before-start behavior.
7. Run task-appropriate correctness checks for both the retained signal behavior and the late lifecycle/responsiveness requirement.

Do not import reference patch, gold implementation, canonical goals, verifier outcomes, historical assistant diagnosis, RESEARCH-01 Phase-B solution or future successful trajectory.

## 5. Fixed scientific agent/runtime identity

Inherited from `STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md`:
- model: GPT-5.6 Sol;
- reasoning: xhigh;
- OMP process under lifetime durable task identity;
- tools: read, bash, edit, write, grep, glob;
- no extra skills/rules/extensions;
- one writer per isolated checkout/session;
- task-correct Node/Bun runtime;
- same frozen authoritative requirements for every arm.

Preferred runtime identity is the official task image above or a separately verified byte/behavior-equivalent local runtime. Runtime deviation is INVALID, not a scientific negative.

## 6. Outcome-blind semantic dependency boundary for future R3 scope

This offline freeze does **not** claim exact file/hunk scope because the scientific common pre-revision state does not exist yet.

Freeze the classification rule now:

### AFFECTED / MUST_REDERIVE_OR_REVALIDATE

Any pre-revision derived reasoning, implementation, test or state whose validity depends on:
- how the persistent/open signal UI is projected into the TUI/editor;
- whether that projection blocks/replaces/focus-steals the input surface;
- UI creation/recreation/update behavior during assistant output/streaming;
- assumptions that UI-open lifecycle is responsive under continued output.

### POTENTIALLY_INDEPENDENT / REUSABLE_IF_PRESENT

Pre-revision derived work may be declared reusable only when its validity does not depend on the late lifecycle defect, including responsibilities such as:
- repository-local extension placement/loading;
- slash-command registration/activation;
- hidden custom-message/control-protocol injection;
- signal token/protocol definition;
- assistant-message `message_end` signal recognition/classification;
- inactive-before-start behavior;
- ordering rule that close is legal only after open;
- same-message combined-signal rejection, if implemented independently from the UI projection mechanism.

### REVALIDATE_ONLY

Tests or reasoning that exercise retained behavior through the same UI/lifecycle seam may remain informative but must be rerun/revalidated after U6.

Exact artifacts are assigned to these classes only **after the fixed common pre-revision snapshot exists and before any U6/R0/R1/R2/R3 post-revision outcome is observed**.

Gold/reference/verifier/post-result evidence remains forbidden.

## 7. Immutable common-prestate contract

If Execution Leverage later authorizes producing the scientific pre-revision state, its freeze is not complete until all items below are materialized outside the mutable live worktree:

1. task initial/base commit identity;
2. exact pre-revision checkout HEAD;
3. `git status --porcelain=v1` receipt;
4. exact tracked dirty patch bytes, including binary-safe representation when needed;
5. copies + SHA256 + byte size of every agent-created/untracked task artifact;
6. explicit deletion manifest for removed tracked files;
7. immutable OMP session/history bytes through the pre-revision boundary + SHA256;
8. model/reasoning/tool/runtime identity receipt;
9. hashes of the requirement-history inputs used;
10. pre-revision derived-work manifest suitable for later reuse accounting;
11. outcome-blind R3 impacted / revalidate / independent annotation generated from this immutable bundle;
12. one freeze manifest containing hashes of every item above.

A live worktree path alone is never the scientific snapshot or reuse denominator.

## 8. Invalidity / nonidentifiability

INVALID if:
- an arm starts from a project state other than the frozen task initial state without an explicitly frozen intervention reason;
- historical execution triggers determine whether U6 is delivered;
- arms receive different final authoritative requirements;
- R3 semantic scope uses RESEARCH-01 Phase-B result, reference patch, verifier outcome, oracle/future solution or any post-revision arm result;
- common prestate is reconstructed independently for R0/R1/R3 instead of cloned from one immutable snapshot;
- a mutable worktree later replaces the frozen artifact bundle for reuse accounting.

NONIDENTIFIABLE for the reuse endpoint if the fixed pre-revision agent produces no material derived work before U6.

## 9. Current decision

`S3_OFFLINE_BOUNDARY_FREEZE = PASS`.

This does not authorize a paid model arm.

Exact next step:

`S3_EXECUTION_LEVERAGE_GATE`

Use only frozen assets and expected costs to decide whether producing the common prestate and paid R2/R3 evidence is worth the spend.

No R0/R1/R2/R3 S3 arm is authorized by this boundary freeze alone.
