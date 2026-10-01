# S2 Common Prestate Run V1

date: 2026-10-01
status: U0_V1_INVALID_RUNTIME__WSL_SUBSTRATE_READY__U0_RETRY_NEXT
task: pi-mono-auto-a4fca584

## Historical U0-v1 checkout — INVALID runtime trajectory

`D:/cs_work/external/spec_stageb_s2_base_e54dff7`

HEAD:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Checkout admission:
- clean after checkout-local `core.filemode=false`;
- exported byte-for-byte from the locked official Docker image;
- 0 remotes;
- 0 local heads;
- 0 tags;
- node_modules present from the official image.

## U0-v1 invalid session

Session directory:
`D:/cs_work/external/spec_stageb_sessions/s2_common_pre_v1`

This session is frozen as `INVALID_RUNTIME_SUBSTRATE__NO_PROJECT_EFFECT` and must never be continued. Authority: `S2_COMMON_PRESTATE_U0_INVALID_V1.md/json`.

## Authoritative WSL-native substrate for retry

Scientific project:
`/home/agent/s2-common-pre-v3`

Frozen task runtime:
- WSL Ubuntu 26.04 / x86_64
- user `agent` uid 1001
- exact clean HEAD `e54dff7efb460e364a39e4a22369991a20c105b9`
- Node v20.20.2
- npm 10.8.2
- task Bun 1.3.13
- task repo/runtime bytes copied from the locked official Docker image with Linux modes preserved

OMP harness:
- OMP 18.1.15
- harness-only Bun 1.3.14 under separate `/opt/s2-omp*` prefixes
- host command-backed `openai-codex` resolver invoked through Windows interop
- credential files are not copied into WSL
- PI proxy reached through temporary user-space relay at `http://172.20.208.1:17897`

Auth/model discovery:
- `omp models openai-codex --json` uses `discoverAuthStorage()` + `ModelRegistry.getAvailable()`
- available set includes `openai-codex/gpt-5.6-sol`

The previous persistent Docker container remains runtime-donor/repair evidence only and is not the authoritative scientific execution substrate.

Authority: `S2_COMMON_PRESTATE_WSL_SUBSTRATE_V1.md/json`.

Agent identity:
- `openai-codex/gpt-5.6-sol`
- xhigh
- OMP 18.1.15
- tools: read,bash,edit,write,grep,glob
- auto-approve
- no skills/rules/extensions/title

## Source-availability adapter

Historical user index 0 points to a GitHub URL that returns 404 at replay time.

To preserve the historical public requirement source without changing the user message, U0 alone appends this frozen context to the system prompt:

`S2_COMMON_PRESTATE_SOURCE_ADAPTER_V1.md`
SHA256:
`cb67aec5cc4ccae4e8f0beaaf414b5c8399909e0fe02882a598d385c8d67b6a4`

The adapter contains only public issue 1216 + linked issue 1207 requirement context. It contains no solution/reference/verifier/oracle/post-outcome evidence.

The adapter is context-only and is not a scientific user turn.

## Controlled turns

U0:
- source message index 0
- prompt file `s2_arm_prompts/S2_COMMON_PRE_U0.txt`
- SHA256 `fb2568144b28f27af54954482a3d2aa843a66459ebcd9a2d73bc0aa781c763c6`

U1:
- source message index 6
- SHA256 `74c374b1a0c3d522a9b1d90cb92e23be569c721940def088461198f378b8db89`

U2:
- source message index 8
- SHA256 `ee45029de3b053c1f648c1339ec7b6a60936a2119f2f98740c89adb62b6fc747`

U3:
- source message index 20
- SHA256 `cebe7791d109d74047ebd025ca82f546c64111c4acaab6e9dda0a4b82bf55de0`

Authoritative delivery after runtime repair:
`U0-retry -> U1 -> U2 -> U3`
through the same fresh v2 durable session using `--continue`.

Do not deliver late revision indices 37/39.

## Stop/freeze rule

After U3 completes:
- stop all scientific turns;
- verify exact session identity and four user turns;
- freeze project/session/artifact bytes;
- classify exact R3 affected/revalidate/independent scope outcome-blind;
- if no material derived work exists, mark reuse NONIDENTIFIABLE.

R2/R3/R0/R1 are not authorized in this run.
