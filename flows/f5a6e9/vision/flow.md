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

## Metaflow kinds and payloads: four things; psyche, mind and field have similar payloads; sessions on spirit, intent, vision

Context: said on 2026-10-07 on Flow's metaflow kinds; relayed by Psyche Opus d4ae97 with elisions marked by it.

> We're going to create this different flow type that is basically a meta flow. It is one of the four things and they have different types of payload but psyche, mind, and field have similar payloads. ... Their variant can be just one of the fields in that particular payload. ... What's the name that we put them all under, these three that are very similar, or are these going to actually diverge and take their own shape? Maybe they subdivide into their own subcategory. ... I'm actually trying to start a session to work on spirit and then I would have a session to work on intent and a session to work on vision. That's what they are so we don't need all of them at the same time.

-- psyche, STT, relayed by d4ae97.

## Many threads if routed properly; a registry knows which flow is active; an implementation is its own kind with a level that corresponds with the model

Context: same day; relayed by d4ae97 with elisions.

> There's no problem with keeping a lot of different threads as long as you route the messages properly. You can't wake up all of the flows, all of the meta flows. The flows are current so we need a registry to know which flow is active. ... I guess there's nothing against using Opus sometimes for an implementation job, which is actually maybe its own kind. This is how you keep track of your work: each implementation has its own flow or meta flow. ... And then each of those can have a different level: primary, secondary, which corresponds with the model, and then we have the actual model.

-- psyche, STT, relayed by d4ae97.

## The thread title names no model; the word-based id, three words or maybe two

Context: same day; relayed by d4ae97 with elisions.

> When we write the name of the thread in the harness, we don't actually mention the model because when I go into Claude I know that I'm talking to Claude, right? I don't need to know that it's Opus. ... I'd rather see the word-based one. I think it would be cool to have this word-based translation that actually works. Let's see if we can do that with three words, maybe even two.

-- psyche, STT, relayed by d4ae97.

## A passable vision for Flow on the current design, where the metaflow is the ancestor of the next; the launch scripts modified to match

Context: said on 2026-10-07; relayed by Psyche Opus d4ae97.

> Let's get a passable vision for Flow using the current Flow design, where MetaFlow is the ancestor of the next. Let's modify the scripts that we're using now to launch all this.

-- psyche, STT, relayed by d4ae97.

## The topic is a dense string: PascalCase of a certain number of words, with a checker

Context: said 2026-10-08 on the type of a metaflow's topic; raw record d4ae97 vision/flow.md:181, which also says the metaflow is a struct whose first field is the aspect and that flows with no topic take the topic core. Relayed by 445410.

> The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.

-- psyche, STT, relayed by 445410.

## The topic of the topicless metaflows is core: the heart of their own aspect

Context: said 2026-10-09; raw record 445410 vision/flow.md; relayed by 4ddfe1 and 445410. Transcription corrected by the relayer: "[topicless]".

> Right, so, the topic is always there and by, well, the topic for the current metaflows that we have that essentially are [topicless] is core. Meaning—core, like they're the heart of the machine, they... are the heart of their own aspect.

-- psyche, STT, relayed by 445410.

## The Flow Nexus vision skill may split along the code: vision-flow, flow-ethos, then memory-ethos, signal-ethos; signal first

Context: same message, 2026-10-09, on «The metaflow's ethos»; relayed by ebbe30.

> I might approve this. This looks good but it needs to land in vision, right? So let's have that part of things done and then all of the books can be redone also. This doesn't require heavy judgment, right? Essentially we could even break up the skill, if it gets too big, with the code into modules that are about the code, right? You would have, let's say, vision-flow, this is what we're talking about: flow-ethos. If that gets big you can even go: psyche, flow, memory-ethos, signal-ethos, just ethos for the rest. If the signal and the memory files get really big, signal is probably one of the first that you'll want to separate because of how it is. Essentially if you load that skill, this is how we would want to see it currently, according to the latest check with the living: this particular nexus talk, the Flow Nexus. We could even, I don't know, maybe call it Flow Nexus also in the skill. That way in the description it can say, "This is the Flow Nexus vision."

-- psyche, STT, relayed by ebbe30.

## The topic is uncapitalized: core, ethos; it is the core:Name type, a camelCaseExpression with runtime checks on creation

Context: typed 2026-10-09 after 445410 wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase of the 2026-10-08 record above; relayed by 445410 and 9fed42.

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

-- psyche, typed, relayed by 9fed42.
