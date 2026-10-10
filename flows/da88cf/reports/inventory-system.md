# System inventory: temporary and undeclared state

Subflow of da88cf. Read-only inventory taken 2026-09-25 20:55 to 21:20 local (-0600) from ouranos, with read-only ssh probes of prometheus and zeus. Nothing was changed on any machine. `sudo -n` is refused on all three reachable hosts, so root-only facts are listed as unknowns.

Every entry has an **O** line for observations (what a command returned), an **I** line for inferences, and a **D** line for the proposed disposition. Unknowns are collected at the end.

Declared sources compared against: CriomOS `19d5736` (2026-09-25 20:08), CriomOS-home `478b4ea0` (2026-09-25 20:08), goldragon cluster data `8c4d03d`. Ouranos's cluster-data features are Edge, LowPower, NextGeneration, Nordvpn, HardwareVideo, TailnetClient, TailnetController, NixBuilder.None, OpenCodeTesting, and PersonaDevelopment[GitoliteServer].

## Counts by class (ouranos unless noted)

| Class | Items |
|---|---|
| Ad-hoc package installs (nix profile element, ~/.local bin/libexec) | 4 |
| Drop-ins, masks, and edits on declared units | 6 |
| Undeclared persistent user units and timers | 7 unit pairs (13 files) |
| Transient `systemd-run` units | 3 |
| Orphaned processes outside any unit | 1 group (67 processes) |
| System-level undeclared state | 2 (firewall drop-in and hook; running generation outside Lojix) |
| Generation and owner drift (system, Home) | 3 |
| Nix configuration and local pins | 4 |
| Local-build GC roots | about 100 roots in 6 groups |
| Tailnet / Headscale | 1 fault with 3 undeclared parts |
| Declared but not deployed | 2 (field-clj; the Flow pin at HEAD) |
| Other nodes | prometheus 4, zeus 1, unreachable 5 |

## A. Ad-hoc package installs

### A1. Flow 0.12.2 in the user nix profile
- **O:** `nix profile list` shows the element `flow` → `/nix/store/c044v5pa…-flow-0.12.2` at priority 4, ahead of `home-manager-path` at priority 5. `~/.nix-profile/bin/flow` and `flow-nexus` resolve to 0.12.2. The profile history shows the flow element installed and removed four times on 2026-09-25 local: 0.10.5 (19:03), 0.10.7 (20:23), 0.12.1 (20:37), and 0.12.2 (20:52). The store path was registered at 20:49, carries no signatures, and has deriver `0bh3gvqf…-flow-0.12.2.drv`. `~/.nix-profile` → `.nix-profile-8-link` → `.nix-profile-8-link-19-link`.
- **O:** The active Home generation provides Flow **0.6.0** (`99rqvjxx…-flow-0.6.0`). CriomOS-home HEAD pins flow `8df890b` (**0.10.7**). Flow main is `34aaf78` (0.12.2).
- **I:** 0.12.2 was built locally from flow main `34aaf78` and installed through `nix profile` by the Flow activation chain (the e51411 Luna subflow, then b7da5d Field Sol). b7da5d log line 108 says "local build and profile-priority-4 reversible user-unit drop-in", and the 38de5b log lines 277–278 name 0.12.2 = 34aaf78.
- **D:** Integrate in CriomOS-home. Move the `flow` input to `34aaf78` in `modules/home/profiles/min/flow.nix` / `flake.nix`, deploy through Lojix, and then remove the profile element (A1) and the drop-in (B1).

### A2. messenger-clj 0.2.5 and the `hm-*` commands
- **O:** `~/.local/libexec/messenger-clj` → `/nix/store/p8mz1msm…-messenger-clj-0.2.5` (link made 2026-09-25 20:36; path registered 20:36:16, unsigned). `~/.local/bin/{messenger-clj, hm-send, hm-send-abrupt, hm-list, hm-register, hm-repair, hm-deregister, hm-rebind, hm-move, hm-retire, hm-heartbeat-state}` are hand-made symlinks into it (14:18–20:35). The wrapper runs babashka with the jar and a Datalevin pod from `3gdswy2p…-source`.
- **O:** `nix-store -q --roots` on the 0.2.5 path returns **no roots**. `nix-gc.timer` runs `nix-collect-garbage --delete-old` at 00:00 (next run 2026-09-26 00:00).
- **O:** CriomOS-home has no messenger-clj input or module; a grep for `messenger-clj|hm-send` finds nothing. The 0.2.2 build exists only as `/git/github.com/LiGoldragon/messenger-clj/result` (16:21). The predecessor's "0.2.2" is therefore out of date: 0.2.5 is live.
- **I:** 00f95a installed it imperatively (88475f log line 74: "messenger 0.2.5 live"). Without a root, tonight's GC can delete the store path, which would break every `hm-*` command.
- **D:** Integrate in CriomOS-home: add messenger-clj as an input and package, per the e51411 audit item M7. Then discard the `~/.local` links. Until then this is the most time-sensitive item.

### A3. Retired messenger artifacts
- **O:** `~/.local/libexec/.retired-hacky-messenger-clojure-9176503a/` (12:03–13:48 today) holds five revision directories, a `launcher`, and cutover, shape, and freeze-audit receipts. Its cutover receipt names `~/.local/state/hacky-messenger-clojure` as the state target.
- **D:** Discard after its receipts are archived to a flow report. It is evidence, not live state.

### A4. Other files in `~/.local/bin`
- **O:** `message-write-configuration` is an ELF binary, 2026-09-17 17:57. Its strings reference `~/.cargo/git/checkouts/protos-…`, so it is a local cargo build. `cloud-maintainer-chrome` is a bash script (2026-06-19) that drives a Chrome debug profile at the DigitalOcean login.
- **I:** `message-write-configuration` was probably made during the secondary-348e7b message schema work on 09-17 (see H). The origin of `cloud-maintainer-chrome` is not evidenced.
- **D:** Discard `message-write-configuration`; if it is needed, the declared `message` package should ship it. `cloud-maintainer-chrome` is unknown: integrate it as a cloud-maintenance feature only if someone owns it, otherwise discard.

## B. Drop-ins, masks, and edits on declared units

### B1. `flow-nexus.service.d/override.conf`
- **O:** Mode 0600, 2026-09-25 20:52. It sets `ExecStart=` and then `ExecStart=/nix/store/c044v5pa…-flow-0.12.2/bin/flow-nexus`. The unit is active and running from 20:52 with PID 3450235 on 0.12.2. The declared unit, from the HM files `zv4s8czi…`, runs 0.6.0.
- **D:** Same as A1: integrate by bumping the declared pin, then delete the drop-in.

### B2. `field-luna-heartbeat` is declared but disabled by hand
- **O:** The active Home generation declares `.service`, `.timer`, and `.path`. In `~/.config/systemd/user`, `field-luna-heartbeat.service` → `/dev/null` (a persistent mask, 13:13 today), and `/run/user/1001/systemd/user/field-luna-heartbeat.service` → `/dev/null` (a runtime mask, 13:13). The `.timer` and `.path` links are absent, and `systemctl --user is-enabled` returns `not-found` for both.
- **I:** Masked on purpose ("heartbeat stays masked", b7da5d log line 78). The e51411 audit says the pinned `prompt-relay-source` 9d144e3 predates the fix `fabbba0d`.
- **D:** Integrate in CriomOS-home. Either repin `prompt-relay-source` to a fixed revision, or gate the module behind a feature so it is off in cluster data. Then remove both masks. The living or the Field owner must choose.

### B3. `codex-remote-control.service.d/limits.conf`
- **O:** Contains `LimitNOFILE=524288`, 2026-09-23 13:20. The declared unit already sets `LimitNOFILE = 524288` (`agent-intercom.nix:125`), and the linked unit file contains it.
- **D:** Discard. It is redundant.

### B4. Inert leftovers
- **O:** `spirit-daemon.service.d/guardian-alignment.conf.disabled-20260628T221924` (June), plus empty `message-daemon.service.d/` (09-17) and `spirit-judge.service.d/` (08-03).
- **D:** Discard.

### B5. `dji-keepalive.service.manual-backup-20260525154824`
- **O:** Inert backup file, content dated 2026-02-17.
- **D:** Discard.

### B6. `swaync.service` → `/dev/null`
- **O:** Masked since 2026-04-09. CriomOS-home sets `swaync.enable = false` (`min/default.nix:494`).
- **D:** Discard the mask. The declared setting already covers it.

## C. Undeclared persistent user units and timers (`~/.config/systemd/user`)

None of these are in the active Home generation. Each is a regular file, or a symlink into a mutable path, enabled through `timers.target.wants`.

| Item | Since | Runs | State | Proposed disposition |
|---|---|---|---|---|
| `agent-intercom-fleet-cleanup.{service,timer}` | 2026-08-09 | node `~/.pi/agent/packages/agent-intercom-orchestrator/src/agent-fleet-cleanup.mjs` | timer every 15 min; service **failed** | Discard. The source path is gone, and CriomOS-home's `agent-intercom.nix` is the declared home for anything still needed. |
| `core-checkup.{service,timer}` | 2026-09-15 | `~/.nix-profile/bin/node` on a pinned `…-source/tools/core-checkup.mjs` with roster `8xgi8bjm…` | every 30 min | Integrate as a CriomOS-home monitoring module (feature-gated) if it is kept; otherwise discard. Owner unknown. |
| `field-census.{service,timer}` | 2026-09-20 | symlinks into `~/primary/tools/field-census/`; node `tools/field-census-cycle.mjs` | every 5 min | Integrate as a CriomOS-home Field-monitoring feature with a pinned source, or discard. Design is in `flows/4b0f60/reports/field-census-and-checkup-architecture.md`. |
| `field-checkup-shadow.{service,timer}` | 2026-09-20 | symlinks into `~/primary/tools/field-checkup/` | every 30 min | Same as field-census. |
| `field-luna-research.{service,timer}` | 2026-09-22 | `/git/github.com/LiGoldragon/field/bin/field-luna-research-run --once`, from an unpinned working copy | timer elapsed | Integrate into the same Field feature with a pinned field input, or discard. |
| `field-monitor-98eb43.{service,timer}` | 2026-09-25 10:19 | node `~/primary/flows/98eb43/monitor/census.mjs` | every 5 min | Discard when flow 98eb43 ends. It is flow-scoped. |
| `cf7879-overnight-poc-batch.service` | 2026-09-15 | symlink into worktree `~/wt/…/primary/cf7879-overnight-batch/`, which is still present | active (exited) since 09-15 22:34 via RemainAfterExit | Discard. |

## D. Transient `systemd-run` units (user manager)

### D1. `codex-remote-control-next-recovery.service`
- **O:** Created 2026-09-24 13:49 and running PID 1998991. It runs `codex-next-0.158.0-alpha.9 app-server --remote-control --listen unix:///home/li/.codex-next/app-server-control/app-server-control.sock` with `CODEX_HOME=~/.codex-next`.
- **O:** The declared `codex-remote-control-next.service` is in `activating/auto-restart` with **NRestarts=42240**. Every attempt fails with "app-server control socket is already in use", and the journal shows the loop running every 2 s.
- **I:** Someone started the transient unit as a manual recovery. It now holds the socket that the declared unit needs. Several Codex-next sessions (for example PIDs 2012036 and 2027935) are attached to it.
- **D:** Integrate. Fix the declared unit in CriomOS-home (Restart policy and socket ownership, or `ExecStartPre` socket cleanup), move the sessions across, and let the declared unit own the socket. Then discard the transient unit.

### D2. `psyche-fable-herdr.service`
- **O:** Created 2026-09-19 12:55 and running PID 807384. It runs `~/.nix-profile/bin/herdr server`, which is the declared herdr 0.8.2 binary from the HM path. `herdr.nix` in CriomOS-home declares no server unit.
- **D:** Integrate as a declared Herdr server user unit in CriomOS-home (`min/herdr.nix`), because live Field panes depend on it. Discard the transient unit only after a controlled handover, since killing it would take down the panes.

### D3. `unity-local-poc-0ab019.service`
- **O:** Created 2026-09-19 10:48 and running PID 599696 with MemoryMax 384M and CPUQuota 20%. It runs `~/primary/flows/0ab019/unity-local-poc/run-local.sh` against `unity-local-poc-0.1.0` store paths.
- **D:** Discard. It is a proof of concept.

Not counted: `app-niri-mako`/`noctalia` scope drop-ins (`50-MemoryLow.conf` and similar). These are written at runtime by the declared `criomos-ui-priority` (`ui-priority.nix:34`, `systemctl --user set-property --runtime`), so they are declared behaviour. The system manager has only `session-3.scope` as a transient unit, which is normal.

## E. Orphaned processes

### E1. 67 `fixture_harness.py` processes
- **O:** 67 processes of `~/.nix-profile/bin/python3 ~/primary/tools/flow-cli-poc/fixture_harness.py --ready-fd 7 --generation N`, started 2026-09-17 12:11. Their parent is the user manager, and they sit in `app-ghostty-surface-transient-2908029.scope`.
- **D:** Discard. These are leaked test fixtures.

`claude bg-spare` / `bg-pty-host` processes going back to 09-15 were also seen. These belong to the Claude Code harness and are not system state; they are listed only for completeness.

## F. System-level undeclared state (ouranos)

### F1. Firewall hook for the Prometheus USB link
- **O:** `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` (root, 0644, 2026-09-21 12:39) adds `ExecStartPost=` and `ExecReload=` pointing at `/etc/systemd/field-prometheus-usb-firewall.sh` (root, 0700, 732 bytes, same time). `firewall.service` loads the drop-in. These are the only non-store, non-`/etc/static` entries under `/etc/systemd`.
- **I:** A Field network flow wrote it for the ouranos→prometheus USB Internet-sharing chain (753e69, `reports/ouranos-host-hook-audit.md` and `network-path-plan-2026-09-21.md`). It persists across switches because `system.control` is not managed by NixOS.
- **D:** Integrate as a CriomOS network feature for USB-downlink sharing, declared per node from cluster data; then delete both files. The script body is root-only and was not read (see Unknowns).

### F2. Running system generation 188 has no Lojix record
- **O:** `/run/current-system` = `/nix/var/nix/profiles/system-188-link` = `hm7zclf0…`, set 2026-09-24 18:43:05. It is the only system generation left. `/run/booted-system` = `8cvwmgdk…` (boot of 09-10).
- **O:** The journal shows `sshd: Accepted publickey for root from 201:6de1:5500:…` (ouranos's own Yggdrasil address) with key `SHA256:7gVt…`, which is li's agent key. `nixos[…]: switching to system configuration …hm7zclf0…` follows. There is no `lojix-self-switch-deploy-*` unit.
- **O:** `lojix 'Query.ByNode.{ goldragon ouranos None }'` lists CompleteHost Current = deployment 4 (`41cvi7l9…`, CriomOS `36653a1`). That store path no longer exists; it has been garbage-collected.
- **I:** Someone, running as li through ssh to root on the same machine, switched to a system built outside Lojix. Lojix's view of ouranos is stale. The source revision of `hm7zclf0` is unknown.
- **D:** Integrate. Redeploy ouranos through `lojix-meta Deploy.Host` from a pushed CriomOS revision, so that Lojix Current equals the running system.

### F3. Two owners of the Home environment
- **O:** The active Home generation is `r3ci9jy0…`. It is activated by the NixOS `home-manager-li.service` in system 188 (18:43:08), and it is `~/.local/state/home-manager/gcroots/current-home`. Its `home-manager-path` (`f5kc0vss…`) is the element in `~/.nix-profile`.
- **O:** The standalone HM profile link is `home-manager-1032` = `f5kp8yn2…` (09-24 09:32). In Lojix, that path is deployment 29 (ActivateNow, CriomOS `90702b6`), which is **Failed** at Activate.
- **O:** Lojix Current UserEnvironment = deployment 27 = `y2mh6ajia…` (profile link 1031).
- **I:** Three different Home generations are claimed by three mechanisms: the live NixOS HM module, the HM profile pointer, and Lojix Current. The NixOS HM module and the Lojix `HomeManagerNixProfileV1` backend both write the same user profile.
- **D:** Integrate. Pick one owner per cluster-data feature in CriomOS or CriomOS-home: either the NixOS module or Lojix UserEnvironment deployment, not both. Then redeploy, so that the Lojix record, the HM profile, and `current-home` all agree.

## G. Nix configuration and local pins

### G1. `~/.config/nix/nix.conf`
- **O:** Undeclared, 2026-09-12. It sets `connect-timeout`, `http-connections`, `max-jobs = 0`, `builders = @/etc/nix/machines`, `builders-use-substitutes`, and an `access-tokens = github.com=…` line holding a **plaintext GitHub token** (value withheld here).
- **D:** Integrate. Put the builder settings in CriomOS nix settings (`/etc/nix/nix.conf` is declared and `/etc/nix/machines` already exists), and deliver the token through the declared secrets path. Rotate the token, since it sits readable in the home directory. Then discard the file.

### G2. User flake registry pin
- **O:** `~/.config/nix/registry.json` (2026-04-26) maps `horizon` to `path:/tmp/flake-false-test/payload-stub`. The target does not exist.
- **D:** Discard.

### G3. Declared system registry is malformed
- **O:** Every `nix` call prints `warning: cannot read flake registry '/nix/store/2573ls7j…-criomos-flake-registry.json': error: input attribute 'owner' is missing`.
- **D:** Integrate a fix in CriomOS's registry generation. This is a declared defect, not temporary state.

### G4. Local-override script
- **O:** `~/primary/tools/nix-local-stack` builds `--override-input` arguments (line 168). No `--override-input` appears in shell history; `.bash_history` has no match and there is no zsh history file.
- **D:** Keep, as tooling. It only matters when its outputs are activated, and none of the running state traces to it.

## H. Local-build GC roots (`/nix/var/nix/gcroots/auto`)

- **O:** 161 entries, of which 12 are dangling. The live ones fall into these groups:
  - 39 `~/.nix-profile-{6,7,8}-link*` generations. The `-6` and `-7` chains are dead, and many point to the empty profile `c0dj6b32…`.
  - `~/.local/state/nix/profiles/profile-1996` (an empty profile, 2026-08-06).
  - 7 HM profile generations.
  - 28 worktree `result` links under `~/wt/…`, including messenger-clj 0.2.0 and 0.2.3, flow-workspace-test, signal-*, and CriomOS-home codex-next-contract.
  - About 40 `/tmp/result`, `/tmp/result-1…36`, and `/tmp/f72ab7-signal-flow-generated-v*.result`.
  - 15 scratchpad results, including 38de5b's flow 0.12.0 and 0.12.1 builds.
  - `/tmp/prometheus-recovery-remote-smoke`.
  - 6 `~/.local/state/secondary-348e7b/…` roots, among them a prometheus system candidate and message 0.12.0 copies from 09-17.
  - `~/primary/firstmate-bridge/.local/herdr/profile-1-link` (2026-07-17).
  - `/var/lib/lojix/audits/bird-zeus-*` (Lojix-owned).
- **O:** `~/primary/result` changed to `hello-test` at 21:17, during this inventory.
- **I:** The flow 0.12.1 build root is at `/tmp/claude-1001/…/38de5bbb…/scratchpad/store-0121-38de5b/flow/result`. No gcroot to a 0.12.2 build output exists apart from the profile.
- **D:** Discard all groups except the Lojix audits and whatever currently backs A1 and A2, and only after A1 and A2 are integrated. Discarding means reclaiming through the disk-hygiene path, not now.

## I. Tailnet and Headscale on ouranos

- **O:** `tailscale status` reports logged out and `unexpected state: NoState`. The health check says: `fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority`. `tailscale debug prefs`: `ControlURL=https://127.0.0.1:8443`, `WantRunning=true`. `tailscaled` has been active since 09-10. The first x509 error in the journal is 2026-06-05; the same error repeats every ~20 s today.
- **O:** `headscale` (0.29.3) has been active since 09-10. Its declared config has `server_url: https://ouranos.goldragon.criome:8443` and `tls_cert_path: /var/lib/headscale/tls/headscale.crt`. It logs `TLS handshake error from 127.0.0.1: remote error: tls: bad certificate` in step with tailscaled.
- **O:** The served certificate, read without verification, is self-signed with `CN=ouranos.maisiliym.criome`, issuer the same, SAN `DNS:ouranos.maisiliym.criome, DNS:localhost, IP:127.0.0.1, IP:192.168.0.18`, valid 2026-03-13 to 2036-03-10.
- **O:** CriomOS `modules/nixos/network/headscale.nix` generates the self-signed certificate only `if [ -s "$certFile" ] && [ -s "$keyFile" ]` is false, so an existing certificate is never regenerated. `tailscale.nix` says "enrollment remains manual" and installs no trust anchor.
- **I:** Three pieces of undeclared state combine here. The certificate was minted under the old cluster name (maisiliym) and never rotated. The control URL is an imperative loopback login pref. The self-signed certificate is not trusted by tailscaled. The node has been off the tailnet since June at the latest. This is a standing fault, not tonight's change.
- **D:** Integrate in CriomOS. For the TailnetController feature: regenerate on FQDN mismatch, or use cluster PKI. For the TailnetClient feature: declare the control URL (the FQDN, not 127.0.0.1) and the trust anchor. Discard the old certificate as part of that deploy. Nothing was restarted.

## J. Declared, verified, no action

- **herdr 0.8.2:** `~/.nix-profile/bin/herdr` → `9x03bz0q…-herdr-0.8.2`, via the HM path of the active Home generation. CriomOS-home pins `herdr/v0.8.2`.
- **orchestrate 0.35.0:** `v42cxgyd…-orchestrate-0.35.0-profile`, via the HM path. CriomOS-home pins `9070cbb`.
- **lojix 7.0.0:** `/run/current-system/sw/bin/lojix` (system path). `lojix.service` is active and running since 09-24 16:14.
- **message-daemon 0.12.0:** A declared HM unit, running `npnsww3f…-message-0.12.0`.
- **field-clj: declared, not deployed.** CriomOS-home HEAD has it in `med/cli-tools.nix:51` (lock `75d7759`). It is not on PATH and is not in the active HM path.
- **Environment mismatch:** `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`, but the socket that exists is `/run/lojix/meta.sock`, and the journal readiness line names `meta.sock`. Integrate by fixing whichever module exports that variable.

## K. Other nodes

Nodes in cluster data: balboa, mirror-alpha, mirror-beta, ouranos, prometheus, tiger, vm-testing, zeus.

### Prometheus (reached as `prometheus.goldragon.criome`; the first attempt timed out)
- **O:** current = booted = `system-55` `7f8kpzcn…`, set 2026-09-24 21:03. Lojix `ByNode` for prometheus lists **no generations**. Its last host deployments are 19 (ActivateNow, **Failed** at Activate, `9d93d62`), 30 (Eval failed), and 31 (TestActivation, Build failed). `7f8kpzcn` does not appear in Lojix.
- **I:** Prometheus is running a system that Lojix does not record. The caller is unknown; it could be the partial effect of failed deployment 19, or an out-of-band switch.
- **D:** Integrate by redeploying through Lojix.
- **O:** Manual root `/nix/var/nix/gcroots/secondary-348e7b-prometheus-candidate` (09-17) and `/tmp/result` (a 26.05 system from 04-27). **D:** Discard.
- **O:** The standalone HM profile is `home-manager-1-link` (March), but `current-home` = `7xzgfn9h…` (06-30). Its nix profile has not changed since 06-20. **I:** Home is activated by the NixOS HM module; the standalone profile is stale. **D:** Covered by the owner decision in F3.
- **O:** `mpd.service` (user) failed. Tailscale is logged out; headscale is inactive, as expected since prometheus is not a controller. No undeclared units, drop-ins, or transient units, and `~/.local/bin` holds only the HM-managed `xdg-open`.

### Zeus
- **O:** current = booted = `system-72` (2026-09-06). There are no Lojix records at all (`Queried.{ [] [] … }`). No undeclared units, drop-ins, or transient units. `mpd.service` failed. Tailscale is not installed.
- **I:** Zeus was deployed before Lojix, or outside it.
- **D:** Bring it under Lojix at its next deploy.

### Unreachable (all unknown)
- tiger: `connect … port 22: Connection timed out` on the FQDN (resolves to `202:3895:…`).
- balboa: `Could not resolve hostname balboa.goldragon.criome`.
- mirror-alpha, mirror-beta, vm-testing: `Network is unreachable`. These are VMs on prometheus.
- Lojix records nothing for tiger.

## Largest gaps between running and declared state

1. **Flow Nexus.** Running 0.12.2 (nix profile plus drop-in); the active Home generation declares 0.6.0; CriomOS-home HEAD pins 0.10.7.
2. **The messenger (`hm-*`).** Running 0.2.5 from an unrooted store path through `~/.local` links. It is not declared anywhere and can be garbage-collected at 00:00.
3. **The ouranos system.** Running generation 188 was switched in outside Lojix, and Lojix Current points to a garbage-collected closure. Three different Home generations are claimed by three mechanisms.
4. **Codex-next.** A transient unit holds the socket, and the declared unit has restarted 42,240 times.
5. **Tailnet.** Imperative enrollment against loopback with a stale self-signed `maisiliym` certificate. Logged out since at least June.
6. **Prometheus.** Its running system is not in Lojix, and its last ActivateNow failed.

## Unknowns

- Root-only facts, because `sudo -n` is refused on ouranos, prometheus, and zeus: the root nix profile contents (on ouranos `default` → `per-user/root/profile`, which does not exist); the body of `/etc/systemd/field-prometheus-usb-firewall.sh`; `/var/lib/headscale/tls` contents and timestamps; `/etc/horizon.json`; live iptables state.
- Who performed the 2026-09-24 18:43 root self-ssh switch to `hm7zclf0` on ouranos, and from which CriomOS revision.
- Who switched prometheus to `system-55` at 2026-09-24 21:03, and from which revision.
- The source revision of `message-write-configuration`, and the owner and purpose of `cloud-maintainer-chrome`, `core-checkup`, and `firstmate-bridge`'s herdr profile.
- Whether the 0.12.2 Flow build ran locally or on a remote builder. The path is unsigned, and no build lines appear in the nix-daemon journal for the last 7 days.
- Why `~/.nix-profile` uses the nested `.nix-profile-8-link-N-link` layout, and which tool created generations 6, 7, and 8.
- tiger, balboa, mirror-alpha, mirror-beta, and vm-testing are unreachable, so none were inventoried.
- Whether the `system.control` firewall drop-in was written by `systemctl edit`, by `set-property`, or directly.
