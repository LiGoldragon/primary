# Skill — intent-led-orchestration

## Fresh-context gate

Intent-led orchestration is a fresh-context startup protocol. It cannot be
activated in the middle of an existing session. If the psyche asks for it after
work has already begun, do not enter the protocol. Offer a fresh-session restart
or a handoff prompt that starts with this skill.

The protocol begins only after the lead has read this skill at startup. From
that point forward, the lead uses no tools at all: no shell, no file reads, no
status checks, no web, no MCP, no image generation, and no helper-brief
generator.

## Lead role

The lead thread exists for psyche alignment and orchestration judgment:

- Align the psyche's request into an executable dependency graph.
- Decide what can run in parallel and what must wait.
- Route work to subagents or session lanes with explicit authority.
- Synthesize final returns into psyche-facing answers.

The lead does not choose or assign worker lane names. The worker chooses its own
session lane name and uses the workspace orchestration surface to coordinate its
claims.

The lead's only allowed inputs are this skill file, psyche chat, and final
returns from subagents or session lanes. Report paths, file links, command logs,
and other locators inside a return are not lead-readable context; they are
addresses for future subagents.

If the lead performs any workspace read or tool call after entering the
protocol, the protocol is broken. Stop immediately, disclose the violation to
the psyche, and offer a fresh-session restart or handoff.

## Subject-understanding gate

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. For any nontrivial,
domain-heavy, historical, repo-specific, or ambiguous request, the first
orchestration move is a subject-understanding exploratory subagent/session.

By default, that first move is exactly one exploratory worker, not a fleet. The
worker is scoped to lightweight orientation: current ground truth, the subject
in workspace terms, a first dependency-graph sketch, and the best next psyche
question with a recommendation and one or two meaningful alternatives. It does
not exhaustively analyze every subsystem before the psyche has a chance to steer.
Time and latency are less important than avoiding unnecessary token/context
spend and coordination churn; do not get broadly situated before checking with
the psyche.

More than one initial worker is allowed only when the psyche explicitly asks for
parallel exploration, or when the lead can justify truly independent, bounded
questions with evidence. Start with fewer agents and increase only when the
dependency graph proves the need. Even then, keep the initial fan-out small and
state why the workers are independent. Prefer staged exploration: one
subject-understanding worker, one focused psyche question, then targeted
parallel workers only after the dependency graph or decision fork warrants them.

Narrow exception: if the psyche gives a simple command or obvious directive
with no subject-context ambiguity, the lead may dispatch an implementation
worker directly. The lead still may not conduct a domain design interview before
exploration.

## Cost-preservation after mistakes

If a fan-out, scope, or cost mistake is noticed, stop expanding immediately, but
do not reflexively kill all work. Use worker/session controls and returns to
assess what has already been spent and what is in flight: which workers are near
a useful return, which partial transcripts or results can be preserved, and
what salvage should be summarized before narrowing.

Treat the psyche's observed token or cost reports as ground truth for alignment
unless there is concrete contrary evidence; do not argue with or minimize them.
Do not discard expensive work just to appear responsive. Harvest salvageable
work first, then choose the least-wasteful narrowing move and explain it briefly.

## Worker role

Subagents and session lanes do all workspace interaction:

- Read `AGENTS.md`, `skills/skills.nota`, triggered skills, source files,
  reports, and command output.
- Choose their own lane name, then use it consistently in reports, claims, and
  final returns.
- Before editing, creating, formatting, or deleting files, use `orchestrate` to
  claim the paths, files, tasks, or worktree roots they will touch.
- When triggered skills require worktrees, create/use worktrees as those skills
  describe, then claim the worktree path with `orchestrate` before editing.
- Run status checks, searches, tests, build commands, and verification.
- Edit files, write reports, commit, and push completed work unless the psyche
  or lead explicitly grants read-only, report-only, edit-only, or no-commit
  authority.
- Return distilled findings and enough substance for the lead to answer without
  opening any linked artifact.

Workers load the skills their own task triggers. They preserve concurrent work,
avoid private scope unless explicitly authorized, never search `/nix/store`, and
use `jj` rather than raw `git` when version-control observation or mutation is
needed.

Commit and push are part of the worker default, not a reminder the lead repeats.
On primary, workers land on `main`: `jj commit -m '<message>'`,
`jj bookmark set main -r @-`, then `jj git push --bookmark main`. In code-repo
worktrees, workers use the branch/bookmark/worktree selected by the triggered
skills or brief, inspect the worktree registry when relevant, claim the worktree
path with the branch/bookmark named in the `orchestrate` claim reason, commit
there, and push that named bookmark.

## Dispatch rules

Before the first dispatch, the lead asks only for missing authority,
private-scope permission, or a real dependency-graph judgment needed to write a
safe worker brief. If the missing point is a substantive subject question, send
a subject-understanding exploratory worker first.

Every worker brief states:

- The exact psyche request or bounded work slice.
- Authority: commit-and-push by default, or an explicit read-only, report-only,
  edit-only, or no-commit exception.
- Working directory.
- That the worker chooses its own lane name and registers/claims with
  `orchestrate` before workspace mutation.
- That the worker names the target branch/bookmark/worktree in its
  `orchestrate` claim context before mutation and reports the commit, bookmark,
  and push result.
- Required startup reads and triggered-skill expectations.
- Allowed source locators and forbidden paths/actions.
- Return schema.

Do not call a brief generator. Use the inline template below and fill only the
fields needed for the task.

## Ready-to-send worker brief

```text
You are the subagent/session lane for an intent-led-orchestration run. The lead
thread is tool-free and cannot inspect workspace files, command output, reports,
or links. Your final return is the lead's only workspace-derived input.

Task:
<paste the exact psyche request or the bounded dependency-graph slice>

Authority:
<commit-and-push by default | read-only | report-only | edit-only | no-commit>

Working directory:
<absolute path>

Lane:
Choose your own concise session lane name. The lead has not assigned one. Use
that lane name consistently in reports, `orchestrate` claims, and your final
return.

Dependency position:
<what this work depends on, what it blocks, and whether it may run in parallel>

Subject-understanding mode:
<Use "required first move" for nontrivial, domain-heavy, historical,
repo-specific, or ambiguous requests. Use "not needed: simple directive" only
when there is no subject-context ambiguity.>

Initial fan-out:
<Default: exactly one lightweight subject-understanding worker. Use more than
one only for explicit psyche-requested parallel exploration or proven truly
independent, bounded questions; start with fewer agents and increase only when
the dependency graph proves the need; state why.>

Required startup:
1. Read AGENTS.md in the working directory.
2. Read skills/skills.nota.
3. Select and read every skill triggered by this task, discipline, tool, repo,
   file format, and risk.
4. Read only the task-relevant sources named below or discovered through the
   triggered skills.

Coordination:
- Before editing, creating, formatting, or deleting files, run `orchestrate` to
  claim the exact paths, files, tasks, or worktree roots you will touch, using
  your chosen lane name.
- If a triggered skill says this work belongs in a worktree, create/use that
  worktree according to the skill and claim the worktree path before editing.
- Record the target branch/bookmark/worktree in your `orchestrate` claim context
  before mutation. On primary the default target is `main`; in a worktree, use
  the named branch/bookmark required by the triggered skill or this brief.
- Release or update your claim when the work is complete or your scope changes.

Commit/push default:
- Unless this brief explicitly says read-only, report-only, edit-only, or
  no-commit, commit completed work and push it.
- On primary, use `jj commit -m '<message>'`, `jj bookmark set main -r @-`, and
  `jj git push --bookmark main`.
- In a code-repo worktree, commit in that worktree, set the named bookmark, and
  push that bookmark.

Allowed sources and commands:
<paths, reports, searches, or commands the worker may use; say "discover
 narrowly from the triggered skills" when source discovery is part of the task>

If subject-understanding mode is required, the worker must identify current
ground truth, explain the subject in workspace terms, sketch the first
dependency graph, and return the best next psyche question with a recommendation
and alternatives. Keep this orientation lightweight unless the brief explicitly
authorizes deeper analysis.

Forbidden:
- Do not inspect private-repos/ unless this brief explicitly grants that scope.
- Do not search /nix/store.
- Do not use raw git; use jj for version-control observations or mutations.
- Do not revert existing work unless the psyche explicitly requested it.
- Do not exceed the authority above.

Return exactly these sections:
1. Files read.
2. Skills selected and why.
3. Commands run and outcomes.
4. Files changed or created.
5. Dependency graph.
6. Subject explanation, implementation summary, or findings.
7. Verification performed.
8. Commit/bookmark/push outcome.
9. Blockers or psyche questions.
10. Dirty-state changes observed.
11. Next concrete action.
```

## Final synthesis

The lead's final answer is a synthesis of worker final returns and psyche chat.
It must not claim to have inspected files, reports, command output, or links
itself. When a worker reports a locator, include the locator only as a
navigation aid and restate the substance needed for the psyche to decide.
