# Distillation proposals

Flow 6329f1, 2026-09-04.

Two proposals ready to be reprinted whole to the living for approval.

---

## Proposal 1 — Vision/protos.md

The following replaces the current Vision/protos.md in its entirety.
Each statement is the living's word re-articulated; the vocabulary
is the living's own. Where the code has gone beyond the records,
those items are listed separately at the end and are not part of
the proposed vision.

### Proposed text (reprint whole)

<!-- begin Vision/protos.md -->

# Protos

## What Protos is

Protos is the name for the style all the dialects share. The
context-switching parse, the delimiters, the heads, the recursive
structure — this is the code that can be shared between all parsers
and belongs in protos. Datom is a protos dialect, carrying only
pure typed data; it does not take part in the multi-pass
rust-generation engine that ethos, nomos and logos are slated to
become, but it shares the protos style. The final fully-decomposed
engine with three daemons is the protos engine.

## What Protos knows

Protos is only about structure. It has nothing to do with struct and
vector, and it only understands form: the syntactic structure. It
would not know what anything is. A head in protos is just a head —
anatomy, not interpretation. Pure anatomy is only structural
recognition of delineations, nothing more. Protos examples show the
textual structure — the delimiters, the head, the capitalization, the
recursive structure — universally, at a very high level,
non-dialect-specific.

## Direction

Text arrives as a prospective value and leaves as a value. Realize
reads the textual form into the real form and may fault: the text
is prospective until it matches its anatomy. Textualize writes the
real form into the textual form and cannot fault: a real value is
already whole. Spans are found on the way in and computed on the way
out. Each direction is several passes.

## Structure

Structure is the word for every unit of the text; its type is
Protoform: headed, enclosed, opaque, or bare.

A headed structure is a head, a separator and a body. The separators
are period, exclamation and colon. The head is a symbol. The body is
another structure. Heads may be daisy-chained: different separators
too.

An enclosed structure stands between its delimiters. Six delimiter
pairs in all: four structural — braces, brackets, guillemets, angle
brackets — and two opaque — curly quotes, where every glyph inside
is content, and parentheses, read by balance. Angle brackets are a
real protos delimiter. A bare structure has no delimiters: a maximal
run.

## Delineation

Delineation is protos. A delineation is the structural survey of a
text: here we have a headed structure, there an enclosed one — no
detail as to what these things mean in terms of the dialect. A
brace-enclosed structure's arity is anatomical; a bracket-enclosed
structure's arity is not.

## Layers

Text, Protoform, Concept, Corporal — four layers. Potential and
actualize go universally, layer to layer. Embodied is the bound;
Corporal is kept for the layer. To embody any layer means we get the
layer below.

The structural capability is on text. The conceive capability is on
structure. The incorporate capability is on concept. The kind that
yields a Protoform is Protosizable.

| capability | sits on | yields |
|---|---|---|
| delineate (Structural) | Text | Protoform (as a Delineation) |
| conceive (Conceptual) | Protoform | the dialect's concept |
| incorporate (Corporal) | Concept | the corporal value |
| protosize (Protosizable) | Concept | Protoform |
| print (Printing) | Protoform | Text |

Structural is the kind name; Delineatable is better expressed as
Structural. Textualize is approved as the direction from value to
text. The whole chain: actualize on a Potential is delineate, then
conceive, then incorporate; textualize on any value is the dialect's
ascent to its concept (datomize, for datom), then protosize, then
print.

Embodied is the bound, an alias of Sized, borne by every corporal
type.

## Multi-pass

Multiple passes are wanted over a single pass, because a single pass
creates corner-cutting bad design. The multiple steps create a mental
model of the machinery, which enforces a correctness in the code that
is millions of times more beneficial than the cost of doing these
multiple passes. Extents are not intrinsic to objects; when we
textualize, these can be computed.

## Canonical print

It is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except for the curly quotes
where a space would be load-bearing. Space the delimiters and the
inner content.

<!-- end Vision/protos.md -->

### Realized by flow 6329f1, not yet the living's word

The following choices were made by this flow's design and writers.
They are in the code but have no psyche record; the living can raise
or reject each.

1. **Situation and Path beside the Protoform.** The flow introduced a
   `Situation` type (a map from `Path` to `Extent`) carried by
   `Delineation`, so that every structure in a delineation can be
   located in the source text by its path through the tree. The
   psyche said extents are not intrinsic to the object (04db2fd2) and
   that delineation finds all the anatomy (e8c4cc61), but the
   specific Situation/Path/Extent grouping and the decision to key
   them by a vector-of-indices path are the flow's design.

2. **The Qualified structure.** The flow introduced
   `Head::Qualified(Symbol, Vec<Protoform>)` and
   `Protoform::Qualified(Symbol, Vec<Protoform>)` to handle angle
   brackets inside bare runs (`Vector<Text>`, `Result<T E>`). The
   psyche ruled that `<>` is a real protos delimiter (b675f3d9) and
   that a head qualifies in ways beyond bare text (e4a40e), but the
   specific Qualified variant carrying a vector of child protoforms
   is the flow's synthesis.

3. **`Corporal<C>` as a protos kind with a type parameter.** The flow
   designed Corporal to take the concept as a type parameter `C`
   (rather than an associated type) so that a dialect can implement
   it for foreign types without orphan-rule violations. The psyche
   ruled incorporate on concept (62022e8f) and Corporal for the layer
   (62022e8f), but the parametrization is the flow's choice.

4. **The backslash escape inside parentheses.** The protos writer
   introduced `\)` as a literal closing parenthesis inside
   parenthesized opaque text. The psyche said parentheses are read by
   balance (Vision/datom.md) and that the escape for an unbalanced
   parenthesis is not yet designed (flow log). The backslash
   mechanism is the writer's choice where the vision left a gap.

### Sources (proposed for Vision/sources/protos.md)

```
a5587095 protosIsTheSharedStyle
ba906ae2 protosIsTheSharedStyle
ba906ae2 encodedFormIsTheCode
e4a40e protos
04db2fd2 anatomy
04db2fd2 multiPass
04db2fd2 portion
04db2fd2 delimiters
e8c4cc61 protos
e8c4cc61 prospective
e8c4cc61 kinds
62022e8f kinds
62022e8f layers
62022e8f concept
62022e8f passes
62022e8f vocabulary
2ef42163 kinds
b675f3d9 structuralParsing
b675f3d9 kinds
1c282d protosizable
1c282d vocabulary
ad19b1 ethos
```

---

## Proposal 2 — Vision/ethos.md, Declaration section

The following is proposed to stand in Vision/ethos.md after the
existing Identity section. Each statement is the living's word
re-articulated. Ethos examples show their target Rust beside them,
as the living ruled.

### Proposed text (reprint whole)

<!-- begin Vision/ethos.md Declaration -->

## Declaration

### File

The unit is File: one file, one Rust module. No namespace inside a
file. An ethos file declares one or more roots. The outer braces are
omitted and always implied in any ethos file; the sweet form — the
form a file is written in — has a corresponding type.

Two roots exist today. A Library declares types, kinds and their
associations. A Signal declares a wire contract: its requests and its
responses. A file holds one sweet root or a full-form datom — a root
in its braces, or a bracket of several ethos objects.

The anatomy of a Library file:

```
Library.{ version }
[ imports ]
[ types ]
[ kinds ]
[ associations ]
```

which the sweet form reads as:

```
Library.{
  { version }
  [ imports ]
  [ types ]
  [ kinds ]
  [ associations ]
}
```

The anatomy of a Signal file:

```
Signal.{ version }
[ imports ]
[ requests ]
[ responses ]
[ types ]
```

Target Rust for a Library: a Rust module with the declared types,
traits, and compile-time kind assertions. Target Rust for a Signal:
a Rust module with the request and reply enums, the declared types,
and a wire module carrying the frame.

### Imports

An import names a source and a type: `protos:Text` or
`protos:[ Text Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: Text,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

```
[ protos:[ Text Textualizable ]  datomic:Datom ]
```

The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:Text` appears as `protos::Text`,
`datomic:Datom` as `datomic::Datom`.

### Types

A struct is a headed brace — the name, a dot, and braces holding its
positions in order. An enum is a headed bracket — the name, a dot,
and brackets holding its variants. An alias is a headed bare — the
name, a dot, and the aliased type. A map is a headed guillemet — the
name, a dot, and guillemets holding the key type and the value type.

Positions are unnamed. Every struct is a tuple struct in the target
Rust; every variant carrying data is a tuple variant.

```
[ Record.{ Text Integer }
  Report.{ Text Vector<Integer> }
  SinkError.[ Closed Full ]
  LockId.Integer
  Roles.« Text Integer » ]
```
```rust
pub struct Record(pub protos::Text, pub protos::Integer);
pub struct Report(pub protos::Text, pub Vec<protos::Integer>);
pub enum SinkError { Closed, Full }
pub type LockId = protos::Integer;
pub type Roles = std::collections::BTreeMap<protos::Text, protos::Integer>;
```

A variant carrying nothing is bare. A variant carrying data is
headed: `Name.Type` for one type, `Name.{ T1 T2 }` for an inline
struct, `Name.[ V1 V2 ]` for an inline enum. Signal requests and
responses are the variants of their respective enums.

```
[ Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]
```
```rust
pub enum Request {
    Lock(LockRequest),
    Release(LockId),
    Observe(ObserveSelection),
}
```

No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.

### Kinds

Kind is the word for the bearer of capabilities; trait is set aside.
Declaring a new kind declares a new trait in the Rust world. A
capability is a function a kind has.

A simple kind opens with a bracket after the dot. Its capabilities
sit inside.

```
[ Summarizable.[ summarize.[ Text ] ] ]
```
```rust
pub trait Summarizable {
    fn summarize(&self) -> protos::Text;
}
```

The receiver after a capability's head names who is called: `.` takes
self, `!` takes mutable self, `:` takes no self.

A capability with inputs is a headed brace: inputs in a bracket,
yield in a bracket. A yield bracket holds one type.

```
[ Fillable.[ push!{ [ Text ] [ Result<Integer SinkError> ] }
             drain![ Vector<Text> ]
             create:[ Self ] ] ]
```
```rust
pub trait Fillable {
    fn push(&mut self, input: protos::Text) -> Result<protos::Integer, SinkError>;
    fn drain(&mut self) -> Vec<protos::Text>;
    fn create() -> Self;
}
```

A complex kind opens with a brace after the dot. Inside: superkinds
in a bracket, associated types with their constraints in a bracket,
associated constants in a guillemet — upper case, in the map
delimiter — and capabilities in a bracket.

```
[ Streamable.{ [ Fillable ]
               [ Item<Serializable> ]
               « CAPACITY Integer »
               [ next![ Option<Item> ] ] } ]
```
```rust
pub trait Streamable: Fillable {
    type Item: Serializable;
    const CAPACITY: protos::Integer;
    fn next(&mut self) -> Option<Self::Item>;
}
```

A kind's identity is its name and its constraints, as stated in the
Identity section above.

### Associations

An association declares that a type bears a kind. The type's name, a
dot, a bracket of its kinds. The generated Rust carries a
compile-time assertion that the type bears the kind; the interaction
body is hand-written Rust.

```
[ Sink.[ Summarizable Fillable ] ]
```
```rust
// Compile-time assertion: Sink bears Summarizable and Fillable.
const _: () = {
    fn assert_sink_summarizable<T: Summarizable>() {}
    let _ = assert_sink_summarizable::<Sink>;
    fn assert_sink_fillable<T: Fillable>() {}
    let _ = assert_sink_fillable::<Sink>;
};
```

Interactions — the term for trait implementations — use the type
itself in all cases. An interaction uses the type itself.

### Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.

<!-- end Vision/ethos.md Declaration -->

### Realized by flow 6329f1, not yet the living's word

The following choices were made by this flow's design and writers.
They are in the code but have no psyche record; the living can raise
or reject each.

1. **The Signal wire module.** The flow designed the wire envelope as
   `Frame.{ Version Body }`, `Body.[ Request Reply Refusal ]`,
   `Refusal.[ VersionMismatch.{ Version Version } Unreadable ]` with
   rkyv derives on every wire type. The psyche gave the Signal
   anatomy (e8c4cc61: Type/Version [Imports] [Requests] [Responses])
   and the binary wire over Unix sockets (Vision/nexus.md), but the
   specific Frame/Body/Refusal shape and the omission of a contract
   id (redundant with the socket) are the flow's design.

2. **The version as wire version.** The version in the Signal root
   (`Signal.{ 1 0 0 }`) is used as the wire protocol version in the
   generated Frame. The psyche's handwritten page shows
   Type/Version, and the flow interprets the version number as the
   compatibility gate for the wire.

3. **Aliases in Signal roots.** The signal crates use named aliases
   in their types sections (`LockId.Integer`, `LockName.Text`, etc.)
   for readability. The psyche's handwritten page shows requests and
   responses but does not prescribe or forbid aliases as a design
   pattern in Signal types.

4. **Copy for unit-only enums.** The ethos-zero emitter derives Copy
   for enums whose variants all carry nothing. The psyche ruled that
   any repetition in ethos syntax is an implementation failure
   (Vision/ethos.md Non-repetition), but the specific derive choice
   for the Rust output is the flow's.

5. **Boxing recursion.** The ethos-zero emitter detects recursive
   type positions and automatically boxes them, emitting the
   appropriate datomic macro. The psyche said portions exist inside
   portions (04db2fd2) and did not object to the box (04db2fd2), but
   the automatic detection and emission are the flow's mechanism.

6. **The compile-time assertion for associations.** The generated
   code carries a `const _` assertion pattern as the association's
   Rust realization. The psyche ruled that associations mean a type
   bears a kind, and that the interaction body is hand-written Rust,
   but the specific assertion pattern is the flow's implementation.

### Sources (proposed to append to Vision/sources/ethos.md)

```
e8c4cc61 ethosFileAnatomy
e8c4cc61 kinds
995a164e ethosTypes
62022e8f ethosTypes
aa4c7747 interactions
aa4c7747 tuples
aa4c7747 ethosTraitSyntax
2b34fafa ethosSourceFiles
2b34fafa ethosNamespaces
b675f3d9 kinds
b675f3d9 structuralParsing
ad19b1 ethos
ad19b1 designPractice
```

---

## Sources

04db2fd2 anatomy
04db2fd2 multiPass
04db2fd2 portion
04db2fd2 delimiters
62022e8f kinds
62022e8f layers
62022e8f concept
62022e8f passes
62022e8f vocabulary
62022e8f ethosTypes
e8c4cc61 protos
e8c4cc61 prospective
e8c4cc61 kinds
e8c4cc61 ethosFileAnatomy
2ef42163 kinds
b675f3d9 structuralParsing
b675f3d9 kinds
a5587095 protosIsTheSharedStyle
ba906ae2 protosIsTheSharedStyle
ba906ae2 encodedFormIsTheCode
1c282d protosizable
1c282d vocabulary
e4a40e protos
995a164e ethosTypes
aa4c7747 interactions
aa4c7747 tuples
aa4c7747 ethosTraitSyntax
2b34fafa ethosSourceFiles
2b34fafa ethosNamespaces
ad19b1 ethos
ad19b1 designPractice
ad19b1 kinds
Vision/protos Direction
Vision/ethos Identity
Vision/datom Syntax
Intent/protosParsing
Intent/data
