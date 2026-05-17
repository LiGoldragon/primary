# Skill — role lanes

*How assistant lanes stack under a main role. The canonical home for
the lane mechanism — every assistant lane reads this plus its main
role's skill, and nothing else lane-specific.*

---

## What a role lane is

A **main role** names a discipline: `designer`, `operator`,
`system-specialist`, `poet`. Each main role has its own skill file
(`skills/<role>.md`) carrying the discipline's required reading,
owned area, working pattern, and authority boundaries.

A **lane** is one agent's seat under a main role. The main role
itself is its own first lane. Additional lanes stack as needed:

```
designer                            ← main lane (the discipline's owner)
designer-assistant                  ← second lane
second-designer-assistant           ← third lane
third-designer-assistant            ← fourth lane (if registered)
...
```

Every lane under a main role **shares the main role's discipline,
required reading, owned area, and beads label.** Lanes exist so
parallel capacity is *visible* to the coordination protocol — two
agents working under one main role with no per-lane lock are
invisible peers, racing each other's edits.

## What's shared, what's per-lane

Three things are per-lane and three things only:

| Per-lane                        | Example                                      |
|---------------------------------|----------------------------------------------|
| Lock filename                   | `designer.lock`, `designer-assistant.lock`, … |
| Report lane (subdirectory)      | `reports/designer/`, `reports/designer-assistant/`, … |
| Claim string                    | `tools/orchestrate claim designer …`, `tools/orchestrate claim designer-assistant …`, … |

Everything else is shared with the main role:

- **Discipline** — what the role attends to (the discipline lives in
  `skills/<main-role>.md`).
- **Required reading** — the workspace baseline, the role-specific
  reading list. Read the main role's skill, and you've read every
  lane's reading list.
- **Owned area + authority** — what the lane may decide, what it may
  not. Lanes don't get more authority than the main role; assistant
  lanes typically scope themselves to bounded support inside the
  main role's authority. See the main role's *"Working with
  assistants"* section for discipline-specific guidance.
- **Beads label** — work items go under `role:<main-role>` (e.g.
  `role:designer`), never `role:designer-assistant`. See
  `orchestrate/AGENTS.md` §"Beads belong to main roles, not
  assistants." A bead is visible to the discipline pool — main lane
  plus every assistant lane under it — and any agent in the pool
  can pick it up.

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

1. Declare the lane in `orchestrate/roles.nota` (the role registry
   read by `tools/orchestrate`). Name its `assistant-of` main role.
2. Create its report subdirectory: `reports/<lane>/`.
3. Add its lock filename to `.gitignore`.
4. Update the role table in `AGENTS.md` to mention the lane.

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
