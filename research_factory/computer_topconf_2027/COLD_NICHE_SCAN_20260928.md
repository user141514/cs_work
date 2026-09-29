# Cold / Niche High-Potential Scan — Computer Top-Conference 2027

date: 2026-09-28
status: BOUNDED_SCAN_COMPLETE
scope: general computer science / ML / AI
budget: max 5 direction families
decision_rule: displace existing BET-COMP-01/02 only with strictly better novelty runway AND equal-or-better falsifier latency / asset availability

## Executive decision

No niche direction currently clears the displacement bar for BET-COMP-01.

One direction is retained as a high-priority WATCHLIST:
**machine-checkable intent/specification state for coding agents under evolving requirements**.

The other four scanned families are already heating quickly or directly occupied by 2026 work.

---

## N1 — Evolving Agent Harness / Regression-Safe Capability Updates

Transition:
agents increasingly accumulate tools, skills, specialist agents and editable harness state after deployment.

Fresh pressure:
- EvoHarnessBench (2026-09) reports harness-induced forgetting even when model weights do not change;
- Agent Skills Can Be Harmful / Regression Tax show that adding relevant skills can create functional and efficiency regressions;
- self-evolving harness methods now explicitly add admission/gating and regression defenses.

Open-looking interface:
predict the regression impact of a proposed harness delta before full deployment/evaluation.

Occupancy / crowding:
HIGH AND RAPIDLY HEATING.
Pre-commit skill gating, budgeted skill selection, contamination control, harness evolution and change-impact analysis already have direct 2026 work.

Decision:
WATCH ONLY, NOT A NEW BET.
Do not enter generic skill selection, skill gating, or harness evolution.

Potential future escape:
a cheap, source-grounded **harness-delta -> affected-capability/test subset** predictor that is evaluated on true behavioral regressions, if direct-prior audit leaves that exact contract open.

---

## N2 — Stateful Agent Memory Freshness / Derived-State Invalidity

Transition:
long-horizon agents now persist memory across sessions and act in changing environments.

Fresh pressure:
- STALE shows a large gap between retrieving updated evidence and actually behaving according to it;
- MAGE treats memory as execution-state management;
- PlanFence shows fresh shared facts do not imply a previously derived plan remains valid.

Occupancy:
HIGH.
State revision, plan dependency validation, hierarchical execution state and memory freshness are already active 2026 topics.

Decision:
NO BET.
The broad "stale memory / stale plan" problem is real but no longer cold.

---

## N3 — Machine-Checkable Intent / Specification State for Coding Agents

Transition:
coding agents increasingly succeed at implementation, shifting the bottleneck upstream from code synthesis to **what behavior the specification actually determines**.

Fresh pressure:
- ICLR 2026 VeriEquivBench identifies specification-quality evaluation as a bottleneck for formally verifiable code;
- 2026 Intent Formalization explicitly frames specification validation as an open research challenge;
- SpecFirst shows that making behavioral specification elicitation a first-class phase improves program synthesis;
- SpecPath shows coding agents can be sensitive to the historical path of equivalent requirement revisions;
- MAGS / program-proof planning show machine-checkable specifications can become the control surface for reliable generation.

Why this is still interesting:
the field is active but substantially less saturated than generic agent memory, KV cache, adaptive compute or skill routing.
The unresolved object is increasingly the **specification state itself**, not another prompting strategy.

Promising exact interface to attack later:
**minimal decision-complete specification**:
given an evolving task/repository, identify the smallest machine-checkable specification/dependency closure that preserves implementation decisions and verifier outcomes relative to a full authoritative specification.

Cheap falsifier shape:
- use existing executable coding-agent tasks / verified-code benchmarks;
- hold model/repository/verifier fixed;
- compare full spec vs structured dependency closure vs naive summary / retrieval;
- test whether a compact spec state preserves behavioral convergence across requirement revisions;
- no model training required for the first pressure test.

Risks:
- may fit ICSE/FSE/PLDI-style venue family better than ICML/NeurIPS unless the state/compression principle generalizes beyond software;
- recent SpecPath and semantic-block/specification-quality work narrow novelty runway.

Decision:
HIGH-PRIORITY WATCHLIST.
This is the only niche direction from the scan allowed to receive a future exact-prior attack before BET-COMP-02 is activated.

---

## N4 — Explicit Belief State for Partially Observable LLM Agents

Transition:
LLM agents are moving from static reasoning tasks into long-horizon partially observed environments.

Fresh work:
- Agent-BRACE;
- Belief-Based World Models;
- Belief-State Engine;
- event-triggered partial-observability planning in embodied systems.

Occupancy:
RAPIDLY HEATING / DIRECT METHOD OCCUPANCY.

Decision:
NO BET.
The general "give LLM agents an explicit belief state" claim is already occupied.

---

## N5 — Revocation / Unlearning of Stateful Agent Execution

Transition:
agents now carry derived state beyond plaintext memory: summaries, plans, caches and tool-side artifacts.

Fresh work:
- continual LLM/MLLM unlearning methods;
- 2026-09 Execution-State Unlearning formalizes counterfactual forgetting across prompt, memory and KV cache and gives provenance-guided selective replay.

Occupancy:
DIRECT.

Decision:
NO BET.
Do not enter generic "forgetting must invalidate derived runtime state".

---

## Portfolio consequence

Current order remains:

1. BET-COMP-01 — Feedback Stability for Iterative Generative Inference — ACTIVE.
2. N3 WATCHLIST — Minimal Decision-Complete Specification State for Coding Agents — exact-prior attack allowed only as a bounded side check.
3. BET-COMP-02 — Minimal Sufficient State for Iterative Generative Inference — QUEUED.

Reason N3 does not yet displace BET-COMP-01:
- BET-COMP-01 has an immediate 1.4B public-model, zero-training discriminator;
- N3 has strong why-now pressure but needs a careful task/spec artifact alignment before the first falsifier;
- venue family for N3 may be SE/PL rather than core ML.

## Reusable rule

Cold/high-potential regions are best found at **new lifecycle/state boundaries created by capability transitions**, not by searching for low paper counts.

A niche is attractive only when:
new capability/regime -> new correctness/state invariant -> direct prior still sparse -> existing artifact can falsify it cheaply.
