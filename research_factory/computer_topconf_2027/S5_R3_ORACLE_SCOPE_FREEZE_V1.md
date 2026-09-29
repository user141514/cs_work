# S5 R3 Oracle Scope Freeze V1

date: 2026-09-28
status: FROZEN_OUTCOME_BLIND
task: pi-mono-auto-ec7037ba
source_prompt: S5_R3_SCOPE_ANNOTATOR_INPUT_V1.md
annotator_turn: turn_11f6f0b7777a496098b69d26756b2149
annotator_model: GPT-5.6 Sol
annotator_tools: none
verifier/reference/canonical_goals_exposed: false
post_revision_outcome_exposed: false

## INDEPENDENT_REUSABLE

- Pre-revision commit/history inventory unrelated to autocomplete or file search.
- Verified PR/issue identities and contributor attributions for unrelated changes.
- Unrelated changelog-entry wording/attribution hunks in:
  - packages/ai/CHANGELOG.md
  - packages/tui/CHANGELOG.md
  - packages/coding-agent/CHANGELOG.md
- Unrelated user-facing cross-package duplication decisions.
- Evidence that pre-revision audit touched exactly those three changelog files.

Reuse unit is hunk/provenance level, not whole-file level.

## IMPACTED_RECHECK

- Pre-revision autocomplete/file-search changelog subject.
- Its wording, package placement, attribution and coding-agent duplication.
- Any global claim that the changelog audit is complete.
- Whole-file versions of the three changelogs.
- Prior affected-package boundary, because U7 directly changes TUI behavior and may require coding-agent documentation.

## MUST_REDERIVE

- Cause analysis for directory completion termination.
- Directory-vs-terminal-file completion semantics.
- Required post-selection state for child completion.
- Trailing-space policy.
- Implementation/control-flow/validation decisions for packages/tui/src/autocomplete.ts.
- Exact production/documentation changes for U7.
- Behavioral checks for directory continuation, Tab/Enter, nested paths and terminal files.

No pre-revision autocomplete.ts implementation edit is credited for reuse.

## MINIMAL_R3_CAPSULE

A fresh post-revision agent may receive:
1. exact independent changelog hunks, identified by package/entry;
2. their commit/PR/issue identifiers and verified attribution;
3. independent cross-package duplication decisions;
4. a marker that the autocomplete/file-search changelog subject is invalidated and must be rechecked;
5. U7 behavioral requirement and frozen base source.

## INVALIDATION_RULE

Omit:
- autocomplete/file-search changelog hunk;
- whole-file changelog snapshot as already valid;
- global audit-complete/attribution-complete conclusions;
- trailing-space/directory-continuation reasoning;
- inferred implementation;
- verifier/reference/future-run information;
- any hunk whose provenance cannot be separated from the completion-related subject.

## PRESERVATION_TARGET

Meaningful reuse:
- unchanged unrelated changelog hunks;
- retained commit-to-entry / PR-to-author provenance;
- retained verified attribution strings;
- retained unrelated cross-package duplication decisions.

File survival alone is insufficient.

## COUNTEREXAMPLE

If an allegedly unrelated retained TUI/coding-agent changelog entry is found to describe the same @ completion flow or depends on directory-selection termination semantics, that hunk must be invalidated too.
