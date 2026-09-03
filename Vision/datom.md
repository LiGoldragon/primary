# Datom

## Name

Datom is the psyche’s own coinage for the new data notation, the
successor to NOTA and to the rejected name Dotos. The name was
chosen for its energetic power and to echo what the notation is:
data, strictly typed, super dense, no field names.

## Nature

Datom is the most advanced textual data format in the world. It
carries data, strictly typed, and its whole work is serialization and
deserialization: carrying data between text and typed form. Datom is
signal's form at the edge: our components speak signal, and datom lets
text-based systems, LLMs and every existing editor, read and write it.
Datom is a kind, not a type, since it has no definite shape; the kind
is Datomic. Generating Rust is Ethos's duty, in today's division of
labor. When Ethos becomes the full authoring language, with Rustlang
as its assembly layer, Datom, the data dialect of the Protos family,
may gain an inline place in authored Ethos, the way Rustlang composes
data directly in code. That road is reached, or even floated, only
with explicit context: how, when, and where data yields Rust, stated
without ambiguity; until then the division stands as spoken.

## Repository and migration

Everything migrates to Datom, and no Dotos file remains. Datom's own
line of descent is NOTA, which also passed through the temporary name
Dotos; that old notation stays behind, frozen, and may be called
legacy. Schema is the abandoned ancestor of Ethos, not of Datom. Datom
is a library for now, and the library takes another name so that datom
is free for the datom nexus, which comes when there is more to do:
translating datom objects between formats, and a parsing cache keyed
by the content-addressed hash of normalized Text.

## The interface shape

A program's configuration surface is the datom's shape itself, as the
ethos interface declares it: a data enum at the root whose variants
are the main operations. A variant's data carries what follows:
another enum where sub-operations are wanted, a struct or vector for
final options, and a struct may embed further sub-operations, or any
combination imaginable. Output is an enum, always; even the most basic
response interface is an enum: Success or Failure. The shape already
is the interface: datom creates the configuration options by its very
shape, and a CLI takes its whole configuration from its datom input. A
Nexus reply is written as its heads down to its data, and only what
carries data is written: an empty Locks observation is
Observed.Locks.[], the Observed variant, its Locks variant, the empty
vector; the layout of a nonempty payload is open.

```
; datom, each in a position expecting the response enum named in the comment
Observed.Locks.[]    ; orchestrate's response: the Observed variant, its Locks variant, the empty vector
Success              ; the most basic response: a variant carrying nothing
```

## De/serialization

Schema-driven and positional: the reader walks the expected type,
writing is the exact reverse projection, and decoding lands directly
in the typed Rust structs. A datom on the way in is a potential datom,
untrusted until it matches its type; on the way out it is a datom. All
naming and self-description live in the type; the text carries only
the data.

```
; datom, in a position expecting Scores: a struct of name Text, values Vector<Integer>.
; The reader walks the type: first position a string, second a vector of integers. The text carries only the data.
{ Ada [ 12 7 -3 ] }
```

## Relation to Ethos

Datom and Ethos are different languages that share an approach, not a
parser. What they may share is a substrate, kinds with a shared
implementation and types; the universal substrate machinery is homed
in protos, all dialects ride it, and datom is the pure-data dialect on
it. Ethos could come to depend on Datom for another reason: ethos
might be read as datom in one pass. Whether that is even possible,
given the situation and the actualization involved in parsing ethos,
is not settled, and the question is set aside for now.

## Syntax

Structure is the word for every unit of the text: enclosed when it
stands between its delimiters, unenclosed when bare. A headed
structure is a head, a separator and a body; the dot is the separator,
written right after the head, and it opens the body's delimiter. A
head is a symbol, a qualified string; the rule that qualifies a string
as a symbol is not yet stated. In datom a head is always a variant, so
it is capitalized. Which head a structure carries is part of its type:
`Accepted.{ … }` and `Refused.{ … }` are two types. When an enum value
is textualized, its variant's name is written as the head every time,
a variant carrying nothing included: `Pending`, never an empty
structure. A brace structure is a struct and a bracket structure is a
vector. A head in front of a structure makes a variant that carries
it: `Reviewer.{ 2024 17 }` is the Reviewer variant carrying a struct
of two positions, and `Observed.Locks.[]` is the Observed variant
carrying the Locks variant carrying an empty vector. A symbol alone,
in a position expecting an enum, is a variant carrying nothing. A
datom is not preceded by a Datom root; a comment may say it is datom.
Curly quotes are the string delimiter, and parentheses are reserved
for Meaning. A string is a string only in a position where the type
defines a string. In such a position a string is written as one bare
word when it contains no space and no delimiter, Ada, 75002,
2026-09-03; any other string is written in curly quotes. Because the
position already knows it holds a string, a bare word may contain
characters that are syntax elsewhere, the colon among them; the
machinery is made fit for this by the right abstraction layers. A
quoted string is opaque: every delimiter inside it is content until
the closing quote. Guillemets delimit a map; inside, key and value are
separated by a space, resolving by position. A map in a position that
expects a map carries no head, since the position already knows its
type; a head is thereby always a variant. An integer is written as
bare decimal, 0, 42, -42: ASCII digits, no leading plus, no leading
zero except 0 itself. A single semicolon opens a comment. Canonical
text leaves a space inside every bracket and brace delimiter, at both
ends, so that head, dot, delimiter and content read apart, and never
inside curly quotes, where a space is content.

```
; datom, in a position expecting Person: a struct of name Text, born Integer, address Address, roles Vector<Role>.
; Each comment names the structure that starts on its line. Indentation shows which structure holds which.
{                                        ; the whole Person is one structure, enclosed by braces: a struct. It holds four structures.
  Ada                                    ;   unenclosed, a bare word. The position says Text, so it is a string.
  1990                                   ;   unenclosed. The position says Integer.
  { “12 Rue de la Paix” Paris 75002 }    ;   enclosed by braces: a struct, the Address. It holds three structures:
                                         ;     one enclosed by curly quotes, opaque, and two unenclosed.
  [ Author                               ;   enclosed by brackets: a vector of Role. It holds two structures:
    Reviewer.{ 2024 17 } ]               ;     a symbol alone, the Author variant carrying nothing, and a headed structure:
}                                        ;     head Reviewer, the dot, and a body that is itself a struct of two unenclosed structures.
                                         ; The closing brace ends the outermost structure, the Person itself.
```

The whole is a structure, and so is every part of it, down to the
unenclosed ones, which hold nothing. What a structure means, struct,
vector, string, integer, variant, is said by the position it sits in,
never by the structure alone.

```
; Reply: an enum of Accepted.{ id Integer  at Text }, Refused.{ reason Text  code Integer }, Pending
Accepted.{ 42 2026-09-03T17:46:20 }         ; the timestamp has no space and no delimiter, so it is bare
Refused.{ “no such file: { } is content” 2 } ; quoted: the string has spaces and braces; inside the quotes they are content
Pending                                      ; a variant carrying nothing

; a map of Text to Address
« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »

; a map of Text to Integer
« name:first Ada  born 1990 »               ; the colon inside a bare word is content: the position holds a string

; a vector of Integer
[ 0 42 -42 ]
```

## Meaning

Meaning is the structured string: parenthesis-delimited, arbitrary
depth, a graph of sorts, seeded by the fact that parentheses inside
text are markup. Curly quotes delimit the plain string. Meaning is
postponed so a working syntax lands as soon as possible: parenthesis
text lands as plain String today, the later type marked in code. The
name Meaning is provisional — it smells of a verb — and is reopened
together with the type.
