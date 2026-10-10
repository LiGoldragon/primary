# Witness: audit of the flow0174-block-to-field-sol receipt commit

Method: read-only. Read the named transcript
(`/tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/tasks/a832e5a56a9a3ec4a.output`)
by parsing its JSONL records for `tool_use`/`tool_result` blocks (never read whole),
then re-derived the repository facts myself with `jj --ignore-working-copy log/file
list` against the live checkout and `git ls-remote` against the real remote. No `jj
commit`, `bookmark`, `rebase`, `push`, `undo`, or `restore` was run by this witness;
only `--ignore-working-copy` reads and one `git ls-remote`.

## What the subflow ran (in order, from its tool calls)

1. `git status --short`; `git rev-parse --is-inside-work-tree` in
   `/home/li/wt/primary/56ae53` → exit 128, "fatal: not a git repository".
2. `jj status` (twice) in the same directory → succeeded, showing a large dirty
   working copy spanning `flows/56ae53/*-recovery/*` and dozens of `flows/8904b1/*`
   paths, atop parent `tollpmto b7af6d53`.
3. `jj commit -m '<message>' flows/8904b1/receipts/flow0174-block-to-field-sol.md`
   — scoped to that one path. New commit `4a71b9d9`, parent `b7af6d53`.
4. `jj bookmark set main -r @-` → refused: "Refusing to move bookmark backwards or
   sideways: main" (local main had already advanced past the commit's parent).
5. `jj log -r 'main | @- | ::@- & ::main'` — read-only, inspected the divergence.
6. `jj show -r 4a71b9d9 --stat` → confirmed exactly one file, 62 insertions, 0
   deletions.
7. `jj git push --allow-new -r 4a71b9d9` → exit 2, invalid flag; no effect.
8. `jj git fetch` → "Nothing changed" (local already had current remote refs).
9. `jj rebase -r 4a71b9d9 -d main` → rebased the scoped commit onto main's current
   tip; also rebased its one descendant (the ordinary working-copy commit holding
   the unrelated dirty pile, unchanged in content, just re-parented).
10. `jj log` / `jj show -r 3a040031` (read-only) to locate the rebased commit.
11. `jj bookmark set main -r 3a040031` → succeeded (forward move).
12. `jj git push --bookmark main` → "bookmark: main [move forward from
    b2a41e35d0b7 to 3a0400313692]".
13. `jj log -r 'ancestors(main, 3)'` — read-only confirmation.

No `git` write command, no `jj undo`/`restore`, and no field-tool commit command
appears anywhere in the transcript's tool calls.

## Where the commit is

- Repository: the jj repo whose store is `/home/li/primary/.jj/repo` (this
  checkout's `.jj/repo` file redirects there); real git remote `origin` =
  `git@github.com:LiGoldragon/primary.git`.
- Commit: `3a04003136926a53f68d729161642e221a699568`
  (change id `vvpuxmlznnwmrkvprskwvnxmywsrwzvt`), parent `b2a41e35d0b756858f69f70bb76c0f345cbba8b0`
  ("flows: record recovery status witness").
- Author/committer: `li <li@goldragon.criome.net>`.
- Message: "Fable 8904b1: report flow0174 socket-length block to Field Sol 9ac67c"
  plus the Claude co-author/session trailers.
- Paths changed: exactly one — `flows/8904b1/receipts/flow0174-block-to-field-sol.md`
  (62 insertions). Confirmed both by `jj show -r 4a71b9d9 --stat` in the transcript
  (pre-rebase) and by `jj --ignore-working-copy file list -r main flows/8904b1`
  here, which lists only that receipt plus one unrelated later witness file from a
  different commit. No other flow's files rode along in this commit; the huge dirty
  pile stayed in the separate (unrelated, still-uncommitted) working-copy commit.

## Is it on the real remote's main

Yes. `git ls-remote git@github.com:LiGoldragon/primary.git refs/heads/main` returns
`10f78113bb13fd2210ac73e9c88ec71a7fa50a9a`. `jj --ignore-working-copy log -r
'ancestors(main,3)'` shows that commit's ancestry as
`10f78113 → 3a040031 (this receipt) → b2a41e35`. The receipt commit is an ancestor
of the real remote's current main tip; a later, unrelated commit (`10f78113`,
a witness landed afterward) now sits on top of it.

## How this checkout relates to the repository

`/home/li/wt/primary/56ae53/.jj/repo` is a redirect file whose content resolves
(via `realpath`) to `/home/li/wt/primary/56ae53/.jj/repo` — i.e. this checkout's
`.jj` is a **workspace** pointer, and the file itself contains the relative path
`../../../../primary/.jj/repo`, which normalizes to `/home/li/primary/.jj/repo`.
The actual store, refs, and operation log live there, not under
`/home/li/wt/primary/56ae53`. There is no `.git` directory anywhere under
`/home/li/wt/primary/56ae53`, which is why a plain `git` command run from here
fails with "not a git repository": git looks for `.git` in this directory or its
parents and finds none — the git colocation, if any, lives with the store at
`/home/li/primary`, not with this workspace. `jj` commands work here regardless,
because jj resolves the repo location through the `.jj/repo` redirect rather than
requiring a local `.git`.

To commit a file under its own flow directory from this checkout, a flow must:
1. `jj commit -m '<message>' <path-under-its-flow-dir>` — always with explicit
   path(s), naming only files it owns; never a bare `jj commit` here since other
   flows keep dirty, uncommitted work in the same shared working copy.
2. `jj bookmark set main -r @-` (or, if that refuses because local `main` has
   moved, `jj git fetch` then `jj rebase -r <that commit> -d main` to bring it
   forward, then `jj bookmark set main -r <rebased commit>`).
3. `jj git push --bookmark main`.
4. Verify scope with `jj --ignore-working-copy file list -r main <flow-dir>` (or
   `jj diff -r @- --name-only` right after the commit) before and after any
   rebase, and verify landing with `git ls-remote <real-remote-url>
   refs/heads/main` against the pushed commit id — not the checkout's own memory
   of its bookmark. Never use raw `git` (no `.git` exists here) and never use the
   field tool's commit command in Primary.

This is exactly the sequence the audited subflow followed, including the
fetch/rebase recovery step made necessary by main having moved concurrently.

## Whether it did any harm

None found. The final push (`b2a41e35 → 3a040031`) was a plain fast-forward on
the real remote; the ancestry shows no rewriting of any other commit. No `jj
undo`/`restore` ran, so no operation log was restored. The earlier failed
attempt (`jj git push --allow-new -r 4a71b9d9`, invalid flag) had no effect
(exit 2 before any network action). The rebase in step 9 gave the *other*
flows' still-uncommitted working-copy commit a new local commit id (its parent
changed from `b7af6d53` to the rebased receipt), but its file contents were
untouched — confirmed here: the large dirty file list observed in this session
predates and is independent of that commit id churn, and none of it is
reflected in `main`'s tracked files beyond the one receipt. No other working
copy elsewhere was touched; this was a single shared-store rebase local to this
audit's own checkout.

## What of this flow's is still uncommitted

Disk vs. `jj --ignore-working-copy file list -r main flows/8904b1` (which lists
only the 2 files landed on main to date):

| Directory | On disk | Tracked on main | Uncommitted |
|---|---|---|---|
| flows/8904b1/ (log.md) | 1 | 0 | 1 |
| flows/8904b1/receipts | 52 | 1 | 51 |
| flows/8904b1/reports | 9 | 0 | 9 |
| flows/8904b1/witnesses | 16 | 1 | 15 |
| **Total** | **78** | **2** | **76** |

(This count includes the witness file this audit itself just wrote, since it
was written to disk before this table was produced.)

## Inferences vs. observations

- Observed directly: every transcript command and its result; every `jj`/`git`
  fact above from live, read-only queries against this checkout and the real
  remote.
- Inferred: that the "flows: record recovery status witness" and
  "flow0174-herdr-fixture-bringup-2" commits surrounding this one came from
  other flows/sessions working the same shared store concurrently — inferred
  from their unrelated messages and timestamps, not directly witnessed here.
- Unknown: whether the still-dirty pile under `flows/56ae53/*-recovery/*` and
  the rest of `flows/8904b1/` belongs to flows that intend to commit it
  themselves; not established by this audit.
