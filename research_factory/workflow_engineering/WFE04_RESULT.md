# WFE-04 Result — Gated Stage-B Dry-Run Adapter

Date: 2026-09-29
Plan: WFE-20260929
Step: WFE-04
Status: COMPLETED_DRY_RUN_ADAPTER__LIVE_BLOCKED
Decision: KEEP the workflow-engineering plan and the adapter; DO NOT authorize live launch.

## Owned question

Can one real existing execution entry be placed behind the WFE gate far enough to prove reject-before-dispatch and deterministic command preparation without launching any model/agent, while exposing the remaining live-enforcement gaps?

Selected real entry:
- `research_factory/computer_topconf_2027/run_stageb_agent.ps1 -Action Launch`
- frozen SHA256 observed on PC2: `bdce805c89020169a9bf139eb82847ca71c9492fa99ec531ba193a36e1b843df`

The historical Stage-B launcher itself was not executed.

## Composition decision

Authority ownership remains singular:
- `offline_gate.py` owns authorization/admission state;
- the historical PowerShell launcher owns its execution mechanics;
- `executor_adapter.py` is a derived dry-run projection only.

The adapter cannot create authorization, cannot launch a process, and cannot advance NEXT_STEP.

A new public gate interface, `Gate.validate_lease()`, revalidates current contract authority, RUNNING attempt state and frozen read hashes before the adapter can prepare a plan. Admitted session paths are now persisted in the authoritative attempt record rather than accepted and discarded.

## TDD evidence

### Lease validation increment

RED:
- admitted lease did not retain session paths;
- `Gate.validate_lease` did not exist.

GREEN:
- 4 focused lease tests passed;
- existing gate suite expanded from 58 to 62 and passed.

### Adapter increment

RED:
- 10 adapter tests failed because `executor_adapter` did not exist.

GREEN:
- valid lease creates a dry-run plan;
- malformed/stale/consumed lease is rejected;
- changed frozen prompt is rejected;
- prompt outside declared read scope is rejected;
- executor hash mismatch is rejected;
- unsafe arm names/timeouts are rejected;
- adapter CLI emits JSON without launching;
- network/process calls are forbidden in behavioral tests.

A later review probe added two further invariants:
- do not invent `-ExecutionPolicy Bypass` in the prepared command;
- live readiness requires actual executor arm/log paths to align with gate-declared session/write scope.

Final test count after those additions, including the verifier-metadata regression: **74**.

## Final verification

Native PC2:
- Windows 10 10.0.19041 SP0
- Python 3.7.0

Command:
`python -B verify_offline.py --output-dir C:/Users/Administrator/AppData/Local/Temp/wfe04_final_verify_v2`

Observed:
- tests_run: 74
- passed: 74
- failures: 0
- errors: 0
- skipped: 0
- success: true
- verifier globally blocked socket.connect and subprocess.Popen.

Final source SHA256:
- executor_adapter.py: `772a5b8e4f90610ccca388487f372ed13c6ea2c3359ddeee37d919c11e7a9e5f`
- offline_gate.py: `2a92ff0ec3b461c8bb0e936a4e9703d7719a473d932bcd3b054e9f5d88174262`
- tests/test_executor_adapter.py: `10b18adfb7c1689a2ad5199919a6d4c65730485483b7691ad953151c044bf551`
- verify_offline.py: `5259bb8570061882fd30ca541344e4dfcd90a677c91c740b0242a73c7b3d9c45`
- tests/test_offline_gate.py: `b82cbb989abbf30213581b9f9a54448c99559cfbd1462212ab20c1c15a6de2fb`

A source scan found no adapter launch/network primitives among:
`import subprocess`, `from subprocess`, `import socket`, `os.system(`, `Popen(`, `Start-Process`.

## Real PC2 dry-run against the actual launcher

The valid admitted lease produced:

- mode: `DRY_RUN`
- would_launch: `false`
- executor: `D:\cs_work\research_factory\computer_topconf_2027\run_stageb_agent.ps1`
- executor hash matched the frozen value;
- prompt path was resolved from a gate-declared frozen input;
- task workspace and session path came from the admitted attempt;
- expected future launcher receipt fields were exposed:
  - Backend
  - SessionId
  - ExitCode
  - TimedOut
  - StdOutLog
  - StdErrLog
  - Arm

The prepared argv was structurally:
`powershell.exe -NoProfile -File <pinned script> -Action Launch -PromptFile <declared prompt> -ArmName s1-r0 -TimeoutSeconds 240`

PowerShell was NOT invoked.

## Decisive live blocker discovered

The real launcher computes its own mutation paths:

- runtime root: `D:\stageb_agent_runtime`
- arm: `D:\stageb_agent_runtime\arms\s1-r0`
- venv: `D:\stageb_agent_runtime\venvs\s1-r0`
- log root: `D:\cs_work\external\spec_stageb_logs`

For the valid gate lease used in the dry-run:

- `arm_within_declared_session_paths = false`
- `log_root_within_declared_writes = false`

Therefore the historical launcher cannot safely be called live under the current gate contract: its actual side effects are outside the lease-owned path set.

Current external preconditions are also absent in the new repository:
- `D:\cs_work\external\spec_stageb_logs\stageb_backend_freeze.json`: missing
- `D:\cs_work\external\spec_stageb_s1_local`: missing

These are not treated as scientific failures.

## Remaining enforcement gaps

The adapter reports, rather than hides:

1. `atomic_dispatch_claim`
   - validation is read-only;
   - a later live path needs an atomic RUNNING -> DISPATCHING/CLAIMED transition before process launch to close validation/launch TOCTOU.

2. `executor_parameters_not_frozen_in_gate`
   - arm/session/timeout/executor request parameters are still adapter inputs rather than an immutable gate-owned dispatch contract.

3. `executor_path_ownership`
   - the historical launcher chooses arm/venv/log locations outside current declared task/session/write scope.

A resumed session would add a fourth gap: session identity is not yet gate-owned.

## What WFE-04 proves

Supported:
- current gate can reject invalid authority before command preparation;
- a valid current lease can deterministically prepare a real launcher command without process/model/network execution;
- executor hash, prompt/read scope, task workspace and admitted session paths can be checked before preparation;
- real launcher side effects and missing preconditions can be surfaced before launch.

Not supported:
- no live executor is enforceably wired;
- no model or agent was started;
- no Stage-B scientific arm was replayed;
- no workflow-effectiveness improvement is established;
- no OS sandbox exists;
- no claim that run_stageb_agent.ps1 is suitable as the future active executor.

## Decision

KEEP the minimal gate and dry-run adapter.

BLOCK live launch. The first unresolved boundary is now the dispatch contract itself, not command construction.

The historical Stage-B launcher remains frozen evidence. Do not patch it opportunistically just to make this dry-run look live-ready.

## Exactly one NEXT_STEP — not executed

ID: WFE-05
Status: PLANNED_NOT_AUTHORIZED
Action: add a model-free gate-owned dispatch contract and atomic claim transition. Freeze executor identity/hash, prompt, executor parameters and all projected mutation paths before a lease can become DISPATCHING/CLAIMED. A claim must be single-use and must fail if contract/read/path authority drifts.
Acceptance: deterministic tests prove only one concurrent claim wins, frozen executor parameters cannot change after claim/admission, every claimed mutation path is within declared session/write authority, and no process/model/network call occurs.
Boundary: do not modify or launch the historical Stage-B PowerShell runner in WFE-05. If its internally chosen paths cannot satisfy the new contract, leave it blocked and use that evidence to decide whether a new active executor seam is required later.
Forbidden: model/API/GPU/agent launch, historical replay, Watchdog changes, automatic WFE-06.
