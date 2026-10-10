# Passive USB downlink observer design

Prepared for Mind Astra `6f51ad` and Psyche Fable `c64ee3` from Mind Sol flow `b666e7`. This is a design artifact only. It authorizes no source, host, build, deployment, probing, recovery, or network change.

## Decision boundary

Implement the first observer only for a non-Router node that declares `UsbDownlink`, such as current Ouranos. The observer reports independent evidence about the local USB edge: link presence and carrier, downstream-peer evidence, address/lease evidence, and, only through an optional recognizer, trusted cluster identity. It never collapses those dimensions into `HEALTHY` or `FAILURE`.

The observer does not expect one named downstream node. An unknown peer is ordinary. An IPv4 address, DHCP lease, MAC address, interface name, or physical plug position is evidence about a moment, never node identity. Router USB edges are an extension point pending the living's ruling; the first implementation must not silently treat Prometheus's shared `br-lan` as equivalent to non-Router `br-downlink`.

This follows the living's established direction:

- integrated Ethernet is upstream and USB Ethernet is downstream; the pattern remains movable and stateless across plug topology (`flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`);
- plugging USB Ethernet enables the downstream-provider feature (`flows/8904b1/vision/anatomy.md`);
- IPv4 is temporal and must not select identity (`flows/01a048a6/vision/deploymentSelection.md`);
- the Criome cluster and its trust value own trusted-node identity (`flows/c8d79f/vision/operational-criomeClusterIsTheTailnet.md`);
- cluster feature data is authored with the cluster; CriomOS stays generic (`flows/8904b1/vision/anatomy.md`).

## Ownership and data flow

The existing owner remains unchanged:

```text
goldragon cluster data
  UsbDownlink network declaration
          |
          v
Horizon projection
  local node capability + cluster-node/trust view
          |
          v
CriomOS non-Router UsbDownlink
  networkd -> br-downlink
  Kea     -> DHCP
  resolved -> DNS
  NixOS NAT/firewall
          |
          +------------------------------+
          | read-only runtime evidence   |
          v                              v
 USB downlink observer ------------ optional cluster recognizer
          |
          v
 local snapshot + transition events
```

`systemd-networkd`, Kea, resolved, NAT, and the firewall keep their current single ownership. The observer reads their public kernel/runtime evidence and never configures an interface, bridge, address, lease, route, firewall rule, or service. It stores no observations in Goldragon or Horizon. Authored intent flows down; runtime evidence does not flow back into authored cluster data.

The first collector watches:

- udev/rtnetlink link events for USB-Ethernet appearance, disappearance, bridge membership, and carrier;
- bridge FDB and neighbor events for fresh L2/L3 peer evidence;
- a bounded initial snapshot of those tables at service start, marked as a read-time snapshot rather than a peer event. The snapshot time is never substituted for the source entry's age: an entry may support `PeerPresent` only when the kernel/source exposes an age that is still current under that source's own contract, or when the observer witnesses the event after it starts. An entry with no trustworthy source age is unknown or stale;
- Kea's existing memfile lease view and journal stream read-only for address/lease evidence, each item retaining its source timestamp. A lease alone never proves current peer presence or identity.

“Passive” means the service may subscribe, read, timestamp, and reduce evidence already produced by the kernel and current service owners. It may not emit ARP, NDP, ICMP, DHCP, DNS, TCP, overlay, or application probes. It may not reset, renew, restart, reload, toggle, rebind, or recover anything.

## State and event contract

The exact surface can be Datom on a local read-only socket or the same typed value serialized as JSON for the first package. The semantic shape is:

```text
UsbDownlinkObservation.{
  SchemaVersion
  ProviderNode
  EdgeRef.{ BootId IfIndex InterfaceName BridgeName }
  LinkEvidence
  PeerEvidence
  Vector<PublicAddressEvidence>
  Recognition
  ObservedAt
}

LinkEvidence =
    LinkAbsent.{ Source ObservedAt }
  | CarrierDown.{ Source ObservedAt }
  | CarrierUp.{ Source ObservedAt }
  | CarrierUnknown.{ Source ObservedAt }

PeerEvidence =
    PeerPresent.{ Source EvidenceRef SourceObservedAt FreshnessBasis }
  | PeerEvidenceStale.{ Source EvidenceRef LastObservedAt }
  | PeerUnknown.{ Reason SourcesConsidered ObservedAt }

PublicAddressEvidence.{ Kind OpaqueEvidenceRef Freshness Source ObservedAt ExpiresAt }

RootRawAddressEvidence.{ Kind RawValue LinkAddress SourceObservedAt SourceExpiresAt }

Recognition =
    RecognizerDisabled.{ Reason }
  | UnknownPeer.{ EvidenceRefs ObservedAt }
  | KnownClusterNode.{ NodeId TrustValue ProofSource ObservedAt FreshUntil }
  | RecognitionStale.{ PriorNodeId ProofSource LastObservedAt }
```

`EdgeRef` correlates observations within one boot. `BootId`, interface name, ifindex, bridge name, and address values must never be interpreted as node identity. `FreshnessBasis` records either a witnessed post-start source event or a source-provided age/current-state contract; observer read time is never a freshness basis. Until Psyche rules an observation duration, start condition, source coverage, and freshness policy, no `PeerAbsent` state exists. No current evidence produces `PeerUnknown`, not an inference that a peer is absent.

The public observation and event stream contains `PublicAddressEvidence` only: its reference is opaque and reveals no address, MAC, or DUID. `RootRawAddressEvidence` is a separate root-only local diagnostic view. It is never embedded in the public observation, journald transition, or future ordinary Nexus surface.

Events carry the complete new dimension value plus a monotonic sequence number and wall-clock observation time:

```text
DownlinkEvent =
    LinkEvidenceChanged
  | PeerEvidenceChanged
  | PublicAddressEvidenceChanged
  | RecognitionChanged
```

There is deliberately no `HEALTHY`, `DHCP_FAILURE`, `ZEUS_MISSING`, or automatic recovery event. `DHCP_FAILURE` would require a witnessed request plus an authored response deadline; neither exists today. A stale neighbor, FDB entry, journal line, or lease cannot establish current presence, known identity, or health.

## Required examples

Carrier down:

```json
{
  "link": {"carrierDown":{"source":"rtnetlink","observedAt":"2026-09-29T15:24:22-06:00"}},
  "peer":{"unknown":{"reason":"carrier-down","sourcesConsidered":[],"observedAt":"2026-09-29T15:24:22-06:00"}},
  "addresses":[],
  "recognition":{"disabled":{"reason":"no-approved-link-identity"}}
}
```

Carrier up with no current peer evidence:

```json
{
  "link":{"carrierUp":{"source":"rtnetlink","observedAt":"2026-09-29T15:26:41-06:00"}},
  "peer":{"unknown":{"reason":"no-current-evidence","sourcesConsidered":["bridge-fdb","neighbor","kea"],"observedAt":"2026-09-29T15:26:41-06:00"}},
  "addresses":[],
  "recognition":{"unknownPeer":{"evidenceRefs":[]}}
}
```

Fresh peer plus an authenticated overlay identity, if the living approves such a link-recognizable identity:

```json
{
  "link":{"carrierUp":{"source":"rtnetlink"}},
  "peer":{"present":{"source":"bridge-fdb","evidenceRef":"ephemeral:fdb:7","sourceObservedAt":"<post-observer-start-event>","freshnessBasis":"witnessed-source-event"}},
  "addresses":[{"kind":"neighbor","opaqueEvidenceRef":"ephemeral:neighbor:4","freshness":"fresh","source":"rtnetlink"}],
  "recognition":{"knownClusterNode":{"nodeId":"<cluster-owned-id>","trustValue":"<projected-trust>","proofSource":"authenticated-overlay-session","freshUntil":"<bounded-time>"}}
}
```

Carrier up with only stale evidence, matching the current Zeus investigation:

```json
{
  "link":{"carrierUp":{"source":"rtnetlink","observedAt":"2026-09-29T15:38:15-06:00"}},
  "peer":{"unknown":{"reason":"no-current-peer-evidence","sourcesConsidered":["bridge-fdb","neighbor"],"observedAt":"2026-09-29T15:38:15-06:00"}},
  "addresses":[{"kind":"dhcp-lease","opaqueEvidenceRef":"ephemeral:lease:9","freshness":"stale","source":"kea"}],
  "recognition":{"unknownPeer":{"evidenceRefs":["ephemeral:lease:9"]}}
}
```

The corresponding value may appear only in the separate root-only diagnostic view:

```json
{"rootRawAddressEvidence":{"kind":"dhcp-lease","rawValue":"10.44.0.148","sourceObservedAt":"2026-09-29T14:45:21-06:00"}}
```

It must not appear in the public observation or event stream, and it must not identify Zeus. Field proved that lease's MAC/DUID belonged to Prometheus's integrated NIC under an earlier topology.

## Optional recognizer seam

The collector passes only time-bounded evidence references to a recognizer interface. With no approved stable proof, the implementation returns `RecognizerDisabled` or `UnknownPeer`; this is complete behavior, not a degraded state.

If the living rules that every cluster node presents one stable, authenticated identity that can be bound to a particular link, Horizon may project the cluster-owned public identity and trust value already authored with that node. The recognizer may then return `KnownClusterNode` only from a cryptographic proof whose ingress is attributable to this edge. It must include proof provenance and freshness. A DNS result, IPv4/IPv6 address, MAC, DHCP client ID/DUID, hostname string, prior lease, or stale neighbor is insufficient by itself.

The recognizer is a pure consumer of projected cluster data plus observations. It may not enroll nodes, edit trust, mint keys, or persist a discovered mapping into cluster data. This keeps identity ownership in the cluster feature and keeps CriomOS free of Goldragon-specific facts.

## Runtime exposure, privacy, and retention

Expose the redacted public snapshot and transition stream through a local read-only Unix socket under `/run/usb-downlink-observer/`; journald may receive only those same redacted transitions. Keep the raw diagnostic view on a separate root-only socket or root-only file in that runtime directory. The package should be shaped so a later Nexus can carry the typed public observation without changing its semantics, but a new privileged/ordinary Nexus is not required for the first proof.

Collect no packet payloads, DNS names, remote application banners, or unrelated interfaces. Keep MACs, DUIDs, and addresses as redacted/opaque ephemeral evidence references in the public snapshot and event surface. Raw values remain only in the separate root-only diagnostic view and only as long as needed to correlate source evidence. Restart may discard all observer state. Default journal retention applies only to redacted transitions; the observer creates no durable database. No observation is exported from the host unless a later, separately designed consumer is authorized.

## Router extension point

Stage one enables the observer only when `UsbDownlink` is declared and `horizon.node.behavesAs.router` is false. It reads `br-downlink` and the same USB bus-role matcher already owned by `usb-downlink.nix`.

If the living rules that Router USB edges are watched too, the collector should accept a projected edge selector and bridge name while preserving the Router module as sole bridge/DHCP/NAT/firewall owner. Prometheus needs an additional distinction: `br-lan` aggregates Wi-Fi and USB LAN membership, so a bridge-wide peer cannot automatically be attributed to the USB edge. Router support must filter evidence by the USB member/port and test multi-member behavior. It must not create a second observer with conflicting semantics.

## Test matrix and acceptance

The smallest behavioral proof is a deterministic reducer test fed synthetic timestamped source events. It must cover:

| Case | Expected observation |
| --- | --- |
| no matching USB Ethernet | `LinkAbsent`; peer unknown; recognizer disabled/unknown |
| USB present, carrier down | `CarrierDown`; no failure or recovery event |
| carrier rises, no FDB/neighbor/Kea evidence | `CarrierUp` plus `PeerUnknown`/no current evidence; unknown is ordinary |
| fresh post-start FDB or neighbor event | peer present with witnessed-event freshness basis; no node identity inferred |
| observer starts with a pre-existing FDB/neighbor entry lacking trustworthy source age | peer unknown or stale; snapshot read time never makes it present |
| lease exists only before carrier transition | stale address evidence; peer unknown; no identity |
| lease/address reused by another topology | address remains evidence only; never selects a node |
| authenticated overlay proof, recognizer enabled | known cluster node with cluster provenance, trust, and expiry |
| recognition proof expires | recognition stale/unknown even if neighbor remains stale |
| Kea has no witnessed request | no `DHCP_FAILURE` |
| observer restart with stale entry already present | snapshot read time is recorded separately; peer remains unknown/stale and no prior identity is resurrected |
| raw address evidence | raw value appears only in the root diagnostic view; public snapshot/events carry an opaque reference |

One non-Router NixOS VM test then proves integration: instantiate the existing `UsbDownlink` fixture, observe carrier down, carrier up without current peer evidence, and normal client attachment and DHCP traffic after the observer starts. Restart the observer with an old entry already present and prove that snapshot read time does not make it fresh. The test manipulates virtual links and ordinary clients from the test harness; the observer itself sends no traffic. Existing hotplug convergence coverage remains, while this test asserts the intermediate observation sequence. Expiry or peer-absence timing is not asserted until Psyche rules that policy.

Acceptance requires that the service has no network capabilities needed to send packets; no `ExecStart`/event path invokes `ping`, `arping`, `ndisc6`, DHCP clients, `networkctl renew`, link setters, service restarts, or firewall tools; the network owner configuration is byte-for-byte unchanged by enabling the observer; every identity result includes cluster provenance and freshness; no snapshot read timestamp is used as source-event freshness; public output contains no raw address/MAC/DUID; and the four examples above appear in behavioral fixtures. Router behavior is absent and explicitly deferred.

## Exact implementation stages and named write set

Stage 1, passive non-Router observation, writes only CriomOS source:

- `packages/usb-downlink-observer/Cargo.toml`
- `packages/usb-downlink-observer/src/main.rs`
- `packages/usb-downlink-observer/default.nix`
- `modules/nixos/network/usb-downlink-observer.nix`
- `modules/nixos/network/default.nix` (one module import)
- `checks/usb-downlink-observer/default.nix` (reducer/evaluation contract)
- `checks/usb-downlink-chain/default.nix` (intermediate-state VM behavior)
- `flake.nix` (package and check registration)

`usb-downlink-observer.nix` derives enablement and `br-downlink` from the existing projected `UsbDownlink` capability. Therefore stage 1 writes neither `goldragon/cluster-definition.datom` nor Horizon: adding observer facts there would duplicate a consequence of the existing feature.

Stage 2 is conditional on the living's identity ruling. If the existing projected Yggdrasil/Tailnet/Criome public identity and trust fields are sufficient, it adds only recognizer inputs/tests in the same CriomOS package and module. If one new cluster-authored field is required, the write train is:

- `horizon-rs/lib/src/proposal.rs` and its authored type/projection tests;
- the Horizon generated projection produced by its repository-supported generator, never hand-edited;
- `goldragon/cluster-definition.datom` and `goldragon/flake.nix` projection checks;
- the Horizon input pins in Goldragon and the normal consumer pin train;
- the CriomOS observer module/package/checks named above.

Stage 3, Router coverage, is conditional on the living's edge-scope ruling. It changes `modules/nixos/network/usb-downlink-observer.nix`, the observer package, `checks/router-usb-downlink-binding/default.nix`, and `checks/usb-downlink-chain/default.nix`; it must not change `modules/nixos/router/default.nix` unless a test proves the existing module does not expose enough read-only edge selection.

Each stage is its own reviewed pin/build/deployment train. None is authorized by this design.

## Alternatives and tradeoffs

- Networkd carrier alone is smallest, but it cannot distinguish “carrier up” from “a peer has emitted evidence.” Keep it as one source, not the verdict.
- Kea lease state is readily available, but leases survive topology and time. Treating a lease, DUID, MAC, or address as identity recreates the exact false-Zeus conclusion just disproved.
- Active heartbeat, ARP/ICMP probing, DHCP renewals, or automated link/service recovery could answer different questions, but they perturb the system and combine observation with control. They are outside this observer.
- A full Nexus from the first implementation offers a typed subscription surface, but adds socket authority, protocol, storage, and lifecycle design before the semantics are proven. Keep the state/event types transport-independent and add a Nexus only when a real cross-process consumer exists.
- Hard-coding one expected downstream node makes current debugging simpler, but contradicts movable topology and makes an unknown or foreign peer falsely unhealthy.

## Questions for Psyche

1. Does every trusted cluster node carry one stable cryptographic identity that it presents in a form attributable to a particular local link? If yes, which cluster-owned identity and proof bind it to that edge? The proposal will not substitute MAC, DUID, hostname, or IP.
2. Should the same observer cover USB members of a Router's `br-lan`, or is the ruled scope only the non-Router `UsbDownlink` provider first?
3. What observation duration, start condition, source coverage, and freshness rules would justify a future `PeerAbsent` state? Until all four are ruled, the surface remains `PeerUnknown` with “no current evidence.”
4. Is local root-only, boot-scoped state with ordinary journald retention the right privacy/ownership boundary, or should any observation stream be retained or exposed to a named Nexus consumer?
