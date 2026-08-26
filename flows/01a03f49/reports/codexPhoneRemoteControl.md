# Codex phone Remote Control with a terminal TUI

## Earlier managed-daemon finding

Codex CLI 0.149.1 can give the phone app and terminal TUI one shared conversation only when a remote-control-enabled managed app-server daemon owns the conversation and the TUI connects to that daemon. An already-running ordinary `codex` TUI cannot be converted or attached because its embedded app-server already owns the thread.

```text
Codex phone ── OpenAI Remote Control relay ── managed app-server daemon ── thread
                                                   │
                                                   └── terminal TUI client
```

The installed command surface gives this recipe:

```sh
codex remote-control start
codex remote-control pair --json
codex --remote unix://
```

The pairing command prints a short-lived code for the phone. The lower-level equivalent is:

```sh
codex app-server daemon enable-remote-control
codex app-server daemon start
codex remote-control pair
codex --remote unix://
```

For a fresh managed Unix host, the daemon can instead be installed with:

```sh
codex app-server daemon bootstrap --remote-control
```

Once the default daemon socket exists, plain `codex` is also implemented to probe and reuse it, but `codex --remote unix://` states the desired topology explicitly.

## Observations

- `codex remote-control start` starts the managed app-server daemon with Remote Control enabled; `pair` creates a short-lived manual pairing code.
- `codex --remote unix://` connects the TUI to the default local daemon socket at `$CODEX_HOME/app-server-control/app-server-control.sock`.
- The phone's Remote Control traffic and the terminal TUI therefore enter the same app-server, which owns the thread and distributes its notifications to clients.
- A plain TUI launched before the daemon uses an embedded app-server. No attach, rebind, or conversion command exists. Starting Remote Control afterward makes another process try to load the thread, producing the intentional `already has an active writer` rejection.
- Closing that TUI releases the lock. Its persisted thread can then be resumed through the daemon-backed TUI, but the original process itself was not converted.
- Bare foreground `codex remote-control` creates an ephemeral private socket and no terminal TUI; it is not the desired shared topology.
- `CODEX_REMOTE_CONTROL_DAEMON_AUTOSTART_DISABLED=1` is present in this flow's environment but absent from the installed Codex source and binary. Codex itself does not recognize it. An outer launcher may interpret it; that remains unknown.

## Proof boundary

These are observations from direct CLI-help and installed-source reads performed through the local inspection subflow. The complete topology has not been live-tested with the living's phone, so the phone UX and pairing state remain unverified here.

The path is also still experimental and documented inconsistently: current developer-command and app-server documentation expose it, while the Remote Connections guide still says mobile setup begins in the ChatGPT desktop app and cannot be initiated from the CLI. It is therefore a real 0.149.1 mechanism, not yet a consistently promised stable product workflow.

## Nix-owned realization

Further source inspection established that `codex remote-control start` is not acceptable for this environment: it requires `$CODEX_HOME/packages/standalone/current/codex` and bootstraps an installer-owned updater. The realized design instead runs the existing single Nix Codex derivation directly:

```text
codex app-server --remote-control --listen unix://
```

Home Manager owns this as a per-user systemd service with `Restart=always` and `UMask=0077`. The normal interactive Codex entrypoint routes fresh, resume, fork, and agents TUIs to `unix://`; noninteractive/admin commands, ChatGPT's `CODEX_CLI_PATH`, and named recovery commands retain the raw pinned executable. Each user has an independent `CODEX_HOME`, socket, authentication, and pairing state.

CriomOS-home producer `ba0de9f84130c47a927a04723db2cb6f33b6b103` and CriomOS consumer `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f` are pushed. Proof includes:

- Ouranos and Zeus materialized evaluations and configured remote builds.
- A NixOS VM with a real user manager and home: service start, `0600` default socket, two concurrent WebSocket `initialize` clients, restart, and post-restart initialization.
- Embedded multi-user Home evaluation and a full aggregate Home package realization, preventing duplicate `bin/codex` providers.
- Ouranos deployment 72 terminal `Completed/Succeeded`, with matching live service and protocol evidence.
- Zeus deployments 73 Evaluate and 74 Realize terminal `Completed/Succeeded`.

Zeus activation remains open because `root@zeus.goldragon.criome` times out. The separately verified store route `root@192.168.18.95` was not substituted for activation without authority. No `TestActivation`, `ActivateNow`, reboot, or phone pairing was performed on Zeus.

## Sources

- Installed Codex CLI 0.149.1 help: `codex --help`, `codex remote-control --help`, `codex app-server daemon --help`.
- Installed source `codex-rs/cli/src/remote_control_cmd.rs`.
- Installed source `codex-rs/tui/src/lib.rs`.
- Installed source `codex-rs/thread-store/src/local/writer_lock.rs`.
- [Codex app-server documentation](https://developers.openai.com/codex/app-server).
- [Codex developer commands](https://developers.openai.com/codex/developer-commands#codex-remote-control).
- [Codex Remote connections documentation](https://developers.openai.com/codex/remote-connections).
- [Active-writer implementation](https://github.com/openai/codex/blob/main/codex-rs/thread-store/src/local/writer_lock.rs).
- [Documentation contradiction issue #35928](https://github.com/openai/codex/issues/35928).
- CriomOS-home revisions `6a50a32de49c`, `59c55dcfcee2`, and final `ba0de9f84130c47a927a04723db2cb6f33b6b103`.
- CriomOS final consumer `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`.
- Lojix deployments 72, 73, and 74.
