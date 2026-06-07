# Skill — role lanes

*How lanes work as parallel windows into a role's single agent.*

## The mirror model — lanes are windows, not agents

A **role** (designer, operator, system-operator, poet,
videographer, assistant, counselor) names a discipline. Each role
has **one agent**: one cryptographic identity, one shared
persona-mind state, one ongoing body of signed work. **Lanes are
windows into that agent.** Running `designer` and `second-designer`
side by side is two windows on the same Designer agent — two
terminals into one persona, not two designers. The framing: *more
talking windows to the same agent.*

The agent's state lives in shared infrastructure (persona-mind for
memory; persona-spirit for intent; persona-orchestrate for the lane
registry and occupancy). Every window reads and writes that shared
state, so they converge automatically. An ordinal prefix
(`second-`, `third-`) disambiguates the filesystem position (lock
file, report subdirectory, claim string), not the agent.

## Lane naming — ordinals and qualifiers only

The only valid lane shapes:

| Shape | Meaning | Examples |
|---|---|---|
| `<role>` | The role's main lane | `designer`, `operator`, `poet` |
| `second-<role>`, `third-<role>` | Additional parallel windows on the same agent | `second-designer`, `third-operator` |
| `<qualifier>-<role>` | Specialized lane with a scope-qualifying prefix | `cluster-operator`, `pi-operator`, `cloud-designer`, `nota-designer`, `system-designer` |

The qualifier set is open but conventional: `system`, `cluster`,
`pi`, `cloud`, `nota`. An ordinal prefix copies the whole following
role — a second cluster-operator is `second-cluster-operator`, not
`second-operator-with-cluster-scope`.

Forbidden forms: `<role>-assistant`, `<role>-specialist`, and any
ordinal variant of them (`second-designer-assistant`). Additional
capacity in a role is a `second-<role>` / `third-<role>` — a
structural-authority window on the agent, not a subordinate. The
authority class is the role; there is no support-tier bracket below
it.

## Subagent dispatch inherits the dispatcher's lane

When an agent in role R dispatches a subagent, the subagent
**inherits the dispatcher's lane, lock, and report-numbering
slot**. It does not create its own lane. Consequences:

- **Lane identity.** A subagent spawned by `designer` operates AS
  `designer` — same lock file, same authority class, same report
  subdirectory.
- **Lock sharing.** Subagents from the same lane share that lane's
  lock; they cannot independently claim overlapping scopes.
- **Dispatcher allocates report numbers.** The dispatcher assigns
  each subagent's report number (and meta-directory path) before
  launch and states it in the dispatch prompt — subagents picking
  their own numbers collide.
- **Reports land in the dispatcher's `reports/<role>/`**, typically
  inside a meta-report directory (see `skills/reporting.md`).
- **Briefing carries the inline-jj rule.** Restate that every
  description-taking `jj` invocation passes its message inline, so
  the subagent never types a bare `jj commit` and stalls on
  `$EDITOR` (see `skills/jj.md`).

Treating a subagent as a separate lane reintroduces the
assistant-suffix problem the naming convention forbids.

## What's shared, what's per-lane

Per-lane (the coordination surface for this window):

| Per-lane | Example |
|---|---|
| Lock filename | `designer.lock`, `cluster-operator.lock` |
| Report-write subdirectory | `reports/designer/` — the window writes here; the agent READS from all of its windows' subdirectories |
| Claim string | `tools/orchestrate claim designer …` |

Per-window (each open UI session has its own): **live LLM context**
(session-local; when a window compacts or clears, the agent's
shared memory survives) and **process/harness state** (pid, window
id, pty).

Shared across all lanes of one role (the agent's surface):

- **Discipline + required reading** — `skills/<role>.md` plus the
  workspace baseline. Read once; every window's list is identical.
- **Owned area + authority class** — structural for every lane
  shape.
- **Cryptographic identity** — one keypair per role; all windows
  sign as the role's agent.
- **Persistent memory** — persona-mind state, intent records in
  persona-spirit, reports across the role's subdirectories.
- **Beads** — beads carry no `role:*` labels. Any agent picks up
  any bead by topic affinity; lanes coordinate through lock files
  and reports, not bead labels.

### Cross-window coordination

Two windows of one role must not race each other:

1. **Lock files per lane.** A window's claim records in its
   `<lane>.lock`; other windows see it and stay out of that scope
   (the `tools/orchestrate` mechanism).
2. **Shared persistent memory.** Intent records, reports, beads,
   and ARCH edits are visible to every window via the filesystem;
   the agent's knowledge converges through the shared substrate.
3. **Session-local context limits.** A window's context is bounded;
   the agent's full knowledge is broader than any one window holds.

The standing discipline when a window starts substantive work:
**query the shared state first** — spirit for recent intent, the
role's report subdirectories for active threads, beads for
in-flight tasks. This is what keeps parallel windows coherent;
without it they drift.

## How to read this for your lane

The lane identifier is the exact role-name the harness gave the
agent. Do not substitute the nearest existing lane. If the session
role is `pi-operator`, claim `pi-operator`, write reports under
`reports/pi-operator/`, and use `orchestrate/pi-operator.lock`.

Your reading list is two skills: this file (the lane mechanism) and
`skills/<main-role>.md` (your discipline). The main role for
`second-designer` / `cloud-designer` / `nota-designer` /
`system-designer` is `designer`; for `pi-operator` /
`cluster-operator` / `cloud-operator` / `second-operator` it's
`operator`; `system-operator`, `poet`, `videographer`,
`assistant`, and `counselor` each have their own discipline file.

Then claim under your lane's identifier:

```sh
tools/orchestrate claim <lane> <scope> [more-scopes] -- <reason>
```

…and write reports under `reports/<lane>/`. The lane's identifier
is its lock filename minus `.lock`.

## Why lanes don't get their own skill files

A per-lane skill file would duplicate the main role's skill without
adding content. The canonical home for *what shape a lane has* is
this file; for *what discipline a lane practices*, the main role's
skill; for *what lanes exist*, `AGENTS.md`'s role table.

## Registering a new lane

A new lane (a `third-designer`, a `second-cluster-operator`)
requires:

1. Add it to `orchestrate/roles.list` (the registry
   `tools/orchestrate` reads) — `parallel-of:<main-role>` for
   ordinal lanes, bare for qualified specialist lanes.
2. Create its report subdirectory `reports/<lane>/`. A brand-new
   *main* role also gets `skills/<role>.md` and a `Role` entry in
   `skills/skills.nota`.
3. The `.gitignore` rule `/orchestrate/*.lock` already covers the
   new lock file; no edit needed.
4. Mention the lane in the role tables of `AGENTS.md` and
   `orchestrate/AGENTS.md`.

No lane-specific skill file is created. The main role's skill
applies to every lane under it.

## See also

- `AGENTS.md` — the role table and the list of current lanes.
- `orchestrate/AGENTS.md` — claim flow, lock-file format, status
  command, blocked-work flow.
- `skills/designer.md`, `skills/operator.md` (and the other main
  role skills) — the discipline every lane under each inherits.
