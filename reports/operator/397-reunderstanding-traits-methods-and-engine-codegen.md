# 397 — Re-understanding traits, methods, and the engine codegen goal

The psyche clarification: the "methods available to use in schema" idea was exploratory. The
original problem was not "make a full method language." The original problem was: represent
enough of the component interface and its Rust relationships in schema that the engine's
repeated hand-wired interface code can be generated.

## What the original need was

The engine stack repeats the same structural code:

- `Input` / `Output` / action/work enums;
- per-leg newtypes and payload wrappers;
- constructors and `From` conversions;
- role/marker impls that say a generated type participates in a plane;
- standard wrapper behavior such as payload access, string display, and selected comparisons;
- later, variant rewraps between isomorphic interface enums.

Those are not business methods. They are consequences of type shape and component role.

So the schema extension was needed to express:

1. **generic frames**: `Work` / `Action` declared once;
2. **bindings**: a component applies those frames to its concrete payloads;
3. **traits/impls as relationships**: a type implements a role or standard trait;
4. **mechanical impl bodies**: only where the body is forced by shape.

That does **not** require arbitrary method calls in schema.

## What traits are for here

Traits in this schema line are not mainly "a menu of methods to call from schema." They are a
way to represent Rust relationships as data.

Examples:

```nota
EntryHandleIsAuditable {| Auditable EntryHandle |}
```

This says:

```rust
impl Auditable for EntryHandle {}
```

That is useful even with no method body, because marker traits and role traits are how
hand-written Rust can accept generated nouns through typed bounds.

For mechanical traits, schema can carry a small amount more:

```nota
EntryHandleDeref {| Deref EntryHandle [ (deref (reference (field self payload))) ] |}
```

This says:

```rust
impl std::ops::Deref for EntryHandle {
    type Target = Statement;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

That is not a general method language. It is a known trait with a known signature and a body
that the schema shape can prove for a newtype wrapper.

## What methods are for, if anything

There are three different "method" classes:

1. **Generated inherent methods**: `new`, `payload`, `into_payload`, enum constructors. These
   are already standard codegen and do not need to be written in schema.
2. **Standard trait impl methods**: `Display::fmt`, `AsRef<str>::as_ref`, scalar comparisons.
   These can be emitted from fixed templates when the payload shape proves them.
3. **Authored method bodies in schema**: expression trees such as
   `(reference (field self payload))`. These are only needed for the small mechanical family
   where the body is shape-proven. They are not needed for the engine interface generation
   goal in general.

Business methods stay hand-written:

- the decision plane;
- store/guardian/query behavior;
- actor runtime behavior;
- anything involving IO, branching policy, database state, or model-facing semantics.

## Do we already have what we need?

For the immediate goal — generate the repeated component interface code — yes, mostly.

What we need to land:

- generic frame declaration and expansion: `(| |)` plus `(Work A B C D)` use;
- concrete owned output, not Rust aliases;
- marker/role impl syntax: `{| Trait Target |}`;
- standard scalar newtype impl templates: `Display`, `AsRef<str>`, scalar comparisons;
- opt-in mechanical impls such as `Deref`, not default-on for every newtype;
- later, `VariantMatch` or equivalent for enum rewrap boilerplate.

What we do **not** need before moving on:

- a broad callable method language in schema;
- a curated std-method allowlist like `as_str`, `trim`, `to_lowercase`;
- arbitrary method-bearing trait impls;
- generic impl headers with bounds, unless a specific generated relationship forces them;
- full "Rust as schema."

## Why the method-composition branch happened

Designer followed a real thread: if a method body is data, then calls inside that body need a
resolver. The good part of that work is the principle:

> a schema-authored body is valid only when every call resolves from the receiver's schema
> shape.

That principle is useful. But it does not mean the project now needs to build a general
schema method language.

The branch is best viewed as a proof and future tool:

- keep the shape-derived resolver idea;
- use it only for narrow mechanical bodies;
- reject everything else as hand-written behavior.

## Practical landing order

The clean path is:

1. Land generic frame expansion.
2. Land scalar newtype standard impl templates.
3. Land marker impls.
4. Add opt-in `Deref` as a mechanical impl.
5. Add variant rewrap / `VariantMatch`.
6. Only then revisit authored method-body composition if a concrete generated impl needs it.

That means we can stop widening the language around "available methods" for now. The language
extension we actually need is smaller and sharper: **types, generic frames, role impls, and
shape-proven mechanical impls**.

## Operator conclusion

The psyche's instinct is right: if introducing traits made us chase "methods available in
schema," we over-read the implication. Traits are needed because the generated types must
participate in Rust relationships. Methods are only relevant when a trait relationship has a
mechanical body that the schema shape uniquely determines.

So yes: for the engine interface codegen goal, we can move on from broad method availability.
The next implementation target should be the narrow landing stack, not more method-language
research.
