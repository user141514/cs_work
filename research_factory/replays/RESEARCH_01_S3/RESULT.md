# RESEARCH-01 Result — S3 Development Workflow Replay

Date: 2026-09-29
Status: COMPLETED_DEVELOPMENTAL_MECHANISM_PASS__WORKFLOW_TRANSITION_BOUNDARY_CONTAMINATED
Task: pi-mono-auto-93c17d3b
Role: DEVELOPMENT_ONLY workflow validation; not held-out evidence and not a paper-effectiveness claim.

## 1. Owned question

Can the frozen workflow handle one real complex late requirement revision by:
- making the active contract explicit;
- separating impacted from independent responsibilities;
- preserving valid prior behavior;
- attacking the first causal counterexample;
- changing only the load-bearing responsibility;
- and passing an endpoint evaluator that was calibrated to reject the pre-revision implementation?

This replay does NOT compare against an old-workflow baseline yet.

## 2. Frozen substrate

Repository: badlogic/pi-mono
Base commit: `5133697bc454da5595cf4b0c70d3c2c725677`
Historical task: SWE-Together `pi-mono-auto-93c17d3b`

Input reconstruction:
- 12 verbatim user messages extracted from `original_session.json`;
- assistant messages excluded;
- `oracle_intents.json`, `oracle_session.jsonl`, `reference_patch.json`, `fix_summary.md` and verifier outcomes were not supplied in the task checkout or prompt. No observed artifact indicates they were used; the provider session was not OS-sandboxed from arbitrary host paths, so non-access is a policy/provenance boundary rather than a mechanically proven property.

Frozen files:
- `PRE_REVISION_REQUIREMENTS.md` SHA256 `f1010e3e37e5ae5f042d5bd442840275cf00de0837dd496712edaea5f2211c30`
- `LATE_REVISION.md` SHA256 `f7635fb88bb2ce578ace71acbbe36d352a7888abf4e20b16ea9313d83a970ca7`

Execution arm:
- fresh Codex provider session;
- model GPT-5.6 Sol;
- effort xhigh;
- same provider session reused for Phase B;
- agent id `agt_4cb18c56`;
- provider session prefix `01a0ebd4`.

## 3. Temporal separation

### Phase A — pre-revision

The late revision file did not exist in the task checkout.

The agent first wrote `PHASE_A_PLAN.md` before modifying tracked deliverables. It decomposed the task into six independently checkable responsibilities and six invariants.

Phase-A implementation:
- `.pi/extensions/signal-ui.ts`
- `packages/coding-agent/test/signal-ui-extension.test.ts`

Phase-A completion:
- 2026-09-29T06:50:51.366Z
- provider duration: 1,701,705 ms (~28.36 min)

Authoritative Phase-A freeze: `phase_a/PHASE_A_SNAPSHOT.json`, captured at 2026-09-29 14:51:21 +08:00, after the valid 06:50:51Z completion and before the extra turn began at 06:51:55Z.

Phase-A frozen hashes:
- extension: `4b161319e53b11fc8d2e8e6cd7fc64fb1fa2c3f003cfe2b41bae0befb5792f3e`
- focused test: `b0392576cd62b2bcd82d6c75a10b8179dba8efd1654a125f3d42deb3ad5ffef5`
- plan: `8260575e608f202d2a61c8a61f8938a883379a576572325fe9d0be1fd53ed5ca`

### Boundary incident

After the valid Phase-A completion, an extra provider turn on the same session started without any late revision input. Its cause was not established. It was stopped to preserve the phase boundary.

- started: 2026-09-29T06:51:55.057Z
- terminated/failure recorded: 2026-09-29T06:58:00.178Z
- duration: 365,121 ms (~6.09 min)
- the extension and Phase-A plan remained byte-identical, but the focused test drifted by +20/-3 lines: `b0392576...` → `d48e1e64...`;
- the post-incident state is retained under `phase_a_post_completion_incident/` and is INVALID as the Phase-A boundary;
- count this as workflow/process overhead and a temporal-boundary violation, not a scientific/task failure.

### Phase B — late revision

Only after the authoritative Phase-A snapshot existed was `LATE_REVISION.md` introduced. However, the live checkout inherited the extra turn's modified focused test rather than being restored byte-for-byte to the authoritative Phase-A snapshot. Therefore the Phase-B implementation outcome is usable developmental mechanism evidence, but the Phase-A→Phase-B workflow transition is not a clean controlled intervention.

Phase B:
- started: 2026-09-29T06:59:20.959Z
- completed: 2026-09-29T07:07:57.390Z
- provider duration: 516,434 ms (~8.61 min)

The Phase-B plan explicitly separated:
- six Phase-A responsibilities that remain independent;
- one impacted responsibility: the UI projection/lifecycle mechanism;
- preserved invariants;
- the new invariant that the editor remain installed/focused/typable while signal status is visible;
- two counterexamples to naive fixes.

## 4. Mechanism discovered

The user suspected repeated UI recreation on streaming/update paths.

The agent inspected the actual repository mechanism and found a different root cause:

`exact OPEN at message_end`
→ Phase-A `ctx.ui.custom()`
→ core `showExtensionCustom()` removes/replaces the normal editor and focuses the custom component
→ transcript rendering can continue, but typing is unavailable
→ editor returns only when the custom UI's `done()` restores it.

The extension did NOT use `message_update`; the freeze was therefore not caused by per-token UI recreation.

This is decision-relevant because it changes the repair.

## 5. Minimal intervention

Phase A already had:
- /start;
- hidden protocol injection;
- exact whole-message signal classification;
- message_end event boundary;
- ordered open/close state;
- combined/embedded/premature signal rejection.

Phase B preserved those and changed only UI projection:

`ctx.ui.custom()` / captured dismiss callback
→ keyed `ctx.ui.setWidget()` / boolean `uiOpen`.

Final mechanism check:
- no `message_update` handler in the extension;
- no `ui.custom`;
- one `message_end` handler;
- keyed `setWidget` open/clear operations.

## 6. Independent endpoint evaluator

Evaluator:
`S3_ENDPOINT_EVALUATOR.mts`

It was built from:
- the visible user contract;
- public task verifier semantics;
- repository UI API semantics.

It does NOT use the reference patch.

Evaluator runtime was fixed to Bun 1.3.14 after Node 24 experimental strip-types emitted the correct JSON but hit a Windows/libuv exit assertion. This runtime issue is evaluator infrastructure only.

### Calibration on Phase A

Same evaluator, before reading Phase-B output:

- public_behavior_pass = true
- lifecycle_pass = false
- overall pass = false
- customCalls = 1
- widgetSetCalls = 0

Specific failures:
- editor_available_while_open = false
- open_uses_nonblocking_projection = false
- editor_available_during_streaming = false

Expected exit code under Bun: 2.

This calibration is important: the evaluator distinguishes “functional protocol works” from “the UI is usable.”

### Final Phase B evaluation

Same evaluator, unchanged rule:

- public_behavior_pass = true
- lifecycle_pass = true
- overall pass = true
- customCalls = 0
- widgetSetCalls = 1
- widgetClearCalls = 1
- all 15 checks = true

Independent syntax checks of both final TypeScript deliverables passed with Node strip-types.

The evaluator itself imported the final extension successfully under Bun.

## 7. Rework / preservation

Exact Phase-A → Phase-B textual change:

Extension:
- +14 / -33 lines
- Phase A lines: 100
- Phase B lines: 81
- exact Phase-A lines retained: 67
- exact-line preservation fraction: 0.67

Focused test, measured against the authoritative first-completion Phase-A snapshot:
- +27 / -3 lines
- Phase A lines: 142
- Phase B lines: 166
- exact Phase-A lines retained: 139
- exact-line preservation fraction: 0.9789

Of that test rework, +20/-3 lines occurred during the invalid post-completion extra turn before the late revision. Therefore this test rework cannot be attributed to the late-revision workflow intervention.

Interpretation:
- the extension protocol contract was largely preserved and the implementation deletion/replacement mass is concentrated in the custom UI lifecycle;
- no Phase-A protocol responsibility was intentionally discarded;
- test preservation is high, but its causal attribution is contaminated by the pre-late extra turn and must not be used as clean workflow-benefit evidence.

Exact-line preservation is a descriptive artifact metric, not a semantic proof.

## 8. Executing-arm checks and limitations

The arm demonstrated RED → GREEN:
- new editor-availability smoke failed on Phase-A code;
- after the UI projection change the same smoke passed.

Available checks:
- local Node smoke PASS after repair;
- TypeScript syntax checks PASS;
- diff whitespace checks PASS.

Unavailable in this dependency-free checkout:
- canonical Vitest collection;
- Biome;
- tsgo;
- live interactive TUI.

Phase A attempted an ordinary `npx` command that tried to reach the registry and was blocked by the no-network environment. Phase B used `npx --offline`. The blocked Phase-A attempt is retained as a process-constraint deviation.

No official benchmark reward is claimed.

## 9. What this supports

Supported developmental mechanism observation:

The structured arm produced one complex requirement-evolution solution that visibly follows:

`new requirement`
→ identify impacted responsibility
→ preserve independent invariants
→ construct a causal counterexample
→ produce RED evidence
→ make a local mechanism change
→ independently re-evaluate endpoint.

The concrete implementation result is stronger than “it produced a plan”: the authoritative Phase-A extension passed functional behavior but failed the lifecycle invariant; the final Phase-B extension changed one mechanism family and passed the same calibrated endpoint evaluator. Because the actual Phase-B checkout inherited a drifted test artifact, this does not establish a clean end-to-end workflow transition.

## 10. What this does NOT support

Do not claim:
- workflow superiority over the old/raw workflow;
- publication novelty;
- SOTA;
- held-out generalization;
- official SWE-Together score;
- lower model cost;
- that orthogonality/invariants caused the success rather than ordinary strong-agent reasoning.

The parent task was known historically and this is a DEVELOPMENT_ONLY replay.

## 11. Decision

KEEP the workflow hypothesis, but DO NOT use this run as the treatment arm of a direct superiority comparison.

The first true unknown is now comparative under a clean boundary:

> From the exact authoritative Phase-A bytes, does mandatory responsibility/invariant/counterexample scaffolding improve late-revision behavior versus an ordinary strong raw agent under identical model/input/evaluator conditions?

Until that is measured, “our workflow is better” is unsupported. The accidental extra turn is itself evidence that temporal state ownership must be included in workflow evaluation.

## Exactly one NEXT_STEP — not executed

ID: RESEARCH-02
Status: PLANNED_NOT_AUTHORIZED

Run a clean paired late-revision replay from the exact authoritative `phase_a/` bytes, not from the contaminated live checkout.

Create two isolated identical arms:
- STRUCTURED: fresh GPT-5.6 Sol/xhigh, exact Phase-A code/tests + PRE_REVISION_REQUIREMENTS + LATE_REVISION, with mandatory goal/responsibility/invariant/counterexample/one-step replanning scaffolding;
- RAW_AGENT: fresh GPT-5.6 Sol/xhigh, exact same Phase-A code/tests + PRE_REVISION_REQUIREMENTS + LATE_REVISION and contamination boundary, but no mandatory structured-workflow scaffolding.

Both use:
- same dependency-free runtime constraints;
- same already-frozen independent endpoint evaluator;
- no historical Phase-B plan/final code or endpoint result;
- fresh provider sessions and isolated checkouts.

Compare:
- endpoint PASS/failure;
- provider wall time;
- process deviations;
- authoritative Phase-A → final rework;
- preservation of valid pre-revision behavior.

This isolates the late-revision workflow intervention and avoids paying to regenerate Phase A.

RESEARCH-02 remains DEVELOPMENT_ONLY. Do not use it as publication evidence.
