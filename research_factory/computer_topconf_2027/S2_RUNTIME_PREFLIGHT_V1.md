# S2 Runtime Preflight V1

date: 2026-10-01
status: PASS_RUNTIME_READY__COMMON_PRESTATE_NEXT
task: pi-mono-auto-a4fca584
model_calls: 0

## Decision

`S2_RUNTIME_PREFLIGHT_V1 = PASS_RUNTIME_READY`

The exact official S2 runtime is locally available and executable.

This preflight used zero model calls and does not constitute a scientific arm.

## Official runtime identity

Image:
`ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-a4fca584:d1a6ee81ebeb`

Pulled/locked digest:
`sha256:24df21b472314647843bab5009a4f5b443a129e7bd42904936e0176277bf8148`

Docker:
- client: 29.8.0
- server: 29.8.0
- server OS/arch: linux/amd64

Container identity:
- configured user: `agent`
- runtime user: `agent`
- uid: 1001
- Node: `v20.20.2`
- Bun: `1.3.13`

Repository:
- HEAD: `e54dff7efb460e364a39e4a22369991a20c105b9`
- expected TASK_INITIAL_STATE: same
- clean status
- remote_count: 0
- head_ref_count: 0
- tag_ref_count: 0

Thus the official image satisfies the frozen base/runtime identity.

## Image-pull transport repair

Initial host pull attempts exposed two wrapper-level issues:
1. Docker CLI could not find `docker-credential-desktop` because the Docker resources/bin directory was absent from PATH.
2. Wrapper-based durable attempts returned non-dispositive process receipts because PowerShell native exit propagation / Git-Bash argument conversion did not prove image materialization.

Neither is scientific evidence.

The valid transport was:
- add `E:\DockerDesktop\resources\bin` to the child PATH;
- launch `docker.exe pull` directly with PowerShell `Start-Process`;
- wait for process exit;
- independently verify the image by `docker image inspect`.

The final pull receipt reported:
- digest `sha256:24df21b4...8148`;
- `Image is up to date`;
- stderr empty.

Completion evidence is the independent image inspection above, not wrapper exit status.

## Frozen verifier identity

Official task metadata:
- `task.toml` SHA256: `ef07e5601a1ea034f91613826367ec003154ab6a7ff4f86249641a940509e6f3`

Normalized official verifier:
- CRLF removed only inside the ephemeral Linux container;
- normalized `tests/test.sh` SHA256:
  `cefe818bfb78d67eead6662a375387a6b350603016c2775e39affa97cfa5874a`

The host verifier file was not modified.

## No-patch verifier baseline

The exact official image, with no task patch applied, executes the frozen verifier to completion.

Final baseline reward:
`0.0000`

Observed baseline gates:
- existing package-manager P2P test suite: PASS (41/41)
- F2P local-install behavior: FAIL, as expected for the unfixed base task
- upstream local-install tests: FAIL/not present on base
- upstream test-count >91: FAIL on base
- upstream P2P package-manager tests: PASS
- upstream P2P scoped tsgo gate: FAIL with `TS5112`
- upstream P2P Biome gate: PASS

The `TS5112` baseline failure is a property of the frozen verifier command against this base/runtime and is retained as baseline evidence. It does not prevent the verifier from executing or producing a deterministic task reward and therefore is not treated as runtime INVALID.

Do not repair or alter the verifier.

## Runtime-admission conclusion

Confirmed:
- exact official image exists locally;
- exact frozen base commit;
- correct non-root runtime user;
- expected Node/Bun toolchain;
- isolated Git state with no future refs/remotes;
- official verifier executes under the exact image;
- deterministic no-patch reward is 0.0000.

Therefore the runtime prerequisite from `S2_EXECUTION_LEVERAGE_GATE_V1` is satisfied.

## Execution authorization

The next paid object is now authorized:

`S2_COMMON_PRESTATE` only.

Purpose:
- deliver the frozen controlled pre-revision requirement sequence 0/6/8/20 once;
- persist the resulting scientific prestate under the fixed GPT-5.6 Sol/xhigh identity;
- freeze exact task artifacts/session;
- freeze exact outcome-blind R3 affected/revalidate/independent scope.

Do not deliver the late revision 37/39 in the common-prestate step.
Do not start R2/R3/R0/R1 in the same supervisor turn.
