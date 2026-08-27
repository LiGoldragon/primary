# Flow 01a03f49

Investigate and design use of the Codex phone app's built-in Remote Control with all Codex TUI sessions created by the living. The phone must join a conversation visible in a terminal and its messages must appear in that same TUI even while the terminal is active. Generic local message ingress such as `codex queue` is not the requested capability.

Complete:

- The living paired the phone on Ouranos, launched a daemon-backed terminal TUI,
  observed all sessions appear after a short discovery delay, and sent a phone
  message into the same live terminal conversation.
- Zeus deployment 75 TestActivation and deployment 76 ActivateNow completed
  successfully through the declared route. Both `li` and Bird have updated
  profiles, active per-user remote-control services, mode-0600 sockets, and
  successful user-scoped WebSocket initialization witnesses. No reboot or route
  substitution occurred.

Settled from installed Codex 0.149.1 source and CLI help: an ordinary already-running TUI cannot be attached or converted because its embedded app-server holds the writer lock. The intended shared topology is to start the remote-control-enabled managed daemon first, pair it to the phone, and run the terminal TUI as a client of that daemon. The phone and TUI then share the daemon's single writer. Exact recipe and limitations are in `reports/codexPhoneRemoteControl.md`.

The living approved a corrected Nix-native realization: Home Manager owns a direct `codex app-server --remote-control --listen unix://` user service using the one existing Codex derivation. The standalone installer, managed mutable path, and updater are excluded. Deployment scope includes Zeus and bird's Zeus profile in addition to the relevant Ouranos/li state.

Realized and pushed: CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103` and CriomOS `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`. Materialized Ouranos and Zeus evaluations, configured remote builds, wrapper routing checks, embedded multi-user Home evaluation, aggregate Home package realization, and a real user-manager VM protocol/restart test passed.

Ouranos UserEnvironment deployment 72 completed successfully and is current. Live proof shows the service active, the default socket at mode 0600, two-client app-server initialization succeeding, and both wrapped and raw recovery Codex at 0.149.1.

Zeus deployment 73 Evaluate and deployment 74 Realize completed successfully.
After Zeus returned online, deployment 75 TestActivation and deployment 76
ActivateNow also completed successfully. Deployment 76 is Current. Live checks
proved the wrapped and raw recovery Codex 0.149.1 entrypoints, service policy,
socket permissions, and protocol initialization independently for `li` and
Bird.

Transcript hygiene incident: after the living asked to remove the displayed
manual pairing code, the root redacted the active local JSONL in place. A
delegated audit then correlated too broadly and redacted five related subflow
transcripts before stopping. The root transcript and four investigation
subflow transcripts remain valid JSONL; the audit worker malformed its own
active transcript during a concurrent rewrite. No marker-positive unrelated
user-history transcript was found, no secret value was printed by the audit,
and no speculative repair or deletion was performed.

Remembered: 019fe121, 019fe728, 1030529c, 01a0338f, 01a038be, 4ddc321d, aa4c7747 — depth 1. Prior work establishes the desire for inter-flow communication and distinguishes local app-server control from cloud Remote Control, but contains no ruling or proof that a phone can join an arbitrary active TUI.
