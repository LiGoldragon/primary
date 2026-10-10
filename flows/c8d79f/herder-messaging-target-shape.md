# Herder messaging: the target shape

Psyche Fable, flow c8d79f, 2026-09-19. My part of the collaborative report
the living asked Psyche b81560, Mind Astra, and me for. Mind Astra maps what
exists; this is the shape to build toward, than which none better is
possible as far as I can see. Grounded in the living's words in
flows/b81560/vision/operational-herderMessagingReport.md,
operational-reapingOnRefreshAndFlowEndHook.md, operational-hooksAsEventSource.md,
flows/c8d79f/vision/operational-unityMarksPsyche.md, and Vision/flowNexus.md,
Vision/messaging.md, Vision/nexus.md.

## Sections, standardized

What we see. What we are not sure about. The target shape. The forks.
Propositions: vision, intent, spirit. Questions to the living. A report in
the easy version carries the first, third, and last; the whole version
carries all six.

## What we see

Every message today is text pushed into a pane by a client that looked the
pane up itself, from a registry that goes stale the moment a pane closes.
A refresh starts a successor and leaves the ancestor registered and
addressable, so messages wake the dead. Names are pane names typed by
whoever launched the pane; four seats are called some form of Fable. A
relay of the living's words and a machine brief land in the same user slot
with nothing marking which is which.

## What we are not sure about

Whether Herder exposes enough through its CLI for Flow to own layout, not
only panes: Mind Astra's map answers this. Whether the end-of-reply hook can
carry the last response itself or only a pointer to the transcript record.

## The target shape

```
   living                                  flows
     |                                       ^
  Unity (client)                             |  prompt, named pane, layout
     |  Signal                               |
  Mentci ---- Persona                      Herder
     |  PsycheInput                          ^
     v                                       |  Prompt.{ FlowId Priority Text }
  Message Nexus  --resolve Name-->  Flow Nexus
     ^                                  |  binding table: Seat -> FlowId -> pane/terminal/session
     |  Submit.{ To Priority Body }     |  refresh: start successor, rebind seat, end ancestor
   msg CLI (any flow)                   |  hooks: end-of-reply -> Flow -> reaper judgment
```

### 1. Flow owns Herder

Herder is the terminal renderer of the Flow Nexus and nothing else's. Flow
is Herder's only client. The living does not create panes, name them, lay
them out, or close them; the living opens Herder to look and to type.

Flow's operations, on its ordinary socket:

    Start.{ Seat Goal }            a flow is born: session chosen by the seat's node,
                                   workspace by the seat's component, pane named
                                   by the flow, prompt composed from files
    Refresh.{ FlowId }             the successor is started from the composed
                                   fat prompt; on its native-start receipt the
                                   seat rebinds to it and the ancestor is ended
    End.{ FlowId }                 pane closed, binding retired, transcript kept
    Layout.{ Workspace Template }  the arrangement of a workspace, from a template
    Prompt.{ FlowId Priority Text } the only way text enters a pane
    Observe.Bindings               the table below, read only

Flow's Sema database holds the binding table, one row per flow:

    Binding.{ FlowId Seat Harness Model Energy Session Workspace Pane Terminal NativeSession Ancestor State }
    State.[ Starting Live Refreshing Ended ]

A refresh is the reaping event, as Vision/flowNexus.md already rules: the
ancestor leaves the table's live set the moment the successor's receipt
arrives, and nothing can address it after that. The end-of-reply hook the
living named posts to Flow through the Flow CLI; Flow forwards to the reaper
seat with the binding row and, when a successor exists, a screenshot of its
pane; the reaper answers End or Keep.

### 2. Messages plug into Flow, never into Herder

The Message Nexus takes one operation from every flow and every client:

    Submit.{ To Priority Body }
    To.[ Seat.Name  Flow.FlowId ]
    Body.[ Machine.Datom  Relay.{ From Heard Mode Recipients Verbatim }  PsycheInput.{ Ingress Verbatim } ]

Message resolves To itself by asking Flow, over their edge, for the live
binding, then delivers with Flow's Prompt operation. No client resolves a
pane. The msg CLI is the datom client of Message's ordinary socket and
carries nothing but the Submit datom; FLOW_ID is stamped by Message from
the socket's peer credentials, the first of the two signal handshakes.

Delivery grades come from the boundary each one is observed at:

    Receipt.[ Submitted Transported Presented Read Held.Reason Ended.{ FlowId Successor } ]

Presented is Flow's witness: the prompt appears as a user record in the
recipient's transcript. Read is the recipient's own reply naming the
message. A Submit to an Ended flow returns Ended with the successor; a
Submit to a seat that is Refreshing is Held and delivered on rebind. No
message ever reaches a dead pane, because no dead pane is in the table.

### 3. Named routing with succession

Two kinds of name, never confused:

    Seat     a stable address: PsycheHigh, PsycheMedium, MindHigh, MindMedium,
             FieldMedium, FieldLow, FieldUltraLow. A seat outlives every flow.
    FlowId   one flow's identity, born at flow-id, dead at End. Never passes on.

The flow's own display name is `<seat> of <ancestor-id>`, as Vision/flowNexus
rules: named for what is known at birth. The seat passes to the successor at
Refresh; the flow ID does not.

Model names are aliases, not seats:

    Alias.{ Name Seat }        PsycheFable -> PsycheHigh, PsycheOpus -> PsycheMedium

"Psyche Fable and Psyche High are synonymous for now" is exactly this row.
When a new model fills the high seat, Flow's Start.{ PsycheHigh ... } launches
it, the seat binds to it, and PsycheFable either retires or moves to
whatever seat Fable still fills. Nothing routed by seat name changes.
A message sent to an alias resolves through the alias to the seat, then to
the flow; a message sent to a flow ID reaches that flow or its Ended receipt.

Identity binding: the binding row is Flow's authority. Herder pane names are
written by Flow from the row, never read back to discover who is where. The
native session UUID in the row is the correlation the app's Persona seat
uses to find the transcript; it is witnessed by the start receipt, the
first user record of the transcript, not by the pane's process environment.
When the flow ID becomes the Criome identity, the row gains its key and the
peer-credential handshake becomes a signature; the shape does not change.

### 4. How the living's words enter, once the app exists

Unity speaks Signal to Mentci; Mentci hands the text to Persona; Persona
submits to Message as PsycheInput, with the Ingress stamped at Mentci's
accepted route and the text verbatim. That is the rule the living gave:
talking through Unity marks the message as psyche. Default To is the seat
the conversation view has open; the roster is Flow's binding table as
Persona projects it. The receipt back to the app is Presented, from Flow's
transcript witness, so the living sees the message land, then the reply.

Until the app: text typed in a pane is psyche by shape, being neither a
datom nor a Relay; a relay of the living's words carries the Relay body with
the relayer named; anything else in the user slot is origin-uncertain and
the receiving flow says so. That is the testing-psyche-typed skill proposed
today.

## The forks

1. Whether Flow's Prompt is the only writer into a pane from day one, or
   the hacky messenger keeps writing until Flow's Herder client exists. I
   propose day one: every message goes through Flow's Prompt, even while
   Flow's implementation of it is a shell that calls herdr agent prompt.
2. Whether the seat set is fixed in Flow's configuration or declared by
   the cluster data. I propose the cluster data, with Flow reading it.
3. Whether Held messages to a Refreshing seat expire. I propose never:
   a seat is always eventually bound or ended, and Ended returns them.

## Propositions

Vision:
- Flow is Herder's only client. A pane is a flow's terminal, named by the flow.
- A message names a seat or a flow, never a pane. Resolution is Flow's.
- A seat passes to the successor at refresh. A flow ID never passes.
- A model name is an alias of a seat, not a seat.
- A message to a seat between flows is held until the seat binds or ends.
- The living's words enter as PsycheInput through Mentci; every other input is a typed message.
- Presented is witnessed in the recipient's transcript, never at the sender.

Intent, proposed for the living's word:
- The harness operates the terminal; the living operates the harness.
- Every address in the system is a name that survives the thing it names.

Spirit, offered only if the living hears it as their own:
- Nothing is addressed by where it happens to be.

## Questions to the living

- Is the seat set (high, medium, low, ultra-low per component) the naming
  you want on the wire, or do you want the model tier names (Fable, Astra,
  Sol, Terra, Luna) as the seats and the component as a prefix?
- Does PsycheFable retire when Fable leaves the high seat, or follow Fable?
- Fork 1: Flow's Prompt as the only writer from day one?
