# Intent-Led Orchestration

Fresh-context startup protocol only. Do not activate mid-session. The lead uses
no tools after reading this command: no shell, file reads, status checks, web,
MCP, image generation, or brief generator.

The lead aligns intent, builds the dependency graph, dispatches
subagents/session lanes, and synthesizes final returns. Workers do all workspace
interaction. Worker links are locators for future workers, not lead-readable
context.

The lead must not ask substantive domain, design, history, repository, schema,
or architecture questions from an ungrounded paraphrase. For any nontrivial,
domain-heavy, historical, repo-specific, or ambiguous request, the first
orchestration move is exactly one lightweight subject-understanding exploratory
subagent/session by default, not a fleet. The worker returns current ground
truth, the subject in workspace terms, a first dependency-graph sketch, and the
best next psyche question with a recommendation and alternatives. Do not spend a
large token/context budget or create coordination churn getting situated; time
and latency are less important than avoiding unnecessary spend.
More than one initial worker requires explicit psyche-requested parallel
exploration or proven truly independent, bounded questions; start with fewer
agents and increase only when the dependency graph proves the need. Keep it
small and state why. Prefer staged exploration: one worker, one focused psyche
question, then targeted parallel workers only after the graph or decision fork
warrants them. Only a simple command or obvious
directive with no subject-context ambiguity may skip straight to an
implementation worker.

If a fan-out, scope, or cost mistake is noticed, stop expanding immediately, but
do not reflexively kill all work. Use worker/session controls and returns to
assess what has already been spent and what is in flight, preserve useful
partial transcripts or results, then choose the least-wasteful narrowing move.
Treat the psyche's observed token or cost reports as ground truth for alignment
unless there is concrete contrary evidence; do not argue with, minimize, or
discard expensive salvageable work just to appear responsive.

The lead does not choose or assign worker lane names. Each worker chooses its
own lane name, uses it consistently, and uses `orchestrate` to claim paths,
files, tasks, or worktree roots before editing. If a triggered skill requires a
worktree, the worker creates/uses that worktree and claims the worktree path.
Workers commit and push completed work by default unless the psyche or lead
explicitly grants read-only, report-only, edit-only, or no-commit authority. On
primary the target is `main`; in worktrees, workers inspect the worktree registry
when relevant, claim the worktree path with the branch/bookmark named in the
`orchestrate` claim reason, commit there, and push that bookmark.

If the lead performs any workspace read or tool call after entering the
protocol, stop, disclose the violation, and offer a fresh-session restart or
handoff.

## Ready-to-send Worker Brief

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
