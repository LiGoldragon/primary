Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

## Skills

Authored skill sources are only the `*.md` files under `Curriculum skills`.
Identity and deployment selection are only `manifests/*.dotos`.
`.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
evidence; never edit them directly. Regenerate from the consumer workspace
after changing the authored sources or manifests.

## Variables

Skill variables are the values that differ between setups. They are set in @SKILL_VARIABLES.md, one `Name: value` per line, and referred to by name everywhere else.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `Vision/`, `psyche-raw/`, and `flows/*/vision/` before assuming.

## Temporary subagent model constraint

- Subagents must never use or inherit Sol.
- `fork_turns="all"` inherits the root model and prevents role/model overrides, so it must not be used when the root model is Sol.
- Spawn ordinary or exploration subagents with the configured Luna/xhigh default or explorer role, using `fork_turns="none"` or a bounded positive fork.
- Terra may be used only for actual implementation when explicitly appropriate and authorized by existing instruction.
- If a non-Sol model cannot be guaranteed, do not spawn the subagent.
