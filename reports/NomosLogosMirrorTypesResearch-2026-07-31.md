# Nomos-to-Logos Mirror Types: Phase-Parameterized Design Research

Report date: 2026-07-31. Grade: research, [agent-inference] unless marked
otherwise. TENTATIVE — research material for psyche review, not doctrine.
Companion to `reports/PsycheVisionFirstPrinciples-2026-07-31.md` (section on
the nomos-to-logos problem statement).

## Problem Statement

[psyche-ruled] The Nomos-side type differs from its Logos counterpart BECAUSE
positions can hold escapes (Realize/Splice/Invoke) where Logos holds concrete
data. It is NOT distinct in essence beyond that: a phase distinction, not two
unrelated type families.

A Logos type such as `Enumeration` is a positional struct:

```rust
pub struct Enumeration {
    pub visibility: Visibility,
    pub attributes: Vec<Attribute>,
    pub name: Identifier,
    pub generics: Generics,
    pub variants: Vec<Variant>,
}
```

Its Nomos counterpart (the legacy `EnumerationTemplate`) has identical shape,
but some positions admit escapes where Logos holds concrete data:

```rust
pub struct EnumerationTemplate {
    pub visibility: Visibility,           // fixed: always literal
    pub attributes: Sequence<Attribute>,  // widened: can hold Escape
    pub name: Scalar<Identifier>,         // widened: can hold Escape
    pub generics: Generics,               // fixed: always literal
    pub variants: Sequence<Variant>,      // widened: can hold Escape
}
```

The engine already deleted the 878-line handwritten mirror universe and
replaced it with a declaration-indexed `TemplateValue<Root>` substrate in
`template_language.rs`. That substrate is fully generic:
`TemplateTerm<Root>` carries
`Declaration | Reference | Literal | Scalar | Nested | Sequence | Future` at
any position, validated against `TemplateLandingShape<Root>` computed from
structural-codec declarations. Three source-scan tests guard against
reintroduction of per-Logos-type Rust mirrors.

The question is now: does the system need to re-introduce Rust-typed mirror
types (as a phase-parameterized single definition rather than the deleted
hand-written pairs), or does the existing declaration-indexed generic
substrate already constitute the correct phase-split implementation? And if
typed mirrors are needed for a future layer (e.g., a richer type-safe API
surface, or direct pattern-matching on template bodies), which technique best
realizes them?

## Standing Laws (constraints on any solution)

- Tuples forbidden in Rust (single-field newtype exception)
- No string manipulation in the transformation
- All protos data is positional
- Identity is integer encodedID chains
- Everything must round-trip textualform <-> encodedform via
  nametree+structuretree
- rkyv for archival encoding
- No `syn`/`quote`/`prettyplease` (proc-macro tooling banned)
- No handwritten Rust twin per Logos type (enforced by source-scan tests)
- The escape algebra is closed: Realize, Splice, Invoke (plus
  RecursiveInvoke, InsertAt as internal forms)

## Existing Solution: The Declaration-Indexed TemplateValue Substrate

Before evaluating candidates, it is critical to recognize what already
exists. The codebase has already implemented a version of the phase split at
the structural-codec level rather than the Rust type level:

- `TemplateLandingShape<Root>` computes per-position whether a field is
  `Fixed` (always literal), `ValueOrFuture` (may hold escape), `Nested`
  (recursive), or `Sequence` (with item-level futures).
- `TemplateValue<Root>` is the runtime representation: a constructor ID plus
  a vector of `TemplateFieldValue<Root>`, each carrying a
  `TemplateTerm<Root>`.
- `TemplateTerm<Root>` is the phase-generic "slot content":
  `Declaration | Reference | Literal | Scalar | Nested | Sequence | Future`.
- Validation against the computed `TemplateLandingShape` ensures that
  `Future` terms only appear where the landing shape admits them.

This is, in effect, a **dynamically-typed trees-that-grow**: one runtime type
(`TemplateValue`) serves both phases, with the phase difference encoded in
the landing-shape declarations rather than in Rust's type system. The landing
shape acts as the "extension descriptor" that trees-that-grow encodes as
type families.

The candidates below should be evaluated as potential **static-typing
upgrades** to this existing dynamic approach, not as replacements for it.

## Option 1: Trees That Grow (Phase Trait with Per-Position Associated Types)

### Technique

Define a `Phase` trait with one associated type per escapable position. The
Logos phase sets each to `!` (never) or `()` (unit); the Nomos phase sets
each to the appropriate escape form.

```rust
trait Phase {
    type NameEscape;
    type AttributesEscape;
    type VariantsEscape;
    // ... one per escapable position across ALL Logos types
}

struct LogosPhase;
impl Phase for LogosPhase {
    type NameEscape = core::convert::Infallible;
    type AttributesEscape = core::convert::Infallible;
    type VariantsEscape = core::convert::Infallible;
}

struct NomosPhase;
impl Phase for NomosPhase {
    type NameEscape = TemplateFuture;
    type AttributesEscape = TemplateFuture;
    type VariantsEscape = TemplateFuture;
}

// The single definition:
struct Enumeration<P: Phase> {
    pub visibility: Visibility,                    // never escaped
    pub attributes: Vec<Either<Attribute, P::AttributesEscape>>,
    pub name: Either<Identifier, P::NameEscape>,
    pub generics: Generics,                        // never escaped
    pub variants: Vec<Either<Variant, P::VariantsEscape>>,
}
```

When `P = LogosPhase`, `Either<Identifier, Infallible>` is statically
guaranteed to be the `Left` (concrete) variant. The `Infallible` arm can
never be constructed.

### Evaluation Against Standing Laws

- **Shape sameness**: Satisfied structurally. `Enumeration<LogosPhase>` and
  `Enumeration<NomosPhase>` share a definition.
- **Position-typed escapes**: Satisfied. Each position has its own associated
  type — if needed, `NameEscape` and `VariantsEscape` can be different types,
  carrying different resolution semantics.
- **Positional encoding / round-trip**: Both `Enumeration<LogosPhase>` and
  `Enumeration<NomosPhase>` can derive rkyv. But they produce different
  archived types (different monomorphizations). The nametree/structuretree
  mechanism must handle the `Either` wrapper — for the Logos phase this is
  trivially `Left`-only, for Nomos it must encode the `Future` variant. This
  means the textual/encoded forms of the two phases are NOT identical, which
  is correct (a template body with escapes does not have the same encoding as
  a concrete Logos value).
- **Tuples forbidden**: No tuples used. `Either` is a two-variant enum, not a
  tuple.
- **No string manipulation**: Satisfied.
- **~38 mirrored scope enums**: Solved if scope enums are also parameterized
  by `Phase`. One definition, two instantiations.

### Problems

- **Verbosity**: For N Logos types with M total escapable positions, the
  `Phase` trait needs M associated types. The existing Logos corpus has ~9
  item kinds with ~5 escapable positions each = ~45 associated types. This is
  unwieldy.
- **Proc-macro ban**: Automating the `Phase` trait generation would naturally
  use proc macros, which are banned (`syn`/`quote`/`prettyplease` all
  forbidden).
- **`Either` wrapper**: The `Either<X, Infallible>` pattern means
  pattern-matching Logos values requires matching through the wrapper, even
  though the `Infallible` arm is dead. This is ergonomically annoying.
  Alternatively, a dedicated `Slot<X, E>` enum with a `value()` method that
  unwraps `Infallible` could help, but the dead arm still exists in the type.
- **Existing source-scan guards**: The source-scan tests that guard against
  handwritten twins may need updating to distinguish "phase-parameterized
  single definition" from "handwritten mirror."

### Prior Art

Najd & Peyton Jones, "Trees that Grow" (2017),
https://arxiv.org/abs/1610.04799. The Haskell version uses open type
families; in Rust the closest analog is associated types on a sealed trait.
GHC adopted this for its own AST starting in GHC 8.6.

## Option 2: Per-Position Wrapping with Escapable<X>

### Technique

```rust
enum Escapable<X> {
    Concrete(X),
    Escape(TemplateFuture),
}

// Nomos type:
struct EnumerationTemplate {
    pub visibility: Visibility,
    pub attributes: Vec<Escapable<Attribute>>,
    pub name: Escapable<Identifier>,
    pub generics: Generics,
    pub variants: Vec<Escapable<Variant>>,
}
```

The Logos type remains unwrapped; the Nomos type wraps each escapable field.

### Evaluation Against Standing Laws

- **Shape sameness**: [psyche-ruled tension] The psyche stated the Nomos type
  "has the same shape" as the Logos type. `Escapable<Identifier>` does NOT
  have the same shape as `Identifier` — it is a sum type. However, this IS
  the pattern already used in the legacy `template.rs` (where
  `Scalar<Identifier>` plays the same role as `Escapable<Identifier>`), and
  the psyche's own statement that positions "can hold escapes" implies the
  widening.
- **Position-typed escapes**: Partially satisfied. `Escapable<X>` carries `X`
  as a type parameter, so the escape is "in a position that expects X." But
  the escape payload (`TemplateFuture`) is the same type regardless of
  position — the position typing comes from the surrounding context, not from
  the escape value itself. If different positions need different escape
  resolution logic, that logic must be dispatched externally.
- **Positional encoding / round-trip**: `Escapable<X>` can derive rkyv and
  NOTA encoding. The Logos type does not use `Escapable`, so the two
  encodings differ (correct).
- **~38 mirrored scope enums**: NOT solved. Each Logos type still needs a
  manually written Nomos counterpart. This is exactly the problem that was
  already solved-and-deleted.

### Problems

- **Reintroduces handwritten mirrors**: Defining `EnumerationTemplate` as a
  separate struct with `Escapable` fields is what the source-scan tests
  explicitly guard against.
- **Not a single definition**: Two type families, not one — contradicts
  [psyche-ruled] phase-distinction framing.
- **Status**: Fallback only. Useful as an implementation detail WITHIN a
  phase-parameterized scheme (the `Either<X, E>` from Option 1 is essentially
  `Escapable` with a phase-dependent escape type), but not a standalone
  solution.

## Option 3: rkyv Archived<T> Precedent (Derive-Generated Mirror)

### Technique

rkyv's `#[derive(Archive)]` generates a parallel type `ArchivedT` from each
`T`. The relationship:

```rust
// rkyv's Archive trait:
pub trait Archive {
    type Archived: Portable;  // the mirror type
    type Resolver;
    fn resolve(&self, resolver: Self::Resolver, out: Place<Self::Archived>);
}
```

For `struct Foo { x: String, y: Vec<u32> }`, rkyv generates:

```rust
struct ArchivedFoo {
    x: <String as Archive>::Archived,   // ArchivedString
    y: <Vec<u32> as Archive>::Archived, // ArchivedVec<u32>
}
```

The mirror has identical positional structure but different leaf types,
mapped through an associated type on each leaf type.

### Applicability as Prior Art

An analogous `HasNomosForm` trait:

```rust
trait HasNomosForm {
    type NomosForm;
    fn instantiate(nomos: Self::NomosForm, ctx: &EvalContext) -> Self;
}

// Leaf implementations:
impl HasNomosForm for Identifier {
    type NomosForm = Either<Identifier, TemplateFuture>;
    fn instantiate(n: Self::NomosForm, ctx: &EvalContext) -> Self {
        match n {
            Either::Left(id) => id,
            Either::Right(future) => ctx.resolve_identifier(future),
        }
    }
}

// A derive on Logos types would generate:
// struct EnumerationNomosForm {
//     visibility: <Visibility as HasNomosForm>::NomosForm,
//     attributes: <Vec<Attribute> as HasNomosForm>::NomosForm,
//     ...
// }
```

### Evaluation Against Standing Laws

- **Shape sameness**: Satisfied by construction — the derive copies
  structure, maps leaf types.
- **Position-typed escapes**: Satisfied via `HasNomosForm` impls on leaf
  types — each leaf type determines its own escape form.
- **Positional encoding / round-trip**: The generated mirror type can derive
  its own rkyv/NOTA encoding. The derive must generate this too.
- **~38 mirrored scope enums**: Solved — one derive per Logos type, no
  handwritten mirrors.
- **Proc-macro ban**: BLOCKED. This requires `syn`/`quote` for the derive
  macro, which are banned. rkyv itself uses them, but rkyv is an external
  dependency, not authored code. Writing a new derive macro in the protos
  codebase would violate the standing law.

### Problems

- **Proc-macro ban is fatal**: Without `syn`/`quote`, this approach cannot be
  implemented in the protos codebase. It remains relevant only as a design
  pattern (the trait structure could be used with manual impls or
  build-script generation).
- **Two types, not one**: Even though generated, the mirror is a separate
  Rust type — it does not satisfy the "single definition, two phases" ideal
  as cleanly as Option 1.

## Option 4: GAT SlotMapper (Uniform Phase Mapping)

### Technique

Use generic associated types (GATs, stable since Rust 1.65) to map ALL
positions uniformly through a single type-level function:

```rust
trait SlotMapper {
    type Map<T>;
}

struct Identity;
impl SlotMapper for Identity {
    type Map<T> = T;
}

struct Escapify;
impl SlotMapper for Escapify {
    type Map<T> = Either<T, TemplateFuture>;
}

struct Enumeration<M: SlotMapper> {
    pub visibility: M::Map<Visibility>,
    pub attributes: M::Map<Vec<Attribute>>,
    pub name: M::Map<Identifier>,
    pub generics: M::Map<Generics>,
    pub variants: M::Map<Vec<Variant>>,
}
```

`Enumeration<Identity>` is the Logos form (all fields unwrapped);
`Enumeration<Escapify>` is the Nomos form (all fields wrapped in `Either`).

### Evaluation Against Standing Laws

- **Shape sameness**: Perfectly satisfied. One definition, literally shared.
- **Position-typed escapes**: NOT satisfied in the uniform version. All
  positions get the same `Either<T, TemplateFuture>` wrapping. But the
  existing codebase shows that some positions are `Fixed` (never escapable)
  while others are `ValueOrFuture`. Under uniform `Escapify`, `visibility`
  and `generics` would be wrapped even though they should be fixed. This is
  incorrect.
- **Positional encoding / round-trip**: For Logos (`Identity`),
  `M::Map<T> = T`, so encoding is normal. For Nomos (`Escapify`), every field
  is `Either<T, TemplateFuture>`, which needs its own encoding. But the
  "fixed" fields (visibility, generics) would encode as
  `Either<Visibility, TemplateFuture>` even though they should just be
  `Visibility` — wasted space and incorrect semantics.
- **~38 mirrored scope enums**: Solved if all positions are truly uniform.
  But they are not.

### Problems

- **Heterogeneous escapability**: The existing `TemplateLandingShape`
  distinguishes `Fixed`, `ValueOrFuture`, `Nested`, and `Sequence` per
  position. A uniform mapper cannot express this. Fields that should be
  `Fixed` get unnecessarily wrapped.
- **rkyv derivation**: `Enumeration<M: SlotMapper>` cannot derive rkyv
  because `M::Map<T>` is an opaque associated type — rkyv needs concrete
  types. The derives would have to be on the monomorphized forms, which
  requires specialization or manual impls.
- **Status**: Elegant but too uniform. Could work as a building block if
  combined with per-position overrides (which collapses it back into
  Option 1).

## Option 5: Sealed Trait with Per-Position Associated Types (Refined Trees-That-Grow)

### Technique

This is Option 1 refined to avoid the verbosity problem. Instead of one flat
`Phase` trait with 45 associated types, use a **hierarchical approach**: one
`Phase` trait per Logos type, sealed by the module.

```rust
mod enumeration {
    pub(crate) mod sealed { pub trait Phase {} }

    pub trait EnumerationPhase: sealed::Phase {
        type NameSlot;
        type AttributesSlot;
        type VariantsSlot;
    }

    pub struct Logos;
    impl sealed::Phase for Logos {}
    impl EnumerationPhase for Logos {
        type NameSlot = Identifier;
        type AttributesSlot = Vec<Attribute>;
        type VariantsSlot = Vec<Variant>;
    }

    pub struct Nomos;
    impl sealed::Phase for Nomos {}
    impl EnumerationPhase for Nomos {
        type NameSlot = Either<Identifier, TemplateFuture>;
        type AttributesSlot = Vec<Either<Attribute, TemplateFuture>>;
        type VariantsSlot = Vec<Either<Variant, TemplateFuture>>;
    }

    pub struct Enumeration<P: EnumerationPhase> {
        pub visibility: Visibility,         // always concrete
        pub attributes: P::AttributesSlot,
        pub name: P::NameSlot,
        pub generics: Generics,             // always concrete
        pub variants: P::VariantsSlot,
    }
}
```

### Evaluation Against Standing Laws

- **Shape sameness**: Satisfied. One definition.
- **Position-typed escapes**: Fully satisfied. Each position has its own
  associated type. Fixed positions (`visibility`, `generics`) are not
  parameterized at all.
- **Positional encoding / round-trip**: `Enumeration<Logos>` and
  `Enumeration<Nomos>` are different monomorphizations. Each can have its own
  rkyv derives if the associated types are concrete. But rkyv derive on a
  generic struct with associated-type fields is not straightforward — rkyv
  needs to know the concrete types at derive time. Manual `Archive` impls or
  monomorphized type aliases (`type LogosEnumeration = Enumeration<Logos>;`)
  with derives on those may be needed.
- **~38 mirrored scope enums**: Each scope enum gets its own `Phase` trait,
  but the definition is shared. The `From` impls and `contains_scope` methods
  can be generic over the phase.
- **Tuples forbidden**: No tuples. `Either` is an enum.

### Problems

- **Boilerplate**: Each Logos type needs its own `Phase` trait with
  associated types for each escapable position. For 9 item kinds with ~3-5
  escapable positions each, this is ~35 trait associated types total, spread
  across ~9 traits. Better than one flat trait with 45, but still
  substantial.
- **rkyv derivation on generic structs**: As noted, `#[derive(Archive)]` on
  `Enumeration<P: EnumerationPhase>` may not work directly. The workaround is
  to define concrete type aliases and derive on those, but this partially
  defeats the "single definition" benefit.
- **Proc-macro ban**: Automating the `Phase` trait generation would help but
  is banned.

## Option 6: The Existing TemplateValue Substrate (Status Quo Enhancement)

### Technique

The codebase already has `TemplateValue<Root>` — a fully generic,
declaration-indexed representation that serves both phases. Rather than
introducing Rust-typed phase parameterization, enhance this substrate:

- `TemplateValue<Root>` already distinguishes `Fixed` vs `ValueOrFuture` vs
  `Nested` vs `Sequence` per position via `TemplateLandingShape`.
- The `TemplateTerm<Root>` enum already carries both concrete values
  (`Declaration`, `Reference`, `Literal`, `Scalar`) and escapes (`Future`).
- Validation against `TemplateLandingShape` already enforces that `Future`
  terms only appear where the landing shape admits them.

Enhancement path: strengthen the existing validation and evaluation layer
rather than adding a Rust type-level phase split.

### Evaluation Against Standing Laws

- **Shape sameness**: Satisfied at the structural level — one `TemplateValue`
  type, one `TemplateTerm` enum, one `TemplateLandingShape` descriptor. The
  "shape" is the structural-codec grammar, not Rust types.
- **Position-typed escapes**: Satisfied via `TemplateLandingShape`, which
  computes per-position what escapes are admitted. The position typing is
  dynamic (checked at validation time) rather than static (checked at
  compile time).
- **Positional encoding / round-trip**: Already implemented.
  `TemplateValue<Root>` derives rkyv. The structural-codec drives
  textual/encoded form for both concrete Logos values and template values.
- **~38 mirrored scope enums**: Already solved — no Rust mirror types exist.
- **Tuples forbidden**: Satisfied.
- **Proc-macro ban**: No macros needed.

### Problems

- **No compile-time phase safety**: The Rust compiler cannot distinguish
  "this TemplateValue is fully concrete" from "this TemplateValue contains
  futures." A `TemplateValue` that should be a Logos value (all concrete)
  could accidentally contain a `Future` term — the error surfaces at
  validation time, not compile time.
- **Pattern-matching ergonomics**: Working with `TemplateValue` requires
  matching on `TemplateTerm` variants and consulting the
  `TemplateLandingShape`. Working with a typed `Enumeration<Logos>` would
  allow direct field access (`e.name` is an `Identifier`, not a
  `TemplateTerm` that might be a `Literal` or `Future`).
- **The psyche's framing**: The psyche described the problem as "one of those
  things [generates] the other" — implying a transformation from a typed
  Nomos value to a typed Logos value. The current substrate transforms from
  `TemplateValue` to `TemplateValue` (or to encoded Logos values via the
  evaluator), which is type-correct but may not match the psyche's mental
  model of typed-template-to-typed-output.

## Interaction with the ~38 Mirrored Scope Enums

The scope-enum problem (from `ScopeOfDomainStudy-2026-07-31.md`) is a
concrete instance of the mirror-type problem at the domain level: 38 scope
enums mirroring 38 domain enums, differing only by an injected `All` variant
at non-root levels. This is NOT the Nomos/Logos phase split — it is a
separate Scope/Domain split — but the same structural pattern applies.

Options 1 and 5 (phase-parameterized definitions) would solve the scope-enum
problem if the `All` variant is modeled as an extension constructor (the
"XExp" of trees-that-grow). Option 6 (the existing substrate) already solved
it at the domain level via `ScopeOf` derivation.

The design question is whether both mirror problems (Nomos/Logos phase and
Scope/Domain phase) should use the same mechanism. If yes, a generic
"phase-parameterized type" framework would serve both. If no, each can use
its domain-specific solution.

## Identity Question

Does the Nomos-phase type share the encodedID vocabulary of the Logos-phase
type, or does it have its own?

[agent-inference] Based on the codebase evidence: `TemplateValue<Root>` uses
the same `EncodedConstructorId<Root>` and `EncodedTypeId<Root>` vocabulary as
Logos values. The constructor ID and structural positions are shared; only
the field values differ (a `TemplateTerm::Future` vs a
`TemplateTerm::Literal`). This means the two phases share structural
identity — they disagree on content, not on what kind of thing they are. This
is consistent with [psyche-ruled] "not distinct in essence."

## Ranked Recommendation

**Rank 1 (recommended): Option 6 — Enhance the existing TemplateValue
substrate.** [agent-inference]

PROVENANCE CAVEAT (added after psyche review, 2026-07-31): the psyche
reiterated "I already made it clear the previous slices were misguided, so we
should doubt any and all parts" — this includes the TemplateValue substrate
itself. Its mechanism may be sound, but "already implemented and tested" is
not evidence of design correctness; the substrate must be re-derived from the
vision before this ranking is acted on. Additionally, the psyche questioned
the Fixed position category ("could we possibly want to support an evaluation
to resolve visibility?") — if every position is escapable (proposed ruling,
unconfirmed), the Fixed/ValueOrFuture distinction collapses, the
"heterogeneous escapability" objection to Option 4 (uniform GAT mapping)
evaporates, and every option above simplifies.

Rationale: The codebase has already solved this problem at the
structural-codec level. The `TemplateValue<Root>` + `TemplateLandingShape<Root>`
mechanism IS the phase-parameterized single definition — it just lives in the
declaration/codec layer rather than the Rust type layer. It already satisfies
every standing law, is already tested, and already handles the position-typed
escape distinction. The 878-line handwritten universe was deleted for good
reason, and source-scan tests guard against its return.

The cost of this approach is that the phase distinction is dynamic rather
than static. A `TemplateValue` that should be fully concrete is not
distinguished from one containing futures at the Rust type level. But the
validation layer already catches this, and the Rust type system cannot easily
express "this generic tree contains no `Future` terms in any position"
without dependent types or very heavy encoding.

**Rank 2: Option 5 — Per-type sealed Phase traits.** [agent-inference]

If the psyche determines that compile-time phase safety is essential (e.g.,
"I want the Rust compiler to refuse to emit a Logos value that still contains
an unresolved escape"), this is the cleanest Rust-native approach. It
requires substantial boilerplate (one trait per Logos type, one associated
type per escapable position), cannot be automated by proc macros under the
standing ban, and has rkyv derivation challenges. But it provides true
compile-time phase separation with one definition per type.

**Rank 3: Option 1 — Flat Phase trait.** [agent-inference]

Simpler than Option 5 but less scalable. Appropriate if the Logos type count
stays small and stable.

**Rank 4: Option 4 — GAT SlotMapper.** [agent-inference]

Elegant but too uniform for the heterogeneous escapability the codebase
requires. Could work if ALL positions were escapable, but the existing
`Fixed` vs `ValueOrFuture` distinction makes this insufficient.

**Rank 5 (fallback): Option 3 — rkyv-style derive mirror.** [agent-inference]

Blocked by the proc-macro ban. Remains relevant as a design pattern if the
ban is ever relaxed.

**Rank 6 (fallback): Option 2 — Separate Escapable<X> mirror types.**
[agent-inference]

Reintroduces handwritten mirrors, contradicts [psyche-ruled] single-family
framing, and is explicitly guarded against by source-scan tests.

## The Single Question Whose Answer Most Changes the Ranking

**Does the psyche require compile-time (Rust type-level) phase separation, or
is the existing declaration-time (structural-codec validation) phase
separation sufficient?**

If compile-time: Option 5 rises to Rank 1, and the substantial boilerplate
cost is accepted as the price of static safety under the proc-macro ban.

If declaration-time is sufficient: Option 6 (status quo enhancement) is
already implemented and should be deepened rather than replaced.

The psyche's statement — "the transformation is going to have to take one of
those things and generate the other" — could mean either "take a
`TemplateValue` and evaluate it into Logos encoded form" (which is what the
existing evaluator does) or "take a typed `Enumeration<Nomos>` and produce a
typed `Enumeration<Logos>`" (which would require Rust-typed phase
parameterization). The answer to this question determines the ranking.

## Citations

- Najd, S. & Peyton Jones, S. (2017). "Trees that Grow." Journal of
  Universal Computer Science, 23(1). https://arxiv.org/abs/1610.04799
- rkyv Archive trait documentation:
  https://docs.rs/rkyv/latest/rkyv/trait.Archive.html
- rkyv derive macro features: https://rkyv.org/derive-macro-features.html
- GATs stabilization (Rust 1.65):
  https://blog.rust-lang.org/2022/10/28/gats-stabilization/
- Existing codebase: `core-nomos/src/template_language.rs` (TemplateValue,
  TemplateLandingShape, TemplateTerm), `core-nomos/src/template.rs` (legacy
  Scalar/Sequence mirror types), `core-nomos/src/authored.rs` ("no Logos type
  has an authored Rust twin"), `core-logos/src/enumeration.rs` (concrete
  Enumeration)
