# BET-COMP-02 — Minimal Sufficient State for Iterative Generative Inference

date: 2026-09-28
state: TOPIC_BET_QUEUED
formal_paper_candidate: false
target: ICML 2027 / NeurIPS 2027

## Organizer

Current-state-only iterative generation can discard useful trajectory information, while full history or recurrent memory can be expensive and heavily occupied by prior work.

The remaining question is:
**what is the minimum state needed to recover the predictive advantage of full history?**

## Direct-prior boundary

Occupied:
- full-history non-Markov conditioning;
- persistent working memory;
- deterministic latent bypass;
- recurrent residual context.

Not claimed:
memory helps.

Potential novelty:
explicit predictive sufficiency / compression:
minimize state capacity while preserving the next-transition predictive distribution available from full history.

## Cheapest discriminator

No generator retraining initially.

Cache trajectories from a public iterative generator and fit:
A. current-state-only predictor;
B. current state + full history;
C. current state + compressed history at several small dimensions.

Measure:
- full-history predictive advantage;
- fraction recovered by compressed state;
- capacity curve.

Kill:
- no meaningful history gap;
- gap disappears after confidence/timestep controls;
- compressed state must approach full-history capacity.

Queue rule:
do not execute while BET-COMP-01 is active.
