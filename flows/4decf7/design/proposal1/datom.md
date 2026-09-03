# Datom

## Name

Datom is the psyche's own coinage for the new data notation, the
successor to NOTA and to the rejected name Dotos. The name was
chosen for its energetic power and to echo what the notation is:
data, strictly typed, super dense, no field names.

## Nature

Datom is the most advanced textual data format in the world. It
carries data, strictly typed, and its whole work is serialization and
deserialization: carrying data between text and typed form. Datom is
signal's form at the edge: our components speak signal, and datom
lets text-based systems, LLMs and every existing editor, read and
write it. Datom is a kind, not a type, since it has no definite
shape; the kind is Datomic. Generating Rust is Ethos's duty, in
today's division of labor. When Ethos becomes the full authoring
language, with Rustlang as its assembly layer, Datom, the data
dialect of the Protos family, may gain an inline place in authored
Ethos, the way Rustlang composes data directly in code. That road is
reached, or even floated, only with explicit context: how, when, and
where data yields Rust, stated without ambiguity; until then the
division stands as spoken.

## De/serialization

Schema-driven and positional: the reader walks the expected type,
writing is the exact reverse projection, and decoding lands directly
in the typed Rust structs. A datom on the way in is a potential
datom, untrusted until it matches its type; on the way out it is a
datom. All naming and self-description live in the type; the text
carries only the data.

## Repository and migration

Everything migrates to Datom, and no Dotos file remains. Datom's own
line of descent is NOTA, which also passed through the temporary
name Dotos; that old notation stays behind, frozen, and may be
called legacy. Schema is the abandoned ancestor of Ethos, not of
Datom. Datom is a library for now, and the library takes another
name so that datom is free for the datom nexus, which comes when
there is more to do: translating datom objects between formats, and
a parsing cache keyed by the content-addressed hash of normalized
Text.

## Relation to Ethos

Datom and Ethos are different languages that share an approach, not
a parser. What they may share is a substrate, kinds with a shared
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
vector for final options, and a struct may embed further
sub-operations, or any combination imaginable. Output is an enum,
always; even the most basic response interface is an enum: Success
or Failure. The shape already is the interface: datom creates the
configuration options by its very shape, and a CLI takes its whole
configuration from its datom input. A Nexus reply is written as its
heads down to its data, and only what carries data is written: an
empty Locks observation is Observed.Locks.[], the Observed variant,
its Locks variant, the empty vector; the layout of a nonempty payload
is open.

## Syntax

The dot opens a delimiter: a Head is bare text ending in a dot,
written immediately before the block it opens; the Head is part of
the block's type, and a variant always re-emits its Head when
textualized. A bare brace block is a struct. A datom is not preceded
by a Datom root; a comment may say it is datom. Curly quotes are the
string delimiter, and parentheses are reserved for Meaning. A string
is a string only in a position where the type defines a string;
there it is written bare whenever the bare form can carry it, and a
bare string may carry symbols that are load-bearing elsewhere, the
colon among them, the machinery made fit for this by the right
abstraction layers. String blocks are opaque: interior delimiters
become content until the block closes. Guillemets delimit a map;
inside, key and value are separated by a space, resolving by
position. A map in a position that expects a map carries no Head,
since the position already knows its type; a Head is thereby always
a variant. An integer is written as bare decimal, 0, 42, -42: ASCII
digits, no leading plus, no leading zero except 0 itself. A single
semicolon opens a comment. Canonical text leaves a space inside every
bracket and brace delimiter, at both ends, so that head, dot,
delimiter and content read apart, and never inside curly quotes,
where a space is content.

## Meaning

Meaning is the structured string: parenthesis-delimited, arbitrary
depth, a graph of sorts, seeded by the fact that parentheses inside
text are markup. The aim is the most advanced structured meaning
system ever made, exposing the emphasis and the other structure a
plain string lacks; annotations are enums used throughout the tree,
Emphasis among them. Curly quotes delimit the plain string. Meaning
is postponed so a working syntax lands as soon as possible:
parenthesis text lands as plain String today, the later type marked
in code. The name Meaning is provisional, it smells of a verb, and is
reopened together with the type.
