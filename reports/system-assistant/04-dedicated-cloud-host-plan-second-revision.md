# 04 — Dedicated cloud host: second revision

Date: 2026-05-12
Role: system-assistant
Supersedes: `reports/system-assistant/03-dedicated-cloud-host-plan-revised.md`
Responds to: `reports/designer-assistant/27-response-to-revised-dedicated-cloud-host-plan.md`
Earlier rounds: `reports/system-assistant/02-...`,
                `reports/designer-assistant/26-response-...`,
                `reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`

## Frame

The designer-assistant accepted plan 03's direction and surfaced
seven more corrections plus a Ghost species recommendation. All
seven land here, plus the Ghost species choice and a follow-on
domain-type widening. The phase order, dependency graph, and
sequencing notes from plan 03 carry over unchanged.

This report is incremental. For sections not touched here, plan 03
is still the source of truth.

## What changed since plan 03

| Plan 03 § | Change | Driving correction |
|---|---|---|
| P3.2 | `ContainedNodeView` no longer holds a `Horizon` recursively. New flat `ProjectedNodeView` type omits `contained_nodes` — the absence of the field is the type expressing "no nested containment". | C1 |
| P1.2 | Legacy `MachineSpecies::Pod` decode path added. `Pod + super_node → Contained { substrate: NixosContainer }`; `Pod` without `super_node` is a validation error. | C2 |
| P1.2 | `ContainmentSubstrate` shrunk to `NixosContainer | MicroVm`. New `WorkloadSubstrate { NativeNixosService, OciContainer, SystemdService }` separates "what runs inside" from "how the node exists". | C3 |
| P3.3 | `privateUsers` sketch fixed. New `UserNamespacePolicy` enum makes host-root mapping explicit and opt-in by data variant, not by trust comparison. | C4 |
| P3.3, new P5.7 | `hostBridge` no longer hardcoded; comes from `ContainerHost.bridge_policy`. New derived `HostPublicEndpointRoute` projection feeds the reverse-proxy module. | C5 |
| P1.1 | `SecretReference` reshaped to `{ name: SecretName, purpose: SecretPurpose }`. Backend choice (sops/agenix/credential) moves to a cluster-level binding. | C6 |
| P5.4 | `CacheRetentionMutation` removed from `signal-lojix`. Externally-visible operations renamed `CacheRetentionRequest/Accepted/Rejected/Observation`; daemon-internal messages stay in `lojix-daemon`. | C7 |
| P6.1, P1.1 | Ghost gets `NodeSpecies::Publication`. `PublicEndpoint.domains` widens to a new `PublicDomain` enum (internal `*.criome` or external FQDN). | Designer §"Ghost Species Recommendation" |

---

## Revised P1 — types corrected

### P1.1 (revised) — `ContainmentSubstrate` is identity, `WorkloadSubstrate` is implementation

```rust
// horizon-rs/lib/src/placement.rs

pub enum ContainmentSubstrate {
    NixosContainer,   // declarative `containers.<name>` via systemd-nspawn
    MicroVm,          // microvm.nix
    // OciContainer and SystemdService are NOT here — they are workload
    // implementations, not node-identity substrates. See WorkloadSubstrate.
}

// horizon-rs/lib/src/workload.rs (new)
pub enum WorkloadSubstrate {
    NativeNixosService,
    OciContainer,
    SystemdService,
}
```

The type carves the architectural rule: a node has identity iff it
has its own address, keys, and lifecycle. That requires a real
isolation substrate (`NixosContainer` or `MicroVm`). Workload choice
sits inside the node, on a different axis.

A node with `placement: Metal` runs workloads directly on the host —
no `WorkloadSubstrate` field needed at the node level; per-service
workload choice is a service-module concern.

### P1.1 (revised) — `SecretReference` is a logical name, not a backend

```rust
// horizon-rs/lib/src/secret.rs
pub struct SecretReference {
    pub name: SecretName,
    pub purpose: SecretPurpose,
}

pub struct SecretName(String);  // newtype with validation
pub enum SecretPurpose {
    BinaryCacheSigning,
    WireguardPrivateKey,
    NordvpnCredentials,
    GhostMailerPassword,
    GhostStripeKey,
    // … one variant per documented secret-bearing role.
    // Open list, but each variant is a typed declaration, not a string.
}
```

The cluster-level binding (which backend stores which secret) lives
on `Cluster`, not on individual nodes:

```rust
// horizon-rs/lib/src/cluster.rs (extension)
pub struct ClusterSecretBinding {
    pub name: SecretName,
    pub backend: SecretBackend,
}

pub enum SecretBackend {
    Sops { file: SopsFilePath, key: SopsKeyPath },
    SystemdCredential { credential_name: String },
    Agenix { secret_id: String },
}
```

`SecretName` newtype carries validation (non-empty,
ASCII-letters-digits-dashes only). `SopsFilePath` and similar are
typed paths — never raw `PathBuf`. CriomOS modules read both the
node's `SecretReference` and the cluster's binding to render a
runtime path; nodes never see backend choice.

### P1.1 (revised) — `BinaryCacheEndpoint` and `PublicDomain`

```rust
pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,
    pub signing_key: SecretReference,    // BinaryCacheSigning
    pub retention_policy: CacheRetentionPolicy,
}

pub struct BinaryCacheEndpoint {
    pub scheme: CacheScheme,
    pub host: PublicDomain,              // was CriomeDomainName
    pub port: u16,
    pub path_prefix: Option<String>,
    pub public_key: NixPubKey,
}

pub enum PublicDomain {
    Criome(CriomeDomainName),            // *.criome internal
    External(ExternalDomainName),        // e.g. blog.example.com
}

pub struct ExternalDomainName(String);   // newtype with hostname validation
```

`PublicEndpoint.domains: Vec<PublicDomain>` for the same reason —
Ghost lives at a real external domain.

### P1.2 (revised) — `MachineSpecies::Pod` migration

The dual-authority rule from plan 03 §1.2 stands; the legacy decode
table extends to cover Pod records:

| Legacy input | Migration |
|---|---|
| `MachineSpecies::Metal` | `NodePlacement::Metal { from machine fields }` |
| `MachineSpecies::Pod` + `super_node: Some(host)` | `NodePlacement::Contained { host, substrate: NixosContainer, trust: parent.trust, resources: from cores+ram_gb, network: default-bridge, state: empty }` |
| `MachineSpecies::Pod` + `super_node: None` | `Error::PodWithoutHost { node: NodeName }` (this was already malformed; now it fails fast) |

The default substrate `NixosContainer` matches what Pod meant
operationally in current code (`BehavesAs::virtual_machine` derives
from it; existing pod nodes are NixOS containers). The
`super_user: Option<UserName>` field migrates onto
`ContainedPlacement` as documented in plan 03 §1.2.

### P1.4 (revised) — `Horizon` and the recursion fix

```rust
// horizon-rs/lib/src/horizon.rs

pub struct Horizon {
    pub node: Node,
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub contained_nodes: BTreeMap<NodeName, ContainedNodeView>,
    pub users: BTreeMap<UserName, User>,
    pub cluster: Cluster,
}

// One level deep. No `contained_nodes` field — that is the type
// stating "the first cut rejects nested containment".
pub struct ProjectedNodeView {
    pub node: Node,
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub users: BTreeMap<UserName, User>,
    pub cluster: Cluster,
}

pub struct ContainedNodeView {
    pub node_view: ProjectedNodeView,
    pub system: SystemInput,
    pub deployment: DeploymentInput,
}
```

This both removes the `Box`-or-stack-overflow type problem and
documents the architectural constraint at the type level. When
nested containment is admitted later, `ProjectedNodeView` grows a
`contained_nodes` field — at that point the projector either
recurses or stops at depth N, and the type changes force every
consumer to acknowledge it.

### P1.5 — derived projections (new section)

These derived records are projected once for the host's viewpoint
so consumers don't re-walk:

```rust
// On Horizon (host viewpoint), derived after children project:
pub struct HostPublicEndpointRoute {
    pub child: NodeName,
    pub domain: PublicDomain,
    pub target_address: ContainerLocalAddress,
    pub target_port: u16,
    pub tls_policy: TlsPolicy,
}

// Horizon { ..., public_endpoint_routes: Vec<HostPublicEndpointRoute> }
```

Population rule: for each `containedNodes[child]` with
`view.node_view.node.capabilities.public_endpoint = Some(pe)`, emit
one `HostPublicEndpointRoute` per `(domain, port)` pair from `pe`.
This is what `infrastructure/reverse-proxy.nix` consumes; the
module never reaches into individual child views to discover
routes.

---

## Revised P3 — container-host module sketch corrected

### P3.3 (revised) — bridge from data, user-namespace policy from data

```nix
{ config, lib, horizon, inputs, flake, ... }:
let
  inherit (horizon.node.capabilities) containerHost;
  mkCriomOSNode = import ../../lib/mkCriomOSNode.nix { inherit flake inputs; };

  # `bridgePolicy` is data, not a literal. Single named bridge today;
  # capability schema can grow per-child or per-substrate later.
  inherit (containerHost.bridgePolicy) bridgeName;

  privateUsersOf = childPlacement:
    let policy = childPlacement.contained.userNamespacePolicy; in
    if policy.kind == "PrivateUsersPick" then "pick"
    else if policy.kind == "HostRootMappingAllowed" then false
    else throw "unknown UserNamespacePolicy: ${policy.kind}";

in {
  config = lib.mkIf (containerHost != null) {
    containers = lib.mapAttrs (childName: view: {
      autoStart    = true;
      privateNetwork = true;
      hostBridge   = bridgeName;
      localAddress = view.deployment.localAddress;
      hostAddress  = view.deployment.hostAddress;
      privateUsers = privateUsersOf view.node_view.node.placement;
      config       = mkCriomOSNode {
        inherit (view) system deployment;
        horizon = view.node_view;
      };
    }) horizon.containedNodes;
  };
}
```

Where the policy type is:

```rust
// horizon-rs/lib/src/placement.rs
pub struct ContainedPlacement {
    pub host: NodeName,
    pub substrate: ContainmentSubstrate,
    pub resources: ContainerResources,
    pub network: ContainerNetwork,
    pub state: ContainerState,
    pub trust: AtLeast,
    pub user_namespace_policy: UserNamespacePolicy,   // NEW
}

pub enum UserNamespacePolicy {
    PrivateUsersPick,
    HostRootMappingAllowed {
        reason: String,
        approved_by: UserName,
    },
}
```

The default in proposals is `PrivateUsersPick`. A child that wants
host-root mapping must declare it explicitly, name a reason, and
name an approver. The Nix module emits `false` only for that
explicit variant. Trust level is no longer the gate — the type is.

### P3.5 (revised) — bridge and routes are projected

The host's bridge name comes from `ContainerHost.bridge_policy`
(named string today; structured policy when needed). The host's
reverse-proxy module reads `horizon.publicEndpointRoutes` (per P1.5
above) and emits per-route nginx/caddy entries. No string scanning
of children.

---

## Revised P5 — contract scope tightened

### P5.4 (revised) — `signal-lojix` carries only the wire surface

The contract crate is the wire boundary. Daemon-internal actor
messages stay inside `lojix-daemon` and are not exported.

Externally-visible operations on cache retention follow the
standard Submission/Accepted/Rejected/Observation pattern, same as
deployment:

```text
signal-lojix
  // deployment surface
  DeploymentSubmission
  DeploymentAccepted
  DeploymentRejected
  DeploymentObservation

  // cache retention surface (operator-visible, e.g. pin/unpin)
  CacheRetentionRequest      // operator → daemon: "pin generation X" / "retire Y"
  CacheRetentionAccepted     // daemon → operator: ack with mutation id
  CacheRetentionRejected     // daemon → operator: typed error
  CacheRetentionObservation  // daemon → observers: live-set changes

  // queries
  GenerationQuery
  GenerationListing
```

Internal-only messages (between `LiveSetActor` and `GcRootActor`,
say, or the systemd-dbus container observer feeding the event log)
are `lojix-daemon`-private types.

Test for the boundary: every type in `signal-lojix` must be reachable
from at least one socket handler in `lojix-cli` or `lojix-daemon`.
A type with no consumer outside the daemon is mis-located.

---

## Revised P6 — Ghost is `NodeSpecies::Publication`

### P6.1 (revised) — Ghost node shape

```text
node ghost
  species: Publication       # NEW variant — see §6.4 below
  size: medium
  trust: medium
  placement: Contained {
    host: hyacinth
    substrate: NixosContainer
    resources: { cores: 2, ram_gb: 2 }
    network: { localAddress: 10.42.0.10, hostAddress: 10.42.0.1 }
    state: { persistent_paths: [ "/var/lib/ghost", "/var/lib/mysql" ] }
    trust: Medium
    user_namespace_policy: PrivateUsersPick
  }
  capabilities: {
    public_endpoint: Some(PublicEndpoint {
      domains: [
        PublicDomain::External(ExternalDomainName("blog.example.com")),
        PublicDomain::Criome(CriomeDomainName::for_subdomain("ghost", cluster)),
      ],
      tls_policy: AcmeLetsEncrypt,
      reverse_proxy_policy: HostTerminates,
    }),
  }
```

The `public_endpoint.domains` list now mixes external and internal
domains via `PublicDomain`. The reverse-proxy projection
(P1.5 / P5.7) emits one route per `(domain, port)`.

### P6.4 — `NodeSpecies::Publication` (new section)

Add the variant to `horizon-rs/lib/src/species.rs`:

```rust
pub enum NodeSpecies {
    Center,
    LargeAi,
    LargeAiRouter,
    Hybrid,
    Edge,
    EdgeTesting,
    MediaBroadcast,
    Router,
    RouterTesting,
    Publication,   // NEW
}
```

`Publication` is narrow on purpose: it covers
publication/membership web surfaces (Ghost, future replacements).
It does **not** imply `cache`, `builder`, `container_host`, or
`router` behavior — those remain on `NodeCapabilities`.

Behavior derivations:

- `BehavesAs::publication = matches!(species, Publication)` — new
  flag for modules that need to gate on publication shape.
- Does not contribute to `behaves_as.center`,
  `behaves_as.large_ai`, etc.

Ghost is the first `Publication` node. The next is whatever
membership/CMS surface follows. If a non-Ghost candidate has
significantly different shape (e.g. a wiki or a static-site
generator), that is the moment to evaluate splitting `Publication`
into finer variants — not in the first cut.

---

## Decisions still owed

Smaller list than after plan 03:

| Question | Owner | Blocks |
|---|---|---|
| Ghost workload — native NixOS service vs OCI container inside the `NixosContainer` node | designer | P6 implementation start |

That is the only remaining question. The Ghost species (Q6 from
plan 03) is now resolved as `Publication`.

## Status after corrections

The architecture is bead-ready. Tracking beads to file (mirrors
plan 03 §"Coordination notes" with one addition):

1. `horizon-rs`: typed placement (with Pod migration), capability,
   secret records, non-recursive child viewpoints, `Publication`
   species, `PublicDomain` type, dual-authority validation.
2. CriomOS: split `nix.nix`; remove three node-name gates; add
   `infrastructure/{container-host,reverse-proxy}.nix` consuming
   `ContainerHost.bridge_policy` and
   `horizon.publicEndpointRoutes`.
3. CriomOS: `lib/mkCriomOSNode.nix` + container-host module
   emitting `containers.<name>` per child; `UserNamespacePolicy`
   enforced.
4. lojix: cache GC-root agent (bootstrap script).
5. After bead `primary-q3y` (kameo migration): `signal-lojix`
   contract crate (Submission/Accepted/Rejected/Observation
   pattern, no daemon-internal types), `lojix-core` extraction,
   `lojix-daemon` skeleton.
6. Ghost as `Publication` node placed in `NixosContainer`;
   workload choice owed.

## Sources

- Designer-assistant response (this round):
  `reports/designer-assistant/27-response-to-revised-dedicated-cloud-host-plan.md`
- Previous round response:
  `reports/designer-assistant/26-response-to-system-assistant-dedicated-cloud-host-plan.md`
- Original architecture:
  `reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`
- Superseded plans:
  `reports/system-assistant/02-...`,
  `reports/system-assistant/03-...`
- Skills consulted: `skills/contract-repo.md`, `skills/abstractions.md`,
  `skills/naming.md`.
