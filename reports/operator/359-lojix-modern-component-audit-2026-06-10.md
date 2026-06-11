# Lojix modern-component audit against Spirit

## Scope

This audit compares the new `lojix` component triad against `spirit` as the current modern component exemplar.

Audited repos:

- `/git/github.com/LiGoldragon/spirit`
- `/git/github.com/LiGoldragon/signal-spirit`
- `/git/github.com/LiGoldragon/meta-signal-spirit`
- `/git/github.com/LiGoldragon/lojix`
- `/git/github.com/LiGoldragon/signal-lojix`
- `/git/github.com/LiGoldragon/meta-signal-lojix`

Spirit reference traits used here:

- daemon crate at repo root;
- one component crate, two binaries: CLI and daemon;
- binary-only daemon startup from one rkyv configuration file;
- optional NOTA text surface for CLI/debug, absent from default daemon graph;
- generated plane schemas for Signal/Nexus/SEMA plus generated daemon shell;
- external contracts split into ordinary signal and meta signal;
- durable state through `sema-engine`/redb;
- process-boundary, dependency-boundary, round-trip, and Nix witnesses.

## Executive result

Lojix has the right large outline: component triad exists, owner mutations are separated into `meta-signal-lojix`, ordinary read/watch operations are in `signal-lojix`, the daemon has two authority-tiered sockets, and deploy pipeline work is named in the Nexus schema.

The main gaps are not conceptual naming. They are modernization and production-readiness gaps:

1. daemon startup is still NOTA/text-config based;
2. the CLI is not yet a NOTA human edge;
3. default dependency graphs still pull deprecated text/legacy crates;
4. sibling contracts are path dependencies;
5. state is in-memory under `Mutex`, not durable `sema-engine`/redb;
6. subscriptions only mint tokens; no daemon-pushed stream frames yet;
7. the daemon shell is handwritten rather than schema-emitted;
8. contract crates lack Spirit-style witnesses;
9. the crate still lives under `triad-port/` and has no repo flake check surface;
10. docs and generated-version metadata drift from the implemented code.

## What is already aligned

### Repo triad exists

The new Lojix surface has the expected three repos:

- `lojix` — daemon and CLI implementation under `triad-port/`;
- `signal-lojix` — ordinary peer-callable contract;
- `meta-signal-lojix` — owner/meta policy contract.

The split is materially enforced in the schemas. `signal-lojix/triad-port/schema/lib.schema` says owner-only mutations live in meta, and `meta-signal-lojix/triad-port/schema/lib.schema` imports shared deploy nouns from `signal-lojix` rather than redefining them.

### Ordinary/meta authority split is implemented in the schemas

Actual `signal-lojix` roots are:

```text
[Query WatchDeployments WatchCacheRetention Unwatch CheckHostKeyMaterial]
[Queried Watching Unwatched KeyMaterialChecked QueryRejected WatchRejected UnwatchRejected KeyMaterialCheckRejected]
```

Actual `meta-signal-lojix` roots are:

```text
[Deploy Pin Unpin Retire]
[Deployed DeployRejected Pinned PinRejected Unpinned UnpinRejected Retired RetireRejected]
```

That is the right direction: deploy and retention mutations are owner-socket operations, not peer-callable ordinary operations.

### Runtime effects are schema-visible

`lojix/triad-port/schema/nexus.schema` names the deploy pipeline as `EffectCommand` variants:

- `ResolveFlakeAuth`
- `MaterializeHorizon`
- `NixEval`
- `NixBuild`
- `CopyClosure`
- `ActivateGeneration`
- `PathInfoGc`

This follows Spirit's rule that internal engine features appear in the Nexus schema before implementation hides them in Rust.

### Actor-native socket shell is partly modern

`lojix/triad-port/src/daemon.rs` uses `triad_runtime::ActorMultiListenerDaemon`, per-connection workers, async frame IO, bounded frame size, read timeout, and concurrency limit. The audit test `tests/actor_native_runtime.rs` guards against older blocking-listener markers such as `spawn_blocking` and `std::process::Command` in the schema runtime.

## Findings

### L1 — daemon startup still violates binary-only daemon startup

Evidence:

- `lojix/triad-port/src/bin/lojix-daemon.rs` says the daemon entry is a “single NOTA argument.”
- It calls `nota_config::ConfigurationSource::from_argv()?.decode()?`.
- `lojix/triad-port/src/lib.rs` derives `NotaRecord` on `DaemonConfiguration` and uses `nota_config::impl_rkyv_configuration!(DaemonConfiguration)`.
- `lojix/triad-port/Cargo.toml` depends unconditionally on `nota-codec`, `nota-config`, and `nota-next`.

Spirit exemplar:

- `spirit/src/bin/spirit-daemon.rs` delegates to the generated daemon entry.
- `spirit/src/schema/daemon.rs` documents: “exactly one argument, a signal-encoded (rkyv) configuration file.”
- `spirit/src/config.rs` loads `SpiritDaemonConfiguration` via `from_binary_path` / `from_binary_bytes` and explicitly says no NOTA is linked there.

Why it matters:

The workspace rule is daemon binary startup only. Daemons must not parse NOTA or accept inline `.nota` configuration at startup. Deploy/bootstrap tooling may generate the binary rkyv configuration file, as Spirit does with `spirit-write-configuration`, but the daemon process itself should reject NOTA.

Fix direction:

- Move Lojix daemon configuration into a contract-owned rkyv type, likely `meta-signal-lojix` because it is the owner/policy surface.
- Add a `lojix-write-configuration` helper if a text edge is needed for launch tooling.
- Make `lojix-daemon` accept exactly one signal/rkyv file argument.
- Remove `nota-config`, `nota-codec`, and `nota-next` from the daemon's default dependency graph.

### L2 — CLI is not yet a Spirit-style NOTA client

Evidence:

- `lojix/triad-port/src/client.rs` rejects `ComponentArgument::InlineNota(_)` with `InlineNotaUnsupported`.
- `ComponentArgument::NotaFile(file)` is passed to `decode_signal_file`, so a `.nota` file is treated as rkyv bytes.
- `ClientReply::Display` prints `Debug` with `{output:?}`, not generated NOTA.
- `lojix/triad-port/src/bin/lojix.rs` comments say inline/NOTA-file text rides the optional `nota-text` feature, but the code has no feature-gated NOTA parse/render path.

Spirit exemplar:

- Spirit's CLI reads one NOTA argument, parses generated `Input`, sends binary rkyv to the daemon, decodes generated `Output`, and prints NOTA.
- The daemon never sees the NOTA.

Why it matters:

The CLI is supposed to be the daemon's thin human/agent adapter. Today it is mostly a binary-frame file sender. That prevents normal operator-facing calls such as `lojix (Query ...)` or `lojix (Deploy ...)` and hides the typed surface behind debug output.

Fix direction:

- Add feature-gated `nota-text` parsing/rendering in the CLI only.
- Parse inline NOTA and NOTA files into `signal-lojix` or `meta-signal-lojix` roots.
- Print generated NOTA for replies.
- Keep signal/rkyv file input as an allowed binary edge if useful, but not as the only path.

### L3 — ordinary/meta short-header collision makes binary file classification ambiguous

Evidence:

`lojix/triad-port/src/client.rs` documents the problem directly:

```text
meta Deploy == ordinary Query == 0x0
```

The client tries decoding as `meta-signal-lojix` first, then as `signal-lojix`, relying on rkyv layout divergence rather than a structural tier discriminator.

Why it matters:

A modern component should not infer socket authority from a best-effort decode against colliding short headers. The authority tier is part of the boundary. The CLI can decide tier from the NOTA root or from an explicit binary envelope, but raw frame bytes with colliding root headers are under-specified.

Fix direction:

- Upstream: add a tier/channel discriminator to binary signal-file envelopes, or separate file forms for ordinary vs meta signal frames.
- Local short-term: after NOTA support lands, prefer NOTA root classification for human calls and reserve raw signal-file input for explicitly tiered paths.

### L4 — default dependency graphs still carry deprecated text/legacy crates

Evidence from `cargo tree --edges normal --no-default-features`:

- `lojix` default/no-default graph includes `nota-next`, `nota-codec`, `signal-lojix`, `meta-signal-lojix`, and `signal-frame`.
- `signal-lojix` default/no-default graph includes `nota-codec` and `signal-frame`.
- `meta-signal-lojix` default/no-default graph includes `nota-codec`, `signal-frame`, and `signal-lojix`.
- `signal-lojix` and `meta-signal-lojix` depend on `signal-frame` without `default-features = false`.
- `signal-lojix` and `meta-signal-lojix` depend on `nota-codec` unconditionally.

Spirit reference:

- `signal-spirit` and `meta-signal-spirit` make `nota-next` optional behind `nota-text` and set `signal-frame` `default-features = false`.
- Their dependency-boundary tests assert the default tree does not contain `nota-next`, `nota-codec`, or `signal-core`.
- `spirit` itself has `nota-next` optional behind `nota-text`, and `tests/dependency_surface.rs` asserts binary-only runtime builds do not pull it.

Why it matters:

Binary-only daemon and contract builds are part of the modern component boundary. Text codecs are for CLI/debug/audit edges, not default daemon or contract runtime. Unconditional `nota-codec` is especially suspicious because Spirit's modern contracts have moved away from it.

Fix direction:

- Make `nota-next` and any NOTA codec support optional under `nota-text` in Lojix contracts and daemon crate.
- Set `signal-frame = { ..., default-features = false }` in contract crates unless the `nota-text` feature opts in.
- Add dependency-boundary tests equivalent to Spirit's.

### L5 — Lojix is pinned to older schema/wire/runtime revisions than Spirit

Evidence from `Cargo.lock` selections:

- Lojix: `schema-rust-next` 0.4.0 in the daemon; 0.3.0 in both contracts.
- Spirit: `schema-rust-next` 0.5.3.
- Lojix contracts: `signal-frame` 0.1.0.
- Spirit: `signal-frame` 0.2.1.
- Lojix: `triad-runtime` 0.6.0.
- Spirit: `triad-runtime` 0.6.1.

Why it matters:

The user asked for deprecated dependencies/patterns. These are not merely old hashes; they correlate with missing modern features: generated daemon module, binary-only defaults, dependency-boundary discipline, and newer signal-frame behavior.

Fix direction:

- Bump Lojix contracts first to current `signal-frame` and `schema-rust-next`.
- Regenerate contract artifacts.
- Bump `lojix` to the same current generation stack as Spirit.
- Run/build new witnesses after each bump.

### L6 — sibling contracts are path dependencies

Evidence:

- `lojix/triad-port/Cargo.toml` uses:
  - `meta-signal-lojix = { path = "../../meta-signal-lojix/triad-port" }`
  - `signal-lojix = { path = "../../signal-lojix/triad-port" }`
- `meta-signal-lojix/triad-port/Cargo.toml` uses:
  - `signal-lojix = { path = "../../signal-lojix/triad-port" }`

Workspace rule:

Cross-repo Rust dependencies use git dependencies, not sibling `path` dependencies. Path dependencies make fresh clones non-portable and bypass the lock/pin story.

Fix direction:

- Replace sibling path dependencies with git dependencies on branch `main` or the appropriate development branch.
- Use local `[patch]` only in a local development overlay if needed, not in committed component manifests.

### L7 — durable SEMA is still in-memory `Mutex` state

Evidence:

- `lojix/INTENT.md` says redb/sema-engine durability remains the next storage cutover.
- `lojix/triad-port/src/lib.rs` defines `Store { state: Mutex<StoreState> }`.
- `StoreState` holds `Vec`-backed generated tables and monotonic counters.
- `lojix/triad-port/Cargo.toml` has no `sema-engine` dependency.
- The architecture says live generation set, GC roots, event log, and containers are persisted via `sema-engine`, but the implementation says in-memory.

Spirit exemplar:

- Spirit's `Store` opens a durable `.sema` database through `sema-engine`.
- Process-boundary tests prove persistence across daemon restart.

Why it matters:

Lojix owns “what generation is running on every node right now,” GC-root retention, and deploy event log. Those cannot be volatile if Lojix is to replace `lojix-cli` as the cluster-operator authority.

Fix direction:

- Add `sema-engine`/redb persistence for the four declared table families.
- Add a schema-version guard and restart persistence tests.
- Treat state digest as a real store marker, not `commit_sequence` mirrored into `state_digest`.

### L8 — subscription surface only opens tokens; it does not push events yet

Evidence:

- `signal-lojix/triad-port/schema/lib.schema` says schema-next cannot yet emit event/stream roots, so Watch/Unwatch are authored as an emittable token handshake and event payloads are defined as records.
- `lojix/triad-port/src/schema_runtime.rs` has `open_subscription` and `close_subscription` but no subscription registry/publisher path.
- `rg` finds no `SubscriptionEvent`, `StreamingFrame`, or event publisher usage in Lojix runtime.

Spirit exemplar:

- Spirit's emitted daemon owns subscription registry, retained writer plumbing, stream event frames, and real daemon-pushed `Output::Event(IntentEvent)` frames.

Why it matters:

Lojix's intent says push, never poll. Today `WatchDeployments`/`WatchCacheRetention` are subscription-token handshakes, not push delivery. Consumers still have to poll `ReadEventLog` or reconnect ad hoc.

Fix direction:

- Upgrade schema/signal-frame support so `signal-lojix` can declare real stream/event relations.
- Generate and implement event frame emission.
- Publish deployment and retention events downstream of committed writes.

### L9 — daemon shell is handwritten instead of schema-emitted

Evidence:

- Lojix `build.rs` emits only `nexus` and `sema` runtime modules through `GenerationPlan::daemon_runtime`.
- `src/daemon.rs` hand-writes listener binding, request loop, decode/execute/encode routing, and ordinary/meta dispatch.
- Spirit emits `src/schema/daemon.rs` and hand-writes only the `ComponentDaemon` hooks.

Why it matters:

Lojix uses `triad-runtime`, so this is not a legacy blocking shell. But it has not adopted the modern shared daemon spine that Spirit now proves: binary configuration argv parsing, generated binder, lifecycle hooks, subscription registry, retained writers, and `ExitReport` entry.

Fix direction:

- After contract/version bumps, add a generated daemon module for Lojix.
- Move Lojix-specific behavior behind `ComponentDaemon`-style hooks.
- Keep component logic in `SchemaRuntime`/Store; let the shared emitter own daemon shell repetition.

### L10 — contract witness coverage is missing

Evidence:

- `signal-lojix/triad-port` has no `tests/` directory.
- `meta-signal-lojix/triad-port` has no `tests/` directory.
- Their `ARCHITECTURE.md` and `INTENT.md` require round-trip witnesses.

Spirit reference:

- `signal-spirit` has `tests/round_trip.rs`, `tests/migration.rs`, `tests/frame.rs`, `tests/dependency_boundary.rs`, and daemon-configuration tests.
- `meta-signal-spirit` has round-trip, frame, and dependency-boundary tests.

Why it matters:

Contracts are the most expensive surface to get wrong. Without rkyv/NOTA round trips, verb-head assertions, dependency-boundary tests, and shared-type import tests, drift in generated artifacts can silently become the contract.

Fix direction:

- Add rkyv frame round trips for every request/reply root.
- Add NOTA round trips behind `nota-text`.
- Add verb-head tests for `Query`, `WatchDeployments`, `Deploy`, `Pin`, etc.
- Add dependency-boundary tests proving default binary-only graphs.
- Add meta/import tests proving shared deploy nouns come from `signal-lojix` once.

### L11 — no repo-root flake/Nix check surface

Evidence:

- `lojix/AGENTS.md` says there is no repo flake yet; use the cargo suite under `triad-port/`.
- The audit found `triad-port/Cargo.toml` and no root `Cargo.toml`/`flake.nix` for Lojix triad repos.
- Lojix tests include ignored live smoke tests, but not a Nix flake check surface like Spirit's.

Spirit reference:

- Spirit has `flake.nix`, root `Cargo.toml`, Nix integration tests, process-boundary tests, and dependency-surface tests.

Why it matters:

The deployment orchestrator should be one of the most reproducibly tested components. Cargo-only tests are not enough in this workspace because Nix builds, closure evaluation, binary package composition, and process-boundary behavior are the actual acceptance surface.

Fix direction:

- Graduate the crate from `triad-port/` to the repo root or make the root flake explicitly package/check the triad-port crate.
- Add pure Nix checks for build, generated artifact freshness, dependency boundary, and contract round trips.
- Keep live Nix/network deploy smoke as named ignored/stateful outputs.

### L12 — docs and generated-version metadata drift

Evidence:

- `lojix/triad-port/Cargo.toml` package version is `0.3.0`, but `lojix/triad-port/build.rs` passes version `0.2.0` into `GenerationPlan::daemon_runtime`.
- `signal-lojix/ARCHITECTURE.md` still contains a “MUST IMPLEMENT — three-layer migration” section whose candidate shape says public roots include `Deploy`, `Pin`, `Unpin`, and `Retire`, while the implemented schema correctly moved those to `meta-signal-lojix`.
- `lojix/triad-port/tests/build_smoke.rs` comments say production override materialization is deferred, while `lojix/ARCHITECTURE.md` and `tests/horizon_materialization_contract.rs` say materialization is now present.

Why it matters:

Version metadata and architecture docs are part of the component's operational truth. Stale text causes agents to implement the wrong next slice, and stale generated version metadata undermines package/version reports.

Fix direction:

- Drive generated version from `CARGO_PKG_VERSION` or update it with every package bump.
- Refresh `signal-lojix/ARCHITECTURE.md` to state the current ordinary/meta split positively, without the stale migration candidate.
- Refresh smoke-test comments to distinguish direct fixture build path from production materialization path accurately.

## Recommended fix order

1. Contract dependency modernization: bump `signal-frame` / `schema-rust-next`, remove unconditional `nota-codec`, disable default `signal-frame` text features, and add dependency-boundary tests.
2. Contract witnesses: add rkyv/NOTA round-trip tests for ordinary and meta roots.
3. CLI text edge: implement feature-gated NOTA parse/render so humans and agents can call `lojix` normally.
4. Binary daemon startup: move daemon configuration to a rkyv contract type and add a writer helper; make `lojix-daemon` reject NOTA startup.
5. Generated daemon shell: move from handwritten socket loop to the Spirit-style emitted daemon module plus component hooks.
6. Durable SEMA: replace `Mutex<StoreState>` with `sema-engine`/redb and add restart-persistence tests.
7. Streaming: upgrade schema/signal-frame support for real event frames and publish deployment/cache-retention events.
8. Repo packaging: graduate `triad-port/` to a root package/flake check surface and replace path dependencies.
9. Documentation/version cleanup: align architecture text and generated version strings with the implemented state.

## Production posture

Lojix is a strong implementation-stage port, not yet a modern production component in Spirit's sense. It is appropriate for continued local triad-port development and non-activating tests. It should not become the cluster deploy authority until binary daemon startup, default dependency boundaries, durable SEMA, CLI NOTA surface, and contract witnesses are fixed.
