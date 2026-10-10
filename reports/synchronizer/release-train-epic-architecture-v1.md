# Synchronizer release-train epic architecture v1

**Status:** design only. This report proposes no source change, release, deployment, or modification to a component lock.

## Outcome

The requested capability is a release-train system, not a replacement Cargo.lock and not a mutable common dependency cache.

One authored NOTA document expresses the **intent** of an epic train: its component membership, candidate branch selectors, train-owned branch naming, verification policy, and projection policy. Synchronizer discovers the actual dependency graph from the selected revisions, rejects any drift from the declared train boundary, materializes component-specific Cargo and Nix locks, and emits an immutable resolved closure. Nix tests consume that resolved closure, never a moving branch name.

The resulting model has four deliberately distinct objects:

```text
ReleaseTrainIntent.nota       human-maintained, branch selectors, no resolved locks
        ↓ resolve + discover + validate
ResolvedReleaseTrain          immutable commits, lock digests, source attestations
        ↓ project
release-train.lock.json       generated JSON projection for Nix and tooling
        ↓ build
per-component candidate commits and an integration flake closure
```

The authoritative human surface remains NOTA. JSON is a generated, canonical Textual projection because Nix can consume it conveniently. It is not an authority, and neither JSON nor a future YAML/TOML projection changes the typed release-train value.

## Source truth and constraints

Synchronizer already has most of the correct orchestration substrate:

- `SynchronizerConfig` is a positional NOTA configuration.
- `DependencyGraph::discover` identifies Cargo and flake edges from manifests, matched by repository identity, rather than declared dependency edges.
- `SynchronizerRun` performs deterministic leaf-to-consumer ascent, writes only a configured staging branch, and verifies pushed revisions remotely.
- `BaseSelection::StagedCascade` already reads a pre-staged component tip when present and seeds the cascade ledger, which is the beginning of coordinated branch verification.
- `Cargo.toml` and `Cargo.lock` are separate typed, format-preserving editing surfaces. A controlled Cargo resolution fallback exists for transitive changes.
- `flake.lock` is a distinct JSON lock domain. Synchronizer preserves the input `original` and changes only locked evidence, correctly avoiding Nix re-locking a cascaded input back to its source branch.
- Nix verification addresses pushed exact revisions. This is the right rule for remote builders and must remain true for epic trains.

These constraints rule out three tempting but incorrect designs:

1. A train NOTA file must **not** replace individual Cargo.lock files. Cargo resolves a package graph per workspace/manifest feature set; only Cargo can produce the valid lock for that consumer.
2. A flake-input override cannot repin Cargo Git dependencies. `flake.lock` and Cargo.lock are independent resolution domains.
3. A shared “latest crates” index must not become source authority. It would weaken the provenance that Cargo checksums, Git commits, Nix nar hashes, and committed locks establish.

## Authority and identity boundaries

### Authored intent versus resolved closure

`ReleaseTrainIntent` is maintained by people. It may name a branch because a branch is a useful request to Synchronizer, but a branch has no reproducible identity. It says, for example, “use the `next-gen` candidate of NOTA and the `poc-structural-codec` candidate of Schema.”

`ResolvedReleaseTrain` is emitted only after Synchronizer has fetched every selected ref and read every manifest at its exact commit. It replaces every selector with an immutable commit and records the lock/projection identities. A builder accepts only this resolved object.

A train run must fail if a selected remote branch moves between resolution and candidate commit creation, or if the final pushed candidate is not based on the recorded source tip. Re-resolving creates a new closure; it never silently mutates an old one.

### Four non-interchangeable identity classes

| Identity | What it identifies | Authority | It must not be substituted for |
| --- | --- | --- | --- |
| Cargo registry checksum / Git commit | exact crate archive or Git source Cargo resolved | Cargo manifest + Cargo.lock + Cargo verification | a Nix narHash or language content hash |
| Nix narHash / fixed-output identity | exact fetched Nix input tree | flake.lock or explicit fixed-output fetch | Cargo package resolution |
| domain BLAKE3 content identity | a typed domain value such as a resolved-train record or future Core value | typed canonical domain encoding | source provenance or Nix fetch authentication |
| release-train closure identity | canonical `ResolvedReleaseTrain` payload | train contract | a component commit alone |

The train closure identity should be domain-separated BLAKE3 over canonical typed resolved-train bytes. It is an indexable statement about a closure, not an assertion that all included source bytes equal the BLAKE3 value. Each source retains its Cargo and Nix provenance evidence.

## Typed contract

The following records are proposed contract types. They are intentionally typed and positional when represented in NOTA; field labels below are explanatory only. They can begin in a small `release-train-contract` crate without depending on prospective language-family Core crates.

```text
ReleaseTrainIntent
  TrainName
  TrainPolicy
  [TrainComponent]
  ProjectionPolicy
  VerificationPolicy

TrainComponent
  ComponentIdentity
  CandidateSelector
  CandidateBranch
  ExpectedBase

CandidateSelector
  Mainline
  Branch(BranchName)
  ExactCommit(CommitId)       ;; allowed only for a deliberately frozen input

TrainPolicy
  CandidateBranchTemplate
  DriftPolicy
  PromotionPolicy

DriftPolicy
  RejectUndeclaredMember
  RejectMissingExpectedMember
  RejectUnexpectedInternalEdge
  RejectSelectorMovement

ResolvedReleaseTrain
  ReleaseTrainIntentIdentity
  ResolutionTime
  [ResolvedComponent]
  DiscoveredTopologyIdentity
  [ComponentResolution]
  SourceIndexIdentity
  ProjectionIdentities

ResolvedComponent
  ComponentIdentity
  SelectedRef              ;; diagnostic only
  SelectedCommit
  CandidateCommit
  CandidateRef
  CargoLockIdentity
  FlakeLockIdentity
  NixSourceAttestations

ComponentResolution
  Consumer
  Producer
  PinSurface               ;; CargoManifest, CargoLock, FlakeManifest, FlakeLock
  RequiredCommit
  ObservedCommit

NixSourceAttestation
  SourceLocator
  CommitId
  NarHash
  LastModified

ProjectionIdentities
  NotaIntentIdentity
  ResolvedClosureIdentity
  JsonProjectionIdentity
  GeneratedFlakeIdentity
```

`ComponentIdentity` is repository identity, not Cargo package name, table key, flake input name, or a branch string. The existing Synchronizer repository-identity matching remains the single way to recognize an internal edge.

`ExpectedBase` protects concurrent work: it specifies the exact mainline or candidate commit on which a selected branch must be based. A branch that has silently rebased elsewhere is not an equivalent train candidate.

### Discovery validates intent; it never yields to it

The intent config names only the candidate component set and selectors. It does **not** declare Cargo or flake edges. Synchronizer reads manifests and locks at resolved commits, discovers the graph as it does today, then validates:

- every discovered internal producer belongs to the train component set;
- every configured component participates in the discovered closure or is explicitly marked an allowed independent root;
- no selected source moved after resolution;
- every Cargo and flake internal pin resolves to the producer commit required by the closure;
- no deliberate `rev` or tag pin is overwritten; it instead produces a specific train-drift failure;
- Cargo package/repository aliases are resolved through existing repository identity, not guessed from names;
- no cycle exists.

Unexpected internal edges, missing members, a lock that resolves an old producer commit, and a manifest whose selector differs from the intent are all loud failures. A plan is a constraint on discovered truth, never an alternative topology authority.

## Epic-branch topology

Each epic uses a unique, configured train name. Worker feature branches remain component-local. Once a component branch is ready to participate, it is pushed. Synchronizer creates or force-rebuilds only the explicitly configured train branch in each participating repository, for example `train/language-family-poc`; it never writes a worker branch or mainline.

```text
component feature branches (pushed)
  nota: next-gen
  schema-language: poc-structural
  schema-rust: poc-textual-rust
          ↓ selected by ReleaseTrainIntent
Synchronizer resolves exact heads and discovered topology
          ↓
component train/<train-name> commits with generated valid per-component locks
          ↓
ResolvedReleaseTrain + generated JSON + generated integration flake
          ↓
remote Nix checks addressed by exact candidate commits
```

The candidate branch is a reproducible integration artifact only after its exact commit appears in `ResolvedReleaseTrain`. Its branch name is never accepted as build identity. A later run may force-update a train branch, but that necessarily produces a different closure identity and must not overwrite an accepted closure artifact.

Existing `StagedCascade` should become an implementation detail of a typed `ReleaseTrainRun`, rather than the external authority. It supplies useful behavior—reading staged tips and seeding the cascade ledger—but the new run adds train identity, selector resolution, graph-drift validation, immutable closure emission, and per-train branch isolation.

## Cargo and Nix projections

### Cargo: generated per consumer, never globally substituted

For every candidate consumer, Synchronizer uses its exact selected base tree and its resolved internal producer commits to create that consumer’s ordinary `Cargo.toml`/`Cargo.lock` edits:

- `Cargo.toml` retains a reachable branch reference when Cargo requires it to reach the locked commit; the train candidate ref is used only as the configured reachable reference.
- `Cargo.lock` records the exact Git revision and the complete graph Cargo resolved for that component.
- If a producer changes transitive dependencies, the existing scratch-tree `cargo update --precise` mechanism regenerates the consumer lock; the resulting lock is then validated against the intended closure.
- The closure stores each component lock’s content identity and the internal package-source observations, but it never merges locks from different components.

A generated lock is valid only as a projection of one exact component manifest, target, toolchain/source configuration, and Cargo resolution. The closure generator must run Cargo in a hermetic scratch materialization and reject a lock whose resolved internal sources disagree with the intended commits.

### Nix: consume resolved JSON without pretending it is flake.lock

Nix flake input resolution is governed by `flake.lock`; a generic JSON document cannot replace it. The train therefore generates two distinct artifacts:

1. **Updated component `flake.lock` files**, produced by the existing typed Nix lock editor and containing source `rev`, `narHash`, and `lastModified` evidence.
2. **`release-train.lock.json`**, a canonical JSON projection of `ResolvedReleaseTrain`, consumed by a generated integration flake or check harness using `builtins.fromJSON`.

The generated integration flake uses only explicit fixed source records from the JSON projection—commit plus narHash for Nix-fetched component trees—and invokes each component’s own flake/package/check interface at the matching candidate commit. It does not dynamically resolve branches or permit an unpinned local path. Shared `nixpkgs`, `fenix`, and `crane` inputs may use normal flake `follows` only where the generated closure verifies that the participating components use compatible source identities.

The integration flake is a test orchestrator, not a replacement package manager. It must report component check output and closure identity together.

## Shared Rust dependency sources and compiled reuse

### What Nix already deduplicates

Nix already shares an identical derivation result across components. If two Crane builds have identical source closure, Cargo lock, toolchain, target, feature set, environment, and build flags, their dependency derivations can be identical and Nix will reuse them. No custom index improves that case.

Most independently versioned repositories will differ in at least their source tree, feature graph, or Cargo lock. Their `buildDepsOnly` derivations therefore legitimately differ. Forcing reuse beyond matching derivation inputs would be unsound.

### Safe source reuse: an immutable crate-source index

A separate `crate-source-index` component is viable after measurement. It is a content-addressed source/vendoring service, not a mutable registry and not part of Synchronizer state.

```text
CrateSourceRecord
  SourceKind                 Registry | Git
  CargoIdentity              name/version/checksum OR canonical git locator/commit
  SourceContentIdentity      BLAKE3 over normalized fetched source bytes
  CargoVerificationEvidence  registry checksum or Git commit/tree evidence
  MaterializationIdentity    fixed-output Nix source or vendor-tree narHash

VendorSnapshot
  ordered CrateSourceRecord identities
  CargoConfigProjection
  snapshot identity
```

For registry crates, Cargo’s recorded checksum remains the source authentication fact. For Git crates, canonical locator plus exact commit remains the source selection fact; a fetched tree identity can supplement, never replace, it. A fixed-output Nix derivation or vetted vendor snapshot can materialize the source set immutably. The release-train closure may reference a `VendorSnapshot` only by exact identity.

The index’s first implementation should be read-only ingestion from already Cargo-validated sources, deterministic materialization, and verification that vendored builds resolve the same package IDs as the component Cargo.lock. It must not accept “latest,” silently alter Cargo configuration, bypass checksums, or mutate content under an existing key.

### Compiled reuse: derive it, do not promise it

A later `rust-dependency-build-index` may index **outputs** only by the full derivation key:

```text
DependencyBuildKey
  VendorSnapshotIdentity
  CargoLockIdentity
  RustToolchainIdentity
  TargetTriple
  FeatureSet
  CargoProfile
  Rustflags
  BuildScriptEnvironmentIdentity
  NixSystem
```

This is evidence and scheduling metadata for Nix/remote builders, not a manually linked Rust artifact cache. The resulting build must remain a Nix derivation whose inputs imply this key; otherwise Cargo build scripts, proc macros, features, and target-specific dependencies make reuse unsound.

The sequence is therefore:

1. measure duplicated download/source/vendor work;
2. introduce immutable source/vendoring reuse if justified;
3. use common toolchain and Crane conventions across components;
4. observe actual matching dependency derivations;
5. only then add an output index for discoverability/retention.

Do not build a shared compiled-cache protocol before evidence shows eligible matching derivations.

## Textual forms and JSON

The release-train contract is typed data. During the current PoC, existing `NotaEncode`/`NotaDecode` may author and read `ReleaseTrainIntent`; serde JSON can produce the generated Nix projection. This bootstrap does not assume unaccepted language-family internals.

The target reusable boundary is:

```text
Typed release-train value
  ↔ StructuralForm-selected intermediate structure
  ↔ TextualNOTA | TextualJson | TextualYaml | TextualToml
```

`TextualJson` is the first additional form because Nix consumes JSON reliably. It must have an explicit expected-type structural table rather than becoming a second semantic model:

- expected type selects the JSON form; JSON token shape never globally determines a Core/domain type;
- JSON objects are a projection with explicit key, ordering, duplicate-key, and absent-versus-null policy;
- NameTable-derived display keys remain at the Textual boundary and never enter Core/domain identity;
- JSON number precision and string escaping have format-specific leaf contracts;
- canonical JSON is generated deterministically for a resolved closure;
- YAML and TOML reuse the typed form/leaf contract where their data models can express it, but each has an explicit adapter for its own ambiguity, duplicate-key, comments, ordering, and numeric rules.

Future StructuralForm mechanics, runtime evaluator behavior, Core naming, and table storage remain proposals until separately ruled. This release-train design only requires that a typed NOTA authoring codec and a deterministic JSON projection exist. It must not block the train on the full language-family PoC.

Conversely, the language-family PoC can consume a resolved release-train fixture as a realistic cross-repository input without making Synchronizer depend on CoreSchema, Nomos, Logos, or Spirit. The dependency direction stays one way:

```text
release-train contract → generated integration closure → language-family candidate checks
```

The language system may later supply the shared TextualForm implementation beneath the contract, but no train behavior is circularly predicated on it.

## Operations and trust boundaries

A future public `signal-release-train` contract is not required for the initial process tool. The initial unit is a non-durable, CLI-invoked Synchronizer operation, like today. If train declarations, approvals, history, or asynchronous builder work become durable, then a stateful `release-train` component earns `signal-release-train`, a daemon, and SEMA-backed closure records.

Initial operations are typed library/CLI operations:

```text
ValidateIntent(intent) -> DiscoveredTopology
ResolveIntent(intent) -> ResolvedReleaseTrain
MaterializeTrain(closure) -> [CandidateCommit]
GenerateNixProjection(closure) -> ProjectionArtifacts
VerifyClosure(closure) -> VerificationReport
PromoteCandidate(closure) -> outside Synchronizer authority
```

Trust boundaries:

- NOTA intent is authenticated/versioned repository data, not an untrusted remote request.
- Git remotes supply candidate bytes but exact commits and expected bases are verified before use.
- Cargo is the resolver of Cargo.lock; Synchronizer validates rather than invents resolution.
- Nix prefetch establishes narHash evidence; Nix builds only immutable candidate refs.
- the source index may materialize only records whose Cargo/Git evidence verifies;
- generated JSON is checked against its typed closure identity before Nix consumes it;
- release-train promotion and production deployment remain outside the tool.

## Staged proof of concept and epic

### P0: contract freeze and observational fixture

Create `release-train-contract` as a small typed library or a clearly isolated Synchronizer module. Add a NOTA intent fixture for the NOTA → schema-language → schema-rust train. Resolve only; do not edit any component. Prove discovery, branch selector resolution, expected-base validation, closure hashing, and drift failure fixtures.

### P1: candidate materialization

Extend Synchronizer with `ReleaseTrainRun`, reusing the existing object-level commit, typed Cargo/flake edits, and `StagedCascade` mechanics. Produce isolated `train/<name>` commits and valid per-component Cargo.lock/flake.lock updates. Test the exact-next-gen NOTA compatibility failure as an expected unresolved closure, then a small synthetic green chain.

### P2: generated Nix projection and portable checks

Generate canonical `release-train.lock.json` and an integration flake fixture. Prove JSON identity, no local path inputs, exact candidate commit/narHash fetches, remote-builder invocation, and failure when any selector or source attestation drifts. This is the first deterministic all-component test surface.

### P3: source reuse measurement and vendor PoC

Measure Cargo fetches, vendor-tree duplication, and actual Crane derivation-key overlap across P2. Only if measurement shows material duplication, build a read-only `crate-source-index` and one immutable `VendorSnapshot` integration test. Do not implement compiled-output indexing yet.

### P4: TextualJson extraction

Once the language-family structural-form boundary is accepted and evidenced, replace the bootstrap JSON adapter with `TextualJson`, preserving byte-level JSON fixtures and closure identity semantics. Add YAML/TOML only as separate adapters with their own test matrices.

### P5: language-family and Spirit composition

Use P2 closure resolution to coordinate the full language-family release train. Spirit remains a separate later isolated-store milestone: its component pins join the closure only after Schema/Nomos/Logos interfaces are actually implemented and portable. No P0–P4 operation touches a Spirit store or deployment pin.

## Acceptance and rollback

Required evidence for P2:

- intent round trip through canonical NOTA;
- resolving a branch selector produces a closure with exact commits;
- the same intent plus moved branch produces a distinct resolution or loud selector-movement failure;
- topology mismatch, missing component, cycle, deliberate pin, and incorrect lock are all loud failures;
- each generated Cargo.lock passes Cargo resolution/build for its own component;
- each generated flake.lock has verified narHash and preserves required Nix input semantics;
- generated JSON parses in Nix and is byte-stable for the same closure;
- integration Nix builds consume only pushed immutable refs and contain no local paths;
- closure report identifies every component commit, lock identity, source attestation, verification gate, and failure;
- repeated resolve/materialize/verify on unchanged refs yields the same closure identity and equivalent projections.

A failed train is rolled back by discarding its per-train candidate branches and generated closure artifacts. It has no authority to merge or mutate mainline. Once a closure is accepted as evidence, retain it immutably; a replacement train is a new identity rather than an in-place edit.

## Psyche-authority questions

1. Should the authoritative NOTA release-train intent live beside the existing operational `synchronizer.nota` in infrastructure data, as a distinct `release-trains/<name>.nota` document, rather than extending the operational config with closure data? **Recommendation: yes.**
2. Authorize per-train candidate branches such as `train/<name>` and require every component selector to have a recorded expected base before materialization? **Recommendation: yes.**
3. Should a discovered component edge outside the intent component set always fail the train, or may an intent explicitly admit immutable external components? **Recommendation: default fail; allow only explicit immutable external declarations.**
4. Authorize P0–P2 as the first epic, deferring the source index until duplication is measured and deferring compiled-output indexing until matching derivations are proven? **Recommendation: yes.**
5. Is JSON acceptable as the first generated Nix projection while TextualJson remains a staged language-family implementation, with YAML/TOML deferred to explicit adapters? **Recommendation: yes.**
6. Does the first release-train PoC include only NOTA → schema-language → schema-rust, or also a minimal downstream Spirit *build* consumer without store activation? **Recommendation: begin with the three-component chain; add Spirit only after P2 is green.**
