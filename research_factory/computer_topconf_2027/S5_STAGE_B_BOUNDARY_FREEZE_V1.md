# S5 Stage-B Boundary Freeze V1 — pi-mono-auto-ec7037ba

date: 2026-09-28
status: OFFLINE_BOUNDARY_FROZEN__R3_SCOPE_PENDING
parent: STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
task: pi-mono-auto-ec7037ba
scientific_result_observed: false

## 1. Official task initial state

Current public SWE-Together environment/Dockerfile hard-checks out:

69d02b8a5fce07041f77aba64c6ebbc8589827ab

Commit subject:
fix(coding-agent): use dynamic paths in error messages (#887)

This is the authoritative Stage-B TASK_INITIAL_STATE.

The historical original session was recorded against a later live repository state, but the current public benchmark image deliberately reconstructs from the declared base commit.

Substrate-validity check:
the late T7 defect already exists at the official base commit.

At packages/tui/src/autocomplete.ts::applyCompletion the base code contains:

if (prefix.startsWith("@")) {
    const newLine = `${beforePrefix + item.value} ${afterCursor}`;
    ...
    cursorCol: beforePrefix.length + item.value.length + 1;
}

Therefore the directory-completion trailing-space defect is observable without requiring later PR #882 code to be present.

## 2. Controlled authoritative pre-revision sequence

### U1 — changelog audit

Use the exact initial instruction:
Audit changelog entries for all commits since the last release, verify missing entries and cross-package duplication, and add missing entries.

### U2 — attribution verification

Exact:
double check that all attributions are correct by locating the issues/prs via gh cli

### U3 — missed attribution correction

Exact:
where's the terrobe pr?

Classification:
diagnostic/correction turn tied to the changelog audit.

### U4 — broader attribution correction

Exact:
how many more cl entries did you fuck up?

Classification:
diagnostic/correction turn; requires another attribution audit and may change changelog artifacts.

### REVISION_BOUNDARY

Immediately after U4 completes.

T5 "commit and push" and T6 "then do a new patch release" are WORKFLOW_ONLY for controlled Stage B.
They are excluded from the scientific requirement sequence and from the shared pre-revision execution because:
- they do not change externally observable product behavior;
- they introduce remote/release side effects;
- the intended comparison is derived-state validity, not Git hosting or release capability.

Historical T5/T6 remain provenance showing that the original session had reached release-oriented work; they are not active requirements.

### U7 — late behavioral revision

Verbatim late requirement context/request:
the user reports that @ directory completion adds a trailing space for tab/enter, causes the file-completion list to disappear, and asks for a pattern where directory selection does not add the terminating space and child completion can continue.

Controlled behavioral requirement:
- selecting a directory in @ file completion must not append a terminating space;
- the resulting directory path must remain eligible for continued child-path completion;
- terminal file selections may retain completion termination behavior when appropriate.

### Historical U8 — excluded workflow turn

"ok commit and push"

Workflow only; not part of the behavioral final specification.

## 3. Pre-revision public-trace pressure

The public oracle trace through U4 records substantial derived work:
- changelog audit across packages/ai, packages/tui and packages/coding-agent;
- multiple git-history inspections;
- multiple GitHub PR/issue attribution checks;
- modifications to three changelog files;
- public-trace cumulative pre-revision patch at U4: 3 files, approximately +25 / -6 lines;
- many unrelated changelog judgments that are semantically independent of the later autocomplete implementation.

This is materially larger pre-revision derived state than S1.

The public trace is used only for substrate/headroom analysis.
The actual controlled pre-revision snapshot for scientific arms must be produced once by the fixed GPT-5.6 Sol/xhigh configuration.

## 4. Consolidated active spec before U7

Derived only from allowed user requirements:
1. audit changelog entries for commits visible from the frozen task initial state;
2. add missing entries under the supplied changelog rules;
3. verify external PR/issue attributions and correct attribution mistakes;
4. maintain cross-package duplication for user-facing changes.

No release/push obligation is part of the controlled contract.

## 5. Consolidated final spec for R2

1. Start from the frozen public task initial state at 69d02b8a5fce07041f77aba64c6ebbc8589827ab.
2. Complete the changelog audit and attribution/cross-package corrections required above.
3. Fix @ directory completion so selecting a directory does not append a trailing terminating space and users can continue completion into child paths.
4. Preserve terminal completion behavior for file selections unless the implementation requires a narrowly justified change.
5. Run repository-relevant correctness checks for the modified completion behavior.

Do not use later git history, reference patches, gold diffs, verifier outcomes or future successful trajectories.

## 6. Fixed agent/runtime

Same as S1:
- GPT-5.6 Sol
- xhigh
- OMP under lifetime
- read,bash,edit,write,grep,glob
- no extra skills/rules/extensions
- one writer per isolated checkout
- task-correct Node/Bun runtime

## 7. Current first unresolved transition

Freeze outcome-blind R3 impact/independent scope using only:
- U1-U4 requirements;
- U7 late requirement;
- official base source structure;
- public pre-revision artifact summary.

Then apply Execution Leverage Gate before paying for any S5 model run.
