# Network Nexus refresh handoff

**Status:** owner-authored architecture and refresh handoff, 2026-09-22. It
authorizes neither a launch, a replacement seat, retirement, nor a network
mutation. Mind High `4b0f60` remains the architecture owner until a successor
has its distinct Flow UUID, native identity, exact HM/Herdr binding, accepted
skills, work-worker relay, successor acceptance, and an explicit transfer.
The user has authorized Field `03` as the sole controller for fresh-successor
lifecycle work through the existing Field Sol `753` coordinator. Return this
handoff and all results through `753`/`03` to `4b0f60` until that transfer.

## Successor boundary

The successor preserves the **gpt-6-astra / medium** profile. This record does
not infer a profile mapping or claim that it has been verified. It receives a
new Flow UUID, never a transferred native handle. Its first native injection
requires a receipt; this report does not prescribe or claim a literal token.
Pending final returns are relayed and acknowledged before transfer. Existing
`0ab019`/`f72ab7` handles and crossover routes `9e7ea5`, `98ac2e`, and
`0ab019` remain protected. No successor inherits native handles.

The two local audit/coordination children have completed and their limits are
incorporated: current routes remain unresolved and cannot receive a blind
send; the Flow verifier has a concrete gap. In `lib.rs`,
`SubmitBindingRegistration` currently yields `VerifierUnavailable`, and the
meta path lacks a `ConnectionContext`; existing triad support for
`SO_PEERCRED` does not supply the missing attester/delegation registry. The
existing verified-record and typed meta-signal-flow submission are useful
building blocks, not that registry. This needs a separately reserved lane.

## Network Nexus contract

The target is one Network Nexus for cluster network state and control. It uses
CriomOS and cluster data as its source of desired configuration and Horizon's
node-enabled capabilities as the typed selector. It covers USB links, Wi-Fi,
uplink and connectivity. An Ouranos API is optional and may be used only when
wired Internet exists. It must not create a second network controller.

Desired configuration is durable and distinct from observations: kernel link,
address, route, DNS and connectivity evidence each carry their own time and
source. An ordinary observation reports those facts; a privileged mutation is
a typed desired-state request. The controller reconciles a single
generation-bound, idempotent plan and records stale input, refusal, rollback
and evidence. A stale observation does not rewrite desired state, and a
successful materialization does not prove link or Internet connectivity.

Map the source path before code changes:

| Layer | Responsibility |
| --- | --- |
| Goldragon | assigns a typed `NodeService` capability to a node. |
| Horizon | projects that assignment as node-enabled capability data. |
| Lojix | materializes the selected typed projection. |
| CriomOS | applies the selected network owner: existing NetworkManager or networkd, never both for one link. |
| Network Nexus | reads evidence and drives one authorized reconciliation plan; it does not replace the declarative owner. |

The USB proposal is an anchored candidate, not a present implementation:
`NodeService::UsbIpv4Gateway { downstreamInterface, MAC, gatewayIPv4Cidr,
uplink }`. It must be capability-driven, with no hostname gate. The existing
generic `networkd` share is separately selected by center/non-router traits;
it is not to be widened onto the NetworkManager-owned USB link. Exactly one
subsystem owns NAT, DHCP/DNS and the downstream link. Existing implementation
state must be re-observed before any claim of current operation.

The reference chain is Horizon `b45d6ad` on main and candidates Signal-Lojix
`01ae2b1e`, Meta-Signal-Lojix `8fb526c4`, Lojix `6b299ec1`, Goldragon
`a911515c`, and CriomOS `9842f51a`. These are source or scoped-check receipts,
not a coherent materialized graph, system build, deployment, or E2E proof.
The separate Field `6db4fe` report records a saved NetworkManager profile and
a source candidate; neither establishes that candidate's current deployment
or durability. Field Terra `034` may continue bounded Prometheus repair under
Field `6db4fe`; this handoff receives its evidence and does not block it.

## Preserved lanes and proof gates

Existing Flow/Message work is not network work. Preserve Medium `2c61af` as
authoritative Flow-verifier coordinator; f72's protected `2836` Flow store,
`2862` Signal Flow and `2864` Message lanes; Medium `3830` Flow library; Low
`e7983847`; Field `9dd3776` consumer/rollback; the reported Field `6db4fe` VM
lane; and protected `553901`, `1834`, `1835`, and `542442` lanes. The reported
Flow/Message bridge `18e14e`, Raw `3ba5d946`, and Flow store `87bd74bd` are
published candidates only: no compiled coherent graph is claimed, and builder
recovery remains pending.

Before a Network Nexus control path is enabled, require: a materialized
Horizon-to-CriomOS payload; one selected link owner; exact generation and plan
identity; an authorized privileged request; a bounded rollback; and evidence
for link, route, DNS and configured connectivity. Refusal, stale generation,
or unavailable privilege leave the prior desired configuration intact. This
is also the boundary for any future optional Ouranos API.

## Sources

- Living authorization and ownership decisions relayed in the current
  `4b0f60` conversation; successor status and completion are handoff facts,
  not native-identity or skills receipts.
- `flows/753e69/reports/horizon-usb-gateway-contract.md` and
  `usb-gateway-integration-ownership.md`: proposed capability, layer map and
  protected integration boundaries.
- `flows/6db4fe/reports/network-durable-source.md` and
  `prometheus-uplink-reliability-2026-09-22.md`: attributed Field source and
  operational observations, with their stated deployment limits.
- Full source anchors reported for Flow/Message candidates:
  Message `18e14e3571c549fe6b57fbe8fdf46a1a240ca2c5`, Raw
  `3ba5d946527163a8fd545d9968e4e23db83d0642`, and Flow
  `87bd74bd4c995d8947440e78d18c0cd6a9ee9597`; no compiled-graph receipt.
- Completed local child returns from `checkup_architecture` and
  `census_contract_design`, relayed by the main flow: route and verifier-gap
  findings only; no fresh socket, native or deployment probe was performed.
