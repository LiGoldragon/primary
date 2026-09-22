# TESTING skill proposal: transitive network topology

Status: **TESTING proposal**. The living requested a reusable testing skill.
Psyche must present the authored behavior and the living must accept its exact
skill form before projection into generated skill trees. This file changes no
generated skill and deploys no network configuration.

## Proposed trigger

Load when a Field test must establish a multi-node Internet-sharing chain in
which each node's integrated NIC is its uplink and its USB NIC is its downlink,
or when stable Ethernet / Optional AP behavior must be tested.

## Required test record

For every node and link, record separately:

1. node identity and exact observation time;
2. integrated and USB interface identities, MACs, drivers, and ownership;
3. declared role: uplink/WAN-facing or downlink/LAN-facing;
4. physical carrier and the identity evidence for the peer at the far end;
5. upstream address, gateway, default route, and DNS source;
6. downstream subnet, DHCP/DNS owner, and lease observed at the intended peer;
7. forwarding and firewall owner, with one declared egress NAT owner;
8. hop-by-hop ARP/neighbor, route, DNS, and Internet proof;
9. management-path preservation and rollback state;
10. evidence grade: source, installed, running, or end-to-end proven.

Carrier, a configured address, or a listening DHCP socket never proves the far
peer or Internet. A historical lease never proves current reachability.

## Invariants

- Integrated NIC is uplink; USB NIC is downlink, unless an explicit accepted
  exception names both interfaces and its lifetime.
- Uplink and downlink are distinct interfaces with stable identity evidence.
- Each downstream link has one non-overlapping subnet and one DHCP/DNS owner.
- No upstream/downstream L2 bridge exists unless the test explicitly targets
  a bridge design.
- NetworkManager and networkd do not own the same link.
- Exactly one durable firewall owner exists. Prefer exactly one egress NAT
  owner at Ouranos; any temporary nested NAT is named and bounded.
- Missing capability means no gateway or AP activation.
- Stable Ethernet / Optional AP mode requires an authorized network-admin
  action, transactional health gate, audit record, and rollback.
- WPA Enterprise acceptance requires unique EAP-TLS client identity, server
  certificate validation, revocation behavior, and isolation tests. A shared
  password is migration state, never certificate-auth proof.

## Mandatory cases

1. Ouranos integrated uplink -> Ouranos USB downlink -> Prometheus integrated
   uplink -> Prometheus USB downlink -> Zeus integrated uplink.
2. Cold boot, USB hotplug, cable unplug/replug, interface enumeration change,
   and DHCP renewal converge to the same roles.
3. Missing peer, carrier-only, stale lease, DHCP request without offer, and
   ARP without reply remain failed/unknown rather than passing.
4. Duplicate DHCP, overlapping subnet, duplicate NAT, wrong local MAC,
   ambiguous USB NIC, and network-manager ownership conflict fail closed.
5. Each hop proves local gateway reachability before DNS and Internet; the
   leaf proves the complete return path.
6. Unrelated nodes do not activate from another node's identical payload.
7. Stable Ethernet mode preserves management; failed health rolls back.
8. Optional AP remains absent unless explicitly enabled, and disabling it
   removes AP-specific listeners and forwarding without breaking wired transit.
9. EAP-TLS accepts a valid device certificate and rejects expired, revoked,
   wrong-EKU, wrong-CA, and untrusted-server cases.
10. IPv6 cannot bypass the IPv4 forwarding and isolation policy.

## Result language

Report **source-published**, **installed-running**, and **end-to-end-proven**
as different grades. Name the exact revision running versus the latest source.
Use `UNKNOWN` where a peer or runtime receipt is absent. Never infer the whole
chain from one successful hop.
