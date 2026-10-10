# Traits, Plainly — the concepts behind the trait question

Requested by the psyche 2026-08-12 ("I would need a simple report
that explains all the concepts needed to understand the whole").
Every concept is shown on one running example from our own design:
`Meaning`, `CurlyText`, and the `ShapeDefined` trait. Nothing here
is a decision; forks are marked where they arise.

## 1. What a trait is

A trait is a named concept with a contract. The contract is a list
of function signatures. A type joins the concept by implementing
the trait — writing those functions for itself.

```rust
trait ShapeDefined {
    fn expects() -> &'static [ProtosShape];
}

impl ShapeDefined for Meaning {
    fn expects() -> &'static [ProtosShape] {
        &[ProtosShape::CurlyQuoteDelimited, ProtosShape::DotParenthesized]
    }
}
```

Two sentences of Rust grammar: `trait X { … }` declares the
concept; `impl X for T { … }` is type T joining it. The compiler
rejects an impl that does not match the contract exactly.

## 2. Inherent methods versus trait methods

The same function can live in two homes:

```rust
impl Meaning {                       // inherent: just a method on Meaning
    fn expects() -> … { … }
}
impl ShapeDefined for Meaning {      // trait: the method belongs to a concept
    fn expects() -> … { … }
}
```

Identical code, different meaning. The inherent method says
"Meaning happens to have a function called expects". The trait
method says "Meaning is a ShapeDefined thing" — the function's
existence follows from a concept the whole system shares. This is
the entire mandatory-trait standard in one contrast: the second
home makes the concept visible; the first hides it in a name.

## 3. Many-to-many

One trait, many types: `Meaning`, `NewString`, `Definition` all
implement `ShapeDefined`. One type, many traits: `Meaning` also
implements its parsing-context trait, `Debug`, `Clone`. A type is
legible as the list of concepts it joins — which is how a system
is understood through traits and main types.

## 4. How trait functions get called: two dispatches

**Static dispatch (generics).** `fn read<T: ShapeDefined>(…)` — the
compiler makes a separate copy of `read` for each T used, each copy
calling T's functions directly. No runtime cost; more compiled
code. The `<T: ShapeDefined>` reads: any type T that has joined
ShapeDefined.

**Dynamic dispatch (trait objects).** `Box<dyn ShapeDefined>` — one
copy of the code; each value carries a hidden table of its type's
trait functions, consulted at runtime. Slight cost per call; needed
only when different types must mix in one collection at runtime.

Rule of thumb the ecosystem follows: generics by default, `dyn`
when heterogeneity is the point. Our walk driver is generic; a
vector of mixed annotation objects inside Meaning could be `dyn`.

## 5. Who may implement what: coherence

The compiler enforces one rule: an `impl Trait for Type` may be
written only in the crate that owns the Trait or the crate that
owns the Type. Nobody else. (This is the "orphan rule" — an impl
with a foreign trait and a foreign type is an orphan, forbidden.)

Consequence: concepts must be designed where they live. If the
protos crate owns `ShapeDefined`, then a dialect crate can join its
own types to it — but a stranger crate cannot join *our* types to
anything behind our back. Coherence is why trait design is
architecture, not decoration.

## 6. Sealed traits: closing the door on purpose

By default any crate that can see a trait can join it (rule 5
permitting). Sometimes the concept's whole point is that *we*
enumerate its members — the standard ProtosShapes, for instance,
must never grow a stranger's variant. The pattern:

```rust
mod private { pub trait Sealed {} }        // invisible outside

pub trait ShapeDefined: private::Sealed {  // requires the invisible trait
    …
}
```

Outsiders can see and call `ShapeDefined`, but joining it requires
also joining `private::Sealed` — which they cannot name. The door
is closed. The asymmetry that makes this a day-one decision:
opening a sealed trait later breaks nobody; sealing an open trait
later breaks everyone who joined. Sealed-by-default keeps every
concept's membership known and its contract evolvable; unseal only
where outside implementations are the point.

## 7. Generated impls

`#[derive(Debug, Clone)]` is the standard example: the compiler
writes the impl for you from the type's own structure. Our design
generalizes this — ethos-rust writing the one-line `ShapeDefined`
match arms *is* a derive, ours: implementations produced from
schema, committed as ordinary Rust. Nothing exotic; the standard
library trains every Rust reader to expect generated impls.

## 8. Extension traits

A trait defined in one crate, implemented for another crate's
types (allowed by rule 5 — you own the trait). This is how the
ecosystem adds behavior to types it doesn't own, and how a
dialect crate could add dialect-specific capability to substrate
types without touching the protos crate.

## 9. Laws and witnesses

A trait's signatures say what functions exist; its *laws* say what
must be true of them. The law of our transcoding pair: writing a
value and reading it back yields the same value — the round-trip.
Laws live in prose and in tests; a round-trip witness is a law
being proven. A trait with laws is a concept with guarantees —
this is what makes comprehension-through-traits trustworthy
without reading implementations.

## 10. The live fork, now stateable in these concepts

One trait or a pair? **One** trait (`read` and `write` in a single
contract) says: transcoding is one concept, both directions
inseparable, the round-trip law inside it — no type may join
half. **A pair** (`Reads` / `Writes`) says: the directions are
separate capabilities that some type might join singly. The
question is exactly: can a type exist that reads but never writes
(or the reverse)? If no such type should exist, the single trait
states that impossibility in the type system itself.
