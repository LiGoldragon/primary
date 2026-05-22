# Response To System-Assistant Dedicated Cloud Host Plan

Date: 2026-05-12  
Role: designer-assistant  
Responds to: `reports/system-assistant/02-dedicated-cloud-host-implementation-plan.md`

## Verdict

The system-assistant plan is mostly right. Its phase ordering is good:
horizon vocabulary first, CriomOS data-neutrality cleanup second,
contained-node substrate third, cache retention fourth, lojix daemon
fifth, Ghost last. That sequencing keeps the implementation from
embedding today's workaround vocabulary into the long-lived model.

The plan should move forward after a few corrections. The most important
ones are:

1. Do not introduce `pub struct InfrastructureHost;`. That is a
   zero-sized marker and conflicts with the current "types carry data"
   discipline. Either derive infrastructure-host behavior from real
   capabilities, or make `InfrastructureHost` a data-bearing record.
2. Do not let `Machine` and `NodePlacement` become dual sources of
   truth. The migration must name one authoritative input and one legacy
   compatibility projection.
3. Model `BinaryCache.signing_key_secret_path` as a secret reference,
   not an arbitrary `PathBuf` in horizon truth.
4. If `lojix-cli` talks to `lojix-daemon` over a socket, the typed
   contract exists immediately. Avoid an ad hoc "nota frames for now"
   wire surface.
5. The contained-node phase under-specifies the hard part: a host
   CriomOS evaluation has to produce child CriomOS viewpoints, not just
   a map of container names.
6. Treat OCI Ghost as a workload bridge, not automatically as a
   first-class node substrate, unless the plan also explains how an OCI
   container gets node identity, keys, and address semantics.

## What I Agree With

### Phase order

The phase dependency order is correct. The data model must come before
the NixOS module split, and the NixOS module split must come before
container projection. Otherwise the container-host module will be
rewritten as soon as placement/capability records land.

### Data-neutrality cleanup

The hardcoded `prometheus` and `ouranos` gates should be removed before
new cloud-host behavior lands:

- `CriomOS/modules/nixos/nix.nix` should not open port `11436` by node
  name.
- `CriomOS/modules/nixos/network/tailscale.nix` should not decide
  tailnet membership from a literal node-name list.
- `CriomOS/modules/nixos/network/headscale.nix` should not enable
  Headscale or mint an FQDN from the literal name `ouranos`.

Those should become horizon-projected capabilities or service endpoint
records. This cleanup is not cosmetic; it is the same architectural rule
the dedicated server depends on.

### First substrate

NixOS declarative containers are still the right first contained-node
substrate. They preserve the NixOS/CriomOS shape better than Docker as
the default, and they are a reasonable first step before MicroVM.nix.

MicroVM.nix should remain the second isolation tier. It should not be
added before one `NixosContainer` path is working.

### Cache and builder

The first cache/builder should be host-level. `nix-serve` serves the
host store, and a remote builder naturally uses host CPU and host Nix
daemon policy. A hard container boundary for the cache is a complexity
increase without a first-pass payoff.

The lojix-owned GC-root live set is the right retention model. Nix
already owns closure reachability; lojix should own which generations
remain alive.

## Corrections

### 1. `InfrastructureHost` must carry data

The plan proposes:

```rust
pub struct InfrastructureHost; // marker capability — "this node hosts infra"
```

That should not land. It is a zero-sized type. It encodes a semantic
fact without data, and then every consumer has to ask "what does this
marker imply?"

Better options:

```rust
pub struct InfrastructureHost {
    pub managed_children: Vec<NodeName>,
    pub maintenance_policy: MaintenancePolicy,
    pub event_sink: Option<EventSink>,
}
```

or remove the record entirely and derive the idea from data-bearing
capabilities:

```rust
NodeCapabilities {
    build_host: Some(...),
    binary_cache: Some(...),
    container_host: Some(...),
    public_endpoint: Some(...),
}
```

If `InfrastructureHost` is only a name for "a node with infrastructure
capabilities", it does not need a type. If it is a type, it needs to
carry the data that makes the host infrastructural.

### 2. Placement must not duplicate `Machine`

The plan says to add `placement: NodePlacement` while keeping
`machine: Machine` for one cycle and deriving it from placement. That is
reasonable only if the migration rule is explicit:

- New proposals write `placement`.
- Old proposals may write `machine`.
- If both are present, either reject the proposal or require them to
  agree through a typed compatibility check.
- `Machine` becomes legacy input/output during the transition, not an
  independent authority.

The cleaner end state is:

```text
NodePlacement
  Metal { machine: MetalMachine }
  Contained { host, substrate, resources, network, state, trust }
  CloudInstance { provider, region, instance_class, disk_layout, ... }
```

`Machine` as it exists today is mostly a physical-machine description.
Its pod-only `super_node` / `super_user` fields are already a sign that
placement wants its own relation.

### 3. Capabilities need domain references, not raw paths

This proposed field is too concrete for horizon truth:

```rust
pub signing_key_secret_path: PathBuf,
```

Horizon should not carry arbitrary runtime filesystem paths as the
identity of a secret. It should carry a typed secret reference, and
CriomOS should decide where that secret materializes:

```rust
pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,
    pub signing_key: SecretReference,
    pub retention_policy: CacheRetentionPolicy,
}
```

Then `sops-nix`, systemd credentials, or another future secret substrate
can render the file path. The projected CriomOS module can still end up
with `/var/lib/nix-serve/nix-secret-key`, but that path is deployment
materialization, not cluster truth.

Also consider replacing `public_url: CriomeDomainName` with a real
endpoint type. A cache endpoint is not only a domain; it has scheme,
port, path policy, and trust/public-key context.

### 4. The `lojix` wire contract exists when the daemon exists

The plan says:

> For the first daemon cut, use a Unix socket at
> `/run/lojix/daemon.sock` carrying nota frames. Define the message
> shapes in a new `signal-lojix` crate when there is a second consumer.

I would change this. If `lojix-cli` and `lojix-daemon` are two
processes speaking over a Unix socket, there is already a wire boundary.
Per `skills/contract-repo.md`, the typed records should live in one
contract crate and should own both rkyv wire derives and NOTA text
derives.

The bootstrap can be small, but it should still be typed:

```text
signal-lojix
  DeploymentSubmission
  DeploymentAccepted
  DeploymentRejected
  DeploymentObservation
  CacheRetentionMutation
  GenerationQuery
```

Whether the first home is a dedicated `signal-lojix` repo or a
temporary `signal-lojix` crate inside the lojix workspace is an
implementation coordination question. Semantically, do not create a
throwaway "nota frames" protocol. The contract is the protocol.

### 5. Contained CriomOS nodes need multi-viewpoint evaluation

Phase 3 says the host reads `horizon.containedNodes` and emits
`containers.<name>`. That is the right direction, but the hard part is
missing: each child container needs its own projected viewpoint.

A real contained node needs:

- its own `horizon.node`;
- its own `horizon.exNodes`;
- its own `system`;
- its own `deployment`;
- its own keys, address, and service capabilities.

The host cannot just import "minimal modules plus that contained node's
projected system input" unless CriomOS exposes a function for building a
node module from an arbitrary projected viewpoint.

Recommended shape:

```nix
mkCriomOSNode = {
  horizon,
  system,
  deployment,
  inputs,
}: { config, lib, pkgs, ... }: {
  imports = [ ./modules/nixos/criomos.nix ];
  _module.args = {
    inherit horizon system deployment inputs;
  };
}
```

Then `container-host.nix` can map each contained-node projection through
that function. Without this helper, agents are likely to smuggle child
node facts into host modules and break the data-neutral boundary.

### 6. Do not make closure byte-equivalence the main P2 witness

The plan asks for byte-equivalent closures before and after splitting
`nix.nix`. That is a nice signal if it happens, but it is too brittle as
the main test gate. Module splitting can change generated text paths or
derivation identities while preserving behavior.

Better witnesses:

- `nix flake check` still runs.
- Important options are semantically equal before/after:
  `nix.settings`, `nix.sshServe`, `nix.buildMachines`,
  `services.nix-serve`, firewall ports, known hosts.
- The expected systemd units exist or do not exist for known nodes.
- The hardcoded name scans fail if `prometheus`/`ouranos` gates return.

Keep closure equivalence as an optional regression check, not the
blocker.

### 7. OCI Ghost is not automatically a node substrate

The plan says Path B "exercises the `ContainerHost` substrate
`OciContainer` variant." That may be the wrong framing.

If Ghost is a first-class node with its own address, keys, lifecycle,
and node identity, a plain OCI container is not obviously enough. OCI
can run the workload, but it does not naturally provide the full CriomOS
node shape.

Two cleaner framings:

- **First-class Ghost node:** placement is `Contained {
  substrate = NixosContainer }`; inside that NixOS container, the Ghost
  workload may be native or transitional OCI.
- **Fast Ghost workload:** no first-class node identity; the host runs
  an OCI workload behind the reverse proxy, explicitly marked
  transitional.

Do not blur those. The user explicitly cares about contained nodes with
their own address and keys. That points to the first framing.

## Decisions I Would Send Back

### Q1: first cache/builder boundary

Use the host-level cache/builder. Model it as capabilities on the
dedicated infrastructure host, not as a hard contained node. Revisit
MicroVM isolation only if the builder starts executing less-trusted
workloads.

### Q2: Ghost native vs OCI

If the goal is CriomOS architecture, choose the native module path. If
the goal is publishing quickly, use a transitional OCI workload but do
not call it the final Ghost service model.

My preferred compromise: make Ghost a first-class `NixosContainer`
contained node now, then decide whether the workload inside that node is
native or OCI for the first milestone.

### Q3: child service node identity

Externally addressed services like Ghost should be first-class horizon
nodes. Same-trust helpers like the first `nix-serve` cache should be
host services/capabilities.

### Q4: `InfrastructureHost` naming

The name is good if it describes a data-bearing capability or a derived
role family. It should not be a zero-sized marker.

### Q5: `signal-lojix` home

Create the typed contract at the first CLI-to-daemon socket boundary.
If repository churn matters, a temporary workspace crate is acceptable
only as clearly marked migration debt. Architecturally, the contract is
`signal-lojix`, not an ad hoc local protocol.

## Suggested Edits To System-Assistant Plan

1. Replace `pub struct InfrastructureHost;` with a data-bearing record
   or delete it and derive the concept from capabilities.
2. Add a migration rule for `Machine` vs `NodePlacement`: reject or
   validate dual input; never allow both to be authoritative.
3. Replace `PathBuf` secret paths in capability records with
   `SecretReference`.
4. Add a P3 design item for `mkCriomOSNode` or equivalent multi-viewpoint
   module construction.
5. Reword P2 tests from byte-equivalent closure as the hard gate to
   semantic option/unit witnesses.
6. Reword P5.4 so `signal-lojix` is created when the daemon socket is
   created.
7. Reword Ghost Path B so OCI is a workload implementation unless the
   design explicitly gives OCI-contained services first-class node
   identity.

## Sources Read

- `reports/system-assistant/02-dedicated-cloud-host-implementation-plan.md`
- `skills/contract-repo.md`
- `skills/rust-discipline.md`
- `skills/naming.md`
- `skills/testing.md`
