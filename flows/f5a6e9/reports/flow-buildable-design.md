# Flow Nexus, buildable design

For Mind and Field. Assembled from the books of flow
f5a6e9, newest edition winning: 17, 18 (the Nexus
starts), 15, 11, 14, 10, 3, 1 (background only), and
the speech across aspects book. Status of each ruling
is in section 4; nothing here is landed in a skill.

## 1. Ethos

One Library, two Signals, one Memory. Layout is the
canonical vertical three-space form.

### Library

```
Library                         ; Flow's
[  meta_signal_flow:[           ; at the revision
      CodexEndpoint             ; Flow pins
      HarnessProfile            ; (88f37592), as
      FlowAspect ] ]            ; the meta socket
[  FlowId.String                ; unideal now: a
                                ; real id built on
                                ; the hash bits that
                                ; identify a flow
   Topic:Name                   ; inline import of
                                ; a core built-in:
                                ; camelCase, checked
                                ; where text enters
   Blake3.Bytes<32>             ; Encodable: hex
   Layer.[                      ; decides the model
      Primary
      Secondary
      Tertiary
      Quaternary ]
   Subaspect.[                  ; a module's kind
      Vision
      Intent
      Knowledge
      Operation
      Trial
      Compensation ]
   Source.{                     ; where a module's
      Repository.String         ; text lives: the
      Hash.Blake3               ; containing source,
      Path.String }             ; hashed, relative
   Path.String                  ; a path relative to
                                ; a source
   Key.{                        ; a module's key,
      Subaspect                 ; written as the
      Topic }                   ; pair
                                ; { Vision flow }
   Said.{                       ; his words, relayed
      Context.String            ; where it was said
      Verbatim.String }         ; the words whole
   Request.[                    ; reaches a flow
      Order.String              ; wakes
      Question.String           ; wakes
      Psyche.Said               ; wakes; the variant
                                ; carries the type
      Psyches.Vector<Said>      ; wakes
      Result.String             ; a flow's answer:
                                ; delivered awake,
                                ; waits asleep
      Notice.String ]           ; wakes nothing
   Aspect.[                     ; whose psyche it
      Psyche                    ; serves
      Mind
      Field ]
   Address.{                    ; names a metaflow,
      Aspect                    ; written short:
      Topic                     ; { Psyche flow
      Layer }                   ; Primary }
   Recipient.[ Address Up ]     ; Up: same topic,
                                ; one layer above
                                ; the sender, in its
                                ; aspect
   Metaflow.{                   ; one per address
      Address
      State.[
         Awake.FlowId           ; its current flow
         Asleep                 ; a request wakes it
         Ended ]
      Past.Vector<FlowId>       ; the last few only,
                                ; oldest first
      Queue.Vector<Request> }   ; waiting, oldest
                                ; first
   Lock.{                       ; one per metaflow,
      Sender                    ; resolved address
      Address                   ; while held
      Until.Integer }           ; seconds since the
                                ; epoch; lapses
   Process.{                    ; the calling
      Pid.Integer               ; process
      Started.Integer }         ; the kernel's start
                                ; time of that pid,
                                ; so a reused pid is
                                ; told apart
   Sender.Address
   Start.{                      ; the one datom
      OrdinarySocketPath.String ; argument of the
      MetaSocketPath.String     ; Nexus's start
      StorePath.String }        ; command
   Nexus.{                      ; the Nexus's own
      SourceRoot.String         ; setup payload
      StableCodex.CodexEndpoint
      NextCodex.CodexEndpoint
      HarnessProfiles.Vector<HarnessProfile>
      MetaAspects.Vector<FlowAspect>
      MessageNexusPath.String   ; Message's
                                ; ordinary socket
      MessageNexusBinary.String  ; store path of
                                ; the Message
                                ; Nexus binary
      Lease.Integer } ]         ; seconds; 60
                                ; before any Nexus
                                ; payload
[]
[]
```

The Library declares once the types both Signals and
Memory use: Said, Aspect, Address, Metaflow, Lock,
Process, Sender, Key, Start and Nexus. Memory and both
Signals import them (status: current best, not before
the living).

Flow's two listening sockets, the ordinary socket and
the meta socket, and the store path come from its start
command, `flow-nexus 'Start.{ … }'`, whose one datom
argument is Start. No environment variable and no
derived default names the store path. At Start, a
missing store file is created; one Flow recognises as
its own (its Memory schema, with the schema's version
written in the file at creation) is opened and
continued from; anything else at StorePath, an old
0.14 store included, refuses to start, the refusal a
datom on standard output, Refused.Store.{ Path.String
Reason.String }, with a non-zero exit so the unit
records it (current best).

The Nexus payload's type is declared once, here, as
Nexus. It carries no socket path. MessageNexusPath is
the Message Nexus's ordinary socket path. Lease is the
lock's span in seconds; Flow runs with 60 before any
Nexus payload (current best).

Build note. ethos-zero 16.0.0 cannot yet express
`Topic:Name` (the inline import, the Ethos topic's)
nor `Bytes<32>` (the intrinsic proposed in «Stored
type and datom form», second edition). Until ethos
can, the build carries `Topic.String`, checked as a
camelCase expression where text enters, and
`Blake3.String` as 64 hex characters, each with a
comment naming the designed type. The design stays
as written above (status: current best, not before
the living).

Encodable, the trait behind Blake3 (vision-datom):

```
Encodable.[
   encode.String        ; the bare run
   decode:{
      [ Textualizable ] ; the run read
      [ Result<Self Error> ] } ]
```

A type bearing Encodable is one bare run in datom,
bytes in memory, no positions. datom-codec gives it
Datomizable and Composing from the two functions.
The Nexus holds the bytes and compares, hashes and
orders them. Bytes<N> is an intrinsic name, N bytes,
copied, ordered, hashed.

A request is one layer of variants. A Said carries
his words and their context, nothing of the relaying
flow. Delivered as one vector, oldest first, the
waking request last:

```
[  Notice.«branch flowRefresh merged»
   Result.«tests pass on the pushed revision»
   Order.«bring the refresh to production» ]
```

### Memory

```
Memory                          ; Flow's
[  flow_ethos:[ FlowId Layer Key
                Source Process ]
   meta_signal_flow:[ HarnessKind ]
   signal_flow:[ Event ] ]
[  Flow.{                       ; one per run
      FlowId
      Session.String            ; the harness's id
      Process                   ; the calling
                                ; process's pid and
                                ; start time learned
                                ; at spawn or bind
      Events.Vector<Event> }    ; signal-flow's
   Module.{                     ; the registry: one
      Key                       ; per key
      Source
      Checked.Boolean }         ; false until its
                                ; first compose
                                ; checks the hash
   Model.{                      ; one per layer
      Layer
      Harness.HarnessKind       ; how it is driven
      Native.String }           ; the model's name
                                ; as the harness
                                ; knows it
   Metaflow.flow_ethos:Metaflow ; ethos-zero's form
                                ; for a record
                                ; naming a Library
                                ; type
   Lock.flow_ethos:Lock         ; likewise
   Nexus.flow_ethos:Nexus       ; the Nexus payload
                                ; stored once
   Threshold.{                  ; one per layer
      Layer
      Handover.Integer
      Refresh.Integer } ]
```

Module, Model and Threshold hold what the meta socket's
Configure sets. A Module is a Key and a Source (current
best). Checked.Boolean is the Memory record's field
alone, false until the first compose checks the hash.
The Library's Lock is stored one per metaflow while
held. The Flow record's Process holds the calling
process's pid and start time, learned at spawn or at
Bind (status: current best, not before the living).

Event is imported from signal-flow: Started,
ToolUsed.String, ContextMeasured.{ Tokens.Integer
Window.Integer }, Stopped. In this build signal-flow
gains ContextMeasured.{ Tokens.Integer Window.Integer }
(current best).

Written, two metaflows:

```
{
   { Psyche core Primary }
   Awake.startInputVital
   [ zooWrongYouth ]
   [ ] }

{
   { Mind flowRefresh Secondary }
   Asleep
   [ ]
   [ Notice.«branch merged» ] }
```

A thread's title is the address written short, then
the flow's words, never the model:
`{ Psyche flow Primary } startInputVital`.

### Signal, the flow socket

```
Signal                          ; what Flow is asked
[  flow_ethos:[ Address FlowId Request Lock
                Sender Recipient Process Key
                Metaflow ]
   signal_flow:[ Event ] ]
[  Launch.{                     ; a metaflow's first
      Address                   ; flow; the address
      Modules.Vector<Key>       ; written short
      Brief.String }            ; a small paragraph
   Wake.{                       ; a sleeping
      Address                   ; metaflow's next
      Request }                 ; the waking request
   Refresh.Address              ; the next link
   End.Address
   Current.Address
   Bind.{                       ; a running process
      Address                   ; becomes this
      Process }                 ; metaflow's flow
   Lock.{                       ; Message asks; time
      Sender                    ; bound
      Recipient }
   Identify.Process             ; who is the caller
   Deliver.{                    ; under the lock
      Lock                      ; sender in lock
      Request }
   Release.Lock
   Report.{                     ; the hook's request
      FlowId
      Event }
   Observe.Agent.FlowId         ; carries Herdr's
                                ; agent state
   Stop.FlowId                  ; reap, no
                                ; successor
   Metaflows ]                  ; list them all
[  Launched.FlowId
   Refreshed.{
      FlowId                    ; the successor
      FlowId }                  ; the predecessor
   Ended
   Current.[
      Awake.FlowId
      Asleep
      Ended
      Unknown ]
   Bound.FlowId                 ; the flow reserved
   Locked.Lock                  ; carries the
                                ; resolved Address
   Identified.Address           ; the caller's
   Delivered                    ; placed in the
                                ; awake flow
   Queued                       ; asleep, or awake
                                ; and busy: waits
   Woken.FlowId                 ; asleep: woken; the
                                ; queue drained with
                                ; the first prompt
   Released
   Reported
   Observed.Agent.[             ; Herdr's agent
      Working                   ; states as it
      Idle                      ; reports them
      Done
      Absent ]
   Stopped
   Listed.Vector<Metaflow>
   Refused.[
      Locked                    ; refresh under way
      Held.Lock                 ; lock held: also
                                ; Refresh and End
      Awake.FlowId              ; Launch of an awake
                                ; metaflow: its
                                ; current flow
      Asleep                    ; Refresh of a
                                ; sleeper
      Lapsed                    ; a granted lock
                                ; that ran out
      Unknown.[                 ; each inner variant
                                ; carries its type
         Address                ; no such metaflow;
                                ; a Sender or an Up
                                ; target naming none
         Lock                   ; never granted, or
                                ; already consumed
         FlowId                 ; Report, Stop or
                                ; Observe.Agent
         Key ]                  ; module missing
                                ; from registry or
                                ; Forget, or from
                                ; Launch if module
                                ; in Launch is missing
      NoLayer                    ; no Model for the
                                ; layer; at Launch,
                                ; and at Lock or
                                ; Deliver for an
                                ; asleep recipient
      NotConfigured             ; Launch before
                                ; Configure.Nexus
      HashMismatch              ; a module recorded
                                ; unchecked fails
                                ; its hash at its
                                ; first compose
      Ended.Address             ; Wake, Lock,
                                ; Deliver, Refresh
                                ; or End of an Ended
                                ; metaflow
      OffRoute                  ; at Lock: sender,
                                ; recipient aspect,
                                ; layer, topic off
                                ; the vision-aspects
                                ; routes
      NoneAbove                 ; Up above Primary
      NotMessage                ; Bind, Lock,
                                ; Deliver or Release
                                ; from not-bound peer
                                ; (not Identify,
                                ; which any local peer
                                ; may ask)
      Unidentified.Process      ; Identify: in no
                                ; metaflow; Bind: a
                                ; dead or reused
                                ; process
      Taken.Address              ; Bind: the old
                                ; process lives
      Store.String ]             ; the store failed;
                                ; its own error text
[]
```

Identify and the Deliver responses and refusals above
are current best, not before the living. Also current
best: Launch of an awake metaflow is Refused.Awake.FlowId
and Refresh of an asleep one Refused.Asleep; Refresh or
End under a held lock is Refused.Held.Lock. The flow
socket has one Unknown.[ Address Lock FlowId Key ],
each inner variant carrying its type (current best).
Unknown.FlowId answers Report, Stop and Observe.Agent
of an unknown flow. Lapsed answers a granted lock that
ran out; Unknown.Lock answers a lock never granted or
already consumed. A Sender whose address names no
metaflow, or an Up whose target names no metaflow, is
Unknown.Address; NoneAbove is only for an Up above
Primary. Wake, Lock, Deliver, Refresh and End
of an Ended metaflow are all refused
Refused.Ended.Address (current best). Report,
Observe.Agent, Stop and Metaflows, with Reported,
Observed.Agent, Stopped and Listed, are current best:
Report is the hook's request, Stop reaps a flow with no
successor, and Observe.Agent.FlowId and
Observed.Agent.[ Working Idle Done Absent ] are named
here because the Flow 0.25.0 payload is unknown to this
design; Observed carries Herdr's agent states as it
reports them.

Bind, Bound.FlowId, Taken.Address and
Unidentified.Process for a Bind are on the ordinary
socket: a process binding itself is ordinary work
(current best).

Written, a launch of this flow:

```
Launch.{
   { Psyche flow Primary }      ; written short
   [ { Vision flow }
     { Knowledge ethos } ]
   «Design Flow's module registry.» }
```

### Signal, the meta socket

```
Signal                          ; the meta socket
[  flow_ethos:[ Layer Key Source Path
                Nexus ]
   meta_signal_flow:[           ; meta-signal-flow
      CodexEndpoint             ; at the revision
      HarnessKind               ; Flow pins
      HarnessProfile            ; (88f37592);
      FlowAspect ] ]            ;
                                ; FlowAspect and the
                                ; Library's Aspect
                                ; name the same
                                ; three; the
                                ; duplicate goes
                                ; when the Library
                                ; lands in code
[  Configure.[
      Module.{                  ; the registry: one
         Key                    ; per key
         Source }
      Model.{                   ; the layer's model
         Layer
         Harness.HarnessKind    ; how it is driven
         Native.String }        ; the model's name
                                ; as the harness
                                ; knows it
      Threshold.{               ; percent of window
         Layer
         Handover.Integer       ; 20
         Refresh.Integer }      ; 40
      Nexus ]                   ; the Library's: the
                                ; Nexus's own setup
   Forget.Key                   ; a module leaves
   Configuration ]              ; what is set
[  Configured
   Forgotten
   Configuration.{              ; the runner values
      Nexus
      Models.Vector<Model>
      Thresholds.Vector<Threshold>
      Modules.Vector<Module> }
   Unconfigured                 ; no Nexus payload
                                ; yet
   Refused.[
      NoSource.Path
      HashMismatch
      Conflict                  ; Nexus payloads
                                ; that disagree in
                                ; one start
      Unknown.Key                ; Forget of an
                                ; unknown key
      Store.String ]             ; the store failed;
                                ; its own error text
                                ; unknown key
[]
```

Configure.Nexus carries no socket path (current best).
Configuration takes no payload and answers
Configuration, or Unconfigured before any Nexus
payload; Field reads the runner values from it
(current best).

Printed forms. Responses print in datom's canonical
form: entries in insertion order (first bound first),
an empty vector as [], one space inside every bracket
and brace. Written, with one entry each:

```
Listed.[
   { { Psyche core Primary }
     Awake.startInputVital
     [ zooWrongYouth ]
     [] } ]

Configuration.{
   <nexus>
   [ { Primary Claude opus } ]
   [ { Primary 20 40 } ]
   [ { { Vision flow }
       { psyche-skills
         <hash>
         vision/flow.md }
       false } ] }

Unconfigured
```

Model and Threshold values are illustrative above.
HarnessKind's variants are meta-signal-flow's.

Unconfigured prints bare.

Order (current best). Model and Module are accepted
before any Nexus payload, in any order. Configure.Nexus
must arrive before any Launch, which otherwise is
refused NotConfigured; a Launch before its Model or
Module is refused NoLayer or Unknown.Key.
Configure.Nexus is needed for Bind under the Message
address, but not for Lock, Deliver, Release or
Identify. A Module arriving before Configure.Nexus is
recorded unchecked; its hash is checked at its first
compose into a launch, and a mismatch refuses that
Launch with HashMismatch. A changed Model or Threshold
for a layer already set is an update, answered
Configured; Conflict is only for Nexus payloads that
disagree within one start.

Written, one Module of psyche-skills:

```
{  { Vision flow }
   { psyche-skills
     <hash>
     vision/flow.md }
   false }
```

A Key is written as the pair, { Vision flow }; Forget
takes a Key, and an unknown one is refused Unknown.Key
(current best).

Configuration lives in datom files in the repositories
that own it, one file per concern. The CLI sends them
in succession over the meta socket; nothing is expanded
across files. Each payload lands whole or is refused
whole. Payloads go in succession, each whole, and
flow-meta's composing of fragments ends. The same Key
with a new hash is an update, answered Configured. A
module is found by its Key; its source file is at
SourceRoot/Repository/Path, Repository being the
checkout's directory under SourceRoot, Hash the blake3
of that file, checked on a read or a write. The Nexus composes from the registry
and reads no path a caller writes.

### Message's simple and extended forms

Defined in Signal as types of their own, nothing
omitted from either; shown here for the lock.

```
[  Send.{                       ; simple: what a
      Address                   ; flow writes
      Request }
   Deliver.{                    ; extended: Message
      Lock                      ; to Flow, under the
      Request }                 ; sender in lock
]
```

The simple form carries what its use needs and is what
the common queries use, above all in a machine's
context; it names the metaflow, never a flow id. The
extended form carries every parameter and serves
debugging and components. Lock is the Memory record.

## 2. Rules

LaunchStatus is replaced by Current and the Flow
record's Events. Observe.Launch, QueueTurnEnd, Restart
and ResolveRecipient are removed on purpose.
ResolveCaller is Identify (current best).

**How a flow starts.** A launch names a metaflow by
its address, the flow's own modules, and a
small-paragraph brief. Flow composes the system prompt
and the first prompt from the module registry and the
layer's model; a few module names call a whole context
because naming a module loads its dependency chain,
so ninety-five percent or more of a flow's context
comes from modules and the brief stays small. Flow
reserves the flow id, writing the metaflow record
before any harness runs (identity is a field of the
request, not read off a title or a model); opens the
pane; spawns the harness; binds the flow to the session
the harness reports; titles it; submits the first
prompt once. The hook reports Report.{ FlowId Started }
at the harness's session start; it learns its FlowId
from the environment Flow sets in the pane at spawn
(the FlowId reserved before the harness ran). The
session id is bound as today: chosen by Flow at
reserve for Claude, reported by Codex's app-server at
bind. HarnessProfile carries how a kind is driven, one
per kind. A new flow's
first response is a presentation of its context in its
role. A wake launches the same way, the drained queue
delivered with the first prompt, the waking request
last.

**The waking rule and the queue.** Every topic has one
metaflow, answering for the whole topic, even across
several skills. Flow keeps its queue. By state: Awake,
the request is delivered now; a Launch of an awake
metaflow is refused Awake.FlowId, naming its current
flow (current best). Asleep, an order, a
question, a psyche or psyches wakes it; a result or a
notice waits in the queue and wakes nothing. Ended,
the request is refused Refused.Ended.Address.
Wake of an awake metaflow is Queued, and the
queue drains at its next
Stop (current best). Refresh of an asleep metaflow is
refused Asleep; Refresh or End while a lock is held is
refused Held.Lock (current best). A waking request drains
the queue: all waiting requests are delivered oldest
first as one vector typed by variant, the waking
request last, with the first prompt of the spawned
flow. A metaflow satisfied with its topic sleeps until
a request changes what it must do. Where a request
lands in an already awake flow is open (section 4).
When the awake flow cannot take it now (it is working,
or its composer is occupied), Flow queues the request,
answers Queued, and drains the queue at the next Stop
the hook reports (status: current best, not before the
living).

**Stop and pane closure.** Stop, or a pane closed
under a flow, moves that flow's id into the
metaflow's Past (the last few kept, oldest first)
and the metaflow becomes Asleep (current best).

**End.** End moves the current flow's id into Past
and empties the queue, so an ended metaflow reads
Ended with that id in Past and an empty queue
(current best).

**The refresh.** Measurement: the hook reads the
transcript at each Stop and reports ContextMeasured,
the sum of the last assistant usage's three input
counts (fresh, cache written, cache read), against the
model's window from the harness catalog. Thresholds
are percent of the window, per layer, from Configure:
Handover 20, Refresh 40. At the first the flow is told
to write its handover; at the second, or at the Stop
after the handover is written, Flow refreshes. No model
decides any step. Steps: lock the metaflow on the
successor; compose from the layer's model, the launch's
modules and the predecessor's handover as the brief;
reserve, open, spawn, bind, title, submit; reap the
predecessor; set the successor awake and append the
predecessor to Past (the last few only); unlock. The
handover is a small paragraph: only what is still
undecided passes; what was decided went into modules.

**The lock.** Message asks Flow for a lock with
Lock.{ Sender Recipient }, bounded in time; Flow
answers Locked.Lock, the Library's Lock.{ Sender
Address Until }, carrying the resolved Address. With
the lock Message hands Flow the request as Deliver.{
Lock Request }, and Flow places it by the waking rule.
What reaches a flow is a request, never a letter; Flow
holds no messages beyond a queue of requests. While a
refresh is under way the metaflow is locked and a lock
request is refused Locked; a held lock refuses
Held.Lock.
Message speaks in metaflows and need not know flows.
Flow resolves Up from the sender's identified address
and includes it in the returned lock. Up is the same
topic, one layer above, within the sender's aspect;
above Primary it is refused NoneAbove. A Sender, or an
Up target, naming no metaflow is refused
Unknown.Address. A Sender whose metaflow is Asleep is
refused Refused.Asleep; one whose metaflow is Ended is
refused Refused.Ended.Address. At Lock, a Recipient
address naming no metaflow is refused Unknown.Address;
an Asleep recipient is granted; an Ended recipient is
refused Refused.Ended.Address. When the recipient is
Asleep, Lock checks the wake's preconditions before
granting: a Model for the recipient's layer, the
registry's modules for its topic composing whatever
exists, an empty set included; a wake composes from
whatever
the registry holds for the recipient's topic, and none
is a valid set, so a metaflow with no registered
module wakes with no modules and no refusal names a
missing one. If not, Lock or Deliver refuses NoLayer.
If the configuration changes between Lock and Deliver,
Deliver answers the same refusal, never Queued. The
lock's span is the Lease of the Nexus payload, in
seconds; Flow runs with 60 before any Nexus payload.
A lock ends by Deliver (one delivery per lock),
Release, lapse, or a refusal at Deliver. A granted
lock that ran out is refused Lapsed; one never granted
or already consumed is refused Unknown.Lock. OffRoute
is refused at Lock; Deliver trusts its lock. Trust at
Lock rests on the gate; Flow does not re-check the
sender's process. Stop leaves the metaflow Asleep;
only End ends it. At Deliver, Flow checks in this
order — the gate (NotMessage), then the lock
(Unknown.Lock, then Lapsed), and only a live lock
reaches the recipient's state (Ended.Address, then
NoLayer for a wake, then Delivered,
Queued or Woken) — so a lapsed lock on an ended
recipient answers Lapsed (current best). Status:
current best, not before the living.

**The Message gate.** Flow re-checks the peer's
executable against MessageNexusBinary, both
resolved to canonical paths, on every Lock,
Deliver and Release, beside the pid and start
time; a mismatch refuses NotMessage and drops
the binding, so Message must Bind again.
Message binds its process at its start with
Bind.{ Address Process } under { Field message
Primary }, a Nexus being Field's body (status:
current best, not before the living).

**Bind.** A running process becomes a metaflow's flow
by Bind on the ordinary socket: it reserves a flow id,
records the process as the Flow record's Process, sets
the metaflow awake, and answers Bound.FlowId. A Bind
under an address whose bound process is gone replaces
the binding. Taken.Address is refused only while the
old process lives; a dead or reused process is refused
Unidentified.Process. When Message binds its process
at its start with Bind.{ Address Process } under
{ Field message Primary }, Flow resolves both the
peer's executable (read from the kernel's record of
the process) and the configured MessageNexusBinary to
their canonical paths, following symlinks, and
compares the results; MessageNexusBinary is the
resolved store path of the Message binary; a
configured value that resolves to no file refuses the
Nexus payload with NoSource.Path. Bind also serves
debugging and flows launched before Flow existed
(status: current best, not before the living).

**Message process exit.** When a bound process
exits, its flow id moves into the metaflow's Past
(the last few kept, oldest first), as for Stop
(current best). When Message's bound process
exits, its metaflow becomes Asleep and the
binding is dropped; a new Bind from the
configured binary wakes it (current best).

**Dead process detection.** Flow does not poll for
a dead bound process: it notices it when a query
touches that metaflow (Metaflows, Current, Lock,
Bind, Deliver), re-checking the pid and start
time then, and at the hook's Stopped for a
harness flow. A dead bound process found on a
Lock or Deliver re-check answers NotMessage and
the binding is dropped (current best).

**Who is the caller.** Flow answers Identify.Process:
it walks the caller's ancestors to a Flow record's
Process, comparing both pid and start time, and
returns that flow's address, else
Unidentified.Process. No environment variable is read.
The Sender of a Lock is that address (status: current
best, not before the living).

**What Flow refuses.** A request that leaves the routes
of the vision-aspects skill (who speaks to whom within
an aspect and across aspects at the same layer in a
shared topic). Also, on the flow socket: Locked,
Held.Lock, Awake.FlowId, Asleep, Lapsed,
Unknown.[ Address Lock FlowId Key ], NoLayer,
NotConfigured, HashMismatch, Ended.Address, OffRoute
(sender and recipient aspect, layer and topic do not
match the routes), NoneAbove, NotMessage,
Unidentified.Process, and for a Bind Taken.Address or
Unidentified.Process. On the meta socket: NoSource,
HashMismatch, Conflict, Unknown.Key and Store.
A store failure on any query — Metaflows,
Current, Lock, Deliver, Identify,
Configuration and the rest — answers
Refused.Store, never an empty vector.

**Context modules, background.** A module is one file
of prompt text with a subaspect, a topic, a
description and its dependencies. A module's
dependencies load with it, before it; each loads once
per flow at the strongest placement any needing module
gave it (system prompt over first prompt over
loadable); a cycle or an unknown dependency is refused
at registration. Placement: words holding for the whole
flow on every turn go in the system prompt; words of
this flow's task go in the first prompt, where a
refresh replaces them; what is needed on occasion stays
loadable. The registry shape is Configure's
Module.{ Key Source }; the earlier Facet and
Location.[ Path Text ] shapes of book 1 are not in the
ethos above.

## 3. Today and to build

**In production today** (book 14, witnessed
2026-10-07 to 09): Flow 0.25.0 at 962ad12 is
the source; the deployed binaries are 0.14.0
on stable and 0.17.4 on Next (from
CriomOS-home's pins and the units); their
store is a sema file of hand-written rkyv
tables (flows, state, configuration, routes,
launch attempts and outcomes, replacements,
roles, events) holding no Metaflow, Lock or
Memory record.

**To build** (none in production): the Library, Memory
and both Signals above; the Start argument of the start
command; the metaflow record written at reservation;
the Configure, Forget and Configuration meta socket
with Blake3 hash checks; Bind and the Message gate on
the ordinary socket; the module registry and
composition from it and the layer's model; the waking
rule with a persistent queue; the Wake, Refresh, End
and Current requests; ContextMeasured reading the
transcript and the 20/40 percent thresholds; the
refresh as a software sequence including the reap; the
time-bound lock request; Encodable and Bytes<N> in
datom-codec and the ethos intrinsics; the simple and
extended message forms; refusal of requests off the
vision-aspects routes. Today Flow has no Memory root,
no metaflow record, no lock, no module registry, and
reads no context size.

**Current best** (deployment and migration): the
new Flow reads nothing of the old store and
migrates nothing; its Memory starts empty and is
filled by Configure payloads on the meta socket
and by flows that Bind or are Launched. The
deploy names a new path for the new Flow's store,
so the old file is neither read, reused nor
deleted while the living's answer on the old store
is pending; and rotates stable and Next; the old
Nexus serves its sessions until they end or are
refreshed into the new one. No migration code
lives in the Nexus. This rests on the living's
2026-09-24 condition that Flow was not yet live,
unconfirmed since Flow 0.14.0 went live; his
answer on «What the new Message does with the old
store» decides Flow and Message together.

## 4. Open rulings

The books record rulings as asked; whether the living
has answered each was not witnessed in the books
themselves. Pending as the books left them, and
everything below may still change:

- Book 17, ruling 1: the whole vision-flow-ethos file
  (amend the ethos, or its name or split). Ruling 2:
  the dependency line in vision-flow. Ruling 3: where a
  request lands in an awake flow, (a) end of prompt,
  (b) tool-call return outside the prompt, (c) other.
- Book 18 (the Nexus starts), ruling 1: Blake3 and the
  meta-socket payloads; (c) the hash is another.
- Book 15, ruling 1: Encodable. Ruling 2: Bytes<N>
  intrinsic. Ruling 3: the Library root (its Sha256 is
  replaced here by Blake3 per book 18). Ruling 4:
  simple and extended forms.
- Book 11, ruling 1: the four request kinds (this
  design adds Psyche and Psyches per 17). Ruling 2:
  Queue on the record. Ruling 3: the waking rule in
  vision-messaging. Ruling 4: the rule in vision-flow.
- Book 14, ruling 1: the Today section in vision-flow.
- Book 10, rulings 1 to 5: Flow manages metaflows;
  layer decides the model; refresh at 20 to 40
  percent; modules make the flow; requests and the
  lock. Ruling 6: sources.
- Speech across aspects: approved by the living on
  2026-10-09; its lines landed in psyche-skills as
  commit 850fd27. Flow refuses requests off the
  vision-aspects routes.
- Book 3, rulings 4 to 6 (thresholds, refresh
  operations Tell, Lock, Reap, Unlock, subject end
  without an end-goal field): partly carried here,
  its Lineage and Role records are superseded by the
  metaflow record of 17.
- Book 1, rulings 2 to 8 (Facet word, location, role
  placements): superseded in shape by Configure.

Current best, pending his ruling 1 of the Flow Nexus
vision, third edition: the Address form, one Aspect and
Address type with the Metaflow record
{ Address State Past Queue }, replacing the two
shapes of the metaflow.

Current best, not before the living: the Memory
records Module.{ Key Source }, Model, Threshold,
Metaflow and Lock; Aspect, Address, Metaflow, Lock,
Process, Sender, Key, Start and Nexus declared once in
the Library with Subaspect and Source; Process on the
Flow record; the Start argument; the Nexus payload and
the Configuration query with its order; the lock,
Bind, Identify and Deliver queries, responses and
refusals of the flow socket; the Message gate; who
resolves Up is before the living in 73ada7's «Who
works out where send up goes»; the build has Flow
resolve it, current best.

Message's needs (73ada7, message-design section 10),
still open here; its list has no N9, N10 or N12:

- N3: Lock and Deliver on the ordinary socket or on
  Flow's meta socket (Message's fork F2); this design
  keeps them on the ordinary socket.
- N8: whether queueing a busy awake flow and draining
  at the next Stop is right; and where a request lands
  in an awake flow (book 17, ruling 3).

Answered in the design, current best: N1 and N2
(Deliver.{ Lock Request }), N4 declaration in
the Library, N5 (Identify.Process, Process on Flow),
N6 (refusals), N7 (Queued, Woken.FlowId), N11
(the Nexus payload's Lease), N13 (Bind).

FlowId.String is his word for now; a hash-based id is
wanted later.

From the handover, undecided:

- The type of the dense title string.
- Whether an implementation kind survives as a topic
  of a Mind metaflow.
- Removal of the machine line in vision-messaging
  lines 8 to 9.
- 73ada7's Message and Flow ethos draft, to follow
  these once ruled.
- knowledge-flow holds the deployed procedure,
  trial-succession the checks, vision-flow changes
  only by the living's ruling.
