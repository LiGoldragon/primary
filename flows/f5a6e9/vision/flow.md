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

## Many threads if routed properly; a registry knows which flow is active; an implementation is its own kind with a level that corresponds with the model

Context: same day; relayed by d4ae97 with elisions.

> There's no problem with keeping a lot of different threads as long as you route the messages properly. You can't wake up all of the flows, all of the meta flows. The flows are current so we need a registry to know which flow is active. ... I guess there's nothing against using Opus sometimes for an implementation job, which is actually maybe its own kind. This is how you keep track of your work: each implementation has its own flow or meta flow. ... And then each of those can have a different level: primary, secondary, which corresponds with the model, and then we have the actual model.

-- psyche, STT, relayed by d4ae97.

## A passable vision for Flow on the current design, where the metaflow is the ancestor of the next; the launch scripts modified to match

Context: said on 2026-10-07; relayed by Psyche Opus d4ae97.

> Let's get a passable vision for Flow using the current Flow design, where MetaFlow is the ancestor of the next. Let's modify the scripts that we're using now to launch all this.

-- psyche, STT, relayed by d4ae97.

## The topic is a dense string: PascalCase of a certain number of words, with a checker

Context: said 2026-10-08 on the type of a metaflow's topic; raw record d4ae97 vision/flow.md:181, which also says the metaflow is a struct whose first field is the aspect and that flows with no topic take the topic core. Relayed by 445410.

> The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.

-- psyche, STT, relayed by 445410.

## The Flow Nexus is started by datom commands; its configuration is loaded atomically from datom payload files in separate repositories, sent in succession on the meta socket

Context: his comment on «The new flows, as they run», 2026-10-09 20:41, in part; relayed by 445410 and 9fed42.

> Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant. Let's do this.

-- psyche, STT, book comment, relayed by 9fed42.
