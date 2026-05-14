# Skill — feature development

*Working on a feature branch in a separate worktree so the main checkout
stays available for parallel work on `main`.*

---

## What this skill is for

When a feature spans more than one commit and one session — typical of
multi-step refactors, multi-repo arcs, or any work tracked by a
`feature` bead — the work lives on a non-`main` branch. **Don't check
out feature branches in the canonical ghq checkout.** That makes `main`
unavailable to peer agents (or to you in another session) until the
feature lands.

Instead, create a **separate worktree** for the feature branch at a
parallel path. The ghq checkout stays on `main`; the worktree is where
the feature work happens. Multiple agents and multiple feature branches
can coexist without ever competing for the same checkout.

---

## The path convention

| Path | Purpose |
|---|---|
| `/git/github.com/<owner>/<repo>/` | **Canonical ghq checkout.** Stays on `main`. Indexed by `ghq list`. Never checks out a feature branch. |
| `~/wt/github.com/<owner>/<repo>/<branch-name>/` | **Feature worktree.** Same repo, separate working copy, on the named branch. Lives under the user's home directory (writable without sudo). Not indexed by ghq. Created and removed per feature. |

`~/wt/` is the user-home worktree root — short prefix, parallel
structure to `/git/github.com/...` underneath so paths are predictable
and findable.

The branch name is the directory leaf — one feature branch per
worktree. A repo can host multiple worktrees simultaneously
(`~/wt/github.com/<owner>/<repo>/<feature-a>/` and
`~/wt/github.com/<owner>/<repo>/<feature-b>/`); each is independent.

---

## Creating a worktree

### For jj-colocated repos (the Li repo norm)

Most repos in this workspace are jj-colocated. Use `jj workspace add`
from inside the canonical ghq checkout:

```sh
mkdir -p ~/wt/github.com/<owner>/<repo>/
jj -R /git/github.com/<owner>/<repo> workspace add \
    ~/wt/github.com/<owner>/<repo>/<branch-name>
```

`jj workspace add` creates a new workspace at the given path that
shares the same operation log + bookmark space as the original. The
new workspace's `@` is independent — you can edit different commits
in the canonical checkout and the worktree without conflict.

After the workspace is created, point its `@` at the feature branch:

```sh
cd ~/wt/github.com/<owner>/<repo>/<branch-name>
jj edit <branch-name>
```

Or `jj new <branch-name>` to create a fresh empty change on top.

### For plain git repos (rare in this workspace)

If a repo lacks `.jj/`, fall back to `git worktree`:

```sh
mkdir -p ~/wt/github.com/<owner>/<repo>/
git -C /git/github.com/<owner>/<repo> worktree add \
    ~/wt/github.com/<owner>/<repo>/<branch-name> <branch-name>
```

After creation, run `jj git init --colocate` from inside the worktree
if jj operations are needed (per `~/primary/skills/jj.md` §"A repo lacks `.jj/`").

---

## Branch naming

Bare descriptive names — `horizon-re-engineering`, `pty-fanout`,
`mind-graph-redesign`. **Never `push-` prefixed.** The `push-`
convention in `~/primary/skills/jj.md` is for short-lived
review-cycle bookmarks; long-lived feature arcs are a different
shape.

The same branch name is used across every repo the feature touches —
so a multi-repo feature ends up with `horizon-re-engineering` branches
in `horizon-rs`, `lojix`, `signal-lojix`, `CriomOS`, `CriomOS-home`,
and `goldragon`, and matching worktrees at the parallel `/wt/...`
paths.

The feature bead's description carries the branch name explicitly
(per `~/primary/skills/beads.md` §"Feature beads carry their branch
name") so any agent picking up the bead lands on the right branches.

---

## Working in a worktree

The worktree is a normal jj working copy. All standard discipline
applies:

- `~/primary/skills/jj.md` — commit/push flow, descriptionless-commits
  ban, peer-file split, end-of-session check.
- The same `tools/orchestrate claim` rules — claim per-path edits
  before starting a session.
- Reports go in `~/primary/reports/<role>/` (workspace-level), not in
  the worktree.

The push surface is the same as the canonical checkout — `jj git push`
goes to the same remote. Pushing the feature branch:

```sh
jj bookmark set <branch-name> -r @-
jj git push --bookmark <branch-name>
```

(With `--allow-new` on the first push of a new bookmark.)

---

## Cleaning up a worktree

When the feature lands and the branch merges to `main`, **delete the
worktree** before deleting the branch.

For jj workspaces:

```sh
jj -R /git/github.com/<owner>/<repo> workspace forget \
    --workspace <branch-name>
rm -rf ~/wt/github.com/<owner>/<repo>/<branch-name>
```

For git worktrees:

```sh
git -C /git/github.com/<owner>/<repo> worktree remove \
    ~/wt/github.com/<owner>/<repo>/<branch-name>
```

Then delete the branch per `~/primary/skills/jj.md` §"Bookmark cleanup
after merge":

```sh
jj -R /git/github.com/<owner>/<repo> bookmark delete <branch-name>
jj -R /git/github.com/<owner>/<repo> git push --deleted
```

Long-lived `/wt/` directories that no longer correspond to active
feature beads are smell — they accumulate and confuse the next agent
about what's in flight. Clean up at merge time.

---

## When NOT to use a worktree

- **Single-commit fixes that land on `main`.** A `task` bead's small
  edit doesn't need a worktree; just commit on the ghq checkout's
  `@`. The feature-branch discipline is for work that spans more than
  one commit.
- **Read-only inspection.** No need to create a worktree to read code
  that exists on `main`.
- **One-off experiments that won't ship.** Use `jj new` on the ghq
  checkout, abandon if the experiment doesn't pan out.

The trigger for this skill is *"this work needs its own branch."* If
the work is going straight to main, no worktree.

---

## Why a worktree, not just a branch

A branch alone (without a worktree) means whoever is currently checked
out in the canonical ghq location can't switch to `main` without
losing their working state. Two agents (or two sessions) end up
fighting over what `git checkout` should be at `/git/.../<repo>/`.

Worktrees avoid this entirely: the canonical checkout stays on
`main`, agents who need that read it freely. The feature worktree is
a separate working copy — independent state, independent `@`, same
underlying repo. Multiple worktrees means multiple agents can work
multiple features in parallel without competing for one checkout.

This matches the workspace's broader push-not-poll discipline (per
`~/primary/skills/push-not-pull.md`): coordination is structural, not
serialized through one shared mutable thing.

---

## Interaction with the orchestration protocol

A worktree's path is its own scope for `tools/orchestrate claim`.
When you start work in a worktree, claim its path:

```sh
tools/orchestrate claim system-assistant '[primary-XXX]' \
    ~/wt/github.com/<owner>/<repo>/<branch-name> -- '<reason>'
```

Distinct from the canonical checkout's path — two scopes, no overlap.
Multiple agents can hold claims on different worktrees of the same
underlying repo simultaneously; they only conflict if both claim the
same worktree path.

The bead-side discipline (per `~/primary/skills/beads.md` §"Feature
beads carry their branch name") plus this worktree path discipline
gives a complete coordination story for multi-agent feature work:
the bead names the branch; the branch lives in worktrees at
predictable paths; agents claim worktrees individually.

---

## See also

- `~/primary/skills/jj.md` — version-control discipline; the standard
  flow for commits and pushes inside a worktree.
- `~/primary/skills/beads.md` §"Feature beads carry their branch
  name" — the upstream discipline that names the branch in the bead.
- `~/primary/protocols/orchestration.md` — claim flow; worktree
  paths are scope-claimable.
- `~/primary/skills/repository-management.md` — the ghq-managed
  canonical checkout layout this skill parallels.
