# Distillation proposal: Vision/protos.md (new) and Vision/datom.md (revision)

Composed in flow b675f3d9 from reports/distillCandidatesProtosDatom.md,
continuing ac1e9ec8's second cut (reports/datomSyntaxDistillationProposal.md)
and the corrections the living gave that flow: no negatives, no
"like JSON", no apology, understand then explain, one claim per
sentence, datom is data. Each statement lands only on the living's
explicit approval.

---

# Vision/protos.md (proposed, new)

Destination: Vision/protos.md. Each `##` below is one statement
heading in that file. Ethos-specific sentences were moved out on the
living's correction (2026-08-27) to the Vision/ethos.md additions
listed at the end of this proposal.

# Protos

## The shared style

Protos is the style all our dialects share. Ethos, Datom, Nomos and
Logos are protos dialects. The fully decomposed engine — three
daemons — is the protos engine; Datom sits beside it as the dialect
for pure typed data.

## Everything is data

A dot opens a delimiter, and everything written is data. The textual
form of a thing is itself data, and so a type.

## One representation

A type has exactly one protos representation.

## Parsing in context

Parsing always happens in a context; the context changes, it never
suspends. The current context says which shapes may come next and
which shape completes it; a met shape announces a type, whose context
takes over until its completing shape, and then the parent resumes
exactly where it left off. A character has no meaning of its own; the
block being parsed gives it one, and a character is free in every
block that has not yet given it a meaning.

## Shape in context tells the type

Within its parsing context, a block's shape tells its type. The
shape is: whether the block opens with a head at all; the character
between the head and the body; the delimiter of the body; the number
of components inside. A block need not start with a head — a bare
brace block or a bare bracket block stands in a position whose
context already knows its type — and where a head is present, its
mere presence can be what conveys the type. Several types may share
one position when their shapes differ; the shape is then what tells
them apart. Structures of different size are different types. The
character between a head and its body adds a type distinction for
the cost of one character.

## Struct and vector

A struct is one fixed shape: the same fields in the same order, each
field's type declared, any type allowed in any field. A vector is the
one variable-length form, and all its components share one type or
one kind.

## Angle brackets

Angle brackets are a protos delimiter. Datom and Ethos keep angle
brackets compatible, so that datom can one day be embedded in ethos
positions.

## Forms of a value

A value has a real form, the typed value inside the program; a
signal form, its bytes on the wire; and a textual form. Realize reads
the textual form into the real form and Textualize writes it back:
one walk in two directions. The words working, code, encoded and
transcodable are retired.

## Shape-defined types

A protos type is implemented as a match over the standard shapes,
each shape carrying its own parsing context; a complex type is a
vector of shapes. ShapeDefined names this.

## Logic planes

A big implementation is the sign of a missing logic plane. Every part
stays simple; the complexity lives in the totality.

---

# Vision/datom.md (proposed revision — only the changed sections)

## Nature  (replaces the current section)

Datom is the most advanced textual data format in the world. It
carries data, strictly typed, and its whole work is carrying data
between text and typed form. Datom is signal's form at the edge: our
components speak signal, and datom lets text-based systems — LLMs and
every existing editor — read and write it.

[The current paragraph on Datom's possible inline place in authored
Ethos stands unchanged.]

## Syntax  (replaces the current section)

The dot opens a delimiter: a Head is bare text ending in a dot,
written immediately before the block it opens. The Head is part of
the block's type, and a variant re-emits its Head when textualized. A
bare brace block is a struct.

Curly quotes are the string delimiter. Parentheses are reserved for
structured strings — the type currently designated Meaning, still to
be designed. A string is a string only in a position where the type
defines a string; there it is written bare whenever the bare form can
carry it, and a bare string may carry symbols that are load-bearing
elsewhere, the machinery made fit for this by the right abstraction
layers. A string block is opaque: interior delimiters are content
until the block closes.

A map is delimited by guillemets, and its entries resolve by
position: key, value, key, value. A position expecting a map carries
no Map head, since the position already knows its type; a Head is
thereby always a variant.

An integer is written as bare decimal — 0, 42, -42: ASCII digits, no
leading plus, no leading zero except 0 itself.

## Repository and migration  (addition)

No Dotos files remain.

## Meaning  (addition)

The name Meaning is provisional — it smells of a verb — and is
reopened together with the type.

## Open  (new section)

Floats and dotted numbers; comments; newlines and indentation; absent
values; what a dot-parenthesis block is now that parentheses belong
to Meaning.

---

# Vision/ethos.md (proposed additions, moved here from the protos draft)

Destination: Vision/ethos.md. Each `##` is one statement heading.

## Type declarations

In an Ethos type declaration the delimiter after the head tells the
type: `X.{…}` declares a struct, `Y.[…]` an enum, `Z.Word` a typedef.
The same mechanism serves wherever several types share one position —
the section of an interface, the capabilities of a kind.

## A block gives its characters their meaning

In Ethos a character means what the block being parsed says it
means: a colon in an import block is the import form; in a block of
capabilities it is free to mean what that block says.

## Angle brackets hold kinds

In Ethos, angle brackets hold the kinds standing in a type's or a
kind's positions — Vector<Ordered>, Result<Vector<Sortable> Error> —
a form chosen for token economy and because it recycles Rust
cognition.

---

## Surfaced, not distilled

- Imports: the 2026-08-07 ruling is `/` for imports, colon keeping
  one meaning; the living fixtures write imports with a colon
  (`signal_standard:lib.[…]`), and the living said this week that
  colon is currently the import form "in the current vision". Which
  stands?
- The 2026-08-04 angle-bracket words (`Result<Vector<Sortable>
  Error>`) and 2026-08-03 head-convention words are transcript-only;
  they are carried into Vision/protos.md above rather than into a
  raw file.

## Sources

- flows/b675f3d9/reports/distillCandidatesProtosDatom.md (record ids)
- flows/ac1e9ec8/reports/datomSyntaxDistillationProposal.md
- flows/ac1e9ec8/vision/datomSyntax.md, datomIsData.md
- flows/01a03eda/vision/datomInteger.md
- psyche-raw/Intent/protosParsing.md
- psyche-raw/Vision/colonConfusion.md
