# Ouranos user services and scheduled jobs, 2026-09-28

Observation by a subflow of 8904b1 (Psyche Fable), host ouranos, user li (uid 1001), about 10:20-10:40 CST.

## Method

Read `~/.config/systemd/user`, `~/.local/share/systemd/user`, `/etc/systemd/user` (static, store links), `/run/user/1001/systemd/{transient,user.control,generator.late}`, `/run/systemd/transient`, with file times (`find -printf`). `systemctl --user list-units --all`, `list-timers --all`, `show` per unit (including `Transient=`). `ps -u li` with cgroups, `/proc/<pid>/{cwd,environ}`, `ss -xlp`. `journalctl --user` around the last timer runs. Cron and at: `crontab`, `atq` not installed; `/var/spool/cron`, `/etc/cron.d` absent. Claude: `~/.claude`, `~/.config/Claude/*/scheduled-tasks.json`. Codex: `~/.codex`, `~/.codex-next`. `pueue status --json`. `~/.config/autostart`, shell profiles. Origins from flow records under `/home/li/primary/flows`. Linger for li: no.

"DECLARED" = a link into `/nix/store/hqs880888kqnmbbmaxizn72q9l4iwcjh-home-manager-files` (home) or into `/etc/static` (system). "HAND-MADE" = anything else.

## Scheduled jobs (the centre of the order)

| Unit (in `~/.config/systemd/user/`) | Ran | Schedule | Origin | State before | Action |
|---|---|---|---|---|---|
| `agent-intercom-fleet-cleanup.{service,timer}` | node `/home/li/.pi/agent/packages/agent-intercom-orchestrator/src/agent-fleet-cleanup.mjs` | every 15 min | HAND-MADE plain files, 2026-08-09 10:21; da88cf wave2-plan row 13 "discard" | timer active; service failing every run (script gone, MODULE_NOT_FOUND) | removed |
| `core-checkup.{service,timer}` | node `…-source/tools/core-checkup.mjs` with `~/.config/core-checkup/policy.json` | every 30 min | HAND-MADE plain files, 2026-09-15 21:51; owner unknown (da88cf row 14) | timer active; service failing every run (ExecStartPre roster path missing) | removed |
| `field-census.{service,timer}` | node `/home/li/primary/tools/field-census-cycle.mjs --observe-only` | every 5 min | HAND-MADE links into `/home/li/primary/tools/field-census/`, 2026-09-20/21; flow 9ddcbc report `field-census-checkup-deployment-2026-09-20.md` | timer stopped 2026-09-27 18:53, still enabled | removed (links only; repo files untouched) |
| `field-checkup-shadow.{service,timer}` | node `/home/li/primary/tools/field-checkup-shadow-cycle.mjs` | every 30 min | HAND-MADE links into `/home/li/primary/tools/field-checkup/`, 2026-09-20; flow 9ddcbc | stopped 18:53, enabled | removed (links only) |
| `field-luna-research.{service,timer}` | `/git/github.com/LiGoldragon/field/bin/field-luna-research-run --once` | every 30 min | HAND-MADE plain files, 2026-09-22 10:29-10:33; flow not recorded by name | stopped 18:53, enabled | removed |
| `field-monitor-98eb43.{service,timer}` | node `/home/li/primary/flows/98eb43/monitor/census.mjs` | every 5 min | HAND-MADE plain files, 2026-09-25 10:19; flow 98eb43 (da88cf row 18: discard when 98eb43 ends) | stopped 18:53, enabled | removed |

All six `timers.target.wants/*.timer` enable links were hand-made and removed with them. Remaining user timers: `systemd-tmpfiles-clean.timer` (system-declared). System timers (logrotate, fwupd-refresh, nix-gc, fstrim, systemd-tmpfiles-clean) are all declared; none flow-made.

Other schedulers: no crontab, cron or at on this host. Claude Desktop `scheduled-tasks.json` (two copies under `~/.config/Claude/`) hold `"scheduledTasks": []`. No durable Claude Code `scheduled_tasks.json` found. No Codex automations stored locally (`~/.codex*/automations` absent; global state holds only a tool schema). Cloud-side routines of either harness were not checked (would need an account call). Pueue: tasks 0-6, all Done, 2025-10 and 2026-04, yt-dlp and TheBookOfSol OCR; the living's own, left.

## Other hand-made units and processes

Removed:
- `~/.config/systemd/user/cf7879-overnight-poc-batch.service`, a dangling link (2026-09-15 22:23) into `/home/li/wt/github.com/LiGoldragon/primary/cf7879-overnight-batch/…` (target gone); not loaded. da88cf row 19 "discard".
- `~/.local/share/systemd/user/gascity-supervisor.service` and 35 `gascity-supervisor-gc-home-*.service`, written 2026-05-04..06 by the `gc` (gascity) tool; all disabled and inactive.
- Process 3108724 `target/debug/flow-nexus`, started 2026-09-27 10:56, cwd `/home/li/wt/github.com/LiGoldragon/flow/codex-session-binding-6fe957`, HOME and runtime under `/home/li/.local/state/flow/mind-astra-refresh-6fe957.fYjXMV/`; a test nexus of flow 6fe957, listening only on its own sandbox sockets, no connections, no live seat. Stopped with SIGTERM by PID. It sat in the cgroup of `codex-remote-control-next.service` but was not its main process; the service is unaffected.

Left, hand-made:
- `~/.config/systemd/user/flow-nexus.service.d/override.conf` (2026-09-25 20:52): special case, below.
- `~/.config/systemd/user/codex-remote-control.service.d/limits.conf` (2026-09-23): `LimitNOFILE=524288`; keep list (Codex remote control). da88cf found it duplicates the declared value.
- `~/.config/systemd/user/field-luna-heartbeat.service -> /dev/null` (mask, 2026-09-25): guards against a declared unit whose source is broken (da88cf row 8); inert; removing is the living's call.
- `~/.config/systemd/user/swaync.service -> /dev/null` (mask, 2026-04-09): desktop notification daemon; desktop, left.
- `~/.config/systemd/user/dji-keepalive.service.manual-backup-20260525154824` and `spirit-daemon.service.d/guardian-alignment.conf.disabled-20260628T221924`: inert files systemd does not load; possibly the living's own; left.
- Process 196271 `dolt sql-server` (cwd `~/.beads/dolt`, since 2026-09-26 18:44) and 618862 a second `gpg-agent --daemon`, both reparented into `codex-remote-control-next.service`'s cgroup. Beads store and keys; left.
- System transient units `lojix-self-switch-deploy-46.service` (active exited) and `lojix-self-switch-deploy-50.service` (failed) in `/run/systemd/transient/`, made by lojix.service's self-switch; system manager, lojix on keep list; left. They vanish at reboot or with `sudo systemctl reset-failed`.

User transient units present: only desktop ones (`app-niri-*`, `app-ghostty-surface-transient-*` terminal tabs holding Herdr and seats, `app-wispr-flow-7971.scope`, dbus-activated GNOME services). No `systemd-run` jobs from flows remain in the user manager.

## Special case: flow-nexus drop-in

`~/.config/systemd/user/flow-nexus.service.d/override.conf` clears `ExecStart` and sets `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus`. The declared unit (`/nix/store/cfsalbbppbskgwd2qyyvwzncj2ki7cyn-flow-nexus.service`) says `flow-0.14.0`. Running PID 1937 is 0.12.2, up since 2026-09-26 16:19. Removing the drop-in and reloading changes nothing until the next restart of flow-nexus.service (or login); then the stable Flow Nexus runs 0.14.0, with whatever state or protocol change 0.12.2 -> 0.14.0 brings for the stable seats bound to it. It also `Requires=codex-remote-control.service`, so it is tied to the Codex seat launch in progress. Not changed.

## Declared units that look like flows' additions

Home configuration: `flow-nexus`, `flow-nexus-next`, `flow-configuration-next`, `message-daemon`, `message-nexus-next`, `orchestrate-nexus`, `codex-remote-control`, `codex-remote-control-next`, `aggregator-daemon`, `opencode-testing` (inactive; stopped 2026-09-27 18:52), `chroma-daemon`, `listener`, `criomos-lock-*`, `criomos-ui-priority`, `active-network-widget`. System configuration: `opencode.service` (user unit from `/etc/static/systemd/user`), `lojix.service`. Not touched.

## Backups

Every removed file is under `/home/li/wt/primary/56ae53/flows/8904b1/witnesses/services-removed-0928/`: `config-systemd-user/` (links preserved as links; `symlinks.txt` lists their targets), `linked-targets/` (contents of the linked field-census and field-checkup units), `local-share-systemd-user/` (36 gascity units), `stray-flow-nexus-3108724.txt`. To restore a timer: copy back into `~/.config/systemd/user/`, `systemctl --user daemon-reload`, `systemctl --user enable --now <name>.timer`.
