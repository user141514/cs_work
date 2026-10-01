# S2 Common Prestate WSL-Native Substrate V1

date: 2026-10-01
status: PASS_WSL_NATIVE_RUNTIME_AUTH_READY__U0_RETRY_NEXT
task: pi-mono-auto-a4fca584
model_calls: 0

## Why this substrate exists

The first common-prestate attempt was invalid because OMP tool execution occurred on the Windows host against Linux task dependencies.

A persistent Docker-container route then reproduced the official Linux task runtime, but scientific OMP could not resolve the host's command-backed openai-codex credential without moving credential state into the container. That route produced no scientific session and no project mutation.

The authoritative repaired path is therefore WSL-native Linux execution:
- task repo/runtime remain Linux;
- the host's existing command-backed Codex resolver is invoked through Windows interop;
- no OAuth database or provider credential file is copied into the Linux scientific environment.

## WSL identity

Distribution:
- Ubuntu 26.04
- x86_64
- glibc 2.43

Scientific user:
- `agent`
- uid 1001

Scientific repo:
`/home/agent/s2-common-pre-v3`

Repo source:
byte/mode-preserving tar stream from the exact locked official S2 Docker image.

Verified repo identity:
- HEAD `e54dff7efb460e364a39e4a22369991a20c105b9`
- clean status
- no task mutation during substrate preparation.

## Exact task runtime

Copied from the locked official task image rather than recreated approximately.

Runtime prefix:
`/opt/s2-runtime`

Verified:
- Node `v20.20.2`
- npm `10.8.2`
- task Bun `1.3.13`

These versions match `S2_RUNTIME_PREFLIGHT_V1`.

## OMP harness isolation

OMP is execution infrastructure, not task runtime.

Harness:
- `@oh-my-pi/pi-coding-agent@18.1.15`
- OMP `18.1.15`
- harness-only Bun `1.3.14`
- installed under separate `/opt/s2-omp` and `/opt/s2-omp-bun` prefixes.

The task PATH does not replace the frozen task Bun with the harness Bun.

## Command-backed Codex auth

Host authority already used by OMP:

`C:\Users\Administrator\.omp\agent\Get-OpenAICodexToken.ps1`

WSL OMP config uses the same resolver through Windows interop:

`/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe ... Get-OpenAICodexToken.ps1`

No provider access token, refresh token, auth database, or `.codex/auth.json` is copied into WSL.

Auth/model discovery validation:
- OMP `models openai-codex --json` completed successfully;
- the command path uses `discoverAuthStorage()`, refreshes the registry, then renders `modelRegistry.getAvailable()`;
- `openai-codex/gpt-5.6-sol` appears in the available model set.

This is a zero-generation auth-resolution check, not a scientific model turn.

## PI proxy transport

WSL cannot directly reach ChatGPT/OpenAI and cannot reach the host loopback proxy.

A temporary user-space TCP relay exposes the already-working host `127.0.0.1:7897` PI proxy to WSL at:

`http://172.20.208.1:17897`

Validation:
- WSL request to relay returns HTTP 400 from the upstream PI proxy;
- no Windows route, firewall, or system proxy was modified.

The relay is execution infrastructure only and must be rechecked before each scientific turn.

## Frozen input identity

The authoritative common-prestate source adapter and exact U0/U1/U2/U3 prompt files remain unchanged from `S2_COMMON_PRESTATE_RUN_V1.md`.

No late-revision 37/39 input has been delivered.

## Superseded operational paths

- U0-v1 Windows-tool-runtime attempt: INVALID, frozen separately.
- Docker-native OMP launch attempts after substrate repair: launch-only failures before scientific session creation because container OMP lacked the host command-backed Codex credential path.
- Those attempts produced no scientific session and no task-repo effect.

They are operational evidence only.

## Decision

`S2_COMMON_PRESTATE_WSL_SUBSTRATE = PASS`

The next scientific object is:

`S2_COMMON_PRESTATE_U0_RETRY`

It must:
- start a fresh WSL-native OMP session;
- use GPT-5.6 Sol / xhigh;
- deliver only exact U0/index=0 with the frozen issue adapter;
- preserve analysis-only zero project mutation.

Do not deliver U1 in the same supervisor step.
