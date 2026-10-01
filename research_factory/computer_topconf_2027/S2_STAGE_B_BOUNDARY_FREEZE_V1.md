# S2 Stage-B Offline Boundary Freeze V1 — pi-mono-auto-a4fca584

date: 2026-10-01
status: OFFLINE_BOUNDARY_FROZEN__COMMON_PRESTATE_PENDING__R3_EXACT_SCOPE_PENDING
parent:
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
- S2_MECHANISM_EXPOSURE_GATE_V1.md
- BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md
task: pi-mono-auto-a4fca584
scientific_post_revision_arm_observed: false
paid_s2_arm_authorized: false

## 1. Task identity

repo: badlogic/pi-mono

Official environment:
- docker image: `ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-a4fca584:d1a6ee81ebeb`
- Dockerfile hard-checkout: `e54dff7efb460e364a39e4a22369991a20c105b9`

Frozen TASK_INITIAL_STATE:

`e54dff7efb460e364a39e4a22369991a20c105b9`

Reason:
the official environment hard-checks out this commit and the first user instruction asks for issue analysis only. No task-initial dirty patch or required branch state is supplied.

Frozen source hashes:
- official task.toml: `ef07e5601a1ea034f91613826367ec003154ab6a7ff4f86249641a940509e6f3`
- official environment/Dockerfile: `cbe4b94cc413226505d89320c183ad1b597a965be58231433aea3bb775872a86`
- official instruction.md: `aed069e0e6154a1c25cc39999f6f57acec654f275e7fbfefe13877b8b69ffa28`
- official original_session.json: `ae10c249ef12dcc1bd3e57b692360386c82a6e848c3a9d1730f72c116a3b53c4`
- Stage-A task freeze: `e34ceeb68d5de194add6079b44ac2457c0283776c7d11fde600cc1af3d213181`
- selector replan: `d02140bceaa785b7f4e3e323fc6b7c3770ec1559dfa848bcebb28035ea557cdf`
- frozen public issue-1216 requirement receipt: `917ee0ada34443673003fd30219bca9d5600033d5b2a1077543e51d573640968`

Requirement compilation uses:
- `S2_ISSUE_1216_SOURCE_V1.md`, the frozen public issue context explicitly referenced by the first user instruction;
- user-role messages only from the official original session.

Forbidden:
assistant trajectory, oracle_session/oracle_intents, canonical_goals, reference_patch, verifier result, future successful diff.

## 2. Controlled authoritative sequence

### C0 — source_message_index 0 — ANALYSIS_ONLY_INITIAL_CONTRACT

The user asks to analyze issue 1216, read related code, identify the real cause / concise implementation approach, and explicitly says:

`Do NOT implement unless explicitly asked. Analyze and propose only.`

Contract:
- understand the public issue;
- no implementation yet.

Frozen public issue requirement context:
- `pi install` should support local extension/file paths;
- avoid requiring manual direct edits to `settings.json`.

### U1 — source_message_index 6 — PRE_IMPLEMENTATION_SETTINGS_SEMANTICS_CLARIFICATION

Verbatim:
`but, wouldn't that basically add a local path to packages i settings.json? is that ok?`

Role:
- confirms the design concerns a local package/path persisted through settings;
- still before implementation authorization.

### U2 — source_message_index 8 — AUTHORITATIVE_IMPLEMENTATION_AUTHORIZATION

Verbatim:
`oki, implement concisely`

Contract transition:
analysis-only -> implementation authorized.

### U3 — source_message_index 20 — AUTHORITATIVE_PRE_REVISION_VERIFICATION_REQUIREMENT

Verbatim:
`try it with pi-test.sh. i'm especially curious what happens with relative paths. are they resolved to absolute paths in settings.json?`

Contract:
- exercise the implementation through pi-test.sh;
- inspect/preserve sensible relative-path behavior in settings;
- this message establishes that path persistence/resolution behavior already exists before the late correction.

### REVISION_BOUNDARY

Freeze after the controlled C0/U1/U2/U3 pre-revision sequence has been delivered and the fixed scientific agent has completed/persisted the resulting implementation state once.

Historical assistant success is not required to decide when the late requirement is delivered.

### U4a — source_message_index 37 — AUTHORITATIVE_LATE_REVISION_PRECURSOR

Verbatim:
`so, i guess when we write to settings.json, we need to make these paths relative to the settings.json, no? or how can they be resolved otherwise if we just have the cwd relative path in settings.json, both user and project?`

Late semantic correction begins:
- existing cwd-relative persistence is identified as wrong/unstable across user/project settings;
- required semantic anchor becomes the settings file receiving the entry.

### U4b — source_message_index 39 — AUTHORITATIVE_LATE_REVISION

Verbatim:
`i want the path to be resolved relative to the settings.json we write it to, anything else makes no sense.`

Controlled late requirement:
- when persisting local package paths, store/interpret them relative to the concrete `settings.json` file being written;
- user- and project-settings locations therefore use their own settings-file directory as semantic base;
- preserve the broader local-package installation/settings feature unless a narrower change is required.

U4a+U4b are one late-revision bundle.

### W1 — source_message_index 76 — POST_REVISION_VERIFICATION_WORKFLOW

`try with -l`

This requests another execution/verification path and adds no new durable package-path semantics.

### E1 — source_message_index 108 — EXPLANATION_ONLY

The user asks for an explanation of a specific source change involving packageSourcesMatch.

This is not a new product requirement.

### W2/W3 — source_message_index 110 / 112 — PUBLICATION_WORKFLOW

`good to commit and push and close the issue?`
`yes`

These concern repository publication/issue workflow, not the scientific product contract.
Stage-B arms must not commit/push/close issues.

### D1 — source_message_index 114 — AMBIGUOUS_POST_REVISION_DOC_CHECK

`oh, do we need to update docs? packages.md possibly?`

Conservative final-spec interpretation:
- check whether the new local-package/path semantics make the user-facing package documentation stale;
- update documentation only if needed for consistency;
- do not convert this question into an unconditional requirement to edit docs.

## 3. Consolidated pre-revision spec

Derived only from allowed requirement sources:

1. Support the issue-1216 local-extension/local-package installation use case through the normal package/settings workflow rather than requiring manual destructive settings edits.
2. After explicit authorization, implement the feature concisely.
3. Local package/path state may be represented in `settings.json`.
4. Preserve both user/project settings behavior implied by the existing package system.
5. Exercise the implementation through `pi-test.sh` and inspect relative-path persistence/resolution behavior.
6. No late settings-file-relative correction has yet been supplied at this stage.

## 4. Consolidated final spec for R2

1. Start from TASK_INITIAL_STATE `e54dff7efb460e364a39e4a22369991a20c105b9`.
2. Implement the local extension/package installation behavior requested by issue 1216 through the normal package/settings flow.
3. Preserve add/remove and existing user/project settings responsibilities of the package feature.
4. When a local package/path is persisted in settings, its stored/resolved semantics must be relative to the specific `settings.json` file receiving the entry, not an arbitrary invocation cwd.
5. User and project settings therefore resolve relative paths from their respective settings-file directories.
6. Duplicate detection/removal/comparison logic must remain correct under that path basis.
7. Exercise relevant CLI/package paths, including the verification intent represented by `pi-test.sh` and later `-l` use, without hardcoding the historical command sequence into product logic.
8. Check user-facing package documentation such as `packages.md` for consistency and update only if the new behavior would otherwise be stale.
9. Run task-appropriate correctness checks.

Do not import assistant trajectory, reference/gold patch, canonical goals, verifier outcomes, oracle session/intents or future successful solution.

## 5. Fixed scientific agent/runtime identity

Inherited from STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md:
- GPT-5.6 Sol;
- xhigh;
- OMP under lifetime durable task identity;
- tools read,bash,edit,write,grep,glob;
- no extra skills/rules/extensions;
- auto-approve;
- one writer per isolated checkout/session;
- task-correct official Node/Bun runtime or separately verified equivalent.

Prospective PARTIAL_REFERENCE_GUARD from BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md is binding for S2.

## 6. Outcome-blind dependency rule for future R3 exact scope

Exact file/hunk scope remains pending the scientific common prestate.

### AFFECTED / MUST_REDERIVE_OR_REVALIDATE

Any pre-revision derived reasoning, implementation, tests or state whose validity depends on:
- the semantic base used to persist local package paths;
- cwd-relative vs settings-file-relative normalization;
- user/project settings-file directory selection;
- serialization of relative package paths;
- package source comparison/deduplication/removal when relative-path equivalence depends on a base directory;
- tests or docs that encode the old path basis.

### POTENTIALLY_INDEPENDENT / REUSABLE_IF_PRESENT

Pre-revision derived work may be reusable when independent of the changed path base, including:
- the general fact that local packages/extensions are supported;
- command/CLI wiring for add/remove/list/install when not path-base-specific;
- settings scope selection mechanics independent of relative-path normalization;
- non-path-specific validation and error handling;
- issue-analysis conclusions unrelated to path origin;
- documentation/provenance text unrelated to path semantics.

### REVALIDATE_ONLY

- tests spanning both retained package behavior and changed path semantics;
- docs that mention local packages/settings paths;
- integration behavior whose correctness depends indirectly on both retained feature wiring and affected path normalization.

Exact artifacts are classified only after one common-prestate bundle exists and before any post-revision arm outcome.

## 7. Immutable common-prestate contract

If later authorized, freeze outside the mutable worktree:
1. base/HEAD identity;
2. git status receipt;
3. tracked dirty patch;
4. every untracked/agent-created artifact with bytes/hash/size;
5. deletion manifest;
6. immutable OMP session bytes/hash through U3;
7. model/reasoning/tool/runtime identity;
8. hashes of requirement inputs and frozen issue context;
9. pre-revision derived-work manifest;
10. outcome-blind exact R3 affected/revalidate/independent scope;
11. one manifest hashing all freeze items.

A mutable worktree path is never the reuse denominator.

## 8. Invalidity / nonidentifiability

INVALID if:
- the prestate uses a project state other than the frozen base without a frozen intervention reason;
- assistant/oracle/reference/verifier/post-outcome evidence enters requirement compilation or R3 scope;
- arms receive different final authoritative requirements;
- R3 scope is produced after observing a post-revision arm;
- R0/R1/R3 reconstruct separate prestates instead of branching from one immutable freeze.

NONIDENTIFIABLE for reuse if the fixed pre-revision agent produces no material derived work before U4a/U4b.

## 9. Decision

`S2_OFFLINE_BOUNDARY_FREEZE = PASS`.

This does not authorize a paid model arm.

Exact next step:
`S2_EXECUTION_LEVERAGE_GATE_V1`.

That gate must apply the prospective PARTIAL_REFERENCE_GUARD and decide the minimum paid arm sequence.