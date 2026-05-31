# 5 — Overview: top broad design improvements + cross-cutting patterns

*Kind: meta-report synthesis · Topics: design-audit-synthesis, reusable-planes, boilerplate-elimination, schema-core-extraction, nota-next-substrate, sema-store-generic, layering · 2026-05-31 · designer lane*

Synthesis of four parallel sub-agent audits (`1-nota-next-audit.md` through `4-spirit-next-audit.md`). The audits identify ~2500-3500 lines of boilerplate eliminable across the four repos through five broad design improvements, plus five cross-cutting patterns that explain why the boilerplate exists.

## Top 5 broad design improvements (ordered by impact × scope)

### #1 — Schema-core extraction (designer 435 Gap C × operator 263 Gap 4)

**Lift the universal envelope/frame/mail/origin-route substrate out of every emitted component into a shared `schema-core` crate.**

Both sub-agent 3 (schema-rust-next) and sub-agent 4 (spirit-next) name this as their #1; together they confirm the magnitude:

- Sub-agent 3 measures ~470 lines per emitted component as BYTE-IDENTICAL across the spirit/triad/imported fixtures — same `Signal<R>` / `Nexus<R>` / `Sema<R>` envelopes, same `SignalFrameError`, same `Plane<S,N,M>`, same `MessageSent` / `NexusMail` / `MessageProcessed`, same `UpgradeFrom` / `AcceptPrevious`.
- Sub-agent 4 measures ~600 lines of the 1269-line `spirit-next/src/schema/lib.rs` as the SAME universal substrate, and identifies an additional ~300-400 lines of hand-written runtime that also lifts (`Mail<Phase>` typestate, `MailLedgerHook` pattern, `Engine`-as-composer, the `SemaStore<T>` wrapper from improvement #3 below).

The duplication isn't just lines — it's TYPE IDENTITY. Today each component gets its own `Signal<R>` type, which prevents cross-component dispatch (a `Signal<Input>` from `spirit-next` is not the same Rust type as a `Signal<Input>` from a hypothetical `mail-next`, even when the schemas declare identical envelopes). Schema-core extraction unifies the type identity and unblocks cross-component dispatch in the same move.

Per-component boilerplate eliminated: ~470 generated lines + ~300-400 hand-written runtime = ~800-1000 lines. The saving COMPOUNDS per new component. Already two components in the stack pay; the future component triad expansion (per `protocols/active-repositories.md`) means dozens of components, each redundantly carrying the same support nouns.

Sequencing implication: this is the LARGEST single improvement but requires coordination across `schema-next` (declare which support nouns are imported from schema-core), `schema-rust-next` (emit `use schema_core::*` instead of inline), and every consumer component (depend on schema-core). The other four improvements can land independently.

### #2 — Drop the text round-trip from declarative macro lowering (Spirit 1280 Maximum violation)

**Replace the `Block → String → Document::parse → Block` round-trip in `schema-next/src/declarative.rs` with direct Block-tree traversal.**

Sub-agent 2 names this as #1 for schema-next, and it's the only finding in the entire audit set that's both a Spirit Maximum-certainty violation AND a self-contained refactor (no nota-next changes needed).

The declarative macro engine stores captured macro bindings as `String` (`declarative.rs:1026-1088`), re-emits them as NOTA text (`NotationBlock::compact_notation` at line 732 and 837), then re-parses the text through `Document::parse(&self.source)` to reconstruct Block trees. This middle hop:

- Violates Spirit 1280 directly: "Schema should prefer structural macros over text macros." The macro engine IS doing text macros disguised as structural.
- Violates Spirit 1263: macros are NOTA-LAYER structural matching; the captures should be Block references, not stringly-typed substrate.
- Eliminates ~150 lines of stringly-typed substrate when fixed.

The fix is internal to `src/declarative.rs` — `MacroBindings` stores `Vec<Block>` captures instead of `Vec<String>`, `ExpandedTemplate::lower_to_output` operates on Block trees directly, the middle `Document::parse` call disappears. Type signatures of `MacroBindings`, `ExpandedTemplate`, `MacroTemplate::expand`, and the `Capture / RestCapture / Atom / Delimited` traversal methods change; public API of `DeclarativeMacroLibrary` and `MacroLibraryArtifact` is preserved.

Sequencing: this is the highest-priority FIX (Maximum-certainty violation) but lowest-scope refactor. Ship it as a small isolated slice before the larger improvements.

### #3 — Generic `SemaStore<T>` + `SerializableArtifact<T>` substrate

**Lift the typed-record-storage and the typed-artifact-projection patterns into one generic substrate that every consumer reuses.**

Sub-agent 2 names `SerializableArtifact<T>` (#2 for schema-next) and `AsschemaStore` redb scaffolding (#3 for schema-next); sub-agent 4 names `SemaStore<T>` (#3 for spirit-next). All three are the same architectural pattern at different positions:

- **`SerializableArtifact<T>`**: schema-next currently has `AsschemaArtifact` (`src/asschema.rs:234-317`) and `MacroLibraryArtifact` (`src/declarative.rs:72-155`) as character-identical 80-line copies — ~160 lines of literal duplication. The pattern is "any T that derives `NotaDecode + NotaEncode + rkyv::Archive + Serialize + Deserialize` gets `read_nota_file / write_nota_file / read_binary_file / write_binary_file` for free." Generic trait or generic struct, both shrink each owner to ~10 lines.

- **`SemaStore<T>`**: schema-next's `AsschemaStore` (`src/store.rs`, just landed in `84ce382`) and spirit-next's existing redb store both repeat `begin_X → open_table → operation → map_err → commit` cycles. Sub-agent 4 finds five identical `From<redb::*Error>` impls each, identical open-or-create-with-mkdir scaffolding, identical transaction patterns. A `SemaStore<T: SemaTableLayout>` over `redb::Database` collapses both into one substrate.

Combined boilerplate eliminated: ~500 lines across schema-next + spirit-next. Multiplicative scope: every additional artifact-owning noun (Spirit 1254 Gap D's `SchemaUpgradeArtifact`, RustModule artifacts, MacroTable artifacts) and every additional store noun (SignalStore, NexusStore per the four-object separation) inherits the generic instead of re-copying.

Sequencing: independent of the others. Ship as a single slice that introduces both generics; rewire existing concrete types to the generics; tests stay green because the surface is preserved. Best timed AFTER #2 (the macro text-roundtrip fix) so the macro library's artifact owner doesn't need rewiring twice.

### #4 — Nota-next derive features + public `Delimiter` encoding surface

**Lift the missing derive shapes and the encoding/decoding primitives from `nota-next` to its public surface so consumers stop hand-rolling them.**

Sub-agent 1 names this as #1 (Delimiter encoding surface) and #2 (derive 2+-field-variant + inherent-method shadowing). The headline numbers from sub-agent 1:

- Delimiter encoding surface: ~150 lines eliminated across the stack. Make `Delimiter::opening_text`, `Delimiter::closing_text`, and `Delimiter::wrap(children)` public; add `Block::expect_delimited(delimiter, type_name)` / `Block::as_delimited(delimiter)` as canonical entry points. Collapses five destructure sites inside `nota-next/src/codec.rs` itself, kills `DelimitedNotation` (32 lines) + `SchemaNodeDelimitedNotation` (40 lines) in schema-next, retires `NotaCollection::format_vector` and `format_map` as free functions hidden as ZST-namespace methods (method-on-noun discipline violation per AGENTS.md).

- Derive extensions: ~300-400 lines eliminated across the stack. (a) Support enum variants with N≥2 unnamed fields (encoding as `(Variant (f1 f2 ...))`) — kills the 53-line hand-rolled `impl NotaDecode/NotaEncode for TypeReference` in `schema-next/src/asschema.rs` and unblocks every schema-emitted enum with multi-field variants. (b) Optional emit-inherent-shadow attribute that emits `pub fn from_nota_block` / `pub fn to_nota` as inherent methods on the type — kills ~20 wrapper-impl blocks per schema-emitted module in spirit-next (240+ lines in `spirit-next/src/schema/lib.rs` alone, similar across every emitted schema).

Sub-agent 2 confirms the substrate-gap framing: bare-variant emission (`TypeReference::String/Integer/Boolean/Path` + `Name`'s smart bare-or-bracketed encoding) is the same pattern force as the inherent-method shadow. Both belong as `#[nota(bare)]` per-variant attributes in the derive.

Sequencing: this is the FOUNDATION work that unblocks the largest downstream simplification. Each downstream consumer (schema-next, schema-rust-next, spirit-next) has hand-rolled code that disappears once these derive features land. Best timed BEFORE schema-core extraction (#1) because the extracted code is cleaner with the derive features applied.

### #5 — Schema-emitted variant-projection + sibling-plane translation derives

**Make the emitter derive `From<Payload> for Enum` (and the sibling `Into<NextEnum>` translations) so the runtime stops hand-rolling them.**

Sub-agent 4 names this as #2 for spirit-next. Today:

- `engine.rs:326-345` hand-writes three identical `NexusMail<X>::into_nexus_input` impls because Rust can't express "my variant payload becomes the enum" generically without `From<Payload> for Enum` impls.
- `SemaOutput::into_signal_output` (`engine.rs:389-398`) is another hand-rolled translation.
- `nexus.rs:105-154` has three identical `FromMail<Payload>` impls.

These impls ARE schema-derivable — the schema declares `Input::Record(Entry)`, the emitter knows it, `impl From<Entry> for Input { fn from(entry: Entry) -> Self { Self::Record(entry) } }` follows mechanically.

Boilerplate eliminated: ~120 lines across `engine.rs` + `nexus.rs`. Smaller absolute reduction than the others but cumulative across every future Signal/Nexus/SEMA boundary. Best timed AS PART OF schema-core extraction (#1) — the schema-core emitter teaches the projection derives, so #1 and #5 land in the same slice naturally.

## Cross-cutting patterns

These patterns explain WHY the boilerplate exists across the stack. They're not separate improvements but the underlying conditions that the top-5 improvements address.

### Pattern A — Substrate gaps in nota-next force consumer-side hand-rolling

Spirit 1278 named one instance (`Asschema::to_nota` as `[...].join("\n")`) but the pattern is broader. Sub-agents 1, 2, and 4 each identify nota-next surface that consumers reach for and find missing:

- Known-root document codec (designer 442) — operator hand-rolled `from_nota_document_fields` and `to_nota`
- Bare-variant emission attribute — schema-next hand-rolled `TypeReference` and `Name` codecs (~95 lines combined)
- Block re-emit method — schema-next has `NotationBlock::compact_notation` + `SchemaNodeNotation::compact` as parallel inventions
- Delimiter encoding methods — schema-next has `DelimitedNotation` + `SchemaNodeDelimitedNotation` as character-identical copies
- NOTA-literal-vs-path branch — spirit-next CLI hand-parses by string prefix when it should be a NOTA codec entry point
- Public `Delimiter::wrap` / `Block::as_delimited` — five repetitions inside nota-next itself

Each gap is cheap to fix in nota-next (50-150 lines added) and removes ~50-150 lines from each consumer. The aggregate is a few hundred net lines saved AND every future consumer inherits the substrate.

### Pattern B — Type-identity duplication breaks cross-component dispatch

Each emitted component owns its own `Signal<R>`, `Nexus<R>`, `Sema<R>` envelopes. Even when two components declare structurally identical envelopes, the Rust types are distinct because they live in different crates. Cross-component dispatch (taking a `Signal<Input>` from one component and routing to another) is impossible without re-encoding through bytes. Schema-core extraction (#1) fixes this in the same move it eliminates duplication.

### Pattern C — Parallel artifact owners signal missing generics

`AsschemaArtifact` vs `MacroLibraryArtifact` (~160 lines duplicated), `MacroPatternData` vs `MacroTemplateData` (~155 lines), `Raw*` vs `Syntax*` vs `*Declaration` (the three-stage lowering pipeline). Each pair is a place where ONE parameterized noun would carry the same semantics. The `SerializableArtifact<T>` (#3) covers one instance; the broader principle applies wherever the audit finds character-identical copies.

### Pattern D — Round-trip-through-text in structural code is anti-pattern

Spirit 1278 + 1280 name this at the macro lowering layer. Sub-agent 2's #1 finding makes it concrete: the declarative macro engine does `Block → String → parse → Block` in the middle of structural matching. This is the same anti-pattern as `Asschema::to_nota`'s hand-rolled `.join("\n")` — bypassing the typed substrate for stringly-typed glue.

The general rule: if structural code calls `.parse()` on text it just emitted, the design is wrong. Either keep the typed form throughout or expose a typed-to-typed shortcut.

### Pattern E — Wrapper layers carrying no new information

Sub-agent 2 Finding 4 names `schema-next::MacroNodeDefinition` as a wrapper around `nota_next::MacroNodeDefinition` that adds zero new structural information — the position is already inside each contained nota case. Designer 441's classDiagram showed the wrapper as a four-object split, but the split is more about RESPONSIBILITY (Asschema-data vs. AsschemaArtifact-projection vs. AsschemaStore-persistence vs. RustEmitter-consumption) than STRUCTURAL nesting. When the wrapper doesn't change the structure, it's pure layering noise.

The rule: every wrapper layer should add a typed concept the inner layer doesn't have. If `Wrapper<T>::method(&self)` just delegates to `self.inner.method()`, the wrapper is parasitic.

## Recommended sequencing

The audit's top-5 + the cross-cutting patterns suggest this order:

1. **First** — #2 (drop macro text round-trip). Highest-priority intent violation (Spirit 1280 Maximum), smallest scope, no cross-repo coordination, ~150 lines eliminated. Slice it as one schema-next commit.
2. **Then** — #4 (nota-next derive features + public Delimiter surface). Foundation work. Unblocks the largest downstream simplification. Slice as one nota-next commit, then propagate the simplifications across schema-next + spirit-next as a second commit per crate. ~450-550 lines eliminated.
3. **Then** — #3 (generic `SemaStore<T>` + `SerializableArtifact<T>`). Mechanical wins, no behavioral changes. One slice each crate. ~500 lines eliminated.
4. **Then** — #1 (schema-core extraction). The big lift; requires coordination across `schema-next`, `schema-rust-next`, all consumer components. Worth doing AFTER the simpler improvements so the extracted code is clean. ~800-1000 lines eliminated per component.
5. **Concurrent with #1** — #5 (variant-projection + sibling-plane translation derives). Falls out of the schema-core emitter changes naturally. ~120 lines eliminated.

Total potential boilerplate elimination across the stack: **~2500-3500 lines**, depending on how many components participate in schema-core (#1's multiplicative scope is the biggest variable).

## What's NOT recommended

A few things the audit considered and rejected:

- **Redesigning the `Mail<Phase>` typestate** (sub-agent 4 §Finding 5): the typestate is structurally sound and should LIFT to schema-core, not be replaced.
- **Refactoring `NotaSurface` gating** (sub-agent 3 §Finding 4): operator 246 closed this cleanly; three variants, three helper methods, three call sites. No improvement available.
- **Reshaping `RustImport::from_resolved_import`** (sub-agent 3 §closing): already a single-line elegant pass-through; the same mechanism will carry `use schema_core::*` once #1 lands.
- **Wholesale rewrite of the macro engine** (sub-agent 2 §Finding 3): #2's text-roundtrip removal is internal to the engine; the macro mechanism itself is sound per Spirit 1263/1279/1280.

## What this audit deliberately did NOT cover

- The intent capture quality of recent psyche prompts (covered in designer 440, 442).
- The `#[nota(known_root)]` derive option for Asschema specifically (covered in designer 442).
- The Asschema four-object separation (covered in designer 441).
- Test coverage gaps (sub-agents flagged a few in passing but the audit lens is BOILERPLATE, not coverage).
- Performance (no findings around hot paths or allocation; out of scope for design audit).

## Cross-references

- `reports/designer/443-design-improvements-audit-2026-05-31/0-frame-and-method.md` — frame
- `reports/designer/443-design-improvements-audit-2026-05-31/1-nota-next-audit.md` — sub-agent 1
- `reports/designer/443-design-improvements-audit-2026-05-31/2-schema-next-audit.md` — sub-agent 2
- `reports/designer/443-design-improvements-audit-2026-05-31/3-schema-rust-next-audit.md` — sub-agent 3
- `reports/designer/443-design-improvements-audit-2026-05-31/4-spirit-next-audit.md` — sub-agent 4
- `reports/designer/435-vision-for-the-four-remaining-gaps.md` — Gap C extraction proposal (matches improvement #1), Gap B RustItem proposal (matches sub-agent 3's #2)
- `reports/designer/441-asschema-types-rkyv-sema-roundtrip.md` — four-object logic separation (Spirit 1272); SemaStore production at operator 84ce382 (matches improvement #3 first instance)
- `reports/designer/442-known-root-nota-anti-pattern-and-elegant-path.md` — the Spirit 1278 anti-pattern + the `#[nota(known_root)]` substrate gap (matches Pattern A)
- `reports/operator/263-unimplemented-gap-audit-2026-05-31.md` — operator's 8-gap audit (Gap 1 = improvement #2; Gap 4 = improvement #1)
- Spirit records: 1254 (four-gap framing), 1263 + 1279 + 1280 (structural macros, two-layer architecture), 1272 (four-object separation), 1278 (anti-pattern + NOTA-layer abstraction).
