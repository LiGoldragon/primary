# Skill — autonomous agent

*How to act when no human is in the loop for routine obstacles.*

---

## What this skill is for

When you hit a known-solvable obstacle in the middle of work, you
solve it and continue. You do not stop and ask permission for
problems that have *standard solutions in this workspace*.
"Asking" produces friction; the friction produces stalling; the
stalling produces stale context.

The trade-off is sharp: you ask only when an action is
destructive, hard to reverse, significantly out of scope, or
operates on shared state outside what was asked of you.
Everything else, you do.

---

## Standard solutions

These problems have known answers in this workspace. When you
hit them, fix them and keep moving.

### Shared workspace work needs orchestration

Before editing files or running commands that create, modify,
format, or delete files, read and use this workspace's
`protocols/orchestration.md`.

The normal claim path is:

```
tools/orchestrate claim <operator|designer> <path> [more-paths] -- <reason>
```

The helper writes the role's own lock file, reads both lock
files, lists open BEADS tasks, and rejects overlapping active
scopes. If the work cannot proceed, create a short BEADS task
with the blocker and the next required action.

```
bd create "Short task title" -t task -p 2 -d "Blocked because ..."
```

Release the role scope as soon as the work is done:

```
tools/orchestrate release <operator|designer>
```

### A Li repo is not JJ-colocated

Li repositories and forks are Git-backed colocated Jujutsu
repositories. Git remains the remote/storage compatibility
layer; `jj` is the working history interface.

Symptom: a Li repo has `.git/` but no `.jj/`.

Fix, after claiming the repo in the orchestration protocol:

```
jj git init --colocate
```

Use `jj st`, `jj diff`, `jj commit`, `jj rebase`, `jj
cherry-pick`, and `jj git push` for normal repository work.
Use plain `git` for remote configuration or for tools that
need Git directly.

### Push fails because the remote is HTTPS

Symptom: `git push` returns
`fatal: could not read Username for 'https://github.com'`.

Cause: this workspace authenticates over SSH; HTTPS without a
credential helper is a misconfiguration.

Fix:

```
git -C <repo> remote set-url origin git@github.com:<owner>/<repo>.git
cd <repo> && jj git push --bookmark main
```

This isn't a global config change — it's per-repo, repairs the
specific repo's remote, and matches the workspace standard. Do
it without asking.

### A workspace has uncommitted state

Symptom: `jj st` shows new or modified files when you
expected a clean tree.

Cause: prior work landed but wasn't committed. Either yours or a
peer agent's.

Fix:

1. Inspect: `jj st`, `jj diff`, and file-level diffs for each
   changed path.
2. Group changes into **logical commits** — by concern, by
   author, or by feature. Don't fold unrelated changes into one
   commit.
3. Commit each group with a short verb-plus-scope message.
4. Move the bookmark and push with `jj git push`.

If the repo is in a coordination zone (e.g. with another agent
holding a lock on some files), commit only files in *your* lock
scope; leave the other agent's files for them. If the working
copy mixes your work with someone else's, split the change
before committing or leave the unrelated work untouched.

### A required tool is missing from PATH

Symptom: `command not found` for `rustfmt`, `clippy`, `jq`, etc.

Fix: invoke via Nix without installing globally —

```
nix run nixpkgs#<package> -- <args>
```

Don't reach for `cargo install`, `pip install`, `npm install -g`,
or distro package managers. The setup is Nix-managed end-to-end;
out-of-Nix installs pollute and break reproducibility.

### A change is meaningful but unpushed

After every meaningful commit in any tracked repo, push
immediately. **Blanket authorization** — proceed without asking.

```
jj commit -m '<msg>' && jj bookmark set main -r @- && jj git push --bookmark main
```

Unpushed work is invisible to other machines and to anyone
consuming the repo as an input.

### A doc references a removed/renamed thing

Symptom: a doc points at `OLD_NAME` or `removed/path.md`.

Fix: update the reference to the new home. Don't leave
half-broken text in place "for the user to clean up later." If
the new home doesn't exist, raise the question — don't paper
over.

### A repo has no `skills.md`, and you've just done substantive work in it

Symptom: you've spent meaningful time in a repo — read its
ARCHITECTURE.md, AGENTS.md, source, reports; understood its
role, invariants, and what it owns; landed a non-trivial change
— and `<repo-root>/skills.md` does not exist.

Fix: write the skill before finishing the task.

1. Check the workspace's `skills/skill-editor.md` for the
   canonical conventions (naming, location, format,
   cross-references). **Read it first**, even if you've written
   skills before — that file is where the conventions are
   refined over time, and following the same protocol keeps the
   skills consistent across the workspace.
2. Gather what you learned: this repo's project-specific intent,
   the invariants about how to work in it, what this repo is the
   canonical owner of and what it isn't, the neighboring repos
   whose skills are worth pointing at.
3. Write `skills.md` at the repo root, following the format from
   `skill-editor.md`.
4. Commit and push.

**What "substantive" means.** A 10-minute typo fix is not enough
context to write a good skill — you don't yet know what's
load-bearing in this repo vs incidental. A multi-step change
that required understanding the repo's role, reading its
ARCHITECTURE.md, and following its invariants — that's enough.
A skill written without that depth is worse than no skill,
because future agents will trust it.

If you're unsure whether your work was substantive enough,
err toward writing the skill — the next agent benefits, and a
thin-but-honest skill is still useful.

---

## When to ask anyway

Solving a routine obstacle is autonomy. The following are *not*
routine; ask first:

- **Destructive operations** that aren't pure undo: deleting
  branches not in your scope, dropping data, force-pushing,
  deleting files outside your stated work, removing dependencies.
- **Hard-to-reverse operations**: amending pushed commits,
  rewriting public history.
- **Out-of-scope cleanup**: "while I was here I noticed X is
  ugly — should I fix it?" — say so, don't just do it.
- **Shared state**: actions that affect other agents' or other
  humans' work-in-flight (visible in coordination locks, recent
  commits, or open PRs).
- **Large-scope assumptions**: when the task expands beyond
  what was asked of you. Surface the scope expansion; let the
  caller decide.

---

## Editing skill files — read skill-editor first

Whenever you edit, create, or refine a skill file (this one,
another workspace skill, or a repo's `skills.md`), **read
`~/primary/skills/skill-editor.md` first**. That file is the
canonical guide for naming, location, format, and
cross-references. The conventions get refined over time; reading
it each time keeps every skill on the same protocol.

This applies to:

- Creating a new repo's `skills.md` (per the
  no-skills-md-after-substantive-work rule above).
- Editing an existing skill file (this one, a sibling workspace
  skill, or a repo's skill).
- Refining the conventions themselves — if you find a new
  convention worth adding, add it to `skill-editor.md`, not as
  a one-off in the skill you happened to be editing.

---

## Skill-file cross-references

When this skill — or any skill — refers to another skill, name
the file by repo + filename. **Don't use full HTTPS URLs.** Deep
file URLs rot when files move; a repo-level reference stays
valid.

Right: `criome's skills.md`, this workspace's `skills/abstractions.md`, `lore's rust/ractor.md` (when the target is tool reference, not a skill).

Wrong: `https://github.com/<org>/<repo>/blob/main/skills.md`.

The reader knows: a repo-level skill is at the repo root,
`skills.md`. A workspace-level skill is at
`<workspace>/skills/<name>.md`. See this workspace's
`skills/skill-editor.md` for the full conventions.
