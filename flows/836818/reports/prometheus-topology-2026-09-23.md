# Ouranos to Prometheus: intended, configured, and how it got that way (Psyche High 836818)

## 1. Intended topology, and what is actually configured

### What the psyche has said

The governing statement, verbatim, from `/home/li/primary/flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md` (living, direct message to Field Medium `753e69`, 2026-09-22):

> "Upstream of Uranus is the ISP router, and I have the USB of Uranus to Prometheus, which should be getting it into its built-in port."

> "Prometheus has a USB Ethernet that goes to Zeus, which should be getting internet from him through the network cable that Zeus's built-in port has. Let's make that the transitive topology, so it's a testing skill. It's a temporary situation also, but it doesn't even matter. It shouldn't matter. The built-in port is for upstream, and the USB is for downstream. We just reuse that pattern, and no matter how we plug things in, that's how I would want it to work, right? Kind of statelessly."

The present question, from `/home/li/primary/flows/836818/vision/network.md` (living, STT, 2026-09-23, direct to this seat):

> "It lies with how we reconfigure the network. It never really worked well from making Uranus [Ouranos] the upstream supplier to Prometheus."

And the earlier hypothesis, same file, 2026-09-23, relayed from Field High `0ad137`:

> "That means maybe Yigdrasil [Yggdrasil] is firewalled on that USB Ethernet device."

Two older records bound it. `/home/li/primary/flows/024bc7/vision/network.md` (STT, 2026-09-13): "all the hosts are connected through a USB Ethernet and create a network where everybody is wired together" — and the living marked it "not ready yet." `/home/li/primary/Vision/deployment.md`: "Zeus is a stable node, and stable nodes are not where testing happens."

### Ouranos as configured

Ouranos's declared record is in `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom` (same content in the canonical worktree's `proposal.datom`). It is `Edge / LowPower / NextGeneration / Nordvpn / HardwareVideo / TailnetClient / TailnetController / NixBuilder.None / OpenCodeTesting / PersonaDevelopment`, and its `routerInterfaces` field is **`None`**. Its Yggdrasil address is `201:6de1:5500:7cac:2db9:759e:42d2:fb1d`.

So in the declared object, **Ouranos names no interfaces at all** — no uplink, no downlink, no gateway, no NAT, no DHCP server. Because it is `Edge` and not `center`/`router`, Horizon's projection sets `enableNetworkManager = true` (`horizon-rs/lib/src/projection/viewpoint.rs`), consumed at `CriomOS/modules/nixos/normalize.nix`. `CriomOS/modules/nixos/network/networkd.nix` is gated `center && !router`, so systemd-networkd is inactive on Ouranos and NetworkManager owns every link. The generic USB share in that file is `10.47.0.1/24` and does not select Ouranos.

Everything that makes Ouranos an upstream supplier is **runtime state, not configuration**. Per `/home/li/primary/flows/6db4fe/reports/network-durable-source.md` (2026-09-21) and `network-chain-attempts.md` Attempts 3, 6, 8, 9:

- a NetworkManager profile `prometheus-share-temporary` on USB `enp0s20f0u1c2`, MAC-pinned, `ipv4.method=shared`, `10.44.0.1/24`, `never-default=yes`, **IPv6 disabled**, autoconnect priority 200, saved to `/etc/NetworkManager/system-connections/`;
- four iptables rules — DHCP UDP/67 in on USB, DNS UDP/TCP 53 in from `10.44.0.0/24`, and `MASQUERADE` for `10.44.0.0/24` only out `enp0s31f6`;
- a root-installed `/etc/systemd/field-prometheus-usb-firewall.sh` plus a drop-in at `/etc/systemd/system.control/firewall.service.d/` that re-adds those rules on firewall start and reload.

The report is explicit that this is "an operational host-specific stopgap … not the accepted network-neutral CriomOS configuration."

Ouranos's firewall on the Yggdrasil ports comes only from the generic `CriomOS/modules/nixos/network/yggdrasil.nix`: `allowedUDPPorts = [9001]`, `allowedTCPPorts = [10001]`, `trustedInterfaces = ["yggTun"]` — global, not per-interface. So Yggdrasil is **not** port-blocked on Ouranos's USB link.

### Prometheus as configured

Prometheus's declared record in the same file is `Center / LargeAi / Router / TailnetClient / NixBuilder.Some.6 / NixCache / VmHost`, with `routerInterfaces` present:

- **WAN / uplink = `eno1`** (integrated NIC)
- AP radio `wlp195s0`, 2.4 GHz, channel 6, WiFi4, WPA3-SAE
- backup AP `wlp199s0f0u4`, SSID `criome-backup`, channel 11
- Yggdrasil address `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`

Because `behavesAs.router` is true, `enableNetworkManager` is false and `CriomOS/modules/nixos/router/default.nix` applies: systemd-networkd owns the links, `networking.firewall.enable = false`, `networking.nat.enable = false`, nftables is the sole firewall and NAT owner.

- `10-wan.network` matches `eno1`, `DHCP = "ipv4"`, `KeepConfiguration = "dynamic-on-stop"`. IPv4 only — no RA or DHCPv6 client. Link-local IPv6 exists by networkd default, which matches the observed `fe80::8647:9ff:fe75:8868`.
- `30-usb-eth` matches **by driver only** (`cdc_ether cdc_ncm r8152 ax88179_178a asix`) and bridges every match into `br-lan`, `ConfigureWithoutCarrier = true`. No interface name, no MAC.
- `40-br-lan` gives the bridge `10.18.0.1/24` (from `CriomOS-lib/lib/default.nix`).
- Forwarding: `net.ipv4.conf.all.forwarding` and `net.ipv6.conf.all.forwarding` both true.
- NAT: `table ip nat { chain postrouting { … oifname "eno1" masquerade } }` — unconditional masquerade of everything leaving `eno1`.
- DHCP server: Kea on `br-lan` only, pool `10.18.0.100–10.18.0.240`. DNS: dnsmasq on `10.18.0.1`.
- hostapd on `wlp195s0`, bridged into `br-lan`; a hand-rolled `hostapd-backup-wireless` unit on the USB radio, also bridged into `br-lan`, started by udev hotplug.

The firewall, verbatim from `modules/nixos/router/default.nix`:

```
chain input { type filter hook input priority 0; policy drop;
  ip6 saddr fe80::/64 ip6 daddr fe80::/64 udp dport 9001 accept
  ip6 saddr fe80::/64 ip6 daddr fe80::/64 tcp dport 10001 accept
  tcp dport ssh accept
  ...
  iifname { br-lan, wlp195s0, yggTun, wlp199s0f0u4 } accept
  iifname "eno1" ct state { established, related } accept
  iifname "eno1" icmp type { echo-request, ... } counter accept
  iifname "eno1" counter drop
  iifname "lo" accept }
chain forward { policy drop;
  iifname { br-lan } oifname { "eno1" } accept
  iifname { "eno1" } oifname { br-lan } ct state { established, related } accept
  ... }
```

**This rule order settles the living's hypothesis.** The two link-local Yggdrasil accepts sit *above* the `eno1` drop, and `tcp dport ssh accept` is unconditional. So on Prometheus, link-local Yggdrasil is **not** firewalled on the Ouranos-facing link, SSH is open there, and everything else inbound on `eno1` is dropped. That is exactly why `0ad137`'s 2026-09-23 report saw "USB TCP22 connects immediately" while "USB TCP80 times out." Source confirms the port-80 timeout is deliberate policy, not a fault.

`CriomOS/modules/nixos/router/yggdrasil.nix` adds a *second* copy of those same two rules in a separate `table ip6 yggdrasil-local` at priority `-100` — redundant with the inline pair.

### Yggdrasil, cluster-wide

`CriomOS/modules/nixos/network/yggdrasil.nix` is identical on every node:

```nix
MulticastInterfaces = [ { Regex = ".*"; Beacon = true; Listen = true; Port = ports.linkLocalTCP; } ];
```

Ports are `multicast = 9001`, `linkLocalTCP = 10001` (`CriomOS-lib/lib/default.nix`). There is **no `Peers` list and no `AllowedPublicKeys` anywhere in any repository.** Peering is IPv6 link-local multicast discovery and nothing else. That single fact carries most of the present fault.

---

## 2. History

**Before.** `/home/li/primary/flows/753e69/reports/network-path-plan-2026-09-21.md`: "Prometheus's reported 2026-09-21 router state was built-in WAN `eno1` at `192.168.1.16/24`, default via `192.168.1.1`; `br-lan` was `10.18.0.1/24`." Prometheus was a router hanging directly off the house LAN. Ouranos was an ordinary client at `192.168.1.5`.

**2026-09-21, the change.** `/home/li/primary/flows/6db4fe/reports/prometheus-connectivity.md`: a NetworkManager profile was added on Ouranos's USB — `ipv4.method shared`, `10.44.0.1/24`, `never-default yes`, **IPv6 disabled**. *Worked:* Ouranos kept Internet, dnsmasq served DHCP and DNS. *Failed:* "Prometheus has **not** been observed on this link… RX counter remained 0 bytes / 0 packets… ARP for `10.44.0.2` failed. Prometheus's Yggdrasil address… did not answer ICMPv6 or SSH port 22."

**Attempts 3–4** (`network-chain-attempts.md`) established the roles: Prometheus `eno1` had "carrier at 1 Gbps and IPv6 link-local but **no IPv4 or default route**"; its USB `enp199s0f0u1` was "intentionally bridged into `br-lan` alongside AP `wlp195s0`." Attempt 4 also recorded: "The Ouranos share deliberately has IPv6 disabled."

**Attempt 5** proved the cable by packet capture and named the blocker: "the `nixos-fw` INPUT chain has no ingress allowance on the USB interface for DHCP UDP/67 or DNS TCP/UDP/53 and ends in a drop. IPv4 NAT `POSTROUTING` has no masquerade rule."

**Attempt 6 — the moment Ouranos actually became upstream supplier.** Four runtime iptables rules added. *Worked:* "Ouranos dnsmasq logged DISCOVER, OFFER, REQUEST, and ACK… leasing `10.44.0.148/24`… Prometheus resolved `cache.nixos.org` and `curl -4 -I https://cache.nixos.org` returned HTTP/2 200… **The Ouranos built-in Ethernet → USB share → Prometheus first hop is now working.**"

**Attempt 7** proved the whole chain to Zeus and a Nix store handshake (`Trusted: 1`). **Attempt 8** persisted the NM profile. **Attempt 9** installed the firewall drop-in; in the same window both downstream ports went `NO-CARRIER` at 12:37:13, before the 12:39:33 reload. **Attempt 10** could not restore carrier.

**On the source side, the same day,** four changes were authored (from the CriomOS/Horizon/Goldragon sweep): `944ad38` "Add typed USB IPv4 gateway service" and `37416e1` "Enforce one USB IPv4 gateway per node" in horizon-rs; `a911515` in goldragon assigning Ouranos `UsbIpv4Gateway.{enp0s20f0u1c2 00:0e:c6:33:4f:97 10.44.0.1/24 enp0s31f6}`; `9842f51` in CriomOS adding the consumer module. **None of these landed.** The only landed CriomOS commit is `114fcbd` (2026-09-21, merged by `6e1ca7b`), "Recover router WAN DHCP after late upstream availability" — a oneshot service and 2-minute timer that runs `networkctl reconfigure eno1` when the WAN has carrier but no IPv4 default route. Its test fixture pins the expected result as `default via 10.44.0.1 dev eno1`, i.e. Ouranos's gateway address.

**2026-09-21, 16:00–16:30 local: the outage onset.** `/home/li/primary/flows/6db4fe/reports/prometheus-uplink-reliability-2026-09-22.md`: Yggdrasil "records inbound/outbound TCP sessions to Zeus timing out at 16:14 and 16:16 local and sessions to Prometheus timing out at 16:16. **The sessions used Ouranos's Wi-Fi link-local interface.**"

**2026-09-22.** `prometheus-builder-recovery-2026-09-22.md`: Ouranos's Wi-Fi profile for `goldragon.criome` was changed — `ipv4.never-default=yes`, `ipv6.never-default=yes`, and both `ignore-auto-dns=yes` (prestate `no` for all four). One activation "stopped in 802.11 authentication: the kernel reports three authentication transmissions without an answer." The report states plainly: "These settings… did **not** repair the failed association." TCP/22 to the Yggdrasil name timed out after 7 seconds.

**2026-09-23.** Prometheus was restarted by the living (`field/0ad137/vision/prometheusConnection.md`). At 12:04 local, `flows/4b0f60/reports/mega-network-diagnosis-mission.md` records Ouranos Wi-Fi still on `goldragon.criome` at `10.18.0.102/24`, Prometheus `eno1` back at `10.44.0.148/24` via `10.44.0.1`, and "USB ARP, TCP/22 and strict ordinary SSH succeeded over USB and Ygg." By ~22:42 UTC, `field/0ad137/reports/prometheus-route-20260923.md` records Ouranos Wi-Fi as **`Mega_2.4G_1896` at `192.168.1.9`** and the overlay gone.

---

## 3. Where the configured state contradicts the intended topology, or itself

1. **Prometheus's link to Ouranos is declared as its WAN.** `routerInterfaces.wan = eno1` was written when `eno1` faced the ISP. Making Ouranos the supplier pointed that declared WAN at a downlink of a node inside the cluster, so Prometheus now applies hostile-Internet policy — `iifname "eno1" counter drop`, forward only `br-lan → eno1` — to an intra-cluster transit link. Nothing in the declared object changed to say otherwise. *This is the structural answer to the living's sentence.*

2. **Two NAT owners in series.** Prometheus masquerades everything out `eno1`; Ouranos masquerades `10.44.0.0/24` out `enp0s31f6`; the house router NATs again. `flows/4b0f60/reports/network-nexus-design.md` (2026-09-22) states the intent: "The preferred durable arrangement is routing at each hop and **one egress NAT owner at Internet-edge Ouranos**. Prometheus routes its downstream prefixes." The configured state is the nested NAT that document names as the thing to avoid.

3. **Ouranos's gateway role exists nowhere in the declared object.** It is a NetworkManager profile, four iptables rules, and a root-installed shell script under `/etc/systemd/system.control`. This contradicts `vision-raw/setupIndependentInterfaces.md` (2026-08-14): "I don't want setup-specific scripts in general repos. Everything must be setup-independent with simple clear interfaces" and "The interface is lojix and meta-lojix CLI only."

4. **A landed test asserts a fact no landed source produces.** `checks/router-wan-recovery/default.nix` expects `default via 10.44.0.1 dev eno1`, but `10.44.0.1` comes only from the unlanded `UsbIpv4Gateway` assignment. The check encodes the new topology while the configuration does not.

5. **`30-usb-eth` matches USB Ethernet by driver alone and bridges it into `br-lan`.** Ouranos's ASIX `cdc_ncm` adapter matches that same driver list. Move the cable to a Prometheus USB port and Prometheus bridges its own upstream into its LAN — two DHCP servers on one segment, upstream and downstream merged at L2. The `testing-transitive-network-topology` invariants require ambiguous USB NIC selection and network-manager ownership conflict to fail closed; this fails open.

6. **Prometheus's USB downlink is not a downlink.** The intended chain gives Zeus its own segment; the configuration makes Prometheus's USB port a bridge member of `br-lan` sharing one subnet, one DHCP server and one broadcast domain with the AP. `network-nexus-design.md` requires "each downstream has a distinct subnet, DHCP/DNS policy and explicit forwarding rule; links are not accidentally bridged."

7. **Ouranos was simultaneously Prometheus's supplier and its client.** While Ouranos held `10.18.0.102/24` from Prometheus's AP it was a downstream client of the node it was feeding. Today it holds `192.168.1.5` on wired and `192.168.1.9` on Wi-Fi — two interfaces on one subnet. The design says the controller "refuses… prefix overlap, link loops."

8. **Duplicate Yggdrasil firewall ownership.** The link-local accepts are written inline in `router/default.nix` at priority 0 *and* again in `router/yggdrasil.nix` as a separate `ip6` table at priority -100. Meanwhile the generic module's `networking.firewall.allowedTCPPorts`/`trustedInterfaces` are inert on Prometheus because `firewall.enable = false`.

9. **The candidate fix would make the present fault permanent.** `usb-ipv4-gateway.nix` (unlanded, `9842f51`) sets `ipv6.method = "disabled"` on the downstream profile — the exact setting that is currently preventing Yggdrasil from peering over USB. Landing it as written durably encodes the overlay outage.

10. **An internal conflict in the record itself.** On 2026-09-23 at 12:04 local, `4b0f60`'s report has Ouranos Wi-Fi on `goldragon.criome` at `10.18.0.102/24` with no Mega profile; at ~22:42 UTC the same day, `0ad137` has it on `Mega_2.4G_1896` at `192.168.1.9`. Either an unrecorded reassociation happened between them, or one observation is wrong. `4b0f60`'s own text says station-only Mega migration ("Decision B") was **not executed**.

---

## 4. The three most likely causes of the present fault

The fault: the Yggdrasil overlay is unreachable over both the Wi-Fi path and the USB path, while SSH over USB works.

### Cause A — IPv6 is fully disabled on Ouranos's USB downlink, so Yggdrasil cannot discover a peer there

**For.** `field/0ad137/reports/prometheus-route-20260923.md` (2026-09-23): "Ouranos USB NM profile prometheus-share-temporary has ipv6.method=disabled and disable_ipv6 sysctl 1. No USB IPv6 link local or Ygg listener. Prometheus eno1 has fe80::8647:9ff:fe75:8868 and Ygg 10001 listening." The source config peers only by link-local multicast (`MulticastInterfaces` `Regex = ".*"`, no `Peers`). With no `fe80` address on the link, Ouranos emits no beacon and opens no listener there. The profile has carried `IPv6 disabled` since its creation on 2026-09-21 (`prometheus-connectivity.md`), and Attempt 4 flagged it explicitly.

**Against.** Nothing in the sources contradicts it. It explains the USB half only — it does not explain the Wi-Fi half.

**Deciding observation.** On Ouranos, `ip -6 addr show enp0s20f0u1c2` and `cat /proc/sys/net/ipv6/conf/enp0s20f0u1c2/disable_ipv6`. A `fe80::` address with `disable_ipv6 = 0` refutes it; absence with `1` confirms it. The bounded repair `0ad137` already proposes — link-local-only IPv6 on that profile with `never-default` and `ignore-auto-dns` — is the test.

### Cause B — Ouranos and Prometheus no longer share any L2 broadcast domain on Wi-Fi

**For.** Every historical Yggdrasil session between them ran over Wi-Fi: `prometheus-uplink-reliability-2026-09-22.md` Round 4 — "The sessions used Ouranos's Wi-Fi link-local interface," timing out 16:14–16:16 on 2026-09-21. Ouranos is now on `Mega_2.4G_1896` at `192.168.1.9` (`0ad137`, 2026-09-23), not on Prometheus's `br-lan`. Prometheus's declared radio is a single 2.4 GHz channel-6 AP and `4b0f60` reports it has "no Mega profile," so it cannot join Mega as a station while serving its AP. `0ad137` also records Prometheus peered only with `200:17f7:4fad:e50b:a50c:2048:2169:41f7` via `br-lan` — which the cluster definition identifies as **Zeus** — and not with Ouranos's identity `201:6de1:…`. Multicast does not cross the router between `192.168.1.0/24` and `10.18.0.0/24`.

**Against.** `4b0f60`'s 12:04 reading the same day still has Ouranos on `goldragon.criome` at `10.18.0.102/24`, and at that time SSH over Ygg worked — so the Wi-Fi association may be intermittent rather than abandoned. `prometheus-builder-recovery-2026-09-22.md` shows the association failing at 802.11 authentication with no reply, which is a radio-layer failure, not a subnet-topology one.

**Deciding observation.** On Ouranos, `nmcli -f NAME,DEVICE,STATE connection show --active` plus `ip -br addr`. If Wi-Fi is associated to `Mega_2.4G_1896` on `192.168.1.0/24` while Prometheus's AP serves `10.18.0.0/24`, there is no shared segment and this is confirmed. If Ouranos is on `10.18.0.x` and still not peering, it is refuted and points to Cause C or a radio fault.

### Cause C — Yggdrasil has no configured peers, so there is no fallback over the one working path

**For.** `CriomOS/modules/nixos/network/yggdrasil.nix` contains only `MulticastInterfaces`; the sweep of CriomOS, CriomOS-lib, criomos-horizon-config and CriomOS-test-cluster found **no `Peers` list and no `AllowedPublicKeys` anywhere**. The USB link carries working IPv4 — SSH connects immediately to `10.44.0.148` — but Yggdrasil has no way to use it, because a static peer entry (`tcp://10.44.0.148:10001`) is the only mechanism that would, and none exists. This is why the overlay is down on *both* paths at once while the IPv4 transport underneath one of them is healthy.

**Against.** This is a design gap rather than a regression; the overlay worked on 2026-09-21 and again briefly on 2026-09-23 morning. It is a necessary condition for the fault, not the trigger.

**Deciding observation.** On either host, read the effective merged Yggdrasil config (the runtime JSON assembled in the unit's `preStart`) and check for a `Peers` array. An empty `Peers` confirms that multicast is the sole peering mechanism. Then `yggdrasilctl getPeers` on each side — reachable only with privilege, which `0ad137` records was denied — to see whether any session exists at all.

**Flow inference (this subflow's inference, marked as such).** Causes A, B and C are not competing; they compose. C is the standing condition, A removed the USB path on 2026-09-21 when the share was created with IPv6 off, and B removed the Wi-Fi path when Ouranos left Prometheus's AP. The overlay survived until 2026-09-21 16:16 only because the Wi-Fi adjacency was still up. The living's sentence is, on this reading, correct in its substance but one layer off in its mechanism: the reconfiguration is what broke it, but the block is the absence of IPv6 on Ouranos's downlink plus the absence of any configured peer — **not** a Yggdrasil firewall rule on Prometheus, whose nftables input chain accepts link-local 9001/10001 above the `eno1` drop.

---

## 5. Is there a typed network definition that would make this a declared object?

Yes — three layers of it, all designed, one partly built, none landed.

**The typed capability.** From `/home/li/primary/flows/753e69/reports/horizon-usb-gateway-contract.md` (2026-09-21), labelled "Candidate payload — proposal, not accepted schema":

```rust
NodeService::UsbIpv4Gateway {
    downstream: Interface,
    downstream_mac: MacAddress,
    gateway: Ipv4Cidr,
    uplink: Interface,
}
```

The Ethos source in the horizon-rs worktree (unlanded) declares it as `UsbIpv4Gateway.{ Interface MacAddress Ipv4Cidr Interface }` added to the `NodeCapability` list. Main horizon-rs has zero occurrences of it. The Goldragon assignment, also unlanded, reads `UsbIpv4Gateway.{enp0s20f0u1c2 00:0e:c6:33:4f:97 10.44.0.1/24 enp0s31f6}` on Ouranos only.

`flows/753e69/reports/transitive-network-topology-security.md` (2026-09-22) states the recursion: "The accepted `UsbIpv4Gateway` service already represents one node's gateway edge with `downstream`, `downstream_mac`, `gateway`, and `uplink`. Reusing that shape per node makes the chain recursive without making it hostname-specific."

**The producer chain**, from `horizon-usb-gateway-contract.md`: Goldragon `proposal.datomic` → Horizon `NodeProposal.services: Vec<NodeService>` → `NodeProposal::project` → Lojix serializes `horizon.json` and exposes it as `builtins.fromJSON` in a generated flake input → CriomOS `node-services.nix` accepts tagged capability records. The report is emphatic: "the CriomOS consumer must never select `ouranos` by host name." `CriomOS-test-cluster/checks/source-constraints.nix` enforces this — the build fails if any CriomOS module text contains `ouranos`, `prometheus`, `zeus`, or a `node.name ==` predicate.

**The hierarchy proper — Network Nexus.** `/home/li/primary/flows/4b0f60/reports/network-nexus-design.md` (2026-09-22, Mind Astra `4b0f60`):

> "Network Nexus keeps typed desired topology and capabilities separate from observed link, lease, authentication, route, DNS and connectivity evidence."

> "The desired shape is a cascaded routed gateway chain: Ouranos integrated NIC is the uplink and its USB NIC the downlink to Prometheus; Prometheus integrated NIC is the uplink and its USB NIC the downlink to Zeus; Zeus uses its integrated NIC as uplink. Each adjacency is a point-to-point transit link. Stable hardware facts and typed node capabilities select the role, with MAC and driver-class verification; ambiguous NIC selection is rejected. Default-route observation never establishes direction."

Its shape is stated concretely in `/home/li/primary/flows/753e69/reports/network-mode-nexus-poc.md` (2026-09-22):

> "- Network Nexus holds desired node mode, stable subnet reservations, a monotonic revision, and an actor/reason audit trail.
> - A mode change is an optimistic compare-and-swap transition. Stale writers are refused.
> - The planner validates one edge gateway, parent reachability, acyclic topology, integrated uplinks, USB downlinks, distinct interfaces, and nonoverlapping allocations.
> - One root pool supplies stable per-link and optional-AP subnets. Disabling a mode deactivates a reservation without recycling it, so re-enabling does not renumber the segment.
> - The plan assigns one egress NAT owner at the edge, per-link DHCP/DNS at the parent, and explicit upstream routes for downstream prefixes.
> - Optional AP is an explicit administrator-selected mode."

A proof of concept was built and independently retested with seven passing tests; its CLI allocated transit segments and "assigned egress NAT solely to Ouranos." But: "The POC emits desired plans only. It does not change a live interface, route, DHCP server, DNS server, firewall, access point, Nexus service, or CriomOS generation." The reports sweep searched `/home/li/wt` and could not find the POC's Rust source — only copies of these two markdown reports.

So the answer to the living's own question — "Do you need to create a network hierarchy kind of thing or with features?" — is that the hierarchy has already been designed twice and implemented once as a planner, and the thing that has never happened is landing it.

---

## Two things worth flagging beyond the question

**A circular dependency blocks the durable fix.** `/home/li/primary/flows/753e69/reports/usb-gateway-materialization-2026-09-21.md`: "The Signal `test-datom-contract` remote-only build reached its derivation but Prometheus rejected the SSH builder connection before compilation. The Lojix remote-only… build also reached its dependency derivations, then failed… because the same Prometheus SSH builder connection could not start." Landing the typed capability requires remote Nix builds on Prometheus; reaching Prometheus's builder requires the network. `flows/753e69/reports/usb-gateway-signal-dependency.md` adds a second blocker: a Horizon `0.5.1` / `0.12.0` version split across the Signal producers that produced "an actual failed compile."

**The living's hypothesis deserves a direct answer.** "Maybe Yggdrasil is firewalled on that USB Ethernet device" — on Prometheus's side it is not: `router/default.nix` accepts `fe80::/64` UDP 9001 and TCP 10001 before the `eno1` drop. On Ouranos's side the ports are open globally. What is blocked is one layer lower: there is no IPv6 on that link at all, so there is nothing for a firewall to pass. This should be put to the living, since it is close to but not identical with what they said.

**Reports and source not fully covered.** `flows/6fb948/reports/*network*` was named in the brief but does not exist; that directory holds no network evidence (only a citation in `mind-high-readiness-20260922.md`). The Network Mode Nexus POC implementation source could not be located on disk. Privileged runtime reads — live `nft list ruleset` counters on Prometheus, `yggdrasilctl getPeers` on either host — were unavailable to the Field and are the gap between this source-level account and a proven one. Per the testing skill's grades: everything above is **source-published** plus the Field's dated runtime observations; nothing here is **end-to-end-proven** for the current moment.

---

## Sources

### Primary (paths relative to the Primary repository root)

Psyche:

- `Vision/deployment.md`
- `Vision/horizon.md`
- `Vision/nexus.md`
- `Vision/sources/horizon.md`
- `vision-raw/setupIndependentInterfaces.md`
- `flows/836818/vision/network.md`
- `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`
- `flows/024bc7/vision/network.md`
- `flows/bcd02a/vision/network.md`
- `flows/01a030b7/vision/zeusUpdate.md`
- `flows/b80e55/vision/unifiedWifiRoamingAndCertAuth.md`
- `flows/b81560/vision/operational-openCodeOnUranusNotZeus.md`
- `flows/b81560/vision/archive-operational-horizonNexusAndNodeResources.md`
- `flows/f38926/vision/archive-horizon.md`
- `flows/0062e8/vision/horizon.md`
- `field/0ad137/vision/prometheusConnection.md`
- `field/0ad137/vision/durableNetworkRefresh.md`

Field and design reports:

- `field/0ad137/reports/prometheus-route-20260923.md`
- `flows/6db4fe/reports/prometheus-builder-recovery-2026-09-22.md`
- `flows/6db4fe/reports/prometheus-builder-recovery.md`
- `flows/6db4fe/reports/network-chain-attempts.md`
- `flows/6db4fe/reports/network-durable-source.md`
- `flows/6db4fe/reports/prometheus-connectivity.md`
- `flows/6db4fe/reports/prometheus-wifi-brief-2026-09-21.md`
- `flows/6db4fe/reports/prometheus-uplink-reliability-2026-09-22.md`
- `flows/6db4fe/reports/configured-builder-transport-2026-09-21.md`
- `flows/753e69/reports/horizon-usb-gateway-contract.md`
- `flows/753e69/reports/ouranos-share-durable-design.md`
- `flows/753e69/reports/network-path-plan-2026-09-21.md`
- `flows/753e69/reports/transitive-network-topology-security.md`
- `flows/753e69/reports/network-mode-nexus-poc.md`
- `flows/753e69/reports/usb-gateway-integration-ownership.md`
- `flows/753e69/reports/usb-gateway-materialization-2026-09-21.md`
- `flows/753e69/reports/usb-gateway-signal-dependency.md`
- `flows/4b0f60/reports/network-nexus-design.md`
- `flows/4b0f60/reports/network-nexus-refresh-handoff.md`
- `flows/4b0f60/reports/mega-network-diagnosis-mission.md`
- `flows/6fb948/reports/` — named in the brief; contains no network report
- `flows/6fb948/reports/remote-cleanup-gates-20260922.md`
- `flows/6fb948/summary.md`
- `flows/0384e0/witnesses/zeus-preflight.md`

Skill:

- `testing-transitive-network-topology`, loaded through the Skill tool
- `psyche`, loaded through the Skill tool

### CriomOS (paths relative to the CriomOS repository root)

- `modules/nixos/router/default.nix`
- `modules/nixos/router/yggdrasil.nix`
- `modules/nixos/router/wan-lease-recovery.sh`
- `modules/nixos/network/default.nix`
- `modules/nixos/network/networkd.nix`
- `modules/nixos/network/yggdrasil.nix`
- `modules/nixos/network/dnsmasq.nix`
- `modules/nixos/network/resolver.nix`
- `modules/nixos/normalize.nix`
- `modules/nixos/nix/cache.nix`
- `modules/nixos/users.nix`
- `modules/nixos/testing/opencode.nix`
- `checks/router-wan-recovery/default.nix`
- commits `114fcbd`, `6e1ca7b`, `d8c765d`, `c14074a`, `3f5b892`, `c250d9a`, `15f1a52`, `0f54288`, `4d6bb24`

Unlanded CriomOS worktree `usb-share-6db4fe`:

- `modules/nixos/network/usb-ipv4-gateway.nix`
- `modules/nixos/network/default.nix`
- `checks/usb-ipv4-gateway/default.nix`
- revision `9842f51`

### Other repositories

- CriomOS-lib: `lib/default.nix`
- CriomOS-test-cluster: `checks/source-constraints.nix`
- criomos-horizon-config: `horizon.dotos`
- goldragon: `cluster-definition.datom`; worktree `goldragon-main-canonical/proposal.datom`; unlanded worktree `post-terminus-horizon-data/proposal.datomic`, revision `a911515`
- horizon-rs: `lib/src/projection/viewpoint.rs`, `lib/src/projection/views.rs`, `lib/src/model.rs`, `lib/src/generated/horizon.rs`, `lib/ethos/horizon.ethos`; unlanded worktree `usb-gateway-main-merge-753e69`, revisions `944ad38`, `37416e1`, `92d40e3`
