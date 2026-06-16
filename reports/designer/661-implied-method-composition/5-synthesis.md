# 661/5 — Synthesis: composition is real, the closure is the schema fragment

## The through-line

The psyche's idea is sound and now proven on real code: each schema shape implies a primitive
method vocabulary, and code-is-data method bodies can be **built by composing calls to those
primitives, addressed by object type**. A composed body either resolves entirely to implied
primitives (→ generated as data) or hits its first non-primitive call (→ it is business logic,
rejected loudly, hand-written). This is `5hjv`'s hand-written boundary given a *precise mechanism*
and `d3r2`'s open "mechanical-body family" resolved into a closure rather than a fixed list.

The adversarial pass sharpened it into the honest form. The single most important result:

> **The clean closure is the *pure-schema-primitive* fragment (`P(T)` + total `VariantMatch`).
> The std-method "leaf" vocabulary a real body also needs is a small curated allowlist with an
> arbitrary boundary — not a structural closure — and must be presented as such.**

## What is proven (green, on real code)

`self`-receiver composition over a closed primitive alphabet generates **byte-identical** Rust
for `ConfigurationPath::as_str` (`self.payload().as_str()`), with the boundary firing as a typed
`SchemaError` (not a panic, not silent). 7 demo tests + schema-next 171/0 + schema-rust-next
105/0 + clippy clean. The interpreter now carries a `MethodCall` node and a fallible `to_rust()`;
the three panics are gone.

## What is validated (census, on real code)

Composition deletes a **meaningful, recurring tax** that scales with component count: ~24 `Deref`
impls across spirit + signal-spirit, ~25 trait-impl one-liners in signal-spirit, all 8 `plane.rs`
cross-namespace conversions, the 24-arm `OperationKind::from_input`, the parallel-variant
re-wraps. It does **not** touch the engine's decide/handle judgment, the guardian, the store, the
validators, the matchers — and must not. That is the correct line.

## What was refined (the honest corrections)

1. **Scope the closure claim to Vocabulary A.** "Composition over shape-implied primitives" is a
   genuine closure only for the pure-schema fragment. (My `d3r2` Clarify already scopes it to
   "those implied primitives" — the report carries the leaf-vocabulary nuance the Clarify did not
   need to.)
2. **Vocabulary B (std leaves) is a curated allowlist, named as such** — minimal (`as_str`/`fmt`/
   `eq`), reviewed per entry, boundary acknowledged as policy. Or forgone entirely.
3. **Prefer the newtype-emitter route for the `Deref`/payload wall:** declare the newtypes,
   emit `Display`/`PartialEq`/`Ord` from fixed per-trait templates (as `Deref` already is) —
   cheaper than a composition interpreter for that class. Reserve composition for
   variant-isomorphism.
4. **Two correctness gates** before the larger slices: ownership-aware projection (`payload` vs
   `into_payload` by what the sink needs) for constructor-with-args; and `VariantMatch` that
   expresses payload-discard → unit-target for the 24-arm class.

## Landing slices (recommended order; operator owns code-repo main)

1. **`MethodCall` + the closed alphabet + the typed boundary** — *done in the prototype.* Land
   it: replace the `Deref`-only assert with the generic `to_rust()`-driven body emitter; the
   `as_str` triple and the `into_payload` accessors come for free.
2. **Newtype-emitter trait templates** (`Display`/`PartialEq`/`Ord`/`PartialOrd`/`Ord`) — deletes
   the largest census category (the ~24 + ~25 trait-impl wall) *without* growing the leaf
   allowlist. Cheapest big win; do it before chasing composition for that class.
3. **`VariantMatch` (total, with discard)** + **ownership-aware projection** — unlocks the
   variant-isomorphism class (`from_input`, `From<Action>`, `plane.rs`), the largest *composition*
   opportunity. Gated on the two correctness fixes in `3`.
4. **Parameter binders + `TypePath` associated calls** — `Self::new(x.into_payload())` and the
   cross-namespace From legs.
5. **Then** generic impl headers (the standing `d3r2` open piece) for the generic re-wraps.

## What this changes in the intent record

`d3r2` (Decision, Low) is Clarified: the generatable-body set is *the closure under composition
over shape-implied primitives, each call addressed by its receiver object type, not a fixed
list.* Certainty stays Low — still designed-not-integrated. The certainty is a candidate to raise
once slices 1-2 land on main. The leaf-vocabulary honesty and the correctness gates are *how*
detail and live here + in the schema-next architecture file, not in the psyche-intent record.

## The line, in one sentence

Standardize the shape-implied primitives, let bodies compose them as data over a closed
schema-shape closure with a loud typed edge, treat std-method leaves as a named curated minimum
(or skip them via newtype trait templates), and keep every genuine decision hand-written on the
generated nouns.
