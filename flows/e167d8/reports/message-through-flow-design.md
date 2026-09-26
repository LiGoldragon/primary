# Message through Flow: target shape

Design subflow of e167d8, 2026-09-25. Target end-shape, no compatibility paths.
Forks for the living are marked **FORK** with options and a recommendation.
Witnessed state is summarized in the Sources section. Nothing here is built.

## 1. The split

**Flow Nexus is the only thing that writes into a pane.** It owns:
- the route (FlowId, then Herdr session, pane and terminal),
- the **pane lease**: an internal, per-pane exclusive hold that covers a whole
  key sequence (Esc, Esc, prompt, Enter) as well as the first prompt of a Start,
  a Command, and the close done by Stop or Replace. No two writes interleave. A
  lease is not handed out on the wire, so no client can hold a pane,
- the **harness knowledge**: keymaps, how each tier becomes Herdr operations,
  and the command grammar,
- the **body refusal**. It is enforced at the writer, because the writer is the
  last gate and is the one that knows the recipient's harness,
- textualizing the letter: a pane is a text boundary, as a CLI is. Flow renders
  the typed letter itself, so the first byte in the pane is always a datom head
  (see FORK F6),
- agent-state observation: a Herdr `events.subscribe` feed, offered to others as
  `Observe.Agent`.

**Message Nexus owns everything durable about a message.** It owns:
- the message record, its Priority, and the sender, which it stamps from the
  peer and never takes from the payload,
- the ledger and the receipts, with each grade kept separate,
- Soft parking: a letter waits until Flow's agent-state subscription says the
  recipient is idle,
- retries, and the recipient's Read acknowledgement.

Message never runs `herdr`. It does not resolve and then write, which is the race
in today's `nexus_delivery.rs`. It hands Flow a typed `Deliver` addressed by
FlowId, and Flow resolves the route under the lease.

**Why the refusal is not in Message, as the brief proposed.** If Message owned
it, a second writer, or a Flow client that bypasses Message, would go around it.
Message still reports a refused body at submit time: it asks Flow's `Vet`, the
same check as Deliver with no typing, when the Send arrives.

**messenger-clj** stops writing panes and is then retired: it no longer delivers,
and it keeps no registry. Flow already holds the registry, which also closes open
fault 5 ("Start does not register in messenger-clj").

## 2. Vocabulary changes

### signal-flow 5.1.0 → 6.0.0 (ordinary, breaking)
- **Removed:** `Send.SendRequest`, `Sent`, `SendRejected`, and the types
  `SendRequest`, `BareInput`, `SendOutcome`, `PresentationReceipt`,
  `PresentationObservedUnixMilliseconds` and `SendRejection`. The ordinary
  socket no longer writes into a pane.
- **Added:** `Observe` gains a selection, giving
  `ObserveSelection.[ Launch.LaunchRequestId Agent.FlowId ]`. The reply
  `AgentObserved.AgentObservation` is sent once on open and then once per Herdr
  state change. It ends when the flow stops.
- **Added types:**
  - `AgentObservation.{ FlowId AgentState }`
  - `AgentState.[ Idle Working Blocked Done Unknown Gone ]`
  - `CallerRefusal.[ CallerUnknown NotAuthorized.Caller PowerExceeded.Caller ]`
- **Changed:** `StartRejection`, `StopRejection`, `RestartRejection` and
  `ReplaceRejection` each gain the variant `CallerRefused.CallerRefusal`.

### meta-signal-flow 6.0.4 → 7.0.0
Imports gain `Caller CallerResolutionRejection ProcessIdentity` from signal-flow.

New queries:
- `Deliver.DeliveryRequest`
- `Vet.DeliveryRequest`
- `Command.CommandRequest`
- `ResolvePeer.ProcessIdentity`

New responses:
- `Delivered.Delivery`
- `DeliveryRejected.DeliveryRejection`
- `Vetted.FlowId`
- `Commanded.CommandOutcome`
- `CommandRejected.CommandRejection`
- `PeerResolved.Caller`
- `PeerResolutionRejected.CallerResolutionRejection`

New types:
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
HarnessProfile.{ HarnessKind Vector<CommandSigil> Vector<KeyName> Vector<KeyName> }  ; sigils, interrupt keys, submit-after-interrupt keys
MetaAspects.Vector<FlowAspect>
MessageNexusPath.String
```

`Configuration` gains `Vector<HarnessProfile> MetaAspects MessageNexusPath`.
The keymaps live in configuration rather than in code because they vary between
setups: Claude takes two Escapes only because its editor is in vim mode.

`Deliver` is idempotent on `DeliveryId`. If the same id is repeated, Flow answers
with the stored `Delivery` and types nothing. A crash while the lease is held
leaves a durable `PaneLease` row, a Sema record kept off the wire:
`PaneLease.{ DeliveryId FlowId HerdrPaneId LeaseStep }`, with
`LeaseStep.[ Acquired Interrupted Placed Submitted ]`. On restart that delivery
settles as `Uncertain` and is never retried automatically.

### signal-message 5.0.0 → 6.0.0 (ordinary, breaking)
A message is really just a message, so the vocabulary is cut to what that needs.

Imports from meta-signal-flow: `FlowId Content BodyRefusal DeliveryRejection InterruptWitness`.

Queries:
- `Send.SendRequest`
- `Withdraw.MessageId`: sender only, and only while parked
- `Acknowledge.MessageId`: recipient only, and it is the only source of Read
- `QueryReceipts.MessageId`
- `Observe.MessageId`: the receipts on open, then each grade change

Responses:
- `Submitted.Submission`
- `SendRejected.SendRejection`
- `Withdrawn.MessageId`
- `Acknowledged.MessageId`
- `Receipts.Submission`
- `ReceiptObserved.Receipt`
- `MessageRejected.MessageRejection`

Types:
```
MessageId.String
Priority.[ HardAbrupt MiddleAbrupt Soft ]
SendRequest.{ Vector<FlowId> Priority Content }
Grade.[ Submitted Parked Transported Presented Uncertain Read Withdrawn Refused.DeliveryRejection ]
Receipt.{ FlowId InterruptWitness Grade }
Submission.{ MessageId Vector<Receipt> }
SendRejection.[ SenderUnknown EmptyRecipients UnknownRecipient.FlowId
                BodyRefused.{ FlowId BodyRefusal } StoreRefused ]
MessageRejection.[ UnknownMessage NotSender NotRecipient NotParked StoreRefused ]
```

**Retired, because Flow owns identity and Flow's `Observe.Agent` replaces
idle-announce:**
- `AssignAgentIdentity`, `BindAgentEndpoint`, `QueryAgentRegistry` and every
  `Agent*` type,
- `FlowDeliver`, `FlowAnnounceIdle`, `TypedPromptEnvelope`,
- `Deliver.DeliveryRequest` with `ClusterMessage`, `ClusterRelay` and
  `PeerEnvelope`, whose psyche relay becomes `Content.Psyche`,
- `SubmitStamped` and `MessageOrigin`, since the sender is stamped from the peer,
- `MessageRequestUnimplemented`.

**FORK F9:** whether Threads and Inbox survive this cut. See section 7.

Ledger records (Sema, not wire):
- `MessageRecord.{ MessageId Sender Vector<FlowId> Priority Content StampedAt }`
- `ReceiptRecord.{ MessageId FlowId InterruptWitness Grade StampedAt }`, append-only
- `ParkRecord.{ MessageId FlowId }`

### meta-signal-message 0.6.0 → 0.7.0
Queries:
- `Configure.MessageConfiguration`: this replaces the unimplemented one and is
  actually applied
- `Send.SendRequest`: Owner-stamped, for the living's own terminal
- `Redeliver.{ MessageId FlowId }`: the only path out of `Uncertain`

Replies: `Configured`, `ConfigureRejected`, `Submitted`, `SendRejected`,
`Redelivered.Receipt`, `RedeliverRejected.MessageRejection`.

`MessageConfiguration.{ OrdinarySocketPath MetaSocketPath FlowMetaSocketPath }`

### The Message→Flow edge
- Message is a client of Flow's **meta** socket, and uses only
  `Deliver Vet ResolvePeer Observe(Agent)`. `Observe` is on the ordinary socket.
- On `Send`, Message:
  1. reads its peer's `SO_PEERCRED`, then calls `ResolvePeer` to get the `Caller`
     that becomes `Sender.Flow`, or `SenderUnknown` on the ordinary socket;
  2. calls `Vet` for each recipient, and the first refusal fails the whole Send;
  3. records the message as `Submitted`;
  4. calls `Deliver` for each recipient.
- A `RecipientWorking` or `ComposerOccupied` reply on Soft becomes `Parked`.
  Message holds one `Observe.Agent` subscription per parked recipient. On `Idle`
  or `Done` it calls `Deliver` again; the lease settles any race and Flow refuses
  again if the recipient is busy.
- Nothing is re-read on a timer.

## 3. How each tier becomes Herdr operations (all under the lease)

These preconditions apply to every tier:
- the route matches the snapshot (session, pane, terminal),
- the agent is not `Blocked`. Typing into a permission dialog could answer it,
  so the reply is `RecipientBlocked`,
- the composer is blank. Otherwise the reply is `ComposerOccupied`, so a draft
  the living is typing is never appended to or clobbered. The screen read is not
  atomic with the typing; this is stated, not solved.

| Tier | Extra precondition | Claude | Codex |
|---|---|---|---|
| HardAbrupt | none | `send-keys esc esc` (profile), `agent prompt <text>`, `send-keys enter` | `send-keys esc`, `agent prompt <text>` (submits itself) |
| MiddleAbrupt | none | `agent prompt <text>`; taken at the next tool boundary | `agent prompt <text>`; queue or steer while working is **unwitnessed**, and the stage-1 test decides |
| Soft | state `Idle` or `Done`, else `RecipientWorking` | `agent prompt <text>` | `agent prompt <text>` |

Each HardAbrupt delivery reports `InterruptWitness` on its own: `Observed` means
the state was seen to leave `Working`. The grades follow the Vision rule: an
interrupt, placing the text, submitting it, and the recipient consuming it are
four separate observations.
- `Transported`: Herdr accepted the text.
- `Presented`: a reaction was seen on the exact pane.
- `Read`: only the recipient's `Acknowledge` sets it.

A Command becomes these operations:
- `Interrupt`: the profile's interrupt keys.
- `Compact`: `agent prompt /compact`, which Flow is allowed to write because
  Flow wrote it.

## 4. Authority

| Operation | Socket, CLI | Gate |
|---|---|---|
| List, ResolveRecipient, LaunchStatus, Observe, ResolveCaller | ordinary, `flow` | none (reads) |
| Restart | ordinary, `flow` | caller is the target (existing) |
| Start | ordinary, `flow` | caller resolved; requested PowerLevel no higher than caller's, else `PowerExceeded` |
| Stop, Replace | ordinary, `flow` | caller is the target, an origin-descendant of it, or of aspect Psyche; else `NotAuthorized` |
| any of the above with an unknown caller | ordinary | `CallerUnknown`; use `flow-meta` |
| Deliver, Vet, Command (Compact, Interrupt), ResolvePeer, Configure, ConsumeReset, RegisterFlow, MetaBindExisting | meta, `flow-meta` | peer is the configured Message Nexus executable, or a non-flow process (owner), or a flow whose aspect is in `MetaAspects` (default `[ Psyche ]`) |
| Send, Withdraw, Acknowledge, QueryReceipts, Observe | ordinary, `message` | sender must resolve; Withdraw by sender only, Acknowledge by recipient only |
| Send (as Owner), Redeliver, Configure | meta, `message-meta` | the same peer rule as Flow meta |

Compact sits at meta, following the living's lean. The living's own words go
further ("we shouldn't let the models compact"), so no ordinary path exists.

Note: both sockets are `0600` under one UID. A process that double-forks loses
its pane ancestry and resolves as "non-flow", that is, as the owner. The gates
above therefore stop accidents and model mistakes, not an adversary (**FORK F4**).

## 5. The body refusal

The refusal has three layers. The first two make a command impossible by
construction. The third reports intent.
1. **Head first.** Flow renders the `Message` value itself, so the pane text
   always begins with `HardAbrupt.`, `MiddleAbrupt.` or `Soft.`. No harness reads
   a capital letter as a command, so `/compact` inside the Content lands as inert
   data.
2. **No keys inside the text.** The Content may not contain any C0 control
   character except LF and TAB, nor DEL or any C1 control. That rules out CR
   (a submit), ESC (an interrupt, or `ESC[201~`, which ends bracketed paste and
   would let the rest be typed raw), and Ctrl-C and Ctrl-D. The refusal is
   `ControlCharacter.<byte offset>`. The only submit boundaries are the Enter
   keys Flow sends itself, so a later line can never become a submission of its
   own. This holds only if `agent prompt` uses bracketed paste, and the stage-1
   test must witness that.
3. **Intent.** Each `HarnessProfile` carries that harness's command sigils:
   Claude `[ / ! # ]` and Codex `[ / ! ]`. If the Content's first line, with
   leading whitespace trimmed, is one of those sigils followed by an identifier
   `[a-z][a-z0-9:_-]*` and then a space or the end, Flow refuses it as
   `HarnessCommand.<that line>`, so the sender learns to use `Command`.
   - A line starting with `!` is refused whatever follows. It is shell mode.
   - A path such as `/home/li/x` is not refused, because the identifier is
     followed by `/`.
   - The sigil sets are configuration, updated through `flow-meta Configure`
     when a harness adds a mode.

`EmptyBody` is refused. There is no size limit ("a message is really just a
message"; the 800-character split was removed by the living).

## 6. Datom examples (one for each new record kind)

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
DeliveryRejected.BodyRefused.EmptyBody
Vetted.7d41e0
flow-meta 'Command.{ 7d41e0 Compact }'
Commanded.{ 7d41e0 Compact Transported }
CommandRejected.UnsupportedForHarness
flow-meta 'ResolvePeer.{ 48211 1001 «8841220 s» }'
PeerResolved.{ e167d8 Psyche High claude-opus-5-5 }
; what lands in the recipient's prompt (the Message value, textualized by Flow)
Soft.{ Flow.e167d8 Text.«Stage 1 is deployed; run the tier tests.» }
; signal-flow
flow 'Observe.Agent.7d41e0'
AgentObserved.{ 7d41e0 Working }
AgentObserved.{ 7d41e0 Idle }
flow 'Stop.7d41e0'
StopRejected.CallerRefused.NotAuthorized.{ da88cf Field Medium gpt-5.5 }
StartRejected.CallerRefused.CallerUnknown
; signal-message
message 'Send.{ [ 7d41e0 ] Soft Text.«Stage 1 is deployed; run the tier tests.» }'
Submitted.{ m-7f3a2c [ { 7d41e0 NotRequested Parked } ] }
message 'Send.{ [ 7d41e0 ] MiddleAbrupt Text./compact }'
SendRejected.BodyRefused.{ 7d41e0 HarnessCommand./compact }
message 'Acknowledge.m-7f3a2c'
Acknowledged.m-7f3a2c
message 'QueryReceipts.m-7f3a2c'
Receipts.{ m-7f3a2c [ { 7d41e0 NotRequested Read } ] }
ReceiptObserved.{ 7d41e0 NotRequested Refused.RecipientWorking }
MessageRejected.NotParked
; meta-signal-message
message-meta 'Redeliver.{ m-81b0e4 7d41e0 }'
Redelivered.{ 7d41e0 Observed Presented }
; Sema records
MessageRecord.{ m-7f3a2c Flow.e167d8 [ 7d41e0 ] Soft Text.«Stage 1 is deployed; run the tier tests.» 1790380000000000000 }
ReceiptRecord.{ m-7f3a2c 7d41e0 NotRequested Parked 1790380000100000000 }
PaneLease.{ m-81b0e4 7d41e0 w3-p2 Interrupted }
```

Every example must pass a round-trip test in its contract crate before its type
is final.

## 7. Forks for the living

- **F1, raw input.** Options: (a) drop `BareInput` everywhere, or (b) keep a
  meta-only `Type.BareInput` as an escape hatch for the owner. **Recommend (a).**
  The living's newest words are "no arbitrary typing", and the owner still has
  `herdr` directly. The earlier words "use it raw" were a bridge until Message
  worked.
- **F2, the edge socket.** Options: (a) Message is a client of Flow's meta socket,
  or (b) Flow opens a third "delivery" socket for Message only.
  **Recommend (a)**, the living's words. (b) only buys least privilege once the
  UIDs differ (F4).
- **F3, which flows may use meta.** Options: (a) aspect Psyche only, (b) none,
  or (c) any flow. **Recommend (a).** Psyche seats deploy and manage flows.
- **F4, the same-UID boundary.** Options: (a) accept that the gates stop
  accidents only, for now, or (b) run agents under a separate Unix user so the
  meta sockets are a real boundary (an OS change). **Recommend (a)** now, and
  (b) as the chartered follow-up.
- **F5, Compact.** Options: (a) keep it as a meta Command, or (b) omit it
  entirely, since the Vision says "no compaction; re-bootstrap".
  **Recommend (a).** The owner decides each time, and flows cannot reach it.
- **F6, who turns the letter into text.** Options: (a) Flow renders the typed
  `Message`; Flow Nexus enables `datom` for that one type, and the exception is
  noted at the site, or (b) Message hands Flow text and Flow only checks it.
  **Recommend (a).** Only (a) guarantees the head comes first.
- **F7, gating ordinary operations.** Options: (a) the table in section 4
  (self, descendant or Psyche for Stop and Replace; a power ceiling on Start), or
  (b) keep them ungated. **Recommend (a)**, landed as a stage of its own (S4).
- **F8, what an owner-sent letter is called.** Options: `Owner`, `Living` or
  `Psyche`. **Recommend `Owner`.** It names the authority, and a Psyche flow is
  a different thing.
- **F9, Threads and Inbox.** Options: (a) retire them with the registry and the
  relay in signal-message 6.0.0, or (b) keep them. **Recommend (a).** Neither is
  in the living's shape of a message, and neither is used on the live path.

## 8. Migration (Nix builds and tests on Prometheus; disposable recipients only)

- **S1: Flow 0.13.0** (signal-flow 6.0.0 and meta-signal-flow 7.0.0).
  - Lands: the lease, harness profiles, the refusal, Deliver, Vet, Command,
    ResolvePeer and Observe.Agent. Ordinary Send is removed.
  - Deploys first. Message 0.12 does not call Flow's Send, so nothing live
    breaks. The living's raw use moves to `flow-meta 'Deliver…'`.
  - Test on a disposable Flow Nexus (its own sockets and store) and a disposable
    Herdr session, with a fixture Claude pane and a fixture Codex pane, each
    marker unique:
    - each tier on each harness, observed on the target side: the transcript
      holds the marker, and the interrupt witness is taken on its own,
    - two concurrent Delivers to one pane never interleave (lease),
    - the refusal cases: `/compact`, `!ls`, `/compact` after an LF, an ESC byte,
      an embedded `ESC[201~`, a CR, an empty body, and a path line that must be
      accepted,
    - a blocked pane and an occupied composer,
    - a crash while the lease is held gives `Uncertain` and is not retried,
    - bracketed paste is witnessed,
    - Codex MiddleAbrupt behavior is witnessed.
- **S2: Message 0.14.0** (signal-message 6.0.0 and meta-signal-message 0.7.0).
  - Lands: `nexus_delivery.rs`, the relay's herdr calls and the flow-delivery
    park are deleted. Delivery goes over the Flow meta edge, with the ledger,
    Priority and Soft parking through Observe.Agent.
  - Deploys through the CriomOS-home pin, with the store moved aside, since the
    record kinds are new.
  - Tests:
    - the whole path, disposable Message, Flow and Herdr: Send, Vet refusal at
      submit, Parked then Transported on idle, Acknowledge gives Read, Withdraw,
      and Redeliver after an injected Uncertain,
    - a static check script, `message-cannot-invoke-herdr`, alongside the
      existing ones.
- **S3: messenger-clj.**
  - `hm-send` and `hm-send-abrupt` become one-line calls to the `message` CLI
    (Soft or MiddleAbrupt, and HardAbrupt).
  - `hm-list` becomes `flow 'List.{}'`.
  - `hm-register`, `rebind`, `move` and `retire` are deleted; Flow Start and
    MetaBindExisting hold identity.
  - Then the shims and the `compensation-messenger-clj` skill are retired
    through Curriculum.
  - Tests: an `hm-send` to a disposable seat arrives by way of the Message
    ledger; the grep for `send-keys` and `agent prompt` in messenger-clj finds
    nothing.
- **S4: gating ordinary Flow operations** (F7).
  - Lands after every seat uses `flow-meta` or Message for what it now does
    raw, so gating does not strand a live seat overnight.
  - Test: a disposable caller flow's Stop of a stranger flow, of itself and of
    its descendant.

## Sources
- `/git/github.com/LiGoldragon/{signal-flow,meta-signal-flow,signal-message,meta-signal-message}` origin/main `ethos/signal.ethos` (signal-flow 74a47ed, meta-signal-flow fbfe897, signal-message 7f2fc2d, meta-signal-message 87a54b0).
- `flow` origin/main 34aaf78: `DESIGN.md`, `crates/flow-nexus/src/herdr.rs` (Send prompt path).
- `message` origin/main 9330640: `src/nexus_delivery.rs` (resolve then herdr, blank-composer guard), `src/flow_delivery.rs` (park, drain on idle).
- `messenger-clj` 7474199: `src/messenger_clj/core.clj` `abrupt-keys` (codex esc; claude esc esc + enter).
- `herdr` 0.8.2 help: `agent prompt|send-keys|wait`, `api schema` (`events.subscribe`).
- Vision/messaging.md; flows/108ab0/vision/operational-{messagePriorityTiers,abruptPerHarness,messageAsDatomInPrompt}.md; flows/88475f/vision/message.md; flows/88475f/vision/flow.md; flows/6cc91b/vision/flowLifecycle.md (no compaction).
- flows/e167d8/log.md (witnessed Flow and Message state, fault 5).
