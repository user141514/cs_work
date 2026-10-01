# S2 Common Prestate U3 Result V1

date: 2026-10-01
status: PASS_PRE_REVISION_VERIFICATION__COMMON_PRESTATE_FREEZE_NEXT
task: pi-mono-auto-a4fca584
scope: common-prestate U3 / source_message_index 20 only

## Decision

`S2_COMMON_PRESTATE_U3 = PASS`

The entire controlled pre-revision sequence U0/U1/U2/U3 is now complete.

No late-revision text from source indices 37/39 has been delivered.

## Scientific identity

Repo:
`/home/agent/s2-common-pre-v3`

Base HEAD:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Final post-U3 worktree:
- same 7 tracked modified files as U2;
- 0 untracked files;
- 0 temporary smoke directories;
- no commit;
- `git diff --check`: PASS.

Final patch:
- bytes: 8,292;
- SHA256:
  `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`.

This is byte-identical to the post-U2 patch.

Therefore U3 verified the pre-revision implementation without changing it.

## Input / session integrity

Frozen source message index:
`20`

Verbatim:
`try it with pi-test.sh. i'm especially curious what happens with relative paths. are they resolved to absolute paths in settings.json?`

Prompt SHA256:
`cebe7791d109d74047ebd025ca82f546c64111c4acaab6e9dda0a4b82bf55de0`

Observed scientific user turns:
1. exact U0/index=0;
2. exact U1/index=6;
3. exact U2/index=8;
4. exact U3/index=20.

No U4a/U4b late-revision messages 37/39 were delivered.

Session ID:
`01a0f7cc-4a3e-7000-8639-ae33f7a25a58`

Post-U3 session SHA256:
`27de34edff19712f382c5086bfc96adc123b04a00f32618f89b8ea847e850000`

Session size:
- 2,037,536 bytes;
- 217 JSONL lines.

Lifetime:
- request key: `s2-common-pre-u3-wsl-v1`;
- turn id: `turn_deaa2372acd24b03b7ea921b2ccd9c0c`;
- exit code: 0;
- outcome: succeeded;
- terminal/quiescent: true;
- wall span: 91.820 s.

Model/runtime:
- `openai-codex/gpt-5.6-sol`;
- fallback=false;
- thinking=`xhigh`;
- Node `v20.20.2`;
- task Bun `1.3.13`;
- OMP `18.1.15`;
- harness Bun `1.3.14`.

## U3 verification result

U3 uses `pi-test.sh` against the existing U2 implementation.

### Global/user-scope path

Command shape:
`./pi-test.sh install packages/coding-agent/examples/extensions/commands.ts`

Observed settings entry:
`/home/agent/s2-common-pre-v3/packages/coding-agent/examples/extensions/commands.ts`

Equivalent input with a leading `./` does not create a duplicate.

### Project-local path

From a temporary project directory:

`../pi-test.sh install -l ../packages/coding-agent/examples/extensions/commands.ts`

Observed project `.pi/settings.json` entry:
the same absolute source path.

### Removal

Global and project-local remove through equivalent relative paths:
- remove the settings entry;
- preserve the source file.

### Current pre-revision path basis

The verified rule is:

> relative local-package paths are resolved against the caller's current working directory and persisted as lexical absolute paths.

They are not resolved relative to:
- the directory containing `pi-test.sh`;
- the destination `settings.json`;
- the settings-file directory.

This is precisely the pre-revision semantic state that later source messages 37/39 are designed to change.

## No post-U2 implementation mutation

U3 incremental mutating edit/write calls:
`0`

Final patch SHA256 equals the post-U2 patch SHA256.

No temporary smoke directory remains in the project.

## Late-semantic exclusion

Outcome-blind scan of final source/docs found no:
- `relative to settings.json`;
- settings-file-relative rule;
- settings-file-directory path basis.

Therefore the late semantic correction has not leaked into the common prestate.

## Forbidden-source boundary

Supervisor scan of U3 tool-call arguments found zero references to:
- reference/gold patch;
- canonical goals;
- oracle session/intents;
- R2/R3 result material;
- RESEARCH-01 Phase-B;
- verifier result.

## Accounting

U3 incremental accounting:
- model calls: 13;
- tool calls: 15;
- mutating edit/write calls: 0;
- input tokens: 6,933;
- output tokens: 2,392;
- cache-read tokens: 2,510,848;
- reasoning tokens: 1,278;
- reported cost: $1.0799112.

## Scientific consequence

The common-prestate trajectory is now complete through all frozen pre-revision user requirements.

Material derived work exists and the load-bearing stale path-basis semantics are both:
- implemented;
- directly verified through the user's requested pi-test.sh workflow.

The scientific session must not receive any further user turn before the immutable common-prestate freeze and outcome-blind exact R3 scope are materialized.

## NEXT_STEP

`S2_COMMON_PRESTATE_FREEZE_V1` only.

Freeze:
- exact base/HEAD identity;
- final tracked patch bytes;
- untracked/deletion manifests;
- final U0-U3 session bytes/hash;
- runtime/auth/input receipts;
- derived-work manifest;
- exact outcome-blind affected/revalidate/independent R3 scope;
- one manifest hashing all freeze artifacts.

Do not deliver 37/39 before that freeze is complete.
Do not start R2/R3/R0/R1.
