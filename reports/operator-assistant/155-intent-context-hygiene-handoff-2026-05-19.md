# Intent Context Hygiene Handoff

Status: superseded. This report incorrectly treated an intent
append as blocked by an orchestrate claim. `skills/intent-log.md`
now says routine intent recording is a lock-free shell append:
`cat >> intent/<topic>.nota <<'EOF' ... EOF`. The live-context
clarification this report proposed is already recorded in
`intent/workspace.nota` as the 2026-05-19T16:35:00Z
`Clarification`; the append-mechanism correction is recorded there
as the 2026-05-19T16:45:00Z `Correction`. Do not treat this report's
proposed entry as pending work.

## Read

I reread the workspace intent surfaces relevant to this request:

- `AGENTS.md`
- `ESSENCE.md`
- `ONBOARDING.md`
- `repos/lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `skills/intent-log.md`
- `skills/intent-clarification.md`
- `skills/repo-intent.md`
- `skills/intent-maintenance.md`
- `intent/workspace.nota`
- `intent/persona.nota`

The current format is positional NOTA in broad topic files under
`intent/`. Each entry is one of `Decision`, `Principle`,
`Correction`, `Clarification`, or `Constraint`, with summary,
verbatim psyche quote, context, certainty, and bare ISO-8601
timestamp.

## Finding

The live prompt contains one durable workspace-level psyche
statement that is not just a routine instruction: during an intent
context sweep, capture only actual live psyche prompts still in the
agent's context. Do not mine compacted summaries, old history, or
agent-written material as fresh psyche.

I did not record earlier compacted-history prompts. The prompt
explicitly excluded them. I also did not add a new persona-spirit
entry, because `intent/persona.nota` already records the current
persona-spirit decisions and principles.

## Blocker

`tools/orchestrate status` shows a fresh `designer` claim on
`/home/li/primary/intent`:

```text
/home/li/primary/intent # absorb psyche answers + corrections on persona-spirit design
```

The working copy also has existing designer-lane changes in
`intent/persona.nota`, `reports/designer/232-persona-spirit-new-component.md`,
and `skills/skills.nota`. I therefore did not edit
`intent/workspace.nota` directly from the operator-assistant lane.

## Proposed Intent Entry

Append this to `intent/workspace.nota` once the intent directory is
free or the designer owner absorbs it:

```nota
  (Constraint
    "When sweeping current context for intent, capture only actual live psyche prompts still present as fresh human input. Do not treat compacted summaries, old history, agent-written files, reports, or prior tool summaries as new psyche intent."
    "If there's anything in your context, if there's like any actual real psyche prompts that you still have in your context, not old history, not compacted history, like new real prompts that you still have in your context that you can turn into intent or that you can add to intent files, that you can create them"
    "Psyche asked the agent to reread the intent protocol, intent clarification, and repo-intent discipline, then capture only durable intent from the live prompt rather than mining compacted conversation history."
    Maximum
    2026-05-19T11:02:52Z)
```

## Repo Intent

No per-repo `INTENT.md` update follows from this prompt. The new
statement is workspace protocol, not project-specific intent for a
repository.
