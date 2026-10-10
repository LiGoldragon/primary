# Rewrite: protos and datomic

## What was yanked

| Item | Why |
|---|---|
| `Enclosure::Guillemets` and all guillemet parsing/printing | Vision/protos.md: "The key-value map, and the guillemets that delimited it, are dropped entirely from protos and its dialects" |
| `Protoform::Qualified(Symbol, Vec<Protoform>)` variant | Merged into `Bare(Head)` to keep four variants per vision; Head::Qualified carries the qualified case |
| `Structural` trait | Renamed to `Protosizable`; protosize on Text is the delineation |
| `Printing` trait | Renamed to `Textualizable`; textualize goes to Text |
| `Corporal<C>` trait | Renamed to `Incorporable<C>`; incorporate goes to Corporate |
| `Conceptual<C>` trait | Renamed to `Conceivable<C>`; conceive goes to Concept |
| `Embodied` trait | Dropped; vision: "drop 'embodied' ... 'sized'"; `Sized` used directly |
| `Problem::EmptyInput` | Empty text yields an empty Delineation, not a fault |
| `Datom::Map(Vec<Pair>)` and `Pair` type | Vision/datom.md: "datom has no map" |
| `Expected::Map`, `Problem::Pairing`, `Problem::DuplicateKey` | Map-related fault variants, removed with the map |
| `BTreeMap<K,V>` Datomic impls | No map container in datom |
| `Fault::Corporal` variant name | Renamed to `Fault::Corporate` matching the layer name |
| `Datomic::datomize` method | Renamed to `Datomic::conceive` (Corporate to Concept, cannot fault) |
| `Textualizable` as a separate blanket trait in datomic | Became a default method on the `Datomic` trait; protos owns the `Textualizable` trait |
| Old ethos shapes (`Library.{0 15 0}`, `Library.{0 9 0}`) | Replaced with variant-headed, no version, imports first |
| `tests/situated.rs` in protos | Replaced by integrated situation tests in delineation.rs |

## New anatomy

### protos 0.17.0

| Module section | Layer or kind | What it holds |
|---|---|---|
| Types (layers) | Text | `Text = String`, `Integer = i64`, `Decimal = f64`, `Boolean = bool`, `Symbol = Text` |
| Types (layers) | Protoform | `Separator`, `Enclosure` (Braced, Bracketed, Angled), `Boundary` (CurlyQuotes, Parentheses), `Head` (Bare, Qualified), `Protoform` (Headed, Enclosed, Opaque, Bare), `Delineation` |
| Types (layers) | Situation | `Extent`, `Path`, `Situation` (BTreeMap), `Fault`, `Problem` |
| Types (universal) | Potential | `Potential<T, C = ()>`, `Situated<F>` |
| Kinds (traits) | to Text | `Textualizable { fn textualize(&self) -> Text }` |
| Kinds (traits) | to Protoform | `Protosizable { type Fault; fn protosize(&self) -> Result<Delineation, Self::Fault> }` |
| Kinds (traits) | to Concept | `Conceivable<C> { type Fault; fn conceive(&self) -> Result<C, Self::Fault> }` |
| Kinds (traits) | to Corporate | `Incorporable<T> { type Fault; fn incorporate(self) -> Result<T, Self::Fault> }` — concept bears it, consumes self by value |
| Kinds (traits) | chain | `Actualizable<T: Sized> { type Fault; fn actualize(&self) -> Result<T, Self::Fault> }` |
| Kinds (traits) | situation | `Pathed`, `Situating` |
| Impls | Textualizable | for Head, Protoform, Delineation |
| Impls | Protosizable | for Text (the delineator) |
| Impls | Actualizable | blanket for Potential<T, C> where C: Incorporable<T> (protosize, conceive, concept.incorporate()) |
| Impls | Situating | for Delineation |

### datomic 0.11.0

| Module section | Layer or kind | What it holds |
|---|---|---|
| Concept type | Datom | Variant, Struct, Vector, Text, Meaning, Bare (6 variants, no Map) |
| Meaning | Meaning | Plain(Text) today; full structured meaning is future |
| Faults | Expected | Variant, Struct, Vector, Text, Meaning, Integer, Decimal, Boolean, Bare (no Map) |
| Faults | Problem | Shape, Arity, UnknownVariant, Separator, Value, OneValue (no Pairing, DuplicateKey) |
| Faults | Fault | Structural, Conceptual, Corporate (renamed from Corporal) |
| Kinds | Datomic | `Sized + Conceivable<Datom, Fault = Infallible>`; where `Datom: Incorporable<Self, Fault = Fault>`; methods `incorporate_from` (dispatch), `textualize` (default) |
| Impls | Protosizable | for Datom (concept to delineation, Infallible) via private Protosizing trait |
| Impls | Conceivable<Datom> | for Protoform, Delineation (protoform to concept, may fault) |
| Impls | Incorporable<T> for Datom | for each concrete T; container impls use T: Datomic bound |
| Impls | Conceivable<Datom> | for each corporate type (ascent, Infallible) |
| Impls | Datomic | for Integer, Boolean, Decimal, Text, Meaning, Vec<T>, Option<T>, Result<T,E>, Datom, Expected, Problem, Fault, protos types, Situated<F> |
| Blanket | Incorporable<Box<T>> for Datom | where T: Datomic; no macro needed for incorporation |
| Macro | impl_datomic_box! | for Conceivable<Datom> + Datomic on Box<T> (orphan rule on Conceivable) |

## Decisions made on flow authority

| Decision | Rationale |
|---|---|
| Fault type keeps its name `Fault`; variant names are `Structural`, `Conceptual`, `Corporate` | Fault variant names match the four layers; `Corporate` replaces `Corporal` since the layer name is Corporate |
| Situation type remains `BTreeMap<Path, Extent>` in Rust | Efficient lookup by path; datom representation uses vector-of-structs (no map) but the Rust type is internal |
| Head qualifies as a symbol by being non-empty and containing no whitespace or delimiter | The vision says "the rule that qualifies a string as a symbol is not yet stated"; this rule is the minimum structural requirement from the delineator |
| Escape glyph inside parentheses is backslash | Carried forward from the current flow decision; `\)` `\(` `\\` |
| Tuple structs in the crates' own types: `Extent(pub Integer, pub Integer)`, `Situated<F>(pub Option<Extent>, pub F)` | Vision allows tuples at contact points; these are positional tuple structs consistent with ethos-declared types |
| Incorporable borne by the concept: `impl Incorporable<T> for Datom` | Vision: "incorporate (Incorporable), goes to Corporate, borne by Concept"; `fn incorporate(self) -> Result<T, Fault>` consumes the concept by value; by value because incorporating is a one-way descent that consumes the intermediate concept |
| Datomic kind's shape: `Sized + Conceivable<Datom, Fault = Infallible>` with where clause `Datom: Incorporable<Self, Fault = Fault>`; provides `incorporate_from` and `textualize` (default) | Vision: "Datom is a kind, not a type, since it has no definite shape; the kind is Datomic"; conceive from Conceivable supertrait (one capability, one trait); incorporate_from dispatches element incorporation in containers to avoid trait-solver overflow |
| `Datomic::incorporate_from` as dispatch method alongside `Incorporable<T>` | Witnessed: stable Rust's trait solver overflows when `Datom: Incorporable<T>` appears as a generic where clause alongside `impl<T> Incorporable<Vec<T>> for Datom where Datom: Incorporable<T>` (unbounded recursion through Vec wrapping). `T: Datomic` with `T::incorporate_from` breaks the cycle because the recursion goes through Datomic, not through Incorporable impls on Datom. The public `Incorporable<T> for Datom` delegates to `T::incorporate_from(self)` |
| Datomic where clause `Datom: Incorporable<Self>` not propagated on stable | Witnessed: `impl<T: Datomic> ... where Datom: Incorporable<T>` compiles, but the where clause on the Datomic trait definition is not automatically available to generic code bound by `T: Datomic`; the bound must be repeated where needed |
| Orphan rule for consumer crates | Witnessed: `impl Incorporable<Person> for Datom` compiles in tests/datomic.rs (a consumer-crate position) because Person is local and appears as the trait parameter T of a foreign trait, with the foreign Datom as Self; RFC 2451 allows this when a local type appears before all uncovered foreign type parameters |
| `impl<T: Datomic> Incorporable<Box<T>> for Datom` compiles as a blanket | Witnessed: the blanket Incorporable for Box<T> compiles without the macro; the macro is retained only for Conceivable<Datom> and Datomic on Box<T> (orphan rule prevents blanket Conceivable on a foreign wrapper type) |
| `Textualizable` as default method on Datomic, not a blanket `impl<T: Datomic> protos::Textualizable for T` | Witnessed: Rust's orphan rule blocks `impl<T: LocalTrait> ForeignTrait for T`; `protos::Textualizable` is foreign to datomic; the default method on Datomic achieves the same chaining (conceive, protosize, textualize) without orphan issues |
| Boolean values: `True`/`False` (capitalized bare words) | Carried forward; consistent with variant naming convention in datom |
| Bare-string rule: a string is bare-safe when it contains no whitespace, no delimiter, no leading/trailing separator, no consecutive separators, and round-trips through delineation+conception as an all-bare chain | Carried forward from previous flow; the structural rule that makes `name:first` and `2026-09-03T17:46:20` bare |
| `Protoform::Bare(Head)` replaces both old `Bare(Symbol)` and `Qualified(Symbol, Vec<Protoform>)` | Keeps four variants per vision; `Head::Bare` for simple bare words, `Head::Qualified` for standalone qualified forms like `Vector<Text>` |
| `Textualizable` trait defined in protos, `Datomic::textualize` as default method | Rust orphan rules prevent blanket `impl<T: Datomic> protos::Textualizable for T` in datomic; the default method on Datomic chains conceive, protosize, textualize |

## Commits and versions

| Crate | Old version | New version | Commit (main) |
|---|---|---|---|
| protos | 0.15.1 | 0.17.0 | `c5594f9d6f73f0e71e071c04b4cee8bb37ea2cf9` |
| datomic | 0.9.1 | 0.11.0 | `2c2e2073fd34aa4dd1a2b2d642c828ec8f651f45` |

datomic pins protos at `c5594f9d6f73`.

Intermediate commits (superseded by the above):
- protos 0.16.0 (`ba2d1cdaec29`): initial rewrite before Incorporable correction
- datomic 0.10.0 (`66e575323e12`): initial rewrite before Incorporable correction

## Test and build output

### protos

```
test result: ok. 38 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`cargo clippy --all-targets -- -D warnings`: clean, no warnings.
`nix build`: success (protos-0.17.0).

### datomic

```
test result: ok. 40 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`cargo clippy --all-targets -- -D warnings`: clean, no warnings.
`nix build`: success (datomic-0.11.0).
Flake code quality checks (no free functions, no inherent methods, no ZST behavior, no forbidden vocabulary): all pass.

## Left hanging

| Item | Why |
|---|---|
| Nix flake `checks` not fully exercised in this flow | `nix build` succeeded for both crates; full `nix flake check` runs all checks (test, clippy, fmt, doc, code quality) but was not run due to remote builder time; the individual cargo checks passed locally |
| Consumers not updated | Brief delegates consumer rewrites to later subflows; protos and datomic pin exact revisions so nothing breaks downstream until consumers are rewritten |
| Ethos self-description is approximate | The `.ethos` files declare the anatomy in the new variant-headed shape but cannot perfectly express Rust generics (Potential<T, C>, blanket impls); the ethos-zero rewrite reads these declarations |
| `Meaning` type is provisional | Vision: "Meaning is postponed so that a working syntax lands as soon as possible: today a parenthesized text lands as a plain String, with the later type marked in code" |
| Symbol qualification rule not formally stated | Vision: "the rule that qualifies a string as a symbol is not yet stated"; the delineator uses the structural minimum (non-empty, no whitespace, no delimiter) |

## Sources

- Vision/protos.md — distilled vision for protos (authority)
- Vision/datom.md — distilled vision for datom (authority)
- Vision/ethos.md — distilled vision for ethos (authority)
- Intent/mandatoryTraits.md — mandatory traits intent (authority)
- Intent/protosParsing.md — context-switching parse intent (authority)
- Intent/data.md — everything is data intent (authority)
- flows/995a164e/vision/rust.md — freestanding implementations forbidden
- flows/995a164e/vision/layerMatching.md — data in capabilities, no constants
- flows/995a164e/vision/kinds.md — naming, associated types/constants
- flows/995a164e/vision/concept.md — Concept layer, singular
- flows/995a164e/vision/contexts.md — parsing contexts
- flows/995a164e/vision/explodedForm.md — sweet/canonical form
- flows/62022e8f/vision/multiFormConcepts.md — multi-form concept
- flows/ba906ae2/vision/signalIsOurMessagingLayer.md — signal naming, sections
- flows/1a6ca4/vision/datom.md — rewrite directive: "anatomically and directly"
