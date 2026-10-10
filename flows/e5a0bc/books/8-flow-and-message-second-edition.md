<!-- to-the-living:start -->
Presentation.{ «Flow and Message», second edition }

## 1. The metaflow

Drawing: two horizontal lines through beads. The upper line, labelled `Voice.{ Mind Tertiary }`, passes through beads `4403a7 → 918df4 → …` and runs off the right edge, no end. The lower line, labelled `Subject ethos`, passes through `7f3a21 → b02c1e` and ends at a round mark labelled `end met`. Each bead is a flow.

A flow is one run of a model: launched, filled, ended. A metaflow is what continues through flows, one after another. It is what you speak to, what a message is addressed to, what is refreshed. Two kinds: a voice, with no known ending; a subject, a long-running task of its own, ended when its end condition is judged met. Every flow continues a metaflow; a flow spawned for one task is a subject with one flow so far, and when it fills up it is refreshed like any other.

Flow's Library root, proposed:

```
Library            ; shared by Flow's roots
[]                 ; imports
[ FlowId.Integer   ; one run; hex when written
  Voice.{          ; no known ending
    Aspect.[
      Psyche
      Mind
      Field ]
    Layer.[
      Primary
      Secondary
      Tertiary
      Quaternary ] }
  Metaflow.[       ; what continues
    Voice
    Subject.{      ; a task of its own
      Voice        ; runs as, spawned by
      Name.String
      End.String } ]   ; when it ends
  Flow.{           ; a flow, nothing repeated
    FlowId
    Metaflow }
  Event.[
    Started
    ToolUsed.String
    ContextMeasured.Integer   ; tokens
    Stopped ] ]
[]                 ; kinds
[]                 ; associations
```

Written:

```
{ 918df4
  Voice.{
    Mind
    Tertiary } }
```

```
{ 7f3a21
  Subject.{
    { Mind
      Secondary }
    ethos
    «syntax changes generated» } }
```

Today, in the code (signal-flow at f95034d): a flow's role is its caller, FlowId is a String, and no Voice, Layer or Metaflow type exists.

```
Caller.{           ; the role today
  FlowId           ; String
  FlowAspect.[
    Psyche
    Mind
    Field ]
  PowerLevel.[
    High
    Medium
    Low
    UltraLow ]
  ModelName }
```

## 2. The registry is Flow's Memory

Drawing: left column, three metaflow labels; right column, flow beads. From `Voice.{ Psyche Primary }` a solid arrow to bead `e5a0bc`, and a faded, crossed arrow to bead `8475a9` behind it.

```
Memory             ; what Flow remembers
[ flow:[           ; from the Library
    FlowId
    Metaflow
    Event ] ]
[ Flow.{           ; one record per flow
    FlowId
    Metaflow       ; what it continues
    State.[        ; Running = current
      Running
      Ended ]
    Vector<Event> } ]   ; oldest first
```

The registry that changes which flow a voice is associated with is this record: the one Running flow with that metaflow. Today Flow has no Memory root; it keeps a table of hook events per flow id and the stored caller.

## 3. Launch, refresh, end

Drawing: a flowchart top to bottom, 360 wide. Step 1 `Launch.{ Metaflow Brief }` → `compose from the voice's role record` → `open, spawn, bind` → `Launched.Flow`. A second entry, step 2 `Refresh.Metaflow`, joins at compose with `handover as the brief`, and its exit adds `reap the predecessor`. A third, step 3 `End.Subject`, goes straight to `reap` and `address closed`.

```
Signal             ; what Flow says
[ flow:[
    FlowId
    Metaflow
    Flow
    Event ] ]
[ Launch.{         ; a metaflow's first flow
    Metaflow
    Brief.String }
  Refresh.Metaflow ; successor; handover = brief
  End.Metaflow     ; a subject judged ended
  Current.Metaflow ; which flow: the messenger asks
  Report.{         ; the hook reporting
    FlowId
    Event } ]
[ Launched.Flow
  Refreshed.{
    Flow           ; the successor
    FlowId }       ; the predecessor, reaped
  Ended.Metaflow
  Current.[
    Running.Flow
    Ended
    Unknown ]
  Refused.[
    NoCapsule
    Busy.Metaflow  ; already has a Running flow
    NoRole.Voice ] ; no role record for it
  Reported ]
[]
```

A launch is composed from the role record of the metaflow's voice (the record «Context modules» asks you about; its rulings stay there) and the brief. A subject runs as its voice: same system prompt, same model, its own brief and end. A voice launches subjects under itself and refreshes itself; Field launches voices at boot; later, Flow does both on its own.

Today's Replace already reaps before it releases (`launching.rs:488`): the predecessor is recorded Stopped, which delivery refuses, before the successor is routable.

## 4. The refresh is software

Drawing: a gauge filling left to right in three stages. At the threshold mark, a hand types `write your handover` into the pane. At the right end, `Stopped` → `Refresh` → a new bead; the old bead greys out and the address arrow moves.

```
Operation          ; one per effect
[ flow:[
    FlowId
    Metaflow
    Flow
    Event ] ]
[ Compose.{        ; role record + brief
    Metaflow
    Brief.String }
  Open.Metaflow    ; the Capsule
  Spawn.{          ; the harness
    Flow
    Composed }
  Bind.Flow        ; the Herdr pane
  Tell.{           ; type into a pane
    FlowId
    String }
  Reap.FlowId      ; stop; address gone
  Record.{
    FlowId
    Event } ]
[ Composed.{
    SystemPrompt.String
    EntryFiles.Vector<String>
    FirstPrompt.String }
  Opened.Capsule
  Spawned.Flow
  Bound.Flow
  Told
  Reaped.FlowId
  Recorded
  Failed.String ]
[ Capsule.{
    Home.String
    Login.Vector<String> } ]
```

The hook reports `ContextMeasured` at each stop. At the threshold Flow performs `Tell` with the handover order; at the next `Stopped` it performs `Refresh`: compose from the handover, spawn, bind, reap, record, address moved. No model decides any of it. Today nothing measures a flow's context: the hook reports only `Started`, `ToolUsed`, `Stopped`.

## 5. Message, married

Drawing: a letter envelope labelled `To Voice.{ Mind Tertiary }` goes to a box `Flow: Current` which answers `918df4`, then to a terminal pane. A side arrow from the pane's process to Flow labelled `who is this? → Voice.{ Psyche Primary }`.

```
Library            ; Message's Library
[ flow:[           ; sender and receiver
    FlowId         ; are Flow's names
    Metaflow ] ]
[ Letter.{
    From.Metaflow  ; never the run
    To.Metaflow
    Body.String } ]
[]
[]
```

```
Signal
[ message:[ Letter ]
  flow:[
    FlowId
    Metaflow ] ]
[ Send.Letter ]
[ Sent.FlowId      ; the run that got it
  Returned.[
    Ended.Metaflow ; the subject had ended
    Unknown.Metaflow ] ]
[]
```

Married: Message never takes a sender from a payload or an environment variable; it reads the sending process and asks Flow which flow, and so which metaflow, that is. Message never routes by itself; it asks Flow `Current` and delivers to the Running flow. The envelope becomes `#msg [ Voice.{ Mind Tertiary } body ]`.

Today, messenger-clj reads the sender from `FLOW_ID` and routes from its own store, never asking Flow. The Rust Message Nexus already does it the married way: it reads its peer's process through the kernel and asks Flow `ResolvePeer`.

Your notion of a voice brokering for a job that may end: a subject is addressable until it is judged ended, a letter after that is returned to its sender, and the subject carries the voice it ran as, so the sender knows where to turn. No broker is needed.

## 6. The title

```
{ 918df4           ; the Flow, as written
  Voice.{
    Mind
    Tertiary } }
```

```
{ Mind Tertiary 918df4 }   ; as you wrote it
```

## 7. Clusters

Metaflows expanding and contracting, three to seven, the Sun woken: bad807's «Metaflows» rulings 1 to 6 stand open there, untouched here. Its ruling 7, a metaflow name on the launch profile, is replaced by `Flow.{ FlowId Metaflow }` above.

## Rulings

1. Every flow continues a metaflow: `Flow.{ FlowId Metaflow }`, `Metaflow.[ Voice Subject ]`, no Job: yes, or amend.
2. A subject carries the voice it runs as and that spawned it, `Subject.{ Voice Name End }`: (a) yes. (b) an aspect only, its model given at launch. (c) amend.
3. The registry is the Flow record in Flow's Memory, a metaflow's current flow its Running one; the messenger resolves through Flow and its own route store goes: yes, or amend.
4. A letter is from a metaflow to a metaflow, the run's id in the ledger only; a letter to an ended subject returns to its sender; no broker: yes, or amend.
5. The refresh in software, section 4: yes, or amend. The threshold: (a) your number, tokens or a share of the window. (b) half the model's window, tuned after a trial.
6. The title: (a) `{ 918df4 Voice.{ Mind Tertiary } }`. (b) `{ Mind Tertiary 918df4 }`.
<!-- to-the-living:end -->
