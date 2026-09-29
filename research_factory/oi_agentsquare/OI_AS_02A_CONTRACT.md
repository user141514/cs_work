# OI-AS-02A — Luna/Medium Manipulation Check

Date: 2026-09-29
Parent: OI-AS-02
Status: AUTHORIZED_SUBSTEP

## Purpose

Verify with the real frozen model condition that the intervention actually changes authority semantics before any ALFWorld environment work.

## Frozen model condition

- Codex CLI
- GPT-5.6 Luna
- reasoning effort: medium
- same invocation path for both arms
- one call per arm
- no tools/files/web requested from the model

## Frozen input

Both arms receive the same ALFWorld-like successful trajectory and the same ongoing task.

## Arms

Original TP prompt: copied semantically from frozen AgentSquare MemoryTP: use successful case to devise a concise new plan of action for the ongoing task.

OI-TP prompt: same cases, but explicitly forbid plan/subgoals/next-action ownership and request only transferable facts/patterns plus constraints/pitfalls.

## Manipulation endpoint

This is not a task-performance endpoint.

Original TP passes manipulation if its response contains at least two ordered current-task action directives using ALFWorld action verbs.

OI-TP passes manipulation if:
- it contains no ordered current-task action sequence of two or more action directives;
- it does not claim to be a plan/subgoal/to-do list;
- it provides memory-derived facts/patterns or constraints/pitfalls.

Frozen ALFWorld action verbs for this check:
go, open, close, take, put, heat, cool, clean, examine, use.

Ordered sequence markers:
first, then, next, after that, finally, step 1/2/..., numbered action lines.

If OI-TP still emits an ordered action sequence, the intervention is not operationally valid and benchmark execution is blocked.
