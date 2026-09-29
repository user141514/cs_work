# SPEC Transfer — Stage A Task Freeze V1

date: 2026-09-28
status: STAGE_A_PASS_WITH_LIMITED_REPO_DIVERSITY
parent: SPEC_TRANSFER_G0_FALSIFIER_V1.md
substrate: SWE-Together
selection_mode: OUTCOME_BLIND_METADATA_ONLY
scientific_experiment_run: false

## 1. Stage-A decision

The frozen eligibility rule required:
- >=5 public tasks;
- >=3 user intents;
- at least one later requirement addition/correction that changes the active contract rather than merely requesting explanation;
- pinned base repository state;
- published verifier/test identity;
- reconstructable consolidated final specification.

Five tasks satisfy the metadata-level rule.

Therefore:

STAGE_A_ELIGIBILITY = PASS.

This does **not** authorize a scientific positive claim.
The official runtime remains blocked on PC2, so Stage B has not run.

## 2. Frozen tasks

### S1 — dataclaw-anonymizer-tests
repo: peteromallet/dataclaw
base_commit: 3c0991467af69675afa948c3ada45475a772fbeb
num_user_intents: 5
category: feature

Evolution witness:
- initial work concerns reviewing/implementing the anonymizer change;
- later intents add tests;
- a later intent further changes the performance/implementation contract by requiring compiled regexes and asking for additional speed improvements.

Verifier identity:
published F2P/P2P gates cover username anonymization behavior, substring safety, import/basic functionality and the task-specific tests.

Why eligible:
the later performance/test requirements are not mere explanation requests; they alter the active implementation/verification contract after prior work exists.

### S2 — pi-mono-auto-a4fca584
repo: badlogic/pi-mono
base_commit: e54dff7efb460e364a39e4a22369991a20c105b9
num_user_intents: 10

Evolution witness:
- initial request is analysis-only for issue 1216 and explicitly forbids implementation;
- later the user authorizes implementation;
- subsequent intent changes path semantics so paths resolve relative to settings.json;
- later intents exercise the new behavior and ask documentation-related follow-up.

Verifier identity:
published task manifest contains explicit functional gates for the implementation and path behavior.

Why eligible:
the action contract changes from analyze-only -> implement -> revised path semantics.

### S3 — pi-mono-auto-93c17d3b
repo: badlogic/pi-mono
base_commit: 5133697bc454da5595655cf4b0c70d3c2c725677
num_user_intents: 9

Evolution witness:
- initial task starts from an existing extension use case;
- later requirements move the extension into the loaded-extension directory;
- later intents require open/close signals across turns and a 10-turn behavior;
- a subsequent correction reports UI freezing during streaming and requires avoiding UI recreation.

Verifier identity:
published F2P/P2P gates cover command/handler behavior, protocol injection, distinct signals and loadable-extension behavior.

Why eligible:
later requirements alter lifecycle/UI behavior after the extension path already exists.

### S4 — pi-mono-auto-d3b2130d
repo: badlogic/pi-mono
base_commit: 353ac792ebb99931c640ee55af90881d3a45c4d9
num_user_intents: 6

Evolution witness:
- initial request asks for npm-registry keyword discovery;
- later requirement introduces the unique pi-package keyword;
- later intents extend the target to sibling packages, publishing/version changes and documentation updates.

Verifier identity:
published task metadata includes an executable test command:
bun x vitest run --reporter=verbose
plus task-specific correctness expectations.

Why eligible:
the required output grows from discovery into repository/package metadata changes and documentation consistency.

### S5 — pi-mono-auto-ec7037ba
repo: badlogic/pi-mono
base_commit: 69d02b8a5fce07041f77aba64c6ebbc8589827ab
num_user_intents: 8

Evolution witness:
- initial task audits release/changelog work;
- after commit/release activity, a later user report says merged autocomplete behavior is broken;
- the subsequent requirement changes trailing-space autocomplete behavior and requires a corrective implementation.

Verifier identity:
published F2P/P2P gates describe the autocomplete behavior and regression boundary.

Why eligible:
a late behavioral regression creates a second implementation phase after earlier release-oriented work.

## 3. Consolidated-final-spec compilation rule

For every frozen task, compile the authoritative final specification only from the ordered user-facing requirement history.

Include:
- the initial instruction;
- later requests that add, remove, replace or clarify externally observable behavior;
- corrections that change implementation constraints when those constraints are explicitly part of the user's contract;
- verification requirements explicitly requested by the user.

Exclude:
- pure workflow requests such as "commit", "push", or "show me";
- conversational questions that do not alter required behavior;
- assistant/model interpretations not confirmed by the user;
- reference patches, gold diffs, successful future executions, verifier outcomes, or post-result explanations.

Conflict rule:
later explicit user requirements supersede incompatible earlier requirements.

Ambiguity rule:
if an intent may or may not change required behavior, mark it AMBIGUOUS and conservatively include it before execution. The classification cannot be changed after outcomes are observed.

At each revision boundary also freeze the **active contract at that time**, so Stage B can distinguish stale derived state from valid reusable state.

## 4. R3 oracle-scope rule

R3 is an oracle only about **semantic dependency scope**, never about the correct final code.

Allowed evidence for dependency annotation:
- requirements/intents available at that revision boundary;
- base-repository source structure available before the run;
- manually frozen human judgment about which prior decisions/tests/files can semantically depend on the changed requirement.

Forbidden:
- reference patch;
- gold implementation;
- post-run successful diff;
- verifier pass/fail outcome;
- any future agent trajectory.

The human annotation is frozen before R0/R1/R2/R3 outcomes are generated.

## 5. Diversity limitation

The five-task smoke set spans only two repositories:
- peteromallet/dataclaw: 1 task;
- badlogic/pi-mono: 4 tasks.

Therefore:
- Stage A proves **substrate availability**, not cross-repository generality;
- Stage B may use these five only as an oracle-upper-bound smoke;
- any later formal candidate confirmation must expand repository diversity before making a broad coding-agent claim.

## 6. Runtime gate

PC2 current official-harness state remains:

G0_SCIENTIFIC_ASSET = PASS.
G0_OFFICIAL_HARNESS_RUNTIME = BLOCKED.

Missing current runtime paths:
- Docker/container runtime;
- or an equivalent verified SWE-Together sandbox path;
- required official-harness provider credentials where applicable.

Do not reinterpret this as a research negative.

## 7. Stage-A verdict

PASS_WITH_LIMITED_REPO_DIVERSITY.

The transfer now has enough public evolving-requirement substrate to justify paying for exactly one Stage-B oracle-upper-bound smoke.

Next decision-changing step:
run R0/R1/R2/R3 on S1-S5 under one fixed agent/runtime once an authoritative sandbox path is available.

No dependency-learning model, no benchmark expansion, and no new topic generation is authorized before that smoke.
