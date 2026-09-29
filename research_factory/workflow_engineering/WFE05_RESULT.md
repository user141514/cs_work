# WFE-05 — Consolidated local execution closeout

Date: 2026-09-29
Plan: WFE-20260929
Status: COMPLETE_LOCAL_BASELINE_FROZEN
Decision: stop speculative infrastructure expansion; use this baseline on research tasks.

## Why the plan changed

The user identified an engineering spiral. WFE-04 had turned an unsuitable historical Stage-B launcher into an unnecessary prerequisite. The root objective is a usable research workflow, not rehabilitation of that launcher or a general agent platform.

The already-tested Gate.initialize and Gate.admit provide atomic single-run ownership and unit admission. A single runner can own admission and immediate execution, avoiding transfer/redemption of detached leases. Therefore no second dispatch service, CLAIMED state machine, registry, dependency or daemon was added. Existing gate and historical launcher source were left unchanged.

This is a bounded implementation-strategy change, not termination/rebranding of the research goal. The old adapter remains historical diagnostic evidence, not the active entry.

## Delivered

- local_runner.py: the real command-line entry for trusted local Python work.
- runtime_tests/test_local_runner.py: real-process acceptance tests and a runnable --smoke example.
- Runtime contract overlay: workflow_version=0.2-local, runner.kind=local-python-v1.

Path:

frozen contract + input/script/interpreter hashes
-> exclusive Gate.initialize
-> dependency/conflict-aware Gate.admit
-> real Python child process (no shell)
-> exit/timeout, declared artifacts, process logs and receipt
-> Gate.finish -> STOPPED, next_step.authorized=false.

Independent ready units may run concurrently up to the existing limit of two. Conflicting write scopes are serialized. Dependent units only run after accepted predecessor artifacts. Failed work stops further admission; already-admitted siblings are waited for. The same state DB cannot be reused to relaunch work.

All executable settings come from the frozen task contract, not an adapter request after admission. Scientific conclusions remain UNASSESSED. KEEP/MODIFY here closes the execution contract and does not update the scientific master plan automatically.

## Native evidence

Host: PC2, Windows-10-10.0.19041-SP0, Python 3.7.0 (E:/Anaconda3/python.exe).

TDD: all 10 new acceptance cases initially failed because local_runner did not exist. After implementation, 10/10 passed. The concurrent-invocation test was strengthened to launch two separate CLI processes; one completed and the other received STATE_EXISTS.

Commands run:

    python -B -m unittest discover -s runtime_tests -v
    python -B runtime_tests/test_local_runner.py --smoke

Observed final runtime suite: 10 tests, 0 failures/errors/skips (13.045s on this run). Includes real independent-worker overlap, dependency ordering, serialization of overlapping writes, invalid authorization, command drift after freeze, unfrozen script/interpreter, out-of-scope logs, nonzero exit, missing output, timeout, duplicate invocation and the existing verifier as a real child. Several cases use multiple subcases; 10 is the test-method count, not an inflated branch count.

The persistent smoke launched local_runner.py as a real CLI, which then launched the existing offline verifier in an isolated input snapshot. It reread the output JSON and the SQLite state after CLI exit:

- verifier: 74 run / 74 passed / 0 failures / 0 errors / 0 skipped;
- phase: STOPPED;
- attempts: 1;
- next_step_authorized: false;
- repeat CLI attempt: exit 2, STATE_EXISTS;
- artifacts: result.json and test_output.txt accepted;
- no model/API/GPU/agent client was run.

Native smoke directory: C:/Users/Administrator/AppData/Local/Temp/wfe_closeout_zxdeya2e.
The explicit subsequent file-tool read of smoke_result.json was denied because Temp is outside allowed read roots; no alternate read route was used. The evidence above is the actual native command output, including the smoke's fresh SQLite/artifact reads and assertions, not a claim of successful direct file-tool retrieval.

Tested source SHA256:
- local_runner.py: 31750bb6942c4ddc798e0fee21972f553bc5417633601e52febae2acb43f8519
- offline_gate.py (unchanged): 2a92ff0ec3b461c8bb0e936a4e9703d7719a473d932bcd3b054e9f5d88174262
- runtime_tests/test_local_runner.py: f678d1c34887480fbe41cc6a4079afd21ae2c0dff007aeeffdfdcc58f742d265

## Honest limits — not a new engineering backlog

Supported surface: a trusted coordinator running explicitly reviewed, bounded local Python scripts. Commands and declared inputs are frozen; receipt correctness remains structural unless a task-specific evaluator supplies stronger evidence.

Not an OS sandbox: arbitrary direct MCP/shell calls, undeclared file/network access by malicious scripts, concurrent hostile filesystem mutation, and interpreter dependency replacement are not mechanically prevented. Reported model usage is zero for the audited local scripts used here, not an independent network meter for arbitrary code.

Timeout handling kills/waits for the direct Python child. Descendant-producing processes, daemons and model clients are outside this baseline. Coordinator interruption can leave a RUNNING record requiring inspection; there is intentionally no automatic retry or assumed exactly-once completion. At-most-once admission applies per state DB, not globally to arbitrary copied databases.

The old Stage-B adapter is still not live-ready. No paid-agent path or workflow-superiority claim was established. These limits are documented boundaries, not automatic authorization to build another platform layer.

## Closure and next decision

Freeze the engineering baseline. No WFE-06 prerequisite is scheduled.

Exactly one next step: RESEARCH-01 — select one reconstructable real complex historical task as DEVELOPMENT_ONLY, freeze the common initial inputs and method-neutral endpoint evaluation, and perform the first bounded workflow replay using existing authorized tools. Comparing workflows must keep the same task/resources; known historical outcomes must not be fed to the executing arm or represented as held-out evidence. No paid run is authorized by this note.

Only a concrete failure of that research task which changes its result may reopen a minimal engineering fix. A hypothetical future requirement is not enough.
