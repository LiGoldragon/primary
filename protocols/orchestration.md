# Orchestration Protocol

The orchestration protocol coordinates autonomous agents sharing the same
workspace. It combines role-owned lock files with the workspace BEADS task
database so agents see both file ownership and open work before they edit.

## Roles

- Codex acts as `operator`.
- Claude acts as `designer`.
- Each agent must know its role before claiming work.

## Coordination State

- Operator lock: `operator.lock`
- Designer lock: `designer.lock`
- BEADS database: `.beads/`
- Helper: `tools/orchestrate`

Each agent edits only its own lock file. The operator edits
`operator.lock`; the designer edits `designer.lock`. The lock files are
coordination records, not operating-system locks.

## Claim Flow

Before editing files or running commands that create, modify, format, or
delete files, an agent claims its intended scope.

Use:

```sh
tools/orchestrate claim <operator|designer> <absolute-path> [more-paths] -- <reason>
```

The helper performs the required work in one call:

1. Writes the intended scope into the agent's own lock file with an
   `Updated-at` timestamp.
2. Reads both lock files.
3. Lists open BEADS tasks.
4. Checks the other active lock for exact or nested path overlap.
5. Clears the agent's claim and exits non-zero if overlap exists.

Use absolute paths where possible. For linked repositories under `repos/`,
claim the real repository path under `/git/...`, not only the symlink path. A
whole repository may be claimed by listing its repository root path.

## Release Flow

When the active work ends or narrows, update the lock immediately.

```sh
tools/orchestrate release <operator|designer>
```

This clears the agent's active scopes and lists the current open BEADS tasks.

## Blocked Work

When an agent cannot proceed because a scope is owned, context is missing, or a
dependency is not ready, it records the blocked work as a BEADS task.

```sh
bd create "Short task title" -t task -p 2 \
  --description "Why this is blocked and what should happen next"
```

Keep BEADS entries short. Long designs, reports, and protocols live as files;
the bead points at the file or path.

## BEADS Check

Every lock write includes an open-task check. Agents should read the open-task
list as part of deciding whether to continue, pick up a blocked item, or leave
context for another agent.

Do not run multiple BEADS commands in parallel from the same workspace. The
embedded backend uses a local database lock; the orchestration helper is the
single coordination read for claim/release checks.

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

Convention: each agent role owns a subdirectory.

- `reports/designer/` — designer's reports.
- `reports/operator/` — operator's reports.
- (New roles get their own subdirectory when introduced.)

Each agent writes only into its own role subdirectory. Other agents may
**read** any report freely; if they want to **build on** another agent's
report, they rewrite the relevant content in a new report inside their own
subdirectory rather than editing the original.

The role subdirectories are *permanently owned* by their role. Treating
them as agent-private write zones removes the report path from the
coordination surface — reports are how agents communicate without racing.

Filename convention inside a role subdirectory is open. The
`YYYY-MM-DD-<topic>.md` shape that the workspace already uses elsewhere is
recommended; the date keeps reports sortable and prevents collisions.

## Overrides

The user may explicitly grant a one-job override that lets an agent bypass
the claim flow for a specific edit. Overrides are **named at the call
site** ("you have an override for this one job; you don't have to check
the lock file"). They do not persist beyond the named scope. After the
override scope completes, the normal claim/release protocol resumes.
