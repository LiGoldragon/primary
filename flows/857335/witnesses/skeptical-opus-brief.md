You are an independent skeptical audit subflow. The living explicitly requests this audit.
FLOW_ID: 564f55
FLOW_DIRECTORY: /home/li/primary/flows/564f55
Delegating execution lane and report destination: /home/li/primary/flows/857335

Do not create a flow lane or log. Record your harness thread/session ID as evidence provenance if available. Read NON_MANAGEMENT_AGENTS.md and the subflow and flow-evidence skills applicable to your work. The supplied FLOW_ID and FLOW_DIRECTORY are intentional and must remain unchanged.

Task: try to DISCONFIRM that the realized stack satisfies the full landed Vision and Intent below. Seek concrete counterexamples, missing requirements, semantic collapses, incomplete boundaries, and tests that falsely appear to prove compliance. This is not a request to praise or confirm the implementation. Equally, do not invent defects: explain rejected hypotheses and distinguish demonstrated failures, direct source findings, inferences and untested risks.

Audit these clean realized repositories and identify exact revisions inspected:
/git/github.com/LiGoldragon/protos main b543678cfc8609529cea7174eb4af8a64daa54ad (0.29.1)
/git/github.com/LiGoldragon/datom-codec main f2cc06858d38a4028c928d33323a6d682e7c222f (0.25.6), including crates/datom-codec-derive
/git/github.com/LiGoldragon/ethos-zero main 4695ee0c1f5d00dcf5cceba08f5fa00412b92184 (6.1.6)
Trace actual dependency/consumer boundaries where necessary, especially generated types and binary-versus-text compilation, but distinguish this released stack from unfinished consumer WIP.

The full ten documents appended below are the standard, with no unstated deferrals. Inspect architecture and actual executable behavior as well as API naming. Check both ascent and descent, context ownership, type-driven composition, arbitrary Rust derives and containers, syntax edge cases, errors and budgets, generated Ethos structures/kinds/imports, and all applicable Signal/Nexus requirements. Do not substitute green builds for design compliance. Do not read the other skeptical auditor's report or existing implementation/audit summaries before completing your independent report.

Read-only audit: do not edit repository sources, manifests, bookmarks, live configuration or services. Do not acquire write locks or deploy anything. Do not launch Nix builds, remote builders, or broad expensive test matrices; existing source/tests and focused lightweight reproductions are sufficient. Temporary scratch evidence may be written only in your own dedicated witness directory below. No nested auditors are required. No messages to external people.

Deliver a self-contained Markdown report. For each finding give severity, exact violated authority passage, source file/line/revision, minimal counterexample or evidence, why it matters, confidence and the smallest principled correction. State what you tested and actual outcomes, unresolved limitations, requirements inspected without findings, and rejected hypotheses. Finish with a Sources section. Do not say the stack is compliant if an applicable requirement is missing. Do not fix source code: the main flow reconciles the two independent reports before further Orchestrate work.

The latest living instruction explicitly authorizes the Codex audit on gpt-5.6-sol at medium effort, superseding an older temporary user-level no-Sol restriction for this audit. The Claude audit is explicitly claude-opus-5 at medium. Do not substitute another model or effort silently.

Your report: /home/li/primary/flows/857335/reports/skeptical-opus.md
Your scratch evidence directory: /home/li/primary/flows/857335/witnesses/skeptical-opus
Write the complete report as your final response; the launcher will preserve it at the report path. You may also write that report directly if supported.

===== /home/li/primary/Vision/protos.md =====
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
recognition of structures, nothing more. Protos examples show the
textual structure — the delimiters, the head, the capitalization, the
recursive structure — universally, at a very high level,
non-dialect-specific.

## Layers

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

## Every layer carries its own context

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

## Kinds are borne by the type converted and named for the layer it becomes

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

## Signal is parallel

Signal is not a layer of the chain: a parallel structure exchanging
compositions in one step, an rkyv serialization carrying our own
protocol.

## Delimiters

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

## Structure

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

## String, escape, error

The text type is `String`. A closing guillemet inside a string is
escaped with a backslash, so the ascent never refuses. The word is
error, not fault, through the chain.

```
«she said \»no\» and left»
```

## Multi-pass

Multiple passes are wanted over a single pass, because a single pass
creates corner-cutting bad design. The multiple steps create a mental
model of the machinery, which enforces a correctness in the code that
is millions of times more beneficial than the cost of doing these
multiple passes.

## Canonical print

It is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except inside the guillemets,
where every glyph is content and a space would be load-bearing. Space
the delimiters and the inner content.

===== /home/li/primary/Vision/datom.md =====
# Datom

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

Two string forms. The bare form: a run with no space and no delimiter
glyph, which may be a whole sentence written without spaces in any
casing; "word" does not do it justice, and its name is open, symbol
being Lisp's. The delimited form: guillemets, which keep the
doubleness of the double quote, cannot be mistyped for it, and point,
so the ends are visible at any size.

```
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
```

## Syntax

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

Everything moves to Datom, and no Dotos file remains. Datom's own line
of descent is NOTA, which also passed through the temporary name
Dotos; that old notation stays behind, frozen, and may be called
legacy. Schema is the abandoned ancestor of Ethos, not of Datom. The
library is named datom-codec so that datom is free for the datom
nexus, which comes when there is more to do: translating datom objects
between formats, and a parsing cache keyed by the content-addressed
hash of normalized text.

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

===== /home/li/primary/Vision/ethos.md =====
# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

## Why Ethos

All the legacy languages have a high noise ratio. Some lisps came
close but lacked the correctness of Rust or Haskell; those have the
correctness but allow no higher layer of abstraction that keeps the
correctness of the whole. Ethos writes the mental model and the code
in one swoop.

## Roots

Library, Signal, Sema, Nexus. No version in a file. Signal's sections
are queries and responses, since there is communication; Nexus's are
input and output, runtime words; Sema's are record types, the rest to
be decided.

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

## Imports

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

## What a declaration turns into

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

## Every declared type bears both kinds

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

## The datom kinds are compiled in only where text is spoken

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

## Kinds are explicit; bodies are hand-written

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

## Kind syntax

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

## Associations

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

## Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.

## Generation

By request to the Ethos Zero daemon, committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```

===== /home/li/primary/Vision/signal.md =====
# Signal

## Name

The serialized form is called signal.

## What signal is

Signal is the messaging layer: fully binary, portable rkyv fixed
across endianness, fully typed with both sides knowing the full
schema, nothing on the wire labeling itself. It is one step from the
composition, beside the text chain.

## Query and response

A Signal declares queries and responses; input and output are too
low-level for it.

```
Signal
[]                                     ; imports
[ Lock.LockRequest  Release.LockId ]   ; queries
[ Locked.Lock  Released.Lock ]         ; responses
[ LockId.Integer                       ; types
  LockName.String
  LockRequest.{ LockName }
  Lock.{ LockId LockName } ]
```

## Text and signal

The textual form is datom; a CLI actualizes it and sends signal; a
Nexus never textualizes.

## Meta signal

The meta signal is never optional: the daemon is configured only over
its meta surface.

## Universal signal

Universal signal is a CapnProto implementation of Ethos. Not built.

===== /home/li/primary/Vision/sema.md =====
# Sema

## What sema is

Sema is the database engine of a Nexus, authored in Ethos so the
stored types are visible; its root, Sema, declares record types. It
matters more than nexus, because operational editing should yield the
migration with the edit.

```
Sema
[]                                                        ; imports
[ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
                                                          ; the remaining sections are to be decided
```

===== /home/li/primary/Vision/nexus.md =====
# Nexus

## A Nexus is the whole

A Nexus is the whole long-running component: the process, its
sockets, and the signal contracts it is compiled with. Daemon is
retired as the name of the thing. Every Nexus is named
component-nexus — orchestrate-nexus, ethos-nexus — and in everyday
speech orchestrate-nexus is called orchestrate.

## A kind of thing

A Nexus is not a thing; it is a kind of thing.

## The nexus core

The core logic of a Nexus, distinct from the daemon component, is the
nexus core or the nexus kernel, interchangeably; its Ethos sections
are input and output.

## Library and daemon

Nexus is the universal library for all nexuses; the daemon lives in
Ethos Zero.

## Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

## Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

## Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

## Sockets

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

## Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

## The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

## Routing

Signals cross the network through a router. The router tells signal
types apart by an enum, held in a universal signal repository every
component depends on, which wraps the objects. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

## First configuration

A Nexus keeps a standard metadata tree. In it a type records whether
the meta Configure was ever done; that record is reversed only on the
meta socket, and while it is unset Configure is accessible on the
ordinary socket. The tree holds everything standard about the Nexus:
its socket paths — its own and those of every edge-socket it connects
to — and whatever else comes up as standard nexus configuration data.
The built-in default configuration is independent of this and is
what gives the socket path on which the Configure signal arrives.

## Repositories

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

## Why everything is a Nexus

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

## Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

## Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

## Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

## Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.

===== /home/li/primary/Intent/anatomy.md =====
# Anatomy

## Code is written anatomically

Code is written anatomically and directly: the logic is read through
the ontology of the trait system. Datom and Ethos Zero are the parts
that must be solid.

===== /home/li/primary/Intent/conversion.md =====
# Conversion

## A kind names one conversion

A kind names one conversion and is borne by the type that undergoes
it, named for the layer it becomes. Each step yields a wholly new
type. A chain is composed in the open, never folded into a kind on its
first type.

===== /home/li/primary/Intent/context.md =====
# Context

## Every layer carries its own context

A value at any layer carries the context it makes sense in, and no
layer carries a fact that belongs to another.

===== /home/li/primary/Intent/mandatoryTraits.md =====
# Mandatory traits

## 2026-08-13 — approved

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
