# Noema — the anatomy of the meaning language

Fable b7ba00, Psyche, 2026-09-26. Written on the living's request, relayed by Psyche Opus 93ba9f, as the book on the dialect behind datom's parenthesised Meaning. Every rule is a proposal until the living rules; the living's words are quoted where they bind (verbatim in `flows/b7ba00/vision/meaningLanguage.md`); each open choice is marked **Fork**.

> This meaning type that we've been keeping for parentheses in datom is going to be really big. … Let's be broad first: let's break down language and maybe we can lay out a pretty good tree that has a certain number of enums and start using that language. … They would just be a bunch of data-carrying enums. You can end up with this chain of dots to express something and some of them have a parenthesis that opens another subnote.

## 0. What already stands, and where this book sits

The language has a home already: the `meaning-language` repository, whose ethos declares the Vaiśeṣika categories as roots (substance, the twenty-four qualities, motion, universal, particular, inherence, absence), a quality structure with typed coordinates, and the Pāṇinian **act** — root, stem formation, tense-mood, voice, person, number, agreement, and the six kāraka roles — with a content-addressed `Statement` and `Annotation`. That is the living's 2026-09-19 ruling built: Vaiśeṣika for the things, Pāṇini for the verbs.

What is missing is the level the living now names: what an utterance *is* — a statement, an inquiry, an order — before what it says. This book adds that level, names the language, and shows the syntax of chains and subnotes. The existing ethos is not replaced; it becomes the third of four layers.

| layer | what it types | source | state |
|---|---|---|---|
| Utterance | what kind of speech act this is | Nyāya, Mīmāṃsā (this book) | proposed |
| Act | who does what to whom, when, how | Pāṇini (`Act`, `Karaka`) | built |
| Category | what kinds of things and qualities exist | Vaiśeṣika (`Padartha`, `Quality`) | built |
| Annotation | a noema about a noema, content-addressed | the living, 09-19 (`Annotation`) | built |

## 1. The name

The language needs a name that is not a Sanskrit term and that reads as its own thing beside datom and ethos.

> the meaning language, which could have its own more poetic Latin or Greek name, is the specified language: the logical language, a little bit like Hanzi.

Proposed: **Noema** (Greek νόημα: what is meant, the thought as an object). A parenthesis in datom opens a noema; the plural is noemata; the root type is `Noema`. It is short, it is not a word already used in the system, and "the noema of this datom" reads plainly.

**Fork 1.** Alternatives with the same fitness: *Sententia* (Latin: meaning, judgment, sentence), *Logia* (Greek: sayings), *Sema* (Greek: sign). Proposed: Noema.

## 2. The root

> There's a root variant, so you can have a vector of these or a single of these, right? You have these two main types, which you could also give a name to.

```
Noema.[ One.Utterance Many.Vector<Utterance> ]
```

Everything inside a parenthesis is one `Noema`. A bare `( … )` in datom that the reader cannot parse is read by balance as an opaque string, as protos already rules; a reader that knows Noema parses it.

## 3. The tree — first broad cut

The living asked for breadth first: statement, inquiry, and the rest of what language does. The Indian traditions already cut this: Nyāya's five-membered argument (claim, reason, example, application, conclusion), Mīmāṃsā's classes of sentence (injunction, prohibition, explanation), and the plain pair question and answer. The English names are candidates; the Sanskrit sits in the table of equivalents (§7), never in the type.

```
Utterance.[ Statement.Statement Inquiry.Inquiry Injunction.Injunction Response.Response Annotation.Annotation ]

Statement.{ Content Support }                 ; something held true, with what it rests on
Support.Vector<Noema>                          ; the reasons: psyches, witnesses, prior statements
Inquiry.[ Question.Content Audit.Content Information.Content ]
Injunction.[ Order.Content Prohibition.Content ]
Response.[ Answer.{ Inquiry Content } Assent Refusal.Content ]
Annotation.{ AnnotationTarget AnnotationBody } ; as built: content-addressed target, prose or linked statement
```

`Content` is what an utterance says, at whatever depth the reader can type it:

```
Content.[ Prose.String Act.Act Noema.Noema ]
```

`Prose` is the bootstrap — the living's "Twitter style" opaque string; `Act` is the Pāṇinian act already built; `Noema` lets an utterance contain utterances (an order whose content is a statement to be relayed).

> For now, we'll keep those in prose, like Twitter style, as a limited number of words, a string, maybe, to fit the concept of an idea or a statement. We'll quickly move into a full set of verbs.

The letter books' four message kinds are now a subset of this tree, not a type of their own: an order is `Injunction.Order`, a question `Inquiry.Question`, an audit request `Inquiry.Audit`, an information request `Inquiry.Information`; a report is a `Statement`, an answer `Response.Answer`. A letter's `Kind` field dissolves: a letter carries a `Noema`.

**Fork 2.** Five top-level utterances, or three (Statement, Inquiry, Injunction) with Response folded into Statement and Annotation kept as the meta-layer? Proposed: five — a response is not a statement (it points at an inquiry), and an annotation is an utterance about a unit, so it belongs in the tree the reader walks.

**Fork 3.** `Support` on every statement, or only on a `Full` statement? Proposed: every statement carries its support; an empty vector is a bare claim, and the reader sees that it is bare.

## 4. Chains of dots

A chain of dotted heads is a path down the tree; the last head carries the data. Reading left to right is reading from the broadest category to the words.

```
Inquiry.Audit.Prose.«Did deployment 38 reach a terminal?»
Injunction.Order.Prose.«Regenerate the ouranos proposal against goldragon main.»
Response.Answer.{ Inquiry.Audit.Prose.«Did deployment 38 reach a terminal?» Prose.«No terminal; the row is orphaned.» }
Statement.{ Prose.«Deployment 38 replaced its own Nexus.» [ (…psyche…) (…witness…) ] }
```

This is ordinary datom: every head is a variant, the data follows. Nothing new is parsed; the tree is what makes the chain mean something.

## 5. The parenthesis — a subnote on a unit

> some of them have a parenthesis that opens another subnote, more information concerning this particular aspect of it, which can contain whatever. … because you escape by balancing the parentheses, when you start a meaning context delimiter, you can use all of the delimiters.

Any unit in a datom may be followed by a parenthesis. What the parenthesis holds is a `Noema` whose target is the unit it follows — an `Annotation` whose `AnnotationTarget` is implicit, the enclosing unit's content address. Inside the parenthesis every delimiter is live until the balancing close.

```
Lock.{ OrchestrateDocs AmberFalcon [ /home/li/primary/Vision/messaging.md ] «Clarify Lock fields»
       (Injunction.Order.Prose.«Hold until the 0.16 pair lands.») }
```

The parenthesis annotates the lock. Nesting is the living's "three or four layers of side notes": a noema inside a noema annotates the inner unit, and each is addressed by the checksum of its content and links, never by a path.

> If a meaning is changed, its identity changes.

**Fork 4.** Is the target of a parenthesis always the unit immediately before it (proposed), or may a parenthesis name its target explicitly with a `ContentLink` for a unit elsewhere? Proposed: implicit when it follows a unit; explicit `Annotation.{ AnnotationTarget AnnotationBody }` when it stands alone, as built.

## 6. Struct fields that carry a root meaning element

> Some of the variants carry structs, which can sometimes have some of their fields in their struct have another root meaning element. It can add an annotation of another meaning in that particular unit.

A field may be typed `Noema`. The built ethos already does this in spirit: a kāraka's filler is a content link to meaning; a statement's subparts are links. Written directly:

```
Karaka.{ KarakaRole Noema }        ; the agent, the object, the instrument — each a meaning, not a string
Statement.{ Content Support }      ; Support is Vector<Noema>
Response.Answer.{ Inquiry Content } ; the inquiry answered is itself an utterance
```

The rule: wherever a struct field would have been a string that means something, its type is `Noema`. Where the meaning is not yet typed, the field is `Content.Prose` — an opaque string the reader passes through.

> The string is an unspecified program. It's unfinished computer science. The final computer science only has a string in display data.

## 7. Table of equivalents

Sanskrit structure first, English candidates second, the chosen English name third. The type carries only the English. Rows marked *cited* are in the existing research (`flows/5851f4/reports/paniniAnatomy.md`, `flows/e51411/reports/sanskrit-grammar.md`); rows marked *recall* are this seat's recollection of the tradition and need the Mind's check before they enter the ethos.

| Sanskrit (IAST) | tradition | English candidates | chosen | grade |
|---|---|---|---|---|
| vākya | Bhartṛhari | sentence, utterance | Utterance | cited |
| sphoṭa | Bhartṛhari | the meaning-bearing whole | Noema (the unit) | cited |
| pratijñā | Nyāya | claim, thesis, statement | Statement | cited |
| hetu | Nyāya | reason, ground, support | Support | cited |
| udāharaṇa | Nyāya | example, instance | Example (inside Support) | cited |
| upanaya | Nyāya | application | Application | cited |
| nigamana | Nyāya | conclusion | Conclusion | cited |
| praśna | Nyāya | question, inquiry | Inquiry | recall |
| uttara | Nyāya | answer, reply | Response.Answer | recall |
| saṃśaya | Nyāya | doubt | Inquiry.Question (with a doubt marker later) | recall |
| vidhi | Mīmāṃsā | injunction, prescription | Injunction.Order | cited (as Pāṇini's operational rule); recall (Mīmāṃsā) |
| niṣedha | Mīmāṃsā | prohibition | Injunction.Prohibition | recall |
| arthavāda | Mīmāṃsā | explanation, commendation | Annotation | recall |
| ājñā / anujñā | general | command / permission, assent | Injunction.Order / Response.Assent | recall |
| padārtha | Vaiśeṣika | category | Category (built as Padartha) | cited |
| kāraka | Pāṇini | role, participant | Role (built as Karaka) | cited |
| dhātu | Pāṇini | root | Root (built as Dhatu) | cited |
| lakāra | Pāṇini | tense-mood | TenseMood (built as Lakara) | cited |
| prayoga | Pāṇini | voice | Voice (built as Prayoga) | cited |

The built ethos still names its variants in Sanskrit (`Lakara`, `Prayoga`, `Kartr`). The living's word is that the types carry English, with the table as the bridge:

> When I say Panini I don't mean do just the Sanskrit and we're not going to use the Sanskrit terms but we can maintain a table of equivalents.

**Fork 5.** Rename the built Sanskrit variants to their English column now, or leave them until the Act layer is next touched? Proposed: rename now, in the same landing that adds the Utterance layer; backward compatibility is not a design variable.

## 8. Display

A noema is never shown raw to the living. Rendering is a template per language and alphabet — the living's "how you display this particular meaning in such-and-such language on such-and-such alphabet." English first:

```
Injunction.Order.Prose.«Regenerate the ouranos proposal.»     →  Order: Regenerate the ouranos proposal.
Inquiry.Audit.Prose.«Did 38 reach a terminal?»                →  Audit: Did 38 reach a terminal?
Statement.{ Prose.«…» [ two psyches ] }                        →  Statement (2 supports): …
```

The human display type of the letter book is this rendering applied to a letter's noema.

## 9. What this book asks the living to rule

1. The name: Noema (Fork 1).
2. Five top-level utterances — Statement, Inquiry, Injunction, Response, Annotation — with the four message kinds as chains beneath them, and the letter's `Kind` dissolved into a `Noema` (Fork 2).
3. Every statement carries its support (Fork 3).
4. A parenthesis annotates the unit before it; explicit targets only when it stands alone (Fork 4).
5. The built Sanskrit variant names become their English equivalents in the same landing (Fork 5).
6. The *recall* rows of the table go to the Mind for checking before they enter the ethos.

Sources: `flows/b7ba00/vision/meaningLanguage.md` (fourteen entries, 2026-08-11 to 2026-09-26); `flows/f38926/vision/meaningLanguage.md` and archives (content-addressed annotation, Nix-like retention, "go find the best ontology"); `Vision/meaning.md`, `Vision/datom.md`; `/git/github.com/LiGoldragon/meaning-language/ethos/meaning.ethos`; `flows/5851f4/reports/paniniAnatomy.md`; `flows/e51411/reports/sanskrit-grammar.md`; `flows/f38926/reports/ontology.md`; the datom, protos and ethos skills.
