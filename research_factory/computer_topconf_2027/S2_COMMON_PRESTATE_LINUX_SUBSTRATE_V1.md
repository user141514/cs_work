# S2 Common Prestate Linux Execution Substrate V1

date: 2026-10-01
status: PASS_LINUX_SUBSTRATE_READY__U0_RETRY_NEXT
task: pi-mono-auto-a4fca584
model_calls: 0

## Goal

Run the scientific OMP agent inside the exact official Linux task image so all file/path/runtime behavior is evaluated on the same substrate as the frozen verifier.

## Container

Persistent container name:
`s2-common-pre-v2`

Current container ID:
`b4e431f5c3f4`

Base image:
`ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-a4fca584:d1a6ee81ebeb`

Image ID:
`sha256:24df21b472314647843bab5009a4f5b443a129e7bd42904936e0176277bf8148`

Task repo inside container:
`/workspace/pi-mono`

Verified:
- user: agent
- uid: 1001
- Node: v20.20.2
- task Bun on PATH: 1.3.13
- repo HEAD: e54dff7efb460e364a39e4a22369991a20c105b9
- repo status: clean
- host PI proxy reachable as `http://host.docker.internal:7897`
- host-bound session directory writable.

## OMP harness isolation

OMP 18.1.15 requires Bun >=1.3.14, while the task runtime is frozen at Bun 1.3.13.

The task Bun was **not upgraded**.

Instead:
- OMP package `@oh-my-pi/pi-coding-agent@18.1.15` is installed globally in the container;
- a separate harness-only Bun 1.3.14 is installed under `/opt/omp-bun` from the npm-distributed Linux binary package;
- OMP is launched explicitly with the harness Bun;
- PATH remains unchanged, so agent bash/tool commands continue to resolve the official task Bun 1.3.13.

Validated simultaneously:
- `bun --version` -> 1.3.13
- `/opt/omp-bun/node_modules/.bin/bun --version` -> 1.3.14
- harness invocation -> `omp/18.1.15`
- Node -> v20.20.2
- task repo exact/clean.

This isolates harness compatibility from task runtime semantics.

## Frozen input mounts

Host runtime input directory:
`D:/cs_work/external/spec_stageb_s2_inputs_v1`

Mounted read-only at:
`/inputs`

Hashes in container:
- source adapter: cb67aec5cc4ccae4e8f0beaaf414b5c8399909e0fe02882a598d385c8d67b6a4
- U0: fb2568144b28f27af54954482a3d2aa843a66459ebcd9a2d73bc0aa781c763c6
- U1: 74c374b1a0c3d522a9b1d90cb92e23be569c721940def088461198f378b8db89
- U2: ee45029de3b053c1f648c1339ec7b6a60936a2119f2f98740c89adb62b6fc747
- U3: cebe7791d109d74047ebd025ca82f546c64111c4acaab6e9dda0a4b82bf55de0

Fresh scientific session bind:
`D:/cs_work/external/spec_stageb_sessions/s2_common_pre_v2`
mounted at `/sessions`.

## Decision

`S2_COMMON_PRESTATE_LINUX_SUBSTRATE = PASS`

The invalid v1 session must not be continued.

Exact next step:
restart U0 from the clean container repo using a fresh v2 session, with the frozen issue adapter appended context-only.

Do not deliver U1 in the same supervisor step.
