# S2 Common Prestate U0 Invalid Attempt V1

date: 2026-10-01
status: INVALID_RUNTIME_SUBSTRATE__NO_PROJECT_EFFECT
task: pi-mono-auto-a4fca584
scope: first attempted common-prestate turn U0 only

## Why invalid

The user turn and source adapter were delivered correctly, but the scientific tool execution substrate was not the frozen task runtime.

Observed during U0-v1:
- OMP harness: 18.1.15;
- model: openai-codex/gpt-5.6-sol;
- thinking: xhigh;
- task checkout content: exact base and clean;
- **tool shell runtime:** Windows host Node v24.16.0 / Bun 1.3.14;
- checkout node_modules had been copied from the official Linux image;
- a runtime probe hit an esbuild cross-platform mismatch.

The frozen S2 runtime authority is Linux/amd64, Node v20.20.2, Bun 1.3.13. Because S2 is itself a path-semantics task, this runtime deviation is scientifically material and cannot be waived merely because U0 was analysis-only.

Therefore U0-v1 contributes zero scientific common-prestate evidence.

## What remains valid as execution evidence

Lifetime:
- request key: s2-common-pre-u0-v1
- turn id: turn_86f29c6e0d474093a6b4db3a4cdf7567
- outcome: succeeded
- terminal/quiescent: true

Session:
- id: 01a0f748-cd50-7000-ad23-65eda39158c4
- JSONL SHA256: 169efffc8e8f4d925d564f8db542ceb92d3c9cc38e20f49ed648c862a3564967
- bytes: 1,604,134
- lines: 153

Input integrity:
- exactly one scientific user turn;
- user0 equals the frozen source message exactly;
- prompt SHA256: fb2568144b28f27af54954482a3d2aa843a66459ebcd9a2d73bc0aa781c763c6;
- source adapter SHA256: cb67aec5cc4ccae4e8f0beaaf414b5c8399909e0fe02882a598d385c8d67b6a4;
- model fallback: false;
- forbidden solution-source tool-path scan: zero hits;
- edit/write tool calls: zero.

Accounting:
- model calls: 13
- tool calls: 67
- mutating edit/write calls: 0
- noncached input+output: 159,912
- reported cost: $1.3404768
- wall: 206.31 s

Project effect:
- checkout HEAD remained e54dff7efb460e364a39e4a22369991a20c105b9;
- git status remained clean after checkout-local filemode normalization;
- no scientific task bytes changed.

## Decision

Do not continue this session.

Do not deliver U1 into it.

The next valid common-prestate trajectory must start a fresh session on the repaired Linux execution substrate.
