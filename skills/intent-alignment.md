# Skill — intent alignment

## What this skill is for

Intent alignment is the canonical protocol for interactive agents to turn a
psyche request into an executable dependency graph. Before planning or building,
orient to what the psyche is trying to do and how they want to operate right now
— what is being built, why it matters, what counts as done, and which choices
are still open. This is the default posture from the first message of a fresh
session, not a step reached for only when a request looks ambiguous; an agent
that dives into execution on its own assumptions about what the psyche wants is
the failure this skill exists to stop. The goal is shared understanding of the
goal, scope, success checks, and first useful slice. A narrowly specialized
agent that ships already trained for one job is the exception — it needs no
interview.

A clear directive to implement or to show is itself the answer: build the
dependency graph, do the work in graph order, and present the result, treating
reversible choices as defaults you can switch later. Reserve the interview for
genuinely ambiguous requests and for blocking, hard-to-reverse forks. Alignment
sharpens intent; it never becomes a reason to stall.

## Dependency graph first

The interview exists to discover the task dependency graph: what must precede
what, what can run in parallel, what is blocked on a psyche answer, and what
check proves each node is done. A linear checklist is a projection of that
graph, not the source of truth.

When the psyche gives a goal, sketch the graph before planning:

- **Goal node** — the user-visible state that counts as done.
- **Input nodes** — repositories, reports, branches, credentials, services, or
  profile state the work depends on.
- **Decision nodes** — choices only the psyche can answer.
- **Work nodes** — edits, builds, migrations, activations, or reports.
- **Verification nodes** — tests, commands, visible UI behavior, or deployment
  checks that prove a work node.
- **Parallel nodes** — independent audits or implementation slices that can be
  delegated without overlapping writes.

Ask only for graph edges or node meanings that change the first executable
slice. Once the graph is clear enough, execute from prerequisites toward the
goal, dispatching subagents only when the psyche asked for delegation and the
nodes are genuinely independent.

For reading/exploring early in context, the universal orientation-dispatch
default applies: send a helper and reason over its report rather than reading
broadly yourself. The psyche-gate here governs change-making dispatch only.

## Interview shape

Start with the user's brief and the smallest useful repo or product context.
Ask exactly one focused question per turn, in plain chat prose — never a batch
of questions, and never the structured questionnaire UI. The questioning is
relentless: one question, the psyche's answer, then the next question shaped by
that answer, continuing until the dependency graph is clear enough to execute.
Each question carries:

- the decision being made
- why it matters
- the recommended answer
- one or two reasonable alternatives when they change the outcome

Use ordinary language. Expand acronyms and explain domain terms the first time
they appear. If a term is not needed, use the plain version instead: say
`destination note` before `product requirements document`, and say `write the
test first` before `test-driven development`.

## What to ask about

Work from highest-risk ambiguity to lower-risk detail:

- user and problem: who this is for and what pain it solves
- finished behavior: what the user should be able to do afterward
- boundaries: what is in scope, out of scope, and explicitly deferred
- existing system: which repo, module, workflow, or data shape this touches
- success checks: what test, manual check, or visible behavior proves it works
- rollout: whether this is prototype, local-only, production, migration, or
  documentation
- dependency edges: what must happen first, what may run concurrently, and what
  blocks later work
- unresolved people questions: who else must answer product, domain, security,
  or operational choices

## How to use recommendations

Give a recommendation with each question so the psyche can approve, correct, or
replace it. A good recommendation is concrete enough to accept as written. When
the agent is guessing, mark it as a guess and explain the evidence.

Ask when a load-bearing variable is missing. Do not silently choose defaults for
variables that change authority, priority, scope, safety, privacy, certainty,
importance, rollout, or who owns the decision. Give the recommended value and
the consequence of choosing it, then let the psyche accept or correct it. This
applies especially when converting alignment answers into Spirit metadata: if
importance, certainty, privacy, or kind would change how future agents treat the
record, ask instead of laundering the agent's guess through the guardian.

If the psyche answers with a correction, carry the correction forward. If the
answer states durable workspace intent rather than task detail, run the Spirit
gate before continuing.

## Stopping point

Stop the interview when the remaining questions no longer change the first
useful slice of work. Then write a short handoff:

- shared goal in plain language
- decisions made
- out-of-scope items
- dependency graph: ordered prerequisites, parallel slices, and blocked nodes
- first vertical slice or next report/task to create from that graph
- tests or checks expected for each node on the first slice
- open questions that still need a human answer

The handoff is task state unless the psyche explicitly makes a durable
workspace decision. Put substantive handoffs in the appropriate report, issue,
or repo surface rather than leaving them only in chat.

## See also

- `human-interaction.md` — psyche-facing capture and clarification rules.
- `reporting.md` — when the handoff belongs in a report instead of chat.
- `intent-log.md` — how durable psyche intent differs from task state.
