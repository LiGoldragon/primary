# Orchestration Protocol

The orchestration protocol coordinates autonomous agents sharing the same
workspace. The live implementation is the `orchestrate` component CLI: it takes
one DOTOS request, submits typed `signal-orchestrate` frames to
`orchestrate-daemon` over Unix sockets, and prints one DOTOS reply. Lock files
are daemon projections for local visibility only.

The daemon-owned store is `orchestrate/orchestrate.redb`. Lock files are
visibility projections, not the source of truth. BEADS is shared coordination
state while it exists, not a lockable scope.

Agents should treat the current production surface as the daemon-backed
`orchestrate` CLI and its DOTOS records, not as an argv compatibility helper or
as a shell helper that owns files directly.

## Disciplines and lanes

A **discipline** is persistent metadata: it loads the lane's skills, its
authority class, and its persistent persona identity (mind memory,
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
intent (e.g. `newLanesDesign`, `schemaWorkAudit`).
A lane carries its discipline as metadata; in the orchestrate registry the
lane's role is a DOTOS vector whose **last token is the base discipline**,
preceding tokens are specializations: `[NewLanesDesign Designer]`,
`[SchemaWorkAudit Operator]`. The lane is ephemeral and disposable; the
discipline (and the persona behind it) persists.

Lanes are **registered per session**, not enumerated in this file. The lane
mechanism is canonical in `.claude/skills/session-lanes/SKILL.md`.

### Registering and observing lanes

The daemon already supports dynamic lanes (`src/lane.rs`,
`src/execution.rs`). A session registers and retires its lane through the
`meta-orchestrate` CLI; the ordinary `orchestrate` CLI observes active lanes.

```sh
# Register a session lane. Register is nested exactly as
#   (Register ((SESSION LANE ([ROLE TOKENS] AUTHORITY) [DETAILS]) MODE))
# SESSION is CamelCase; LANE is the session-intent identifier; the role
# vector's last token is the discipline; AUTHORITY is Structural or Support;
# MODE is Fresh or Recovery. DETAILS is free text: bracket it when it is
# several words, and write a single word as a bare atom.
meta-orchestrate "(Register ((NewLanesDesign newLanesDesign ([NewLanesDesign Designer] Structural) [refresh coordination docs]) Fresh))"
# -> (LaneRegistered ((NewLanesDesign newLanesDesign ([NewLanesDesign Designer] Structural) [refresh coordination docs]) <nanos> Active))

# Observe the live lane registry.
orchestrate "(Observe Lanes)"
# -> LanesObserved.[{Session Lane Active <nanos> <age> [...activity...]}]

# Retire a drained lane by its lane identifier.
meta-orchestrate "(Retire (Lane newLanesDesign))"
# -> (LaneRetired newLanesDesign)
```

The schema shapes below are the **deployed** contract — `signal-orchestrate`
0.10.1 (rev `d5ecda9`) and `meta-signal-orchestrate` 0.5.0 (rev `c3ba5567`),
the revisions `orchestrate` 0.16.0 is pinned to in its `Cargo.lock`. Read the
pinned schema, not a local `repos/signal-orchestrate` checkout: that checkout
is an older line (0.5.0) and its reply shapes differ from what the daemon
actually speaks.

- `Register [LaneRegistrationRequest]`, `LaneRegistrationRequest
  (LaneAssignment LaneRegistrationMode)`, `LaneAssignment (SessionIdentifier
  LaneIdentifier LaneOwner LaneDetails)`, `LaneOwner (Role LaneAuthority)`,
  `Role ((Vec RoleToken))`, `LaneAuthority [Structural Support]`,
  `LaneRegistrationMode [Fresh Recovery]` -> `LaneRegistered (LaneRegistration)`.
- `Observe Lanes` -> `LanesObserved ((Vec LaneProjection))`, `LaneProjection
  (LaneRegistration (Vec LaneResourceClaim) TimestampNanos DurationNanos)`,
  `LaneResourceClaim (ScopeReference ScopeReason TimestampNanos
  DurationNanos)`.
- `Retire [Retirement]`, `Retirement [(Role RetireRoleOrder) (Lane
  LaneIdentifier)]` -> `LaneRetired (LaneIdentifier)`.
- `Claim [RoleClaim]`, `RoleClaim (RoleName (Vec ScopeReference)
  ScopeReason)`, `ScopeReference [(Path WirePath) (Task TaskToken)]` ->
  `ClaimAcceptance` or `ClaimRejection`. All three fields are required.
- `Release [RoleRelease]`, `RoleRelease RoleName` ->
  `ReleaseAcknowledgment (RoleName (Vec ScopeReference) (Vec Worktree))`.
  The third field is the lane's still-open worktrees: release reports them
  rather than silently dropping them, so read it before assuming a lane is
  fully drained.
- `RequestWorktree [WorktreeRequest]`, `WorktreeRequest (RepositoryName
  BranchName LaneName PurposeText)` -> `WorktreeScaffolded (Worktree)` or
  `WorktreeRequestRejected`. `Worktree (RepositoryName BranchName WirePath
  LaneName WorktreeStatus PurposeText TimestampNanos PushedState)`.
- `ConcludeWorktree [WorktreeConclusionRequest]`, `WorktreeConclusionRequest
  (LaneName WorktreeConclusion)`, `WorktreeConclusion [Merged Rejected]` ->
  `WorktreeConcluded (Worktree MainIntegration)` or
  `WorktreeTeardownRefused (Worktree TeardownRefusal)`.
- `RepositoryMainContended (RepositoryName RoleName ScopeReason DurationNanos
  FeatureWorktree)`, `FeatureWorktree [(Scaffolded Worktree) (Existing
  Worktree)]` — the reply when another lane holds a repository's `main`. It
  names the worktree you should work in instead, so treat it as a redirect,
  not a plain rejection.
- `Observation [Roles Sessions (SessionLanes SessionIdentifier) Lanes
  Worktrees Repositories Topics (Topic OrchestratorTopicPath) Agents]`.

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
- CLI: `orchestrate` with one DOTOS request argument.

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
  so no coordination is needed. Do not claim the workspace root,
  `reports/`, or a session report path just to create, edit, correct,
  supersede, or delete a report in your own lane. If the same task also
  edits shared files — skills, `AGENTS.md`, repo `ARCHITECTURE.md`, code,
  schemas — claim those shared paths for the non-report edits.

**Lock selectively — never the whole space** (psyche record 2586). When a
task does need a claim, claim only the specific files or subfolders you will
edit — never the workspace root or a whole directory. Over-locking the whole
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
multi-lane / impersonal commit is accepted.

Recording psyche intent goes through the deployed `spirit` CLI per
`.claude/skills/spirit-log/SKILL.md` and
`.claude/skills/spirit-cli/SKILL.md`.

### Daemon CLI

The current production surface for ordinary claim/release/observe work is the
`orchestrate` component CLI speaking DOTOS directly to `orchestrate-daemon`:

```sh
orchestrate "(Claim (newLanesDesign [(Path /absolute/path/to/workspace/AGENTS.md)] [refresh coordination docs]))"
orchestrate "(Release newLanesDesign)"
orchestrate "(Observe Lanes)"
orchestrate "(Observe Worktrees)"
orchestrate "(Query (20 []))"
```

The ordinary and meta CLIs each take exactly one DOTOS argument and print exactly
one DOTOS reply. Meta-policy requests such as `Register`, `Retire`,
`RegisterWorktree`, and `RefreshWorktreeIndex` use `meta-orchestrate`.
`orchestrate-daemon` is the only writer of durable claim state. On first
startup, the daemon imports existing `orchestrate/*.lock` files if
`orchestrate.redb` has no claims; after that, lock files are downstream
projections.

Use the component CLI and its typed DOTOS records for claim, release, observe,
and query work.

### Verbs an ordinary agent needs

The shapes below are the ones the deployed `orchestrate` 0.16.0 CLIs actually
accept, verified by running each against the live daemon.

Free-text fields — lane details, claim reasons, worktree purposes — follow the
canonical DOTOS atom rule: **bracket multi-word text, write a single word as a
bare atom**. `[why this lane exists]` and `probe` both parse; `[probe]` does
not, and fails with `non-canonical string delimiter for "probe": use probe`.

```sh
# Lane lifecycle (meta CLI).
meta-orchestrate "(Register ((<Session> <lane> ([<Role Tokens>] Structural) [<why this lane>]) Fresh))"
meta-orchestrate "(Retire (Lane <lane>))"

# Claim takes three fields: lane, scope vector, reason. The reason is not
# optional — omitting it is a parse error.
orchestrate "(Claim (<lane> [(Path /absolute/path) (Task primary-f99)] [<why>]))"

# Release takes the bare lane identifier and clears all of its scopes.
# It does not take a scope vector.
orchestrate "(Release <lane>)"
# -> (ReleaseAcknowledgment (<lane> [<released scopes>] [<still-open worktrees>]))

# Worktrees. RequestWorktree takes four fields — repository, branch,
# owning lane, purpose — and the daemon mints the path.
orchestrate "(RequestWorktree (<repo> <branch> <lane> [<purpose>]))"
# -> (WorktreeScaffolded (<repo> <branch> /absolute/path <lane> Active [<purpose>] <nanos> <push-state>))
# -> (WorktreeRequestRejected RepositoryNotFound) when no such checkout exists.

# ConcludeWorktree takes two fields: the owning lane and the disposition,
# which is Merged or Rejected. Merged is gated on the work being an
# ancestor of main; a blocked teardown replies WorktreeTeardownRefused.
orchestrate "(ConcludeWorktree (<lane> Merged))"

# Orchestrator agent seats. MintAgentIdentity allocates the identity,
# LaunchAgent starts the harness process for an already-minted identity,
# and SendOrchestratorMessage routes one message to an agent or to the
# orchestrator itself.
orchestrate "(MintAgentIdentity (<Session> [<mission description>] Claude))"
# -> (AgentIdentityMinted <agent-id>)
orchestrate "(LaunchAgent <agent-id>)"
# -> (AgentLaunched (<agent-id> <pid> <optional log path>))
# -> (AgentLaunchRefused (<agent-id> [UnknownAgent AgentNotAllocated
#      HarnessUnreachable HarnessRefused] <detail>))
orchestrate "(SendOrchestratorMessage (<sender-id> (Agent <agent-id>) (<subject> <content>)))"
# -> (OrchestratorMessageRouted (<slot> [<recipients>] Submitted))
# -> (OrchestratorMessageRejected [NoEligibleRecipient SenderNotRegistered
#      MalformedPayload MissingCoordinator])

# Observation.
orchestrate "(Observe Lanes)"
orchestrate "(Observe Worktrees)"
orchestrate "(Observe Repositories)"
orchestrate "(Observe Roles)"
orchestrate "(Observe Agents)"
orchestrate "(Query (20 []))"
```

`MintAgentIdentity`, `LaunchAgent`, and `SendOrchestratorMessage` exist in the
deployed daemon (`orchestrate/src/execution.rs`) and in the pinned
`signal-orchestrate` 0.10.1 contract. They are absent from the older local
`repos/signal-orchestrate` checkout; that checkout is not the deployed source.

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
/absolute/path/to/workspace/orchestrate/AGENTS.md # sync coordination docs
[primary-f99] # chroma dotos migration
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

Exit status only tells you whether the request *parsed*. Malformed DOTOS exits
1; a request the daemon understood and **refused** still exits 0. So read the
reply record as well as the status: `ClaimAcceptance`, `ReleaseAcknowledgment`,
and `LaneRegistered` are success, while `ClaimRejection` and `PartialApplied`
are refusals that arrive with exit 0.

Mix freely:

```sh
orchestrate "(Claim (schemaWorkAudit [(Task primary-f99) (Path /absolute/path/to/chroma)] [chroma dotos migration]))"
```

The daemon performs the required work in one call:

1. Accepts the typed claim request through `signal-orchestrate`.
2. Checks every other active claim for overlap (path nesting for path locks;
   exact match for task locks).
3. Commits accepted claim state to `orchestrate.redb`.
4. Regenerates `orchestrate/<lane>.lock` projections from daemon state.
5. Returns `(ClaimAcceptance ...)` or `(ClaimRejection ...)` as DOTOS.

Use absolute paths where possible. Claim a repository by listing that
checkout's root path. Use `protocols/repos-manifest.dotos` for repository
identity; do not bake one machine's checkout root into guidance.

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
session lanes, each a `LaneProjection`.
`Observe Roles` returns the active claim snapshot as DOTOS. Open BEADS tasks
remain in BEADS; the orchestrate component does not own the BEADS database.

The ordinary way to get a feature worktree is `RequestWorktree`, which
scaffolds it and registers it in one call. `RegisterWorktree` on the meta CLI
is the back door for a worktree that already exists on disk and needs to be
added to the daemon's inventory:

```sh
meta-orchestrate "(RegisterWorktree (<repo> <branch> /absolute/path <lane> Active <purpose> <timestamp-nanos> Unpushed))"
```

`RegisterWorktree` takes the eight `Worktree` fields **positionally**. Do not
write a leading `Worktree` tag: `Worktree` is a positional record, not a
tagged union, and the tag makes it nine objects where the decoder wants eight
(`expected Worktree to hold 8 root objects, found 9`).

## JJ Bookmark Verification

```sh
orchestrate "(Observe Worktrees)"
```

The daemon-native verification surface is the typed worktree registry observed
with `Observe Worktrees`; repository hygiene that is not yet daemon-modeled is
handled by the relevant repo's normal `jj` commands and reports.


Reads `protocols/repos-manifest.dotos`, selects the records whose `lifecycle`
is `Active`, and iterates those repositories directly; it does not crawl the
filesystem, and it does not scope to the curated `active-repositories.md`
attention map (a subset that would reintroduce partial coverage). For each
such repository, it counts local `push-*` bookmarks, flags bookmarks already
merged to `main` as delete candidates, flags unmerged bookmarks older than
seven days as rebase-or-abandon candidates, and names local-only unmerged
bookmarks that would block `release` for a lane claiming that repository.

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

- Create or update a `signal-mind` item.
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

This section describes direct BEADS commands only. New design work should
target `signal-mind`; do not add new BEADS integrations.

Useful direct commands:

```sh
bd list --status open --flat --limit 20
bd ready
bd show <id>
bd close <id> --reason "<what changed>"
```

## Beads use topic labels

As of 2026-05-19 (per psyche 2026-05-19), any agent can pick up any bead based
on topic affinity rather than a prescribed lane.

When filing a bead: use **topic labels** (`dotos`, `persona`, `criome`,
`horizon`, etc.) so agents working in that topic find the bead via `bd ready`
or `bd list --label <topic>`.

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
**discipline** identity (its persistent mind), not by the
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
`private-repos/assistant-reports/` or `private-repos/counselor-reports/`; that
substance stays out of public reports, public Spirit records, public commits,
and chat per the leak gate in `.claude/skills/privacy/SKILL.md`.

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
the lane in the daemon with `meta-orchestrate "(Retire (Lane <lane>))"`.

`LanesObserved` (from `orchestrate "(Observe Lanes)"`) is the live index of
**active** lanes; `protocols/retired-lanes.md` is the thin index of drained
ones — together they keep every session discoverable for
regression / model-behavior forensics without re-growing the working report
tree. The full lane lifecycle is canonical in
`.claude/skills/session-lanes/SKILL.md`.

For *how* to write a report (filename convention, prose-plus-visuals medium,
tone in chat replies, always-name-paths rule), see this workspace's
`.claude/skills/reporting/SKILL.md`. This protocol covers only the
lane-coordination side.

## Overrides

The user may explicitly grant a one-job override that lets an agent bypass
the claim flow for a specific edit. Overrides are **named at the call
site** ("you have an override for this one job; you don't have to check
the lock file"). They do not persist beyond the named scope. After the
override scope completes, the normal claim/release protocol resumes.
