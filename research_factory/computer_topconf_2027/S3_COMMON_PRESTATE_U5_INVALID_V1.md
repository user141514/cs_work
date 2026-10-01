# S3 Common Prestate U5 Invalid Attempt V1

date: 2026-10-01
status: INVALID_PROMPT_MISMATCH__RECOVERED
task: pi-mono-auto-93c17d3b
scope: excluded U5 launch attempt only

## Cause

The first U5 launch corrupted the frozen verbatim prompt during shell quoting:

expected:
`dude, if you output open and close, close is also executed. let's try again. 10 turns, read all the @README.md files 10 lines each. open on first turn, close on last turn`

delivered:
`dude, if you output open and close, close is also executed. lets try again. 10 turns, read all the @README.md files 10 lines each. open on first turn, close on last turn`

Because `let's` became `lets`, this attempt is scientifically invalid regardless of semantic similarity.

## Runtime disposition

Lifetime turn:
`turn_ef0a43d36e464683ace3ead07d1db1b0`

The attempt was cancelled while running and reached:
- outcome: `cancelled`;
- phase: `terminal`;
- quiescent: `true`.

Scientific checkout effects:
- no tracked change;
- extension SHA256 remained `1d76a1742be2dee3356f770cb6bb7385565d3aaa1e4eaa5bc64f665875ac4080`.

## Session recovery

The invalid launch appended exactly two JSONL records:
1. the corrupted user message;
2. the automatically resolved `@README.md` fileMention.

The byte prefix immediately before those two records had SHA256:

`f495f7995abe1e3d1caccb225570db7035d5cc2cb73b0f3bbe419c642c36b6ad`

which exactly matches the authoritative post-U4 session hash recorded before U5.

After the invalid scope was proven quiescent, only those two appended records were removed. The restored JSONL then independently re-hashed to the exact same authoritative post-U4 value `f495f799...`.

Therefore recovery returned the durable session to the previously verified U4 state byte-for-byte before any valid U5 retry.

## Decision

This attempt contributes **zero scientific evidence** and must never be counted in U5 model/task outcomes.

It is retained only as execution-integrity evidence.
