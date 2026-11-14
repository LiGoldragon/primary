# CriomOS history repair — 2026-11-12 16:52 UTC

The released, guarded repair completed.

* Containment read `hook.zoekt-index.command=true`; relevant lock files were
  absent.
* The shallow file matched the audited SHA-256
  `cdbf265b39864b696eb4e790edf01fb6a7a14724cba5d78d1cc4e7ce5f00f600`.
* `refs/heads/snapshot` matched the expected old value `01993a0d…` and was
  deleted with `git update-ref -d` using that old-value guard.
* The shallow bytes were rechecked unchanged, then only `.git/shallow` was
  removed.

Postconditions: the repository reports `shallow=false`; snapshot is absent;
all ordinary refs, linked-worktree HEAD records, and captured relevant statuses
compare byte-for-byte equal before and after. Common HEAD remains
`refs/heads/flow-home-opencode-42265e`; local main and all ordinary branches
were preserved. Ordinary ancestry now traverses `97cd643 -> … -> 4ef2668 ->
b222f17 -> 57ed3fd`; connectivity-only fsck exited successfully with no missing
or broken objects.

Evidence: `repair-before.txt`, `repair-after.txt`, the paired comparison files,
and the immutable pre-repair evidence under `raw/`.
