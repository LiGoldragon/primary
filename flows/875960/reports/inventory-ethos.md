# Inventory of ethos types: current Flow design, signal-flow, meta-signal-flow

Read-only inventory, 2026-10-11. Witnessed by reading the three sources; the declarations were extracted by a script that splits each section into its top-level declarations, collapses whitespace, and attaches the source comment. A source declares each type once; a declaration in place inside another (for example `State.[ Awake.FlowId Asleep Ended ]` inside `Metaflow`) stays inside its parent line and is not counted separately.

Sources:
- (A) `/home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md`, section 1 (lines 9 to 601), design prose; the code blocks are not a compiled file. Comments in (A) are the source's trailing comments.
- (B) `/git/github.com/LiGoldragon/signal-flow`, `git show origin/field/signal-aspect-store-e3ddf94ed9bb:ethos/signal.ethos`, after `git fetch origin`. Comments in (B) are the lines above each declaration.
- (C) `/git/github.com/LiGoldragon/meta-signal-flow`, `git show origin/field/meta-aspect-store-1a1258b9873b:ethos/signal.ethos`, after `git fetch origin`.
- Neither branch has `ethos/library.ethos`: `git ls-tree` of each lists only `ethos/signal.ethos`. Both import the Library types from `flow_ethos` and do not declare them.

Source defect found in (A): in the Signal flow-socket block and the Signal meta-socket block the response section is never closed. `Refused.[ ... Store.String ]` closes only Refused, and the next line is `[]`, which then reads as part of the response section. The extraction closed the response section before that `[]`; the counts below assume that reading.

## Counts

| Source and section | Count |
|---|---|
| A Library types | 22 |
| A Library trait (Encodable, in prose) | 1 |
| A Memory record types | 7 |
| A Signal flow: queries / responses | 14 / 16 |
| A Signal meta: queries / responses | 3 / 5 |
| A Message's forms (Send, Deliver) | 2 |
| B (signal-flow): queries / responses / types | 18 / 31 / 88 |
| C (meta-signal-flow): queries / responses / types | 11 / 23 / 58 |
| Total declarations, A / B / C | 70 / 137 / 92 |

Queries and responses are the variants of the generated `Query` and `Response` enums; types are the declarations in the types section (A: Library types section and Memory record section).

## (A) Current Flow design

### Library

Root comment: Flow's

Imports: `meta_signal_flow:[ CodexEndpoint HarnessProfile ]`

#### Types (22)
```
FlowId.String ; unideal now: a real id built on the hash bits that identify a flow
Topic:Name ; inline import of a core built-in: camelCase, checked where text enters
Blake3.Bytes<32> ; Encodable: hex
Layer.[ Primary Secondary Tertiary Quaternary ] ; decides the model
Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ] ; a module's kind
Source.{ Repository.String Hash.Blake3 Path } ; where a module's text lives: the containing source, hashed, relative
Path.String ; a path relative to a source
Reason.String ; why a store refuses
Key.{ Subaspect Topic } ; a module's key, written as the pair { Vision flow }
Said.{ Context.String Verbatim.String } ; his words, relayed where it was said the words whole
Request.[ Order.String Question.String Psyche.Said Psyches.Vector<Said> Result.String Notice.String ] ; reaches a flow wakes wakes wakes; the variant carries the type wakes a flow's answer: delivered awake, waits asleep wakes nothing
Aspect.[ Psyche Mind Field ] ; whose psyche it serves
Address.{ Aspect Topic Layer } ; names a metaflow, written short: { Psyche flow Primary }
Recipient.[ Address Up ] ; Up: same topic, one layer above the sender, in its aspect
Metaflow.{ Address State.[ Awake.FlowId Asleep Ended ] Past.Vector<FlowId> Queue.Vector<Request> } ; one per address its current flow a request wakes it the last few only, oldest first waiting, oldest first
Lock.{ Sender Address Until.Integer } ; one per metaflow, resolved address while held seconds since the epoch; lapses
Process.{ Pid.Integer Started.Integer } ; the calling process the kernel's start time of that pid, so a reused pid is told apart
Sender.Address
Start.{ OrdinarySocketPath.String MetaSocketPath.String StorePath.String } ; the one datom argument of the Nexus's start command
StoreRefusal.{ Path Reason } ; the store at StorePath is not Flow's own, or cannot be opened
StartRefusal.[ Store.StoreRefusal ] ; the start reply when it refuses
Nexus.{ SourceRoot.String StableCodex.CodexEndpoint NextCodex.CodexEndpoint HarnessProfiles.Vector<HarnessProfile> MetaAspects.Vector<Aspect> MessageNexusPath.String MessageNexusBinary.String Lease.Integer } ; the Nexus's own setup payload Message's ordinary socket store path of the Message Nexus binary
```

Trait declared in prose beside the Library (not inside the root block):
```
Encodable.[ encode.String decode:{ [ Textualizable ] [ Result<Self Error> ] } ] ; the bare run the run read
```

### Memory

Root comment: Flow's

Imports: `flow_ethos:[ FlowId Layer Key Source Process ] meta_signal_flow:[ HarnessKind ] signal_flow:[ Event ]`

#### Record types (7)
```
Flow.{ FlowId Session.String Process Events.Vector<Event> } ; one per run the harness's id the calling process's pid and start time learned at spawn or bind signal-flow's
Module.{ Key Source Checked.Boolean } ; the registry: one per key false until its first compose checks the hash
Model.{ Layer Harness.HarnessKind Native.String } ; one per layer how it is driven the model's name as the harness knows it
Metaflow.flow_ethos:Metaflow ; ethos-zero's form for a record naming a Library type
Lock.flow_ethos:Lock ; likewise
Nexus.flow_ethos:Nexus ; the Nexus payload stored once
Threshold.{ Layer Handover.Integer Refresh.Integer } ; one per layer
```

(A) also states in prose that Memory imports `signal_flow:[ Event ]`, that `Event` is `Started`, `ToolUsed.String`, `ContextMeasured.{ Tokens.Integer Window.Integer }`, `Stopped`, and that "In this build signal-flow gains ContextMeasured". `Event` itself is not declared in a code block of (A).

### Signal, the flow socket

Root comment: what Flow is asked

Imports: `flow_ethos:[ Address FlowId Request Lock Sender Recipient Process Key Metaflow ] signal_flow:[ Event ]`

#### Queries (14)
```
Launch.{ Address Modules.Vector<Key> Brief.String } ; a metaflow's first flow; the address written short a small paragraph
Wake.{ Address Request } ; a sleeping metaflow's next the waking request
Refresh.Address ; the next link
End.Address
Current.Address
Bind.{ Address Process } ; a running process becomes this metaflow's flow
Lock.{ Sender Recipient } ; Message asks; time bound
Identify.Process ; who is the caller
Deliver.{ Lock Request } ; under the lock sender in lock
Release.Lock
Report.{ FlowId Event } ; the hook's request
Observe.Agent.FlowId ; carries Herdr's agent state
Stop.FlowId ; reap, no successor
Metaflows
```

#### Responses (16)
```
Launched.FlowId
Refreshed.{ FlowId FlowId } ; the successor the predecessor
Ended
Current.[ Awake.FlowId Asleep Ended Unknown ]
Bound.FlowId ; the flow reserved
Locked.Lock ; carries the resolved Address
Identified.Address ; the caller's
Delivered ; placed in the awake flow
Queued ; asleep, or awake and busy: waits
Woken.FlowId ; asleep: woken; the queue drained with the first prompt
Released
Reported
Observed.Agent.[ Working Idle Done Absent ] ; Herdr's agent states as it reports them
Stopped
Listed.Vector<Metaflow>
Refused.[ Locked Held.Lock Awake.FlowId Asleep Lapsed Unknown.[ Address Lock FlowId Key ] NoLayer NotConfigured HashMismatch Ended.Address OffRoute NoneAbove NotMessage Unidentified.Process Taken.Address Store.String ] ; refresh under way lock held: also Refresh and End Launch of an awake metaflow: its current flow Refresh of a sleeper a granted lock that ran out each inner variant carries its type no such metaflow; a Sender or an Up target naming none never granted, or already consumed Report, Stop or Observe.Agent module missing from registry or Forget, or from Launch if module in Launch is missing no Model for the layer; at Launch, and at Lock or Deliver for an asleep recipient Launch before Configure.Nexus a module recorded unchecked fails its hash at its first compose Wake, Lock, Deliver, Refresh or End of an Ended metaflow at Lock: sender, recipient aspect, layer, topic off the vision-aspects routes Up above Primary Bind, Lock, Deliver or Release from not-bound peer (not Identify, which any local peer may ask) Identify: in no metaflow; Bind: a dead or reused process Bind: the old process lives the store failed; its own error text
```

### Signal, the meta socket

Root comment: the meta socket

Imports: `flow_ethos:[ Layer Key Source Path Nexus ] meta_signal_flow:[ CodexEndpoint HarnessKind HarnessProfile ]`

#### Queries (3)
```
Configure.[ Module.{ Key Source } Model.{ Layer Harness.HarnessKind Native.String } Threshold.{ Layer Handover.Integer Refresh.Integer } Nexus ] ; the registry: one per key the layer's model how it is driven the model's name as the harness knows it percent of window 20 40 the Library's: the Nexus's own setup
Forget.Key ; a module leaves
Configuration
```

#### Responses (5)
```
Configured
Forgotten
Configuration.{ Nexus Models.Vector<Model> Thresholds.Vector<Threshold> Modules.Vector<Module> } ; the runner values
Unconfigured ; no Nexus payload yet
Refused.[ NoSource.Path HashMismatch Conflict Unknown.Key Store.String ] ; Nexus payloads that disagree in one start Forget of an unknown key the store failed; its own error text unknown key
```

### Message's simple and extended forms

"Defined in Signal as types of their own, nothing omitted from either; shown here for the lock." The block is a bare list of two variants with no root.

#### Variants (2)
```
Send.{ Address Request } ; simple: what a flow writes
Deliver.{ Lock Request } ; extended: Message to Flow, under the sender in lock
```

## (B) signal-flow, branch field/signal-aspect-store-e3ddf94ed9bb, ethos/signal.ethos

Root: `Signal`. Imports: `flow_ethos:[ Aspect Address FlowId Request Lock Sender Process Metaflow Key Recipient Layer Topic Subaspect Source OrdinarySocketPath MetaSocketPath Start ModelName HarnessKind ]`

File header comment (verbatim, before the `Signal` root):
```
; Presentation names the living-directed output's book; it carries no body
; or sender. Transcript content ownership is deliberately not declared.
;
; QueueTurnEnd is a pre-end wakeup, not evidence that the turn completed.
; Stop may precede the final native record or repeat while a turn continues.
; TurnEndQueued acknowledges durable enqueue only and must return without
; waiting for the final transcript record. The Nexus verifies completion and
; deduplicates actual native (SessionId, TurnId) before any downstream work.
; A missing transcript path is None, never an invented empty path.
; No handler, hook or state subscription is implemented by this vocabulary.
;
; Flow ordinary Signal.
;
; Replace carries a StartRequest whose LaunchProfile names the replaced
; flow as its predecessor. The successor is launched; once it has
; Started, the predecessor is Stopped and taken out of receiving, and
; only then is the successor routable. Reaping belongs to the refresh
; event: no state holds both flows routable. Replaced carries the
; stopped predecessor's FlowId and the successor's Started.
; ReplaceRejection names why no replacement took place; after
; ReapRefused the successor is not routable.
;
; LaunchStatus answers a known LaunchRequestId with one LaunchInspected
; snapshot: its LaunchAttempt, its optional settled outcome, and the
; FlowNode actually recorded for the launched flow, if one exists. A
; pending attempt has no outcome. A replacement's FlowNode is its
; successor, never the predecessor named in LaunchProfile. An unknown
; request has neither attempt nor outcome; an outcome without an attempt
; is InconsistentRecords. If the rows change while read, the answer is
; ReadViewChanged. The snapshot is marker-consistent, not a transaction.
;
; Observe.Launch opens an exchange that goes on answering: on open it
; sends what LaunchStatus would, then one LaunchInspected frame for
; every later phase change, and it ends after the inspection carrying
; the outcome. Nothing is re-read on a timer; a launch that does not
; move sends nothing. Every other query is answered with exactly one
; frame.
;
; Nothing on this socket writes into a pane. Flow is the only pane writer,
; and it writes only through the privileged Deliver and Command of the
; meta contract, under its own per-pane lease.
;
; Observe.Agent opens an exchange that goes on answering: on open it
; sends the flow's agent state as Herdr shows it now, then one
; AgentObserved frame for every later change Herdr announces, and it
; ends after the frame carrying Gone, when the flow's bound pane has left
; Herdr or the flow is no longer live. Nothing is re-read on a timer. A
; flow Flow does not hold answers one Gone frame. Unknown is Herdr's own
; word for an agent it cannot read.
;
; A Pending flow becomes Active when it is witnessed live: on a
; Presented Deliver, or when List finds its bound pane present in Herdr.
; Nothing else promotes it.
;
; A flow's lifecycle is what List reports of it. Pending and Active are
; live: a bound native seat answers. Pending is a seat not yet witnessed
; live; Active is one that has been.
;
; The three ways a flow stops being live are distinct, and each names
; who ended it. Stopped is Flow's own act: Stop, or a replacement's
; reap, closed a pane Flow was holding. Exited is the seat's own act or
; its accident: its pane is gone from Herdr and Flow never closed it, so
; nothing can be sent to it. Retired is an owner's act: the flow is
; taken out of Flow's receiving deliberately, through the privileged
; Retire, whatever its pane is doing. A pane going away never makes a
; flow Retired — an exit retains the flow's record and says only that it
; Exited; retirement comes from authority, never from an observation.
;
; None of the three is a deletion: every one of them keeps the flow's
; row, its origin and its history, and none is ever reported with an
; Available route. Only Pending and Active ever are.
;
; ResolveCaller names the flow bound to the process that called: the
; Nexus reads the caller from its own socket, never from the payload.
; The optional FlowId is the caller's claim, checked against the
; binding: CallerMismatch carries the Caller the binding names.
;
; Bind binds the calling process to an Address. A Bind for { Field message
; Primary } is accepted only when the kernel-reported executable is the
; configured MessageNexusBinary; an unconfigured Nexus answers
; NotConfigured and another executable answers NotMessage. The Process in
; the request is not proof of the caller's executable.
;
; Lock, Deliver and Release are accepted only from the exact bound Message
; process (PID and start time). Message's Identify result supplies the
; distinct Sender Address in Lock; Flow trusts that bound Message peer's
; assertion and does not independently resolve the Sender's origin. A
; Sender must name an existing Awake metaflow. Unknown addresses are not
; created; an Asleep Sender is refused as Asleep and an Ended Sender as
; Ended.Address.
;
; Report carries one harness event of a flow Flow holds, sent by the
; harness's hook through the Flow CLI with the FlowId the flow was
; launched with. Flow stores the event in that flow's Memory and answers
; Reported. A FlowId Flow does not hold is refused, Refused.Unknown.FlowId,
; never adopted: a flow Flow did not launch is a flow Flow does not know.
;
; Launched is what Start answers, carried by the Started reply; it was
; named Started until 9.0.0, when Event's Started took that name.
```

#### Queries (18)
```
Start.StartRequest
Restart.RestartRequest
ResolveRecipient.RecipientResolutionRequest
Stop.FlowId
Replace.StartRequest
LaunchStatus.LaunchRequestId
Observe.ObserveSelection
ResolveCaller.Option<FlowId>
QueueTurnEnd.TurnEndRequest
Report.{ FlowId Event }
Lock.{ Sender Recipient }
Bind.{ Address Process }
Identify.Process
Deliver.{ Lock Request }
Release.Lock
End.Address
Current.Address
Metaflows
```

#### Responses (31)
```
Started.Launched
LaunchPending.LaunchAttempt
StartAmbiguous.PromptDeliveryIntent
Restarted.Restarted
RecipientResolved.FlowNode
Stopped.FlowId
Listed.Vector<Metaflow>
StartRejected.StartRejection
RestartRejected.RestartRejection
RecipientResolutionRejected.RecipientResolutionRejection
StopRejected.StopRejection
Replaced.Replaced
ReplaceRejected.ReplaceRejection
LaunchInspected.LaunchInspection
LaunchStatusRejected.LaunchStatusRejection
CallerResolved.Caller
CallerResolutionRejected.CallerResolutionRejection
AgentObserved.AgentObservation
TurnEndQueued.TurnEndRequest
TurnEndRejected.TurnEndRejection
Reported
Locked.Lock
Bound.FlowId
Identified.Address
Delivered
Queued
Woken.FlowId
Released
Ended
Current.[ Awake.FlowId Asleep Ended Unknown ]
Refused.Refusal
```

#### Types (88)
```
SessionId.String
TurnId.String
FlowType.String
Generation.Integer
EndpointPath.String
HerdrSessionName.String
HerdrAgentName.String
HerdrWorkspaceId.String
HerdrPaneId.String
HerdrTerminalId.String
LaunchRequestId.String
SourcePath.String
SourceSha256.String
SkillName.String
Effort.String
RememberingDepth.Integer
SystemPromptBundleFile.String
InstructionPrompt.String
FirstPromptBody.String
FirstPromptText.String
PromptSha256.String
NativeSessionId.String
NativeTurnId.String
ReceiptSha256.String
TranscriptDevice.String
TranscriptInode.String
TranscriptByteOffset.Integer
TranscriptPrefixSha256.String
TranscriptRootDevice.String
TranscriptRootInode.String
NativeSkillPath.String
NativeSkillSha256.String
PowerLevel.[ High Medium Low UltraLow ]
LaunchSource.{ SourcePath SourceSha256 }
RememberedFlow.{ FlowId RememberingDepth }
LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> Aspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
TargetReceiptRequest.{ LaunchRequestId PromptSha256 }
FirstPromptPayload.{ FirstPromptBody PromptSha256 FirstPromptText }
ComposedLaunch.{ LaunchProfile FirstPromptPayload TargetReceiptRequest }
HerdrPaneBinding.{ LaunchRequestId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId }
NativeLaunchIntent.{ LaunchRequestId PromptSha256 HarnessKind ModelName Effort Vector<SkillName> }
NativeLaunchBinding.{ LaunchRequestId FlowId NativeSessionId HarnessKind HerdrPaneBinding }
RegistrationAcknowledgement.{ LaunchRequestId FlowId NativeSessionId HerdrPaneBinding }
NativeTranscriptCursor.{ NativeSessionId HarnessKind TranscriptDevice TranscriptInode TranscriptByteOffset TranscriptPrefixSha256 }
NativeTranscriptAbsence.{ NativeSessionId HarnessKind TranscriptRootDevice TranscriptRootInode }
NativeTranscriptBoundary.[ Existing.NativeTranscriptCursor Absent.NativeTranscriptAbsence ]
NativeSkillSelection.{ SkillName NativeSkillPath NativeSkillSha256 }
PromptDeliveryIntent.{ LaunchRequestId PromptSha256 FlowId NativeSessionId HarnessKind ModelName Effort Vector<NativeSkillSelection> HerdrPaneBinding NativeTranscriptBoundary }
NativeTargetReceipt.{ LaunchRequestId PromptSha256 FlowId NativeSessionId NativeTurnId ReceiptSha256 ModelName Effort Vector<NativeSkillSelection> }
PromptDeliveryResult.[ Observed.NativeTargetReceipt Ambiguous.PromptDeliveryIntent ]
LaunchAttemptPhase.[ Reserved NativeLaunchIntentRecorded NativeBound RegistrationAcknowledged PromptIntentRecorded PromptObserved PromptAmbiguous ]
LaunchAttempt.{ LaunchRequestId LaunchProfile PromptSha256 OriginClue LaunchAttemptPhase Option<NativeLaunchIntent> Option<NativeLaunchBinding> Option<RegistrationAcknowledgement> Option<PromptDeliveryIntent> Option<PromptDeliveryResult> }
LaunchStatusOutcome.[ Started.Launched Replaced.Replaced StartRejected.StartRejection ReplaceRejected.ReplaceRejection ]
LaunchInspection.{ LaunchAttempt Option<LaunchStatusOutcome> Option<FlowNode> }
LaunchAttemptReservation.[ Reserved.LaunchAttempt Existing.LaunchAttempt Conflict ]
OriginClue.{ FlowId SessionId TurnId }
StartRequest.{ LaunchProfile OriginClue }
RestartRequest.{ FlowId OriginClue }
RecipientResolutionRequest.FlowId
StopRequest.FlowId
RouteReadiness.[ Ready Parked ]
EndpointSelection.[ Available.{ EndpointPath RouteReadiness } Unavailable ]
HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId }
HerdrRouteSelection.[ Available.HerdrRoute Unavailable ]
FlowLifecycle.[ Pending Active Stopped Retired Exited ]
FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle }
Launched.{ FlowId SessionId OriginClue }
Restarted.{ FlowId SessionId Generation }
BindingRefusal.[ PaneMismatch TerminalMismatch HarnessMismatch NotReady ReservedIdentityMismatch ClaimUnavailable ObservationRefused TransportRefused Unclassified ] ; BindingRefusal names one checked native-binding failure without raw adapter text. PaneMismatch covers the agent name, workspace, or pane check. TerminalMismatch covers the terminal check. HarnessMismatch covers the reported harness and official session source check. NotReady covers interactive readiness. ReservedIdentityMismatch covers selected, observed, or claimed identity conflicts. ClaimUnavailable covers Flow identity claim and claim readback failures. ObservationRefused covers a missing or malformed agent/session observation. TransportRefused covers the Herdr request or response transport boundary. Unclassified marks a stored v10 unit refusal whose stage was not kept.
StartRejection.[ CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused BindingRefused.BindingRefusal RegistrationRefused IntentPersistenceRefused OriginUnavailable ] ; StartRejection preserves a typed BindingRefused result at the public wire.
RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ]
RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ]
StopRejection.[ UnknownFlow AlreadyStopped RouteUnavailable CloseRefused PersistenceRefused ]
Replaced.{ FlowId Launched }
ReplaceRejection.[ PredecessorAbsent UnknownPredecessor PredecessorStopped LaunchRefused.StartRejection ReapRefused.StopRejection ]
ObserveSelection.[ Launch.LaunchRequestId Agent.FlowId ]
AgentState.[ Idle Working Blocked Done Unknown Gone ]
AgentObservation.{ FlowId AgentState }
LaunchStatusRejection.[ UnknownLaunchRequest PersistenceRefused ReadViewChanged InconsistentRecords ]
Caller.{ FlowId Aspect PowerLevel ModelName }
CallerResolutionRejection.[ CallerUnknown CallerMismatch.Caller ]
Title.String
Presentation.{ Title }
TranscriptPath.String
TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }
TurnEndRejection.[ UnknownSession SessionMismatch InvalidTurnId InvalidTranscriptPath QueueRefused ]
Refusal.[ Locked Held.Lock Awake.FlowId Asleep Lapsed Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ] NoLayer NotConfigured Ended.Address OffRoute NoneAbove NotMessage Taken.Address Unidentified.Process Store.String ]
Event.[ Started ToolUsed.String Stopped ]
```

## (C) meta-signal-flow, branch field/meta-aspect-store-1a1258b9873b, ethos/signal.ethos

Root: `Signal`. Imports: `signal_flow:[ FlowNode FlowId Aspect PowerLevel ModelName HarnessKind NativeSessionId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId Caller CallerResolutionRejection Event ] flow_ethos:[ OrdinarySocketPath MetaSocketPath SourceRoot ClientPath Home ControlSocketPath CodexEndpoint StableCodex NextCodex Key KeyName CommandSigil InterruptKeys SubmitKeys HarnessProfile HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease Subaspect Topic Layer Source ]`

File header comment (verbatim, before the `Signal` root):
```
; Flow privileged Signal.
;
; Flow is the only pane writer. Deliver and Command are the only ways
; anything is typed into a flow's pane, and both run under Flow's own
; per-pane lease: an exclusive hold over the whole key sequence, never
; handed out on the wire.
;
; Deliver carries a typed Message addressed by FlowId; Flow renders it,
; so the pane text always begins with its Priority head (HardAbrupt.,
; MiddleAbrupt. or Soft.). A Letter names its MessageId first: the id the
; sender's Message Nexus minted, carried through untouched so the
; recipient reading the pane can Acknowledge it. Flow never interprets it. The Content may hold no control character but
; LF and TAB (ControlCharacter carries the byte offset in the rendered
; pane text), and a first line that is a harness command (a sigil of the
; recipient's HarnessProfile, then a command word) is refused as
; HarnessCommand: harness commands go through Command. Vet answers what
; Deliver would refuse and types nothing. Deliver is idempotent on its
; DeliveryId: a repeat answers the stored Delivery and types nothing. A
; delivery a crash left under the lease settles Uncertain and is never
; retried.
;
; Soft needs the recipient Idle or Done; every tier refuses a Blocked
; recipient and a composer that already holds text. Transported means
; Herdr accepted the text for the exact binding; Presented means the
; recipient was seen reacting on the exact pane. InterruptWitness says
; whether a HardAbrupt interrupt was seen to leave Working.
;
; Every query on this socket answers MetaRefused unless the peer is the
; configured Message Nexus executable, a process in no flow's pane (the
; owner), or a flow whose aspect is in MetaAspects.
;
; MessageNexusBinary is the executable identity used by Bind as Message on
; the ordinary socket. A payload PID does not establish that identity.
;
; ResolvePeer names the flow a process runs in, as ResolveCaller does for
; an ordinary connection's own peer.
;
; ReadEvents answers the harness events Flow holds in its Memory for one
; flow, in the order its Reports were recorded: EventsRead, or
; ReadEventsRejected.UnknownFlow for a FlowId Flow does not hold.
;
; Configure accepts one whole typed Module, Model, Threshold or Nexus value.
; The three non-Nexus values are independent updates. Nexus setup values must
; agree within one process. Configuration reads the committed Nexus and the
; committed model, threshold and module vectors; it never returns defaults.
; Configure.Nexus names the actual Message executable in MessageNexusBinary.
; Lease is the lock duration in seconds; a fresh, unconfigured default is 60.
```

#### Queries (11)
```
Configuration
Configure.ConfigurationChange
ConsumeReset.ResetRequest
RegisterFlow.FlowNode
MetaBindExisting.MetaBindExisting
Retire.FlowId
Deliver.DeliveryRequest
Vet.DeliveryRequest
Command.CommandRequest
ResolvePeer.ProcessIdentity
ReadEvents.FlowId
```

#### Responses (23)
```
Configured
Configuration.ConfigurationSnapshot
Unconfigured
ResetConsumed.ResetOutcome
FlowRegistered.FlowNode
ConfigureRejected.ConfigureRejection
ResetRejected.ResetRejection
FlowRegistrationRejected.FlowRegistrationRejection
BoundExisting.BoundExisting
BindExistingRejected.BindExistingRejection
FlowRetired.FlowNode
RetireRejected.RetireRejection
Delivered.Delivery
DeliveryRejected.DeliveryRejection
Vetted.FlowId
Commanded.CommandOutcome
CommandRejected.CommandRejection
PeerResolved.Caller
PeerResolutionRejected.CallerResolutionRejection
MetaRefused.MetaRefusal
Refused.Refusal
EventsRead.{ FlowId Vector<Event> }
ReadEventsRejected.[ UnknownFlow StoreRefused ]
```

#### Types (58)
```
NexusRuntimeSettings.{ OrdinarySocketPath MetaSocketPath SourceRoot StableCodex NextCodex Vector<HarnessProfile> MetaAspects MessageNexusPath MessageNexusBinary Lease } ; Flow Library owns the shared configuration field types. This record exists only for Flow's current internal launch defaults. The process sockets are separately supplied by Library.Start; this record is not a Configure wire payload.
ConfigureModule.{ Key Source }
ConfigureModel.{ Layer Native.String }
ConfigureThreshold.{ Layer Handover.Integer Refresh.Integer }
ConfigureNexus.{ SourceRoot StableCodex NextCodex HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease }
ConfigurationChange.[ Module.ConfigureModule Model.ConfigureModel Threshold.ConfigureThreshold Nexus.ConfigureNexus ] ; Keep the payload type distinct from the unit Query.Configuration variant.
ConfigurationSnapshot.{ Nexus.ConfigureNexus Models.Vector<ConfigureModel> Thresholds.Vector<ConfigureThreshold> Modules.Vector<ConfigureModule> }
IdempotencyKey.String
CreditId.String
CreditSelection.[ Next Specific.CreditId ]
ResetRequest.{ IdempotencyKey CreditSelection }
ResetOutcome.[ Reset NothingToReset NoCredit AlreadyRedeemed ]
ConfigureRejection.[ StoreRefused Conflict ]
ResetRejection.[ AdapterUnavailable ProtocolRefused ]
FlowRegistrationRejection.[ StoreRefused UnknownOrUnclaimedIdentity ConflictingBinding ]
ProcessId.Integer
ProcessUserId.Integer
ProcessStartToken.String
ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken }
HerdrServerSocketPath.String
HerdrServerProcessIdentity.ProcessIdentity
MetaFlowOwnerId.FlowId
HerdrTabId.String
WorkingDirectory.String
FlowLifecycle.[ RegisteredUnconfirmed ]
FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }
FlowBinding.{ FlowId Aspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }
MetaBindExisting.{ FlowContainer Vector<FlowBinding> }
BoundFlowBinding.{ FlowId FlowLifecycle }
FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ]
RefusedFlowBinding.{ FlowId FlowBindingRefusalReason }
FlowBindingResult.[ Bound.BoundFlowBinding Refused.RefusedFlowBinding ]
BoundExisting.{ FlowContainer Vector<FlowBindingResult> }
BindExistingRejection.[ ContainerUnavailable ContainerIdentityMismatch StoreRefused ]
RetireRejection.[ UnknownFlow AlreadyGone StoreRefused ]
DeliveryId.String
MessageId.String
CommandLine.String
ByteOffset.Integer
Sender.[ Flow.FlowId Owner ]
PsycheContext.String
PsycheVerbatim.String
Content.[ Text.String Psyche.{ PsycheContext PsycheVerbatim } ]
Letter.{ MessageId Sender Content }
Message.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]
DeliveryRequest.{ DeliveryId FlowId Message }
InterruptWitness.[ NotRequested Observed Unobserved ]
DeliveryGrade.[ Transported Presented Uncertain ]
Delivery.{ DeliveryId FlowId InterruptWitness DeliveryGrade }
BodyRefusal.[ EmptyBody HarnessCommand.CommandLine ControlCharacter.ByteOffset ]
DeliveryRejection.[ UnknownFlow FlowStopped RouteUnavailable RecipientWorking RecipientBlocked ComposerOccupied BodyRefused.BodyRefusal NotDelivered PersistenceRefused FlowRetired FlowExited ]
HarnessCommand.[ Compact Interrupt ]
CommandRequest.{ FlowId HarnessCommand }
CommandGrade.[ Transported Observed Uncertain ]
CommandOutcome.{ FlowId HarnessCommand CommandGrade }
CommandRejection.[ UnknownFlow FlowStopped RouteUnavailable RecipientBlocked UnsupportedForHarness NotDelivered FlowRetired FlowExited ]
MetaRefusal.[ PeerUnknown PeerNotAuthorized.Caller ]
Refusal.[ Store.String ]
```

## Differences

### Types in (A) and in neither (B) nor (C) as a declaration

Reading: "imported" means B or C names it in its imports (from `flow_ethos` or `signal_flow`), so the declaration lives elsewhere (the Library, which has no file on these branches). "absent" means neither declares nor imports it.

| (A) type | where | status |
|---|---|---|
| FlowId | A Library | imported (B imports it, C imports it) |
| Topic | A Library | imported (B imports it, C imports it) |
| Blake3 | A Library | absent |
| Layer | A Library | imported (B imports it, C imports it) |
| Subaspect | A Library | imported (B imports it, C imports it) |
| Source | A Library | imported (B imports it, C imports it) |
| Path | A Library | absent |
| Reason | A Library | absent |
| Key | A Library | imported (B imports it, C imports it) |
| Said | A Library | absent |
| Request | A Library | imported (B imports it) |
| Aspect | A Library | imported (B imports it, C imports it) |
| Address | A Library | imported (B imports it) |
| Recipient | A Library | imported (B imports it) |
| Metaflow | A Library | imported (B imports it) |
| Lock | A Library | imported (B imports it) |
| Process | A Library | imported (B imports it) |
| Start | A Library | imported (B imports it) |
| StoreRefusal | A Library | absent |
| StartRefusal | A Library | absent |
| Nexus | A Library | absent |
| Flow | A Memory | absent |
| Module | A Memory | absent |
| Model | A Memory | absent |
| Metaflow | A Memory | imported (B imports it) |
| Lock | A Memory | imported (B imports it) |
| Nexus | A Memory | absent |
| Threshold | A Memory | absent |
| Encodable | A Library trait | absent |

Queries and responses of (A) not present by name:

- flow queries not in B queries: Launch, Wake, Refresh
- flow responses not in B responses: Launched, Refreshed, Observed
- meta queries not in C queries: Forget
- meta responses not in C responses: Forgotten

### Types and variants in (B) or (C) and not in (A)

- B queries (6): Restart, ResolveRecipient, Replace, LaunchStatus, ResolveCaller, QueueTurnEnd
- B responses (18): Started, LaunchPending, StartAmbiguous, Restarted, RecipientResolved, StartRejected, RestartRejected, RecipientResolutionRejected, StopRejected, Replaced, ReplaceRejected, LaunchInspected, LaunchStatusRejected, CallerResolved, CallerResolutionRejected, AgentObserved, TurnEndQueued, TurnEndRejected
- B types (87): SessionId, TurnId, FlowType, Generation, EndpointPath, HerdrSessionName, HerdrAgentName, HerdrWorkspaceId, HerdrPaneId, HerdrTerminalId, LaunchRequestId, SourcePath, SourceSha256, SkillName, Effort, RememberingDepth, SystemPromptBundleFile, InstructionPrompt, FirstPromptBody, FirstPromptText, PromptSha256, NativeSessionId, NativeTurnId, ReceiptSha256, TranscriptDevice, TranscriptInode, TranscriptByteOffset, TranscriptPrefixSha256, TranscriptRootDevice, TranscriptRootInode, NativeSkillPath, NativeSkillSha256, PowerLevel, LaunchSource, RememberedFlow, LaunchProfile, TargetReceiptRequest, FirstPromptPayload, ComposedLaunch, HerdrPaneBinding, NativeLaunchIntent, NativeLaunchBinding, RegistrationAcknowledgement, NativeTranscriptCursor, NativeTranscriptAbsence, NativeTranscriptBoundary, NativeSkillSelection, PromptDeliveryIntent, NativeTargetReceipt, PromptDeliveryResult, LaunchAttemptPhase, LaunchAttempt, LaunchStatusOutcome, LaunchInspection, LaunchAttemptReservation, OriginClue, StartRequest, RestartRequest, RecipientResolutionRequest, StopRequest, RouteReadiness, EndpointSelection, HerdrRoute, HerdrRouteSelection, FlowLifecycle, FlowNode, Restarted, BindingRefusal, StartRejection, RestartRejection, RecipientResolutionRejection, StopRejection, Replaced, ReplaceRejection, ObserveSelection, AgentState, AgentObservation, LaunchStatusRejection, Caller, CallerResolutionRejection, Title, Presentation, TranscriptPath, TurnEndRequest, TurnEndRejection, Refusal, Event
- C queries (8): ConsumeReset, RegisterFlow, MetaBindExisting, Retire, Vet, Command, ResolvePeer, ReadEvents
- C responses (18): ResetConsumed, FlowRegistered, ConfigureRejected, ResetRejected, FlowRegistrationRejected, BoundExisting, BindExistingRejected, FlowRetired, RetireRejected, DeliveryRejected, Vetted, Commanded, CommandRejected, PeerResolved, PeerResolutionRejected, MetaRefused, EventsRead, ReadEventsRejected
- C types (57): NexusRuntimeSettings, ConfigureModule, ConfigureModel, ConfigureThreshold, ConfigureNexus, ConfigurationChange, ConfigurationSnapshot, IdempotencyKey, CreditId, CreditSelection, ResetRequest, ResetOutcome, ConfigureRejection, ResetRejection, FlowRegistrationRejection, ProcessId, ProcessUserId, ProcessStartToken, ProcessIdentity, HerdrServerSocketPath, HerdrServerProcessIdentity, MetaFlowOwnerId, HerdrTabId, WorkingDirectory, FlowLifecycle, FlowContainer, FlowBinding, MetaBindExisting, BoundFlowBinding, FlowBindingRefusalReason, RefusedFlowBinding, FlowBindingResult, BoundExisting, BindExistingRejection, RetireRejection, DeliveryId, MessageId, CommandLine, ByteOffset, PsycheContext, PsycheVerbatim, Content, Letter, Message, DeliveryRequest, InterruptWitness, DeliveryGrade, Delivery, BodyRefusal, DeliveryRejection, HarnessCommand, CommandRequest, CommandGrade, CommandOutcome, CommandRejection, MetaRefusal, Refusal

### Same name, different declaration

Each entry gives (A) first, then the other, exactly as collapsed above. Compared by name across A's Library, Memory, queries and responses and B/C's types, queries and responses; the comparison is within the matching socket for queries and responses and across all declarations for types.

- Sender (A Library vs C types)
  - A: `Sender.Address`
  - other: `Sender.[ Flow.FlowId Owner ]`
- Observe (A flow query vs B queries)
  - A: `Observe.Agent.FlowId`
  - other: `Observe.ObserveSelection`
- Stopped (A flow response vs B responses)
  - A: `Stopped`
  - other: `Stopped.FlowId`
- Refused (A flow response vs B responses)
  - A: `Refused.[ Locked Held.Lock Awake.FlowId Asleep Lapsed Unknown.[ Address Lock FlowId Key ] NoLayer NotConfigured HashMismatch Ended.Address OffRoute NoneAbove NotMessage Unidentified.Process Taken.Address Store.String ]`
  - other: `Refused.Refusal`
- Configure (A meta query vs C queries)
  - A: `Configure.[ Module.{ Key Source } Model.{ Layer Harness.HarnessKind Native.String } Threshold.{ Layer Handover.Integer Refresh.Integer } Nexus ]`
  - other: `Configure.ConfigurationChange`
- Configuration (A meta response vs C responses)
  - A: `Configuration.{ Nexus Models.Vector<Model> Thresholds.Vector<Threshold> Modules.Vector<Module> }`
  - other: `Configuration.ConfigurationSnapshot`
- Refused (A meta response vs C responses)
  - A: `Refused.[ NoSource.Path HashMismatch Conflict Unknown.Key Store.String ]`
  - other: `Refused.Refusal`

Identical, flow queries: End, Current, Bind, Lock, Identify, Deliver, Release, Report, Stop, Metaflows

Identical, flow responses: Ended, Current, Bound, Locked, Identified, Delivered, Queued, Woken, Released, Reported, Listed

Identical, meta queries: Configuration

Identical, meta responses: Configured, Unconfigured

Identical, Library types vs B types: none

Identical, Library types vs C types: none

Identical, Memory records vs B types: none

Identical, Memory records vs C types: none

Between (B) and (C), declared in both with different declarations:

- FlowLifecycle
  - B: `FlowLifecycle.[ Pending Active Stopped Retired Exited ]`
  - C: `FlowLifecycle.[ RegisteredUnconfirmed ]`
- Refusal
  - B: `Refusal.[ Locked Held.Lock Awake.FlowId Asleep Lapsed Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ] NoLayer NotConfigured Ended.Address OffRoute NoneAbove NotMessage Taken.Address Unidentified.Process Store.String ]`
  - C: `Refusal.[ Store.String ]`
- Delivered (response)
  - B: `Delivered`
  - C: `Delivered.Delivery`
Notes on the differences (the flow's reading of the lists above, not stated by any source):

- (A) declares the Library types once and both Signals import them; (B) and (C) import part of that set from `flow_ethos` (B: Aspect Address FlowId Request Lock Sender Process Metaflow Key Recipient Layer Topic Subaspect Source OrdinarySocketPath MetaSocketPath Start ModelName HarnessKind; C: OrdinarySocketPath MetaSocketPath SourceRoot ClientPath Home ControlSocketPath CodexEndpoint StableCodex NextCodex Key KeyName CommandSigil InterruptKeys SubmitKeys HarnessProfile HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease Subaspect Topic Layer Source). The types (A) puts in the Library and neither imports nor declares are Blake3, Path, Reason, Said, StoreRefusal, StartRefusal, Nexus.
- (B) imports `Sender` from `flow_ethos` as (A) declares it (`Sender.Address`), while (C) declares its own `Sender.[ Flow.FlowId Owner ]`.
- (B) imports `Start` from `flow_ethos` and also declares a query variant `Start.StartRequest`; in (A) `Start` is the Nexus start datom and the query is `Launch`.
- (A)'s flow-socket `Launch`, `Wake`, `Refresh` queries and the `Launched`, `Refreshed`, `Observed` responses have no counterpart in (B); (B) has `Start`/`Restart`/`Replace` and `Started`/`Restarted`/`Replaced`. The (A) `Refused` carries `HashMismatch`; (B)'s `Refusal` has no `HashMismatch` and writes the inner `Unknown` as `Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ]` where (A) writes `Unknown.[ Address Lock FlowId Key ]`. The order of `Taken.Address` and `Unidentified.Process` is swapped. (C)'s `Refusal` is `Store.String` alone; (C)'s `MetaRefused` takes the others.
- (A)'s `Send.{ Address Request }` (Message simple form) is declared in neither (B) nor (C). (A)'s `Deliver.{ Lock Request }` equals (B)'s query `Deliver`; (C)'s `Deliver.DeliveryRequest` is a different, FlowId-addressed message.
- (A) `Configure` carries Module, Model, Threshold and Nexus in place; (C) names them `ConfigureModule`, `ConfigureModel`, `ConfigureThreshold`, `ConfigureNexus` inside `ConfigurationChange`. (A)'s Model has `Layer Harness.HarnessKind Native.String`; (C)'s `ConfigureModel` is `Layer Native.String`.
- (A)'s Memory records (Flow, Module, Model, Threshold) have no counterpart in (B) or (C), which declare wire types only; (A)'s `Forget` / `Forgotten` have none in (C).
- (A) declares `Event` by prose as Started, ToolUsed.String, ContextMeasured.{ Tokens.Integer Window.Integer }, Stopped; (B) declares `Event.[ Started ToolUsed.String Stopped ]`, without ContextMeasured.

## Traits

None of the three sources declares a trait or a capability in a code block. Grep for `trait`, `Trait`, `fn`, `behaviour`, `behavior`, `query`, `response` over the three sources (case-insensitive) returned:

- (A) line 169 of the report: "Encodable, the trait behind Blake3 (vision-datom):" followed by a code block, the only trait-shaped declaration in (A), written in prose beside the Library and not inside the Library root (whose traits and associations sections are `[]` `[]`):

  ```
  Encodable.[
     encode.String        ; the bare run
     decode:{
        [ Textualizable ] ; the run read
        [ Result<Self Error> ] } ]
  ```

  (A) line 403: "Identify and the Deliver responses and refusals above"; line 509: "Printed forms. Responses print in datom's canonical form" (prose, no trait).
- (B) `signal.ethos` line 36: "; move sends nothing. Every other query is answered with exactly one"; line 236: "; TransportRefused covers the Herdr request or response transport boundary." Both are comments.
- (C) `signal.ethos` line 28: "; Every query on this socket answers MetaRefused unless the peer is the"; line 95: "; Keep the payload type distinct from the unit Query.Configuration variant." Both are comments.
- No `fn`, `behaviour` or `behavior` hit in any source. Neither (B) nor (C) has a traits section (their roots are `Signal` with four sections: imports, queries, responses, types).
- Behaviour appears only as comment prose in (B) and (C), not as declarations. Examples quoted: (B) "Replace carries a StartRequest whose LaunchProfile names the replaced flow as its predecessor. The successor is launched; once it has Started, the predecessor is Stopped and taken out of receiving, and only then is the successor routable."; (B) "No handler, hook or state subscription is implemented by this vocabulary."; (B) "Observe.Launch opens an exchange that goes on answering ... Nothing is re-read on a timer"; (C) "Deliver is idempotent on its DeliveryId: a repeat answers the stored Delivery and types nothing."; (C) "Every query on this socket answers MetaRefused unless the peer is the configured Message Nexus executable ...". (A)'s behaviour sits in section 2, Rules, outside the range read.

## Ethos syntax today

Sources: `/home/li/primary/.claude/skills/knowledge-ethos/SKILL.md` (the generated skill; `/git/github.com/LiGoldragon/psyche-skills/skills/knowledge-ethos.md` does not exist), whose line 6 says "As of 16.0.0 ethos-zero reads four roots", and the grammar it points to, `/git/github.com/LiGoldragon/ethos-zero` (Cargo.toml version 17.0.0, local HEAD b2fa8b0, `README.md`, `fixtures/*.ethos`, and protos's `protos-kinds.ethos`). The skill and the checkout differ in version (16.0.0 against 17.0.0) and in vocabulary: the skill says "kind", the README says "trait" for the same thing. The README is quoted for traits.

Roots and sections (README lines 41 to 49, SKILL.md line 6):

```
Library    [ imports ] [ types ] [ traits ] [ associations ]
Signal     [ imports ] [ queries ] [ responses ] [ types ]
Memory     [ imports ] [ record types ]
```

Struct. `Name.{ fields }`, a field named after its type (SKILL.md line 10, README line 73). Example (`fixtures/record-types.ethos`): `Record.{ String Integer }`. A position may declare its type in place: `Capsule.{ Home.String Login.Vector<String> }` (README line 73).

Enum. `Name.[ variants ]`; a variant carries a payload as `Variant.Type`, `Variant.{ ... }` or `Variant.[ ... ]` (README lines 92 and 104). Example: `State.[ Running Ended ]` (README line 74), and from this inventory `Refusal.[ Locked Held.Lock Store.String ]`.

Alias. `Name.Type`, for example `Short.String` and `OptionalSpiritGuardianProviderName.Option<SpiritGuardianProviderName>` (`fixtures/alias-format.ethos`; SKILL.md line 10).

Trait. Supported, in a Library's third section only (README lines 113 to 118; SKILL.md line 12). `Name.[ capabilities ]` or `Name.{ [ supertraits ] [ associated types ] [ CONSTANTS ] [ capabilities ] }`. The receiver is the separator: `.` is `&self`, `!` is `&mut self`, `:` takes no self; `name.[ Yield ]` yields alone, `name.{ [ inputs ] [ Yield ] }` takes inputs. Examples, from `protos-kinds.ethos` lines 15 and 8 and the README line 128:

```
Textualizable.[ textualize.[ String ] ]
Spendable.[ spend![ Boolean ] ]
Resolvable.[ resolve.{ [ Textualizable ] [ Self ] } ]
```

A type bears a trait in the fourth Library section, the associations: `ReaderBudget.[ Spendable ]` (`protos-kinds.ethos` line 18; SKILL.md line 6 and README line 46 name the section). A concrete type in an input is refused, `Conceptual.{ [ path ] TraitWanted.String }` (README lines 136 to 138). The generated Rust method is `fn resolve<N: Textualizable>(&self, input: N) -> Self` (README line 129). The interaction body is hand-written (SKILL.md line 16). Neither Signal nor Memory has a traits section, so a trait cannot be declared in those roots; both can only import a trait name from a Library.

Generic. No generic type can be declared: no declaration form takes a type parameter, and `fixtures/*.ethos` and `ethos-zero.ethos` contain none. Generic types are applied: the intrinsics Vector, Option, Result are written with tight angles, `Vector<Event>`, `Option<FlowId>`, `Result<Protos Error>` (README line 155; SKILL.md line 10), and an imported generic can be applied, `qualified.[ Wrapper<Self> ]` (`fixtures/self-traits.ethos` line 2). A trait head parameter and a bounded associated type appear in the trait form, `Streamable.{ [] [ Item<Textualizable> ] [] [ push!{ [ Textualizable ] [ Self ] } ] }` (README line 133), and the generator emits method generics lettered from `N` (README line 124; SKILL.md line 12). Bytes<N> is not expressible: (A) records that ethos-zero 16.0.0 cannot express `Bytes<32>` or the inline import `Topic:Name`; the 17.0.0 README states neither.

Are traits expressible at all? Yes, in a Library's third section with bearing in the fourth, as a hand-chosen set of capability signatures that generate Rust trait definitions; not in a Signal or a Memory. Whether (A)'s Library can put `Encodable` there is not stated; (A) puts it in prose beside the Library.
