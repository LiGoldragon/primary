# Skill — intent alignment

## What this skill is for

Intent alignment is the default first move for an interactive agent: on any
psyche request that isn't already crisp enough to execute, align with the psyche
on what is being built, why it matters, what counts as done, and which choices
are still open, before turning it into a plan or tasks. The goal is not a fast
plan; it is shared understanding of the goal, scope, success checks, and the
first useful slice. A narrowly specialized agent that ships already trained for
one job is the exception — it needs no interview.

A clear directive to implement or to show is itself the answer: do the task and
present the result, treating reversible choices as defaults you can switch
later. Reserve the interview for genuinely ambiguous requests and for blocking,
hard-to-reverse forks. Alignment sharpens intent; it never becomes a reason to
stall.

## Interview shape

Start with the user's brief and the smallest useful repo or product context.
Ask exactly one focused question per turn, in plain chat prose — never a batch
of questions, and never the structured questionnaire UI. The back-and-forth
rhythm is the method itself: one question, the psyche's answer, then the next
question shaped by that answer. Each question carries:

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
- first vertical slice or next report/task to create
- tests or checks expected
- open questions that still need a human answer

The handoff is task state unless the psyche explicitly makes a durable
workspace decision. Put substantive handoffs in the appropriate report, issue,
or repo surface rather than leaving them only in chat.

## See also

- `human-interaction.md` — psyche-facing capture and clarification rules.
- `reporting.md` — when the handoff belongs in a report instead of chat.
- `intent-log.md` — how durable psyche intent differs from task state.
