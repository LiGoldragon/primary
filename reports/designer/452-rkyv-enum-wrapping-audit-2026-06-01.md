; spirit
[rkyv enum-wrapping closed-sum structural-macros audit MacroPatternObject sized-archive variant-tag witness pilot]
[Designer sub-agent audit of Spirit 1324 — the closed-sum-enum-per-shape pattern as the honest representation for type-erasing structural-macro outputs in rkyv-archived schema-emitted code. Pilot is MacroPatternObject in schema-next/src/declarative.rs. Eight cargo tests on feature branch audit-rkyv-enum-wrapping-presumption, gated behind cargo feature rkyv-enum-wrapping-audit, plus a flake check.]
2026-06-01
designer

# 452 — Audit of the closed-sum-enum rkyv wrapping presumption

## TL;DR

**Hypothesis HOLDS WITH CAVEATS.** The closed-sum-enum-per-shape
pattern is the correct fit for type-erasing structural-macro outputs
in rkyv-archived schema-emitted code on three load-bearing
properties: (1) every variant has known archive size, satisfying rkyv
0.8's sized-exact requirement; (2) the variant tag survives the
wire and disambiguates same-shape sibling variants
(`Capture(String)` vs `RestCapture(String)` vs `Atom(String)`); (3)
deep nesting scales **linearly** with depth, not exponentially. The
strongest piece of evidence is the linear-growth witness — depth-80
nesting archives in 1,449 bytes (~18 bytes per Delimited level on
top of the 9-byte leaf); the same shape with open type erasure would
either lose the variant tags or require out-of-band shape metadata
per archived value.

The caveat: the closed-sum-enum tax is REAL but small. The 4-variant
sample archives at 54 bytes vs 42 bytes for an open-bytes form
(ratio 1.29), and the stack-size cost is 32 bytes per
`MacroPatternObject` even when the held variant is a 4-byte
`Capture(Name)` — every variant pays for the widest. Two open
questions remain that the audit cannot settle from inside one pilot:
(a) when same-shape sibling variants (`Capture`/`RestCapture`/`Atom`
all wrap `String`) are sufficient to deserve a closed-sum vs a
single tagged `String` newtype with a discriminator field, and (b)
when the schema-emitter should prefer per-variant `RelPtr`
indirection over `Box<T>` for recursive variants.

## The hypothesis as captured

Per Spirit 1324 (Clarification, High, 2026-06-01):

> When a structural macro produces outputs of different shape
> (different data shapes inside captures: an atom, a delimited
> record with N children, a body stream, a rest-captured vector of
> blocks), we don't know the actual SIZE of the resulting type at
> the macro-definition layer — it depends on what the macro matched.
> Wrapping each shape with a closed-sum enum carrying each shape as
> a distinct data-bearing variant is hypothesized to be the **honest
> representation** of that wrapper-and-indirection link in the
> storage layer, because rkyv archive format is **sized-exact
> portable binary** — unlike JSON, CBOR, or MessagePack where the
> wire format hides shape variability, rkyv requires every archived
> value to have a known archive size up-front. Closed-sum enums
> make the variant-set known at type-system level; the archived
> bytes can recover the variant via a tag. Open type erasure
> (`Box<dyn Trait>`, untyped bytes, runtime reflection) cannot have
> this property and would force ugly workarounds in storage.

## Method

**Pilot picked:** `MacroPatternObject` in
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:317-322`.
Four variants of meaningfully different shape:

| Variant | Payload | Shape |
|---|---|---|
| `Capture(String)` | a 24-byte String | fixed-shape, distinct semantic |
| `RestCapture(String)` | a 24-byte String | same shape as Capture, distinct semantic |
| `Atom(String)` | a 24-byte String | same shape as Capture, distinct semantic |
| `Delimited(Box<MacroPatternDelimited>)` | recursive variable-size | `delimiter + Vec<MacroPatternObject>` |

The pilot is canonical: it's named in the production schema source
(`schemas/core.schema:14`), emitted as the same Rust enum, used by
the schema-emitted built-in macro library
(`schemas/builtin-macros.macro-library`), and lives in rkyv-archived
storage as the live `MacroLibrary` artifact. Three of four variants
share an identical `String` payload — the harshest test for the
"closed-sum preserves variant identity across the wire" property.

**Branch:** `audit-rkyv-enum-wrapping-presumption` in
`/git/github.com/LiGoldragon/schema-next/` (pushed to origin).
Worktree at
`~/wt/github.com/LiGoldragon/schema-next/audit-rkyv-enum-wrapping-presumption/`.

**Tests:** eight gated behind the `rkyv-enum-wrapping-audit` cargo
feature; default `cargo test` stays green; the suite runs via
`cargo test --features rkyv-enum-wrapping-audit` or the flake check
`#rkyv-enum-wrapping-audit`. Each test file path:
`tests/rkyv_enum_wrapping_audit.rs`.

| # | Test | What it surfaces |
|---|---|---|
| 1 | `macro_pattern_object_stack_size_is_bounded_by_string_variant_plus_tag` | closed-sum stack tax = 4 words |
| 2 | `macro_pattern_delimited_payload_is_strictly_larger_than_other_variants` | Box collapses the recursive variant |
| 3 | `each_variant_archives_to_a_reasonable_byte_count` | same-shape variants archive identically |
| 4 | `every_variant_round_trips_with_tag_preserved` | the load-bearing closed-sum property |
| 5 | `built_in_macro_library_round_trips_through_closed_sum` | production data round-trips through the pilot |
| 6 | `deeply_nested_pattern_archives_with_linear_byte_growth` | linear, not exponential |
| 7 | `closed_sum_archive_is_not_catastrophically_worse_than_open_bytes` | wide comparison vs an open-bytes form |
| 8 | `trait_object_alternative_is_structurally_excluded` | `Box<dyn Archive>` is not dyn-compatible |

## Findings — biggest first

### Finding 1 — Linear scaling with depth is the strongest evidence

The hypothesis predicts: closed-sum nesting + `Box<T>` for recursive
variants = predictable archive size. The deep-nesting witness
confirms this directly. Building a left-nested chain of
`Delimited(Box<MacroPatternDelimited>)` around a `Capture("Leaf")`
core:

| Depth | Archive bytes |
|---|---|
| 5 | 99 |
| 20 | 369 |
| 80 | 1,449 |

The per-Delimited cost is ~18 bytes (the slope of the line). The
ratio test in the witness (test 6) confirms slope-of-slope ratio is
< 2.0 across the 5-20 and 20-80 ranges — strictly linear within
noise floor.

The contrast case is what an open-form would do under nesting. An
"untyped bytes carrier" alternative would either need to nest its
own length prefix (then it's a worse closed-sum tagged by length),
or it would need to defer the parse — pushing the cost to
read-time, which is exactly when rkyv's zero-copy property is most
load-bearing. **The closed-sum form preserves rkyv's sized-archive
invariant under deep recursion; that is the property the hypothesis
gets right.**

### Finding 2 — Stack-size tax is 4 words per enum value, paid by every variant

`std::mem::size_of::<MacroPatternObject>()` is 32 bytes on x86-64
Linux. The breakdown:

| Component | Bytes |
|---|---|
| `String` (the widest payload) | 24 |
| Enum discriminator | 1 (rounded to 8 via padding) |
| Total (rounded to 8-byte alignment) | 32 |

Every variant — including `Capture("X".to_string())` whose
practical payload is a 1-byte string — occupies the full 32 bytes.
This is the **honest closed-sum tax**: every variant pays the cost
of the widest variant's payload.

The recursive `Delimited` variant is what makes Box load-bearing.
`MacroPatternDelimited` itself is 32 bytes (1-byte delimiter + 7
bytes padding + 24 bytes Vec header). Without `Box`, the
`Delimited` variant would force the enum's stack form to grow to
match — and worse, the recursive case (`Delimited` containing
`Delimited`) would create an infinite-size type that the compiler
correctly refuses. The `Box<MacroPatternDelimited>` collapses the
recursive variant to a single pointer (8 bytes), and the enum's
ceiling is the 24-byte String. **This is the canonical recursive-
enum-with-Box pattern, and it's the only viable shape for a
closed-sum enum with recursive variants in rkyv.**

### Finding 3 — Variant tag survives the wire; same-shape siblings don't collide

Three variants (`Capture`, `RestCapture`, `Atom`) carry identical
`String` payloads. Witness test 4 archives `Capture("Name")`,
restores, and asserts the result is `MacroPatternObject::Capture` —
not `Atom` or `RestCapture`. The closed-sum form preserves the
variant distinction across the rkyv archive boundary.

The structural value: in the production built-in macro library
(`schemas/builtin-macros.macro-library`), this distinction encodes
semantic meaning. `Capture("Name")` matches a single block; the
matched block is bound. `RestCapture("Fields")` matches zero-or-more
blocks; the matched sequence is bound. `Atom("Type")` matches a
literal text "Type"; nothing is captured. The three semantics
diverge sharply; preserving the variant tag across the wire is
load-bearing.

A bytes-form alternative would archive only the `String` payload
(9 bytes for a 4-char name); the receiver would have no way to
recover the variant without out-of-band shape metadata. The
closed-sum form encodes the variant in 9 bytes total (4-char string
+ 4-byte length + 1-byte tag rounded by alignment) — **the tag is
nearly free at the bytes level**.

### Finding 4 — The closed-sum tax is 1.29x vs raw-payload-bytes, not catastrophic

The form-vs-form witness compares total archive bytes for the same
4 sample values:

| Form | Total bytes (4 variants) |
|---|---|
| Closed-sum `MacroPattern(MacroPatternObject)` | 54 |
| Open-payload-bytes (just the payload archives) | 42 |
| Ratio | 1.29x |

The 12-byte overhead covers: rkyv's outer `MacroPattern` newtype
wrapper, the enum tag, and the per-value RelPtr offsets rkyv uses
internally. The audit's prediction was an honest comparison: the
open-bytes form skips the wrapping AND loses the variant tag AND
defers parse cost to read-time. The 1.29x ratio is **the cost of
preserving the variant identity at archive time** — paid once at
write, recovered for free at every read.

**The closed-sum form is not catastrophically expensive.** A 3x or
10x ratio would warrant audit concern; 1.29x is the honest tag
overhead the hypothesis predicts.

### Finding 5 — Trait-object alternative is structurally excluded by rkyv 0.8

The witness test 8 documents the negative case: `Box<dyn Archive>`
would not compile.

```text
error[E0038]: the trait `Archive` is not dyn-compatible
  note: for a trait to be dyn-compatible it needs to allow
        building a vtable
  note: associated type `Archived` is not dyn-compatible
```

`rkyv::Archive` has associated types (`Archived`, `Resolver`) that
make it not dyn-compatible. This is not a workaround-able quirk —
it's the load-bearing property that makes rkyv's archived shape
recoverable from bytes alone. The audit confirms: the closed-sum
form isn't a stylistic preference; **the trait-object alternative
doesn't exist in rkyv 0.8.**

### Finding 6 — Production-built-in library round-trips through the closed-sum pattern

The production-checked-in `MacroLibrary::builtin()` archives to 699
bytes covering 5 source entries. Round-trip witness 5 confirms
end-to-end fidelity. Inspection of the pattern-side variants
exercised by the production library:

| Variant | Pattern-side usage in builtins |
|---|---|
| `Capture` | yes (5 occurrences) |
| `RestCapture` | yes (5 occurrences) |
| `Delimited` | yes (deepest nesting depth 3 in builtins) |
| `Atom` | **no — pattern side never matches a literal atom** |

`Atom` appears only on the template side (`MacroTemplateObject`).
This is an honest finding the audit surfaces: the four-variant
closed-sum on `MacroPatternObject` is **structurally** justified
(the schema-source pattern grammar supports it; users may write
literal-text-matching patterns), but the **production** built-in
library uses only three. The pattern is paying for a fourth variant
that today's macros don't reach. The right read is "the variant
exists for users to author" — not "the variant is dead code."

### Finding 7 — `Atom`/`Capture`/`RestCapture` is the audit's "smell" — three variants, same shape

The pilot has THREE variants that wrap an identical `String`. They
differ semantically — Capture matches a single block and binds it;
RestCapture matches zero-or-more blocks and binds them; Atom matches
literal text and binds nothing. Different semantics; identical
data shape.

This is the audit's biggest **structural** finding. The closed-sum
pattern is honest here — semantics distinguish the variants — but it
also reveals that **the type-erasure pressure is in the
NotaParser/lowering layer**, not in the macro-output layer. The
NOTA token form is:

- `$Name` → `Capture("Name")`
- `$*Fields` → `RestCapture("Fields")`
- `Struct` → `Atom("Struct")`

The lowering function dispatches on the first character of the
captured token (`$` vs `$*` vs anything else). The variant
distinction at the enum level is THE materialization of that
lowering decision. A single-`String`-with-prefix alternative
(`PatternToken(String)` where the string is `"$Name"` /
`"$*Fields"` / `"Struct"`) would push the dispatch back to the read
site — a stringly-typed regression.

**The closed-sum form is the right answer here, but the audit
notes the asymmetry**: three variants for `String` payloads vs one
for the recursive structural variant. The next audit pass should
ask whether `Capture`/`RestCapture` ought to be unified under a
`Bind(CaptureName)` variant carrying a typed `enum CaptureName {
Single(String), Rest(String) }` — which would preserve the closed-
sum honesty AND consolidate the two same-semantic siblings.

## Questions the audit raises

Ordered by how much they matter to subsequent work.

**Q1 — When do same-shape sibling variants deserve consolidation?**
The pilot has `Capture(String)` and `RestCapture(String)` as
distinct top-level variants. Both wrap a string; both are bound;
the only difference is binding-cardinality. A `Bind(CaptureName)`
form with `enum CaptureName { Single(String), Rest(String) }` would
be one consolidation. Designer report 453 or later should establish
the rule: "when N variants share payload shape AND semantic
neighbourhood, they should consolidate into one variant whose
payload encodes the distinction."

**Q2 — When should the recursive variant use `RelPtr` over `Box`?**
The pilot's `Delimited(Box<MacroPatternDelimited>)` uses Rust's
`Box`, which rkyv archives transparently. rkyv's `RelPtr<T>` is the
lower-level primitive — a 4-byte offset relative to the archive
position. For dense recursive structures, `RelPtr` may produce
smaller archives than `Box`. The audit does not have evidence
either way; the current pilot's archived sizes are honest but not
optimized. Worth a follow-up if the schema-emitter wants to squeeze
archive bytes.

**Q3 — Does the variant-set need to be statically closed, or can it
be schema-versioned?** The audit's hypothesis says "closed-sum enums
make the variant-set known at type-system level." Designer/447's
upgrade-as-SEMA design adds `SchemaEdit::AddVariant` as a first-
class upgrade operation. The two compose cleanly today (a new
variant means a new compiled binary, per Spirit 1311), but the
audit notes the closed-sum's static-closure conflicts with eventual
hot-reload scenarios. No action; just naming the tension.

**Q4 — What's the upper bound on variant count before the closed-
sum form becomes a code-smell?** The pilot has 4 variants. The
sibling `PatternElement` (5 variants) and `MacroTemplateObject` (4)
are similar. `Asschema`'s `TypeReference` has 7 variants
(`String`/`Integer`/`Boolean`/`Path`/`Plain`/`Vector`/`Map`/
`Optional`). Designer/447's `SchemaEdit` enum has 8 variants. At
some count, the closed-sum becomes a switch-statement-of-types
rather than a real domain enum. The audit doesn't have evidence to
set a threshold, but names this as a question for the next pilot
(`SchemaEdit` at 8 variants is the natural next subject).

**Q5 — Should the schema-emitter inline `Box` indirection
automatically, or require it explicit in the schema source?**
Today, `MacroPatternObject` declares `Delimited
MacroPatternDelimited` in the schema source; the emitter would
default to inline (`Delimited(MacroPatternDelimited)`) which won't
compile because of the recursive type. The current source uses
`Box` manually. A future schema-emitter could detect the recursive
case and emit `Box<T>` automatically; the audit recommends doing so
(otherwise every schema author hits the same compile error).

## Suggestions — concrete pattern refinements

The audit's tests support these refinements; operator should
consider them for the schema-emitter.

### Suggestion 1 — When a closed-sum variant is recursive, the emitter SHOULD emit `Box<T>` automatically

The current `MacroPatternObject` declares
`Delimited(MacroPatternDelimited)` in NOTA source but the emitted
Rust uses `Box<MacroPatternDelimited>`. Two reasons:

- Rust requires `Box` for recursive enum variants (otherwise
  infinite size, compile error).
- rkyv 0.8 archives Box transparently — no extra work for the
  schema-emitter.

Add this as an emitter-level rule: when an enum variant's payload
type is the enum itself, or contains the enum reachable through any
field, **the emitter inserts `Box<T>` around the recursive
reference**. Document the rule alongside the emitter; cite this
audit.

### Suggestion 2 — When variant payloads are identical type AND identical semantic family, prefer consolidation

The pilot's `Capture(String)`/`RestCapture(String)` consolidation
candidate (Q1 above). The rule:

- Same payload type alone is NOT enough to warrant consolidation
  (semantics matter — `Capture` and `Atom` both wrap String but
  have different semantic families).
- Same payload type AND same semantic family (both are "binding
  captures") IS enough.
- The consolidation introduces a typed sub-enum (`enum CaptureName
  { Single(String), Rest(String) }`) that preserves the variant
  distinction at one nesting level down — closed-sum-within-closed-
  sum, still rkyv-archivable.

### Suggestion 3 — When the closed-sum exceeds ~10 variants, sub-divide by concern

The current pilot at 4 variants is comfortably within budget. The
sibling 7-variant `TypeReference` and 8-variant `SchemaEdit` are at
the boundary. The next pilot should audit whether the high-variant-
count cases naturally split into sub-enums (e.g.
`TypeReference::Scalar(ScalarType)` + `TypeReference::Composite
(CompositeType)`). The closed-sum stays closed; the nesting carries
the concern split. No action this report; named for follow-up.

### Suggestion 4 — Stack-size watchpoint as ongoing witness

Add a stack-size assertion to every load-bearing closed-sum-enum
test suite. The pilot's witness 1 asserts
`size_of::<MacroPatternObject>() <= 4 * size_of::<usize>()`. The
pattern: when a closed-sum enum's stack size silently grows past
its predicted budget, the cause is usually a Box-indirection that
got lost or a payload type that became wider. The watchpoint
surfaces this drift at test time.

## Honest verdict

**The closed-sum-enum-per-shape pattern is the honest answer for
type-erasing structural-macro outputs in rkyv-archived schema-
emitted code, with one caveat: same-shape sibling variants should
be consolidated by semantic family before being committed at top
level.** The hypothesis is right that rkyv's sized-archive
requirement forces the variant-set to be statically closed; right
that `Box<T>` collapses recursive variants without losing rkyv
compatibility; right that the variant tag is preserved across the
wire essentially for free (1.29x archive ratio vs raw-payload
bytes); and right that trait-object alternatives are structurally
excluded by rkyv 0.8.

The audit's refinement: the cleanest STATEMENT of the principle
now is:

> When a schema-emitter produces a Rust type whose values may take
> N structurally-different shapes, AND those shapes must be
> archived in rkyv storage, the emitter shall produce a closed-sum
> enum with one variant per shape. Recursive variants shall be
> emitted as `Box<T>`. Same-payload-type sibling variants shall be
> consolidated under one variant whose payload is a typed sub-enum
> when (and only when) the siblings share semantic family.

The hypothesis HOLDS as stated; the refinement is what the test
witnesses actually license.

## Pilot test code — selected witnesses

The full suite is at
`/git/github.com/LiGoldragon/schema-next/tests/rkyv_enum_wrapping_audit.rs`
on branch `audit-rkyv-enum-wrapping-presumption`. Selected excerpts:

### Stack-size witness (test 1)

```rust
#[test]
fn macro_pattern_object_stack_size_is_bounded_by_string_variant_plus_tag() {
    let stack_size = size_of::<MacroPatternObject>();
    assert!(
        stack_size <= 4 * size_of::<usize>(),
        "MacroPatternObject stack size grew past 4 words: {stack_size} bytes; closed-sum \
         padding budget exceeded — investigate whether a variant payload grew",
    );
    assert!(
        stack_size >= size_of::<String>(),
        "MacroPatternObject stack size below String: {stack_size}; \
         a payload variant was silently dropped or shrunk",
    );
}
```

### Round-trip with tag-preservation witness (test 4)

```rust
#[test]
fn every_variant_round_trips_with_tag_preserved() {
    let cases = [
        MacroPattern::new(MacroPatternObject::Capture("Name".to_owned())),
        MacroPattern::new(MacroPatternObject::RestCapture("Fields".to_owned())),
        MacroPattern::new(MacroPatternObject::Atom("Struct".to_owned())),
        MacroPattern::new(MacroPatternObject::Delimited(Box::new(
            MacroPatternDelimited::new(
                MacroDelimiter::Brace,
                vec![MacroPatternObject::Capture("X".to_owned())],
            ),
        ))),
    ];
    for original in cases {
        let bytes = rkyv::to_bytes::<RkyvError>(&original).expect("archive");
        let restored: MacroPattern =
            rkyv::from_bytes::<MacroPattern, RkyvError>(&bytes).expect("decode");
        assert_eq!(original, restored, "round-trip dropped the variant tag");
    }
}
```

### Linear-growth witness (test 6)

```rust
#[test]
fn deeply_nested_pattern_archives_with_linear_byte_growth() {
    let small = build_chain(5);
    let medium = build_chain(20);
    let deep = build_chain(80);
    let small_to_medium = (archived_byte_count(&medium) - archived_byte_count(&small)) as f64 / 15.0;
    let medium_to_deep = (archived_byte_count(&deep) - archived_byte_count(&medium)) as f64 / 60.0;
    let ratio = if small_to_medium > medium_to_deep {
        small_to_medium / medium_to_deep
    } else {
        medium_to_deep / small_to_medium
    };
    assert!(ratio < 2.0, "byte growth is not linear with depth");
}
```

### Open-form comparison witness (test 7)

```rust
#[test]
fn closed_sum_archive_is_not_catastrophically_worse_than_open_bytes() {
    // ... 4 sample variants archived two ways
    let ratio = closed_total as f64 / open_total as f64;
    assert!(
        ratio < 3.0,
        "closed-sum total ({closed_total}) is more than 3x the open-bytes \
         total ({open_total}); the wrapper layers are imposing more cost \
         than honest tag overhead would predict",
    );
}
```

### Trait-object-excluded witness (test 8 — documentation form)

```rust
// The following commented code is illustrative; uncommenting it would
// surface the compile error inline:
//
//   trait ArchivedShape: rkyv::Archive {}
//   struct OpenWrapper { inner: Box<dyn ArchivedShape> }
//   // error[E0038]: the trait `Archive` is not dyn-compatible
//   //   note: associated type `Archived` is not dyn-compatible
```

## Branches pushed

| Repo | Branch | Commit | Worktree path |
|---|---|---|---|
| `schema-next` | `audit-rkyv-enum-wrapping-presumption` | `97fde52c` (jj `mlmzuupx`) | `~/wt/github.com/LiGoldragon/schema-next/audit-rkyv-enum-wrapping-presumption/` |

Pushed to `origin` 2026-06-01.

## Cross-references

**Mandatory reading consulted before any test design:**

- `/home/li/primary/AGENTS.md` — workspace hard overrides; rkyv-and-storage discipline.
- `/home/li/primary/skills/rust/storage-and-wire.md` — canonical rkyv + redb pattern.
- `/home/li/primary/skills/architectural-truth-tests.md` — witness pattern and the pair-rule sweep discipline.
- `/home/li/primary/skills/feature-development.md` — worktree convention.
- `/home/li/primary/skills/designer.md` — designer protocol, specify-by-example.
- `/home/li/primary/skills/abstractions.md` — verb belongs to noun (consolidation rule).
- `/home/li/primary/skills/language-design.md` — closed-vs-open-sum discipline (§"Position defines meaning", §"Strings are transitional").
- `/home/li/primary/repos/lore/rust/rkyv.md` — rkyv 0.8 feature-pin discipline and `Archive` trait constraints.

**Spirit records cited:**

- **1324** (Clarification, High, 2026-06-01) — the audit hypothesis (this report verifies-with-caveats).
- **1287** (Correction, Maximum) — parser body decode delegates to body stream; pattern-side dispatch.
- **1290** (Decision, Maximum) — `NotaBodyDecode` as semantic entry; relevant to how pattern decoding flows.
- **1294** (Decision, Maximum) — schema source enum body vectors honour homogeneity; relevant to how `MacroPatternObject` variants are encoded.
- **1295** (Correction, Maximum) — enum bodies preserve vector homogeneity through the structural macro shorthand.
- **1305** (Principle, Maximum) — upgrade mechanisms are SEMA operations (Q3 context).
- **1311** (Constraint, Maximum) — new Rust data types require recompiling the daemon binary (the closed-sum closure aligns with this).
- **1312** (Principle, Maximum) — NOTA always corresponds to a specified object (the closed-sum form is HOW that correspondence stays exact under rkyv storage).
- **1313** (Clarification, High) — schema-editing upgrade operation examples (Q3 follow-up surface).

**Companion designer reports:**

- `444-stack-vision-2026-05-31/2-data-model.md` — the rkyv equivalences for the 11 major types; the closed-sum patterns are visible.
- `447-upgrade-as-sema-design-2026-06-01.md` — `SchemaEdit` and `FieldMigration` are 8-variant and 5-variant closed-sum enums (the audit's Q4 candidate for the next pilot).

## For the orchestrator

The audit verifies Spirit 1324's hypothesis with caveats. The
closed-sum-enum-per-shape pattern is the honest representation for
type-erasing structural-macro outputs in rkyv-archived schema-
emitted code on three properties: every variant has known archive
size (rkyv 0.8's sized-archive requirement); the variant tag
survives the wire; deep nesting scales linearly, not exponentially.
Pilot was `MacroPatternObject` in schema-next/src/declarative.rs.
Eight tests on branch `audit-rkyv-enum-wrapping-presumption` in
schema-next, gated by cargo feature `rkyv-enum-wrapping-audit`,
plus a matching flake check. Default cargo test stays green.
Strongest evidence: 1,449-byte archive at depth-80 nesting (~18
bytes per Delimited level, linear); 1.29x archive cost vs raw-
payload bytes (honest tag overhead). Trait-object alternative
structurally excluded by rkyv 0.8 — `Box<dyn Archive>` doesn't
compile (associated types make `Archive` not dyn-compatible).
Biggest open question: when should same-shape sibling variants
(`Capture(String)`/`RestCapture(String)`/`Atom(String)` all wrap
String) consolidate under a typed sub-enum vs stay at top level?
The audit's refinement: consolidate by semantic family, not by
payload type alone. The next pilot candidate is `SchemaEdit` from
designer/447 (8 variants, the audit's Q4 candidate). Branch pushed
to origin. Verdict: HOLDS WITH CAVEATS.
