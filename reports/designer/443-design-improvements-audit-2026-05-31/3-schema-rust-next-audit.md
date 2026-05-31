# 3 — schema-rust-next design audit

*Kind: audit · Topics: rust-emission, rust-module-as-data, schema-core, plane-envelopes, boilerplate-elimination · 2026-05-31 · designer lane sub-agent*

## Scope

`schema-rust-next` is one file: `src/lib.rs` (1554 lines). It contains
`RustEmitter` (the entry point), `RustModule` (the data model
between Asschema and rendered text), `RustWriter` (the rendering
machinery), and `NotaSurface` / `RustEmissionOptions` (the
feature-gating knobs).

Audit corpus, all under `/git/github.com/LiGoldragon/schema-rust-next/`:
- `src/lib.rs:1-1554` — the entire emitter
- `tests/emission.rs:1-692` — primary test surface
- `tests/big_emission.rs:1-...` — large-fixture tests
- `tests/cross_crate_import.rs:1-62` — import emission tests
- `tests/fixtures/spirit_generated.rs` (707 lines), `triad-reactive-large.generated.rs` (1442 lines), `imported-mail-consumer.generated.rs` (759 lines) — emitted-source snapshots
- `INTENT.md`, `ARCHITECTURE.md`, `README.md`

The lens: per the orchestrator's frame, "reusable logical planes" + "boilerplate elimination". Designer 435 named the four remaining gaps; this audit verifies the schema-rust-next state against Gap B (RustModule-as-data) and Gap C (schema-core shared support nouns), and looks for residual hand-rolled patterns.

## Finding 1: RustModule-as-data closure is partial — type declarations are data, support surfaces are still string concatenation

Designer 435 named "RustModule-as-data emitter" as Gap B and Spirit 1254 lists it among the four remaining bootstrap gaps. The current repo claims partial closure (per INTENT.md line 173: *"Rust emission is data before it is text. The emitter maps Asschema into a typed RustModule object... Tests assert the module data shape directly so the core mapping is not hidden inside string-writer side effects."*). The verification: closure is **real for the data-bearing type declarations**, **absent for everything else**.

### Where `RustModule` is data — half the emitted source

The `RustModule` struct (`src/lib.rs:84-94`) carries:

- `scalar_aliases: Vec<RustScalarAlias>` — typed.
- `imports: Vec<RustImport>` — typed.
- `declarations: Vec<RustDeclaration>` — typed, with `RustTypeDeclaration::{Struct, Enum, Newtype}` and `RustField` / `RustEnumVariant` substructure.
- `root_enums: Vec<RustEnum>` — typed.
- `support: RustSupportModel` — limited to `map_key_type_names` and `private_type_names`. Just the witness lists, not the surfaces themselves.

The data model covers the *namespace declarations* and *root enums* cleanly. `RustDeclaration::from_asschema_declaration` (`src/lib.rs:356-362`) is a clean data-to-data projection.

### Where `RustModule` is NOT data — the support surface

The `RustWriter` struct (`src/lib.rs:662-667`) carries only `output: String`, `map_key_types`, `private_type_names`, `nota_surface`. Everything else is hand-typed string lines through `self.line("…")` and `format!()`. The writer has 28 `emit_*` methods (per `grep "fn emit_"`), 308 `self.line(…)` calls, 58 `format!()` calls.

Of those 28 emit methods, 12 emit hand-coded boilerplate strings that do NOT come from `RustModule` data at all:

| Method (line) | Emits | Source |
|---|---|---|
| `emit_signal_frame_support` (`991`) | `SignalFrameError` enum + Display impl | Hardcoded strings (`992-1018`) |
| `emit_signal_frame_impl` (`1040`) | `route() / short_header() / route_from_short_header / encode_signal_frame / decode_signal_frame` | Hardcoded strings (`1040-1140`) |
| `emit_mail_event_support` (`1142`) | `MessageIdentifier`, `OriginRoute`, `MessageRoot`, `MessageSent`, `NexusMail<Payload>`, `MessageProcessed<Reply>`, `MessageSentHook`, `MessageProcessedHook<Reply>`, impl blocks | Hardcoded strings (`1142-1288`) |
| `emit_schema_plane_support` (`1290`) | `pub mod schema { pub enum Plane<S, N, M> { ... } impl Plane }` | Hardcoded strings (`1290-1311`) |
| `emit_plane_envelope` (`1313`) | `Signal<R> / Nexus<R> / Sema<R>` envelope + impl | Parameterised on name only — same body emitted 3 times (`1313-1343`) |
| `emit_plane_namespaces` (`1345`) | `pub mod signal { pub type Input = super::Input; ... }`, etc. | Hardcoded strings + name interpolation (`1345-1394`) |
| `emit_plane_origin_route_constructor` (`1396`) | `impl <Type> { pub fn with_origin_route ... }` | Hardcoded strings (`1396-1410`) |
| `emit_nexus_trait` (`1421`) | `pub trait <Root>Nexus { ... }` | Hardcoded + variant-driven (`1421-1440`) |
| `emit_nexus_dispatch_impl` (`1442`) | `pub fn dispatch_mail_with_nexus(...) { match self { ... } }` | Hardcoded strings (`1442-1467`) |
| `emit_upgrade_support` (`1469`) | `UpgradeFrom`, `AcceptPrevious`, blanket impl | Hardcoded strings (`1469-1483`) |
| `emit_schema_plane_trait_support` (`1485`) | `NexusEngine`, `SemaEngine` traits | Hardcoded strings (`1485-1498`) |
| `emit_nota_inherent_bridge` / `emit_nota_copy_inherent_bridge` (`912`, `925`) | `impl <T> { fn from_nota_block / to_nota }` | Hardcoded strings (`912-936`) |

For these 12 methods, the rendered Rust is **byte-identical across components** (modulo string-interpolated identifiers). They are universal scaffolding the emitter knows about, glued in as text.

The data model `RustModule` does NOT include:

- `RustImpl` (trait or inherent impls)
- `RustTrait` 
- `RustFunction` / `RustMethod`
- `RustConst` 
- `RustSubmodule` (no `pub mod schema { ... }` representation)
- `RustAttribute` (no `#[derive(...)]` data form — derives are built ad-hoc inside `derive_attribute` at `src/lib.rs:715-744`)

Designer 435 named the target as `enum RustItem { UseItem, TypeAlias, Struct, Enum, Impl, Function, ConstItem, Module }`. The current `RustTypeDeclaration` is the trio `{Struct, Enum, Newtype}` — eight other item kinds are absent and emitted as strings.

### What it means

Tests can assert on the module shape **for the schema-derived nouns** (the test at `tests/emission.rs:89-122` does exactly that). They cannot assert on the SHAPE of the support surface — for those, tests have to substring-match against rendered source. The structural-vs-text test split tracks this exactly: across all three test files, **85 `code.contains(...)` assertions vs. 4 module-data assertions** (`grep -c '\.contains('` and `grep -c 'emit_module'`). The data-vs-text ratio is ~5%.

This is the boilerplate Spirit 1254 (Gap B) names. The closure is genuinely incomplete: `RustModule` is data for the schema-derived half; for the support half, the writer IS the emitter.

## Finding 2: Per-component duplication of universal envelope/frame/mail surface is the largest fix in the stack (Gap C)

This is the headline finding. Spirit 1254 (Decision, High) names this as Gap C and recommends it as the **first** gap to close. Designer 435 §4 estimates ~500-600 lines deduplicated per component. The repo's three checked-in emission snapshots make the size measurable:

| Fixture | Total lines | Universal-support lines (estimated) | Component-specific lines |
|---|---|---|---|
| `spirit_generated.rs` | 707 | ~470 | ~237 |
| `triad-reactive-large.generated.rs` | 1442 | ~470 | ~972 |
| `imported-mail-consumer.generated.rs` | 759 | ~470 | ~289 |

The ~470 lines of identical universal support across every emitted module:

- `pub mod short_header { ... }` (variant-driven names, but structurally identical)
- `const SIGNAL_SHORT_HEADER_BYTE_COUNT: usize = 8;` (1 line, identical)
- `pub enum SignalFrameError { ... }` + Display impl + Error impl (~20 lines, identical)
- Per-root: `pub enum <Root>Route { ... }` (variant-driven)
- Per-root: `route() / short_header() / route_from_short_header / encode_signal_frame / decode_signal_frame` impl (~50 lines per root, body identical structurally)
- `pub struct MessageIdentifier(pub Integer)` + NOTA bridge (~12 lines, identical)
- `pub struct OriginRoute(pub Integer)` + NOTA bridge (~12 lines, identical)
- Per-component `pub enum MessageRoot { ... }` (variant-driven from root enums)
- `pub mod schema { pub enum Plane<S, N, M> { ... } impl Plane }` (~17 lines, identical)
- `pub struct Signal<Root> { ... }` + impl (~25 lines, identical) — emitted via `emit_plane_envelope("Signal")` at `src/lib.rs:1164`
- `pub struct Nexus<Root> { ... }` + impl (~25 lines, identical)
- `pub struct Sema<Root> { ... }` + impl (~25 lines, identical)
- `pub struct MessageSent { ... }` (~7 lines, identical)
- `pub struct NexusMail<Payload> { ... }` (~7 lines, identical) + impl (~17 lines, identical)
- `pub struct MessageProcessed<Reply> { ... }` (~7 lines, identical) + impl (~25 lines, identical)
- `pub trait MessageSentHook { ... }` (~5 lines, identical)
- `pub trait MessageProcessedHook<Reply> { ... }` (~5 lines, identical)
- `impl MessageSent { ... }` (~10 lines, identical)
- `pub trait UpgradeFrom<Previous> { ... }` + `AcceptPrevious` + blanket impl (~13 lines, identical)

Verified by visual comparison: `spirit_generated.rs:417-543` and `triad-reactive-large.generated.rs:1138-1264` show the IDENTICAL `pub mod schema { pub enum Plane ... }` through to `pub trait MessageProcessedHook` block.

### What the duplication costs today

- Every fix to wire support requires re-emitting every consumer crate's `src/schema/`. This is exactly the friction the architecture is supposed to remove.
- `SignalFrameError`, `MessageSent`, `Plane`, etc. each have a **different type identity per crate** — `crate_a::SignalFrameError` and `crate_b::SignalFrameError` are distinct types even though they're structurally identical. A function written against `crate_a::SignalFrameError` cannot accept the equivalent value from `crate_b` without a conversion. This is the runtime cost in addition to the source-size cost.
- The `Plane` enum's generic parameters (`<SignalRoot, NexusRoot, SemaRoot>`) only make sense if downstream code can name it shared; today each component is its own `crate::schema::Plane` and cross-component dispatch must re-wrap.
- The duplication is what blocks `spirit-next` from importing schema-emitted types from other components — every component is a closed namespace for its envelope shapes.

### The shape of the closure (from designer 435 + Spirit 1254)

`schema-core` (or a triad of shared crates: `signal-frame`, `plane-envelope`, `origin-routing`, `mail-keeper`) holds the universal nouns. The emitter learns when to emit `use schema_core::Signal;` instead of an inline `pub struct Signal<Root> { ... }`. The schema-core types are themselves schema-emitted (recursion: schema-core has its own `schema/lib.schema`), so the universal surface IS schema-derived — it just lives once.

The `RustModule` data model would gain `imports: Vec<RustImport>` entries pointing at `schema_core::*`, and the writer would drop the 12 hand-rolled emit methods entirely.

This is Gap C; this audit confirms it as the largest single boilerplate win available in schema-rust-next. **~470 × N components** of dedup, where N is the number of component-triad crates that import schema-core.

## Finding 3: Per-shape emission has the right unification at the `RustItem` level — half of the way

The four shape emitters — `emit_struct`, `emit_enum`, `emit_newtype`, `emit_root_enum` — share structural code that could collapse if the `RustItem` enum were adopted.

Current shape emitters (`src/lib.rs:837-900`):

- `emit_newtype` (`837`): derive line + `pub struct <Name>(pub <T>);` (10 lines)
- `emit_struct` (`849`): derive line + `pub struct <Name> { fields }` (17 lines)
- `emit_enum` (`868`): derive line + `pub enum <Name> { variants }` (13 lines)
- `emit_root_enum` (`882`): derive line + `pub enum <Name> { variants }` (8 lines — different derive, no Newtype/Struct case)

Across these four:
- All four start with `self.line(derive)` where `derive` comes from `data_type_derive` or `root_data_type_derive`.
- `emit_struct` and `emit_newtype` differ from `emit_enum` and `emit_root_enum` only in the keyword (`struct` vs `enum`) and body shape (`{...}` vs `{Variant, ...}`).
- `emit_enum` and `emit_root_enum` share variant emission (`emit_variant` at `891`) but diverge on visibility (no visibility argument on root_enum, hardcoded `pub`) and derive choice.

These four ALREADY share enough that the dispatch in `emit_type` (`817-825`) handles three of them. The missing fourth is `emit_root_enum`, which is called separately at `src/lib.rs:175-178` because it (a) gets a different derive set and (b) skips the visibility/private-fields path. With a unified `RustItem` enum and `RustDeclaration` carrying `is_root: bool` (or via a `RustEnum::Root` variant), this could collapse into one dispatch point.

That same `RustItem` unification opens the door to the 12 hand-rolled support emit methods. If `RustItem::Impl(RustImpl)` and `RustItem::Trait(RustTrait)` existed, methods like `emit_signal_frame_impl` and `emit_nexus_trait` would build typed values instead of string-formatting. The data model exists in concept (designer 435 named the items); the implementation has only the noun-shape leaves so far.

## Finding 4: NotaSurface gating is the cleanest part of the emitter

`NotaSurface::{AlwaysEnabled, FeatureGated, Disabled}` (`src/lib.rs:266-271`) plus `feature_gate_attribute` (`278-283`) and `feature_gated_derive_attribute` (`285-292`) form a small, clean policy interface. Three methods, three call sites:

- `emit_nota_gate` (`src/lib.rs:969-973`) — emits `#[cfg(feature = "...")]` at every nota-conditional position. Called from `emit_nota_inherent_bridge` and `emit_nota_root_enum_support` and `emit_nota_support`.
- `feature_gated_derive_attribute` returns the conditional derive line; called from `derive_attribute` (`715-744`).
- `includes_nota_in_derive` is a boolean check used inside `derive_attribute` to decide whether NOTA derives are inlined unconditionally (only true when `AlwaysEnabled`).

The pattern correctly captures the asymmetry: derives are `#[cfg_attr(feature = "X", derive(...))]` (always present, conditional behaviour); impls and `use` items are `#[cfg(feature = "X")]` (presence is conditional). Three call sites for the gate attribute (`emit_nota_support` at `831`, `emit_nota_inherent_bridge` at `913`, `emit_nota_root_enum_support` at `944`/`956`) are tractable.

What COULD be cleaner: every `emit_nota_*` method calls `self.emit_nota_gate()` THEN `self.line("impl X for Y {")` THEN body. If `RustImpl` were data, the gating could be a field on the impl item (`nota_gated: bool`) and the renderer would handle the `#[cfg(...)]` emission once. Today the gate-then-line pattern is repeated at every nota-impl site, but that's a Finding-3-shape issue, not a NotaSurface-design issue. The NotaSurface enum itself is sized right and located right.

One minor note: `NotaSurface::FeatureGated { feature: String }` is currently stringly-typed. If feature gating were generalised beyond `nota-text` (say, to gate the rkyv-binary surface or future plane surfaces), a `FeatureName(Name)` typed wrapper would be appropriate; for one-knob status quo, the `String` is fine.

## Finding 5: Cross-crate import emission is elegant — and reveals an asymmetric design constraint

`RustImport::from_resolved_import` (`src/lib.rs:336-341`) is a one-line projection:

```rust
fn from_resolved_import(import: &ResolvedImport) -> Self {
    Self { use_item: import.use_item(): }
}
```

The actual `use marker_core::schema::mail::DatabaseMarker as DatabaseMarker;` string is composed by `ResolvedImport::use_item()` in `schema-next`. The schema-rust-next side is a pure pass-through.

This is elegant per se — and it sets up the precedent for the schema-core Gap C closure. The same `RustImport` mechanism could carry `use schema_core::{Signal, Nexus, Sema, OriginRoute, SignalFrameError, MessageSent, ...}` once schema-core exists. No new emitter machinery would be needed; only the decision about WHEN to emit a schema-core import versus a local inline definition (which is fundamentally a schema-next question about whether the consumer's `.schema` declared a dependency on schema-core).

The asymmetric constraint surfaced: today `RustImport` only carries pre-baked `use_item: String`. The string came from `schema-next`. If schema-core imports become data-driven (per-import structure: source crate, source path, local alias), the type evolves. That's a small shape change with no behavioural impact in schema-rust-next.

## Finding 6: Tests assert on text 95% of the time — the data-driven discipline isn't reaching the test surface

Across the three test files (`emission.rs`, `big_emission.rs`, `cross_crate_import.rs`):

- 85 `code.contains("...")` substring assertions on emitted Rust source
- 4 assertions on `module.declaration_named(...)`, `module.root_enums()`, `module.scalar_aliases()`

The single test at `tests/emission.rs:89-122` (`emitter_builds_rust_module_data_before_rendering_text`) is the only structural-shape test. Every other test asserts text — either substring containment or full-text snapshot match against checked-in `tests/fixtures/*.rs`.

Fixture-comparison snapshot tests have their place — they pin the exact emitted source as a contract. But the heavy substring usage IS a signal that the substrate isn't yet at "data first, text optional." Examples of substring-style assertions:

- `tests/emission.rs:40-86` — 14 `code.contains(...)` checks against `spirit_generated.rs`
- `tests/emission.rs:138-152` — `!code.contains("nota_next")`, `!code.contains("NotaDecode")`, etc. — testing `NotaSurface::Disabled` strips text. Could equally test "the module's declarations have no NOTA-related attributes / impls / imports."
- `tests/big_emission.rs:311-340` — 18 `code.contains(...)` checks across three big fixtures

If `RustModule` modelled traits, impls, and modules, all of these substring assertions could become data assertions. Instead of `code.contains("pub trait InputNexus")`, the test could query `module.traits().iter().find(|t| t.name() == "InputNexus")` and inspect methods. That's the Gap B story made operational in the test surface.

The discipline test: when adding a new emission (a new trait, a new struct, a new method), does the test assert *on the module's structure* or *on a substring of the output*? Today the answer is overwhelmingly the latter, and refactoring the writer to reorder lines, change whitespace, or swap synonymous Rust forms (e.g. `pub fn x(&self) -> &Y { &self.y }` vs `pub fn x(&self) -> &Y { let inner = &self.y; inner }`) would break tests for cosmetic reasons. Snapshot tests + the one data-shape test handle most of the regression risk but at the cost of locking the rendered form, not the rendered semantics.

## Finding 7: A `RustModulePath` micro-finding — the "drop first segment of namespace" knowledge is encoded in module-segment slicing

`RustModulePath::module_segments` (`src/lib.rs:571-582`) does a small heuristic: take all namespace segments, drop the first (crate-name) if there are more than one. The slicing logic is correct for "spirit-next:lib" → `lib`, "spirit-next:signal:public" → `signal/public`, "spirit:lib" → `lib`.

This is mechanical and small, but it's the kind of decision that could live in `Asschema::identity()` as a structured object (component crate name + module path tuple) rather than as a slicing operation here. As Spirit 1245 observes: schema is the authoritative substrate; here, schema-rust-next reaches into the `Name` to do path slicing. A typed `SchemaModulePath` in schema-next would be the canonical home. Low priority — works as-is.

## Top 3 broad improvements for schema-rust-next (ordered by impact × scope)

### 1. Close Gap C — extract universal envelope/frame/mail surface into shared `schema-core` and emit `use schema_core::*` instead of inline definitions

**Impact:** Removes ~470 lines from EVERY emitted component (the spirit/triad/imported numbers above), plus collapses ~12 hand-rolled emit_* methods in `src/lib.rs`. Eliminates the type-identity duplication problem (one `Signal<R>` per Rust universe instead of one per emitted crate), unblocking cross-component dispatch. Bug fixes to envelope code become single-edit operations.

**Scope:** Multi-repo — requires a new `schema-core` crate (or component-triad set: `signal-frame`, `plane-envelope`, `origin-routing`, `mail-keeper`) authored in its own `.schema`, emitted into a checked-in source file, and consumed by every component. Schema-next needs a `.schema` field declaring "I import these support nouns from schema-core" so schema-rust-next knows when to emit `use schema_core::Signal` instead of inline.

**Why first:** Designer 435 §7 recommends this first; Spirit 1254 names it as the most pragmatic of the four. The dedup compounds with every new component added. It's also the cleanest in the sense that it doesn't change the schema language or the macro mechanism — it changes only where universal types are *located*.

### 2. Close Gap B — extend `RustModule` data model from "type declarations only" to "all Rust items" (`RustItem` enum)

**Impact:** Eliminates the remaining 12 hand-rolled emit_* methods in the writer. Tests can assert on data instead of text (the 85:4 ratio inverts). Lays the substrate for speculative multi-target emission (e.g. Python codegen sharing the same item model). Cosmetic-only refactors of the renderer stop breaking tests. Enables semantic snapshot tests that catch "the impl block lost its trait bound" without locking whitespace.

**Scope:** Single-repo to `src/lib.rs`. `RustItem` enum with variants `UseItem`, `TypeAlias`, `Struct`, `Enum`, `Newtype`, `Impl`, `Trait`, `Function`, `Const`, `Module`. `RustModule { items: Vec<RustItem> }`. The writer becomes a renderer (`RustItem::render` per variant). The 28 emit methods either become item builders inside `RustModule::from_asschema` or fold into per-item render impls.

**Why second:** Most of the work in this gap is "decide where the items live + write the typed forms." It doesn't change emission output; it changes WHERE the emission decisions are made. After Gap C lands, Gap B has half the surface area (the support items live in schema-core, so schema-rust-next only needs the item types it still emits locally — type declarations + the impl/trait/method nouns for per-component Nexus dispatch, plane namespaces, and origin-route constructors).

### 3. Unify the four shape emitters (`emit_struct`, `emit_enum`, `emit_newtype`, `emit_root_enum`) into one item-driven renderer; eliminate the `emit_type` → `emit_struct` indirection

**Impact:** Removes ~80 lines from the writer, but more importantly removes the SPECIAL-CASE-PER-SHAPE pattern that today requires every emission decision to be made in two places (the data builder in `RustModule::from_asschema` AND the dispatch in `RustWriter::emit_type`). Folds the visibility logic, the derive logic, and the body rendering into a single per-item path. Makes the addition of a fifth shape (e.g. a tagged union, an actor-state-machine, an opaque ID type) a SINGLE-FILE-SINGLE-EDIT operation instead of a 6-edit shotgun.

**Scope:** Local to `src/lib.rs`. Builds on Gap B (it's essentially a sub-case of `RustItem` adoption). Could land before Gap B as a stepping stone — make `RustTypeDeclaration` carry the full data needed to render (visibility + name + body + derive selection + nota-gating) so the writer becomes a pure projection.

**Why third:** Gap C is the bigger boilerplate win; Gap B subsumes this finding once it lands. As a standalone improvement, this is incremental — it cleans up Findings 3 by collapsing per-shape emitters but doesn't address the larger Gap B (Findings 1) or Gap C (Findings 2) surfaces. Worth pursuing only if Gap B is deferred and the operator wants a smaller intermediate slice.

## Cross-references

- Spirit 1244 — *"Generated component types always need binary rkyv support, while NOTA encode/decode is opt-in for text-facing clients..."* (Maximum, 2026-05-30). The current `NotaSurface` design (Finding 4) implements this principle correctly.
- Spirit 1246 — *"The assembled schema MUST become a live serializable artifact"* (Maximum). Verified — `RustEmitter::emit_file_from_nota_path` and `emit_file_from_binary_path` (`src/lib.rs:59-73`) close that loop on the schema-rust-next side. The `BigRustFixture::assert_emission_uses_live_asschema_artifact` test at `tests/big_emission.rs:211-218` exercises the artifact path.
- Spirit 1254 — the four-gaps decision (High, 2026-05-30). Gap B and Gap C are the two this audit confirms.
- Spirit 1255 — *"Proceed with the operator's leaned schema gap-closure order: check in reviewable .asschema text artifacts first, then RustModule data emission, typed MacroLibrary, schema-core support nouns..."* (High). The "RustModule data emission" item here is Gap B (Finding 1); "schema-core support nouns" is Gap C (Finding 2). Order: artifacts → RustModule data → MacroLibrary → schema-core. This audit suggests schema-core (Gap C) is the **bigger boilerplate win** but designer 435 §7 explicitly calls it first regardless — so the operator's order may have been driven by a different consideration (perhaps that RustModule-as-data is needed to express schema-core's own emission cleanly).
- Designer 435 §3 (Gap B target shape) — the `RustItem` enum proposal that Finding 1 and Finding 3 both point at.
- Designer 435 §4 (Gap C target shape) — the schema-core crate proposal that Finding 2 points at.
- INTENT.md lines 173-177 — declares "Rust emission is data before it is text" as principle; this audit confirms it is **partially** realised today (type declarations are data; support surface is text).
