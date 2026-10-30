# Flow

## There are no seats; a seat is a flow. A flow has a flow ID and a role, one of which is a voice; nothing already in the voice is repeated

Context: his comment on the book «How we call the voices», on its types block (`Voice.{ Aspect Layer }`, `Seat.{ Aspect Layer FlowId }`), 2026-10-05.

> Also we don't want to repeat. This is a repetition. The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow. We're not going to repeat. The flow is just the flow ID and maybe something else but we're not going to repeat what's already in the voice. Actually yeah, we can say that the flow has a flow ID and a role, one of which is a voice.

-- psyche, typed, book comment.

## Flow and Message are designed and implemented together, deeply married

Context: same message, 2026-10-06; "message" is read as the Message Nexus and its messenger.

> In conjunction with designing and implementing Flow is message, which is going to be deeply married with it

-- psyche, STT. The sentence ends without a period; it is read as complete.

## A flow's context size is monitored; 700,000 tokens is unacceptable

Context: same message, 2026-10-06, on Psyche Fable 8475a9.

> Then I went to talk to Fable and I said that he had 700,000 tokens of context. That's unacceptable but we don't have a way to monitor that yet.

-- psyche, STT.

## Flow spawning gets automated: a refresh, or a metaflow spawning another for a subject that needs its own metaflow; not Field forever

Context: his comment on «Flow spawning», on the word "request", 2026-10-06T14:54.

> Well eventually flow spawning is going to get automated, in terms of refreshing the flow or in terms of a meta flow spawning another one because there's a job, there's a particular interest in a particular subject or implementation that needs its own metaflow. I don't think that it's going to be just because we're starting it with field now (because that falls in fields, topics, or things of interest). That doesn't mean field is going to do it forever.

-- psyche, typed, book comment.

## The end of a metaflow
Context: comment on "End" in the metaflow record, section 1.

> This is pretty good. I'm curious what the end is. Is that a description of the end goal? I guess we could put that there if that's what you mean. I'm not sure if it should be unlimited in size. Maybe we have this concept of a limited-size string. I don't want to push this too much because, like I said, I want Flow to be deployed but we can put this into Notion maybe.
>
> Really the final solution is the SEMA language, the fully semantic machine-readable true programming language that still doesn't exist: a semantic and/or programming language, really a universal mathematical universal language.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

## A flow is not always a metaflow
Context: comment on "Flow" in the metaflow record, section 1.

> A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

## Looking up by metaflow; a metaflow's flow history
Context: comments on "FlowId" in the registry record, section 2 «The registry is Flow's Memory».

> That doesn't make any sense. How do I know which flow a metaflow is? I'm going to look up "by metaflow" and a flow isn't always a metaflow so this is missing the mark by a long shot.

> And what about the flow history of a certain metaflow? Maybe it doesn't go on forever. I could see a long-running voice. Actually I guess a voice is a variant of a metaflow. Probably eventually, not that we have to worry about this, we wouldn't want to keep the entire history. You could see a scenario in which this becomes unwieldy.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

## The refresh threshold is 20% to 40%
Context: comment on the threshold bar in the figure, section 4 «The refresh is software».

> That's a nitpick but visually that threshold doesn't really represent what I want. It's more like 20% to 40%. That looks more like 70%.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

## Spirit replaces the system prompt; intent specializes metaflows; vision goes in the user prompt
> I think it's a good system because I can see that there are three different aspects to the thinking machine: the psyche, the mind, and the field. The psyche is trying to understand what it wants and what it sees as what it wants to build, right? The vision, the intent, and the spirit are also sort of designed there. This is central to how the whole rest of the machine behaves: we're going to replace the system prompt with the spirit.
>
> Depending on which kind of metaflow we're starting the harness in, we're going to load different parts of the intent in the system prompt as well. This will give us specialized metaflows because that's going to come from the intent. I guess the vision goes in the user prompt. That's what you put there as soon as you're trying to develop something or audit it, because you're going to implement it or audit it based on the vision.

-- psyche, STT, 2026-10-07.

## A fourth type: the topic flow, ephemeral, off the pane
> We can start this new opus, which is going to be of the other type, which is like topic, basically. I think it's the fourth type and these are ephemeral. They have a different payload and we don't need it on the pane.

-- psyche, STT, 2026-10-07.

## Many threads, one registry of the current flow
> I guess they're all eventually going to have a thread. There's no problem with keeping a lot of different threads as long as you route the messages properly. You can't wake up all of the flows, all of the meta flows. The flows are current so we need a registry to know which flow is active.

-- psyche, STT, 2026-10-07.

## Documenting the current environment is mind's work; each implementation has its own flow
> This is a job for the mind, right, to document the current environment, which is knowledge: how the tools that we have now are working, so that the agents that are working with them can either improve them, which is the mind. It just is a mind job not a psyche job. I guess there's nothing against using Opus sometimes for an implementation job, which is actually maybe its own kind. This is how you keep track of your work: each implementation has its own flow or meta flow. That's brilliant. And then each of those can have a different level: primary, secondary, which corresponds with the model, and then we have the actual model.

-- psyche, STT, 2026-10-07.

## Primary designs and implements; Secondary is its secretary; messages move by level
> Astra is primary and designs and implements because he uses his own subflows with his own design directly. He doesn't need to use Sol to implement new designs. Sol is good for keeping track of everything that Primary is working on and acting as a secretary. You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. I guess this is basic intent, right, because it's not spirit. It's not about general behavior and how to act. It's still going to be a system prompt, right, but it's not universal in nature. It's just due to the environment that we work in because the messaging program is imperfect and it cannot actually enforce this.
>
> In any case it's probably going to be explained to the Flow anyway that he cannot message from tertiary to primary or from tertiary to secondary of another aspect, right? They have to either go horizontally, [one] level up, or any level down and across, right? This is why the level under essentially acts as a secretary for any other level under it so that the higher levels don't get disturbed by what happens at the bottom. This is why the bottom stuff is more chatty and requires less effort because it just needs to be parented by the upper layer. They need authority and mandates to do stuff. They need to be told by a higher when they're not sure. They have to admit that they don't know and they're not sure how to do it because they have to be told that their models are less capable of inferring properly. They're weaker inferring models, so they're good at understanding basic tasks but not as good at making decisions as the upper layer, which has more understanding and context.

-- psyche, STT, 2026-10-07. Transcription corrected: "when level up" → "one level up".

## A Clojure Flow prototype, with its own database, addressed by metaflow name, specified in Ethos
> Anyway I would really like to get all of the current or the most current psyche vision, or the most psyche-aligned version of the Clojure flow prototype, with its own database with metaflow addressing by metaflow name. We could even have channel enforcement anchored in the configuration-style data: we should spec everything in Ethos and then have a standard, maybe even eventually code, from which Ethos code creates the types, the functions, and the logic, centered around the concepts defined in Ethos in the vision, right?
>
> We're always creating psyche data, mostly vision, because this is what we're going towards, what our vision is.

-- psyche, STT, 2026-10-08.

## A flow is aspect, topic and layer; the core topic is the hub of its aspect
> Let's get this Opus Flow prototype to know how to start. There are going to be different types, the main types, which are:
> - psyche
> - mind
> - field
>
> Those three aspects, psyche, mind, and field, I think, are even applicable for topics. If you have a psyche and then it has a topic, the non-topiced flows would just be the topic of core.
>
> We can have the focused starting point, basically the kernel, the first flows that sort of hold all of their aspect together. They think in the most general ways about psyche. They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct. It's just a struct.
>
> The first field is the aspect, [psyche, mind or] field:
> - Mind would be implementing, documenting things.
> - Field would be maintaining, debugging, deploying, using an actual mutating system, running commands such as `field` or `flow` to start new things or to wind things down that we didn't have hooks for, and automating wind down. Eventually Field is doing what we're trying to automate. It's kind of acting as glue for the system to run.
> - Psyche can also audit but it's a different kind of audit. It's like, does it conform to the design of the psyche? It's a more broad redesign-the-architecture kind of audit.
> - Mind is more like trying to find optimization and removing bad tests, replacing it with actual real-world emulation, like a runtime-based test.
>
> I also want this topic. The whole topic is testing. We can have a Psyche testing secondary flow or we can have a Mind Psyche, right? Mind Psyche in the sense of the Psyche component. The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably. I'm sure there's a library that can make sure something conforms to an English expression, a word, etc., if you break it down using the PascalCase logic, etc.

-- psyche, STT, 2026-10-08. Transcription corrected: "psyche minor field" → "psyche, mind or field".
