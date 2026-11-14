# Send delivery correlation in Flow 0.53.1 (candidate 9435, signal-flow 51 9f15, meta-signal-flow 64 efc0)

Traced from source at the pinned revisions; no tests run.

Short answer: in 0.53.1 a client cannot follow one Send's later states on the public wire. `DeliveryCursor` is a position in an event stream, renumbered on every state change, and no later observation carries anything that links back to the cursor the Send got. That link exists only through the private `logical_delivery_id`, which Deliver no longer returns either.

I read the wire at the pinned revisions with `git show`. The checkouts under `/git/github.com/LiGoldragon/` are not at those revisions (signal-flow is at ce083f2, meta-signal-flow at 281f5aa). Pointers marked **SF** are `signal-flow@9f159d9:ethos/signal.ethos` and **MSF** are `meta-signal-flow@efc0bf5:ethos/signal.ethos`. Nexus paths are under `crates/flow-nexus/src/`.

## 1. What DeliveryCursor is

- **Type:** a plain integer, `DeliveryCursor.Integer` (SF:657).
- **How it is minted:** one durable counter for all deliveries (`store/logical_delivery.rs:76-91`, read at 1386-1399), stored in the Nexus database. It continues across a Nexus restart, and `Configure.Counters` carries it over when a store is replaced (MSF:72-82).
- **At admission:** the Nexus takes the next cursor, and the private id is made from it: `id = format!("logical-delivery-{next:020}")` (`logical_delivery.rs:1108-1111`). The same happens for Codex tool sends (`logical_delivery.rs:726-729`). So the cursor in the Send answer equals the number inside the private id.
- **That match is not a contract.** Other ids are built differently: `simplified-result-…` and `simplified-publication-notice-…` (`logical_delivery.rs:591`, 620), and `legacy:` rows (`queue_delivery.rs:657`, 909). Rows seeded at startup also get cursors unrelated to their ids (`logical_delivery.rs:963-994`).
- **Every state change mints a new cursor:** `snapshot.delivery_cursor = next` in `commit_logical_transition` (`logical_delivery.rs:1284-1289`), and again at 441 for wake receipts. All transitions go through it: Attempting (`queue_delivery.rs:853`), Withdrawn (`queue_delivery.rs:1375`), and the rest via `queue_delivery.rs:60`.
- **Storage:** event rows are keyed by cursor (`logical_delivery.rs:118`). The table of current state is keyed by the private id (`logical_delivery.rs:98-100`).
- **The observation cursor is a highwater mark:** it is the maximum cursor over all senders (`logical_delivery.rs:1345-1350`, 1375-1377).

Verdict: the cursor is unique per event and durable, so it works as a resume point. It is not a stable per-delivery identity. Only the Queued event at admission carries the cursor the sender was given.

## 2. Following a Send's later states

Ordinary socket:

| Input | Who may call it | Output | Key carried |
|---|---|---|---|
| `ObserveSends.Option<DeliveryCursor>` (SF:275) | the calling process, identified as a flow (`lib.rs:954-966`, `observe_sends.rs:32-33`) | first `SendsObserved.VisibleSendObservation { DeliveryCursor Vector<VisibleDeliverySnapshot> }`, then one `SendChanged.VisibleDeliverySnapshot` per change (SF:308-309, 724; `observe_sends.rs:85-95`) | each snapshot is `{ DeliveryCursor VisibleSender Address VisibleDeliveryState }` (SF:723) |
| `ObserveSender.{ Process Option<NativeSessionId> Option<DeliveryCursor> }` (SF:276) | only the bound Message process; it names the sender by process or Codex thread (`observe_sends.rs:35-57`, `lib.rs:968-978`) | same as above | same as above |

- **Filtering:** results are filtered only by sender address (`logical_delivery.rs:1351-1368`).
- **What the snapshot lacks:** no private id, no admission cursor, no request body (projection at `message_projection.rs:156-169`).
- **Getting a NativeReceipt:** `Delivered.NativeReceipt` (SF:666, 712) is the only way to obtain one.
- **What does not help:**
  - `Observe` covers only `Launch` and `Agent` (SF:569-570).
  - `Current` is per metaflow.
  - There is no `Subscribe`.

Meta socket (MSF:32-34: open to the Message executable, the owner, or flows whose aspect is in `MetaAspects`):

- `ReadSendOutcomes` returns `VisibleSendOutcomeRecord { Option<Process> Option<Address> Option<Address> RequestDigest VisibleOrdinarySendOutcome }` (MSF:514). This links a Send to its admission cursor and nothing later.
- `ReadQueueDeliveries.Address` returns `VisibleQueueDelivery { NativeSessionId HarnessKind VisibleQueueEvidence Standing }` (MSF:506). It carries no attempt id and no logical id.
- `Inspect.Address` exposes no keys (MSF:488-493).
- `Debug.Address` returns `DebugSnapshot { Address Vector<FlowId> Vector<LogicalDeliveryId> }` (MSF:494-495, 516; `logical_delivery.rs:353-377`). It is the one interface that exposes the private ids, as a bare list per recipient with no cursor, sender or body.

## 3. Identify, Lock, Deliver in 0.53.1

All three still exist on the ordinary socket, together with Bind, Release and IdentifyThread (SF:266-273). Each of them is refused with `NotMessage` unless the caller is the exact bound Message process (`metaflow.rs:132-165`; direct dispatch refuses at `lib.rs:364-369`). Bind is accepted only when the kernel-reported executable is the configured `MessageNexusBinary` (SF:177-181).

- **Identify.Process** returns `Identified.Address` for a process: one bound by Bind, one in a flow pane Flow launched, or a Codex app-server child (`metaflow.rs:167-170`, 55-83; `sending.rs:111-141`).
- **Lock.{ Sender Recipient }** returns `Locked.Lock` (`store.lock_metaflow`, `metaflow.rs:172`). Flow trusts the Sender that Message asserts, which must be an Awake metaflow (SF:183-191).
- **Deliver.{ Lock Message }** verifies the lock and admits the delivery under that Sender (`store/metaflow.rs:249-286`). For abrupt priority or a live recipient it sends directly (`metaflow.rs:173-231`).
  - What Message receives on the wire is only the projected answer: `SendAccepted.VisibleSendAcceptance`, `Sent.NativeReceipt` or `Failed.VisibleSendFailure` (`lib.rs:1024-1034`, `message_projection.rs:76-91`).
  - The private answer with the id is kept inside the Nexus.

The privileged `meta Deliver.DeliveryRequest` (MSF:3-24, 241, 426) is different: it is Flow's own pane writer for typing into a pane, not message admission.

**Send versus Deliver:** Send carries no sender. Its sender is whichever flow the calling process runs in (SF:4-9; `sending.rs:206-259`). Message's own process would send as its own bound Address (`metaflow.rs:42`). So Send is the supported path for a flow sending as itself, and it cannot relay on behalf of another flow. For an external sender like Message, relaying for a sender is still Identify, then Lock, then Deliver, with `ObserveSender` to follow. In 0.53.1 that path no longer hands back the private id.

## 4. Gaps

1. **No public per-delivery key.** The admission cursor is stable, but every later snapshot has a new cursor and no back-reference. A client can match `SendChanged` to its Send only by guessing from sender and recipient, which is ambiguous when several sends to one recipient are in flight. Message's ledger keyed on `logical_delivery_id` has nothing on the wire to key on.
2. **Direct sends return no cursor at all.** `Sent` carries a `NativeReceipt` only, and `Failed` carries a reason only (SF:715-721). For example, `Failed(NotSent)` leaves the request queued as `Retryable(WakeRefused)` (`sending.rs:1389-1398`), and the sender gets no handle to follow it.
3. **The Uncertain or Attempting answer carries a stale cursor.** It returns the admission cursor while the current row has already moved to a newer one (`sending.rs:1420-1426`).
4. **ObserveSender mixes sources.** It returns everything sent by that sender address, including the flow's own Sends, so Message cannot tell its relays apart (`logical_delivery.rs:1357`, 1365).
5. **Withdraw needs the private id.** `meta Withdraw.{ Address LogicalDeliveryId }` (MSF:221-228, 255) can get one only from `Debug`, which does not link ids to cursors or bodies.
6. **ResolveQueueDelivery needs an attempt id nobody shows.** It takes a `QueueAttemptId` (MSF:468), but `VisibleQueueDelivery` omits it (MSF:506), and no visible reply carries it.
7. **Closing a Task is done by content, not by id.** `Done` and `Result` match the full typed request (SF:623-628; `logical_delivery.rs:852-955`). Two open matches give `Refusal.Ambiguous`, so correlating by content can fail where the private id would not.
