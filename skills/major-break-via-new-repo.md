# Skill — major-break-via-new-repo

*When an architectural break is large enough that the existing repo's invariants no longer fit, create a new repository with a `-next` / `-v2` / longer descriptive suffix and develop in parallel. After the break stabilizes, rename to the canonical short name (replacing the original). Per psyche 2026-05-26.*

## What this skill is for

Most architectural changes belong on a **feature branch in a worktree**
under the existing repo (per `feature-development.md`). This skill names
the EXCEPTION: when the architectural break is large enough that the
existing repo's invariants — its `ARCHITECTURE.md`, its types, its
tests, its repo `INTENT.md` — no longer fit the new shape.

In that case, the cost of holding two competing architectures inside
one repo (branch state drift, agent confusion about which file is
canonical, accidental cross-contamination) exceeds the cost of a fresh
repo. The fresh repo lets the new architecture develop in parallel
without disrupting production work on the old one.

Use this skill when the trigger fires (see below). Otherwise, default
to feature branches.

## The trigger

A **major architectural break** — not a refactor, not a new feature, not
even a substantial reorganization. The signs:

- The repo's `ARCHITECTURE.md` would need to be rewritten from scratch
  (not edited) to describe the new shape.
- The repo's `INTENT.md` carries invariants the new direction
  contradicts (e.g. "six-position schema with Features section" when
  the new direction is "root struct with positional sub-fields").
- A meaningful number of existing tests assert the OLD shape and would
  need to be deleted or inverted to rejection-tests (this is a smell
  that the repo IS the old shape).
- Agents repeatedly read the existing repo's guidance, conclude the
  old shape is canonical, and wire new work through old surfaces.
- Multiple parallel feature branches accumulate, each carrying drift,
  with no clear path to integration.

One or two of these can survive on a branch; three or more is the
trigger to consider this skill.

The opposite signal — **don't** apply this skill — when:

- The change is a refactor, even a large one (the invariants stay).
- The change is additive (new types alongside old types in the same
  scope).
- The change is a rename without semantic drift.
- The change is bounded to one or two files.
- Operator can integrate the change into `main` in one or two slices.

## The naming convention

The new repo's name carries a suffix that signals prototype /
breakthrough status:

| Suffix | When to use |
|---|---|
| `-next` | The new shape that is expected to replace the old one. Implies an eventual rename to the canonical short name. |
| `-v2` | When the old version is expected to keep living (some workspaces support both major versions) — rarer; the workspace's default direction is supersession via rename. |
| longer descriptive suffix | When the break is exploratory and not yet expected to converge on a single canonical name. E.g. `nota-structural-library`, `schema-derived-nota`. |

Per psyche 2026-05-26: the longer name **signals prototype status**.
Agents picking up a `<name>-next` repo know they're working on the
breakthrough version, not the production version.

## Workflow

### Step 1 — Decide whether the trigger fires

If you're uncertain, ask the psyche. Per `intent-clarification.md`:
when intent on a question is unclear, ask. The decision to create a
new repo is significant — it touches the workspace's repo-name surface
which agents read on every session.

If the psyche has explicitly authorized the break (intent record naming
the new repo or the methodology), proceed.

### Step 2 — Create the new repo

Use `gh repo create` with a description that names the relationship to
the old repo:

```sh
gh repo create LiGoldragon/<name>-next --public \
  --description "<purpose> — successor to <old-name>"
```

The description is the agent-facing breadcrumb back to the old repo.
Future agents reading `gh repo view <name>-next` learn the provenance
without needing a separate report.

### Step 3 — Choose: fork or start fresh

Two valid approaches:

| Approach | When to use |
|---|---|
| **Fork** (start from old repo's commit history) | When meaningful substrate carries forward — types, tests, ARCHITECTURE bones, file structure. Cheaper to delete than to rewrite. |
| **Start fresh** (initial scaffold from scratch) | When the break is deep enough that the old substrate is more confusion than help. The canonical workspace file set (`README.md`, `ARCHITECTURE.md`, `INTENT.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `flake.nix`, `rust-toolchain.toml`, `Cargo.toml`, `src/lib.rs`) lands as an initial commit. |

The fork choice is reversible (rewrite history later) but the
"started fresh" cleanliness is harder to recover after grafting old
code. Default to fresh unless the substrate cost is clearly large.

### Step 4 — Scaffold the canonical workspace file set

Every workspace repo carries this set (or the subset relevant to its
language/runtime):

- `README.md` — short intro + provenance pointer back to the predecessor
- `ARCHITECTURE.md` — repo shape per `architecture-editor.md`
- `INTENT.md` — per-repo intent synthesis per `repo-intent.md` (psyche
  intent in italics; verbatim quotes; no embellishment)
- `AGENTS.md` — pointer to workspace `AGENTS.md` (`@~/primary/AGENTS.md`
  if this repo sits next to primary; otherwise the explicit path)
- `CLAUDE.md` — `You MUST read AGENTS.md.`
- `.gitignore` — language-specific (Rust: `/target` + `/result` for Nix)
- `flake.nix` — Nix-flake setup matching the workspace standard
- `rust-toolchain.toml` — pinned toolchain (workspace default 1.85.0)
- `Cargo.toml` — lib/bin crate setup
- `src/lib.rs` — placeholder module-level documentation pointing at
  the contract (per `component-triad.md` if applicable)

### Step 5 — Develop in parallel

The new repo gets its own worktrees, feature branches, and operator
sessions. Production work continues on the OLD repo unchanged. Agents
reaching the workspace see TWO repos side-by-side:

- The old repo on `main` — production. Don't disrupt.
- The new repo on `main` — prototype evolving toward replacement.

Per `component-triad.md`: if the new repo IS a daemon, it has a triad
shape (`<name>-next` daemon + `signal-<name>-next` working signal +
`core-signal-<name>-next` policy signal — or, more commonly, just
the daemon repo first because contracts live in the existing signal
repos until the daemon's contract surface settles).

### Step 6 — Cross-reference

The old repo's `README.md` or `ARCHITECTURE.md` gets a note pointing
to the new repo: "Successor under development at
`github:<owner>/<name>-next` — see that repo's `INTENT.md` for the
direction."

The new repo's `README.md` notes the predecessor: "Successor to
`<old-name>` per psyche YYYY-MM-DD (intent record N)."

This pairing keeps agents from accidentally treating the prototype
as the production repo or vice versa.

### Step 7 — When stable, rename to canonical short name

After the new architecture has proven itself (per psyche authorization
or operator-led migration):

- Migrate any remaining consumers off the old repo to the new one.
- Archive or delete the old repo (psyche authority — these are
  significant decisions; don't act unilaterally).
- Rename the new repo from `<name>-next` to `<name>` (replacing the
  original name). `gh repo rename` handles this; downstream
  references (cargo deps, flake inputs) need updates per the
  workspace's repo-management practice.

The longer descriptive suffix is meant to be **temporary**. Once the
break is canonical, the canonical name is shorter and clearer.

## When NOT to apply this skill

The default for most work is feature-development.md (feature branches
in worktrees under existing repos). Do NOT create a new repo for:

- A bug fix.
- A new feature that fits the existing architecture.
- A rename without semantic change.
- A refactor (even a substantial one) that keeps the repo's invariants.
- An additive change (new types alongside existing types).
- Multi-step work that can land in 2-4 slices on `main`.

The cost of a new repo is real: it adds to the workspace's repo-name
surface that every agent reads; it splits agents' attention between
the old and new shapes; it creates a migration burden when the new
repo eventually replaces the old.

Apply this skill only when the break is genuinely major and the cost
of NOT having a fresh repo (drift, agent confusion, accumulated
contradictions) exceeds the cost of having one.

## See also

- this workspace's `skills/feature-development.md` — the default
  branching pattern (worktrees under existing repos).
- this workspace's `skills/component-triad.md` — the daemon + working
  signal + policy signal shape for stateful components.
- this workspace's `skills/repo-intent.md` — how to author the new
  repo's `INTENT.md`.
- this workspace's `skills/architecture-editor.md` — how to author
  the new repo's `ARCHITECTURE.md`.
- this workspace's `skills/intent-clarification.md` — ask the psyche
  when the trigger is unclear.
- this workspace's `AGENTS.md` hard overrides — "designers work on
  feature branches in `~/wt`; operators own main + rebase" applies
  inside both old and new repos.
