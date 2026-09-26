# Daisy chain: declared vs live, and the plan to make it declared

Subflow of da88cf, 2026-09-25 21:30–21:45 local (CST, UTC-6). Read-only: nothing on any machine or repo was changed. Grades: **[O]** observed this session, **[R]** read from another flow's record, **[I]** inferred, **[U]** unknown.

## 0. Answer to the living's question

The chain **works right now, but only because of hotfixes**. The two hotfixes are:

- **Ouranos hop.** A manual NetworkManager share plus a root-only firewall drop-in.
- **Prometheus hop.** Generation 55 was built from an unmerged branch and activated outside a completed Lojix deployment.

So the living's condition, "deployed properly, no hotfixes", is **not met**. What passes today is not a test of a declared chain.

At 21:31 [O] Zeus fetched `https://example.com` over IPv4, with the source forced to its wired port (`curl -4 --interface enp0s31f6`), and got 200. Its default route is via 10.18.0.1, and Prometheus's default route is via 10.44.0.1. That is an IPv4 end-to-end pass on the *running* state.

**Caveat:** Zeus is dual-homed. It also sits on Wi-Fi `Mega_2.4G_1896`, a different upstream: its 192.168.1.1 has MAC `48:96:d9:24:18:96`, while ouranos's ISP router has `10:07:1d:f8:7a:d8`. That Wi-Fi carries Zeus's IPv6 default and a metric-600 IPv4 default. **An unforced test on Zeus passes through the Wi-Fi and proves nothing about the chain.**

## 1. Declared vs live, per hop

### Hop A: ISP router to ouranos integrated NIC (uplink)

- **Live [O]:**
  - `enp0s31f6` 192.168.1.5/24, default via 192.168.1.1, DHCP lease from 192.168.1.1.
  - NM profile `Wired connection 1` (auto-generated, `ipv4.method=auto`, priority -999).
- **Declared:** nothing specific. Ouranos is an Edge/NetworkManager node, and the wired profile is NM's default.
- **Does this hop depend on the chain?** No [O]. The laptop's own Internet path never touches the USB NIC.

### Hop B: ouranos USB NIC to Prometheus eno1

**Live [O]:**

- `enp0s20f0u1c2` 10.44.0.1/24, run by NM connection `prometheus-share-temporary`:
  - UUID `92eb01d2-2087-44c9-a6ff-b2420df89d33`
  - `interface-name=enp0s20f0u1c2`, `mac-address=00:0E:C6:33:4F:97`
  - `ipv4.method=shared`, `never-default=yes`, `ipv6.method=auto`
  - autoconnect yes, priority 200, state activated
- NM's dnsmasq is running with:
  - `--listen-address=10.44.0.1 --dhcp-range=10.44.0.10,10.44.0.254,3600`
  - leasefile `/var/lib/NetworkManager/dnsmasq-enp0s20f0u1c2.leases`
- Forwarding: `net.ipv4.ip_forward=0` globally, but per-interface forwarding=1 on both NICs.
- Firewall:
  - `firewall.service` (iptables-nft) is active and `nftables.service` is inactive.
  - A drop-in `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` runs `/etc/systemd/field-prometheus-usb-firewall.sh` (root 0700, 732 B, dated 09-21, unreadable to me).
  - The NAT rules themselves are **[U]**: `iptables -S` needs root and `nft` is not installed.
- NM's `firewall-backend` is not set in `NetworkManager.conf` **[U]**: whether NM itself also installs `nm-shared` NAT is unknown.
- Generation `system-188`; configuration revision **[U]** (no `configuration-revision` file).

**Declared:**

- CriomOS main (`d193baf`) has `modules/nixos/network/usb-ipv4-gateway.nix`, imported by `network/default.nix`, landed as `e98035f` on 09-21. It:
  - activates on a `horizon.node.capabilities` entry of kind `usbIpv4Gateway` with the exact fields `downstream downstreamMac gateway uplink`;
  - requires NetworkManager, no networkd, the iptables firewall and no `networking.nat`;
  - forces NM `firewall-backend=none`;
  - declares an NM `ensureProfiles` shared profile;
  - adds iptables INPUT/FORWARD/MASQUERADE rules.
- It also **throws unless `criomos.usbIpv4Gateway.profileUuid` is set**, and nothing on main sets it. That is a node-local fact that would have to live in CriomOS.
- The check `checks/usb-ipv4-gateway` is eval-only.
- Goldragon main (`8c4d03d`) gives ouranos **no** such capability [O].
- The Horizon producers in use cannot express it (section 2).
- **So hop B is live-imperative, not declared.**

### Hop C: Prometheus eno1 (WAN) to br-lan, with Wi-Fi AP and USB downlink to Zeus

**Live [O]:**

- Uptime 15 min at 21:31 (power-outage reboot 21:15). Generation `system-55`, the only generation.
- eno1 10.44.0.148/24 by DHCP, default via 10.44.0.1.
- br-lan 10.18.0.1/24. Bridge members, both forwarding:
  - `enp199s0f0u1` (networkd `configured`, now UP/LOWER_UP)
  - `wlp195s0` (hostapd)
- Services: hostapd, kea-dhcp4-server, dnsmasq, systemd-networkd and nftables are active. `hostapd-backup-wireless` is inactive.
- `/etc/systemd/network/05-usb-eth.network`: `Name=!eno1`, `Property=ID_BUS=usb`, `Type=ether` → `Bridge=br-lan`, `ConfigureWithoutCarrier=true`. That is da85c4a's rule, not main's.
- `10-wan.network`: `DHCP=ipv4`, `KeepConfiguration=dynamic-on-stop`, `SendRelease=false`.
- Zeus `10.18.0.103` (`90:2e:16:47:ea:e3`) is REACHABLE on br-lan. From Prometheus, ping to Zeus and to 1.1.1.1 both OK, and DNS OK.

**Declared on main (CriomOS `d193baf`):**

- The Router feature, gated on `behavesAs.router`, which Horizon projects from the `Router` capability.
- It declares WAN DHCP on `routerInterfaces.wan`, br-lan, Kea, nftables forward br-lan→WAN, masquerade out WAN, and hostapd.
- It declares the USB downlink as `30-usb-eth`, **matching `Driver=cdc_ether cdc_ncm r8152 ax88179_178a asix`**.
- That rule is proven not to match links renamed at boot, because networkd records no driver for them. So on main the Zeus downlink is **declared but broken** (752e0f `reports/internet-propagation-analysis.md`, confirmed live by Field High [R]).
- The fix exists only on branch `prometheus-usb-bus-property-5f38bc` (`da85c4a`), which is what gen 55 runs [R: 752e0f log, "Field High: the USB repair is deployed declaratively on Prometheus"; I: built 21:03, two minutes after that commit].

### Hop D: Zeus integrated NIC (leaf)

- **Live [O]:**
  - `enp0s31f6` 10.18.0.103/24 by DHCP, default via 10.18.0.1 metric 100, DNS 10.18.0.1. Up 8 days.
  - Also `wlp0s20f3` on `Mega_2.4G_1896` (192.168.1.5, IPv6 global, default metric 600).
- **Declared:** Zeus is Edge. The NM wired default profile does the rest.

**Three NATs in series [O/I]:** Prometheus masquerade → ouranos (NM/drop-in) masquerade → ISP router. The skill's "one egress NAT owner, prefer Ouranos" is not met. It would be acceptable only as a named, bounded nested NAT.

## 2. The branches: what exists, what it contains

### horizon-rs (`/git/github.com/LiGoldragon/horizon-rs`, jj+git colocated; all origin heads present locally)

**The production lineage is split:**

| Consumer | Pins horizon-rs | Version | NodeCapability |
|---|---|---|---|
| lojix main `c4bba4f` (both flake and Cargo.lock) | `40d04d2` | 0.10.1 | no `OpenCodeTesting`, no `UsbIpv4Gateway` |
| CriomOS main (`horizon_2`, via lojix) | `40d04d2` | 0.10.1 | same |
| goldragon main flake (composer) | `ee8d6f8` | 0.12.0 | has `OpenCodeTesting` |

- **Version skew:** goldragon's data uses `OpenCodeTesting`, which 0.10.1's schema lacks. Lojix deployments 30 and 31 got past projection [R], so decoding evidently works through some path, but the mechanism is **[U]**. This needs to be settled before any schema change.
- `92d40e3` (09-21, "Merge USB IPv4 gateway capability into current Horizon main") is `ee8d6f8` plus:
  - ethos `UsbIpv4Gateway.{ Interface MacAddress Ipv4Cidr Interface }` as a `NodeCapability` alternative;
  - a projection to `{usbIpv4Gateway:{downstream,downstreamMac,gateway,uplink}}`, which is exactly what CriomOS's consumer reads;
  - validation (one per node, canonical unicast MAC, host CIDR /1–/30) and a contract test.
  - **Its version stays 0.12.0: no bump for a positional schema change.**
- **horizon-rs `main` = `b45d6ad`** (09-21 14:09, "Restore Datomic ClusterProposal primary API with USB gateway and OpenCodeTesting") sits on top of `92d40e3`.
  - It **replaces the ethos/projection crate with the old proposal API**: `lib/src/generated/horizon.rs` and `projection/*` are deleted, and `lib/Cargo.toml` reads `version = "0.5.1"`.
  - Its `horizon.ethos` no longer has `RouterInterfaces` or `NodeCapability`.
  - [I] It is an agent's regression or an abandoned direction. **No production consumer can follow horizon-rs main as it stands.** This is the first blocker, and it needs a ruling from Mind, who owns the horizon-rs schema.
- `usb-gateway-6db4fe` (`944ad38`, `37416e1`): the same capability written against the obsolete Aug-29 proposal API (base `f8c5808`). Its content was merged into `92d40e3`. **Discard the branch.**
- `prometheus-usb-downlink-5f38bc` (`fed0a12`, 09-24, base `40d04d2`) appends `Option<MacAddress>` to `RouterInterfaces`, projected as `usbLanMacAddress`, with a contract test. **Positional schema change, no version bump (0.10.1).** It lacks `OpenCodeTesting`, so it cannot decode goldragon main [I].

### lojix

- `prometheus-usb-downlink-5f38bc` (`387c13b`) repins only the flake input to horizon `fed0a12` over `git+ssh`. Cargo.lock still says `40d04d2`, so the pins disagree.
- Not on main. **Discard** with the MAC approach.

### goldragon

- `prometheus-usb-downlink-5f38bc` (`1781f07`, base = main `8c4d03d`) appends `Some.«00:0e:c6:ad:21:5d»` to Prometheus's `RouterInterfaces`.
  - It needs horizon `fed0a12` plus `OpenCodeTesting`, a combination that exists nowhere.
  - **Discard.** It is superseded by bus-role matching, which needs no data.
- `usb-gateway-data-753e69` (`a911515`) adds `UsbIpv4Gateway.{enp0s20f0u1c2 00:0e:c6:33:4f:97 10.44.0.1/24 enp0s31f6}` to ouranos. It sits on the obsolete `proposal.datomic` lineage (base `be4bf4d` 08-13, 4 ahead / 10 behind). **Discard the branch; reuse the values.**

### CriomOS (`/git/github.com/LiGoldragon/CriomOS`; main `d193baf`)

- **`prometheus-usb-bus-property-5f38bc` `da85c4a`.**
  - Its own change touches 3 files:
    - `router/default.nix`: `30-usb-eth` → `05-usb-eth`, `Property=ID_BUS=usb`, `Name=!<wan>`;
    - `network/networkd.nix`: the same for center non-routers, renamed to `05-usb-eth` so it sorts before the `10-main-eth` catch-all;
    - `checks/router-usb-downlink-binding`, eval-level assertions including the negative case that the PCI WAN does not match, registered in `flake.nix`.
  - It sits on top of 12 **pin-only commits** from `field-astra-5f38bc-flow-pins` (home/lojix/Flow pins, not on main). Its base is `864e01b`; main is 3 commits ahead, all pin/lock changes.
  - Main has not touched `router/` or `network/` since the base, so there are **no module conflicts**; `flake.nix`/`flake.lock` pin hunks will conflict [I].
  - **Installed-running on Prometheus [O/R]**, with the Zeus lease and IPv4 Internet witnessed. **Rebase just `da85c4a`'s own diff onto main, drop the pin commits, and merge.**
- **`prometheus-usb-downlink-5f38bc` `de5ac1b`:** MAC match from `usbLanMacAddress`, plus a lojix repin to the ssh URL. **Discard**: superseded, and it depends on the discarded schema.
- **Unbookmarked `e92a336`** (Mind's "USB downlink activation source fix", workspace `usb-downlink-source-fix`):
  - the same bus-role match;
  - plus a `router-usb-ethernet-reconcile` oneshot (`networkctl reload`, then `reconfigure` of the USB non-WAN links on each generation switch);
  - plus a check `router-usb-downlink-activation`.
  - The reconcile addresses a real gap: a switch that installs a new `.network` does not revisit links that already exist. **Take the reconcile unit and its check on top of da85c4a.** Its match hunks duplicate da85c4a (keep da85c4a's `05-` naming).
- **Unbookmarked `e0aef3d`** ("Match non-router USB Ethernet before generic Ethernet"): covered by da85c4a's networkd hunk. **Discard.**
- **`usb-gateway-consumer-6db4fe` `9842f51`:** already on main as `e98035f`. **Delete the bookmark.**
- **CriomOS-home:** no network branches are relevant (only Active Network widget branches).

**Ouranos-side downlink work:** none on any branch beyond the consumer already on main and the stale goldragon data branch [O].

## 3. The declared end shape, per the living

Verbatim, from `flows/*/vision`. `Vision/` holds nothing on this, and `vision-raw/` has nothing relevant.

1. 2026-09-22, `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`: "The built-in port is for upstream, and the USB is for downstream. We just reuse that pattern, and no matter how we plug things in, that's how I would want it to work, right? Kind of statelessly."
2. Same file: "…it becomes a Wi-Fi access point itself. That would be a feature, like an opportunistic Wi-Fi access point or something like that, or a mode: optional Wi-Fi access point, right?"
3. 2026-09-23, `flows/836818/vision/network.md`: "It never really worked well from making Uranus [Ouranos] the upstream supplier to Prometheus. Do you need to create a network hierarchy kind of thing or with features? I don't know."
4. 2026-09-24, `flows/e51411/vision/network.md`: "Well the concept of router is just a feature now so it's not a router per se. It has that feature. … Can we just make a really really simple fix that doesn't try to reimagine everything and introduce a bunch of other variables"
5. 2026-09-25, `flows/752e0f/vision/internetPropagation.md`: "This is a feature, right? Prometheus would ostensibly have the same feature so that USB Ethernet devices become downlinks, so it would propagate any internet access it has through that."
6. 2026-09-25 ~22:15, `flows/da88cf/vision/daisyChain.md`: "See if the lambda [sic] daisy chain setup works once you've deployed it properly and there are no hotfixes to make it work."

No record found for the words "daisy chain" as network before item 6, or for "optional AP" beyond item 2.

**What the vision implies [I]:**

- **One feature, USB-downlink Internet propagation**, present on both ouranos and Prometheus. The integrated NIC is the uplink and any USB Ethernet is a downlink, selected by bus role rather than by name or MAC ("statelessly").
- **The Wi-Fi AP is a separate, optional feature** (item 2). Prometheus's "Router" today bundles three things:
  - (a) propagation with DHCP/DNS/NAT;
  - (b) a USB downlink bridged into the LAN;
  - (c) the AP.
- So **Prometheus's router is the same propagation feature with the AP added**. Item 4 says the router is "just a feature".
- Item 4's "really simple fix" argues against a schema-wide rework tonight.

**Tension:** the existing `UsbIpv4Gateway` payload names interfaces and a MAC (node-specific, not stateless). The Prometheus fix that works selects by `ID_BUS=usb`. The minimal honest shape:

- **Horizon:** a capability `UsbDownlink.{ Ipv4Cidr }`, carrying only the downlink subnet (the one value that must differ per node: ouranos `10.44.0.1/24`, Prometheus `10.18.0.1/24`). The uplink is the integrated (non-USB) NIC, and the downlinks are `ID_BUS=usb`.
- **Router** remains the node that also bridges the AP into the same LAN. Later split into `UsbDownlink` + `OptionalAccessPoint`; not tonight.
- **Fallback:** if Mind prefers the already-written `92d40e3` `UsbIpv4Gateway` (explicit interfaces + MAC), it works for ouranos as a first step, at the cost of the "no matter how we plug" property. **This choice is a ruling for Mind/the living, not for me.**

## 4. Producer-first implementation plan

Step 0 is a ruling. Everything after it is ordinary Field work.

### Step 0: settle horizon-rs main (ruling)

- Reset or revert horizon-rs main from `b45d6ad` back onto the ethos lineage (`92d40e3`).
- Decide 0.10.1 vs 0.12.0 as the one version lojix and goldragon share. Today lojix is 0.10.1 and goldragon composes with 0.12.0.
- Without this, no schema change can be consumed.

### Step 1: horizon-rs

- On the ethos line (`92d40e3`), either:
  - keep `UsbIpv4Gateway` (fallback path), **or**
  - add `UsbDownlink.{ Ipv4Cidr }` to `NodeCapability`, projected as `{usbDownlink:{gateway}}`, validating one per node and a canonical host CIDR.
- **Bump to 0.13.0** (positional schema change).
- Add a contract test.
- Publish; repin lojix (flake **and** Cargo.lock, same rev) and the goldragon flake.

### Step 2: goldragon

- Add to ouranos's capability vector `UsbDownlink.{10.44.0.1/24}` (or the `UsbIpv4Gateway` record from `a911515`).
- Declare nothing new on Prometheus: its Router already covers its downlink.
- Keep the subnets non-overlapping: 10.44.0.0/24 vs 10.18.0.0/24.

### Step 3: CriomOS

1. Rebase `da85c4a`'s three-file diff onto main, plus e92a336's `router-usb-ethernet-reconcile` unit and check.
2. Adapt `usb-ipv4-gateway.nix`:
   - key it on the ruled capability;
   - match the downlink by NM `match.path "*-usb-*"` or a udev property instead of name/MAC, if `UsbDownlink` is chosen;
   - **drop the mandatory `profileUuid`**: derive a stable UUID from the node name, so the fact stays in data and not in CriomOS.
3. Add an activation step on NM nodes that **deactivates (autoconnect=no, down) any undeclared `ipv4.method=shared` profile on the same device**. On ouranos that is `prometheus-share-temporary`; delete it only after acceptance.
4. Remove the `90-field-prometheus-usb.conf` firewall drop-in in the same migration. It lives in `/etc/systemd/system.control`, a persistent runtime override outside Nix: a one-shot migration or a manual root step, recorded.
5. Checks: keep the eval assertions, and add a **NixOS VM test (`runNixOSTest`) of the chain**, run on Prometheus per tonight's build order:
   - node `isp`: DHCP + DNS + an HTTP "internet" host;
   - node `ouranos-like`: NM, capability → gateway on a QEMU `usb-net` device (qemu-xhci + `-device usb-net`, which yields a real `ID_BUS=usb`; feasibility [I]);
   - node `prometheus-like`: the router module with hostapd off or `mac80211_hwsim`, WAN on the PCI virtio NIC, downlink on a `usb-net` device;
   - node `zeus-like`: plain DHCP client;
   - assertions: leases at each hop, gateway ping before DNS, DNS, then HTTP from the leaf through the forced interface;
   - negative cases: a PCI NIC never becomes a downlink; no Internet when the upstream has none; a second shared profile fails the assertion.

### Step 4: Lojix deploys, order and rollback

1. **Prometheus first.** For it, the change is almost a no-op: gen 55 already carries the bus-role rule, so this replaces the branch-built generation with a main-built one through Lojix, recorded.
   - Use `switch`, not `boot`, and **no reboot**: networkd is kept running by design, and `KeepConfiguration=dynamic-on-stop` holds the WAN lease.
   - Rollback: previous generation (55) via Lojix or `switch-to-configuration` of `system-55`.
   - Witness: `05-usb-eth` unchanged, `enp199s0f0u1` in br-lan, Zeus lease REACHABLE, forced-interface curl from Zeus.
   - Pause builds on Prometheus first, or accept that they may be interrupted.
2. **Ouranos second.** Its own Internet path is untouched.
   - The downstream blinks for seconds while NM swaps profiles on `enp0s20f0u1c2`: the address drops and dnsmasq restarts with the same per-interface leasefile, so Prometheus should keep 10.44.0.148 [I].
   - Any closure copy over 10.44.0.x must be complete before activation. Lojix copies before it switches [I].
   - Rollback is local and does not need the link: `nixos-rebuild switch --rollback` or boot 188, then `nmcli con mod prometheus-share-temporary autoconnect yes && nmcli con up …`. The profile is kept, disabled, until acceptance.
3. **Then run the transitive test per the skill**, section 5.

## 5. Risks to the sleeping living, and the activation window

- **Ouranos's own Internet (the laptop the living sleeps next to): no dependency on the chain [O].**
  - Residual risk: an ouranos switch that restarts NetworkManager bounces `Wired connection 1` for a few seconds, which live agent sessions would ride out.
  - The Headscale/Tailscale x509 fault [R] is separate.
- **Circularity:** ouranos's `goldragon.criome` Wi-Fi profile must stay `autoconnect=no` / `never-default` [R]. Otherwise ouranos could take its default route from Prometheus's AP, which takes Internet from ouranos.
- **Prometheus reboot** drops:
  - the AP (the living's phone), and it comes back at txpower 3 dBm, regdom PL [R];
  - Zeus's downlink;
  - the Nix builder and cache used tonight.
  - After the power outage it recovered unattended in about 12 s of DHCP [R]. Still: **no reboot tonight; `switch` only**.
- **Zeus** keeps Internet through its own Wi-Fi even if the chain breaks [O], so a broken chain does not strand it. The same fact makes an unforced test a false pass.
- **Safe window:**
  - after the builds on Prometheus finish or are paused;
  - with one agent holding the Prometheus ssh management path (it rides hop B, so ouranos's activation briefly severs it; deploy Prometheus first while hop B is still the known-good manual one);
  - only after the VM test is green.
- **Success witnesses** (each distinct):
  - *Source-published:* horizon, goldragon and CriomOS revisions on main, checks and VM test green.
  - *Installed-running:*
    - ouranos: `nmcli` shows only the declared `usb-ipv4-gateway` shared profile active; the manual one is inactive; the drop-in is gone; iptables shows the `criomos-usb-gateway-*` rules (root).
    - Prometheus: runs the Lojix-recorded main generation with `05-usb-eth` + reconcile.
  - *End-to-end-proven:* a fresh lease at each hop, and hop-by-hop gateway ping → DNS → HTTP, ending at Zeus with `curl -4 --interface enp0s31f6` = 200. Repeat after a USB unplug/replug on each hop and after a DHCP renew. IPv6 is not covered: the path is IPv4-only by construction [R].

## Sources

- Live, this session:
  - ouranos: `ip -br addr`, `ip route`, `nmcli`, `sysctl`, `pgrep dnsmasq`, `systemctl cat firewall`;
  - Prometheus over ssh: `ip`, `bridge link`, `networkctl`, `/etc/systemd/network/*`, `systemctl is-active`, `ip neigh`, pings;
  - Zeus over ssh: `ip`, `resolvectl`, `nmcli`, forced-interface `curl -4`.
- Repos (read-only git/jj, `--ignore-working-copy`): `/git/github.com/LiGoldragon/{horizon-rs,lojix,goldragon,CriomOS,CriomOS-home}`; workspaces under `/home/li/wt/github.com/LiGoldragon/CriomOS/{prometheus-usb-*,usb-downlink-*,usb-share-6db4fe,usb-gateway-main-753e69}`.
- Revisions:
  - horizon-rs `40d04d2`, `ee8d6f8`, `92d40e3`, `b45d6ad`, `fed0a12`, `944ad38`, `37416e1`;
  - lojix `c4bba4f`, `387c13b`;
  - goldragon `8c4d03d`, `1781f07`, `a911515`;
  - CriomOS `d193baf`, `864e01b`, `da85c4a`, `de5ac1b`, `e92a336`, `e0aef3d`, `9842f51`, `e98035f`.
- Records: `flows/da88cf/reports/wifi-prometheus.md`; `flows/f5a74e/reports/cluster-topology-roles.md`; `flows/752e0f/reports/internet-propagation-analysis.md`; `flows/752e0f/log.md` (lines ~125–135, 49–79 of the 09-25 section); `.claude/skills/testing-transitive-network-topology/SKILL.md` (read as a file for content).
- Vision: `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`, `flows/836818/vision/network.md`, `flows/e51411/vision/network.md`, `flows/752e0f/vision/internetPropagation.md`, `flows/5f38bc/vision/prometheusZeusInternetPropagationAndTailnetAlternatives.md`, `flows/da88cf/vision/daisyChain.md`, `flows/e71dab/vision/tailscale.md`.
