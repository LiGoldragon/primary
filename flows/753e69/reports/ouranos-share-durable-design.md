# Ouranos USB share: durable design handoff

**Status:** carried design for Terra and Field Astra. This is not a deployment
instruction, a configuration evaluation, or evidence that a durable rule has
been installed. Terra must evaluate the selected NixOS firewall backend and
the Horizon schema before selecting an implementation.

## Established temporary path

Terra's recorded root-scoped runtime repair on 2026-09-21 admitted DHCP UDP
67 and DNS TCP/UDP 53 only on Ouranos USB interface `enp0s20f0u1c2`, and
added an IPv4 source NAT rule for `10.44.0.0/24` only when traffic left
`enp0s31f6`, the built-in Ethernet WAN.

After a bounded Prometheus `eno1` reconfiguration, Prometheus acquired
`10.44.0.148/24` with gateway `10.44.0.1`; its networkd client recorded the
lease, and it resolved `cache.nixos.org` and received HTTP/2 200. The DHCP
accept counter and the scoped masquerade counter both increased. This proves
the working temporary Ouranos-to-Prometheus Internet hop. It does not make the
runtime rules declarative or durable.

The earlier packet capture proved the physical pairing between Ouranos USB and
Prometheus built-in `eno1`: DHCP requests and an Ouranos USB ARP broadcast
were visible at both ends. The separate Prometheus-to-Zeus USB segment remains
unwitnessed and outside this change.

## Current authored configuration

The operating-system source is network-neutral. It holds no Ouranos-specific
host selection: host identity and role enter through Lojix-materialized
`horizon` input. Therefore a host-name conditional is not an acceptable
durable shape.

| Authored source | Relevant present contract |
| --- | --- |
| `CriomOS/modules/nixos/network/default.nix` | Imports the network modules, including `networkd.nix`; this is the integration point for a new capability-gated USB-share module. |
| `CriomOS/modules/nixos/network/networkd.nix` | Existing generic USB-share form: `10.47.0.1/24`, networkd DHCP server, `IPMasquerade = "ipv4"`, IPv4 forwarding. Its `center && !router` selector excludes Ouranos and conflicts with NetworkManager ownership of the USB link. Do not broaden it to select by node name. |
| `CriomOS/modules/nixos/normalize.nix` | Enables NetworkManager from `horizon.node.enableNetworkManager`; it is the applicable connection manager on Ouranos. |
| `goldragon/cluster-definition.datom` | The Ouranos node carries Edge/LowPower/NextGeneration and related capabilities, but no capability meaning “provides USB IPv4 Internet share.” |
| `CriomOS/modules/nixos/router/default.nix` | Router-only precedent for explicit LAN-to-WAN forwarding, established return traffic, and WAN-only masquerade. It does not select Ouranos. |

The active temporary NetworkManager profile is `prometheus-share-temporary` on
`enp0s20f0u1c2`, with `ipv4.method=shared`, `10.44.0.1/24`, IPv6 disabled and
`never-default=true`. The upstream default route remains on `enp0s31f6`.

## Proposed durable shape

Introduce a semantic Horizon capability such as `UsbInternetGateway`, assigned
only to Ouranos in the Goldragon definition. Project it into Horizon and gate a
new CriomOS network module on that capability. The exact schema type, generated
projection field, and configuration source are not yet evidenced; Terra must
locate and validate them before editing.

The proposed module has three deliberately separated responsibilities:

1. **NetworkManager owns the USB link, address, DHCP and DNS.** Declare the
   profile with `networking.networkmanager.ensureProfiles.profiles`, bound to
   `enp0s20f0u1c2`, with shared IPv4 address `10.44.0.1/24`, IPv6 disabled,
   never-default, and a reviewed autoconnect policy. This replaces the
   in-memory profile without changing the built-in Ethernet's route priority.

2. **NixOS firewall owns USB service admission.** Permit only UDP 67 and UDP/
   TCP 53 on `enp0s20f0u1c2`; do not use `trustedInterfaces`, which would
   expose every host service on the USB link. On the iptables backend, the
   interface-scoped `networking.firewall.interfaces.<if>.allowedUDPPorts` and
   `allowedTCPPorts` options are the narrow declarative contract. If source
   restriction to `10.44.0.0/24` is needed, use backend-appropriate narrowly
   scoped rules, not global allowed ports.

3. **NixOS NAT owns source NAT and forwarding.** The intended policy is source
   `10.44.0.0/24`, egress only `enp0s31f6`, plus USB-to-WAN forwarding and
   established return traffic. The standard NixOS NAT interface expresses the
   source subnet and external interface through `networking.nat.internalIPs`
   and `networking.nat.externalInterface`; with nftables it also supplies
   matching forward acceptance. Terra must determine whether the evaluated
   Ouranos deployment uses the iptables or nftables backend before choosing the
   final forward-rule expression.

One subsystem must be the durable NAT owner. NetworkManager shared mode often
has its own sharing/NAT behavior, while the live temporary configuration left
no usable NAT rule after NixOS firewall handling. The observed repair supports
NixOS as the NAT owner, but this remains a proposal until Terra evaluates a
declarative activation and proves that exactly one masquerade rule covers
`10.44.0.0/24 -> enp0s31f6`. If NetworkManager instead reliably installs and
retains its own NAT rule after the evaluated firewall lifecycle, do not add Nix
NAT; replace shared mode with explicit address plus scoped DHCP/DNS before
making NixOS the NAT owner.

## Disconfirming evidence and unknowns

- The generic `10.47.0.0/24` networkd implementation is unreachable for all
  current Goldragon nodes; it is a source precedent, not Ouranos configuration.
- The temporary runtime profile and iptables rules prove the first hop only.
  They do not prove durable NetworkManager lifecycle behavior or the Zeus leg.
- DNS resolution succeeded from Prometheus, but the temporary TCP/UDP 53 rule
  counters were zero. The result does not prove that Prometheus used Ouranos's
  DNS listener.
- The exact Horizon schema and generated projection field needed for the new
  capability have not been located in this evidence pass.
- The post-evaluation firewall backend is unknown. Live inspection used the
  iptables `nixos-fw` chain; NixOS NAT emits different rule forms for nftables.

## Deployment and rollback gates

1. **Capability gate:** Terra identifies the Horizon schema and generated
   projection contract, adds a semantic capability without node-name logic, and
   assigns it only where the role is intended.
2. **Evaluation gate:** evaluate the materialized Ouranos configuration and
   inspect the selected firewall/NAT backend and generated rules. This handoff
   authorizes no local build fallback.
3. **Exposure gate:** prove that USB ingress newly admits only DHCP UDP 67 and
   DNS UDP/TCP 53. Do not mark the USB interface trusted.
4. **Single-NAT gate:** prove one, and only one, source NAT rule for
   `10.44.0.0/24` exiting `enp0s31f6`; no broad subnet or all-interface
   masquerade.
5. **Functional gate:** reconfigure the already declared Prometheus `eno1`
   client, then witness its lease, default route, DNS query directed at
   `10.44.0.1`, and outbound egress. Confirm Ouranos retains its built-in
   Ethernet preferred default route.
6. **Rollback gate:** keep the exact temporary-rule deletion procedure until
   the declarative activation passes all gates. The declarative rollback is the
   previous system generation and removal/down-state of the ensured profile;
   it must leave Prometheus AP and `br-lan` untouched.

No reboot, garbage collection, app restart, NetworkManager restart, or local
build fallback belongs in this plan.

## Ownership

Terra alone may mutate Ouranos NetworkManager, firewall, NAT, Horizon-capability
wiring, or deploy state for this change. Prometheus and Zeus owners retain
their local interface and downstream-chain work. This carried report grants no
peer-side mutation authority.

## Sources

- `flows/6db4fe/reports/network-chain-attempts.md`, attempts 5–6: paired
  capture, temporary root rules, DHCP lease, route, and egress witness.
- `flows/753e69/reports/network-path-plan-2026-09-21.md`: carried topology,
  current state, and prior ownership boundaries.
- `flows/024bc7/vision/network.md`: living's intended USB chain.
- `CriomOS/modules/nixos/network/default.nix`,
  `CriomOS/modules/nixos/network/networkd.nix`,
  `CriomOS/modules/nixos/normalize.nix`, and
  `CriomOS/modules/nixos/router/default.nix`: current authored contracts.
- `goldragon/cluster-definition.datom`: current node capability assignment.
- NixOS source contracts:
  `nixos/modules/services/networking/networkmanager.nix`, `nat.nix`,
  `nat-nftables.nix`, `firewall.nix`, and `firewall-iptables.nix`.
