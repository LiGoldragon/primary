# protos and datomic rewrite

Flow 6329f1, subflow protos-datomic.

## What was read

1. Flow log `/home/li/primary/flows/6329f1/log.md` -- the full spec (Design section)
2. Vision/datom.md, Vision/ethos.md, Vision/protos.md
3. Intent/mandatoryTraits.md, Intent/data.md, Intent/protosParsing.md
4. Psyche records: flows/1c282d, 04db2fd2, 62022e8f, e8c4cc61, ad19b1 vision/
5. reports/psyche-mining.md, remember-1c282d.md, remember-ad19b1.md, code-anatomy.md
6. Existing protos (main 2f605fd) and datomic (main 8b17abc) source

## What was written

### protos 0.15.0

Branch: `ProtoformStack` at `56c683ec8d1e` (5 commits)
Worktree: `/home/li/wt/github.com/LiGoldragon/protos/protos-ProtoformStack-6329f1`

Files: `src/lib.rs`, `tests/delineation.rs`, `Cargo.toml`, `protos.ethos`, `README.md`, `ARCHITECTURE.md`, `UPGRADES.md`

### datomic 0.8.0

Branch: `ProtoformStack` at `768426ea5f34` (3 commits)
Worktree: `/home/li/wt/github.com/LiGoldragon/datomic/datomic-ProtoformStack-6329f1`

Files: `src/lib.rs`, `tests/datomic.rs`, `Cargo.toml`, `datomic.ethos`, `README.md`, `ARCHITECTURE.md`, `UPGRADES.md`

## Final public API

### protos 0.15.0

```rust
pub type Text = String;
pub type Integer = i64;
pub type Decimal = f64;
pub type Boolean = bool;
pub type Symbol = Text;

pub struct Extent(pub Integer, pub Integer);
pub type Path = Vec<Integer>;
pub type Situation = BTreeMap<Path, Extent>;
pub enum Separator { Period, Exclamation, Colon }
pub enum Enclosure { Braced, Bracketed, Guillemets, Angled }
pub enum Boundary { CurlyQuotes, Parentheses }

pub enum Head { Bare(Symbol), Qualified(Symbol, Vec<Protoform>) }
pub enum Protoform {
    Headed(Head, Separator, Box<Protoform>),
    Enclosed(Enclosure, Vec<Protoform>),
    Opaque(Boundary, Text),
    Bare(Symbol),
    Qualified(Symbol, Vec<Protoform>),
}
pub struct Delineation { pub protoforms: Vec<Protoform>, pub situation: Situation }
pub struct Fault { pub extent: Extent, pub problem: Problem }
pub enum Problem { Unclosed(Enclosure), UnclosedBoundary(Boundary), Unopened, MissingBody, MissingHead, EmptyInput }
pub struct Potential<T, C = ()>(Text, PhantomData<fn() -> (T, C)>);
pub struct Situated<F>(pub Option<Extent>, pub F);

pub trait Structural { fn delineate(&self) -> Result<Delineation, Fault>; }
pub trait Printing { fn print(&self) -> Text; }
pub trait Protosizable { fn protosize(&self) -> Protoform; }
pub trait Conceptual<C: Protosizable> { type Fault; fn conceive(&self) -> Result<C, Self::Fault>; }
pub trait Corporal<C: Protosizable>: Embodied { type Fault; fn incorporate(concept: C) -> Result<Self, Self::Fault>; }
pub trait Actualizable<T: Embodied> { type Fault; fn actualize(&self) -> Result<T, Self::Fault>; }
pub trait Pathed { fn path(&self) -> &[Integer]; }
pub trait Situating { fn situate(&self, path: &[Integer]) -> Option<Extent>; }
pub trait Embodied: Sized {} // blanket

// Blanket: impl<C, T: Corporal<C>> Actualizable<T> for Potential<T, C> where ...
```

### datomic 0.8.0

```rust
pub enum Datom { Variant(..), Struct(..), Vector(..), Map(..), Text(..), Meaning(..), Bare(..) }
pub struct Pair(pub Datom, pub Datom);
pub enum Meaning { Plain(Text) }
pub enum Expected { Variant, Struct, Vector, Map, Text, Meaning, Integer, Decimal, Boolean, Bare }
pub enum Problem { Shape(..), Arity(..), UnknownVariant(..), Separator(..), Value(..), Pairing, DuplicateKey(..), OneValue }
pub enum Fault { Structural(protos::Fault), Conceptual(Path, Problem), Corporal(Path, Problem) }

pub trait Datomic: Corporal<Datom, Fault = Fault> { fn datomize(&self) -> Datom; }
pub trait Textualizable { fn textualize(&self) -> Text; } // blanket for Datomic

// Corporal<Datom> + Datomic for: Integer, Decimal, Boolean, Text, Meaning, Vec<T>, BTreeMap<K,V>, Option<T>, Result<T,E>, Expected, Problem, Fault, Datom
// Conceptual<Datom> for Protoform and Delineation
// Protosizable for Datom; Pathed for Fault; From<protos::Fault> for Fault
```

## Judgment calls (subflow protos-datomic, flow 6329f1)

1. **Corporal type parameter**: Corporal takes the concept as a type parameter `C` (not associated type) to satisfy the orphan rule for `impl Corporal<Datom> for i64`. This adds a second type parameter to `Potential<T, C>`.

2. **Separator-before-qualified rule**: Inside a bare run, a separator splits head from body BEFORE qualification. `LockPaths.Vector<LockPath>` delineates as Headed(Bare(LockPaths), Period, Qualified(Vector, [LockPath])), not a single Qualified with a dotted symbol.

3. **Meaning vs MeaningValue**: Renamed to `Meaning` per the vision. No Rust collision with `Datom::Meaning`.

4. **Head enum**: Chose a dedicated `Head` enum (`Bare`/`Qualified`) rather than using Protoform for the head position, keeping the constraint explicit in the type system.

5. **Fault Datomic impls**: Structural fault incorporate is simplified (reconstructs a placeholder protos::Fault) since exact structural fault round-trip requires the protos::Problem enum to also be Datomic. The Conceptual and Corporal variants round-trip exactly.

## Witnessed test and nix results

### protos
- `cargo test`: 37 passed, 0 failed
- `cargo clippy --all-targets -- -D warnings`: pass
- `cargo fmt --check`: pass
- `nix flake check`: all checks passed (remote builder prometheus)

### datomic
- `cargo test`: 32 passed, 0 failed (6 proptests, 26 unit)
- `cargo clippy --all-targets -- -D warnings`: pass
- `cargo fmt --check`: pass
- `nix flake check`: pass (remote builder prometheus)

## Pushed revisions

- protos ProtoformStack: `56c683ec8d1e`
- datomic ProtoformStack: `768426ea5f34`

## Left undone

1. **ethos-zero, signal crates, orchestrate**: subsequent train stops
2. **Worktrees**: remain for the next train stops (ethos-zero pins these revs)

## Sources

- Flow 6329f1 log.md (spec)
- Vision/datom.md, Vision/ethos.md, Vision/protos.md
- Intent/mandatoryTraits.md, Intent/data.md, Intent/protosParsing.md
- Psyche flows: 1c282d, 04db2fd2, 62022e8f, e8c4cc61, ad19b1
- reports/psyche-mining.md, remember-1c282d.md, remember-ad19b1.md, code-anatomy.md
