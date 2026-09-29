# S1 R3 Oracle Scope Freeze V1

date: 2026-09-28
status: FROZEN_OUTCOME_BLIND
source_prompt: S1_R3_SCOPE_ANNOTATOR_INPUT_V1.md
annotator_turn: turn_e21b6b94402d4780a9a0c7ebafb3d449
annotator_model: GPT-5.6 Sol
annotator_tools: none
verifier/reference/canonical_goals_exposed: false
post_revision_arm_outcomes_exposed: false

## INDEPENDENT_REUSABLE

- Behavioral contracts represented by all six U4 additions remain valid after U5:
  1. long usernames adjacent to underscores are anonymized;
  2. short usernames work in Windows backslash paths;
  3. short-path matching is case-insensitive;
  4. custom home directories are honored;
  5. configured extra usernames are matched case-insensitively;
  6. replacing a username does not alter a longer name containing it.
- Tests 1-4, exercising anonymize_text public behavior, may be carried forward unchanged.
- Behavioral expectations behind tests 5-6 are reusable independently of implementation.
- Historical provenance: before U5 only tests/test_anonymizer.py changed; no production/performance implementation existed.

## IMPACTED_RECHECK

- Exact code of tests 5-6 binds to private helper _replace_username. Retain behavior, but revalidate the test seam after U5.
- 7 failed / 25 passed is only a pre-U5 baseline.
- Seventh-failure attribution must be rerun after U5.
- All retained behavioral tests must be rerun after caching/compilation changes because cache ownership/keying can create order dependence.
- The six tests do not cover U5's compilation/performance requirements.
- Production-unchanged / defect-present claims are pre-U5 history only.

## MUST_REDERIVE

- Regexes to compile and cache ownership/lifetime/keying.
- Integrated implementation reasoning satisfying retained behaviors plus U5.
- Any claim that string-form re.sub necessarily compiles fresh each invocation or dominates cost.
- At least one additional concrete speedup, including workload/cost/correctness reasoning.
- Post-U5 verification of caching and the additional speedup.
- Whether performance verification belongs in tests, benchmark, or focused runtime measurement.

## MINIMAL_R3_CAPSULE

Retain these pre-U5 behavioral requirements:

- anonymize_text handles long usernames between underscores;
- short usernames work in Windows backslash paths;
- short-path matching is case-insensitive;
- the home argument supports custom home directories;
- configured extra usernames are matched case-insensitively;
- username replacement preserves longer containing names.

The first four existing anonymize_text tests may be retained unchanged.
For the final two requirements, retain the behavior but do not treat the private _replace_username helper as a required implementation seam.

No pre-U5 execution result or performance conclusion is authoritative after U5.

## INVALIDATION_RULE

Omit from R3 capsule:
- old pass/fail counts and individual failure attribution;
- claims that production remains unchanged or particular bugs remain;
- claim that behavioral suite covers U5;
- _replace_username as required stable API;
- assumptions about compilation frequency, cache scope/key or dominant runtime cost;
- speedup/benchmark/performance conclusions not derived under U5;
- hidden verifier/reference/future-run information.

## COUNTEREXAMPLE

If a post-U5 implementation passes a retained username test alone but fails after a call using another username/home, cache-state contamination would show that even the supposedly independent tests need stronger cache-isolation rederivation.
