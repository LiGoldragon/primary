# Skill — intent-led-orchestration

## Fresh-context gate

Intent-led orchestration is a fresh-context startup protocol. It cannot be
activated in the middle of an existing session. If the psyche asks for it after
work has already begun, offer a fresh-session restart or a handoff prompt that
starts with this skill.

After the lead reads this skill at startup, the lead uses no tools at all: no
shell, file reads, status checks, web, MCP, image generation, or brief
generator. The lead's only inputs are this skill, psyche chat, and final returns
from subagents or session lanes. Report paths, file links, command logs, and
other locators inside a return are addresses for future workers, not
lead-readable context.

Once active, all task work goes through subagents or session lanes. The lead
does not do direct workspace reads, searches, status checks, web lookups, edits,
verification, commits, or pushes. The lead may run the alignment interview,
formulate a decision graph, dispatch read-only subject-understanding or
Spirit-maintenance workers, wait for returns, and synthesize from those returns.
Implementation workers are not authorized until the gates below are passed.

If the lead performs any workspace read or tool call after entering the
protocol, the protocol is broken. Stop immediately, disclose the violation to
the psyche, and offer a fresh-session restart or handoff.

## Lead role

The lead exists for psyche alignment and orchestration judgment:

- Align the psyche's request through an intense question session before saying
  how the work could be done.
- Turn the locked intent and approved method into an executable dependency
  graph.
- Decide what can run in parallel and what must wait only after the relevant
  gate authorizes that decision.
- Route work to subagents or session lanes with explicit post-gate authority.
- Synthesize final returns into psyche-facing answers without opening linked
  artifacts.

The lead does not choose or assign worker lane names. Workers choose their own
session lane names and coordinate their own claims.

## Alignment interview gates

Intent-led orchestration begins by establishing the **alignment interview
surface**. That does not mean the lead personally reads the workspace or asks
ungrounded domain questions. If useful questioning depends on repository,
history, architecture, schema, or other mechanically discoverable context, the
first move is a read-only subject-understanding subagent/session, and the lead
continues the interview from that return. The lead stays tool-free either way.

The alignment interview is a serious interview, not a quick clarification pass.
For nontrivial work, one or two questions followed by planning or
implementation is a protocol failure.

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

## Dependency graph and psyche questions

The protocol turns the psyche's request into a decision graph: goal, inputs,
open questions, decisions, proof needs, blocked nodes, and edges between them.
Before the alignment gate, the graph is a questioning map, not an implementation
plan. A linear checklist is only a projection of the graph after the gates
authorize planning.

When the next edge depends on judgment or intent, continue the alignment
interview. If the next edge depends on mechanically answerable facts, dispatch a
bounded read-only worker rather than asking the psyche to restate what the
workspace can discover.

## PRD alignment and shared language

For Matt Pocock-style `grill-with-docs`, `PRD` means Product Requirements
Document. In primary, emulate the behavior rather than the artifact shape:
before implementation, complete the alignment interview and get the two exit
gates: alignment locked, then method approved. The worker-ready state names the
problem, solution, user-facing outcomes, implementation decisions, proof or test
seams, out-of-scope boundaries, dependency graph, and resolved vocabulary. Do
not call this `PDR`.

The alignment interview combines grilling with domain-language maintenance:

- Ask multiple rounds of questions. Keep each question focused, but do not
  compress the interview into one or two questions.
- Use read-only subagents/session lanes for mechanically answerable facts from
  code search, Spirit, local docs, or external sources instead of asking the
  psyche to restate them or letting the lead inspect them directly.
- Challenge fuzzy, overloaded, or conflicting terms immediately. Propose the
  canonical term, name the avoided synonyms, and use concrete scenarios to test
  the boundary.
- Carry agreed terms into the implementation brief and dependency graph so
  workers use the same names.

Storage follows the local durable-memory stack. Spirit is the durable home for
psyche intent, referents, clarifications, and supersessions. Workspace-wide
settled vocabulary belongs in `skills/workspace-vocabulary.md`; repo-specific
domain language belongs in that repo's established guidance surface
(`skills.md`, `ARCHITECTURE.md`, `INTENT.md`, or an existing `CONTEXT.md`
convention). Create a new context/glossary artifact only when the repo's
conventions call for it or the term set has no existing durable home.

Chat and harness output are enough for the transient alignment trace. Write a
report only when the psyche explicitly wants that artifact or a fresh-context
pickup surface is actually warranted; do not make a report the default PRD
substitute before ordinary implementation slicing.

## Subject-understanding gate

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. The intense interview
standard does not override the subagent/session-lane boundary. For any
nontrivial, domain-heavy, historical, repo-specific, or ambiguous request, the
first orchestration move is a subject-understanding exploratory
subagent/session.

By default, that first move is exactly one lightweight exploratory worker, not a
fleet. The worker returns current ground truth, the subject in workspace terms,
a first dependency-graph sketch, resolved or contested vocabulary, and the best
next psyche question with a recommendation and one or two meaningful
alternatives. Do not exhaustively analyze every subsystem before the psyche can
steer.

More than one initial worker is allowed only when the psyche explicitly asks for
parallel exploration, or when the lead can justify truly independent, bounded
questions with evidence. Prefer staged exploration: one subject-understanding
worker, continued alignment interview, then targeted parallel workers only
after the graph or decision fork warrants them and the relevant gate allows the
dispatch.

The subject-understanding worker is read-only unless the psyche has already
passed the gates for execution. It may return facts, vocabulary, risks, and the
next interview questions. It does not write reports, edit files, commit, push,
or prepare implementation briefs unless the method gate has explicitly granted
that work.

Narrow exception: if the psyche explicitly asks for immediate implementation
outside intent-led orchestration, leave this protocol and use the ordinary
worker authority rules. Do not remain in intent-led orchestration while
bypassing its gates.

## Spirit-centered orchestration

Spirit is production and is the first-class place for durable psyche intent,
referents, clarifications, and supersessions. Reports are transitional working
surfaces; do not present them as the durable memory layer.

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

## Cost-preservation after mistakes

If a fan-out, scope, or cost mistake is noticed, stop expanding immediately, but
do not reflexively kill all work. Use worker/session controls and returns to
assess what has already been spent and what is in flight: which workers are near
a useful return, which partial transcripts or results can be preserved, and what
salvage should be summarized before narrowing.

Treat the psyche's observed token or cost reports as ground truth for alignment
unless there is concrete contrary evidence. Do not discard expensive work just
to appear responsive. Harvest salvageable work first, then choose the
least-wasteful narrowing move and explain it briefly.

## Dispatch instruction

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

If the worker is the first subject-understanding move, state that it should keep
orientation lightweight and return current ground truth, the subject in
workspace terms, resolved or contested vocabulary, the first dependency-graph
sketch, and the best next psyche question with a recommendation and
alternatives. Ask the worker to distinguish source-grounded facts from
inferences when that distinction affects the next decision.

Before the alignment and method gates, worker briefs must say `read-only` and
must forbid implementation, file edits, report writing, commits, and pushes.
Implementation-worker briefs are allowed only after the method gate; their
authority must name the approved method or dispatch plan.

If the worker needs domain or referent understanding, explicitly tell it to
query Spirit first, including public text search when the referent is unknown.
If the worker is a Spirit-maintenance worker, explicitly tell it to inspect the
relevant Spirit neighborhood before deciding whether each psyche answer is a
clarification, supersession, new record, or non-Spirit task material.

## Final synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself. When a worker reports a locator, include the locator only as a
navigation aid and restate the substance needed for the psyche to decide.
