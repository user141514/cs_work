# S2 Common Prestate Run V1

date: 2026-10-01
status: U0_U1_U2_U3_PASS__COMMON_PRESTATE_FROZEN__R3_SCOPE_FROZEN__R2_NEXT
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
`U0-v2 PASS -> U1 PASS -> U2 PASS -> U3 PASS`
through the same WSL-native durable session.

The scientific session is now permanently FROZEN for turn delivery. The immutable common-prestate bundle and exact outcome-blind R3 scope have been materialized; this session must never be continued.

U0-v2 authority:
- result: `S2_COMMON_PRESTATE_U0_RESULT_V2.md/json`
- session ID: `01a0f7cc-4a3e-7000-8639-ae33f7a25a58`
- post-U0 session SHA256: `2caf68e6dde9adcefce8fd990ba9f4d81b4564231cec3069042ed4e2d7eb1033`
- project remains exact/clean
- analysis-only contract satisfied with 0 edit/write calls.

U1 authority:
- result: `S2_COMMON_PRESTATE_U1_RESULT_V1.md/json`
- same session ID: `01a0f7cc-4a3e-7000-8639-ae33f7a25a58`
- post-U1 session SHA256: `1482ce0c2958fd1517f965bf2c27fcf943ce010d1220f3172611cd691a07d9f4`
- project remains exact/clean
- pre-implementation clarification contract satisfied with 0 tool calls.

U2 authority:
- result: `S2_COMMON_PRESTATE_U2_RESULT_V1.md/json`
- same session ID: `01a0f7cc-4a3e-7000-8639-ae33f7a25a58`
- post-U2 session SHA256: `bc039ce82b8b5d2ae222ac7c96a050b44fb7bffdcdb3864a0fd3845e4a5e4424`
- 7 tracked modified files, 0 untracked files
- patch SHA256: `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`
- material derived work is now non-empty
- pre-revision implementation persists relative CLI paths as lexical absolute paths
- no settings.json-relative late-revision semantics are present.

U3 authority:
- result: `S2_COMMON_PRESTATE_U3_RESULT_V1.md/json`
- same session ID: `01a0f7cc-4a3e-7000-8639-ae33f7a25a58`
- post-U3 session SHA256: `27de34edff19712f382c5086bfc96adc123b04a00f32618f89b8ea847e850000`
- final patch is unchanged from U2: `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`
- pi-test.sh verifies both user/global and project-local relative inputs persist the same lexical absolute path
- relative-path basis is caller cwd, not settings.json directory
- no new edit/write calls; no temporary smoke directories remain.

Do not deliver late revision indices 37/39 to this frozen session.

## Freeze result

`S2_COMMON_PRESTATE_FREEZE_V1 = PASS`

Authority:
- `S2_COMMON_PRESTATE_FREEZE_V1/`
- `S2_COMMON_PRESTATE_FREEZE_RESULT_V1.md/json`

Frozen snapshot:
- base `e54dff7efb460e364a39e4a22369991a20c105b9`
- tracked patch SHA256 `6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`
- patch bytes 8,292
- 7 tracked modified files
- 0 untracked task artifacts
- 0 deletions
- fresh official-image reconstruction PASS

Frozen session:
- external frozen copy SHA256 `27de34edff19712f382c5086bfc96adc123b04a00f32618f89b8ea847e850000`
- 2,037,536 bytes / 217 lines
- exactly four scientific user turns: 0,6,8,20
- 37/39 absent

Freeze manifest SHA256:
`22498a753aeda06a14d612e3fa825db84504249902e2d9d71f928df09f44e5f5`

Exact outcome-blind R3 semantic scope is frozen in `R3_SCOPE_V1.md/json`; whole-file reuse and whole-line credit for mixed `docs/packages.md:77` are forbidden.

## R2 result

`S2_R2_FULL_RESTART` is complete as a valid independent execution. Authority:
- `S2_R2_FULL_RESTART_SNAPSHOT_V1/`
- `S2_R2_FULL_RESTART_RESULT_V1.md/json`

The raw frozen verifier reward is `0.0000`, but the primary F2P measurement is structurally invalid for the frozen base because the verifier instantiates runtime `PackageManager` while the task base defines `PackageManager` only as an interface and `DefaultPackageManager` as the runtime class. Under PRG-1 this yields no scientific correctness verdict and no PARTIAL_REFERENCE classification. R3/R0/R1 are not authorized.

## Selector replan result

`BFSC_SELECTOR_REPLAN_AFTER_S2_VERIFIER_INVALID` is complete. Authority:
- `BFSC_SELECTOR_REPLAN_AFTER_S2_VERIFIER_INVALID_20261002.md/json`

The selector keeps BFSC at PRECARD because S4 is the only still-unobserved frozen V-witness slot, but it does not authorize S4 paid work. A prospective S4-only `VERIFIER_COMPATIBILITY_GATE` now precedes mechanism exposure and all paid execution so the factory does not repeat S2's structurally invalid measurement failure.

## S4 verifier-compatibility result

`S4_VERIFIER_COMPATIBILITY_GATE_V1 = VERIFIER_COMPATIBLE`. Authority:
- `S4_VERIFIER_COMPATIBILITY_GATE_V1.md/json`

The exact frozen S4 verifier executes against the frozen base with exit 0. Observed P2P gates pass; F2P failures are the intended absent `pi-package`/documentation/search behavior, not a structurally impossible harness assumption.

## S4 mechanism-exposure result

`S4_MECHANISM_EXPOSURE_GATE_V1 = EXPOSURE_NONIDENTIFIABLE`. Authority:
- `S4_MECHANISM_EXPOSURE_SOURCE_V1.json`
- `S4_MECHANISM_EXPOSURE_GATE_V1.md`
- `S4_MECHANISM_EXPOSURE_RESULT_V1.md/json`

The user-only source shows a correction after choosing `pi-package`, but not the concrete already-created target/package implementation that the correction invalidates. Assistant trajectory evidence would be required to identify it and is forbidden by the gate. S4 paid execution remains closed.

## Exact next step

`BFSC_SELECTOR_REPLAN_AFTER_S4_EXPOSURE_NONIDENTIFIABLE` only.

Do not repair/rescore S2, do not run S2 R3/R0/R1, and do not run S4 common-prestate/R2/R3/R0/R1 before the selector decision.
