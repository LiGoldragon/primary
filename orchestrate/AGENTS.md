# Orchestration Protocol

The orchestration protocol coordinates autonomous agents sharing the same
workspace. The live implementation is the `orchestrate` component CLI: it takes
one NOTA request, submits typed `signal-orchestrate` frames to
`orchestrate-daemon` over Unix sockets, and prints one NOTA reply. Lock files
are daemon projections for local visibility only.

The daemon-owned store is `orchestrate/orchestrate.redb`. Lock files are
visibility projections, not the source of truth. BEADS is shared coordination
state while it exists, not a lockable scope.

Agents should treat the current production surface as the daemon-backed
`orchestrate` CLI and its NOTA records, not as an argv compatibility helper or
as a shell helper that owns files directly.

## Disciplines and lanes

A **discipline** is persistent metadata: it loads the lane's skills, its
authority class, and its persistent persona identity (persona-mind memory,
signing key). A discipline is not a directory and not a session. There are
**nine disciplines**:

- `designer` — architecture, skills, reports
- `operator` — implementation
- `system-operator` — OS / platform / deploy
- `system-maintainer` — Crayon OS and Logic maintenance, debugging, deploy
- `poet` — writing as craft
- `editor` — source-grounded research, quotation, synthesis
- `videographer` — video as craft
- `assistant` — personal-affairs support for the psyche
- `counselor` — personal-affairs advisory, paired with assistant

A **lane** is a unique work-*session* identity named for that session's
intent (e.g. `newLanesDesign`, `schemaWorkAudit`) — not a fixed role name.
A lane carries its discipline as metadata; in the orchestrate registry the
lane's role is a NOTA vector whose **last token is the base discipline**,
preceding tokens are specializations: `[NewLanesDesign Designer]`,
`[SchemaWorkAudit Operator]`. The lane is ephemeral and disposable; the
discipline (and the persona behind it) persists.

The old fixed role-lanes (`operator`, `second-operator`,
`cluster-operator`, `schema-designer`, …) and ordinal / qualifier lane
shapes are **retired as the lane model**; the disciplines they named
survive as discipline metadata. Lanes are now **registered per session**,
not enumerated in this file. The lane mechanism is canonical in
`skills/session-lanes.md`.

### Registering and observing lanes

The daemon already supports dynamic lanes (`src/lane.rs`,
`src/execution.rs`). A session registers its lane, the workspace observes
active lanes, and a drained lane is retired — all through the `orchestrate`
CLI's typed NOTA records.

```sh
# Register a session lane. Role is a NOTA vector of identifier tokens whose
# last token is the discipline; LaneAuthority is Structural or Support.
orchestrate "(Register ([NewLanesDesign Designer] Structural))"
# -> (LaneRegistered (newLanesDesign [NewLanesDesign Designer] Structural))

# Observe the live lane registry.
orchestrate "(Observe Lanes)"
# -> (LanesObserved [ ...(LaneRegistration LaneIdentifier Role LaneAuthority)... ])

# Retire a drained lane by its lane identifier.
orchestrate "(Retire (Lane newLanesDesign))"
# -> (LaneRetired newLanesDesign)
```

The schema shapes (from `orchestrate/schema/orchestrate-v0-1.schema` and
`orchestrate-types-v0-1.schema`):

- `Register [LaneRegistrationRequest]`, `LaneRegistrationRequest (Role
  LaneAuthority)`, `Role ((Vec RoleToken))`, `LaneAuthority [Structural
  Support]` → `LaneRegistered (LaneRegistration)`.
- `Observe Lanes` → `LanesObserved ((Vec LaneRegistration))`,
  `LaneRegistration (LaneIdentifier Role LaneAuthority)`.
- `Retire [Retirement]`, `Retirement [(Role RetireRoleOrder) (Lane
  LaneIdentifier)]` → `LaneRetired (LaneIdentifier)`.

`LanesObserved` is the live index of **active** lanes; the append-only
`protocols/retired-lanes.md` indexes drained ones.

The harness names a session's lane; an agent learns its lane and discipline
from the harness, not from this file. Each agent claims and releases under
its own session lane and edits only its own lock file.

## Coordination State

- Lock files: one per active session lane at `orchestrate/<lane>.lock`
  (e.g. `orchestrate/newLanesDesign.lock`), where `<lane>` is the
  session-intent name. The daemon projects these from claim state.
- BEADS database: `.beads/` (legacy transitional work-item store).
- CLI: `orchestrate` with one NOTA request argument.

Agents do not edit lock files as the normal path. They use `orchestrate`; the
daemon mutates typed claim state and projects each lane's lock file. The lock
files are coordination records, not operating-system locks.

`.beads/` is never claimed. Any agent may create, update, comment on, or close
BEADS tasks at any time. A BEADS task is a shared work item, not a file-ownership
claim.

### Exempt from the claim flow

One surface is written without claiming a lock:

- **Reports.** Each session lane writes only into its own
  `reports/<lane>/` session directory; session directories don't overlap,
  so no coordination is needed. Do not claim `/home/li/primary`,
  `reports/`, or a session report path just to create, edit, correct,
  supersede, or delete a report in your own lane. If the same task also
  edits shared files — skills, `AGENTS.md`, repo `INTENT.md`, code,
  schemas — claim those shared paths for the non-report edits.

**Lock selectively — never the whole space** (psyche record 2586). When a
task does need a claim, claim only the specific files or subfolders you will
edit — never `/home/li/primary` or a whole directory. Over-locking the whole
workspace is a root cause of the branch-dancing on primary: an agent that
locks everything then forks for its push instead of just committing to
`main`. Lock narrowly; work on `main`.

**Component migrations lock one component at a time** (Spirit record
`cb0j`, one-component lock discipline for component migrations). A fleet-wide
migration does not justify claiming the whole fleet. Claim the next component
or directly coupled contract pair, migrate it, commit and push it, release the
lock, then claim the next component. This keeps unrelated component owners and
lanes moving while the migration advances one bounded surface at a time.

**Reports never need a lock** — agents keep forgetting this, so it bears
repeating: a report in your own lane is created, edited, superseded, or
deleted with no claim at all. A lane writes **only** in its own
`reports/<lane>/`, never another lane's session directory — except a
one-time explicit psyche instruction for a specific task, and never touched
again after unless re-instructed (record 2587).

**Commit the whole working copy eagerly and impersonally** (records 2589,
2620). Keeping primary clean is everyone's job: if you see uncommitted
reports or edits sitting in the working copy, just commit them to `main` —
the **entire** working copy via `jj commit` with no path arguments, not only
your own paths — briefly noting the contents. Path-scoped commits leave
peers' changes undrained in the shared copy and let two agents fork off the
same base; committing everything drains the copy and keeps history linear.
Committing is janitorial and does not belong to a report's creator; the
multi-lane / impersonal commit is accepted. Full flow: `skills/jj.md`
§"Commit the whole working copy — never path-scoped".

Intent capture is no longer a file append surface. Recording psyche
intent goes through the deployed `spirit` CLI per `skills/intent-log.md`
and `skills/spirit-cli.md`. There is no legacy-file fallback; the
`intent/*.nota` substrate is retired (its history lives in git).

### Daemon CLI

The current production surface is the `orchestrate` component CLI speaking
NOTA directly to `orchestrate-daemon`:

```sh
orchestrate "(Claim (newLanesDesign [(Path /home/li/primary/AGENTS.md)] [refresh coordination docs]))"
orchestrate "(Release newLanesDesign)"
orchestrate "(Observe Lanes)"
orchestrate "(Observe Worktrees)"
orchestrate "(Query (20 []))"
```

The CLI takes exactly one NOTA argument and prints exactly one NOTA reply.
`orchestrate-daemon` is the only writer of durable claim state. On first
startup, the daemon imports existing `orchestrate/*.lock` files if
`orchestrate.redb` has no claims; after that, lock files are downstream
projections.

The old argv-compatible `tools/orchestrate claim|release|status` helper is
retired. Do not extend or rely on it; use the component CLI and its typed NOTA
records.

### Lock-file format

Each lock file is plain text. Each line is **one scope**, optionally
followed by `# reason`. An empty file means the lane is idle.

A **scope** is one of two kinds:

- **Path lock** — an absolute path. Coordinates editing of files/dirs
  on disk. Overlap rule: a path lock conflicts with another path lock
  if they're equal or nested.
- **Task lock** — a bracketed token like `[primary-f99]`. Coordinates
  *who is actively working on* a BEADS task (or any other named work
  item the bracketed token identifies). Overlap rule: exact match.

```
/home/li/primary/skills/autonomous-agent.md # sync coordination docs
[primary-f99] # chroma nota-codec migration
```

The two kinds are independent: a path lock and a task lock never
conflict, and a single role can hold both at once (e.g. claim the
task plus the specific paths the task requires).

The filename names the session lane; nothing else needs to live in the
file. To inspect, run `orchestrate "(Observe Lanes)"` or read the projected
`orchestrate/<lane>.lock` file for a local human-readable view. The daemon is
the canonical writer after startup; agents use the `orchestrate` CLI rather
than editing lock files by hand. Manual lock-file edits are legacy recovery
only, before the daemon imports an empty store.

Lock files are **runtime state, gitignored.** They live on the local
filesystem only — coordination between agents on the same machine, not
versioned history. A clean checkout starts with no lock files; the daemon
projects them on first accepted claim. Don't commit them, don't expect them to
travel between machines.

## Claim Flow

Before editing files, running commands that create/modify/delete files, or
taking on a tracked unit of work, an agent claims its intended scope.

```sh
orchestrate "(Claim (<lane> [(Path /absolute/path) (Task primary-f99)] [reason text]))"
```

`<lane>` is **the registered session lane** — the session-intent name this
agent is running under (`newLanesDesign`, `schemaWorkAudit`), discipline-tagged
in the registry by the last token of its role vector. It is not a fixed role
name; observe the active set with `orchestrate "(Observe Lanes)"`. Each scope
is either `(Path /absolute/path)` or `(Task primary-f99)`. The claim names
*who is acting* (the lane); the scope names *what* (paths / tasks) — the scope
mechanism is unchanged.

Mix freely:

```sh
orchestrate "(Claim (schemaWorkAudit [(Task primary-f99) (Path /git/github.com/LiGoldragon/chroma)] [chroma nota-codec migration]))"
```

The daemon performs the required work in one call:

1. Accepts the typed claim request through `signal-orchestrate`.
2. Checks every other active claim for overlap (path nesting for path locks;
   exact match for task locks).
3. Commits accepted claim state to `orchestrate.redb`.
4. Regenerates `orchestrate/<lane>.lock` projections from daemon state.
5. Returns `(ClaimAcceptance ...)` or `(ClaimRejection ...)` as NOTA.

Use absolute paths where possible. For linked repositories under `repos/`,
claim the real repository path under `/git/...`, not only the symlink path. A
whole repository may be claimed by listing its repository root path.

### When to use a task lock

Task locks bridge BEADS' lifecycle (filed → open → closed) to in-flight
coordination ("who is working on this *right now*"). Use one when you
take on a tracked task that other agents might otherwise also pick up:

```sh
orchestrate "(Claim (schemaWorkAudit [(Task primary-f99)] [chroma migration]))"
# … do the work …
orchestrate "(Release schemaWorkAudit)"
bd close primary-f99 -r "<closing note>"
```

A bead going from open → closed in BEADS doesn't tell other agents
"someone is on it" while in progress; the task lock does. After
closing the bead, release the lock.

For non-BEADS work items (a GitHub PR, a draft design report you
haven't filed yet), the task token can name them: `(Task pr:42)`,
`(Task draft:role-redesign)`. The daemon treats task tokens as exact-match
identifiers; conflicts are exact collisions.

## Release Flow

When the active work ends or narrows, update the lock immediately.

```sh
orchestrate "(Release <lane>)"
```

This clears the lane's active scopes and lists the current open BEADS tasks.
Release first checks any tracked repository touched by the lane's path claims
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
orchestrate "(Observe Lanes)"
orchestrate "(Observe Roles)"
orchestrate "(Observe Worktrees)"
```

`Observe Lanes` returns `LanesObserved` — the snapshot of active registered
session lanes, each a `(LaneRegistration LaneIdentifier Role LaneAuthority)`.
`Observe Roles` returns the active claim snapshot as NOTA. Open BEADS tasks
remain in BEADS; the orchestrate component does not own the BEADS database.

## JJ Bookmark Verification

```sh
orchestrate "(Observe Worktrees)"
```

The old `verify-jj` compatibility command belonged to the retired helper. The
daemon-native replacement surface is the typed worktree registry observed with
`Observe Worktrees`; repository hygiene that is not yet daemon-modeled should
be handled by the relevant repo's normal `jj` commands and reports, not by
keeping the compatibility helper alive.


Scans the repositories named by `protocols/active-repositories.md`; it does
not crawl the filesystem. For each tracked repository, it counts local
`push-*` bookmarks, flags bookmarks already merged to `main` as delete
candidates, flags unmerged bookmarks older than seven days as
rebase-or-abandon candidates, and names local-only unmerged bookmarks that
would block `release` for a lane claiming that repository.

## Blocked Work

When an agent cannot proceed because a scope is owned, context is missing, or
a dependency is not ready, it records blocked work durably.

Legacy shell-helper era:

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

As of 2026-05-19 (per psyche 2026-05-19), beads do
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

Lock files are different. Each session lane edits its own lock file —
locks name *who is actively touching what files right now*, which is
per-lane. Two lanes in the same discipline can hold different lock
scopes at the same time without conflict; one bead can be claimed by
whichever lane picked it up.

The mind-graph destination (per "Command-line mind target" above)
preserves this: typed work items in `mind.redb` route by the lane's
**discipline** identity (its persistent persona-mind), not by the
ephemeral session-lane name. Several concurrent session lanes in the
same discipline all write into that one persona's mind.

## Version Control

Li repositories and forks are Git-backed colocated Jujutsu repositories. If a
Git-backed Li repo lacks `.jj/`, claim the repo and run:

```sh
jj git init --colocate
```

Use `jj` for local history work. Git remains the compatibility layer for
remotes and storage.

## Reports

Reports live under **`reports/<lane>/`** where `<lane>` is the
session-intent name — a **session directory**, one per active lane (e.g.
`reports/newLanesDesign/`), not a permanent per-role directory. Numbering is
per-lane. A report is written as a **fresh-context pickup point**: an agent
starting from a clean context can pick the work up, reason about it, and —
where it is implementable — implement it; implementable work is linked into a
bead dependency graph (`bd dep <blocker> --blocks <blocked>`).

The `reports/` directory is **exempt from the claim/release flow** because
each session lane owns its own session directory and these do not overlap.
Do not claim report paths in your own lane, and do not add your own report
files to a lock file. This includes fresh report corrections and
context-maintenance edits: the session directory itself is the lock. Claim
only the shared non-report surfaces touched by the same work.

Each lane writes only into its own session directory. Other lanes may
**read** any public report freely; to **build on** another lane's report,
rewrite the relevant content in a new report inside your own session
directory rather than editing the original. A continuation or review report
states explicitly what it supersedes and deletes its predecessor in the same
commit. Private assistant/counselor report substance goes in
`private-repos/assistant-reports/` or `private-repos/counselor-reports/` and
requires the access gate in `skills/privacy.md` before even reading.

### Drain and retire

At session close the lane **drains** via the three-fate disposition: every
idea routes to exactly one of — **intent** (captured via the Spirit CLI),
**work** (a bead linked into the dependency graph), or **abandon**
(already-landed / stale / wrong; git preserves it). When a lane has drained,
**delete its session directory** — git history and the session transcript are
the archive — and record the retirement in the single append-only registry
`protocols/retired-lanes.md`: one entry per retired lane carrying the lane
name, discipline, the git revision range holding its reports, a transcript
pointer, the drain date, and a one-line statement of what it decided. Retire
the lane in the daemon with `orchestrate "(Retire (Lane <lane>))"`.

`LanesObserved` (from `orchestrate "(Observe Lanes)"`) is the live index of
**active** lanes; `protocols/retired-lanes.md` is the thin index of drained
ones — together they keep every session discoverable for
regression / model-behavior forensics without re-growing the working report
tree. The full lane lifecycle is canonical in `skills/session-lanes.md`.

For *how* to write a report (filename convention, prose-plus-visuals medium,
tone in chat replies, always-name-paths rule), see this workspace's
`skills/reporting.md`. This protocol covers only the lane-coordination side.

## Overrides

The user may explicitly grant a one-job override that lets an agent bypass
the claim flow for a specific edit. Overrides are **named at the call
site** ("you have an override for this one job; you don't have to check
the lock file"). They do not persist beyond the named scope. After the
override scope completes, the normal claim/release protocol resumes.
