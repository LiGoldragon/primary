# 273 - Schema migration synthesis after operator/151

*Designer synthesis, 2026-05-21. Operator/151 landed a real
implementation proposal responsive to /260 and /261; it carries two
refinements the designer-side picture foreshadowed but did not pin
down. This report absorbs both and reconciles operator/151's per-
component `spirit-migrate` shape with /270's universal sema-upgrade
triad. Audit /272 §5c item 1 flagged this as the first of two
recommended follow-ups.*

## 1. Why this report

Operator/151 (2026-05-21 15:13) is a working implementation proposal:
`v0.1.0` tags pushed across `persona-spirit`, `signal-persona-spirit`,
`owner-signal-persona-spirit`, plus matched LiGoldragon dependency
revisions; a concrete deployed-vs-current diff at storage and signal
layers; a per-component module layout
(`persona-spirit/src/schema/{current,version_1}.rs` plus
`migration/version_1_to_2.rs`); a one-shot `spirit-migrate`
maintenance binary consuming the same migration library the daemon
itself uses. Two refinements deserve first-class designer-side
framing because they are general, not Spirit-specific:

1. **Type-family split.** Public-signal historical types and
   private-storage historical wrappers are two distinct record sets,
   owned by two different crates, both tracked by the schema-
   migration discipline. /260 foreshadowed this; /261's per-record-
   type recommendation accepted it implicitly without naming the
   two-family axis.
2. **Commit-sequence high-water mark.** Any live-copy cutover
   protocol needs a durable high-water mark, taken at copy-snapshot
   time and re-read at switch time, to detect writes between
   snapshot and switch. The mark belongs at the sema-engine pressure
   point — sema-engine is the universal commit point for every
   persona daemon's sema database (intent record 72's sema database
   vocabulary).

Both widen the picture. Neither contradicts /260, /261, /263, /269,
or /270; both pin down dimensions left implicit.

## 2. The type-family split

/260 named the dual-axis problem (wire contract plus storage schema)
but stopped at the conceptual layer. /261's per-record-type machinery
framed versioning as "each NotaRecord type" without distinguishing
where those types live. Operator/151's deployed-Spirit read forces
the split explicit.

### 2a. What actually lives on disk

The deployed Spirit daemon stores not the public signal `Entry`
directly but a runtime-only wrapper tree:

```rust
struct StoredRecord {
    identifier: RecordIdentifier,
    entry: StampedEntry,
}
pub struct StampedEntry {
    entry: Entry,        // public signal type
    date: Date,          // public signal type
    time: Time,          // public signal type
}
```

`StoredRecord` and `StampedEntry` are private to `persona-spirit`
(the runtime crate); table keys, table names, and indexing payloads
similarly. None are wire-visible. But all are rkyv-encoded into the
redb database, participate in on-disk layout, and break read-back
when their Rust types change.

| Type family | Natural owner | Visibility | Examples |
|---|---|---|---|
| Public-signal historical types | `signal-<component>` + `owner-signal-<component>` | Wire-visible | `Entry`, `RecordQuery`, `Magnitude`, `Observation` |
| Private-storage historical wrappers | `<component>` runtime crate | Daemon-internal | `StoredRecord`, `StampedEntry`, table keys |

Both families need historical record sets under Approach C and
participate in /263's layout-bound annotations. Both are leaves at
the schema-language level — the family distinction is a property of
where each leaf gets generated, not of its shape.

### 2b. Why the split matters for sema-upgrade

Sema-upgrade's `Inspect` reply (/270 §3b) reports a schema-address.
That address must bind to **the full set of layout-affecting types
the daemon depends on** — the union of working-contract types,
policy-contract types, *and* runtime private storage wrappers. A
schema-address capturing only public-signal types would miss layout
drift in `StoredRecord` or `StampedEntry`; a daemon with a new
private wrapper could open the prior daemon's database and crash on
decode.

The /263 diff classifier reads schemas at the language layer.
Nothing in /263 forbids declaring private-storage record types in
the same artefact as public-signal types. What the language gains
is a **visibility annotation** — each top-level `Record` declaration
carries `(public)` or `(private)` so the classifier and generator
know which crate to emit the type into. The component schema is the
union; the schema-address is its canonical hash.

### 2c. Implication for /260 and /261

Neither needs `-v2`. /260 reads with the family split already
implicit ("the rkyv layout of the payloads it stores"). /261's
per-record-type machinery already supports two families — each
NotaRecord carries its own version regardless of crate. The split
is a clarification, not a contradiction. Sema-upgrade absorbs it
into its content-address discipline.

## 3. The commit-sequence high-water mark

/270 §5 sketched the daemon-at-boot upgrade flow assuming the daemon
is **not serving traffic during migration**. Stop-old-start-new does
not need a high-water mark. Live-copy cutover with writes in flight
does. Operator/151 §"Does copy-migrate-verify-switch make sense?"
introduces it as the missing primitive.

### 3a. The protocol and the failure mode

Copy-migrate-verify-switch: snapshot the running sema database at
sequence `S0` while the old daemon serves; migrator copies and
transforms the snapshot into the new schema; before switching, re-
read the old daemon's current sequence `S1`. If `S1 == S0`, stop
the daemon and install the migrated copy atomically; if `S1 > S0`,
retry or replay the delta `(S0, S1]` against the migrated copy.

Without a durable monotonic sequence at the sema-engine layer, the
verify step cannot answer "did any writes happen since snapshot".
A weak proxy — `max(RecordIdentifier)` for Spirit's append-only
stream — works only for append-only data with monotonic identifiers
and does not generalise to mutation, retraction, owner-channel
policy state, or subscription mutation. Operator/151 bounds the
proxy to today's Spirit shape.

### 3b. Where it lives - sema-engine

The mark belongs at the **sema-engine pressure point**. Every
committed effect already passes through sema-engine; advancing a
monotonic counter alongside each commit is the minimal intrusion.
The counter is durable, survives daemon restart, and advances in
commit order regardless of which contract leg issued the effect.

Concrete shape: sema-engine maintains `CommitSequence` (initial 0,
+1 atomically per commit); the database exposes
`current_commit_sequence()` every daemon consults; the migrator
reads the sequence at snapshot time and again at the cutover gate;
sema-upgrade's working contract gains
`(operation AskCommitSequence ((Component …)))` with reply
`(SequenceReported ((Component …) (Sequence u64)))`.

The sequence is **not** the schema-address. The address identifies
the type-layout shape; the sequence identifies the data volume.
Both are needed: address tells the migrator *what to migrate*,
sequence tells *whether the source moved underneath the snapshot*.

### 3c. Today's Spirit and the future

Spirit today has no commit-sequence machinery. The first migration
can use stop-old-start-new without live-copy cutover. The commit-
sequence is a **necessary predecessor** to any live-copy protocol;
it belongs in sema-engine before any persona daemon attempts zero-
downtime migration with writes in flight — a new constraint on
sema-engine's roadmap. /270 §9 question 7 (idempotent re-run)
flagged the related partial-replay concern; the commit-sequence is
its substrate.

## 4. Reconciling operator/151 with /270

Operator/151 proposes a per-component Spirit layout
(`persona-spirit/src/{schema,migration}/...`, `spirit-migrate`
binary). /270 proposes a universal triad orchestrating migrations
across every persona daemon. These shapes are not in tension; they
name two different concerns.

### 4a. The clean carve-up

| Concern | Owner |
|---|---|
| Pure migration functions (per-record-type transforms) | `<component>` library modules (operator/151's layout) |
| Historical public signal record definitions | `signal-<component>` + `owner-signal-<component>` |
| Historical private storage wrappers | `<component>` runtime crate |
| Read-time lifting in daemon (Approach C) | Daemon, calling the same per-component library |
| Eager full-copy migration | sema-upgrade triad, driving the per-component library |
| Owner approval, throttle, quarantine, schema catalogue | sema-upgrade owner contract |
| Commit-sequence high-water mark | sema-engine (universal); exposed via sema-upgrade |

Operator/151's `spirit-migrate` is not retired; it is reframed. The
per-component library *is* the migration code; what changes is who
calls it. Two valid surfaces remain — daemon read-path call (read-
time lift) and sema-upgrade orchestrator call (eager full-copy).
Operator/151's binary becomes either (1) a thin Signal client of
sema-upgrade forwarding a `Migrate` request — same shape as
`upgrade` CLI; or (2) a boot-time in-process library call where
sema-upgrade calls Spirit's migration library through linkage at
daemon start. Both preserve operator/151's `src/schema/` and
`src/migration/` layout. **Designer lean: (2) in-process library.**
/270 §9 question 1's reason holds — triad invariant 2 is preserved
by linkage rather than foreign-database open.

### 4b. Plan vs transform

The **plan** is what sema-upgrade computes from a schema-address
diff — data, a tree of typed steps (zero-cost, append-only,
structural) per /263. The **transform code** is the per-record-type
Rust function the per-component library exports — pure functions
mapping a prior-version record to a current-version record. A plan
step says "lift `StoredRecord` from `A0` to `A1`"; the executor is
`lift_stored_record_v1_to_v2`. Sema-upgrade dispatches; the per-
component library performs. Plans are generated; transform code is
hand-written (generator-emitted later once /263's generator lands).

### 4c. Owner authority

Operator/151 does not address owner approval. /270's owner contract
carries `ApprovePlan` / `RejectPlan` / `Quarantine`. Migration via
sema-upgrade gains owner authority by default; a standalone
`spirit-migrate` would bypass it. The universal orchestrator is the
universal authority surface; Spirit's per-component library has no
business reasoning about approval.

## 5. Updated implementation picture

The next operator slice is one of two equivalent shapes.

**Shape A — sema-upgrade triad first.** Create the triad with /270's
wire surface; add `current_commit_sequence()` to sema-engine and
expose via `AskCommitSequence`; implement `Inspect` returning
`Proceed` for matching addresses (today: every deployed daemon);
land Spirit's identity migration library (`version_1_to_1` exists
for the first real migration); first real migration is a sema-
upgrade plan plus a Spirit library function pair.

**Shape B — per-component library first.** Land Spirit's
`src/schema/current.rs` (frozen `v1` plus `version_1_to_1` identity);
add `current_commit_sequence()` to sema-engine; defer sema-upgrade
until a second persona-daemon needs migration; sema-upgrade later
wraps the existing library as canonical caller.

Both converge. **Designer lean: Shape A.** Sema-upgrade is universal
infrastructure; once it exists, every subsequent migration pays a
fixed cost (define schema, hand-write transform) instead of
inventing migration machinery per component. The sema-engine commit-
sequence work is needed under either shape and should land first.

## 6. Open questions worth psyche input

**6a. Schema visibility annotation in /263.** Does the language gain
`(public)` / `(private)` annotations on top-level `Record`, or is
visibility inferred from which schema file the type appears in?
Designer lean: **annotation**, because a single canonical schema
artefact per component is cleaner than splitting across files.

**6b. Commit-sequence scope.** Per-component (each daemon has its
own) or per-database (sema-engine maintains one sequence per
database)? Operator/151 implies per-component; sema-engine's
universal-pressure-point shape suggests per-database. The latter is
simpler. Designer lean: **per-database**.

**6c. Single-deploy-stack readiness for first migration.** Is the
first production migration allowed the simple cutover (write-free
window, single-user Spirit case acceptable)? Operator/151's open-
questions section asks the same. Designer lean: **allow stop-old-
start-new for the first production migration**; land commit-sequence
work in parallel for the second.

**6d. Per-component historical-types module layout.** In-tree
`schema_v1`, `schema_v2`, ... inside `signal-<component>`, or sibling
`signal-<component>-history` crate? /261 left this open; operator/151
implicitly chose in-tree. Designer lean: **in-tree module** until
the historical tree grows load-bearing.

## 7. References

**Reports.** `reports/designer/260-schema-migration-discipline.md` —
Approach C selection; the kickoff this synthesis builds on.
`reports/designer/261-schema-version-surface-research.md` — layered
shape recommendation the type-family split refines.
`reports/designer/263-schema-specification-language-design.md` —
schema language; site of the proposed visibility annotation in §6a.
`reports/designer/269-universal-magnitude-type-design.md` —
`Magnitude` final leaf; cross-component signal type schema-migration
must track. `reports/designer/270-sema-upgrade-component-design.md`
— universal sema-upgrade triad; the orchestrator operator/151's
per-component library composes under.
`reports/operator/151-spirit-deployed-version-and-schema-migration.md`
— operator's implementation proposal; source of the two refinements
this report absorbs.
`reports/designer/272-audit-of-operator-state-2026-05-21.md` — audit
naming this synthesis as the first of two recommended follow-ups
(§3a, §5c item 1).

**Intent records.** Record 21 (`intent/component-shape.nota`) —
Approach C selection. Record 72 — sema database vocabulary; sema-
engine as universal commit point. Record 73 — NOTA branches/leaves
vocabulary; basis for closed-set types as final leaves.

**Workspace artefacts.** `skills/component-triad.md` — triad
invariants relevant to §4's carve-up. `skills/nota-design.md` —
NOTA positional-record discipline underlying /263's syntax.
