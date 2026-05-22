# Universal Magnitude Type Design

Designer report. A workspace-universal `Magnitude` ordinal vocabulary,
seven-variant unit-variant enum, lives as a final leaf in `signal-sema`.
Replaces the per-component `Certainty` enum currently in
`signal-persona-spirit` and supersedes report /267-v2's certainty-drift
finding by widening the vocabulary rather than narrowing it. This
report is design only — runtime migration choreography belongs to /260,
/263, /270.

## 1. The problem

`signal-persona-spirit::Certainty` is a three-variant enum
(`Maximum`, `Medium`, `Minimum`) owned by one component contract.
Report /267-v2 documented seven `intent/*.nota` records carrying `High` —
written by an agent that invented a rung between `Medium` and
`Maximum` because the visible set felt too thin. Spirit's daemon
rejects them on parse. /267-v2's proposed fix was to map `High -> Maximum`
and forbid `High` going forward, narrowing the writer to fit the type.
The wrong move; the drift is the diagnostic, not the bug.

Two deeper failure modes underlie this:

**Per-component ownership of a workspace-universal idea.** Magnitude —
where on a coarse ordinal scale does this sit — is not Spirit-domain.
It applies to intent certainty, mind item priority
(`signal-persona-mind::ItemPriority`), and any future component
ordinal. Hiding the enum inside one contract crate forces every other
contract needing the same scale to either pull a transitive
cross-domain dependency on Spirit's contract or reinvent its own
ordinal — drift again, multiplied across components.

**Schema-too-narrow.** A unit-variant enum costs one tag byte
regardless of variant count. Seven variants and three variants are
identical on the wire. Picking three for "simplicity" buys nothing
and forces the writer to flatten distinctions they actually perceive.

## 2. The solution

A single workspace-universal `Magnitude` type, seven unit variants,
ordered Minimum < VeryLow < Low < Medium < High < VeryHigh < Maximum,
living in `signal-sema`.

In NOTA branches/leaves vocabulary (per the 2026-05-20 records in
`intent/nota.nota`): `Magnitude` is a **final leaf** — a fixed-size,
non-data-carrying enum where every variant is a unit (bare PascalCase
token). It never grows children; it has the same wire shape today
that it will have a decade from now.

Home determination. `signal-core` was renamed to `signal-frame` in
the 2026-05-19 architecture split (per `intent/component-shape.nota`
2026-05-19T20:00Z). `signal-frame` is intentionally domain-free wire
mechanics; a workspace-universal vocabulary type belongs there no more
than a `Severity` enum belongs inside TCP. `signal-executor` is the
daemon-side execution framework; contracts do not depend on it. Wrong
home.

`signal-sema` is the workspace's shared classification vocabulary
crate. Its existing residents — `SemaOperation`, `OperationClass`,
`SemaOutcome`, `Slot<Payload>`, `Revision`, `Bind`, `Wildcard`,
`PatternField` — are exactly the universal-vocabulary shape Magnitude
needs. Every contract crate already depends on `signal-sema` for its
`ToSemaOperation` projection. `signal-sema/ARCHITECTURE.md` declares
the scope as "universal ... vocabulary" and excludes
"component-specific payload records." Magnitude is a closed
classification set indexed by ordinal rank; structurally identical to
`SemaOperation`.

**signal-sema is the home.** It is the shared-typed-record-vocabulary
crate in everything but its name. The psyche's mention of "SignalCore"
in passing was the older name; the intent log settled the rename.

## 3. The type definition

```rust
//! In signal-sema/src/magnitude.rs.

use nota_codec::NotaEnum;
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};

/// Workspace-universal seven-rung ordinal magnitude.
///
/// Records (intent records, mind items, anything else carrying an
/// ordinal rating) cite this single vocabulary. Components consume
/// only the subset of variants they choose to act on; the variant
/// set is the wire schema, the consumption policy is per-component.
#[derive(
    Archive,
    RkyvSerialize,
    RkyvDeserialize,
    NotaEnum,
    Debug,
    Clone,
    Copy,
    PartialEq,
    Eq,
    PartialOrd,
    Ord,
    Hash,
)]
pub enum Magnitude {
    Minimum,
    VeryLow,
    Low,
    Medium,
    High,
    VeryHigh,
    Maximum,
}
```

The `PartialOrd` and `Ord` derives matter: variants declare from
smallest to largest, so derived ordering preserves the rank.
Components that want "anything at least High" can write
`magnitude >= Magnitude::High` without a hand-written match.

Re-export from `signal-sema/src/lib.rs`:

```rust
pub mod magnitude;
pub use magnitude::Magnitude;
```

The new module slots beside `operation`, `outcome`, `pattern`,
`identity` — a peer leaf in the existing tree.

## 4. The naming question

Psyche left naming "slightly open" between `Magnitude` and a wrapping
form like `SizeMagnitude`. Designer lean: **`Magnitude`**, unwrapped.

Per `skills/naming.md` (no-redundant-ancestry), a name carries only
what the namespace doesn't already supply. The use-site form is
`signal_sema::Magnitude` or `Magnitude` when imported. The field
holding it carries the dimension: `certainty: Magnitude` (Spirit's
`Entry`), `priority: Magnitude` (mind), `severity: Magnitude` in any
future component. Field name carries the dimension; type carries the
scale. `Size` in `SizeMagnitude` duplicates "scale" without sharpening
it.

`SizeMagnitude` is the framework-category anti-pattern flagged in
`skills/naming.md`: `Magnitude` is the role, `Size` is a
synonym-of-the-role tag bolted on. Both halves say magnitude. Same
shape as `*Actor`, `*Message`. Decision is the psyche's; lean lands
for ratification.

## 5. Consumption policy

The variant set is the schema. The consumed subset is per-component
policy. Three patterns will appear:

**Full vocabulary.** A component that classifies finely uses all
seven. Spirit's classifier (when /265 lands) might emit any of the
seven based on rhetorical force, frequency, explicit psyche markers.
Records on disk carry the agent's actual read of the statement, not
a coarsened proxy.

**Subset consumption.** A component matching only coarse distinctions
reads the full vocabulary but matches a subset:

```rust
match magnitude {
    Magnitude::Minimum => deprioritize(),
    Magnitude::Medium => acknowledge(),
    Magnitude::Maximum => act_immediately(),
    _ => acknowledge(), // VeryLow/Low/High/VeryHigh fall to acknowledge
}
```

Policy can change without a schema migration.

**Ordered comparison.** A component wanting "everything at or above X"
uses the derived `Ord`:

```rust
if intent.certainty >= Magnitude::High {
    surface_to_psyche(&intent);
}
```

The discipline: **never collapse the wire vocabulary to fit a
component's current consumption policy.** Record agents write the
full ordinal they perceive; consumers pick what they care about. The
agent that wanted `High` in /267-v2 was right; the right fix is the
wider schema, not the narrower writer.

## 6. Migration impact

The migration is design-only here. Runtime choreography lands in
/260, /263, /270.

**signal-persona-spirit changes.** Delete the `Certainty` enum
(lines 208-215 of `src/lib.rs`). Replace every `pub certainty:
Certainty` field with `pub certainty: Magnitude`. Import `Magnitude`
from `signal-sema`. The `Entry`, `RecordSummary`, `RecordProvenance`
records all touch.

The type-alias option (`pub type Certainty = signal_sema::Magnitude`)
is the wrong shape per ESSENCE's "backward compatibility is not a
constraint" — Spirit has no pinned external consumers, and an alias
preserves a misleading domain-local name for a workspace-universal
type. Field stays `certainty:` (the dimension), type is `Magnitude`
(the scale).

**Caller changes.** The persona-spirit daemon and tests import
`Certainty` directly (`tests/sema_projection.rs`, `tests/daemon.rs`,
`tests/actor_runtime.rs`, `src/actors/classifier.rs`, `src/store.rs`).
Each import switches to `Magnitude` from `signal-sema`. Both old and
new vocabularies contain `Maximum`, `Medium`, `Minimum`, so existing
literal values survive the rename.

**Spirit CLI accepted NOTA shape.** Records written through the
spirit CLI today carry `Maximum` / `Medium` / `Minimum`. After
migration all seven variants parse. The seven `High` records in
`intent/*.nota` enumerated in /267-v2 §2 stop being drift the instant
the wider Magnitude lands — they become first-class records.

`bootstrap-policy.nota`: no change. Policy shape is independent of
the certainty enum vocabulary. No external pinned consumers exist;
the break costs nothing.

## 7. Other candidates for collapse onto Magnitude

A scan across `signal-persona-*`, `owner-signal-*`,
`signal-repository-ledger`, `signal-persona-router`,
`signal-persona-orchestrate`, and `signal-persona-harness` surfaced
one strong candidate beyond Spirit's `Certainty`:

**signal-persona-mind::ItemPriority** (lines 596-605 of
`signal-persona-mind/src/lib.rs`): five-variant ordinal
`Critical / High / Normal / Low / Backlog`. Same shape as `Certainty`
— closed-set, ordinal, unit variants — and same drift risk (an agent
emitting `VeryHigh` against the deployed five-variant set would fail
decode identically to /267-v2's case).

The variant vocabularies differ; the shape is the same. Two paths:

1. Migrate `ItemPriority` to `Magnitude`, mapping the existing five
   to a seven-scale subset (`Critical -> Maximum`, `High -> High`,
   `Normal -> Medium`, `Low -> Low`, `Backlog -> Minimum`). Mind
   consumers pick which subset they match on.
2. Keep `ItemPriority` distinct, accepting that "priority" and
   "magnitude" name different scales even when both are seven-rung.

Designer lean: **path 1.** The point of universal Magnitude is that
the scale is the schema and the labels are arbitrary; field name
gives meaning at the use site. `Critical` and `Backlog` flatten
cleanly to `Maximum` and `Minimum`; nothing is lost.

No other ordinal candidates surfaced. Other closed-set enums
(Spirit's `Kind`, `ObservationMode`, `Presence`, `UnimplementedReason`;
Mind's `EdgeKind`; subscription tokens) are categorical, not ordinal —
no rank — and don't fit Magnitude. Decision on ItemPriority is the
psyche's (Q2 below).

## 8. Open questions worth psyche input

**Q1. Name ratification.** Lean is `Magnitude`, unwrapped. Reasoning
in §4. Wrapping form `SizeMagnitude` is rejected as framework-tag
ceremony per `skills/naming.md`. Confirm or override.

**Q2. ItemPriority collapse.** Migrate
`signal-persona-mind::ItemPriority` onto `Magnitude` as described in
§7 path 1? The lean is yes — one workspace ordinal vocabulary,
field-name carries the dimension. Counter-case: priority and
certainty may diverge in the future (a sixth-rung labeled "Urgent"
might mean something for priority but nothing for certainty), in
which case keeping them separate now is cheaper than separating them
later. The psyche's call.

**Q3. Reserved variant gap?** Seven rungs is what the psyche stated.
If a future agent encounters a record carrying `Severe` or `Critical`
or some other label not in the seven, the decoder rejects on parse —
the same failure mode /267-v2 caught. Should there be a `Reserved` /
`Unspecified` / `Unknown` variant as a graceful default, or is the
seven-variant closed set held strictly? Strict-closed is the
cleaner shape (the lean) and matches how `SemaOperation` is
defined; the cost is that adding a future eighth rung is a
hard break of every persisted record. Confirm strict-closed.

**Q4. `Certainty` rename or alias?** §6 calls for outright rename to
`Magnitude` at the field type position (keeping the field *name* as
`certainty`). The type-alias option is rejected as transitional-shape
per ESSENCE. Confirm rename-only.

## See also

- `intent/component-shape.nota` — psyche statements driving the
  universal-Magnitude direction.
- `intent/nota.nota` 2026-05-20 — branches/leaves vocabulary; fixed-
  size leaf framing for unit enums.
- `reports/designer/267-v2-intent-substrate-certainty-drift.md` — the
  certainty-drift finding this report supersedes by widening.
- `signal-sema/ARCHITECTURE.md` — destination crate scope.
- `signal-persona-spirit/src/lib.rs` lines 208-215 — current
  `Certainty` being replaced.
- `signal-persona-mind/src/lib.rs` lines 596-605 — `ItemPriority`
  collapse candidate.
- `skills/naming.md` — ancestry rule grounding the lean.
- `skills/typed-records-over-flags.md` — the wider discipline.
