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

### Push fails because the remote is HTTPS

Symptom: `git push` returns
`fatal: could not read Username for 'https://github.com'`.

Cause: this workspace authenticates over SSH; HTTPS without a
credential helper is a misconfiguration.

Fix:

```
git -C <repo> remote set-url origin git@github.com:<owner>/<repo>.git
git -C <repo> push
```

This isn't a global config change — it's per-repo, repairs the
specific repo's remote, and matches the workspace standard. Do
it without asking.

### A workspace has uncommitted state

Symptom: `git status` shows new or modified files when you
expected a clean tree.

Cause: prior work landed but wasn't committed. Either yours or a
peer agent's.

Fix:

1. Inspect: `git status`, `git diff <file>` for each.
2. Group changes into **logical commits** — by concern, by
   author, or by feature. Don't fold unrelated changes into one
   commit.
3. Commit each group with a short verb-plus-scope message.
4. Push.

If the repo is in a coordination zone (e.g. with another agent
holding a lock on some files), commit only files in *your* lock
scope; leave the other agent's files for them.

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
git push                    # plain git
jj git push --bookmark main # jj
```

Unpushed work is invisible to other machines and to anyone
consuming the repo as an input.

### A doc references a removed/renamed thing

Symptom: a doc points at `OLD_NAME` or `removed/path.md`.

Fix: update the reference to the new home. Don't leave
half-broken text in place "for the user to clean up later." If
the new home doesn't exist, raise the question — don't paper
over.

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

## Skill-file cross-references

When this skill — or any skill — refers to another skill, name
the file by repo + filename. **Don't use full HTTPS URLs.** Deep
file URLs rot when files move; a repo-level reference stays
valid.

Right: `criome's skills.md`, `lore's programming/abstractions.md`.

Wrong: `https://github.com/<org>/<repo>/blob/main/skills.md`.

The reader knows: a repo-level skill is at the repo root,
`skills.md`. A workspace-level skill is at
`<workspace>/skills/<name>.md`. See this workspace's
`skills/skill-editor.md` for the full conventions.
