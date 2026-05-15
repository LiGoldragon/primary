# Primary Workspace — Agent Instructions

This file names what's specific to *this* workspace. The
cross-workspace agent discipline lives in `repos/lore/AGENTS.md`.

## Required reading, in order

1. **`ESSENCE.md`** — workspace intent. Upstream of every other
   doc. If a downstream rule conflicts with intent, intent wins.
2. **`repos/lore/AGENTS.md`** — canonical agent contract. AGENTS/CLAUDE
   shim pattern, per-repo `ARCHITECTURE.md`, documentation
   layers, beauty-as-criterion, verb-belongs-to-noun, push-not-
   poll, naming, design reports as visuals, parallel-tool-result
   verification, version control via `skills/jj.md`.
3. **`protocols/orchestration.md`** — how roles share this
   workspace.
4. **Your role's `skills/<role>.md` is the required-reading
   list.** Each role's skill file carries an explicit
   "Required reading" section listing every workspace skill
   mandatory for that role:

   - `operator` / `operator-assistant` → `skills/operator.md`
   - `designer` / `designer-assistant` → `skills/designer.md`
   - `system-specialist` / `system-assistant` → `skills/system-specialist.md`
   - `poet` / `poet-assistant` → `skills/poet.md`

   Assistants also read their own assistant file
   (`skills/<role>-assistant.md`); the reading list it carries
   is identical to the main role's. Read every skill the role
   lists before doing substantive work in that role.
5. **The repo's `AGENTS.md` + `skills.md`** when editing inside
   a repo under `repos/`.

## Nix store search is forbidden

The Nix store is not a workspace search surface. Do not run
generic filesystem search or traversal tools (`rg`, `grep`,
`find`, `fd`, broad shell globs, recursive `ls`) against
`/nix/store`.

When looking for Nix-controlled information, use Nix: inspect the
source checkout, `nix eval`, `nix flake show`, `nix flake
metadata`, `nix path-info`, or a targeted derivation output. If a
value cannot be reached that way, change the Nix code so the value
is exposed as an evaluable option, package, check, passthru, or
helper output.

## Feature branches live in worktrees, not the canonical checkout

When work touches code that is already in production (the deploy
stack, the OS layer, anything users depend on right now) and the
arc spans more than one commit, the work belongs on a feature
branch in a *separate worktree* — not on the canonical ghq
checkout under `/git/...`. Keeping the canonical checkout on
`main` is what lets every peer agent see production reality
without negotiating who-has-the-checkout.

The worktree path is parallel-and-predictable:
`~/wt/github.com/<owner>/<repo>/<branch-name>/`. Same shape as
the ghq layout under `/git/github.com/...`, with the branch name
as the leaf directory. The same branch name is used across every
repo a multi-repo arc touches.

The full discipline — when to use a worktree, how to create one
(jj-colocated and plain-git forms), branch naming, push flow,
cleanup at merge time, and the orchestration-protocol interaction
— lives in `skills/feature-development.md`. Read that skill
before starting any non-trivial branch work; it is part of every
role's required reading.

## Roles

The workspace recognises eight coordination roles:

- `operator` — implementation; default agent: Codex.
- `operator-assistant` — extra implementation/audit capacity
  under operator discipline; default agent: any.
- `designer` — architecture, skills, reports; default agent: Claude.
- `designer-assistant` — extra design/audit capacity under
  designer discipline; default agent: Codex.
- `system-specialist` — OS / platform / deploy; default agent: any.
- `system-assistant` — extra OS/platform/host capacity under
  system-specialist discipline; default agent: any.
- `poet` — writing as craft; default agent: any.
- `poet-assistant` — extra writing, citation, and publishing
  capacity under poet discipline; default agent: any.

Each agent must know its role before claiming or editing. The
coordination protocol is `protocols/orchestration.md`; the
helper is `tools/orchestrate`.

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace intent — upstream. |
| `protocols/orchestration.md` | Role-coordination protocol. |
| `protocols/active-repositories.md` | Current active repo map for architecture sweeps. Smaller than the recent checkout index. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `reports/<role>/` | Role-owned reports (`operator/`, `operator-assistant/`, `designer/`, `designer-assistant/`, `system-specialist/`, `system-assistant/`, `poet/`, `poet-assistant/`). Exempt from claim flow; each role writes only its own subdirectory. |
| `<role>.lock` | Per-role coordination state file. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Never claimed; any agent may write BEADS tasks at any time. **Transitional** — see below. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Broad recent checkout index + cutoff rule. Not the active architecture set. |
| `GOALS.md` | Standing high-level goals. |

## Spell every identifier as a full English word

`Request` not `Req`. `Reply` not `Rep`. `Configuration` not `Cfg`.
Types, fields, variables, macro template placeholders, file-internal
helpers — *everything* spells out. The narrow carve-outs (loop
counters, generic type parameters with no semantic content, common
acronyms, std-library names) and the full justification live in
`ESSENCE.md` §"Naming — full English words" and `skills/naming.md`.
This rule is ignored often enough to warrant being surfaced here.

## Reports are for agents; chat is for the user

Long-form output goes in `reports/<role>/`. Reports are the
durable, scrollable, agent-consumable record — peers and future
versions of yourself read them. Chat is the **user's** working
surface; the user reads it now and acts on it.

The implication: a chat reply is never *just* a pointer to a
report when the user has something to attend to. Whatever the
user must read, decide on, or act on goes **in the chat with
full inline context** — open questions, blockers, surprising
findings, recommendations awaiting approval — each stated so
the user can engage without opening the report. Opaque IDs,
section numbers, or "see report N" without inline substance
are a discipline violation: the user is not navigating a
database while reading.

A small chat reply is fine when the output is small. An
elaborate output deserves a report **plus** a chat reply that
carries the user-attention items inline. See
`skills/reporting.md` §"When to write a report vs answer in
chat" and §"What goes in chat when a report exists" for the
discipline in full.

## No harness-dependent memory

Memory and persistent agent state belong in workspace files —
`skills/`, `repos/lore/`, `reports/`, `protocols/`, repo `skills.md`,
repo `ARCHITECTURE.md`, or `.beads/` while bd is the active
substrate. **Don't use harness-dependent memory systems** —
e.g. Claude Code's per-session memory files at
`~/.claude/projects/<workspace>/memory/`, or any agent-private
state store an outside agent cannot read.

**Why:** memory tied to one harness is invisible to every other
harness and to the human. The workspace's truth must live in
files every agent can open. If you learn something durable,
write it to the right workspace file (per
`skills/skill-editor.md` and the report conventions in
`protocols/orchestration.md`); never to harness-private state.

## BEADS is transitional

`.beads/` exists today for convenience. The destination is
**Persona's native typed work graph** — see
`reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md`
§2.2 and the `signal-persona-mind` / `persona-mind` repos. The
work graph is part of Persona's central mind state, not a
separate component. Don't build a Persona↔bd bridge; don't
deepen the bd investment. Use bd only for short-tracked-item
coordination while the native mind graph is being implemented;
design new shapes assuming bd goes away.

BEADS is never an ownership lock. Do not claim `.beads/`.
Any agent may create, update, comment on, or close BEADS tasks
at any time. If the current backend reports a database lock,
that is storage-engine contention, not coordination ownership.
