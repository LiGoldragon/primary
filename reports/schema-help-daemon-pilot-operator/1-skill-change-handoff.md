---
title: 1 — Context-preserving subagent dispatch skill handoff
role: schema-help-daemon-pilot-operator
variant: Handover
date: 2026-06-24
topics: [skills, subagents, context, human-interaction]
description: |
  Handoff for the skill change needed after the main agent consumed the
  context that the psyche explicitly asked a subagent to spend instead.
slot: 1
---

# 1 — Context-preserving subagent dispatch skill handoff

## What Happened

The psyche asked the main operator session to use a subagent to determine
whether the schema-help daemon pilot bead graph was aligned enough for
fanout. The point of the request was context economy: the subagent should
collect the broad repo, report, bead, and intent context, then return a
compact summary for the main session to use.

The main agent did the opposite. Before and after launching the subagent it
loaded broad workspace, operator, reporting, beads, Rust, actor, contract,
schema, testing, Nix, and repo-map context in the main thread. It also
registered a lane, wrote `reports/schema-help-daemon-pilot-operator/0-frame-and-method.md`,
spawned one context subagent, then continued doing readiness checks while
the subagent ran. The psyche interrupted because the main session had
already spent the context budget the subagent was meant to preserve.

The subagent `019efb1d-c112-7f82-ba9a-9b5fb960f65a` was shut down before it
returned a report. No code-repo implementation fanout was launched.

## Failure Mode

The current guidance makes three correct rules collide badly in this case:

- psyche-facing agents load intent / interaction guidance before answering;
- agents read the relevant skills before acting;
- when substantial work begins, agents gather enough context to make the
  plan safe.

Those rules lack one special case: when the psyche explicitly asks for a
subagent to collect context or preserve main-session context, the main
agent must run a **minimal dispatch envelope** and stop reading broadly.
The delegated context-gathering task owns the broad read.

The missing rule is not "use subagents non-blocking" — AGENTS.md already
says that. The missing rule is **context-preserving dispatch discipline**:
after the minimal edge checks, the parent must not duplicate the
subagent's exploration in the parent context.

## Skill Change Needed

Add a concise rule to the psyche-facing / autonomy guidance. Best target:
`skills/human-interaction.md`, because this is triggered by a psyche
request shape. A cross-reference from `skills/autonomous-agent.md` or
`skills/operator.md` may also be useful, but the atomic rule belongs at the
human boundary.

Suggested substance:

```markdown
## Context-preserving subagent dispatch

When the psyche explicitly asks to use a subagent to collect context,
save context, decide alignment, or prepare fanout, the parent agent runs
only the minimal dispatch envelope: Spirit gate, lane/report slot setup
if needed, and the subagent brief. The parent does not read target repos,
broad topic skills, reports, or bead graphs that the subagent was asked
to collect. The subagent writes the context report; the parent waits for
that report or does only genuinely unrelated work.
```

The parent can include the user's pasted graph or instructions in the
subagent prompt without locally verifying them first. Verification is the
subagent's job in this pattern.

## Warning For The Next Session

Do not resume the schema-help daemon pilot work first. Do not relaunch the
alignment subagent. Do not start by reading the broad schema, Rust, actor,
Nix, report, and bead context again. That repeat would recreate the exact
failure this report exists to prevent.

The first action is the skill fix. Patch the human-boundary guidance so
future agents know that a psyche request for context-saving subagents means
the parent runs only the minimal dispatch envelope and delegates the broad
read. Only after that rule lands should any session reopen the
schema-help pilot fanout.

## Current Workspace State

There are existing uncommitted edits from another lane:

- `skills/human-interaction.md`
- `reports/preciousMainContext/5-human-interaction-cut.md`

The current `human-interaction` edit is a pruning pass that removes a
duplicated "Subagent dispatch — always non-blocking" section because
AGENTS.md already carries that rule. That is compatible with this handoff:
the new rule should not re-add the duplicate "always non-blocking" text.
It should add the narrower context-preserving behavior above.

Before committing the skill work, inspect the current dirty diff. At the
time this handoff was written, `skills/human-interaction.md` also contained
stray literal tool-wrapper text near the end (`</content>` and `</invoke>`).
That should be removed as part of the skill cleanup before the working copy
is committed.

## Pickup Steps

1. Read this report and the current dirty diff for `skills/human-interaction.md`.
2. Clean the existing `skills/human-interaction.md` edit enough to publish,
   including removing any literal tool-wrapper residue at the file end.
3. Add the context-preserving subagent dispatch rule without restoring the
   broader duplicated sections removed by the `preciousMainContext` pruning
   pass.
4. Decide whether the rule lands in `skills/human-interaction.md` only, or
   also gets a pointer in `skills/autonomous-agent.md` / `skills/operator.md`.
5. Update `skills/skills.nota` only if the manifest description is being
   edited in the same cleanup wave.
6. Run a quick markdown readback of the edited skill, especially the file end,
   to catch tool-wrapper residue.
7. Commit the whole primary working copy and push `main` only after the dirty
   skill state is clean enough to publish.
