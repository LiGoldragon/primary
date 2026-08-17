# Entry files — CLAUDE.md, AGENTS.md, NON_MANAGEMENT_AGENTS.md, agent variables

Design session `358f143a`, typed (captured 2026-08-17T19:01+02:00).
Excerpts from one message answering the Designer's anatomy of the
entry files; trims between them.

## 2026-08-17 — why `CLAUDE.md` as `@AGENTS.md` was unoptimal

> the subagent problem is codex only, and @ references arent loaded
> recursively, apparently.

## 2026-08-17 — one authored entry module in Curriculum generates CLAUDE.md and AGENTS.md

The Designer proposed one authored entry module in Curriculum with
`{% if claude %}` / `{% if codex %}` conditionals, emitting CLAUDE.md
and AGENTS.md into the consumer workspace:

> yes, exactly what I was thinking

On the Designer's count that shared lines are now written two or
three times:

> twice, not thrice

## 2026-08-17 — the Sol subagent constraint stays in AGENTS.md

The Designer had called the "Temporary subagent model constraint" a
hack belonging in NON_MANAGEMENT_AGENTS.md:

> too risky. I cant affort a bunch of sol subagents destroying my
> quotas again. With almost no upside.

## 2026-08-17 — variables have names; they live in their own setup-specific file, documented in Curriculum's agents.md

The Designer had proposed a `## Skills` line listing reference skill
collection paths:

> theyre not variables if they dont have a name, but that is rougly
> the idea

On NON_MANAGEMENT_AGENTS.md holding only the hacks:

> right now its doing too much. variables should go in its own
> (AGENT_VARIABLES.md?) file, which is setup specific and therefore
> not in curriculum, but is documented in curriculum's agents.md file,
> so agents are made aware that those variables should be set and how.

Context (agent-authored, separate from the psyche's words): the
end-shape ruled — Curriculum authors one entry module and generates
CLAUDE.md and AGENTS.md per target; Codex-only material (the Sol
constraint) rides a codex conditional and is not demoted to a hack
file; setup-specific values (paths, reference collections) become
named variables in a workspace-owned file whose name is tentatively
AGENT_VARIABLES.md; the authored entry module documents which
variables must be set and how; NON_MANAGEMENT_AGENTS.md shrinks
accordingly.
