Presentation.{ «Models, effort and quota» }

Which model sits in which seat, what effort means, how quota is read and shown, when the system slows down, and what cost is counted. A seat is one long-lived post, an aspect at a power tier. Quota is the share of a subscription's usage window already spent.

## 1. What he wants

### Better models, not higher effort

Capability comes from picking a better model. Effort is a setting on a model call, and it stays at medium.

> If we want better AI, we need better models, not higher effort. Let's put that in the intent somewhere.

-- 18 September 2026

High effort is a sign of rushing. It is kept for one case only: a quota about to reset unused.

> From now on, high effort is kind of a waste. It's a waste of energy. It means somebody is rushing.

-- 13 September 2026

> If my quotas are running out and I don't have much time to use it, then we can go into high effort and use up our quotas.

-- 13 September 2026

Proposed: effort may go lighter for speed, as in voice, but never higher for quality.

### A tier word names power, not effort

High, medium, low and ultra-low name how much energy a seat burns. That is set by which model holds the seat, not by its effort setting.

> I think there's been confusion because when I say "high psyche high," I think he starts Astro on high and Fable on high because it's called high, but it's all medium.

-- 18 September 2026

> It's a power level, right? High because it's literally how much energy we're spending.

-- 17 September 2026

> Sonnet is low-powered. I didn't say low effort. Low corresponds with Sonnet.

-- 25 September 2026

### Which model sits where

The Claude side carries Psyche. The OpenAI side carries Mind and Field.

> The stack of basically mind runs on the OpenAI stack and field as well.

-- 20 September 2026

**Psyche, on Claude.** High is Fable, the main-flow model.

> Fable is the Claude code main flow model.

-- 13 September 2026

Medium is the older Opus, chosen for its disposition to doubt and ask rather than act. The seat is Opus 4.6 with the million-token context.

> I think I would like 4.6 even better than 4.7, the 4.6 1 million token.

-- 18 September 2026

Low is Sonnet. Ultra-low is Haiku, because it doubts more and invents less.

> If the Haiku has a much lower hallucination rate, then we should use it for the ultra-low-power Psyche, then.

-- 21 September 2026

**Mind and Field, on OpenAI.** High is Astra: quick, willing, sometimes reckless, its work checked afterward. Medium is Sol. Low is Terra, ultra-low is Luna.

> It commits more easily and does more quickly, but also more recklessly sometimes.

-- 16 September 2026

> And then the main flow for the lower layer is the old Opus. On the Codex side, it's the latest Sol, and at the higher layer, it's Astra.

-- 16 September 2026

Terra is paused until its next version, and Luna takes its jobs.

> We're going to take out Terra until Terra 6 releases and we're just going to give those jobs to the new Luna 6 instead.

-- 24 September 2026

Outside Psyche, ultra-low is Luna, because a Claude session costs a whole harness to start.

> Since we're launching the whole harness, we're better off just leaning on Luna for ultra-low power everywhere.

-- 20 September 2026

**Who designs and who builds.** Fable and Astra design. The secondary Opus builds and tests with Opus helpers.

> Primary deals with designs and ideas, and he passes them on to secondary.

-- 3 October 2026

**Delegation goes down, not up.** Fable and Astra are main flows only; nothing starts one as a helper. Fable hands work to Opus, Sonnet and Haiku; Astra to Sol, Terra and Luna, cheapest first.

### Fable is the most expensive voice

Fable is spoken to rarely, and only with something worth saying.

> We should really minimize how much Fable is talked to because it's the most expensive model.

-- 28 September 2026

When Fable's share runs thin, the Claude side falls back to Opus.

> If Fable gets overused, then we have to fall back to an Opus model for Claude, and so on.

-- 15 September 2026

There is only ever one Fable seat at a time. A second one, or one left running at high effort, is an emergency.

> We have to take urgent action to stop bad model flows from being started or from continuing on when they should be stopped.

-- 26 September 2026

### The model is declared in one place

One declaration names each seat's model, and every skill and launcher reads it. No code writes a model number by hand.

> Let's make that model set in one place, and then that one declaration sets it everywhere in the skills and everything. That's what the Nexus architecture is like.

-- 18 September 2026

> Let's make sure there's no part of the code that hardcodes model numbers.

-- 29 September 2026

Proposed: until Flow holds the declaration, the shared variables file carries every seat's model and effort, not only one seat's.

### The third model, open-source

A third model family will join Claude and OpenAI. It is open-weight, chosen for doubt and care, and has its own helpers.

> We want the most careful and doubtful and conceptually capable, especially when given lots of incentive to research and consult the knowledge database.

-- 14 September 2026

> Yeah, Kimi K3 on OpenCode sounds great. Let's set that up.

-- 14 September 2026

> If OpenRouter works for privacy and choosing the models that we want, then, if it's easy, I can set up an account.

-- 14 September 2026

Local models run only on the machine that holds the AI-node role.

> It's whichever node plays the role of what we're calling a large AI node

-- 26 September 2026

This third seat also opens the private part, which is chartered but not active.

### Quota is read by one call, with no model in the loop

One command, a simple Nexus component, returns every subscription, every quota window, and every live seat's context use.

> With one boom, one CLI call, you get the full breakdown of all my subscriptions and quotas, and it shouldn't be that hard.

-- 3 October 2026

It is pushed by events, never polled, and uses no model. When nothing runs, nothing is checked.

> Let's go for a hook-based, push-based check and not a polling-based check because we don't need to check what the quota is if no agent is ever running, right?

-- 3 October 2026

Context and token use come from the harness's own records. Seats are never asked to report on themselves.

> If we don't have to ask the agents to try and tell us, which I think is kind of wasteful

-- 14 September 2026

Proposed: each check runs on a seat's work event, at most once every few minutes, and writes one record.

### How quota is shown

A situation report gives, per subscription, what is left, what that comes to per day, and whether we are ahead or behind.

> I get the quotes for each subscription that is left, and how much that turns out to be per day, and whether or not we're above or below percentage-wise and stuff.

-- 15 September 2026

The weekly rhythm is about fourteen percent a day, Claude and OpenAI meeting at the week's end. The five-hour window keeps each day fair.

> They are balanced and meet up at the end of the week if we use them at about 14% per day.

-- 14 September 2026

> Obviously, the 5-hour window is something to contend with, and I think that it's a good gauge for maintaining a fair amount of usage for each.

-- 15 September 2026

Seats get four or five ready-made figures attached to their next message, so they never stop to check.

> The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately.

-- 18 September 2026

Burn rate is drawn as graphs, set against his own activity.

> create visual graphs and correspond them with psyche activity

-- 19 September 2026

A monitoring view shows each candidate's stack and memory use.

> I need a better view of what the different candidates are in terms of their stack. What kind of stack do they have? What's the memory usage?

-- 3 October 2026

Proposed: the five figures are percent used, percent left, time to reset, burn over the last five hours, and today's share against fourteen percent.

### What triggers low power

The system always knows, per provider, whether it is in high-power or low-power mode.

> It is just to keep track of whether we're in high-power mode or in low-power mode with different providers.

-- 19 September 2026

As a notion, not a ruling: a gauge that tells seats to slow down.

> A quota-gauge program that keeps running and tells people to slow down when they're over quota.

-- 27 September 2026, notion

A low-priority helper may refuse a job the remaining quota cannot pay for. Decisions climb toward the primary seat.

> If it's going into low-power mode, it has to say, "Maybe this would take too long, and we don't have enough quota," right?

-- 16 September 2026

An ultra-low Field job keeps track of power and decides how many helpers the system can afford.

> basically deciding how much power to allocate on certain subflows

-- 19 September 2026

When quota sits unused, light work runs to keep ideas built and testable. When OpenAI usage is high, the system waits on design.

> If my quota is being unused for the daily or hourly rate ... then we would run some light encouragement to keep concepts materialized so they can be tested.

-- 15 September 2026

Proposed: low power starts when a subscription is more than one day's share ahead of the fourteen-percent line, or its five-hour window passes eighty percent. In low power, Fable is not called, new helpers drop one tier, and only primary work starts.

### What cost is counted

Cost is counted in context as much as in money. A wasted token is a cost, however small.

> token costs are not qualified by size, but by necessity. a useless token cost must be eliminated

-- late August 2026

> Messages that absolutely have nothing to do with you and are costing us money (a lot of money in terms of the fact that it's polluting your context and then degrading our design, destroying our machine).

-- 3 October 2026

Switching a running seat's model is a cost too, because everything is read again.

> I just changed your model but that costs money because now you have to recompute everything.

-- 24 September 2026

An accounting system weighs quota, priority and where context is spent next. For now, Persona keeps the books.

> There's a whole accounting system that keeps track of how much quota there is, what's a priority, what we need to spend LLM context on next, and so on.

-- 3 October 2026

> That would be a good use of Persona for now. Persona keeps track, I guess, unless you have an idea.

-- 15 September 2026

## 2. What exists today

His subscriptions are Claude Max, the twenty-times tier, and ChatGPT Pro. Read live this evening: Claude five-hour window 20%, Claude weekly 11%, Fable weekly 10%, Codex weekly 21%. Both providers give percentages only, never an absolute limit. That reading was a manual check, not a running tool.

Mind Astra has designed the one call as a read-only request on the existing harness program, returning both providers, every window, and each live seat's context. Its build handoff to the secondary is held undelivered. The harness code has no quota code yet, checked tonight.

The older field census tool last wrote on 27 September. It runs on no timer now.

The variables file names one seat only: psyche medium Claude, Opus 4.6 with the million context, medium effort. Fable, Sonnet, Haiku and the OpenAI seats are declared nowhere in one place.

## 3. Questions

**1. Where do the quota books live?** Answer 1 for Persona, 2 for the OpenAI bridge, or 3 for the harness program that gives the one call.

**2. Is fourteen percent a day the line?** Answer yes if passing it by one day's share, or eighty percent of a five-hour window, puts that provider in low power. Otherwise give your number.

**3. How many power tiers on the OpenAI side?** Answer 3 for high, medium and ultra-low while Terra is paused, or 4 to keep a low tier.

**4. Should every seat's model go in the variables file now,** until Flow holds the declaration? Answer yes.
