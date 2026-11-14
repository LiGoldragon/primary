# dzs immutable local candidate commit

## Exact identity

The previously sealed candidate tree was committed without changing its bytes by `git commit-tree` and named only in the isolated clone.

- Local ref: `refs/heads/candidate/dzs-owned567be7`
- Commit: `e6528df680e5a79de202b34e9b5ec3f6c5cac67e`
- Author and committer: `li <ligoldragon@gmail.com>`
- Parent: `c537aec8eaf6a4bea34ef022744d1df89283db97`
- Tree: `28187743c0d7e8f5876a37912123f0812a03673c`
- Pair file blob: `44aa10ba2f7a5c79fe078918e9c7489af74ec362`
- Sole changed path: `crates/translator/src/bin/belief-pair.rs`

The clone remains detached at the parent and its index remains the sealed tree. No normal commit hook ran.

## Rationale and evidence boundary

Source review covers every post-spawn exit: once both children are successfully spawned, one data-bearing `PairedChildren` owner holds them in `Option<Child>` slots; only a matching terminal status takes the already-reaped slot, and each subsequent return reaches owner cleanup.

The bounded test cases provide representative coverage for:

- owner rejection, which is a **pre-spawn** path;
- second-child spawn failure after the first child exists;
- Configure transport failure after both children exist; and
- both owned terminal orders.

This evidence does not establish dynamic per-exit exhaustiveness, syscall counts, exact reaper identity, arbitrary cleanup-failure behavior, or runtime behavior with ptrace, subreapers, or unrelated external children. Cleanup remains blocking and best effort. `waitpid(-1)` retains its explicit standalone two-direct-child scope.

No build or test was run while creating this immutable commit.

## Live main witness and separation

A read-only `git ls-remote` witnessed `refs/heads/main` at `9119cd60420b0f9bd82b129987efd856bde06280` on `git@github.com:LiGoldragon/belief-nexus.git` between `2026-11-04T22:01:27,703215075-06:00` and `2026-11-04T22:01:28,911377467-06:00`.

Between exact base `c537aec...` and live main, the sole intervening commit is `9119cd6`, which changes only `.beads/issues.jsonl`. No source path intervenes. The candidate remains local: no push, shared main mutation, deployment, bead closure, or production promotion occurred.
