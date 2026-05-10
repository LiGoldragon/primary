# 102 — Kameo deep dive

*Designer report. Deep research into the Kameo actor framework
(`https://docs.rs/kameo`, source at
`https://github.com/tqwewe/kameo`, version 0.20.0 as of
2026-05-10). Pure facts + workspace-fit analysis. Switch
decision is the user's, not surfaced here.*

---

## 0 · What Kameo is

A lightweight Rust actor framework, MIT/Apache-2.0 dual
licensed, single-author (tqwewe), at version 0.20.0. Built on
Tokio. Optional libp2p-based distribution. Production users
include Caido (security tooling). Author advertises it as a
high-performance fault-tolerant actor library that scales
from local single-node concurrency to network-distributed
systems.

Core dependencies: `tokio`, `futures`, `dyn-clone`,
`downcast-rs`. Optional: `libp2p` (remote actors),
`opentelemetry`, `metrics`, `tracing`, `kameo_macros`
(derive macros), `serde`/`rmp-serde` (remote
serialization).

---

## 1 · The Actor trait — the load-bearing fact

From `https://github.com/tqwewe/kameo/blob/main/src/actor.rs`:

```rust
pub trait Actor: Sized + Send + 'static {
    /// Arguments to initialize the actor.
    /// "Its common for `Args = Self`, allowing the actors
    /// state to be passed directly."
    type Args: Send;

    /// Actor error type, used by lifecycle hooks.
    type Error: ReplyError;

    fn name() -> &'static str { type_name::<Self>() }

    fn supervision_strategy() -> SupervisionStrategy {
        SupervisionStrategy::default()  // OneForOne
    }

    /// Construct Self from Args. Self IS the actor.
    fn on_start(
        args: Self::Args,
        actor_ref: ActorRef<Self>,
    ) -> impl Future<Output = Result<Self, Self::Error>> + Send;

    fn on_message(
        &mut self,
        msg: BoxMessage<Self>,
        actor_ref: ActorRef<Self>,
        tx: Option<BoxReplySender>,
        stop: &mut bool,
    ) -> impl Future<Output = Result<(), Box<dyn ReplyError>>> + Send;

    fn on_panic(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        err: PanicError,
    ) -> impl Future<Output = Result<ControlFlow<ActorStopReason>, Self::Error>> + Send;

    fn on_link_died(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        id: ActorId,
        reason: ActorStopReason,
    ) -> /* … */;

    fn on_stop(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        reason: ActorStopReason,
    ) -> impl Future<Output = Result<(), Self::Error>> + Send;
}
```

**Three load-bearing differences from ractor's `Actor` trait:**

1. **`on_start` returns `Self`.** ractor's `pre_start(&self, _, args) -> Self::State` keeps `Self` and `State` distinct. Kameo collapses them: `Self` IS the state.
2. **There is no `Self::State` associated type.** Only `Args` and `Error`. The actor's data lives on `Self`.
3. **Every lifecycle hook takes `&mut self`.** `on_message`, `on_panic`, `on_link_died`, `on_stop` — all mutable self. ractor's hooks take `&self` + `&mut state`.

**The documented common case is `Args = Self`** — the user
passes the constructed actor directly:

```rust
#[derive(Actor)]
struct Counter { count: i64 }

let actor_ref = Counter::spawn(Counter { count: 0 });
```

The `#[derive(Actor)]` macro emits a default impl with
`Args = Self`, `Error = Infallible`, and a passthrough
`on_start` that returns the Args unchanged. Trivial actors
get this for free.

---

## 2 · The Message trait — per-kind, not one-enum

Kameo splits message handling across one trait impl per
message kind, not one big `Msg` enum:

```rust
struct Inc { amount: i64 }
struct Dec { amount: i64 }
struct Read;

impl Message<Inc> for Counter {
    type Reply = i64;
    async fn handle(&mut self, msg: Inc, _ctx: &mut Context<Self, Self::Reply>) -> i64 {
        self.count += msg.amount;
        self.count
    }
}

impl Message<Dec> for Counter { /* … */ }
impl Message<Read> for Counter { /* … */ }
```

Trait shape (from `src/message.rs`):

```rust
pub trait Message<T: Send + 'static>: Actor {
    type Reply: Reply;

    fn name() -> &'static str { type_name::<T>() }

    fn handle(
        &mut self,
        msg: T,
        ctx: &mut Context<Self, Self::Reply>,
    ) -> impl Future<Output = Self::Reply> + Send;
}
```

Per-message Reply type. The `Context<A, R>` carries the
actor's own `ActorRef`, an optional reply sender, and a stop
flag (`ctx.stop()` halts after the current message).

**Implications:**

- New message kinds = new `Message<Kind> for MyActor` impls
  (often each in its own file).
- Reply types vary per message — no need for one giant Reply
  enum.
- The `messages!` derive macro can wire many message kinds
  in one block; explicit impls are also fine.
- CQRS framing is built in: Messages mutate state; Queries
  (separate trait) are read-only and can run concurrently.

The `DelegatedReply<T>` pattern lets a handler defer reply
to a spawned task — useful for handlers that wait on async
IO without blocking the mailbox:

```rust
impl Message<Msg> for MyActor {
    type Reply = DelegatedReply<String>;
    async fn handle(&mut self, msg: Msg, ctx: &mut Context<…>) -> Self::Reply {
        let (delegated, sender) = ctx.reply_sender();
        if let Some(tx) = sender {
            tokio::spawn(async move {
                tokio::time::sleep(Duration::from_secs(1)).await;
                tx.send("done!".to_string());
            });
        }
        delegated
    }
}
```

---

## 3 · Spawning — `Counter::spawn(Counter { … })`

The `Spawn` trait (in `actor::Spawn`) provides the spawn
methods. Common forms:

```rust
// Default — into a tokio task with default mailbox (cap 64).
let actor_ref = Counter::spawn(Counter { count: 0 });

// With a custom mailbox.
let actor_ref = Counter::spawn_with_mailbox(
    Counter { count: 0 },
    Mailbox::bounded(256),
);

// Supervised under a parent — see §5.
let actor_ref = Worker::supervise(&parent_ref, Worker)
    .restart_policy(RestartPolicy::Transient)
    .restart_limit(5, Duration::from_secs(10))
    .spawn()
    .await;

// Prepared — get the ActorRef before the actor runs.
let prepared = MyActor::prepare();
prepared.actor_ref().tell("greet me!").await?;
prepared.run(MyActor).await;     // run in current task
prepared.spawn(MyActor);         // spawn in tokio task
prepared.spawn_in_thread(MyActor); // spawn in OS thread
```

The `PreparedActor<A>` pattern decouples mailbox creation
from actor execution — useful for tests, sync run-in-place,
and pre-spawn message queueing.

`spawn_in_thread` requires multi-threaded tokio runtime
(panics on `current_thread` flavor).

---

## 4 · Lifecycle hooks — all on `&mut self`

```rust
impl Actor for MyActor {
    type Args = Self;
    type Error = Infallible;

    async fn on_start(args: Self, actor_ref: ActorRef<Self>) -> Result<Self, Self::Error> {
        // initialization happens here; messages sent internally during
        // on_start are prioritized before externally-sent messages
        Ok(args)
    }

    async fn on_panic(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        err: PanicError,
    ) -> Result<ControlFlow<ActorStopReason>, Self::Error> {
        // default: stop the actor with ActorStopReason::Panicked(err)
        // override to: continue, restart, escalate
        Ok(ControlFlow::Break(ActorStopReason::Panicked(err)))
    }

    async fn on_link_died(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        id: ActorId,
        reason: ActorStopReason,
    ) -> Result<ControlFlow<ActorStopReason>, Self::Error> {
        // default: stop unless reason is Normal
        // override to: stay alive on linked death
    }

    async fn on_stop(
        &mut self,
        actor_ref: WeakActorRef<Self>,
        reason: ActorStopReason,
    ) -> Result<(), Self::Error> {
        // cleanup before drop
        Ok(())
    }
}
```

`PanicError` can be downcast into `Self::Error`, the
message-handler error, a `String` (from `panic!`), or any
type passed to `panic_any!`.

---

## 5 · Supervision — declarative restart policies

From `src/supervision.rs`:

**Restart policies** (when to restart):

| Policy | On panic | On error | On normal exit |
|---|---|---|---|
| `Permanent` | restart | restart | restart |
| `Transient` | restart | restart | no restart |
| `Never` | no restart | no restart | no restart |

**Supervision strategies** (which children to restart):

| Strategy | Behavior |
|---|---|
| `OneForOne` (default) | Only restart the failed child |
| `OneForAll` | Restart all children when any fails |
| `RestForOne` | Restart the failed child + all younger siblings |

Supervisors declare their strategy via `Actor::supervision_strategy`:

```rust
impl Actor for Supervisor {
    type Args = ();
    type Error = Infallible;

    fn supervision_strategy() -> SupervisionStrategy {
        SupervisionStrategy::OneForAll
    }

    async fn on_start(_: Self::Args, actor_ref: ActorRef<Self>) -> Result<Self, Self::Error> {
        let worker = Worker::supervise(&actor_ref, Worker)
            .restart_policy(RestartPolicy::Transient)
            .restart_limit(5, Duration::from_secs(10))
            .spawn()
            .await;
        Ok(Supervisor)
    }
}
```

`restart_limit(n, window)` stops restart storms — at most `n`
restarts within `window`; subsequent failure escalates.

The supervision pattern is structurally Erlang/OTP. ractor
has supervision via links + monitors but no declarative
strategy enum.

---

## 6 · Mailbox + backpressure

Default mailbox capacity is **64** (constant
`DEFAULT_MAILBOX_CAPACITY` in `src/actor.rs`). Bounded by
default — backpressure-aware. Unbounded available.

Construction:

```rust
let bounded = Mailbox::bounded(256);
let unbounded = Mailbox::unbounded();
let actor_ref = MyActor::spawn_with_mailbox(args, bounded);
```

When a bounded mailbox is full, `tell` and `ask` await until
space is available. This is the workspace's no-polling
discipline expressed at the framework level — producers wait
for the consumer's mailbox to drain.

---

## 7 · Registry + distributed actors

**Local registry** — actors register under a string key for
lookup:

```rust
let actor_ref = MyActor::spawn(MyActor::default());
actor_ref.register("my_actor")?;

// Elsewhere:
let found: Option<ActorRef<MyActor>> = ActorRef::lookup("my_actor");
```

**Distributed actors** (feature-gated `remote`):

Built on libp2p. Supports TCP/IP, WebSockets, QUIC. Actors
register on the network; remote peers look them up via
`RemoteActorRef::<MyActor>::lookup(name).await`. Messages
serialize via `serde` + `rmp-serde` (MessagePack).

The remote feature pulls in `libp2p` (large dep tree). For
local-only systems, leave it off.

---

## 8 · Streams — `attach_stream`

Actors can be attached to streams; each item arrives as a
`StreamMessage<T, S, F>` message:

```rust
pub enum StreamMessage<T, S, F> {
    Next(T),       // each item from the stream
    Started(S),    // stream attachment fact
    Finished(F),   // stream end
}
```

Useful for ingesting Tokio streams, watch channels, or
broadcast channels into an actor's mailbox without the actor
itself owning a polling loop.

---

## 9 · `#[derive(Actor)]` + `#[messages]` macros

The `kameo_macros` crate (optional; `macros` feature) provides:

- **`#[derive(Actor)]`** — emits trivial `Actor` impl with
  `Args = Self`, `Error = Infallible`, passthrough
  `on_start`. For actors with no custom lifecycle.
- **`#[derive(Reply)]`** — derive Reply for plain return
  types.
- **`#[messages]`** — block-level macro to wire many
  `Message<Kind>` impls in one place.
- **`#[derive(RemoteActor)]` / `#[remote_message]`** — for
  the distributed feature.

Without the `macros` feature, all impls are written by hand
— more verbose but fully explicit (which the workspace
generally prefers).

---

## 10 · Comparison to ractor — concrete

| Concern | ractor 0.15 | Kameo 0.20 |
|---|---|---|
| Self carries state | No — separate `Self::State` | **Yes — Self IS the state** |
| Construction signature | `pre_start(&self, _, Self::Arguments) -> Self::State` | **`on_start(Self::Args, ActorRef<Self>) -> Self`** |
| Handler signature | `handle(&self, _, msg, &mut state)` | **`handle(&mut self, msg, ctx)`** |
| Lifecycle hooks `&self` vs `&mut self` | `&self` + `&mut state` | **`&mut self` everywhere** |
| Message vocabulary | Single `Msg` enum per actor | **Per-kind `Message<T>` impls** |
| Reply mechanism | `RpcReplyPort` per message | `type Reply` on Message impl |
| Supervision policy | Manual via links/monitors | **Declarative `RestartPolicy` + `SupervisionStrategy` + `restart_limit`** |
| Default mailbox | Configurable | Bounded 64 by default |
| Distributed | No (in-process) | **Yes** (libp2p, optional) |
| Registry | Named via `spawn` | Explicit `register("name")` |
| Streams as input | Manual | **`attach_stream`** |
| Tokio runtime | Yes | Yes |
| Sync/CurrentThread support | Yes | Tokio-only; `spawn_in_thread` requires multi-thread runtime |
| Macros | `cast!` / `call!` | `#[derive(Actor)]` / `#[messages]` |
| Test ergonomics | Sync-façade pattern in lore | `PreparedActor::run` for in-task execution |
| Battle-testing | More mature; in production at WhatsApp tooling, etc. | Younger; growing user base; v0.20 |

---

## 11 · Workspace fit — against `~/primary/skills/actor-systems.md`

The skill names eight load-bearing rules. Kameo against each:

| Skill rule | Fit | Why |
|---|---|---|
| Actor noun carries data | **Native** | `Self` IS the actor; `Args = Self` is the documented common case |
| Methods on the noun | **Native** | All hooks on `&mut self`; methods on `MyActor` directly |
| Typed mailbox | **Native** | Bounded by default; per-message types |
| Supervision is part of design | **Strong** | Declarative `RestartPolicy` + `SupervisionStrategy`; restart limits |
| Actor topology introspection | **Manual** | Registry + `ActorId` + links; no built-in topology dump |
| Push-only / no polling | **Native** | Mailbox is the push channel; no scheduled wakeups by default |
| No shared locks | **Native** | Same as ractor — message passing model |
| No public ZST actor nouns | **Native** | The framework's actor IS the data; no ZST behavior marker pattern |

The "manual topology introspection" is the only gap — no
built-in way to dump the supervision tree as typed records.
Easy to add via a separate crate (a `TopologyActor` that
collects link state on registration).

The skill's §"Rust shape" target shape — `ClaimNormalize`
struct with fields, `ClaimNormalize::open(args)` returning
`Self`, `&mut self` handlers — is **literally Kameo's
shape**, not a target Kameo needs adapting to.

---

## 12 · Code shape — what consumer code reads like

```rust
use kameo::{Actor, message::{Context, Message}, actor::ActorRef};
use kameo::error::Infallible;

// The actor IS the data. No ZST. No separate State.
pub struct ClaimNormalize {
    config:    NormalizationConfig,
    in_flight: HashMap<RequestId, WirePath>,
    metrics:   ClaimNormalizeMetrics,
}

impl ClaimNormalize {
    fn validate(&self, path: &WirePath) -> Result<(), ClaimNormalizeFailure> { /* … */ }
    fn collapse_double_slashes(&self, path: WirePath) -> WirePath { /* … */ }
}

impl Actor for ClaimNormalize {
    type Args = Self;     // documented common case
    type Error = ClaimNormalizeFailure;

    async fn on_start(state: Self, _ref: ActorRef<Self>) -> Result<Self, Self::Error> {
        Ok(state)
    }
}

// One impl per message kind.
pub struct Normalize { pub operation: OperationId, pub path: WirePath }

impl Message<Normalize> for ClaimNormalize {
    type Reply = Result<NormalizedScope, ClaimNormalizeFailure>;

    async fn handle(
        &mut self,
        msg: Normalize,
        _ctx: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.in_flight.insert(msg.operation, msg.path.clone());
        self.validate(&msg.path)?;
        let collapsed = self.collapse_double_slashes(msg.path);
        let scope = NormalizedScope::from(collapsed);
        self.metrics.normalize_count += 1;
        self.in_flight.remove(&msg.operation);
        Ok(scope)
    }
}

// Spawning + use.
let normalizer = ClaimNormalize::spawn(ClaimNormalize {
    config:    NormalizationConfig::default(),
    in_flight: HashMap::new(),
    metrics:   ClaimNormalizeMetrics::default(),
});

let scope = normalizer.ask(Normalize { operation, path }).await?;
```

Comparison — same actor in ractor:

```rust
pub struct ClaimNormalize;  // ZST behavior marker

pub struct ClaimNormalizeState {
    config:    NormalizationConfig,
    in_flight: HashMap<RequestId, WirePath>,
    metrics:   ClaimNormalizeMetrics,
}

pub struct ClaimNormalizeArgs { config: NormalizationConfig }

pub enum ClaimNormalizeMsg {
    Normalize { operation: OperationId, path: WirePath, reply: RpcReplyPort<…> },
}

impl Actor for ClaimNormalize {
    type State     = ClaimNormalizeState;
    type Arguments = ClaimNormalizeArgs;
    type Msg       = ClaimNormalizeMsg;

    async fn pre_start(&self, _, args) -> Result<Self::State, _> {
        Ok(ClaimNormalizeState { config: args.config, in_flight: HashMap::new(), metrics: Default::default() })
    }

    async fn handle(&self, _, msg, state: &mut Self::State) -> Result<(), _> {
        match msg {
            ClaimNormalizeMsg::Normalize { operation, path, reply } => {
                let result = state.normalize(operation, path);
                let _ = reply.send(result);
                Ok(())
            }
        }
    }
}
```

Five named types (Self, State, Args, Msg, plus reply enum)
in ractor; one named type (Self) plus one Message kind in
Kameo. The methods that do the real work live in different
places: ractor's are on `ClaimNormalizeState`; Kameo's are
on `ClaimNormalize`.

---

## 13 · Concerns and unknowns

Things I cannot answer from documentation alone:

1. **Maturity / battle-testing.** Kameo 0.20 is younger
   than ractor 0.15. Production users (Caido) exist, but
   ractor has more public deployment evidence. Both are
   single-author projects.
2. **Long-term maintenance.** Single-author risk applies to
   both. Neither is owned by a major foundation.
3. **Performance under high actor count.** Skills/actor-systems.md
   anticipates "hundreds of actors normal." Documentation
   doesn't quantify per-actor cost; Kameo's blog post
   *"Comparing Rust Actor Libraries"* (linked from the
   README) may have numbers. Empirical test needed.
4. **Topology dump for architecture-truth tests.** Kameo
   has no built-in topology export. Workspace would need a
   small `TopologyRegistryActor` that intercepts registration.
   ractor's situation is similar.
5. **Migration complexity if persona-mind starts on ractor
   then switches.** Each `ractor::Actor` impl rewrites to a
   `kameo::Actor` impl. The trait reshape is mechanical
   per-actor (split `Msg` enum into per-kind types; move
   `State` fields onto `Self`; change `pre_start` to
   `on_start`; change `&self`+`&mut state` to `&mut self`)
   but adds up across many actors.
6. **Determinism in tests.** Neither framework ships a
   deterministic scheduler. Workspace-side test fixture
   needed in either case.

---

## 14 · What this report does not do

- **Does not recommend whether to switch.** That's the
  user's decision per the prior chat exchange.
- **Does not propose a wrapper crate.** Both `persona-actor`
  and `workspace-actor` are explicitly retired per
  operator/103; not revived here.
- **Does not propose hiding ractor.** If ractor is the
  chosen runtime, consumer code uses it directly per
  operator/103 §5.
- **Does not draft a migration plan.** That's the
  implementer's lane (operator / operator-assistant) once
  the runtime decision is made.

---

## See also

- `https://docs.rs/kameo/latest/kameo/` — top-level API docs
  (kameo 0.20.0, fetched 2026-05-10).
- `https://github.com/tqwewe/kameo` — source repo; lifecycle
  source quoted from `src/actor.rs`, message source from
  `src/message.rs`, supervision from `src/supervision.rs`.
- `https://docs.page/tqwewe/kameo` — "The Kameo Book"
  (tutorials and advanced topics; not consumed for this
  report).
- `https://theari.dev/blog/comparing-rust-actor-libraries/`
  — blog post comparing Actix, Coerce, Kameo, Ractor, Xtra
  (linked from kameo README; not consumed for this report).
- `~/primary/skills/actor-systems.md` — the workspace's
  actor discipline skill; §"Rust shape" target is
  structurally Kameo's native shape.
- `~/primary/reports/operator/103-actor-abstraction-drift-correction.md`
  — the corrective report that retired `persona-actor` /
  `workspace-actor`; §9 row 5 defaults to "no Kameo switch
  yet" pending direct-ractor pain evidence.
- `~/primary/repos/lore/rust/ractor.md` — current ractor
  reference for the workspace.
