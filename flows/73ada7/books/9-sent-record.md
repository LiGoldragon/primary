<!-- to-the-living:start -->
Presentation.{ «What Message remembers of what it sent» }

## The case

Message hands Flow a request for a metaflow once Flow has given it the lock, and Flow places it. In Message's buildable design, Message's Memory holds its configuration alone: nothing is written when a message is sent, so after delivery Message keeps no record of who sent what to whom, of which kind, or when. The design gives two grounds, that the queue is Flow's and that message ids are refused, and marks the empty send path as its own inference. The same design reports that the Message in production keeps messages, receipts and parks in its store, and that the rewrite drops them with no migration (message-design.md:562-563); that is the design's claim, not observed here. The design leaves message history open as its fork F13: it would come from "a different kind of interface" that no design has yet. Message and Flow as designed are in development, none of it in production. Two of the living's records ask more of a sent message than the design keeps: one asks that a successor know what its ancestor sent, and one says the database can know a message's kind. Neither says which store holds it.

## Distillation

### D1. What Message keeps of a sent message, in vision-messaging

Target: `psyche-skills/skills/vision-messaging.md`, a new section after «Only messages that act, deliver, or block» (line 31-33) and before «Sources» (line 35). The section before it stands as: Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports. Nothing is removed; one section is added, and its source lines are appended under «Sources».

**Option (a), Message keeps no record of a sent message.**

Added, under the heading «Message's Memory holds its configuration»: Message's Memory holds its configuration alone; a request leaves nothing in it once Flow has placed it. Message history is a separate design, reached by something other than a message id.

Sources added: 93ba9f messagingInterface; f5a6e9 flow.

Rests on: flows/93ba9f/vision/messagingInterface.md:23 (2026-09-26, raw, heard by 93ba9f; relayed copy at flows/b7ba00/vision/messaging.md:29), on not getting the message id and developing a different kind of interface to get message history; flows/f5a6e9/vision/flow.md:59 (logged 2026-10-07), on Flow holding no messages and Message talking in metaflows. Message's design proposes this (flows/73ada7/reports/build/message-design.md:275-277, fork F13 at 612-614), unruled. That the 2026-09-26 words defer history rather than place it outside Message is this flow's reading; they do not say where history is kept.

**Option (b), a history kept by Message.**

Added, under the heading «Message keeps a history of what it delivered»: Message's Memory keeps each message it delivers, with its sender, recipient and kind, and answers a query for that history, never a lookup by message id. A successor reads there what its ancestor sent. How much history is kept is bounded.

Sources added: 93ba9f messagingInterface; b81560 operational-refreshOutboxAndMessageChannels.

Rests on: flows/b81560/vision/operational-refreshOutboxAndMessageChannels.md:17-21 (artifact comment, 2026-09-19, raw), on the new flow knowing the message that was sent after the lock came in, and knowing what its ancestor sent to another flow; flows/93ba9f/vision/messagingInterface.md:23 (2026-09-26, raw), on history through an interface that is not by message id. The bound draws on flows/d4ae97/vision/flow.md:74 (comment, 2026-10-07, raw), which speaks of a metaflow's flow history, not message history, and on flows/840e42/vision/logging.md:7-9 (landed 2026-10-01; the date heard was not read), which speaks of Flow's log of notifications kept thin and garbage-collectable. Carrying either onto Message's history is this flow's inference. That the 2026-09-19 words need a store of sent messages somewhere is this flow's reading; they name the message and flow system, not Message alone.

**Option (c), a history behind a separate interface.**

Added, under the heading «Message history has its own interface»: Message history is kept behind an interface of its own, apart from sending. Message hands it each message it delivers, and it is queried by what a message is, never by message id. Message's Memory holds its configuration alone.

Sources added: 93ba9f messagingInterface.

Rests on: flows/93ba9f/vision/messagingInterface.md:23 (2026-09-26, raw), on "a different kind of interface to get message history". Whether "a different kind of interface" means an interface apart from Message, or a different kind of query on Message itself, is unknown; this option takes the first reading, which is this flow's.

**Option (d), the database knows each message's kind.**

Added, under the heading «The database knows a message's kind»: Message's Memory records the kind of each message it delivers. The recipient is not told how hard a message breaks in; a flow that wants to know finds it there.

Sources added: 93ba9f messagingInterface.

Rests on: flows/93ba9f/vision/messagingInterface.md:67 (artifact comment, 2026-09-26, raw; relayed copy at flows/b7ba00/vision/messaging.md:91), on whether to tell the model a message is soft or hard: "The database can know it", said with "I don't know. I don't think so". The same comment goes on to say the soft or hard approach was wrong and that it is just what kind of message it is. Which database those words mean is not named; reading it as Message's Memory is this flow's inference, as is the reading that the database keeping the kind still stands once soft and hard are dropped.

**Ruling D1.** (a) No record. (b) A history in Message's Memory. (c) A history behind its own interface. (d) Memory records each message's kind. (e) Amend, by line.

## Voice

One choice. Once a message is delivered, the new Message forgets it. Message's design keeps nothing and leaves history for later, from your words that history comes through a different kind of interface, not by message id. A writes that down. B has Message keep a bounded history, so a successor can read what its ancestor sent, as you asked on the Session Flashbook. C puts history behind its own interface, with Message feeding it. D keeps each message's kind in the database, since you said the database can know it. Which one? This flow's reading: your words don't say which store holds history, and D was said about soft and hard, which you then dropped.
<!-- to-the-living:end -->
