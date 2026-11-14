# Horizon history repair — 2026-11-12 16:53 UTC

The released, guarded repair completed.

* Containment read `hook.zoekt-index.command=true`; relevant lock files were
  absent.
* `.git/shallow` matched the exact audited bytes `db7aed85…\n`.
* `refs/heads/snapshot` matched the expected old value `76dc9f06…` and was
  deleted with `git update-ref -d` using that old-value guard.
* The shallow bytes were rechecked unchanged, then only `.git/shallow` was
  removed.

Postconditions: the repository reports `shallow=false`; snapshot is absent;
all ordinary refs, linked-worktree HEAD records, and primary/wireless statuses
compare byte-for-byte equal before and after. The primary HEAD remains detached
at `b45d6ad4`; the wireless worktree remains clean at
`flow-d76b4c-wireless=f5037569`. Ordinary ancestry now traverses
`f5037569 -> db7aed85 -> e723ce11`; connectivity-only fsck exited successfully
with no missing or broken objects.

Evidence: `repair-before.txt`, `repair-after.txt`, the paired comparison files,
and the immutable pre-repair evidence named in `REPORT.md`.
