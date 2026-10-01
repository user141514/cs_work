# S3 Outcome-Blind R3 Scope V1

date: 2026-10-01
status: FROZEN_OUTCOME_BLIND
task: pi-mono-auto-93c17d3b
common_prestate: S3_COMMON_PRESTATE_FREEZE_V1
post_revision_outcome_exposed: false
reference_patch_exposed: false
verifier_outcome_exposed: false
development_phase_b_exposed: false

## Basis

This scope is frozen only from:
- the immutable post-U5 common-prestate bundle;
- the already-frozen U6 semantic requirement;
- the pre-registered dependency rule in `S3_STAGE_B_BOUNDARY_FREEZE_V1.md`.

The late revision is known only as a requirement:
while assistant output/streaming occurs with the signal UI active, input/editor responsiveness must remain usable; UI projection/lifecycle must not repeatedly recreate, replace, focus-steal or block the input surface.

No U6 execution, R2/R3 output, reference patch, verifier result, canonical goal or RESEARCH-01 Phase-B solution was inspected to create this scope.

## Exact artifact

Only one material pre-revision task artifact exists:

`.pi/extensions/message-signals.ts`

Frozen copy:
`S3_COMMON_PRESTATE_FREEZE_V1/artifacts/.pi/extensions/message-signals.ts`

SHA256:
`1d76a1742be2dee3356f770cb6bb7385565d3aaa1e4eaa5bc64f665875ac4080`

Whole-file reuse is forbidden because independent protocol logic and late-revision-dependent UI projection coexist in this file.

## AFFECTED / MUST_REDERIVE_OR_REVALIDATE

Exact pre-U6 projection seam:

- line 19: `WIDGET_KEY` — identity of the persistent projected widget;
- lines 51-59: `setWorkflowWidget` / `clearWorkflowWidget`, including `ctx.ui.setWidget(... placement: "aboveEditor")`;
- line 96: initial active-widget projection during `/start`;
- line 120: widget clear on DONE;
- line 126: paused/waiting-widget projection on INPUT;
- line 132: widget clear when input is cancelled/empty;
- line 137: active-widget projection before hidden follow-up;
- line 151: widget clear on session switch.

These exact lines determine how persistent/open signal state is projected into the interactive TUI/editor and therefore lie on the frozen late-revision causal boundary.

R3 must not treat their pre-U6 implementation as valid reusable solution code.

## REVALIDATE_ONLY

These retained UI-facing behaviors are not themselves the frozen projection repair, but they cross the same interaction boundary and must be rechecked after U6:

- line 127: `ctx.ui.input(...)` user-input collection;
- line 121: completion notification;
- line 133: cancelled-input notification.

Their intent may be retained; their post-U6 interaction behavior cannot be credited without revalidation.

## INDEPENDENT_REUSABLE

The following semantic/code units do not depend on the late projection/focus/update defect and may be retained by R3:

1. signal/control constants excluding `WIDGET_KEY`: lines 18, 20-21;
2. assistant text extraction and standalone signal classification: lines 25-48;
3. hidden control-protocol construction and ordered INPUT/DONE contract: lines 61-76;
4. command registration, idle/UI admission, active/awaiting state initialization: lines 79-95;
5. hidden custom-message injection on start: lines 98-107;
6. message-end admission, assistant/stop filtering, signal extraction and DONE state transition excluding projection calls: lines 109-119;
7. INPUT state transition excluding projection/input UI calls: lines 122-125 and 128-131;
8. retained post-input control flow excluding projection/notification calls: lines 134-136;
9. hidden follow-up message injection with `deliverAs: "followUp"`: lines 138-145;
10. session-switch state reset excluding widget clear: lines 148-150.

Reuse means semantic/hunk reuse only. It does not authorize copying the whole pre-U6 file unchanged.

## MINIMAL R3 CAPSULE

A fresh R3 post-revision agent may receive:

- the frozen final requirements including U6;
- the frozen base source;
- the independent reusable semantic/code units above;
- an explicit marker that the UI projection seam is invalidated and must be rederived/revalidated;
- the REVALIDATE_ONLY list above.

It must not receive:
- pre-U6 projection code as an accepted solution;
- any post-U6 result;
- reference/gold patch;
- verifier outcome;
- RESEARCH-01 Phase-B diagnosis/repair;
- whole-file reuse credit.

## Reuse accounting invariant

Later reuse accounting must use this frozen hunk classification and the immutable bundle bytes.

A retained line inside an AFFECTED hunk gets zero independent-reuse credit unless the post-U6 agent rederives/revalidates it under the new requirement.
A file surviving by path/name is not reuse by itself.
