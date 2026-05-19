# Intent Context Sweep

Role: system-specialist

## Documents Read

- `AGENTS.md`
- `ESSENCE.md`
- `repos/lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `skills/skills.nota`
- `skills/intent-log.md`
- `skills/intent-clarification.md`
- `skills/intent-maintenance.md`
- `skills/repo-intent.md`
- existing `intent/*.nota`

## Protocol Understood

The intent layer is the highest-authority workspace surface:

- `ESSENCE.md` holds the most universal, maximum-certainty psyche
  intent.
- `intent/<topic>.nota` records explicit psyche statements verbatim,
  by broad topic, in positional NOTA.
- `<repo>/INTENT.md` is agent-written prose, but every statement in it
  must be directly backed by recorded psyche intent.
- If intent is absent, unclear, or contradictory, the agent asks the
  psyche rather than inferring.

Only psyche prompts are source material. Agent reports, summaries,
compacted history, and NOTA-formatted agent messages are not psyche.

## Existing Intent State

The current intent log already records the load-bearing protocol:

- `intent/workspace.nota` records intent as the cornerstone of agent
  activity, psyche as the human source, `INTENT.md` as per-repo intent
  synthesis, and the authority of the intent layer.
- `intent/reports.nota` records the chat-versus-report discipline.
- `intent/nota.nota` records positional NOTA rules.
- `intent/component-shape.nota` records component-triad constraints.

I found no existing per-repo `INTENT.md` files under the active
LiGoldragon checkouts I inspected.

## Live Context Candidate

The only current live psyche prompt I found that should become intent
is this turn's constraint on backfilling intent from context. It belongs
in `intent/workspace.nota`.

Candidate record:

```nota
(Constraint
  "When backfilling intent from context, use only live psyche prompts in the current context. Do not record intent from old history, compacted summaries, or agent-written summaries."
  "if there's like any actual real psyche prompts that you still have in your context, not old history, not compacted history, like new real prompts that you still have in your context that you can turn into intent or that you can add to intent files, that you can create them"
  "The psyche asked for an intent-protocol pass and clarified what context is eligible for backfill."
  Medium
  2026-05-19T11:02:20Z)
```

## Not Recorded

I did not record the cluster-data variant decisions from compacted
history, even though they are real and recently implemented, because
the psyche explicitly narrowed this task away from old history and
compacted history. Those decisions currently live in reports and repo
architecture, but not in `intent/`.

I also did not create any per-repo `INTENT.md` files. The live context
available to me in this task contained no new repo-specific psyche
prompt that was both current and not already a report/code task.

## Blocker

I did not edit `intent/workspace.nota` because the designer lane holds
the live `/home/li/primary/intent` lock:

```text
/home/li/primary/intent # absorb psyche answers + corrections on persona-spirit design
```

This report is the handoff for the candidate entry above. Once the
designer releases `intent/`, that entry can be applied directly if the
psyche still wants this system-specialist lane to do it.
