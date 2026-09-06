# Horizon preservation map

This map is an inventory of the legacy Horizon producer, based on the direct
source at producer base `f8c5808466a47c2fd741cf0b119d73e8ba2add3d`.  It is the
schema and projection boundary for the Datom migration; no field in this map
may be omitted from the materialized `HorizonDefinition`.

## Root proposal

| Legacy source | Meaning | Datom location |
| --- | --- | --- |
| `ClusterProposal.nodes` (`lib/src/proposal.rs:28`) | Cluster-local named nodes | `ClusterDefinition.cluster_nodes: Vector<NodeDefinition>` |
| `ClusterProposal.users` | Cluster users | `ClusterDefinition.users: Vector<UserDefinition>` |
| `ClusterProposal.domains` | Named DNS-provider records | `ClusterDefinition.domains: Vector<DomainDefinition>` |
| `ClusterProposal.trust` | Cluster, cluster-name, node-name, and user-name trust floors | `ClusterDefinition.trust: ClusterTrust` with separate `ClusterTrustEntry`, `NodeTrustEntry`, and `UserTrustEntry` vectors |
| `ClusterProposal.domain_configuration` | Internal suffix and public cluster domains | `HorizonConfiguration.domain_configuration: DomainConfiguration` |

The external `HorizonConfiguration.generic_nodes` is a catalogue only.
`ClusterDefinition.generic_node_names` is the sole membership selection.  The
composer rejects an unknown selection, duplicate selection, duplicate
catalogue name, duplicate cluster-local name, or a selected/local name
collision before it writes `HorizonDefinition`.

## NodeDefinition

| Legacy source | Meaning and preserved behavior | Datom location |
| --- | --- | --- |
| `NodeProposal.species` (`proposal.rs:55`) | A legacy mixed profile enum. Its source-defined unions become independent capability/profile facts; it is not renamed into a new role enum. | `NodeDefinition.capabilities`: `Center`, `LargeAi`, `Router`, `Edge`, `NextGeneration`, `LowPower`, `TestVm`, `CloudNode` as applicable. `MediaBroadcast` and `RouterTesting` have no source consumer/projection behavior and are not compatibility fields. |
| `NodeProposal.size` | Capacity floor; combines with user size | `NodeDefinition.size: Magnitude` |
| `NodeProposal.trust` | Input to `min(node input, named node floor, cluster floor)`; Zero removes a node from projected membership | `NodeDefinition.trust: Magnitude` |
| `NodeProposal.machine` | Hardware and guest-host relationship, detailed below | `NodeDefinition.machine: MachineDefinition` |
| `NodeProposal.io.keyboard` | Keyboard remains available to both Live and Installation nodes | `NodeDefinition.environment.keyboard` |
| `NodeProposal.io.compressed_swap` | RAM-backed compressed swap remains available to both variants | `NodeDefinition.environment.compressed_swap` |
| `NodeProposal.io.bootloader` | Boot target setting | `NodeVariant.Installation.bootloader` |
| `NodeProposal.io.disks` | Persistent target, mount, filesystem and options | `NodeVariant.Installation.disks` only |
| `NodeProposal.io.swap_devices` | Persistent swap devices/sizes | `NodeVariant.Installation.swap_devices` only |
| `NodeProposal.pub_keys.ssh` | Node SSH public key | `NodeDefinition.keys.ssh` |
| `NodeProposal.pub_keys.nix` | Node Nix signing/build public key | `NodeDefinition.keys.nix` |
| `NodeProposal.pub_keys.yggdrasil` | Yggdrasil key, address and subnet | `NodeDefinition.keys.yggdrasil` |
| `NodeProposal.link_local_ips`, `node_ip`, `wireguard_pub_key` | Link-local addresses and main WireGuard identity | `NodeDefinition.network.link_local_ips`, `.node_ip`, `.wireguard_pub_key` |
| `NodeProposal.wireguard_untrusted_proxies` | VPN peer public key, endpoint and interface address | `NodeDefinition.network.wireguard_proxies` |
| `NodeProposal.router_interfaces` | WAN/WLAN names, band/channel/standard, WPA secret reference, backup AP facts | `NodeDefinition.network.router_interfaces` |
| `NodeProposal.online` | `None` means online; explicit false prevents remote-builder dispatch while retaining the node | `NodeDefinition.online: Option<Boolean>` |
| `nordvpn`, `wifi_cert`, `wants_printing`, `wants_hw_video_accel` | Explicit service opt-ins | `NodeDefinition.capabilities` variants `Nordvpn`, `WifiCertificate`, `Printing`, `HardwareVideo` |
| `NodeProposal.services` | Tailnet, Nix, Persona, VM-host, VM-testing, and Web-host service roles and settings | `NodeDefinition.capabilities` variants, preserving each payload |

`NodeVariant.Live` has no persistent disk/layout payload.  It is used by the
generic installer definitions.  `NodeVariant.Installation` is required for a
node that carries boot/disk/swap configuration.  This split does not remove
keyboard, compressed swap, network, keys, role, trust, or capabilities from
Live.

## MachineDefinition

| Legacy `Machine` field (`lib/src/machine.rs:15`) | Datom location |
| --- | --- |
| `species = Metal`, `arch` | `MachineDefinition.Metal.{ architecture, hardware }`; architecture is required |
| `species = Pod` | `MachineDefinition.VirtualMachine.{ host_choice, hardware, disk_gib }`; the host choice carries an explicit or inherited architecture |
| `cores` | `Hardware.cores` |
| `model` | `Hardware.model` |
| `mother_board` | `Hardware.motherboard` |
| `chip_gen` | `Hardware.chip_generation` |
| `ram_gb` | `Hardware.ram_gib` |
| `location` | `Hardware.location` |
| `super_node` | `VirtualMachineHost.Cluster.primary_host` |
| `super_nodes` | `VirtualMachineHost.Cluster.additional_hosts` |
| `super_user` | `VirtualMachineHost.Cluster.user` |
| `disk_gb` | `VirtualMachine.disk_gib` |

`MachineSpecies::Pod` is a VM guest, not a container: source comments call it
“Pod (VM)”, require a host set, derive the guest architecture from host(s),
and use `disk_gb` for the VM root disk (`machine.rs:8-13, 47-80`).  Its Datom
name is therefore `VirtualMachine`; the approved schema has no `Container`
variant.

`VirtualMachineHost` distinguishes `Cluster.{ primary_host, additional_hosts,
user, architecture_override }`, whose hosts are validated and used for local
image exchange, from `External.{ provider_or_location, architecture }`.
Cluster architecture may be omitted and is then inherited after validating all
declared hosts share it. Metal and External architectures are required. External
is an explicit non-empty authored provider/location reference such as
`digitalocean-fra1`; it is never inferred from a node name or a profile
capability. An external VM remains
`VirtualMachine`, not `Metal`.

## Capabilities and dependent settings

| Legacy value | Datom form |
| --- | --- |
| `TailnetClient`, `TailnetController`, `NixCache` | payload-free `NodeCapability` variants |
| `NixBuilder.maximum_jobs` | `NodeCapability.NixBuilder.Option<Integer>` |
| `PersonaDevelopment.capabilities` / `GitoliteServer` | `NodeCapability.PersonaDevelopment.Vector<PersonaCapability>` |
| `VmHost.guest_subnet`, `kvm`, `maximum_guests` | `NodeCapability.VmHost.{ TapSubnet KvmAvailability Option<Integer> }`; `KvmAvailability` remains `Available` or `Absent`, never an untyped Boolean |
| `VmTesting.gpu_passthrough`, `display`, `gpu` | `NodeCapability.VmTesting.{ Boolean Text Option<Text> }`; it enables the persistent VM-testing host and remains distinct from the payload-free `TestVm` guest capability |
| `WebHost.sites` | `NodeCapability.WebHost.Vector<HostedSite>`; site has domain, pinned source and renderer |
| `RouterInterfaces` | Typed `RouterInterfaces` and `BackupWireless`; secret references remain references, never decrypted content |

## Users, domains and trust

| Legacy value | Datom form |
| --- | --- |
| `UserProposal.species`, `size`, `keyboard`, `style` | `UserDefinition.role`, `.size`, `.keyboard`, `.style` |
| `github_id`, `fast_repeat`, `editor`, `text_size` | corresponding typed optional fields on `UserDefinition` |
| `pub_keys[node].ssh`, `.keygrip` | `UserDefinition.public_keys: Vector<UserPubKey>` |
| `DomainProposal.species` | `DomainDefinition.provider: DomainProvider` |
| trust cluster floor/maps | named entry vectors in `ClusterTrust` rather than untyped parallel vectors |
| domain internal suffix/public domains | `DomainConfiguration.{ internal_suffix, public_cluster_domains }` |

## Projection obligations

The new projection has to retain the old consumer-facing behavior:

1. resolve selected generic nodes before projection; catalogue presence alone
   is not membership;
2. apply trust floors and exclude a node or user at `Zero`;
3. validate one Tailnet controller among trusted nodes;
4. resolve a VM guest architecture and validate every declared host exists and
   shares it;
5. expose service payloads, router/proxy data, node keys, domain configuration,
   users, domains, and trust to the selected node projection;
6. derive domain names, user identity/defaults, Nix builder/cache data, admin
   keys, and VM image-exchange host keys from those retained facts.

The first implementation test must round-trip a document containing each
non-empty payload above, then project both graphical and minimal selected Live
installers and an Installation node.  Negative tests cover unknown and
duplicate generic selection, duplicate names, collisions, and invalid VM host
references.

## Legacy profile decomposition

`NodeSpecies` must not be carried forward as a renamed role field. The legacy
projection itself calls it a mixed profile enum (`lib/src/node.rs:182-212`) and
derives these facts: `LargeAi` gives `LargeAi + Center`; `LargeAiRouter` adds
`Router`; `Hybrid` gives `Router + Edge + NextGeneration`; `Edge` gives
`Edge + LowPower`; and `EdgeTesting` gives `Edge + LowPower + NextGeneration`.
`Center`, `Router`, `TestVm`, and `CloudNode` become their directly named
profile capabilities. `MediaBroadcast` and `RouterTesting` have no source
consumer behavior beyond legacy enum identity, so they are not carried as
compatibility data. Machine kind independently produces bare-metal or
virtual-machine behavior, and node variant remains exactly Live or
Installation; ISO behavior is derived at projection time.
