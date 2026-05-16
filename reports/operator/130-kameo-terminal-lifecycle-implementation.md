# Kameo Terminal Lifecycle Implementation

Operator report. Created 2026-05-16.

## Summary

The Kameo fork now follows the Akka-shaped public lifecycle contract:

- callers wait for one terminal outcome with `wait_for_shutdown()`;
- the terminal outcome says why actor state is absent;
- link death is delivered as one terminal signal carrying that outcome;
- ordinary message admission closes before cleanup begins;
- lifecycle/control signals are still accepted through the control plane;
- link dispatch is awaited until the target channel accepts the signal, not until the target actor processes it;
- the public ordinal phase API is gone.

```mermaid
flowchart TD
    "stop requested" --> "close ordinary message admission"
    "close ordinary message admission" --> "stop children"
    "stop children" --> "await on_stop"
    "await on_stop" --> "drop actor state"
    "drop actor state" --> "dispatch terminal link signals"
    "dispatch terminal link signals" --> "unregister actor"
    "unregister actor" --> "set terminal outcome"
    "set terminal outcome" --> "wait_for_shutdown returns"
```

## Public Contract

The new public lifecycle data is:

```rust
pub enum ActorStateAbsence {
    Dropped,
    NeverAllocated,
    Ejected,
}

pub enum ActorTerminalReason {
    StartupFailed,
    Stopped,
    SupervisorRestart,
    Killed,
    Panicked,
    LinkDied,
    CleanupFailed,
    #[cfg(feature = "remote")]
    PeerDisconnected,
}

pub struct ActorTerminalOutcome {
    pub state: ActorStateAbsence,
    pub reason: ActorTerminalReason,
}
```

`ActorRef::wait_for_shutdown()` and `WeakActorRef::wait_for_shutdown()` now return
`ActorTerminalOutcome`.

`ActorRef::is_accepting_messages()` and `WeakActorRef::is_accepting_messages()` name the precise
admission fact. `is_alive()` remains as a compatibility alias for message admission. `is_terminated()`
means the terminal outcome has been published.

## Internal Shape

The old public lifecycle phase stream is removed. Internally, `ActorLifecycle` is a single terminal
cell:

```rust
pub(crate) struct ActorLifecycle {
    outcome: Arc<SetOnce<ActorTerminalOutcome>>,
}
```

This avoids the false witness problem: startup failure no longer pretends to pass through cleanup or
state-drop phases. It simply resolves:

```rust
ActorTerminalOutcome {
    state: ActorStateAbsence::NeverAllocated,
    reason: ActorTerminalReason::StartupFailed,
}
```

## Admission Gate

The mailbox now has a logical message-admission gate shared by all sender clones. Closing admission
rejects only ordinary `Signal::Message`. It intentionally still allows lifecycle/control signals such
as stop and link-death.

```rust
fn accepts_signal(&self, signal: &Signal<A>) -> bool {
    self.is_accepting_messages() || !matches!(signal, Signal::Message { .. })
}
```

This implements the DA correction: new user messages are not accepted once shutdown starts, but
control-plane delivery cannot deadlock behind a physically closed receiver.

## Link Signals

`Signal::LinkDied` carries both:

- `ActorTerminalOutcome` for the lifecycle contract;
- legacy `ActorStopReason` for existing diagnostic/error payloads, including panic detail.

`Actor::on_link_died` now receives the outcome:

```rust
fn on_link_died(
    &mut self,
    actor_ref: WeakActorRef<Self>,
    id: ActorId,
    outcome: ActorTerminalOutcome,
    reason: ActorStopReason,
) -> impl Future<Output = Result<ControlFlow<ActorStopReason>, Self::Error>> + Send
```

The default behavior branches on `outcome.reason`. It keeps the legacy reason only to construct the
compatibility `ActorStopReason::LinkDied` when stopping the observing actor.

## Tests Added

`tests/lifecycle_phases.rs` now has six lifecycle-contract tests:

- `wait_for_shutdown_returns_after_cleanup_drop_and_notifications`
- `message_admission_stops_before_cleanup_finishes`
- `link_signal_delivers_terminal_outcome_to_actor_hook`
- `startup_failure_returns_never_allocated_outcome`
- `stop_error_returns_cleanup_failed_outcome`
- `supervisor_restart_waits_for_terminal_outcome_before_replacement_start`

The highest-value witnesses are:

```rust
assert!(
    !actor_reference.is_accepting_messages(),
    "shutdown closes ordinary message admission before cleanup finishes"
);

assert!(
    !actor_reference.is_terminated(),
    "closing message admission is not the same as terminal shutdown"
);
```

and:

```rust
assert_eq!(observed_outcome, linked_actor_outcome);
assert_eq!(observed_outcome.state, ActorStateAbsence::Dropped);
assert_eq!(observed_outcome.reason, ActorTerminalReason::Stopped);
```

## Verification

All commands were run with low build parallelism:

```sh
CARGO_BUILD_JOBS=1 cargo check -p kameo --all-targets --all-features
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 cargo test --all-features --test lifecycle_phases -- --nocapture
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 cargo test -p kameo supervision -- --nocapture
```

Results:

- all-targets/all-features check: passed;
- lifecycle tests: 6 passed;
- supervision filtered tests: 29 passed.

## Known Limits

`run_to_state_ejection` has not been redesigned yet. The right future shape is an enum, not
`JoinHandle<(A, Outcome)>`, because startup failure has no actor state to return.

Remote peer disconnect currently maps to `ActorTerminalOutcome::peer_disconnected()`. That preserves the
existing stop path, but remote-disconnect semantics may need a sharper model because a local node cannot
prove remote actor state was dropped.

The compatibility `shutdown_result` API still returns the older `ActorStopReason`/`PanicError` surface.
It now waits for the terminal outcome before reading that compatibility result.

