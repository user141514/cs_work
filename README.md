# cs_work

Dedicated Git repository for the user's general computer-science / machine-learning / AI / software-systems top-conference research.

## Active layout

```text
research_factory/
├── PROJECT_AUTHORITY.md
├── DECISION_CONTRACT_GATE_V1.md
├── EXECUTION_LEVERAGE_GATE_V1.md
├── workflow_engineering/
│   ├── MASTER_PLAN.md
│   ├── WORKFLOW_SPEC_V0_1.md
│   ├── offline_gate.py
│   ├── local_runner.py
│   └── ...
└── computer_topconf_2027/
    ├── LIVE_STATE.md
    ├── ASSET_LEDGER_20260928.md
    └── ...
```

Recovery starts from `AGENTS.md` and `research_factory/PROJECT_AUTHORITY.md`.

## Repository separation

WFE-03.1 moved the active CS research substrate out of the mixed `D:/bio_paper` workspace. The old copies remain provenance only; new CS plans, code and evidence belong here.

Historical files are intentionally retained even when a line of research is paused or negative. Migration does not relabel their scientific status. Some frozen Stage-B verifier scripts still reference historical `D:/bio_paper/external` benchmark/venv assets; they are provenance, not current execution entrypoints, until explicitly rebound and reverified.

## Current workflow status

- WFE-01: completed specification.
- WFE-02: offline gate implemented and independently verified.
- WFE-03: native PC2 verification passed.
- WFE-03.1: repository separation/migration.
- WFE-04: historical Stage-B dry-run probe completed; historical live launcher remains blocked.
- WFE-05: consolidated real local execution completed. Engineering baseline frozen; 10 native real-process acceptance cases passed, plus the existing 74-test verifier executed as a real child.
- RESEARCH-01: completed DEVELOPMENT_ONLY S3 replay. Final implementation passes the frozen public+lifecycle endpoint, but the workflow transition is boundary-contaminated by an extra post-Phase-A provider turn that changed the focused test before the late revision; do not use it as comparative evidence.
- RESEARCH-02: superseded by user redirection; preserved but inactive.
- OI-AS-00: AgentSquare ALFWorld static O+I scan completed; 42/210 hard-inadmissible, 182/210 soft-coupled.
- OI-AS-01: module-label directional screen completed; MemoryTP is uniquely lowest among four non-None memory modules, but evidence is tiny-n/non-causal.
- OI-AS-02: planned controlled original-TP vs orthogonalized-TP experiment; not authorized merely by being listed.

Runnable model-free end-to-end example (from `research_factory/workflow_engineering`):

```sh
python -B runtime_tests/test_local_runner.py --smoke
```

This baseline runs trusted bounded local Python work, not arbitrary untrusted agents. No paid-agent or OS-sandbox readiness claim. See the workflow README for usage and `research_factory/workflow_engineering/MASTER_PLAN.md` for exact execution authority.
