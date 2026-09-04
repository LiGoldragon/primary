# API deviations from the spec

Flow 6329f1, subflow protos-datomic.

## Spec additions (not deviations)

### Head enum and Qualified protoform (protos)

The spec's Headed was `Headed.{ Symbol Separator Protoform }`. The coordinator directed
a spec addition: a symbol immediately followed by an angled enclosure (`Vector<Text>`,
`Processable<[Clonable Sendable] Serializable>`) is a Qualified structure, recognized
by protos as pure anatomy. The head of a Headed can be a bare symbol or a Qualified.

What stands:
- `Head.[ Bare.Symbol Qualified.{ Symbol Vector<Protoform> } ]`
- `Protoform::Headed(Head, Separator, Box<Protoform>)`
- `Protoform::Qualified(Symbol, Vec<Protoform>)` -- standalone
- Print: angle tight inside Qualified
- In datomic, conceive faults on Qualified

### Corporal trait in protos

The coordinator directed homing the universal chain in protos. Corporal is now a protos
trait with the concept as a type parameter (not an associated type) to satisfy the
orphan rule for primitive Datomic impls.

What stands:
- `Corporal<C: Protosizable>` in protos with `type Fault; fn incorporate(concept: C) -> Result<Self, Self::Fault>`
- `Potential<T, C = ()>` with two type parameters (C defaults to `()` for non-actualized use)
- Blanket `impl<C, T: Corporal<C>> Actualizable<T> for Potential<T, C>`
- `Pathed` trait in protos for path-bearing faults
- `Situated<F>` generic in protos
- `Datomic` extends `Corporal<Datom, Fault = datomic::Fault>` plus `datomize`
- `DatomicActualizable` dropped

Why: orphan rule requires C (the concept type) to be a type parameter so `impl Corporal<Datom> for i64`
is allowed from datomic (Datom is local, satisfying RFC 2451).

### Separator-before-qualified delineation rule

The coordinator confirmed: inside a bare run, a separator splits head from body before
qualification. `LockPaths.Vector<LockPath>` delineates as
`Headed(Bare(LockPaths), Period, Qualified(Vector, [Bare(LockPath)]))`, not as a
single Qualified. Same for chains: `A.B<C>.D`.

## Resolved deviations

### DatomicActualizable (resolved)

Previously: `DatomicActualizable<T: Datomic>` as orphan-rule workaround.
Resolution: `Corporal<C>` trait in protos with blanket Actualizable. DatomicActualizable dropped.

### MeaningValue renamed to Meaning

Previously: `MeaningValue` to avoid name collision with `Datom::Meaning`.
Resolution: the vision's type is `Meaning`; Rust has no collision between the enum
and the variant of a different enum.

## Remaining deviations

### Vision/datom.md map example type mismatch

The spec says `name:first Ada born 1990` is "a map of Text to Integer" but Ada is not
an integer. Tested as Text to Text. The example demonstrates the bare-string rule for
keys, and this behavior is covered.

## Resolved generated code defects

### ethos-zero incorporate/Datomic split (resolved at f2211ac6)

ethos-zero c85e9f76 emitted `incorporate` inside `impl datomic::Datomic` instead of
`impl protos::Corporal<datomic::Datom>`. Fixed in f2211ac6: the emitter now generates
two impl blocks (Corporal for incorporate, Datomic for datomize) at all generation sites.

### Signal aliases emitted as single-field structs (resolved at f2211ac6)

ethos-zero c85e9f76 emitted `Name.Type` aliases in Signal roots as
`pub struct Name(pub Type);` (single-field struct). Fixed in f2211ac6: aliases are always
`pub type Name = Type;` and no Corporal/Datomic impls are generated for them (the
underlying type already has them). `Release.42` is now a bare integer in datom.

### Wire types lacked Datomic impls (resolved at f2211ac6)

The wire envelope types (Version, Refusal, Body, Frame) had rkyv derives but no
Corporal/Datomic impls, so refusals could not be printed as datom. Fixed in f2211ac6:
all wire types now have Corporal and Datomic impls. A refusal prints as
`VersionMismatch.{ { 1 0 0 } { 0 9 0 } }` or `Unreadable`.

**Fixed in ethos-zero f2211ac6**: the emitter now generates separate `impl datomic::Corporal<datomic::Datom>` 
and `impl datomic::Datomic` blocks. `Name.Type` in Signal roots emits `pub type Name = Type;` (alias, 
not struct). Wire types (Version, Refusal, Body, Frame) also carry Corporal and Datomic impls.
The post-processing workaround is removed.

## Port findings (claude-answers port, flow 6329f1)

### datomic: no Datomic for Box<T>

datomic provides `Datomic` (and thus `Corporal<Datom>`) for `Vec<T>`,
`Option<T>`, `Result<T, E>`, and `BTreeMap<K, V>`, but not for `Box<T>`.
Since `Box` is `#[fundamental]`, datomic could provide `impl<T: Datomic>
Corporal<Datom> for Box<T>` and `impl<T: Datomic> Datomic for Box<T>`
without orphan issues. Without it, any consumer with a recursive type
must write a local impl per concrete type.

**Workaround**: claude-answers provides `impl Corporal<Datom> for Box<Query>`
and `impl Datomic for Box<Query>` locally, delegating to `Query::incorporate`
and `Query::datomize`. This is orphan-allowed because `Box` is fundamental
and `Query` is local.

### datomic: no Datomic for Situated<F>

`protos::Situated<F>(Option<Extent>, F)` has no `Corporal<Datom>` or `Datomic`
impl in datomic, even though `Option<Extent>` and every datomic `Fault` are
`Datomic`. datomic could provide `impl<F: Datomic> Corporal<Datom> for
Situated<F>` (the struct is from protos, the concept from datomic — orphan
rules allow it). Without it, a consumer that catches `Situated<Fault>` must
manually construct the datom to textualize the fault.

**Workaround**: claude-answers constructs
`Datom::Struct(vec![situated.0.datomize(), situated.1.datomize()])` and
textualizes it directly in main.rs.

### ethos-zero: Library types lack derive attributes

ethos-zero emits `#[derive(Archive, ...Clone, Debug, PartialEq, Eq)]` for
Signal types but no derives for Library types. A Library-only crate must
implement `Debug`, `Clone`, `PartialEq` manually or restructure its tests.

**Workaround**: claude-answers restructured its tests to use pattern matching
(`matches!()`) and textualization comparison (`assert_eq!(query.textualize(),
...)`) instead of direct struct equality.

### ethos-zero: Meaning maps to datomic::MeaningValue (stale name)

ethos-zero 1.1.0 maps the intrinsic type `Meaning` to `datomic::MeaningValue`
in its emitter, but datomic 0.8.0 names the type `datomic::Meaning`. Any ethos
declaring a Meaning field will produce non-compiling Rust. claude-answers does
not use Meaning, so this does not block the port.
