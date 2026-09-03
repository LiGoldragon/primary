# Distillation proposal 1 — flow 4decf7

Composed in the main flow from the six gatherings in reports/, from
flows/b675f3d9/reports/distillProposalProtosDatom.md and its
acbb6006 addendum, and from the living's fresh words in this flow.
Each statement lands only on the living's explicit approval, and
each names its topic. On approval: the referenced raw records move to
`archive-` files beside their sources; the fresh verbatim heard in
this flow (the opening message on the practice; "kinds are
qualifier-named") is logged directly as archived in
flows/4decf7/vision/archive-<topic>.md; transcript-only words that
no log carries are logged the same way; the sources files are
appended; impurities named below are destroyed.

## Ordering assumption

Several records are undated in their files. The record's own words
date them: 2ef42163 answers the Embodied/Forged debate of 04db2fd2
(2026-08-26/27) and precedes e8c4cc61 (2026-08-29), which precedes
62022e8f (2026-08-30/31) and 995a164e (2026-08-30 to 09-01). Under
that order the naming of the text-to-value direction is a succession,
realize → embody → actualize, and Prospective → Potential likewise,
not a same-time conflict.

---

## Topic: kinds — Vision/kinds.md (new)

### Kind is the word

Kind is the word for the bearer of capabilities: something that can
run is a runner, and Runnable is its kind. Trait is set aside as
acoustically ambiguous. In ethos there are no generics, only kinds.
Declaring a new kind declares a new trait in the Rust world and
implies more in the ethos world, still to be determined.

### Capability

A capability is a function a kind has: Runnable is the kind, run the
capability.

### Kinds are qualifier-named

Kinds are qualifier-named: Writable and Readable, Runnable,
Textualizable, Structural, Embodied. Write is not a kind. The verbs
Rust imposes are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed. An existing Rust trait may be
kept under its own name rather than carried in a conversion table.

### Identity

A kind is identified, as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>.

### Positions hold kinds

Angle brackets hold the kinds standing in a type's or a kind's
positions: Vector<Ordered>, Result<Vector<Sortable> Error>. The form
is chosen for token economy and because it recycles Rust cognition. A
kind declaration's position holds a kind, never a type. The type that
bears a kind is Self, as in Rust.

### Declaration

The kind syntax is drawn from the anatomy of a Rust trait in its most
complex form, so that every kind can be expressed with the most
elegant syntax. A simple kind is a bracket block of capabilities; a
complex kind opens with a brace and carries fields such as its
superkinds. Ethos keeps separate blocks for types and kinds.

### Capability signature

A capability's yields are written in a bracket block, even a single
yield. The head takes one separator, so its options are mutually
exclusive: `!` marks a mutable self, `:` no self. Within a kind's
capabilities, different structures may be different types, told
apart, as everywhere in ethos, by the delimiter after the head.

### Open

- The names of a kind's sections: associated types, constants; asked
  twice, not ruled.
- A single yield standing bare, `len.Count`, was accepted on
  2026-08-27; yields always bracketed was ruled the same day. Which
  stands?
- The name of the default kind every ethos type bears to describe its
  textual structure: Datomizable narrows it to datom; ProtoShaped,
  ProtoFormed, ProtoExpressible, protoform, protosic, protoformal
  floated; Protoformed too close in speech to protoform.

---

## Topic: protos — Vision/protos.md (Direction replaced, the rest new)

### The shared style

Protos is the style all our dialects share. Ethos, Datom, Nomos and
Logos are protos dialects. The fully decomposed engine, three
nexuses, is the protos engine. Datom is a protos dialect that takes
no part in the ethos → nomos → logos → Rust engine, being the dialect
for pure typed data.

### Everything written is data

A dot opens a delimiter. The textual form of a thing is itself data,
and so a type.

### One representation

A type has exactly one protos representation.

### A block gives its characters their meaning

A character has no meaning of its own: the block being parsed gives
it one, and a character is free in every block that has not yet given
it a meaning.

### Situation

Situation is the word for what a parse is in; it frees context.
(Intent/protosParsing says context. Intent wording changes only on
the living's explicit word.)

### Anatomy, not interpretation

Protos is structural recognition of delineations and nothing more. A
Head is just a Head. The number of components in a brace block is
anatomical; in a bracket block it is not. Delineation is protos, and
so is anatomy: a shape is described independently of the type it
represents. A type's anatomy belongs to its dialect.

### Structure

Structure is the one word for a struct's field, an enum's variant, a
vector's element: every object is a structure. An enclosed structure
holds a vector of inner structures; an opaque structure holds none. A
Structural thing's capability, structure, returns its protos
structure and every structure it contains, recursively.

### Shape in context tells the type

Within its parsing context, a block's shape tells its type. The shape
is: whether the block opens with a head at all; the character between
the head and the body; the delimiter of the body; the number of
components inside. A block need not start with a head: a bare brace
block or a bare bracket block stands in a position whose context
already knows its type; and where a head is present, its mere
presence can be what conveys the type. Several types may share one
position when their shapes differ; the shape is then what tells them
apart. Structures of different size are different types. The
character between a head and its body adds a type distinction for the
cost of one character.

### Struct and vector

A struct is one fixed shape: the same fields in the same order, each
field's type declared, any type allowed in any field. A vector is the
one variable-length form, and all its components share one type or
one kind.

### Angle brackets

Angle brackets are a protos delimiter. Datom and Ethos keep angle
brackets compatible, so that datom can one day be embedded in ethos
positions.

### Forms of a value

A value has an embodiment, its Rust value, the form the runtime uses;
a signal form, its bytes on the wire; and a textual form. Any concept
in Protos has an embodiment: a kind, a type, a datom value each have
a Rust value, and a kind declaration in ethos becomes an embodied Rust
value holding its name and the rest of its definition. Embodied is
our word over Sized. The words working, real, code, encoded and
transcodable are retired.

### Headed and contained

An embodiment has two textual forms. In the headed form the head
stands outside the block it opens; in the contained form the name is
the first position of a self-contained block. The contained form is
how the embodiment is specified, its head a field of the Rust struct;
the headed form is syntax sugar.

### Symbols

A capitalized bare symbol and an uncapitalized one are two different
types: the capitalized one is an embodiment, a corporal symbol; the
uncapitalized one is a reference, a path, a link.

### Direction (replaces the current statement)

Text arrives as a potential value and leaves as a value. Text is
Potential: actualize reads it into its embodiment and may fault,
since the text is potential until it matches its anatomy. The
Embodied is Textualizable: textualize writes the textual form and
cannot fault, since an embodied value is already whole. The two
capabilities sit on two different types: the text is never
textualized, the embodied is never actualized. Spans are found on the
way in and computed on the way out. Each direction is several passes,
and the type being embodied into is not known until later passes.

### Layers

Reading is layered: Text, Structure, Concept, Corpus. Structure is
the anatomical survey, which knows only that a protos object is
there; Concept is the dialect's reading, where a data-carrying enum
is first the concept of an enum, a vector; Corpus is the final form,
the embodiment. The kinds are Structural, Conceptual, Corporal, and
the capability that reaches a layer sits on the layer above:
structure on Text, conceive on Structure, incorporate on Concept. To
embody a layer is to get the layer below. Potential is the kind used
universally to go from one layer to the next, a rewording of Rust's
TryInto; actualize is its capability; Embodied is its bound. Text to
Potential<Protos> lives in protos; Protos to Potential<Datom> lives
in datom; the associations of different libraries are never mixed.

### Shape-defined types

A protos type is implemented as a match over the standard shapes,
each shape carrying its own parsing context; a complex type is a
vector of shapes. ShapeDefined names this.

### Logic planes

A big implementation is the sign of a missing logic plane. Every part
stays simple; the complexity lives in the totality.

### Open

- Import separator: `/` (2026-08-07) or the colon after the source
  name (the 2026-08-20 examples). Which stands? An ethos matter,
  blocking the ethos round.
- The name of the structure-layer type: Protos, or Structure.
- The parenthesis block: content-opaque today, not yet universal, so
  not yet protos.
- Multi-form concepts and the concept layer: marked unsettled by the
  living in their own words.

---

## Topic: datom — Vision/datom.md (revision)

### Nature (replaces the first paragraph; the second paragraph stands)

Datom is the most advanced textual data format in the world. It
carries data, strictly typed, and its whole work is carrying data
between text and typed form. Datom is signal's form at the edge: our
components speak signal, and datom lets text-based systems, LLMs and
every existing editor, read and write it.

### Kind (new)

Datom is a kind, not a type: it has no definite shape. The kind is
Datomic. A datom is not preceded by a Datom root; a comment may say
it is datom.

### Direction (new)

A datom on the way in is a potential datom, untrusted until it
matches its type; on the way out it is a datom.

### The interface shape (addition, last sentence)

A CLI takes its whole configuration from its datom input.

### Syntax (replaces)

The dot opens a delimiter: a Head is bare text ending in a dot,
written immediately before the block it opens. The Head is part of
the block's type, and a variant re-emits its Head when textualized. A
bare brace block is a struct.

Curly quotes are the string delimiter. Parentheses are reserved for
Meaning. A string is a string only in a position where the type
defines a string; there it is written bare whenever the bare form can
carry it, and a bare string may carry symbols that are load-bearing
elsewhere, the colon among them, the machinery made fit for this by
the right abstraction layers. A string block is opaque: interior
delimiters are content until the block closes.

Guillemets delimit a map, and its entries resolve by position: key,
a space, value. A position expecting a map carries no Map head, since
the position already knows its type; a Head is thereby always a
variant.

An integer is written as bare decimal: 0, 42, -42; ASCII digits, no
leading plus, no leading zero except 0 itself.

A single semicolon opens a comment.

### Style (new)

Canonical text leaves a space inside every bracket and brace
delimiter, at both ends, so that head, dot, delimiter and content
read apart; never inside curly quotes, where a space is content.

### Repository and migration (addition)

No Dotos file remains.

### Library and nexus (new)

Datom is a library for now, and the library takes another name so
that datom is free for the datom nexus, which comes when there is
more to do: translating datom objects between formats, and a parsing
cache keyed by the content-addressed hash of normalized Text.

### Meaning (addition, after the first sentence)

The aim is the most advanced structured meaning system ever made,
exposing the emphasis and the other structure a plain string lacks;
annotations are enums used throughout the tree, Emphasis among them.

### Reply shape (new, provisional)

A Nexus reply is written as its heads down to its data, and only what
carries data is written. An empty Locks observation is
Observed.Locks.[]: the Observed variant, its Locks variant, the empty
vector. The layout of a nonempty payload is open.

### Open

Floats and dotted numbers; newlines and indentation; omittable
fields; the dot-parenthesis block now that parentheses belong to
Meaning; the library's name, datom-codec floated; what Text has over
String: normalized, non-structural whitespace removed, a
content-addressed hash.

---

## Topic: ethos — Vision/ethos.md (two additions, from the b675f3d9 draft)

### Type declarations

In an Ethos type declaration the delimiter after the head tells the
type: X.{…} declares a struct, Y.[…] an enum, Z.Word a typedef. The
same mechanism serves wherever several types share one position: the
section of an interface, the capabilities of a kind.

### A block gives its characters their meaning

In Ethos a character means what the block being parsed says it
means: a colon in an import block is the import form; in a block of
capabilities it is free to mean what that block says.

(The draft's third ethos addition, "Angle brackets hold kinds", lands
in kinds as "Positions hold kinds".)

---

## Topic: distillation — Vision/distillation.md (additions)

### Distilling as we go

Distillation runs alongside the work: the raw vision that relates to
what is being done is brought forward as a distillation while the
work proceeds.

### Fresh material enters through the distillation

What the living says fresh during the work is folded into the
distillation proposal rather than created as a raw record. Once the
distillation is agreed, the verbatim words are logged in the flow
that heard them, archived from the start since the distillation
carries their content, and referenced from the distillation's
sources. The aim is vision that is born distilled.

### Understand, then explain

A proposal is written by one who has understood: statements that
confuse when said together are separated; everything is split up,
then re-assembled.

---

## Graduation questions

- Logic planes (protos): a pattern guiding many decisions. Should
  this be Intent?
- The best shape (6863ef19 theBestShape: the minimum code for the
  most elegant machinery, easily understood, extended, introspected):
  the living flagged possible Intent. Should this be Intent, and in
  what words?
- Multiple steps are not feared (e8c4cc61 prospective): already
  Spirit's correctness-over-machinery line; not re-stated.

## Impurities discarded (destroyed on approval)

- 01a038b5 curriculumStackToDatomInsteadOfDotos: "I want to migrate
  curriculum stack to datom instead of dotos": a working instruction.
- ac1e9ec8 datomSkill: the session opener "Acquire all psyche on
  datom syntax. We will distill it all, then create a skill…": a
  working instruction (the acbb6006 addendum asked; unanswered).
- 04db2fd2 kinds, third entry: "extend our example to specify all of
  protos, and draft out the accompanying kinds…": a working
  instruction with a question.

## Not carried, left for their own topics

- The protos, datom and ethos skills (e8c4cc61 designPractice,
  62022e8f designPractice, f426777b skillDesigning): topic skills.
- Import resolution (2b34fafa importResolution, sourceNotCrate,
  vision-raw importResolution): the ethos round, once the separator
  is ruled.
- "datom doesnt support omittable fields yet" (4d5fc7da datom):
  implementation status; archived with its record, listed under
  datom Open.
- The crystallization of this practice into a skill: the flow's
  plan, in log.md.

## Sources to append on approval

Vision/sources/kinds.md (new):
6863ef19 traitsAsCapabilities · 06196cc7 traitsAsCapabilities ·
2b34fafa traitsAsCapabilities · f426777b spokenVocabulary ·
04db2fd2 kinds · 2ef42163 kinds · e8c4cc61 kinds · 62022e8f kinds ·
995a164e kinds · b675f3d9 kinds ·
5abf3be8 encodedFormFingerprintTraitDesign · 4decf7 kinds

Vision/sources/protos.md (new; includes the landed Direction's
source):
04db2fd2 directionAsymmetry · a5587095 protosIsTheSharedStyle ·
ba906ae2 protosIsTheSharedStyle · ba906ae2 encodedFormIsTheCode ·
06196cc7 encodedFormIsTheCode · 06196cc7 traitsAsCapabilities ·
06196cc7 threeStacks · 6863ef19 encodedFormIsTheCode ·
6863ef19 traitsAsCapabilities · 2b34fafa traitsAsCapabilities ·
2b34fafa protosIsTheSharedStyle · 04db2fd2 textualTypes ·
04db2fd2 multiPass · 04db2fd2 delineate · 04db2fd2 anatomy ·
04db2fd2 portion · 04db2fd2 delimiters · 04db2fd2 kinds ·
db97561c prospective · e8c4cc61 protos · e8c4cc61 prospective ·
2ef42163 kinds · 62022e8f kinds · 62022e8f concept ·
62022e8f headedAndContained · 62022e8f symbols · 62022e8f passes ·
995a164e designPractice · b675f3d9 structuralParsing ·
5abf3be8 dotOpensDelimiterEverythingIsData ·
vision-raw encodedFormIsTheCode · vision-raw traitsAsCapabilities ·
vision-raw protosIsTheSharedStyle · 4decf7 protos (transcript-only
words of 2026-08-04 on angle brackets, logged archived)

Vision/sources/datom.md (append):
ac1e9ec8 datomIsData · 01a03eda datomInteger · 04db2fd2 datomMaps ·
04db2fd2 datomNexus · 04db2fd2 text · 04db2fd2 textualTypes ·
04db2fd2 anatomy · 04db2fd2 directionAsymmetry ·
e8c4cc61 datomSyntax · e8c4cc61 datomizable · 62022e8f datomSyntax ·
62022e8f kinds · 995a164e datomSyntax · 01a04339 datom ·
01a035d3 rustCodeFromTheData · 01a03d6e dotosFiles ·
01a03d6e ethosInterfaces · a5587095 structuredStringType ·
5abf3be8 colonLegalInStringPosition · 4decf7 datomSyntax
(transcript-only words: 2026-08-07 floats question; 2026-08-04
"String is correct", logged archived)

Vision/sources/ethos.md (new; the earlier 68512643 distillation left
none, its sources reconstructed from archive headers):
01a02a34 ethos · 01a02a34 schemaSyntax ·
vision-raw ethosDotosDivisionAndHelp · vision-raw ethosNonRepetitionLaw ·
b675f3d9 structuralParsing · a5587095 colonFormTransformerSyntax ·
4decf7 ethos (transcript-only words of 2026-08-03 on X.{ and Y.[,
logged archived)

Vision/sources/distillation.md (append):
4decf7 distillation · ac1e9ec8 datomSyntax

---

## Revision 2 — merged texts (after the living's corrections of 2026-09-03)

The living's corrections: "might imply more" in place of "implies
more"; an example with no Rust standard in place of Write/Writable;
no conversion tables; the proposal is the merged text of each topic,
prose not bullet points, composed with the existing distilled vision
in hand, a new sentence merged into the existing sentence on its
matter.

Conversion-table wording located: nowhere in Vision/, Intent/ or the
spirit. Raw only: b675f3d9 kinds ("maintain a table for conversion
... it might be better to keep the existing trait as-is") and the
6b31eff3 transcript of 2026-08-04 (a translation table in logos
emission). Neither feeds the distillation; the transcript line is
not logged.

The merged texts stand in design/proposal1/: kinds.md, protos.md,
datom.md, ethos.md, distillation.md, each the whole file as it would
land in Vision/. Vocabulary edits inside existing sentences: "traits"
to "kinds" in datom Relation to Ethos and ethos Why Ethos; em-dashes
in existing sentences replaced by commas where a sentence was
re-touched.

Skill line proposed for psyche-distillation (authored source
/git/github.com/LiGoldragon/Curriculum/skills/psyche-distillation.md,
then regenerated): "A proposal is composed with the existing
distilled text of every topic it touches in hand, and shows each
topic's text as it will stand: new material merged into the existing
sentences, prose, never bullet points."

The open items, impurities, not-carried list and sources of revision
1 stand, with these changes: the 6b31eff3 translation-table line is
dropped from the datom sources; the datom Repository block now
carries the later word (the library renamed, datom free for the
nexus) over the earlier "the repository is plain datom", a tension
for the living to rule.

---

## Revision 3 — with example code (after the living's words of 2026-09-03)

Landed before this revision: Vision/kinds.md Kind and Naming, on the
living's word that what was read past without comment is accepted.

Identity re-worded to name exactly what identifies a kind: its name
and its positions, as a Rust trait is identified by its name and its
generic parameters; what a position requires, superkinds, associated
types and constants, capabilities are definition, not identity. The
Rust facts are the flow's exactness; the living rules on the wording.

Examples and their origin. The living's own: X.{ … } and Y.[ … ]
(236af273, 2026-08-03); Sorted.{Vector<Ordered>} with its Rust
comment, and Result<Vector<Sortable> Error> (6b31eff3, 2026-08-04);
Processable<[Clonable Sendable] Serializable> (b675f3d9, 2026-08-26);
Library.{0 1 0} with its sections, headed and contained (e8c4cc61,
2026-08-29); signal-psyche:Object, signal-psyche:[Object Thing],
signal-psyche:stream.[Stream Termination] (2b34fafa, 2026-08-20);
Observed.Locks.[] (01a04339); 0 42 -42 (01a03eda); [ key value
second-key second-value ] (ac1e9ec8, re-delimited with the guillemets
ruled the same day). Flow-written from the living's corrections:
Textualizable.[ textualize.[ Text ] ] (a 2ef42163 line the living
read past); Embodiable.[ embody.{ [Text] [Result<Self Error>] } ]
(the living's "bearer? you mean Self?" and "why Fault instead of
Error?"); Sink.[ push![ Count ] create:[ Self ] ] from "! for
mutable self", "`:` for no self stands", "use [] even for single
object yield"; Text.[ Potential<Protos> ] and Protos.[
Potential<Datom> ] from 995a164e's typed words; the Rust impls in
Direction; the anatomy, struct, map and vector lines. Every
flow-written example is composed only from ruled syntax, and the
living rules on each.

Yields: the bare len.Count was accepted 2026-08-27T09:04Z (b675f3d9);
"use [] even for single object yield" was ruled 2026-08-28T11:07Z
(04db2fd2). The later stands; the sentence on different structures
being different types stands without the bare example.

Error, not Fault, in examples: the living's Result<… Error> and the
question "why are we using Fault instead of Error?" (e8c4cc61).

The complex kind opening with a brace has no example: the living
named it and no shape of it has been approved. The kind-to-type
association syntax is open ("we need to draft a syntax for kind to
type association"); the association block is the living's file
section, the inner form is the one the living read past.

New in distillation: re-distilling, vision shows its code, examples
carry only what was said. The living's "you should always present
the ethos spec of any new object" (e8c4cc61, 2026-08-29) waits for
the skills round.

Skill lines proposed for psyche-distillation (authored source in
Curriculum, regenerated after): "A distillation re-distills: the
existing distilled text of every topic it touches goes into the
distiller with the raw records, and the proposal shows each topic's
text as it will stand, prose, never bullet points." and "Whatever
describes anything to do with code shows example code, commented; an
example shows only what the living said or wrote."

---

## Revision 4 — every Rust example paired with its ethos (2026-09-03)

The living: "Whenever presenting Rust code, you should always present
the equivalent ethos code." Folded into distillation, Vision shows
its code. Applied: Runnable now yields Outcome so that its ethos
uses the bracketed-yield form; the legacy line pairs with the
association Sink.[ Write ]; Identity's Rust drops the where-clause,
associated type and constant, whose ethos is the unshaped complex
kind, and pairs with Convert<Clonable>.[ convert.[ Result<Clonable
Error> ] ] and Text.[ Convert<Integer> Convert<Boolean> ]; Direction
pairs with the two kinds and two associations; datom De/serialization
uses the living's own Sorted for Rust, ethos and datom alike.
The capability yielding the kind named in its position follows the
living's "why not return Embodied trait instead of Output?"
(e8c4cc61). Unruled and flagged: the separator for a consuming self
(actualize takes self in Rust; `.` is written); the association
form Type.[ Kind … ] is the one the living read past in 2ef42163.

Skill line proposed for psyche-interraction: "Rust code shown to the
psyche is always shown with its equivalent ethos."
