# S2 Common Prestate U2 Result V1

date: 2026-10-01
status: PASS_PRE_REVISION_IMPLEMENTATION__MATERIAL_DERIVED_WORK__U3_NEXT
task: pi-mono-auto-a4fca584
scope: common-prestate U2 / source_message_index 8 only

## Decision

`S2_COMMON_PRESTATE_U2 = PASS`

U2 is the first valid implementation turn of the S2 common-prestate trajectory.

It creates material pre-revision derived work under the still-frozen pre-revision path semantics.

## Scientific identity

Repo:
`/home/agent/s2-common-pre-v3`

Base HEAD remains:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Final worktree after U2:
- 7 tracked modified files;
- 0 untracked files;
- no commit;
- `git diff --check`: PASS.

Modified files:
- `packages/coding-agent/CHANGELOG.md`
- `packages/coding-agent/README.md`
- `packages/coding-agent/docs/packages.md`
- `packages/coding-agent/docs/settings.md`
- `packages/coding-agent/src/core/package-manager.ts`
- `packages/coding-agent/src/core/settings-manager.ts`
- `packages/coding-agent/src/main.ts`

Diff:
- 30 insertions;
- 8 deletions;
- binary patch bytes: 8,292;
- patch SHA256:
  `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`.

## Input / session integrity

Frozen source message index:
`8`

Verbatim:
`oki, implement concisely`

Prompt SHA256:
`ee45029de3b053c1f648c1339ec7b6a60936a2119f2f98740c89adb62b6fc747`

Observed scientific user turns:
1. exact U0/index=0;
2. exact U1/index=6;
3. exact U2/index=8.

No U3 or late revision 37/39 was delivered.

Session ID:
`01a0f7cc-4a3e-7000-8639-ae33f7a25a58`

Post-U2 session SHA256:
`bc039ce82b8b5d2ae222ac7c96a050b44fb7bffdcdb3864a0fd3845e4a5e4424`

Session size:
- 1,961,019 bytes;
- 172 JSONL lines.

Lifetime:
- request key: `s2-common-pre-u2-wsl-v1`;
- turn id: `turn_02047112a3254160b52b6d05f205c17d`;
- exit code: 0;
- outcome: succeeded;
- terminal/quiescent: true;
- wall span: 288.081 s.

Model/runtime:
- `openai-codex/gpt-5.6-sol`;
- fallback=false;
- thinking=`xhigh`;
- Node `v20.20.2`;
- task Bun `1.3.13`;
- OMP `18.1.15`;
- harness Bun `1.3.14`.

## Pre-revision implementation state

U2 implements issue-1216 local package support under the agent's pre-revision interpretation.

Load-bearing implementation semantics now present:

1. Local paths are accepted as package sources.
2. The local path is validated for existence.
3. Local packages are referenced in place rather than copied/installed/deleted.
4. `pi remove <local-path>` removes only the settings entry.
5. Equivalent relative/absolute inputs are normalized for matching.
6. **Relative CLI paths are resolved to lexical absolute paths before persistence.**

The code path establishing that semantic state is visible in `packages/coding-agent/src/main.ts` via `resolveLocalPackagePath(...)`, which uses path resolution before the settings entry is stored.

User-facing docs also explicitly state:

> Relative paths passed to `pi install` are stored as absolute paths.

Outcome-blind scan found no `settings.json-relative`, settings-file-directory, or equivalent late-revision semantics in the final U2 source/docs.

Therefore U2 has materialized exactly the stale path-basis state needed for the later revision experiment.

## Artifact receipts

Post-U2 file SHA256:

- `CHANGELOG.md`: `9b9a48ae82a389c886717b03957fbd7389800973fbafbc9f3d08d15c862c631f`
- `README.md`: `1cadf59bb5864959e3c45c0594507315c1ea6e3d69691a003cb03a371a2ff70a`
- `docs/packages.md`: `458f8535c36c0db3fdfb4954e02970f9c1cf45b54fcafd0b7bd2289a9d92bc89`
- `docs/settings.md`: `4c4042c344ab1e93e76a3c041e34cb52812a3f552537c87116036da60b72b6a3`
- `src/core/package-manager.ts`: `5ec392966ca1caf1c4fc47f00d2eb9956bed3ad754f901043b207f287266f6b8`
- `src/core/settings-manager.ts`: `3b7431539980cad3e68ec3ebe8017d96dbc0f17a5370b217e1a146718fe746f5`
- `src/main.ts`: `54db7ccc7fc2407f33998550ace7a3d791541b623b6d75be7ff519fddeeb15d8`

These are receipts only.
The authoritative immutable common-prestate freeze still occurs after U3.

## Verification actually performed by the scientific agent

Observed smoke behavior:

- relative local extension install succeeds;
- temporary settings file stores the absolute source path;
- package can be listed from another working directory;
- local remove removes the settings entry;
- source file remains intact after remove;
- missing local source fails with `Local package not found`.

Workspace check:

`npm run check`

Observed:
- root Biome stage completed; one file was formatted;
- root `tsgo --noEmit` passed;
- web-ui Biome stage passed;
- web-ui TypeScript then failed because base checkout lacks built artifacts/types for `@mariozechner/pi-agent-core` / `@mariozechner/pi-ai`.

That final web-ui failure is retained as an environment/check boundary, not silently promoted to a U2 correctness PASS or scientific negative.

No task test suite was run because the agent followed the repository policy requiring explicit instruction before running tests.

## Forbidden-source boundary

Supervisor scan of U2 assistant tool-call arguments found zero references to:
- reference/gold patch;
- canonical goals;
- oracle session/intents;
- R2/R3 result material;
- RESEARCH-01 Phase-B;
- verifier result.

U2 receives no late-revision text.

## Accounting

U2 incremental accounting:
- model calls: 13;
- tool calls: 20;
- mutating edit/write calls: 2;
- input tokens: 310,396;
- output tokens: 7,201;
- cache-read tokens: 2,065,024;
- reasoning tokens: 4,997;
- reported cost: $2.2116136.

## Scientific consequence

Material derived work is now definitely non-empty.

Therefore S2 can no longer become reuse-NONIDENTIFIABLE merely because the pre-revision trajectory produced no implementation artifact.

This does not yet freeze the common prestate because U3/index=20 is still part of the pre-revision contract.

## NEXT_STEP

`S2_COMMON_PRESTATE_U3` only.

Deliver exact source_message_index=20 in the **same WSL-native durable session** using `--continue`.

U3 is a pre-revision verification turn and may inspect/test the current implementation.

Do not deliver late revision 37/39 in the same supervisor step.
