# WFE-03.1 Result — CS Repository Separation

Date: 2026-09-29
Plan: WFE-20260929
Step: WFE-03.1
Status: COMPLETED_REPOSITORY_MIGRATION
Decision: KEEP the workflow-engineering plan and move its active ownership to D:/cs_work.

## Purpose

Separate general-CS/top-conference research from the mixed D:/bio_paper workspace without rewriting historical evidence or creating two live sources of truth.

## Migration source and target

Source:
- D:/bio_paper/research_factory/workflow_engineering/
- D:/bio_paper/research_factory/computer_topconf_2027/

Target:
- D:/cs_work/research_factory/workflow_engineering/
- D:/cs_work/research_factory/computer_topconf_2027/

Target Git remote:
- user141514/cs_work

Working branch:
- chore/wfe-03-1-migrate-cs-work

## Byte-parity evidence before authority edits

Exact source/destination SHA256 lists were generated independently for each copied subtree, excluding __pycache__, and diffed.

Observed:
- workflow_engineering: 13/13 files parity PASS
- computer_topconf_2027: 55/55 files parity PASS

Three directly referenced upstream files were then copied with cmp parity PASS:
- research_factory/DECISION_CONTRACT_GATE_V1.md
- research_factory/EXECUTION_LEVERAGE_GATE_V1.md
- RESEARCH_MASTER_PLAN_DYNAMIC_V1.md

The legacy dynamic master plan is retained only to satisfy historical relative provenance; it is not active authority.

## Post-migration execution check

The WFE offline gate suite was run from the new `D:/cs_work` path on native PC2 Windows 10 / Python 3.7.0.

Observed:
- tests_run: 58
- passed: 58
- failures: 0
- errors: 0
- skipped: 0

The tested core source hashes remain identical to WFE-03. This establishes that repository relocation did not break the active offline gate path.

## Hygiene

- __pycache__ directories were excluded.
- repository .gitignore excludes Python caches, local verification outputs, SQLite runtime state and common tool caches.
- an obvious secret-pattern scan over migrated files returned SECRET_HITS=0.
- Git commit identity was absent initially; repo-local identity was recovered from the user's existing PC2 Git repositories rather than invented or changed globally.

Raw migrated assets were committed as:
- 01a9eba chore: migrate computer research assets

## Authority transfer

New active recovery entry:
- D:/cs_work/AGENTS.md
- D:/cs_work/research_factory/PROJECT_AUTHORITY.md

Rule after this step:
- D:/cs_work is the sole active write authority for CS/top-conference and workflow-engineering state.
- corresponding D:/bio_paper copies are historical/read-only provenance.
- future agents must not advance WFE/BFSC state in both locations.

## Known retained external dependency

A post-migration scan found historical Stage-B verifier scripts with hard-coded `D:/bio_paper/external/...` benchmark/venv paths. `run_s5_local_verifier.sh` also names its historical probe/postprocess by the old absolute research path.

These scripts belong to the paused BFSC replay substrate and are not the current WFE execution entry. WFE-03.1 therefore preserves them as historical evidence rather than silently rewriting a frozen experiment harness. Before any one of them can become a live executor in WFE-04 or later, its external assets and internal paths must be explicitly rebound and reverified under the new repository contract.

## Scientific boundary

This step performed no:
- model/API/GPU call;
- research-agent launch;
- historical paired replay;
- scientific topic promotion/kill;
- claim that the new workflow is better.

BFSC/selector scientific state remains PAUSED_UNRESOLVED.

The old `D:/bio_paper` AGENTS/project authority/WFE master/LIVE_STATE were updated with relocation pointers so a future recovery does not create a second active writer.

## Exactly one NEXT_STEP — not executed

ID: WFE-04
Status: PLANNED_NOT_AUTHORIZED
Action: identify one real execution entry and build the smallest gate-to-executor adapter in model-free dry-run mode.
Acceptance and forbidden actions remain defined in workflow_engineering/MASTER_PLAN.md.
