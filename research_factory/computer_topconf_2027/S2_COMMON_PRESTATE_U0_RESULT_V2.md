# S2 Common Prestate U0 Result V2

date: 2026-10-01
status: PASS_ANALYSIS_ONLY__U1_NEXT
task: pi-mono-auto-a4fca584
scope: common-prestate U0 / source_message_index 0 only

## Decision

`S2_COMMON_PRESTATE_U0 = PASS`

This is the first valid scientific turn of the S2 common-prestate trajectory.

Historical U0-v1 remains excluded as `INVALID_RUNTIME_SUBSTRATE__NO_PROJECT_EFFECT`.

## Scientific identity

WSL scientific repo:
`/home/agent/s2-common-pre-v3`

HEAD:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Final repo state:
- clean;
- no tracked/untracked task change;
- `git diff --check`: PASS.

Runtime:
- Ubuntu 26.04 x86_64;
- user `agent`, uid 1001;
- Node `v20.20.2`;
- task Bun `1.3.13`;
- OMP `18.1.15`;
- harness Bun `1.3.14`;
- command-backed openai-codex auth through Windows interop;
- PI proxy through the temporary user-space relay.

Model:
- `openai-codex/gpt-5.6-sol`;
- fallback=false;
- thinking=`xhigh`.

## Input integrity

Frozen source message index:
`0`

Prompt SHA256:
`fb2568144b28f27af54954482a3d2aa843a66459ebcd9a2d73bc0aa781c763c6`

Source adapter:
`S2_COMMON_PRESTATE_SOURCE_ADAPTER_V1.md`

Adapter SHA256:
`cb67aec5cc4ccae4e8f0beaaf414b5c8399909e0fe02882a598d385c8d67b6a4`

Observed:
- exactly one scientific user turn;
- user turn equals the frozen U0 text exactly;
- adapter is system/context-only and is not counted as a user turn;
- no late revision 37/39 was delivered.

## Session

Session ID:
`01a0f7cc-4a3e-7000-8639-ae33f7a25a58`

Session path:
`/home/agent/s2-common-pre-v3-sessions/2026-10-01T14-09-15-838Z_01a0f7cc-4a3e-7000-8639-ae33f7a25a58.jsonl`

Post-U0 SHA256:
`2caf68e6dde9adcefce8fd990ba9f4d81b4564231cec3069042ed4e2d7eb1033`

Size:
- 1,172,490 bytes;
- 114 JSONL lines.

Lifetime:
- request key: `s2-common-pre-u0-wsl-v1b`;
- turn id: `turn_2172000c55ce474f806019efc0e1a155`;
- exit code: 0;
- outcome: succeeded;
- terminal/quiescent: true;
- wall span: 280.771 s.

## Analysis-only contract

The U0 contract explicitly forbids implementation.

Independent acceptance:
- edit tool calls: 0;
- write tool calls: 0;
- final repo change: none;
- final assistant stop reason: `stop`.

The agent performed repository/code analysis and a failed local-path install probe, but the probe left no task-repo effect.

Therefore the analysis-only contract is satisfied.

## Forbidden-source boundary

Supervisor scan of assistant tool-call arguments found zero references to:
- reference/gold patch;
- canonical goals;
- oracle session/intents;
- R2/R3 result material;
- RESEARCH-01 Phase-B;
- verifier result.

No solution-bearing future evidence entered U0.

## Accounting

U0 incremental accounting:
- model calls: 12;
- tool calls: 48;
- mutating edit/write calls: 0;
- input tokens: 119,735;
- output tokens: 13,796;
- cache-read tokens: 855,808;
- reasoning tokens: 10,131;
- reported cost: $1.0971832.

## Evidence boundary

Supported:
- S2 historical issue/code analysis can be reproduced under the frozen scientific runtime;
- analysis-only U0 completes without project mutation;
- the fresh v3 scientific session is valid for continuation.

Not supported:
- implementation correctness;
- any pre-revision derived code artifact yet;
- mechanism reuse identifiability;
- late-revision behavior;
- R2/R3/R0/R1 results.

## NEXT_STEP

`S2_COMMON_PRESTATE_U1` only.

Deliver exact source_message_index=6 in the **same WSL-native session** using `--continue`.

Do not deliver U2/U3/37/39 in the same supervisor step.
