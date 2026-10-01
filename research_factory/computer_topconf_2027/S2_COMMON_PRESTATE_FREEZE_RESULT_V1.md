# S2 Common Prestate Freeze Result V1

date: 2026-10-01
status: PASS_COMMON_PRESTATE_FROZEN__R3_SCOPE_FROZEN__R2_NEXT
task: pi-mono-auto-a4fca584
freeze_bundle: S2_COMMON_PRESTATE_FREEZE_V1
freeze_manifest_sha256: 22498a753aeda06a14d612e3fa825db84504249902e2d9d71f928df09f44e5f5

## Decision

`S2_COMMON_PRESTATE_FREEZE = PASS`

The post-U3 pre-revision scientific state is now represented by an immutable logical bundle independent of the mutable WSL worktree, and the exact outcome-blind R3 semantic/file-hunk scope is frozen before any late-revision/R2/R3 outcome.

S2 is identifiable for the reuse endpoint because material derived work exists.

## Frozen project identity

Base commit:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Final scientific project state:
- 7 tracked modified files;
- 0 untracked task artifacts;
- 0 tracked deletions;
- no commit inside the task repo.

Tracked patch:
- bytes: 8,292;
- SHA256:
  `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`.

Exact reconstruction is:

`base commit + tracked_dirty.patch`

with empty deletion and untracked-artifact manifests.

The mutable WSL worktree is not the snapshot.

## Independent reconstruction validation

A fresh exact official S2 Docker image was used as an independent reconstruction substrate.

Validation:
- exact base HEAD: PASS;
- `git apply --check --binary`: PASS;
- patch application: PASS;
- reconstructed git status: exact 7-file modified set;
- untracked files: 0;
- all seven reconstructed file SHA256 values exactly match the live post-U3 prestate.

Authority:
`S2_COMMON_PRESTATE_FREEZE_V1/reconstruction_validation.json`.

## Frozen session/history

Session ID:
`01a0f7cc-4a3e-7000-8639-ae33f7a25a58`

Frozen external copy:
`D:/cs_work/external/spec_stageb_sessions/s2_common_pre_frozen_v1/2026-10-01T14-09-15-838Z_01a0f7cc-4a3e-7000-8639-ae33f7a25a58.jsonl`

- bytes: 2,037,536;
- lines: 217;
- SHA256:
  `27de34edff19712f382c5086bfc96adc123b04a00f32618f89b8ea847e850000`;
- scientific user turns: exactly four;
- exact controlled indices: 0, 6, 8, 20;
- late revision 37/39 absent.

The live WSL session file is now read-only and the session directory is non-writable for the scientific user.

This session must never be continued.

## Runtime / agent identity

Scientific trajectory:
- `openai-codex/gpt-5.6-sol`;
- xhigh;
- no fallback;
- OMP 18.1.15;
- tools `read,bash,edit,write,grep,glob`;
- no skills/rules/extensions/title.

Task runtime:
- official image identity:
  `sha256:24df21b472314647843bab5009a4f5b443a129e7bd42904936e0176277bf8148`;
- base: exact `e54dff7...`;
- Node v20.20.2;
- npm 10.8.2;
- task Bun 1.3.13;
- user agent uid1001.

Scientific execution substrate:
- WSL-native Ubuntu 26.04 / x86_64;
- task repo/runtime copied byte/mode-preserving from the exact official image;
- isolated harness Bun1.3.14 for OMP only;
- host command-backed Codex resolver via Windows interop;
- no provider credential file copied into WSL.

## Requirement-input integrity

Frozen inputs include:
- public issue-1216 requirement receipt;
- source adapter;
- exact U0/U1/U2/U3 prompt files;
- user-only source receipt;
- Stage-B boundary freeze;
- exact late-revision bundle text 37/39.

Late semantic correction is frozen as:

> persist/interpret local package paths relative to the specific settings.json receiving the entry rather than persisting caller-cwd-derived absolute-path semantics.

The late revision has not been delivered to the common-prestate session.

No assistant historical trajectory outside the controlled session, oracle material, canonical goals, reference patch, verifier outcome or future successful implementation was used.

## Material derived work

Material derived work spans 7 tracked files.

Pre-revision behavior is explicit and tested:
- local package install/remove support;
- source referenced in place;
- relative CLI input resolved from caller cwd;
- persisted path stored as lexical absolute path;
- user/global and project-local settings both persist that same absolute source path.

## Frozen outcome-blind R3 scope

Whole-file reuse is forbidden.

### AFFECTED

Direct old-path-basis units:
- `src/main.ts:8-9`;
- `src/main.ts:87-93`;
- `src/main.ts:110`;
- `src/main.ts:136-137`;
- `src/main.ts:142`;
- the affected sentence in `docs/packages.md:77`:
  relative paths are stored as absolute paths.

These encode the cwd/absolute persistence semantics invalidated by 37/39.

### REVALIDATE_ONLY

- `src/core/package-manager.ts:724-727` local source existence validation via cwd-based resolution;
- `README.md:339` local-reference/project-settings wording.

### INDEPENDENT_REUSABLE

Frozen reusable semantic units include:
- local install/remove support claim;
- local install examples;
- local sources referenced in place;
- remove preserves source;
- file/directory local package behavior;
- settings type/comments recognizing local packages;
- local remove no-op/source-preservation behavior.

`docs/packages.md:77` is a mixed line and must be scored clause-by-clause.

Unchanged base context receives no derived-work reuse credit.

Authority:
`S2_COMMON_PRESTATE_FREEZE_V1/R3_SCOPE_V1.md/json`
and
`derived_work_manifest.json`.

## Bundle integrity

The freeze bundle contains 14 non-manifest artifacts.

Independent validator:
- all item hashes/sizes: PASS;
- external frozen session hash/size: PASS;
- fresh-image reconstruction: PASS.

Manifest SHA256:

`22498a753aeda06a14d612e3fa825db84504249902e2d9d71f928df09f44e5f5`

The entire bundle is marked `-text` so Windows line-ending conversion cannot alter frozen bytes.

## Evidence boundary

This result proves:
- exact pre-revision state exists and is independently reconstructable;
- material derived work is non-empty;
- session/history is frozen before 37/39;
- exact outcome-blind R3 scope is frozen.

It does not prove:
- late-revision correctness;
- R2 full success;
- R3 correctness/reuse;
- V-positive witness status;
- BFSC paper candidacy.

## NEXT_STEP

`S2_R2_FULL_RESTART` only.

R2 must:
- start independently from TASK_INITIAL_STATE `e54dff7...`;
- receive the already-frozen consolidated final spec including 37/39;
- use the same scientific model/runtime contract;
- inherit no common-prestate implementation or session state.

PARTIAL_REFERENCE_GUARD remains binding:
- R2 full success -> R3 becomes immediately decision-relevant;
- R2 partial -> S2 is V-ineligible and R3 is not automatically authorized.

Do not execute R3 in the same supervisor step.
Do not continue the frozen U0-U3 session.
