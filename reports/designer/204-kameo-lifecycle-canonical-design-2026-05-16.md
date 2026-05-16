# 204 — Kameo lifecycle: canonical design (Akka contract, translated to Rust async)

Date: 2026-05-16
Role: designer
Scope: designer's POV on the most-correct, working-system-true Kameo
lifecycle contract, after the audit (`reports/designer/202`),
working-system synthesis (`reports/designer/203`), operator's branch
review (`reports/operator/126`), operator's response
(`reports/operator/128`), and designer-assistant's independent pass
(`reports/designer-assistant/96`).

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
    /// Wait for the actor to fully terminate.
    ///
    /// At the moment this resolves, the runtime guarantees:
    /// - if the actor reached `Running`, its `on_stop` hook has
    ///   completed (success or error captured in outcome);
    /// - if the actor was constructed, its `Self` value has been
    ///   dropped — every resource owned uniquely by `Self` is
    ///   released;
    /// - all parent/watcher notifications have been dispatched
    ///   (channel sends completed, not merely spawned);
    /// - the registry entry for this actor has been removed.
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
    /// Actor was killed via `abort()`/`kill()`; `on_stop` did not run.
    Killed,
    /// Handler, `on_stop`, or `on_start` panicked.
    Panicked,
    /// `on_start` returned `Err`.
    StartupFailed,
    /// `on_stop` returned `Err`. The actor `Self` was still dropped.
    CleanupFailed,
}

/// Watchers receive exactly ONE signal per terminated actor.
pub enum Signal {
    LinkDied { id: ActorId, outcome: ActorTerminalOutcome },
}

/// Two run modes. NOT fungible — different contracts:
impl<A: Actor> PreparedActor<A> {
    /// State is dropped at termination; `state: Dropped` (or
    /// `NeverAllocated` on startup failure).
    pub async fn run_to_termination(self, args: A::Args)
        -> Result<ActorTerminalOutcome, PanicError>;

    /// State is returned to the caller; `state: Ejected`. The caller
    /// is responsible for dropping it. The runtime makes no claim
    /// about resource release after this returns.
    pub async fn run_to_state_ejection(self, args: A::Args)
        -> Result<ActorRunOutcome<A>, PanicError>;

    /// `run_to_termination` returns the same enum; ejection variants
    /// are unreachable on this path.
    pub async fn run_to_termination(self, args: A::Args)
        -> Result<ActorRunOutcome<A>, PanicError>;
}

/// Per-DA correction: a tuple return is not type-correct because
/// `on_start` failure leaves no `A`. An enum is needed.
pub enum ActorRunOutcome<A> {
    /// Actor ran successfully and `Self` was dropped at terminal.
    Dropped(ActorTerminalOutcome),
    /// Caller chose `run_to_state_ejection` and the actor reached
    /// terminal; `actor` is the ejected `Self`, caller owns it now.
    Ejected { actor: A, outcome: ActorTerminalOutcome },
    /// `on_start` returned `Err` or panicked; no `A` was ever
    /// constructed. Possible on either run mode.
    NeverAllocated(ActorTerminalOutcome),
}
```

The same `ActorRunOutcome<A>` is returned by both run methods.
`Ejected` is unreachable from `run_to_termination` (that API
always drops); `Dropped` is unreachable from `run_to_state_ejection`
(that API always ejects); `NeverAllocated` is reachable from
either when `on_start` fails. Operator can refine to two separate
enums if the type-level guarantee is wanted.

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

Steps 1+2 (`on_stop` await, `drop(actor)`) complete strictly before
steps 4+5 (parent/watcher notification) begin. This is the
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
mailbox:

- The control plane has its own queue, separate from
  `Message<T>` user messages.
- The control plane is processed even when the recipient's
  user-message processing is blocked (e.g., its current handler
  is awaiting something).
- A control-plane signal cannot deadlock against the recipient's
  user-handler execution.

This is what Akka has as system-messages, what Erlang has as
EXIT/DOWN signal handling outside the normal receive loop. Kameo
0.20 has the *shape* of this with its `Signal` enum (`StartupFinished`
etc.) but the discipline must be made explicit: terminal death
notifications go through the control plane, not the user mailbox.

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
succeed only after step 7 in `finish_terminate`. But this is an
implementation detail of the registry, not a public lifecycle
fact. The two operations have different internal triggers; the
public contract doesn't expose either.

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

## 4. What changes from the current branch

| Branch today | Canonical design |
|---|---|
| `ActorLifecyclePhase` 8-variant enum publicly exposed | **Removed.** Internal sequence only. |
| `wait_for_lifecycle_phase(phase)` public | **Removed.** Replaced with `wait_for_shutdown() -> ActorTerminalOutcome`. |
| `tokio::watch<ActorLifecyclePhase>` published | **Replaced** with internal step sequencing + `oneshot<ActorTerminalOutcome>` for terminal wait. |
| `notify_links` uses `tokio::spawn(...)` fire-and-forget | **Each dispatch `.await`-ed.** This is the largest internal change. |
| `StateReleased` phase publicly observable | **Internal.** The terminal outcome's `state: Dropped` is the public signal. |
| `LinksNotified` phase publicly observable | **Removed.** The terminal event *is* the post-notify boundary. |
| Linear `PartialOrd` over 8 phases | **Removed.** Paths walk different internal sequences; outcome carries path information. |
| `PreparedActor::run()` returns only `ActorStopReason` (current branch) | **Two methods:** `run_to_termination()` (drops state) vs `run_to_state_ejection()` (returns state, sets `state: Ejected`). |
| Startup failure has same enum as graceful stop | **Different internal sequence.** Same `ActorTerminalOutcome` shape with `state: NeverAllocated`. |
| `WeakActorRef::wait_for_shutdown_result()` inconsistent with strong | **Fixed.** Both surfaces resolve at the same `ActorTerminalOutcome`. |
| `is_alive()` exists with inconsistent semantics | **Deprecated.** Replaced with `lifecycle.is_running()` / `lifecycle.is_terminated()` querying the runtime's internal state. |

## 5. Staged landing

The audit's PRs #1 and #2 (`reports/designer/202` §6) remain the
right minimal upstream candidates:

### PR #1 — `kameo-shutdown-short-fix` as-is

One-line: `wait_for_shutdown` waits on `shutdown_result` instead
of mailbox closure. Pure bug fix. Cleanly upstream-eligible.

### PR #2 — `kameo-shutdown-lifecycle-fix` as-is

Drop-before-notify-links reordering, `PreparedActor::run()`
signature change. Upstream conversation; must name the break.

### PR #3 — Canonical design (replaces audit/202's PR #3 entirely)

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
`StoreKernel` Template-2 deferral. On a Kameo fork pinned to
this design, that test passes and the comment at
`persona-mind/src/actors/store/mod.rs:295-307` can be removed.

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
2. **Audit/202's PR #3 plan should be replaced** by §5 of this
   report (PR #3 = Akka contract translation, not 12-fact stream).
3. **The `reports/designer/203` working-system synthesis** should
   be updated (or annotated in chat) to reflect that the
   "observable fact stream" recommendation is superseded by this
   design. The single-owner storage topology recommendation for
   StoreKernel (from designer-assistant/96) is unchanged and
   correct — it solves a different problem at a different layer.
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

- `reports/designer/202-kameo-push-only-lifecycle-audit-2026-05-16.md`
  — the audit that prompted this design
- `reports/designer/203-working-system-reference-for-kameo-lifecycle-2026-05-16.md`
  — three-system synthesis; this report's §3 supersedes /203's
  fact-stream recommendation
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
