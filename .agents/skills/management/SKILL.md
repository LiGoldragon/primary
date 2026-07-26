---
name: management
description: 'Use when coordinating delegated work for a caller.'
---

Reserve your context for managing subagents.
Use no tools except subagent coordination.
Delegate all task work.
Do other work while agents run.
Return a synthesis to the caller.

Keep a wait active while agents run; you are resumed only through it.
Pass the longest timeout the wait accepts. Omitting it defaults to thirty seconds.
A psyche message interrupts the wait immediately, so a long wait costs no responsiveness.
Say nothing when a wait returns with nothing finished.
