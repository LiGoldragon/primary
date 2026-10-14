
## Flow exposes the harness; Message makes use of it; Flow first

Context: comment on «Flow: CLI, deployment, long term» (https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA), proposal «Flow exposes the harness; Message makes use of it; Flow first», 2026-10-14T15:15; relayed by Psyche Core Secondary.

> Yes this is good.

-- psyche, STT, 2026-10-14.

## Anybody may call Flow; a flow refreshes itself safely

Context: same book, proposal «anybody may call Flow; a flow refreshes itself safely», 2026-10-14T15:16; relayed by Psyche Core Secondary.

> Yeah this is good, especially the later part.

-- psyche, STT, 2026-10-14.

## A needed flow is started, running or not

Context: same book, proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», 2026-10-14T15:18; relayed by Psyche Core Secondary.

> We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.

-- psyche, STT, 2026-10-14.

## A full Flow Nexus proposal: short-term, and long-term/universal

Context: spoken to the Psyche Core Tertiary after commenting on «Flow: CLI, deployment, long term», 2nd edition; relayed by Psyche Core Secondary.

> I commented on Flow CLI development, or something like that, the second edition, and I want to add that I need to see a full Flow Nexus proposal, also probably separately.
>
> Let's have the short-term version and then the long-term/universal version: the parts that are independent of whether or not it's short-term or long-term, like the overall intention of the design, which is going to live in the long-term/Nexus proposal. We focus on specifying the ethos and from the ethos we already talked about the fact that we're going to derive the short-term prototype code.

-- psyche, STT, 2026-10-14.

## A started flow without a task: the default task is a proposal or a question

Context: comment on the vision-flow L24 line (a needed metaflow started with its context modules and prompt), 2nd edition of «Flow: CLI, deployment, long term»; relayed by Psyche Core Secondary.

> Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. Just mentioning it: by default maybe you set it somewhere else later on but the default task is to create a proposal or a question.

-- psyche, STT, 2026-10-14.

## Vertical communication is not strictly short-term

Context: comment on choice 2, vision-model-roles L51 «Short-term: vertical communication stays within one aspect and normally advances one layer at a time.»; same book.

> This concept is not strictly short-term. What makes you think this is a short-term concept?

-- psyche, STT, 2026-10-14.

## The obsolete routing lines are removed

Context: comments on the vision-model-roles L62–69 and L52–55 deletions; same book.

> Yes do all that removal.

> Yes we can remove that.

-- psyche, STT, 2026-10-14.

## No Primary is started without a Secondary; queuing is a goal

Context: comment on choice 3, «A layer a request needs is started whether or not it is running.»; same book.

> I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.

-- psyche, STT, 2026-10-14.

## A still-young working transcript is reawakened; what young means

Context: comment on choice 4, «with a working transcript, its flow is reawakened from it»; same book.

> I would say, with a still-young working transcript, let's have a proposal to explain what a young context is in terms of ratio and where average context size starts to degrade rapidly (around the 100,000-token point).

-- psyche, STT, 2026-10-14.

## Flow decides where hooks talk

Context: same speech to the Psyche Core Tertiary, on hooks; relayed by Psyche Core Secondary.

> We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).

-- psyche, STT, 2026-10-14.

## Low-usage mode: a lean Opus with Sonnet and Haiku; every Fable call goes through the living

Context: the living, directly to Psyche Flow Secondary da2038, on Claude usage running low ("Get Codex to help you").

> Need to limit the Fable calls dramatically. You can see we get "Get Codex to help you" because Claude is low on usage. Let's put Claude into low-usage mode and make sure that big Fable sessions are just retired right away, even if they're restarted. It'll have to go through me until we get more Fable usage or something.
>
> Let's start working just with a small lean Opus that I can talk to, with a Sonnet and Haiku assistant. Just this simple stack with limited topic usage and just going to coordinate mostly Codex usage. It's going to use Mind Secondary as a gateway for Mind Astra to essentially just respond with designs.
>
> Just like all the primaries, we need to pass this new, more efficient, high-efficiency infrastructure so primaries should be minimally disturbed. We should try and programmatically enforce that only secondaries can reach them, like the whole vertical stack enforcement, with just a fallback: if Metaflow is not active currently, respond when there's no recipient or something.
>
> Just make it simple and workable for now to try and limit, especially the Fable usage, but probably also Astra because I'm guessing our Codex usage. Let's check that too.
>
> ... We should probably lean heavily right now, just like a single opus with its lower stack, like secondary maximum psyche with a rare Fable call. Basically mode now, so every Fable call has to go through me and has to be special.

-- psyche, STT, 2026-10-14.

## A Fable fallback; lean datom calls; a language of changes; Astra designer mode under 128k

Context: the living, directly to Psyche Flow Secondary da2038, after the low-usage order.

> And I want research into the best Fable fallback. Probably it's going to be in the open source camp in the sense that we need it. I would like to have something to lean on to use less Fable, whether it's by using it as a front before Fable to make sure that the communication is always relevant.
>
> Basically we have this Opus. We need these light calls that have almost no training, no system prompt pre-training (or not pre-training but pre-prompt, like the harness-injected stuff). We really don't need any of the tools and stuff. We just have our own specialized datom-based dialect.
>
> The response just comes in as datom, with the variant and then the payload, which is probably a struct. We should have more than one field. There's always something useful, like the meta part of the payload, right? It could even be its own struct so that it's visually sort of like, "Here's the meta." You can even divide it like that so that cognitively you're telling the system how to design, right? You add meta here.
>
> In datom it's cheap because it's just an additional pair of braces. There's your inner struct, which is the metadata of your whatever, your simple last response, which is just text. It's like the default. Well it's not the default. I guess even the most basic responses can't even be just a single string payload because it would be a proposal, which would have a path at least. A single proposal is the basic fallback default, right, or multiple proposals and then you have a vector of them. They're each about something, the most basic of which is a path and then a diff, which can basically just take a variant, right, where you just have a plain edition, targeted edition, or whatever.
>
> Let's develop a really cool language to talk about changes. Also just for now, basic: between certain paragraphs or in a certain section because Markdown is its own structured data, we can map Markdown into a certain datom-based language of variants. You could even get an output of Flow to sort of draft that into a book and then get an Astra.
>
> All you have to do is basically collaborate with [Mind] Secondary and then we use Astra in this designer mode with secondary in its own aspect, maximizing the efficiency of each call. We make sure that the context doesn't grow beyond 128,000 tokens at the time of the call, right? If it's 127 then we can still use it especially if it's on the same topic.
>
> If it's not on the same topic, if it's a wildly varying topic, that's why we want lean calls: it's cheap to just start another one because it really doesn't even need tool calls. It can just talk to secondary to ask it what it would like to know. All the tool calls are really just talking to the secondary and the secondary then handles ...

-- psyche, STT, 2026-10-14. Transcription corrected: "mine secondary" → "[Mind] Secondary". The last sentence is unfinished.
