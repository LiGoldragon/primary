# Zeus contact: Mind synthesis and production questions — 2026-09-29

Mind Sol `b666e7` prepared this bounded synthesis for the Field → Mind → Psyche pipeline. Its direct operational source is Field Sol `1bc255`, report `flows/1bc255/reports/zeus-reachability-2026-09-29.md` as published in primary revision `d26dfb82276c`. Mind made no host, service, configuration, network, or source change. The root cause and a lasting fix are not yet proven.

## Judgment now

The current intended path, corrected by the living, is:

`Prometheus br-lan (10.18.0.1/24) → Ouranos built-in Ethernet (10.18.0.101/24) → Ouranos UsbDownlink br-downlink (10.44.0.1/24) → Zeus`

Field directly proved the path through Ouranos to the local side of `br-downlink`: Prometheus answered from Ouranos; Ouranos's USB adapter and bridge were configured, had carrier, and were forwarding at 100 Mb/s. Field did not prove any Zeus identity or response beyond that boundary. The exact current failure is therefore: **no identified Zeus endpoint was learned or reached behind Ouranos's downlink**, not a demonstrated firewall, DHCP, NAT, Yggdrasil, or CriomOS defect.

The strongest new inference is that the address Field probed may not be Zeus at all. Historical live evidence in `flows/38de5b/receipts/live-witness-20260925.md` identifies `10.44.0.148` and MAC `84:47:09:75:88:68` as Prometheus's integrated `eno1` when Prometheus was downstream of Ouranos. Field found a recent Kea ACK for that same address and MAC at 14:45:21, but no current lease-database or endpoint-identity witness. After the living changed the cables, the old lease can no longer name the host by topology alone. The former Zeus address `10.18.0.103` likewise belongs to the earlier Prometheus→Zeus arrangement and is stale for the current topology.

## Evidence by status

### Directly observed today by Field

- At 15:24:22 Ouranos's USB downlink had no carrier and `br-downlink` was down.
- The Ouranos journal records carrier loss at 14:50:55 and carrier gain at 15:26:41. At 15:27–15:29 the USB member and `br-downlink` were `UP,LOWER_UP`, the sole bridge member was forwarding at 100 Mb/s, and `br-downlink` held `10.44.0.1/24`.
- The forwarding database had no learned downstream client MAC.
- Kea had ACKed `10.44.0.148` to MAC `84:47:09:75:88:68`, most recently in the bounded journal at 14:45:21. This was a prior DHCP event, not proof of a current endpoint or of Zeus.
- A targeted probe produced a `FAILED` neighbor for `10.44.0.148`; ICMP lost 2/2 and TCP/22 returned `No route to host`.
- Ouranos could reach Prometheus on the upstream `10.18.0.0/24` segment. No host was mutated.

### Historical facts relevant to interpretation

- On 2026-09-25, before the topology change, Prometheus held `10.44.0.148/24` on integrated `eno1` with MAC `84:47:09:75:88:68` and gateway `10.44.0.1`; Zeus was then `10.18.0.103` behind Prometheus's `br-lan`.
- The authored cluster data declares Ouranos `UsbDownlink.{ 10.44.0.0/24 }`. The CriomOS consumer gives that non-Router capability `br-downlink`, DHCP, DNS, and forwarding/NAT ownership.
- Prometheus's Router feature owns `br-lan` at `10.18.0.1/24` and derives USB Ethernet membership in that LAN. These are two implementations of the living's downstream-provider idea, but they do not currently express the topology in the same way.

### Hypotheses, not findings

- Zeus may be powered off, unbooted, disconnected, attached beyond an unobserved peer or switch, using another interface/address/MAC, or failing to transmit at layer 2.
- The carrier transition may have been a physical reconnect, negotiation event, or change at an intermediate peer. Ouranos alone cannot identify its cause.
- A firewall or disabled SSH could matter after neighbor resolution, but the present failed neighbor prevents that diagnosis.
- A current software defect may still exist, but no observation here selects one. Changing firewall, DHCP, NAT, Yggdrasil, or networkd now would be speculative.

### Missing decisive witness

The minimum missing witness is a direct mapping of **Zeus identity → physical interface → current MAC/address → observed traffic on Ouranos's downlink**. Obtain it at Zeus's console or from a controlled reconnect while capturing carrier, FDB, DHCP, ARP/neighbor, and then one SSH connection. Without that mapping, neither `10.44.0.148` nor any proposed source fix is attributable to Zeus.

## Next bounded attack

Preserve the current capture first. Then perform one physical or identity intervention at a time so its effect is attributable:

1. At Zeus, witness power/boot state and read the connected NIC's link, MAC, and IPv4 state locally. Record which physical cable or adapter it uses.
2. On Ouranos, begin a bounded observation of carrier events, bridge FDB changes, Kea events, and ARP/neighbor traffic for `br-downlink`.
3. Disconnect and reconnect only the Zeus-side downlink once, observing which Ouranos carrier/FDB/DHCP event changes. Do not change network configuration in this step.
4. Correlate the locally read Zeus MAC with the learned FDB/DHCP identity. Probe that current address once for neighbor resolution and SSH.
5. Only after this split: if no carrier, stay in the physical/peer path; if carrier but no Zeus frames, diagnose Zeus NIC/boot; if DHCP and neighbor work but SSH fails, inspect Zeus routing, firewall, and sshd; if Zeus is reachable, capture forwarding/DNS/Internet and recovery-after-replug acceptance before calling the feature operational.

This attack can identify the broken boundary. It does not yet promise a software change.

## Production design decision for Psyche and Mind Astra

The durable question is: **should every intentional downstream edge be explicit in cluster topology data, with the host capability choosing how to realize it, or should Router continue to infer a downlink from any eligible USB Ethernet device while only non-Routers declare `UsbDownlink`?**

### Option A — explicit downstream edges, composed by host capability (Mind recommendation)

Record that Ouranos provides a downstream segment to Zeus and that Prometheus provides its LAN/downstream segment to Ouranos. Keep addresses and intended peer/segment identity with topology data. Let `UsbDownlink` realize a separate `br-downlink` on a non-Router; let Router realize the declared edge as a port of `br-lan`. Router remains the single DHCP/DNS/NAT owner for its LAN, so this does not add a second NAT stack.

This matches the living's requirement that data live with data and that the same feature mean “plug in USB Ethernet and provide downstream,” while preserving the legitimate implementation difference between a Router LAN and a non-Router transit hop. It also makes an unexpected old peer lease visible as a topology mismatch rather than implicit success.

Cost: the schema and consumers must represent peer/segment intent without binding correctness to unstable interface names or hardware addresses. Migration and tests are required.

### Option B — retain the current split

Keep explicit `UsbDownlink` only for non-Routers and let Router derive all eligible USB Ethernet devices into `br-lan`.

Benefit: smaller change and stateless hotplug behavior. Cost: the intended edge and peer remain implicit, so monitoring cannot distinguish an expected Zeus link from an old Prometheus lease or an unintended USB NIC. This is the ambiguity exposed today.

### Option C — one generic downstream-provider capability

Replace the two paths with a parameterized downstream-provider feature whose service profile selects a dedicated bridge or Router LAN composition.

Benefit: one vocabulary and one acceptance contract. Cost: a wider refactor with greater regression risk. It should not be coupled to restoring Zeus contact.

Psyche should judge A versus B now. C is an architectural follow-on only if the existing capability boundary is found inadequate. A broader NAT, Wi-Fi, tailnet, or Yggdrasil redesign is outside this Zeus incident.

## Production acceptance and observable recovery

Whichever design is chosen, production readiness needs one per-edge health story rather than “the interface is up”:

- physical carrier state and last transition;
- expected bridge membership and forwarding state;
- learned downstream FDB identity;
- DHCP discover/offer/request/ack and the current lease identity;
- neighbor resolution and a named peer health probe;
- DNS and Internet forwarding only after peer identity is established;
- recovery after boot and after one unplug/replug, with bounded time and an observable failure state when recovery does not happen.

These observations should say which boundary failed. Automatic reconfiguration is not justified merely because a peer is absent; recovery should first reapply the declared link state, then report the unresolved physical, identity, or peer-health boundary.

## Pipeline action record

| Layer | Action actually taken | Action still owed |
| --- | --- | --- |
| Field | Performed the read-only Ouranos/Prometheus reachability, carrier, bridge, FDB, Kea, neighbor, ICMP, and TCP observations; recorded exact times; made no host change. | Obtain the bounded physical/console identity witness and one-at-a-time reconnect correlation, under Fable's Zeus-first ruling. |
| Mind | Reconciled today's witness with the corrected topology, authored capability shape, and historical endpoint identities; identified the stale-identity ambiguity; framed production options and acceptance. Made no source or host change. | After the missing witness, name the recurring fault from evidence and scope the smallest lasting implementation. Do not claim a lasting fix before that. |
| Psyche | Fable ruled Zeus contact priority #1: Field attacks the host; Mind makes the lasting fix and explains why the same fault returns. | Decide the explicit-topology question (A or B), judge the eventual action, and present the Field/Mind/Psyche record to the living. No Psyche design decision or implementation is claimed here. |

The Codex update was separately assigned by Fable and is not part of this Zeus report. The requested book/page presentation follows the Zeus work in Fable's priority order; this report supplies the bounded Mind portion and does not claim that publication occurred. The living's final `maybe` clause was unfinished and is not completed here.
