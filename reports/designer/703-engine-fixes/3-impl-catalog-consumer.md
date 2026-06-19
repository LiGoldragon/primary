# 703.3 — schema-rust-next consumes the `{| |}` impl-reference catalog

Research-and-decide file for the 703 frame, decision #2 ("`{| |}` catalog
consumer"). Verdict, then the executable consumer design the implementation
agent follows. All line numbers re-verified against `schema-next` main
(`da5643c` merged) and `schema-rust-next` `src/lib.rs` as checked out.

## TL;DR verdict

**Yes — schema-rust-next must consume the catalog, and the catalog must
DRIVE emission rather than sit beside it.** But "consume" is not "emit the
referenced impl body": the catalog carries no bodies. `ImplReference` is
`Marker(trait) | TraitImpl(trait, [sig]) | InherentMethod(sig)`
(`schema.rs:1215-1222`) — trait names and method *signatures*, never a Rust
body. So consumption has two complementary halves, and they layer cleanly
on the existing `scalar_like()` path rather than fighting it:

1. **Selection** — the catalog becomes the authoritative answer to "which
   standard impls does this type get," replacing the `scalar_like()` shape
   inference as the *trigger*. The impl *bodies* still live in
   schema-rust-next's `*Tokens` emitters (that is correct — the body is
   generator knowledge, not schema data); the catalog says *which* emitter
   fires for *which* type.
2. **Verification** — schema-rust-next gains a `RustSurface` *producer*: it
   scans the module it just lowered and emits the `ImplFact` set, so
   `RustSurface::verify_catalog` runs against a real generated surface
   instead of the hand-built facts that exist only in
   `schema-next/tests/impl_catalog.rs:409`.

The relationship to `scalar_like()` is **replace-the-trigger, keep-the-bodies,
add-the-loop**. Not a parallel mechanism; not a wholesale rewrite.

## What the catalog actually is (re-verified)

`Schema` carries impls in two places, unioned by one walk:

- Per-declaration: `Declaration::impls() -> &ImplCatalog`
  (`schema.rs:1130`), the fused form `RecordIdentifier String {| Display Ord |}`.
- Standalone: `Schema::impl_blocks() -> &[ImplBlock]` (`schema.rs:539`),
  the body-optional form `StatementText {| Display (word_count {} Integer) |}`
  targeting an elsewhere-declared type.
- The union walk: `Schema::referenced_impls() -> Vec<ReferencedImpl>`
  (`schema.rs:549-568`) — every entry paired with its target `Name`. **This
  is the single enumerable manifest the consumer reads.** Use it; do not
  re-walk `namespace()` + `impl_blocks()` by hand.

Each `ReferencedImpl` exposes `target() -> &Name` and
`entry() -> &ImplReference` (`schema.rs:1431-1438`). Each `ImplReference`
exposes `trait_name() -> Option<&Name>` and `methods() -> &[MethodSignature]`
(`schema.rs:1226-1242`). A `MethodSignature` is `name + [MethodParameter] +
return_reference` with a canonical `render()` (`schema.rs:1297-1353`); a
`MethodParameter` is `name + reference: TypeReference` (`schema.rs:1368-1385`).

Every catalog type is publicly exported from `schema_next`
(`schema-next/src/lib.rs:33-36`): `ImplBlock`, `ImplCatalog`,
`ImplCompositionKey`, `ImplFact`, `ImplReference`, `MethodParameter`,
`MethodSignature`, `ReferencedImpl`, `RustSurface`. schema-rust-next already
imports from `schema_next` at `lib.rs:3-8`; this is a one-line extension of
that `use`.

## Where it is dropped on the floor today

`Schema::lower_to_rust` (`lib.rs:403-459`) builds `RustModule` from
`namespace()`, `input_and_output()`, `streams()`, `families()`,
`relations()`, `resolved_imports()` — and **never reads `impl_blocks()` or
`Declaration::impls()`**. Confirmed by 702 (`grep 'ImplReference\|ImplCatalog'
src/` → 0). The standard impls that *do* emit come from a parallel inference:

- `StandardNewtypeImplTokens` (`lib.rs:2064-2158`), gated on `scalar_like()`
  (`lib.rs:2088-2090`) = direct `String`/`Path`/`Integer`/`Boolean` only.
- Emitted at `lib.rs:5252-5254`, gated on
  `RustRenderContext::emits_standard_newtype_impls()` (`lib.rs:1465`), itself
  fed by `RustEmissionOptions::standard_newtype_impls` — `false` in all three
  constructors (`lib.rs:498/514/527`), flipped on only by
  `ContractCrateBuild::wire_contract_module` (`build.rs:154-160`).

Two defects this design fixes, both flagged by 702: (1) **target-dependent
ergonomics** — a WireContract newtype gets `Display`/`AsRef`/`PartialEq`, an
identically-shaped NexusRuntime newtype gets none, because the trigger is an
emission flag, not the type's declared intent; (2) **transitive scalars are
invisible** — `scalar_like()` matches `TypeReference::String` directly, so
`Statement(StatementText(String))` is skipped. The catalog has no such blind
spot: if the schema author wrote `Statement {| Display |}`, the reference is
explicit and the trigger fires regardless of nesting or emission target.

## (a) Replace, complement, or layer? — LAYER, with the catalog as trigger

The `scalar_like()` path conflates two jobs: deciding *which* impls a newtype
deserves (a schema-semantics question) and *how to spell* `Display`/`AsRef`/etc.
(a generator question). Split them:

- **Trigger moves to the catalog.** `scalar_like()` shape inference is
  retired as the *selector*. A type gets a standard impl iff its catalog
  references the corresponding trait/method. This makes ergonomics a
  function of declared intent, uniform across every emission target.
- **Bodies stay in schema-rust-next.** `StandardNewtypeImplTokens`'
  `Display`/`AsRef<str>`/`PartialEq<&str>`/`PartialEq<u64>`/`PartialOrd<u64>`/
  `PartialEq<bool>` bodies (`lib.rs:2099-2150`) are correct and stay — the
  catalog names `Display`, the emitter knows the body. The catalog does not,
  and should not, carry Rust bodies.
- **The shape check becomes a guard, not a gate.** `scalar_like()` survives
  as the *capability check*: `Display`-on-a-`String`-newtype emits
  `self.payload().fmt(f)`; the same `Display` reference on a struct must NOT
  emit that body. The catalog says "emit Display here"; the type's shape says
  "the payload-delegating body is the right one." If the catalog references a
  trait the generator has no body recipe for under the target's shape, that is
  a typed error (see below), not a silent drop.

This is strictly more correct than `scalar_like()` and is not a parallel
mechanism — there is exactly one selector (the catalog) and one body library
(the `*Tokens` nouns).

### Why not "replace": the unrecognized-trait floor

The catalog can reference traits with no schema-rust-next body recipe (an
author writes `{| QueryMatcher [ (matches { candidate.Node } Boolean) ] |}`
for a trait the runtime crate hand-implements). schema-rust-next must NOT try
to emit a body for those — there is none to emit. They are still real catalog
entries that `verify_catalog` checks. So consumption is two-tier:

- **Recognized standard traits** (`Display`, `Ord`, `AsRef`, the scalar
  comparisons) → schema-rust-next emits the body from its recipe library.
- **Unrecognized traits / hand-written methods** → schema-rust-next emits
  NOTHING but records the reference for the surface/verify loop (the crate is
  trusted to provide them; `verify_catalog` is the trust boundary).

## (b) What "consuming" means, per entry

For each `ReferencedImpl` from `schema.referenced_impls()`, resolve the
target to its lowered declaration and dispatch on `entry()`:

| `ImplReference` | Recognized standard? | Consumer action |
|---|---|---|
| `Marker(Display)` on string/path newtype | yes | emit `impl Display { self.payload().fmt(f) }` |
| `Marker(Ord)` | yes (derive-class) | route to the `derive`/`#[rkyv(derive)]` set, not an `impl` block |
| `Marker(AsRef)` etc. on scalar newtype | yes | emit the corresponding scalar body |
| `TraitImpl(QueryMatcher, [sig])` | no recipe | emit nothing; record for verify (crate provides it) |
| `InherentMethod(word_count …)` | no recipe | emit nothing; record for verify |

The recognized set is a closed, named classification owned by a new
schema-rust-next noun (below), keyed on the trait `Name` plus the target's
`TypeReference` shape (so `Display`-on-newtype-over-String resolves to the
payload-delegating recipe, and `Display`-on-anything-else is rejected as
unrecognized-under-this-shape rather than mis-emitted). "Emit nothing" is the
correct, honest action for a reference whose body the generator does not own
— the alternative (guessing a body) is unsound.

## (c) Minimal correct consumer design — file:fn + change

The design is four moves in schema-rust-next. It keeps the existing
`StandardNewtypeImplTokens` bodies, swaps their *trigger*, and adds the
surface-producer that makes `verify_catalog` meaningful.

### Move 1 — carry the catalog into `RustModule`

`RustModule` (`lib.rs:251-265`) gains one field
`referenced_impls: Vec<RustImplReference>` where `RustImplReference` is a new
owned noun (the `ReferencedImpl<'schema>` borrow cannot cross into the owned
module). `Schema::lower_to_rust` (`lib.rs:403-459`) populates it:

```
referenced_impls: self
    .referenced_impls()
    .iter()
    .map(|reference| reference.lower_to_rust(context))
    .collect(),
```

New `impl LowerToRust<RustImplReference> for ReferencedImpl<'_>` carrying
`target: Name`, plus the entry as an owned mirror `RustImplEntry` (an enum
`Marker(Name) | TraitImpl(Name, Vec<RustMethodSignature>) | InherentMethod(
RustMethodSignature)`). `RustMethodSignature` mirrors `name + params +
return_reference` (it already round-trips `TypeReference`, which
schema-rust-next handles natively via `RustTypeReferenceTokens`,
`lib.rs:1531-1585`). This is mechanical lowering, same pattern as every other
`LowerToRust` impl in the file.

### Move 2 — the standard-impl recipe classifier

New noun `StandardImplRecipe` — a data-bearing type, NOT a ZST namespace
(test from AGENTS.md: its job is "resolve a (trait, target-shape) pair to a
body recipe," which is real owned behavior). It holds the resolved trait
`Name` and the target's `TypeReference`, and answers:

- `fn recipe(&self) -> Option<StandardImplBody>` — `Some` for the recognized
  closed set (Display/AsRef/PartialEq<&str>/PartialEq<u64>/PartialOrd<u64>/
  PartialEq<bool>) under a scalar-backed shape, `None` otherwise.
- The `None` arm is what marks an entry as "verify-only, emit nothing."

`StandardImplBody` is the existing `StandardNewtypeImplTokens` bodies,
factored to be addressable per-trait rather than emitted as one block. The
`scalar_like()` / `string_like()` / `integer_like()` / `boolean_like()`
predicates (`lib.rs:2073-2090`) MOVE onto `StandardImplRecipe` as the shape
guard — they stop being the trigger and become "is the payload-delegating
body valid for this shape." `Display`-on-Integer maps to `self.payload().
fmt(f)` (the integer's own `Display`), consistent with the current block.

### Move 3 — drive emission from the catalog

`emit_newtype_inherent_impl` (`lib.rs:5250-5255`) keeps emitting
`NewtypeInherentImplTokens` (the unconditional Bucket-1 `new`/`payload`/
`into_payload`/`From` — that is intrinsic to being a newtype, not a catalog
entry, and stays unconditional). It STOPS calling `StandardNewtypeImplTokens`
on the `emits_standard_newtype_impls()` flag.

New `RustModuleRenderer::emit_catalog_impls(&mut self, module_referenced_impls,
declarations)` runs in `RustModule::render` (insert after
`emit_newtype_inherent_impls`, `lib.rs:354`). For each `RustImplReference`:

1. Resolve `target` to its `RustDeclaration` (`module.declaration_named`,
   `lib.rs:309-313`) to get the target's `TypeReference` shape.
2. Build a `StandardImplRecipe` per trait/method in the entry.
3. `Some(body)` → `emit_item_tokens(body.into_token_stream())`.
   `None` + recognized-as-derive (`Ord`) → fold into the derive set.
   `None` + unrecognized → skip emission (verify-only).

The `RustEmissionOptions::standard_newtype_impls` flag and
`with_standard_newtype_impls()` (`lib.rs:481/540`), plus
`RustRenderContext::standard_newtype_impls` / `emits_standard_newtype_impls`
(`lib.rs:1344/1465`), are DELETED — the catalog is the trigger, so the flag
is dead. `build.rs:159` drops `.with_standard_newtype_impls()`. This removes
the target-dependent-ergonomics defect at the root: every target lowers the
same catalog the same way.

### Move 4 — the `RustSurface` producer (makes `verify_catalog` real)

This is the half that turns `verify_catalog` from test-only into a build
invariant. New noun `EmittedRustSurface` on the schema-rust-next side, built
from a `RustModule` *after* lowering:

- `impl From<&RustModule> for EmittedRustSurface` — walks the module's
  emitted impls (the ones Move 3 actually produced, plus the intrinsic
  newtype inherents and the derive-class traits) and produces the
  `Vec<ImplFact>` describing what the generated crate genuinely exposes.
- `fn into_surface(self) -> schema_next::RustSurface` — `RustSurface::new(facts)`.

Then a new `RustModule::verify_catalog(&self, schema: &Schema) ->
Result<(), SchemaError>` that builds the surface from `self`, calls
`schema_next::RustSurface::verify_catalog(&surface, schema)`, and returns the
typed result. The build driver (`ContractCrateBuild`, `build.rs`) calls it
after lowering and before writing the file — a catalog entry whose body the
generator neither emits nor recognizes-as-crate-provided fails the build with
`SchemaError::UnverifiedImplReference` (`schema.rs:1527/1550`), naming the
exact target + signature. THIS is "meaningful on a real crate surface": the
facts come from `From<&RustModule>`, not a hand-built test vector.

Caveat the implementation agent must respect: the producer can only attest to
impls schema-rust-next *itself* emits (standard recipes + intrinsics +
derives). Hand-written-in-the-runtime-crate impls (`QueryMatcher`, inherent
`word_count`) are NOT in the emitted surface, so a naive
`module.verify_catalog` would reject them. Resolution: `verify_catalog` on the
module verifies only the **recognized** subset against the emitted surface;
unrecognized entries are passed through to a *crate scan* surface (future
work — file a follow-up bead) or, for now, recorded and reported as
"externally-provided, unverified" rather than failed. Be honest: the
build-time guarantee in this slice covers generator-emitted impls; the
full crate-scan boundary is a named follow-up, not silently claimed.

## Discipline check

Every new symbol is a method or `impl Trait for Type`: `RustImplReference` /
`RustImplEntry` / `RustMethodSignature` are data-bearing lowering nouns with
`LowerToRust` impls (same shape as `RustField`/`RustEnumVariant`);
`StandardImplRecipe` owns the (trait, shape)→body resolution (real behavior,
not a namespace); `EmittedRustSurface` is `impl From<&RustModule>`;
conversions are `From`, not `fn project_*`. Errors are the existing typed
`SchemaError::UnverifiedImplReference`. No free fns, no ZST namespace, no new
string-codegen (bodies stay `quote!`-based `ToTokens`). The deleted flag/field
trail is breaking-change-clean per the no-backward-compat override.

## Test plan (must be honestly green, no faked assertions)

1. Port `schema-next/tests/fixtures/impl-catalog/*.schema` into
   schema-rust-next fixtures; lower each and assert the emitted code contains
   the recognized bodies (`fused-markers` → `impl Display`, `impl Ord`-via-derive
   for `RecordIdentifier`).
2. `body-optional` (`StatementText {| Display (word_count {} Integer) |}`):
   assert `Display` emits, `word_count` does NOT (no recipe), and the entry is
   recorded for verify.
3. Transitive scalar: a fixture `Statement {| Display |}` over
   `StatementText(String)` — assert `Display` emits (the `scalar_like()`
   blind spot the catalog closes).
4. `RustModule::verify_catalog` round-trip: lower `fused-markers`, build the
   emitted surface, assert recognized entries verify `Ok`; mutate a fixture to
   reference an absent recognized impl and assert `UnverifiedImplReference`
   with the exact target/signature (mirror of
   `schema-next/tests/impl_catalog.rs:443-475`, now on a *generated* surface).
5. Compile-and-delegate: keep the existing
   `generated_standard_impls_compile_and_delegate_to_payloads`
   (`standard_newtype_impls.rs:69-89`) green, now reached via catalog not flag.

If any step cannot go green, report PartialGreen with the exact failing
`cargo test` output and the remaining step — do not delete an assertion to
pass.
