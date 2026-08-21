# Create Trait Crate Search

Research ordered by the psyche, design session `2b34fafa`, 2026-08-21. Logged in
`psyche/Vision/assembly.md` 2026-08-21: "when something has a new method, it means
that it can be created. So that's a property, that's a trait. So maybe somebody has
made a crate for this. You can look."

Evaluated against the trait doctrine in `psyche/Vision/traitsAsCapabilities.md`:
traits are capabilities; the trait method for Create does not receive the subject as
a parameter (the type being created does not exist yet — inputs are consumed into it,
not handed to it). A derive macro that generates only an inherent `fn new` without
defining or implementing a trait does not satisfy the concept.

## Findings

### Crates searched

**`type_constructor`** (wTools/Wandalen project)
- https://crates.io/crates/type_constructor
- https://docs.rs/type_constructor
- The only published Rust crate found that defines actual construction traits rather
  than only derive macros. Defines `From_0`, `From_1<T>`, `From_2<T1,T2>`,
  `From_3<T1,T2,T3>` as distinct traits with signatures `fn from_0() -> Self`,
  `fn from_1(val: T) -> Self`, etc.
- The crate's stated purpose is working around orphan-rule restrictions for primitive
  wrapper types. Construction abstraction is a side effect, not the design goal.
- Marked deprecated on crates.io.
- Maximum arity: 3. No unified trait across arities.

**`derive-new`**
- https://docs.rs/derive-new
- Derive macro generating an inherent `fn new()` method only. No trait defined or
  implemented. Adjacent art only.

**`derive_more` — `#[derive(Constructor)]`**
- https://jeltef.github.io/derive_more/derive_more/constructor.html
- Documentation states explicitly: "Constructor is not an actual trait." Generates an
  inherent `fn new` method only. Adjacent art only.

**`bon`, `derive_builder`, `typed-builder`**
- Builder-pattern crates. Generate builder structs via derive macros. No trait is
  defined or implemented representing construction capability. Orthogonal approach.

**`frunk`**
- https://docs.rs/frunk
- Provides `Generic` (structural representation), HList, Coproduct, Monoid,
  Semigroup. No construction trait.

**`cc-traits`**, **`base-traits`**, **`extension-trait`**
- Collection operation traits; numeric/scalar traits; extension-trait macro
  infrastructure. None defines a construction trait.

**`syn-helpers` — `Constructable` trait**
- https://crates.io/crates/syn-helpers
- This trait means "this AST node can be constructed by a proc macro." It is
  proc-macro infrastructure, not a general type-construction abstraction.

**`impl-trait-for-tuples`**
- https://docs.rs/impl-trait-for-tuples
- A macro that expands trait implementations across tuple arities. Defines no
  construction trait of its own. Used by Bevy, Axum, Actix for variadic-style
  handler signatures.

### Why the abstraction is absent from std

The account (no variadic generics; From/TryFrom cover one input; Default covers zero)
is confirmed by sources.

The root blocker is the absence of variadic generics. A unified `trait Create<Args>`
where Args ranges over any argument count requires the language to be generic over
the number of type parameters — which Rust cannot do.

- Open issue since 2013: https://github.com/rust-lang/rust/issues/10124
- Multiple draft RFCs postponed: https://github.com/rust-lang/rfcs/issues/376
- Lang-team design notes confirm no singular best choice has emerged:
  https://github.com/rust-lang/lang-team/blob/master/src/design_notes/variadic_generics.md
- 2025 analysis of dead-end designs: https://poignardazur.github.io/2025/07/09/variadic-generics-dead-ends/

The std coverage as of 2026:
- `Default` — the 0-argument case.
- `From<T>` / `TryFrom<T>` — the exactly-1-argument case.
- Nothing for N arguments, and no unifying interface.

A URLO thread "Adding trait New to the standard library"
(https://users.rust-lang.org/t/adding-trait-new-to-the-standard-library/7430)
addressed only the 0-argument case and was dismissed because `Default` already exists.
The N-argument case was noted but not developed.

### How existing approaches fake it

**Arity-split traits** (`type_constructor` pattern): define `From_1<A>`, `From_2<A,B>`,
etc. as separate traits. Mechanically valid; no unifying bound available.

**Macro expansion over finite arities** (`impl-trait-for-tuples` pattern): a macro
generates trait implementations for each tuple arity up to N. A code-generation
workaround used in major frameworks. Not a semantic abstraction — the unified trait
must be named by the macro author, not by the stdlib or a shared crate.

**Tuple-argument encoding** — `impl Create<(A, B)> for T` — was found in no
published crate as a committed API convention. It is mechanically valid Rust; no one
has published a crate making it the primary interface.

**Builder pattern** — construction ergonomics solved via a generated builder struct.
No trait exposed; nothing a generic function can bound against.

The cleanest existing formulation is `type_constructor`'s arity-split family: it is
the only instance of published construction traits in Rust, but it does not unify
them and was not designed for the purpose.

### "Completed Rust" / missing-abstractions crates

No crate with the mission of supplying missing general (non-domain-specific) Rust
abstractions was found that includes a construction trait. The closest lane-adjacent
crates are:

- `frunk` — generic functional programming (HList, structural Generic). Different
  lane (type-level structural programming, not construction abstraction).
- `derive_more` — derive macros for common trait boilerplate. Does not introduce new
  traits; adds implementations of existing ones.
- `cc-traits` — collection operation traits. Domain-specific.

The "Create trait" lane is vacant as a primary mission.

## Interpretation

**Verdict: the concept is substantially vacant.**

No crate provides a general `trait Create<Args>` (or equivalent under any name) where
Args is a type parameter that a implementing type consumes to produce itself — a
declared capability that generic code can bound against. The design space has not been
claimed.

**Nearest misses, ranked:**

1. `type_constructor` — Actual construction traits, not just derive macros. But:
   arity-split not unified (no single `Create<Args>` bound), designed for an unrelated
   purpose (orphan-rule workaround), deprecated, max arity 3. Demonstrates the
   mechanism works; does not claim the design space.

2. `derive_more` Constructor — Widely used naming (`Constructor`) but explicitly not
   a trait. The vocabulary exists in the ecosystem without the abstraction.

3. Builder crates (`bon`, `derive_builder`, `typed-builder`) — Solve the practical
   construction ergonomics problem differently. No trait, no generic bound, no
   capability declaration. Orthogonal.

**Evaluation against trait doctrine:** The Create trait does not violate the
"fake trait" criterion (a trait whose method receives the capability's subject as a
parameter). For construction, the subject does not exist yet — the arguments are
consumed into the new instance. There is no pre-existing subject to pass. A method
`fn create(args: Args) -> Self` correctly takes the inputs and produces the type;
`self` is absent because it cannot be present. This passes the doctrine test.

**The tuple-argument encoding** (`impl Create<(A, B)> for T` to fake variadic generics)
is available in Rust today with no macro machinery. No published crate has made it a
primary API. If an own crate is authored, this is the cleanest available formulation
for the Args type parameter — a tuple whose elements are the construction inputs,
consumed by value.

Sources listed inline above.
