You are an outcome-blind dependency-scope annotator for a controlled coding-agent experiment.

Your ONLY job is to classify which pre-revision derived work can be safely reused after a late requirement change, and which reasoning must be rederived.

You are deliberately NOT given any benchmark verifier, hidden tests, reference patch, gold solution, canonical goals, post-revision run, or successful future trajectory. Do not infer or invent them.

## Frozen task initial state

Repository: badlogic/pi-mono
Commit: 69d02b8a5fce07041f77aba64c6ebbc8589827ab

Relevant base source in packages/tui/src/autocomplete.ts:

```ts
applyCompletion(
    lines: string[],
    cursorLine: number,
    cursorCol: number,
    item: AutocompleteItem,
    prefix: string,
): { lines: string[]; cursorLine: number; cursorCol: number } {
    const currentLine = lines[cursorLine] || "";
    const beforePrefix = currentLine.slice(0, cursorCol - prefix.length);
    const afterCursor = currentLine.slice(cursorCol);

    const isSlashCommand =
        prefix.startsWith("/") &&
        beforePrefix.trim() === "" &&
        !prefix.slice(1).includes("/");

    if (isSlashCommand) {
        const newLine = `${beforePrefix}/${item.value} ${afterCursor}`;
        ...
    }

    if (prefix.startsWith("@")) {
        const newLine = `${beforePrefix + item.value} ${afterCursor}`;
        const newLines = [...lines];
        newLines[cursorLine] = newLine;

        return {
            lines: newLines,
            cursorLine,
            cursorCol: beforePrefix.length + item.value.length + 1,
        };
    }

    ...
}
```

Thus the late trailing-space behavior is present in the frozen base itself.

## Frozen pre-revision user requirements

U1:
Audit changelog entries for all commits since the last release. For affected packages, add missing entries, verify external contribution attribution format, and duplicate user-facing ai/agent/tui changes into coding-agent where appropriate.

U2:
double check that all attributions are correct by locating the issues/prs via gh cli

U3:
where's the terrobe pr?

U4:
how many more cl entries did you fuck up?

Workflow-only commit/push/release requests are excluded from the controlled scientific requirement sequence.

## Public pre-revision derived-work summary

The historical public trace through U4 shows the relevant type and scale of pre-revision work:
- audited git history and three package changelogs;
- checked multiple PR/issue authors;
- modified exactly:
  - packages/ai/CHANGELOG.md
  - packages/tui/CHANGELOG.md
  - packages/coding-agent/CHANGELOG.md
- cumulative pre-revision patch was approximately +25 / -6 lines across those three files;
- the modifications included many changelog entries/attributions for unrelated features/fixes across ai/tui/coding-agent;
- one pre-revision changelog subject concerns autocomplete/file-search behavior, so not every changelog decision is guaranteed independent of the late revision;
- no pre-revision production edit to packages/tui/src/autocomplete.ts is part of this derived-work summary.

The actual scientific run will generate its own pre-revision snapshot with the fixed model. This public trace is only used to classify dependency shape before outcomes.

## Late revision U7

The user reports a behavioral regression in @ file completion:

- typing/selecting a directory such as @packages completes to @packages/ followed by a trailing space;
- the completion list then disappears;
- tab and enter both terminate completion;
- deleting the space and invoking completion again exposes child folders;
- user asks why directory selection adds a space and wants a better pattern.

Frozen behavioral requirement:
1. selecting a directory in @ file completion must not append a terminating space;
2. the resulting directory path must remain eligible for continued child-path completion;
3. terminal file selections may keep terminating behavior when appropriate.

## Classification target

Classify PRE-REVISION derived work into exactly three sets:

INDEPENDENT_REUSABLE:
work whose validity does not depend on how U7 is implemented and can be carried forward unchanged.

IMPACTED_RECHECK:
work still potentially useful but needing revalidation because U7 changes the behavior or its documentation surface.

MUST_REDERIVE:
reasoning/decisions that directly concern the completion behavior or must be recomputed to satisfy U7.

Then give:
- MINIMAL_R3_CAPSULE: smallest state capsule a fresh post-revision agent may receive while legitimately reusing independent prior work.
- INVALIDATION_RULE: what must be omitted from that capsule.
- PRESERVATION_TARGET: concrete artifact categories whose survival would count as meaningful reuse.
- COUNTEREXAMPLE: one observation that would prove your dependency classification too optimistic.

Do not propose a solution patch. Do not use hidden benchmark knowledge.