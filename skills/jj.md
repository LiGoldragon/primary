# Skill — jj

*Version control in this workspace is `jj`. Commit and push
through `jj` after every meaningful change. Raw `git` is
forbidden as a daily-commit tool; it survives only as an
explicit escape hatch for two named remote-config cases
below.*

---

## What this skill is for

Whenever you have made meaningful changes — even a one-line
edit that shipped — apply this skill before moving on. The
discipline is short:

1. Group the changes into logical commits.
2. Commit each group with a short verb-plus-scope message.
3. Push immediately, per commit, not in batch.

This applies to every tracked repo in the workspace. Don't
ask for permission to commit or push routine work; **the
user has granted blanket authorization for the standard
flow**. Save the asking for the listed exceptions at the
end.

The tool is **`jj` (Jujutsu)**. Every Li repo is a
Git-backed colocated jj repository — the working-history
interface is `jj`; Git remains the remote/storage layer. If
a repo lacks `.jj/`, run `jj git init --colocate` (see
"Standard fixes" below).

For the underlying CLI reference (`jj` commands, options,
the `@` model, undo, bookmarks), see lore's
`jj/basic-usage.md`. This skill is *how we use jj here*;
lore is *how jj works*.

---

## Raw `git` is forbidden for daily commits

The default tool for **every commit** is `jj`. **Don't
reach for `git add` / `git commit` / `git push` / `git
checkout` for normal work.** When a partial commit feels
hard, the answer is to learn the jj idiom for it (see
"Partial commits" below), not to drop down to `git`.

`git` survives in this workspace as an explicit escape
hatch for **two named cases**:

1. **Per-repo HTTPS → SSH remote fix** (one-time config
   repair when push fails on a fresh clone).
2. **Manual divergence resolution** when two peers pushed
   in parallel and `jj git push` rejects.

Both are detailed under "Standard fixes" below. Anything
else — daily commits, partial commits, branch motion,
amending, undo — uses `jj`.

If you find yourself reaching for raw `git` outside the two
named cases, stop. Either find the jj equivalent or
escalate (per `skills/autonomous-agent.md`) — don't paper
over the unfamiliarity by dropping to git.

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

`-r @-` because `jj commit` advances `@` to a new empty
change; the commit you want to push is its parent.

If the message contains apostrophes, use double quotes
(`-m "<msg>"`). Apostrophes inside `'…'` terminate the
shell string.

---

## Never let jj open an editor

Every jj command that takes a description has an inline
flag. **Always use it.** An agent that lets jj fall back to
`$EDITOR` blocks the session on a no-op editor invocation,
or worse, leaves a half-described commit when the editor
exits without saving.

| Command | Inline form |
|---|---|
| `jj commit` | `jj commit -m '<msg>'` |
| `jj describe` | `jj describe -m '<msg>'` |
| `jj describe @-` | `jj describe @- -m '<msg>'` |
| `jj split <paths>` | `jj split -m '<msg>' <paths>` |
| `jj split -i` | `jj split -i -m '<msg>'` |
| `jj squash --into <rev>` | `jj squash --into <rev> --use-destination-message` |
| `jj new` | `jj new -m '<msg>'` |
| `jj duplicate <rev>` | not editor-bound; safe |
| `jj rebase` | safe unless conflicts surface |

The deeper rule: **if a jj command would prompt for text
without a flag, find the flag.** The flags exist on every
description-taking command. The `-m '<msg>'` form is the
canonical workspace shape.

Two compound idioms worth knowing:

- **`jj split -m '<msg>' <paths>`** — first commit gets the
  description; the working copy (second commit) inherits
  empty. After the split, the working copy can be
  re-described later if needed.
- **`jj squash --into <rev> --use-destination-message`** —
  keeps the destination's existing description without
  prompt. Use when amending into an already-described
  commit.

If you find yourself reaching for `EDITOR=true`,
`GIT_EDITOR=true`, or any other no-op-editor environment
shim, **stop**. The right answer is the inline `-m` flag on
the command being run. Editor shims are anti-patterns —
they hide the fact that the wrong invocation form was
used.

---

## Before you describe — the working-copy check

`jj describe` (or any commit-equivalent that finalises `@`)
captures **every change in the working copy**, regardless of
who authored it. Run `jj st` before describing and read the
list of changed paths against your scope.

If `jj st` shows files outside your claim — a peer agent's
in-flight edit, a linter touch, anything not yours — **do
not describe**. Use `jj split` to isolate your paths first
(see below). The bare `describe` will bundle peer work into
a commit with your authorship and your message, leaving the
peer's intent muddled in version control history.

This check is procedural, not aesthetic. The recurring
failure mode is "I edited files X and Y; I run `jj describe`;
the working copy also contained Z (peer file or linter
output); the resulting commit covers X+Y+Z under my message."
Once pushed, fixing it requires either a force-push or a
follow-up commit that explains the muddle. Both are worse
than running `jj st` and `jj split` up front.

The default before any describe in a shared workspace:

```sh
jj st                                # what's actually here?
# if peers are present:
jj split -m '<my-msg>' <my-paths>    # isolate my scope
# if only mine:
jj describe -m '<my-msg>'            # bundled commit
```

When in doubt — split.

---

## Partial commits — `jj split` with paths

When the working tree contains both your changes and a peer
agent's uncommitted work (visible via the orchestration
locks), commit only files in your scope. `jj split` is the
right tool — and `git add <paths>` is **not** the workspace
shape, even though both produce the same end-state.

Canonical idiom for committing a subset of paths:

```sh
jj split -m '<short verb + scope>' <my-path-1> <my-path-2> ...
jj bookmark set main -r @-
jj git push --bookmark main
```

`-m` sets the description for the **first** commit (the one
containing the selected paths) inline — **no editor
opens**. The remaining paths stay in the working copy `@`
(which inherits an empty description) for the peer agent to
pick up later.

For interactive selection of changes (rather than whole
paths), use `jj split -i` — opens the diff editor for change
selection. Even with `-i`, pass `-m` to set the description
inline and avoid the second editor prompt.

---

## Logical commits

When the working tree contains more than one concern, **split
before committing**. A single commit captures one logical
change; unrelated edits go in their own commits.

The grouping criterion (in priority order):

1. **By concern.** A documentation update is one commit; a
   code change is another.
2. **By author.** If you and a peer agent both have
   uncommitted work in the tree (visible via the
   orchestration locks), commit only files in your scope;
   leave the other agent's files for them. Use `jj split`
   per the partial-commits idiom above.
3. **By feature.** A multi-step feature lands as several
   commits, each one a coherent step that compiles, passes
   tests, and reads cleanly in the diff.

Don't fold unrelated edits into one "miscellaneous" commit.
"While I was here" cleanups go in their own commit with a
clear message.

---

## Commit message style

Single line. Short. A short verb plus scope, plus an
optional short clause naming the change. The repo is
implicit (the commit is in the repo). Detail lives in the
diff and the report.

Examples:

- `Slot<T> migration`
- `report add 119`
- `reader for typed slots`
- `AGENTS commit-style shortened`

If a single change touches multiple repos, each repo gets
its own short commit.

---

## Always push

After every logical commit, **push immediately**. Blanket
authorization — proceed without asking.

Unpushed work is invisible to other machines and to anyone
consuming the repo as a flake input. Forgotten pushes cause
divergence and surprising forks. Don't batch pushes "to be
clean"; the standard cadence is one push per commit.

---

## Standard fixes for routine obstacles

These problems have known answers in this workspace. When
you hit them, fix them and keep moving.

### A repo lacks `.jj/` (jj not initialised)

Symptom: `jj st` from inside a repo prints
`Error: There is no jj repo in "<path>"` even though `.git/`
exists.

Cause: the repo is git-only; jj isn't colocated. Li
repositories and forks are Git-backed colocated jj repos.
Git remains the remote/storage layer; `jj` is the
working-history interface.

Fix:

```sh
jj git init --colocate
```

Then proceed with the normal `jj` flow. Run from inside the
repo's working tree.

### Push fails because the remote is HTTPS — *named git escape hatch*

Symptom: `jj git push` returns
`fatal: could not read Username for 'https://github.com'`.

Cause: this workspace authenticates over SSH; HTTPS without
a credential helper is a misconfiguration.

Fix (per-repo, one-time config repair):

```sh
git -C <repo> remote set-url origin git@github.com:<owner>/<repo>.git
jj git push --bookmark main
```

This is one of the **two named escape-hatch cases for raw
`git`** in this workspace. The fix touches only the remote
URL config — once. After it lands, the normal `jj` flow
resumes.

### Push rejected — remote has commits you don't have — *named git escape hatch*

Symptom: `jj git push` returns
`Updates were rejected because the remote contains work
that you do not have locally.`

Cause: another agent or another machine pushed in parallel.

Fix: fetch and integrate. This is the **second named
escape-hatch case for raw `git`** — divergence resolution
uses `git fetch` + `git rebase` because the workflow is
mature there:

```sh
git fetch origin
git log --oneline --graph origin/main..HEAD
git log --oneline --graph HEAD..origin/main
```

If the remote's changes are a clean fast-forward over
yours, rebase your work onto theirs:

```sh
git rebase -X theirs origin/main           # your local commits win on conflict
# or:
git rebase origin/main                     # let conflicts surface for manual resolution
```

If conflicts surface (modify/delete or content), resolve in
favour of your scope's changes (per the orchestration
lock); ask only if the resolution genuinely changes the
meaning of the peer's work. After resolution:
`git rebase --continue`, then `jj git push --bookmark main`.

After this case completes, the normal `jj` flow resumes.

### Working tree has uncommitted state when you expected clean

Symptom: `jj st` shows new or modified files that aren't
yours.

Cause: prior work landed but wasn't committed. Either yours
from an earlier session, or a peer agent's that hasn't been
pushed yet.

Fix:

1. Inspect file by file: `jj st`, `jj diff <file>`.
2. If you can identify ownership (your work vs theirs),
   **commit only files in your lock scope** in logical
   groups using `jj split` (see "Partial commits" above);
   leave peer-owned files alone.
3. If ownership is ambiguous, file a BEADS task and ask
   before touching.

---

## Per-logical-commit pushes — not batch

Don't accumulate three commits and push at the end. Each
commit gets its own push. The cost is one extra
`jj git push` per commit; the benefit is that consumers see
your work as it lands, parallel agents fetch the latest tip
on every iteration, and recovery from a bad commit is
`jj undo` rather than rolling back multiple changes.

The exception: when one logical change spans several
commits that depend on each other (a refactor with three
sequential steps), push the whole sequence at the end of
the sequence. But each individual commit message still
names the step, not the sequence.

---

## When to ask anyway

Routine obstacles are autonomy. The following are *not*
routine; ask first:

- **`git reset --hard` or anything that discards
  uncommitted work** that isn't clearly yours.
- **Force-push** to any branch — especially main.
- **Amending pushed commits** or rewriting public history.
- **Deleting branches** not in your scope.
- **Changing remote URLs** for reasons other than HTTPS→SSH
  on push failure.
- **Reaching for raw `git`** outside the two named
  escape-hatch cases above.

---

## See also

- this workspace's `skills/autonomous-agent.md` — when to
  act on routine obstacles without asking; this skill is
  the VCS leaf it points at.
- this workspace's `skills/skill-editor.md` — every
  meaningful edit to a skill ends with the standard flow
  above.
- lore's `jj/basic-usage.md` — `jj` CLI reference (the `@`
  model, commit/describe distinction, undo, bookmarks).
- lore's `AGENTS.md` — the workspace contract; the VCS
  section there points at this skill.
