# S3 Common Prestate U1 Invalid Run V1

date: 2026-10-01
status: INVALID_SUPERVISOR_INTERRUPTION
task: pi-mono-auto-93c17d3b
scope: S3_COMMON_PRESTATE U1 only

## What happened

The first scientific U1 attempt used the frozen identity correctly:
- OMP 18.1.15;
- openai-codex/gpt-5.6-sol;
- xhigh;
- tools read,bash,edit,write,grep,glob;
- exact frozen U1 user message;
- one durable session JSONL.

During U1 the agent ran:

`npm run check`

which invokes:

`biome check --write --error-on-warnings . && tsgo --noEmit && cd packages/web-ui && npm run check`

The formatter temporarily touched many tracked files. The agent then explicitly attempted to revert formatter-only changes with:

`git diff --binary | git apply --reverse`

A supervisor audit saw a large transient `git status` listing with CRLF warnings and incorrectly treated it as persistent checkout contamination, then externally killed the still-running OMP process.

Post-stop forensic audit showed:
- `git diff --name-only` count = 0;
- `git ls-files -m` count = 0;
- tracked worktree was already clean;
- only agent-created untracked file remained: `.pi/extensions/start.ts`.

Therefore the agent/model did **not** fail the scientific task at this point. The run is invalid solely because the supervisor terminated it before normal/quiescent completion.

## Frozen invalid evidence

Session:
`D:/cs_work/external/spec_stageb_sessions/s3_common_pre_v1/2026-10-01T06-30-37-691Z_01a0f628-657c-7000-9edc-85d0a4cc338e.jsonl`

Session SHA256:
`f05fc364cb0ecfd2527bb19064155ded01e425ee328904fdd7760811956a8367`

Session exit records:
`0`

Accounting:
- model calls: 14
- tool calls: 38
- mutating tool calls: 1
- input tokens: 120343
- output tokens: 8186
- cache-read tokens: 862592
- reasoning tokens: 5335
- reported cost: $0.9901288
- observed wall span: 190.717 s

This cost is retained as invalid execution overhead and excluded from the S3 scientific result denominator.

## Decision

Do not continue this session.

Restart the exact same U1 from:
- a fresh detached S3 checkout;
- a fresh empty session directory;
- the same frozen U1 prompt;
- the same OMP/model/thinking/tools configuration.

No prompt repair or agent restriction is introduced from this invalid run.
