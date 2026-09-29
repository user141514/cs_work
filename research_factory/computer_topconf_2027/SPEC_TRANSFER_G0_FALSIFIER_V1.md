# SPEC Transfer G0 + PRECARD Falsifier Contract V1

date: 2026-09-28
status: FROZEN_PRECARD_CONTRACT__RUNTIME_BLOCKED_OFFICIAL_HARNESS
parent:
- SPEC_ANCESTRY_TRANSFER_V1.md
- TRANSFER_PRIOR_ATTACK_20260928.md
research_object: Behavioral Self-Adjustment / Behavioral From-Scratch Consistency for Coding Agents
lifecycle_stage: PRE_TOPIC_TRANSFER_PROBE
formal_paper_candidate: false

## 1. Progress audit

Completed:
- target residual abstracted as incremental recomputation under changing authoritative requirements;
- mature ancestors identified: program slicing, self-adjusting computation, incremental view maintenance, build/change-impact systems;
- transferred invariant identified: reused derived state is valid only when independent of changed authoritative state;
- target mismatch identified: coding-agent dependencies are semantic, stochastic, cross-artifact, and partly latent;
- bounded direct-prior attack found no single current work matching coding-agent evolving requirements + runtime derivation lineage + selective invalidation/rederivation + behavioral from-scratch consistency;
- public executable substrate identified: SWE-Together.

Current true blocker:
official SWE-Together execution on PC2 is not currently available because:
- Docker/container runtime not installed;
- no E2B key;
- no Gemini/OpenRouter/Anthropic/GHCR credentials in current environment.
Codex CLI is available, but that alone does not satisfy the official SWE-Together harness contract.

This is an execution-environment blocker, not scientific evidence.

## 2. G0 exact-asset audit

### Scientific asset identity

Primary:
Togetherbench/SWE-Together.

Verified public contract:
- 109 repository-level interactive coding tasks;
- original first instruction;
- ordered user intents;
- replayable reactive user-simulator prompts;
- pinned base commit;
- container image identity;
- executable verification/scoring artifacts;
- reference patch / completeness goals where applicable;
- support for Codex/Claude/OpenCode-style agents.

Dataset identity:
yifannnwu/SWE-Together, test split, 109 rows.

Representative smoke task:
dataclaw-anonymizer-tests
- repo: peteromallet/dataclaw
- base_commit: 3c0991467af69675afa948c3ada45475a772fbeb
- num_user_intents: 5
- category: feature
- later user requests include review, tests, and regex/performance refinement;
- deterministic F2P/P2P verification gates are published;
- upstream PyPI 0.3.2 provenance is pinned to the same publishing commit.

G0_SCIENTIFIC_ASSET = PASS.

### Runtime identity

PC2 preflight:
- git: available;
- uv: available;
- Codex CLI: available;
- node: available;
- D: free space ~69.2 GB;
- Docker: unavailable;
- Podman/nerdctl/containerd: unavailable;
- WSL executable: unavailable in current shell;
- E2B/Gemini/OpenRouter/Anthropic/GHCR/OpenAI API environment keys: absent.

G0_OFFICIAL_HARNESS_RUNTIME = BLOCKED.

No experiment result may be inferred from this blocker.

## 3. Claim under test

Necessary economic/structural claim:

> Under evolving requirements, there exists a nontrivial regime in which dependency-scoped selective rederivation can recover verifier-observable behavior close to a clean run from the consolidated final specification while reusing materially more prior work than a full restart.

This is only a prerequisite for a future method paper.

POSITIVE_SUPPORTS:
- the self-adjusting-computation transfer has usable headroom;
- semantic dependency discovery is worth studying as the next method problem.

NEGATIVE_FALSIFIES:
- the economic premise of selective rederivation under the tested regime if even an oracle dependency slice cannot preserve behavior with nontrivial reuse.

NEGATIVE_DOES_NOT_FALSIFY:
- all specification tracking;
- ProjectGuard-style global state;
- all coding-agent memory/provenance methods;
- self-adjusting computation in other consumers.

## 4. Strongest cheap rivals / controls

R0 — RAW_HISTORY:
continue the evolving interaction with all prior derived state retained.

R1 — CONSOLIDATED_REFRESH:
provide the current consolidated authoritative requirements/project state while preserving the existing implementation/session state.
This represents ProjectGuard/SpecD-like explicit-current-state mitigation at the contract level without claiming to reproduce either system exactly.

R2 — FULL_RESTART:
restart from the task's base repository and consolidated final specification.
This is the expensive behavioral reference for from-scratch consistency.

R3 — ORACLE_DEPENDENCY_SCOPED_REDERIVATION:
use an outcome-blind dependency scope frozen **before any agent outcome is observed**, constructed only from:
- ordered user requirements/intents available up to the revision boundary;
- the base repository's pre-run static structure/dependencies;
- a manually frozen human dependency annotation when the semantic dependency is not mechanically recoverable.

The reference patch, gold implementation, post-run successful diff, verifier outcome, or any artifact derived from them is **for evaluation only** and is forbidden when constructing the R3 impact slice.

R3 is deliberately an oracle upper bound over semantic dependency knowledge, not an outcome oracle.
If R3 has no useful cost/correctness region, do not build a learned dependency estimator.

## 5. Declared endpoints

Primary correctness endpoint:
- task verifier / frozen completeness behavior relative to the clean final-spec control.

Primary reuse/cost endpoint:
- fraction of pre-revision derived work preserved versus FULL_RESTART.

Operational work accounting, in preferred order:
1. agent/tool steps after the revision;
2. token/model-call counts if exposed;
3. changed/rederived artifacts;
4. wall time as secondary.

Do not substitute final diff size alone for recomputation cost.

## 6. Headroom / identifiability

HEADROOM_PRECHECK:
Before scientific adjudication, require a frozen task subset with:
- at least 5 tasks;
- each has >=3 user intents;
- at least one post-implementation requirement addition/correction that changes the active contract rather than merely asks for explanation;
- executable verifier;
- reconstructable consolidated final specification.

If fewer than 5 eligible tasks can be recovered from the public suite:
VERDICT = PRECARD_NONIDENTIFIABLE__INSUFFICIENT_EVOLVING_REQUIREMENT_SUBSTRATE.

This is not a scientific negative.

## 7. Staged execution

Stage A — substrate eligibility only:
- enumerate tasks by outcome-blind rules above;
- freeze task IDs and final-spec compilation rule;
- verify each task's base commit/verifier identity is reconstructable from published metadata;
- freeze the R3 dependency-annotation rule before any model run;
- never use reference patches/gold diffs to compile the final spec or impact slice.

Stage B — oracle upper-bound smoke:
- run R0/R1/R2/R3 on 5 frozen tasks;
- one fixed coding-agent configuration;
- no learned dependency model;
- no hyperparameter tuning.

Stage C — only if Stage B supports headroom:
- expand to 10-20 frozen tasks or a second agent configuration;
- then decide whether to activate a formal TOPIC_BET around semantic derivation-state estimation.

No later stage may rescue a failed prerequisite.

## 8. Pass / fail predicates

Because this is a necessary-condition PRECARD rather than a final method comparison, thresholds are conservative and interpretable.

PASS_HEADROOM requires on the frozen Stage-B set:
1. R3 achieves at least 80% of FULL_RESTART's verifier-success count, with no task counted positive when R3 violates an explicit late requirement that FULL_RESTART satisfies; AND
2. R3 preserves at least 30% of pre-revision derived work on median task relative to FULL_RESTART; AND
3. R3 is not strictly worse than CONSOLIDATED_REFRESH on both correctness and recomputation cost.

These are pilot thresholds, not publication claims.

REPAIR_NEGATIVE:
R3 fails because the oracle dependency mapping/adapter is demonstrably invalid or does not execute the intended selective invalidation.

CLAIM_NEGATIVE:
R3 is validly executed but either:
- requires near-total invalidation (<30% median reuse) to approach FULL_RESTART; or
- loses >20% of FULL_RESTART verifier successes on the frozen set.

CANDIDATE_KILL:
allowed only for the ancestry-derived selective-rederivation transfer after a valid oracle-upper-bound CLAIM_NEGATIVE.
Do not kill the broader specification-state research area.

## 9. Counterexample audit

PASS_WITHOUT_VALUE:
Resolved by requiring both behavioral closeness to FULL_RESTART and material reuse; correctness alone is insufficient.

FAIL_WITHOUT_IDENTIFICATION:
Resolved by Stage-A eligibility/headroom gate; insufficient suitable tasks => NONIDENTIFIABLE, not KILL.

WIN_WITHOUT_ATTRIBUTION:
Resolved at this stage by using oracle dependency scope. A positive does not attribute value to any learned dependency mechanism; it only establishes that dependency-scoped reuse has headroom.

## 10. Strongest current occupancy pressure

ProjectGuard:
kills weak claims that external semantic/structural project state or restart-style mitigation is novel.

SpecD:
kills weak claims that spec graphs, code graphs, impact analysis, deterministic spec deltas, or compiled spec context are novel.

SpecPath:
establishes specification-path sensitivity but does not itself supply selective rederivation.

Requirements After the First Edit:
establishes real late-requirement invalidation pressure but does not test dependency-scoped reuse.

Therefore any future contribution must live in:
semantic derivation state
+
selective invalidation/rederivation
+
behavioral from-scratch consistency
+
recomputation economy.

## 11. Immediate next action

Stage A is complete under `SPEC_STAGE_A_TASK_FREEZE_V1.md` with verdict `PASS_WITH_LIMITED_REPO_DIVERSITY`.

The next decision-changing action is Stage B only:
- obtain one authoritative SWE-Together sandbox/runtime path;
- run the frozen R0/R1/R2/R3 arms on S1-S5 under one fixed coding-agent configuration;
- do not train a dependency model or add tasks before the oracle-upper-bound decision.

Current PC2 blocker:
- no Docker/container runtime is available;
- no equivalent verified SWE-Together sandbox path is configured;
- official-harness provider credentials are absent.

Do not reinterpret the runtime blocker as scientific evidence.
