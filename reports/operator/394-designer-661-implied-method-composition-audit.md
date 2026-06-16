# 394 — Audit of Designer 661 implied-method composition

## Verdict

Designer 661 is directionally right and materially improves the design. The strongest part is
the adversarial correction: the pure schema primitive fragment is a real closed composition
space; the std-method leaf set is a curated allowlist, not a structural closure.

The prototype proves a useful first body composition (`self.payload().as_str()`) and the
composition miss path is typed (`SchemaError::UnresolvedComposition`). I verified the targeted
proof test locally:

- `schema-rust-next/reaction-expand`: `cargo test --test composition_demo` — 7 passed.
- `schema-next/reaction-expand`: `cargo test reaction` — targeted reaction test passed.

I would not merge the prototype as-is. I would merge the architecture refinement, then ask for
one hardening slice before operator main integration.

## Finding 1 — Unsupported impl-emission cases still panic/assert outside the composition miss

Severity: blocking for main, not blocking for design validation.

The report says the composition boundary is typed and the three expression panics are gone.
That is true for `Expression::to_rust`: an unresolved method call returns
`SchemaError::UnresolvedComposition`.

But the surrounding Rust impl emitter still uses `assert!` / `panic!` for unsupported schema
data:

- generic impl headers assert out at emission;
- `Deref` over a non-newtype panics;
- `Deref` without a `deref` method panics;
- method-bearing impls other than `Deref` / `Composed` panic.

Those are acceptable for a prototype, but not for the schema language. A schema author should
get typed schema errors before generated Rust emission, not a generator panic. This is the
same standard Designer applied to `UnresolvedComposition`; it should apply to the whole
`{| |}` impl path.

Required hardening before main: move these cases into typed `SchemaError` validation and add
negative tests.

## Finding 2 — The current `ComposablePrimitive` is name-only, not yet receiver-shape typed

Severity: design gap for the next slice.

The report's intended rule is receiver-type resolution: a method is valid if it belongs to
the capability set of the receiver's schema shape. The current prototype uses a closed enum
alphabet resolved only by method name: `payload`, `into_payload`, `as_str`.

That is fine for proving the syntax and boundary, but it is not yet the real capability
registry. As written, `payload` is accepted as a primitive without proving the receiver is a
single-field newtype, and `as_str` is accepted as a primitive without proving the receiver is
a string-like leaf. Rust compilation catches some bad cases later, but the schema layer should
own this check.

Required next step: give `Expression::to_rust` a type/resolution context, so `MethodCall`
resolves against `(receiver type, method name)`, not method name alone.

## Finding 3 — `Composed` as a pseudo-trait needs a name decision

Severity: medium.

The prototype encodes inherent impl methods with a fake `Composed` trait reference:

`{| Composed ConfigurationPath [ (as_str ...) ] |}`

That works mechanically, but it blurs the `{| Trait Target |}` story. `Composed` is not a
trait impl; it lowers to an inherent `impl ConfigurationPath { ... }`. Before this reaches
main, either:

- make `Composed` an explicit schema construct for inherent impls, not a trait name; or
- name the pipe-brace form as "impl block" generally and make trait-vs-inherent a typed enum
  in the data model.

I would not leave `Composed` looking like an ordinary trait.

## The fork: std leaf allowlist or pure schema only?

My recommendation: **pure schema primitives first; no general std leaf registry in the first
main slice.**

Use newtype trait templates for the easy leaf-like wall:

- `Deref`;
- `Display`;
- `PartialEq` / `Eq`;
- `PartialOrd` / `Ord`;
- perhaps `AsRef<str>` / `AsRef<Path>` when the inner type is exactly known.

Reserve composition for schema-native transformations:

- newtype payload / into-payload;
- struct field projection;
- enum constructors and projections;
- total `VariantMatch`;
- cross-namespace rewraps;
- frame leg conversions.

If a leaf allowlist is later needed, make it a separate named policy table with a small
reviewed surface. Do not describe it as implied by schema shape.

## What I accept as proven

- `(call receiver method args...)` is a workable syntax for body composition.
- `MethodCall` is the right node shape for the next expression slice.
- Unresolved composition as a typed error is the right boundary.
- The `self.payload().as_str()` proof is real and compiles/runs.
- The report's two-vocabulary correction is important and should stay in architecture.
- The deletability thesis is plausible: lots of boilerplate is schema-shape tax, not
  business logic.

## Main integration plan I would use

1. Land only architecture docs now.
2. Harden the prototype into a pushed branch pair:
   - typed validation for all unsupported impl/body cases;
   - receiver-shape-aware capability resolution;
   - decide the inherent-impl representation instead of pseudo-trait `Composed`.
3. Land pure-schema composition slice:
   - `MethodCall`;
   - newtype payload / into-payload;
   - `Reference`;
   - marker impls;
   - mechanical `Deref`.
4. Land newtype trait templates for the boilerplate wall.
5. Land `VariantMatch` and ownership-aware projection for rewrap/conversion classes.

This keeps the strong part of Designer's design and avoids turning the schema language into
an arbitrary Rust method-call frontend by accident.
