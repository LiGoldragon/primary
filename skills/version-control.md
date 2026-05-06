# Skill — version control

*Always commit and push with `jj` when you're done making changes.
Push per logical commit, not in batch.*

---

## What this skill is for

Whenever you have made meaningful changes — even a one-line edit
that shipped — apply this skill before moving on. The discipline
is short:

1. Group the changes into logical commits.
2. Commit each group with a short verb-plus-scope message.
3. Push immediately, per commit, not in batch.

This applies to every tracked repo in the workspace. Don't ask
for permission to commit or push routine work; **the user has
granted blanket authorization for the standard flow**. Save the
asking for the listed exceptions at the end.

For the underlying CLI reference (`jj` commands, options, the
`@` model, undo, bookmarks), see lore's `jj/basic-usage.md`.
This skill is *how we use jj here*; lore is *how jj works*.

---

## The standard flow

In a clean working tree after an edit batch:

```sh
jj st                                                  # see what changed
jj diff                                                # confirm content
jj commit -m '<short verb + scope>'                    # finalise @, advance to fresh empty
jj bookmark set main -r @-                             # point main at the just-committed change
jj git push --bookmark main                            # publish
```

Or as the canonical one-liner:

```sh
jj commit -m '<msg>' && jj bookmark set main -r @- && jj git push --bookmark main
```

`-r @-` because `jj commit` advances `@` to a new empty change;
the commit you want to push is its parent.

If the message contains apostrophes, use double quotes
(`-m "<msg>"`). Apostrophes inside `'…'` terminate the shell
string.

---

## Logical commits

When the working tree contains more than one concern, **split
before committing**. A single commit captures one logical change;
unrelated edits go in their own commits.

The grouping criterion (in priority order):

1. **By concern.** A documentation update is one commit; a code
   change is another.
2. **By author.** If you and a peer agent both have uncommitted
   work in the tree (visible via the orchestration locks), commit
   only files in your scope; leave the other agent's files for
   them.
3. **By feature.** A multi-step feature lands as several commits,
   each one a coherent step that compiles, passes tests, and
   reads cleanly in the diff.

Don't fold unrelated edits into one "miscellaneous" commit.
"While I was here" cleanups go in their own commit with a clear
message.

---

## Commit message style

Single line. Short. A short verb plus scope, plus an optional
short clause naming the change. The repo is implicit (the commit
is in the repo). Detail lives in the diff and the report.

Examples:

- `Slot<T> migration`
- `report add 119`
- `reader for typed slots`
- `AGENTS commit-style shortened`

If a single change touches multiple repos, each repo gets its own
short commit.

---

## Always push

After every logical commit, **push immediately**. Blanket
authorization — proceed without asking.

Unpushed work is invisible to other machines and to anyone
consuming the repo as a flake input. Forgotten pushes cause
divergence and surprising forks. Don't batch pushes "to be
clean"; the standard cadence is one push per commit.

---

## Standard fixes for routine VCS obstacles

These problems have known answers in this workspace. When you
hit them, fix them and keep moving.

### A repo lacks `.jj/` (jj not initialised)

Symptom: `jj st` from inside a repo prints
`Error: There is no jj repo in "<path>"` even though `.git/`
exists.

Cause: the repo is git-only; jj isn't colocated. Li
repositories and forks are Git-backed colocated jj repos. Git
remains the remote/storage layer; `jj` is the working-history
interface.

Fix:

```sh
jj git init --colocate
```

Then proceed with the normal `jj` flow. Run from inside the
repo's working tree.

If the colocation fails or behaves strangely, fall back to
plain `git` for the immediate work and file a BEADS task
describing what didn't work — don't fight the tool.

### Push fails because the remote is HTTPS

Symptom: `git push` (or `jj git push`) returns
`fatal: could not read Username for 'https://github.com'`.

Cause: this workspace authenticates over SSH; HTTPS without a
credential helper is a misconfiguration.

Fix:

```sh
git -C <repo> remote set-url origin git@github.com:<owner>/<repo>.git
git -C <repo> push       # or: jj git push --bookmark main
```

This isn't a global config change — it's per-repo, repairs the
specific repo's remote, and matches the workspace standard. Do
it without asking.

### Push rejected — remote has commits you don't have

Symptom: `jj git push` (or `git push`) returns
`Updates were rejected because the remote contains work that
you do not have locally.`

Cause: another agent or another machine pushed in parallel.

Fix: fetch and integrate.

```sh
git fetch origin
# inspect the divergence:
git log --oneline --graph origin/main..HEAD
git log --oneline --graph HEAD..origin/main
```

If the remote's changes are a clean fast-forward over yours,
rebase your work onto theirs:

```sh
git rebase -X theirs origin/main           # if your local commits should win on conflict
# or:
git rebase origin/main                     # let conflicts surface for manual resolution
```

If conflicts surface (modify/delete or content), resolve in
favour of your scope's changes (per the orchestration lock); ask
only if the resolution genuinely changes the meaning of the
peer's work. After resolution: `git rebase --continue`, then
push.

### Working tree has uncommitted state when you expected clean

Symptom: `jj st` (or `git status`) shows new or modified files
that aren't yours.

Cause: prior work landed but wasn't committed. Either yours from
an earlier session, or a peer agent's that hasn't been pushed
yet.

Fix:

1. Inspect file by file: `jj st`, `jj diff <file>`.
2. If you can identify ownership (your work vs theirs), **commit
   only files in your lock scope** in logical groups; leave
   peer-owned files alone.
3. If ownership is ambiguous, file a BEADS task and ask before
   touching.

---

## Per-logical-commit pushes — not batch

Don't accumulate three commits and push at the end. Each commit
gets its own push. The cost is one extra `jj git push` per
commit; the benefit is that consumers see your work as it lands,
parallel agents fetch the latest tip on every iteration, and
recovery from a bad commit is `jj undo` rather than rolling back
multiple changes.

The exception: when one logical change spans several commits
that depend on each other (a refactor with three sequential
steps), push the whole sequence at the end of the sequence. But
each individual commit message still names the step, not the
sequence.

---

## When to ask anyway

Routine VCS obstacles are autonomy. The following are *not*
routine; ask first:

- **`git reset --hard` or anything that discards uncommitted
  work** that isn't clearly yours.
- **Force-push** to any branch — especially main.
- **Amending pushed commits** or rewriting public history.
- **Deleting branches** not in your scope.
- **Changing remote URLs** for reasons other than HTTPS→SSH on
  push failure.

---

## See also

- this workspace's `skills/autonomous-agent.md` — when to act on
  routine obstacles without asking; this skill is the VCS leaf
  it points at.
- this workspace's `skills/skill-editor.md` — every meaningful
  edit to a skill ends with the standard flow above.
- lore's `jj/basic-usage.md` — `jj` CLI reference (the `@`
  model, commit/describe distinction, undo, bookmarks).
- lore's `AGENTS.md` — the workspace contract; the VCS section
  there points at this skill.
