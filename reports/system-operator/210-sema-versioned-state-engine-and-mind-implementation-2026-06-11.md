# SEMA Versioned State Engine And Mind Implementation — 2026-06-11

## Frame

The psyche asked for independent prior-art/constraint research, a wait loop for
the system-designer report, then a concrete implementation that keeps SEMA
state versioning reusable rather than reimplemented per component.

Relevant intent is Spirit record `j487`: component Sema database
version-control/server-backed atomic durability must be built once as a
reusable library of generic types and traits, with every component able to opt
in. The earlier duplicate system-operator record `avxy` was removed after
`j487` landed.

Research inputs used:

- System-operator research report:
  `reports/system-operator/209-Research-sema-versioned-state-prior-art-and-constraints.md`
- System-designer report:
  `reports/system-designer/92-reusable-versioned-sema-library/18-synthesis.md`
- Earlier system-operator audit:
  `reports/system-operator/208-Audit-sema-design-log-source-of-truth-feedback.md`

## Implementation Choice

The implementation starts in `sema-engine`, not in each component. This follows
the system-designer correction that `sema-engine` is the real reusable seed:
the older `sema` kernel is only the typed redb/rkyv storage layer, while
`sema-engine` already owns registered record families, commit sequence,
operation log, and replay surfaces.

I chose the same-file log first:

- The payload-bearing version log is stored in the same `.sema` file as the
  component state.
- The domain table write, existing metadata `CommitLogEntry`, and new
  `VersionedCommitLogEntry` land in one storage-kernel write transaction.
- The default engine open path remains metadata-only; a component must opt in
  with `EngineOpen::with_versioning`.

This deliberately avoids a component-local journal and avoids choosing the
remote protocol before the local authoritative log is typed and replayable.

Spirit was not used as the component target because the operator lane already
had Spirit claimed for guardian work and its worktree had unrelated Nix changes.
Per the psyche's fallback instruction, I used `mind`, which was clean and already
stores typed graph records through `sema-engine`.

## Landed Changes

`sema-engine` commit `c970d3f2` (`sema-engine: add opt-in versioned state log`):

- Added `src/versioning.rs` with:
  - `VersioningPolicy`
  - `VersionedStoreName`
  - `SchemaHash`
  - `EntryDigest`
  - `VersionedPayload`
  - `VersionedLogOperation`
  - `VersionedCommitLogEntry`
- Added `EngineOpen::with_versioning`.
- Added an internal `__sema_engine_versioned_commit_log` table.
- Versioned assert/mutate operations persist rkyv record bytes.
- Versioned retract operations persist tombstones keyed by table/key.
- Versioned entries carry store identity, schema hash, commit sequence,
  snapshot, previous digest, entry digest, and a non-empty operation list.
- Added `Engine::versioned_commit_log` and
  `Engine::versioned_replay_from_sequence`.
- Added tests for opt-in behavior, persisted payload replay after reopen,
  digest chaining, tombstones, and multi-operation commit bundling.
- Updated `INTENT.md` and `ARCHITECTURE.md` to describe the reusable
  versioned-state substrate and its non-network boundary.

`mind` commit `7e29a4f4` (`mind: opt store into sema-engine version log`):

- Updated `Cargo.lock` to consume `sema-engine` at `c970d3f2`.
- `MindTables::open` now opens the engine with `VersioningPolicy` store name
  `mind` and a schema-version-derived schema hash label.
- The existing typed thought operation-log test now also verifies the
  payload-bearing version log and decodes the stored `StoredThought` payload.
- Updated `INTENT.md` and `ARCHITECTURE.md` to state that Mind uses the shared
  engine log rather than a Mind-specific journal.

## Validation

`sema-engine`:

- `cargo test` passed after the implementation and docs update.

`mind`:

- First broad test attempt hit host disk exhaustion while compiling test
  targets: `No space left on device`.
- Freed generated build artifacts with `cargo clean` in `mind` and
  `sema-engine`.
- `cargo test --lib` passed.
- `cargo test --test weird_actor_truth typed_graph_records_cannot_bypass_sema_engine -- --exact`
  passed.

Both repos were pushed to `main`; both `main@origin` bookmarks matched the
pushed commits after verification.

## Remaining Work

No remote server was implemented in this pass. What now exists is the reusable
local authoritative log that a remote mirror/server can consume. The next layer
should add:

- idempotent remote append keyed by store, commit sequence, and entry digest;
- remote acknowledgement policy and named durability levels;
- restore protocol from checkpoint plus versioned log tail;
- remote retention and compaction rules;
- checkpoint records that bind current table state to a version-log digest;
- explicit handling for component-local tables that still bypass
  `sema-engine::assert` / `mutate` / `retract`.

The engine also inherits its documented single-owner assumption: component
daemons must serialize engine calls through one store actor. The versioned log
does not try to make concurrent multi-handle writes safe.
