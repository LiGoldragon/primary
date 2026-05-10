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
4. **Required workspace skills** — before any work, read:
   - `skills/autonomous-agent.md` — how to act on routine
     obstacles; lists checkpoint-read skills.
   - `skills/skill-editor.md` — conventions for editing
     skills.
   - `skills/reporting.md` — reports vs. chat; always-name-
     paths; inline-summary rule for cross-references.
   - `skills/jj.md` — version-control discipline.
     **`jj describe @` is forbidden**; use `jj commit -m`.
     Read `jj st` output before every commit.
   - `skills/repository-management.md` — `gh` CLI for repo
     creation and metadata.
   - Read other `skills/<name>.md` on demand for the work at
     hand (e.g., `rust-discipline.md` when writing Rust;
     `contract-repo.md` when working on a contract crate;
     `language-design.md` when designing notation).
5. **The repo's `AGENTS.md` + `skills.md`** when editing inside
   a repo under `repos/`.

## Roles

The workspace recognises six coordination roles:

- `operator` — implementation; default agent: Codex.
- `operator-assistant` — extra implementation/audit capacity
  under operator discipline; default agent: any.
- `designer` — architecture, skills, reports; default agent: Claude.
- `designer-assistant` — extra design/audit capacity under
  designer discipline; default agent: Codex.
- `system-specialist` — OS / platform / deploy; default agent: any.
- `poet` — writing as craft; default agent: any.

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
| `reports/<role>/` | Role-owned reports (`operator/`, `operator-assistant/`, `designer/`, `designer-assistant/`, `system-specialist/`, `poet/`). Exempt from claim flow; each role writes only its own subdirectory. |
| `<role>.lock` | Per-role coordination state file. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Never claimed; any agent may write BEADS tasks at any time. **Transitional** — see below. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Broad recent checkout index + cutoff rule. Not the active architecture set. |
| `GOALS.md` | Standing high-level goals. |

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
`reports/operator/97-native-issue-notes-tracker-research.md`
and the `signal-persona-mind` / `persona-mind` repos. The work
graph is part of Persona's central mind state, not a separate
component. Don't build a Persona↔bd bridge; don't deepen the bd
investment. Use bd only for short-tracked-item coordination while
the native mind graph is being implemented; design new shapes
assuming bd goes away.

BEADS is never an ownership lock. Do not claim `.beads/`.
Any agent may create, update, comment on, or close BEADS tasks
at any time. If the current backend reports a database lock,
that is storage-engine contention, not coordination ownership.
