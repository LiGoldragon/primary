# Prometheus return witness — da88cf subflow, 2026-09-25

Witness taken from ouranos (flow da88cf subflow). All host clocks read in
CST (-06:00); ouranos and Prometheus clocks agreed to the second
(`date -Is` on both at 21:17:54).
Scratch evidence (poll log, build log, per-derivation classification) is in
`/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/prometheus-return/`.

Nothing was reverted, restarted, authenticated or changed. The one mutation
was the witness build: one 7-byte store path on each host.

## 0. What Prometheus is (cluster data, live units)

- Builder: `/etc/nix/machines` on ouranos (declarative symlink to
  `/etc/static/nix/machines`):
  `ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 6 10 big-parallel,kvm,nixos-test - AAAA…`
- Cache: `substituters = http://nix.prometheus.goldragon.criome https://cache.nixos.org/`; `nix-serve.service` is running on Prometheus.
- Name resolution: `prometheus.goldragon.criome` and `nix.prometheus.goldragon.criome` → `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` (Yggdrasil 200::/7; `yggdrasil.service` runs on Prometheus). `wg.prometheus.goldragon.criome` → `5::5` (did not answer ICMP).
- Router: the previous boot's journal shows `kea-dhcp4` serving `br-lan` as `10.18.0.1`, a `router-wan-lease-recovery` timer, and `hostapd`, `dnsmasq` and `strongswan` running. Prometheus is also the LAN/Wi-Fi router for 10.18.0.0/24.
- Other: `prometheus-llama-router.service`.
- **Headscale is not on Prometheus.** It runs on ouranos: `headscale.service` is active since 2026-09-10 13:33:55 and listens on `*:8443`. CriomOS gates it on the node capability `tailnetController` in `modules/nixos/network/headscale.nix` ("Self-signed cert for Phase 1"). Prometheus's own tailscaled is not enrolled: `tailscale status` → `Logged out.`, journal `health(warnable=wantrunning-false): error: Tailscale is stopped.`
- Machine: GMKtec NucBox_EVO-X2, BIOS `EVO-X2 1.11` dated 10/17/2025.

## 1. Return timeline

Observed:
| time (-06:00) | event | source |
|---|---|---|
| 2026-09-25 12:55:13 | last journal entry of previous boot `b321aa5e…` (routine timer) | `journalctl --list-boots`, `-b -1` |
| 21:15:44 | current boot `638be1a9…` starts (kernel) | `journalctl --list-boots` |
| 21:16:26 | first nix-daemon client on Prometheus (`user li`) | Prometheus journal |
| 21:17:15, 21:17:24 | nix-ssh builder sessions from ouranos `201:6de1:…:fb1d` (88475f tester's two builds, before mine) | Prometheus journal |
| 21:17:24 | **my first poll**: ICMP to 200:ca41:… **ok**; ssh `BatchMode` login **ok**; tailscale peer **none** (5::5 no reply) | poll.log |
| 21:17:54 | `uptime`: `up 0:02` | ssh |
| 21:18:21–23 | witness remote build (§4) | build.log |

The first poll already succeeded, so "first ICMP" and "first ssh" are upper
bounds (≤ 21:17:24), not the true first moments. Prometheus is **never** a
tailscale peer of ouranos: ouranos has no tailnet (§2).

Clock discrepancy (observed): flow logs put the power-on at "about 21:57"
(b7da5d, da88cf) and 88475f's witness at "about 22:02". Both host clocks
show boot at 21:15:44 and 88475f's builds at 21:17. The flow-log times run
about 40 minutes ahead of the host clocks. Which clock those log entries
used is unknown.

## 2. Tailscale / Headscale on ouranos: a real, separate defect

Observed, with Prometheus up:
```
$ tailscale status
# Health check:
#     - You are logged out. The last login error was: fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority
#     - Unable to connect to the Tailscale coordination server to synchronize the state of your tailnet. Peer reachability might degrade over time.
unexpected state: NoState
```
`systemctl status tailscaled`: `active (running) since Thu 2026-09-10 13:29:53 CST`, tailscale 1.102.2, `--state=/var/lib/tailscale/tailscaled.state … --tun tailscale0`.

Journal since -1d (5853 lines): the same pair repeats every 20–40 s through the whole day, before and after Prometheus returned. Latest lines:
```
Sep 25 21:17:12 ouranos tailscaled[1482]: control: doLogin(regen=false, hasUrl=false)
Sep 25 21:16:35 ouranos tailscaled[1482]: Received error: fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority
```
Earliest retained occurrence:
```
2026-06-05T07:00:46-06:00 ouranos tailscaled[3337]: pm: using backend prefs for "profile-bd89": Prefs{… url="https://127.0.0.1:8443" host="ouranos" … Persist{o=, n=[HPa9Y] u="li" ak=-}}
2026-06-05T07:00:46-06:00 ouranos tailscaled[3337]: linkChange: in state NoState; …
2026-06-05T07:00:47-06:00 ouranos tailscaled[3337]: Received error: fetch control key: Get "https://127.0.0.1:8443/key?v=133": x509: certificate signed by unknown authority
2026-06-05T07:00:47-06:00 ouranos tailscaled[3337]: health(warnable=login-state): error: You are logged out. …
```

Verdict (inference from the lines above): the control server is
`127.0.0.1:8443`, which is Headscale on ouranos itself. Prometheus never
enters that path. The failure dates back to at least 2026-06-05, and it went
on unchanged after Prometheus came back. It is a **real defect, separate
from Prometheus**. Ouranos's tailscaled does not trust the Phase-1
self-signed certificate, and there is no enrolled identity (`NoState`).

It did not cause today's builder outage. The builder and the cache reach
Prometheus over Yggdrasil (`200:ca41:…`), not the tailnet. They worked the
moment Prometheus was powered on, with tailscaled still logged out.

Not done: `tailscale up`, `tailscale login`, or any change to the cert or trust.

## 3. Prometheus health (read-only over ssh)

- `uptime`: ` 21:17:54  up   0:02,  0 users,  load average: 0.37, 0.33, 0.14`
- `journalctl --list-boots | tail -3`:
```
 -2 40b41a7e… Thu 2026-09-24 13:44:46 CST Thu 2026-09-24 15:02:00 CST
 -1 b321aa5e… Thu 2026-09-24 15:02:17 CST Fri 2026-09-25 12:55:13 CST
  0 638be1a9… Fri 2026-09-25 21:15:44 CST Fri 2026-09-25 21:17:54 CST
```
- Last lines of `journalctl -b -1 -n 30`: routine lines only. `router-wan-lease-recovery` runs every 2 min and `kea-dhcp4` gave a DHCPACK to 10.18.0.103 at 12:53:56. The last line is:
  `2026-09-25T12:55:13-06:00 prometheus systemd[1]: Finished Recover a late router WAN DHCP lease.`
  There is no systemd shutdown sequence (no "Stopping …" of system units, no `Reached target Shutdown` / `Power-Off`). The only shutdown-like lines are ordinary user-manager logouts, the last at 11:16:24.
- Next boot: `2026-09-25T21:15:46-06:00 prometheus systemd-journald[625]: File /var/log/journal/6e83…/system.journal corrupted or uncleanly shut down, renaming and replacing.`
- `nixos-version`: `26.11.20260813.0e251e2 (Zokor)`. Booted system `nixos-system-prometheus-26.11.20260813.0e251e2`.
- `systemctl --failed`: `0 loaded units listed.`
- `nix-daemon` active, `sshd` active, `nix-serve` running.
- `/nix`: `/dev/nvme0n1p2  1.9T  848G  995G  47% /nix`.

Verdict (inference): this was **not a clean shutdown**. The journal stops in
the middle of routine activity, with no shutdown sequence, and journald later
reported the file as uncleanly shut down. That pattern fits a power loss, a
forced power-off (holding the button), or a hard hang that never flushed.
The living found the box off, which argues against a simple hang: a hung box
would still have been on. So a power loss or forced power-off is the likely
cause. The logs cannot tell a mains power loss from a held button. A short
press of the power button would have produced a clean logind shutdown, and
there is none.

**Restore on power:** CriomOS at 19d5736 contains nothing about power-restore
or wake-on-LAN (grep for restore/AC power/power loss/wake-on found nothing).
No remote check can prove the BIOS setting. The living can check it on the
box: enter the firmware setup at boot (EVO-X2 BIOS 1.11) and find the
power-state-after-AC-loss option (names vary, e.g. "Restore on AC Power
Loss", "State After G3", "AC Back"). Set it to Power On / Last State. The
supply and the wall socket or power strip it hangs from are also worth a
look. If the box also dropped at 12:55 and the 10.18.0.0/24 LAN it routes
went down then, other LAN clients may have seen it. I did not check that.

## 4. Remote build witness: YES

Live settings on ouranos before the build: `max-jobs = 0` already in effect
for user li (from `~/.config/nix/nix.conf`, §5), `builders = @/etc/nix/machines`,
`fallback = true`. I still passed `--max-jobs 0` and never passed `--builders`.

```
name=da88cf-remote-witness-1790392701 start=2026-09-25T21:18:21-06:00
$ nix build --no-link --print-out-paths --max-jobs 0 -L -v --impure --expr 'derivation { name = "da88cf-remote-witness-1790392701"; system = "x86_64-linux"; builder = "/bin/sh"; args = ["-c" "echo da88cf > $out"]; }'
querying info about '/nix/store/val2ndk3…-da88cf-remote-witness-1790392701' on 'http://nix.prometheus.goldragon.criome'...
querying info about '…' on 'https://cache.nixos.org'...
this derivation will be built:
  /nix/store/hcm5sd1ihn0yhmm5h36w05jzjr1v7l7s-da88cf-remote-witness-1790392701.drv
connecting to 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
building '/nix/store/hcm5sd1ihn0yhmm5h36w05jzjr1v7l7s-da88cf-remote-witness-1790392701.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
copying dependencies to 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
building '/nix/store/hcm5sd1ihn0yhmm5h36w05jzjr1v7l7s-da88cf-remote-witness-1790392701.drv'...
copying outputs from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
/nix/store/val2ndk3z55ar4pgddwijvmmyx2d2fg0-da88cf-remote-witness-1790392701
exit=0 end=2026-09-25T21:18:23-06:00
```
Neither substituter had the path (both were queried, then it was built).

Prometheus side: nix-daemon does not log derivation names. The matching lines:
```
2026-09-25T21:18:21-06:00 prometheus sshd-session[3018]: Accepted publickey for nix-ssh from 201:6de1:5500:7cac:2db9:759e:42d2:fb1d port 32870 ssh2: ED25519 SHA256:x5qI23+57xXlINVab5szQd2UVgwb4F9a9PzwLJj6FCw
2026-09-25T21:18:22-06:00 prometheus nix-daemon[2112]: accepted connection from pid 3035, user nix-ssh (trusted)
2026-09-25T21:18:23-06:00 prometheus nix-daemon[2112]: reaped child process 3053, status = succeeded
2026-09-25T21:18:23-06:00 prometheus sshd-session[3018]: pam_unix(sshd:session): session closed for user nix-ssh
```
The derivation-level proof is on Prometheus: the build log
`/nix/var/log/nix/drvs/hc/m5sd1ihn0yhmm5h36w05jzjr1v7l7s-da88cf-remote-witness-1790392701.drv.bz2`
(mtime 21:18:23.068) and the output
`/nix/store/val2ndk3…-da88cf-remote-witness-1790392701` (content `da88cf`,
deriver `…hcm5sd1i…drv`).

## 5. Hotfixes and local-build traces around the absence (none reverted)

### 5a. max-jobs on ouranos: declared 1, live 0 (ad hoc, older than the outage)
- Declared: `/etc/nix/nix.conf` → `/nix/store/2pz4lskw…-nix.conf` has `max-jobs = 1`, `cores = 2`, `connect-timeout = 5`, `fallback = true`. Under CriomOS `modules/nixos/nix/client.nix`, 1 is the value for a node that is `isRemoteNixBuilder` but not the center. goldragon's README lists the `NixBuilder` set as "`ouranos` at the default capacity of one and `prometheus` at six". So 1 is the declared value for ouranos.
- Live for user li: `nix config show max-jobs` → `0`. With `HOME`/`XDG_CONFIG_HOME` pointed away → `1`.
- Source of the 0: `/home/li/.config/nix/nix.conf` (mtime 2026-09-12 05:41). It holds `max-jobs = 0`, `builders = @/etc/nix/machines`, `builders-use-substitutes = true`, `connect-timeout = 60`, `http-connections = 8`, and **a plaintext GitHub `access-tokens` line** (value not copied here). Origin: flows/f6db8d/log.md:113, "~/.config/nix/nix.conf now `max-jobs = 0`, honored by the daemon".
- Status: **ad hoc, not declared**, predates today's outage, still in effect. The local builds today got around it per command (see 5b).
- Revert/decide: either declare "no local builds on ouranos" in cluster data (drop ouranos from the NixBuilder set, or give it capacity 0 so client.nix yields 0) and delete the user-file line, or accept the declared 1 and delete the user-file line. Also note `connect-timeout = 60` overrides the declared 5. The access token belongs in the secrets path, not a user nix.conf. This is a ruling for the living.

### 5b. Local builds on ouranos while Prometheus was off
- The ouranos nix-daemon journal does not name built derivations. It records only failures, e.g. `2026-09-25T13:50:14-06:00 ouranos nix-daemon[1108864]: ssh: connect to host prometheus.goldragon.criome port 22: Connection timed out`, repeated through 15:29 and later.
- Method: build logs under `/nix/var/log/nix/drvs` on ouranos with mtime in the window when Prometheus was off (12:55:13 → 21:15:44). Prometheus could not have built them. **305 derivation logs**: 36 Flow (flow-0.10.4 … flow-0.12.2, flow-workspace-deps/test/clippy/fmt, signal-flow and meta-signal-flow cargo-git sources), 41 messenger-clj (0.1.0 … 0.2.5, checks, uberjars, tests), and the rest field-clj, clj-build example, ethos, primary fixtures, orchestrate, lojix-deps, and many `Cargo.toml`/`linkLockedDeps`/vendor steps. First at 14:08 (messenger-clj-0.1.0), last at 20:49 (flow-0.12.2). By hour: 14h 85, 15h 4, 16h 72, 18h 8, 19h 26, 20h 43. A log file shows a build that was attempted locally; some may have failed. Full list: scratchpad `window.txt`.
- None before 14:08. Since Prometheus returned, only remote builds (21:17 ×2 from 88475f's tester, 21:18 mine).
- Authority on record: flows/38de5b/log.md:231 "e51411 ruling …: local builds on ouranos allowed while Prometheus is down". flows/836818/log.md:95 "local build when the builder is unreachable is allowed" (the living via d8df70). b7da5d's log says the local builds used "command-scoped builder-disable/cache-only flags", and e51411:124 says "local build with max-jobs auto". So these were **per-command flags. They left no persistent setting.**
- Revert/decide: no setting to revert. The local build outputs are unsigned by Prometheus and were built outside the policy. Proposal: rebuild whatever is live from them (Flow 0.12.2) on Prometheus through the declared path, then let GC collect the locally built paths. Local building has been off since the living's "all Nix builds/tests move to Prometheus immediately".

### 5c. Flow Nexus activation on ouranos: ad hoc user-unit drop-in plus a profile install
- `/home/li/.config/systemd/user/flow-nexus.service.d/override.conf` (mtime 2026-09-25 20:52, not a store link):
  ```
  [Service]
  ExecStart=
  ExecStart=/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus
  ```
  The base unit `flow-nexus.service` → `/nix/store/7j12prgx…-flow-nexus.service` comes from home-manager (b7da5d says it still names 0.6.0). The service has been active since 20:52:09.
- `nix profile` (user): entry `flow` → `/nix/store/c044v5pa…-flow-0.12.2`. History: v16 `flow 0.10.7 -> ∅`, v17 `∅ -> 0.12.1`, v18 `0.12.1 -> ∅`, v19 `∅ -> 0.12.2` (dates in UTC, 2026-09-26). `which flow flow-nexus` → `~/.nix-profile/bin/…` → flow-0.12.2.
- Status: **ad hoc**, built locally (5b), outside home-manager.
- Revert/decide: pin Flow 0.12.2 (or later) in CriomOS-home, build on Prometheus, activate home-manager, then remove `override.conf`, `nix profile remove flow`, `systemctl --user daemon-reload` and restart. Removing the drop-in before the pin lands would drop the service back to the 0.6.0 base unit and break the live Nexus. Order matters.

### 5d. Other items seen, not attributed to the outage
- `~/.config/systemd/user/field-luna-heartbeat.service -> /dev/null` (masked, 2026-09-25 13:13). This falls in the window, but I found no evidence tying it to Prometheus.
- Older ad hoc user drop-ins (message-daemon Sep 17, codex-remote-control Sep 23, spirit-* Jul/Aug). All predate the outage.
- `/etc/nix/*` is all declarative store links except `secret-key`, `secret-key.pub` and an empty `preCriad`. There is no builder-list override. `/etc/nix/machines` is intact and declarative.

## Unknowns
- Mains power loss or forced power-off: the logs cannot separate them. The BIOS power-restore setting can only be checked on the box.
- Whether anything else failed at 12:55 (UPS, power strip, the 10.18.0.0/24 LAN clients). Not checked.
- The true first ICMP/ssh moment: the box was already up at my first poll (boot 21:15:44, first client connection 21:16:26).
- Which clock the flow logs' "21:57" and "22:02" used.
- Whether any of the 305 local build attempts failed, and which of their outputs are live besides Flow 0.12.2.
- Tailscale repair: which CA ouranos should trust, and whether ouranos (as `tailnetController`) should enroll to its own Headscale by `127.0.0.1` or by its FQDN. Field Sol's scan found no CA/cert.
