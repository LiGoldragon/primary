# 226 — Persona-orchestrate implementation shape

*Absorbs `/225`. The action: take orchestrate-cli the last 1cm and
land memory variants in persona-mind. Operator-ready slice plus the
memory schema operator implements against.*

---

## 0 · TL;DR

`persona-orchestrate` doesn't exist yet, and **shouldn't be stood up
today**. What does exist:

- **`persona-mind` is a real working daemon** — Kameo actors, Unix
  socket, sema-engine durability, dispatching `RoleClaim` /
  `RoleRelease` / `RoleObservation` / `RoleHandoff` /
  `ActivitySubmission` / `ActivityQuery` end-to-end. Smoke scripts
  prove it survives restart.
- **`signal-persona-mind` contract carries every record needed** for
  claim/release/status. No contract addition required for stage 1.
- **`orchestrate-cli` already projects every flow into typed
  `MindRequest`** — it just doesn't send the request anywhere. Lock
  files are written directly.

The shortest path to "persona-orchestrate does something real":
**finish wiring `orchestrate-cli` to actually send its already-typed
requests through the `persona-mind` socket.** The full
`persona-orchestrate` daemon (separate triad with its own contracts +
sema state) comes later, when memory routing pressure justifies it.

Memory schema in §3 (8 variants, NOTA-shaped per
`skills/nota-schema-docs.md`). Action plan in §5.

The lane set from `/225` (13 lanes with `concept-designer`,
`persona-deployer`, `lojix` as own subsystem) carries forward
unchanged — it is the destination; this report is about the **next
slice** that makes orchestrate real today.

---

## 1 · State as of 2026-05-18

| Component | Status | Path |
|---|---|---|
| `persona-mind` daemon | **Working.** Kameo actors, Unix socket, sema-engine. Smoke scripts pass. | `/git/.../persona-mind` |
| `signal-persona-mind` contract | **Shipped.** RoleClaim/Release/Observation/Handoff/Activity wired end-to-end. | `/git/.../signal-persona-mind` |
| `mind` CLI | **Working.** One NOTA record in, one NOTA reply out. | `persona-mind/src/bin/mind.rs` |
| `tools/orchestrate` shell | **22-line shim** that execs the Rust port. | `/home/li/primary/tools/orchestrate` |
| `orchestrate-cli` Rust port | **Working but disconnected.** Projects `MindRequest` but writes lock files instead of sending. | `/home/li/primary/orchestrate-cli/` |
| `persona-orchestrate` daemon | **Does not exist.** | (no path) |
| `signal-persona-orchestrate` contract | **Does not exist.** | (no path) |

The wire distance from "today" to "orchestrate-cli sends through
mind" is one Unix-socket call.

---

## 2 · Slice 1 — wire `orchestrate status` through `persona-mind`

**First flow to replace: `status` (read-only).** No conflict
semantics; no lock-file write; the failure modes are bounded
(socket-not-running falls back to lock-file scan).

Mechanical steps (operator-side):

1. `orchestrate-cli/Cargo.toml` — add `persona-mind` as a git
   dependency (already exports `MindClient`, `MindDaemonEndpoint`,
   `MindFrameCodec`).
2. `orchestrate-cli/src/workspace.rs` — add
   `mind_socket_path()` resolving from `$PERSONA_MIND_SOCKET` env var
   first, then `$XDG_RUNTIME_DIR/mind.sock`, then
   `<workspace>/.mind/mind.sock`.
3. `orchestrate-cli/src/claim.rs::status()` — when the socket is
   reachable, connect `MindClient`, send the projected
   `MindRequest::RoleObservation`, render the `RoleSnapshot` reply.
   When unreachable, fall back to lock-file scanning (existing path).
4. `orchestrate-cli/src/render.rs` — add
   `render_lock_state_from_snapshot(snapshot: &RoleSnapshot, ...)`
   mirroring the existing `StatusReport` renderer so output stays
   shell-compatible.

After Slice 1 lands: `tools/orchestrate status` round-trips through
the real daemon. State that was implicit in lock files becomes
sema-engine-durable. Restart-survival inherits from `persona-mind`'s
existing test (`scripts/mind-store-survives-process-restart`).

**No contract addition required.** Existing `signal-persona-mind`
records carry the flow.

Slices 2 and 3 (release, claim) follow the same pattern. Claim is
last because it carries the conflict-detection logic that needs to
move from lock-file scanning to a sema-engine query against
`persona-mind`'s `claims` table.

---

## 3 · Memory variant set

`persona-mind` will function as "a better beads": typed memory
records that cover every use case beads tracks today. Drawn from the
beads audit (54 open / 210 closed / 264 total, dominated by `task`
with `bug`, `feature`, `epic`, `decision` minorities).

Eight variants. Common fields apply to every variant; kind-specific
extensions follow. Each variant carries enough field detail for
operator to implement against; pseudo-NOTA per
`skills/nota-schema-docs.md`.

### Common fields

```nota
(Common <id> <title> <body> <created-at> <created-by> <status>
        <priority> <labels> <relations>)
;;   id          : TypedThoughtId    (content-derived)
;;   title       : ShortText
;;   body        : TextBody
;;   created-at  : Timestamp
;;   created-by  : Identity
;;   status      : Opening | Active | Closed
;;   priority    : P0 | P1 | P2 | P3 | P4
;;   labels      : [TypedLabel]      (see §3.1)
;;   relations   : [Relation]        (Blocks, BlockedBy, ChildOf, Supersedes, ...)
```

### 3.1 TypedLabel

```nota
(TypedLabel <kind>)
;;   kind : RoleLabel | RepoLabel | TopicTag | WorkflowTag

(RoleLabel <role>)
;;   role : RoleName                 (per signal-persona-mind enum, or LaneIdentifier post-/225)

(RepoLabel <repo>)
;;   repo : RepoIdentifier           (typed; see §3.6)

(TopicTag <kind> <noun>)
;;   kind  : Skill | Contract | Component | Concept
;;   noun  : ShortText

(WorkflowTag <state>)
;;   state : Active | Drift | Cleanup | Hygiene | Stale | Prototype
```

### 3.2 Task

```nota
(Task <acceptance-criteria> <spec-id?> <progress-notes>)
;;   acceptance-criteria : TextBody
;;   spec-id?            : ReportPath
;;   progress-notes      : [(Note <timestamp> <author> <body>)]
```

Covers 45 of 54 open beads. `progress-notes` is the load-bearing
addition: `primary-at7x` carries 7 iterative slice updates over 6
days; the chronology is the value, not the title.

### 3.3 Bug

```nota
(Bug <severity> <incident-at?> <reproduction?> <discovery-path?>)
;;   severity        : Catastrophic | High | Normal | Low
;;   incident-at?    : Timestamp
;;   reproduction?   : TextBody
;;   discovery-path? : ReportPath | CommitHash | "live"
```

`primary-51pn` (Whisrs P0 audio-loss) is the canonical example.

### 3.4 Feature

```nota
(Feature <branch> <repos>)
;;   branch : BranchName
;;   repos  : [RepoIdentifier]
```

For non-main-branch arcs that span multiple repos. Carries the branch
name explicitly per `skills/beads.md` §"Feature beads carry their
branch name". `horizon-leaner-shape` is the canonical multi-repo
example.

### 3.5 Epic

```nota
(Epic <children> <required-skills?>)
;;   children        : [TypedThoughtId]    (relations, not embedded)
;;   required-skills : [SkillName]
```

Multi-step body of work. `primary-ipjx` (durable-first STT) and
closed `primary-i10` (persona-engine-sandbox 5-step) are examples.

### 3.6 Decision

```nota
(Decision <options> <criteria> <discovered-from?> <resolution?>)
;;   options          : [(DecisionOption <name> <body> <implications>)]
;;   criteria         : TextBody
;;   discovered-from? : ReportPath
;;   resolution?      : (DecisionResolution <chosen-option> <report-link> <closed-at>)
```

`primary-0v2` (clavifaber/sshd identity unification) is the canonical
shape. Replaces beads' awkward `decision` type with explicit
option-enumeration.

### 3.7 Migration

```nota
(Migration <source-state> <target-state> <sites-remaining>)
;;   source-state    : TextBody
;;   target-state    : TextBody
;;   sites-remaining : [(MigrationSite <repo> <path> <status>)]
```

Multi-site sweeps where closure depends on coverage. Closed
`primary-186` (Ractor → Kameo) and `primary-77l` (`~/git` →
`/git/github.com`) are examples.

### 3.8 Discipline

```nota
(Discipline <skill-path> <skill-section?> <discovered-from?>)
;;   skill-path       : SkillPath
;;   skill-section?   : SectionAnchor
;;   discovered-from? : ReportPath
```

A rule that lives in a skill, plus a pointer to where. Avoids the
anti-pattern of opening a task that never closes; instead, the
discipline-record is already-closed-on-arrival and points at the
canonical rule. Closed `primary-bmy` is the example.

### 3.9 Investigation

```nota
(Investigation <question> <expected-output> <time-box?>)
;;   question        : TextBody
;;   expected-output : ReportPath | DesignerReport | OperatorReport
;;   time-box?       : Duration
```

Open question whose definition-of-done is a report. Closed
`primary-5lm` (deep Kameo 0.20 research) and `primary-jg1` (audit
Chroma and Clavifaber) are examples.

### 3.10 RepoIdentifier — typed, not stringly

Per the user's direction: not a string like `LiGoldragon/primary`.
A typed record:

```nota
(RepoIdentifier <owner> <repo> <branch?>)
;;   owner   : Identity     (GitHub user or org name)
;;   repo    : ShortText    (repo name)
;;   branch? : BranchName   (jj bookmark name; absent ⇒ default branch)
```

The repository-change-ledger daemon (per
`reports/designer-assistant/121-repository-change-ledger-proposal-2026-05-18.md`)
will be the queryable index over these identifiers.

---

## 4 · Memory placement — orchestrate vs mind

The user's direction: orchestration state (lock-like "who is working
on what right now") **stays in orchestrate**; durable memories
(work-graph, decisions, history) **go to mind**.

In today's shape:

- **`orchestrate-cli`** owns the lock-file equivalent — short-lived,
  per-session, names *who holds what scope right now*. After Slice 1,
  this is a sema-engine table inside `persona-mind` (`claims` exists
  already), but the *write path* still goes through orchestrate's CLI
  surface.
- **`persona-mind`** owns durable memories: every other record kind
  in §3. Mind is the storage; orchestrate is the lane-coordination
  surface.

When `persona-orchestrate` exists as its own daemon (future), the
`claims` state moves there. Until then, mind holds both — fine
because they're already typed records in the same engine.

### Cross-component create-on-behalf

Per user direction: unprivileged components (orchestrate, future
roles, future tools) should be able to **create memories in
persona-mind** with origin-traceable provenance. Mind already
supports this through `created_by`. The pattern:

```nota
(NoteSubmission <body> <origin> <timestamp> <visibility>)
;;   origin     : (Origin <component> <reason>)
;;   visibility : Note | Memory   (Note = unprivileged, traceable; Memory = peer-with-mind)
```

A component (orchestrate) writes a `Note` with `Origin =
"orchestrate"`; mind stores it but flags its provenance. Privileged
components (designer running directly) can write `Memory` records.

This is a §3.1 TypedLabel extension or a `kind` field on the common
record — operator's call when implementing.

---

## 5 · Action plan

| Stage | Lane | What |
|---|---|---|
| 1 | persona-operator | Wire `orchestrate-cli` to send `MindRequest::RoleObservation` through the live `persona-mind` socket. Status flow only. Falls back to lock-file scan when socket unreachable. |
| 2 | persona-operator | Same for `release` (single-verb, no conflict). |
| 3 | persona-operator | Same for `claim`. Conflict detection moves from lock-file scan to sema-engine query against `persona-mind`'s `claims` table. |
| 4 | persona-designer | Land the 8 memory variants in `signal-persona-mind` as new request variants under the existing `Mind` channel. Round-trip + canonical-examples tests. |
| 5 | persona-operator | Wire `bd` use-cases through `mind` CLI — `mind submit-task`, `mind submit-bug`, `mind comment`, `mind close`. Either as wrappers on top of the typed `mind '<one NOTA>'` flow or as sub-commands. |
| 6 | persona-operator | Add `mind list --kind <variant> --status open` query. Replaces `bd list`. |
| 7 (deferred) | persona-designer | Stand up `signal-persona-orchestrate` contract + `persona-orchestrate` daemon when memory routing pressure justifies splitting from `persona-mind`. |
| 8 (deferred) | persona-deployer | Production-deploy persona stack so memory survives across machine restarts. |

Stages 1-6 are weeks of operator work, not days. Stage 1 is hours.

---

## 6 · Open questions

- **The closed `RoleName` enum in `signal-persona-mind`**: needs the
  path-4 resolution from `reports/second-designer-assistant/6-...md`
  before lanes can be created dynamically. Until then, the closed
  8-variant set is the only thing the contract accepts. Concrete fix:
  `RoleName` → `LaneIdentifier(LaneSlot)` newtype, with `persona-mind`
  (or eventually `persona-orchestrate`) owning the `lane_registry`
  table. This is a contract change cascade; designer-lane work
  separate from this report's slice.
- **`mind` CLI subcommand surface vs one-NOTA-record-in shape**: the
  user wrote `mind` as one-NOTA-in/one-NOTA-out. For ergonomics, do
  we add subcommands (`mind submit-task ...`) or keep CLI thin and
  expect agents to write NOTA directly? Lean: stay thin; if user
  ergonomics need subcommands, wrap externally rather than thickening
  the CLI.
- **`persona-orchestrate` repo creation timing** (Stage 7): when does
  the carve-out justify standing up a third daemon? Lean: when
  memory routing pressure in `persona-mind` measurably hurts (latency
  on the `claims` table, or contention with thought-graph dispatch).
  Until then, both live in mind.
- **Per-repo persona-mind vs global**: user said global. The
  `RepoIdentifier` typed record carries the repo info as a field; no
  per-repo database. Confirmed direction; flagging here so operator
  knows not to build per-repo schemas.

---

## 7 · Carry-forward from `/225`

The lane set from `/225` (13 lanes, `concept-designer` +
`persona-deployer` + `lojix` as own subsystem) is **the destination**.
This report doesn't restate the lane discussion — see `/225` for the
lane taxonomy reasoning.

After Slice 1 lands and the lane rename happens (per `/225` §6 Stage
B), `orchestrate-cli` will route lane claims to `persona-mind` with
the new lane names. The closed `RoleName` enum cascade is the gating
work.

This report **replaces `/225`** as the current direction. `/225`
should be deleted when this report lands.

---

## See also

- `signal-persona-mind` — the contract carrying claim/release/status verbs already.
- `persona-mind` — the daemon doing the work today.
- `orchestrate-cli` — the Rust port that projects `MindRequest` but doesn't send.
- `skills/nota-schema-docs.md` — pseudo-NOTA convention used in §3.
- `skills/beads.md` — current beads discipline being replaced.
- `reports/designer-assistant/121-repository-change-ledger-proposal-2026-05-18.md` — the queryable repo index.
- `reports/designer/224-workspace-redesign-first-concept-2026-05-18.md` — original research-grounded direction.
