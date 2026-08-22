# Kameo runtime anatomy witness

Observation date: 2026-08-22. All source reads were read-only. Local fork revision is `3486e4f63ea4e87123476cfbdefeb12403540306`; its common ancestor is `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`; fresh upstream identity is `tqwewe/kameo` `main` at `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`.

## Fork source witnesses

`src/actor/spawn.rs:173-313` (`3486e4f6`) shows the terminal sequence:

1. `on_start` is unwind-caught. A successful actor enters `ActorBehaviour` and the abortable mailbox loop.
2. When the loop returns a stop reason, `actor_ref.stop_message_admission()` runs before `state.shutdown()`.
3. Parent shutdown is marked, child shutdown signals are sent, and the actor waits for child mailbox closure while calling `mailbox_rx.recv()`.
4. `on_stop` runs. On success the code constructs `ActorTerminalOutcome::dropped(reason)`, drops the actor state, awaits `links.notify_links(..., outcome, mailbox_rx)`, unregisters, sets the compatibility shutdown result, then sets the lifecycle `SetOnce`. On cleanup error it invokes the error hook, constructs `cleanup_failed`, performs the same drop/notify/unregister/publication order, and sets an error result.
5. Startup failure has no actor state. It closes admission, sets startup error, shuts down/waits children while draining, constructs `startup_failed` (`NeverAllocated`), notifies links, unregisters, sets the error result, and publishes the outcome.

`src/actor/lifecycle.rs:8-128` (`3486e4f6`) defines `ActorStateAbsence::{Dropped,NeverAllocated,Ejected}`, terminal reasons, and a shared `Arc<SetOnce<ActorTerminalOutcome>>`. Only `Dropped` and `NeverAllocated` are constructed in the runtime; `Ejected` has no construction use in the local source search. `wait_for_shutdown` returns the cell value and `is_terminated` checks publication.

`src/actor/actor_ref.rs:92-119,274-285,678-768,2230-2235` (`3486e4f6`) exposes separate admission and terminal states. `stop_gracefully` sends `Signal::Stop`; the control lane makes this independent of ordinary user-message capacity. `is_accepting_messages` reads the admission flag, while `is_terminated` reads the lifecycle cell. Shutdown result accessors refuse to expose a result until terminal publication.

`src/mailbox.rs:38-150,185-254,673-677,801-903,1024-1120,1270-1364` (`3486e4f6`) shows two physical lanes. Bounded/unbounded ordinary messages carry `QueuedMessage { generation, signal }`; lifecycle and link signals use an unbounded control channel. Ordinary sends read admission and generation before enqueue, and bounded async sends re-check both after acquiring a permit. `stop_message_admission` stores false and increments the generation. Receiver `recv`, `try_recv`, and poll paths inspect control first and discard queued messages whose generation is stale. `blocking_recv` drives the async receive path with a newly built current-thread runtime. `is_closed`, `is_empty`, and `len` combine both channels.

`src/links.rs:40-96,114-229,248-301,320-366` (`3486e4f6`) shows awaited notification dispatch. The parent path either drops `mailbox_rx` when `parent_shutdown` is set or passes it to the parent. Sibling dispatch uses `FuturesUnordered` and awaits all link sends. `Link::notify` carries both `ActorStopReason` and `ActorTerminalOutcome`. The child spec restart decision consumes the outcome and applies policy/intensity checks.

`src/actor/kind.rs:206-390,438-442` (`3486e4f6`) shows `on_link_died` receives outcome plus reason, restart coordination stores the passed mailbox receiver for replacement, and `ActorBehaviour::shutdown` returns the state to the lifecycle caller. In the no-restart path sibling notifications are awaited before the local `on_link_died` hook.

## Fork test witnesses

`tests/lifecycle_phases.rs:466-552` proves strong and weak shutdown waits return equal `Dropped/Stopped` outcomes only after delayed `on_stop`, `Drop`, and resource release. It also proves weak shutdown-result access stays hidden after `on_stop` but before state drop/lifecycle publication.

`tests/lifecycle_phases.rs:554-600` proves admission closes while cleanup is blocked, `is_terminated` remains false during that interval, ordinary send returns `ActorNotRunning`, and terminal publication follows cleanup.

`tests/lifecycle_phases.rs:602-631` proves a linked observer hook receives the same terminal outcome value as the stopped actor. `:633-706` proves link/control dispatch does not wait for a bounded target user mailbox and that the Stop control signal wins over queued ordinary work. `:708-790` proves an async bounded send waiting for capacity is rejected after admission closes and does not later succeed; queued ordinary work is not handled. `:792-813` proves blocking receive wakes for a late Stop control signal. `:815-869` proves queued asks are discarded on stop and their callers receive `ActorStopped`.

`tests/lifecycle_phases.rs:871-901` proves startup failure yields `NeverAllocated/StartupFailed` and cleanup failure yields `Dropped/CleanupFailed` while the compatibility shutdown result is an error. `:903-996` proves both async and thread-spawned supervised replacements start only after the old actor's resource has dropped. The witness is a drop counter/resource rebind; it does not directly inspect the source actor's lifecycle cell at replacement start.

There is no fork test in this checkout proving that ordinary tells survive a supervisor restart. Because restart reopens admission without resetting the shared generation, queued messages from the prior generation are stale to the reused receiver and are discarded by the fork receiver.

## Common ancestor witness

At `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`, `src/actor/spawn.rs:168-298` returns `Result<(A, ActorStopReason), PanicError>`. After the actor loop it calls `state.shutdown`, shuts down/waits children while receiving from the mailbox, asynchronously schedules link notification through the locked `LinksInner`, then runs `on_stop`, unregisters, sets the shutdown result, and returns `(actor, reason)`. There is no admission close, terminal outcome cell, or explicit state drop before notification. `ActorRef::wait_for_shutdown` at `src/actor/actor_ref.rs:647-649` waits for mailbox sender closure and returns unit.

At that revision `src/mailbox.rs` has one channel for ordinary messages and lifecycle/link signals; `src/links.rs:96-142` schedules parent/sibling notifications with `tokio::spawn`. Thus a bounded one-lane mailbox can delay a control send behind ordinary messages, and notification work is not part of the lifecycle task's awaited critical path.

## Current upstream witness

At `main@upstream` (`b4aaee79`), `src/actor/spawn.rs:199-364` retains the `(A, ActorStopReason)` result shape. It computes `will_restart`, drains while children close, preserves tells for a restart, sends leftover terminal tells to `on_undelivered`, catches `on_undelivered` and `on_stop` panics, schedules link notification through the old locked `LinksInner`, unregisters, sets the shutdown result, and returns the actor state. `src/actor/actor_ref.rs:48-53,287-295,663-664` uses one shared `Arc` for handle state, flips an `accepting` flag before enqueuing Stop, and keeps `wait_for_shutdown` as a unit wait on mailbox closure.

`src/mailbox.rs:51-134,170-305,596-662` remains one channel, with an admission flag that rejects later ordinary messages but does not move control signals to a separate lane. Its `MailboxReceiver::front` and `push_front` preserve signals for a restarted incarnation. `src/actor/spawn.rs:383-453` preserves queued tells during child-drain/restart, bounces queued asks with `ActorRestarting` when a restart is expected or `ActorNotRunning` on terminal stop, and calls `on_undelivered` for terminal leftover tells. `src/links.rs:122-158,160-205,287-379` uses a shared restart tracker to predict the supervisor decision; link notification is still spawned and carries reason only.

Current upstream tests in `tests/stop_gracefully_closes_mailbox.rs` explicitly expect already queued messages to run before Stop, later tells/asks to be rejected, and `is_alive` to turn false while draining. `tests/supervision_mailbox.rs` and `tests/on_undelivered.rs` expect tells to survive panic/normal supervised restart, asks to bounce with `ActorRestarting`, and terminal leftovers to reach `on_undelivered`.

## Commands and limits

Source was read using the local Jujutsu repository and `jj file show` at the three revisions above. The local fork working copy was clean. No fetch, checkout, ref update, source/configuration edit, build, test run, or Cargo resolution was performed. The current upstream identity was obtained separately through the previously recorded read-only forge witness; this runtime witness does not assert that local upstream refs remain fresh beyond the recorded head query.
