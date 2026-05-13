# 45 - Sema kernel and Sema engine interface split

*Designer-assistant report, 2026-05-14. Scope: evaluate the new
proposal to keep a small `sema` interface for typed storage while
creating a separate `sema-engine` interface/repository for full Signal
verb execution. This report revises the "one crate" direction in
`reports/designer/157-sema-db-full-engine-direction.md` in light of the
micro-component rule and the clarified ESSENCE rule that backward
compatibility is not a design constraint for systems still being born.*

## 0. Bottom line

Yes: split the interfaces.

The clean shape is:

- `sema`: the typed redb/rkyv storage kernel. It owns database
  lifecycle, schema/header guards, typed tables, low-level
  transaction closures, and only storage-kernel mechanics.
- `sema-engine`: a new repository and crate for the full database
  engine. It owns Signal verb execution over registered record
  families: query plans, mutation plans, indexes, subscriptions,
  validation, operation logs, snapshots, and schema introspection.

This is not a backward-compatibility compromise. It is a boundary
correction. The current `sema` crate is a small kernel capability; the
full engine is a different noun with different vocabulary. Per
`skills/micro-components.md`, that earns a separate repo.

The important caveat: do not preserve the current `sema` API just
because current components use it. If `sema` needs to break so
`sema-engine` has a beautiful substrate, break it. The split is not
"old API forever plus new API beside it." The split is "kernel and
engine are different capabilities."

## 1. What the current `sema` implementation actually is

The current repo is small and kernel-shaped.

`/git/github.com/LiGoldragon/sema/src/lib.rs` owns:

- `Sema::open` and `Sema::open_with_schema`;
- `Sema::read` and `Sema::write`;
- `Table<K, V>` with `get`, `insert`, `remove`, `iter`, and `range`;
- schema-version and rkyv-format guards;
- a legacy slot-store surface: `store`, `get(Slot)`, and slot `iter`;
- Criome-specific `reader_count` and `set_reader_count` leftovers.

`/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` currently says
Sema is the kernel for typed stores and explicitly does not own
runtime write ordering, actor mailboxes, validator pipelines, wire
format, or subscriptions.

That architecture is no longer sufficient for the full engine, but it
is still a coherent description of a kernel. The mistake would be
growing that kernel until it contains two capabilities:

```text
sema
  storage kernel vocabulary:
    redb, rkyv, Table, Schema, transaction, header guard

  engine vocabulary:
    SemaVerb, QueryPlan, MutationPlan, Subscribe, Validate,
    operation log, snapshot id, subscription sink, record catalog
```

Those vocabularies are related, but they are not the same bounded
context. The storage kernel can be used by components that need simple
typed persistence. The engine is for components that want Signal's
database-operation language executed for them.

## 2. Why a separate `sema-engine` repo is the better shape

### 2.1 It matches micro-components

`skills/micro-components.md` says a new capability defaults to a new
repo. "Storage kernel" and "database-operation engine" are two
capabilities:

- the kernel hides redb/rkyv details behind typed tables;
- the engine executes high-level operations over record families.

The engine has enough vocabulary, tests, and invariants to deserve its
own `ARCHITECTURE.md`, `AGENTS.md`, `skills.md`, flake, Cargo package,
and report trail.

### 2.2 It protects the low-level interface from semantic overload

`sema` should not depend on `signal-core` if it can avoid it. A kernel
should not need to know what `Assert`, `Match`, `Subscribe`, or
`Infer` mean. It should know how to open a file, guard a schema, and
read/write typed records under transactions.

`sema-engine` can depend on both:

```text
signal-core   -> owns SemaVerb and generic wire operation words
sema          -> owns typed redb/rkyv storage mechanics
sema-engine   -> maps Signal verbs to database execution over sema
```

This keeps dependency direction clean. Simple storage consumers do not
pay the conceptual or dependency cost of the full engine.

### 2.3 It lets the transition be correct without being transitional

There is no backward-compatibility requirement. But separate repos
still help because they let the engine be built beside the kernel
without forcing every current consumer to migrate in the same commit.

That is not a design compromise if the rule is explicit:

- `sema` may break whenever its API is wrong;
- `sema-engine` may require a cleaner `sema` surface;
- components that still use only `sema` do so because they only need
  kernel storage, not because old code is being protected.

The wrong shape would be "keep ugly sema calls because components use
them." The right shape is "keep the kernel only where the kernel is
the true abstraction."

## 3. The proposed repository map

### `sema`

Role: typed storage kernel.

Owns:

- `Sema` database handle;
- redb file lifecycle;
- rkyv encode/decode guardrails;
- schema/header guards;
- `Table<K, V>`;
- closure-scoped `read` and `write`;
- low-level table iteration/scanning primitives;
- low-level key support and table materialization.

Should probably remove or relocate:

- legacy raw slot-store methods if they are no longer a beautiful
  kernel abstraction;
- `reader_count` and `set_reader_count`, because they are
  Criome-specific runtime configuration;
- any future Signal verb or query-plan type.

May still add:

- `Table::scan_range` if the kernel needs closure-scoped scanning;
- named packed-key support if it is purely storage-key mechanics;
- low-level index table helpers only if they remain storage nouns and
  do not become query semantics.

### `sema-engine`

Role: full database-operation engine.

Depends on:

- `sema`;
- `signal-core`;
- possibly tiny general crates for time, ids, or typed errors if those
  become shared engine vocabulary.

Owns:

- `Record` or `EngineRecord` trait;
- `RecordFamily` / `TableDescriptor`;
- `IndexDescriptor`;
- `QueryPlan`;
- `MutationPlan`;
- `AggregatePlan`;
- `ConstrainPlan`;
- `Subscription`;
- `SubscriptionSink`;
- `OperationLog`;
- `SnapshotId`;
- `ValidationResult`;
- operation execution for Signal verbs.

Does not own:

- Persona-specific record types;
- component authorization;
- actor mailbox order;
- Unix sockets;
- Nexus parsing;
- human-facing formatting;
- a daemon process by default.

Important: `sema-engine` should start as a Rust library, not a
`sema-engine-daemon`. Each Persona component owns its own state file
and actor. The engine executes inside that component's daemon. A
central engine daemon would blur state ownership and create a false
shared database component.

Do not create a separate engine-protocol crate yet. `signal-core`
already owns the universal verb words, and `sema-engine` is the first
implementation of their database execution. If a second engine
implementation appears, or if plan IR must cross a process boundary,
then split out an engine contract crate. Before that, a contract for a
single implementation would be ceremony rather than a useful boundary.

### Component repos

State-bearing components choose one of two interfaces:

```text
small storage need:
  component -> sema

full Signal operation need:
  component -> sema-engine -> sema
```

For example:

- `persona-mind` should move to `sema-engine` because graph queries,
  subscriptions, operation logs, and snapshot identity are central to
  its domain.
- `persona-terminal` should likely move to `sema-engine` once
  observations become queryable and subscribable.
- a simple component with one configuration table may stay on `sema`.

## 4. How this changes designer 157

`reports/designer/157-sema-db-full-engine-direction.md` asks where the
source lives and recommends one repo with modules. I now recommend
changing that answer.

The better answer is:

```text
Q1 revised:
  Keep `sema` as the storage kernel.
  Create `sema-engine` as the full database-operation engine.
  Break `sema` as needed to make the engine substrate beautiful.
```

This keeps the design goal from 157 intact: sema-engine is still the
full execution engine for Signal verbs. It only changes source
organization and dependency direction.

157's packages map cleanly:

| 157 package | New home |
|---|---|
| Verb-mapping witnesses per contract | `signal-*` contracts, unchanged |
| Record trait + table/index registration | `sema-engine`, backed by `sema` |
| QueryPlan / MutationPlan IR + execution | `sema-engine` |
| Subscribe primitive | `sema-engine` |
| Validate, ListRecordKinds, snapshot identity | `sema-engine` |
| Low-level scan/key helpers | `sema` only if they are storage-kernel shaped |

So the split is not a retreat from full engine. It is a better
component boundary for the same full-engine goal.

## 5. What should change in `sema`

The current `sema` implementation is close to a clean kernel, but it
has two pieces of debt.

### 5.1 Legacy slot store

The raw slot-store API is explicitly "compatibility utility used by
older criome record-store code." It is suspicious under the new
ESSENCE rule:

```text
Sema::store(&[u8]) -> Slot
Sema::get(Slot) -> Option<Vec<u8>>
Sema::iter() -> Vec<(Slot, Vec<u8>)>
```

This is not typed-table storage. It stores raw bytes and asks the
consumer to decode later. If Criome still needs it, it should either:

- move to a Criome-specific storage layer;
- become a typed append-only table abstraction in `sema`;
- or be deleted when Criome moves to the new model.

Do not preserve it as kernel API just because it exists.

### 5.2 Criome reader-count config

`DEFAULT_READER_COUNT`, `reader_count`, and `set_reader_count` are
already marked deprecated and Criome-specific. They should leave
`sema` before or during the engine work. The kernel should not carry
runtime actor-pool configuration for one consumer.

### 5.3 Table API

`Table::iter` and `Table::range` eagerly collect rows. That is a
reasonable simple surface for a kernel, but the engine will need
closure-scoped scans with early stop. Add that to `sema` only if it is
expressed as a kernel primitive:

```text
Table scans rows under a transaction and gives the caller owned typed
records. It does not know domain predicates, Signal verbs, or query
plans.
```

`sema-engine` can then use that primitive to implement `QueryPlan`.

## 6. What `sema-engine` should expose first

Start with the smallest engine surface that proves the split:

1. `EngineCatalog`

   Registers record families and indexes. It is the engine's typed map
   of "what can be queried or mutated."

2. `QueryPlan`

   Covers `Match` by key/range/index, `Project`, `Aggregate`, and
   simple `Constrain` later. The first implementation can support
   `Match` and `Project` while reserving typed unimplemented variants
   for the rest.

3. `MutationPlan`

   Covers `Assert`, `Mutate`, `Retract`, and closure-scoped `Atomic`.

4. `OperationLog`

   Records what the engine did: verb, record family, key, origin,
   result, snapshot id.

5. `Subscription`

   Registers a query plan and pushes initial snapshot plus post-commit
   deltas through a consumer-owned sink.

6. `Validate`

   Executes a plan in a rollback-only transaction and returns typed
   diagnostics.

Do not start with every optimization. Start with the types that prove
the engine owns the verb execution.

## 7. Witnesses that prove the boundary

The split needs tests that make the boundary hard to fake.

### Kernel witnesses in `sema`

- `sema_has_no_signal_core_dependency`: source or cargo metadata
  witness that the kernel does not depend on Signal.
- `sema_has_no_persona_dependency`: same for Persona.
- `typed_table_round_trip`: a typed value goes in and comes out
  through `Table<K, V>`.
- `schema_mismatch_hard_fails`: schema guard remains kernel-owned.
- `legacy_raw_slot_store_absent_or_criome_owned`: either the raw slot
  store is gone from `sema`, or an explicit report names why it is
  still kernel-shaped.

### Engine witnesses in `sema-engine`

- `engine_depends_on_sema_and_signal_core`: verifies dependency
  direction.
- `engine_executes_assert_through_registered_record_family`: no
  component opens a raw table for the operation.
- `engine_match_uses_registered_index`: a `Match` plan over an index
  returns ordered records through the engine.
- `engine_atomic_rolls_back_all_record_families`: heterogeneous
  operations fail atomically.
- `engine_subscribe_pushes_after_commit`: proves subscription deltas
  are engine-owned, not component-hand-rolled.
- `component_can_use_sema_without_sema_engine`: simple kernel consumer
  compiles without the engine crate.

### Component migration witnesses

- `persona_mind_no_direct_sema_table_import_after_engine_migration`:
  once migrated, mind uses `sema-engine` for graph records and
  subscriptions.
- `persona_terminal_observations_use_engine_catalog`: terminal
  observations are registered as record families and indexes in the
  engine.

## 8. Recommendation

Adopt the split:

```text
sema          = beautiful storage kernel
sema-engine   = full Signal/Sema verb execution engine
```

Then immediately make the high-level rule explicit:

- `sema` may break;
- `sema-engine` may force `sema` to change;
- no transitional design is allowed solely to protect current callers;
- old deployment needs live on old branches or separate repos, not in
  the new design.

The work order I would give operators:

1. Clean `sema` into a storage kernel by removing or relocating
   Criome-specific and raw compatibility surfaces.
2. Create `sema-engine` as a new repo with its own architecture,
   skills, flake, and witnesses.
3. Implement catalog + basic `Assert`/`Match` execution first.
4. Migrate `persona-mind` as the first real consumer.
5. Add subscription/changefeed once the first query/mutation path is
   real.

This gives the full engine without turning the kernel into a bundled
monolith.
