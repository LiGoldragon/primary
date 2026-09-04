# Remember: Flow 1c282d

Remembered by subflow of 6329f1.
Session: `1c282d6a-11a9-47b8-be36-ed358293569e`
Session transcript: `/home/li/.claude/projects/-home-li-primary/1c282d6a-11a9-47b8-be36-ed358293569e.jsonl` (237 lines)

## Summary

Flow 1c282d was a realization flow that gathered all psyche vision on
ethos, datom, and protos, synthesized a unified architecture, received
three rulings from the living, and then received an instruction to
execute a deep refactor/rewrite. The model never responded to that
final instruction -- the session ended (bridge-session) immediately
after the living's "go at it" message. No code was written by this
flow; its output is a vision synthesis and three psyche records.

---

## 1. Psyche Records

### 1.1 flows/1c282d/vision/protosizable.md

Source path: `/home/li/primary/flows/1c282d/vision/protosizable.md`

Verbatim:

```
# Protosizable

## The form is protos; the kind is Protosizable

> ethos isnt datom-expressible. the form is protos. I think protosic is the right kind. `type.protosize() -> protoform` - does that make sense. flesh the fuck out of that for me, with the ethos spec of it all and ascii visuals

— psyche, typed.

> protosizable!

— psyche, typed. (Correcting the kind name from "protosic" to "protosizable".)

## The association: Concept bears Protosizable

> ethos:Concept.[ Protosizable]

— psyche, typed. (The ethos Concept type bears the Protosizable kind.)

## Structure is really Protoform

> looks like Structure is really Protoform.

— psyche, typed. (The type currently called Structure/Portion in protos — Headed/Enclosed/Bare — is a Protoform. Not a separate type alongside it.)
```

### 1.2 flows/1c282d/vision/vocabulary.md

Source path: `/home/li/primary/flows/1c282d/vision/vocabulary.md`

Verbatim:

```
# Vocabulary

## Potential replaces Prospective

> potential

— psyche, typed. (Answering: Prospective vs. Potential — which stands?)

## Structure replaces Portion

> structure

— psyche, typed. (Answering: Portion vs. Structure — should it become Structure?)
```

### 1.3 Notion files

The flow's `notion/` directory exists but is empty. No notion records were created.

---

## 2. Log

Flow 1c282d has no log file (`log.md` or equivalent). There is no index entry for it in `/home/li/primary/flows/index.md`. The only index reference is in the 6329f1 entry (line 162), which references it as a predecessor to remember.

Flow 444e5e's log references 1c282d with a single sentence:

> Fixed Claude flow-ID initialization after session 1c282d followed a Codex-only generated instruction: Curriculum now renders harness-specific commands, Primary pins and deploys the corrected sources, and the installed behavior is independently verified.

This is the complete content of `/home/li/primary/flows/444e5e/log.md`.

---

## 3. Reports and Evidence

Flow 1c282d produced no reports or evidence files. Its `flows/1c282d/` directory contains only the `vision/` and `notion/` subdirectories. The vision synthesis and Protosizable design were delivered as model responses within the session, not written to files.

The vision synthesis is a design document about datom, ethos, ethos-zero, protos, and orchestrate. It is included verbatim below (from session transcript line 179, assistant message):

### 3.1 Vision Synthesis (verbatim, from session line 179)

```
All four subflows are back. Let me synthesize and present the unified vision.

---

## The Architecture: Three Programs, Four Layers, Two Dialects

### The Three Programs

**protos** (library, zero-dependency) — the universal structural substrate. The sole character reader and writer. Knows nothing about meaning — only the anatomy of text: heads, separators, delimiters, enclosed regions. All dialects ride it.

**datomic** (library, depends on protos) — datom serialization/deserialization. Maps between protos portions and typed Rust values. Positional, schema-driven, no field names.

**ethos-zero** (nexus/executable, depends on protos + datomic) — reads ethos files through protos, matches the anatomy to ethos concept types, emits Rust source. Version zero: the monolith that goes straight from ethos to Rust, bootstrapping toward the eventual three-nexus stack (ethos/nomos/logos).

---

### The Four Layers

Each layer takes a prospective input and yields a more concrete output. The capability to descend lives on the layer above. Embody is the general word for reaching the layer below.

Text  ──delineate──▶  Structure  ──conceive──▶  Concept  ──incorporate──▶  Corporal

**1. Text** — `Text<T>`: normalized string (non-structural whitespace removed) with content hash and phantom target type. Incoming text is prospective — untrusted until it matches its anatomy.

**2. Structure** — `Delineation` = a vector of structures (the vision word for what the current code calls `Portion`). Pure protos anatomy: Headed (head + separator + body), Enclosed (structural or opaque boundaries), Bare (symbol). No interpretation. "Protos is only about structure; it wouldn't know what anything is."

**3. Concept** — the dialect's abstract objects. For datom: "the first pass of a datom yields the concept of an enum, not the Rust type — it'll be a vector representing 'this is an enum, a variant with name X and payload of such and such.'" For ethos: TypeDeclaration, KindDeclaration, Capability, Association. "The concept layer is the Datom and Ethos types of the settled chain." The layer enum is Concept, singular.

**4. Corporal** — the final form. For datom: the Rust value itself (`Record(text, 42)`, `Vec<Integer>`, `BTreeMap<K,V>`). For ethos: generated Rust code — "Ethos also has a Corporal layer, from which the generated Rust is yielded."

### How Protos Fits

Protos owns layers 1→2 entirely. Its types:

| Type | Role |
|------|------|
| `Text<T>` | Normalized text + content hash + phantom target |
| Structure (currently `Portion`) | Headed / Enclosed / Bare |
| Headed | Symbol head + Separator + body structure |
| Enclosed | Structural (Braced/Bracketed/Guillemets/Angled) or Opaque (CurlyQuote/Parentheses) |
| Bare | Symbol |
| Delineation | `Vec<Structure>` |
| Symbol | A qualified string |
| Separator | Period (`.`) / Exclamation (`!`) / Colon (`:`) |

Six delimiter pairs: `{ }`, `[ ]`, `« »`, `< >`, `" "` (curly quotes), `( )` (parentheses). Three separators.

The context-switching parse (from Intent/protosParsing.md):

> Protos parsing always happens inside a context, and only the current context gives shapes their meaning: it defines which shapes can appear next and which shape completes it. A met shape announces a type, and that type's context takes over completely until its completing shape; then the parent context resumes exactly where it left off. Reading and writing are one walk in two directions.

The walk is a stack: each frame keeps the parent context's position. When a delimiter opens, a child context takes over completely. When it closes, the parent resumes.

### Direction Asymmetry (settled, distilled)

- **Realize** (in): text → typed values. May fault. Spans found on the way in.
- **Textualize** (out): typed values → text. Cannot fault. Spans computed on the way out.
- Each direction is several passes.

---

## Datom Syntax → Rust Types

### Primitives

| Datom text | Expected Rust type | Notes |
|------------|-------------------|-------|
| `42` | `i64` | Bare decimal |
| `-42` | `i64` | Negative bare decimal |
| `0` | `i64` | Zero |
| `true` / `false` | `bool` | |
| `〝hello world〞` | `DatomicString` | Curly quotes are the string delimiter |
| `hello` (bare word) | `DatomicString` | In string position, bare when no space/delimiter needed |

### Compound structures

| Datom text | Rust type | Rule |
|------------|-----------|------|
| `{ a b c }` | `SomeStruct(a, b, c)` | Brace = struct. Positional, no field names. |
| `[ a b c ]` | `Vec<T>` | Bracket = vector. All elements share a type. |
| `« k1 v1 k2 v2 »` | `BTreeMap<K,V>` | Guillemets = map. Key and value separated by space. |
| `Head.{ a b }` | `Enum::Head(Inner(a, b))` | Head + dot + braces = variant carrying struct |
| `Head.[ a b ]` | `Enum::Head(vec![a, b])` | Head + dot + brackets = variant carrying vector |
| `Head` | `Enum::Head` | Bare = unit variant |

### Governing principles

- **Schema-driven and positional**: the reader walks the expected type. The text carries only data. All naming and self-description live in the type.
- A datom is not preceded by a "Datom" root — the type is known from context.
- A head is always a variant, so capitalized.
- Canonical text leaves a space inside every bracket and brace delimiter.
- Semicolon opens a comment.
- Parentheses reserved for Meaning (the structured string — deferred).
- Colon remains legal in a position expecting a string.
- A map in expected position carries no Map head.

### Example: a Nexus reply

Given ethos-declared types, a reply looks like:
```
Observed.Locks.[]
```
"Only what carries data is written."

---

## Ethos Syntax → Rust

### The Canonical Example (from distilled Vision/ethos.md)

**Ethos:**
```
Library.{
  {0 1 0}
  [ protos:[Text Textualizable] ]                             ; imports
  [ Record.{ Text Integer }                                   ; types
    Report.{ Text Vector<Integer> } ]
  [ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; kinds
  [ Report.[ Textualizable ] ]                                ; associations
}
```

**Target Rust:**
```rust
struct Record(Text, Integer);
struct Report(Text, Vec<Integer>);

// The kind's identity: name + constraints.
// Ethos writes the bounds alone; Rust needs named parameters.
trait Processable<A: Clone + Send, B: Serialize> { /* … */ }

impl Textualizable for Report { /* … */ }
```

### File anatomy (from the psyche's handwritten page)

```
Signal.{0 2 0}                              ; root variant (species) + version
[ethos:[Registry ...]]                      ; imports
[Generate.{ Registry Target }]              ; request types
[Generated.{ Vector<RustFile> ... }
 GenerationFailure.[                        ; response types
   SyntaxError.Vector<FilePath>
   MissingImport.Vector<ImportName> ... ]]
```

The outer braces are always omitted in an ethos file. A file is one "sweet" ethos (the headed form with implied outer braces) or a full datom vector.

Layout: **Root.Version [Imports] [Types] [Kinds] [Associations]** — five sections, each a bracketed vector.

### Type declarations

| Ethos | Rust | Rule |
|-------|------|------|
| `Record.{ Text Integer }` | `struct Record(Text, Integer);` | Head + braces = struct (tuple struct, positional) |
| `Status.[ Active Inactive Pending ]` | `enum Status { Active, Inactive, Pending }` | Head + brackets = enum |
| `SyntaxError.Vector<FilePath>` | variant carrying data (inline) | A variant named as existing type = data-carrying |
| `SomeMap.« NameType ValueType »` | `BTreeMap<NameType, ValueType>` | Guillemets for map type |

Non-repetition: a variant named as an already-defined type triggers a data-carrying variant automatically. No `SyntaxError.SyntaxErrorData` redundancy.

### Kind (trait) declarations

A kind's identity is its name and its constraints — exactly what identifies a Rust trait. Angle brackets hold the constraints (a protos delimiter, recycled from Rust).

**Ethos:**
```
Processable<[Clonable Sendable] Serializable>.[
  process.{ Self }
  process!{ Self }
]
```

**Rust:**
```rust
trait Processable<A: Clone + Send, B: Serialize> {
    fn process(&self);       // period separator = &self
    fn process_mut(&mut self);  // exclamation separator = &mut self
}
```

- A constraint is a kind, or a bracket of kinds.
- `[Clonable Sendable]` = one generic parameter bounded by both `Clone + Send`.
- `Serializable` = a second parameter bounded by `Serialize`.
- Two heads that differ in a constraint are two different kinds.
- In ethos there are no generics, only kinds.
- What else a kind declares — superkinds, associated types and constants, capabilities — is its definition, not its identity.

### Separator meanings in capabilities

| Separator | Rust receiver | Example |
|-----------|--------------|---------|
| `.` period | `&self` | `process.{ Self }` → `fn process(&self)` |
| `!` exclamation | `&mut self` | `process!{ Self }` → `fn process_mut(&mut self)` |

Yields always in `[]`.

### Associations (impl blocks)

**Ethos:**
```
[ Report.[ Textualizable ] ]
```

**Rust:**
```rust
impl Textualizable for Report { /* … */ }
```

"Interactions" is the psyche's term for these.

### Compile-time checks the generated Rust carries

1. **Every method under a trait** — "traits are the comprehension surface." No freestanding implementations. No free functions.

2. **Kind constraints** — `Processable<[Clonable Sendable] Serializable>` compiles to `trait Processable<A: Clone + Send, B: Serialize>`. Rust's type system enforces the bounds.

3. **Positional tuple structs** — field order enforced by position.

4. **`impl Datomic` generated for every type** — every ethos-declared type gets datom serialization/deserialization generated, ensuring it can cross the text boundary.

5. **Exhaustive enum matching** — Rust enforces all variants handled.

6. **Fully qualified names** — "Rust as an assembly language, explicit, correct over sweet."

7. **No freestanding implementations** — every `impl` block is for a trait. "Freestanding implementations are forbidden."

8. **Associated constants in each kind hold its forms** — "the check is at compilation, not generation."

---

## The Parsing Pipeline in Both Dialects

### Datom reading (text → Rust value)

```
"Head.{ 42 〝hello〞 }"       Text<Datom>
        │
        ▼ protos delineate
Headed("Head", Period,       Structure (Vec<Structure>)
  Enclosed(Braced, [
    Bare("42"),
    Enclosed(CurlyQuote, "hello")
  ]))
        │
        ▼ datomic: conceive + incorporate (currently one step, vision says two)
Enum::Head(Inner(42, "hello"))   Corporal Rust value
```

The conceptual layer exists even for datom ("the concept of an enum"), though the current datomic crate collapses concept → corporal into one step. Vision says it should be separated.

### Ethos reading (text → Rust source)

```
"Library.{ ... }"            Text<Ethos>
        │
        ▼ protos delineate
Headed("Library", Period,    Structure (Vec<Structure>)
  Enclosed(Braced, [
    Enclosed(Braced, [...]),   ; version
    Enclosed(Bracketed, [...]),; imports
    Enclosed(Bracketed, [...]),; types
    Enclosed(Bracketed, [...]),; kinds
    Enclosed(Bracketed, [...]) ; associations
  ]))
        │
        ▼ ethos conceive
File::Interface {            Concept (Ethos types)
  version: (0, 1, 0),
  imports: [...],
  types: [TypeDecl::Struct("Record", [...]), ...],
  kinds: [KindDecl { name: "Processable", constraints: [...], ... }],
  associations: [Assoc("Report", ["Textualizable"])]
}
        │
        ▼ ethos incorporate (RustEmitter)
syn::File { ... }            Corporal (Rust AST → formatted source)
```

### Textualization (reverse — cannot fault)

```
Rust value  ──datomic textualize──▶  structures  ──protos print──▶  canonical text
Ethos concepts  ──ethos textualize──▶  structures  ──protos print──▶  canonical ethos text
```

---

## The Kind System Vocabulary

| Ethos term | Rust equivalent | Source |
|------------|----------------|--------|
| Kind | Trait | distilled Vision/ethos.md |
| Capability | Method on a trait | distilled |
| Self | `Self` | recycled from Rust |
| Result | `Result` | recycled from Rust |
| Interaction | `impl` block | flow aa4c7747 |
| Constraint | Generic parameter with bounds | distilled |
| Association | `impl Kind for Type` | distilled |
| Source | Crate | flow 2b34fafa |

### Layer-specific kinds (from flow 62022e8f, confirmed with "yes")

| Transition | Kind | Capability |
|-----------|------|-----------|
| Text → Structure | Structural / Delineatable | delineate |
| Structure → Concept | Conceptual | conceive |
| Concept → Corporal | Corporal | incorporate |

"Each layer kind is an alias of a Potential." "Incorporate is the corporal capability; embody is the general word for reaching the layer below."

### Naming rules (settled)

- Kinds are qualifier-named: Runnable, Textualizable, Structural, Embodied. *Run* is not a kind.
- Verbs Rust imposes (Write, Read) tolerated as legacy, removed once ethos is the authored language.
- No generics in ethos, only kinds.
- A kind declaration's position holds a kind, never a type.

---

## Open Questions Needing Your Word

Three points where the vision forks and I don't know which way you want to go:

**1. Prospective vs. Potential** — Flow 62022e8f proposed switching `Prospective` to `Potential` and the layer verb from `prospect` to `actualize`. The distilled Vision/protos.md still says "prospective." The current code uses `Prospective<T>`. Which stands?

**2. Portion vs. Structure** — Vision/datom.md says "Structure is the word for every unit." Flow e8c4cc61 says "Structure is a better Portion." The current protos crate uses `Portion` as the enum name. Should it become `Structure`?

**3. The default datom kind name** — A kind borne by all ethos types by default that describes their datom-textual structure. "Datomizable" was raised from notion to vision, but later "Datomizable narrows too explicitly to datom" — alternatives floated: ProtoShaped, ProtoFormed, protoform, protosic, protoformal. None settled.
```

### 3.2 Protosizable Design (verbatim, from session line 218)

This was the model's response after the living answered the three open questions. It is a design document for the Protosizable kind.

```
Vision logged. Now the flesh-out.

---

## Protosizable: The Structural Bridge Between Layers

### Where it sits

                              THE FOUR LAYERS
                              
  Text          Structure         Concept           Corporal
  ─────         ─────────         ───────           ────────
  Text<T>       Vec<Structure>    Concept enum      Rust value / Rust AST
                                       │
                                       │ protosize()
                                       ▼
                                  Protoform
                                  ─────────
                                  "here is what I
                                   look like as
                                   structures"

Protoform is the contract between layers 2 and 3. It tells the parser what structures to expect for a concept, and tells the serializer what structures to emit.

                READING (Realize)                    WRITING (Textualize)

  Text<T>                                           Concept
    │                                                  │
    │ delineate                                        │ protosize()
    ▼                                                  ▼
  Vec<Structure>                                    Protoform
    │                                                  │
    │              ┌──────────┐                        │ build structures
    └──── match ──▶│Protoform │                        ▼
                   └────┬─────┘                     Vec<Structure>
                        │                              │
                        │ conceive                     │ print
                        ▼                              ▼
                     Concept                         Text<T>
                        │
                        │ incorporate
                        ▼
                     Corporal

On the way **in**: delineate the text, then match the resulting structures against the concept's Protoform — if they match, conceive the concept; if they don't, fault.

On the way **out**: the concept knows its Protoform, builds the corresponding structures, protos prints them.

---

### The Protoform type (proposed ethos spec)

Protoform.[                                        ; protos structural pattern
  Bare                                             ; leaf: a scalar value (text, integer, boolean)
  Enclosed.{ StructuralEnclosure Inner }           ; delimited region: { }, [ ], « », < >
  Headed.{ Symbol Separator Protoform }            ; head.separator body
]

Inner.[                                            ; what's inside an enclosure
  Sequence.Vector<Protoform>                       ; fixed ordered fields       (struct)
  Homogeneous.Protoform                            ; variable same-form elements (vector)
  Paired.{ Protoform Protoform }                   ; key-value pairs            (map)
  Alternation.Vector<Protoform>                    ; one of these               (enum variants)
]

Target Rust:

enum Protoform {
    Bare,
    Enclosed(StructuralEnclosure, Inner),
    Headed(Symbol, Separator, Box<Protoform>),
}

enum Inner {
    Sequence(Vec<Protoform>),
    Homogeneous(Box<Protoform>),
    Paired(Box<Protoform>, Box<Protoform>),
    Alternation(Vec<Protoform>),
}

---

### The Protosizable kind (proposed ethos spec)

Protosizable.[
  protosize.[ Protoform ]                          ; yields the structural form of this concept
]

Target Rust:

trait Protosizable {
    fn protosize(&self) -> Protoform;
}

The association:

[ ethos:Concept.[ Protosizable ] ]                 ; Concept bears Protosizable

Target Rust:

impl Protosizable for Concept { /* … */ }

This means every variant of the ethos Concept enum can describe its structural anatomy.

---

### Concrete examples: what protosize() returns

**1. `Record.{ Text Integer }` — a struct**

Record.protosize() ──▶  Enclosed(Braced, Sequence([Bare, Bare]))

Meaning: "I am a braced enclosure containing two bare values in order."

In datom text (when the type is known from context):
{ 〝Moby Dick〞 1851 }

Matched against:
Enclosed ──── Braced
                 │
          Sequence([Bare, Bare])
                 │       │
              〝Moby..〞  1851     ✓ matches

As an enum variant in datom (headed form):
Record.{ 〝Moby Dick〞 1851 }

Matched against:
Headed("Record", Period, Enclosed(Braced, Sequence([Bare, Bare])))

---

**2. `Status.[ Active Inactive Pending ]` — an enum of bare variants**

Status.protosize() ──▶  Enclosed(Bracketed, Alternation([
                          Headed("Active",    Period, Bare),
                          Headed("Inactive",  Period, Bare),
                          Headed("Pending",   Period, Bare),
                        ]))

In datom text:
Active

The parser sees a bare symbol, checks the Alternation — `Active` matches the first branch.

---

**3. `Vector<Integer>` — a vector**

Vector<Integer>.protosize() ──▶  Enclosed(Bracketed, Homogeneous(Bare))

In datom text:
[ 1 2 3 42 ]

Matched against:
Enclosed ──── Bracketed
                 │
          Homogeneous(Bare)
                 │
              1, 2, 3, 42    ✓ each element is Bare

---

**4. `BTreeMap<Text, Integer>` — a map**

SomeMap.protosize() ──▶  Enclosed(Guillemets, Paired(Bare, Bare))

In datom text:
« name 42 title 7 »

Matched against:
Enclosed ──── Guillemets
                 │
          Paired(Bare, Bare)
                 │
              name→42, title→7    ✓ each pair is Bare+Bare

---

**5. A data-carrying enum variant: `GenerationFailure`**

GenerationFailure.[
  SyntaxError.Vector<FilePath>
  MissingImport.Vector<ImportName>
]

GenerationFailure.protosize() ──▶  Enclosed(Bracketed, Alternation([
  Headed("SyntaxError",   Period, Enclosed(Bracketed, Homogeneous(Bare))),
  Headed("MissingImport", Period, Enclosed(Bracketed, Homogeneous(Bare))),
]))

In datom text:
SyntaxError.[ 〝main.es〞 〝lib.es〞 ]

Matched against:
Headed ──── "SyntaxError"
               │
        Enclosed(Bracketed, Homogeneous(Bare))
               │
            〝main.es〞, 〝lib.es〞    ✓

---

### The full parsing pipeline with Protoform

Reading a datom `Record.{ 〝hello〞 42 }` when the expected type is an enum with a Record variant:

          ┌─────────────────────────────────────────────────────────┐
  TEXT    │  Record.{ 〝hello〞 42 }                                 │
          └───────────────┬─────────────────────────────────────────┘
                          │
                    delineate (protos)
                          │
          ┌───────────────▼─────────────────────────────────────────┐
  STRUCT  │  Headed("Record", Period,                               │
          │    Enclosed(Braced, [                                    │
          │      Enclosed(CurlyQuote, "hello"),                      │
          │      Bare("42")                                         │
          │    ]))                                                   │
          └───────────────┬─────────────────────────────────────────┘
                          │
         conceive: which variant? ◄─── Outer.protosize() says
                          │            Alternation with "Record" branch
                          │
                   match head "Record"
                          │
         conceive body  ◄─── Record.protosize() says
                          │   Enclosed(Braced, Sequence([Bare, Bare]))
                          │
          ┌───────────────▼─────────────────────────────────────────┐
  CONCEPT │  Concept::Struct {                                      │
          │    name: "Record",                                      │
          │    fields: [Concept::Scalar("hello"), Concept::Scalar(42)]│
          │  }                                                      │
          └───────────────┬─────────────────────────────────────────┘
                          │
                    incorporate
                          │
          ┌───────────────▼─────────────────────────────────────────┐
  CORPORAL│  Record(DatomicString("hello"), 42_i64)                 │
          └─────────────────────────────────────────────────────────┘

---

### For ethos reading (same pipeline, different concepts)

Reading `Library.{ {0 1 0} [ protos:[Text] ] [ Record.{ Text Integer } ] ... }`:

  TEXT     ──delineate──▶  STRUCTURE  ──conceive──▶        CONCEPT              ──incorporate──▶  CORPORAL
                                            │
                                   Library.protosize()
                                   says: Braced, Sequence of
                                   [version, imports, types,
                                    kinds, associations]
                                            │
                                            ▼
                                   File::Interface {         ──▶  syn::File {
                                     version: (0,1,0),              struct Record(Text, i64);
                                     imports: [...],                 trait ...;
                                     types: [Record, ...],           impl ...;
                                     kinds: [...],                 }
                                     associations: [...]           then: formatted Rust source
                                   }

---

### Open fork: protosize as capability or associated constant?

The psyche wrote `type.protosize() -> Protoform` — a function call. But earlier vision also said "an associated constant in each kind holds its forms."

Two shapes:

**A. Capability (function)** — `protosize.[ Protoform ]`
trait Protosizable {
    fn protosize(&self) -> Protoform;
}
Each concept instance computes its protoform. Could vary per instance (e.g., different arity forms of the same concept).

**B. Associated constant** — `PROTOFORM: Protoform`
trait Protosizable {
    const PROTOFORM: Protoform;
}
Each *type* has one fixed protoform. Simpler, static, known at compile time.

A multi-form concept (same concept at different arities) favors **A**. A fixed-shape type favors **B**. Which way?
```

### 3.3 Protoform collapse (verbatim, from session line 226)

This is the model's response after the living said "looks like Structure is really Protoform."

```
That collapses the model significantly. What the current code calls `Portion` (Headed / Enclosed / Bare) — the thing protos delineates text into — that IS a Protoform. There's no separate "structural description" type alongside it. The protoform is the structure.

So the pipeline is simpler than I proposed:

  Text<T>  ──delineate──▶  Protoform        ──conceive──▶  Concept  ──incorporate──▶  Corporal
                           (Headed/Enclosed/Bare)
                                ▲
                                │
                           and a Concept
                           bears Protosizable,
                           so it can yield
                           its own Protoform back

Which means:
- `protosize()` on a Concept returns a `Protoform` — the same type protos already produces from text
- Matching incoming text means: delineate → get a Protoform → does it match what the expected concept's protosize says?
- Textualizing means: the concept yields its Protoform → protos prints it

The Protoform type in protos right now (currently called `Portion`):

Protoform.[
  Headed.{ Symbol Separator Protoform }
  Enclosed.{ StructuralEnclosure Vector<Protoform> }
  Bare.Symbol
]

That's already defined. The rename from Portion to Protoform is the main change. And the `Inner` / `Sequence` / `Homogeneous` / `Alternation` distinctions I proposed are not separate types — they're just how a Concept interprets a `Vector<Protoform>` inside an enclosure. The structure itself doesn't know whether it's a struct or a vector; that's the Concept layer's job.

This means the Protosizable kind and its capability are the *only* new things:

Protosizable.[
  protosize.[ Protoform ]
]

trait Protosizable {
    fn protosize(&self) -> Protoform;
}

And the Concept layer's conceive step is: match a Protoform (from text) against a Protoform (from protosize), and if they correspond structurally, build the Concept.

Does this read right, or am I overcollapsing? The distinction between "the protoform that came from text" and "the protoform that the concept declares" is the same type — one is concrete (has actual values in its symbols and enclosures) and the other is... also concrete? Or is the protosize output more like a pattern/template?

That's the fork: is the protosize output a *concrete Protoform with placeholder values*, or is it structurally identical to what came from text, just without the actual data?
```

---

## 4. Last Model Response

The last model response is the Protoform collapse at session line 226, reproduced verbatim in section 3.3 above.

The model raised a final open question about whether `protosize()` returns a concrete Protoform or a pattern/template, but the living did not answer. Instead, the living's next message (line 229) was the implementation instruction.

The living's final message (session line 229, verbatim):

> thats good. go at it. do a deep refactor/rewrite of datom and ethos-zero. test with a branch of orchestrate. right now orchestrate replies are *absolutely not* datom, which is ridiculous. regenerate its ethos and make its cli's actually speak datom. im going to bed, so if youre unsure, mine for more recent psyche and make a judgment call. work well. use critical writers to implement. take your time. dont stop for decisions, just give me a new version of all the components involved (protos, ethos, datom, orchestrate) on an epic multi repo branch-train. I want to get up to a new POC stack with orchestrate as the MVP.

The model never responded to this instruction. The session was bridged (bridge-session record at line 232, `bridgeSessionId: cse_01C2xziUNfKL8PDCwg9Zngru`). Total session cost: $9.38 (Opus 4.6 1M).

---

## 5. Witnessed State of Touched Repositories

Witnessed on 2026-09-04 by git commands. These are the repositories the flow's vision synthesis discussed; the flow wrote no code to any of them.

### 5.1 datomic (symlink datom -> datomic)

- Path: `/git/github.com/LiGoldragon/datomic`
- Branch: Detached HEAD at main (`8b17abc`)
- HEAD == main: YES
- Dirty: Clean
- Recent commits on main:
  ```
  8b17abc Release Datomic map layout correction
  8e194c6 Complete Datomic map-owned private layouts
  4baeaac Pin Datomic to complete Protos contract
  fae7f3e State complete Datomic declaration contract in Ethos
  6f0354d Normalize map declarations for Portion grammar
  ```
- Other branches: `epic-datom-path-locks-20260822`

### 5.2 ethos-zero

- Path: `/git/github.com/LiGoldragon/ethos-zero`
- Branch: Detached HEAD at `b0830fb` (NOT main)
- HEAD == main: NO
- HEAD commit: `b0830fb Prove complete map-owned Rust contracts`
- Dirty: Clean
- HEAD is an ancestor of main; main has 14 commits ahead of HEAD:
  ```
  b922afb Derive value semantics for data-only unit enums
  60dd93a Emit data-only Datomic schema libraries
  9f652df Add named Ethos record field emission
  060cc7a Order Nexus subscription activation before stream events
  a0850a8 Complete Nexus socket and containment hardening 0.7.1
  2d25c65 Harden Nexus runtime boundaries
  2309e5b Run Ethos-zero as a durable Nexus workspace
  f043fc4 Project WireContract roots through Datomic
  ec9db03 Emit WireContract refusal and event frame roots
  a0e21ed Harden WireContract emission invariants
  0836a1f Emit WireContract signal modules
  30e5ef6 Emit structural map-owned schema defaults
  dd5283a Prove real pinned Orchestrate interfaces
  a752943 Prove complete map-owned Rust contracts
  ```
- Other branches: `e3-bootstrap-wip-01a04a30`

### 5.3 protos

- Path: `/git/github.com/LiGoldragon/protos`
- Branch: Detached HEAD at main (`2f605fd`)
- HEAD == main: YES
- Dirty: Clean
- Recent commits on main:
  ```
  2f605fd State complete Protos declaration contract in Ethos
  589c039 Complete Protos E2 trait signatures
  caf468c Specify Protos E2 public-surface ownership
  f9eadcd Normalize map declarations for Portion grammar
  99cb6d9 Adopt headed Schema map root
  ```
- Other branches: `SpiritLineageBTrain`, `SpiritSourceIntegration`, `SpiritSourceIntegrationPreEncoded`, `SpiritV14Implementation`, `identifier-slicing-contracts`, `no-alias-migration`

### 5.4 orchestrate

- Path: `/git/github.com/LiGoldragon/orchestrate`
- Branch: Detached HEAD at `be5dfa2` (named branch ref: `HEAD detached from be5dfa2`)
- HEAD == main: YES (main is `e0f3bc5`, which is HEAD)
- Dirty: YES -- 4 modified files:
  ```
  ARCHITECTURE.md        |  4 +--
  README.md              |  3 +-
  src/bin/orchestrate.rs |  7 +++--
  tests/live_nexus.rs    | 76 ++++++++++++++++++++++++++++++++++++++++++++++++--
  ```
- Recent commits on main:
  ```
  e0f3bc5 Realize durable ordinary Lock Nexus
  6ced922 Close ordinary operations deployment task
  c66ff74 Record ordinary operations skill progress
  4cc55c0 Track ordinary Orchestrate operations skill
  7857a47 Close Orchestrate Nexus release epic
  ```
- Other branches (many): `LandTypedHumanTime`, `RegistryMaintenanceDeployment`, `RegistryRemovalIntegration`, `RegistryRemovalRuntime`, `RegistryRemovalRuntimeFinal`, `WorktreeSubjectIntegration`, `epic-datom-path-locks-20260822`, `interim-table-reaping`, `preserve/orchestrate-lane-suspect-recovery-20260720`, `realizer-three-stack-status`, `session-lane-claim-ownership`, `session-lane-meta-lifecycle`, `session-lane-observe-projections`, `session-lane-storage-migration`, `typed-human-readable-time`, `workflow-engine-thin-slice`

Note: The orchestrate dirty state was not created by flow 1c282d (which wrote no code). It is pre-existing uncommitted work from another flow.

---

## Sources

- Session transcript: `/home/li/.claude/projects/-home-li-primary/1c282d6a-11a9-47b8-be36-ed358293569e.jsonl`, lines 179, 206, 218, 223, 226, 229
- Psyche records: `/home/li/primary/flows/1c282d/vision/protosizable.md`, `/home/li/primary/flows/1c282d/vision/vocabulary.md`
- Flow 444e5e log: `/home/li/primary/flows/444e5e/log.md`
- Git witness: `git log`, `git status`, `git branch`, `git rev-parse` run on 2026-09-04 against repos under `/git/github.com/LiGoldragon/`
