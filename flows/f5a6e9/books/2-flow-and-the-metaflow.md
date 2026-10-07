<!-- to-the-living:start -->
Presentation.{ «Flow and the metaflow» }

Each of your comments on the second edition, then the shape it produced. Book 1, «Context modules», gives the role record and the launch's modules; this book gives what a flow is, what continues, the lock, the refresh and the end.

## 1. "A flow could exist and not be a metaflow"

Your comment: "make it an optional metaflow... The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name."

A flow has a flow id and a role, and may continue a metaflow. A role is a voice or a worker (today's read-trivial, write-ordinary, tester, book). A metaflow is the voice of the flow's own role, or a named subject; a subflow or a one-task flow continues nothing.

```
Library              ; Flow's
[ curriculum:[ Name ] ]
[ Role.[
    Voice.{
      Aspect.[
        Psyche
        Mind
        Field ]
      Layer.[
        Primary
        Secondary
        Tertiary
        Quaternary ] }
    Worker.Name ]    ; a subflow's role
  Metaflow.[         ; what continues
    Voice            ; the role's own
    Subject.Name ]   ; a task of its own
  Event.[
    Started
    ToolUsed.String
    ContextMeasured.{
      Tokens.Integer
      Window.Integer }
    Stopped ] ]
[]
[]
```

`Voice` inside Metaflow carries nothing: the flow continues the voice its role names, written once. Three flows, written:

```
{ f5a6e9              ; this seat
  Voice.{ Psyche Primary }
  Some.Voice
  Some.b27767 }       ; its predecessor

{ 7f3a21              ; a subject
  Voice.{ Mind Secondary }
  Some.Subject.ethos
  None }

{ 3c91e0              ; a subflow
  Worker.read-trivial
  None
  None }
```

## 2. "How do I know which flow a metaflow is?"

Your comments: "I'm going to look up by metaflow", and "what about the flow history of a certain metaflow? ... we wouldn't want to keep the entire history."

Two records in Flow's Memory. The flow record is one per run; the lineage record is one per metaflow and is what a lookup by metaflow reads: its current flow and its lock. History is not a third record: each flow names its predecessor, so a metaflow's history is the walk back from its current flow, and forgetting old flow records is how the history is trimmed, nothing else to maintain.

```
Memory
[ curriculum:[ Name Sha256 ]
  flow:[ FlowId Role Metaflow Event ] ]
[ Flow.{             ; one per run
    FlowId
    Role
    Option<Metaflow>
    Predecessor.Option<FlowId>
    State.[
      Running
      Stopped ]
    ; what it was composed from
    Read.Vector<Read.{
      Name
      Sha256 }>
    Events.Vector<Event> }
  Lineage.{          ; one per metaflow
    Role
    Metaflow
    Current.Option<FlowId>
    Lock.[
      Open           ; Current receives
      Refreshing.FlowId  ; the successor
      Ended ] } ]
```

Today Flow holds a flow row and role (`FlowNode`, `Caller`), and an events table on disk that survives a restart, keyed by a flow id String; no lineage, no predecessor, no lock.

## 3. The lock

Your words: the lock is needed to roll a metaflow over into a new flow, and Message later uses it to know whether a message can reach a flow.

The lock is the lineage's state. Open: letters reach the current flow. Refreshing: a successor is being composed and spawned; a letter waits in Flow and is delivered to whichever flow is current when the lock opens, so nothing is lost in the handover and nothing reaches a flow that is about to be reaped. Ended: a letter is returned to its sender. Only Flow sets the lock; a refresh takes it first and releases it last.

## 4. "It's more like 20% to 40%"

Measured, in a transcript of your secretary's seat: a flow's context on a turn is the sum of the last assistant record's three input counts (fresh, cache written, cache read); Claude Code's own status line uses the same sum. One turn there read 111,054 tokens; the seat reached 436,496 before a manual compaction. The window comes from the harness's model catalog: 1,000,000 tokens for the Claude models in use; Codex writes its window into each usage record, 258,400. The Stop hook already receives the transcript path and reads nothing from it today.

The hook reports `ContextMeasured` at each Stop. Two marks on the window, per role, defaults 20 and 40: at the first the flow is told to write its handover; at the second, or at the Stop after the handover is written, Flow refreshes. For a 1,000,000-token window that is 200,000 and 400,000 tokens.

```
Threshold.{          ; per role, percent
  Handover.Integer   ; 20: write it
  Refresh.Integer }  ; 40: refresh now
```

## 5. The refresh is software

Drawing: a gauge filling left to right; at the first mark a hand types `write your handover` into the pane; at the second mark the lock closes, a new bead appears, the old bead greys out, the lock opens on the new bead.

The steps, each one operation, no model deciding any of it: Lock the lineage on the successor's id; Compose from the role record, the predecessor's handover as the brief, and the launch's modules; Open, Spawn, Bind; Reap the predecessor; set Current; Unlock. The handover is a small paragraph, as your Sun record says: only what is still undecided passes to the next flow; what was decided went into context modules, and the successor gets it from there.

```
Signal
[ flow:[ FlowId Role Metaflow Flow ] ]
[ Launch.{
    Role
    Option<Metaflow>
    Modules.Vector<Name>
    Brief.String }
  Refresh.Metaflow   ; by its name
  End.Metaflow       ; a subject
  Current.Metaflow ] ; the messenger asks
[ Launched.Flow
  Refreshed.{
    Flow             ; the successor
    FlowId }         ; reaped
  Ended.Metaflow
  Current.[
    Running.FlowId
    Refreshing       ; wait
    Ended
    Unknown ]
  Refused.[
    Locked.Metaflow  ; already refreshing
    NoRole.Role
    NoLineage.Metaflow ] ]
[]
```

Your request to review the operation type: today's Operation root has fourteen operations (Compose, Reserve, Record, Register, Confirm, Open, Spawn, Bind, Title, Submit, Continue, Close, Prune, Release) and the refresh adds four. Shown here are the four, in the same root:

```
Operation
[ ...                ; the fourteen stand
  Tell.{             ; type into a pane
    FlowId
    String }
  Lock.{
    Metaflow
    FlowId }         ; the successor
  Reap.FlowId        ; Close + Stopped
  Unlock.Metaflow ]
[ Told
  Locked
  Reaped.FlowId
  Unlocked
  Failed.[
    AlreadyLocked
    NotLocked ] ]
```

## 6. "I'm curious what the end is"

Your comment: an end goal in a limited-size string could go there, "but we can put this into Notion maybe."

A voice has no end. A subject ends by judgment: the subject's own flow, or the voice that launched it, says `End`; the lineage's lock becomes Ended, its current flow is reaped, and a letter to it is returned. No end-goal field is in the record: the judgment is a flow's, made in its context, and the end is recorded when it happens. The limited-size string stays your notion.

## 7. What comes after

A voice launches subjects under itself and refreshes itself; Field launches voices at boot; later Flow does both on its own, as you said flow spawning will be automated. Clusters that expand and contract, three to seven, stand in bad807's records, untouched here.

## Rulings

1. A flow is `{ FlowId Role Option<Metaflow> Predecessor }`, `Role.[ Voice Worker ]`, `Metaflow.[ Voice Subject.Name ]` with Voice meaning the role's own: yes, or amend.
2. Two records, Flow and Lineage; history by predecessor walk, trimmed by forgetting: yes, or amend.
3. The lock as the lineage's state, Open, Refreshing, Ended, with letters waiting through a refresh and returned after an end: yes, or amend.
4. Thresholds as percent of the model's window, 20 handover and 40 refresh by default, per role: (a) yes. (b) absolute tokens: your numbers.
5. The refresh steps and the four operations added: yes, or amend.
6. No end-goal field; a subject ends by `End` from its own flow or its voice: (a) yes. (b) add `End.String` with a size limit you name.
<!-- to-the-living:end -->
