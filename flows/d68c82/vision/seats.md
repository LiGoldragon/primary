
## Every boss has its secretary
"Okay I've compacted psyche spirit primary but I don't see any psyche spirit secondary. What the fuck? We're supposed to start a secondary before a primary. Let's make that a rule: we always start a secondary because you can't have a boss without a secretary. That's impossible so every boss needs its secretary."
-- psyche, STT, 2026-10-12.

## Fable judges; lower layers shovel

> I'd also like to talk about how we can insulate Fable from the low-level drudgery, the shoveling aspect that should be the concern of lower levels.
>
> I see a world where we have Fable Flow, or more than one, which doesn't actually have hardly any tool access. Something like that, where any questions that it brings forth would be researched and answered by other models. Some hooks would automatically forward these questions. The Fable Flow wouldn't have to make the call to a sub-agent to look into stuff. It would just pose the question and the question would be answered. The answer would be given back to it the next time it gets a turn, with all the other things that would be queued for it: whether they're new insights from the psyche, information that a previous turn was asking about, or anything like that. All of its context would revolve around making judgments, inferring, and summarizing instead of actually grabbing the shovel handle and shoveling.

Context: same comment, 2026-10-13T16:20.
-- psyche, STT.

## Subagents run Haiku, Sonnet and Opus; there is no Fable subagent

> We should have a haiku at the lowest power, and then a sonnet, and then an opus. There's no fable subagent.

-- psyche, STT.

## 2026-10-14 — every Primary has a Secondary, started first

> whenever we start a primary it needs a secondary. Every primary needs a secondary to act as a secretary. It's like a variant so you start the secondary first actually. The tertiary is so cheap that you might as well start one too so the secretary has its own assistant. I guess you could start the tertiary first. It's programmatic and it's so cheap. There's actually no point not doing it.
>
> Every topic, but then we run into the cost of running a harness. Especially with [Claude] and Codex harnesses, they're heavyweight. Maybe secondary and primary is good most of the time, especially in design, unless the topic becomes really big.

-- psyche, STT. Transcription corrected: "Cloud" → "Claude".

## 2026-10-14 — A Fable-assisted pair

> Send it to a fresh Fable-assisted primary and secondary. Starting with the secondary, we'll assemble all of the psyche-relevant and then start creating a prompt, not too long, like a couple thousand characters maximum, to add to what Fable will start with (so that he has a head start in terms of collecting stuff and it comes into the user prompt). Then Fable can just create the design and that's all Fable is for, really.
>
> The only thing it actually can be bothered with is to be given more information and then it can either be allowed to ask questions. If it ends its turn with a question or more than one question, then the secondary will just... We need an end-turn hook, basically, for the primary's turn end to notify the secretary.

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.

## 2026-10-14 — Lean mode: a rare Fable, protected Primaries

Context: spoken to the Psyche Flow Secondary on Claude usage running low; relayed.

> Need to limit the Fable calls dramatically. You can see we get "Get Codex to help you" because Claude is low on usage. Let's put Claude into low-usage mode and make sure that big Fable sessions are just retired right away, even if they're restarted. It'll have to go through me until we get more Fable usage or something.
>
> Let's start working just with a small lean Opus that I can talk to, with a Sonnet and Haiku assistant. Just this simple stack with limited topic usage and just going to coordinate mostly Codex usage. It's going to use Mind Secondary as a gateway for Mind Astra to essentially just respond with designs.
>
> Just like all the primaries, we need to pass this new, more efficient, high-efficiency infrastructure so primaries should be minimally disturbed. We should try and programmatically enforce that only secondaries can reach them, like the whole vertical stack enforcement, with just a fallback: if Metaflow is not active currently, respond when there's no recipient or something.
>
> Just make it simple and workable for now to try and limit, especially the Fable usage, but probably also Astra because I'm guessing our Codex usage. Let's check that too. Let's get a report on usage, how much under- or overused we are, and a historical look at maximizing our usage while also keeping enough usage to be able to continue designing and working.
>
> There are also two resets, I think, with ChatGPT/OpenAI that I need to check the date on so we should visualize that too. We should probably lean heavily right now, just like a single opus with its lower stack, like secondary maximum psyche with a rare Fable call. Basically mode now, so every Fable call has to go through me and has to be special.

-- psyche, STT.

## Model numbers stay out of view by default

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the depths line naming claude-haiku-4-5 and gpt-5.6-luna.

> All these model numbers are obsolete. Plus we shouldn't make the user interface expose the model number by default. Most users will be oblivious to the model number. It'll just be whatever is the default at that moment. We will at some point specify model numbers of course and then we might even have aliases sometimes when we want to keep some versions because it's interesting.

-- psyche, STT.
