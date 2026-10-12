<!-- to-the-living:start -->
Presentation.{ «Flow, whole, in ethos, third edition» }

Nothing here has been approved before. Landed and gone from this book: metaflows and the core topic, layers and launch, refresh.

```
  still open
  +----------------------------------------+
  |  1  new wording from your comments     |
  |  2  the ethos file, whole              |
  |  3  nine rulings                       |
  +----------------------------------------+
```

## Distillation

### Proposal 1 — new wording, from your comments of 20:23 to 20:32

File: `psyche-skills/skills/vision-flow.md`, section «What it does», after the metaflow paragraph landed today. Added:

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.

Ruling 1: the three paragraphs as written, or amended by paragraph.

Ruling 2: four layers in every aspect, Quaternary included, as landed, or three.

Ruling 3: the name of the uncapitalized camelCase identifier type: (a) Name; (b) Word; (c) yours.

Ruling 4: the title of a thread: (a) the address written short, then the flow's words; (b) aspect, model and id; (c) other.

### Proposal 2 — vision-flow-ethos, Flow in ethos

File: `psyche-skills/skills/vision-flow-ethos.md`, new, the file vision-ethos points to. Shown whole; one root per ethos file in Flow's repository.

Library, types:

```
Library                      ; Flow's shared types
[  core:Name ]               ; camelCase, lower
[  Hash.Bytes<32>            ; blake3; Encodable
   FlowId.Hash               ; the harness session
                             ; id, hashed; written
                             ; as three words
   Topic.core:Name           ; core is permanent
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
      Result.String          ; waits idle
      Notice.String ]        ; wakes nothing
   Recipient.[               ; where a request
      Address                ; goes
      Up ]                   ; one layer above
                             ; the sender
   Verdict.[                 ; the waking
      Wake.Layer             ; judgment
      Stay ]
   Lock.{                    ; Flow's own, one
      Address                ; per metaflow
      Until.Instant }        ; lapses
   Subaspect.[               ; a module's kind
      Spirit
      Intent
      Vision
      Knowledge
      Operation
      Compensation
      Trial ]
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
   Effort.[
      High
      Medium
      Low ]
   Model.{                   ; one per layer
      Layer
      Harness.HarnessKind
      Native.String
      Effort }
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
   Notification.[            ; what a subscriber
      Entered.{              ; hears
         Address
         Request }
      Woken.{
         Address
         FlowId }
      Refreshed.{
         Address
         FlowId }
      Idled.Address ]
   Metaflow.{                ; one per address
      Address
      State.[
         Awake.FlowId
         Idle ]
      Modules.Vector<Key>    ; what wakes it
      Past.Vector<FlowId>
      Queue.Vector<Request> }
   Flow.{                    ; one per run
      FlowId
      Process
      Events.Vector<Event> }
   Refusal.[                 ; every no, typed
      Unknown.[
         Address
         FlowId
         Key ]
      Awake.FlowId
      Idle
      Refreshing
      NoLayer
      NotConfigured
      HashMismatch
      OffRoute
      NoneAbove
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
   Identifiable.[            ; who calls, from
      identify.{             ; the process alone
         [ Process ]
         [ Result<Address
                  Refusal> ] }
      bind!{
         [ Address Process ]
         [ Result<FlowId
                  Refusal> ] } ]
   Lockable.[                ; Flow's own lock
      grant!{
         [ Instant ]
         [ Result<Lock
                  Refusal> ] }
      free![ Self ]
      lapse![ Vector<Lock> ] ]
   Wakeable.[                ; idling, waking
      judge.{
         [ Request ]
         [ Verdict ] }
      wake!{
         [ Request ]
         [ Result<FlowId
                  Refusal> ] }
      queue!{
         [ Request ]
         [ Self ] }
      drain![ Vector<Request> ]
      idle![ Self ] ]
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
                  Refusal> ] } ]
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
      subscribe.[ Vector<Metaflow> ]
      notify.[ Notification ] ]
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
              Observable
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
                Request Recipient
                Process Key
                Metaflow Event
                Notification
                Refusal ] ]
[  Launch.{                  ; queries
      Address
      Modules.Vector<Key>
      Brief.String }
   Send.{                    ; Message asks;
      Recipient              ; the sender is the
      Request }              ; calling process
   Subscribe.Address
   Refresh.Address
   Bind.{
      Address
      Process }
   Identify.Process
   Report.{                  ; the hook's
      FlowId
      Event }
   Stop.FlowId
   Show.Address
   List ]
[  Launched.FlowId           ; responses
   Sent                      ; in the context
   Queued                    ; idle, busy, or
                             ; refreshing
   Woken.FlowId
   Subscribed.Vector<Metaflow>
   Notified.Notification     ; each change,
                             ; as it happens
   Refreshed.{
      FlowId                 ; successor
      FlowId }               ; predecessor
   Bound.FlowId
   Identified.Address
   Reported
   Stopped
   Shown.Metaflow
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
   Show ]
[  Configured                ; responses
   Forgotten
   Shown.{
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
                Request Recipient
                Process Key
                Module Event
                Metaflow Flow
                Notification
                Refusal ] ]
[  Spawn.{                   ; operations
      Metaflow
      Modules.Vector<Module>
      Brief.String }
   Judge.{                   ; wake or stay
      Metaflow
      Request }
   Rouse.{
      Metaflow
      Request }
   Enqueue.{
      Metaflow
      Request }
   Place.{                   ; into an awake
      Metaflow               ; flow's context
      Request }
   Succeed.Metaflow          ; refresh
   Attach.{                  ; bind a process
      Metaflow
      Process }
   Grant.Metaflow            ; the lock
   Free.Metaflow
   Note.{                    ; record an event
      FlowId
      Event }
   Notify.{
      Address
      Notification }
   Reap.FlowId
   Register.Module
   Unregister.Key ]
[  Spawned.FlowId            ; outcomes
   Judged.Verdict
   Roused.FlowId
   Enqueued
   Placed
   Succeeded.{
      FlowId
      FlowId }
   Attached.FlowId
   Granted.Lock
   Freed
   Noted
   Notified
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

Ruling 5: Flow starts with no arguments, its socket paths and store path a constant in the executable, its configuration in its own store; the design's Start datom of three paths goes. (a) as here; (b) keep the Start datom; (c) other.

Ruling 6: every refusal is a variant, the store's included; `Store.String` goes. (a) as here; (b) other.

Ruling 7: storage. (a) storage is Rememberable, the kind every Memory record bears, with its version and its upgrade from the former form, and there is no fifth root; (b) a Storage root of its own, declaring how Memory persists; (c) your words.

Ruling 8: the waking judgment. (a) Flow asks a small model, configured per layer like any Model, and acts on its Verdict; (b) a separate Nexus judges; (c) other.

Ruling 9: Message's subscription. (a) one Subscribe per metaflow, answered with the metaflow on open and then each Notification as it happens, as here; (b) one subscription to all of Flow; (c) other.

Ruling 10: Up. (a) one layer above the sender in its aspect, refused above Primary; (b) the next running rung in that direction; (c) other.

Ruling 11: the Operation names, Spawn, Judge, Rouse, Enqueue, Place, Succeed, Attach, Grant, Free, Note, Notify, Reap, Register, Unregister. (a) as here; (b) the queries' own verbs; (c) other.

Your records against the design, beyond the rulings:

| your record | date | the design |
|---|---|---|
| refresh floor 15–20 %; restart on a change of direction | undated | thresholds only |
| the bottom of each aspect runs the refresh | 2026-10-07 | no model decides a step |
| a small model checks a launch | undated | no model decides a step |
| messages reach both flows until the old logs out | undated | the lock refuses them |
| predecessor woken when its successor fails | undated | no such path |
| module text fed into memory | 2026-10-07 | a hashed source |
| Flow's memory lives in Mind | 2026-09-17 | its own store |
| effort is data of the model | 2026-09-26 | no effort — enters above |
| spirit first among module kinds; compensation above trial | 2026-10-07 | neither — enters above |
| options are a last resort | undated | Option in the stage — none above |
| queries in the imperative voice | 2026-08-26 | Metaflows, Current, Configuration — Show, List above |

Field's branch against this ethos (the Secondary's reading):

| the branch has | here |
|---|---|
| letters, message ids, priority tiers, Sender.[ Flow Owner ], PowerLevel | gone |
| Lock, Deliver, Release on the wire | gone: Send, Subscribe |
| Restart, ResolveRecipient, QueueTurnEnd, LaunchStatus, Observe.Launch | gone |
| no Launch, Wake, Refresh | Launch, Send, Refresh |

Not yet expressible in ethos-zero, for the Ethos seat: a new type that is not an alias; `Bytes<32>`; `core:Name`; a trait outside a Library. The build carries strings there; the ethos stays as written.
<!-- to-the-living:end -->
