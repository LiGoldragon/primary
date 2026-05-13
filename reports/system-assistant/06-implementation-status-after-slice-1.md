# 06 — Implementation status: after kameo-collapse + P1 slice 1

Date: 2026-05-12
Role: system-assistant
Tracks: `reports/system-assistant/04-...` and `05-...`
Beads: primary-q3y, primary-a70

## What landed this pass

Two pieces shipped to their auto-push bookmarks (not yet on main —
awaiting review):

| Bead | Repo | Bookmark | Status |
|---|---|---|---|
| primary-q3y (kameo migration) | lojix-cli | `push-ovulwxnnpykv` | tests pass (49/49), ractor removed |
| primary-a70 P1 slice 1 (types) | horizon-rs | `push-oowpqtrszouq` | cargo check + tests pass (107/107) |

### kameo migration (primary-q3y)

The bead description hinted at the right answer: "collapse
actor-shaped wrappers into methods on data-bearing nouns." All six
"actors" in lojix-cli (`ProposalReader`, `HorizonProjector`,
`HorizonArtifact`, `NixBuilder`, `ClosureCopier`, `Activator`) were
ZST one-shot wrappers around methods that already existed on data
nouns. The collapse is delete-not-port: actor types and `Msg`
enums removed; `DeployCoordinator`/`DeployState`/`ActorCallResult`
replaced by `pub async fn deploy(req) -> Result<DeployOutcome>` in
`deploy.rs`; `main.rs` calls it directly; `ractor` dependency
removed; three unused error variants
(`Ractor`/`ActorRpcFailed`/`ActorMessagingFailed`) removed;
`proposal.rs` deleted entirely (held only the actor; the data
noun lives in `cluster.rs`).

This unblocks primary-sff (P5 lojix-core extraction).

### P1 slice 1 — types-exist milestone

Three new modules in `horizon-rs/lib/src/`:

- `placement.rs` — `NodePlacement` (Metal | Contained),
  `ContainmentSubstrate` (NixosContainer | MicroVm only; no
  `WorkloadSubstrate` per report 05), `ContainedPlacement` with
  typed `UserNamespacePolicy`
  (`PrivateUsersPick | HostRootMappingAllowed { reason, approved_by }`),
  supporting types for resources / network / state.
- `capability.rs` — `NodeCapabilities` (with derived
  `is_infrastructure_host()` method replacing the deleted marker),
  `BuildHost`, `BinaryCache` (with `BinaryCacheEndpoint` carrying
  scheme + host + port + path_prefix + public_key), `PublicDomain`
  (Criome | External), `ContainerHost` (with `BridgePolicy.bridge_name`
  and projected `children`), `PublicEndpoint`, `CacheRetentionPolicy`.
- `secret.rs` — `SecretReference { name, purpose }` (logical
  reference; cluster-level binding holds backend choice),
  `SecretName` newtype, `SecretPurpose` closed-set enum.

`lib.rs` registers the three new modules.

**Intentional omission**: `NotaRecord` / `NotaEnum` derives are
left off these types until they are wired into a proposal record.
Sum types with data variants (`NodePlacement`,
`UserNamespacePolicy`, `PublicDomain`) need hand-written
`NotaEncode/NotaDecode` impls following the `LojixRequest`
pattern; those land in the slice that adds `placement` to
`NodeProposal`. Newtypes use `NotaTransparent` (matches the
existing `NodeName`/`CriomeDomainName` pattern in
`name.rs`).

No existing types modified. No tests modified. All 107 horizon-rs
tests still pass.

## What didn't land — and why

### P1 slice 2 (wire types into `Node`)

Slice 2 would add `placement` and `capabilities` fields to `Node`
and derive them in `NodeProposal::project`. Two reasons I stopped
short:

1. **System-specialist active on `horizon.rs` + `error.rs`** —
   `validate singleton tailnet controller`. Node-side changes
   could collide if their work expands into `node.rs`.
2. **Legacy Pod migration needs a design call.** Existing Pod
   proposals have `machine.species = Pod` plus `cores` / `ram_gb`,
   but no `ContainerNetwork` (localAddress/hostAddress) or
   `ContainerState`. To shim them into `ContainedPlacement` the
   options are (a) make `ContainerNetwork`/`ContainerState` fields
   `Option` on `ContainedPlacement`, (b) emit placeholder
   addresses, or (c) keep `Machine`-backed nodes on a separate code
   path. The clean answer probably involves splitting the migration
   into "legacy Pod renders as `Contained` with structural
   defaults" vs "new proposals author placement directly", and
   that needs a designer pass.

Both reasons argue for slice 2 to land after a coordination beat.

### P5 (lojix-core extraction)

primary-sff is unblocked in principle (q3y is done) but should not
start until q3y is merged to main. Otherwise the crate split
re-introduces the kameo migration's deleted code.

### P2/P3/P4/P6

P2 is in active progress by system-specialist (CriomOS module
split). P3/P4/P6 chain off P1 slice 2 + P2 completion.

## Where the locks stand

- `system-assistant.lock`: empty (released after each slice).
- `system-specialist.lock`: file-scoped on horizon.rs/error.rs/tests
  for the tailnet-controller work; file-scoped on CriomOS modules
  for P2.
- `operator.lock`: persona contract pins (unrelated repo).

The file-scoped locks the user requested are now in place on both
sides — the broad-repo locks from earlier in this session have
been narrowed.

## Next-up beads for this implementation

In dependency order:

1. **P1 slice 2** (no bead yet — extends primary-a70). Add
   `placement` + `capabilities` fields to `Node`; derive in
   `NodeProposal::project`; resolve legacy Pod migration shape.
   Waits for system-specialist's horizon.rs lock to release.
2. **P1 slice 3** (extends primary-a70). Add `placement` to
   `NodeProposal`; write hand-written
   `NotaEncode/NotaDecode` for sum-with-data enums; dual-authority
   validation (`Error::ConflictingPlacementAuthority` /
   `Error::MissingPlacement` / `Error::PodWithoutHost`); add
   `NodeSpecies::Publication`.
4. **P1 slice 4** (extends primary-a70). Add `Horizon.contained_nodes`,
   `ProjectedNodeView`, `ContainedNodeView`,
   `HostPublicEndpointRoute` derivations.
5. **P2 completion** (primary-7zz, in-progress by system-specialist).
6. **P3** (primary-9wi), **P4** (primary-hpx), **P5** (primary-sff
   after q3y merges), **P6** (primary-5u9).

## Sources

- `reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md` — the plan.
- `reports/system-assistant/05-workload-decision-native-and-workloadsubstrate-removed.md` — the workload rule.
- `skills/nix-discipline.md` §"Services are NixOS modules, not OCI workloads".
- Pushed branches:
  `github.com/LiGoldragon/lojix-cli/push-ovulwxnnpykv`,
  `github.com/LiGoldragon/horizon-rs/push-oowpqtrszouq`.
