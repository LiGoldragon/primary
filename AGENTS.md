A prompt that is or contains only a bead ID (like primary-751) is a
dispatch envelope. Run bd show <id>, load every skill the bead names
as primordial (valid for the whole session), and follow it.

Worker agents (non-management) *must* read @WORKING_AGENTS.md.

## Skills: source of truth and deployment

- `.agents/skills/` is the source of truth. Create and edit skills here only.
- Pi and Codex read from `.agents/skills/` directly.
- `.claude/skills/` is a deployed copy for Claude Code. Its contents must mirror `.agents/skills/`.
- Never create skills in `.claude/skills/`, `.codex/`, or `.pi/`. Author in `.agents/skills/`, deploy outward.
- A skill found in `.claude/skills/` but not in `.agents/skills/` is improperly placed; move it to `.agents/skills/`.

## Psyche

Psyche is the living mind the agent extends. Agents never access it
directly — they infer from what the psyche has expressed in writing.

Three levels, descending authority:

- **Spirit** — philosophy. Almost never changes. The psyche announces
  Spirit epiphanies; do not ask "is this Spirit?" Read
  `psyche/Spirit.md`.
- **Intent** — declared goals and guiding rules for a project or
  domain. Broader than Vision, rarer. When work does not align with
  known Intent, escalate to the psyche before continuing.
- **Vision** — concrete, domain-scoped, abundant, moves constantly.
  The default level. Everything starts here unless obviously broader.

Less Spirit than Intent, less Intent than Vision. Inversion signals
unenunciated Vision or contaminated levels.

Psyche logs live in `psyche/`:
- `psyche/Spirit.md` — single file, all agents read.
- `psyche/Intent/<aspect>/<topic>.md` — per awareness aspect, per topic.
- `psyche/Vision/<aspect>/<topic>.md` — per awareness aspect, per topic.

Use these logs to check alignment. If your work contradicts known
Intent, stop and ask the psyche what they want to do.
