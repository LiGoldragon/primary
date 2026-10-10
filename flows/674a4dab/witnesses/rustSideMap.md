# Rust/Data Side Map

Method: code read Cargo.toml, lib.rs, flake.nix, src/ across all listed repos
Method: probe `find -name '*.rs' | xargs wc -l`, `grep -rn`, `ls`, `cat`

## 1. Crate/Repository Summary

| Repo | What it is | Rust lines | Modules | Key deps (path/git) |
|---|---|---|---|---|
| horizon-rs | Typed schema, projection, and CLI for CriomOS cluster horizons; reads ClusterProposal dotos, produces viewpoint-scoped enriched Horizon JSON | 6,494 | 29 | dotos (git) |
| criomos-horizon-config | Pan-horizon DOTOS config (horizon.dotos); domain suffixes, transitional LAN | 0 (Nix-only) | 0 | none |
| goldragon | Production cluster proposal data: 8 nodes, 2 users, trust/access/router maps, secrets | 0 (data-only) | 0 | none |
| lojix | Deploy orchestrator Nexus: daemon, two CLI clients, bootstrap, store tools | 21,277 | 17 | horizon-lib, signal-lojix, meta-signal-lojix, signal-frame, sema-engine, triad-runtime, dotos (all git) |
| signal-lojix | Ordinary Signal contract for the lojix Nexus | 1,444 | 6 | signal-frame, core-ethos, name-table, schema-rust, sema-translator, structural-codec, dotos (all git) |
| meta-signal-lojix | Owner Signal contract for lojix policy surface | (not counted) | -- | signal-lojix, signal-frame, dotos (git) |
| dotos | Structural DOTOS reader and codec; hand-authored recursion floor | 8,646 | 19 | dotos-derive (path, workspace) |
| datom | Pure positional typed data on the Protos substrate | 2,167 | 4 | protos (git) |
| core-ethos (= core-schema repo) | Bootstrap Ethos type system: structural codec, identity, discovery | 6,774 | 10 | content-identity, name-table, raw-discovery, structural-codec (git) |
| core-logos | Complete ordered structural carrier for Logos | 836 | 7 | content-identity, name-table, protos (git) |
| core-nomos | Authority-sealed bootstrap Ethos lowering into Logos | 1,321 | 4 | content-identity, core-ethos, core-logos, name-table (git) |
| ethos-engine | EncodedEthos daemon; kameo actor-based, speaks signal-ethos | 1,601 | 6 | core-ethos, core-schema (compat), name-table (2 revs), content-identity, schema-language, kameo, signal-ethos, signal-sema-storage (git) |
| ethos-monolith | Code generator: reads signal Ethos text, emits signal.rs for wire consumers | 6,240 | 31 | protos (git) |
| orchestrate | Orchestration Nexus: lock requests, worktrees | (not separately counted) | -- | signal-orchestrate, meta-signal-orchestrate, datom, dotos, protos, sema-engine, signal-frame (git) |

### ASCII Dependency Graph

```
                         NEXUS LAYER
  lojix ──git──> horizon-lib (horizon-rs/lib)
    |  ──git──> signal-lojix ──git──> signal-frame
    |  ──git──> meta-signal-lojix ──git──> signal-lojix
    |  ──git──> sema-engine ──git──> sema, signal-sema, core-ethos, core-nomos
    |  ──git──> triad-runtime
    |  ──git──> dotos

  orchestrate ──git──> signal-orchestrate ──git──> ethos-monolith ──git──> protos
    |  ──git──> datom ──git──> protos
    |  ──git──> dotos, sema-engine, signal-frame

                       SCHEMA/TYPE LAYER
  core-nomos ──git──> core-ethos, core-logos, name-table, content-identity
  core-ethos ──git──> content-identity, name-table, raw-discovery, structural-codec
  core-logos  ──git──> content-identity, name-table, protos

                       ENGINE LAYER
  ethos-engine ──git──> core-ethos, core-schema(compat), name-table(x2),
    |                   content-identity, schema-language, kameo,
    |                   signal-ethos, signal-sema-storage

                       FOUNDATION LAYER
  structural-codec ──git──> content-identity, name-table, raw-discovery
  name-table ──git──> content-identity
  raw-discovery ──git──> content-identity
  content-identity (leaf)
  protos (leaf)
  dotos ──path──> dotos-derive (workspace)

                       DATA / NIX-ONLY
  horizon-rs ──path──> lib (workspace), ──git──> dotos
  criomos-horizon-config  (horizon.dotos, no Rust)
  goldragon               (datom.dotos + synchronizer.dotos + secrets/, no Rust)
```

All inter-repo Rust deps are git with pinned revs. The only path dep crossing a crate boundary is horizon-rs's own workspace lib. Several repos pin different revisions of the same leaf (content-identity, name-table, signal-frame).

## 2. Data Model and Instance Data

### What Horizon defines

**Input** (ClusterProposal in dotos): NodeProposal, UserProposal, DomainProposal, ClusterTrust, Machine, Io, NodePubKeys, NodeService (9 variants), RouterInterfaces, WireguardProxy, UserPubKeyEntry, HostedSite, SiteSource, SiteRenderer, SecretReference.

**Output** (Horizon in JSON): Node (~60 fields -- identity, trust, species, machine, pubkeys, derived booleans, viewpoint-only builder_configs/cache_urls/admin_ssh_pub_keys), Cluster, User (~25 fields), BuilderConfig.

**Enums**: NodeSpecies (Center, Router, Edge, Hybrid, EdgeTesting, LargeAi, LargeAiRouter, TestVm, CloudNode), MachineSpecies (Metal, Pod), UserSpecies (Code, Multimedia, Unlimited), Arch, Keyboard, Style, Editor, TextSize, KvmAvailability, WlanBand, WlanStandard.

### Where instance data lives

| Fact | File | Format | Consumers |
|---|---|---|---|
| Cluster proposal (nodes Ouranos, Zeus, Bird + 5 others; users li, bird) | `/git/.../goldragon/datom.dotos` | positional DOTOS | horizon-cli (stdin), lojix (ProposalSource) |
| Pan-horizon config (domain suffixes, transitional LAN) | `/git/.../criomos-horizon-config/horizon.dotos` | DOTOS | CriomOS flake input |
| Projected horizon per deploy | written by lojix at deploy time | JSON (content-addressed flake) | CriomOS, CriomOS-home (flake input override) |
| Router wifi secrets, LLM token | `/git/.../goldragon/secrets/` | SOPS-encrypted | CriomOS at eval/activation |

### Data flow

goldragon/datom.dotos --> horizon-cli --cluster --node (or lojix in-process via horizon-lib) --> enriched Horizon JSON --> CriomOS and CriomOS-home consume via flake input override during Nix evaluation. The default flake input is a stub (`path:./stubs/no-horizon`) that throws; lojix overrides it per deployment.

### Same fact in more than one place

- Host names (ouranos, zeus, bird, etc.) appear in `goldragon/datom.dotos` (canonical) and in `horizon-rs/lib/tests/` (5 test fixture files) and `lojix/tests/deploy_transport_integration.rs`.
- The `core-ethos` crate exists at two repo URLs: `/git/.../core-schema` and `/git/.../core-ethos` -- byte-identical src/ trees, same Cargo.toml package name.

## 3. Lojix

### Nexus and socket layout

Two Unix domain sockets, no default paths (from `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET` env vars, injected via `LOJIX_CONFIGURATION` archive):
- **Ordinary** (mode 0o660): Query, WatchDeployments, WatchCacheRetention, Unwatch, CheckHostKeyMaterial
- **Owner** (mode 0o600): Deploy, Pin, Unpin, Retire, Test

### Deployment request contents

`Deploy.Host`: cluster_name, node_name, host_composition, proposal_source, flake_reference, deployment_transport (nix_store_uri + ssh_destination), deployment_input_mode, deployment_output_selector, activation_backend, host_deploy_action, source_revision_policy, optional_nix_builder_spec, extra_substituter_vector.

`Deploy.UserEnvironment`: same shape with user_name and user_environment_action replacing host_composition and host_deploy_action.

These fields come from the caller (meta-lojix CLI or programmatic client). No field has a daemon-supplied default except via TestDefaults in the startup configuration (development only).

### State

Sema store (redb `.sema` file at configurable path): generation set, GC-roots retention tree, append-only event log, container-lifecycle mirror, deployment records, outbox records, identifier allocations. Schema v4 required.

### Current state of named queries (from flows/01a048a6/log.md)

- **Query.ByDeployment**: fails at the frame boundary -- non-functional.
- **CheckHostKeyMaterial**: stub returning empty material -- implemented but returns no data.
- No deployment request or runtime mutation has been submitted.
- Deployment preflight is blocked: no authoritative `manifests/*.dotos` selection exists.

### Nix invocation

Lojix invokes Nix through a `NixCommand` struct (schema_runtime.rs:5750) wrapping program + arguments, executed by `EffectExecution`:
- `nix eval --raw <attribute>.drvPath` (with optional `--refresh`, flake input overrides)
- `nix build --print-out-paths`
- `nix copy --substitute-on-destination --to <store-uri> <closure>`
- `nix flake metadata --json <flake>`
- `nix hash path --type sha256 --sri <path>`
- `nix-store` (bootstrap only, GC root registration)

Pipeline: MaterializeHorizon -> NixEval -> NixBuild -> CopyClosure -> ActivateGeneration.

## 4. Goldragon

**What it computes**: Nothing -- it is pure data. Contains `datom.dotos` (production cluster proposal: 8 nodes, 2 users, trust maps, machine specs, node services, pubkeys), `synchronizer.dotos` (component repo list for the synchronizer tool), and `secrets/` (SOPS-encrypted router wifi/LLM credentials).

**Inputs**: Authored by hand in DOTOS positional records conforming to horizon-rs ClusterProposal schema.

**Emissions**: The `.dotos` file itself is the emission -- consumed by horizon-cli on stdin (or lojix in-process via horizon-lib) and projected into JSON.

**Consumers**: horizon-rs/horizon-cli, lojix (ProposalSource), CriomOS and CriomOS-home (via projected Horizon JSON flake input).

**manifests/*.dotos in /home/li/primary**: The directory exists but is empty. The flow log (01a048a6) states deployment is blocked because "no authoritative `manifests/*.dotos` selection supplies the required explicit store/SSH transport, builder, selector, and input mode for Ouranos and Zeus." These manifests do not yet exist.

## 5. Dead or Duplicated Code

| # | Finding | Paths |
|---|---|---|
| 1 | Repo duplicate: core-schema is byte-identical to core-ethos (same crate name core-ethos) | `/git/.../core-schema/` = `/git/.../core-ethos/` |
| 2 | DeploymentTransport defined twice (runtime vs durable) | `lojix/src/runtime_flow.rs:74` / `lojix/src/runtime_model.rs:66` |
| 3 | DeploymentInputMode defined twice | `lojix/src/runtime_flow.rs:79` / `lojix/src/runtime_model.rs:71` |
| 4 | ActivationBackend defined twice | `lojix/src/runtime_flow.rs` / `lojix/src/runtime_model.rs` |
| 5 | ExtraSubstituter defined twice | `lojix/src/runtime_flow.rs` / `lojix/src/runtime_model.rs` |
| 6 | TestExecutionProfile defined twice | `lojix/src/runtime_flow.rs` / `lojix/src/runtime_model.rs` |
| 7 | Input/Output defined twice | `lojix/src/runtime_flow.rs` / `lojix/src/runtime_model.rs` |
| 8 | Legacy compat path (no external consumers) | `ethos-engine/src/legacy_ingest.rs`, `legacy_storage_ingest.rs` |
| 9 | ethos-engine pins name-table at two different revisions + compat dep on core-schema at frozen rev | `ethos-engine/Cargo.toml` |
| 10 | Generated signal.rs checked in (by design) | `signal-lojix/src/schema/lib/generated.rs` (547 lines) + all signal-* repos |

Notes: zero `#[allow(dead_code)]` annotations across all 14 repos. Two documentary "stub" references in `lojix/src/schema_runtime.rs` (lines 4825, 4942) referring to CriomOS no-secrets stub concept. `synchronizer.dotos` refers to `datom.nota` but the file is `datom.dotos` (stale naming). `orchestrate/src/store.rs` has `LegacyStoredLock` struct (line 202) for pre-1/5 store format refusal.

## 6. Unknowns

- How the different pinned revisions of shared leaves (content-identity, name-table, signal-frame) across consumers relate to each other -- whether they are intentionally staggered or merely out of sync.
- The full list of repos that pin core-schema vs core-ethos by git URL and whether any consumer actually requires both repo URLs.
- What `sema-engine`, `sema`, `signal-sema` contain internally (not explored in depth -- only their dependency role was traced).
- Whether `triad-runtime` is used beyond lojix.
- The internal structure of `orchestrate` and `meta-signal-orchestrate` (only dependency edges traced).
- What `schema-rust`, `schema-language`, `sema-translator`, `signal-sema-translator` do individually (only their role as signal-lojix/ethos-engine build deps was noted).
- Whether the runtime_flow/runtime_model type duplication in lojix is a deliberate architecture (transient vs durable) or a consolidation target.
- Whether any other Nix evaluation (Curriculum, CriomOS-test-cluster beyond what was found) consumes horizon data through additional paths.
- What state, if any, lojix keeps under /var/lib or ~/.cache at runtime -- the paths are configurable and no hardcoded defaults were found.
- The exact contents and role of `goldragon/synchronizer.dotos` beyond the `datom.nota` reference.
