# S1 Stage-B Boundary Freeze V1 — dataclaw-anonymizer-tests

date: 2026-09-28
status: BOUNDARY_FROZEN__R3_SCOPE_PENDING_PRESTATE
parent: STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
task: dataclaw-anonymizer-tests
scientific_result_observed: false

## 1. Task identity

repo: peteromallet/dataclaw

ancestry:
- main/base_commit: 3c0991467af69675afa948c3ada45475a772fbeb

frozen TASK_INITIAL_STATE:
- windows: 3c9474ef6aa1eb75deff170a05f33e9257aeb8fd

Reason:
the original first user turn asks to review `git diff main windows`, and its recorded tool result contains the already-existing windows patch. Those bytes are project input at Turn 1, not agent-derived post-task work.

## 2. Controlled authoritative sequence

### P0 — task initial state

Checkout windows@3c9474ef6aa1eb75deff170a05f33e9257aeb8fd.

### U1 — diagnostic instruction

Exact:
`Read \`git diff main windows\` for the changes in this branch. Review them.`

Contract role:
- inspect current project state;
- produce review/diagnostic derived state.

### U2 — diagnostic refinement

Exact:
`Is there any visible issue in the changes?`

Contract role:
- require visible-issue diagnosis;
- no explicit user requirement to commit/push.

### Historical U3 — excluded workflow turn

Exact historical text:
`Read \`git show HEAD\` for the new commit. Review it.`

Classification:
WORKFLOW_ONLY for controlled Stage B.

Reason:
it requests inspection of a commit created by the historical agent; it does not add an externally observable product requirement. Whether a fixed agent happens to create a commit after U2 must not control later requirement exposure.

### U4 — pre-revision verification requirement

Exact:
`Add tests in tests/test_anonymizer.py to cover the changes.`

Classification:
AUTHORITATIVE_PRE_REVISION_REQUIREMENT.

It changes the required verification artifact and can create reusable derived work.

### REVISION_BOUNDARY

Immediately after U4 completes and the resulting workspace/session state is persisted.

This exact snapshot becomes the common branch point for R0/R1/R3.

### U5 — late revision

Exact:
`Compile the regexes in the anonymizer. How else can we speedup the anonymizer?`

Classification:
AUTHORITATIVE_LATE_REVISION.

It changes the implementation/performance contract after prior diagnostic/test work exists.

## 3. Consolidated active spec before U5

Derived only from allowed user requirements:

1. Review the existing main..windows changes and identify visible issues.
2. Maintain the current task project state rooted at the windows branch.
3. Add runnable pytest coverage in tests/test_anonymizer.py for the changes.

No gold bug list or verifier-derived hidden requirement is injected.

## 4. Consolidated final spec for R2

Derived only from allowed user requirements:

1. Start from the frozen S1 task initial project state (windows).
2. Review the main..windows changes and account for visible issues.
3. Add tests in tests/test_anonymizer.py covering the changes.
4. Compile/cachе the anonymizer regexes so pattern construction is amortized rather than repeated per call.
5. Address the user's open performance request by identifying at least one additional concrete way to speed up the anonymizer; implementation is not required unless the fixed agent judges it necessary.

Important:
this spec does not import the reference patch, canonical-goal bug list, verifier outcomes or historical assistant diagnosis.

## 5. Fixed pre-revision agent configuration

- GPT-5.6 Sol
- xhigh reasoning
- OMP session continuation
- tools: read,bash,edit,write,grep,glob
- no extra skills/rules/extensions
- Python runtime: D:/bio_paper/external/spec_stageb_s1_venv
- one isolated worktree writer

The existing U1/U2 local run is admitted only as the common pre-revision trajectory substrate; it is not a post-revision arm result.

## 6. R3 scope freeze timing

Do not freeze exact R3 impacted/independent derived work until U4 completes, because the actual pre-revision derived artifacts do not yet exist.

After U4 and before any U5/R0/R1/R2/R3 post-revision outcome:
- read only current requirement history + TASK_INITIAL_STATE + pre-revision workspace/session state;
- freeze impacted vs independent derived work;
- then clone the common snapshot.

Gold/reference/verifier results remain forbidden.

## 7. Invalidity / nonidentifiability

INVALID if:
- an arm starts from main rather than the frozen task initial windows state;
- U3 presence/absence changes whether U4/U5 is delivered;
- post-revision arms receive different authoritative requirements;
- R3 annotation uses gold/reference/verifier/post-revision evidence.

If U4 produces no material derived work, S1 is NONIDENTIFIABLE for the reuse endpoint and remains harness calibration only.

## 8. Next transition

Deliver U4 to the existing common pre-revision OMP session
->
persist exact workspace/session snapshot
->
freeze R3 impact annotation
->
branch R0/R1/R3 and construct independent R2.
