# Skill — intent clarification

*When intent on a question is unclear, absent, or contradicted, ask
the psyche. Don't infer; don't compose new intent from old; ask.
The cost of one question is bounded; the cost of building on
invented intent compounds.*

## What this skill is for

The intent layer (the workspace `intent/` log, per-repo
`INTENT.md`, and `ESSENCE.md`) is the source of authoritative
direction. When the agent is about to make a decision and one of
these is true, this skill applies:

- No documented psyche intent speaks to the question.
- Two psyche intents speak to the question with conflicting
  implications.
- A documented intent applies but the agent is uncertain whether
  the current case fits the recorded shape.
- The agent is about to *propose* changing a documented intent
  (which by `skills/intent-maintenance.md` requires explicit
  psyche confirmation anyway).

**The agent asks the psyche before deciding.** Inferring is the
discipline breaking; asking is the discipline working.

## When to ask vs when to proceed

Some decisions are agent-territory, no psyche question needed:

- Routine implementation: a variable name, the shape of an
  unexposed helper, the choice between two equally-good libraries
  with no documented psyche preference.
- Tactical sequencing: which step first within a task whose
  goal is already clear.
- Applying documented intent literally to a case it plainly
  covers.

Some decisions need a question:

- Anything that could *contradict* documented intent.
- Anything that *extends* documented intent into new territory
  the psyche hasn't named.
- Anything where the agent has to *invent* a principle to
  proceed — principles are psyche-territory.
- Anything the psyche has previously been ambiguous about and the
  agent's current choice will set a precedent.

The test: *would the psyche have a specific opinion on this if
asked?* If yes, ask. If no, decide.

## How to ask

Per `skills/reporting.md` §"Questions to the user — paste the
evidence, not a pointer":

1. **Surface the gap concretely.** Quote any existing psyche
   intent (with the file path it's recorded under). Name what's
   recorded and what's not.
2. **Propose 2-4 options with tradeoffs.** Each option includes
   what it costs and what it gains. The psyche picks one or
   redirects.
3. **State your lean** if you have one. The psyche may accept it
   directly; that's faster than them generating from scratch.

Don't ask open-ended ("what do you think?"). Don't ask without
options. The psyche's time is the resource; structured questions
cost them seconds, open-ended questions cost minutes.

## After the psyche answers

1. **Record the new intent** per `skills/intent-log.md` — the
   psyche just gave you a new statement; that's intent.
2. **If the new statement supersedes prior intent**, follow
   `skills/intent-maintenance.md` §"Supersession protocol".
3. **If the new statement extends intent (no override)**, record
   under a new sub-topic; cross-reference if useful.
4. **Update the relevant per-repo `INTENT.md`** per
   `skills/repo-intent.md` if the new statement is
   project-specific.

## When the psyche is not reachable

If the psyche cannot be reached within the timeframe of the
work, three options, in order of preference:

1. **Defer the decision.** Park the work that needs the answer.
   Continue with work that doesn't.
2. **Pick the most conservative option.** If proceeding is
   required, take the option that's most easily reversible if
   the psyche later corrects.
3. **State the assumption explicitly** in the chat / report
   where the work lands: *"Decided X assuming Y; will revise if
   psyche corrects."*

Don't silently invent intent. Don't promote agent inference to
documented intent.

## See also

- `skills/intent-log.md` — recording psyche statements.
- `skills/repo-intent.md` — per-repo `INTENT.md` discipline.
- `skills/intent-maintenance.md` — supersession protocol.
- `skills/reporting.md` §"Questions to the user — paste the
  evidence, not a pointer" — how to ask.
- `ESSENCE.md` §"Intent is primordial; psyche is the source" —
  the apex principle this skill enforces.
