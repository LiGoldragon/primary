# Horizon USB IPv4 gateway contract

## Finding

No current Horizon type or projected payload describes an IPv4 Internet
gateway over USB. `UsbInternetGateway` in the earlier durable-design report is
a candidate name only, not an accepted schema or implemented feature.

The prior CriomOS host-name-gated USB-share draft was removed. The remaining
generic Networkd share is selected by derived Center/non-Router traits and
cannot represent the Ouranos link.

## Exact producer to consumer path

1. Goldragon authors node service records in
   `proposal.datomic`. Ouranos presently has Tailnet, builder, and Persona
   Development services, but no USB IPv4 gateway record.
2. Horizon's hand-owned `NodeProposal.services: Vec<NodeService>` and the
   closed `NodeService` enum parse and serialize each service through the
   `Datomic` implementation in `proposal.rs`.
3. `NodeProposal::project` in `node.rs` copies `services` unchanged into the
   projected `Node`; `ClusterProposal::project` in `horizon.rs` supplies that
   node as the viewpoint's `horizon.node`.
4. Lojix projects the selected node, serializes it as `horizon.json`, and
   exposes `horizon = builtins.fromJSON (builtins.readFile ./horizon.json)` in
   its generated flake input.
5. CriomOS obtains that flake input as `horizon`. Its `node-services.nix`
   accepts tagged capability records with a `kind` and payload fields.

## Candidate payload — proposal, not accepted schema

The smallest complete shape appears to be:

```rust
NodeService::UsbIpv4Gateway {
    downstream: Interface,
    downstream_mac: MacAddress,
    gateway: Ipv4Cidr,
    uplink: Interface,
}
```

For the observed link, the proposed Goldragon assignment would name downstream
`enp0s20f0u1c2`, its observed MAC `00:0e:c6:33:4f:97`, gateway
`10.44.0.1/24`, and uplink `enp0s31f6`. These are deployment facts carried in
the payload; the CriomOS consumer must never select `ouranos` by host name.

`Interface` already models an interface name. New `MacAddress` and
IPv4-only addressed-CIDR types are warranted: `TapSubnet` describes an IPv4
network rather than a gateway address, and `NodeIp` permits IPv6.

## Consumer integration

CriomOS should add a NetworkManager-owned module, imported from
`network/default.nix`, that gates entirely on this proposed capability. It
should configure the downstream link and its gateway/DHCP/DNS behavior from
the payload, retain NetworkManager ownership already selected by `normalize.nix`,
and declare only the payload's upstream interface for NAT/forwarding.

Do not extend `network/networkd.nix`: its current `behavesAs.center &&
!behavesAs.router` gate, fixed `10.47.0.0/24`, and Networkd ownership are a
separate generic configuration.

## Authorship, generated output, and tests

`proposal.rs`, `node.rs`, and `horizon.rs` are hand-owned Horizon behavior.
`lib/ethos/horizon.ethos` generates `lib/src/generated/d3.rs` through
`generation.rs`; the generated tree supplies Datomic anatomy for declared
types, while `NodeService` remains hand-owned because it carries serde and
validation behavior.

The implementation sequence is:

1. Add the variant, newtypes, codec arms, and exact Datomic round-trip test.
2. Add a projection test showing its payload reaches the viewpoint node.
3. Assign the capability only in Goldragon's Ouranos record.
4. Keep Lojix materialization unchanged except for consuming the new Horizon
   revision; add or update its materialized-input test if the pinned contract
   makes this necessary.
5. Add a focused CriomOS evaluation test proving payload-only enablement,
   NetworkManager ownership, gateway/subnet/uplink values, and no node-name
   predicate.

## Open decisions and ownership

The capability name and its exact codec/newtype representation are unresolved.
So is the division of NAT responsibility between NetworkManager shared mode and
declarative firewall rules; exactly one must own NAT. The firewall backend and
the complete DHCP option set also remain unverified.

The flow's durable-design handoff assigns permanent Ouranos NetworkManager,
firewall/NAT, and Horizon-capability mutation to Terra. Astra's historical
source lock `3939` is absent; the current related Astra lock `3926` is only on
its network-chain report. No pending source change was observed in the scoped
CriomOS workspace.

## Sources

- `flows/753e69/reports/ouranos-share-durable-design.md`
- `flows/753e69/reports/network-path-plan-2026-09-21.md`
- `flows/024bc7/vision/network.md`
- `/home/li/wt/github.com/LiGoldragon/goldragon/post-terminus-horizon-data/proposal.datomic`
- `/home/li/wt/github.com/LiGoldragon/horizon-rs/post-terminus-horizon-data/lib/src/{proposal,node,horizon,generation}.rs`
- `/home/li/wt/github.com/LiGoldragon/horizon-rs/post-terminus-horizon-data/lib/{ethos/horizon.ethos,src/generated/d3.rs,tests/datomic_proposal.rs,tests/node.rs}`
- `/home/li/wt/github.com/LiGoldragon/lojix/horizon-contract-repin-8565e8/src/{schema_runtime,bootstrap}.rs`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/usb-share-6db4fe/modules/nixos/{node-services,normalize}.nix`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/usb-share-6db4fe/modules/nixos/network/{default,networkd}.nix`
