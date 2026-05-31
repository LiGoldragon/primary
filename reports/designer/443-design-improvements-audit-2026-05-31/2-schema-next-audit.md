# 2 — schema-next design audit

*Kind: audit · Topics: schema-next, asschema, declarative-macros, AsschemaStore, hand-rolled-codec, lowering-pipeline, artifact-IO, parallel-data-types, text-roundtrip, wrapper-thinness · 2026-05-31 · designer lane sub-agent*

## Scope

`/git/github.com/LiGoldragon/schema-next/` only — schema vocabulary, asschema, macro mechanism, `AsschemaStore`. Not nota-next, not schema-rust-next, not spirit-next. Six source modules under audit:

| File | Lines | Role |
|---|---|---|
| `src/asschema.rs` | 1309 | The assembled-schema noun + codec impls |
| `src/declarative.rs` | 1864 | `DeclarativeMacroLibrary` + `MacroLibraryArtifact` + assembled-template lowering |
| `src/engine.rs` | 1008 | `SchemaEngine` + `SchemaError` + bootstrap macros |
| `src/macros.rs` | 615 | `MacroRegistry` + `MacroNodeDefinition` wrapper + dispatch trait |
| `src/syntax.rs` | 568 | Legacy `SyntaxSchema` layer above raw |
| `src/raw.rs` | 361 | `RawSchemaFile` raw-NOTA reading |
| `src/store.rs` | 202 | New `AsschemaStore` redb persistence (commit `84ce382`) |
| `src/module.rs` | 105 | `SchemaPackage` + `SchemaModuleSource` |
| `src/resolution.rs` | 227 | `ImportResolver` + `ImportSource` + `ResolvedImport` |

The `Asschema::to_nota` / `Asschema::from_nota_document_fields` anti-pattern is the canonical example from designer 442 — mentioned here as Finding 0 then set aside; this audit looks for OTHER substrate gaps.

## Finding 0 (briefly): the canonical anti-pattern is already named

`Asschema::to_nota` (`src/asschema.rs:175-177` → routed through the hand-built `to_nota_document_body` at lines 221-232) and `Asschema::from_nota_document_fields` (`src/asschema.rs:189-204`) match Spirit 1278 verbatim: six hand-typed positional reads, two hand-typed field-projections that fabricate `Name::new("Input")` / `Name::new("Output")` inside the codec body, and a six-element `NotaDocumentEncoding::new(vec![...])` builder. The hand-rolled `\n.join` from `daff76a` was replaced by `NotaDocumentEncoding` at `62d78bc`, but the schema-side per-field projection remains because nota-next has no `#[nota(known_root)]` / `#[nota(name = "Input")]` derive. Designer 442 owns the prescription (the `known_root` derive in nota-next); this audit moves on.

## Finding 1: artifact-IO is duplicated verbatim across two owners; should be one trait

`AsschemaArtifact` (`src/asschema.rs:234-317`) and `MacroLibraryArtifact` (`src/declarative.rs:72-155`) carry the same eight methods with the same shape:

```
from_nota_source / to_nota_source
from_binary_bytes / to_binary_bytes
read_nota_file / write_nota_file
read_binary_file / write_binary_file
```

Plus a private `ArtifactPath` helper struct (`AsschemaArtifactPath` at `src/asschema.rs:295-317`; `MacroLibraryArtifactPath` at `src/declarative.rs:133-155`) that exists ONLY to hold an `io_error` projection from `std::io::Error` to `SchemaError::Io`. The two are character-identical apart from the wrapped type name. ~80 lines of pure duplication per owner; ~160 lines that should be one place.

The pattern is exactly `SerializableArtifact<T>` from the prompt's question 5:

```rust
// Sketch (not a recommendation of exact form — operator's call):
trait SerializableArtifact: Sized {
    type Inner: NotaDecode + NotaEncode + rkyv::Archive + ...;
    fn inner(&self) -> &Self::Inner;
    fn wrap(inner: Self::Inner) -> Self;
    // default-impl bodies for the eight methods, all in terms of Inner's codec + path IO
}
```

The two artifact owners shrink to ~10 lines each (a one-field wrapper struct + the `inner`/`wrap` glue). The artifact-IO methods live ONCE.

Stage-5 consequence: when `schemas/core.asschema` emits its own Rust nouns, more artifact-bearing types appear (`SignalArtifact`, `NexusArtifact`, `SemaArtifact`, schema-diff artifact, schema-upgrade artifact per Spirit 1254 Gap D). Without the trait, each one re-copies the same 80 lines. With the trait, they get the eight methods free. This is exactly the scope-multiplier the prompt's lens optimises for.

## Finding 2: `MacroPattern` / `MacroTemplate` are parallel data types with parallel codecs; the parallelism is structural noise

Look at `src/declarative.rs:265-450`. Two pairs of public data types:

| Pattern side | Template side |
|---|---|
| `MacroPatternData` (line 265) | `MacroTemplateData` (line 364) |
| `MacroPatternObjectData` (line 301) | `MacroTemplateObjectData` (line 400) |
| `MacroPatternDelimitedData` (line 330) | `MacroTemplateDelimitedData` (line 429) |

Each pair is THE SAME ENUM with the same four variants (`Capture(String)`, `RestCapture(String)`, `Atom(String)`, `Delimited(Box<...>)`) and identical rkyv attribute bounds. ~75 lines of declarations duplicated.

Then the internal `PatternObject` (line 637) and `TemplateObject` (line 887) are again the same enum, with **near-identical `from_block`, `from_data`, `to_data` method bodies** (verified by direct diff — only the type-suffix `MacroPatternObjectData::Capture` vs `MacroTemplateObjectData::Capture` differs). ~80 more lines duplicated.

The pattern side has extra `matches_pair` / `matches_block` / `push_capture_names` methods (lines 707-767); the template side has `expand_notations` (line 959). That semantic asymmetry justifies different *use-sites*, not different *data types*. One typed `MacroAst<Mode>` (where `Mode` distinguishes Pattern from Template) or one `MacroAst` shared by both with the pattern-specific verbs as methods, the template-specific verbs as methods on the same noun, would collapse the parallelism without losing any semantic information.

The deeper signal: a macro pattern's child shape and a macro template's child shape **are the same shape** — captures, atoms, delimited bodies. The fact that they live in separate types is an accident of the implementation iterating quickly through declarative-macro space. Six co-evolving structs (three data types + three runtime types) is high coordination cost; any future addition (a new capture variant, a new delimiter shape, a new rkyv-archive constraint) lands in 6 places.

## Finding 3: the declarative macro engine round-trips through a text string in the middle of structural lowering

`src/declarative.rs:1121-1144`, the `DeclarativeSchemaMacro::lower` method:

```rust
let bindings = self.definition.pattern.captures(object)?...;
context.remember_macro(self.name());
context.remember_position(position);
bindings.remember(self.name(), context);
let expanded = self.definition.template.expand(&bindings)?;
context.remember_expanded_template(self.name(), expanded.source());
expanded.lower_to_output(registry, context)
```

The chain is **structured Block → bindings → text template → re-parse via Document::parse → structured Block → typed MacroOutput**. The middle hop through `String` is at `MacroTemplate::expand` (`src/declarative.rs:872-883`), which calls `self.object.expand_notations(bindings)` (line 959) producing `Vec<String>` of notation chunks, then `ExpandedTemplate::lower_to_output` (line 1157) calls `Document::parse(&self.source)` and walks back into structural lowering.

Worse, the `MacroBindings` (lines 1026-1088) store captured values as `String` in the first place (`SingleMacroBinding { name: String, value: String }`, `RepeatedMacroBinding { name, values: Vec<String> }`) — produced by `NotationBlock::new(object).compact_notation()` (lines 732, 837) — even though the captured object is a `&Block` available at match time. So the round-trip is forced from the moment a capture binds: `Block → notation String → re-parse to Block → lower`.

This contradicts Spirit 1280 (Maximum) directly: *"Schema should prefer structural macros over text macros."* And Spirit 1263 names this same trap: *"the Nota decoder is EXTENDED by registered macros: when parsing a brace or bracket position with a macro registry attached, each entry is dispatched against the macros; the first matching macro extracts named captures from the matched blocks; consumer code (Schema being one consumer) interprets captures into output."* The captures should be **typed Block references**, not stringified notation.

The fix isn't local to one method — it's the data model of `MacroBindings`. Change to:

```rust
struct MacroBindings<'schema> {
    singles: Vec<SingleMacroBinding<'schema>>,   // value: &Block instead of String
    repeated: Vec<RepeatedMacroBinding<'schema>>, // values: Vec<&Block>
}
```

Then `expand_notations` becomes `expand_blocks` (or `expand_to_blocks`), templates produce `Vec<Block>` (owned where bindings need cloning), and `lower_to_output` consumes Block directly. The text hop disappears entirely; `Document::parse` is never called by the macro engine. The 80-line stringly-typed substrate retires.

This finding has the highest semantic punch in the repo because it touches a Spirit-Maximum constraint, costs no public-API change (the artifact already gets the right answer), and removes a layer of round-tripping every time a declarative macro fires.

## Finding 4: the `schema-next::MacroNodeDefinition` wrapper is mostly redundant with `nota_next::MacroNodeDefinition`

`src/macros.rs:294-580`. The schema-side struct:

```rust
pub struct MacroNodeDefinition {
    position: MacroPosition,
    dispatch: MacroDispatch,
    cases: Vec<NotaMacroNodeDefinition>,
}
```

But every case inside `cases` already carries its own `PositionPredicate` derived from `position.position_predicate()` (see lines 327, 348, 428, 455, 556, 575 — every constructor pipes the SAME position predicate into every case). So the wrapper-level `position` field is redundant with the per-case position carried by each nota `MacroNodeDefinition`. The wrapper exists effectively to:

1. Carry a `MacroDispatch` enum (`RootPositional` / `Structural` / `TaggedInvocation` / `StructuralOrTaggedInvocation`, lines 583-588) — but `MacroDispatch` is only consulted at ONE site (line 540 `accepts_tagged_invocation`), and the four variants reduce to a single boolean question. That's a single boolean dressed as an enum.
2. Group cases by position (so `MacroRegistry::node_definition(position)` can find them). But the nota-next `MacroRegistry` could be queried directly by `PositionPredicate` with the same effect.
3. Be a closure for the static constructor methods (`root_imports()`, `namespace_declaration()`, `struct_fields()`, `enum_variants()`, `type_reference()`, etc.). Those COULD live as static constructors on a typed nota-next builder.

Concretely: `MacroNodeDefinition::matches` (line 508) builds a fresh `NotaMacroRegistry::unchecked(self.cases.clone())` on every call and dispatches; `unsupported_structure_error` (line 514) does the same dance to harvest the no-match diagnostic. Both are cheap glue around what nota-next already exposes; both could be one method on a richer nota-next type.

The wrapper has informational mass close to zero. If schema-next contributes the `MacroDispatch` boolean and the position grouping back into nota-next as a thin profile on `nota_next::MacroRegistry` (or just removes the wrapper entirely and stores `Vec<NotaMacroNodeDefinition>` indexed by position), the wrapper disappears. That's ~290 lines of `MacroNodeDefinition` code retiring.

Per spirit 1263 (Maximum, *"Macros are a NOTA-LAYER concept, not just a Schema-layer concept"*), the wrapper is precisely the layering schema-next was meant to delete. It exists today because the nota-next surface has a sharp edge (positional grouping, dispatch profiles) that schema-next had to smooth over locally.

## Finding 5: `AsschemaStore` repeats redb transaction scaffolding 4× per write/read pair

`src/store.rs` is 202 lines, just landed at `84ce382`. The transaction pattern repeats in:

- `put_binary_bytes` (lines 59-87): `begin_write → open_table → insert → commit`, four `.map_err(|error| SchemaError::SemaDatabase { operation: SemaDatabaseOperation::X, ...})` clauses.
- `get_artifact` (lines 89-117): `begin_read → open_table → get`, three `.map_err(...)`.
- `len` (lines 138-156): `begin_read → open_table → len`, three `.map_err(...)`.
- `ensure_tables` (lines 162-184): `begin_write → open_table → commit`, three `.map_err(...)`.

That's 13 occurrences of the same `.map_err` to `SemaDatabaseOperation::X` pattern in 200 lines (`grep -c "SchemaError::SemaDatabase"` returns 14). The `SemaDatabaseOperation` enum (`src/engine.rs:169-178`) has seven variants — `Open`, `BeginRead`, `BeginWrite`, `OpenTable`, `Read`, `Write`, `Commit` — and every redb call site spells one out by hand.

This is the right place to extract a thin scoped-transaction helper:

```rust
struct AsschemaTable<'database> {
    transaction: redb::WriteTransaction,
    table: redb::Table<'database, &'static str, &'static [u8]>,
}

impl AsschemaTable<'_> {
    fn open_write(database: &Database) -> Result<Self, SchemaError> { /* one place for BeginWrite + OpenTable */ }
    fn open_read(database: &Database) -> Result<ReadOnlyTable, SchemaError> { /* one place for BeginRead + OpenTable */ }
    fn put(&mut self, key: &str, bytes: &[u8]) -> Result<(), SchemaError> { /* Write op-map */ }
    fn commit(self) -> Result<(), SchemaError> { /* Commit op-map */ }
}
```

Every public method on `AsschemaStore` becomes 3-4 lines instead of 15-25. The `SemaDatabaseOperation` enum stays (it's a real diagnostic vocabulary) but is spelled exactly once per variant inside the helper.

Stage-5 consequence: there is no reason the same redb-scaffolding will not be needed for a future `SignalStore`, `NexusStore`, `SemaStore`, `SchemaUpgradeStore` (Spirit 1254 Gap D's upgrade artifact). The helper drains the same boilerplate from each.

## Finding 6: `TypeReference` hand-written codec is ~50 lines because of the legacy aliases; the nesting itself is normal

`src/asschema.rs:660-713`. The full `NotaDecode`/`NotaEncode` impl for `TypeReference` is hand-written.

The shape:

- `NotaDecode` (lines 661-698): demote_to_string → match scalar names (`String`/`Integer`/`Boolean`/`Path`) → fall through to `expect_children(Parenthesis, ..., 2)` then match `Plain` / `Vector` / `Optional` / `Map`.
- `NotaEncode` (lines 700-713): match variants → format strings with bare scalar names for the four scalars and parenthesized forms for `Plain`/`Vector`/`Map`/`Optional`.

Is this fundamentally necessary? Partly. The reason it can't be `#[derive(NotaDecode, NotaEncode)]` cleanly is that the four scalar variants want to round-trip as **bare atoms** (`String`, `Integer`, `Boolean`, `Path`) — without a parenthesized record wrapper. The default derive would emit `(String)` / `(Integer)` etc., because that's the nota convention for unit-variant enums in an enum-typed position. There's no way today to tell the nota derive *"this variant prints bare"*.

So this is a substrate gap: nota-next is missing a `#[nota(bare)]` per-variant attribute (or some equivalent — `#[nota(transparent_unit)]`) that says "emit this unit variant as its bare name, no parens." The same mechanism would solve other consumers' bare-name needs (Spirit's `Magnitude`, schema's `MacroPosition`, anything where the variant name reads naturally as a symbol).

The recursive `Box<TypeReference>` part is fine — the rkyv `omit_bounds` annotations at lines 652-657 already handle the rkyv-archive recursion; the nota derive could descend into the box transparently. The `Map(Box, Box)` shape's special two-child payload (lines 768-779 `from_nota_map_payload`) is real schema vocabulary, not codec stress — it could survive as a hand-written impl IF the rest were derived, or could be expressed via a per-variant nota attribute (`#[nota(grouped)]`).

The fact that schema-next needs ~50 lines of hand-rolled codec for `TypeReference` AND ~25 lines for `Name` (`src/asschema.rs:63-77`, where `Name` emits as bare symbol when the symbol predicate holds and as `[bracket-string]` otherwise) tells you the nota-next derive surface doesn't yet have variant-level emission overrides. Both of these are substrate gaps in nota-next; schema-next is paying the rent twice.

## Finding 7: the `Raw → Syntax → Asschema` pipeline is three parallel data models with parallel methods

| Position | Raw | Syntax | Asschema |
|---|---|---|---|
| Top container | `RawSchemaFile` (raw.rs:7) | `SyntaxSchema` (syntax.rs:8) | `Asschema` (asschema.rs:96) |
| Entry / declaration | `RawDatatypeEntry` (raw.rs:126) | `SyntaxDatatype` (syntax.rs:47) | `Declaration` (asschema.rs:363) |
| Struct/enum/newtype | `RawNotaDatatype::PipeBrace/PipeParenthesis/Atom` (raw.rs:142) | `SyntaxStructDeclaration` / `SyntaxEnumDeclaration` / `SyntaxKeyValueDeclaration` (syntax.rs:102/242/369) | `StructDeclaration` / `EnumDeclaration` / `NewtypeDeclaration` (asschema.rs:464/602/442) |
| Type ref | `RawNotaDatatype::Record/Atom` | `SyntaxReference` (syntax.rs:412) | `TypeReference` (asschema.rs:646) |

Each layer's methods (`from_blocks`, `from_raw`, `from_path_and_source`, `name`, `fields`, `variants`) replicate the same projection shape: parse the next layer down → walk objects → wrap each one as the layer-specific noun.

This is the legacy `SyntaxSchema` layer (preserved per `ARCHITECTURE.md §"Syntax Schema Layer"` while the macro engine migrates to strict key/value authored schema). It's documented as legacy, but the data-model parallelism remains: every new field in `Asschema` has the potential to need a mirror in syntax. As long as the `syntax` layer exists, every shape change is paid for twice.

Per the architecture doc, the live path is `RawSchemaFile → SchemaEngine → Asschema` (the syntax layer is parallel, not in the live macro pipeline). The cleanup is just to retire `syntax.rs` once the fixtures it carries (`tests/syntax_layer.rs`) migrate to the strict key/value form. That's a ~570-line file that's structurally dead-but-not-yet-deleted. Not a design *improvement* per se, just structural debt that's already named in the architecture and waiting on the fixture migration to land.

Lower-impact than findings 1-6, but flagged because the parallel data models contribute to the "feels like there's too much code" pressure that motivates this audit.

## Finding 8: `SchemaNodeDelimitedNotation` (asschema.rs:1273-1309) and `DelimitedNotation` (declarative.rs:1828-1864) are the same struct with the same methods

Both wrap a `Delimiter`, expose `opening()` / `closing()` / `wrap(children: &[String])`. Identical 35-line impls. Both should be one type at the nota-next layer (or a method on `Delimiter` itself — `Delimiter::wrap_notation_children(&[String]) -> String`). The fact that this got copy-pasted between two modules in the same crate is a smell that the "delimiter to text notation" surface lives in the wrong place.

Same goes for `NotationBlock::compact_notation` (declarative.rs:1810) and `SchemaNodeNotation::compact` (asschema.rs:1254) — two near-identical "walk a Block back into compact text" implementations. Both are answering "given a parsed Block, give me a text re-emit." That's a `Block::reemit_compact()` method on nota-next's `Block` — schema-next has had to invent it twice because nota-next didn't expose it.

## Top 3 broad improvements for schema-next (ordered by impact × scope)

### 1. Drop the text round-trip from declarative macro lowering (Finding 3)

**Impact**: highest semantic punch. Directly resolves Spirit 1280 (Maximum) and Spirit 1263 (Decision) violations IN the live macro engine. Removes a `Block → String → Document::parse → Block` round-trip that fires on every macro expansion. Eliminates ~150 lines of stringly-typed substrate (`MacroBindings` value storage, `ExpandedTemplate::lower_to_output`, the `Document::parse(&self.source)` middle hop, the `NotationBlock::compact_notation` callsites at line 732 and 837).

**Scope**: internal to `src/declarative.rs`. Type signatures of `MacroBindings`, `ExpandedTemplate`, `MacroTemplate::expand`, and the `Capture/RestCapture/Atom/Delimited` traversal methods change; the public `DeclarativeMacroLibrary` and `MacroLibraryArtifact` API don't change.

**Why it's #1**: it's the only finding here that's both a Spirit-Maximum violation AND a substrate gap entirely fixable inside schema-next without nota-next changes. Findings 1, 4, 5 also need a nota-next companion change (artifact trait, position-grouped registry, scoped transaction helper) or have lower semantic stakes; Finding 3 is a self-contained schema-next refactor with a Maximum-certainty intent record naming the design.

### 2. Extract `SerializableArtifact<T>` so artifact-IO lives once (Finding 1)

**Impact**: removes ~160 lines of literal duplication TODAY between `AsschemaArtifact` and `MacroLibraryArtifact`. Stage-5 consequence is multiplicative: every additional artifact-owning type (Spirit 1254 Gap D's `SchemaUpgradeArtifact`, the schema-emitted Signal/Nexus/SEMA artifacts, RustModule-data artifacts, MacroTable artifacts) inherits the trait instead of re-copying 80 lines. Per the architecture doc's pattern, EVERY noun in the asschema four-object separation (Asschema / AsschemaArtifact / AsschemaStore / RustEmitter, per Spirit 1272) eventually wants an artifact owner. That's at least 6-8 artifact types when the stack is built out.

**Scope**: a new trait inside schema-next (or even better, inside nota-next so other consumers can also benefit — the artifact-IO pattern isn't schema-specific, it's "anything with NotaDecode + rkyv + a file path"). The trait owns the eight methods + the path-error projection. `AsschemaArtifact` and `MacroLibraryArtifact` shrink to ~10 lines each.

**Why it's #2**: maximum line-count reduction with minimal mechanism. Less semantically deep than Finding 3, but pure mechanical elimination of duplication with clean horizon implications. The current code is what Spirit 1272's "separated typed-object responsibilities" wants but each owner is paying full artifact rent independently.

### 3. Drain the redb transaction boilerplate from `AsschemaStore` (Finding 5)

**Impact**: removes ~80 lines of per-method redb scaffolding inside `store.rs` (currently ~140 of 202 lines is `begin_X → open_table → operation → map_err` repetition). Slightly less immediate impact than Finding 1 but the multiplicative future scope is the same: every Store noun the architecture wants (SignalStore, NexusStore per Spirit 1270's plane separation, the SEMA store family) re-pays the same scaffolding.

**Scope**: a private `AsschemaTable` helper inside `src/store.rs` (or in a `sema-storage` substrate if multiple stores emerge — operator's call). The `SemaDatabaseOperation` enum stays as the typed diagnostic vocabulary; the `.map_err` lines drop from 13 to 7 (once per enum variant, inside the helper).

**Why it's #3**: smaller absolute line reduction than Findings 1 and 3, but it touches `84ce382` — the most recently landed code in this scope — which means it locks the pattern before the boilerplate is paved into more stores. Operator just shipped the first redb-backed store; if the helper lands now, every subsequent store gets it free.

## Cross-cutting observations (for the synthesis report)

- **Substrate gaps in nota-next that schema-next is paying twice for**: variant-level bare-emission attribute (Finding 6 — `Name` + `TypeReference::String/Integer/Boolean/Path` both pay for this), Block re-emit method (Finding 8 — `NotationBlock` + `SchemaNodeNotation` both invent it), known-root document codec (Finding 0 + designer 442). All four are likely cheap to add to nota-next and would remove ~150 lines of schema-side glue.
- **Wrapper layer thinness**: the `schema-next::MacroNodeDefinition` wrapper (Finding 4) is the second time in this audit set (alongside operator 261's macro-node-stack work) that a schema-side wrapper has been flagged as adding zero new information over the nota-next type. Pattern hint: schema-next's contribution should be the **handlers** (Block → typed schema fragment) and the **vocabulary** (the position predicates, the case constructors), not parallel data structures.
- **Parallel data types signal under-engineered generics**: `MacroPatternData` vs `MacroTemplateData` (Finding 2), `AsschemaArtifact` vs `MacroLibraryArtifact` (Finding 1), `Raw*` vs `Syntax*` vs `*Declaration` (Finding 7). Each parallel pair is a place where one parameterised noun would carry the same semantics.
- **The "happens to work" middle hops are the real anti-patterns**: text round-trip in macro lowering (Finding 3), six-element hand-built `NotaDocumentEncoding::new(vec![...])` in `Asschema::to_nota_document_body` (Finding 0), `Name::new("Input")` fabricated inside the decode body (Finding 0). All three produce the right answer; all three carry a future-cost that the Spirit log already names.
