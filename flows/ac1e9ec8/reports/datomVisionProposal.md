# Datom — proposed full vision (third draft)

The complete `Vision/datom.md` as this flow proposes it after the
living's corrections to the first draft. Every sentence was split
into its single claims, each checked to stand alone and read one way,
then re-assembled. Lands only on approval.

---

# Datom

## Name

Datom is the most advanced textual data format in the world: data,
strictly typed, super dense. The name was chosen for its energetic
power. Datom descends from NOTA, which also carried the temporary
name Dotos.

## Nature

Datom carries data, strictly typed. Components speak signal; datom
is signal's textual form at the edge, where text-based systems —
LLMs and existing editors — read and write what components exchange.
Its whole work is serialization and deserialization: carrying data
between text and typed form.

## Reading and writing

A datom text is read against a type and written from one. The type
is declared outside the text: in Rust today, in the Ethos interface
as it lands.

The type fixes what every position expects: a string; a struct, with
its fields in a fixed order; a vector of one element type; a map of
one key type to one value type; or an enum of named variants, each
with its own payload type.

Reading walks the type. Each position in the text is read as the type
expected there, and the value lands directly in the typed value.
Writing is the same walk in reverse: the typed value projects back
into the same text.

Field names live in the type alone. The text carries a struct's
fields in the type's order and spells no field name.

A variant's name is written in the text, because which variant is
present is data.

## Syntax

Every form is read in a position, and the position's type decides
what the form is.

Where the type expects a string:

- The string is written bare — without delimiters — whenever the
  bare form can carry it.
- Bare text is a string only where the type expects a string. The
  same bare text in an enum position is a variant name.
- Because the position already says string, a bare string may carry
  symbols that are load-bearing elsewhere; the machinery is made fit
  for this by the right abstraction layers.
- Otherwise curly quotes delimit the string: `“ … ”`. Curly quotes
  are the default string delimiter.
- A string block is opaque: interior delimiters are content until the
  block closes.

Where the type expects a struct: `{ … }`, holding the fields in the
type's order.

Where the type expects a vector: `[ … ]`, holding the elements in
order.

Where the type expects a map: `« … »`, holding key, value, key,
value, resolving by position. A map is a list of key/values.
Guillemets are the map's own delimiter, so a map is easy to spot.

Where the type expects an enum: the variant's name. A variant with
payload writes its name, a dot, and the payload in the payload's own
form: `Variant.{…}`, `Variant.[…]`, `Variant.«…»`, `Variant.(…)`.
The dot opens the delimiter. The name before the dot is the Head;
the Head is part of the block's type, and a Head is always a variant.
A textualized variant re-emits its Head.

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

Parentheses are reserved for the structured string, Meaning, still
to be designed. Parentheses carry a duty — they are a major symbol of
cognition — and parentheses inside text are already markup, which is
the seed of the design: a structured string reads balance-based,
interior balanced pairs being content and the string closing at the
final unbalanced closer, to arbitrary depth, a graph of sorts. One
string type carries both forms: plain (curly quotes) and structured
(parentheses). The name Meaning is provisional — it smells of a
verb — and is reopened together with the type.

## Repository and migration

The repository is plain datom. NOTA stays behind, frozen, as legacy.

## Relation to Ethos

Datom and Ethos share an approach and a substrate: traits with a
shared implementation and types, homed in protos. All dialects ride
that substrate, and datom is the pure-data dialect on it.

Ethos depends on Datom, at minimum to intake data for signals; the
Meaning context therefore lives in the datom repository, seen by both
languages.

Datom may one day be embedded in Ethos positions, and the two
syntaxes stay compatible for that: angle brackets are Ethos's,
guillemets are datom's map.

## Archive

The raw records this vision distills, retired forms included: the
`archive-datomSyntax` and `archive-threeStacks` files in
`psyche-raw/Vision/` and in the flows that heard them.

---

## Sources

- `Vision/datom.md` (current)
- `flows/ac1e9ec8/vision/datomSyntax.md`, `datomIsData.md`,
  `distillationNegatives.md`
- `flows/ac1e9ec8/witnesses/datomCurrentSyntax.md` (implementation
  divergences noted in log)
