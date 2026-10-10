# Reports

## 2026-08-22 — "do we even need reports?"

Context (agent, brief): the flow had admitted it filed the
software-design review packet unread, relaying the subflow's account
in near-factual voice. The psyche then questioned the value of
subflow-written reports as such. Verbatim, spoken to flow cff271af:

> Here's the thing. The living speaks to the main flow. So, if we
> have a bunch of artifacts, I mostly don't read reports. They're
> there for... To be honest, right now I'm wondering, in most cases,
> do we even need reports? Because if the audience is in the main
> flow, and in almost all the cases is not me, then what is really
> the intended audience? And what is the point of doing all this
> research if the main flow only really just pretends to be or is
> only superficially aware of them? So, it's alright for subflows to
> do research. That's their purpose. But I don't see that much value
> in them creating all these reports. Because, see, the problem is
> the main flow won't actually be aware of their content. And then
> the conversation will go through, this flow will go through its
> life, its cycle, and then another flow will remember it and
> perhaps probably consider these reports as having had an influence
> on its past, where in fact it only had a superficial influence on
> its past, since the main flow is the main flow. So, tell me what
> you think about all that.

No ruling yet — the psyche asked the flow for its assessment.

## 2026-08-22 — the strata; the subflow's response is in the transcript; the prompt is the precious stratum

Context (agent, brief): continuing the same conversation, after the
flow proposed reports-only-when-addressed and reception logging. The
message opened with the request "remember bc05da32". Verbatim:

> Yeah, there's some interesting things you've raised here, and
> there's something I want to point out, which is that if an
> agent's, sorry, if a subflow's output is only its response back to
> the main flow or to its parent, that data still sits in the
> transcript file. So making the subflow write a report and then
> making the main flow read the report just seems like useless
> churn. We're not really worried about subflows spending a few more
> tokens, especially when we're talking about cheap models like
> Sonnet and Luna. What is really important is the main flow's
> context and implementation workflows being essentially
> well-informed, which should not depend on a bunch of reports that
> subagents wrote, because the conceptualization of what the subflow
> really ought to do, that liability really falls on the main flow,
> because the main flow is what interacts with the living psyche, or
> it's as close as it gets. So if anything, if an implementing
> subflow must be given data, must be given the full response of a
> previous subflow, what really is the cost? What is really the
> extra cost? And let's say we produce a simple tool designed
> specifically for this, and I think we already have something that
> falls within that sort of use case that would allow... Because
> see, the problem with... It's the strata. The problem is the
> strata. If we make some... If we judge something to be important
> for an implementation subflow, and we tell that subflow to read
> that using tool calls, then we're putting that information, which
> is supposedly important, at the bottom stratum. And the only way
> to put information in its mid-stratum is bypassing its prompt, so
> essentially for the main flow to give it to it. Until we have a
> more advanced meta-harness that can do really cool stuff, like
> fetch a bunch of responses from a bunch of previous flows as the
> prompt, or perhaps even after editing it through another flow,
> passing that as a prompt to yet another flow, until we have that,
> we essentially have to depend on the current infrastructure, which
> is that the most useful and precious context is only that which
> the parent flow gives it as its starting prompt. And in the case
> of Claude, and I think this has actually... We could even have a
> whole conversation about that, but I think that a big reason why
> Claude has some people who are pretty adamant about the fact that
> it's more capable of understanding them is because Claude
> apparently, and I've had a few flows actually look into this, but
> maybe this information isn't actually accurate, but apparently,
> Codex does not load skills that are loaded by the model itself in
> the mid-stratum, and only Claude does. So that is maybe, if that
> is true about Claude, that is just one more way and another reason
> why skills are so important. But besides that, as well as the
> entry files, of course, but besides that, yeah, the most powerful
> part of the context for a subflow is going to be its initial
> prompt. So it's going to have to come directly from the parent. So
> these files are actually, because they're files and because we
> don't have a proper way to load them into the more valuable part,
> into the more valuable stratum, have a lower value, if you
> understand what I'm saying.

Note (agent): the Claude/Codex skill-loading difference is flagged
by the psyche as possibly inaccurate — a claim to verify, not
ground.
