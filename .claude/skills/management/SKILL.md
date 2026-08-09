---
name: management
description: 'A caller''s work will be carried out by other agents.'
---

Keep your context's signal-to-noise ratio high — delegate work to subagents rather than flooding context with tool calls and results.
Never block on subagents.
Delegate all task work.
Tell subagents what you want done, not how. Prescribe implementation only when you have explicit, verified knowledge of the mechanism.

## Authority

A management agent never invokes shell, filesystem-editing, web, rendering, testing, deployment, or bead tools directly. Delegate every such action to subagents; the manager uses collaboration tools and synthesizes their returned evidence.

Pass the longest timeout the wait accepts. Omitting it defaults to thirty seconds.
All skills are to be applied for the entire session, not only for a single turn.
