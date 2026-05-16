# 131 — Kameo control-plane lifecycle work

Date: 2026-05-16
Role: operator
Scope: Kameo fork `kameo-push-only-lifecycle`, commit `44c0552e`

## 0. Summary

This report records the Kameo lifecycle implementation pass after:

- `reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md`
- `reports/designer-assistant/99-review-current-designer-204-kameo-lifecycle.md`

The pass implemented the next narrow correctness slice:

1. ordinary user messages and lifecycle/control signals now use
   physically separate mailbox lanes;
2. ordinary message admission is generation-guarded so bounded sends
   that began before shutdown cannot cross closed admission;
3. lifecycle tests now prove that full user mailbox capacity does not
   block control signals, and that a pending bounded send cannot report
   success after shutdown admission closes;
4. `stop_gracefully` documentation now states the current contract:
   stop after the in-flight handler, not after draining all ordinary
   queued messages.

The work landed on the fork branch as:

```text
44c0552e actor: split lifecycle control mailbox
```

## 1. Why this pass existed

The lifecycle design has converged on an Akka-like public contract:
one terminal outcome, no public phase stream, and release-before-notify
ordering inside the framework. DA/99 named two immediate bugs still
present after the previous operator commit:

- a single bounded queue cannot serve as both user mailbox and lifecycle
  control plane;
- a bounded send can check admission, wait for capacity, then enqueue
  after admission closes unless the send is made generation-safe.

Those are framework bugs, not Persona-specific bugs. They matter because
Persona actors will own exclusive resources: redb files, sockets,
terminal sessions, harness processes, and local-model sessions. A
supervisor waiting on shutdown must be waiting on the actor lifecycle,
not on mailbox closure or a best-effort notification task.

The implemented slice intentionally did **not** touch the unsettled API
surfaces from `/204`: state ejection, brutal termination, or public
intermediate lifecycle facts.

## 2. Shape

The mailbox now has two lanes.

```mermaid
flowchart LR
    "ordinary sender" --> "message lane"
    "message lane" --> "MailboxReceiver"

    "runtime control sender" --> "control lane"
    "control lane" --> "MailboxReceiver"

    "MailboxReceiver" --> "actor loop"
```

The receiver checks the control lane first. Ordinary messages remain
bounded when the user requested a bounded mailbox; control signals use
an unbounded control lane so they cannot be blocked by ordinary user
capacity.

That maps to `/204` invariant 2:

> notification dispatch is awaited on a non-deadlocking control plane.

The implementation still awaits dispatch into the recipient mailbox. It
does not wait for the recipient actor to process the control signal in
its handler, which would create deadlocks.

## 3. Key implementation

The core internal type is now:

```rust
enum MailboxSenderInner<A: Actor> {
    Bounded {
        messages: mpsc::Sender<QueuedMessage<A>>,
        control: mpsc::UnboundedSender<Signal<A>>,
    },
    Unbounded {
        messages: mpsc::UnboundedSender<QueuedMessage<A>>,
        control: mpsc::UnboundedSender<Signal<A>>,
    },
}

struct QueuedMessage<A: Actor> {
    generation: u64,
    signal: Signal<A>,
}
```

This keeps the public `Signal<A>` surface intact but stops ordinary and
control traffic from competing for the same bounded queue capacity.

Ordinary `send` now captures the current generation, waits for bounded
capacity, then checks that the generation is still current before it
uses the permit:

```rust
let generation = self.current_message_generation();
if !self.accepts_message_generation(generation) {
    return Err(mpsc::error::SendError(signal));
}
let permit = match messages.reserve().await {
    Ok(permit) => permit,
    Err(_) => return Err(mpsc::error::SendError(signal)),
};
if !self.accepts_message_generation(generation) {
    return Err(mpsc::error::SendError(signal));
}
permit.send(self.queued_message(generation, signal));
```

Shutdown closes ordinary admission by flipping the admission flag and
incrementing the generation:

```rust
pub(crate) fn stop_message_admission(&self) {
    self.admission_open.store(false, Ordering::Release);
    self.message_generation.fetch_add(1, Ordering::AcqRel);
}
```

The receiver filters stale queued messages:

```rust
fn accept_queued_message(
    message_generation: &AtomicU64,
    queued: QueuedMessage<A>,
) -> Option<Signal<A>> {
    if queued.generation == message_generation.load(Ordering::Acquire) {
        Some(queued.signal)
    } else {
        None
    }
}
```

This gives two lines of defense:

- a sender waiting for capacity re-checks admission before sending;
- any stale message already queued under an old generation is ignored by
  the receiver.

## 4. Test witnesses

The test fixture added a `QueueBlockedActor`:

```rust
struct QueueBlockedActor {
    handler_started_sender: Option<oneshot::Sender<()>>,
    handler_release_receiver: Option<oneshot::Receiver<()>>,
    user_work_count: Arc<AtomicUsize>,
}
```

It has one message that blocks inside a user handler and one ordinary
user-work message that increments a counter if it is ever processed.
That creates a reproducible "actor is busy and user mailbox is full"
condition.

### 4.1 Full user mailbox does not block control signals

Test:

```text
control_signals_do_not_wait_for_bounded_user_mailbox_capacity
```

Scenario:

1. spawn `QueueBlockedActor` with `mailbox::bounded(1)`;
2. block its current user handler;
3. fill the ordinary user message lane until `MailboxFull`;
4. link a second actor to it;
5. stop the linked actor;
6. prove the linked actor reaches `wait_for_shutdown()` within the
   timeout even though the observer's ordinary user mailbox is full.

The test also stops the observer through the control lane and asserts
that queued ordinary user work did not run after stop won:

```rust
assert_eq!(
    user_work_count.load(Ordering::SeqCst),
    0,
    "the stop control signal wins over queued ordinary user work"
);
```

### 4.2 Pending bounded send cannot cross closed admission

Test:

```text
pending_bounded_user_send_cannot_cross_closed_admission
```

Scenario:

1. spawn `QueueBlockedActor` with `mailbox::bounded(1)`;
2. block its current user handler;
3. fill the ordinary user lane until `MailboxFull`;
4. start another ordinary send so it waits behind capacity;
5. send `stop_gracefully` through the control lane;
6. release the blocked handler;
7. prove the pending ordinary send resolves as
   `ActorNotRunning`, not `Ok(())`.

This is the concrete witness for the generation guard. The old shape
could let a bounded send enter after admission closure because the send
had already passed its initial admission check before waiting on
capacity.

## 5. Documentation correction

The old `stop_gracefully` documentation said:

```text
Signals the actor to stop after processing all messages currently in its mailbox.
```

That conflicts with the new lifecycle contract. A stop signal is a
control-plane signal; it should not be blocked behind ordinary user
messages. The docs now say:

```text
Signals the actor to stop after the current in-flight message completes.
```

and explain that ordinary admission closes before cleanup starts.

This is not a cosmetic wording change. The tests now encode the same
contract: queued ordinary user work is not processed merely because it
was already in the mailbox when stop arrived.

## 6. Verification

Commands run with low build parallelism:

```sh
CARGO_BUILD_JOBS=1 cargo check -p kameo --all-targets --all-features
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 cargo test -p kameo --all-features --test lifecycle_phases -- --nocapture
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 cargo test -p kameo --all-features bounded -- --nocapture
CARGO_BUILD_JOBS=1 cargo test -p kameo --all-features -- --test-threads=2
```

Results:

- `cargo check`: passed.
- lifecycle integration test: 8 passed.
- bounded mailbox focused suite: 16 passed across unit and lifecycle
  tests.
- full `kameo` package suite with all features: passed.

One operational note: the full `--all-features` package suite cannot
run with `RUST_TEST_THREADS=1`. An existing remote `ActorId` hash test
uses a barrier and deadlocks with one test thread. It passes with
`--test-threads=2`; build jobs still stayed at `1`.

## 7. What is good

The mailbox/control split is the right direction. It makes the design's
"await dispatch to a non-deadlocking control plane" statement real
instead of semantic hand-waving over a single `Signal<A>` enum.

The generation guard is also the right primitive. It directly names the
admission epoch and gives the receiver enough information to discard
stale ordinary messages. This is better than trying to infer legality
from channel closure alone.

The tests are constraint-shaped: they set up the exact failure mode and
prove the architectural path, not just a final output. A full ordinary
mailbox and a blocked user handler are the conditions that previously
made lifecycle control unsafe.

## 8. What is still lacking

This pass did not implement internal lifecycle facts from `/204` §2.5.
The public API should still stay minimal, but framework tests would be
stronger if the runtime emitted internal facts such as
`AdmissionStopped`, `CleanupHookFinished`, `LinkSignalsDispatched`, and
`TerminalResultVisible` under a test-only surface.

This pass did not redesign `run_to_state_ejection`. DA/99 called out
that the API sketch in `/204` still needs cleanup before implementation.
That work should wait.

This pass did not change `kill()` semantics. `/204` now distinguishes
current Kameo `Killed` behavior from future brutal termination. This
pass keeps current Kameo behavior.

This pass did not add a direct test for the exact visibility boundary of
`get_shutdown_result()`. The current spawn path sets `shutdown_result`
after link notification and registry removal, and immediately before the
terminal lifecycle outcome. That should get its own witness if this API
remains compatibility surface.

This pass did not split the registry into `mark_unfindable` and
`release_slot`. `/204` names that as part of the larger exclusive
resource story. It remains future work.

## 9. Impact on Persona

Persona can now depend on a stronger Kameo fork for the specific
problem that blocked exclusive-resource actors:

```mermaid
flowchart TD
    "StoreKernel" --> "owns redb handle"
    "supervisor" --> "stop child"
    "stop child" --> "control lane stop"
    "control lane stop" --> "ordinary admission closes"
    "ordinary admission closes" --> "cleanup and drop"
    "cleanup and drop" --> "terminal outcome"
    "terminal outcome" --> "replacement may open resource"
```

The guarantee is not yet "all Persona lifecycle work is solved." The
guarantee is narrower and load-bearing: ordinary user traffic cannot
consume the capacity needed for lifecycle dispatch, and pending ordinary
sends cannot truthfully report success after shutdown admission closes.

That is enough to keep moving on Persona's state-owning actors while the
remaining Kameo lifecycle surfaces are clarified.

