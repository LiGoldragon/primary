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
the closing quote. An integer is written as bare decimal, 0, 42, -42:
ASCII digits, no leading plus, no leading zero except 0 itself. A
single semicolon opens a comment. Canonical text leaves a space inside
every bracket and brace delimiter, at both ends, so that head, dot,
delimiter and content read apart, and never inside curly quotes, where
a space is content.

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

; a vector of Integer
[ 0 42 -42 ]
```

## Map

A map is a container whose keys are known only from the data: the
reader learns the shape by reading, where a struct's shape is known
before reading. Datom is typed from the position down: a position
knows its type before the text is read, and a container that reveals
its shape only in the text contradicts that. So datom has no map. Most
of what is called a map is not one: an object with fixed fields, a
configuration table, a record written as a dictionary. These are
structs whose notation declined to declare their fields, and every
such notation ends up adding a way to declare them; that the word
covers so much that is not a map shows how little a map is actually
used. The map that remains, its keys minted at run time and its values
all of one type, is a vector of structs, which is how the typed data
formats already write it; that keys do not repeat is a rule the type
states. What a map would hold is a struct when its keys are fixed, and
a vector of structs when they are not. Datom does not implement a
thing because it has been standard in the past.

## Meaning

Meaning is the structured string: text that carries, besides its
words, the emphasis and the other structural aspects a plain string
simply lacks, an annotated string, meant to revolutionize the
performance of thinking machines on text. The aim is the most
advanced structured meaning system ever made. Parentheses are a
major symbol of cognition, and in datom they have one duty: the
parenthesis pair is the Meaning delimiter, as the curly quotes are
the plain string's. The seed of the design is that parentheses
inside ordinary text are already markup, so a Meaning is read by
balance: a parenthesis pair inside it is structure of its own,
nesting to arbitrary depth, a graph of sorts, and the Meaning closes
at the parenthesis that balances the one that opened it; an
unbalanced parenthesis inside it is escaped. Opening a Meaning makes
the whole delimiter and structure spectrum available inside it,
until the closing parenthesis restores the outer context. Its
annotations are enums used throughout the tree, Emphasis among them;
its shape is still open. Meaning is datom. Strings are strings and
Meaning is Meaning: a position of type String expects a plain string
and nothing else, and a position of type Meaning expects a Meaning.
Meaning is postponed so that a working syntax lands as soon as
possible: today a parenthesized text lands as a plain String, with
the later type marked in code. The name Meaning smells of a verb; it
stands provisionally and is reopened together with the type.

```
; datom, in a position expecting Note: a struct of author Text, body Meaning.
; The first position expects a string: Ada has no space and no delimiter, so it is bare.
; The second position expects a Meaning, so the parenthesis opens it and it is read by balance:
; the inner pair is structure inside the Meaning, and the parenthesis that balances the opening one ends it.
; Today the whole parenthesized text lands as a plain String; what the inner pair will mean is not yet designed.
{ Ada (The build passed on the third try (after two timeouts)) }

; datom, in a position expecting Remark: a struct of author Text, body Text.
; The second position expects a plain string; it has spaces, so it is quoted,
; and the parentheses inside the quotes are content, not a Meaning.
{ Ada “The build passed on the third try (after two timeouts)” }

; datom, in a position expecting Standup: a struct of team Text, items Vector<Meaning>.
; Each component of the vector is one Meaning; each is read by balance on its own.
{ Backend
  [ (Ada fixed the flaky test (the one with the timeout))
    (Bo is out (back Monday)) ] }
```
