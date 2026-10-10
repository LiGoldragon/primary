<!-- to-the-living:start -->
Presentation.{ «Who works out where send up goes» }

## The case

In the next Message and Flow, a flow can send to a named metaflow or send up, Recipient Up: to the layer above it in its own aspect and topic, so a Mind ethos Secondary sending up reaches the Mind ethos Primary. Someone has to turn Up into that metaflow. Message's design does it: Message asks Flow which metaflow the sender runs in, works out the one above, and then asks Flow for that metaflow's lock; from a Primary it refuses with NoneAbove and never calls Flow. Flow's buildable design has no Up at all. Its Deliver carries the sender's metaflow, and Flow refuses with OffRoute a request whose sender and recipient leave the routes of vision-aspects, which since today vision-flow names as Flow's to enforce. So in Message's design the routes are known in two places: Message knows the step up, and Flow checks every route. Both designs are in development, none of it in production. That putting Up in Flow would keep the routes in one place, and that Flow would then need a way to receive Up rather than a metaflow, are this flow's inferences. When the topic has no Primary, both designs refuse the send as Unknown.Metaflow; whether send up should instead fall back to core is not asked here.

## Distillation

### D1. Who resolves send up, in vision-messaging

Target: `psyche-skills/skills/vision-messaging.md`, a new section after «A message is a datom, and it arrives as one», ending "There is no envelope around it.", before «Priority is a head on the datom». Nothing removed.

**Option (a), added:** a new section, «Send up goes to the layer above, in one's own aspect and topic»:

A flow that sends up reaches the flow one layer above it, in its own aspect and its own topic. Message works out that metaflow from the sender's own, then asks Flow for its lock. A Primary has no layer above, and Message refuses its send up without asking Flow.

Rests on: flows/b7ba00/vision/messaging.md:109 (2026-09-26), on send up meaning the higher layer and on Message working out where it goes and asking Flow, said with the alternative left open; flows/6aa08d/vision/fieldStack.md:7 (2026-10-07), on going up one's own aspect and never into another; flows/445410/vision/messaging.md:39 (2026-10-09), on a Secondary's report going to the Primary of its own topic. Message's design 7.4 (flows/73ada7/reports/build/message-design.md:392-407) builds this, unruled.

**Option (b), added:** a new section, «Send up goes to the layer above, in one's own aspect and topic»:

A flow that sends up reaches the flow one layer above it, in its own aspect and its own topic. Message passes Up to Flow as it is, and Flow, which holds the routes, works out that metaflow from the sender's own and locks it. A Primary has no layer above, and Flow refuses its send up.

Rests on: the same record flows/b7ba00/vision/messaging.md:109 (2026-09-26), on the alternative that Flow works it out; the approved line at psyche-skills/skills/vision-flow.md:26 (landed 2026-10-09), on Flow refusing a request that leaves the vision-aspects routes; flows/445410/vision/messaging.md:49 (2026-10-09), on messaging being strict on whom a flow may message by who it is; flows/6aa08d/vision/fieldStack.md:7 and flows/445410/vision/messaging.md:39 for where up goes, as in (a). Flow's buildable design already checks the route from the sender's metaflow (flows/f5a6e9/reports/flow-buildable-design.md:206-212, 243-247 and 425-431), unruled; that it would take Up from there is this flow's reading.

**Ruling D1.** (a) Message resolves it. (b) Flow resolves it. (c) Amend, by line.

## Voice

One choice. A flow sends up, and someone has to find the flow above it in its own aspect and topic. On the 26th you said Message works it out and asks Flow, or maybe Flow does, and left it open. Today you approved that Flow refuses anything off the vision-aspects routes. Message's design resolves Up itself. A keeps it in Message, B moves it to Flow beside the routes. Which one? This flow's reading: B keeps the routes in one place.
<!-- to-the-living:end -->
