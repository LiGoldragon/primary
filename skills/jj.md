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

## `jj describe @` is forbidden for finalising new work

The canonical commit form is **`jj commit -m '<msg>'`** —
nothing else. **Never use `jj describe @ -m '<msg>'`** to
finalise new working-copy work, even though it is
functionally similar.

Why forbidden:

- `jj commit` is *named* a commit. It explicitly *advances
  `@` to a new empty child*. The next edit will go in a new
  commit; you can't accidentally pile more changes onto
  the just-described one.
- `jj describe @` is *named* "describe." It just sets a
  description on the current `@` without advancing. A
  follow-up edit lands in the same commit, growing it
  silently. Bookmark advancement (`-r @`) is also
  incidental — the bookmark moves to the same commit you
  just described, and jj's "became immutable, new commit
  created on top" warning papers over the non-canonical
  flow.
- The friction of `-r @-` (commit's bookmark form) is the
  discipline. The thought "wait, am I targeting the right
  commit?" is what surfaces "what's actually in this
  commit?" — which is the moment to remember to read
  `jj st`.

Allowed `describe` uses (narrow):

| Form | Use |
|---|---|
| `jj describe @- -m '<msg>'` | Edit description of an already-committed parent (typo fix, message update before push) |
| `jj describe <rev> -m '<msg>'` | Edit description of any earlier revision (rare) |

**Forbidden:**

| Form | Why |
|---|---|
| `jj describe @ -m '<msg>'` | This is the path that bundles peer files into your commit. Use `jj commit -m '<msg>'` instead. |
| `jj describe -m '<msg>'` (defaults to `@`) | Same — implicit `@` is forbidden. |

If you find yourself typing `jj describe`, stop and ask:
*am I editing an already-committed description, or am I
finalising new work?* If finalising new work — use
`jj commit`.

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
| `jj describe @-` | `jj describe @- -m '<msg>'` (only for editing already-committed descriptions; see §"`jj describe @` is forbidden") |
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

## Descriptionless commits are forbidden

`(no description set)` on a commit you authored is a
**workspace contract violation**, on equal footing with the
ban on raw `git` for daily commits. The 2026-05-12 117-orphan
incident (see `reports/designer/140-jj-discipline-after-
orphan-incident.md`) traced directly to this: an agent ran
`jj commit` without `-m`, the editor returned empty, the
commit succeeded with an empty description, no bookmark was
set, and the work became reachable only by op-log spelunking.

The structural fix lives in workspace `jj` config —
`ui.editor = "false"` so editor fallback aborts the operation.
**System-specialist:** land this config at the workspace
level so editor fallback fails loudly rather than writing
empty descriptions silently. Until that lands, this section
is the procedural backstop.

**Before every push**, run:

```sh
jj log -r 'main..@- & description(exact:"")'
```

If anything appears, fix it before pushing:

```sh
jj describe <rev> -m '<msg>'
```

**If `jj st` or any `jj log` output ever shows
`(no description set)` on a commit you authored**, stop and
describe it immediately — even before the next file edit.
The instant you continue past it, the next agent's view of
your work depends on you having set a description; their
`jj log` filters will hide it otherwise.

---

## Before you commit — the working-copy check

`jj commit` (and any other path that finalises `@`)
captures **every change in the working copy**, regardless of
who authored it. Run `jj st` before committing and read the
list of changed paths against your scope.

If `jj st` shows files outside your claim — a peer agent's
in-flight edit, a linter touch, anything not yours —
**don't commit the whole working copy.** Use `jj split` to
isolate your paths first (see below). A bare `jj commit`
bundles peer work into a commit with your authorship and your
message, leaving the peer's intent muddled in version control
history.

This check is procedural, not aesthetic. The recurring
failure mode is "I edited files X and Y; I run `jj commit`;
the working copy also contained Z (peer file or linter
output); the resulting commit covers X+Y+Z under my message."
Once pushed, fixing it requires either a force-push or a
follow-up commit that explains the muddle. Both are worse
than running `jj st` and `jj split` up front.

A pragmatic note: if you accidentally bundle a peer file
once, that's not catastrophic. The substance is intact;
the commit attribution is muddled but recoverable. Don't
spend extra command roundtrips guarding against rare
bundles. Read `jj st`'s output when it appears in any
preceding tool result — that's usually enough.

The default before any commit in a shared workspace:

```sh
jj st                                # what's actually here?
# if peers are present:
jj split -m '<my-msg>' <my-paths>    # isolate my scope
# if only mine:
jj commit -m '<my-msg>'              # canonical commit
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

### `jj restore` is hazardous mid-commit

`jj restore -f <rev>` reverts the working copy to match
`<rev>` without changing `@`'s position. It silently discards
any uncommitted changes in the working copy. Use sparingly;
**never** to "clean up before a commit" — that's what
`jj split` is for.

If you find yourself reaching for `jj restore` during normal
work, stop and check `jj st`; you probably want `jj split`
(to keep your paths and isolate peer paths) or `jj abandon @`
with deliberate intent. The 2026-05-12 117-orphan incident
included a `restore into commit …` op that was a load-bearing
step toward the failure — see `reports/designer/140-jj-
discipline-after-orphan-incident.md` §1.

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

## End-of-session check

Before ending a session — closing the conversation,
releasing a claim, handing off, or running `jj new main` /
`jj edit main` (which has the same effect as ending the
session in terms of moving `@` off the current chain) —
confirm every commit you authored is reachable from a
bookmark or from `main`. The check:

```sh
jj log -r 'main..@ ~ bookmarks()'
```

If the output is empty (or shows only the empty `@` working
copy), the session ends clean. If anything else appears,
those are **unbookmarked descendants of main** — pushable
work that no one but you can find. They are exactly the
shape of the 117-orphan failure (see
`reports/designer/140-jj-discipline-after-orphan-incident.md`).

Each row needs one of:

- **Land on main** — `jj bookmark set main -r <rev> && jj git push --bookmark main`.
- **Bookmark for review** — `jj bookmark create push-<topic> -r <rev> && jj git push --bookmark push-<topic>`.
- **Explicit abandon** — `jj abandon <rev>`, only if you
  genuinely want the work gone. Discarded work is the most
  expensive kind to recover; the bias is *always* toward
  bookmark-then-decide later.

Prefer landing on main when the work is yours and complete.
Reserve `push-<topic>` bookmarks for work that needs review
before landing — not as a default "stash so I can move on."
A long-lived chain of `push-*` bookmarks is itself a smell;
it usually means someone forgot to advance `main`.

---

## `jj git push -c @` is forbidden for routine commits

The form `jj git push --change @` (or `-c @`) creates an
auto-named `push-<change-id>` bookmark on the remote and pushes
the commit to it. It does **not** advance `main`. The bookmark
accumulates on the remote until someone manually deletes it.

**Use the standard flow instead** (per §"The standard flow").
The commit lands on `main`; no auto-named bookmark is created;
consumers see the work immediately.

Allowed `--change` uses, narrow:

- **Orphan recovery** — when an agent's prior work was
  abandoned and needs to be brought back onto a fresh `@`, per
  `reports/designer/140-jj-discipline-after-orphan-incident.md`
  §6.
- **Explicit "needs review before main"** — when the work
  genuinely needs review before landing. Use a descriptive
  bookmark name (`jj bookmark create push-<topic>`), not the
  auto-naming form. Descriptive names are findable on the
  remote and easy to delete after merge.

If you find yourself reaching for `-c @` in routine work, stop.
The standard flow is the discipline; the difference is one
extra command, not three.

The pattern compounds. Auto-named bookmarks accumulate on the
remote silently — there's no clean-up step. A workspace with 26
stray `push-*` bookmarks (as observed 2026-05-13, see
`reports/system-assistant/10-bookmark-divergence-forensic.md`)
is the direct consequence of treating `-c @` as routine.

---

## Bookmark cleanup after merge

When a `push-<topic>` bookmark's commit becomes an ancestor of
`main` (because the work merged), **delete the bookmark**.
Locally and on the remote:

```sh
jj bookmark delete push-<topic>
jj git push --deleted
```

(`--deleted` is its own mode; it can't be combined with
`--bookmark`. Run it on its own after the local delete; it pushes
every locally-deleted bookmark to the remote in one call.)

Long-lived `push-*` bookmarks are noise. They mislead
reviewers ("is this still in flight?"), they multiply the
surface area of `jj bookmark list`, and they grow forever if
no one prunes. The standard flow above (push directly to `main`)
avoids creating them in the first place; this rule cleans up the
ones that exist legitimately for review.

**End-of-session addition**: include `jj bookmark list` in the
session-end check. Any bookmark starting with `push-` whose
commit is already an ancestor of `main` should be deleted before
the session ends:

```sh
# list candidate bookmarks
jj bookmark list | awk '/^push-/ {print $1}'
# for each name, check ancestor status:
jj log -r '<commit>::main' --no-graph     # nonempty = ancestor = delete
```

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
