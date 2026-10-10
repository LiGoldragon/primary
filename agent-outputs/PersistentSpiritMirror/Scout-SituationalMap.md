# Scout Situational Map — Persistent Two-VM Spirit A→B Mirror over the Criome Propagation Path

## Task and scope

Map the concrete ground truth a weaver needs to plan this slice: two **persistent**
VMs on host `prometheus`, defined in cluster data (horizon projection) with support
in `horizon-rs` and CriomOS; Spirit as the pilot component; goal = Spirit state
created on node A mirrors one-directionally to node B, carried over the Criome
daemon's auto-authenticated propagation path, persisting across runs (real
deployment, not an ephemeral test).

Read-only mapping pass. No target repos were edited or built. Facts are separated
from interpretation; unknowns and blockers are named. Prior-scout givens
(`CriomOS-test-cluster`/`runNixOSTest`, `lojix-deploy-smoke`, ephemeral VMs lack
persistence, Spirit "gate-config arming", prometheus-only Rust builds) were taken
as established and deepened.

## Correction (2026-07-03): goldragon is PUBLIC — supersedes every "private / authorization-gated" note below

The `goldragon` cluster-facts repo (`github:LiGoldragon/goldragon`) is **public
and safe to edit** (confirmed 2026-07-03; its README/ARCHITECTURE state so).
`datom.nota` carries only references to SOPS-encrypted secrets. Every mention
below of "private `goldragon`", "authorization-gated", or "not authorized to
open it" is **void** — the facts were read and the two guests (`mirror-alpha`
5::7/128, `mirror-beta` 5::8/128) authored + pushed (goldragon main
`824ffe6498c3`). One map claim was also revised by later ground truth: the guest
network model in Area 1/kink-1 is confirmed — the CriomOS `/128` host-route fix
(landed CriomOS main `4f7953ebbbff`) is necessary but NOT sufficient; guests
still boot network-dark. See `OperatingSystemImplementer-DeployEvidence.md`.

## Sources consulted (paths + commands)

- Repo inventory: `protocols/repos-manifest.nota`, `protocols/active-repositories.md`,
  `ghq list`. All target repos are checked out under `/git/github.com/LiGoldragon/<name>`
  (and `/git/github.com/Criome/<name>`); the `repos/` and `private-repos/` dirs are empty.
- Prior reports (givens): `reports/field-readiness/10-vm-cluster-probe.md`,
  `reports/field-readiness/11-build-readiness.md`,
  `reports/capacityAdmissionSlice/5-Kickoff-make-vm-testing-infra-real.md`,
  `agent-outputs/CapacityAdmissionSlice/CriomosImplementer-T2CriomeModuleEvidence.md`,
  `agent-outputs/CriomeAuthWitnessFullBody/CriomosImplementer-WitnessRunEvidence-v3.md`.
- Live horizon projection on this host (owner-readable):
  `/var/lib/lojix/generated-inputs/goldragon/{ouranos,zeus,prometheus}/…/horizon/horizon.json`
  (queried for schema shape only via `jq`; key material omitted).
- The load-bearing test source read directly:
  `/git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkCriomeAuthWitnessTest.nix` (591 lines).
- Deep source reads delegated to four read-only Explore sub-agents (horizon projection,
  criome daemon, spirit, propagation/mirror). Their symbol-level findings are marked
  "(sub-agent)"; anything I opened myself is unmarked.
- `git -C <repo>` status/rev checks on spirit, criome, mirror, router, CriomOS,
  CriomOS-test-cluster.

Not consulted / out of scope: the private `goldragon` cluster-facts repo authored
source (this brief does not authorize opening it; prior kickoff report 5 treats it
as authorization-gated). The `secrets/` projections were not read. No Spirit intent
records were queried (mechanical mapping).

## Terminology / repo map (observed)

| Concept | Repo / path |
|---|---|
| Authored pan-horizon config (LiGoldragon personal) | `/git/github.com/LiGoldragon/criomos-horizon-config/horizon.nota` (12 lines, stub — no nodes/VMs) |
| Authored **goldragon cluster** facts (declares prometheus + its VMs) | private `goldragon` repo (`protocols/repos-manifest.nota:184`, `Data Active`, Family Content) — NOT read |
| Horizon projector (NOTA cluster facts → per-node JSON) | `/git/github.com/LiGoldragon/horizon-rs` |
| Projected per-node horizon | `/var/lib/lojix/generated-inputs/<cluster>/<node>/<variant>/horizon/horizon.json` |
| OS layer that hosts guests / runs daemons | `/git/github.com/LiGoldragon/CriomOS` (`modules/nixos/`) |
| VM test harness (runNixOSTest) | `/git/github.com/LiGoldragon/CriomOS-test-cluster` |
| Pilot component | `/git/github.com/LiGoldragon/spirit` (+ `signal-spirit`, `meta-signal-spirit`) |
| Auth daemon | `/git/github.com/LiGoldragon/criome` (+ `signal-criome`, `meta-signal-criome`) |
| Mirror receiver | `/git/github.com/LiGoldragon/mirror` (+ `signal-mirror`) |
| Cross-node forward transport | `/git/github.com/LiGoldragon/router` (persona-router) |

Note: the prior scout's name `mkCriomeClusterTest` is not a current file. The current
file is `lib/mkCriomeAuthWitnessTest.nix`; its own comment calls `mkCriomeClusterTest`
a **precedent** (the throwaway-root-guest pattern), and the "Stage A/B" language is
criome's (see Area 3), not a filename.

## THE ONE FACT THAT DOMINATES THE SLICE

The cross-node "spirit → criome → router → mirror" chain that the field probe
witnessed **does not exist as a production path** — the two-VM test *composes* it.
Verbatim from `mkCriomeAuthWitnessTest.nix` header (lines 13-40):

> "spirit ships head DIRECTLY to a mirror and the router only fans out a typed
> reference, so the recorded 'spirit -> criome -> router -> mirror' is composed
> here from the REAL mechanisms … The sender leg is the router-forward-witness bin
> rather than a router daemon outbound forward, because **no router daemon ingress
> attaches a RoutedContractObject to an OUTBOUND message (a real code limitation)**;
> the bin uses the router's OWN production CriomeForwardAttestation, so every
> signature/verification is real."

So: the criome **auth gate** (accept vs refuse a forward by registered matching key)
and the mirror **durable landing** are real and proven. The **sender leg** that would
autonomously ship a Spirit body from A to B is a test binary (`router-forward-witness`),
not a standing daemon. This is the largest build gap in the slice.

## Area 1 — Cluster data / horizon projection: two persistent VMs on prometheus

### OBSERVED
- **Schema shape (projected).** A projected node horizon is JSON with an `exNodes.<name>`
  map. A VM guest node has: `species: "TestVm"`, `machine: { species: "Pod", cores,
  ramGb, diskGb, superNode: "<host>", … }`, `nodeIp`, `services`, `criomeDomainName`,
  per-node pubkeys, and `behavesAs: { virtualMachine: true, testVm: true, … }`.
  Verified against the live prometheus projection and the public fixture
  `CriomOS-test-cluster/fixtures/horizon/*.json` (the brief's `fixtures/horizon/<node>.json`).
- **Precedent for a persistent VM on prometheus EXISTS.** The live projection
  `/var/lib/lojix/generated-inputs/goldragon/prometheus/full-os/horizon/horizon.json`
  already declares `exNodes["vm-testing"]`: `species TestVm`, `machine.species Pod`,
  `cores 4`, `ramGb 8`, `diskGb 40`, `superNode "prometheus"`, `nodeIp "5::6/128"`,
  `behavesAs.testVm true`, `criomeDomainName "vm-testing.goldragon.criome"`. Prometheus
  itself declares host capacity `(VmHost 169.254.100.0/22 Available 4)` (field probe 10).
- **Authored source of a node/VM (sub-agent, public example).** In the test cluster,
  nodes are authored in `CriomOS-test-cluster/clusters/fieldlab.nota` as
  `NodeProposal` records (e.g. `mercury (TestVm …)`); a host declares
  `(VmHost <guestSubnet> <kvm> <maximumGuests>)` in its service list. Projector types:
  `horizon-rs/lib/src/proposal.rs` (`NodeService::VmHost { guest_subnet, kvm,
  maximum_guests }`), `species.rs` (`NodeSpecies::TestVm`), `machine.rs`
  (`MachineSpecies::Pod`, `super_node`), `node.rs` (`BehavesAs::test_vm`).
- **What "persistent" means at the storage layer (sub-agent, verified module exists).**
  `CriomOS/modules/nixos/test-vm-host.nix` discovers guests where
  `machine.superNode == thisNode && behavesAs.testVm`, emits `microvm@<guest>.service`,
  and gives each a host-side disk image `/var/lib/microvms/<guest>/root.img`
  (`autoCreate = true`, size = `diskGb`, ext4). The image lives on the host filesystem
  (outside `/nix/store`), so it survives guest reboots. `autostart = false` (started on
  demand). This is the deployed path on prometheus.
- **A second, older module** `CriomOS/modules/nixos/vm-testing/default.nix` (`VmTesting`
  service, libvirt/Spice, single persistent routed VM) exists but is **NOT deployed** on
  prometheus (field probe 10: prometheus carries `VmHost`, not `VmTesting`, and has no
  libvirt). Treat it as superseded.

### INTERPRETATION
- Defining **two persistent VMs on prometheus** means authoring two `TestVm`/`Pod`
  guest nodes with `superNode: prometheus` in the goldragon cluster facts, projecting,
  and redeploying prometheus's system. `test-vm-host.nix` then emits `microvm@vm-a` and
  `microvm@vm-b`, each with its own persistent `root.img`. Persistence across runs is
  already provided by the host-side image + NixOS `stateVersion`; no new storage
  mechanism is needed for OS/daemon state.
- The declared-guest path is **heavyweight**: each added guest is a cluster-facts edit +
  re-projection + prometheus system redeploy (field probe kink 6), versus zero host
  changes for ephemeral runNixOSTest guests.
- The existing `vm-testing` guest is the precedent but is **network-dark and
  un-enterable** as declared (field probe kink 1: guest gets no in-guest address, no
  sshd, IPv4/IPv6 family mismatch in the tap route). A **standing, reachable** A/B pair
  needs the guest-side network fix from kink 1 before the mirror can even be driven
  across the two guests. This is a real prerequisite, not cosmetic.

### UNKNOWNS
- Whether prometheus's two mirror-slice guests should be authored in the **private
  goldragon** facts (authorization-gated) or added to the **public** `CriomOS-test-cluster`
  fixtures. The public cluster has no prometheus node today (sub-agent); the live private
  cluster does. This is a psyche/authorization decision (see Real-world conditions).
- Whether one host can host declared `TestVm` guests **and** run the persona-router/mirror
  daemons for the slice simultaneously under the current module gating (Area 5).

## Area 2 — horizon-rs and CriomOS supporting infra

### OBSERVED
- **horizon-rs** is the projector: authored `HorizonProposal`/`NodeProposal` NOTA →
  typed `Node` → per-node `horizon.json`. VM-hosting is entirely **cluster-data-generated**
  (sub-agent: `horizon-rs/ARCHITECTURE.md`), i.e. adding a guest is a data edit, not a
  code change. Relevant types in `horizon-rs/lib/src/{proposal,species,machine,node}.rs`
  (sub-agent).
- **CriomOS** hosts guests and daemons. Modules present and directly observed in
  `CriomOS/modules/nixos/`: `test-vm-host.nix` (emits microvm guests from cluster data),
  `test-vm-guest.nix`, `vm-testing/` (superseded), `criome.nix`, `criome-node-test.nix`,
  `criome-auth-integrated-test.nix`, `persona-router.nix`, `mirror.nix`, `router/`.
- The horizon projection reaches the host through **lojix**: authored facts →
  `/var/lib/lojix/generated-inputs/<cluster>/<node>/<variant>/{system,horizon,deployment,secrets}`
  → CriomOS system build (field probe 11 gives the working `--override-input` recipe).

### INTERPRETATION
- The supporting infra for "define + host a standing guest on prometheus" is **already
  built and deployed** (microvm.nix via `test-vm-host.nix`), minus the kink-1 guest-network
  defect. No horizon-rs code change is required to add two guests; only cluster data +
  redeploy.

### UNKNOWNS
- Exact prometheus host descriptor (cores/RAM/disk in the authored facts) — lives in the
  private cluster facts; the machine's live capacity (32 threads, 124 GiB RAM, 913 GB free)
  is known from field probe 10 and is ample for two 8 GB guests.

## Area 3 — Criome daemon auth (+ BLS witness/quorum)

### OBSERVED (sub-agent, symbol-level; corroborated by prior T2 evidence)
- **Daemon**: `criome/src/daemon.rs` (`CriomeDaemon::run()`); working socket + `<socket>.meta`
  (owner-only, 0600, SO_PEERCRED-enforced per criome HEAD commit `b4af86d`); SEMA store with
  tables `criome-identity`, `criome-attestation`, `criome-authorization-state`,
  `criome-signature-solicitation`, `criome-submitted-signature`.
- **Config** (`signal-criome` `CriomeDaemonConfiguration`, 6 positional fields):
  `socket_path, store_path, meta_socket_path?, cluster_root: Option<BlsPublicKey>,
  authorization_mode: AuthorizationMode (Quorum | AutoApprove | ClientApproval),
  node_identity: Option<Identity>` (defaults `Host("criome")`; distinct per node in a cluster).
  This matches the witness config line
  `(CriomeConfigurationArtifact (<sock> <store> (Some <meta>) None Quorum (Some (Host <identity>))) <out>)`
  observed in `mkCriomeAuthWitnessTest.nix:107`.
- **Master key**: `criome/src/master_key.rs` — BLS12-381 MinPk secret key from `/dev/urandom`,
  persisted `{store_path}.masterkey` atomically at mode 0600 (rejects symlink/group/other bits);
  signs with a domain-separation tag.
- **Identity registration** (`actors/registry.rs`, `admission.rs`): registering an *external*
  identity requires a `cluster_root` BLS signature over a domain-separated `RegistrationStatement`;
  the daemon **self-registers its own node identity** on first startup (bypassing the cluster-root
  gate) with `KeyPurpose::CriomeRoot`, and on restart verifies the stored key matches its master key.
- **Verification flow** (`actors/verifier.rs`): `AttestationVerifier::verify()` → resolve signer
  identity in registry → check status (reject Revoked) → require registered public key == presented
  key → require `Bls12_381MinPk` scheme → verify BLS signature over domain-separated preimage →
  expiry check. Returns `Valid | InvalidSignature | UnknownSigner | Revoked | Expired`.
- **BLS witness / quorum**: **Stage A (1-of-1) is implemented** — `criome/src/bin/criome-cluster-witness-test.rs`
  proves `Rule::Threshold(k=1)` authorizes with one valid signature and rejects with zero.
  Threshold policy evaluation exists in `criome/src/language.rs`; routing messages
  (`SignatureSolicitationRoute`, `SignatureSubmission`) exist in `actors/authorization.rs`.
  **Stage B (multi-node quorum) is designed but incomplete**: per criome `ARCHITECTURE.md §6.1`,
  the **cross-host wire crypto is an open design slot** (TLS vs signed envelopes vs SSH) and there is
  **no cross-node quorum test**.

### INTERPRETATION
- "Auto-authenticate" for this slice = the **Stage A** shape, and it already works: each node runs
  its own criome (own master key, own identity, own store); node B **pre-registers** node A's
  `Host(node-a)` identity → node A's public key; thereafter every forward node A signs is
  verified deterministically with no human in the loop. The witness proves exactly this: the *only*
  difference between refuse and accept is a correctly-registered matching key on criome B.
- The slice does **not** need Stage B multi-node quorum. It needs Stage-A pairwise trust:
  a one-time registration of A's identity into B's criome, plus each node's criome standing up
  with a durable master key and identity.

### UNKNOWNS
- How node B's registration of node A is **provisioned at deploy time**. The witness registers A
  into B mid-test via `RegisterIdentity`. A standing deployment needs a deploy-time seed. Prior T2
  evidence (`CriomosImplementer-T2CriomeModuleEvidence.md`) shows `CriomOS/modules/nixos/criome.nix`
  already carries an `ExecStartPost` "peer-identity seed hook" / "cross-instance identity-seed hook" —
  but that module is on a **branch, not landed on main**, and the exact seed input format/authority
  is unconfirmed. This is the concrete "arm criome for A→B trust" work item.

## Area 4 — Spirit: state store, gate-config arming, mirror hook

### OBSERVED (sub-agent, symbol-level)
- **Store**: `spirit/src/store/mod.rs` over `sema-engine` (`SemaDatabase` at `<path>.sema`).
  Records are a versioned commit log; **head** = `EntryDigest` (blake3, 32 bytes, hex);
  **body** = rkyv bytes of `VersionedCommitLogEntry`. `versioned_log_head()` returns the digest;
  `versioned_log_head_object()` returns the head entry body. (Prior v3 evidence: body was 320 octets,
  head `326640ac…`.)
- **Sockets**: working `socket_path` + owner-only `meta_socket_path` (`spirit/src/schema/daemon.rs`);
  daemon in `spirit/src/daemon.rs`.
- **Ordinary ops** (`signal-spirit`): Record, Propose, Clarify, Supersede, Retire, Observe, Lookup…
- **Meta ops** (`meta-signal-spirit`): `Configure`, `Import`, `ObserveHead`, `ObserveHeadObject`,
  `CollectRemovalCandidates`.
- **"Gate-config arming" is concrete** (this is the clearest single answer): spirit has a local
  criome authorization gate (`spirit/src/criome_gate.rs`). It is armed via the meta `Configure`
  op setting `criome_gate_target: CriomeGateTarget::Socket(<criome.sock path>)`
  (`meta-signal-spirit/src/schema/meta_signal.rs`, `CriomeGateTarget { Default | Socket(...) }`).
  Engine path: `engine.configure()` → `criome_gate.configure_socket(path)` → `arm(...)`.
  **When unarmed, the gate holds every head back — no head ships.** When armed, every post-commit
  head does a real criome authorization round-trip before fan-out. `Configure` also sets a **mirror
  target** and archive location.
- **Source-side ship hook**: `engine.gate_and_ship_head()` captures the head
  (`LocalHeadCapture::spirit_head`), calls `criome_gate.authorize_head(...)`, and only if
  `decision.ships()` calls `self.mirror_shipper.ship_unshipped()` (`spirit/src/shipper.rs`,
  `mirror::ComponentShipper::ship_unshipped()`).
- **Destination-side import hook**: meta `Import` (`engine.import()`) appends each `ImportedRecord`
  (`record_identifier` + full `VersionedCommitLogEntry` entry) via `nexus.store().import_record(...)`;
  meta `ObserveHead` re-reads the head for re-hash verification.

### INTERPRETATION
- The A→B mirror hooks are already present in spirit code: **source** = the armed criome gate +
  `mirror_shipper.ship_unshipped()`; **destination** = meta `Import` + `ObserveHead` re-hash.
  The remaining Spirit work is **configuration/deployment**, not new engine logic: arm the gate
  on A (Configure→Socket) and point the mirror target at the transport that reaches B.
- The prior witness seeds records on A via **owner-only meta `Import`** (which bypasses the guardian),
  because the guardian-compiled spirit refuses ordinary `Record` with no agent configured
  (`ReferentGuardianRejected … guardian is required but no guardian agent is configured`, v3 L3).
  So "state created on node A" in the current proof is meta-imported, not organically Recorded.
  A real deployment must decide whether A accepts ordinary Records (needs a guardian agent) or
  whether seeding via meta Import is acceptable for the slice.

### UNKNOWNS / STATE
- **spirit checkout is DIRTY and on a detached HEAD** (directly observed: HEAD `11452d6`, 9 modified
  files incl. `Cargo.lock`, `Cargo.toml`, `flake.lock`, `src/engine.rs`, `src/store/mod.rs`,
  `src/production_migration.rs`, three tests). Field probe 11 saw it on `criome-authorization-push`;
  it has since moved. **Disposition needed before the slice builds from a clean rev.** (criome, mirror,
  router, CriomOS, CriomOS-test-cluster were all clean at their heads.)
- Whether `mirror_shipper` ships to a **local** mirror only (see Area 5) — this is the pivot that
  decides how much new transport the slice needs.
- No meta query exposes "is the gate armed" (sub-agent found `criome_gate_armed()` but not surfaced).

## Area 5 — Propagation / transport (the "criome propagation path")

### OBSERVED
- **Standing daemon modules already exist and are boot-proven** (directly verified they exist;
  gating verified by reading the modules):
  - `CriomOS/modules/nixos/mirror.nix` — gated on services `TailnetClient && PersonaDevelopment`;
    runs `mirror` daemon as `mirror:mirror`; working socket `/run/mirror/working.sock` (0660),
    meta `/run/mirror/meta.sock`, store `/var/lib/mirror/mirror.sema`, TCP `0.0.0.0:7474`;
    hardened unit.
  - `CriomOS/modules/nixos/persona-router.nix` — gated on service `PersonaRouter`; runs
    `persona-router` daemon; listen `0.0.0.0:7440` (configurable via the `PersonaRouter` service
    payload); joins the `criome` group to dial `/run/criome/criome.sock`; applies a startup
    **bootstrap** doc `/run/persona-router/bootstrap.rkyv` (peers + actor-homes + grants) authored
    from NOTA at deploy time; hardened unit.
  - `CriomOS/modules/nixos/criome.nix` + `criome-auth-integrated-test.nix` — hardened per-user
    criome with both 0600 sockets, boot-proven (from the test-cluster caveat comment and T2 evidence).
- **What is REAL vs COMPOSED** (from the `mkCriomeAuthWitnessTest.nix` header, read directly, and
  sub-agent corroboration):
  - REAL and proven: criome attestation **sign** (`CriomeForwardAttestation` on A) and **verify**
    (node B's persona-router dials B's criome, `VerifyAttestation`, `Valid`→`ForwardAccepted`,
    `UnknownSigner`/`InvalidSignature`→`ForwardRefused(AttestationInvalid)`); the router→mirror
    ComponentSocket delivery gated by an `(operator mirror)` bootstrap grant; the mirror's durable
    `Append` (redb commit == ack) and `ObserveHeads` read-back.
  - COMPOSED / NOT PRODUCTION: the **sender leg**. In production "spirit ships head DIRECTLY to a
    mirror and the router only fans out a **typed reference**" (not the body). The test fabricates the
    body-carrying sender with the `router-forward-witness` bin because **"no router daemon ingress
    attaches a RoutedContractObject to an OUTBOUND message (a real code limitation)."** The bin uses
    the router's own production attestation code, so the crypto is real; the *daemon that would
    autonomously forward a Spirit body A→B does not exist.*
- **Transport concretely**: TCP length-prefixed `signal-router::ForwardMessage` from A to
  `node-b:7440`; payload is a `RoutedContractObject` wrapping a `signal-mirror::Append` (genesis
  entry carrying the head digest + real body); node B relays to mirror `working.sock`.

### INTERPRETATION
- The receiver half of a standing A→B mirror is **essentially deployable today**: node B needs
  persona-router (`PersonaRouter` service) + criome + mirror (`TailnetClient` + `PersonaDevelopment`)
  modules, a bootstrap doc naming A as a peer and mirror as the actor-home with the `(operator mirror)`
  grant, and B's criome pre-seeded with A's identity.
- The **sender half is the real build gap**. Options (sub-agent): (a) deploy a standing shipper
  service on A modeled on `router-forward-witness` (uses production `CriomeForwardAttestation`), or
  (b) add a router-daemon outbound ingress that accepts a `RoutedContractObject` and forwards it.
  Either is net-new standing code, not just config.
- Two other deploy-time gaps: **receiver store pre-registration** (the test calls
  `meta-mirror RegisterStore spirit`; no standing mechanism seeds the mirror's store row), and
  **bootstrap generation from deploy config** (the test hand-writes the bootstrap NOTA; a standing
  deploy must generate peers/actor-homes/grants from node config, incl. the mirror socket path).

### UNKNOWNS
- Whether spirit's `mirror_shipper` (Area 4) can be pointed at a **remote** mirror/router directly,
  which would let A ship without a separate shipper daemon. The header comment implies spirit ships to
  a *co-resident* mirror and the router only fans references — i.e. spirit-direct-to-remote is not the
  designed path — but this was not confirmed at the code level. **This is the single most important
  design question for the weaver** (it determines whether the sender leg is "configure spirit's mirror
  target at B" or "build a standing shipper/router-forward daemon").
- Whether the `router-forward-witness` bin is packaged in a way a standing service could reuse, or is
  test-only.

## Area 6 — Constraints and real-world conditions the psyche must satisfy

### OBSERVED / establishing facts
- **prometheus is the only VM-test + build host** and it works: real KVM, 32 threads, 124 GiB RAM,
  913 GB free; `runNixOSTest` two-VM slices boot and pass in ~100 s; reachable at
  `ssh root@prometheus.goldragon.criome` with key auth (field probe 10). No account/spend/physical
  action is required to run VM clusters there.
- **VM tests must run ON prometheus, not ouranos** (the orchestrator laptop). ouranos is forbidden to
  fire QEMU and its `/etc/nix/machines` advertises `big-parallel,kvm` but **not `nixos-test`**, so VM
  drivers cannot be remote-scheduled to prometheus — you must `ssh root@prometheus … nix run/build`
  (field probe kinks 2, 5). Iteration is **push-first**: prometheus runs from `github:` refs; local-path
  flakes do not travel, so every fixture edit must be pushed before prometheus sees it.
- **Rust builds go through prometheus** (local `max-jobs=1`); component daemons build warm in 6–110 s;
  a per-edit floor is ~24 s for one daemon (field probe 11).
- **A latent build bomb**: persona's fenix rust-stable pin (2026-05-05) has a stale FOD;
  `persona-dev-stack` and the whole-engine topology checks fail to instantiate. The slice's components
  (spirit, criome, mirror, router, CriomOS) build fine individually today; but any surface that pulls
  persona's dev-stack toolchain will hit this (field probe 11 K1/K2).
- **Secrets/keys the auth path needs**: each node's criome mints and persists its **own BLS master key**
  at `<store_path>.masterkey` (0600) — generated on first boot, not a human-provided secret. Per-node
  ssh/nix/ygg/wireguard pubkeys are authored in the (private) cluster facts and projected. The one
  human-shaped secret decision is trust seeding: node B must be given node A's **identity/public key**
  at deploy time (Area 3 unknown).

### REAL-WORLD CONDITIONS the psyche/human must satisfy (interpretation)
1. **Authorize + author the two prometheus guests.** Decide whether the two persistent VMs (node A,
   node B) are authored in the **private goldragon** cluster facts (authorization-gated — this scout
   was not authorized to open it) or added to the **public** test-cluster. Then author two
   `TestVm`/`Pod` guests with `superNode: prometheus`, project, and **redeploy prometheus's system**
   (a real host mutation).
2. **Fix the guest-network defect (kink 1)** if the two VMs must be *reachable/standing* (not just
   booted): declared guests today are network-dark and un-enterable. This is a CriomOS
   `test-vm-host.nix` change + cluster-facts decision + prometheus redeploy. (If the slice runs the
   A→B mirror **inside a single runNixOSTest** with two guests instead of two standing microvms, this
   defect is avoided — but that is an ephemeral test, not the "persists across runs, real deployment"
   the slice asks for. The weaver must pick.)
3. **Disposition the dirty spirit checkout** (9 modified files, detached HEAD) so the slice builds
   from a clean pushed rev.
4. **Accept the prometheus-only, push-first loop**: fixture edits pushed to GitHub, tests fired via
   `ssh root@prometheus … nix run github:…`.
5. **Provide the A→B trust seed**: confirm how node B's criome is given node A's identity+public key
   at deploy time (the `criome.nix` peer-seed hook is on a branch, not landed).

## Consolidated UNKNOWNS / BLOCKERS

- **B1 (design, biggest).** Is the sender leg "point spirit's `mirror_shipper` mirror-target at node B"
  or "build a standing shipper / router-outbound-forward daemon"? The test's header says spirit ships
  to a *co-resident* mirror and the router fans out only a typed reference, and that no router daemon
  attaches a routed object to an outbound message — implying new standing code is required. Not
  code-confirmed whether spirit-direct-to-remote is possible. **Resolve before planning the slice.**
- **B2 (build gap).** No production standing daemon carries a Spirit body A→B; the proof uses the
  `router-forward-witness` test bin. Receiver-side modules (persona-router, mirror, criome) exist and
  are boot-proven; the sender-side standing path does not exist.
- **B3 (deploy plumbing).** Standing A→B needs, at deploy time: (a) node B criome pre-seeded with node
  A's identity/key; (b) mirror store row pre-registered for `spirit`; (c) persona-router bootstrap
  (peers + mirror actor-home + `(operator mirror)` grant) generated from node config. All three are
  hand-done in the test today.
- **B4 (host/data).** Two persistent guests on prometheus require authoring in cluster facts + a
  prometheus redeploy; the standing/reachable variant additionally requires the kink-1 guest-network
  fix. The authoritative facts likely live in the private `goldragon` repo (authorization-gated).
- **B5 (Spirit semantics).** In the current proof, "state created on A" is owner-only meta `Import`
  (guardian bypass); ordinary `Record` is fail-closed without a guardian agent. Decide whether the
  slice seeds A via meta Import or arms a guardian for organic Records.
- **B6 (Stage-B not needed but noted).** Cross-node BLS **quorum** (Stage B) is unbuilt (open crypto
  slot). The slice only needs Stage-A pairwise trust, so this is not a blocker — but do not scope the
  slice as needing quorum.
- **B7 (checkout hygiene).** spirit dirty + detached (B2 of git state); latent persona fenix FOD bomb
  (field probe 11) if the slice pulls the persona dev-stack toolchain.

## What was NOT checked / weak evidence
- The private `goldragon` cluster-facts source (authorization-gated; not opened). Prometheus's exact
  host descriptor and its two-guest authoring surface are therefore inferred from the public schema +
  the live projection's shape, not from authored source.
- Sub-agent symbol-level claims for `horizon-rs`, `criome`, `spirit`, `router`, and `mirror` internals
  were not each independently reopened by me; I verified the load-bearing ones (test header, module
  gating, live projection schema, git states, spirit gate-config field name via the sub-agent's cited
  path `meta-signal-spirit/src/schema/meta_signal.rs`). Finer method/line numbers marked "(sub-agent)".
- No build or VM run was executed this pass (mapping only). No Spirit intent records were queried.
