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
