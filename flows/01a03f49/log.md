# Flow 01a03f49

Investigate and design use of the Codex phone app's built-in Remote Control with all Codex TUI sessions created by the living. The phone must join a conversation visible in a terminal and its messages must appear in that same TUI even while the terminal is active. Generic local message ingress such as `codex queue` is not the requested capability.

Open:

- Activate the already-realized CriomOS candidate on Zeus. The declared activation route `root@zeus.goldragon.criome` times out; using the reachable direct IP for activation requires a new routing decision.
- Live proof with the Codex phone app requires the living to complete pairing on the phone.

Settled from installed Codex 0.149.1 source and CLI help: an ordinary already-running TUI cannot be attached or converted because its embedded app-server holds the writer lock. The intended shared topology is to start the remote-control-enabled managed daemon first, pair it to the phone, and run the terminal TUI as a client of that daemon. The phone and TUI then share the daemon's single writer. Exact recipe and limitations are in `reports/codexPhoneRemoteControl.md`.

The living approved a corrected Nix-native realization: Home Manager owns a direct `codex app-server --remote-control --listen unix://` user service using the one existing Codex derivation. The standalone installer, managed mutable path, and updater are excluded. Deployment scope includes Zeus and bird's Zeus profile in addition to the relevant Ouranos/li state.

Realized and pushed: CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103` and CriomOS `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`. Materialized Ouranos and Zeus evaluations, configured remote builds, wrapper routing checks, embedded multi-user Home evaluation, aggregate Home package realization, and a real user-manager VM protocol/restart test passed.

Ouranos UserEnvironment deployment 72 completed successfully and is current. Live proof shows the service active, the default socket at mode 0600, two-client app-server initialization succeeding, and both wrapped and raw recovery Codex at 0.149.1.

Zeus deployment 73 Evaluate and deployment 74 Realize completed successfully. `TestActivation` and `ActivateNow` were not submitted because the declared activation route timed out before and after realization. The old live li and bird profiles remain active; both still lack the new active service. No endpoint was substituted and no reboot occurred.

Remembered: 019fe121, 019fe728, 1030529c, 01a0338f, 01a038be, 4ddc321d, aa4c7747 — depth 1. Prior work establishes the desire for inter-flow communication and distinguishes local app-server control from cloud Remote Control, but contains no ruling or proof that a phone can join an arbitrary active TUI.
