# Kameo fork runtime anatomy

Status at 2026-08-22: this is a read-only reconstruction of the LiGoldragon fork at `3486e4f63ea4e87123476cfbdefeb12403540306`, compared with its common ancestor `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92` and current local upstream `main@upstream` at `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`. No source, refs, configuration, checkout, or live state was changed, and tests were not run.

## Observations

### Before the fork: one queue, reason-only teardown

At the common ancestor, `run_actor_lifecycle` returns `Result<(A, ActorStopReason), PanicError>` (`src/actor/spawn.rs:168-298`). A successful lifecycle takes the state out of `ActorBehaviour`, marks and shuts down children, waits for child mailbox closure while receiving and discarding mailbox signals, schedules link notification through `tokio::spawn`, runs `on_stop`, unregisters, sets the compatibility shutdown result, and returns the actor state and reason. Startup failure has no actor state and follows a similar reason-only path.

The ancestor mailbox is one bounded or unbounded channel carrying ordinary messages, startup/lifecycle signals, and link-death signals (`src/mailbox.rs`). `stop_gracefully` enqueues `Signal::Stop` into that same channel; there is no admission flag or generation. Its `ActorRef::wait_for_shutdown()` returns unit after the mailbox sender observes receiver closure (`src/actor/actor_ref.rs:647-649`). Link notification is spawned from `LinksInner::notify_links` (`src/links.rs:96-142`), so a caller waiting on the actor task does not await link-send completion.

### Fork: two lifecycle phases and explicit terminal outcome

The fork separates “ordinary messages are no longer admitted” from “the actor has reached terminal shutdown.” When the actor loop ends, `src/actor/spawn.rs:207-220` closes ordinary admission and increments the message generation before `state.shutdown()`. Cleanup then marks parent shutdown, sends child shutdown signals, and waits for child mailboxes while receiving from the actor mailbox (`:222-233`).

For an allocated actor, `on_stop` runs before the state is dropped. On success (`:234-251`) the fork constructs `ActorTerminalOutcome::dropped(reason)`, drops the actor state, awaits `Links::notify_links`, unregisters, sets the compatibility shutdown result, and finally publishes the lifecycle `SetOnce`. Cleanup failure follows the same order with `cleanup_failed` (`:252-268`). A startup failure has no actor state and publishes `startup_failed`, whose fields are `NeverAllocated/StartupFailed` (`:273-312`).

`ActorLifecycle` is an `Arc<SetOnce<ActorTerminalOutcome>>` (`src/actor/lifecycle.rs:60-128`). `ActorRef::wait_for_shutdown()` returns this value and `is_terminated()` reports whether it is published (`src/actor/actor_ref.rs:678-691`). `get_shutdown_result`, `with_shutdown_result`, and their weak variants refuse to expose the compatibility result until `is_terminated` is true (`:411-535` and weak equivalents). `is_accepting_messages()` is deliberately separate from terminal state (`:92-119`).

### Fork mailbox anatomy: control wins, old generations do not

Each fork mailbox has an ordinary-message channel and an unbounded control channel (`src/mailbox.rs:38-150`). Ordinary messages are wrapped as `QueuedMessage { generation, signal }`; startup, Stop, supervisor-restart, and LinkDied signals use control. Ordinary sends check the admission flag and generation before enqueue. Bounded async sends reserve capacity and check both again before using the permit (`:216-255`), preventing a send that was waiting on capacity from crossing a concurrent shutdown. `stop_message_admission` stores false and increments the generation (`:673-677`).

The receiver's `recv`, `try_recv`, and poll paths prefer control and discard stale queued messages (`:843-902`, `:941-975`, `:1090-1128`). Thus Stop and LinkDied do not wait behind a full ordinary queue, and ordinary messages enqueued in the previous generation are not delivered after shutdown or restart. `close`, `is_closed`, `is_empty`, and `len` account for both lanes (`:1024-1087`). Blocking receive is implemented by driving the async receive path with a new current-thread runtime (`:977-992`).

The fork's `stop_gracefully()` sends Stop but does not itself flip the admission flag; the lifecycle task flips it when the loop exits. A racing ordinary send that reaches the current generation before the loop processes Stop can enter the ordinary queue, but the subsequent generation increment makes it stale and the receiver discards it. A send waiting for bounded capacity is rechecked and fails instead of succeeding after the transition.

### Fork links and supervision

`Links::notify_links` takes the link notification out of the links mutex and awaits its dispatch (`src/links.rs:80-97`). Parent notification either drops the child receiver immediately under `parent_shutdown` or passes the receiver to the parent for restart (`:114-163`). Sibling sends run concurrently in `FuturesUnordered` but the dispatch future awaits all of them (`:184-229`). Local and remote links carry both `ActorStopReason` and `ActorTerminalOutcome` (`:248-301`). The notification await means “send accepted or failed,” not “the target hook has finished.”

The actor hook and restart decision receive the outcome in addition to the legacy reason (`src/actor/kind.rs:206-213,239-367`; `src/actor.rs:294-311`). A cleanup failure can therefore have legacy reason `Normal` but terminal reason `CleanupFailed`, and restart policy sees the terminal failure classification. A parent decides through `ErasedChildSpec::should_restart(&ActorTerminalOutcome)` (`src/links.rs:320-366`). For a restart it passes the old mailbox receiver to the factory; the factory clears stale child bookkeeping, resets `parent_shutdown`, and calls `open_message_admission` (`src/supervision.rs:677-710`). Opening admission does not reset the shared generation, so old ordinary queue entries remain stale.

### Current upstream behavior where these mechanisms overlap

Current upstream still returns `(A, ActorStopReason)` and retains the one-channel mailbox. It adds an `accepting` flag and flips it before enqueuing Stop (`src/actor/spawn.rs:199-364`; `src/actor/actor_ref.rs:287-295`), so later ordinary sends fail, but already queued messages remain ahead of Stop and can run. Its receiver has a `front` queue and `push_front` to preserve queued signals for a restart (`src/mailbox.rs:596-662`).

Upstream's teardown predicts whether restart will happen, drains while children close, preserves tells for a restart, bounces asks with `ActorRestarting` during restart or `ActorNotRunning` on terminal stop, and sends terminal leftover tells to `on_undelivered` (`src/actor/spawn.rs:383-453`). It catches `on_undelivered` and `on_stop` panics and still returns the actor state. Its link path remains reason-only and schedules notification with `tokio::spawn` (`src/links.rs:160-205`). `wait_for_shutdown()` remains a unit wait on mailbox closure (`src/actor/actor_ref.rs:652-664`).

These upstream changes touch the exact mechanisms but do not reproduce the fork contract: upstream's `accepting` flag overlaps admission only; `front`/drain preserve queued tells rather than generation-discarding them; `on_undelivered` provides a terminal tell hook absent from the fork; shared restart tracking predicts the supervisor decision rather than passing a terminal outcome; and spawned link notification is not part of the fork's awaited terminal sequence.

## Claims

- The fork enforces a two-stage shutdown invariant: ordinary sends stop being admitted before cleanup completes, while terminal observation waits for cleanup, state destruction, link dispatch, unregister, and compatibility result publication.
- The fork enforces a control-progress invariant under mailbox saturation: lifecycle and link signals use an unbounded, control-priority lane and cannot be blocked by ordinary bounded user work.
- The fork enforces a generation boundary: an ordinary message belongs to the incarnation that admitted it, and queued old-generation messages cannot execute in a later lifecycle incarnation. Queued asks still resolve through their reply-sender drop behavior; the fork test observes `ActorStopped`.
- The fork enforces a state-absence-before-notification invariant: allocated state is dropped before link dispatch begins. A supervisor can receive the terminal outcome after that drop and may start a replacement before the source lifecycle cell is published, because publication occurs after awaited dispatch. The tests prove resource drop before replacement start, not publication-cell ordering.
- The fork makes terminal classification part of supervision/link API. A caller or linked actor can distinguish `Dropped/Stopped`, `Dropped/CleanupFailed`, and `NeverAllocated/StartupFailed`; the legacy stop reason remains available for compatibility/detail.
- The fork's `wait_for_shutdown` is a stronger observable than the ancestor/upstream mailbox-closure wait: after it returns, the lifecycle outcome is present and the tests witness `on_stop`, `Drop`, and resource release. Before it returns, `is_accepting_messages` may already be false while `is_terminated` remains false.

## Runtime diagrams

### Normal stop, common ancestor versus fork

```text
COMMON ANCESTOR (one signal lane)

run loop
  -> receive [Message | Stop | LinkDied]
  -> state.shutdown() -> actor value remains owned by lifecycle result
  -> mark/send children; wait child mailbox closure while receiving
  -> tokio::spawn(link notification)
  -> on_stop(actor)
  -> unregister + shutdown_result
  -> task returns (actor, reason)
  -> wait_for_shutdown() observes mailbox receiver closure; returns ()

FORK (ordinary lane + control lane + terminal cell)

run loop
  -> receive control Stop (control has priority)
  -> stop_message_admission(false); generation += 1
  -> state.shutdown() -> actor value
  -> mark/send children; wait child mailbox closure while stale messages are discarded
  -> on_stop(actor)
  -> outcome = Dropped(reason) or CleanupFailed
  -> drop(actor)
  -> await link dispatch(outcome)
  -> unregister + shutdown_result
  -> lifecycle.SetOnce(outcome)
  -> wait_for_shutdown() returns outcome
```

Startup failure skips the allocated-state and `on_stop` boxes in the fork diagram: `on_start` error -> admission close -> child handling -> `StartupFailed/NeverAllocated` -> awaited link dispatch -> result/unregister -> lifecycle publication.

### Saturated mailbox and queued work

```text
FORK SEND                                      FORK RECEIVE

Message -> admission/gen check                 control.recv (biased first)
        -> bounded messages<Queued(gen,msg)>   or messages.recv
        -> recheck after reserve                -> if gen == current: deliver
                                               -> else: drop stale and loop
Stop/LinkDied -> unbounded control             if both lanes closed/empty: None

Consequence: Stop and LinkDied progress even while messages is full;
ordinary tells admitted before shutdown become stale; queued asks resolve
as stopped when their reply sender is dropped.
```

### Supervised restart

```text
FORK

old loop exits
  -> admission false; generation increments
  -> state dropped
  -> parent receives LinkDied(reason, outcome, mailbox_rx)
  -> should_restart(outcome)
       no restart: sibling notifications + local on_link_died
       restart: factory reuses mailbox_rx, opens admission, starts replacement
  -> reused receiver sees old ordinary messages with old generation -> discards
  -> source lifecycle cell is published after link dispatch, independently of
     when the parent schedules replacement

CURRENT UPSTREAM

old loop exits
  -> will_restart(reason), drain child window
       restart: preserve tells in receiver.front; bounce asks ActorRestarting
       terminal: drain tells to on_undelivered; bounce asks ActorNotRunning
  -> spawned reason-only link notification
  -> on_stop (panic caught), result, return actor state
```

## Edge cases evidenced by tests

The fork's `tests/lifecycle_phases.rs` covers:

- delayed cleanup and delayed `Drop` before strong/weak `wait_for_shutdown` returns (`:466-501`);
- result-helper gating while `on_stop` has finished but actor state is still dropping (`:503-552`);
- admission closure during blocked cleanup and ordinary send rejection before terminal publication (`:554-600`);
- equal terminal outcome delivered to a linked hook (`:602-631`);
- link/control progress despite bounded user-mailbox saturation and Stop winning over queued work (`:633-706`);
- pending bounded send failing after the generation/admission transition (`:708-790`);
- blocking receive waking for a late control signal (`:792-813`);
- queued ask resolving as `ActorStopped` and not being handled (`:815-869`);
- startup failure as `NeverAllocated/StartupFailed` and cleanup error as `Dropped/CleanupFailed` (`:871-901`);
- resource release before replacement start for both async and thread-spawned supervision (`:903-996`).

Current upstream's directly overlapping tests are `tests/stop_gracefully_closes_mailbox.rs`, `tests/supervision_mailbox.rs`, and `tests/on_undelivered.rs`. They cover queued-before-Stop processing, rejecting sends after the accepting flag flips, restart preservation of tells, ask bounce classification, child-drain deadlock avoidance, and terminal `on_undelivered` delivery.

## Invariants, observations, and costs by mechanism

| Mechanism | Fork invariant and caller/supervisor observation | Cost or API consequence |
|---|---|---|
| Shutdown/admission | `is_accepting_messages=false` can precede cleanup; ordinary sends fail or become stale; `is_terminated=true` only after final publication. | Atomic load/store and generation increment on lifecycle transition; send paths add atomic checks and bounded-send recheck. |
| Restart/queued messages | A reused receiver does not process an old-generation ordinary message. Supervisor gets outcome and old receiver through LinkDied. | Queued tells are dropped rather than preserved; no fork `on_undelivered` tell hook. Receiver may scan and discard many stale entries, O(number of stale entries) total. |
| State destruction | `Dropped` means actor state existed and was dropped before link dispatch; `NeverAllocated` means startup never yielded state. | `PreparedActor::run/spawn/spawn_in_thread` no longer return `A`; callers lose the old state-ejection path. Public `Ejected` is currently not constructed. |
| Link notification | Target receives outcome plus legacy reason; source waits for send dispatch, not target hook execution. | Parent dispatch can extend shutdown latency; sibling sends are concurrent but all awaited. Remote send latency is on the teardown path. The old spawn-and-return race is reduced but not eliminated for target processing. |
| Saturation/control | Stop and LinkDied bypass ordinary bounded capacity and are control-priority. | Second channel, unbounded control memory, `QueuedMessage` wrapper, biased-select implementation, and possible ordinary-message starvation during a sustained control flood. |
| Terminal observation | `wait_for_shutdown` is a value-bearing barrier; compatibility result is hidden until the outcome cell is set. | New lifecycle cell and API; existing callers must accept a return value and use new terminal enums. |
| Link/supervision API | `on_link_died` and link wire paths carry `ActorTerminalOutcome`; restart classification can see cleanup/startup failure. | Trait implementations, local link adapters, remote serialization, and supervision code require the new parameter and outcome semantics. |
| Handle layout | Fork `ActorRef` clones its individual fields; current upstream consolidates most shared state behind one `Arc`. | Fork may perform more Arc clones per handle clone than current upstream; current upstream's optimization is post-fork and not evidence that semantics are equivalent. |
| Failure handling | Fork catches `on_start`, handler, and link-hook panics, but `on_stop` is awaited without an outer catch in `src/actor/spawn.rs:234-236`. | An `on_stop` panic is not covered by fork tests and, from the shown control flow, can prevent shutdown-result/lifecycle publication. Current upstream catches `on_stop`; this is a material edge-risk observation, not a tested failure. |

For ordinary send/receive, each successful operation remains expected O(1), with one additional atomic/generation check and (for bounded async send) a second check after reserve. Stale-message cleanup is O(k) over the stale entries removed. Link dispatch is O(number of targets) sends with sibling futures concurrent; the fork waits for completion, while ancestor/upstream spawn the work. The unbounded control lane removes backpressure for control but shifts risk to memory growth under a control-signal flood.

## Hypotheses

- The fork commits and tests indicate an intentional lifecycle contract centered on state absence, terminal outcomes, and control progress; this is inferred from code and test names, not a current design ruling.
- The generation boundary appears intentionally to favor terminal/restart isolation over preserving queued ordinary work. No fork test settles whether that loss is the desired restart policy.
- Awaited link dispatch appears intended to make notification send part of shutdown’s causal boundary; it does not establish that the notified actor has processed its hook.

## Unknowns and evidence limits

- Tests and builds were not run. All test statements are source assertions, not fresh execution results.
- No fork test covers tells or asks queued across a successful supervisor restart. Code reading predicts stale-generation discard; this remains a behavior to verify if restart preservation is a requirement.
- No fork test covers `on_stop` panic, remote-link timing, sustained control-lane load, cancellation during bounded reserve, or concurrent Stop/message admission races.
- The replacement-start tests witness prior state `Drop`, but do not directly establish whether the source actor's lifecycle cell was published before the replacement began.
- `ActorStateAbsence::Ejected` is public but has no construction use in the local source search; its intended caller-visible meaning is unknown.
- Current upstream source was read at the local `main@upstream` object named above; freshness and forge identity are recorded in the relationship witnesses, but no additional fetch was performed for this anatomy pass.

## Sources

- Runtime witness: `flows/fb50d4a5/witnesses/runtimeAnatomy.md`
- Test witness: `flows/fb50d4a5/witnesses/lifecycleTests.md`
- Fork source: `/git/github.com/LiGoldragon/kameo/src/actor/spawn.rs`, `src/actor/lifecycle.rs`, `src/actor/actor_ref.rs`, `src/mailbox.rs`, `src/links.rs`, `src/actor/kind.rs`, `src/actor.rs`, `tests/lifecycle_phases.rs`
- Common ancestor source: `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92` for the same `src/` paths via `jj file show`
- Current upstream source/tests: `main@upstream` at `b4aaee797cc3fd12e8194db406d9d73a6bc021ce` for the same paths plus `tests/stop_gracefully_closes_mailbox.rs`, `tests/supervision_mailbox.rs`, `tests/on_undelivered.rs`, and `tests/actor_ref_counts.rs`
- Relationship witness: `flows/fb50d4a5/reports/kameoForkUpstream.md`
