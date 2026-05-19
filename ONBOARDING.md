# Primary Workspace — Onboarding

Read this once when beginning a new session or role. Companion to
`AGENTS.md` (compact, every-session) and `ESSENCE.md` (intent,
upstream of everything). This file holds the broader context — file
map, longer-form discipline, and rationale — that fresh agents need
once. Specialised agents working in a focused scope don't have to
re-read every session; designers and general-purpose agents should
read it on starting.

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace essence — most universal psyche intent. |
| `AGENTS.md` | Compact every-keystroke rules. |
| `ONBOARDING.md` | This file. |
| `intent/` | Workspace log of psyche statements. |
| `<repo>/INTENT.md` | Per-repo synthesis of psyche intent. |
| `orchestrate/AGENTS.md` | Role-coordination protocol. |
| `protocols/active-repositories.md` | Current active repo map for architecture sweeps. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `skills/skills.nota` | Typed skill index (name, path, kind, tier, description). |
| `reports/<role>/` | Role-owned reports. Each role writes only into its own subdirectory. Exempt from claim flow. |
| `orchestrate/<lane>.lock` | Per-lane coordination state file. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Transitional. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Broad recent checkout index. |
| `GOALS.md` | Standing high-level goals. |

## Skill discovery — query the index, don't scan the directory

`skills/skills.nota` is the typed index. Entries carry:

- `name` — kebab-case identifier
- `path` — relative path to the skill file
- `kind` — `role` / `architecture` / `craft` / `programming` / `workflow` / `meta`
- `tier` — 1 (apex) to 4 (consulted-when-the-topic-comes-up)
- `description` — one line that lets an agent decide whether to read

When a topic comes up, query the index for the kind and read the
matching skill(s). Don't read every skill — read what the moment
demands.

## Reports are for agents; chat is for the user

The full discipline lives in `skills/reporting.md`. Summary of the
load-bearing rules:

- Substantive output (explanation, proposal, analysis, audit,
  synthesis) goes in `reports/<role>/<N>-<topic>-<date>.md`.
- The chat names the report path and carries user-attention items
  inline — open questions, blockers, recommendations awaiting
  approval. Each is stated so the user can engage without opening the
  report.
- A chat reply is never *just* a pointer when the user has something
  to attend to.
- Opaque IDs, section numbers, or "see report N" without inline
  substance is a discipline violation.

Whenever an agent creates, edits, supersedes, or deletes a report,
the chat reply names every affected path.

## Nix store search — the longer version

The Nix store is not a workspace search surface. Running `rg`, `grep`,
`find`, `fd`, broad globs, or recursive `ls` against `/nix/store` is
forbidden. Reasons: the store grows unbounded; full-text search
across it exhausts memory; the matches are usually noise (dependency
trees, not source).

When looking for Nix-controlled information, use Nix:

- Source checkout (the repo, not the store).
- `nix eval` against an attribute path.
- `nix flake show` / `nix flake metadata`.
- `nix path-info` for a specific derivation output.
- A targeted check/test/passthru derivation that exposes the value.

If a value cannot be reached this way, change the Nix code to expose
it as an evaluable option, package, check, passthru, or helper output.

## No harness-dependent memory — the longer version

Memory and persistent agent state must live in workspace files every
agent can open — `skills/`, `repos/lore/`, `reports/`, `protocols/`,
repo `skills.md`, repo `ARCHITECTURE.md`, or `.beads/` while bd is the
active substrate.

**Don't** use harness-dependent memory systems — e.g. Claude Code's
per-session memory files at `~/.claude/projects/<workspace>/memory/`,
or any agent-private state store an outside agent cannot read.

**Why**: memory tied to one harness is invisible to every other
harness and to the human. The workspace's truth must live in files
every agent can open. If you learn something durable, write it to the
right workspace file; never to harness-private state.

## BEADS is transitional

`.beads/` exists today for convenience. The destination is **Persona's
native typed work graph** in `signal-persona-mind` / `persona-mind`.
The work graph is part of Persona's central mind state, not a separate
component. Don't build a Persona↔bd bridge; don't deepen the bd
investment. Use bd for short-tracked-item coordination while the
native mind graph is being implemented; design new shapes assuming bd
goes away.

BEADS is never an ownership lock. Do not claim `.beads/`. Any agent
may create, update, comment on, or close BEADS tasks at any time. If
the current backend reports a database lock, that is storage-engine
contention, not coordination ownership.

## Feature branches in worktrees — when and how

When work touches code that is already in production (the deploy
stack, the OS layer, anything users depend on right now) and the arc
spans more than one commit, the work belongs on a feature branch in
a separate worktree.

Worktree path:
`~/wt/github.com/<owner>/<repo>/<branch-name>/` — parallel-and-
predictable, same shape as the ghq layout under `/git/...`. The same
branch name is used across every repo a multi-repo arc touches.

The full discipline — when to use a worktree, how to create one
(jj-colocated and plain-git forms), branch naming, push flow, cleanup
at merge time, and the orchestration-protocol interaction — lives in
`skills/feature-development.md`. Read that skill before starting any
non-trivial branch work.

## Two deploy stacks — the longer version

**Production today** runs the old monolithic `lojix-cli` stack on
`main` branches in the canonical `/git/...` checkouts: `horizon-rs`,
`lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `goldragon`. If
you need to fix something that is live on a node right now, the fix
goes on `main` in those checkouts.

**The lean rewrite** — new `lojix` daemon + thin `lojix` CLI client +
lean horizon proposal/view + pan-horizon config — lives on
`horizon-leaner-shape` branches in worktrees under `~/wt/...`, plus
two new repos: `lojix` and `criomos-horizon-config`. It has smoke-
built `zeus` end-to-end through `prometheus` but has not been cut
over. No node in the cluster runs it. Do not deploy it as if it were
a fix.

**Do not fold one stack into the other piecemeal.** Schemas have
diverged. Cutover happens as a coordinated multi-repo merge after
the rewrite reaches feature parity and the migration is staged per
`protocols/active-repositories.md`. Until then: production edits →
`main` in the canonical checkout; rewrite edits →
`horizon-leaner-shape` in the worktree.

Stale worktrees on `horizon-re-engineering` are superseded by
`horizon-leaner-shape`; don't pick that branch up.

## New role without a skill — escalate

When an agent claims a role that does not yet have a `skills/<role>.md`
companion (because the role was newly created at runtime, or the
workspace forked from a template that doesn't enumerate every role
yet):

1. Read this file, `AGENTS.md`, and `ESSENCE.md` first.
2. Read `skills/skills.nota` to find the closest existing role-skill
   (likely `skills/designer.md`, `skills/operator.md`, or another
   discipline file) and use it as the discipline baseline.
3. If the role's scope still isn't clear, **escalate** — ask the user
   for guidance on what the role does, what it owns, what its
   neighbouring lanes are. Per `skills/autonomous-agent.md`, escalation
   is the right move when the rule isn't yet on disk.
4. As the role does substantive work, draft a new `skills/<role>.md`
   in-place — capture the discipline you actually applied. Keep it
   compact per `skills/skill-editor.md`.

A workspace where new roles can be created dynamically (e.g. by a
future `persona-orchestrate` daemon) needs this entry point so that a
new role isn't a dead end.

## Intent layer — psyche, log, per-repo, workspace

**Psyche** means the human author. Psyche prompts arrive as
natural language; NOTA-formatted persona messages between agents
are not psyche, agent-written files are not psyche. Only the psyche
is the source of new intent.

The intent layer has three surfaces:

1. **The workspace intent log** at `intent/` — NOTA files
   organised by topic. Each entry holds a terse agent rephrasing,
   the psyche's verbatim quote with surrounding context, a
   certainty marker, and a timestamp. Five record kinds:
   `Decision`, `Principle`, `Correction`, `Clarification`,
   `Constraint`. Discipline: `skills/intent-log.md`.
2. **Per-repo `INTENT.md`** at each repo root — agent-written
   prose, 100% backed by psyche statements, no embellishment or
   inference. Like `ARCHITECTURE.md` but for psyche-stated
   intent. Discipline: `skills/repo-intent.md`.
3. **`ESSENCE.md`** at the workspace root — workspace-level intent.

When an agent encounters a question the intent layer doesn't
speak to (or speaks to ambiguously), the rule is to ask the
psyche before deciding (`skills/intent-clarification.md`). Don't
infer; don't compose new intent from old.

Supersession is always explicit, and **only the psyche can
supersede psyche intent**. An agent encountering documented intent
that seems wrong asks the psyche — never overrides on its own
authority. Discipline: `skills/intent-maintenance.md`.

Eventually the log migrates to typed `persona-mind` memory
variants (`AuthorialDecision`, `AuthorialPrinciple`, …); topic
becomes a relation tag; the file path seeds the memory's `uid`.
Until then, filesystem-organised NOTA files are the carrier.

## See also

- `AGENTS.md` — the compact every-keystroke contract.
- `ESSENCE.md` — workspace essence; most universal psyche intent.
- `orchestrate/AGENTS.md` — role coordination protocol.
- `skills/skills.nota` — typed skill index.
- `skills/skill-editor.md` — how to edit skill files without growing them noisy.
- `skills/intent-log.md` — recording psyche intent.
- `skills/intent-maintenance.md` — sweeping the intent log.
- `skills/intent-clarification.md` — asking the psyche.
- `skills/repo-intent.md` — per-repo `INTENT.md`.
- `intent/` — the workspace log itself.
- `protocols/active-repositories.md` — live repo map and stack discipline.
