# Messaging

## 2026-10-30 — A delivered message shows no delivery id and no flow id
Context: the living, in the Psyche core Primary chat d12d26, on a message as it lands in the chat: "[ { logical-delivery-00000000000000020084 Sender.{ Psyche core Secondary } Soft.Result.«From Psyche core Secondary a27c64. …» } ]".

> logical-delivery-00000000000000020084

have this removed from the output. noise. and remove the flowID too

## 2026-10-30 — The delivery id is useless: not shown anywhere; the sender never names its flow id
Context: the living, same chat, correcting the Primary's reading ("the Flow Nexus drops the delivery id from what lands in a prompt, and flows stop writing their flow id in the body").

No, that's not what I said. The sender does not name his ID, and the output does not show the ID. The ID is useless.

## 2026-10-30 — A message routes by the metaflow triple alone
Context: the living, same chat, right after.

The message must route correctly using the Metaflow triple without the flow ID.

## 2026-10-30 — A flow id is never used for sending; a peer is thought of only as its metaflow, since a metaflow is a continuation of flows
Context: the living, same chat, right after.

We must not use the flow ID for sending messages. That's for sure. Make sure that that's not the case. They're also useless as far as knowing where the message came from, because a meta flow is not his particular flow. It's a continuation of flow, so nobody thinks about their peers in terms of flow ID ever.

## 2026-10-30 — The flow id is a backend abstraction: the runtime routes by it, a user never sees it
Context: the living, same chat, correcting the Primary's "the flow id leaves the signal types themselves".

Well, obviously, don't now make a version that shows the Flow ID, right?

What do you mean? Yeah, it leaves the query, but the runtime is aware of flow IDs, obviously, because it needs to know where to route the message. The users never need to be aware of them. It's a backend abstraction.

## 2026-10-30 — Debugging interfaces or query types expose the flow ids and delivery ids when one must be explicit
Context: the living, same chat, after the ids were ruled out of every ordinary output.

But make sure you have debugging interfaces or query types that actually expose them in case you need to be explicit.
