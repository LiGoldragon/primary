<!-- to-the-living:start -->
Presentation.{ «Who keeps a waiting request» }

## The case

In the next Message and Flow, Message asks Flow for a time-limited lock on a metaflow and hands Flow the request. If the metaflow is awake, Flow places the request now. If the request wakes the metaflow, a new flow starts. If the flow has ended, the request goes back to its sender. One case is open: a result or a notice sent to a sleeping metaflow, which does not wake it. It must wait until a request that wakes the metaflow arrives. Where it waits is the ruling.

## Distillation

### D1. Where a waiting request waits, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, at the end of «Starting flows», before «Repository and skills». Nothing removed.

**Option (a), added:** a new section headed "A waiting request waits in Flow":

Every topic has one metaflow. A request to a sleeping metaflow that does not wake it waits in that metaflow's queue, which Flow keeps. A request that wakes it drains the queue: Flow hands the new flow the waiting requests in the order received, the waking request last.

Rests on: the waking rule and queue, flows/f5a6e9/vision/messaging.md:3 (2026-10-08), which names no holder; the unruled proposal 4 of «The queue and the waking rule», which both buildable designs follow. A queue kept on the metaflow record gives it a vector, against your notion of a fixed-size record (flows/d4ae97/notion/flow.md, 2026-10-08).

**Option (b), added:** a new section headed "A waiting request waits in Message":

Flow holds no requests. A request to a sleeping metaflow that does not wake it stays with Message. When a request wakes the metaflow, Flow tells Message that it can now send, and Message hands Flow the waiting requests in the order received, the waking request last.

Rests on: flows/f5a6e9/vision/flow.md:51 (2026-10-07), on what Flow holds and on Flow signalling Message that a request can be sent; and the same waking-rule record.

**Ruling D1.** (a) Flow keeps the queue. (b) Message keeps it. (c) Amend, by line.

## Voice

One choice. A result or a notice for a sleeping flow has to wait somewhere. On the 7th you said holding messages is not Flow's job; the designs put the queue in Flow anyway. A keeps it in Flow, B keeps it in Message. Which one?
<!-- to-the-living:end -->
