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

## Live proof

The complete topology was live-tested on Ouranos with the living's phone. The
Nix-owned service was active, the living paired the phone with
`codex remote-control pair`, and a TUI launched with
`codex --remote unix://` remained open in the terminal. After a short discovery
delay, the phone showed the daemon-backed sessions. A message sent from the
phone appeared in the same live terminal conversation.

The path remains experimental in Codex 0.149.1. The Nix-owned lifecycle is
deliberately different from the installer-owned lifecycle: do not run
`codex remote-control start`. The Home Manager service already runs the
remote-control-enabled app-server, and ordinary wrapped `codex` launches route
to `--remote unix://` automatically.

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
- Zeus deployment 75 TestActivation and deployment 76 ActivateNow terminal
  `Completed/Succeeded`; deployment 76 is Current.
- Live Zeus verification for both `li` and Bird: updated profiles expose wrapped
  `codex` and `direct-codex` 0.149.1, the Nix-owned user services are active with
  `Restart=always` and `UMask=0077`, the default sockets are mode `0600`, and a
  real WebSocket `initialize` exchange succeeded in each user's independent
  `CODEX_HOME`.

The declared activation route was rechecked and identified Zeus before the
state-changing deployments. No route substitution, reboot, manual
`remote-control start`, or Zeus phone pairing was performed.

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

## Recovered version from unlanded commit 7cf8a304216c (2026-08-27 22:09 UTC)

#\1 Codex phone Remote Control with a terminal TUI

#\1 Desktop-owned session result

Live testing on Ouranos established that Codex Desktop 26.820.60940 has its
own raw Codex 0.149.1 `app-server` child, connected to Desktop over stdio. It
is separate from the Nix-owned terminal daemon. For the tested thread, that
Desktop child was the active writer.

Desktop had persisted Remote Control as enabled for
`app_server_client_name='Codex Desktop'`. A prompt sent from the phone reached
the desktop-owned thread. Desktop-created sessions are therefore phone
accessible; this was not a failed-control case.

The briefly absent user bubble is a live synchronization limitation. Codex
durably records the user message, but 0.149.1 emits no ordinary live
`EventMsg::UserMessage` item notification. `turn/start` begins with an empty
item list, and Desktop's follower path does not optimistically insert its own
submitted turn. Assistant and tool events stream immediately; a later thread
hydration/read reconstructs the user message, matching the observed
screenshots.

The terminal daemon and the Desktop stdio app-server are separate local writer
domains. Both can independently enable Remote Control. Changing
`CODEX_CLI_PATH` to the terminal TUI wrapper is not a fix: it does not bridge
those domains and risks ownership/recursion collisions. This finding warrants
no Nix or runtime change.

#\1 Earlier managed terminal-daemon finding

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

#\1 Observations

- `codex remote-control start` starts the managed app-server daemon with Remote Control enabled; `pair` creates a short-lived manual pairing code.
- `codex --remote unix://` connects the TUI to the default local daemon socket at `$CODEX_HOME/app-server-control/app-server-control.sock`.
- The phone's Remote Control traffic and the terminal TUI therefore enter the same app-server, which owns the thread and distributes its notifications to clients.
- A plain TUI launched before the daemon uses an embedded app-server. No attach, rebind, or conversion command exists. Starting Remote Control afterward makes another process try to load the thread, producing the intentional `already has an active writer` rejection.
- Closing that TUI releases the lock. Its persisted thread can then be resumed through the daemon-backed TUI, but the original process itself was not converted.
- Bare foreground `codex remote-control` creates an ephemeral private socket and no terminal TUI; it is not the desired shared topology.
- `CODEX_REMOTE_CONTROL_DAEMON_AUTOSTART_DISABLED=1` is present in this flow's environment but absent from the installed Codex source and binary. Codex itself does not recognize it. An outer launcher may interpret it; that remains unknown.

#\1 Live proof

The complete topology was live-tested on Ouranos with the living's phone. The
Nix-owned service was active, the living paired the phone with
`codex remote-control pair`, and a TUI launched with
`codex --remote unix://` remained open in the terminal. After a short discovery
delay, the phone showed the daemon-backed sessions. A message sent from the
phone appeared in the same live terminal conversation.

The path remains experimental in Codex 0.149.1. The Nix-owned lifecycle is
deliberately different from the installer-owned lifecycle: do not run
`codex remote-control start`. The Home Manager service already runs the
remote-control-enabled app-server, and ordinary wrapped `codex` launches route
to `--remote unix://` automatically.

#\1 Nix-owned realization

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
- Zeus deployment 75 TestActivation and deployment 76 ActivateNow terminal
  `Completed/Succeeded`; deployment 76 is Current.
- Live Zeus verification for both `li` and Bird: updated profiles expose wrapped
  `codex` and `direct-codex` 0.149.1, the Nix-owned user services are active with
  `Restart=always` and `UMask=0077`, the default sockets are mode `0600`, and a
  real WebSocket `initialize` exchange succeeded in each user's independent
  `CODEX_HOME`.

The declared activation route was rechecked and identified Zeus before the
state-changing deployments. No route substitution, reboot, manual
`remote-control start`, or Zeus phone pairing was performed.

#\1 Sources

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
- Follow-up local runtime witness on Ouranos: Codex Desktop 26.820.60940's raw
  Codex 0.149.1 `app-server` child over stdio, and its persisted
  `app_server_client_name='Codex Desktop'` Remote Control state.
- Follow-up installed Codex 0.149.1 app-server protocol/source witnesses:
  `EventMsg::UserMessage` and the `turn/start` item payload; Desktop follower
  behavior was observed against that live protocol.
- No web sources were used for the Desktop follow-up.
