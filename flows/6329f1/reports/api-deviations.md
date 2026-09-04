# API deviations from the spec

Flow 6329f1, subflow protos-datomic.

## Spec additions (not deviations)

### Head enum and Qualified protoform (protos)

The spec's Headed was `Headed.{ Symbol Separator Protoform }`. The coordinator directed
a spec addition: a symbol immediately followed by an angled enclosure (`Vector<Text>`,
`Processable<[Clonable Sendable] Serializable>`) is a Qualified structure, recognized
by protos as pure anatomy. The head of a Headed can be a bare symbol or a Qualified.

What stands:
- `Head.[ Bare.Symbol Qualified.{ Symbol Vector<Protoform> } ]` -- the head is an enum
- `Protoform::Headed(Head, Separator, Box<Protoform>)` -- head is a Head, not a Symbol
- `Protoform::Qualified(Symbol, Vec<Protoform>)` -- standalone `Vector<Text>`
- Print: `Vector<Text>`, `Processable<[ Clonable Sendable ] Serializable>.[ cap ]` (angle tight, inner bracket spaced)
- In datomic, conceive faults on a Qualified head or a standalone Qualified (Shape)

Why: the coordinator's message of 2026-09-04, spec addition for ethos type expressions.

## Deviations

### DatomicActualizable instead of Actualizable (datomic)

The spec says `Actualizable<Embodied>` is borne by `Potential<T>`. Both the trait
and the type are defined in protos, and the generic parameter T is uncovered, so
the orphan rule prevents implementing `protos::Actualizable<T>` for `protos::Potential<T>`
from datomic. Instead, datomic provides `DatomicActualizable<T: Datomic>` as a trait
extension that gives `Potential<T>` its `actualize()` method.

What the spec said: `Potential<Datomic>.[ Actualizable ]`
What stands: `impl<T: Datomic> DatomicActualizable<T> for Potential<T>`
Why: Rust orphan rule (E0210)

### Vision/datom.md map example type mismatch

The spec says `\u{00AB} name:first Ada born 1990 \u{00BB}` is "a map of Text to Integer"
but Ada is not an integer. The test treats it as a map of Text to Text. The example
demonstrates the bare-string rule for keys (name:first with a colon is bare in a
string position), and this test covers that behavior.
