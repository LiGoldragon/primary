# Skill — autonomous agent

*How to act when no human is in the loop for routine obstacles.*

---

## Required reading before applying this skill

This skill assumes a baseline of workspace discipline. **Read
the following before treating any obstacle as routine,** and
re-read whenever the relevant kind of obstacle is in front of
you.

### Coordination — how the workspace shares state

- `~/primary/protocols/orchestration.md` — claim/release
  scopes, role lock files, BEADS coordination. Required
  before any file edit in shared workspace.
- `~/primary/skills/jj.md` — version-control discipline.
  Required before any commit or push. *Do not skim.* Notably:
  `jj describe @` is forbidden; the canonical form is `jj
  commit -m '<msg>'`. Reading the status output is part of
  the discipline, not optional.
- `~/primary/skills/repository-management.md` — creating
  GitHub repos, changing visibility, issues, PRs, the `ghq`
  layout. Required before any `gh` CLI use, repo creation,
  or local clone navigation.
- `~/primary/skills/reporting.md` — when to write a report
  vs. answer in chat; the always-name-paths rule;
  inline-summary rule for cross-references. Required before
  any substantive output.
- `~/primary/skills/skill-editor.md` — when editing skills
  (this one or any other). Required before skill edits.

### Design discipline — how to think before you write

- `~/primary/skills/beauty.md` — beauty as the criterion;
  ugliness as diagnostic reading. Required before deciding
  "this is done." Notably: if a name, structure, or shape
  feels ugly, slow down — the structure you're missing is
  exactly what the ugliness signals.
- `~/primary/skills/abstractions.md` — verb-belongs-to-noun.
  Required before writing any reusable verb (function or
  method). Notably: a free function is an incorrectly-
  specified verb; the rule forces you to find the noun the
  verb belongs to, and inventing that noun is often the
  load-bearing design step.
- `~/primary/skills/naming.md` — full English words; six
  narrow exceptions for short forms; no crate-name prefix on
  types. Required before naming any identifier.
- `~/primary/skills/micro-components.md` — one capability,
  one crate, one repo; component fits in one LLM context
  window; cross-crate deps via `git =`, never
  `path = "../"`. Required before adding a capability — the
  default is a new repo, not a new module in an existing
  crate.
- `~/primary/skills/push-not-pull.md` — producers push;
  consumers subscribe; polling is forbidden. Required before
  designing any producer-consumer interaction. Notably: when
  no push primitive exists, escalate — never fall back to a
  poll loop "for now."
- `~/primary/skills/contract-repo.md` — the wire contract
  between Rust components lives in a dedicated repo of typed
  records. Required before two Rust components signal each
  other across a process boundary.

### Language and tooling

- `~/primary/skills/rust-discipline.md` — methods on types,
  domain newtypes, one-object-in/out, errors as crate-owned
  enums, redb + rkyv discipline. Required before writing or
  reviewing Rust.
- `~/primary/skills/nix-discipline.md` — flake-input forms
  (default `github:`), no hand-edited `flake.lock`, no raw
  `/nix/store/...` paths, `nix run nixpkgs#<pkg>` for missing
  tools, `nix flake check` as canonical pre-commit runner.
  Required before editing any `flake.nix` or invoking a tool
  not on PATH.

These are not "read once at session start and forget" — they
are *checkpoint reads* before the kind of work each one
governs. If you're about to commit, re-look at jj.md's
"Before you commit" check. If you're about to write a report
that cites another report, re-look at the inline-summary
rule in reporting.md. If you're about to write a free
function, re-look at abstractions.md's "find the noun"
diagnostic. If you're about to grow a crate with a new
feature, re-look at micro-components.md's "default to a new
repo."

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
tools/orchestrate claim <role> <path> [more-paths] -- <reason>
```

`<role>` is one of `operator`, `designer`, `system-specialist`,
`poet`, `assistant`. The helper writes the role's own lock file,
reads every role's lock file, lists open BEADS tasks, and rejects
overlapping active scopes. If the work cannot proceed, create a
short BEADS task with the blocker and the next required action.

BEADS is never claimed. Do not claim `.beads/` before creating
or updating a task; any agent may write BEADS tasks at any time.
If `bd` reports a backend database-lock error, treat it as
transient storage contention, not ownership. Retry the BEADS
operation as the next natural action or continue with a clear
note if the task could not be recorded.

```
bd create "Short task title" -t task -p 2 -d "Blocked because ..."
```

Release the role scope as soon as the work is done:

```
tools/orchestrate release <role>
```

### Version-control obstacles

**When you finish a batch of changes, commit and push.** That's
the standing rule — blanket authorization, no asking required.
The full procedure (logical-commit grouping, the canonical
one-liner, the standard fixes for HTTPS push failure /
divergence / uncommitted state / repos missing `.jj/`) lives in
this workspace's `skills/jj.md`.

If a VCS obstacle blocks you and the jj skill
doesn't already name the fix, surface it instead of inventing
one — that's how the skill grows.

Do not leave role-owned work uncommitted. Before finishing,
run `jj status` in every repo or workspace area you changed.
Commit and push your own files, including role-owned reports
and coordination artifacts. If the working copy also contains
another agent's files, split your paths with the partial-commit
flow in `skills/jj.md` and leave the other agent's work alone.

### A design wants polling

Symptom: the next implementation step wants a sleep loop, a
periodic file reread, a retry timer for unknown state, or an
agent instruction to "check again later."

Fix: apply `skills/push-not-pull.md`. Producers push;
consumers subscribe. Build or wire the producer's subscription
primitive, defer the dependent feature, or escalate. Do not add
polling "for now"; the workspace treats polling as a design
failure unless it is one of the named carve-outs in
`skills/push-not-pull.md`.

### A required tool is missing from PATH

Symptom: `command not found` for `rustfmt`, `clippy`, `jq`, etc.

Fix: invoke via Nix without installing globally —

```
nix run nixpkgs#<package> -- <args>
```

Don't reach for `cargo install`, `pip install`, `npm install -g`,
or distro package managers. The setup is Nix-managed end-to-end;
out-of-Nix installs pollute and break reproducibility.

### A stateful or custom test command is becoming part of the work

Symptom: while debugging a feature, you keep running a long
command by hand — for example an ignored integration test, a
real-harness test, a WezTerm capture experiment, or a stateful
script that depends on local authentication.

Fix: turn the command into a named repo script and expose it
through the repo's flake.

Good pattern:

```
scripts/test-actual-thing
nix run .#test-actual-thing
```

The script may still run stateful commands such as `cargo test`
against the working tree. The point is not to force everything
into a pure derivation; the point is to document the command,
its environment variables, and its setup in versioned repo
files. Iteration becomes: edit the script, run the named Nix
command, inspect output, repeat.

If a one-off debug command teaches you something useful, either
keep the script with a clear `debug-*` name or fold it into the
real test script before finishing.

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
