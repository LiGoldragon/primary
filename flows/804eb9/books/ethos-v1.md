Presentation.{ «Ethos: the basics» }

# Ethos: the basics

```
+-------------+
|    Ethos    |
+-------------+
   | declares
   v
+-------------+   fills    +-------------+
| types and   |<-----------|    Datom    |
| traits      |            +-------------+
+-------------+
   | generates through Ethos Zero
   v
+-------------+
| Rust types  |
| and traits  |
+-------------+
   | are given bodies by
   v
+-------------+
| hand-written|
| capabilities|
+-------------+
```

```
+-------------------------+
| a file: a vector of     |
| roots                   |
+-------------------------+
   | holds            | holds
   v                  |
+-----------------+   |
| Library: what   |   |
| is shared       |   |
+-----------------+   |
   | is shared by     |
   v                  v
+-------------------------+
| Signal: what it says    |
| Operation: what it does |
| Memory: what it keeps   |
+-------------------------+
```

```
+------------+
|    type    |
+------------+
   | bears
   v
+------------+
|   trait    |
+------------+
   | holds
   v
+------------+
| capability |
+------------+
   | is
   v
+------------+
| what the   |
| type does  |
+------------+
```

## psyche-context › vision/ethos.md

````markdown
## Flow, a current best example

Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.

## Where the golden ethos lives

```
┌──────────────────────────────────────────┐
│ vision-ethos                             │
│                                          │
│  what ethos is · its layout              │
│  its two anatomies: types and traits     │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ the ethos of ethos                 │  │
│  │ the types an ethos file is made of │  │
│  │ the first golden ethos             │  │
│  └────────────────────────────────────┘  │
└───────────────────┬──────────────────────┘
                    │ example
                    ▼
        ┌───────────────────────┐
        │ vision-flow-ethos     │
        │ the Flow Nexus, in    │
        │ ethos; its own skill  │
        └───────────────────────┘
```

The anatomy of ethos lives in vision-ethos itself, as
the first golden ethos; Flow's ethos is one example,
in its own skill.

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

Ethos is central. The anatomy of the system, every type and every trait
it uses, is read in its ethos; an implementation is mostly the
hand-written bodies.

## Why Ethos

All the legacy languages have a high noise ratio. Some lisps came
close but lacked the correctness of Rust or Haskell; those have the
correctness but allow no higher layer of abstraction that keeps the
correctness of the whole. Ethos writes the mental model and the code
in one swoop.

## Roots

Library, Signal, Operation, Memory. No version in a file. Signal's sections are
queries and responses, since there is communication; Sema's are record
types, the rest to be decided. Signal gives a Nexus its main types and
Sema its database types.

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

Terseness is in the low amount of noise, never in shortened words.

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

## Trait

Trait is the word for the bearer of capabilities, the same word in
ethos and in Rust; kind might be used to also mean traits.
In ethos there are no generics, only traits. Declaring a new trait
declares a new trait in the Rust world and might imply more in the
ethos world.

A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named.

## Naming

Traits are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

## Identity

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a trait, or a bracket of traits: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only traits; a
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the trait. What else a
trait declares, its supertraits, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.

```
Library
[ std:[ Clonable Sendable Serializable ] ]                  ; imports: where the three constraint traits come from
[]                                                          ; types
[ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; traits: the head is the identity, the name and two
                                                            ;   constraints, the first a bracket of two traits, the
                                                            ;   second one trait; the bracket after the dot holds
                                                            ;   its capabilities, its definition
[]                                                          ; associations
```
```rust
// The trait's identity: its name and its constraints, two generic parameters with their bounds.
// What ethos writes as the bounds alone, Rust writes as a named parameter carrying them;
// the parameter names are Rust's need, not the trait's.
pub trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
```

## Declaration: File

The unit is File: one file, one Rust module. No namespace inside a
file. An ethos file is written in the sweet form: the root's head,
then the sections as siblings, the outer braces omitted. The braced
form — the root's head opening braces that hold every section — is
the canonical form. The sweet form is kept out of the main logic run:
before the text is read as ethos at all, the file is converted
mechanically to the canonical form, so the ethos reader sees only
proper ethos.

An ethos file carries no version; datom has no versions. What is
versioned is versioned in a manifest of some kind, never in the file.

A Library's sections, in order, are imports, types, traits and
associations. Every root's first section is its imports; its own
sections follow.

```
; the sweet form, as a file is written: the head, then the sections as siblings
Library
[ protos:String ]               ; imports
[ Record.{ String Integer } ]   ; types
[]                              ; traits
[]                              ; associations

; the canonical form the reader sees, after the mechanical conversion
Library.{
  [ protos:String ]
  [ Record.{ String Integer } ]
  []
  []
}
```

## The type ethos

`Type` is a single-field variant carrying one declaration, so its payload is the declaration's own form, as any single-field variant's is; it is no exception to the datom.

```
Type.CommitMessage.[ Landing.Vector<String>
                     Fix.String ]
```

## Imports

An import names a source and a type: `protos:String` or
`protos:[ String Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

```
Library
[ protos:[ String Textualizable ]  datom:Datom ]   ; imports
[]                                                 ; types
[]                                                 ; traits
[]                                                 ; associations
```

The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.

A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.

## What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
A field is named after its type in snake case; a constructed type
type-first, `string_vector`, `lock_option`; a repeated type as first
and second.

```
Library
[]                                            ; imports
[ LockId.Integer                              ; types
  LockName.String
  Lock.{ LockId LockName Vector<String> Option<Lock> }
  Generation.{ String String } ]
[]                                            ; traits
[]                                            ; associations
```
```rust
pub type LockId = Integer;
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
#[derive(Datomizable, Compositional)]
pub struct Generation { pub first_string: String, pub second_string: String }
```

## Inline types

A type may be declared where it is used. The inline struct or enum is
a full type whose derived name carries an underscore, non-idiomatic
for a Rust type, so it never collides and reads at a glance as
inferred from the sugar.

```
Library
[]                                                       ; imports
[ LockId.Integer                                         ; types
  LockName.String
  Lock.{ LockId LockName }
  LockRejection.[ DuplicateName.Lock                     ;   an enum: one variant naming a defined type,
                  PathOverlap.{ Lock Lock } ] ]          ;   one declaring its payload inline
[]                                                       ; traits
[]                                                       ; associations
```
```rust
pub type LockId = Integer;
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
#[derive(Datomizable, Compositional)]
pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
#[derive(Datomizable, Compositional)]
pub enum LockRejection { DuplicateName(Lock), PathOverlap(PathOverlap_Data) }
```

Everything is a type; there is no key-value. A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.

## A variant named as a defined type carries that type

When a variant's name is a type already defined in the library, that
type is the data the variant carries. Nothing further is written.

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: FilePath is an alias of String
  SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
  GenerationFailure.[ SyntaxError          ;        an enum: the variant SyntaxError is bare here,
                      Unwritable ] ]       ;        but SyntaxError is a defined type, so it carries one
[]                                         ; traits
[]                                         ; associations
```
```rust
pub type FilePath = String;
pub type SyntaxError = Vec<FilePath>;
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```
```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]     ; the datom
```

## A variant may declare its payload inline

Instead of naming a defined type, a variant may declare what it
carries in place: a vector, a struct, or an enum, each a full type
with a derived name, recursively.

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   declared inline: a struct, derived name
[]                                                        ; traits
[]                                                        ; associations
```
```rust
pub type FilePath = String;
#[derive(Datomizable, Compositional)]
pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(Vec<FilePath>), Unwritable(Unwritable_Data) }
```

## Every declared type bears both traits

Ethos Zero emits `Datomizable` and `Compositional` on every struct and
enum it generates, so every ethos-declared type always bears both
traits and no declared type can exist without them. An alias bears them
through the type it names: an alias is not a new type and cannot carry
a derive.

```rust
pub type FilePath = String;                  // an alias: String already bears both
pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
#[derive(Datomizable, Compositional)]        // a type: always derived
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

## The datom traits are compiled in only where text is spoken

A generated signal library bears `Datomizable` and `Compositional`
conditionally, under a feature the CLI and client enable and the Nexus
does not. The Nexus compiles the same types without any
textualization capability and without datom-codec as a dependency.

```rust
// emitted by Ethos Zero into the signal crate
#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
pub enum Query { Lock(LockRequest), Release(LockId) }
```
```toml
# the CLI's manifest
signal-orchestrate = { version = "…", features = ["datom"] }
# the Nexus's manifest
signal-orchestrate = { version = "…" }
```

## Shapes and placement

Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in a
Signal's first two sections, an alias in the types section. Where
types are defined a bracket is an enum, never a vector. Ethos may
generate default implementations for Query and Response, which is why
Signal is its own root.

```
Signal
[]                                                     ; imports
[ Lock.LockRequest  Release.LockId ]                   ; queries
[ Locked.Lock  Released.Lock ]                         ; responses
[ LockId.Integer                                       ; types
  LockName.String
  FlowId.String
  LockRequest.{ LockName FlowId }
  Lock.{ LockId LockName } ]
```
```rust
pub enum Query    { Lock(LockRequest), Release(LockId) }
pub enum Response { Locked(Lock), Released(Lock) }
pub type LockId = Integer;
pub type LockName = String;
pub type FlowId = String;
```

## Traits are explicit; bodies are hand-written

A trait is declared, never inferred; an association asserts the type
bears it. The generated Rust carries a compile-time assertion that the
type bears the trait; the interaction body is hand-written Rust.

```
Library
[]                                                ; imports
[ Record.{ String Integer } ]                     ; types
[ Summarizable.[ summarize.[ String ] ] ]         ; traits
[ Record.[ Summarizable ] ]                       ; associations
```
```rust
#[derive(Datomizable, Compositional)]
pub struct Record { pub string: String, pub integer: Integer }
pub trait Summarizable { fn summarize(&self) -> String; }
// Compile-time assertion: Record bears Summarizable.
const _: () = {
    fn assert_record_summarizable<T: Summarizable>() {}
    let _ = assert_record_summarizable::<Record>;
};
```

## Trait syntax

A simple trait opens with a bracket after the dot. Its capabilities sit
inside. The receiver after a capability's head names who is called:
`.` takes self, `!` takes mutable self, `:` takes no self. A
capability with inputs is a headed brace: inputs in a bracket, yield
in a bracket. A yield bracket holds one type.

```
Library
[]                                                            ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; traits
             drain![ Vector<String> ]
             create:[ Self ] ] ]
[]                                                            ; associations
```
```rust
#[derive(Datomizable, Compositional)]
pub enum SinkError { Closed, Full }
pub trait Fillable {
    fn push(&mut self, input: String) -> Result<Integer, SinkError>;
    fn drain(&mut self) -> Vec<String>;
    fn create() -> Self;
}
```

A complex trait opens with a brace after the dot. Inside: supertraits in
a bracket, associated types with their constraints in a bracket,
associated constants in a bracket — upper case, each the name, a dot,
and its type — and capabilities in a bracket.

```
Library
[ std:Serializable ]                                ; imports
[]                                                  ; types
[ Fillable.[ create:[ Self ] ]                      ; traits
  Streamable.{ [ Fillable ]
               [ Item<Serializable> ]
               [ CAPACITY.Integer ]
               [ next![ Option<Item> ] ] } ]
[]                                                  ; associations
```
```rust
pub trait Fillable { fn create() -> Self; }
pub trait Streamable: Fillable {
    type Item: Serializable;
    const CAPACITY: Integer;
    fn next(&mut self) -> Option<Self::Item>;
}
```

A trait's identity is its name and its constraints, as stated in the
Identity section above.

## Associations

An association declares that a type bears a trait: the type's name, a
dot, a bracket of its traits. In the Signal and Sema roots the
associations of the query, response and record types are implied and
never written. In a Library they are the fourth section, after the
traits.

```
Library
[]                                                       ; imports
[ Sink.{ String Integer } ]                              ; types
[ Summarizable.[ summarize.[ String ] ]                  ; traits
  Fillable.[ create:[ Self ] ] ]
[ Sink.[ Summarizable Fillable ] ]                       ; associations
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

No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.

## Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.

## Zero

Ethos Zero was first named Ethos Monolith; the two are the same thing.
Zero as in version 0: no daemon yet, no Nexus. The ethos repository is
for the ethos nexus that follows.

## Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```
````

### Proposal 1: A file is a vector of roots · psyche-context › vision/ethos.md

In Roots. Rule: land, amend or reject.

+ A file is a vector of roots, so a library, a signal, a memory and an operation may stand in one file; which roots share a file is file management only.

```ethos
+ [ Library.{
+   []
+   [ Name.String
+     Shape.[ Round Square ]
+     Sink.{ Name Shape } ]
+   [ Named.[ name.[ String ] ]
+     Shaped.[ shape.[ Shape ] ] ]
+   [ Named.[ Name Sink ]
+     Shaped.[ Shape Sink ] ] }
+   Memory.{
+   []
+   [ Record.{ Name Integer } ]
+   [ Stored.[ store![ Record ] ] ]
+   [ Stored.[ Record ] ] } ]
```

### Proposal 2: A file of one root may drop the vector · psyche-context › vision/ethos.md

Added to Proposal 1. Reject it, and every file is written as a vector. Rule: land, amend or reject.

+ A file that holds one root may write it without the vector.

### Proposal 3: Every root carries traits · psyche-context › vision/ethos.md

In Roots and Associations. Rule: land, amend or reject.

+ Every root ends with a traits section and an associations section, as a Library does, because a type does things only through the traits it bears.
- In the Signal and Sema roots the associations of the query, response and record types are implied and never written.

### Proposal 4: A type that bears no trait is refused · psyche-context › vision/ethos.md

In Traits are explicit; bodies are hand-written. Rule: land, amend or reject.

+ Every declared type bears at least one trait; a type that bears none is refused, because it does nothing.

### Proposal 5: A type over one type is a new type · psyche-context › vision/ethos.md

In What a declaration turns into. Rule: land, amend or reject.

+ A type declared over one other type is a new type, never an alias: `Name.String` is a struct of one unnamed position.
+ A struct has at least two positions; a type of one position is written as a new type, `Name.String`, never `Name.{ String }`.
+ An enum has at least two variants.

### Proposal 6: Ethos is shown as Ethos · psyche-context › vision/ethos.md

In What Ethos is. Rule: land, amend or reject.

+ Ethos is shown as Ethos; the Rust it generates is shown only where the subject is how Ethos generates Rust.

## psyche-context › vision/datom.md

````markdown
## Name

Datom is the psyche’s own coinage for the new data notation, the
successor to NOTA and to the rejected name Dotos. The name was
chosen for its energetic power and to echo what the notation is:
data, strictly typed, super dense, no field names. The library is
datom-codec. Datomic names the conceptual layer abstractly; it is
not a term of the code.

## Nature

Datom is the most advanced textual data format in the world. It
carries data, strictly typed, and its whole work is serialization and
deserialization: carrying data between text and typed form. Datom is
signal's form at the edge: our components speak signal, and datom lets
text-based systems, LLMs and every existing editor, read and write it.
Generating Rust is Ethos's duty, in today's division of labor. When
Ethos becomes the full authoring language, with Rustlang as its
assembly layer, Datom, the data dialect of the Protos family, may gain
an inline place in authored Ethos, the way Rustlang composes data
directly in code. That road is reached, or even floated, only with
explicit context: how, when, and where data yields Rust, stated
without ambiguity; until then the division stands as spoken.

## A datom is a form at a path

```rust
pub struct Datom { pub path: Path, pub form: Form }
pub enum Form { Struct(Vec<Datom>), Vector(Vec<Datom>), Variant(Symbol, Box<Datom>), Bare(String), String(String), Meaning(Opaque) }
```

## Strings

Two string forms. The bare form, whose name is bare: a run with no
space and no delimiter glyph, which may be a whole sentence written
without spaces in any casing; "word" does not do it justice. It is a
bare string, undelimited because it needs no delimiters. The delimited
form: guillemets, which keep the doubleness of the double quote,
cannot be mistyped for it, and point, so the ends are visible at any
size.

```
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
```

## Syntax

Structure is the word for every unit of the text: enclosed when it
stands between its delimiters, unenclosed when bare. A headed
structure is a head, a separator and a body; the dot is the separator,
written right after the head. Any whitespace, any amount, may follow it: a space, a tab, a line break; so nesting may go down instead of to the right. A
head is a symbol. In datom a head is always a variant, so it is
capitalized. Which head a structure carries is part of its type:
`Accepted.{ … }` and `Refused.{ … }` are two types. When an enum value
is textualized, its variant's name is written as the head every time,
a variant carrying nothing included: `Pending`, never an empty
structure. A brace structure is a struct and a bracket structure is a
vector. A head in front of a structure makes a variant that carries
it: `Reviewer.{ 2024 17 }` is the Reviewer variant carrying a struct
of two positions, and `Observed.Locks.[]` is the Observed variant
carrying the Locks variant carrying an empty vector. A symbol alone,
in a position expecting an enum, is a variant carrying nothing. A
datom is not preceded by a Datom root; a comment may say it is datom.
Guillemets are the string delimiter, and parentheses are reserved for
Meaning. A string is a string only in a position where the type
defines a string. In such a position a string is written bare when it
contains no space and no delimiter, Ada, 75002, 2026-09-03; any other
string is written in guillemets. Because the position already knows it
holds a string, a bare run may contain characters that are syntax
elsewhere, the colon among them. A guillemet string is opaque: every
glyph inside it is content until the closing guillemet, which is
escaped with a backslash where it is content. An integer is written as
bare decimal, 0, 42, -42: ASCII digits, no leading plus, no leading
zero except 0 itself. A single semicolon opens a comment. Canonical
text leaves a space inside every bracket and brace delimiter, at both
ends, so that head, dot, delimiter and content read apart, and never
inside the guillemets, where a space is content.

```
Observed.Locks.[]     ; on one line
Observed.             ; or going down
   Locks.
      []
```

```
; datom, in a position expecting Person: a struct of name String, born Integer, address Address, roles Vector<Role>.
; Each comment names the structure that starts on its line. Indentation shows which structure holds which.
{                                        ; the whole Person is one structure, enclosed by braces: a struct. It holds four structures.
  Ada                                    ;   unenclosed, a bare run. The position says String, so it is a string.
  1990                                   ;   unenclosed. The position says Integer.
  { «12 Rue de la Paix» Paris 75002 }    ;   enclosed by braces: a struct, the Address. It holds three structures:
                                         ;     one enclosed by guillemets, opaque, and two unenclosed.
  [ Author                               ;   enclosed by brackets: a vector of Role. It holds two structures:
    Reviewer.{ 2024 17 } ]               ;     a symbol alone, the Author variant carrying nothing, and a headed structure:
}                                        ;     head Reviewer, the dot, and a body that is itself a struct of two unenclosed structures.
                                         ; The closing brace ends the outermost structure, the Person itself.
```

The whole is a structure, and so is every part of it, down to the
unenclosed ones, which hold nothing. What a structure means, struct,
vector, string, integer, variant, is said by the position it sits in,
never by the structure alone.

```
; Reply: an enum of Accepted.{ id Integer  at String }, Refused.{ reason String  code Integer }, Pending
Accepted.{ 42 2026-09-03T17:46:20 }          ; the timestamp has no space and no delimiter, so it is bare
Refused.{ «no such file: { } is content» 2 } ; delimited: the string has spaces and braces; inside the guillemets they are content
Pending                                      ; a variant carrying nothing

; a vector of Integer
[ 0 42 -42 ]
```

## The datom composes; the type states its positions

The descent into a composition is the datom's act, written once. What
only the type can supply, its positions in order, is stated by the
type through the derive, so the reading of the tree, arity, budget,
locus, lives in one place and no type repeats it.

```rust
impl Composable for Datom {
    fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error> {
        let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity, else an error at this path
        T::from_positions(positions)
    }
}
```

## Any Rust type

Datom is used on more than ethos-declared types. Any Rust type bears
the two kinds through a derive in datom-codec, with no attributes,
because datom is structural all the way down: field order is position
order, a field's type is the position's type, a bare variant carries
nothing, a single-field variant carries its type's own form, a
multi-field variant carries an inline struct. Hand-written impls are
reserved to the intrinsics.

```rust
#[derive(Datomizable, Compositional)]
pub struct Locus { pub path: Path, pub extent: Extent }

impl Compositional for Locus {                              // generated
    const ARITY: Integer = 2;
    fn from_positions(mut p: Positions<'_>) -> Result<Self, Error> { Ok(Locus { path: p.position()?, extent: p.position()? }) }
}
impl Datomizable for Locus {                                // generated: each child placed as the tree is built
    fn datomize(&self, at: Path) -> Datom {
        Datom { form: Form::Struct(vec![self.path.datomize(at.child(0)), self.extent.datomize(at.child(1))]), path: at }
    }
}
```

## From text and back

A potential, text that may become a T, owns the budget and actualizes
by the descent written once: protosize, datomize, compose. A
composition becomes text by the open chain.

```rust
let query: Query = Potential::<Query>::from(text).actualize(budget)?;
let out = response.datomize(Path::root()).protosize().textualize();
```

## Containers

Vector, Option, Result, Box bear the kinds once, generically; Option
and Result read as ordinary variants.

```
[ Some.42 None ]     Ok.{ Ada 1990 }     Err.«no such lock»
```

## Errors

An error names the layer that raised it and the path of the datom
where it arose; the extent is the protos node at that path. An error
is itself datomizable.

```
[ 1 x ]                                  ; read as Vector<Integer>
Corporate.{ [ 1 ] Value.x }              ; at path 1, the bare string x is not an integer
```

## Omittable fields

Not yet; a written datom gives every position.

```
Deploy.{ ouranos }     ; Arity.{ 2 1 }
```

## The interface shape

A program's configuration surface is the datom's shape itself, as the
ethos interface declares it: a data enum at the root whose variants
are the main operations. A variant's data carries what follows:
another enum where sub-operations are wanted, a struct or vector for
final options, and a struct may embed further sub-operations, or any
combination imaginable. Output is an enum, always; even the most basic
response interface is an enum: Success or Failure. The shape already
is the interface: datom creates the configuration options by its very
shape, and a CLI takes its whole configuration from its datom input. A
Nexus reply is written as its heads down to its data, and only what
carries data is written: an empty Locks observation is
Observed.Locks.[], the Observed variant, its Locks variant, the empty
vector; the layout of a nonempty payload is open.

```
; datom, each in a position expecting the response enum named in the comment
Observed.Locks.[]    ; orchestrate's response: the Observed variant, its Locks variant, the empty vector
Success              ; the most basic response: a variant carrying nothing
```

## De/serialization

Schema-driven and positional: the reader walks the expected type,
writing is the exact reverse projection, and decoding lands directly
in the typed Rust compositions. A datom on the way in is a potential
datom, untrusted until it matches its type; on the way out it is a
datom. All naming and self-description live in the type; the text
carries only the data.

```
; datom, in a position expecting Scores: a struct of name String, values Vector<Integer>.
; The reader walks the type: first position a string, second a vector of integers. The text carries only the data.
{ Ada [ 12 7 -3 ] }
```

## Relation to Ethos

Datom and Ethos are different languages that share an approach, not a
parser. What they may share is a substrate, kinds with a shared
implementation and types; the universal substrate machinery is homed
in protos, all dialects ride it, and datom is the pure-data dialect on
it. Ethos could come to depend on Datom for another reason: ethos
might be read as datom in one pass. Whether that is even possible,
given the situation and the actualization involved in parsing ethos,
is not settled, and the question is set aside for now.

## Repository

Everything moves to Datom: all of the stack, Horizon, Lojix, everything;
no Dotos file remains. Datom's own line of descent is NOTA, which also
passed through the temporary name Dotos; that old notation stays
behind, frozen, and may be called legacy. Schema is the abandoned
ancestor of Ethos, not of Datom. The library is named datom-codec so
that datom is free for the datom nexus, which comes when there is more
to do: translating datom objects between formats, and a parsing cache
keyed by the content-addressed hash of normalized text.

## Map

A map is a container whose keys are known only from the data: the
reader learns the shape by reading, where a struct's shape is known
before reading. Datom is typed from the position down: a position
knows its type before the text is read, and a container that reveals
its shape only in the text contradicts that. So datom has no map. Most
of what is called a map is not one: an object with fixed fields, a
configuration table, a record written as a dictionary. These are
structs whose notation declined to declare their fields, and every
such notation ends up adding a way to declare them; that the word
covers so much that is not a map shows how little a map is actually
used. The map that remains, its keys minted at run time and its values
all of one type, is a vector of structs, which is how the typed data
formats already write it; that keys do not repeat is a rule the type
states. What a map would hold is a struct when its keys are fixed, and
a vector of structs when they are not. Datom does not implement a
thing because it has been standard in the past.

## Meaning

Meaning is the structured string: text that carries, besides its
words, the emphasis and the other structural aspects a plain string
simply lacks, an annotated string, meant to revolutionize the
performance of thinking machines on text. The aim is the most
advanced structured meaning system ever made. Parentheses are a
major symbol of cognition, and in datom they have one duty: the
parenthesis pair is the Meaning delimiter, as the guillemets are
the plain string's. The seed of the design is that parentheses
inside ordinary text are already markup, so a Meaning is read by
balance: a parenthesis pair inside it is structure of its own,
nesting to arbitrary depth, a graph of sorts, and the Meaning closes
at the parenthesis that balances the one that opened it; an
unbalanced parenthesis inside it is escaped. Opening a Meaning makes
the whole delimiter and structure spectrum available inside it,
until the closing parenthesis restores the outer context. Its
annotations are enums used throughout the tree, Emphasis among them;
its shape is still open. Meaning is datom. Strings are strings and
Meaning is Meaning: a position of type String expects a plain string
and nothing else, and a position of type Meaning expects a Meaning.
Meaning is postponed so that a working syntax lands as soon as
possible: today a parenthesized text lands as a plain String, with
the later type marked in code. The name Meaning smells of a verb; it
stands provisionally and is reopened together with the type.

```
; datom, in a position expecting Note: a struct of author String, body Meaning.
; The first position expects a string: Ada has no space and no delimiter, so it is bare.
; The second position expects a Meaning, so the parenthesis opens it and it is read by balance:
; the inner pair is structure inside the Meaning, and the parenthesis that balances the opening one ends it.
; Today the whole parenthesized text lands as a plain String; what the inner pair will mean is not yet designed.
{ Ada (The build passed on the third try (after two timeouts)) }

; datom, in a position expecting Remark: a struct of author String, body String.
; The second position expects a plain string; it has spaces, so it is delimited,
; and the parentheses inside the guillemets are content, not a Meaning.
{ Ada «The build passed on the third try (after two timeouts)» }

; datom, in a position expecting Standup: a struct of team String, items Vector<Meaning>.
; Each component of the vector is one Meaning; each is read by balance on its own.
{ Backend
  [ (Ada fixed the flaky test (the one with the timeout))
    (Bo is out (back Monday)) ] }
```

The meaning language is now developed, and is defined in
Vision/meaning.md; that supersedes the postponement stated above.
````

### Proposal 7: A new type is written as its value · psyche-context › vision/datom.md

Follows Proposal 5. Reject it, and a new type is written as a struct of one position, `{ Ada }`. Rule: land, amend or reject.

+ A new type is written as the value it wraps: a `Name` reads `Ada`, never `{ Ada }`.

```datom
+ { Ada 1990 }
```
