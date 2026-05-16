# 204 — Kameo lifecycle: canonical design (Akka contract, translated to Rust async)

Date: 2026-05-16
Role: designer
Scope: canonical Kameo lifecycle contract. Responds to
`reports/operator/126`, `reports/operator/128`, and
`reports/designer-assistant/96`. The discipline statement and
prior-art research have been agglomerated into
`ESSENCE.md` §"Release before notify" and
`skills/actor-systems.md` §"Release before notify".

This report is opinionated. It rejects the observable-fact-stream
direction the prior round converged on. The answer is simpler and
older.

## 0. The verdict

**Akka Classic's lifecycle contract is the most correct, reliable
working-system answer for Kameo.** Translated to Rust async with
each dispatch step explicitly awaited, the contract is strictly
stronger than Akka's (Rust's `.await` on channel send is stronger
than JVM monitor happens-before). Path-awareness lives in a typed
outcome enum, not in observable intermediate phases.

The 12-fact observable lifecycle stream proposed in
`reports/operator/128` and `reports/designer-assistant/96` is
over-engineering *for the public API*. **Akka deliberately rejected
public phase signals in the Typed redesign** (akka-meta#21) for the
same reason it should be rejected here: exposing internal sequence
as public contract creates fragile user code and conflates
"implementation mechanism" with "user surface."

**The 12 facts are correct as the *internal* model** (§2.5):
they're how the framework proves its own correctness in tests.
They just don't surface as public API. Operator/128 and DA/96's
substance lands in `pub(crate) enum LifecycleFact` + test
infrastructure, not in the public `ActorRef` surface.

Rust's async constraints do not change this public-vs-internal
boundary. They change the *internal* mechanism (await on dispatch,
not fire-and-forget spawn; admission stops at step 1, not late;
"await dispatch" means accepted into a control-plane channel,
not processed by the recipient's handler). They do not change
the *public* contract (single termination event + outcome
describing how we got there).

**Per DA's refinement after first draft, four corrections landed:**

1. **Admission stops first.** §1.2 sequence opens with
   `mailbox.close_admission()`, not closes mailbox after `drop`.
   New sends get clean errors instead of silently queuing.
2. **"Await" means control-plane delivery, not handler processing.**
   §2 invariant 2 names this explicitly — the death-signal is
   enqueued into a non-deadlocking control channel; the recipient's
   `on_link_died` handler runs separately.
3. **`ActorRunOutcome<A>` enum replaces tuple return.** §1.1 —
   the `(A, ActorTerminalOutcome)` tuple isn't type-correct on
   startup-failure paths where `A` was never constructed.
4. **Internal lifecycle facts retained for tests.** §2.5 —
   `pub(crate) enum LifecycleFact` + test introspection.
   12-fact model is correct internally; just not public.

## 1. The contract

### 1.1 Public API — minimal

```rust
pub trait Actor: Sized + Send + 'static {
    type Args: Send + 'static;
    type Error: Send + 'static;

    async fn on_start(
        args: Self::Args,
        actor_ref: ActorRef<Self>,
    ) -> Result<Self, Self::Error>;

    async fn on_stop(
        &mut self,
        weak_ref: WeakRef<Self>,
        reason: ActorStopReason,
    ) -> Result<(), Self::Error> {
        Ok(())
    }
}

impl<A: Actor> ActorRef<A> {
    /// Wait for the actor to reach a terminal outcome.
    ///
    /// At resolution, the actor has reached a terminal outcome.
    /// Inspect `outcome.state` to know whether `Self` was dropped,
    /// never allocated, or ejected to a caller. Inspect
    /// `outcome.reason` for the path that led there.
    ///
    /// When `outcome.state == Dropped`:
    /// - the actor's `on_stop` hook completed (success or error
    ///   captured in `outcome.reason`);
    /// - the actor's `Self` value has been dropped — every
    ///   resource owned uniquely by `Self` is released;
    /// - all parent/watcher notifications have been dispatched
    ///   (channel sends completed, not merely spawned);
    /// - the registry entry for this actor has been removed.
    ///
    /// When `outcome.state == NeverAllocated`: no actor state ever
    /// existed; `on_stop` did not run; parent/watcher notifications
    /// have been dispatched and registry entry removed.
    ///
    /// When `outcome.state == Ejected`: the actor `Self` was
    /// returned to the caller via `run_to_state_ejection`. The
    /// runtime makes NO claim about resource release — the caller
    /// owns the actor and is responsible for dropping it.
    pub async fn wait_for_shutdown(&self) -> ActorTerminalOutcome;
}

/// The terminal outcome carries path information. Callers wait
/// for `wait_for_shutdown` and then branch on the outcome.
pub struct ActorTerminalOutcome {
    pub state:  ActorStateAbsence,
    pub reason: ActorTerminalReason,
}

pub enum ActorStateAbsence {
    /// Actor was constructed; `Self` was dropped synchronously.
    /// Every resource owned uniquely by `Self` has been released.
    Dropped,
    /// `on_start` returned `Err` or panicked; `Self` was never
    /// constructed. There was no state to drop.
    NeverAllocated,
    /// Caller used `run_to_state_ejection`; the state was returned
    /// to the caller and the caller now owns it.
    Ejected,
}

pub enum ActorTerminalReason {
    /// Graceful stop completed via `on_stop` returning `Ok`.
    Stopped,
    /// Actor was killed via `abort()`/`kill()`. Current Kameo
    /// semantics: in-flight work is aborted but `on_stop` STILL
    /// runs and the actor state is still dropped. The actor is
    /// terminated but cleanup ran.
    Killed,
    /// Handler, `on_stop`, or `on_start` panicked.
    Panicked,
    /// `on_start` returned `Err`.
    StartupFailed,
    /// `on_stop` returned `Err`. The actor `Self` was still dropped.
    CleanupFailed,
    /// Brutal termination — `on_stop` did NOT run, state may not
    /// have been dropped cleanly. Reserved for a future
    /// `Shutdown::Brutal` mode (OTP-shape shutdown timeout escape).
    /// NOT the same as `Killed`. See PR #4 in §5 for the
    /// shutdown-timeout configuration this variant accompanies.
    Brutal,
    /// Supervised restart — the actor was stopped to be restarted
    /// by its supervisor. Cleanup ran; state was dropped. Operator
    /// added this variant in operator/130 to preserve existing
    /// kameo `ActorStopReason::SupervisorRestart` semantics.
    SupervisorRestart,
    /// A linked actor died, propagating death to this actor.
    /// Cleanup ran; state was dropped.
    LinkDied,
}

/// Watchers receive exactly ONE signal per terminated actor.
/// Public payload — the framework may retain additional
/// private fields (mailbox receiver, sibling links) for
/// supervisor-restart material; those are NOT part of the
/// public contract observed by user `on_link_died` handlers.
/// Per `reports/designer-assistant/98` §2.1, omitting the
/// private fields would break supervised restart.
pub enum Signal {
    LinkDied { id: ActorId, outcome: ActorTerminalOutcome },
}

/// Two run modes. NOT fungible — different contracts:
impl<A: Actor> PreparedActor<A> {
    /// State is dropped at termination. Returns either `Dropped`
    /// (success path) or `NeverAllocated` (startup-failure path).
    pub async fn run_to_termination(self, args: A::Args)
        -> Result<ActorTerminationRunOutcome, PanicError>;

    /// State is returned to the caller. Returns either `Ejected`
    /// (success path) or `NeverAllocated` (startup-failure path).
    /// The runtime makes NO claim about resource release after
    /// this returns — the caller now owns the actor.
    pub async fn run_to_state_ejection(self, args: A::Args)
        -> Result<ActorEjectionRunOutcome<A>, PanicError>;
}

/// Returned by `run_to_termination`. Two variants — the API
/// never ejects, so `Ejected` is unrepresentable.
pub enum ActorTerminationRunOutcome {
    Dropped(ActorTerminalOutcome),
    NeverAllocated(ActorTerminalOutcome),
}

/// Returned by `run_to_state_ejection`. Two variants — the API
/// never drops at terminal, so `Dropped` is unrepresentable.
pub enum ActorEjectionRunOutcome<A> {
    Ejected { actor: A, outcome: ActorTerminalOutcome },
    NeverAllocated(ActorTerminalOutcome),
}
```

Per DA/99 §1.1: two separate enums make the unreachable variants
unrepresentable at the type level. A unified `ActorRunOutcome<A>`
with three variants (Dropped, Ejected, NeverAllocated) is also
acceptable if the workspace wants one type, but the duplicate
`run_to_termination` signature from the prior draft must go.

**That is the entire surface.** No `ActorLifecyclePhase` enum.
No `wait_for_lifecycle_phase`. No `wait_for_lifecycle_target`.
No `watch<ActorLifecyclePhase>` publisher. No intermediate-phase
observation primitives.

### 1.2 Internal `finish_terminate` — Akka's chain, awaited, with admission-stops-first

Per DA's correction (mailbox admission must close *before*
cleanup starts; otherwise new sends queue into an actor that
will never process them), the runtime's terminal sequence on
the success path is:

```rust
async fn finish_terminate<A: Actor>(
    mut actor: A,
    ctx: ShutdownContext<A>,
    reason: ActorStopReason,
) -> ActorTerminalOutcome {
    // 1. STOP ADMISSION FIRST.
    //    New sends from outside return SendError::ActorStopping
    //    immediately. The mailbox sender's `is_closed()` flips true.
    //    This is the Rust equivalent of Akka's `Terminate` system
    //    message + later `dispatcher.detach`, but consolidated to
    //    the front so callers get a clean error instead of silent
    //    enqueue-into-the-void.
    ctx.mailbox.close_admission();

    // 2. Finish the currently-running handler (if any).
    //    The handler that was processing when the stop signal
    //    arrived runs to its natural conclusion. New messages
    //    cannot arrive because step 1.
    //    (This is implicit in the runtime task structure; no
    //    explicit call needed.)

    // 3. Stop children. Drain children's mailboxes; wait until
    //    every child has reached its own terminal outcome.
    //    (Akka's "all children PostStop before parent PostStop"
    //    rule from akka-actor/.../FaultHandling.scala.)
    ctx.stop_and_await_children().await;

    // 4. Await user cleanup — release async resources.
    let cleanup_result = AssertUnwindSafe(
        actor.on_stop(ctx.weak.clone(), reason.clone())
    ).catch_unwind().await;

    // 5. Drop actor explicitly — Self-owned resources released here.
    //    For `run_to_state_ejection`, this step is replaced by
    //    "return actor to caller" and outcome.state = Ejected.
    drop(actor);

    // 6. Dispatch parent notification — AWAITED on the parent's
    //    *control channel* (system-message plane), NOT the parent's
    //    user mailbox. The await resolves when the signal has been
    //    accepted by a non-deadlocking control plane, NOT when the
    //    parent's handler has processed it. See §2 invariant 2 for
    //    why this distinction is load-bearing.
    ctx.parent.deliver_child_terminated_to_control_plane(
        ctx.id, outcome.clone(),
    ).await;

    // 7. Dispatch watcher notifications — same semantics as step 6.
    //    Each watcher's control channel is awaited, not its
    //    handler-processing.
    for watcher in ctx.watchers.drain() {
        watcher.deliver_link_died_to_control_plane(
            ctx.id, outcome.clone(),
        ).await;
    }

    // 8. Cancel our outbound watches. The actors we were watching
    //    no longer need to track us as an observer.
    for watched in ctx.watching.drain() {
        watched.unwatch(ctx.id).await;
    }

    // 9. Unregister from the registry. New actors can now claim
    //    this name.
    ctx.registry.remove(ctx.id).await;

    // 10. Resolve wait_for_shutdown. The oneshot send is the
    //     last thing the runtime does; callers awaiting
    //     wait_for_shutdown() see the outcome here.
    ctx.terminal_outcome_sender.send(outcome.clone()).ok();
    outcome
}
```

Strict ordering. Every step awaited. By the time
`wait_for_shutdown().await` resolves on any caller's thread,
every prior step has completed.

**This is Akka's `finishTerminate` chain — adapted for Rust
async + DA's admission-stops-first correction.** The source
comment in `akka-actor/.../FaultHandling.scala`:

> *The following order is crucial for things to work properly.
> Only change this if you're very confident and lucky.*

— applies verbatim. The translation strengthens Akka in three
ways:

1. **Admission stops at step 1**, before cleanup starts.
   Akka's `Terminate` system message stops dequeueing but
   keeps the mailbox attached; Rust's stricter "sender
   refuses new sends" gives callers a clean error.
2. **Each dispatch is `.await`-ed** on a control channel
   (steps 6, 7). Akka's `sendSystemMessage(DWN)` enqueues
   onto the JVM mailbox and relies on JVM monitor happens-before
   for cross-thread visibility; Rust's `.await` on a channel
   send is strictly stronger — the sender is blocked until the
   message is in the channel.
3. **The terminal-outcome oneshot is the last operation**.
   The `wait_for_shutdown` resolution is sequenced strictly
   after registry-remove, link-cancellation, watcher-dispatch,
   parent-dispatch, drop, on_stop, child-drain, and
   admission-stop. No path can resolve the terminal wait
   before completing all prior steps.

### 1.3 The startup-failure path — different sequence, same contract

```rust
async fn finish_terminate_startup_failure<A: Actor>(
    err: A::Error,
    ctx: ShutdownContext<A>,
) -> ActorTerminalOutcome {
    let outcome = ActorTerminalOutcome {
        state:  ActorStateAbsence::NeverAllocated,
        reason: ActorTerminalReason::StartupFailed,
    };

    // 1. Stop admission (mailbox sender refuses new sends).
    ctx.mailbox.close_admission();

    // No on_stop — there was no actor.
    // No drop(actor) — there was nothing to drop.
    // No outbound watches — actor never reached Running.

    // 3. Stop and drain children (if any were spawned during on_start).
    ctx.stop_and_await_children().await;

    // 6. Dispatch parent notification to control plane.
    ctx.parent.deliver_child_terminated_to_control_plane(
        ctx.id, outcome.clone(),
    ).await;

    // 7. Dispatch watcher notifications.
    for watcher in ctx.watchers.drain() {
        watcher.deliver_link_died_to_control_plane(
            ctx.id, outcome.clone(),
        ).await;
    }

    // 9. Unregister from registry.
    ctx.registry.remove(ctx.id).await;

    // 10. Resolve wait_for_shutdown.
    ctx.terminal_outcome_sender.send(outcome.clone()).ok();
    outcome
}
```

Different internal sequence — no steps 4, 5, 8 (no actor existed
to clean up, drop, or unwatch from). **Same public contract:** one
`wait_for_shutdown` resolution with an outcome that names the
path (`state: NeverAllocated, reason: StartupFailed`).

No false witnesses are possible. There is no
`wait_for_state_dropped` predicate that could erroneously return
`true` on this path. The only externally observable event is the
terminal one, and its outcome is honest.

## 2. The three load-bearing invariants

Everything else falls out of these. These are the contract; the
implementation is in service of them.

### Invariant 1 — Release happens-before notify

Steps 4+5 (`on_stop` await, `drop(actor)`) complete strictly before
steps 6+7 (parent/watcher notification) begin. This is the
Erlang/OTP discipline made explicit:

> Exit signals due to links, down signals, and reply signals from
> an exiting process due to alive_requests are not sent until all
> directly visible Erlang resources held by the terminating
> process have been released.
> — `erlang.org/doc/system/ref_man_processes.html`

Erlang enforces this at the BEAM VM. Akka enforces it via
chained `try/finally` on the dispatcher thread. Kameo enforces
it via `await` ordering in the runtime task. **Same invariant,
three different mechanisms.** The Kameo version is the one Rust
can give us.

### Invariant 2 — Notification dispatch is awaited on a non-deadlocking control plane

Steps 6 and 7 use `.await` on each channel send, not
`tokio::spawn(...)`. This is where the current
`kameo-push-only-lifecycle` branch is broken:
`src/links.rs:112-141` uses `tokio::spawn(parent_link.notify(...))`
and returns immediately. The branch marks `LinksNotified` before
any notification future has even been polled — two scheduler
hops away from "linked peers know."

The correct shape is `await` on each dispatch. But — per DA's
correction — **"await" here means "accepted into a non-deadlocking
control channel," NOT "processed by the recipient actor's
handler."** If the dying actor waits for the parent to *process*
the signal in its handler, shutdown can deadlock: parent is
running a handler that called `child.stop().await`; child's
shutdown waits for parent to handle the death signal; parent
can't handle the death signal until its current handler returns;
parent's current handler is waiting on child's shutdown.

The implementation requirement is that Kameo grow (or formalize)
a **system-message control plane** distinct from the user
mailbox. **"Distinct" has a specific operational meaning:**

- The control plane is **physically separate** from the user
  mailbox — either a second channel, or a reserved capacity in
  the existing channel that ordinary user messages provably
  cannot consume.
- The control plane is processed even when the recipient's
  user-message processing is blocked (e.g., its current handler
  is awaiting something).
- A control-plane signal cannot deadlock against the recipient's
  user-handler execution.
- Filling the user mailbox to capacity must not block control
  signals.

**A single `Signal<A>` enum variant tagged "control" sharing one
bounded mpsc queue with `Signal::Message` does NOT satisfy this
requirement.** Per `reports/designer-assistant/98` §1.1, that
shape preserves two failure modes:
1. If the bounded mailbox is full of ordinary user messages,
   `signal_link_died(...).await` blocks behind user capacity.
2. If a parent actor handler is awaiting a child's shutdown,
   the parent cannot process the link signal from the same
   receiver until that handler returns.

This is what Akka has as system-messages (a *separate* queue with
its own dispatcher entry), what Erlang has as EXIT/DOWN signal
handling outside the normal receive loop. Kameo 0.20's `Signal`
enum is multi-variant *but single-channel* — the variants share
queue capacity. The earlier draft of this section said Kameo "has
the *shape* of this" which was misleading; the shape is *not* yet
there.

Acceptable implementations:

- **Two physical channels** — one for `Signal::Message`, one for
  control signals. The actor's runtime loop `select!`s between
  them with the control channel as the preferential branch.
- **Reserved capacity** — one channel where N slots are reserved
  for control signals and user `tell`/`ask` enforces a max of
  `capacity - N`. Simpler but requires careful accounting.
- **Unbounded control queue + bounded user queue** combined via
  `select!` — control signals never block on capacity; user
  messages preserve backpressure.

The terminal `await` resolves when the death-signal has been
enqueued into the recipient's control-plane queue (channel send
completed), which is processed asynchronously and cannot
deadlock. The recipient's `on_link_died` handler runs at the
recipient's own pace, separate from the dying actor's shutdown
sequence.

### Invariant 3 — Path-awareness lives in the outcome, not in observable phases

A startup-failure path walks a different internal sequence. The
public contract still resolves `wait_for_shutdown` with
`ActorTerminalOutcome { state: NeverAllocated, reason:
StartupFailed }`. Callers branch on the *outcome*, not by
waiting for different phases.

This is why **no observable intermediate-phase API is needed**.
The outcome carries everything a caller needs to know about
which path the actor took. Asking "did state get dropped?" is
answered by inspecting `outcome.state == ActorStateAbsence::Dropped`.
The terminal event is sufficient.

## 2.5. Internal lifecycle facts exist — for tests, not for users

Per DA's clarification: the internal step sequence in §1.2 + §1.3
is real, and the framework's correctness depends on it being
provably ordered. **Those facts have a home in the implementation
and in test infrastructure — not in the public API.**

Concretely:

```rust
// pub(crate) — internal only.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum LifecycleFact {
    AdmissionStopped,
    InFlightWorkEnded,
    ChildrenAbsent,
    CleanupHookFinished,
    ActorStateAbsent,
    LinkSignalsDispatched,
    RegistryEntryAbsent,
    TerminalResultVisible,
}

// pub(crate) — available to tests via a feature flag or
// test-only build path.
#[cfg(any(test, feature = "test-introspection"))]
impl<A: Actor> ActorRef<A> {
    /// Test-only: returns the set of internal lifecycle facts
    /// observed so far. Used by the framework's correctness tests
    /// to assert ordering invariants. NOT a public API; production
    /// users go through `wait_for_shutdown()`.
    pub(crate) fn observed_lifecycle_facts(&self) -> &[LifecycleFact];
}
```

Tests can then assert:

```rust
#[tokio::test]
async fn admission_stops_before_on_stop_runs() {
    // ... drive the actor to shutdown ...
    let facts = actor_ref.observed_lifecycle_facts();
    let admission_idx = facts.iter().position(|f| *f == LifecycleFact::AdmissionStopped).unwrap();
    let cleanup_idx = facts.iter().position(|f| *f == LifecycleFact::CleanupHookFinished).unwrap();
    assert!(admission_idx < cleanup_idx, "admission must stop before cleanup hook runs");
}

#[tokio::test]
async fn link_signals_dispatched_before_terminal_visible() {
    // ... drive the actor to shutdown ...
    let facts = actor_ref.observed_lifecycle_facts();
    assert!(
        facts.iter().position(|f| *f == LifecycleFact::LinkSignalsDispatched)
            < facts.iter().position(|f| *f == LifecycleFact::TerminalResultVisible),
    );
}
```

These tests **live in the framework**, prove the framework's
internal correctness, and are invisible to consumers. Operator
implements `finish_terminate` such that each `LifecycleFact`
is emitted at the right boundary; the test infrastructure
verifies the ordering on every run; consumers never see the
enum.

This is how Akka does it (internal `terminating` flag inspected
only by the framework's own tests and by `akka.event.Logging`
debug output) and how Erlang does it (the BEAM has internal
process state machine that's debuggable via `erlang:process_info/1`
but is not part of the public actor contract). The discipline
is: **internal sequence is rich and testable; public contract
is minimal and outcome-shaped.**

The 12-fact proposals from operator/128 and DA/96 §3 are
correct as the *internal* model. They're wrong only when
exposed as public API. With this clarification, those reports'
substance lands in the framework's `pub(crate) enum LifecycleFact`
+ test infrastructure, not in the public `ActorRef` surface.

## 3. Why the observable-fact-stream design is wrong

Operator/128 and designer-assistant/96 converged on a 12-fact
`ActorLifecycleFact` enum published over a `tokio::sync::watch`
channel, with predicate-based waits like
`wait_for_lifecycle_target(ActorLifecycleFact::ActorStateAbsent(_))`.
This direction is wrong. Five reasons:

### 3.1 Akka deliberately rejected it

The Akka Typed lifecycle redesign issue (akka-meta#21) explicitly
removed intermediate-phase signals. The reasoning:

> A `Stopping` signal would re-introduce the kind of "I am dying
> but not dead" state the redesign tried to eliminate.

Akka has been deployed at scale on the JVM since 2010 with this
shape. The Typed redesign tightened the contract by *removing*
observability, not adding it. The framework that has run actors
in production longest deliberately chose the minimal-surface
shape.

### 3.2 The motivating use case dissolves under the outcome model

The argument for the fact stream was: "a supervisor wants to
wait for state-dropped specifically, before restart binding the
same resource."

Under the outcome contract this becomes:

```rust
let outcome = child_ref.wait_for_shutdown().await;
match outcome.state {
    ActorStateAbsence::Dropped => {
        // resource was held by Self; Self is now dropped; safe to restart
        spawn_replacement().await;
    }
    ActorStateAbsence::NeverAllocated => {
        // no resource was held; safe to restart
        spawn_replacement().await;
    }
    ActorStateAbsence::Ejected => {
        // caller-controlled state; supervisor shouldn't be restarting in this mode
        unreachable!("supervised actors use run_to_termination, not run_to_state_ejection");
    }
}
```

`wait_for_shutdown` is sufficient. The outcome distinguishes the
paths. No separate predicate-style wait is needed.

### 3.3 The 12-fact stream is implementation, not contract

The 12 facts (`Prepared`, `Starting`, `Running`, `AdmissionStopped`,
`InFlightWorkEnded`, `ChildrenAbsent`, `CleanupHookFinished`,
`ActorStateAbsent(_)`, `RegistryEntryAbsent`,
`LinkSignalsDispatched`, `TerminalResultVisible`, `Terminated(_)`)
describe the *runtime's internal sequence*. They are useful as
internal invariants the framework's tests assert on. They are
not useful as a public API.

Exposing them as public contract creates user code that depends
on the sequence's specifics, which:

1. **Breaks if the runtime ever optimizes the sequence.** The
   internal order is a runtime concern; coupling users to it
   ossifies the implementation.
2. **Multiplies the test matrix.** Every user-visible phase is
   a wait target; every wait target needs cross-actor-state-
   path testing. The contract surface explodes.
3. **Invites the "I'm dying but not dead" bug.** A user
   waiting on `CleanupHookFinished` and acting on it is reading
   in-flight state. Akka's argument from akka-meta#21 applies
   directly.

### 3.4 The `LookupAdmissionClosed` / `RegistryEntryAbsent` split is solving a problem the outcome model already solves

The "split publication from reservation" argument (operator's
chat) was a real concern for a model where registry-absent is a
public wait target. Under the outcome contract, callers don't
wait for registry-absent — they wait for terminal, which fires
*after* registry removal. A peer holding a stale reference and
sending a message gets a clean error (mailbox closed); a fresh
caller trying to register the same name waits for that name to
be free.

The split is real *internally* — the registry's `lookup` should
return `None` early (at admission-stops) while `register` should
succeed only after step 9 in `finish_terminate`. But this is an
implementation detail of the registry, not a public lifecycle
fact. The two operations have different internal triggers; the
public contract doesn't expose either.

**The three race conditions the split closes (design rationale):**

| Race | What goes wrong | When closed |
|---|---|---|
| **R1 stale discovery** | Peer calls `lookup(name)`, gets a ref to the dying actor, sends a message. Best case clean error; worst case silent drop. | `lookup` returns `None` *early*, at admission-stops (step 1 of `finish_terminate`). |
| **R2 resource collision** | Peer sees `lookup` return `None`, calls `register(name, new_actor)`. New actor's `on_start` tries to acquire the same exclusive resource. Races old actor's still-held resource. | `register` blocks/fails *late*, until registry-entry removal (step 9 of `finish_terminate`). |
| **R3 double publication** | Two refs registered under the same name. Lookups non-deterministic. | Slot mutex preserved by the tombstone between steps 1 and 9. |

A registry that serves both events from one removal point closes
only one of R1 or R2:
- Service Fabric removes early (closes R1, *leaves R2 open* —
  fine for SF because state is replicated, broken for us
  because we have local exclusive resources).
- A naive "remove at terminal" closes R2 but *leaves R1 open* —
  peers can find the dying actor for the duration of `on_stop`.

The split closes all three. **The implementation lives in the
framework's registry as two distinct operations**:
`mark_unfindable(name)` at step 1, `release_slot(name)` at
step 9. Public API never sees this — it sees only the terminal
outcome.

### 3.5 The watch-as-history concern doesn't argue for an event stream

Designer-assistant/96 §4 correctly notes that `tokio::watch`
retains only the latest value and is not an audit log. Their
conclusion is that Persona must mirror lifecycle events into
durable state if it wants audit. That conclusion is correct
regardless of whether the framework publishes a fact stream —
the framework's job is to give the user a primitive that
satisfies the current-truth question, and Persona's job is to
keep its own durable history. The fact stream is not needed for
either side.

If Persona wants audit, an external observer pattern (a
PersonaLifecycleObserver actor that subscribes to terminal
outcomes from a SupervisorRegistry) is the right shape —
explicit, application-owned, decoupled from framework
internals.

## 4. What changes from the pre-operator/130 branch

Per DA/99 §1.5: this table was historically ambiguous after
operator/130 landed. Split now into (a) what operator/130
already fixed and (b) what remains for the next pass.

### 4.1 Already landed in operator/130 (kameo commit `1329a646`)

| Pre-operator/130 branch shape | Now in operator/130 |
|---|---|
| `ActorLifecyclePhase` 8-variant enum publicly exposed | **Removed.** Internal sequence only. |
| `wait_for_lifecycle_phase(phase)` public | **Removed.** Replaced with `wait_for_shutdown() -> ActorTerminalOutcome`. |
| `tokio::watch<ActorLifecyclePhase>` published | **Replaced** with `Arc<SetOnce<ActorTerminalOutcome>>` for terminal wait. |
| `notify_links` uses `tokio::spawn(...)` fire-and-forget | **Each dispatch `.await`-ed** via `LinkNotification::dispatch().await`. |
| `StateReleased` phase publicly observable | **Internal.** The terminal outcome's `state: Dropped` is the public signal. |
| `LinksNotified` phase publicly observable | **Removed.** The terminal event *is* the post-notify boundary. |
| Linear `PartialOrd` over 8 phases | **Removed.** Paths walk different internal sequences; outcome carries path information. |
| Startup failure has same enum as graceful stop | **Different internal sequence.** `outcome.state: NeverAllocated`. |
| `WeakActorRef::wait_for_shutdown_result()` inconsistent with strong | **Fixed.** Both surfaces resolve at the same `ActorTerminalOutcome`. |
| Admission stops late | **Stops first** via `stop_message_admission()` at the head of the shutdown sequence. |
| `is_alive()` exists with inconsistent semantics | **Compat alias** for `is_accepting_messages()`. `is_terminated()` added. |

### 4.2 Remaining for the next operator pass

Per DA/98 review of operator/130. These are correctness gaps
the current implementation does not yet satisfy:

| Gap | Severity | Spec response (this report) |
|---|---|---|
| Lifecycle/control signals share user mailbox; deadlock + capacity-block | **HIGH** | §2 invariant 2 — physical channel separation, reserved capacity, or unbounded control + bounded user. A shared `Signal<A>` mpsc with admission gate does NOT satisfy. |
| Admission gate not atomic with send-capacity acquisition; stale messages cross restart | **HIGH** | §6.5.2 — generation tokens / fresh mailbox per generation / acquire-and-recheck. |
| `PreparedActor::run()` returns `ActorStopReason`; `run_to_state_ejection` not yet enum-shaped | MEDIUM | §1.1 — two separate enums, `ActorTerminationRunOutcome` + `ActorEjectionRunOutcome<A>`. |
| `get_shutdown_result()` race window before terminal outcome | MEDIUM | §6.5.4 — set terminal outcome before compat result, or gate compat behind `is_terminated()`. |
| `is_alive()` compat-alias semantics risky for old callers | MEDIUM | §6.5.4 — deprecate with `#[deprecated]` and rustdoc warning. |
| Graceful-stop queue semantics not test-locked | MEDIUM | §6.5.4 — explicit test matrix per DA/98 §1.5. |
| Remote `PeerDisconnected` reports `state: Dropped` but can't actually prove it | LOW (operator-flagged) | Future: `state: NeverAllocated` or new variant. |

## 5. Staged landing

PRs #1 and #2 below are the minimal upstream candidates:

### PR #1 — `kameo-shutdown-short-fix` as-is

One-line: `wait_for_shutdown` waits on `shutdown_result` instead
of mailbox closure. Pure bug fix. Cleanly upstream-eligible.

### PR #2 — `kameo-shutdown-lifecycle-fix` as-is

Drop-before-notify-links reordering, `PreparedActor::run()`
signature change. Upstream conversation; must name the break.

### PR #3 — Canonical design

This is the substantive design contribution. It is **not** the
audit's "path-aware fact stream"; it is the Akka contract
adapted to Rust async:

- `ActorTerminalOutcome` + `ActorStateAbsence` + `ActorTerminalReason`
  enums as the public surface.
- `wait_for_shutdown() -> ActorTerminalOutcome` replacing
  `wait_for_lifecycle_phase`.
- `Signal::LinkDied { id, outcome }` carrying the outcome to
  watchers.
- `finish_terminate` rewritten as the seven-step await-chain
  (success path) plus the four-step sequence (startup-failure
  path).
- `notify_links` rewritten to await dispatch, not
  `tokio::spawn(...)`.
- `run_to_termination()` and `run_to_state_ejection()` as two
  explicit `PreparedActor` surfaces.
- Tests for both internal sequences: slow `on_stop`, slow
  `Drop`, startup failure, weak/strong wait equivalence,
  registry ordering, link dispatch.

This is a substantial upstream conversation. The fork carries it
indefinitely if upstream resists.

### PR #4 — Fork-only extensions

- OTP-shape shutdown timeout: `Shutdown::{Graceful(Duration),
  Infinity, Brutal}`.
- Public-docs invariant in the `Actor` trait rustdoc (Akka regret —
  document the release-before-notify guarantee explicitly).
- `is_alive` deprecation in favor of phase-derived predicates.

## 6. The contract test bar

A Kameo fork ships when these falsifiable tests pass on the new
contract:

```rust
#[tokio::test]
async fn wait_for_shutdown_resolves_after_on_stop_completes() {
    // slow on_stop (200ms sleep) — wait_for_shutdown must not resolve before
}

#[tokio::test]
async fn wait_for_shutdown_resolves_after_drop_completes() {
    // Drop impl with 200ms delay — wait_for_shutdown must not resolve before
}

#[tokio::test]
async fn link_died_signal_arrives_after_drop_completes() {
    // watcher receives Signal::LinkDied only after dying actor's Drop ran
}

#[tokio::test]
async fn startup_failure_terminal_outcome_is_never_allocated() {
    // on_start returns Err — outcome.state == NeverAllocated, reason == StartupFailed
}

#[tokio::test]
async fn run_to_state_ejection_outcome_is_ejected() {
    // actor returned to caller — outcome.state == Ejected, no claim of resource release
}

#[tokio::test]
async fn weak_and_strong_wait_for_shutdown_resolve_identically() {
    // both ref types observe the same ActorTerminalOutcome at the same boundary
}

#[tokio::test]
async fn registry_lookup_returns_none_at_admission_stop() {
    // peer cannot discover the dying actor by name even before terminal
}

#[tokio::test]
async fn registry_register_blocks_until_terminal() {
    // new actor with same name can register only after old reaches terminal
}

#[tokio::test]
async fn supervised_restart_does_not_race_resource() {
    // ResourceActor owning TcpListener; supervised restart; rebind succeeds
    // (this is the live regression test from the current branch)
}

#[tokio::test]
async fn supervised_spawn_in_thread_resource_released_before_restart() {
    // Template-2 (dedicated OS thread) on a supervised actor:
    // supervisor's restart blocks until the OS thread has run Drop
    // (this is the failing case at persona-mind/src/actors/store/mod.rs:295-307)
}
```

The last test is the workspace's live blocker — the
`StoreKernel` Template-2 deferral.

Per DA/99 §1.6: this Kameo lifecycle design removes the
*lifecycle* blocker for a supervised dedicated-thread
`StoreKernel`. It does NOT by itself finish the StoreKernel
destination. The comment at
`persona-mind/src/actors/store/mod.rs:295-307` can be removed
only after BOTH:

1. The Kameo lifecycle fix lands and is verified by the
   supervised-`spawn_in_thread` test above.
2. The single-owner storage plane and `CloseAndConfirm`
   discipline from `reports/designer-assistant/96-kameo-lifecycle-independent-pov-2026-05-16.md`
   §2 land and are verified by the practical close-confirm
   test in DA/96 §5.2 (start owner → write rows → close-confirm
   → wait → fresh process reopens → reads succeed).

The Kameo fix and the StoreKernel topology fix are
complementary, not substitutes. Each closes a different layer
of the failure.

## 6.5. Implementation review — operator/130 + DA/98

Operator landed the design at kameo commit `1329a646`
(`actor: publish terminal lifecycle outcomes`); see
`reports/operator/130-kameo-terminal-lifecycle-implementation.md`.
DA reviewed the implementation in
`reports/designer-assistant/98-review-operator-130-kameo-lifecycle-implementation.md`,
which is the canonical review.

Three high-level findings from DA/98 that this report's spec
should sharpen:

### 6.5.1 (HIGH) The "control plane" requirement is real, not implemented yet

§2 invariant 2 above is now sharpened. Operator's implementation
uses one mailbox with an admission gate — it satisfies "admission
stops first" (DA correction #1) but **not** "non-deadlocking
control plane" (DA correction #2). The two failure modes
(deadlock when parent handler awaits child shutdown; block when
user mailbox is full) remain.

The fix is structural: separate the physical channel for control
signals from the user mailbox, per the acceptable
implementations enumerated in §2 invariant 2 above. This is the
load-bearing follow-up to operator/130.

### 6.5.2 (HIGH) Admission gate must be atomic with send-capacity acquisition

The current implementation checks admission *before* `tx.send().await`
parks on bounded capacity. A bounded-full mailbox can have a
pending send that passes the admission check, parks, and then
completes after admission closes — enqueuing an ordinary message
after shutdown started. On supervised restart, the replacement
actor's reused mailbox sees that stale message.

Required spec: a `Signal::Message` send that crosses the
admission-close boundary must fail with `SendError::ActorStopping`,
not enqueue. Two acceptable mechanisms (per DA/98 §1.2):

- **Generation tokens** — each message carries a generation
  identifier; the receiver drops messages from prior generations.
- **Fresh mailbox per generation** — supervised restart creates
  a new mailbox; the old one is dropped (with any pending sends).
- **Acquire-and-recheck** — `send().await` acquires capacity,
  then re-checks admission before committing; aborts without
  enqueuing if admission closed.

### 6.5.3 (MEDIUM) `Signal::LinkDied` carries private restart material

DA/98 §2.1 caught a /204 specification gap: the public payload
`{ id, outcome }` is correct but insufficient. The framework
must retain `mailbox_rx` and `dead_actor_siblings` privately on
the supervised path so the supervisor can install the
replacement actor with the original mailbox. /204 §1.1 has
been amended to note this.

### 6.5.4 (MEDIUM) Public compatibility surface needs alignment

DA/98 §1.3, §1.4, §1.5 surface three smaller issues:
- `get_shutdown_result()` can return `Some` while
  `is_terminated()` returns `false` (a small race window).
- `is_alive()` compatibility alias now means "accepting ordinary
  messages" — risky for old callers that treated `!is_alive()`
  as "safe to restart."
- Graceful-stop queue semantics (queued-before-stop, pending
  sends crossing close, messages-during-restart) need an
  explicit test matrix.

These are cleanup, not correctness blockers. DA/98 §3 names them.

### 6.5.5 (POSITIVE) Restart material preservation

DA/98 §2.1 also flagged a /204 design oversight that operator
*correctly worked around*: the public `Signal::LinkDied { id,
outcome }` sketch in §1.1 was too narrow for the supervised
restart path. Operator kept private fields alongside the public
payload — the right move. /204 §1.1 has been amended above to
make this discipline explicit.

### 6.5.6 Follow-up review of /204 itself (DA/99)

After this report's §6.5 amendments, DA reviewed /204 in
`reports/designer-assistant/99-review-current-designer-204-kameo-lifecycle.md`
and surfaced six remaining flaws *in this design document*:

| DA/99 finding | /204 response (now landed) |
|---|---|
| §1.1 Duplicate `run_to_termination` signatures | §1.1 — single sig per method; two separate enums (`ActorTerminationRunOutcome`, `ActorEjectionRunOutcome<A>`) make unreachable variants unrepresentable |
| §1.2 `wait_for_shutdown` rustdoc overclaims under ejection | §1.1 — rustdoc rewritten with per-state branches; explicitly NO claim of resource release on `Ejected` |
| §1.3 `Killed` definition contradicts Kameo's current `kill()` semantics | §1.1 — `Killed` now reflects "in-flight aborted, `on_stop` still runs"; new `Brutal` variant reserved for no-cleanup mode |
| §1.4 Invariant 1 has stale step numbers | §2 invariant 1 — corrected `1+2 → 4+5, 4+5 → 6+7` to match §1.2 numbering |
| §1.5 §4 "Branch today" table historically ambiguous | §4 split into §4.1 (already landed in operator/130) + §4.2 (remaining for next pass) |
| §1.6 StoreKernel closure claim too strong | §6 last-test wording — closure requires BOTH Kameo lifecycle fix AND DA/96 §2 single-owner storage plane |

DA/99 is the canonical review of /204; this section records
the responses but does not duplicate the findings.

## 7. Open questions / where I might be wrong

### 7.1 Is `Signal::LinkDied` enough, or do supervisors need finer-grained signals?

The Akka contract gives watchers `Terminated(ref)`. Akka *also*
gives supervisors `ChildFailed(ref, cause)` as a distinct signal,
distinguishing "child stopped gracefully" from "child failed with
an exception." The proposal above folds both into
`Signal::LinkDied { id, outcome }` — the outcome's `reason` field
distinguishes them (`Stopped` vs `Panicked` vs `CleanupFailed`
vs `StartupFailed`).

This is probably fine. Worth flagging because Akka split them
deliberately — supervisors often need to dispatch on "graceful"
vs "failed" without unpacking a reason enum. The outcome-as-data
shape supports this with a one-line predicate
(`outcome.reason.is_failure()`); whether that's enough ergonomics
or whether two separate signals are warranted is a judgment call
for operator during implementation.

### 7.2 Does `Signal::LinkDied` need a guaranteed-once delivery?

Akka gives `Terminated` as exactly-once per watcher per
termination. The Rust translation needs the same — the channel
send for each watcher is awaited, and the runtime tracks which
watchers have been delivered to (so a watcher added during
shutdown doesn't get a duplicate).

Implementation detail; not a contract concern.

### 7.3 Should `wait_for_shutdown` be cancellable?

If a caller drops the future returned by `wait_for_shutdown()`,
the underlying `oneshot` receiver is dropped. The actor's
terminal sender writes to the oneshot regardless (or detects the
drop and skips); either is fine. The contract is "if you await
to completion, you get the outcome; if you drop, you don't" —
standard `oneshot` semantics. No special handling needed.

### 7.4 Cross-thread visibility of the terminal outcome

The runtime task that runs `finish_terminate` is owned by Tokio.
The `oneshot::Sender<ActorTerminalOutcome>` send happens after
all prior steps; the receiver on a caller's task observes the
outcome with Tokio's normal channel happens-before. This gives
us Akka's JVM-monitor guarantee for free.

The one subtlety: Rust's memory model doesn't have JVM's
volatile-write semantics for arbitrary fields. The
`ActorTerminalOutcome` is `Send + Copy` (or close to it — small
enum + small enum), so this isn't a concern in practice. But
the framework should explicitly avoid any "actor field that the
watcher reads after Terminated" pattern — the outcome is the
contract; nothing else.

## 8. Recommendation

1. **Adopt this design as the canonical Kameo lifecycle
   contract** for the workspace fork.
2. PR #3 is Akka contract translation, not the 12-fact stream
   that an earlier round of this design proposed.
3. The single-owner storage topology for StoreKernel (from
   `reports/designer-assistant/96`) is unchanged and correct —
   it solves a different problem at a different layer.
4. **Operator's `reports/operator/128`** proposed an
   `ActorLifecycleFact` enum; this design supersedes that
   proposal. The `ActorTerminalOutcome` + enum substructure in
   §1.1 captures the same information operator wanted to expose,
   in a contract shape Akka has validated for 15 years.
5. **Designer-assistant/96**'s 12-fact model is also superseded;
   their core corrections (TxnWorker pool wrong for sema-engine;
   single-owner is correct for StoreKernel; SF inference vs
   citation) all stand.
6. **The "publication-vs-reservation" registry split** (operator's
   chat) is correct as an internal implementation detail but does
   not need to surface as public lifecycle facts.

## 9. Sources

### Primary working-system reference

- Akka Classic `FaultHandling.scala::finishTerminate` — the
  source of the seven-step ordering with the "Order is crucial"
  comment:
  `https://github.com/akka/akka/blob/main/akka-actor/src/main/scala/akka/actor/dungeon/FaultHandling.scala`
- Akka Typed lifecycle redesign decision to remove intermediate
  signals: `akka/akka-meta#21`
  `https://github.com/akka/akka-meta/issues/21`
- Erlang Reference Manual on processes — the release-before-notify
  VM guarantee:
  `https://www.erlang.org/doc/system/ref_man_processes.html`

### Workspace context

- `ESSENCE.md` §"Release before notify" — workspace-level intent
- `skills/actor-systems.md` §"Release before notify" — full
  discipline (shutdown sequence, control plane, await semantics,
  terminal outcomes, decomposition)
- `skills/kameo.md` §"Lifecycle contract" — Kameo-specific API
- `reports/operator/126-kameo-push-only-lifecycle-branch-review.md`
- `reports/operator/128-response-to-da-96-kameo-lifecycle-audit.md`
  — operator's `ActorLifecycleFact` proposal that this design
  supersedes
- `reports/designer-assistant/96-kameo-lifecycle-independent-pov-2026-05-16.md`
  — DA's 12-fact model (this design supersedes the public-fact
  framing; DA's storage-topology correction for StoreKernel is
  independent and stands)
- `persona-mind/src/actors/store/mod.rs:295-307` — the live
  Template-2 deferral closed by this design
