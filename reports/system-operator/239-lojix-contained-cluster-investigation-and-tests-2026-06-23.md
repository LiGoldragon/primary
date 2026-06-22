# Lojix Contained Cluster Investigation And Tests

Date: 2026-06-23
Role: system-operator

## Question

Can lojix now deploy test VM clusters?

Answer: no. Lojix can accept and verify per-node contained runs on the ordinary signal face, and the POC test surface can express a compact criome/spirit/router cluster as client-side expansion into multiple `DeployContained` requests. It does not yet have a daemon-owned `RunContainedCluster` root, a persisted cluster aggregate, a co-live barrier, or working `VmHostGuest` substrate execution.

## Tested

### Lojix POC branch

Worktree:

`/home/li/wt/github.com/LiGoldragon/lojix/system-operator-contained-test-poc`

Command:

```sh
cargo test --test test_op
```

Result: passed, 5/5.

Covered:

- `deploy_contained_is_ordinary_and_records_pending_run`
- `check_and_release_use_the_contained_run_handle`
- `verify_contained_steps_fail_closed_when_gate_case_is_not_1_of_1`
- `non_hermetic_targets_are_typed_rejections_in_the_poc`
- `criome_spirit_router_cluster_interface_is_compact`

Command:

```sh
cargo test --features nota-text
```

Result: passed all non-ignored tests. The run covered 71 passing tests across unit and integration suites. Six external/slow tests remained intentionally ignored, including real Nix eval/build and daemon socket smoke tests.

### Spirit criome gate witness

Worktree:

`/home/li/wt/github.com/LiGoldragon/spirit/schema-help`

Command:

```sh
cargo test --test criome_gate_1of1 --features mirror-shipper
```

Result: did not compile far enough to execute the witness.

Blocking error:

`signal-criome v0.1.0` from `main#9194c795` failed its build script because the checked-in generated schema artifact is stale:

```text
StaleGeneratedArtifact {
  path: ".../signal-criome.../src/schema/lib.rs",
  update_environment_variable: "SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS"
}
```

Interpretation: the real local criome gate witness exists in spirit and is shaped correctly for the intended proof, but current dependency freshness blocks using it as verification evidence from this branch. Repair belongs in `signal-criome` or the pinned dependency/toolchain path, not in lojix.

### CriomOS-test-cluster read-only structural probe

Repository:

`/git/github.com/LiGoldragon/CriomOS-test-cluster`

This repo is currently claimed by `cloud-operator` and has active dirty changes, so I kept it read-only and avoided VM checks.

Command:

```sh
nix eval --json .#checks.x86_64-linux --apply 'builtins.attrNames'
```

Result: succeeded. Exposed checks include:

- `cluster-contracts`
- `full-module-contracts`
- `lojix-deploy-smoke`
- `multiple-tailnet-controllers-rejected`
- `pod-missing-super-node-rejected`
- `projections-match-fieldlab`
- `source-constraints`
- `spirit-nspawn-can-build`
- `vm-base-home`
- `vm-dune`
- `vm-edge-desktop`
- `vm-mercury`

Command:

```sh
nix build \
  .#checks.x86_64-linux.projections-match-fieldlab \
  .#checks.x86_64-linux.cluster-contracts \
  .#checks.x86_64-linux.source-constraints \
  --no-link
```

Result: failed before reaching the cluster assertions. The blocker was a fixed-output derivation hash mismatch for `channel-rust-stable.toml`:

```text
specified: sha256-gh/xTkxKHL4eiRXzWv8KP7vfjSk61Iq48x47BEDFgfk=
got:       sha256-mvUGEOHYJpn3ikC5hckneuGixaC+yGrkMM/liDIDgoU=
```

Interpretation: this does not prove a cluster contract failure. It proves the current test-cluster flake cannot be used as a clean structural verification source until the pinned Rust channel hash or source is reconciled.

## Code Findings

### Lojix has no daemon-owned cluster root yet

Searches over `lojix` and `signal-lojix` found no implemented `RunContainedCluster` or `ClusterRun` root. The ordinary contract currently contains the converged per-run grammar:

- `DeployContained`
- `VerifyContained`
- `Release`
- `Query(ByContainedRun ...)`

The schema already names contained substrates:

- `HermeticVm`
- `VmHostGuest`
- `EphemeralDroplet`

But runtime admission accepts only `HermeticVm` in the POC.

### VmHostGuest is intentionally unavailable

`SchemaRuntime::resolve_and_validate` rejects every target that is not `HermeticVm` with `DeployContainedRejectionReason::SubstrateUnavailable`.

That means a request can name `VmHostGuest`, but the daemon will not bring up a test VM guest yet. The test `non_hermetic_targets_are_typed_rejections_in_the_poc` verifies this current boundary.

### The compact cluster test is an authoring-layer sketch

`tests/test_op.rs` defines a `ContainedClusterTest` helper. Its `deploy_inputs()` method maps each member node into one ordinary `DeployContained` input.

That proves the intended public shape can be compact and easy to write, but it is not a cluster coordinator. It does not:

- allocate a cluster run identifier
- persist aggregate cluster state
- bring all members up before verification
- enforce a co-live barrier
- verify a cross-member gate
- release all members on failure or restart reconciliation

### Gate verification is fail-closed but not the live socket proof

The lojix POC has a Nexus effect named `VerifyContainedGate`. The test suite proves malformed or unsupported gate steps fail closed. A simple 1-of-1 gate body can complete a contained run.

The real local criome socket proof is still in spirit's `criome_gate_1of1` test. It exercises:

- authorized head ships
- threshold-short head is denied
- unconfigured gate holds the head back

That proof has not yet been wired into lojix execution, and its direct test currently cannot compile because of stale `signal-criome` generated artifacts.

## Host And Safety State

The current host is `ouranos`. `/dev/kvm` exists and `systemd-detect-virt` reports `none`, so the machine looks physically capable of KVM. The active Unix groups shown for the user did not include `kvm`, and `CriomOS-test-cluster` guidance reserves VM checks for explicitly authorized VM-testing hosts/builders.

I did not run `vm-*` checks.

## Current Capability

Lojix currently has:

- ordinary contained deploy/test/release verbs
- durable per-contained-run query state
- source and flake coordinates persisted in contained run records
- fail-closed gate verification semantics in the POC
- a compact test authoring sketch for criome/spirit/router as three contained members
- typed rejection for unavailable non-hermetic substrates

Lojix does not currently have:

- `RunContainedCluster`
- `ClusterRunRecord`
- `Query(ByClusterRun ...)`
- cluster coordinator lifecycle
- co-live barrier
- release-all/reconcile-after-crash behavior for cluster members
- `VmHostGuest` bring-up execution
- real criome socket gate proof wired into `VerifyContainedGate`

## Root Blockers

1. The `RunContainedCluster` contract and daemon coordinator are not implemented.
2. `VmHostGuest` is still a typed but unavailable substrate.
3. The live spirit/criome gate witness is blocked by stale `signal-criome` generated schema artifacts.
4. `CriomOS-test-cluster` structural checks are blocked by a stale fixed-output Rust channel hash.
5. VM checks require explicit VM-testing host/builder authority; this session did not have that authorization.

## Best Insight

The shape is closer than the phrase "VM cluster deployment" makes it sound, but the missing piece is not a small flag or a client loop. A real cluster test needs a daemon-owned aggregate because the correctness property is co-live: all members must exist at the same time before the gate runs, and release/reconciliation must be centralized so a failure or restart does not strand live members.

So the next code slice should not make the CLI loop over three `DeployContained` calls and call that a cluster. The next slice should add `RunContainedCluster` as a first-class ordinary root that lowers to the already-proven per-run machinery while owning the aggregate lifecycle.

## Best Question

Should the first `RunContainedCluster` implementation target `HermeticVm` only, proving the aggregate lifecycle and co-live/release semantics before `VmHostGuest`, or should it wait until `VmHostGuest` can bring up real NixOS test VMs?

My recommendation: implement the cluster root on `HermeticVm` first, with the real aggregate record, query, release-all, and restart reconciliation. Then swap in `VmHostGuest` as a substrate once the substrate execution is ready. That keeps the daemon-owned cluster semantics from being blocked by VM infrastructure, while still preserving the typed boundary that real VM clusters need.
