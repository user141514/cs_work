# Feedback Stability — Ancestry / Neighbor / Invariant / Transfer V1

date: 2026-09-28
status: ANCESTRY_TRANSFER_COMPLETE__TRANSFER_OPEN_BUT_CROWDED__RANK1_REACTIVATED
target_object: iterative generative / recurrent inference with reused derived state
previous_object: BET-COMP-01 Feedback Stability
current_object: Feedback Utility State = finite-horizon propagation risk + extrinsic progress
experiment_status: G0_ASSET_PREFLIGHT_PASS__DECISION_CONTRACT_PENDING

## 1. Target residual abstraction

Observed target pressure:
2026 iterative AI systems increasingly reuse intermediate predictions or hidden state:
- self-conditioning in diffusion;
- deterministic latent bypass across diffusion steps;
- persistent working memory;
- looped/recurrent transformer computation.

Current methods establish that history/feedback can help, while FastDiSS shows inaccurate self-conditioning can compound error.

Abstract state-transition problem:

derived state f_t
+
current computation state h_t
->
update F_t(h_t, f_t)
->
future state / output.

Unknown:
when does reusing f_t attenuate error and add useful information, and when does it amplify error or recycle stale information?

Do not assume the correct research object is a Jacobian.
The research object is the **decision-relevant state that tells whether another feedback/update is globally useful over the remaining horizon**.

---

# 2. Ancestor A — Feedback Control / Small-Gain Reasoning

## Source structure

SOURCE_STATE:
signals/states circulating around a feedback interconnection.

SOURCE_TRANSITION:
closed-loop interaction of forward and feedback operators.

SOURCE_INVARIANT:
disturbances should not be amplified without bound; robust closed-loop behavior requires the feedback interconnection to remain stable under uncertainty.

SOURCE_OPERATOR:
gain bounding, damping/attenuation, loop shaping, isolation or controller redesign.

SOURCE_GUARD:
operator gains and interconnection assumptions support a stability certificate.

SOURCE_FAILURE_MODE:
local component behavior can be individually reasonable while the closed loop is unstable; conservative gain bounds may reject stable nonlinear systems.

SOURCE_EVIDENCE:
induced gain / stability bounds; perturbation-response behavior.

## Target mapping

source disturbance
-> perturbation/error in carried hidden prediction/state.

source feedback-loop gain
-> amplification from a perturbation in recurrent/self-conditioning state to future hidden/output state.

source damping/isolation
-> scale, gate, delay, or remove feedback.

source robust stability
-> bounded downstream degradation under feedback error.

## Broken assumptions in AI regime

1. Classical stability often concerns infinite-horizon/asymptotic boundedness.
   The target computation is finite-horizon and task-directed.

2. Useful semantic recurrence may intentionally be non-contractive.
   Moving farther in representation space can be progress.

3. State/output norms need not align with task loss or semantic correctness.

4. The update operator is strongly input-, token-, layer- and context-dependent.

## Mismatch residual

The missing target object is not generic loop gain.
It is a **task-relevant finite-horizon induced feedback gain**:
how much a perturbation in feedback at step t changes downstream task-relevant state/output over the remaining recurrence horizon.

## Transfer hypothesis A1 — Finite-Horizon Semantic Feedback Gain

For a bounded perturbation delta f_t:

G_t^H =
task_distance(Y_{t:H}(f_t + delta), Y_{t:H}(f_t))
/
feedback_distance(delta)

or a hidden-state surrogate calibrated to actual downstream task degradation.

Prediction:
high finite-horizon gain should predict when feedback corruption is harmful better than current entropy/confidence and raw hidden-state norm.

Cheap falsifier:
on a frozen looped model, perturb recurrent state at each depth and measure:
- local one-step gain;
- H-step/terminal gain;
- output/task degradation;
- entropy/confidence/depth baselines.

Kill if:
finite-horizon gain provides no incremental predictive value over trivial proxies.

Verdict:
TRANSFER_OPEN, but not yet a topic until compared against Ancestors B/C.

---

# 3. Ancestor B — Numerical Fixed-Point Iteration / Deep Equilibrium Models

## Source structure

SOURCE_STATE:
iterate x_k.

SOURCE_TRANSITION:
x_{k+1} = F(x_k).

SOURCE_INVARIANT:
near a desired fixed point, the update should contract sufficiently for convergence.

SOURCE_OPERATOR:
relaxation/damping; Jacobian control; safeguarded acceleration; Anderson acceleration / mixing.

SOURCE_GUARD:
residual/contraction/Jacobian regime where acceleration is safe and convergence is meaningful.

SOURCE_FAILURE_MODE:
acceleration can be unstable outside its convergence basin; a small local residual or Jacobian property does not necessarily imply better task objective.

SOURCE_EVIDENCE:
residual decrease, convergence rate, spectral/Jacobian behavior.

Mature ML bridge:
DEQ work explicitly regularizes the Jacobian of fixed-point update equations to stabilize forward/backward fixed-point convergence.

## Target mapping

iterate x_k
-> recurrent hidden state h_k / latent denoising state.

fixed-point residual ||F(x)-x||
-> hidden-state update residual ||h_{k+1}-h_k||.

relaxation
-> damped recurrent update.

safeguarded acceleration
-> only accept stronger feedback/extra recurrence when the state indicates safe progress.

## Broken assumptions

The target need not have a meaningful fixed point.
Ouro-like recurrence can improve a final prediction while hidden states continue moving.
Therefore contraction/residual shrinkage may suppress useful computation.

## Mismatch residual

**Convergence is not the same as semantic progress.**

This yields a stronger question than "is the Jacobian stable?":

Can we distinguish:
- benign non-contractive semantic progress;
- harmful feedback amplification;
- idle/over-refinement?

## Transfer hypothesis B1 — Safeguarded Semantic Recurrence

Use a two-dimensional state:
1. stability/gain risk;
2. progress/information gain.

Intervention:
- continue/ordinary recurrence when progress is positive and gain risk acceptable;
- damp when progress positive but amplification risk high;
- stop/isolate when progress is low and recurrence mostly recycles/amplifies state.

Prediction:
a joint stability × progress controller should dominate a stability-only or entropy-only controller.

Cheap falsifier:
before building a controller, show that examples with similar local contraction/residual have materially different downstream task gains, and that an explicit progress state separates them.

Kill if:
contraction/residual alone already predicts value well, or no separable harmful-vs-useful non-contractive regime exists.

Verdict:
TRANSFER_OPEN and more target-specific than direct Jacobian transfer.

## Rejected direct transfer

"Apply Anderson acceleration to iterative generative inference" is not the preferred topic:
- it is an algorithm name rather than a preserved invariant;
- Anderson-like acceleration has already been transferred into modern ML/generative contexts;
- it assumes a solver-style objective closer to fixed-point convergence than the target semantic-computation contract.

---

# 4. Ancestor C — Iterative Decoding / Belief Propagation

This ancestor is unusually important because it already studies **repeated information exchange under a finite iteration budget**, closer to recurrent AI than classical infinite-horizon control.

## Source structure C1 — EXIT / information transfer

SOURCE_STATE:
soft beliefs/messages.

SOURCE_TRANSITION:
one decoder/component transforms incoming soft information into new extrinsic information passed to another component.

SOURCE_INVARIANT:
an iteration is useful only if it creates new information that moves the coupled system toward decodability/convergence.

SOURCE_OPERATOR:
use transfer functions/charts to predict convergence and iteration usefulness; design constituent interactions rather than only inspect local confidence.

SOURCE_FAILURE_MODE:
high confidence is not equivalent to useful extrinsic information; loops can recycle correlated information.

## Target mapping

soft messages
-> recurrent hidden/prediction state.

extrinsic information
-> information added by the current recurrence beyond what was already contained in the incoming state.

EXIT transfer
-> depth-conditioned map from incoming state quality/information to outgoing incremental information/task progress.

## Broken assumptions

Coding theory has a known channel/statistical model and semantically clean bits.
LLM/generative hidden states do not have an obvious scalar mutual-information coordinate or ground-truth extrinsic channel.

## Mismatch residual

The target lacks an operational notion of **new information contributed by a recurrence**, separate from confidence.

## Transfer hypothesis C1 — Extrinsic Progress State

Measure whether a recurrence contributes information predictive of the target that was unavailable from the previous state, rather than measuring only confidence.

Possible cheap operationalizations:
- incremental logit/task-loss gain conditional on previous prediction;
- probe residual target information in delta h_t after conditioning on h_t;
- counterfactual readout using h_t versus (h_t, delta h_t).

Prediction:
harmful/idle recurrence should have low extrinsic progress even when confidence increases.

Cheap falsifier:
cache recurrent states on Ouro. Compare:
- confidence change;
- hidden-state norm/residual;
- an outcome-blind trained probe for incremental target information;
against actual next-depth task improvement.

Kill if:
incremental-information state gives no information beyond confidence/depth.

Verdict:
TRANSFER_OPEN, high conceptual value; needs care to avoid becoming diagnosis-only.

---

## Source structure C2 — Residual Belief Propagation / informed scheduling

SOURCE_STATE:
messages on graph edges.

SOURCE_TRANSITION:
asynchronous message update.

SOURCE_INVARIANT:
not every update is equally urgent; scheduling should target messages whose update most reduces distance to a fixed point.

SOURCE_OPERATOR:
message residual estimates priority; damping/scheduling allocates computation to unstable/high-impact parts.

KNOWN FAILURE LESSON:
a local residual is a scheduling proxy, not guaranteed global value. Greedy/local update priority can waste work or hurt global error behavior when dependencies/correlations matter.

## Target mapping

message residual
-> local hidden/token/component change.

dynamic schedule
-> selective recurrent update / selective feedback.

## Transfer lesson

This ancestor argues against a naive target method:
"update the largest hidden-state residual" is insufficient.

A credible target state must estimate **downstream influence**, not merely local change magnitude.

Verdict:
SOURCE LESSON retained; direct residual scheduling is too weak.

---

# 5. Cross-Ancestor invariant

The common mature structure is:

current derived state
+
candidate update/feedback
->
local change
->
propagated future effect
->
global progress / harm.

All three mature fields distinguish, in different ways:

**local activity != global value.**

- Control: local component behavior must be evaluated through the closed loop.
- Fixed-point numerics: an aggressive update is useful only inside a suitable convergence regime.
- Iterative decoding: confidence/message change matters only insofar as it transfers useful information and advances convergence.

Therefore the target research state should not be merely:
entropy,
Jacobian norm,
hidden residual,
or recurrence depth.

The higher-level missing state is:

## Feedback Utility State

Two coordinates are minimally necessary:

1. PROPAGATION RISK:
if feedback is wrong, how strongly will its error influence the remaining computation?

2. EXTRINSIC PROGRESS:
does this update add task-relevant information beyond what the current state already contains?

This is the first genuinely cross-domain transferred object.

---

# 6. Strongest target hypothesis after transfer

Working hypothesis:

**Useful iterative feedback occupies a regime of positive extrinsic progress with bounded finite-horizon propagation risk.**

This yields a 2D policy:

| Progress | Propagation risk | Action |
|---|---|---|
| high | low | normal feedback / continue |
| high | high | damp / guarded feedback |
| low | low | stop / skip as idle compute |
| low | high | isolate / no-feedback |

This is not yet claimed novel.
It must survive 2026 target-prior search.

---

# 7. Direct target-prior boundary already known

Occupied:
- FastDiSS: robustness to inaccurate self-conditioning via training perturbation;
- Loopholing: always-on deterministic latent bypass;
- MetaState: persistent working memory with recurrent injection;
- Ouro: adaptive recurrence/early exit;
- generic adaptive-compute stopping.

Still potentially open:
- explicit finite-horizon feedback propagation risk;
- its combination with extrinsic-progress state;
- feedback-topology action (normal/damp/isolate), rather than only number-of-steps stopping.

Target prior attack must search this exact 2D contract before method activation.

---

# 8. Cheapest discriminator now changes

The old PRECARD:
"does local amplification predict downstream harm?"

is insufficient.

New ancestry-derived discriminator:

On one frozen recurrent model:
1. cache recurrent states across depth;
2. inject bounded perturbation at depth t and measure finite-horizon downstream propagation risk;
3. measure an extrinsic-progress proxy for the unperturbed recurrence;
4. label actual effect of continuing/feedback on task outcome;
5. compare four model families:
   - entropy/confidence/depth;
   - local residual/Jacobian-like sensitivity;
   - propagation risk only;
   - propagation risk + extrinsic progress.

Decision:
- if local stability alone wins, ancestor mismatch is unnecessary and the topic is narrower;
- if risk + progress cleanly separates useful non-contractive recurrence from harmful amplification, the cross-domain transfer produces a new target state worth a direct method pilot;
- if neither beats trivial proxies, kill Feedback Stability as a top-conference bet.

No GPU run is authorized until exact target-prior occupancy of this contract is checked.

---

# 9. Current verdict

BET-COMP-01 as originally phrased is DOWNGRADED from active experiment to:
**ANCESTRY-DERIVED REFORMULATION / PRIOR ATTACK REQUIRED**.

The strongest candidate object is no longer "Feedback Stability" alone.

It is:

**Feedback Utility State = finite-horizon propagation risk + extrinsic progress**

with conditional feedback topology as a possible downstream method.

This is a model change, not a naming change.
