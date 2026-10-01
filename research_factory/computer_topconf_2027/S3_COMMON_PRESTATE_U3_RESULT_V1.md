# S3 Common Prestate U3 Result V1

date: 2026-10-01
status: PASS_U3__U4_NEXT
task: pi-mono-auto-93c17d3b
scope: S3_COMMON_PRESTATE pre-revision turn U3 only

## Scientific identity

Checkout:
`D:/cs_work/external/spec_stageb_s3_common_pre_v2`

Frozen root:
`5133697bc454da5595655cf4b0c70d3c2c725677`

Session directory:
`D:/cs_work/external/spec_stageb_sessions/s3_common_pre_v2`

Session ID:
`01a0f62d-3227-7000-ac03-03b36dfb1b6b`

Session JSONL:
`2026-10-01T06-35-52-231Z_01a0f62d-3227-7000-ac03-03b36dfb1b6b.jsonl`

Session SHA256 after U3:
`8fcb2578290a6566a0eb3c0b2d123961d6cb54afb6cc4fc537a12931af63c1d4`

Observed identity remained:
- model: `openai-codex/gpt-5.6-sol`;
- fallback: false;
- thinking: `xhigh`;
- exactly three user turns total;
- user turn 3 equals the frozen U3 verbatim;
- Lifetime turn `turn_4278395b4ee8456095f0cee71372b0c4` exited 0 and quiescent.

Forbidden-source scan:
PASS for reference-patch, oracle-intent/session, canonical-goal, late-revision, Phase-B and S3 endpoint/R3-scope markers.

## U3 input

Source:
`source_message_index=36`

Verbatim:
`ok, if you do it all in one message then the ui will not open i guess`

Frozen interpretation:
- UI open and close must not collapse into one assistant response;
- the open state must be able to survive across message/turn boundaries.

Source_message_index 38/40 are historical observations, not new requirements, and were not injected.

## U3 output state

The agent modified only the existing project-local extension:
`.pi/extensions/message-signals.ts`

Final extension SHA256:
`1d76a1742be2dee3356f770cb6bb7385565d3aaa1e4eaa5bc64f665875ac4080`

Final checkout:
- HEAD remains the frozen root;
- no tracked diff;
- only `.pi/extensions/message-signals.ts` remains untracked;
- `git diff --check`: PASS.

The implementation now makes the U3 separation explicit:
- after `[[PI_EXTENSION_INPUT]]`, the protocol requires the model to end the response immediately;
- it must wait for the extension's hidden follow-up before continuing;
- signal parsing scans standalone signal lines;
- if an invalid response contains both INPUT and DONE, INPUT wins, preventing same-message immediate close;
- DONE therefore closes only when a later completed assistant response emits it.

The agent's temporary combined-signal regression smoke passed and left no extra checkout file.

## Evidence boundary

This is a U3 common-prestate transition PASS, not a final product/evaluator PASS.

The source state is consistent with the frozen U3 interpretation, but a real sustained multi-turn UI interval is not yet independently established here. That behavior is the purpose of the already-frozen U4/U5 requirement turns; do not pull their evidence backward into U3.

No claim is made that the final S3 common prestate, R2, R3, or paper-level value gate has passed.

## Accounting

U3 incremental session accounting:
- model calls: 12;
- tool calls: 13;
- mutating tool calls: 4;
- input tokens: 146,609;
- output tokens: 3,714;
- cache-read tokens: 1,474,304;
- reasoning tokens: 2,049;
- reported cost: $1.2504376;
- Lifetime wall span: 104.289 s.

## Decision

`S3_COMMON_PRESTATE_U3 = PASS`

No objective, evaluator, claim or evidence threshold was changed.

Do not freeze the final common prestate yet.

## NEXT_STEP

`S3_COMMON_PRESTATE_U4` only.

Deliver source_message_index=42 verbatim in the same v2 checkout/session using `--continue`:

`ok, i started, now do a bunch of turns, in the first turn open the ui, in the last turn clos eit`

Do not inject historical observations source_message_index=38/40.
Do not send U5/U6 in the same supervisor turn.
