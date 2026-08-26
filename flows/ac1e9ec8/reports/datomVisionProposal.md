# Datom — proposed full vision

The complete `Vision/datom.md` as this flow proposes it, for the
living's review. Lands only on approval. Positive statements only;
retired forms live in the linked archives.

---

# Datom

## Name

Datom is the psyche's own coinage for the data notation, the
successor to NOTA, which also passed through the temporary name
Dotos. The name was chosen for its energetic power and to echo what
the notation is: data, strictly typed, super dense, no field names.

## Nature

Datom carries data only — like JSON, strictly typed. Its whole work
is serialization and deserialization: carrying data between text and
typed form. Generics and Rust generation belong to Ethos. When Ethos
becomes the full authoring language, with Rust as its assembly layer,
Datom — the data dialect of the Protos family — may gain an inline
place in authored Ethos, the way Rust composes data directly in code;
that road is taken with its how, when, and where stated explicitly.

## De/serialization

Schema-driven and positional: the reader walks the expected type,
writing is the exact reverse projection, and decoding lands directly
in the typed structs. All naming and self-description live in the
type; the text carries only the data.

## Syntax

Consistency comes first: datom's syntax is fixed before the rest.
Each delimiter shows its container's kind, so a reader sees the
shape of the data without the type in front of them.

- **bare** — a string written without delimiters; the default. A
  string is written bare whenever the bare form can carry it, and a
  bare string may carry symbols that are load-bearing elsewhere; the
  machinery is made fit for this by the right abstraction layers.
- **( … )** — a string. Parentheses carry a duty — they are a major
  symbol of cognition — and are the default string delimiter,
  balance-based: interior balanced pairs are plain content
  (parentheses inside text are markup, the seed of the structured
  string), the string closes at the final unbalanced closer, and an
  unbalanced interior parenthesis is escaped. String blocks are
  opaque: interior delimiters become content until the block closes.
- **{ … }** — a struct: its fields, in order.
- **[ … ]** — a vector: its elements, in order.
- **« … »** — a map: key, value, key, value, resolving by position.
  A map is a list of key/values, and its own delimiter makes it easy
  to spot.
- **Head.** — a dotted prefix glued to the delimiter it opens: the dot
  opens the delimiter, and the prefix is part of the block's type.
  Its official name is Head. A Head is always a variant:
  `Variant.{…}`, `Variant.(…)`, `Variant.[…]`, `Variant.«…»`, or
  the bare `Variant` alone. A variant always re-emits its Head when
  textualized.

A request is a root variant carrying its Head.

## The interface shape

A program's configuration surface is the datom's shape itself, as
the ethos interface declares it: a data enum at the root whose
variants are the main operations. A variant's data carries what
follows: another enum where sub-operations are wanted, a struct or
vector for final options — and a struct may embed further
sub-operations, or any combination imaginable. Output is an enum,
always — even the most basic response interface is an enum: Success
or Failure. The shape already is the interface: datom creates the
configuration options by its very shape.

## Meaning

The structured super-string type, Meaning, is postponed so a working
syntax lands as soon as possible: parenthesis-delimited and
curly-quote text both land as plain String for now, with the later
type marked in code. The eventual shape is one string type with two
variants — legacy (curly quotes) and structured (parentheses,
arbitrary depth, a graph of sorts). The name Meaning is provisional —
it smells of a verb — and is reopened together with the type.

## Repository and migration

Everything is datom: every data file and every wire message. Datom's
line of descent is NOTA, which also carried the temporary name Dotos;
that notation stays behind, frozen, as legacy. The repository is
plain datom.

## Relation to Ethos

Datom and Ethos are different languages that share an approach and a
substrate — traits with a shared implementation and types. The
universal substrate machinery is homed in protos; all dialects ride
it, and datom is the pure-data dialect on it. Ethos depends on Datom,
at minimum to intake data for signals; the Meaning context therefore
lives in the datom repository, seen by both languages.

## Archive

The raw records this vision distills, retired forms included:

- `psyche-raw/Vision/archive-datomSyntax.md`
- `psyche-raw/Vision/archive-threeStacks.md`
- `flows/06196cc7/vision/archive-datomSyntax.md`
- `flows/a5587095/vision/archive-datomSyntax.md`
- `flows/ac1e9ec8/vision/archive-datomSyntax.md`

---

## Sources

- `Vision/datom.md` (current)
- `flows/ac1e9ec8/vision/datomSyntax.md`, `datomIsData.md`,
  `distillationNegatives.md`
- `flows/ac1e9ec8/reports/datomSyntaxDistillationProposal.md`
