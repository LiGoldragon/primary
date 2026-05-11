# Skill — kameo

*Workspace actor runtime. Self IS the actor; messages are typed
per-kind; supervision is declarative. The framework's shape agrees
with `skills/actor-systems.md`'s rules — no carve-outs needed.*

---

## What this skill is for

Use this skill when you write or edit Rust that defines, spawns,
supervises, or sends messages to an actor in this workspace. Kameo
0.20 is the workspace's actor runtime, replacing direct `ractor`.

For the architectural discipline — when a logical plane deserves
an actor, what counts as actor-shape, the no-blocking-handler rule,
the no-public-ZST-actor-noun rule — see this workspace's
`skills/actor-systems.md`. This skill is *how* you express that
discipline in Kameo specifically.

The falsifiable source for every claim below is twofold:

- `/git/github.com/LiGoldragon/kameo-testing` — designer's test bed
  (lifecycle, messages, spawn, mailbox, registry, supervision,
  streams, links, topology).
- `/git/github.com/LiGoldragon/kameo-testing-assistant` —
  designer-assistant's complementary tests (data-bearing patterns,
  failure & mailbox, lifecycle/registry/threads).

Together they cover the surface a Persona component needs.

## Maturity and pinning

Kameo is pre-1.0, actively developed, and small enough that API
churn between minor versions is real. As of 2026-05-10:

- crates.io: 33 versions; latest `0.20.0` (2026-04-07); ~248k total
  downloads, ~109k recent.
- GitHub: `tqwewe/kameo`; ~1,300 stars, last push 2026-04-27, 9
  open issues, single primary author.
- Public production users: `CapSoftware/Cap` (Loom alternative) on
  `0.17.2`; `ethui/ethui` (Ethereum toolkit) on workspace pin;
  `volga-project/volga` on `0.16.0`; `microsoft/dactor` ships a
  `dactor-kameo` adapter.

Read this as: not boring infrastructure yet, but real — beyond toy.
Pin Kameo's version intentionally per-crate; expect minor breaks.

**Rust 1.88 is required.** Kameo 0.20 declares `rust-version =
"1.88.0"`. Crates pinned at older toolchains (Persona's runtime
crates were on 1.85) must bump before adopting Kameo. See
`tools/sync-rust-fenix` for workspace-wide fenix lock alignment
once any crate's toolchain moves.

---

## The core shape

Kameo's load-bearing fact: **`Self` IS the actor.** Not a behavior
marker plus a separate `State`. Not a wrapper crate. The struct that
carries your actor's data is the type you implement `Actor` on.

```rust
use kameo::Actor;
use kameo::actor::{ActorRef, Spawn};
use kameo::error::Infallible;
use kameo::message::{Context, Message};

pub struct ClaimNormalizer {
    in_flight:    HashMap<RequestId, WirePath>,
    max_in_flight: usize,
    metrics:      ClaimNormalizerMetrics,
}

impl Actor for ClaimNormalizer {
    type Args  = Self;          // the documented common case
    type Error = Infallible;

    async fn on_start(args: Self, _ref: ActorRef<Self>) -> Result<Self, Self::Error> {
        Ok(args)
    }
}

pub struct Normalize { pub operation: OperationId, pub path: WirePath }

impl Message<Normalize> for ClaimNormalizer {
    type Reply = Result<NormalizedScope, ClaimNormalizerFailure>;

    async fn handle(
        &mut self,
        msg: Normalize,
        _ctx: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.in_flight.insert(msg.operation, msg.path.clone());
        let scope = self.validate_and_collapse(msg.path)?;
        self.metrics.normalize_count += 1;
        self.in_flight.remove(&msg.operation);
        Ok(scope)
    }
}

let normalizer = ClaimNormalizer::spawn(ClaimNormalizer {
    in_flight:     HashMap::new(),
    max_in_flight: 64,
    metrics:       ClaimNormalizerMetrics::default(),
});

let scope = normalizer.ask(Normalize { operation, path }).await?;
```

The actor type owns its data. Methods that operate on that data
live on the actor (`fn validate_and_collapse(&mut self, …)`). The
no-public-ZST-actor-noun rule from `skills/actor-systems.md` is
naturally satisfied: the actor type is the data-bearing noun.

---

## Naming actor types

**Name the actor by what it IS or what role it plays — never by
the framework category it falls into.** `Counter` is an actor;
`CounterActor` is `Counter` plus framework-category ceremony.

```rust
// Right
pub struct ClaimNormalizer { ... }
pub struct MindRoot { ... }
pub struct StoreSupervisor { ... }
pub struct Counter { count: i64 }

// Wrong — framework-category suffix
pub struct ClaimNormalizerActor { ... }
pub struct MindRootActor { ... }
pub struct StoreSupervisorActor { ... }
pub struct CounterActor { ... }
```

The `Actor` suffix is the same shape as `Type` / `Class` /
`Object` suffixes that ESSENCE retired. It names the framework
category the type happens to fall into — not the type's role or
function. The trait impl (`impl Actor for Counter`) makes the
framework participation explicit; the type name should describe
what the type IS.

This applies at every level of the actor surface:

| Concept | Wrong | Right |
|---|---|---|
| Actor type | `ClaimNormalizerActor` | `ClaimNormalizer` |
| Actor type | `MindRootActor` | `MindRoot` |
| Actor type | `CounterActor` | `Counter` |
| Message type | `IncMessage`, `IncMsg`, `Inc` | `Increment` |
| Message type | `SubmitMessage`, `SubmitClaim` | `ClaimSubmission` |
| Reply type (when needed) | `SubmitReply` | `SubmissionReceipt` |
| Handle type | `CounterHandle` (when wrapping `ActorRef<Counter>` for no reason) | use `ActorRef<Counter>` directly |

**Descriptive role suffixes earn their place** — they name what
the type DOES, not what category it falls into:

- `Supervisor` (this type supervises children)
- `Normalizer`, `Resolver`, `Validator`, `Decoder`, `Encoder`,
  `Dispatcher` (this type performs that named function)
- `Tracker`, `Cache`, `Ledger`, `Store` (this type holds that kind
  of state)

These are nouns with meaning. `Actor` is a category tag.

The historical drift toward `*Actor` / `*Message` suffixes came
from frameworks like ractor where the actor's behavior marker was
a separate ZST from its `State` — the suffix disambiguated. In
Kameo, where `Self` IS the actor, that disambiguation is moot and
the suffix becomes the workspace's "feels too verbose" trap (per
`ESSENCE.md` §"Naming"). Drop the suffix from the start.

---

## Public consumer surface — `ActorRef<A>` or domain wrapper

Kameo's `ActorRef<A>` is statically typed against the actor; the
message types it accepts are guaranteed by `impl Message<T> for A`
at compile time. There is no class of misuse a wrapper newtype
prevents — sending the wrong message is a type error at the call
site. The question isn't safety; it's **what API makes sense** for
the consumer.

Two patterns, distinguished by whether the wrapper carries domain
meaning:

### `ActorRef<A>` directly — when the actor IS the public API

Default for actors whose message types ARE the consumer surface.
The consumer spawns the actor (or is handed an `ActorRef<A>`) and
calls `actor_ref.ask(msg).await` / `actor_ref.tell(msg).await`
directly. Re-export `kameo::actor::ActorRef` from the crate root
if it makes consumer imports cleaner.

```rust
let normalizer = ClaimNormalizer::spawn(ClaimNormalizer { … });
let scope = normalizer.ask(Normalize { operation, path }).await?;
```

Most workspace actors fit this — small actors with a clear single
message vocabulary, in-workspace consumers, no multi-step
orchestration to hide.

### Domain wrapper — when the public API is a domain abstraction

When the consumer surface is a domain abstraction *over* one or
more actors, wrap. Two name shapes are both acceptable:

- **Bare domain noun** when the wrapper IS the conceptual surface
  and no shadowing data type exists: `Mind`, `Router`. Cleaner.
- **`*Handle` suffix** when the bare noun would shadow a sibling
  data type and the disambiguation matters: `LedgerHandle` (when
  `Ledger` is the data type with `entries: Vec<Entry>`),
  `MindHandle` (when `Mind` is also a typed record kind elsewhere).
  Per `skills/naming.md`, `Handle` is *relationship-naming* (the
  value IS a held authority on the live actor) — same shape as
  Tokio's `JoinHandle` or std's `File` / `Child` — *not*
  framework-category tagging like `Actor` / `Message`.

Never `*ActorHandle` (the `Actor` part is still the framework-category
trap). For remote-network services, `*Client` may be a better
relationship name than `*Handle`.

```rust
pub struct Mind {
    root:   ActorRef<MindRoot>,
    reader: ActorRef<SemaReader>,
}

impl Mind {
    pub async fn claim(
        &self,
        role:   ActorName,
        scope:  WirePath,
        reason: ScopeReason,
    ) -> Result<ClaimAcceptance, MindError> {
        self.root.ask(MindRequest::Claim { role, scope, reason }).await
            .map_err(MindError::from)?
            .into_acceptance()
    }

    pub async fn note(&self, item: ItemId, body: NoteBody) -> Result<NoteAdded, MindError> { … }

    pub async fn ready_work(&self) -> Result<Vec<ReadyItem>, MindError> { … }
}
```

A wrapper earns its place when **at least one** of these is true (per
designer-assistant/6 §"A Rule That Fits Both Sides"):

1. **Lifecycle ownership** — the wrapper has `start(config)` /
   `stop()` methods naming "I own this live service," not just "I
   hold a reference to an actor." Consumers think in services.
2. **Topology insulation** — the wrapper hides actor topology from
   the public API. If `Ledger` later becomes
   `LedgerWriter` + `LedgerReader` + `LedgerIndex` internally, the
   public `Ledger.append()` / `Ledger.read()` surface stays stable.
3. **Fallible-`tell` prevention** — the wrapper exposes only the
   safe method (`mind.claim(...)` does `ask` internally), removing
   the consumer's option to `tell` a `Result`-returning handler and
   crash the actor. (See §"The tell-of-fallible-handler trap".)
4. **Capability narrowing** — `LedgerReader` and `LedgerWriter` as
   distinct wrappers around the same underlying actor, exposing
   only `read` or only `append`. Different from Kameo's
   `Recipient<M>` (single-message); a wrapper handles a small
   domain surface.
5. **Domain error vocabulary** — `Result<T, MindError>` instead of
   `Result<T, SendError<Submit, SubmitError>>` at every call site.
6. **Domain verbs over Message construction** — `mind.claim(role,
   scope, reason)` instead of `mind_ref.ask(MindRequest::Claim {
   role, scope, reason })`. Caller writes domain English; wrapper
   constructs the typed Message.
7. **Library publication** — the crate is consumed by code that
   shouldn't construct Kameo Message values directly (external
   library users; downstream crates that want a stable API surface
   that survives Kameo version churn).

### Escape hatch for advanced consumers

When a wrapper exists, advanced consumers may still need raw `ActorRef`
access (testing, custom orchestration). Expose deliberately, not
implicitly:

```rust
impl ClaimNormalizerHandle {
    /// Escape hatch for tests and advanced orchestration that need to
    /// construct messages or use Kameo's full builder surface.
    pub fn actor_ref(&self) -> &ActorRef<ClaimNormalizer> {
        &self.normalizer
    }
}
```

Or expose a narrower Kameo-native capability:

```rust
impl ClaimNormalizerHandle {
    pub fn normalize_recipient(&self)
        -> ReplyRecipient<NormalizeClaim, NormalizedClaim, NormalizeError>
    {
        self.normalizer.recipient()
    }
}
```

This keeps Kameo honest and visible without making it the first API
every domain caller has to learn.

### Don't wrap defensively

A bare wrapper that just holds an `ActorRef<A>` and delegates
method-by-method without adding domain content is still the
speculative-abstraction shape operator/103 retired with
`persona-actor` / `workspace-actor`. We just spent a wave switching
FROM ractor TO Kameo *because* we hadn't wrapped — the migration was
bounded. Don't pre-pay the wrapper cost for a runtime swap that may
never come.

```rust
// Wrong — wrapper adds nothing the type system isn't already enforcing
pub struct CounterHandle {
    counter: ActorRef<Counter>,
}
impl CounterHandle {
    pub async fn increment(&self) -> Result<i64, SendError<Increment>> {
        self.counter.ask(Increment).await
    }
}
```

If the wrapper ends up just delegating method-by-method to `ActorRef`
with no transformation, no error mapping, no lifecycle ownership, no
capability narrowing, drop it and expose `ActorRef<A>` directly.

The discriminator: **does the wrapper meet at least one of the seven
criteria above, or is it type laundering?** If it doesn't meet one,
it's laundering.

---

## Module map (where each thing lives)

The single source of confusion in Kameo's surface is the split
between `kameo::actor::*` and `kameo::error::*`. Memorise this:

| Symbol | Path |
|---|---|
| `Actor`, `Spawn`, `ActorRef`, `WeakActorRef`, `ActorId`, `PreparedActor`, `Recipient`, `ReplyRecipient` | `kameo::actor::*` |
| `Message`, `Context`, `StreamMessage` | `kameo::message::*` |
| `Reply`, `ReplyError`, `ReplySender`, `DelegatedReply`, `ForwardedReply` | `kameo::reply::*` |
| `ActorStopReason`, `PanicError`, `PanicReason`, `SendError`, `RegistryError`, `HookError`, `Infallible` | `kameo::error::*` |
| `bounded(n)`, `unbounded()`, `MailboxSender`, `MailboxReceiver`, `Signal` | `kameo::mailbox::*` (free functions) |
| `RestartPolicy`, `SupervisionStrategy`, `SupervisedActorBuilder` | `kameo::supervision::*` |
| `ACTOR_REGISTRY`, `ActorRegistry` | `kameo::registry::*` (only without `feature = "remote"`) |

The default Kameo cargo features are `["macros", "tracing"]`.
Workspace default: leave `remote` off — Persona is local-process
for now, libp2p is heavy, and the registry API switches signatures
under `remote`. Document an explicit decision in the consumer
crate's `ARCHITECTURE.md` if you turn `remote` on.

The convenience import is:

```rust
use kameo::prelude::*;
```

Add `use kameo::message::StreamMessage;` if you use `attach_stream`,
and `use kameo::error::Infallible;` if you write the `type Error`
field by hand (`#[derive(Actor)]` covers both).

---

## Lifecycle hooks

| Hook | Default | When to override |
|---|---|---|
| `on_start(args, actor_ref) -> Result<Self, Error>` | required | Always; this constructs the actor. |
| `on_message(...)` | dispatches via `BoxMessage::handle_dyn` | Almost never — only for custom buffering or scheduling. |
| `on_panic(&mut self, ref, err) -> ControlFlow<ActorStopReason>` | `Break(Panicked(err))` — actor stops | When the actor should survive specific panic kinds. Inspect `err.reason()` for `PanicReason::HandlerPanic` / `OnMessage` / etc. |
| `on_link_died(&mut self, ref, id, reason) -> ControlFlow<ActorStopReason>` | `Continue` for `Normal`/`SupervisorRestart`, `Break(LinkDied{..})` otherwise | When peer death should be visible without stopping. |
| `on_stop(&mut self, ref, reason) -> Result<(), Error>` | `Ok(())` | When the actor needs to persist or clean up before drop. |
| `next(&mut self, ref, mailbox_rx) -> Result<Option<Signal>, Error>` | `mailbox_rx.recv()` | When the actor merges other input sources via `tokio::select!`. |

Three load-bearing details:

- **`on_start` failure short-circuits.** A returned `Err` (or
  panic) wraps as `PanicError { reason: PanicReason::OnStart }`,
  the `JoinHandle` resolves to `Err(panic_error)`, and **`on_stop`
  is not called**. Under supervision, this is restartable like any
  other `Panicked` reason.
- **`on_stop` panics propagate.** Kameo's harness does *not*
  `catch_unwind` around `on_stop`. A panic in `on_stop` ends the
  actor's tokio task as a panicked task. Errors returned from
  `on_stop` are stored in `shutdown_result` for
  `wait_for_shutdown_result()` to surface — *not* a task panic
  despite stale doc claims to the contrary.
- **`PanicReason` distinguishes the source.** `HandlerPanic`,
  `OnMessage`, `OnStart`, `OnPanic`, `OnLinkDied`, `OnStop`,
  `Next`. Inspect via `err.reason()` and downcast via
  `err.downcast::<MyError>()` or `err.with_str(|s| ...)`.

---

## Messages and replies

Each message kind is a separate `Message<T>` impl on the actor.
Multiple impls compose freely on one actor; dispatch is statically
resolved at the call site.

```rust
struct Increment(i64);
struct Multiply(i64);
struct ReadCount;

impl Message<Increment> for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
impl Message<Multiply>  for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
impl Message<ReadCount> for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
```

Names are full English (per `skills/naming.md`): `Increment` not
`Inc`, `Multiply` not `Mul`, `ReadCount` not `Read` (which would
shadow `std::io::Read`).

The `#[messages]` macro on an `impl` block generates these for you
(see `notes/findings.md` for sub-attributes). Hand-rolled impls are
also fine and often clearer.

### `ask` vs `tell`

| Form | Returns | Use when |
|---|---|---|
| `actor_ref.ask(msg).await` | `Result<R::Ok, SendError<M, R::Error>>` | The reply matters. |
| `actor_ref.tell(msg).await` | `Result<(), SendError<M>>` | Fire-and-forget. |

`actor_ref.ask(msg).await` and `actor_ref.tell(msg).await` work
directly via `IntoFuture`. The builder methods `mailbox_timeout`,
`reply_timeout` (ask only), `try_send`, `blocking_send`, `send_after`
(tell only) are available when you need them.

### Result replies

For a handler with `type Reply = Result<T, MyError>`:

- Ok path: caller's `ask().await` returns `Ok(T)` directly.
- Err path: caller's `ask().await` returns `Err(SendError::HandlerError(MyError))`.

Pattern-match on the variant — don't `unwrap_or` past it:

```rust
match actor_ref.ask(Divide { ... }).await {
    Ok(value)                                          => use_value(value),
    Err(SendError::HandlerError(DivisionError::ByZero)) => …,
    Err(SendError::ActorNotRunning(_))                  => …,
    Err(SendError::Timeout(_))                          => …,
    Err(other)                                          => panic!("unexpected: {other:?}"),
}
```

### The `tell`-of-fallible-handler trap

A handler whose `Reply = Result<_, _>` returning `Err(_)` to a `tell`
becomes `ActorStopReason::Panicked(PanicError { reason: PanicReason::OnMessage })`.
The default `on_panic` stops the actor.

This is the most common Kameo footgun. **Never `tell` a fallible
handler unless you've overridden `on_panic` to recover from
`PanicReason::OnMessage`.** When in doubt, `ask` and ignore the
reply — the error gets routed to the caller as `SendError::HandlerError`
and the actor lives.

### `DelegatedReply<R>`

Use when the handler needs to defer the reply to a spawned task —
i.e., the work behind the reply is async/IO/long-running and the
actor's mailbox should not block on it:

```rust
impl Message<DoSlow> for Worker {
    type Reply = DelegatedReply<String>;

    async fn handle(&mut self, msg: DoSlow, ctx: &mut Context<Self, Self::Reply>) -> Self::Reply {
        let (delegated, sender) = ctx.reply_sender();
        if let Some(tx) = sender {
            tokio::spawn(async move {
                let result = expensive_io(msg).await;
                tx.send(result);
            });
        }
        delegated
    }
}
```

The actor returns immediately; the spawned task replies later. The
caller's `ask().await` blocks until `tx.send(...)` fires (or the
task drops). Without `DelegatedReply`, the actor's mailbox would
block on the slow work — re-creating the hidden-lock failure mode
`skills/actor-systems.md` warns against.

---

## Spawning

| Form | Returns | Notes |
|---|---|---|
| `MyActor::spawn(args)` | `ActorRef<MyActor>` | Sync. Default mailbox capacity 64. |
| `MyActor::spawn_with_mailbox(args, mailbox::bounded(256))` | `ActorRef<MyActor>` | Sync. Custom mailbox. |
| `MyActor::spawn_with_mailbox(args, mailbox::unbounded())` | `ActorRef<MyActor>` | Sync. No backpressure. |
| `MyActor::spawn_in_thread(args)` | `ActorRef<MyActor>` | Sync. Dedicated OS thread; **panics on `current_thread` Tokio runtime**. |
| `MyActor::spawn_link(&peer, args).await` | `ActorRef<MyActor>` | **Async.** Linked to `peer` before run loop starts (avoids the spawn-then-link race). |
| `MyActor::supervise(&parent, args).restart_policy(...).restart_limit(n, dur).spawn().await` | `ActorRef<MyActor>` | **Async.** Supervised. Args must be `Clone + Sync` (or use `supervise_with(factory)`). |
| `MyActor::prepare()` then `prepared.actor_ref()` then `prepared.spawn(args)` | `PreparedActor<MyActor>` | The `ActorRef` is available *before* the run loop starts — useful for pre-registering or pre-enqueueing. |

Use `PreparedActor::run(args).await` when a test needs the actor
value back after shutdown. The pattern is:

```rust
let prepared_actor = Ledger::prepare();
let ledger_ref = prepared_actor.actor_ref().clone();
ledger_ref.tell(OpenItem { title }).await?;
ledger_ref.tell(AddNote { body }).await?;
let stop_task = tokio::spawn(async move { ledger_ref.ask(StopAndRead).await });
let (final_ledger, stop_reason) = prepared_actor.run(Ledger::new()).await?;
assert!(matches!(stop_reason, ActorStopReason::Normal));
assert_eq!(final_ledger.snapshot(), stop_task.await??);
```

This is the clean test shape for "messages changed actor state and I
need to assert on the final actor value."

The default mailbox capacity is **64** (`pub(crate) const
DEFAULT_MAILBOX_CAPACITY: usize = 64`). Macro doc claims 1000;
that's stale. Size deliberately when traffic patterns warrant it.

---

## Test patterns

Prefer push witnesses over sleeps. If a test needs to know that a
handler started, a restart happened, or a link death was observed,
have the actor send on a `oneshot` or `watch` channel at the exact
moment:

```rust
let (started_sender, started_receiver) = tokio::sync::oneshot::channel();
let (release_sender, release_receiver) = tokio::sync::oneshot::channel();

gate.tell(HoldUntilReleased {
    started: started_sender,
    release: release_receiver,
}).await?;

started_receiver.await?;
gate.tell(QueuedBehindHeldMessage).await?;
release_sender.send(())?;
```

For repeated lifecycle events, use `watch`:

```rust
let (generation_sender, mut generation_receiver) = tokio::sync::watch::channel(0);
let actor = RestartingActor::spawn(RestartingActor {
    generation_sender,
});

generation_receiver.changed().await?;
assert_eq!(*generation_receiver.borrow(), 1);
```

A bounded `timeout(...).await.is_err()` is acceptable only when the
test is proving a should-not-fire condition. It is not a substitute
for waiting "long enough."

When asserting shutdown behavior, match the structured
`ActorStopReason`, not just a counter:

```rust
let stop_reason = peer.wait_for_shutdown_result().await?;
assert!(matches!(
    stop_reason,
    ActorStopReason::LinkDied { reason, .. }
        if matches!(*reason, ActorStopReason::Killed)
));
```

For final state assertions, use `PreparedActor::run` as described in
§"Spawning" rather than exposing test-only shared locks.

---

## Supervision

Declarative — no manual restart wiring.

```rust
use kameo::supervision::{RestartPolicy, SupervisionStrategy};

// Parent supervisor — carries data so it isn't a public ZST. The
// child registry tracks who's been spawned for diagnostics; the
// failure_log captures structured restart events.
struct StoreSupervisor {
    children:    HashMap<ActorId, ChildSpec>,
    failure_log: Vec<RestartEvent>,
}

impl Actor for StoreSupervisor {
    type Args = Self;
    type Error = Infallible;
    async fn on_start(args: Self, _: ActorRef<Self>) -> Result<Self, Self::Error> { Ok(args) }

    // Default is OneForOne. Override for OneForAll or RestForOne.
    fn supervision_strategy() -> SupervisionStrategy {
        SupervisionStrategy::OneForAll
    }
}

let supervisor = StoreSupervisor::spawn(StoreSupervisor {
    children:    HashMap::new(),
    failure_log: Vec::new(),
});
let child = Worker::supervise(&supervisor, WorkerArgs { … })
    .restart_policy(RestartPolicy::Permanent)
    .restart_limit(5, Duration::from_secs(10))
    .spawn()
    .await;
```

| Defaults | Value |
|---|---|
| `RestartPolicy` | `Permanent` (always restart) |
| `SupervisionStrategy` | `OneForOne` (only failed child restarts) |
| `restart_limit` | 5 restarts per 5 seconds |

Restart-policy semantics:

| Policy | On panic | On handler error | On normal exit |
|---|---|---|---|
| `Permanent` (default) | restart | restart | restart |
| `Transient` | restart | restart | no restart |
| `Never` | no restart | no restart | no restart |

Strategy semantics:

| Strategy | Behavior |
|---|---|
| `OneForOne` (default) | Only the failed child restarts. |
| `OneForAll` | All children restart together when any fails. |
| `RestForOne` | Failed child + all younger siblings (spawned later) restart. |

`restart_limit(n, window)` is reset-after-quiet, not sliding. Past
the limit, the supervisor's `on_link_died` fires for the dead child;
default behavior stops the supervisor.

**Restart reconstructs Self from Args, not from memory.** This is
the load-bearing supervision rule. When Kameo restarts an actor:

- The mailbox survives — queued messages reach the new instance;
  the message currently being processed is lost.
- **The actor's mutable state does not survive.** `on_start` runs
  again with the original `Args` (or a fresh value from
  `supervise_with(factory)`). A counter the crashed instance had
  bumped to 12 reads back as 0 (or whatever `Args` rebuilds to).
- Anything that *must* survive restart belongs outside the actor:
  in the component's own `sema-db`-backed redb (durable state via
  redb+rkyv), in shared `Arc<AtomicU32>` (cheap counters), or in
  `Args` itself (so each restart sees the same starting value).

Kameo makes restart policy easy to express; it does **not** make
restart semantics automatically safe. Design with reconstruction
in mind from the start.

### `OneForAll` / `RestForOne` can bypass `RestartPolicy::Never`

Strategy and policy compose, but not in the way the docs suggest.
When a sibling failure triggers `OneForAll` or `RestForOne`,
Kameo's coordinated restart paths can call sibling factories
directly — apparently bypassing each child's individual
`RestartPolicy::Never`. A child you set as `Never` may still be
respawned if a sibling failure invokes a strategy that restarts
the whole group.

```rust
// supervisor uses OneForAll
fn supervision_strategy() -> SupervisionStrategy {
    SupervisionStrategy::OneForAll
}

// child A: explicitly Never
let child_a = WorkerA::supervise(&supervisor, args)
    .restart_policy(RestartPolicy::Never)
    .spawn()
    .await;

// child B: Permanent
let child_b = WorkerB::supervise(&supervisor, args)
    .restart_policy(RestartPolicy::Permanent)
    .spawn()
    .await;

// When child B panics, OneForAll triggers — child A's `Never`
// is bypassed; both children get respawned.
```

If your supervision strategy is `OneForAll` or `RestForOne`,
test the bypass behavior explicitly. `RestartPolicy::Never`
doesn't always mean what it says under coordinated strategies.

The safe combinations:

| Strategy | Per-child Policy | Behavior |
|---|---|---|
| `OneForOne` | Any | Each child's policy is honored independently |
| `OneForAll` / `RestForOne` | All children share the same policy | Predictable |
| `OneForAll` / `RestForOne` | Mixed policies | **Coordinated paths may bypass `Never`; test explicitly** |

---

## Mailbox

Two factories at module level — there is no `Mailbox` type with
methods on it:

```rust
use kameo::mailbox;

let (tx, rx) = mailbox::bounded(64);    // backpressure on full
let (tx, rx) = mailbox::unbounded();    // unlimited; OOM risk under load
```

Bounded is the default. `tell().await` waits when full;
`tell().try_send()` returns `SendError::MailboxFull(msg)`;
`tell().mailbox_timeout(d).send().await` waits up to `d` then fails
with `Timeout`. Pick the form at the call site; there are no
overflow policies built in.

`ask().await` blocks twice: first on enqueue (mailbox capacity),
then on the reply (oneshot). `ask().reply_timeout(d).send().await`
caps the reply wait.

---

## Local registry

Without `feature = "remote"`, the registry is a process-global
`Mutex<HashMap>` at `kameo::registry::ACTOR_REGISTRY`.

```rust
let actor_ref = MyActor::spawn(MyActor { … });
actor_ref.register("namespace::name")?;        // sync; returns RegistryError on collision

let found: Option<ActorRef<MyActor>> = ActorRef::<MyActor>::lookup("namespace::name")?;
```

| Behavior | Detail |
|---|---|
| Collision | `Err(RegistryError::NameAlreadyRegistered)` — never overwrites. |
| Unknown name | `Ok(None)`. |
| Actor death | Entry auto-removed (per the 0.19 fix). |
| Strong/weak | Local registry holds **strong** refs — registration keeps the actor alive. |

When `feature = "remote"` is on, `register` and `lookup` become
async, take `Arc<str>`, require `A: RemoteActor`, and use libp2p
Kademlia. Different shape; named here only so consumers don't try
to call the local form on a remote build.

---

## Streams

`actor_ref.attach_stream(stream, started_value, finished_value)`
spawns a Tokio task that:

1. `tell(StreamMessage::Started(started_value))`
2. For each item: `tell(StreamMessage::Next(item))`
3. `tell(StreamMessage::Finished(finished_value))` once the stream
   ends.

The actor implements `Message<StreamMessage<M, T, F>>` to receive
all three envelopes. Handler typically uses `type Reply = ();`.

The returned `JoinHandle<Result<S, SendError<...>>>` resolves with
the unconsumed stream if the actor stops mid-stream — useful for
recovery. Backpressure on the actor's mailbox naturally throttles
the producer.

---

## Links

`actor_ref.link(&peer_ref).await` creates a bidirectional link.
When either dies, the survivor's `on_link_died(id, reason)` fires.
Default behavior continues for `Normal` / `SupervisorRestart`,
breaks (stops the survivor) for `Killed` / `Panicked` / `LinkDied`.

Two link patterns emerge — keep them separate in the design:

- **Supervision links** — death should propagate. Use the default
  `on_link_died`; the survivor stops on abnormal peer death and
  the supervisor restarts both per its strategy.
- **Observational links** — death should be observed without
  stopping the survivor. Override `on_link_died` to record the
  event (counter, channel send, sema row) and return
  `Ok(ControlFlow::Continue(()))` for all reasons.

A given actor may participate in both kinds — fail-fast on its
sibling, observe a downstream watchdog. Be deliberate per pair.

`actor_ref.unlink(&peer_ref).await` removes the link bidirectionally.

Use `spawn_link` instead of `spawn` + `link` when the link must be
established before the actor can fail — avoids the race where the
actor dies before the link is installed.

---

## Workspace conventions on top of Kameo

These are workspace rules per `skills/actor-systems.md`, applied to
Kameo's surface. They are not Kameo's defaults; they are how this
workspace uses Kameo.

- **Public actor nouns carry data.** Kameo permits ZST actors
  (`struct Pinger;`) but the workspace forbids them as the public
  surface. The actor type IS the state; if you don't have any
  fields, you don't have an actor — you have a verb. Find the
  noun.
- **One actor per file when the actor is durable enough to name.**
  `src/actors/store_supervisor.rs`, `src/actors/claim_normalize.rs`,
  etc. Co-locate the `Actor` impl, the `Message<T>` impls for
  that actor, and the message/reply types in one file.
- **No raw `Spawn::spawn` outside the runtime root.** Spawn happens
  at the supervision tree's root; child spawns go through
  `supervise(&parent, ...).spawn().await`.
- **No blocking inside a normal handler.** A handler that sleeps,
  polls, or runs synchronous IO has recreated a hidden lock per
  `skills/actor-systems.md`. Move the wait into a dedicated
  supervised actor (`CommandActor`, `FileReadActor`, etc.) and
  send it a typed message. The three concrete shapes such actors
  take are documented below in §"Blocking-plane templates".
- **Tests live in `tests/`, not `#[cfg(test)] mod tests`.** Per
  `skills/rust-discipline.md` — and the kameo-testing repo
  demonstrates the shape.
- **Don't reach for `remote` until cross-process actors are
  designed.** The local registry semantics differ; the libp2p
  surface is heavy. Document the decision in the consumer's
  `ARCHITECTURE.md` if you enable it.

---

## Blocking-plane templates

The no-blocking-handler rule says *move the wait into a dedicated
supervised actor*. Three concrete templates land that rule, each
fitting a different shape of blocking work. They live side-by-side
here so consumers can pick the right one without inventing a fourth.

### Template 1 — `spawn_blocking` + `DelegatedReply` detach

For an actor whose blocking work is short-to-medium and occasional
(subprocess invocations, blocking IO leaves, bounded CPU bursts).
The handler returns *immediately*; the blocking work runs on Tokio's
blocking pool; the reply ships back when it completes. The actor's
mailbox doesn't stall.

```rust
impl Message<DeliverToHarness> for HarnessDelivery {
    type Reply = DelegatedReply<DeliveryResult>;

    async fn handle(
        &mut self,
        message: DeliverToHarness,
        context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        let (delegated, sender) = context.reply_sender();
        context.spawn(async move {
            let outcome = tokio::task::spawn_blocking(move || {
                HarnessDelivery::deliver(message)  // sync work
            }).await;
            if let Some(sender) = sender {
                sender.send(outcome.into());
            }
        });
        delegated
    }
}
```

Live reference: `persona-router::HarnessDelivery`
(`src/harness_delivery.rs:88-120`).

The actor's ARCH must explicitly name it as the dedicated blocking
plane for the backend it owns. The detach is invisible without that
ARCH-level naming.

### Template 2 — Dedicated OS thread (`spawn_in_thread`)

For a state-bearing actor with *frequent* sync work that would burn
through per-call `spawn_blocking` invocations — typically a
redb-backed store, a file watcher, anything where every message
touches the same sync backend.

```rust
fn spawn_in_thread(store: StateStore) -> ActorRef<StateStore> {
    let (actor_ref, mailbox) = kameo::actor::Mailbox::bounded(64);
    std::thread::spawn(move || {
        let runtime = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .expect("dedicated store runtime");
        runtime.block_on(store.run_loop(mailbox));
    });
    actor_ref
}
```

Live reference: `chroma::StateStore` (`src/state.rs:61`).

The actor runs on its own OS thread, off the Tokio worker pool
entirely. One mailbox, one writer, one thread — cleaner than per-call
detach for high-frequency stores. Pair with a typed schema and the
sema-family pattern from `rust-discipline.md` §"sema-family pattern".

### Template 3 — `tokio::process` + bounded `timeout` + `kill_on_drop`

For process-exec work where async equivalents exist
(`tokio::process::Command` is the common case). Often cleaner than
Template 1 because the whole handler stays properly async — no
detach machinery.

```rust
async fn run_dconf_write(key: &str, value: &str) -> Result<(), ApplyError> {
    tokio::time::timeout(Duration::from_secs(1), async {
        let mut child = tokio::process::Command::new("dconf")
            .args(["write", key, value])
            .kill_on_drop(true)
            .spawn()
            .map_err(ApplyError::spawn)?;
        let status = child.wait().await.map_err(ApplyError::wait)?;
        if !status.success() {
            return Err(ApplyError::exit(status));
        }
        Ok(())
    })
    .await
    .map_err(|_| ApplyError::timeout())?
}
```

Live reference: `chroma::DesktopThemeConcern::run_dconf_write`
(`src/theme.rs:493-510`).

Bounded by `timeout`; child killed on drop or timeout; no
`spawn_blocking` needed. When `tokio::process` is available, prefer
this over `std::process::Command::output()` wrapped in detach
machinery.

### Picking a template

| Shape of work | Template |
|---|---|
| occasional short blocking call, no async equivalent | 1 — `spawn_blocking` + `DelegatedReply` |
| frequent sync DB / store / watcher | 2 — dedicated OS thread |
| process-exec with async API (`tokio::process`) | 3 — `tokio::process` + timeout |

**Anti-template (the violation):** doing the blocking work inline in
an `async fn handle()` with no detach. The actor's mailbox stalls
and the Tokio worker thread it ran on starves any sibling actors
scheduled there. See `skills/actor-systems.md` §"No blocking" for
the full rule and `~/primary/reports/designer/113-actor-blocking-audit.md`
for a worked example (`persona-wezterm::TerminalDelivery`).

---

## Anti-patterns and gotchas

- **`tell`-ing a fallible handler.** A `Result::Err` from a
  `tell`'d handler crashes the actor by default. `ask` instead, or
  override `on_panic` to recover from `PanicReason::OnMessage`.
- **Self-`ask` from within a handler.** Deadlocks; the handler is
  busy and can't reply to itself. Debug+tracing builds emit a
  warning at the call site. Refactor: split the work into a
  separate method or a separate actor.
- **`spawn_in_thread` under `#[tokio::test]`.** Default test flavor
  is `current_thread` — `spawn_in_thread` panics with *"threaded
  actors are not supported in a single threaded tokio runtime"*.
  Use `#[tokio::test(flavor = "multi_thread")]`.
- **`#[derive(Actor)] #[actor(mailbox = bounded(64))]` doesn't
  work.** Documented but unparsed; only `#[actor(name = "...")]`
  is implemented. Use `spawn_with_mailbox` instead.
- **`PendingReply` (from `ask().enqueue()`) blocks the caller.**
  The actor still runs; the reply sits in the oneshot until you
  await it. If you forget to await/drop, the caller hangs.
- **Pipelined `tell(panic_trigger) + ask(other)` races on_panic
  recovery.** Even with `on_panic` returning `Continue(())`, the
  second message's reply oneshot can be set up before recovery
  finishes — caller observes `ActorStopped`. Use `ask(panic_trigger)`
  (which awaits past the panic AND the recovery), then `ask(other)`
  on a known-recovered actor. See
  `kameo-testing/tests/lifecycle.rs::on_panic_continue_keeps_stateful_actor_alive_after_handler_panic`.
- **`DelegatedReply`'s spawned task is not supervised actor work.**
  Errors from the detached future do not call the actor's
  `on_panic`; they route to the global error hook (or the original
  ask caller, for ask-shaped delegations). Use `DelegatedReply`
  for short reply deferrals; for real long work, supervise a
  dedicated actor.
- **`on_stop` panics propagate as task panics.** No `catch_unwind`
  around `on_stop` in 0.20. Don't panic in stop hooks; return
  `Err` instead.
- **`Args = Self` requires `Clone + Sync` for supervision.**
  `MyActor::supervise(&parent, args)` needs `Args: Clone + Sync`
  to clone for each restart. If `Self` isn't `Clone + Sync`, use
  `supervise_with(|| MyActor { ... })` with a factory closure
  instead.
- **`RpcReply` does not exist.** References in older workspace
  reports are stale (likely confusion with ractor's
  `RpcReplyPort`). Use `DelegatedReply<R>`, `ForwardedReply<M, R>`,
  or `ReplySender<R>` directly.

For surprises surfaced under test, see
`/git/github.com/LiGoldragon/kameo-testing/notes/findings.md`.

---

## See also

- this workspace's `skills/actor-systems.md` — the architectural
  discipline this skill serves.
- this workspace's `skills/rust-discipline.md` — the Rust style
  Kameo code follows.
- `/git/github.com/LiGoldragon/kameo-testing` — designer's test
  bed; every behavior named above is exercised by a passing test.
- `/git/github.com/LiGoldragon/kameo-testing-assistant` —
  designer-assistant's complementary test bed; data-bearing
  patterns, restart-from-args reconstruction, observational
  link-death survival.
- `~/primary/reports/designer-assistant/5-kameo-testing-assistant-findings.md`
  — designer-assistant's findings (maturity signals, restart
  reconstruction, supervision-vs-observational link split). Folded
  into this skill.
- `/git/github.com/LiGoldragon/kameo-testing/notes/findings.md` —
  source-grounded research notes behind the skill's claims.
- `https://github.com/tqwewe/kameo` — upstream source (v0.20.0
  tag is the workspace's pinned baseline).
- `https://docs.rs/kameo/0.20.0/kameo/` — rustdoc reference.
