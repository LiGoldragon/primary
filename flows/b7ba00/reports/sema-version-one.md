# Sema, version one

Fable b7ba00, Psyche, 2026-09-26, on the living's word relayed by Psyche Opus 93ba9f. The technical text stands alone; illustration markers name where a picture inserts. Every rule is a proposal until the living rules; the living's words are quoted where they bind (verbatim in `flows/b7ba00/vision/meaningLanguage.md`; the notion in `flows/b7ba00/notion/sema.md`).

## 1. The name is Sema

> Originally that was the idea. Sema was supposed to be the language of meaning and so that is actually the right name.

The language of meaning is **Sema**. What this book earlier called Noema is Sema; a parenthesis in datom opens a sema; the root type is `Sema`.

The rename reaches two places. The database now called Sema stores sema but not only sema, so it takes a new name — the living asks for something clever. Ethos also has a root named Sema; the rename reaches it, and the Mind surveys what refers to it before anything moves.

**Ruling 1.** The database's new name. Candidates, each one word, Greek, not yet used in the system: *Mnema* (memory, a record), *Thesauros* (a store), *Archeion* (the archive). Proposed: Mnema.

[ILLUSTRATION 1 — three labels: the language Sema; the database, formerly Sema, now Mnema (proposed); Ethos's root Sema, reached by the rename. One arrow from the old database name to the new.]

## 2. Is the Category layer equivalent with Ethos?

> Is this category part of the language equivalent with our ethos?

The Category layer — the Vaiśeṣika roots, the twenty-four qualities, the quality structures — is written entirely in Ethos's own forms: aliases, structs, enums, vectors. It adds no construct to Ethos. It is an Ethos library, a vocabulary of things and their qualities, declared the way any type is declared.

So the answer is: Category is Ethos, used for one purpose. Ethos declares what kinds of things exist; Sema says something about them. The three layers are then: Ethos types for what is (Category), the Pāṇinian act for who does what (Act), and the utterance for what kind of saying it is (Utterance). Annotation attaches to any of them.

## 3. Sema version one — a strongly typed string

> The first version of sema could be that it just has one or two layers of variants, possibly with one variant and then another variant inside and the payload at the end being a string. That way we get a sort of strongly typed string, if you will. And this then becomes the basis for how agents start to communicate with the message component.

> We could even have the inner component be Markdown, I guess … I think the same delimiter that we use for strings would work so that we're reminded that this part of SEMA is undeveloped, basically. When SEMA is fully developed there are no more strings because we can express anything through the structure of the SEMA specification.

Version one is the utterance tree, at most two levels deep, ending in a Markdown payload written in string guillemets. The guillemets are the mark of what is not yet typed.

```
Markdown.String

Sema.[ Statement.Markdown
       Inquiry.Inquiry
       Injunction.Injunction
       Response.Response ]

Inquiry.[ Question.Markdown  Audit.Markdown  Information.Markdown ]
Injunction.[ Order.Markdown  Prohibition.Markdown ]
Response.[ Answer.Markdown  Assent  Refusal.Markdown ]
```

Written out, a sema is one or two heads and then the words:

```
Statement.«Deployment 38 replaced its own Nexus at 09:24.»
Inquiry.Audit.«Did deployment 38 reach a terminal?»
Injunction.Order.«Regenerate the ouranos proposal against goldragon main.»
Response.Answer.«No terminal; the row is orphaned in Copying.»
Response.Assent
```

The reader knows from the heads what kind of saying this is before reading a word; the words themselves stay Markdown until Sema can type them.

**Ruling 2.** Is the payload type named `Markdown` in Ethos, an alias of String, as above? Proposed: yes, so that the guillemets always mean "Markdown, undeveloped" and nothing else.

**Ruling 3.** May `Response.Assent` carry nothing? Proposed: yes — assent has no words to add; every other leaf carries Markdown.

[ILLUSTRATION 2 — the two-level tree: Sema at the root; four branches Statement, Inquiry, Injunction, Response; their leaves; each leaf ending in a guillemet pair «…» drawn as the "undeveloped" mark.]

## 4. How an agent talks to Message with it

The living has ruled that a letter's head is its kind, an open set of Ethos types each carrying all its data, and that priority leaves the letter. A letter is therefore a kind whose fields are the sender and a sema:

```
Sender.[ Living  Seat.Seat ]
Seat.[ Psyche.Layer  Mind.Layer  Field.Layer ]
Layer.[ Primary  Secondary  Tertiary  Quaternary ]

Order.{ Sender Sema }
AuditRequest.{ Sender Sema }
AuditReport.{ Sender Sema Vector<Sema> }        ; the report and what it rests on
PsycheUpdate.{ Sender Psyche }                  ; the living's words, not a sema
Letter.[ Order.Order  AuditRequest.AuditRequest  AuditReport.AuditReport  PsycheUpdate.PsycheUpdate  … ]
```

Three letters as a flow sends them:

```
Order.{ Psyche.Primary  Injunction.Order.«Regenerate the ouranos proposal against goldragon main.» }
AuditRequest.{ Psyche.Primary  Inquiry.Audit.«Did deployment 38 reach a terminal?» }
AuditReport.{ Field.Primary  Statement.«38 is orphaned in Copying; its self-switch replaced the Nexus.»
              [ Statement.«lojix-self-switch-deploy-38.service Result=success»  Statement.«no copier process on ouranos at 10:31» ] }
```

The sender stays outside the sema as the letter's first field: the sema is what is said; who says it is the letter's business. Which kind interrupts is the database's judgment per kind; nothing in the letter says soft or hard.

**Ruling 4.** The sender outside the sema, as the letter's first field. Proposed: yes.

**Ruling 5.** Which kinds ship first. Proposed: Order, Question, AuditRequest, InformationRequest, AuditReport, ImplementationReport, PsycheUpdate, Answer — the living's list plus the four already in use.

[ILLUSTRATION 3 — one letter drawn as a box: the kind as its head; inside, the sender at left and the sema at right; the sema's guillemet payload shaded as "undeveloped"; below, the database holding a small table kind → interrupts or not.]

## 5. The road to full Sema

Version one is the trunk. Each later version types what the guillemets still hide, and every consumer moves with it:

| version | what the payload becomes | layer it draws on |
|---|---|---|
| one | Markdown in guillemets | Utterance |
| two | the Pāṇinian act where the words are an act: root, tense-mood, voice, roles | Act (built) |
| three | Ethos objects where the words name things and qualities | Category (built) |
| full | no strings; every unit a sema; annotation on any unit | all, with Annotation |

The living's notion of a complete communication — a struct holding a vector of utterances, a vector of acts, and a vector of Ethos objects, with annotation attachable — is recorded as a notion. It is not built here; it is the shape version three would reach for if the living raises it.

[ILLUSTRATION 4 — a road with four milestones, version one to full; at each, the same example sentence drawn with less guillemet and more structure.]

## 6. What this book asks the living to rule

1. The database's new name (Mnema proposed).
2. `Markdown` as the payload type in Ethos, an alias of String.
3. `Response.Assent` carrying nothing.
4. The sender outside the sema, first field of every kind.
5. The first kinds to ship.

And two items the Mind carries before anything lands: what refers to Ethos's root named Sema; and the equivalents table's recall rows from the Noema book.

Sources: `flows/b7ba00/vision/meaningLanguage.md`, `flows/b7ba00/vision/messaging.md` (the head is the kind), `flows/b7ba00/notion/sema.md`, `flows/b7ba00/reports/anatomy-of-the-meaning-language.md` (now the Sema book, with its addendum), `/git/github.com/LiGoldragon/meaning-language/ethos/meaning.ethos`.