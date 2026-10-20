# Idle panes stay open: references (unrendered)

Asked by the living: whether a Primary's pane should close after every turn that leaves its queue empty.
His words, direct speech 2026-10-19: "Closing panes when they're done is a long-term thing. We don't have to do that right now."

## Code witnessed
- flow origin/aa034f-next 2c390fb (not yet pushed with the keep-open change): crates/flow-nexus/src/waking.rs lines 1548-1563, the match on Operation::Sleep reached when the queue is empty and the lock is free; sleep() at ~1052 closes the pane (Operation::Close) and records the flow Stopped and the metaflow Asleep.
- crates/flow-nexus/src/codex_turns.rs only decides when a Codex thread rests (TurnEvent::Status Idle -> ThreadTurn::Resting); it holds no close, so no line of it is shown.
- psyche-context origin/main vision/flow.md line 27 (sleep line), 33-35 (wake lines), 57 (short-term marker "Short term, a Primary is not started without its Secondary").
