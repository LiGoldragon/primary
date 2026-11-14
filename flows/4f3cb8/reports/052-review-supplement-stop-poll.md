# 052 frozen-packet supplement — reminder stop polling

This supplements, without modifying, the frozen56-file packet e545c6c2d378be1a1c86eed9ea688096c8fd259e3e7059ce58f7a31e5e01d38c. It corrects the runtime consumer ledger's source association, not the approved policy ownership or shape.

ReminderPolicy.Scan replaces the reminder scan interval REMINDER_TICK at `crates/flow-nexus/src/reminding.rs:15–16`. ReminderPolicy.StopPoll replaces BOTH `Duration::from_millis(250)` uses at `reminding.rs:95–97`: the stop-responsive sleep and the corresponding spent-duration increment. The previous citation `store/reminder.rs:25–55` does not establish this polling consumer; it belongs to reminder firings/minutes arithmetic.

A waiting interval captures its committed Scan and StopPoll values together at its existing operation boundary. The sleep and spent increment use the SAME captured StopPoll duration; a mid-wait live change does not pair a prior sleep with a newly read increment. A later waiting interval uses the newly committed snapshot. Preserve the current loop's termination/comparison behavior; no new disabled state, hidden250ms, silent clamping or retry policy is introduced. Deadline/duration additions remain checked as already approved.

Oracle: with a deterministic fake clock/sleeper and a non250ms configured StopPoll, witness each sleep and corresponding spent increment use that exact value, stopping still checked at the existing loop points. Change committed policy during a wait: current interval retains its captured values, next interval observes new values. Separately vary Scan with StopPoll held fixed to prove distinct consumers. Invalid/absent-required values refuse configuration before effects under the already approved validation rules.

The source mapper must add this exact row and the fresh independent checker must re-pin this supplement and corrected row. No source body or prebody clearance is supplied here.
