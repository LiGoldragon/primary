Landing work: questions held back for later.

**Work trees.** On one side:

> "everybody can have their own lightweight clone, like lightweight worktrees."

-- 18 September

On the other:

> "I do not want fucking work trees."

-- 3 October

**Branches.** On one side:

> "and youll need to branch the two signal repos as well."

-- 22 August

On the other:

> "I want everything merged on main, right? All the time."

-- 17 September

3. Does the queue need timed, reserved spots, now that there are no branches to rebase? The spots were described for branches.

6. Should Orchestrate ask Flow whether a holder is idle, and drop its locks by itself? That would make forfeiture automatic. Today it is done by hand.

7. Can the 215 branches on Primary's remote be deleted as they are? Or must any unmerged work in them be saved first? You asked for them removed, by Codex.

8. Does the publisher cover every repository, or only Primary? Other repositories are still pushed by hand.

9. Should Orchestrate, and Primary itself, get the stable and next rotation? Only Flow and Message have it today.
