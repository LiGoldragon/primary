# Semantic closure supplement

Correction: `PollingPolicy.AgentStop` actual production symbol is `Reminding::keep_reminding` `crates/flow-nexus/src/reminding.rs:91-99`; `REMINDER_TICK` is `:16` (5 seconds), while `:95-97` sleeps 250ms and increments `waited` by 250ms. `ReminderPolicy.Scan` is `REMINDER_TICK`; `ReminderPolicy.StopPoll` is the 250ms sleep/increment compound expression, not `store/reminder.rs:25-55`.

Remaining exact rows requiring Core/author review:

- RetryPolicy.RetryMultiplier: no constant; observed compound `wait = (wait * 2).min(Self::LONGEST_WAIT)` at `flow-nexus/src/send_tool.rs:610`, owner `PacesReconnection::respond_for`; question is only whether authored field replaces literal multiplier.
- FramePolicy.Nexus: exact literal/consumer requires source context at `flow-nexus/src/lib.rs:1389`; classify against the RuntimePolicy validation proposal before body.
- LaunchPolicy.FlowIdentity/ClaudeHome/FlowDirectory: proposal names are authored leaves, but exact current fallback branches are compound `herdr.rs:143-198`; no single constant exists.
- ParserPolicy five leaves: current Nexus Budget construction is repeated at `flow-nexus/src/main.rs:55-62,361-368,508-515,625-632`; each leaf maps to a distinct Budget field/check, no missing receiver.
- Existing Minutes: `RulesMinutes::ruled_interval` and `TASK_REMINDERS` are separate existing semantics (`store/reminder.rs:27,34-50`); DefaultMinutes family is `store.rs:1154-1205`. Absence/read failure must remain typed refusal; no runtime default claim.
- Existing HarnessProfiles/LeaveOuts: exact retained records are `store.rs:298,342` and `store.rs:1295-1421`; validation/refusal paths remain existing family behavior.

Codec identity receipt with `GIT_OPTIONAL_LOCKS=0`: prepared Datom HEAD `4dff16b4f7412febc3b71aac8b49680cd20988cb`, Protos HEAD `15b41da8f2579e73ead59bc0c2b97529b8ac32d3`; prepared worktrees clean. Cached checkout file hashes match prepared roots: Datom `src/core.rs bafb29f33af6da57497f978eb3d7e4014a48bc65f619b3ea5e609cd00bddf005`, `src/composition.rs f67e48ae697a7352a4162356c22c738b5d499291629868896b89aa76b9b56dfd`; Protos `src/core.rs 4bd622e0416ddbc83bc07ce1b310ac9316384fa5876e5fbe7a95f4500575d925`. Cached checkouts have untracked `.cargo-ok`; no source difference.

Exact unresolved adapter/codec gaps are only future generated field constructors and external test fixture migration; no broad receiver search remains claimed beyond the attached artifacts.
