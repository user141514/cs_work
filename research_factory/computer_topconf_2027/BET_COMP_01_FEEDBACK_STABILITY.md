# BET-COMP-01 — Feedback Stability for Iterative Generative Inference

date: 2026-09-28
state: REFORMULATED_AS_FEEDBACK_UTILITY_STATE__RANK1_PRECARD__CONTRACT_V2_FROZEN__LEVEL1_HOOK_NEXT
formal_paper_candidate: false
target: ICML 2027 / NeurIPS 2027

## Current authority override

The original single-coordinate "Feedback Stability" framing below is historical.

Current object is the ancestry-derived reformulation:

**Feedback Utility State = finite-horizon propagation risk + extrinsic progress**.

Bounded direct-prior attack is already complete with `DIRECT_VETO=false / TRANSFER_OPEN_BUT_CROWDED`.

`FEEDBACK_UTILITY_G0_ASSET_PREFLIGHT_V1 = PASS` on public Ouro-1.4B revision `574fa66...` and PC2 local resources.

`FEEDBACK_UTILITY_DECISION_CONTRACT_FREEZE_V1 = PASS`.

`FEEDBACK_UTILITY_LEVEL1_HARNESS_PREFLIGHT_V1 = REPAIR_NEGATIVE__EXIT_AT_STEP_INDEXING_CONTRACT_MISMATCH` after tokenizer/data admission PASS.

`FEEDBACK_UTILITY_DECISION_CONTRACT_REPAIR_V2 = PASS_REPAIR_ONLY` with no scientific-field drift beyond the indexing mapping.

Exact next step: `FEEDBACK_UTILITY_LEVEL1_HOOK_PREFLIGHT_V2`.

No checkpoint download/GPU scientific run is authorized before the remaining Level-1 hook PASS.

## Organizer

Iterative generative models often reuse their own intermediate predictions through self-conditioning, recurrent residuals, latent bypasses or working memory. The field has established both sides:
- feedback can correct errors and preserve useful intermediate information;
- inaccurate feedback can compound error, especially under few-step inference.

The unresolved interface is not whether feedback exists, but whether **feedback should be treated as a controlled dynamical operator rather than an always-on architectural choice**.

## Claim under consideration

A local feedback-amplification / stability quantity measured at inference time predicts when injecting historical information will improve or degrade final generation better than simple confidence, entropy, timestep or feedback magnitude.

If that state exists, it could support conditional feedback:
- ordinary feedback in stable regimes;
- damped feedback near instability;
- no-feedback / isolated side state in unstable regimes.

## Current direct-prior boundary

FastDiSS:
occupies compounded self-conditioning error and training-time robustness to noisy feedback.

Loopholing Discrete Diffusion:
occupies deterministic latent propagation across discrete denoising steps.

Residual Context Diffusion:
occupies recurrent injection of discarded token representations.

MetaState:
occupies persistent recurrent working memory around a frozen diffusion LM.

None of these, under the bounded 2026 audit, directly owns:
local stability state -> conditional feedback topology -> matched endpoint evidence.

Novelty runway is therefore narrow but currently open.

## G0 exact-asset candidate

Primary:
ByteDance/Ouro-1.4B, a public 1.4B Looped Language Model with configurable recurrent steps and adaptive exit.

Secondary confirmation only after primary PASS:
official ICLR 2026 Loopholing Discrete Diffusion repository (ahn-ml/lddm), with released pretrained checkpoints and baseline implementations.

Why Ouro is first:
- 1.4B is single-GPU inference-feasible;
- recurrent depth is explicit and configurable;
- custom model code exposes the recurrent computation path;
- no generator training is needed for the discriminator;
- the built-in adaptive-exit/entropy signal is a strong cheap rival that the proposed stability state must beat.

## PRECARD discriminator

Type:
necessary state/leverage probe; not yet a method pilot.

Arms/signals on Ouro:
- local amplification/sensitivity statistic under bounded recurrent-state perturbation;
- built-in adaptive-exit / entropy signal;
- output confidence / entropy;
- recurrence depth;
- recurrent-state norm/change magnitude.

Endpoint:
downstream generation degradation / improvement caused by the perturbation or by feedback ablation.

Required observation:
the stability statistic must predict sign or magnitude of downstream recurrence benefit/harm materially better than Ouro's built-in adaptive-exit/entropy signal and the other trivial proxies across multiple depths and perturbation scales.

Kill:
if it collapses to timestep/confidence or has weak predictive value.

Advance:
only if the state is predictive; then test a direct stability-gated feedback controller against always-on feedback and no-feedback at matched NFE/latency.

## Paper shape if successful

Figure 1: feedback is non-uniformly beneficial and exhibits stable/unstable regimes.
Figure 2: local stability predicts error propagation beyond trivial proxies.
Figure 3: stability-gated feedback improves quality/compute frontier across at least two iterative-generation settings.
