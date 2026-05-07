# Orchestration Protocol

The orchestration protocol coordinates autonomous agents sharing the same
workspace. It combines role-owned lock files with the workspace BEADS task
database so agents see both file ownership and open work before they edit.
BEADS is shared coordination state, not a lockable scope.

## Roles

The workspace recognises four coordination roles. Each role has its own lock
file, its own report subdirectory, and a natural primary scope.

| Role | Default agent | Lock file | Reports subdir | Natural primary scope |
|---|---|---|---|---|
| `operator` | Codex | `operator.lock` | `reports/operator/` | Rust crates, persona, sema-ecosystem implementation |
| `designer` | Claude | `designer.lock` | `reports/designer/` | ESSENCE, AGENTS, lore, skills, design reports |
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
- BEADS database: `.beads/`.
- Helper: `tools/orchestrate`.

Each agent writes only its own lock file. The lock files are coordination
records, not operating-system locks.

`.beads/` is never claimed. Any agent may create, update, comment on, or close
BEADS tasks at any time. A BEADS task is a shared work item, not a file-ownership
claim.

## Claim Flow

Before editing files or running commands that create, modify, format, or
delete files, an agent claims its intended scope.

```sh
tools/orchestrate claim <role> <absolute-path> [more-paths] -- <reason>
```

`<role>` is one of `operator`, `designer`, `system-specialist`, `poet`.

The helper performs the required work in one call:

1. Writes the intended scope into the role's own lock file with an
   `Updated-at` timestamp.
2. Reads every role's lock file.
3. Lists open BEADS tasks.
4. Checks every other active lock for exact or nested path overlap.
5. Clears the role's claim and exits non-zero if any overlap exists.

Use absolute paths where possible. For linked repositories under `repos/`,
claim the real repository path under `/git/...`, not only the symlink path. A
whole repository may be claimed by listing its repository root path.

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

Lists every role's lock file plus the open BEADS tasks. Useful before
starting work to see what other roles are doing.

## Blocked Work

When an agent cannot proceed because a scope is owned, context is missing, or
a dependency is not ready, it records the blocked work as a BEADS task.

```sh
bd create "Short task title" -t task -p 2 \
  --description "Why this is blocked and what should happen next"
```

Keep BEADS entries short. Long designs, reports, and protocols live as files;
the bead points at the file or path.

## BEADS Check

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
- `reports/designer/` — designer's reports.
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
