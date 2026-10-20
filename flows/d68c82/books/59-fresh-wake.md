<!-- to-the-living:start -->
Presentation.{ «A sleeping flow wakes whole: report» }

# A sleeping flow wakes whole: report

Messages to a sleeping flow now work in production, on the new Flow release (0.35.10). One flow sent a message to a flow that was asleep. The sleeping flow woke as a fresh conversation, received every one of its context modules whole and exactly once, read the message with its sender's name on it, and answered that it was ready. Its queue then emptied and it went back to sleep.

## What now works

The sending flow, a Codex flow, started whole and sent the message during its very first turn. The message was queued for the sleeping flow with the sender's name attached.

The sleeping flow, a Claude flow, woke with all 36 of its modules. It was a new conversation, not the old one resumed. It ran on the small model at medium effort, answered ready without using any tools, and showed its proper name. Flow accepted the wake, put the flow back to sleep, and its queue was empty afterward.

An earlier try had stalled because Flow knew the model by its short name while the model reported its full name. Flow now records the full model names, and the wake was accepted. No code change was needed for this.

Before the wake, the production store was checked and read back complete, with nothing lost or set aside. All three services are running with no automatic restarts.

## One caveat

The earlier, refused try had already delivered the same message once. To finish the proof, Flow was restarted, and the message was delivered a second time. The message was harmless, so nothing went wrong, but delivering a message exactly once is not yet proven.

## What remains

| What | State | Who carries it |
| --- | --- | --- |
| Delivering a message exactly once | not yet proven | Flow's owner |
| A too-long message sent in parts | not yet proven on a real flow | Field |
| Archiving a start that failed | seen once by accident, not yet proven on purpose | Field |

Nothing here needs your ruling.
<!-- to-the-living:end -->
