# Spirit Production Database Sandbox Migration Test

## Scope

The test used the deployed production Spirit database only as a source file.
The live database was copied into temporary directories before every open or
daemon startup attempt. No mutation path touched the production file.

Production source:

- deployed CLI: `spirit` from the installed production profile
- deployed database:
  `/home/li/.local/state/persona-spirit/v0.5.2/persona-spirit.redb`
- production public baseline:
  `spirit "(Observe (Records ((Any []) None Any Any SummaryOnly)))"` returns
  364 public Zero-privacy records

## What Was Added

`spirit` now carries an ignored integration test:

- `/git/github.com/LiGoldragon/spirit/tests/production_database_sandbox.rs`

It requires `SPIRIT_PRODUCTION_DATABASE` and is intentionally ignored during
normal `cargo test` because it depends on the machine-local production store.

The test has two witnesses.

1. Direct copied-file startup:
   copy the production file to a temporary `production-copy.sema`, generate a
   binary `Configuration`, start the new `spirit-daemon`, and assert startup
   fails with the expected schema-version guard.
2. Explicit content migration:
   copy the production file to a temporary legacy source, open that copy with
   the production v5 record shape, convert each production `Entry` into the new
   schema-derived `spirit::schema::signal::Entry`, send each one to a spawned
   new Spirit daemon over binary `SignalTransport`, and then verify the new
   sandbox database through new Spirit queries and mutations.

## Result

Direct database reuse does not work, and should not be treated as working.

The new daemon refuses the copied production file before binding its sockets:

```text
sema: schema version mismatch — file was written with v5, this build expects v1
```

That is sema's version guard doing the right thing. New Spirit cannot be cut
over by simply pointing it at
`/home/li/.local/state/persona-spirit/v0.5.2/persona-spirit.redb`.

Explicit content migration does work in the sandbox. The test decodes the
copied production v5 records and reasserts them through the new daemon's binary
Signal path into a fresh new `.sema` target. It then proves:

- every migrated production record receives a new Spirit identifier;
- every migrated identifier resolves through `Lookup`;
- `Count` works for a topic query over the migrated content;
- `Observe` returns a stash handle over migrated content;
- `LookupStash` returns the stashed migrated records;
- fresh post-migration `Record` works;
- `ChangeCertainty` works;
- `ChangeRecord` works;
- `Remove` works;
- `State` classification still records;
- `Tap` exposes operation history.

The migration path used binary schema values, not CLI text. That is important:
one production description contains bracket syntax that the current generated
NOTA text projection emitted as an unsafe inline bracket string during an
earlier replay attempt. The daemon/schema/store path was fine; the text edge
was the wrong layer for bulk migration.

## Remaining Production-Readiness Gaps

The new Spirit is not yet a production drop-in for the deployed database.

The direct-open path is blocked by schema version and storage shape:

- production `persona-spirit` uses `SPIRIT_SCHEMA_VERSION = 5`;
- new `spirit` uses `SPIRIT_SCHEMA_VERSION = 1`;
- production stores a `StoredRecord { identifier: signal_spirit::RecordIdentifier, entry: StampedEntry }`;
- new Spirit stores a schema-derived `Entry` in a sema-engine identified table;
- production identifiers are short base36 codes;
- new identifiers are sema-engine numeric identifiers.

The sandbox migration deliberately mints new identifiers. That preserves record
content and makes the records queryable in new Spirit, but it does not preserve
old `RecordIdentifier` values. If existing agent workflows, reports, or
external references depend on production short identifiers, cutover needs an
identifier mapping artifact or a schema decision that makes old identifiers
first-class in new Spirit.

The new query surface also lacks an all-topic query root. The test proves "all
records are queryable" by looking up every migrated identifier and then uses a
topic query for `Count`/`Observe`. If production workflows require broad
database-wide observation through new Spirit, the signal/nexus/sema schemas need
a visible Nexus/SEMA feature for that operation rather than an ad-hoc store
branch.

The generated NOTA text projection needs a bracket-safe string witness before
CLI-text export/import can be trusted for arbitrary production descriptions.
Bulk database migration should stay binary/schema-level regardless.

## Verification

Run from `/git/github.com/LiGoldragon/spirit`:

```sh
SPIRIT_PRODUCTION_DATABASE=$HOME/.local/state/persona-spirit/v0.5.2/persona-spirit.redb \
  cargo test --features nota-text --test production_database_sandbox -- --ignored --test-threads=1
```

Result:

```text
running 2 tests
test copied_production_database_requires_explicit_migration ... ok
test production_records_migrate_into_new_spirit_and_remain_queryable ... ok
```

Additional local verification:

```text
cargo test --features nota-text --test production_database_sandbox
cargo test --all-features
cargo clippy --all-targets --all-features -- -D warnings
```

All passed.
