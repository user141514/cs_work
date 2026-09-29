# S5 Stage-B R0 Result V1

date: 2026-09-29
status: VALID_S5_R0__S5_VALUE_NEGATIVE__R1_DECISION_IRRELEVANT
task: pi-mono-auto-ec7037ba
arm: R0 RAW_HISTORY
parent:
- S5_STAGE_B_R2_R3_RESULT_V1.md
- S5_R0_CONTINUATION_PATH_REPAIR_V1.md
- BFSC_SELECTOR_V2_DECISION_ADDENDUM_20260928.md
- ../../RESEARCH_MASTER_PLAN_DYNAMIC_V1.md

## 1. Valid arm identity

request_key:
s5-r0-raw-history-v2

turn_id:
turn_7e078188ec374f63b60063ca0f2c499b

outcome:
succeeded

terminal/quiescent:
true / true

runtime:
- GPT-5.6 Sol
- xhigh
- OMP process under lifetime
- tools = read,bash,edit,write,grep,glob
- no skills/rules/extensions

continuation workspace:
C:/Users/Administrator/.devspace/worktrees/spec_stageb_s5_base_69d02-0421b2d6

session:
D:/bio_paper/external/spec_stageb_sessions/s5_r0_raw_history_v2

The v1 relocated-workspace attempt remains INVALID_HARNESS and contributes no scientific evidence.

## 2. RAW_HISTORY continuation validity

The pristine common pre-revision session and R0-v2 session share the exact same byte prefix through the frozen U1-U4 state.

common pre-revision JSONL bytes:
1,366,879

common SHA-256:
76d15dfb5a82fa43f3b714cda5121ec4b14474f296430609a7ad7e495eaa76b9

R0-v2 first 1,366,879-byte SHA-256:
76d15dfb5a82fa43f3b714cda5121ec4b14474f296430609a7ad7e495eaa76b9

R0-v2 total JSONL bytes:
1,632,450

Therefore the admitted R0 continuation contains the frozen pre-revision transcript exactly and appends the U7 continuation rather than substituting a different history.

The continuation also uses the original absolute workspace identity required by S5_R0_CONTINUATION_PATH_REPAIR_V1.md.

## 3. Frozen verifier result

Local-equivalent verifier:
reward = 1.0000

All gates pass:
- changelog structure intact;
- changelog Unreleased growth;
- attribution format;
- directory completion has no trailing space;
- directory marker/continuation behavior;
- all four upstream P2P diagnostics.

Direct evaluator observations:
- directory line = `@src/`
- directory cursor = 5
- terminal file line = `@README.md `
- terminal file cursor = 11

Therefore:
S5_R0_CORRECTNESS = EQUAL_PASS_WITH_R2_R3.

## 4. Post-revision accounting

The R0 JSONL includes the entire shared U1-U4 history, so whole-session totals are not comparable to fresh R2/R3 post-revision sessions.

Whole R0-v2 session:
- model calls = 48
- tool calls = 134
- mutating tool calls = 4
- noncached input+output = 310,088
- reported cost = $4.1447392

Frozen common pre-revision session:
- model calls = 32
- tool calls = 106
- mutating tool calls = 2
- noncached input+output = 265,972
- reported cost = $3.3517408

R0 post-revision delta:
- model calls = 16
- tool calls = 28
- mutating tool calls = 2
- noncached input+output = 44,116
- reported cost = $0.7929984
- lifetime start-to-terminal wall = approximately 231.386 s

This delta, not the whole-session total, is the valid post-revision R0 accounting.

## 5. Frozen value-gate adjudication on S5

Existing valid R3:
- correctness = 1.0000
- credited pre-revision reuse = 36.84%
- reported post-revision cost = $2.4217048

Existing valid R2:
- correctness = 1.0000
- reported post-revision cost = $2.7281256

R0:
- correctness = 1.0000
- reported post-revision cost = $0.7929984

### V-A correctness rescue

R0 already matches R2/R3 correctness and costs less than R3.

Therefore, even if an unrun R1 were incorrect, R3 would still be strictly dominated by the other cheap rival R0 on the V-A correctness+reported-cost comparison.

V-A cannot become true on S5.

### V-B efficiency frontier

Frozen requirement:
R3 cost <= 0.90 * strongest-correct-cheap-rival cost.

Since R0 is already a correct cheap rival:
strongest-correct-cheap-rival cost <= $0.7929984.

Even using R0 alone, the permissive upper bound for R3 is:
0.90 * $0.7929984 = $0.71369856.

Observed R3:
$2.4217048.

Therefore V-B cannot become true on S5.
Any correct R1 cheaper than R0 would only make the threshold stricter.

## 6. Decision

S5_HEADROOM:
PASS locally (R3 vs R2), unchanged.

S5_VALUE_GATE_V:
NEGATIVE.

S5 is NOT a V-positive pressure witness.

R1 CONSOLIDATED_REFRESH is now decision-irrelevant for S5 and must not be run merely to complete a symmetric four-arm table.

This is a direct application of the execution-leverage invariant:
if a lower-cost existing result has already fixed the decision, further paid execution is forbidden.

## 7. What this does NOT establish

This does NOT kill BFSC/selective rederivation over the frozen S2-S5 horizon.

The prospective gate requires at least one V-positive witness among S2-S5.
S5 is one negative task.

It also does not authorize a new mechanism family or the queued orthogonality/invariant workflow research line.

## 8. NEXT_STEP

Total plan remains ACTIVE.

Next scientific step only:
S3 offline boundary freeze + execution-leverage gate.

Purpose:
determine, without paid post-revision model runs, whether S3 provides a valid late-revision regime and enough pre-revision work/headroom to justify the same sequential R2/R3-first policy.

Do not run S3 paid arms during that step.
Do not run S5 R1.
Do not start S2/S4.
Do not activate the orthogonality/invariant workflow candidate yet.
