# 111 - Horizon/Lojix Context Maintenance

Date: 2026-05-17  
Role: designer-assistant

## What This Replaces

This report supersedes and deletes the recent designer-assistant Horizon
working reports:

- `106-horizon-constant-cluster-data-boundary-critique.md`
- `107-lean-horizon-implementation-audit-2026-05-17.md`
- `108-sys134-lean-horizon-audit-synthesis-2026-05-17.md`
- `109-lean-horizon-forward-guidance-after-user-decisions-2026-05-17.md`
- `110-ideal-cluster-schema-visualization-2026-05-17.md`

Those five reports accumulated roughly 1,900 lines. The load-bearing
substance is below in condensed form.

## Current State

System-specialist report 134 says the `horizon-leaner-shape` branch
stack now builds a real `zeus` CriomOS system target through the new
`lojix` daemon path. I did not rerun the expensive build smoke, but code
inspection supports the architectural claim: `lojix` loads a cluster
proposal, loads pan-horizon config, projects Horizon, stages inputs, and
builds via Nix.

The core implementation move is correct:

- `goldragon/datom.nota` is leaner.
- `criomos-horizon-config/horizon.nota` exists as a pan-horizon input.
- `horizon-rs` code has the correct two-input projection:
  `ClusterProposal::project(&HorizonProposal, &Viewpoint)`.
- AI/VPN catalogs moved out of cluster data into CriomOS-owned catalog
  space.

## Source Taxonomy

The durable taxonomy:

```text
Cluster proposal
  Authored facts about this cluster:
  nodes, users, trust, placement, machine facts, secret references,
  provider selections, explicit overrides.

Pan-horizon config
  Authored facts about this horizon/federation:
  domain suffixes, temporary IPv4 LAN constant, future horizon-wide
  deploy/network policy that is not per-cluster.

Horizon projection
  Reducer output:
  view-specific node maps, derived identities, role/capability booleans,
  builder/cache visibility, projected names consumed by downstream code.

CriomOS / CriomOS-home
  OS and home implementation:
  service rendering, provider catalogs, runtime defaults, resolver
  defaults, AI serving implementation, VPN server catalogs.

lojix
  Deploy orchestrator:
  reads typed configuration, reads pan-horizon config + cluster proposal,
  asks horizon-rs for the projected view, stages inputs, builds/deploys.
```

Rule:

> Outside cluster data does not automatically mean inside Horizon. Some
> facts belong in pan-horizon config; some belong in CriomOS catalogs;
> some are simple CriomOS rendering logic; some are projection outputs.

## Settled Decisions

### 1. `lojix-daemon` must receive the pan-horizon config path in typed config

`lojix` is what calls Horizon during deployment. Someone hosting their
own meta-cluster must be able to supply their own pan-horizon config and
domain suffixes.

Current gap: `lojix` still has a hardcoded default path for the
pan-horizon source in runtime construction. Tests can override it, but
the daemon's typed startup contract does not carry it.

Implementation target:

```rust
pub struct LojixDaemonConfiguration {
    pub daemon_socket_path: WirePath,
    pub daemon_socket_mode: SocketMode,
    pub daemon_socket_group: Option<UnixGroup>,
    pub state_directory: WirePath,
    pub gc_root_directory: WirePath,
    pub horizon_configuration_source: WirePath,
    pub peer_daemons: Vec<PeerDaemonBinding>,
    pub operator_identity: OperatorIdentity,
    pub owned_cluster: ClusterName,
}
```

Then pass `horizon_configuration_source` into
`RuntimeConfiguration::from_daemon_configuration`.

### 2. Projected-only records move out of `proposal::*`

If the cluster author never writes it, it does not belong under
`proposal::*`.

Move or split:

- `LanNetwork`
- `LanCidr`
- `DhcpPool`
- `ResolverPolicy`
- `Ssid`

Likely destinations:

- `view::*` for projected output-only types;
- neutral `network` or `name` module if the type is shared between
  projection helper code and output records.

### 3. Reserved service labels are not user configuration

Predictability is the goal. The Git service is `git.<domain>`. Tailnet
is `tailnet.<domain>`. This does not need to be bikeshedded in
pan-horizon config.

Guidance:

- Remove `reserved_subdomains` from `HorizonProposal` unless a concrete
  behavior needs it.
- Do not inflate Horizon with configurable service-label policy.
- Let CriomOS service modules render canonical labels where the label is
  an implementation convention.

### 4. Horizon should stay a reducer, not become a string-concat library

Some of the recent cleanup overcorrected from "not cluster data" into
"put all derivation code in Horizon." That is not the desired shape.

Horizon should derive values that multiple downstream consumers need or
that genuinely require combining pan-horizon config, cluster facts, and
viewpoint. CriomOS may still contain small service rendering logic.

## LAN Decision

Do not pursue the hash-allocated IPv4 LAN design for v1.

Current decision:

- Keep a single transitional IPv4 LAN constant in Horizon/pan-horizon
  config.
- Add a loud warning in code and architecture:
  "single-router IPv4 LAN; replace with IPv6-first network later."
- Do not build a multi-cluster IPv4 allocator now.
- Do not hardcode IP addresses in CriomOS.

Suggested shape:

```nota
(TransitionalIpv4Lan
  "10.18.0.0/24"
  "10.18.0.1"
  (DhcpPool "10.18.0.100" "10.18.0.240")
  "TEMPORARY: single-router IPv4 LAN until IPv6-first network lands")
```

The exact type name can change. The point is explicit temporary data,
not hidden Rust constants and not hash allocation.

## Future IPv6 Network Direction

The long-term target is IPv6-first internal networking with IPv4
Internet compatibility at the router/gateway layer.

Research summary:

- **Jool** is the best first Linux candidate. It supports stateful NAT64
  and SIIT, documents RFC compliance, and has tutorials for stateful
  NAT64 and 464XLAT.
- **Stateful NAT64 + DNS64** is the practical first shape for IPv6-only
  clients reaching IPv4 servers by name.
- **464XLAT** becomes relevant when software uses IPv4 literals or
  IPv4-only APIs.
- **TAYGA** is stateless NAT64 through TUN. It is simpler, but its
  stateless model wants one-to-one IPv4/IPv6 mapping unless paired with
  stateful NAT44, so it is not the preferred featureful router target.

Sources used:

- Jool introduction and RFC compliance:
  https://www.jool.mx/en/intro-jool.html
- Jool stateful NAT64 tutorial:
  https://www.jool.mx/en/run-nat64.html
- Jool 464XLAT explanation:
  https://nicmx.github.io/Jool/en/464xlat.html
- RFC 8683 NAT64/464XLAT deployment guidance:
  https://www.ietf.org/rfc/rfc8683.html
- TAYGA manpage:
  https://manpages.ubuntu.com/manpages/jammy/man8/tayga.8.html

Future identity/address idea:

- Long-term IPv6 identity should probably derive from cryptographic
  identity, eventually Criome/BLS.
- Root SSH public key could be an interim experiment, but that makes
  host-key rotation into network renumbering and should be marked
  temporary.
- Relevant prior art: RFC 4193 ULA pseudo-random global IDs and
  Yggdrasil's public-key-derived IPv6 addresses.

Sources:

- RFC 4193:
  https://www.rfc-editor.org/rfc/rfc4193.html
- Yggdrasil implementation notes:
  https://yggdrasil-network.github.io/implementation.html

## Ideal Cluster Schema Direction

The cluster proposal should move toward:

```text
ClusterProposal
  nodes
  users
  trust
  secretBindings
  providerSelections

NodeProposal
  name
  species              # primary noun
  roles/capabilities   # additive responsibilities
  placement
  trust
  machine/io facts
  public keys
  secret references
  explicit overrides
```

Important point: `Router` and `LargeAi` are additive roles, not mutually
exclusive species. Prometheus can be:

```nota
(Node prometheus
  species Edge
  roles [Router LargeAi NixBuilder]
  placement Metal
  ...)
```

Possible first `NodeRole` enum:

- `Router`
- `LargeAi`
- `NixBuilder`
- `NixCache`
- `TailnetController`
- `ServiceHost`

Open design question: exact closed `NodeRole` and `NodeOverride` enums
need a focused schema report before implementation.

## AI Model Materialization

User decision: model files can live in the Nix store. Reproducibility
matters.

The problem is not the store. The problem is realizing huge GGUF
payloads on the wrong node or dragging them across Wi-Fi/LAN during an
ordinary system build.

Guidance:

- Keep model artifacts reproducible.
- Investigate a canonical Hugging Face download/fetcher path.
- Build or realize large model artifacts on or near the large-AI/cache
  host.
- Do not treat the current `prometheus` GGUF issue as a reason to undo
  the data-boundary cleanup.

## Immediate Implementation Targets

1. Refresh `horizon-rs/ARCHITECTURE.md` so it describes three projection
   inputs: `HorizonProposal`, `ClusterProposal`, and `Viewpoint`.
2. Add `horizon_configuration_source` to `signal-lojix::LojixDaemonConfiguration`
   and plumb it through `lojix-daemon`.
3. Replace the IPv4 LAN hash allocator with an explicit transitional
   IPv4 LAN record/constant and warning.
4. Remove `reserved_subdomains` unless a real consumer appears.
5. Move projected-only records out of `proposal::*`.
6. Create a focused ideal-cluster-schema report with before/after NOTA
   for `prometheus`, `zeus`, and one contained node.
7. Create a later IPv6-first network design around Jool, DNS64, optional
   464XLAT, and cryptographic identity-derived IPv6 addressing.

## Context Notes

note: use `lojix`, not `logix`.

note: current work is on feature worktrees under
`~/wt/github.com/LiGoldragon/<repo>/horizon-leaner-shape/` or related
branch names. Production checkouts under `/git/...` should stay stable.

note: the deleted intermediate audits contained line-specific evidence.
If exact file/line archaeology is needed, use git history. This report
preserves the current decisions, not every proof trail.

