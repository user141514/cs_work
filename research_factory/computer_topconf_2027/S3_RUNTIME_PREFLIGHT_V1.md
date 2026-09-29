# S3 Runtime Preflight V1

date: 2026-09-30
status: AUTHORIZED_ZERO_MODEL_RUNTIME_PREFLIGHT
task: pi-mono-auto-93c17d3b
parent: S3_EXECUTION_LEVERAGE_GATE_V1.md
model_calls_authorized: false

## Owned decision

Can PC2 execute the exact official S3 task runtime/verifier path closely enough that a later controlled Stage-B common-prestate/R2/R3 run would be scientifically admissible?

This preflight owns runtime validity only. It cannot produce a BFSC scientific result.

## Frozen official assets

Docker image:
`ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-93c17d3b:2f7d1992e60d`

TASK_INITIAL_STATE:
`5133697bc454da5595655cf4b0c70d3c2c725677`

Official verifier:
- `tests/test.sh`
- SHA256: `2d06c9a791d7e2d6785711f14bf8bc3657b3dcc13049e5566d48adfb6706c046`

Verifier manifest:
- `tests/test_manifest.yaml`
- SHA256: `a29b160939ea5abbef70987b9852b87c8f2fe00f07c39074b3b9054fa07a7e2f`

Official task.toml:
- SHA256: `4676cc1660709cd1da6030a9e1e47cebc741409e96b8fb19ddbf1fc7d4d6c8e3`

Official Dockerfile:
- SHA256: `1c9f85e457efd7fdee80c2b81c5d9b3c8cd620addad86a9b8056b9b9225dca40`

## PASS criteria

All must pass without any model/agent call:

R1. Docker Desktop daemon is reachable from the already-installed Docker CLI.

R2. The exact official S3 image is locally inspectable after bounded acquisition:
- use existing local image if present;
- otherwise one direct pull of the exact frozen image is allowed;
- no substitute image after a pull failure.

R3. Container runtime identity:
- image starts successfully;
- `/workspace/pi-mono` exists;
- Git HEAD is exactly TASK_INITIAL_STATE;
- `node` and `bun` are available;
- `package.json`, `.pi`, and `packages/coding-agent` exist.

R4. Official verifier path executes inside that exact image:
- mount/copy only the frozen official verifier files;
- run `tests/test.sh` without any agent-produced patch;
- verifier exits through its own finalize path and writes `/logs/verifier/reward.txt` plus gate output;
- baseline reward is expected to be 0 because no task solution is present and is **not** a scientific negative.

R5. No scientific state mutation:
- no GPT/Codex/Claude/OMP provider run;
- no common prestate;
- no R0/R1/R2/R3 arm;
- no edits inside a scientific checkout retained as evidence.

## Verdicts

- `PASS_RUNTIME_READY`: R1-R5 pass.
- `IMAGE_ASSET_BLOCKED`: daemon works but exact image cannot be acquired under the one direct frozen path.
- `RUNTIME_INVALID`: image starts but exact checkout/tool/verifier contract cannot execute.
- `DAEMON_NOT_READY`: installed Docker runtime cannot be started/reached in this bounded preflight.

## Handoff

Only `PASS_RUNTIME_READY` may authorize the already-frozen paid sequence:

`COMMON_PRESTATE -> R2_FULL_RESTART -> R3_ORACLE_SCOPED`

This preflight itself must stop before any model call.
