# S3 Common Prestate Run Contract V1

date: 2026-10-01
status: COMMON_PRESTATE_FROZEN__R3_SCOPE_FROZEN__R2_NEXT
task: pi-mono-auto-93c17d3b
parent:
- S3_STAGE_B_BOUNDARY_FREEZE_V1.md
- S3_EXECUTION_LEVERAGE_GATE_V1.md
- S3_RUNTIME_PREFLIGHT_RESUME_RESULT_V2.md

## Owned step

Generate exactly one scientific pre-revision trajectory for S3.

Execution advanced one user-authorized supervisor turn at a time through valid U5-v2. The first U5 launch remains excluded as `INVALID_PROMPT_MISMATCH`; exact post-U4 session state was restored by byte hash before valid U5-v2. The post-U5 state is now frozen in `S3_COMMON_PRESTATE_FREEZE_V1` with manifest SHA256 `06b55884fbca4169175cfc178a145b2a68937f810a1be268da346f6b185a195d`, and exact outcome-blind R3 file/hunk scope is frozen. The original v2 session is now a frozen history artifact and must not be continued.

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

## U2 result

U2 passed in the same v2 checkout/session. Authority:
- `S3_COMMON_PRESTATE_U2_RESULT_V1.md`
- `S3_COMMON_PRESTATE_U2_RESULT_V1.json`

The exact frozen U2 was the second user turn; GPT-5.6 Sol/xhigh identity remained unchanged; no forbidden source marker entered the session; the extension was content-preservingly moved into `.pi/extensions/message-signals.ts`.

## U3 result

U3 passed in the same v2 checkout/session. Authority:
- `S3_COMMON_PRESTATE_U3_RESULT_V1.md`
- `S3_COMMON_PRESTATE_U3_RESULT_V1.json`

The exact frozen U3 was the third user turn; model/thinking identity and forbidden-source boundary remained unchanged. The resulting extension explicitly requires response termination after INPUT and waits for a hidden follow-up; INPUT wins over an invalid same-response DONE. A sustained real multi-turn interval remains for U4/U5 rather than being backfilled into U3.

## U4 result

U4 passed as a valid controlled trajectory turn in the same v2 checkout/session. Authority:
- `S3_COMMON_PRESTATE_U4_RESULT_V1.md`
- `S3_COMMON_PRESTATE_U4_RESULT_V1.json`

The exact frozen U4 was the fourth user turn; identity and forbidden-source boundaries remained intact. The agent made no code change and ended with standalone `[[PI_EXTENSION_INPUT]]`, creating first/open-wait protocol evidence. Because the runner uses `--no-extensions`, this is not independent live-UI verification and no arbitrary answer is injected.

## U5 result

The first U5 launch is invalid execution evidence only:
- `S3_COMMON_PRESTATE_U5_INVALID_V1.md`
- `S3_COMMON_PRESTATE_U5_INVALID_V1.json`

After exact hash-proven restoration to the recorded post-U4 session bytes, valid U5-v2 passed as the final pre-revision requirement-assimilation turn. Authority:
- `S3_COMMON_PRESTATE_U5_RESULT_V2.md`
- `S3_COMMON_PRESTATE_U5_RESULT_V2.json`

The exact frozen U5 is the fifth scientific user turn. It made no code change and ended after workload turn 1/10 with standalone `[[PI_EXTENSION_INPUT]]`. This does not claim live 10-turn UI verification in the frozen `--no-extensions` scientific runner; no arbitrary follow-up answer and no workflow-only U6-equivalent turn was injected.

## Common-prestate freeze result

Freeze passed. Authority:
- `S3_COMMON_PRESTATE_FREEZE_RESULT_V1.md`
- `S3_COMMON_PRESTATE_FREEZE_RESULT_V1.json`
- `S3_COMMON_PRESTATE_FREEZE_V1/FREEZE_MANIFEST.json`
- `S3_COMMON_PRESTATE_FREEZE_V1/R3_SCOPE_V1.md/json`

The exact post-U5 state is reconstructable from frozen base + empty tracked patch + one byte-exact untracked artifact copy + empty deletion manifest. The session history is frozen by exact bytes/hash outside the mutable worktree. Material derived work is present, and whole-file R3 reuse is forbidden by the frozen mixed-seam classification.

## Exact next step

`S3_R2_FULL_RESTART` only.

R2 must start independently from TASK_INITIAL_STATE plus the frozen final specification including U6. Do not continue the common-prestate session and do not start R3 in the same supervisor turn.
