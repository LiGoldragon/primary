Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

## Skills

Authored skill sources are only the `*.md` files under `Curriculum skills`.
Identity and deployment selection are only `manifests/*.dotos`.
`.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
evidence; never edit them directly. Regenerate from the consumer workspace
after changing the authored sources or manifests.

## Variables

Setup-specific values are named in `AGENT_VARIABLES.md`, one `Name: value` per line. Read it at start; skills refer to variables by name.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `psyche/` before assuming.
