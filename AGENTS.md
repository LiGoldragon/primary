# Primary Workspace Agent Instructions

## Agent Identity

- Codex is the operator agent.
- Claude is the designer agent.
- Before making edits, each agent must know which role it is acting as.

## Agent Lock Files

- Operator lock: `operator.lock`
- Designer lock: `designer.lock`
- The operator may edit only `operator.lock`.
- The designer may edit only `designer.lock`.
- The only exception is initial workspace setup, where the operator created
  both lock files.

## Lock Rule

Before editing files or running commands that create, modify, format, or delete
files, an agent must:

1. Write the intended scope into its own lock file with an `Updated-at`
   timestamp.
2. Read both lock files in the same tool call as that lock write.
3. Check whether the intended write scope overlaps another agent's active
   scope.
4. If there is overlap, remove the overlapping scope from its own lock file in
   the next tool call and stop before editing.
5. On a later attempt, repeat the same write-and-read step. If the other
   agent has removed or narrowed the overlapping scope, the agent may claim
   the scope again and proceed.

Use absolute paths where possible. For linked repositories under `repos/`, lock
the real repository path under `/git/...`, not only the symlink path. A whole
repository may be locked by listing its repository root path.

Locks are coordination records, not operating-system locks. Each agent is
responsible for keeping its own lock current and removing or narrowing active
scopes when work is finished.
