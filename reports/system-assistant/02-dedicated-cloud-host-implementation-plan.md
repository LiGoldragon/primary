# 02 — Dedicated cloud host + contained node: implementation plan

Date: 2026-05-12
Role: system-assistant
Builds on: `reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`
Upstream survey: `reports/designer-assistant/26-criomos-cloud-infrastructure-survey.md`

## Frame

Designer-assistant report 27 made the architectural choices: split node truth
into role / placement / capability; first contained substrate is NixOS
declarative containers (`systemd-nspawn`); MicroVM.nix is the second tier for
weaker-trust public services; the first Nix cache/builder stays host-level;
`lojix-cli` shrinks to a one-Nota wrapper while a `lojix-daemon` grows into
the long-lived owner of generation liveness, GC roots, and contained-node
lifecycle. Ghost is the first real public service node and it is not in
nixpkgs as a module.

This report is the engineering plan to land that. It does not relitigate
the architecture; the open questions in §"Open Questions" of report 27 are
explicitly listed at the end of this report as decisions owed back to the
designer. It is **research**: no code lands here, and several of the paths
listed below sit under the existing `system-data-purity-and-wifi-cert-audit`
lock held by `system-specialist` on `CriomOS`, `CriomOS-home`, `CriomOS-lib`,
`horizon-rs`, `goldragon`, and `clavifaber` (verified at write time in
`/home/li/primary/system-specialist.lock`). Implementation must coordinate
through `protocols/orchestration.md` once that lock releases or splits.

Verified against the live source at write time:

- `horizon-rs/lib/src/species.rs` — `MachineSpecies` is `Metal | Pod` only.
- `horizon-rs/lib/src/machine.rs` — `Machine` has pod-only fields
  (`super_node`, `super_user`).
- `horizon-rs/lib/src/node.rs` — `BehavesAs::virtual_machine` derives from
  `MachineSpecies::Pod`; `is_remote_nix_builder`, `is_dispatcher`, and
  `is_nix_cache` derive from role/trust/size as report 27 quoted.
- `CriomOS/modules/nixos/nix.nix` — single file mixes Nix client, build
  receiver, dispatcher, cache; carries the `node.name == "prometheus"`
  string. Lines 75–82 and 215–225.
- `CriomOS/modules/nixos/network/tailscale.nix` — gates on
  `elem node.name [ "ouranos" "prometheus" ]`.
- `CriomOS/modules/nixos/network/headscale.nix` — gates on
  `node.name == "ouranos"`, builds `ouranos.${cluster.name}.criome` literal.
- `lojix-cli/src/request.rs` and `src/deploy.rs` — current actor pipeline is
  `ractor`-based (`ProposalReader → HorizonProjector → HorizonArtifact →
  NixBuilder → ClosureCopier → Activator`, supervised by `DeployCoordinator`).
  The `Cargo.toml` still pins `ractor = "0.13"`.
- Open bead `primary-q3y` already tracks the `ractor` → `kameo` migration.
  Lojix-core extraction must sequence with that.

The plan below is ordered for **dependency**, not urgency. Phases are
independent enough that they can be claimed by separate
operator/system-specialist passes once decisions are nailed.

---

## Mapping designer-27 → engineering phases

| Designer-27 step | Engineering phase | Primary repo(s) | Lock/bead |
|---|---|---|---|
| Horizon vocabulary | **P1** | `horizon-rs`, `goldragon` | sits under `system-data-purity` lock |
| CriomOS infra module split + node-name cleanup | **P2** | `CriomOS` | sits under `system-data-purity` lock; intersects bead `primary-tpd` |
| First contained node substrate (NixOS containers) | **P3** | `CriomOS` | depends on **P1**, **P2** |
| Host-level cache + GC root agent | **P4** | `CriomOS`, future `lojix-daemon` | depends on **P1** for capability data |
| `lojix-core` extraction + `lojix-daemon` skeleton | **P5** | `lojix-cli` | sequences with bead `primary-q3y` (kameo migration) |
| Ghost first public service node | **P6** | `CriomOS`, possibly `pkgs/` | depends on **P3**; requires designer answer to "Path A vs Path B" |

---

## Phase 1 — Horizon vocabulary pass

The single change that unblocks every other phase: stop overloading
`MachineSpecies::Pod` and `NodeSpecies::Center` to mean "where the node lives"
and "what infrastructure services it runs." Add typed axes for placement and
capability. Keep `NodeSpecies` as compatibility/archetype sugar so existing
consumers compile during the transition.

### 1.1 New typed records (in `horizon-rs/lib/src/`)

Add a new module `placement.rs`:

```rust
// horizon-rs/lib/src/placement.rs (new)
pub enum NodePlacement {
    Metal(MetalPlacement),
    Contained(ContainedPlacement),
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
    NixosContainer,   // declarative `containers.<name>` via systemd-nspawn
    MicroVm,          // microvm.nix
    OciContainer,     // podman / docker via NixOS oci-containers module
    SystemdService,   // bare service, no namespace
}
```

And a `capability.rs`:

```rust
// horizon-rs/lib/src/capability.rs (new)
pub struct NodeCapabilities {
    pub build_host: Option<BuildHost>,
    pub binary_cache: Option<BinaryCache>,
    pub container_host: Option<ContainerHost>,
    pub public_endpoint: Option<PublicEndpoint>,
    pub infrastructure_host: Option<InfrastructureHost>,
}

pub struct BuildHost {
    pub max_jobs: u32,
    pub cores_per_job: u32,
    pub trust: AtLeast,
}

pub struct BinaryCache {
    pub public_url: CriomeDomainName,
    // Path on disk; the actual key bytes never enter horizon.
    pub signing_key_secret_path: PathBuf,
    pub retention_policy: CacheRetentionPolicy,
}

pub struct ContainerHost {
    pub substrates: Vec<ContainmentSubstrate>,
    pub bridge_policy: BridgePolicy,
    pub public_endpoint_policy: PublicEndpointPolicy,
}

pub struct PublicEndpoint {
    pub domains: Vec<CriomeDomainName>,
    pub tls_policy: TlsPolicy,
    pub reverse_proxy_policy: ReverseProxyPolicy,
}

pub struct InfrastructureHost; // marker capability — "this node hosts infra"
```

Naming: `InfrastructureHost` (not `CloudHost` — provider-leaking) and
`ContainerHost` as a narrower capability, per designer 27 §"Role".

### 1.2 Wire into `Node` and `NodeProposal`

- Add `placement: NodePlacement` to `NodeProposal` and to `Node`. Keep
  `machine: Machine` for one cycle and derive it from
  `placement` at projection time, so existing `pkgs/` consumers don't
  break in the same commit.
- Add `capabilities: NodeCapabilities` to `Node`. Derive the existing
  `is_remote_nix_builder`, `is_nix_cache`, `is_dispatcher` flags from
  the new capability records during the transition; do not delete the
  flags in the same commit that adds the records.
- Adjust `BehavesAs::derive` to read from `placement` rather than
  `machine.species`; `MachineSpecies::Pod` becomes a legacy synonym for
  `Contained { substrate: NixosContainer, .. }`.

### 1.3 Goldragon proposal-data shape

The cluster proposal that goldragon emits gets the new records. The
proposal-side change is:

- New `placement` field (positional, at the tail per nota convention,
  `Option<NodePlacement>` for backward parsing) on every node proposal.
- New `capabilities` field, same convention.
- The derivation rules in `node.rs`'s `NodeProposal::project` consume
  the new fields if present; fall back to the current
  `species`/`machine.species`-driven derivations if absent.

### 1.4 Tests for P1

- `horizon-rs/lib/src/`: existing projection tests must stay green
  with no proposal changes (compatibility derivation works).
- New unit tests: a node with `placement: Contained { host: prometheus,
  substrate: NixosContainer, .. }` projects with
  `behaves_as.virtual_machine = true` and `behaves_as.bare_metal =
  false`.
- New integration test: a node with both `species: Center` and
  `capabilities: { binary_cache: Some(..), build_host: Some(..) }`
  projects with `is_nix_cache = true` derived from the capability,
  not from the species.

### 1.5 Sequencing note

P1 is the lock-in point. Once `placement` and `capabilities` exist in
the projection, every later phase keys off them. No other phase should
land before P1 because its file changes will be rewritten when P1 lands.

---

## Phase 2 — CriomOS infrastructure module split + data-neutrality cleanup

### 2.1 Split `nix.nix`

Replace `modules/nixos/nix.nix` with a `nix/` subdirectory:

```text
modules/nixos/nix/
  default.nix          # imports the four below
  client.nix           # nix.settings, package, channel.enable, registry
  builder.nix          # sshServe + buildMachines + knownHosts
  cache.nix            # nix-serve, nix-serve user/group, port 80 firewall
  retention-agent.nix  # gc-root agent (P4 lands the body)
```

Each file's gate:

- `client.nix` — unconditional (every node).
- `builder.nix` — `mkIf horizon.node.capabilities.buildHost != null`,
  swapping the current `isRemoteNixBuilder` and `isDispatcher` flags
  for capability projections from P1.
- `cache.nix` — `mkIf horizon.node.capabilities.binaryCache != null`,
  swapping `isNixCache`.
- `retention-agent.nix` — `mkIf
  horizon.node.capabilities.binaryCache.retentionPolicy != null`. Stub
  in P2; body lands in P4.

The mechanical change is small per file; the structural value is
naming the four concerns.

### 2.2 Remove node-name gates

Three documented violations in the current code:

- `modules/nixos/nix.nix:79` — `optional (node.name == "prometheus") 11436`.
  Replace with `horizon.node.capabilities.publicEndpoint.openPorts` or
  with whatever the LLM service module already projects (this is the
  per-node llama.cpp service port; it should sit beside the LLM gate,
  not in the Nix module).
- `modules/nixos/network/tailscale.nix:10` — `elem node.name
  [ "ouranos" "prometheus" ]`. Add a `TailnetMember` capability or a
  projected boolean `horizon.node.tailnetMember`. Coordinates with
  open bead `primary-tpd` (Tailscale/Headscale role review).
- `modules/nixos/network/headscale.nix:14` — `node.name == "ouranos"`
  and the literal `"ouranos.${cluster.name}.criome"` FQDN at line
  17–20. Replace with a projected `HeadscaleServer` capability that
  carries its public name, port, and TLS policy. The fallback FQDN
  construction in `headscale.nix:20` is the smell — that is the
  CriomOS module guessing at horizon truth.

### 2.3 Add `infrastructure/` subdirectory

```text
modules/nixos/infrastructure/
  default.nix
  container-host.nix       # P3 — projects `containers.<name>`
  reverse-proxy.nix        # P5/P6 — single nginx/caddy from PublicEndpoint
```

`default.nix` aggregates and is added to the `criomos.nix` import list.

### 2.4 Tests for P2

- `nix flake check` on CriomOS (build-only) must pass on every node
  in the current cluster after the split.
- A target build of `nixosConfigurations.target.config.system.build.toplevel`
  for `prometheus`, `ouranos`, and one edge node must produce
  byte-equivalent closures pre/post split. (Equivalent at the system
  closure root; module evaluation order changes, but the realised
  derivation graph for the same input proposal must be identical.)
- Integration: existing `checks/whisrs-level-widget` and any other
  CriomOS tests still pass.

### 2.5 Sequencing note

P2 can start the moment P1 is merged. The compat-shimmed flags
(`isNixCache`, `isRemoteNixBuilder`, `isDispatcher`) keep working
during the cutover — P2 just changes which condition the modules
read from.

---

## Phase 3 — First contained-node substrate

### 3.1 What this phase produces

A `modules/nixos/infrastructure/container-host.nix` that:

1. Reads `horizon.node.capabilities.containerHost.substrates`. If it
   contains `NixosContainer`, enables the host scaffolding for
   declarative containers.
2. Reads `horizon.containedNodes` (a new projected map keyed by
   container `NodeName`, projected for nodes whose `placement.host
   == this node`) and emits `containers.<name> = { ... }` per entry.
3. Each emitted container imports a curated minimal NixOS module set
   plus that contained node's projected `system` input (so the
   contained node is itself a CriomOS NixOS generation, not an ad-hoc
   container config).

The crucial property: the contained node is **just another node** in
the horizon proposal. Its `placement.host` names the dedicated server
it lives inside. Goldragon proposes both host and child; horizon
projects both; CriomOS's container-host module is the bridge.

### 3.2 systemd-nspawn user-namespace policy

Public-facing contained nodes must declare `privateUsers`. The default
for the container-host module:

- `placement.trust < AtLeast::Max` → `privateUsers = "pick"` (auto
  user-namespace mapping).
- `placement.trust == Max` → `privateUsers = false` is allowed only
  when capability flag explicitly opts in. Default: still `"pick"`.

This is the published `systemd-nspawn(1)` discipline: without user
namespacing, container root is host root for capability-permitted
operations, which is unacceptable for any service exposed to the
public internet.

### 3.3 Network shape

Default to host-bridged networking (`hostBridge` /
`hostAddress` / `localAddress` per the NixOS containers module). The
host's reverse proxy (P5/P6) terminates TLS on the public IP and
proxies to the contained node's `localAddress` — that is the
`ContainerHost.bridge_policy` and `PublicEndpoint.reverse_proxy_policy`
in concrete form.

### 3.4 Independence from host generation

Designer-27 §"Cost" called this out: declarative containers update
with the host. For the first dedicated server this is fine — the host
deploys are atomic and `lojix` already manages them. Two notes:

- Do **not** import `extra-container` yet. Adding a second update
  cadence before the first one is proven adds unnecessary state.
- When independent updates become useful, the natural answer is
  `lojix-daemon`-owned per-container activation, not `extra-container`,
  because it keeps the same activation boundary lojix already owns.

### 3.5 Tests for P3

- A NixOS test (under `CriomOS/checks/`) that builds a host node with
  one declarative `NixosContainer` child, boots both, and asserts the
  child's `systemctl is-system-running` reaches `running` and is
  reachable on its `localAddress` from the host.
- `placement.trust < Max` host build must fail evaluation if
  `privateUsers` is explicitly set to `false` on the child. (Belt-and-
  suspenders: the type system prevents the proposal, the module
  asserts it, and the test catches regressions.)

### 3.6 Reserved for later: MicroVM.nix

Add `microvm.nix` as a flake input only when `ContainmentSubstrate::
MicroVm` first appears in a proposal. Its host module will live at
`modules/nixos/infrastructure/microvm-host.nix`. Skeleton outline:

- `mkIf any (s: s == MicroVm) capabilities.containerHost.substrates`.
- One `microvm.vms.<name>` per contained node with that substrate.
- Default to `shares` containing read-only `/nix/store`; never
  writable until designer reopens that decision (per designer-27
  §"Cost").

Do not land this in P3. Carrying both substrate paths before either
has shipped is premature.

---

## Phase 4 — Host-level cache and GC root agent

### 4.1 Cache stays host

Per designer-27 §"Nix Cache And Builder Shape": the first dedicated
host runs `nix-serve` directly, not in a container. P2 already moved
the wiring into `nix/cache.nix`; P4 only adds the retention agent.

### 4.2 GC root layout

`/nix/var/nix/gcroots/criomos/<cluster>/<node>/<kind>/<generation>` →
`<store-path>` symlinks, one per:

- `current` — the active system or home top-level.
- `boot-pending` — the closure currently on `system.profile` but not
  yet activated.
- `rollback/<n>` — the last N rolled-back generations (default 4).
- `pinned/<label>` — operator-pinned releases (e.g. tagged builds).
- `recent/<timestamp>` — short-grace builds to keep the cache from
  evicting freshly-built closures before clients fetch them.

Closure introspection uses `nix path-info -r`; do not reimplement
Nix's reachability graph.

### 4.3 Where the agent lives

Two options:

- **A:** as a small standalone daemon in `lojix-daemon` (P5). Reads
  events from the deploy event log, writes/removes roots.
- **B:** as a `systemd` oneshot triggered from the activation phase
  of every deploy.

Recommendation: **A** is the right home, but B is the bootstrap. Land
B in P4 as a small Nix-pure script (path-only, idempotent, no daemon
state), and migrate to A when P5 is far enough along that the daemon
has an event log to subscribe to. Document B as transitional in
`retention-agent.nix`.

### 4.4 Two-phase deletion

Per designer-27 §"Recommended first retention model" item 6: deletion
first removes the root and the index entry, then waits for the
narinfo TTL before assuming clients stopped requesting the path.
Concrete implementation:

- The agent removes the root.
- An immediate `nix-collect-garbage --delete-older-than <ttl>` is
  **not** run; rely on the next nightly GC, which is already configured
  per-node in the existing `nix.gc` settings.
- The narinfo TTL is `narinfo-cache-positive-ttl` /
  `narinfo-cache-negative-ttl` in `nix.conf`. Set them explicitly in
  `nix/cache.nix` once the agent ships, so the grace window is
  documented next to the agent.

### 4.5 Attic deferred

Designer-27 named Attic as the scale path. Do not land it in P4. The
trigger for adding Attic is "second cache node exists or first
multi-region build farm proposal lands" — neither is true today.

### 4.6 Tests for P4

- Unit test on the script: given a mocked store path tree, root
  creation/removal is idempotent.
- NixOS test that deploys a generation, verifies a root appears under
  `/nix/var/nix/gcroots/criomos/...`, deploys again, verifies the
  rollback root for the previous generation also exists, and
  `nix-collect-garbage` does not delete either.

---

## Phase 5 — Lojix-core extraction and lojix-daemon skeleton

### 5.1 What the current shape gives us

`lojix-cli/src/deploy.rs` already encodes the actor pipeline. The
extraction is largely a **package split**, not a rewrite:

```text
lojix-cli/                     (current monolith)
  Cargo.toml      [package] lojix-cli
  src/
    main.rs       parse argv → LojixRequest → DeployCoordinator
    deploy.rs     DeployCoordinator + actor wiring
    build.rs      NixBuilder
    copy.rs       ClosureCopier
    activate.rs   Activator
    artifact.rs   HorizonArtifact
    project.rs    HorizonProjector
    proposal.rs   ProposalReader
    request.rs    LojixRequest, FullOs/OsOnly/HomeOnly
```

→

```text
lojix-cli/                     (workspace root, multi-crate)
  Cargo.toml      [workspace]
  core/                        (new crate: lojix-core)
    Cargo.toml    [package] lojix-core
    src/
      lib.rs
      deploy.rs   ← from cli/src/deploy.rs
      build.rs    ← from cli/src/build.rs
      copy.rs     ← from cli/src/copy.rs
      activate.rs ← from cli/src/activate.rs
      artifact.rs ← from cli/src/artifact.rs
      project.rs  ← from cli/src/project.rs
      proposal.rs ← from cli/src/proposal.rs
      request.rs  ← from cli/src/request.rs (struct moves; CLI parsing stays in cli)
  cli/                         (renamed: was the whole thing)
    Cargo.toml    [package] lojix-cli  (depends on lojix-core)
    src/
      main.rs     thin: argv → LojixRequest → call lojix-core
  daemon/                      (new crate: lojix-daemon, P5.4)
    Cargo.toml    [package] lojix-daemon
    src/
      main.rs
      live_set.rs
      gc_roots.rs
      events.rs
```

### 5.2 Sequence with the kameo migration (bead `primary-q3y`)

`primary-q3y` will rewrite the actor framework from `ractor` to
`kameo`. Sequencing options:

- **Option A: kameo first, extract second.** Bead `primary-q3y` lands;
  the actors get rewritten in place inside `lojix-cli/src/`. Then this
  phase splits the kameo-based crate into `lojix-core` + `lojix-cli`.
  Cleaner for the diff because the crate split moves whole files
  rather than rewriting them.
- **Option B: extract first, kameo second.** This phase does a mechanical
  package split with `ractor` actors intact. Bead `primary-q3y` then
  rewrites only `lojix-core`'s actor surface. Better if `primary-q3y`
  is delayed and the cache-retention agent (P4 → P5 migration) needs
  `lojix-daemon` sooner.

Recommendation: **Option A**. Resolve `primary-q3y` first. The crate
split is mechanical and small; doing it after the actor framework is
stable means it is one diff, not two. If P4 runs the cache-retention
agent as a Nix-pure script in the bootstrap form (per §4.3), nothing
in P4 blocks waiting for kameo.

### 5.3 Daemon shape

`lojix-daemon` owns long-lived state:

- **Live set** — `BTreeMap<(ClusterName, NodeName, Kind), Generation>`
  persisted via `sema` (today's typed db; see active-repositories.md).
- **GC roots** — owns the `/nix/var/nix/gcroots/criomos/...` tree.
- **Event log** — appends typed events
  (`BuildRealized`, `CachePublished`, `ActivationSucceeded`,
  `GenerationRetired`, `ContainerStarted`, `ContainerStopped`).
- **Container lifecycle** — observes `containers.<name>.service`
  via systemd dbus, mirrors transitions into the event log.

The daemon does **not** initiate deploys itself in the first cut. It
observes and records. Deploy initiation stays where it is — the CLI
sends a request, the daemon records what happened.

### 5.4 Wire contract

Designer-27 named `signal-lojix` as the eventual signal vocabulary.
For the first daemon cut, use a Unix socket at
`/run/lojix/daemon.sock` carrying nota frames. Define the message
shapes in a new `signal-lojix` crate when there is a second consumer
of the daemon's events; until then the daemon's API is "lojix-cli
talks to it directly through a typed local channel."

### 5.5 `BuilderSelection` refactor

Designer-27 §"5. Lojix daemon extraction" item 4 named replacing
`builder: Option<NodeName>` with a closed enum. Concrete:

```rust
// in lojix-core/src/request.rs
pub enum BuilderSelection {
    Local,                    // build on the deploy target
    DispatcherChooses,        // delegate to dispatcher
    Named(NodeName),          // explicit remote builder
}
```

This collapses the current `None == "local-or-dispatcher-decides"`
overload that the existing `resolve_builder_target` carries
(`lojix-cli/src/deploy.rs:59-75`). Migration:

- Add `BuilderSelection`. Keep `builder: Option<NodeName>` as a
  deprecated alias for one cycle, decoded as
  `None → DispatcherChooses, Some(n) if n == self.node → Local,
  Some(n) → Named(n)` to match the current behavior.
- Deprecate after one operator-visible release; remove after two.

### 5.6 Tests for P5

- The crate split must not change behavior. Existing
  `lojix-cli/tests/` integration tests run against the new
  `cli` binary unchanged.
- Daemon: a NixOS test that brings up `lojix-daemon`, runs a deploy,
  asserts the event log contains the expected ordered events and
  the GC-root tree was updated.

---

## Phase 6 — Ghost as first public service node

### 6.1 The honest constraints

Per designer-27 §"Ghost As First Public Service Node":

- Nixpkgs has `ghost-cli` (a deployment helper) but no `services.ghost`
  module and no `pkgs.ghost` for the CMS itself.
- Ghost 6 needs Node `^22.13.1` and supports MySQL 8 only for
  production.
- Ghost has an official Docker Compose path.

The decision (Path A: native NixOS module, vs Path B: transitional
OCI bridge) is owed back to the designer. Designer-27 §"Open
Questions" item 2 names it. **This phase does not choose; it scopes
both paths so the decision can be made on cost data.**

### 6.2 Path A — native NixOS module

Module would live at `CriomOS/modules/nixos/services/ghost.nix` and a
package at `CriomOS/packages/ghost/default.nix`. Estimated work:

- Package Ghost from upstream tarball using `mkYarnPackage` or the
  `pnpm` overlay (Ghost ships a yarn lockfile; check whether 6.x
  switched). 1–2 days for a clean working pin.
- Package Ghost-CLI separately and use it to bootstrap config.
  Alternative: skip ghost-cli and write the `config.production.json`
  declaratively from horizon-projected facts. The declarative path
  is more CriomOS-shaped.
- `services.ghost = { enable, version, contentDir, dbHost, dbName,
  mailFrom, ... }`. Maps to a systemd unit running `ghost`'s node
  entrypoint.
- MySQL 8 service (existing nixpkgs `services.mysql` with
  `package = pkgs.mysql80`).
- Reverse proxy: nginx with TLS via `security.acme` from horizon.
- Secrets: mail/Stripe via `sops-nix` or systemd credentials per the
  cluster's secret discipline (still being settled per designer-26
  §"Current CriomOS Shape").
- Backup: borg/restic of the content directory + mysqldump cron.
  Belongs in a `services/ghost-backup.nix` sibling.

Risk: `ghost-cli` is designed to manage Ghost imperatively. Avoiding
it means tracking what the official "production install" actually
provisions — straight from the tarball, not from the install guide's
prose.

### 6.3 Path B — transitional OCI bridge

Use NixOS's `virtualisation.oci-containers` module. Estimated work:

- `services/ghost-oci.nix` declaring the Ghost image, MySQL image,
  and named volumes.
- Image tags pinned in horizon (a `ContainerImagePin` capability or
  similar typed record), not in Nix files. The image-tag pin is the
  one piece that must come from horizon-projected truth, otherwise
  Docker Compose becomes a second deployment language.
- Volume state under `/var/lib/ghost/` and `/var/lib/mysql-ghost/`,
  declared in the module.
- `EnvironmentFile` populated from `sops-nix` at runtime; secrets
  never enter the Nix store.
- Reverse proxy + TLS as in Path A.

This gets a working public Ghost faster and exercises the
`ContainerHost` substrate `OciContainer` variant, which is useful in
its own right. The cost is the standing reminder that the OCI image
graph is a second source of truth — every image bump is an
operator-visible step that does not flow from horizon proposal
changes.

### 6.4 Decision matrix

| Criterion | Path A (native) | Path B (OCI) |
|---|---|---|
| First-deploy time | ~1 week | ~2 days |
| Long-term fit | Native NixOS service node | Transitional bridge |
| Horizon truth coverage | Full | Partial (image tags) |
| Secret discipline | `sops-nix` | `sops-nix` (same) |
| Upgrade story | `nixos-rebuild` | `nixos-rebuild` + image tag bump |
| Ghost-version churn cost | Each version needs packaging | Bump tag in horizon |
| Force-multiplier for next service | High (every native module is reusable shape) | Low (next OCI service is the same work again) |
| Backup story | Identical (same content + DB) | Identical |

If the goal is "improve CriomOS," choose A. If the goal is "publish
Ghost this month and revisit," choose B and **mark the module
explicitly transitional** (`ghost-oci.nix` is fine; do not call it
`ghost.nix` since that name should be reserved for the native
implementation).

---

## Cross-cutting: which beads track what

| Phase | Existing bead | Notes |
|---|---|---|
| P1 | none today | File a `role:system-specialist` bead "horizon-rs: typed placement and capability records" once decisions in §"Decisions owed" land. |
| P2 | `primary-tpd` (Tailscale/Headscale review) | Subsumes the node-name cleanup. File a new bead "CriomOS: split nix.nix into nix/{client,builder,cache,retention-agent}.nix" before P2 starts. |
| P3 | none today | File a bead "CriomOS: container-host module + first NixosContainer node" after P1 lands. |
| P4 | none today | File a bead "lojix: cache GC-root agent (bootstrap script form, then daemon)". |
| P5 | `primary-q3y` (Ractor → Kameo) | Sequence A (resolve `primary-q3y` first). File bead "lojix: extract lojix-core crate and add lojix-daemon skeleton" once `primary-q3y` closes. |
| P6 | none today | Do not file until designer answers Path A vs B. The bead body depends on the answer. |

All beads file under `role:system-specialist` per
`skills/system-assistant.md` §"Active beads" — the system-assistant
pool has no separate label.

---

## Coordination with the current `system-data-purity` lock

`/home/li/primary/system-specialist.lock` currently shows
`system-data-purity-and-wifi-cert-audit` over `CriomOS`,
`CriomOS-home`, `CriomOS-lib`, `horizon-rs`, `goldragon`, and
`clavifaber`. P1, P2, and (later) P5 all touch paths under that lock.

Two clean handoffs:

1. The audit closes. `system-specialist` releases the lock. The first
   phase claim (`tools/orchestrate claim system-assistant horizon-rs
   -- "P1 typed placement+capability records per
   reports/system-assistant/02-..."`) takes the same paths.
2. The audit splits. `system-specialist` releases `horizon-rs` while
   keeping the CriomOS paths. P1 starts under
   `system-assistant`, P2 waits for the rest of the lock to release.

Do not start file edits until one of those two happens.

---

## Decisions owed back to designer

These remain unresolved after report 27 §"Open Questions" and block
the phases listed:

1. **Q1: hard container boundary for the first cache?** Designer-27
   recommends host-level. Plan above takes that recommendation. If
   the answer changes, P4 grows a `BinaryCache` substrate variant
   (likely `MicroVm` with shared `/nix/store`) and the host-level
   option in §4.1 retires. Blocks: P4.

2. **Q2: Ghost native vs OCI?** Decision matrix in §6.4 above.
   Blocks: P6.

3. **Q3: child service nodes as first-class horizon nodes?**
   Designer-27 recommends first-class for externally-addressed
   services like Ghost; plain host services for same-trust helpers.
   Plan above assumes that split. If Ghost is a plain host service
   instead of a child node, §3 and §6 both shrink. Blocks: P3, P6.

4. **Q4: `InfrastructureHost` as the role name?** Plan above takes
   it. If a different name lands, P1's `capability.rs` renames once
   and P2's reverse-proxy/container-host modules read the new field
   name. Cheap to change.

5. **New question: where does `signal-lojix` live?** Designer-27
   §5.3 names a contract crate. Suggested name and home:
   `signal-lojix` at `github.com/LiGoldragon/signal-lojix`,
   following the `signal-persona-*` convention from
   `protocols/active-repositories.md`. Blocks: P5.4 wire contract,
   though the bootstrap (local Unix socket + nota frames) is fine
   without the contract crate.

---

## Sources

- Live source verified at write time:
  `/git/github.com/LiGoldragon/horizon-rs/lib/src/{species,machine,node}.rs`,
  `/git/github.com/LiGoldragon/CriomOS/modules/nixos/{nix.nix,criomos.nix,network/tailscale.nix,network/headscale.nix}`,
  `/git/github.com/LiGoldragon/lojix-cli/src/{request,deploy}.rs`,
  `/git/github.com/LiGoldragon/lojix-cli/Cargo.toml`,
  `/git/github.com/LiGoldragon/lojix-cli/skills.md`.
- Designer-assistant report 27:
  `/home/li/primary/reports/designer-assistant/27-dedicated-cloud-host-and-contained-node-research.md`.
- Designer-assistant report 26:
  `/home/li/primary/reports/designer-assistant/26-criomos-cloud-infrastructure-survey.md`.
- Coordination protocol and lock semantics:
  `/home/li/primary/protocols/orchestration.md`,
  `/home/li/primary/skills/system-assistant.md`,
  `/home/li/primary/system-specialist.lock`.
- Open beads: `bd ready --label role:system-specialist` at write
  time — `primary-q3y` (kameo migration), `primary-tpd`
  (Tailscale/Headscale review).
- External docs (cited via designer-27): NixOS containers manual,
  `systemd-nspawn(1)`, MicroVM.nix host module docs, Ghost install /
  Docker / Node / database compatibility pages.
