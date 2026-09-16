# curriculumSubagentGap

## 2026-09-16 — Curriculum has no authored surface for specialty subagents; roles.datom generates only permission×depth workhorses

Context: after the concept subagent test succeeded, the living asked to add the description to the Claude subagents that are generated in Curriculum, and acknowledged that Curriculum's regeneration may delete files not authored there.

> Okay, let's make the concept subflow subagent description and add it to the Claude subagents that are generated in curriculum. I'm guessing curriculum deletes all of the files that are not currently there. I'm not sure. We might have to rethink that. Maybe there's a namespace for different elements to generate different skills, but we're just going to go with how it works for now.

-- psyche, typed.

Flow reading, not the living's words: Curriculum's own `AGENTS.md` and `ARCHITECTURE.md` state its authored surface is `skills/*.md` and `roles.datom` only. The primary repo's `.claude/agents/*.md` files (`read-trivial`, `read-ordinary`, `read-demanding`, `write-trivial`, `write-ordinary`, `write-demanding`) are generated from `roles.datom`'s `descriptions` positional field — six `{permission depth «description»}` tuples that produce six subagents by convention. A specialty subagent — `visual-report-from-md`, or a future one — does not fit that permission×depth matrix.

Two paths for now, both imperfect:

1. **Author the subagent source at `Curriculum/skills/<name>.md`** with subagent-style frontmatter (`name`, `description`, `model`, `tools`, plus a `kind: subagent` marker) so a future Curriculum runtime pass can distinguish it from an ordinary skill. That is what this flow just did for `visual-report-from-md` — committed at `a6c0d66` on Curriculum `main`. Downside: the current runtime probably does not know about `kind: subagent` and will not generate a matching `.claude/agents/<name>.md`.
2. **Extend `roles.datom` to carry a specialty-subagent list** — a new positional field or a new variant inside `descriptions`. Downside: schema change; the runtime must be updated in lock-step.

The living has flagged that a rethink is due — a namespace for different kinds so different generators produce different files. This entry records the gap so the rethink has a place to start.

## Consequences for the current test

- `.claude/agents/visual-report-from-md.md` in this flow's worktree (committed to `flow/48cff7`) is the *runtime* form of the subagent. If Curriculum regenerates the primary repo's `.claude/` tree from `roles.datom` today, this file is likely deleted.
- `Curriculum/skills/visual-report-from-md.md` (committed at `a6c0d66`) is the *authored* form. It survives Curriculum's own edits.
- Until the runtime learns to generate a subagent file from a skill with `kind: subagent`, the ad hoc `.claude/agents/` copy is the only way the harness can invoke the subagent by name.

## Open questions worth the living's word

1. Confirm the two paths above are the right framing, or name a third.
2. Choose the direction — extend `roles.datom` schema, add a new authored file type in Curriculum, or something else.
3. Which flow does the runtime update — an implementation subflow dispatched to Codex, a Claude implementation subflow, or a joint pair.
4. Whether the ad hoc `.claude/agents/<name>.md` copies live in `flows/<flow>/.claude/agents/` per flow until Curriculum handles them, or somewhere else.
