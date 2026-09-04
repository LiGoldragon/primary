# Orchestrate Default Checkout and Beads State

Witness of /git/github.com/LiGoldragon/orchestrate default checkout displacement
and `.beads` availability, observed 2026-09-04 ~15:50 UTC+2.

## What Moved the Working Copy

Raw git commands executed at 2026-09-04 11:31-11:32 (from `git reflog`):

1. `git stash` -- stashed dirty tree (incl. `.beads` changes) while detached at e0f3bc5
2. `git checkout main` -- moved HEAD from e0f3bc5 to main (then at dadd537)
3. `git pull origin main` -- fast-forwarded main to 9585484 (ProtoformStack docs)
4. `git commit` -- committed "Correct 0.27 rollout" (281e070) directly on main
5. `git checkout be5dfa2` -- moved HEAD to old May 18 commit

All five operations bypassed jj. The jj op log shows no explicit default@
movement at that time. One hour later, jj imported the changed git state via
two operations: `import git head` (op 7386d8f8d94b) and `import git refs`
(op 31a8d4b64482), creating the current default@ working copy `slprsnst`
(a9320f8a) on top of main* (885f6e3e).

**Result:** git HEAD is at be5dfa2 (May 18 commit) but jj default@ thinks it
is on 885f6e3e. The filesystem matches be5dfa2 -- `.beads` is absent because
that commit predates its introduction. `bd where` finds no workspace.

## The Old Working Copy Snapshot

The jj change `rntxsplq` (b87739e6) is the snapshotted former default@ working
copy, a child of e0f3bc5 with no description, dated 2026-09-04 04:01. Its diff:

    .beads/issues.jsonl     7 lines added
    ARCHITECTURE.md         4 lines changed
    README.md               3 lines changed
    src/bin/orchestrate.rs   7 lines changed
    tests/live_nexus.rs     76 lines added

The same dirty tree also survives as `git stash@{0}` (5 files, 89 insertions).

## Beads on Main

`.beads` IS tracked on origin/main (885f6e3e). All 11 beads exist there:

| ID | Status | Type |
|---|---|---|
| orchestrate-4ui | closed | epic |
| orchestrate-4ui.1 | closed | task |
| orchestrate-4ui.2 | closed | task |
| orchestrate-4ui.3 | closed | task |
| orchestrate-4ui.4 | closed | task |
| orchestrate-4ui.5 | closed | task |
| orchestrate-4ui.6 | closed | task |
| orchestrate-de0 | in_progress | task |
| orchestrate-yew | closed | feature |
| orchestrate-xbe | closed | task |
| orchestrate-egu | closed | epic |

The 7 beads added in the dirty tree (orchestrate-4ui epic + 6 children) and
orchestrate-de0 (added later) are all present on main. Origin/main is a
strict superset of the dirty working copy's `.beads` content. The non-beads
dirty changes (ARCHITECTURE.md, README.md, orchestrate.rs, live_nexus.rs)
are superseded by the 20+ commits between e0f3bc5 and 885f6e3e.

**No bead data is lost.** The beads written this morning exist on origin/main,
not only in the lost working copy.

## Beads Store Format

metadata.json declares `"backend": "dolt"`, `"dolt_mode": "embedded"`. However,
the Dolt database directory (dolt/ or embeddeddolt/) is gitignored and absent
from worktrees. The `.beads/issues.jsonl` file IS tracked and committed. The
store is a plain file set (config.yaml, .gitignore, issues.jsonl, metadata.json,
README.md) safe to restore via file copy or `jj restore`. Running `bd bootstrap`
in any working directory with the JSONL will recreate the embedded Dolt database.

## Restoration

No `.beads` restoration is needed -- the beads are on main. If the non-beads
dirty tree changes from `rntxsplq` were wanted, either command would recover
them without touching anything else:

    jj restore --from rntxsplq --to slprsnst ARCHITECTURE.md README.md src/bin/orchestrate.rs tests/live_nexus.rs

Or from the git stash:

    git stash show -p stash@{0} | git apply

The default checkout itself needs repair: git HEAD (be5dfa2) diverges from
jj default@ (on 885f6e3e). Running `jj status` in the default checkout would
snapshot the be5dfa2 filesystem state as `slprsnst`'s content, producing a
massive deletion diff against 885f6e3e. To repair, first align git HEAD with
what jj expects before any jj snapshot occurs.

## Default Workspace Target

origin/main: 885f6e3e ("Import datomic::Situated<datomic::Fault>; remove
local Situated; bump 0.29.2"). The jj main* bookmark agrees. main@git
shows ef10df21 (one behind) because jj has not fetched since the
orchestrate-situated-6329f1 worktree pushed.

## Orchestrate Locks

`orchestrate 'Observe.Locks'` returns three active locks, none covering
/git/github.com/LiGoldragon/orchestrate:

- Lock 639: DialectSkills / 6329f1 on Curriculum
- Lock 440: WisprAuthWitness on listener
- Lock 441: WisprEdgeProxy on listener

No other flow holds an Orchestrate Lock on the orchestrate repository.

## Sources

- `jj op log --limit 60` in /git/github.com/LiGoldragon/orchestrate
- `jj log -r 'all()' --limit 80` in the same
- `git reflog --date=iso` in the same
- `git stash list` and `git stash show --stat`
- `git ls-tree origin/main .beads`
- `git show origin/main:.beads/issues.jsonl` and `git show e0f3bc5:.beads/issues.jsonl`
- `jj diff -r rntxsplq --stat` and `jj diff -r rntxsplq -- .beads`
- `orchestrate 'Observe.Locks'`
- `bd where` in the default checkout
- `.beads/config.yaml` and `.beads/metadata.json` from orchestrate-situated-6329f1 worktree
