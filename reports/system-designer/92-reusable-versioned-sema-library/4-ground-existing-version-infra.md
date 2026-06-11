# Ground: existing version/upgrade/handover infrastructure — the no-reinvent boundary

## Scope and method

Read every named repo at `/git/github.com/LiGoldragon/`: `version-projection`, the upgrade triad (`upgrade` + `signal-upgrade` + `meta-signal-upgrade`), the handover pair (`signal-version-handover` + `meta-signal-version-handover`), plus the two existing hand-rolled migration ladders this infrastructure is supposed to absorb (`upgrade/src/migrations/persona_spirit/...` and `spirit/src/production_migration.rs`) and the `signal-spirit` projection ladder they call into. Maturity read from source plus last-commit dates. This maps what each layer owns and the exact seam where a reusable VC-state library would begin; it does not propose that library's shape.

## The layered picture, top to bottom

```
meta-signal-version-handover   meta-signal-upgrade      <- meta authority (force-flip/rollback/quarantine)
signal-version-handover ---->  signal-upgrade           <- daemon-to-daemon handover wire (MERGED rightward)
        (orphaned)             upgrade                  <- runtime: catalogue + handover driver + DB-migration
                  \            /
                   version-projection                   <- pure type-relation primitives (NO store, NO daemon)
                          |
                   sema-engine / sema                   <- the durable store the VC library would wrap
```

The handover pair and the upgrade triad are **two generations of the same idea**. `signal-version-handover/INTENT.md` and `signal-upgrade/INTENT.md` both record the merge: "the merged ordinary upgrade surface (per the `signal-version-handover` + `signal-sema-upgrade` merge)". The live `upgrade` runtime depends on `signal-upgrade` and `meta-signal-upgrade` and does **not** depend on `signal-version-handover` or `meta-signal-version-handover` (confirmed in `upgrade/Cargo.toml`). The standalone handover pair is the older, superseded contract; the triad is the live one.

## version-projection — pure type relation, real, the one piece that already composes

### What it does today
A library-only crate (439 lines, no daemon, no store, no socket) owning four things:

- **`VersionProjection<Source, Target>` trait** (`projection.rs:9`): one method, `project(source) -> Result<Target, Self::Error>`. Forward and reverse are the same trait with type params swapped; a blanket `Identity` impl (`projection.rs:26`) covers unchanged types for free. This is the "is this representable in the target type" relation, nothing more.
- **`Projected` marker** (`projection.rs:17`): every participating type carries `const CONTRACT_VERSION` and `fn component()`.
- **`ContractVersion([u8; 32])`** (`version.rs:46`): Blake3 schema-version hash, with `#hex` NOTA literal codec. This is the schema-identity primitive — already content-addressed, already typed, already the selector other layers branch on.
- **`policy.rs`**: typed `WritePolicy {Mirror, DivergenceRecord, Reject}`, `ReadPolicy`, `SubscribePolicy`, `PerOperationPolicy`. Pure vocabulary; the INTENT is explicit that the *decision* lives in each consumer's `version_policy.rs`, never here.

### Maturity: real and consumed
Seven dependents across `/git` (`upgrade`, `persona`, `signal-spirit`, `signal-version-handover`, `meta-signal-version-handover`, `orchestrate`, itself). `signal-spirit/src/migration.rs` carries real impls: `V010ToV011`, `V020ToV030`, `V030ToV040` (`migration.rs:314-316`) with per-field projections. The `upgrade` persona-spirit migration actually calls `<V010ToV011 as VersionProjection<v010::Entry, Entry>>::project(...)` (`version_0_1_0_to_0_1_1.rs:297`).

### The one place it brushes the central tension
`version-projection/src/index.rs` defines `RuntimeMigrationLookup` keyed by `RecordKind(String)` with `DecodeFunction = fn(&[u8], &RecordKind) -> Result<String, DecodeError>` (`index.rs:9, 35`). This is a **stringly-keyed, raw-bytes-to-String decode registry** — the exact shape the new library is warned against degenerating into. It exists here to let a version-pair-blind wire (`MirrorPayload`'s raw bytes) be decoded by `RecordKind` at the boundary. The new VC library must decide whether it reuses this lookup or whether the central "generic-without-stringly-typed" tension forces a different selector (the design direction's per-entry SCHEMA-HASH is a candidate replacement for the `RecordKind` string).

## The upgrade triad — orchestration, partly real, partly skeleton

### signal-upgrade (ordinary wire) — real, schema-generated
The live handover + catalogue contract. `Inspect`/`AttemptUpgrade`/`Report` for the catalogue; `AskHandoverMarker`/`ReadyToHandover`/`HandoverCompleted`/`Mirror`/`Divergence`/`RecoverFromFailure` for the daemon-to-daemon protocol. The load-bearing `HandoverMarker` lives in the generated `signal-upgrade/src/schema/lib.rs:185`: `{component, schema_hash: ContractVersion, state_sequence, mirrored_write_count, record_frontier: Option<Integer>, recorded_at_date, recorded_at_time}`. `MirrorPayload`/`DivergencePayload` carry raw bytes plus a `RecordKind` discriminant — version-pair-blind by design.

### meta-signal-upgrade (meta policy) — real, schema-generated
Seven operations: `Register`/`Allow`/`Block`/`Query` (catalogue policy) and `ForceFlip`/`Rollback`/`Quarantine` (selector authority). 1383 lines, schema-derived. Pure contract: no daemon, store, or Tokio.

### upgrade (runtime) — MIXED maturity; this is the important nuance
- **Real and tested:** the migration catalogue and the database-migration path. `MigrationCatalogue` (`catalogue.rs:149`) holds `MigrationModule`s; each module carries a `run: fn(&Attempt)` plus optional `migrate_database: fn(&DatabaseMigration)` (`catalogue.rs:22-27`). The persona-spirit module (`version_0_1_0_to_0_1_1.rs`) genuinely opens a source `.sema`, reads all records through a frozen `historical` type set, projects each via `version-projection`, and writes a fresh target `.sema` — with passing tests (`version_0_1_0_to_0_1_1.rs:339-367`).
- **Real:** the handover driver/client. `handover.rs` has a full async `HandoverClient` over `UnixStream` (`handover.rs:307`), a `HandoverDriver` that asks both sides for markers, cross-checks them field-by-field (`ensure_next_marker_matches`, `handover.rs:477`), drives ready→complete, and recovers on failure (`handover.rs:435-475`). The marker cross-check compares `state_sequence`, `mirrored_write_count`, `record_frontier`.
- **Skeleton:** durable runtime state. The `Engine` (`execution.rs:11`) holds `completions`/`rejections` in in-memory `Vec`s, not a store. Every write verb except `AttemptUpgrade` returns `not_built_yet` (`execution.rs:201-213`). The `upgrade-daemon` binary is a placeholder that returns `daemon_placeholder_response` and opens **no durable state** (`bin/upgrade-daemon.rs:1-9`). The `event.rs` types (`ActiveVersionChanged`, `ActiveVersion`, `VersionQuarantined`) are typed and rkyv-ready but not yet persisted anywhere.

So the upgrade runtime is **a real migration-execution + handover-protocol engine without a durable backing store yet**. That gap is precisely what the psyche's reusable VC-state library is for — but note the upgrade daemon's own state (catalogue, policy, active-version event log, quarantine list) is itself a candidate *consumer* of the VC library, not a competitor to it.

## The handover pair — superseded, still present

### signal-version-handover — orphaned older generation
438 lines, real wire types, but **not depended on by the live `upgrade` runtime**. Its `HandoverMarker` (`signal-version-handover/src/lib.rs`) carries `{component, schema_hash, commit_sequence, write_counter, last_record_identifier, recorded_at_date, recorded_at_time}` — a *different field naming* from the live `signal-upgrade` marker (`commit_sequence`/`write_counter`/`last_record_identifier` vs `state_sequence`/`mirrored_write_count`/`record_frontier`). Its INTENT records the load-bearing receiver-side rule: raw mirror-payload bytes land in a separate container outside the typed DB; the typed DB only accepts records already reverse-projected through `version-projection`; non-representable becomes a typed `Divergence`. That rule survived the merge into `signal-upgrade`; the crate did not.

### meta-signal-version-handover — superseded meta authority
330 lines. `AttemptHandover` (normal path) plus `ForceFlip`/`Rollback`/`Quarantine` overrides, consumed by Persona on its meta surface. Same overrides now live in `meta-signal-upgrade`. Last touched 2026-06-08, before the triad's 06-11 schema refresh.

Both handover-pair repos are best read as **frozen prior art**: their marker shape and receiver-side discipline are the design memory; their code is not the live path.

## The two hand-rolled migration ladders — the duplication j487 names

This is the strongest evidence for j487 ("build the mechanism once; do not reimplement per component"). There are currently **three** independent expressions of the same read-all/project/rewrite pattern:

1. **`spirit/src/production_migration.rs`** — the poster-child's own ladder. Frozen `SpiritStoreV1..V7Record` type sets (`production_migration.rs:133-228`), a `SpiritStorePreviousRecords` dispatcher keyed on `SchemaVersion` (`production_migration.rs:954-977`), each `into_new_entry()` projecting to current. `SpiritStoreUpgrade::upgrade_previous_store` opens a temp `.sema`, imports every projected record, then `fs::rename(&database_path, backup_path)` + `fs::rename(temporary_path, database_path)` (`production_migration.rs:978-995`). Eight schema versions of hand-frozen types living inside the production daemon.
2. **`upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`** — the triad's *separate* persona-spirit migration, with its own frozen `historical` type set (`version_0_1_0_to_0_1_1.rs:110-244`) and the same read-all / project / write-fresh-`.sema` shape (`migrate_paths`, lines 42-59).
3. **`signal-spirit/src/migration.rs`** — the projection ladder (`v010`/`v020`/`v030` modules, `V010ToV011`/`V020ToV030`/`V030ToV040`) both of the above call into.

Two independent *migration drivers* (spirit's own and the upgrade triad's) wrapping the same `signal-spirit` projections, each re-declaring frozen historical types, each doing temp-write + `fs::rename`. That is exactly the per-component reimplementation j487 forbids — and the concrete seam where the reusable VC-state library lands.

## The exact no-reinvent boundary

| Concern | Owned by existing infra (do NOT rebuild) | Owned by the new reusable VC-state library |
|---|---|---|
| Schema identity primitive | `version-projection::ContractVersion([u8;32])` Blake3 hash + `#hex` codec | Reuse it as the per-log-entry SCHEMA-HASH selector |
| Adjacent-version type transform | `VersionProjection<S,T>` trait + per-component impls in `signal-X/migration.rs` | Call it inside replay/reduce; never re-derive it |
| Representability outcome | `ProjectionError::NotRepresentable` | Map it to the durable `Divergence` record on the log |
| Write/read/subscribe policy *vocabulary* | `version-projection::policy::*` | Consume; do not redefine |
| Daemon-to-daemon handover *wire + protocol* | `signal-upgrade` (live) / `signal-version-handover` (frozen) + `upgrade/handover.rs` driver | Provide the durable marker contents (commit-sequence cursor, schema-hash, frontier) the protocol reads; do NOT own the socket protocol |
| Meta authority (force-flip/rollback/quarantine) | `meta-signal-upgrade` (live) | Provide the durable active-version / quarantine *state* these orders mutate; do NOT own the authority wire |
| Migration *orchestration* (catalogue, attempt routing, handover driving) | `upgrade` runtime | Be the store the catalogue/policy/event-log persists into; do NOT own orchestration |
| The actual durable log: payload-bearing, hash-linked, replayable; same-file-vs-separate-file; remote mirror; checkpoint protocol | **nobody — this is the gap** | **This is the library** |

The clean one-line statement of the seam: **everything above the store boundary (type relation, wire, protocol, authority, orchestration) exists and is partly real; the durable, payload-bearing, hash-linked, server-mirrorable LOG underneath it does not exist — every current migration is a one-shot temp-file rewrite with no log.** The new library owns the log and the materialized view; it *calls* `version-projection` for transforms, *feeds* the handover/meta wires their durable marker/state, and *is the backing store* the upgrade runtime currently lacks.

## How the new library must compose (not duplicate)

- The marker the handover protocol exchanges already wants `{schema_hash, commit_sequence/state_sequence, write_counter, record_frontier}`. The design direction's "digests beside monotonic markers; `CommitSequence` stays the ordered cursor" maps directly onto this existing marker shape — the library should *produce* this marker from its log head, not invent a parallel one. Watch the field-name divergence between the two marker definitions before standardizing.
- `version-projection`'s `RuntimeMigrationLookup` (stringly `RecordKind` → `DecodeFunction`) is the existing answer to "decode version-pair-blind bytes." The library's per-entry SCHEMA-HASH selector is a typed alternative to that string key. These two must not both exist as competing selectors; resolving which wins is a design decision the library forces (and is where the central generic-vs-stringly tension actually bites).
- The upgrade runtime's `SchemaTransition`-shaped need is already half-expressed: `MigrationModule.migrate_database` (`catalogue.rs:73`) is a typed `fn(&DatabaseMigration) -> Completion`. The design direction's first-class `SchemaTransition(v_old_hash -> v_new_hash, reducer)` log entry is the durable, replayable generalization of this in-memory module. The reducer in the log entry and the `migrate_database` fn are the same function viewed from two sides.

