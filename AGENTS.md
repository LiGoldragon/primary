# Primary Workspace — Agent Instructions

This file names what's specific to *this* workspace. The
cross-workspace agent discipline lives in `lore/AGENTS.md`.

## Required reading, in order

1. **`ESSENCE.md`** — workspace intent. Upstream of every other
   doc. If a downstream rule conflicts with intent, intent wins.
2. **`lore/AGENTS.md`** — canonical agent contract. AGENTS/CLAUDE
   shim pattern, per-repo `ARCHITECTURE.md`, documentation
   layers, beauty-as-criterion, verb-belongs-to-noun, push-not-
   poll, naming, design reports as visuals, parallel-tool-result
   verification, version control via `skills/version-control.md`.
3. **`protocols/orchestration.md`** — how operator and designer
   share this workspace.
4. **The relevant `skills/<name>.md`** — start with
   `autonomous-agent.md` and `skill-editor.md`. Read the others
   on demand for the work at hand.
5. **The repo's `AGENTS.md` + `skills.md`** when editing inside
   a repo under `repos/`.

## Roles

- **Codex** acts as `operator`.
- **Claude** acts as `designer`.

Each agent must know its role before claiming or editing. The
coordination protocol is `protocols/orchestration.md`; the
helper is `tools/orchestrate`.

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace intent — upstream. |
| `protocols/orchestration.md` | Role-coordination protocol. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `reports/designer/`, `reports/operator/` | Role-owned reports. Exempt from claim flow; each role writes only its own subdirectory. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Short-tracked-item store. **Transitional** — see below. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Active repo list + cutoff rule. |
| `GOALS.md` | Standing high-level goals. |

## No harness-dependent memory

Memory and persistent agent state belong in workspace files —
`skills/`, `lore/`, `reports/`, `protocols/`, repo `skills.md`,
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
**Persona's typed messaging fabric** — see
`reports/designer/2026-05-06-persona-messaging-design.md` for
the design. Don't build a Persona↔bd bridge; don't deepen the bd
investment. Use bd for short-tracked-item coordination today;
design new shapes assuming bd goes away.
