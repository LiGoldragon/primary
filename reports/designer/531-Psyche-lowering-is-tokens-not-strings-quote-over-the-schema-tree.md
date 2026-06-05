---
title: 531 — The deep lowering design — every schema noun is ToTokens, lowering is quote! over the tree
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema-rust-next, lowering, quote, proc-macro, tokens, codegen, methods-on-nouns, asschema-migration]
description: |
  The psyche's two questions unify into one design: (1) every schema type
  and subobject owns its lowering (records de8i/v5n7), and (2) lowering
  should produce TokenStreams via quote!, not hand-rolled strings (record
  4np2). Together: every schema noun implements quote::ToTokens, and the
  whole lowering is quote! interpolation over the schema tree. The
  hand-rolled string emitter re-implements what proc-macro2/quote do
  natively — including the very type-AST the audit (529) asked for.
---

# 531 — Lowering is tokens, not strings — quote! over the schema tree

Your two questions are one design.

- *"Why isn't lowering a trait on every schema type/subobject?"* (deeper
  than the operator's tack-on — records `de8i`, `v5n7`).
- *"Why are we emitting all these strings — this ad-hoc Rust macro system
  — instead of feeding the typed schema into an actual Rust macro that
  fills itself from the structure tree?"* (record `4np2`).

They combine into: **every schema noun implements `quote::ToTokens`, and
lowering the whole schema is `quote!` interpolation over the schema tree.**

## What you named — a hand-rolled code generator

schema-rust-next is, structurally, a **hand-rolled Rust code generator**.
It walks the schema and builds Rust **source text** by string
concatenation — `self.output.push(format!("pub struct {} {{", name))` —
across the 52-method `RustWriter`. That is the "ad-hoc Rust macro system"
you put your finger on: it re-implements, by hand and worse, the thing
Rust already has for turning data into code. The audit (529) saw the
symptoms (the god-struct, the string-concat type building, the missing
type-AST); your question names the cause.

## The answer — `quote!` / `proc-macro2` / `ToTokens`

Rust's real machinery for "fill a code template from a structure tree" is
`quote!` over `proc-macro2::TokenStream`. You write a template and
interpolate typed data into it, including repetition over a sub-tree:

```rust
quote! {
    pub struct #name {
        #( pub #field_names: #field_types, )*
    }
}
```

`#name`, `#field_names`, `#field_types` are not strings — they are values
that implement `ToTokens`, and `quote!` splices them in as **tokens**.
`#( … )*` repeats over a collection. That `#( … )*` *is* the "structure
graph tree filling up the macro" you described: each schema node, being
`ToTokens`, interpolates itself.

## The unification — per-noun `ToTokens` + `quote!` over the tree

Combine the two:

```rust
impl ToTokens for SchemaStruct {
    fn to_tokens(&self, out: &mut TokenStream) {
        let name = &self.name;
        let fields = &self.fields;          // each Field: ToTokens
        out.extend(quote! { pub struct #name { #(#fields),* } });
    }
}
impl ToTokens for SchemaField { … }         // every subobject, down to TypeReference
impl ToTokens for TypeReference { … }        // (Vec T) -> quote!{ Vec<#inner> }, etc.
```

Lowering the whole schema becomes `quote! { #(#declarations)* }`. There is
**no emitter and no writer** — the lowering is the recursive composition of
the nouns' own `ToTokens` impls. The 3000-line string god-struct
**dissolves** into one small `ToTokens` impl per schema noun. This is your
"every single schema type and subobject has a lowering impl" — and it is
not absurd: it is exactly how `serde` (`Serialize` per type) and every
compiler back-end (codegen per AST node) are built. Many tiny local impls,
no central special-casing god-struct.

## The audit's "missing type-AST" is already `proc-macro2` — adopt, don't build

Report 529 found "string-concat type building, no `TypeExpression` AST"
and suggested *building* a `TypeExpression` enum with `Display`. Your
question makes that suggestion obsolete in the best way: **`proc-macro2`'s
`TokenStream` already IS that typed code tree.** You don't build a
type-AST and render it to strings — you adopt the one Rust ships, and
`quote!` is the renderer. The missing layer the audit pointed at is a
dependency, not a thing to write.

## Your own codebase already does this

`nota-next-derive` builds `NotaDecode` / `NotaEncode` /
`StructuralMacroNode` with `quote!` over `proc-macro2` — tokens, not
strings. So the stack is **inconsistent**: the *derives* use Rust's real
macro machinery; the schema-rust-next *emitter* hand-rolls strings. The
fix makes the emitter look like the derives.

## The one real choice — visibility

The single thing to decide. The workspace values **source-visible emitted
Rust** (checked-in `src/schema/*.rs`, reviewable — a real constraint). Two
ways to keep `quote!` *and* that value, plus the radical option:

1. **build.rs + `quote!` + `prettyplease`** — build the `TokenStream` from
   the schema, run `prettyplease::unparse(&syn::parse2(tokens)?)`, write
   the result to the checked-in `src/schema/*.rs`. You get the real
   machinery **and** the visible file. `proc-macro2`/`quote` work fine
   outside proc-macro crates (build scripts, libraries) — you only need a
   `proc-macro` crate for `#[proc_macro]` entry points. *This is the
   smallest move from today: keep the write-to-.rs step, replace only the
   string-building with `quote!`.*
2. **A real proc macro** — `schema!("path/to.schema")` expands to the types
   inline in the consumer. Maximally "feed the data into an actual Rust
   macro," but the generated code is no longer a checked-in file (only
   `cargo expand` shows it) — it trades the source-visibility value away.

I'd take **(1)** first: it dissolves the god-struct, adopts the token-tree,
keeps the visible `.rs`, and is the least disruptive to the rest of the
stack — then consider (2) later if inline expansion proves worth losing
visibility.

## Why this is deeper than the tack-on

The operator added a trait at the top that delegates to the same string
emitter — the verbs didn't move and the strings stayed. The deep version
moves the verbs onto **every** noun *and* changes their currency from
strings to tokens. The god-struct doesn't get a façade; it ceases to
exist. And it lands exactly where the Asschema-removal `from_source`
rewrite goes — so the migration is the moment to write the new emitter as
`ToTokens`-over-`quote!` rather than extend the hand-rolled one.

## `ToTokens` has no context — the pattern (operator was right to flag this)

`quote::ToTokens::to_tokens(&self, tokens: &mut TokenStream)` has a **fixed
signature with no context parameter.** So when rendering needs context —
feature-gated NOTA derives, private-type field visibility — you cannot
thread it through a plain `ToTokens` impl. The operator caught this; the
immediate shape (methods on the nouns returning `TokenStream` with an
explicit render context, `fn render(&self, cx: &RenderContext) ->
TokenStream`) is the correct first move.

For the end state, **split the context by kind** — this is where "bake it
into the noun" needs a caveat:

- **Intrinsic per-noun properties** (a declaration's *visibility*) genuinely
  belong **on the noun**. Bake those in, and `ToTokens` is clean for them —
  exactly as the operator plans.
- **Generation-wide options** (whether the `nota-text` derive is emitted —
  a build-level switch, not a property of any one struct) must **not** be
  baked into every noun; that duplicates one global flag across hundreds of
  values. For those, keep `ToTokens` but thread context through a
  **context-carrying wrapper** — the idiomatic quote pattern:

  ```rust
  struct InContext<'a, T>(&'a T, &'a RenderContext);
  impl<T: RenderInContext> ToTokens for InContext<'_, T> {
      fn to_tokens(&self, out: &mut TokenStream) { self.0.render(self.1, out) }
  }
  // call site: quote! { #( #fields.map(|f| InContext(f, cx)) )* } — context flows, ToTokens stays
  ```

So "direct `ToTokens` impls become clean" is true for the
*intrinsic-property* rendering; the *generation-wide* rendering stays on a
wrapper-plus-context, not on baked-in flags. The runtime/plane emission
(projections, engine emission, the `PlaneType` cross-object logic) is where
context concentrates and where this distinction earns its keep — the
declarations slice the operator started with is the clean warm-up.

## Lineage

Captured: `4np2` (tokens not strings), building on `de8i` + operator
`v5n7` (per-noun lowering). Connects report 529 (the audit — the
god-struct, string-concat, missing type-AST) and 530 (lowering on the
nouns). Note: `de8i` (designer) and `v5n7` (operator) are a near-duplicate
pair — flag for the next intent-maintenance consolidation.
