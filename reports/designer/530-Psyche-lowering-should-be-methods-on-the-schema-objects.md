---
title: 530 — Why lowering should be methods on the schema objects, not the RustWriter god-struct
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema-rust-next, emitter, lowering, methods-on-nouns, abstractions, code-quality, asschema-migration]
description: |
  The psyche asked why the lowering into Rust isn't a trait on the
  deserialized schema objects. It half is — there's a lower_to_rust trait
  — but it's a FAÇADE over the RustWriter god-struct: the trait impls just
  hand self to the emitter, which holds all the verbs. The clean shape is
  render-methods on the Rust-model nouns. This is the methods-on-nouns
  discipline applied to emission, and the Asschema migration is the moment
  to do it. Captured as record de8i.
---

# 530 — Lowering belongs on the schema objects

> *"Why is the lowering into Rust not a trait implementation on these
> deserialized schema objects themselves?"*

The instinct is right, and the code is subtler than it looks.

## What's actually there — a façade trait over a god-struct

There IS a lowering trait (`schema-rust-next/src/lib.rs:83-139`):

```rust
trait LowerToRust {
    fn lower_to_rust_file(&self, emitter: &RustEmitter) -> GeneratedFile;
    fn lower_to_rust_code(&self, emitter: &RustEmitter) -> RustCode;
    fn lower_to_rust_module(&self, emitter: &RustEmitter) -> RustModule;
}
```

So on the surface, lowering *is* a method on the schema objects:
`schema.lower_to_rust_file(emitter)`. But look at what the impl does — it
takes an `emitter: &RustEmitter` and **hands `self` straight back to it**.
The trait method is a thin wrapper; the actual work happens in
`RustEmitter` → `RustWriter`, which holds **all** the verbs as 52 `emit_*`
methods that take the model types as arguments:

```rust
impl RustWriter {
    fn emit_struct(&mut self, visibility: Visibility, declaration: &RustStruct) { … }  // :1221
    fn emit_enum(&mut self, visibility: Visibility, declaration: &RustEnum) { … }       // :1240
    fn emit_type(&mut self, declaration: &RustDeclaration) { … }                        // :1137
    // … 50 more
}
```

And the Rust-model nouns themselves — `RustStruct` (`:640`), `RustEnum`
(`:690`), `RustField` (`:667`), `RustEnumVariant` (`:717`) — are **passive
data**. They carry fields; they have no `render`/`lower` of their own.

So the answer to your question: lowering *looks* like it's on the objects
(the `lower_to_rust` trait), but it's **methods-on-nouns in name only.** The
verbs live on the `RustWriter` god-struct; the nouns are inert. The trait
is a façade over `emitter.emit_struct(struct)` instead of `struct.render()`.

## Why it ended up this way — incidental pulls, none fundamental

1. **The string buffer.** `RustWriter` owns the output buffer and every
   method does `self.output.push(line)`. Once one object owns the buffer,
   it becomes the gravitational centre that pulls all the emit logic into
   itself. That is the single biggest cause of the god-struct.
2. **Genuinely cross-object logic.** The plane split, the
   NexusWork→NexusAction projections, the plane-type predicates — these are
   about *relationships between* objects, not one object. That is real, but
   it's not a reason for a god-struct; it's the *missing `PlaneType` type*
   the audit (529) found. Give the cross-object concept its own type.
3. **Context threading.** Imports, generation options, resolved names —
   the per-object render needs them. Thread them as a small `RenderContext`
   argument, not by hoisting all logic into the context-holder.

None of these is fundamental. Each has a clean answer that keeps the verbs
on the nouns.

## The clean shape — render on the nouns

The verbs move onto the Rust-model nouns. Each renders itself and composes
recursively; the output is **typed `RustCode`**, not a mutated shared
buffer:

```rust
trait Render {
    fn render(&self, context: &RenderContext) -> RustCode;
}

impl Render for RustStruct  { fn render(&self, cx: &RenderContext) -> RustCode { /* its own fields */ } }
impl Render for RustEnum    { fn render(&self, cx: &RenderContext) -> RustCode { /* its variants, each variant.render(cx) */ } }
impl Render for RustField   { … }
impl Render for TypeExpression { … }   // the missing type-AST from 529 — replaces string-concat type building
```

`RustModule::render(cx)` calls `declaration.render(cx)` for each; the
`lower_to_rust_*` trait stays as the *entry point* but its body becomes
`self.into_module().render(cx)` rather than delegating to a god-struct. The
52-method `RustWriter` dissolves into ~6 `Render` impls on the nouns + a
small `RenderContext` + the `PlaneType` type for the cross-object bits.

This is the audit's three emitter findings — the `RustWriter` god-struct,
the missing `TypeExpression` AST, the scattered `PlaneType` predicates —
**all the same fix**, unified: put the verbs on the nouns, and the
cross-object concepts become their own types.

## The one nuance — where the trait lives (layer separation)

If the trait were on schema-next's *schema* objects (`Asschema`/`SourceXxx`),
you'd worry it makes schema-next depend on Rust-emission. It doesn't have
to: schema-rust-next **defines** `Render` and **implements** it for the
types it needs (it already depends on the schema crate; implementing your
own trait for a dependency's type is allowed — no orphan issue). But the
more natural home is schema-rust-next's *own* Rust-model nouns (`RustStruct`
etc.) getting the `Render` impls — pure methods-on-nouns, no cross-crate
concern at all. The schema stays Rust-agnostic; the emission crate owns
both the model and its rendering.

## Why now — symmetry with the pipeline, and the migration moment

This is the same insight as "resolution = methods on the source nouns"
(records 520/524), applied to the *other* arrow. The pipeline is:

```
NOTA  --deserialize (methods on the types, via the structural macro codec)-->  schema-in-rust  --lower-->  rust
```

The deserialize arrow is **already** methods-on-the-objects. The lower arrow
should be too — and currently isn't (the façade). Both arrows belong on the
schema objects; the god-struct emitter is the asymmetry to remove.

And the timing is exact: the Asschema-removal adds `RustModule::from_source`
to *this* emitter. Bolting a new entry onto a 52-method god-struct deepens
the problem; doing the `from_source` rewrite as a move to `Render`-on-nouns
fixes the audit's biggest smell *and* lands the migration in one motion.

## Lineage

Captured: record `de8i` (Principle). Applies records 712/882 (methods on
data-bearing nouns) to the emitter. Connects: report 529 (the audit — the
`RustWriter` god-struct, `TypeExpression`, `PlaneType` findings) and records
520/524 (the Asschema-removal pipeline, resolution-on-source-nouns).
