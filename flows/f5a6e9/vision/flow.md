# Flow

## A voice is a permanent metaflow, one that may sleep and is woken by a message; the role is maybe a short camel-case string; the worker names are the old system

Context: his comment 1 of 9 on «Flow and the metaflow» (https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW), 2026-10-07 18:32, on the passage "A flow has a flow id and a role, and may continue a metaflow. A role is a voice or a worker (read-trivial, write-ordinary, tester, book). A metaflow is the voice of the flow's own role, or a named subject." Relayed verbatim by Field db38f8 at his order.

> There's a bunch of things that are false in here. I guess you could say a flow always has a role if we describe a role as maybe some kind of short camelcase expression, a string. It just describes, I don't know. I'm not even sure that a flow always has a role but maybe.
>
> A role is a voice. That's not true. A role may be a voice or a worker. Read trivial. Right. No, no, no, no, no, no. This read trivial. Right. Ordinary.
>
> This stuff is just an old system and it doesn't really correspond with the new system. Metaflow is the voice. No, Metaflow is not automatically a voice. A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken in the sense that if a message is intended for it, flow would automatically... This isn't intended for the first version but eventually it would just trigger the flow to be spawned with the right context modules depending on the message.
>
> There would probably be some kind of a judgment, a judgment machine call. When I say judgment I mean, you know what I mean. It's not just LLM. It's not just LLM, there's more than just LLMs. It's thinking machine judgment and then you go on.
>
> Anyway you can see that I don't like your proposal. It feels like you just grabbed everything you could see and just threw it all in a pot and thought that it would make a nice meal but it tastes like shit.

-- psyche, STT, book comment, relayed by db38f8.

## "Worker" is not the right term; maybe "goal"

Context: his comment 3 of 9 on «Flow and the metaflow» (https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW), 18:58, on "; a subflow's role". Relayed by db38f8.

> I don't think "worker" is the right term. Maybe "goal" or something like that.

-- psyche, STT, book comment, relayed by db38f8.

## Refer to metaflows, with the metaflow's memory holding its current flow and maybe its predecessor; options are a last resort

Context: his comment 5 of 9, 19:01, on `Voice.{ Psyche Primary }` in the three written flows, whose records carried `Option<Metaflow>` and `Predecessor.Option<FlowId>`. Relayed by db38f8; "Wispr Flow's" left [sic] by the relayer.

> I don't understand why you insist on using the structure whereby you refer to everything by flow ID instead of referring to the meta flows and then having a reference in the meta flow memory to Wispr Flow's [sic] current for it and maybe its predecessor. I don't see the point of putting that data with the flow data. It's very noisy. Your syntax, now you have all these options and I very much dislike options. I think that they're really a last resort if we can't get a better design that can work without them. What do you think? Give me some feedback on that.

-- psyche, STT, book comment, relayed by db38f8.

## Metaflow is the major abstraction, what we mostly think about; Flow is lower-level and almost never user-facing

Context: his comment 7 of 9, 19:04, on the Memory block of proposal 2. Relayed by db38f8.

> Again you're making Flow the only abstraction and you're just shimming Metaflow as a tiny afterthought inside of it, which is not my vision. Metaflow is a major abstraction and it's what we mostly think about. The Flow abstraction is a lower-level thing and it's not user-facing in almost any cases.

-- psyche, STT, book comment, relayed by db38f8.

## History centred on the metaflow, not on Flow

Context: his comment 8 of 9, 19:05, on "History is not a third record. Each flow names its predecessor, so a metaflow's history is the walk back from its current flow." Relayed by db38f8.

> Again you're centering this around Flow and not Metaflow, which is not in line with my vision.

-- psyche, STT, book comment, relayed by db38f8.

## What is sent to flows are typed requests, not letters; Flow holds no messages; Message asks Flow for a time-bound lock and talks in metaflows

Context: his comment 9 of 9, 19:09, on proposal 3, "The lock is the lineage's state ... A letter waits in Flow and is delivered to whichever flow is current when the lock opens". Relayed by db38f8.

> The abstractions that are sent in flows are not letters. We are going to have actual types. If, let's say, something asked for a certain flow to be compacted, then the logic for how this would unfold, or how that metaflow would be refreshed in terms of routing, would be very different than a message.
>
> Obviously if the flow is brand new, the last thing we want to do is compact it. We wouldn't send whatever needs to be sent into that pane for it to compact to the new flow. That's just one example. There's probably a bunch of different behaviors that would correspond to different requests that are being asked to be sent to a certain flow.
>
> I don't think that it's Flow's job to hold messages. It's more like it's Flow's job to tell the message component later on to give it the signal that a message can now be sent. The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message because now it has the lock. Flow told the message that it has the lock for that flow or that metaflow. The message doesn't have to know about the flows. It can also just talk in terms of metaflows. And indeed when this is done and more polished, I'm mostly going to talk in terms of meta flows.

-- psyche, STT, book comment, relayed by db38f8.
