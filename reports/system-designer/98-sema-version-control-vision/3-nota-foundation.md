# 98/3 — nota-next — typed structural codec audit and parsing-bypass sweep

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
An independent adversarial verifier re-checked every key claim against the code; its verdicts are appended at the end of this file.*

# NOTA Language Audit: Type-Directedness and Codec Strictness

## Executive Summary

The psyche's belief that "NOTA is positional, very strict, fully typed; there should not be any custom parsing outside of it" is **substantially correct at the nota-next layer** but **faces a significant counterexample in schema-next**, where the `MacroLibrarySourceEntry` parsing bypasses the derived codec in favor of stringly-typed manual dispatch. The codec itself is bidirectional, canonical, and fully type-directed when used. However, higher layers make a deliberate choice to hand-parse NOTA-like structures for declarative macro definitions.


## 1. Codec Shape: NOTA Structural Macro Node Implementation

### Type-Directed Decoding (Fully Top-Down)

The structural macro node codec is entirely type-directed from the top down:

1. **Dispatch Entry Point** (/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:715-731): When `from_structural_candidate` is called, it first tries fast-path direct decoding if the candidate holds a single block; otherwise, it constructs a typed `StructuralVariantSet` from the enum's declared variants and calls `.dispatch(candidate)`.

2. **Variant Ordering and First-Match** (/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:669-678): The derive macro iterates `data.variants.iter()` in declaration order (line 671), collecting `StructuralVariantDerive` instances. These are then emitted in order into the `structural_variants()` method (lines 692-696), which produces a vector preserving declaration order.

3. **Declaration-Order Dispatch** (/git/github.com/LiGoldragon/nota-next/src/macros.rs, dispatch impl): The `StructuralVariantSet::dispatch` method loops through `self.variants()` in order (line in macros.rs checks `for variant in self.variants()`) and returns the first match; no tie-breaking, no fallback.

4. **Recursive Field Decoding** (/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:814): After a variant matches structurally, each field is decoded via `<#field_type as ::nota_next::StructuralMacroNode>::from_structural_block(#block)`, which recursively applies the same type-directed process. There is no untyped intermediate representation.

5. **Shape Attributes Enforce Structural Contracts** (/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:767): Each variant carries a `StructuralVariantShape` (parsed from `#[shape(...)]` attributes) that specifies the expected delimiter, arity, and atom case. The derive macro generates direct-match conditions (line 786) that fail fast if the block doesn't conform, so only structurally valid blocks can enter the field-decode phase.

### Source Spans and Error Reporting

- **Span Preservation** (/git/github.com/LiGoldragon/nota-next/src/parser.rs:68-73): Every `Block` carries a `SourceSpan` with byte, line, and column positions (lines 68-73). The parser thread all the way to the leaf.
- **Error Types** (/git/github.com/LiGoldragon/nota-next/src/codec.rs:6-40): `NotaDecodeError` includes span-adjacent context (type name, expected delimiter, variant names, etc.). Field-level decode errors carry node, variant, and field indices (nota-next/derive/src/lib.rs:815-820), enabling precise diagnostics.

### Encode-Back: Bidirectional and Canonical

- **Canonical String Emission** (/git/github.com/LiGoldragon/nota-next/src/codec.rs:465-502): `NotaString::format()` (lines 465-478) emits bare atoms when eligible, bracket strings `[...]` for inline strings, and pipe-text `[|...|]` for strings containing delimiters or special markers. Decoding rejects redundant delimiters (line 495-502), raising `NonCanonicalStringDelimiter` if a bracket or pipe string is decoded but the value qualifies as a bare atom.
- **Structural Macro Encode** (/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:733-737): Each variant's encode arm (generated via `StructuralVariantDerive::encode_arm`, line 826-840) pattern-matches the Rust enum and reconstructs the NOTA surface by recursively calling `to_structural_nota()` on fields.
- **No Quotes in Bare Atoms** (INTENT.md line 48): "Typed `String` decoding rejects redundant bracket or pipe delimiters when the decoded text is eligible for bare atom formatting." This is implemented in `NotaString::reject_redundant_delimiter()` (codec.rs line 495).


## 2. Strictness Audit: The Stringly-Typed Escape Hatch

### The Codec Is Strict, But Hand-Parsing Exists

The `NotaDecode`/`NotaEncode` derive traits produce fully typed codecs with **no stringly-typed escape hatches** when used as intended. However, `schema-next` implements a secondary manual parser for declarative macro definitions that **does bypass the codec**:

**Bypass #1: `MacroLibrarySourceEntry` Hand-Parsing** (/git/github.com/LiGoldragon/schema-next/src/declarative.rs:693-698, 752-754)

```rust
// Line 695-698: Stringly-typed dispatch
match record.variant_name()?.as_str() {
    "SchemaMacro" => Ok(Self::SchemaMacro(SchemaMacro::from_record(record)?)),
    _ => Err(record.expected_source_entry_error()),
}

// Line 752-754: Hand-parsing via demote_to_string
fn variant_name(&self) -> Result<Name, SchemaError> {
    self.child(0).schema_name()  // Extracts symbol from child, then converts to string
}
```

- `MacroLibrarySourceEntry` derives `NotaDecode`/`NotaEncode` (line 19-24), so a typed codec exists.
- But `MacroLibrary::from_source` (lines 43-49) manually parses document blocks, constructs `MacroLibrarySourceEntryRecord` (a shallow wrapper), and calls `MacroLibrarySourceEntry::from_block`, which extracts the variant discriminator via `record.variant_name()?.as_str()` and pattern-matches the string.
- The typed path (`from_nota_source`, line 70-71) delegates to `NotaSource::new(source).parse::<Self>()`, which uses the derived codec—but this path is **not the default** for reading `.schema` files (the `builtin_source()` method uses `from_source` instead).

**Characteristics:**
- Pattern-matches extracted symbol names as strings without consulting the Rust type system.
- No structural shape enforcement (the code assumes a fixed 5-object parenthesized structure without validation).
- Only one variant exists currently (`SchemaMacro`), making the dispatch vacuous but the plumbing still present.

**Other Hand-Parsing Sites:**
- Macro expansion template dispatch (lines 1408-1424): Matches extracted symbol heads (`"Type"`, `"Fields"`, `"Variants"`, `"Reference"`) as bare strings.
- Variant signature parsing (source.rs) uses typed `StructuralMacroNode` for the core variant struct but may have manual fallback paths for some edge cases.

### Direct Use of `demote_to_string()` in Manual Implementations

Several types in `schema-next/src/schema.rs` implement `NotaDecode`/`NotaEncode` by hand, using `demote_to_string()` to extract variant discriminators (e.g., `SymbolPath`, line 174). This is not a bypass—it's expected in hand-written enum codec implementations where the Rust type itself is not derive-generated. The public API types are still the Rust types; the hand-parsing is internal to those trait implementations.


## 3. Parsing-Bypass Sweep Results

### Search Scope
Grepped `/git/github.com/LiGoldragon/{spirit,signal-spirit,meta-signal-spirit,schema-next,schema-rust-next,sema,sema-engine,signal-sema,nota-config,triad-runtime,orchestrate,signal-orchestrate,repository-ledger,introspect}` for:
- `winnow`, `nom`, `pest`, `chumsky` → **No matches** (except chronos, which is unrelated).
- `regex::`/`Regex::new` → **No matches**.
- `.split(` outside of legitimate contexts → **One match**: `schema-next/src/schema.rs:27` in `Name::namespace_segments()`, which splits a namespace path on `:` (legitimate).
- `parse::<...>` outside of type-directed `NotaSource::parse` → **Legitimate numeric parsing only**: `parse::<u64>()` for fixed-byte widths (source.rs:1648), arity counts, etc.
- `std::env::var` → **Two matches**: socket path env vars in `spirit/src/bin/{spirit.rs, meta-spirit.rs}` (legitimate system integration).

### Legitimate Parsing Contexts

1. **Number/Dimension Parsing**: `parse::<u64>()` for byte widths in `FixedBytes` references (schema-next:1648). Legitimate because these are schema type parameters, not NOTA-layer values.
2. **Namespace Path Splitting**: `Name::namespace_segments()` splits on `:` to decompose qualified names (schema-next:27). Legitimate because namespace paths are a vocabulary concept above NOTA.
3. **Socket Path Environment**: SPIRIT_SOCKET and SPIRIT_META_SOCKET env vars for IPC. Legitimate system integration.

### Real Bypasses (Ranked by Impact)

| Bypass | Location | Severity | Status | Workaround Exists? |
|--------|----------|----------|--------|-------------------|
| `MacroLibrarySourceEntry::from_block()` stringly-typed dispatch | schema-next/src/declarative.rs:695-698 | **HIGH** | Transitional (typed path exists via `from_nota_source`) | Yes: use `NotaSource::parse::<MacroLibrary>()` |
| Macro expansion template head dispatch (`match head.as_str()`) | schema-next/src/declarative.rs:1408-1424 | **MEDIUM** | Active in macro lowering path | No direct typed alternative visible |
| Manual enum variant discriminator extraction | schema-next/src/schema.rs:174-184, spirit/src/schema/\*.rs | **LOW** | Expected (hand-written codec impls) | N/A (internal to codec) |


## 4. Legacy Seam: Old `nota` vs `nota-next` Status

**Finding: Fully Migrated**

- No `nota` crate in the workspace; only `nota-next`.
- All Cargo.toml dependencies point to `nota-next` (git branch main):
  - `spirit/Cargo.toml:67`
  - `schema-next/Cargo.toml:16`
  - `nota-config/Cargo.toml:14`
  - And all derived crates transitively.
- The `-next` suffix is **not pending removal**; it is the canonical name. INTENT.md (lines 8, 119) refers to it as the "replacement track on `main`."


## 5. Three Worst Counterexamples (Ranked)

### 1. **MacroLibrarySourceEntry Stringly-Typed Dispatch** (schema-next/src/declarative.rs:695-698)

**What it does**: Manually extracts the first child of a 5-child parenthesized block, converts it to a symbol, and matches the symbol's text string against a hardcoded variant name. No type-system guidance.

**Why it violates the principle**: The enum `MacroLibrarySourceEntry` has a derived codec that would guide type-directed parsing, but the `from_source` method bypasses it entirely. Even though only one variant (`SchemaMacro`) exists, the code structure invites future variants to be added as new string cases in a match statement, not as enum variants.

**Impact**: Users reading schema `.schema` files via `MacroLibrary::builtin_source()` get routed through this hand-parsed path. The typed path (`from_nota_source`) exists but is not the default public API path.

**Unforced error**: The stringly-typed dispatch is unnecessary; the code could simply construct the enum and use its derived codec directly.


### 2. **Macro Expansion Template Head Dispatch** (schema-next/src/declarative.rs:1408-1424)

**What it does**: Extracts the first child of a parenthesized macro expansion instruction (`(Type ...)`, `(Fields ...)`, etc.), demotes it to a string, and matches on the string literal.

```rust
match head.as_str() {
    "Type" => MacroExpansionType::new(...),
    "Fields" => MacroExpansionFields::from_objects(...),
    ...
}
```

**Why it violates the principle**: No structural macro node or enum codec guards this decision. The variant keywords are embedded in pattern-match strings rather than represented as Rust enum variants.

**Impact**: Moderate—these are schema-level macros, not user code, so the impact is limited to schema engine internals. But adding a new expansion template requires touching both the enum definition and this string-match statement.


### 3. **Manual Hand-Parsing of Schema Structures** (schema-next/src/declarative.rs, multiple sites)

**What it does**: Functions like `MacroLibrarySourceEntryRecord::new()` (line 735-743), `MacroLibrarySourceEntryRecord::variant_name()` (line 752-754), and similar manual extractors use index-based child access (`.child(0)`, `.child(1)`, etc.) without enforcing schema via the codec.

```rust
fn variant_name(&self) -> Result<Name, SchemaError> {
    self.child(0).schema_name()  // Positional, unguarded
}
```

**Why it violates the principle**: Decoding is positional and manual, not guided by the Rust type. If the schema changes (e.g., a field is inserted), the indices must be manually updated in multiple places.

**Impact**: Low—the code is localized to schema parsing, and it works. But it is not "fully typed" in the sense the psyche means; the Rust compiler cannot verify positional correctness.


## 6. Verdict on the Psyche's Belief

**Claim**: "NOTA is positional, very strict, fully typed; there should not be any custom parsing outside of it."

**Assessment**: **Partially upheld, with important caveats.**

### What's True:
1. **The nota-next codec itself is fully typed, strict, and bidirectional.** Every value shape (struct, enum, vector, map, option) is represented as a Rust type with derived or hand-written `NotaDecode`/`NotaEncode` implementations. Decoding is entirely type-directed; no untyped intermediate tree-walking.
2. **The StructuralMacroNode system is fully typed and declaration-order-first-match.** Variants are matched in the order declared in the Rust enum; structural patterns are validated before field decoding; encode-back is canonical (bare atoms when eligible, no redundant delimiters).
3. **Source spans and error reporting are first-class.** Every block carries position information, and codec errors include type/field context for diagnostics.

### What's Not Fully True:
1. **schema-next hand-parses NOTA-like structures for schema declarations.** `MacroLibrarySourceEntry` and macro expansion templates use stringly-typed string matching to discriminate variants, bypassing the codec layer. This is a deliberate design choice (the declarative macro definition format is not schema-generated), but it means the highest layers of the stack do engage in custom text parsing.
2. **The hand-parsing is positional and manual.** Functions like `MacroLibrarySourceEntryRecord::variant_name()` use `.child(0)` indexing without enforcing structure via the type system.

### Constructive Reading:
The psyche likely means: "**NOTA values themselves (once parsed into blocks) should be decoded into Rust types without custom parsing.**" This is **entirely true**. The bypassses occur at the schema-declaration level (how to represent macros, templates, etc. in source files), which is a layer above NOTA value decoding. If those declarations were schema-generated, they too would be fully typed.


## Recommendations

1. **Migrate `MacroLibrarySourceEntry::from_source()`** to use `NotaSource::parse::<MacroLibrary>()`. The hand-parsing is code duplication over a type-driven alternative.
2. **Define macro expansion templates as a StructuralMacroNode enum**, replacing the string-match dispatch with type-directed pattern matching. Variants would be `Type(...)`, `Fields(...)`, `Variants(...)`, `Reference(...)`.
3. **Audit schema-next/src/declarative.rs for positional assumptions.** Any indexed `.child(N)` access should be replaced with codec-driven field access or explicit shape validation.
4. **Document why hand-parsing exists**: if it's intentional (e.g., for schema forward-compatibility), make the rationale clear in code comments and architecture docs.



## keyClaims
- CLAIM: StructuralMacroNode decoding is type-directed all the way down, using Rust enum variants (not strings) as discriminators, with variants matched in declaration order and field types recursively decoded via StructuralMacroNode trait bounds.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:715-731 (from_structural_candidate dispatches typed variants); src/macros.rs dispatch loop (iterates variants in order); derive/src/lib.rs:814 (recursive StructuralMacroNode field decode)
- CLAIM: String encoding is bidirectional and canonical: bare atoms emit without delimiters when eligible, bracket strings [x] when needed for whitespace, pipe-text [|...|] for delimiters; decoding rejects redundant delimiters as non-canonical.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/src/codec.rs:465-502 (NotaString::format and reject_redundant_delimiter); INTENT.md:46-49 (canonical formatting contract)
- CLAIM: MacroLibrarySourceEntry bypasses its derived NotaDecode codec in favor of stringly-typed hand-parsing via from_block(), matching extracted symbol names as strings rather than using the Rust type system.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:19-24 (derives NotaDecode); 43-49 (from_source hand-parses); 695-698 (variant_name().as_str() string match); 752-754 (variant_name extracts first child via demote_to_string)
- CLAIM: Variant dispatch is declaration-order first-match: the derive macro iterates data.variants.iter() in order, emits them into structural_variants() in that order, and StructuralVariantSet::dispatch loops variants in order returning the first match.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:669-695 (iterate data.variants in order, emit to vec); src/macros.rs dispatch (for variant in self.variants()) returns first Ok
- CLAIM: No regex, pest, nom, winnow, or chumsky usage in the active stack (spirit, schema-next, sema, nota-config); only nota-next codec and type-directed parsing.
  EVIDENCE: grep -rn 'winnow|nom|pest|chumsky' across repos returns no hits; grep 'regex::' returns no hits; all parse::<> outside of NotaSource are legitimate numeric/env parsing
- CLAIM: Source spans are preserved end-to-end: every Block carries SourceSpan with byte/line/column; codec errors include type/variant/field context for diagnostics.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/src/parser.rs:68-73 (Block carries SourceSpan); codec.rs:6-40 (NotaDecodeError types); derive/src/lib.rs:815-820 (field error includes node/variant/field indices)
- CLAIM: No old 'nota' crate in workspace; all dependencies are nota-next on branch main; the -next suffix is the canonical name, not a temporary suffix.
  EVIDENCE: ls /git/github.com/LiGoldragon | grep nota shows only nota-next and nota-config; all Cargo.toml deps reference nota-next; INTENT.md line 119 calls it 'the replacement track on main'
- CLAIM: Macro expansion template dispatch (Type/Fields/Variants/Reference) uses stringly-typed match on extracted symbol heads without codec guidance, requiring string literals for variant discrimination.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:1408-1424 (match head.as_str() on string literals; no StructuralMacroNode or enum codec)
- CLAIM: Manual schema structure parsing via positional child indexing (.child(0), .child(1), etc.) does not enforce schema via the type system; if schema changes, indices must be manually updated.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:735-754 (MacroLibrarySourceEntryRecord uses .child(index) without validation); 746-750 (child method definition, unguarded indexing)
- CLAIM: The typed codec path exists and works (from_nota_source delegates to NotaSource::parse), but is not the default for reading user-authored .schema files; from_source (hand-parsed) is used by builtin_source().
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:36 (builtin() uses from_nota_source); 40 (builtin_source() uses from_source); 70-71 (from_nota_source uses NotaSource::parse)

## openQuestions
- Is the schema-next hand-parsing (MacroLibrarySourceEntry, macro expansion templates) intentional for forward-compatibility with user-defined schema extensions, or is it legacy that should be migrated to typed codecs?
- Why is from_source (hand-parsed) used by builtin_source() instead of from_nota_source (typed)? Is there a semantic difference in how the two paths interpret the schema file format?
- Does the stringly-typed dispatch in macro expansion templates block adding new template kinds, or is it extensible enough that future additions can follow the pattern without breaking the constraint?
- Are there plans to migrate MacroLibrarySourceEntry and macro template dispatch to StructuralMacroNode, or is the current hand-parsing considered acceptable schema-layer code?


## Adversarial verification verdicts

- [CONFIRMED] StructuralMacroNode decoding is type-directed all the way down, using Rust enum variants (not strings) as discriminators, with variants matched in declaration order and field types recursively decoded via StructuralMacroNode trait bounds.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:671-677 (data.variants.iter() in order, mapped to structural variants); :814 (recursive field decode via <#field_type as ::nota_next::StructuralMacroNode>::from_structural_block); :476-480 (dispatch loop iterates self.variants() in order, returns first Ok match)
- [CONFIRMED] String encoding is bidirectional and canonical: bare atoms emit without delimiters when eligible, bracket strings [x] when needed for whitespace, pipe-text [|...|] for delimiters; decoding rejects redundant delimiters as non-canonical.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/src/codec.rs:465-479 (NotaString::format() logic for bare/bracket/pipe-text); :495-502 (reject_redundant_delimiter() returns error if eligible for bare atom); :351-365 (parse_string calls reject_redundant_delimiter on lines 354, 364)
- [CONFIRMED] MacroLibrarySourceEntry bypasses its derived NotaDecode codec in favor of stringly-typed hand-parsing via from_block(), matching extracted symbol names as strings rather than using the Rust type system.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:19-24 (derives NotaDecode); :693-699 (from_block hand-parses, only call path); :695 (variant_name().as_str() string match); :752-753 (variant_name extracts first child via schema_name() -> atom text)
- [CONFIRMED] Variant dispatch is declaration-order first-match: the derive macro iterates data.variants.iter() in order, emits them into structural_variants() in that order, and StructuralVariantSet::dispatch loops variants in order returning the first match.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:671-677 (iterate data.variants in order, collect to vec); :692-695 (emit vec in same order); /git/github.com/LiGoldragon/nota-next/src/macros.rs:476-480 (for variant in self.variants() returns first Ok match)
- [CONFIRMED] No regex, pest, nom, winnow, or chumsky usage in the active stack (spirit, schema-next, sema, nota-config); only nota-next codec and type-directed parsing.
  EVIDENCE: grep -E 'winnow|nom|pest|chumsky|regex' across /git/github.com/LiGoldragon/{spirit,schema-next,sema,nota-config,nota-next}/Cargo.toml returns zero hits
- [CONFIRMED] Source spans are preserved end-to-end: every Block carries SourceSpan with byte/line/column; codec errors include type/variant/field context for diagnostics.
  EVIDENCE: /git/github.com/LiGoldragon/nota-next/src/parser.rs:68-73 (Block carries SourceSpan, source_span() method); /git/github.com/LiGoldragon/nota-next/src/macros.rs:1348-1352 (StructuralMacroNodeError::Field includes node, variant, field indices); :815-819 (field decode error includes node, variant, field index)
- [CONFIRMED] No old 'nota' crate in workspace; all dependencies are nota-next on branch main; the -next suffix is the canonical name, not a temporary suffix.
  EVIDENCE: ls /git/github.com/LiGoldragon/ shows only nota-next and nota-config (no bare 'nota'); grep -r 'nota-next.*branch.*main' across Cargo.toml files confirms all deps use main branch; /git/github.com/LiGoldragon/nota-next/INTENT.md:119-120 ('replacement track on main')
- [CONFIRMED] Macro expansion template dispatch (Type/Fields/Variants/Reference) uses stringly-typed match on extracted symbol heads without codec guidance, requiring string literals for variant discrimination.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:1408-1424 (match head.as_str() on string literals 'Type', 'Fields', 'Variants', 'Reference'); no StructuralMacroNode or enum codec used
- [CONFIRMED] Manual schema structure parsing via positional child indexing (.child(0), .child(1), etc.) does not enforce schema via the type system; if schema changes, indices must be manually updated.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:746-750 (child() method uses unguarded .root_object_at(index).expect()); :752-769 (variant_name/name/position/pattern/template hardcoded to indices 0-4); :738 (only validates count, not field meanings)
- [CONFIRMED] The typed codec path exists and works (from_nota_source delegates to NotaSource::parse), but is not the default for reading user-authored .schema files; from_source (hand-parsed) is used by builtin_source().
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/declarative.rs:35-36 (builtin() calls from_nota_source); :39-40 (builtin_source() calls from_source); :70-71 (from_nota_source uses NotaSource::parse); :43-50 (from_source hand-parses via from_block)

