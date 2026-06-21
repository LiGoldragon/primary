---
title: 709 — Battery and lojix daemon pre-OMS review
role: system-maintainer
variant: Refresh
date: 2026-06-21
topics: [battery, lojix, deployment, pre-oms]
description: |
  Operational review of Ouranos battery charge limiting, the legacy lojix-cli
  archive/cutover, and the current daemon deployment state across Ouranos,
  Prometheus, and Zeus. Includes the manual follow-up list for the pre-OMS
  daemon runbook.
---

# 709 — Battery and lojix daemon pre-OMS review

## Intent anchors

[Ouranos should keep ThinkPad battery-care charge thresholds enabled for ordinary use, preferring the 75-80 percent conservation window over routine full charging.]

[Lojix is the production deploy path: execute the cutover now — the lojix daemon becomes production and legacy lojix-cli retires per node, standing down the parallel Stack A / Stack B burden.]

## Task list carried from the prompt

1. Investigate why the battery reached / was heading toward full charge.
2. Enable battery charge limiting if supported.
3. Remind the psyche how to toggle the battery-saving mode.
4. Start a pre-OMS manual / README review centered on `lojix-daemon`.
5. Deprecate and archive the old `lojix-cli`, marking where the migration went.
6. Check whether Ouranos, Prometheus, and Zeus are deployed onto the daemon stack.
7. Check whether daemon meta deployment still depends on a live root-SSH-capable user agent.

## Battery finding

Ouranos is a Lenovo ThinkPad T14 Gen 5 (`21MLS18Y00`) with a Celxpert Li-poly battery. The kernel exposes native ThinkPad charge-threshold controls:

- `charge_control_start_threshold`
- `charge_control_end_threshold`
- `charge_behaviour`

The deployed `battery-ctl` utility already exists and supports:

```sh
battery-ctl care    # 75-80 percent conservation window
battery-ctl full    # 90-95 percent near-full window
battery-ctl status  # show current thresholds, charge level, state
```

I enabled care mode during this pass. Final observed state:

- start threshold: 75%
- stop threshold: 80%
- battery level: 79%
- state: charging until it reaches the 80% stop threshold
- battery health: about 90.5% of design capacity
- cycle count: 171

The hardware supports the conservation behavior directly; this is not a fake software-only limit. The battery reaching 100% is therefore not evidence that the controller is intentionally recalibrating because it thinks the battery is old. The more likely cause is that the runtime threshold state reset to 0/100 after a sleep path, and the deployed reapply service did not run afterward.

## Battery root cause

`battery-charge-default.service` is enabled for:

- `multi-user.target`
- `suspend.target`
- `hibernate.target`

The machine actually used `hybrid-sleep` overnight. The boot/resume log shows the machine entering `hybrid-sleep` around 03:33 and returning around 08:48. After that resume, `battery-charge-default.service` did not run, because it is not wanted by `hybrid-sleep.target`. Before I manually re-enabled care mode, direct sysfs showed thresholds reset to start 0 / stop 100.

UPower briefly reported the old 75/80 threshold after sysfs had reset, which looks like a stale cached view. The reliable source is the sysfs files and `battery-ctl status`.

## Battery maintenance recommendation

The durable fix belongs in `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`:

- add `hybrid-sleep.target` to the battery threshold service `after` / `wantedBy` list;
- consider `suspend-then-hibernate.target` if that sleep path is used;
- optionally add a power-supply udev event hook that reapplies `battery-ctl care` when the battery/AC device appears or changes.

The event hook is preferable to polling: the positive mechanism is “apply care thresholds on relevant power/sleep events,” not periodic checking.

I did not edit CriomOS because `system-designer` currently has an active lock over `/git/github.com/LiGoldragon/CriomOS` and `/git/github.com/LiGoldragon/goldragon` for the live VM-host / lojix migration work.

## lojix-cli archive result

The legacy `lojix-cli` repo is now archived on GitHub.

Local doc changes landed first on `lojix-cli/main` in commit `4deeee54` (`archive lojix-cli docs for daemon cutover`):

- `README.md` now says the repo is archived and points to `github:LiGoldragon/lojix`.
- `INTENT.md` now says `lojix-cli` is the archived legacy deploy CLI and names the daemon replacement stack.
- `ARCHITECTURE.md` now states archive status and removes the pending schema-upgrade section as active work.
- `skills.md` now warns agents not to add new deploy behavior here.

Then GitHub archive was applied. The repository now reports `isArchived: true`. I attempted to update the GitHub description after archiving, but GitHub rejects metadata edits on archived repositories; the old short description remains there. The README carries the real migration pointer.

## daemon deployment state

### Ouranos

Ouranos is running the daemon stack.

Observed state:

- `lojix-daemon.service`: active and enabled.
- ordinary socket: `/run/lojix/ordinary.sock`.
- owner socket: `/run/lojix/owner.sock`.
- installed clients: `lojix`, `meta-lojix`, `lojix-daemon`.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` returns current HomeOnly generation rows.

The daemon service runs as user `li` and carries `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh`. That socket is currently present and has an SSH key loaded, so meta deploys can work while the user agent/session is alive.

### Prometheus

Prometheus is not running the daemon stack.

Observed state over root SSH:

- host is reachable and system state is `running`.
- `lojix-daemon.service`: unit not found.
- `/run/lojix`: absent.
- `lojix`, `meta-lojix`, `lojix-daemon`: not present in PATH.

This matches current cluster data: Prometheus has `TailnetClient`, `NixBuilder`, `NixCache`, and `VmHost`; it does not have `PersonaDevelopment`. CriomOS currently enables `lojix-daemon` only when the node has `PersonaDevelopment`.

### Zeus

Zeus could not be validated.

Observed state:

- DNS resolves `zeus.goldragon.criome` to its Yggdrasil address.
- ping gets no reply.
- root SSH to `zeus.goldragon.criome` timed out.
- the local Ouranos daemon query for `goldragon zeus` returns no generation rows.

So Zeus is currently either offline/unreachable from Ouranos, not participating on the expected network path, or blocked before SSH. I did not infer daemon state for Zeus without host access.

## Daemon operational caveat

The psyche's concern is accurate: the daemon is operational, but meta deployment currently borrows the live operator SSH agent. The service is started as `li` and gets `SSH_AUTH_SOCK` pointing at the user's GPG SSH agent. This works only while that runtime socket exists and contains the deployment-capable key.

That is not a final daemon identity model. A durable deploy daemon should get first-class machine identity / criome-mediated authorization rather than borrowing an ambient logged-in user agent. This is already aligned with the captured lojix/criome direction, but it is not solved on the running system.

## Pre-OMS manual notes

The manual should live in the active `lojix` repo, not in the archived `lojix-cli` repo. I could not edit `lojix/README.md` in this pass because `system-designer` currently has an active lock on `/git/github.com/LiGoldragon/lojix`, `signal-lojix`, and `meta-signal-lojix` for live deploy-into-VM work.

Suggested first manual sections:

1. **Status** — daemon stack is production on Ouranos; legacy `lojix-cli` is archived.
2. **Binaries** — `lojix-daemon`, `lojix`, `meta-lojix`, `lojix-write-configuration`.
3. **Sockets** — ordinary peer socket versus owner/meta socket, with authority split.
4. **Read-only query** — `lojix "(Query (ByNode (goldragon ouranos None)))"`.
5. **Privileged deploy** — `meta-lojix` request shape, with examples copied from the live schema/tests, not invented in prose.
6. **Host prerequisites** — target root SSH, cache/substituter expectations, and builder selection.
7. **Current caveat** — the daemon depends on `li`'s live SSH agent socket for root SSH; this is a temporary operator-session dependency.
8. **Current host state** — Ouranos active; Prometheus not installed by current role data; Zeus unreachable.

## Open follow-ups

1. Patch CriomOS battery threshold reapply for `hybrid-sleep.target` once the current CriomOS lock is free, then deploy Ouranos.
2. Decide whether `lojix-daemon` should run only on `PersonaDevelopment` nodes or on all named operator/cluster hosts. Current data explains why Prometheus lacks it.
3. Bring Zeus online or identify why root SSH over `zeus.goldragon.criome` is timing out.
4. Move the pre-OMS manual into `lojix/README.md` after the active `system-designer` lock clears.
5. Replace the daemon's ambient `SSH_AUTH_SOCK` dependency with first-class deploy credentials / criome-mediated machine identity.
