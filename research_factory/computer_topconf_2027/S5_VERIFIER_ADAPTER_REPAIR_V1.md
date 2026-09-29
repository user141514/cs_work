# S5 Verifier Adapter Repair V1

date: 2026-09-28
status: FROZEN_BEFORE_R3
task: pi-mono-auto-ec7037ba
scope: local-equivalent evaluator repair only
scientific_outcome_changed: no

## 1. Trigger

The first local-equivalent evaluation of the completed S5 R2 arm returned reward 0.5000 because both weighted T7 gates reported:

- t7_f2p_autocomplete_dir_no_trailing_space = false
- t7_f2p_autocomplete_dir_marker = false
- detail = "could not invoke autocomplete module behaviorally"

This result is invalid for scientific adjudication.

## 2. Root cause

The public task module exports:

`CombinedAutocompleteProvider`

as a class. The public verifier's generic behavioral probe enumerates exported JavaScript functions and invokes them as ordinary callables.

A JavaScript class has `typeof === "function"`, but calling the constructor with `fn.apply(...)` throws. The verifier swallows that exception, so the result set is empty.

Therefore the original probe cannot observe the actual task API surface.

The public canonical reference patch confirms the problem is evaluator-side:
- it modifies only `CombinedAutocompleteProvider.applyCompletion()` for the U7 behavior;
- it does not add a standalone exported completion function;
- consequently the old generic probe would also fail to observe the canonical correct implementation.

The unrelated base64-encoded `cd /workspace/pi-mono` CI-prelude diagnostic is not the cause of the weighted T7 failure and is not used to justify the repair.

## 3. Repair object

Authority:
`s5_autocomplete_evaluator_probe.mjs`

The repaired probe uses the existing public class API directly:

1. instantiate `CombinedAutocompleteProvider`;
2. call `applyCompletion()` with a real-shape @ directory item:
   `{ value: "@src/", label: "src/" }`;
3. require:
   - output exactly `@src/`;
   - no terminating space;
   - cursor immediately after the slash;
4. call the same API with a terminal file item:
   `{ value: "@README.md", label: "README.md" }`;
5. require terminal-file behavior remains `@README.md ` with cursor after the space.

No R2/R3 output, reference diff, hidden verifier result, or future trajectory is used as probe input.

## 4. Pre-freeze counterexample validation

Before changing the local adapter:

### Frozen base
source:
`external/spec_stageb_s5_base_69d02/packages/tui/src/autocomplete.ts`

Observed:
- dirNoTrailingSpace = false
- dirMarker = false
- fileTerminates = true
- directory line = `@src/ `

Expected negative reproduced.

### Public canonical reference patch
evaluator-only isolated clone:
`D:/stageb_agent_runtime/evaluator/s5-reference`

Observed:
- dirNoTrailingSpace = true
- dirMarker = true
- fileTerminates = true

Expected positive reproduced.

The public reference patch is used **only** for evaluator validation after the R3 outcome-blind scope had already been frozen. It is never exposed to R2/R3 model prompts or R3 dependency-scope construction.

### Existing R2 arm
Observed:
- dirNoTrailingSpace = true
- dirMarker = true
- fileTerminates = true

This is not accepted as scientific evidence until the repaired full verifier is rerun.

## 5. Gate identity and weights

Do not invent a new scoring rule.

Keep the existing weighted gates and weights exactly:

- t1_f2p_changelog_unreleased_grew = 0.25
- t1_f2p_changelog_attribution_format = 0.25
- t7_f2p_autocomplete_dir_no_trailing_space = 0.30
- t7_f2p_autocomplete_dir_marker = 0.20

Only the observation implementation for the two existing T7 gates changes.

`fileTerminates` is a non-weighted evaluator sanity / requirement-preservation observation. It must be reported, but it does not add reward weight.

## 6. Evidence preservation

For every repaired local verifier run:

- preserve the original public-verifier gates as `gates.official_raw.json`;
- write the direct probe output as `evaluator_probe.json`;
- write corrected final gates to `gates.json`;
- recompute `reward.txt` from the unchanged four weights.

No other gate is altered.

## 7. Acceptance before R3

The repaired adapter is valid only if:

1. frozen base => corrected reward 0.0000;
2. public reference patch => corrected T7 PASS and corrected reward 1.0000;
3. existing R2 => corrected verifier executes without adapter error;
4. reference/base validation identities remain outside all scientific agent contexts.

Only then may R2 correctness be accepted and R3 start.
