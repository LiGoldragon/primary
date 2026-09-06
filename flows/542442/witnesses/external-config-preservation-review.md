# External Horizon preservation review

## Method

Compared `reports/horizon-preservation.md` against the legacy Horizon producer
at `f8c5808466a47c2fd741cf0b119d73e8ba2add3d`: `proposal.rs`, `machine.rs`,
`io.rs`, `species.rs`, and the old `ClusterProposal::project` path. Checked
the resulting field set against Goldragon's production `proposal.datom` without
reproducing private material.

## Result

The map covers legacy root, node, machine, I/O, service, user, domain, trust,
network, router, key, and viewpoint-projection fields. The required correction
is representation fidelity: legacy `VmHost.kvm` is the closed
`KvmAvailability` value (`Available` or `Absent`), so the new contract must
retain a typed equivalent rather than silently flatten it to a Boolean.

Legacy `NodeSpecies` is a mixed classification. Consumer search found
`TestVm` and `CloudNode` behavior in CriomOS/Horizon, while `MediaBroadcast`
and `RouterTesting` have no production data occurrence or consumer branch
beyond legacy enum identity. The accepted replacement must express active
behaviors as independent typed capabilities/facts rather than relabeling the
mixed enum as one `role` field.

## Sources

- `reports/horizon-preservation.md`.
- `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-datom-node-542442/lib/src/{proposal,machine,io,species,horizon}.rs`.
- `/home/li/wt/github.com/LiGoldragon/goldragon/generic-nodes-542442/proposal.datom`.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/horizon-datom-integration-542442/modules/nixos/{criomos,test-vm-guest,test-vm-host}.nix`.
