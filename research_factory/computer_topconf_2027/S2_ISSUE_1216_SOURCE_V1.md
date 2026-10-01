# S2 Issue 1216 Requirement Source Receipt V1

date: 2026-10-01
task: pi-mono-auto-a4fca584
original_url: https://github.com/badlogic/pi-mono/issues/1216
resolved_public_url: https://github.com/earendil-works/pi/issues/1216
issue_number: 1216
title: Support installing local extension using pi install
state_at_retrieval: closed
source_role: initial public requirement context referenced by user message index 0

## Frozen requirement meaning

The public issue states that:
- `pi install` did not accept a local path even though the extension system itself could work with a local file;
- the desired feature is support for installing/managing a local extension/file through the normal pi package/install flow rather than requiring direct manual edits to `settings.json`;
- the motivation includes reproducible/programmatic configuration while avoiding destructive or corrupting manual settings updates;
- the issue itself does not prescribe an implementation design.

## Evidence boundary

This receipt freezes only the public problem statement used by the initial user instruction.

It does not include or use:
- reference/gold patch;
- later implementation/solution history;
- verifier outcomes;
- oracle session/intents;
- benchmark canonical goals.

Current public source evidence was retrieved from GitHub issue 1216 on 2026-10-01.
