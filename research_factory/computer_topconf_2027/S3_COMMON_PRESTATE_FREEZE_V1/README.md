# S3 Common Prestate Freeze V1

This directory is the immutable logical snapshot of the scientific S3 state immediately after valid U5 and before U6.

Reconstruction identity:

`base commit + tracked_dirty.patch + untracked artifact copies + deletion manifest`

The mutable scientific checkout is not the snapshot.

The original OMP JSONL already lives outside the mutable worktree and is frozen by exact path, byte size and SHA256 in `session_receipt.json`. It must not be continued after this boundary.

`R3_SCOPE_V1.md/json` freezes the outcome-blind semantic/file-hunk dependency scope before any post-revision arm is observed.
