Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

## Skills

`.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
evidence; never edit them directly. Regenerate from the Curriculum skills
after changing the authored sources or manifests.

## Variables

Skill variables are the values that differ between setups. They are set in @SKILL_VARIABLES.md, one `Name: value` per line, and referred to by name everywhere else.

## Committing

Primary is always committed: commit and push what you edited before
going idle. Dirty changes found in the tree are committed first, as
their own commit.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `Vision/`, `vision-raw/`, and `flows/*/vision/` before assuming.

## Temporary subagent model constraint

- Subagents must never use or inherit Sol.
- `fork_turns="all"` inherits the root model and prevents role/model overrides, so it must not be used when the root model is Sol.
- Spawn ordinary or exploration subagents with the configured Luna/xhigh default or explorer role, using `fork_turns="none"` or a bounded positive fork.
- Terra may be used only for actual implementation when explicitly appropriate and authorized by existing instruction.
- If a non-Sol model cannot be guaranteed, do not spawn the subagent.

## Codex Instruction Overrides

Skills loaded by the user (with $skill-name) are to be applied for your entire session, not only for a single turn, but you should not automatically instruct subagents to read them.
