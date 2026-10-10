# Ethos design: starting context

Topic: Ethos and Datom, the Protos stack (protos, datom-codec, ethos-zero).
Assembled 2026-10-09 for flow d4ae97 from files read that day. The partner
topic flow is Nexus design; its context is
`/home/li/primary/flows/d4ae97/reports/topic-nexus/context.md`.

How to read this file:

- Section 1 quotes the distilled, approved psyche: the vision- and intent-
  skills, from their authored sources (psyche-skills at 4312cc0). Each skill
  is quoted whole except its front matter and its `## Sources` list; headings
  are lowered two levels to fit this file, and the text is otherwise exact.
  `/home/li/primary/Vision/ethos.md` is an older copy of vision-ethos (its
  Roots line still reads "Library, Signal, Sema") and is not quoted.
- Section 2 quotes the knowledge- skills: the machine-written description of
  what runs today (mind-skills at 37ca3f7). It is a claim, not the living's
  word.
- Section 3 quotes raw psyche records that are newer than the skills or say
  what the skills do not, verbatim with their record headings, oldest first.
  Records marked notion are the living thinking aloud. Bracketed words and
  [sic] marks are the logging flow's, as logged.
- Section 4 lists where a raw record contradicts or moves past a skill.
- Section 5 lists the open questions and the books awaiting his rulings.
- Section 6 lists what was cut.

The order for this flow is logged only for Nexus
(`flows/d4ae97/vision/messenger.md`, 2026-10-09, quoted in the Nexus file).
The words "Ethos and Datom, like the Proto stack" come from the brief this
file was assembled under; no record holding them was found.

## 1. Distilled statements (vision- and intent- skills)

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-ethos.md`

#### What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

Ethos is central. The anatomy of the system, every type and every kind
it uses, is read in its ethos; an implementation is mostly the
hand-written bodies.

#### Why Ethos

All the legacy languages have a high noise ratio. Some lisps came
close but lacked the correctness of Rust or Haskell; those have the
correctness but allow no higher layer of abstraction that keeps the
correctness of the whole. Ethos writes the mental model and the code
in one swoop.

#### Roots

Library, Signal, Operation, Memory. No version in a file. Signal's sections are
queries and responses, since there is communication; Sema's are record
types, the rest to be decided. Signal gives a Nexus its main types and
Sema its database types.

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory kind carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

#### Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

Terseness is in the low amount of noise, never in shortened words.

#### Self-description

A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object —
CLI now, Mentci later — and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.

#### Horizon

Ethos will eventually replace everything, Rustlang becoming its
assembly layer. Designs are chosen for that horizon; what it
enables — generator emission among it — comes in its time.

#### Kind

Kind is the word for the bearer of capabilities: something that can
run is a runner, Runnable is its kind, and run is its capability, a
function the kind has. Trait is set aside as acoustically ambiguous.
In ethos there are no generics, only kinds. Declaring a new kind
declares a new trait in the Rust world and might imply more in the
ethos world.

A capability speaks in Self, the kind's own parameters and other kinds; a concrete type in an input is a kind not yet named.

#### Naming

Kinds are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a kind. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

#### Identity

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
Library
[ std:[ Clonable Sendable Serializable ] ]                  ; imports: where the three constraint kinds come from
[]                                                          ; types
[ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; kinds: the head is the identity, the name and two
                                                            ;   constraints, the first a bracket of two kinds, the
                                                            ;   second one kind; the bracket after the dot holds
                                                            ;   its capabilities, its definition
[]                                                          ; associations
```
```rust
// The trait's identity: its name and its constraints, two generic parameters with their bounds.
// What ethos writes as the bounds alone, Rust writes as a named parameter carrying them;
// the parameter names are Rust's need, not the kind's.
pub trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
```

#### Declaration: File

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

A Library's sections, in order, are imports, types, kinds and
associations. Every root's first section is its imports; its own
sections follow.

```
; the sweet form, as a file is written: the head, then the sections as siblings
Library
[ protos:String ]               ; imports
[ Record.{ String Integer } ]   ; types
[]                              ; kinds
[]                              ; associations

; the canonical form the reader sees, after the mechanical conversion
Library.{
  [ protos:String ]
  [ Record.{ String Integer } ]
  []
  []
}
```

#### Imports

An import names a source and a type: `protos:String` or
`protos:[ String Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

```
Library
[ protos:[ String Textualizable ]  datom:Datom ]   ; imports
[]                                                 ; types
[]                                                 ; kinds
[]                                                 ; associations
```

The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.

#### What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom kinds through the derive, which Ethos Zero emits with the type.
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
[]                                            ; kinds
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

#### Inline types

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
[]                                                       ; kinds
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

#### A variant named as a defined type carries that type

When a variant's name is a type already defined in the library, that
type is the data the variant carries. Nothing further is written.

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: FilePath is an alias of String
  SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
  GenerationFailure.[ SyntaxError          ;        an enum: the variant SyntaxError is bare here,
                      Unwritable ] ]       ;        but SyntaxError is a defined type, so it carries one
[]                                         ; kinds
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

#### A variant may declare its payload inline

Instead of naming a defined type, a variant may declare what it
carries in place: a vector, a struct, or an enum, each a full type
with a derived name, recursively.

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   declared inline: a struct, derived name
[]                                                        ; kinds
[]                                                        ; associations
```
```rust
pub type FilePath = String;
#[derive(Datomizable, Compositional)]
pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(Vec<FilePath>), Unwritable(Unwritable_Data) }
```

#### Every declared type bears both kinds

Ethos Zero emits `Datomizable` and `Compositional` on every struct and
enum it generates, so every ethos-declared type always bears both
kinds and no declared type can exist without them. An alias bears them
through the type it names: an alias is not a new type and cannot carry
a derive.

```rust
pub type FilePath = String;                  // an alias: String already bears both
pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
#[derive(Datomizable, Compositional)]        // a type: always derived
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

#### The datom kinds are compiled in only where text is spoken

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

#### Shapes and placement

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

#### Kinds are explicit; bodies are hand-written

A kind is declared, never inferred; an association asserts the type
bears it. The generated Rust carries a compile-time assertion that the
type bears the kind; the interaction body is hand-written Rust.

```
Library
[]                                                ; imports
[ Record.{ String Integer } ]                     ; types
[ Summarizable.[ summarize.[ String ] ] ]         ; kinds
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

#### Kind syntax

A simple kind opens with a bracket after the dot. Its capabilities sit
inside. The receiver after a capability's head names who is called:
`.` takes self, `!` takes mutable self, `:` takes no self. A
capability with inputs is a headed brace: inputs in a bracket, yield
in a bracket. A yield bracket holds one type.

```
Library
[]                                                            ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; kinds
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

A complex kind opens with a brace after the dot. Inside: superkinds in
a bracket, associated types with their constraints in a bracket,
associated constants in a bracket — upper case, each the name, a dot,
and its type — and capabilities in a bracket.

```
Library
[ std:Serializable ]                                ; imports
[]                                                  ; types
[ Fillable.[ create:[ Self ] ]                      ; kinds
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

A kind's identity is its name and its constraints, as stated in the
Identity section above.

#### Associations

An association declares that a type bears a kind: the type's name, a
dot, a bracket of its kinds. In the Signal and Sema roots the
associations of the query, response and record types are implied and
never written. In a Library they are the fourth section, after the
kinds.

```
Library
[]                                                       ; imports
[ Sink.{ String Integer } ]                              ; types
[ Summarizable.[ summarize.[ String ] ]                  ; kinds
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

#### Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.

#### Zero

Ethos Zero was first named Ethos Monolith; the two are the same thing.
Zero as in version 0: no daemon yet, no Nexus. The ethos repository is
for the ethos nexus that follows.

#### Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-datom.md`

#### Name

Datom is the psyche’s own coinage for the new data notation, the
successor to NOTA and to the rejected name Dotos. The name was
chosen for its energetic power and to echo what the notation is:
data, strictly typed, super dense, no field names. The library is
datom-codec. Datomic names the conceptual layer abstractly; it is
not a term of the code.

#### Nature

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

#### A datom is a form at a path

```rust
pub struct Datom { pub path: Path, pub form: Form }
pub enum Form { Struct(Vec<Datom>), Vector(Vec<Datom>), Variant(Symbol, Box<Datom>), Bare(String), String(String), Meaning(Opaque) }
```

#### Strings

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

#### Syntax

Structure is the word for every unit of the text: enclosed when it
stands between its delimiters, unenclosed when bare. A headed
structure is a head, a separator and a body; the dot is the separator,
written right after the head, and it opens the body's delimiter. A
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

#### The datom composes; the type states its positions

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

#### Any Rust type

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

#### From text and back

A potential, text that may become a T, owns the budget and actualizes
by the descent written once: protosize, datomize, compose. A
composition becomes text by the open chain.

```rust
let query: Query = Potential::<Query>::from(text).actualize(budget)?;
let out = response.datomize(Path::root()).protosize().textualize();
```

#### Containers

Vector, Option, Result, Box bear the kinds once, generically; Option
and Result read as ordinary variants.

```
[ Some.42 None ]     Ok.{ Ada 1990 }     Err.«no such lock»
```

#### Errors

An error names the layer that raised it and the path of the datom
where it arose; the extent is the protos node at that path. An error
is itself datomizable.

```
[ 1 x ]                                  ; read as Vector<Integer>
Corporate.{ [ 1 ] Value.x }              ; at path 1, the bare string x is not an integer
```

#### Omittable fields

Not yet; a written datom gives every position.

```
Deploy.{ ouranos }     ; Arity.{ 2 1 }
```

#### The interface shape

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

#### De/serialization

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

#### Relation to Ethos

Datom and Ethos are different languages that share an approach, not a
parser. What they may share is a substrate, kinds with a shared
implementation and types; the universal substrate machinery is homed
in protos, all dialects ride it, and datom is the pure-data dialect on
it. Ethos could come to depend on Datom for another reason: ethos
might be read as datom in one pass. Whether that is even possible,
given the situation and the actualization involved in parsing ethos,
is not settled, and the question is set aside for now.

#### Repository

Everything moves to Datom: all of the stack, Horizon, Lojix, everything;
no Dotos file remains. Datom's own line of descent is NOTA, which also
passed through the temporary name Dotos; that old notation stays
behind, frozen, and may be called legacy. Schema is the abandoned
ancestor of Ethos, not of Datom. The library is named datom-codec so
that datom is free for the datom nexus, which comes when there is more
to do: translating datom objects between formats, and a parsing cache
keyed by the content-addressed hash of normalized text.

#### Map

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

#### Meaning

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

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-protos.md`

#### What Protos is

Protos is the name for the style all the dialects share. The
context-switching parse, the delimiters, the heads, the recursive
structure — this is the code that can be shared between all parsers
and belongs in protos. Datom is a protos dialect, carrying only
pure typed data; it does not take part in the multi-pass
rust-generation engine that ethos, nomos and logos are slated to
become, but it shares the protos style. The final fully-decomposed
engine with three daemons is the protos engine.

#### What Protos knows

Protos is only about structure. It has nothing to do with struct and
vector, and it only understands form: the syntactic structure. It
would not know what anything is. A head in protos is just a head —
anatomy, not interpretation. Pure anatomy is only structural
recognition of structures, nothing more. Protos examples show the
textual structure — the delimiters, the head, the capitalization, the
recursive structure — universally, at a very high level,
non-dialect-specific.

#### Layers

Four layers, text above and the value below: the textual layer; the
protosic layer, whose root type is the `Protos` enum; the conceptual
layer, which is the datomic, ethosic, logosic, or nomosic layer
according to the language; and the compositional layer, the
composition, the value put together in memory, the densest form.
Going down, the information gains density and strictness; going up,
visibility. Each step converts into a wholly different type, and
nothing of the previous step is used after it.

```
; textual: these characters, uninterpreted
{ Ada 1990 }
```
```rust
// protosic: an enclosure of two bare runs, each structure at its extent in the text
Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])
// conceptual, here datomic: a struct of two positions, each datom at its path
Datom { path: [], form: Form::Struct(vec![Datom { path: [0], form: Form::Bare("Ada") }, Datom { path: [1], form: Form::Bare("1990") }]) }
// compositional: the meaning fully absorbed; no position, because the tree is consumed
Person { name: String::from("Ada"), born: 1990 }
```

#### Every layer carries its own context

A value at a layer contains the context it makes sense in, in both
directions, and no layer carries a fact that belongs to another. The
extent, where a structure sits in the text, is a fact of the protosic
layer, and every `Protos` node carries one. The path, where a datom
sits in its tree, is a fact of the datomic layer, and every datom
carries one, read down from text or built up from a composition
alike. The budget, how much reading one act allows, is a fact of the
reader and lives on it. The composition carries no position: it is
the layer where context has been consumed. There is no site and no
situated pair; an error's locus is the datom's path, and its extent
is found by following that path into the protos the reader holds.

#### Kinds are borne by the type converted and named for the layer it becomes

No type bears a kind two layers away. A chain is written in the open
where it is used, never folded into a kind on its first type.

| type | kind | becomes |
|---|---|---|
| text | `Protosizable` | protos |
| `Protos` | `Textualizable` | text |
| `Protos` | `Datomizable`, or `Ethosizable` further on | its concept |
| `Datom` | `Protosizable` | protos |
| `Datom` | `Composable` | any compositional type |
| composition | `Datomizable` | datom |
| composition | `Compositional` | states its own positions, so a datom can compose it |

```rust
impl Protosizable  for String { fn protosize(&self) -> Result<Protos, Error>; }
impl Textualizable for Protos { fn textualize(&self) -> String; }
impl Datomizable   for Protos { fn datomize(&self) -> Result<Datom, Error>; }
impl Protosizable  for Datom  { fn protosize(&self) -> Protos; }
impl Composable    for Datom  { fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
impl Datomizable   for Person { fn datomize(&self, at: Path) -> Datom; }
impl Compositional for Person { const ARITY: Integer; fn from_positions(p: Positions<'_>) -> Result<Self, Error>; }

let text = person.datomize(Path::root()).protosize().textualize();
```

#### Signal is parallel

Signal is not a layer of the chain: a parallel structure exchanging
compositions in one step, an rkyv serialization carrying our own
protocol.

#### Delimiters

Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph
content; `( )` reserved for meaning, its type unspecified, read by
balance as opaque until it is. The curly quotes are not delimiters.
Every structure of the protosic layer is a variant of the `Protos`
enum, and none of them means anything on its own: whether an
enclosure is a struct or a vector, whether a bare run is a name or a
number, is said by the conceptual layer that reads it.

```rust
Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])   // structure: an enclosure of two runs
Datom::Struct(vec![Datom::Bare("Ada"), Datom::Bare("1990")])                // meaning: a struct of two positions
```

#### Structure

Structure is the word for every unit of the text; its type is the
`Protos` enum: headed, enclosed, opaque, or bare.

A headed structure is a head, a separator and a body. The separators
are period, exclamation and colon. The head is a symbol. The body is
another structure. Heads may be daisy-chained: different separators
too.

An enclosed structure stands between its delimiters; a bare structure
has no delimiters. A brace-enclosed structure's arity is anatomical;
a bracket-enclosed structure's arity is not. Angle brackets are a
real protos delimiter. The key-value map, which the guillemets once
delimited, is dropped entirely from protos and its dialects.

#### String, escape, error

The text type is `String`. A closing guillemet inside a string is
escaped with a backslash, so the ascent never refuses. The word is
error, not fault, through the chain.

```
«she said \»no\» and left»
```

#### Multi-pass

Multiple passes are wanted over a single pass, because a single pass
creates corner-cutting bad design. The multiple steps create a mental
model of the machinery, which enforces a correctness in the code that
is millions of times more beneficial than the cost of doing these
multiple passes.

#### Canonical print

It is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except inside the guillemets,
where every glyph is content and a space would be load-bearing. Space
the delimiters and the inner content.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-anatomy.md`

#### Code is written anatomically

Code is written anatomically and directly: the logic is read through
the ontology of the trait system. Datom and Ethos Zero are the parts
that must be solid.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-protos-parsing.md`

Protos parsing always happens inside a context, and only the
current context gives shapes their meaning: it defines which
shapes can appear next and which shape completes it. A met shape
announces a type, and that type's context takes over completely
until its completing shape; then the parent context resumes
exactly where it left off. Reading and writing are one walk in
two directions — text lands in typed values, and typed values
project back into the same text.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-data.md`

Everything is data. Code is data: a type is declared with code, so
a type is data; a trait is data; an impl is data. "Code", "type",
"check", "configuration" are not kinds of being — they are roles
data plays for an interpreter, and an interpreter is just another
program, so it too is data. There is one plane; nothing stands
above it. Protolanguages make this obvious by being a data
notation before they are anything else.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-conversion.md`

#### A kind names one conversion

A kind names one conversion and is borne by the type that undergoes
it, named for the layer it becomes. Each step yields a wholly new
type. A chain is composed in the open, never folded into a kind on its
first type.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-context.md`

#### Every layer carries its own context

A value at any layer carries the context it makes sense in, and no
layer carries a fact that belongs to another.

### `/git/github.com/LiGoldragon/psyche-skills/skills/intent-mandatory-traits.md`

#### 2026-08-13 — approved

> Every method call in our Rust code lives under a trait, because
> traits are the comprehension surface — the layer where concepts
> become visible and implementations are constrained to think within
> them. Rust is the new assembly language: no serious engineer reads
> all the assembly, and the same is happening to Rust. Traits and
> main types are what the psyche reads; everything else is
> implementation detail that Ethos will eventually generate.

— psyche-approved wording, 2026-08-13 (Steward session d2bb5f5f).
Proposed by Steward, approved with "otherwise its good, implement
commit and deploy."

## 2. Machine-written description of what runs today (knowledge- skills)

Written by machines; a claim about the current code, not the living's word.

### `/git/github.com/LiGoldragon/mind-skills/skills/knowledge-ethos.md`

As of 16.0.0 ethos-zero reads four roots: Library, Signal, Operation, Memory. The sweet form, root head then sections as siblings, is converted to the canonical braced form before reading. Section order: Library imports, types, kinds, associations; Signal imports, queries, responses, types; Operation imports, operations, outcomes, types, proposed and pending the living's word; Memory imports, record types. A Signal generates `pub enum Query` and `pub enum Response`, an Operation `pub enum Operation` and `pub enum Outcome`, from the two sections after imports. A file headed `Sema`, Memory's head before 15.0.0, is refused as `Conceptual.{ [ 0 ] Renamed.Memory }`.

The canonical print is vertical: a structure with more than one element, one of which has a next layer, opens on its line and its elements hang aligned beneath the first; the closer ends the last line; a space inside every non-empty bracket and brace, `[]` and `{}` empty, angles tight (`Vector<Event>`). protos owns it as `Textualizable::textualize`; the one-line form is `Compactable::compact`, which the command-line replies use.

`Name.Type` is an alias, `Name.{ }` a struct, `Name.[ ]` an enum. A field is named after its type in snake case, `string_vector`, `lock_option`, `first_lock` and `second_lock` when repeated. An inline struct or enum payload generates a Rust type named `<Variant>_Data`; a vector payload is carried as the vector, with no `_Data`. A struct position may declare its type in place, `Brief.String`, `State.[ Running Ended ]`, `Capsule.{ Home.String Login.Vector<String> }`: the type takes that name in the file's namespace and the position holds it by name (`brief: Brief`). Imports are `protos:String` or `protos:[ String Integer ]`; intrinsics need none: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

A simple kind is `Name.[ capabilities ]`; receivers `.` self, `!` mutable self, `:` none; a capability with inputs is `push!{ [ inputs ] [ yield ] }`; a complex kind is `Name.{ [ superkinds ] [ associated types ] [ CONSTANTS ] [ capabilities ] }`. A kind in an input or yield becomes a method parameter bounded by it, lettered from `N` (`fn resolve<N: Textualizable>(&self, input: N)`), or `Self::Item` where an associated type is already bounded by that kind (`Item<Textualizable>`). Self, the kind's head parameters and a named associated type stay as written. A concrete type in an input (`String`, `Vector<Self>`, a declared type) is refused with `KindWanted`; a yield may name one. An imported name is taken as a kind in an input and as a type in a yield.

protos and datom-codec generate their kinds files from their own ethos, with the kinds Spendable (protos), Branchable, Budgeted, Positional and Composable (datom-codec).

In every root each generated struct and enum derives rkyv's Archive, Serialize and Deserialize, Clone, Debug, PartialEq, Eq and Hash, and its Datomizable and Composing sit behind a `knowledge-datom` feature that the CLI enables and the Nexus does not. A crate holding generated Rust depends on rkyv 0.8 always and on datom-codec only under `knowledge-datom`; where a position holds a `Decimal`, a `Meaning` or a datom-codec `Error`, it enables datom-codec 0.32.2's `rkyv` feature, which enables protos's, unconditionally. An alias carries no derive. A generated file opens with `#![allow(dead_code, non_camel_case_types, non_snake_case)]`, every item carries `#[rustfmt::skip]`, names are fully qualified with no `use`. Generated Rust is committed and held fresh by a test. An association generates a compile-time assertion; the interaction body is hand-written.

```
ethos-zero 'Generate.{ /abs/flow.ethos /abs/out }'
Generated.[ /abs/out/flow.rs ]

ethos-zero 'Check./abs/flow.ethos'
Checked./abs/flow.ethos
```

A refused file answers `Rejected.{ file { line column } reason }`, the reason naming the path within the file (`Conceptual.{ [ path ] KindWanted.Path }`), and a rejected Generate writes nothing. With no argument ethos-zero prints its own ethos in the canonical print.

### `/git/github.com/LiGoldragon/mind-skills/skills/knowledge-datom.md`

Datom is the pure-data dialect on the protos substrate: data, strictly typed, super dense, no field names. Its whole work is carrying data between text and typed form. Schema-driven and positional: the reader walks the expected type, writing is the exact reverse projection. All naming lives in the type; the text carries only the data. The library is datom-codec.

#### A datom is a form at a path

```rust
pub struct Datom { pub path: Path, pub form: Form }
pub enum Form { Struct(Vec<Datom>), Vector(Vec<Datom>), Variant(Symbol, Box<Datom>), Bare(String), String(String), Meaning(Opaque) }
```

#### Syntax

A brace structure is a struct, a bracket structure is a vector, and a head in front of a structure is a variant carrying it. In datom a head is always a variant, so it is capitalized. A symbol alone, in a position expecting an enum, is a variant carrying nothing; a variant's name is written as the head every time, one carrying nothing included. Guillemets are the string delimiter and parentheses are reserved for Meaning. A datom is not preceded by a Datom root. What a structure means — struct, vector, string, integer, variant — is said by the position it sits in, never by the structure alone.

A string has two forms: bare, a run with no space and no delimiter glyph, which may be a whole sentence written without spaces in any casing; and guillemets, where every glyph is content until the closing guillemet, which is escaped with a backslash where it is content. Because the position already knows it holds a string, a bare run may carry characters that are syntax elsewhere, the colon among them. An integer is bare ASCII decimal, no leading plus and no leading zero except `0` itself. A decimal is finite and point-mandatory. Today a parenthesized text lands as a plain String, with the Meaning type marked in code.

There is no map. What a map would hold is a struct when its keys are fixed, and a vector of structs when they are not.

```
; datom, in a position expecting Person: a struct of name String, born Integer, address Address, roles Vector<Role>.
{ Ada 1990 { «12 Rue de la Paix» Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }

; Reply: an enum of Accepted.{ id Integer  at String }, Refused.{ reason String  code Integer }, Pending
Accepted.{ 42 2026-09-03T17:46:20 }          ; the timestamp has no space and no delimiter, so it is bare
Refused.{ «no such file: { } is content» 2 } ; delimited: the string has spaces and braces; inside the guillemets they are content
Pending                                      ; a variant carrying nothing

[ 0 42 -42 ]                                 ; a vector of Integer
Observed.Locks.[]                            ; the Observed variant, its Locks variant, the empty vector
[ Some.42 None ]   Ok.{ Ada 1990 }   Err.«no such lock»   ; Vector, Option and Result read as ordinary variants
```

#### The datom composes; the type states its positions

The descent into a composition is the datom's act, written once. What only the type can supply, its positions in order, is stated by the type through the derive, so arity, budget and locus live in one place and no type repeats them.

```rust
pub trait Composable {
    fn compose<T: Composing>(&self, budget: &mut Budget) -> Result<T, Error>;
    fn compose_positions<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>;
}
pub trait Composing: Sized { fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>; }
pub trait Compositional: Composing { const ARITY: Integer; fn from_positions(positions: Positions<'_>) -> Result<Self, Error>; }
pub trait Datomizable { fn datomize(&self, at: Path) -> Datom; }
```

#### Any Rust type

Any Rust type bears the two kinds through datom-codec's derive, with no attributes, because datom is structural all the way down: field order is position order, a field's type is the position's type, a bare variant carries nothing, a single-field variant carries its type's own form, a multi-field variant carries an inline struct. Hand-written impls are reserved to the intrinsics.

```rust
#[derive(datom_codec::Datomizable, datom_codec::Composing)]
pub struct Locus { pub path: Path, pub extent: Extent }

impl Compositional for Locus {                              // generated: the positions, in order
    const ARITY: Integer = 2;
    fn from_positions(mut positions: Positions<'_>) -> Result<Self, Error> {
        Ok(Self { path: positions.position()?, extent: positions.position()? })
    }
}
impl Composing for Locus {                                  // generated: the datom reads, spending the budget
    fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error> {
        datom.compose_positions(budget)
    }
}
impl Datomizable for Locus {                                // generated: each child placed as the tree is built
    fn datomize(&self, at: Path) -> Datom {
        Datom { path: at.clone(), form: Form::Struct(vec![self.path.datomize(at.child(0)), self.extent.datomize(at.child(1))]) }
    }
}
```

#### From text and back

```rust
let query: Query = Potential::<Query>::from(text).actualize(&mut budget)?;
let out = response.datomize(Path::new()).protosize().textualize();
```

#### Errors

An error names the layer that raised it and the path of the datom where it arose; the extent is the protos node at that path. An error is itself datomizable.

```
[ 1 x ]                                  ; read as Vector<Integer>
Error.{ Composition [ 1 ] Value.{ Integer x } }   ; at path 1, the bare string x is not an integer
```

#### The interface shape

A program's configuration surface is the datom's shape itself: a data enum at the root whose variants are the main operations, a variant's data carrying what follows. Output is an enum, always. A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, never as a datom file.

```sh
orchestrate 'Lock.{ MyLock 6329f1 [ /abs/path ] «why I hold it» }'
# -> Locked.{ 442 MyLock 6329f1 [ /abs/path ] «why I hold it» }
```

A written datom gives every position; omittable fields are not yet.

#### A datom needs a type

A datom is written only against a type that already exists. When none exists, the type is declared first, in Ethos through the vision-ethos skill; there is no ad hoc datom and no field label standing in for a type.

### `/git/github.com/LiGoldragon/mind-skills/skills/knowledge-protos.md`

Protos is the style every dialect shares: the context-switching parse, the delimiters, the heads, the recursive structure. It owns the only character reader and the only character writer. It knows form and nothing else: what a structure means — struct, vector, string, integer, variant — is said by the conceptual layer that reads it, never by protos.

#### Four layers

Textual, protosic, conceptual, compositional. Going down, the information gains density and strictness; going up, visibility. Each step converts into a wholly different type, and nothing of the previous step is used after it. Implement the descent as multiple passes; a single pass is not an option.

```
; textual: these characters, uninterpreted
{ Ada 1990 }
```
```rust
// protosic: an enclosure of two bare runs, each structure at its extent in the text
Protos::Enclosed { extent: Extent { start: 0, end: 12 }, enclosure: Braced, children: vec![
    Protos::Bare { extent: Extent { start: 2, end: 5 }, text: "Ada".to_owned() },
    Protos::Bare { extent: Extent { start: 6, end: 10 }, text: "1990".to_owned() } ] }
// conceptual, here datomic: a struct of two positions, each datom at its path
Datom { path: vec![], form: Form::Struct(vec![
    Datom { path: vec![0], form: Form::Bare("Ada".to_owned()) },
    Datom { path: vec![1], form: Form::Bare("1990".to_owned()) } ]) }
// compositional: the meaning fully absorbed; no position, because the tree is consumed
Person { name: String::from("Ada"), born: 1990 }
```

#### Delimiters

Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph content; `( )` reserved for meaning, its type unspecified, read by balance as opaque until it is. The curly quotes are not delimiters. There is no key-value map in protos or in any dialect. A brace enclosure's arity is anatomical; a bracket enclosure's is not.

#### Structure

Structure is the word for every unit of the text; its type is the `Protos` enum: headed, enclosed, opaque, or bare. A headed structure is a head, a separator and a body; the separators are period, exclamation and colon; the head is a symbol; heads daisy-chain, separators differing. An enclosed structure stands between its delimiters; a bare structure has none.

#### Every layer carries its own context

The extent, where a structure sits in the text, is a fact of the protosic layer, and every `Protos` node carries one. The path, where a datom sits in its tree, is a fact of the datomic layer. The budget, how much reading one act allows, is a fact of the reader and lives on it. The composition carries no position.

#### Kinds

A kind is borne by the type converted and named for the layer it becomes. No type bears a kind two layers away; a chain is written in the open where it is used, never folded into a kind on its first type.

| type | kind | becomes |
|---|---|---|
| text | `Protosizable` | protos |
| `Protos` | `Textualizable` | text |
| `Protos` | `Datomizable`, or `Ethosizable` further on | its concept |
| `Datom` | `Protosizable` | protos |
| `Datom` | `Composable` | any compositional type |
| composition | `Datomizable` | datom |
| composition | `Composing` | read from a datom; a struct form states its positions through `Compositional` |

```rust
pub enum Protos {
    Headed { extent: Extent, head: Symbol, constraints: Option<Box<Protos>>, separator: Separator, body: Box<Protos> },
    Enclosed { extent: Extent, enclosure: Enclosure, children: Vec<Protos> },
    Opaque { extent: Extent, boundary: Boundary, content: String },
    Bare { extent: Extent, text: String },
}
pub enum Enclosure { Braced, Bracketed, Angled }
pub enum Boundary  { Guillemets, Parentheses }
pub enum Separator { Period, Exclamation, Colon }
pub struct Extent { pub start: usize, pub end: usize }
pub struct Error  { pub extent: Extent, pub problem: Problem }
pub struct ReaderBudget { pub remaining: usize }

pub trait Protosizable    { type Output; fn protosize(&self) -> Self::Output; }  // String -> Result<Protos, Error>; Datom -> Protos
pub trait Textualizable   { fn textualize(&self) -> String; }
pub trait Canonicalizable { fn canonicalize(&mut self); }

let text = person.datomize(Path::new()).protosize().textualize();
```

#### String, escape, error

The text type is `String`. A closing guillemet inside a string is escaped with a backslash, so the ascent never refuses. The word is error, not fault, through the chain.

```
«she said \»no\» and left»
```

#### Canonical print

A space inside every delimiter at both ends when non-empty, and never inside the guillemets, where every glyph is content and a space would be load-bearing. `Head.body` with nothing around the separator. A single `;` opens a comment to end of line; comments are not printed.

## 3. Raw records newer than or absent from the skills, oldest first

### `/home/li/primary/flows/8e9e77/vision/single-field-structs.md` (2026-09-08)

#### 2026-09-08 — Those should be new types

> Also, there's another recent flow which you might want to look into, where we talked about single-field structs, which are an aberration and which we need to sort of train against, or possibly even refuse. I think we should possibly even refuse single-field struct types and ethos, and instruct against them even in Rust, because those should be new types.

-- psyche, typed.

### `/home/li/primary/flows/8e9e77/vision/single-field-structs.md` (2026-09-08)

#### 2026-09-08 — This should be a new type

Context: Responding to the description of `X.{ T }` as an Ethos one-position product, and its generated Rust tuple struct.

> Which, as I was talking in the other flow, is something that I want to make illegal now because it's absurd. This should be a new type and not a struct with just a single element in it.
>
> Then the implementation is wrong because a new type should be just the name of the type and then the separator, which is a period, and then the name of the contained type. If it's an inline type declaration, then it's just that: a type declaration. Never mind that. That's what it is. It would be absurd to make a new type that contains another complex type. A new type generally is like `name.string`, `age.integer`, or whatever we use: `int`.

-- psyche, typed.

### `/home/li/primary/flows/692df8/vision/ethos.md` (2026-09-15, date of first commit; the record states none)

#### Always specify the object type when showing Ethos; a requirement for talking about Ethos with clarity

Context: correction of a sketch the primary showed, which declared types without naming what kind of Ethos object each was. Logged directly by the main flow.

> The code you showed me for the shape in Ethos is wrong because it doesn't have a variant. You need to always specify your object type in Ethos. Otherwise, we don't know what we're looking at because it's context-dependent. I know by standard, but let's just make this a requirement to talk about Ethos with clarity.

-- psyche, typed.

### `/home/li/primary/flows/692df8/vision/identifiers.md` (2026-09-15, date of first commit; the record states none)

#### Identifiers are real types, not strings: an ethos library of identifier types on datom's own hashing types, a UTF-8 base legal in datom, bit-typed ids

Context: answer to the orchestrate Signal sketch, where FlowId and ClusterId were typed String. The opening sentences of the same message ruled the main-flow wording good and the word "Flow", not "seat"; those are recorded in log.md and vocabulary is the living's ruling. Logged directly by the main flow.

> Why are we saying that the ID is a string? It seems to me that we could maybe create an ethos library for this, but those are real types, like a SHA-256. Yes, in a way, it's a string when you print it, but it's not a string per se.
>
> Your flow ID is, let's say, what? Maybe we don't need to go hexadecimal. We can expand our bit range, our bit efficiency. Whatever is legal in datom is what we should use for our hashing base: a UTF-8 base for hashes. We should probably type them like, "This ID is a 36-bit identifier," or whatever we want to say that.
>
> We have our own protocol for all these identifiers, which uses datom's own standard hashing types that are in the library that we use to create these complex ID types.

-- psyche, typed.

### `/home/li/primary/flows/692df8/vision/identifiers.md` (2026-09-15, date of first commit; the record states none)

#### A readable alphabet, perhaps words, since the only cost is the token cost; security levels by how bad a collision is; what a legal symbol is, defined in Signal

Context: answer to the primary's alphabet, width, short-form and home questions. Logged directly by the main flow.

> The alphabet would be something that can be read. I was even thinking about how LLMs quantize or tokenize. If they tokenize as efficiently, because this is what I think is going on (for each character having essentially the same size as a small word when it's in a hash), then we might as well use words. The only cost we're worried about is the LLM token cost.
>
> Maybe we have a legible one because it's funny: the world is sort of leaning towards that too because they're more readable. They're more easily communicable in a speech-to-text context, and even cognitive. We think better in terms of words.
>
> How many bits do we need for safety in our context? We need to define different contexts properly, like three different levels of security in terms of how bad a collision is or how much control we have over it, because it's limited in nature. Local and private, then it's totally different. If it's a public namespace or something, then it's totally different.
>
> We should have both alpha-numeric, like readable, still readable, but alpha-numerics, sort of with symbols perhaps in, because these can still be said if they're commonly known. Obviously, colons and stuff like delimiters, dots and stuff are not going to be allowed, just like the bare string, basically. We should probably clarify what the bare string is. What would be a legal symbol, or I don't know, what do we mean by that? An ethos object identifier, right? What we can use as an identifier for an object. What is legal there as a symbol, basically, or what I call a symbol in ethos, something that symbolizes an object, like a data variant or whatever. That would probably live in ethos core or ethos standard, or I guess Signal could have it because we're going to think in terms of Signal. Essentially, sema is storing Signal, so it's all Signal. The data itself, we're going to refer to it as Signal when it's binary and it's typed. Signal is a good place to put that.

-- psyche, typed.

### `/home/li/primary/flows/b05237/vision/operational-ethosTypeRoot.md` (2026-09-19)

#### You should always make the ethos representation of that object in a type. Start with just a single type. The type ethos could have two sections: a single object, and a vector of all of the type definitions needed to fill that type. Ethos subjects: the library, just types, just kinds; the library combines them, and signal is more specialized. A communication layer is kind of a signal ethos object

Context: typed by the living to Psyche Fable (subflow of b05237) on
2026-09-19, quoting the datom sketch of FinalResponse from the
operational-final-response skill. The living corrects the presentation: the
object is shown as an ethos type, not a datom sketch, and proposes a Type
root of two sections. A queued `/export` command from Herder landed inside
the living's message; it is not the living's words and is omitted from the
quote. Logged by the subflow before acting.

> You should always make the ethos representation of that object in a type. You'd start with just a single type, or if you need to define more than one, you could have types, and then you open a vector bracket as a square bracket for a vector, meaning there are multiple types being defined.
> We can also, if that's not official, extend that there are different types of ethos subjects:
> - the library
> - just types
> - just kinds
> You have the library, which combines them, and signal, which is more specialized. In a way, this is kind of what you're defining here. If you're defining a communication layer, it is kind of like a signal ethos object that you're defining.
> Just start with the type. If you're just going to do one thing, at least define the type in the type. I guess the type could also have the private types, so it could have two sections:
> 1. just a single thing, a single object
> 2. a vector of all of the type definitions that are needed to fill that type
> That's what the type ethos type would be.

-- psyche, typed, direct to Psyche Fable, subflow of b05237. ("Etho subjects" reads "ethos subjects"; corrected.)

### `/home/li/primary/flows/b05237/vision/operational-ethosTypeRoot.md` (2026-09-19)

#### And the types plural would be a vector of public types

Context: typed by the living to Psyche Fable (subflow of b05237) on
2026-09-19, minutes after the Type-root statement, while Mind Astra's design
reply was arriving in the same pane. The living notes their earlier message
went through together with the machine message. Logged by the subflow before
acting.

> And the types plural would be a vector of public types, and then it looks like my message went through with the machine message.

-- psyche, typed, direct to Psyche Fable, subflow of b05237.

### `/home/li/primary/flows/b81560/vision/operational-nexusProcessObjectsAndEthosInDatom.md` (2026-09-19)

#### The Nexus process objects process everything. The spec is ethos, called from signal through a process that gets implemented. Give a subflow the spec and examples, explain in prose, then switch to datom for the system prompt. It responds with the spec of its response types. If it misresponds, correct it by naming the violated spec part. Better error messages generated automatically from ethos structure. Ethos becomes a payload in datom — how do we escape it?

Context: spoken directly by the living to primary Psyche opus (Claude, medium,
flow b81560) on 2026-09-19. The living describes the full Nexus → Signal →
Datom → Ethos pipeline. Nexus process objects are the implementations that
handle what comes through signal. The main function is standard. Projects must
use ethos specs. A subflow gets the spec and examples, starts in prose/markdown,
then switches to datom for the system prompt. The model responds in the spec'd
response types; misresponses are corrected by naming the violated spec part.
Error messages are auto-generated from the parse/protos structure — structure
errors are specific because the parser knows what was expected. Ethos is the
spec language used for training, error messages, and discussing new object
types. Ethos becomes a payload carried inside datom — this requires specifying
how ethos is escaped inside datom. Logged by the main flow before acting.

> So, the Nexus: it's too bad I lost this whole thing. The Nexus process objects are the ones that process everything that goes, and the main function is standard. That's why we have to force certain things, and the project has to use the ethos specs. The spec for the objects is the Nexus, and you have to call a Nexus object from signal. It has to go through a process, and that process is the implementation that gets written. It could involve a subflow, calling a subflow that's trying to use this spec. It's given the spec and a few examples of what should happen in a spec datom type, root message. Eventually, that's the vision.
>
> We can just make it simple for now: give it the spec of what it's expected to say and a few examples, and explain in prose, in a markdown thing, and then tell it, "Okay, now we switch to this spec." Then it starts to program it in datom for the rest of the system prompt. It expects it to respond with the spec of the types of responses it's supposed to be giving back, right? If it misresponds, it tries to correct it and tell it which part of the spec it's violating.
>
> We need better error messages that can be generated automatically because of the way we've created ethos, the structure, and all of that. We can give the error message as, "This is not the right structure," because when we decode, we can decode the structure part. If we can't do that, then we get an error message: "This is the wrong structure." We can get very specific types of error messages just based on the way we parse and the way we generate the protos. Datom is what's going to be generated and decoded, mostly, but ethos is the spec. Ethos is used to explain the messages in error messages or in training, or to talk about ideas for different kinds of new objects. Basically, ethos becomes a payload in datom, where we talk about ethos in datom, so that also has to be specified. How do we do that? How do we escape it?

-- psyche, direct to primary Psyche opus b81560.

### `/home/li/primary/flows/26c50c/vision/ethos.md` (2026-09-24)

#### Kinds and compiled conversion boundaries — 2026-09-24

> Yeah I meant kinds not traits. If I say traits I mean kinds. They're kind of the same thing but we say kind because I think it's actually more accurate.
>
> I want you to design that aspect of everything, or look at the design of it, and look at how enforced the ethos code is. Look at how we make sure that it's the code that runs, that it is compiled in, and that it does what it's supposed to be doing. It makes the code able to lower and lower (and vice versa) from a datom string or from string syntax into a Rust value, or not, depending on whether it has that option turned on during compilation. That way the Nexus doesn't do the string conversion but the CLI does and eventually the user interface will have all of that conversion-to-string logic compiled in.

-- living, typed directly in this flow.

### `/home/li/primary/flows/e51411/vision/ethos.md` (2026-09-25)

#### Within a few months, write whole programs directly in Ethos: function syntax, implementations, and a manifest for compiling and dependencies

> But within a few months I would like to develop Ethos to the point where we can just write the whole program directly in Ethos. That would mean fleshing out the function syntax in Ethos, implementations, and maybe the little things that need to be put together. Maybe the manifest needs to be fleshed out better for compiling and finding dependencies and so on.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. Said after choosing Clojure with Malli for HackingMessenger, as the direction beyond it.

### `/home/li/primary/flows/e51411/vision/ethos.md` (2026-09-25)

#### Implementations on kinds, as pure low-noise description

> I want you to reconsider if we exclude expanding ethos to do implementations (i.e., functions), which is all we would have, really. We would have implementations on objects, which are kinds actually. If we take that out then what is the state of ethos without that in the picture?
>
> I just mentioned that because we want to eventually do that but for now, unless you think you want to do some research, is it worth it to do this and what would the syntax look like? I don't know if it would satisfy me but if you think you can figure out how we would extend the syntax of ethos to do the functions and support it and make the syntax perfect and super minimal (so that there's no repetition, nothing out of place, and no noise), it's all just pure description of a program, as compact as it can be, basically, and not in word size. We don't shorten words. The compactness is in the very low noise amount.

-- psyche, STT, 2026-09-25, to e51411.

> How would that look? You can put a sub-agent and make a presentation or ask Fable and then present both in the book. Let's do the "how is ethos" without that separately in another book.

-- psyche, STT, 2026-09-25, to e51411, closing the words above.

### `/home/li/primary/flows/b7ba00/vision/types.md` (2026-09-26)

#### Everything becomes a type; open-ended variants are names; the map is out

Context: the living's comment on the "Implementations in Ethos" book, at "Names or types? Values carry written names (Fable), or are named by their type and filled from scope (Opus)." Retrieved by a reading subflow of 93ba9f. The "..." is as returned; whether it is the living's or an elision is unknown.

> Ultimately everything becomes a type because everything is a variant of a set. Even an actual instance of something is one member in a population in a set but for engineering reasons we don't create an enum for everything. There are these open-ended variants, which we call names. The same way we took out the map, right? The key-value map is out of our syntax because it's really just a poorly specified struct... There are no names really but you specify something while everything is a type. Even an instance of a type is a type of its own when seen from the right angle.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/c64ee3/vision/ethos.md` (2026-09-29)

#### c64ee3-3 — ethos is always written correctly; a block lacking its type is not ethos

Context: a comment by the living on the page, anchored on the first code block of this seat's first anatomy of skill deployment. That block showed six type declarations taken out of a whole Ethos file, without the root's head and without the other sections.

> We need to edit the skill that concerns this. Whenever ethos is written, this block is not ethos because it's lacking a type so it's invalid. Ethos always has to be correctly written; otherwise it's out of context, which means we don't know what it is. Actually you're telling me that it's ethos but still we should just write it correctly.

-- psyche, 2026-09-29 16:55, typed as a comment on the page.

### `/home/li/primary/flows/c64ee3/vision/ethos.md` (2026-09-29)

#### c64ee3-7 — the edit is the migration; ethos specified in ethos

Context: said in the same message as record c64ee3-6, on where the skill pipeline goes once it is real datom and ethos.

> When we go into a real Datom ethos, real binary specification, and data migration from the changes, it's using operational editing as an operation, which becomes the migration itself. The step to change the data is the same as the edit that's made to the source code because, in ethos, we're going to specify ethos in its own ethos language. The ethos language will then have its structure for how it stores itself in the nexus, so those will be ethos versions. That is the same principle for all the different proto families. You'll do the same with datom and eventually ethos would just compile to a full Rust program.

-- psyche, 2026-09-29, direct to this seat, STT.

### `/home/li/primary/flows/7328f4/vision/ethos.md` (2026-09-30)

#### Listing only types uses the types type

Context: Comment by the living on the book "Anatomy Correction" (Psyche Fable c64ee3), on the block "Ethos file 2 of 2 · Library root". Read by this flow from the page on 2026-09-30.

> If you're only listing types then you can use the `types` type. We should make sure that that's in the code, in the spec, and in the vision anyway.

-- psyche, typed (page comment, 2026-09-30T16:59).

### `/home/li/primary/flows/7328f4/vision/ethos.md` (2026-09-30)

#### Too much indirection; a variant carries the type of its own name; the struct follows the variant

Context: Comment by the living on the same book, on "Ethos file 1 of 2 · Signal root".

> This is something that goes deeper but the ethos syntax here is not what I envision still and I didn't address it before. Now I see that it's a bigger problem. We also want to work on other things and try to fix it. I feel like I've been fixing for days.
>
> On the syntax we don't want to do something like there's too much indirection. I already said, for example, if you have a skill type and one of the variants is psyche, that psyche object: the rule of ethos is that if there's another type called psyche with the same name, that's what data that variant carries. You don't need to write psyche type.
>
> We don't really need something like the collection because submit is too short. Using just an indirection to put a simple struct there, I think, is bad form. I think we can just have the definition of that struct be what comes right after the submit. The submit variant has, for data, a struct and its name will just be derived deterministically by ethos. I think that, for a variant, you can have a variant and a struct name be the same thing so I don't even think that's a problem.
>
> When we say stuff like skill name, I think it should just be name. Maybe not. Maybe that's appropriate. I haven't read everything. I don't know what deployed is. I'm trying to see where deployed actually happens. Oh vector deployed. Okay yeah, that's fair. The rest is all good.
>
> Like I said don't use psyche type. Just type psyche. I mean I'm not telling you to change. Obviously that's [the vision] so I want all of [the vision] to be edited to take that into account. Let's put a package together for this and give it to Fable on a new flow to help design this properly so he can send sub-agents to look at the current state and make his design proposition. Astra makes his and then we'll combine them. Fable and Astra Mind will agree after they've done their own design proposal on what it should actually look like.  And then Mindester [sic] will implement it on a fresh flow.

-- psyche, STT (page comment, 2026-09-30T17:10). Transcription corrected: "division" → "the vision" (twice). "Mindester" kept as heard.

### `/home/li/primary/flows/5578cc/vision/identifiers.md` (2026-10-03)

#### The three-word camelCase id is the interface wanted

Context: comment on «Flow ids in words, and seats launched by Flow», at the drawn shape `abandonAbilityAble` (a 33-bit id written as three BIP-39 words).

> This looks perfect. That's exactly the user interface I was looking for.

-- psyche, typed, 2026-10-03T15:54, book comment.

### `/home/li/primary/flows/5578cc/vision/identifiers.md` (2026-10-03)

#### The words are the first 33 bits of the harness's id, and convert back

Context: comment on «Flow ids in words, and seats launched by Flow», at "1. What the words are."

> Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?

-- psyche, typed, 2026-10-03T15:59, book comment. Ends with a question, answered in chat.

### `/home/li/primary/flows/9fb0ad/vision/ethosLibrary.md` (2026-10-03)

#### The word-id codec goes into a library all components reuse; manifest, registry, index; ask Fable questions, then a new flow designs
Comment on «Flow ids in words, and seats launched by Flow», thread at abandonAbilityAble.
> "This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something. This might mean needing to develop the way ethos is put together, like manifest, registry, index: where do dependencies, libraries, etc., come from? Let's get Fable to ask me some questions about that and then with the answers he can start on a new flow and design something."

-- psyche, typed, book comment, 2026-10-03T15:56Z, relayed by 5578cc.

### `/home/li/primary/flows/9fb0ad/vision/ethosLibrary.md` (2026-10-03)

#### The word-id library is generic over hash sizes; a kind that yields words
Comment on «Questions on the Ethos library», point 1.
> "No the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size. We could have a few different types. There's this 33-bit type. Maybe there's a situation in which we don't even need 33 bits. Maybe there's a situation in which we need more so it's a generic type. I don't know. Let's look at the Rust mechanics here and what we can do in terms of reusability. Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?"

-- psyche, typed, book comment, 2026-10-03T16:08Z.

### `/home/li/primary/flows/edf227/vision/identifiers.md` (2026-10-03)

#### FlowId is a hash, not an integer; a word-to-hash ambiguity in the last character is acceptable; a collision is brought to the psyche; the minimum product first, the word id may come in a later version
Comment on «The anatomy», at FlowId.Integer.
> "First of all it's not an integer, it's a hash, right? To be precise I don't know how we want to approach that but the other problem is this: because the 33-bit might not correspond with the alphanumeric cutoff of characters, when converting from words to alphanumeric to find a transcript, we might end up with a bunch of possibilities for the last character. I'm guessing that's possible, maybe something to consider. I don't care. If 33 bits, for me, I think it is enough entropy. If there is a clash then the model can easily figure out, "Okay here are two matches," and that would be worth bringing up to the psyche: "Oh we've had a collision," and then see what we do. But other than that it's not a big deal. I would like to get the minimum [viable] product up first so if we let go of the word ID for now and then do that in a later version, that's okay."

-- psyche, typed, book comment, 2026-10-03T19:26Z. Transcription corrected: "YBro" → "viable".

### `/home/li/primary/flows/edf227/vision/identifiers.md` (2026-10-03)

#### The flow id is a hash; its text forms are serialization, outside the Nexus; the Nexus thinks of it as a hash with traits
> "The flow ID is not a string, it's a hash. Why do you say integer and then string, or do you mean that an integer is a hash? I guess we need traits that allow us to switch back and forth, or I would like this to be a serialization and deserialization thing so that it's not actually in the Nexus. The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits. In the deserialization, we can have special implementations, maybe, so that a certain kind of thing is deserialized with a certain kind of algorithm that creates an alphanumeric hash from a string, from a hash which is an integer or whatever. Find out how this works and how we could do it."

-- psyche, STT, 2026-10-03.

### `/home/li/primary/flows/5578cc/vision/ethos.md` (2026-10-03)

#### Role is missing from the registry's kinds, and "kind" collides with ethos's own kind

Context: relayed by 6e782c; comment on «Context modules», at the registry listing of kinds (Library, Kind: Spirit Intent Vision Knowledge …).

> I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic.

-- psyche, typed, 2026-10-03, book comment.

### `/home/li/primary/flows/bad807/vision/ethos.md` (2026-10-04)

#### A field variant is missing; structs over chained variants: Voice is a struct of aspect and layer, and a flow has a role, one of which is a voice

Context: his comment on «The Nexus», on the code block "The anatomy in code" (`Voice.[ Psyche.Layer Mind.Layer ]`). Relayed by aa887c with its bracketed corrections.

> There are two things that are not really related but kind of meet: 1. There's a missing variant called `field`. 2. Now I'm seeing a syntax or a pattern in Ethos that I would like to develop because it allows for a certain cool-looking datom syntax: a series of variants one after another. There possibly could be many of those although I think the most common use is for two variants in a row, because after that you might as well use a struct. One could argue that one could use a struct from the beginning and I think that might be simpler. I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type, because it creates this repetition that you can see now: `[psyche].layer`, `[mind].layer`, `.layer` is being repeated. I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice. We can start leaning more on [structs] than on chaining up [variants], which ends up in an ugly Ethos pattern.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### Expanding: a special syntax that replaces an object with the datom payload in a file; a repo keeps a datom file indexing itself, so a deploy manifest is never recomposed by the model

Context: spoken to this flow, opening the design of datom expansion.

> One of the things I want to talk about is the concept of expanding. I would like Datom to be able to insert another Datom payload inside a certain file, like `replace`. It would be a special syntax, maybe a particular symbol just for that, since it's going to be quite unique. Let's review how we can make that system in an ideal architecture. What should it look like, with as many layers of correctness as correctness would allow or would warrant?
>
> I know that we've talked a lot about the ethos architecture but maybe Datom needs to also get a little bit of attention in how it actually works. That would allow us to have these sort of manifests. For deploying a skill curriculum, it would be kind of absurd to ask for the model to compose the entire registry of a certain skill repo every time the deploy happens. That repo could essentially just maintain a Datom file that indexes and specifies the entire repo.
>
> Wherever that payload is supposed to be, the agent could just use that special syntax. That means that this file, which would be a path, ought to be used to replace this object with the data in that file. Basically it's just a simple replace.
>
> We could also talk about what happens if we go the other way and we want to get a certain response with all of these values. I don't know if it's that useful but at least for the input that would be really useful.

-- psyche, STT, 2026-10-05.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### No Curriculum repo in the deploy; the skill repositories themselves are invoked

Context: his comment on «Datom expansion», the syntax example invoking curriculum-deploy with the Curriculum repository. Relayed by 8f0f57.

> Well with the new vision we wouldn't involve this curriculum repo. We would just directly invoke the particular repositories like mind, psyche, and field.

-- psyche, STT, book comment, 2026-10-05.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### No datom in any Nexus; string handling in a Nexus is forbidden

Context: his comment on the drawing's box «Nexus: no Expander, so @ is Forbidden». Relayed by 8f0f57.

> Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus.

-- psyche, STT, book comment, 2026-10-05.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### A reference path is not a string: no guillemets

Context: his comment on layer 1, "a bare string that begins with @ is written in guillemets". Relayed by 8f0f57.

> No it wouldn't use [guillemets] because that would make it a string, which it's not. It's a path. It's an expanding path or whatever the right term is here. Yeah it's a reference path so it's not a string so it's not going to have the string delimiter.

-- psyche, STT, book comment, 2026-10-05.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### Expansion is a step before the structure step, like the ethos rearranging step

Context: his comment on layer 2, "expansion happens at compose". Relayed by 8f0f57.

> So compose would be a step before the protos structure step, like finding the structure. There would be a step before that, kind of like how we have a step, or we should have a step in ethos to rearrange an ethos file so that it's a variant with a struct.

-- psyche, STT, book comment, 2026-10-05.

### `/home/li/primary/flows/8475a9/vision/datom.md` (2026-10-05)

#### Everything in Rust is a trait; a wrong trait design is a wrong anatomy

Context: his comment on the Rust block, whose compose was an inherent method. Relayed by 8f0f57.

> The trait is missing here. Everything should be done with a trait, right? Don't we have that rule? How we code in Rust: everything is a trait. Everything must fall under a trait. If the trait design is wrong then there's something wrong with the anatomy of the design of the system.

-- psyche, STT, book comment, 2026-10-05.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Don't double-wrap types: if a job is a flow ID, say flow ID

Context: his comment on «Flow spawning», on its Library root (Role.[ Voice Job ], Job wrapping a FlowId), 2026-10-06T14:59.

> Well first of all I still don't see the meta flow. If a job is a flow ID, then why are we even using the word "job"? Just use "flow ID". Why are you going to wrap a new type with another new type? Don't double-wrap types. That's silly.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### The datom file expansion and the ethos syntax changes are implemented in ethos, ahead of the three-repo curriculum deploy

Context: same message, 2026-10-06; on Astra implementing the three-repository, skill-based curriculum deploy.

> I want to get Astra going maybe on a new flow after all this, on implementing the three-repo skill-based curriculum deploy. I guess we would need the datom file expansion and also all of the things that I've been talking about modifying ethos syntax to be implemented in ethos.

-- psyche, STT.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Types are declared inline up to a decent level of recursion; repeating type names to declare them apart is noise

Context: his comment on «Ethos, distilled», proposal 5 (Everything is a type), 2026-10-06T15:52.

> There's some good here but remember I was saying that until we reach the third level of recursion I would rather see the types defined inline. Here there would only be one entry where each field of the struct would have the definition of these types inline, which would avoid repetition, right? That's the whole point: the terseness, unless the type is reused somewhere else.
>
> Even if Ethos must support declaring types inline that are used elsewhere, it could be confusing visually to find where a type's been defined but that's okay. I would rather the types be defined inline up until a decent level of recursion. I don't want to have to repeat the type names just so that they're declared independently. I think that's silly. And it creates a whole bunch of repetition, which creates a whole bunch of cognitive load.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Inline declaration is mandatory unless the type is too deep; an algorithm decides

Context: his comment on «Ethos, distilled», proposal 6 (Inline types), 2026-10-06T15:53.

> Well like I said earlier, even if a type is declared inline in one place, it can still be declared at the top. We don't have to and in fact just because of the extra repetition that creates, I would want to make the inline declaration mandatory unless that particular type is so deep that it itself requires too much recursion to be declared inline. We have to explain some kind of algorithm to determine whether or not a type should be declared inline.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### A one-position type is called a new type

Context: his comment on «Ethos, distilled», proposal 7 (One position), which said "There is no struct of one position. A type that holds one other type is written as its name, a dot, and …", 2026-10-06T15:55.

> No it's not. It's named `a.` and that's a type. It's a new type, which is explained syntactically elsewhere. We're not going to talk like little kindergarten. We're engineers here. We're going to call things what they are and that's a new type.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Line breaking: a recursive block that would run too far right opens its first element on a new line, indented; vectors wrap at a width, aligned with the first item

Context: his comment on «Ethos, distilled», proposal 8 (Vertical), on its example `launch {` with `voice` on the same line, 2026-10-06T15:58.

> This is a good beginning but I'd like to further develop the logic that we use to determine where the new lines are and things. If the recursive block is going to expand to the right too much, then instead of, like in the example, you have `launch {` and then you put `voice` on the same line, instead of that I would put `voice` on a new line, indented right, so that you get more space to the right that way.
>
> This is fine the way you had it in your example because `voice.aspect.layer` was not so long. Actually it's wrong because `aspect` is declared elsewhere and we're saying we can have three levels of recursion. `aspect` should have been declared in line, which means `voice` should have been on a new line, and then you would add more than enough room to declare `aspect` and `layer` in line. `layer` can have its variance wrap around.
>
> Like when we have a vector, we can do this: we can have more than one item per line but at a certain length it wraps around and lines up with the first item and then continues like that. We can have a certain number per line but only up to a certain width.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Show the Ethos, not the Rust it generates
Context: comment on "enum" in the Names section.

> Well if you're showing, don't show me code generated from Ethos unless we're working on Ethos and how it generates Rust. Just show me the Ethos. That's the whole point of having Ethos. If you show me the Rust that Ethos makes, then we lose all of the benefits of even having Ethos. It's like having winter boots and going outside in the snow barefoot. Use your winter boots.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Newtypes, not type aliases
Context: comment on `pub type FlowId = String;`.

> Isn't that a type alias? We want new types not type aliases. Let's look at what this is in practice on the Rust side and what the differences are. From memory I don't think I want type aliases. I'm pretty sure I want... I think they're called the single tuple new types or just new type for short. I think the properties of those are more interesting than these type aliases, which I think don't really offer much in terms of correctness but you're welcome to correct me.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### Traits are load-bearing abstractions
Context: comments on "ReportsThroughCli", "PreparesClaudePane", and the one-method Nexus trait.

> On a similar note here, maybe something like executable instead of reports through CLI. I feel like the machine is just inventing a whole bunch of silly traits that are not really load-bearing, as in it's offering the right abstraction. The [trait] is a cognitive help so if it's just these silly big verb-containing phrases, it seems like it's just sort of making [traits] up for the sake of filling the requirement that everything must be done under a [trait].

> That doesn't really qualify as a trait and it's probably too narrow. There's probably a bunch of other capabilities that we could agglomerate under an appropriately named trait, like a Claude host trait. I guess we can use either a qualifier or a name for traits.

> A trait that only has one function is suspicious and a trait that's only implemented by one type is doubly suspicious. Just throwing that out there. I think we need to design traits more carefully and types. This is why we created ethos.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06. Transcription corrected: "trade" → "trait" (his own correction, "Trait not trade.").

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-06)

#### The running Nexus as operation, actor or process; all types in Ethos
Context: comment on "RunningNexus", «Start: what self is».

> This is an interesting concept and I think it belongs in operation ethos as the main operation. Maybe "operation" is the right term. Maybe it's "actor" or maybe there's something in between: "process."
>
> Showing me types in Rust is kind of silly. Like I said, we have Ethos. Is that because we have a problem with it? Is it because we don't support mutexes in Ethos, so the machine feels obligated to define that type in Rust directly? I feel like we should maybe possibly make all of the types in Ethos but maybe there are limitations and problems with that. Or maybe it's not realistic. You're invited to push back on that but also to consider it seriously.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

### `/home/li/primary/flows/d4ae97/notion/ethos.md` (2026-10-06)

#### Traits extracted as Ethos
Context: comment on "PreparesClaudePane"; framed "just a thought".

> I'd like to maybe get a list so I could get a secondary, maybe on a new secondary flow, or don't spend too much time dealing with the refresh. You should be just designing. I don't know who I'm talking to here but we should get a fresh Opus flow on designing a system with Sol, [Mind Secondary], that can use Rust tools to extract:
> - trait names
> - what types implement them
> - what each of these traits has, basically the short version of the trait
>
> Maybe it could even be represented as ethos. Maybe we can represent all the traits as ethos. Just a thought so that we could review the concept and then the implementation would be done in Rust.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06. Transcription corrected: "mine secondary" → "Mind Secondary".

### `/home/li/primary/flows/d4ae97/notion/ethos.md` (2026-10-06)

#### Flowcharts as an Ethos spec
Context: comment on the hook figure (pane, SessionStart, PostToolUse, Stop).

> This graph is good so it could become vision. I don't know. I guess that would be a Mermaid chart. It would be cool to research. We could have a proto-like language or maybe it's just a spec on a datom or it's an ethos spec of flowcharts, which is then represented in datom. That would be cool to be able to start keeping our documentation about flow graphs and flowcharts in proto syntax. Just the thought, but we can just do more, maybe for now. Is that what's been happening?

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

### `/home/li/primary/flows/db38f8/vision/ethosAndBookComments.md` (2026-10-06)

> I really don't see the point of looking at types in Rust when we've created a language almost entirely for these types and traits. It just felt silly to keep going and reading all this Rust.

-- psyche, STT, 2026-10-06.

> Are machines scared to use Ethos or is there something broken with it? I'm really curious why it seems so difficult.

-- psyche, STT, 2026-10-06.

> Also the way the comments were aligned in some of the recent books: the first comment on the comments should be lined up with the object's indentation. I didn't see any use of the new line indentation style, which should be favored over starting indentation on the same line where the containing type is declared. This takes a lot of horizontal space and also makes it difficult to line up the comments because then the comments don't have a lot of space.

-- psyche, STT, 2026-10-06.

### `/home/li/primary/flows/e5a0bc/vision/ethos.md` (2026-10-06)

#### Comments line up with the object's indentation; the new-line indentation style is favoured over opening on the declaring line

Context: his comment on recent books' ethos blocks, 2026-10-06, relayed verbatim by Field db38f8 at his request.

> Also the way the comments were aligned in some of the recent books: the first comment on the comments should be lined up with the object's indentation. I didn't see any use of the new line indentation style, which should be favored over starting indentation on the same line where the containing type is declared. This takes a lot of horizontal space and also makes it difficult to line up the comments because then the comments don't have a lot of space.

-- psyche, STT, relayed by db38f8.

### `/home/li/primary/flows/e5a0bc/vision/ethos.md` (2026-10-06)

#### A comment goes above or beside the thing it comments on, not below

Context: same comment.

> Is this really how most people comment, below the thing they comment on? My experience was that we would put the comment above or beside the thing we would comment on.

-- psyche, typed, book comment.

### `/home/li/primary/flows/e5a0bc/vision/ethos.md` (2026-10-07)

#### Vertical expansion, not horizontal: a new line and an indented new line for each element, the comment lined up with the element it is on

Context: his comment on «Flow and Message», 2026-10-07, on its Library root, where `Voice.{ Aspect.[ Psyche Mind Field ] …` ran inline and the comment "a metaflow with no known ending" sat on a line of its own under `Voice`.

> I have no idea what this comment (a metaflow with no known ending) is supposed to address because your formatting is not following my guidelines. I prefer vertical expansion rather than horizontal and here you have not only one but two inline horizontal expansions.
>
> If you made a new line and an indented new line for aspect, and then another indented new line for psyche, and placed your comments (because the way I see it, this comment is lined up with voice indentation-wise), I associate visually and automatically with that.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-07)

#### Review the specification of the operation type
Context: comment on "Composed" (with open and spawn), section 4 of «Flow and Message» 2nd edition.

> What's this section about, with `composed`, `open`, and `spawn`? What is that? I'd like to get to review the specification of the operation type ethos.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-07)

#### A Nexus's types live in its three roots or in named libraries
Context: comment on `Settings`, among the types Curriculum defines in Rust.

> Yeah that's what I'm saying. When we write a nexus, essentially all of the types, because we have three layers, are going to be in one of the three layers or in the library. The libraries can be named. They can have subnames, right? Kind of like Rust: if you create a file, I guess, called foo.bar.ethos or whatever (what is our file suffix for Ethos anyway?), .ethos is great because LLM is thinking word anyway.
>
> I don't know where I was going but yeah this is a shit show. I'm realizing now that I'm actually looking at the code with you and this is what we need to do, right? Let's fix this. Let's rewrite this as a whole vision that would be better. Even if I don't agree with all of it maybe you can just apply my correction and then we'll write the vision. That's it: write the vision and it's all around the ethos code.

-- psyche, comment on «Curriculum's ethos, and every Nexus's three roots» (https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU), 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-07)

#### Variants are ordered by seniority, the first most senior
> I guess we should represent it in the order, so whenever you have a variant in ethos you need to position the variants hierarchically. There's an implied hierarchy: the first one is most senior. That's going to be the case with spirit being first and, in the field, compensation is above trial, right? It's tested, trial, and field work.

-- psyche, STT, 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-07)

#### Traits are written in ethos
> We can have other kinds of checks to make sure that all implementations are done under a [trait] but that's very mechanical. The model is just code around it and writing really dumb traits. We have to teach people how to design traits, which is why we have to look at the traits, which is why all the traits should not now [sic] have to be written in the ethos. We can mechanically make sure there's no trait.

-- psyche, STT, 2026-10-07. Transcription corrected: "trade" → "trait".

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-07)

#### No trait outside the ethos-generated code (correction of the entry above)
> I was saying we can mechanically make sure there's no trait in the non-ethos-generated part of the code and my speech detect got me off.

-- psyche, typed, 2026-10-07. Corrects the [sic] in "Traits are written in ethos": every trait is written in ethos; a mechanical check finds none in hand-written code.

### `/home/li/primary/flows/d4ae97/vision/curriculum.md` (2026-10-07)

#### Curriculum's ethos is unreadable
Context: comment on `String` in curriculum.ethos.

> Wow, string, string, string, string, string. Am I supposed to know what any of this is? This is so fucking retarded. I don't understand any of this. Roll packet plan. What is this curriculum? This makes no sense to me. ... We have a lot of correction to do here, eh? This is garbage. What the hell happened?

-- psyche, comment on «Curriculum's ethos, and every Nexus's three roots» (https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU), 2026-10-07. Transcription kept: "Roll packet plan" is RolePacketPlan.

### `/home/li/primary/flows/02dda6/vision/ethos-code-in-vision.md` (2026-10-07)

#### The vision contains the ethos code

Context: The living's message relayed by 0c85a3, 2026-10-07.

> The vision is actually going to contain the ethos code. I actually realized that today when I was reading the books on Claude and everything was presented as an edit to the source code of the ethos code of certain repositories. This is what happens when we send an implementer with the new vision skill.
>
> First we put the code in the vision and then I guess we just write a tool that fetches the ethos source code from the current vision of a certain nexus. You could even do this deterministically. You would fetch the ethos source code from the current vision of a certain nexus. There would be the meta and all of them. They all would be in the vision.

-- psyche, STT, 2026-10-07, relayed by 0c85a3.

### `/home/li/primary/flows/d4ae97/vision/datom.md` (2026-10-07)

#### Hashes and flow ids: a stored type and a string representation
Context: said beside his comments on the second edition of the Flow book, about how certain objects convert between their stored form and their Datom form.

> Have on the side: develop this concept (and this is in my comments in the book) of how certain types of objects have a different kind of conversion in the sense that they might be an 8-bit, sorry. I don't know how many bytes 256-bit is but I think it's 8. No, sorry, it's more than that: 8 × 4.
>
> Anyway the number of bytes that it takes for the SHA-256 to fit is going to be the type or we should actually have an actual type. Let's look at what types people use for hashes in actual fast Rust code and that's the type we're going to use to store it.
>
> When it's actually represented in Datom or ingested from Datom, it's going to have some string representation and the flow ID as well, like the words to integer or something. We have some kind of a match concept that we'll implement so that the transcript file can be found using these words programmatically, in code. There's going to be a conversion which probably will end up with a some kind of a match, like a regular expression match or something, a glob on a superset of string, because the 33 bits doesn't actually line up with the alphanumeric cutoff of the Flow IDs representation in the alphanumeric (if you follow what I'm saying). We can be pretty certain at 33 bits that we're not going to have clashes in session IDs. I'm almost entirely certain of that.

-- psyche, STT, 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/datom.md` (2026-10-07)

#### Stored type and datom representation; shorthands; the flow id as three words
Context: comment on "FlowId" in the registry record, section 2 «The registry is Flow's Memory».

> I know I said I want to focus on bringing Flow Nexus to production and this would probably slow things down quite a bit but this is who I am. Perfectionism does slow down a lot of things but here it is.
>
> Certain concepts, I guess you could call them, or certain types in ethos, will have to have a different representation than how they're stored in the runtime. For example the SHA-256 is a good example. I've seen another presentation in which the SHA-256, which is really a 256-bit number, is said to be a string.
>
> Now I understand what the machine is trying to convey in terms of the fact that when we handle this SHA-256 in datom in text form, it's a string. Everything basically is a string. It would kind of be absurd to say that now integers are strings and enums are strings just because they have a string representation. Although, like I said, I do understand the reasoning or the practical reasons behind this, we need some kind of abstraction there. When we go from datom representation into an in-memory type, there's a conversion that happens and this touches the flow ID as well. You could represent certain things differently, not represent them, but they would have different methods.
>
> The shorthand concept ties into this, where you get a certain kind of query or response that is the full-size, fully explicit, advanced expert version that has all the parameters. You have the shortened version that only contains the bits that matter for the particular use case in which these shorthands are being used, namely in the thinking machine context most of the time.
>
> For example messaging doesn't require knowing its flow ID at all. In fact it would be bad practice to try to send to a flow ID because the sender doesn't know if that is the current flow of that voice. I guess you could have a subflow. Research this thoroughly.
>
> Can subflows use subflows themselves? It would be interesting to allow a subflow to use another subflow to populate its context at the middle stratum using the messenger. I don't know because the messenger has this registration process that probably would slow things down. I'm going all over the place now.
>
> The flow ID needs to be represented with this. We decided on three words and I think it's probably wise because in LLM terms it's fairly cheap for the amount of entropy that we get. This three-word camel case format conversion, and the same thing with the [SHA-256], is sort of like some kind of base 32 or whatever it is that they're using, into an actual 256-bit whatever or a vector of bytes. I don't know how these things are represented. I think a vector of bytes is going to be the type that is in memory, whereas when it's back out into datom, it's going to be in this alphanumeric encoding and this concept is probably going to come back and be used in other places as well.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07. Transcription corrected: "shot 256" → "SHA-256".

### `/home/li/primary/flows/f5a6e9/vision/ethos.md` (2026-10-07)

#### Three spaces of indentation: two are not visually enough

Context: his comment 2 of 9 on «Flow and the metaflow» (https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW), 2026-10-07 18:57, on `Worker.Name ]    ; a subflow's role` in the signal.ethos block. Relayed verbatim by Field db38f8.

> Well this just shows me that I guess you've used two spaces for indentation and that isn't visually enough to really see the structure. I know that usually it's either two or four but maybe we can try three. I like the number three so I think we should give it a shot. Maybe four is too much and three is enough.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/f5a6e9/vision/ethos.md` (2026-10-07)

#### A SHA-256 type does not belong in the curriculum library

Context: his comment 6 of 9 on the same book, 19:02, on the Memory block importing `curriculum:[ Name Sha256 ]`. Relayed by db38f8. Transcription corrected: "shot 256" → "SHA-256".

> I don't see how a [SHA-256] type belongs in the curriculum library.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-08)

#### Ethos redesigned to his syntax; patterns wanted and disallowed
> I want to redesign the ethos and flow. ... Actually probably changing ethos to better conform with my expectations of the syntax and what kind of patterns I want to see and what kind of patterns I don't want to see and even disallow

-- psyche, STT, 2026-10-08.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-08)

#### Ethos is designed with the datom payload's cost in mind
> Basically the guiding principle in designing the ethos and the datom payload is also keeping in mind what the datom payload looks like, considering that the datom will probably be more expensive because machines will have to output them. It's funny because System 1 models actually make that cheaper, which is interesting.

-- psyche, STT, 2026-10-08.

### `/home/li/primary/flows/d4ae97/vision/ethos.md` (2026-10-08)

#### Jev and the System 1 models speak a subset of Ethos
> Also I want to marry Jev System 1 and its siblings, the System 1 models, to probably a subset of the Ethos specification so it could talk to an Ethos contract. Like I said it's only a subset because it doesn't have all the types yet. Let's get that also going, where we're designing in another flow.

-- psyche, STT, 2026-10-08.

### `/home/li/primary/flows/d4ae97/vision/datom.md` (2026-10-08)

#### A checked bridge between JSON and datom, adaptable to other formats
> And if we make the tool that can translate [JSON] to Datom and vice versa with the actual specified ethos (checking, back-checking whenever it goes in or out, type-checking it through the [rest of the] infrastructure), then we could use Datom with our [Clojure] tools, which would be really cool. And if we design it well it would be really easy to adapt it to other things like [Cap'n Proto]. I'm guessing [Clojure] has [Cap'n Proto]. I think everything does. I think Java has it so [Clojure] automatically can get it. That would be: if we create the right abstraction then we can adapt it to different data formats.

-- psyche, STT, 2026-10-08. Transcription corrected: "JavaScript" → "JSON"; "REST infrastructure" → "rest of the infrastructure"; "Closure" → "Clojure"; "Cap and Proto" → "Cap'n Proto". The first two corrections are inferred from the conversation (the JSON bridge); not confirmed by him.

### `/home/li/primary/flows/d4ae97/vision/tools.md` (2026-10-08)

#### Clojure builds under Nix; Ethos to JSON; the mind keeps a registry of topics
> This is interesting, and I'd like maybe an Astra Flow mind to research the most correct way to deal with Nick's [Nix] issue, which ends up at:
> - the most reproducibility
> - lower recompilation time
> - reuse of already compiled Nix artifacts as much as possible
> - maybe even maximizing the use of closure code itself to write the logic with which it's compiled
>
> We could even get someone to design a closure abstraction or to look at research if anybody has made a closure abstraction around Nix.
>
> Also, to go along with the Jev system 1 to Ethos interface, let's look at creating a utility or library, or both, that lets us go through JSON for a particular Ethos datom to be translated into a specification eventually. ... I'm guessing there are so many tools that we're going to be able to interact with that way, and yet we get to write our specification in Ethos and hide all of the ugliness of JSON.
>
> That's another topic that goes along with it. It's sort of like a subtopic of datom Ethos design. Let's start also maintaining these topics. This is an aspect of the mind: to keep a registry of the topics. Until we have the mind nexus component, we can maybe write something in closure. Maybe we just do a hard pass on all our closure prototypes and start working on a bridge for the JSON that will allow us to migrate the data into Nexus. It'll make for a quicker startup of the prototype and then a smoother transition into the future runtime.

-- psyche, comment on mkCljUberjar, 2026-10-08. Transcription corrected: "Nick's" → "Nix".

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-08)

#### A Clojure Flow prototype, with its own database, addressed by metaflow name, specified in Ethos
> Anyway I would really like to get all of the current or the most current psyche vision, or the most psyche-aligned version of the Clojure flow prototype, with its own database with metaflow addressing by metaflow name. We could even have channel enforcement anchored in the configuration-style data: we should spec everything in Ethos and then have a standard, maybe even eventually code, from which Ethos code creates the types, the functions, and the logic, centered around the concepts defined in Ethos in the vision, right?
>
> We're always creating psyche data, mostly vision, because this is what we're going towards, what our vision is.

-- psyche, STT, 2026-10-08.

### `/home/li/primary/flows/ebbe30/vision/aspects.md` (2026-10-09)

#### Three aspects to every topic

Context: Said at the start of the day, 2026-10-09, while ordering a book audit.

> I know we want to have more than one flow now for psyche, per topic, like each aspect essentially. The aspect is now, I think, part of any metaflow. It shows us which aspect of that topic it's actually taking care of.
> - If it's psyche it's trying to design and bring the living's vision into cohesive context: to the point, well-worded, and with a high concentration of vision signal to noise.
> - The mind is where it gets put into an implementation.
> - The field is when it's being used in the system. The system is being mutated or debugged in accordance with that topic.
>
> There are three aspects to every topic potentially. Just because we start a psyche on, let's say, ethos, doesn't mean that we need to automatically start a mind on ethos. Eventually when the design is ready, we would for implementation unless sometimes the psyche could also do a first implementation or an alternative implementation to compare (just like field could do a field implementation, a closure, or a fast prototype to do something). In the same way, psyche could take the design and then try to extend it into an implementation.
>
> If we had, let's say, a lot of usage in the models that we use for psyche, like now, overnight maybe if we still have a lot of Claude, we'll have Claude do some implementations in psyche, which is fine. It really depends on the budget.

-- psyche, STT, 2026-10-09.

## 4. Where a raw record contradicts or moves past a skill

PS = `/git/github.com/LiGoldragon/psyche-skills/skills/`,
MS = `/git/github.com/LiGoldragon/mind-skills/skills/`,
F = `/home/li/primary/flows/`. The pairing of lines is this file's reading.

1. Alias against newtype. Skill: "An alias bears them through the type it
   names: an alias is not a new type and cannot carry a derive." with
   `pub type LockId = Integer;` (PS`vision-ethos.md`, sections "What a
   declaration turns into" and "Every declared type bears both kinds"); also
   "`Name.Type` is an alias" (MS`knowledge-ethos.md`). Raw: "We want new
   types not type aliases." (F`d4ae97/vision/ethos.md`, 2026-10-06); "It's a
   new type, which is explained syntactically elsewhere." (same file,
   2026-10-06); "This should be a new type and not a struct with just a
   single element in it." (F`8e9e77/vision/single-field-structs.md`,
   2026-09-08).
2. Inline payload name. Skill: "The inline struct or enum is a full type
   whose derived name carries an underscore, non-idiomatic for a Rust type,
   so it never collides" (PS`vision-ethos.md`, "Inline types"). Raw: "I think
   that, for a variant, you can have a variant and a struct name be the same
   thing so I don't even think that's a problem." (F`7328f4/vision/ethos.md`,
   2026-09-30). The same skill also says "A variant's payload is written in
   the variant and bears the variant's name".
3. Inline declaration, optional or mandatory. Skill: "A type used once is
   declared inline where it is used; ... Inline nesting goes about three
   deep; past that, the type comes from a Library." (PS`vision-ethos.md`).
   Raw moves past it: "I would want to make the inline declaration mandatory
   unless that particular type is so deep that it itself requires too much
   recursion to be declared inline. We have to explain some kind of
   algorithm" (F`d4ae97/vision/ethos.md`, 2026-10-06).
4. Layout style. Skill: "a structure with more than one element opens on
   its line and its elements hang beneath the first, aligned" (PS`vision-ethos.md`,
   "Spacing"). Raw: "I didn't see any use of the new line indentation style,
   which should be favored over starting indentation on the same line where
   the containing type is declared." (F`e5a0bc/vision/ethos.md`, 2026-10-06);
   "If you made a new line and an indented new line for aspect"
   (same file, 2026-10-07); "instead of that I would put `voice` on a new
   line, indented right" (F`d4ae97/vision/ethos.md`, 2026-10-06).
5. Indent width and vector wrap, absent from the skill. Raw: "maybe we can
   try three" (F`f5a6e9/vision/ethos.md`, 2026-10-07); "at a certain length
   it wraps around and lines up with the first item"
   (F`d4ae97/vision/ethos.md`, 2026-10-06).
6. Comment placement. Skill: "Ethos carries a comment on every section and
   on every line that has a next layer ... a comment runs from ; to the end
   of the line." (PS`vision-ethos.md`). Raw adds where: "we would put the
   comment above or beside the thing we would comment on." and "the first
   comment on the comments should be lined up with the object's indentation"
   (F`e5a0bc/vision/ethos.md`, 2026-10-06/07). Knowledge: "comments are not
   printed" (MS`knowledge-protos.md`).
7. Kind naming. Skill: "Kinds are qualifier-named: Runnable, Textualizable,
   Structural, Embodied." (PS`vision-ethos.md`, "Naming"). Raw: "I guess we
   can use either a qualifier or a name for traits." (F`d4ae97/vision/ethos.md`,
   2026-10-06).
8. Trait design moves past the mandatory-trait rule. Skill: "Every method
   call in our Rust code lives under a trait" (PS`intent-mandatory-traits.md`);
   "A kind is declared, never inferred" (PS`vision-ethos.md`). Raw: "A trait
   that only has one function is suspicious and a trait that's only
   implemented by one type is doubly suspicious." (F`d4ae97/vision/ethos.md`,
   2026-10-06); "we can mechanically make sure there's no trait in the
   non-ethos-generated part of the code" (same file, 2026-10-07).
9. Roots and Sema. Skill: "Library, Signal, Operation, Memory. ... Sema's
   are record types, the rest to be decided. Signal gives a Nexus its main
   types and Sema its database types." (PS`vision-ethos.md`, "Roots", first
   paragraph; the second paragraph names Memory). Raw: "That means we rename
   all of the Sema aspect pertaining to the database."
   (F`b7ba00/vision/meaningLanguage.md`, 2026-09-26, quoted in the Nexus
   file). The four-root line was settled by d4ae97 during the 2026-10-07
   migration ("Decided: vision-ethos Roots = Library Signal Operation
   Memory", F`d4ae97/log.md` line 159), not by a ruling of his.
10. File and namespace. Skill: "The unit is File: one file, one Rust module.
    No namespace inside a file." (PS`vision-ethos.md`). Raw moves past it:
    "The libraries can be named. They can have subnames, right? Kind of like
    Rust: if you create a file, I guess, called foo.bar.ethos"
    (F`d4ae97/vision/ethos.md`, 2026-10-07); a library manifest, registry,
    index (F`9fb0ad/vision/ethosLibrary.md`, 2026-10-03).
11. Versions. Skill: "An ethos file carries no version; datom has no
    versions." (PS`vision-ethos.md`). Raw: "The ethos language will then have
    its structure for how it stores itself in the nexus, so those will be
    ethos versions." (F`c64ee3/vision/ethos.md`, 2026-09-29).
12. Horizon. Skill: "Ethos will eventually replace everything ... what it
    enables — generator emission among it — comes in its time."
    (PS`vision-ethos.md`). Raw: "within a few months I would like to develop
    Ethos to the point where we can just write the whole program directly in
    Ethos" (F`e51411/vision/ethos.md`, 2026-09-25); "we're going to specify
    ethos in its own ethos language" (F`c64ee3/vision/ethos.md`, 2026-09-29);
    "The vision is actually going to contain the ethos code."
    (F`02dda6/vision/ethos-code-in-vision.md`, 2026-10-07).
13. Flow id type. Skill example: `FlowId.String` (PS`vision-ethos.md`,
    "Shapes and placement"). Raw: "The flow ID is not a string, it's a hash."
    (F`edf227/vision/identifiers.md`, 2026-10-03).
14. Stored form against text form, absent from the skills. Skill: "All
    naming and self-description live in the type; the text carries only the
    data." (PS`vision-datom.md`). Raw: "Certain concepts ... will have to
    have a different representation than how they're stored in the runtime"
    and "a vector of bytes is going to be the type that is in memory, whereas
    when it's back out into datom, it's going to be in this alphanumeric
    encoding" (F`d4ae97/vision/datom.md`, 2026-10-07).
15. Expansion, absent from the skills. Skill: "Five pairs." of delimiters
    (PS`vision-protos.md`); "Not yet; a written datom gives every position."
    (PS`vision-datom.md`, "Omittable fields").
    Raw: "I would like Datom to be able to insert another Datom payload
    inside a certain file ... It would be a special syntax" and "It's a path.
    It's an expanding path ... so it's not going to have the string
    delimiter." (F`8475a9/vision/datom.md`, 2026-10-05).
16. Format bridges. Skill: the datom nexus "comes when there is more to do:
    translating datom objects between formats" (PS`vision-datom.md`,
    "Repository"). Raw: "the tool that can translate [JSON] to Datom and vice
    versa with the actual specified ethos" (F`d4ae97/vision/datom.md`,
    2026-10-08), now, for the Clojure tools.
17. Chained variants. Skill example: "`Observed.Locks.[]` is the Observed
    variant carrying the Locks variant carrying an empty vector"
    (PS`vision-datom.md`). Raw: "We can start leaning more on [structs] than
    on chaining up [variants], which ends up in an ugly Ethos pattern."
    (F`bad807/vision/ethos.md`, 2026-10-04), said of ethos declarations.
18. Absent from the skills: variant order by seniority
    (F`d4ae97/vision/ethos.md`, 2026-10-07); a Type root and the `types`
    type (F`b05237/vision/operational-ethosTypeRoot.md`, 2026-09-19;
    F`7328f4/vision/ethos.md`, 2026-09-30); ethos as a payload inside datom
    and its escaping (F`b81560/vision/operational-nexusProcessObjectsAndEthosInDatom.md`,
    2026-09-19); identifiers as real types and a word-id library
    (F`692df8/vision/identifiers.md`, F`5578cc/vision/identifiers.md`,
    F`9fb0ad/vision/ethosLibrary.md`); a Jev subset of Ethos and payload cost
    (F`d4ae97/vision/ethos.md`, 2026-10-08).

Inside the skills, not against a raw record:

- PS`vision-datom.md` ends "defined in Vision/meaning.md"; that file does
  not exist (`/home/li/primary/Vision/` holds ethos.md, messaging.md,
  nexus.md). The meaning language is in PS`vision-meaning.md`.
- PS`vision-ethos.md` names the derive `Compositional` and the feature
  `"datom"`; MS`knowledge-ethos.md` and MS`knowledge-datom.md` name
  `Composing` and the feature `knowledge-datom`.

## 5. Open questions and books awaiting his rulings

His own open questions, quoted:

- "How do we escape it?" — ethos as a payload in datom
  (F`b81560/vision/operational-nexusProcessObjectsAndEthosInDatom.md`, 2026-09-19).
- "Is this category part of the language equivalent with our ethos?"
  (F`b7ba00/vision/meaningLanguage.md`, 2026-09-26).
- "Is this a kind that can yield so we can call the Flow ID method on Flow
  ID that is `as_words` or something?" (F`9fb0ad/vision/ethosLibrary.md`,
  2026-10-03); and "like manifest, registry, index: where do dependencies,
  libraries, etc., come from?" (same file).
- "Is it because we don't support mutexes in Ethos, so the machine feels
  obligated to define that type in Rust directly?" and "You're invited to
  push back on that but also to consider it seriously."
  (F`d4ae97/vision/ethos.md`, 2026-10-06).
- "Are machines scared to use Ethos or is there something broken with it?"
  (F`db38f8/vision/ethosAndBookComments.md`, 2026-10-06). e5a0bc's answer,
  a claim from F`e5a0bc/log.md`: nothing broken; the ethos files on disk are
  one-line and unreadable.
- "We have to explain some kind of algorithm to determine whether or not a
  type should be declared inline." (F`d4ae97/vision/ethos.md`, 2026-10-06).
- The SHA-256 type: "Let's look at what types people use for hashes in
  actual fast Rust code" (F`d4ae97/vision/datom.md`, 2026-10-07); "I don't
  see how a [SHA-256] type belongs in the curriculum library."
  (F`f5a6e9/vision/ethos.md`, 2026-10-07).

Machine claims about the code, from F`e5a0bc/log.md` (its ethos survey,
`flows/e5a0bc/reports/ethos-survey.md`), not witnessed here: inline
declarations are accepted at any depth and are not mandatory; `Name.Type`
generates an alias; the protos writer has no width setting; no `@`
expansion exists; no ethos version is in any manifest. From F`d4ae97/log.md`
line 183, claimed witnessed by d4ae97: "Curriculum ethos witnessed: Library
root only; no Nexus has Memory; only Flow has Operation."

Books awaiting his rulings (listed as awaiting in F`d4ae97/handover.md` and
F`e5a0bc/summary.md`; no ruling on them was found in the logs read):

- «Ethos: inline, layout, expansion», e5a0bc, nine rulings: inline algorithm,
  layout and file width, one position as newtype, expansion before
  structure, index source, path resolution, content pin, write-back, the
  `Dereferencing` kind. https://claude.ai/artifact/41VVDCvTkh742a7dXEznCk;
  source F`e5a0bc/books/5-ethos-inline-layout-expansion.md`. Rulings 4 to 9
  carry «Datom expansion» 2nd ed. rulings 2 to 7 (F`8475a9/books/3-expansion-v2.md`).
- «Vertical ethos, the skill line», e5a0bc, one ruling: replace the hanging
  layout line in vision-ethos with the new-line style, indent two.
  https://claude.ai/artifact/Q3V7kZ26DH5VdpvD4JHJy8;
  F`e5a0bc/books/7-vertical-ethos-the-skill-line.md`. His later word is
  three spaces (contradiction 5).
- «The code», 2nd ed., e5a0bc, three rulings.
  https://claude.ai/artifact/YaukDkgd5hMCwr55QH8K4m.
- «Stored type and datom form», f5a6e9, five proposals (Encodable kind,
  Bytes and the hash, the flow id, the words, the shorthand).
  https://claude.ai/artifact/6cgk7UGUTyK9gCFULNtfLC;
  F`f5a6e9/books/5-stored-type-and-datom-form.md`.
- «Levels, tests, traits», d4ae97, proposal 3: vision-ethos variant order and
  traits. https://claude.ai/artifact/HuFye2HYkS5bEUnQGy76gp;
  F`d4ae97/books/7-levels-tests-traits.md`.
- «Curriculum's ethos, and every Nexus's three roots», d4ae97, two rulings,
  commented ("This is garbage."). https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU.
- «Curriculum, a vision in ethos», d4ae97, ten ethos files proposed.
  https://claude.ai/artifact/XJ2gicWJRFcC75CdyP2jyr;
  F`d4ae97/books/8-curriculum-vision-in-ethos.md`.
- «Astra's five candidates», 41fa34, proposal 5: the JSON and Datom bridge.
  https://claude.ai/artifact/3AXTdcjQjzqka5kFHCoLZw.
- «Ethos, distilled», 2nd ed., d4ae97: proposals 1 and 4 landed; the rest
  overtaken by e5a0bc's book 5 (F`d4ae97/log.md` line 112).
  https://claude.ai/artifact/5QcHZT4VEvBgAa5QWRHSvV.
- bad807's «Ethos» and «Datom» books, with ruling lists
  F`bad807/books/1-ethos.rulings.md` (roots, layout, inline payload name,
  one-field structs, what `Name.String` declares, comments, versions) and
  F`bad807/books/2-datom.rulings.md` (datom everywhere or only where needed;
  the flow id's type). Status unknown; bad807 is retired.
- The Jev subset of Ethos: ordered 2026-10-08, material gathered at
  F`d4ae97/reports/jev-ethos/material.md`, no book yet.

## 6. Cut

Quoted nowhere here, by path:

- `/home/li/primary/Vision/ethos.md` (older copy of vision-ethos);
  PS`vision-archive-ethos-monolith.md`; PS`vision-meaning.md` (its own
  topic); PS`vision-signal.md`, PS`vision-sema.md`, PS`vision-nexus.md`
  (in the Nexus file); every skill's `## Sources` list.
- Covered by the skills: F`91ea9f/vision/ethos.md` (2026-10-02: four
  roots, memory upgrade, vertical layout, KindWanted, closer on the last
  line); F`edf227/vision/ethosComments.md`; F`b80e55/vision/ethosInlineTypeDeclaration.md`;
  F`0625c3/vision/datom.md`; F`f6db8d/vision/arity.md`; F`26c50c/vision/ethos.md`
  (audit and process entries); F`d4ae97/vision/ethos.md` "Ethos is central,
  very central"; F`d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md`
  and `/home/li/primary/vision-raw/genericParametersAreTraits.md` (older
  forms of items 1 and 8).
- Relays of records quoted here: F`41fa34/vision/ethos-json.md`,
  F`41fa34/vision/ethos-and-example-datom.md`, F`41fa34/vision/expands-vertically.md`,
  F`41fa34/notion/clojure-flow.md`, F`0c85a3/vision/ethos.md`,
  F`0c85a3/vision/vision.md`, F`0c85a3/notion/vision.md`,
  F`aa887c/vision/ethos.md`, F`f768df/vision/flow.md`, F`8475a9/vision/flow.md`.
- Book presentation of ethos (a books topic): F`5ed94b/vision/visionBooks.md`,
  F`d66c26/vision/books.md`, F`d4ae97/vision/books.md`, F`e5a0bc/vision/books.md`;
  code generated from skills: F`d4ae97/vision/skills.md`.
- Meaning language: F`b7ba00/vision/meaningLanguage.md` (except two entries
  quoted in the Nexus file), F`93ba9f/vision/meaningLanguage.md`,
  F`b7da5d/vision/meaningLanguage.md`, F`b7ba00/notion/sema.md`,
  F`93ba9f/notion/semaCommunication.md`.
- Older or narrower: F`9993b5/vision/typedString.md`,
  F`9993b5/vision/datomStructuralEditing.md`, F`bcd02a/notion/ethos.md`,
  F`62022e8f/vision/multiFormConcepts.md`, F`88475f/vision/titles.md`,
  F`e51411/vision/titles.md`, F`f1c841/vision/ethos.md`.
- The remaining records of the 2026-10-08 census
  (F`d4ae97/reports/flow-ethos-census/census.json`, 1,376 records, and the
  147 left-out entries listed in its `topic-flow-context.md`).
