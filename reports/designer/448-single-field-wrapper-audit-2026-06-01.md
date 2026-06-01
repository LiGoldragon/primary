; spirit
[single-field-wrapper-audit method-only-discipline orphan-rule typestate workspace-discipline craft-check]
[Audit of the single-field struct wrapper pattern across nota-next + schema-next + spirit-next, prompted by `struct CodecDerive { input: DeriveInput }`. 28 instances surveyed; all pay their way through one of five reasons. The pattern is the workspace's method-only-rule answer to "the verb needs a noun the inner type cannot provide."]
2026-06-01
designer

# 448 — Single-field wrapper audit — why `CodecDerive { input: DeriveInput }` and friends

## TL;DR

`struct CodecDerive { input: DeriveInput }` at `nota-next/derive/src/lib.rs:23` is the textbook case of a load-bearing pattern: a single-field wrapper that exists to give methods a noun the inner type cannot provide. Across the three next-stack repos there are 28 such wrappers; every one pays its way through one of five distinct reasons. None is gratuitous.

**The short answer to "why use a single-field struct, then?"** Because the inner type cannot host the methods you need to put somewhere. Four of the five reasons make the wrapper structurally necessary; the fifth makes it semantically valuable. The pattern is the workspace's method-only-rule (AGENTS.md hard override) answer to "I have a verb that needs a noun; the natural noun is foreign or too generic."

## The CodecDerive specific case

```rust
// nota-next/derive/src/lib.rs:23
struct CodecDerive {
    input: DeriveInput,
}

impl CodecDerive {
    fn new(input: DeriveInput) -> Self { ... }
    fn expand_decode(self) -> TokenStreamTwo { ... }
    fn expand_encode(self) -> TokenStreamTwo { ... }
    fn expand(self, direction: CodecDirection) -> TokenStreamTwo { ... }
}
```

Four candidate alternatives, each rejected by a workspace rule:

| Alternative | Rejected by |
|---|---|
| Free function `fn expand_codec(input: DeriveInput, direction: CodecDirection)` | AGENTS.md hard override §"Every Rust function is a method or associated function on an `impl` block of a NON-ZERO-SIZED data-bearing type, or a trait impl. Free functions are forbidden." |
| Inherent `impl DeriveInput { fn expand_decode(self) ... }` | Rust orphan rule: `DeriveInput` comes from the `syn` crate; you cannot add inherent methods to foreign types. |
| Type alias `type CodecDerive = DeriveInput; impl CodecDerive { ... }` | Rust forbids inherent impls on type aliases of foreign types (same orphan rule applies). |
| Extension trait `trait CodecDeriveExt { fn expand_decode(self) ... } impl CodecDeriveExt for DeriveInput { ... }` | Legal but hides the intent ("this DeriveInput is being used for codec derivation") behind a generic trait surface. Less direct. |

The newtype wrapper `CodecDerive { input: DeriveInput }` is the only direct answer that satisfies workspace discipline. The struct is non-zero-sized (carries `DeriveInput`); the methods belong to the noun; the name carries the operation intent; the call sites read `CodecDerive::new(input).expand_decode()` — verb belongs to noun, exactly what `skills/abstractions.md` §"The Karlton bridge" prescribes.

## The audit — 28 single-field wrappers across the three repos

### nota-next (9 wrappers)

| Type | Field | Inherent methods | Trait impls | Category |
|---|---|---|---|---|
| `CodecDerive` (derive crate) | `input: DeriveInput` | 4 | 0 | A — orphan-rule (foreign type) |
| `ContainerNotaAttributes` (derive crate) | `known_root: bool` | 2 | 0 | D — growth anticipation |
| `FieldNotaAttributes` (derive crate) | `name: Option<LitStr>` | 2 | 0 | D — growth anticipation |
| `NotaBodyEncoding` | `fields: Vec<String>` | 4 | 0 | B — named container with collection |
| `Pattern` | `elements: Vec<PatternElement>` | 3 | 0 | B — named container with collection |
| `MacroRegistry` | `nodes: Vec<MacroNodeDefinition>` | 5 | 0 | B — named container with collection |
| `StructureHeader` | `slots: Vec<StructureSlot>` | 3 | 0 | B — named container with collection |
| `StructureHeaderBuilder` (private) | `slots: Vec<StructureSlot>` | 5 | 0 | E — internal builder/parser state |
| `AtomCharacter` (private) | `character: char` | 2 | 0 | A — orphan-rule (primitive type) |

### schema-next (19 wrappers)

| Type | Field | Inherent methods | Trait impls | Category |
|---|---|---|---|---|
| `AsschemaArtifact` | `asschema: Asschema` | 11 | 0 | C — semantic projection newtype |
| `AsschemaArtifactPath` (private) | `path: PathBuf` | 3 | 0 | A — orphan-rule (foreign std type) |
| `StructFieldMap` | `entries: Vec<FieldDeclaration>` | 6 | 0 | B — named container |
| `SchemaNodeDelimitedNotation` (private) | `delimiter: Delimiter` | 4 | 0 | A — orphan-rule on workspace primitive (Delimiter from nota-next) |
| `MacroLibrary` | `source_entries: Vec<MacroLibrarySourceEntry>` | 11 | 0 | B — named container |
| `MacroLibraryArtifact` | `library: MacroLibrary` | 11 | 0 | C — semantic projection newtype |
| `MacroLibraryArtifactPath` (private) | `path: PathBuf` | 3 | 0 | A — orphan-rule |
| `MacroPattern` | `object: MacroPatternObject` | 5 | 0 | C — semantic distinction newtype |
| `MacroTemplate` | `object: MacroTemplateObject` | 4 | 0 | C — semantic distinction newtype |
| `DeclarativeSchemaMacro` (private) | `definition: ExecutableMacroDefinition` | 0 | 1 (`SchemaMacroHandler`) | C — semantic newtype carrying trait impl |
| `DelimitedNotation` (private) | `delimiter: Delimiter` | 4 | 0 | A — orphan-rule on workspace primitive |
| `SchemaEngine` | `registry: MacroRegistry` | 10 | 0 | C — semantic newtype (engine over registry) |
| `RootImportsMacro` (private) | `signature: MacroSignature` | 1 | 1 (`SchemaMacro`) | C — semantic newtype carrying trait impl |
| `RootNamespaceMacro` (private) | `signature: MacroSignature` | 1 | 1 (`SchemaMacro`) | C — same |
| `RawDatatypeMap` | `entries: Vec<RawDatatypeEntry>` | 3 | 0 | B — named container |
| `RawNotaSequence` | `items: Vec<RawNotaDatatype>` | 3 | 0 | B — named container |
| `RawSchemaFileName` (private) | `stem: String` | 2 | 0 | A — orphan-rule (foreign std type) |
| `ImportResolver` | `packages: Vec<SchemaPackage>` | 5 | 0 | B — named container |
| `AsschemaStoreKey` | `value: String` | 2 | 0 | A — orphan-rule (foreign std type) |

### spirit-next (7 wrappers)

| Type | Field | Inherent methods | Trait impls | Category |
|---|---|---|---|---|
| `Daemon` | `configuration: Configuration` | 4 | 0 | C — semantic newtype (runtime over config) |
| `MailLedger` | `events: Mutex<Vec<MailLedgerEvent>>` | 4 | 0 | B — named container |
| `BeingProcessed` | `sema_input: ...` | 0 | 0 | F — typestate phase data |
| `Processed` | `output: ...` | 0 | 0 | F — typestate phase data |
| `SignalTransport<Stream>` | `stream: Stream` | 9 | 0 | A — orphan-rule (generic type parameter) |
| `SpiritNextCli` (private) | `arguments: Vec<String>` | 4 | 0 | E — internal CLI state |
| `SpiritNextDaemonCli` (private) | `arguments: Vec<String>` | 3 | 0 | E — internal CLI state |

## The six categories — when this pattern earns its place

### Category A — Orphan-rule workaround (10 wrappers)

The inner type is foreign (Rust standard library, `syn`, `proc_macro2`) or a workspace primitive that the consumer wants to attach methods to in its own crate. Rust's coherence rules forbid inherent methods on foreign types; the wrapper is the local newtype that carries the methods.

Examples: `CodecDerive`, `AtomCharacter`, `AsschemaArtifactPath`, `MacroLibraryArtifactPath`, `RawSchemaFileName`, `AsschemaStoreKey`, `SignalTransport<Stream>`, `SchemaNodeDelimitedNotation`, `DelimitedNotation`.

This category is **structurally necessary** — there is no Rust idiom that hosts the methods without the wrapper. Removing the wrapper would force the choice between (a) writing free functions (forbidden), or (b) writing an extension trait (legal but indirect). The wrapper is the most direct expression of "the verb belongs to a noun, and the noun is this carrier."

### Category B — Named container with collection inside (9 wrappers)

The inner type is a collection (`Vec<T>`, `BTreeMap<K,V>`) but the role the collection plays has its own name and methods. The wrapper is the noun that names the role.

Examples: `Pattern`, `MacroRegistry`, `StructureHeader`, `StructFieldMap`, `MacroLibrary`, `RawDatatypeMap`, `RawNotaSequence`, `ImportResolver`, `MailLedger`, `NotaBodyEncoding`.

`Pattern { elements: Vec<PatternElement> }` exists because `Pattern::matches(&self, blocks: &[&Block]) -> Option<MacroCaptures>` is what `Pattern` IS. Without the wrapper, the method would have to be either (a) a free function `fn match_pattern(elements: &[PatternElement], blocks: &[&Block]) -> Option<MacroCaptures>` (forbidden), or (b) a method on `Vec<PatternElement>` (impossible — orphan rule on `Vec`, and even if legal, it'd put pattern-matching logic on the wrong noun).

This category is also structurally necessary because of the orphan rule against `Vec` + the method-only discipline, AND semantically valuable because the role name (`Pattern`) carries intent that the storage type (`Vec<PatternElement>`) doesn't.

### Category C — Semantic distinction newtype (7 wrappers)

The inner type is workspace-owned but the wrapper carries semantic distinction. The wrapper makes "this Asschema is being used as an artifact" or "this MacroPatternObject is being used as a Pattern (top-level)" type-system-enforced.

Examples: `AsschemaArtifact { asschema: Asschema }`, `MacroLibraryArtifact { library: MacroLibrary }`, `MacroPattern { object: MacroPatternObject }`, `MacroTemplate { object: MacroTemplateObject }`, `SchemaEngine { registry: MacroRegistry }`, `Daemon { configuration: Configuration }`, plus the trait-impl-carriers `DeclarativeSchemaMacro`, `RootImportsMacro`, `RootNamespaceMacro`.

`AsschemaArtifact` exists because the artifact projection (NOTA file + rkyv file + freshness check) is a different concern from the typed `Asschema` data. The wrapper hosts artifact methods (`to_nota_file`, `from_binary_path`, `is_fresh_against`) that aren't `Asschema`'s job. Each concern gets its own noun.

The trait-impl carriers (`DeclarativeSchemaMacro`, `RootImportsMacro`, `RootNamespaceMacro`) have 0 or 1 inherent methods but each carries a `SchemaMacro` or `SchemaMacroHandler` trait impl. The wrapper exists so the trait can be implemented as a distinct type — the inner field is what the trait methods need; the type identity is what dispatch needs.

This category is semantically valuable but not always structurally necessary. The alternative for some C cases would be to grow the inner type with the additional methods. For `AsschemaArtifact`, that would put file-IO methods on `Asschema` directly — coupling that should stay separate. For `MacroPattern { object: MacroPatternObject }`, the alternative would be to drop the wrapper and put the methods on `MacroPatternObject` directly — but the wrapper names the pattern-vs-template role distinction at the type level, useful when both are passed through generic functions.

### Category D — Growth-anticipation single-field attribute schemas (2 wrappers)

The wrapper holds one field today but is the typed surface for what will grow into multiple attribute fields.

Examples: `ContainerNotaAttributes { known_root: bool }`, `FieldNotaAttributes { name: Option<LitStr> }`.

`ContainerNotaAttributes::from_attributes` parses attribute lists into the typed surface; today it sets only `known_root`. When the workspace adds another `#[nota(...)]` container attribute, the field is added to the struct and call sites are unaffected. The wrapper IS the schema extensibility point.

This category is **forward-looking discipline**. The alternative is to use the bare type (`bool`) and pay the refactoring cost when the schema grows. Per `skills/abstractions.md` §"premature abstraction" caveats, this is borderline — but for attribute parsers specifically, the schema growth path is well-established and the wrapper has visible callsites (`attributes.known_root()`) that read identically before and after growth.

### Category E — Internal builder / parser / CLI state (4 wrappers)

Private types that exist as parser cursor state, builder accumulators, or CLI argument carriers.

Examples: `StructureHeaderBuilder`, `SpiritNextCli`, `SpiritNextDaemonCli`. Also the `Cursor` and `Parser` structs in nota-next/src/parser.rs (private; not in the wrapper list but same shape).

These are internal mechanisms; the wrapper is the noun for the parser/builder/CLI state machine. The methods (`push_block`, `push_slot`, `finish`, `single_argument`, `run`) belong to the state machine, not to its raw inner data.

This category is **idiomatic Rust** — every parser, every builder, every CLI follows this shape. Private types; the wrapper IS the state machine.

### Category F — Typestate phase data (2 wrappers)

The wrapper exists purely to give type-level identity to a lifecycle phase. The methods live on the parameterized container (`Mail<BeingProcessed>` and `Mail<Processed>`), not on the phase carrier itself.

Examples: `BeingProcessed { sema_input: ... }`, `Processed { output: ... }`.

Per `spirit-next/src/nexus.rs` and Spirit record 970, the typestate pattern requires that `Mail<BeingProcessed>` and `Mail<Processed>` be structurally distinct types — different data fields, different valid methods. The phase types `BeingProcessed` and `Processed` are the carriers; they have no methods of their own but their existence is what makes `Mail<Phase>` a typestate.

This category is **the typestate pattern** documented in `skills/rust/methods.md` §"Typestate as method-presence". Zero inherent methods on the phase carriers is the EXPECTED shape — the methods belong on the parameterized container, not on the phase markers.

## When the pattern would be anti-pattern

For completeness — when single-field wrappers are NOT legitimate (the workspace would have caught these in review):

- **Zero methods AND zero trait impls AND not a typestate phase carrier.** A struct that only exists to rename a field is gratuitous. `type` aliases handle pure renaming. None of the 28 audited wrappers fall into this anti-pattern category.
- **Zero-sized-type "namespace" struct.** `struct Foo;` with `impl Foo { fn helper(...) -> ... }` is a ZST namespace — explicitly forbidden by AGENTS.md hard override §"Methods on ZERO-SIZED placeholder types used as a namespace are equally forbidden — that's a free function in disguise." None of the **single-field-wrapper** types audited in this report are ZSTs (the audit scope is single-field wrappers specifically); every wrapper carries non-empty data. **This scope DOES NOT clear adjacent code of ZST anti-patterns** — operator 270 §"Concrete Disagreement" surfaced `struct FieldEncode;` at `nota-next/derive/src/lib.rs:342` as a real ZST violation in the exact file `CodecDerive` lives in. The audit methodology improvement (operator 270 §"Operator Position"): after validating single-field wrappers, ALSO grep for ZST method holders in the same scope. A valid wrapper pattern can coexist with a ZST anti-pattern nearby. This report adopted that methodology in the post-operator-270 revision, surfacing `FieldEncode` via the §"Convergence with operator 269" section.
- **Wrapper whose only use site immediately destructures the inner field.** If `let CodecDerive { input } = wrapper;` is the first line of every method, the wrapper added no value — the methods could have taken `DeriveInput` directly (would be true if `DeriveInput` weren't foreign). The `CodecDerive` case avoids this anti-pattern by having `self.input.attrs`, `self.input.ident`, `self.input.data`, `self.input.generics` access spread through `expand`.

## The verdict on `CodecDerive` specifically

The wrapper is structurally necessary because:

1. `DeriveInput` is from `syn` — foreign type, orphan rule forbids inherent methods.
2. AGENTS.md forbids free functions in production code.
3. The methods `expand_decode`, `expand_encode`, `expand` are the operation; they need a noun.
4. The noun name `CodecDerive` carries intent — "this DeriveInput is being used for codec derivation" — that the inner `syn::DeriveInput` type cannot communicate.
5. The four methods on the wrapper validate that the noun pays its way; this is not a name-only abstraction.

The wrapper is the workspace-discipline answer. Removing it would force a workspace-rule violation.

## Pattern essay — why this is the workspace's natural shape

Three workspace rules compose to make the single-field wrapper a recurring shape:

| Rule | Source | What it forces |
|---|---|---|
| Method-only discipline | AGENTS.md hard override + `skills/rust/methods.md` | Every verb belongs to a noun (struct, enum, or trait impl). No free functions. |
| Verb belongs to noun | `skills/abstractions.md` §"The Karlton bridge" | Find the noun BEFORE writing the verb. Name the type first; methods follow. |
| Naming clarity | `skills/naming.md` + AGENTS.md hard override §"Spell every identifier as a full English word" | The noun's name carries semantic intent. `CodecDerive` over `DeriveInput`; `Pattern` over `Vec<PatternElement>`. |

When these three rules meet a foreign type (or a generic type parameter, or a collection type without intent), the single-field wrapper is what falls out. It is not a workaround; it is the structurally correct expression of "this verb belongs to this noun, and this noun is distinct from its carrier."

The pattern's healthy version — what this audit confirms — has the wrapper paying its way through one of the five concrete reasons in categories A-F. The unhealthy version would be a wrapper with zero methods and zero trait impls outside the typestate pattern, which simply does not appear in these three repos.

## Implications for designer + operator practice

For designer reports proposing new types: when a new method needs a home and the natural carrier is a foreign or generic type, propose the wrapper directly. The pattern is well-established; don't apologize for it. Cite this report when reviewers ask "why not just use the inner type."

For operator implementations: when introducing a new wrapper, the test is the same five-reason taxonomy. If the new wrapper fits one of A-F with concrete method or trait-impl content, ship it. If it fits none, refactor — either the wrapper has missing methods (Category D growth-anticipation rarely applies outside attribute parsers and signal frame schemas) or the wrapper is gratuitous and the type alias / direct use is correct.

For audit reviewers: the keystroke check is "method count > 0 OR trait impl > 0 OR typestate phase marker." All three of these justify the wrapper; absence of all three is the anti-pattern signal.

## Convergence with operator 269

Operator independently audited the same question in `reports/operator/269-rust-single-field-wrapper-validity-audit-2026-06-01.md` and converged on the same verdict: `CodecDerive` is valid; the workspace's method-only discipline plus the orphan rule make the wrapper structurally necessary. Operator's five-reason taxonomy maps onto this report's six categories: operator's (1) domain newtype, (2) external-type workflow owner, (3) collection with behavior, (4) IO/error owner, (5) typestate phase carrier ⇔ this report's A (orphan-rule), B (named container), C (semantic newtype), E (internal state), F (typestate). The Category D growth-anticipation surface is folded into operator's reason 2; both readings are valid for the attribute-parser wrappers (`ContainerNotaAttributes`, `FieldNotaAttributes`). Three-way convergence of "the pattern is sound" across designer 445's broad substrate audit + operator 269 + this report is a strong correctness signal.

### Operator finding I missed — `FieldEncode` ZST anti-pattern

Operator 269 §"Adjacent Invalid Pattern" catches a real workspace-rule violation this report did not surface:

```rust
// nota-next/derive/src/lib.rs:342
struct FieldEncode;

impl FieldEncode {
    fn body_named(field: &Field) -> Result<TokenStreamTwo, Error> { ... }
}
```

This is the ZST-namespace pattern explicitly forbidden by AGENTS.md hard override §"Methods on ZERO-SIZED placeholder types used as a namespace are equally forbidden — that's a free function in disguise." The sibling `FieldDecode<'field>` at line 316 is the correctly-shaped data-bearing wrapper; `FieldEncode` should mirror its shape:

```rust
// proposed fix
struct FieldEncode<'field> {
    field: &'field Field,
}

impl<'field> FieldEncode<'field> {
    fn new(field: &'field Field) -> Self { Self { field } }
    fn body_named(&self) -> Result<TokenStreamTwo, Error> { ... }
}
```

**Bead-shaped operator action.** "operator: refactor `nota-next/derive/src/lib.rs:342` `struct FieldEncode;` into `FieldEncode<'field> { field: &'field Field }` mirroring `FieldDecode`'s shape; convert `body_named` from associated function to method on `&self`." Single-file refactor; one operator-hour. This finding plus designer 445 Findings 1-4 are the active workspace-discipline bead queue today.

This is exactly the kind of finding the audit cycle is designed to surface — designer 445 surveyed the three repos' `src/` trees but did NOT cover the derive crate's internals, leaving the gap operator 269 closes. Cross-lane convergence catches what single-lane audit misses.

### Follow-up comparison — operator 270

Operator landed a follow-up comparison report at `reports/operator/270-single-field-wrapper-comparison-with-designer-448-2026-06-01.md`. Three substantive contributions:

1. **Adopts the 6-category taxonomy** as the broader framing, with operator 269's shorter validity test ("what new noun did this type create?") as the implementation-review one-liner. Both phrasings are valid; the taxonomy is for design-time framing, the one-liner is for code-review heuristic.
2. **Flags the scope-misleading sentence** in this report's §"When the pattern would be anti-pattern": "None of the audited types are ZSTs" was true within the 28-instance single-field-wrapper list but reads as workspace-wide clearance. Fixed above with explicit scope statement.
3. **Adds the methodology improvement** to the workspace's audit playbook: after validating single-field wrappers, ALSO grep for ZST method holders in the same scope. A valid wrapper pattern can coexist with a ZST anti-pattern nearby — `CodecDerive` + `FieldEncode` in the same file is the worked example. This should land in `skills/architectural-truth-tests.md` or a new `skills/rust/wrapper-audit.md` skill as a durable methodology note (separate decision, not for this report).

The operator 270 comparison closes a clean designer ↔ operator audit loop: designer 448 frames the taxonomy and provides the broad scan; operator 269 catches the in-file ZST adjacency; operator 270 validates the taxonomy and surfaces the methodology improvement. Three reports, one shared verdict, two real cleanup actions filed (operator 269 §"Preferred Cleanup" for `FieldEncode` + this report's bead). The pattern designer 446 §4 names — "validate-recipe-first, surface findings through bead-shaped operator actions" — is what just played out at micro-scale on this question.

## Cross-references

- `nota-next/derive/src/lib.rs:23-57` — `CodecDerive` definition and methods.
- `nota-next/src/macros.rs:183` — `Pattern` (Category B canonical example).
- `nota-next/src/parser.rs:329` — `StructureHeader` (Category B + packed-byte derivation).
- `schema-next/src/asschema.rs:194` — `AsschemaArtifact` (Category C canonical example).
- `schema-next/src/declarative.rs:950` — `DeclarativeSchemaMacro` (Category C trait-impl carrier).
- `spirit-next/src/nexus.rs:47-55` — `BeingProcessed` + `Processed` (Category F typestate).
- `AGENTS.md` §"Every Rust function is a method or associated function on an `impl` block of a NON-ZERO-SIZED data-bearing type" — the hard override that drives this pattern.
- `skills/abstractions.md` §"The Karlton bridge" — why methods need nouns.
- `skills/rust/methods.md` §"Typestate as method-presence" + §"No ZST method holders" — typestate pattern and ZST exclusion.
- `skills/rust/methods.md` §"Legitimate ZST uses — narrow, named" — the narrow allowances for ZST patterns; phase carriers in Category F are NOT ZSTs (they carry payload data).
- `skills/naming.md` — naming clarity; full English words.
- `reports/designer/445-next-stack-audit-2026-06-01.md` — the substrate audit; this single-field-wrapper audit complements it on a specific pattern question.

## For the psyche

The pattern is sound, applied consistently, and pays its way in every instance audited. The `CodecDerive` case is the textbook example: foreign-type orphan rule + method-only discipline meet at the single-field wrapper as the only direct expression. No refactoring needed; no pattern revision needed. If a future review surfaces a wrapper that does NOT pay its way through one of the six categories, that is the signal to refactor — but no such case exists today in the three audited repos.
