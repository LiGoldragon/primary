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

The workspace organises work under **four main roles**, each carrying its
own discipline. Additional **lanes** — `second-<role>`, `third-<role>`,
and qualified lanes like `<qualifier>-<role>` — share their main role's
discipline, skill file, and beads label; only the lock file, report
subdirectory, and claim string differ per lane. The lane mechanism is
canonical in `skills/role-lanes.md`.

Per spirit record 920 (Maximum, 2026-05-27): the prior `<role>-assistant`
and `<role>-specialist` suffixes are RETIRED workspace-wide. The current
set of lanes is enumerated below.

| Lane | Main role | Default agent | Lock file | Reports subdir | Natural primary scope |
|---|---|---|---|---|---|
| `operator` | operator | Codex | `orchestrate/operator.lock` | `reports/operator/` | Rust crates, persona, sema-ecosystem implementation |
| `second-operator` | operator | (any) | `orchestrate/second-operator.lock` | `reports/second-operator/` | Second parallel operator window |
| `pi-operator` | operator | Pi | `orchestrate/pi-operator.lock` | `reports/pi-operator/` | Pi-harness implementation window under operator discipline |
| `cluster-operator` | operator | Codex | `orchestrate/cluster-operator.lock` | `reports/cluster-operator/` | Live cluster maintenance, production deploy/update authority, and cluster-scoped implementation under operator discipline |
| `cloud-operator` | operator | (any) | `orchestrate/cloud-operator.lock` | `reports/cloud-operator/` | Cloud-deploy operator window — cloudflare and similar provider surfaces |
| `designer` | designer | Claude | `orchestrate/designer.lock` | `reports/designer/` | ESSENCE, AGENTS, lore, skills, design reports |
| `second-designer` | designer | (any) | `orchestrate/second-designer.lock` | `reports/second-designer/` | Second parallel designer window |
| `third-designer` | designer | (any) | `orchestrate/third-designer.lock` | `reports/third-designer/` | Third parallel designer window |
| `system-designer` | designer | (any) | `orchestrate/system-designer.lock` | `reports/system-designer/` | Specialized designer lane scoped to system topics (CriomOS, horizon, lojix, goldragon, deployment) |
| `nota-designer` | designer | (any) | `orchestrate/nota-designer.lock` | `reports/nota-designer/` | Specialized designer lane scoped to NOTA language design |
| `cloud-designer` | designer | (any) | `orchestrate/cloud-designer.lock` | `reports/cloud-designer/` | Specialized designer lane scoped to cloud component design |
| `system-operator` | system-operator | (any) | `orchestrate/system-operator.lock` | `reports/system-operator/` | CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon |
| `poet` | poet | (any) | `orchestrate/poet.lock` | `reports/poet/` | TheBookOfSol, substack-cli, prose-craft surfaces |

The "Default agent" column is convenience labelling for the lock file, not a
binding. Any agent may take any lane; the main role determines scope
authority, not which model holds it.

Each agent must know its lane before claiming work. Each agent edits only
its own lock file.

## Coordination State

- Lock files: one per lane at `orchestrate/<lane>.lock` (e.g.
  `orchestrate/operator.lock`, `orchestrate/system-operator.lock`).
- BEADS database: `.beads/` (legacy transitional work-item store).
- Helper: `tools/orchestrate`.

Each agent writes only its own lock file. The lock files are coordination
records, not operating-system locks.

`.beads/` is never claimed. Any agent may create, update, comment on, or close
BEADS tasks at any time. A BEADS task is a shared work item, not a file-ownership
claim.

### Exempt from the claim flow

One surface is written without claiming a lock:

- **Reports.** Each role writes only into its own `reports/<role>/`
  subdirectory; subdirs don't overlap, so no coordination is needed.

Intent capture is no longer a file append surface. Recording psyche
intent goes through the deployed `spirit` CLI per `skills/intent-log.md`
and `skills/spirit-cli.md`. Do not append to `intent/*.nota` during
normal work; those files are legacy history.

### Command-line mind target

The current implementation is the lock-file helper described below. The target
implementation is the Rust `mind` CLI backed by a long-lived `persona-mind`
daemon and the `signal-persona-mind` contract. `tools/orchestrate` remains the
compatibility helper name during migration.

Target surface:

```sh
mind "(<one NOTA request record>)"
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

The filename names the lane; nothing else needs to live in the file. To
inspect, `cat orchestrate/<lane>.lock` or `tools/orchestrate status`. The
helper is the canonical writer; agents may also edit lock files by hand as
long as the format is preserved.

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

`<role>` is one of `operator`, `second-operator`, `pi-operator`,
`cluster-operator`, `cloud-operator`, `designer`, `second-designer`,
`third-designer`, `system-designer`, `nota-designer`, `cloud-designer`,
`system-operator`, or `poet`.
Each `<scope>` is either an absolute path or a bracketed task lock
(`'[primary-f99]'` — quote it; `[` is a shell glob character).

Mix freely:

```sh
tools/orchestrate claim system-operator '[primary-f99]' \
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
tools/orchestrate claim system-operator '[primary-f99]' -- chroma migration
# … do the work …
tools/orchestrate release system-operator
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
Release first checks any tracked repository touched by the role's path claims
for local-only `push-*` bookmarks whose commits are not ancestors of `main`.
If it finds one, release refuses and leaves the lock in place until the commit
has a clear home: land it on `main`, push the bookmark, or deliberately
abandon/rebase the work.
Before release at the end of a non-trivial session, re-read any task bead you
claimed. Close it if the work shipped; otherwise update it with the blocker or
next action. The lock file is the live-edit surface; the bead is the durable
goal surface.

## Status

```sh
tools/orchestrate status
```

Lists every role's lock file plus open BEADS tasks in the current
shell-helper era. In the typed target, `RoleObservation` reports role
state and `QueryKind::Ready` reports ready work from the native mind graph.

## JJ Bookmark Verification

```sh
tools/orchestrate verify-jj
```

Scans the repositories named by `protocols/active-repositories.md`; it does
not crawl the filesystem. For each tracked repository, it counts local
`push-*` bookmarks, flags bookmarks already merged to `main` as delete
candidates, flags unmerged bookmarks older than seven days as
rebase-or-abandon candidates, and names local-only unmerged bookmarks that
would block `release` for a lane claiming that repository.

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
bd list --status open --flat --limit 20
bd ready
bd show <id>
bd close <id> --reason "<what changed>"
```

## Beads are not role-labeled

As of 2026-05-19 (psyche-stated in `intent/workspace.nota`), beads do
not carry `role:*` labels. Any agent can pick up any bead based on
topic affinity rather than a prescribed lane. The earlier
discipline-pool-via-role-label rule is retired.

When filing a bead: don't add a `role:*` label. Use **topic labels**
(`nota`, `persona`, `criome`, `horizon`, etc.) so agents working in
that topic find the bead via `bd ready` or `bd list --label <topic>`.

When picking up a bead: scan `bd ready` and pick by topic fit and
priority. Lane assignment is per-task judgment, not pre-labelled.

The motivation (per psyche 2026-05-19): keep a single agent on a
task/topic across what would previously have been multiple lane
handoffs — less context-shuffling, less ceremony.

Lock files are different. Each agent (main or assistant) edits its own
lock file — locks name *who is actively touching what files right now*,
which is per-agent. Two agents in the same discipline can hold different
lock scopes at the same time without conflict; one bead can be claimed at
the discipline pool level and worked by whichever agent picked it up.

The mind-graph destination (per "Command-line mind target" above)
preserves this: typed work items in `mind.redb` route by the main role's
identity, not the assistant's. Assistants act as additional capacity
under one role's identity.

## Version Control

Li repositories and forks are Git-backed colocated Jujutsu repositories. If a
Git-backed Li repo lacks `.jj/`, claim the repo and run:

```sh
jj git init --colocate
```

Use `jj` for local history work. Git remains the compatibility layer for
remotes and storage.

## Reports

The `reports/` directory is **exempt from the claim/release flow** because
reports are already partitioned by role lane. Each role's report subdirectory
is its implied write lock. Do not claim report paths in your own lane, and do
not add your own report files to a lock file.

Convention: each role owns a subdirectory.

- `reports/operator/` — operator's reports.
- `reports/second-operator/` — second operator's reports.
- `reports/pi-operator/` — Pi operator's reports.
- `reports/cluster-operator/` — cluster operator's reports.
- `reports/cloud-operator/` — cloud operator's reports.
- `reports/designer/` — designer's reports.
- `reports/second-designer/` — second designer's reports.
- `reports/third-designer/` — third designer's reports.
- `reports/system-operator/` — system operator's reports.
- `reports/system-designer/` — system designer's reports (specialized designer lane).
- `reports/nota-designer/` — nota designer's reports (specialized designer lane).
- `reports/cloud-designer/` — cloud designer's reports (specialized designer lane).
- `reports/poet/` — poet's reports.

Each role writes only into its own role subdirectory. Other roles may
**read** any report freely; if they want to **build on** another role's
report, they rewrite the relevant content in a new report inside their own
subdirectory rather than editing the original.

The role subdirectories are *permanently owned* by their role. The lock is
always implied by the lane itself, not by a line in `<role>.lock`. Treating
report lanes as role-private write zones removes report paths from the
coordination surface — reports are how roles communicate without racing.

Cross-lane report edits are exceptional. If the user explicitly asks a role to
edit, delete, or rewrite another role's report, that request is the named
override for that report edit. Otherwise, respond in your own lane.

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
