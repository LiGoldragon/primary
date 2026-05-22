# Skill — role lanes

*How lanes work as parallel windows into a role's single agent.
The canonical home for the lane mechanism — every lane reads this
plus its main role's skill, and nothing else lane-specific.*

## The mirror model — lanes are windows, not agents

(Per `intent/persona.nota` 2026-05-22, intent ID 147 in
spirit-v0.1.1.) A **role** (designer, operator, system-specialist,
poet) names a discipline. Each role has **one agent**: one
persistent cryptographic identity, one shared persona-mind state,
one ongoing body of signed work. **Lanes are windows into that
agent.** When the workspace runs `designer` and `second-designer`
side by side, those are two windows on the same Designer agent —
two terminals open into the same persona, not two separate
designers.

The keystone framing: *I just need more talking windows to the
same agent.*

The agent's state lives in shared persona infrastructure
(persona-mind for memory; persona-spirit for intent records;
persona-orchestrate for lane registry + occupancy). Each window
reads + writes the shared state, so they converge automatically.
The agent has one knowledge, one identity, one ongoing thread of
work — multiple windows let the psyche talk to it from several
positions at once.

Lane names that carry the same role plus an ordinal prefix
(`designer`, `second-designer`, `third-designer`) are all windows
to the same Designer agent. The ordinal disambiguates the
filesystem position (lock file, report subdirectory, claim
string), not the agent.

### Assistant lanes — bounded-authority windows on the same agent

Assistant lanes (`<role>-assistant`, `second-<role>-assistant`)
are also windows on the role's agent, but at **bounded support
authority** (per `intent/persona.nota` 2026-05-21 records on
authority class). Same agent, same identity, same shared memory —
but the lane's claim flow is scoped to support-tier work
(audits, sweeps, mechanical edits) rather than structural
decisions. Structural authority stays with the role's
parallel-main lanes (`<role>`, `second-<role>`, etc.).

A lane carrying just `<role>` or `second-<role>` is a
**structural-authority window**. A lane carrying `-assistant` is
a **support-authority window**. The agent backing both is the
same.

## What's shared, what's per-lane

Per-lane (the filesystem / coordination surface for this window):

| Per-lane                        | Example                                      |
|---------------------------------|----------------------------------------------|
| Lock filename                   | `designer.lock`, `second-designer.lock`, `designer-assistant.lock`, … |
| Report-write subdirectory       | `reports/designer/`, `reports/second-designer/`, … (the window writes here; the agent READS from all of its windows' report subdirectories) |
| Claim string                    | `tools/orchestrate claim designer …`, `tools/orchestrate claim second-designer …`, … |

Per-window-not-per-lane (each open UI session has its own):

- **Live LLM context** — what's currently in the chat session. The
  context-window contents are session-local; the underlying
  knowledge is in the agent's shared memory. When a window
  compacts or clears, the agent's memory survives.
- **Process / harness state** — pid, claude-code window id,
  terminal-cell pty. Per-session.

Shared across all lanes of the same role (the agent's surface):

- **Discipline** — what the role attends to (`skills/<role>.md`).
- **Required reading** — the workspace baseline + role-specific
  reading list. Read the role's skill once; every window's reading
  list is the same.
- **Owned area + authority class** — structural for
  `<role>`/`second-<role>`; support for `-assistant` variants.
- **Cryptographic identity** — one keypair per role; all windows
  sign as the role's agent (per `intent/persona.nota` ID 148).
- **Persistent memory** — persona-mind state for the role; intent
  records in persona-spirit; reports across the role's
  subdirectories.
- **Beads** — as of 2026-05-19 (per `intent/workspace.nota`), beads
  do not carry `role:*` labels. Any agent picks up any bead based
  on topic affinity. Lanes coordinate through lock files and
  reports, not bead labels.

### Cross-window coordination

Two windows of the same role need to coordinate so they don't
race each other. Three mechanisms:

1. **Lock files per lane.** When a window claims a scope, its
   `<lane>.lock` file records the claim. Other windows see the
   lock and stay out of that scope. This is the existing
   `tools/orchestrate` mechanism.
2. **Shared persistent memory.** Intent records, reports, beads,
   ARCH edits — all visible to every window via the filesystem.
   When window A files an intent record, window B can query
   spirit and see it. The agent's knowledge converges through
   the shared substrate.
3. **Session-local context limits.** A window's LLM context is
   bounded; the agent's full knowledge is broader than any one
   window can hold. Windows pick up shared state by querying
   spirit / reading recent reports / consulting intent files at
   the start of substantive work.

When a window starts substantive work, the standing discipline
is: **query the shared state first** (spirit for recent intent;
the role's report subdirectories for active threads; beads for
in-flight tasks). This is what makes parallel windows coherent;
without it they drift.

## How to read this for your lane

Whatever lane you're claiming, the reading list is two skills:

1. **`skills/role-lanes.md`** (this file) — the lane mechanism.
2. **`skills/<main-role>.md`** — your discipline. The "main role" for
   `designer-assistant` is `designer`; for `second-operator-assistant`
   is `operator`; for `poet-assistant` is `poet`; etc.

Then claim under your lane's identifier:

```sh
tools/orchestrate claim <lane> <scope> [more-scopes] -- <reason>
```

…and write reports under `reports/<lane>/`. The lane's identifier
is the filename of its lock file minus `.lock`.

## Why lanes don't get their own skill files

Each assistant lane previously had its own skill file (e.g.
`skills/designer-assistant.md`, `skills/second-designer-assistant.md`).
Those files repeated their main role's required-reading list, the
beads-label rule, and the claim shape, with three identifiers swapped
per file. Per `ESSENCE.md` §"Efficiency of instruction" — *each rule
lives in one canonical place; other docs cite by reference; they
don't restate* — the per-lane skill files were duplication, not
content. They are gone.

The canonical home for *what shape an assistant lane has* is this
file. The canonical home for *what discipline an assistant lane
practices* is the main role's skill. The canonical home for *what
lanes exist* is `AGENTS.md`'s role table.

## Registering a new lane

A new lane (a `third-designer-assistant`, a `fourth-operator-assistant`,
or a future fifth lane under any main role) requires:

1. Add the lane to `orchestrate/roles.list` (the lane registry read
   by `tools/orchestrate`). Name its `assistant-of` main role on the
   same line. The eventual destination format is `orchestrate/roles.nota`
   — a typed Nota record — per the design report referenced from
   `orchestrate/roles.list`.
2. Create its report subdirectory: `reports/<lane>/`.
3. The `.gitignore` rule `/orchestrate/*.lock` already covers the new
   lock file; no edit needed.
4. Update the role table in `AGENTS.md` and `orchestrate/AGENTS.md`
   to mention the lane.

That is the whole list. No new skill file. No new section in the
main role's skill — the main role's *"Working with assistants"*
guidance applies to every lane under it, regardless of how many
lanes there are.

## See also

- this workspace's `AGENTS.md` — the role table; the list of which
  lanes currently exist.
- this workspace's `orchestrate/AGENTS.md` — the claim flow,
  lock-file format, status command, blocked-work flow, BEADS rules.
- this workspace's `skills/designer.md`,
  `skills/operator.md`,
  `skills/system-specialist.md`,
  `skills/poet.md` — the four main role skills. Every lane under
  one of these inherits its discipline.
- this workspace's `ESSENCE.md` §"Efficiency of instruction" — the
  one-canonical-home principle that this skill realises.
