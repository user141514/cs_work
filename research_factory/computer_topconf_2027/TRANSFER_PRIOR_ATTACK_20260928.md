# Ancestry-Derived Transfer Prior Attack — 2026-09-28

date: 2026-09-28
status: BOUNDED_DIRECT_PRIOR_ATTACK_COMPLETE
scope:
- Feedback Utility State for iterative/recurrent AI inference
- Behavioral Self-Adjustment for coding agents under requirement evolution

## 0. Decision

Both cross-domain transfers remain scientifically open under the bounded search, but they are not equally strong.

Rank by current research value:
1. **Behavioral Self-Adjustment / From-Scratch Consistent Coding Agents** — stronger nonlocal transfer, clearer new-regime mismatch, stronger cold/high-potential profile.
2. **Feedback Utility State** — still plausible, but target neighborhood is more crowded and the contribution risks collapsing into another adaptive-compute/stability controller.

This ranking changes the previous portfolio ordering.
No method experiment is authorized yet; the next action is a cheap asset/falsifier preflight for Rank 1.

---

# 1. Transfer A — Feedback Utility State

## Exact target contract

Consumer:
finite-depth looped/recurrent or iterative generative inference.

State:
two-part decision state:
- finite-horizon propagation risk of carried feedback error;
- extrinsic progress contributed by the current recurrence beyond the prior state.

Intervention:
choose ordinary feedback / damped feedback / isolated-no-feedback / stop.

Evidence:
predict and improve task-level benefit/harm from recurrence beyond entropy/confidence/depth at matched compute.

## Current direct/adjacent priors

Direct pressure / neighboring methods:
- FastDiSS: inaccurate self-conditioning compounds errors; training-time perturbation improves robustness.
- Loopholing Discrete Diffusion: deterministic latent feedback path preserves continuous information across denoising.
- MetaState: persistent recurrent working memory around frozen dLLM backbone.
- Ouro: looped latent computation with configurable recurrence and adaptive exit.

Mature ancestors:
- small-gain / robust-feedback reasoning;
- fixed-point / DEQ Jacobian stabilization and relaxation;
- EXIT / iterative decoding information-transfer analysis;
- residual BP informed scheduling.

## Direct-veto result

No bounded-search source was found that already owns the full target contract:
finite-horizon feedback propagation risk
+
extrinsic progress
->
feedback-topology control
with task-level evidence.

Therefore:
DIRECT_VETO = false.

## Novelty width

NARROW_TO_MEDIUM.

Risk:
the two-dimensional state may reduce empirically to confidence/entropy plus depth.
The target field already contains many adaptive-compute and recurrent-state methods.

## Falsifier latency

Excellent:
Ouro-1.4B is public and exposes configurable recurrent steps and adaptive exit.
No training is required to test whether the ancestry-derived state exists.

## Verdict

TRANSFER_OPEN_BUT_CROWDED.

Retain as queued Rank 2.
Do not run before Rank 1 preflight unless Rank 1 is asset-blocked or directly occupied.

---

# 2. Transfer B — Behavioral Self-Adjustment for Coding Agents

## Exact target contract

Consumer:
coding agents executing software changes under evolving requirements.

State:
runtime derivation lineage spanning:
requirement/spec atom
-> design/implementation decision
-> verification obligation/test
-> code/action artifact.

Intervention:
on requirement revision, selectively invalidate and rederive only the affected closure while preserving independent derived work.

Correctness evidence:
**Behavioral From-Scratch Consistency (BFSC)**:
the revision-history execution should reach verifier-observable behavior equivalent to a clean run from the consolidated final authoritative specification.

Efficiency evidence:
material reduction in rederived nodes / agent calls / tokens / tool calls / wall time relative to full reset.

## Current target pressure

### SpecPath
Establishes specification-path sensitivity:
equivalent final contracts can produce behaviorally different coding-agent implementations.
It does not provide selective rederivation.

### Requirements After the First Edit
Establishes that late requirements are followed by substantially more invalidation/rework in real coding-agent sessions.
It diagnoses pressure rather than supplying a from-scratch-consistent incremental execution method.

### VeriEquivBench / Intent Formalization
Establish specification quality and intent formalization as current bottlenecks.

## Current neighboring interventions

### PlanFence
Dependency-scoped validation of pending actions/plans against exact public records.
Directly occupies generic:
"fresh facts do not guarantee fresh plans; validate only dependencies of the pending action."

Boundary:
PlanFence is action-validation/replanning over distributed-agent records, not a coding-agent derivation graph spanning requirements -> decisions -> tests -> code with BFSC against a clean final-spec execution.

### SpecD
Current engineering system already combines spec graphs, code graphs, impact analysis and deterministic spec-delta handling.

Boundary:
this kills weak claims such as:
- first spec graph for coding agents;
- first change impact analysis for coding agents;
- first deterministic delta application.

It does not, by itself, establish BFSC for stochastic coding-agent derived state.

### Agent provenance/evidence graph tools
Current tools increasingly capture causal/execution provenance.
This makes provenance collection itself non-novel.

## Mature source structures

### Program slicing
Given a dependence graph and criterion/change, compute the transitive impacted slice.

### Self-adjusting computation
Record dynamic dependencies during execution; after input mutation reexecute affected computation; preserve the invariant of from-scratch consistency.

### Incremental view maintenance
Propagate base-state deltas through derivation/query structure so the materialized view equals full recomputation.

### Incremental build systems
Invalidate and rebuild affected artifacts while preserving independent artifacts.

## New-regime mismatch

These mature systems assume dependencies are explicit or mechanically observable.

Coding-agent dependencies are:
- semantic;
- probabilistic/stochastic;
- cross-artifact;
- sometimes latent/unrecorded;
- mutable because rederivation can discover new dependencies.

Therefore the real unknown is not impact-graph traversal.
It is:

**Can a sufficiently sound behavioral derivation graph be constructed cheaply enough that dependency-scoped rederivation approaches clean-from-scratch behavioral correctness without degenerating to full replay?**

This is the load-bearing scientific question.

## Direct-veto result

Bounded current search found:
- diagnostics of requirement-path sensitivity;
- measurement of late-requirement invalidation;
- plan dependency validation;
- spec/code impact-analysis tools;
- provenance DAG tooling.

No single inspected work matched all four:
A. coding-agent evolving-requirement consumer;
B. cross-layer runtime semantic derivation state;
C. selective invalidation/rederivation;
D. BFSC + recomputation-cost evidence.

Therefore:
DIRECT_VETO = false.

This is not a firstness claim; direct-prior search remains provisional until exact benchmark/implementation preflight.

## Novelty width

MEDIUM and substantially more nonlocal than Feedback Stability.

Why:
the core method identity comes from transferring self-adjusting computation's correctness contract into a regime where dependencies themselves must be inferred.

## Falsifier latency

Potentially low if a small equivalent-history task set can be reconstructed.

Public assets:
- SpecPath defines the exact paired-contract evaluation design, but a public code repository was not surfaced by the bounded search.
- SWE-chat provides real coding-agent traces/dataset infrastructure, but the GitHub README currently says data/code are still being released.
- ProgramBench is public and executable, but it is not itself an evolving-requirement benchmark.

Therefore G0 is not yet PASS.
The first action is an **asset/preflight**, not a method implementation.

## Cheapest pressure/falsifier preflight

Construct or recover a very small controlled set (not a new benchmark paper) of 5-10 coding tasks with:
- initial requirement;
- one semantically meaningful revision;
- consolidated final equivalent requirement;
- executable behavioral verifier.

Run a single existing coding agent in:
A. direct consolidated final spec;
B. revision history preserving all state;
C. full reset at revision;
D. dependency-scoped rederive using externally recorded provenance edges.

No model training.

First question:
does there exist a nontrivial regime where D approaches C's verifier behavior while preserving substantially more prior work?

Negative:
if D needs near-total invalidation to match C, the transfer's economic premise fails.

Positive:
if D recovers path invariance with partial rederivation, then semantic dependency discovery becomes the next method question.

## Venue fit

This transfer is intrinsically computer-science rather than "ML paper by default".

If formal BFSC semantics / derivation correctness are load-bearing:
PLDI 2027 is plausible; official research-paper deadline 2026-11-12.

If contribution remains primarily empirical agent orchestration:
software-engineering venues are more natural; do not force PLDI or ICML.

## Verdict

TRANSFER_OPEN_PENDING_G0.

Promote to current Rank 1 research object for preflight.
Not yet a TOPIC_BET/PAPER_CANDIDATE.
