<!-- to-the-living:start -->
Presentation.{ «Flow, whole, in ethos» }

## Where things are

Your order of 2026-10-11: Flow whole, every type and every trait in ethos. Drawn from 1,258 of your records, checked word by word.

```
  a Nexus, as your vision has it
  +----------------------------------------+
  |  Library: what the parts share         |
  +----------------------------------------+
        |              |              |
        v              v              v
  +-----------+  +-----------+  +-----------+
  |  Signal   |  | Operation |  |  Memory   |
  |  says     |  |  does     |  | remembers |
  +-----------+  +-----------+  +-----------+
        |   query      ^    change     |
        +------------->|<--------------+
            response   |   ok / failed
        every method in a trait

  the current design (in development)
  +----------------------------------------+
  |  Library · Signal · Signal · Memory    |
  |  no Operation; one trait, in prose     |
  |  starts from a datom of paths     x    |
  |  refuses with the store's text    x    |
  +----------------------------------------+
        x = against the Nexus vision

  Field's signal-flow branch
  +----------------------------------------+
  |  Operation, no Memory                  |
  |  letters · message ids · priority      |
  |  tiers · PowerLevel: all rejected      |
  +----------------------------------------+

  "storage", in your words
  2026-10-02: not fond of the word;
              memory it is; its kind =
              change ok/failed + upgrade-from
  2026-10-11: "the storage ethos" beside
              "the memory ethos"
        -> read here as the trait
           Rememberable; ruling 7
```

## Distillation

### Proposal 1 — vision-flow, the vision whole

File: `psyche-skills/skills/vision-flow.md`.

Section «What it does», its three paragraphs as they stand, kept; replaced after them is nothing. Added, after the Capsule paragraph:

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. A voice is a permanent metaflow: it sleeps and is woken, and never ends. A job is a metaflow that ends when its mission is done; a message sent to it after that returns to its sender with notice that it has ended.

A flow's id is a hash, held by the Nexus as bytes and written as three camelCase words. The Nexus reserves it before the flow starts and the flow reads it in its prompt.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. A metaflow asleep is woken by a waking request and receives its whole queue, oldest first, in the first prompt. Flow holds the lock on a metaflow: the lock is granted to a sender for a bounded time and lapses by itself.

Section «Starting flows», first paragraph kept. Its second paragraph, removed:

A voice is an aspect carrying a rank, `Psyche.Primary`: Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices. The model behind a voice is configuration, declared once in Flow and changed only over its meta wire; not every model is exposed to every voice. Voices are addressed by name; a flow id is for the ledger and the archive, and is written in words. A side flow is a job, not a voice: focused, not long-lived, gone when its mission is done; a message sent to it after that returns to its sender with notice that the flow has ended.

Added in its place:

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source, and reads no path a caller writes.

Section «A replaced session is reaped by the refresh itself», kept. Added after it:

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process and never trusts a claimed id.

Ruling 1: the paragraphs as written, or amended by paragraph.

Ruling 2: four layers in every aspect, Quaternary included, as your records of October say, or three, as the standing line says.

Ruling 3: the title of a thread. (a) the address written short, then the flow's three words: `{ Psyche flow Primary } startInputVital`; (b) aspect, model and id, as vision-model-roles has it; (c) other.

### Proposal 2 — vision-flow-ethos, Flow in ethos

File: `psyche-skills/skills/vision-flow-ethos.md`, new, the file vision-ethos points to. Shown whole; one root per ethos file in Flow's repository.

Library, types:

```
Library                      ; Flow's shared types
[  core:Name ]               ; a camelCase word
[  Hash.Bytes<32>            ; blake3; Encodable
   FlowId.Hash               ; one run; written
                             ; as three words
   Topic.core:Name           ; a topic's name
   Aspect.[                  ; whose psyche
      Psyche
      Mind
      Field ]
   Layer.[                   ; decides the model
      Primary
      Secondary
      Tertiary
      Quaternary ]
   Address.{                 ; names a metaflow
      Aspect
      Topic
      Layer }
   Role.[                    ; what a metaflow is
      Voice                  ; permanent
      Job.String ]           ; ends with its
                             ; mission
   Instant.Integer           ; seconds since the
                             ; epoch
   Process.{                 ; a calling process
      Pid.Integer
      Started.Instant }      ; so a reused pid is
                             ; told apart
   Said.{                    ; the living's words
      Context.String
      Verbatim.String }
   Request.[                 ; reaches a metaflow
      Order.String           ; wakes
      Question.String        ; wakes
      Psyche.Said            ; wakes
      Psyches.Vector<Said>   ; wakes
      Result.String          ; waits asleep
      Notice.String ]        ; wakes nothing
   Recipient.[               ; where a request
      Address                ; goes
      Up ]                   ; one layer above
                             ; the sender
   Sender.Address
   Lock.{                    ; one per metaflow
      Sender
      Address                ; resolved
      Until.Instant }        ; lapses
   Subaspect.[               ; a module's kind
      Vision
      Intent
      Knowledge
      Operation
      Trial
      Compensation ]
   Key.{                     ; a module's key
      Subaspect
      Topic }
   Source.{                  ; where its text is
      Repository.String
      Hash
      Path.String }
   Module.{                  ; the registry entry
      Key
      Source }
   Model.{                   ; one per layer
      Layer
      Harness.HarnessKind
      Native.String }
   Threshold.{               ; percent of window
      Layer
      Handover.Integer
      Refresh.Integer }
   Event.[                   ; what a hook reports
      Started
      ToolUsed.String
      ContextMeasured.{
         Tokens.Integer
         Window.Integer }
      Stopped ]
   Metaflow.{                ; one per address
      Address
      Role
      State.[
         Awake.FlowId
         Asleep
         Ended ]
      Past.Vector<FlowId>
      Queue.Vector<Request> }
   Flow.{                    ; one per run
      FlowId
      Session.String
      Process
      Events.Vector<Event> }
   Refusal.[                 ; every no, typed
      Unknown.[
         Address
         Lock
         FlowId
         Key ]
      Awake.FlowId
      Asleep
      Ended.Address
      Held.Lock
      Locked
      Lapsed
      NoLayer
      NotConfigured
      HashMismatch
      OffRoute
      NoneAbove
      NotMessage
      Unidentified.Process
      Taken.Address
      Store.[
         NotOwn
         Unopenable
         Unwritable ] ] ]
```

Library, traits (`.` self, `!` mutable self, `:` no self):

```
[  Encodable.[               ; one bare run in
      encode.[ String ]      ; datom; bytes in
      decode:{               ; memory
         [ String ]
         [ Result<Self
                  Refusal> ] } ]
   Rememberable.{            ; the memory kind
      [ ]
      [ Previous ]           ; the former form
      [ VERSION.Integer ]
      [ change!{             ; a standard change,
           [ Self ]          ; succeeded or
           [ Result<Self     ; failed
                    Refusal> ] }
        upgrade:{            ; from the former
           [ Previous ]      ; version: the very
           [ Self ] } ] }    ; edit the type had
   Identifiable.[            ; who calls
      identify.{
         [ Process ]
         [ Option<Address> ] }
      bind!{
         [ Address Process ]
         [ Result<FlowId
                  Refusal> ] } ]
   Lockable.[                ; the lock on a
      grant!{                ; metaflow
         [ Sender Recipient ]
         [ Result<Lock
                  Refusal> ] }
      release!{
         [ Lock ]
         [ Result<Self
                  Refusal> ] }
      lapse![ Vector<Lock> ] ]
   Wakeable.[                ; sleeping and
      wake!{                 ; waking
         [ Request ]
         [ Result<FlowId
                  Refusal> ] }
      queue!{
         [ Request ]
         [ Self ] }
      drain![ Vector<Request> ]
      sleep![ Self ] ]
   Lineal.[                  ; one run after
      launch!{               ; another
         [ Vector<Key> String ]
         [ Result<FlowId
                  Refusal> ] }
      refresh!{
         [ ]
         [ Result<FlowId
                  Refusal> ] }
      reap!{
         [ FlowId ]
         [ Result<Self
                  Refusal> ] }
      end![ Self ] ]
   Composable.[              ; modules into a
      compose.{              ; prompt
         [ Vector<Module> ]
         [ Result<String
                  Refusal> ] }
      check.{
         [ Source ]
         [ Result<Hash
                  Refusal> ] } ]
   Observable.[              ; state by
      report!{               ; subscription,
         [ Event ]           ; never by polling
         [ Self ] }
      subscribe.[ Vector<Metaflow> ] ]
   Configurable.[            ; over the meta
      configure!{            ; socket only
         [ Module ]
         [ Result<Self
                  Refusal> ] }
      forget!{
         [ Key ]
         [ Result<Self
                  Refusal> ] } ] ]
```

Library, associations:

```
[  Hash.[ Encodable ]
   FlowId.[ Encodable ]
   Process.[ Identifiable ]
   Metaflow.[ Lockable
              Wakeable
              Lineal
              Rememberable ]
   Flow.[ Observable
          Rememberable ]
   Module.[ Composable
            Rememberable ]
   Model.[ Rememberable ]
   Threshold.[ Rememberable ]
   Lock.[ Rememberable ]
   Nexus.[ Configurable
           Rememberable ] ]
```

Signal, ordinary socket:

```
Signal                       ; the ordinary socket
[  flow_ethos:[ Address FlowId
                Request Lock
                Sender Recipient
                Process Key
                Metaflow Event
                Refusal ] ]
[  Launch.{                  ; queries
      Address
      Modules.Vector<Key>
      Brief.String }
   Wake.{
      Address
      Request }
   Refresh.Address
   End.Address
   Current.Address
   Bind.{
      Address
      Process }
   Lock.{                    ; Message asks
      Sender
      Recipient }
   Identify.Process
   Deliver.{                 ; under the lock
      Lock
      Request }
   Release.Lock
   Report.{                  ; the hook's
      FlowId
      Event }
   Stop.FlowId
   Metaflows ]
[  Launched.FlowId           ; responses
   Woken.FlowId
   Queued
   Refreshed.{
      FlowId                 ; successor
      FlowId }               ; predecessor
   Ended
   Current.[
      Awake.FlowId
      Asleep
      Ended ]
   Bound.FlowId
   Locked.Lock
   Identified.Address
   Delivered
   Released
   Reported
   Stopped
   Listed.Vector<Metaflow>
   Refused.Refusal ]
[]                           ; types: none of its
                             ; own
```

Signal, meta socket:

```
Signal                       ; the meta socket
[  flow_ethos:[ Module Model
                Threshold Key
                Refusal ]
   meta_signal_flow:[
      CodexEndpoint
      HarnessKind
      HarnessProfile ] ]
[  Configure.[               ; queries
      Module
      Model
      Threshold
      Nexus ]
   Forget.Key
   Configuration ]
[  Configured                ; responses
   Forgotten
   Configuration.{
      Nexus
      Models.Vector<Model>
      Thresholds.Vector<Threshold>
      Modules.Vector<Module> }
   Unconfigured
   Refused.Refusal ]
[  Nexus.{                   ; the Nexus's own
      SourceRoot.String      ; setup
      StableCodex.CodexEndpoint
      NextCodex.CodexEndpoint
      HarnessProfiles.Vector<HarnessProfile>
      MetaAspects.Vector<Aspect>
      MessageSocket.String
      Lease.Integer } ]      ; the lock's seconds
```

Operation, one per effect:

```
Operation                    ; what Flow does
[  flow_ethos:[ Address FlowId
                Request Lock
                Sender Recipient
                Process Key
                Module Event
                Metaflow Flow
                Refusal ] ]
[  Spawn.{                   ; operations
      Metaflow
      Modules.Vector<Module>
      Brief.String }
   Rouse.{                   ; wake a sleeper
      Metaflow
      Request }
   Enqueue.{
      Metaflow
      Request }
   Succeed.Metaflow          ; refresh: a
                             ; successor
   Retire.Metaflow           ; end
   Attach.{                  ; bind a process
      Metaflow
      Process }
   Grant.{
      Sender
      Recipient }
   Place.{                   ; deliver, awake
      Lock
      Request }
   Free.Lock                 ; release
   Note.{                    ; record an event
      FlowId
      Event }
   Reap.FlowId
   Register.Module           ; configure
   Unregister.Key ]
[  Spawned.FlowId            ; outcomes
   Roused.FlowId
   Enqueued
   Succeeded.{
      FlowId
      FlowId }
   Retired
   Attached.FlowId
   Granted.Lock
   Placed
   Freed
   Noted
   Reaped
   Registered
   Unregistered
   Failed.Refusal ]
[]                           ; types: none of its
                             ; own
```

Memory:

```
Memory                       ; what Flow remembers
[  flow_ethos:[ Metaflow Flow
                Lock Module
                Model Threshold ]
   meta_signal_flow:[ Nexus ] ]
[  Metaflow                  ; records: one per
   Flow                      ; address; one per
   Lock                      ; run; one per held
   Module                    ; lock; the registry;
   Model                     ; one per layer;
   Threshold                 ; one per layer;
   Nexus                     ; stored once
   Configured.Boolean ]      ; whether the meta
                             ; Configure was ever
                             ; done
```

Rulings:

Ruling 4: Flow starts with no arguments, its socket paths and store path a constant in the executable, and its configuration in its own store, as the Nexus vision says; the design's Start datom of three paths goes. (a) as here; (b) keep the Start datom; (c) other.

Ruling 5: every refusal is a variant, the store's included; the design's `Store.String` carrying the store's own error text goes. (a) as here; (b) other.

Ruling 6: the flow id is `FlowId.Hash` over `Hash.Bytes<32>`, Encodable, written as three camelCase words; `Bytes<32>` is the intrinsic of «Stored type and datom form», and ethos-zero cannot yet express it nor a new type that is not an alias, so the build carries a string until it can. (a) as here; (b) a string stays the design; (c) other.

Ruling 7: storage. (a) storage is Rememberable, the kind every Memory record bears, with its version and its upgrade from the former form, and there is no fifth root; (b) a Storage root of its own, declaring how Memory persists; (c) your words.

Ruling 8: Bind, the attaching of an already running process to a metaflow. (a) on the ordinary socket, as here and in the design; (b) on the meta socket, as your record of 2026-09-24 reads; (c) other.

Ruling 9: Up. (a) one layer above the sender in its aspect, refused above Primary, as here; (b) the next running rung in that direction, Low reaching High when Medium is not running, as vision-model-roles has it; (c) other.

Ruling 10: the Operation names: Spawn, Rouse, Enqueue, Succeed, Retire, Attach, Grant, Place, Free, Note, Reap, Register, Unregister. (a) as here; (b) the same verbs as the queries, Launch, Wake, Refresh, End, Bind, Lock, Deliver, Release, Report, Stop, Configure, Forget, the operation telling itself from the query by its root; (c) other.

Your records against the design, beyond the rulings:

| your record | date | the design |
|---|---|---|
| a flow's role: voice or job | 2026-10-05, 10-07 | no role — enters above as Role |
| a flow that is not a metaflow | 2026-10-07 | every flow in one — enters as Role.Job |
| refresh floor 15–20 %; restart on a change of direction | undated | thresholds only |
| the bottom of each aspect runs the refresh | 2026-10-07 | no model decides a step |
| a small model checks a launch | undated | no model decides a step |
| messages reach both flows until the old logs out | undated | the lock refuses them |
| predecessor woken when its successor fails | undated | no such path |
| module text fed into memory | 2026-10-07 | a hashed source |
| Flow's memory lives in Mind | 2026-09-17 | its own store |

Field's branch against this ethos (the Secondary's reading):

| the branch has | here |
|---|---|
| letters, message ids, priority tiers, Sender.[ Flow Owner ], PowerLevel | gone |
| Restart, ResolveRecipient, QueueTurnEnd, LaunchStatus, Observe.Launch | gone |
| no Launch, Wake, Refresh | present |

Not yet expressible in ethos-zero, for the Ethos seat: a new type that is not an alias; `Bytes<32>`; `core:Name`; a trait outside a Library. The build carries strings there; the ethos stays as written.
<!-- to-the-living:end -->
