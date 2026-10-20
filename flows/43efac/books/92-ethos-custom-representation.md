<!-- to-the-living:start -->
Presentation.{ «Ethos: the open enum, second edition — a custom representation» }

# Ethos: the open enum, second edition — a custom representation

## psyche-context › vision/ethos.md

````markdown
## Ethos and Nexus are infrastructure

Ethos and Nexus are basic infrastructure, not examples: the wood houses are built from. Chronos is the example project built with them, short term.

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
Type.CommitMessage.[ Landing.⟦String⟧
                     Fix.String ]
```

## Imports

An import starts with a colon, followed by uncapitalized namespace segments separated by colons, ending in the type: `:namespace:sub:Type`. It is usable inline in a type declaration or a field, and the import section uses the same syntax: `:protos:String`, or `:protos:[ String Integer ]` for several. An explicit import and an intrinsic name mean the same thing. The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized.

```
Library
[ :protos:[ String Textualizable ]   ; imports
  :datom:Datom ]
[ Record.{ String Datom } ]          ; types: Datom, imported
[]                                   ; traits
[ Record.[ Textualizable ] ]         ; associations: Textualizable, imported
```

The generated code carries no `use` statements; each imported name is
written fully qualified: `:protos:String` appears as `protos::String`,
`:datom:Datom` as `datom::Datom`.

An import may stand where the type is used, with no entry in the imports section. In a declaration the colon replaces the dot: `Topic:custom:Name` declares `Topic` over the type `Name` from the namespace `custom`. A field takes the import with its leading colon: `Failure.{ :protos:Error String }`. The colon marks the import; the namespace segments are uncapitalized and the type is capitalized.

```
Library
[]                              ; imports
[ Topic:custom:Name             ; an alias, inline
  Failure.{ :protos:Error       ; a field, inline
            String } ]
[]                              ; traits
[]                              ; associations
```

```
+--------------------------------------------+
| the registry                               |
+--------------------------------------------+
                      |
                      | holds uncapitalized segments
                      v
+--------------------------------------------+
| :namespace:sub                             |
+--------------------------------------------+
                      |
                      | ends in the type
                      v
+--------------------------------------------+
| :namespace:sub:Type                        |
+--------------------------------------------+
         |                          |
         | listed in                | written in
         v                          v
+-------------------+  +---------------------+
| the import        |  | a declaration or    |
| section           |  | a field, inline     |
+-------------------+  +---------------------+
```

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

## White braces define a struct

White braces define a struct, so a struct definition looks different from a struct value. The definition, in ethos, names the types of its positions inside white braces; the value, in datom, fills them inside plain braces.

```
Library
[]                              ; imports
[ LockId.Integer                ; types
  LockName.String
  Lock.⦃ LockId LockName ⦄ ]    ; a definition
[]                              ; traits
[]                              ; associations
```
```
{ 7 renew }
```

```
+--------------------------------------------+
| a struct                                   |
+--------------------------------------------+
         |                          |
         | is defined in            | is filled in
         v                          v
+-------------------+  +---------------------+
| white braces,     |  | plain braces,       |
| in ethos          |  | in datom            |
+-------------------+  +---------------------+
```

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

## An open enum

An open enum is an Ethos object whose capitalized words are its fixed variants. A word that is not capitalized is its implied extensible variant, a camel ID: a word-based camel-case identifier, written bare, with no variant head before it. The name camel ID is temporary. A check that a word is a word-based camel-case identifier comes long term; short term, none is made.

The metaflow topic is an open enum: its fixed variants are a constant set, such as the core topic, and the users or the machine extend it with camel IDs as they need topics.

The same mechanism carries an object that is represented unconventionally, such as a word-based hash.

```
+--------------------------------------------+
| a word in an open enum's position          |
+--------------------------------------------+
        |                        |
        | capitalized            | uncapitalized
        v                        v
+----------------+     +---------------------+
| fixed variant  |     | camel ID            |
+----------------+     +---------------------+
        |                        |
        |                        | is checked
        |                        | long term as
        |                        v
        |             +---------------------+
        |             | word-based          |
        |             | camel-case          |
        |             | identifier          |
        |             +---------------------+
        | is a                   | is a
        v                        v
+--------------------------------------------+
| value of the open enum                     |
+--------------------------------------------+
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
Signal's first two sections, an alias in the types section. An enum
declaration is a vector of its variants, and uses the vector's
delimiters. Ethos may generate default implementations for Query and
Response, which is why Signal is its own root.

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

## White square brackets define a vector

White square brackets around an item type define a vector type, replacing the word Vector, which is so common: `⟦String⟧` is the vector of String. The vector value keeps its plain brackets in datom.

```
+--------------------------------------------+
| a vector type                              |
+--------------------------------------------+
         |                          |
         | was written as           | is written as
         v                          v
+-------------------+  +---------------------+
| the word Vector   |  | white square        |
| and angle         |  | brackets around     |
| brackets          |  | the item type       |
+-------------------+  +---------------------+
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

### Proposal 1: psyche-context › vision/ethos.md

- An open enum is an Ethos object whose capitalized words are its fixed variants. A word that is not capitalized is its implied extensible variant, a camel ID: a word-based camel-case identifier, written bare, with no variant head before it. The name camel ID is temporary. A check that a word is a word-based camel-case identifier comes long term; short term, none is made.
+ An open enum is an Ethos enum whose fixed variants are capitalized, with one more variant, the custom variant, that takes a String. A word that is not capitalized is that custom variant, a camel ID: a word-based camel-case identifier, written bare, with no variant head before it. The name camel ID is temporary. A check that a word is a word-based camel-case identifier comes long term; short term, none is made.

  The metaflow topic is an open enum: its fixed variants are a constant set, such as the core topic, and the users or the machine extend it with camel IDs as they need topics.

- The same mechanism carries an object that is represented unconventionally, such as a word-based hash.
+ The same mechanism carries an object that is represented unconventionally, such as a word-based hash, through a trait.
+
+ ## An unusually represented type
+
+ A type may write and read its own datom form in place of the generated one; it is unusually represented. A trait says so. It is declared in Ethos like any trait and associated with the type, and the logic is hand-written Rust. The trait's working name is UnusuallyRepresented.
+
+ When the type is made into a datom, the generated code asks the trait first: the trait gives the datom form, or declines, and the generated code writes what it declines. When a datom is read as the type, the generated code offers the trait the datom first: the trait gives the value or a refusal, or declines, and the generated code reads what it declines. A type with fixed variants keeps the generated form of its fixed variants, and the trait holds only the rest.
+
+ The trait refuses the generated form of the values it writes, so a value has one spelling. The trait is the one place where a rule on a form is kept, such as that a word is a camel ID.
+
+ The custom variant of an open enum is the first use: the trait writes it as its bare word and reads a bare uncapitalized word as that variant. A flow id kept as the first bits of its harness id and written as three words is another. A digest or a revision written as its hexadecimal digits, a latitude read only within its range, and bytes written as hexadecimal digits are others.
+
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

### Proposal 2: mind-context › inquiry/ethos-representation-trait-name.md, a new file

+ ---
+ description: The name of the trait through which a type writes and reads its own datom form is unresolved.
+ ---
+
+ ## The name of the trait
+
+ What is the trait named, through which a type writes and reads its own datom form? The living's working name is unusually represented. Ethos names a trait by a quality of the type that bears it: Runnable, Textualizable, Structural, Embodied. What would settle it: the living choosing one name, then the vision, the Ethos file and the Rust trait all using it; the Rust name and the Ethos name are one. Every proposal of this book uses the working name, and a ruling renames it everywhere. The alternatives:
+
+ - Alternative a: UnusuallyRepresented, the working name. It says that the type's representation is the exception to the generated one.
+ - Alternative b: SelfRepresenting. It says that the type represents itself: it holds the logic of its own writing and reading.
+ - Alternative c: CustomDatomizable. It says that the type is a Datomizable with custom logic, naming the datom step it replaces.
+ - Alternative d: RepresentationOverriding. It says that the type overrides the representation Ethos generates for it.
+ - Alternative e: SelfSpelling. It says that the type spells itself, the way a camel ID or a word-based hash is spelled.

### Proposal 3: datom-codec › datom-codec-unusual.ethos, a new file

```ethos
+ ; What a datom shows to a type that reads it, and
+ ; the type that writes and reads its own datom.
+ Library
+ [ crate:[ Datom Form ErrorKind ] ] ; imports
+ [] ; types
+ [ Formed.[ form.[ Form ] ] ; the form of a datom
+   UnusuallyRepresented.[
+     unusual_form.[ Option<Form> ] ; to write
+     from_unusual_form:{ ; to read
+       [ Formed ]
+       [ Option<Result<Self ErrorKind>> ] } ] ]
+ [ Datom.[ Formed ] ] ; associations
```

### Proposal 4: datom-codec › src/unusual.rs, a new file

```rust
+ //! A type that writes and reads its own datom.
+
+ use crate::{Datom, ErrorKind, Form};
+
+ /// What a datom shows to a type that reads it.
+ pub trait Formed {
+     fn form(&self) -> Form;
+ }
+
+ /// A type whose datom is not the generated one.
+ /// The derive asks it first, both ways; a `None`
+ /// hands the datom to the generated code.
+ pub trait UnusuallyRepresented {
+     fn unusual_form(&self) -> Option<Form>;
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>>
+     where
+         Self: Sized;
+ }
+
+ impl Formed for Datom {
+     fn form(&self) -> Form {
+         self.form.clone()
+     }
+ }
+
+ impl Formed for &Datom {
+     fn form(&self) -> Form {
+         self.form.clone()
+     }
+ }
+
+ /// How a type's own reading refuses.
+ pub trait Refusing {
+     fn refused_value(
+         expected: &str,
+         text: String,
+     ) -> Self;
+     fn refused_form(
+         expected: &str,
+         found: &Form,
+     ) -> Self;
+ }
+
+ impl Refusing for ErrorKind {
+     fn refused_value(
+         expected: &str,
+         text: String,
+     ) -> Self {
+         Self::Value {
+             expected: expected.into(),
+             value: text,
+         }
+     }
+
+     fn refused_form(
+         expected: &str,
+         found: &Form,
+     ) -> Self {
+         let found = match found {
+             Form::Struct(_) => "Struct",
+             Form::Vector(_) => "Vector",
+             Form::Variant(..) => "Variant",
+             Form::Bare(_) => "Bare",
+             Form::String(_) => "String",
+             Form::Meaning(_) => "Meaning",
+         };
+         Self::Form {
+             expected: expected.into(),
+             found: found.into(),
+         }
+     }
+ }
```

### Proposal 5: datom-codec › src/lib.rs

```rust
  mod projection;
+ mod unusual;

  pub use protos::Symbol;
+ pub use unusual::{
+     Formed, Refusing, UnusuallyRepresented,
+ };
```

### Proposal 6: datom-codec › crates/datom-codec-derive/src/unusual.rs, a new file

```rust
+ //! The statements a type marked
+ //! `#[datom(unusually_represented)]` is given.
+ //! `reading` is spliced first in each generated
+ //! `compose`, `writing` first in each `datomize`;
+ //! for an unmarked type each is empty.
+
+ use proc_macro2::TokenStream;
+ use quote::quote;
+ use syn::DeriveInput;
+
+ const MARK: &str = "unusually_represented";
+
+ fn marked(input: &DeriveInput) -> bool {
+     input.attrs.iter().any(|attribute| {
+         attribute.path().is_ident("datom")
+             && attribute
+                 .parse_nested_meta(|meta| {
+                     match meta.path.is_ident(MARK)
+                     {
+                         true => Ok(()),
+                         false => {
+                             Err(meta.error("?"))
+                         }
+                     }
+                 })
+                 .is_ok()
+     })
+ }
+
+ /// First in `compose`: ask the type to read.
+ pub fn reading(
+     input: &DeriveInput,
+ ) -> TokenStream {
+     if !marked(input) {
+         return quote!();
+     }
+     quote! {
+         if let Some(read) = <Self as
+             ::datom_codec::UnusuallyRepresented>
+             ::from_unusual_form(datom)
+         {
+             use ::datom_codec::Budgeted;
+             budget.spend(&datom.path)?;
+             return read.map_err(|kind| {
+                 <::datom_codec::Error as
+                     ::datom_codec::ErrorRaising>
+                     ::composition(
+                         datom.path.clone(), kind)
+             });
+         }
+     }
+ }
+
+ /// First in `datomize`: ask the type to write.
+ pub fn writing(
+     input: &DeriveInput,
+ ) -> TokenStream {
+     if !marked(input) {
+         return quote!();
+     }
+     quote! {
+         if let Some(form) =
+             ::datom_codec::UnusuallyRepresented
+                 ::unusual_form(self)
+         {
+             return ::datom_codec::Datom {
+                 path: at,
+                 form,
+             };
+         }
+     }
+ }
```

### Proposal 7: datom-codec › crates/datom-codec-derive/src/lib.rs

```rust
+ mod unusual;

- #[proc_macro_derive(Composing)]
+ #[proc_macro_derive(
+     Composing,
+     attributes(datom)
+ )]

      let name = &input.ident;
+     let asked = unusual::reading(&input);

+                     #asked
                      match &datom.form {

+                 #asked

- #[proc_macro_derive(Datomizable)]
+ #[proc_macro_derive(
+     Datomizable,
+     attributes(datom)
+ )]

      let name = &input.ident;
+     let asked = unusual::writing(&input);

+                     #asked
                      match self { #(#arms),* }

+                 #asked
```

### Proposal 8: ethos-zero › src/generation.rs

```rust
      ) -> TokenStream;
  }

+ /// The trait whose association marks a type as
+ /// unusually represented: its datom derives ask
+ /// that trait first, both ways.
+ const UNUSUALLY_REPRESENTED: &str =
+     "UnusuallyRepresented";
+
+ /// Whether a trait reference names the trait
+ /// called [`UNUSUALLY_REPRESENTED`]: qualified in
+ /// place, imported by the name its source gives
+ /// it, or declared in the file.
+ trait Representing {
+     fn names_unusual_representation(
+         &self,
+         file: &File,
+     ) -> bool;
+ }
+
+ impl Representing for Reference {
+     fn names_unusual_representation(
+         &self,
+         file: &File,
+     ) -> bool {
+         let named = match (
+             &self.source,
+             file.resolve(&self.name),
+         ) {
+             (Some(_), _) => self.name.clone(),
+             (
+                 None,
+                 Resolution::Imported(_, emitted),
+             ) => emitted,
+             (None, Resolution::Trait(name)) => {
+                 name
+             }
+             (None, _) => return false,
+         };
+         named.as_ref() == UNUSUALLY_REPRESENTED
+     }
+ }
+
+ /// Whether a Library associates a type with the
+ /// trait called [`UNUSUALLY_REPRESENTED`].
+ trait UnusuallyRepresenting {
+     fn unusually_represented(
+         &self,
+         file: &File,
+     ) -> bool;
+ }
+
+ impl UnusuallyRepresenting for Identity {
+     fn unusually_represented(
+         &self,
+         file: &File,
+     ) -> bool {
+         let File::Library(library) = file else {
+             return false;
+         };
+         for association in &library.associations {
+             if association.identity.name
+                 != self.name
+             {
+                 continue;
+             }
+             for trait_reference in
+                 &association.traits
+             {
+                 if trait_reference
+                     .names_unusual_representation(
+                         file,
+                     )
+                 {
+                     return true;
+                 }
+             }
+         }
+         false
+     }
+ }
+
  trait DatomDeriving {
-     fn datom_derives(&self) -> TokenStream;
+     fn datom_derives(
+         &self,
+         file: &File,
+     ) -> TokenStream;
  }

  /// while violating the schema's invariants.
+ ///
+ /// A type its Library associates with
+ /// `UnusuallyRepresented` also bears
+ /// `datom(unusually_represented)` behind the same
+ /// feature: the datom derives ask that trait
+ /// first.
  impl DatomDeriving for Identity {
-     fn datom_derives(&self) -> TokenStream {
+     fn datom_derives(
+         &self,
+         file: &File,
+     ) -> TokenStream {
+         let unusual = if self
+             .unusually_represented(file)
+         {
+             quote! {
+                 #[cfg_attr(
+                     feature = "datom",
+                     datom(unusually_represented)
+                 )]
+             }
+         } else {
+             TokenStream::new()
+         };
          quote! {
              #[rustfmt::skip]
+             #unusual
          }
      }
  }

          }
          let fields =
              references.field_names(owner);
-         let derive = identity.datom_derives();
+         let derive =
+             identity.datom_derives(scope.file);
          let bounds = if recursive {
              identity.recursion_bounds()
          } else {

          let name = identity.name.tokens();
          let parameters =
              identity.parameters(scope);
-         let derive = identity.datom_derives();
+         let derive =
+             identity.datom_derives(scope.file);
          let mut definitions =
              Vec::with_capacity(self.len());
          let mut nested = Vec::new();
```

### Proposal 9: datom-codec › examples/unusual/topic.ethos, a new file

```ethos
+ ; A Topic that is open: fixed variants, and a
+ ; Custom variant that holds a camel ID.
+ Library
+ [ datom_codec:UnusuallyRepresented ] ; imports
+ [ Aspect.[ Psyche ; sees: the living's side
+            Mind ; implements what Psyche sees
+            Field ] ; the tools, via Mind
+   Topic.[ Core ; the permanent topic
+           Ethos ; the topic about Ethos
+           Custom.String ] ; any other: camel ID
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ] ; decides the model
+   Address.{ Aspect Topic Layer } ] ; types
+ [] ; traits: the one used is imported
+ [ Topic.[ UnusuallyRepresented ] ] ; associations
```

```datom
+ ; without the trait
+ ; read, and written back the same
+ { Psyche Core Secondary }
+ ; read, and written back the same
+ { Psyche Custom.flowDesign Secondary }
+ ; refused: flowDesign is no variant of Topic
+ { Psyche flowDesign Secondary }
```
```datom
+ ; with the trait
+ ; read, and written back the same
+ { Psyche Core Secondary }
+ ; read as Custom, written back the same
+ { Psyche flowDesign Secondary }
+ ; refused: the head Custom is not written
+ { Psyche Custom.flowDesign Secondary }
+ ; refused: not a camel ID
+ { Psyche flow_design Secondary }
+ ; refused: FlowDesign is no variant
+ { Psyche FlowDesign Secondary }
```
```
+--------------------------------------------+
| the registry                               |
+--------------------------------------------+
                      |
                      | holds uncapitalized segments
                      v
+--------------------------------------------+
| :namespace:sub                             |
+--------------------------------------------+
                      |
                      | ends in the type
                      v
+--------------------------------------------+
| :namespace:sub:Type                        |
+--------------------------------------------+
         |                          |
         | listed in                | written in
         v                          v
+-------------------+  +---------------------+
| the import        |  | a declaration or    |
| section           |  | a field, inline     |
+-------------------+  +---------------------+
```

### Proposal 10: datom-codec › examples/unusual/topic/represented.rs, a new file

```rust
+ use datom_codec::{
+     ErrorKind, Form, Formed, Refusing, Symbol,
+     UnusuallyRepresented,
+ };
+
+ use super::generated::Topic;
+
+ impl Topic {
+     // A word that begins with a lowercase letter.
+     fn is_lowercase(word: &str) -> bool {
+         word.chars().next().is_some_and(|c| {
+             c.is_ascii_lowercase()
+         })
+     }
+
+     // A camel ID: that, then letters and digits.
+     // The first check; the long-term check, of
+     // words, would replace it here.
+     fn is_camel_id(word: &str) -> bool {
+         Topic::is_lowercase(word)
+             && word.chars().all(|c| {
+                 c.is_ascii_alphanumeric()
+             })
+     }
+
+     fn from_word(
+         word: String,
+     ) -> Result<Self, ErrorKind> {
+         match Topic::is_camel_id(&word) {
+             true => Ok(Topic::Custom(word)),
+             false => {
+                 let kind = "camel ID";
+                 Err(ErrorKind::refused_value(
+                     kind, word,
+                 ))
+             }
+         }
+     }
+ }
+
+ impl UnusuallyRepresented for Topic {
+     // Written: a Custom topic is its camel ID.
+     // Core and Ethos stay generated.
+     fn unusual_form(&self) -> Option<Form> {
+         match self {
+             Topic::Custom(word)
+                 if Topic::is_camel_id(word) =>
+             {
+                 Some(Form::Bare(word.clone()))
+             }
+             _ => None,
+         }
+     }
+
+     // Read: a lowercase bare word is Custom.
+     // The old head, Custom.word, is refused. Any
+     // other form is left to the generated code.
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>> {
+         match input.form() {
+             Form::Bare(word)
+                 if Topic::is_lowercase(&word) =>
+             {
+                 Some(Topic::from_word(word))
+             }
+             Form::Variant(Symbol(head), _)
+                 if head == "Custom" =>
+             {
+                 Some(Err(ErrorKind::Variant {
+                     expected: "Topic".into(),
+                     found: head,
+                 }))
+             }
+             _ => None,
+         }
+     }
+ }
```

### Proposal 11: datom-codec › examples/unusual/flow_id.ethos, a new file

```ethos
+ ; A flow id kept as the first 33 bits of its
+ ; harness id, and written as three words.
+ Library
+ [ datom_codec:UnusuallyRepresented ] ; imports
+ [ Layer.[ Primary Secondary Tertiary
+           Quaternary ] ; decides the model
+   FlowId.{ Integer } ; the 33 bits, as an integer
+   Seat.{ Layer FlowId } ] ; a flow's layer, id
+ [] ; traits: the one used is imported
+ [ FlowId.[ UnusuallyRepresented ] ] ; associations
```

```datom
+ ; without the trait
+ ; read: a struct holds the integer
+ { Secondary { 2050 } }
+ ; refused: words are no struct
+ { Secondary abandonAbilityAble }
```
```datom
+ ; with the trait
+ ; read: 2050, the indexes 0, 1 and 2
+ { Secondary abandonAbilityAble }
+ ; read: 2^33 - 1, the greatest id
+ { Secondary zooZooZoo }
+ ; refused: the struct form
+ { Secondary { 2050 } }
+ ; refused: two words
+ { Secondary abandonAbility }
+ ; refused: four words
+ { Secondary abandonAbilityAbleAbout }
+ ; refused: notAWord is not in the list
+ { Secondary notAWord }
+ ; refused: it begins with a capital
+ { Secondary AbandonAbilityAble }
```
```
+--------------------------------------------+
| a struct                                   |
+--------------------------------------------+
         |                          |
         | is defined in            | is filled in
         v                          v
+-------------------+  +---------------------+
| white braces,     |  | plain braces,       |
| in ethos          |  | in datom            |
+-------------------+  +---------------------+
```

### Proposal 12: datom-codec › examples/unusual/flow_id/represented.rs, a new file

```rust
+ use std::sync::OnceLock;
+
+ use datom_codec::{
+     ErrorKind, Form, Formed, Refusing,
+     UnusuallyRepresented,
+ };
+
+ use super::generated::FlowId;
+
+ // BIP-39 English, 2048 words, one a line;
+ // SHA-256 2f5eed53...b24dbda.
+ const LIST: &str =
+     include_str!("bip39-english.txt");
+
+ impl FlowId {
+     const BITS: u32 = 33;
+
+     fn words() -> &'static Vec<&'static str> {
+         static WORDS: OnceLock<Vec<&str>> =
+             OnceLock::new();
+         WORDS.get_or_init(|| {
+             LIST.lines().collect()
+         })
+     }
+
+     // Three 11-bit groups, high bits first, as
+     // camel case: abandonAbilityAble is 2050.
+     fn spell(&self) -> Option<String> {
+         let bits =
+             u64::try_from(self.integer).ok()?;
+         if bits >> Self::BITS != 0 {
+             return None;
+         }
+         let mut spelled = String::new();
+         for shift in [22, 11, 0] {
+             let index = (bits >> shift) & 0x7ff;
+             let word =
+                 Self::words()[index as usize];
+             if spelled.is_empty() {
+                 spelled.push_str(word);
+             } else {
+                 spelled.push_str(
+                     &word[..1].to_uppercase(),
+                 );
+                 spelled.push_str(&word[1..]);
+             }
+         }
+         Some(spelled)
+     }
+
+     // The reverse: split at each capital, look
+     // each word up, and join the three indexes.
+     fn unspell(text: &str) -> Option<Self> {
+         let mut words: Vec<String> = Vec::new();
+         for letter in text.chars() {
+             if letter.is_ascii_uppercase()
+                 || words.is_empty()
+             {
+                 words.push(String::new());
+             }
+             words.last_mut()?.push(
+                 letter.to_ascii_lowercase(),
+             );
+         }
+         let list = Self::words();
+         let first = text.chars().next()?;
+         if words.len() != 3
+             || !first.is_ascii_lowercase()
+         {
+             return None;
+         }
+         let mut bits = 0i64;
+         for word in &words {
+             let index = list
+                 .binary_search(&word.as_str())
+                 .ok()?;
+             bits = bits << 11 | index as i64;
+         }
+         Some(FlowId { integer: bits })
+     }
+ }
+
+ impl UnusuallyRepresented for FlowId {
+     // Written: the words, if the integer is 33
+     // bits. Otherwise the generated form, which
+     // cannot be read back.
+     fn unusual_form(&self) -> Option<Form> {
+         self.spell().map(Form::Bare)
+     }
+
+     // Read: only three known words. Any other
+     // form, the generated struct, is refused.
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>> {
+         Some(match input.form() {
+             Form::Bare(text) => FlowId::unspell(
+                 &text,
+             )
+             .ok_or(ErrorKind::refused_value(
+                 "three BIP-39 words",
+                 text,
+             )),
+             other => {
+                 Err(ErrorKind::refused_form(
+                     "Bare", &other,
+                 ))
+             }
+         })
+     }
+ }
```

### Proposal 13: datom-codec › examples/unusual/revision.ethos, a new file

```ethos
+ ; A git revision, written as its 40 lowercase
+ ; hex digits and read only if it is one.
+ Library
+ [ datom_codec:UnusuallyRepresented ] ; imports
+ [ Revision.{ String } ; the 40 hex digits
+   Pin.{ Name.String Revision } ] ; types
+ [] ; traits: the one used is imported
+ [ Revision.[ UnusuallyRepresented ] ]
```

```datom
+ ; without the trait
+ ; read: a struct holds the digits
+ { datomCodec
+   { 4dff16b4f7412febc3b71aac8b49680cd20988cb } }
+ ; refused: digits are no struct
+ { datomCodec
+   4dff16b4f7412febc3b71aac8b49680cd20988cb }
```
```datom
+ ; with the trait
+ ; read, and written back the same
+ { datomCodec
+   4dff16b4f7412febc3b71aac8b49680cd20988cb }
+ ; refused: the struct form
+ { datomCodec
+   { 4dff16b4f7412febc3b71aac8b49680cd20988cb } }
+ ; refused: uppercase digits
+ { datomCodec
+   4DFF16B4F7412FEBC3B71AAC8B49680CD20988CB }
+ ; refused: seven digits, not forty
+ { datomCodec 4dff16b }
```

### Proposal 14: datom-codec › examples/unusual/revision/represented.rs, a new file

```rust
+ use datom_codec::{
+     ErrorKind, Form, Formed, Refusing,
+     UnusuallyRepresented,
+ };
+
+ use super::generated::Revision;
+
+ impl Revision {
+     // Forty lowercase hexadecimal digits.
+     fn is_revision(text: &str) -> bool {
+         text.len() == 40
+             && text.chars().all(|c| {
+                 c.is_ascii_digit()
+                     || ('a'..='f').contains(&c)
+             })
+     }
+ }
+
+ impl UnusuallyRepresented for Revision {
+     // Written: the digits, bare, if a revision.
+     fn unusual_form(&self) -> Option<Form> {
+         Revision::is_revision(&self.string).then(
+             || Form::Bare(self.string.clone()),
+         )
+     }
+
+     // Read: only a bare revision. The generated
+     // struct form is refused.
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>> {
+         Some(match input.form() {
+             Form::Bare(text)
+                 if Revision::is_revision(
+                     &text,
+                 ) =>
+             {
+                 Ok(Revision { string: text })
+             }
+             Form::Bare(text) => {
+                 Err(ErrorKind::refused_value(
+                     "Revision", text,
+                 ))
+             }
+             other => {
+                 Err(ErrorKind::refused_form(
+                     "Bare", &other,
+                 ))
+             }
+         })
+     }
+ }
```

### Proposal 15: datom-codec › examples/unusual/latitude.ethos, a new file

```ethos
+ ; A latitude in degrees, read only inside the
+ ; range -90 to 90.
+ Library
+ [ datom_codec:UnusuallyRepresented ] ; imports
+ [ Latitude.{ Decimal } ; degrees north
+   Place.{ Name.String Latitude } ] ; types
+ [] ; traits: the one used is imported
+ [ Latitude.[ UnusuallyRepresented ] ]
```

```datom
+ ; without the trait
+ ; read: a struct holds the decimal
+ { Greenwich { 51.5 } }
+ ; refused: a bare decimal is no struct
+ { Greenwich 51.5 }
+ ; read: nothing bounds the range
+ { Nowhere { 123.4 } }
```
```datom
+ ; with the trait
+ ; read, and written back the same
+ { Greenwich 51.5 }
+ ; read, negative
+ { Wellington -41.3 }
+ ; read: the pole is inside the range
+ { Pole 90.0 }
+ ; refused: 123.4 is outside -90 to 90
+ { Nowhere 123.4 }
+ ; refused: the struct form
+ { Greenwich { 51.5 } }
+ ; refused: 51 is no decimal
+ { Greenwich 51 }
```

### Proposal 16: datom-codec › examples/unusual/latitude/represented.rs, a new file

```rust
+ use datom_codec::{
+     Decimal, Decimating, ErrorKind, Form, Formed,
+     Refusing, Symbol, UnusuallyRepresented,
+ };
+
+ use super::generated::Latitude;
+
+ impl Latitude {
+     fn in_range(decimal: &Decimal) -> bool {
+         (-90.0..=90.0).contains(&decimal.float())
+     }
+
+     fn read(
+         text: String,
+     ) -> Result<Self, ErrorKind> {
+         match text.parse::<Decimal>() {
+             Ok(decimal)
+                 if Self::in_range(&decimal) =>
+             {
+                 Ok(Latitude { decimal })
+             }
+             _ => Err(ErrorKind::refused_value(
+                 "Latitude, -90 to 90",
+                 text,
+             )),
+         }
+     }
+
+     // 51.5 is the head 51 over the bare 5.
+     fn text(
+         form: &Form,
+     ) -> Result<String, ErrorKind> {
+         match form {
+             Form::Bare(text) => Ok(text.clone()),
+             Form::Variant(
+                 Symbol(whole),
+                 part,
+             ) => match &part.form {
+                 Form::Bare(rest) => {
+                     Ok(format!("{whole}.{rest}"))
+                 }
+                 other => {
+                     Err(ErrorKind::refused_form(
+                         "Bare", other,
+                     ))
+                 }
+             },
+             other => {
+                 Err(ErrorKind::refused_form(
+                     "Decimal", other,
+                 ))
+             }
+         }
+     }
+ }
+
+ impl UnusuallyRepresented for Latitude {
+     // Written: the decimal, bare, if in range.
+     fn unusual_form(&self) -> Option<Form> {
+         let decimal = &self.decimal;
+         if Latitude::in_range(decimal) {
+             Some(Form::Bare(decimal.to_string()))
+         } else {
+             None
+         }
+     }
+
+     // Read: join the text, read the decimal, then
+     // check the range. Other forms are refused.
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>> {
+         Some(
+             Latitude::text(&input.form())
+                 .and_then(Latitude::read),
+         )
+     }
+ }
```

### Proposal 17: datom-codec › examples/unusual/octets.ethos, a new file

```ethos
+ ; Bytes, written as hex digits, two to a byte,
+ ; and read only if each pair is one byte.
+ Library
+ [ datom_codec:UnusuallyRepresented ] ; imports
+ [ Octets.{ Vector<Integer> } ; each integer a byte
+   Keypress.{ Name.String Octets } ] ; types
+ [] ; traits: the one used is imported
+ [ Octets.[ UnusuallyRepresented ] ] ; associations
```

```datom
+ ; without the trait
+ ; read, and written back the same
+ { UpArrow { [ 27 91 65 ] } }
+ ; read: nothing bounds a byte
+ { Bad { [ 27 300 65 ] } }
+ ; refused: hex digits are no struct
+ { UpArrow 1b5b41 }
```
```datom
+ ; with the trait
+ ; read: 27, 91 and 65, written back
+ { UpArrow 1b5b41 }
+ ; read: no bytes at all
+ { Empty «» }
+ ; refused: the struct form
+ { UpArrow { [ 27 91 65 ] } }
+ ; refused: an odd number of digits
+ { Odd 1b5 }
+ ; refused: zz are no hex digits
+ { NotHex zz }
```

### Proposal 18: datom-codec › examples/unusual/octets/represented.rs, a new file

```rust
+ use datom_codec::{
+     ErrorKind, Form, Formed, Refusing,
+     UnusuallyRepresented,
+ };
+
+ use super::generated::Octets;
+
+ impl Octets {
+     // One byte as two hex digits, or None.
+     fn hex(byte: i64) -> Option<String> {
+         u8::try_from(byte)
+             .ok()
+             .map(|byte| format!("{byte:02x}"))
+     }
+
+     // Two hex digits to a byte, all through.
+     fn unhex(text: &str) -> Option<Vec<i64>> {
+         if text.len() % 2 != 0 || !text.is_ascii()
+         {
+             return None;
+         }
+         (0..text.len())
+             .step_by(2)
+             .map(|at| {
+                 let pair = &text[at..at + 2];
+                 i64::from_str_radix(pair, 16).ok()
+             })
+             .collect()
+     }
+
+     fn read(
+         text: String,
+     ) -> Result<Self, ErrorKind> {
+         match Octets::unhex(&text) {
+             Some(bytes) => Ok(Octets {
+                 integer_vector: bytes,
+             }),
+             None => {
+                 let kind = "hex bytes";
+                 Err(ErrorKind::refused_value(
+                     kind, text,
+                 ))
+             }
+         }
+     }
+ }
+
+ impl UnusuallyRepresented for Octets {
+     // Written: hex, bare; no bytes at all is «».
+     fn unusual_form(&self) -> Option<Form> {
+         let digits: String = self
+             .integer_vector
+             .iter()
+             .map(|byte| Octets::hex(*byte))
+             .collect::<Option<_>>()?;
+         Some(if digits.is_empty() {
+             Form::String(digits)
+         } else {
+             Form::Bare(digits)
+         })
+     }
+
+     // Read: a bare even run of hex digits, or «».
+     fn from_unusual_form<N: Formed>(
+         input: N,
+     ) -> Option<Result<Self, ErrorKind>> {
+         Some(match input.form() {
+             Form::String(text)
+                 if text.is_empty() =>
+             {
+                 Ok(Octets {
+                     integer_vector: vec![],
+                 })
+             }
+             Form::Bare(text) => {
+                 Octets::read(text)
+             }
+             other => {
+                 Err(ErrorKind::refused_form(
+                     "Bare", &other,
+                 ))
+             }
+         })
+     }
+ }
```

### Proposal 19: mind-context › knowledge/ethos-layers.md, a new file

+ ---
+ description: The layers Ethos is made of, and how each reads an enum, a variant and a capital letter today, is needed to place a change.
+ dependencies: [knowledge-ethos, knowledge-datom, knowledge-protos]
+ ---
+
+ ## The layers, as the code stands
+
+ Witnessed in protos main 15b41da (0.32.2), ethos-zero main 07714b0 (17.0.0) and datom-codec main 4dff16b, read, not run, except where a line says it was run.
+
+ Ethos text is read by ethos-zero and becomes a Rust type; the type's derive, from datom-codec, reads and writes datom text through protos. Ethos-zero is the bootstrap and the generator in one crate: canonicalization, protosization, conception, checking and generation are its passes. Datom-codec is the Datom reader and writer. No registry of types exists in these repositories; the only registry in code is Curriculum's registry of skills.
+
```
+--------------------------------------------+
| a word in an open enum's position          |
+--------------------------------------------+
        |                        |
        | capitalized            | uncapitalized
        v                        v
+----------------+     +---------------------+
| fixed variant  |     | camel ID            |
+----------------+     +---------------------+
        |                        |
        |                        | is checked
        |                        | long term as
        |                        v
        |             +---------------------+
        |             | word-based          |
        |             | camel-case          |
        |             | identifier          |
        |             +---------------------+
        | is a                   | is a
        v                        v
+--------------------------------------------+
| value of the open enum                     |
+--------------------------------------------+
```
+
+ ## Capital letters today
+
+ Protos has no test of case: a run with a separator becomes a headed structure, any other run a bare one. Datom-codec's step from Protos to the Datom form is case-blind too. Case is read only by the type that composes the form: a derived enum matches a bare form against its unit variants by their exact spelling, and routes any other form to its payload variants by spelling.
+
+ Ethos-zero requires a capital letter on the name of a declared type or trait, and on no variant. Run against ethos-zero 07714b0: an enum `Topic.[ core ethos ]` is checked and accepted; a type named `topic` is rejected with Case.topic.
+
+ An alias is a Rust alias, transparent, never a new type: `Topic.String` is a `String`. A type reaches a custom text form through a hand-written reader and writer of its own, as Decimal has, or through an import of a Rust type that has one.
+
+ ## Topic and flow id today
+
+ Flow's library declares `Topic.String`; the camel-case check on a topic is a comment there ("check camelCase at input"), and no check in Rust was found. A flow id is `FlowId.String`; the title code accepts six characters, each a hexadecimal digit. A word-based id is a design in the records and in no code on main.
+
+ ## Syntax on a branch
+
+ The white braces and white square brackets are landed in vision/ethos.md; ethos-zero main does not parse them. They are on the branch ethos-proposals of ethos-zero, protos and datom-codec. The Ethos code of this book uses the brackets and braces that main parses.

### Proposal 20: mind-context › knowledge/ethos-datomization.md, a new file

+ ---
+ description: How a type becomes a datom and a datom a type, and where a type's own representation hooks in, is needed to place or judge a custom datom form.
+ dependencies: [knowledge-ethos, knowledge-datom, knowledge-protos]
+ ---
+
+ ## Witnessed
+
+ datom-codec main 4dff16b, protos main 15b41da, ethos-zero main 07714b0 (17.0.0). Read, except the hook, which was built and run in scratch copies: datom-codec with the hook, 48 existing tests passing; ethos-zero with the hook, its tests, clippy and no-free-function checks passing.
+
+ ## Reading
+
+ - Datom text is read by Protos, formed into a Datom, then composed into the type: `Composing::compose(datom, budget)`. A Datom is a path and a Form. A Form is Struct, Vector, Variant(Symbol, Datom), Bare(String), String(String) or Meaning.
+ - A period-headed run is a Variant. `51.5` arrives as Variant(51, Bare 5); `Core` as Bare; `Custom.flowDesign` as Variant(Custom, Bare flowDesign). The Datom form refuses angle enclosures and qualified heads.
+ - A derived struct checks its arity, then reads its positions in order. A one-position struct is not transparent: `{ hello }`.
+ - A derived enum matches a Bare form against its unit variants by exact spelling, and any other form against its payload variants by head. The last arm refuses with ErrorKind::Variant. A unit variant written with a payload, and a payload variant written bare, are refused.
+ - Leaf types are read by hand in datom-codec: String (Bare, or guillemets when empty, spaced or delimited), i64 (no plus sign, no leading zero), bool (True, False), Vec, Option (Some., None), Result, Box, tuples to twelve, Meaning, Decimal (a point is required; joined from Variant(whole, Bare fraction)). The protos types Extent, Symbol, ReaderBudget, Separator, Problem and Error are written by hand too.
+
+ ## Writing
+
+ - A value is datomized to a Datom, protosized, then textualized. A unit variant is Bare(name), a payload variant Variant(name, body), a struct Struct of its positions.
+ - Writing cannot fail: `datomize` returns a Datom, not a Result.
+
+ ## Where a representation is decided
+
+ - In the two derives of datom-codec-derive, Datomizable and Composing. Ethos-zero emits the types and one derive attribute and emits no impl of either trait. Before the hook, no attribute, trait or registry changed a representation: the derives declared no helper attribute.
+ - An alias is a Rust alias: it takes its target's form and carries no derive. The live Ethos files on main declare 689 intrinsic aliases, none checked by its type (String 481, Integer 181, Boolean 14, Decimal 5, Vector<Integer> 7, Vector<String> 1). A check sits in a comment or in a consumer's code. Counted by a scan of origin main of about 220 repositories, not compiled.
+ - One way to a hand-written form exists: import a Rust type that has its own impls, as Decimal and Meaning are intrinsics and protos:Extent is imported. Ethos then cannot show the type's variants.
+ - The traits Datomizable and Composing declared in datom-codec-kinds.ethos are an anatomy: the crate's own traits take concrete Path, Datom and Budget, and its generated kinds file is not compiled.
+
+ ## The hook
+
+ - UnusuallyRepresented has `unusual_form(&self) -> Option<Form>` and `from_unusual_form(Formed) -> Option<Result<Self, ErrorKind>>`. Formed gives the Form of a Datom. A None declines to the generated code.
+ - A type is marked `#[cfg_attr(feature = "datom", datom(unusually_represented))]`. Ethos-zero emits it for a type its Library associates with the trait. The two derives then add one statement first in `compose` and one first in `datomize`.
+ - Run: Topic, FlowId, Revision, Latitude and Octets, each read and written with and without the trait.
+ - Seen: a value the trait declines is written in the generated form, which the trait's reader then refuses, such as a FlowId of 2^33 written `{ 8589934592 }`. The trait is consulted for every datom of its type, so a reader returns None for forms it does not own. The trait is per type, not per position. A marked type without the impl does not compile.
+
```
+--------------------------------------------+
| a vector type                              |
+--------------------------------------------+
         |                          |
         | was written as           | is written as
         v                          v
+-------------------+  +---------------------+
| the word Vector   |  | white square        |
| and angle         |  | brackets around     |
| brackets          |  | the item type       |
+-------------------+  +---------------------+
```

### Proposal 21: mind-context › inquiry/ethos-open-enum-layer.md, a new file

+ ---
+ description: Whether the open enum is a convention of the custom variant and the trait or a kind of enum that Ethos declares, and whether a registry is a layer, is unresolved.
+ ---
+
+ ## At which layer the open enum lands
+
+ This book lands the open enum in the derive: an enum with a custom variant that takes a String, and a trait that the derive asks first, so that a bare word is the custom variant. Nothing in the Ethos object says that the enum is open or which variant is the custom one; that is the name Custom by convention and the logic of the trait's implementation. What would settle it: one open enum, the Topic of the metaflow address, taken through each alternative to the datom `{ Psyche flowDesign Secondary }` and back, and the work each needed counted. Alternative c was taken so, in scratch, in proposals 3 to 9. The alternatives:
+
+ - Alternative a, the reader. Protos or the Datom form tells a capitalized word from another, so the Datom form gains a kind for an identifier. It touches the Datom form and every composition that reads a bare form, and protos, which several dialects share, would learn the Ethos rule of case.
+ - Alternative b, the type system. Ethos-zero's declaration gains a kind of enum that is open and names its custom variant, so that the definition says in Ethos what the enum is. Its model, conception, checking and generation change.
+ - Alternative c, the derive asking the trait, as this book proposes. The custom variant is an ordinary variant; the Ethos object does not say that it is open.
+ - Alternative d, an imported type. A Rust type with its own reader and writer is imported into the library, as Decimal is. Ethos cannot show the fixed variants of the type.
+
+ ## The registry as a layer
+
+ The living counts a registry among the layers. In the code read, it is not a layer of Ethos. Does a camel ID need a registry: the set of topics a user or the machine has created, kept somewhere, so that a topic is checked when it is created? Alternative a: the check is of form only, and the set of live topics is Flow's memory. Alternative b: the open enum's extensions are recorded in the registry the library is addressed by.

### Proposal 22: mind-context › inquiry/ethos-open-enum.md, a new file

+ ---
+ description: The name of the camel ID, how a word is checked, the constant topics, and what a hash is to an open enum are unresolved.
+ ---
+
+ ## The final name of the camel ID
+
+ What is the final name of the camel ID? The living calls it temporary. Three names for one idea stand in the context today: a camelCase identifier (vision flow), a camelCaseExpression of the type core:Name (vision flow), and camel ID. What would settle it: the living choosing one name, then every module using it. The alternatives:
+
+ - Alternative a: keep camel ID.
+ - Alternative b: word ID, which names what it is made of, as the word-based hash does.
+ - Alternative c: open variant, which names the place it takes in the enum.
+ - Alternative d: camelCaseExpression, the name already in the Flow vision.
+
+ ## How a word is checked
+
+ The landed vision says that short term no check is made. The trait is where the check lives, and the Topic example carries a first one: a lowercase first letter, then letters and digits. Which words, from which list; whether a digit or an acronym is allowed; whether the check is a form only or a membership of a word list. Alternative a: no check beyond a lowercase first letter, which tells a camel ID from a fixed variant. Alternative b: the first check of the example. Alternative c: the long-term check of words.
+
+ ## The constant topics: Core or core
+
+ The living wrote the constant topic as `core`, uncapitalized, and defined a fixed variant as capitalized. Run against the Topic example, `Core` is the fixed variant and a bare `core` is read as the custom topic `core`: one name, two values. Alternative a: the constants are fixed variants, and the trait refuses a camel ID that spells a fixed variant in lowercase, so that `core` is refused. Alternative b: the constants are fixed variants and `core` is a second spelling the set accepts as the custom topic. Alternative c: no fixed variant; every topic is custom and `core` is a reserved word of the set.
+
+ ## What a hash is to an open enum
+
+ A word-based hash has no fixed variant and no custom variant. With the trait it is not an open enum but a type that the trait represents, as FlowId is. Is that the end of the idea of a hash as an open enum with an empty set of fixed variants? And does a fixed variant of an open enum ever carry a payload? The derive reads it, as Labelled.Point; the trait declines the forms it does not own.

### Proposal 23: mind-context › inquiry/ethos-custom-representation.md, a new file

+ ---
+ description: Whether an unusual form can refuse in writing, and the choices of the word-based flow id and of each usage are unresolved.
+ ---
+
+ ## Whether writing can refuse
+
+ Writing gives a form or declines; it cannot fail. A value the trait declines, such as a flow id of 2^33 or more, a byte of 300 or a Custom topic that holds Core, is written in the generated form, which the trait's reader refuses. What would settle it: a case where such a value arises. The alternatives:
+
+ - Alternative a: unusual_form returns Option<Result<Form, ErrorKind>> and Datomizable gains a fallible twin, touching every writer.
+ - Alternative b: a value is valid at construction, by a constructor that checks and a field that is not public, which Ethos cannot declare on main.
+ - Alternative c: leave it. The generated form is written, and the reader refuses it, so no wrong value is read silently.
+
+ ## When the trait is consulted
+
+ Every datom of a marked type is offered to the trait first. Alternative a: that, so the old spelling Custom.flowDesign is refused. Alternative b: the trait is consulted only after the generated reading refuses, which accepts Custom.flowDesign as a second spelling of the same topic.
+
+ ## Where the trait is declared
+
+ The trait is declared in a new Ethos file of datom-codec, and its Rust is written by hand from the generated text, as the kinds file's Rust is not compiled. Alternative a: the new file. Alternative b: the trait joins datom-codec-kinds.ethos. Alternative c: the trait is generated into the crate by ethos-zero.
+
+ ## The word-based flow id
+
+ - The words: the example runs BIP-39 English, 2048 words, 11 bits a word, the list pinned by its SHA-256. The living asked for a denser list; a 1024-word list of single-token words was researched and not built, giving 10 bits a word. No ruling is recorded.
+ - The count: three words make 33 bits. The living said maybe two.
+ - The representation: the example holds the 33 bits as an Integer in a struct. The living said the id is a hash, not an integer. Alternative a: the integer in a struct. Alternative b: bytes. Alternative c: an opaque hash intrinsic.
+ - The bits: for Claude the first 33 bits of the session UUID, for Codex the random tail from hex index 23; for OpenCode, unruled.
+ - A clash: two sessions with the same words are an Ambiguous reply, never a guess, and are no part of the datom form.
+ - The six-hex alias: the words replace it wherever a flow is named, or stand beside it.
+
+ ## The other usages
+
+ - Digests and revisions: 29 hash and digest aliases are Strings with at most a check in a consumer, most of them 64 hexadecimal digits. The example shows a 40-digit revision, as a 64-digit digest does not fit a phone. Which of the aliases become unusually represented types?
+ - Latitude: chronos holds a hand-written Latitude on an older datom pin, and horizon declares Latitude as an unchecked Decimal. Which hosts the checked type?
+ - Bytes: eleven alias names carry bytes as Vector<Integer>, written `[ 27 91 65 ]`, with no range check. The hex form changes the terminal wire.
+ - Not drawn here: timestamps in four representations, session UUIDs, keys and signatures of unknown encoding, version numbers, and paging cursors. What would settle it: the living naming which of these to draw.
<!-- to-the-living:end -->
