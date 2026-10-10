# ProtoformStack branch train merged to main

Witnessed 2026-09-04 by subflow of flow 6329f1.
Method: `jj bookmark set main -r ProtoformStack` then `jj git push --bookmark main`
on each repository, followed by `jj git fetch` and rev-parse of `main@origin`.
All six were fast-forward merges (ProtoformStack contained main in every case).
Lock 630 (MergeProtoformStack, flow 6329f1) held on all six paths during the
operation and released after all pushes and witnesses completed.

## Per-repository

| repo | main was | main now (= ProtoformStack tip) | origin/main witnessed |
|---|---|---|---|
| protos | bfde3b878dd3 | 56c683ec8d1e | 56c683ec8d1e |
| datomic | b670c72d0c2c | a27f9b8e7789 | a27f9b8e7789 |
| ethos-zero | b922afba278d | 185f13a90354 | 185f13a90354 |
| signal-orchestrate | a597f1ae9910 | b25bbd9fbc8f | b25bbd9fbc8f |
| meta-signal-orchestrate | 5cdf35a989f2 | 5a99ccb1781f | 5a99ccb1781f |
| CriomOS-home | 433958aecbe4 | f8d5c5d7b58f | f8d5c5d7b58f |

## Command trail

For each repository:

```
jj bookmark set main -r ProtoformStack
jj git push --bookmark main
jj git fetch
jj log -r 'main@origin' --no-graph -T 'commit_id'
```

## signal-orchestrate dirty workspace

The default workspace held a superseded 2026-08-26 draft (4 modified files:
Cargo.lock, Cargo.toml, src/generated/signal.rs, tests/generated_contract.rs).
The draft was saved as a patch at `flows/6329f1/reports/signal-orchestrate-superseded-draft.patch`
(18565 bytes) before any operation. The bookmark advance and push do not
require a clean working copy in jj, so the draft was left in place. An
accidental `jj restore` was immediately undone; the workspace retains its
original dirty state.

## ProtoformStack branches

All six ProtoformStack branches remain on origin, not deleted, per instruction.

## Sources

- `jj log`, `jj status`, `jj bookmark set`, `jj git push`, `jj git fetch` on each repository
- `git merge-base --is-ancestor` to confirm fast-forward feasibility
- Orchestrate Lock 630 acquire and release
