# Network path plan — 2026-09-21

## Scope and result

This is a carried, read-only handoff for the Terra worker and the owners of
Prometheus and Zeus. It distinguishes a local Ouranos observation made at
2026-09-21T12:14:46-06:00 from point-in-time reports and source configuration.
No peer probe, credential/key read, network change, restart, build, reboot, or
garbage collection occurred in this evidence pass.

The intended path is stated by the living as: Ouranos receives Internet on its
built-in Ethernet; its USB Ethernet serves Prometheus; Prometheus's separate
USB Ethernet serves Zeus. The Zeus USB leg was explicitly described as not
ready. The intended topology is therefore not a witnessed working chain.

## Witnessed on Ouranos

- Built-in Ethernet `enp0s31f6` was UP with `192.168.1.5/24`; it held the only
  IPv4 default route, `via 192.168.1.1` at metric 100. This is the current
  upstream Internet candidate.
- USB Ethernet `enp0s20f0u1c2` was carrier UP but had no IPv4 address. NetworkManager
  showed `Wired connection 2` still obtaining DHCP. The earlier temporary
  shared profile was not active.
- USB counters were 15,128 bytes / 94 packets received and 165,597 bytes /
  1,102 packets transmitted, with zero receive/transmit errors. Carrier and
  counters do not identify the far endpoint.
- `/var/lib/NetworkManager/dnsmasq-enp0s20f0u1c2.leases` was zero bytes;
  `conf/{all,default,enp0s31f6,enp0s20f0u1c2}/forwarding` were all `0`.
  No DHCP/DNS listener for the former `10.44.0.1/24` share was present.
- `wlp0s20f3` was down with no carrier. `nft` was unavailable in this user
  environment, so the actual local firewall/NAT rules are unknown.

## Historical and source claims

- A 2026-09-21 report records a temporary, in-memory Ouranos NetworkManager
  share on `enp0s20f0u1c2`: `10.44.0.1/24`, DHCP/DNS, forwarding enabled per
  interface, with the built-in route retained. Its peer had zero RX and no
  lease. That profile is absent from the current observation above.
- Prometheus's reported 2026-09-21 router state was built-in WAN `eno1` at
  `192.168.1.16/24`, default via `192.168.1.1`; `br-lan` was `10.18.0.1/24`.
  A reported USB adapter `enp199s0f0u2c2` had no carrier and was a `br-lan`
  member. This is point-in-time peer evidence, not a present remote read.
- Current CriomOS source makes Prometheus a router with a single declared WAN.
  The `30-usb-eth` rule matches USB Ethernet driver families and bridges every
  matching interface into `br-lan`. The firewall permits `br-lan` to WAN and
  masquerades WAN egress. It has no declared, isolated USB downstream subnet
  for Zeus. Plugging an upstream into an automatically bridged USB port can
  merge L2 domains and DHCP servers.
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
| Foreign-router Wi-Fi / mesh | Design source describes this path; current Ouranos Wi-Fi is down. | Unavailable in current observation. |

## Bounded next plan

1. The Prometheus owner, locally or through an already established
   host-key-safe access route, should identify the cable endpoint and verify
   the intended NIC, carrier, bridge membership, DHCP lease/default route,
   DNS, and forwarding/NAT counters. If its USB port is meant to serve Zeus,
   determine whether the current `br-lan` bridge is acceptable or whether an
   isolated routed/share subnet is required before changing source or runtime.
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

## SSH topology options

- **Direct:** use a known Prometheus hostname/address only with a verified
  expected host key and the existing authorized SSH identity. A successful
  transport connection alone is insufficient.
- **Jump host:** if Zeus is reachable only through Prometheus, use SSH
  `ProxyJump` or a local `-W` stream through verified Prometheus host identity,
  then independently verify Zeus's host key. Do not accept a key merely because
  the jump succeeded.
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
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:161-175,373-399`
  and `modules/nixos/network/networkd.nix:15,30-48` — current configuration.
