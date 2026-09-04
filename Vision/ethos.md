# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

## Why Ethos

Existing text data formats and existing programming languages both
fail. Rust is the new assembly, read in full by no one; Ethos is the
concise, dense, cognitively concentrated language for writing code
with AI agents — easy to read and write, showing the interfaces: the
main types and the main traits. Behavior falls under traits, which
creates an ontology in code.

## Generation

Ethos generates the Rust. Rust generated from ethos is committed, so
ordinary tooling — language servers — works normally; a freshness
mechanism is deliberately left open.

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

## Self-description

A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object —
CLI now, Mentci later — and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.

## Horizon

Ethos will eventually replace everything, Rustlang becoming its
assembly layer. Designs are chosen for that horizon; what it
enables — generator emission among it — comes in its time.

## Kind

Kind is the word for the bearer of capabilities: something that can
run is a runner, Runnable is its kind, and run is its capability, a
function the kind has. Trait is set aside as acoustically ambiguous.
In ethos there are no generics, only kinds. Declaring a new kind
declares a new trait in the Rust world and might imply more in the
ethos world.

## Naming

Kinds are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a kind. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

## Identity

A kind is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a kind, or a bracket of kinds: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only kinds; a
constraint in a kind declaration is a kind, never a type. Two heads
that differ in a constraint are two kinds. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the kind. What else a
kind declares, its superkinds, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.

```
Library.{
  {0 1 0}
  [ protos:[Text Textualizable] ]                             ; imports
  [ Record.{ Text Integer }                                   ; types: a struct of two fields
    Report.{ Text Vector<Integer> } ]                         ;   another
  [ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; kinds: the head is the identity, the name and two constraints,
                                                              ;   the first a bracket of two kinds, the second one kind;
                                                              ;   the bracket after the dot holds its capabilities, its definition
  [ Report.[ Textualizable ] ]                                ; associations: Report bears Textualizable
}
```
```rust
// The target Rust of the library above.
struct Record(Text, Integer);
struct Report(Text, Vec<Integer>);
// The trait's identity: its name and its constraints, two generic parameters with their bounds.
// What ethos writes as the bounds alone, Rust writes as a named parameter carrying them;
// the parameter names are Rust's need, not the kind's.
trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
impl Textualizable for Report { /* … */ }
```

## Declaration

### File

The unit is File: one file, one Rust module. No namespace inside a
file. An ethos file is written in the sweet form: the root's head
with its version, then the sections as siblings, the outer braces
omitted. The braced form — the root's head opening braces that hold
the version and every section — is the canonical form. The sweet
form is kept out of the main logic run: before the text is read as
ethos at all, the file is converted mechanically to the canonical
form, so the ethos reader sees only proper ethos.

Proper ethos is variant-headed: a properly defined struct with its
version and all of its fields. Ethos is an enum of such variants: a
kinds variant, which only holds kinds; a types variant, which only
holds types; a signal variant, which holds the specialized types of
a wire contract — a query type and a response type — each with its
own implied kind associations; a sema variant, which holds a storage
(record) type with its implied associated kinds. The implied
associations are a shorthand: instead of always adding the
associations by hand, they are implied, because these types always
bear those kinds in these variants, which are essentially different
kinds of structs.

```
; the sweet form, as a file is written: the head with its version, then the sections as siblings
Types.{ 0 1 0 }
[ … ]                         ; the variant's fields follow, each a section

; the canonical form the reader sees, after the mechanical conversion
Types.{
  { 0 1 0 }
  [ … ]
}
```

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
struct, `Name.[ V1 V2 ]` for an inline enum. The requests and the
responses of a signal are the variants of its query type and of its
response type.

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
body is hand-written Rust. In the signal and sema variants the
associations of the query, response and record types are implied and
never written.

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
itself in all cases.

### Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.
