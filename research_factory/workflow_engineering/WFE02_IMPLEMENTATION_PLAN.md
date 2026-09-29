# WFE-02 Offline Admission and Receipt Gate Implementation Plan

> For agentic workers: execute inline with test-driven-development and executing-plans. The user explicitly authorized implementation; do not start additional model workers.

**Goal:** enforce the frozen workflow v0.1 current-step contracts through a minimal offline gate, demonstrating rejected counterexamples and permitted legal work without model calls.

**Architecture:** one Python-standard-library gate, one SQLite state store per frozen run, immutable contract identity and input/evaluator hashes, explicit admission/submission/finish operations. No executor, shell launcher, automatic scheduler or model client. A test-only fake worker creates fixture artifacts; production only validates requests and records state.

**Tech Stack:** Python standard library (pathlib, hashlib, json, sqlite3, unittest); source compatible with Python 3.7+. Independently available offline interpreter is Python 3.13.5. PC2 default Python was observed as 3.7.0, but subsequent remote shell calls were platform-blocked; remote execution remains unverified unless later explicitly succeeds.

**Spec:** WORKFLOW_SPEC_V0_1.md, especially sections 4–6 and 10.

## Global constraints
- Only WFE-02 is authorized. No model/API/GPU/agent launch, Watchdog changes, historical replay or live executor integration.
- No installation, credentials access, legacy run/setup scripts or destructive session migration.
- Tests use temporary directories and an isolated SQLite database; no historical results are edited.
- D:/bio_paper is not a Git repository. No commit/rebase/push claim; preserve authority edits through exact replacements and readback.
- The gate is not an OS sandbox or an authentication boundary. Bypassing its future controlled executor is still possible.
- Structural evidence validity, execution outcome, reported scientific claim and plan decision remain separate. Hash validity does not prove scientific correctness.

## Files and interfaces
- `offline_gate.py`: `Gate.initialize(contract_path, state_dir)`, `Gate(state_dir).admit(request)`, `.submit(receipt)`, `.finish(request)`, `.status()`; `GateError.code` stable rejection codes; CLI JSON input/output. `scoped_path` handles native resolved paths and portable Windows path checks.
- `tests/test_offline_gate.py`: deterministic fake-worker fixtures, identity/dependency/isolation/evidence/budget/transition tests, concurrent admission tests and no-network/no-process sentinels.
- `fixtures/historical_wrong_workspace.json`: development-only minimal counterexample derived from the documented session-path contamination failure; not a copied original session or a counterfactual success claim.
- `README.md`: commands, contract/request shapes, enforcement boundaries and integration preconditions.
- `WFE02_RESULT.md`: actual test commands/outcomes, limitations, decision and exactly one next step.

## Review focus
1. Path aliases, directory ancestors, symlinks and Windows drive/case handling: reject scope escapes and conflicting resources, allow truly independent read-only work.
2. Concurrent admissions and persistence: SQLite transactions serialize checks with reservations; reopen must not reset admission/completion state.
3. Contract mutation and stale receipts: re-read authoritative contract and frozen inputs/evaluator before each state-changing operation.
4. Missing/tampered artifacts and failed execution: consume the admitted attempt, classify INVALID, never promote it to a scientific negative.
5. Completion and budget: count failed attempts, disallow duplicate dispatch/submission and automatic next-step authorization; valid no-model work must pass.

## Task 1: Freeze executable interfaces and counterexamples
- [x] Write real-behavior unittest fixtures and assertions before production code.
- [x] Run the bootstrap RED (gate absent) and subsequent regression RED cases; fixture versus implementation failures distinguished in WFE02_RESULT.md.
- [x] Record the historical failure fixture as DEVELOPMENT_RETROSPECTIVE only.

## Task 2: Implement minimal enforcement
- [x] Implement identity/contract/DAG/path checks, admission reservations and durable state using SQLite transactions.
- [x] Implement receipt validation against actual files and frozen hashes, preserving invalid attempt accounting.
- [x] Implement finish -> STOPPED with exactly one unauthorised next-step recommendation (none on TERMINATE); no dispatch side effect.
- [x] Run the complete new gate suite; fix defects with regression tests before adding code.

## Task 3: Verify and close this step
- [x] Exercise positive/negative fake-driver scenarios, persistence and concurrent admission, with no model/network/process launch.
- [x] Inline review and final full-suite verification: 58/58 PASS, 0 skips; Python 3.7 grammar PASS on Python 3.13.5, not PC2 runtime verification. Additional repeated threaded conflict checks: 100/100 PASS.
- [x] Save tested implementation/tests/fixture/verifier/docs/report to PC2 using permitted file tools; re-read core implementation and regression-test sections. Remote runtime execution and remote hash computation remain unverified.
- [x] Update master plan and project entry: offline gate implemented versus live integration not implemented.
- [x] Record actual outcomes in WFE02_RESULT.md. Sole NEXT_STEP=WFE-03 native PC2 offline verification; PLANNED_NOT_AUTHORIZED. STOP.

## Progress / rulings
- Spec and master plan read from live PC2 ws_597f47059c. No pre-existing gate code is present in workflow_engineering; only the master plan and spec existed.
- Ruling: use an independent offline test environment because two simple remote shell requests were platform-blocked. File tools remain available. This is not a workaround to execute on the blocked host; PC2 runtime validation will remain explicitly pending.
- Ruling: reuse the existing workflow contract and historical failure semantics, not unsafe task-specific launch/migration helpers. None of those helpers is needed for a model-free validator.
