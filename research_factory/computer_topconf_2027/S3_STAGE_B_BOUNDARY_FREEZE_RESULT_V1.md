# S3 Stage-B Offline Boundary Freeze Result V1

date: 2026-09-30
status: PASS
task: pi-mono-auto-93c17d3b
paid_s3_arm_authorized: false

## Frozen decisions

- TASK_INITIAL_STATE:
  `5133697bc454da5595655cf4b0c70d3c2c725677`
- official image:
  `ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-93c17d3b:2f7d1992e60d`
- controlled user-message source indices:
  `0,2,31,34,36,38,40,42,44,48,51,54`
- late revision:
  source_message_index `54`
- revision boundary:
  after the controlled pre-revision U1-U5 contract is implemented/persisted once by the fixed scientific agent, before U6/index 54 is delivered.

Historical observations/workflow triggers do not determine requirement exposure.

## Pre-revision contract

The scientific pre-revision task requires:
- repository-local loadable test extension;
- slash-command activation;
- hidden control-message injection;
- distinct signal-driven open/close behavior;
- open/close separation across messages;
- persistent multi-turn open state with later close;
- inactive-before-start behavior.

The historical 10-turn README workload is a verification scenario, not a permanent product feature.

## Late-revision contract

The late revision requires preserving the existing signal-extension behavior while fixing the UI lifecycle/responsiveness problem:
- streaming/output while UI is active must not freeze user typing/input;
- projection/update behavior must not repeatedly recreate or replace the interactive surface in a way that causes the reported freeze.

No specific implementation repair is frozen.

## R3 boundary

Exact R3 file/hunk scope is intentionally **PENDING_COMMON_PRESTATE**.

Frozen now is the semantic rule:
- UI projection/lifecycle/focus/update-dependent work is AFFECTED / REVALIDATE;
- extension placement, activation, hidden protocol, signal classification and other responsibilities independent of the UI projection mechanism may be reusable if actually present in the future common prestate.

Exact artifacts may be classified only after the fixed common prestate exists and before any post-revision arm result.

## Immutable common-prestate requirement

Any future scientific common prestate must materialize immutable:
- HEAD / dirty-state receipts;
- exact tracked patch bytes;
- copies + hashes of untracked task artifacts;
- deletion manifest;
- OMP session/history bytes + hash;
- model/runtime/tool identity;
- requirement-input hashes;
- derived-work manifest;
- outcome-blind R3 scope;
- one manifest hashing the entire freeze bundle.

A live mutable worktree is not a scientific snapshot or reuse denominator.

## Decision

`S3_OFFLINE_BOUNDARY_FREEZE = PASS`

Exact next step:

`S3_EXECUTION_LEVERAGE_GATE`

That gate must decide, without symmetry-driven spend, whether producing the scientific common prestate and paid R2/R3 evidence is decision-relevant.

No R0/R1/R2/R3 S3 arm is authorized yet.
