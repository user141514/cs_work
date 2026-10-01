# S2 Common Prestate Freeze V1

This directory is the immutable logical snapshot of S2 immediately after valid U3/source_message_index=20 and before late-revision bundle 37/39.

Reconstruction identity:

`base commit + tracked_dirty.patch + deletion manifest + untracked-artifact manifest`

For S2 the deletion and untracked manifests are empty; the material project state is the exact 8,292-byte tracked patch over base `e54dff7...`.

The mutable WSL worktree is not the snapshot.

The original scientific session is copied byte-for-byte to:

`D:/cs_work/external/spec_stageb_sessions/s2_common_pre_frozen_v1/...`

and frozen by exact path, byte size and SHA256 in `session_receipt.json`. The live session must not be continued after this boundary.

`R3_SCOPE_V1.md/json` freezes the outcome-blind semantic/file-hunk dependency scope before any late-revision/R2/R3 outcome.
