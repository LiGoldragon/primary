*Kind: Audit · Topic: sema-upgrade-path-current-state · Date: 2026-05-24*

# 317 / 1 — Sema-upgrade path audit (Subagent A)

Audit of the deployed sema-upgrade path as it sits on disk in seven
crates, against the design landed in `/285`, `/287`, and `/315`. The
question every section answers: which protocol concern is **landed**
(real production code paths), which is **stubbed** (the type exists
and the wire round-trips but the handler returns a placeholder), and
which is **designed-only** (ARCH/report mentions it, no Rust file
contains it).

## §1 What's on disk

All seven repos exist as live checkouts at `/git/github.com/LiGoldragon/`.
The orchestrator frame named `owner-signal-version-handover` as
"may not exist yet"; it now exists, is ~228 lines of types, and has
248 lines of round-trip witness tests
(`/git/github.com/LiGoldragon/owner-signal-version-handover/src/lib.rs`,
`tests/round_trip.rs`).

| Repo | Shape on disk | Lib LOC | Notes |
|---|---|---|---|
| `version-projection` | library, 5 source files | `src/lib.rs:1-19` re-exports | All four pieces present: trait, marker, error, policy types, migration index, `ContractVersion`. |
| `signal-version-handover` | signal-contract crate, one `src/lib.rs` | 197 lines | Six operations + seven replies + `MirrorPayload` raw-bytes shape, all generated via `signal_channel!`. |
| `owner-signal-version-handover` | signal-contract crate, one `src/lib.rs` | 228 lines | Four ops (`AttemptHandover` / `ForceFlip` / `Rollback` / `Quarantine`) + observability. EXISTS, contra orchestrator's hedge. |
| `sema-engine` | engine library | `src/sequence.rs:17` `CommitSequence(u64)`; `src/engine.rs:531` `current_commit_sequence`, `:550` `replay_from_sequence`. | Real API, durable per-database counter via `LATEST_COMMIT_SEQUENCE_KEY`. |
| `sema-upgrade` | library + two temporary bins; `src/handover.rs` is the protocol witness. Per ARCH §1 still "library-shaped today; a future `sema-upgrade-daemon` will own…" — the persona-absorbs path of `/315` §2.1. | 324 lines in `src/handover.rs`. | Witness, not production. |
| `persona-spirit` | production daemon; v0.1.1 in `Cargo.toml`. Three sockets bound: `ordinary`, `owner`, `upgrade` (`src/daemon.rs:138-140` + `src/daemon.rs:580-651` for bind). A fourth optional `engine_management` socket exists but is unrelated to handover. | n/a | Real upgrade socket; protocol handled in `src/actors/root.rs:221-388`. |
| `persona` | manager daemon; `src/upgrade.rs` (746 lines) owns the `HandoverDriver` + four event types; `src/manager.rs:260-401` owns the four manager messages and owner-handover dispatch. | n/a | Real client of `signal-version-handover` against component upgrade sockets. |

## §2 Per-crate current state

### §2.1 `version-projection`

**Landed**:

- `VersionProjection<Source, Target>` trait with associated `Error`
  type (`src/projection.rs:9-13`). Matches /285 §1.2 signature
  exactly (one method `project(Source) -> Result<Target, Error>`).
- `Projected` marker with `CONTRACT_VERSION` const +
  `component()` function (`src/projection.rs:17-21`).
- `Identity` blanket impl `VersionProjection<T, T>` for every
  `T: Projected` (`src/projection.rs:24-32`).
- `ProjectionError` with `NotRepresentable`, `TransformFailed`,
  `DirectionNotImplemented` (`src/projection.rs:34-47`). Matches
  /285 §1.5.
- `ComponentPolicy` / `OperationPolicy` / `PerOperationPolicy` /
  `OperationKind` (`src/policy.rs:99-115`).
- `WritePolicy` (`Mirror` / `DivergenceRecord` / `Reject`),
  `ReadPolicy` (`ActiveProjectsResponse` / `DualQueryMerge` /
  `ActiveOnly`), `SubscribePolicy` (`ResumeAgainstNext` /
  `TerminateAtHandover`, default `TerminateAtHandover` per
  `src/policy.rs:62-66`).
- `MigrationIndex` + `MigrationIndexEntry` carrying
  `(ComponentName, ContractVersion, DecodeFunction)` triple
  (`src/index.rs:24-55`); `find()` is linear scan (`:71-80`).
- `ContractVersion([u8; 32])` with NOTA byte-literal encoding
  (`src/version.rs:33-71`). 32 bytes hard-coded; the Blake3-hash
  binding rule from /285 §7.3 is documented in
  `ARCHITECTURE.md:81-86` but no hash *generator* lives here
  (per the "no schema-hash generation" non-goal at
  `ARCHITECTURE.md:141-142`).

**Stubbed / partial**:

- No production crate ships a non-`Identity` `VersionProjection<X, Y>`
  impl today. Search of all seven repos returns only the test types
  `LegacyToCurrent` / `CurrentToLegacy` in
  `sema-upgrade/tests/handover.rs:28-58`. `persona-spirit/src/store.rs:337`
  implements `Projected` for `StampedEntry` (the private storage
  wrapper) but NOT `VersionProjection<historical::StampedEntry, StampedEntry>`.
  The trait is loaded; no production type binds to it.

**Designed-only**:

- Per-operation policy *literals* for Spirit (the `Reject /
  ActiveProjectsResponse / TerminateAtHandover` table from /285
  §8.2) live nowhere — no `persona-spirit/src/version_policy.rs`
  exists. Search returns zero hits.
- Owner-side handover contract `owner-signal-version-handover`
  is listed as Possible-features
  (`version-projection/ARCHITECTURE.md:151-158`), but the contract
  has since landed (see §2.3). The Possible-features text is stale.
- Typed Mirror payload shape (Possible-features at
  `ARCHITECTURE.md:159-164`) — superseded by spirit 274 (Maximum)
  Maximum-certainty Decision to keep raw bytes. The
  Possible-features entry no longer reflects intent. See §5.

### §2.2 `signal-version-handover`

**Landed**:

- `signal_channel!` macro instantiation
  (`src/lib.rs:179-197`) emits `VersionHandover` channel with
  six operations and seven replies. Matches /285 §3.4 table.
- All six operations exist as request payload types:
  - `AskHandoverMarker(MarkerRequest)` (`src/lib.rs:85-87`)
  - `ReadyToHandover(ReadinessReport)` (`:89-93`)
  - `HandoverCompleted(CompletionReport)` (`:95-99`)
  - `Mirror(MirrorPayload)` (`:101-108`)
  - `Divergence(DivergencePayload)` (`:110-118`)
  - `RecoverFromFailure(RecoveryRequest)` (`:120-124`)
- `HandoverMarker` carries the full /285 §3.4 shape:
  `component`, `schema_hash: ContractVersion`, `commit_sequence: u64`,
  `write_counter: u64`, `last_record_identifier: Option<u64>`,
  `recorded_at_date: Date`, `recorded_at_time: Time`
  (`src/lib.rs:73-82`). Note the marker captures wallclock locally
  via `Date` / `Time` records defined inline (`:13-71`) — these
  carry `NotaEncode` / `NotaDecode` impls that route through
  `nota_codec::Encoder::write_date` / `write_time`.
- `MirrorPayload` carries raw bytes + `RecordKind` discriminant
  (`src/lib.rs:102-108`). Matches spirit 274 (Maximum certainty):
  raw bytes in their own container. There is NO typed Mirror
  variant.
- `DivergencePayload` carries the same shape plus a
  `DivergenceReason` enum (`NotRepresentable` / `TargetUnavailable`
  / `TargetRejected`) at `src/lib.rs:110-177`.
- `HandoverRejectionReason` covers `SchemaMismatch`,
  `CommitSequenceAdvanced`, `AlreadyInHandover`, `NotReady`
  (`src/lib.rs:160-168`).
- Six NOTA + frame round-trip tests in `tests/round_trip.rs:1-113`.

**Stubbed / partial**: None at the contract level — this crate is
pure wire vocabulary.

**Designed-only**: Read-during-handover semantics
(`ARCHITECTURE.md:256-258` Possible-features entry — never lands
into operations, lives only as the daemon's read-pause discipline).
This is correctly deferred.

### §2.3 `owner-signal-version-handover`

**Landed**:

- Four operations: `AttemptHandover`, `ForceFlip`, `Rollback`,
  `Quarantine` (`src/lib.rs:198-218` `signal_channel!`).
- Six reply variants matching the operations plus `Rejected` +
  `RequestUnimplemented` (`:205-212`).
- `Version` record pairing `VersionLabel` (string) with
  `ContractVersion` (32-byte hash) (`src/lib.rs:15-19`).
- `VersionEndpoint` carrying `(version, owner_socket_path,
  upgrade_socket_path)` (`src/lib.rs:127-131`); this is what
  Persona consumes to dial the four sockets per §1.6.7.
- `ForceReason`, `RollbackReason`, `QuarantineReason` typed
  enums (`src/lib.rs:79-101`).
- `RejectionReason` covers eight cases — `UnknownComponent`,
  `UnknownVersion`, `NotAllowed`, `AlreadyQuarantined`,
  `NotQuarantined`, `VersionQuarantined`, `HandoverRejected`,
  `UpgradeSocketUnavailable` (`:165-177`).
- `observable` clause in the channel
  (`src/lib.rs:213-217`) with `OperationReceived` /
  `EffectEmitted` event types.
- Canonical NOTA examples + round-trip tests for every operation
  and reply (`tests/round_trip.rs:129-247`).

**Stubbed**: Nothing in the contract.

**Designed-only**: ARCHITECTURE.md is intentionally terse (42
lines, `ARCHITECTURE.md:1-42`). It explicitly notes "Runtime safety
decisions remain in Persona. This crate only supplies typed owner
vocabulary and typed replies" (`:38-40`) — so the contract is the
finished slice and runtime behaviour properly lives in `persona/`.

The /315 §2.2 statement that bead `primary-7kge` (P1) "carries the
contract crate" is now satisfied. **The /315 §2.2 entry should
retire** — only the `version-projection/ARCHITECTURE.md`
Possible-features text needs cleanup.

### §2.4 `sema-engine` — `CommitSequence`

**Landed**:

- `CommitSequence(u64)` struct with `genesis()`, `new(value)`,
  `value()`, `next()` (`src/sequence.rs:17-35`).
- `Engine::current_commit_sequence(&self) -> Result<CommitSequence>`
  reading from the `LATEST_COMMIT_SEQUENCE_KEY` counter in redb
  (`src/engine.rs:531-539`). Persisted across restarts.
- `Engine::replay_from_sequence(&self, start: CommitSequence) ->
  Result<Vec<CommitLogEntry>>` (`src/engine.rs:550-559`) doing a
  full-log iteration then a `filter` — linear scan but functional.
- Internal `next_commit_sequence` minted on every commit
  (`src/engine.rs:97`, `:168`, `:235`, `:383`); each commit
  appends a `CommitLogEntry` (`src/log.rs:16-47`) carrying the
  sequence + record key + snapshot id + table name and writes
  the new high-water mark into the `COUNTERS` table
  (`src/engine.rs:114-118`).

**Stubbed**: None — this is fully landed and matches /315 §4
("already absorbed"). The signal of an actually-durable monotonic
counter is solid.

**Designed-only**: None remaining for the handover path.

### §2.5 `sema-upgrade`

The crate sits in the persona-absorbs lean from /315 §2.1: it is a
library with two temporary bins, NOT a triad daemon. The
`sema-upgrade-daemon` does not exist on disk and ARCH §"Possible
features" calls this out (`ARCHITECTURE.md:178-186`).

**Landed**:

- Library exposes `Engine`, `Lowering`, `MigrationIndex`,
  `DatabaseMigration`, and `PrototypeHandover`
  (`src/lib.rs:7-21`).
- `MigrationIndex::prototype()` returns a single-row index
  containing the persona-spirit `0.1.0 → 0.1.1` module
  (`src/index.rs:158-162`). The module is wired to its own
  database-migration function via
  `migrations::persona_spirit::version_0_1_0_to_0_1_1::module()`.
- The Spirit migration module
  (`src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`)
  follows the two-submodule pattern from ARCH §"Two-submodule
  migration pattern": `mod historical` (`:102-236`) reproduces
  the deployed v0.1.0 types byte-for-byte; `mod current_shape`
  (`:238-318`) builds the v0.1.1 records from historical ones.
  The Certainty → Magnitude conversion lives at lines 303-311
  as a plain `From<historical::Certainty> for Magnitude` impl
  (not via the `VersionProjection` trait — see gap matrix §3).
- `migrate_paths(source, target)` (`:34-51`) is the production-
  shaped function: validates source exists, target doesn't,
  paths differ; reads historical records via the `historical`
  schema; writes them through `current_shape::from(...)` into
  the target. Three unit tests at `:328-373` cover the happy path
  and two rejection paths.
- `Engine` (`src/execution.rs:93-118`) is the `signal-executor`-
  shaped wrapper that turns the `signal-sema-upgrade` working
  contract into per-command `Effect`s. `Engine::prototype()`
  is the entry point.
- `PrototypeHandover` (`src/handover.rs:121-272`) is the
  testable state machine: two `PrototypeEndpoint`s
  (current and next) plus an `active: ActiveVersion` selector
  and a divergence sink (`Vec<DivergencePayload>`). State
  enum `EndpointState::{Public, Handover, PrivateUpgradeOnly}`
  at `:21-25` matches /287 §4. `PrototypeHandover::for_spirit_0_1_0_to_0_1_1`
  (`:139-145`) builds the fixture with synthetic 32-byte
  schema hashes (`[1; 32]` / `[2; 32]`) — not real Blake3 hashes.
- `mirror_with_projection<Projection, Source, Target>`
  (`src/handover.rs:219-272`) is the only production-shaped
  function that actually composes `VersionProjection::project`
  with the `Mirror` / `Divergence` wire path. It is generic over
  the projection type and called by the test suite only.
- Two temporary bins:
  - `sema-upgrade-temporary`
    (`src/bin/sema_upgrade_temporary.rs:1-109`) — one-NOTA-arg
    CLI that decodes `(Attempt (<source-path> <target-path>
    (<component> <source-version> <target-version>)))` and
    invokes `MigrationIndex::prototype().migrate_database(...)`.
    Used by the Nix sandbox apps to drive the database half of
    the cutover.
  - `sema-upgrade-handover-temporary`
    (`src/bin/sema_upgrade_handover_temporary.rs:1-37`) — one-
    NOTA-arg CLI accepting only `(RunSpirit010To011)` literally,
    running the `PrototypeHandover` state machine in-process and
    printing `(SmartHandoverCompleted persona-spirit
    CurrentPrivateUpgradeOnly NextPublic)`. Per ARCH
    §"Nix Live Sandbox" this bin retires once the deployed
    v0.1.0 daemon has its own private upgrade socket.

**Stubbed**:

- `MirrorDecision::Diverged` records into `self.divergences`
  (`src/handover.rs:267`) but the divergence sink is in-memory
  only — there is no persona-introspect or persistent log behind
  it. Matches `ARCHITECTURE.md:186-193` Possible-features entry.
- `RecoverFromFailure` in the prototype hard-codes
  `recovered: false` (`src/handover.rs:68-71`) — no actual
  recovery is attempted in the state machine.

**Designed-only**:

- `sema-upgrade-daemon` triad (ARCH §"Possible features").
- Production mirror payload application against real daemon
  sockets (ARCH §"Possible features"). The path is proven in
  prototype but never crosses a socket in production.

### §2.6 `persona-spirit` — private upgrade socket addition

The orchestrator frame asked specifically for the "third socket
beside ordinary + owner." It exists:
`upgrade_socket_path: SocketPath` at
`src/daemon.rs:49`, bound via
`SocketBinding::bind(&self.configuration.upgrade_socket_path, …)`
at `src/daemon.rs:589-592` and listened via
`UnixListener::bind(self.configuration.upgrade_socket_path.as_path())`
at `:623-624`. The bind path sets the same socket mode as ordinary
+ owner (`:647-651`). A fourth optional socket
(`engine_management_socket_path`, `src/daemon.rs:54`) exists but
is unrelated to handover.

**Landed**:

- Bound, mode-set, listened private upgrade socket (above).
- `serve_upgrade_one()` at `src/daemon.rs:780-793` runs one
  request/reply exchange off the upgrade listener.
- `serve_forever()` spawns the upgrade-listener thread alongside
  ordinary and owner (`src/daemon.rs:881-938`); on shutdown the
  upgrade socket file is removed (`:967`).
- `UpgradeSocketServer` and `UpgradeExchangeHandler`
  (instantiated at `:900-908` and `:996-1006`) handle the
  serve-forever loop.
- `SubmitUpgradeRequest` Kameo message
  (`src/actors/root.rs:54-56`) carries `signal_version_handover::Operation`
  into the root actor, which dispatches in `submit_upgrade_request`
  (`src/actors/root.rs:221-388`). All six operations have real
  branches.
- `HandoverState { Active, HandoverMode { accepted_marker },
  PrivateUpgradeOnly }` (`src/actors/root.rs:92-99`) matches /287
  §4 state diagram exactly. Public-socket state mirrors this
  via the `PublicSockets` struct (`src/daemon.rs:195-206`,
  transitions at `:1410-1427`):
  - `ReadyToHandover` reply `HandoverAccepted` triggers
    `public_sockets.enter_handover_mode()` (`:1410-1412`) — reads
    accepted, writes rejected.
  - `HandoverCompleted` reply `HandoverFinalized` triggers
    `public_sockets.close()` (`:1413-1415`) — both ordinary and
    owner refuse all requests after.
  - `RecoverFromFailure` reply `RecoveryCompleted{recovered:true}`
    triggers `public_sockets.leave_handover_mode()` (`:1416-1426`).
  These three lifecycle transitions are real and tested.
- `AskHandoverMarker` reads from the store actor
  (`src/actors/root.rs:228-236`); the marker is built in
  `SpiritStore::handover_marker` (`src/store.rs:128-148`) from
  the actual `sema-engine` `current_commit_sequence`
  (`:134-138`) plus `last_record_identifier` (`:144`) plus a
  daemon-stamped wall-clock date/time
  (`HandoverClock::read` at `:213-220`).
- `ReadyToHandover` re-reads the marker, requires the
  `commit_sequence` to match the client-supplied
  `source_marker`, and refuses with
  `HandoverRejectionReason::CommitSequenceAdvanced` otherwise
  (`src/actors/root.rs:237-271`). `AlreadyInHandover` rejection
  also fires (`:266-269`) if state isn't `Active`.
- `HandoverCompleted` validates state is `HandoverMode` AND the
  `accepted_marker` still matches the stored marker; the latter
  guards against drift between `ReadyToHandover` and
  `HandoverCompleted` (`src/actors/root.rs:272-310`).
- `Mirror` handler decodes the raw bytes directly into the
  receiver's own `crate::store::StampedEntry` via `rkyv::from_bytes`
  (`src/actors/root.rs:325-358`) and asserts into the store.
  Returns `MirrorAcknowledged` if successful or
  `HandoverRejected{SchemaMismatch}` otherwise. This is the path
  the orchestrator frame asked specifically about.
- `Spirit` `Projected` impl on the private `StampedEntry`
  wrapper, with `CONTRACT_VERSION = SPIRIT_CONTRACT_VERSION`
  (a literal 32-byte array starting with thirty zeros then
  `1, 1, 0` — clearly placeholder, not Blake3) and
  `component() -> ComponentName::new("persona-spirit")`
  (`src/store.rs:337-343`).
- Integration tests covering the full upgrade exchange:
  `persona_spirit_daemon_serves_version_handover_frames_through_upgrade_socket`
  at `tests/daemon.rs:626-734` runs `AskHandoverMarker →
  ReadyToHandover → HandoverCompleted` through three threads and
  asserts the ordinary + owner socket files are removed after
  completion. `persona_spirit_upgrade_completion_requires_accepted_readiness`
  at `tests/daemon.rs:737-`… verifies completion is gated.

**Stubbed**:

- `Mirror` decodes raw bytes ONLY as the receiver's own
  `crate::store::StampedEntry` shape (`src/actors/root.rs:325-326`).
  There is no `VersionProjection` call on the receiver side. The
  payload encoding is implicit: sender must already have produced
  bytes that decode as the receiver's current `StampedEntry`. This
  works for v0.1.0 → v0.1.1 (the live cutover direction) because
  v0.1.1 is the wider type and a forward projection runs on the
  sender side — but the *reverse* direction (live v0.1.1 → v0.1.0
  during overlap) needs `VersionProjection<Magnitude, Certainty>`
  to run on the receiver and that impl doesn't exist on disk.
- `Mirror.kind` is required to equal the literal string
  `"StampedEntry"` (`MIRROR_KIND_STAMPED_ENTRY` const at
  `src/actors/root.rs:21`); other `RecordKind` values are
  rejected. Hard-coded — no extensibility for additional record
  shapes.
- `Divergence` handler returns
  `DivergenceAcknowledgement{divergence_identifier: 0}`
  literally (`src/actors/root.rs:361-368`) — the divergence is
  acknowledged but never persisted or counted. Matches the gap
  flagged for sema-upgrade's prototype.
- `RecoverFromFailure` is partial: from `HandoverMode` it
  transitions back to `Active` and returns `recovered: true`
  (`:369-384`); from `PrivateUpgradeOnly` it returns
  `recovered: false`. There is no replay of failed mirror
  payloads, no consultation of a divergence log, no compensating
  state-machine sequence. This is the "recovery" of
  `/sema-upgrade ARCHITECTURE.md:186-193` Possible-features
  entry — only partial.
- `SPIRIT_CONTRACT_VERSION` (`src/store.rs:21-23`) is a
  hand-written 32-byte placeholder (zeros + `1, 1, 0`), not a
  Blake3 hash of the schema. The /285 §7.3 "schema-version hash
  binding" rule is unattested in code; the `ContractVersion`
  type holds bytes but no Blake3 generator exists in any of the
  seven repos (consistent with `version-projection/ARCHITECTURE.md:141-142`
  non-goal: "No schema-hash generation").
- `write_counter == commit_sequence` literally
  (`src/store.rs:142-143`). The marker carries both fields, but
  they alias in production. /285 §3.4 names them as separate
  fields without specifying the semantic difference; in
  practice the daemon treats them as one value.

**Designed-only**:

- A `VersionProjection<v0_1_0::Entry, v0_1_1::Entry>` impl in
  a frozen `signal-persona-spirit-v0-1-0` crate per /285 §8.1
  ("`SpiritEntryForward` maps `Certainty → Magnitude`…"). The
  frozen crate exists conceptually — `sema-upgrade`'s migration
  module reproduces the v0.1.0 layout inline (`mod historical`
  at `version_0_1_0_to_0_1_1.rs:102-236`) — but no
  `signal-persona-spirit-v0-1-0` crate exists in `/git/github.com/LiGoldragon/`,
  and the `From<historical::Certainty> for Magnitude` impl at
  `version_0_1_0_to_0_1_1.rs:303-311` is NOT routed through the
  `VersionProjection` trait. This is the **single largest
  in-code gap** between design and shipped state.
- `version_policy.rs` (per /285 §8.2) does not exist in
  `persona-spirit/src/`.
- The fourth optional socket
  (`engine_management_socket_path`, `src/daemon.rs:54`) is the
  Persona-to-component management channel, not part of the
  three-socket handover surface — included here only because the
  orchestrator frame might confuse it with a handover socket.

### §2.7 `persona` — orchestrator role

The persona engine is the upgrade orchestrator per spirit
208/209/210 and /287 §5. The §1.6.7 of `persona/ARCHITECTURE.md`
documents the role; the implementation is in `src/upgrade.rs` (746
lines) and `src/manager.rs:260-401`.

**Landed**:

- `Target` value (`src/upgrade.rs:49-71`) carries the four-socket
  shape from `persona/ARCHITECTURE.md:504-516`:
  `(component, current_version, next_version,
  current_owner_socket_path, current_upgrade_socket_path,
  next_owner_socket_path, next_upgrade_socket_path)`. Built from
  `owner_signal_version_handover::AttemptHandover` via
  `Target::from_owner_attempt` (`:73-83`).
- `HandoverClient` (`src/upgrade.rs:306-377`) wraps a Unix
  socket dial of the component's upgrade socket; carries
  `ask_marker`, `ready_to_handover`, `complete_handover`,
  `recover_from_failure` async methods that submit a single
  `HandoverOperation` and pattern-match the expected reply
  variant.
- `HandoverDriver::drive_current_side` (`src/upgrade.rs:434-477`)
  is the production protocol orchestration. The sequence:
  1. `current.ask_marker` (`:436-441`)
  2. `next.ask_marker` (`:442-447`)
  3. `Self::ensure_next_marker_matches(&marker, &next_marker)`
     (`:448`) — requires `component`, `commit_sequence`,
     `write_counter`, `last_record_identifier` to all match
     (`:479-501`).
  4. `current.ready_to_handover` (`:449-455`)
  5. `current.complete_handover` (`:456-463`); on failure,
     `current.recover_from_failure` is best-effort dispatched
     (`:465-473`).
- `EngineManager::drive_version_handover`
  (`src/manager.rs:290-300`): quarantine-gates the target,
  records `UpgradePrepared`, starts the next component unit
  via `start_next_component_unit` (`:302-315`, dispatches to
  `unit_manager.ask(StartUnit::new(unit))`), runs the
  `HandoverDriver`, completes the upgrade. Persona-as-orchestrator
  is real, not aspirational.
- `EngineManager::handle_owner_version_handover`
  (`src/manager.rs:345-401`) dispatches the four owner ops:
  `AttemptHandover` → `drive_version_handover`;
  `ForceFlip`, `Rollback` → direct `ActiveVersionChanged` event
  append without protocol; `Quarantine` → `VersionQuarantined`
  event append.
- Active-version event-log model:
  `ActiveVersionChangeSource::{HandoverMarker, ForceFlip,
  Rollback}` (`src/upgrade.rs:568-587`) plus
  `ActiveVersionChanged` (`:594-654`) and `VersionQuarantined`
  (`:661-693`) and `ActiveVersion` (`:696-746`) — all rkyv-
  archived so they persist into the manager event log.
- Quarantine gate enforced before each
  `prepare_upgrade` / `drive_version_handover` via
  `ensure_target_not_quarantined` (`src/manager.rs:317-343`),
  matching `persona/ARCHITECTURE.md:602-608`.

**Stubbed**:

- `start_next_component_unit` (`src/manager.rs:302-315`) routes
  through `unit_manager.ask(StartUnit::new(unit))`. The
  production controller `SystemdTransientUnitController`
  (referenced in `persona/ARCHITECTURE.md:557-568`) requires
  systemd D-Bus to actually launch a unit; tests inject a
  recording controller. The deploy path landing isn't audited
  here, but the wiring exists.
- `handover_rejection_reason` (`src/manager.rs:403-412`) maps
  errors to `RejectionReason` enums; it's a sparse mapping
  (only `ComponentVersionQuarantined`, `Io`,
  `UnexpectedSignalFrame`, `HandoverMarkerComponentMismatch`
  are distinguished; everything else collapses to
  `HandoverRejected`).
- Persona's `HandoverDriver` never sends `Mirror` or
  `Divergence` operations — those are exclusively
  next-to-current and the next daemon emits them. The
  `HandoverClient` on persona has `ask_marker`,
  `ready_to_handover`, `complete_handover`,
  `recover_from_failure` only (`:327-376`). This is consistent
  with /287 §4: Persona orchestrates the high-level
  current-side protocol; Mirror/Divergence are next-side
  responsibilities.

**Designed-only**:

- Persona's manager event log is mentioned in §1.6.7 as the
  active-version selector home (`persona/ARCHITECTURE.md:478-480`,
  "lives in Persona's manager event log, not in CriomOS-home
  filesystem symlinks"). The `ActiveVersion` snapshot reducer is
  referenced (§1.6.7, `:570-575`) — the rkyv-archive types exist
  in `src/upgrade.rs:696-746` but the snapshot read/write paths
  weren't traced in this audit beyond the `complete_upgrade`
  append (`src/manager.rs:271-288`).
- Design D public-socket handoff (`persona/ARCHITECTURE.md:577-600`)
  is a separate concern — `src/transport.rs` — outside the
  handover protocol's scope.

## §3 Gap matrix

Rows are the concerns the orchestrator frame named. Columns:
designed location (`/285`, `/287`, `/315`, or per-repo ARCH),
in-code location (file:line or "not present"), status
(Landed / Stubbed / Designed-only), Spirit-pilot critical-path?
(does `primary-x3ci` block on this?).

| Concern | Designed | In-code | Status | Pilot critical? |
|---|---|---|---|---|
| `VersionProjection<Source, Target>` trait | `/285` §1.2 | `version-projection/src/projection.rs:9-13` | Landed | Yes — entire migration story rests on this trait being importable. |
| `Projected` marker | `/285` §1.2 | `version-projection/src/projection.rs:17-21`; sole prod impl `persona-spirit/src/store.rs:337-343` | Landed (trait) / Stubbed (only one impl, on the private wrapper) | Partial — production daemon's `Projected` impl on `StampedEntry` is real; no `Projected` on the Spirit public `Entry`. |
| `VersionProjection<v0_1_0::Entry, v0_1_1::Entry>` (Spirit) | `/285` §8.1 (`SpiritEntryForward` / `SpiritEntryReverse`) | not present; `From<historical::Certainty> for Magnitude` exists at `sema-upgrade/.../version_0_1_0_to_0_1_1.rs:303-311` but NOT as `VersionProjection` impl; tests-only at `sema-upgrade/tests/handover.rs:28-58` | Designed-only (live cutover); Stubbed (test fixture) | **Yes — blocking.** The Spirit cutover ships v0.1.1 records that landed via the migration; reverse projection from v0.1.1 → v0.1.0 during the `Mirror` overlap window cannot run because the impl doesn't exist. The /287 §6 Phase 3 "Mirror writes if old-compat reads needed" story has nothing behind it. |
| `AskHandoverMarker` exchange | `/285` §3.4, `/287` §3 | `signal-version-handover/src/lib.rs:85-87`, daemon impl `persona-spirit/src/actors/root.rs:228-236`, store read `persona-spirit/src/store.rs:128-148`, orchestrator `persona/src/upgrade.rs:327-337`, drive `persona/src/upgrade.rs:436-447` | Landed end-to-end | No (already real). |
| `ReadyToHandover` exchange | `/285` §3.4, `/287` §3 | `signal-version-handover/src/lib.rs:89-93`, daemon impl `persona-spirit/src/actors/root.rs:237-271`, drift refusal `:259-264`, orchestrator `persona/src/upgrade.rs:339-349`, drive `persona/src/upgrade.rs:449-455` | Landed end-to-end | No. |
| `HandoverCompleted` exchange | `/285` §3.4, `/287` §3 | `signal-version-handover/src/lib.rs:95-99`, daemon impl `persona-spirit/src/actors/root.rs:272-310`, public-socket close `persona-spirit/src/daemon.rs:1413-1415`, orchestrator `persona/src/upgrade.rs:351-364`, drive `persona/src/upgrade.rs:456-475` | Landed end-to-end | No. |
| `Mirror` payload (raw bytes per spirit 274) | `/285` §3.4, signal-version-handover ARCH §"Mirror payload — raw bytes in a separate container", `/315` §2.3, spirit 274 Maximum | wire `signal-version-handover/src/lib.rs:101-108`, sema-upgrade prototype `sema-upgrade/src/handover.rs:219-272`, daemon receiver `persona-spirit/src/actors/root.rs:311-360` | Stubbed (production) | **Yes — partial-blocking.** The wire format is fine; the receiver in production decodes raw bytes directly as its own `StampedEntry` without going through reverse projection or storing the raw bytes in a separate container first. The "raw bytes in a separate container" discipline from signal-version-handover ARCH §"Receiver-side storage discipline" (`signal-version-handover/ARCHITECTURE.md:213-216`) has no on-disk container in `persona-spirit`. For the v0.1.0 → v0.1.1 cutover the Magnitude widening means forward projection on the sender saves us: bytes land that already decode as v0.1.1 shape. But the discipline is unattested in code. |
| `Divergence` operation + sink | `/285` §3.4 / §6 (cross-version-failures table), signal-version-handover ARCH | wire `signal-version-handover/src/lib.rs:110-118`, sema-upgrade prototype sink in-memory `sema-upgrade/src/handover.rs:267`, daemon stub `persona-spirit/src/actors/root.rs:361-368` (always returns `divergence_identifier: 0`) | Stubbed | Not for first cutover (forward-only direction is lossless); Yes for second-component cutovers and steady-state operation. |
| `RecoverFromFailure` operation | `/285` §3.4, signal-version-handover ARCH | wire `signal-version-handover/src/lib.rs:120-124`, daemon partial `persona-spirit/src/actors/root.rs:369-384` (transitions HandoverMode→Active or returns false from PrivateUpgradeOnly), orchestrator `persona/src/upgrade.rs:366-376` + best-effort dispatch in `persona/src/upgrade.rs:465-473` | Stubbed | Not for first cutover (degenerate case is stop-old/start-new); Yes for cutovers with live writes mid-protocol. |
| `ForceFlip` (owner contract) | `/285` §9 ("not shipped today"), `/315` §2.2, owner ARCH | wire `owner-signal-version-handover/src/lib.rs:103-109`, dispatcher `persona/src/manager.rs:364-373` (direct event log append) | Landed | No (administrative). |
| `Rollback` (owner contract) | as above | wire `owner-signal-version-handover/src/lib.rs:111-117`, dispatcher `persona/src/manager.rs:374-383` | Landed | No (administrative). |
| `Quarantine` (owner contract) | as above | wire `owner-signal-version-handover/src/lib.rs:119-124`, dispatcher `persona/src/manager.rs:384-393`, gate `persona/src/manager.rs:317-343` | Landed end-to-end | No (administrative; gate is live for the cutover protection rail). |
| Persona-as-orchestrator | `/287` §5, `persona/ARCHITECTURE.md` §1.6.7, spirit 208/209/210 | `persona/src/upgrade.rs` (HandoverDriver), `persona/src/manager.rs:260-401` (manager messages, owner dispatch, quarantine gate, next-unit start) | Landed | Yes — `primary-a5hu` Persona epic is upstream of `primary-x3ci`. Per /315 §6 "Persona must land before Spirit cutover." The code is on disk; full deployment readiness wasn't audited. |
| `ContractVersion` real (Blake3) | `/285` §7.3 ("schema-version hash binding"), version-projection ARCH §"Version identity" | type at `version-projection/src/version.rs:33-71`; producer not present (per non-goal at `version-projection/ARCHITECTURE.md:141-142`); placeholder `SPIRIT_CONTRACT_VERSION` at `persona-spirit/src/store.rs:21-23` | Designed-only (generator) / Stubbed (literal) | No for first cutover (placeholder bytes round-trip and the marker validation compares equal-to-equal). Yes for steady state (drift detection would silently miss a schema change). |
| `MigrationIndex` runtime use | `/285` §6.3 (compile-time signal-X library lookup) | `version-projection/src/index.rs:24-90` (types only — `entries: Vec<MigrationIndexEntry>`, `find` is linear); separate `sema-upgrade::MigrationIndex` at `sema-upgrade/src/index.rs:148-193` (different shape — wraps `MigrationModule`s; not the same type). | Stubbed (overlap, two indices) | Not for first cutover; Yes for the persona-introspect cross-version-failure decode path from /285 §6. |
| Sandbox witness (217/218-record migration) | `/287` §7, `/315` §1 | `sema-upgrade/flake.nix:298-474` (`spirit-smart-handover-sandbox` shell app), drives `sema-upgrade-temporary` + `sema-upgrade-handover-temporary` + tagged `persona-spirit-v0-1-0` + tagged current `persona-spirit` | Landed | This IS the substrate proving the cutover works in-the-large. |

## §4 Spirit pilot — first-live-test focus

The Spirit cutover bead `primary-x3ci` ships v0.1.0 → v0.1.1 in
production. Mapping the gap matrix rows onto critical-path status:

**Blocks `primary-x3ci`** (must land before the cutover):

- **`primary-a5hu` Persona deploy**: per `persona/ARCHITECTURE.md:481-483`
  "Persona lands BEFORE the first Spirit cutover (intent 209); Spirit
  v0.1.0 is retrofitted with the upgrade socket and v0.1.1 lands
  with the full handover protocol live, driven by Persona." The code
  exists; this is a deploy gate, not a code gate. **/315 §6 names
  this explicitly.**
- **Spirit v0.1.0 retrofit with private upgrade socket**: the
  deployed v0.1.0 daemon does NOT have a private upgrade socket
  (`sema-upgrade/ARCHITECTURE.md:151-156` explicit:
  "The deployed `v0.1.0` daemon does not yet own that socket"). The
  `sema-upgrade-handover-temporary` external runner exists
  precisely as the bridge until retrofit lands.
- **Hand-written `VersionProjection<Magnitude, Certainty>`** (the
  reverse direction). For a forward-only Spirit cutover where v0.1.0
  is shut down at the cutover moment, this is dispensable — the
  pilot can use stop-old / start-new per /285 §9 ("First v0.1.0 →
  v0.1.1 uses stop-old / start-new; from the second cutover the
  counter is the precondition for zero-downtime handover"). For a
  zero-downtime cutover with live mirror writes during the overlap,
  the reverse projection impl must exist or the `Mirror` handler in
  `persona-spirit/src/actors/root.rs:325-358` will succeed only for
  records that already round-trip as v0.1.1 shape — which is most of
  them but not records written with widened `Magnitude::High` /
  similar.

**Does NOT block `primary-x3ci`** (deferrable to second cutover):

- Full `Divergence` sink (in-memory is fine; the cutover doesn't
  produce divergences if writes only flow main → next).
- `RecoverFromFailure` beyond the partial state-machine recovery
  in `persona-spirit/src/actors/root.rs:369-384`.
- Blake3 `ContractVersion` generator (the placeholder bytes still
  compare equal-to-equal for marker validation).
- Production-shaped raw-bytes side container per
  `signal-version-handover/ARCHITECTURE.md:213-216` (the daemon
  receiver decodes directly today; the cutover Magnitude widening
  is forward-projection-on-sender, so the receiver always sees
  bytes that decode as its own shape).
- `sema-upgrade-daemon` triad — `/315` §2.1 lean is
  persona-absorbs.

**Could trip the cutover unexpectedly** (audit-worthy):

- The `MIRROR_KIND_STAMPED_ENTRY` hard-coding at
  `persona-spirit/src/actors/root.rs:21` means a Mirror with any
  other `RecordKind` is silently rejected as `SchemaMismatch`.
  Operationally, the sender is `sema-upgrade::handover` (test path,
  not live cutover) and the live cutover path doesn't have a
  production sender at all — there's no real `Mirror` traffic in
  the first cutover. But anything that DOES send a Mirror with a
  different kind will be rejected as if there's a schema mismatch.
- `write_counter == commit_sequence` at
  `persona-spirit/src/store.rs:142-143`. If the operator (or a
  future maintainer) ever distinguishes the two in design, the
  shipped daemon treats them as one variable. Drift in semantics
  would silently work in both daemons because both alias.
- `HandoverDriver::ensure_next_marker_matches`
  (`persona/src/upgrade.rs:479-501`) requires the next daemon's
  marker to equal the current daemon's marker on `component`,
  `commit_sequence`, `write_counter`, `last_record_identifier`.
  At first start the next daemon's database is empty —
  `commit_sequence == 0`, `last_record_identifier == None` — and
  the current daemon has actual writes. The driver will REFUSE the
  handover with `NextHandoverMarkerMismatch`. Either the sandbox
  shell script handles this externally by populating next's
  database first (it does, via
  `sema-upgrade-temporary` migration before starting the next
  daemon, see `sema-upgrade/flake.nix:403-431`), or the production
  cutover script must do the same. The driver's logic assumes the
  caller has primed the next database; **the production pilot
  needs an explicit step (run `sema-upgrade-temporary` against the
  v0.1.0 redb to produce the v0.1.1 redb) BEFORE invoking
  `AttemptHandover`**. This is unattested in
  `persona/ARCHITECTURE.md`.

## §5 Mirror-payload retirement — Possible-features cleanup

Three ARCH files name the typed Mirror payload as a coordinated
Possible-features entry:

- `version-projection/ARCHITECTURE.md:159-164` — "Typed `Mirror`
  payload shape. … Lean: bytes, until a second component handover
  surfaces."
- `signal-version-handover/ARCHITECTURE.md:244-254` — "Typed
  `Mirror` payload — deferred until second component handover
  surfaces the need."
- `sema-upgrade/ARCHITECTURE.md:186-193` — "Mirror payload
  application on the production private upgrade socket."

Per spirit 274 (Maximum certainty Decision):
**Mirror payload is raw bytes in its own container.** The
typed-enum alternative is rejected on the import-cost grounds.

Two distinct things are entangled in the Possible-features text:

1. **The wire-shape question** — typed enum vs raw bytes. This is
   *settled* (raw bytes). The Possible-features entries in
   `version-projection/ARCHITECTURE.md` and
   `signal-version-handover/ARCHITECTURE.md` should retire to a
   one-sentence Constraint pointing at spirit 274 + the
   `signal-version-handover` raw-bytes section (currently at
   `signal-version-handover/ARCHITECTURE.md:107-160`).
2. **The production mirror application question**
   (`sema-upgrade/ARCHITECTURE.md:186-193`) — "where the divergence
   sink lives in the prototype before persona-introspect ships."
   This is *unsettled* and is properly a Possible-features entry.
   Independent of (1).

**Cleanup characterisation**: the wire-shape Possible-features
retirement (item 1) is a **1-PR cleanup** —
two short edits, both in ARCH files only, neither touching code or
tests. It belongs in the macro-convergence epic's documentation
slice ONLY if the macro epic is touching these ARCH files anyway;
otherwise it's a standalone P3 polish bead. Recommendation: lift
to a single P3 bead and resolve before the convergence epic, so the
epic doesn't have to thread through stale ARCH text. The mirror-
application question (item 2) stays out of macro convergence — it's
production-runtime work, not contract-macro work.

## §6 Summary

- **Wire vocabulary**: fully landed and round-tripped in tests for
  both ordinary and owner contracts.
- **Daemon protocol participation**: persona-spirit accepts the
  full upgrade-socket protocol with a real state machine and
  public-socket lifecycle transitions. Mirror handling is partial
  — decodes as receiver's own type, no projection, no raw-bytes
  side container.
- **Orchestrator**: persona has the `HandoverDriver`, the four
  manager messages, the four owner-op dispatchers, the quarantine
  gate, and the active-version event-log model. Code lands; deploy
  readiness is the gate.
- **Sandbox witness**: `spirit-smart-handover-sandbox` flake app
  drives the full sequence end-to-end through two tagged daemon
  builds plus two temporary bins. This is the proven 217/218-record
  migration referenced in the orchestrator's prior context.
- **Single largest in-code gap**: no `VersionProjection<v0_1_0::X,
  v0_1_1::X>` impl exists in any production crate — only as test
  fixtures and as a non-`VersionProjection` `From` impl inside the
  sema-upgrade migration module. The trait is loaded but not bound
  in production. For the first Spirit cutover this is workable
  (stop-old / start-new) but it is the gap that blocks
  zero-downtime live-mirror cutovers.
- **Pilot-blocking deploy gates**: Persona deploy + Spirit v0.1.0
  retrofit (named explicitly in `sema-upgrade/ARCHITECTURE.md`
  Possible-features and in `/315` §6).
- **Mirror-payload Possible-features text** is stale across three
  ARCH files; a single-sentence retirement in two of the three is
  a 1-PR cleanup separate from the macro convergence epic.

## §7 End-to-end live path trace

The Spirit pilot's proven path runs through Nix sandbox apps, not
through Persona-against-real-daemons (because v0.1.0 has no upgrade
socket and Persona deploys is the open `primary-a5hu` work).

The `spirit-smart-handover-sandbox` flake app
(`sema-upgrade/flake.nix:298-474`) is the live witness:

1. Start tagged `v0.1.0` daemon against a copy of the source redb
   (`flake.nix:344-359`). Old daemon has ordinary + owner sockets
   only — no upgrade socket exists in the v0.1.0 build.
2. Verify v0.1.0 reads work (`flake.nix:379-386`).
3. Write one record through v0.1.0 (`flake.nix:388-395`).
4. Confirm v0.1.0 cannot accept `Magnitude::High`
   (`flake.nix:397-401`) — proves the schema widening matters.
5. Snapshot copy the v0.1.0 redb (`flake.nix:403`).
6. Run `sema-upgrade-temporary` migration
   (`flake.nix:405-407`) — invokes the migration module's
   `migrate_paths` (`sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:34-51`),
   which reads historical records via the `historical` schema
   (`:64-79`) and writes them through `current_shape::from(record)`
   into the target (`:81-100`) using
   `From<historical::StoredRecord> for current_shape::StoredRecord`
   (`:259-266`) which chains through `From<historical::Certainty>
   for Magnitude` (`:303-311`).
7. Start tagged current `v0.1.1` daemon on the migrated redb
   (`flake.nix:409-430`). New daemon has all three sockets
   (`persona-spirit/src/daemon.rs:580-651` bind path).
8. Verify the migrated record survives migration
   (`flake.nix:432-434`).
9. Run `sema-upgrade-handover-temporary` (`flake.nix:436-443`),
   which invokes `PrototypeHandover::for_spirit_0_1_0_to_0_1_1()`
   (`sema-upgrade/src/handover.rs:139-145`) then
   `run_atomic_handover` (`:163-199`). The state machine is
   in-process — it does NOT cross a socket; the sandbox proves the
   protocol semantics with both endpoints in one Rust process. The
   prototype walks
   `AskHandoverMarker → ReadyToHandover → HandoverCompleted` via
   `handle_current_operation` on a single `PrototypeEndpoint`
   (`:49-119`).
10. Write a `Magnitude::High` record through the next daemon
    (`flake.nix:445-452`) — only possible after the cutover
    because v0.1.0 can't represent `High`.
11. Verify v0.1.0's database did NOT receive the post-cutover write
    (`flake.nix:459-463`) — proves cross-daemon write isolation.

The corresponding **production** path (not yet shippable):

1. Operator: `persona '(AttemptHandover (persona-spirit
   ((v0.1.0 <hash-0>) /run/persona/.../v0.1.0/owner.sock
   /run/persona/.../v0.1.0/upgrade.sock) ((v0.1.1 <hash-1>)
   /run/persona/.../v0.1.1/owner.sock
   /run/persona/.../v0.1.1/upgrade.sock)))'.
2. Persona owner socket receives this, decodes as
   `owner_signal_version_handover::Operation::AttemptHandover`,
   dispatches into
   `EngineManager::handle_owner_version_handover`
   (`persona/src/manager.rs:345-401`).
3. `Target::from_owner_attempt` builds the four-socket value
   (`persona/src/upgrade.rs:73-83`).
4. `drive_version_handover` (`persona/src/manager.rs:290-300`):
   ensure not quarantined → `prepare_upgrade` (appends
   `UpgradePrepared` event) → `start_next_component_unit` (starts
   the v0.1.1 unit via systemd) → `HandoverDriver::drive_current_side`.
5. `HandoverDriver::drive_current_side`
   (`persona/src/upgrade.rs:434-477`) dials BOTH upgrade sockets in
   sequence. **Step that blocks the production pilot**: the next
   daemon's marker (`commit_sequence == 0` on a fresh start) will
   never match the current daemon's marker. The sandbox solves this
   by running `sema-upgrade-temporary` BEFORE starting next
   (`sema-upgrade/flake.nix:403-407`). The production analogue must
   do the same — i.e., the manager's `start_next_component_unit`
   path must either (a) take a pre-migrated database, or (b) the
   `AttemptHandover` operation must include a database-staging
   prerequisite. Today neither is wired.
6. Assuming markers match: `current.ready_to_handover` →
   `current.complete_handover`.
7. `current` (persona-spirit v0.1.0 daemon)
   `submit_upgrade_request(ReadyToHandover)` flips
   `HandoverState::Active` → `HandoverState::HandoverMode{accepted_marker}`
   (`persona-spirit/src/actors/root.rs:251-258`), which in turn
   triggers `public_sockets.enter_handover_mode()` at
   `persona-spirit/src/daemon.rs:1410-1412` — public reads pass,
   writes refuse.
8. `current` `submit_upgrade_request(HandoverCompleted)` flips
   `HandoverState::HandoverMode` → `HandoverState::PrivateUpgradeOnly`
   (`persona-spirit/src/actors/root.rs:301-307`); triggers
   `public_sockets.close()` at `persona-spirit/src/daemon.rs:1413-1415`
   — both ordinary and owner sockets refuse all traffic.
9. `EngineManager::complete_upgrade` (`persona/src/manager.rs:271-288`)
   appends `ActiveVersionChanged` to the event log.
10. Owner socket reply: `Reply::HandoverSucceeded(HandoverSucceeded
    { component, active_version, commit_sequence })`
    (`persona/src/manager.rs:353-357`).

The **gap between sandbox and production** is the bracketed
"and the cross-daemon protocol runs across an actual private upgrade
socket": the sandbox witness runs `PrototypeHandover` in-process; the
production path runs `HandoverClient` over Unix sockets to the
component's upgrade socket. The wire protocol is the same six
operations; the integration tests at
`persona-spirit/tests/daemon.rs:626-734` prove the daemon side of the
socketed protocol works; the missing piece is the deployed v0.1.0
daemon owning the upgrade socket (the retrofit named in
`sema-upgrade/ARCHITECTURE.md:194-199`).

## See also

- `0-frame-and-method.md` — orchestrator frame for the 317 dispatch.
- `reports/designer/315-design-sema-upgrade-and-handover-current-state.md`
  — current-state design, this audit's direct upstream.
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`
  — canonical spec.
- `reports/designer/287-version-handover-component-explained.md`
  — canonical visual reference.
- `version-projection/ARCHITECTURE.md` — peer library contract.
- `signal-version-handover/ARCHITECTURE.md` — wire contract +
  raw-bytes Mirror discipline.
- `owner-signal-version-handover/ARCHITECTURE.md` — owner contract
  (lands, 42-line ARCH terse).
- `sema-engine/ARCHITECTURE.md` — `CommitSequence` durable
  high-water mark home (referenced by /315 §4).
- `sema-upgrade/ARCHITECTURE.md` — protocol witness + Nix sandbox
  host.
- `persona-spirit/ARCHITECTURE.md` — daemon state machine + private
  upgrade socket addition.
- `persona/ARCHITECTURE.md` §1.6.7 — Persona-as-orchestrator
  documentation.
