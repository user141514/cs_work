# S3 Runtime Preflight Resume Result V2

date: 2026-10-01
status: PASS_RUNTIME_READY
task: pi-mono-auto-93c17d3b
parent:
- S3_RUNTIME_PREFLIGHT_V1.md
- S3_RUNTIME_PREFLIGHT_RESULT_V1.md
- S3_RUNTIME_PREFLIGHT_RECHECK_20260930.md
model_calls_made: 0
paid_model_authorized_now: false

## Recovery from prior blocker

The previous preflight stopped at `DAEMON_NOT_READY` because the old Docker Desktop installation was incomplete.

After user repair/reinstall, Docker Desktop is now installed under:

`E:/DockerDesktop`

Observed running components:
- Docker Desktop frontend;
- `com.docker.backend`;
- `com.docker.service`;
- Docker build backend.

Docker Engine is now reachable.

## R1 — Docker daemon

PASS.

Docker client:
- version: 29.8.0
- context: `desktop-linux`

Docker server:
- Docker Desktop 4.91.0 (239619)
- Engine: 29.8.0
- OS: linux
- arch: amd64
- kernel: `6.18.40.1-microsoft-standard-WSL2`

## R2 — exact official image

PASS.

Exact frozen image:

`ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-93c17d3b:2f7d1992e60d`

Pulled/inspected locally as:

`sha256:4805e21fa2f3d38ed5dacc320ec0400b3fd402194051124b3a8a85cf826455fa`

Identity:
- OS: linux
- arch: amd64
- size: 3,334,974,820 bytes
- created: 2026-06-07T21:37:13.048793442Z

No substitute image was used.

## R3 — container runtime identity

PASS when executed as the image's intended non-root `agent` user.

Observed:
- user: `agent`
- uid: 1001
- Git HEAD:
  `5133697bc454da5595655cf4b0c70d3c2c725677`
- working tree: clean
- Node: `v20.20.2`
- Bun: `1.3.13`
- `package.json`: present
- `.pi`: present
- `packages/coding-agent`: present

A root-user probe triggered Git's expected `dubious ownership` protection because the Dockerfile chowns the repo to `agent`; this was not treated as a runtime failure. The admissible identity check uses `--user agent` and passes without modifying Git safe-directory configuration.

## R4 — official verifier baseline

PASS for runtime execution.

The Windows-host copy of `tests/test.sh` is stored with CRLF line endings. Direct bind-mounted execution in Linux therefore fails at Bash parsing before verifier logic runs.

For runtime validation only, the same frozen script was transformed **inside the ephemeral container** by removing carriage returns (CRLF -> LF), with no host-file mutation and no logical verifier change.

Normalized verifier SHA256:

`b64d2ffa9e79d382e46fcd2d3f87ede26a9f04fabb4328e4a9f39bc4f89576ee`

Baseline execution with no agent patch produced:

`reward = 0.0000`

Expected F2P baseline failures:
- new extension absent;
- extension loadable gate absent.

Runtime/P2P checks:
- `.pi/extensions` directory: PASS
- existing `tps.ts` compiles with Bun: PASS

This establishes that the exact image, repository/toolchain and verifier logic can execute locally. Baseline reward 0 is expected and is not a BFSC scientific negative.

## R5 — no scientific state mutation

PASS.

This resume preflight performed:
- zero GPT/Codex/Claude/OMP provider/model calls;
- zero common-prestate generation;
- zero R0/R1/R2/R3 scientific arms;
- zero retained mutation of a scientific checkout.

## Final verdict

`S3_RUNTIME_PREFLIGHT_V1 = PASS_RUNTIME_READY`

The previous `DAEMON_NOT_READY` result is preserved as historical operational evidence; it is not rewritten.

Runtime admission is now complete.

## Exact next step — not executed

The already-frozen first paid step is now eligible:

`S3_COMMON_PRESTATE`

After the immutable common prestate and exact outcome-blind R3 file/hunk scope are frozen:

`R2_FULL_RESTART -> R3_ORACLE_SCOPED`

R0 remains conditional on R3-vs-R2 headroom surviving.
R1 remains not authorized for symmetry.

No paid/model execution was started in this runtime-preflight turn.
