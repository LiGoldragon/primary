# Lojix onto its Ethos: a survey against ethos-zero 28

This maps what it takes to bring Lojix onto its Ethos as bead primary-kc4e defines it. The generator is ethos-zero 28 (970459d).

What was read:
- origin/main of lojix (da0ad8a), signal-lojix (bd5d250) and meta-signal-lojix (1b0aaeb), in detached worktrees;
- ethos-zero 970459d with its README and UPGRADES;
- orchestrate ef4fe80;
- the 2e404d and 565bc8 reports;
- the vision modules ethos, signal, nexus, nexus 1 and memory.

Nothing in Lojix was built, committed, pushed or messaged. The only thing built was the ethos-zero 28 binary, through the configured remote builder (`/nix/store/383qv46b…-all-workspace-members/bin/ethos-zero`). I ran its `Check` and `Generate` on the Lojix Ethos files, and on copies of them in scratch.

Each claim is marked **Observed** (read from source or seen in a run) or **Inference** (my reading). The full type lists, the shape-by-shape twin table, the external-call table and the ethos-zero transcripts are in `lojix-survey-appendix.md`, beside this file.

## The largest findings

1. **Observed.** The wire moves to 28 with one kind of Ethos refusal, on three marker declarations. But Check accepts files whose positional pairing is wrong. Today's output order makes `watch_deployments` answer a `ConfigurationRejection`, and makes meta `deploy` answer a `RejectedDeploy`. Both output lists have to be reordered, and that is a wire break.
2. **Observed.** The hand model is a triple copy in places. There are 146 wire twins in all: 114 in runtime_model.rs, 18 in bootstrap.rs, 11 in runtime_flow.rs (a third copy of the same wire names), and 3 more for TestDefaults and TestMode.
3. **Observed.** 84 types sit in the stored closure, and 61 of them are wire twins. 17 of those are enums whose variants the wire lists in another order. Two more carry the Horizon definition inside on one side and beside it on the other. **Inference:** a Memory that holds the contract types keeps today's bytes only if the wire takes the stored order. The wire breaks anyway for pairing, so one break can carry both.
4. **Observed.** ethos-zero 28 cannot express three things Lojix uses:
   - asynchronous capabilities: `Answering` and `Emittable::emit` are synchronous, while Lojix's effects are async over tokio and zbus;
   - raw bytes: the quarantined row's `Vec<u8>`;
   - generic declarations: `Nexus<Root>`.

   It also has no Ethos home for Memory keys, family names, schema version or upgrades.
5. **Observed.** Lojix pins nexus 0.1.1. A generated Memory record holding `nexus::ConfigurationState` needs nexus 0.5.0 (64a735d), the release that adds `Hash`.

## 1. Repositories, crates, builds and pins

| repository | origin/main | crates (version) | Ethos source | generated Rust | how it is checked | ethos-zero | build |
|---|---|---|---|---|---|---|---|
| signal-lojix | bd5d250 | signal-lojix 0.11.0 | `ethos/signal.ethos`, a Signal: 5 inputs, 11 outputs, 99 types; imports `horizon_lib::HorizonDefinition` | `src/generated/signal.rs`, 659 lines | `build.rs` asserts the committed file equals fresh generation, at every build | c2653dd (16.0.0), build-dependency | crane, through LiGoldragon/rust-build |
| meta-signal-lojix | 1b0aaeb | meta-signal-lojix 0.12.0 | `ethos/signal.ethos`, a Signal: 7 inputs, 14 outputs, 29 types; imports 28 names from signal-lojix | `src/generated/signal.rs`, 287 lines | `build.rs`, the same | c2653dd, build-dependency | crane, through rust-build |
| lojix | da0ad8a | lojix (library) 0.10.6; lojix-nexus (daemon); lojix-client (`lojix`); meta-lojix-client (`lojix-meta`); lojix-offline-tools (lojix-bootstrap, -write-configuration, -inspect-store, -reset-store, -migrate-configuration) | `ethos/ingress.ethos`, a Library: the offline tools' requests | `src/ingress.rs`, 251 lines, compiled only under the `tools` feature; lojix-nexus takes `default-features = false`, so the daemon does not compile it | `tests/ingress_freshness.rs`, a test, not the build | c2653dd, dev-dependency | crane and fenix directly in `flake.nix`. Four component builds. Checks: six cargo test checks, fmt, clippy `-D warnings`, and four NixOS VM checks |

The other pins that bear on the move are below. All of them are **Observed**.

| dependency | Lojix pins | Orchestrate on 28 pins | bearing |
|---|---|---|---|
| ethos-zero | c2653dd (16.0.0) on every edge, horizon-lib and signal included | 970459d (28.0.0), with 19.2 still in the graph through signal 7afb68b | Two revisions coexist in Orchestrate's graph, so Lojix can move edge by edge |
| signal (frames) | f35460de, 8.0.0 | 7afb68b, 10.3.0 | 8.0.0 has no contract greeting, so a mismatched client fails to decode and gets no named refusal |
| nexus | a84bfa96, 0.1.1 | 64a735d, 0.5.0 | 64a735d derives `Hash` on ConfigurationState, Situation and Relocation |
| memory-engine | 27f256c, 0.19.0 (memory 0.2.0, redb 4.1.0) | ef24197, 0.20.0 | 0.20 converts a sema file found at the memory path, on open |
| horizon-lib | e723ce1, 0.17.1 | — | Generated by ethos-zero 16 from `lib/ethos/horizon.ethos`, a Signal with no inputs or outputs; it Checks under 28 |
| triad-runtime | 4cc0a10 (0.10.1); 02cdd49 (0.8.1) in lojix-nexus's dev-dependencies | — | The runner Lojix's decision engine plugs into |
| datom-codec and protos | 4dff16b and 15b41da (both 0.32.2) | eabead4 and 3c7ade3 (0.33.0) | — |

**Memory today (Observed).** The engine is memory-engine; there is no sema crate in the lock.
- **File and format.** The store is one file, `lojix.memory`, in the state directory. It is schema version 5 (`LOJIX_SCHEMA_VERSION`), with rkyv 0.8 rows, one row per element.
- **Families.** There are 12, each with a hand-written table name, family name, schema hash (`[n; 32]`, n from 1 to 13, 10 not used) and record key:

| table | record | key |
|---|---|---|
| live-set | LiveGeneration | generation id |
| gc-roots | GcRoot | generation id |
| event-log | EventLogEntry | event-log position |
| container-lifecycle | ContainerLifecycleRecord | event-log position |
| deploy-job | DeployJob (in-flight deploys only) | deployment id |
| test-run | StoredTestRun | test-run id |
| deployment-record | DeploymentRecord | deployment id |
| identifier-allocation | IdentifierAllocation | `global` |
| deployment-outbox | DeploymentOutboxRecord | deployment id and transition marker |
| pending-transition-intent | PendingTransitionIntent | deployment id and transition ordinal |
| nexus-configuration | NexusConfigurationRecord, holding `nexus::ConfigurationState<LojixNexusConfiguration>` | `desired` |
| quarantined-row | QuarantinedRow | table, key, number |

- **Legacy conversion.** A sema-era `lojix.sema` is converted on a copy at startup (`legacy_store.rs`), and the sema file is kept as the rollback.
- **Quarantine.** A row that no longer decodes is moved into `quarantined-row` with its bytes and its error. ARCHITECTURE names the cause: a deploy job or configuration archived with an earlier HorizonDefinition layout. A quarantined configuration row is rebuilt from the built-in defaults.
- **Other stored formats.** Beside the store:
  - the legacy rkyv startup archive named by `LOJIX_CONFIGURATION`, which the reset and migrate tools read;
  - the bootstrap journal: its own private `lojix-v5.memory` and `bootstrap-v5.rkyv`.
- **Fixtures.** `tests/fixtures` holds three 180 KiB redb files: a sema 8.1.0 store, a v5 store from before the configuration family, and a v5 store holding one deploy job with a Horizon 0.12 definition.

**Running (Observed).** The audit of 2026-11-13 found lojix.service 0.10.6 on ouranos (321682e). CriomOS main's flake.lock pins lojix da0ad8a.

## 2. The hand-written types

**Method (Observed).**
- I listed every type declaration and newtype macro outside the `#[cfg(test)]` modules: 385 data types and 160 traits.
- Names were matched against what ethos-zero 28 generates from the three Ethos files.
- Shapes were compared field by field and variant by variant.

**Counts by category (Observed).**

| category | data types | where | notable |
|---|---|---|---|
| wire twin | 146 | runtime_model 114, bootstrap 18 (ingress), runtime_flow 11, lib.rs 2, schema_runtime 1 | DeploymentRecord, DeploymentPhase, HostDeployment, Selection, TestRun, PinRequest, every scalar newtype, the four markers |
| store record that is not a twin | 37 | runtime_model 23, bootstrap journal 10, lib.rs 2, quarantine.rs 2 | DeployJob, LiveGeneration, GcRoot, EventLogEntry, PendingTransitionIntent, DeploymentOutboxRecord, IdentifierAllocation, NexusConfigurationRecord, LegacyStartupConfiguration, QuarantinedRow |
| operation and decision state | 44 | runtime_model 14, schema_runtime 14, runtime_flow 8, daemon.rs 8 | MemoryWriteInput (11 writes) and MemoryWriteOutput (14), MemoryReadInput (3) and MemoryReadOutput (4), Ordinary/Meta Ingress and Egress, NexusWork, NexusAction, DeployPipeline, the kameo messages |
| emission (external calls) | 77 | schema_runtime 38, runtime_flow 33, bootstrap 6 | EffectCommand (10 commands), EffectResult (12 results), NixCommand, HostActivation, the DetachedActivation family, ShellCommand |
| other | 68 | inspection, reconstruction, inspected_text, clients, tools, daemon shell, Error, Store, bootstrap's 13 `*Validated` types | — |
| unused | 13 | runtime_model 11, runtime_flow 2 | the nine `*Table` newtypes, and both files' `Input` and `Output` |

**How the 114 runtime_model twins agree with the generated shapes (Observed; bytes are Inference from rkyv's layout rules).**

| agreement | count | effect on stored bytes |
|---|---|---|
| Same shape at its own level. The integer newtypes differ as `u64` against `i64` | 45 | none, for values below 2^63 |
| Same variants, different order | 25 | the tag changes |
| Field names differ only (`from`/`until`, `node`/`host`, `url`/`public_key`, `optional_x` against `x_option`) | 13 | none |
| Hand newtype against generated one-field struct (GenerationLookup, RejectedWatch, SubscriptionClosed, the markers) | 11 | none |
| Marker or flag wrapping and field names differ (`state_marker: StateMarker` against `database_marker: DatabaseMarker`, `bool` against `DetailTruncated`) | 16 | none at this level |
| Structurally different | 4 | see below |

The four that differ in structure (**Observed**):
- **HostDeployment and UserEnvironmentDeployment.** The hand types carry `horizon_definition_option` inside, as their ninth field. The wire carries it beside, in `ActualizedDeploySubmission`, and `adapters.rs` merges it in.
- **Generation.** On the wire the closure path is optional. The raise turns a non-canonical store path into `None`.
- **NodeSelector.** It holds GenerationArtifact; the wire holds RequestedGenerationArtifact, a second enum with the same three variants in another order.

**The stored closure.**
- **Observed.** 84 types are reachable from the ten runtime_model families. 23 are Lojix's own and 61 are wire twins.
- **Observed.** 17 of the twins are enums in another order on the wire, among them DeploymentPhase, DeploymentLifecycle, GenerationSlot, ActivationEffect, DeploymentTerminal and DeploySubmission. Two more are HostDeployment and UserEnvironmentDeployment.
- **Inference.** Storing the generated types as the wire now orders them changes the bytes of almost every family. Reordering the wire to the stored order changes no stored byte.

**Duplication inside the hand model (Observed).**
- **The wire names, three times.** The 11 wire names that runtime_flow.rs declares exist three times: on the wire, in runtime_model and in runtime_flow.
- **TestDefaults, four times:**
  - signal-lojix;
  - lib.rs's legacy startup archive;
  - schema_runtime's runtime projection;
  - ingress's WriterTestDefaults.
- **Test runs.** StoredTestRun has exactly the fields of the hand TestRunRecord.
- **Deploys.** DeployPipeline (the in-memory cursor) largely repeats DeployJob (its persisted mirror).
- **Phases, five times.** DeploymentPhase and DeploymentLifecycle have the same nine variants, on the wire as well. Beside them are DeployJobPhase, DeployStage and DeployResumeStage.
- **Bootstrap.** bootstrap.rs repeats the ingress request twice: as 18 twins, then as 13 `*Validated` types.

**Emissions today (Observed).** Every daemon call goes through one struct, `NixCommand`, and its async `Effect::run` over `tokio::process`:
- about a dozen `nix` invocations: flake metadata, eval, hash, build (local, offloaded, check), copy, path-info, and a build in the target store;
- `ssh` carrying shell text for `switch-to-configuration`, `systemd-run`, `bootctl` and `journalctl`;
- `nix-env --set` and `systemd-run --user`;
- `hostname -s`.

The detached same-host activation talks to systemd over D-Bus with zbus: GetUnit, StopUnit, the UnitNew signal, and changes to ActiveState. Horizon materialization writes generated flake inputs and copies `.sops` secrets under the state directory. lojix-bootstrap uses synchronous `std::process` and waits on unit state with a 100 ms sleep loop (bootstrap.rs lines 658 and 2886). Failure evidence is bounded to 4096 bytes and persisted into the DeploymentRecord. The full table is appendix F.

## 3. What schema_runtime.rs and lib.rs hold

**schema_runtime.rs (Observed).** It runs to 11,173 lines: 8,567 of production and 2,606 of tests, 96 test functions. It is the daemon's decision engine and its effect executor in one file. `SchemaRuntime` is a per-request engine over a shared `Arc<Store>`, holding the in-flight state `DeployPipeline`, `TestPipeline` and `MetaOperation`.
- **Deciding.** `SignalDeciding` decides each arriving input into a `NexusAction`: read memory, write memory, run an effect, reply, or continue.
- **Memory.** `MemoryApplying` and `MemoryObserving` carry the writes and reads out against the Store, answering typed receipts or rejections.
- **Pipelines.** `DeployDriving` and `TestDriving` are the async pipelines. A deploy runs flake auth, Horizon materialization, eval, build, copy and activate, recording a phase transition between stages. It resumes from the DeployJob row after a restart (`DeployJobResuming`).
- **Effects.** `EffectRunning` and the `Effect` trait run the external calls listed in section 2. The file also holds the materialization of generated flake inputs and secrets, the SSH routing and shell quoting, host and user-environment activation, the detached-activation observer, and test VMs.

The engine speaks only the hand model. Its private `ordinary` and `meta` modules re-export runtime_model under the wire's names, and a comment at lines 393–395 says "no wire type crosses this module boundary". The exception is the configuration: the wire's LojixNexusConfiguration, through lib.rs's alias, and its TestDefaults, converted at line 1351. It declares 54 data types, 38 of them effect shapes, and 60 traits.

**lib.rs (Observed).** It runs to 4,098 lines: 3,375 of production and 722 of tests. It is the crate root and the durable store.
- **The store.** It declares `Store` over memory-engine and `LojixRecord`, with the twelve family identities and their `EngineRecord` keys (section 1). It also declares the store's capability traits, each implemented on Store:
  - DurableStore and StoreIntegrity: open, the write gate, decode-all on open, compaction resume;
  - NexusPersistable: the configuration metadata tree;
  - IdentifierAllocating: the durable high-water row;
  - TransitionJournal: exactly-once phase delivery through intent and outbox rows bound to their commit;
  - EventHistory: the bounded event log and its retention;
  - DeploymentLedger, GenerationLedger and TestRunLedger.
- **The rest.** It also holds:
  - the crate's `Error` (about thirty variants);
  - the configuration: `NexusConfiguration`, an alias of the wire's LojixNexusConfiguration, with built-in defaults, store-path discovery, and the legacy rkyv startup archive with its migration into the store;
  - the `Payload` trait that every hand newtype implements;
  - the module list.

It persists runtime_model types and translates nothing to or from the wire.

## 4. Moving signal-lojix and meta-signal-lojix from ethos-zero 16 to 28

**Check with the 28 binary (Observed).**
- signal-lojix is refused: `Rejected.{ … { 68 19 } Conceptual.{ [ 1 3 44 1 ] Wrapping.{ AdmissionMarker DatabaseMarker } } }`. AdmissionMarker, TransitionMarker and TerminalMarker are each written `X.DatabaseMarker`, a head over a struct, which 19.3.0 refuses. With the three written `X.{ DatabaseMarker }` in a scratch copy, the file Checks and generates.
- meta-signal-lojix Checks as it is. So do lojix's `ingress.ethos` and horizon-lib's `horizon.ethos`.

**What regeneration changes in the Rust (Observed, by diffing 16's output against 28's).**
- The aliases become newtypes. In signal-lojix 33 scalar aliases become `pub struct X(pub T)`, and the three marker aliases become one-field structs. In meta, `QuickCheck` becomes a newtype. In ingress, 21 aliases become newtypes.
- `Query` and `Response` become `Input` and `Output`.
- Each contract gains `Answering` (5 and 7 capabilities) and `impl Answerable for Input`.
- Nothing else changes: every field name, enum and variant order is as before.
- **Inference.** The regeneration alone leaves the rkyv bytes unchanged.

**What breaks in meaning (Observed).** Check passes, but positional pairing makes today's orders answer wrongly:
- signal-lojix: `watch_deployments` yields a ConfigurationRejection, `query` a TestRunListing, `unwatch` a RejectedQuery;
- meta-signal-lojix: `reverse_configuration` yields a ConfigurationRejection, `deploy` a RejectedDeploy, `test` a RefusedDeploy.

Both output lists must be reordered so that the n-th output answers the n-th input, with refusals and reactions after. That moves the archived tag of most outputs.

Two inputs do not pair one to one:
- `Query.Selection` is answered by three different outputs: Queried, DeploymentEventsQueried and TestRunsQueried, by selection.
- `WatchDeployments` and `WatchCacheRetention` share `Watching`.

A scratch candidate with reordered outputs and a second watch output Checks for both contracts (appendix G). Meta pairs cleanly: Configured, ConfigurationReversed, Retired, Pinned, DeployAccepted, Tested, Unpinned; then the seven rejections and the reaction DeployTerminal.

**What the consumers then change (Observed for where, Inference for how much).**

| consumer | change |
|---|---|
| signal-lojix, meta-signal-lojix | Repin the build-dependency to 970459d. Fix the three markers. Reorder outputs (and take the section 6 rulings). Rename `Query` and `Response` in `tests/generated_contract.rs`. Write UPGRADES entries. |
| lojix daemon | Rename `Query` and `Response` to `Input` and `Output` in daemon.rs: its three framing traits and its ordinary request decode. |
| lojix adapters | Rewrite adapters.rs throughout. Its `text_value!` and `integer_value!` macros implement `Lowerable` from bare `String` and `i64`, which are newtypes now. The marker wrappers change too. In all, `Query` and `Response` appear on 135 lines across 8 files, the clients and tests included. |
| lojix configuration | Use newtype constructors wherever wire values are built from raw ones: lib.rs's configuration defaults and legacy conversion, schema_runtime's TestDefaults, the meta client's ClientQuery actualization, the configuration writer. |
| lojix ingress | Regenerate. bootstrap.rs's `From` conversions and the configuration writer take newtypes and positional names (`first_writer_path` to `fifth_writer_path`). |
| CriomOS | Bump the flake pin. Its text is untouched if the output names stay: `harness-update.nix` sends `Deploy.UserEnvironment.{ … }` and greps `DeployAccepted.{ N`, and the `lojix-nexus-start` check sends `Query.ByNode.{ … }`. |
| lojix-test | Behavioral replay against lojix by flake URL; it changes where reply text changes. |

The hand model insulates the store from the wire today, so this step alone does not touch the Memory (**Inference**).

**A divergence from the vision (Observed).** The vision says an enum of one variant is refused. 28 accepts ingress's five: InspectionRequest, ResetStoreRequest, BootstrapRequest, BootstrapStrictHostKeyMode and ConfigurationWriterInput.

## 5. Where ethos-zero 28 cannot express what Lojix needs

1. **Asynchronous capabilities (Observed).**
   - **Answering is synchronous.** `Answering` capabilities are synchronous `fn`, and so is the generated dispatch. Lojix's `submit_test` is `async fn`. The deploy pipeline and test pipeline await child processes and D-Bus inside kameo actors.
   - **Emittable is synchronous.** `Emittable::emit` is a synchronous `fn emit(&self, translator) -> Outcome`. Every one of Lojix's effects is `async fn run(&self, &EffectExecution) -> Result<Product, StageFailure>` over tokio::process and zbus. Some run for many minutes: builds, copies, activations.
2. **Raw bytes (Observed).** `QuarantinedRow.archive` is `Vec<u8>`, the original row bytes. The intrinsics have no byte type, and `Vector<Integer>` generates `Vec<i64>`, a different archive.
3. **Generic declarations (Observed).**
   - `Routed<Root>.{ Integer Root }` is refused as `Expected.Declaration`.
   - runtime_flow's `Nexus<Root>`, the route-tagged work and action, cannot be declared.
   - Generic types are usable only when imported, as `nexus::ConfigurationState<…>` is.
4. **Memory identity and upgrades (Observed).** The Memory root declares record types only. None of the following has an Ethos section:
   - the twelve table names, family names and schema hashes;
   - the record-key derivations;
   - schema version 5;
   - an upgrade from a previous format.

   The vision says a memory trait carries each version's upgrade and leaves the remaining sections to be decided. Orchestrate kept the same pieces hand-written; its question 4 is the same question.
5. **One input, several success answers (Observed).** Positional pairing gives an input one success payload; any other output can only come back through the refusal channel (`Err(Output)`). `Query` has three success answers today, and the two watches share one. This can be expressed only by reshaping the contract (section 6, question 2).
6. **Subscriptions (Inference from the generated dispatch).** `WatchDeployments` answers `Watching` and then streams `DeploymentPhaseObserved` frames on the same connection. A reaction can be declared as an output past the last input. Nothing generated ties a reaction to the subscription that asked for it, so the stream stays outside the dispatch.
7. **Operation has no behavior (Observed).** An `Operation` file generates its types and two enums, and no trait, dispatch or pairing. Lojix's decide, act and continue runner (NexusWork, NexusAction) can be declared as data; its driving stays hand-written. The README also says Operation's sections are "proposed, not yet the living's word".
8. **Runtime holders that are not data (Inference).** SchemaRuntime, Store, RuntimeConfiguration and EffectExecution (both holding `PathBuf`), the zbus proxies and the kameo actors hold things that do not archive. Every generated type derives rkyv, Eq and Hash, so these cannot be Ethos types. They are not Signal, Operation, Memory or Emission data either.

These are expressible and are only work:
- **Integer signedness.** `Integer` is `i64`, and Lojix's identifiers are `u64` with checked conversion today.
- **Copy.** Generated types derive no `Copy`, which Lojix's unit enums have.
- **Position names.** Names such as `from` and `until` need a head in place, which declares a newtype.
- **The orphan rule.** `EngineRecord` cannot be implemented on a signal-lojix type inside lojix, so a stored contract type is wrapped in a Memory record.

## 6. Open design questions, each with my reading

1. **Where a stored twin and the wire disagree, which side yields?** At issue are the 17 reordered enums, HostDeployment and UserEnvironmentDeployment (Horizon definition inside or beside), Generation's optional closure path, and RequestedGenerationArtifact against GenerationArtifact.
   - *Reading:* give the wire the stored order. The stored order is the lifecycle order, which reads as the vision's seniority; the wire's present order looks arbitrary (DeploymentPhase begins `Built Completed Failed Copying`). The wire breaks for pairing anyway, so the Memory keeps its bytes and needs no upgrade.
   - The deploy-job record holds the contract's `ActualizedDeploySubmission` whole. Its upgrade is written and proved on the deploy-job fixture; the family holds in-flight deploys only.
   - Generation keeps the optional path, its filter staying body code. RequestedGenerationArtifact folds into GenerationArtifact.
2. **How do `Query`'s three answers and the shared `Watching` pair?**
   - *Reading:* the vision's "variations of a feature stand at the root" points the way. `Query.Selection` keeps ByNode, ByGeneration and ByDeployment, answered `Queried`. Two inputs of their own take the rest: `QueryDeploymentEvents.EventLogRange` and `QueryTestRuns.TestRunLookup`.
   - Each watch gets its own output. The CriomOS check's `Query.ByNode.{ … }` text is unchanged.
3. **What becomes of `WatchCacheRetention`?** It is observed to issue a token and register no watcher, and no output ever streams a cache-retention event.
   - *Reading:* remove it, unless a cache-retention reaction is wanted.
4. **Does Lojix keep its runner, or answer through the generated dispatch?** Today a pure `decide` returns a `NexusAction`, and triad-runtime drives memory steps and effect continuations.
   - *Reading:* answer through `input.answer(&answerer)`. The answerer does the memory step directly (the redb-backed Store is synchronous) and hands deploy and test jobs to their actors after the admission write, as today.
   - NexusWork, NexusAction, OrdinaryIngress, MetaIngress and the triad-runtime dependency then retire.
5. **How do async effects meet a synchronous `emit`?** There are three ways:
   - (a) a synchronous `emit` run on a blocking thread, with std::process and zbus's blocking API;
   - (b) ethos-zero generating an async `emit`;
   - (c) a translator process carrying the Emission, as vision nexus/1 draws it.
   - *Reading:* (a) now, as the smallest step and Curriculum's shape; (c) is the horizon.
6. **What are Lojix's operations?** Its memory-level operations are 11 writes and 3 reads, each with a typed outcome. The vision's operations are per-input attempts.
   - *Reading:* the 11 writes and 3 reads become the Operation's operations and outcomes, which is what the running code does. Per-input attempts wait for the Operation root's sections to be the living's word.
7. **Does quarantine stay?** The vision rules that the old store is upgraded on open and never accommodated; Lojix quarantines rows it cannot read, and the quarantined row needs a byte type Ethos lacks.
   - *Reading:* retire quarantine once each format change carries its upgrade. The existing `quarantined-row` family is emptied by an upgrade that reports what it drops, or kept as a frozen legacy table only the inspector reads.
8. **Does "the running binary" include the offline tools?** lojix-bootstrap carries 18 ingress twins, 13 `*Validated` types, a journal Memory of 10 rkyv types and synchronous process calls. CriomOS exposes it as a package and an app.
   - *Reading:* yes, after the daemon and its clients, as their own steps.
9. **Is horizon-lib in scope?** Its HorizonDefinition is in the Signal and in the Memory, and is generated by ethos-zero 16.
   - *Reading:* yes, as its own step. Its 37 aliases becoming newtypes leaves the bytes unchanged (Inference), so Lojix's Memory needs no upgrade for that step.
   - Still open: may Lojix's Memory hold a foreign contract type whose layout another repository can change? That is the cause quarantine exists for.
10. **What becomes of the legacy startup archive?** That is LegacyStartupConfiguration, with its TestDefaults and TestMode twins, still read by the reset and migrate tools and written by the configuration writer.
    - *Reading:* retire it with the tools step. The vision has a Memory that exists hold the configuration.
11. **Are DeploymentPhase and DeploymentLifecycle one type?** They have the same nine variants on the wire.
    - *Reading:* one type, merged in the same contract change as question 1.
12. **What are acknowledgement outputs called?** `DeployAccepted` and `Tested` answer at admission, before the work is done; `Watching` is not a past tense.
    - *Reading:* keep `DeployAccepted`, since the vision allows an acknowledgement as the answer, and "Deployed" would be false at that moment. Rename the watch outputs with question 2.

### Settled by precedent

- ethos-zero 28 for every Lojix Ethos file. Committed generated Rust is checked by `build.rs` at every build and fails as "X is stale" (Orchestrate, Curriculum).
- Outputs pair by position, with refusals and reactions after. Both ends repin together, and the moved tags are accepted (Orchestrate).
- Each input has its own output, named in the past tense (Orchestrate's `Configured`).
- A store failure is answered within each contract as `Refused.Store`, after every other output. A fault in the request is a named rejection (Orchestrate rulings 3 and the final fix).
- The Nexus answers with `input.answer(&answerer)`, a per-call bearer over the store (Orchestrate, Energy).
- Memory records are generated from `memory.ethos`. Keys, table and family names, schema hashes and `EngineRecord` impls stay hand-written beside them (Orchestrate).
- A contract type kept in Memory is held whole inside a record of its own, `StoredLock.{ Lock }` (Orchestrate).
- A generated record archives to the bytes of the record it replaces. This is proved both ways by representation tests, fixtures and live-store copies; equal bytes need no upgrade; frozen old layouts and their upgrades stay hand-written (Orchestrate, Energy).
- A position is named by a head in place, which declares a newtype and leaves the bytes unchanged (ruling 7).
- Every generated type derives `Hash`, and a foreign stored kind gains it (nexus 64a735d).
- `Integer` is `i64`, and an allocator refuses at `i64::MAX` (Orchestrate).
- An external call is an Emission: the consumer implements `Emittable<Translator>` for each emission type, and nothing dispatches over the Emission enum (Curriculum ruling 1).
- `operation.ethos` follows the running code and is used as the operation enum, with the daemon's own behavior trait hand-written (Energy).
- A file format that is not on the wire stays out of the wire contract, so ingress and the bootstrap journal stay in Lojix's own Ethos (Curriculum ruling 3).
- Builds stay on crane, with no build-base edge (Orchestrate).
- A contract changes once per release, with an UPGRADES entry (Orchestrate).
- Work is built on branches, gated with `nix-fast-build --remote prometheus`, and nothing is switched before release (Orchestrate, the bead).

## 7. Proposed order of steps

Each step is a branch, gated by every repository's flake checks on the builder, and proved as listed. Smallest first.

| step | change | proof |
|---|---|---|
| 0 | Fable rules on questions 1–12. | — |
| 1 | Delete the 13 unused types (lojix). | Gate only. |
| 2 | ingress on 28 in lojix: regenerate, move the freshness check into a `build.rs`, adapt bootstrap.rs and the configuration writer to newtypes. | Tools tests; each tool's Datom text unchanged. |
| 3 | horizon-lib on 28 (if question 9 says so). | Horizon fixtures. lojix's three store fixtures open unchanged on a lojix pinned to it. |
| 4 | signal-lojix and meta-signal-lojix on 28, one wire break: markers, positional pairing, the question 1, 2, 3, 11 and 12 rulings, `Refused.Store`. | Contract round-trip and Datom tests. A table of moved tags. |
| 5 | lojix repins both contracts and nexus 0.5.0, mechanically: `Input` and `Output`, newtype constructors, adapters kept. | A/B transcripts, the same inputs against the live 0.10.6 and the branch over a store copy. Crossed versions refused. Store untouched. |
| 6 | The leaf twins go: runtime_model's scalar and marker newtypes and agreeing leaves become the generated types, and adapters lose their macros. | Representation tests per family against frozen 0.10.6 records; the three fixtures. |
| 7 | `memory.ethos`: the 23 own record types, NexusConfigurationRecord, and wrappers for stored contract types. LojixRecord stays hand-written. Quarantine and the deploy-job upgrade per questions 1 and 7. | Both-ways bytes (the Energy pattern); fixtures; live copies from ouranos; rollback of 0.10.6 onto the store the branch served. |
| 8 | Answering: the daemon answers through the generated dispatch. OrdinaryIngress and Egress, MetaIngress and Egress, adapters.rs and the remaining runtime_model twins are deleted. | A/B transcripts. The deploy-honesty, watch and failure-evidence tests. |
| 9 | `operation.ethos`: the memory reads and writes and their outcomes; the runner per question 4. | Engine-routing and durable-resume tests. |
| 10 | `emission.ethos`: typed emissions in place of NixCommand's kinds and EffectCommand and EffectResult. runtime_flow's 11 twins are deleted. `emit` per question 5. | Fake-program focused tests; the four NixOS VM checks (retained transient semantics, collected transient journal, target-store realization, same-host test activation). |
| 11 | The offline tools: bootstrap twins and `*Validated`, the journal Memory, the legacy archive (questions 8 and 10). | Bootstrap tests. |
| 12 | Rerun the audit, then release: CriomOS pin, then the `harness-update` text check. | The audit verdict. |
