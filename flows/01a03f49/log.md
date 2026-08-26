# Flow 01a03f49

Investigate and design use of the Codex phone app's built-in Remote Control with all Codex TUI sessions created by the living. The phone must join a conversation visible in a terminal and its messages must appear in that same TUI even while the terminal is active. Generic local message ingress such as `codex queue` is not the requested capability.

Open:

- Live proof with the Codex phone app has not been run.
- Whether the surrounding launcher interprets `CODEX_REMOTE_CONTROL_DAEMON_AUTOSTART_DISABLED`; Codex 0.149.1 itself does not.

Settled from installed Codex 0.149.1 source and CLI help: an ordinary already-running TUI cannot be attached or converted because its embedded app-server holds the writer lock. The intended shared topology is to start the remote-control-enabled managed daemon first, pair it to the phone, and run the terminal TUI as a client of that daemon. The phone and TUI then share the daemon's single writer. Exact recipe and limitations are in `reports/codexPhoneRemoteControl.md`.

Remembered: 019fe121, 019fe728, 1030529c, 01a0338f, 01a038be, 4ddc321d, aa4c7747 — depth 1. Prior work establishes the desire for inter-flow communication and distinguishes local app-server control from cloud Remote Control, but contains no ruling or proof that a phone can join an arbitrary active TUI.
