---
variant: Research
role: operator
source: https://www.youtube.com/watch?v=-QFHIoCo-Ko&t=3729s
source_title: "Full Walkthrough: Workflow for AI Coding - Matt Pocock"
source_channel: "AI Engineer"
source_date: 2026-04-24
created: 2026-06-24
---

# Matt Pocock AI Coding Workflow Extraction

## Source And Method

Source video: "Full Walkthrough: Workflow for AI Coding - Matt Pocock", published by AI Engineer on 2026-04-24. The supplied timestamp, `3729s` (`01:02:09`), lands in the implementation phase, during the discussion of team feedback, prototypes, and when the Kanban implementation loop should begin.

I extracted the structure from the YouTube chapter metadata and English captions using `yt-dlp`, then cleaned the caption format locally because the VTT repeats partial lines as words appear. The report paraphrases the workflow rather than preserving a transcript. The captions are adequate for workflow extraction, but any exact quotation should be checked against the video.

## Core Thesis

The workflow is built around the idea that LLMs have a limited high-quality context band. Pocock calls this the "smart zone": the model does its best work early in a fresh context, then quality degrades as the context fills. The process therefore converts large work into small, feedback-rich slices that fit inside a fresh agent session.

The workflow is not "spec to code." He explicitly rejects treating a PRD as a compiler input. The human stays load-bearing during alignment, issue shaping, QA, and code review. Implementation can become AFK, but product judgment and taste stay human-owned.

## End-To-End Workflow

### 1. Research And Prototype

Use research and prototypes before committing to the destination when the idea is uncertain, especially with front-end or domain-heavy work.

The prototype does not need the full PRD loop. It is a feedback tool: create something disposable, let domain experts or the human click through it, and feed what was learned back into the alignment session.

Operational purpose:

- discover unknowns before writing a destination document
- validate UI direction visually, since AI front-end judgment is still weak
- bring research, third-party library experiments, and domain feedback back into the idea phase

### 2. Grill Session

Start almost every piece of AI work with a compact "grill me" skill rather than asking for a plan immediately.

The skill asks one decision-driving question at a time until the human and agent share the same design concept. It should walk dependencies, recommend answers, and expose decisions the human or domain expert had not considered.

Key shape:

- clear the context before starting
- pass only the brief and the grill skill
- let an isolated exploration subagent inspect the codebase and summarize back when useful
- answer the AI's questions until the ambiguous branches are resolved
- treat the conversation history as the design-concept asset

This phase is human-in-the-loop by design. If a question needs a domain expert, product owner, or teammate, pause and bring them into the loop.

### 3. Write The PRD

Convert the shared design concept into a destination document.

The PRD is not the thing to over-review. Pocock's position is that once the grill session has produced alignment, the PRD mostly summarizes that alignment. Reviewing it in detail often just tests the LLM's summarization ability.

Useful PRD contents:

- problem statement
- solution statement
- user stories
- implementation decisions
- testing decisions
- out-of-scope decisions, because they define done
- proposed modules to modify

Important implementation discipline: keep the codebase in mind while writing the PRD. This is where the future module map starts to appear. The workflow is code-aware from the PRD onward.

### 4. Slice The PRD Into Issues

Turn the PRD into a Kanban board, not a sequential multi-phase plan.

Each issue should be independently grabbable and should record blocking relationships. The result is effectively a directed acyclic graph: after a blocker lands, multiple independent issues can be assigned to agents in parallel.

The crucial slicing rule is vertical slices, or traceable bullets. AI tends to plan horizontally: database first, API second, front end last. Pocock argues that this delays integrated feedback until too late. Each slice should cross enough layers to produce something observable and testable.

Issue shape:

- local markdown issue or GitHub issue
- title
- type, such as AFK or human-in-loop
- blockers
- scope
- expected observable behavior
- tests or feedback loops to run

Human review is cheap and important here. The human should reject issues that are too horizontal and push them toward thin end-to-end slices.

### 5. Implement With AFK Agents

Once the idea, grill session, PRD, and issue graph are human-reviewed, the human can step back.

The basic sequential loop, called a Ralph loop in the talk, is:

- load the local issue backlog into context
- load recent commits
- run the coding agent with edit permissions
- let it pick the next unblocked AFK task
- have it explore the repository
- use TDD to complete the task
- run feedback loops
- produce a commit or summary
- repeat until no AFK tasks remain

The prompt prioritizes work in this rough order: critical bug fixes, development infrastructure, trace bullets, polishing, quick wins, and refactors. The implementation phase is the main AFK section, but it depends on the earlier human-reviewed preparation.

### 6. Automated Review, Human QA, And Code Review

After implementation, run an automated review in a fresh context. Pocock's reason is context quality: if the implementing agent spent the session, asking the same context to review means the reviewer is now in the degraded zone. Clearing context gives the reviewer a better shot.

Review shape:

- implement in one context
- clear context
- push coding standards and review instructions into the reviewer context
- review the commit or diff
- fix issues found by the reviewer

Then human QA and code review remain required. AI can run tests and review code, but human QA is where product taste, judgment, and reality are imposed back onto the codebase. He treats attempts to automate idea creation, research, prototype judgment, QA, and taste as a path to low-quality output.

TDD is central. The agent should write a failing test first, confirm red, implement, then confirm green. Pocock says this makes it harder for the agent to cheat by writing tests after the implementation.

Feedback loop floor:

- tests
- type checks
- manual QA
- visible end-to-end behavior for vertical slices
- fresh-context code review

### 7. Continue Through QA-Generated Issues

QA is not only a gate. It creates more Kanban work.

While agents implement, the human can QA completed slices, discover blockers or defects, and add new issues to the board. The board can absorb blocking issues continuously. The loop continues until the work is good enough for broader team review.

Only after the implementation is acceptable should it go to the team for full review.

## Parallel Agent Workflow

Pocock's Sandcastle workflow generalizes the sequential Ralph loop into parallel work:

1. A planner inspects the issue backlog.
2. It chooses a set of currently unblocked issues that can run in parallel.
3. For each issue, it creates a worktree and Docker sandbox.
4. An implementer runs inside each sandbox with the issue number, title, and branch.
5. If commits are produced, a reviewer reviews those commits.
6. A merger agent receives the created branches and issues.
7. The merger integrates branches and fixes merge, type, and test failures.

He distinguishes instruction delivery by phase:

- implementer: coding standards can be pull-based, available as skills or repo guidance when needed
- reviewer: coding standards should be pushed directly, because the review compares code against those standards

He uses a stronger model for review than implementation in this workflow because review is where judgment matters more.

## Codebase Shape For AI Effectiveness

The codebase must be shaped so feedback loops are strong.

Bad shape: many shallow modules, unclear dependencies, and tiny tests around tiny functions. This is hard for AI to navigate and hard to test well.

Good shape: deep modules with small interfaces and substantial behavior behind them. The human designs the interface and delegates implementation behind it. Tests wrap meaningful module boundaries, not every tiny internal function.

Practical rule:

- keep a module map in mind during PRD and issue slicing
- decide which deep modules will exist or change
- design the interface
- let agents implement inside the boundary
- test from the boundary where possible

This preserves human understanding of the system while still delegating implementation.

## Documentation Lifecycle

Pocock is wary of leaving completed PRDs and plans in the repository as live guidance. Once code has moved on, old PRDs can mislead agents because they look authoritative while being stale.

His preferred handling is to keep issue history where completed status is visible, such as closed GitHub issues, instead of leaving old markdown plans in the active repo. If docs remain, they must not silently become stale context for agents.

## Operator Adaptation For This Workspace

The useful pieces for the operator lane map closely to existing workspace discipline:

- Grill session maps to psyche-facing clarification before design or implementation. For durable workspace intent, Spirit remains the source of truth; a grill transcript is task state unless the psyche states a durable decision.
- PRD maps to a destination report or per-repo design surface, not a replacement for `INTENT.md`.
- Kanban issue graph maps to beads plus, where needed, report-backed implementation plans. Use vertical slices rather than horizontal schema/API/UI layers unless a designer report explicitly requires a different cut.
- AFK implementation maps to operator work on claimed paths, but this workspace forbids hidden blocking subagents unless the psyche authorizes dispatch. Parallelism must use explicit lanes or authorized background subagents.
- Fresh-context review maps to a separate review pass after implementation. In this workspace, that can be another operator lane or a later fresh context, with `skills/testing.md`, repo `INTENT.md`, and relevant reports pushed into the review context.
- Sandboxed worktree branches map to the code-repo operator flow under `/git`, not primary. Primary reports stay on main directly.
- The old-PRD warning aligns with this workspace's report discipline: durable truth migrates into `INTENT.md`, `ARCHITECTURE.md`, skills, tests, and current reports. Stale reports should be agglomerated or retired.

## Workflow Checklist

For a new feature using this pattern:

1. Start with a small context: brief plus relevant skill.
2. Run a grill session until the design concept is shared.
3. Pull in domain experts or teammates for unresolved human decisions.
4. Write a destination PRD or report with out-of-scope and testing decisions.
5. Identify the module map and deep-module boundaries.
6. Convert the destination into vertical-slice issues with blockers.
7. Human-review the issue graph, especially for horizontal slicing.
8. Let agents implement unblocked AFK issues with TDD and feedback loops.
9. Review in a fresh context with standards pushed into the reviewer.
10. Human-QA the observable behavior and add new issues for defects.
11. Repeat until the work is good enough for team review.
12. Retire or close stale planning artifacts so agents do not treat them as current truth.

## Timestamps

- `00:03:00` - LLM constraints, smart zone, dumb zone, and task sizing.
- `00:06:48` - Ralph loop: destination plus repeated small changes.
- `00:12:21` - Grill me skill introduced as alignment mechanism.
- `00:26:49` - Human-in-loop work versus AFK work.
- `00:30:39` - PRD as destination document.
- `00:33:00` - PRD remains code-aware through proposed modules.
- `00:39:38` - PRD to Kanban issue graph.
- `00:41:47` - Vertical slices / traceable bullets.
- `00:49:39` - Independently grabbable issues and parallel agents.
- `00:52:15` - Human exits the loop for implementation.
- `00:54:19` - Local issues and a simple once-run agent loop.
- `00:55:12` - AFK loop and Docker sandbox.
- `01:05:28` - Automated review before human QA.
- `01:06:42` - TDD for agents.
- `01:09:02` - Completed issue becomes immediately QA-able.
- `01:13:39` - Human QA as taste and quality control.
- `01:14:19` - Deep modules and AI-effective codebase shape.
- `01:23:23` - Plan/PRD doc rot warning.
- `01:28:22` - Push versus pull context for standards and skills.
- `01:29:50` - Sandcastle parallel worktree/sandbox workflow.
- `01:34:15` - Final summary of alignment, PRD, issues, implementation, QA, and review.
