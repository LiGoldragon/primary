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

The falsifiable source for every claim below is
`/git/github.com/LiGoldragon/kameo-testing` — every substantive
behavior cites a test in that repo.

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

pub struct ClaimNormalize {
    in_flight:    HashMap<RequestId, WirePath>,
    max_in_flight: usize,
    metrics:      ClaimNormalizeMetrics,
}

impl Actor for ClaimNormalize {
    type Args  = Self;          // the documented common case
    type Error = Infallible;

    async fn on_start(args: Self, _ref: ActorRef<Self>) -> Result<Self, Self::Error> {
        Ok(args)
    }
}

pub struct Normalize { pub operation: OperationId, pub path: WirePath }

impl Message<Normalize> for ClaimNormalize {
    type Reply = Result<NormalizedScope, ClaimNormalizeFailure>;

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

let normalizer = ClaimNormalize::spawn(ClaimNormalize {
    in_flight:     HashMap::new(),
    max_in_flight: 64,
    metrics:       ClaimNormalizeMetrics::default(),
});

let scope = normalizer.ask(Normalize { operation, path }).await?;
```

The actor type owns its data. Methods that operate on that data
live on the actor (`fn validate_and_collapse(&mut self, …)`). The
no-public-ZST-actor-noun rule from `skills/actor-systems.md` is
naturally satisfied: the actor type is the data-bearing noun.

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
struct Inc(i64);
struct Mul(i64);
struct Read;

impl Message<Inc>  for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
impl Message<Mul>  for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
impl Message<Read> for Calculator { type Reply = i64; async fn handle(...) -> i64 { ... } }
```

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

The default mailbox capacity is **64** (`pub(crate) const
DEFAULT_MAILBOX_CAPACITY: usize = 64`). Macro doc claims 1000;
that's stale. Size deliberately when traffic patterns warrant it.

---

## Supervision

Declarative — no manual restart wiring.

```rust
use kameo::supervision::{RestartPolicy, SupervisionStrategy};

// Parent supervisor: chooses how to react to child failures.
struct Supervisor;
impl Actor for Supervisor {
    type Args = Self;
    type Error = Infallible;
    async fn on_start(args: Self, _: ActorRef<Self>) -> Result<Self, Self::Error> { Ok(args) }

    // Default is OneForOne. Override for OneForAll or RestForOne.
    fn supervision_strategy() -> SupervisionStrategy {
        SupervisionStrategy::OneForAll
    }
}

let supervisor = Supervisor::spawn(Supervisor);
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

**Restart preserves the mailbox.** Messages queued at the time of
crash survive into the new instance; the message currently being
processed is lost. The new instance runs `on_start` again — counters
on `Self` reset unless they live in `Args` (`Clone`-ed in) or are
shared via `Arc<AtomicU32>` etc.

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
  send it a typed message.
- **Tests live in `tests/`, not `#[cfg(test)] mod tests`.** Per
  `skills/rust-discipline.md` — and the kameo-testing repo
  demonstrates the shape.
- **Don't reach for `remote` until cross-process actors are
  designed.** The local registry semantics differ; the libp2p
  surface is heavy. Document the decision in the consumer's
  `ARCHITECTURE.md` if you enable it.

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
- `/git/github.com/LiGoldragon/kameo-testing` — the falsifiable
  source: every behavior named above is exercised by a passing
  test.
- `/git/github.com/LiGoldragon/kameo-testing/notes/findings.md` —
  documented surprises, gotchas, and source citations.
- `https://github.com/tqwewe/kameo` — upstream source (v0.20.0
  tag is the workspace's pinned baseline).
- `https://docs.rs/kameo/0.20.0/kameo/` — rustdoc reference.
