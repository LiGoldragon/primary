# Source packet for the context, usage, and flow books

For the active Sonnet book seat. This packet is editorial source, not a
published book, design approval, or implementation instruction. It separates
the living's words, current observed capability, proposed technical shapes,
and the exploratory per-topic-flows notion. Preserve those distinctions in
the books.

## Editorial boundary

The material concerns four related but non-equivalent subjects:

1. **Quota and usage telemetry** — the living asks for subscription/quota,
   context, and time-based visibility. A working one-shot snapshot exists with
   defined limits.
2. **Queued context at wake/message time** — the living envisions a hook that
   can accumulate relevant material and deliver it when a flow next receives
   a message or wakes. Queue ownership, relevance, ordering, and urgency are
   undecided.
3. **Flow lifecycle and handoff** — existing vision says a context threshold
   can notify the responsible refresher and allow a handover before messages
   reach the replacement. This does not itself choose a telemetry contract or
   a queue format.
4. **Per-topic flows** — explicitly a notion being floated for research, not
   a requirement. It may include several Fables/Astras across aspects, finite
   lives, and perhaps several flows per seat.

Do not turn questions, a report's proposed design, or external precedent into
living-approved architecture. Do not add compatibility rationale or claim an
exact current-context meter where the current source supplies only a proxy.

## Living records — reproduce intact

### Usage, quotas, time, and programmatic measurement

> I want a tool. I want the most reliable way to design this tool to get the context, my quotas, and my different subscriptions. I want that tool now so that you can get an update on your own. You can programmatically get an update on your own quotas once in a while, or you can ask the tool, and then you can tell me. With one boom, one CLI call, you get the full breakdown of all my subscriptions and quotas, and it shouldn't be that hard.

— psyche, STT. [Source](../28d847/vision/quotas.md).

> It has to also show us how much time is left and then compute all the other metrics. We looked into that before: some kind of transformation that we would put using the time. We'll refine the algorithms, but let's maybe find out what the best is for this kind of thing, to cognitively better visualize it: how much use you have per time and for how much time. That is also really important because if what I have left is until tomorrow morning, then obviously it's different than me spending it during the daytime.

— psyche, STT. [Source](../28d847/vision/quotas.md).

> I want you to start working on a protocol for managing the quotas for the usage of both Claude and Codex, so that they are balanced and meet up at the end of the week if we use them at about 14% per day. We try to keep that rhythm.
>
> This would also drive the frequency of update of certain parts, with priority to the core and primary. It's better to agree on ideas and proof of concepts and things that we want to land directly from primary, which can then go to secondary to be implemented into production and at scale.
>
> We're going to have some kind of accounting system for these quotas. If Codex has not much usage, then Claude can start driving the proof of concept more with some Opus jobs, which are really good to manage, like an Opus main flow sub-job. If you want to make a big job out of it with a custom prompt, that makes it really good at knowing what it wants to do and doing a really good job. Opus 5 can do that really well. Also, it was kind of made as a response to Sol or whatever.
>
> Even small jobs can be driven by Sonnet on the Cloud side, and trivial jobs can go to Haiku or Sonnet. Sonnet is really good also and quite cheap.

— psyche, STT, 2026-09-14. [Source](../6cc91b/vision/quotas.md).

> Keep things flowing and try and figure out how you're going to log how much context and how many tokens of input and output are used by all the models, maybe if that's possible and if it's recorded in the harness. If we don't have to ask the agents to try and tell us, which I think is kind of wasteful, we could ballpark estimate from what we send and what some programmatic tool measuring thing (maybe one that already exists or that we can copy the patterns of)

— psyche, STT, 2026-09-14. [Source](../6cc91b/vision/quotas.md).

> "get Mind to research and design a component that would keep track of my subscription allowance and my different harnesses. This is something we've researched before. Look at previous art and how other people have attempted it.
>
> Let's go for a hook-based, push-based check and not a polling-based check because we don't need to check what the quota is if no agent is ever running, right? When an agent has an event, meaning some work has been done, and it doesn't have to be at the end of the turn, this tool that uses no LLM can do another checkup and ask him also about the research and systems."

— psyche, typed, 2026-10-03. [Source](../9fb0ad/vision/quotaTracking.md).

### Context visibility

> Well that's a big problem so we should design a solution to that. There's Steve Yeggy: he has his own wheelhouse and he has a screen where he can see the context and the usage of everything. People have done it and it can be done for any harness so there's no excuse except "I haven't done it yet."

— psyche, typed, 2026-10-04. [Source](../vision/context-visibility.md).

This record answers a current visibility problem. The local context-visibility
investigation verified Wheelhouse's operational screen and per-account burn
telemetry, but not an exact, provider-authoritative per-flow prompt-occupancy
reading. Keep that limitation visible.

The following are preserved as questions/corrections, not vision to restate:

> Can we get context size on everything? How hard is that?

— psyche, typed, 2026-09-25, directly to Field Sol b7da5d.

> That doesn't really answer my question. Can we make a single tool call that gets us the context size of every flow?

— psyche, typed, 2026-09-25, directly to Field Sol b7da5d. [Source](../b7da5d/vision/contextSize.md).

### Queue at the next wake/message

> I'd like some of the flows, or maybe all of the flows, once we get a hook in place, where we control what gets injected in the prompt and what goes through messaging. Essentially we can inject more stuff along with the messages that are coming into a certain flow. We can use that opportunity to inject a bunch of other stuff that has been queued in preparation for that particular flow to be woken up, so that it would know all of this as soon as it woke up. Yet we wouldn't have to wake up every time some accumulation of vision or whatever that touches its lanes or its topics is coming into the system.

— psyche, typed, 2026-10-04. [Source](../vision/flow-context-injection.md).

Earlier, the living framed a narrower hook as a question and asked for the
visualization anatomy:

> Let's all keep track of the quotas and the burn rates, estimated burn rates.
>
> Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop. The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately. It creates a few, like 4 or 5, useful metrics.
>
> Show me the anatomy of all that: the quota visualization interface.

— psyche, artifact comment, 2026-09-18. [Source](../b05237/vision/operational-quotaBurnRateHook.md).

### Threshold-triggered refresh and handoff

> You need to refresh yourself. We need some way to automate the refresh call. When a model reaches a certain context window, whoever is in charge of refreshing should get a message that some flow needs to be refreshed. I guess the flow itself needs to know so that it can create a handover response. At that point that same hook system picks up the final response and essentially locks the messages from being sent over there immediately.
>
> If there are sub-agents still working, it's okay. I guess we could just notify the new flow of what happens after they return, and/or what they returned or whatever. Maybe even the sub-agents eventually will be able to message them to tell them who to message their results to and in what way. We're not going there yet. I'm just talking about this hook principle we can use in many ways like that.

— psyche, typed direct user turn, 2026-09-26. [Source](../b860be/vision/refreshAutomation.md).

### Per-topic flows — explicitly exploratory

> I have this notion that we need flows that are per topic so we might have more than one Fable and more than one Astra in different aspects. They would not necessarily be really long-standing and they could possibly have more than one flow. It's a concept that I'm floating up and maybe someone wants to research what other people have done, seen, tested, experimented with, or envisioned in that regard.

— psyche, typed, 2026-10-04. [Source](../notion/topic-flows.md).

## Current observed tool surface

The active source review reports Harness 0.6.1's one-shot, owner-local,
read-only `UsageSnapshotQuery` and its human wrapper. The existing working
command forms are:

```text
harness-usage
harness UsageSnapshotQuery
```

Their successful installation/execution is Field-reported acceptance evidence,
not rerun in this packet. The surface returns subscription windows and context
observations with timestamps and typed unavailable results; it starts no
model. It is not a live per-Flow occupancy query.

Current context semantics to state plainly:

- Codex supplies last-request input-token accounting and sometimes a recorded
  context-window capacity. The relation is a proxy for the preceding request,
  not current prompt occupancy.
- Claude supplies the previous assistant request's input plus cache-token
  accounting as a proxy. The deployed collector has no window capacity or
  exact percentage.
- Thread-cumulative tokens are accounting/history, not context occupancy.
- The contract names `Exact`, `Proxy`, `Superseded`, and `Unknown`; existing
  collectors use only proxy bases. A later user event or compaction supersedes
  a prior occupancy claim rather than making it zero.

These are current evidence-backed facts from
[context-visibility-gap.md](context-visibility-gap.md) and
[quota-acceptance-review.md](quota-acceptance-review.md). Do not present the
proposed future Flow-to-native-session binding, `FlowContextQuery`, exact
adapters, dashboard, ledger, or polling service as deployed.

## Research evidence for a book's “what others did” material

[topic-flows-research.md](topic-flows-research.md) is the finalized bounded
research report. Its evidence classes must stay distinct:

- Anthropic's production Research account implements task-bounded, isolated
  research subagents and reports an internal breadth-first evaluation; it also
  reports high multi-agent token cost. It is not evidence for persistent,
  user-addressable topic assistants.
- Microsoft Research's Magentic-One implements an orchestrator with task and
  progress ledgers and publishes benchmark/ablation results. It supports
  testing a ledger/routing hypothesis, not that more roles or sessions always
  improve work.
- A2A gives identifiers and lifecycle vocabulary for context/task/artifact
  continuity. It is a protocol, not an evaluation of delayed wake injection
  or topic routing.
- Steve Yegge's closed Wheelhouse essay visibly supports an operational and
  account-usage screen; public Gas Town supports dashboard and handoff
  mechanisms. Neither source establishes provider-authoritative live context
  occupancy across harnesses.

The report's bounded experiment is an optional research design, never an
approved rollout. It compares one session with independently scoped finite
facet sessions, using correctness, cross-facet omission, handoff
reconstruction, time, token/tool use, and duplicate-receiver outcomes.

## Editorial gaps that must remain gaps

- A topic's definition, router, correction path, and user-visible identity.
- Whether one topic can have parallel workers while exactly one flow receives
  user messages.
- Queue ownership, relevance criteria, delivery ordering, source references,
  freshness/staleness, urgent delivery, and conflict handling.
- Which information survives a finite flow: artifacts, source references,
  handoff, identity, or another bounded set.
- A current authoritative provider endpoint for per-flow live occupancy,
  including its scope and freshness.
- Thresholds or policy for refresh, quota balance, and scheduled/continuous
  work.

## Source map

Primary living records:

- [quotas, 2026-09-14](../6cc91b/vision/quotas.md)
- [quotas and time, current collected record](../28d847/vision/quotas.md)
- [push-not-poll quota hook, 2026-10-03](../9fb0ad/vision/quotaTracking.md)
- [context visibility, 2026-10-04](../vision/context-visibility.md)
- [flow context injection, 2026-10-04](../vision/flow-context-injection.md)
- [refresh automation, 2026-09-26](../b860be/vision/refreshAutomation.md)
- [per-topic notion, 2026-10-04](../notion/topic-flows.md)

Evidence/research reports:

- [context visibility gap and current capability](context-visibility-gap.md)
- [quota acceptance review](quota-acceptance-review.md)
- [quota metrics design](quota-time-metrics-design.md)
- [topic-flows research](topic-flows-research.md)

The two current reports named above are evidence, not psyche. Use their source
citations rather than copying a design decision out of them as a living word.
