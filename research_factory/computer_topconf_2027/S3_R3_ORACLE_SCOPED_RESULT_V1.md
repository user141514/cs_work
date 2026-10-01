# S3 R3 Oracle-Scoped Result V1

date: 2026-10-01
status: VALID_R3__REUSE_PASS__PARTIAL_PARTIAL_ADJUDICATION_GAP__R0_R1_NOT_AUTHORIZED
task: pi-mono-auto-93c17d3b
arm: R3_ORACLE_SCOPED

## Decision

R3 executed validly and preserved substantial pre-revision work, but the S3 local-headroom verdict is **INCONCLUSIVE under the frozen decision rule**.

Do not label this result LOCAL_HEADROOM_PASS.
Do not label this result LOCAL_HEADROOM_NEGATIVE.
Do not run R0 or R1.

Reason: both R2 and R3 are partial verifier failures. The pre-registered S3 rule defines the explicit negative case `valid R2 succeeds but R3 fails`, and the positive case `R3 matches/approaches R2`, but it never freezes how partial verifier rewards or gate vectors should define "match/approach". Any numeric closeness threshold invented now would be post-outcome rule creation.

The authorization consequence is nevertheless unambiguous: R0 is allowed only if R3 headroom **survives**. That condition is not established. Therefore paid S3 execution stops here and control returns to selector/replanning.

## R3 execution identity

R3 started from a fresh worktree reconstructed from the immutable common-prestate bundle:
- exact base commit `5133697bc454da5595655cf4b0c70d3c2c725677`;
- byte-exact frozen pre-revision artifact `.pi/extensions/message-signals.ts`;
- fresh R3 session;
- frozen final requirements + outcome-blind R3 capsule only;
- no R2 implementation/verifier result exposed as solution context.

Agent identity:
- GPT-5.6 Sol;
- xhigh;
- no fallback;
- tools read/bash/edit/write/grep/glob;
- no skills/rules/extensions/title call;
- normal terminal exit and quiescent scope.

Final artifact:
- path: `.pi/extensions/message-signals.ts`;
- lines: 153;
- bytes: 4,720;
- SHA256: `66e09ad68c282c81e2b20417808ad1c888f406b4f90f483f9116b9e0ddef44b8`.

R3 changed only the frozen AFFECTED projection seam:
- `WIDGET_KEY` -> `STATUS_KEY`;
- `setWorkflowWidget/clearWorkflowWidget` -> `setWorkflowStatus/clearWorkflowStatus`;
- lifecycle projection calls changed from `setWidget` to `setStatus`.

The independent protocol/state/follow-up units remained byte-identical.

## Reuse accounting

Frozen independent semantic units preserved:
- 10 / 10 = 100%.

Frozen independent lines preserved:
- 103 / 103 = 100%.

Conservative credited reuse floor using the full 153-line pre-revision artifact as denominator:
- 103 / 153 = **67.32%**.

Whole-file positional identity:
- 142 / 153 = 92.81%.

The 30% reuse threshold is therefore clearly satisfied. Whole-file survival is not used as the scientific reuse denominator.

## R3 work / cost

Native OMP accounting:
- model calls: 38;
- tool calls: 60;
- mutating tool calls: 5;
- noncached input+output tokens: 165,390;
- reported model cost: $1.943112;
- wall: 377.848 s;
- input tokens: 148,045;
- output tokens: 17,345;
- cache-read tokens: 2,510,080;
- reasoning tokens: 11,750.

Compared with R2:
- model calls: -29.63%;
- tool calls: -43.40%;
- noncached input+output: -6.45%;
- reported cost: -44.80%;
- wall: -40.22%.

So R3 achieves substantial recomputation economy.

## Official verifier

Same frozen official S3 verifier/runtime as R2.

R3 final reward:
`0.5850`

R2 final reward:
`0.7650`

R3 gates:
- Gate1 command + handler: PASS
- Gate2 protocol injected: **FAIL**
- Gate3 observable reaction: PASS
- Gate4 distinct signals: **FAIL**
- Gate5 inactive-before-start: PASS
- Gate6 pattern/no-tool: PASS
- upstream canonical file exists: FAIL
- upstream canonical loadable: FAIL
- P2P extension directory: PASS
- P2P existing tps.ts compiles: PASS

R2 differs only in substantive Gate2 among the inner gates:
- R2 Gate2 PASS;
- R3 Gate2 FAIL;
- both Gate4 FAIL.

Therefore R3's frozen verifier gate profile is strictly weaker than R2's, and scalar reward is lower. This is real evidence against an unqualified "R3 matches R2" statement.

### Gate2 measurement-validity check

The additional Gate2 failure was checked against the real interactive runtime.

The source explicitly executes extension commands immediately while the session is streaming. `ExtensionContext.isIdle()` is defined as "not streaming". Therefore an extension command invoked with `isIdle()==false` is a real reachable interactive state.

R3 retained the pre-revision idle admission and rejects `/start` in that state, which is why the frozen harness does not observe protocol injection. This failure cannot be dismissed solely as an impossible-state verifier artifact.

## Why the final local-headroom label remains inconclusive

The evidence strongly shows:
1. reuse >=30%: PASS;
2. R3 cheaper than R2: PASS;
3. R3 verifier result lower than R2: observed;
4. both R2 and R3 full_verifier_success=false.

But the frozen S3 Execution Leverage Gate does not define:
- whether two `full_success=false` arms are considered a match;
- whether scalar reward should be used for partial-outcome closeness;
- a reward-ratio threshold;
- a gate-vector dominance rule.

Its explicit negative clause assumes successful R2, which did not occur.

Therefore converting this observation to LOCAL_HEADROOM_NEGATIVE now would introduce a post-outcome adjudication rule. Converting it to LOCAL_HEADROOM_PASS merely because both full-success booleans are false would be equally unjustified.

Scientific status:
`INCONCLUSIVE_PRE_REGISTERED_RULE_GAP`.

## Independent review gate

A fresh independent reviewer was attempted but could not execute under the current host worker backend. The review artifact is saved as:
`S3_R3_ADVERSARIAL_REVIEW_V1.json`

Its verdict is `BLOCKED`, with `independent_review=not_run`.

No reviewer approval is claimed.

## Immediate authorization consequence

The pre-registered gate authorizes R0 only if R3-vs-R2 headroom **survives**.

Because headroom is not established here:
- R0 remains unauthorized;
- R1 remains unauthorized;
- R2/R3 must not be rescued or rerun under a newly invented partial-score rule.

The proper next transition is higher-level selector/replanning using the frozen S3 evidence and preserving this adjudication gap as a protocol lesson for future tasks.

## NEXT_STEP

`BFSC_SELECTOR_REPLAN_AFTER_S3_PARTIAL_ADJUDICATION_GAP` only.

Do not run additional S3 arms before that selector decision.
