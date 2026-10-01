# Flow component prototype proof

The prototype lives at `tools/flow-component` in the isolated proposal branch.
It is not a new Flow repository, installed service, durable unit, or deployed
Nexus daemon.

## Existing PTY comparison

`/git/github.com/LiGoldragon/terminal-cell` is version 3.0.1 and is the
existing low-level durable PTY: it owns a daemon process, transcript, control
and data sockets, and Ghostty viewer attachment. It accepts `LaunchCell`,
`SendLine`, `ObserveCell`, `AttachViewer`, and `CloseCell` through its own
Datom lifecycle CLI. The Flow prototype did not reimplement any of those PTY,
transcript, input-gate, or viewer capabilities. Its direct Ghostty path is a
bounded launch-mechanics stopgap because terminal-cell does not presently bind
the per-flow user scope and Claude bridge postflight as one Flow-owned record.
Any durable Flow implementation must select terminal-cell as its PTY backend
or explicitly replace it; it must not add another durable PTY.

## Component boundary

The CLI accepts exactly one inline Datom `Launch` or `Attach` object through
`datom-codec`; it has no convenience-word parser. `Launch` becomes a portable
binary `MetaSignal`, while `Attach` becomes an `OrdinarySignal`. A temporary
two-socket test binds ordinary mode `0660` and meta mode `0600` from the pinned
`nexus` crate's actual `SocketAuthority` API, transmits each Signal, and
restores the typed value. The temporary sockets are removed at test end.

This is a Nexus-shaped transport proof, not a bound daemon: it has no durable
store, peer-credential admission, running server, installed socket, or lifecycle
owner. `FutureLifecycleRecord::{Check,Recycle}` only reserves the data shape;
the prototype does not emit either record, wake an old flow, or write any old
flow log. The stated lifecycle policy remains future work: health/check can
recycle normally without waking the old flow; failure alone may request old-flow
help after the owner records why.

## Throwaway Haiku proof

The first attempt used split Ghostty flags (`--working-directory <path>` and
`--title <name>`). Ghostty reported configuration errors that each required an
assignment value, and Claude's recorded cwd became the component directory
instead of the requested flow directory. Its bridge and response are retained
as evidence that the scope/Claude path worked, but the first attempt is a
**failed launch proof** because the terminal configuration was invalid. The
renderer now uses `--working-directory=<path>` and `--title=<name>` and the
fixture asserts each is one argv token.

The corrected second proof used a fresh identity and was stopped after evidence
collection:

```text
flow: 9b8c1a
name: test-claude-9b8c1a
session UUID: 9b8c1a42-51c3-4f21-91c2-87a2efbd9513
unit: flow-9b8c1a.scope
model requested and recorded: haiku / claude-haiku-4-5-20251001
```

Its exact argv used the corrected assignment forms:

```text
systemd-run --user --scope --unit=flow-9b8c1a.scope --collect --no-block env -i HOME=/home/li PATH=<supplied-interactive-path> DISPLAY=:0 WAYLAND_DISPLAY=wayland-1 XDG_CURRENT_DESKTOP=niri:GNOME XDG_SESSION_TYPE=wayland XDG_RUNTIME_DIR=/run/user/1001 ghostty --window-inherit-working-directory=false --working-directory=/home/li/wt/primary-5f4fea-item30 --title="Claude test-claude-9b8c1a" -e bash -lc 'user_prompt=$(<"$2"); exec claude --session-id "$3" --name "$4" --remote-control "$4" --model "$5" --effort medium --dangerously-skip-permissions --append-system-prompt-file "$1" "$user_prompt"' flow-component <system-prompt> <user-prompt> 9b8c1a42-51c3-4f21-91c2-87a2efbd9513 test-claude-9b8c1a haiku
```

No Ghostty configuration error appeared. The session record had the exact UUID,
requested cwd `/home/li/wt/primary-5f4fea-item30`, name `test-claude-9b8c1a`,
and nonempty bridge ID `session_016rWUA1UvLj3fAUn4qtrkqu`. Its transcript said
remote control was active and recorded `FLOW_COMPONENT_HAIKU_OK`. Niri reported
Ghostty window 126, PID 1242518, title `Claude test-claude-9b8c1a`; the active
scope cgroup was `.../app.slice/flow-9b8c1a.scope` with Ghostty, Claude PID
1242552, and its intercom child. The Claude environment retained only supplied
HOME/PATH/display/XDG values and no `NO_COLOR`, `CODEX_CI`, or `CODEX_*` value.
The scope is now inactive.

The first test scope was also stopped:

```text
flow: 3e8d4b
name: test-claude-3e8d4b
session UUID: 3e8d4b71-4e8f-4ec0-9de0-0ce21a54a231
unit: flow-3e8d4b.scope
model requested: haiku
model recorded: claude-haiku-4-5-20251001
```

The rendered command was:

```text
systemd-run --user --scope --unit=flow-3e8d4b.scope --collect --no-block env -i HOME=/home/li PATH=<supplied-interactive-path> DISPLAY=:0 WAYLAND_DISPLAY=wayland-1 XDG_CURRENT_DESKTOP=niri:GNOME XDG_SESSION_TYPE=wayland XDG_RUNTIME_DIR=/run/user/1001 ghostty --window-inherit-working-directory=false --working-directory /home/li/wt/primary-5f4fea-item30 --title "Claude test-claude-3e8d4b" -e bash -lc 'user_prompt=$(<"$2"); exec claude --session-id "$3" --name "$4" --remote-control "$4" --model "$5" --effort medium --dangerously-skip-permissions --append-system-prompt-file "$1" "$user_prompt"' flow-component <system-prompt> <user-prompt> 3e8d4b71-4e8f-4ec0-9de0-0ce21a54a231 test-claude-3e8d4b haiku
```

Observed scope cgroup:

```text
/user.slice/user-1001.slice/user@1001.service/app.slice/flow-3e8d4b.scope
```

It contained Ghostty PID 1229300, Claude PID 1229355, and its intercom child,
all outside `codex-remote-control.service`. Claude's observed environment had
only the supplied HOME/PATH/display/XDG values: `NO_COLOR`, `CODEX_CI`, and all
`CODEX_*` values were absent. Niri reported Ghostty window 123, PID 1229300,
title `✳ test-claude-3e8d4b`. The local session record had the exact UUID, name
`test-claude-3e8d4b`, and nonempty bridge ID
`session_01DCcMGJKrS8wzfbLpPpacBn`; its transcript stated remote control was
active and the Haiku response was `FLOW_COMPONENT_HAIKU_OK`.

No local remote-list API or remote index entry was available to independently
observe the remote registration's name. The exact bridge/name remote-list
postflight remains **unverified**, so this is a successful launch-mechanics and
bridge-registration proof, not a completed remote-name postflight. The test
scope was stopped and is inactive. No production service was restarted.
