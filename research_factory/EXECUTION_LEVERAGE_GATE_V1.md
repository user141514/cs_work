# Execution Leverage Gate V1

date: 2026-09-28
status: AUTHORITATIVE_PROJECT_GATE
scope: TOPIC_BET -> PRECARD_LEVERAGE -> PAPER_CANDIDATE experiment admission
owner: research_factory

## 0. Purpose

Optimize decision-changing scientific information per unit execution cost.

Scientific pressure, novelty and claim validity decide whether a topic is worth considering.
Execution leverage decides the cheapest evidence level that is allowed to adjudicate the next transition.

Never infer:

cheap experiment -> scientifically good topic

or

expensive field -> scientifically bad field.

The gate only controls escalation cost after a scientifically meaningful decision has been identified.

## 1. Core invariant

If the same next research decision can be resolved at a lower execution level, a higher level is not authorized.

Formally:

EL = expected decision-changing information / (API cost + GPU cost + engineering time + data dependency cost)

Use EL as an ordering principle, not as an unconstrained scalar score.

The hard rule is:

LOWER_LEVEL_SUFFICIENT -> HIGHER_LEVEL_FORBIDDEN

Escalation is allowed only when the lower level is non-identifying for the exact frozen claim and the claim remains scientifically alive.

## 2. Execution levels

### Level 0 — Existing-result computation
Examples:
- already-produced outputs, checkpoints, metrics, metadata or logs;
- direct joins, counters, geometry, attribution, parameter analysis;
- no new model inference.

Default cost target:
- API: 0
- GPU: 0 or negligible
- engineering: minutes to <=1 h

### Level 1 — Public/local artifact offline replay
Examples:
- released traces / checkpoints / selected-example artifacts;
- replay of selectors, rerankers, stopping rules, budget policies;
- checkpoint/LoRA/gradient/embedding geometry;
- no fresh expensive generation.

Default cost target:
- API: 0
- GPU: none or light
- engineering: <=2 h where assets already exist

### Level 2 — Small-model inference-only
Examples:
- 1B-3B inference;
- small calibration/evaluation runs;
- bounded molecular generation or replay on an already-working stack.

Default cost target:
- API: 0
- GPU: tens of minutes to a few hours

### Level 3 — Small LoRA / bounded fine-tuning
Use only after Levels 0-2 cannot decide the next transition.

### Level 4 — Full training / API rollout / multi-agent / RL
Requires explicit evidence that lower levels cannot identify the claim and that the candidate has enough upside to justify high-variance/high-cost execution.

### Level 5 — Large-model training / video / robotics / large diffusion generation
Exceptional for topic-selection precards.
Normally allowed only after PAPER_CANDIDATE activation or when the scientific object is impossible to instantiate below this level.

## 3. Required fields before every PRECARD

Freeze:

EXECUTION_LEVEL:
LOWER_LEVELS_CHECKED:
WHY_LOWER_LEVELS_INSUFFICIENT:
EXISTING_ASSETS_REUSED:
NEW_API_CALLS_ESTIMATE:
NEW_GPU_TIME_ESTIMATE:
ENGINEERING_TIME_ESTIMATE:
NEW_DATA_DEPENDENCIES:
OWNED_DECISION:
KILL_OR_PROMOTION_POWER:
ESCALATION_TRIGGER:
EARLY_STOP_RULE:

A PRECARD without these fields is not executable.

## 4. Admission logic

### G-EL0 — Reuse-first
Before acquiring or generating anything, search the current project assets for:
- matched outputs;
- traces;
- checkpoints;
- logs;
- metadata;
- existing analysis code;
- public released artifacts already downloaded.

If an exact-enough asset exists, use it first.

### G-EL1 — Decision equivalence
A cheaper experiment substitutes for a costly one only if it owns the same next decision.

Do not use a cheap proxy to overclaim candidate falsification.
Decision Contract kill-scope rules remain authoritative.

### G-EL2 — Escalation proof
To move from level k to k+1, record:
1. what lower-level result was obtained;
2. why that result is non-identifying for the frozen claim;
3. which missing variable the higher level uniquely observes;
4. the smallest higher-level action that observes it.

### G-EL3 — Cost accounting
Count:
- model/API calls;
- GPU wall time;
- repeated runs required by variance;
- data download/access friction;
- benchmark/evaluator engineering;
- custom kernels/systems work;
- human orchestration and debugging time.

A low raw GPU count does not make an experiment cheap if data or systems work dominates.

## 5. Domain bias for topic search

Prefer research spaces where a decisive PRECARD is commonly available at Levels 0-2.

### First-priority search regions
- data selection / data valuation / curriculum;
- model merging / LoRA / adapter geometry;
- offline reasoning-trace replay;
- ranking / attribution / selector analysis.

### Second-priority regions, constrained to cheap forms
- quantization sensitivity / bit-allocation replay / small-model inference;
- KV / memory / long-context replay;
- small-model inference-only algorithmic probes.

### Deprioritized for high-frequency topic search unless reusable artifacts exist
- API-heavy agents / multi-agent rollouts;
- RL with repeated online trajectories;
- world-model / video generation;
- embodied/robotics experiments;
- large diffusion or foundation-model retraining.

This is a search prior, not a ban.

## 6. Lifecycle interaction

### TOPIC_BET
Prefer bets whose first discriminator is Level 0-2.
A Level 4-5 first discriminator is a strong negative admission signal.

### PRECARD_LEVERAGE
Must execute at the minimum sufficient level.
A negative result inherits only the Decision Contract's frozen kill scope.

### PAPER_CANDIDATE
May authorize Level 3 after positive local leverage.
Level 4-5 requires explicit candidate-level justification.

### METHOD_PILOT / FULL_CONFIRMATION
Higher levels are allowed when they are necessary to test the actual method claim, but cost still enters comparator/value accounting.

## 7. Current application: R11-001

Existing assets:
- 10-NFE and 20-NFE MolDiff/DDIM outputs share persisted initial states for 64 root samples;
- raw validity differs strongly at the sample level;
- a provisional terminal-edge entropy signal already shows nontrivial rescue ranking.

Therefore the next authorized evidence level is Level 0/1 offline replay.

Fresh paired generation is not authorized by default.
It becomes eligible only if offline replay is non-identifying because the existing outputs do not expose the required pre-outcome state, endpoint pairing, or evaluation variable.

## 8. Success metric for the factory

Track:
- hypotheses killed or promoted per GPU-hour;
- hypotheses killed or promoted per API call;
- median TOPIC_BET -> decision latency;
- fraction of PRECARDs resolved at Level 0-2;
- escalation rate with valid escalation proof;
- wasted high-level runs that lower-level evidence could have avoided.

Fast, logically valid negative results count as successful throughput.
