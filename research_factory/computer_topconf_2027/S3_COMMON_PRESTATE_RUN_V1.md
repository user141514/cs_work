# S3 Common Prestate Run Contract V1

date: 2026-10-01
status: U1_V2_PASS__U2_NEXT
task: pi-mono-auto-93c17d3b
parent:
- S3_STAGE_B_BOUNDARY_FREEZE_V1.md
- S3_EXECUTION_LEVERAGE_GATE_V1.md
- S3_RUNTIME_PREFLIGHT_RESUME_RESULT_V2.md

## Owned step

Generate exactly one scientific pre-revision trajectory for S3.

This contract currently authorizes **U1 only**. Later U2/U3/U4/U5 are separate continuation turns in the same durable OMP session and same checkout.

No late revision U6, R0, R1, R2 or R3 is authorized by this file.

## Scientific checkout

Invalid U1-v1 checkout (historical only):
`D:/cs_work/external/spec_stageb_s3_base_5133697`

Authorized U1-v2 scientific checkout:
`D:/cs_work/external/spec_stageb_s3_common_pre_v2`

Frozen initial state:
- HEAD = `5133697bc454da5595655cf4b0c70d3c2c725677`
- detached HEAD;
- dirty status = empty before U1;
- remotes = 0;
- refs = 0;
- `node_modules` restored with `npm ci --ignore-scripts`.

The local clone was created from the historical pi-mono object store only as a byte source, then detached/stripped of refs/remotes. No later branch/tag is reachable through ordinary Git refs.

## Agent identity

Frozen Stage-B identity:
- provider/model: `openai-codex/gpt-5.6-sol`;
- reasoning: `xhigh`;
- runner: OMP durable session;
- tools: `read,bash,edit,write,grep,glob`;
- no skills;
- no rules;
- no extensions;
- no title-generation model call;
- auto-approve enabled;
- PI_PROXY = `http://127.0.0.1:7897`.

OMP executable for this S3 cohort step:
`C:/Users/Administrator/.bun/bin/omp.exe`
observed version:
`omp/18.1.15`.

The frozen scientific contract did not previously encode an OMP CLI patch version. 18.1.15 is selected prospectively here to minimize runtime drift; do not claim that S5's historical CLI patch version was mechanically recovered from its JSONL.

## Session identity

Invalid U1-v1 session directory (historical only):
`D:/cs_work/external/spec_stageb_sessions/s3_common_pre_v1`

Authorized U1-v2 / future U2-U5 session directory:
`D:/cs_work/external/spec_stageb_sessions/s3_common_pre_v2`

U1-v2 starts a new session from a fresh checkout.
U2-U5, if U1-v2 passes, must use `--continue` against the v2 session directory.
There must be exactly one v2 session JSONL before any continuation.

## U1 input

Source:
`USER_REQUIREMENTS_RAW.json source_message_index=2`.

Prompt authority:
`s3_arm_prompts/S3_COMMON_PRE_U1.txt`.

No C0/context-only message, historical observation, workflow-only turn, late revision, oracle, reference patch, verifier outcome or development Phase-B artifact is supplied.

## Execution boundary

U1 command configuration:
- `--model openai-codex/gpt-5.6-sol`
- `--thinking xhigh`
- `--tools read,bash,edit,write,grep,glob`
- `--no-skills --no-rules --no-extensions --no-title --auto-approve`
- `--session-dir <frozen dir>`
- `--cwd <scientific checkout>`
- `--print`
- hard runtime ceiling: 45 minutes.

## U1 acceptance

U1 is valid only if:
1. exactly one session JSONL exists;
2. session model record resolves to `openai-codex/gpt-5.6-sol`;
3. thinking record is `xhigh`;
4. first user message equals the frozen U1 text;
5. OMP terminates normally/quiescently;
6. checkout remains rooted at frozen HEAD;
7. no forbidden source path enters the session;
8. resulting derived state is retained for later U2 continuation, not yet frozen as the final common prestate.

If U1 fails transport/provider/runtime, record INVALID and do not silently rerun with a different model/backend.

## U1 result

U1-v2 passed. Authority:
- `S3_COMMON_PRESTATE_U1_RESULT_V2.md`
- `S3_COMMON_PRESTATE_U1_RESULT_V2.json`

## Exact next step

U2 only:
source_message_index=31
`move that to cwd/.pi/extensions so i can relaod`

No U3-U5 in the same supervisor turn.
