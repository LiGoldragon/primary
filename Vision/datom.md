# Datom

## Name

Datom is the psyche's own coinage for the new data notation, the
successor to NOTA and to the rejected name Dotos. The name was
chosen for its energetic power and to echo what the notation is:
data, strictly typed, super dense, no field names.

## Nature

Datom carries data only — like JSON, but strictly typed. Generics
belong to Ethos; Datom's whole work is serialization and
deserialization — carrying data between text and typed form.
Generating Rust is Ethos's duty, in today's division of labor. When
Ethos becomes the full authoring language, with Rustlang as its
assembly layer, Datom — the data dialect of the Protos family — may
gain an inline place in authored Ethos, the way Rustlang composes
data directly in code. That road is reached, or even floated, only
with explicit context: how, when, and where data yields Rust, stated
without ambiguity; until then the division stands as spoken.

## De/serialization

Schema-driven and positional: the reader walks the expected type,
writing is the exact reverse projection, and decoding lands directly
in the typed Rust structs. All naming and self-description live in
the type; the text carries only the data.

## Repository and migration

Everything migrates to Datom. Datom's own line of descent is NOTA —
which also passed through the temporary name Dotos; that old
notation stays behind, frozen, and may be called legacy. Schema is
the abandoned ancestor of Ethos, not of Datom. The repository is
plain datom, with no variant suffix.

## Relation to Ethos

Datom and Ethos are different languages that share an approach, not
a parser. What they may share is a substrate — traits with a shared
implementation and types; the universal substrate machinery is homed
in protos, all dialects ride it, and datom is the pure-data dialect
on it. Ethos depends on Datom, at minimum to intake data for
signals; the Meaning context therefore lives in the datom
repository, seen by both languages.

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

## Syntax

Consistency comes first: datom's syntax is fixed before the rest.
Parentheses carry a duty — they are a major symbol of cognition —
and are the default string delimiter, balance-based: interior
balanced pairs are plain content (parentheses inside text are
markup, the seed of the structured string), the string closes at the
final unbalanced closer, and an unbalanced interior parenthesis is
escaped. A string is written bare whenever the bare form can carry
it, and a bare string may carry symbols that are load-bearing
elsewhere — the machinery is made fit for this by the right
abstraction layers. String blocks are opaque: interior delimiters
become content until the block closes. A bare brace block is a
struct; a dot-parenthesis block is a string-carrying variant. The
dotted prefix of a delimited block is part of the block's type; its
official name is Head; a variant always re-emits its Head when
textualized. A map's payload is a square-bracket vector of key.value
entries, since a map is conceptually a list of key/values.

## Meaning

The structured super-string type, Meaning, is postponed so a working
syntax lands as soon as possible: parenthesis-delimited and
curly-quote text both land as plain String for now, with the later
Meaning type marked in code. The eventual shape is one string type
with two variants — legacy (curly quotes) and structured
(parentheses, arbitrary depth, a graph of sorts).
