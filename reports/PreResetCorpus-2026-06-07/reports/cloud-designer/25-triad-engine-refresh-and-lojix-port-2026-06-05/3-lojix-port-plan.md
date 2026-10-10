# lojix port plan — building the full triad component under the post-asschema engine model

The exact file list to build the lojix component under the new schema-rust-next
0.1.13 model, each file mapped to its `cloud`-template counterpart. The working
reference is the freshly-rebuilt `cloud` component (cargo build exit 0; both
`cloud` and `cloud-daemon` binaries produced — see
`1-new-triad-composition-guide.md`). The two daemon schema drafts that this plan
produces live alongside it at
`drafts/lojix.nexus.schema` and `drafts/lojix.sema.schema`; the Phase-1 GREEN
wire contracts are at `../24-lojix-wire-contracts-2026-06-05/drafts/`.

Read order before building: the composition guide (`1-...`), then this plan,
then the two schema drafts. The guide is HONEST that `cloud` is mid-migration
(its §6) — this plan inherits that honesty and routes the port AROUND the
inline `Store` / two-listener tail, not through it.

## 1. The three repositories

Three repos make the lojix triad (`skills/component-triad.md` component triad
rule; the contract-crate / daemon-crate split is the cloud layout at
`cloud/Cargo.toml:10-21`, `signal-cloud/Cargo.toml:9-10`):

| Repo | Role | Cloud-template counterpart |
|---|---|---|
| `signal-lojix` | ordinary wire contract (`WireContract`) | `signal-cloud` |
| `meta-signal-lojix` | meta policy wire contract (`WireContract`) | `meta-signal-cloud` |
| `lojix` | daemon crate (runtime + two bins) | `cloud` |

The contract crates carry typed wire vocabulary and ZERO runtime; the daemon
crate owns the runtime, the engines, the schema, and the two binaries. Both
contract `lib.schema` drafts already exist (`24-.../drafts/`) and their
`lib.schema` naming already matches `cloud` — they emit `lib`, consumed by the
daemon as `signal-lojix:lib:*` / `meta-signal-lojix:lib:*`, exactly as
`cloud/schema/nexus.schema:8-21` imports `signal-cloud:lib:*`.

## 2. signal-lojix crate — modeled on signal-cloud

Wire-contract emission target. Each file maps 1:1 to signal-cloud.

| Path | Role | signal-cloud counterpart |
|---|---|---|
| `Cargo.toml` | `links = "signal-lojix"`, `build = "build.rs"`, `[lib] name = "signal_lojix"` | `signal-cloud/Cargo.toml:9-14` |
| `build.rs` | `CargoSchemaMetadata::new("signal-lojix").emit_schema_directory(...)` + `GenerationPlan::wire_contract(root, "signal-lojix", "0.1.0")` + `.write_or_check("SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS")` | `signal-cloud/build.rs:20-32` |
| `schema/lib.schema` | the authored ordinary wire schema (ALREADY DRAFTED) | `signal-cloud/schema/lib.schema` |
| `src/lib.rs` | crate docs + `pub mod schema;` exposing the generated module; wire-noun newtypes / any hand-written surface the daemon's legacy bridge needs | `signal-cloud/src/lib.rs:1-11` |
| `src/schema/mod.rs` | `pub mod lib;` | `signal-cloud/src/schema/mod.rs:1` |
| `src/schema/lib.rs` | CHECKED-IN generated wire types (emitted from `lib.schema`) | emitted by `build.rs`, checked in |
| `tests/round_trip.rs` | rkyv + NOTA round-trips | per component-triad |

`Cargo.toml` deps mirror `signal-cloud/Cargo.toml:20-27`: `nota-codec`,
`rkyv` (the exact feature set at `signal-cloud/Cargo.toml:23`), `signal-frame`,
and `schema-rust-next` as the sole build-dependency. The `nota-text` feature +
optional `nota-next` follow the same pattern (`signal-cloud/Cargo.toml:16-22`).

The PUBLISH side of the Cargo `links` seam: `emit_schema_directory` prints
`cargo::metadata=schema-dir=<root>/schema` (`schema-rust-next/src/build.rs:244-247`);
because the crate declares `links = "signal-lojix"`, Cargo re-exposes it to
direct dependents as `DEP_SIGNAL_LOJIX_SCHEMA_DIR`
(`schema-rust-next/src/build.rs:257-269` — uppercase, `-`→`_`).

## 3. meta-signal-lojix package — modeled on meta-signal-cloud

Identical wire-contract shape with `links = "meta-signal-lojix"`. The decision
that fixes its dependency form is `11yimmwp4pueiudhl30`: the meta-signal crate
is a PATH-DEP package that cross-imports the ordinary contract's shared types
via `signal-lojix:lib:TypeName` (precedent: `meta-signal-cloud/Cargo.toml:24`
takes `signal-cloud` as a git dep and the cloud meta schema imports
`signal-cloud:lib:*`; the lojix decision makes that a path dep during the
single-workspace build).

| Path | Role | meta-signal-cloud counterpart |
|---|---|---|
| `Cargo.toml` | `links = "meta-signal-lojix"`, `[lib] name = "meta_signal_lojix"`, **path dep on `signal-lojix`** per decision `11yimmwp4pueiudhl30` | `meta-signal-cloud/Cargo.toml:9-14,24` |
| `build.rs` | `CargoSchemaMetadata::new("meta-signal-lojix").emit_schema_directory(...)` + `GenerationPlan::wire_contract(root, "meta-signal-lojix", "0.1.0")` + `.write_or_check("META_SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS")` | `meta-signal-cloud/build.rs:20-32` |
| `schema/lib.schema` | the authored meta wire schema (ALREADY DRAFTED) | `meta-signal-cloud/schema/lib.schema` |
| `src/lib.rs` | crate docs + `pub mod schema;` | `meta-signal-cloud/src/lib.rs` |
| `src/schema/mod.rs` | `pub mod lib;` | same |
| `src/schema/lib.rs` | CHECKED-IN generated wire types | emitted, checked in |
| `tests/round_trip.rs` | rkyv + NOTA round-trips | per component-triad |

Note: meta-signal-cloud takes `signal-cloud` as a GIT dep
(`meta-signal-cloud/Cargo.toml:24`). For lojix, decision `11yimmwp4pueiudhl30`
makes this a PATH dep so the wire-contract pair builds together as one
workspace unit; `build.rs` is otherwise byte-identical in shape. The meta
crate's own `build.rs` does NOT register the ordinary contract as a dependency
schema (a wire-contract emission has no dependency-schema concept — only the
daemon does); the cross-import resolves through the meta schema's own
`schema/lib.schema` import block (`meta-signal-lojix.lib.schema:43-56`) at
authoring time, which the build's `ImportResolver` resolves locally because the
two `schema/` dirs sit in the same workspace.

## 4. lojix daemon crate — modeled on cloud

The runtime crate: schema, build seam, engines, two bins.

| Path | Role | cloud counterpart |
|---|---|---|
| `Cargo.toml` | `[lib] name = "lojix"` + two `[[bin]]`: `lojix-daemon`, `lojix`; deps on `signal-lojix` + `meta-signal-lojix` (path), `triad-runtime`, `sema-engine`, `nota-codec`/`nota-config`, `rkyv`, `thiserror`; `schema-rust-next` build-dep | `cloud/Cargo.toml:10-45` |
| `build.rs` | `daemon_runtime` plan with BOTH dependency schemas (§4.1) | `cloud/build.rs:20-122` |
| `schema/nexus.schema` | daemon Nexus plane (DRAFTED — `drafts/lojix.nexus.schema`) | `cloud/schema/nexus.schema` |
| `schema/sema.schema` | daemon SEMA plane (DRAFTED — `drafts/lojix.sema.schema`) | `cloud/schema/sema.schema` |
| `src/schema/mod.rs` | `pub mod nexus; pub mod sema;` | `cloud/src/schema/mod.rs:1-2` |
| `src/schema/nexus.rs` | CHECKED-IN generated Nexus runtime (`@generated`) | `cloud/src/schema/nexus.rs:1` |
| `src/schema/sema.rs` | CHECKED-IN generated SEMA runtime (`@generated`) | `cloud/src/schema/sema.rs:1` |
| `src/schema_runtime.rs` | hand-implemented `SchemaRuntime` (NexusEngine + SemaEngine) | `cloud/src/schema_runtime.rs:6-374` |
| `src/lib.rs` | crate root, `Error` enum, `DaemonConfiguration`, `Store` (durable state on sema-engine), module declarations | `cloud/src/lib.rs:28-103` |
| `src/effects.rs` | the deploy-pipeline IO (nix eval/build, copy-closure, activate, gc, flake-auth) lifted into `run_effect` arms — NEW, no cloud counterpart to copy (cloud's provider IO is still inline — guide §6b) | conceptual: `cloud/src/cloudflare.rs` lifted into `run_effect` |
| `src/daemon.rs` | the daemon loop — see §4.4 BLOCKER (single vs two listener) | `cloud/src/daemon.rs` (do NOT copy the two-listener shape) |
| `src/bin/lojix-daemon.rs` | daemon entry — single NOTA arg → daemon run | `cloud/src/bin/cloud-daemon.rs:11-14` |
| `src/bin/lojix.rs` | CLI entry — `ComponentArgument` flow (NOT the legacy `signal_cli!` bridge) | `cloud/src/bin/cloud.rs:1-9` (shape only; see §4.5) |

### 4.1 The daemon build.rs seam, exactly

Copy `cloud/build.rs:20-122` structure verbatim, substituting names. The
`ContractSchemaDependencies` / `MissingContractSchemas` two-struct realization
(`cloud/build.rs:41-122`) is the method-only (no-free-function) form of the
two-dependency case and ports directly:

- `rerun-if-changed` for `schema/nexus.schema`, `schema/sema.schema`,
  `src/schema/nexus.rs`, `src/schema/sema.rs` (`cloud/build.rs:21-24`).
- `DependencySchema::from_cargo_metadata("signal-lojix", "signal-lojix", "0.1.0")`
  and `(... "meta-signal-lojix" ...)` — reads `DEP_SIGNAL_LOJIX_SCHEMA_DIR` /
  `DEP_META_SIGNAL_LOJIX_SCHEMA_DIR` (`cloud/build.rs:49-60`); returns
  `Ok(None)` when absent so the daemon gracefully SKIPS + warns on a fresh
  checkout (`cloud/build.rs:81-110`, mechanism at
  `schema-rust-next/src/build.rs:205-207`).
- `cargo:rerun-if-env-changed` for both `DEP_*_SCHEMA_DIR` vars
  (`cloud/build.rs:64-67`).
- `GenerationPlan::daemon_runtime(root, "lojix", "0.1.0").with_dependency_schema(ordinary).with_dependency_schema(meta)`
  (`cloud/build.rs:77-79`). `daemon_runtime` attaches `nexus_runtime()` +
  `sema_runtime()` module emissions (`schema-rust-next/src/build.rs:41-49`);
  lojix needs NO `signal_runtime_module` (like cloud, it reuses the contracts'
  wire surface).
- `GenerationDriver::new(plan).generate().write_or_check("LOJIX_UPDATE_SCHEMA_ARTIFACTS")`
  (`cloud/build.rs:33-37`).

### 4.2 The SchemaRuntime engine — what lojix hand-implements

`SchemaRuntime` is one data-bearing noun implementing the two engine traits on
itself (`cloud/src/schema_runtime.rs:6-12,299-374`). For lojix the state it
carries is the daemon's durable handles (the sema-engine `Engine` + the four
tables), not in-memory `Vec`s — but the trait surface is identical:

- `nexus::NexusEngine` (generated trait at the lojix analog of
  `cloud/src/schema/nexus.rs:733-774`):
  - `decide(Nexus<Work>) -> Nexus<Action>` — the routing brain
    (`cloud/src/schema_runtime.rs:339-353`). `SignalArrived` →
    `decide_signal_arrival` which fans `OrdinaryInput`/`MetaInput`
    (`schema_runtime.rs:72-106`). For lojix: ordinary `Query` →
    `CommandSemaRead(QueryGenerations)`, ordinary `CheckHostKeyMaterial` →
    `CommandSemaRead(CheckKeyMaterial)`, meta `Deploy` →
    `CommandSemaWrite(RecordDeploySubmitted)` then drive the effect pipeline,
    meta `Pin`/`Unpin`/`Retire` → the matching `CommandSemaWrite`.
  - `apply_sema_write` / `observe_sema_read` (`schema_runtime.rs:300-314`) —
    delegate to the SEMA engine, threading `OriginRoute`.
  - `run_effect(CommandEffect) -> EffectCompleted` — THE EFFECT HANDLER. This
    is where the deploy pipeline lives: each `EffectCommand` variant
    (`ResolveFlakeAuth`/`NixEval`/`NixBuild`/`CopyClosure`/`ActivateGeneration`/
    `PathInfoGc`) dispatches to its IO and returns a typed `EffectResult`
    (`drafts/lojix.nexus.schema` EffectCommand/EffectResult). UNLIKE cloud
    (whose `run_effect` is a stub — `schema_runtime.rs:316-328`), lojix MUST
    do real IO here (§4.3).
  - `budget_exhausted_reply(ContinuationExhausted) -> ReplyToSignal`
    (`schema_runtime.rs:330-337`) — the typed reply when the continuation
    budget (default limit 32 — `triad-runtime/src/runner.rs:1`) is spent. For
    lojix: an ordinary `QueryRejected` or a meta `DeployRejected` carrying the
    current `DatabaseMarker`.
- `sema::SemaEngine` (generated trait at the lojix analog of
  `cloud/src/schema/sema.rs:1032-1062`): `apply_inner` (write) +
  `observe_inner` (read), each threading `OriginRoute`
  (`cloud/src/schema_runtime.rs:356-374`). These read/write the four tables on
  the sema-engine `Engine`.

The `RunnerEngines` adapter (`NexusRunnerAdapter`) and the
`execute`-drives-`Runner` glue are GENERATED into `src/schema/nexus.rs:776-820`
— lojix writes NONE of it. The recursive loop is the generated
`NexusEngine::execute` (`cloud/src/schema/nexus.rs:760-773`): it builds a
`Runner` from `continuation_limit()`, wraps `self` in the adapter, calls
`runner.drive(...)`, and wraps the reply as `NexusAction::reply_to_signal`.

The DEPLOY PIPELINE as the recursive loop: a meta `Deploy` →
`decide` emits `CommandSemaWrite(RecordDeploySubmitted)` → the write returns
`DeploySubmitted(AcceptedDeploy)` → `decide` on that completion emits
`CommandEffect(ResolveFlakeAuth)` → `run_effect` returns
`FlakeResolved` → `Continue` re-enters → `CommandEffect(NixEval)` →
`ClosureEvaluated` → `CommandEffect(NixBuild)` → `ClosureBuilt` →
`CommandEffect(CopyClosure)` → `CommandEffect(ActivateGeneration)` →
`CommandSemaWrite(RecordPhaseTransition)` at each stage → finally
`ReplyToSignal(Deployed)`. Each hop spends one continuation-budget step
(`triad-runtime/src/runner.rs:147-184`); the default 32 limit comfortably
covers the ~8-stage pipeline, but a multi-node fan-out deploy may need a raised
`continuation_limit()` override (flag for review — see §6).

### 4.3 Effects do real IO — lifting the deploy pipeline

The honest caveat from the guide (§6b): cloud's `run_effect` is a STUB and the
real Cloudflare HTTP lives inline in `Store` (`cloud/src/lib.rs:767-797`). A
faithful lojix port does the OPPOSITE — it BUILDS the effect handler for real.
Each `EffectCommand` arm in `src/effects.rs`:

- `ResolveFlakeAuth` → resolve the flake ref against the proposal source
  (intent `1orezxnzgedct1grkn4` names `ResolveFlakeAuth` as a pipeline stage).
- `NixEval` → `nix eval` the system/home attribute → `EvaluatedClosure`.
- `NixBuild` → `nix build`; the `BuildTarget` discriminant
  (`drafts/lojix.nexus.schema` `BuildTarget [Local (Remote BuilderNode)]`)
  selects a LOCAL dispatcher build when no builder is present, honoring the
  dropped hallucinated guard `783n` and the contract's no-local-build-guard
  discipline (`meta-signal-lojix.lib.schema:38-41`).
- `CopyClosure` → `nix copy --to ssh://<node>` → `CopiedClosure`.
- `ActivateGeneration` → activate via the `ActivationKind`
  (Switch/Boot/Test/BootOnce) → `ActivatedGeneration`.
- `PathInfoGc` → `nix path-info -r` + two-phase GC respecting narinfo TTL
  (`lojix/ARCHITECTURE.md:53-55`) → `GarbageCollected`.

Any stage failure returns `EffectFailed(EffectFailure{ stage, detail })`, which
`decide` translates into a meta `DeployRejected` / the matching phase event.

### 4.4 The daemon loop — BLOCKER, see §6

`src/daemon.rs` is where the template GAP bites. Do NOT copy
`cloud/src/daemon.rs:23-43` (two raw `UnixListener` threads calling
`Store::handle_*` inline — the legacy bypass the guide flags at §6a). The
new-model target is a `DaemonRuntime` impl that decodes a wire frame into
`NexusWork::SignalArrived`, calls `NexusEngine::execute` (which drives the
`Runner`), and encodes the `ReplyToSignal` back — over `triad-runtime`'s
`SingleListenerDaemon` (`triad-runtime/src/daemon.rs:11-21,100-117`). But
lojix, like cloud, has an ordinary socket AND an owner/meta socket
(`lojix/ARCHITECTURE.md:41` names one socket today, but the triad's
authority-tiering needs two — `skills/component-triad.md` two-socket rule). The
runtime ships only `SingleListenerDaemon` (single socket). This reconciliation
is UNBUILT in the template (guide §6a) and is the load-bearing blocker (§6).

### 4.5 The CLI — new-model, not the legacy bridge

`src/bin/lojix.rs` + the client module use `ComponentArgument`
(`triad-runtime/src/argument.rs:57-104` — exactly one NOTA arg, classified as
inline NOTA / NOTA file / signal-encoded file) and the generated
`signal-lojix` / `meta-signal-lojix` `Input`/`Output` types. Do NOT port
`cloud/src/client.rs` — it rides the legacy `signal_cli!` `Frame` path
(`cloud/src/client.rs:22-60`) that the guide §6c flags as the migration bridge,
not the new-model CLI reference.

## 5. Checked-in generated-artifact discipline

Generated Rust is CHECKED IN under `src/schema/` in all three crates (the
`// @generated by schema-rust-next` header — `cloud/src/schema/nexus.rs:1`).
The discipline (`schema-rust-next/ARCHITECTURE.md:89-93,146-152`):

- `write_or_check(<UPDATE_ENV>)` compares each generated file against the
  working tree (`schema-rust-next/src/build.rs:344-358`); on a normal build the
  env var is absent so a mismatch FAILS with `StaleGeneratedArtifact` naming
  the update variable (`build.rs:478-484`).
- The per-crate UPDATE env vars: `SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS`,
  `META_SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS`, `LOJIX_UPDATE_SCHEMA_ARTIFACTS`
  — set one to flip `FreshnessCheck` into write mode and rewrite the checked-in
  files (`build.rs:525-534`).
- The authored `.schema` is round-tripped through generated schema text + rkyv
  archive bytes as internal codec witnesses (`build.rs:425-448`), but those are
  NOT checked-in outputs — only the Rust files are
  (`ARCHITECTURE.md:146-152`).

Change loop: edit `.schema` → build with the UPDATE var set → commit the
regenerated `src/schema/*.rs` → build without the var to confirm freshness.

## 6. Blockers and template gaps

### BLOCKER (load-bearing) — two-socket daemon vs single-listener runtime

`triad-runtime` ships ONLY `SingleListenerDaemon` (one socket —
`triad-runtime/src/daemon.rs:11-21`), but a triad component needs TWO
authority-tiered sockets: ordinary (peer-callable `signal-lojix`) and
owner/meta (`meta-signal-lojix` — Deploy/Pin/Unpin/Retire). cloud worked around
this by NOT using the runtime daemon at all — it kept the legacy two-listener
loop (`cloud/src/daemon.rs:23-43`) and bypasses the schema engine entirely
(guide §6a). So there is NO template to copy for "schema-engine-driven daemon
with two authority-tiered sockets" — that glue is unbuilt everywhere. lojix
cannot wire its daemon loop to the schema engine until this is resolved. Two
candidate resolutions to escalate:
1. Extend `triad-runtime` with a `DualListenerDaemon` (ordinary + owner
   sockets, each tier tagging arrivals into the same `NexusWork::SignalArrived`
   stream via the `SignalInput` union the nexus schema already declares —
   `drafts/lojix.nexus.schema` `SignalInput`).
2. Have the lojix daemon bind two `SingleListenerDaemon`s sharing one
   `SchemaRuntime` behind a mutex (mirrors cloud's shared-`Store`-behind-`Mutex`
   pattern at `cloud/src/lib.rs:9` but driving `NexusEngine::execute` instead of
   inline `Store`).
Recommendation: option 1 (extend the runtime) — the two-socket need is
universal to every triad component, so it belongs in `triad-runtime`, not
re-solved per component. This is a `triad-runtime` change that is a PREREQUISITE
for any port that wires the daemon loop to the schema engine, and it should land
before (or alongside) lojix's `src/daemon.rs`.

### GAP — streaming / subscription events (carried, not blocking the build)

The signal-lojix contract carries Watch/Unwatch as a request→`SubscriptionToken`
handshake because schema-next cannot yet emit a daemon-pushed event frame
(`signal-lojix.lib.schema:11-20`). The SEMA `EventLogTable` + the two event
payloads (`DeploymentPhaseEvent`, `CacheRetentionTransitionEvent`) are modeled,
so the daemon can ANSWER a `ReadEventLog` poll and mint subscription tokens, but
it cannot PUSH events until the schema-next event-frame-emission enhancement
lands (the named follow-on on the lojix path). The port builds GREEN without
push; push is a later wire-up. Not a build blocker — flagged so it is not
mistaken for complete.

### QUESTION resolved — inline Store vs Nexus runner

The task asks whether lojix should follow cloud's mid-migration inline `Store`
or go straight to the Nexus runner. Answer: go STRAIGHT to the Nexus runner. The
inline `Store` (`cloud/src/lib.rs:449-1288`) + two-listener loop + inline
provider IO are the migration TAIL the guide §6 explicitly says NOT to
replicate. lojix is a fresh build with no legacy CLI to bridge, so it should
port only the new-model parts (the `SchemaRuntime` engine shape, the schema
files, the `build.rs` seam, the checked-in generated artifacts) and BUILD the
daemon glue that cloud still lacks (the §6 BLOCKER). A `Store` noun still exists
in lojix — but as the sema-engine-backed durable-state holder the `SemaEngine`
impl reads/writes, NOT as a parallel inline request engine.

### Minor — continuation budget for fan-out deploys

The deploy pipeline is ~8 stages, well under the default 32 continuation limit
(`triad-runtime/src/runner.rs:1`). A multi-node fan-out (one Deploy touching N
nodes) would multiply stages; if lojix ever fans a single Deploy across nodes
in one continuation chain, override `continuation_limit()`
(`cloud/src/schema/nexus.rs:749-751`) or split per-node deploys into separate
SignalArrived works. Flag for the implementer; not a blocker for the
single-node path.
