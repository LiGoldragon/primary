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
<svg viewBox="0 0 480 250" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><polygon points="240,8 410,48 240,88 70,48" fill="#7b6be0" fill-opacity=".14" stroke="#7b6be0"/><text x="240" y="54" text-anchor="middle" font-weight="600">Does the program read text?</text><line x1="150" y1="70" x2="120" y2="116" stroke="#8a9792" stroke-width="2" marker-end="url(#m1)"/><text x="118" y="96" text-anchor="end">yes</text><line x1="330" y1="70" x2="360" y2="116" stroke="#8a9792" stroke-width="2" marker-end="url(#m1)"/><text x="362" y="96">no</text><rect x="10" y="120" width="220" height="120" rx="8" fill="#1f9e89" fill-opacity=".14" stroke="#1f9e89"/><text x="120" y="146" text-anchor="middle" font-weight="600">speaks datom</text><text x="120" y="174" text-anchor="middle">a CLI's argument, answer</text><text x="120" y="198" text-anchor="middle">a message between machines</text><text x="120" y="222" text-anchor="middle">a title</text><rect x="250" y="120" width="220" height="120" rx="8" fill="#d08a1e" fill-opacity=".14" stroke="#d08a1e"/><text x="360" y="146" text-anchor="middle" font-weight="600">speaks no datom</text><text x="360" y="174" text-anchor="middle">a Nexus: signal only</text><text x="360" y="198" text-anchor="middle">a messenger: carries</text><text x="360" y="222" text-anchor="middle">what it is given</text>
</svg>

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
<svg viewBox="0 0 480 420" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><text x="14" y="24" font-weight="600">CLI, built with the datom feature</text><rect x="8" y="32" width="464" height="200" rx="10" fill="#1f9e89" fill-opacity=".07" stroke="#1f9e89" stroke-dasharray="6 4"/><rect x="30" y="48" width="340" height="58" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="200" y="68" text-anchor="middle" font-size="13">datom text</text><text x="200" y="92" text-anchor="middle" font-family="monospace" font-size="13">Simple.{ Voice «which locks are held» }</text><line x1="200" y1="106" x2="200" y2="130" stroke="#8a9792" stroke-width="2" marker-end="url(#m2)"/><text x="212" y="124" font-size="13">actualize</text><rect x="30" y="132" width="340" height="58" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="200" y="156" text-anchor="middle" font-weight="600">datom-codec</text><text x="200" y="179" text-anchor="middle" font-size="13">protosize → datomize → compose</text><line x1="200" y1="190" x2="200" y2="250" stroke="#8a9792" stroke-width="2" marker-end="url(#m2)"/><text x="212" y="218" font-size="13">a composition, no text</text><rect x="30" y="252" width="340" height="56" rx="6" fill="#7b6be0" fill-opacity=".18" stroke="#7b6be0"/><text x="200" y="276" text-anchor="middle" font-weight="600">typed signal</text><text x="200" y="297" text-anchor="middle" font-family="monospace" font-size="13">Query Ask.Asking</text><line x1="200" y1="308" x2="200" y2="334" stroke="#8a9792" stroke-width="2" marker-end="url(#m2)"/><rect x="8" y="336" width="464" height="74" rx="10" fill="#d08a1e" fill-opacity=".14" stroke="#d08a1e"/><text x="200" y="364" text-anchor="middle" font-weight="600">Nexus, built without datom-codec</text><text x="200" y="390" text-anchor="middle" font-size="13">answers in signal</text><path d="M430,336 V77 H374" fill="none" stroke="#8a9792" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#m2)"/><text x="452" y="206" font-size="13" text-anchor="middle" transform="rotate(-90 452 206)">answer: signal, then textualize</text>
</svg>

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
<svg viewBox="0 0 480 350" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><text x="115" y="24" text-anchor="middle" font-size="13">everyday CLI call</text><text x="365" y="24" text-anchor="middle" font-size="13">debugging, component to component</text><rect x="10" y="34" width="210" height="154" rx="10" fill="#1f9e89" fill-opacity=".12" stroke="#1f9e89" stroke-width="2"/><text x="115" y="58" text-anchor="middle" font-weight="600" font-family="monospace">Simple.{ }</text><rect x="25" y="70" width="180" height="30" rx="5" fill="none" stroke="#8a9792" stroke-dasharray="4 3"/><text x="115" y="90" text-anchor="middle" font-size="13" fill-opacity=".6">no flow id</text><rect x="25" y="108" width="180" height="30" rx="5" fill="#1f9e89" fill-opacity=".22"/><text x="115" y="128" text-anchor="middle" font-family="monospace" font-size="14">Role</text><rect x="25" y="146" width="180" height="30" rx="5" fill="#1f9e89" fill-opacity=".22"/><text x="115" y="166" text-anchor="middle" font-family="monospace" font-size="14">Question</text><rect x="260" y="34" width="210" height="154" rx="10" fill="#7b6be0" fill-opacity=".12" stroke="#7b6be0" stroke-width="2"/><text x="365" y="58" text-anchor="middle" font-weight="600" font-family="monospace">Extended.{ }</text><rect x="275" y="70" width="180" height="30" rx="5" fill="#7b6be0" fill-opacity=".3"/><text x="365" y="90" text-anchor="middle" font-family="monospace" font-size="14">FlowId</text><rect x="275" y="108" width="180" height="30" rx="5" fill="#7b6be0" fill-opacity=".22"/><text x="365" y="128" text-anchor="middle" font-family="monospace" font-size="14">Role</text><rect x="275" y="146" width="180" height="30" rx="5" fill="#7b6be0" fill-opacity=".22"/><text x="365" y="166" text-anchor="middle" font-family="monospace" font-size="14">Question</text><line x1="115" y1="188" x2="210" y2="226" stroke="#8a9792" stroke-width="2" marker-end="url(#m3)"/><line x1="365" y1="188" x2="270" y2="226" stroke="#8a9792" stroke-width="2" marker-end="url(#m3)"/><rect x="120" y="228" width="240" height="40" rx="6" fill="#8a9792" fill-opacity=".15" stroke="#8a9792"/><text x="240" y="254" text-anchor="middle">Asking: one type</text><line x1="240" y1="268" x2="240" y2="296" stroke="#8a9792" stroke-width="2" marker-end="url(#m3)"/><rect x="120" y="298" width="240" height="40" rx="6" fill="#d08a1e" fill-opacity=".14" stroke="#d08a1e"/><text x="240" y="324" text-anchor="middle" font-family="monospace" font-size="14">Query Ask.Asking → Nexus</text>
</svg>

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
<svg viewBox="0 0 480 270" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><text x="14" y="22" font-weight="600">CLI side: the renderings</text><rect x="5" y="30" width="470" height="122" rx="10" fill="#1f9e89" fill-opacity=".07" stroke="#1f9e89" stroke-dasharray="6 4"/><rect x="15" y="50" width="125" height="58" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="77" y="74" text-anchor="middle" font-size="13">hex, today</text><text x="77" y="96" text-anchor="middle" font-family="monospace">6329f1</text><rect x="177" y="50" width="126" height="58" rx="6" fill="#7b6be0" fill-opacity=".2" stroke="#7b6be0" stroke-width="2"/><text x="240" y="74" text-anchor="middle" font-family="monospace" font-weight="600">FlowId</text><text x="240" y="96" text-anchor="middle" font-size="13">a number</text><rect x="340" y="50" width="125" height="58" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="402" y="74" text-anchor="middle" font-size="13">later</text><text x="402" y="96" text-anchor="middle">three words</text><line x1="175" y1="70" x2="143" y2="70" stroke="#8a9792" stroke-width="2" marker-end="url(#m6)"/><line x1="143" y1="90" x2="175" y2="90" stroke="#8a9792" stroke-width="2" marker-end="url(#m6)"/><line x1="305" y1="70" x2="337" y2="70" stroke="#8a9792" stroke-width="2" marker-end="url(#m6)"/><line x1="337" y1="90" x2="305" y2="90" stroke="#8a9792" stroke-width="2" marker-end="url(#m6)"/><text x="77" y="136" text-anchor="middle" font-size="13">render ⇄ read</text><text x="402" y="136" text-anchor="middle" font-size="13">render ⇄ read</text><line x1="240" y1="108" x2="240" y2="200" stroke="#7b6be0" stroke-width="3" marker-end="url(#m6)"/><text x="252" y="182" font-size="13">signal carries the number</text><rect x="90" y="202" width="300" height="58" rx="8" fill="#d08a1e" fill-opacity=".14" stroke="#d08a1e"/><text x="240" y="226" text-anchor="middle" font-weight="600">Nexus</text><text x="240" y="248" text-anchor="middle" font-size="13">stores · keys · compares the number</text>
</svg>

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
<svg viewBox="0 0 480 250" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><rect x="90" y="10" width="300" height="42" rx="6" fill="#7b6be0" fill-opacity=".16" stroke="#7b6be0"/><text x="240" y="37" text-anchor="middle" font-family="monospace">FlowId.{ Integer }</text><line x1="240" y1="52" x2="240" y2="86" stroke="#8a9792" stroke-width="2" marker-end="url(#m7)"/><text x="252" y="75" font-size="13">ethos-zero 16.0.0</text><rect x="40" y="88" width="400" height="42" rx="6" fill="#7b6be0" fill-opacity=".16" stroke="#7b6be0"/><text x="240" y="115" text-anchor="middle" font-family="monospace" font-size="14">pub struct FlowId { pub integer: i64 }</text><line x1="200" y1="130" x2="150" y2="180" stroke="#8a9792" stroke-width="2" marker-end="url(#m7)"/><text x="160" y="152" font-size="13" text-anchor="end">datom-codec 0.32.2</text><line x1="280" y1="130" x2="330" y2="180" stroke="#8a9792" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#m7)"/><text x="318" y="152" font-size="13">by hand</text><rect x="15" y="182" width="210" height="58" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="120" y="205" text-anchor="middle" font-size="13">generated, measured</text><text x="120" y="228" text-anchor="middle" font-family="monospace">{ 12232711 }</text><rect x="255" y="182" width="210" height="58" rx="6" fill="none" stroke="#d08a1e" stroke-dasharray="6 4"/><text x="360" y="205" text-anchor="middle" font-size="13">hex · three words</text><text x="360" y="228" text-anchor="middle" font-size="13">a CLI-crate impl</text>
</svg>

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
<svg viewBox="0 0 480 200" width="700" style="max-width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="15" fill="currentColor">
<defs><marker id="m9" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a9792"/></marker></defs><rect x="90" y="10" width="300" height="42" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="240" y="37" text-anchor="middle" font-family="monospace">Presentation.{ «Datom» }</text><line x1="240" y1="52" x2="240" y2="76" stroke="#8a9792" stroke-width="2" marker-end="url(#m9)"/><text x="252" y="69" font-size="13">read</text><rect x="60" y="78" width="360" height="42" rx="6" fill="#7b6be0" fill-opacity=".18" stroke="#7b6be0"/><text x="240" y="105" text-anchor="middle" font-family="monospace" font-size="14">Block::Presentation, title Datom</text><line x1="240" y1="120" x2="240" y2="144" stroke="#8a9792" stroke-width="2" marker-end="url(#m9)"/><text x="252" y="137" font-size="13">canonical print</text><rect x="90" y="146" width="300" height="42" rx="6" fill="#1f9e89" fill-opacity=".16" stroke="#1f9e89"/><text x="240" y="173" text-anchor="middle" font-family="monospace">Presentation.{ Datom }</text>
</svg>

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
