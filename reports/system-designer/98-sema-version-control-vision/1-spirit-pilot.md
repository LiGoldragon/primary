# 98/1 — Spirit, the pilot component — persistence path, guardian, generated/hand split, migration, VC seam

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
An independent adversarial verifier re-checked every key claim against the code; its verdicts are appended at the end of this file.*

# Spirit Component: Persistence, Guardian, Code Generation, and Versioning Architecture

## 1. PERSISTENCE PATH: Exact Write Path from Record Operation to Disk

Spirit persists records through a strict three-plane flow: Signal admission → Nexus decision → SEMA write. The exact write path for a `Record` operation is:

**CLI edge to wire framing:**
- `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs:35-44`: CLI reads NOTA input text, parses into generated `Input` type via `text.parse::<Input>()`, frames as binary rkyv over Unix socket

**Socket to daemon admission:**
- `/git/github.com/LiGoldragon/spirit/src/engine.rs:333-348`: `SignalAdmission::admit()` validates the decoded `Input`, mints `origin_route` and `message_identifier`, returns `SignalAccepted` only if validation passes

**Nexus decision:**
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119`: `Nexus::decide_signal_arrival()` matches `Input::Record(record)` and emits `NexusAction::command_effect(NexusEffectCommand::record_with_implied_referents(...))`
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:564-569`: Effect handler calls `apply_record_with_implied_referents()`, which registers implied referents first, then emits `NexusEffectResult::record_referents_settled()`

**Guardian gating (conditional on `agent-guardian` feature):**
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:615-626` (agent-guardian enabled): `guard_record()` creates `GuardianOperation::record(request)`, calls `guard_model(operation)` which invokes the agent guardian Unix socket, returns `Err(rejection)` on guardian rejection or `Ok(Ok(receipt))` on acceptance
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:607-613` (agent-guardian disabled): `guard_record()` directly calls `self.store.record_entry(request.entry)`

**SEMA write operation:**
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:982-989`: Loop in `execute_to_reply()` converts `NexusAction::CommandSemaWrite(command)` to `SemaWriteInput` via `into_sema_write_input()`, calls `apply_sema_write_operation()` which invokes `Store::apply_inner()`
- `/git/github.com/LiGoldragon/spirit/src/store.rs:124-193`: `SemaEngine::apply_inner()` matches `SemaWriteInput::Record(record)`, calls `self.record(record.into_payload())`

**Disk persistence through sema-engine:**
- `/git/github.com/LiGoldragon/spirit/src/store.rs:481-490`: `Store::record()` creates `StoredRecord { record_identifier: String, entry: Entry }`, mints unused base36 short key via `RecordIdentifierMint`, calls `database.assert_record(keyed_assertion)` where `database` is `SemaDatabase` (sema-engine handle)
- `/git/github.com/LiGoldragon/spirit/src/store.rs:244-259`: `Store::open(path)` calls `SemaDatabase::open(EngineOpen::new(path.clone(), SPIRIT_SCHEMA_VERSION))` at `/path/to/*.sema` file, registers two tables: `ENTRIES_TABLE` named "records" and `REFERENTS_TABLE` named "referents"

**Disk files at runtime:**
- Main database: `/path/to/spirit.sema` (opened at launch via `Store::open(path)`, registered with sema-engine schema version 8)
- Archive database: `/path/to/spirit.archive.sema` (opened on-demand by `Store::collect_removal_candidates()` at owner-configured target)
- Guardian journal: `/path/to/spirit.guardian.sema` (opened on-demand by `guardian_journal.rs` to log guardian decisions, only with `agent-guardian` feature)

**Crate boundaries crossed:**
1. CLI `spirit` binary (nota-text feature enabled)
2. `spirit` daemon library: `SignalAdmission::admit()` 
3. `spirit` library: `Nexus` decision plane
4. `sema_engine` crate: `SemaDatabase::open()`, keyed record assertions/mutations/retractions
5. Filesystem: rkyv-serialized bytes to `*.sema` file

**Key type on write path:**
- `Entry { Domains * Kind * Description * Certainty * Importance * Privacy * Referents * }` (defined in `/git/github.com/LiGoldragon/spirit/schema/signal.schema:205`)
- `StoredRecord { record_identifier: String, entry: Entry }` (defined in `/git/github.com/LiGoldragon/spirit/src/store.rs:73-77`)

## 2. GUARDIAN MECHANISM: Implementation, Verdict Types, Operation Gates

**Location of guardian mechanism:**
- Agent guardian implementation: `/git/github.com/LiGoldragon/spirit/src/guardian.rs` (432 lines)
- Guardian journal (decision logging): `/git/github.com/LiGoldragon/spirit/src/guardian_journal.rs` (248 lines)
- Guardian prompt building (model interaction): `/git/github.com/LiGoldragon/spirit/src/guardian_prompt.rs` (537 lines)
- Nexus integration (effect command dispatch): `/git/github.com/LiGoldragon/spirit/src/nexus.rs:456-522`

**What it gates (which operations):**
All write-side mutations when `agent-guardian` feature is active (compile-time selection):
- `Record`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:615-626`
- `Propose`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:636-650`
- `Clarify`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:660-670`
- `Supersede`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:680-690`
- `Retire`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:741-749`
- `Remove`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:708-718`
- `ChangeRecord`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:728-738`
- `RegisterReferent`: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:759-769`

Read operations (`Observe`, `Lookup`, `Count`, `PublicRecords`, `PrivateRecords`) are NOT gated.

**Verdict types:**
- `GuardianVerdict = Accept | (Reject { GuardianRejectionReason * Explanation * })` (defined in `/git/github.com/LiGoldragon/spirit/schema/nexus.schema:112-113`)
- `ReferentGuardianVerdict = Accept | (RejectReferent { ReferentGuardianRejectionReason * Explanation * })` (defined in `/git/github.com/LiGoldragon/spirit/schema/nexus.schema:114-115`)
- Rejection reasons are generated from schema: `GuardianRejectionReason` lists 19 variants (Duplicate, Contradiction, Compound, NonIntent, UnclearPrivacy, UnclearDomain, etc.) defined in `/git/github.com/LiGoldragon/spirit/schema/signal.schema:223`

**Guardian gating path (all writes):**
- `/git/github.com/LiGoldragon/spirit/src/nexus.rs:456-522`: Effect dispatch for `GuardRecord`, `GuardRemove`, `GuardReferentRegistration`, and record-with-implied-referents operations
- These call `guard_record()`, `guard_remove()`, etc. which check `#[cfg(feature = "agent-guardian")]` at compile time
- With feature enabled: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:616-625`: creates `GuardianOperation`, calls `self.guard_model(operation)` (defined at 800+), which calls `self.guardian.as_ref().unwrap().guard()` 
- `/git/github.com/LiGoldragon/spirit/src/guardian.rs:119-147`: `AgentGuardian::guard()` function signature takes `&GuardianOperation`, returns `AgentGuardianDecision` containing `GuardianVerdict`

**Function signature for admission:**
```rust
fn guard(
    &self,
    operation: &GuardianOperation,
    records: RecordSet,
    database_marker: DatabaseMarker,
) -> AgentGuardianDecision
```
Location: `/git/github.com/LiGoldragon/spirit/src/guardian.rs:119`

**Reuse as admission policy for rebase/merge:**
The guardian is **feature-isolated** to `agent-guardian` compile-time flag. A rebase/merge path would:
1. Define new operation types in `/git/github.com/LiGoldragon/spirit/schema/nexus.schema` (e.g., `RebaseOperation`, `MergeOperation`)
2. Emit new `NexusEffectCommand` variants
3. Add `GuardRebase` / `GuardMerge` effect handlers in `apply_effect_operation()` (line 456+)
4. Call the same `guardian.guard()` method with the rebased/merged records
5. Return `GuardianRejected` or `GuardianAccepted` as part of `NexusEffectResult`

The exact entry point is the `guard()` method, which takes `&GuardianOperation` (a schema-visible enum that could be extended with rebase/merge variants).

## 3. GENERATED VS HAND-WRITTEN CODE

**Line counts by category:**

Generated code (all in `/git/github.com/LiGoldragon/spirit/src/schema/`)
- `domain.rs`: 3,801 lines (domain enum definitions)
- `signal.rs`: 5,398 lines (Input, Output, Entry, Query, etc.)
- `nexus.rs`: 2,577 lines (NexusWork, NexusAction, effects)
- `sema.rs`: 1,322 lines (WriteInput/WriteOutput, ReadInput/ReadOutput)
- `meta_signal.rs`: 706 lines (wire contract only)
- `daemon.rs`: 670 lines (async runtime glue)
- **Total generated: 14,474 lines**

Hand-written code (core logic):
- `nexus.rs`: 1,354 lines (decision logic, effect dispatch, guardian integration)
- `store.rs`: 1,604 lines (SEMA persistence, query predicates, archive database)
- `engine.rs`: 1,458 lines (Signal admission, Nexus composition, meta-socket handling)
- `production_migration.rs`: 1,638 lines (schema version upgrades)
- `guardian.rs`: 432 lines (agent-guardian Unix socket integration)
- `guardian_prompt.rs`: 537 lines (prompt building for agent)
- `guardian_journal.rs`: 248 lines (decision logging)
- Other (config, daemon, transport, trace): ~850 lines
- **Total hand-written: ~8,121 lines**

**Ratio: 64% generated, 36% hand-written**

**Schema-generated traits implemented:**
- `SemaEngine for Store` (apply_inner, observe_inner): `/git/github.com/LiGoldragon/spirit/src/store.rs:105-236`
- `NexusEngine for Nexus` (on_start, on_stop, decide): `/git/github.com/LiGoldragon/spirit/src/nexus.rs:1041-1070`
- `SignalEngine for SignalAdmission` (admit, triage, reply): `/git/github.com/LiGoldragon/spirit/src/engine.rs:310-415`
- Effects are dispatched via generated `NexusEffectCommand` enum; `apply_effect_operation()` (line 456+) implements the effect dispatch using pattern matching on generated variants

**Trait visibility:**
Per INTENT.md line 117-122, generated plane modules are public through `spirit::schema::{signal,nexus,sema}` but not flattened into crate root. External types import `spirit::schema::signal::Input` not `spirit::Input`.

## 4. OPERATION FLOW: End-to-End Record Operation Trace

Exact flow for `Input::Record(RecordRequest)`:

1. **CLI text edge** → `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs:34-44`
   - Reads NOTA text `(Record { ... })`
   - Calls `text.parse::<Input>()` → generated `FromStr` impl on `Input` enum
   - Frames to binary rkyv via `Input::encode_signal_frame()` (generated)

2. **Unix socket → daemon** → `/git/github.com/LiGoldragon/spirit/src/transport.rs`
   - `SignalTransport::exchange(&input)` sends length-prefixed frame
   - Daemon reads via `GeneratedDaemonRuntime` listener (generated in `src/schema/daemon.rs`)

3. **Signal admission** → `/git/github.com/LiGoldragon/spirit/src/engine.rs:158-172`
   - `Engine::handle_async(input)` calls `self.signal_admission.admit(input)`
   - Mints `origin_route` (line 334), `message_identifier` (line 336)
   - Validates via `signal_input.root().validate()` (generated method, line 337)
   - Returns `SignalAccepted { sent: MessageSent, input: Signal<Input> }`

4. **Nexus triage** → `/git/github.com/LiGoldragon/spirit/src/engine.rs:158-171`
   - Calls `SignalEngine::triage(accepted)` which asks generated Nexus composer for `nexus::Nexus<nexus::Work>`
   - This is generated; outputs `NexusWork::SignalArrived(Input)`

5. **Nexus decision loop** → `/git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119`
   - `decide_signal_arrival(Input::Record(record))` emits `NexusAction::command_effect(NexusEffectCommand::record_with_implied_referents(...))`

6. **Effect dispatch** → `/git/github.com/LiGoldragon/spirit/src/nexus.rs:456-475`
   - Case `NexusEffectCommand::RecordWithImpliedReferents(request)` calls `apply_record_with_implied_referents(request)`
   - Registers implied referents (line 565), then returns `NexusEffectResult::record_referents_settled(request)`

7. **Guardian gate** → `/git/github.com/LiGoldragon/spirit/src/nexus.rs:616-625` (if agent-guardian feature)
   - Next loop iteration: `NexusWork::effect_completed(NexusEffectResult::record_referents_settled(...))`
   - `decide_effect_completion()` examines the settled referents result
   - Calls `guard_record(request)` which creates `GuardianOperation`, calls agent socket, gets verdict
   - On acceptance, falls through to return `NexusEffectResult::recorded(receipt)`
   - On rejection, returns `NexusEffectResult::guardian_rejected(rejection)`

8. **SEMA write** → `/git/github.com/LiGoldragon/spirit/src/nexus.rs:982-989`
   - `NexusAction::CommandSemaWrite(CommandSemaWrite::Record(...))` emitted
   - Calls `self.apply_sema_write_operation(input)` which delegates to `Store::apply_inner()`
   - `/git/github.com/LiGoldragon/spirit/src/store.rs:124-134` matches `SemaWriteInput::Record`, calls `self.record(entry)`
   - Inserts into sema-engine via `database.assert_record(Assertion::new(key, StoredRecord))`
   - Returns `SemaWriteOutput::recorded(SemaReceipt { record_identifier, database_marker })`

9. **Persistence to disk** → sema-engine internal
   - `SemaDatabase` (sema-engine handle) commits to `*.sema` file
   - `CommitSequence` counter incremented (durable across restarts)
   - `StateDigest` recomputed as blake3 hash of all records + commit sequence

10. **Reply** → `/git/github.com/LiGoldragon/spirit/src/engine.rs:171-172`
    - `SignalEngine::reply(nexus_action)` converts `NexusAction::ReplyToSignal(Output::RecordAccepted(...))` to `Signal<Output>`
    - Frames as binary rkyv via `Output::encode_signal_frame()` (generated)

11. **CLI output** → `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs:44-45`
    - `transport.read_subscription_event()` or direct reply decodes `Output`
    - Calls `Output::Display` impl (generated), prints NOTA text

**Crate boundaries crossed:**
1. `spirit` CLI crate → 2. `spirit` daemon library (Signal plane) → 3. `spirit` library (Nexus plane) → 4. `spirit` library (SEMA plane via Store) → 5. `sema_engine` crate (database write) → 6. `spirit` CLI (reply output)

**Triad separation validation:**
- ALL storage: `Store` in `spirit` daemon crate, backed by `sema-engine`, persists to `*.sema`
- ALL decisions: `Nexus` and `SignalAdmission` in `spirit` daemon crate, consume generated `NexusWork`/`NexusAction`
- ALL comms: Signal plane (`Input`/`Output`) in `spirit` daemon crate, rkyv binary frames via Unix sockets

## 5. CLI SPLIT: Ordinary and Meta CLI

**Ordinary CLI:**
- Binary: `spirit` (`/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs`)
- Features: Requires `nota-text` (enables NOTA parsing)
- Socket: `$SPIRIT_SOCKET` env var (default `/tmp/spirit.sock`)
- Operations: All working-signal operations (Record, Observe, etc.)

**Meta CLI:**
- Binary: `meta-spirit` (`/git/github.com/LiGoldragon/spirit/src/bin/meta-spirit.rs`)
- Features: Requires `nota-text`
- Socket: `$META_SPIRIT_SOCKET` env var
- Operations: Owner-only (Configure, Import)

**Configuration arrival:**
- Source: Binary rkyv `signal_spirit::SpiritDaemonConfiguration` file
- Decode: `/git/github.com/LiGoldragon/spirit/src/daemon.rs:1-287` (generated daemon runtime glue)
- Path: Single command-line argument to `spirit-daemon` (no NOTA parsing in daemon startup)
- Helper tool: `spirit-write-configuration` (`/git/github.com/LiGoldragon/spirit/src/bin/spirit-write-configuration.rs`) accepts NOTA `ConfigurationWriteRequest`, writes binary config file
- Per INTENT.md line 143: "The daemon's single argument is a path to a binary rkyv `SpiritDaemonConfiguration` object from the `signal-spirit` contract."

**Meta socket gating:**
- File mode: `0o600` (owner read/write only), set via `SocketModeBits::new(OWNER_ONLY_SOCKET_MODE)` in `/git/github.com/LiGoldragon/spirit/build.rs:11` and `build.rs:60`
- Listener tier: `MetaListenerTier` separates meta from working (line 60-61 in build.rs)
- Admission: `triad_runtime::AsyncMultiListenerDaemon` tags connections with `ListenerTier::Meta`, routes to meta schema decoder

## 6. MIGRATION/SCHEMA-CHANGE PATH: Historical and Current Shape

**Migration module location:**
- `/git/github.com/LiGoldragon/spirit/src/production_migration.rs` (1,638 lines)
- Defines historical database shapes: `ProductionDatabase`, `SpiritStoreV1Database` through `SpiritStoreV7Database`
- Implements upgrade path through versions 1→2, 2→3, 3→4, 4→5, 5→6, 6→7, 7→8

**How schema changes are applied:**
- Upgrade entry: `SpiritStoreUpgrade::run()` (starts at line ~1500 in production_migration.rs)
- Opens source database at historical schema version, enumerates records, transforms per version rules
- Example: v4→v5 adds `Importance` field with `Magnitude::Minimum` default
- Writes transformed records to new database at schema version 8
- Returns `SpiritStoreUpgradeOutput::Upgraded(SpiritStoreUpgradeCompleted { record_count })`

**Database rewrite mechanism:**
- Opening: Calls `SemaDatabase::open(EngineOpen::new(path, SPIRIT_STORE_CURRENT_SCHEMA_VERSION))` at target path
- Iteration: Reads ALL records from old database via `database.records()`
- Transformation: Manually reconstructs each `StoredRecord` with new schema fields
- Assertion: Calls `new_database.assert_record(Assertion::new(key, transformed_record))`
- No wholesale `fs::rename` — records are individually persisted through sema-engine
- Durability: sema-engine commits to `.sema` file; if process crashes mid-upgrade, the incomplete target is corrupt and must be restarted

**Current schema version:**
- Version 8 defined in `/git/github.com/LiGoldragon/spirit/src/store.rs:46` as `SPIRIT_SCHEMA_VERSION = SchemaVersion::new(8)`

**Schema-authored migration types:**
- `ProductionMigrationRequest { source_database_path, target_database_path }` (defined in production_migration.rs:33-36, not in schema)
- `SpiritStoreUpgradeRequest { database_path }` (line 49-51)
- Both accept NOTA input but are hand-written not generated (no `.schema` source)

**Binary CLI tools:**
- `spirit-migrate-production`: Requires `production-migration` feature, migrates old production schema to Spirit schema v1
- `spirit-upgrade-store`: Requires `production-migration` feature, upgrades an existing Spirit store to current schema version

## 7. VC SEAM: Narrowest Point to Introduce Versioned Operation Log

**Current state:**
- Mail ledger is **in-memory only** (line 669 in ARCHITECTURE.md: "The mail ledger is still in-memory")
- `MailLedgerEvent` entries record Signal sent/processed markers, not durable operations
- Operation log in `ObserverTapTable` (line 82 in nexus.rs) is also in-memory: `operation_log: Vec<OperationKind>`
- SEMA store tracks `CommitSequence` (durable) and `StateDigest` (durable hash), but no operation log

**Narrowest seam to add versioned operation log:**
Location: `/git/github.com/LiGoldragon/spirit/src/store.rs:63-71` (Store struct definition) and `/git/github.com/LiGoldragon/spirit/src/store.rs:244-259` (Store::open)

1. **Add operation log table to Store** (no engine changes needed):
   - Register third table in `Store::open()` via `database.register_table(TableDescriptor::new(OPERATIONS_TABLE))`
   - Define `struct LoggedOperation { sequence: u64, operation_kind: String, timestamp: u64, input_digest: String }`

2. **Append to log at every write**:
   - In `Store::apply_inner()` (line 124), after every `SemaWriteInput` variant (Record, Remove, etc.), append `LoggedOperation` via `database.assert_record(Assertion::new(log_key, logged_op))`
   - CommitSequence is already incremented by sema-engine, use it as sequence number

3. **Implement log rebuild query**:
   - Add `Store::read_operation_log()` method to query the operations table via `database.query_plan(QueryPlan::prefix(OPERATIONS_TABLE))`
   - Rebuild state view from log if needed (future work)

4. **Changes required in spirit itself**:
   - `Store` struct: Add `operations: TableReference<LoggedOperation>`
   - `Store::open()`: Register operations table, no changes to open path parameters or error handling
   - `Store::apply_inner()`: Append one log entry per SemaWriteInput (6 variants), no changes to SEMA write semantics
   - New method: `Store::read_operation_log()` returns `Result<Vec<LoggedOperation>>`

5. **No changes required in engine/Nexus**:
   - `NexusEngine::execute()` loop already goes through `Store::apply()` → no new barriers
   - Guardian remains a gate *before* the effect dispatch, not within SEMA
   - Rebase/merge would be new effect commands, consuming the log but not changing its append path

**Why this is the narrowest seam:**
- sema-engine already manages multi-table transactions atomically
- `CommitSequence` counter is already durable and monotonic, no additional sequencing logic needed
- No Signal/Nexus/SEMA plane boundary changes
- Log is *append-only* table, no mutations to existing records
- Future rebase/merge path reads from log (SELECT) not through guardian (which gates writes)

**Migration path for existing data:**
- New Spirit databases start with empty operations table (no old log to reconstruct)
- Upgraded databases from v8: operations table empty initially (no retroactive log)
- Future schema v9 upgrade could backfill operation log from audit trail if one is added, but that's separate

**Compatibility with guardian:**
- Guardian gates decisions *before* SEMA write
- Operation log records what *was written*, not what was rejected
- Guardian rejections are not logged to the operations table (they never reach SEMA)
- This preserves the guardian as an admission policy, not an operation filter



## keyClaims
- CLAIM: Spirit persists via Store::record() → SemaDatabase::assert_record() → rkyv-serialized StoredRecord { record_identifier: String, entry: Entry } to named table 'records' in *.sema file opened at Store::open(path)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:481-490,124-134,244-259,47-48
- CLAIM: Record operation crosses Signal → Nexus → SEMA crate boundaries: SignalAdmission::admit() mints origin_route, Nexus::decide_signal_arrival() routes to NexusEffectCommand, Store::apply_inner() writes to sema-engine
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/engine.rs:333-348, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119, /git/github.com/LiGoldragon/spirit/src/store.rs:124-134
- CLAIM: Guardian is feature-gated at compile time (agent-guardian) and gates write operations via Nexus effect dispatch NexusEffectCommand::GuardRecord/GuardRemove/GuardChangeRecord/GuardReferentRegistration, calling AgentGuardian::guard() which returns GuardianVerdict (Accept | Reject {GuardianRejectionReason, Explanation})
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/nexus.rs:456-522, /git/github.com/LiGoldragon/spirit/src/guardian.rs:119-147, /git/github.com/LiGoldragon/spirit/schema/nexus.schema:112-115
- CLAIM: 14,474 lines generated from schema/{signal,nexus,sema,domain,meta-signal}.schema via schema-rust-next in build.rs, producing src/schema/{signal,nexus,sema,domain,meta_signal,daemon}.rs carrying Input/Output/NexusWork/NexusAction/SemaWriteInput enums
  EVIDENCE: /git/github.com/LiGoldragon/spirit/build.rs:28-52, /git/github.com/LiGoldragon/spirit/src/schema/ file listing, /git/github.com/LiGoldragon/spirit/src/schema/signal.rs:1
- CLAIM: Schema-generated traits: SemaEngine for Store, NexusEngine for Nexus, SignalEngine for SignalAdmission; hand-written implement one decision step and effect/write/read hooks; generated plane modules public via spirit::schema::{signal,nexus,sema}, not flattened into crate root
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:105, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1041, /git/github.com/LiGoldragon/spirit/src/engine.rs:56-61, /git/github.com/LiGoldragon/spirit/INTENT.md:117-122
- CLAIM: Configuration delivered as binary rkyv signal_spirit::SpiritDaemonConfiguration file (single CLI argument to spirit-daemon), decoded in daemon startup, NOT parsed as NOTA; spirit-write-configuration CLI tool accepts NOTA ConfigurationWriteRequest and writes binary file for deploy tooling
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/daemon.rs:1, /git/github.com/LiGoldragon/spirit/INTENT.md:143, /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:149-169
- CLAIM: Meta socket separate from working socket with file mode 0o600 (owner only), managed via MetaListenerTier in generated daemon runtime, routes meta Input to meta_signal.schema contract, carries Configure (sets archive target) and Import (bypasses guardian restore path)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/build.rs:11,60-61, /git/github.com/LiGoldragon/spirit/src/engine.rs:215-257, /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:171-223
- CLAIM: Schema change path implemented via production_migration.rs (1,638 lines) defining historical shapes ProductionDatabase, SpiritStoreV1-V7Database, transforming records version-by-version, opening new database at schema v8, appending transformed records via sema-engine without fs::rename
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/production_migration.rs:1-100, /git/github.com/LiGoldragon/spirit/src/store.rs:46
- CLAIM: Mail ledger is in-memory Vec<MailLedgerEvent> (stated known limit), operation log in ObserverTapTable is in-memory Vec<OperationKind>; narrowest seam to add versioned operation log is register new table in Store::open(), append LoggedOperation on every SemaWriteInput variant, no Nexus/engine changes needed
  EVIDENCE: /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:669, /git/github.com/LiGoldragon/spirit/src/nexus.rs:82,89, /git/github.com/LiGoldragon/spirit/src/store.rs:244-259,63-71
- CLAIM: Guardian bypassed only on meta-socket Import operation (owner privilege), which directly calls Store::import_record() skipping guard_* methods; all working-socket writes gate through guardian when agent-guardian feature enabled
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/engine.rs:236-257, /git/github.com/LiGoldragon/spirit/INTENT.md:98
- CLAIM: Operation flow: CLI NOTA parse → signal frame → SignalAdmission::admit (origin_route mint) → NexusEngine::triage (Nexus<NexusWork>) → Nexus::decide_signal_arrival (effect command) → apply_effect_operation (guardian gate) → NexusAction::CommandSemaWrite → Store::apply_inner → sema-engine assert_record → *.sema file commit
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/bin/spirit.rs:34-45, /git/github.com/LiGoldragon/spirit/src/engine.rs:333-348,158-172, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119,982-989, /git/github.com/LiGoldragon/spirit/src/store.rs:481-490
- CLAIM: Disk files at runtime: spirit.sema (live database, opened at path, schema v8), spirit.archive.sema (opened on-demand at owner-configured target), spirit.guardian.sema (opened on-demand to log guardian decisions, agent-guardian feature only)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:244-259,310-324,332-339,426-428

## openQuestions
- Will rebase/merge operations follow the same NexusEffectCommand dispatch pattern as GuardRecord/GuardRemove, or require new admission logic before Nexus?
- Should the versioned operation log table use durable commit-scoped keys (like CommitSequence) or global monotonic IDs independent of record identifiers?
- Does the existing production migration path have a forward-upgrade story (v8→v9) or does each new schema version require a separate migration binary?
- Can guardian decisions themselves be logged durably (as audit trail separate from operation log) without blocking write admission, or does guardian rejection need to be invisible to the operation log?


## Adversarial verification verdicts

- [CONFIRMED] Spirit persists via Store::record() → SemaDatabase::assert_record() → rkyv-serialized StoredRecord { record_identifier: String, entry: Entry } to named table 'records' in *.sema file opened at Store::open(path)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:481-485,244-259,73-77,47,124-134
- [CONFIRMED] Record operation crosses Signal → Nexus → SEMA crate boundaries: SignalAdmission::admit() mints origin_route, Nexus::decide_signal_arrival() routes to NexusEffectCommand, Store::apply_inner() writes to sema-engine
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/engine.rs:333-365,385-391, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119,1092-1105, /git/github.com/LiGoldragon/spirit/src/store.rs:124-134,192
- [CONFIRMED] Guardian is feature-gated at compile time (agent-guardian) and gates write operations via Nexus effect dispatch NexusEffectCommand::GuardRecord/GuardRemove/GuardChangeRecord/GuardReferentRegistration, calling AgentGuardian::guard() which returns GuardianVerdict (Accept | Reject {GuardianRejectionReason, Explanation})
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/nexus.rs:456-522,616-627,700-739,752-851, /git/github.com/LiGoldragon/spirit/src/guardian.rs:119-147, /git/github.com/LiGoldragon/spirit/schema/nexus.schema:112-115
- [CONFIRMED] 14,474 lines generated from schema/{signal,nexus,sema,domain,meta-signal}.schema via schema-rust-next in build.rs, producing src/schema/{signal,nexus,sema,domain,meta_signal,daemon}.rs carrying Input/Output/NexusWork/NexusAction/SemaWriteInput enums
  EVIDENCE: /git/github.com/LiGoldragon/spirit/build.rs:28-52, bash wc -l output: 14474 total lines in src/schema/*.rs
- [CONFIRMED] Schema-generated traits: SemaEngine for Store, NexusEngine for Nexus, SignalEngine for SignalAdmission; hand-written implement one decision step and effect/write/read hooks; generated plane modules public via spirit::schema::{signal,nexus,sema}, not flattened into crate root
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:105, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1041, /git/github.com/LiGoldragon/spirit/src/engine.rs:367-399, /git/github.com/LiGoldragon/spirit/INTENT.md:117-122
- [CONFIRMED] Configuration delivered as binary rkyv signal_spirit::SpiritDaemonConfiguration file (single CLI argument to spirit-daemon), decoded in daemon startup, NOT parsed as NOTA; spirit-write-configuration CLI tool accepts NOTA ConfigurationWriteRequest and writes binary file for deploy tooling
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/daemon.rs:99-103, /git/github.com/LiGoldragon/spirit/src/config.rs:97-106, /git/github.com/LiGoldragon/spirit/src/bin/spirit-write-configuration.rs:30-40,114-140
- [CONFIRMED] Meta socket separate from working socket with file mode 0o600 (owner only), managed via MetaListenerTier in generated daemon runtime, routes meta Input to meta_signal.schema contract, carries Configure (sets archive target) and Import (bypasses guardian restore path)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/build.rs:11,60-61, /git/github.com/LiGoldragon/spirit/src/engine.rs:215-257, /git/github.com/LiGoldragon/spirit/src/daemon.rs:149-178, /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:171-223
- [CONFIRMED] Schema change path implemented via production_migration.rs (1,638 lines) defining historical shapes ProductionDatabase, SpiritStoreV1-V7Database, transforming records version-by-version, opening new database at schema v8, appending transformed records via sema-engine without fs::rename
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/production_migration.rs:1-100,84-120, wc -l confirms 1638 lines, no fs::rename usage in migration transform
- [CONFIRMED] Mail ledger is in-memory Vec<MailLedgerEvent> (stated known limit), operation log in ObserverTapTable is in-memory Vec<OperationKind>; narrowest seam to add versioned operation log is register new table in Store::open(), append LoggedOperation on every SemaWriteInput variant, no Nexus/engine changes needed
  EVIDENCE: /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:665, /git/github.com/LiGoldragon/spirit/src/nexus.rs:82-84,88-90,1111-1113, /git/github.com/LiGoldragon/spirit/src/store.rs:244-259,63-71
- [CONFIRMED] Guardian bypassed only on meta-socket Import operation (owner privilege), which directly calls Store::import_record() skipping guard_* methods; all working-socket writes gate through guardian when agent-guardian feature enabled
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/engine.rs:236-257, /git/github.com/LiGoldragon/spirit/src/daemon.rs:149-178 (meta handler), /git/github.com/LiGoldragon/spirit/INTENT.md:98
- [CONFIRMED] Operation flow: CLI NOTA parse → signal frame → SignalAdmission::admit (origin_route mint) → NexusEngine::triage (Nexus<NexusWork>) → Nexus::decide_signal_arrival (effect command) → apply_effect_operation (guardian gate) → NexusAction::CommandSemaWrite → Store::apply_inner → sema-engine assert_record → *.sema file commit
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/bin/spirit.rs:34-45,56-57, /git/github.com/LiGoldragon/spirit/src/engine.rs:158-173,333-365,385-391, /git/github.com/LiGoldragon/spirit/src/nexus.rs:1107-1119,1092-1105,982-1027, /git/github.com/LiGoldragon/spirit/src/store.rs:481-490,124-134
- [CONFIRMED] Disk files at runtime: spirit.sema (live database, opened at path, schema v8), spirit.archive.sema (opened on-demand at owner-configured target), spirit.guardian.sema (opened on-demand to log guardian decisions, agent-guardian feature only)
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/store.rs:46,244-259,310-324,326-339

