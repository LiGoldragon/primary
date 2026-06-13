# horizon-rs model — where a test-VM role/species + host/location slot in

Read-only grounding for cloud-designer session 47. Every claim cites a
file:line under `/git/github.com/LiGoldragon`. Mutates nothing.

## Taxonomy: two separate enums carry "what kind of thing"

There is no `role` module. "Role/species" splits across two closed
enums in `horizon-rs/lib/src/species.rs`:

- **`NodeSpecies`** (`species.rs:13-23`) — the node's *cluster role*:
  `Center, LargeAi, LargeAiRouter, Hybrid, Edge, EdgeTesting,
  MediaBroadcast, Router, RouterTesting`. This is the "role" axis the
  psyche means. A new `TestVm` (or `EdgeTestVm`) variant goes here.
- **`MachineSpecies`** (`species.rs:37-40`) — the *substrate*:
  `Metal` | `Pod`. `Pod` already means "virtual machine." This is the
  axis that carries virtual-vs-physical, NOT the cluster role.

Service roles are a *third* axis: the open-ended `NodeService` enum
(`proposal.rs:96-121`): `TailnetClient, TailnetController,
NixBuilder{maximum_jobs}, NixCache, PersonaDevelopment{capabilities}`.
Per-node `Vec<NodeService>`, never inferred from node name
(`proposal.rs:88-93`).

`NodeSpecies` drives derived flags via `TypeIs::from_species`
(`node.rs:166-180`) and then `BehavesAs::derive` (`node.rs:182-204`).
Note `BehavesAs.virtual_machine` is set from `MachineSpecies::Pod`
(`node.rs:191`), and `iso` from `!virtual_machine && io_disks_empty`
(`node.rs:192`). So "is this a VM" is already a derived boolean keyed
on `MachineSpecies::Pod`, not on the cluster role.

## Node record shape

Input node = `NodeProposal` (`proposal.rs:36-94`), positional in nota:

```
species: NodeSpecies          # the role/species variant
size: Magnitude (default Zero) # capacity ladder, not raw resources
trust: Magnitude (default Min)
machine: Machine              # hardware — see below
io: Io
pub_keys: NodePubKeys         # ssh required; nix/ygg optional
link_local_ips, node_ip: Option<NodeIp>   # internal CIDR, cluster-authored
wireguard_pub_key, nordvpn, wifi_cert, wireguard_untrusted_proxies
wants_printing, wants_hw_video_accel
router_interfaces: Option<RouterInterfaces>
online: Option<bool>          # admin-offline gate (default Some(true))
services: Vec<NodeService>
```

`Machine` (`machine.rs:12-39`):
```
species: MachineSpecies       # Metal | Pod
arch: Option<Arch>            # Pod defers to super_node
cores: u32
model: Option<ModelName>
mother_board: Option<MotherBoard>
super_node: Option<NodeName>  # "Pod-only: which node hosts this pod" (machine.rs:21)
super_user: Option<UserName>  # "Pod-only: which user runs this pod" (machine.rs:23)
chip_gen: Option<u32>
ram_gb: Option<u32>           # only existing memory field
```

**A node-hosted-on-another-node relation ALREADY exists:**
`Machine.super_node: Option<NodeName>` (`machine.rs:21`), explicitly
"which node hosts this pod." `NodeProposal::resolve_arch`
(`node.rs:549-575`) walks one hop from a Pod to its `super_node` to
inherit arch — `Error::MissingSuperNode` / `UnresolvableArch`
(`node.rs:564-573`). This IS the "HOST (physical node the VM runs on)"
edge the psyche wants. Output `Node` (`node.rs:27-126`) carries the
full `machine: Machine` through (`node.rs:35`, set at `node.rs:404-405`,
`node.rs:413`), so `super_node` survives projection.

Resources today are NOT raw cpu/mem/disk on the proposal: capacity is
the abstract `Magnitude` ladder (`magnitude.rs:29-35`), projected to
`AtLeast` booleans (`magnitude.rs:61-66`). `Machine.cores` (u32) and
`Machine.ram_gb: Option<u32>` are the only literal resource fields;
disk is only described structurally via `Io` filesystems, not a size.

## Projection: ClusterProposal -> per-node Horizon (Viewpoint)

`ClusterProposal` (`proposal.rs:24-34`): `nodes`, `users`, `domains`,
`trust`. Entry-point `ClusterProposal::project(&Viewpoint)`
(`horizon.rs:31-145`). `Viewpoint{cluster, node}` (`horizon.rs:25-29`).

1. Validate viewpoint node exists (`horizon.rs:34-36`) and single
   tailnet controller (`horizon.rs:39`, `:147-171`).
2. Project every node via `NodeProposal::project` (`node.rs:334-475`);
   trust=Zero nodes dropped (`horizon.rs:45-49`); arch resolved
   (`horizon.rs:50`).
3. Fill viewpoint-only fields on the one viewpoint node via
   `Node::fill_viewpoint` (`node.rs:485-547`) — builder configs, cache
   urls, sibling/dispatcher/admin ssh keys.
4. Remove viewpoint from map; remaining go in `ex_nodes`
   (`horizon.rs:135-143`).

Output `Horizon{cluster, node, ex_nodes, users}` (`horizon.rs:16-23`).

## Address / Criome domain / location derivation

`CriomeDomainName::for_node(node, cluster)` ->
`"<node>.<cluster>.criome"` (`name.rs:106-109`), called at
`node.rs:339`. Cache subdomain `nix.<domain>` (`name.rs:111-113`).
Tailnet base `tailnet.<cluster>.criome` (`name.rs:79-83`). Node IP is
NOT derived — it is cluster-authored `node_ip: Option<NodeIp>` (CIDR,
`address.rs:90-122`) passed through (`node.rs:416`). **There is no
`location`/datacenter/region field anywhere** (grep: only `ram_gb` and
io memory_percent match resource terms; nothing for location). The
closest existing "where it physically is" datum is `super_node`.

## Example node declarations (positional nota, source-decl order)

fieldlab `dune` — the live **Pod hosted on another node** (the model
for a test VM today), `CriomOS-test-cluster/clusters/fieldlab.nota:80-104`:
```
dune (Edge
  Min Max
  (Pod (Some X86_64) 2 (Some [fixture-pod]) None (Some atlas) (Some aria) None (Some 4))
  ... [(TailnetClient)])
```
Reading the `Machine` tuple: `Pod`, arch `X86_64`, 2 cores, model,
mother_board None, **super_node `atlas`**, super_user `aria`, chip_gen
None, ram_gb 4. So `dune` is a VM declared to run on host `atlas`.

Live goldragon `ouranos` — `EdgeTesting` Metal node,
`goldragon/datom.nota:28-58`: `(Metal (Some X86_64) 12 ... )`,
`super_node` = None (physical), services include `TailnetController`,
`NixBuilder`, `PersonaDevelopment`. All goldragon nodes are `Metal`
with `super_node None`; no production VM exists yet.

## Where the test-VM concept slots in (design landing points)

- **Role/species variant** — add a `TestVm` (or `EdgeTestVm`) variant
  to `NodeSpecies` (`species.rs:13-23`). Must be threaded through
  `TypeIs` (struct `node.rs:152-164` + `from_species` `node.rs:166-180`)
  and reflected in `BehavesAs::derive` (`node.rs:182-204`). This is the
  "first-class test-VM role" the psyche wants. Substrate stays
  `MachineSpecies::Pod` (`species.rs:37-40`) so `virtual_machine`
  derives true (`node.rs:191`).
- **HOST (physical node the VM runs on)** — reuse the EXISTING
  `Machine.super_node: Option<NodeName>` (`machine.rs:21`). It already
  means "which node hosts this pod" and is already projection-walked
  (`node.rs:549-575`). No new relation needed; possibly rename/clarify
  the doc to cover test VMs.
- **Resources (cpu/mem/disk)** — `cores` and `ram_gb` already live on
  `Machine` (`machine.rs:16,38`). A disk-size field would be new on
  `Machine` (none today; disk is only structural in `Io`). Decide
  whether on-demand VM resources are raw (cpu/mem/disk on `Machine`)
  or stay abstract via `size: Magnitude`.
- **LOCATION** — NO field exists. New field needed. By the three-part
  proposal test (`ARCHITECTURE.md:18-44` / `INTENT.md:20-27`): if
  location is cluster-authored, variable, and non-derivable it belongs
  on `NodeProposal` or `Machine`; otherwise it is a horizon/CriomOS
  concern. For a VM whose physical placement is its `super_node` host,
  much of "location" may be *derivable* from the host rather than
  authored.
- **ON-DEMAND (launched to test, stopped after)** — closest existing
  knob is `online: Option<bool>` (`proposal.rs:78-86`), which already
  gates a node out of `nix.buildMachines` when administratively
  offline. An on-demand lifecycle state is either an extension of this
  or a new field; nothing models "stopped/ephemeral" today beyond
  online/offline and trust=Zero drop.
- **Domain/deploy integration is automatic**: any new node gets
  `<node>.<cluster>.criome` (`name.rs:106-109`) and flows through
  `project` (`horizon.rs:31-145`) like any other node, so lojix deploy
  and CriomOS config validation pick it up with no special path —
  exactly the "integrated like any node" goal.
