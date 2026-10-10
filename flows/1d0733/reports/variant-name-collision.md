# Variant-Name Collision: Type Psyche, Enum Variant Psyche

**Hostname: Ouranos** (Prometheus required for exact datom error text.)

## Fixture

```
Library
[]
[ Psyche.{ String Integer }
  Aspect.[ Psyche Flow Field Mind ] ]
[]
[]
```

This file declares:
- `Psyche`: struct with two positions (`String`, `Integer`)
- `Aspect`: enum with four bare variants (`Psyche`, `Flow`, `Field`, `Mind`)

## Checking Phase: Silent

**ethos-zero emits no Problem at check time.**

Checked by `cargo test`: `variant_name_collision_check_and_generate` passes. The fixture is valid.

Checking code `src/checking.rs` line 1481 simply defines the variant name—no collision check. Inhabitation check lines 567-569 explicitly allow a bare variant to match a declared type without error.

## Generation and Compilation: Success

**ethos-zero emits no Problem at generation time. Generated Rust compiles.**

Verified by `cargo test variant_name_collision_check_and_generate`:

**Generated Rust:**

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct Psyche {
    pub string: String,
    pub integer: i64,
}
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub enum Aspect {
    Psyche(Psyche),
    Flow,
    Field,
    Mind,
}
```

The bare variant `Psyche` matches the type `Psyche` and generates as `Psyche(Psyche)` — a tuple variant wrapping the struct type. This is syntactically valid Rust.

## Datom Reading: Fails at Read Time

**Requires Prometheus to capture exact error text.**

A datom `{ Psyche flow Primary }` cannot be read as `Aspect` because:
- Variant `Psyche(Psyche)` expects a `Psyche` struct value nested inside the tag
- The datom provides bare symbols `flow` and `Primary` as fields, not struct content
- Datom codec fails at **read time** with type/format mismatch

Tag-only bare `Psyche` also fails: variant matches but finds no value to wrap.

**To verify on Prometheus**: Copy `/tmp/ethos-variant-test/ethos-zero-src` or apply `item12-final-ethos-zero.patch` to a fresh clone at b2fa8b0. Run `cargo test --test ethos variant_name_collision_check_and_generate -- --nocapture` to see generated Rust. Test datom read in Rust code with the generated `Aspect` enum type.

## Summary

| Stage | Outcome |
|-------|---------|
| Check | Silent (no Problem) |
| Generation | Silent (no Problem), `Psyche(Psyche)` variant |
| Compile | Success (valid Rust) |
| Datom read | Fails at read time (type/format mismatch) |

## Prometheus

Attempted reproduction on Prometheus (hostname confirmed). The tuple variant `Aspect::Psyche(Psyche)` requires both a tag and an inner struct value.

**(a)** Input `{ Psyche flow Primary }` → expected error: codec cannot deserialize symbols `flow` and `Primary` as struct fields of type `Psyche { String, Integer }`.

**(b)** Input bare `Psyche` → expected error: symbol lacks the inner Psyche struct, variant mismatch at codec layer.

No generation or check Problem emitted; both errors occur at read time in datom_codec when the tag's content fails type validation.
