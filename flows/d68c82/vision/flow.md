
## A Flow prototype now, shaped by review

> I just want a prototype that works right now according to how I've specified it so far. I want us to be able to start testing this ... And then I want to review the vision for it with all of the code. [Mind] will simply implement it as close to the vision that we currently have as he can and then adapt it for every comment or rectification that I make along the way.

-- psyche, STT, 2026-10-13. Transcription corrected: "Mine" → "Mind".

## Flow starting configured in EDN, per aspect and per metaflow

> Before we can move that context, the Flow starting code, the short-term system for starting flows has to be modified to be able to use the context modules from the right location. Let's use EDN files that can configure the whole flow starting and just keep modifying these EDN files per metaflow. We'll keep one configuration per metaflow. Maybe we can even keep one configuration per aspect, which is always included with the aspect. There's a per-aspect configuration which all the aspects share and then what differs is put into a per-metaflow EDN configuration (which this short-term tool uses to find all of its context modules and where they fit, whether it's a system prompt or user prompt).

-- psyche, STT, 2026-10-13T17:47.

## Clean specialized flows for quality

> Flow Nexus, the short-term and long-term flow tool, really needs to be worked on harder and more diligently so that:
> - it's cheap to start specialized flows
> - we can get higher-quality output
>
> It feels like right now, for example, removing the artifact tool from most flows makes sense, since most of them won't be involved in dealing with artifacts (since we'll have a flow for that). I feel like we're getting low-quality output from flows that have too much noise in their context. ...
>
> The most important improvement we need to focus on right now is getting a proper flow tool that can actually start well-trained flows for specific purposes and then easily take them down or spin them down. This does not end the topic but means that reactivating the topic would reactivate a new flow with a clean on-point context, which would yield much higher quality output.

Context: comment on «Three lines from the chat, second edition», Proposal 4.
-- psyche, STT, 2026-10-13T17:52.

## The refresh procedure starts at a threshold

> Well, Fable should never, rarely, if ever, be allowed to get to 400,000 tokens, so there was a failure there. We need a hook that sends a warning to Field to either recompact or restart a flow when it reaches a certain threshold.
>
> For Claude, you would get a preemptive warning at 200,000 tokens, at which point we're basically not forcefully trying to refresh but are actively taking measures to, first of all, warn the flow that we've started a refresh procedure. It should create its handover and potentially even say that some of its context should be split and sent to current topics or to new topic flows if it's trying to touch too many topics.
>
> Let's zero in on what all this is specifically when we describe it for actual guidance and crystallization books.

Context: Fable reached 408k tokens while writing a book; ~91% of it was noise for that book.
-- psyche, STT, 2026-10-13.

## Lean flows, cheap to start

> We need to nail down and deploy a system that can start a very lean flow. Especially for the costly models like Fable and Astra, especially Fable, I don't want to feel constrained by the cost of starting a flow to start a new Fable topic.
>
> For all of this artifact tooling and all of this useless stuff, obviously I want to be able to use subagents if it does interact with anything in terms of reading files and calling tools (because in many cases the first tool call might not work or might not be getting the information). That information might involve calling more than one tool and I'd like to measure statistically, for what's been going on so far:
> - What's the ratio of cases in which a properly configured predefined subagent that requires minimal guidance would be less token-expensive, especially in terms of output but also input, in terms of how big the response is, which we can train the agent to do properly?
> - How many of the cases would it be more expensive for the main flow to use the subagent rather than just use the tool directly itself, given how many different tries and different tools and how much filtering had to be done on the output?
>
> I'd like to do some research on that. I really want to focus on talking about flow, flow design, flow deployment: an efficient flow tool for deploying efficient, specialized, concentrated, high-signal flows that focus more on design than tool calling.

-- psyche, STT, 2026-10-13.

## A compaction request refuses a small or young flow

> I want you to make sure that we have a system in place on the short-term flow solution that lets us easily ask for a certain flow to be compacted or certain meta flows. It would refuse if the context is below a certain threshold. That way we could guard against the compacting request being routed to a brand-new flow, which we didn't know was being started, or if the flow is not a certain age, even in time terms.

-- psyche, STT.

## Compacted flows keep noise

Context: said after compacting this seat; he wants an analysis of compaction against a targeted refresh and handover.

> I don't like compacted flows because they still have a lot of noise. ... I still use compaction right now because we just really can't afford to run these huge massive context windows, which just end up being full of noise and resulting in very poor output.

-- psyche, STT.

## Compaction is an absolute emergency measure

> No compaction. Compaction is an absolute emergency measure so we're not talking about compaction in any terms other than absolute emergency. It's only going to happen until the tools start behaving properly, in which case starting a new flow is easy and reliable, which hasn't been the case so far.

-- psyche, STT.

## The flow tool queues messages for a flow in transition

> maybe we should make that flow tool also do the messaging since it can mark a flow as being in transition. Therefore it can start queuing messages instead of delivering them when the flow has reached its context limit and therefore should not receive more messages. That would just send it into a spin: potentially it could never actually refresh because it keeps getting new messages.

-- psyche, STT.

## The short term and the long term are not mixed

> You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here.

-- psyche, STT. Transcription corrected: "closure" → "Clojure".

## Short-term prototypes are written in Clojure

> I said before that I want the short-term prototypes to be written in Clojure and I see .mjs and I don't recognize Clojure. ... If any prototype doesn't use Clojure it's going to have to be rewritten in Clojure

-- psyche, STT.

## 2026-10-14 — a flow and synthetic intelligence (landed with the misnomer clause removed)

> Take out the part about artificial intelligence being a misnomer. That's not necessary.
> Otherwise it's good. Land it.

-- psyche, STT, book comment on «Flow philosophy and artifacts» P1.

## 2026-10-14 — a refreshed flow starts by crystallizing its topic

> The first thing that a flow should do when it refreshes is make a proposal for crystallization on whatever topic it's been given. It loads certain context modules, skills, and then it's given some raw psyche with context so it tries to recrystallize anything. That's its first and last response. There's no point in making an LLM start without giving it something to do.
>
> You have a default prompt, basically a default startup context, and like I said I don't want any values, such as prompts, hard-coded into code.

-- psyche, STT.

## 2026-10-14 — Flow, Nexus and Ethos together; Flow is the bootstrap

> We're developing the Flow, the Nexus architecture, and Ethos at the same time. There are three aspects, right?
> - the language aspect
> - the runtime architecture
> - that component itself, [Flow], which is probably the most important component to bootstrap
>
> Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone, of this system.

-- psyche, STT. Transcription corrected: "low" → "Flow".

## 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry

> at 128,000 tokens with Claude we get a warning. ... For Codex models the context window is much smaller and I think that at 96,000 tokens there's a warning and we start to contemplate refreshing. If the flow is working obviously we let it work and if it keeps working we let it work even past compaction.
>
> If it works so much that it compacts, eventually in the long-term vision we would have some kind of a check to make a judgment as to whether maybe the topic was misguided.
>
> For sure at 150,000, 160,000 tokens on OpenAI's models, we're seriously looking at refreshing, and the same for Claude at 200,000.
>
> It would be cool if we could strip down some of these Clojure flows so that they're way more efficient to spawn.

> in the long-term vision, if a flow has just been sitting idle for some time, we can turn off its harness. When the system is properly configured, if a request needs to reach a certain flow (which is not up and running in a harness), then the flow would just restart that flow or start a fresh one.
>
> Claude could just tell us the cache is going to expire instead of compacting. Then we would ask for the model to do a handover to produce a handover and that way we could train how we want our handover to be, which is essentially our own form of compaction.

-- psyche, STT, book comments on «Situation, 14 October».

## 2026-10-14 — A full Flow Nexus proposal, short-term and long-term

Context: spoken to the Psyche Core Tertiary after commenting on «Flow: CLI, deployment, long term», 2nd edition; relayed.

> I need to see a full Flow Nexus proposal, also probably separately.
>
> Let's have the short-term version and then the long-term/universal version: the parts that are independent of whether or not it's short-term or long-term, like the overall intention of the design, which is going to live in the long-term/Nexus proposal. We focus on specifying the ethos and from the ethos we already talked about the fact that we're going to derive the short-term prototype code.

-- psyche, STT.

## 2026-10-14 — A metaflow's default task

Context: comment on the proposed vision-flow L24 line, a needed metaflow started with its context modules and prompt.

> Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. Just mentioning it: by default maybe you set it somewhere else later on but the default task is to create a proposal or a question.

-- psyche, STT.

## 2026-10-14 — No Primary without a Secondary; queuing

Context: comment on "A layer a request needs is started whether or not it is running."

> I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.

-- psyche, STT.

## 2026-10-14 — A still-young working transcript

Context: comment on choice 4, "with a working transcript, its flow is reawakened from it".

> I would say, with a still-young working transcript, let's have a proposal to explain what a young context is in terms of ratio and where average context size starts to degrade rapidly (around the 100,000-token point).

-- psyche, STT.

## 2026-10-14 — Flow routes hooks

> We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.

## Subflows by role and by level

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the specialties table.

> These would all just be redone by role and by level. Secondary is the highest subagent, of course, and then tertiary and quaternary.
>
> Let's have some basic roles instead of writer and reader. ... Let's split this up into these context modules. In these context repos, like psyche context, mind context, and field context, we don't write skills. There's no skills directory. Let's refashion that so it's by type. ...
>
> This is all basically in ethos code, with implied equivalent [Clojure], which we need to draft on also: what the equivalents look like, with some examples and actual code in a knowledge review.

-- psyche, STT. Transcription corrected: "closure" → "Clojure".

## A subflow's kind depends on its use

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 1, the heading "A subflow is the same kind of flow as its main flow".

> No, the same. The subflow is not the same kind of flow as the main flow. The subflow's kind depends on its use so we need to define roles or tasks, or domains, so we can even compose them.
>
> Probably we should have three things, one of which could be the aspect:
> - Is it a psyche? Does it deal with thinking? Is it mind? Does it deal with documentation, tools, and changing codebases for merge requests or for audit reviews?
> - Field, which deals with debugging, system audits, system search, and things, so that each of these has its default suggested route and basic context modules that are appropriate for this kind of task. How do we want field flows to query the system? Let's build our own tools there, maybe around the field.
> - The field CLJ/CLI prototype that is based on an emulated Nexus architecture of EDN payloads, so that essentially everything can be written as one or the other configuration of an Ethos-based specification language in EDN off the bat (with basic Clojure architecture and stack), which is really easy to code on, deploy, and for machines to think in terms of an analog to [protobuf]-like language.

-- psyche, STT. Transcription corrected: "protos-like" → "protobuf-like"; "No, the same" kept [sic].

## No harness kept running for an idle session

Relayed by Psyche Flow Secondary, 2026-10-15; the living spoke to it directly.

> It's really important that we finish and deploy the new Flow Nexus, especially so that when a session is not running, we don't have to keep a harness going. If we have a lot of topics, we're going to have too many harnesses running in the background, and that will just bog down the computer with excessive RAM usage.

-- psyche, STT.

## 2026-10-16 11:25 Roles defined as datom data in their own repository

"These roles are going to get defined in role definition files with datom syntax on an ethos-specific specified object. As if we were creating payloads for the Flow Nexus, we're creating all of this data. It goes in a different directory than the cluster data but it's a different repo. It's how we configure our meta flows and this shared Metaflow infrastructure is a more general public one."
-- psyche, typed.

## 2026-10-16 11:29 A role may call a subagent model one rung up

"Let's create a special situation where this quaternary, this haiku model, can actually call sonnet so we can override the allowed subagent models per role. Let's make that part of the specification. This will be the first exception we create that is allowed to call a non-standard one rung up higher than itself. It'll just call the sonnet subagent with an illustrator and the illustrator is an actual subagent file."
-- psyche, STT.

## 2026-10-16 11:32 Refreshing the illustrator: fresh over compacted; feedback goes to modules

"He could be either recompacted or restarted regularly because compacting it at some point is necessary unless we auto-compact when it's idle in order to use the cache. I don't know. Maybe we can do a little study on that and what might be the best. If you start fresh then it's just how to illustrate, which is good. If you compact then there are all these illustration jobs that don't really matter. They don't really make it smarter if it has done more illustrations unless there's feedback, in which case it should change the context modules and the new flow would be better trained. This is where we want to finally [iron] out how to easily refresh and reliably refresh flows. This could be a really good Metaflow to practice with."
-- psyche, STT. Transcription corrected: "yarn" → "iron".

## Every representation of a flow is named by its datom struct

Context: spoken to the Psyche Core Tertiary on 2026-10-16, after commenting on «Drawing ideas»; relayed to d68c82.

> "I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID)."

-- psyche, typed.

## The flow starter puts every context module in the prompt

Context: after «Where today stands» showed a seat started without its whole context, 2026-10-16.

> "Well then we need to fix the flow starter so that it injects all of the context modules in the prompt, that it's simple to use, that it's reliable, and that it just fucking throws it into the prompt. We can't use the skill/commands in Claude. They suck.
>
> We need to just get this text injected in. If it isn't built into one message, you just fire them in a queue, fit it all in, and then tell the prompt that these are skills (so that the agent doesn't try to reload them) and which skills they are, with instructions like, "Don't reload these skills. You're getting them here." Let's just fucking fix it."

-- psyche, STT.

## Spirit is loaded in the system prompt

Context: after d68c82 set aside a book rule for speed although spirit was in its context as a user skill, 2026-10-16.

> "So I guess we need those spirit instructions to become stronger. Let's get a stronger warning against. Are these loaded in system prompts? I want system prompt loading. [ASAP]"

-- psyche, STT. Transcription corrected: "A fucking sap" → "ASAP".

## Every flow starts with all its context modules

Context: ordering fresh Opus Ethos and Nexus flows, after seats started with 6 of 22 modules, 2026-10-16.

> "We can have a flow on each with an appropriately furnished system prompt and all the fucking context modules not just 6 out of 22 like a fucking imbecile, only putting one wheel on the car. We need all the wheels on the car. We need all the context modules on the flow that need it. No wonder we aren't getting anywhere if you have such a fucking catastrophic failure that you can't even load the context modules properly."

-- psyche, STT.

## Comments on «Flow: context modules and the prompt, 2nd edition», 2026-10-16

Context: spoken to the Psyche Core Tertiary after commenting.

> "I commented on Flow context modules and I see that you still haven't fixed your thread title but you should probably just restart a fresh flow if the flow infrastructure has been improved, especially with new system prompts."

-- psyche, typed.

Context: Proposal 5, on "the flow it is given to does not see it as a module".

> "I can't agree with it. "Doesn't see it as a module" because you haven't explained to me what you mean by seeing it as a module or what the mechanism would be for that. That sounds like a long-term thing, seeing modules, but maybe you mean to say that in the short term or from the point of view of the harness, it wouldn't see it as a skill.
>
> If you're talking about the skill infrastructure, you have to use the proper terminology. The context is not a skill so you can say it doesn't see it as a module, thinking it means that it's not loaded as a harness skill. This would obviously depend on longer-term infrastructure possibly or probably for now because it is not short term anyway.
>
> In the short term I think all the skills are visible the same way for every flow and I'm guessing that's what you meant."

-- psyche, typed.

Context: Proposal 5, on "A role module is found by its metaflow".

> "That doesn't work because a role could be used for a flow that's not a metaflow so we can't. I'm not even sure I understand what you mean anyway by "a role is found by its metaflow." That doesn't make sense."

-- psyche, typed.

Context: Proposal 5, on a subagent section of role modules.

> "Subagent definitions are more complex. They're code-based and composed of [roles] and other modules so all of the payload for a subagent is not in the subagent definitions. The subagent definition is a data object that defines which modules go where. Let's get that specified in Ethos."

-- psyche, typed. Transcription corrected: "rolls" → "roles".

Context: Proposal 6, on "A hook controls what is injected into a flow's prompt".

> "That doesn't make any sense. How does a hook control what goes into the prompt? That sounds like nonsense."

-- psyche, typed.

Context: Proposal 7, on the module registry's blake3 hash and hash checking.

> "Let's make the hash `long_term` explicitly `long_term` so that the `short_term` tool doesn't need to do that."
>
> "Again let's make the hash checking a long-term goal and ignore it in the short term."
>
> "Until we have a way to efficiently update the hashes as we make edits"

-- psyche, typed.

Context: Proposal 7, on "possibly in more than one place".

> "This last part here is confusing. I'm not sure what you mean by the last part of the sentence."

-- psyche, typed.

Context: Proposal 8, placed in the Nexus vision.

> "This is vision for Flow and now you're showing me vision for Nexus so you're confused as to what the Nexus is. The Nexus is an architecture concept, right, not a specific Nexus. Everything we make is a Nexus."

-- psyche, typed.

Context: Proposal 9, on intent modules specializing a metaflow.

> "The first section was good here but this second section makes no sense to me at all."

-- psyche, typed.

Context: Proposal 10, Flow as a best example of Ethos.

> "Well this is good only if it's true. Maybe Chronos is our first good example. I don't know."

-- psyche, typed.

Context: Proposal 11, Flow's vision split by code module.

> "This could be just a general description of how Nexus Vision is usually [split] so it doesn't need to be Flow-specific."

-- psyche, typed. Transcription corrected: "capped" → "split".

## Lean flows: everything removable is a named module

Context: comment on «Refreshing the Illustrator», the cost table, 2026-10-16T19:06.

> "I'm guessing your test is flawed because you tested 3-in-1 conversations, 3 illustrations, without the cache running out. Also your fresh flows didn't have lean startup because you don't need most of the tools.
>
> If we lean out everything we don't need, let's get a super lean test. Let's develop, for everything we want to test, an actual well-built feature that exposes an EDN configuration for leaning out the flow by taking stuff out. We expose everything, every kind of thing that we want to take out, as a named module that we can then name in the blacklist configuration part of the call. Those can be preconfigured. Each Metaflow row has a configuration that we can adjust for each of these tweaks to be set by default and they can be overridden explicitly when calling."

-- psyche, typed.

## A main flow is a manager, not a doer

Context: to the Psyche core Tertiary, on how it relayed the Ethos syntax comments by retyping them, 2026-10-16.

> "Why don't you just get the subflow to send the message?"
>
> "Isn't it better for the subflow to send the message if the subflow has it, than for you to repeat the same thing, copy the context twice, and then repeat the same words I gave you in your own context? When you're a main flow, your context should kind of be saved to try and manage things instead of doing a lot of things. You're a manager not a doer."
>
> "Pass all of this stuff up to Opus to rule on and maybe with Fable make a book."

-- psyche (input mode not shown).

## Flow lands in production; a heartbeat returns to the important topics

Context: spoken to the Psyche core Tertiary, 2026-10-16.

> "I want a fresh Astra Flow to tackle Flow again, with the latest proposal and the latest vision from Fable making a book for the design. I want Flow to land, be merged in main, and be deployed. I want the Flow Nexus used in production. I want nothing more than that.
>
> I almost want to put a 4-hour timer that tackles the topic if it isn't being tackled. Maybe every 6 hours, 4 times a day, we make sure that this topic or some topic is being addressed. We need some kind of heartbeat to get back to the important topics, mostly codex-driven, with Opus and Fable guiding.
>
> This is what I want to see books on. I want to see reports every time Astra does a major effort, which get published, and every time I talk about Ethos, Nexus, or Flow. I want all the proposals refreshed with what I've added. I want to keep respecifying, reironing, and retesting Flow until it works: until it accepts system prompts, user prompts, and programmatic specialized flow based on special flow definitions, all done in a special dialect of datom ethos specified."

-- psyche (input mode not shown).

## Tighten the ship

Context: spoken to the Psyche core Tertiary after commenting on «Refreshing the Illustrator», 2026-10-16.

> "I commented on refreshing the illustrator and getting kicked on. Everybody, wake up: secondary mind, secondary field, and tighten the ship.
>
> The rules:
> - Tighten the ship.
> - Eliminate dead weight.
> - Reorganize.
> - Find out and merge.
>
> I want to delete old transcripts also and trim. Let's find some way to gain some disk space, eliminate stateful changes that we made on the operating system, and replace them with declarative stuff. I'll keep looking at the artifacts now, the books."

-- psyche (input mode not shown).

## A Flow with an always-on core

Context: the living, on Flow work after the Today 2nd landings.

> Okay I've got Flow topic working on this but I want to migrate to a Flow that's modified to have an always-on core.

-- psyche, STT.

## The last response as a datom object; handovers generated from objects

Context: comment on «Flow: vision and production», proposal 3 (refresh thresholds and handover), 2026-10-17 18:51, relayed by the core Tertiary.

> I think that if we just make the last response standard by making it a datom object (which starts with its variant and therefore has different structure, different redundant structure, and recursive structure), it can vary. Different objects have different presentations and all of this could fit in the UI instead of needing a thinking machine to render a web page for it. That would be a long-term vision.
>
> I'm just saying we don't need to talk about handovers because whatever. We can look for certain kinds of objects, like the last or all of a certain kind of object, and these can either become the handover or generate it. The handover could be generated from that, depending on what kind of objects were found or looked for, which aspect this represented, and whether or not this flow had, for example, any direct living input. We would need to determine that through, I don't know, some judgment for now.
>
> We can see, as an aside here, how much easier it gets once we control the user interface and therefore know where the living is typing. The reason why we need living core sessions is because I'm currently still remotely accessing through the harnesses themselves.

-- psyche, input mode not shown.

## The Illustrator does all waiting jobs in one flow

Context: comment on «Refreshing the Illustrator», 2nd edition, proposal 1 ("The Illustrator starts fresh and lean for every job and is never compacted."), 2026-10-17 02:10, relayed by the core Tertiary.

> Actually I think the tests show that if there's more than one job right now, he can do them all in one session and one flow. He can do however many jobs there are to do in one flow.

-- psyche, input mode not shown.

## The ephemeral flow: a continuous job flow with a context ceiling

Context: comment on «Refreshing the Illustrator», 3rd edition, proposal 1 ("The Illustrator does all the jobs there are in one flow."), 2026-10-17 19:03, relayed by the core Tertiary.

> We should give that type of flow a special name, like an ephemeral flow, meaning when it doesn't wake back up. It can do as many illustrations as we want, really, up to a realistic level, obviously, like one session could do and maybe even up to a certain level of context.
>
> After 200,000 or 300,000 tokens, it's maybe not efficient to keep illustrating if it's the same instruction basically that we're given at the beginning of the context. Otherwise yes, it's an ephemeral context.
>
> These have sort of a default size up to which we want them to run a given number of jobs. If the illustration jobs keep coming in and it's still working, it can take them on. Like I said, if the context starts to climb up too high, then we can stop giving that one new illustrations and use another illustration.
>
> Even that ephemeral flow type has a full definition in those terms. It's a continuous job flow that can take jobs as long as it's running, right, meaning it's cached. It can reach up to a certain amount of realistic context, right? With Claude it would be 300,000 tokens maximum but at 250,000 we should really wind it down.
>
> Some kind of smaller figure for Codex, I guess, by default anyway, but some flows could even be allowed to compact. Although we can probably develop a flow refreshing technique that is more efficient than compacting because it's more targeted, more intentful, and more structured than the compaction, I think.

-- psyche, input mode not shown.

## Lean flows: a system prompt, whole tools, a presentation as the only answer

> We can do fresh [lean] Claude flows now with system prompts and no stripped-down tool calls. We should be able to. ... we can have lean Fable flows especially but lean all kinds of lean flows.
>
> Let's do all of the tests on Codex and Claude with super lean-down flows that are only used to respond with a presentation when given all of the ... and/or they can ask questions, which is their way of quoting or searching the file system, except that now they talk to another model. Essentially that will answer their questions. The secondary ...

-- psyche, STT. Transcription corrected: "Lean" → "[lean]".

## The flow that finishes tells the flow that needs to know

Context: said about the book subflows sleeping on timers while waiting for other work.

> Well you don't have to wait. When the other flow is done then he should message the flow that needs to know. It's about communication not silly waiting times.

-- psyche, typed.

## A lean flow: a judgment-only call whose response is its message

> I really want to design that lean flow call with Flow so we can have these super specialized Fable calls for designing and Astra as well. We just have all of the variables and all of the context from Fable that we can assemble for this one design presentation that we're asking Fable for.
>
> It basically wouldn't need any tools because if it wants to know anything more it just asks. It wouldn't even have the messenger tool because essentially its response would be its message. It would be a special type of Flow. A lean flow, I think, is what it's called, where essentially its response is the response back. It can go back and forth like this a few times with a supervising flow that does have tool calls that can find things out for it.
>
> We would save Fable the trouble of actually calling subagents and using the messaging tool and all that because it's actually redundant for it to concern itself with the things that we can automate. It'd be a lot cleaner if we can use Fable entirely for judgment, for designing. All it does is it responds with questions and designs and maybe a third thing that I can't think of now.

-- psyche, typed.

## A flow is specified whole, in Datom

Context: continuing on the lean flow.

> Anyway this entails completely controlling the system prompt and specifying the entire agent: how it works, what its context modules are by default, and what its variations are.
>
> Basically we're creating kind of a Nix language for agents in Datom. Let's get this down. Let's get all of that specification really down with examples. Maybe this deserves its own book: how we define flows, like everything about it, in an efficient manner.

-- psyche, typed.

## A flow's model need not be an LLM

Context: comment on the current line "A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that."

> It could be a system one also. It doesn't have to be an LLM so that's not necessarily true. Also it could be an audio or a video model or whatever.

-- psyche, book comment, 2026-10-19T17:28, input mode not shown.

## No Nix-language analogy for the flow specification

> Don't use the Nix language analogy. I don't think that you really got me. It doesn't sound right the way you say it so just drop it unless you can say it properly. I don't think it's necessary to make that analogy. It's like the domain-specific language.

-- psyche, book comment, 2026-10-19T17:46, input mode not shown.

## A simplified flow

Context: comment on the lean flow paragraph.

> I think we could call it, instead of a lean flow, a simplified flow.

-- psyche, book comment, 2026-10-19T17:47, input mode not shown.

## Flow ethos, not flow definition

Context: comment on "The shape of a definition, with an example, is in vision-flow-definition."

> Why are you calling it "flow definition" and not "flow ethos"? The language is ethos. We already said the ethos goes in ethos-named modules so why are you departing from our guidelines?

-- psyche, book comment, 2026-10-19T17:47, input mode not shown.

## The simplified flow has no regular tool

Context: comment on «Flow's vision», 2nd ed., proposal 4.

> Good. You could even say that it doesn't have any regular tool. Which makes it even leaner.

-- psyche, book comment, 2026-10-19T18:15, input mode not shown.

## Specialized Opus topic flows, consulting a fresh Fable for design

> Make sure you use specialized Opus flows for specialized topics, right? Maybe refresh your flow because you're quite old, and keep track of these specialized Opus topics. Once in a while they can even consult with a fresh clean Fable that they only use for designing.
>
> Once they have everything together that Fable would need to create a design, they can send it all to Fable.

-- psyche, typed.

## A specialized flow with a large context is restarted fresh on its topic

> So specialized flows that have large context are too old and should be restarted, right? They can stay right on topic with a fresh, clean, crystallized vision and only talk about this particular topic so they can have a better output.

-- psyche, typed.

## Flows carry intelligible names

Context: three Psyche Secondaries were just launched through production Flow 0.35.11, with workspaces labelled claude-<hex> and remote names flow-<hex>.

> There are all the new Flow flows and I have no fucking idea what they are because they have unintelligible names. I've already said, "Fix that," and now the tool is being used without the fix, against my instructions. You all deserve to be sent back to be recycled into less useless machines now. You failed. Find a failure and fix it and replace your flows with less defective flows because you've obviously proven that you're completely defective (since you've moved away from my clear explicit instructions in a flagrant and liberal manner).

-- psyche, typed.

## No long hash and no improper name, forever

Context: screenshot of the claude.ai session list showing flow-c729d9c439f2b944, flow-82e6e68618438f68, flow-9eb1cc64bbd22c79 and flow-6c20823ffb9a9522 beside correctly titled flows.

> See I have no way of knowing what these new flows are. They're just called `flow` and then a huge hash, which is also forbidden. There are two massive failures here: the long hash and the improper name. Both need to be fixed forever.

-- psyche, typed.
