# 163 — Seven verbs, no `Structure` eighth: schema is data

*Designer decision record, 2026-05-14. Closes the falsifiable
eighth-verb question raised in `/162 §4` with a concrete containment
argument and worked examples. The adopted direction: the seven-verb
`SignalVerb` set absorbs all DDL-shaped operations through the
schema-as-data discipline. `Structure` does not earn its seat until
concrete workspace traffic breaks the containment rule.*

**Retires when:** real workspace DDL traffic fires one of the
falsifiability triggers in §5, at which point this report is
superseded by an eighth-verb proposal.

---

## 0 · TL;DR

- The seven-verb `SignalVerb` spine (`Assert`, `Mutate`, `Retract`,
  `Match`, `Subscribe`, `Atomic`, `Validate`) is the adopted closed
  set.
- DDL-shaped operations (`CREATE TABLE`, `ALTER`, `DROP`, `CREATE
  INDEX`, schema migrations) **fit cleanly inside the seven** when
  the catalog itself is a typed table.
- The case rests on three workspace-specific properties: (1) the
  catalog is a typed redb table managed by the same engine actor as
  every other table; (2) `sema-engine` is single-writer per daemon,
  so DDL needs no separate lock/visibility primitive; (3) shape is
  **compile-time-typed Rust**, not runtime SQL, so the wire only
  carries an *announcement* of a decision the type system already
  made — not the shape itself.
- The argument is falsifiable. Three concrete conditions (§5) would
  reopen the eighth-verb question. None apply to current workspace
  traffic.

---

## 1 · The thesis: schema is data

The SQL/relational tradition treats DDL and DML as distinct because
SQL fuses three things into `CREATE TABLE`:

1. **Declare a new shape** (the type)
2. **Allocate storage** (the physical table)
3. **Make this visible to the planner** (catalog registration)

The workspace separates these three:

| SQL fusion | Workspace home |
|---|---|
| Declare a new shape | A `#[derive(NotaRecord)] struct T { ... }` in a contract crate. **Compile-time.** |
| Allocate storage | Internal to `sema-engine` when a consumer calls `Engine::register_table::<T>()`. **Engine-internal.** |
| Catalog registration | A row in the engine's typed `RegisteredTable` catalog table. **Boundary-visible.** |

Only the third crosses a Signal boundary. The shape is already in
Rust; the storage is engine-internal. What `CREATE TABLE` carries
on the wire is an *announcement*: "this consumer has decided to
hold type `T`." That announcement is an `Assert` on a catalog row.

**No new verb. The catalog is just another table.**

---

## 2 · Worked examples

### 2.1 · CREATE TABLE — `Assert` on the catalog

```rust
// Consumer-facing API (in code, not on the wire):
engine.register_table::<TerminalSession>(TableDef { ... })?;

// What crosses the Signal boundary (or lands in the catalog redb table):
Operation {
    verb: SignalVerb::Assert,
    payload: EngineCatalog::TableRegistration(RegisteredTable {
        record_kind: "TerminalSession",
        schema_version: SchemaVersion(3),
        record_size_hint: 240,
        index_count: 2,
    }),
}
```

### 2.2 · CREATE INDEX — `Assert` on the index catalog

```rust
Operation {
    verb: SignalVerb::Assert,
    payload: EngineCatalog::IndexRegistration(RegisteredIndex {
        table: "TerminalSession",
        index_name: "by_started_at",
        key_type: "TimestampNanos",
    }),
}
```

The actual b-tree materialization (scanning rows, populating the
index pages) is internal engine work that doesn't cross a Signal
boundary, so it doesn't need a verb.

### 2.3 · DROP TABLE — `Retract` on the catalog

```rust
Operation {
    verb: SignalVerb::Retract,
    payload: EngineCatalog::TableRegistration(target_table),
}
```

The engine's downstream cleanup (drop the redb sub-table, GC rows,
release the b-tree pages) is internal to the engine, post-commit.

### 2.4 · Schema migration with backfill — `Atomic` over the above

```rust
Operation {
    verb: SignalVerb::Atomic,
    payload: vec![
        // Mark the catalog row as migrating
        Op::Mutate(RegisteredTable::TerminalSession, status: Migrating { from: v3, to: v4 }),
        // Rewrite every existing row under the new shape
        Op::Mutate(TerminalSession { …new shape, derived from old }),  // × N rows
        // Mark the catalog row as active at v4
        Op::Mutate(RegisteredTable::TerminalSession, schema_version: SchemaVersion(4)),
    ],
}
```

Two-phase visibility (`pending → active`) lives in the **catalog
row's typed state machine**, not in a special DDL verb. The schema
version guard in `sema-engine` (per `/158 §3`) reads the catalog
row and refuses operations against a `Migrating` table; that
guarding is engine-internal and doesn't need its own boundary verb.

### 2.5 · Rename a column / change a column type

A sub-case of §2.4. The migration's per-row `Mutate` writes rewrite
the rows under the new field name or type. The catalog row records
the rename so projections from old archives still parse.

### 2.6 · Add a constraint (NOT NULL, UNIQUE, FK) — `Validate` then `Assert`

```rust
Operation {
    verb: SignalVerb::Atomic,
    payload: vec![
        // Dry-run: scan every row against the new constraint
        Op::Validate(SchemaCheck { table, new_constraint }),
        // If pass, assert the constraint row
        Op::Assert(RegisteredConstraint {
            table: "TerminalSession",
            kind: NotNull("session_id"),
        }),
    ],
}
```

`Validate` is exactly the seventh verb's use case — execute as
dry-run, refuse commit on failure. No new verb.

### 2.7 · Online DDL with concurrent traffic

SQL treats this as a special case because relational engines have
row-locks and statement-level visibility. The workspace doesn't:
`sema-engine` is single-writer per daemon. Concurrent traffic queues
behind the `Atomic` commit boundary; the engine's actor runtime
handles it. "Online" is the consumer's UX choice (return
immediately, stream progress via `Subscribe`), not a different
boundary semantic.

---

## 3 · Why this works in the workspace specifically

The case for DDL-as-its-own-verb is grounded in SQL-tradition
assumptions, none of which hold in the workspace:

| SQL tradition | Why DDL is distinct there | Why it isn't distinct here |
|---|---|---|
| Schema lives in a different namespace (`information_schema`, `pg_catalog`) with different access rules | DDL touches a different access path with different concurrency rules | `sema-engine`'s catalog *is* a typed redb table managed by the same actor as every other table — one path, one rule |
| Schema changes take exclusive locks (`ACCESS EXCLUSIVE`) | DDL stalls all readers; needs its own scheduling primitive | `sema-engine` is single-writer per daemon; `Atomic` is the only commit boundary that exists |
| Schema is runtime-typed (`CREATE TABLE T (a INT, b TEXT)`) | The shape of `T` is a runtime artifact; the verb has to carry the shape | Shape is compile-time-typed Rust types declared via `#[derive(NotaRecord)]`. The wire only carries a catalog *announcement*, not the shape itself |

The deepest reason is the third one. In SQL, `CREATE TABLE` is the
only way to make a shape *exist*. In the workspace, the shape exists
because someone wrote a Rust struct in a contract crate. The
catalog entry **announces** that decision — it doesn't **create**
the type. So the "DDL" operation is informational about something
the type system already settled at compile time.

---

## 4 · Convergent evidence from the verb-roots research

The seven-only direction is supported by the four research streams
synthesized in `/162`:

- **Database stream**: schema migration was named as one of ten
  falsifiable pressure points where the closed set might be
  incomplete. The pressure point is *real* in the SQL tradition;
  the question is whether it crosses into workspace traffic.
- **Astrology stream**: Saturn-secondary is *structure-imposition*
  (distinct from `Retract`'s impose-end). The mapping notes
  Saturn-secondary as the home for a possible eighth verb but does
  not force the addition.
- **Workspace archeology stream**: per-component verb-usage
  inventory shows zero current consumers using a DDL-shaped root.
  The workspace's actual traffic doesn't exercise the pressure
  point.
- **Linguistics stream** (indirectly): the verb set is grounded in
  database-operation completeness, not linguistic-universal
  grounds. The argument for or against `Structure` lives in
  engineering pressure, not language-philosophical principle.

The convergent reading: `Structure` is a *named falsifiability
target*, not a commitment. It earns its seat when concrete traffic
forces the question.

---

## 5 · Falsifiability — when the case reopens

Three concrete conditions would reopen the eighth-verb question.
None apply to current workspace traffic. If any fires, this report
retires in favor of a `Structure` (or kindred) proposal.

### 5.1 · Runtime user-defined types

A future component lets end-users define their own record kinds at
runtime — a no-code schema designer, a tenant-isolated multi-schema
service, an LLM-authored typed-table tool. Then the schema *isn't*
compile-time-decided; the wire has to carry the shape itself, not
just an announcement.

The seven-verb absorption depends on shape-as-Rust. Runtime-defined
shapes break that assumption.

**Current workspace state**: no component allows runtime-defined
record types. Consumers register Rust-typed tables at engine start;
the type system is closed.

### 5.2 · Cross-daemon schema consensus

A future Sema runtime distributes one logical database across
multiple writers and schema must agree across them. Then DDL needs
Paxos/Raft-shaped agreement primitives that aren't reducible to
single-writer `Atomic`.

**Current workspace state**: every `sema-engine` consumer is
single-writer (the daemon owns its redb). Cross-daemon
communication happens via Signal frames, not via shared storage.
There is no consensus to schedule.

### 5.3 · Visibility protocols not expressible as a catalog state machine

A schema change requires visibility semantics that the catalog row's
typed state cannot carry. The canonical example: "old readers see
v3, new readers see v4, both concurrent for 10 minutes" with
cryptographic visibility guarantees per reader.

The catalog-row state machine in §2.4 handles two-phase visibility
(`pending → active`) honestly. It does not handle reader-isolated
visibility windows. If those become a wire concern, the catalog row
isn't enough and `Structure` (or kindred) earns its seat.

**Current workspace state**: no consumer requires reader-isolated
schema visibility. Migrations land atomically; consumers see the new
shape post-commit.

### 5.4 · How the trigger fires

If a designer (or operator, or operator-assistant) finds themselves
writing a payload that doesn't honestly fit `Assert`/`Mutate`/
`Retract`/`Atomic` against the catalog table:

1. **Stop.** This is a workspace-level design event per the
   verb-discipline rule.
2. **Test the containment rule.** Can the operation be modeled as a
   catalog state machine? If yes (even if awkwardly), reach for it
   first.
3. **If genuinely not.** Surface the case in a designer report
   naming the specific operation, why the catalog state machine
   doesn't carry it, and what the missing boundary semantic is.
   That report retires this one and motivates the eighth verb.

The rule is "no payload maps to no root" — the failure mode is a
typed proposal for a new root, not a workaround.

---

## 6 · The shape of the argument

The seven-verb case is not "DDL doesn't exist." It is **"DDL isn't
a different *kind of act*; it is the same kinds of act applied to
a different table."**

The verb spine names *what kind of boundary behavior* happens
(durable write, read, streaming lifecycle, transaction boundary,
execution mode). The payload says *what* the boundary behavior
applies to. The catalog table is just another payload target.

When a SQL programmer reaches for `CREATE TABLE`, they are fusing
three operations that the workspace keeps separate: shape
declaration (Rust), storage allocation (engine-internal), and
catalog announcement (wire-visible). The seven verbs only need to
cover the third — and `Assert`/`Mutate`/`Retract`/`Atomic`/
`Validate` already do.

This is the same conceptual move the workspace made when adopting
the seven-root shape over the prior twelve (per `/162 §6`): the
twelve confused vocabulary with roots, the seven restored the
roots-vs-modifiers stratum split. The case against `Structure`
makes the same move: don't add a verb for an operation that's
already expressible inside the existing closed set.

---

## 7 · Adoption

This report is the adopted workspace direction:

1. **`SignalVerb` stays seven.** No `Structure` (or `Define`,
   `Schema`) variant is added.
2. **Schema/catalog operations fit `Assert`/`Mutate`/`Retract`
   under `Atomic`** per the worked examples in §2. The catalog is a
   typed `sema-engine` table.
3. **The schema-version guard** (per `/158 §3`) reads the catalog
   row state; engine-internal, not a boundary verb concern.
4. **The falsifiability triggers in §5** are the conditions under
   which the case reopens. Until then, the seven hold.
5. **The eighth-verb watch-list item in `/162 §9`** is
   superseded by this report: the seven absorb DDL by default; no
   eighth verb is pending.

---

## 8 · See also

- `reports/designer/162-signal-verb-roots-synthesis.md` §4 — the
  containment rule this report formalizes.
- `reports/designer-assistant/50-signal-core-base-verb-shape.md`
  §3, §7 — the seven-root criterion and the original `Structure`
  containment.
- `reports/designer-assistant/51-review-designer-162-signal-verb-roots.md`
  §2.4 — DA's sharper containment framing that motivated this
  report.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` — the
  seven-variant `SignalVerb` enum as landed.
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md` — where
  the catalog table lives and how schema-version guarding works.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the verb-discipline
  rule. The "no payload maps to no root" failure mode in §5.4
  follows this rule.
