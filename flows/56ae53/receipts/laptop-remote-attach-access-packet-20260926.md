# Laptop remote-attach access packet

Scope: a bounded, read-only access packet for the living's laptop. It does
not attach a remote Herdr client, inspect a remote session or pane, create a
session, or alter any local service.

## Supported command shape

The installed `herdr --help` and `herdr --remote li@100.64.0.2 --session
default --help` both state this supported shape:

```sh
herdr --remote <ssh-target> [--session <name>]
```

The installed Herdr version is `0.8.2`. The intended default-session command
is therefore syntactically supported:

```sh
herdr --remote li@100.64.0.2 --session default
```

For the named recovery context, the syntactically corresponding form is:

```sh
herdr --remote li@100.64.0.2 --session recovery-56ae53
```

This packet does not claim that the laptop can authenticate, that either
remote session exists, or that an attach will succeed. It records command-line
syntax only.

## Messenger registry session map

The assigned current registry map is:

| Session | Seats |
| --- | --- |
| `default` | `8904b1`, `dc53b4`, `38f337`, `6fe957`, `139366`, `184bd8`, `9ac67c`, `22e12b` |
| `recovery-56ae53` | `c56100` |

The existing recovery roster independently corroborates the eight listed
`default` seats as the Fable, Opus, Sonnet, Mind Astra, Mind Luna, Field Luna,
Field Sol, and Field Astra seats. This is a Messenger registry map, not a live
remote Herdr session read.

## Route evidence and boundaries

Current local Tailnet evidence identifies this host as `ouranos` with
`100.64.0.2`; `ip route get 100.64.0.2` resolves through the local loopback
route. SSH configuration resolves `li@100.64.0.2` to user `li`, port `22`.
The earlier `remote-access.md` witness records that a read-only self-SSH probe
to that address reached Ouranos and read local Herdr status. These facts prove
the Ouranos self-route only. They do not prove the living's laptop path,
laptop Tailnet membership, laptop SSH identity, or remote attach.

No `HERDR_ENV` value was present for this work. No session or pane inspection
was attempted.

Prometheus remains unreachable from Ouranos: current Tailnet status marks the
peer offline, consistent with the existing recovery summary. This is separate
from the local Ouranos route and does not imply anything about laptop access.

## Evidence grade

The command syntax and local Tailnet identity are direct local observations.
The registry map is the scoped coordination input corroborated in part by the
existing eight-seat roster. Laptop remote attach and the named recovery session
remain unverified until the living performs the attach from the laptop.
