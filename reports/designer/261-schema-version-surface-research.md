# 261 — Schema version surface research (Approach C)

*Informed survey of the per-component vs per-record-type question
left open by `/260` after psyche selected Approach C
(in-process versioned reads). Industry parallels first, then the
workspace's actual constraints, then each option in full, then a
recommendation. The psyche selects.*

## What is being chosen

Under Approach C, the daemon stamps a schema-version tag on every
stored record and dispatches read-side on the tag, migrating older
records on read into the current shape. The remaining question is
**what number lives in the tag** — what does the version actually
range over?

- **Per-component**: one counter for the whole `signal-<component>`
  contract. Every record stored by the daemon carries the same
  number. Any contract edit bumps the number; every record type's
  layout is implicitly part of the version.
- **Per-record-type**: each NotaRecord type tracks its own version.
  `Entry` has its own counter; `RecordSubscription` has its own.
  Tags identify a `(type, version)` pair.
- **Layered (both)**: per-record-type machinery in the read path;
  per-component number as a coarse human-facing label and the
  unit a schema-in-NOTA bump operates on.

## Industry parallels — how other systems do this

A quick sweep of the prior art that informs the choice. Each row
is the load-bearing way to read what they're doing, not exhaustive.

**Postgres / Rails / Alembic migrations.** Per-schema timestamp or
serial number. One migration runs the whole database forward
atomically; there's no notion of "this table is at v5 while that
table is at v3". The migration *is* the diff. **Closest analogue:
per-component.**

**Protobuf wire format.** Two layers. The package is informally
versioned (`mypackage.v1`, `mypackage.v2`); messages within a
package evolve via field numbers — adding a field is
wire-compatible because unknown field numbers are tolerated.
**Closest analogue: layered, but the per-record machinery is
implicit through field numbering rather than explicit
versioning.**

**Apache Avro.** Each schema is its own unit, stored separately
in a schema registry. Messages carry a schema-id reference; the
reader picks the writer's schema by id and uses Avro's
reader-vs-writer resolution. **Closest analogue: per-record-type,
with the type-as-schema as the granularity.**

**Cap'n Proto.** Schemas use explicit per-field id numbers; adding
a field with a new id is wire-compatible. Per-struct evolution
via union variants and optional fields. **No explicit version
tag** — compatibility is statically guaranteed by id discipline.

**rkyv.** Zero-copy, layout-dependent. **No built-in versioning.**
Any change to a struct's layout (new field, reordered fields,
changed inner type) means the on-disk bytes can't be read by the
new type. The application has to version itself.

**Event sourcing / CQRS systems** (Akka Persistence, EventStore,
domain-driven shops). Each event type is independently versioned;
"upcasters" lift v1 events to v2, v2 to v3, and so on on read.
The per-event-type model is the established pattern in
event-stream literature. **Closest analogue: per-record-type.**

**Apache Iceberg / Delta Lake** (analytics tables). Table-level
schema versions; old data readable under old schemas, new data
under new. Schema evolution is per-table; the lake has many
tables at different versions concurrently. **Closest analogue:
per-component if "component" maps to "table".**

The pattern of the field: **persistent-data systems with per-row
typed records** tend to version per-record-type (Avro, event
sourcing). **Atomic-migration database systems** (SQL ecosystem)
version per-schema. **Statically-checked wire formats** (Protobuf,
Cap'n Proto) make explicit versioning unnecessary through
field-id discipline.

## Workspace-specific constraints

Three workspace facts constrain the choice in ways the industry
parallels don't quite capture.

**NOTA strictness governs the user-facing text only — not rkyv
storage.** *(Corrected 2026-05-21 per psyche, `intent/signal.nota`
record 28.)* NOTA's positional discipline (from `nota/README.md`:
*"Every declared field appears as a token: omitted trailing
optionals are a typed error"*) applies to the agent-readable wire
text. The migration concern lives one layer down at **rkyv**, the
zero-copy binary format the daemon stores in redb. rkyv carries
*natural headroom* — a bool occupies a byte; a small-variant enum's
discriminator fits in a byte regardless of how many variants are
currently declared. Within that headroom, schema additions are
wire-compatible without migration: adding a fourth unit variant to
a three-variant enum is zero-cost so long as the byte still holds
it and variant order is preserved.

The Cap'n Proto-style structural-compatibility discipline IS
therefore available to the workspace; it just lives at the rkyv
layer, not the NOTA layer. The schema system can identify
zero-cost changes (those that stay within rkyv headroom) from a
schema diff and skip migration on them. This reshapes the
version-surface analysis below — see report `/263` for the deeper
content-addressable schema-layout schema direction this opens.

**aski-core precedent.** The workspace's existing schema-from-NOTA
project (`/git/github.com/LiGoldragon/aski-core`) uses a single
crate-level Cargo version (`0.17.0`) for the whole contract. The
generator `corec` emits one Rust file from many `.core` schema
files into one crate. **The workspace's prior pattern is
per-component.** But aski-core is parse-tree types used at
compile time — there is no persistent on-disk data versioned
against it. The precedent is suggestive, not directly applicable.

**rkyv layout sensitivity.** Persona daemons store rkyv-encoded
payloads in redb. rkyv's zero-copy layout is sensitive to the
exact Rust type: a field reorder, an `Option<X>` becoming a typed
enum, a transparent newtype turning into a struct — any of these
break read-back even when the conceptual schema is "the same". So
the version tag has to bind to *layout-affecting change*, not
just to semantic change. Whatever the version surface, the bump
discipline has to be triggered by any layout edit, not by
intent.

## Option A — per-component, full analysis

One `SCHEMA_VERSION` constant per `signal-<component>` crate. Each
stored record carries the same number. Read path:

```rust
match record.version {
    1 => migrate_v1_to_current(record.payload),
    …
    N => deserialize_current(record.payload),
}
```

**What ships in code.**

- Each `signal-<component>` exports `pub const SCHEMA_VERSION: u32 = N;`
- Each record-storing daemon writes the tag once per record.
- The daemon maintains a chain `migrate_vK_to_vK+1` for every K.
- Historical type definitions live in `schema_v3 { … }`,
  `schema_v4 { … }` modules inside the contract crate.
- A schema bump = one Cargo release that adds a new module,
  bumps the constant, and provides one migration function.

**Pros.**

- **Matches the workspace's component-shape lens.** The contract
  IS the unit; talking about "the contract version" maps cleanly
  to a number. Schema-in-NOTA, if it lands, naturally produces
  one version per generated contract — same shape.
- **Forces explicit migration consideration on every change.** No
  way to silently skip migration work; the constant always bumps;
  the migration step always lands. Layout-sensitivity-by-rkyv is
  caught by the discipline.
- **Single dispatch point per stored record.** The read path is
  one match expression at the top of `Entry::read`,
  `Subscription::read`, etc. Simple to reason about.
- **Composes with aski-core precedent.** If schemas eventually
  generate from `.core`-style files via a `corec`-like generator,
  the natural output is one versioned crate. Per-component is
  what comes out of that machinery without further work.
- **Talkability.** "The spirit contract is at v5" is the way
  humans naturally describe contract evolution.

**Cons.**

- **Bumps cascade across unchanged record types.** Changing only
  `Entry` still bumps the whole contract; `RecordSubscription`'s
  read path goes through a v4→v5 identity migration for no
  semantic reason. The cost is negligible at runtime but creates
  busywork at code-edit time — every unchanged type has to gain
  an identity-migration step.
- **All historical types live together.** `schema_v3`,
  `schema_v4`, `schema_v5` all carry the FULL contract at each
  version. Once a few bumps land, the crate is mostly historical
  code. Eventually pushes toward a sibling
  `signal-<component>-history` crate.
- **One contract version can't capture asymmetric evolution
  rates.** If `Entry` changes every week and `RecordSubscription`
  never changes, they nonetheless travel in lockstep through
  contract versions. Conceptually noisy, even if mechanically
  fine.

## Option B — per-record-type, full analysis

Each NotaRecord type carries its own version constant. Stored
records embed the tag as `(type_id, version)` or use a
type-keyed table layout in redb. Read path dispatches on the
record's own type-tag pair.

```rust
impl Entry {
    pub const VERSION: u32 = 3;
    pub fn read_versioned(bytes: &[u8], version: u32) -> Self {
        match version {
            1 => migrate_entry_v1_to_v3(deserialize_v1(bytes)),
            2 => migrate_entry_v2_to_v3(deserialize_v2(bytes)),
            3 => deserialize_current(bytes),
            _ => panic!(),
        }
    }
}
```

**What ships in code.**

- Each NotaRecord declares its own `VERSION` const (or a derive
  emits it).
- Stored records embed the version tag per type.
- Migration code lives next to the type — `Entry`'s migration
  chain is in `Entry`'s file.
- Bumping `Entry` from v2 to v3 doesn't touch
  `RecordSubscription`.

**Pros.**

- **Change locality.** A change to `Entry` bumps only `Entry`;
  unchanged types stay at their last version. Code edits
  proportional to actual change, not to time elapsed.
- **Fine-grained migration code.** Per-type read function carries
  its own migration chain — the migration for `Entry` doesn't
  need to know about `Subscription`'s evolution. Each
  migration is small and reads cleanly.
- **Matches event-sourcing intuition.** "An event has a type and
  a version" is the language of CQRS / event streams. Persona
  daemons store record streams; the analogy is direct.
- **No "identity migration" busywork.** Unchanged types literally
  don't change; no v4→v5 noop migrations to write.

**Cons.**

- **Transitive layout dependence is sneaky.** When `Topic` (a
  NotaRecord) adds a variant, every type that embeds `Topic`
  silently has its rkyv layout shifted — even though those
  types' own field set didn't change. Per-record-type discipline
  has to chase this transitively: if `Topic` bumps, every type
  with a `Topic` field also bumps. **Easy to miss; failure
  surfaces as a deserialise crash.**
- **More bookkeeping.** Each NotaRecord type owns a constant;
  bumps require touching the type's source. A schema with
  20 stored types has 20 version constants to keep current.
  Auto-derive can help (a `NotaVersioned` derive that the
  generator emits), but the surface grows with the schema.
- **Migration coordination across types is implicit.** If a
  contract edit changes `Entry` AND `Topic`, the two bumps are
  two separate migrations; the daemon has to apply them
  consistently. Per-component would have one migration covering
  both.
- **"What version is the contract?"** has no clean answer.
  Talkability drops: humans want to say "spirit is at v5", not
  "Entry v3, Subscription v1, Topic v2". The lack of a coarse
  label hurts cross-agent / cross-session communication.

## Option C — layered (per-component label + per-record-type machinery)

The layered shape carries both: each `signal-<component>` exports
a coarse `CONTRACT_VERSION` (the human-facing number, bumped on
any change), AND each NotaRecord carries a fine `VERSION` (the
read-path dispatch number).

```rust
impl signal_persona_spirit {
    pub const CONTRACT_VERSION: u32 = 7;  // bumps on any contract edit
}

impl Entry {
    pub const VERSION: u32 = 3;  // bumps only on Entry layout change
    // read-path dispatch uses Self::VERSION
}
```

**What ships in code.**

- Contract carries `CONTRACT_VERSION`; record types each carry
  their own `VERSION`.
- Stored records use the per-type version for dispatch.
- The contract version is a *label* — used in handshakes,
  schema-in-NOTA file headers, contract docs — not by the read
  path.
- Optional: a static assertion that `CONTRACT_VERSION` ≥
  `max(every record's VERSION)` to catch forgotten bumps.

**Pros.**

- **Composes both axes.** The per-record-type machinery gives
  change-locality and clean migration code; the per-component
  label gives talkability and matches the aski-core /
  schema-in-NOTA shape.
- **Schema-in-NOTA fit.** A NOTA schema file naturally carries a
  contract version in a header; the per-type versions can be
  emitted from the schema itself (each `.core`-style declaration
  carries a version). The two layers come for free from the
  generator.
- **Backwards-only enforcement is possible.** A lint that
  `CONTRACT_VERSION` only ever bumps when at least one
  type's `VERSION` bumped catches "documentation changes
  miscategorised as contract bumps".

**Cons.**

- **Two surfaces to maintain.** Discipline drift is twice as
  likely; the per-component number could go stale while
  per-record-type numbers stay current, or vice versa.
- **The contract number is decorative.** It doesn't drive any
  machinery; its only consumers are humans and schema-in-NOTA
  headers. That's a real benefit but a softer one than the
  per-record-type machinery delivers.
- **Slightly more code to write for each bump.** Both numbers
  bump (when a record changes); the static assert catches
  inconsistency at compile time but is still an extra step.

## The decisive concrete fork

The three options collapse to one practical question: **does the
daemon ship migration code per-type, or one big migration per
contract bump?**

- Per-type means option B or C — the read path forks by
  `(type, version)` and migration code lives next to the type.
- Per-contract means option A — the read path forks by
  `(contract, version)` and migration is one omnibus function.

Everything else (the talkability label, the schema-in-NOTA fit,
the precedent) is downstream of that fork.

## Recommendation

**Option C, layered**, with caveats.

The per-record-type machinery (the real benefit) is what makes
change locality possible and matches the natural shape of a
persona daemon's stored data (per-record streams of typed
domain events). Event sourcing's per-event-type pattern has
decades of production evidence behind it; the failure modes
are well-understood and the migration code stays small. The
workspace will eventually want this property.

The per-component label (option A's benefit) costs almost
nothing additional once the per-record-type machinery is in
place — one `CONTRACT_VERSION` constant per `signal-<component>`,
bumped together with whichever type's `VERSION` triggered the
contract edit. The label gives talkability and slots cleanly
into the schema-in-NOTA proposal's NOTA schema file headers.

The only real reason to choose pure-A over layered-C is if the
workspace prefers the discipline of "every change forces every
type to consider migration" — under per-component, an unchanged
type still gets its identity migration written, which can catch
sneaky transitive layout changes (a `Topic` variant addition
that nobody noticed shifted `Entry`'s layout). That's a real
safety net. The layered shape compensates with the static-assert
discipline that catches the inverse failure (forgetting to bump
the type when its layout depends on a changed dependency); the
discipline is just at a different place.

**Practical pilot for spirit**:

1. `signal-persona-spirit` adds `pub const CONTRACT_VERSION: u32 = 1;`
2. Each NotaRecord type adds `pub const VERSION: u32 = 1;`
   (mechanical; could be auto-derived later).
3. Stored payloads embed the per-record version (prefix byte or
   field, designer follow-up to pick).
4. Read path dispatches per-type on the embedded version.
5. The first real schema change — likely soon, given operator
   activity — pilots the bump-and-migrate flow on whichever type
   changed.

The aski-core / corec precedent suggests the per-record-type
versions can eventually be generator-emitted from the NOTA
schema files (each schema declaration becomes a versioned type).
That's the long-term path, downstream of the schema-in-NOTA
thread.

## What stays open

- **The wire encoding of the version tag.** Prefix byte? Field on
  every NotaRecord (`version: u32`)? rkyv-side mechanism vs
  application-side? Designer follow-up.
- **Where historical type modules live.** Same as `/260` Q2 —
  inside `signal-<component>` or in a sibling
  `signal-<component>-history` crate. Likely the former until
  the module tree gets noisy.
- **Owner-channel symmetry.** Owner contract data has different
  recovery characteristics; treat the same as the working
  contract, or differently (bootstrap from policy file)?
  Probably a dedicated follow-up report.

## References

- `reports/designer/260-schema-migration-discipline.md` — the
  Approach C selection that this report drills into.
- `intent/component-shape.nota` 2026-05-21 record 21 — the
  Approach C decision.
- `intent/signal.nota` 2026-05-21 record 12 + 20 — the
  schema-in-NOTA proposal and its aski-core grounding.
- `/git/github.com/LiGoldragon/aski-core` — workspace prior art
  on schema-from-NOTA via the `corec` generator. Uses
  per-component (per-crate) versioning. Parse-tree types only;
  no on-disk persistence.
- `/git/github.com/LiGoldragon/askic` — aski-core's evolving
  successor; same pattern, version 0.18.0.
- `/git/github.com/LiGoldragon/nota` — README §"Records" carries
  the strict positional rule and the no-tail-omission
  constraint that pushes the workspace toward explicit
  versioning.
- Industry references (general programming knowledge, not
  workspace artefacts): Protobuf field-numbering, Apache Avro
  schema registry, Cap'n Proto unique-id fields, rkyv layout
  semantics, Akka Persistence event upcasters, Apache Iceberg
  table evolution.
