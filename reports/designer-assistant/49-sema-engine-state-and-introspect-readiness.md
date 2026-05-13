# 49 - sema-engine state and readiness

*Designer-assistant report, 2026-05-14. Scope: survey the current
`sema-engine` implementation after operator work, verify whether the
repository exists, compare the current surface to
`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`,
and give the operator a concrete finish path.*

## 0. Bottom line

The `sema-engine` repository exists and is real:

- Local checkout: `/git/github.com/LiGoldragon/sema-engine`
- Remote: `https://github.com/LiGoldragon/sema-engine`
- Default branch: `main`
- Current remote head surveyed: `33e7c63 sema-engine: add operation log snapshots`

No repository-creation recommendation is needed. The recommendation is
to finish the existing repo.

Current state: **semi-ready kernel of the full engine.** It has the
right repository boundary, the right library-only shape, the right core
dependencies, a durable registered-table catalog, `Assert`, `Match`,
`SnapshotId`, and an operation log. It is not yet the full database
operation engine described in `/158`.

The operator has also cleaned `sema` into the intended storage kernel:
`/git/github.com/LiGoldragon/sema` is at
`57ad38c sema: remove legacy slot store`, and the source-scan witnesses
for no `Slot`, no legacy raw-byte store, no schema-less public open, and
no reader-count API now exist. One stale doc line remains:
`sema/ARCHITECTURE.md` still says Package A is "in progress" and speaks
as if `sema-engine` has not yet been created. That status should be
updated.

I did not run tests in `sema-engine` because the operator currently
holds `/git/github.com/LiGoldragon/sema-engine` and
`/git/github.com/LiGoldragon/persona-mind` under lock for the
persona-mind consumer migration. This is therefore a read-only code and
architecture survey.

## 1. What is implemented

`sema-engine` currently implements the smallest useful full-engine
slice:

| Surface | Current state |
|---|---|
| Repository boundary | Exists as independent repo with `AGENTS.md`, `ARCHITECTURE.md`, `skills.md`, flake, Cargo package, and tests. |
| Runtime shape | Library crate only. No daemon binary, no `src/main.rs`, no Kameo actor tree. Correct. |
| Dependencies | Direct dependencies are `sema`, `signal-core`, `rkyv`, and `thiserror`. No direct Persona contract crates, no direct Kameo, no direct Tokio, no direct NOTA codec. |
| Engine open | `Engine::open(EngineOpen)` wraps `sema::Sema::open_with_schema`. Correct dependency direction. |
| Registered tables | `register_table` persists `TableRegistration` into `__sema_engine_catalog` and reconstructs catalog state on reopen. |
| Record trait | `EngineRecord::record_key()` supplies the key; records remain component-owned typed Rust values. |
| Assert | `Engine::assert(Assertion<R>)` checks the table registration, writes the record, writes an operation-log entry, updates latest snapshot, and returns `MutationReceipt`. |
| Match | `Engine::match_records(QueryPlan<R>)` supports `All` and `Key` filters and returns `QuerySnapshot`. |
| Snapshot | `SnapshotId` exists; mutation replies and query snapshots carry it. |
| Operation log | `OperationLogEntry` exists and persists on assert; `operation_log()` returns the current log. |
| Tests | There are dependency-boundary tests, assert/match tests, catalog reopen tests, unregistered-table rejection, and operation-log/snapshot reopen tests. |

This is enough to prove the essential layering:

```text
component-owned record type
  -> sema-engine EngineRecord / Assertion / QueryPlan
  -> sema typed table operations
  -> component.redb
```

It is also enough for a first simple consumer that only needs:

- register a record family;
- append/assert typed records;
- read by key or scan all;
- observe a snapshot id;
- inspect the full operation log.

## 2. What is not implemented yet

The current implementation is not yet the full `/158` engine surface.
Missing surfaces:

| `/158` surface | Current state |
|---|---|
| `register_index` / `IndexDescriptor` / `IndexRef` | Missing. |
| Rich `QueryPlan` | Only `All` and `Key`; no key range, index lookup, filter, project, limit, order, aggregate, or constrain. |
| `MutationPlan` | Missing. Only direct `Assertion<R>` exists. |
| `mutate` | Missing. |
| `retract` | Missing. |
| `atomic` | Missing. There is no multi-record or multi-family transaction scope at the engine layer yet. |
| `subscribe` | Missing. No `SubscriptionSink`, subscription catalog, initial snapshot, or commit-then-emit delta. |
| `validate` | Missing. No dry-run or validation scope. |
| `list_tables()` | Not exposed as a first-class API. `catalog()` returns an in-memory catalog reference, but `/158` wants explicit schema introspection. |
| `list_indexes()` | Missing. |
| `operation_log_range()` | Missing. Current API returns the whole operation log. |
| Component migrations | No surveyed Persona component depends on `sema-engine` yet. `persona-mind` still owns `MindTables` over direct `sema`. |

The current state maps roughly to:

```text
/158 Package 1: sema cleanup              done in sema
/158 Package 2: repo + table/catalog/log  partially done
/158 Package 3: query/mutation plans      barely started
/158 Package 4: subscribe                 not started
/158 Package 5: validate/introspection    not started
component migration                       not landed yet
```

## 3. Boundary gaps

### 3.1. Dependency pin is not strict enough

`sema-engine/Cargo.toml` currently uses:

```toml
sema = { git = "https://github.com/LiGoldragon/sema.git", branch = "main" }
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git", branch = "main" }
```

`Cargo.lock` pins exact revisions, but `/158 §3.2` requires explicit
manifest revisions:

```toml
sema = { git = "https://github.com/LiGoldragon/sema.git", rev = "..." }
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git", rev = "..." }
```

The current dependency-boundary test checks "git, not path"; it does
not reject `branch = "main"`. Operator should change the manifest to
explicit `rev = ...` pins and add a witness that fails on `branch =`.

### 3.2. "No NOTA in sema-engine" is direct-only right now

`sema-engine` has no direct `nota-codec` dependency, which is good.
But `signal-core` currently depends on `nota-codec`, so `sema-engine`
inherits NOTA transitively through the verb-spine crate.

That may be acceptable if the rule is "the engine never imports or
uses NOTA APIs directly." It is not acceptable if the rule is "the
engine's build graph must contain no NOTA at all." If the stricter rule
is desired, the fix is not in `sema-engine`; it is to split
`signal-core` so the pure verb/frame spine is independent from NOTA
pattern/channel helpers.

Recommendation: do not block the current engine slice on this, but file
it as an architecture question before declaring the dependency boundary
fully clean.

### 3.3. `sema/ARCHITECTURE.md` status is stale

The `sema` architecture now correctly describes the storage-kernel
boundary, but its status section still says Package A is in progress
"before creating the library-only `sema-engine` repository." That was
true earlier today; it is stale now. Operator should update it to say:

- Package A cleanup has landed at `57ad38c`;
- `sema-engine` exists;
- remaining work is engine-surface completion and consumer migration.

### 3.4. Consumer migration has not started in code

`persona-mind` remains a direct `sema` consumer. Its architecture still
names `MindTables`, `StoreKernel`, direct `sema::Table` constants, slot
cursors, graph tables, and subscription registration tables. That is
expected while the operator is holding the migration lock, but it means
the engine has not yet proven itself against a real component.

Until `persona-mind` moves even one graph path through `sema-engine`,
the engine is still a successful library pressure test, not an
integrated stack capability.

## 4. Readiness for persona-introspect

`persona-introspect` can start architecture and actor work now, but its
real local store should wait for the next `sema-engine` surfaces.

Ready now:

- define `IntrospectionStore` as a real state-carrying actor;
- define `introspect.redb` as owned local state;
- forbid direct peer redb opens;
- add architecture/tests proving NOTA is edge-only and peer state is
  reached through daemon sockets;
- prepare local record families such as `ObservedTarget`,
  `IntrospectionQueryRecord`, `IntrospectionReplyRecord`, and
  `IntrospectionErrorRecord`.

Potentially ready with current `sema-engine`:

- persist a simple local query/reply/error audit trail keyed by
  `RecordKey`;
- reopen the local catalog;
- read by key or scan all records;
- use `SnapshotId` as a local observation cursor.

Not ready yet:

- cache-backed `DeliveryTrace` by correlation id if it needs indexes;
- time-window observation queries;
- subscription-backed live introspection;
- schema/catalog listing through explicit `list_tables()`;
- replay from a bounded operation-log range.

Therefore the introspect implementation should either:

1. start with a minimal audit store on current `Assert`/`Match`, or
2. land the actor and architecture skeleton first and wait for
   `operation_log_range`, `list_tables`, indexes, and `Subscribe`.

My recommendation is (2) for the first operator-assistant pass, unless
operator finishes the next `sema-engine` surface before the
introspect store work starts.

## 5. Operator finish path

Priority order:

1. **Pin dependencies exactly.** Replace `branch = "main"` with
   explicit `rev = ...` for both `sema` and `signal-core`; add a
   witness rejecting branch pins and sibling path deps.
2. **Update stale architecture status.** `sema/ARCHITECTURE.md` should
   stop saying the repo is being cleaned before `sema-engine` exists.
   `sema-engine/ARCHITECTURE.md` should mark the current package as
   "catalog + Assert + Match + operation-log snapshots landed; next
   package is query/mutation plan widening."
3. **Expose catalog introspection.** Add `list_tables()` as a real API
   instead of requiring consumers to borrow `catalog()`. This directly
   supports introspection and component self-reporting.
4. **Add bounded log access.** Add `operation_log_range(range)` before
   any component needs replay/catch-up.
5. **Widen `QueryPlan` carefully.** Add key range and index-backed
   lookup before generic filter/project/order. Time-indexed
   observations in terminal/router/introspect need this soon.
6. **Add `MutationPlan` plus `mutate` / `retract`.** Criome and manager
   lifecycle state need update/removal semantics, not only append/assert.
7. **Add `atomic`.** Multi-family writes need one transaction and one
   coherent snapshot.
8. **Add `Subscribe` last among core primitives but before migrating
   graph subscriptions.** The commit-then-emit contract is the hard
   part; do not implement component-local subscription machinery that
   will be thrown away immediately.
9. **Migrate one persona-mind graph path.** First proof should be a
   real `persona-mind` request compiling to `Engine::assert` or
   `Engine::match_records`, not only toy tests inside `sema-engine`.
10. **Then hand operator-assistant the introspect store.**
    `persona-introspect` should use `sema-engine` for its own database,
    but peer inspection still goes through daemon sockets and component
    contracts.

## 6. Recommendation

Treat `sema-engine` as **semi-ready, not missing**.

Do not create another repository. Do not rename this one. Continue from
the existing repo and push it from "registered table + Assert/Match
proof" to "full database-operation engine" in the order above.

The next operator report should not ask whether `sema-engine` exists;
it should report which engine package is being completed and which
first real consumer path proves it.
