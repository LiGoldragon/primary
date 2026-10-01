`Presentation.{ «The cluster never blocks itself» }`

**Why Sonnet was stuck.** Even with permission checks bypassed, Claude Code still asks before deleting files somewhere that looks dangerous. My guess is that "delete every PNG under a folder named by a variable" read as "delete at the root" and triggered that check. That is not confirmed yet. The question waited in Sonnet's pane until someone answered it, 83 minutes later.

**The fix in one place.** A hook in the Claude launcher answers every permission question the moment it appears, so nothing ever waits on a person. Whatever your policy doesn't allow is refused with a reason, and the flow rewrites its command straight away.

**Seeing it.** Flow already knows when a seat is waiting like this. That moment should go as an event to the seat's Mind, without anything polling for it.

**Your ruling.** When the hook meets a question your policy doesn't cover, should it allow it, or refuse it with a reason?