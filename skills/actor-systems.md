# Skill — actor systems

*Actors are a thinking discipline: every logical plane gets a
named owner, a typed mailbox, supervision, and tests that prove
the path was used.*

---

## What this skill is for

Use this skill whenever a component is a daemon, service, runtime,
router, state engine, watcher, delivery engine, database owner, or
other long-lived system with concurrent or ordered behavior.

The workspace uses actors not mainly because actors are fast, but
because actor boundaries force correctness in thinking. An actor
turns a vague step into a noun with state, a mailbox, failure
semantics, and an observable trace. That pressure matters in an
agent-written codebase: an agent can hide a missing phase inside a
helper method, but it is much harder to fake an actor topology,
typed messages, and trace witnesses.

For Rust implementation details, the runtime default is **`kameo`
0.20** — see this workspace's `skills/kameo.md` for usage. Kameo's
native shape (`Self` IS the actor; `Args = Self` is the documented
common case; per-kind `Message<T>` impls; declarative supervision)
agrees with the rules below; no carve-outs needed.

Do not introduce a second actor library or wrapper trait layer as a
prerequisite. Do not name or design a `persona-actor`,
`workspace-actor`, `workspace_actor::Actor`, or equivalent wrapper
crate/trait unless the human explicitly asks for a new actor
abstraction. Those names are historical drift from the
ractor-substitute thread (operator/103); the framework is now Kameo
and the wrapper question is settled. A component may have many
actors; it still has one Rust actor library: `kameo`.

---

## Core rule

**Actors all the way down.**

Every non-trivial logical plane deserves an actor. Smallness is not
an objection; triviality is. A plane is actor-shaped when all three
are true:

- it has a typed domain name, not just a verb on existing data
- it has a failure mode callers act on
- it can be tested independently with typed synthetic input

Those tests catch the boundary. `ClaimConflict`, `IdMint`,
`SemaCommit`, `FocusObservation`, `PromptGuard`, and
`ReplyShape` are actors. "Strip trailing slash" is a method on the
actor that owns path normalization.

If the plane owns state, transforms a request, validates authority,
decides legality, mints identity or time, performs IO, commits
durable state, maintains a view, shapes replies, supervises
children, or records trace, it is probably actor-shaped. The
overhead is acceptable; the correctness in design is the point.

```mermaid
flowchart LR
    vague["one actor with helper methods"] --> hidden["hidden planes"]
    hidden --> bypass["bypass is easy"]

    dense["many named actors"] --> visible["visible planes"]
    visible --> tests["topology and trace tests"]
    tests --> correct["bypass fails"]
```

---

## Actor per plane

An actor-heavy system should look over-named to conventional Rust
eyes. That is expected.

| Plane | Actor noun |
|---|---|
| Parse one CLI record with diagnostics | `NotaDecoder` |
| Identify caller | `CallerIdentityResolver` |
| Add actor identity to request | `EnvelopeBuilder` |
| Route request by type | `RequestDispatcher` |
| Normalize a claim path | `ClaimNormalizer` |
| Check claim conflicts | `ClaimConflictDetector` |
| Mint item identity | `IdMint` |
| Mint store time | `Clock` |
| Append event | `EventAppender` |
| Commit state | `SemaWriter` |
| Read state | `SemaReader` |
| Maintain ready-work view | `ReadyWorkView` |
| Shape query result | `QueryResultShaper` |
| Encode reply | `NotaReplyEncoder` |

(Names follow `skills/kameo.md` §"Naming actor types": the type
IS the actor; the role describes what it does; no `Actor` suffix.)

These actors may be small. Some may be short-lived per request.
Some may be long-lived singletons. Some may become pools. The
choice of residency is a runtime decision; the actor identity is an
architecture decision.

Do not create actors for pure value transformations that have no
domain failure and no independent runtime ownership. Those methods
belong on the data-bearing actor that owns the surrounding phase.

---

## Blocking is a design bug

An actor's mailbox is the push channel for that actor. If an actor
blocks inside message handling, it stops receiving pushes and the
system has recreated a hidden lock.

Forbidden inside a normal actor handler:

- sleeping to wait for state
- polling for state
- blocking on a mutex or read-write lock
- blocking process execution
- blocking filesystem or network calls
- synchronous waits for another actor that can call back upward
- long CPU work that starves the mailbox

Replace blocking with another actor:

| Blocking smell | Actor-shaped replacement |
|---|---|
| Handler runs a slow command | `Command` or `CommandPool` owns process execution. |
| Handler waits for file IO | `FileReader` / `FileWriter` owns that IO. |
| Handler waits for database commit | Send a typed intent to `SemaWriter`; receive a reply. |
| Handler sleeps before retry | Subscribe to the producer event; no sleep. |
| Handler locks shared state | Send a message to the actor that owns that state. |
| Handler does expensive CPU transform | `TransformWorker` pool owns that work. |

The rule is not "nothing ever takes time." The rule is that time
belongs to a named actor whose mailbox and supervision make the wait
visible. A blocking operation is allowed only inside the actor whose
single job is that blocking plane, and that actor is supervised,
traceable, and replaceable.

---

## No shared locks

Do not use `Arc<Mutex<T>>` or `Arc<RwLock<T>>` as the ownership
model between actors. That turns the lock into the real actor and
makes the actors decorative.

State has one owner:

```mermaid
flowchart LR
    owner["StateOwner"] --> state["private State"]
    caller["Caller"] -->|typed message| owner

    bad_a["Actor A"] -. forbidden .-> lock["Arc<Mutex<State>>"]
    bad_b["Actor B"] -. forbidden .-> lock
```

If two actors need the same state, the state has the wrong owner or
the state should be split into two actors. Use message passing,
snapshots, and read views; do not add shared locks.

---

## Supervision is part of the design

An actor without a supervised parent is not finished. Every actor
belongs in a tree.

```mermaid
flowchart TB
    root["RootSupervisor"]
    root --> ingress["IngressSupervisor"]
    root --> domain["DomainSupervisor"]
    root --> commit["CommitSupervisor"]
    root --> view["ViewSupervisor"]

    domain --> claim["ClaimSupervisor"]
    claim --> normalize["ClaimNormalizer"]
    claim --> conflict["ClaimConflictDetector"]
```

Each supervisor needs a typed failure policy:

| Failure | Policy question |
|---|---|
| child rejects input | reply with typed rejection |
| child panics | restart, stop, or escalate |
| child loses IO resource | rebuild resource actor or escalate |
| view refresh fails | preserve committed state and schedule pushed retry |
| writer fails | abort transition and emit typed failure |

No detached tasks. If work must run independently, it is an actor
or a supervised worker pool.

---

## Rust shape

The workspace runtime default is **`kameo` 0.20**. The actor type IS
the data-bearing noun — Kameo collapses the framework's behavior
marker and the actor's mutable state into a single struct. The
no-public-ZST-actor rule is naturally satisfied because the type
that carries the actor's data IS the actor.

Kameo native shape:

- the actor type carries fields (`pub struct ClaimNormalize { in_flight: …, metrics: … }`);
- `type Args = Self` is the documented common case; the spawner
  passes a fully-built actor value to `on_start` which returns it;
- `type Error = kameo::error::Infallible` (or a typed crate Error)
  on the `Actor` impl;
- domain methods live on the actor type directly (`impl ClaimNormalize { fn validate_and_collapse(&mut self, …) }`), not on a ZST namespace;
- per-kind `impl Message<Verb> for ClaimNormalize` for each accepted
  message — no monolithic `Msg` enum;
- the public consumer surface is `ActorRef<ClaimNormalize>` directly;
  Kameo's `ActorRef<A>` is statically typed against the actor, so
  no `*Handle` wrapper is needed — including for library users
  (see `skills/kameo.md` §"ActorRef<A> is the public consumer
  surface");
- supervision is declarative: `ClaimNormalize::supervise(&parent, args).restart_policy(...).restart_limit(n, dur).spawn().await`.

For actor-dense systems:

- one actor per file when the actor is durable enough to name;
  co-locate the `Actor` impl, the `Message<T>` impls for that actor,
  and the message/reply types in one file;
- one `impl Message<Verb> for Actor` per verb — no monolithic
  message enum;
- no "handle anything" `on_message` override inside a component;
- no raw `Spawn::spawn` outside the runtime root; child spawns go
  through `supervise(&parent, args).spawn().await`;
- no `Arc<Mutex<T>>` between actors;
- no long `await` inside a handler unless this actor owns that wait;
- no blocking call inside a handler except in a dedicated blocking
  plane actor — and that actor uses `DelegatedReply<R>` so the
  mailbox stays responsive;
- no public ZST actor nouns (Kameo permits them, the workspace
  doesn't — actor types must carry data fields);
- never `tell` a handler whose `Reply = Result<_, _>` unless `on_panic`
  is overridden to recover from `PanicReason::OnMessage` — a
  `Result::Err` from a `tell`'d handler crashes the actor by default
  (see `skills/kameo.md` §"The tell-of-fallible-handler trap").

The actor's public consumer surface is `ActorRef<MyActor>`.
Consumers spawn the actor (or are handed an `ActorRef`) and call
`ask` / `tell` directly. They do not construct actor internals.

---

## Traces are required

An actor-heavy system must expose an actor trace in tests. The
trace is how we prove that the named planes actually ran.

```mermaid
flowchart LR
    request["MindRequest"] --> runtime["actor runtime"]
    runtime --> trace["ActorTrace"]
    trace --> pattern["expected actor path"]
    pattern --> pass["pass or fail"]
```

Trace events should include:

- actor started
- actor stopped
- message received
- message replied
- child spawned
- child failed
- write intent sent
- commit completed
- view refreshed

The trace is not a logging substitute. It is a test witness.

---

## Test actor density

Behavior tests are not enough. Tests must prove that the actor
planes exist and are used.

Required test families:

| Test | What it proves |
|---|---|
| topology manifest test | expected supervisors and actors exist |
| trace-pattern test | request ran through required actor sequence |
| forbidden-edge test | actor did not bypass required owner |
| no-writer-in-query test | query path did not mutate state |
| no-blocking-handler test | actor handler did not perform forbidden blocking work |
| failure-injection test | each actor phase has typed failure behavior |
| actor-count test | future agents cannot collapse actors by assuming overhead |
| no-zst-actor test | public actor nouns carry data fields (Kameo's `Self IS the actor` shape makes this naturally enforceable via `mem::size_of::<MyActor>() > 0`) |

Test name patterns:

- `claim_cannot_commit_without_conflict_actor`
- `query_cannot_touch_sema_writer`
- `item_open_cannot_mint_id_without_id_actor`
- `handler_cannot_block_mailbox`
- `topology_cannot_omit_claim_normalizer`
- `claim_normalizer_cannot_be_empty_marker`

The `#[test]` wrapper calls methods on a fixture. The fixture
drives the actor runtime, captures the trace, and asserts the
topology or path.

---

## When not to create an actor

Do not create an actor for:

- a pure value type
- a contract record
- a one-line display implementation
- a parser that is just a short-lived data-bearing object inside
  an already actor-owned phase
- a library crate with no runtime ownership

Even then, the behavior still belongs on a data-bearing type, not
a free function or a ZST method holder.

---

## See also

- this workspace's `skills/rust-discipline.md` — Rust ownership,
  typing, errors, redb/rkyv, and the kameo default.
- this workspace's `skills/architectural-truth-tests.md` —
  tests that prove the actor path was used.
- this workspace's `skills/push-not-pull.md` — actor mailboxes
  are push channels; polling is forbidden.
- this workspace's `skills/abstractions.md` — actor verbs belong
  on the data-bearing actor noun, not on framework marker glue.
- this workspace's `skills/kameo.md` — Kameo 0.20 usage in this
  workspace (the framework reference).
- `/git/github.com/LiGoldragon/kameo-testing` — falsifiable source
  for every Kameo behavior the skill cites.
- lore's `rust/testing.md` — actor runtime testing and fixture
  patterns.
