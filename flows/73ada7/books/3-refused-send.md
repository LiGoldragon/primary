<!-- to-the-living:start -->
Presentation.{ «What happens to a refused send» }

## The case

In the next Message and Flow, Message asks Flow for a time-limited lock on a metaflow before it hands Flow a request. Flow refuses the lock in two cases: another lock on that metaflow is already held, or the metaflow is being refreshed, since the refresh holds the same lock while it starts the successor. Open is what becomes of the request then. Flow's buildable design answers the lock with the refusal Held or Locked and keeps nothing; it queues only a request that already has the lock and finds the awake flow busy. Message's design passes the refusal back to the sender, who sends again if it chooses; Message neither retries nor keeps the request. Both designs are in development, none of it in production. That a refresh lasts only as long as it takes to start one flow, so a sender would often meet Locked only briefly, is this flow's inference.

## Distillation

### D1. What happens to a send refused for a held lock or a refresh, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, at the end of «What it does», after the paragraph ending "Flow holds the lock on flows.", before «Starting flows». Nothing removed.

**Option (a), added:** a new paragraph:

When the lock on a metaflow is already held, or the metaflow is being refreshed, Flow refuses the lock and keeps nothing. The refusal goes back to the sender, which sends again if it chooses.

Rests on: flows/1b8ac0/vision/messaging.md:31 (2026-09-21), on Message asking Flow to send and Flow answering successful or not; the accepted decision recorded with it at flows/1b8ac0/vision/messaging.md:25 (2026-09-21), that a locked flow refuses with no downgrade; the unruled refusals Locked and Held of f5a6e9's buildable design (flows/f5a6e9/reports/flow-buildable-design.md:234-236 and 412-414).

**Option (b), added:** a new paragraph:

When the lock on a metaflow is already held, or the metaflow is being refreshed, Flow refuses the lock and keeps nothing. Message keeps the request, and Flow tells Message when the lock is free, so the request can now be sent.

Rests on: flows/f5a6e9/vision/flow.md:59 (2026-10-07), on Flow telling Message later that a message can now be sent, and Flow holding no messages; flows/e5a0bc/vision/flow.md:25 (2026-10-07), on Message using the lock to know whether a message can reach a flow. Both were said about a lock that cannot yet be had; that the first of them was said about a waiting letter and not about a refusal is this flow's reading.

**Option (c), added:** a new paragraph:

When the lock on a metaflow is already held, or the metaflow is being refreshed, Flow keeps the request in that metaflow's queue and hands it over once the lock is free, in the order received.

Rests on: the unruled queue of f5a6e9's buildable design, which already queues a request to a busy awake flow (flows/f5a6e9/reports/flow-buildable-design.md:383-387), and the unruled proposal 4 of «The queue and the waking rule» (flows/f5a6e9/books/11-the-queue-and-the-waking-rule.md, 2026-10-08). It stands against flows/f5a6e9/vision/flow.md:59 (2026-10-07), on Flow holding no messages.

**Ruling D1.** (a) Back to the sender. (b) Flow tells Message when it may send. (c) Flow queues it. (d) Amend, by line.

## Voice

One choice. Message asks for a lock, and the lock is held or a refresh is running. On the 21st you said Flow answers successful or not; on the 7th you said Flow tells Message later that a message can now be sent, and holds no messages. The designs send the refusal back to the sender. A sends it back, B has Flow tell Message when to send, C has Flow queue it. Which one? This flow's reading: if book 1 goes to B, B here matches it.
<!-- to-the-living:end -->
