# RESEARCH-01 / S3 Phase A Plan

## Goal

Implement the pre-revision test extension behavior: a slash command starts a multi-turn signal exercise by injecting a hidden custom session message; the extension observes completed assistant messages and independently reacts to an open signal on the first turn and a close signal on the last turn, so a close signal is not collapsed into or executed with the open turn.

## Current state

- Checkout remains detached and exactly at `5133697bc454da5595655cf4b0c70d3c2c725677`.
- `.pi/extensions/signal-ui.ts` implements the extension and `packages/coding-agent/test/signal-ui-extension.test.ts` provides focused behavioral coverage.
- The only tracked-worktree changes are those two untracked deliverable files; generated `graft` cache data was removed.
- This checkout has no installed `node_modules`, so repository commands that require Vitest, Biome, or `tsgo` cannot execute locally without a prohibited dependency fetch.

## Independently checkable responsibilities

1. Register the requested slash-command entry point using the repository's existing extension API.
2. Inject a non-visible custom session message that gives the model an unambiguous multi-turn signal protocol.
3. Observe completed assistant messages through the existing `message_end` event and recognize only the intended signal output.
4. Open extension-owned UI state when the open signal appears, without treating future close instructions as an immediate close signal.
5. Close that UI state only when a later completed assistant message contains the close signal.
6. Cover command injection, signal separation/order, irrelevant messages, and UI open/close transitions with focused tests or the cheapest equivalent repository-local checks.

## Invariants

- Hidden control instructions do not become visible transcript content.
- Normal assistant messages and unrelated signal-like text do not trigger UI transitions.
- Each `message_end` is handled independently; open and close are not inferred from instructions embedded in the same injected control message.
- Opening does not immediately close the UI; closing is accepted only after a prior open transition in the active exercise.
- Existing extension command, session, event, and UI APIs are reused; no new protocol infrastructure or persistent authority is introduced.
- The change is confined to the test extension and genuinely necessary tests; existing unrelated behavior remains unchanged.

## First real unknown

Resolved: `ExtensionAPI.registerCommand()` owns `/start`; `pi.sendMessage({ display: false })` owns hidden instruction injection without starting a turn; `pi.on("message_end", ...)` observes completed messages; and non-awaited `ctx.ui.custom()` plus its captured `done` callback owns the transient TUI lifecycle. Exact whole-message classification ensures one completed assistant message can cause at most one state transition.

## Composition decision

- **Outcome:** the model can open extension UI during a multi-turn tool run and close it only on a later completed message.
- **Overlap and ownership:** the agent owns message completion, the TUI owns rendering, and this extension is the sole acceptance authority for its two signal transitions and the sole holder of the UI dismissal callback.
- **Composition invariant:** an entire assistant message maps to zero or one signal; `close` is legal only while this extension's UI is open.
- **Counterexample:** two independent substring checks both pass when one response contains the open and close tokens, so local open/close handling works while the UI never remains visible.
- **Smallest decision:** reuse the existing message and UI APIs, recognize only an exact standalone signal, and keep one closure-local active/open state rather than add a tool or shared protocol service.

## Planned tracked files

- Create `.pi/extensions/signal-ui.ts`: command registration, hidden protocol message, exact signal classification, and extension-owned UI lifecycle.
- Create `packages/coding-agent/test/signal-ui-extension.test.ts`: behavioral regression coverage for hidden injection and ordered, separate open/close transitions.

## Exact acceptance checks

1. Focused canonical test: `npx tsx ../../node_modules/vitest/dist/cli.js --run test/signal-ui-extension.test.ts` from `packages/coding-agent`. Result: unavailable before collection because `node_modules` is absent; `npx` attempted a registry fetch and failed with `EPERM` under the no-network/no-approval environment.
2. Executable fallback: `node --experimental-strip-types .research_input/phase_a_signal_ui_smoke.mts`. Result: exit 0, `signal UI smoke checks passed`; covers hidden injection, premature close rejection, combined-signal rejection, open, embedded-close rejection, and later exact close.
3. Repository check: `npm run check`. Result: unavailable at its first step because local `biome` is not installed; no lint/type-check result was produced.
4. Syntax checks: `node --experimental-strip-types --check .pi/extensions/signal-ui.ts` and the same command for `packages/coding-agent/test/signal-ui-extension.test.ts`. Result: both exit 0.
5. Diff checks: `git diff --no-index --check -- NUL <file>` for each new tracked file produced no whitespace diagnostics; both complete new-file diffs were inspected against every responsibility and invariant.

## Actual implementation and review evidence

- `/start` registers through the existing extension API and appends one `display: false` custom control message without triggering a model turn.
- The control message requires the open marker on the first assistant turn, the close marker on the final assistant turn, and explicitly forbids both in one response.
- `message_end` handling ignores non-assistant/non-exact text and maps an entire completed assistant message to zero or one signal.
- The open path starts `ctx.ui.custom()` without awaiting it so the agent loop can continue; the close path invokes that same UI instance's captured completion callback only after a later exact close signal.
- Focused tests specify hidden injection, combined/embedded signal rejection, ordered open/close, and close-before-open rejection.
- Five-axis self-review found no required correctness, readability, architecture, security, or performance change. The extension adds no dependency and holds all transition authority in closure-local state.

## Unresolved uncertainty

The canonical Vitest test, Biome formatting/lint, `tsgo` type check, and live interactive TUI path remain unverified in this dependency-free checkout. The local parser and behavioral smoke harness pass, but they do not substitute for the unavailable repository toolchain or an installed interactive runtime.

## Current next action

await late revision
