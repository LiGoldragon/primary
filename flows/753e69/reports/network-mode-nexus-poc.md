# Network Mode Nexus proof of concept

Field Medium Sol `753e69` implemented this source-only proof of concept from
Mind Astra `4b0f60`'s `flows/4b0f60/reports/network-nexus-design.md` and the
living's transitive-topology direction recorded in
`flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`.

The POC makes the proposed split concrete:

- Network Nexus holds desired node mode, stable subnet reservations, a
monotonic revision, and an actor/reason audit trail.
- A mode change is an optimistic compare-and-swap transition. Stale writers
  are refused.
- The planner validates one edge gateway, parent reachability, acyclic
  topology, integrated uplinks, USB downlinks, distinct interfaces, and
  nonoverlapping allocations.
- One root pool supplies stable per-link and optional-AP subnets. Disabling a
  mode deactivates a reservation without recycling it, so re-enabling does not
  renumber the segment.
- Every loaded ledger is revalidated against the root pool: indexes are unique,
  CIDRs and host fields must derive exactly from their index, keys and records
  must be well formed, and every active segment must have a reservation.
- The plan assigns one egress NAT owner at the edge, per-link DHCP/DNS at the
  parent, and explicit upstream routes for downstream prefixes.
- Optional AP is an explicit administrator-selected mode. The POC records the
  EAP-TLS target but creates no keys, credentials, radio state, or service.

The POC emits desired plans only. It does not change a live interface, route,
DHCP server, DNS server, firewall, access point, Nexus service, or CriomOS
generation. The existing Horizon `UsbIpv4Gateway` and CriomOS consumer remain
the integration boundary; no installed or running state is claimed here.

Focused tests cover the Ouranos to Prometheus to Zeus chain, edge-only NAT,
stable optional-AP reservation, stale revision refusal, duplicate edge,
cycles, ambiguous interfaces, audit fields, and the no-live-mutation grade.

## Independent evidence

Terra independently retested implementation revision `4cbd8a237203` with all
seven source tests passing. Its separate CLI chain witness allocated transit
segments `.0` and `.1`, assigned egress NAT solely to Ouranos, and allocated
the optional AP at `.2`; the AP reservation stayed stable while inactive and
after reactivation.

The independent negative cases refused corrupted state and a stale
compare-and-swap while preserving the state bytes. A one-node `strace` of the
CLI observed no network commands. This proves source-only planning behavior;
it does not prove a deployed Nexus, CriomOS reconciliation, or live network
reachability.
