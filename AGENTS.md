# Primary Workspace Agent Instructions

## Agent Identity

- Codex is the operator agent.
- Claude is the designer agent.
- Before making edits, each agent must know which role it is acting as.

## Orchestration Protocol

Autonomous agents MUST read `protocols/orchestration.md` before editing files
or running commands that create, modify, format, or delete files.

The protocol coordinates:

- Role-owned lock files: `operator.lock` and `designer.lock`.
- The workspace BEADS task database: `.beads/`.
- The helper command: `tools/orchestrate`.

Use `tools/orchestrate claim <operator|designer> <path> [more-paths] --
<reason>` before edits. The helper writes the agent's own lock file, reads both
lock files, lists open BEADS tasks, and rejects overlapping active scopes.

Use `tools/orchestrate release <operator|designer>` when the scope is finished
or no longer active.

## No harness-dependent memory

Memory and persistent agent state belong in workspace files — `skills/`,
`lore/`, `reports/`, `protocols/`, repo `skills.md`, repo `ARCHITECTURE.md`,
or `.beads/` while bd is the active coordination substrate. **Don't use
harness-dependent memory systems** — e.g. Claude Code's per-session memory
files at `~/.claude/projects/<workspace>/memory/`, or any agent-private state
store an outside agent cannot read.

**Why:** memory tied to one harness is invisible to every other harness
and to the human. The workspace's truth must live in files every agent can
open. If you learn something durable, write it to the right workspace file
(per the skill-editor and report conventions); never to harness-private
state.
