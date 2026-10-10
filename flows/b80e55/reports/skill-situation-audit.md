# Skill situation audit — generation, deletion risk, and curriculum redesign

Flow b80e55, subflow report, 2026-09-21.

## Current state

65 skills in primary `.claude/skills/`, all with exact counterparts in
Curriculum `skills/`. Zero skills exist in primary that are not in Curriculum.
This means every skill was first authored in Curriculum, then projected
(copied) to primary's `.claude/skills/` and `.agents/skills/` trees.

9 testing-prefixed skills exist: testing-commit-scope, testing-datom-messaging,
testing-flashbook, testing-flashbook-illustration, testing-flow-titles,
testing-generated-projection, testing-long-run-progress, testing-message-route,
testing-push-landed. All 9 are currently in Curriculum.

## How projection works today

There is **no automated generator**. Curriculum is a pure data repository with
no CLI, Nix build derivation, deployment script, or Makefile. The `result`
symlink points to a Nix store path `skills-0.5.0` that is not present on this
host. Projection is done manually by flows: a flow reads a Curriculum skill
source, writes it to `.claude/skills/<name>/SKILL.md` and
`.agents/skills/<name>/SKILL.md`, and commits.

All observed regeneration commits (14 in the last 200 commits) are **additive**:
they add new skills or update existing ones. None deletes a skill. No commit
in the last 500 shows bulk `rm -rf .claude/skills/` or directory cleanup.

## The deletion risk

Today: **low**. Manual projection only adds/updates. But the CLAUDE.md says
these trees are "generated read-only evidence; never edit them directly." If an
automated generator is built (the living's vision: "a binary, an executable
with a nexus with CLIs, and it regenerates some skills"), it would logically
`rm -rf` and recreate, destroying any ad-hoc skill not in its source.

The living's correction: Curriculum should **only delete the types of skills
it's overwriting**, not blanket-delete. If it's overwriting vision-type skills,
it deletes only those. Testing-prefix skills authored elsewhere survive.

## The redesign needed

1. **Skill types with prefixes** — skills have types (vision, operational,
   testing, etc.) and Curriculum knows which types it owns per regeneration.
2. **Type-scoped deletion** — a regeneration of vision skills deletes only
   `vision-*` skills, not `testing-*` or `operational-*`.
3. **Three source repos** — psyche, mind, field. Each generates skills with
   the right prefix. All project to the same shared primary.
4. **Testing skills** — authored ad-hoc by flows, not by Curriculum. Protected
   from regeneration by prefix.

## Immediate protection

Until the redesign lands, testing-prefix skills should also live in
Curriculum as their source of truth (they currently do). If an automated
generator is built, it must respect the type-scoped deletion rule before
being used.
