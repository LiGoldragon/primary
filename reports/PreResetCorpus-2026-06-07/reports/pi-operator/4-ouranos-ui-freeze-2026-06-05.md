# Ouranos UI freeze incident investigation

Date: 2026-06-05
Role: pi-operator
Host: `ouranos`
Incident window: previous boot ending at about 14:59:50 CEST

## Summary

The previous boot did not show a kernel panic, kernel OOM kill, watchdog lockup, or clean shutdown. It ended after a user power-key event at 14:59:40 and then a new boot started at 15:00:23. The logs show a graphical-session starvation event: Niri/libinput reported one input-processing backlog sample of 20.8 seconds at 14:56:38, and systemd-journald began logging repeated memory-pressure cache flushes from 14:57:47 through the hard reboot. Psyche observation corrects the severity framing: the visible UI/input freeze was not merely 20.8 seconds; it was minutes-long, roughly five minutes or more, with touchpad movement still waiting to be processed.

The most likely trigger was the `lojix-run` `HomeOnly Build` smoke I started for `bird` on `zeus`. That run began at 14:29:55 and was still writing stderr at 14:58:36. It had planned 54 local derivation builds plus a 3.3 GiB unpacked closure fetch, and it was copying many paths from the Prometheus substituter with repeated 5–6 second download timeouts. That overlapped the first Niri lag reports, PipeWire underruns, and the final memory-pressure cluster.

The strongest contributing factor is that `ouranos` has no swap. `systemd-oomd` logged at boot that memory-pressure handling is degraded without swap. Under combined agent load plus Nix copy/build/eval pressure, the compositor and audio stack were not protected from starvation.

A secondary active problem was a broken `persona-spirit-daemon-v0.1.1.service` restart loop. It had reached restart counter 29,385 by 14:58:06 and was still looping after reboot. Each instance was small, so it is unlikely to be the sole cause of a whole-UI freeze, but it produced continuous process churn and log volume during the incident. I stopped that old failing side-by-side user service at runtime after reboot; current production/newer Spirit daemons remained running.

## Evidence

### Boot and shutdown evidence

- Previous boot: 2026-05-28 13:55:47 through 2026-06-05 14:59:50.
- Current boot: started 2026-06-05 15:00:23.
- Last previous-boot marker relevant to the hard reboot: `systemd-logind` recorded `Power key pressed short` at 14:59:40.
- No matching kernel log evidence was found for OOM kill, kernel panic, soft lockup, hung task, GPU reset, thermal shutdown, or watchdog reset.

### UI starvation evidence

Niri/libinput reported that the compositor/input processing was falling behind. These are sparse journal samples and lower bounds, not a complete measurement of how long the graphical session felt frozen:

- 14:50:28 — event processing lagging by 51 ms.
- 14:50:56–14:50:58 — timer events lagging by about 2.7–2.9 seconds and event processing lagging by 1.18 seconds.
- 14:56:38 — event processing lagging by 20.8 seconds.
- 14:58:59 — touchpad frame errors, likely after the session had already become badly delayed.
- Psyche observation after the first report: the user-visible Niri/touchpad backlog was roughly five minutes or more, with movement still not visibly processed. The 20.8 second log line should therefore be treated only as a logged symptom, not as the duration of the freeze.

PipeWire logged many ALSA broken-pipe/resync messages starting at 14:52. This is consistent with realtime/audio starvation under system pressure, not with a single isolated webcam or camera package issue.

### Memory pressure evidence

`systemd-journald` logged `Under memory pressure, flushing caches` repeatedly in the final minutes:

- 14:57:47 and 14:57:51.
- 14:58:06, 14:58:39, 14:58:43, 14:58:47.
- 12 times in the 14:59 minute before the hard reboot.

Earlier in the previous boot, memory-pressure messages were sparse and clustered around unrelated earlier moments. The final cluster is therefore incident-specific.

Current boot memory/swap state:

- 30 GiB RAM.
- 0 B swap.
- `systemd-oomd` warns that memory-pressure usage is degraded with no swap.

### `lojix-run` evidence

Run directory:

`~/.local/state/lojix-runs/20260605122955-homeonly-zeus/`

Request:

`HomeOnly goldragon zeus bird ... CriomOS-home rev 4d202ba64dff... Build None None`

Key findings from the run logs:

- Started at 14:29:55.
- `stdout.log` stayed empty.
- `stderr.log` was last modified at 14:58:36, so the run was still active during the freeze window.
- Nix planned 54 local derivation builds.
- Nix planned 156 fetched paths, 3.3 GiB unpacked.
- The fetch set included broad graphical/profile packages such as `cameractrls`, OBS, Krita, GIMP, Calibre, and libvirt-related packages, plus side-by-side Spirit service derivations.
- The substituter fetches from Prometheus were timing out repeatedly around the tail of the log.
- Only one explicit local `building ...` line appears before the last written log line.

This means the intended “small HomeOnly Build smoke” was not small on this machine. It was a broad profile closure operation under a cache state where many packages had to be fetched/unpacked and some derivations still had to build locally.

### Spirit v0.1.1 restart loop evidence

Previous boot final window:

- `persona-spirit-daemon-v0.1.1.service` was repeatedly starting, failing with `InvalidDaemonConfiguration`, and restarting.
- Restart counter reached 29,385 at 14:58:06.
- Individual service runs were low memory, but some consumed seconds of CPU over tens of seconds of wall time.

After reboot:

- The same old service resumed the restart loop.
- I stopped it at runtime with `systemctl --user stop persona-spirit-daemon-v0.1.1.service`.
- The active production/newer Spirit services stayed running.

## Likely cause

The incident was a severe resource-starvation failure, not a kernel crash. The proximate workload was the HomeOnly `lojix-run` build/eval/copy for `bird` on `zeus`, started by this agent. It ran concurrently with several other agent sessions and existing user services. On a no-swap laptop/desktop session, the Nix operation’s closure fetch/unpack/build pressure plus agent load was enough to starve Niri and PipeWire for a user-visible minutes-long interval.

The `persona-spirit-daemon-v0.1.1` restart loop was not large enough to explain the freeze alone, but it made the system dirtier: constant process starts, failures, and journal traffic during the same pressure window.

## What was ruled out

- No kernel OOM kill found.
- No panic/BUG/Oops/soft-lockup/hung-task log found.
- No clean shutdown sequence found before reboot.
- No evidence that `cameractrls` itself crashed the UI. The issue was the broad Home profile build/fetch path, not the webcam-control package at runtime.
- No evidence that Home activation ran; this was the `Build` smoke, not `Activate`.

## Immediate mitigation already applied

- Stopped the broken old `persona-spirit-daemon-v0.1.1.service` runtime restart loop after reboot.
- Left the pushed `cameractrls` commits intact; both CriomOS-home and CriomOS working copies are clean.
- Did not resume the HomeOnly deployment after the freeze.

## Recommended follow-up

1. Add swap or zram on `ouranos`. Without swap, systemd-oomd is degraded and graphical sessions have little grace under build/eval pressure.
2. Put agent and Nix build workloads in resource-limited scopes: lower CPU/IO priority and memory ceilings for interactive-session agent work.
3. Make `lojix-run` resource-safe by default on interactive machines: `systemd-run --user` scope, low IO/CPU priority, explicit timeout/progress heartbeat, and possibly an option to require confirmation when the planned closure is multi-GiB or includes many local derivations.
4. Add a preflight check before any deploy/build smoke that reports planned build/fetch counts and asks before continuing if the machine is interactive and under active multi-agent load.
5. Fix or retire side-by-side old Spirit daemon slots so a failed legacy daemon cannot restart forever. At minimum add `StartLimitBurst`/`StartLimitIntervalSec`; better is to disable broken obsolete slots by profile generation.
6. Prefer remote builders or the target/Prometheus for heavy closure realization when the operator workstation is the active UI machine.
7. Pause further Zeus HomeOnly activation until the resource-safety changes or an explicitly quiet window.
