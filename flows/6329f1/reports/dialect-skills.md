# Dialect skills report

Branch `DialectSkills` at `e287ae0f` on `Curriculum`, pushed to origin.
Worktree: `/home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1`.
Lock 639 held on the worktree.

Three skills drafted for living approval, not landed on main.

## Judgment calls

- **protos skill**: Listed all six delimiter pairs in one table with what each encloses in each dialect, since agents need to know which glyph to reach for. Included the four layers and the kind table because an agent touching protos needs the descent/ascent vocabulary. Did not include the protos.ethos declaration — too much internal detail for a skill; the table and the rules suffice.
- **datom skill**: Used the Person struct, vector, map, variant, and Meaning examples verbatim from Vision/datom.md. The CLI example uses the witnessed orchestrate reply. Showed the Datomic trait and the actualize/textualize call sites as the living requested ("datom and ethos should show some rust code"). Used `incorporate` and `datomize` as the capability names per the design spec; used `Corporal<Datom>` as the supertrait per the landed code.
- **ethos skill**: Used the Library example from the design spec (Record/Report), not from Vision/ethos.md (which had the not-yet-landed declaration), because the design spec's example aligns with what the code actually does. Signal example from the design spec. Showed target Rust beside every form per the ruling (ad19b1). The complex kind Streamable example is from the design spec. Imports use the colon separator per the witnessed ethos files. Listed intrinsics from the design spec.
- **Vocabulary**: Used "kind" everywhere, never "trait" except in Rust target examples. Used "position" for datom field locations. Used "structure" for protos textual units. Used "capability" for kind methods.
- **Dependencies**: protos has none. datom depends on protos. ethos depends on protos and datom.
- **Form**: Matched the existing Curriculum skills — YAML frontmatter with description and dependencies, terse imperative body, no skill variables needed (these skills describe languages, not installed tools).

## Full text

### skills/protos.md

```
---
description: Reading or writing any protos dialect, or touching the protos crate.
dependencies: []
---

Protos is the universal textual structure every dialect shares. It owns the only character reader and the only character writer. A dialect receives already-delineated structure and supplies its own types.

## Delimiters

Six delimiter pairs, four structural and two opaque:

| glyph | name | encloses |
|---|---|---|
| `{ }` | Braces | struct in datom; struct in ethos |
| `[ ]` | Brackets | vector in datom; enum, bracket of kinds, capability list in ethos |
| `« »` | Guillemets (U+00AB/U+00BB) | map: key value key value by position |
| `< >` | Angles | kind constraints: `Vector<Text>`, `Processable<[Clonable Sendable] Serializable>` |
| `“ ”` | Curly quotes (U+201C/U+201D) | opaque string: every glyph inside is content until the closing quote; no escapes |
| `( )` | Parentheses | opaque, read by balance: nesting counted, closing at the matching parenthesis; `\(` and `\)` escape unmatched parentheses |

## Separators

`.` Period, `!` Exclamation, `:` Colon. Inside a bare run a separator splits head from body when a non-whitespace, non-closing character follows: `Some.42` is Headed(Some, Period, Bare 42); `Reviewer.{` is Headed with an enclosed body. A separator followed by whitespace, a closer, or end of text is a MissingBody fault; a run beginning with a separator is a MissingHead fault.

## Heads

A head is a symbol. A headed structure is a head, a separator, and a body: the dot is the default separator, written right after the head, and it opens the body's delimiter. `a:b:c` chains right-associatively.

## Bare words

A bare word is a maximal run of characters containing no whitespace and no delimiter glyph.

## Comments

A single `;` opens a comment to end of line. Comments are never printed.

## Canonical spacing

`{ a b }`, `[ a b ]`, `« k v k v »` — one space inside at both ends when non-empty; `{}` `[]` `«»` when empty. Angles tight: `<a b>`. `Head.body` with nothing around the separator. Siblings one space apart. Opaque regions verbatim with their glyphs. One line.

## Layers

| layer | type | descent (may fault) | ascent (cannot fault) |
|---|---|---|---|
| Text | `protos::Text`, `protos::Potential<T>` | `Structural::delineate` on Text -> `Delineation` | -- |
| Protoform | `protos::Protoform`, `protos::Delineation` | `Conceptual<C>::conceive` on Protoform -> C | `Printing::print` -> Text |
| Concept | the dialect's data model | dialect-specific (datom: `Datomic::incorporate`) | `Protosizable::protosize` -> Protoform |
| Corporal | the Rust value | -- | dialect-specific (datom: `Datomic::datomize`) |

Descent is realization and may fault. Ascent is textualization and cannot fault. `Actualizable<T>::actualize` on `Potential<T>` chains the whole descent. `Textualizable::textualize` chains the whole ascent.

## Kinds

| kind | layer | what it does |
|---|---|---|
| Structural | Text | `delineate` -> `Delineation` |
| Protosizable | Concept | `protosize` -> `Protoform` |
| Conceptual\<C\> | Protoform | `conceive` -> C |
| Actualizable\<T\> | Potential | `actualize` -> T (blanket: delineate, conceive, incorporate) |
| Printing | Protoform | `print` -> Text |
| Corporal | -- | the bound borne by every corporal type; each dialect defines its own |
| Embodied | -- | alias of Sized |

## What protos does not know

Protos has no struct, no vector, no map, no integer, no string, no interpretation. What a structure means is said by the dialect, never by protos alone.
```

### skills/datom.md

```
---
description: Constructing, reading, or interpreting datom, or implementing Datomic.
dependencies: [protos]
---

Datom is the pure-data dialect on the protos substrate. It carries data, strictly typed, and its whole work is serialization and deserialization. Schema-driven and positional: the reader walks the expected type, writing is the exact reverse projection. All naming lives in the type; the text carries only the data.

## Text forms

Each form occupies the position its type declares. What a structure means is said by the position, never by the structure alone.

Struct — braces, positional:
```
; Person: a struct of name Text, born Integer, address Address, roles Vector<Role>.
{ Ada 1990 { “12 Rue de la Paix” Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }
```

Vector — brackets:
```
[ 0 42 -42 ]
```

Map — guillemets, key and value by position:
```
« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »
```

Variant — a head alone for a variant carrying nothing; a head, the dot, and a body for a variant carrying data:
```
Pending
Accepted.{ 42 “2026-09-03T17:46:20” }
Observed.Locks.[]
```

String — bare when it contains no space and no delimiter; curly-quoted otherwise. In a string position a bare word may contain characters that are syntax elsewhere:
```
Ada
“no such file: { } is content”
name:first
```

Integer — bare ASCII decimal, optional leading `-`, no `+`, no leading zero except `0` itself:
```
0  42  -42
```

Decimal — finite, point-mandatory, no exponent:
```
3.14  -0.5
```

Boolean:
```
True  False
```

Meaning — parenthesized text, read by balance:
```
(The build passed on the third try (after two timeouts))
```

## The CLI

A datom-speaking CLI takes exactly one inline datom value and no flags. Its type system is the only interface.

```sh
orchestrate 'Lock.{ MyLock 6329f1 [ /abs/path ] “why I hold it” }'
# -> Locked.{ 442 MyLock 6329f1 [ /abs/path ] “why I hold it” }
```

With no argument, a CLI prints its contract's ethos.

## Datomic in Rust

A Rust type bears `Datomic` through two capabilities — `incorporate` (static, constructs the value from a `Datom`) and `datomize` (projects the value into a `Datom`):

```rust
// The kind: every corporal type that crosses the text boundary.
// incorporate is static (:), datomize takes self (.).
trait Datomic: Corporal<Datom> {
    fn incorporate(datom: &Datom) -> Result<Self, Fault>;
    fn datomize(&self) -> Datom;
}
```

`Potential<T>::actualize()` chains the whole descent — delineate, conceive, incorporate — and may fault. `Textualizable::textualize()` chains the whole ascent — datomize, protosize, print — and cannot fault:

```rust
let potential = Potential::<Lock>::from(text);
let lock: Lock = potential.actualize()?;
let text: Text<Lock> = lock.textualize();
```

Every ethos-declared type gets its `Datomic` generated. No hand-written Datomic implementations for declared types.
```

### skills/ethos.md

```
---
description: Writing or reading an ethos file, or generating Rust from one.
dependencies: [protos, datom]
---

Ethos is the schema language. It specifies the types; datom fills them with data. Ethos generates the Rust.

## File roots

Two roots: `Library` and `Signal`. A file is one sweet ethos object; the outer braces are omitted and always implied:

```
; A Library file (sweet form). The full form wraps everything in Library.{ … }.
Library.{0 1 0}
[ protos:[Text Textualizable] ]                                ; imports
[ Record.{ Text Integer }                                      ; types
  Report.{ Text Vector<Integer> } ]
[ Textualizable.[ textualize.[ Text ] ] ]                      ; kinds
[ Report.[ Textualizable ] ]                                   ; associations
```
```rust
struct Record(protos::Text, protos::Integer);
struct Report(protos::Text, Vec<protos::Integer>);
impl Textualizable for Report { /* … */ }
impl datomic::Datomic for Record { /* generated */ }
impl datomic::Datomic for Report { /* generated */ }
```

```
; A Signal file (sweet form).
Signal.{1 0 0}
[]                                                             ; imports
[ Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]  ; requests
[ Locked.Lock  LockRejected.LockRejection  Released.Lock  ReleaseRejected.ReleaseRejection  Observed.Observation ]
[ LockId.Integer … ]                                            ; types
```
```rust
enum Request { Lock(LockRequest), Release(LockId), Observe(ObserveSelection) }
enum Reply { Locked(Lock), LockRejected(LockRejection), /* … */ }
```

## Type declarations

`Name.{ … }` — a struct. Positions are unnamed; the type carries the shape:
```
Sink.{ Text Vector<Text> }
```
```rust
struct Sink(protos::Text, Vec<protos::Text>);
```

`Name.[ … ]` — an enum. Each variant bare or carrying an inline payload:
```
SinkError.[ Closed Full ]
LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]
```
```rust
enum SinkError { Closed, Full }
enum LockRejection { DuplicateName(Lock), PathOverlap(LockOverlap) }
```

`Name.Type` — an alias:
```
LockId.Integer
Roles.« Text Integer »
```
```rust
type LockId = protos::Integer;
type Roles = BTreeMap<protos::Text, protos::Integer>;
```

## Kinds

A kind is the bearer of capabilities. The `.` receiver takes self, `!` takes mutable self, `:` takes no self.

Simple kind — capabilities in a bracket:
```
Summarizable.[ summarize.[ Text ] ]
```
```rust
trait Summarizable { fn summarize(&self) -> protos::Text; }
```

Complex kind — a struct of superkinds, associated types with their constraints, associated constants in `« UPPER_CASE Type »`, and capabilities:
```
Streamable.{ [ Fillable ]
             [ Item<Serializable> ]
             « CAPACITY Integer »
             [ next![ Option<Item> ] ] }
```
```rust
trait Streamable: Fillable {
    type Item: Serializable;
    const CAPACITY: protos::Integer;
    fn next(&mut self) -> Option<Self::Item>;
}
```

A capability's inputs and yield are each a bracket holding one type:
```
push!{ [ Text ] [ Result<Integer SinkError> ] }
create:[ Self ]
```
```rust
fn push(&mut self, input: protos::Text) -> Result<protos::Integer, SinkError>;
fn create() -> Self;
```

Kind identity is the name and the constraints, written as one head:
```
Processable<[Clonable Sendable] Serializable>.[ … ]
```
```rust
trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
```

## Associations

A type bears a kind:
```
[ Sink.[ Summarizable Fillable ] ]
```
```rust
impl Summarizable for Sink { /* … */ }
impl Fillable for Sink { /* … */ }
```

Every ethos-declared type gets `impl datomic::Datomic` generated from its anatomy.

## Imports and intrinsics

`[ protos:[Text Textualizable] ]` imports names from another library. Intrinsic names known without import: Text, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

## Generation

`ethos-zero` generates the Rust. Generated Rust is committed; a freshness test asserts the committed output matches a fresh generation. The CLI speaks datom:

```sh
ethos-zero 'Generate.{ /abs/file.ethos /abs/out-dir }'
# -> Generated.[ /abs/out-dir/signal.rs ]
```

With no argument, `ethos-zero` prints its own ethos.

## Non-repetition

Any repetition in ethos syntax is an implementation failure.
```

## Sources

- Vision/protos.md, Vision/datom.md, Vision/ethos.md — distilled vision
- Intent/protosParsing.md — intent on parsing
- flows/e8c4cc61/vision/ethosFileAnatomy.md — the living's handwritten page
- flows/6329f1/log.md ## Design — the synthesis spec
- protos 56c683ec README and protos.ethos — landed code self-description
- datomic a27f9b8e README and datomic.ethos — landed code self-description
- ethos-zero 185f13a9 README, ethos-zero.ethos, signal.ethos — landed code self-description
- POC witness and final witness in flows/6329f1/reports — verbatim CLI output
