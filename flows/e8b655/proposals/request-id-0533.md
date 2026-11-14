# Flow 0.53.3: the request id

A bounded design, eighth revision. No source is changed. Ground truth: the Flow
0.53.1 candidate at `/git/worktrees/flow-0531-precompose-e8b6` (`fc27dd`; paths
below are under `crates/flow-nexus/src/` unless named otherwise); the wire is
written against signal-flow 52.0.0 `2f9e2b` and meta-signal-flow 65.0.0 `baaa5b`;
it is rebased onto the accepted 0.53.2 contract (prepared as signal-flow 53 and
meta-signal-flow 66, not yet accepted) before implementation (Versioning).
The changed Ethos was applied to scratch copies of those two files, of
`crates/flow-ethos/ethos/library.ethos` and of
`crates/flow-nexus/ethos/send_tool.ethos`, and each copy passes
`ethos-zero Check` (ethos-zero 17.0.0).

**Rulings, earlier** (Psyche core Fable), binding where the new ones leave them:

1. A RequestId is always four lowercase base36 characters. A collision is
   redrawn up to a bound, then the admission is refused typed. The upgrade uses
   the same rule.
2. The living's messages (Psyche, Psyches) carry an id and are never answered by
   Result.
3. Result answers an Order or a Question. Done closes a Task.
4. A reminder carries the task's id and its words.
5. After the upgrade each recipient of an open task is told its open task ids by
   a Notice, once.
6. Sent carries the RequestId alone.

**Rulings, new** (Psyche core Fable, via Mind core Astra), superseding permanent
ids:

- **R1.** An id is unique among requests the Nexus still holds. Once a request is
  archived its id is free again. Admission is refused `RequestIdSpaceFull` when
  the space is full of held requests; bounded draws that all collide are
  `RequestIdDrawsCollided`, which claims nothing about fullness. No store
  replacement as a remedy, no automatic reset.
- **R2.** Archive is the explicit cutoff. A Result or Done naming an id with no
  current binding is refused Unresolved. After reuse the id denotes its current
  request. The stale-answer risk after reuse is accepted (below). No quarantine,
  no timeout, no second public handle.
- **R3.** Receipts are exposed only through the debugging query. An authenticated
  recipient answer settles Uncertain as Read, the answer as evidence, kept apart
  from delivery evidence (receipts). Withdraw by id and the send tool's Task and
  Done are deferred.

**Rulings, latest** (Psyche core Fable):

- **R4.** The key Message sends with each Deliver stands: a handle between two
  Nexuses, inside the wire, seen by no flow and carried in no reply. Condition: it
  never appears in a Sent, a delivered request, or any debugging answer meant for a
  flow (Paths, The DeliverKey).
- **R5.** Archive is by the owner only, and the owner is the flow that sent the
  request: an unanswered Order or an open Task holds its id until its sender
  archives it, through its own address. Flow runs no archive pass (Archive).
  Settled by Fable, eighth revision: archive is by the sending flow alone, through
  its own address, and the Nexus archives nothing of itself. So a request sent by
  Flow or by Unknown, and a request held at the upgrade, holds its id for the
  store's life unless its sender archives it, and the Nexus owner has no archive
  override.

**Ruling, seventh revision** (Fable, via Mind core Astra):

- **R6.** Two identical held Orders and one historical answer: the answer is
  assigned to the earlier Order by delivery order; the later stays open with its
  new id. The upgrade reports every record decided this way with both ids, so the
  owner can correct a mistaken assignment. Deterministic; no silent closure; no
  refusal of the whole upgrade for this case (Upgrade, step 6; Assignment report).
- **R6, extended by Fable (eighth revision).** Several answers take one Order each,
  in admission order, delivery order deciding which Order; a moved Order counts
  where it was delivered; only groups of two or more Orders are reported. No input
  moves a closure: the sender corrects by archiving a wrongly open Order or
  resending a wrongly closed one. The owner in R6 is the sending flow (R5).
  An Order with no `Delivered` event (Uncertain) orders after every delivered Order
  of its group, among such by admission cursor, and is reported like the rest.

**Accepted risk (R2), not prevented.** Say flow S answered request I from R, and
I was archived. If I is later drawn for a new request from R to S that is
answerable and open, a delayed duplicate Result or Done from S naming I is
admitted against the new request. The same holds for an id S remembers in its
context. Flow cannot tell these apart by the id, and nothing here claims to. Only the
request's sender can free its id (R5), so only a sender that archives while its
recipient may still answer exposes it.

**Reviewer constraints** (Mind core Astra, Mind nixCriomos Sol): (a) an answer is
admitted only after its sender and recipient are authenticated against the
request it names; (b) the answer's own id stays distinct from the id it answers;
(c) withdrawn by R1: Counters carries no ids; (d) the upgrade is idempotent;
(e) Withdraw stays by LogicalDeliveryId, as R3 defers it; (f) Living versus
Psyche renaming stays out.

**Review blockers** (Mind nixCriomos Sol): (g) withdrawn by R1, as no issued-id
set remains; (h) an answer given before ids is not given again: the upgrade
archives every delivered request, so none can be named by id (Upgrade); (i) Read
and Delivered are terminal, and the attempt is settled by the answer (Answers);
(j) task announcements are durable per Notice and retried, bounded (Task
announcement).

**Review findings, sixth revision** (Mind nixCriomos Sol): (k) a Pending
announcement row had no pass to retry it after the archive it waits for: answered
in Task announcement, *When*, and its tests; (l) the Archive section let Flow
archive its own requests against R5: answered in Archive (Flow's own requests,
Capacity), the Archive tests and R5 as settled; (m) the upgrade left references
to moved deliveries with no reader path, and could reopen requests answered before
ids: answered in Upgrade steps 4, 5, 6 and 10, Answers (the simplified reply) and
the Upgrade tests.

**Review blocker, seventh revision** (Mind nixCriomos Sol): (n) Message's durable
state kept no held-unclassified snapshot and no rule keeping the cursor below one:
a Deliver admitted with its answer lost, a snapshot of I at c held while it is
pending, cursor c persisted, a crash, and the reconnect resumes after c, recovers
the acceptance by its key and never sees c to classify. Answered in Consumers
(Message: the cursor never passes an unclassified event, events are acted on in
cursor order, effect and cursor are one write) and the Message boundary tests.

**Ruling recorded, seventh revision** (Fable, via Mind core Astra): (o) R6, two
identical held Orders and one historical answer. Answered in Upgrade step 6 (the
delivery-order key), the Assignment report, Memory
(`flow-nexus-upgrade-assignment`), Archive condition 2, the Upgrade tests, and
Left for judgment 5, now ruled.

## What changes

The Nexus mints a request id for every request it admits and returns it in the
answer to the Send or Deliver. Every later snapshot of that request carries the
same id, until the request is archived; its last snapshot is `Archived`. A
recipient sees the id as the first field of the request delivered to it. A
Result or Done names the request by its id alone. This replaces matching by the
whole request's content (`store/logical_delivery.rs:852-955`).

The id names a held request. It gives no right to do anything: observation is
filtered by sender as before (`logical_delivery.rs:1351-1368`), and an answer is
checked against the authenticated parties, not the id (Answers). `RequestId` is
its own type, separate from `DeliveryCursor`, which still changes on every state
change and still serves as the resume point. It is drawn at random, not computed
from the private `logical_delivery_id`. Inside the store, rows refer to one
another by `LogicalDeliveryId`, which is never reused; a `RequestId` is resolved
only through a held binding.

The id is plain in every answer, snapshot and queue entry. Only a refusal before
admission carries none, and it has its own shape (`Unadmitted`).

## Minting

- **Alphabet and length:** lowercase base36, `0-9a-z`, as bead ids; always four
  characters. The space is 36^4 = 1,679,616 ids. An id never lengthens.
- **Source:** the operating system's random source (`getrandom`, already in
  `Cargo.lock`, added as a direct dependency). Tests inject a scripted source
  through a `DrawsRequestId` trait.
- **Scope:** one Nexus store. The table `flow-nexus-request-id` holds one binding
  per held request; an id is free when no binding holds it. A per-recipient scope
  would not do: ObserveSends and ObserveSender span recipients.
- **Draw, in order, in the admission's own commit under the logical-delivery write
  gate (the minting gate):**
  1. If the table holds 1,679,616 bindings, refuse `Refusal.RequestIdSpaceFull`
     without drawing: every id names a held request.
  2. Draw an id. If no binding holds it, take it.
  3. Otherwise redraw. After `RequestIdDraws` draws that all collided, refuse
     `Refusal.RequestIdDrawsCollided`: the draws found no free id, which says
     nothing of whether the space is full.
  4. A refusal writes nothing: no delivery, no binding. It is
     `SendFailure.Unadmitted` (send tool: the same two variants).
- **Ordering against archive (R1):** an archive commit and a minting commit both
  hold the minting gate, and no commit does both. An id an archive frees can be
  drawn from the next commit on. The cursor only rises under that gate, so the
  `Archived` snapshot of an id's old request always comes at a lower cursor than
  the admission that draws the id again. Ids are freed only by archive: no reset,
  and store replacement is no remedy for a full space.
- **The bound:** `RequestIdDraws`, a configuration, default 64, at least 1
  (`Configure.RequestIdDraws`; below 1 is `ConfigureRejected.RequestIdDrawsRefused`;
  a new Memory seeds the default as it seeds DefaultMinutes).
- **Every admission site mints:** `accept_logical_delivery_for` (Send, Deliver,
  reminders, heartbeat), `accept_tool_send`, both entries in
  `deliver_simplified_reply`. `seed_missing_queued_deliveries` copies the entry's
  existing id.
- **Oversized:** the rendered-prompt budget (`sending.rs:87-93`) measures the
  delivered form with a four-character placeholder id, because the check runs
  before minting.

## Archive

A request is held from its admission to its archive. Archive is one commit, and
nothing else ends a binding.

**Who archives (R5).** The flow that sent the request, and only it, through its
own address. `ArchiveRequest.RequestId` is an ordinary-socket input from the
sending flow's own seat, identified by its process as Send is (Answers, step 1);
for a request relayed by Message, the sender is the Lock's Sender. Flow starts no
archive of its own: no archive pass, no timeout, and the meta socket has no
archive input. An unanswered Order or Question, an open Task, and every request
that has ended, holds its id until its sender archives it. Delivered, Failed and
Withdrawn requests wait too (open question).

- **Flow's own requests.** A request sent by `Flow` (a reminder, an announcement
  or failure Notice, the heartbeat) or by `Unknown` (queued before senders were
  kept) has no flow to archive it. Flow archives none of them (R5): each holds its
  id for the store's life. An `ArchiveRequest` naming one is `UnknownRequest` to
  every flow, as no flow is its sender. No one archives them (R5, settled).
- **Capacity.** Ids are freed only by senders' archives, so the held count grows
  by one with every request of Flow's own or Unknown, and with every request whose
  sender does not archive it. When the table holds 1,679,616 bindings, every
  admission is refused `RequestIdSpaceFull`, Flow's own included (reminders,
  announcements, the heartbeat), until a sender archives (R1: no reset, no
  replacement). Before that, with a fraction f of the space held, all 64 default
  draws collide with probability f^64: about 0.1% at f = 0.9, about 53% at
  f = 0.99, refused `RequestIdDrawsCollided`.
- **Told.** The sending flow is answered `RequestArchived.RequestId`, or
  `ArchiveRejected.ArchiveRejection`, and nothing is written:
  - `Caller`: its seat or metaflow is not identified, the refusal of Send;
  - `UnknownRequest`: no held request of its own has the id. An id another flow
    sent reads the same, so the id teaches nothing;
  - `NotYet`: the request is not eligible (conditions 1 to 5); try again after it
    ends. One reason for all, so no flow learns of Message's Deliver, an internal
    call or another flow's request;
  - `StoreRefused`.

**Eligible**, read under the gates, every condition holding:

1. **Ended:** the state is Delivered, Read, Failed or Withdrawn, and every attempt
   of it is finished (Settled, Absent, Resolved or Read). Queued, Attempting,
   Retryable and Uncertain requests are held. So is a Withdrawn request whose
   attempt may have reached the seat and stays recorded as it stands. Whether it
   was answered is not asked: the sender decides.
2. **Not named:** no held request that has not ended shows its id: a Result or Done
   answering it, a Reminder for it, or an announcement or assignment Notice listing
   it (its row `Admitted` with that Notice not ended). A simplified reply owed on it
   counts as named (condition 5).
3. **Acknowledged:** no `DeliverCall` row of it waits for Message's Acknowledge
   (Paths, Deliver).
4. **Answered call:** no Send, send-tool call or Deliver that admitted it is still
   waiting for its answer to be written. This hold is in memory, one per call, and
   a restart drops it with the call.
5. **No open reply:** no open simplified-reply binding has it as its input.

Rows that only record history do not hold a request: its events, its send
outcomes, its send-call row, its purpose, the heartbeat's `outstanding`, answers
already ended. Each refers to it by LogicalDeliveryId, or shows the id as it was.

**The archive commit.** Under the dispatch gate, then the minting gate (the order
admissions take them), eligibility is read again, then one commit:

1. Its binding row is retracted.
2. Its current row keeps its final snapshot and gains `archived: Some(a)`, `a` a new
   cursor. Readers by LogicalDeliveryId (the direct-send wait, the heartbeat, the
   send tool's refresh) still read its final state.
3. The event at `a` is asserted: its snapshot with state `Archived`.
4. For an open Task: its reminder row is retracted. A reminder already admitted and
   not ended names the task (condition 2) and holds the archive.

Nothing is minted. A crash leaves all of it or none.

**History after archive.** These rows keep the old id as the id it had then: the
current row (marked `archived`), its events, its retained request and its
attempts (their QueueEntry), its send outcomes and send-call row, and answers
naming it (`Answered.{ L I words }`, where L ties the answer to it exactly). None
of them resolves an id. Every lookup by id goes through the binding table. A
binding names L, and L's current row must carry the same id and no `archived`
mark, or the lookup fails `StoreError::StateInvariant`. Outward:

- **ObserveSends, ObserveSender:** the `Archived` snapshot ends the id's request.
  A cursorless opening lists held requests only (Observation).
- **Send-tool replay:** a replayed call whose request is archived is answered
  `SendOutcome.Archived.{ Sender Target }`, never the stored id.
- **DebugDelivery, ArchiveRequest:** resolve held ids only. The old id is
  `UnknownRequest`, or names the request that holds it now (an ArchiveRequest
  reaches it only if its caller sent that request).
- **ReadSendOutcomes:** history. An outcome shows the id it was answered with.

**Backstop:** `commit_logical_transition` moves nothing out of Delivered, Read or
an archived row, and refuses with `StoreError::StateInvariant`. Only the archive
commit writes `Archived`.

## Wire (Ethos)

A diff against signal-flow 52, meta-signal-flow 65 and flow-ethos at 0.53.1.
Each excerpt is as checked in the scratch copy.

```ethos
; flow-ethos library.ethos
RequestId.String                                  ; new: four base36; unique among held requests, free once archived
ResultPayload.[ Answered.{ LogicalDeliveryId RequestId String }   ; was Answered.{ Answerable String }
                Historical.String ]
DonePayload.[ Answered.{ LogicalDeliveryId RequestId String }     ; was { LogicalDeliveryId Answerable String }
              Historical.{ LogicalDeliveryId String } ]
Request.[ ... Done.DonePayload
          Reminder.{ RequestId String } ]         ; new, last: Flow's reminder, the task's id and words
QueueEntry.{ LogicalDeliveryId RequestId SentBy Delivery Message }   ; RequestId is the entry's own
; Answerable is removed (no longer used)

; signal-flow signal.ethos
; import flow_ethos: Answerable removed, RequestId added
Deliver.{ Lock DeliverKey SendableMessage }       ; was { Lock Message }: Message's key; resolved like a Send
Acknowledge.Vector<DeliverKey>                    ; new request, Message only; answered Acknowledged
ArchiveRequest.RequestId                          ; new, ordinary socket: the sending flow archives its own request
DeliverKey.String                                 ; new: Message's own key for one Deliver; in Deliver and Acknowledge only
StoreIdentity.String                              ; new: drawn once for the store
SendableRequest.[ Order.String
                  Question.String
                  Psyche.Said
                  Psyches.Vector<Said>
                  Result.{ RequestId String }     ; answers an Order or a Question
                  Notice.String
                  Task.AnswerableTask
                  Done.{ RequestId String } ]     ; closes a Task
DeliveredRequest.[ Order.{ RequestId String }     ; new: the request as its recipient sees it, id first
                   Question.{ RequestId String }
                   Psyche.{ RequestId Said }
                   Psyches.{ RequestId Vector<Said> }
                   Result.{ RequestId String }    ; the id of the request it answers, not its own
                   Notice.{ RequestId String }
                   Task.{ RequestId Minutes String }
                   Done.{ RequestId String }      ; the id of the task it closes
                   Reminder.{ RequestId String }  ; the id of the open task, and its words
                   PriorResult.String             ; an answer admitted before ids: names no request
                   PriorDone.String ]
DeliveredMessage.[ HardAbrupt.DeliveredRequest    ; new; replaces VisibleMessage, removed
                   MiddleAbrupt.DeliveredRequest
                   Soft.DeliveredRequest ]
VisibleNativeInput.{ VisibleSender DeliveredMessage }
VisibleRequest.[ ... Reminder.{ RequestId String } ]   ; legacy evidence only
VisibleResultPayload.[ Answered.{ RequestId String } Historical.String ]
VisibleDonePayload.[ Answered.{ RequestId String } Historical.String ]
Refusal.[ ... TopicRefused.Topic Unresolved RequestIdSpaceFull RequestIdDrawsCollided MinutesRefused.MinutesRefusal ]   ; NoOpenTask and Ambiguous removed
VisibleRefusal.[ ... TopicRefused.Topic Unresolved RequestIdSpaceFull RequestIdDrawsCollided MinutesRefused.MinutesRefusal ]   ; Ambiguous removed
DeliveryState.[ ... Delivered.NativeReceipt Read Failed.Refusal Withdrawn Archived ]   ; Read: no receipt; Archived: the last snapshot
VisibleDeliveryState.[ ... Uncertain Delivered Read Failed.VisibleRefusal Withdrawn Archived ]   ; Delivered loses its receipt
SendAcceptance.{ LogicalDeliveryId RequestId DeliveryCursor DeliveryState }
SendReceipt.{ LogicalDeliveryId RequestId }       ; was { LogicalDeliveryId NativeReceipt }
SendFailure.[ Unadmitted.SendFailureReason        ; refused before admission: no delivery, no id
              Admitted.{ LogicalDeliveryId RequestId SendFailureReason } ]   ; was { Option<LogicalDeliveryId> SendFailureReason }
DeliverySnapshot.{ DeliveryCursor LogicalDeliveryId RequestId SentBy Address DeliveryState }
SendObservation.{ StoreIdentity DeliveryCursor Vector<DeliverySnapshot> }
VisibleSendAcceptance.{ RequestId DeliveryCursor VisibleDeliveryState }
VisibleSendReceipt.RequestId                      ; was NativeReceipt
VisibleSendFailure.[ Unadmitted.VisibleSendFailureReason
                     Admitted.{ RequestId VisibleSendFailureReason } ]
VisibleDeliverySnapshot.{ RequestId DeliveryCursor VisibleSender Address VisibleDeliveryState }
VisibleSendObservation.{ StoreIdentity DeliveryCursor Vector<VisibleDeliverySnapshot> }
ArchiveRejection.[ Caller.VisibleRefusal UnknownRequest NotYet StoreRefused ]
; responses added: Acknowledged; DeliverKeyReused, answered to Deliver alone and
; in no Refusal; RequestArchived.RequestId; ArchiveRejected.ArchiveRejection

; meta-signal-flow signal.ethos
; import signal_flow: VisibleMessage removed, DeliverySnapshot added; import flow_ethos: RequestId added
; every type that imports a changed shape (VisibleQueueEvidence, Letter,
; OrdinarySendOutcome, VisibleOrdinarySendOutcome) changes with it
Withdraw.{ Address LogicalDeliveryId }            ; unchanged: Withdraw by id is deferred (R3)
DebugDelivery.RequestId                           ; new query: one held request whole
DeliveryDebugged.{ DeliverySnapshot Receipt.Option<NativeReceipt> ReadBy.Option<LogicalDeliveryId> }   ; delivery evidence and answer evidence, apart
DebugDeliveryRejected.[ UnknownRequest StoreRefused ]
; no archive input here: archive is the sending flow's, on the ordinary socket
ConfigureCounters.{ LogicalDelivery.Integer QueueAttempt.Integer SendOutcome.Integer }   ; unchanged: no ids carried
CountersRefusal.[ NotEmpty Lowered.ConfigureCounters NotRunning ]                         ; unchanged
DrawBound.Integer
TryBound.Integer                                  ; new: Notices one task announcement may have admitted
ConfigurationChange.[ ... Counters.ConfigureCounters RequestIdDraws.DrawBound AnnouncementTries.TryBound ]
ConfigurationSnapshot.{ ... Counters.ConfigureCounters RequestIdDraws.DrawBound AnnouncementTries.TryBound }
ConfigureRejection.[ ... CountersRefused.CountersRefusal RequestIdDrawsRefused AnnouncementTriesRefused ]
ResolveQueueDeliveryRejection.[ ... AlreadyDelivered AlreadyRead ]   ; AlreadyDelivered loses its receipt (R3); AlreadyRead new
VisibleResolveQueueDeliveryRejected.[ ... AlreadyDelivered AlreadyRead ]

; flow-nexus send_tool.ethos
; import signal_flow: RequestId added
SendKind.[ Order Question Result.RequestId Notice ]   ; "request" is required with kind Result; Task and Done deferred (R3)
SendRefusal.[ ... TopicRefused.Topic Unresolved RequestIdSpaceFull RequestIdDrawsCollided ]
SendOutcome.[ Accepted.{ Sender Target SendAcceptance }
              LegacyUnknown.{ Sender Target }
              Archived.{ Sender Target }          ; new: a replay whose request has since been archived
              Refused.SendRefusal ]
```

An answer is `Unadmitted` if no delivery was written, and `Admitted` if one was,
whatever the reason. `Unadmitted` holds only the reason. The implementer may
narrow the reasons it can hold.

```datom
; sent: a request is written without an id
Send.{ { Mind core Sol } Soft.Order.«Review the drain fix.» }
; answered queued, then typed and received: the id alone
SendAccepted.{ «k7ph» 41 Queued }
Sent.«k7ph»
; delivered to Mind core Sol, the id first
[ { Sender.{ Psyche core Fable } Soft.Order.{ «k7ph» «Review the drain fix.» } } ]
; a later state: the cursor moves, the id stays; the receipt is not shown
SendChanged.{ «k7ph» 44 Sender.{ Psyche core Fable } { Mind core Sol } Delivered }
; answered by id, the request's text not repeated
Send.{ { Psyche core Fable } Soft.Result.{ «k7ph» «Reviewed; green.» } }
[ { Sender.{ Mind core Sol } Soft.Result.{ «k7ph» «Reviewed; green.» } } ]
; once the Result has ended, the sender archives the Order from its own seat
ArchiveRequest.«k7ph»
RequestArchived.«k7ph»
; its last snapshot
SendChanged.{ «k7ph» 52 Sender.{ Psyche core Fable } { Mind core Sol } Archived }
; «k7ph» is free; a later request may hold it, always at a higher cursor
SendChanged.{ «k7ph» 90 Sender.{ Psyche core Fable } { Field core Luna } Queued }
; a task, delivered, reminded, closed
Send.{ { Mind core Sol } Soft.Task.{ 30 «Rebuild the book.» } }
[ { Sender.{ Psyche core Fable } Soft.Task.{ «m2xq» 30 «Rebuild the book.» } } ]
[ { Sender.Flow Soft.Reminder.{ «m2xq» «Rebuild the book.» } } ]
Send.{ { Psyche core Fable } Soft.Done.{ «m2xq» «Rebuilt.» } }
; the living's words carry an id too, and no Result answers them
[ { Sender.{ Psyche core Fable } Soft.Psyche.{ «w3ne» { «context» «words» } } } ]
; Message relays under its own key; a resend with that key is answered from the record
Deliver.{ { … } «m-0193» Soft.Notice.«Tea at four.» }
SendAccepted.{ «r5tb» 61 Queued }
Acknowledge.[ «m-0193» ]
Acknowledged
; the same key with another request: answered apart, in no refusal a flow sees
Deliver.{ { … } «m-0193» Soft.Notice.«Tea at five.» }
DeliverKeyReused
; every observation opens with the store's identity
SendsObserved.{ «q0f3…» 61 [ ] }
; refused before admission: its own shape, no id
SendRefused.TopicRefused.«Core»
Failed.Unadmitted.Refused.Unresolved
Failed.Unadmitted.Refused.RequestIdDrawsCollided
; failed after admission: the id, plain
Failed.Admitted.{ «k7ph» ReceiptUncertain }
; the sender archives an Order that has not ended: refused, nothing written
ArchiveRequest.«t9da»
ArchiveRejected.NotYet
; meta socket: the receipt, by the debugging query only
DebugDelivery.«r5tb»
DeliveryDebugged.{ { 63 «0061» «r5tb» Sender.{ Psyche core Fable } { Mind core Sol } Delivered.{ Claude «5f1c…» «p-1» } } … }
```

## Memory

**New family `flow-nexus-request-id` v1.** One row per held request,
`RequestIdBinding { request_id, logical_delivery_id, closure }`, keyed by
`request_id`, asserted in the admission commit and retracted in the archive
commit. `closure` is `Open`, or `Answered(answer)`, the LogicalDeliveryId of the
Result or Done that closed it. It moves only from Open, never back.

**New family `flow-nexus-deliver-call` v1.** One row per Deliver Message has not
acknowledged, `DeliverCall { key, sender, digest, answer }`, keyed by the
DeliverKey: `answer` is the admitted response with its id. Asserted in the
admission commit, retracted by Acknowledge. Only Deliver and Acknowledge read it;
no query or reply shows it.

**New family `flow-nexus-store-identity` v1.** One row: the store's identity,
sixteen random base36 characters, drawn at a new store's first open or by the
upgrade, never changed.

**New family `flow-nexus-delivery-before-ids` v1.** One row per delivery the
upgrade archives, `PriorDelivery { logical_delivery_id, current, events, request,
attempts, outcomes }`, each field in its frozen 0.53.2 shape. Read by no query and
no reader in this revision: upgrade step 5 leaves no reference a reader resolves
naming a moved delivery.

**Changed rows.** The current row gains `archived: Option<DeliveryCursor>`. The
attempt phase gains `Read { answer, late_receipt }`, `answer` the answer's
LogicalDeliveryId and `late_receipt` an `Option<NativeDeliveryReceipt>`.

**New family `flow-nexus-task-announcement` v1.** One row per Notice part,
`TaskAnnouncement { recipient, part, tasks, tries, status }`, keyed by
`(recipient, part)`. `tasks` lists the tasks' LogicalDeliveryIds, fixed when the
row is written. `tries` counts the Notices admitted for it. `status` is one of:

- `Pending(Option<Refusal>)`: no Notice of it is admitted now; the refusal is its
  last refusal before admission, None before a try.
- `Admitted(notice)`: its Notice (by LogicalDeliveryId) is admitted and has not
  ended (Queued, Attempting, Retryable or Uncertain).
- `Delivered(notice)`: its Notice was delivered. Terminal.
- `Failed(notice)`: its last Notice ended Failed or Withdrawn with `tries` at
  `AnnouncementTries`. Terminal.
- `Closed`: no task it lists is still held and open; nothing is left to tell.
  Terminal.

**New family `flow-nexus-upgrade-assignment` v1.** The report of upgrade step 6
(R6). One row per Notice part, `UpgradeAssignment { sender, part, decisions,
tries, status }`, keyed by `(sender, part)`, `sender` the Orders' sender. Written
in the upgrade commit and never retracted; `decisions` is fixed when written, and
only `tries` and `status` change, as a task announcement row's do. One
`AssignmentDecision { recipient, assigned, open }` per group decided by delivery
order: `assigned` lists each answer with the Order it closes, `{ answer, order,
order_id }`, `answer` and `order` LogicalDeliveryIds and `order_id` the Order's
minted RequestId, or None for an Order the upgrade archives; `open` lists each
held Order of the group left Open, `{ order, order_id }`. Every row the decision
read stays where step 5 puts it, held or in `PriorDelivery`.

**Upgrade on first open.** One commit, before any native I/O, for a store whose
families are at the 0.53.2 versions. These move up one version from where 0.53.2
leaves them (at 0.53.1: current v6, event v6, metaflow v7, address-hold v6,
queue-delivery-request v7, queue-delivery-attempt v8, send-outcome v7, send-call
v7). Each row is decoded by its frozen shape, following the 0.42.0 pattern.

*Frozen shapes*, as read at 0.53.1, not verified against 0.53.2; the implementer
confirms them against the accepted 0.53.2 Memory before the upgrade is written:
- attempt v8: `{ request_id, attempt_id, native_request_id, flow_id, thread_id,
  harness_kind, history_anchor, address, queue_evidence, phase }`; evidence
  `Logical(QueueEntry { L, sent_by, delivery, message })` or
  `Legacy { sent_by, request }`; phase `Prepared`, `Uncertain(Option<Undecided>)`,
  `ReceiptRecorded(receipt)`, `Settled(receipt)`, `Absent(record)` or
  `Resolved(record)`.
- send outcome v7: `{ record: { send_outcome_id, caller, sender, recipient,
  digest, outcome } }`; outcome `Accepted { L, cursor, state }`, `Refused`,
  `PriorAdmission`, `Sent { L, receipt }` or `Failed { Option<L>, reason }`.
- send call v7: `{ key, digest, outcome }`; outcome `Accepted { sender, target,
  SendAcceptance }`, `LegacyUnknown` or `Refused`.
- current v6 and event v6: `{ snapshot: { cursor, L, sent_by, address, state } }`;
  retained request v7: `{ request_id, address, queue_evidence, state }`; metaflow
  v7 and address-hold v6 hold queues of QueueEntry.

In order:

1. **Check.** Every row decodes by its frozen shape. Every reference by
   LogicalDeliveryId has its current row: queue entries, retained requests,
   attempts with Logical evidence, outcomes (`Accepted`, `Sent`,
   `Failed { Some(L) }`), send-call `Accepted`, reminders, simplified-reply inputs,
   the heartbeat's `outstanding` and purposes. Every queue entry's current row has
   not ended. None of the new families exists yet. **Orphans:** a reference
   whose current row is missing is an inconsistency; the upgrade does not guess.
   Legacy evidence names no LogicalDeliveryId and is no orphan: it stays as it is.
2. **Held or archived.** A stored request is held if its state is Queued,
   Attempting, Retryable or Uncertain; or an attempt of it is unfinished; or it is
   a Task with an open reminder; or it is the input of an open simplified-reply
   binding. Every other stored request is archived by the upgrade and gets no id.
   This keeps the finished requests as 0.53.2 left them: no sender or recipient
   ever saw an id for them, so none waits for a sender's archive. A delivered Order
   or Question is archived even if unanswered: its recipient never saw an id, so no
   Result could name it.
3. **Mint** for held requests only, in ascending LogicalDeliveryId, by the Minting
   rule with the seeded bound.
4. **Held rows** are written in the new shapes with their id: current
   (`archived: None`), events, retained request, attempts (phase as it is; no
   stored attempt is Read), outcomes, send-call rows, and queue entries in
   metaflows and address holds. Each gets its binding, its closure set by step 6.
   Its sender never received the id (R5, settled). One sent by Flow or Unknown
   holds its id for good (Archive, R5).
5. **Archived rows:** current, events, retained request, attempts and outcomes of
   each archived delivery move unchanged into one `PriorDelivery` row. No
   `Archived` event is written for them, as they had no id. No id is freed, so
   minting in this same commit reuses none. Every other row that names a moved
   delivery by LogicalDeliveryId is handled in this same commit, by what its
   reader does (paths at `dade096`, under `crates/flow-nexus/src/`):
   - **Send-call rows** become `Archived.{ Sender Target }`, so the send tool's
     refresh (`send_tool.rs:414-416`) reads no moved delivery.
   - **The heartbeat's `outstanding`**, when it names a moved delivery, becomes
     `None`. Its one reader, `heartbeat_tick` (`heartbeat.rs:257-273`), clears it
     when the delivery's snapshot is Delivered, Failed or Withdrawn, and a moved
     delivery is one of those (step 2): the upgrade makes the clearing the tick
     would make. Left in place, the tick would find no current row, keep it, and
     never send that recipient a heartbeat again.
   - **Purpose rows** stay as they are. Their one reader, `heartbeat_evidence`
     (`heartbeat.rs:96-178`), matches them against queue entries, which name held
     deliveries only (step 1), and counts Ordinary rows per address; it reads no
     current row. Moving them would lower each recipient's sent count and make
     every heartbeat standing read as changed.
   - **Simplified-reply bindings:** an open one's input is held (step 2). A
     completed one stays; its readers return before reading its input
     (`store/logical_delivery.rs:505-560`).
   - **Reminder rows** exist only for open reminders, whose tasks are held (step 2),
     so none names a moved delivery.
   - **Queue entries, retained requests, attempts and outcomes** name held
     deliveries, or move with theirs.

   Every other reader by LogicalDeliveryId (the direct-send wait in `sending.rs`,
   `finish_failed_direct`, `withdraw_queued`, `mark_queue_retryable`, the wake's
   startup prefix) reads an id from a call in flight or a queue entry, and no call
   in flight survives the restart that runs the upgrade. So no reader reaches a
   `PriorDelivery` row, and none needs a path to one. Resolving through
   `PriorDelivery` instead would make every read by LogicalDeliveryId a second
   lookup in a frozen shape, for one durable reference the tick's own rule already
   clears.
6. **Old answers and closures.** First, each held request's closure is read from
   the answers as stored, in their frozen shapes, moved answers included:
   - a Task is `Answered(d)` if a stored `Done.Answered.{ L … }` names its L, `d`
     that Done's LogicalDeliveryId; a Task whose reminder is open has none;
   - an Order (or a Question, if 0.53.2 answers it) is closed by delivery order
     (R6). Its group is every stored Order, held or moved, with the same recipient
     S, the same sender R and the same text; its answers are every stored
     `Result.Answered` with a LogicalDeliveryId, sent by S to R, whose Answerable
     names that text. (A Result in Legacy evidence names no delivery; 0.53.1's
     matcher reads Logical entries only, `store/queue_delivery.rs:518-532`.)
     - **Keys.** An Order's delivery-order key is the cursor of its first event
       whose state is `Delivered(_)`:
       `LogicalDeliveryEvent.snapshot.delivery_cursor`, the event row's own key
       (`store/logical_delivery.rs:113-119` at `dade096`). An answer's key, and
       any request's admission cursor, is the cursor of its first event.
       Every event takes its own cursor from the one counter under the
       logical-delivery write gate (`commit_logical_transition`, `:1258-1313`;
       `settle_wake_startup_receipts`, `:400-460`; the admissions), and events are
       only asserted, never retracted, so no two events share a cursor and every
       key is unique. 0.53.1's own matcher ordered by each request's current
       cursor (`:864`), which moves with every state change and orders no
       delivery; it is not used.
     - **Ties.** Two Delivered keys never tie. An Order with no `Delivered` event
       has no delivery-order key: it comes after every Order with one, and among
       such Orders by admission cursor, also unique, and is reported like the rest
       (ruled by Fable, R6 extended).
     - **Assignment.** The answers are taken in ascending key. Each is assigned to
       the unassigned Order of its group, admitted below the answer's key, that
       comes first in delivery order; an answer with none is assigned none.
     - **Closure.** A held Order assigned answer `r` is `Answered(r)`. A held
       Order assigned none stays `Open` with its new id, which its recipient
       answers by (Answers). A moved Order's assignment changes no row of it.
     - **Report.** Every group with two or more Orders and at least one answer is
       decided by delivery order and reported, both ids with it (Assignment
       report). This case never fails the upgrade (R6);
   - the input of a completed simplified-reply binding is `Answered(p)`, `p` its
     reply's LogicalDeliveryId (`simplified-result-{flow}-{input}`,
     `store/logical_delivery.rs:591`);
   - every other held request is `Open`.

   A held request answered before ids is thereby closed, whatever kept it held: an
   Order Delivered with an unfinished attempt settles by its receipt as before and
   is never Read; an Uncertain one stays Uncertain until resolved by its digest or
   `ResolveQueueDelivery`, as the settlement to Read runs only on an admitted
   answer. A Result or Done naming its id is Unresolved (Answers, step 8), so no
   answer given before ids is given again (blocker h). The one exception is R6's:
   an identical Order left open by delivery order may be answered by its new id,
   and its sender is told (Assignment report).

   Then every `Result.Answered.{ Answerable String }` becomes
   `Result.Historical.String`, and every `Done.Answered.{ L Answerable String }`
   becomes `Done.Historical.{ L String }`. A Done already closed its task's
   reminder when it was admitted.
7. **Removed refusals:** stored `Refusal.Ambiguous` and `Refusal.NoOpenTask(_)`
   become `Unresolved` (`message_projection.rs:34`). **Outcomes of held requests:**
   `SendFailure { Some(L) reason }` becomes `Admitted.{ L id reason }`, `None`
   becomes `Unadmitted.reason`, and `Sent.{ L receipt }` becomes `Sent.{ L id }`;
   the receipt stays in the delivery's `Delivered` state.
8. **Announcement rows** for open tasks (Task announcement, below), and
   **assignment rows** for the groups step 6 reports (Assignment report, below).
9. **Store identity** drawn; family versions bumped.
10. **Fail closed:** a failed check, more held requests than the space, an
    exhausted draw, or a reference a reader resolves (the step 1 list less
    purposes and completed simplified-reply bindings) left naming no current row
    after step 5 fails the open with `StartRefusal.Store` naming it, and nothing
    is written: the store stays byte for byte as it was.

**Idempotent (constraint d).** A store at the new versions is not touched. The
upgrade is one commit, so no partial result exists to resume.

- A store opened by 0.53.3 is not opened by an earlier Flow. Take the usual backup
  first.

**Task announcement (ruling 5).** An open task is a held Task with an open
reminder in Attempting, Uncertain or Delivered (a Queued or Retryable task is
delivered with its id).

*Rows, at upgrade step 8.* Group the open tasks by recipient, in ascending
LogicalDeliveryId. Split each group into parts, in that order, so each part's
Notice fits the rendered-prompt budget (measured with placeholder ids). The Notice
is a `Soft` Notice from Flow: "Your open tasks; close each with Done by its id:"
then one line per task, `id words`; a line too long to fit alone is cut to fit,
ending "…". Write one row per part, `tries` 0, `Pending(None)`.

*A pass*, under the dispatch gate, once serving, in order:

1. Each `Admitted(n)` row: read n's state by its LogicalDeliveryId. Delivered:
   `Delivered(n)`. Failed or Withdrawn (both reached only by a request that never
   reached the seat): `Pending(None)` if `tries` is below `AnnouncementTries`, else
   `Failed(n)`. Any other state: unchanged; an Uncertain Notice is never sent
   again, and the reminders still carry each task's id (ruling 4).
2. Each `Pending` row, in `(recipient, part)` order: its Notice lists the row's
   tasks still held and open, each id read from its binding now. None: the row
   becomes `Closed`.
3. Otherwise admit that Notice through the ordinary admission, minting its own id.
   In the same commit the row becomes `Admitted(n)` and `tries` rises by one. From
   then until n ends, its tasks are named (Archive, condition 2).
4. A refusal before admission (the recipient's metaflow not held, `Unknown`;
   `RequestIdSpaceFull`; `RequestIdDrawsCollided`; any other) writes
   `Pending(Some(refusal))` if the row's last refusal differs, `tries` unchanged.
   The row is tried again at the next pass.

*When:* a pass runs on a change, never on a timer:

- at each start;
- after a commit changes the state of an `Admitted` row's Notice;
- after a committed archive: it frees a binding, the change a `RequestIdSpaceFull`
  waits for;
- after a committed admission made outside a pass: the table has changed, the
  change a `RequestIdDrawsCollided` waits for, with an archive;
- after a commit adds a metaflow: the change a recipient not held waits for.

The last three run a pass only while some row is Pending. A trigger that comes
while a pass runs makes one more pass after it, however many come. A pass's own
commits trigger nothing. A row refused for any other reason is tried at each pass
these bring, and at the next start. Triggers are kept in memory; one lost to a
crash is covered by the pass at start.

*Bound:* a pass tries each Pending row at most once; passes follow triggering
commits, coalesced, and none follows a pass's own; a row has at most
`AnnouncementTries` Notices admitted. `AnnouncementTries` is a
configuration (`Configure.AnnouncementTries`), default 3, at least 1 (below 1 is
`ConfigureRejected.AnnouncementTriesRefused`); a new Memory seeds the default.

*Restart-safe:* step 3 writes the admission and the row together, so one try
admits one Notice. Step 1 reads the Notice's durable state, so a crash between a
Notice's change and its row's is repaired at the next pass. A Notice is admitted
again only after its predecessor never reached the seat, so a recipient is told
once. A row never shows an id it did not read from a held binding, so it never
teaches an archived one.

**Assignment report (R6).** The owner of an Order is its sender (R5). Every group
upgrade step 6 decides by delivery order goes to its sender, both ids with it.

*Rows, at upgrade step 8.* Group the decisions by sender, in ascending
LogicalDeliveryId of each group's first Order, and split them into parts as the
task announcement does. The Notice is a `Soft` Notice from Flow: "Identical
Orders answered before ids; each answer was given to the earliest delivered. If
one is wrong, archive the open one or send it again:" then one line per decision
and Order, `id answered words` or `id open words`, an Order the upgrade archived
shown as `archived answered words`; a line too long to fit alone is cut to fit,
ending "…". Write one row per part, `tries` 0, `Pending(None)`.

*The pass* is the task announcement's, one pass for both families, task rows
first: the same steps, statuses, triggers, bound (`AnnouncementTries`) and restart
rules, with `sender` for `recipient`. Its Notice lists the row's decisions that
still have a held Order, each id read from its binding now; an Order the upgrade
archived, or its sender has since archived, is shown `archived`. A row with no
held Order left becomes `Closed`. The rows themselves are the durable report:
decisions are never rewritten, and the row stays after its Notice ends.

*Correcting.* An Order wrongly left open is archived by its sender, or answered by
its recipient by its id. An Order wrongly closed is sent again by its sender; no
input reopens a closure (R6, extended).

**Restart:** ids, bindings, closures, archive marks, DeliverCall rows, the store
identity, announcement rows and assignment rows are durable. Nothing is
re-minted. Nothing is archived at start; in-memory call holds (condition 4) end
with their calls. A send-tool replay reads the stored outcome with its id, or
`Archived` if its request is archived.

**`Configure.Counters` store replacement (R1).** Unchanged from 0.53.1: taken only
on an empty store (`NotEmpty` otherwise). An empty store holds no binding, as a
binding exists only with its delivery, so Counters never meets a held binding and
carries no ids. In the new store every id is free. The replaced store's held
requests end with that store, unarchived, and their ids name nothing in the new
one (Unresolved). Consumers learn of the change from the new store identity
(Observation). Replacement is not a remedy for a full space.

**Naming:** queue-delivery rows already have a private field `request_id` (the
queue request key, `store/queue_delivery.rs:107,222`). It is renamed
`queue_request_id` so the name has one meaning.

## Answers (Result and Done)

The Nexus authenticates the answer's sender S: for a Send, the calling process's
flow and its Awake metaflow; for a Deliver, the Lock's Sender; for the send tool,
the thread's metaflow. S is never read from the message. The answer names a
recipient R and a referenced id I. `resolve_sendable_message`
(`logical_delivery.rs:831`) runs these steps under the minting gate, in this
order. The first that fails refuses and writes nothing. A step 1 or 2 failure
keeps its own refusal; every failure from step 3 to step 8 is `Unresolved` and
reads the same to the caller.

1. S is authenticated (the existing refusals: Unidentified, NotAwake, Locked, Held).
2. R is a metaflow Flow holds (Unknown, TopicRefused).
3. `binding(I)` gives a held delivery L. No binding: Unresolved (R2), whether I was
   never drawn or its request is archived.
4. L's recipient is S.
5. L's sender is `Sender(R)`. A sender `Unknown` or `Flow` matches no R.
6. The kinds match: a Result needs L to be an Order or a Question; a Done needs L
   to be a Task. A Psyche, Psyches, Notice, Reminder, Result or Done is
   Unresolved.
7. L's state is Delivered, Read or Uncertain. Queued, Attempting, Retryable,
   Failed and Withdrawn are Unresolved.
8. L's closure is `Open`. A Task also needs an open reminder (address R, recipient
   S); the check at admission (`logical_delivery.rs:1050-1066`) stays.
9. The existing admission checks (Oversized, Minutes).
10. Mint the answer's own id A by the Minting rule; `RequestIdSpaceFull` or
    `RequestIdDrawsCollided` if it cannot.
11. One commit:
    - the answer's delivery, with own id A, carrying `Result.Answered.{ L I words }`
      or `Done.Answered.{ L I words }`, and its binding for A;
    - L's closure becomes `Answered(A's LogicalDeliveryId)`;
    - L, if Delivered: its state unchanged; L, if Uncertain: the settlement below,
      on this authenticated answer and nothing else;
    - for a Done, the task's reminder closes.

L stays held until its sender archives it. The answer names it until the answer
ends (Archive, condition 2), and this commit archives nothing.

The id alone proves nothing: steps 4 and 5 test the authenticated parties, so a
stranger who knows I is refused as anyone else is, and learns nothing of L's kind,
state or closure. The one case the id cannot tell is the accepted risk (R2): a
duplicate answer from S to R landing on a later request from R to S that holds I.

**Uncertain to Read (blocker i, R3).** The settlement, inside step 11's commit, in
order:

1. Find L's one unfinished attempt; while L is Uncertain it is in
   `Uncertain(_)`. None, or more than one, is a store fault: the whole answer is
   refused `Store` and nothing is written.
2. That attempt's phase becomes `Read { answer: A's LogicalDeliveryId,
   late_receipt: None }`. Its evidence is the answer alone: no resolver, no
   process, no receipt is recorded.
3. L's retained request row, Queued or Parked, becomes Settled.
4. If L is still in its metaflow's queue (at its head, unparked), it leaves it.
5. L's state becomes `Read`, at a new cursor, with its event row.

Answer evidence and delivery evidence stay apart: the answer is in `answer`, a
receipt only ever in `late_receipt` or a `Settled` phase. DebugDelivery shows them
as `ReadBy` and `Receipt`.

`Read` counts as settled wherever `Settled` does: `is_finished` holds, it is not
listed by ReadQueueDeliveries or Inspect, and neither `unsettled_deliveries` nor
`recover_outstanding_deliveries` returns it.

Once L is Read or Delivered, nothing moves it or overwrites it but the archive:

1. **A late receipt** (`record_delivery_receipt`) on a `Read` attempt with no
   late receipt is kept as `late_receipt`; the same receipt again is a no-op, a
   different one is refused as at `ReceiptRecorded` today. L stays Read.
2. **`settle_recorded_delivery`** on a `Read` attempt writes nothing.
3. **A stale Absent** (`mark_delivery_absent`), and `mark_delivery_uncertain`,
   `mark_delivery_undecided` and `park_uncertain_delivery`, on a `Read` attempt
   write nothing and return false, as on `Settled`.
4. **`ResolveQueueDelivery`** on a `Read` attempt, either outcome, is refused
   `AlreadyRead`, and on a `Settled` one `AlreadyDelivered`; neither carries a
   receipt (R3), and nothing is written.
5. **A restart** finds the attempt finished and reconciles nothing.
6. **A retry or requeue:** L is no longer queued, so `prepare_oldest_delivery`
   never hands it over and Withdraw finds it `NotQueued`; `mark_queue_retryable`
   moves only Queued and Retryable; `seed_missing_queued_deliveries` seeds only
   queue entries; `finish_failed_direct` returns the state unchanged on Read as
   on Delivered.
7. **The backstop** (Archive) refuses any other move.

**Two ids (constraint b).** The answer has its own id A, the id of its delivery
row, binding, snapshot and queue entry; the id it answers, I, is in its stored
payload with L. Both are durable. The recipient's pane shows only I
(`Result.{ I words }`); the answer's sender sees A in its acceptance and
snapshots. A Result naming A is Unresolved at step 6.

An id names at most one held request, so Ambiguous can no longer happen and is
removed.

`deliver_simplified_reply` admits `Result.Answered` naming the input's id, through
the same steps 3 to 11. Every queue entry has an id, so the `Historical` branch
remains for one case only: an input whose closure is not `Open` because it
was answered before ids (Upgrade, step 6). Its reply is admitted as
`Result.Historical.String`, 0.53.1's own form, with its own minted id and naming
no request, and the binding completes in the same commit. So the reply's words
are delivered, the input is not answered twice, and no open binding is left to
hold the input from archive (condition 5).

## Paths

- **Several sends in flight:** each Send gets its own id. Two identical Orders to
  one recipient have two ids, and each Result closes exactly one.
- **Direct sends:** the direct path admits first (`metaflow.rs:173-231`,
  `sending.rs:285`), so `Sent` and `Failed.Admitted` (`NotSent`, or `Refused`
  after admission) carry the admitted id. The ten-second
  `SendAccepted(Uncertain/Attempting)` (`sending.rs:1420`) carries the same id, so
  a stale cursor no longer breaks the link. The call holds its request from
  archive until its answer is written (Archive, condition 4), so `Sent` never
  shows an id already free. A refusal before admission carries none.
- **Deliver (Message's relay):** `Deliver.{ Lock DeliverKey SendableMessage }`,
  the Lock's Sender as S and its Address as R, accepted only from the bound
  Message process. In order:
  1. A DeliverCall row under that key with the same digest: answered from its
     stored answer, and nothing is admitted. With another digest:
     `DeliverKeyReused`. This comes before the Lock check, as the admission
     consumed the Lock.
  2. Otherwise resolved and admitted through `resolve_sendable_message`; the
     admission commit writes the DeliverCall row with the answer and its id. A
     refusal before admission writes no row, and a resend is tried afresh.
  3. `Acknowledge.Vector<DeliverKey>` retracts those rows (unknown keys are
     skipped) and answers `Acknowledged`.

  **A lost answer:** the request stays bound, as an unacknowledged DeliverCall
  keeps it from archive (condition 3). Message learns its id by sending the same
  Deliver again with the same key, which is answered from the record. No cursor,
  text or LogicalDeliveryId is involved. The key is Message's own, on the Message
  contract alone: no flow sees it, no snapshot carries it, nothing resolves by it,
  and it is gone at Acknowledge. Message no longer supplies a private
  `LogicalDeliveryId` in a Done.
- **The DeliverKey (R4).** It never appears in a Sent, a delivered request, or any
  debugging answer meant for a flow. The types hold it:
  - `DeliverKey` is the type of one field in the contract: `Deliver`'s, and the
    element of `Acknowledge`'s vector. The Nexus's private DeliverCall row keeps it
    and no query or reply reads that row.
  - No Sent (`SendReceipt`, `VisibleSendReceipt`), no `SendAcceptance`,
    `SendFailure`, `DeliverySnapshot` or their Visible forms, no
    `DeliveredRequest` or `VisibleNativeInput`, and no `DeliveryDebugged`,
    `DebugSnapshot` or send-outcome record has a field of that type, directly or
    through a type it holds.
  - The answers to a Deliver are the ordinary ones (`SendAccepted`,
    `SendRefused`, `Failed`, `Acknowledged`) and the unit `DeliverKeyReused`,
    which is no `Refusal`: Refusal also fills `Failed` in a snapshot and the
    refusals flows read, so the variant is moved out.
  - A resend is answered from the stored answer, which holds an id and no key.
- **Withdraw:** unchanged from 0.53.1, by `LogicalDeliveryId`, which the owner
  reads from DebugDelivery or `Debug.Address`; Withdraw by id is deferred (R3). A
  Withdrawn request keeps its binding until it is archived.
- **Debugging query (R3):** meta `DebugDelivery.RequestId` answers
  `DeliveryDebugged.{ DeliverySnapshot Receipt ReadBy }`: the private snapshot,
  the native receipt its attempt holds (delivery evidence), and the answer that
  settled it as Read (answer evidence), by LogicalDeliveryId so it never names a
  reused id. `UnknownRequest` for an id no held request has. It sits with
  `Debug.Address`, the one explicit interface that exposes private keys, and it
  is the only reply that carries a receipt.
- **Archive:** ordinary `ArchiveRequest.RequestId`, the sending flow's (Archive).

## Observation across archive and reuse

- **Order.** Every snapshot of a request comes at or above its admission's
  cursor, and `Archived` is its last. The admission that draws the id again comes
  at a higher cursor (Minting). So, for one id, a cursor-ordered stream is cut by
  its `Archived` snapshots into requests: a snapshot of I at cursor c belongs to
  the request whose span, from the previous `Archived(I)` to the next, holds c.
- **With a cursor,** ObserveSends and ObserveSender replay every event after it,
  in cursor order, `Archived` included. Events are never pruned, so nothing is
  skipped. The highwater is the cursor counter less one, so it holds when the
  upgrade moves archived events out.
- **Without a cursor,** the opening lists held requests only. A consumer that
  tracked ids drops them all before it opens without a cursor; every request it
  then sees is new to it.
- **Buffers.** A consumer that holds a snapshot of I to classify later orders it
  against `Archived(I)` snapshots by cursor, never by arrival.
- **Store identity.** Every opening carries the StoreIdentity. A consumer whose
  stored identity differs (a replaced or upgraded store) drops its cursor and
  every id it tracked.
- **Limit.** A Result or Done delivered to a pane, and an id a flow remembers,
  carry no cursor. A delayed duplicate answer is covered only by R2's accepted
  risk.

## Projection (`message_projection.rs`)

- `visible_send_response`, `visible_send_outcome_record` and
  `visible_delivery_snapshot` copy the `RequestId` into the visible types.
  `logical_delivery_id` is still dropped. `Delivered.NativeReceipt` projects to
  `Delivered`; `VisibleSendReceipt` is the id alone; `Archived` to `Archived`.
- `visible_send_observation` copies the StoreIdentity.
- `visible_send_failure` maps `Unadmitted` to `Unadmitted` and `Admitted` to
  `Admitted`, dropping the logical id.
- `visible_refusal` loses its NoOpenTask and Ambiguous arms and gains
  `RequestIdSpaceFull` and `RequestIdDrawsCollided`.
- A new `delivered_request(id, &Request) -> DeliveredRequest` adds the id to
  Order, Question, Notice, Task, Psyche and Psyches. Result and Done `Answered`
  show their stored (referenced) `RequestId`. `Reminder` shows its task's id.
  `Historical` becomes `PriorResult` or `PriorDone`.
- `ProjectsQueueEntry::visible_input` returns `VisibleNativeInput`, always: every
  queue entry has an id, so the pane renderers (`composition.rs:712`,
  `waking.rs:1969`, `delivery/body.rs`) and `visible_queue_evidence` have no id-less
  case.
- `visible_request` stays only for legacy evidence. Its `Answered` arms show the
  `RequestId`.
- Composer read-back (`delivery/body.rs:173,381`) parses the new
  `VisibleNativeInput` shape.
- Reminders (`reminding.rs:64-80`) build `Request::Reminder { task id, task words }`,
  reading the id from the task's binding. The last reminder's failure Notice to
  the sender stays a Notice. Stored old reminders stay Notices.

## Consumers

- **flow CLI:** no code changes beyond the wire pin. It parses
  `Soft.Result.{ «k7ph» «…» }` and prints answers and snapshots with their plain
  ids; a `Failed` prints `Unadmitted` or `Admitted` with its id. Its parse tests
  (`crates/flow/src/main.rs:188,208`) move to the id form.
- **A flow answering:** it reads the id at the head of the delivered request and
  sends `Result.{ id words }` for an Order or a Question, or `Done.{ id words }` for
  a Task, to the sender shown. It does not repeat the request. A flow that sent a
  request archives it with `ArchiveRequest.{ id }` when it needs the id no more.
  Its Curriculum send skill teaches both; that text is outside this change.
- **A Codex flow on the send tool:** kind `Result` takes `"request": "k7ph"` and
  resolves as above. Without `request` it is refused `Malformed`; an id that does
  not resolve is refused `Unresolved`. The accepted outcome shows the id through
  `SendAcceptance`; a replay after archive answers `Archived`.
- **Message.** The boundary Flow relies on; Message's own code is outside this
  change. Message keeps, durably and per StoreIdentity:
  - its observation cursor P: every event at or below P is classified and its
    effect written, and no event above P has its effect written;
  - an outbox: each Deliver's key and request, written before it is sent;
  - a ledger: key to RequestId and acceptance cursor, written when the answer
    arrives;
  - a pending set: keys sent with no ledger entry yet.

  A snapshot held unclassified is kept in memory only, and P never passes it
  (blocker n). Flow keeps every event and replays every event after a cursor, in
  cursor order (Observation; events are only asserted and keyed by their cursor,
  `store/logical_delivery.rs:113-119,1351-1360` at `dade096`), so a cursor kept
  below the earliest unclassified event brings every held snapshot back with
  nothing stored beside it. A durable held buffer would copy part of that log
  into Message and need its own atomic write with the cursor, its own replay
  order and its own retirement, for the same guarantee.

  In order:
  1. **Answer:** write the ledger entry, then Acknowledge. A refusal before
     admission marks the outbox entry refused: no id, nothing to follow.
  2. **Restart or reconnect:** if the opening's StoreIdentity differs from the one
     stored, drop the cursor, ledger and pending set. Otherwise resume with the
     stored cursor, resend every pending Deliver with its key, and Acknowledge
     every ledger entry. Both are answered from Flow's record without a second
     admission. The replay after P returns every event held before the crash, in
     cursor order, and each is classified afresh by step 3.
  3. **Classify** each ObserveSender snapshot of I at cursor c, strictly in cursor
     order. Message may read ahead, but acts on the event at c only after every
     event below c:
     - while any Deliver is pending, or the stream read has not reached the highest
       acceptance cursor in the ledger (read through it: the highest cursor read is
       at least that cursor; no later event is awaited), a snapshot whose id is not in the ledger is
       held unclassified. It is neither Message's relay nor the flow's own, and
       every later event waits behind it, in memory;
     - **Entry selection.** The candidate for a snapshot of I is the ledger entry
       of I with the lowest acceptance cursor a not yet retired; ledger entries
       sharing I never share a span, since I is reused only after an
       `Archived(I)`, and retirement goes in cursor order. The snapshot waits,
       held, until the stream has been read through a (the highest cursor read is
       at least a; no later event is awaited), so the last `Archived(I)` below
       a, at cursor b (0 if none), is known. It is Message's relay if b < c; the
       candidate's span runs from b to its own `Archived(I)`. Any other entry of I
       is never consulted for it: a newer entry never classifies an older
       snapshot because it shares I;
     - otherwise it is the flow's own;
     - an `Archived(I)` in a ledger entry's span retires that entry when its turn
       comes, so every earlier event of that span is classified first; an event of
       a later request holding I finds no entry, or its own with a higher
       acceptance cursor.
  4. **Cursor commit:** the effect of the event at c (its classification, a
     retirement) and P's advance to c are one durable write. P never passes the
     earliest event held unclassified. An effect Message makes beyond its own
     store is made before that write, so a crash between them repeats it on
     replay; the StoreIdentity and c name the event uniquely, so a repeat can be
     recognised.
  5. Message never opens without a cursor while its ledger or pending set holds
     anything, unless the StoreIdentity changed.

## Versioning

- **Flow:** 0.53.3.
- **signal-flow:** the next major after the accepted 0.53.2 contract. Breaking:
  types are removed, renamed and reshaped.
- **meta-signal-flow:** the next major after the accepted 0.53.2 contract. It
  imports the changed shapes.
- **Allocation:** 0.53.2 is prepared as signal-flow 53 and meta-signal-flow 66 and
  is not yet accepted, so 0.53.3 allocates no major now. When 0.53.2 is accepted,
  the Wire diff is rebased onto its exact contract and 0.53.3 takes the next
  majors after it (54 and 67 if 0.53.2 lands as prepared).
- **flow-ethos:** moves with Flow.
- **Release notes:** UPGRADES.md for 0.53.3 states the pins, the family versions,
  the upgrade (held and archived requests), archive, the DeliverKey and
  Acknowledge, the store identity, the announcement and the assignment report.

## Tests

Minting (ruling 1, R1)
- `request_id_is_four_base36_characters`
- `request_id_collision_redraws_and_stays_four_characters` (scripted source draws a held id, then a free one)
- `request_id_draws_collided_refuses_unadmitted_and_writes_nothing`
- `request_id_draws_collided_below_a_full_space_is_not_space_full`
- `request_id_space_full_of_held_requests_refuses_without_drawing`
- `request_id_draw_bound_is_configurable` (zero is RequestIdDrawsRefused)
- `held_request_id_is_never_drawn`
- `archived_request_id_is_drawn_again` (scripted source)
- `request_id_survives_restart`
- `request_id_drawn_independently_of_logical_id`
- `oversized_counts_the_delivered_form`

Archive (item 1, R5)
- `nothing_archives_without_its_sender` (an ended, answered request stays held across commits and restarts)
- `meta_socket_has_no_archive_request`
- `sender_archives_a_delivered_notice`
- `sender_archives_an_answered_order_after_its_answer_ends`
- `sender_archives_an_unanswered_delivered_order`
- `sender_archives_a_failed_or_withdrawn_request`
- `sender_archives_an_open_task_and_its_reminder_closes`
- `sender_archives_a_request_relayed_by_message` (the Lock's Sender)
- `archive_by_a_stranger_holding_the_id_is_unknown_request` (reads as an id no held request has; nothing written)
- `archive_from_an_unidentified_process_is_refused_caller`
- `archive_refused_not_yet_names_no_condition` (one reason for conditions 1 to 5)
- `archive_refusals_write_nothing`
- `archive_refuses_a_request_not_ended` (Queued, Attempting, Retryable, Uncertain)
- `archive_refuses_a_withdrawn_request_with_an_unfinished_attempt`
- `archive_refuses_a_request_named_by_an_unended_answer`
- `archive_refuses_a_task_named_by_a_queued_reminder`
- `archive_refuses_tasks_listed_by_an_unended_announcement_notice`
- `archive_refuses_orders_listed_by_an_unended_assignment_notice`
- `archive_refuses_a_request_with_an_unacknowledged_deliver`
- `archive_refuses_a_request_whose_admitting_call_is_unanswered`
- `archive_refuses_the_input_of_an_open_simplified_reply`
- `flow_archives_none_of_its_own_requests` (a reminder, an announcement Notice, a failure Notice, a heartbeat Notice and an Unknown-sender request, all ended, stay held across commits and restarts)
- `archive_request_naming_a_flow_or_unknown_sent_request_is_unknown_request` (nothing written)
- `space_held_by_flows_own_requests_refuses_flows_own_admissions_space_full` (scripted: a full table of Flow-sent requests; a heartbeat and a reminder are refused, nothing written)
- `archive_commit_retracts_binding_and_writes_archived_event_together` (fault injected: both or neither)
- `archived_current_row_keeps_its_final_snapshot`
- `archived_rows_never_resolve_an_id` (after reuse, lookups reach the new request; old rows unchanged)
- `binding_naming_an_archived_row_is_a_state_invariant`
- `transition_out_of_delivered_read_or_archived_is_refused`
- `archive_survives_restart`
- `tool_replay_after_archive_answers_archived`

Ordering (item 2)
- `no_commit_archives_and_mints`
- `archived_id_is_drawable_from_the_next_commit`
- `reused_id_admission_cursor_is_above_its_archived_event`
- `archive_and_admission_never_interleave` (the minting gate is held)

Deliver answer (item 3)
- `deliver_answer_is_kept_under_its_key_in_the_admission_commit`
- `deliver_resent_with_its_key_answers_the_stored_id_and_admits_nothing`
- `deliver_resent_after_its_lock_was_consumed_answers_from_the_key`
- `deliver_key_with_another_request_refused_deliver_key_reused`
- `deliver_refused_before_admission_keeps_no_key`
- `acknowledge_releases_the_key_and_lets_the_request_archive`
- `acknowledge_of_unknown_keys_answers_acknowledged`
- `acknowledge_from_other_than_message_refused`
- `deliver_key_survives_restart`
- `deliver_lost_answer_recovered_by_key_alone` (no cursor, text or logical id read)
- `deliver_key_is_the_type_of_no_field_but_deliver_and_acknowledge` (R4: walks the contract's types)
- `sent_cannot_carry_a_deliver_key` (R4: DeliverKey is reachable from no Sent, SendAcceptance or SendFailure type, Visible forms included)
- `delivered_request_cannot_carry_a_deliver_key` (R4: DeliveredRequest, DeliveredMessage, VisibleNativeInput)
- `debugging_answer_cannot_carry_a_deliver_key` (R4: DeliveryDebugged, DebugSnapshot, send-outcome records)
- `deliver_key_text_appears_in_no_reply_or_pane` (R4: a distinctive key through Deliver, then Sent, SendChanged, ObserveSends, the pane text, DebugDelivery, Debug.Address and ReadSendOutcomes, none holds it)
- `deliver_key_reused_is_no_refusal_a_flow_reads` (R4: absent from Refusal and VisibleRefusal; answered to Deliver alone)

Reminders and announcements (item 4)
- `reminder_reads_its_task_id_from_the_binding`
- `announcement_notice_lists_only_held_open_tasks` (a task its sender archived is left out)
- `announcement_text_reads_ids_from_bindings_at_admission`
- `announcement_never_teaches_an_archived_id`

Observation (item 5)
- `archived_is_the_last_snapshot_of_its_request`
- `cursor_replay_includes_archived_in_cursor_order`
- `reused_id_snapshots_follow_its_archived_event`
- `cursorless_opening_lists_held_requests_only`
- `observation_opens_with_the_store_identity`
- `observation_highwater_is_the_cursor_counter`
- `observe_sends_never_shows_another_senders_id`
- `cursor_replay_from_one_cursor_is_identical_each_time` (archived and reused-id events included; Message's replay relies on it)

Message boundary (item 6; Flow side here, Message side named for Message's repository)
- `observe_sender_tells_relays_from_own_sends_by_id`
- `message_holds_unknown_snapshots_while_a_deliver_is_pending`
- `message_classifies_held_snapshots_once_its_stream_passes_the_acceptance_cursor`
- `message_takes_a_snapshot_below_the_last_archived_as_not_its_relay`
- `message_retires_a_ledger_entry_on_archived`
- `message_drops_its_ledger_on_a_store_identity_change`
- `message_resends_pending_delivers_by_key_on_restart`
- `message_acknowledges_only_after_its_ledger_entry_is_durable`
- `message_never_opens_without_a_cursor_while_tracking`
- `message_cursor_never_passes_an_unclassified_event` (blocker n)
- `message_acts_on_events_in_cursor_order_behind_a_held_one` (a later event classifiable at once waits; P stays below the held one)
- `message_writes_an_events_effect_and_its_cursor_together` (fault injected: both or neither)

Message crash witnesses (blocker n; named for Message's repository; each injects a crash at one point, restarts against the same Flow store, and witnesses every event classified once, in cursor order, none lost, and no effect in Message's store written twice)
- `message_crash_after_holding_before_any_cursor_write_replays_the_held_event`
- `message_crash_after_the_cursor_write_below_a_held_event_replays_it` (P at the event before it, never at it)
- `message_crash_with_the_answer_lost_recovers_by_key_and_classifies_the_replayed_snapshot` (Sol's trace: Deliver admitted, answer lost, snapshot of I at c held while pending, crash; the resend recovers the acceptance by key, c is replayed and classified as the relay)
- `message_crash_after_the_answer_before_its_ledger_write_resends_by_key`
- `message_crash_after_the_ledger_write_before_acknowledge_classifies_on_replay`
- `message_crash_after_an_events_effect_and_cursor_write_replays_nothing_twice`
- `message_crash_with_an_archived_held_behind_its_span_retires_the_entry_after_the_span` (`Archived(I)` waits behind a held snapshot of I; on replay the snapshot is the relay, then the entry retires)
- `message_crash_between_an_archived_and_its_retirement_write_retires_once_on_replay`
- `message_crash_with_a_reused_id_held_classifies_it_as_the_flows_own` (its relay of I archived, the flow's own request draws I; that event held at the crash)
- `message_crash_with_its_own_relay_reusing_an_id_gives_each_span_its_entry` (a second relay accepted with I before the stream passes the first's `Archived(I)`)
- `message_selects_the_ledger_entry_whose_span_holds_the_snapshot` (an old own send of I, its `Archived(I)`, then Message's relay accepted with I; its pending key and ledger entry both present before replay reaches the old send: the old send is the flow's own, the relay's snapshots are the relay)
- `message_crash_with_two_relay_generations_of_one_id_pending_classifies_each_by_its_span` (two ledger entries of I, an `Archived(I)` between them, the crash before replay reaches the first)
- `message_classifies_on_a_quiet_stream_whose_last_event_is_the_acceptance` (the stream ends at acceptance cursor a; held snapshots classify once a is read, with no later event)
- `message_crash_repeats_an_outside_effect_named_by_store_identity_and_cursor` (the crash between the outside effect and the write)

Upgrade (item 7)
- `upgrade_mints_ids_for_held_requests_only`
- `upgrade_archives_delivered_failed_and_withdrawn_requests_without_ids`
- `upgrade_archives_a_delivered_unanswered_order`
- `upgrade_holds_unended_requests_unfinished_attempts_open_tasks_and_reply_inputs`
- `upgrade_moves_archived_rows_into_delivery_before_ids_unchanged`
- `upgrade_writes_one_id_in_every_row_of_a_held_delivery`
- `upgrade_turns_every_old_answer_historical`
- `upgrade_maps_ambiguous_and_no_open_task_to_unresolved`
- `upgrade_maps_send_failure_and_send_receipt_of_held_requests`
- `upgrade_turns_archived_send_calls_archived`
- `upgrade_fails_closed_on_an_undecodable_row`
- `upgrade_fails_closed_on_an_orphan_reference` (one case per referring family)
- `upgrade_fails_closed_on_a_queue_entry_whose_delivery_ended`
- `upgrade_fails_closed_when_held_requests_exceed_the_space_or_draws_exhaust`
- `upgrade_failure_leaves_the_store_byte_identical`
- `upgrade_rerun_changes_nothing` (constraint d)
- `upgrade_draws_a_store_identity`
- `upgrade_keeps_legacy_evidence_as_it_is`
- `upgraded_uncertain_attempt_settles_by_its_stored_digest`
- `result_for_order_delivered_before_ids_unresolved` (blocker h)
- `done_for_task_closed_before_upgrade_unresolved` (blocker h)
- `upgrade_clears_heartbeat_outstanding_naming_a_moved_delivery`
- `upgrade_keeps_heartbeat_outstanding_naming_a_held_delivery`
- `upgrade_keeps_purpose_rows_and_each_recipients_sent_count`
- `upgrade_keeps_completed_reply_bindings_and_they_owe_nothing`
- `upgrade_leaves_no_resolved_reference_naming_a_moved_delivery` (walks the step 1 list less purposes and completed bindings)
- `upgrade_fails_closed_on_a_reference_left_naming_no_current_row`
- `upgraded_store_restarts_and_serves` (witness: a 0.53.2 store with a delivered heartbeat Notice as `outstanding`, delivered and held Orders, an open Task, purposes, an open and a completed simplified-reply binding; upgrade, stop, start; then a heartbeat tick admits a new heartbeat Notice to that recipient, sent counts are as before the upgrade, a Send, a Result and a Done by id, an ArchiveRequest and a cursor observation each succeed, and no read by LogicalDeliveryId fails)
- `upgrade_closes_a_held_task_answered_by_an_old_done`
- `upgrade_closes_a_held_order_with_an_unfinished_attempt_answered_by_an_old_result` (a Result by its id is Unresolved; the attempt settles by its receipt, never Read)
- `upgrade_closes_a_held_uncertain_order_answered_before_ids` (a Result by its id is Unresolved; it stays Uncertain until resolved)
- `upgrade_closes_the_held_input_of_a_completed_reply`
- `upgrade_leaves_an_unanswered_held_order_and_an_open_task_open`
- `simplified_reply_to_an_input_closed_before_ids_is_historical_and_completes` (its own id; names no request; the input's closure unchanged)
- `simplified_reply_to_an_open_upgraded_input_answers_by_its_id`

Upgrade, delivery order (R6; written against the accepted 0.53.2 frozen shapes, which are not yet accepted, so they run once 0.53.2 is accepted)
- `upgrade_gives_one_old_result_to_the_earlier_delivered_of_two_identical_held_orders` (the later stays Open with its new id; a Result by that id is admitted)
- `upgrade_delivery_order_is_the_first_delivered_event_cursor` (A admitted before B, B Delivered first: B closes; neither admission nor current cursor decides)
- `upgrade_orders_with_no_delivered_event_come_last_by_admission_cursor`
- `upgrade_assigns_no_order_admitted_after_its_answer`
- `upgrade_assigns_answers_in_admission_order_one_order_each` (three identical Orders, two answers: the two earliest delivered close)
- `upgrade_counts_a_moved_identical_order_in_delivery_order` (the moved Order delivered first takes the answer; the held one stays Open)
- `upgrade_ignores_a_legacy_evidence_result_for_assignment`
- `upgrade_with_identical_held_orders_never_fails_closed` (R6)
- `upgrade_reports_every_group_decided_by_delivery_order_with_both_ids`
- `upgrade_reports_no_group_of_one_order`
- `upgrade_assignment_is_identical_on_two_copies_of_a_store` (scripted id source: same closures, same report rows)
- `upgrade_assignment_rows_survive_restart_and_are_never_retracted`
- `assignment_notice_tells_each_sender_once` (through the announcement pass; retried and bounded as a task announcement)
- `assignment_notice_reads_ids_from_bindings_and_shows_archived_orders_archived`
- `assignment_row_with_no_held_order_left_closed`

Answers and delivery
- `send_accepted_names_request_id`
- `direct_sent_carries_request_id_alone` (ruling 6)
- `direct_not_sent_after_admission_names_request_id`
- `uncertain_answer_names_request_id_not_stale_cursor`
- `refusal_before_admission_is_unadmitted_without_id`
- `failure_after_admission_is_admitted_with_id`
- `request_id_plain_in_every_answer_snapshot_and_queue_entry`
- `identical_orders_get_distinct_ids`
- `delivered_order_carries_its_id_first` (exact pane text)
- `delivered_question_carries_its_id_first`
- `delivered_task_carries_id_minutes_words`
- `delivered_result_names_the_answered_id`
- `delivered_psyche_and_psyches_carry_an_id` (ruling 2)
- `reminder_carries_task_id_and_words` (ruling 4)
- `last_reminder_failure_stays_a_notice`
- `historical_answer_delivers_as_prior`
- `composer_reads_back_delivered_input`
- `result_by_id_admits_for_open_order`
- `result_by_id_admits_for_question` (ruling 3)
- `result_naming_psyche_unresolved` (ruling 2)
- `result_naming_task_or_notice_or_reminder_unresolved`
- `done_by_id_closes_task_and_reminder`
- `done_naming_order_or_question_unresolved` (ruling 3)
- `done_for_closed_task_unresolved`
- `result_unknown_id_unresolved`
- `result_naming_an_archived_id_unresolved` (R2)
- `result_naming_a_reused_id_resolves_to_its_current_request` (R2)
- `reused_id_duplicate_answer_from_the_same_parties_lands_on_the_new_request` (R2: the accepted risk, witnessed, not hidden)
- `result_from_stranger_holding_the_id_unresolved` (constraint a)
- `result_to_other_than_order_sender_unresolved` (constraint a)
- `answer_refusals_from_steps_three_to_eight_read_alike` (constraint a)
- `result_before_order_delivered_unresolved`
- `second_result_for_order_unresolved`
- `answer_has_its_own_id_distinct_from_the_id_it_answers` (constraint b)
- `answer_keeps_both_ids_across_restart` (constraint b)
- `answer_pane_shows_only_the_answered_id` (constraint b)
- `result_naming_an_answers_own_id_unresolved` (constraint b)
- `deliver_result_resolves_with_lock_sender`
- `simplified_reply_answers_input_id`
- `tool_result_resolves_by_id`
- `tool_result_without_request_malformed`
- `answer_sets_the_binding_closure_to_its_logical_id`
- `closure_survives_restart`

Uncertain to Read (blocker i, R3)
- `result_for_uncertain_order_from_its_recipient_marks_it_read`
- `result_for_uncertain_order_from_stranger_leaves_it_uncertain`
- `done_for_uncertain_task_from_its_recipient_closes_it_and_marks_it_read`
- `uncertain_to_read_settles_its_attempt_by_the_answer` (phase Read, answer by logical id, no resolver, no receipt)
- `uncertain_to_read_takes_a_queued_head_out_of_the_queue`
- `uncertain_to_read_settles_a_parked_request`
- `uncertain_to_read_without_one_unfinished_attempt_refused_store_and_writes_nothing`
- `read_attempt_is_not_listed_and_not_recovered`
- `read_keeps_a_late_receipt_apart_from_its_answer_and_stays_read`
- `read_refuses_a_different_late_receipt`
- `read_ignores_a_stale_absent`
- `read_ignores_uncertain_undecided_and_park`
- `resolve_queue_delivery_on_read_is_already_read` (both outcomes; nothing written)
- `read_is_never_retried_requeued_or_seeded`
- `withdraw_of_a_read_request_is_not_queued`
- `read_survives_restart_without_reconciliation`

Receipts (R3)
- `visible_delivered_state_omits_native_receipt`
- `resolve_queue_delivery_rejections_carry_no_receipt`
- `debug_delivery_shows_receipt_and_read_by_apart`
- `debug_delivery_unknown_or_archived_id_is_unknown_request`
- `ordinary_socket_cannot_debug_delivery`

Task announcement (ruling 5, blocker j)
- `upgrade_writes_pending_rows_per_recipient_and_part`
- `upgrade_rows_skip_queued_and_closed_tasks`
- `announcement_parts_fit_the_rendered_budget`
- `announcement_cuts_an_overlong_line`
- `announcement_admission_and_row_commit_together`
- `announcement_follows_its_notice_to_delivered`
- `announcement_failed_or_withdrawn_notice_retried_with_a_new_id`
- `announcement_tries_bounded_then_failed` (zero is AnnouncementTriesRefused)
- `announcement_uncertain_notice_never_resent`
- `announcement_refused_before_admission_stays_pending_with_its_refusal` (no held metaflow; space full; draws collided)
- `announcement_refusal_before_admission_is_not_a_try`
- `announcement_with_no_open_task_closed`
- `announcement_sent_once_across_restart`
- `announcement_repaired_after_a_crash_between_notice_and_row`
- `announcement_pass_tries_each_pending_row_at_most_once`
- `announcement_space_full_retried_after_an_archive_frees_an_id` (every part Pending; one archive; the next pass admits)
- `announcement_draws_collided_retried_at_the_next_admission` (scripted source)
- `announcement_draws_collided_retried_after_an_archive` (scripted source)
- `announcement_unheld_recipient_retried_when_its_metaflow_is_added`
- `announcement_pending_row_untried_without_a_triggering_commit` (no timer)
- `announcement_admission_or_archive_runs_no_pass_without_a_pending_row`
- `announcement_pass_own_commits_trigger_no_pass`
- `announcement_triggers_during_a_pass_make_one_more_pass`
- `announcement_pending_row_retried_at_start_after_a_lost_trigger`

Store replacement (R1)
- `configure_counters_carries_no_request_ids`
- `replacement_store_holds_no_binding`
- `replacement_store_resolves_old_id_unresolved`
- `replacement_store_has_a_new_store_identity`

CLI
- `cli_parses_result_by_request_id`
- `cli_prints_sent_with_request_id`

## A fact from the 0.53.0 store

The retired 0.53.0 store (export at `/tmp/e75baa-cutover/0531-execution/0530-custody-export/`) held 2223 deliveries: 1672 Delivered, 2 Failed, 549 Uncertain and Parked. Of the 549, 471 were SeatNotResting. By the rule they were placed in the pane and count as delivered. A quarter of all deliveries ending Uncertain, most to a working seat, is evidence that a delivery to a working seat gets no receipt. Recorded as a fact for this design; no action in this revision.

## Open questions

Out of scope, by ruling: the Living versus Psyche renaming (constraint f), Withdraw
by id, and the send tool's Task and Done (R3).

### For the living (policy)

1. **The upgrade archives every finished request,** delivered unanswered Orders and
   Questions included, as neither their recipients nor their senders ever saw an id,
   so none waits for a sender's archive. Confirm.
2. **Receipts on the meta socket.** R3 is read strictly: `AlreadyDelivered` loses
   its receipt, so DebugDelivery is the only reply that carries one. Confirm.
3. **Announcement retries.** A Notice the owner withdrew is retried like one that
   failed, up to `AnnouncementTries` (default 3). Confirm both.
4. **Which requests wait for their sender.** R5 names the unanswered Order and the
   open Task. This revision holds every request until its sender archives it:
   Delivered, Failed, Withdrawn, and those nothing can answer (Notice, Psyche, Result,
   Done, Reminder) too, as Flow runs no pass. The cost is one archive per request
   sent. The alternative: a Failed, Withdrawn or unanswerable request frees its id
   when it ends, since only an id a flow can answer by goes stale. Which?
These are choices awaiting the living, not approvals.

### For the implementer

1. **Attempting.** An answer to a request still Attempting is Unresolved (step 7).
   A recipient that answers before the receipt arrives retries. Confirm.
2. **Simplified reply to a non-answerable input.** What `deliver_simplified_reply`
   does on a Psyche, Notice or Reminder input today, and what ruling 2 makes it do.
   Not read.
3. **Frozen shapes** were read at 0.53.1; confirm 0.53.2 leaves them.
4. **Gates.** Each writer of a row that holds a request from archive (reminder,
   simplified-reply binding, announcement row, DeliverCall) holds the dispatch
   gate or the minting gate. Confirm each.
5. **Call holds.** Each admitting path (Send, send tool, Deliver) registers its
   hold before admission and releases it after its answer is written. Confirm
   none is missed.
6. **The `RequestIdDraws` and `AnnouncementTries` seeds** and their place in the
   configuration snapshot, following DefaultMinutes.
7. **Keep and Drop.** R5 asks for the archive input to go as Keep and Drop go;
   they are not in the Flow wire read here, so `ArchiveRequest` follows Send's
   process identification. Confirm the form against theirs.

### Left for judgment

1. **Item 3's wording.** "Its id stays bound until Message acknowledges or the
   request archives" is read with item 1's eligibility: an unacknowledged Deliver
   keeps its request from archive, so acknowledgement always comes first.
2. **A Message that lost its outbox** never acknowledges its keys, so their
   requests stay held for good, and the sender's ArchiveRequest is refused `NotYet`.
   Should the owner be able to release a DeliverCall?
3. **Unanswered Delivers across a store change.** Message holds outbox entries
   with no answer when the StoreIdentity changes. Should it resend them to the new
   store or report them lost? That is Message's design.
4. **History reading.** The upgrade's `PriorDelivery` rows and archived current
   rows are read by no query here, and ReadSendOutcomes shows old outcomes as
   history. Is a history query wanted?
5. **Closing identical held Orders: ruled (R6), closed.** The answer goes to the
   earlier Order by delivery order, the later stays open with its new id, and every
   such decision is reported with both ids (Upgrade, step 6; Assignment report).
   Its reading beyond the ruled case is ruled (R6, extended).
