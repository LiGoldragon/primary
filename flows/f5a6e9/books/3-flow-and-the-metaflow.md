<!-- to-the-living:start -->
Presentation.{ «Flow and the metaflow» }

## Proposal 1: Vision/flowNexus.md, a flow, its role and its metaflow

Lines removed: none. Lines added, as a new section after "A session is named after its direct ancestor":

```
## A flow may continue a metaflow

A flow has a flow id and a role, and may
continue a metaflow. A role is a voice or a
worker (read-trivial, write-ordinary, tester,
book). A metaflow is the voice of the flow's
own role, or a named subject. A subflow or a
one-task flow continues nothing. A flow that
is a metaflow is addressed by its long-term
metaflow name, never by its flow id.
```

Lines added to the Library root of the signal-flow crate, file `crates/signal-flow/ethos/signal.ethos`:

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

Ruling 1.

## Proposal 2: the Flow repository, new file crates/flow-nexus/ethos/memory.ethos

Lines removed: none. Today Flow holds a flow row and role, and an events table on disk that survives a restart, keyed by a flow id String; no lineage, no predecessor, no lock. Lines added: two records. The flow record is one per run. The lineage record is one per metaflow, and a lookup by metaflow reads it: its current flow and its lock.

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

Lines added to Vision/flowNexus.md, after the section of Proposal 1:

```
## A metaflow's history is its predecessors

History is not a third record. Each flow
names its predecessor, so a metaflow's history
is the walk back from its current flow.
Forgetting old flow records is how the history
is trimmed; nothing else is maintained.
```

Ruling 2.

## Proposal 3: Vision/flowNexus.md, the lock

Lines removed: none. Lines added:

```
## The lock is the lineage's state

Open: letters reach the current flow.
Refreshing: a successor is being composed and
spawned. A letter waits in Flow and is
delivered to whichever flow is current when
the lock opens, so nothing is lost in the
handover and nothing reaches a flow about to
be reaped. Ended: a letter is returned to its
sender. Only Flow sets the lock; a refresh
takes it first and releases it last. Message
reads the lock to know whether a letter can
reach a flow.
```

Ruling 3.

## Proposal 4: Vision/flowNexus.md, thresholds on the context window, and the Library ethos

Lines removed: none. Lines added to Vision/flowNexus.md:

```
## A refresh follows the context's fill

A flow's context on a turn is the sum of the
last assistant record's three input counts:
fresh, cache written, cache read. The window
comes from the harness's model catalog:
1,000,000 tokens for the Claude models in use;
Codex writes its window into each usage
record, 258,400. The Stop hook reads the
transcript and reports ContextMeasured at each
Stop. Two marks on the window, per role,
default 20 and 40 percent. At the first the
flow is told to write its handover. At the
second, or at the Stop after the handover is
written, Flow refreshes.
```

Lines added to the role record:

```
Threshold.{          ; per role, percent
  Handover.Integer   ; 20: write it
  Refresh.Integer }  ; 40: refresh now
```

Ruling 4.

## Proposal 5: Vision/flowNexus.md, the refresh is software; signal-flow and operation.ethos

Lines removed: none from the Vision. In Vision/flowNexus.md the section "A replaced session is reaped by the refresh itself" stands; this follows it:

```
## The refresh is a sequence of operations

No model decides any step. Lock the lineage on
the successor's id; compose from the role
record, the predecessor's handover as the
brief, and the launch's modules; open, spawn,
bind; reap the predecessor; set Current;
unlock. The handover is a small paragraph:
only what is still undecided passes to the
next flow. What was decided went into context
modules, and the successor gets it from there.
```

Lines added to `crates/signal-flow/ethos/signal.ethos`, its Signal and Output roots:

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

Lines added to `crates/flow-nexus/ethos/operation.ethos`: the Operation root has fourteen operations today (Compose, Reserve, Record, Register, Confirm, Open, Spawn, Bind, Title, Submit, Continue, Close, Prune, Release); four are added, the fourteen stand.

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

Ruling 5.

## Proposal 6: Vision/flowNexus.md, the end of a flow

Lines removed: none. Lines added:

```
## A voice has no end; a subject ends by judgment

The subject's own flow, or the voice that
launched it, says End. The lineage's lock
becomes Ended, its current flow is reaped, and
a letter to it is returned. No end-goal field
is in the record: the judgment is a flow's,
made in its context, and the end is recorded
when it happens.
```

Ruling 6.

## Rulings

1. Proposal 1: a flow is `{ FlowId Role Option<Metaflow> Predecessor }`, `Role.[ Voice Worker ]`, `Metaflow.[ Voice Subject.Name ]`, Voice meaning the role's own. (a) Land it as written. (b) Amend it, and say how.
2. Proposal 2: two records, Flow and Lineage; history by predecessor walk, trimmed by forgetting. (a) Land it as written. (b) Amend it, and say how.
3. Proposal 3: the lock as the lineage's state, Open, Refreshing, Ended, with letters waiting through a refresh and returned after an end. (a) Land it as written. (b) Amend it, and say how.
4. Proposal 4: thresholds as percent of the model's window, 20 handover and 40 refresh by default, per role. (a) Land it as written. (b) Absolute tokens instead: give your numbers.
5. Proposal 5: the refresh steps and the four added operations. (a) Land them as written. (b) Amend them, and say how.
6. Proposal 6: no end-goal field; a subject ends by End from its own flow or its voice. (a) Land it as written. (b) Add `End.String` with a size limit you name.
<!-- to-the-living:end -->
