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
