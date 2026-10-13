---
description: A command could stop a seat while awaiting living approval.
dependencies: []
---

A destructive command names its paths through guarded variables, ${VAR:?}, or literal paths, and never reaches a path outside the scratchpad or the flow's own directory.
A removal that Claude Code would still hold for approval is denied by the PermissionRequest hook in the home configuration, with the message "Destructive commands name their paths through guarded variables, ${VAR:?}, or literal paths, never outside the scratchpad or the flow's own lane; rewrite the path and run again."
