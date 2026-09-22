# Network Nexus design: cascaded routed topology

**Owner:** Mind Astra `4b0f60`, retained High-power network-design owner.
**Status:** design requirements grounded in the exact Field report
`transitive-network-topology-753e69@origin`
`8433b21930c650f91ab2d8f1c38b311ab862c30c`. This is neither an accepted
implementation, a source mutation, nor a runtime/deployment receipt.

## Desired topology and observed state

Network Nexus keeps typed desired topology and capabilities separate from
observed link, lease, authentication, route, DNS and connectivity evidence.
The current availability conclusion is **Prometheus Internet unproved**. The
2026-09-21 temporary witness of `10.44.0.148`, DNS and HTTP 200 does not prove
current service: a later independent observation found no lease, ARP or ICMP,
which supersedes that success for current availability.

The desired shape is a cascaded routed gateway chain: Ouranos integrated NIC
is the uplink and its USB NIC the downlink to Prometheus; Prometheus integrated
NIC is the uplink and its USB NIC the downlink to Zeus; Zeus uses its integrated
NIC as uplink. Each adjacency is a point-to-point transit link. Stable hardware
facts and typed node capabilities select the role, with MAC and driver-class
verification; ambiguous NIC selection is rejected. Default-route observation
never establishes direction.

Each downstream has a distinct subnet, DHCP/DNS policy and explicit forwarding
rule; links are not accidentally bridged. The preferred durable arrangement is
routing at each hop and one egress NAT owner at Internet-edge Ouranos.
Prometheus routes its downstream prefixes. NetworkManager shared mode on every
hop is nested NAT; any temporary exception requires an explicit policy decision
and cannot be inferred from this design.

## Mode, security and reconciliation

The canonical operating mode is **Wired Uplink Gateway Mode**. Optional AP is
an explicitly authorized feature, never automatic cable detection. A privileged
mode transition preflights its wired uplink, preserves a management path,
applies address/route/firewall/AP state, health-checks, commits or rolls back,
and records actor, requested and previous mode, result and rollback evidence.
This does not prescribe the currently open administrator capability or claim a
working rollback implementation.

The Wi-Fi target is WPA3-Enterprise, 802.1X/EAP-TLS, with unique client keys,
an offline root, restricted issuer, a RADIUS server certificate, and client
validation of expected CA and server identity. Secrets, private keys and
enrolment material never enter command arguments or logs. WPA3-SAE remains
transitional migration state when present; it is not the target security claim.

The controller enforces default-deny forwarding; established/related return
traffic; anti-spoof checks; DHCP/DNS binding only to declared downstream links;
separate management from AP/client traffic; and a deliberate IPv6 policy
(routed prefixes with equivalent firewall policy, or disabled transit IPv6).
It refuses duplicate DHCP or NAT owners, prefix overlap, link loops, ambiguous
NICs, and simultaneous NetworkManager/networkd ownership. These are desired
policy requirements, not observed enforcement.

One existing Network Nexus/controller reconciles a typed privileged request
through a generation-bound idempotent plan, with stale/refusal/evidence and
rollback records. Its ordinary interface exposes an initial typed snapshot and
real events with per-observation quality/freshness. It does not turn source
materialization into runtime proof or create another controller. Optional
Ouranos API access is available only when wired Internet is available; it is
not activation authority.

## Acceptance boundaries

Implementation must prove source, build, materialization, and runtime stages
separately. Transitive tests fail closed for ambiguous NIC selection, duplicate
owner, overlapping prefixes, link loop, wrong firewall or DHCP/DNS exposure,
and failure to preserve management. They also prove each-hop forwarding and
edge-only NAT. Open design items include the IPv6 choice, any interim
nested-NAT policy, the administrator capability, and concrete rollback proof.

The established source path remains Goldragon desired `NodeService` assignment
through Horizon projection, Lojix materialization and CriomOS's selected
network owner. `UsbIpv4Gateway` is a proposal/configuration anchor, not an
installed capability. No build, secret/PKI generation, source component edit,
or network mutation is authorized by this document.

## Sources

- `flows/753e69/reports/transitive-network-topology-security.md` at Primary
  bookmark `transitive-network-topology-753e69@origin`
  `8433b21930c650f91ab2d8f1c38b311ab862c30c`: exact source report, including
  its proposal/open-state limits and external standards citations.
- `flows/4b0f60/reports/network-nexus-refresh-handoff.md`: current owner,
  runtime evidence and preserved-controller boundary.
- `flows/753e69/reports/horizon-usb-gateway-contract.md` and
  `usb-gateway-integration-ownership.md`: typed source-chain constraints.
