# Send semantics in Flow 0.53.1 (candidate 9435, wire signal-flow 51.0.0 9f15)

Traced from source, no tests run. Paths relative to `/git/worktrees/flow-0531-precompose-e8b6/crates/flow-nexus/src/`; ethos is signal-flow `ethos/signal.ethos` at 9f15.

## What replaced the Queue restriction

- The priority picks the internal mode: HardAbrupt and MiddleAbrupt store `Delivery::Wake`, Soft stores `Delivery::Queue` (sending.rs:199, 260-264). Nothing rejects Queue; removed in commit bce92fb.
- `QueueNotPermitted` is never produced; only its projection remains (message_projection.rs:64).
- A Send goes direct if abrupt or the recipient is Awake and live (sending.rs:285), after taking the address's waking lease (sending.rs:1195-1274). It is queued instead, answered `SendAccepted(Queued)`, when the lease is taken (1206) or the address is held by an outstanding delivery, an address hold, a restart record or a past-threshold refresh (1253-1271).

| Priority | Awake | Asleep |
|---|---|---|
| Soft | typed directly, no interrupt (delivery.rs:507); Working gets it typed; Blocked or foreign composer text refused at the pane (delivery.rs:177-187) | queued, not woken (waking.rs:1399-1405); delivered when something else wakes it |
| MiddleAbrupt | typed directly, no interrupt, even Working | wakes it (sending.rs:1303), then drains; declared-but-no-record gets an Asleep record first (store/metaflow.rs:18-40) |
| HardAbrupt | as MiddleAbrupt, plus interrupt when Working (delivery.rs:507-511); refused if composer holds text not Flow's (493-496) | as MiddleAbrupt |

Answers: `Sent` on the agent's receipt (sending.rs:1353, 1414); `SendAccepted(Queued)` waiting for the turn (1323-1336); `SendAccepted(Uncertain/Attempting)` after the 10 s wait (1420); else `Failed.NotSent`. A refused Soft Send answers `SendRefused(..)`; a refused abrupt Send answers `Failed{ None, Refused(..) }` (sending.rs:347-354).

## Refusals a Send produces

- TopicRefused: topic not camelCase, checked first (sending.rs:221-226).
- Unidentified: no calling process, or the caller is neither a pane seat nor a Codex app-server thread (sending.rs:113-136, 228-233; metaflow.rs:56-83).
- Store: clock, sender identification, resolve or accept failure (sending.rs:118, 129, 137, 240, 252, 274, 343); abrupt lease failure and direct-finish failure as `Failed.Refused.Store` (1216, 1225, 1248, 1429).
- Unresolved: Result not naming an Order, or no open order; Done not naming a Task, or no open task (store/logical_delivery.rs:854, 904, 913, 945).
- Ambiguous: more than one open order or task matches (store/logical_delivery.rs:901, 946).
- Oversized: rendered prompt over 64 KiB (sending.rs:87-93, 277).
- MinutesRefused: Task minutes zero, negative or unreachable (store/logical_delivery.rs:1075-1084).
- Unknown.Address: recipient has no metaflow record at accept (store/logical_delivery.rs:1043-1045), Soft or an abrupt Send that could not take the lease.
- Failed reasons: Refused(..) for abrupt; RecipientUnavailable for abrupt to an undeclared or model-less address (sending.rs:1230, 1240); NotSent when the wake failed before typing (1397) or the direct path failed (1428).

## Produced only by other inputs

- Unknown.FlowId: Report (reporting.rs:77-85, store.rs:2921), refresh (waking.rs:1609).
- Unknown.Lock, Lapsed: Deliver and Release.
- Locked: Adopt, BindSeat. Held, Asleep: Lock. Taken: Bind, Adopt, BindSeat.
- NotConfigured: Bind, Lock, IdentifyThread, Launch. NotSendServer: IdentifyThread.
- NotMessage: metaflow-only queries on the ordinary socket, ObserveSends/ObserveSender, Bind.
- Direct: never a Send answer; a delivery state `Failed(Direct(..))` (store/queue_delivery.rs:1036), seen through ObserveSends/SendChanged; the Send itself answers `Failed.NotSent`.

## Never produced

Awake, Unknown.Key, ReceiptUncertain, QueueNotPermitted. NoLayer and NoneAbove no longer exist in 51.0.0 (removed in 0.52.0, commit 1fe20d1, with Up).
