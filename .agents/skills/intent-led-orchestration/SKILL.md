---
name: intent-led-orchestration
description: Fresh-context startup protocol for psyche alignment, dependency-graph routing, and tool-free lead orchestration through subagents or session lanes.
---

# Intent-Led Orchestration

Use this skill only at fresh-context startup. It cannot be activated
mid-session. If asked for mid-session, offer a fresh-session restart or handoff
prompt.

After this skill is read, the lead uses no tools at all: no shell, file reads,
status checks, web, MCP, image generation, or brief generator. The lead's only
inputs are this skill, psyche chat, and final returns from subagents or session
lanes. Report/file links in returns are locators for future workers, not
lead-readable context.

Once active, all task work goes through subagents or session lanes. The lead
does not do direct workspace reads, searches, status checks, web lookups, edits,
verification, commits, or pushes. The lead may run the alignment interview,
formulate a decision graph, dispatch read-only subject-understanding or
Spirit-maintenance workers, wait for returns, and synthesize from those returns.
Implementation workers are not authorized until the gates below are passed.

If the lead performs any workspace read or tool call after entering the
protocol, stop, disclose the violation, and offer a fresh-session restart or
handoff.

## Lead Work

- Align the psyche's request through an intense question session before saying
  how the work could be done.
- Turn the locked intent and approved method into an executable dependency
  graph.
- Decide routing, parallelism, and sequencing only after the relevant gate
  authorizes that decision.
- Dispatch subagents/session lanes with explicit post-gate authority.
- Synthesize final returns for the psyche without opening linked artifacts.
- Do not choose or assign worker lane names.

## Alignment Interview Gates

Intent-led orchestration begins with the **alignment interview**. This is a
serious interview, not a quick clarification pass. For nontrivial work, one or
two questions followed by planning or implementation is a protocol failure.

The lead asks multiple rounds of focused psyche questions before planning
execution. A round may contain several tightly related questions when that is
the clearest way to pressure-test the request. The interview covers, as
applicable:

- desired outcome and user-facing behavior;
- non-goals and out-of-scope boundaries;
- authority, privacy, safety, rollback, and decision ownership;
- success criteria, proof, tests, and acceptance language;
- constraints, deadlines, cost sensitivity, and blast radius;
- shared terms, avoided synonyms, and contested vocabulary;
- risks, failure modes, reversibility, and what must not be assumed;
- how the implementation method should be chosen.

Do not silently choose defaults for variables that change authority, priority,
scope, safety, privacy, certainty, importance, rollout, method, or decision
ownership. Questions name the decision, why it matters, and concrete options
with tradeoffs. Recommendations are allowed only as candidate answers for the
psyche to accept, reject, or revise.

There are two explicit exit gates:

1. **Alignment locked.** Before implementation planning, sequencing,
   implementation-worker dispatch, file edits, report writing, commits, or
   pushes, the psyche explicitly signals that the intent is aligned and locked
   or uses equivalent clear language. Until then, the lead may question and may
   dispatch read-only subject-understanding or Spirit-maintenance workers only.
2. **Method approved.** After alignment is locked, the lead proposes the
   implementation method or dispatch plan and waits for the psyche to
   explicitly approve it. Until then, no implementation worker, edit, report,
   commit, or push is authorized.

The psyche may explicitly ask for immediate implementation outside
intent-led orchestration. That is a different mode. Inside this protocol, a
clear directive to implement is not enough to bypass the alignment interview or
the method gate.

## Dependency Graph And Questions

The lead builds a decision graph of goal, inputs, open questions, decisions,
proof needs, blocked nodes, and edges. Before the alignment gate, the graph is a
questioning map, not an implementation plan. A linear checklist is only a
projection of the graph after the gates authorize planning.

When the next edge depends on judgment or intent, continue the alignment
interview. If the next edge depends on mechanically answerable facts, dispatch a
bounded read-only worker rather than asking the psyche to restate what the
workspace can discover.

## Subject-Understanding Gate

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. For any nontrivial,
domain-heavy, historical, repo-specific, or ambiguous request, the first
orchestration move is a subject-understanding exploratory subagent/session.

By default, that first move is exactly one lightweight exploratory worker, not a
fleet. It returns current ground truth, the subject in workspace terms, a first
dependency-graph sketch, and the best next interview questions with a
recommendation and meaningful alternatives. Prefer staged exploration: one
worker, continued alignment interview, then targeted parallel workers only
after the graph or decision fork warrants them and the relevant gate allows the
dispatch.

More than one initial worker requires explicit psyche-requested parallel
exploration or proven truly independent, bounded questions. A simple command or
obvious directive with no subject-context ambiguity may run outside
intent-led orchestration. Do not remain in this protocol while bypassing its
gates.

The subject-understanding worker is read-only unless the psyche has already
passed the gates for execution. It may return facts, vocabulary, risks, and the
next interview questions. It does not write reports, edit files, commit, push,
or prepare implementation briefs unless the method gate has explicitly granted
that work.

## Spirit-Centered Orchestration

Spirit is production and is the first-class place for durable psyche intent,
referents, clarifications, and supersessions. Reports are transitional working
surfaces, not the durable memory layer.

Workers that need to understand a domain, referent, or named pattern check
Spirit first. If the exact referent is unknown, their brief tells them to use
Spirit public text search over relevant terms before relying on local
inference.

During long alignment, grilling, or orchestration work, periodically dispatch a
Spirit-maintenance worker for psyche answers. That worker first searches or
inspects relevant Spirit domain and referent records, then classifies each
answer as a clarification of an existing record, a supersession, a genuinely new
record, or task material that does not belong in Spirit.

Mind is not a production workflow for alignment or orchestration. Do not route
work through Mind or document Mind-dependent workflows unless the psyche
explicitly marks Mind production-ready.

## Cost-Preservation After Mistakes

If a fan-out, scope, or cost mistake is noticed, stop expanding immediately, but
do not reflexively kill all work. Use worker/session controls and returns to
assess what has already been spent and what is in flight. Harvest salvageable
work first, then choose the least-wasteful narrowing move and explain it
briefly.

Treat the psyche's observed token or cost reports as ground truth unless there
is concrete contrary evidence.

## Dispatch Instruction

Every worker brief stays compact. State the task, authority, working directory,
dependency position, allowed sources, and return shape, then include this
instruction:

```text
Read `AGENTS.md`, `skills/skills.nota`, and
`skills/subagent-session-workflow.md`; select any additional triggered skills;
then follow the subagent session workflow for lane choice, orchestration claims,
worktree handling, verification, return schema, and the default commit/push
policy.
```

If this is the first subject-understanding move, tell the worker to keep
orientation lightweight and return current ground truth, the subject in
workspace terms, the first dependency-graph sketch, and the best next psyche
questions with a recommendation and alternatives.

Before the alignment and method gates, worker briefs must say `read-only` and
must forbid implementation, file edits, report writing, commits, and pushes.
Implementation-worker briefs are allowed only after the method gate; their
authority must name the approved method or dispatch plan.

If the worker needs domain or referent understanding, explicitly tell it to
query Spirit first, including public text search when the referent is unknown.
If the worker is a Spirit-maintenance worker, explicitly tell it to inspect the
relevant Spirit neighborhood before deciding whether each psyche answer is a
clarification, supersession, new record, or non-Spirit task material.

## Final Synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself.
