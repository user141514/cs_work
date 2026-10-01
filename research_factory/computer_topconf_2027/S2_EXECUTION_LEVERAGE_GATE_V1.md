# S2 Execution Leverage Gate V1

date: 2026-10-01
status: SCIENTIFIC_LEVERAGE_PASS__EXECUTION_DEFERRED_IMAGE_NOT_READY
task: pi-mono-auto-a4fca584
parent:
- EXECUTION_LEVERAGE_GATE_V1.md
- S2_MECHANISM_EXPOSURE_GATE_V1.md
- S2_STAGE_B_BOUNDARY_FREEZE_V1.md
- BFSC_SELECTOR_REPLAN_AFTER_S3_20261001.md
formal_paper_candidate: false
paid_model_authorized_now: false

## 1. Owned decision

Should the factory pay for S2 scientific execution, and if so what is the minimum sequential evidence purchase that can still change BFSC H/V?

This gate does not decide:
- whether BFSC is a paper candidate;
- whether S2 is V-positive;
- whether RAW_HISTORY fails;
- whether S4 should be skipped.

## 2. Lower-level evidence already exhausted

Zero-model evidence establishes:
- S2 mechanism exposure = `EXPOSURE_SOURCE_PROVEN`;
- S2 offline Stage-B boundary freeze = PASS;
- task initial state, pre-revision sequence, late-revision bundle, pre/final specs, immutable common-prestate contract and future outcome-blind R3 semantic rule are frozen;
- S2 is one of only two remaining unobserved V-positive witness opportunities (S2/S4).

Static evidence cannot establish:
- whether the fixed scientific agent produces material pre-revision derived work;
- whether FULL_RESTART reaches frozen verifier success;
- whether ORACLE_SCOPED preserves correctness/reuse under the late path-base correction;
- provider work/cost under the intervention.

Therefore some paid execution remains decision-relevant.

## 3. Prospective PARTIAL_REFERENCE_GUARD implication

The S3 result changed execution semantics but not H/V metrics.

A valid S2 R2 with `full_verifier_success=false` cannot make S2 V-positive under the frozen V-A/V-B contract.

The S3-style sequence:

`common prestate -> R2 -> R3`

must therefore be refined to:

`common prestate -> freeze exact R3 scope -> R2 -> conditional R3`.

### Why common prestate still comes before R2

The immutable contract requires exact R3 artifact/file-hunk scope to be frozen from the actual pre-revision derived state before any post-revision arm outcome.

Running R2 first and creating the common prestate only afterward would expose scope construction to post-outcome contamination.

Therefore the first paid object remains the scientific common-prestate run.

## 4. Minimum paid sequence

### Step P1 — COMMON_PRESTATE

Authorized only after exact runtime preflight passes.

Purpose:
- execute the controlled pre-revision sequence 0/6/8/20 once under GPT-5.6 Sol/xhigh;
- determine whether material derived work exists;
- freeze exact common-prestate bytes/session and exact outcome-blind R3 affected/revalidate/independent scope.

Stop if:
- no material derived work -> S2 NONIDENTIFIABLE for reuse;
- execution/runtime invalid -> repair bounded runtime only.

### Step P2 — R2 FULL_RESTART

Run independently from TASK_INITIAL_STATE + frozen final spec.

If R2 is invalid:
- no scientific verdict; bounded runtime repair only.

If R2 full verifier success = true:
- S2 remains eligible to become V-positive;
- authorize R3 next because R3 correctness/reuse is required for both local H headroom and V.

If R2 full verifier success = false:
- mark `PARTIAL_REFERENCE`;
- S2 cannot become V-positive under the frozen V gate;
- do not invent a local reward/gate-vector match threshold;
- do not run R0/R1 for S2 V.

### Step P3 — R3 ORACLE_SCOPED, conditional

If R2 full success:
- run R3 immediately from the immutable common-prestate + frozen exact scope.

If R2 partial:
- do **not** automatically spend on R3.
- retain the immutable prestate/scope and defer S2 R3 until the remaining S4 evidence makes clear whether S2 R3 can still change an already-frozen original H endpoint (aggregate verifier-success count, median reuse, or another frozen Stage-B predicate).
- if later bounds show S2 R3 cannot change H, skip it permanently as decision-irrelevant.

This is prospective and does not rescore S3.

## 5. Why S2 still has sufficient leverage

S2 is higher leverage than S4 under the frozen order:
- analyze-only -> implementation authorization -> active path persistence -> authoritative path-base correction;
- mechanism exposure is directly source-proven;
- the revision changes a concrete semantic basis while preserving surrounding package/settings responsibilities.

Portfolio state:
- S5: V-negative;
- S3: V-ineligible because R2 full success=false;
- S2/S4: only remaining unobserved V-witness opportunities.

Thus a successful S2 R2/R3 pair could still produce the first prospective V-positive witness and materially change whether BFSC proceeds beyond PRECARD.

## 6. Runtime readiness

Current zero-model probe:
- Docker client/server: 29.8.0 / 29.8.0;
- server: linux/amd64;
- daemon reachable;
- required official image:
  `ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-a4fca584:d1a6ee81ebeb`;
- image is **not currently present locally**.

Therefore the scientific leverage is positive but exact S2 runtime identity is not yet locked.

This is operational readiness, not a scientific negative.

## 7. Verdict

SCIENTIFIC_EXECUTION_LEVERAGE:
`PASS`

CURRENT_EXECUTION_AUTHORIZATION:
`DEFERRED_IMAGE_NOT_READY`

Paid model calls remain forbidden now.

## NEXT_STEP

`S2_RUNTIME_PREFLIGHT_V1` only.

Zero-model preflight must:
1. pull/inspect the exact official S2 image;
2. verify image identity and exact base commit;
3. verify non-root agent/toolchain/runtime;
4. execute the frozen official verifier on the no-patch baseline or equivalent declared baseline path;
5. record task/verifier hashes and runtime/P2P gates;
6. stop without model calls.

Only after preflight PASS may P1 COMMON_PRESTATE become authorized.
