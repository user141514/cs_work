# Ancestry–Transfer Gate V1 — Cross-Domain Structure Transfer for Top-Conference Topic Formation

date: 2026-09-28
status: AUTHORITATIVE_PRE_TOPIC_GATE
scope: computer science / ML / AI topic formation
owner: research_factory/computer_topconf_2027

## 0. Why this gate exists

The previous selector can reconstruct a current field, expose residuals, veto direct prior collisions, and run cheap falsifiers.

That is not sufficient for method generation.

Failure mode:
current field -> local residual -> local repair idea -> direct-prior check

This is locally rigorous but systematically biased toward incremental variations inside the target field.

The missing generator is:
**detect a target residual -> locate mature ancestor/neighbor fields that already solved the same abstract invariant -> extract their executable structure -> remove source-specific assumptions -> map the structure into the new target regime -> treat broken assumptions as the new research residual.**

This gate sits before TOPIC_BET activation.

## 1. Lifecycle

CURRENT_RESEARCH_STATE
->
TARGET_RESIDUAL
->
PROBLEM_ABSTRACTION
->
ANCESTOR_DISCOVERY
->
MATURE_OPERATOR_EXTRACTION
->
STRUCTURAL_MAPPING
->
NEGATIVE_TRANSFER_AUDIT
->
MISMATCH_RESIDUAL
->
TARGET REINSTANTIATION
->
DIRECT_PRIOR OCCUPANCY
->
CHEAP FALSIFIER
->
TOPIC_BET

No method experiment is authorized merely because a local residual exists.

## 2. Problem abstraction

Starting from the target-domain observation, repeatedly remove target-specific nouns until the object is stated as:

- State
- Transition/update
- Invariant/correctness contract
- Perturbation/change
- Control/intervention
- Evidence of success/failure

Stop when further abstraction would erase the causal mechanism.

Example:
"looped LM hidden feedback sometimes hurts"
->
"an iterative process reuses its own derived state; a perturbation in carried state can be amplified or attenuated by future updates; the system must decide whether/how to reuse that state."

This abstract object, not the target vocabulary, drives ancestor search.

## 3. Ancestor discovery

Find fields where the same invariant is first-class and has mature operators.

An ancestor is valid only if:
1. it owns the same abstract state-transition problem;
2. it has explicit intervention semantics, not only a metaphor;
3. it has known success and failure conditions;
4. it supplies measurable evidence.

Typical ancestors may include:
- control / dynamical systems;
- numerical analysis / fixed-point solvers;
- coding / iterative decoding;
- probabilistic graphical models / message passing;
- databases / incremental view maintenance;
- programming languages / self-adjusting computation;
- program analysis / slicing and change impact;
- distributed systems / consistency and invalidation.

Do not select ancestors because terminology sounds similar.

## 4. Mature operator extraction

For every ancestor, record:

SOURCE_STATE:
SOURCE_TRANSITION:
SOURCE_INVARIANT:
SOURCE_OPERATOR:
SOURCE_GUARD / ADMISSION CONDITION:
SOURCE_FAILURE_MODE:
SOURCE_EVIDENCE:

The transferable object is usually this contract, not a named algorithm.

Examples:
- feedback control: bounded closed-loop gain -> damping/isolation;
- fixed-point methods: contraction/residual -> relaxation/safeguarded acceleration;
- iterative decoding: information-transfer state -> continue/stop/retune iterations;
- self-adjusting computation: dynamic dependencies -> selective invalidation/recompute with from-scratch consistency;
- program slicing: dependency reachability -> impacted slice;
- incremental view maintenance: base delta + provenance -> derived-view delta.

## 5. Structural mapping

Map source to target explicitly:

source.state -> target.state
source.change/perturbation -> target.change
source.dependency/feedback edge -> target causal edge
source.operator -> target intervention
source.invariant -> target correctness property
source.evidence -> target measurable endpoint

A transfer is admissible only if the target mapping preserves the causal relation, not merely the name.

## 6. Negative-transfer audit

Before proposing a method, list source assumptions that fail in the target regime.

This is mandatory because the failed assumption often *is* the research contribution.

For each transfer:
- Which source assumption is absent?
- If the analogy is wrong, what target observation will contradict it?
- Does the mature operator remain well-defined?
- Does it optimize the target endpoint or only a proxy?
- Does local improvement imply global progress?

Examples:
- fixed-point contraction assumes convergence to an equilibrium; semantic recurrence may intentionally move through non-equilibrium representations;
- residual BP assumes a message-update graph with explicit dependencies; neural hidden-state dependencies are distributed/learned;
- self-adjusting computation assumes exact dependency tracking; coding-agent semantic dependencies may be latent, uncertain, or hallucinated.

## 7. Mismatch residual

Define:

MISMATCH_RESIDUAL =
mature source invariant/operator
-
assumptions valid in target regime.

The new research topic should primarily attack this mismatch.

Bad:
"apply small-gain theorem to LLMs."

Better:
"classical contraction is too strong for finite-horizon semantic recurrence; can a task-relevant finite-horizon induced gain identify harmful feedback while permitting useful non-contractive computation?"

Bad:
"use dependency graph for coding agents."

Better:
"classic incremental systems rely on exact dependencies; coding agents must infer semantic dependencies among requirements, plans, tests and code. Can an inferred derivation graph preserve from-scratch behavioral consistency under equivalent requirement revisions with less recomputation?"

## 8. Transfer operators -> mechanism portfolio

Do not collapse a mismatch residual directly into one favored target repair.

When multiple mature operators or target update semantics remain plausible, compile a bounded **2-4 family mechanism portfolio** before the first family-specific scientific result. Default to 3; use a singleton only when the frozen evidence uniquely forces one family.

Each family must contain:
1. ancestor / frozen source evidence;
2. invariant;
3. mature operator;
4. broken source assumption;
5. target replacement state/operator;
6. FAMILY_PROVENANCE_TICKET: frozen residual/interface -> generic causal operation -> family;
7. novel prediction;
8. complete target claim graph and direct-prior boundary;
9. cheapest discriminator;
10. family-specific negative scope and handoff trigger.

Families must differ in causal intervention point or causal assumption. Parameter/threshold/backbone/benchmark variants are not different families.

Different families may share an explicitly frozen interface-level necessary condition. Test that condition once when it is the cheapest discriminator; a valid negative may close every family that logically requires it.

Do not generate a portfolio of superficial analogies, and do not invent a fifth family after seeing results unless new evidence changes the residual/interface and starts a new formation round.

## 9. Target occupancy check

After transfer generation, return to current 2025-2026 target literature.

A transfer is killed if a single current prior already matches:
- target consumer;
- target state;
- intervention locus;
- evidence/correctness contract.

Do not preserve occupied transfers by renaming the ancestor concept.

## 10. Cheap falsifier

The first experiment must distinguish:
A. the transferred invariant is load-bearing;
B. a trivial target-native proxy already explains the effect;
C. the source-target analogy fails.

No TOPIC_BET activation if the experiment can only show correlation with no decision consequence.

## 11. Output contract

For every live target residual, write one compact table:

TARGET_RESIDUAL
ANCESTOR
SOURCE_INVARIANT
MATURE_OPERATOR
TARGET_MAPPING
BROKEN_ASSUMPTION
MISMATCH_RESIDUAL
NOVEL_PREDICTION
DIRECT_PRIOR_BOUNDARY
CHEAP_FALSIFIER
VERDICT

Allowed verdicts:
- TRANSFER_OPEN
- TRANSFER_OCCUPIED
- NEGATIVE_TRANSFER
- SOURCE_STRUCTURE_NOT_CAUSAL
- ASSET_BLOCKED
- WATCHLIST

## 12. Current application

Apply this gate before further compute to:
1. BET-COMP-01 Feedback Stability;
2. coding-agent Specification State watchlist.

Existing experimental authorization for Ouro is suspended until Feedback Stability passes this gate.
