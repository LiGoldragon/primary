# Remote access to Codex Flows in Herdr panes — options (Psyche High 752e0f)

Read-only research. Nothing launched, attached, prompted, or changed.

## Option 1 — Herdr `--remote` / `session attach` (SSH-based)

What the living would do: SSH into this host (ouranos), then run
`herdr session attach messaging-build` (or `herdr --remote <ssh-target>`
directly from the phone's own client, which internally does the same).

`herdr --help` confirms `--remote <ssh-target>` and `herdr session attach
<name>` as real subcommands; no separate web/API client for Herdr is
advertised in `herdr --help` beyond the socket `api` subcommand (local use).

What must be true on the host: this host must be SSH-reachable from the
phone. Per `flows/836818/reports/prometheus-topology-2026-09-23.md` and
`flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`, SSH (tcp/22) is
open on Prometheus's WAN-facing link from Ouranos today, but those reports
describe the Ouranos↔Prometheus↔Zeus chain, not a path from an external
phone to Ouranos itself; no record read here establishes that this host
(ouranos) accepts inbound SSH from outside the LAN/Yggdrasil today.
Unknown: whether the living's phone can already reach ouranos over
Yggdrasil or LAN for SSH — not established by the documents read.

## Option 2 — Codex Remote Control (Codex phone app) — works today, proven

What the living would do: open the Codex app on the phone and pair (the
living already did this once: `codex remote-control pair`, on-host, printed
a short pairing code; codex TUI sessions then appeared on the phone).

`codex remote-control --help` and `codex app-server daemon --help` (this
host) show `start`/`pair`/`enable-remote-control`/`bootstrap` (the last
explicitly "Install durable local app-server management for SSH-driven
use"). Live on this host now: `codex-remote-control.service` is
`loaded active running` ("Codex Remote Control app-server"), backed by a
Unix socket (`~/.codex/app-server-control/app-server-control.sock`), not a
TCP listener — confirmed by `ss -tlnp` (no codex TCP listeners) and the
socket file's `srw-------` mode. `tools/native-seat-launch.mjs` (line 99,
and its check at line 250) launches Codex flows against this same
`app-server-control.sock`, i.e. Herdr-hosted Codex Flows attach to the
identical daemon the phone pairs with — not a separate, unreachable
process.

Earlier record, verbatim, `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`:

> "I'm trying to use the remote control feature in the Codex app on my
> phone, and right now I cannot connect to a session that is essentially
> running in a terminal somewhere."

> (after the Nix-owned always-running app-server design was proposed)
> "ok, lets do that."

> (2026-08-27, after completing the proof) "ok everything works! we got
> it!"

So this exact request — reaching Codex sessions from the phone — was
already built, deployed (Ouranos and Zeus), and the living confirmed it
working on 2026-08-27. What is unknown: whether that pairing still holds
today, and whether it shows the specific `messaging-build` Herdr panes (not
re-tested here; read-only brief).

## Option 3 — Claude Code Remote Control (today's working baseline for Claude)

`flows/01a04524/vision/claudeRemoteControl.md` records the living aiming
Claude's remote control at the same design as Option 2 ("session 01a03f49
has the right design ... try to aim for the same design with claude") — i.e.
Option 2 is explicitly the model Claude's own working Remote Control was
built to match. Not itself a route to Codex.

## Answer in plain words

Two options exist. Option 1 (SSH + `herdr session attach`) needs host
reachability that is not established as true today from a phone. Option 2
(Codex's own phone Remote Control app) is already built, already deployed
on this host, its app-server daemon is running now, and Herdr-hosted Codex
Flows (launched via `tools/native-seat-launch.mjs`) attach to that same
daemon — so it works today with nothing new, and the living already
proved it working once, in the living's own words: "ok everything works!
we got it!"
