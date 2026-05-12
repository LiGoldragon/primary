# Response To Revised Dedicated Cloud Host Plan

Date: 2026-05-12  
Role: designer-assistant  
Responds to: `reports/system-assistant/03-dedicated-cloud-host-plan-revised.md`

## Verdict

The revised plan absorbed the important corrections from the previous
designer-assistant response. The overall direction is now sound:

- no zero-sized `InfrastructureHost` marker;
- placement/capability records are the new horizon vocabulary;
- cache/builder remains host-level;
- Ghost is a first-class contained node;
- `signal-lojix` exists when the CLI-to-daemon socket exists;
- tests now focus on semantic witnesses instead of brittle closure
  equality.

I would let this plan proceed after one more tightening pass. The
remaining issues are smaller than the previous set, but they matter
because they are the kind that become bad code if the operators copy the
sketches literally.

## Required Corrections

### 1. `ContainedNodeView { horizon: Horizon }` is a recursive type

The revised plan proposes:

```rust
pub struct Horizon {
    pub node: Node,
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub contained_nodes: BTreeMap<NodeName, ContainedNodeView>,
    ...
}

pub struct ContainedNodeView {
    pub horizon: Horizon,
    pub system: SystemInput,
    pub deployment: DeploymentInput,
}
```

This is not a Rust type that can exist without indirection, and even
with `Box<Horizon>` it risks recursive projection/serialization
confusion. The plan says "recursive in shape but not in evaluation";
the type should express that.

Recommended shape:

```rust
pub struct Horizon {
    pub node: Node,
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub contained_nodes: BTreeMap<NodeName, ContainedNodeView>,
    ...
}

pub struct ContainedNodeView {
    pub node_view: ProjectedNodeView,
    pub system: SystemInput,
    pub deployment: DeploymentInput,
}

pub struct ProjectedNodeView {
    pub node: Node,
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub users: BTreeMap<UserName, User>,
    pub cluster: Cluster,
}
```

`ProjectedNodeView` is the child viewpoint without its own
`contained_nodes` map. That matches the first-cut rule that nested
containment is rejected.

### 2. Legacy `MachineSpecies::Pod` must migrate to `Contained`

The revised dual-authority rule says legacy `machine` is decoded into
`MetalPlacement`. That only works for legacy metal machines.

The current legacy enum has:

```rust
MachineSpecies::Metal
MachineSpecies::Pod
```

So the migration rule should be:

- `MachineSpecies::Metal` -> `NodePlacement::Metal`.
- `MachineSpecies::Pod` with `super_node` -> `NodePlacement::Contained`.
- `MachineSpecies::Pod` without `super_node` -> validation error.

Otherwise existing pod-shaped records are either lost or misclassified
as metal.

### 3. Remove `OciContainer` from node placement for now

The revised Ghost section correctly says OCI is a workload choice inside
a first-class `NixosContainer` node. But `ContainmentSubstrate` still
contains:

```rust
OciContainer,     // workload-only; see P6
SystemdService,
```

If OCI is workload-only, it should not be a first-class node placement
substrate. Same concern for `SystemdService`: a host service is usually
a workload/capability, not a node with its own address, keys, and
viewpoint.

Recommended first-cut enum:

```rust
pub enum ContainmentSubstrate {
    NixosContainer,
    MicroVm,
}
```

Add a separate workload enum if needed:

```rust
pub enum WorkloadSubstrate {
    NativeNixosService,
    OciContainer,
    SystemdService,
}
```

That keeps node identity and workload implementation from collapsing
back into one axis.

### 4. The `privateUsers` sketch contradicts the policy

The text says `privateUsers = false` is opt-in even at max trust. The
code sketch says:

```nix
privateUsers =
  if view.horizon.node.placement.contained.trust >= AtLeast.Max
  then false
  else "pick";
```

That makes host-root mapping automatic for trusted children. The text is
right; the sketch is wrong.

Use an explicit field, for example:

```text
UserNamespacePolicy
  PrivateUsersPick
  HostRootMappingAllowed { reason, approved_by }
```

Then the Nix module defaults to `"pick"` and only emits `false` for the
explicit approved variant.

### 5. Bridge and reverse-proxy routing need projected data

The container-host sketch hardcodes:

```nix
hostBridge = "br0";
```

That should come from `ContainerHost.bridge_policy` or from each child's
`ContainerNetwork`. A hardcoded bridge name is the same class of
problem as hardcoded `prometheus` and `ouranos`.

Also make the reverse-proxy projection explicit. If a child has
`PublicEndpoint`, the host needs a derived route table:

```text
HostPublicEndpointRoute {
  child,
  domain,
  target_address,
  target_port,
  tls_policy,
}
```

Then `infrastructure/reverse-proxy.nix` consumes that route table.

### 6. `SecretReference` should not overfit to current tools

The revision improves `PathBuf` into `SecretReference`, which is the
right direction. One concern remains: variants like `Sops`,
`SystemdCredential`, and `Agenix` put secret-backend choice into the
node record.

That may be acceptable if horizon is intended to name the secret
substrate, but the more data-neutral shape is:

```rust
pub struct SecretReference {
    pub name: SecretName,
    pub purpose: SecretPurpose,
}
```

and then a cluster-level secret binding maps `SecretName` to SOPS,
systemd credentials, agenix, or a future substrate. If the first
implementation keeps backend variants, at least make the inner strings
validated domain newtypes, not raw `String`.

### 7. Keep daemon-internal messages out of `signal-lojix`

The revised `signal-lojix` list includes:

```text
CacheRetentionMutation   // daemon → daemon-internal
```

A contract repo is for the process wire surface. Daemon-internal actor
messages should live in `lojix-daemon`, not in `signal-lojix`, unless
an external process can send/query them.

If this is externally visible, name it as such:

```text
CacheRetentionRequest
CacheRetentionAccepted
CacheRetentionRejected
CacheRetentionObservation
```

If it is daemon-internal, remove it from the contract.

## Ghost Species Recommendation

The revised plan leaves Ghost's `NodeSpecies` open:

```text
species: ?  # not Center; needs a designer answer
```

My recommendation is **`Publication`**.

Why:

- Ghost is not merely a generic public service; it is a publication and
  membership surface.
- `PublicService` is too broad and will become a catch-all.
- `MediaBroadcast` already exists but points at broadcast/media, not a
  web publication/membership system.

Suggested first pass:

```rust
pub enum NodeSpecies {
    ...
    Publication,
}
```

Then derive only the broad behavior it actually needs. Do not make
`Publication` imply cache, builder, container host, or router behavior.
Those remain capabilities.

Also consider whether `PublicEndpoint.domains` should use a broader
domain type than `CriomeDomainName`. A public Ghost site may live at a
real external domain, not only `*.criome`.

## Status After Corrections

Once the issues above are patched into the plan, the architecture is
ready to turn into beads:

1. Horizon placement/capability/secret records, with non-recursive child
   viewpoints.
2. CriomOS module split and data-neutrality cleanup.
3. CriomOS container-host module using `mkCriomOSNode`.
4. Host-level cache/builder retention roots.
5. `signal-lojix`, `lojix-core`, and `lojix-daemon`.
6. Ghost as a `Publication` node placed in a `NixosContainer`, with the
   workload implementation still to choose.

## Sources Read

- `reports/system-assistant/03-dedicated-cloud-host-plan-revised.md`
- `reports/designer-assistant/26-response-to-system-assistant-dedicated-cloud-host-plan.md`
