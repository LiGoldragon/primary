# 654 — Generics & traits as data: what generates, what's still hand-wired, and the honest next slice

The psyche asked: *"review the improved nota/schema syntax and how it can represent the
generics/traits we wanted it to represent so it could generate the code we actually need
for the components, and avoid hand-wiring all of it with newtypes."* This is the review.

**Spirit gate.** Exploratory framing ("let's review … how it can represent"), so the
outcome is **Observe + flag candidate intent**, not Record. The durable arrow about
generating-not-hand-wiring is already recorded — [EVERYTHING is a serializable data
object, the MACRO most of all … the ONLY code is one tiny generic interpreter over data]
(`4itr`, Maximum), [a programming language is a set of structural macros — with Rust's
struct, enum, fn, impl, and generics included] (`7c71`, VeryHigh), [push as much of the
compiler definition into data as possible] (`vpbx`). What is **not** recorded is
traits-as-data; that gap, plus three others, is surfaced as candidate intent at the end
for the psyche to settle. Method: a survey workflow (5 readers across nota-next /
schema-next / schema-cc / spirit-triad), a 3-lens design panel, and one adversarial
critique. Sub-reports of this session live alongside in the meta-directory note; this is
the synthesis.

## The headline (and the crux from chat, answered)

The crux I flagged in chat — *does a generic declaration emit a generic Rust type, or
only monomorphized instantiations?* — has a clean answer: **it emits true generic Rust.**
A parameterized declaration `(Work Event WriteDone ReadDone EffectDone) [...]` emits
`pub enum Work<Event, WriteDone, ReadDone, EffectDone> { ... }`; an application `(Foo A B)`
emits the type-use `Foo<A, B>`; an applied root `(Work SignalInput ...)` emits
`pub type Input = Work<SignalInput, ...>;` — all arity-checked at lowering
(schema-rust-next `lib.rs:3852-3866, 4080-4089`; schema-next `schema.rs:526-630`). No
source-level monomorphization happens; the binder→argument substitution exists only as a
**test-side** equivalence proof (`tests/reaction.rs` `FrameExpansion`), not a compiler
pass. So generics-of-*types* is real and landed.

**The actual gap is one level up: generic *impls* and *traits* do not generate.** Two
precise facts carry the whole review:

1. For any parameterized declaration the emitter **suppresses** the inherent
   constructors, `From` impls, and accessors it normally emits — because it cannot
   synthesize an `impl<P..> Type<P..>` header (schema-rust-next `lib.rs:5099-5106,
   5149-5156`). Those conversions are then hand-written in the runtime crate.
2. There is **no schema node for a trait or an impl at all.** `TypeDeclaration` is the
   closed sum `Struct | Enum | Newtype` (`schema.rs:892-896`). Every trait and impl in
   the stack comes from one of three hand-authored sources, never from declared data
   (table below).

So "generate the code we need and stop hand-wiring newtypes" is really **two** capability
asks — *generic impl emission* and *trait/impl-as-data* — neither of which exists yet,
sitting on top of a generics-of-types layer that is already done.

## Layer map — what is data, what is hand-wired

```
                         ROUND-TRIPS THROUGH NOTA TEXT + RKYV (4itr)
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ TIER 3  schema-next / schema-rust-next  — the compiler (increasingly emitted)  │
  │   • Type declarations  Struct | Enum | Newtype ............... DATA ✓ (emitted) │
  │   • Generic decls (Work<…>) + applications (Foo A B) ......... DATA ✓ (emitted) │
  │   • Reference dispatch precedence (resolve_parenthesis_…) .... DATA ✓ (via cc)  │
  │   • Generic IMPL headers  impl<P..> Type<P..> where P: B ..... HAND-WIRED ✗     │
  │   • Trait declarations  pub trait NexusEngine: Send {…} ...... HAND-WIRED ✗     │
  │   • Trait impls (markers, blanket, Deref) ................... HAND-WIRED ✗     │
  ├──────────────────────────────────────────────────────────────────────────────┤
  │ TIER 2  schema-cc  — the compiler definition as typed data                     │
  │   • ReferenceGrammar  (Builtin Vector 1 … DeclaredMacro Application) . DATA ✓   │
  │   • emits ONE method (resolve_parenthesis_reference) via quote! ...... 1 impl   │
  │   • BuiltinHead / BuiltinArity / ArgumentCount  StructuralMacroNode .. HAND-WIRED ✗
  ├──────────────────────────────────────────────────────────────────────────────┤
  │ TIER 1  nota-next  — the seed (irreducible hand-written floor)                  │
  │   • NOTA block parser (text → Document → Block) .............. HAND-WIRED (seed)│
  │   • #[derive(StructuralMacroNode)] over a 7-shape vocabulary . HAND-WIRED (seed)│
  │     emits NotaDecode/NotaEncode IMPLS from a #[shape] annotation ← the existing │
  │     "trait-impl-from-data" mechanism, just not named or generalized            │
  └──────────────────────────────────────────────────────────────────────────────┘
```

The irony the psyche pointed at lives at Tier 2: **the compiler-of-the-compiler is itself
partly hand-wired with newtypes.** `BuiltinHead` (a PascalCase-atom newtype) and
`BuiltinArity` (`Atom`-keyword-or-bare-integer) carry hand-written `StructuralMacroNode`
impls — ~112 lines — because the derive's 7-shape vocabulary has no *leaf* shape
(bare-atom, symbol, keyword-or-integer) and supports enums only, not newtype structs
(schema-cc `grammar.rs:64-157, 207-268`; the code comments say so at `grammar.rs:204-206`).

## Current generic forms (all landed, all emitting)

| NOTA form | Position | Emits |
|---|---|---|
| `(Foo Alpha Beta)` | reference / field | `Foo<Alpha, Beta>` type-use |
| `(Work E W R Eff) [(SignalArrived E) …]` | declaration head | `pub enum Work<E, W, R, Eff> { … }` (true generic) |
| `(Vector T)` `(Optional T)` `(Map K V)` `(ScopeOf T)` `(Bytes N)` | reference | `Vec<T>` `Option<T>` `BTreeMap<K,V>` `…Scope` `FixedBytes<N>` (built-ins win dispatch) |
| `(Work SignalInput SemaWriteOutput …)` | component root | `pub type Input = Work<SignalInput, …>;` (applied alias) |
| `(ReferenceGrammar (Builtin Vector 1) … Application)` | schema-cc grammar | `impl TypeReference { fn resolve_parenthesis_reference }` |

What generics **cannot** express today: bounds / where-clauses (a binder is just a `Name`),
trait declarations, trait impls, generic functions, higher-kinded params, associated-type
projection. The first of these — **bounds** — is the load-bearing absence: it is *the
reason* the parameterized-decl impls are suppressed.

## Where every trait and impl actually comes from

| Source | Mechanism | Examples | Data-driven? |
|---|---|---|---|
| proc-macro derive | `#[derive]` reads a Rust AST + `#[shape]` attrs at macro time | `NotaDecode`/`NotaEncode`, `StructuralMacroNode`, rkyv | shape annotation only; trait set fixed |
| `quote!` template in schema-rust-next | fixed text keyed off the hand-written `Plane` enum | `pub trait NexusEngine: Send`, `impl<C,P> AcceptPrevious<P> for C where C: UpgradeFrom<P>`, marker impls | **no** — `Plane`-keyed |
| hand-written in daemon | per-noun by hand on generated types (`5hjv` pattern) | 12× `impl Deref` (body `self.payload()`), `plane.rs` cross-plane `From` bridges | **no** |

The encouraging part: the emitter **already renders every Rust shape the ask needs** —
`pub trait T: Super`, `impl<C,P> Trait<P> for C where …`, `enum Work<…>` with threaded
generics. The gap looked purely representational. **It is not** — see the overclaim catch.

## The overclaim catch (the operator-384 lesson, applied to ourselves)

All three design lenses reached for the same headline: *"the emitter already threads
`impl<P..> Type<P..>` headers, so traits/generic-impls are a representational change, not a
new capability."* The adversarial lens **verified that false** — and it is the exact shape
of the precedence-as-data overclaim the operator caught in `384`:

- `RustGenericParameterTokens` (`lib.rs:4043-4064`) renders **only** `<a, b>` from a
  `&[Name]` — no bounds, no where-clause.
- `EnumPayloadFromImplTokens` (`lib.rs:4657`) emits `impl From<P> for Enum` with **zero**
  generics and does not even hold the parameter list; variant-constructor tokens emit a
  bare `impl Enum`.
- The **only** `impl<C,P> Trait<P> for C where …` anywhere in the emitter is the **verbatim
  hand-typed** `AcceptPrevious` string (`lib.rs:6448-6450`) and the `NexusEngine` template
  — neither is reusable header-threading machinery.

So emitting generic impls is **genuinely new codegen** (new parameter+bound fields and
where-clause rendering on every relevant token struct, plus bounds round-tripping through
the closure-walk binder resolution and arity check), **not** feeding existing tokens from
data. Recording this as a guardrail is candidate intent below, so no future design
re-makes the claim.

A second, quieter overclaim also caught: "replace the marker-impl branch with declared
`(Impl …)` values, byte-identical, delete the branch" is not free — the role→trait binding
is not a constant push-list, it is **structural inference** (`nexus_runner_shape`,
`lib.rs:6366` reads `NexusWork`/`NexusAction` variant *names* to decide which type is
sema-write-input, etc.). Deleting the branch relocates that inference to the schema author
or a new pass; it does not vanish.

## Hand-wiring inventory, ranked by the capability that removes it

| Capability (in dependency order) | Status | Removes | Honest cost |
|---|---|---|---|
| **A. Single-payload `Deref` directive** `(Newtype Record Entry (derives Deref))` | not built | 12× hand `impl Deref` (`spirit/engine.rs:767-861`) | low — fixed body (`self.payload()`), no generics, no bounds, rides the newtype decl |
| **B. `ImplDeclaration` schema section + marker impls** `(Impl SemaWriteInput WriteInput)` | not built | `RuntimeRoleTraitImpl` hardcoded `&'static str` paths + push-lists (`lib.rs:4758-4808, 5904-5973`) | medium — needs the role→trait binding made explicit (it is inferred today), not just relocated |
| **C. Generic impl-header threading** `impl<P..> Type<P..> where P: B` + bound vocabulary `(Param Event [NotaDecode])` | not built (**NEW codegen**) | the suppressed parameterized-decl `From`/constructor/accessor impls (`lib.rs:5099-5106, 5149-5156`) | high — new fields + where rendering on 3+ token structs; bounds through closure-walk + arity |
| **D. Leaf shapes in the derive vocabulary** (atom-leaf, symbol, keyword-or-integer) + struct-newtype structural derive | not built | schema-cc `BuiltinHead`/`BuiltinArity`/`ArgumentCount` hand impls; schema-next `Name` hand impl | medium — extends the seed proc-macro's shape sum |
| **E. Frame application emit** (expand `(Work …)` root into the concrete enum, or emit the alias + collapse per-plane dupes) | proven in test, not emitted | per-plane re-declaration of the Work/Action skeleton; `plane.rs` 8 cross-plane `From` bridges | medium — the equivalence is proven leg-for-leg; only the emitter wiring is missing |
| **F. Trait declarations as data** `(Trait NexusEngine [Send] [(Method …)])` | not built | `NexusEngineTraitTokens` template (`lib.rs:2508-2660`) | high — default method *bodies* are real Rust, not data; only signatures datify cleanly |
| **G. Shape vocabulary as data** (`t85k`) + EmissionTarget as data | aspirational | the 7-shape Rust match arms encoded ~6× in the derive; schema-cc's single-method ceiling | highest — large seed refactor; sequence last |

The genuine business logic — the Nexus decision plane, the store, the guardian, the
signal query matchers — **stays hand-written** on generated nouns. That is the deliberate
`5hjv` boundary, not debt.

## Recommended path (synthesis of the three lenses + critique)

1. **Capture the Spirit intent first** (gate before any code) — traits-as-data is
   genuinely unrecorded. (Candidate-intent list below; the psyche settles it.)
2. **First verifiable slice = capability A, the `Deref` directive — not marker impls.**
   The critique's correction: marker-impl replacement carries the hidden role-inference
   overclaim, so it is *not* the cleanest first proof. The `Deref` directive is: no
   generics, no bounds, no role inference, no new top-level section to populate yet — and
   its body is the single fixed payload-projection shape all three lenses already agree
   on. Verify by **regenerate-and-diff**: the 12 `Deref` impls appear from data, the hand
   blocks delete, everything else stays byte-stable (the same identity-hash discipline we
   used for the positional cascade and the schema-cc integration).
3. **Model the data shape right from day one:** an `ImplDeclaration` is a **top-level
   schema section** (a typed `Vec` sibling to relations / families / streams), *not* a
   variant of the `Declaration` struct (correcting a Lens-1 error: `Declaration` at
   `schema.rs:821` is a struct, and relations/families/streams are parallel `Vec` fields
   on `Schema`, `schema.rs:370-378`). Slice 1 populates it via the newtype attribute; the
   shape is then correct for slices B/C/F later.
4. **Grammar:** the impl form is a **positional, `for`-less** record
   `(Impl [params] TraitRef Target [where] [body])` — the hard-override [NOTA records are
   positional, no keywords inside] settles it against the `for`-keyword form.
5. **Defer with the overclaim corrected in the record:** capability C (generic-header
   threading) is flagged as *new codegen*, the real prerequisite behind "bounds";
   capability B waits on an explicit role→trait table or a computed pass; F/G are
   aspirational, gated on body/bound vocabularies that do not exist. **Never** model
   arbitrary Rust expression bodies — that rebuilds an expression compiler inside NOTA and
   violates `4itr`/`2zed`.

```
slice 1 (A): (Newtype Record Entry (derives Deref))  ──emit──▶  impl Deref for Record { … self.payload() }
              └ proves "trait-impl-from-data" with ZERO overclaimed machinery; diff-verified
slice 2 (D): leaf shapes in the derive  ──▶  delete schema-cc BuiltinHead/BuiltinArity hand impls
slice 3 (B): ImplDeclaration + marker impls  ──▶  needs explicit role→trait binding (not inference)
slice 4 (C): bound vocab + impl-header threading  ──▶  NEW codegen; unblocks suppressed parameterized-decl impls
slice 5 (E): frame-application emit  ──▶  collapse per-plane Work/Action dup + delete plane.rs From bridges
slice 6 (F/G): trait decls / shape-vocab-as-data  ──▶  aspirational; the meta-schema fixpoint
```

## Candidate intent for the psyche to settle

These passed the survey's gap-check (none is currently in Spirit) but the prompt was
exploratory, so they are **proposed, not recorded**:

1. **Decision** — Trait declarations and trait impls are representable as schema data; the
   build-time compiler emits the impl/trait Rust from those declared NOTA values, the same
   way `StructuralMacroNode` emits codec impls from a shape annotation. (Closes the live
   gap; turns `7c71`'s "impl … included" from aspiration into a recorded generation target.)
2. **Principle** — Generated impl method bodies are restricted to (a) marker/empty bodies
   and (b) a small fixed, named mechanical-body family (e.g. payload projection); arbitrary
   Rust expression bodies are **not** modeled as data, and genuine business logic stays
   hand-written on generated nouns. (Guards `4itr`/`2zed`; ratifies `5hjv` as a deliberate
   boundary.)
3. **Principle** — Emitting generic impl headers (`impl<P..> Type<P..> where P: Bound`) is
   **new codegen capability**, not a free consequence of generics-as-data; a
   parameter-bound vocabulary is its prerequisite, and the suppressed parameterized-decl
   impls remain suppressed until both land. (Names the precedence-style overclaim so future
   designs don't assume the threading exists.)
4. **Decision** — An impl is a top-level schema section (a typed `Vec` sibling to
   relations/families/streams), not a `Declaration` variant; the impl NOTA form is a
   positional record with no embedded keywords.

## Open questions (each restated for chat)

- **Record traits-as-data now, and as Decision or Principle?** (candidate #1)
- **How far do impl method bodies go as data** — marker + tiny fixed mechanical family
  (the 3-lens consensus), or zero mechanical family until a real body vocabulary exists?
- **Role→trait binding** — author it explicitly as data (a `(RoleMarker …)` table) or keep
  the emitter inferring it from variant names and move only the rendering to data?
- **Confirm the `for`-less positional impl grammar** as settled by the positional-record
  hard-override.
