A prompt that is or contains only a bead ID (like primary-751) is a
dispatch envelope. Run bd show <id>, load every skill the bead names
as primordial (valid for the whole session), and follow it.

Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

## Skills

Authored skill sources are only `/git/github.com/LiGoldragon/skills/skills/*.md`.
Identity and deployment selection are only `manifests/*.dotos`.
`.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
evidence; never edit them directly. Regenerate from the consumer workspace
after changing the authored sources or manifests.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `psyche/` before assuming.
