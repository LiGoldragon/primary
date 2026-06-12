# 98/4 — schema-next + schema-rust-next — schema-on-NOTA, emission state, the generation seam for VC

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
An independent adversarial verifier re-checked every key claim against the code; its verdicts are appended at the end of this file.*

# Schema-on-NOTA Vision: Implementation Status Report

## 1. SCHEMA-ON-NOTA Deserialization Architecture

**Claim: Schema purely parses through nota-next's structural codec.**

Schema-next implements its schema-on-NOTA promise cleanly. The deserialization entry point is `SchemaSource::from_document(document: &Document)` at `/git/github.com/LiGoldragon/schema-next/src/source.rs:34`, which receives an already-parsed `nota_next::Document` — NOTA owns all text tokenization and structural parsing.

The file reads `.schema` text through two stages:
1. `Document::parse(source: &str)` at line 30 delegates to nota-next for full lexical and structural parsing
2. `SchemaSource::from_document` then calls typed lowering methods like `SourceImports::from_block`, `SourceRootEnum::from_block`, and `SourceNamespace::from_block` — each a `from_block(block: &Block)` pattern that consumes the NOTA-already-parsed `Block` structures

**Hand-rolled parsing check:** The only text-level operations are:
- `Block::demote_to_string()` calls in macro nodes like `SourceVariantName::from_structural_block` at line 1446 (checking if an atom demotes to a symbol string)
- `NotaBlock::new(block).parse_string()` for `Name` codec at schema.rs:61 (delegating through nota-next's codec layer, not a custom parser)

These are **structural metadata queries on already-parsed NOTA blocks, not hand-rolled parsing**. The actual text syntax lives entirely in nota-next's `AtomClassification`, `BlockShape`, and `PatternElement` matching. Schema owns only the semantic mapping: when a block shape matches a position, what does it mean in schema terms?

**Key implementation:** `SourceVariantSignature` derives `nota_next::StructuralMacroNode` at line 1269, making enum variants structural-macro-node types. The derive exposes `SourceVariantSignature::Unit`, `SelfTagged`, `Data`, and `Streaming` cases — one per NOTA structural shape — without any schema-specific lexer or grammar. Variant names use `SourceVariantName`, which implements `StructuralMacroNode` at line 1431, delegating validation to nota-next's `BlockShape::pascal_atom` pattern and symbol classification.

## 2. Canonical Schema-in-Rust Representation

**Claim: `Schema` is the fully-typed, rkyv-serializable round-trip image; resolution lives on types.**

The production schema-in-Rust value is `struct Schema` at `/git/github.com/LiGoldragon/schema-next/src/schema.rs:207`, containing:
```rust
pub struct Schema {
    identity: super::SchemaIdentity,
    imports: Vec<ImportDeclaration>,
    resolved_imports: Vec<super::ResolvedImport>,
    input: EnumDeclaration,
    output: EnumDeclaration,
    namespace: Vec<Declaration>,
    streams: Vec<StreamDeclaration>,
    relations: Vec<RelationDeclaration>,
}
```

This derives `rkyv::Archive, rkyv::Serialize, rkyv::Deserialize` (line 207). It owns methods that resolve symbol paths directly:
- `symbol_path_position(&self, path: &SymbolPath) -> Option<SymbolPathPosition>` at line 341 — the canonical query for resolving a path into a role (Type, RootVariant, Field, EnumVariant)
- `type_named(&self, name: &str) -> Option<&TypeDeclaration>` at line 287
- `root_named(&self, name: &str) -> Option<&EnumDeclaration>` at line 269

**Resolution step completion:** The older "assemble" step is gone. The pipeline is now:
1. `.schema` → `Document::parse` (nota-next)
2. `Document` → `SchemaSource` (typed source nouns: `SourceRootEnum`, `SourceNamespace`, etc.) via `SchemaSource::from_document`
3. `SchemaSource` → `Schema` via `SchemaEngine::lower_schema_source_with_resolver` — at engine.rs line 1 (implied from method names in lib.rs:82-93)

The `SchemaSource` layer owns round-trip through `.schema` text and rkyv archive via `SchemaSourceArtifact`. Once lowered to `Schema`, visibility is baked in (`Declaration` wraps visibility + name + value), inline declarations are hoisted into namespace order, and variant resolution against imports is complete. No second pass, no string reconstruction.

## 3. Emission Status: LowerToRust Token Pipeline

**Claim: String-writer migration is complete; all emission goes through `proc_macro2::TokenStream` + `quote!`.**

The Rust writer god-struct `RustWriter` is gone — no code in `/git/github.com/LiGoldragon/schema-rust-next/src` defines it.

Emission uses a trait-based recursive lowering pattern:
- **`LowerToRust<Target>` trait** at lib.rs:212: each schema noun implements `lower_to_rust(&self, context: &RustLoweringContext) -> Target`
- **Trait coverage** (lib.rs search results): implementations for `Schema`, `ResolvedImport`, `RelationDeclaration`, `RelationValue`, `Declaration`, `TypeDeclaration`, `NewtypeDeclaration`, `StructDeclaration`, `FieldDeclaration`, `EnumDeclaration`, `EnumVariant` — the full schema surface
- **Token-building examples**: 
  - `RustScalarAliasTokens` at line ~1320 implements `ToTokens` (checked in grep results)
  - `EnumVariantConstructorsTokens` at line 4048 implements `ToTokens` 
  - `EnumPayloadFromImplTokens` at line 3983 implements `ToTokens`
  - 40+ token wrapper types across Signal/Nexus/SEMA/upgrade surfaces (full list in grep at lines 1232–2933)

The renderer `RustModuleRenderer::emit_item_tokens` at line 4245 parses the TokenStream as `syn::File` and passes through `RustfmtSkippedItems`, never building Rust text directly. The only string write is `writer.line(format!("// @generated by {}", ...))` at line 278 — required because prettyplease drops non-doc comments.

**Emission scope — what gets produced today:**
1. **Types**: Scalars (String, Integer, Boolean, Path), structs, enums, newtype tuple wrappers, all with derives (rkyv + feature-gated NOTA)
2. **Traits & Impls**: 
   - Inherent impl blocks with constructors: `new()`, `payload()`, `into_payload()` for newtypes (NewtypeInherentImplTokens)
   - Associated constructors per enum variant: `Input::record(entry)` (EnumVariantConstructorsTokens)
   - `From<Payload> for Enum` impls for unique payload types (EnumPayloadFromImplTokens)
3. **Signal-frame codec** (WireContract): `encode_signal_frame`, `decode_signal_frame`, `SignalFrameError`, route enums, short-header module (SignalFrameImplTokens + RouteEnumTokens + ShortHeaderModuleTokens)
4. **Runtime planes** (Signal/Nexus/SEMA): Engine trait (`NexusEngine`, `SemaEngine`), envelope wrappers (`Nexus<T>`, `Sema<T>`), origin routes, plane namespaces, trace object names (TraceObjectNameEnumTokens + PlaneEnvelopeTokens + PlaneNamespaceTokens + runtime trait impls)
5. **Upgrade trait surface**: `UpgradeFrom<Previous>`, `AcceptPrevious<Previous>` (emitted as support, implementation hand-written)
6. **No `VersionProjection`, no `RecordFamily` enum, no per-family decoder** — see below

## 4. Schema Identity & Content Hash

**Claim: No content hash computed anywhere; only manual version identity.**

The only identity mechanism is `struct SchemaIdentity` at engine.rs:27:
```rust
pub struct SchemaIdentity {
    component: Name,
    version: String,
}
```

It holds a **hand-authored version string** — `Version::new("1.0")` style — not a content hash. The crate tests use "Digest" as a field name for *data payloads*, not schema hashes (collections_generated.rs:125, spirit_generated.rs fixture uses a "Digest" newtype field over Bytes or FixedBytes — that's a record field, not a schema versioning mechanism).

**No hash computation present**: grep for blake/sha/digest across both crates returns no hash algorithm imports. `Name` derives `Hash` (schema.rs:14) for use in `HashMap`/`HashSet` internal Rust operations, but there is no computed Blake3/SHA2 digest of the schema text or semantic structure.

**Natural location for hash**: The `SchemaIdentity` noun at `engine.rs:27` would naturally compute a `blake3::hash` of `Schema::to_binary_bytes()` or of the `.schema` source text, emitting it as a method like `SchemaIdentity::content_hash() -> Hash` and storing it alongside or replacing the hand-authored version string. Callers would then emit this as a `pub const SCHEMA_HASH: &[u8] = b"..."` at the module level.

## 5. Generation Seam for Version Control Integration

**Question: Where would RecordFamily enum and family identity land in the emission pipeline?**

If the engine wants, per record family:
- A stable family identity (schema-derived hash)
- A `RecordFamily` enum (closed sum over all top-level declarations/root variants)
- A typed decoder from family tag + bytes → typed value

**The increment would land in `RustModule::render()`** (lib.rs:274). Current structure:
1. `RustModule` holds `declarations`, `root_enums`, `streams`, `relations`, `support`
2. `render()` emits types, inherent impls, route enums, codec, runtime support

**Addition point (medium complexity, ~3 new TokenStream types):**
1. Add `family_identity: Blake3Hash` field to `RustModule` (computed from `Schema::to_binary_bytes()`)
2. Add new section after root enums: **`RecordFamily` enum** — one variant per namespace type + root variant. Module: `enum RecordFamily { Record(u16), Observe(u16), Recorded(u16), ... }`. Emitter: new `RecordFamilyEnumTokens` implements `ToTokens` (similar to `TraceObjectNameEnumTokens` at line 2933)
3. Add **decoder dispatch function**: `fn decode_record_family(tag: u16, bytes: &[u8]) -> Result<RecordFamily, DecodeError>` — a match over family tags, calling the appropriate rkyv decoder (`record_from_bytes`, `observe_from_bytes`, etc.). Emitter: new `RecordFamilyDecoderTokens` implements `ToTokens`
4. Add **family identity export**: `pub const RECORD_FAMILY_SCHEMA_HASH: [u8; 32] = b"..."` — placed at module level before the enum. One-liner in the render path.

The scope is **small-to-medium**:
- No changes to `LowerToRust` trait or schema noun signatures
- New `RustModule` fields: 1 identity, 2 for the enum/decoder nouns
- New token wrappers: 2–3 (enum, decoder, optional hash constant builder)
- Emission call site: add 3 lines in `RustModule::render()` to emit enum, decoder, hash
- Decoder construction: 1 match arm per distinct type in namespace + root variants — scales with schema size

The machinery already exists: `TraceObjectNameEnumTokens` at line 2933 builds a discriminated enum of plane trace events. `RecordFamily` would use the identical pattern but over type names. The decoder is straightforward token-building.

## 6. Conformance Gaps & Workspace Discipline Audit

**Question: Anything violating workspace discipline (free functions, ZST namespaces, stringly-typed cores, hand-rolled parsing)?**

### **Clean areas:**
1. ✅ **No free functions**: All logic lives in trait impls and type methods. Grep for `^pub fn` + `^fn ` in source.rs, engine.rs, schema.rs returns zero matches (test-harness functions excluded)
2. ✅ **No stringly-typed core dispatch**: Route names, object names, trace events are all enum types (RouteEnumTokens, TraceObjectNameEnumTokens, etc.)
3. ✅ **No hand-rolled parsing of schema syntax**: Only NOTA structural queries (`demote_to_string`, `parse_string` on NOTA-provided blocks)
4. ✅ **Full rkyv round-trip**: `SchemaSource::from_binary_bytes`/`to_binary_bytes` (source.rs:138–146), `Schema::from_binary_bytes`/`to_binary_bytes` (schema.rs:386–394)

### **Minor slop identified:**

**1. RustModuleRenderer.line() + format! at lib.rs:278**
```rust
writer.line(format!("// @generated by {}", self.generator_name));
```
This is a **known exemption** — the `// @generated` comment cannot pass through prettyplease (which drops non-doc comments). The intent-doc at daemon_emit.rs:24–26 acknowledges this. No violation.

**2. Six uses of format!() for identifiers in lib.rs**
```rust
format!("{}Route", name.as_str())  // line ~1720 in RouteName
format!("{}Scope", name)             // line ~2822 in PlaneNamespaceAlias
syn::LitInt::new(&format!("0x{:016X}", ...), Span::call_site())  // ShortHeader
```
These are **ident/literal constructors**, not Rust code emission. They build proc_macro2::Ident and Literal values for use in quote! templates. Correct pattern.

**3. daemon_emit.rs:91–95 — upgrade tier socket mode as octal format!**
```rust
let socket_mode = syn::LitInt::new(&format!("0o{bits:o}", Span::call_site());
```
Again, **literal construction, not code emission**. Correct.

### **Architecture at spec:**
- **SourceVariantSignature** structural macro node dispatch: follows workspace pattern (nota-next-layer ownership of pattern matching)
- **SourceVariantName** codec: uses `AtomClassification::classify` from nota-next, not custom symbol validation
- **Schema.symbol_path_position()** resolution: methods on the noun, not free dispatch function
- **TypeReference** codec recursion: each variant owns its lowering through `from_block`, no central string-based dispatcher
- **RustModule** per-noun lowering: `Declaration::lower_to_rust`, `TypeDeclaration::lower_to_rust`, etc. — traits on nouns, not a central walker

No ZST namespaces. All type safety preserved. All codec/lowering machinery trait-based.

### **One genuine gap — not a violation, but incomplete:**

**Asschema retirement is real but semantic-schema storage is absent.** Per INTENT.md line 132–138, the old `.asschema.rkyv` artifact and redb-backed semantic store are deleted. The new pipeline is `.schema` → `SchemaSource` (with `SchemaSourceArtifact` owning `.schema` text + rkyv) → `Schema` (no artifact). However, **there is no production semantic-schema store or query service**. This is by design (per the Constraints section), not a code smell. The engine-layer responsibility is to lower schema once at build time; runtime code references the emitted Rust types. This is architecturally sound but leaves an open question for the VC system: how does sema-engine query schema at runtime if needed? (Answer: through the emitted Rust signatures, not a schema query layer.)



## keyClaims
- CLAIM: Schema-next parses .schema files purely through nota-next's Document::parse, then lowers via from_block methods on StructuralMacroNode types; no custom text parsing or lexer exists outside nota-next.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/source.rs:29–31 (Document::parse entry), lines 53–97 (from_block lowering chain), lines 1431–1461 (SourceVariantName StructuralMacroNode impl)
- CLAIM: The canonical schema-in-Rust representation is struct Schema with rkyv derives and methods like symbol_path_position for resolving paths into semantic roles; the old 'assemble' step is gone.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/schema.rs:207–216 (Schema struct definition with rkyv derives), lines 341–384 (symbol_path_position resolution method)
- CLAIM: String-writer RustWriter god-struct is gone; emission is entirely proc_macro2::TokenStream + quote! through ToTokens trait impls; 40+ token wrapper types cover all schema surfaces including Signal/Nexus/SEMA runtime support.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:212–214 (LowerToRust trait definition), lines 4245–4248 (emit_item_tokens parses TokenStream, no string building), grep results showing ToTokens impls at lines 1232–2933
- CLAIM: No content hash or version projection is computed; only hand-authored SchemaIdentity with version string field exists; no RecordFamily enum or family-tagged decoder present.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/engine.rs:27–47 (SchemaIdentity struct with version: String, no hash method), grep for blake/sha/digest across both repos finds zero algorithm imports, only test fixture field names using 'Digest' as a type name
- CLAIM: A RecordFamily enum + decoder + schema hash would land as 2–3 new ToTokens wrapper types in RustModule::render() pipeline; scope is small-to-medium, reusing existing TraceObjectNameEnumTokens pattern.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:274–350 (RustModule::render with emission call sites), line 2933 (TraceObjectNameEnumTokens as precedent pattern), lines 823–850 (RustDeclaration and LowerToRust impl as structural example)
- CLAIM: No free functions in schema-next core modules; all logic lives in trait impls and type methods; no ZST namespaces or stringly-typed core dispatch.
  EVIDENCE: grep 'fn ' /git/github.com/LiGoldragon/schema-next/src --include='*.rs' excluding tests returns zero matches for module-level functions; RouteEnumTokens (line 1345), TraceObjectNameEnumTokens (line 2933) are enum-based dispatch, not strings
- CLAIM: One format!() call at lib.rs:278 for '// @generated' comment is a documented exemption because prettyplease drops non-doc comments; six other format!() uses are for proc_macro2::Ident/Literal construction, not Rust code text emission.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:278 (// @generated comment), daemon_emit.rs:24–26 (intent doc acknowledging prettyplease limitation), lib.rs:~1720 format!('{Route}') and ~2822 format!('{Scope}') are Ident/Literal builders used in quote! templates

## openQuestions
- Does sema-engine at runtime need schema query capability, or does it operate entirely through emitted Rust type signatures? (The removal of the semantic-schema store leaves this architectural boundary unclear.)
- Should SchemaIdentity compute a blake3/SHA2 hash of Schema::to_binary_bytes() as the canonical version, replacing or supplementing the hand-authored version string?
- Are there daemon crates that currently emit a per-family decoder, or would RecordFamily be a new seam for the VC system?
- Does the psyche intend RecordFamily to cover both top-level namespace declarations and root Input/Output variants, or only one?


## Adversarial verification verdicts

- [CONFIRMED] Schema-next parses .schema files purely through nota-next's Document::parse, then lowers via from_block methods on StructuralMacroNode types; no custom text parsing or lexer exists outside nota-next.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/source.rs:30 (Document::parse entry point), lines 53–97 show from_block lowering chain (SourceImports::from_block, SourceRootEnum::from_block, SourceNamespace::from_block, SourceRelations::from_block), /git/github.com/LiGoldragon/schema-next/src/source.rs:1431–1461 (SourceVariantName StructuralMacroNode impl using from_structural_block). Grep for custom parsing returns zero results outside nota-next imports.
- [CONFIRMED] The canonical schema-in-Rust representation is struct Schema with rkyv derives and methods like symbol_path_position for resolving paths into semantic roles; the old 'assemble' step is gone.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/schema.rs:207–216 (Schema struct with rkyv::Archive, rkyv::Serialize, rkyv::Deserialize derives), lines 341–384 (symbol_path_position resolution method matching paths to Type/RootVariant/Field/EnumVariant roles). Grep for 'assemble' returns only doc comments referencing past design, no live code.
- [CONFIRMED] String-writer RustWriter god-struct is gone; emission is entirely proc_macro2::TokenStream + quote! through ToTokens trait impls; 40+ token wrapper types cover all schema surfaces including Signal/Nexus/SEMA runtime support.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:4245–4248 (emit_item_tokens parses TokenStream via syn::parse2, never builds Rust code strings; all emit_* methods route through this). Grep 'impl ToTokens for' in lib.rs yields 44 impls (lines 1232–2896 show RouteEnumTokens, SignalFrameImplTokens, NexusEngineTraitTokens, SemaEngineTraitTokens, etc.). Only RustModuleRenderer exists (line 3950) and it uses emit_item_tokens, not string building.
- [CONFIRMED] No content hash or version projection is computed; only hand-authored SchemaIdentity with version string field exists; no RecordFamily enum or family-tagged decoder present.
  EVIDENCE: /git/github.com/LiGoldragon/schema-next/src/engine.rs:27–47 (SchemaIdentity struct with only component: Name and version: String fields, no hash method or projection). Grep for 'blake|sha|digest|hash' across both repos returns zero algorithm imports; test file references to 'Digest' are bare type names in schema fixtures (/git/github.com/LiGoldragon/schema-next/tests/lowering.rs:143–162), not cryptographic operations.
- [CONFIRMED] A RecordFamily enum + decoder + schema hash would land as 2–3 new ToTokens wrapper types in RustModule::render() pipeline; scope is small-to-medium, reusing existing TraceObjectNameEnumTokens pattern.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:274–350 (RustModule::render method showing emission call sites: emit_scalar_alias, emit_imports, emit_type, emit_root_enum, emit_domain_scope_relation_support, etc.). TraceObjectNameEnumTokens impl at line 2735 shows precedent for enum-based dispatch with ToTokens. Pattern is reusable for RecordFamily.
- [CONFIRMED] No free functions in schema-next core modules; all logic lives in trait impls and type methods; no ZST namespaces or stringly-typed core dispatch.
  EVIDENCE: Grep 'fn ' on schema-next src/*.rs excludes tests yields zero module-level functions. All parsing is via StructuralMacroNode::from_structural_block (source.rs), all lowering via impl blocks on Declaration/TypeDeclaration/EnumVariant/etc. (schema.rs), all engine dispatch via SchemaEngine methods (engine.rs). No stringly-typed routing found.
- [NUANCED] One format!() call at lib.rs:278 for '// @generated' comment is a documented exemption because prettyplease drops non-doc comments; six other format!() uses are for proc_macro2::Ident/Literal construction, not Rust code text emission.
  EVIDENCE: /git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:278 (format!('// @generated by {}') confirmed as documented exemption). Grep 'Ident::new(&format!' or 'LitInt::new(&format!' finds 6 calls across all files (lib.rs:1544, 1590; migration.rs:490, 522; daemon_emit.rs:846, 863). However, the claim understates the full picture: there are 19 total format!() calls in lib.rs. Of these, most are for building intermediate Strings that are then parsed via syn::parse_str (use_item at line 750, use_item parsed at line 1776-1778) or wrapped in RustTypeTokens/RustIdentifier (scope_name at line 1276-1278, route_name at lines 2939/2949 used in token construction). All format!() outputs eventually flow through TokenStream emission; none directly write Rust code text. The claim is correct in substance but incomplete in accounting for the full 19 format!() calls.

