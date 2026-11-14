# 052 admission and configuration: proposed authored Rust contracts

## Latest task-authority correction

Current 052 scope is version zero: typed startup/configuration policy, optional existing Continuity and configured default, Resume.FlowId preserving existing identity/transcript, and idle harness retention. Ordinary caller identification stays unchanged. Launch/Refresh retain their existing payload shapes. There is no new gate, Living payload, StartedBy or Continues field. Exact916 Refusal already lacks FableNeedsTheLiving/NeedsTheLiving, so no gate-discriminant removal or provenance migration is required. Actual configuration/Continuity/Resume compatibility is a separate row-level check. Backend changes remain subject to the approved admission/configuration requirements and final body gate.

Task-authority provenance, the living's exact words relayed by Mind core Secondary: “No you do not have special authority. The main Fable flow does not have any special authority so there is nothing there. You are pursuing nothing. You are still trying to pursue a type of security that we are not even close to tackling yet.” The subsequent Psyche ruling removed gate and provenance work entirely. These quotations record supersession; they add no implementation requirement.

For final design judgment, not body authorization. Bases: Flow 916b54574ae0024b893a9f4252f2e97704db48c1, Engine 9884905ff9c660ad97a35c524e42532d5c7bac90, Sema 51d7927c872f0df12791bad8d39a4db6433b01a1, redb 4.3.0. Names below are proposed in-process types, not claims of existing declarations or allocated schemas.

## 1. An existing file is inspected and promoted as one owner

Ownership graph: Flow owns EngineInspection; it owns SemaInspection; it owns redb Inspection; it owns one File/backend and continuous exclusive lock. The private owner association is this containment, not a filesystem object. Identity is fstat on that File. Path is diagnostic. No independently supplied proof, clone, serialization, detached receipt, or backend/token pairing API exists.

Authored Rust signatures (native dependency errors remain typed; new errors are listed below):

```rust
pub struct Device(pub u64);
pub struct Inode(pub u64);
pub struct FileIdentity { pub device: Device, pub inode: Inode }

// redb: private fields retain backend, exclusive lock and inspected read state.
pub struct Inspection { /* private */ }
pub trait ExistingFileInspecting {
    fn inspect_file(&self, file: std::fs::File)
        -> Result<Inspection, InspectionError>;
}
// Implemented by existing Builder, with configured limits, not a new opener namespace.
pub trait InspectedReading {
    fn identity(&self) -> &FileIdentity;
    fn with_read<T, E, F>(&self, read: F) -> Result<T, ReadFailure<E>>
    where F: for<'view> FnOnce(ScopedRead<'view>) -> Result<T, E>;
}
pub trait InspectedPromoting {
    fn promote(self) -> Result<Database, PromotionError>;
}
pub enum ReadFailure<E> {
    Begin(redb::TransactionError),
    Read(E),
}
// ScopedRead has private borrowed transaction fields and returns owned decoded
// values only; no native transaction/table/iterator/backend accessor.
// Both implemented only by Inspection. promote consumes its retained backend.
```

Inspecting takes an existing opened file, acquires exclusive ownership, checks identity and reads without begin_writable, repair, initialization or Sema writes. Empty existing files, recovery-required files and ambiguous/unsupported formats refuse. No drop/reacquire lock or pathname reopen in promotion. A failed promotion may have performed the explicitly traced first writer-open mutation; it is not reported as pre-mutation refusal.

InspectionError distinguishes native I/O/locking, EmptyExisting, RecoveryRequired and unsupported/ambiguous format evidence. PromotionError distinguishes pre-writable failure from WriterOpening failure; the latter makes no unchanged-byte claim. Native error payload types must be retained from the pinned implementation, not flattened to String.

The higher-ranked closure keeps ScopedRead borrowed within inspection; returned T cannot borrow the view. The wrapper exposes no owned native table/iterator that could detach a read transaction. Native table/storage/decode errors are retained in the closure-chosen E, separately from begin-read failure. Only lower storage layers see this scoped read interface. Flow sees AdmissionObserving's owned finite result, never the transaction or raw reserved-table access. A finite observation is data, not a transferable admission proof. The owning object's private validated state alone permits promotion, with its exclusive lock continuously retained. Final signatures must additionally prevent any dependency API from cloning/detaching the transaction.

Sema adds an owned SemaInspection over redb Inspection. Its only promotion consumes itself; it supplies schema observation without ensuring/writing schema. EngineInspection owns SemaInspection and exposes a finite observation, not raw table access:

```rust
pub struct AdmissionMetadata {
    pub schema: Option<u64>,
    pub layout: Option<u64>,
    pub catalog: Vec<TableRegistration>,
}
pub struct AdmissionObservation<R> {
    pub metadata: AdmissionMetadata,
    pub identity_record: Option<R>,
}
pub trait AdmissionObserving {
    type IdentityRecord: EngineRecord + EngineStoredValue;
    fn identity(&self) -> &FileIdentity;
    fn observe(&self)
        -> Result<AdmissionObservation<Self::IdentityRecord>, AdmissionError>;
}
pub struct IdentityLocator<R> {
    pub descriptor: TableDescriptor<R>,
    pub key: RecordKey,
}
```

Pinned signature check: stored schema and layout observations are Option<u64>; malformed decoding returns typed AdmissionError rather than a fabricated value. Declared Sema schema remains sema::SchemaVersion(u32). IdentityLocator combines existing TableDescriptor<R> and RecordKey, without a new IdentityRecord trait. EngineInspection binds exactly one locator at construction; observe returns all four areas from one read view. Flow uses TableDescriptor<FlowStoreState> with table flow_nexus_state, family flow-nexus-state, schema flow-nexus-state-v2, RecordKey::Domain(identity); these are its authored record declaration, not raw Engine reserved-table vocabulary. R uses existing EngineRecord+EngineStoredValue bounds; retained plan values add Send+Sync+'static and pinned archived deserialize/check bounds. Full bound spellings are witnessed in /tmp/d05351-signature-pointers.md and reused, not redesigned.

Flow validates exact allowed current/predecessor/retired catalog completeness and next_flow_number > 0 from this one retained read view. Engine validates its format and family constraints. The owning inspection is the sole constructor of a prepared opening; refusal leaves its file unpromoted.

New-store creation is a separate capability, authorized explicitly for a nonexistent target and using create_new; it never treats an existing empty/unrecognized file as a new store. Its required configuration and schema declarations validate before creation. New-store initialization writes are stated as creation effects, not existing-file admission.

## 2. One prepared opening includes conversions and startup rows

Extend the existing Engine upgrade preparation/materialization and AtomicCommit implementation, rather than adding another batch engine. Existing current-row AtomicCommit stays its source of typed writes. Preparation gains selected upgrade/catalog operations, all evaluated against the retained view. A private implementation plan carries final current rows, conversions, catalog/log/counter updates; all share one owning database and read view.

```rust
pub struct OpeningPlan { /* typed declarations, selected upgrade edges,
                            existing AtomicCommit row operations; private */ }
pub struct PreparedOpening { /* owns EngineInspection and its prepared plan */ }
pub trait OpeningPreparing {
    fn prepare(self, plan: OpeningPlan)
        -> Result<PreparedOpening, OpeningRefusal>;
}
pub trait OpeningCommitting {
    fn commit(self) -> Result<Opened, OpeningFailure>;
}
pub struct Opened { pub engine: Engine, pub outcome: CommitOutcome }
```

EngineInspection implements OpeningPreparing; PreparedOpening implements OpeningCommitting. The plan contains requested operations, not an externally supplied validation token. prepare reads/decodes every selected predecessor with exact frozen mirrors, converts, resolves startup changes against the converted snapshot, validates full configuration and all resulting writes, and refuses duplicate final coordinates or incompatible edges. It owns the inspected view until preparation ends. commit consumes the same backend, performs writer promotion, then ONE Sema transaction materializes selected conversions, catalog, final startup rows, logs and counters. Neither persist_open nor upgrade_table may commit early on this path. No runtime listener/worker starts before successful commit.

OpeningPlan is built by the owning EngineInspection, not by Engine::begin_atomic_commit on a temporary Engine. Its typed row builders reuse AtomicCommit's preparation/materialization internals, but bind to the inspection owner and view. No public constructor takes a plan prepared for a different database; prepared operations cannot be detached and paired with another owner. This is the explicit additive opening-owned builder boundary, not a claim that current AtomicCommit can already be constructed before Engine open.

Conversion and startup override of one logical setting is composed into ONE final row during preparation, not two writes to the same coordinate. Two independent writes to a final coordinate refuse. Catalog and counter ownership are Engine's; Flow cannot supply conflicting raw writes to those tables.

The configuration resolution callback/interface is private to the store-owned capability and typed. Exact implementation may use the existing prepared-write trait machinery; it must not expose a general user callback that writes while validation is running. This plan requires an Engine change: current APIs cannot satisfy the transaction boundary.

Logical rollback after a failed final transaction does not imply unchanged file bytes: promotion may have set recovery_required. Pre-promotion refusal, writer-opening failure, transaction failure and committed result remain distinct outcomes. Fault tests identify exact first mutation.

## 3. The live writer owns the whole resolve interval

```rust
struct ConfigurationWriter { gate: std::sync::Mutex<()> }
trait ConfigurationWriting {
    fn configure_batch(&self, changes: &[ConfigurationChange])
        -> Result<ConfigurationBatchOutcome, ConfigurationFailure>;
}
```

Store ownership combines this private capability with its one Engine; the gate is held across snapshot, resolve, full validation, typed plan creation and existing AtomicCommit commit. Helpers require its borrowed private mutation context and cannot independently acquire or bypass it. Startup and config-only initialization use the same preparation/validation machinery with exclusive opening ownership; live meta passes one change. Internal setup and legacy policy configuration route through it. Legacy live placement writes refuse the named setting. Any remaining Engine configuration-table writer is a blocker, not an assumed exception. Redb exclusive ownership excludes a second process writer.

Ordinary readers keep the existing marker-consistent all-family snapshot. Publish runtime policy only after committed result; preserve existing accepted operation snapshots/deadlines and seats.

```rust
pub struct CommitOutcome {
    pub receipt: AtomicCommitReceipt,
    pub maintenance: MaintenanceOutcome,
}
pub enum MaintenanceOutcome {
    Complete,
    Failed(sema_engine::Error),
}
```

Result::Err denotes failure before successful requested transaction commit; a maintenance failure after commit stays inside Ok(CommitOutcome). Exact pinned maintenance error is sema_engine::Error, with no narrower existing type; it is retained, not stringified or renamed as a fictitious native error. This changes generic Engine outcome consumers together. Exact Flow916 has versioning disabled, so its maintenance-failure branch is unreachable; generic versioned-Engine fault tests are separate evidence, not fabricated Flow coverage.

## 4. Gates and acceptance evidence

- Flow independent candidate/lock25605 exists. Independent redb/Sema/Engine repositories, locks, baseline and namespace/version allocations must be witnessed before their edits. No abandoned roots or patches.
- Approve concrete record bounds, metadata observation variants and commit outcome compatibility before bodies. No public or persisted enum is silently extended; schema effects mapped to exact current and frozen predecessor types.
- Existing-file inspection tests: exact dev/ino retained, path replacement cannot redirect promotion, exclusive lock continuous, no secondary token pairing API; empty/recovery/v9/unknown modern root refuses before mutation, original bytes checked. No filesystem owner-link artifact exists.
- Creation tests: missing target allowed only through creation capability; existing empty file refuses; race to create refuses without overwrite.
- Opening faults: malformed predecessor/edge/row/required config gives no promotion; injected failure after promotion is reported separately; failure inside final transaction leaves all selected logical upgrades/config/catalog/log/counter changes uncommitted. Exact predecessor-produced archive/reopen fixtures, not self-generated current-shape substitutes.
- Live writers: concurrent served/direct/config-only ownership tests; source-root-only preserves omitted endpoints/profiles; absent vectors preserve, valid empty clears, invalid empty leaves unchanged; duplicates/overlaps refuse; all inventory policy rows map to field, validation and activation.
- Postcommit maintenance: committed receipt survives injected maintenance failure in generic enabled mode; current Flow no-versioning path separately witnessed.
- First052 startup omits declarations/Continuity families unless intentionally built from a fresh exact runtime observation. Same identity/transcript/work is preserved through eventual capsule and Adopt, which remain later gates.

## Final design checks still required

This is a concrete ownership/transaction shape, not a claim that placeholder dependency types compile. The current reader must supply exact existing record bounds/identity locator and native error types to finish the signature spelling. Core must approve that finite identity capability and opening preparation interface before bodies; in particular the single prevalidated combined upgrade/startup plan must be demonstrably materializable with the reused Engine machinery. A broad generic transaction/CAS API is not proposed.

## Final API delta: typed Flow resolution, with no storage-write capability

The Engine owns a borrowed converted-record view tied to PreparedOpening's owner. The Flow adapter can project only its declared configuration families from that view, using typed descriptors, not reserved catalog/log/counter tables. The view is closure-scoped exactly as inspection is; no transaction or reference into it may escape. It exposes no commit, Engine, Sema, backend, or mutation handle.

```rust
// Flow-private; no cross-crate plugin/trait implementation is admitted.
trait ConfigurationResolving {
    fn resolve(&self, snapshot: ConfigurationInput)
        -> Result<ValidatedConfiguration, ConfigurationFailure>;
}
struct FlowConfigurationResolution {
    requested: Vec<ConfigurationChange>,
}
// Generated from SAME field declarations; absent versus domain None preserved.
struct ConfigurationInput { /* Option per stored field */ }
struct ValidatedConfiguration {
    resolved: ConfigurationSnapshot,
}
```

Only Flow's private validator module constructs ValidatedConfiguration. It contains ONE canonical final resolved snapshot, not a second requested-change list. The resolver holds requested input but stage never receives that input. Its only data input from Engine is owned ConfigurationInput projected from the converted view. resolve overlays requests, rejects duplicate keys, validates every required value and all cross-field constraints, then returns the final snapshot. There is no public ApplicationResolution trait, no caller-supplied resolver object installed in Engine, and no Engine callback into arbitrary user policy.

Exact permitted call graph:

1. Flow opening owner asks Engine's opening-owned plan to prepare selected conversions, without writes. A scoped ConvertedRecords view supplies only owned typed records from declared application families; its constructors and owner association are private to Engine.
2. Flow-private projection returns ConfigurationInput. No transaction, iterator, backend, or storage writer escapes. Flow-private ConfigurationResolving::resolve produces ValidatedConfiguration without any write handle.
3. Flow-private staging consumes ValidatedConfiguration and borrows the same owner's OpeningRows. It projects the resolved snapshot into final typed family rows. The opening owner computes differences against its retained converted view; raw requested changes are never staging input. OpeningRows has no commit method, only typed staged row operations for that owner's declared application families; Engine rejects reserved-family access, owner mismatch and duplicate final coordinates.
4. Engine validates the combined opening plan and consumes it through the single commit boundary. Only Engine materializes catalog/log/counter writes. Flow gets an Engine only after that boundary succeeds.

This is an explicit public/private split: Engine exposes typed scoped converted reads, an opening-owned staging builder and consuming commit; Flow keeps projection/resolution/staging adapters module-private. No public Engine trait allows plugging in a resolver. All owner/view/row-builder fields are private; only the owning opening constructs them. Builder borrows cannot survive the owner, and staged plans cannot be re-associated with another backend. There is no temporary Engine.

Rust cannot prohibit arbitrary global I/O merely from a function signature. The private resolver/projection/staging call graph is therefore a mandatory source-review condition: no global I/O, mutable global state, Engine/Sema handles or unlisted callback calls. Pre-body review checks this specified capability graph; post-body review must witness the actual implementation and fault behavior. A promise is not source evidence.

Live configuration uses the same private resolver and generated final-snapshot row mapping under ConfigurationWriter, feeding existing AtomicCommit. Opening uses that mapping with the combined conversion plan. There is one mapping, not parallel startup/meta validators.

## Exact proposed commit result delta

```rust
// In existing Engine implementation, replacing the current return type:
pub fn commit_atomic(&self, group: AtomicCommit)
    -> sema_engine::Result<CommitOutcome>;
```

This retains the existing method/call path and heterogeneous plan; it is not a second commit engine. Before requested transaction commit, failures return Err(sema_engine::Error). After commit, all maintenance evidence returns Ok(CommitOutcome { receipt, maintenance }); callers cannot interpret postcommit failure as unchanged/refused. Generic Engine and all owned non-Flow consumers must be enumerated and changed together. Flow916's no-versioning case is separately witnessed, not used to justify leaving generic consumers unadapted. Exact consumer ledger and version allocation remain pre-body gates.

## Removed historical provenance work

The former Option<StartedBy> proposal, constructors, migrations and tests are removed by the final Psyche ruling. No provenance field is added in this change.

## Affected consumer boundaries before edits

1. redb: Builder existing-file inspection, reader/lock lifetime and Database writer transition, callers and tests of new API. Existing path open may remain for unrelated consumers, but the approved Flow path must use inspected promotion.
2. Sema: owned inspected construction, schema observation, same-backend promotion and scoped read/write materialization. Existing path callers need explicit retained behavior and no accidental Flow fallback.
3. Engine: EngineOpen/open/registration, typed identity observation, atomic preparation/materialization, family upgrade preparation, shared log/catalog/counter commit and postcommit outcome. Every commit_atomic consumer must handle receipt plus maintenance outcome, including tests and non-Flow owned consumers located before changes.
4. Flow: configuration-only and running open, staged-upgrade path replacement, runtime/meta/executable startup, internal and legacy writers, all policy consumers, generated Start, Nix startup emission, and configuration-only listener. Replace rather than retain the old path-reopen route for approved Flow admission.
5. Ordinary/meta contracts and clients: Resume.FlowId, removed Fable gate, live placement refusal, field-level configuration, snapshot and Continuity; generated projections and all constructors/call sites update together. Launch and Refresh receive no Living payload. No provenance readback is added.
6. Persisted families: explicit inventory of every embedded changed wire/refusal shape, frozen historical mirrors and selected upgrade edges. No version is allocated by this document; collision checks and allocation receipts remain mandatory.

Exact repository consumer lists, dependency clone/lock/base evidence, allocations and independent review are pending artifacts from the verified owner. This proposal names boundaries, not completed check evidence or a cleared writer.
