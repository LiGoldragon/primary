# Primary Workspace — Agent Instructions

This file is intentionally compact. It carries discipline that applies
on every keystroke. Rationale, examples, and detail live in
`skills/<name>.md`, `AGENTS-extended.md`, and the skill index at
`skills/skills.nota`.

## Required reading, in order

1. **`ESSENCE.md`** — workspace intent. Upstream of every other doc.
2. **`repos/lore/AGENTS.md`** — cross-workspace agent contract.
3. **`orchestrate/AGENTS.md`** — how roles share this workspace.
4. **Your role's `skills/<role>.md`** carries your required-reading list.
5. **The repo's `AGENTS.md` + `skills.md`** when editing inside a repo under `repos/`.

The skill index lives in `skills/skills.nota` — kind, tier, one-line
description per skill. Query by topic, not by filename.

## Roles

Four main roles, each with stacked lanes. The lane mechanism is
canonical in `orchestrate/AGENTS.md` and `skills/role-lanes.md`.

- `operator` — implementation
- `designer` — architecture, skills, reports
- `system-specialist` — OS / platform / deploy
- `poet` — prose as craft

Each agent must know its lane before claiming or editing.

## Chat reply discipline

The chat is the user's working surface. The user is juggling many
agents — they don't have time to read narration.

- **Brief.** State what changed and what's next.
- **No process narration.** No "I'll now do X." Just do it.
- **Substance in artifacts.** Reports, skill files, ARCH files. The chat carries paths + user-attention items only.
- **No long enumerations in chat.** Tables, lists, multi-paragraph explanations belong in a report.

Full discipline: `skills/reporting.md`.

## Reports — substance + path + decisions

Output that explains, proposes, analyses, audits, or summarises goes
in `reports/<role>/<N>-<topic>-<date>.md`. The chat names the path and
surfaces what the user must read, decide on, or act on — inline, with
substance, not as a teaser.

Each role writes only into its own role subdirectory. Reports are
exempt from the claim flow.

When an agent creates, edits, supersedes, or deletes a report, the
chat reply names the full report path.

Full discipline: `skills/reporting.md`.

## Skills should not be noisy

Agents are smart enough to fill in obvious blanks. Skill files carry
the rule and the *why*, not every edge case. When a skill grows past
what an agent reads in one pass, the agent stops reading.

If you're editing a skill, ask: what would a smart agent miss without
this line? If the answer is "nothing", cut the line. Hard caps and
quoted line counts are noise.

Full discipline: `skills/skill-editor.md`.

## Spell every identifier as a full English word

`Request` not `Req`. `Reply` not `Rep`. `Configuration` not `Cfg`.
Types, fields, variables, macro template placeholders, file-internal
helpers — *everything* spells out. Carve-outs and rationale in
`ESSENCE.md` §"Naming" and `skills/naming.md`.

## Nix store search is forbidden

Don't run `rg`, `grep`, `find`, `fd`, broad globs, or recursive `ls`
against `/nix/store`. Use Nix tooling (`nix eval`, `nix flake show`,
`nix path-info`). Full rule in `AGENTS-extended.md` §"Nix discipline".

## No harness-dependent memory

Memory lives in workspace files every agent can open — `skills/`,
`reports/`, `protocols/`, repo `skills.md`, repo `ARCHITECTURE.md`.
Never in harness-private state. Full rule in `AGENTS-extended.md`.

## Two deploy stacks coexist

Production runs on `main` in the canonical `/git/...` checkouts. The
lean rewrite lives on `horizon-leaner-shape` branches in `~/wt/...`
worktrees. **Do not fold one into the other piecemeal.** Live
inventory in `protocols/active-repositories.md`.

## Feature branches live in worktrees

Multi-commit work on production code lives in
`~/wt/github.com/<owner>/<repo>/<branch-name>/`, not in the canonical
`/git/...` checkout. Full discipline in `skills/feature-development.md`.

## See also

- `AGENTS-extended.md` — rationale, the where-things-live table, the BEADS transitional note, longer explanations.
- `skills/skills.nota` — typed skill index (name, path, kind, tier, description).
- `orchestrate/AGENTS.md` — role coordination protocol.
- `ESSENCE.md` — workspace intent.
