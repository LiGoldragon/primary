
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
