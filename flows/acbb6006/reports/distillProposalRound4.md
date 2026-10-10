# Distillation round 4: protos, datom syntax, ethos, ethos interfaces, ethos-monolith, kinds, anatomy — reconsidered

Composed in flow acbb6006 from flows/b675f3d9/reports/distillCandidates
{ProtosDatom,Ethos,Kinds}.md (verbatim records), replacing the three
b675f3d9 proposals. Reconsidered under today's rulings: a statement
carries what the psyche said and nothing beyond it; no narrative of
current work; no useless negatives; destination named per statement;
discards pointed out. Each statement lands only on the living's
approval (anything commented past and not commented on is approved).

Record ids refer to the candidate reports.

---

# Vision/protos.md (new)

## The shared style
From a5587095/5, ba906ae2/1.
Protos is the name of the style all our dialects share. The final,
fully decomposed engine with its three daemons is the protos engine;
Datom sits beside it, a protos dialect for pure typed data only,
outside the Ethos/Nomos/Logos Rust-generation engine.

## Everything is data
From 5abf3be8/1, 6863ef19/4.
The dot opens a delimiter, and everything is data. The textual form
of a thing is data, and so a type.

## One representation
From 6863ef19/2.
A type has one protos representation.

## Structure tells the type
From b675f3d9/6, b675f3d9/10.
Structural parsing tells types apart by structure: structs of
different size are different types, and the delimiter between the
head and the body adds further type differentiation at the cost of
one character.

## Struct and vector
From b675f3d9/9, b675f3d9/11.
A struct always has the same fields in the same order; its
definition declares the field types, and a field may hold any type.
Variable length is a vector, and all its components share one type
or one kind.

## Angle brackets
From b675f3d9/7, ac1e9ec8/10.
Angle brackets are a protos delimiter. Datom and Ethos keep angle
brackets compatible, so that datom may one day be embedded in ethos
positions.

## Forms of a value
From 06196cc7/1, 1b, 1c, 4c; 6863ef19/2.
A value has a real form, a signal form and a textual form. Realize
reads the textual form into the real form; Textualize writes it
back. Code, encoded, working and transcodable are retired words.

## Shape-defined types
From a5587095/8, a5587095/9, 06196cc7/4c.
ShapeDefined is the kind a protos type bears. Implementing it is a
match over the standard shapes, each shape with its own parsing
context; a more complex type is a vector of shapes, the structure
dictating the outer type.

## Logic planes
From a5587095/10. Graduation asked: Intent?
A big implementation is the sign of a missing logic plane.
Everything is simple individually; the complexity is in the totality.

Withdrawn from the b675f3d9 draft: "Parsing in context" (Intent/
protosParsing.md already carries it); "Shape in context tells the
type" (grown beyond the words; replaced by "Structure tells the type").

---

# Vision/datom.md (revisions)

## Nature (replaces the first paragraph; the Ethos-inline paragraph stands)
From ac1e9ec8/6, /1, /9; 012fbf07/1.
Datom is the most advanced textual data format in the world. It
carries data, strictly typed; its whole work is carrying data
between text and typed form. Our components speak signal; datom is
used at the edge, to let text-based systems — LLMs and every existing
editor — understand signal.

## Syntax (replaces the section)
From 06196cc7/2, /3, /4b, /5, /7, /8; ac1e9ec8/8, /7, /2, /4; 01a03eda/1.
Consistency comes first: datom's syntax is fixed before the rest.
The dot opens a delimiter. The dotted prefix of a delimited block is
its Head, part of the block's type; a variant re-emits its Head when
textualized. A bare brace block is a struct. Curly quotes delimit
strings; parentheses are reserved for structured strings, Meaning. A
string is a string only in a position where the type defines a
string; there a string that needs no quotes is written bare, and a
bare string may carry symbols that are load-bearing elsewhere, the
machinery made fit for this by the right abstraction layers. A
string block is opaque: interior delimiters are content until the
block closes. Guillemets delimit a map; a position expecting a map
carries no Map head. An integer is bare decimal: 0, 42, -42.

Not stated (unruled): key/value resolving by position in a map
(ac1e9ec8/3, "considering"); whether a Head is always a variant
(ac1e9ec8/5, a question).

Withdrawn from the b675f3d9 draft: "No Dotos files remain"; the
"Open" section (unknowns stay in flow logs).

---

# Vision/ethos.md (additions)

## The delimiter after the head tells the type
From 236af273/1, a5587095/8, b675f3d9/10 (placed in ethos on the living's 2026-08-27 ruling).
X.{…} declares a struct, Y.[…] an enum: the delimiter after the head
tells the type. The same mechanism serves wherever several types
share one position — in the signal interfaces and elsewhere.

## A block gives its characters their meaning
From b675f3d9/8.
Ethos parsing depends on the block being parsed: a colon in an
import block is the import form; the same colon in another block
means what that block says. Ethos uses the same thing in different
contexts to mean different things.

## Angle brackets hold kinds
From 6b31eff3/2 (transcript-only), b675f3d9-7.
Angle brackets hold the kinds in a type's positions —
Result<Vector<Sortable> Error> — chosen for token economy and because
it recycles Rust cognition.

## One abstraction up
From aa4c7747/1, f426777b/1.
Ethos is one abstraction up from Rust: our response to all other
programming languages, a higher level of abstraction than any of
them. It gives, in one swoop, the mental model of the machine and the
code for it, where Rust or JavaScript is full of noise — more than
half of the code is noise.

## File and source
From 2b34fafa/2, /3.
The unit of Ethos is the file. A source is what Rust calls a crate.

## What Ethos generates, and where it lives
From 019feb93/1, 01a02fd5/1, f426777b/3.
Ethos generates the Rust for the wire types (signal), the major
internal engine operation types (nexus), and the database types
(sema). Every wire interface is written in Ethos, in the component's
signal repositories. The nexus and sema Ethos, once designed, live in
the component's main repository.

## Kinds are checked at build time
From aa4c7747/8.
Ethos checks at build time that a type carries the kinds it claims.

## The trinity
From 55d18f4f/1.
Ethos, Nomos and Logos are nexuses, each with the architecture of
every other component, all messages signal. Everything is in the
nexus: the Ethos nexus loads the Ethos and holds the whole thing.

Withdrawn from the b675f3d9 draft: "Ethos declares; datom is data"
(Vision/ethos.md "What Ethos is" already says it); "The first scope"
(MVP scope — a working decision; see discards).

---

# Vision/ethosInterfaces.md (new)

## Sections confer
From 5abf3be8/1, 01a03d6e/1.
Sections exist to confer a kind on their items — Input, Output,
Refusal. An item in the input slot is a request by standing there;
the word request is redundant.

## Imperative voice
From 01a03d6e/1, /2.
An interface is designed verb-oriented, in the imperative voice:
list, observe. Commands universal across nexuses — observe above all
— are reused, so that a model can use a nexus it was never trained
on from the primordial commands it already knows.

## Streams
From d63804f2/1, 5abf3be8/2.
A stream is a section inside the object, the fourth kind of section;
its initiation and termination live in the input.

## Imports
From 2b34fafa/6, /7, /8, /4.
Pulling from an external source is explicit: source:Object pulls
Object from the source's lib file; source:[Object Thing] pulls
several; source:file.[Object Thing] pulls from a named file of the
source. The source name resolves through a manifest written in
datom; a name the manifest cannot resolve is an error; a bare path
resolves locally. What exists is an import reference; there is no
Import type. A file has no namespace inside it.

---

# Vision/ethosMonolith.md (revisions)

## Name (addition)
From aa4c7747/2, /4.
Its better name is ethos-zero: version zero, which bootstraps Ethos
into the nexus trinity of Ethos, Nomos and Logos nexuses. Whether
ethos-cc — compiler-compiler — is an accurate name is asked.

## Shape (replaces the first sentence)
From aa4c7747/3.
The monolith is written as a nexus from the start: the things it
deals with are broken down, and the kinds — the ways those things
interact — are isolated and properly named.

Withdrawn from the b675f3d9 draft: "What it generates" (now in
ethos.md); "The trinity it bootstraps" (now ethos.md "The trinity").

---

# Vision/kinds.md (new)

## Kind is the word
From b675f3d9-7, f426777b-11, -13.
In Ethos the word is kind. A kind is what a Rust trait becomes, one
abstraction up: declaring a new kind declares a new trait on the
Rust side and implies things Rust has no word for, still to be
settled. Trait is set aside as acoustically ambiguous in speech.

## A kind is named as a qualifier
From b675f3d9-7, f426777b-14, 6863ef19-6.
A kind is named as a qualifier — Runnable, Writable, Readable. Write
is not a kind.

## Capability
From b675f3d9-8.
A capability is an actual function a kind has: Runnable is the kind,
run is one of its capabilities.

## Interaction
From aa4c7747-10, -11.
An interaction is a kind's implementation on a type. An interaction
uses the type itself; one that does not is no interaction of that
type.

## Concept
From b675f3d9-15 (handwritten page).
A concept is a type or a kind.

## No generics, only kinds
From b675f3d9-7, f426777b-11, no-session-1.
In Ethos there are no generics, only kinds. What Rust writes as a
generic parameter is a kind, and several kinds in one declaration
adjust the emitted Rust.

## Identity
From b675f3d9-10, -11.
As in Rust, a kind is identified by its name and the identity parts
of its data: the kinds in its positions, written in the head —
Processable<[Clonable Sendable] Serializable>.

## Kinds are declared explicitly
From f426777b-2.
A kind is declared, never extracted from its interactions; recovering
what a kind is and how many interactions it has from implementations
would be complex.

## Creation is From
From 2b34fafa-wm3, aa4c7747-21.
Creation is TryFrom or From, called by those names. There is no
Create kind.

## Rust's own traits keep their names (a lean)
From b675f3d9-11.
An existing Rust trait is referred to as Rust names it; a conversion
table would incur a cost.

## Capability forms
From b675f3d9-15 (the handwritten page; the image is authoritative — the transcription is an agent's).
A capability is written as one of several structural forms, and
Capability is a vector-represented enum of them: SingleYield.{Name
Concept}, written Head.Concept; MutableSingleYield.{Name Concept},
written Head!Concept; MultipleYields.{Name Vector<Concept>}, written
Name.[ConceptOne ConceptTwo …]; Standard.{Name Vector<Concept>
Vector<Concept>}, written Head.{[InputOne InputTwo] [OutputOne
OutputTwo]}.

## Finding a kind's declaration
From b675f3d9-9 (its design content; its instruction part is a discard).
A kind's declaration is found from the anatomy of a Rust trait in its
most complex form; a struct is needed to fit it all, or a root enum
to tell kinds of kinds apart.

Withdrawn from the b675f3d9 draft: "Declaration is the first scope"
(MVP scope; see discards).

---

# Vision/anatomy.md (new)

## The map before the code
From 2b34fafa-27, -28, 15b67974-22.
An agent that writes code before it has a model of the world has
already failed; catching a fake kind afterwards is too late. The
work is building a map of what is being made — its ontology, its
anatomy, an object- and capability-oriented layout. The map is the
Ethos interface file. Old code is at most inspiration for the map.

## Ontology is designed before it is implemented
From e06e4c07-16, ba906ae2-1, e06e4c07-13.
Every behaviour falls under a kind, which creates an ontology in
code. Placeholder kinds for every function make no sensible ontology;
an ontology is designed before it is implemented, and agents are
trained and given a workflow for it. The universal nexus kinds are
the basic ontology of an actor/dataflow software system.

## Types first
From psyraw-6863ef19.
Types are thought through first; kinds are what types implement.

## Costume kinds
From 2b34fafa-30.
A kind whose capabilities are ordinary functions pretending to be a
kind misses the approach; this is a cornerstone of models'
misunderstanding of the vision.

## The three-part machine
From 2b34fafa-23, -24.
A machine agglomerates several types, creates one coherent type from
them, and converts it to another type. That is one form of it — the
machine may be accumulating variables in a method's body — and no
single form is invested in.

## From over Into
From 2b34fafa-25.
Things are created from other things; nothing is harvested and then
asked what it can be made into. Everything is demand-driven, so From
is better than Into.

## Processing is for the effect
From f426777b-1, -3.
When an object enters a nexus, the point is the effect; the response
comes as an effect of that. TryFrom is doubted as the way to think
of processing; Apply is liked, uncertain, and a new terminology is
needed.

Withdrawn from the b675f3d9 draft: "Sections confer" (in
ethosInterfaces.md); "A spoken vocabulary" (own topic below).

---

# Vision/spokenVocabulary.md (new)

## A spoken vocabulary for software engineering
From aa4c7747-3, f426777b-12.
Programming was never done in speech. A spoken vocabulary for
software engineering is being created — a way to speak it at a
higher, more correct layer of abstraction; it may be called logic
engineering.

# Vision/rustConventions.md (new)

## Tuples
From aa4c7747-14.
There is no tuple in the code we design; where a standard trait or a
dependency requires one, it is allowed at that contact point only.

---

# Graduation and Intent questions
- "Logic planes" (protos): Intent?
- "easy cognition is the first safe bet" (2b34fafa/1): a principle
  worth Intent, or a monolith working decision (discard)?
- psyche-raw/Intent/mandatoryTraits.md carries a psyche-approved
  wording; does it enter Intent/mandatoryTraits.md as it stands?

# Tensions
- ethos-cc: asked as a name by the psyche, never answered.
- Effect verb: Apply liked, uncertain; "we need a new terminology".
- The word for a kind's declaration itself (still "trait declaration"
  in operational use).

# Discards this round (impurities, dissected; the living's ruling asked)
- aa4c7747/6 "When I said traits I just meant trait declaration.
  Implementation would be a big job … not MVP sounding anymore." —
  MVP scope decision.
- 2b34fafa/1 "for the monolith thats good enough. easy cognition is
  the first safe bet." — unless graduated (above).
- 5abf3be8/2, the clauses "not now … for now we could just … write it
  all by hand and wire it up … getting to minimum viable product" —
  working plan; the stream-as-fourth-kind words are kept.
- aa4c7747-18 "And so we need to define what the trait syntax for
  Ethos is" — task.
- 2b34fafa-30, the clause "Do a research in this" — instruction.
- b675f3d9-9, the instruction clauses ("So start by looking at … doing
  the anatomy …") — the design content is kept in "Finding a kind's
  declaration".
- 2b34fafa-29 "we still need to establish the protocol for create the
  anatomy of a well designed object and capabilities oriented
  machine." — task.
- a5587095/11 "the intent is good" — approval; a5587095/7's "Lets
  flesh it out in detail with examples" — instruction (its "the parse
  is two-way … must become our design pattern" is Intent content,
  kept in place).
- 6863ef19/1, the clause "lets look at an update to the skills, and
  reconsider traits as 'capabilities'. Rethink the whole concept over
  and represent it this way" — instruction.
- ac1e9ec8/5 "Is there a scenario in which a Head. isnt a variant?" —
  a question.
- aa4c7747/8 "I approve your trait implementation checking mechanism."
  — an approval that carries the ruling; proposed ARCHIVED (it is the
  only record of the mechanism), not destroyed.

Superseded records (archived, not destroyed): 2b34fafa/5 (import
fallback), d63804f2/2 ('/' for imports), 2b34fafa-31 (infinitive),
06196cc7-20/21 (verbs), 5abf3be8/3 (encoded form), f426777b/2 (sema
and nexus in the signal repos), a5587095/3–4 and 06196cc7/6 (paren
strings, bracket map), 6863ef19/1 (capabilities as the trait word).

## Sources
- flows/b675f3d9/reports/distillCandidatesProtosDatom.md
- flows/b675f3d9/reports/distillCandidatesEthos.md
- flows/b675f3d9/reports/distillCandidatesKinds.md
- flows/b675f3d9/reports/distillProposal{ProtosDatom,Ethos,Kinds}.md
- flows/b675f3d9/vision/distillation.md (placement ruling)
- flows/acbb6006/vision/distillation.md, nexus.md, approval.md
