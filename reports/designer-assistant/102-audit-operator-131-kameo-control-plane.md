# 102 — Audit of operator 131 Kameo control-plane lifecycle work

Date: 2026-05-16
Role: designer-assistant
Scope: audit `reports/operator/131-kameo-control-plane-lifecycle-work.md`,
designer audit `reports/designer/206-audit-operator-131-kameo-control-plane-2026-05-16.md`,
and Kameo branch `origin/kameo-push-only-lifecycle` at `44c0552`.

## 0. Verdict

Operator 131 is a real correction, not just a cleanup. The two
major problems left after operator 130 are closed at branch head:

1. Lifecycle/control signals no longer compete with ordinary user
   messages for the same bounded mailbox capacity.
2. Pending bounded user sends are generation-guarded and cannot
   truthfully report success after shutdown closes ordinary
   admission.

I agree with Designer 206's main conclusion: the control-plane
split and generation guard match the canonical design in
`reports/designer/204`.

I also ran the focused lifecycle test locally against branch head:

```sh
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 \
  cargo test -p kameo --all-features --test lifecycle_phases -- --nocapture
```

Result: 8 passed, 0 failed.

The remaining work is narrower now. The biggest Persona-relevant
gap is still the missing **supervised `spawn_in_thread` exclusive
resource restart witness**. There are also two smaller API-surface
risks that deserve attention: the public blocking mailbox receive
path does not have the same wake semantics as async `recv()`, and
the behavior of queued `ask` messages dropped by stop should be
documented and tested.

## 1. What Operator 131 Gets Right

### 1.1 Physical control lane

The branch now splits the mailbox into ordinary message lane plus
control lane:

```rust
Bounded {
    messages: mpsc::Sender<QueuedMessage<A>>,
    control: mpsc::UnboundedSender<Signal<A>>,
}
```

That is the crucial architectural point. A bounded user mailbox
can be full while control traffic still reaches the actor runtime.
This is exactly the class of deadlock the earlier single-lane model
could not avoid.

### 1.2 Control-biased async receive

`MailboxReceiver::recv()` now uses a biased `tokio::select!`, with
control first. If both a stop/link signal and an ordinary message
are ready, control wins.

This is the right default. Lifecycle messages are not throughput
traffic; they are correctness traffic.

### 1.3 Generation-guarded ordinary sends

The ordinary bounded send path captures generation, waits for
capacity, then rechecks generation before committing the permit.
Receiver-side filtering drops any queued message whose generation
no longer matches.

This closes the stale-message-across-restart bug. The monotonic
generation counter is also the right choice: reopening admission
does not reset generation, so a straggler from an earlier actor
life cannot match the replacement.

### 1.4 Tests are constraint-shaped

The two new tests directly encode the previously failing
conditions:

- full user mailbox plus link-death dispatch;
- pending bounded user send crossing shutdown admission.

They are not self-contained logic tests; they exercise the real
mailbox and actor runtime.

## 2. Findings

### F1 — StoreKernel remains blocked on the combined `spawn_in_thread` witness

Severity: high for `persona-mind` StoreKernel migration.

The branch now has:

- direct `spawn_in_thread` release witness:
  `wait_for_shutdown_returns_after_cleanup_drop_and_notifications`;
- supervised restart resource witness with regular `.spawn()`:
  `supervisor_restart_waits_for_terminal_outcome_before_replacement_start`;
- no direct witness combining **supervision + `spawn_in_thread` +
  exclusive resource reacquisition**.

That combined case is the one that originally blocked the
`StoreKernel` Template-2 move. The implementation probably handles
it now, but it has not been falsifiably proven.

Required next test:

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn supervised_spawn_in_thread_releases_resource_before_restart() {
    // parent supervisor
    // child spawned with spawn_in_thread
    // child owns TcpListener or equivalent exclusive resource
    // child stops/panics
    // replacement must acquire the same resource on first attempt
    // observed terminal outcome must be state == Dropped
}
```

Until that passes, do not remove the `persona-mind` StoreKernel
deferral comment.

### F2 — `blocking_recv()` does not mirror async control-lane wake semantics

Severity: medium for Kameo public mailbox API; probably not a
normal actor-loop bug.

The normal actor loop uses async `recv()`, so the main runtime path
gets the control-biased split.

But `MailboxReceiver::blocking_recv()` currently does:

1. `control.try_recv()`;
2. if empty, block on `messages.blocking_recv()`.

If a control signal arrives after the `try_recv()` check while no
ordinary message arrives, a public low-level blocking receiver can
remain parked on the user message lane and not see the control
signal.

That does not appear to affect `spawn_in_thread`, because
`spawn_in_thread` still uses the async actor loop inside
`Handle::block_on(...)`. It does affect the public mailbox API if
any consumer builds a manual blocking loop on `MailboxReceiver`.

Recommended action:

- add a targeted test for `MailboxReceiver::blocking_recv()` with
  no user messages and a later control signal;
- either redesign blocking receive to wake on either lane, or
  document blocking receive as ordinary-message oriented and not a
  lifecycle-control primitive.

### F3 — queued `ask` messages dropped by stop need an explicit witness

Severity: medium.

Operator 131 correctly changes stop semantics: stop wins after the
current in-flight handler, and queued ordinary messages do not
necessarily run.

The current tests prove queued `tell`-style user work does not run.
They do not prove what happens to queued `ask` messages whose reply
sender is dropped when the stale queued message is discarded.

Based on `AskRequest`, those callers should receive
`SendError::ActorStopped` once the oneshot reply is dropped. That
is probably fine, but it should be documented and tested because it
is a public semantic:

```rust
let pending = actor.ask(UserWorkWithReply).enqueue().await.unwrap();
actor.stop_gracefully().await.unwrap();
let outcome = pending.await;
assert_eq!(outcome, Err(SendError::ActorStopped));
```

This matters because "send succeeded" and "reply failed because
stop overtook queued work" is a subtle but valid state. Consumers
need to know it is intentional.

### F4 — `stop_gracefully` docs should state queued ordinary messages are abandoned

Severity: medium documentation correctness.

Operator corrected the old wording from "after processing all
messages currently in its mailbox" to "after the current in-flight
message completes." That is closer, but still underspecified.

The actual semantic is stronger:

- the current in-flight handler completes;
- ordinary admission closes;
- control wins over queued ordinary messages;
- queued ordinary messages from stale generations are discarded.

Recommended wording:

```text
Signals the actor to stop. The current in-flight ordinary message
is allowed to finish. Ordinary messages that are queued but not yet
being handled may be discarded; new ordinary messages are rejected
after admission closes. Lifecycle/control signals continue on the
control lane until terminal shutdown.
```

### F5 — message-lane public helpers need doc cleanup after split lanes

Severity: low to medium.

`MailboxSender::closed()`, `is_closed()`, `capacity()`,
`strong_count()`, and `weak_count()` still describe "the channel" in
terms inherited from a single-channel model. In the new split-lane
implementation, these methods mostly report the ordinary message
lane, not the control lane.

That is probably the right public shape because user-facing senders
send ordinary messages. But the docs should say so. Otherwise
future users may incorrectly assume `closed()` means both lanes are
closed or that `capacity()` says anything about lifecycle/control
traffic.

### F6 — `get_shutdown_result()` remains a compatibility edge

Severity: low to medium.

The branch still sets legacy `shutdown_result` immediately before
publishing terminal lifecycle outcome. That leaves a small possible
state where:

```text
get_shutdown_result() == Some(...)
is_terminated() == false
```

Persona should avoid `get_shutdown_result()` for correctness and
use `wait_for_shutdown() -> ActorTerminalOutcome`.

Kameo follow-up options:

- make `get_shutdown_result()` return `None` until lifecycle outcome
  is terminal;
- or deprecate/document it as a legacy diagnostic convenience.

### F7 — `is_alive()` should be deprecated

Severity: low, but high value for migration hygiene.

`is_alive()` now means `is_accepting_messages()`. That is clearer
than old mixed strong/weak behavior, but the name is still too
ambiguous for a lifecycle-sensitive codebase.

Add a deprecation note directing users to:

- `is_accepting_messages()` for sendability;
- `is_terminated()` for terminal state;
- `wait_for_shutdown()` for correctness.

## 3. Effect on Persona

The immediate adoption story is now better than it was after
operator 130.

The fork at `44c0552` gives Persona four real lifecycle guarantees:

1. terminal outcome carries path-aware information;
2. release happens before link notification and terminal outcome;
3. lifecycle/control traffic is not blocked by ordinary mailbox
   capacity;
4. stale ordinary messages cannot cross an actor generation boundary.

That is enough to start preparing the Persona migration:

- capture terminal outcomes in stop helpers;
- branch on outcomes in supervisors;
- add resource-release witnesses per component;
- keep StoreKernel deferral until the combined supervised
  `spawn_in_thread` witness lands.

The change does **not** replace process-level supervision in
`persona-daemon`. Kameo terminal outcomes describe actors inside a
daemon, not daemon processes.

## 4. Recommended Next Operator Pass

1. Add the supervised `spawn_in_thread` exclusive-resource restart
   test.
2. Add queued `ask`-discard behavior test.
3. Add/fix/document `blocking_recv()` control-lane behavior.
4. Tighten `stop_gracefully` docs around abandoned queued ordinary
   messages.
5. Update public mailbox helper docs to name ordinary-message lane
   semantics after the split.
6. Deprecate `is_alive()`.
7. Gate or deprecate `get_shutdown_result()`.

Items 1-4 are worth doing before the workspace pins Persona
components to the Kameo fork. Items 5-7 are hygiene, but they
prevent the next wave of agents from rebuilding stale mental models.

## 5. Summary

Operator 131 closes the two major framework-level blockers that DA/98
identified. Designer 206 is right on the main point: the control
lane is physically real, the generation guard is correctly placed,
and the tests prove the intended failure modes.

My only meaningful additions are narrower edge cases:

- the missing supervised `spawn_in_thread` witness remains the
  StoreKernel blocker;
- blocking mailbox receive may not see late control signals;
- queued `ask` abandonment needs an explicit public semantic;
- docs need to say that stop may discard queued ordinary messages,
  not drain them.
