---
title: 462 — Pocock project and session lifecycle
role: operator
variant: Research
date: 2026-06-24
topics: [psyche-alignment, session-management, external-workflow]
description: |
  Source-grounded extraction from Matt Pocock's public skills and Sandcastle
  repositories, focused on alignment interviews, fresh-context boundaries,
  issue/PRD lifecycle, session handling, cleanup, and fit with primary's
  lane/report/Spirit discipline.
---

# 462 — Pocock project and session lifecycle

## Sources Inspected

Primary local context:

- `/home/li/primary/ESSENCE.md`
- `/home/li/primary/INTENT.md`
- `/home/li/primary/orchestrate/AGENTS.md`
- `/home/li/primary/skills/role-lanes.md`
- `/home/li/primary/skills/reporting.md`
- `/home/li/primary/skills/alignment-interview.md`
- `/home/li/primary/reports/operator/461-Research-ai-coding-workflows-matt-pocock.md`

External sources cloned to scratch:

- `https://github.com/mattpocock/skills`, cloned at `/tmp/mattpocock-skills`
- `https://github.com/mattpocock/sandcastle`, cloned at `/tmp/mattpocock-sandcastle`

External source files with load-bearing details:

- `/tmp/mattpocock-skills/README.md`
- `/tmp/mattpocock-skills/skills/productivity/grill-me/SKILL.md`
- `/tmp/mattpocock-skills/skills/productivity/grilling/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/grill-with-docs/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/ask-matt/SKILL.md`
- `/tmp/mattpocock-skills/skills/productivity/handoff/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/to-prd/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/to-issues/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`
- `/tmp/mattpocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md`
- `/tmp/mattpocock-skills/skills/engineering/triage/SKILL.md`
- `/tmp/mattpocock-skills/.out-of-scope/question-limits.md`
- `/tmp/mattpocock-sandcastle/README.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0003-reuse-worktree-by-default.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0007-worktree-locking.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0011-resume-is-one-iteration.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0012-agent-provider-owned-session-storage.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0016-resume-requires-filesystem-backed-sessions.md`
- `/tmp/mattpocock-sandcastle/docs/adr/0018-fork-is-session-only.md`
- `/tmp/mattpocock-sandcastle/src/WorktreeManager.ts`
- `/tmp/mattpocock-sandcastle/src/SandboxFactory.ts`
- `/tmp/mattpocock-sandcastle/src/createWorktree.ts`
- `/tmp/mattpocock-sandcastle/src/createSandbox.ts`
- `/tmp/mattpocock-sandcastle/src/SessionStore.ts`
- `/tmp/mattpocock-sandcastle/src/templates/parallel-planner-with-review/main.mts`
- `/tmp/mattpocock-sandcastle/src/templates/parallel-planner-with-review/plan-prompt.md`
- `/tmp/mattpocock-sandcastle/src/templates/parallel-planner-with-review/implement-prompt.md`
- `/tmp/mattpocock-sandcastle/src/templates/parallel-planner-with-review/review-prompt.md`

## What The Public Project Actually Contains

There are two public parts.

`mattpocock/skills` is the workflow and instruction layer. Its README frames the main failure mode as agent-human misalignment and recommends a grilling session before each meaningful change. The current `/grill-me` file is intentionally only a wrapper: it says to run `/grilling`. The reusable `/grilling` skill carries the core mechanism: interview relentlessly, walk the design tree branch by branch, give a recommended answer for each question, ask one question at a time, and explore the codebase instead of asking when codebase inspection can answer the question. `/grill-with-docs` adds `/domain-modeling`, so the interview also updates project vocabulary and ADR-style decisions.

`mattpocock/sandcastle` is the orchestration/runtime layer. Its README defines Sandcastle as a TypeScript library for invoking agents through `run()`, creating isolated sandboxes, managing branch strategy, and merging commits back. It supports Docker, Podman, Vercel, and no-sandbox modes; one-shot `run()`; reusable `createSandbox()`; and first-class `createWorktree()`.

## Grill And Alignment Shape

The closest primary analogue is already `skills/alignment-interview.md`. Pocock's `/grilling` and primary's alignment interview agree on the important shape:

- one focused question per turn
- a recommended answer included with the question
- dependencies resolved in order
- codebase exploration used when it can answer the question
- stopping only when remaining questions no longer change the first useful slice

Differences matter. Pocock's public skill uses intentionally forceful language, does not itself distinguish durable intent from task state, and in `/grill-with-docs` writes domain docs/ADRs as part of the conversation. Primary must keep the Spirit gate in front: a grill answer is not automatically durable intent. It becomes Spirit only when it states a lasting Decision, Principle, Correction, Clarification, or Constraint; otherwise it is task state and belongs in a report, issue, or implementation brief.

For primary, the clean mapping is to keep `skills/alignment-interview.md` as the local grill shape, but borrow two Pocock details: make every question carry a concrete recommendation, and explicitly let the agent inspect code instead of asking the psyche questions whose answer is mechanically discoverable.

## Fresh Context Boundaries

The strongest source is `/tmp/mattpocock-skills/skills/engineering/ask-matt/SKILL.md`.

Pocock's main flow is:

1. `/grill-with-docs`
2. optional `/handoff` to a fresh prototype session and `/handoff` back
3. `/to-prd`
4. `/to-issues`
5. fresh implementation session per independent issue

The key boundary rule is not "clear often." It is phase-specific. Keep the grill, PRD, and issue breakdown in one unbroken context window so issue slicing inherits the same design conversation. Then clear context between implementation issues because each issue should be independently grabbable.

`/handoff` is explicitly a bridge between context windows: write a markdown summary to the OS temp directory, do not duplicate content already captured in PRDs, issues, commits, diffs, or ADRs, and reference those artifacts by path or URL. `/compact` is different: it stays in the same conversation and is suitable only at intentional phase breaks.

Primary already has a stronger durable surface than Pocock's temp handoff: reports. The mapped rule should be:

- grill/alignment transcript: task state unless durable intent is captured in Spirit
- handoff between windows: a report or assigned meta-report file, not a temp-only file
- implementation issue context: start fresh from repo `INTENT.md`, repo `AGENTS.md`, relevant report/design, and the single issue
- review context: start fresh and push the standards/report/issue into context

## Session Naming And Run Names

Pocock's skills do not impose session names for chat threads. Sandcastle does impose operational names in API calls: `name: "planner"`, `name: "implementer"`, `name: "reviewer"`, `name: "merger"`, and issue-derived branch names like `sandcastle/issue-{id}`. The template planner requires deterministic branch names so re-planning the same issue preserves accumulated progress.

Primary should not import Sandcastle branch names into primary itself. The useful mapping is conceptual:

- report meta-directory name is the durable session name
- sub-report slots are allocated before subagent launch
- lane lock path and report path are the primary coordination identity
- code repos may use branch/worktree names derived from issue identifiers, but primary reports stay on main

## PRD And Issue Lifecycle

`/to-prd` converts the already-aligned conversation into a PRD without further interview. It asks the agent to explore the repo if needed, sketch test seams, confirm seams with the user, then publish to the issue tracker. Its template includes problem statement, solution, user stories, implementation decisions, testing decisions, out-of-scope, and notes. It explicitly warns against specific file paths or code snippets except when prototype snippets encode a decision more precisely than prose.

`/to-issues` breaks a PRD or plan into tracer-bullet issues. Each issue should be a thin vertical slice through all integration layers, complete enough to demo or verify. The user reviews granularity, dependencies, and split/merge choices before publication. Published issue bodies contain parent, what to build, acceptance criteria, and blockers.

The setup skill supports GitHub, GitLab, local markdown under `.scratch/<feature>/`, and other trackers. The local markdown convention is one feature directory, `PRD.md`, numbered issue files under `issues/`, a `Status:` line, and comments appended at the bottom.

Primary mapping:

- PRD maps to a Research/Design/Proposal report or repo design surface, not to repo `INTENT.md`.
- Issues map to beads or whatever replaces beads, plus report-backed vertical slices when the slice needs design context.
- Pocock's local `.scratch/` issue store is close in spirit to primary reports, but primary already separates reports, Spirit, repo intent, and transitional beads. Do not add `.scratch/` as a parallel tracker inside primary unless the psyche asks.
- The vertical-slice discipline maps cleanly and should be preferred over horizontal "schema first/API second/UI third" plans, except where primary's schema-stack work intentionally requires contract-first sequencing.

## Archiving, Deletion, And Garbage Collection

Pocock's skills repo has a lifecycle warning rather than a full archival daemon. Report 461 captured the video's old-PRD warning: stale PRDs and plans left in the repo can mislead future agents. The public skills encode that indirectly by publishing PRDs/issues to an issue tracker and by making `/handoff` avoid duplicating material already captured elsewhere.

Sandcastle has concrete cleanup mechanics, but they are runtime cleanup, not product-plan archival:

- `createSandbox()` with `await using` calls `sandbox.close()` automatically.
- A clean worktree is removed; a dirty worktree is preserved and reported with review and cleanup instructions.
- `createWorktree().close()` likewise preserves dirty worktrees and removes clean ones.
- `WorktreeManager.pruneStale()` runs `git worktree prune` and removes orphaned directories under `.sandcastle/worktrees/`.
- ADR 0007 specifies file locks under `.sandcastle/locks/<name>.lock`, stale lock cleanup by dead PID, and no wait/retry on contention.
- Branch strategy reuse is explicit: existing managed worktrees are reused; clean ones may fast-forward from origin when safe; dirty or diverged ones are reused as-is with logging.

Primary already has the better archival discipline for planning artifacts: reports retire when their substance migrates to `INTENT.md`, `ARCHITECTURE.md`, skills, tests, or current reports; meta-report directories are garbage-collected as one session unit. Sandcastle's concrete cleanup behavior suggests one useful operational addition for any future primary session runner: cleanup should preserve dirty work and remove only clean generated worktrees/sandboxes, and stale locks should be machine-detectable rather than manually edited state.

## Resume, Fork, And Session Storage

Sandcastle treats model sessions as provider-owned artifacts. ADR 0012 says the agent provider owns session storage end to end because Claude, Codex, Pi, and other tools store and rewrite sessions differently. ADR 0016 narrows resumability to filesystem-backed sessions; database-only session state is not supported. `SessionStore.ts` implements provider-specific paths and cwd rewriting for Claude, Codex, and Pi.

ADR 0011 says `.resume()` is exactly one iteration. A resumed iteration produces a new session id, so multi-iteration resume would be ambiguous unless the caller explicitly chains resume calls.

ADR 0018 says `.fork()` isolates the agent session only, not the branch or sandbox. Safe concurrent fan-out still requires distinct branches; session forking alone does not protect shared git state.

Primary mapping:

- This validates primary's existing fresh-context preference: resuming is a narrow continuation tool, not a general replacement for writing durable handoffs.
- A future primary runner should treat session transcripts as volatile evidence. Durable state still lands in Spirit, reports, repo docs, issues, and commits.
- If primary ever forks sessions for fan-out, lane/report allocation and branch/worktree allocation must be distinct. Forking the model transcript does not by itself create safe workspace isolation.

## What Maps Cleanly To Primary

Clean imports:

- one-question-at-a-time alignment with a recommendation per question
- codebase exploration before asking mechanically answerable questions
- one unbroken alignment-to-issue-slicing phase, then fresh implementation contexts
- vertical-slice issue breakdown with explicit blockers and acceptance criteria
- fresh-context review after implementation
- deterministic names for implementation branches/worktrees in code repos
- preserving dirty worktrees while removing clean generated worktrees
- stale-lock pruning by observable process liveness

Do not import directly:

- treating a grill transcript or PRD as durable intent
- letting `/grill-with-docs` write ADR/domain truth without the Spirit gate and primary report discipline
- adding a `.scratch/` issue tracker beside reports and beads without a workspace decision
- using Sandcastle's branch/merge lifecycle on primary, where everyone works directly on main
- assuming session fork means safe parallel workspace fork
- leaving completed PRDs as live guidance after their substance has moved into implementation or permanent docs

## Bottom Line

The public Pocock stack is not a single tool to copy. It is a two-layer pattern: small composable skills for alignment and issue shaping, plus Sandcastle for sandboxed implementation/review/merge loops. Primary already has stronger intent and report discipline. The valuable adaptation is narrow: sharpen `alignment-interview` with recommendation-bearing grill questions, preserve phase boundaries deliberately, make implementation slices independently fresh-context-loadable, and treat old plans/sessions as collectable once their substance has moved into Spirit, reports, repo docs, tests, or commits.
