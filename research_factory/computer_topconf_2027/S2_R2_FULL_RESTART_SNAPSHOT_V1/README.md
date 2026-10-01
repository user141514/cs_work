# S2 R2 Full-Restart Snapshot V1

This directory freezes the completed S2 R2 FULL_RESTART arm.

R2 is a valid independent execution from TASK_INITIAL_STATE, with one recorded prompt transport normalization: the frozen prompt file's final LF was stripped by shell command substitution while all 2,970 semantic characters were delivered unchanged.

Project reconstruction:
- exact base commit;
- tracked_dirty.patch;
- the two files under artifacts/.

The snapshot is independently reconstructable in the exact official image.

The frozen official verifier returns raw reward 0.0000, but its F2P harness is structurally invalid for this task base because it instantiates PackageManager even though PackageManager is a TypeScript interface and the runtime class is DefaultPackageManager.

Therefore this snapshot records:
- VALID R2 EXECUTION;
- positive secondary product-semantic evidence;
- INVALID PRIMARY VERIFIER MEASUREMENT;
- NO SCIENTIFIC R2 CORRECTNESS VERDICT;
- R3/R0/R1 NOT AUTHORIZED.
