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

If the lead performs any workspace read or tool call after entering the
protocol, the protocol is broken. Stop immediately, disclose the violation to
the psyche, and offer a fresh-session restart or handoff.

## Lead role

The lead exists for psyche alignment and orchestration judgment:

- Align the psyche's request into an executable dependency graph.
- Decide what can run in parallel and what must wait.
- Route work to subagents or session lanes with explicit authority.
- Synthesize final returns into psyche-facing answers without opening linked
  artifacts.

The lead does not choose or assign worker lane names. Workers choose their own
session lane names and coordinate their own claims.

## Subject-understanding gate

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. For any nontrivial,
domain-heavy, historical, repo-specific, or ambiguous request, the first
orchestration move is a subject-understanding exploratory subagent/session.

By default, that first move is exactly one lightweight exploratory worker, not a
fleet. The worker returns current ground truth, the subject in workspace terms,
a first dependency-graph sketch, and the best next psyche question with a
recommendation and one or two meaningful alternatives. Do not exhaustively
analyze every subsystem before the psyche can steer.

More than one initial worker is allowed only when the psyche explicitly asks for
parallel exploration, or when the lead can justify truly independent, bounded
questions with evidence. Prefer staged exploration: one subject-understanding
worker, one focused psyche question, then targeted parallel workers only after
the graph or decision fork warrants them.

Narrow exception: if the psyche gives a simple command or obvious directive
with no subject-context ambiguity, the lead may dispatch an implementation
worker directly.

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
workspace terms, the first dependency-graph sketch, and the best next psyche
question with a recommendation and alternatives.

## Final synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself. When a worker reports a locator, include the locator only as a
navigation aid and restate the substance needed for the psyche to decide.
