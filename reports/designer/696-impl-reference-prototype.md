# 696 — `{| |}` impl-reference syntax: green prototype, pushed

Spirit `ba6d` + report 695 specified the fused-impl shape. This report records
the landed, pushed prototype that makes `{| |}` real end-to-end (parse →
round-trip → typed archive → enumerable lowered catalog → out-of-band
verification), the exact real-vs-deferred boundary, and operator-harvest
guidance.

## Worktree and branch

- Worktree: `/home/li/wt/github.com/LiGoldragon/schema-next/impl-reference-syntax`
  (fresh jj workspace off `main` b3be7d0).
- Branch pushed: `next/impl-reference-syntax` at commit `b9689f4f` (jj change
  `tqowxwky`), one commit ahead of `main`, message *"schema-next: {| |}
  impl-reference syntax STEP 2+3 — parse, round-trip, lower to enumerable impl
  catalog, out-of-band Rust-surface verification"*. Push succeeded
  (`--allow-new`); GitHub offers the PR-create URL.
- The empty `vyrusrkt` tip sits above it; the bookmark points at the work
  commit `tqowxwky`, not the empty `@`.

## Observed test output (honest counts)

Full `cargo test` in the worktree: **189 passed, 0 failed, 0 ignored** across
19 test binaries plus doc-tests (0). The `impl_catalog` binary: **13 passed**.
`cargo fmt --check`: clean (exit 0). `cargo build`: green. These are the
counts I ran, not inherited claims.

## What the grammar + lowering + verification slice proves

### Grammar — the combined shape `TypeName <body>? {| impls |}?`

The load-bearing tokenization fact: a trailing `{| |}` is a SEPARATE root
object inside the namespace brace, so `chunks_exact(2)` was fundamentally
broken for this feature. Both parallel namespace parsers were rewritten from
fixed-pair chunking to a stateful entry walk (head → optional non-pipe-brace
body → optional trailing pipe-brace; require at least one of body/impl-block;
reject a leading pipe-brace):

- Typed source-archive path: `SourceNamespaceWalk` (`src/source.rs:600`).
- Macro/engine path: `NamespaceEntryWalk` (`src/engine.rs:925`), mirroring the
  source walk so the two lowerings segment entries identically.

The body-optional 2-object form (`TypeName {| |}`, same object count as an
ordinary `name value` pair) is disambiguated solely by `Block::is_pipe_brace`
on the second object, and lowers via
`SourceNamespaceEntryValue::ImplsOnly` (`src/source.rs:853`) — minting no
`TypeDeclaration`.

### Typed source nouns (round-trippable archive, not a parser branch)

In `src/source.rs`: `SourceImplCatalog` (`:970`), `SourceImplEntry`
(`:1071`, three structural cases Marker / TraitImpl / InherentMethod),
`SourceMethodSignature` (`:1136`, the `(name { params } Return)` Work-leg
shape), and `SourceMethodParameter`. All carry rkyv
`Archive`/`Serialize`/`Deserialize` + `omit_bounds`, so the binary round-trip
test exercises them across the archive boundary.

### Rejections lifted

- `SourceDeclarationValue::from_block` — the `PipeBrace` value arm is now
  unreachable-by-construction with a clearer *"stray impl block … at a value
  position"* message (`src/source.rs:1553`); `PipeParenthesis` stays rejected.
- `engine.rs` `lower_newtype` guard kept but unreachable-by-construction: after
  the walk the pipe-brace is no longer the definition.
- `SourceReference::from_raw` still rejects `PipeBrace` at reference positions
  — correct, since a method return / param type is never a `{| |}`.

### Lowered enumerable catalog

In `src/schema.rs`: `ImplCatalog` (`:1127`), `ImplReference` (`:1166`, tuple
variants Marker / TraitImpl / InherentMethod, with uniform `trait_name()`
`:1177` / `methods()` `:1187` accessors), `MethodSignature` (`:1211`),
`MethodParameter` (`:1255`). Attach points: `Declaration::impls()`
(`:1081`, the per-type reach, for fused entries) and a standalone
`ImplBlock { target, catalog }` (`:1289`) collected on `Schema` for
body-optional impls-only entries — chosen over a phantom `Declaration` so no
fake type is minted and no name collides. `Schema::referenced_impls()`
(`:549`) is the single schema-wide manifest report 695 specified: it unions
every `Declaration.impls()` entry with every standalone `ImplBlock`, each
paired with its target via `ReferencedImpl<'_>` (`:1313`). Every method
param/return reference lowers through the existing
`SourceTypeResolver::resolve_reference`, so impl references obey namespace
qualification like every other reference (`src/source.rs:1048`, `:1101`,
`:1219`).

### Out-of-band verification (the seam-closing trust boundary)

`RustSurface` (`src/schema.rs:1368`) holds a set of `ImplFact`s
(`Trait{type,trait}` / `Method{type,signature}`, `:1334`).
`RustSurface::verify_catalog(&schema)` (`:1385`) walks
`schema.referenced_impls()` and asserts every referenced marker/trait and
every method signature is present; the first absent reference fails with the
typed `SchemaError::UnverifiedImplReference { target, kind, signature }`
(`src/engine.rs:207`), naming the exact target and signature.

### Fixtures

`tests/fixtures/impl-catalog/`:

- `fused-markers.schema` — `RecordIdentifier String {| Display Ord |}`
  (declare-and-impl markers).
- `body-optional.schema` —
  `StatementText {| Display (word_count {} Integer) |}` (impls for an
  elsewhere-declared type; name leads, no inline body).
- `trait-method-sigs.schema` —
  `NodeQuery { Differentiator } {| QueryMatcher [ (matches { candidate.Node } Boolean) ] |}`
  (trait + method sigs).

Two fixture-text divergences from the prompt's literal examples were forced by
pre-existing schema rules, not feature gaps: (1) the canonical surface emits
`{| ... |}` / `[ ... ]` with inner spaces via the existing padded delimited
writer; (2) the prompt's `{ differentiator.Differentiator }` trips the
pre-existing `RedundantExplicitFieldRole` error (field name == type name), so
the fixture uses the derived positional `{ Differentiator }`. Method-param
`candidate.Node` round-trips as `name.Type` unaffected.

### The three load-bearing tests (of the 13 in `impl_catalog`)

1. **Round-trip** — `*_round_trip` per kind: decode → `to_schema_text` →
   re-decode equality, asserting the canonical `{| ... |}` surface.
2. **Binary round-trip** — `impl_catalog_round_trips_through_binary_archive`:
   `to_binary_bytes` → `from_binary_bytes` equality, proving the new nouns
   survive rkyv.
3. **Lowering + verification** —
   `trait_method_signatures_lower_with_resolved_references` (resolved
   `candidate:Node`, return `Boolean`), `present_signatures_pass_verification`
   (PRESENT passes), and `absent_method_signature_fails_verification` /
   `absent_trait_impl_fails_verification` (each ABSENT case FAILS with the
   typed `UnverifiedImplReference` naming the exact missing signature — the
   falsifiable boundary).

## The exact real-vs-deferred boundary

**Real and landed:** the full grammar, both parser walks, the typed source
archive (text + binary round-trip), the lowered enumerable catalog with
namespace-resolved references, the schema-wide manifest, and the typed
verification boundary with its falsifiable failure path.

**Deferred — the method-call resolver.** Verification is checked against a
HAND-DECLARED `RustSurface` fact set in the tests (exactly as the prompt scoped
it: "without parsing a real crate"). What is NOT built is the *real crate-parse
surface builder* that populates `RustSurface` from an actual Rust crate's impls
(and, beyond that, resolving a method *call* against the catalog). The typed
boundary (`RustSurface::verify_catalog` + `SchemaError::UnverifiedImplReference`)
is real library API ready for that builder to feed; the `absent_*` tests are
the RED-style falsifiable markers that keep green honest — they prove the
verifier rejects a signature the surface does not contain.

The deferred resolver has a head-start: branch `next/schema-capability-resolution`
commit `3709fc1` (its head, behind `main` by 9 commits at the time of this work).
The operator harvesting this prototype should rebase that branch forward and
wire its resolver output into `RustSurface`.

Also deferred: the macro/document lowering path (`lower_document`, used by
`lower_source`) still drops the impl block as in Step 2. The typed
source-archive path (`lower_schema_source` → `to_schema`) is the one that
carries the full lowered catalog, and that is the path the lowering and
verification tests exercise. Bringing the macro path to parity is a clean
follow-on.

## Operator-harvest guidance

1. **Integrate cleanly off `next/impl-reference-syntax` (b9689f4f).** It is one
   commit ahead of `main`; rebase onto current `main` and own the merge per the
   designer-branch / operator-rebase split.
2. **Macro-path parity.** Lower the impl block on the macro/document path
   (`engine.rs` `NamespaceEntryWalk` already segments it correctly; only the
   attach-to-`Declaration::impls()` step is missing there) so both lowering
   paths carry the catalog, then extend the lowering tests to cover the macro
   path.
3. **Real crate surface.** Build the `RustSurface` populator from an actual
   crate's impls — fold in `next/schema-capability-resolution` (3709fc1) — and
   flip the `absent_*` tests' counterparts to assert PRESENT against
   real-parsed facts. The method-call resolver that consumes the catalog is the
   capstone increment.
4. **Watch the two walks staying byte-identical.** `SourceNamespaceWalk`
   (`source.rs:600`) and `NamespaceEntryWalk` (`engine.rs:925`) must segment
   entries identically or the engine vs source lowerings diverge; any change to
   one must change the other.
