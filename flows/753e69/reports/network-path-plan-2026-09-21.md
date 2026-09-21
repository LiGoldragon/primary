# Network path plan — 2026-09-21

## Scope and result

This is a carried, read-only handoff for the Terra worker and the owners of
Prometheus and Zeus. It distinguishes current local Ouranos observations made
at 2026-09-21T12:19:09-06:00 from point-in-time reports and source configuration.
No peer probe, credential/key read, network change, restart, build, reboot, or
garbage collection occurred in this evidence pass.

The intended path is stated by the living as: Ouranos receives Internet on its
built-in Ethernet; its USB Ethernet serves Prometheus; Prometheus's separate
USB Ethernet serves Zeus. The Zeus USB leg was explicitly described as not
ready. The intended topology is therefore not a witnessed working chain.

## Current witness on Ouranos

- Built-in Ethernet `enp0s31f6` was UP with `192.168.1.5/24`; it held the only
  IPv4 default route, `via 192.168.1.1` at metric 100. This is the current
  upstream Internet candidate.
- USB Ethernet `enp0s20f0u1c2` was UP at `10.44.0.1/24` under the active
  NetworkManager profile `prometheus-share-temporary` (UUID
  `92eb01d2-2087-44c9-a6ff-b2420df89d33`), configured as IPv4 shared and
  never-default. It installed the direct `10.44.0.0/24` route without changing
  the preferred built-in default. Wi-Fi was also up at `10.18.0.102/24`, with
  a secondary default through `10.18.0.1` at metric 600.
- USB counters were 19,368 bytes / 118 packets received and 196,012 bytes /
  1,339 packets transmitted, with zero receive/transmit errors. Carrier and
  counters do not identify the far endpoint.
- `/var/lib/NetworkManager/dnsmasq-enp0s20f0u1c2.leases` was zero bytes;
  per-interface forwarding was `1` on `enp0s31f6` and `enp0s20f0u1c2`
  (`all` and `default` remained `0`). DHCP was listening on UDP/67 and DNS on
  `10.44.0.1:53`. The zero lease means no DHCP peer is witnessed.
- `wlp0s20f3` was up. `nft` was unavailable in this user
  environment, so the actual local firewall/NAT rules are unknown.

The earlier snapshot at 2026-09-21T12:14:46-06:00 found the temporary share
inactive, with the USB IPv4-less and forwarding at `0`; it is superseded for
live-state purposes by the 12:19:09 observation above.

## Historical and source claims

- A 2026-09-21 report records the same temporary, in-memory Ouranos
  NetworkManager share on `enp0s20f0u1c2`: `10.44.0.1/24`, DHCP/DNS,
  forwarding enabled per interface, with the built-in route retained. Its peer
  had zero RX and no lease. The present activation above is independently
  witnessed but still has zero lease and does not identify Prometheus.
- Prometheus's reported 2026-09-21 router state was built-in WAN `eno1` at
  `192.168.1.16/24`, default via `192.168.1.1`; `br-lan` was `10.18.0.1/24`.
  A reported USB adapter `enp199s0f0u2c2` had no carrier and was a `br-lan`
  member. This is point-in-time peer evidence, not a present remote read.
- Current CriomOS source makes Prometheus a router with a single declared WAN.
  The `30-usb-eth` rule matches USB Ethernet driver families and bridges every
  matching interface into `br-lan`. The firewall permits `br-lan` to WAN and
  masquerades WAN egress. It has no declared, isolated USB downstream subnet
  for Zeus. The bridge is the configured USB-downstream shape for the AP and
  wired clients. The earlier L2/DHCP merge observation applies only to the
  contrary topology of attaching an upstream to a Prometheus USB interface;
  it is not a reason to remove the intended downstream bridge.
- The generic non-router center sharing implementation is `10.47.0.1/24` with
  DHCP and IPv4 masquerade, but its condition is `center && !router`. Reports
  state it does not select Ouranos, Prometheus, or Zeus. It is a source shape,
  not a current service witness.

## Bypass candidates — unverified

| Candidate | Evidence | Grade |
| --- | --- | --- |
| House LAN direct to Prometheus `192.168.1.16` through `enp0s31f6` | Historic Prometheus address is on Ouranos's present L2 subnet. | Unverified; address may be stale. |
| Yggdrasil direct SSH | Local `yggTun` route exists; recent reports recorded timeouts to Prometheus and Zeus. | Unverified / previously nonresponsive. |
| WireGuard | Historic report: `wg.prometheus` resolved but local routing was unavailable; Zeus had no WG DNS record. | Unverified / locally incomplete. |
| Tailscale | Historic report recorded `NoState`. | Unverified. |
| Foreign-router Wi-Fi / mesh | Design source describes this path; current Ouranos Wi-Fi is connected. | Unverified as an administrative route. |
| Prometheus Ygg SSH | Strict host-key SSH to the configured Prometheus Ygg alias succeeded in a separate named read-only check. | **Verified administrative bypass only**; it does not prove Internet forwarding or USB peer attachment. |

## Bounded next plan

1. The Prometheus owner, locally or through an already established
   host-key-safe access route, should identify the cable endpoint and verify
   the intended NIC, carrier, DHCP lease/default route, DNS, and forwarding/NAT
   counters. Preserve the current Prometheus AP/USB downstream `br-lan` bridge.
   The candidate upstream for the Ouranos USB cable is Prometheus's built-in
   WAN `eno1`; this is an active Field Astra decision/peer claim, not an
   end-to-end cable witness.
2. The Zeus owner should locally identify its USB NIC and check carrier, DHCP
   lease/address, default route, DNS, and an outbound Internet request through
   Prometheus. It must report the precise interface and address only after
   witnessing them.
3. Once the physical peer is proven, Terra may own the Ouranos-only side:
   preserve the built-in default route, select an existing NetworkManager
   checkpoint/rollback path, then apply and witness a share only if the peer
   interface and target have been established. Prove nonzero Ouranos USB RX,
   a lease, peer DNS, peer default route, and egress before treating the
   segment as usable.
4. Perform the configured Prometheus builder handshake only after transport
   and SSH identity are verified. No local fallback build is authorized by
   this plan.

## New peer-state evidence

Separate named read-only checks established the following:

- Strict host-key SSH to the configured Prometheus Ygg alias succeeded. A
  direct TCP attempt to historic `192.168.1.16` had no route. Prometheus sent a
  Ygg ICMP request to the named Zeus address successfully. These establish an
  administrative Ygg path to Prometheus and ICMP reachability from Prometheus
  to Zeus; neither proves the USB chain nor Internet forwarding.
- Prometheus remote inspection at 2026-09-21T12:18:46.650–12:18:47.015 CDT
  found USB NIC `enp199s0f0u1` UP/LOWER_UP, an ASIX device on USB path
  `/sys/devices/.../usb4/4-1/4-1:1.0`, a `br-lan` member with forwarding cost
  5. `wlp195s0` was the other reported bridge member, cost 100; the FDB had
  learned unicast entries on both. No IPv4 default route was printed. IPv4 and
  IPv6 forwarding were both `1`. NAT could not be inspected without root:
  `nft` was denied and `iptables` absent.
- A strict verified-Ygg SSH inspection at
  2026-09-21T12:22:43.026–12:22:43.400 CDT found Prometheus built-in WAN
  `eno1` carrier UP/LOWER_UP at 1 Gbps full duplex. It had only IPv6 link-local
  state: no IPv4 address/default route/neighbours, and only a `fe80::/64`
  route. `networkctl` reported `/etc/systemd/network/10-wan.network` as
  degraded/configuring and offline; networkd was running, and no DHCP lease
  file was present. Counters were 41,695 B / 354 RX packets and 20,822 B / 111
  TX packets, without errors/drops. `eno1` is not a `br-lan` member, so there
  is no FDB comparison to Ouranos USB MAC `00:0e:c6:33:4f:97`; carrier/counters
  alone do not pair the cable.
- At 12:24 local time, the active Ouranos shared profile was still connected.
  Its dnsmasq pool was `10.44.0.10`–`10.44.0.254`, started at 12:16:47; its
  exact lease file was empty and its relevant request logs contained no DHCP
  request. Neighbour resolution for `10.44.0.2` failed. On Prometheus, `eno1`
  remained configured with `DHCP=ipv4`, but was configuring/degraded/offline
  with no IPv4 address, DHCP lease, or neighbour; logs recorded only carrier
  acquisition and IPv6 link-local configuration. These facts show no completed
  DHCP exchange or paired endpoint, not that no traffic occurred.
- Each host attempted one ten-second passive ARP/DHCP capture, but both lacked
  `CAP_NET_RAW`. No capture was obtained, so this report makes no
  traffic-absence claim.
- At 2026-09-21T12:19:04.485–12:19:04.712 CDT, one strict BatchMode five-second
  SSH `ProxyJump` attempt to Zeus reached Prometheus, matched its known ED25519
  host key, and completed public-key authentication. The proxied stream then
  closed during key exchange (`kex_exchange_identification: Connection closed
  by remote host`) before Zeus host-key/authentication or commands. Zeus SSH
  through Prometheus is therefore **not established**.
- The latest bounded endpoint comparison found Ouranos USB MAC
  `00:0e:c6:33:4f:97` and Prometheus USB MAC `00:0e:c6:ad:21:5d`. Prometheus's
  FDB on that USB port did not contain the Ouranos MAC, and its neighbour table
  was empty. This does not establish that these USB interfaces are cabled to
  each other. Only one USB NIC was observed on Prometheus, so no second USB NIC
  is witnessed for a Prometheus-to-Zeus segment.
- A direct `ssh zeus` from Ouranos failed at DNS resolution before host-key or
  authentication. This is a name-resolution result, not an observation of Zeus
  SSH service state.

**USB-chain grade: unverified.** The active Ouranos shared segment, Prometheus
USB bridge port, and Ygg administrative route are independently evidenced, but
no end-to-end physical peer or DHCP lease has been witnessed. The latest Field
Astra report directs preservation of the Prometheus AP/USB downstream bridge
and investigation of its built-in `eno1` as the Ouranos USB upstream candidate.
That decision does not establish cable pairing; the Prometheus-to-Zeus separate
USB leg also remains unwitnessed.

## Coordinated DHCP test gate

The next discriminating test needs Terra to hold capture capability and make
one reversible Prometheus `eno1` DHCP reconfiguration. Do not restart
`systemd-networkd` by default. During that single bounded attempt, witness a
matching DHCP DISCOVER/OFFER/ACK on both sides, then a Prometheus IPv4 lease,
address and default route. If those observations do not line up, stop and
retain the evidence; no durable configuration or cable conclusion follows.

## SSH topology options

- **Direct:** use a known Prometheus hostname/address only with a verified
  expected host key and the existing authorized SSH identity. A successful
  transport connection alone is insufficient.
- **Jump host:** if Zeus is reachable only through Prometheus, use SSH
  `ProxyJump` or a local `-W` stream through verified Prometheus host identity,
  then independently verify Zeus's host key. The one observed jump reached
  Prometheus but closed before that Zeus verification; do not treat it as a
  jump route.
- **Local forwarding:** after both host identities are verified, forward a
  specific local TCP port through Prometheus to Zeus for one bounded service
  check. Bind locally, time-limit it, and close it after the check. This does
  not establish Internet forwarding or the USB chain by itself.

No key material, fingerprints, or credential contents belong in this report.

## Ownership boundary

Terra alone may change Ouranos NetworkManager or firewall state, and only after
the peer-side checks identify the cable, endpoint, interface, and intended
routing shape. Prometheus and Zeus owners alone validate their respective
local physical/interface/route state. This handoff grants neither peer mutation
nor a durable CriomOS change.

## Sources

- `flows/024bc7/vision/network.md` — living's 2026-09-13 intended USB chain.
- `flows/6db4fe/reports/network-chain-attempts.md` (mtime 2026-09-21 12:13:50
  -0600), `prometheus-connectivity.md` (08:14:36 -0600), and
  `prometheus-builder-recovery.md` (10:39:18 -0600) — recent Ouranos evidence.
- `flows/e1953c/reports/prometheusNetwork.md` (mtime 2026-09-14 17:15:09
  -0600; report's reported peer observations dated 2026-09-21) — Prometheus
  router and USB analysis.
- `flows/79715b/reports/reachability-2026-09-17.md` — previous bypass results.
- Named peer checks reported 2026-09-21T12:18:46.650–12:19:04.712 CDT — strict
  Prometheus SSH, Prometheus bridge/forwarding state, Prometheus-to-Zeus ICMP,
  and the failed pre-Zeus-authentication ProxyJump.
- Latest named endpoint/DNS checks — USB MAC/FDB/neighbour comparison, USB NIC
  count on Prometheus, and direct Zeus name-resolution failure from Ouranos.
- Named `eno1` peer check at 2026-09-21T12:22:43.026–12:22:43.400 CDT —
  verified-Ygg inspection of Prometheus WAN carrier, address/route/lease state,
  and counters. Field Astra's reported bridge-preservation/`eno1` decision is
  explicitly a peer claim, not a live cable-pairing witness.
- Bounded DHCP-path probe at 12:24 local — current Ouranos share/dnsmasq/lease
  state, Prometheus `eno1` DHCP/lease state, failed neighbour resolution, and
  unavailable passive capture capability on both hosts.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:161-175,373-399`
  and `modules/nixos/network/networkd.nix:15,30-48` — current configuration.
