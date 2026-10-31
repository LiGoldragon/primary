# Flow Nexus

## 2026-10-30 — The logical-delivery ids go out of the production Flow Nexus; they are noise
Context: the living, in the Psyche core Primary chat b0d3ae (transcript line 1873, 21:38 UTC), after a Secondary's message cited a receipt id.

Can we get this logical delivery nonsense out of the production flow nexus at least? It's really annoying and it's just introducing a bunch of noise.

## 2026-10-30 — The queue is made irrelevant or flushed reliably; the system never accumulates messages; a queue that sits too long gets a judgment flow: relevant, rerouted, the flow woken to consume it, or too old
Context: the living, in the Psyche core Primary chat 0568e3, after the Primary brought him the count of queued requests on the stable Flow Nexus during the cutover.

How is counting the queue going to help you? That's not going to solve your problem. Your problem is not knowing whether or not there is a queue but creating a solution so that the queue, whether it's there or not, is irrelevant (or so that you can flush all the queues reliably). As an aside, as a bonus, maybe try and create a system that doesn't just accumulate messages forever. I mean that would be really bad and if that's the case then we have a misbehaving system anyway. Miscommunication: there are books, entire libraries written on the harmful consequences of miscommunication. If messages get stuck then you're going to have a lot of problems. In any case, regardless of whether or not queues... I think we should be able to read the queues but regardless the system should not be one that consistently accumulates queues, like our queues waiting for a message to come in. If so maybe that flow is never going to be messaged again, in which case maybe someone should take the queue instead.

There could be a backup system where, if a queue sits for too long, we spin up a flow to take a look at it, not necessarily flush it, but to render a judgment: Is this even relevant? Do we want to reroute that information somewhere else? Do we want to actually wake the flow, flush the queue, and let the flow deal with those messages? Or has the issue now become too old that it's irrelevant?

Judgment, right? Judgment is how we resolve problems that don't have a deterministic solution.

## 2026-10-30 — A queue is flushed into its flow right before the flow's cache goes cold
Context: the living, in the Psyche core Primary chat 0568e3, right after his words on queue judgment.

And it would be good to have flush cues if they're present right before a cache is about to go cold. Does that make sense?

## 2026-10-30 — The flush stands on knowing when a flow goes idle: hooks set up reliably every time, state marks reaching the Nexus constantly
Context: the living, in the Psyche core Primary chat 0568e3, right after his words on flushing a queue before the cache goes cold.

Which means keeping tabs on when a flow goes idle, which means setting up hooks reliably and every time and getting information in the flow constantly that marks flows as active or idle.

## 2026-10-30 — A separate repository for the Flow hooks, simple, not in Rust, so a hook is tweaked without recompiling everything
Context: the living, in the Psyche core Primary chat 0568e3, after his words on hooks marking flows idle and active.

We should probably create a separate repo for the Flow hooks and make them simple. They don't have to be written in Rust because we don't want to have to recompile everything every time we need to tweak a hook. What do you think?
