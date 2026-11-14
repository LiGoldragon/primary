# Psyche criomos Opus 6670d4: handover, 2026-11-10 17:30 CST

Full log: flows/6670d4/state.md. Deploy requests: flows/6670d4/deploy/.

## Waiting on a word or an event
- **l33p (Task, open):** one proof run of the harness updater on the Lojix watch, HELD by Psyche core Opus until the living is back and prometheus serves builds.
  - The updater (CriomOS harness-update.nix, a09e39e and later) opens WatchDeployments before submitting, reads the watch to its own terminal, then moves the mains and activates.
  - Lojix 0.10.6 streams live on ouranos; the watch was proven by Realize and ActivateNow 400 to 407.
  - Then send Done l33p with lojix 321682e (0.10.6), signal-lojix 0.11.0 bd5d250, meta-signal-lojix 0.12.0 1b0aaeb and the CriomOS revision.
- **Living plug-in tests (6fx6, CriomOS 4400906):**
  - The Pixel tether should come up under NetworkManager on ouranos with no step from him.
  - nm-applet should give a Wi-Fi password prompt (untested).
- **tiger:** unreachable; deploy li's Home and host there when it is announced back online, never by retrying.
- **Uplink vendor list into Horizon:** cancelled (6fx6). The roles are a udev classification; no contract change.

## Live state
- **ouranos:**
  - CriomOS 4400906 (Lojix 402/403), boot default the same line.
  - BIOS 1.19 is flashed.
  - Runtime /run/systemd/logind.conf.d/90-trip.conf (lid and suspend key are plain suspend while he travels) is to be removed when he is back.
- **prometheus:** CriomOS 4400906 (Lojix 404 to 407; stage 73e2e08 on branch usb-role-stage-6670d4).
- **zeus:** CriomOS a09e39e, li Home at 9bd9fb6 (Home 393/394).
- **Psyche core Opus asked for the cause of prometheus's 17:12 reboot (p3bz):** Result sent. An abrupt hard reset or power loss, no trace in the OS, cause unknown.
- **Waiting on deployments:** use `scratchpad/await-watch.sh <request> <node>` (opens a watch, submits, reads to terminal). Never re-query on a timer.

## For the successor, lower priority (from the living through Psyche core Fable, 3vj7; report to Psyche core Fable)
- **Theme:** the theme goes dark at the wrong hour on ouranos (about 17h in Oaxaca), because the location provider (GeoClue, used by chroma-daemon) never worked.
  - Set the location to Oaxaca in the host data for ouranos and zeus, so the theme switches at the right time. Find where chroma reads a fixed location, and whether Horizon has a location field (NodeDefinition has Option<FixedLocation>).
  - Say what it would take to make the location provider work.
  - Look at why the theme switch looks wrong in the Claude terminal interface when it changes.

## Audit
flows/a59d6f/criomos-audit.md: 5 and 6 belong to the Flow line, 8 to Curriculum's owner, and 11 and 12 await Fable's ruling. Everything else is done.

## Flow client
`flow-nexus` (0.54); a Result or Done names the request id. Refresh with `flow-nexus 'Refresh.{ Psyche criomos Opus }'`.
