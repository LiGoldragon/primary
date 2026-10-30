## A flow is one run of a metaflow

Context: comment on «Flow's vision», the current vision/flow.md line "A flow is one run of a voice".

> The run: one run of a metaflow not a voice. Let's get rid of that voice vocabulary. Consistency

-- psyche, book comment, 2026-10-19T17:27, input mode not shown.

## Subflows replacing the subagent tool is long term, stated broadly

Context: comment on «How a flow is defined», the vision/flow.md heading "Subflows replace the harness subagent facility".

> Let's clean up this subflow vision a bit. It's a bit confusing and mark it as long term. This should just be in its own book. This is long term. We want to replace the subagent tool with actual flows but it's long term and it should be just a broad explanation of the concept instead of being so specific. These paragraphs are getting maybe too much into specifics and these are confusing short-term hacks with long-term vision. Like how we have the field coordinator involved, this sounds more short-term than long-term and maybe it's not even relevant anymore. I don't know. If we're not doing it right now, we can remove it and just represent the concept more clearly or more sanely.

-- psyche, book comment, 2026-10-19T17:45, input mode not shown.

## A startup may take several prompts, one model call

Context: comment on proposal 11, "A fresh flow starts with one prompt".

> Well this is true except that if it doesn't fit in one prompt, we can put it in two. Technically speaking from the harness's point of view, it looks like two prompts but they're sent almost instantaneously, one after the other. We don't end up making two LLM calls. However many prompts it needs to fit the initial startup in, we should never forget that a lot of the stuff goes in the system prompt, which is technically different from the harness's point of view.

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.

## The Primary becomes a simplified flow

Context: comment on proposal 12, no Primary without its Secondary.

> Yes this is good, especially since we eventually want primary to be a simplified flow so that it's only used for guiding the design or posing questions, things like that. Essentially rendering a judgment

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.

## A refreshed flow's first act is a book shaped by its context and prompt

Context: comments on proposals 16 and 17, a refreshed flow's first act.

> Not quite. It's a book, basically. It's a book which can have different forms so the book that it makes will depend on the context that it was loaded with and the goal or question it was given (essentially like the prompt). The so-called prompt is the actual only piece of string which was given to this supplier, which is unique to it and not a context module.

> This is also good so I'm not clear on which proposal I want. Like I said I want the difference between the different proposals to be explained.

-- psyche, book comments, 2026-10-19T18:23, input mode not shown.

## No handover: every task ends in a presentation, and Flow moves the next messages on

Context: comments on proposals 18 and 19, the handover warning thresholds.

> Like I said before there's no handover because every time a flow is given a task, it should end with a presentation. Maybe the word "presentation" is not right, but "a book." I don't like the word "book" because the books are going to go away and be replaced by a better user interface. We can use a word that essentially just means, for now, that we're making a book: a presentation, I think, or something which essentially could fit into a book, like the specification of every main response that the model gives.
>
> If it's being interrupted by messages from other flows, obviously, depending on what the messages are, it doesn't need to make a full presentation because it's maybe just being updated about things. Whenever it's given a specific psyche-originating task or goal or question, or whenever it starts its flow for the first time, the first thing it'll do (when it stops or in its last response) will be a presentation.

> Besides the whole fact that it's not told to write a handover, in fact it doesn't need to be told anything when it's going over context. It just stops getting new messages because the Flow reserves its next messages for the next flow of it. It just needs to be trained by default to always give a presentation whenever it's given significant new context to consider, especially psyche-originating.
>
> The amount at which each model should be refreshed depends on the models. It's going to be a specification and configuration that goes into Flow and obviously we need to specify. Roughly speaking the OpenAI models have a smaller usable context. The Claude models seem to be better: they can handle a longer horizon better and context recovery is deeper and better.

-- psyche, book comments, 2026-10-19T18:25–18:26, input mode not shown.

## Compaction is allowed for continuous work, with a warning and an investigation

Context: comment on proposal 21, some flows may compact.

> Yes some flows, like all flows, can compact if they're just continually working and without being given more work. But we should get a warning and somebody should investigate if a flow is working so much that it has to compact. Then maybe it's having trouble and we can bring this up to the living or get Psyche to reconsider how to approach it and give guidance.

-- psyche, book comment, 2026-10-19T18:29, input mode not shown.

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

## A compaction request refuses a small or young flow

> I want you to make sure that we have a system in place on the short-term flow solution that lets us easily ask for a certain flow to be compacted or certain meta flows. It would refuse if the context is below a certain threshold. That way we could guard against the compacting request being routed to a brand-new flow, which we didn't know was being started, or if the flow is not a certain age, even in time terms.

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

## 2026-10-14 — a flow and synthetic intelligence (landed with the misnomer clause removed)

> Take out the part about artificial intelligence being a misnomer. That's not necessary.
> Otherwise it's good. Land it.

-- psyche, STT, book comment on «Flow philosophy and artifacts» P1.

## 2026-10-14 — Flow, Nexus and Ethos together; Flow is the bootstrap

> We're developing the Flow, the Nexus architecture, and Ethos at the same time. There are three aspects, right?
> - the language aspect
> - the runtime architecture
> - that component itself, [Flow], which is probably the most important component to bootstrap
>
> Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone, of this system.

-- psyche, STT. Transcription corrected: "low" → "Flow".

## 2026-10-14 — No Primary without a Secondary; queuing

Context: comment on "A layer a request needs is started whether or not it is running."

> I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.

-- psyche, STT.

## 2026-10-14 — Flow routes hooks

> We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.

## No harness kept running for an idle session

Relayed by Psyche Flow Secondary, 2026-10-15; the living spoke to it directly.

> It's really important that we finish and deploy the new Flow Nexus, especially so that when a session is not running, we don't have to keep a harness going. If we have a lot of topics, we're going to have too many harnesses running in the background, and that will just bog down the computer with excessive RAM usage.

-- psyche, STT.

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

## Every flow starts with all its context modules

Context: ordering fresh Opus Ethos and Nexus flows, after seats started with 6 of 22 modules, 2026-10-16.

> "We can have a flow on each with an appropriately furnished system prompt and all the fucking context modules not just 6 out of 22 like a fucking imbecile, only putting one wheel on the car. We need all the wheels on the car. We need all the context modules on the flow that need it. No wonder we aren't getting anywhere if you have such a fucking catastrophic failure that you can't even load the context modules properly."

-- psyche, STT.

## A main flow is a manager, not a doer

Context: to the Psyche core Tertiary, on how it relayed the Ethos syntax comments by retyping them, 2026-10-16.

> "Why don't you just get the subflow to send the message?"
>
> "Isn't it better for the subflow to send the message if the subflow has it, than for you to repeat the same thing, copy the context twice, and then repeat the same words I gave you in your own context? When you're a main flow, your context should kind of be saved to try and manage things instead of doing a lot of things. You're a manager not a doer."
>
> "Pass all of this stuff up to Opus to rule on and maybe with Fable make a book."

-- psyche (input mode not shown).

## A Flow with an always-on core

Context: the living, on Flow work after the Today 2nd landings.

> Okay I've got Flow topic working on this but I want to migrate to a Flow that's modified to have an always-on core.

-- psyche, STT.

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
