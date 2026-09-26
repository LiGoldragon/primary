# Wave 2 plan: disposition of every temporary change, and dispatch order

Subflow of da88cf, read-only. Written 2026-09-25 (ouranos clock, CST). Nothing on any machine or repository was changed.

**Inputs read:** `reports/inventory-system.md` (whole), `reports/prometheus-return.md` (§5 hotfixes, and the rest), `flows/b7da5d/reports/prometheus-hotfix-inventory.md`, `flows/b7da5d/witnesses/tailscale-trust.md`. I also read `reports/headscale-repair.md` and `reports/wifi-prometheus.md` §0, and `vision/daisyChain.md` and `vision/clusterData.md`.

**Absent when I started and when I finished:** `reports/inventory-branches.md` and `reports/prometheus-pending.md`. The branch rows below come only from the da88cf log plus one `jj bookmark list` in messenger-clj. The Prometheus deploy rows do not yet know why Lojix deployments 19, 30 and 31 failed.

**Repository heads I checked:**
- CriomOS main is `d193baf` ("Update Ouranos field-clj home package"), so a676b3's field-clj pin has already landed. The inventory compared against `19d5736`.
- CriomOS-home main is `478b4ea0`. Its `flake.nix:79` pins flow `8df890b`, which is 0.10.7.
- messenger-clj main is `dfcf91f0`. Its `flake.nix` already builds the package through clj-build. Neither `m1-sender-aspect-model-38de5b` nor `m6-nix-38de5b` is an ancestor of main.
- horizon-rs has **no** `usbIpv4Gateway` capability. CriomOS has the consumer, `modules/nixos/network/usb-ipv4-gateway.nix` (commits `e98035f` and `73ba25c`, marked "source-only"). goldragon cluster data carries no gateway record.
- lojix pins horizon-rs `40d04d2`.
- `CriomOS/modules/nixos/nix/client.nix` gives `max-jobs = 1` to any node that has `NixBuilder`. Ouranos carries `NixBuilder.None`.
- No module in CriomOS-home main declares `codex-remote-control-next`. The unit's source is unknown. One candidate is the worktree `codex-next-contract` named in inventory H.

**Grades:**
- **W** (witnessed): a da88cf or b7da5d subflow saw it in command output or a file.
- **C** (claimed): relayed by a seat and not re-witnessed.
- **⚠** marks an item whose discard would break something that is live now.

## 1. Disposition table

| # | Item | Host | Grade | Disposition | Target repo · module · option | Owner | Depends on | Verification |
|---|---|---|---|---|---|---|---|---|
| 1 | Flow 0.12.2 as a `nix profile` element (priority 4), built locally | ouranos | W | integrate | CriomOS-home `flake.nix` `flow.url` → flow `34aaf78` (0.12.2); consumed by `modules/home/profiles/min/flow.nix` | Mind Sol 00f95a | — | the Home path's `flow --version` is 0.12.2 and was built on Prometheus; `nix profile list` shows no `flow` element (after 2) |
| 2 ⚠ | `flow-nexus.service.d/override.conf` pointing at 0.12.2 | ouranos | W | integrate, then delete | none: the declared unit comes from row 1 | Field Luna e71dab | 1, 25 | `systemctl --user cat flow-nexus` shows no drop-in and ExecStart in the HM store path at 0.12.2; Nexus answers. **Deleting it before 25 drops Nexus to 0.6.0.** |
| 3 ⚠ | messenger-clj 0.2.5 hand-linked into `~/.local/{bin,libexec}` (every `hm-*` command) | ouranos | W | integrate | CriomOS-home: new input `messenger-clj` (`github:LiGoldragon/messenger-clj/dfcf91f0` or later) and new module `modules/home/profiles/min/messenger-clj.nix` installing the package's `bin/*` | Mind Sol 00f95a | 4 | `readlink -f $(command -v hm-send)` resolves into the HM path; the `~/.local` links are gone; `hm-list` works. **Removing the links before 25 breaks all messaging.** |
| 4 | Temporary GC root for messenger 0.2.5 (dispatched tonight) | ouranos | C | discard after 3 lands | — | e71dab | 3, 25 | `nix-store -q --roots` on the 0.2.5 path shows only the HM root |
| 5 | Retired messenger artifacts in `~/.local/libexec/.retired-hacky-messenger-clojure-9176503a/` | ouranos | W | discard | receipts archived first to `flows/da88cf/receipts/` | Sonnet subflow, then e71dab | — | directory gone; archive file present |
| 6 | `~/.local/bin/message-write-configuration` (local cargo build, 09-17) | ouranos | W | discard | — | e71dab | — | file gone; `message` still works |
| 7 | `~/.local/bin/cloud-maintainer-chrome` (DigitalOcean login driver) | ouranos | W | **needs the living's word** | if kept: CriomOS-home new module `modules/home/profiles/med/cloud-maintenance.nix`, gated by a cluster-data feature | — | — | — |
| 8 | `field-luna-heartbeat` masked by hand (persistent and runtime `/dev/null`) | ouranos | W | integrate as feature | CriomOS-home `modules/home/profiles/min/field-luna-heartbeat.nix` gated off by a feature until `prompt-relay-source` (`flake.nix:20`, `9d144e3`) is repinned past `fabbba0d`; then remove both masks | CriomOS-home editor (Opus) | 1 (repo serialisation) | the unit is absent from the HM generation, or present and running from the fixed pin; no mask links |
| 9 | `codex-remote-control.service.d/limits.conf` | ouranos | W | discard | — (already declared at `agent-intercom.nix:125`) | e71dab | — | `systemctl --user show -p LimitNOFILE` is still 524288 |
| 10 | Inert drop-in leftovers (spirit `.disabled`, empty `message-daemon.service.d/`, `spirit-judge.service.d/`) | ouranos | W | discard | — | e71dab | — | files gone |
| 11 | `dji-keepalive.service.manual-backup-*` | ouranos | W | discard | — | e71dab | — | file gone |
| 12 | `swaync.service → /dev/null` | ouranos | W | discard | — (`min/default.nix:494` sets `swaync.enable = false`) | e71dab | — | swaync not running after `daemon-reload` |
| 13 | `agent-intercom-fleet-cleanup.{service,timer}` (failing; source gone) | ouranos | W | discard | — | e71dab | — | timer gone |
| 14 | `core-checkup.{service,timer}` | ouranos | W | **needs the living's word** (owner unknown) | if kept: new CriomOS-home `modules/home/profiles/min/field-monitoring.nix` | — | — | — |
| 15 | `field-census.{service,timer}` (runs from `~/primary/tools`) | ouranos | W | **needs the living's word** | if kept: the same new `field-monitoring.nix`, feature-gated, with a pinned `primary`/`field` input; design in `flows/4b0f60/reports/field-census-and-checkup-architecture.md` | CriomOS-home editor | 14's answer | — |
| 16 | `field-checkup-shadow.{service,timer}` | ouranos | W | **needs the living's word** | same as 15 | — | 15 | — |
| 17 | `field-luna-research.{service,timer}` (unpinned working copy) | ouranos | W | **needs the living's word** | same as 15, with a pinned `field` input | — | 15 | — |
| 18 | `field-monitor-98eb43.{service,timer}` | ouranos | W | discard when 98eb43 ends | — | e71dab, on 98eb43's end | 98eb43 closure | timer gone |
| 19 | `cf7879-overnight-poc-batch.service` (into a worktree) | ouranos | W | discard | — | e71dab | — | unit gone |
| 20 ⚠ | Transient `codex-remote-control-next-recovery` holds the socket; the declared unit has restarted 42,240 times | ouranos | W | integrate | the module that declares `codex-remote-control-next` is **not in CriomOS-home 478b4ea0**, so locate it first (candidate: branch or worktree `codex-next-contract`); fix with `ExecStartPre` stale-socket removal plus `RestartSec` backoff | CriomOS-home editor (Opus), handover by e71dab | 25 | declared unit active, NRestarts stable, sessions attached to it; transient unit gone. **Stopping the transient unit now kills live Codex-next sessions.** |
| 21 ⚠ | Transient `psyche-fable-herdr` (the Herdr server behind live panes) | ouranos | W | integrate; the handover needs the living's word | CriomOS-home `modules/home/profiles/min/herdr.nix`: new `systemd.user.services.herdr-server`, feature-gated | CriomOS-home editor; handover by e71dab | 25, Q5 | declared unit owns the server; panes reattached. **Killing the transient unit ends every pane.** |
| 22 | Transient `unity-local-poc-0ab019` | ouranos | W | discard (confirm 0ab019 is done) | — | e71dab | — | unit gone |
| 23 | 67 leaked `fixture_harness.py` processes (09-17) | ouranos | W | discard | — | e71dab | — | `pgrep -fc fixture_harness` returns 0 |
| 24 ⚠ | Firewall hook `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` + `/etc/systemd/field-prometheus-usb-firewall.sh` (root; body unread) | ouranos | W (body unknown) | integrate as feature (the daisy-chain downlink) | producer: horizon-rs `lib/src/model.rs` new `NodeCapability::UsbIpv4Gateway { uplink, downstream, downstreamMac, gateway }`; data: goldragon `cluster-definition.datom` record on ouranos; consumer: CriomOS `modules/nixos/network/usb-ipv4-gateway.nix` (exists), plus a `systemd.tmpfiles` `r` rule deleting both hook files in the same generation | horizon-rs / goldragon / CriomOS editors (Opus); b7da5d deploys | N1–N4, 52 | declared iptables NAT with the `criomos-usb-gateway-nat` comment present, hook files absent, and the testing-transitive-network-topology cases pass. **Deleting the hook before the declared gateway is live may cut any downstream host riding the USB link.** Leaving it after the gateway is live makes a duplicate NAT owner, which the skill says must fail closed. |
| 25 | ouranos running generation 188 was switched by root self-ssh outside Lojix; Lojix Current points to a GC'd closure | ouranos | W | integrate (redeploy) | Lojix `Deploy.Host` goldragon ouranos from pushed CriomOS main | Field Sol b7da5d | 26 (interim), 48, 2b.1 | Lojix `Query.ByNode` Current store path = `/run/current-system` |
| 26 | Three owners claim Home (NixOS HM module, standalone HM profile 1032 = failed deployment 29, Lojix Current = 27) | ouranos (also prometheus, row 44) | W | **needs the living's word**; interim ruling by da88cf | CriomOS `modules/nixos/userHomes.nix` (NixOS HM module) **or** Lojix `UserEnvironment` (`HomeManagerNixProfileV1`), never both | da88cf rules; 504461 / b7da5d apply | — | `current-home`, the HM profile and Lojix Current name one path |
| 27 | `~/.config/nix/nix.conf` builder lines (`max-jobs = 0`, `connect-timeout = 60`, `http-connections`, `builders-use-substitutes`) | ouranos | W | integrate | goldragon: remove `NixBuilder.None` from ouranos, so `CriomOS/modules/nixos/nix/client.nix` `localMaxJobs` yields 0 ("laptop stays quiet"); first check that no node lists ouranos in its `/etc/nix/machines`. Put the other lines in `client.nix` if they are wanted. | goldragon editor; CriomOS editor | 28 | `nix config show max-jobs` is 0 with `HOME` pointed away; the user file is deleted |
| 28 ⚠ | Plaintext GitHub `access-tokens` in the same file | ouranos | W | **needs the living's word** (rotation is the living's account) | new sops secret `goldragon/secrets/githubAccessToken.sops` read by a CriomOS nix module through `!include` of `/run/secrets/…` | CriomOS editor after Q2 | — | the token is absent from `~/.config`; private fetches (field-clj) still evaluate on ouranos. **Deleting the line before the secret path lands breaks evaluation of private inputs on ouranos**, and evaluation must happen there tonight. |
| 29 | `~/.config/nix/registry.json` (`horizon` → a missing `/tmp` path) | ouranos | W | discard | — | e71dab | — | file gone |
| 30 | Declared flake registry malformed (`input attribute 'owner' is missing`) | ouranos (all nodes) | W | integrate (declared defect) | CriomOS `modules/nixos/nix/client.nix`, the registry-entry builder from `sourceInfo` | CriomOS editor (Opus) | — | no registry warning on any `nix` call after deploy |
| 31 | `~/primary/tools/nix-local-stack` (`--override-input` tool) | ouranos | W | keep (tooling, not system state) | — | — | — | — |
| 32 | About 100 local-build GC roots in 6 groups (profile chains 6/7, `/tmp/result*`, worktree results, scratchpads, secondary-348e7b) | ouranos | W | discard (disk-hygiene path) | — | Sonnet subflow, disk-hygiene | 2, 3, 4 | root count reduced; Lojix audit roots kept |
| 33 | 305 locally built derivations from the outage (Flow, messenger-clj, field-clj …), unsigned | ouranos | W | discard (let GC take them after Prometheus rebuilds what is live) | — | covered by 32 | 1, 3 | the live Flow and messenger paths are signed by the Prometheus key |
| 34 | Headscale certificate: CN/SAN `ouranos.maisiliym.criome`, never regenerated (the oneshot only checks that the file is non-empty) | ouranos | W | integrate | CriomOS `modules/nixos/network/headscale.nix`: `headscale-selfsigned-cert` regenerates when the SAN lacks `criomeDomainName` (tonight, Fork A′: the key becomes a sops secret) | CriomOS editor (Opus) | Q1 fork ruling | `openssl s_client` SAN carries `ouranos.goldragon.criome` |
| 35 | tailscaled `ControlURL=https://127.0.0.1:8443` hand-set | ouranos | W (inferred strong) | integrate | CriomOS `modules/nixos/network/tailscale.nix`: new oneshot `criomos-tailnet-enroll` running `tailscale up --login-server=https://<controller FQDN>:8443 --auth-key=file:<sops path>` (not upstream `authKeyFile`, which puts the key in argv) | CriomOS editor | 34, 36, 37 | `tailscale debug prefs` ControlURL is the FQDN |
| 36 | No trust anchor for the self-signed control certificate | ouranos, prometheus | W | integrate | CriomOS new module `modules/nixos/network/cluster-pki.nix` setting `security.pki.certificateFiles` from a public cert in goldragon (A′: the Headscale leaf; later A: a cluster CA) | CriomOS editor | 34 | tailscaled stops logging x509 errors |
| 37 | Enrollment: no identity (`NoState` on ouranos, `NeedsLogin` on prometheus); a preauth key needs root on the controller (`sudo -n` refused) | ouranos, prometheus | W | **needs the living's word** | new sops secret `tailnetAuthKey`, consumed by row 35 | the living, then b7da5d | 34–36 | `tailscale status` lists both peers; ouranos pings prometheus over 100.64/10 |
| 38 | tailscaled uploads logs to Tailscale Inc. | ouranos | W | integrate | CriomOS `tailscale.nix`: `services.tailscale.disableUpstreamLogging = true` | CriomOS editor | — | no `logtail: upload` lines |
| 39 | Controller on a roaming laptop (Fork C: move `TailnetController` to prometheus) | cluster | W (topology) | **needs the living's word** | goldragon `cluster-definition.datom` capability move | — | — | — |
| 40 | field-clj declared (`med/cli-tools.nix:51`, CriomOS `d193baf`) but not deployed | ouranos | W | integrate (deploy) | — (already declared) | b7da5d deploy; Field Astra 504461 witnesses | 25 | `field-clj` on PATH from the HM path; clj-build check green on Prometheus |
| 41 | `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`, but the socket is `meta.sock` | ouranos | W | integrate | CriomOS `modules/nixos/lojix.nix:209` `cfg.ownerSocketPath` default → `/run/lojix/meta.sock` (the lojix VM test uses meta.sock); check `checks/lojix-nexus-service` | CriomOS editor | — | `echo $LOJIX_OWNER_SOCKET` in a new login names an existing socket |
| 42 | prometheus runs `system-55` (09-24 21:03), unknown to Lojix; its last ActivateNow (19) failed | prometheus | W | integrate (redeploy) | Lojix `Deploy.Host` goldragon prometheus from CriomOS main | b7da5d | prometheus-pending report (absent), 48, 25 | Lojix Current = prometheus `/run/current-system` |
| 43 | prometheus manual root `secondary-348e7b-prometheus-candidate` + `/tmp/result` (26.05) | prometheus | W | discard | — | Sonnet disk-hygiene (root may be needed) | 42 | roots gone |
| 44 | prometheus standalone HM profile stale (March) vs `current-home` (06-30) | prometheus | W | follows 26 | as 26 | — | 26 | as 26 |
| 45 | `mpd.service` failed on prometheus and zeus | prometheus, zeus | W | unknown (a declared defect, not a hotfix) | — | later | — | — |
| 46 | zeus has no Lojix record | zeus | W | integrate (first Lojix deploy; zeus is the chain's leaf) | Lojix `Deploy.Host` goldragon zeus | b7da5d | N3 | Lojix Current = zeus `/run/current-system` |
| 47 | tiger, balboa, mirror-alpha, mirror-beta, vm-testing unreachable | various | W (unreachable) | unknown | — | — | — | — |
| 48 | Stale Lojix generated inputs / materialization for ouranos (the hardware-evaluation mismatch) | ouranos | C | integrate (fresh coherent request) | Lojix producer; no hand edit of `/var/lib/lojix/generated-inputs` | b7da5d | — | Lojix `Evaluate` of ouranos succeeds on current inputs |
| 49 | 5f38bc historical `--override-input` target realizations under generated inputs | ouranos | C | unknown → likely discard after 48 | — | Opus review | 48, branch report | — |
| 50 | NetworkManager profile `goldragon.criome` `autoconnect=no`, set by an agent (d8df70) on 09-24 to avoid mt7925 panics | ouranos | W | **needs the living's word** | if rejoined: CriomOS new client module `modules/nixos/network/wifi-sae-client.nix`, gated by a new cluster-data capability (`wifi-eap.nix` serves the unused EAP SSID) | — | — | — |
| 51 | Branch messenger-clj `m6-nix-38de5b` (Nix build on clj-build) | repo | W (not merged); content C | discard (main already builds on clj-build; confirm no unique commit) | messenger-clj | Opus review | — | bookmark deleted on origin after the diff is shown empty in substance |
| 52 | Branch messenger-clj `m1-sender-aspect-model-38de5b` ("launcher receipt names the registering Flow") | repo | W (not merged); content C | unknown → merge or discard by review | messenger-clj | Opus review, then 00f95a | — | merged into main, or deleted with a reason |
| 53 | 5f38bc consumer pin branches, paused | repos | C | unknown | — | Opus review | branch report | — |
| 54 | All other feature branches and worktrees | all repos | — (report absent) | unknown | — | inventory-branches subflow | — | — |
| 55 | Prometheus cannot fetch private field-clj (archive 404, ssh host key) | prometheus | C | integrate later; tonight no change (evaluate on ouranos, derivations on Prometheus) | future: CriomOS `programs.ssh.knownHosts` for github + a deploy key as a sops secret | — | — | — |
| 56 | Prometheus BIOS restore-on-AC-loss unknown (it stayed off after power loss) | prometheus | W (unknowable remotely) | **needs the living's word** (hands on the box) | — | the living | — | — |
| N1 | new: horizon-rs `UsbIpv4Gateway` capability and projection | horizon-rs | — | integrate | `lib/src/model.rs`, `lib/src/projection/node.rs`, `generated/horizon.rs`; the projection must emit `kind = "usbIpv4Gateway"` with exactly `downstream downstreamMac gateway uplink` | Opus write-demanding | — | a unit test projects a datom record to the exact JSON the CriomOS module asserts |
| N2 | new: lojix bumps its horizon-rs pin | lojix | — | integrate | `lojix/flake.nix:17` | Opus write-ordinary | N1 | lojix checks green on Prometheus |
| N3 | new: goldragon gateway records on ouranos (downlink → prometheus) and prometheus (downlink → zeus) | goldragon | — | integrate | `cluster-definition.datom` | Opus write | N1, f5a74e evidence, Q7 | horizon-compose output carries both records |
| N4 | new: CriomOS lock bump of lojix | CriomOS | — | integrate | `flake.lock` | CriomOS editor | N2 | running lojix accepts records with the new capability |

**Counts (56 inventory rows; N1–N4 are new work and are not counted):**

| Disposition | Rows | Count |
|---|---|---|
| Integrate as feature or declared fix | 1, 2, 3, 8, 20, 21, 24, 25, 27, 30, 34, 35, 36, 38, 40, 41, 42, 46, 48, 55 | 20 |
| Discard | 4, 5, 6, 9, 10, 11, 12, 13, 18, 19, 22, 23, 29, 32, 33, 43, 51 | 17 |
| Needs the living's word | 7, 14, 15, 16, 17, 26, 28, 37, 39, 50, 56 | 11 |
| Needs the living's word, handover part only | 21 | (counted in integrate) |
| Unknown | 45, 47, 49, 52, 53, 54 | 6 |
| Keep | 31 | 1 |
| Follows another row | 44 (follows 26) | 1 |

**⚠ Live-breaking if discarded early:** 2, 3, 20, 21, 24, 28. The GC root (row 4) protects row 3 until the 00:00 nightly GC.

## 2. Decidable tonight by da88cf vs needs the living

**Decidable by da88cf** (under the living's ~22:05 delegation: "follow the topology … I leave it to Fable's best judgment"):
- Every discard row except 7 and 14–17.
- The CriomOS-home pins (1, 3).
- Heartbeat gated off (8).
- The codex-next unit fix (20).
- Declaring the Herdr server unit, without the handover (21).
- Redeploys through Lojix (25, 42, 46).
- `max-jobs 0` for ouranos through cluster data (27). This matches the ~22:08 refinement: fallback stays a per-command flag after a witnessed remote failure.
- The registry fix (30).
- The Lojix socket fix (41).
- The Headscale SAN and trust fix with Fork A′ (34, 36). A′ is the smallest change and adds no CA with power over every name. Fork A comes later.
- The declared control URL (35).
- Turning off upstream logging (38).
- The daisy-chain producers and data (N1–N4, 24), provided the interface evidence settles Q7.
- **Interim for 26:** tonight Home arrives only through the host deploy, via CriomOS `userHomes.nix`, because that is what activated the live generation. No separate Lojix UserEnvironment activation runs on ouranos tonight. 504461 witnesses the result instead of activating.

**Questions for the living:**

- **Q1. Home owner.** Should Home be installed by the system deploy, or by its own Lojix "user environment" deploy? Today ouranos has three different Home versions claimed by three mechanisms, and none agree. Tonight it goes through the system deploy only.
- **Q2. GitHub token.** A GitHub token sits readable in `~/.config/nix/nix.conf`. May we treat it as exposed? If so, please rotate it and let it be stored encrypted for ouranos. The file stays until then, because removing it stops ouranos from reading private repositories such as field-clj.
- **Q3. Joining the tailnet.** Joining the tailnet needs a one-time key created as root on ouranos, and agents cannot use sudo. Will you run one command, or have ouranos mint the key itself at deploy time? Example: `headscale preauthkeys create`, with the output piped straight into the encrypted secret file.
- **Q4. Headscale's home.** Headscale runs on the laptop, which roams and sleeps. Should it move to Prometheus, which is always on?
- **Q5. Restarting Herdr.** The Herdr server that holds every open pane was started by hand on 09-19. Moving it under the declared unit means one restart that closes all panes. When may we do that?
- **Q6. Monitors.** Keep or drop these monitors: core-checkup (every 30 min), field-census (every 5 min), field-checkup-shadow, and field-luna-research. The last three run from working copies. Also `cloud-maintainer-chrome`, a script that drives a DigitalOcean login.
- **Q7. The daisy chain.** The chain is ouranos → Prometheus → zeus by USB. Which USB adapter is plugged into which box? Should Prometheus's WAN come from ouranos's USB port, given that Prometheus is also the house Wi-Fi router and does its own NAT? Two NAT owners break the chain test.
- **Q8. Wi-Fi.** On 09-24 an agent turned off ouranos's Wi-Fi auto-join to Prometheus's AP, to stop Prometheus's Wi-Fi driver panics. Should ouranos rejoin?
- **Q9. Power.** At the Prometheus box, set the firmware option "Restore on AC power loss" to On, so it comes back by itself after a power cut.

## 3. Dispatch waves

**Serialisation.** One Orchestrate lock per repo edit, and one editor per repo at a time:
- CriomOS-home: 00f95a first, then the CriomOS-home Opus editor.
- CriomOS: a676b3 first, then the CriomOS Opus editor.
- horizon-rs → lojix → goldragon each take their own lock.

Deploys go only through b7da5d, using Lojix's typed contract.

### Wave 2a (now; independent)

**2a.1 → Mind Sol 00f95a** (rows 1, 3)
> Outcome: CriomOS-home main pins flow `34aaf78` (0.12.2) and adds messenger-clj (main `dfcf91f0` or later) as an input, with new module `modules/home/profiles/min/messenger-clj.nix` installing messenger-clj and every `hm-*` command.
> Constraints: jj only; Orchestrate lock on CriomOS-home; commit only these paths; evaluate on ouranos, build derivations on Prometheus (`--max-jobs 0`); no activation, deploy, or `~/.local` change.
> Evidence: da88cf `reports/inventory-system.md` A1 and A2; the 0.2.5 store path is live and unrooted.
> Return: pushed revision, `nix flake check` result on Prometheus, and the HM path showing `flow` 0.12.2 and `hm-send`. Release the lock.

**2a.2 → Field Luna e71dab** (rows 6, 9–13, 19, 22, 23, 29)
> Outcome: remove these undeclared leftovers on ouranos: `~/.local/bin/message-write-configuration`; `codex-remote-control.service.d/limits.conf`; the spirit `.disabled`, `message-daemon.service.d` and `spirit-judge.service.d` drop-ins; the dji backup; the swaync mask; the `agent-intercom-fleet-cleanup` and `cf7879-overnight-poc-batch` units; the unity-local-poc-0ab019 transient (first confirm 0ab019 is closed); the 67 `fixture_harness.py` processes; `~/.config/nix/registry.json`.
> Constraints: nothing else. Do NOT touch the flow-nexus drop-in, the Flow profile element, `~/.local/bin/hm-*`, `~/.config/nix/nix.conf`, the codex-next or Herdr transients, or the Field timers. Run `systemctl --user daemon-reload` once at the end.
> Evidence: `reports/inventory-system.md` B3–B6, C, D3, E1, G2.
> Return: per item, the before/after command output. Then run `systemctl --user --failed` and `hm-list` to show nothing live broke.

**2a.3 → Mind Astra f5a74e** (row 24, N3, Q7)
> Outcome: evidence for the daisy chain ouranos → prometheus → zeus. For each node, record the integrated NIC and the USB NIC: name, MAC, driver, carrier, and the far-end peer MAC.
> Also: which link carries today's ouranos↔prometheus Yggdrasil traffic; the NAT owners on prometheus (router module, `br-lan`); and the exact datom insertion point for a `UsbIpv4Gateway.{ uplink downstream downstreamMac gateway }` record.
> Constraints: read-only; no `sudo`; mark root-only facts UNKNOWN.
> Evidence: the testing-transitive-network-topology skill's required record; the consumer is `CriomOS/modules/nixos/network/usb-ipv4-gateway.nix`.
> Return: a report in your flow with a per-node table and grades (W/C/UNKNOWN).

**2a.4 → da88cf Opus subflow (write-demanding, horizon-rs)** (N1)
> Outcome: horizon-rs gains `NodeCapability::UsbIpv4Gateway` with fields `uplink downstream downstreamMac gateway`. It projects to horizon JSON exactly as `CriomOS/modules/nixos/network/usb-ipv4-gateway.nix` asserts: `kind` "usbIpv4Gateway" and exactly those four fields.
> Constraints: jj; Orchestrate lock on horizon-rs; generated code regenerated from its source, never hand-edited; tests and checks run on Prometheus; push to main only when green.
> Return: revision, test names, the projected JSON of one fixture record.

**2a.5 → da88cf Opus subflow (read-only review)** (rows 49, 51–54)
> Outcome: a merge-or-discard verdict for messenger-clj `m6-nix-38de5b` and `m1-sender-aspect-model-38de5b`, and for the 5f38bc paused consumer pin branches. Fold in `reports/inventory-branches.md` if it has landed.
> Constraints: read-only; do not delete bookmarks.
> Evidence: neither messenger branch is an ancestor of main `dfcf91f0`; main already builds on clj-build.
> Return: for each branch, its commits not on main, whether each is already in main in substance, and the verdict with a reason.

**Not a dispatch:** wait for `reports/prometheus-pending.md`. It gates 2c.3.

### Wave 2b (after 2a.1 is pushed)

**2b.1 → Mind Sol a676b3** (CriomOS lock bump)
> Outcome: CriomOS main locks CriomOS-home at 00f95a's pushed revision.
> Constraints: jj; Orchestrate lock on CriomOS; rebase onto current main (`d193baf` or later); evaluate on ouranos, derivations on Prometheus; commit `flake.lock` only.
> Return: revision; `nix build` of `nixosConfigurations`/Lojix check for ouranos and prometheus, successful on Prometheus. Release the lock.

**2b.2 → da88cf Opus subflow (CriomOS-home editor, after 00f95a releases)** (rows 8, 20, 21)
> Outcome, in one serial lock:
> - (a) Gate `field-luna-heartbeat.nix` behind a feature that is off, unless `prompt-relay-source` can be repinned to a revision containing `fabbba0d`.
> - (b) Locate the declaration of `codex-remote-control-next`. It is not in main 478b4ea0; check the `codex-next-contract` worktree/branch. Land a fix so a stale socket cannot crash-loop it (`ExecStartPre` cleanup plus `RestartSec`).
> - (c) Declare a `herdr-server` user unit in `min/herdr.nix`, disabled on ouranos until the handover.
> Constraints: jj; lock; no activation; checks on Prometheus.
> Return: revision and check results. Name the codex-next source you found, or UNKNOWN.

**2b.3 → da88cf Opus subflow (lojix, write-ordinary)** (N2, after 2a.4)
> Outcome: lojix `flake.nix` pins horizon-rs at the N1 revision; checks green on Prometheus; push.
> Constraints: jj; lock on lojix; flake pin only.
> Return: revision and check list.

### Wave 2c (after 2b.1; ouranos first)

**2c.1 → Field Sol b7da5d** (rows 48, 25, 40; interim for 26)
> Outcome: ouranos runs CriomOS main (with 2b.1) through Lojix: a fresh coherent materialization, then `Deploy.Host` goldragon ouranos, TestActivation then ActivateNow, per the Lojix typed contract. Home arrives through the host deploy only; no separate UserEnvironment activation tonight.
> Constraints: evaluate on ouranos, derivations on Prometheus; no hand switch; do not touch the Flow drop-in or the `~/.local` links.
> Evidence: `reports/inventory-system.md` F2 and F3; b7da5d's own hotfix inventory.
> Return:
> - Lojix deployment id and its Current store path, equal to `/run/current-system`.
> - The HM path showing flow 0.12.2, `hm-send`, and field-clj.

**2c.2 → da88cf Opus subflow (CriomOS editor, after a676b3 releases)** (rows 30, 34, 35, 36, 38, 41; N4 once 2b.3 lands)
> Outcome, as one serial lock, several commits:
> - Registry `owner` fix in `nix/client.nix`.
> - `lojix.nix` owner socket = `meta.sock`.
> - Tailscale `disableUpstreamLogging`.
> - Headscale certificate regenerates on SAN mismatch.
> - New `network/cluster-pki.nix` (Fork A′: trust the Headscale leaf from goldragon).
> - Tailnet enroll oneshot using `--auth-key=file:`, inert until a `tailnetAuthKey` secret exists.
> - Then the lojix lock bump.
> Constraints: jj; lock; no secret material created or read by an agent; checks on Prometheus.
> Return: revisions per concern and check results. Name any option that needs a secret the living has not supplied.

**2c.3 → Field Sol b7da5d** (row 42; gated by prometheus-pending)
> Outcome: prometheus runs CriomOS main through Lojix `Deploy.Host` goldragon prometheus (TestActivation, then ActivateNow).
> Evidence: prometheus-pending names why deployments 19, 30 and 31 failed; address that first.
> Constraints: evaluation on ouranos; prometheus is the live router and builder, so keep the previous generation for rollback.
> Return: Lojix Current = `/run/current-system`; `systemctl --failed` empty; one remote build witnessed afterwards.

### Wave 2d (after 2c.1 is witnessed)

**2d.1 → Field Luna e71dab** (rows 2, 1-cleanup, 3-cleanup, 4)
> Outcome: first show that the HM path now provides flow 0.12.2 and every `hm-*` command. Only then:
> - Delete `flow-nexus.service.d/override.conf`.
> - `nix profile remove flow`.
> - Delete the `~/.local/{bin,libexec}` messenger links.
> - Remove the temporary messenger GC root.
> - `daemon-reload` and restart flow-nexus.
> Constraints: stop at the first failed check and report; no other paths.
> Return: `systemctl --user cat flow-nexus` (no drop-in), `flow --version`, `hm-list` output, and the roots list for 0.2.5.

**2d.2 → Field Astra 504461** (row 40)
> Outcome: witness field-clj on ouranos from the deployed Home, and run the clj-build check on Prometheus.
> Constraints: no activation; Home came through the host deploy.
> Return: the command path, version, and check result.

**2d.3 → da88cf Sonnet subflow (disk-hygiene)** (rows 32, 33, 43)
> Outcome: reclaim the listed local-build GC root groups on ouranos, keeping the Lojix audit roots and whatever backs the live generation. List prometheus's two manual roots and remove them only if non-root permissions allow.
> Constraints: the disk-hygiene skill; only after 2d.1 has returned.
> Return: roots before and after, bytes freed.

### Wave 2e (daisy chain; after 2a.3, 2c.2 with N4, and Q7)

**2e.1 → da88cf Opus subflow (goldragon editor)** (N3, row 27)
> Outcome: add `UsbIpv4Gateway` records for ouranos and prometheus from f5a74e's evidence. Remove `NixBuilder.None` from ouranos, after confirming no node's machines list names ouranos.
> Constraints: jj; lock on goldragon; data only; horizon-compose output checked.
> Return: revision and the projected records.

**2e.2 → da88cf Opus subflow (CriomOS editor)**
> Outcome: in `usb-ipv4-gateway.nix`, add a tmpfiles `r` for `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` and `/etc/systemd/field-prometheus-usb-firewall.sh`, so the hook dies in the same generation that brings the declared NAT.
> Constraints: jj; lock; checks on Prometheus.
> Return: revision.

**2e.3 → Field Sol b7da5d** (rows 24, 46)
> Outcome: deploy through Lojix in order: ouranos, then prometheus, then zeus (zeus's first Lojix deploy).
> Constraints: TestActivation first on each; the management path must survive; roll back on a failed health gate.
> Return: per host, the Lojix id and Current = running; the hook files absent on ouranos.

**2e.4 → da88cf tester subflow**
> Outcome: run every mandatory case in testing-transitive-network-topology on the chain.
> Constraints: read-only, except the cable and hotplug cases, which need the living's hands and are reported as UNKNOWN until then.
> Return: per hop, a grade (source-published / installed-running / end-to-end-proven), plus the revision running versus latest.

### Wave 2f (after the living's answers)

- Q2 → the token becomes a secret, then 2d-style removal of the `nix.conf` token line (row 28).
- Q3 → the enrollment secret, then a deploy of ouranos and prometheus, then `tailscale status` shows both peers (row 37).
- Q4 → move the controller in cluster data (row 39).
- Q5 → the Herdr handover (row 21).
- Q6 → a `field-monitoring.nix` feature, or discard (rows 7, 14–17).
- Q8 → the Wi-Fi client feature (row 50).
- Q1 → the permanent Home owner (rows 26, 44).

## 4. Critical paths

**(a) Prometheus and ouranos redeployed from main through Lojix:**
2a.1 (00f95a CriomOS-home pins) → 2b.1 (a676b3 CriomOS lock) → 2c.1 (b7da5d: fresh materialization, then Deploy.Host ouranos) → [prometheus-pending report] → 2c.3 (Deploy.Host prometheus).

The ouranos deploy does not wait for 2c.2. Those fixes ride the next deploy (2e.3).

**(b) Daisy chain declared and testable:**
2a.3 (f5a74e interface evidence) ∥ 2a.4 (horizon-rs producer) → 2b.3 (lojix pin) → 2c.2 tail (CriomOS lock of lojix) → Q7 answered → 2e.1 (goldragon records) → 2e.2 (hook removal rule) → 2e.3 (deploy ouranos → prometheus → zeus) → 2e.4 (tester).

The longest link is the producer chain, horizon-rs → lojix → CriomOS. The blocking unknown is Q7 (Prometheus's NAT ownership and USB placement).
