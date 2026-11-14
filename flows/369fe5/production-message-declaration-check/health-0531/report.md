# Stable 0531 health witness

Observed `2026-11-07T20:37:27-06:00`.

- Unit `flow-nexus-0531.service`: `ActiveState=active`, `SubState=running`, `MainPID=933207`, `ExecMainCode=0`, `ExecMainStatus=0`.
- `ActiveEnterTimestamp` and `ExecMainStartTimestamp`: `2026-11-07 14:22:24 CST`.
- `/proc/933207/exe`: `/nix/store/vnfcw4w5s0vi0gyb6w8h6kzisc2hpnh4-flow-configured-0.53.1/bin/flow-nexus`, unchanged from prior inventory.
- Ordinary socket `/run/user/1001/flow-0531/flow.sock`: socket mode 600, listener owned by `flow-nexus` PID 933207, fd 6.
- Meta socket `/run/user/1001/flow-0531/flow-meta.sock`: socket mode 600, listener owned by `flow-nexus` PID 933207, fd 4.
- Bounded journal scope: `journalctl --user -u flow-nexus-0531.service --since '2026-11-07 14:20:00'`, viewed through `20:37:31`; recent entries show admitted Notice/Question/Order records and accepted send-tool invocations. No exit/restart/error line appeared in the viewed tail.

This witnesses stable service state, executable identity, socket existence/listeners, and recent activity at the observation time. It is not a universal health claim. It does not query or touch private 0532, and does not establish application-level correctness beyond these observations.
