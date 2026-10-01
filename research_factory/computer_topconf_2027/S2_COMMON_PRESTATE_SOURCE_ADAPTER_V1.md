# S2 Common-Prestate Frozen Issue Context Adapter V1

Purpose: restore the public requirement source referenced by historical user turn 0 without changing that user turn.

Replay fact:
- historical URL: https://github.com/badlogic/pi-mono/issues/1216
- the historical URL returns 404 at replay time;
- the public issue is currently available at https://github.com/earendil-works/pi/issues/1216;
- this appendix contains only public issue requirement context and its directly linked issue #1207.
- It contains no reference patch, verifier result, oracle session, canonical goals, assistant trajectory, or future successful implementation.

When the user asks to read issue 1216, treat the frozen source below as the issue content that the URL referred to. Analyze repository code yourself from the task checkout. Do not infer an implementation from this appendix beyond what the issue/comments state.

## Issue #1216 — Support installing local extension using `pi install`

State at frozen retrieval: closed

### Body

What do you want to change?

`pi install` does not allow a local path, although the extension system itself works with a local file. The issue points to the package documentation and asks to extend `pi install` to support a local file/path rather than requiring manual edits to `settings.json`.

Why?

The reporter wants automated, reproducible configuration using Nix. Directly making `settings.json` immutable conflicts with pi because settings can be updated by normal user interaction. Supporting local files through `pi install` would allow programmatic configuration without manual `settings.json` updates that could delete or corrupt user settings.

How?

No implementation proposal was supplied.

### Comments

1. Maintainer: `settings.json` is not static; it changes through normal TUI interaction such as /settings, /model, shift+tab, and other actions. The maintainer notes that `pi install` on main supports local paths.

2. Reporter: this is why linked issue #1207 proposed separating user-defined settings from extension-specific config, which could be managed by Nix/other systems. The reporter asks whether local-path install behavior recently changed and notes that documentation still says it does not work with a local path.

3. Maintainer: the local-path support is in main and not released yet.

4. Reporter thanks the maintainer.

Direct linked issue: #1207.
No linked PR is present in the issue body/comments.

## Linked issue #1207 — Add extra configuration support for extension management

State at frozen retrieval: closed

### Body

The reporter proposes an additional configuration mechanism so extension definitions can live outside the general `settings.json`, for example an `extensions.json` containing base extension directories and extra extension paths. The motivation is team/declarative extension management and Nix/Home Manager-friendly configuration while keeping personal settings separate.

The concrete names/shape are explicitly presented as examples rather than requirements.

### Comment

The maintainer explains that this can already be achieved through pi packages: a package can carry its own extensions/themes/skills/prompts and dependencies, users can install such a meta package via `pi install git:...`, then use `pi config` to select desired features, with that selection stored in `settings.json`.

## Provenance receipts

Raw public API source hashes captured before this adapter:
- issue 1216: `967abaeac2832f407a837a1a7528b8fa5661929d6cfff5349c6e4600d7653f6e`
- issue 1216 comments: `77d664cbada894b40a40a99427aa4debf4fcdff95d59361dd0362b5d3755c3d8`
- issue 1207: `0e173a935437c2812a94a3c2c572c3bd59c1aca4bbfd29ae8bd2549b3d7dfc36`
- issue 1207 comments: `a4323086aca38eff82c9e42fbf245370e5bab952604573ba15beefd00a6bd041`

This adapter is context-only. It is not a scientific user turn and must not be counted as one.
