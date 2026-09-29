# S1 R3 Oracle Scope Repair V2

date: 2026-09-28
status: FROZEN_REPAIR_BEFORE_RERUN
parent: S1_R3_ORACLE_SCOPE_FREEZE_V1.md
reason: PRE_REVISION_STATIC_COMPATIBILITY_OMISSION
repair_class: REPAIR_NEGATIVE, not scientific claim negative

## Static evidence available before post-revision outcomes

The frozen task-initial/pre-revision repository tests import and exercise:
- _replace_username
- anonymize_text
- anonymize_path
- Anonymizer
- _hash_username

Therefore repository compatibility structure already made _replace_username an observable callable seam for this task, even though its internal implementation is private.

The V1 oracle annotation was too aggressive because its input included only the newly added U4 patch, not the complete pre-existing test contract.

## Repaired invariant

R3 may invalidate and rederive the implementation behind _replace_username, but must preserve:
- symbol importability;
- accepted call signature;
- baseline-compatible behavior required by pre-revision tests.

R3 must NOT preserve:
- old str.replace implementation;
- old substring semantics;
- old case sensitivity;
- any assumption that the helper must remain the primary internal mechanism.

A thin compatibility wrapper is allowed.

## Everything else remains frozen

Independent reusable:
- six U4 behavioral requirements;
- pre-revision behavioral tests, subject to rerun.

Must rederive:
- regex compilation/cache ownership and keying;
- integrated U5 implementation reasoning;
- additional concrete speedup;
- post-U5 correctness/performance evidence.

No gold/reference/verifier outcome is admitted into the repaired implementation scope.