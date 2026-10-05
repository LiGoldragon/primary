Psyche Fable, the Primary designer; only the secretary Psyche Opus talks to it.

## Skills to load

- spirit
- psyche
- psyche-interraction
- vocabulary
- behavior
- main-flow
- skill-designing
- psyche-distillation
- vision-ethos
- datom
- vision-nexus
- vision-flow
- operation-book
- trial-presentation-book
- operation-relaying-the-living
- compensation-messenger-clj
- prompt-crafting
- knowledge-flow
- knowledge-nexus
- trial-succession

## flows/bad807/books/1-ethos-v2.md

<!-- to-the-living:start -->
Presentation.{ «Ethos» }

Fifteen proposals and nine rulings on ethos, one change each.

## How it is now

### The vision files
- `Vision/ethos.md`, 442 lines. Its Roots: Library, Signal, Sema.
- Its headings: What Ethos is, Why Ethos, Roots, Non-repetition, Self-description, Horizon, Kind, Naming, Identity, Declaration: File, Imports, What a declaration turns into, Inline types, the two variant sections, the datom-kinds sections, Shapes and placement, Kinds are explicit, Kind syntax, Associations, Spacing, Zero, Generation.
- `Vision/sema.md`, 15 lines: Sema is the database engine, with a Sema root of record types.
- `Vision/archive-ethosMonolith.md` keeps the words behind Zero.

### ethos-zero 16.0.0
It reads four roots, Library, Signal, Operation, Memory. A `Sema` head is refused, as witnessed today:

```
Rejected.{ … { 1 1 } Conceptual.{ [ 0 ] Renamed.Memory } }
```

- It prints vertically, and drops comments from the print.
- It accepts one-field structs, and writes `Name.String` as `pub type`.
- It names a variant's inline payload `<Variant>_Data`.

[drawing: ethos file to ethos-zero to Rust to the Nexus and the CLI]

*How ethos-zero 16.0.0 runs today: one ethos file becomes one Rust module, which the Nexus and the CLI both compile.*

### The ethos files in the workspace
89 `*.ethos` files under `/git/github.com/LiGoldragon`, by the root they head:

| Signal | Library | Interface | Nexus | Sema | Memory | Operation |
|---:|---:|---:|---:|---:|---:|---:|
| 45 | 27 | 12 | 2 | 2 | 1 | 0 |

They hold 389 comment lines in 4,122, and 237 one-field structs in 42 files.

### Crates that pin ethos-zero
48 crates pin it: 21 at 9.0.0, 13 at 10.0.0, 3 at 16.0.0, the rest from 0.7.1 to 15.0.0.

### Where vision lives
On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills.
Each [vision] proposal names its Vision/ file as its home today, and travels with the migration.

## Proposals

### 1. What Ethos is
[vision] `Vision/ethos.md`, heading What Ethos is. Ground: "effective compliance with ethos".

**Now:** "Ethos is the schema language. Of the two main syntaxes most agents will face, Ethos specifies the types and Datom fills them with data."

**Proposed:**
> "Ethos is the typed spec every Nexus is programmed from. Every runtime component is a Nexus, and every Nexus has an ethos; reading it shows the main objects and processes the component deals with.
>
> Ethos specifies the types and datom fills them with data. Ethos compiles to Rust: ethos-zero reads an ethos file and writes the Rust module the Nexus is built on."

### 2. Roots
[vision] `Vision/ethos.md`, heading Roots. Assumes (b) of Ruling 1. Ground: "signal, operation, and memory".

**Now:** "Library, Signal, Sema. No version in a file. Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types."

**Proposed:**
> "Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says: imports, queries, responses, types. Operation declares what it does, one operation for every effect: imports, operations, outcomes, types.
>
> Memory declares what it remembers: imports, record types. Library declares what they share: imports, types, kinds, associations. A signal reaches memory only through operation, and returns through operation."

[drawing: the four roots of one ethos]

*The roots of one ethos: a signal reaches memory only through operation; Library feeds all three.*

```
Operation
[ lock:[ Lock LockName ] ]      ; imports: the types the lock Library shares
[ Take.Lock                     ; operations: one for every effect
  Free.LockName ]
[ Taken.Lock                    ; outcomes
  Failed.[ Held.Lock
           Unknown.LockName ] ]
[]                              ; types
```
ethos-zero 16.0.0 writes, derives left out:
```rust
pub enum Operation { Take(lock::Lock), Free(lock::LockName) }
pub enum Failed_Data { Held(lock::Lock), Unknown(lock::LockName) }
pub enum Outcome { Taken(lock::Lock), Failed(Failed_Data) }
```

### 3. What sema is
[vision] `Vision/sema.md`, heading What sema is. Assumes (b) of Ruling 1. Ground: "Yeah the memory is good".

**Now:** "Sema is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Sema, declares record types. It matters more than nexus, because operational editing should yield the migration with the edit."

**Proposed:** "Sema is the database engine of a Nexus. What it stores is declared in the Memory root of the Nexus's ethos, so the stored types are visible, and an edit to that root yields the migration with the edit."

```
Memory
[ lock:[ LockId LockName FlowId ] ]   ; imports
[ Lock.{ LockId                       ; record types: one lock as stored
         LockName
         FlowId } ]
```

### 4. Everything is a type
[vision] `Vision/ethos.md`, new heading Everything is a type, after Non-repetition. Now: no such section. Ground: "everything is a variant of a set".

**Proposed:**
> "Everything is a type, because everything is a variant of a set; an instance is one member of a population. For engineering reasons not everything becomes an enum: the open-ended variants are names.
>
> Ethos has no key-value map, since a map is a poorly specified struct; a position is a type, never a key, and datom carries no field names."

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: a path is its own type
  GenerationFailure.[ SyntaxError.Vector<FilePath>
                      Unwritable ] ]       ;   an enum, no keys anywhere
[]                                         ; kinds
[]                                         ; associations
```
The datom, a variant with no field names:
```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]
```

### 5. An ethos edit is the data migration
[vision] `Vision/ethos.md`, new heading, after Declaration: File. Now: no such section. Ground: "which becomes the migration itself".
Assumes (b) of Ruling 6, versions held outside the file, and upgrade-from.

**Proposed:**
> "A change to ethos is operational: the edit to a Memory root is itself the operation that migrates the stored data into its new format. The Memory kind carries a standard successful or unsuccessful change on its record types, and each version carries the upgrade from the version before it.
>
> Versions are held by the Nexus that stores the records and by its manifest, never in the ethos file. Ethos is specified in its own ethos, so the same holds for ethos itself and for every proto family, datom included."

The upgrade-from choice follows a leaning he left open.

[drawing: the upgrade mechanism]

*The upgrade mechanism, not yet built: ethos-zero 16.0.0 generates no upgrade operation.*

### 6. Layout
[vision] `Vision/ethos.md`, heading Spacing, renamed Layout. Assumes (b) of Ruling 2. Ground: "a language that expands vertically".

**Now:** "Space the delimiters and the inner content. Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty."

**Proposed:**
> "Ethos expands vertically. A structure with more than one element, one of which has a next layer, opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line and never takes a line of its own.
>
> Elements that are all leaves sit on one line. A space stands inside every non-empty bracket and brace. Inline nesting goes about three deep; past that, the type comes from a Library, where three more levels open."

```
Signal
[]                                   ; imports
[ Lock.{ LockName                    ; queries: take a lock by name for a flow
         FlowId }
  Release.LockId ]
[ Locked.Lock                        ; responses
  Refused.[ Held.Lock
            Unknown ] ]
[ LockId.Integer                     ; types
  LockName.String
  FlowId.Integer
  Lock.{ LockId LockName FlowId } ]
```

### 7. Comments
[vision] `Vision/ethos.md`, new heading Comments, after Layout. Assumes (a) of Ruling 5. Now: no such section. Ground: "so that I can see what the machine is seeing".

**Proposed:** "Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there. A comment runs from ; to the end of the line, and it is kept wherever the ethos is printed."

### 8. ethos-zero prints comments
[implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, section Print, line 156. Built on a yes to Ruling 5 (a). Ground: "what the machine is seeing".
Witness: `ethos-zero` with no argument prints `ethos-zero.ethos` without its 10 leading comment lines.

**Now:** "section on its own line; comments are not printed."

**Proposed:** "section on its own line; each comment is printed where it was written, at the end of its line or on the line above the structure it names."

### 9. Inline types
[vision] `Vision/ethos.md`, heading Inline types. Assumes (b) of Ruling 3. Ground: "a variant and a struct name be the same thing".

**Now:** "A type may be declared where it is used. The inline struct or enum is a full type whose derived name carries an underscore, non-idiomatic for a Rust type, so it never collides and reads at a glance as inferred from the sugar."

**Proposed:** "A type may be declared where it is used. A variant's inline payload is a full type that takes the variant's own name, as a struct position's inline type already does; a second declaration of that name in the file is refused as a duplicate."

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   a struct named Unwritable, after its variant
[]                                                        ; kinds
[]                                                        ; associations
```

### 10. One position is a new type
[vision] `Vision/ethos.md`, new heading, after What a declaration turns into. Assumes (a) of Ruling 4. Now: no such section. Ground: "This should be a new type".

**Proposed:** "A struct holds two or more positions. A type with one position is written as its name, a dot and the contained type, `HarnessName.String`; a struct of one position is refused. A variant with one payload carries it after the dot, with no braces."

```
Signal
[]                                         ; imports
[ HarnessStatusQuery.HarnessName ]         ; queries: the payload after the dot, no braces
[ HarnessStarted.HarnessName ]             ; responses
[ HarnessName.String ]                     ; types: one position, a new type
```

### 11. ethos-zero names payloads and refuses one-field structs
[implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, lines 92 and 93. Built on a yes to Ruling 3 (b) and Ruling 4 (a). Ground: "refuse single-field struct types".
The refusal would meet 237 one-field structs in 42 of the 89 files.

**Now:** "capture those names. A variant `Name.{ T1 T2 }` carries a generated struct `Name_Data` with one field per position."

**Proposed:** "capture those names. A variant `Name.{ T1 T2 }` carries a generated struct `Name` with one field per position. A struct of one position, `Name.{ T }`, is refused as `Conceptual.{ [ path ] OnePosition.Name }`."

### 12. Kind
[vision] `Vision/ethos.md`, heading Kind. Assumes (b) of Ruling 7. Ground: "If I say traits I mean kinds".

**Now:**
> "Kind is the word for the bearer of capabilities: something that can run is a runner, Runnable is its kind, and run is its capability, a function the kind has. Trait is set aside as acoustically ambiguous.
>
> In ethos there are no generics, only kinds. Declaring a new kind declares a new trait in the Rust world and might imply more in the ethos world."

**Proposed:**
> "Kind is the word for the bearer of capabilities: something that can launch is launchable, Launchable is its kind, and launch is its capability. When trait is said, kind is meant; trait stays the Rust word for what a kind generates.
>
> In ethos there are no generics, only kinds: what a capability takes is another kind, never a type. Declaring a new kind declares a new trait in the Rust world."

```
Library
[ protos:Textualizable ]                   ; imports
[ LaunchError.[ Busy Unreadable ] ]        ; types
[ Launchable.[ launch!{ [ Textualizable ]  ; kinds: a launchable takes a textualizable brief
                        [ Result<Self LaunchError> ] } ] ]
[]                                         ; associations
```
ethos-zero 16.0.0 writes, derives left out:
```rust
pub trait Launchable {
    fn launch<N: protos::Textualizable>(&mut self, input: N) -> std::result::Result<Self, LaunchError>
    where Self: Sized;
}
```

### 13. Horizon
[vision] `Vision/ethos.md`, heading Horizon. Assumes (a) of Ruling 8 for today. Ground: "write the whole program directly in Ethos".

**Now:** "Ethos will eventually replace everything, Rustlang becoming its assembly layer. Designs are chosen for that horizon; what it enables — generator emission among it — comes in its time."

**Proposed:**
> "Ethos will eventually replace everything, Rust becoming its assembly layer. Today ethos declares the types and kinds and ethos-zero compiles them to Rust; the bodies are written by hand, in Rust shaped so that a signal reaches memory only through operation.
>
> The whole program written in ethos needs a function syntax, implementations on kinds, and a manifest for compiling and finding dependencies."

### 14. Move the 9.0.0 pins to 16.0.0
[implementation] `/git/github.com/LiGoldragon/signal-harness/Cargo.toml`, line 28, and the same line in the 20 other crates pinned to 9.0.0. Each crate is regenerated and its rkyv dependency added.
Rests on a witness, no record of his: 9.0.0 reads no Operation or Memory root.

```toml
# Now
ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = …the 9.0.0 commit }
# Proposed
ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = …the 16.0.0 commit }
```
The 20 other crates:
```
chroma                   claude-answers           meta-signal-aggregator
meta-signal-criome       meta-signal-harness      meta-signal-mentci
meta-signal-mirror       meta-signal-persona      meta-signal-repository-ledger
meta-signal-router       meta-signal-spirit       signal-aggregator
signal-criome            signal-introspect        signal-mentci
signal-mind              signal-repository-ledger signal-router
signal-spirit            signal-spirit-judge
```

### 15. Structs over chained variants
[vision] `Vision/ethos.md`, new section. His comment on the anatomy block of «The Nexus» asked for a Field variant, and noted that `.Layer` was repeated per variant. Now: no such section.

**Proposed:**
> "When every data-carrying variant of a variant type would carry the same type, the type is a struct with a variant field, not a variant chain. Two variants in a row is the most a chain carries; past that, a struct."

```
Voice.{ Aspect Layer }                          ; a struct of aspect and layer
Aspect.[ Psyche Mind Field ]                    ; the variant field
; never: Voice.[ Psyche.Layer Mind.Layer Field.Layer ]
```

The flow applies it to its books' example code; a flow's role is named `Role.[ Voice … ]`.

## Rulings

| Ruling | (a) | (b) |
|---|---|---|
| **1. Roots** | Three roots, Library, Signal, Sema: `Vision/ethos.md` Roots; 2026-09-10. | Four roots, Library, Signal, Operation, Memory: 2026-10-02. |
| **2. Layout** | One declaration per line, delimiters spaced, as the protos print: `Vision/ethos.md` Spacing, as of 2026-09-11, dated by commit. | Vertical expansion about three deep, the closing delimiter ending the last line: 2026-10-02. |
| **3. The name of a variant's inline payload** | Derived with an underscore, `Unwritable_Data`, so it never collides: 2026-09-09; ethos-zero 16.0.0. | The variant's own name, shared by variant and struct: 2026-09-30. |
| **4. One-field structs, and what `Name.String` declares**<br>The flow reads the second as part of the first, a departure from the new-type form he asked for. | A one-field struct is refused, and `Name.String` is a new type of its own: 2026-09-08. | A one-field struct is accepted, and `Name.String` is a Rust alias, `pub type Name = String`, bearing no derive: `Vision/ethos.md`; ethos-zero since 2026-09-10, dated by commit; 42 files use it. |
| **5. Comments** | A comment on every section and next-layer line, kept: 2026-10-03. | Comments read and dropped from the print: ethos-zero README, 16.0.0, 2026-10-02, dated by commit. |
| **6. Versions** | No version in an ethos file: 2026-09-09. | Ethos versions, each with its upgrade: 2026-09-29; 2026-10-02. |
| **7. Trait or kind** | Trait set aside as acoustically ambiguous: 2026-08-26. | Kind meant when trait is said, trait still said for Rust: 2026-09-11; 2026-09-24. |
| **8. Bodies by hand, or the whole program in ethos** | Ethos types and kinds, implementations written by hand: 2026-10-04. | The whole program in ethos within a few months: 2026-09-25; 2026-09-29. |
| **9. Chained variants**<br>Proposal 15. | A variant type may chain a payload per variant, `Voice.[ Psyche.Layer Mind.Layer ]`: the books before this one. | A struct with a variant field, `Voice.{ Aspect Layer }`: his comment on «The Nexus». |
<!-- to-the-living:end -->


## flows/bad807/books/2-datom-v2.md

<!-- to-the-living:start -->
Presentation.{ «Datom» }

## How it is now

### In Vision
```
Vision/datom.md      315 lines
  sections   Name · Nature · A datom is a form at a path · Strings · Syntax
             The datom composes · Any Rust type · From text and back
             Containers · Errors · Omittable fields · The interface shape
             De/serialization · Relation to Ethos · Repository · Map and Meaning
  forms      bare and «» strings · { } struct · [ ] vector · Head. variant
  absent     field names · map
Vision/protos.md     datom = the pure-data protos dialect
                     signal = a parallel structure beside the text chain
Vision/signal.md     43 lines, names no formats
  sections   What signal is · Query and response · Text and signal
             Meta signal · Protocol
Vision/ethos.md      "The datom kinds are compiled in only where text is spoken"
                     → no datom-codec in a Nexus build
                     its Signal example declares FlowId.String
```

Nowhere in Vision yet: where datom is used, the two formats, the flow id's type, how a new object is shown.

### In code
```
datom-codec 0.32.2   /git/github.com/LiGoldragon/datom-codec, 1689 lines of src/
  Form = Struct · Vector · Variant · Bare · String · Meaning · Decimal
ethos-zero 16.0.0    emits on every type:
  #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
signal-flow 10.0.0   ethos/signal.ethos line 116:
  FlowId.String
```

Datom lines in proposals 3, 7, 8, 9: checked with datom-codec 0.32.2.
Rust blocks: ethos-zero 16.0.0 output (in 3, derive lines left out, one struct per line).

## 1. Where datom is spoken · vision

`Vision/datom.md`, new section after "The interface shape". Assumes Ruling 1 (b). Now: no such section.
The living: "where the program doesn't need it".

### Proposed
````markdown
## Where datom is spoken

Datom is spoken wherever text meets a typed program. A CLI takes one
inline datom and answers with one; a message between machines is a
datom; a title is a datom. A program that reads no text speaks no
datom: a Nexus speaks signal and is built without datom-codec, and a
messenger carries what it is given and forces no datom on it. A tool
that requires datom says so in its own skill. A response given as
datom is a datom as a whole, its prose a Markdown string inside it.
````

### The logic
[drawing: Does the program read text?]

*Text decides: where a program reads text, datom; where it does not, none.*

## 2. Datom beside protos and signal · vision

`Vision/datom.md`, new section after "From text and back". Now: no such section.
The living: "without needing to know how to deserialize".

### Proposed
````markdown
## Datom beside protos and signal

Protos reads the structure of the text and knows nothing of meaning.
Datom gives each structure the meaning its position states. The
composition is the value itself. Signal carries a composition from one
program to another in one step, with no text. A Nexus never handles
datom: the CLI, built with the datom feature, actualizes the text and
sends signal; the Nexus answers in signal, and the CLI textualizes
the answer. Datom lives only on the side that faces text.
````

### The flow
[drawing: CLI, built with the datom feature]

*Datom text → codec → typed signal → Nexus; the answer comes back as signal and the CLI writes it as text.*

## 3. One query, two formats · vision

`Vision/signal.md`, new section after "Query and response". Now: no such section.
The living: "cast into a different container".

### Proposed
````markdown
## Formats

A Signal defines the formats its communication takes. The simple
format and the extended format carry the same data cast into
different containers: the simple one leaves out the flow id and what
only the technical side needs, the extended one carries them. Common
queries and responses use the simple format. The extended format is
for debugging and for components that need richer compatibility with
each other; a CLI can use it, though it rarely does.

```
Signal
[]                                          ; imports
[ Ask.Asking ]                              ; queries
[ Answered.Answer ]                         ; responses
[ FlowId.{ Integer }                        ; types
  Role.[ Voice Implementer Auditor ]
  Question.String
  Answer.String
  Asking.[ Simple.{ Role Question }         ; the simple format: no flow id
           Extended.{ FlowId Role Question } ] ]  ; the extended format
```
```
; datom, each in a position expecting Asking
Simple.{ Voice «which locks are held» }
Extended.{ { 12232711 } Voice «which locks are held» }
```
````

The names Simple and Extended, and one `Asking` holding both, are this flow's proposal.
The living asked for two formats of one query.

### Generated by ethos-zero 16.0.0
```rust
pub struct Simple_Data { pub role: Role, pub question: Question }
pub struct Extended_Data { pub flow_id: FlowId, pub role: Role, pub question: Question }
pub enum Asking { Simple(Simple_Data), Extended(Extended_Data) }
pub enum Query { Ask(Asking) }
```

### Two containers
[drawing: everyday CLI call]

*Same data, two containers; both arrive as one query type.*

## 4. A new object is shown first as its ethos spec · vision

`Vision/ethos.md`, new section after "Self-description". Now: no such section.
The living: "the ethos and the example datom".

### Proposed
````markdown
## Shown first as ethos

Every machine-to-machine language made along the way is ethos.
Whenever a new object is presented, a kind, a message or a datom, its
ethos spec comes first, and an example datom follows, showing the
object in use: how it is used and the queries and responses it
produces. Ethos that is shown is always correct ethos; a block that
lacks its type is not ethos.
````

## 5. Titles and presentations are datom · vision

`Vision/datom.md`, new section after "The interface shape". Now: no such section.
The living: "the titles will be everywhere".

### Proposed
````markdown
## Titles and presentations

Every title is a datom: a variant naming what the thing is, carrying a
struct of its parts, `PsycheV2.{ Fable 2 }`. A presentation to the
living opens with one datom line naming it, `Presentation.{ «Datom» }`,
and wherever code logic is involved it shows ethos and datom: the
ethos spec of each type it introduces, an example datom in use, and
high-level code where the logic is the point.
````

## 6. An identifier is a value; its text is datom's · vision

`Vision/datom.md`, new section after "Datom beside protos and signal". Assumes Ruling 2 (a). Now: no such section.
The living: "The Nexus just thinks of it as a hash".

### Proposed
````markdown
## Identifiers and their text forms

An identifier is a value of its own type, and its text forms belong to
datom. The flow id is a hash, held as a number of its own type,
`FlowId.{ Integer }`. A Nexus stores, keys and compares the number and
never sees text. Its renderings, six hex characters today and three
words later, are reversible, and live only on the side that faces
text, with the datom kinds.
````

### Where each form lives
[drawing: CLI side: the renderings]

*The number crosses the wire; its text forms exist only where text is read and written.*

## 7. Flow's id becomes its own type · implementation

`/git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos`, line 116. Built on a yes to Ruling 2 (a).
The living: "The flow ID is not a string, it's a hash".

### Now
```
[ FlowId.String
```

### Proposed
```
[ FlowId.{ Integer }                  ; a flow's id: a hash, a number of its own type
```

### Generated by ethos-zero 16.0.0
```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct FlowId {
    pub integer: i64,
}
```

### From spec to text
[drawing: FlowId.{ Integer }]

*The datom form is generated; the hex and word renderings of proposal 6 are not, yet.*

They stay a hand-written impl in the CLI crate until the generator links a rendering to the datom form.

## 8. The datom skill says where datom is spoken and names the formats · implementation

`/git/github.com/LiGoldragon/Curriculum/skills/datom.md`, new section after "A datom needs a type" (line 104). Now: no such section.
The living: "when the tool actually uses Datom".

### Proposed
````markdown
## Where datom is spoken

Datom is spoken where text meets a typed program: a CLI's one inline
argument and its answer, a message between machines, a title. A Nexus
never handles datom; its CLI does. A tool that needs no datom gets
none. A Signal may offer two formats of one query, a simple one
without the flow id for common use and an extended one with it for
debugging and component-to-component work; both are variants of one
type.

```
; datom, each in a position expecting Asking
Simple.{ Voice «which locks are held» }
Extended.{ { 12232711 } Voice «which locks are held» }
```
````

## 9. The presentation line has a type · implementation

`/git/github.com/LiGoldragon/Curriculum/skills/main-flow.md`, line 39.
One clause is added; the rest of the line stays as it is.
The living: "the metadata is one datom line".

### Now
```
… its first line inside is one datom naming the book, `Presentation.{ «title» }`;
a quoted marker stays inline. …
```

### Proposed
```
… its first line inside is one datom naming the book, `Presentation.{ «title» }`,
in a position expecting `Block.[ Presentation.{ Title } ]` with `Title.String`;
a quoted marker stays inline. …
```

### The type
```
Library
[]                                     ; imports
[ Title.String                         ; types
  Block.[ Presentation.{ Title } ] ]   ; a block's metadata line
[]                                     ; kinds
[]                                     ; associations
```

### What datom-codec 0.32.2 does with it
[drawing: Presentation.{ «Datom» }]

*Quoted or bare, the line reads to the same value.*

## Rulings

### 1. Datom everywhere, or only where a program needs it
- (a) Datom everywhere: all the CLIs, the system prompt of every machine call. Said 2026-09-15 and 2026-09-19.
- (b) Datom only where the program needs it; none forced on a messenger. Said 2026-09-27 and 2026-09-28.

Proposals 1 and 8 assume (b).

### 2. The flow id's type
- (a) A hash, a number of its own type; text forms are serialization outside the Nexus. The living's words, 2026-10-03.
- (b) A string: `FlowId.String` in `Vision/ethos.md` (2026-09-09) and in signal-flow 10.0.0.

Proposals 6 and 7 assume (a).
<!-- to-the-living:end -->


## flows/bad807/books/3-nexus-v2.md

<!-- to-the-living:start -->
Presentation.{ «The Nexus» }

## Where it stands

Four nexuses run, each on an ordinary and a meta socket.

```
Orchestrate Nexus   0.37.0
Flow Nexus          0.23.0     flow-nexus on PATH resolves 0.12.2
Message Nexus       0.19.0     meta socket: message-owner.sock
Lojix Nexus         8.1.0
```

- ethos-zero 16.0.0 reads four roots: Library, Signal, Operation, Memory.
- Flow alone has a generated Operation root (`flow-nexus/ethos/operation.ethos`, 81 lines).
- Each Nexus writes its own `main`: Flow 111 lines, Orchestrate 39, Message 37, Lojix 21.
- The `nexus` library 0.5.0 has configuration, authority, situation and relocation types, no entry point; Orchestrate and Lojix use it, Flow and Message do not.
- Flow 0.24.0's store takes the signal straight in (`store.rs:673`, called from `lib.rs:122`).

`Vision/nexus.md` has no section on layers. `Vision/flowNexus.md` speaks of Flow alone.
Vision statements migrate into the psyche repository as Vision-type skills; each [vision] proposal names its `Vision/` file as its home today.

## The anatomy

[drawing: CLI]

Three parts, one path: signal → operation → memory → operation → signal.

## The anatomy in code

The whole Flow Nexus in the four roots, as proposed.

```
Library                                  ; what the three parts share
[]                                       ; imports: none
[ FlowId.Integer                         ; types
  Voice.{ Aspect Layer }                 ;   who a flow speaks for: an aspect at a layer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Event.[ Started Stopped ] ]
[]                                       ; kinds
[]                                       ; associations

Signal                                   ; what Flow says, on its ordinary socket
[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
[ Launch.{ Voice Brief.String }          ; queries
  Report.{ FlowId Event } ]
[ Launched.FlowId                        ; responses
  Refused.[ NoCapsule VoiceBusy.Voice ]
  Reported ]
[]                                       ; types

Operation                                ; what Flow does: one operation for every effect
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Start.{ Voice Capsule }                ; operations
  Record.{ FlowId Event } ]
[ Started.FlowId                         ; outcomes
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String Login.Vector<String> } ]   ; types

Memory                                   ; what Flow remembers
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Flow.{ FlowId Voice State.[ Running Ended ] Vector<Event> } ]   ; record types
```

Illustration only: not run through ethos-zero; FlowId 7 below and the brief are invented.

## One signal's path

```
Launch.{ { Psyche Primary } «Draft the Nexus book» }   ; 1 Query, typed at the CLI
Start.{ { Psyche Primary } { /home/li/primary [] } }   ; 2 Operation, from Signal's intend
Flow.{ 7 { Psyche Primary } Running [ Started ] }      ; 3 the Change handed to Memory
Succeeded                                              ; 4 Memory answers Operation
Started.7                                              ; 5 Outcome
Launched.7                                             ; 6 Response, back to the CLI
```

Shown as datom; inside the Nexus each is an rkyv value.

[drawing: socket]

One signal through the entry point: ten steps, none hand-written (calls solid, returns dashed).

## The layers

[drawing: Primary]

Four layers of authority, each holding voices (`Voice.{ Aspect Layer }`), beside the four running nexuses.

## Proposals

### 1. Three parts and one path — landed
Landed in `Vision/nexus.md` with example code.

### 2. The standard entry point — pointer
Now designed as actors in «The standard entry point: three actors, one path»; rule there.

### 3. [vision] `Vision/nexus.md`, "Library and daemon"

Now:
> Every component built from now on is a Nexus. The nexus repository is the library that defines the core of a Nexus component.

Proposed:
> The nexus repository is the core library of every Nexus. It defines the kinds of the three parts and the standard entry point, and it keeps the parts apart at compile time: only an operation's kind can touch a memory type, so no signal reaches memory except through an operation.

Grounded: "an architecture guard basically". Assumes Ruling 5(b).

### 4. [vision] `Vision/nexus.md`, "Signal only"

Now:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket. A Nexus thinks in typed values — enums, structs, scalars — and the string fields it still carries are records on the way to a fully typed form.

Proposed:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket. A Nexus never handles text: it decodes known types in their rkyv form, and every text form of a value, datom or an identifier's printed form, is made outside it, in a CLI or an interface.

Grounded: "so that it's not actually in the Nexus".

### 5. [vision] `Vision/nexus.md`, "Why everything is a Nexus"

Now:
> Everything built from now on is a Nexus, and what was built in another shape is rewritten as one. The consistency creates reliability, quality, and clarity.

Proposed:
> Every runtime component is a Nexus, and what runs in another shape is rewritten as one. A library stays a library: kinds, datom and other code compiled into a Nexus are not themselves Nexuses. The consistency creates reliability, quality, and clarity.

Grounded: "the runtime part of course". Assumes Ruling 4(a).

### 6. [vision] `Vision/nexus.md`, new "An operation may be a machine call"

Now: no such section.
Proposed:
> An operation may be performed by a machine call. The call is given the ethos spec of what it is to answer, a few datom examples and a prose explanation, and is then told it speaks that spec. It answers in datom of the spec's response types; an answer outside the spec is returned to it naming the part of the spec it broke.

Grounded: "now we switch to this spec".

### 7. [vision] `Vision/nexus.md`, new "Layers"

Now: no such section.
Proposed:
> Flows run in four layers of authority: Primary, Secondary, Tertiary, Quaternary. One Nexus holds each flow's layer and answers, for a calling process, which layer it belongs to. Spawning and messaging are controlled by the more highly permissioned nexuses.

Grounded: "controlled by more highly permissioned nexuses". Assumes Ruling 8(b); the holder is Ruling 10.

### 8. [implementation] `Curriculum/skills/vision-nexus.md`, line 6

On his yes to 1 to 3. Now:
> A Nexus is the long-running whole: its executable `<nexus>-nexus`, at least two sockets, one default CLI client per socket, and the signal contracts it is compiled with. It is a Nexus, never a daemon.
>
> Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers. A Nexus is a vertex in the graph of nexuses; an edge joins two vertices and carries one contract; every connected pair has an ordinary edge, only some a meta edge.

Proposed, after "what it remembers.":
> A signal reaches memory only through operation and returns through it. Every Nexus's `main` is the one line `nexus::main!(<Nexus>);`; the `nexus` library's entry point owns that path and its kinds keep the three parts apart.

Grounded: the three-part path.

### 9. [implementation] `nexus/ethos/nexus.ethos`, new

The core library's types and part kinds.

```
Library                                  ; the nexus core library: what every Nexus shares
[]                                       ; imports: none
[ Part.[ Signal Operation Memory ]       ; types: the three parts
  Step.[ Received Intended Changing      ;   the path, in order
         Remembered Performed Answered ]
  Changed.[ Succeeded Failed ]           ;   every memory change answers one of these
  Socket.[ Ordinary Meta ] ]             ;   the two sockets every Nexus opens
; kinds: one per part, only the entry point calls them; Query, Operation, Outcome and
; Response are each Nexus's own types, generated from its Signal and Operation roots
[ Signaling.[ intend.[ Operation ] answer.[ Response ] ]
  Operating.[ perform.[ Outcome ] ]
  Remembering.[ change.[ Changed ] ] ]
[]                                       ; associations
```

Unchecked by ethos-zero 16.0.0; the kind-capability syntax is the flow's guess. Grounded: "expose the types used in core of the program (in ethos)".

### 10. [implementation] `nexus/src/entry.rs`, new

Now: `nexus` 0.5.0 has `authority.rs`, `configuration.rs`, `lib.rs`, `relocation.rs`, `situation.rs`.

```rust
/// Signal: what the Nexus says. It is never handed memory.
pub trait Signaling {
    type Query; type Response; type Operation; type Outcome;
    fn intend(&self, query: Self::Query) -> Self::Operation;
    fn answer(&self, outcome: Self::Outcome) -> Self::Response;
}
/// Operation: what the Nexus does; the one part given memory.
pub trait Operating<M: Remembering> {
    type Operation; type Outcome;
    fn perform(&mut self, operation: Self::Operation, memory: &mut Remembrance<M>) -> Self::Outcome;
}
/// Memory: what the Nexus remembers. Opening needs an Admission.
pub trait Remembering: Sized {
    type Change;
    fn open(admission: Admission) -> Result<Self, Refusal>;
    fn change(&mut self, change: Self::Change) -> Changed;
}
/// Built only inside `enter`; private fields, so nothing else holds memory.
pub struct Admission { situation: Situation }
pub struct Remembrance<M: Remembering> { memory: M }
pub trait Changing<M: Remembering> { fn change(&mut self, change: M::Change) -> Changed; }
impl<M: Remembering> Changing<M> for Remembrance<M> {
    fn change(&mut self, change: M::Change) -> Changed { self.memory.change(change) }
}
/// A whole Nexus names its parts; their types are generated from its ethos.
pub trait Nexus {
    type Memory: Remembering;
    type Operation: Operating<Self::Memory>;
    type Signal: Signaling<Operation = <Self::Operation as Operating<Self::Memory>>::Operation,
                           Outcome = <Self::Operation as Operating<Self::Memory>>::Outcome>;
    fn parts(configuration: &Configuration) -> (Self::Signal, Self::Operation);
}
/// The one path, provided once; the blanket impl leaves no Nexus its own.
pub trait Entering: Nexus {
    fn enter() -> ExitCode {
        // defaults → open memory with the Admission → bind both sockets, then per frame:
        //   let operation = signal.intend(query);
        //   let outcome = operation_part.perform(operation, &mut remembrance);
        //   socket.send(signal.answer(outcome));
        Served::until_terminated()
    }
}
impl<N: Nexus> Entering for N {}
#[macro_export]
macro_rules! main {
    ($nexus:ty) => { fn main() -> std::process::ExitCode { <$nexus as $crate::Entering>::enter() } };
}
```

Illustration only; not compiled. Grounded: "make Nexus sort of the only main call".

### 11. [implementation] `flow/crates/flow-nexus/src/main.rs`, Flow first

Now: 111 hand-written lines (0.24.0) with `trait AnswersVersion` and the startup sequence, and in `store.rs:673`:

```rust
fn apply(&self, query: Query) -> Result<Response, StoreError>;
```

Proposed: `main.rs` becomes one line, and the store takes no `Query`.

```rust
nexus::main!(flow_nexus::FlowNexus);
// store.rs implements Remembering:
fn change(&mut self, change: memory::Flow) -> Changed;
```

Grounded: "the main function is standard".

### 12. [implementation] `Curriculum/skills/knowledge-nexus.md`, line 8

Now:
> Field's retained Home 83 result reports the running server engines as Orchestrate Nexus 0.37, Flow Nexus 0.23, Message Nexus 0.19, and Lojix Nexus 8.1. It reports these stable socket pairs:

Proposed:
> On 2026-10-04 the process list shows Orchestrate Nexus 0.37.0, Flow Nexus 0.23.0, Message Nexus 0.19.0 and Lojix Nexus 8.1.0 running; `flow-nexus` on `PATH` resolves 0.12.2, not the running 0.23.0.
>
> None enters through the standard entry point; Flow alone writes one of the three parts in ethos (its Operation root), Lojix and Orchestrate hold Library roots only, Message none. Their socket pairs:

Grounded: measured by this flow (process list, `readlink` of each binary on `PATH`, `/run` socket listing).

## Rulings
1. What Nexus names, and the middle part's name.
   - (a) Nexus is the whole; the middle part is Operation. 2026-08-19 to 2026-10-04; `Vision/nexus.md` approved 2026-09-11.
   - (b) Nexus is the core inside, the whole a metaNexus; the middle part is Process. 2026-09-13 to 2026-10-02.
2. The keeping part's name.
   - (a) Memory, Sema freed for the meaning language. 2026-09-26 to 2026-10-02.
   - (b) Sema, the database engine of a Nexus. 2026-09-10 (`Vision/sema.md` undated).
3. The nexus core language.
   - (a) Set aside, signal and memory types being enough. 2026-09-10 (one record).
   - (b) The core described in ethos. 2026-09-13, 2026-09-14.
4. Everything a Nexus, and its limits.
   - (a) Every runtime component, libraries excepted. 2026-08-19 to 2026-08-26.
   - (b) Some tools start as a plain server or a Clojure tool. 2026-08-28; 2026-09-29 (notion).
5. An architecture guard.
   - (a) A guard written for one repository is foolish. 2026-08-18 (one record).
   - (b) The kinds and the entry point are the guard. 2026-09-14, 2026-10-04.
6. What the entry macro converts.
   - (a) It takes a datom-derived type and writes the input conversion. 2026-08-22 (one record).
   - (b) No datom in a Nexus; conversion lives in the CLI. 2026-10-03 (one record).
7. The messaging Nexus's name.
   - (a) Message. 2026-09-17 (one record).
   - (b) Messenger. 2026-09-25 (one record).
8. Layers of authority: three or four. Settled at four, by the tertiary/quaternary ruling.
   - (a) Three: Primary, Secondary, Tertiary. 2026-09-14 (one record).
   - (b) Four, with Quaternary. 2026-09-26, 2026-09-27.
9. Layers of ethos: three or four.
   - (a) Three specifications, one per part. 2026-10-02 (one record).
   - (b) Four roots, Library beside the three parts. 2026-09-09; ethos-zero 16.0.0 as deployed.
10. Which Nexus holds a flow's layer.
   - (a) Persona. 2026-09-14, 2026-09-16.
   - (b) Flow. 2026-09-16 (one record).
<!-- to-the-living:end -->


## flows/bad807/books/8-datom-file-v2.md

<!-- to-the-living:start -->
Presentation.{ «A Nexus reads a value from a datom file» }

## His words
> "let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this … a variant `me` [sic] that would tell it what type of CLI you would have to use … There's a string involved no matter what unless all of that is, again, put into an external tool."

His book comment on «The Nexus».

## Today
A datom value reaches a Nexus only as an argument string.
```
orchestrate "<one inline datom>"                        # env::args(), no flags
  → Potential::<Query>::from(source).actualize(&mut budget)   # datom-codec 0.31.0
  → Dispatch::Open(Query) → one frame of signal → orchestrate-nexus
```
Orchestrate 0.36.1 refuses anything else: "accepts exactly one inline Datom query and no flags".
`orchestrate-nexus/Cargo.toml`: "No `datom-codec` and no `protos`".

[drawing: Today: three present paths for a datom value]Today a datom reaches a Nexus as one argument; only the aggregator daemon parses a file itself.
### The two settings files outside that path
```rust
// aggregator 0.7.0, src/daemon.rs lines 35 to 38 (datom-codec 0.27.0)
std::fs::read_to_string(configuration_path)  →  DatomText::read
// its CLI reads the same file for the socket paths (src/client.rs line 37)
```
Lojix 6.0.0: `lojix-write-configuration` turns one inline datom into an rkyv archive.
The Nexus loads it from the path in `LOJIX_CONFIGURATION`.

### What the rule says now
```text
skills/datom.md line 95: "datom passes inline at a CLI boundary, never as a datom file"
```
The corpus names this the tension "Settings file" (`ethos-nexus-corpus.md` line 9150).
The ethos below is checked and generated with ethos-zero 16.0.0; nothing ran against a live socket.

## Three ways from the file to the Nexus

[drawing: Three ways the value travels from the file to the Nexus]Right column: the string each way leaves inside the Nexus.
## a) The Nexus runs a reader as a subprocess
No ethos added to the Signal. The reader is a Memory value; his variant names the CLI.
```
Reader.[ Orchestrate Lojix ]               ; which reader program the Nexus spawns
```
Rust, Nexus side, compiled in the scratch crate without the `datom` feature:
```rust
impl Invoking for Reader {
    fn program(&self) -> &'static str {
        match self { Self::Orchestrate => "orchestrate-read", Self::Lojix => "lojix-read" }
    }
    fn read_roster(&self, path: &FilePath) -> Result<Roster, ReadFailure> {
        let output = std::process::Command::new(self.program()).arg(path).output().map_err(|_| ReadFailure::Spawn)?;
        if !output.status.success() { return Err(ReadFailure::Exit) }
        rkyv::from_bytes::<Roster, rkyv::rancor::Error>(&output.stdout).map_err(|_| ReadFailure::Archive)
    }
}
```

[drawing: Way a: the Nexus spawns a reader and decodes its stdout]Way a: the Nexus starts a program by name and trusts its stdout.
The names `Orchestrate`, `Lojix`, `orchestrate-read` and `lojix-read` are the flow's illustration.
No such reader binary exists; no CLI of ours prints rkyv today.

The no-text rule keeps its letter: the Nexus parses no datom.
It loses its spirit: the Nexus starts processes by name and trusts their stdout.

- For: the Nexus pulls on its own, at any time, with no caller connected.
- Against: a command string and a process boundary inside the Nexus; a reader binary per contract.
- Against: `PATH` on the host decides what runs, not the contracts the Nexus is compiled with.

## b) The Nexus asks; the CLI reads, decodes and sends the typed value
Ethos added to the Signal. `Check` with ethos-zero 16.0.0 answers `Checked`.
```
Signal
[]                                                ; imports
[ Configure.Configuration                         ; queries
  Supply.Supplied ]                               ;   the CLI hands in what was asked for
[ Configured                                      ; responses
  ReadFile.Wanted                                 ;   the Nexus asks the caller for a file
  Refused.[ NotWanted.FilePath ] ]                ;   a supply nobody asked for
[ FilePath.String                                 ; types
  Wanted.[ Configuration.FilePath                 ;   the variant names the type, and so the CLI
           Roster.FilePath ]
  Supplied.{ FilePath Reading.[ Configuration.Configuration
                                Roster.Roster
                                Missing
                                Unreadable ] }
  Configuration.{ SocketPath.FilePath Roster }
  Roster.Vector<Member>
  Member.String ]
```
`Roll`, `roll-meta`, `Roster` and `Member` are the flow's invented example names.

### Two exchanges on one connection

[drawing: ReadFile and Supply over two exchanges]The CLI answers ReadFile by opening exchange 2 with Supply; the Nexus never touches the file.
On `signal` 8.0.0 the querying side only opens exchanges:
```
Dispatch::{ Greet Open Abandon }
```
So `Supply` rides a second exchange on the same connection; the frame and the greeting stay as they are.

### The Nexus's answer
Compiled in the scratch crate without the `datom` feature:
```rust
impl Answering for Roll {
    fn answer(&mut self, query: Query) -> Response {
        match query {
            Query::Configure(Configuration { roster, .. }) if roster.is_empty() =>
                Response::ReadFile(Wanted::Roster(self.roster_path.clone())),
            Query::Configure(Configuration { roster, .. }) => { self.roster = Some(roster); Response::Configured }
            Query::Supply(Supplied { file_path, reading: Reading::Roster(roster) }) if file_path == self.roster_path =>
                { self.roster = Some(roster); Response::Configured }
            Query::Supply(Supplied { file_path, .. }) => Response::Refused(Refused_Data::NotWanted(file_path)),
        }
    }
}
```

[drawing: The Nexus's answer: four outcomes]The Nexus decides which file and which type; it only holds the path.
### The CLI's supply
Compiled in the scratch crate with datom-codec 0.32.2:
```rust
impl RosterFile<'_> {
    fn read(&self) -> Reading {
        let Ok(text) = std::fs::read_to_string(self.0) else { return Reading::Missing };
        let mut budget = Budget { remaining: 10_000, reader: ReaderBudget { remaining: 10_000 }, depth: 0, maximum_depth: 256 };
        Potential::<Roster>::from(text).actualize(&mut budget).map(Reading::Roster).unwrap_or(Reading::Unreadable)
    }
}
```

[drawing: The CLI's read: three outcomes]Run in the scratch crate on a good, a malformed and a missing file.
The good file answers:
```text
Supply(Supplied { file_path: "…/roster.datom", reading: Roster(["Ada", "Grace", "Barbara Liskov"]) })
```
### What b costs and gives
His variant naming the CLI becomes the `Wanted` variant naming the type.
The CLI built with that contract is the one already connected, so no program name is stored.

- For: no datom, no file access and no command string in the Nexus; the Nexus still decides which file and which type.
- For: works on `signal` 8.0.0 unchanged; the CLI side is about 20 lines per contract, generated from the `Wanted` variants.
- Against: the Nexus can ask only while a CLI is connected; a pull with no caller present needs a.

## c) The caller reads the file; the Nexus is unchanged
No ethos added. The shell composes the one inline datom; the CLI stays unchanged too.
```sh
roll-meta "Configure.{ /run/roll/roll.sock $(cat roster.datom) }"
# actualized in the scratch crate as
# Configure(Configuration { socket_path: "/run/roll/roll.sock", roster: ["Ada", "Grace", "Barbara Liskov"] })
```
No string in the Nexus; the cost to the no-text rule is nil.

His earlier words (a notion) are this way with the reader writing an archive:

> "next to it would be the compiled signal file so that then the Nexus could load it because it's already signal"

That is what `lojix-write-configuration` does today; the Nexus then holds the archive's path.

- For: free today, for every Nexus; nothing to design or build.
- Against: the Nexus cannot pull; the caller must know which file holds which position.
- Against: the file must hold exactly one position's value; it cannot be spliced in deeper than the shell can quote.

## Where the string lives

[drawing: Where the string lives in each way]Only a holds a program name; b holds one typed path; c holds nothing.
## What the flow proposes
Way b, for the Nexuses that declare it; c stays as what every Nexus already has.
It is the one way the Nexus pulls, as he asks, and still sees only signal.

The variant he wanted names a type, never a program; the one string is a path, held and passed, never read.
Way a puts a command string and a process boundary into the Nexus: the string he wanted out "unless … put into an external tool".

This recommendation is the flow's proposal, not his.

## The datom file form
One real settings file, `/git/github.com/LiGoldragon/aggregator/examples/configuration.datom`, one line, verbatim:
```text
{ /run/aggregator/aggregator.sock 432 /run/aggregator/aggregator-meta.sock 384 /var/lib/aggregator/aggregator.sema [ { example-repository /srv/aggregator/repositories/example } ] [ Claude.{ /srv/aggregator/transcripts/claude } Codex.{ /srv/aggregator/transcripts/codex } ] MetadataOnly { 32 4096 } { { DaemonLocalStorePath OpaqueStaleCapable FragileReferenceAscending } { 64 4096 65536 1024 131072 32768 8388608 262144 1024 } [] } }
```
It is read against this type, `meta-signal-aggregator` 0.7.0, `ethos/signal.ethos` lines 66 to 68:
```
AggregatorConfiguration.{ OrdinarySocketPath OrdinarySocketMode MetaSocketPath MetaSocketMode
                          StorePath ActiveRepositories TranscriptSources DefaultProjection
                          DefaultLimitPolicy OutputInterfaceConfiguration }
```

[drawing: Each position of the file fills one field, in order]A datom file is one datom, no root, against one type: positions follow its fields in order.
The test `example_configuration_carries_the_written_sockets_and_sources` actualizes it and passes.
Under b the file holds the value of one `Wanted` variant; under c, the value of one position in the inline datom.

## Proposals
### 1. [vision] `/home/li/primary/Vision/nexus.md`
New section "A value from a file", after "Signal only". Assumes Ruling 1 (b).
Grounded: his book comment, "ostensibly the CLI that it's meant to work with".
The `ReadFile` and `Supply` names are the flow's proposal, not his.

Now: no such section. Proposed:
```text
## A value from a file

A Nexus that needs a value kept in a datom file asks its caller for it. It answers with `ReadFile`, whose variant names the type it wants and carries the file's path; the CLI, built with the same contract, reads the file, actualizes the value and sends it back as `Supply`. The Nexus holds the path and never opens the file. A Nexus declares this only when it needs it. A caller may always read a file itself and send its value inline.
```
### 2. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/datom.md`
Line 95, its last clause. Built on a yes to proposal 1.
Grounded: his book comment, "pull in a value from a file".

Now:
```text
A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, never as a datom file.
```
Proposed:
```text
A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, and a CLI reads a datom file only when its Nexus answers with `ReadFile`, sending the value back as signal.
```
### 3. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`
Line 14, a sentence after "never by a claim." Built on a yes to proposal 1.
Grounded: his book comment, "pull in a value from a file".

Now: no such sentence. Proposed:
```text
A Nexus that wants a value from a datom file answers `ReadFile` with the wanted type's variant and the path; the CLI reads and actualizes the file and opens a second exchange with `Supply`; the Nexus holds the path and never the text.
```
### 4. [implementation] `/git/github.com/LiGoldragon/aggregator/src/daemon.rs`
Lines 35 to 38. Independent of proposals 1 to 3.
Follows "A Nexus starts with no arguments" (`Vision/nexus.md`, "Configuration").
Grounded: "the Nexus only gets signal".

Now:
```rust
    pub fn run(&self) -> Result<()> {
        let configuration_path = self.arguments.configuration_path()?;
        let configuration_store = ConfigurationStore::at_path(configuration_path);
        let configuration = configuration_store.read_configuration()?;
```
Proposed: the daemon starts from its built-in defaults with no `--configuration`.
`meta-aggregator` sends the file's value as `Configure.{ … }` (way c), so the daemon is built without datom-codec.

## Rulings
### 1. Which way a Nexus gets a value from a datom file
- (a) It runs a reader subprocess named by a variant. His book comment: "a variant … that would tell it what type of CLI you would have to use".
- (b) It asks with `ReadFile`, the connected CLI supplies. His book comment: "ostensibly the CLI that it's meant to work with"; the flow's proposal.
- (c) The caller reads and sends it, the Nexus unchanged. His book comment: "unless all of that is, again, put into an external tool"; a notion: "next to it would be the compiled signal file".

### 2. Whether the no-text rule admits a path string in a Nexus
- (a) Yes, a path held and passed but never parsed. `Vision/nexus.md` "Signal only": "the string fields it still carries are records on the way to a fully typed form".
- (b) No, a path is first given a type of its own. A record: "in a way, it's a string when you print it, but it's not a string per se".

### 3. Whether every Nexus can ask for a file
- (a) Only those that declare it in their Signal. His book comment: "Maybe not all the Nexuses need this".
- (b) Every Nexus, through the shared nexus library. `Vision/nexus.md` "First configuration": "whatever else comes up as standard nexus configuration data".
<!-- to-the-living:end -->



## /home/li/primary/flows/aa887c/books/context-modules-v3.md

<!-- to-the-living:start -->
Presentation.{ «Context modules» }

What a flow starts its thinking with: the standard, the files it touches, and the code of each change.
Marks: **vision** is what is wanted; it enters on your word. **today** is explanation, witnessed in the cited file. **implementation** is built on your yes. Code marked **proposed** exists in no file yet.

## Your comments on the last edition
1. "We shouldn't say that." It answered two lines of Proposal 1, not the whole block: the heading "A context module is one file of what a flow starts its thinking with" and the sentence under it, "A context module is one file of prompt text with a type, a name and a description." Both are gone.
2. "universal statements that aren't true for all harnesses" and "it feels a bit strong and unnecessary": the placements are now stated as what is wanted. Which harness does what today is a separate table (Figure 1) with its sources. The claims about forks and subagents are cut.
3. "redo this with example code": every proposal now shows the code that is there now and the code that replaces it, each with its source path.

## Where things are now
```
Skill sources      /git/github.com/LiGoldragon/Curriculum/skills/<name>.md        71 flat files
Role data          /git/github.com/LiGoldragon/Curriculum/roles.datom             one Roles record
Generator          /git/github.com/LiGoldragon/curriculum-deploy                  types in curriculum-deploy.ethos
Main-flow prompt   /home/li/primary/tools/main-flow-mode/system-prompt.md         15 lines, outside Curriculum
Launchers          /home/li/primary/tools/{claude,codex,opencode}-main-flow-launch.mjs
Migration          /home/li/primary/flows/aa887c/scripts/migrate-skills.sh        to psyche-, mind-, field-skills; not run
```

### today: how the skill trees are made
[drawing: Curriculum skills and roles.datom go through curriculum-deploy into the generated skill trees and agent definitions]

Figure 1. *Today: Curriculum's skill files become the skill trees; roles.datom becomes the subagent definitions.*

### today: where a module reaches each harness
[drawing: Table of the three placements against Claude, Codex and OpenCode main flows and subagents, as the launchers do it today]

Figure 2. *Today, per harness. Sources: the launchers below, and the claude-harness and codex-harness skills.*

The launcher code behind Figure 2:

`tools/claude-main-flow-launch.mjs`, lines 34, 100, 110, 198 (excerpt)
```js
export const BIRTH_SKILLS = ['main-flow', 'spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'];
  const prompt = `${BIRTH_SKILLS.map(n => `/${n}`).join(' ')} # Launch brief\n\n${brief.trim()}\n`;
  const promptFile = systemPromptFile ?? path.join(modeDir, 'system-prompt.md');
  … claude … --system-prompt-file ${sh(mode.promptFile)} … "$(cat ${sh(promptFile)})"
```

`tools/codex-main-flow-launch.mjs`, lines 61, 64, 67 and 82 (excerpt): the skill text goes into the first prompt; no `model_instructions_file` is passed, so Codex keeps its stock base instructions.
```js
  const blocks = ['main-flow', ...ASPECT_SKILLS[aspect]].map(name => { … return skillBlock(workspace, name, text); });
  const prompt = `${blocks.join('\n')}\n# Launch brief\n\n${brief.trim()}\n`;
  return `exec env … ${sh(client.expectedPath)} -m ${sh(o.model)} -c 'model_reasoning_effort="medium"' --dangerously-bypass-approvals-and-sandbox -C ${sh(o.workspace)} "$(cat ${sh(promptFile)})"`;
```

`tools/opencode-main-flow-launch.mjs`, lines 74 to 78
```js
// The main-flow mode: the agent whose prompt replaces OpenCode's own.
export function seatConfig(systemPrompt, model) {
  if (!systemPrompt.trim()) throw new Error('main-flow system prompt is empty');
  return {agent: {[AGENT]: {description: 'A main flow seat.', mode: 'primary', model, prompt: systemPrompt}}};
}
```

`curriculum-deploy/src/roles.rs`, `packet` (excerpt): a subagent's definition body is the role modules joined; on Codex it is written as `developer_instructions`, not as base instructions.
```rust
        for module_id in &self.string_vector {
            modules.push(self.module(module_id)?);
        }
        let body = modules.join("\n\n");
        // ClaudeAgent → .claude/agents/{identifier}.md, body after the frontmatter
        // CodexAgent  → .codex/agents/{identifier}.toml, developer_instructions = body
```

## Proposal 1: the standard
**vision** · create `/home/li/primary/Vision/contextModules.md`

Now: no such file. Proposed, whole:
> **Context modules**
>
> **Types**
> A module's type says who stands behind it and where it may go; a name is unique within its type.
> The types are declared once, in the generator's ethos; no other text lists them.
>
> **Three placements**
> We want a module to reach a flow in one of three places.
> The system prompt replaces the harness's own prompt.
> The first prompt is the launch turn: what this flow does now.
> Loadable modules are loaded by name when a situation calls.
>
> **A role**
> A role is one record naming, for each placement, its modules by type, and its model. Flow composes the launch from that record with no model in the loop.
>
> **What qualifies for the system prompt**
> A module goes in the system prompt when it is steady, changing only on the living's word; when it addresses the role's whole run, never a task; and when it must be present before the first tool call or must hold against the harness's own guidance.
> Distilled spirit, intent and vision qualify; raw records never do. A seat's identity module qualifies.
> Knowledge is loadable, because it changes with the system. Any other Operation module goes in the first prompt or stays loadable.
>
> **What makes a module high quality**
> Every line is a definition or a rule in the present tense, leading with what is wanted. Each line traces to a record of the living or to a witness.
> One fact lives in one module. A module carries no history, no objection, and no unknown where a measurement is possible.
> It uses our terms, not a vendor's, except where a harness is named. It fits its placement's budget, and the budget is measured.

Removed from the last edition: the heading and sentence of your comment 1; "it reaches the main flow and its forks, never its subagents"; "they are the only placement a subagent reaches"; "the skill tree".

## Proposal 2: Queued, a fourth placement
**vision** · **proposed, unruled** · Proposal 1, after Loadable; and the `Placement` line of Proposal 4

Today: the Claude launcher's `UserPromptSubmit` hook re-injects the first five paragraphs of the system prompt every 20th prompt (`tools/claude-main-flow-launch.mjs`, lines 112 and 113; `tools/main-flow-mode/reminder-hook.py`).
```js
  const hook = ['python3', sh(path.join(modeDir, 'reminder-hook.py')), '--prompt-file', sh(promptFile),
    '--state-dir', sh(path.join(jobDir, 'main-flow-reminder')), '--every', '20'].join(' ');
```
Proposed:
> Queued context enters a running flow between its turns: what Flow has queued for that flow, carried into its next incoming message.
```
Placement.[ SystemPrompt FirstPrompt Loadable Queued ]
```

## Proposal 3: the types, declared once
**implementation** · `/git/github.com/LiGoldragon/curriculum-deploy/curriculum-deploy.ethos`, lines 25 and 32

Now:
```
  RoleModule.{ String String }
  Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> }
```
**proposed**, replacing those two lines:
```
  ModuleType.[ Spirit Intent Vision Notion Knowledge Operation ]
  Location.[ Path.String ]
  Module.{ ModuleType Name.String Location }
  Manifest.Vector<Module>
  Placement.[ SystemPrompt FirstPrompt Loadable ]
  Selection.{ ModuleType Vector<Name> }
  Placed.{ Placement Vector<Selection> }
  RoleConfiguration.{ Role Vector<Placed> ModelChoice }
  Roles.{ Vector<RoleConfiguration> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> }
```
- `ModuleType` is the one place the types are listed.
- `RoleModule` goes: a role's text is a module file.
- `Vector<String>` and `TargetInsertion` go: a subagent's definition body is its own SystemPrompt selections.

## Proposal 4: the module file
**implementation** · each skill file moves to `<repository>/<type>/<name>.md`; the frontmatter is unchanged

The type is the directory; no `type:` line (ruling 1 of the migration, `flows/aa887c/scripts/migrate-skills.sh`).

Now, `Curriculum/skills/spirit.md`, lines 1 to 4:
```
---
description: Every agent task.
dependencies: [behavior, correction, vocabulary]
---
```
Now, `curriculum-deploy/src/catalog.rs`, `DeclaredSource::skills` (excerpt): the name is the file stem.
```rust
                let name = path
                    .file_stem()
                    .expect("markdown stem")
                    .to_string_lossy()
                    .into_owned();
```
Proposed placement, `flows/aa887c/scripts/migrate-skills.sh`, manifest rows (excerpt; `repository|type|name|…`):
```
psyche|spirit|spirit|1|whole:$CUR/spirit.md
psyche|vision|contextModules|105|whole:$SPL/books/psyche-vision-contextModules.md
mind|operation|main-flow|11|…
mind|operation|psyche-primary|101|whole:$SPL/books/mind-operation-psyche-primary.md
field|knowledge|flow|45,11|whole:$CUR/knowledge-flow.md …
```
**proposed**: the generator reads the three repositories into one `Manifest`, one record per file:
```
[ { Spirit spirit Path.«/git/github.com/LiGoldragon/psyche-skills/spirit/spirit.md» }
  { Vision contextModules Path.«/git/github.com/LiGoldragon/psyche-skills/vision/contextModules.md» }
  { Operation main-flow Path.«/git/github.com/LiGoldragon/mind-skills/operation/main-flow.md» }
  { Knowledge flow Path.«/git/github.com/LiGoldragon/field-skills/knowledge/flow.md» } ]
```

## Proposal 5: the standard as a loadable module
**implementation** · create `psyche-skills/vision/contextModules.md` (manifest row 105)

**proposed**:
```
---
description: A context module, its type or its placement is being designed, edited or judged.
---
<the body of Proposal 1, without its title>
```
The cut text it copies, `flows/aa887c/scripts/splits/books/psyche-vision-contextModules.md`, still holds the last edition's lines and is re-cut from this one.

## Proposal 6: one main-flow module
**implementation** · `mind-skills/operation/main-flow.md` takes the fifteen lines of `tools/main-flow-mode/system-prompt.md`; that file is removed

Now, `Curriculum/skills/main-flow.md`, lines 1 to 8 (excerpt):
```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, …
Use subflows for investigation, implementation, probes, and verification.
```
Now, `tools/main-flow-mode/system-prompt.md`, line 1 of 15:
```
You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
```
**proposed**, `mind-skills/operation/main-flow.md`:
```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
<the other fourteen lines of tools/main-flow-mode/system-prompt.md, unchanged>

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, …
```
- Removed from main-flow.md: lines 8, 10, 11, 17, 18 and 51, which the system prompt repeats.

## Proposal 7: the psyche-primary module
**implementation** · create `mind-skills/operation/psyche-primary.md` (manifest row 101)

Now: the seat's identity is in the launch brief only. **proposed**, whole, from `flows/aa887c/scripts/splits/books/mind-operation-psyche-primary.md`:
```
---
description: The seat is the Psyche voice at the Primary layer.
user-only: true
---
You are the Psyche voice at the Primary layer: the seat that hears the living and designs what the machines start their thinking with.

What the living must read, rule on or approve goes whole into the living messenger as a presentation; he answers by number. Chat is unread.

You design, rule and judge. The Secondary builds and tests what you hand down.
```

## Proposal 8: the role record
**implementation** · `Curriculum/roles.datom`

Now, `Curriculum/roles.datom` (excerpt): the role texts are inline strings; no main-flow role.
```
Roles.{ [ { general-instructions «The brief is your authority. Decide what it settles; return what it does not.» }
          { codex-skill-loading «Do not reload a complete pasted skill unless freshness or source verification is required.» }
          { spirit-role «The purpose of AI is to extend a psyche. …» }
          { intent-role «Every layer carries its own context. …» }
          { subflow-role «Your flow is `FLOW_ID` and `FLOW_DIRECTORY` in your environment. …» } ]
        …
        [ general-instructions spirit-role intent-role subflow-role ]
        [ { general-instructions CodexAgent [ codex-skill-loading ] } ] }
```
**proposed**, the Psyche Primary role, whole, from `flows/aa887c/scripts/roles/psyche-primary.datom`:
```
{ Voice.{ Psyche Primary }
  [ { SystemPrompt [ { Spirit [ spirit ] }
                     { Operation [ main-flow psyche-primary ] }
                     { Vision [ vocabulary psyche ] } ] }
    { FirstPrompt [ { Operation [ psyche-logging edit-coordination ] } ] }
    { Loadable [ { Vision [ context-modules flow ethos nexus psyche-interraction ] }
                 { Knowledge [ nexus flow ethos ] } ] } ]
  { claude-fable-5-1 None } }
```
- `spirit-role` and `intent-role` repeat existing text: subagents select `{ Spirit [ spirit ] }` and `{ Intent [ context ] }`.
- `general-instructions`, `codex-skill-loading` and `subflow-role` become `mind-skills/operation/` files, bodies unchanged (manifest rows 102 to 104).
- The record names `context-modules`; the manifest names `contextModules`. One spelling follows the stem-case ruling (open item 6 of the migration).

## Proposal 9: Flow composes the launch from the role
**implementation** · replaces `BIRTH_SKILLS`, `ASPECT_SKILLS` and the fixed system-prompt path in the three launchers; Flow takes this step when Flow launches

[drawing: Proposed: the role record and the manifest go into composeLaunch, which yields a system prompt, a first prompt and a loadable tree for the harness]

Figure 3. *Proposed: dashed boxes do not exist yet.*

Now: the composition is hard-coded per launcher (the excerpts under Figure 2).

**proposed**, one function the launchers share (no such file today):
```js
// Proposed. role: the parsed role record; manifest: Map of `${type} ${name}` → path.
const body = text => text.replace(/^---\n[\s\S]*?\n---\n/, '').trim();
export function composeLaunch(role, manifest, brief, read) {
  const paths = placement => (role.placed.find(p => p.placement === placement)?.selections ?? [])
    .flatMap(({type, names}) => names.map(name => {
      const found = manifest.get(`${type} ${name}`);
      if (!found) throw new Error(`no module ${type} ${name}`);
      return found;
    }));
  return {
    systemPrompt: paths('SystemPrompt').map(p => body(read(p))).join('\n\n'),
    firstPrompt: `${paths('FirstPrompt').map(p => body(read(p))).join('\n\n')}\n# Launch brief\n\n${brief.trim()}\n`,
    model: role.model,
  };
}
```

## Proposal 10: skill-designing's types
**vision** · `Curriculum/skills/skill-designing.md`, lines 55 to 59 and 66 to 67

Now:
```
A skill's kind says who stands behind it.
A gold skill carries no prefix. It is the living's vision of the desired result, approved by the living, and changes only on the living's word.
An `operation-` skill is deployed when the living describes what he wants a skill to do or to change; the primary Mind seat reviews and interprets it, and no glance from the living is needed.
A `compensation-` skill is written by flows; it compensates for what the system does not yet do, so that the system runs.
A `trial-` skill is written by flows: it is being tried for how useful it can become as a compensation skill.
…
A role skill carries an aspect's identity and names its
dependencies. Mark role skills user-only.
```
Proposed, replacing those lines:
> A skill is a context module; its type, declared in the generator's ethos, says who stands behind it and where it may go.
> Spirit, Intent, Vision and Notion are the living's: distilled on his word, changed on his word.
> Knowledge is what a flow found out about the system as it is; any flow may load it. Operation is how a thing is done; the primary Mind seat reviews it.
> A compensation is an Operation module whose name begins `compensation-`, welded in by a flow so the system runs; a trial is an Operation module whose name begins `trial-`, being tried.
> A seat's identity is an Operation module, marked user-only.

## Proposal 11: the distillation line
**vision** · `Curriculum/skills/psyche-distillation.md`, after line 25

Now, line 25:
```
A distilled statement carries what the psyche said and nothing beyond it; a small ruling makes a small statement, never a theory grown around the words.
```
Proposed, added after it:
> A proposal is small, conservative and general, and infers nothing; it is accepted whole or not at all.
> An order, an instruction for a situation, or an intervention is not distilled into a rule; it stays in the log.

## Rulings
1. **The set of types** (Proposals 3 and 10). (a) Six: compensation and trial are Operation modules by name prefix. (b) Eight: Compensation and Trial are types of their own.
2. **The standard** (Proposal 1): yes, or amend by line.
3. **The main-flow and psyche-primary modules** (Proposals 6 and 7): yes, or amend.
4. **Codex.** Today the Codex launcher keeps the stock base instructions and puts the skill text in the first prompt (Figure 2). (a) The system prompt replaces the base instructions through `model_instructions_file`. (b) Keep stock on Codex for now.
5. **The implementation** (Proposals 3 to 9): (a) one yes, built in that order. (b) comment what changes.
6. **Queued** (Proposal 2): (a) a fourth placement. (b) three placements; the hook stays Flow's affair.
7. **The distillation line** (Proposal 11): yes, or amend.
<!-- to-the-living:end -->


## flows/bad807/books/16-metaflows.md

<!-- to-the-living:start -->
Presentation.{ «Metaflows» }

The standing edition: what stands now, and what is still yours to rule.

How to read the marks.
**His**: your words state it. *Reading*: the flow's reading, past your words. **The flow's proposal**: designed here, every name, number, rule and type.
**S**: the tradition itself states it. **Contested**: the sources disagree. **Unruled**: left open until you rule.

## 1. The definitions

### Metaflow
**His**:
```
Metaflow    "something that sort of continues through several flows, one after another"
Voice       "a Metaflow with no known ending. This ending could itself become a judgment call."
```

### The Sun, Sūrya
**His**:
```
Woken       "it's not always on. The other three are always already awake."
Primary     "the sun (meaning the primary layer) can unwind"
Unwinds     "If nothing is cooking then when things calm down"
Hands on    only what is "still in debate, fuzzy, or haven't been ruled into the context modules"
The decided goes into "the context modules, which are where the behavior gets changed for the future"
```
Judgment as the Sun's charge is the flow's word; you answered "Yeah no, that's good." Ruling 2.

## 2. The three always awake, and the Sun's cycle

### His notion
**His**, thinking aloud, marked "I don't know":
```
Śani · Saturn       "imposes limits so in a sense he has to stay up"
Budha · Mercury     "what would wake up when the psyche speaks"
Candra · Moon       "then the moon would interpret it"
```
Then: "The other three are always already awake." Mercury "wakes" in the first; is awake in the second. *Reading*: Mercury is awake and stirs when you speak.

### The flow's reading of them
*Reading*: the charges and the seats are the flow's.
```
Line              Charge                               The seat or program that is it now
Budha · Mercury   hears first, routes                  the quaternary, the secretary, messenger-clj
Candra · Moon     keeps and interprets the record      psyche logging, distillation, the raw records by flow
Śani · Saturn     limits and measures                  quota, context occupancy, reaping on Replace, the Field publisher
```
Ruling 3.

### The Sun's cycle
```
State       What happens
asleep      nothing is cooking; no seat runs
woken       the secretary brings a question that needs judgment
judging     it rules; each ruling becomes a context module
unwinding   things calm down; the decided is already in modules
handover    its successor receives only the undecided
```

[drawing: The Sun's cycle: asleep, woken, judging, unwinding, with the decided going to context modules and the undecided to the successor]

Figure 1. The Sun's cycle, from «The geography of the Metaflows». **His**: the decided goes into context modules; only the undecided passes on.

## 3. The triad: open

**Unruled.** Three readings of the base. Each with its research in two lines and its marks.

### (a) Moon, Mercury, Saturn awake; the Sun woken
His notion tonight. The graha of the old floor, with the charges of section 2.
```
Research   Candra mind, Budha "the clever giver of language", Śani limit and time (BPHS 3.12–13, S)
           strands per graha: Candra sattva, Budha rajas, Śani tamas (BPHS 3.22, S): one of each
```
**Contested.** Your "There's nothing without the sun" stands against a base without it; here the Sun is in the system as the primary layer, woken, not among the three.
The old floor's acts (keeping, making, clearing; trimūrti) are late and Purāṇic; this option does not need them.

### (b) Sūrya, Vāyu, Agni: the three worlds
From «The sun in the triad». **The flow's proposal**.
```
Research   tisra eva devatāḥ (only three gods): Agni earth, Vāyu or Indra midspace, Sūrya heaven (Nirukta 7.5, S)
           Agni second only to Indra in Rigvedic hymns; hymn 1.1 is to Agni (S); Vāyu as Śani, Agni as Maṅgala (BPHS 3.20, S)
```
**Contested.** It puts the Sun in the always-open base: against "it's not always on."
BPHS 3.18 makes Agni the Sun's own deity; the Sūrya Siddhānta's authority is Sūrya's, its reckoning all seven.

### (c) Another of his
```
Research   none for a triad you have not named
Researched Sūrya, Budha, Śani (book 13's b); the vyāhṛti bhūḥ, bhuvaḥ, svaḥ, earth, space between, heaven (book 12's c)
```

## 4. The lattice to seven: unruled

**Unruled.** Which lines open later, and out of which parent, waits on the triad.
```
Under (a)   awake: Candra, Budha, Śani      woken: Sūrya      open later: Maṅgala, Śukra, Guru
            parents by strand (BPHS 3.22): Maṅgala out of Śani (tamas), Śukra out of Budha (rajas),
            Guru out of Candra (sattva)                                            Reading
Under (b)   base: Sūrya, Vāyu as Śani, Agni as Maṅgala      open later: Candra, Budha, Guru, Śukra
            parents (book 13): Candra and Guru out of Sūrya, Budha out of Vāyu, Śukra out of Agni
Under (c)   whatever your triad leaves out, parents to be drawn
```
Under (a) the Sun is not opened by demand: it is woken. The opening order and tie order wait on ruling 1.
A line folds back into its parent when its demand falls; the base never folds.

## 5. Demand and availability

**The flow's proposal**, as book 12 has it. Every number is the flow's default. Ruling 4.

### What is counted
```
Demand        queued messages on its topics · living records on its topics
              open proposals awaiting your ruling · its flows past the changeover share
Pressure      messages + records + 2 × proposals + full flows
Availability  quota left against due left = 1 − day/7, your "about 14% per day" · a seat free
```

### The rule
```
Expand    pressure ≥ 8 at 3 readings in a row, and quota left ≥ due, and a seat free
Hold      pressure 3 to 7: nothing changes
Contract  pressure ≤ 2 at 6 readings in a row, once open at least 6 readings
          or quota left < due: the open line with the least pressure folds
Limits    one change per reading; never under three, never over seven
Reading   taken at an event: a turn end, an enqueue, a record published, a ruling; never on a timer
```
Hysteresis: the gap between 8 and 2, the run of readings each side needs, and the six-reading minimum span.

### As ethos, one datom each
```
Demand.{ QueuedMessages LivingRecords OpenProposals FullFlows }      { 5 1 1 0 }
Availability.{ QuotaLeft QuotaDue SeatsFree }                       { 0.62 0.57 2 }
Reading.{ Demand Availability }                                     { { 5 1 1 0 } { 0.62 0.57 2 } }
Threshold.{ Pressure Readings }                                     { 8 3 }
```
Counts are Integers; QuotaLeft and QuotaDue are decimals.

[drawing: Demand and availability feed a reading that expands, holds or contracts the set]

Figure 2. The cycle, from «Metaflows that expand and contract». **The flow's proposal**: a reading at an event expands, holds or contracts by one line at most.

### Not measured yet
```
Context share    no flow can read its own context size; "full flows" reads zero until it can
Topic counters   no Nexus counts messages or records per topic
Persona          named as where quota accounting goes; not built
```

## 6. Clusters

**His**: they "span and contract and eventually even possibly disappear"; "3-to-5-to-12 metaflows".
**The flow's proposal**, as book 12 has it:
```
Purpose     the situation or goal it serves, one sentence
End         one sentence, put to the judge
Judge       who rules the end met: ruling 5
Opened by   a ruling of yours, or a goal a seat sets
Size        3, then 5, then 12, by the rules of section 5, under a ceiling of its own
Home        the line that receives its leftovers when it ends
```

```
EndCondition.String
Opener.[ Ruling.String Goal.String ]
Judge.[ Jev Sun Seat.FlowId ]                                ; Sun added beside book 12's two
Cluster.{ ClusterName Purpose Opener EndCondition Judge Home Vector<MemberName> ClusterState }
```

### Today's four, as examples
*Reading*: which of these is a cluster is the flow's reading.
```
Ethos design               design and implement ethos; books before you, not yet its own flow
Chronos entry-point test   one query over a real socket; branch only, remote test times out
Skill migration            every skill at home in psyche, mind or field; dry run waits on your numbers
Jev evaluation             a typed decision at Flow's decision points; rollout held for the reuse investigation
```

[drawing: The Chronos entry-point test as a cluster: opened on a goal, spanning to three lines, held at a blocker, its end a judgment still to come]

Figure 3. One cluster's life, from «The geography of the Metaflows». *Reading*: its end is a judgment, not a date.

## 7. Where it lives: Flow

**The flow's proposal**. Re-read against the files as they stand.

```
File      /git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos
Now       LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
Proposed  LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect Option<MetaflowName> PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
Why       a flow names the Metaflow it continues; None is a flow spawned for its own goal
```

```
File      /git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos
Now       requests end … QueueTurnEnd.TurnEndRequest Report.{ FlowId Event } ]
Proposed  … Report.{ FlowId Event } Weigh.Weighing Metaflows.{} OpenCluster.Cluster EndCluster.ClusterName ]
Why       counts reach Flow through Weigh; the set and its clusters are read and changed through Flow
```

```
File      /git/github.com/LiGoldragon/flow/crates/flow-nexus/ethos/operation.ethos
Now       Record.[ Intent.NativeLaunchIntent … Settled.{ LaunchRequestId LaunchOutcome } Harness.{ FlowId Event } ]
Proposed  Record.[ … Harness.{ FlowId Event } Expanded.Opening Contracted.Folding Clustered.Cluster ]
Why       Flow's memory keeps each change beside the flows it already holds; Open is taken, by Open.ComposedLaunch
```
**Unruled.** Under (a) the Sun is woken, not Open or Folded; book 12's MetaflowState has no state for it yet.

[drawing: Where Metaflow and Cluster records sit in Flow]

Figure 4. The proposed places, from «Metaflows that expand and contract». Black: today. Brown: the flow's proposal. Dashed: not built.

## 8. The map

[drawing: Three always-awake lines around the Sun, with four clusters on an orbit]

Figure 5. The geography, from «The geography of the Metaflows». *Reading*: three lines never sleep; the Sun is woken through the gate; clusters circle and pass.

**His**, on the 3×4 table of voices: "Maybe it's not organic enough."
```
The twelve voices    aspect [ Psyche Mind Field ] × layer [ Primary Secondary Tertiary Quaternary ]: who answers, at what power
The map              which line runs, which sleeps, which cluster is open
Overlap              the Sun is the primary layer: the two already touch there              Reading
```

## 9. Rulings

Each: the options, then the flow's recommendation, not yours.
```
1  The triad            a  Moon, Mercury, Saturn always awake; the Sun woken
                        b  Sūrya, Vāyu, Agni: the three worlds
                        c  another of yours (say which)
                        Recommendation: a; it is your latest word, and the Sun stays primary
2  The Sun's charge     a  yes: judgment
                        b  amend (say what)
                        Recommendation: a
3  The three awake      a  yes: Budha hears and routes · Candra keeps and interprets · Śani limits and measures
                        b  amend (say which line, and what moves)
                        Recommendation: a
4  Thresholds           a  your numbers (say them)
                        b  the flow's defaults: expand 8 for 3 readings, contract 2 for 6, span 6, due 1 − day/7
                        c  the defaults, tuned after a trial period
                        Recommendation: c
5  Who judges a         a  Jev, a typed question on the end condition, a seat confirming
   cluster ended        b  the Sun, woken for it
                        c  a seat: the one that opened it
                        d  you
                        Recommendation: a, raising to b when Jev's answer is unsure
6  The map              a  stands beside the 3×4 table of voices
                        b  replaces it
                        Recommendation: a; the voices are wired in Flow today, the map is not
7  The Flow records     yes: LaunchProfile names its Metaflow; Weigh, Metaflows, OpenCluster, EndCluster;
                        Flow's memory records Expanded, Contracted, Clustered
                        Recommendation: yes
```
<!-- to-the-living:end -->


## flows/bad807/vision/distillation.md

# Distillation

## The machine stuffs too much into the distillation, turning specifics into generals; until Sema carries annotated psyche, what is vision, what is instruction and what is a situational intervention is untangled by hand

Context: typed in chat to this flow after commenting on the context-module books.

> I've commented on the context module book and one pattern that emerges and is becoming a really big problem for progress to take place: the machine is trying to stuff too much into the distillation and is using specifics and trying to turn them into generals. Things that were like orders given or specific instructions for a specific situation are clumsily being turned, or the machine is attempting to turn them into these general guidelines, which they're not. We've talked about this.
> ... Until then I guess we're going to have to manually untangle what is actual vision, what is specific instructions, and what is specific to a situation where I had to intervene and keep the machine from doing something wrong (even if it might have been because I misunderstood what the machine was doing or what was happening).

-- psyche, typed, 2026-10-04.

## Small, conservative proposals that infer less; a proposal is accepted whole

Context: typed in chat to this flow, after his comments on the context-module books.

> One of the patterns which we probably want to avoid is to make large distillation proposals and to be reckless in the proposal. It's better to be conservative and stay more general than to try to do more and then have nothing land because the proposal is not accepted. It has to be accepted whole. If the proposals are smaller, they're more likely to be accepted. If they're less experimental, less reckless, and try to infer less, then they're more likely to be accepted as well.

-- psyche, typed, 2026-10-04.

## A good visual becomes distilled vision; the format of distilled vision — data, format, version control — serves machine and human alike

Context: his comment on the book «The Nexus», on its shape drawing (the three parts and the enforced path). Relayed by aa887c.

> This is a good visual. I would like it to become an actual distilled vision. Let's talk about how we deal with distilling vision: data-wise, format-wise, version control-wise. What kind of format is this? What's the best format we want to use, something that both the machine can use as context and that humans can easily perceive?

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.


## flows/bad807/vision/presentations.md

# Presentations

## Every proposal says where it lands: here is how it is now, here is what we would like to change

Context: his comment on the book «Context modules: the standard and the first system-prompt modules», which named modules and rulings without naming the files they land in. Relayed by 28d847.

> I don't understand the context module book. Where is all of this text proposal being proposed to be put into? I'm supposed to know where things are. Everything is a proposal or an explanation of how: here's how it is now and here's what we would like to change ... Implementation can diverge from vision but what I'm saying is I don't understand what is being proposed or where these proposals are supposed to be edited into.

-- psyche, typed, 2026-10-04, relayed by 28d847.


## flows/bad807/vision/books.md

# Books

## Code blocks and minimal text; no revision hashes, no timestamps; visuals for every code or logic flow; never dense walls of text

Context: typed in chat to this flow after reading «A Nexus reads a value from a datom file».

> I was reading a nexus that reads a value from a datom and it's too compact, too dense. I don't want all these revision hashes and it's just one big huge wall of text. My senses are blocking it because it's hard to see and it's too dense. You need to visualize that stuff.
>
> Whenever there's code involved I need things to be broken up. I want code blocks and minimal text. I don't want all of these timestamps and sure, version numbers are cool but no revision hashes and visuals. I need visuals to visualize the code flow or the logic flow.
>
> I want all this in a skill. I don't want any more of this super packed, dense, impossible-to-read stuff so redo all the books this way.

-- psyche, typed, 2026-10-04.


## Vision/messaging.md

# Messaging

## A message is a datom, and it arrives as one

The message body is a datom that lands in the recipient's prompt as a
datom-formatted object. There is no envelope around it.

## Priority is a head on the datom

    Priority.[HardAbrupt MiddleAbrupt Soft]

## Delivery is harness-specific, and the mechanism differs per tier

Hard abrupt on Codex is one Escape, and the prompt submits itself. Hard
abrupt on Claude is two Escapes — the first is taken by the input editor in
vim mode and never reaches the harness — then the prompt, then an explicit
Enter, because after an interrupt the prompt is placed in the composer
without being submitted. Middle abrupt is the terminal prompt, which a
Claude recipient receives at its next tool boundary. Soft waits for the
recipient to finish.

## An interrupt witness is not a delivery witness

Inducing an interrupt, placing prompt text, submitting it, and the recipient
consuming it are four separate observations. None of them stands for
another, and a submission is never a read receipt.

## Only messages that act, deliver, or block

Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.


## flows/aa887c/vision/fableContext.md

# Fable context

## What the next Fable is started with

Context: his words to Field 42265e after closing the old Fable's window, relayed to this seat.

> Let's feed it:
> - all of the books
> - all of the recent books
> - what a psyche is
> - the basic skills
> - the Markdown content of the books that it made
> - all of the psyche and the vision that directly touches upon this
> Let's get that into the spirit and intent, its main roles, and assistant prompt, along with behavior, the main flow behavior, and all of that basic behavior stuff in the system prompt. The rest goes in the user prompt, along with the instructions and which skills to load.
> It should create a sort of "what is most salient, what sticks out most in all of that context, what seems most important, and what should be tackled first, because we would gain significantly by improving the whole persona, the whole meta harness."

-- psyche, STT.

## Opus helps build Fable's next context

Context: his additional words to Field 42265e.

> Let's get Opus also involved in building [Fable's] next context so that it has a really good understanding of:
> - all of my vision
> - most honed skills
> - all of the things that we're designing lately with the books

-- psyche, STT. Transcription corrected: "Fables'" → "Fable's".

## The first prompt is not the whole corpus

Context: on hearing that the composed first prompt for the new Fable is 2.4 MB (about 600k tokens): every book, every vision record and the source corpus in full.

> That's way too much. It would make the context too big from the first prompt so it's a bad idea from the beginning. ... There's way too much context there.

-- psyche, STT.


## flows/aa887c/vision/jev.md

# Jev

## Jev judges what enters the database, writes commits, checks the system

Context: his words to Field 42265e on starting the next Fable, relayed to this seat.

> I'm very interested in [Jev], and I think there's huge value there. Also, using the new Flow, better messages, and Datom syntax for basic commands for a lot of things, and using [Jev] to automate things like committing and judging if certain items can enter a database and things like that.
> When we get Psyche back up, we're going to have calls like that. [Jev] is perfect for judging if something should be edited or if it should be merged with some other text because it's kind of overlapping, so that the database doesn't grow too fast and there are no conflicting views on anything. It would be really useful to do the commit messages, check that the system is running, and check that there are no conflicting main flows.

-- psyche, STT. Transcription corrected: "Jav" → "Jev".


## flows/aa887c/vision/persona.md

# Persona

## Persona backs up, restarts the cluster, and runs the monitors

Context: his words to Field 42265e on starting the next Fable, relayed to this seat.

> I think we should use persona and start giving persona the power to actually start:
> - make a backup
> - know how to restart the whole cluster, the whole persona, all the meta flows, with the right context
> - run the monitor jobs
> It can maybe make the dev [sic] calls to monitor the system and maybe take action if something has failed or one of the AI providers is offline, and we need to go to a backup model or something like that.

-- psyche, STT.


## flows/aa887c/vision/nexus.md

# Nexus

## The three parts and one path land, with example code

Context: his comment on the book «The Nexus», proposal 1 (Vision/nexus.md, new section "Three parts and one path").

> This is good. Can land, and I would also like to have example code to show with it.

-- psyche, STT.

## Signal and memory talk only to operation

Context: his comment on the book «The Nexus», proposal 2 (Vision/nexus.md, new section "The standard entry point").

> Let's flesh this out in actual code. Could we say it better: an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory. Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process.
>
> Let's look at the actual code and how this could be done in multiple various ways. Let's test it. Let's have it tested on an actual component that we have written, like Flow, Message [sic], or Orchestrate, on a branch, and see if it works as the other component or if we could make it work. A toy, I mean, or a simple nexus which isn't in production, something that we've been drafting.
>
> Maybe let's do something useful. If we're going to test anything, we might as well test one of our non-production-ready ideas. You can hand this over to Astra once you have the design and the book. I want extensive: I want to see code. I want to see visual architecture. I want to feel like you have some meat there on that bone.

-- psyche, STT.

## The core library's language refined after practice

Context: his comment on the book «The Nexus», on the proposed text "The nexus repository is the core library of every Nexus…".

> Again after we see how this works in practice, let's refine the language so that it's more accurate to what's possible and what we actually want in practice. In terms of whether it is an actor-based language or whether it is different

-- psyche, STT.

## A Nexus pulls a value from a datom file

Context: his comment on the book «The Nexus», on the proposed text "Every client speaks to a Nexus in pure signal, fully binary…".

> Yes this is good and I also want to design something that would let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this but it would be a fairly simple call, I guess, where it would have a variant `me` [sic] that would tell it what type of CLI you would have to use, essentially. That means storing a string somewhere because the CLI is invoked with a system call that uses a string. There's a string involved no matter what unless all of that is, again, put into an external tool. Anyway let's look at different ideas here, with Fable being the lead designer on this and passing it down as a book.

-- psyche, STT.


## flows/aa887c/reports/fable-transcript-direction.md

# Where bad807's discussion was going: for the next Fable

Source: transcript `~/.claude/projects/-home-li-primary/bad807ad-3be6-4543-9f3f-bdc5ef1850f8.jsonl`. "L" is the transcript line number. Scope: the last third, from L2253 (21:18), to the end, L3364 (00:35). The final books came out at L3252–L3287.
Coverage marks: **vision** = flows/bad807/vision/, **notion** = flows/bad807/notion/, **log** = flows/bad807/log.md, **books** = flows/bad807/reports/books.md, **ctx** = flows/aa887c/reports/fable-context-contribution.md.

## (a) His latest words not yet in any vision/notion/Vision record

Every other typed message in this span is already recorded verbatim, in vision/metaflow.md, vision/gatedFlows.md, vision/jev.md, vision/ontology.md, vision/contextModules.md, notion/voices.md, notion/metaflowDimensions.md or notion/openSourceModels.md. Four are not:

1. L2253: "All I said was the model for the tertiary is Luna Medium and Sonnet Medium."
   Covered as a ruling in log:183 and aa887c/log.md:40. Not recorded as vision.
2. L2768: "Do you want to step back and take a fresh look at everything because this seems just very one-sided? What do you think?"
   Paraphrased in log:233 ("Books paused on his question about one-sidedness"). Not recorded in his words. **Uncovered.**
3. L2833: "Well that was more like a question. What would the son be in charge of?"
   [son = sun] Only his answer to it is in vision/metaflow.md: L2841, "Yeah no, that's good." The question itself is not. Low weight.
4. L2868: "So why don't you just re-update all of the books that you've been authoring and then let's take everything into mapping out the new geography of the meta flows. Are we using Flow yet? When can we expect to rebootstrap on Flow?"
   Paraphrased in log:239. Not in his words. **Uncovered.** It is his last typed message in the flow.

## (b) Design threads Fable had open

- **Ranked gate.** In L3252/L3287 Fable says only three books block building: «Context modules» (7 rulings), «Three skill repositories and the main workspace» (10) and «Jev» (7). Covered: log, ctx 2.1/2.3.
- **Rebootstrap on Flow.** L2904 gives a forced order:
  1. his numbers on workspace/placing;
  2. Mind's generator change;
  3. the main-workspace repository, which does not exist yet;
  4. Flow 0.24.0 deployed, launching seats from role records, with the launcher retired.

  Witnessed at L2904: Flow 0.23.0 tracks no live seat. Covered in log:241. Not in ctx; the next Fable needs this order.
- **Metaflows design.** The open points are:
  - the base triad: his L2724 Sun correction against his L2784/L2798 notion;
  - the three always awake (Saturn, Mercury, Moon) and the Sun woken for judgment (L2828–L2836);
  - the Sun's handover, which carries only the undecided (L2841).

  All of these are in «Metaflows» (16-metaflows.md) with 7 rulings. Its ruling 2 (the Sun's charge) is already answered "yes" in L2841, so it only needs confirming. Covered: log, vision, books.
- **Metaflow as a Flow component.** This is a Metaflow record with an optional end; LaunchProfile names the Metaflow it continues, and Replace continues the same one. It "waits on his yes to the direction" (log:189). Promised as "its own small book" at L2295 and never delivered as one. **Not in ctx.**
- **Sun unwind and handover.** Promised in L2863 and again in L3287: "When you want this Sun to unwind, say so and I write the summary and handover with the undecided marked." Not delivered, because the living closed the flow. **Uncovered in ctx.** This report and ctx stand in for it.
- **Working commitments.** At L2779 Fable committed to:
  - "stop issuing books";
  - "build what you rule, and let the next book come from something built and witnessed rather than from the next idea";
  - "I would read every page before it goes to you".

  The last one was kept for the standing editions (log:249–259). **Not in ctx.**
- **Migration.** Build blockers and refusals are ruled (L3307, L3332; log:263–265). The secretary creates the flow-data repository, and Astra owns the roles.datom reshaping and the generator. Nothing runs before his numbers. Covered: log, ctx 2.1.
- **Chronos entry-point branch.** The test failed to compile on two type errors at daemon.rs:69 and :74. Repair, plus one run, is authorized; no merge (L3364; log:269). Covered: log.
- **Jev.** fuzzy-jev 0.6.0 speaks /alpha/decisions directly, so no bespoke adapter is needed. It is to be evaluated by witness once the key exists (L3344; log:267). Covered: log.

## (c) Questions Fable put to him, still unanswered

- **Every ruling in the standing books.** The list is in «The standing books, ranked…»: https://claude.ai/artifact/QTJMdEdkBCSdDXVuHbv2TH. The three first books gate building. Covered: ctx, books.
- **L2943 and «The geography of the Metaflows».** Does the map stand beside the table of voices or replace it? Are the three always-awake lines in charge of what it lists? Which clusters are open now? These were folded into the «Metaflows» rulings. Covered in log.
- **L2863/L3287.** "When you want this Sun to unwind, say so". Unanswered. The flow was closed instead.
- **L2779.** "What do you want: that ranking, or a different cut?" Superseded: he ordered the re-update at L2868, and the ranking was delivered at L3287.
- **«Metaflow, into the vocabulary».** Its second ruling, the direction for Flow's component (L2358). Unanswered. Not in ctx.

## (d) His corrections of Fable's behavior

- L2768, the one-sidedness question, quoted in (a). **Uncovered in vision.**
  Fable's own diagnosis at L2779:
  - 28 books went out with no numbers back;
  - the Sanskrit line went further than his words;
  - Fable had not read the books itself;
  - a specific had twice been turned into a general.
- L2648: "The 3-inside-4 is interesting but not quite my point." Covered: vision/metaflow.md.
- L2724: "How can we keep the sun out of the basic triad? That seems like sacrilege." Covered: vision/metaflow.md.
- L2798: "No I don't really vibe with this whole..." and L2820: "No, by "wake" I mean "wake it" because it's not always on." Covered: notion/metaflowDimensions.md.
- Earlier, still governing the work:
  - L1026, "the machine is trying to stuff too much into the distillation and is using specifics and trying to turn them into generals". Covered: vision/distillation.md.
  - L1669, "too compact, too dense … no revision hashes … I need visuals". Covered: vision/books.md and ctx 3.1.

## (e) Fable's last statement of priorities

L3287: "Nothing of mine is in motion. Three things remain, none of them mine to start: your numbers on «Context modules», «Three skill repositories and the main workspace» and «Jev», which release the Secondary's migration and Mind's generator and workspace; Astra's test receipt on the Chronos branch; and the publisher clearing so this lane's records and books reach main."

It is restated in L3364: "your numbers on the three first books remain the gate." Covered: log, ctx 2.1/6.

## Sources

- Transcript bad807ad-3be6-4543-9f3f-bdc5ef1850f8.jsonl, lines cited above. Read by line-scoped jq extraction; the `transcript` CLI is not installed. Provenance receipt: unavailable.
- flows/bad807/log.md, flows/bad807/reports/books.md, flows/aa887c/reports/fable-context-contribution.md, flows/bad807/vision/*.md, flows/bad807/notion/*.md, flows/bad807/books/16-metaflows.md, Vision/.


## flows/aa887c/reports/fable-context-contribution.md (section 2 only)

## 2. What waits for his answers

### 2.1 First priorities

- Skill migration into psyche-skills, mind-skills and field-skills, with psyche-logs and flow-data.
  - Fully prepared; dry run passes.
  - Script: `flows/aa887c/scripts/migrate-skills.sh`
  - Table: `flows/aa887c/reports/placing-table.md`
  - Waits on his numbers on the workspace edition: stem case; conduct rules as vision or intent; the prefix paragraph.
- Astra's part: the curriculum-deploy change and the main-workspace bootstrap, with the new roles.datom shape.
  - Prepared Psyche Primary record text: `flows/aa887c/scripts/roles/psyche-primary.datom`

### 2.2 Design books before him

- Ethos structs over chained variants.
- The format of distilled vision.
- The datom-file pull.
- The entry-point actors (signal and memory talk only to operation). Code: `flows/bad807/evidence/entry-point/`
- Jev use and the Jev ecosystem.
- Metaflows and metaflow roles.
- Nesting.
- The sun triad.
- Geography.
- «The shape of a book, into the skill».

### 2.3 Standing editions

- «Context modules» — https://claude.ai/artifact/JGdUchiTpNgwLYfaqwaBWc
- «Three skill repositories and the main workspace» — https://claude.ai/artifact/JKSJRFpH8FKSuizbobXiDd
- «Jev» and «Metaflows»: URLs in the list below.
- All book URLs come from `flows/bad807/reports/books.md`.

### 2.4 Every book

Format: title — URL — Markdown source. Editions of one title (first, reshaped, amended) share the latest source file. A source marked "no local source" has no Markdown under `flows/bad807/books/`. Rulings sit beside sources as `flows/bad807/books/<n>-<name>.rulings.md`. Where each book stands: `flows/bad807/reports/book-revision-inventory.md`.

- «Context modules: the standard and the first system-prompt modules» — https://claude.ai/artifact/LshbWB3qxFt8VCjfMyhKGV — no local source under flows/bad807/books/
- «Context modules: where each proposal lands» — https://claude.ai/artifact/9WmPNMnkA5wkuxYncp9Wp1 — no local source under flows/bad807/books/
- «Context visibility: every flow's context and quota on one screen» — https://claude.ai/artifact/Mwtt8GoFXeySjWAbXhQxmh — no local source under flows/bad807/books/
- «Datom» — https://claude.ai/artifact/5QXhkrZ6bUmHdWuzn3thJP — `flows/bad807/books/2-datom-v2.md`
- «Flows per topic: a notion and what others have done» — https://claude.ai/artifact/SqwVZaiNJoMczvUsfEWccK — no local source under flows/bad807/books/
- «Signal» — https://claude.ai/artifact/6GTtzM8b6bdYBbzNGVacZD — `flows/bad807/books/4-signal-v2.md`
- «Three skill repositories and the main workspace» — https://claude.ai/artifact/6zgqzzzrUWwsotzHokqUNp — `flows/bad807/books/17-workspace.md`
- «Operation» — https://claude.ai/artifact/PPtohyLV2pLud82PAuDEoE — `flows/bad807/books/6-operation-v2.md`
- «The Nexus» — https://claude.ai/artifact/PoCBpppWC8u6ZV5H1BYCmm — `flows/bad807/books/3-nexus-v2.md`
- «Context modules: your two comments answered» — https://claude.ai/artifact/4RvF3E1VkjHi3xtCC8udre — no local source under flows/bad807/books/
- «Ethos» — https://claude.ai/artifact/MUG7U2QATCFoJFB3S4Vqsq — `flows/bad807/books/1-ethos-v2.md`
- «Memory» — https://claude.ai/artifact/XmniNLyZmteyJC7J4t43Y5 — `flows/bad807/books/5-memory-v2.md`
- «Placing the skills: three questions» — https://claude.ai/artifact/FkXPdP5rkm8Y9Jz7KpocWY — no local source under flows/bad807/books/
- «Two lines of your vision touched by the placing» — https://claude.ai/artifact/EMUmU7ntRjrxUdbrjdcHFN — no local source under flows/bad807/books/
- «Ethos: structs over chained variants» — https://claude.ai/artifact/BYjpo6agaJqRDF8ijWwJyw — no local source under flows/bad807/books/
- «The format of distilled vision» — https://claude.ai/artifact/U8T8csR4q3cp4KP9CReH6b — no local source under flows/bad807/books/
- «A Nexus reads a value from a datom file» — https://claude.ai/artifact/1saCmAi5wZ6m6objefUoik — `flows/bad807/books/8-datom-file-v2.md`
- «The standard entry point: three actors, one path» — https://claude.ai/artifact/UnMFEjS3nBE5gDVvoXsWL9 — `flows/bad807/books/7-entry-point.md`
- «The shape of a book, into the skill» — https://claude.ai/artifact/Cq3qraDQxYUQt9asLeP6re — no local source under flows/bad807/books/
- «Ethos» (reshaped) — https://claude.ai/artifact/XjAvCXLxbMty667gnVFFVE — `flows/bad807/books/1-ethos-v2.md`
- «The Nexus» (reshaped) — https://claude.ai/artifact/EuYQop6yAY18iyaY6uDuWD — `flows/bad807/books/3-nexus-v2.md`
- «Operation» (reshaped) — https://claude.ai/artifact/AaPtaTKrJMRhBDHDa95v2V — `flows/bad807/books/6-operation-v2.md`
- «Memory» (reshaped) — https://claude.ai/artifact/G9Ctu1HeQSFzqmQT9LUmDQ — `flows/bad807/books/5-memory-v2.md`
- «Signal» (reshaped) — https://claude.ai/artifact/DGdAnXwjHFfMFEAtwnEFHw — `flows/bad807/books/4-signal-v2.md`
- «Datom» (reshaped) — https://claude.ai/artifact/CGMnvpbxu5WV5jpqjq2HyW — `flows/bad807/books/2-datom-v2.md`
- «A Nexus reads a value from a datom file» (reshaped) — https://claude.ai/artifact/P7e8miuzGpRN1URGYxiDLc — `flows/bad807/books/8-datom-file-v2.md`
- «Jev: what Mind and Psyche agree on» — https://claude.ai/artifact/7mkRZ8AxEGH7umF9bVCPpg — no local source under flows/bad807/books/
- «Tertiary and quaternary voices» — https://claude.ai/artifact/Suwbq4VTnFV9uPqxKpd4Vw — no local source under flows/bad807/books/
- «Metaflow, into the vocabulary» — https://claude.ai/artifact/17eNj85ut2YsxNUynQGQRf — no local source under flows/bad807/books/
- «The Metaflows and the sets of three to seven» — https://claude.ai/artifact/2GPFEoS9ZLVWX3d3hfuVhq — no local source under flows/bad807/books/
- «Jev in the flow-handling system: where a typed decision helps now» — https://claude.ai/artifact/98MeaVj7EHvRTAfpTvkARN — `flows/bad807/books/9-jev-use.md`
- «The three inside the four: nesting, load, and the geometry of mind and speech» — https://claude.ai/artifact/EVoaJFrtMCCAmpn85A7XaE — `flows/bad807/books/10-nesting.md`
- «Our open-source stack and Jev: use, tools, plugins, infrastructure, trends» — https://claude.ai/artifact/RjkX3DVu9AGU15vQxXEWkk — `flows/bad807/books/11-jev-ecosystem.md`
- «Metaflows that expand and contract: three to seven, by demand and availability» — https://claude.ai/artifact/JmBjyo3b4NcFMxh41jpTYX — `flows/bad807/books/12-metaflow-roles.md`
- «The sun in the triad» — https://claude.ai/artifact/SP8s9iMexMBj9Qbabi4qLc — `flows/bad807/books/13-sun-triad.md`
- «The geography of the Metaflows» — https://claude.ai/artifact/3sk7cuiZphy57EJNYtrKDY — `flows/bad807/books/14-geography.md`
- «The Nexus» (amended) — https://claude.ai/artifact/5WtkWipRSiKc5SyGWuYSTN — `flows/bad807/books/3-nexus-v2.md`
- «Memory» (amended) — https://claude.ai/artifact/9hdSGyiKhtmjEFAo1S3s7P — `flows/bad807/books/5-memory-v2.md`
- «Signal» (amended) — https://claude.ai/artifact/HHbLiGgpcZxcq4jQTs4pgq — `flows/bad807/books/4-signal-v2.md`
- «Datom» (amended) — https://claude.ai/artifact/Af8ktTQNUxgJJCy3rJ3WER — `flows/bad807/books/2-datom-v2.md`
- «A Nexus reads a value from a datom file» (amended) — https://claude.ai/artifact/GHkkz725t7mYZrBJ8GiNCB — `flows/bad807/books/8-datom-file-v2.md`
- «The standard entry point: three actors, one path» (amended) — https://claude.ai/artifact/QFyEQ4ZDfqDshVBwYyW5CQ — `flows/bad807/books/7-entry-point.md`
- «Ethos» (amended) — https://claude.ai/artifact/47UdBWDgymNkzNWFwwRJay — `flows/bad807/books/1-ethos-v2.md`
- «Metaflows» (standing edition) — https://claude.ai/artifact/52nh2mXjUSnQizezFn6yxP — `flows/bad807/books/16-metaflows.md`
- «Jev» (standing edition) — https://claude.ai/artifact/PcJYyh1TqqorSvv7j2UpCU — `flows/bad807/books/18-jev.md`
- «Context modules» (standing edition) — https://claude.ai/artifact/JGdUchiTpNgwLYfaqwaBWc — `flows/bad807/books/15-context-modules.md`
- «Three skill repositories and the main workspace» (standing edition) — https://claude.ai/artifact/JKSJRFpH8FKSuizbobXiDd — `flows/bad807/books/17-workspace.md`
- «The standing books, ranked by what your numbers unblock» — https://claude.ai/artifact/QTJMdEdkBCSdDXVuHbv2TH — no local source under flows/bad807/books/

