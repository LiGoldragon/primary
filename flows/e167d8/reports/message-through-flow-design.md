# Message through Flow: target shape

Design subflow of e167d8, 2026-09-25. Target end-shape, no compatibility paths.
Forks for the living are marked **F1–F9** (section 7) with a recommendation.
Nothing here is built; witnessed state is in Sources.

## 1. The split

**Flow Nexus is the only pane writer.** It owns:
- the route (FlowId → Herdr session, pane, terminal);
- the **pane lease**: an internal per-pane exclusive hold spanning a whole key
  sequence (Esc, Esc, prompt, Enter), a Start's first prompt, a Command, and a
  Stop/Replace close. No two writes interleave. The lease is never handed out on
  the wire, so no client can hold a pane;
- **harness knowledge**: keymaps, tier → Herdr operations, command grammar;
- the **body refusal**, enforced at the writer: the last gate, and the only one
  that knows the recipient's harness;
- textualizing the letter. A pane is a text boundary like a CLI; Flow renders the
  typed letter, so the first byte in a pane is always a datom head (F6);
- agent-state observation from Herdr `events.subscribe`, offered as `Observe.Agent`.

**Message Nexus owns everything durable**: the record, Priority, the sender
(stamped from the peer, never the payload), the ledger and receipts (grades kept
separate), Soft parking until Flow reports the recipient idle, retries, and the
recipient's Read acknowledgement. Message never runs `herdr`; it never resolves
then writes (today's race in `nexus_delivery.rs`). It hands Flow a typed
`Deliver` addressed by FlowId, and Flow resolves the route under the lease.

**Split changed from the brief:** the refusal lives in Flow, not Message. In
Message, any second writer or a Flow client bypassing Message would go around it.
Message still reports refusals at submit time by calling Flow's `Vet` (the same
check as Deliver, nothing typed).

**messenger-clj** stops writing panes, then is retired. It keeps no registry:
Flow holds identity, which dissolves open fault 5 ("Start does not register in
messenger-clj").

## 2. Vocabulary changes

### signal-flow 5.1.0 → 6.0.0 (ordinary, breaking)
- **Removed:** `Send.SendRequest`, `Sent`, `SendRejected`, and types `SendRequest
  BareInput SendOutcome PresentationReceipt PresentationObservedUnixMilliseconds
  SendRejection`. The ordinary socket writes into no pane.
- **Added:** `ObserveSelection.[ Launch.LaunchRequestId Agent.FlowId ]`; reply
  `AgentObserved.AgentObservation`, on open and then per Herdr state change,
  ending when the flow stops. Types:
  `AgentObservation.{ FlowId AgentState }`,
  `AgentState.[ Idle Working Blocked Done Unknown Gone ]`,
  `CallerRefusal.[ CallerUnknown NotAuthorized.Caller PowerExceeded.Caller ]`.
- **Changed:** `StartRejection StopRejection RestartRejection ReplaceRejection`
  each gain `CallerRefused.CallerRefusal`.

### meta-signal-flow 6.0.4 → 7.0.0
Imports gain `Caller CallerResolutionRejection` from signal-flow.
Queries: `Deliver.DeliveryRequest Vet.DeliveryRequest Command.CommandRequest
ResolvePeer.ProcessIdentity`. Responses: `Delivered.Delivery
DeliveryRejected.DeliveryRejection Vetted.FlowId Commanded.CommandOutcome
CommandRejected.CommandRejection PeerResolved.Caller
PeerResolutionRejected.CallerResolutionRejection`. Types:
```
DeliveryId.String  CommandLine.String  ByteOffset.Integer  KeyName.String  CommandSigil.String
Sender.[ Flow.FlowId Owner ]
PsycheContext.String  PsycheVerbatim.String
Content.[ Text.String Psyche.{ PsycheContext PsycheVerbatim } ]
Letter.{ Sender Content }
Message.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]   ; Priority is the head on the datom
DeliveryRequest.{ DeliveryId FlowId Message }
InterruptWitness.[ NotRequested Observed Unobserved ]
DeliveryGrade.[ Transported Presented Uncertain ]
Delivery.{ DeliveryId FlowId InterruptWitness DeliveryGrade }
BodyRefusal.[ EmptyBody HarnessCommand.CommandLine ControlCharacter.ByteOffset ]
DeliveryRejection.[ UnknownFlow FlowStopped RouteUnavailable RecipientWorking RecipientBlocked
                    ComposerOccupied BodyRefused.BodyRefusal NotDelivered PersistenceRefused ]
HarnessCommand.[ Compact Interrupt ]
CommandRequest.{ FlowId HarnessCommand }
CommandGrade.[ Transported Observed Uncertain ]
CommandOutcome.{ FlowId HarnessCommand CommandGrade }
CommandRejection.[ UnknownFlow FlowStopped RouteUnavailable RecipientBlocked UnsupportedForHarness NotDelivered ]
InterruptKeys.Vector<KeyName>  SubmitKeys.Vector<KeyName>
HarnessProfile.{ HarnessKind Vector<CommandSigil> InterruptKeys SubmitKeys }
MetaAspects.Vector<FlowAspect>  MessageNexusPath.String
```
`Configuration` gains `Vector<HarnessProfile> MetaAspects MessageNexusPath`.
Keymaps are configuration because they differ between setups (Claude's two
Escapes come from vim mode). `Deliver` is idempotent on `DeliveryId`: a repeat
returns the stored `Delivery` and types nothing. A crash under the lease leaves
a Sema row `PaneLease.{ DeliveryId FlowId HerdrPaneId LeaseStep }`,
`LeaseStep.[ Acquired Interrupted Placed Submitted ]`; on restart that delivery
settles `Uncertain` and is never retried automatically.

### signal-message 5.0.0 → 6.0.0 (ordinary, breaking)
"A message is really just a message", so the vocabulary shrinks to that. Imports
from meta-signal-flow: `FlowId Content BodyRefusal DeliveryRejection InterruptWitness`.
- Queries: `Send.SendRequest`, `Withdraw.MessageId` (sender only, only while
  parked), `Acknowledge.MessageId` (recipient only; the sole source of Read),
  `QueryReceipts.MessageId`, `Observe.MessageId` (receipts on open, then each
  grade change).
- Responses: `Submitted.Submission SendRejected.SendRejection Withdrawn.MessageId
  Acknowledged.MessageId Receipts.Submission ReceiptObserved.Receipt
  MessageRejected.MessageRejection`.
```
MessageId.String
Priority.[ HardAbrupt MiddleAbrupt Soft ]
SendRequest.{ Vector<FlowId> Priority Content }
Grade.[ Submitted Parked Transported Presented Uncertain Read Withdrawn Refused.DeliveryRejection ]
Receipt.{ FlowId InterruptWitness Grade }
Submission.{ MessageId Vector<Receipt> }
SendRejection.[ SenderUnknown EmptyRecipients UnknownRecipient.FlowId BodyRefused.{ FlowId BodyRefusal } StoreRefused ]
MessageRejection.[ UnknownMessage NotSender NotRecipient NotParked StoreRefused ]
```
- **Retired** (Flow owns identity; `Observe.Agent` replaces idle-announce):
  `AssignAgentIdentity BindAgentEndpoint QueryAgentRegistry` and every `Agent*`
  type; `FlowDeliver FlowAnnounceIdle TypedPromptEnvelope`; `Deliver` with
  `ClusterMessage ClusterRelay PeerEnvelope` (the psyche relay becomes
  `Content.Psyche`); `SubmitStamped MessageOrigin` (sender comes from the peer);
  `MessageRequestUnimplemented`. Threads and Inbox: F9.
- Ledger (Sema, not wire):
  `MessageRecord.{ MessageId Sender Vector<FlowId> Priority Content StampedAt }`,
  `ReceiptRecord.{ MessageId FlowId InterruptWitness Grade StampedAt }`
  (append-only), `ParkRecord.{ MessageId FlowId }`.

### meta-signal-message 0.6.0 → 0.7.0
Queries: `Configure.MessageConfiguration` (replaces the unimplemented one, and is
applied), `Send.SendRequest` (stamped `Owner`, for the living's terminal),
`Redeliver.{ MessageId FlowId }` (the only way out of `Uncertain`). Replies:
`Configured ConfigureRejected Submitted SendRejected Redelivered.Receipt
RedeliverRejected.MessageRejection`.
`MessageConfiguration.{ OrdinarySocketPath MetaSocketPath FlowMetaSocketPath }`.

### The Message→Flow edge
Message is a client of Flow's **meta** socket (`Deliver Vet ResolvePeer`) and of
its ordinary socket (`Observe.Agent`). On `Send`, Message:
1. reads its peer's `SO_PEERCRED` and calls `ResolvePeer` → `Sender.Flow`
   (`SenderUnknown` on the ordinary socket if unresolved);
2. calls `Vet` per recipient; the first refusal fails the whole Send;
3. records `Submitted`;
4. calls `Deliver` per recipient.

On Soft, `RecipientWorking` or `ComposerOccupied` becomes `Parked`: Message holds
one `Observe.Agent` per parked recipient and re-Delivers on `Idle`/`Done`. The
lease settles races; Flow refuses again if the recipient is busy. No timers.

## 3. Tiers → Herdr operations (all under the lease)

Every tier requires: the route matches the snapshot (session, pane, terminal);
the agent is not `Blocked` (typing into a permission dialog could answer it:
`RecipientBlocked`); and the composer is blank (`ComposerOccupied`), so the
living's draft is never appended to or clobbered. The screen read is not atomic
with the typing; this is stated, not solved.

| Tier | Extra precondition | Claude | Codex |
|---|---|---|---|
| HardAbrupt | none | `send-keys esc esc` (profile), `agent prompt <text>`, `send-keys enter` | `send-keys esc`, `agent prompt <text>` (submits itself) |
| MiddleAbrupt | none | `agent prompt <text>`, taken at the next tool boundary | `agent prompt <text>`; queue vs steer while working is **unwitnessed**, stage 1 decides |
| Soft | `Idle`/`Done`, else `RecipientWorking` | `agent prompt <text>` | `agent prompt <text>` |

HardAbrupt reports `InterruptWitness` on its own (`Observed` = state seen leaving
`Working`). Per the Vision, the interrupt, text placement, submission and
consumption are four separate observations. `Transported` = Herdr accepted the
text; `Presented` = a reaction was seen on the exact pane; `Read` = only the
recipient's `Acknowledge`. Commands: `Interrupt` = the profile's interrupt keys;
`Compact` = `agent prompt /compact`, which only Flow may write.

## 4. Authority

| Operation | Socket, CLI | Gate |
|---|---|---|
| List ResolveRecipient LaunchStatus Observe ResolveCaller | ordinary `flow` | none (reads) |
| Restart | ordinary `flow` | caller is the target (as now) |
| Start | ordinary `flow` | caller resolved; PowerLevel ≤ caller's, else `PowerExceeded` |
| Stop, Replace | ordinary `flow` | target is the caller, the caller's origin-descendant, or caller aspect Psyche; else `NotAuthorized` |
| any of the above, caller unresolved | ordinary | `CallerUnknown`; use `flow-meta` |
| Deliver Vet Command(Compact, Interrupt) ResolvePeer Configure ConsumeReset RegisterFlow MetaBindExisting | meta `flow-meta` | peer is the configured Message Nexus executable, a non-flow process (owner), or a flow whose aspect is in `MetaAspects` (default `[ Psyche ]`) |
| Send Withdraw Acknowledge QueryReceipts Observe | ordinary `message` | sender must resolve |
| Send (as Owner) Redeliver Configure | meta `message-meta` | same peer rule as flow-meta |

Compact is at meta, per the living's lean; the Vision ("we shouldn't let the
models compact") argues for no ordinary path at all. Both sockets are `0600`
under one UID, and a double-forked process loses its pane ancestry and resolves
as "non-flow" = owner. These gates stop accidents and model mistakes, not an
adversary (F4).

## 5. The body refusal

Three layers: two make a command impossible by construction, the third reports
intent.
1. **Head first.** Flow renders the `Message` value, so pane text always begins
   `HardAbrupt.`, `MiddleAbrupt.` or `Soft.`. No harness reads a capital as a
   command; a `/compact` inside the Content lands as inert data.
2. **No keys in the text.** The Content may hold no C0 control except LF and TAB,
   no DEL, no C1. That excludes CR (submit), ESC (interrupt, or `ESC[201~`, which
   ends bracketed paste and lets the rest type raw), Ctrl-C and Ctrl-D:
   `ControlCharacter.<offset>`. The only submit boundaries are the Enters Flow
   sends, so no later line becomes its own submission. This assumes `agent
   prompt` uses bracketed paste; stage 1 must witness it.
3. **Intent.** Each `HarnessProfile` lists the harness's command sigils: Claude
   `[ / ! # ]`, Codex `[ / ! ]`. If the Content's first line (leading whitespace
   trimmed) is a sigil + identifier `[a-z][a-z0-9:_-]*` + space or end, Flow
   refuses `HarnessCommand.<line>`, telling the sender to use `Command`. `!` is
   refused whatever follows (shell mode). A path like `/home/li/x` passes (the
   identifier is followed by `/`). Sigils are configuration, updated through
   `flow-meta Configure` when a harness adds a mode.

`EmptyBody` is refused. There is no size limit: the living removed the
800-character split.

## 6. Datom examples

```
; meta-signal-flow
flow-meta 'Deliver.{ m-7f3a2c 7d41e0 Soft.{ Flow.e167d8 Text.«Stage 1 is deployed; run the tier tests.» } }'
Delivered.{ m-7f3a2c 7d41e0 NotRequested Presented }
flow-meta 'Deliver.{ m-81b0e4 7d41e0 HardAbrupt.{ Owner Text.«Stop the ouranos build now.» } }'
Delivered.{ m-81b0e4 7d41e0 Observed Transported }
flow-meta 'Deliver.{ m-90c1aa 7d41e0 MiddleAbrupt.{ Flow.88475f Psyche.{ «on build hosts» «Prometheus should be doing the builds.» } } }'
DeliveryRejected.RecipientBlocked
flow-meta 'Vet.{ m-a2d913 7d41e0 Soft.{ Flow.e167d8 Text./compact } }'
DeliveryRejected.BodyRefused.HarnessCommand./compact
DeliveryRejected.BodyRefused.ControlCharacter.14
Vetted.7d41e0
flow-meta 'Command.{ 7d41e0 Compact }'
Commanded.{ 7d41e0 Compact Transported }
CommandRejected.UnsupportedForHarness
flow-meta 'ResolvePeer.{ 48211 1001 «8841220 s» }'
PeerResolved.{ e167d8 Psyche High claude-opus-5-5 }
; what lands in the recipient's prompt
Soft.{ Flow.e167d8 Text.«Stage 1 is deployed; run the tier tests.» }
; signal-flow
flow 'Observe.Agent.7d41e0'
AgentObserved.{ 7d41e0 Idle }
flow 'Stop.7d41e0'
StopRejected.CallerRefused.NotAuthorized.{ da88cf Field Medium gpt-5.5 }
StartRejected.CallerRefused.CallerUnknown
; signal-message and meta-signal-message
message 'Send.{ [ 7d41e0 ] Soft Text.«Stage 1 is deployed; run the tier tests.» }'
Submitted.{ m-7f3a2c [ { 7d41e0 NotRequested Parked } ] }
message 'Send.{ [ 7d41e0 ] MiddleAbrupt Text./compact }'
SendRejected.BodyRefused.{ 7d41e0 HarnessCommand./compact }
message 'Acknowledge.m-7f3a2c'
Acknowledged.m-7f3a2c
Receipts.{ m-7f3a2c [ { 7d41e0 NotRequested Read } ] }
ReceiptObserved.{ 7d41e0 NotRequested Refused.RecipientWorking }
MessageRejected.NotParked
message-meta 'Redeliver.{ m-81b0e4 7d41e0 }'
Redelivered.{ 7d41e0 Observed Presented }
; Sema records
MessageRecord.{ m-7f3a2c Flow.e167d8 [ 7d41e0 ] Soft Text.«Stage 1 is deployed; run the tier tests.» 1790380000000000000 }
ReceiptRecord.{ m-7f3a2c 7d41e0 NotRequested Parked 1790380000100000000 }
PaneLease.{ m-81b0e4 7d41e0 w3-p2 Interrupted }
```
Each example must pass a round-trip test in its contract crate before its type is
final.

## 7. Forks for the living

- **F1 Raw input.** (a) Drop `BareInput` everywhere, or (b) keep a meta-only
  `Type.BareInput` as an owner escape hatch. **Recommend (a):** the newest words
  are "no arbitrary typing"; the owner still has `herdr`; "use it raw" was a
  bridge until Message worked.
- **F2 Edge socket.** (a) Message is a client of Flow's meta socket, or (b) Flow
  opens a third delivery socket for Message only. **Recommend (a),** the
  living's words; (b) only adds least privilege once UIDs differ (F4).
- **F3 Which flows reach meta.** (a) Aspect Psyche only, (b) none, (c) any.
  **Recommend (a):** Psyche seats deploy and manage flows.
- **F4 Same-UID boundary.** (a) Accept accident-grade gating now, or (b) run
  agents as a separate Unix user so meta sockets are a real boundary (an OS
  change). **Recommend (a)** now, with (b) as the chartered follow-up.
- **F5 Compact.** (a) Keep it as a meta Command, or (b) omit it ("no compaction;
  re-bootstrap"). **Recommend (a):** the owner decides each time; flows cannot.
- **F6 Who textualizes the letter.** (a) Flow renders the typed `Message` (the
  Flow Nexus enables `datom` for that one type, exception noted at the site), or
  (b) Message sends text and Flow only checks it. **Recommend (a):** only (a)
  guarantees the head comes first.
- **F7 Ordinary gating.** (a) The section 4 table, or (b) ungated.
  **Recommend (a),** landed as its own stage (S4).
- **F8 Owner's sender name.** `Owner`, `Living` or `Psyche`. **Recommend
  `Owner`:** it names the authority, and a Psyche flow is a different thing.
- **F9 Threads and Inbox.** (a) Retire them with the registry and relay in
  signal-message 6.0.0, or (b) keep them. **Recommend (a):** neither fits "a
  message is just a message", and neither is on the live path.

## 8. Migration

Nix builds and tests run on Prometheus. Recipients are disposable only.

- **S1: Flow 0.13.0** (signal-flow 6.0.0, meta-signal-flow 7.0.0).
  - Lands: lease, harness profiles, refusal, `Deliver Vet Command ResolvePeer
    Observe.Agent`; ordinary Send removed.
  - Deploys first. Message 0.12 does not use Flow Send, so nothing live breaks;
    the living's raw use becomes `flow-meta 'Deliver…'`.
  - Tests (disposable Flow Nexus with its own sockets and store, disposable Herdr
    session, fixture Claude and Codex panes, unique markers): each tier × harness
    observed target-side, with the interrupt witnessed separately; two concurrent
    Delivers to one pane never interleave; refusals for `/compact`, `!ls`, ESC,
    an embedded `ESC[201~`, CR and empty; a path line and `/compact` after an LF
    are accepted; blocked pane; occupied composer; a crash under the lease settles
    `Uncertain` with no retry; bracketed paste witnessed; Codex MiddleAbrupt
    witnessed.
- **S2: Message 0.14.0** (signal-message 6.0.0, meta-signal-message 0.7.0).
  - Lands: `nexus_delivery.rs`, the relay's herdr calls and the flow-delivery park
    are deleted; delivery over the Flow meta edge; ledger; Priority; Soft parking
    via `Observe.Agent`.
  - Deploys through the CriomOS-home pin with the store moved aside (new record
    kinds).
  - Tests (disposable Message + Flow + Herdr): Send; Vet refusal at submit;
    Parked → Transported on idle; Acknowledge → Read; Withdraw; Redeliver after
    an injected Uncertain; a static check script `message-cannot-invoke-herdr`
    next to the existing ones.
- **S3: messenger-clj.**
  - `hm-send`/`hm-send-abrupt` become one-line `message` CLI calls; `hm-list`
    becomes `flow 'List.{}'`; `hm-register rebind move retire` are deleted
    (identity lives in Flow Start and MetaBindExisting); then the shims and the
    `compensation-messenger-clj` skill are retired through Curriculum.
  - Tests: an `hm-send` to a disposable seat shows up in the Message ledger; a
    grep for `send-keys` and `agent prompt` in messenger-clj finds nothing.
- **S4: ordinary Flow gating** (F7).
  - Lands after every seat uses `flow-meta` or Message for what it does raw today,
    so no live seat is stranded overnight.
  - Test: a disposable caller flow Stops a stranger, itself and a descendant.

## Sources
- `/git/github.com/LiGoldragon/{signal-flow,meta-signal-flow,signal-message,meta-signal-message}` origin/main `ethos/signal.ethos` (74a47ed, fbfe897, 7f2fc2d, 87a54b0).
- `flow` origin/main 34aaf78: `DESIGN.md` (ResolveCaller via SO_PEERCRED and pane env; sockets 0600, one UID), `crates/flow-nexus/src/herdr.rs` (Send → `agent prompt`).
- `message` origin/main 9330640 (0.13.0): `src/nexus_delivery.rs` (resolve then herdr, blank-composer guard), `src/flow_delivery.rs` (park, drain on idle).
- `messenger-clj` 7474199: `src/messenger_clj/core.clj` `abrupt-keys` (codex esc; claude esc esc + enter).
- herdr 0.8.2 help: `agent prompt|send-keys|wait`, `api schema` (`events.subscribe`).
- Vision/messaging.md; flows/108ab0/vision/operational-{messagePriorityTiers,abruptPerHarness,messageAsDatomInPrompt}.md; flows/88475f/vision/{message,flow}.md; flows/6cc91b/vision/flowLifecycle.md.
- flows/e167d8/log.md (witnessed Flow and Message state, fault 5).
