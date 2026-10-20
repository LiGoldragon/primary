<!-- to-the-living:start -->
Presentation.{ «Flow's Ethos, as it now stands» }

# Flow's Ethos, as it now stands

## psyche-context › vision/nexus.md

````markdown
## A Nexus is the whole

A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.

## A kind of thing

Nexus is our word for the style of component that speaks signal and uses a similar database.

## Library and daemon

Every component built from now on is a Nexus. The nexus repository is
the library that defines the core of a Nexus component.

## Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.

## Long term: traits in ethos

Long term, every trait a Nexus uses is declared in ethos; short term, a Nexus goes without declared traits.

## Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

## Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

## Sockets

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

## Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.

## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.

Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.

## The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

Peers depend on each other's wire repositories, never on each other's Nexuses.

## Routing

Signals cross the network through a router. The router tells signal
types apart by an enum that wraps the objects, held in the signal
repository, which every component depends on. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

## First configuration

A Nexus keeps a standard metadata tree. In it a type records whether
the meta Configure was ever done; that record is reversed only on the
meta socket, and while it is unset Configure is accessible on the
ordinary socket. The tree holds everything standard about the Nexus:
its socket paths — its own and those of every edge-socket it connects
to — and whatever else comes up as standard nexus configuration data.
The built-in default configuration is independent of this and is
what gives the socket path on which the Configure signal arrives.

## Repositories

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

`<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, never optional, since configuration flows through it. The CLI is `<nexus>`.

A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each; no catch-all. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary never appears on the public wire.

## Why everything is a Nexus

The Nexus is an architecture concept, not one specific Nexus: everything made is a Nexus.

A Nexus's vision is split by its code modules.

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

## Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

## Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.

## Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

## Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.

## Three parts and one path

A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.

The library, shared by the three parts:

```ethos
Library
[]
[ FlowId.Integer
  Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
  Address.{ Aspect Topic Layer }
  Event.[ Started Stopped ] ]
[]
[]
```

Signal, what Flow says:

```ethos
Signal
[ flow:[ FlowId Address Event ] ]
[ Launch.{ Address Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId
  Refused.[ NoCapsule
            AddressBusy.Address ]
  Reported ]
[]
```

Operation, what Flow does:

```ethos
Operation
[ flow:[ FlowId Address Event ] ]
[ Start.{ Address Capsule }
  Record.{ FlowId Event } ]
[ Started.FlowId
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

Memory, what Flow remembers:

```ethos
Memory
[ flow:[ FlowId Address Event ] ]
[ Flow.{ FlowId Address
         State.[ Running Ended ]
         Vector<Event> }
  Answer.[ Succeeded Failed ] ]
```

```datom
; 1 Query, typed at the CLI, sent as signal
Launch.{ { Psyche core Primary }
         «Draft the Nexus book» }
; 2 Operation, from Signal's intend
Start.{ { Psyche core Primary }
        { /home/li/primary [] } }
; 3 the Change Operation hands Memory
Flow.{ 7 { Psyche core Primary } Running
       [ Started ] }
; 4 Memory's answer to Operation
Succeeded
; 5 Outcome
Started.7
; 6 Response, from Signal's answer, to the CLI
Launched.7
```
````

### Proposal 1: Library, changed in 6c8e266 · psyche-context › vision/nexus.md

```ethos
  Library
  []
  [ FlowId.Integer
- Voice.{ Aspect Layer }
+ Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
+ Address.{ Aspect Topic Layer }
  Event.[ Started Stopped ] ]
  []
  []
```

```
+--------------------------+
| Voice                    |
| removed                  |
+--------------------------+
             |
             | is replaced by
             v
+--------------------------+
| Address                  |
| Aspect Topic Layer       |
| added                    |
+--------------------------+
      |         |         |
      | named   | named   | named
      | by      | by      | by
      v         v         v
+----------+ +-----------+ +--------+
| Signal   | | Operation | | Memory |
+----------+ +-----------+ +--------+
```

### Proposal 2: Signal, changed in 6c8e266 · psyche-context › vision/nexus.md

```ethos
  Signal
- [ flow:[ FlowId Voice Event ] ]
- [ Launch.{ Voice
-          Brief.String }
+ [ flow:[ FlowId Address Event ] ]
+ [ Launch.{ Address Brief.String }
  Report.{ FlowId Event } ]
  [ Launched.FlowId
  Refused.[ NoCapsule
-           VoiceBusy.Voice ]
+           AddressBusy.Address ]
  Reported ]
  []
```

### Proposal 3: Operation, changed in 6c8e266 · psyche-context › vision/nexus.md

```ethos
  Operation
- [ flow:[ FlowId Voice Event ] ]
- [ Start.{ Voice Capsule }
+ [ flow:[ FlowId Address Event ] ]
+ [ Start.{ Address Capsule }
  Record.{ FlowId Event } ]
  [ Started.FlowId
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
  [ Capsule.{ Home.String
            Login.Vector<String> } ]
```

### Proposal 4: Memory, changed in 6c8e266 · psyche-context › vision/nexus.md

```ethos
  Memory
- [ flow:[ FlowId Voice Event ] ]
- [ Flow.{ FlowId
-        Voice
+ [ flow:[ FlowId Address Event ] ]
+ [ Flow.{ FlowId Address
         State.[ Running Ended ]
-        Vector<Event> } ]
+        Vector<Event> }
+ Answer.[ Succeeded Failed ] ]
```

```
+--------------------+
| Signal             |
+--------------------+
    |            ^
    | asks       | replies
    v            |
+--------------------+
| Operation          |
+--------------------+
    |            ^
    | changes    | answers Succeeded
    v            | or Failed (added)
+--------------------+
| Memory             |
+--------------------+
```

### Proposal 5: The Datom path, changed in 6c8e266 · psyche-context › vision/nexus.md

```datom
  ; 1 Query, typed at the CLI, sent as signal
- Launch.{ { Psyche Primary } «Draft the Nexus book» }
+ Launch.{ { Psyche core Primary }
+          «Draft the Nexus book» }
  ; 2 Operation, from Signal's intend
- Start.{ { Psyche Primary } { /home/li/primary [] } }
+ Start.{ { Psyche core Primary }
+         { /home/li/primary [] } }
  ; 3 the Change Operation hands Memory
- Flow.{ 7 { Psyche Primary } Running [ Started ] }
+ Flow.{ 7 { Psyche core Primary } Running
+        [ Started ] }
  ; 4 Memory's answer to Operation
  Succeeded
  ; 5 Outcome
  Started.7
- ; 6 Response, from Signal's answer, back to the CLI
+ ; 6 Response, from Signal's answer, to the CLI
  Launched.7
```

## flow › crates/flow-ethos/ethos/library.ethos

```ethos
; Flow's shared types live in this leaf package. Signal and Meta-Signal
; import them here and re-export their original Rust paths. Aspect is one
; nominal type shared by addresses, launch profiles and meta configuration.

Library
[]
[ FlowId.String
  ; ethos-zero 16 cannot express Topic:Name yet; check camelCase at input.
  Topic.String
  ; The design type is Blake3.Bytes<32>; 16.0 uses a 64-hex-character string.
  Blake3.String
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ]
  ; Define the component types once. Source refers to these declarations;
  ; inlining Path.String inside Source would redeclare Path globally.
  Repository.String
  Hash.Blake3
  Path.String
  Reason.String
  Source.{ Repository Hash Path }
  Key.{ Subaspect Topic }
  Said.{ Context.String Verbatim.String }
  Request.[ Order.String
            Question.String
            Psyche.Said
            Psyches.Vector<Said>
            Result.String
            Notice.String ]
  Aspect.[ Psyche Mind Field ]
  Address.{ Aspect Topic Layer }
  Recipient.[ Address Up ]
  ; Who a queued request is from: the Address Flow resolved for its sender
  ; (the Lock's Sender of a Deliver, the thread's metaflow of a send-tool
  ; call), or Unknown for a request queued before Flow kept senders.
  SentBy.[ Sender Unknown ]
  QueuedRequest.{ SentBy Request }
  Metaflow.{ Address
             State.[ Awake.FlowId Asleep Ended ]
             Past.Vector<FlowId>
             Queue.Vector<QueuedRequest> }
  Lock.{ Sender Address Until.Integer }
  Process.{ Pid.Integer Started.Integer }
  Sender.Address
  OrdinarySocketPath.String
  MetaSocketPath.String
  StorePath.String
  Start.{ OrdinarySocketPath MetaSocketPath StorePath }
  ; Startup refusal is distinct from the ordinary/meta socket Refusal.Store.String.
  StoreRefusal.{ Path Reason }
  StartRefusal.[ Store.StoreRefusal ]
  SourceRoot.String
  ClientPath.String
  Home.String
  ControlSocketPath.String
  ModelName.String
  CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }
  StableCodex.CodexEndpoint
  NextCodex.CodexEndpoint
  HarnessKind.[ Codex Claude ]
  KeyName.String
  CommandSigil.String
  InterruptKeys.Vector<KeyName>
  SubmitKeys.Vector<KeyName>
  HarnessProfile.{ HarnessKind Vector<CommandSigil> InterruptKeys SubmitKeys }
  HarnessProfiles.Vector<HarnessProfile>
  MetaAspects.Vector<Aspect>
  MessageNexusPath.String
  MessageNexusBinary.String
  Nexus.{ SourceRoot
          StableCodex
          NextCodex
          HarnessProfiles
          MetaAspects
          MessageNexusPath
          MessageNexusBinary
          Lease.Integer } ] ; Lease seconds; 60 before any Nexus payload.
[]
[]
```

## flow › crates/flow-nexus/ethos/operation.ethos

```ethos
; Flow Nexus Operation: what the Nexus does. Every effect its launch and
; record paths perform is one operation, and each is answered by one
; Outcome. An effect changes something: Herdr's panes, a harness, the
; or the store. A read of the world (a pane's presence, a transcript
; receipt, a seat's composed context) is not an operation.
;
; Compose has the context composer compose the seat's system and USER
; context from the module identities its profile names, verifies it, and
; composes the system prompt and the first USER message, split into parts
; when it does not fit one message; nothing is written to disk.
; Reserve opens the launch attempt in the journal and, for a Claude launch,
; claims the flow's FlowId for the native session id Flow chooses for it,
; and holds that flow in Memory before any harness runs: Reserved carries
; the FlowId, Spawn starts the harness with it as FLOW_ID and that session
; id, and Bind verifies the harness came up as the flow reserved. A Codex
; launch reserves no FlowId; Bind claims it from the session Codex reports. Record writes one
; journal or lifecycle entry; Record.Harness appends the harness event a
; Report carried to the events Flow's Memory holds for that flow, and a
; flow Flow does not hold fails UnknownFlow and is never adopted.
; Record.Context writes the tokens a flow's native session carried into
; its last turn, read from its transcript when its hook reports Stopped.
; Register binds a flow's row and role. Confirm makes a Pending launch
; Active and records the Address its launch profile names Awake as it, in
; one write, and answers Started; an Address Awake as a live flow fails
; AddressAwake, an Ended one AddressEnded, and the launch stays Pending. Open makes the launch pane; Spawn starts
; the native harness in it. A Codex Spawn first opens the thread through
; the app-server with the system prompt as its base instructions and the
; launch's exclusions in its config, reads them back, and submits the first
; part of the first USER message as the thread's first turn; only then
; does the TUI attach to that thread, and Spawned names it; the thread is
; recorded for the launch request first, so a launch recovered after its
; start binds to it. A start Herdr
; refuses, or one Flow refuses before calling Herdr, fails SpawnRefused with
; its cause and, for Codex, the thread it had opened, archived. Open, a
; Codex thread's opening, a Spawn Flow did not attempt, Bind and Title fail
; LaunchRefused with the stage and the fixed category of the failure. Bind claims the
; flow's identity from the harness's integration report, and for Codex
; requires the thread Spawn opened; Title names the claimed flow; Submit
; types the next part of the first USER message once (the last part
; carries the brief), and for Codex first applies the exclusions to the
; attached thread again and reads them back, a first part being already in
; the thread; Close closes a flow's pane. Release gives back what
; Reserve took for a launch then refused: the held flow and its FlowId
; claim, answered Released.
;
; Sleep, Wake and Drain move a metaflow between Awake and Asleep so a seat
; that is not running keeps no harness. Sleep closes the pane of the flow a
; metaflow is awake as and records it Asleep (Record.Asleep), keeping the
; flow's native session so a later wake can resume it. Wake reads the whole
; queue of an Asleep metaflow, oldest first, and starts a seat that carries
; it in its first prompt: the last flow resumed when its session is under
; its layer's refresh threshold, else a fresh launch composed from the
; configured layer Model and the module identities the seat's last launch
; named. Record.Awoken then names the
; started flow and the count of queued requests it was handed, which leave
; the queue in that same write, so a wake that dies first loses nothing.
; Drain types the oldest queued request into the Awake flow's pane and
; removes it once typed, answering what it typed. Wake runs off the
; dispatch gate and takes it per step.
;
; Record.Refresh marks one Asleep metaflow so its next wake starts a fresh
; launch composed from the modules and leave-outs its last launch named,
; whatever its context size; the mark is a row of its own, keyed by the
; Address, and Record.Awoken retracts it in the write that records the wake.
; A mark already held is left as it is. It fails NotAsleep for a metaflow
; that is not Asleep.
;
; LaunchOutcome and Replacement are the store's own types, imported from
; the Nexus crate until the Memory root is compiled.

Operation
[ signal_flow:[ FlowId LaunchRequestId FlowNode Caller LaunchProfile ComposedLaunch Origin LaunchAttemptReservation HerdrPaneBinding NativeLaunchIntent NativeLaunchBinding RegistrationAcknowledgement PromptDeliveryIntent PromptDeliveryResult Launched Event Address Request QueuedRequest ContextRefusal LeaveOutRefusal NativeSessionId HarnessSpawnRefusal NativeLaunchRefusal ]
  flow_nexus:[ LaunchOutcome Replacement ] ]
[ Compose.LaunchProfile
  Reserve.{ ComposedLaunch Origin }
  Record.[ Intent.NativeLaunchIntent
           Binding.NativeLaunchBinding
           Acknowledgement.RegistrationAcknowledgement
           Delivery.PromptDeliveryIntent
           Delivered.PromptDeliveryResult
           Active.FlowId
           Stopped.FlowId
           Retired.FlowId
           Exited.FlowId
           Replacing.Replacement
           Withdrawn.LaunchRequestId
           Settled.{ LaunchRequestId LaunchOutcome }
           Harness.{ FlowId Event }
           Context.{ FlowId Tokens.Integer }
           Asleep.{ Address FlowId }
           Awoken.{ Address FlowId Delivered.Integer }
           Refresh.Address ]
  Register.{ FlowNode Caller }
  Confirm.FlowId
  Open.ComposedLaunch
  Spawn.PaneLaunch
  Bind.PaneLaunch
  Title.{ ComposedLaunch NativeLaunchBinding }
  Submit.{ ComposedLaunch PromptDeliveryIntent }
  Close.FlowNode
  Release.FlowId
  Sleep.{ Address FlowNode }
  Wake.Address
  Drain.Address ]
[ Composed.ComposedLaunch
  Reserved.{ LaunchAttemptReservation Option<FlowId> }
  Recorded
  Registered.FlowNode
  Started.Launched
  Opened.HerdrPaneBinding
  Spawned.Option<NativeSessionId>
  Bound.NativeLaunchBinding
  Titled
  Submitted.PromptDeliveryResult
  Closed
  Released
  Slept
  Woken.FlowId
  Drained.Vector<QueuedRequest>
  Failed.[ CompositionRefused
           StoreRefused
           ConflictingBinding
           Unstarted
           HerdrRefused
           CodexRefused
           UnknownFlow
           ClaimRefused
           NotAsleep
           NotAwake
           NothingQueued
           AddressAwake
           AddressEnded
           ContextRefused.ContextRefusal
           LeaveOutRefused.LeaveOutRefusal
           SpawnRefused.HarnessSpawnRefusal
           LaunchRefused.NativeLaunchRefusal ] ]
[ PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> Option<NativeSessionId> } ]
```

## signal-flow › ethos/signal.ethos

```ethos
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
; Start and Replace carry a LaunchProfile; a Replace's profile names the
; replaced flow as its predecessor. Neither carries its origin: the Nexus
; derives it from the calling process as Identify does (its pane's bound
; flow and that flow's native session), and a caller that is no bound flow,
; such as a deploy script, is an Unbound origin, recorded, never refused.
; A launch's power is its Address layer's and its harness is the one whose
; configured endpoint serves its model (Codex), else Claude; neither is
; named in the profile. The successor is launched; once it has
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
; Sender must name an existing Awake metaflow. The request is queued with
; that Sender (QueuedRequest.{ SentBy Request }), and a woken or drained
; flow reads each queued request with who sent it; a request queued before
; senders were kept reads SentBy Unknown. Unknown addresses are not
; created; an Asleep Sender is refused as Asleep and an Ended Sender as
; Ended.Address.
;
; Report carries one harness event of a flow Flow holds, sent by the
; harness's hook through the Flow CLI with the FlowId the flow was
; launched with. Flow stores the event in that flow's Memory and answers
; Reported. A FlowId Flow does not hold is refused, Refused.Unknown.FlowId,
; never adopted: a flow Flow did not launch is a flow Flow does not know.
;
; A LaunchProfile names the Address of the seat it launches. When the
; launch is confirmed, the Nexus records that Address's metaflow Awake as
; the launched flow, under the rules Bind applies: a metaflow Awake as a
; live flow is refused (AddressAwake), an Ended one is refused
; (AddressEnded), and an Asleep one, or one Awake as a flow no longer live,
; is taken over, a displaced flow joining Past. A replacement takes over
; the metaflow of the predecessor its profile names. A Start whose Address
; would be refused is refused before anything launches.
;
; Launched is what Start answers, carried by the Started reply; it was
; named Started until 9.0.0, when Event's Started took that name. It names
; the flow, its native session and the Herdr route it runs in (Available
; while its pane is held, Unavailable once it is gone), so the caller can
; register the seat with its messenger.
;
; A LaunchProfile names its seat's context only by module identity:
; SystemModules for the system prompt and UserModules for the first USER
; message. Flow has the context composer resolve those identities in the
; context repositories and verifies the answer; no path and no context
; text travels in a Start. The only text a Start carries is the seat's
; first brief, InstructionPrompt.
;
; The first USER message is the composed modules followed by the brief,
; sent once. When it does not fit one message it is split on module
; boundaries into PromptParts, each naming itself part k of n; the brief is
; in the last. A part after the first is sent only after the seat finished
; its answer to the one before. The durable PromptDeliveryIntent holds
; every part's SHA-256 in order, how many parts were submitted, and the
; count of Stop reports seen when the last one was. The receipt is every
; part observed in order as a user turn, then the seat's first answer at
; the intended model and effort.

Signal
[
  flow_ethos:[ Aspect Address FlowId Request SentBy QueuedRequest Lock Sender Process Metaflow Key Recipient Layer Topic Subaspect OrdinarySocketPath MetaSocketPath Start ModelName HarnessKind ] ]
[ Start.LaunchProfile
  Restart.FlowId
  ResolveRecipient.RecipientResolutionRequest
  Stop.FlowId
  Replace.LaunchProfile
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
  Metaflows ]
[ Started.Launched
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
  Refused.Refusal ]
[
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
  ModuleIdentity.String
  SystemModules.Vector<ModuleIdentity>
  UserModules.Vector<ModuleIdentity>
  Effort.String
  RememberingDepth.Integer
  SystemPromptText.String
  SystemPromptSha256.String
  InstructionPrompt.String
  FirstPromptBody.String
  PromptPartText.String
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
  PartsSubmitted.Integer
  StopsReported.Integer
  PowerLevel.[ High Medium Low UltraLow ]
  RememberedFlow.{ FlowId RememberingDepth }
  ; A leave-out names one part of a harness's start that a flow goes
  ; without: a tool or tool group, an instruction block, or a harness
  ; feature. Each turns into the harness's own flag, environment variable
  ; or setting. ToolSearch and BashTool are named so that leaving them out
  ; is refused: without ToolSearch every deferred tool's schema loads, and
  ; without Bash the flow cannot message, commit or build. SkillTool and
  ; BundledSkills are refused unless WorkflowTool is left out too, since
  ; Workflow then inlines its authoring reference. A Claude leave-out is
  ; refused for a Codex start, and a Codex one for a Claude start.
  LeaveOut.[ ClaudeAiConnectors ConfiguredMcpServers AgentTool ExplorePlanAgents FileTools WorkflowTool ScheduleWakeupTool ReportFindingsTool ListAgentsTool CronTools WebTools DeferredTools SkillTool BundledSkills ClaudeMd GitInstructions AttributionReminder UserSettings ToolSearch BashTool CodexSkillListing CodexAgentsMd CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ]
  LeaveOuts.Vector<LeaveOut>
  ; A Start's leave-outs, when it names them, replace the default its
  ; metaflow's configuration names; None takes that default.
  LaunchProfile.{ LaunchRequestId SystemModules UserModules Address ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName Option<LeaveOuts> InstructionPrompt }
  TargetReceiptRequest.{ LaunchRequestId PromptSha256 }
  PromptPart.{ PromptPartText PromptSha256 }
  FirstPromptPayload.{ FirstPromptBody PromptSha256 Vector<PromptPart> }
  SystemPrompt.{ SystemPromptText SystemPromptSha256 }
  ; The harness the Nexus derived for the launch's model, and the effective
  ; leave-outs: the Start's, else its metaflow's default.
  ComposedLaunch.{ LaunchProfile HarnessKind SystemPrompt FirstPromptPayload TargetReceiptRequest LeaveOuts }
  HerdrPaneBinding.{ LaunchRequestId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId }
  NativeLaunchIntent.{ LaunchRequestId PromptSha256 SystemPromptSha256 HarnessKind ModelName Effort Vector<PromptSha256> }
  NativeLaunchBinding.{ LaunchRequestId FlowId NativeSessionId HarnessKind HerdrPaneBinding }
  RegistrationAcknowledgement.{ LaunchRequestId FlowId NativeSessionId HerdrPaneBinding }
  NativeTranscriptCursor.{ NativeSessionId HarnessKind TranscriptDevice TranscriptInode TranscriptByteOffset TranscriptPrefixSha256 }
  NativeTranscriptAbsence.{ NativeSessionId HarnessKind TranscriptRootDevice TranscriptRootInode }
  NativeTranscriptBoundary.[ Existing.NativeTranscriptCursor
                             Absent.NativeTranscriptAbsence ]
  PromptDeliveryIntent.{ LaunchRequestId PromptSha256 FlowId NativeSessionId HarnessKind ModelName Effort Vector<PromptSha256> PartsSubmitted StopsReported LeaveOuts HerdrPaneBinding NativeTranscriptBoundary }
  NativeTargetReceipt.{ LaunchRequestId PromptSha256 FlowId NativeSessionId NativeTurnId ReceiptSha256 ModelName Effort Vector<PromptSha256> }
  PromptDeliveryResult.[ Observed.NativeTargetReceipt
                         Ambiguous.PromptDeliveryIntent ]
  LaunchAttemptPhase.[ Reserved NativeLaunchIntentRecorded NativeBound RegistrationAcknowledged PromptIntentRecorded PromptObserved PromptAmbiguous ]
  LaunchAttempt.{ LaunchRequestId LaunchProfile PromptSha256 Origin LaunchAttemptPhase Option<NativeLaunchIntent> Option<NativeLaunchBinding> Option<RegistrationAcknowledgement> Option<PromptDeliveryIntent> Option<PromptDeliveryResult> }
  LaunchStatusOutcome.[ Started.Launched Replaced.Replaced StartRejected.StartRejection ReplaceRejected.ReplaceRejection ]
  LaunchInspection.{ LaunchAttempt Option<LaunchStatusOutcome> Option<FlowNode> }
  LaunchAttemptReservation.[ Reserved.LaunchAttempt
                             Existing.LaunchAttempt
                             Conflict ]
  ; Where a launch or a flow came from: the bound flow that asked, with its
  ; native session, or Unbound for a caller that is no bound flow.
  FlowOrigin.{ FlowId SessionId }
  Origin.[ Flow.FlowOrigin Unbound ]
  RecipientResolutionRequest.FlowId
  StopRequest.FlowId
  RouteReadiness.[ Ready Parked ]
  EndpointSelection.[ Available.{ EndpointPath RouteReadiness }
                      Unavailable ]
  HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId }
  HerdrRouteSelection.[ Available.HerdrRoute
                        Unavailable ]
  FlowLifecycle.[ Pending Active Stopped Retired Exited ]
  FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection Origin FlowLifecycle }
  Launched.{ FlowId SessionId HerdrRouteSelection Origin }
  Restarted.{ FlowId SessionId Generation }
  ; BindingRefusal names one checked native-binding failure without raw adapter text.
  ; PaneMismatch covers the agent name, workspace, or pane check.
  ; TerminalMismatch covers the terminal check.
  ; HarnessMismatch covers the reported harness and official session source check.
  ; NotReady covers interactive readiness.
  ; ReservedIdentityMismatch covers selected, observed, or claimed identity conflicts.
  ; ClaimUnavailable covers Flow identity claim and claim readback failures.
  ; ObservationRefused covers a missing or malformed agent/session observation.
  ; TransportRefused covers the Herdr request or response transport boundary.
  ; Unclassified marks a stored v10 unit refusal whose stage was not kept.
  BindingRefusal.[ PaneMismatch TerminalMismatch HarnessMismatch NotReady ReservedIdentityMismatch ClaimUnavailable ObservationRefused TransportRefused Unclassified ]
  ; ContextRefusal names why a seat's context was not composed for its
  ; Start: the composer could not be reached or rejected the request; its
  ; answer named another metaflow; a payload's text differs from its
  ; SHA-256; a requested module is missing from the composed provenance;
  ; the system text exceeds one argument; or one module with its part
  ; header does not fit one message.
  ; LeaveOutRefusal names why a Start's effective leave-outs were refused:
  ; a part a flow cannot go without, a skill leave-out with Workflow kept,
  ; or a leave-out of the other harness.
  LeaveOutRefusal.[ Indispensable.LeaveOut NeedsWorkflowLeftOut.LeaveOut NotForHarness.LeaveOut ]
  ContextRefusal.[ ComposerUnavailable ComposerRejected MetaflowMismatch PayloadMismatch ModuleMissing SystemTooLarge ModuleTooLarge ]
  ; HerdrRefusal is Herdr's own answer to a refused agent start, kept whole:
  ; the error code and message of its JSON error body, or no code and the
  ; whole text Herdr printed when it printed no such body.
  HerdrErrorCode.String
  HerdrErrorMessage.String
  HerdrRefusal.{ Option<HerdrErrorCode> HerdrErrorMessage }
  ; SpawnRefusalCause names why the harness start in the launch pane was
  ; refused: Herdr refused it, or Flow refused it before Herdr was called
  ; because an argument carries a control character or the typed command
  ; is longer than one terminal line holds.
  SpawnRefusalCause.[ Herdr.HerdrRefusal ControlCharacter CommandTooLong ]
  ; OpenedThread accounts for the Codex thread Flow opened through the
  ; app-server before a refused harness start: its id, what its first turn
  ; had come to when the start was refused, and whether the app-server
  ; archived it.
  FirstTurn.[ Answered InProgress Unanswered Unread ]
  ThreadArchive.[ Archived ArchiveRefused ]
  OpenedThread.{ NativeSessionId FirstTurn ThreadArchive }
  HarnessSpawnRefusal.{ SpawnRefusalCause Option<OpenedThread> }
  ; NativeTargetRefusal names why Herdr's report of a launch pane is not the
  ; bound native target: Herdr could not be read, the pane is another one,
  ; a Claude pane reports no native session, or the reported harness or
  ; session is not exactly the one bound.
  NativeTargetRefusal.[ HerdrUnreadable PaneMismatch NoNativeSession IdentityInexact ]
  ; RegistrationRefusal names the stage at which a launched flow's
  ; registration was refused: its Herdr route was not verified under its
  ; FlowId claim; its row and role conflict with a flow Flow holds, or were
  ; not written; the pane binding belongs to another launch request; the
  ; acknowledgement is not the native binding; the composed first prompt is
  ; not canonical; the native target is not the one bound; the transcript
  ; boundary could not be captured; or a Codex transcript does not begin by
  ; naming the thread Flow opened. Unclassified marks a stored 18.0.0 unit
  ; refusal whose stage was not kept.
  RegistrationRefusal.[ RouteUnverified RoleConflict RoleUnrecorded PaneBindingForeign AcknowledgementMismatch PromptNotCanonical NativeTarget.NativeTargetRefusal TranscriptBoundary ThreadNotNamed Unclassified ]
  ; NativeLaunchStage names the step of a launch that failed once Flow had
  ; begun it natively: opening the launch pane, opening the Codex thread,
  ; starting the harness before Herdr was asked, binding the started
  ; harness, naming the claimed flow (its title), reading the launch
  ; receipt, or confirming the received flow Active. Unclassified, in stage
  ; and category, marks a stored 18.0.0 unit refusal whose stage was not
  ; kept.
  NativeLaunchStage.[ Open CodexThread Spawn Bind Naming Receipt Confirm Unclassified ]
  ; NativeLaunchFailure is the fixed category of that failure; no adapter
  ; text is carried. The receipt's own: the transcript boundary is not the
  ; intent's, the Codex transcript does not begin by naming the thread
  ; bound, a user turn differs from the startup parts, the session shows a
  ; part its leave-outs removed, or the model or effort differs from the
  ; intent. The confirmation's own: the received flow is not held with its
  ; native session. SendToolUnsupported, at CodexThread: the Codex
  ; app-server was not shown to accept Flow's send tool behind its
  ; experimental API, so no thread was opened.
  NativeLaunchFailure.[ PaneTargetMismatch NativeSessionMissing NativeIdentityConflict FlowClaimUnavailable HarnessMismatch HerdrUnreadable ForeignBinding InvalidFlowId NotReady TranscriptUnreadable TitleReadbackDiffers CodexNamingRefused PaneLabelRefused AdapterRefused BoundaryMismatch ThreadNotNamed PartDiffers LeaveOutShown ModelOrEffortDiffers SessionUnrecorded Unclassified SendToolUnsupported ]
  NativeLaunchRefusal.{ NativeLaunchStage NativeLaunchFailure }
  ; StartRejection preserves a typed BindingRefused result at the public wire.
  ; AddressAwake: the profile's Address is Awake as a live flow, or another
  ; unsettled launch names it. AddressEnded: the Address was ended.
  ; NativeLaunchRefused: a native step of the launch failed, at its stage.
  ; RegistrationRefused: the started flow was not registered, at its stage.
  ; HarnessSpawnRefused: the harness start itself was refused.
  StartRejection.[ CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused.NativeLaunchRefusal BindingRefused.BindingRefusal RegistrationRefused.RegistrationRefusal IntentPersistenceRefused OriginUnavailable AddressAwake AddressEnded ContextRefused.ContextRefusal LeaveOutRefused.LeaveOutRefusal HarnessSpawnRefused.HarnessSpawnRefusal ]
  RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ]
  RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ]
  StopRejection.[ UnknownFlow AlreadyStopped RouteUnavailable CloseRefused PersistenceRefused ]
  Replaced.{ FlowId Launched }
  ReplaceRejection.[ PredecessorAbsent
                     UnknownPredecessor
                     PredecessorStopped
                     LaunchRefused.StartRejection
                     ReapRefused.StopRejection ]
  ObserveSelection.[ Launch.LaunchRequestId
                     Agent.FlowId ]
  AgentState.[ Idle Working Blocked Done Unknown Gone ]
  AgentObservation.{ FlowId AgentState }
  LaunchStatusRejection.[ UnknownLaunchRequest PersistenceRefused ReadViewChanged InconsistentRecords ]
  Caller.{ FlowId Aspect PowerLevel ModelName }
  CallerResolutionRejection.[ CallerUnknown
                              CallerMismatch.Caller ]
  Title.String
  Presentation.{ Title }
  TranscriptPath.String
  TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }
  TurnEndRejection.[ UnknownSession SessionMismatch InvalidTurnId InvalidTranscriptPath QueueRefused ]
  Refusal.[ Locked
            Held.Lock
            Awake.FlowId
            Asleep
            Lapsed
            Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ]
            NoLayer
            NotConfigured
            Ended.Address
            OffRoute
            NoneAbove
            NotMessage
            Taken.Address
            Unidentified.Process
            Store.String ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
```

### Proposal 6: A struct has no head in Datom, the walk's Flow line · psyche-context › vision/nexus.md

```datom
  ; 3 the Change Operation hands Memory
- Flow.{ 7 { Psyche core Primary } Running
-        [ Started ] }
+ { 7 { Psyche core Primary } Running
+   [ Started ] }
```

Ruling: land, amend, or reject.

### Proposal 7: FlowId as a String, as the code has it · psyche-context › vision/nexus.md

```ethos
  Library
  []
- [ FlowId.Integer
+ [ FlowId.String
  Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
  Address.{ Aspect Topic Layer }
  Event.[ Started Stopped ] ]
  []
  []
```

```datom
  ; 3 the Change Operation hands Memory
- { 7 { Psyche core Primary } Running
+ { a1b2c3 { Psyche core Primary } Running
    [ Started ] }
  ; 4 Memory's answer to Operation
  Succeeded
  ; 5 Outcome
- Started.7
+ Started.a1b2c3
  ; 6 Response, from Signal's answer, to the CLI
- Launched.7
+ Launched.a1b2c3
```

Ruling: land, amend, or reject.

### Proposal 8: Event with ToolUsed, as the code has it · psyche-context › vision/nexus.md

```ethos
  Library
  []
  [ FlowId.Integer
  Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
  Address.{ Aspect Topic Layer }
- Event.[ Started Stopped ] ]
+ Event.[ Started
+         ToolUsed.String
+         Stopped ] ]
  []
  []
```

Ruling: land, amend, or reject.

### Proposal 9: Said and Request in the Library, as the code has them · psyche-context › vision/nexus.md

```ethos
  Library
  []
  [ FlowId.Integer
  Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
  Address.{ Aspect Topic Layer }
- Event.[ Started Stopped ] ]
+ Event.[ Started Stopped ]
+ Said.{ Context.String Verbatim.String }
+ Request.[ Order.String
+           Question.String
+           Psyche.Said
+           Psyches.Vector<Said>
+           Result.String
+           Notice.String ] ]
  []
  []
```

Ruling: land, amend, or reject.

### Proposal 10: Metaflow in Memory, as the code has it · psyche-context › vision/nexus.md

```ethos
  Memory
- [ flow:[ FlowId Address Event ] ]
+ [ flow:[ FlowId Address Event Request ] ]
  [ Flow.{ FlowId Address
         State.[ Running Ended ]
         Vector<Event> }
+ Metaflow.{ Address
+            MetaflowState.[ Awake.FlowId
+                            Asleep
+                            Ended ]
+            Past.Vector<FlowId>
+            Queue.Vector<Request> }
  Answer.[ Succeeded Failed ] ]
```

```datom
+ ; 3b the Metaflow Memory holds for the address
+ { { Psyche core Primary } Awake.7
+   [ 4 5 ]
+   [ Order.«Check the build» ] }
```

```
+--------------------+
| Memory             |
+--------------------+
      |           |
      | holds     | would hold
      v           v
+-----------+ +--------------+
| Flow      | | Metaflow     |
| (stands)  | | (proposed)   |
+-----------+ +--------------+
                    |
                    | queues
                    v
              +-----------+
              | Request   |
              | (proposed)|
              +-----------+
```

Ruling: land, amend, or reject.

### Proposal 11: A knowledge module for the Flow Nexus ethos · mind-context › knowledge/flow-nexus-ethos.md, a new file

+ ---
+ description: A type, field or variant of the Flow Nexus ethos is read, written or judged against what each is for.
+ dependencies: [vision-nexus, vision-flow, vision-ethos]
+ ---
+
+ The Flow Nexus ethos is four files in psyche-context vision/nexus.md, one main object each: Library, Signal, Operation, Memory. Code compared: flow 0.35.11 (67b80b3) and signal-flow (6a49664), as origin main has them.
+
+ ## Library
+
+ - FlowId: names one flow in Report, Launched, Started, Record and the Memory record Flow. Vision nexus: Integer. Code: String. Vision flow: the hash of the harness session id, six characters.
+ - Topic: a metaflow's topic, a camelCase word, core by default. String in vision and code; the camelCase check is made at input because ethos-zero 16 cannot express it. Whether it becomes an open enum is unruled.
+ - Aspect: Psyche, Mind or Field. The same in code.
+ - Layer: Primary, Secondary, Tertiary or Quaternary; the layer decides the model. The same in code.
+ - Address: `{ Aspect Topic Layer }`, in that field order, the address of a metaflow. What Launch, Start and Flow name is a metaflow, never a flow. It replaced Voice `{ Aspect Layer }` in 6c8e266. The same in code.
+ - Event: a lifecycle event of a flow, Started or Stopped. Code adds `ToolUsed.String` between them.
+
+ ## Signal
+
+ - Launch `{ Address Brief.String }`: asks Flow to start a flow for the metaflow at Address; Brief is a small paragraph. Vision flow says a launch also names the context modules; the query has no field for them. Code: `Start.LaunchProfile`, which carries SystemModules, UserModules, Address, ModelName, Effort and InstructionPrompt.
+ - Report `{ FlowId Event }`: a harness event of a flow, reported by a hook calling the Flow CLI. The same name and fields in code.
+ - Launched.FlowId: the answer to Launch, the new flow's id. Code: `Started.Launched`, a struct of FlowId, SessionId, HerdrRouteSelection and Origin.
+ - Refused: Launch was refused. NoCapsule: no place for the flow to run. AddressBusy.Address: the metaflow at that address is taken. Code has neither; its StartRejection has AddressAwake and AddressEnded.
+ - Reported: Report was accepted. The same in code.
+ - The vision has no meta Signal; code has one, in meta-signal-flow.
+
+ ## Operation
+
+ - Start `{ Address Capsule }`: starts the flow at Address in Capsule. Code has no Start operation; its operations are Compose, Reserve, Record, Register, Confirm, Open, Spawn, Bind, Title, Submit, Close, Release, Sleep, Wake and Drain.
+ - Record `{ FlowId Event }`: stores an event for a flow. Code: `Record.Harness.{ FlowId Event }` carries the same pair among seventeen kinds of record.
+ - Started.FlowId: the outcome of Start. Recorded: the outcome of Record.
+ - Failed: CapsuleRefused, the capsule was refused; StoreRefused, Memory refused the write. Code: seventeen variants, StoreRefused among them.
+ - Capsule `{ Home.String Login.Vector<String> }`: where a flow runs. The vision defines neither string; vision flow says the first capsule copies only the credential files. Code has no Capsule.
+
+ ## Memory
+
+ - Flow `{ FlowId Address State.[ Running Ended ] Vector<Event> }`: one flow's record: its id, the address of its metaflow, whether it runs or has ended, its events in order. The generated Rust fields are named after their types: flow_id, address, state, event_vector.
+ - Answer: Succeeded or Failed, Memory's answer to an operation, as vision nexus says memory answers that the change succeeded or failed. Added beside Flow in 6c8e266. Code has no Answer.
+ - Metaflow: not in the vision's Memory. In code's Library: `{ Address State.[ Awake.FlowId Asleep Ended ] Past.Vector<FlowId> Queue.Vector<QueuedRequest> }`; its store keeps flows and metaflows in separate tables.
+ - Code has no Memory ethos file: its store is Rust, in flow-nexus store.rs. Its flow lifecycle is Pending, Active, Stopped, Retired, Exited.
+
+ ## The variant as a field
+
+ - A variant declared where a field stands, `State.[ Running Ended ]`, is the declaration and the field at once. In Datom it is written bare, `Running`. The living kept this form on 2026-10-19 because it has less noise.
+ - A type is declared once per file: a second State in the same file is refused, `Duplicate.State`.
+
+ ## Datom
+
+ - A struct has no head in Datom: Flow is `{ 7 { Psyche core Primary } Running [ Started ] }`. The headed `Flow.{ ... }` is refused: expected Struct, found Variant.
+ - An enum variant has its head: `Launch.{ ... }`, `Start.{ ... }`, `Started.7`, `Launched.7`, `Succeeded`.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
