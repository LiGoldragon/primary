<!-- to-the-living:start -->
Presentation.{ «Datom» }

How it is now. `Vision/datom.md` (315 lines) holds Name, Nature, A datom is a form at a path, Strings, Syntax, The datom composes, Any Rust type, From text and back, Containers, Errors, Omittable fields, The interface shape, De/serialization, Relation to Ethos, Repository, Map and Meaning: bare and «» strings, `{ }` struct, `[ ]` vector, `Head.` variant, no field names, no map. `Vision/protos.md` names datom the pure-data protos dialect and signal a parallel structure beside the text chain. `Vision/signal.md` (43 lines: What signal is, Query and response, Text and signal, Meta signal, Protocol) names no formats. `Vision/ethos.md` "The datom kinds are compiled in only where text is spoken" keeps datom-codec out of a Nexus build, and its Signal example declares `FlowId.String`. Where datom is used, the two forms, the flow id's type and how a new object is shown stand nowhere in Vision. In code: datom-codec 0.32.2 (`/git/github.com/LiGoldragon/datom-codec`, commit 4dff16b, 2026-10-02, 1689 lines of `src/`, on protos rev 15b41da) implements `Form` as Struct, Vector, Variant, Bare, String, Meaning, plus Decimal; ethos-zero 16.0.0 emits on every type `#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]`; signal-flow 10.0.0 declares `FlowId.String` (`ethos/signal.ethos` line 116). The datom lines of proposals 3, 7, 8 and 9 were checked with datom-codec 0.32.2 and the Rust blocks are ethos-zero 16.0.0 output (proposal 3: derive lines left out, each struct on one line), 2026-10-04.

### 1. Where datom is spoken [vision]

File: `Vision/datom.md`, a new section after "The interface shape". Assumes Ruling 1 (b).

Now: no such section.

Proposed:

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

Grounded: 2026-09-27, 8904b1, "where the program doesn't need it".

### 2. Datom beside protos and signal [vision]

File: `Vision/datom.md`, a new section after "From text and back".

Now: no such section.

Proposed:

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

Grounded: 2026-10-03, 5578cc, "without needing to know how to deserialize".

<svg viewBox="0 0 700 230" width="700" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="14" fill="currentColor">
<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
<rect x="8" y="30" width="500" height="150" rx="8" fill="none" stroke="currentColor" stroke-dasharray="6 4"/>
<text x="18" y="22">CLI and client, built with the datom feature</text>
<rect x="545" y="30" width="147" height="150" rx="8" fill="none" stroke="currentColor" stroke-dasharray="6 4"/>
<text x="552" y="22">Nexus, no datom-codec</text>
<rect x="20" y="80" width="90" height="50" rx="6" fill="none" stroke="currentColor"/><text x="65" y="110" text-anchor="middle">Text</text>
<rect x="140" y="80" width="90" height="50" rx="6" fill="none" stroke="currentColor"/><text x="185" y="110" text-anchor="middle">Protos</text>
<rect x="260" y="80" width="90" height="50" rx="6" fill="none" stroke="currentColor"/><text x="305" y="110" text-anchor="middle">Datom</text>
<rect x="380" y="80" width="118" height="50" rx="6" fill="none" stroke="currentColor"/><text x="439" y="110" text-anchor="middle">Composition</text>
<rect x="557" y="80" width="123" height="50" rx="6" fill="none" stroke="currentColor"/><text x="618" y="110" text-anchor="middle">Composition</text>
<line x1="110" y1="95" x2="138" y2="95" stroke="currentColor" marker-end="url(#a2)"/><line x1="230" y1="95" x2="258" y2="95" stroke="currentColor" marker-end="url(#a2)"/><line x1="350" y1="95" x2="378" y2="95" stroke="currentColor" marker-end="url(#a2)"/>
<line x1="138" y1="118" x2="112" y2="118" stroke="currentColor" marker-end="url(#a2)"/><line x1="258" y1="118" x2="232" y2="118" stroke="currentColor" marker-end="url(#a2)"/><line x1="378" y1="118" x2="352" y2="118" stroke="currentColor" marker-end="url(#a2)"/>
<text x="124" y="72" text-anchor="middle" font-size="12">protosize</text><text x="244" y="72" text-anchor="middle" font-size="12">datomize</text><text x="364" y="72" text-anchor="middle" font-size="12">compose</text>
<text x="124" y="150" text-anchor="middle" font-size="12">textualize</text><text x="244" y="150" text-anchor="middle" font-size="12">protosize</text><text x="364" y="150" text-anchor="middle" font-size="12">datomize</text>
<line x1="498" y1="95" x2="555" y2="95" stroke="currentColor" stroke-width="2" marker-end="url(#a2)"/><line x1="557" y1="118" x2="500" y2="118" stroke="currentColor" stroke-width="2" marker-end="url(#a2)"/>
<text x="527" y="150" text-anchor="middle" font-size="12">signal</text>
<text x="350" y="215" text-anchor="middle" font-size="13">The text chain runs only inside the CLI; between programs only signal moves.</text>
</svg>

The text chain lives in the CLI; the Nexus sees only compositions carried by signal.

### 3. One query, two formats [vision]

File: `Vision/signal.md`, a new section after "Query and response".

Now: no such section.

Proposed:

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

Grounded: 2026-10-03, edf227, "cast into a different container".

The Simple and Extended names and the one `Asking` type holding both are this flow's proposal, not his; he asked for two formats of one query.

Ethos-zero 16.0.0 accepts the spec above and generates:

```rust
pub struct Simple_Data { pub role: Role, pub question: Question }
pub struct Extended_Data { pub flow_id: FlowId, pub role: Role, pub question: Question }
pub enum Asking { Simple(Simple_Data), Extended(Extended_Data) }
pub enum Query { Ask(Asking) }
```

<svg viewBox="0 0 700 250" width="700" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="14" fill="currentColor">
<defs><marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
<text x="160" y="22" text-anchor="middle">the living, an everyday CLI call</text>
<text x="530" y="22" text-anchor="middle">another component, debugging</text>
<rect x="20" y="32" width="280" height="44" rx="6" fill="none" stroke="currentColor"/><text x="160" y="59" text-anchor="middle" font-family="monospace" font-size="13">Simple.{ Role Question }</text>
<rect x="370" y="32" width="320" height="44" rx="6" fill="none" stroke="currentColor"/><text x="530" y="59" text-anchor="middle" font-family="monospace" font-size="13">Extended.{ FlowId Role Question }</text>
<line x1="160" y1="76" x2="300" y2="122" stroke="currentColor" marker-end="url(#a3)"/><line x1="530" y1="76" x2="400" y2="122" stroke="currentColor" marker-end="url(#a3)"/>
<rect x="225" y="124" width="250" height="44" rx="6" fill="none" stroke="currentColor" stroke-width="2"/><text x="350" y="151" text-anchor="middle">Asking: one type, two containers</text>
<line x1="350" y1="168" x2="350" y2="196" stroke="currentColor" marker-end="url(#a3)"/>
<rect x="225" y="198" width="250" height="40" rx="6" fill="none" stroke="currentColor"/><text x="350" y="223" text-anchor="middle">Query Ask.Asking, to the Nexus</text>
</svg>

Both formats arrive as one query type; only the container differs.

### 4. A new object is shown first as its ethos spec [vision]

File: `Vision/ethos.md`, a new section after "Self-description".

Now: no such section.

Proposed:

````markdown
## Shown first as ethos

Every machine-to-machine language made along the way is ethos.
Whenever a new object is presented, a kind, a message or a datom, its
ethos spec comes first, and an example datom follows, showing the
object in use: how it is used and the queries and responses it
produces. Ethos that is shown is always correct ethos; a block that
lacks its type is not ethos.
````

Grounded: 2026-10-02, 91ea9f, "the ethos and the example datom".

### 5. Titles and presentations are datom [vision]

File: `Vision/datom.md`, a new section after "The interface shape".

Now: no such section.

Proposed:

````markdown
## Titles and presentations

Every title is a datom: a variant naming what the thing is, carrying a
struct of its parts, `PsycheV2.{ Fable 6329f1 }`. A presentation to the
living opens with one datom line naming it, `Presentation.{ «Datom» }`,
and wherever code logic is involved it shows ethos and datom: the
ethos spec of each type it introduces, an example datom in use, and
high-level code where the logic is the point.
````

Grounded: 2026-09-25, e51411, "the titles will be everywhere"; 2026-10-04, 5ed94b.

### 6. An identifier is a value; its text is datom's [vision]

File: `Vision/datom.md`, a new section after "Datom beside protos and signal". Assumes Ruling 2 (a).

Now: no such section.

Proposed:

````markdown
## Identifiers and their text forms

An identifier is a value of its own type, and its text forms belong to
datom. The flow id is a hash, held as a number of its own type,
`FlowId.{ Integer }`. A Nexus stores, keys and compares the number and
never sees text. Its renderings, six hex characters today and three
words later, are reversible, and live only on the side that faces
text, with the datom kinds.
````

Grounded: 2026-10-03, edf227, "The Nexus just thinks of it as a hash".

<svg viewBox="0 0 700 230" width="700" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="14" fill="currentColor">
<defs><marker id="a6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
<rect x="8" y="28" width="684" height="92" rx="8" fill="none" stroke="currentColor" stroke-dasharray="6 4"/>
<text x="18" y="20">CLI side, datom feature: the renderings</text>
<rect x="30" y="50" width="170" height="48" rx="6" fill="none" stroke="currentColor"/><text x="115" y="79" text-anchor="middle" font-family="monospace">hex: 6329f1</text>
<rect x="265" y="50" width="170" height="48" rx="6" fill="none" stroke="currentColor" stroke-width="2"/><text x="350" y="79" text-anchor="middle">FlowId (number)</text>
<rect x="500" y="50" width="170" height="48" rx="6" fill="none" stroke="currentColor"/><text x="585" y="79" text-anchor="middle">three words</text>
<line x1="263" y1="66" x2="202" y2="66" stroke="currentColor" marker-end="url(#a6)"/><line x1="202" y1="84" x2="263" y2="84" stroke="currentColor" marker-end="url(#a6)"/>
<line x1="437" y1="66" x2="498" y2="66" stroke="currentColor" marker-end="url(#a6)"/><line x1="498" y1="84" x2="437" y2="84" stroke="currentColor" marker-end="url(#a6)"/>
<text x="232" y="112" text-anchor="middle" font-size="12">render / read</text><text x="468" y="112" text-anchor="middle" font-size="12">render / read</text>
<line x1="350" y1="100" x2="350" y2="160" stroke="currentColor" stroke-width="2" marker-end="url(#a6)"/>
<text x="360" y="140" font-size="12">signal carries the number</text>
<rect x="190" y="162" width="320" height="48" rx="6" fill="none" stroke="currentColor"/><text x="350" y="191" text-anchor="middle">Nexus: stores, keys, compares the number</text>
</svg>

The number crosses the wire; text forms exist only where text is read and written.

### 7. Flow's id becomes its own type [implementation]

File: `/git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos`, line 116. Built on a yes to Ruling 2 (a).

Now:

```
[ FlowId.String
```

Proposed:

```
[ FlowId.{ Integer }                  ; a flow's id: a hash, a number of its own type
```

Ethos-zero 16.0.0 generates from it:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct FlowId {
    pub integer: i64,
}
```

Measured, datom-codec 0.32.2 writes this id as `{ 12232711 }`. The hex and word renderings of proposal 6 are not generated by ethos-zero 16.0.0; until the generator links a rendering to the datom form, they are a hand-written impl in the CLI crate.

Grounded: 2026-10-03, edf227, "The flow ID is not a string, it's a hash".

### 8. The datom skill says where datom is spoken and names the formats [implementation]

File: `/git/github.com/LiGoldragon/Curriculum/skills/datom.md`, a new section after "A datom needs a type" (line 104).

Now: no such section.

Proposed:

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

Grounded: 2026-09-28, 8904b1, "when the tool actually uses Datom".

### 9. The presentation line has a type [implementation]

File: `/git/github.com/LiGoldragon/Curriculum/skills/main-flow.md`, line 39.

Now:

```
A presentation meant to become a book, or to change one, sits between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, each on its own line, and its first line inside is one datom naming the book, `Presentation.{ «title» }`; a quoted marker stays inline. Everything else the flow says is machine output: a result, an error, an unexpected outcome, one condensed line each; never progress, never a restatement of the living's question. A conversational answer to the living carries no markers.
```

Proposed:

```
A presentation meant to become a book, or to change one, sits between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, each on its own line, and its first line inside is one datom naming the book, `Presentation.{ «title» }`, in a position expecting `Block.[ Presentation.{ Title } ]` with `Title.String`; a quoted marker stays inline. Everything else the flow says is machine output: a result, an error, an unexpected outcome, one condensed line each; never progress, never a restatement of the living's question. A conversational answer to the living carries no markers.
```

The type, and what it does today:

```
Library
[]                                     ; imports
[ Title.String                         ; types
  Block.[ Presentation.{ Title } ] ]   ; a block's metadata line
[]                                     ; kinds
[]                                     ; associations
```
```
Presentation.{ «Datom» }    ; read by datom-codec 0.32.2 into Block::Presentation, title Datom
Presentation.{ Datom }      ; the same value, as datom-codec's canonical print writes it
```

Grounded: 2026-10-01, fe945a, "the metadata is one datom line".

### Rulings

1. Datom everywhere, or only where a program needs it.
   (a) Datom everywhere: all the CLIs, the system prompt of every machine call. 2026-09-15 (692df8), 2026-09-19 (b81560).
   (b) Datom only where the program needs it; none forced on a messenger. 2026-09-27 (8904b1), 2026-09-28 (8904b1).
   Proposals 1 and 8 assume (b).
2. The flow id's type.
   (a) A hash, a number of its own type; text forms are serialization outside the Nexus. 2026-10-03 (edf227, his words).
   (b) A string: `FlowId.String` in `Vision/ethos.md` (2026-09-09) and in signal-flow 10.0.0 (2026-10-03).
   Proposals 6 and 7 assume (a).
<!-- to-the-living:end -->
