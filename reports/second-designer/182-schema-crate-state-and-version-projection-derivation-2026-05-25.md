*Kind: Research + Walkthrough · Topic: schema crate current state + concrete BEFORE/AFTER + how upgrade macro would derive projection · Date: 2026-05-25 · Lane: second-designer*

# 182 — Schema crate state + how a schema diff derives a version projection

## §1 Frame

Per psyche directive 2026-05-25: "we haven't really looked at schema in detail. We need to look at schema and how it's not actually spec'd out properly, I think. I put an operator on it, but yeah, I don't think the schema is really deriving its data from nota format directly right now, if there's anything there, if there's any actual semi-real code there even at all. So I want to know what the situation is on that."

Plus: "the macro is in the code, deriving the code from the schema difference, which actually we have to look at some examples of that, like here's the schema before, here's the schema change, how is that going to translate".

Resolved /181 §3 open question (a): macro decides projection module location; not a big deal — captured as intent 587.

This report answers: (1) what's actually IN the schema crate today; (2) the concrete Spirit v0.1.0 → v0.1.1 schema diff; (3) how the macro WOULD derive the projection from that diff; (4) the smallest MVP to make it real.

## §2 The schema crate IS real — not skeleton

`/git/github.com/LiGoldragon/schema/src/` has 17 source files (~5K LoC total). Real working code, not stub:

| File | Role | Status |
|---|---|---|
| `parser.rs` | `Schema::parse_str(input) -> Result<Schema>` consumes `nota_codec::Decoder` | WIRED — actual NOTA parser, not builder-only |
| `reader.rs` | `LoadedSchema::read_path(path) -> Result<Self>` loads file, recursively resolves imports, detects cycles via `BTreeSet<PathBuf>` | WIRED |
| `document.rs` | `Schema { imports, ordinary_header, owner_header, sema_header, namespace, features }` + `assemble(&[resolutions]) -> Result<AssembledSchema>` | WIRED |
| `assembled.rs` | `AssembledSchema { imports, routes, types, features }` + `plan_upgrade_from(&self, previous: &Self) -> Result<UpgradePlan>` | WIRED |
| `upgrade.rs` | 7 projection kinds (Identity/Standard/Annotated/Added/Renamed/Dropped/Untranslatable) + `UpgradeAnnotation` enum | WIRED |
| `engine.rs` | 5 `BuiltinSchemaMacro` variants (Import/Header/Type/Feature + one more); `LoweringContext` | WIRED |
| `declaration.rs` | `DeclarationBody::{Enum, Newtype, Record, Alias}` + `SchemaField { name, schema_type }` per operator/180 | WIRED — field names preserved per operator/180 |
| `import.rs` | `ImportDirective::{Import, ImportAll}`, `Imports`, `SchemaPath` | WIRED |
| `header.rs` | `Header { roots: Vec<HeaderRoot> }`, `HeaderRoot { name, endpoints }` per operator/174-v5 uniform form | WIRED |
| `feature.rs` | `Feature::{Reply, Event, Observable, Upgrade}` | WIRED |
| `expression.rs` | `TypeExpression::{Primitive, Named, Container(Vec/Option/Map)}` | WIRED |
| `layout.rs` | `Layout::for_declaration` (still pre-assembly — known gap per /171 §4.3) | PARTIAL — gap noted |

**The schema-crate-isn't-real concern is unfounded.** Parser is real, reader is real, AssembledSchema is real, plan_upgrade_from is real. **What's NOT real is the MACRO that emits Rust code from AssembledSchema** — that's the brilliant macro library's `signal_channel!([schema])` proc-macro, which today emits wire types + codecs + dispatch (per operator/180 + designer/333 §5) but does NOT yet emit `VersionProjection` impls. THAT's the gap.

## §3 Concrete BEFORE/AFTER — Spirit v0.1.0 vs v0.1.1

### §3.1 v0.1.0 schema (frozen at `signal-persona-spirit/schemas/v0.1.0/schema.nota`)

```
[
  (Operation
    (State Statement)
    (Record Entry)
    (Observe Observation)
    (Watch Subscription)
    (Unwatch SubscriptionToken))

  (Kind Decision Principle Correction Clarification Constraint)
  (Certainty Maximum Medium Minimum)

  (Topic (Topic String))
  (Summary (Summary String))
  (Context (Context String))
  (Quote (Quote String))
  (StatementText (StatementText String))

  (Entry (Entry Topic Kind Summary Context Certainty Quote))
  (Statement (Statement StatementText))
]
```

Note the OLD schema shape: single flat vector of records; no 6-position structure; newtypes carry their own name twice `(Topic (Topic String))`; records positional `(Entry (Entry Topic Kind Summary Context Certainty Quote))`. **`Certainty` enum is the load-bearing type that becomes `Magnitude`.**

### §3.2 v0.1.1 schema (current at `signal-persona-spirit/spirit.schema`)

```
{
  Magnitude (ImportAll schemas/signal-sema/magnitude.schema)
  SemaSet (Import schemas/signal-sema/sema.schema [SemaOperation SemaOutcome SemaObservation])
}

[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
  (Watch [Subscription])
  (Unwatch [SubscriptionToken])
]

[]

[]

{
  State [(Statement Statement)]
  Record [(Entry Entry)]
  Observe [(Observation Observation)]
  Watch [(Subscription Subscription)]
  Unwatch [(SubscriptionToken SubscriptionToken)]

  Kind [Decision Principle Correction Clarification Constraint]
  ObservationMode [SummaryOnly WithProvenance]
  ...

  Topic (String)
  ...

  Entry ((topic Topic) (kind Kind) (summary Summary) (context Context) (certainty Magnitude) (quote Quote))
  Statement ((text StatementText))
  ...
}
```

Note the NEW schema shape: 6-position structure; **`Magnitude` IMPORTED from signal-sema** (cross-component refactor); per-leg headers; explicit field names `(certainty Magnitude)` per operator/180; newtypes simpler `Topic (String)`.

## §4 The schema DIFF mapped to the 7 projection kinds

Running `next_assembled.plan_upgrade_from(&previous_assembled)` would produce these projections (approximately — assuming v0.1.0 is loaded via the same parser, which requires some adaptation since v0.1.0 isn't 6-position):

| Type in v0.1.1 | Was in v0.1.0 | Projection kind | Note |
|---|---|---|---|
| `Kind` enum | identical | `Identity` | No transformation needed |
| `Magnitude` enum (from signal-sema) | `Certainty` (local in v0.1.0) | `Renamed { current: Magnitude, previous: Certainty }` | **Requires `(RenamedFrom Certainty)` annotation in v0.1.1's Upgrade feature** |
| `Topic` newtype | `Topic` newtype (different shape) | `Identity` | rkyv-level format equivalent (both wrap String); field-name change is Rust-level only |
| `Summary`, `Context`, `Quote`, `StatementText` | same | `Identity` | Same as Topic |
| `Entry` record | `Entry` record (positional → named, `Certainty` → `Magnitude` field) | `Standard { kind: ContainerEmbed }` (per intent 561) OR `Annotated { Migrate }` | Field types changed (Certainty→Magnitude); structural shape equivalent |
| `ObservationMode`, `Presence`, `UnimplementedReason`, `FocusArea`, etc. | not present | `Added` | New types; no migration needed |
| `RecordSummary`, `RecordProvenance`, `TopicCount`, `QuestionSummary` | not present | `Added` | New types |
| `State [(Statement Statement)]` (Record/Observe/Watch/Unwatch namespace enums) | same logical operations, different syntactic shape | structural rather than data — handled by header lowering, not VersionProjection | |

**The load-bearing data-shape change is `Certainty → Magnitude`** — a one-variant-per-variant identity rename (`Maximum→Maximum, Medium→Medium, Minimum→Minimum`). That's the single From impl /324 §7 names. Everything else is either pure additions or structural reshuffling that doesn't require record migration.

## §5 What the macro WOULD emit (canonical pattern from hand-written reference)

The existing hand-written projection at `upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:100-318` IS the canonical output shape. The pattern:

```rust
mod historical {
    use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};
    use sema_engine::{EngineRecord, RecordKey};

    // private rkyv reproduction of v0.1.0 types — every leaf
    #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
    pub struct Topic(String);
    impl Topic { pub fn new(value: impl Into<String>) -> Self { Self(value.into()) } /* ... */ }

    #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, Copy, PartialEq, Eq, Hash)]
    pub enum Certainty { Maximum, Medium, Minimum }

    #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
    pub struct Entry {
        pub topic: Topic,
        pub kind: Kind,
        pub summary: Summary,
        pub context: Context,
        pub certainty: Certainty,  // OLD type
        pub quote: Quote,
    }

    #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
    pub struct StoredRecord {
        pub identifier: RecordIdentifier,
        pub entry: StampedEntry,
    }
    // ...
}

mod current_shape {
    // current types with explicit From impls for the changed fields
    impl From<historical::Certainty> for signal_sema::Magnitude {
        fn from(value: historical::Certainty) -> Self {
            match value {
                historical::Certainty::Maximum => signal_sema::Magnitude::Maximum,
                historical::Certainty::Medium => signal_sema::Magnitude::Medium,
                historical::Certainty::Minimum => signal_sema::Magnitude::Minimum,
            }
        }
    }

    impl From<historical::Entry> for signal_persona_spirit::Entry {
        fn from(value: historical::Entry) -> Self {
            Self {
                topic: value.topic.into(),
                kind: value.kind.into(),
                summary: value.summary.into(),
                context: value.context.into(),
                certainty: value.certainty.into(),  // Certainty -> Magnitude
                quote: value.quote.into(),
            }
        }
    }

    impl From<historical::StoredRecord> for signal_persona_spirit::StoredRecord {
        fn from(value: historical::StoredRecord) -> Self { /* field-by-field From */ }
    }
}

pub fn migrate_paths(source: &Path, target: &Path) -> DatabaseMigrationResult<ModuleResult> {
    let records = read_historical_records(source)?;
    write_current_records(target, records)  // calls historical -> current_shape From impls
}
```

This pattern is what the MACRO should emit. The information needed:
- v0.1.0 type shapes (from v0.1.0 AssembledSchema; rkyv derives bolted on)
- v0.1.1 type shapes (from current crate's compiled types — already available since we're emitting INTO the current crate)
- The rename annotation: `(Upgrade (RenamedFrom Magnitude Certainty))` in v0.1.1's features
- The migration table descriptor: `RECORDS` is the redb table name; comes from `(Storage [(Records StoredRecord)])` once Storage variant lands (/181 §6)

## §6 What's missing for derivation — three concrete gaps

1. **The `Upgrade` feature variant body shape isn't fully spec'd** — `Feature::Upgrade(Upgrade { from_version: Version, annotations: Vec<UpgradeAnnotation> })` exists per `schema/src/upgrade.rs` but the SCHEMA-LEVEL syntax for writing `(Upgrade (FromVersion 0 1 0) (RenamedFrom Magnitude Certainty) ...)` in NOTA isn't fully defined or tested. Operator's /180 added `SchemaField` for record fields but the Upgrade feature's NOTA grammar hasn't been exercised yet. Concrete need: write a minimal `(Upgrade ...)` block in `spirit.schema` and confirm `parser.rs::parse_features` accepts it.

2. **The macro doesn't yet have an `UpgradeMacro` variant** in `engine.rs`'s BuiltinSchemaMacro enum. Per /181 §3, this is the MVP slice that adds:
   - `UpgradeRuleInput { previous_schema: AssembledSchema, current_schema: AssembledSchema, annotations: Vec<UpgradeAnnotation> }`
   - `UpgradeMacro` BuiltinSchemaMacro variant
   - Code generator that walks `UpgradePlan` projections and emits the historical + current_shape + migrate_paths pattern

3. **Loading v0.1.0 schema requires shape-adaptation** — v0.1.0's flat-vector NOTA isn't 6-position. Either v0.1.0 needs to be CONVERTED to 6-position retroactively (mechanical transformation; preserves semantics), OR the parser needs a v0.1.0-specific entry point that knows the old shape. Lean: convert v0.1.0 to 6-position (one-shot mechanical edit), preserve the .nota file as a historical artifact, future schemas all use 6-position. This means `Schema::parse_str` only ever needs to parse one grammar.

## §7 The MVP path — three steps, sequenceable

**Step 1**: convert `signal-persona-spirit/schemas/v0.1.0/schema.nota` to 6-position shape, preserving semantics. ~30 minutes of mechanical edit:

```
{}
[(Operation (State Statement) (Record Entry) (Observe Observation) (Watch Subscription) (Unwatch SubscriptionToken))]
[]
[]
{
  Kind [Decision Principle Correction Clarification Constraint]
  Certainty [Maximum Medium Minimum]
  Topic (String)
  Summary (String)
  Context (String)
  Quote (String)
  StatementText (String)
  Entry ((topic Topic) (kind Kind) (summary Summary) (context Context) (certainty Certainty) (quote Quote))
  Statement ((text StatementText))
}
[]
```

Then `Schema::parse_str(v0.1.0_text).unwrap()` succeeds; `.assemble(&[])` returns AssembledSchema for v0.1.0.

**Step 2**: add `(Upgrade (FromVersion 0 1 0) (RenamedFrom Magnitude Certainty))` to `spirit.schema`'s features section. Run `Schema::parse_str(v0.1.1_text)?.assemble(...)?.plan_upgrade_from(&v0.1.0_assembled)?` — confirm it produces a `Renamed { current: Magnitude, previous: Certainty }` projection without erroring.

**Step 3**: add `UpgradeMacro` BuiltinSchemaMacro variant + code generator (per /181 §3). Hand-write the generator for the 7 projection kinds; emit the historical + current_shape + migrate_paths Rust code. Verify byte-equivalent to the existing hand-written `version_0_1_0_to_0_1_1.rs:100-318`.

Estimated effort: Step 1 = 30 min; Step 2 = 1-2 hours (likely surfaces grammar gaps that need closing); Step 3 = 1-2 sessions (the generator IS the schema engine's largest new emit-side capability).

## §8 Open psyche question (the truly-uncertain remainder)

Just one — and even this has a lean.

**Q**: should the historical-types module live in the COMPONENT'S crate (`signal-persona-spirit/src/historical_v0_1_0.rs` — colocated with current types) or in the UPGRADE crate (`upgrade/src/migrations/persona_spirit/historical.rs` — current pattern)? **Lean: keep current pattern (upgrade crate)** — the historical types are only needed at migration time; component crate shouldn't carry them. The macro emits INTO the upgrade crate, not the component crate. Confirm direction?

## §9 What this report changes about the situation

The pessimistic framing ("schema isn't really deriving its data from nota") is HALF-RIGHT and HALF-WRONG:
- **HALF-RIGHT**: the proc_macro `signal_channel!([schema])` doesn't yet emit VersionProjection from schema diffs. That's the largest hand-written deviation per /176 §13 + /333 §13.
- **HALF-WRONG**: the schema CRATE itself has a real working NOTA parser + assembler + diff algorithm. The crate is not a sketch.

The remaining work IS macro emission of the projection code. The schema substrate is solid. /181 §3 (UpgradeMacro variant) is the right MVP slice; this report sharpens it with concrete BEFORE/AFTER + concrete generator pattern.

## §10 References

- `/git/github.com/LiGoldragon/schema/src/parser.rs` — actual NOTA parser
- `/git/github.com/LiGoldragon/schema/src/reader.rs` — file loader with import cycle detection
- `/git/github.com/LiGoldragon/schema/src/document.rs` — Schema::assemble
- `/git/github.com/LiGoldragon/schema/src/assembled.rs` — AssembledSchema::plan_upgrade_from
- `/git/github.com/LiGoldragon/schema/src/upgrade.rs` — 7 projection kinds enum
- `/git/github.com/LiGoldragon/schema/src/engine.rs` — current 5 BuiltinSchemaMacro variants
- `/git/github.com/LiGoldragon/signal-persona-spirit/schemas/v0.1.0/schema.nota` — v0.1.0 schema (flat vector, needs 6-position retro)
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` — v0.1.1 schema (6-position, named fields)
- `/git/github.com/LiGoldragon/upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` — hand-written reference (the macro's target output)
- `reports/second-designer/181-counter-ego-mvp-leans-2026-05-25.md` §3 — UpgradeMacro MVP proposal
- `reports/designer/333-upgrade-mechanism-full-design-explained.md` §9 — hand-written historical pattern documented
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` §3.4 — UpgradeRule variant proposed
- Intent records 491 (upgrade knowledge on next version), 506 (data-carrying macro variants), 561 (schema diff Add/Remove/Modify), 569 (iterative-to-fixed-point macro), 585 (commit + push end of pass), 586 (lean on intent propose MVP), 587 (macro decides projection module location)
