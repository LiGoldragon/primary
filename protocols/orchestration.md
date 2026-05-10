# Orchestration Protocol

The orchestration protocol coordinates autonomous agents sharing the same
workspace. The current shell-helper implementation combines role-owned lock
files with the transitional workspace BEADS task database so agents see both
file ownership and open work before they edit.

The destination is the **command-line mind**: the Rust `mind` CLI as a thin
client to the long-lived `persona-mind` daemon, using the
`signal-persona-mind` contract. It replaces lock-file ownership and BEADS work
tracking with typed role state, activity, and a native work/memory graph stored
in `mind.redb`.

BEADS is shared coordination state while it exists, not a lockable scope.

## Roles

The workspace recognises six coordination roles. Each role has its own lock
file, its own report subdirectory, and a natural primary scope.

| Role | Default agent | Lock file | Reports subdir | Natural primary scope |
|---|---|---|---|---|
| `operator` | Codex | `operator.lock` | `reports/operator/` | Rust crates, persona, sema-ecosystem implementation |
| `operator-assistant` | (any) | `operator-assistant.lock` | `reports/operator-assistant/` | Extra implementation/audit workforce under operator discipline |
| `designer` | Claude | `designer.lock` | `reports/designer/` | ESSENCE, AGENTS, lore, skills, design reports |
| `designer-assistant` | Codex | `designer-assistant.lock` | `reports/designer-assistant/` | Extra design audit, report, skill, and protocol support under designer discipline |
| `system-specialist` | (any) | `system-specialist.lock` | `reports/system-specialist/` | CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon |
| `poet` | (any) | `poet.lock` | `reports/poet/` | TheBookOfSol, substack-cli, prose-craft surfaces |

The "Default agent" column is convenience labelling for the lock file, not a
binding. Any agent may take any role; the role determines scope authority,
not which model holds it.

Each agent must know its role before claiming work. Each agent edits only
its own lock file.

## Coordination State

- Lock files: one per role at `<role>.lock` (e.g. `operator.lock`,
  `system-specialist.lock`).
- BEADS database: `.beads/` (legacy transitional work-item store).
- Helper: `tools/orchestrate`.

Each agent writes only its own lock file. The lock files are coordination
records, not operating-system locks.

`.beads/` is never claimed. Any agent may create, update, comment on, or close
BEADS tasks at any time. A BEADS task is a shared work item, not a file-ownership
claim.

### Command-line mind target

The current implementation is the lock-file helper described below. The target
implementation is the Rust `mind` CLI backed by a long-lived `persona-mind`
daemon and the `signal-persona-mind` contract. `tools/orchestrate` remains the
compatibility helper name during migration.

Target surface:

```sh
mind '<one NOTA request record>'
```

Target invariants:

- The protocol truth is the typed `signal-persona-mind` request/reply
  vocabulary.
- The `mind` binary accepts exactly one NOTA request record and prints exactly
  one NOTA reply record.
- The `mind` binary is a thin client. The long-lived `persona-mind` daemon owns
  `MindRoot` and `mind.redb`.
- If `tools/orchestrate` survives during cutover, it is only an external
  workspace wrapper that translates the current ergonomic commands into the
  canonical one-record CLI. It is not a `persona-mind` component.
- Durable state lives in `mind.redb`, owned by `persona-mind` through its
  mind-specific Sema layer/table declarations.
- Lock files are current helper state only. They are not imported, read, or
  projected by `persona-mind`; they retire at the workspace cutover boundary.
- Claim, release, and handoff requests create activity records automatically.
- The mind graph supplies native typed work items, notes, dependencies,
  decisions, aliases, and ready-work queries through the same
  `signal-persona-mind` contract.
- BEADS is retired by the `persona-mind` wave. Existing BEADS entries may be
  imported once as native mind events and aliases, but there is no long-term
  Persona↔bd bridge and no dual-write path.

Until that Rust path is implemented and tested, the shell helper remains the
canonical writer for lock files. The `persona-mind` implementation does not
need lock-file projection logic. Once agents use `mind` directly, lock files
disappear as an ownership mechanism rather than becoming a parallel state
model.

### Lock-file format

Each lock file is plain text. Each line is **one scope**, optionally
followed by `# reason`. An empty file means the role is idle.

A **scope** is one of two kinds:

- **Path lock** — an absolute path. Coordinates editing of files/dirs
  on disk. Overlap rule: a path lock conflicts with another path lock
  if they're equal or nested.
- **Task lock** — a bracketed token like `[primary-f99]`. Coordinates
  *who is actively working on* a BEADS task (or any other named work
  item the bracketed token identifies). Overlap rule: exact match.

```
/home/li/primary/skills/autonomous-agent.md # sync claim-helper docs
[primary-f99] # chroma nota-codec migration
```

The two kinds are independent: a path lock and a task lock never
conflict, and a single role can hold both at once (e.g. claim the
task plus the specific paths the task requires).

The filename names the role; nothing else needs to live in the file. To
inspect, `cat <role>.lock` or `tools/orchestrate status`. The helper is the
canonical writer; agents may also edit lock files by hand as long as the
format is preserved.

Lock files are **runtime state, gitignored.** They live on the local
filesystem only — coordination between agents on the same machine, not
versioned history. A clean checkout starts with no lock files; the helper
creates them on first claim. Don't commit them, don't expect them to
travel between machines.

## Claim Flow

Before editing files, running commands that create/modify/delete files, or
taking on a tracked unit of work, an agent claims its intended scope.

```sh
tools/orchestrate claim <role> <scope> [more-scopes] -- <reason>
```

`<role>` is one of `operator`, `operator-assistant`, `designer`,
`designer-assistant`, `system-specialist`, or `poet`.
Each `<scope>` is either an absolute path or a bracketed task lock
(`'[primary-f99]'` — quote it; `[` is a shell glob character).

Mix freely:

```sh
tools/orchestrate claim system-specialist '[primary-f99]' \
  /git/github.com/LiGoldragon/chroma -- chroma nota-codec migration
```

The helper performs the required work in one call:

1. Writes the intended scopes into the role's own lock file: one scope
   per line, each annotated with the supplied reason as a `# comment`.
2. Reads every role's lock file.
3. Lists open BEADS tasks.
4. Checks every other active lock for overlap (path nesting for path
   locks; exact match for task locks).
5. Clears the role's claim and exits non-zero if any overlap exists.

Use absolute paths where possible. For linked repositories under `repos/`,
claim the real repository path under `/git/...`, not only the symlink path. A
whole repository may be claimed by listing its repository root path.

### When to use a task lock

Task locks bridge BEADS' lifecycle (filed → open → closed) to in-flight
coordination ("who is working on this *right now*"). Use one when you
take on a tracked task that other agents might otherwise also pick up:

```sh
tools/orchestrate claim system-specialist '[primary-f99]' -- chroma migration
# … do the work …
tools/orchestrate release system-specialist
bd close primary-f99 -r "<closing note>"
```

A bead going from open → closed in BEADS doesn't tell other agents
"someone is on it" while in progress; the task lock does. After
closing the bead, release the lock.

For non-BEADS work items (a GitHub PR, a draft design report you
haven't filed yet), the bracketed token can name them:
`'[pr:42]'`, `'[draft:role-redesign]'`. The helper doesn't validate
the token — it's an exact-match identifier; conflicts are exact
collisions.

## Release Flow

When the active work ends or narrows, update the lock immediately.

```sh
tools/orchestrate release <role>
```

This clears the role's active scopes and lists the current open BEADS tasks.

## Status

```sh
tools/orchestrate status
```

Lists every role's lock file plus open BEADS tasks in the current
shell-helper era. In the typed target, `RoleObservation` reports role
state and `QueryKind::Ready` reports ready work from the native mind graph.

## Blocked Work

When an agent cannot proceed because a scope is owned, context is missing, or
a dependency is not ready, it records blocked work durably.

Current shell-helper era:

```sh
bd create "Short task title" -t task -p 2 \
  --description "Why this is blocked and what should happen next"
```

Keep BEADS entries short. Long designs, reports, and protocols live as files;
the bead points at the file or path.

Typed target:

- Create or update a `signal-persona-mind` item.
- Add a `Blocks`, `DiscoveredFrom`, `References`, or `RelatesTo` edge as
  appropriate.
- Add notes as append-only mind graph events.
- Use imported BEADS IDs only as aliases.

## Legacy BEADS Check

Every lock write includes an open-task check. Agents should read the
open-task list as part of deciding whether to continue, pick up a blocked
item, or leave context for another agent.

BEADS is not part of the claim/release surface. Agents do not claim `.beads/`
before writing tasks, comments, state changes, or closures. If the current
storage backend reports an exclusive database-lock error, treat that as
transient backend contention only — not as another agent owning BEADS. Retry the
BEADS command as the next natural action, or switch the workspace to a backend
that supports concurrent access. Do not create an orchestration lock for
`.beads/`.

This section describes the legacy helper behavior only. New design work should
target `signal-persona-mind`; do not add new BEADS integrations.

Useful direct commands:

```sh
bd list --status open --flat --no-pager --limit 20
bd ready
bd show <id>
bd close <id> --reason "<what changed>"
```

## Version Control

Li repositories and forks are Git-backed colocated Jujutsu repositories. If a
Git-backed Li repo lacks `.jj/`, claim the repo and run:

```sh
jj git init --colocate
```

Use `jj` for local history work. Git remains the compatibility layer for
remotes and storage.

## Reports

The `reports/` directory is **exempt from the claim/release flow**. All agents
should be able to write reports at any time without coordinating a lock.

Convention: each role owns a subdirectory.

- `reports/operator/` — operator's reports.
- `reports/operator-assistant/` — operator assistant's reports.
- `reports/designer/` — designer's reports.
- `reports/designer-assistant/` — designer assistant's reports.
- `reports/system-specialist/` — system specialist's reports.
- `reports/poet/` — poet's reports.

Each role writes only into its own role subdirectory. Other roles may
**read** any report freely; if they want to **build on** another role's
report, they rewrite the relevant content in a new report inside their own
subdirectory rather than editing the original.

The role subdirectories are *permanently owned* by their role. Treating
them as role-private write zones removes the report path from the
coordination surface — reports are how roles communicate without racing.

For *how* to write a report (filename convention, prose-plus-visuals
medium, tone in chat replies, always-name-paths rule), see this
workspace's `skills/reporting.md`. This protocol covers only the
role-coordination side.

## Overrides

The user may explicitly grant a one-job override that lets an agent bypass
the claim flow for a specific edit. Overrides are **named at the call
site** ("you have an override for this one job; you don't have to check
the lock file"). They do not persist beyond the named scope. After the
override scope completes, the normal claim/release protocol resumes.
