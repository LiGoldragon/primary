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
