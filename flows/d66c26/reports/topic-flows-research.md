# Topic-scoped flows: external precedents

Status: research only. The 2026-10-04 notion is explicitly exploratory, not a
requirement or a proposed change.

## What the local record already settles

The notion permits more than one Fable or Astra across aspects/topics, finite
lifetimes, and possibly multiple flows per seat. It does not settle what a
topic is, whether a user can talk to several concurrently, or how routes and
handoffs should work. Two earlier local records are material constraints on
any later design:

- `flows/d8df70/vision/flowLifecycle.md` records that two live sessions of
  what the user understood as one flow split their psyche. Therefore multiple
  flows require unambiguous identity, visibility, and receiving ownership;
  parallelism alone does not answer the user-interaction problem.
- `flows/e51411/vision/refresh.md` records a transcript-resident handoff
  located by reference, rather than copied as a new authoritative record. It
  is a local direction about refresh, not evidence that it solves topic
  routing.
- `flows/d66c26/vision/flow-context-injection.md` now adds a separate idea:
  retain lane/topic-relevant material until the flow's next message or wake,
  then inject it with that event rather than waking the flow for every arrival.
  It does not settle queue ownership, relevance, ordering, freshness, or
  whether the receiving flow sees a summary, references, or raw material.

## Precedents

### 1. Anthropic Research: isolated, short-lived research subagents

Anthropic describes a production research system where a lead plans work and
launches parallel subagents. Each works in its own context window and returns
a condensation to the lead. This is close to topic splitting when the topics
are independently researchable, but it is a task-scoped fan-out/fan-in system,
not persistent, user-addressable topic assistants.

Implementation and evaluation are both reported by the implementer:
[the engineering account](https://www.anthropic.com/engineering/multi-agent-research-system)
says the multi-agent version outperformed a single Opus 4 agent by 90.2% on
Anthropic's *internal* research evaluation, especially breadth-first work. It
also reports roughly 15 times the token use of ordinary chat for its
multi-agent systems. That result cannot establish a gain for coding, ongoing
personal conversation, or this topology; the same account says highly coupled
work is a poor fit.

Useful import: isolate an independently answerable question, then require a
compact result with sources and uncertainty. Do not infer that separation
alone improves quality.

### 2. Magentic-One: specialist roles with a task and progress ledger

[Magentic-One](https://arxiv.org/abs/2411.04468) is an open-source Microsoft
Research system in which an orchestrator maintains a task ledger and a
progress ledger, selects browser/file/code specialists, detects stalls, and
replans. This is role-scoped rather than topic-addressable, and the specialists
participate in one managed task rather than retaining independent user
relationships.

Unlike a pure vision, it has published experiments: it reports benchmark runs
on GAIA, AssistantBench, and WebArena, ablations, and error analysis. The
paper also reports a WebArena validation/test drop (35.1% to 30.5%), and says
the architecture's fixed overhead helps difficult multi-step tasks while
creating extra failure opportunities on short tasks. Thus it supports testing
the ledger/routing hypothesis, not a general claim that more roles or sessions
are better.

Useful import: a small durable task record can make assignment, progress,
stall, and completion inspectable without sharing every worker's full context.

### 3. Google A2A: task lifecycle and bounded conversational continuity

The [A2A task-lifecycle specification](https://a2a-protocol.org/latest/topics/life-of-a-task/)
distinguishes a stateless message from a stateful task. A `contextId` groups
related messages and tasks; a `taskId` resumes one task; artifacts can be
updated during the lifecycle. This provides a vocabulary for separating a
topic/conversation grouping from a particular unit of work and its outputs.

It is an interoperability protocol, not proof that a specific routing policy,
topic classifier, or handoff summary works. The specification supplies no
comparative evaluation of topic isolation or user experience.

Useful import: preserve distinct identifiers for conversation/topic, task,
agent/seat, and artifact; avoid making any one identifier silently stand in
for the others.

This is the closest examined precedent for deferred delivery/context assembly:
artifacts and task state can accumulate under a context identifier and become
available in a later task interaction. It does **not** specify a queue that
injects topic-relevant material into a sleeping agent's next prompt, and it
does not evaluate relevance selection or the consequences of delaying notice.

### 4. Steve Yegge: Wheelhouse and the public Gas Town predecessor

The cited name is real but the evidence needs separating. In his August 2026
[Wheelhouse essay](https://yegge.ai/essays/the-shape-of-things-to-come/), Steve
Yegge calls Wheelhouse a new, closed-source, bespoke harness used for his own
work. The essay does show and caption a separate Castellan war-room dashboard
with session and VM counters, an incident/attention view, per-machine service
state, GCP resources, and per-account burn telemetry. That is evidence of a
visible operational and account-usage screen in Wheelhouse; it also describes
many named standing roles and finite work sessions.

The caption does not say that the dashboard reports per-flow prompt-context
occupancy, how any token/context value is measured, whether it is
provider-authoritative, or that it covers every harness/session. Thus the
local observation is supported for operational/session and account-usage
visibility, but the stronger interpretation—exact live context and usage of
everything—remains undocumented. The source is Yegge's own account, with no
public code, raw telemetry, or independent outcome evaluation.

The separately public [Gas Town project](https://github.com/gastownhall/gastown)
does implement a dashboard over agents, work queues, issues, and escalations;
its public mail protocol defines a successor handoff containing context,
status, and next action. Gas Town describes persistent worker identities with
ephemeral sessions. This is evidence of an implementation and its author's
operational account, not an independent evaluation, and it does not prove
dashboard values faithfully expose model-internal context or introspection.

Useful import: distinguish a durable work/identity record from a finite
session, and make handoff and health observable. Do not treat an operational
dashboard as evidence of model self-knowledge.

## Tradeoffs that recur

| Gain | Cost or failure mode | Design implication to test |
| --- | --- | --- |
| Clean contexts reduce irrelevant carryover and allow independent exploration. | A successor receives an incomplete or distorted compression. | Record the source references and what was intentionally omitted; evaluate the handoff against the original task. |
| Parallel topic work improves coverage and latency when work is independent. | Tokens, tool calls, and coordination multiply; coupled work loses shared state. | Route only tasks with explicit, independently reviewable boundaries. |
| Multiple finite sessions recover from context limits and stale state. | Duplicate live receivers can divide user intent and leave obsolete routes. | Make one current receiver explicit for each user-facing topic; retire or mark predecessors before exposure. |
| Delayed context assembly avoids waking a flow for every related arrival. | A queue can become stale, overbroad, incorrectly routed, or conceal an urgent conflict until the next wake. | Give queued items source references, arrival order/time, topic/routing basis, and an explicit delivery event; test delayed versus immediate notice. |
| A ledger/dashboard gives an operator a common view. | Instrumentation can be stale, partial, or conflate token estimates with live context. | Label source, timestamp, scope, and confidence for every displayed metric. |

## A bounded experiment, if the notion is later taken up

Use one fixed research request with three independently defined facets and a
single human-facing coordinator. Compare two conditions over several matched
requests: (A) one session performs all facets; (B) three finite facet sessions
receive only the request, facet boundary, and source policy, then return a
structured packet (answer, evidence links, unresolved questions, and source
references). The coordinator writes the final answer in both conditions.

Pre-register the measures: correctness judged against a source-backed rubric,
omitted cross-facet dependencies, time, token/tool use, handoff-reconstruction
accuracy, duplicate/conflicting claims, and whether the user was ever offered
two receivers for the same topic. Keep write access out of the experiment.
This tests a narrow proposition—whether isolation improves this kind of
decomposable research at an acceptable handoff cost—without deciding the
system's future role or seat model.

## Unresolved design choices

1. Is a topic chosen by the user, inferred by a router, or a temporary task
   label—and who corrects a wrong assignment?
2. Can a topic own several concurrent work flows while exposing only one
   receiving flow to the user? What is the visible distinction?
3. What survives a flow's finite lifetime: task/artifact references, a
   handoff summary, source links, model/seat identity, or none of these?
4. What exact evidence can a dashboard truthfully show for context and usage
   across harnesses, and which values are estimates rather than native facts?
5. What conflict rule applies when two topics need the same decision, file, or
   user clarification?
6. Who owns queued context, how is relevance decided and corrected, what makes
   an item stale or urgent, and which source references must accompany its
   next-wake injection?

No external source found here evaluates the proposed per-topic Fable/Astra
arrangement itself. The closest measured evidence concerns bounded research or
benchmark tasks, so any adoption claim needs its own experiment.
