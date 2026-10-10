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
[]
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
      Address                   ; while held
      Until.Integer }           ; seconds since the
                                ; epoch; lapses
   Process.{                    ; the calling
      Pid.Integer               ; process
      Started.Integer }         ; the kernel's start
                                ; time of that pid,
                                ; so a reused pid is
                                ; told apart
   Sender.Address ]             ; who sent a request
[]
[]
```

The Library declares once the types both Signals and
Memory use: Said, Aspect, Address, Metaflow, Lock, Process
and Sender. Memory and both Signals import them (status:
current best, not before the living).

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
[  flow_ethos:[ FlowId Topic Layer
                Request Subaspect
                Source Address
                Process ]
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
      Subaspect                 ; per subaspect and
      Topic                     ; topic
      Source }
   Model.{                      ; one per layer
      Layer
      Native.String }           ; the model's name
                                ; as the harness
                                ; knows it
   Metaflow.flow_ethos:Metaflow ; ethos-zero's form
                                ; for a record
                                ; naming a Library
                                ; type
   Lock.flow_ethos:Lock         ; likewise
   Threshold.{                  ; one per layer
      Layer
      Handover.Integer
      Refresh.Integer } ]
```

Module, Model and Threshold hold what the meta socket's
Configure sets. The Library's Lock is stored one per
metaflow while held. The Flow record's Process holds
the calling process's pid and start time, learned at
spawn or at Bind (status: current best, not before
the living).

Event is imported from signal-flow: Started,
ToolUsed.String, ContextMeasured.{ Tokens.Integer
Window.Integer }, Stopped.

Written, two metaflows:

```
Metaflow.{
   { Psyche core Primary }
   Awake.startInputVital
   [ zooWrongYouth ]
   [ ] }

Metaflow.{
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
                Sender Process ]
   curriculum:[ Name ] ]
[  Launch.{                     ; a metaflow's first
      Address                   ; flow; the address
      Modules.Vector<Name>      ; written short
      Brief.String }            ; a small paragraph
   Wake.{                       ; a sleeping
      Address                   ; metaflow's next
      Request }                 ; the waking request
   Refresh.Address              ; the next link
   End.Address
   Current.Address
   Lock.Address                 ; Message asks; time
                                ; bound
   Identify.Process             ; who is the caller
   Deliver.{                    ; under the lock
      Lock
      Sender                    ; for the route
      Request }
   Release.Lock ]
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
   Locked.Lock
   Identified.Address           ; the caller's
   Delivered                    ; placed in the
                                ; awake flow
   Queued                       ; asleep, or awake
                                ; and busy: waits
   Woken.FlowId                 ; asleep: woken; the
                                ; queue drained with
                                ; the first prompt
   Released
   Refused.[
      Locked                    ; refresh under way
      Held.Lock                 ; already locked
      Lapsed                    ; the lock ran out
      UnknownModule.Name        ; a module
      NoLayer                   ; no model for it
      Unknown.Address           ; no such metaflow
      Ended.Address             ; returned to its
                                ; sender
      OffRoute                  ; sender and
                                ; recipient aspect,
                                ; layer, topic off
                                ; the vision-aspects
                                ; routes
      Unidentified.Process ] ]  ; in no metaflow
[]
```

Identify and the Deliver responses and refusals above
are current best, not before the living. Unknown module
is renamed UnknownModule.Name so that Unknown.Address
can be a variant of its own.

Written, a launch of this flow:

```
Launch.{
   { Psyche flow Primary }      ; written short
   [ vision-flow
     knowledge-ethos ]
   «Design Flow's module registry.» }
```

### Signal, the meta socket

```
Signal                          ; the meta socket
[  flow_ethos:[ Subaspect Topic Layer
                Source Address FlowId
                Process ] ]
[  Configure.[
      Module.{                  ; the registry
         Subaspect
         Topic
         Source }
      Model.{                   ; the layer's model
         Layer
         Native.String }        ; the model's name
                                ; as the harness
                                ; knows it
      Threshold.{               ; percent of window
         Layer
         Handover.Integer       ; 20
         Refresh.Integer } ]    ; 40
   Forget.{                     ; a module leaves
      Subaspect
      Topic }
   Bind.{                       ; a running process
      Address                   ; becomes this
      Process } ]               ; metaflow's flow
[  Configured
   Forgotten
   Bound.FlowId                 ; the flow reserved
   Refused.[
      Unknown.Topic
      NoSource.Path
      HashMismatch
      Taken.Address ] ]         ; already awake
[]
```

Bind is for debugging and for flows launched before
Flow existed: it reserves a flow id, records the
process as the Flow record's Process, and sets the
metaflow awake (status: current best, not before the
living).

Written, one payload file of psyche-skills:

```
Configure.Module.{
   Vision
   flow
   { psyche-skills
     a3f1…9c2e
     vision/flow.md } }
```

Configuration lives in datom files in the repositories
that own it, one file per concern. The CLI sends them
in succession over the meta socket; nothing is expanded
across files. Each payload lands whole or is refused
whole. A module is found by subaspect and topic; its
file's place is Curriculum's to know, checked against
the hash on a read or a write. The Nexus composes from
the registry and reads no path a caller writes.

### Message's simple and extended forms

Defined in Signal as types of their own, nothing
omitted from either; shown here for the lock.

```
[  Send.{                       ; simple: what a
      Address                   ; flow writes
      Request }
   Deliver.{                    ; extended: Message
      Lock                      ; to Flow, under the
      Sender                    ; lock; no flow id
      Request } ]
```

The simple form carries what its use needs and is what
the common queries use, above all in a machine's
context; it names the metaflow, never a flow id. The
extended form carries every parameter and serves
debugging and components. Lock is the Memory record.

## 2. Rules

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
prompt once. The hook reports Started. A new flow's
first response is a presentation of its context in its
role. A wake launches the same way, the drained queue
delivered with the first prompt, the waking request
last.

**The waking rule and the queue.** Every topic has one
metaflow, answering for the whole topic, even across
several skills. Flow keeps its queue. By state: Awake,
the request is delivered now. Asleep, an order, a
question, a psyche or psyches wakes it; a result or a
notice waits in the queue and wakes nothing. Ended, the
request returns to its sender. A waking request drains
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

**The lock.** Message asks Flow for a lock on the
metaflow, bounded in time; with the lock it hands Flow
the request, and Flow places it by the waking rule. A
lock that lapses is released by Flow. What reaches a
flow is a request, never a letter; Flow holds no
messages beyond a queue of requests. While a refresh is
under way the metaflow is locked and a lock request is
refused Locked; a held lock refuses Held. Message
speaks in metaflows and need not know flows. Status:
current best, not before the living.

**Who is the caller.** Flow answers Identify.Process:
it walks the process's ancestors to the harness
process and compares both the pid and start time
of a Flow record's Process, returning that flow's
address, else Unidentified.Process. The Sender of a
Deliver is that address (status: current best, not
before the living).

**What Flow refuses.** A request that leaves the routes
of the vision-aspects skill (who speaks to whom within
an aspect and across aspects at the same layer in a
shared topic). Also, by Signal: Locked, Held, Lapsed, UnknownModule,
NoLayer, Unknown.Address, Ended.Address, OffRoute
(Sender and recipient aspect, layer and topic do not
match the routes), Unidentified.Process, and for a
Configure Unknown topic, NoSource, HashMismatch, and
for a Bind Taken.

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
loadable. The registry shape is now Configure's
Module; the earlier Facet and Location.[ Path Text ]
shapes of book 1 are not in the ethos above.

## 3. Today and to build

**In production today** (book 14, witnessed
2026-10-07 to 09): the Flow repository is 0.24.0, six
crates, most in flow-nexus. It composes the system
prompt and first prompt from caller-supplied paths,
has Replace, an events store on disk, and hooks that
report Started, ToolUsed and Stopped. Main flows are
launched by the Primary scripts: the Claude launcher
passes a system prompt file and a first prompt opening
with six slash skills; the Codex launcher reads
.agents/skills SKILL.md files into the first prompt;
both take --topic, Core by default, with continuation
inheritance. The flow id is six hex characters of the
harness session id. Authored skills live in
psyche-skills, mind-skills and field-skills. Messages
go through messenger-clj, which routes from its own
store and types into Herdr panes. The bottom layer of
each aspect runs the refresh.

**To build** (none in production): the Library, Memory
and both Signals above; the metaflow record written at
reservation; the Configure and Forget meta socket with
Blake3 hash checks; the module registry and
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
records Module, Model, Threshold, Metaflow and Lock;
Aspect, Address, Metaflow, Lock, Process and Sender
declared once in the Library with Subaspect and
Source; Process on the Flow record;
the lock, Identify and Deliver queries, responses and
refusals of the flow socket; Bind on the meta socket.

Message's needs (73ada7, message-design section 10),
still open here; its list has no N9, N10 or N12:

- N3: Lock and Deliver on the ordinary socket or on
  Flow's meta socket (Message's fork F2); this design
  keeps them on the ordinary socket.
- N8: whether queueing a busy awake flow and draining
  at the next Stop is right; and where a request lands
  in an awake flow (book 17, ruling 3).
- N11: the lease length is in no Configure payload;
  Lock carries Until and nothing sets its span.

Answered in the design, current best: N1 and N2
(Deliver.{ Lock Sender Request }), N4 declaration in
the Library, N5 (Identify.Process, Process on Flow),
N6 (refusals), N7 (Queued, Woken.FlowId), N13 (Bind).

Said is the build's name for the type carrying his
words; the Aspect variant Psyche and the Request
variant Psyche (carrying Said) clash by name, and the
clash is reported to the living.

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

Gap found while assembling (the flow's own
inference): FlowId remains String (comment in
Library).
