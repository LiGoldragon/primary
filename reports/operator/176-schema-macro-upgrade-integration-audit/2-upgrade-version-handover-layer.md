*Kind: Audit Slice · Topic: upgrade/version/handover layer · Date: 2026-05-24 · Lane: operator*

# 176.2 · Upgrade/version/handover layer

## Scope

Read-only audit of:

- `/git/github.com/LiGoldragon/upgrade`
- `/git/github.com/LiGoldragon/signal-upgrade`
- `/git/github.com/LiGoldragon/owner-signal-upgrade`
- `/git/github.com/LiGoldragon/version-projection`
- `/git/github.com/LiGoldragon/sema-engine`
- `/git/github.com/LiGoldragon/CriomOS-test-cluster`

## What Is Live On The Code Path

### The v0.1.0 to v0.1.1 Spirit migration exists

`upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` implements
the database migration used by `upgrade-spirit-sandbox-test`.

The shape is the hand-written two-module pattern:

- `historical` re-declares the archived v0.1.0 storage records.
- `current_shape` declares current storage records.
- explicit conversions map old `Certainty` to current `Magnitude`.

This is enough for the current sandbox migration witness.

### `signal-upgrade` is used by upgrade runtime library code

The `upgrade` crate imports `signal-upgrade` types in catalogue, execution, and
handover code. The ordinary upgrade contract is not purely decorative.

`owner-signal-upgrade` is weaker: the audit found placeholder/event usage, but
no meaningful owner operation runtime path.

### sema-engine commit sequence exists

`sema-engine` implements a monotonic commit sequence, durable commit log
entries, and replay APIs. Unit tests prove replay-from-sequence behavior and
that rejected commits do not advance the sequence.

## What Is Not Yet On The Runtime Path

### The migration is not schema-derived

The current migration does not use a schema diff or generated projection. It is
handwritten Rust conversion logic.

The `schema` crate can plan some upgrade annotations in tests, and
`version-projection` defines the trait surface, but the migration does not come
from generated schema-derived impls.

### `VersionProjection` is scaffold plus hand-written use

`version-projection` provides:

- `VersionProjection<Source, Target>`
- `Identity`
- `Projected`
- `RuntimeMigrationLookup`

The Spirit signal contract has handwritten `V010ToV011` implementations and
tests. The upgrade database migration does not delegate to those impls as the
single authority; it repeats a parallel historical/current conversion shape in
the `upgrade` crate.

### Handover driver is mock-tested, not system-wired

`upgrade/src/handover.rs` contains a UnixStream client/codec/driver, and
`upgrade/tests/handover_driver.rs` tests it with mock UnixListener endpoints.

The real `upgrade` and `upgrade-daemon` binaries are still placeholders. The
nspawn runner uses `upgrade-spirit-sandbox-test`, which performs an in-process
copy/migrate/verify flow rather than driving the private handover socket
between live daemons.

### sema-engine replay is not wired into handover

Spirit uses the current commit sequence in handover markers. The upgrade stack
does not yet use `replay_from_sequence()` to reconcile writes during a live
handover window.

## Nspawn State

`CriomOS-test-cluster` has a Spirit nspawn path that installs v0.1.0, v0.1.1,
and `upgrade`, writes records, runs the sandbox migration, and verifies record
survival.

Designer report `/330` records a successful Prometheus run at N=10. Operator
prior work also had in-process 500-record witnesses. The current nspawn path is
still an offline/copy migration proof, not a zero-downtime socket handover
proof.

## Verdict

The upgrade stack can migrate the Spirit database in a sandbox today. It does
not yet prove the desired live no-downtime protocol, and it does not use
schema-derived migration code.
