# DomainScope — forbidden-logic audit (NOTA codec + scope operations)

Audit (workflow `wf_22039cb2`, 4 agents) of the `DomainScope`/`ScopeOf` implementation across
`spirit`, `schema-rust-next`, `schema-next`, asked: *is there any hand-rolled NOTA
parsing/codec or custom logic anywhere, instead of real schema-derived typed enums?* Verdict
verified against the live daemon and current `origin/main`, not the sub-agents' stale premise.

## Verdict

**The hand-rolled NOTA codec slop is FIXED and deployed (live 0.9.2). A real residual
remains live and regen does *not* fix it: every scope *operation* is stringly-typed — it
Debug-stringifies the typed enum variants into `Vec<String>` and string-matches.** The typed
recursive enum is real; the logic on top of it is not. That half-undoes the typed-enum win
(`izib`, `k4zc`) and must be fixed in the generator + engine.

## Resolution — the operation layer is now typed (live 0.9.3)

**Resolved.** spirit `603a962` (live **0.9.3**), generated against schema-rust-next `d3bc2289`,
removes `path_segments`/`from_path`/`try_from_path` from generated scope enums and replaces them
with **typed structural operations**: `impl From<Domain> for DomainScope` (+ child `From`s) and
`contains_scope`/`contains_domain` implemented with typed `matches!` patterns. Verified
independently on `origin/main`: `path_segments`/`from_path`/`from_paths`/`two_segment_path`/`segment`/
Debug-`{:?}` are **all gone (0 matches)**; `contains_scope` is structural enum matching —
`matches!((self, scope), (Self::All, _) | (Self::Body, Self::Body) | ...)`. Query matching and
guardian equivalence now use the typed ops (`DomainScope::from(domain).expand()`). The
typed-recursive-enum model is fully realized — type *and* operations.

**One surface note for the psyche.** The scope terminal is an explicit `All` unit variant on each
`*Scope` enum (`TechnologyScope = All | Hardware(..) | Software(..)`), so "all of software" is
`(Technology (Software All))` and the bare `(Technology Software)` shorthand is rejected
(`Software` is payload-carrying, so it needs its terminal). This is arguably the *correct*
realization of `izib` (mandatory subdomains; no Option machinery): `All` is a real
domain-meaningful variant, not `Some`/`None`. Whether `All` reads clean enough vs. the bare form is
a psyche call. Designer lean: **accept `All`** — the bare form would require a payload-carrying
variant written without its payload, a non-standard codec special-case best avoided; `All`
dissolves the special case (every scope terminates at a real variant, leaf or `All`).

## What was fixed (the codec) — confirmed resolved

The earlier deployed `b373582` (0.9.1) had, *inside the schema-generated* `src/schema/domain.rs`,
a hand-rolled `nota_path_from_block` `nota_next::Block` walker plus hand `impl NotaDecode /
NotaEncode for DomainScope` and a `nota_path_to_string` formatter — the worst case: a
hand-written codec living in a `// @generated` artifact, forced by the scope enums *missing*
the `#[cfg_attr(feature="nota-text", derive(NotaDecode, NotaEncode))]` every other type had.

Operator fixed it at the right layer and shipped it:
- **`schema-rust-next` `0bc4591`** ("use derived NOTA for recursive scopes") deletes the
  hand-emitting `ScopeRootCodecTokens` and now emits the *derive* via
  `scope_enum_type_attributes → derive_attributes` — the same path every other noun uses;
  `tests/emission.rs:198-199` assert the output *excludes* `fn nota_path_from_block` and
  `impl NotaEncode for DomainScope`. Generator audit: **clean**.
- **`spirit` `980e73b`** ("use ordinary NOTA for domain scopes", live **0.9.2**) regenerated
  against it. Verified on `origin/main`: `nota_path` = **0** occurrences,
  `impl NotaDecode for DomainScope` = **0**. The hand-rolled codec is gone.
- **`schema-next` `2397d5b`** `ScopeOf` is a *declarative* `TypeReference` variant
  (`ScopeOf(Box<TypeReference>)`) mirroring `Vector`/`Optional`, pure semantic lowering over
  already-parsed blocks. Bootstrap codecs (`Name`/`SymbolPath`/`TypeReference`/`StructFieldMap`)
  are the exempt schema-compiler bootstrap. Audit: **clean**.

So the confessed sin (and the broader codec slop the sub-agents found) is genuinely resolved.
Operator did the correct generator-level fix and redeployed.

## The live residual (the real finding) — `engine.rs`, still on 0.9.2

`DomainScope` is a typed recursive enum with a proper derived codec — but **every operation on
it downgrades to `Vec<String>` of Debug-stringified variant names**:

```rust
// src/engine.rs (live 0.9.2)
pub fn matches_scope(&self, scope: &DomainScope) -> bool {
    self.path_segments().starts_with(scope.path_segments().as_slice())   // string prefix-match
}
fn two_segment_path<T: std::fmt::Debug>(root: &str, leaf: T) -> Vec<String> {
    vec![String::from(root), Self::segment(leaf)]
}
fn segment<T: std::fmt::Debug>(value: T) -> String { format!("{value:?}") }   // Debug AS the key
```

`matches_scope`/`matches_scope_set` (the operation that drives query filtering and equivalence
expansion) convert both sides to `Vec<String>` via `path_segments()`, which builds the vector
by **`format!("{value:?}")` on the enum variant** — then string-prefix-matches. Also live:
`engine.rs:920 from_paths(Vec<Vec<String>>)`, `store.rs:1374` guardian dedup routing
`Domain → path_segments() → from_path(Vec<String>) → expand()`, and the generated
`ScopePathImplTokens` (`from_path`/`try_from_path`/`path_segments`) which the generator **still
emits** — so a regen does *not* remove this.

**Why it's forbidden, not cosmetic.** `Debug` (`{:?}`) is explicitly *not* a stable API — it is
for debugging output. Using it as the load-bearing key for scope matching means a variant
rename or any `Debug` change silently breaks domain matching. And it is exactly the
stringly-typed scope the psyche eliminated from the codec, *relocated into the operations*: the
type is a typed recursive enum, but `matches_scope`/`expand`/equivalence treat it as strings.
This violates `izib`/`k4zc`/`34hu` (typed recursive enums; every segment a real variant) at the
operational level. The fix is a typed **structural** match that recurses the enum tree (and
typed `From<Domain>` conversions), retiring `path_segments`/`from_path`/the Debug `segment`.

## Out of scope / not forbidden (confirmed)

- `production_migration.rs` `current_nota()` hand-formats `format!("({area} {leaf:?})")` but
  **re-parses through the derived `NotaSource::parse`** — a one-time store-version migration
  shim; allowed.
- `src/bin/spirit-write-configuration.rs` *does* hand-roll a `nota_next::Block` walker — but for
  the **configuration** write request, not domain/scope. Out of scope here; worth a **separate
  parser-discipline review** (it's a hand-rolled parser).
- The ~42 inherent `from_nota_block` methods in generated `domain.rs` are *delegating bridges*
  (`<Self as NotaDecode>::from_nota_block`), not parsers — the scout's "~25 hand-written" was an
  overcount.

## Operator-actionable

1. **Retire the stringly-typed scope operations.** Replace `engine.rs` `matches_scope` (and
   `path_segments`/`two_segment_path`/`segment`/`from_paths`) and `store.rs` `from_path` routing
   with **typed recursive-enum operations** — a structural prefix-match recursing the scope tree,
   and typed `From<Domain> for DomainScope`. No `Vec<String>`, no `format!("{:?}")`.
2. **Generator:** stop emitting `ScopePathImplTokens` (the `Vec<String>` path API) from
   `schema-rust-next`, or replace it with typed structural helpers, so the residual cannot be
   reintroduced on regen.

## Net

Two layers, two outcomes. **Codec layer: properly fixed and deployed** — operator did the right
generator-level derive fix after the psyche caught the hand-parsing. **Operation layer: still
stringly-typed** — scope matching/expansion runs on `Vec<String>` built by Debug-stringifying
enum variants, which is brittle and untyped and undercuts the whole point of typed recursive
enums. The typed-enum win is only half-realized until the operations are typed too. This is a
generator + engine change, not a regen.
