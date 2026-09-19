# Herder messaging — detailed report

Flow b81560, 2026-09-19. Synthesized from Mind Astra 0ab019 (components),
Psyche Fable c8d79f (design), Psyche b81560 (coordination).

## What we see

### Three messaging systems, none complete

| System | Transport | Resolution | Receipt | Status |
|---|---|---|---|---|
| Hacky Messenger (hm-send) | herdr agent prompt | HM registry file | Transported only | Working, stale registrations |
| Central messenger (tools/msg) | pane send-text to messenger pane | Persisted pane_id file | None | Dead — pane w4:p3 gone |
| Raw herdr agent prompt | herdr agent prompt | Manual name | Transported only | Working, no identity |

### Infrastructure running but empty

Message Nexus 0.12 is live (PID 3297488) with ordinary socket
`/run/user/1001/message/message.sock` and owner socket
`message-owner.sock`, both mode 0600. Source-inspected capabilities:
Submit/inbox, identity assignment, endpoint binding, registry query,
FlowDeliver, FlowAnnounceIdle, Deliver with persisted attempt receipts,
thread query/subscription/index. Agent registry: empty.

Flow Nexus is live (PID 3727637) with ordinary socket
`/run/user/1001/flow/flow.sock` and meta socket `flow-meta.sock`.
CLI: `flow start <type>`, `flow restart <id>`, `flow resolve <id>`.
Resolve b81560 and 0ab019 both return `RecipientResolutionRejected.UnknownFlow`.
No flows registered.

### Break points witnessed

1. **No atomic binding.** Herdr agent list → agent prompt is two calls;
   the pane can die between them. Current messenger checks name/pane/terminal
   before and after, but that is not an atomic delivery.

2. **Dead pane, live registration.** When a harness exits but its pane
   survives, text injection hits whatever process remains. HM and herdr
   have no way to distinguish a live harness from an empty shell.

3. **Refresh leaves ancestors addressable.** A successor starts; the
   ancestor stays registered; messages wake flows that should be reaped.
   This is the living's complaint: "Why are you sending messages to flows
   that are over?"

4. **No origin marking.** A relay of the living's words and a machine
   brief land in the same user slot with nothing marking which is which.

## What we are not sure about

- Whether Herder 0.8.2 exposes enough CLI surface for Flow to own layout
  (workspace creation, pane arrangement, split management), not only panes.
  Mind Astra's map shows agent/pane/api surface but not workspace template
  operations.

- Whether the end-of-reply hook can carry the last response itself or only
  a pointer to the transcript record.

- Automatic list cleanup timing in Herder when a harness exits — not
  verified by killing a harness.

## The target shape

### 1. Flow owns Herder

Herder is the terminal renderer of the Flow Nexus. Flow is Herder's only
client. The living does not create panes, name them, lay them out, or close
them; the living opens Herder to look and to type.

```
Flow operations (ordinary socket):

    Start.{ Seat Goal }              session born, workspace/pane chosen by seat
    Refresh.{ FlowId }              successor started, seat rebound, ancestor ended
    End.{ FlowId }                  pane closed, binding retired, transcript kept
    Layout.{ Workspace Template }   workspace arrangement from template
    Prompt.{ FlowId Priority Text } the only way text enters a pane
    Observe.Bindings                the binding table, read only
```

```
Flow's Sema binding table, one row per flow:

    Binding.{ FlowId Seat Harness Model Energy Session
              Workspace Pane Terminal NativeSession Ancestor State }
    State.[ Starting Live Refreshing Ended ]
```

A refresh is the reaping event: the ancestor leaves the live set the moment
the successor's native-start receipt arrives. The end-of-reply hook posts to
Flow through the Flow CLI; Flow forwards to the Luna reaper with the binding
row and, when a successor exists, a screenshot of its pane; the reaper
answers End or Keep.

### 2. Messages go through Message Nexus, resolve through Flow

```
Message operation:

    Submit.{ To Priority Body }
    To.[ Seat.Name  Flow.FlowId ]
    Body.[ Machine.Datom  Relay.{ From Heard Mode Recipients Verbatim }
           PsycheInput.{ Ingress Verbatim } ]
```

Message resolves To by asking Flow over their edge for the live binding,
then delivers with Flow's Prompt. No client resolves a pane. The msg CLI
is the datom client of Message's ordinary socket; FLOW_ID is stamped by
Message from the socket's peer credentials (the first signal handshake).

```
Receipt grades:

    Receipt.[ Submitted Transported Presented Read
              Held.Reason Ended.{ FlowId Successor } ]
```

Presented is witnessed in the recipient's transcript (the prompt appears
as a user record). Read is the recipient's own reply naming the message.
Submit to an Ended flow returns Ended with the successor. Submit to a
Refreshing seat is Held and delivered on rebind. No message reaches a dead
pane because no dead pane is in the table.

### 3. Named routing with succession

```
Two kinds of name:

    Seat      PsycheHigh, PsycheMedium, MindHigh, MindMedium,
              FieldMedium, FieldLow, FieldUltraLow
              Outlives every flow. Passes to the successor at refresh.

    FlowId    Born at flow-id, dead at End. Never passes on.

Display name: <seat> of <ancestor-id>
```

```
Model aliases:

    Alias.{ Name Seat }
    PsycheFable  -> PsycheHigh
    PsycheOpus   -> PsycheMedium
```

When a new model fills the high seat, Flow starts it under PsycheHigh,
the seat binds to it, and PsycheFable either retires or moves. Nothing
routed by seat changes.

### 4. Living's words enter as PsycheInput

```
Unity --> Mentci --> Persona --> Message (as PsycheInput)
    Signal       PsycheInput      Submit.{ To Body.PsycheInput.{ Ingress Verbatim } }
```

The Ingress is stamped at Mentci's accepted route so every flow knows it
is hearing the living. Default To is the seat the conversation view has
open. Until the app: text typed in a pane is psyche by shape (neither a
datom nor a Relay); everything else in the user slot is origin-uncertain.

## The forks

1. **Flow's Prompt as sole writer from day one?** Fable proposes yes, even
   while Flow's implementation of Prompt is a shell calling herdr agent
   prompt. This eliminates the dual-path problem immediately.

2. **Seat set in Flow's config or cluster data?** Fable proposes cluster
   data, with Flow reading it. This connects to the hardware type vision
   (operational-clusterDataAndHardwareAnatomy.md).

3. **Do Held messages expire?** Fable proposes never: a seat is always
   eventually bound or ended, and Ended returns them.

## Propositions

### Vision

- Flow is Herder's only client. A pane is a flow's terminal, named by
  the flow.
- A message names a seat or a flow, never a pane. Resolution is Flow's.
- A seat passes to the successor at refresh. A flow ID never passes.
- A model name is an alias of a seat, not a seat.
- A message to a seat between flows is held until the seat binds or ends.
- The living's words enter as PsycheInput through Mentci; every other
  input is a typed message.
- Presented is witnessed in the recipient's transcript, never at the
  sender.

### Intent (proposed)

- The harness operates the terminal; the living operates the harness.
- Every address in the system is a name that survives the thing it names.

### Spirit (offered only if the living hears it as their own)

- Nothing is addressed by where it happens to be.

## Questions to the living

1. Is the seat set (high/medium/low/ultra-low per component) the wire
   naming, or model tier names (Fable/Astra/Sol/Terra/Luna) as seats
   with component prefix?
2. Does PsycheFable retire when Fable leaves the high seat, or follow
   Fable?
3. Flow's Prompt as sole writer from day one — yes or no?

## Sources

- Mind Astra 0ab019: live CLI/process/socket receipts 2026-09-19;
  repos/message/src/{command,client,engine}.rs;
  repos/flow/crates/flow-nexus/src/{lib,herdr}.rs;
  installed Herder help and tools/{msg,messenger,msg-psyche-poc}
- Psyche Fable c8d79f: flows/c8d79f/herder-messaging-target-shape.md
- Mind Sol effa1b: initial infrastructure probe 2026-09-19
- Living vision: flows/b81560/vision/operational-herderMessagingReport.md,
  operational-reapingOnRefreshAndFlowEndHook.md,
  operational-hooksAsEventSource.md
