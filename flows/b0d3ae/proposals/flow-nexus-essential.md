Presentation.{ «The Flow Nexus, bare» }

# The Flow Nexus, bare

Created by the Primary

### Proposal 1: vision:flow-nexus · psyche-belief › vision/flow-nexus.md — whole, retaken

**Why** The module is cut to what the Nexus needs to function. Your four comments are in: the metaflow is a name on the user side, the id is not lengthened, sleeping and waking move to the long vision, the one-model line is gone.

```text
---
description: The Flow Nexus, which starts, messages, refreshes and ends flows.
dependencies: [vision-nexus, vision-model-roles]
---

## Address

A flow is addressed by { Aspect topic Layer }. Inside the Nexus the unit is the flow: one harness session, one id, one address. The metaflow is the user-facing name for the flows that have run at one address, one after another; in the chat a flow is called by its address.

A flow's id is the first six characters of the hash of its harness session id, so its transcript is found from it. Every call to the Flow CLI is identified by the calling process.

## Start

A launch names an address, a remembering and a brief. The Nexus composes the flow's prompts from the belief modules declared for that address: spirit and intent in the system prompt, the other modules, the remembering and the brief in the first prompt. The layer selects the model. The Capsule gives the flow its place to run, one Herdr pane; a permission prompt reaching the living is a launch failure.

## Message

A request is sent to an address and the Nexus delivers it into the flow's prompt. When the flow is busy, the request queues and is delivered when the flow is idle, the queue whole and oldest first; when no flow is running at the address, one is started with the queue as its first prompt. The living's words, a comment among them, reach a flow by this path.

A request is one of a closed set: an order, a question, the living's words, a result, a notice. The Nexus refuses a request that leaves the routes of vision:aspects.

## State

Every harness event reaches the Nexus through the harness's hooks calling the Flow CLI, so the Nexus knows each flow's state as it changes: started, working, idle, ended.

## Refresh

A flow past its model's context threshold is refreshed as it goes idle: a successor is launched at the same address with a remembering of its predecessor, the predecessor is ended, and what queues meanwhile goes to the successor. The threshold is configured per model. A compaction is a refresh that was missed.

## End

A flow is ended by request, by refresh, or when it is abandoned or superseded; its transcript stays.

## Signal

Signal
[ flow:[ Address Remembering FlowId Request ] ]      ; imports
[ Launch.{ Address Remembering Brief.String }         ; queries
  Send.{ Address Request }
  Refresh.FlowId
  End.FlowId ]
[ Launched.FlowId                                     ; responses
  Delivered  Queued  Started.FlowId
  Refreshed.FlowId
  Ended
  Refused.[ NoCapsule RouteClosed AddressBusy ] ]
[]                                                    ; types

; the living's comment on a book, carried to the Psyche core Primary
Send.{ { Psyche core Primary }
       Words.«This is not necessary.» }
Delivered
```

**Moved, not removed** These leave the module for vision:long:flow-nexus, as they stand today, under the same headings: a metaflow sleeping and waking; the topic enum; the judgment by a small model of whether to wake a topic; the simplified flow; a Primary as a simplified flow; the flow ethos specifying a flow whole; the heartbeat; the ephemeral flow; restarting without waking; versions; the Capsule's later encryption; the real-world test; Herdr as one exchangeable backend.

**Removed** The one-model line. Id lengthening on collision. "What it does", which said the Nexus three times. "Repository and belief modules", held by vision:belief-modules. "What a refresh carries", said once under Refresh.

### Proposal 2: vision:messaging · psyche-belief › vision/messaging.md — Destroy

**Why** The Nexus is the one send path, and Message is said under it. The priority head and the four witnesses go with it; a request's datom form is the Signal above.
