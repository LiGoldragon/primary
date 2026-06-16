# 661/3 — The composition design, and the two vocabularies

## The starting point

The code-is-data interpreter today is a three-node tree (`reaction-expand/src/schema.rs:1072`):

```rust
pub enum Expression { SelfReceiver, Field(Box<Expression>, Name), Reference(Box<Expression>) }
```

`to_rust()` is total over exactly one body family — newtype payload projection: `&self.0` is
`(reference (field self payload))`. That is the entire generatable surface today (one `Deref`
body). The design grows it to the **closure under composition over the implied primitives**.

## The Expression extension

Two new capabilities, and no more — application and total variant discrimination:

```rust
pub enum Expression {
    SelfReceiver,                                  // &self leaf (borrow)
    SelfValue,                                     // self leaf (move) — for into_* bodies
    Field(Box<Expression>, Name),
    Reference(Box<Expression>),
    TypePath(TypeReference),                       // Self, nexus::OriginRoute — a call head
    MethodCall { receiver: Box<Expression>, method: Name, arguments: Vec<Expression> },
    VariantMatch { scrutinee: Box<Expression>, arms: Vec<VariantArm> },
}
```

`MethodCall` is application over the recursive `(Head Arg…)` form — the method resolves against
the *receiver's schema shape*, never a free function. `VariantMatch` is the **only** control
flow: a *total* match whose arm set **is** the scrutinee enum's variant set (exhaustiveness is
structural, not authored), each arm yielding a recursively-closed result. `SelfValue` splits
from `SelfReceiver` because move-vs-borrow (`into_payload`'s `self.0` vs `payload`'s `&self.0`)
is real in the emitted code and must be carried as data, not inferred.

`to_rust()` becomes `Result<String, SchemaError>` (was infallible `String`): resolution
failures surface as typed errors, replacing the prototype's three panics.

## The closure rule

Let `P(T)` be the implied-primitive set of type `T`'s schema shape (the catalog in `1`). A call
`(call receiver method args…)` **resolves** iff `method ∈ P(typeof(receiver))`. A body is
**generatable** iff every call resolves (recursively — a callee may itself be a generatable
method) and every leaf is `self` / a parameter / a `Field` / a `TypePath`.

**Resolution is "addressed by object type" — a deterministic single-table lookup**, exactly as
`3742`/`wqdi` resolve use-site names: compute `typeof(receiver)` structurally, look `method` up
in `P(typeof(receiver))`. Names are unique within a shape, so exactly one primitive matches —
no search, no inference, no guessing.

**The sharp edge:** the first call whose `method ∉ P(typeof(receiver))` means the body is
genuine business logic → generation **fails loudly** with a typed `SchemaError`
(`UnresolvedComposition { target_type, method, receiver_type }`), never silently emitted wrong
and never a panic. Business-logic methods simply aren't declared as data; they stay
hand-written. The census confirms this edge lands exactly at the first `guard_*`/`store.*`/
cross-product call.

## The refinement the adversaries forced: two vocabularies

The design's first framing — "the closure over shape-implied primitives is closed, finite, and
*derivable*" — is **true for one vocabulary and false for another**, and the headline example
straddles both. This is the central correction (full attack in `4`):

### Vocabulary A — `P(T)`, the pure schema primitives (a genuine closure)

Newtype `{new, payload, into_payload, From<Inner>}`; struct `{new, accessors, withers,
single-field From}`; enum `{per-variant constructor, route, is_/as_/try_, From<unique
payload>}`; plus `VariantMatch` over the receiver's *own* declared variant set. This **is**
closed, finite, shape-derivable, and terminating. No `+`, no `if`, no loop, no IO is reachable
because none is a primitive of any schema shape. The `plane.rs` From legs, the 24-arm
`OperationKind::from_input`, the cross-namespace conversions, the `Deref`/payload wall — all
live here. **Here the thesis holds in full.**

### Vocabulary B — the std "leaf registry" (a curated allowlist, NOT a closure)

To express `self.payload().as_str()`, the second call (`as_str`) resolves to *nothing in any
schema shape* — it is `String::as_str`. The design rescued this with a "leaf registry" of
allowed std methods (`as_str`, `fmt`, `Vec::iter`, integer `==`/`cmp`). The skeptic showed this
is **not shape-derivable and not principled**: `self.payload().trim()` is *structurally
identical* to the accepted `as_str` body, differing only in which `str` method — and `trim`,
`to_lowercase`, `chars`, `wrapping_add` are all reachable by the exact same construction. The
only thing keeping `wrapping_add` out and `as_str` in is **a human deciding what to type into
the list**. That is a policy allowlist with an arbitrary boundary, not a structural closure.

### The honest position

- **The principled core is Vocabulary A.** Scope the *closure claim* to the pure-schema
  fragment — that is where "composition over shape-implied primitives" is genuinely closed, and
  the census says it is the bulk of the win (the variant-isomorphism class especially).
- **Vocabulary B is a separate, explicitly-curated, finite allowlist** — present it honestly
  as such. Keep it minimal (`as_str`/`fmt`/`eq`); everything past it is business logic. Its
  boundary is reviewed policy, one entry at a time, *not* "derivable from shape."
- **For the pure-`Deref`/payload wall, prefer the cheaper move:** declare the newtypes in the
  schema and let the newtype emitter emit `Display`/`PartialEq`/`Ord` from fixed per-trait
  templates (as it already emits `Deref`). That deletes the wall *without* the leaf registry at
  all. Reserve composition for the variant-isomorphism class a template cannot express.

## Two correctness hazards on the slices beyond the proven core

The skeptics found (with code) that the naive projection generates *non-compiling* Rust for two
in-scope-claimed cases — both deferred past the proven slice, both flagged as gates:

1. **Borrow/move at argument position.** `Self::new(x.payload())` passes `&Inner` where `new`
   wants `Inner` — compiles only for `Copy`. The resolver must pick `into_payload()` (owning)
   vs `payload()` (borrow) by *what the sink needs*, not by name. **Ownership-aware projection**
   is the gate for constructor-with-args composition.
2. **Variant discard → unit target.** `Input::State(_) => Self::State` (the 24-arm `from_input`)
   maps a payload-carrying source variant to a *unit* target, discarding the payload.
   `VariantArm` must express the discard pattern + a no-argument target constructor, or it emits
   `Self::State(state)` against a unit variant — non-compiling. The largest opportunity needs a
   richer `VariantMatch`.

(Generic impl headers — `From<Action> for NextStep` over five type parameters — remain the
known `d3r2` open piece; the prototype emitter asserts non-generic.)

## What is committed vs open

**Committed:** the closure rule scoped to Vocabulary A; the typed-`SchemaError` boundary; the
node *shapes* (`MethodCall`, `TypePath`, `VariantMatch`, `SelfValue`); resolution-by-shape-table;
the smallest extension (`4`).

**Open / undecided (flagged for the psyche or a syntax pass):** the call atom name (`(call recv
method args…)` vs the bare `(recv method args…)` application form — leaning head-led for parse
clarity); the parameter-binder leaf (`(param x)` vs `(arg x)`); `Self::new` as a `TypePath`
receiver vs a dedicated node; `VariantMatch` binder elision for unit variants; and the size and
membership rule of the curated leaf allowlist (Vocabulary B) — or whether to forgo it entirely
in favor of newtype-emitter trait templates.
