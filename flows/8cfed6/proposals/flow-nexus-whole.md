Presentation.{ «The Flow Nexus, retaken» }

# The Flow Nexus, retaken

Created by Fable; records gathered by Opus

### Proposal 1: vision:flow-nexus · psyche-belief › vision/flow-nexus.md — whole, retaken

**Comment** The module is rebuilt whole from your words: messaging folded in, the Flow Nexus the one send path, the perennial vision alone, and the Ethos carried in it so the next machine reads the design in code. The horizon-marked lines wait for their own modules.

```text
---
description: The Flow Nexus — the Nexus that starts, names, tracks, refreshes and ends flows and carries every request between them; its metaflows, queue, belief modules, capsule, versions and heartbeat.
dependencies: [vision-nexus, vision-ethos, vision-datom]
---

## Metaflows

A metaflow is one address, { Aspect topic Layer }, that continues through several flows one after another; a flow is its current run. What is addressed is the metaflow; a peer is known only as its metaflow. A topic is an open enum: the constant topics, core among them, are fixed, and the users and the machine extend the set with camelCase identifiers; core is the permanent topic of its aspect, the one that keeps the machine going.

A topic lives on; when idle, its flows are turned off and its address stays. A metaflow sleeps so that an idle session keeps no harness: when its turn ends with nothing waiting, the harness closes and the transcript stays. A metaflow wakes when a request needs it, and the flow woken for it is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.

A flow runs one model, linear and very limited: a language model, a System 1 model, an audio model or a video model. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence.

## Identity

A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from it. The Flow Nexus gives a flow its id and tells it its metaflow in its system prompt. Every call to the Flow Nexus is identified by the calling process, so anybody may call it, a flow for its own refresh among them. In the chat and between flows a flow is named by its metaflow; the id is for the ledger and for finding the transcript, and a debugging query exposes it when one must be explicit.

## Starting a flow

Starting flows cheaply is the cornerstone of the system: clean flows, specialized flows and refreshed flows, each with a clean, on-point context, taken down as easily as they are started. A launch is a small datom: the metaflow, how far back it remembers, and a brief of a small paragraph; everything else about the launch is configuration the Flow Nexus holds for that metaflow, loaded as data from files in the belief repositories, changed over the meta socket, held in its own Memory.

The Flow Nexus composes the prompts from the metaflow's declaration: the belief modules named in its registry, the raw records its remembering names, and the brief. Spirit and intent sit in the system prompt; vision and the rest go in the first prompt, brimming with vision, in as many prompts as it takes, sent one right after another, so that the start is one model call. A module the declaration names and the clones lack is reported in its place in the prompt, as expected and not found, and the launch proceeds. The belief module types are configuration the runtime takes, like every behavior a person might want otherwise.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect, and the layer selects the model through one declaration. Every flow is started with full permissions; a permission prompt reaching the living is a launch failure. A main flow is started with its subflow tool. There is at all times a core Primary of each aspect: a flow archived has a successor.

A flow is specified whole, in Datom, by a language declared in Ethos: its system prompt, its belief modules and its variations. Long term, subflows are started by the Flow Nexus with a system prompt of their own, in place of the harness's subagent tool.

## Requests

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. A request is a datom and lands in the recipient's prompt as one, the datom being the whole message; every field of it is its own typed position, and the living's words are told from a machine's by that form. What lands in a flow is a type of two positions, the sender's triple and the message. A message is sent to an address and arrives from one: the sender's triple is the whole provenance a flow sees.

A priority is a head on the request: HardAbrupt interrupts the recipient's turn, MiddleAbrupt reaches it at its next tool boundary, Soft waits for its turn to end. A pressing request wakes its recipient; one that only queues carries what may wait. The flow that finishes messages the flow that needs to know, in plain words the reader acts on.

Inducing an interrupt, placing prompt text, submitting it, and the recipient consuming it are four separate observations, each witnessed on its own. The flow id and the delivery id are the Nexus's own: it routes and correlates by them, and a debugging query on the meta socket exposes them.

## Waking and the queue

A metaflow asleep is woken by an order, a question or the living's words; a result or a notice waits in its queue until a waking. When it wakes, the queue flushes as one message, oldest first, the waking request included, so the flow acts on complete information. A metaflow under refresh queues what arrives until its successor has started, while the Flow Nexus keeps serving every other request. What touches a topic queues for it, the vision touching it among it, and rides in with the request that wakes it.

A task request may carry the minutes it is expected to take; the Flow Nexus reminds the sender when they pass, and the done reply names the task and cancels the reminder. A flow asks the Flow Nexus to wake it at a time. A receiver going idle with a task open fires a notification to whoever waits on it, so every task is seen through.

## Refresh

A flow is refreshed when its context passes its model's threshold, configured per model in the Flow Nexus; a flow still working finishes its work first. A refresh happens from outside the flow as well as at its own call. Its successor receives its beliefs and the raw vision and notion records its remembering names, and takes up its aspect's default work: a Psyche flow reviews its presentation or makes one, a Mind flow its implementation and tests, a Field flow the system. The predecessor's biases end with it. A flow refreshes before compaction; a compaction is a refresh that was missed, and when a successor cannot start the Flow Nexus restarts the predecessor and compacts it, so every metaflow keeps a flow. A refresh runs under the metaflow's lock, the predecessor reaped in the same event, its thread put out on the app-server, its transcript archived.

A flow that keeps working without being given more work may compact; its compaction raises a warning, and the flow investigates why it worked so long.

## Hooks

Every harness event reaches the Flow Nexus through the harness's hooks calling the Flow CLI, so it knows each flow's state as it changes: a turn's beginning and end, idleness, a context threshold passed, a marked block landing in a transcript. A hook may carry content, the last message among it, ephemeral, acted on or dropped. Which hooks are installed is configuration. A poller that must exist is registered and reported.

## The Capsule

The Capsule is the component that makes where a flow runs; Herdr is its first backend, the terminal workspace every flow runs in, one pane per flow, used as it is and driven by the Flow Nexus alone. A Nexus holds several capsules: a simple query uses the default and a variant names one. Its first embodiment is the semi-sandbox: credential files copied, everything else recreated with its own sockets and store, running light models; later it encrypts the sensitive parts of the filesystem under a volatile key.

## Versions

Stable and next are declared in Nix, each with the nexuses it pairs with, so that the stable is the fallback while the next is tried; a next may be run raw before it is deployed. A build is tested in a testing capsule of its own, its own Herdr and store, where cheap, low-effort Codex and Claude flows message one another and start flows; a testing binary opens the testing store. A flow's binding to its Flow Nexus is data the Flow Nexus holds, read from a file or a socket, so that a flow moves between versions. A configuration decides which app-server a new flow or a refresh starts on, and running flows on the old server keep running. The Flow Nexus ships one or two versions a day, one fix per version; a change of memory format moves the minor version.

## The heartbeat and the tracker

The heartbeat is hourly, its rate following the energy left, and it feeds the flow it reaches what that flow would otherwise fetch: comments, usage, time left. It reminds every flow it reaches to judge its own sanity by these signs: an echo chamber, jargon and nonsense increasing, an acknowledgement answering an acknowledgement; the counts it carries are evidence, and the judgment is the flow's. A heartbeat reaches a flow for which something changed that bears on it, and reaches the Primary when the Secondary judges it must.

The tracker is a Field Quaternary on the cheapest model: it keeps the task list, each bead assigned to a metaflow, checks that the assigned flow is active, and notifies through the Secondary, sparing the expensive flows. Each aspect may have a heartbeat of its own. The number of running flows is kept low: a topic flow no longer used is retired, and a runaway helper process is stopped in the heartbeat's round.

## Debugging

The meta socket carries an operation for every situation met: rebinding a metaflow to a new pane or a new flow id, ordering a flow's compaction, reading a metaflow's deliveries with their ids, reading a flow's events. A broken system is fixed from inside; a stalled flow is unstalled by the others.

## The Ethos

The library, shared by the three parts:

    Library
    [ :protos:[ String Integer ] ]
    ; FlowId is the Nexus's own; a user sees it
    ; only when debugging. Topic is an open enum:
    ; fixed topics and camelCase identifiers.
    [ FlowId.String
      Topic.String
      Aspect.[ Psyche Mind Field ]
      Layer.[ Primary Secondary
              Tertiary Quaternary ]
      ; the metaflow triple
      Address.{ Aspect Topic Layer }
      Sender.Address
      ; the closed set of what reaches a metaflow
      Request.[ Order.String
                Question.String
                Psyche.{ Context.String
                         Verbatim.String }
                Result.String
                Notice.String ]
      ; the priority head over the request
      Message.[ HardAbrupt.Request
                MiddleAbrupt.Request
                Soft.Request ]
      ; queued for the next wake, or woken now
      Delivery.[ Queue Wake ]
      ; what a flow receives: the triple, the message
      Landed.{ Sender Message }
      RememberingDepth.Integer
      Remembering.[ Predecessors.RememberingDepth
                    Custom.Vector<FlowId> ]
      ; the refresh threshold, per model
      Threshold.{ Model.String Tokens.Integer } ]
    []
    []

Signal, what the Flow Nexus says on its ordinary socket:

    Signal
    [ flow:[ Address Remembering Message
             Delivery Landed ] ]
    [ Launch.{ Address Remembering Brief.String }
      Refresh.Address
      Send.{ Address Delivery Message }
      Wake.{ Address Minutes.Integer } ]
    [ Launched.Address
      Refreshed.Address
      Sent.Address
      Queued.Address
      Refused.[ Unknown.Address
                Asleep.Address
                ModuleMissing.String ] ]
    []

Signal, what it says on its meta socket:

    Signal
    [ flow:[ Address FlowId Sender
             Message Threshold ] ]
    ; configuration is data; ReadDeliveries
    ; is the debugging query
    [ Configure.[ Threshold
                  Capsule.String
                  AppServer.String ]
      Compact.Address
      Rebind.{ Address Pane.String }
      ReadDeliveries.Address ]
    [ Configured
      Compacted.Address
      Rebound.Address
      DeliveriesRead.Vector<Delivery> ]
    ; here the ids are positions
    [ Delivery.{ Id.Integer FlowId
                 Sender Message } ]

Memory, what it remembers:

    Memory
    [ flow:[ Address FlowId Message ] ]
    [ Metaflow.{ Address
                 State.[ Awake.FlowId Asleep ]
                 Past.Vector<FlowId>
                 Queue.Vector<Message> } ]

The datom of a launch, a send, and what lands:

    Launch.{ { Psyche core Primary }
             Predecessors.2
             «Draft the Nexus book» }
    Send.{ { Mind flow Secondary } Wake
           Soft.Order.«Review the book.» }
    { { Psyche core Secondary }
      Soft.Order.«Review the book.» }
```

**What does not return from the old module**, each with its reason:

- "A flow the living asks for is launched, properly and surely." — says nothing a launch does not already say.
- "Message asks the Flow Nexus to send … Message is the send path …" — the Message Nexus vision is set aside; the Flow Nexus is the send path.
- "Short term, the Secondary starts first, then its Primary." · "A Nexus component … replacing the harness's subagents" · "Long term, a Primary is a simplified flow" · "A simplified flow is a kind of flow made for judgment alone" — horizon-marked; the short line is a compromise for knowledge, the long lines wait for vision:long:flow-nexus.
- "Who speaks to whom … The Flow Nexus refuses a request that leaves those routes." — you ruled the route is not enforced programmatically: "What if you don't have a secondary?"
- "The flow repository … is a runtime repository. Every belief module lives outside it" · "Herdr holds the panes" · "A superseded flow is closed" — kept in substance, under Starting, the Capsule and Refresh.
- "A flow gives a presentation … A message from another flow that only updates it is answered with a short note." — a flow's conduct, belonging to intent:main-flow and vision:proposal.
- "What a refresh carries … the basic skills" — superseded by the no-handover line: beliefs and raw records, nothing else.
- "An ephemeral flow is a continuous job flow …" — a long-term kind of flow, for vision:long:flow-nexus.
- "Restarting without waking" — folded into Refresh ("from outside").
- The mermaid of the first prompt — the Ethos and datom show it.

### Proposal 2: vision:messaging · psyche-belief › vision/messaging.md — Destroy

**Comment** Everything it held stands under Requests above, in the Flow Nexus whose send path it is. The 32 running declarations that name vision:messaging take vision:flow-nexus in the same landing.

```text
- ## A message is a datom, and it arrives as one
- The message body is a datom that lands in the recipient's prompt as a datom-formatted object. The datom is the whole message.
- ## Priority is a head on the datom
-     Priority.[HardAbrupt MiddleAbrupt Soft]
- ## Delivery is harness-specific
- A pressing message wakes its recipient; a message that only queues carries what may wait.
- A request to deliver a recipient's queue delivers every queued message, or nothing when none is queued.
- ## An interrupt witness is not a delivery witness
- Inducing an interrupt, placing prompt text, submitting it, and the recipient consuming it are four separate observations. None of them stands for another, and a submission is never a read receipt.
- ## A message carries what its reader acts on
- A message carries what its reader acts on: what the sender intends, or what it has done.
```

### Rulings

1. Proposal 1: land · amend · reject
2. Proposal 2: land · amend · reject
