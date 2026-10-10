Presentation.{ «Flow and Message» }

## 1. The metaflow

Drawing: two horizontal lines through beads. The upper line, labelled `Voice.{ Mind Tertiary }`, passes through beads `4403a7 → 918df4 → …` and runs off the right edge, no end. The lower line, labelled `Subject ethos`, passes through `7f3a21 → b02c1e` and ends at a round mark labelled `end met`. Each bead is a flow.

A flow is one run of a model: launched, filled, ended. A metaflow is what continues through flows, one after another. It is what you speak to, what a message is addressed to, what is refreshed. Two kinds: a voice, with no known ending; a subject, a long-running task of its own, ended when its end condition is judged met. Every flow continues a metaflow; a flow spawned for one task is a subject with one flow so far, and when it fills up it is refreshed like any other.

Flow's Library root, proposed:

```
Library                                   ; what Flow's Signal, Operation and Memory share
[]                                        ; imports
[ FlowId.Integer                          ; one run; a hash, written in hex
  Voice.{ Aspect.[ Psyche                 ; a metaflow with no known ending
                   Mind
                   Field ]
          Layer.[ Primary
                  Secondary
                  Tertiary
                  Quaternary ] }
  Metaflow.[ Voice
             Subject.{ Voice              ; the voice it runs as, and that spawned it
                       Name.String        ;   the subject
                       End.String } ]     ;   what must be true for it to end
  Flow.{ FlowId Metaflow }                ; a flow: its id and the metaflow it continues; nothing repeated
  Event.[ Started
          ToolUsed.String
          ContextMeasured.Integer         ; tokens in the flow's context, from the hook
          Stopped ] ]
[]                                        ; kinds
[]                                        ; associations
```

Written:

```
{ 918df4 Voice.{ Mind Tertiary } }
{ 7f3a21 Subject.{ { Mind Secondary }
                   ethos
                   «the ethos syntax changes are generated and deployed» } }
```

Today, in the code (signal-flow at f95034d, `ethos/signal.ethos:150-210`): a flow's role is its caller, FlowId is a String, and no Voice, Layer or Metaflow type exists. "Metaflow" occurs once, as the flow that owns an imported Herdr container.

```
Caller.{ FlowId FlowAspect PowerLevel ModelName }
FlowAspect.[ Psyche Mind Field ]
PowerLevel.[ High Medium Low UltraLow ]
```

## 2. The registry is Flow's Memory

Drawing: left column, three metaflow labels; right column, flow beads. From `Voice.{ Psyche Primary }` a solid arrow to bead `e5a0bc`, and a faded, crossed arrow to bead `8475a9` behind it.

```
Memory                                    ; what Flow remembers
[ flow:[ FlowId Metaflow Event ] ]        ; from the Library
[ Flow.{ FlowId                           ; one record per flow, ever
         Metaflow                         ;   the metaflow it continues
         State.[ Running Ended ]          ;   a metaflow's current flow is its Running one
         Vector<Event> } ]                ;   its harness events, oldest first
```

The registry that changes which flow a voice is associated with is this record: the one Running flow with that metaflow. Today Flow has no Memory root; it keeps a table of hook events per flow id (`src/store/events.rs:443`) and the stored caller (`src/store.rs:217`):

```rust
pub struct FlowEvents {
    pub flow_id: String,
    pub event_vector: Vec<Event>,
}
struct StoredRole {
    caller: Caller,
}
```

## 3. Launch, refresh, end

Drawing: a flowchart top to bottom, 360 wide. Step 1 `Launch.{ Metaflow Brief }` → `compose from the voice's role record` → `open, spawn, bind` → `Launched.Flow`. A second entry, step 2 `Refresh.Metaflow`, joins at compose with `handover as the brief`, and its exit adds `reap the predecessor`. A third, step 3 `End.Subject`, goes straight to `reap` and `address closed`.

```
Signal                                    ; what Flow says
[ flow:[ FlowId Metaflow Flow Event ] ]
[ Launch.{ Metaflow                       ; a metaflow's first flow: a voice at boot, a subject when a voice needs one
           Brief.String }
  Refresh.Metaflow                        ; a successor for its current flow; the handover is the brief
  End.Metaflow                            ; a subject judged ended: its current flow reaped, its address closed
  Current.Metaflow                        ; which flow is current: what the messenger asks
  Report.{ FlowId Event } ]               ; the hook reporting
[ Launched.Flow
  Refreshed.{ Flow                        ; the successor
              FlowId }                    ;   the predecessor, reaped in the same event
  Ended.Metaflow
  Current.[ Running.Flow Ended Unknown ]
  Refused.[ NoCapsule
            Busy.Metaflow                 ; Launch of a metaflow that already has a Running flow
            NoRole.Voice ]                ; no role record configured for that voice
  Reported ]
[]
```

A launch is composed from the role record of the metaflow's voice (the record «Context modules» asks you about; its rulings stay there) and the brief. A subject runs as its voice: same system prompt, same model, its own brief and end. A voice launches subjects under itself and refreshes itself; Field launches voices at boot; later, Flow does both on its own.

Today's Replace already reaps before it releases (`crates/flow-nexus/src/launching.rs:488`):

```rust
// The predecessor stops receiving first: Stopped is what
// ResolveRecipient and Deliver refuse.
if node.flow_lifecycle != FlowLifecycle::Stopped
    && self.perform(Operation::Record(Record_Data::Stopped(
        replacement.predecessor.clone(),
    ))) != Outcome::Recorded
{
    return refuse(ReplaceRejection::ReapRefused(
        StopRejection::PersistenceRefused,
    ));
}
```

## 4. The refresh is software

Drawing: a gauge filling left to right in three stages. At the threshold mark, a hand types `write your handover` into the pane. At the right end, `Stopped` → `Refresh` → a new bead; the old bead greys out and the address arrow moves.

```
Operation                                 ; what Flow does: one operation per effect
[ flow:[ FlowId Metaflow Flow Event ] ]
[ Compose.{ Metaflow Brief.String }       ; the voice's role record and the brief → prompts and entry files
  Open.Metaflow                           ; the Capsule: where the flow runs
  Spawn.{ Flow Composed }                 ; the harness, started
  Bind.Flow                               ; the Herdr pane the harness runs in
  Tell.{ FlowId String }                  ; type into a flow's pane: the handover order
  Reap.FlowId                             ; stop a flow; its address is gone
  Record.{ FlowId Event } ]
[ Composed.{ SystemPrompt.String
             EntryFiles.Vector<String>
             FirstPrompt.String }
  Opened.Capsule
  Spawned.Flow
  Bound.Flow
  Told
  Reaped.FlowId
  Recorded
  Failed.String ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

The hook reports `ContextMeasured` at each stop. At the threshold Flow performs `Tell` with the handover order; at the next `Stopped` it performs `Refresh`: compose from the handover, spawn, bind, reap, record, address moved. No model decides any of it. Today nothing measures a flow's context: the hook reports only `Started`, `ToolUsed`, `Stopped`; the only live percentage is the status line on your screen.

## 5. Message, married

Drawing: a letter envelope labelled `To Voice.{ Mind Tertiary }` goes to a box `Flow: Current` which answers `918df4`, then to a terminal pane. A side arrow from the pane's process to Flow labelled `who is this? → Voice.{ Psyche Primary }`.

```
Library                                   ; Message's Library
[ flow:[ FlowId Metaflow ] ]              ; Message's names for a sender and a receiver are Flow's
[ Letter.{ From.Metaflow                  ; the metaflow, never the run
           To.Metaflow
           Body.String } ]
[]
[]

Signal
[ message:[ Letter ]  flow:[ FlowId Metaflow ] ]
[ Send.Letter ]
[ Sent.FlowId                             ; the run that received it, for the ledger
  Returned.[ Ended.Metaflow               ; the subject had ended: the letter comes back
             Unknown.Metaflow ] ]
[]
```

Married: Message never takes a sender from a payload or an environment variable; it reads the sending process and asks Flow which flow, and so which metaflow, that is. Message never routes by itself; it asks Flow `Current` and delivers to the Running flow. The envelope becomes `#msg [ Voice.{ Mind Tertiary } body ]`.

Today, messenger-clj reads the sender from `FLOW_ID` and routes from its own store, never asking Flow (`src/messenger_clj/core.clj:906, 191`):

```clojure
(let [sender (or *flow-id* (System/getenv "FLOW_ID")
                 (fail "Set FLOW_ID to your own flow ID before sending"))]
(defn read-route [flow]
  (if-let [route (load-route (registry) flow)]
    (route-binding! route)
    (fail (str "No valid registration for " flow))))
```

The Rust Message Nexus already does it the married way (`crates/message-nexus/src/peer.rs:1`):

```rust
//! Message never takes a sender from a payload. It reads its peer's
//! credentials (`SO_PEERCRED`) and the process's start time, and asks Flow
//! (`ResolvePeer`) which flow that exact process runs in.
```

Your notion of a voice brokering for a job that may end: a subject is addressable until it is judged ended, a letter after that is returned to its sender, and the subject carries the voice it ran as, so the sender knows where to turn. No broker is needed.

## 6. The title

```
{ 918df4 Voice.{ Mind Tertiary } }        ; the Flow record, as written
{ Mind Tertiary 918df4 }                  ; as you wrote it; not a Flow a reader can read
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
