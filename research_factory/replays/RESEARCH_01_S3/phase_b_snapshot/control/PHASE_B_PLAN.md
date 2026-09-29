# RESEARCH-01 / S3 Phase B Plan

## Current goal

Keep the Phase-A signal protocol and explicit first-turn open / last-turn close behavior, while ensuring the visible signal UI never removes, refocuses, or blocks the normal editor and is never recreated reentrantly from high-frequency streaming updates.

## What changed in the new requirement

While the signal UI is open and model output continues streaming, the transcript still renders but the user cannot type. The concern is whether UI work in the message lifecycle is repeatedly rebuilding or otherwise blocking the interactive editor. The revised user-visible requirement is that the signal UI remain visible between the separate open and close messages without taking away normal editor input.

## Phase A responsibilities: independent versus impacted

The following responsibilities are independent of the freeze and must remain unchanged:

1. `/start` registers through the existing extension command API.
2. `/start` injects one hidden custom message without starting a model turn.
3. The hidden message defines distinct exact open and close signals and forbids emitting both in one response.
4. Only completed assistant messages with an exact standalone signal may transition the signal UI.
5. Open and close remain separate ordered transitions; combined, embedded, irrelevant, and premature close signals remain ignored.
6. Focused behavioral tests remain the contract for injection, signal classification, and UI state transitions.

The impacted responsibility is only the UI projection mechanism. The Phase-A outcome—open makes extension-owned status visible and a later exact close removes it—remains required, but implementing that outcome with non-overlay `ctx.ui.custom()` is invalid because it replaces the editor. The Phase-A test harness assertion that `custom()` is called must therefore be revised to assert visible status plus continued editor availability.

## Phase A invariants that remain valid

- Hidden control instructions remain absent from visible transcript rendering.
- Normal assistant content and signal-like substrings do not trigger UI transitions.
- One `message_end` maps to at most one transition.
- Close is accepted only after an open transition in the active exercise.
- The extension remains the sole acceptance authority for its UI state.
- Existing extension command, event, and UI APIs are reused with no new dependency or shared protocol infrastructure.
- No unrelated repository behavior is changed.

## New lifecycle and performance invariant

While signal status UI is visible, the normal editor remains installed, focused, and able to receive typing. UI creation/removal occurs only on exact state transitions (`closed → open` and `open → closed`), never on token-level or other high-frequency update paths; repeated open signals while already open are idempotent and do not recreate the projection.

## Smallest causal model for the freeze

Confirmed source path:

`exact OPEN message_end` → Phase A handler calls non-overlay `ctx.ui.custom()` → `showExtensionCustom()` saves editor text, clears `editorContainer`, inserts the custom component, and focuses that component → chat/Markdown rendering continues elsewhere in the TUI, but the editor is no longer present or focused → typing is unavailable until exact CLOSE calls the captured `done()` callback and `restoreEditor()` runs.

The signal UI is not recreated on every streamed update: the extension has no `message_update` handler and guards opening with its open state. The failure is input ownership for the entire open interval, not excessive recreation.

## Counterexamples to naive fixes

- Making the existing `ctx.ui.custom()` call fire-and-forget, debounced, or guarded more aggressively can make lifecycle/unit assertions pass and prove the UI opens only once, yet the non-overlay custom UI still replaces the editor and typing remains unavailable.
- Closing the custom UI immediately after rendering restores typing and can make an input-availability check pass, but violates the Phase A invariant that the status remains visibly open until a later exact close signal.

## Minimal current change

Preserve the command, hidden protocol message, exact signal classifier, `message_end` boundary, active state, and ordering rules. Replace only the custom-editor-replacement lifecycle with one keyed `ctx.ui.setWidget()` projection: set the widget on exact open, retain a boolean open state, and clear the same widget key on exact close or restart. The repository's widget path renders adjacent to the editor and does not clear or refocus it.

## Exact cheapest acceptance checks

1. Modify the focused Vitest harness first so an open signal must leave simulated editor input available, render a keyed widget exactly once, and avoid `ctx.ui.custom()`; the current Phase A code must fail this assertion.
2. Modify the ignored Node smoke harness with the same editor-availability model; run `node --experimental-strip-types .research_input/phase_a_signal_ui_smoke.mts` before implementation and expect failure on the new invariant, then after implementation expect exit 0.
3. Preserve existing focused assertions for hidden injection, combined/embedded signal rejection, close-before-open rejection, visible-open state, and later exact close.
4. Attempt the canonical focused test from `packages/coding-agent` with `npx tsx ../../node_modules/vitest/dist/cli.js --run test/signal-ui-extension.test.ts`; do not fetch dependencies.
5. Run Node syntax checks for both tracked TypeScript files and attempt `npm run check`; report unavailable toolchain steps as unverified rather than passed.
6. Inspect complete Phase-B-vs-Phase-A diffs, whitespace diagnostics, and final status; only the UI projection lines and their focused test harness assertions may change.

## Actual evidence

- **Repository ownership trace:** `showExtensionCustom()` clears `editorContainer`, inserts the custom component, and calls `setFocus(component)` until `done()` restores the editor. `setExtensionWidget()` instead updates a keyed widget map and renders the widget containers without clearing or refocusing the editor.
- **RED reproduction:** after the focused harness modeled editor ownership, `node --experimental-strip-types .research_input/phase_a_signal_ui_smoke.mts` failed against Phase A with `opening status UI does not replace the editor`, actual custom-call count `1`, expected `0`.
- **GREEN verification:** after replacing the projection, the same smoke command exited 0 with `signal UI smoke checks passed`. It covers hidden injection, combined/embedded signal rejection, premature close rejection, editor availability while open, no `message_update` subscription, idempotent repeated open, and later exact close using the same widget key.
- **Canonical focused test:** `npx --offline tsx ../../node_modules/vitest/dist/cli.js --run test/signal-ui-extension.test.ts` did not collect tests because dependencies are absent; npm exited `ENOTCACHED` without fetching.
- **Syntax:** Node type-stripping syntax checks for `.pi/extensions/signal-ui.ts` and `packages/coding-agent/test/signal-ui-extension.test.ts` both exited 0.
- **Repository check:** `npm run check` stopped at its first command because local `biome` is not installed; Biome, `tsgo`, and web checks did not run.
- **Diff/status:** both new tracked deliverable files have no whitespace-error diagnostics; only `.pi/extensions/signal-ui.ts` and `packages/coding-agent/test/signal-ui-extension.test.ts` appear in `git status --short`, and HEAD remains `5133697bc454da5595655cf4b0c70d3c2c725677`.
- **Five-axis self-review:** no additional correctness, readability, architecture, security, or performance issue was found. Signal text remains treated as untrusted exact-match input and can only affect this extension's local widget state while explicitly active.

## Rework relative to Phase A

- **Preserved unchanged:** signal constants, hidden protocol content, `/start` registration and hidden `sendMessage`, exact assistant-text classifier, `message_end` boundary, active-run state, combined/embedded/premature signal rejection, and explicit first-open/later-close semantics.
- **Revised implementation hunks:** added an `ExtensionContext` type and private widget key; replaced the captured `dismissUi` callback with boolean `uiOpen`; replaced the non-awaited `ctx.ui.custom()`/promise lifecycle with one `setWidget(key, lines)` call; and replaced callback dismissal with `setWidget(key, undefined)`.
- **Revised test hunks:** retained all Phase-A protocol assertions, replaced the expectation that `custom()` opens UI with widget/open-state/editor-availability assertions, and added coverage that no `message_update` handler exists and a repeated open signal does not recreate the widget.
- **Discarded Phase-A behavior:** only editor replacement/focus capture while the status is open. No Phase-A protocol responsibility or ordering invariant was discarded.

## Remaining uncertainty

The installed Vitest suite, Biome/`tsgo` checks, and a live interactive terminal acceptance run remain unavailable in this dependency-free checkout. The executable harness proves the extension's boundary choices and state transitions but simulates the documented editor-focus semantics rather than driving a real TUI.

## Current next action

return for independent endpoint evaluation
