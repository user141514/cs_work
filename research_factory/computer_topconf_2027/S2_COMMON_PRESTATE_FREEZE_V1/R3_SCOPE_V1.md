# S2 Outcome-Blind R3 Scope V1

date: 2026-10-01
status: FROZEN_OUTCOME_BLIND
task: pi-mono-auto-a4fca584
common_prestate: S2_COMMON_PRESTATE_FREEZE_V1
post_revision_outcome_exposed: false
reference_patch_exposed: false
verifier_outcome_exposed: false
development_phase_b_exposed: false

## Basis

This scope is frozen only from:
- the immutable post-U3 common-prestate bytes;
- the already-frozen late-revision requirement bundle, source indices 37/39;
- the dependency rule in `S2_STAGE_B_BOUNDARY_FREEZE_V1.md`.

Frozen late semantic correction:

> when a local package path is written to settings, its persistent meaning must be relative to the specific `settings.json` receiving the entry rather than being materialized from the caller's cwd into an absolute stored path.

Known pre-revision fact, frozen before this scope:
- U2 implementation stores relative CLI paths as lexical absolute paths;
- U3 verifies user/global and project-local settings both persist that absolute path;
- relative-path basis is caller cwd.

No 37/39 execution, R2/R3 output, reference patch, verifier result, canonical goal or future successful repair was inspected to construct this scope.

## Exact common-prestate project state

Base:
`e54dff7efb460e364a39e4a22369991a20c105b9`

Tracked patch:
`S2_COMMON_PRESTATE_FREEZE_V1/tracked_dirty.patch`

SHA256:
`6d072b1f42bc39306b9a9e494ee631cd19712eac979aeca52f79fb2149a71c75`

Material derived work spans seven tracked files.

Whole-file reuse is forbidden.

## AFFECTED / MUST REDERIVE OR REVALIDATE

These pre-revision derived units encode the old cwd/absolute persistence basis and must not be accepted as reusable solution code.

### `packages/coding-agent/src/main.ts`

- lines 8-9 — imports introduced solely for the pre-revision local-path resolver;
- lines 87-93 — `resolveLocalPackagePath(...)`, which expands local CLI input to an absolute path using process/caller cwd;
- line 110 — local source normalization key becomes the absolute-path helper result;
- lines 136-137 — derives `storedSource` from the affected absolute normalization;
- line 142 — writes that normalized absolute source into settings.

These units sit directly on the late-revision semantic boundary.

### `packages/coding-agent/docs/packages.md`

Line 77 contains mixed semantic clauses.

Affected clause only:

> Relative paths passed to `pi install` are stored as absolute paths.

That clause must be rewritten or removed under the late requirement.

The rest of line 77 is not automatically invalidated; see INDEPENDENT_REUSABLE.

## REVALIDATE_ONLY

These units retain useful intent but cross the same path-semantics boundary and therefore require explicit post-revision validation.

### `packages/coding-agent/src/core/package-manager.ts`

- lines 724-727 — local source existence validation through the existing cwd-based `resolvePath(parsed.path)`.

The likely retained responsibility is:
- a relative CLI argument still has to locate the source from the invocation context.

But R3 must verify that this runtime source lookup remains cleanly separated from how the path is persisted into user/project settings.

### `packages/coding-agent/README.md`

- line 339 — local paths are referenced in place and `-l` uses project settings.

The feature/scope description likely remains valid, but R3 must recheck wording after settings-file-relative persistence is introduced.

## INDEPENDENT_REUSABLE

The following pre-revision derived units do not depend on whether persisted local paths are absolute or settings-file-relative.

1. `CHANGELOG.md:12` — feature claim that `pi install` / `pi remove` support local paths.
2. `README.md:332` — local-path install example.
3. `docs/packages.md:26-27` — local package/file install examples.
4. `docs/packages.md:77`, clause:
   > Local paths can be registered with `pi install` or added directly to settings.
5. `docs/packages.md:77`, remaining in-place/source-lifetime/file-vs-directory clauses:
   local sources are referenced in place; remove does not delete source; file/directory package loading behavior.
6. `docs/settings.md:143` — `packages` may contain npm, git or local packages.
7. `src/core/package-manager.ts:742-744` — local remove does not uninstall/delete the source.
8. `src/core/settings-manager.ts:44,74` — settings type/comments recognize local package sources.

These may be retained if still compatible with the final spec.

## AFFECTED CONTEXT — NO DERIVED-WORK REUSE CREDIT

These lines are unchanged base code and are therefore not pre-revision derived-work units, but R3 must reason about them because affected code depends on them.

### `src/main.ts:113-125`

`sourcesMatch` / `packageSourcesMatch` consume the affected local normalization key.

R3 must rederive or revalidate equivalence/dedup/removal across:
- CLI input relative to caller cwd;
- entries persisted relative to user settings;
- entries persisted relative to project settings.

These unchanged lines get zero reuse credit by themselves.

### `src/main.ts:134-150`

The existing user/project settings selection and write calls surround the affected storage/dedup/remove logic.

The unchanged scope-selection/write context gets zero derived-work reuse credit.

### `src/core/package-manager.ts:1180-1193`

Existing helpers:
- `resolvePath(input)` — caller-cwd resolution;
- `resolvePathFromBase(input, baseDir)` — explicit-base resolution.

These are base primitives useful for rederivation, not derived-work reuse units.

## MIXED-LINE INVARIANT

`docs/packages.md:77` contains both affected and independent clauses.

Therefore:
- whole-line reuse credit is forbidden;
- a later diff that preserves the line path/number is not evidence of reuse;
- reuse must be adjudicated clause-by-clause.

## MINIMAL R3 CAPSULE

A fresh R3 post-revision agent may receive:

- the frozen final requirements including late bundle 37/39;
- the frozen base source;
- the INDEPENDENT_REUSABLE units above;
- the REVALIDATE_ONLY units above;
- an explicit statement that the old absolute-path persistence units are invalidated;
- the affected-context dependency notes above.

It must not receive:

- the affected pre-revision absolute-path implementation as accepted solution code;
- any post-revision output;
- R2 result/implementation;
- reference/gold patch;
- verifier outcome;
- oracle session/intents;
- canonical goals;
- future successful diff;
- whole-file or mixed-line reuse credit.

## Reuse accounting invariant

Later R3 reuse accounting must use:
- the immutable bundle bytes;
- the semantic unit classes in `derived_work_manifest.json` and this scope.

A retained AFFECTED unit gets zero independent-reuse credit unless it is explicitly rederived/revalidated under the final requirement.

A file surviving by path/name is not reuse by itself.

## Scope status

`S2_R3_SCOPE = FROZEN_OUTCOME_BLIND`

This scope is frozen before:
- late revision 37/39 execution;
- R2 execution;
- R3 execution.
