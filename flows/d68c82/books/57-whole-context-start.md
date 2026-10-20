<!-- to-the-living:start -->
Presentation.{ «A flow starts whole: report» }

# A flow starts whole: report

Starting a flow now works in production. On the new Flow release (0.35.5), one Claude flow and one Codex flow were started for real, each received every one of its context modules whole and exactly once, and each answered that it was ready.

## What now works

The Claude flow got all 36 of its modules, including the one its book work depends on. It ran on the small model at medium effort, answered ready, and showed its proper name. Tools it needs were there; the tools and context it should not have were absent. It then fell asleep as intended.

The Codex flow got all 34 of its modules, answered ready, registered itself, and showed its proper name in its pane. The exact conversation it opened was matched and accepted by Flow.

Before the start, every check on the running services passed, the production store read back complete with nothing lost or set aside, and no service restarted. Nothing was replayed, and no older record was written over the new ones.

One gap found in the previous attempt is also closed in the code: a flow that falls asleep before it finishes registering is now kept as started and is never started twice. That fix is tested but not yet released.

## What remains

| What | State | Who carries it |
| --- | --- | --- |
| Waking a sleeping flow fresh | held until one Codex wake check is done | Flow's owner |
| Messages to a sleeping flow | the link between the messenger and sleeping flows is not yet in production | Mind |
| A too-long message sent in parts | not yet proven on a real flow | Field |
| Archiving a start that failed | not yet proven on a real flow | Field |
| Releasing the falling-asleep fix | written and tested, waiting to be released | Flow's owner |

Nothing here needs your ruling.
<!-- to-the-living:end -->
