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

### protos 0.16.0

| Module section | Layer or kind | What it holds |
|---|---|---|
| Types (layers) | Text | `Text = String`, `Integer = i64`, `Decimal = f64`, `Boolean = bool`, `Symbol = Text` |
| Types (layers) | Protoform | `Separator`, `Enclosure` (Braced, Bracketed, Angled), `Boundary` (CurlyQuotes, Parentheses), `Head` (Bare, Qualified), `Protoform` (Headed, Enclosed, Opaque, Bare), `Delineation` |
| Types (layers) | Situation | `Extent`, `Path`, `Situation` (BTreeMap), `Fault`, `Problem` |
| Types (universal) | Potential | `Potential<T, C = ()>`, `Situated<F>` |
| Kinds (traits) | to Text | `Textualizable { fn textualize(&self) -> Text }` |
| Kinds (traits) | to Protoform | `Protosizable { type Fault; fn protosize(&self) -> Result<Delineation, Self::Fault> }` |
| Kinds (traits) | to Concept | `Conceivable<C> { type Fault; fn conceive(&self) -> Result<C, Self::Fault> }` |
| Kinds (traits) | to Corporate | `Incorporable<C>: Sized { type Fault; fn incorporate(concept: C) -> Result<Self, Self::Fault> }` |
| Kinds (traits) | chain | `Actualizable<T: Sized> { type Fault; fn actualize(&self) -> Result<T, Self::Fault> }` |
| Kinds (traits) | situation | `Pathed`, `Situating` |
| Impls | Textualizable | for Head, Protoform, Delineation |
| Impls | Protosizable | for Text (the delineator) |
| Impls | Actualizable | blanket for Potential<T, C> (protosize, conceive, incorporate) |
| Impls | Situating | for Delineation |

### datomic 0.10.0

| Module section | Layer or kind | What it holds |
|---|---|---|
| Concept type | Datom | Variant, Struct, Vector, Text, Meaning, Bare (6 variants, no Map) |
| Meaning | Meaning | Plain(Text) today; full structured meaning is future |
| Faults | Expected | Variant, Struct, Vector, Text, Meaning, Integer, Decimal, Boolean, Bare (no Map) |
| Faults | Problem | Shape, Arity, UnknownVariant, Separator, Value, OneValue (no Pairing, DuplicateKey) |
| Faults | Fault | Structural, Conceptual, Corporate (renamed from Corporal) |
| Kinds | Datomic | `Incorporable<Datom, Fault = Fault> + Sized`; methods `conceive`, `textualize` (default) |
| Impls | Protosizable | for Datom (concept to delineation, Infallible) via private Protosizing trait |
| Impls | Conceivable<Datom> | for Protoform, Delineation (protoform to concept, may fault) |
| Impls | Datomic | for Integer, Boolean, Decimal, Text, Meaning, Vec<T>, Option<T>, Result<T,E>, Datom, Expected, Problem, Fault, protos types, Situated<F> |
| Macro | impl_datomic_box! | for Box<T> where T: Datomic (orphan rule workaround for recursive types) |

## Decisions made on flow authority

| Decision | Rationale |
|---|---|
| Fault type keeps its name `Fault`; variant names are `Structural`, `Conceptual`, `Corporate` | Fault variant names match the four layers; `Corporate` replaces `Corporal` since the layer name is Corporate |
| Situation type remains `BTreeMap<Path, Extent>` in Rust | Efficient lookup by path; datom representation uses vector-of-structs (no map) but the Rust type is internal |
| Head qualifies as a symbol by being non-empty and containing no whitespace or delimiter | The vision says "the rule that qualifies a string as a symbol is not yet stated"; this rule is the minimum structural requirement from the delineator |
| Escape glyph inside parentheses is backslash | Carried forward from the current flow decision; `\)` `\(` `\\` |
| Tuple structs in the crates' own types: `Extent(pub Integer, pub Integer)`, `Situated<F>(pub Option<Extent>, pub F)` | Vision allows tuples at contact points; these are positional tuple structs consistent with ethos-declared types |
| Datomic kind's shape: the trait `Datomic` requires `Incorporable<Datom, Fault = Fault> + Sized`; provides `conceive(&self) -> Datom` and `textualize(&self) -> Text` (default) | Vision: "Datom is a kind, not a type, since it has no definite shape; the kind is Datomic"; incorporate from Datom (may fault), conceive to Datom (cannot fault), textualize through the chain |
| Recursion is boxed via `impl_datomic_box!` macro (unchanged pattern) | Rust orphan rules prevent blanket `Incorporable<Datom> for Box<T>`; the macro generates per-type impls |
| Boolean values: `True`/`False` (capitalized bare words) | Carried forward; consistent with variant naming convention in datom |
| Bare-string rule: a string is bare-safe when it contains no whitespace, no delimiter, no leading/trailing separator, no consecutive separators, and round-trips through delineation+conception as an all-bare chain | Carried forward from previous flow; the structural rule that makes `name:first` and `2026-09-03T17:46:20` bare |
| `Protoform::Bare(Head)` replaces both old `Bare(Symbol)` and `Qualified(Symbol, Vec<Protoform>)` | Keeps four variants per vision; `Head::Bare` for simple bare words, `Head::Qualified` for standalone qualified forms like `Vector<Text>` |
| `Textualizable` trait defined in protos, `Datomic::textualize` as default method | Rust orphan rules prevent blanket `impl<T: Datomic> protos::Textualizable for T` in datomic; the default method on Datomic chains conceive, protosize, textualize |

## Commits and versions

| Crate | Old version | New version | Commit (main) |
|---|---|---|---|
| protos | 0.15.1 | 0.16.0 | `ba2d1cdaec291eba3b919c88acc86c09480a4fdc` |
| datomic | 0.9.1 | 0.10.0 | `66e575323e12ca22c77478882849d2fd20c6ab1f` |

datomic pins protos at `ba2d1cdaec29`.

## Test and build output

### protos

```
test result: ok. 38 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`cargo clippy --all-targets -- -D warnings`: clean, no warnings.
`nix build`: success (protos-0.16.0).

### datomic

```
test result: ok. 40 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`cargo clippy --all-targets -- -D warnings`: clean, no warnings.
`nix build`: success (datomic-0.10.0).
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
