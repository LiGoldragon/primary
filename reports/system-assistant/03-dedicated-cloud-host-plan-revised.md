# 03 — Dedicated cloud host: revised implementation plan

Date: 2026-05-12
Role: system-assistant
Supersedes: `reports/system-assistant/02-dedicated-cloud-host-implementation-plan.md`
Responds to: `reports/designer-assistant/26-response-to-system-assistant-dedicated-cloud-host-plan.md`
Original architecture: `reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`

## Frame

The designer-assistant accepted plan 02's phase order and most of its
substance, and surfaced seven corrections. All seven are right and
land here as a consolidated revision. Implementation should work from
this report; report 02 is now legacy context.

The seven corrections, in the order the designer listed them:

1. `InfrastructureHost` cannot be a zero-sized marker.
2. `Machine` and `NodePlacement` cannot be dual authorities.
3. `BinaryCache.signing_key_secret_path: PathBuf` cannot live in
   horizon truth.
4. `lojix-cli` ↔ `lojix-daemon` over a socket means the typed
   contract (`signal-lojix`) exists immediately, not "later".
5. P3 has to specify how a host CriomOS evaluation produces child
   CriomOS viewpoints, not just a map of container names.
6. P2 closure byte-equivalence is too brittle as the gating witness.
7. OCI Ghost is a workload implementation, not a node substrate
   that confers identity.

Q3 (child service node identity) and Q4 (`InfrastructureHost`
naming) are resolved below as part of the corrections; Q1, Q2, Q5
are folded in with the designer's preferred answers from
report 26-response.

---

## What changed since plan 02

| § | Change | Driving correction |
|---|---|---|
| P1.1 | `InfrastructureHost` capability deleted; the role-family idea is derived from `NodeCapabilities`. `ContainerHost` keeps a `children: Vec<NodeName>` field projected from `exNodes`. | C1, Q4 |
| P1.2 | Explicit dual-authority rule: new proposals use `placement`; legacy `machine` field is decoded into `MetalPlacement` at parse time; both-present is a validation error. | C2 |
| P1.1 | `signing_key_secret_path: PathBuf` → `signing_key: SecretReference`. New `BinaryCacheEndpoint` type replaces the bare `CriomeDomainName`. | C3 |
| P3 | New §3.1 specifies `mkCriomOSNode` and `horizon.containedNodes` projection shape. The container-host module emits `containers.<name>.config = mkCriomOSNode { ... }` per child. | C5 |
| P2.4 | Test rubric replaced. Semantic option/unit equivalence + a literal-name regression scan are the gate. Closure byte-equivalence is a diagnostic, not a blocker. | C6 |
| P5.4 | `signal-lojix` is created when the socket is created. Bootstrap can be a temporary workspace crate, but it is typed from day one. | C4, Q5 |
| P6 | Ghost is a first-class `Contained { substrate: NixosContainer }` node. The choice of native vs OCI for the *workload inside* that container is what's left to decide. | C7, Q2, Q3 |

The phase numbering and dependency ordering carry over from plan 02
unchanged.

---

## Phase 1 (revised) — Horizon vocabulary pass

### 1.1 Capability records — corrected

`horizon-rs/lib/src/capability.rs` (new module):

```rust
pub struct NodeCapabilities {
    pub build_host: Option<BuildHost>,
    pub binary_cache: Option<BinaryCache>,
    pub container_host: Option<ContainerHost>,
    pub public_endpoint: Option<PublicEndpoint>,
    // No InfrastructureHost. The concept is derived:
    //
    //   fn is_infrastructure_host(&self) -> bool {
    //       self.binary_cache.is_some()
    //           || self.container_host.is_some()
    //           || self.public_endpoint.is_some()
    //   }
    //
    // If a future need names data the marker would have carried,
    // add a real record then.
}

pub struct BuildHost {
    pub max_jobs: u32,
    pub cores_per_job: u32,
    pub trust: AtLeast,
}

pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,
    pub signing_key: SecretReference,
    pub retention_policy: CacheRetentionPolicy,
}

pub struct BinaryCacheEndpoint {
    pub scheme: CacheScheme,        // Http | Https
    pub host: CriomeDomainName,
    pub port: u16,
    pub path_prefix: Option<String>,
    pub public_key: NixPubKey,      // the signing pubkey clients verify against
}

pub enum CacheScheme { Http, Https }

pub struct ContainerHost {
    pub substrates: Vec<ContainmentSubstrate>,
    pub bridge_policy: BridgePolicy,
    pub public_endpoint_policy: PublicEndpointPolicy,
    /// Children whose `placement.host == this_node`. Derived during
    /// projection from `horizon.exNodes`; never authored directly.
    /// Carried as data so consumers don't re-walk `exNodes`.
    pub children: Vec<NodeName>,
}

pub struct PublicEndpoint {
    pub domains: Vec<CriomeDomainName>,
    pub tls_policy: TlsPolicy,
    pub reverse_proxy_policy: ReverseProxyPolicy,
}
```

`SecretReference` (new module `secret.rs`):

```rust
pub enum SecretReference {
    Sops(SopsSecretId),
    SystemdCredential(SystemdCredentialName),
    Agenix(AgenixSecretId),
}

// Logical names. CriomOS modules + the secret substrate config
// resolve these to runtime materialization (file paths, credential
// IDs). Horizon never carries `/var/lib/...` paths.
pub struct SopsSecretId(pub String);
pub struct SystemdCredentialName(pub String);
pub struct AgenixSecretId(pub String);
```

The `SopsSecretId(String)` is a *logical name* (e.g.
`"nix-cache-signing-key"`). The `.sops.yaml` mapping that says which
encrypted file holds that logical secret lives in the secret
substrate config, not in horizon. The runtime path
(`/var/lib/nix-serve/nix-secret-key`) is materialization, derived
inside CriomOS.

### 1.2 Placement records and the dual-authority rule

`horizon-rs/lib/src/placement.rs` (new module):

```rust
pub enum NodePlacement {
    Metal(MetalPlacement),
    Contained(ContainedPlacement),
    // CloudInstance lands in P1.5 once provider-side records exist;
    // not part of the dedicated-host milestone.
}

pub struct MetalPlacement {
    pub arch: Arch,
    pub model: Option<ModelName>,
    pub motherboard: Option<MotherBoard>,
    pub ram_gb: Option<u32>,
}

pub struct ContainedPlacement {
    pub host: NodeName,
    pub substrate: ContainmentSubstrate,
    pub resources: ContainerResources,
    pub network: ContainerNetwork,
    pub state: ContainerState,
    pub trust: AtLeast,
}

pub enum ContainmentSubstrate {
    NixosContainer,   // `containers.<name>` via systemd-nspawn
    MicroVm,          // microvm.nix
    OciContainer,     // workload-only; see P6
    SystemdService,
}
```

**Dual-authority rule (corrects C2).** Exactly one of `placement` or
the legacy `machine` field is authoritative on a `NodeProposal`.
Validation:

- New proposal: `placement` is required, `machine` is rejected.
- Legacy proposal: `machine` is decoded into `MetalPlacement` at
  parse time and `placement` is synthesized; `machine` becomes a
  read-only echo on `Node` for one cycle.
- Both present: validation error
  `Error::ConflictingPlacementAuthority { node: NodeName }` — never
  silently merged.
- Neither present: validation error
  `Error::MissingPlacement { node: NodeName }`.

`Machine` is removed from `Node` after the cycle. The pod-only
`super_node` / `super_user` fields documented in
`horizon-rs/lib/src/machine.rs` migrate into `ContainedPlacement`
(`host` and a new `super_user: Option<UserName>`); their continued
presence on `Machine` is the proof the data wanted its own type.

### 1.3 Compatibility derivation during the cycle

The flags currently consumed by CriomOS — `is_remote_nix_builder`,
`is_dispatcher`, `is_nix_cache`, `behaves_as.virtual_machine` —
derive from the new records during the transition:

- `is_remote_nix_builder = capabilities.build_host.is_some() &&
  is_fully_trusted && !type_is.edge`.
- `is_nix_cache = capabilities.binary_cache.is_some()`.
- `behaves_as.virtual_machine = matches!(placement,
  NodePlacement::Contained(_))`.

The flags survive the cycle so CriomOS keeps compiling. They are
removed in the same commit that drops `Machine` from `Node`.

### 1.4 Goldragon proposal-data shape

Same as plan 02 §1.3, plus the dual-authority rule from §1.2 above.
`placement` is positional at the tail (compatibility);
`capabilities` likewise. Validation lives in `horizon-rs`, not in
goldragon — goldragon emits, horizon validates.

### 1.5 Tests for P1

- Unit: a node with `placement: Contained { host: prometheus,
  substrate: NixosContainer, .. }` projects with
  `behaves_as.virtual_machine = true`,
  `behaves_as.bare_metal = false`.
- Unit: a node with `capabilities: { binary_cache: Some(BinaryCache
  { signing_key: Sops(SopsSecretId("nix-cache-signing-key")), .. }),
  .. }` projects with `is_nix_cache = true`.
- Unit: a proposal with both `placement` and `machine` present is
  rejected with `Error::ConflictingPlacementAuthority`.
- Integration: a child node's `placement.host` is reflected in the
  host's projected `capabilities.container_host.children`.

### 1.6 Sequencing

P1 is still the lock-in point. Nothing after P1 may land before it.

---

## Phase 2 (revised) — CriomOS infrastructure module split + cleanup

§2.1, §2.2, §2.3 carry over from plan 02 unchanged. The split is

```text
modules/nixos/nix/
  default.nix
  client.nix
  builder.nix
  cache.nix
  retention-agent.nix
modules/nixos/infrastructure/
  default.nix
  container-host.nix
  reverse-proxy.nix
```

with the three node-name gates (`prometheus` LLM port,
`["ouranos","prometheus"]` tailnet list, `ouranos` Headscale gate +
literal FQDN) removed in favor of horizon-projected capabilities.

### 2.4 Test rubric — replaced (corrects C6)

The designer is right that closure byte-equivalence is too brittle
as the gate. Module evaluation order can shift derivation hashes
without changing behavior, and a single store-path drift over a
toolchain bump would block the cleanup unnecessarily. New rubric:

**Hard gates (must pass before P2 lands)**

1. `nix flake check` on `CriomOS` succeeds for every cluster node.
2. **Semantic option equivalence** between pre-split and post-split
   `nixosConfigurations.target.config`, evaluated against three
   nodes (`prometheus`, `ouranos`, one edge):
   - `nix.settings` (deep equal)
   - `nix.sshServe` (deep equal)
   - `nix.buildMachines` (set-equal by `hostName`)
   - `services.nix-serve` (deep equal)
   - `networking.firewall.allowedTCPPorts` (set-equal)
   - `programs.ssh.knownHosts` (set-equal by host)
   These are evaluated by a small NixOS test that builds both
   configs and `builtins.toJSON`-compares the named subtrees.
3. **Literal-name scan**: `grep -rE '"(prometheus|ouranos)"'
   modules/` returns no matches. (Per the cleanup rule, the only
   place those strings can appear after P2 is configuration data
   from horizon, never module source.)
4. **Unit-presence scan**: for each known node, the systemd units
   that should exist (`nix-serve.service` on cache nodes,
   `tailscaled.service` on tailnet members, `headscale.service` on
   the Headscale server) are present pre and post; units that
   shouldn't exist are absent in both.

**Diagnostic (run, but does not block)**

- Closure equality on `system.build.toplevel` for the three nodes.
  Drift is interesting and worth a comment in the PR, but does not
  fail the gate.

This rubric also catches the regression mode the designer flagged:
if a future PR re-introduces `node.name == "prometheus"`, the
literal-name scan fails the next CI run.

---

## Phase 3 (revised) — First contained-node substrate

The hard part the previous plan glossed (corrects C5) is that each
contained node is a full CriomOS node and needs its own viewpoint.
The host's container-host module cannot just import "minimal
modules"; it has to *re-evaluate CriomOS* per child, with the
child's projected horizon, system, and deployment inputs.

### 3.1 `mkCriomOSNode` — the missing helper

Add at `CriomOS/lib/mkCriomOSNode.nix`:

```nix
{ flake, inputs }:
{
  horizon,        # the *child's* projected horizon (viewpoint=child)
  system,         # child's system input
  deployment,     # child's deployment input
}:
{ config, lib, pkgs, ... }: {
  imports = [ ../modules/nixos/criomos.nix ];
  _module.args = {
    inherit horizon system deployment inputs;
  };
}
```

This is the function the host uses to build each contained node's
NixOS config. It threads child-viewpoint horizon/system/deployment
into the same module tree the host uses, so a contained node is
just CriomOS evaluated from a different viewpoint. No special-case
"contained CriomOS" module set — the same modules, gated as ever
on capabilities.

### 3.2 `horizon.containedNodes` projection

`horizon-rs` adds, to `Horizon` (the top-level projection):

```rust
pub struct Horizon {
    pub node: Node,                            // viewpoint
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub contained_nodes:                       // NEW
        BTreeMap<NodeName, ContainedNodeView>,
    pub users: BTreeMap<UserName, User>,
    pub cluster: Cluster,
}

pub struct ContainedNodeView {
    pub horizon: Horizon,         // child's viewpoint, fully projected
    pub system: SystemInput,      // child's system flake input
    pub deployment: DeploymentInput,  // child's deployment input
}
```

Population rule: `contained_nodes[child]` is `Some` iff the host's
viewpoint sees a node with `placement: Contained { host: this_node,
.. }`. The child's `horizon.node` is the child viewpoint;
`horizon.ex_nodes` is "everything else from the child's viewpoint",
including the host itself.

This is recursive in shape but not in evaluation: the projector
computes each child viewpoint exactly once, top-down. There is no
provision for nested containment in the first cut (a contained node
cannot itself be a container host); that constraint is enforced at
projection time by rejecting proposals where any
`placement.host = X` and `X` itself is `Contained`.

### 3.3 The container-host module

`modules/nixos/infrastructure/container-host.nix`:

```nix
{ config, lib, horizon, inputs, flake, ... }:
let
  inherit (horizon.node.capabilities) containerHost;
  mkCriomOSNode = import ../../lib/mkCriomOSNode.nix { inherit flake inputs; };
in {
  config = lib.mkIf (containerHost != null) {
    containers = lib.mapAttrs (childName: view: {
      autoStart = true;
      privateNetwork = true;
      hostBridge = "br0";
      localAddress = view.deployment.localAddress;
      hostAddress  = view.deployment.hostAddress;
      privateUsers =
        if view.horizon.node.placement.contained.trust >= AtLeast.Max
        then false  # opt-in only, see §3.4
        else "pick";
      config = mkCriomOSNode {
        inherit (view) horizon system deployment;
      };
    }) horizon.containedNodes;
  };
}
```

Two notes:

- `mkCriomOSNode` is the bridge from §3.1; without it this module
  would not know how to build a NixOS config for a child.
- `flake` and `inputs` are threaded in from the top of CriomOS so
  contained nodes share the host's flake-input universe. Per-child
  input pinning is a future enhancement; not in the first cut.

### 3.4 systemd-nspawn user-namespace policy

Same default as plan 02 §3.2: `placement.trust < Max → privateUsers
= "pick"`. Even at trust = Max, `privateUsers = false` is opt-in
per child via a capability flag on the *child's* placement, not the
host's. Public-internet-exposed containers must keep user
namespacing on; the type system makes this explicit.

### 3.5 Network shape

Same as plan 02 §3.3: host-bridged with `localAddress` per child.
The host's reverse proxy (P5/P6) is the only TLS terminator
visible to the public IP.

### 3.6 Tests for P3

- NixOS test: build a host node with one `NixosContainer` child.
  Boot both. Assert `systemctl is-system-running` reaches `running`
  on both. Assert child is reachable on its `localAddress` from
  the host. Assert `containers.<child>.privateUsers != false`
  unless explicitly opted in.
- Property test on horizon projection: a proposal with nested
  containment (`A: Contained { host: B }`, `B: Contained { host: C
  }`) is rejected with a typed error.

### 3.7 MicroVM.nix (deferred)

Same as plan 02 §3.6: add `microvm.nix` only when the first
`MicroVm` substrate appears in a proposal. The `mkCriomOSNode`
helper above also feeds `microvm.vms.<name>` directly when that
day comes — same function, different consumer.

---

## Phase 4 — Host-level cache and GC root agent

Same as plan 02 §4 with one swap: the agent reads `BinaryCache.signing_key`
as a `SecretReference` (per §1.1 above), and the path
`/var/lib/nix-serve/nix-secret-key` is derived inside CriomOS, not
read from horizon.

§4.3 still recommends bootstrap as a Nix-pure script, migrate to
`lojix-daemon` ownership in P5.

---

## Phase 5 (revised) — Lojix-core extraction and lojix-daemon

§5.1, §5.2, §5.3, §5.5, §5.6 carry over from plan 02 unchanged.
Sequencing recommendation is still: resolve bead `primary-q3y`
(kameo migration) first, then split.

### 5.4 (revised) Wire contract — typed from day one (corrects C4)

Drop the "nota frames for now, contract crate later" framing.
`lojix-cli` and `lojix-daemon` over a Unix socket is two processes
on a wire — per `skills/contract-repo.md` the typed records and the
wire derives belong in one contract crate that both consume.

**First contract surface** (`signal-lojix`, naming consistent with
the `signal-persona-*` family in `protocols/active-repositories.md`):

```text
DeploymentSubmission     // CLI → daemon: "deploy this request"
DeploymentAccepted       // daemon → CLI: ack with a deployment id
DeploymentRejected       // daemon → CLI: typed error
DeploymentObservation    // daemon → CLI/observers: phase events
                         //   Submitted, Building, Built, Copying,
                         //   Activating, Activated, Failed, …
GenerationQuery          // any → daemon: "what's the live set?"
GenerationListing        // daemon → caller: live set
CacheRetentionMutation   // daemon → daemon-internal: pin/unpin/retire
                         //   (also exposed for operator queries)
```

Same `NotaRecord` + rkyv derive shape as the existing
`signal-persona-*` crates. `signal-lojix` carries no behavior; only
typed records and shared error vocabulary.

**Where `signal-lojix` lives.** Two options:

- **A:** dedicated repo `signal-lojix` at
  `github.com/LiGoldragon/signal-lojix`, parallel to `signal-persona-*`.
  Best long-term home; matches the standing convention.
- **B:** temporary `contract/` workspace crate inside `lojix-cli/`
  during the daemon-skeleton milestone. Acceptable only as
  explicitly marked migration debt with a tracking bead.

**Recommendation:** **A**. Repository churn is a one-time cost; an
in-tree workspace crate that other consumers can never depend on
without absorbing the whole `lojix-cli` workspace is a worse trade.
The `signal-persona-*` crates set the precedent.

The bootstrap is small (one or two record types decoded over the
socket on first deploy event) — small but typed, not free-form
nota-text.

---

## Phase 6 (revised) — Ghost as first public service node

The designer's compromise (corrects C7, resolves Q2/Q3): **Ghost is
a first-class `Contained { substrate: NixosContainer }` node.** The
node identity, address, keys, and lifecycle are NixOS-shaped via
the container substrate. The choice of native module vs OCI
workload is then a question about *what runs inside that
container*, not about whether Ghost has a node identity.

### 6.1 Ghost node shape (fixed)

In horizon:

```text
node ghost
  species: ?         # not Center; needs a designer answer — likely a
                     # new variant or "Hybrid" if compatible
  size: medium
  trust: medium      # public-facing service, not fully trusted
  placement: Contained {
    host: hyacinth   # the dedicated infrastructure host
    substrate: NixosContainer
    resources: { cores: 2, ram_gb: 2 }
    network: { localAddress: 10.42.0.10, ... }
    state: { persistent_paths: [ "/var/lib/ghost" ] }
    trust: Medium
  }
  capabilities: {
    public_endpoint: Some(PublicEndpoint {
      domains: [ "ghost.<cluster>.criome", ... ],
      tls_policy: AcmeLetsEncrypt,
      reverse_proxy_policy: HostTerminates,
    }),
  }
```

Because Ghost has its own `placement` and its own `capabilities`,
the host's reverse proxy automatically picks it up via
`PublicEndpoint`, and the host's container-host module
automatically materializes it via `mkCriomOSNode`.

### 6.2 Workload-inside-the-container — the remaining decision

With identity sorted, the remaining question is what runs inside
the Ghost container:

- **Workload A: native NixOS service.** Inside the contained
  CriomOS node, `services.ghost.enable = true` consumes a
  CriomOS-owned `services/ghost.nix` module that packages Ghost
  from the upstream tarball, runs `services.mysql` with `mysql80`,
  and reads secrets via `SecretReference`s declared in the Ghost
  node's `capabilities`. ~1 week to build and harden the package.
- **Workload B: OCI bridge.** Inside the contained CriomOS node,
  `virtualisation.oci-containers.containers.ghost = { ... }` runs
  the official Ghost image, with image tags pinned via a typed
  `ContainerImagePin` capability. ~2 days. The contained node
  still has full CriomOS identity; only the *workload* is OCI.

The corrections from C7 mean we no longer pretend Path B implies
"Ghost is an OCI-substrate node." Path B is a workload choice
inside an otherwise NixosContainer-substrate node.

The designer recommends "first-class NixosContainer node now;
decide native vs OCI workload for the first milestone." That stands
as the resolution. The native vs OCI workload question is the only
open Ghost decision; see §"Decisions still owed" below.

### 6.3 Decision matrix (revised — workload only)

| Criterion | Workload A (native) | Workload B (OCI inside the container) |
|---|---|---|
| First-deploy time | ~1 week | ~2 days |
| Long-term fit | Native NixOS service | Transitional workload |
| Horizon truth coverage | Full | Image tag is a typed pin |
| Secret discipline | `SecretReference` → sops/credentials | Same |
| Upgrade story | `nixos-rebuild` | `nixos-rebuild` + image tag bump |
| Ghost-version churn cost | Each version needs packaging | Bump tag in horizon |
| Force-multiplier for next service | High | Low |
| Backup story | Identical (content + DB) | Identical |

The asymmetry is the same as in plan 02 §6.4, but the framing is
honest: this matrix only chooses what runs *inside* the Ghost
node, not whether Ghost has node identity.

---

## Decisions resolved by the designer's response

| Open question | Status |
|---|---|
| Q1 — first cache/builder boundary | **Resolved**: host-level capabilities; revisit isolation only if the builder runs less-trusted workloads. |
| Q3 — child service node identity | **Resolved**: externally-addressed services (Ghost) are first-class horizon nodes; same-trust helpers (first cache) stay as host capabilities. |
| Q4 — `InfrastructureHost` naming | **Resolved by deletion**: not a marker type. Derived from capabilities; no name needed. |
| Q5 — `signal-lojix` home | **Resolved**: dedicated repo, created when the daemon socket is created. |

## Decisions still owed

| Open question | Owner | Blocks |
|---|---|---|
| Q2 — Ghost workload native vs OCI inside the container | designer | P6 implementation start |
| New: which `NodeSpecies` Ghost claims (existing variant or new) | designer | P1 proposal validation for Ghost |

## Coordination notes

Same as plan 02. The `system-data-purity-and-wifi-cert-audit` lock
held by `system-specialist` over `CriomOS`, `CriomOS-home`,
`CriomOS-lib`, `horizon-rs`, `goldragon`, `clavifaber` covers most
P1 / P2 / P5 paths. The `tools/orchestrate claim` for
`system-assistant` waits on lock release or split.

Beads to file (unchanged from plan 02 §"Cross-cutting"):

- P1: "horizon-rs: typed placement, capability, and SecretReference
  records (with dual-authority validation)"
- P2: bead body folds into existing `primary-tpd`
  (Tailscale/Headscale review)
- P3: "CriomOS: container-host module, mkCriomOSNode helper, and
  first NixosContainer child"
- P4: "lojix: cache GC-root agent (bootstrap script form)"
- P5: file after `primary-q3y` closes; "lojix: extract lojix-core,
  add lojix-daemon, create signal-lojix contract crate"
- P6: blocked on Q2

## Sources

- Designer-assistant response:
  `reports/designer-assistant/26-response-to-system-assistant-dedicated-cloud-host-plan.md`
- Original architecture:
  `reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`
- Superseded plan:
  `reports/system-assistant/02-dedicated-cloud-host-implementation-plan.md`
- Skills consulted: `skills/contract-repo.md`, `skills/abstractions.md`,
  `skills/naming.md`, `skills/testing.md`,
  `skills/system-assistant.md`.
- Live source unchanged from plan 02's verification at
  `/git/github.com/LiGoldragon/{horizon-rs,CriomOS,lojix-cli}`.
