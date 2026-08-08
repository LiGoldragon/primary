# New triad composition guide — composing a component under the post-asschema engine model

The authoritative reference for composing a triad component under the NEW
schema-rust-next 0.1.13 model (asschema removed; schema-object-trait lowering
+ source-driver emission; `triad-runtime` owning the recursive Runner). The
working reference is the freshly-rebuilt `cloud` component, which BUILDS
end-to-end (cargo build exit 0; both `cloud` and `cloud-daemon` binaries
produced). Every claim below cites file:line in that template plus
`triad-runtime` and `schema-rust-next`.

This guide is HONEST about where `cloud` is still mid-migration (§6): the
schema-driven Nexus/SEMA engine is fully generated and hand-implemented, but
the daemon loop does NOT yet run it — the `Store` answers wire requests
inline, and the Cloudflare call is inline rather than a `CommandEffect`. A
faithful port targets the schema-driven engine, NOT the inline `Store`.

## 1. Component file layout

Three repositories make the repo triad (per `skills/component-triad.md:56-75`).
The contract crates carry typed wire vocabulary and zero runtime; the daemon
crate owns the runtime, the CLI, and the engine state.

### Contract crates — `signal-<component>` and `meta-signal-<component>`

Each contract crate is a `WireContract` emission target: wire nouns, derives,
NOTA/rkyv codecs, short headers, signal-frame encode/decode, and NOTHING else
(`schema-rust-next/ARCHITECTURE.md:96-98`). Layout for `signal-cloud`:

| Path | Role | Evidence |
|---|---|---|
| `Cargo.toml` | `links = "signal-cloud"`, `build = "build.rs"` | `signal-cloud/Cargo.toml:9-10` |
| `build.rs` | publishes schema dir + emits `WireContract` | `signal-cloud/build.rs:20-32` |
| `schema/lib.schema` | the authored wire schema | `signal-cloud/schema/lib.schema:1-59` |
| `src/lib.rs` | hand-written wire nouns + `signal_channel!` + `pub mod schema` | `signal-cloud/src/lib.rs:11,327-341` |
| `src/schema/mod.rs` | `pub mod lib;` | `signal-cloud/src/schema/mod.rs:1` |
| `src/schema/lib.rs` | CHECKED-IN generated wire types (from `lib.schema`) | emitted by `build.rs` |
| `tests/round_trip.rs` | rkyv + NOTA round-trips | per `skills/component-triad.md:69` |

`meta-signal-cloud` is the identical shape with `links = "meta-signal-cloud"`
(`meta-signal-cloud/Cargo.toml:9-10`) and its own `build.rs` calling
`GenerationPlan::wire_contract(... "meta-signal-cloud" ...)`
(`meta-signal-cloud/build.rs:24-31`). The meta-signal repo is optional — it
appears only when the component has an owner that issues policy
(`skills/component-triad.md:110-114`). `cloud` has both.

Note that `signal-cloud/src/lib.rs` today carries BOTH a hand-written wire
surface (the `signal_channel!` macro at `:327-341` producing `Operation` /
`Reply` / `ChannelRequest` / `ChannelReply` over `signal_frame`) AND the
generated `schema::lib` module. The hand-written `signal_channel!` surface is
what the legacy daemon/CLI wire path consumes; the generated `schema::lib`
module is what the daemon's Nexus/SEMA schema imports. Both coexist during
migration (§6).

### Daemon crate — `<component>`

The runtime crate. Layout for `cloud` (`cloud/Cargo.toml:10-21`,
`cloud/src/` listing):

| Path | Role | Evidence |
|---|---|---|
| `Cargo.toml` | `[lib]` + two `[[bin]]`: `cloud-daemon`, `cloud` | `cloud/Cargo.toml:10-20` |
| `build.rs` | emits `daemon_runtime` (nexus+sema) | `cloud/build.rs:20-38` |
| `schema/nexus.schema` | daemon Nexus plane schema | `cloud/schema/nexus.schema:1-50` |
| `schema/sema.schema` | daemon SEMA plane schema | `cloud/schema/sema.schema:1-68` |
| `src/schema/mod.rs` | `pub mod nexus; pub mod sema;` | `cloud/src/schema/mod.rs:1-2` |
| `src/schema/nexus.rs` | CHECKED-IN generated Nexus runtime (`@generated`) | `cloud/src/schema/nexus.rs:1` |
| `src/schema/sema.rs` | CHECKED-IN generated SEMA runtime (`@generated`) | `cloud/src/schema/sema.rs:1` |
| `src/schema_runtime.rs` | hand-implemented `SchemaRuntime` (NexusEngine + SemaEngine) | `cloud/src/schema_runtime.rs:6-374` |
| `src/lib.rs` | crate root, `DaemonConfiguration`, the inline `Store` | `cloud/src/lib.rs:28-36,95-103,449` |
| `src/daemon.rs` | the (legacy) two-listener daemon loop | `cloud/src/daemon.rs:14-201` |
| `src/client.rs` | CLI client (legacy `signal-frame` path) | `cloud/src/client.rs:29-60` |
| `src/frame_io.rs` | length-prefixed frame read/write helpers | `cloud/src/frame_io.rs:39-71` |
| `src/cloudflare.rs`, `src/cloudflare_cli.rs` | provider IO (inline today) | `cloud/src/lib.rs:29-32` |
| `src/bin/cloud-daemon.rs` | daemon entry — single NOTA arg → `Daemon::run` | `cloud/src/bin/cloud-daemon.rs:11-14` |
| `src/bin/cloud.rs` | CLI entry — `Client::run_from_environment` | `cloud/src/bin/cloud.rs:1-9` |

Binary naming follows `skills/component-triad.md:124-211`: CLI binary is the
unprefixed `cloud`; daemon binary is `cloud-daemon`. The CLI is the daemon's
thin first client, not a triad leg.

## 2. The build.rs pattern, exactly

Two distinct `build.rs` shapes — one for contract crates, one for the daemon —
both driven by `schema_rust_next::build`.

### Contract crate build.rs (`signal-cloud/build.rs`)

```
println!("cargo:rerun-if-changed=schema/lib.schema");                  // :21
CargoSchemaMetadata::new("signal-cloud").emit_schema_directory(&root); // :22  -> publishes schema dir
GenerationDriver::new(GenerationPlan::wire_contract(&root, "signal-cloud", "0.1.0")) // :23-27
    .generate().expect(...)                                            // :28-29
    .write_or_check("SIGNAL_CLOUD_UPDATE_SCHEMA_ARTIFACTS")            // :30
    .expect("checked-in signal-cloud schema artifacts are fresh");     // :31
```

`emit_schema_directory` is the PUBLISH side of the Cargo `links` seam: it
prints `cargo::metadata=schema-dir=<crate_root>/schema`
(`schema-rust-next/src/build.rs:244-247`). Because the crate declares
`links = "signal-cloud"` (`signal-cloud/Cargo.toml:9`), Cargo re-exposes that
metadata to DIRECT dependents as the env var `DEP_SIGNAL_CLOUD_SCHEMA_DIR`
(`schema-rust-next/src/build.rs:257-269` computes the variable name:
uppercase, `-`→`_`). This is how a contract crate publishes its schema
directory to the daemon (`schema-rust-next/ARCHITECTURE.md:138-145`).

### Daemon crate build.rs (`cloud/build.rs`)

```
println!("cargo:rerun-if-changed=schema/nexus.schema");   // :21
println!("cargo:rerun-if-changed=schema/sema.schema");    // :22
println!("cargo:rerun-if-changed=src/schema/nexus.rs");   // :23
println!("cargo:rerun-if-changed=src/schema/sema.rs");    // :24

// READ side of the links seam — pull each contract's published schema dir:
DependencySchema::from_cargo_metadata("signal-cloud", "signal-cloud", "0.1.0")        // :49-54
DependencySchema::from_cargo_metadata("meta-signal-cloud", "meta-signal-cloud", "0.1.0") // :55-60

println!("cargo:rerun-if-env-changed=DEP_SIGNAL_CLOUD_SCHEMA_DIR");       // :65
println!("cargo:rerun-if-env-changed=DEP_META_SIGNAL_CLOUD_SCHEMA_DIR");  // :66

GenerationPlan::daemon_runtime(crate_root, "cloud", "0.1.0")             // :77
    .with_dependency_schema(ordinary_signal)                            // :78
    .with_dependency_schema(meta_signal)                                // :79

GenerationDriver::new(plan).generate().expect(...)                       // :33-35
    .write_or_check("CLOUD_UPDATE_SCHEMA_ARTIFACTS")                     // :36
    .expect("checked-in cloud runtime schema artifacts are fresh");      // :37
```

Mechanism detail:

- `DependencySchema::from_cargo_metadata(crate_name, links_name, version)`
  reads `DEP_<LINKS>_SCHEMA_DIR` via `CargoSchemaMetadata`
  (`schema-rust-next/src/build.rs:197-209`). It returns `Ok(None)` when the
  var is absent (`:205-207`), so `cloud/build.rs` gracefully SKIPS generation
  and warns when a contract's metadata is missing
  (`cloud/build.rs:75-86,105-110`) rather than failing the build — important
  for a fresh checkout where contract crates have not yet emitted metadata.
- `GenerationPlan::daemon_runtime` attaches TWO module emissions:
  `ModuleEmission::nexus_runtime()` (`schema/nexus.schema` →
  `RustEmissionTarget::NexusRuntime`) and `ModuleEmission::sema_runtime()`
  (`schema/sema.schema` → `RustEmissionTarget::SemaRuntime`)
  (`schema-rust-next/src/build.rs:41-49,132-158`). A daemon that also carries
  a local Signal runtime adds `ModuleEmission::signal_runtime_module("signal")`
  explicitly (`schema-rust-next/ARCHITECTURE.md:129-131`); `cloud` does NOT —
  it has no `signal.schema` and reuses the contract's wire surface.
- `.with_dependency_schema(...)` registers each contract's published `schema/`
  dir into the `ImportResolver` (`schema-rust-next/src/build.rs:65-68,
  98-104,223-229`), so the daemon's `nexus.schema`/`sema.schema` can import
  contract roots by single-colon path (`signal-cloud:lib:Input`,
  `meta-signal-cloud:lib:Registration` — see
  `cloud/schema/nexus.schema:8-21`).
- `GenerationDriver.generate()` runs the load→lower→emit→round-trip-witness
  sequence per module (`schema-rust-next/src/build.rs:290-305,381-405`) and
  returns a `GeneratedPackage`.
- `.write_or_check(<UPDATE_ENV>)` is the freshness gate (§5).

A standalone single-contract daemon registers one `DependencySchema`; a daemon
with a meta-signal contract registers both, matching `cloud`. The
`ContractSchemaDependencies` / `MissingContractSchemas` structs in
`cloud/build.rs:41-122` are the template's tidy method-only realization of the
two-dependency case (no free functions; per the Rust discipline).

## 3. The nexus.schema and sema.schema shapes

These are daemon-LOCAL schema files (runtime implementation schema, not Signal
contracts — `cloud/schema/nexus.schema:1-4`). They import contract roots and
SEMA roots, then declare the daemon's decision / effect / state language.

### nexus.schema — the engine FEATURE CATALOG (record z6qu)

Per `skills/component-triad.md:857-872`, every internal engine feature is a
declared Nexus verb+object; the nexus schema is the one place the engine's
complete internal surface is readable. `cloud/schema/nexus.schema`:

- Imports (`:7-22`): the two Signal roots (`OrdinaryInput`/`OrdinaryOutput`
  from `signal-cloud:lib`, `MetaInput`/`MetaOutput` from `meta-signal-cloud:lib`),
  the four local SEMA roots (`cloud:sema:Sema{Read,Write}{Input,Output}`),
  plus effect payload types (`ZoneQuery`, `RecordQuery`, `PlanIdentifier`, …).
- Operation roots (`:23-24`): `[NexusWork]` (input) and `[NexusAction]`
  (output).
- `NexusWork` (`:48`) = `[SignalArrived SemaReadCompleted SemaWriteCompleted
  EffectCompleted]` — the four kinds of work that re-enter the engine.
- `NexusAction` (`:49`) = `[CommandSemaRead CommandSemaWrite CommandEffect
  ReplyToSignal Continue]` — the five-variant action set ratified by Spirit
  1486 (`skills/component-triad.md:1078-1104`).
- `SignalInput` (`:37`) = `[(OrdinaryInput OrdinaryInput) (MetaInput
  MetaInput)]` and `SignalOutput` (`:38`) — the unions that fold the ordinary
  and meta wire surfaces into one engine input/output.
- `EffectCommand` catalog (`:40-43`): `[CloudflareObserveZones
  CloudflareObserveRecords CloudflareApplyPlan]` with their payloads — the
  per-component effect vocabulary (external IO declared, not inlined).
- `EffectResult` (`:44-46`): `[ZonesObserved RecordsObserved (PlanApplied
  PlanApplied)]` — what each effect returns.

The re-entry protocol — `SignalArrived` → `Command*` → `Continue` — is the
recursive loop: a `SignalArrived` work decides a `CommandSemaRead/Write` or
`CommandEffect` action; the runner runs that command and feeds the result back
as the next `*Completed` work; `Continue(NexusWork)` re-enters
`decide` immediately in-process (`skills/component-triad.md:1106-1116`). The
generated `NexusAction::into_runner_next_step()` maps each action variant onto
the runtime `NextStep` (`cloud/src/schema/nexus.rs:721-731`).

### sema.schema — durable state plane

`cloud/schema/sema.schema`:

- Operation roots (`:34-35`): `[SemaReadInput SemaWriteInput]` (input) and
  `[SemaReadOutput SemaWriteOutput]` (output) — the split read/write halves.
- `SemaReadInput` (`:37-40`): `[Observe ObservePlan Validate]` — multi-variant
  (passes the "name two operations" interface test,
  `skills/component-triad.md:1230-1259`).
- `SemaWriteInput` (`:46-54`): the eight write operations (`RegisterAccount`,
  `RotateCredential`, `SetPolicy`, `PreparePlan`, `PrepareProjection`,
  `ApprovePlan`, `ApplyPlan`, `RetireAccount`).
- `SemaReadOutput` / `SemaWriteOutput` (`:42-56`): the typed reply unions.
- Table records (`:64-67`): `AccountPolicyTable`, `AccountBinding`,
  `PlanTable`, `StoredPlan` — the durable table shapes (policy state + working
  state, per `skills/component-triad.md:378-417`).
- `StateMarker` (`:60-62`): `{ CommitSequence * StateDigest * }` — the database
  marker that travels on every SEMA reply and that Nexus propagates back to the
  Signal response (`skills/component-triad.md:900-904`). Generated as
  `cloud/src/schema/sema.rs:128-137`.

## 4. How the daemon wires triad-runtime

### What `triad-runtime` provides (generic, same for every component)

- `Runner` + `ContinuationBudget` + `ContinuationLimit` +
  `ContinuationExhausted` — the recursive Nexus loop with a typed continuation
  budget (`triad-runtime/src/runner.rs:58-184`). `Runner::drive` loops on
  `decide_next_step`, dispatching `Reply` (return), `SemaWrite`/`SemaRead`/
  `RunEffect`/`Continue` (each spends one budget step via
  `spend_next_step` and on exhaustion returns `budget_exhausted_reply`)
  (`runner.rs:147-184,103-116`). Default limit 32 (`runner.rs:1`).
- `RunnerEngines` — the generic trait the runner drives, with associated types
  `Reply / SemaWrite / SemaRead / Effect / Work` and methods `decide_next_step`,
  `apply_sema_write`, `observe_sema_read`, `run_effect`,
  `budget_exhausted_reply` (`runner.rs:30-48`).
- `SingleListenerDaemon` / `BoundSingleListenerDaemon` / `DaemonRuntime` — the
  single-listener daemon runner: bind socket, `on_start`, serve streams via
  `DaemonRuntime::handle_stream`, `on_stop` (`triad-runtime/src/daemon.rs:11-21,
  72-162`). A daemon implements `DaemonRuntime` and hands it to
  `SingleListenerDaemon::run` (`daemon.rs:100-117`).
- `ComponentCommand` / `ComponentArgument` — the single-argument rule:
  `from_environment()` reads argv, `nota_argument()` / `signal_file_argument()`
  classify the one argument as inline NOTA, NOTA file, or signal-encoded file
  (`triad-runtime/src/argument.rs:57-104`). Exactly one arg or
  `ArgumentError::ArgumentCount` (`:96-103`).
- `LengthPrefixedCodec` + `FrameBody` + `MaximumFrameLength` — the 4-byte
  big-endian length-prefixed wire codec (`triad-runtime/src/frame.rs:79-122`).
- Trace transport — `TraceClient` / `TraceSocketListener` / `TraceLog` /
  `TraceFrame` / `TraceEventFrame` (`triad-runtime/src/trace.rs:16-313`).

### What the component HAND-IMPLEMENTS

The component supplies the three plane engines as trait impls on ONE
data-bearing noun. In `cloud` that noun is `SchemaRuntime`
(`cloud/src/schema_runtime.rs:6-12`), which implements:

- `nexus::NexusEngine` (`schema_runtime.rs:299-353`) — the generated trait at
  `cloud/src/schema/nexus.rs:733-774`. The component MUST hand-implement:
  - `decide(Nexus<Work>) -> Nexus<Action>` — the routing brain
    (`schema_runtime.rs:339-353`): `SignalArrived` → `decide_signal_arrival`,
    `Sema{Read,Write}Completed` → reply translation, `EffectCompleted` →
    `Continue`.
  - `apply_sema_write` / `observe_sema_read` (`schema_runtime.rs:300-314`) —
    delegating to the SEMA engine.
  - `run_effect(CommandEffect) -> EffectCompleted` (`schema_runtime.rs:316-328`)
    — THE EFFECT HANDLER: dispatches each declared `EffectCommand` variant
    (the three Cloudflare effects) to its result. (In `cloud` today these are
    stubbed to empty listings — §6.)
  - `budget_exhausted_reply(ContinuationExhausted) -> ReplyToSignal`
    (`schema_runtime.rs:330-337`) — the typed reply when the continuation
    budget is spent (cloud returns `RequestRejected(PlanExpired)`).
- `sema::SemaEngine` (`schema_runtime.rs:356-374`) — the generated trait at
  `cloud/src/schema/sema.rs:1032-1062`: `apply_inner` (write) and
  `observe_inner` (read), each threading the `OriginRoute` through.

### What is GENERATED (the `RunnerEngines` adapter)

The `RunnerEngines` impl is GENERATED, not hand-written. `schema-rust-next`
emits `NexusRunnerAdapter` (`cloud/src/schema/nexus.rs:776-820`), which wraps a
`&mut Engine: NexusEngine` plus the origin route and implements
`triad_runtime::RunnerEngines` by forwarding to the component's `NexusEngine`
methods. The generated default `NexusEngine::execute`
(`cloud/src/schema/nexus.rs:760-773`) builds a `Runner` from
`self.continuation_limit()`, constructs the adapter, calls `runner.drive(...)`,
and wraps the reply as a `NexusAction::reply_to_signal`. So the component
writes domain logic on `NexusEngine`; the runner wiring and the
`RunnerEngines` bridge are emitted. This is the concrete realization of
"component code becomes a one-line main" (`skills/component-triad.md:1117-1125`)
— minus the daemon loop, which is still hand-written here (§6).

## 5. Generated-artifact discipline

Generated Rust is CHECKED IN under `src/schema/` (both contract `lib.rs` and
daemon `nexus.rs`/`sema.rs` carry the `// @generated by schema-rust-next`
header — `cloud/src/schema/nexus.rs:1`, `cloud/src/schema/sema.rs:1`). The
discipline (`schema-rust-next/ARCHITECTURE.md:89-93,146-152`):

- `write_or_check(<UPDATE_ENV>)` compares each generated file against the
  working tree (`schema-rust-next/src/build.rs:344-358,472-495`). On a normal
  build the env var is absent, so a mismatch fails the build with
  `StaleGeneratedArtifact` naming the update variable
  (`build.rs:478-484,556-563`).
- Setting the per-component UPDATE env var (`CLOUD_UPDATE_SCHEMA_ARTIFACTS`
  for the daemon — `cloud/build.rs:36`; `SIGNAL_CLOUD_UPDATE_SCHEMA_ARTIFACTS`
  for the contract — `signal-cloud/build.rs:30`) flips `FreshnessCheck` into
  write mode, rewriting the checked-in files (`build.rs:525-534,472-477`).
- The driver ALSO round-trips the authored `.schema` through generated schema
  text and rkyv archive bytes as internal codec witnesses
  (`build.rs:425-448`), but those are NOT written as output — only the Rust
  files are checked-in artifacts (`ARCHITECTURE.md:146-152`).

The loop for a schema change: edit the `.schema`, run the build with the
UPDATE env var set, commit the regenerated `src/schema/*.rs`, then build
without the var to confirm freshness.

## 6. IMPORTANT honest caveat — where cloud is mid-migration

The cloud component BUILDS and the schema-driven engine is fully present, but
the DAEMON LOOP DOES NOT YET RUN IT. A faithful port must target the
schema-driven engine, not the inline `Store`. Three concrete gaps:

### (a) The Store answers requests directly inline — the Nexus runner is bypassed

`cloud/src/daemon.rs` runs the LEGACY two-listener shape, not
`triad-runtime`'s `SingleListenerDaemon`. `Daemon::run` spawns two raw
`UnixListener` threads (`daemon.rs:23-43`) and each stream handler decodes a
`signal-frame` `Frame` and calls `store.handle_ordinary_request(request)` /
`store.handle_owner_request(request)` DIRECTLY
(`daemon.rs:135-146,164-175`). `Store::handle_ordinary_request`
(`cloud/src/lib.rs:526-538`) and the whole `Store` impl (`lib.rs:449-1288`) are
a parallel hand-written engine: `handle_ordinary_operation`
(`lib.rs:554-559`), `handle_owner_operation` (`lib.rs:1034-1045`), and dozens
of private decision methods. NONE of this routes through `SchemaRuntime`,
`NexusEngine`, the `Runner`, the continuation budget, or the generated
`src/schema/*.rs`. The schema-driven path
(`cloud/src/schema_runtime.rs` + the generated Nexus/SEMA traits) is built and
compiles but is NOT instantiated by the daemon.

What this means for a port: do NOT copy the `Store`/`daemon.rs` shape. Copy the
`SchemaRuntime` shape (NexusEngine + SemaEngine on one noun) and build the
missing glue: a `DaemonRuntime` impl that decodes a wire frame into a
`NexusWork::SignalArrived`, calls `NexusEngine::execute` (which drives the
`Runner`), and encodes the `ReplyToSignal` back. The single-listener vs
two-listener split (ordinary/owner sockets) also has to be reconciled with
`triad-runtime`'s `SingleListenerDaemon` (single socket) — the runtime today
provides only a single-listener daemon, while cloud needs two authority-tiered
sockets (`skills/component-triad.md:337-368`). That reconciliation is unbuilt.

### (b) The Cloudflare call is inline, not a CommandEffect

In the schema, the external Cloudflare IO is a declared effect catalog
(`cloud/schema/nexus.schema:40-46`) and the generated `run_effect` is the
intended seam (`cloud/src/schema/nexus.rs:755`). But the REAL Cloudflare HTTP
calls live inline in `Store`: `cloudflare_zone_listing` /
`cloudflare_record_listing` / `apply_cloudflare_plan`
(`cloud/src/lib.rs:767-797,1150-1172`) call `self.cloudflare.zones(...)` /
`.records(...)` / `.apply_plan(...)` directly during request handling. The
schema-driven `SchemaRuntime::run_effect` (`schema_runtime.rs:316-328`) is a
STUB returning empty `ZoneListing`/`RecordListing` and a synthetic
`PlanApplied`, with NO real provider call. So the `CommandEffect` →
`run_effect` → `EffectResult` → `EffectCompleted` → `Continue` path is wired in
types but does no IO.

What this means for a port: the effect catalog is the correct destination —
external calls (`skills/component-triad.md:886-891`: "Cloud component starts
the Cloudflare CLI to change DNS — the external call is a nexus schema") belong
as `CommandEffect` variants whose `run_effect` arm performs the IO and returns
a typed `EffectResult`. The inline `Store` provider calls are the OLD shape to
be lifted into `run_effect`, not replicated.

### (c) The CLI also rides the legacy wire path

`cloud/src/client.rs` uses `signal_frame::signal_cli!` (`client.rs:22-27`) and
the hand-written `signal_cloud::Operation`/`Reply` surface over
`OrdinaryFrameIo`/`MetaFrameIo` (`client.rs:55-60`), not the generated
`schema::lib` Input/Output or a `triad-runtime` `ComponentCommand` flow. This
is consistent with the daemon still speaking the legacy `Frame` wire; both ends
migrate together. A port should not treat `client.rs` as the new-model CLI
reference — it is the legacy bridge that coexists during migration.

### Summary of the faithful-port target

| Aspect | Mid-migration (do NOT copy) | New-model target (the port) |
|---|---|---|
| Request engine | `Store` inline (`lib.rs:449-1288`) | `SchemaRuntime` NexusEngine+SemaEngine (`schema_runtime.rs`) |
| Daemon loop | two raw listener threads (`daemon.rs:23-43`) | `triad-runtime` daemon driving `NexusEngine::execute`/`Runner` |
| External IO | inline `self.cloudflare.*` (`lib.rs:767-797`) | `CommandEffect` → `run_effect` (`nexus.schema:40-46`) |
| CLI | `signal_cli!` legacy `Frame` (`client.rs:22-60`) | `ComponentArgument` + generated Input/Output |
| Wire types | hand-written `signal_channel!` (`signal-cloud/src/lib.rs:327-341`) | generated `schema::lib` Input/Output |

The schema files, the generated `src/schema/*.rs`, the `SchemaRuntime` engine
impls, and the `build.rs` seam are FULLY new-model and are the parts to port
faithfully. The daemon loop, the inline `Store`, the inline provider calls, and
the legacy CLI/contract wire surface are the migration tail to be replaced by
`triad-runtime`-driven equivalents.
