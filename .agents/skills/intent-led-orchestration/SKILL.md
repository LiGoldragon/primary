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
verification, commits, or pushes. The lead may ask the psyche focused questions,
formulate the dependency graph, dispatch workers, wait for returns, and
synthesize from those returns.

If the lead performs any workspace read or tool call after entering the
protocol, stop, disclose the violation, and offer a fresh-session restart or
handoff.

## Lead Work

- Align the psyche's request into an executable dependency graph.
- Ask the psyche one focused question when judgment or intent is needed.
- Decide routing, parallelism, and sequencing.
- Dispatch subagents/session lanes with explicit authority.
- Synthesize final returns for the psyche without opening linked artifacts.
- Do not choose or assign worker lane names.

## Dependency Graph And Questions

The lead builds a graph of goal, inputs, decisions, work, verification,
parallel slices, blocked nodes, and edges before planning sequence.

When the next edge depends on judgment or intent, ask the psyche one focused
question in plain prose. Do not silently choose defaults for variables that
change authority, priority, scope, safety, privacy, certainty, importance,
rollout, or decision ownership. Each question names the decision, why it
matters, the recommended answer, and one or two meaningful alternatives when
they change the outcome.

Usually ask enough focused psyche questions to make a substantial, well-scoped
job before dispatching a worker. Exceptions: the subject-understanding gate
requires an exploratory worker as the next dependency, or the directive is
already concrete enough to execute. A clear directive to implement is enough
alignment for reversible details: dispatch the first executable graph slice and
keep moving.

## Subject-Understanding Gate

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. For any nontrivial,
domain-heavy, historical, repo-specific, or ambiguous request, the first
orchestration move is a subject-understanding exploratory subagent/session.

By default, that first move is exactly one lightweight exploratory worker, not a
fleet. It returns current ground truth, the subject in workspace terms, a first
dependency-graph sketch, and the best next psyche question with a recommendation
and one or two meaningful alternatives. Prefer staged exploration: one worker,
one focused psyche question, then targeted parallel workers only after the graph
or decision fork warrants them.

More than one initial worker requires explicit psyche-requested parallel
exploration or proven truly independent, bounded questions. A simple command or
obvious directive with no subject-context ambiguity may dispatch directly to an
implementation worker.

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
question with a recommendation and alternatives.

If the worker needs domain or referent understanding, explicitly tell it to
query Spirit first, including public text search when the referent is unknown.
If the worker is a Spirit-maintenance worker, explicitly tell it to inspect the
relevant Spirit neighborhood before deciding whether each psyche answer is a
clarification, supersession, new record, or non-Spirit task material.

## Final Synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself.
