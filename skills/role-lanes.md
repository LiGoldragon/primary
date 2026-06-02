# Skill — role lanes

*How lanes work as parallel windows into a role's single agent.
The canonical home for the lane mechanism — every lane reads this
plus its main role's skill, and nothing else lane-specific.*

## The mirror model — lanes are windows, not agents

(Per `intent/persona.nota` 2026-05-22, intent ID 147 in
spirit-v0.1.1.) A **role** (designer, operator, system-operator,
poet, assistant, counselor) names a discipline. Each role has **one agent**: one
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

## Lane naming convention — ordinals and qualifiers; no assistant/specialist suffixes

Per psyche 2026-05-27 (spirit record 920, Maximum): the prior
`<role>-assistant` and `<role>-specialist` conventions are
**RETIRED** workspace-wide. The only valid lane shapes are:

| Shape | Meaning | Examples |
|---|---|---|
| `<role>` | The role's main lane | `designer`, `operator`, `poet`, `system-operator`, `assistant`, `counselor` |
| `second-<role>`, `third-<role>`, `fourth-<role>` | Additional parallel windows on the same role's agent | `second-designer`, `third-designer`, `second-operator` |
| `<qualifier>-<role>` | Specialized lane with a scope-qualifying prefix | `system-operator`, `cluster-operator`, `pi-operator`, `cloud-operator`, `cloud-designer`, `nota-designer`, `system-designer` |

The qualifier set is open but conventional: `system`, `cluster`,
`pi`, `cloud`, `nota`. Ordinal prefixes (`second-`, `third-`)
copy the whole following role per spirit record 174 — a second
cluster-operator is `second-cluster-operator`, not
`second-operator-with-cluster-scope`.

**Retired forms** — do not use, do not introduce:

- `<role>-assistant` (e.g. `designer-assistant`, `poet-assistant`,
  `operator-assistant`).
- `second-<role>-assistant`, `third-<role>-assistant`, etc.
- `<role>-specialist` (e.g. `system-specialist` — renamed to
  `system-operator`).

When the workspace needs additional capacity in a role, the new
window becomes a `second-<role>` or `third-<role>` — a
structural-authority window on the role's agent, not a
subordinate. The authority class is the role; there is no
support-tier authority bracket below it.

**Migration:** existing `reports/<role>-assistant/` directories
are folded into `reports/<role>/`. Numbering is already global
across the role; no collisions. Lock files
(`orchestrate/<role>-assistant.lock`) and registry entries are
removed once their reports have moved.

## Subagent dispatch inherits the dispatcher's lane

Per psyche 2026-05-27 (spirit record 920, Maximum): when an agent
in role R dispatches a subagent, the subagent **inherits the
dispatcher's lane, lock, and report-numbering slot**. The
subagent does not create its own lane.

Concrete consequences:

- **Lane identity.** The subagent operates AS the dispatcher's
  lane. A subagent spawned by `designer` is operating under the
  `designer` lane — same lock file, same authority class, same
  report subdirectory.
- **Lock sharing.** Two subagents dispatched from the same lane
  share that lane's lock. They cannot independently claim
  overlapping scopes — the dispatcher's lock covers them both.
- **Report number allocation by the dispatcher.** Per spirit
  record 289, the dispatcher allocates each subagent's report
  number (and meta-directory slice path) **before** launch and
  states the assignment in the dispatch prompt. Subagents do not
  pick their own number; collisions otherwise.
- **Reports land in the dispatcher's `reports/<role>/`.** The
  subagent writes its sub-report into the dispatcher's role
  subdirectory — typically inside a meta-report directory per
  `skills/reporting.md` §"Meta-report directories — sub-agent
  sessions". Subagent output never lands in a separate
  `<role>-assistant/` subdir; that suffix is retired (see §"Lane
  naming convention" above).
- **Briefing carries the inline-jj rule.** Per `skills/jj.md`,
  every description-taking `jj` invocation must pass the message
  inline. When briefing a subagent, restate the rule so the
  subagent does not type a bare `jj commit` and stall on
  `$EDITOR`.

The subagent is additional capacity for the dispatcher's lane,
not a separate lane. Treating it as a separate lane reintroduces
the assistant-suffix problem the 920 record retired.

## What's shared, what's per-lane

Per-lane (the filesystem / coordination surface for this window):

| Per-lane                        | Example                                      |
|---------------------------------|----------------------------------------------|
| Lock filename                   | `designer.lock`, `second-designer.lock`, `cluster-operator.lock`, … |
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
- **Owned area + authority class** — structural for every lane
  shape (`<role>`, `second-<role>`, `<qualifier>-<role>`). The
  former support-tier `-assistant` bracket is retired
  (record 920); all lanes carry structural authority for their
  role.
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

The lane identifier is the exact role-name the harness gave the
agent. Do not substitute the nearest existing lane. If the session
role is `pi-operator`, claim `pi-operator`, write reports under
`reports/pi-operator/`, and use `orchestrate/pi-operator.lock`.

Whatever lane you're claiming, the reading list is two skills:

1. **`skills/role-lanes.md`** (this file) — the lane mechanism.
2. **`skills/<main-role>.md`** — your discipline. The "main role"
   for `second-designer` / `third-designer` / `cloud-designer` /
   `nota-designer` / `system-designer` is `designer`; for
   `pi-operator` / `cluster-operator` / `cloud-operator` /
   `second-operator` is `operator`; for `system-operator` it's
   its own discipline file; for `poet` lanes it's `poet`; for
   `assistant` lanes it's `assistant`; for `counselor` lanes it's
   `counselor`; etc.

Then claim under your lane's identifier:

```sh
tools/orchestrate claim <lane> <scope> [more-scopes] -- <reason>
```

…and write reports under `reports/<lane>/`. The lane's identifier
is the filename of its lock file minus `.lock`.

## Why lanes don't get their own skill files

Per-lane skill files were duplication of the main role's skill,
not content. They are gone. The canonical home for *what shape a
lane has* is this file. The canonical home for *what discipline
a lane practices* is the main role's skill. The canonical home
for *what lanes exist* is `AGENTS.md`'s role table.

## Registering a new lane

A new lane (a `third-designer`, a `second-cluster-operator`, or a
future fifth lane under any main role) requires:

1. Add the lane to `orchestrate/roles.list` (the lane registry
   read by `tools/orchestrate`). Use `parallel-of:<main-role>`
   for ordinal lanes and bare for qualified specialist lanes.
   The eventual destination format is `orchestrate/roles.nota`
   — a typed Nota record — per the design report referenced from
   `orchestrate/roles.list`.
2. Create its report subdirectory: `reports/<lane>/`.
   A brand-new main role also gets `skills/<role>.md` and a `Role`
   entry in `skills/skills.nota`.
3. The `.gitignore` rule `/orchestrate/*.lock` already covers the
   new lock file; no edit needed.
4. Update the role table in `AGENTS.md` and `orchestrate/AGENTS.md`
   to mention the lane.

That is the whole list for an additional lane under an existing
role. No lane-specific skill file is created. The main role's skill
applies to every lane under it, regardless of how many lanes
there are.

## See also

- this workspace's `AGENTS.md` — the role table; the list of which
  lanes currently exist.
- this workspace's `orchestrate/AGENTS.md` — the claim flow,
  lock-file format, status command, blocked-work flow, BEADS rules.
- this workspace's `skills/designer.md`,
  `skills/operator.md`,
  `skills/system-operator.md`,
  `skills/poet.md`,
  `skills/assistant.md`,
  `skills/counselor.md` — the six main role skills. Every lane under
  one of these inherits its discipline.
- this workspace's `ESSENCE.md` §"Efficiency of instruction" — the
  one-canonical-home principle that this skill realises.
