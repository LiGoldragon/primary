# 664 — Shape-derived capability resolver: the proposal branch, adversarially tested, vs operator's standard-impls branch

The psyche directed: *research what methods we can guarantee as standard generated impls, move
from the shallow name-allowlist to receiver-shape-derived capability resolution, and make a
proposal feature branch to demonstrate.* Two parallel-lane branches now exist, built
independently, converging on one principle from opposite ends. This report is **my resolver
branch's build + adversarial result, and the two-branch comparison with the landing
recommendation.** The four-bucket default policy and the open psyche questions live in
`reports/nota-designer/663-standard-impl-default-policy.md`; operator's branch is
`reports/operator/395`.

## The principle both branches prove: "the schema shape proves the body"

Operator's report says it exactly — *the receiver is a newtype; the payload is a closed scalar
leaf; the impl only delegates to that payload.* That is the shape-derived-capability idea, and
the two lanes implement its two faces:

- **Operator (emitter side)** — the shape decides which standard impls to **stamp**.
- **Designer (resolver side)** — the shape decides which composed-body calls a receiver may
  **resolve**.

Both replace "a method-name allowlist" with "the schema shape determines it."

## My branch — proven core, two caught flaws

Branch `next/schema-capability-resolution`: schema-next `3709fc15` (pushed), schema-rust-next
`8b147fac` (local — cross-patched to the schema-next worktree, not cleanly pushable). Built on
the 660/661 composition prototype. Full suite green: `composition_demo` 9/9, schema-next 171/0,
schema-rust-next 107/0, clippy `-D warnings` clean on both.

### What survived adversarial attack (the core — the psyche's exact ask)

> **Claim — the resolver is genuinely SHAPE-DERIVED, not a disguised name-allowlist: SURVIVED
> (high).**

The old `ComposablePrimitive::resolve(name)` matched a method name against a 3-entry string list
*ignoring the receiver*. The new resolver walks the `Expression` tree against the schema type
graph, computes `typeof(receiver)`, looks up its `ReceiverShape` (Newtype/Struct/Enum/Builtin),
and matches the call against **that shape's** capabilities:

```rust
pub fn resolve_call(&self, receiver: &Expression, method: &Name, arguments: &[Expression])
    -> Result<Capability, SchemaError> {
    let receiver_type = self.type_of(receiver)?;     // 1. typeof receiver (walks the type graph)
    let shape = self.shape_of(&receiver_type)?;      // 2. its schema shape
    let capability = shape.resolve(method)           // 3. name vs THAT shape's set
        .ok_or_else(|| SchemaError::UnresolvedCapability { /* method, receiver_type, shape */ })?;
    capability.check_arity(arguments.len())?;        // 4. arity
    Ok(capability)
}
```

So `payload` resolves on `ConfigurationPath` *because it is a newtype*, and is **rejected on a
struct** (`UnresolvedCapability{receiver_shape:"struct"}`) — the exact case the allowlist got
wrong. Type propagation is proven at depth 2: `(as_str (call (call self payload) as_str))` →
`typeof(self.payload())` computes `String` → `String` is a `Builtin` leaf → `as_str` resolves →

```rust
impl ConfigurationPath { pub fn as_str(&self) -> &str { self.payload().as_str() } }
```

Five typed `SchemaError` variants (`UnresolvedCapability`, `UnknownFieldProjection`,
`ReceiverShapeMismatch`, `UndeclaredReceiverType`, `CapabilityArityMismatch`) replace the single
`UnresolvedComposition`. The principle the psyche asked for — *"prove this receiver is a newtype,
therefore payload is valid, at the schema layer"* — is achieved and adversarially confirmed.

### What the skeptics refuted (both about breadth beyond the proven core)

> **Claim — the default-generated standard impls are always-safe: REFUTED (high).**

My branch added `StructInherentImplTokens` emitting, **by default for every multi-field
struct**, an all-fields `new` + per-field accessors. A struct with a field named `new` emits two
items named `new` → `error[E0592]: duplicate definitions`. Demonstrated on a real
`FieldNamedNew { new Integer scale Integer }`; no guard exists. **This validates operator's
conservatism** — operator scoped standard impls to scalar *newtypes*, opt-in, deliberately not
structs-by-default. The fix is either drop struct-default-by-default, or add a collision guard
(reject a field name colliding with a generated method name as a typed `SchemaError`).

> **Claim — typeof-propagation is deterministic AND correct: REFUTED (high).**

Two holes, both about chaining beyond the proven depth-2 newtype case:
- `Capability::VariantConstructor::result_type()` returns a `TypeReference::String` **placeholder**
  — a variant constructor returns the owning *enum*, not String. The only guard is a code comment
  ("never the receiver of an outer call"), an assumption, not an invariant. A probe chaining off a
  constructor result was **accepted with wrong type and no error**.
- `Expression::to_rust`'s `Field` arm blindly maps `payload`→`.0` *without consulting the
  resolver*, so `(field self payload)` on a struct emits `self.0` (invalid) while `type_of`
  correctly errors — the two projections of the same node **disagree**.
- Residual emitter `panic!`/`assert!` remain on adjacent structural paths (generic impl headers,
  missing-deref, unsupported method-bearing impls) — the same typed-errors hardening operator
  flagged as the merge blocker.

Fixes: `VariantConstructor` must carry the owning enum's type; `to_rust`'s `Field` arm must go
through the resolver; residual panics → typed `SchemaError`.

## The two-branch comparison

| | Operator `f265aad6` (schema-rust-next) | Designer `3709fc15`/`8b147fac` |
|---|---|---|
| Face | emitter — standard impls stamped | resolver — composed calls resolved |
| Scope | scalar newtypes (String/Path/Integer/Boolean) | newtype/struct/enum shape resolution + struct impls |
| Standard impls | `Display`/`AsRef<str>`/`PartialEq<scalar>`/`PartialOrd<u64>` | newtype (inherited) + struct `new`/accessors (**flawed**) |
| Resolution | n/a (emission only) | **genuinely shape-derived** (proven) |
| Default vs opt-in | opt-in `with_standard_newtype_impls()` | struct impls default-ON (**hazard**) |
| Known hazards | none | struct `new`-collision; typeof placeholder; residual panics |
| Mergeable as-is | **yes** (green, safe, scoped) | core proven; needs the fixes above |

The branches are **complementary, not competing**: operator owns the safe scalar-newtype
*emission*; my branch owns the shape-derived *resolution* (the composition side operator
explicitly deferred). Operator's standard-impl implementation is the mature one; my struct-impl
addition is superseded by operator's conservative scoping.

## Combined landing recommendation

1. **Land operator's scalar-newtype standard impls first** — green, safe, scoped (per operator's
   gates; the default-ON flip is open psyche-question 2 below).
2. **Take my resolver core** (shape-derived `MethodCall` resolution), with the fixes: drop
   struct-default-by-default (or add the collision guard); `VariantConstructor` carries its owning
   enum; `to_rust`'s `Field` arm consults the resolver; residual emitter panics → typed errors.
3. **Then `VariantMatch`** (total, payload-discard) for the variant-rewrap class — the largest
   composition opportunity, which neither branch yet covers.

The default-impl policy (the four buckets, the unconditional vs conditional vs opt-in vs
leave-to-derive tiers) is settled in `nota-designer/663`; this report adds the resolver evidence
and the comparison.

## Open questions for the psyche (from `nota-designer/663`, restated)

1. **`Deref` by default, or opt-in marker?** Real-schema counting: **189 newtypes wrap another
   schema type vs 18 scalar-backed, and only ~24 of ~207 carry a hand `Deref`** — ~88% deliberately
   do *not* deref. The data argues `Deref` is per-newtype *intent* (an opt-in `*deref` marker),
   which **refines `d3r2`'s "newtype Deref by default" wording**. This is a recommendation pending
   your call — not yet captured.
2. **Flip `with_standard_newtype_impls()` default-ON**, regenerate spirit/signal-spirit, delete the
   redundant hand-written scalar impls in the same slice?
3. **Nested-newtype transitive scalar** — should `Statement(StatementText(String))` get the scalar
   impls automatically (deletes `self.payload().payload()` hand-impls), or stay opaque at depth 2?
4. **`as_str` exception** — recommendation is *zero* named std-leaf methods (covered by `AsRef<str>`
   + `Display`); confirm you don't want a generated `.as_str()`.

## Intent note

`d3r2` (Clarified) records the direction (shape-derived capability resolution, standard impls by
default, pure-schema-first). No new capture this turn: the one substantive divergence —
Deref-as-marker vs `d3r2`'s "by default" (open question 1) — is a recommendation pending your
decision, and recording it now would pre-empt that decision. When you decide, `d3r2`'s Deref
clause gets refined accordingly.
