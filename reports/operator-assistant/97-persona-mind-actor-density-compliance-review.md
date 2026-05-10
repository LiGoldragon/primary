# 97 - Persona-mind actor-density compliance review

Status: assistant research pass on
`reports/operator/101-persona-mind-full-architecture-proposal.md`.

Author: Codex (assistant)

Date: 2026-05-10

---

## Summary

`reports/operator/101-persona-mind-full-architecture-proposal.md` is not just
a rename or storage proposal. It changes the implementation bar:
`persona-mind` should be an actor-dense system, with `MindRootActor` and eight
top-level supervisors, many per-phase actors, one serialized writer path, and
typed post-commit views/subscriptions.

The recently developed Persona runtime components do not yet comply with that
approach. They are still mostly reducer/service-object scaffolds:

- no reviewed runtime crate depends on `ractor`;
- no reviewed runtime crate exposes the four-piece actor shape from
  `skills/rust-discipline.md` (`Actor`, `State`, `Arguments`, `Message`,
  plus `*Handle`);
- `persona-mind` has the central contract and in-memory behavior tests, but
  no actor tree, no `persona-sema` dependency, no `mind.redb` persistence, and
  no internal request envelope carrying caller identity;
- `persona-router` uses names like `RouterActor` and `HarnessActor`, but those
  are ordinary structs mutated synchronously by a Unix-socket loop;
- `persona-message` remains a transitional file-backed ledger with a polling
  `tail` loop;
- `persona-system` pushes Niri event-stream observations, but it is still a
  synchronous adapter/CLI rather than supervised actors.

This is not surprising: the current code looks like Phase 0 from operator/101,
not Phase 1. The risk is documentation drift: several architecture files now
describe actor-owned Sema state as if the runtime shape already exists.

## Actor-Dense Standard From Operator/101

Operator/101 sets these load-bearing constraints:

- `persona-mind` is the central state component for claims, handoffs,
  activity, memory/work items, notes, dependencies, decisions, aliases, and
  ready-work views.
- `mind` operations enter through `signal-persona-mind`, then pass through
  ingress, dispatch, domain, store, view, subscription, and reply actors.
- `MindRootActor` supervises `ConfigActor`,
  `IngressSupervisorActor`, `DispatchSupervisorActor`,
  `DomainSupervisorActor`, `StoreSupervisorActor`,
  `ViewSupervisorActor`, `SubscriptionSupervisorActor`, and
  `ReplySupervisorActor`.
- Operation phases become actors when they have a named failure mode:
  `NotaDecodeActor`, `CallerIdentityActor`, `EnvelopeActor`,
  `ClaimNormalizeActor`, `ClaimConflictActor`, `IdMintActor`, `ClockActor`,
  `SemaWriterActor`, `EventAppendActor`, `CommitActor`,
  `ReadyWorkViewActor`, `GraphTraversalActor`, `ErrorShapeActor`, and so on.
- Only `SemaWriterActor` opens write transactions.
- Query actors use read snapshots and must not repair state while answering.
- Actor multiplicity is intentional: hundreds of actors are normal, not
  exceptional.

That matches `skills/rust-discipline.md` §"Actors: logical units with
ractor": stateful components with a message protocol default to `ractor`;
actors own state, receive typed messages, and live under recursive
supervision.

## Scope Reviewed

I reviewed the active central-mind wave and adjacent recently developed
runtime crates:

| Repo | Current main | Relevance |
|---|---:|---|
| `/git/github.com/LiGoldragon/persona-mind` | `1709e28f` | central runtime target from operator/101 |
| `/git/github.com/LiGoldragon/signal-persona-mind` | `a75fe712` | central contract |
| `/git/github.com/LiGoldragon/persona-router` | `53074412` | adjacent stateful runtime actor candidate |
| `/git/github.com/LiGoldragon/persona-message` | `3046a46e` | transitional message CLI/ledger |
| `/git/github.com/LiGoldragon/persona-system` | `d469e2ee` | pushed OS observation boundary |
| `/git/github.com/LiGoldragon/persona-sema` | `47dd3879` | typed storage library |

I also checked for actor-runtime adoption across the runtime crates:

```text
persona-mind     ractor/actor-runtime dependency hits: 0
persona-router   ractor/actor-runtime dependency hits: 0
persona-message  ractor/actor-runtime dependency hits: 0
persona-system   ractor/actor-runtime dependency hits: 0
persona-sema     ractor/actor-runtime dependency hits: 0
```

The lack of `ractor` is not a problem for contract crates or
`persona-sema`. It is a problem for `persona-mind` if operator/101 is now the
active architecture.

## Findings

### P1 - `persona-mind` is a reducer scaffold, not an actor tree

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/Cargo.toml:19` depends only on
  `signal-persona-mind`; there is no `ractor`, `persona-sema`, `sema`, `redb`,
  `nota-codec`, or async runtime dependency.
- `/git/github.com/LiGoldragon/persona-mind/src/lib.rs:1` exposes only
  `claim`, `memory`, and `role`.
- `/git/github.com/LiGoldragon/persona-mind/src/main.rs:1` prints
  `"mind scaffold"` instead of parsing one NOTA request and submitting it to
  an actor tree.
- The repo has no `src/actors/` directory, no `MindRootActor`, and none of
  the eight top-level supervisors from operator/101.

The architecture file already claims a much larger surface:
`/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md:38` says the library
opens `mind.redb` through `persona-sema`, and
`/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md:46` names typed
runtime tables. The code does not have those dependencies or modules yet.

Compliance gap:

`persona-mind` currently proves some domain semantics, but it does not prove
the actor-heavy runtime shape. It should be treated as Phase 0, not as a
runtime implementation.

### P1 - `persona-mind` central state is in-memory and single-object owned

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:16` stores
  `MemoryState { store, graph: RefCell<Graph> }`.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:38` defines one
  `Graph` with counters and `Vec<Item>`, `Vec<Edge>`, `Vec<Note>`, and
  `Vec<Event>`.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:63` dispatches all
  memory requests through one `match` on `MindRequest`.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:80` through
  `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:184` performs open,
  note, link, status, alias, and query behavior as direct methods on that one
  `Graph`.

This is useful reducer work, but it is the opposite of operator/101's
actor-dense decomposition. There is no `MemoryFlowActor`, `ItemOpenActor`,
`SourceResolveActor`, `EdgeValidateActor`, `GraphTraversalActor`,
`QueryPlanActor`, or `QueryResultShapeActor`.

Compliance gap:

The reducer should survive, but it needs to be put behind actors. The current
`Graph` is a good sync-facade test target, not the runtime owner.

### P1 - `persona-mind` mints identity inside the reducer, not through actor-owned infrastructure

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:25` hardcodes
  `ActorName::new("persona-mind")`.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:80` mints
  `StableItemId` from an incrementing in-memory counter.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:85` mints
  `DisplayId` through a local `DisplayIdMint`.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:336` mints
  `EventSeq` and `OperationId` from in-memory counters.
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:337` stamps events
  with the hardcoded actor.

Operator/101 and designer/100 require this to live in actor-owned
infrastructure:

- `CallerIdentityActor` derives caller identity.
- `EnvelopeActor` wraps `MindRequest` into `MindEnvelope`.
- `IdMintActor` owns operation, event, item, and display IDs.
- `ClockActor` owns time.
- `SemaWriterActor` serializes commit ordering.

Compliance gap:

There is no `MindEnvelope` path in `persona-mind` yet. Memory events are
auditable only in the trivial "persona-mind did it" sense, not in the
workspace sense where operator/designer/assistant activity must be attributable
to the calling actor.

### P1 - Claim handling is per-role local state, not central conflict state

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/claim.rs:31` defines
  `ClaimState { role, scopes }`.
- `/git/github.com/LiGoldragon/persona-mind/src/claim.rs:45` adds claims for
  that one role and collapses redundant children.
- There is no multi-role claim table, no conflict result type, no handoff
  transition, and no activity/event append.

The claim reducer is a useful atom, but operator/101 requires a central
claim path:

`ClaimFlowActor -> ClaimNormalizeActor -> ClaimConflictActor -> SemaWriterActor
-> EventAppendActor -> RoleSnapshotViewActor -> NotaReplyEncodeActor`.

Compliance gap:

The current claim code can answer "does this role own this normalized path?"
It cannot answer "does this new claim conflict with another role, commit
atomically, append an event, and refresh the role view?"

### P1 - `persona-mind` docs are already ahead of code

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md:150` lists
  `src/state.rs`, but that file does not exist.
- The same code map lists `src/tables.rs`, `src/activity.rs`,
  `src/projection.rs`, and `src/service.rs`; those files do not exist.
- The architecture still says lock files are regenerated projections at
  `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md:54`, while
  operator/101 Phase 3 says lock files are retired and typed read views replace
  that workflow.

Compliance gap:

The repo documentation should either be marked explicitly as target/Phase 2+
or updated to the actor-dense operator/101 structure. Right now it mixes target
claims with nonexistent files, which will mislead the next implementer.

### P2 - `signal-persona-mind` is mostly fine as a contract, but it does not solve runtime identity

Evidence:

- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:855` declares
  the `MindRequest`/`MindReply` channel.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:668` through
  `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:706` define
  memory request bodies with no actor field.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:755` defines
  `EventHeader { event, operation, actor }`.

That contract shape is consistent with designer/100: the request payload
should not let the caller supply actor identity. But the missing runtime
piece is still real: `persona-mind` needs an internal `MindEnvelope` and
`CallerIdentityActor`/`EnvelopeActor` before persistence.

Compliance gap:

Do not fix this by adding `actor` fields to `Opening`, `NoteSubmission`,
`Link`, `StatusChange`, or `AliasAssignment`. Fix it in `persona-mind` by
adding the actor-tree ingress path.

### P2 - `persona-router` uses actor names but not actors

Evidence:

- `/git/github.com/LiGoldragon/persona-router/src/router.rs:17` defines
  `RouterDaemon { socket, actor }`.
- `/git/github.com/LiGoldragon/persona-router/src/router.rs:42` handles
  incoming Unix-socket streams synchronously in a loop.
- `/git/github.com/LiGoldragon/persona-router/src/router.rs:109` defines
  `RouterActor { actors: HashMap<ActorId, HarnessActor>, pending:
  Vec<Message> }`.
- `/git/github.com/LiGoldragon/persona-router/src/router.rs:122` applies
  every input through one synchronous `match`.
- `/git/github.com/LiGoldragon/persona-router/src/router.rs:246` performs
  delivery side effects directly from `HarnessActor::deliver`.
- `/git/github.com/LiGoldragon/persona-router/src/router.rs:257` sleeps for
  one second inside the delivery path.

The architecture file says the router owns a router-scoped Sema database and
emits follow-up frames only after commit
(`/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md:39`), but
`Cargo.toml` has no `persona-sema`, `sema`, or `ractor` dependency.

Compliance gap:

This is not actor-heavy; it is a synchronous state machine with actor-shaped
names. The first compliance move is to rename or explicitly classify the
current structs as reducer scaffolds, then add a real `RouterRootActor` /
`RouterHandle` shape when `primary-186` or its successor lands.

### P2 - `persona-message` remains file-backed and polling

Evidence:

- `/git/github.com/LiGoldragon/persona-message/src/store.rs:36` stores actor
  identity in `actors.nota`.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:40` and
  `/git/github.com/LiGoldragon/persona-message/src/store.rs:44` define
  `messages.nota.log` and `pending.nota.log`.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:102` appends
  messages directly to the local file log.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:213` implements
  `tail` as an infinite polling loop.
- `/git/github.com/LiGoldragon/persona-message/src/store.rs:235` sleeps
  200ms between file reads.
- `/git/github.com/LiGoldragon/persona-message/src/daemon.rs:44` is a
  synchronous Unix-socket daemon around `MessageStore`.

The architecture file honestly calls this a transitional local ledger at
`/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md:41`. That is good.
The noncompliance is only dangerous if this remains the active runtime shape
after router/mind actors land.

Compliance gap:

`persona-message` should become only the NOTA projection/CLI layer. Durable
message routing state belongs behind `persona-router`'s real actor path, not
inside a file-backed polling ledger.

### P3 - `persona-system` pushes events but is not supervised

Evidence:

- `/git/github.com/LiGoldragon/persona-system/src/niri.rs:27` runs a one-shot
  `niri msg --json windows` probe.
- `/git/github.com/LiGoldragon/persona-system/src/niri.rs:41` runs a
  subscription by spawning `niri msg --json event-stream`.
- `/git/github.com/LiGoldragon/persona-system/src/niri.rs:60` loops over
  stdout lines and writes observations directly to the caller's output.

This is closer to the push-not-poll discipline than `persona-message`, but it
still lacks a supervised `SystemAdapterActor`, subscription actor, restart
policy, and typed connection to `persona-router`.

Compliance gap:

This is not as central as `persona-mind`, but once it becomes a long-lived
runtime component, it should receive the same ractor treatment: backend actor,
subscription actor, and typed output channel.

### P3 - `persona-sema` is not an actor, and that is correct

Evidence:

- `/git/github.com/LiGoldragon/persona-sema/ARCHITECTURE.md:20` states the
  crate is a storage library, not a daemon.
- `/git/github.com/LiGoldragon/persona-sema/src/store.rs:21` defines
  `PersonaSema { sema }`, a typed storage handle.
- `/git/github.com/LiGoldragon/persona-sema/src/tables.rs:60` materializes the
  current table set by calling `sema.write`.

This crate should not grow an actor tree merely to match operator/101.
Operator/101 wants `persona-mind` actors to use `persona-sema`, not for
`persona-sema` to become a storage actor.

Compliance note:

The only mild cleanup is naming: the `persona-sema-daemon` binary is still a
placeholder in `Cargo.toml`, while the architecture says the crate is not a
daemon. That is documentation/surface hygiene, not an actor-density blocker.

## What Should Not Be Counted As Noncompliance

Contract crates such as `signal-persona-mind`,
`signal-persona-system`, and `signal-persona-message` should not contain
runtime actors. Their job is the closed typed vocabulary, rkyv frame shape,
and round-trip tests. The actor-heavy requirement applies to the consumers
that own state and lifecycle.

Likewise, `persona-sema` should stay a library. The actor belongs in the
component that owns a domain database, not in a generic storage namespace.

## Recommended Compliance Path

### 1. Land `persona-mind` Phase 1 before persistence

Add `ractor` to `persona-mind` and implement the actor shell before moving
truth into redb:

- `src/actors/root.rs`
- `src/actors/ingress.rs`
- `src/actors/dispatch.rs`
- `src/actors/claim.rs`
- `src/actors/handoff.rs`
- `src/actors/activity.rs`
- `src/actors/memory.rs`
- `src/actors/query.rs`
- `src/actors/store.rs`
- `src/actors/view.rs`
- `src/actors/subscription.rs`
- `src/actors/reply.rs`

Keep the existing reducers as sync-facade state tests under those actors. The
goal of Phase 1 is not full durability; it is to ensure every request enters
through the same actor tree.

### 2. Add internal `MindEnvelope`

Add an internal runtime type, not a signal payload field:

```rust
pub struct MindEnvelope {
    pub actor: ActorName,
    pub request: MindRequest,
}
```

The `CallerIdentityActor` resolves the actor. The `EnvelopeActor` constructs
the envelope. Every domain flow actor consumes the envelope, and every event
header uses `envelope.actor`.

### 3. Put ID/time minting behind actors

Move local counters and display ID generation out of `Graph`:

- `IdMintActor` owns `EventSeq`, `OperationId`, `StableItemId`, and
  `DisplayId` minting.
- `ClockActor` owns timestamps when activity persistence lands.
- The caller supplies content only.

### 4. Add actor-shape architectural truth tests

Useful first tests:

- `persona-mind` depends on `ractor`.
- `persona-mind` has `src/actors/root.rs`.
- `MindRootActor` exists.
- The eight top-level supervisors from operator/101 exist.
- The `mind` binary does not directly mutate `MemoryState` or `ClaimState`.
- There is no production `RefCell<Graph>` path used as the runtime owner.
- Memory/work events are stamped from `MindEnvelope.actor`, not a hardcoded
  `"persona-mind"` actor.

These are intentionally structural. They prevent the next scaffold from
claiming actor compliance while staying a synchronous service object.

### 5. Defer `persona-router` and `persona-message` actor rewrites until mind Phase 1 is visible

`persona-router` and `persona-message` have real actor gaps, but `persona-mind`
is the central architecture pivot. Build one correct actor-dense component
first, then reuse that shape in router and message.

## Bottom Line

The current codebase does not yet comply with operator/101's actor-heavy
approach. It has typed contracts and useful reducer tests, but not supervised
runtime actors.

The highest-signal next work is `persona-mind` Phase 1: add the ractor-based
root/supervisor skeleton, route the existing memory and claim reducers through
typed actor messages, and add structural truth tests that make "actor-dense"
impossible to fake.
