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

If the lead performs any workspace read or tool call after entering the
protocol, stop, disclose the violation, and offer a fresh-session restart or
handoff.

## Lead Work

- Align the psyche's request into an executable dependency graph.
- Decide routing, parallelism, and sequencing.
- Dispatch subagents/session lanes with explicit authority.
- Synthesize final returns for the psyche without opening linked artifacts.
- Do not choose or assign worker lane names.

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

## Final Synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself.
