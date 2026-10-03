# Quota and context-usage requirements

## Proposed immediate scope

This flow proposes a reliable, simple Nexus-owned query that reports Claude and
Codex subscriptions, quotas, and context in one CLI call as the first
deliverable. The proposed boundary is a snapshot/reporting boundary. The quoted
records do not themselves approve excluding a daemon, Persona history, or a
live Watch; they establish the requirements below while those choices remain
implementation sequencing.

### One-call provider query

> I want a tool. I want the most reliable way to design this tool to get the context, my quotas, and my different subscriptions. I want that tool now so that you can get an update on your own. You can programmatically get an update on your own quotas once in a while, or you can ask the tool, and then you can tell me. With one boom, one CLI call, you get the full breakdown of all my subscriptions and quotas, and it shouldn't be that hard.

-- psyche, STT. Source: `flows/28d847/vision/quotas.md`.

> ... collect all of our requirements and make a simple Nexus component to query things from Codex and Claude. Maybe it's called... I don't know. Maybe there's one for [Claude] and one for Codex. Didn't we already have a repo for that?

-- psyche, STT. Source: `flows/28d847/vision/quotas.md`.

### Per-subscription quota, daily allocation, and target variance

> Is Codex working? I haven't even gone. The remote access on Claude is better, so it would be cool if I get a periodical, a small report on how much Codex has been going. Let's start getting the quotas measured.
>
> When I ask for a report, like a situation report, which is going to be a thing, I guess, then I get the quotes for each subscription that is left, and how much that turns out to be per day, and whether or not we're above or below percentage-wise and stuff. Let's start working out how we want to visualize that best, so you could do some heuristics research on how to best represent something like that.

-- psyche, typed. Source: `flows/692df8/vision/quota.md`.

> I want you to start working on a protocol for managing the quotas for the usage of both Claude and Codex, so that they are balanced and meet up at the end of the week if we use them at about 14% per day. We try to keep that rhythm.
>
> This would also drive the frequency of update of certain parts, with priority to the core and primary. It's better to agree on ideas and proof of concepts and things that we want to land directly from primary, which can then go to secondary to be implemented into production and at scale.
>
> We're going to have some kind of accounting system for these quotas. If Codex has not much usage, then Claude can start driving the proof of concept more with some Opus jobs, which are really good to manage, like an Opus main flow sub-job. If you want to make a big job out of it with a custom prompt, that makes it really good at knowing what it wants to do and doing a really good job. Opus 5 can do that really well. Also, it was kind of made as a response to Sol or whatever.
>
> Even small jobs can be driven by Sonnet on the Cloud side, and trivial jobs can go to Haiku or Sonnet. Sonnet is really good also and quite cheap.

-- psyche, STT. Source: `flows/6cc91b/vision/quotas.md`.

### Windows, resets, slack, and freshness

> I see you're talking about continuous operation, and I think what I want to do is a quota-based thing. If my quota is being unused for the daily or hourly rate, or if you divide the week by the number of hours in the week, then we would run some light encouragement to keep concepts materialized so they can be tested.
> ...
> Let's get this machine rolling and humming on the usage that we have.
>
> Like I said, Codex, we can use the week before, like 3 days before, which will be perfect, because then that means we can use another week with the reset in 3. Or, sorry, no, that's not how the reset works. Anyway, if we want to go more heavily for now, we can use Codex until we use that reset. We have a reset before the 20th of September, so let's use it.

-- psyche, STT. Source: `flows/840e42/vision/quota.md`.

> Well, obviously, the 5-hour window is something to contend with, and I think that it's a good gauge for maintaining a fair amount of usage for each. There are different metrics too. If Fable gets overused, then we have to fall back to an Opus model for Claude, and so on.
> ...
> The Slack is counted in various ways, some of which is more used internally than as a user. It's not so much for the user to see, right? It's for the whole system to then manage the usage from that and know when to start flows, and so it's going to start waiting on a design aspect, maybe for a bit, before going into implementation because the codex usage is high, right? It might as well just wait for more vision to come in if that's what's happening, and for some concepts to be fleshed out with the psyche. The codex could also be overabundant, and then the code that's maybe talking to the psyche is using codex to help it think out loud, in real time, to find data and to search transcripts or whatever. It would use its own subagents. 4, so it's uploading onto codex, and that's why the interface has to be flawless.

-- psyche, STT. Source: `flows/840e42/vision/quota.md`.

Freshness is required for a truthful report: every provider value needs its
observation time and explicit source state. This is a necessary interpretation
of a current quota/window report, rather than a separately spoken output-field
specification. Unknown, unavailable, stale, and incompatible values must stay
distinct rather than becoming zero or a fabricated remaining value.

### Context and input/output usage

> Keep things flowing and try and figure out how you're going to log how much context and how many tokens of input and output are used by all the models, maybe if that's possible and if it's recorded in the harness. If we don't have to ask the agents to try and tell us, which I think is kind of wasteful, we could ballpark estimate from what we send and what some programmatic tool measuring thing (maybe one that already exists or that we can copy the patterns of)

-- psyche, STT. Source: `flows/6cc91b/vision/quotas.md`.

The immediate report may expose source-backed context proxies, provided it says
which proxy/basis produced each value and does not present an emitted-token
counter as current resident context. This preserves the request for context
without inventing a vendor fact.

### Push collection rather than polling

> "get Mind to research and design a component that would keep track of my subscription allowance and my different harnesses. This is something we've researched before. Look at previous art and how other people have attempted it.
>
> Let's go for a hook-based, push-based check and not a polling-based check because we don't need to check what the quota is if no agent is ever running, right? When an agent has an event, meaning some work has been done, and it doesn't have to be at the end of the turn, this tool that uses no LLM can do another checkup and ask him also about the research and systems."

-- psyche, typed, 2026-10-03. Source: `flows/9fb0ad/vision/quotaTracking.md`.

The snapshot command therefore has no timer/polling loop. A later event hook can
invoke the same bounded query after a harness event, without an LLM.

### Persona accounting boundary

> How is the work on the quota accounting, which I guess we would put in maybe a new component or in Persona? That's where it goes. That would be a good use of Persona for now. Persona keeps track, I guess, unless you have an idea.

-- psyche, STT, relayed. Source: `flows/5f4fea/vision/quotaAccounting.md`.

The CLI may read current sources and calculate a report. It does not relocate,
replace, or write Persona's accounting ledger.

## Proposed downstream scope

This flow proposes that the following real requirements follow the initial
one-call snapshot because they need durable observation/history and a later
presentation or Nexus integration. This is not a living-approved exclusion
from the component.

### Multi-provider power state, history, and visual analytics

> What do you mean? We're not in low-resource mode anyway now because the Opus subscription, the cloud subscription, reset. Let's get one of the mind components, maybe Astro, if he's not busy, to maybe refresh and design a quota.
>
> We already started that a long time ago: a quota awareness system, a quota accounting system that remains aware of the quotas on subscriptions, and eventually multiple subscriptions will be supported. It is just to keep track of whether we're in high-power mode or in low-power mode with different providers.
>
> If there is a reset, right now we have a Codex reset, so it's not like we can actually go into high-power mode, use a reset, and use a week and a half a week.

-- psyche, direct to primary Psyche opus b81560. Source: `flows/b81560/vision/operational-quotaAwarenessSystem.md`.

> Let's move things forward with Codex. We have reset, so we can start getting a low-level worker to start putting reports together on quota usage and figuring out what kind of system we can do to keep track and collect data. We can figure out our burn rate at different times and create visual graphs and correspond them with psyche activity and stuff like that.

-- psyche, direct to primary Psyche opus b81560. Source: `flows/b81560/vision/operational-quotaBurnRateVisualGraphs.md`.

> Let's all keep track of the quotas and the burn rates, estimated burn rates.
>
> Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop. The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately. It creates a few, like 4 or 5, useful metrics.
>
> Show me the anatomy of all that: the quota visualization interface.

-- psyche, artifact comment. Source: `flows/b05237/vision/operational-quotaBurnRateHook.md`.

### Lifecycle and archives

> And if any, we shouldn't let the models compact. There's no need. They're better off rebootstrapping on with a really good first prompt on a new flow.
>
> The old flow will wind down and maybe be archived or something, depending on how we decide to archive things or how to mark things as archived by changing the thread name, like "ancestor" or "concluded," or a different status, I guess. I guess a concluded thread could be reawakened to ask a question if we want, but maybe because of how long the cache lasts, it would be expensive to do that, so it's better not to.
>
> At a certain maximum, at 60%, the flow basically has to change over, but it can restart if the conversation shifts dramatically. It can restart and repopulate itself with a better context for that emphasis in a fresh flow, starting from having around 200,000 tokens of context, right? 20, 30% for Claude, and I don't know what that is for Astra.

-- psyche, STT. Source: `flows/6cc91b/vision/flowLifecycle.md`.

> Let's talk also about garbage collecting sessions and sort of archiving them, and just keeping the important parts of the exchanges, like the main responses and the most important parts of the prompts and the final responses of the agent flows.

-- psyche, STT. Source: `flows/6cc91b/vision/sessionArchiving.md`.

Context figures inform lifecycle decisions but must not themselves compact,
restart, archive, or alter a session in the initial read-only component.

## Reporting boundary

> Okay, let's agree that the thing I read now is the latest report. Just update your last report, or make a combined version of them, and that's the sort of report update protocol that we're going to develop.
>
> If everything you've done has been in the report, and if you're waiting on questions from multiple of them, you need to combine them. I'm only going to read one report at a time. If there's anything I haven't addressed in the report, I haven't even mentioned or commented on, you just have to not leave anything there undone, right? If it's still relevant, if this hasn't been answered essentially by me just talking without reading the report or whatever, then you're going to do that.

-- psyche, STT. Source: `flows/6cc91b/vision/reporting.md`.

The proposed initial output is a concise human situation report with a
machine-readable typed reply that retains source, basis, timestamps, and value
states. A JSON projection is optional only where it fits the actual CLI; no
quoted requirement mandates JSON. Historical graphs and burn-rate inference
are proposed as separate, later metrics/reporting work.

## Sources

- `flows/28d847/vision/quotas.md`
- `flows/6cc91b/vision/quotas.md`
- `flows/6cc91b/vision/flowLifecycle.md`
- `flows/6cc91b/vision/reporting.md`
- `flows/6cc91b/vision/sessionArchiving.md`
- `flows/692df8/vision/quota.md`
- `flows/840e42/vision/quota.md`
- `flows/9fb0ad/vision/quotaTracking.md`
- `flows/5f4fea/vision/quotaAccounting.md`
- `flows/b81560/vision/operational-quotaAwarenessSystem.md`
- `flows/b81560/vision/operational-quotaBurnRateVisualGraphs.md`
- `flows/b05237/vision/operational-quotaBurnRateHook.md`
