# S5 Autocomplete Evaluator Correction Receipt V1

date: 2026-09-28
status: CORRECTION_FROZEN_BEFORE_R3_OUTCOME
task: pi-mono-auto-ec7037ba
affected_endpoint: U7 autocomplete directory completion behavior

## 1. Observed evaluator conflict

The path-adapted official SWE-Together verifier on valid R2 produced:
- changelog structure: PASS;
- changelog growth: PASS;
- changelog attribution: PASS;
- t7 directory no-trailing-space: FAIL;
- t7 directory marker: FAIL;
- raw local-equivalent reward: 0.5000.

The verifier detail for both T7 gates was:
`could not invoke autocomplete module behaviorally`.

R2's own focused real-provider regression test passed 6/6 and directly exercised directory -> child completion plus terminal-file spacing.

Therefore R2 could not be interpreted scientifically until the evaluator mismatch was adjudicated.

## 2. Concrete defect

The official behavioral probe enumerates exported values with `typeof value === "function"` and invokes them as ordinary functions.

The repository exposes the relevant API as the exported class:
`CombinedAutocompleteProvider`.

A JavaScript class has `typeof === "function"` but cannot be invoked without `new`.
The probe catches invocation exceptions and therefore can reach `hasResults=false` without testing `applyCompletion` or `getForceFileSuggestions`.

This defect exists independently of the R2 implementation.

## 3. Frozen correction

Correction script:
`research_factory/computer_topconf_2027/verify_s5_autocomplete_behavior.mts`.

It uses only the repository's existing public class API:
- instantiate `CombinedAutocompleteProvider([], sandbox)`;
- obtain real root file/directory suggestions;
- select `@nested/`;
- run `applyCompletion`;
- verify no terminating space and exact cursor position;
- call `getForceFileSuggestions` again and require child visibility;
- separately require terminal-file completion to retain its terminating space.

No reference patch, gold diff, hidden canonical goal or future successful trajectory is read.

## 4. Counterexample acceptance

Frozen base commit 69d02...:
- directoryMarker = true;
- fileMarker = true;
- directoryNoTrailingSpace = false;
- directoryContinues = false;
- fileTerminatesWithSpace = true;
- u7Pass = false.

R2 full-restart worktree:
- directoryMarker = true;
- fileMarker = true;
- directoryNoTrailingSpace = true;
- directoryContinues = true;
- fileTerminatesWithSpace = true;
- u7Pass = true.

Thus the correction discriminates the known buggy base from the independently produced R2 implementation on the exact U7 behavior.

## 5. Scientific adjudication

The original raw 0.5000 verifier artifact is retained as evaluator evidence and is not rewritten.

For Stage-B scientific correctness:
- R2 changelog gates PASS;
- corrected U7 behavioral endpoint PASS;
- R2 is accepted as a valid clean-final-spec behavioral reference for S5.

The correction is frozen before R3 scientific outcome and must be applied unchanged to R3/R0/R1.

If the corrected probe had also passed on the frozen base, it would be non-discriminating and R2 would remain non-identifiable. It did not.
