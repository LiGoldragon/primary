# Codex 6 / Flow rebootstrap inventory

Observed 2026-09-24 10:20–10:29 America/Mexico_City. This is a read-only
inventory. It neither exercised Flow nor contacted the app-server API.

## Current runtime

| Component | Observed state | Evidence |
| --- | --- | --- |
| Codex app-server | `codex-cli 0.153.4`; PID `1553993`; active since 09:35:28; command `codex app-server --remote-control --listen unix://` | `systemctl --user show/cat codex-remote-control.service`; `codex --version`; `/proc/1553993/cmdline` |
| App-server control edge | `/home/li/.codex/app-server-control/app-server-control.sock`, mode `0600`, owned by `li:users`; listener is PID `1553993` | `ss -lxnp`, `stat` |
| Flow Nexus | `flow 0.3.0`; PID `1635310`; active since 09:52:49 | `systemctl --user show/cat flow-nexus.service`; `/proc/1635310/exe` |
| Flow edges | `/run/user/1001/flow/flow.sock` and `flow-meta.sock`, each live and owned by PID `1635310` | `ss -lxnp` |
| Herdr | `herdr 0.8.2`; two independent servers: `default` (PID `807384`) and `messaging-build` (PID `3219203`) | `herdr session list`; `ss -lxnp`; `/proc/*/exe` |

The current Nix executables resolve to `codex-0.153.4`, `flow-0.3.0`, and
`herdr-0.8.2`. The installed `flow` and `flow-nexus` SHA-256 values observed
were respectively `f4a2cefc…421267` and `5accc445…ebedd7`.

## Model catalog and active named seats

The active Codex configuration declares `gpt-6-astra` at `xhigh`; its default
subagent model is `gpt-5.6-luna` at `xhigh`. The declared built-in profiles in
the deployed Home Manager source are default/explorer = Luna, worker = Terra.
`tools/native-seat-launch.mjs` additionally has explicitly guarded profiles
for `gpt-5.6-sol`, `gpt-5.6-luna`, `gpt-5.6-terra`, and `gpt-6-astra`; it
rejects live launch unless the exact recognized seat/profile/receipt conditions
hold.

Live foreground remote Codex clients include:

| Model | PID | Native thread short id | Finding |
| --- | ---: | --- | --- |
| Sol | `347255` | `01a0cefc` | remote resume on the current app-server socket, medium effort |
| Luna | `1154324` | `01a0bca3` | remote resume on the current app-server socket, medium effort |
| Terra | `1154423` | `01a0bca3` | remote resume on the current app-server socket, medium effort |

The `messaging-build` Herdr session currently exposes `field-medium-9ddcbc`
as a working Codex pane (`w0:p2`, terminal `term_65bef46ad013e44`), while
`mind-sol-flow-psyche`, `field-luna-recovery`, and `field-terra-recovery` are
done. Herdr's current Codex agent records do not include an `agent_session` or
native thread UUID for these panes. Therefore the listed Sol/Luna process
threads cannot be proved bound to a named Herdr agent from these observations.
The current Flow marker is `9ddcbc` and records Codex identity `01a0c051…bc64b`.

## Exact installed Flow interface and launch contract

`flow` has no flag interface: it accepts exactly one inline Datom. `--help`
and `--version` are rejected as invalid Flow queries. The checked source
revision is working-copy `wvumvxworzlu` / commit `b5c6bc05657d`; the installed
binary is the separately evidenced Nix `flow-0.3.0` derivation above.

The ordinary Signal contract (`flow/crates/signal-flow/src/lib.rs`) contains
only:

```
Start.{ <flow-type> <goal> { <parent-flow-id> <session> <turn> } }
Restart.{ <flow-id> <authority-flow-id> }
```

There is no `Respawn` variant. The current code recognizes only
`codex-medium` for `Start`; other flow types return `StartRejected`. A Start
persists a pending record, calls app-server `thread/start` with its fixed model,
then `turn/start`; only then returns `Started`. A Restart requires
`authority-flow-id == flow-id`, performs `thread/resume` and `turn/start`, and
only then records/returns `Restarted.{ <flow-id> <generation> }`. Failure is
represented as `StartRejected` or `RestartRejected`.

The Flow Nexus adapter opens `codex app-server proxy --sock
/home/li/.codex/app-server-control/app-server-control.sock`, then WebSocket
JSON-RPC `initialize`, `thread/start`/`thread/resume`, and `turn/start`. Its
compiled `flow-nexus` main fixes the launch model to `gpt-5.6-terra`, effort
`medium`, timeout 10 seconds, and store path
`/home/li/primary/flow/flow.sema`. It does not select Astra, Sol, or Luna.

The checked client source defaults to `/tmp/flow-nexus.sock` and
`/tmp/flow-nexus-meta.sock`, whereas the live daemon owns the `/run/user/1001/flow`
sockets. A caller must supply the live socket with `FLOW_SOCKET` (and
`FLOW_META_SOCKET` for the privileged client) unless the deployed client has a
different wrapper. This was not exercised.

## Controllers, ownership, and duplicate-launch blockers

`flow-nexus.service` is user-systemd managed with `Restart=on-failure`,
`RestartSec=2s`, and `Requires=`/`After=` `codex-remote-control.service`.
`codex-remote-control.service` has `Restart=always`, `RestartSec=2s`, and is
the sole observed listener for the app-server control socket. These services
are the active launch controllers.

The Flow source removes the configured socket pathname before binding it; it
does not implement a separate singleton lock. Manually starting a second
Nexus against the same configured socket can therefore disrupt the existing
listener rather than safely refusing. The socket permissions and systemd unit
ownership constrain ordinary users but do not supply a Flow-level duplicate
launch guard.

`flows/.9ddcbc.flow-id.lock` exists (mode `0600`, created with the marker on
2026-09-20). It is a zero-byte claim-marker companion; this inventory did not
establish an advisory/file-lock holder. The repository contains many such
historical markers. No read-only Flow query for registrations or locks exists
in the current two-variant ordinary Signal contract.

## Rebootstrap blockers

1. The live Flow Nexus launches only Terra through `Start.{ codex-medium … }`.
   It has no supported Start request that selects GPT-6 Astra, Sol, or Luna.
2. The exact request term is `Restart`, not `Respawn`; it resumes an existing
   Flow-owned thread and cannot create the requested named seats.
3. Flow's client default socket differs from the observed live socket. Use of
   a bare installed `flow` client is likely to reach stale/nonexistent `/tmp`
   paths unless the socket environment is set.
4. Neither Herdr's current agent listing nor Flow's ordinary interface proves
   a Sol/Luna native-thread-to-Herdr binding or exposes a registration record.
5. A second manually launched Nexus has no observed singleton refusal and may
   steal the socket pathname from the systemd-managed instance.

## Sources read

- `flow/crates/{flow,signal-flow,flow-nexus}/src/{main.rs,lib.rs,codex.rs,store.rs}`
- `tools/native-seat-launch.mjs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/{default.nix,flow.nix}`
- live `systemctl --user`, `ss -lxnp`, `ps`/`/proc`, `herdr session list`, and
  `herdr … agent get` observations described above.
