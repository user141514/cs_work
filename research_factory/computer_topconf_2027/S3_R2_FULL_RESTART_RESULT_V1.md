# S3 R2 Full-Restart Result V1

date: 2026-10-01
status: VALID_EXECUTION__PARTIAL_CORRECTNESS__REWARD_0_7650__R3_NEXT
task: pi-mono-auto-93c17d3b
arm: R2_FULL_RESTART

## Decision

`S3_R2_FULL_RESTART = VALID_PARTIAL`

R2 is a valid, executable FULL_RESTART arm but **does not reach full frozen-verifier success**.

Final official verifier reward:

`0.7650`

This is not a runtime INVALID and is not eligible for parameter/implementation rescue after outcome observation.

The next pre-registered scientific arm remains:

`S3_R3_ORACLE_SCOPED`

No R3 execution occurred in this R2 step.

## Isolation / identity

R2 started from a fresh DevSpace worktree at:

`5133697bc454da5595cf4b0c70d3c2c725677`

The older local S3 base checkout was rejected because it already contained a historical untracked extension. A new detached worktree was created directly from the exact base commit.

R2 start:
- clean tracked/untracked state;
- detached exact base;
- 0 remotes;
- 0 local heads;
- 0 tags;
- new session directory `D:/cs_work/external/spec_stageb_sessions/s3_r2_full_v1`;
- no common-prestate artifact or session inherited.

Frozen prompt:
`S3_R2_FULL_RESTART_PROMPT_V1.txt`

SHA256:
`cbcdd757cbcec0bb4e1118487f9a964ad990b605ad86c195dac03265d86b1551`

The native OMP transcript contains one user turn: the ordinary `@file` wrapper around that exact prompt file.

Observed agent identity:
- `openai-codex/gpt-5.6-sol`;
- xhigh;
- fallback=false;
- no skills/rules/extensions/title call;
- tools = read,bash,edit,write,grep,glob.

A scan of assistant tool-call arguments found zero path/command references to the forbidden result/solution sources checked for RESEARCH-01, reference/gold, canonical goals, hidden verifier result, common-prestate, R3 scope or Phase-B artifacts.

## R2 output

Final scientific worktree:
- HEAD remains exact base;
- tracked diff: empty;
- only untracked task artifact:
  `.pi/extensions/signal-ui.ts`.

Artifact:
- lines: 139;
- bytes: 4,049;
- SHA256: `886a067d86e30d220fcc5a6fa4884ce81cef4c6ab91746406198c203625a5673`.

An exact byte copy is stored under:
`S3_R2_FULL_RESTART_SNAPSHOT_V1/artifacts/.pi/extensions/signal-ui.ts`.

During `npm run check`, repository-wide formatting/line-ending churn temporarily appeared across many tracked files. The agent inspected it and restored only formatter-induced worktree changes before completion. Independent final inspection confirms tracked diff = 0 and only `signal-ui.ts` remains.

## Agent-side checks

The arm reported and its session records show:

- dedicated lifecycle smoke: PASS;
  - inactive before `/start`;
  - hidden protocol message;
  - separate input/done transitions;
  - combined input+done ignored;
  - widget remains open through 20 intervening completed messages;
  - duplicate input/ordinary output does not recreate widget;
  - later done closes;
  - no `message_update` handler;
- dedicated Biome check: PASS;
- dedicated TypeScript check: PASS;
- `npx tsgo --noEmit`: PASS;
- isolated CLI load with `--no-extensions -e .pi/extensions/signal-ui.ts --help`: PASS;
- repository-wide `npm run check`: reached pre-existing/unrelated `packages/web-ui` dependency/type errors; no final tracked formatter residue;
- live TUI keystroke test: unavailable because local CLI had no configured model.

These checks are supporting evidence only. Scientific correctness is the official frozen verifier below.

## Official frozen verifier

Task metadata SHA256:
`4676cc1660709cd1da6030a9e1e47cebc741409e96b8fb19ddbf1fc7d4d6c8e3`

Normalized official verifier SHA256:
`b64d2ffa9e79d382e46fcd2d3f87ede26a9f04fabb4328e4a9f39bc4f89576ee`

Exact official image:
`sha256:4805e21fa2f3d38ed5dacc320ec0400b3fd402194051124b3a8a85cf826455fa`

The host verifier was not modified. The same preflight transport normalization removed CR characters only inside the ephemeral container.

Verifier gates:

- F2P command + message handler: PASS
- F2P protocol injected: PASS
- F2P reaction observed: PASS
- F2P distinct signal kinds: **FAIL**
- F2P inactive-before-activation: PASS
- F2P token-pattern/no-tool registration: PASS
- upstream canonical file exists: **FAIL**
- upstream canonical extension loadable: **FAIL**
- P2P extensions directory: PASS
- P2P existing `tps.ts` compiles: PASS

Inner reward before upstream adjustment:
`0.85`

Final reward:
`0.7650`

### Failure interpretation

The decisive behavioral miss is Gate 4: the frozen verifier's candidate roundtrip did not observe distinct open/close reactions. R2 uses `[[SIGNAL_INPUT]]` and `[[SIGNAL_DONE]]`; its open token does not match the verifier's tested open-token candidates.

The two upstream failures are due to the frozen verifier's canonical preferred filename `message-signal.ts`, while R2 independently chose `signal-ui.ts`. These upstream gates are informational but still reduce final weighted reward under the frozen verifier.

These observations are recorded, **not repaired**.

## Cost / work

Native OMP accounting:

- model calls: 54
- tool calls: 106
- mutating tool calls: 10
- noncached input+output tokens: 176,796
- reported model cost: $3.5202112
- wall span: 632.049 s
- input tokens: 151,625
- output tokens: 25,171
- cache-read tokens: 6,025,728
- reasoning tokens: 15,455

Session:
`2026-10-01T08-55-22-389Z_01a0f6ac-ea11-7000-a4b4-df734d0cc779.jsonl`

SHA256:
`666bdc1892a443d7cae819528c91925a90f9275eccc37373168e82da752fa9db`

## Frozen-rule interpretation

The S3 Execution Leverage Gate pre-registered:

`common prestate -> R2 -> R3`

and stops before R3 only when R2 is runtime-invalid/non-executable or an earlier prerequisite fails.

R2 here is valid/executable. Its partial correctness therefore does **not** authorize:
- R2 repair/retry;
- R0;
- R1;
- threshold changes.

It also does not complete the owned S3 decision, because local selective-rederivation headroom and preserved-work fraction require the already-frozen R3 arm.

Because R2 did not reach full verifier success, S3 cannot become a V-positive witness through a criterion that requires R2 full success unless later frozen-set logic says otherwise; do not reinterpret R2's 0.765 as success.

## NEXT_STEP

`S3_R3_ORACLE_SCOPED` only.

R3 must branch from the immutable post-U5 common-prestate bundle and use only the already-frozen outcome-blind semantic/file-hunk dependency scope. It must not receive R2 implementation details, verifier gate outcomes or this result as solution context.

Do not run R0/R1.
Do not repair or rerun R2.
