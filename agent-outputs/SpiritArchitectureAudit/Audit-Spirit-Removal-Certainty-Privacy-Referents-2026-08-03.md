# Spirit removal audit: certainty, privacy, and referents

Date: 2026-08-03 (Europe/Madrid)

Status: read-only engine/data audit. No source, runtime, service, Beads, or store mutation was performed. Live witnesses used only `Version`, `Marker`, and `Count`; no record, referent, archive, journal, or backup body was read.

## Psyche ruling applied

Certainty, privacy, and referents are to be gone from Spirit. For the persisted migration this means:

- retain each current record's identifier and remaining substance;
- remove certainty and privacy fields, selectors, operations, semantics, and persisted bytes;
- remove record-to-referent edges, canonical referent objects, aliases, the referent family, and all referent-specific operations;
- do not leave compatibility fields, tables, history, or archives inside the migrated database;
- allow an old-format copy only as a private rollback backup outside the active migrated database and service data surface.

This is a destructive schema migration, not a compatibility deprecation.

## Executive finding

The three concepts are fully wired through the current release, not decorative metadata.

```text
ordinary/meta clients
        |
        v
signal-spirit Entry + Query + operations
        |
        v
daemon -> Nexus -> guardian packet -> spirit-judge -> model prompt
        |                    |                         |
        |                    +-> guardian journal <---+
        v
SEMA store
  +-- RecordsFamily: Entry includes Certainty, Privacy, Referents
  +-- ReferentsFamily: canonical referent + aliases
  +-- MigrationsFamily: includes migrated referent count
  +-- versioned log/checkpoints: archived record and referent mutations
  +-- separate records archive: full Entry
```

The conforming end state is structurally smaller:

```text
Entry = Domains + Kind + Description + Importance
Query = domain/text/kind/importance dimensions only

SEMA store
  +-- RecordsFamily: identifier + reduced Entry
  +-- MigrationsFamily: record projection receipt only

No ReferentsFamily
No certainty/privacy/referent wire roots or query selectors
No old-format log/checkpoint/archive/journal in the active Spirit surface
```

There are no physical certainty or privacy secondary indexes to delete. Those dimensions are implemented as full-record scan predicates and sort keys. The referent registry is a real keyed family and must be deleted. “Drop the indexes” therefore means deleting the referent family and removing the certainty/privacy/referent selection, sort, scoring, and canonicalization paths.

## Exact deployed source closure

The live release reports `0.25.1`. Its immutable source closure is recorded in `spirit@eabe6c6d:flake.nix:831-869` and independently locked by `CriomOS-home@d2d02bb6:flake.lock:3356-3381,3405-3507`:

| Component | Revision |
| --- | --- |
| `spirit` | `eabe6c6d96112b46d15443e1c1a29d940605785f` |
| `signal-spirit` | `1cf7c010029de46369b742687da4fa1ca6def9a9` |
| `meta-signal-spirit` | `0a7a2438c8e5d57cb1fd413452d0a7ddad4fb9b3` |
| `signal-spirit-judge` | `7c25b71a34858c0d912dff8fd0b4f4ac213d7cd1` |
| `spirit-judge` | `901d1fe404f277778e32318871b97cdcaff85a43` |
| `spirit-judge-config` | `b6a3fe7e0f91f2e5ff8ddec94ebfe2b489fc355d` |
| `sema-engine` | `b3b5fb714412f820f870c290a6cb7800acb9bdec` |

The current Home Manager module consumes Spirit's maintained service bundle and starts the judge before the daemon (`CriomOS-home@d2d02bb6:modules/home/profiles/min/spirit.nix:50-62,127-220`). The release bundle configures schema v13 migration on every daemon start, a gated judge, and no mirror target (`spirit@eabe6c6d:nix/service-bundle.nix:33-69,78-105`). The production daemon is compiled with `agent-guardian`, not `mirror-shipper` (`spirit@eabe6c6d:flake.nix:766-770`).

## Bounded live witnesses

Both `spirit-daemon.service` and `spirit-judge.service` were active and running. The daemon entered the active state at 2026-08-03 19:04:25 CEST.

The marker before and after every count was identical:

```text
(MarkerReported (974 7784350440604474991))
```

The current live materialized record count is 24.

| Axis | Exact live counts |
| --- | --- |
| Privacy | Zero 24; Minimum 0; VeryLow 0; Low 0; Medium 0; High 0; VeryHigh 0; Maximum 0 |
| Certainty | Zero 0; Minimum 0; VeryLow 0; Low 0; Medium 4; High 20; VeryHigh 0; Maximum 0 |

Observed facts:

- There is no non-zero privacy state among the 24 live records. Every record still physically carries a `Privacy::Zero` field that the migration must omit.
- All 24 records carry certainty above the classifier fallback of `Minimum`: four `Medium`, twenty `High`. These values will be discarded.
- No live record is currently in the certainty-zero removal-candidate state.
- The live referent-object count and record-to-referent edge count remain unknown. Spirit exposes no count-only referent inventory operation and no predicate for “has any referent.” Supplying a referent selector would require learning or guessing names. That was not done.

The earlier `(Current (24 0))` migration result is not evidence of an empty referent family. On an already-current store the migration implementation returns `store.len()` and hardcodes `referent_count: 0` (`spirit@eabe6c6d:src/production_migration.rs:2818-2831`).

Directly opening the live database just to count referents was rejected as an unsafe witness. `sema-engine` has no read-only flag on `EngineOpen`, and a successful open may apply a storage-layout plan after validation (`sema-engine@b3b5fb71:src/engine.rs:100-126,2767-2784,3173-3204`). Its `storage_reader` exists only after that open (`sema-engine@b3b5fb71:src/engine.rs:1256-1275`).

### Live copy surface, metadata only

The Spirit state directory and its files are mode `0755` and `0644` respectively. A bounded name/size/mode inventory found 44 `.sema` or `.sema.*` artifacts plus the configuration archive. No body was opened.

The named surface includes:

- active `spirit.sema` and `spirit.archive.sema`;
- fourteen `spirit.schema-old-backup-*.sema` files;
- six `spirit.archive.schema-old-backup-*.sema` files;
- five stale guardian journals: the unversioned file and v2 through v5;
- sixteen predeploy, preremoval, recovery, or GC backup names, with some categories overlapping the `.sema` set;
- no current `spirit.guardian.v6.sema` file.

These old files are operationally important: current code deliberately leaves incompatible guardian versions untouched (`spirit@eabe6c6d:src/guardian_journal.rs:22-32`; `src/store/mod.rs:600-612`), and current migration deliberately creates old-schema hard links beside the live files (`src/production_migration.rs:19-46,3068-3077,3183-3187`). That is incompatible with the new ruling as a permanent post-migration state. A rollback copy may remain only after being moved outside the active Spirit state surface and made genuinely private. The present `0755` directory plus `0644` files is not such a private rollback boundary.

## Occurrence and wiring classification

### Ordinary contract and generated types: wired

The authored ordinary contract declares `PublicRecords`, `PrivateRecords`, `ChangeCertainty`, and `RegisterReferent` input roots and their result roots (`signal-spirit@1cf7c010:schema/signal.schema:44-45,62-72,79-94`). It declares referent objects and aliases, Entry and query fields, selection axes, removal archives, operation-kind observations, guardian reasons, and the eight-rung magnitude (`schema/signal.schema:105-108,139-167,185-210,212-233,253-263`).

Generated Rust archives the exact fields in `Entry`, `CertaintyChange`, and `Query`, and the input/output enums expose the operations (`signal-spirit@1cf7c010:src/schema/signal.rs:1690-1728,2027-2036,2109-2169`). Because these types own NOTA and rkyv frames, deleting fields changes both textual arity and binary archive layout.

`SignalReuse { Import Export }` is contract-only: generated structs exist, but neither is an ordinary root and no Spirit runtime route uses them (`signal-spirit@1cf7c010:schema/signal.schema:46-52`; generated-only occurrences at `src/schema/signal.rs:129-159`). It should still be removed if the contract must contain no stale compatibility vocabulary.

### Validation and public semantics: wired

An active Entry is currently invalid unless it has a referent; certainty zero is the exception (`signal-spirit@1cf7c010:src/lib.rs:247-272`). Query referent selections are also validated. This makes referents part of admission validity, not just tagging.

The store implements all three query dimensions as predicates over every materialized Entry and implements referent matching in memory (`spirit@eabe6c6d:src/store/mod.rs:1726-1748,1883-1902,1934-1983`). Observation sorts by certainty then importance; public intent and public text search first filter on privacy/certainty, then sort by certainty; text search also scores referent text (`src/store/mod.rs:858-931,1645-1664,1773-1785`).

Required effect:

- delete `PrivacySelection`, `CertaintySelection`, and `ReferentSelection` from `Query`;
- remove certainty ranking, privacy gating, referent matching, canonicalization, and referent text scoring;
- replace the existing deterministic ordering with a certainty-free ordering;
- remove or redefine `PublicRecords`, `PrivateRecords`, `PublicIntent`, and `PublicTextSearch`. Their current meanings cannot survive unchanged because “public/active” is exactly privacy zero plus certainty at least minimum (`src/store/mod.rs:1773-1776`);
- remove the active-entry “non-empty referents” validation rule.

### Daemon, Nexus, SEMA operations, and CLIs: wired

The daemon stages and routes `ChangeCertainty` and `RegisterReferent` (`spirit@eabe6c6d:src/daemon.rs:189-200,294-303`). Nexus lowers both into SEMA (`src/nexus.rs:285-305,1285-1298`). SEMA writes dispatch to concrete mutation/registration methods (`src/store/mod.rs:205-257`). Certainty changes rewrite the stored Entry (`src/store/mod.rs:1119-1137`); referent registration mutates or asserts keyed canonical rows and aliases (`src/store/mod.rs:750-810`).

The ordinary `spirit` CLI generically parses every generated `Input` and sends it to the live socket (`spirit@eabe6c6d:src/bin/spirit.rs:23-52,71-103`), so both operations are deployed. The owner `meta-spirit` CLI is also deployed and can import identifiers plus complete Entries (`src/bin/meta-spirit.rs:15-37`; `meta-signal-spirit@0a7a2438:schema/meta-signal.schema:9-20,46-52`). Owner import auto-registers every Entry referent before writing the record (`spirit@eabe6c6d:src/store/mod.rs:716-748`).

`spirit-render` is wired and built in the release but is not exposed by the current Home Manager profile. Its request is entirely referent-based and it hardcodes privacy zero plus certainty-at-least-minimum; its generated document publishes those filters and full returned Entries (`spirit@eabe6c6d:src/render.rs:34-59,171-234,257-343`; `flake.nix:794-829`). It must be retired or redesigned around remaining query dimensions.

`CollectRemovalCandidates` is wired owner behavior whose eligibility depends on exact certainty zero and whose archive receipt carries full Entries. With certainty gone, this operation cannot retain its current meaning. Explicit `Retire`/`Supersede` paths already exist and are separate from the certainty sentinel.

### Store schemas and catalog: wired

The authored SEMA schema imports all three concepts. `StoredRecord` owns a complete Entry, `StoredReferent` owns the canonical object and aliases, and `Migration` records a referent count. The catalog has Records, Referents, and Migrations families (`spirit@eabe6c6d:schema/sema.schema:1-18,27-64`). Generated family hashes, descriptors, and decoding include the Referents family (`src/schema/sema.rs:291-341,1138-1263`).

The store opens and registers all three tables and carries a typed referent table handle (`spirit@eabe6c6d:src/store/mod.rs:109-117,335-358`). The family directory materializes referent log rows by generated hash (`src/store/family_directory.rs:12-51`). This is the real physical deletion boundary.

There are no separate certainty/privacy index families. `observe` loads all records and filters them (`src/store/mod.rs:858-875`). The only directly keyed ruled concept is `ReferentsFamily`, keyed by canonical referent text (`src/store/mod.rs:1377-1392`; frozen v13 `src/production_migration/v13.rs:573-595`).

### Versioned log, checkpoints, marker, restore, and mirror: wired with one deployment exception

The live database's authoritative versioned log and checkpoints preserve table rows as archived bodies. Restore imports checkpoint and suffix verbatim and registers the referent family (`spirit@eabe6c6d:src/store/mod.rs:428-547`). Certainty changes and referent mutations therefore remain in historical log entries even after later mutations.

The database marker digest includes archived StoredRecord bytes and every StoredReferent (`src/store/mod.rs:1336-1366`). A conforming destructive migration must change the marker. Old/new marker equality is not a valid acceptance criterion.

Mirror restore code also consumes those verbatim checkpoints/log entries, but the mirror shipper is feature-gated and is not compiled into the deployed daemon (`spirit@eabe6c6d:src/store/mod.rs:122-170,529-537`; `flake.nix:766-770`). The current deployment's mirror path is therefore not wired. Historical or externally retained mirror data was not discoverable from bounded local metadata and remains an explicit unknown.

### Separate archive: wired

The separate archive table uses the same `StoredRecord` type and therefore stores full certainty/privacy/referent-bearing Entries (`spirit@eabe6c6d:src/store/archive.rs:14-59`). Clarify, retire, supersede, and candidate collection archive old Entries before mutation/removal. The default archive is the sibling `spirit.archive.sema`; an owner can configure another path in memory (`src/store/mod.rs:577-597`).

The existing migration only discovers the default sibling. It explicitly says owner-configured non-default archives require a separate request and copies every record verbatim (`spirit@eabe6c6d:src/production_migration.rs:3084-3088,3112-3187`). A new migration must project every known archive and refuse activation when a configured archive cannot be inventoried. The current runtime exposes no read-only “show effective archive target” operation, so a post-start owner reconfiguration is unknown.

### Guardian, judge contract, adapter, and prompts: wired

The Spirit guardian sends complete candidate/context `RecordSet` values to the judge and sends the entire referent registry for referent admission (`spirit@eabe6c6d:src/guardian.rs:137-200`). It derives `JudgmentScope::Private` from any Entry privacy other than zero (`src/guardian.rs:364-402`). It maps `UnclearPrivacy`, `Overstated`, and every referent rejection/result (`src/guardian.rs:500-619,686-750`). Guardian context retrieval expands by both domain and referents (`src/store/mod.rs:1003-1016,1562-1593`).

The `signal-spirit-judge` authored schema labels itself a concept sketch, so that file is conceptual, but its hand-written Rust is the actual wired contract (`signal-spirit-judge@7c25b71a:schema/signal.schema:1-3`; `src/lib.rs:33-57`). Admission packets carry complete operations and records; referent packets carry registration plus all registered referents; privacy is a `Public`/`Private` diagnostic scope (`src/lib.rs:65-162,210-296`).

The adapter serializes complete operations and RecordSets into provider prompts and serializes the complete referent registry for referent judgment (`spirit-judge@901d1fe4:src/lib.rs:180-245,285-383`). Its privacy scope changes diagnostic handling (`src/lib.rs:530-566`). Removing per-record privacy should remove this Spirit-specific scope selection, but must not weaken the adapter's general safe-diagnostic/redaction behavior.

The active prompt pack teaches the seven-field Entry, certainty burden ladder, privacy boundary, referent-vs-domain distinction, `UnclearPrivacy`, `Overstated`, certainty downgrade, and a dedicated referent registration judge (`spirit-judge-config@b6a3fe7e:manifest.nota:19-30`; `prompts/intent-admission/record-shape.md:1-5`; `checklist.md:1-11`; `burden-ladder.md:1-8`; `rejection-reasons.md:10-17`; `prompts/referent-registration/system.md:1-7`; `user-template.md:1-9`). These are active runtime configuration, not documentation residue.

Required effect:

- delete `JudgeReferentRegistration`, its packet/reply/verdict/reasons, prompt pack, fixtures, adapter route, and guardian projections;
- remove `JudgmentScope`'s Entry-privacy derivation and the Spirit private/public contract axis;
- remove certainty/privacy metadata judgment, `UnclearPrivacy`, field-coupled `Overstated`, certainty-downgrade prose, and all referent/domain instructions;
- continue safe redaction/hash behavior as unconditional adapter safety if still required, not as Spirit record privacy state;
- rebuild the guardian record-context query without referents.

### Guardian journal: wired code; current v6 absent; old physical files stale

The journal stores complete GuardianOperations, RecordSets, referent registrations, complete registered-referent inventories, and verdicts (`spirit@eabe6c6d:src/guardian_journal.rs:34-65`). It is appended on every judgment (`src/guardian_journal.rs:199-230`; `src/store/mod.rs:620-630`).

No current v6 file existed at audit time, so there is no live v6 body to migrate. Five older journal files do exist and are deliberately ignored by current code. They are stale to the runtime but not physically gone. A conforming cutover must either:

- project non-referent decisions into a new journal shape while deleting dropped fields and all referent decisions; or
- retire the journal state entirely.

In either case, old journal bytes may remain only in the private rollback backup, not in the active state directory.

### In-memory copies: wired but ephemeral

The stash table retains complete RecordSets until one lookup consumes them; observer taps retain operation kinds including the ruled operations (`spirit@eabe6c6d:src/nexus.rs:49-81,175-218`). Subscription/events and responses also carry Entry. Stopping the daemon clears the in-memory copies, but the corresponding types and operation variants must still be removed from the new contract/runtime.

### Tests and documentation: wired acceptance plus stale teaching surface

This is a broad acceptance rewrite, not a local migration-only change. A bounded source inventory found ruled-concept occurrences in 32 Spirit source/test files, 6 signal-spirit source/test files, 2 spirit-judge files, and 2 signal-spirit-judge files.

Representative hard gates include:

- generated route/frame round trips for ChangeCertainty and complete Entry shapes (`spirit@eabe6c6d:tests/generated_signal_plane.rs:198-225,352-364`);
- process-boundary certainty mutation and zero-certainty visibility (`tests/process_boundary.rs:1133-1202`);
- owner import auto-registering and validating referents (`tests/import_auto_register_referents.rs:1-11,41-104`);
- versioned log proofs for certainty and referent mutations (`tests/versioned_store.rs:145-243`);
- referent-based render/filter output (`tests/spirit_render.rs:29-59`);
- signal contract validation requiring active referents (`signal-spirit@1cf7c010:tests/validation.rs:52-96`);
- exact generated Entry shape assertions (`signal-spirit@1cf7c010:tests/generated_contract.rs:309-325,452-456`);
- judge privacy/referent behavior and field-bearing fixtures (`spirit-judge@901d1fe4:src/lib.rs:975-1015,1131-1177`; `src/witness.rs:61-84`);
- frozen v13 archived layout/discriminant tests (`spirit@eabe6c6d:src/production_migration/v13.rs:1045-1168`).

The frozen v13 reader tests must remain in the offline migration-only feature. Tests that assert current ruled behavior must be deleted or rewritten. Architecture, README, and manual prose that calls certainty/privacy/referents current behavior becomes stale after the cutover.

## Required destructive migration

The current store is schema v13 (`spirit@eabe6c6d:src/store/mod.rs:90-98`). The next schema must have a new version and new Records/Migrations family hashes because archived Entry and Migration shapes change.

The existing v13 frozen reader accurately reproduces the old Entry, StoredReferent, three-family catalog, and migration marker (`spirit@eabe6c6d:src/production_migration/v13.rs:500-620,656-675,722-802`). Its current `fold_into` is not suitable because it enumerates and forwards every referent (`src/production_migration/v13.rs:808-884`). Reuse its decode boundary, not its preservation sink.

Required sequence:

1. Stop the daemon and judge and prove the store is quiescent.
2. Inventory the active live path, effective archive path, guardian journal, and any explicitly known mirror/checkpoint/export targets using metadata only.
3. Create one rollback snapshot outside the active Spirit state directory, under a `0700` directory with `0600` files. It is private rollback material, not a compatible archive or import source for the new daemon.
4. Open v13 only through the offline frozen reader.
5. Create a virgin next-version store with only the new Records and Migrations catalog.
6. For each current StoredRecord, preserve `RecordIdentifier`, `Domains`, `Kind`, `Description`, and `Importance`; omit `Certainty`, `Privacy`, and `Referents`.
7. Do not materialize any StoredReferent row. Do not carry referent aliases or a migrated referent count.
8. Seed a new versioned history from projected current records and a new migration receipt. Do not ingest the old checkpoint or suffix verbatim: they contain the deleted record fields and referent rows.
9. Apply the same lossy projection to the default archive and every explicit custom archive. Refuse cutover if an expected archive cannot be inventoried. Do not import old archived rows verbatim.
10. Project or retire the guardian journal. Delete every referent decision and ensure no old Entry archive survives in the active journal.
11. Atomically place the new store/archive, then remove all old-format live, archive, guardian, predeploy, preremoval, GC, and schema-backup names from the active state directory. The sole allowed old copy is the external private rollback snapshot.
12. Start the new services and prove the new contract, catalog, and bounded state witnesses.

The current hard-link backup scheme is not sufficient for step 3 or step 11 because it deliberately retains readable old bytes alongside the active files (`spirit@eabe6c6d:src/production_migration.rs:19-46,3075-3077,3183-3187`).

### Exact data-loss scope

From the migrated live database:

- 24 certainty values are deleted: four Medium and twenty High;
- 24 privacy fields are deleted: all Zero;
- every record-to-referent edge is deleted; cardinality unknown;
- every canonical referent object and alias is deleted; cardinality unknown;
- every certainty mutation, referent registration/alias mutation, and old full-Entry row in the active versioned history/checkpoint is discarded rather than replayed verbatim;
- current materialized record identifiers and remaining Entry substance are retained;
- the pre-cutover database marker and log head are not retained as the new state identity.

From other Spirit-owned active surfaces:

- certainty/privacy/referent fields in every archived Entry are deleted; archive record count and value distribution are unknown;
- every referent guardian decision is deleted;
- ruled fields in retained non-referent guardian decisions are deleted, or the journal is retired;
- stale old-format store/archive/journal copies in the active state directory are removed. Their full contents were not inspected; deleting rather than privately backing them up may also discard older record versions and audit testimony.

The expected historical loss is broader than three columns because the old versioned entries are typed archived bodies. The simple conforming fold preserves current allowed state, not old operation history. Preserving allowed portions of history would require a separate event-by-event lossy projector; importing old entries wholesale is forbidden.

## Acceptance witnesses after migration

Use bounded, non-content witnesses:

- the new version reports the intended release and both services are active;
- `Count` with the reduced query shape returns 24;
- a migration-internal digest over `(RecordIdentifier, Domains, Kind, Description, Importance)` matches before/after without printing any field values;
- the new catalog metadata contains Records and Migrations only and contains no Referents family;
- the active state directory contains only current-format active files and no old-format shadows; the external rollback location has private modes;
- old `ChangeCertainty`, `RegisterReferent`, referent judge, privacy/certainty selectors, and old Entry arities fail contract parsing or are absent from generated roots;
- the new marker is stable across read-only witnesses but is not required to equal the v13 marker;
- process tests prove record identity and remaining-substance retention, restart, archive projection, rollback, corruption/refusal, and no body leakage.

Do not use full `Observe`, `Lookup`, archive enumeration, guardian enumeration, or referent enumeration as production acceptance output.

## Coordination impact

The durable Spirit integration coordinator is `protos-engine-po1.10`; Spirit and its contract repos currently have no Beads database. Existing work items assume preservation and are now semantically stale:

- `protos-engine-po1.10` says preserve typed identity and full chains;
- `.10.3` says preserve ordinary wire behavior;
- `.10.4` says the meta contract remains behavior-compatible;
- `.10.5` says preserve ordinary and owner behavior;
- `.10.6` explicitly says retain identifiers and archive behavior;
- `.10.7` expects acceptance to preserve the old surface.

The psyche ruling must be written into that work graph before implementation. At minimum `.10.3` through `.10.7` need revised acceptance, and `.10.6` must name the exact lossy projection above. `protos-engine-po1.10.11` remains blocked on the independent Ethos `ScopeOf` prerequisite; this ruling does not resolve that engine blocker.

No Beads item was changed during this audit.

## Unknowns that must remain named

- Live referent-object and record-edge cardinalities.
- Current archive row count and its certainty/privacy/referent distribution.
- Whether a non-default archive path was configured after the last daemon start.
- Contents of the 44 live/historical `.sema` artifacts; only names, sizes, modes, and timestamps were observed.
- Existence of old data on a historical remote mirror or in user-selected `spirit-render` output directories.
- Whether the psyche wants any non-ruled portion of old guardian audit history projected, rather than retiring it.

None of these unknowns justifies inspecting sensitive record bodies. They should be closed by migration tooling that emits counts/digests only, explicit operator inventory, or an additional psyche ruling where retention changes the destructive boundary.
