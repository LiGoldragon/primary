# Bytes in ethos

## Context

A hash is bytes. A Blake3 hash is 256 bits, 32
bytes. Ethos has no type that holds bytes: the
intrinsic names in vision/ethos.md are String,
Integer, Decimal, Boolean, Meaning, Vector, Option,
Result and Self, with no Byte and no byte array.
So a design that stores a hash must stand it in as
something else, and each stand-in loses what the
hash is.

```
┌────────────────────────────────────┐
│ a hash in memory                   │
│ 32 bytes, a vector of bytes        │
└─────────────────┬──────────────────┘
                  │ lost: the bytes are
                  │ no longer one value
                  ▼
┌────────────────────────────────────┐
│ the ethos type today               │
│ four Integers, signed, in an order │
│ chosen by hand                     │
│ or a hex String of 64 characters   │
└─────────────────┬──────────────────┘
                  │ lost: the String says
                  │ text, not bytes; any
                  │ text fits it
                  ▼
┌────────────────────────────────────┐
│ datom                              │
│ an alphanumeric encoding           │
│ the only form the text needs       │
└────────────────────────────────────┘
```

The Source nexus design in flow 058f16, section
"Shared sources library", stores a Blake3 hash for
every source and drafts it as
`Blake3.{ Integer Integer Integer Integer }`, a
stand-in that names the missing byte array as its
reason. Your record on hashes,
flows/d4ae97/vision/datom.md, 2026-10-07, "Stored
type and datom representation; shorthands; the flow
id as three words", names the type in memory and
the form in datom.

Nothing here is in production. The Source nexus is
a design in a flow; no branch builds it.

### Terms

Bytes and Byte are names coined for this book, not
yours. Bytes: one value that is a vector of bytes,
a hash among them. Byte: one byte, eight bits.
"Alphanumeric encoding" is your record's name for
the datom form; which encoding it is (base 32 or
another) is not chosen here.

### The code

Ethos used below. `Library` is the root of a file
of shared types; its four sections are imports,
types, traits and associations. In the types
section `Name.Type` declares a name over a type,
and `Name.{ … }` a struct whose positions are
types. `Vector<T>` is the intrinsic vector of T.
`Integer` is the intrinsic whole number; the
Source design reads it as 64 bits, signed. A
comment runs from `;` to the end of the line.

The wrong form: a hash as a hex String.

```
Library
[]                         ; imports
[ Blake3.String            ; types: wrong, the
  SourceName.String        ;   hash held as text
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

The type says text. It holds 64 characters where
the hash is 32 bytes, takes any text, a name or a
sentence, as a hash, and leaves no real stored type
behind: what is stored is a string representation,
the thing your record sets apart from the type in
memory.

## Proposal: a statement on bytes in Imports

Target: psyche-skills/vision/ethos.md, section
"## Imports", right after the intrinsic list.

Above, as it stands:

An import names a source and a type: `protos:String` or
`protos:[ String Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

### Choice 1: a Bytes intrinsic

```diff
+
+Bytes is an intrinsic known without import: one
+value that is a vector of bytes, of fixed or open
+length. In memory it is a vector of bytes; in
+datom it is written in an alphanumeric encoding.
```

```
Library
[]                         ; imports
[ Blake3.Bytes             ; types: the hash as
  SourceName.String        ;   bytes
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

`Blake3.Bytes` names the hash over the new
intrinsic. How a fixed length, 32 for Blake3, is
written in ethos is not chosen by this statement.

```
; datom, in a position expecting Blake3
; the run is illustrative: its length
; follows the encoding, not chosen here
k3m9q2x7ra4bf8nd5wp1ct6ve0zy2hsg
```

### Choice 2: a Byte intrinsic and Vector<Byte>

```diff
+
+Byte is an intrinsic known without import: one
+byte. A run of bytes, a hash among them, is
+Vector<Byte>.
```

```
Library
[]                         ; imports
[ Blake3.Vector<Byte>      ; types: the hash as a
  SourceName.String        ;   vector of Byte
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

No new container: bytes ride the existing Vector.
A datom vector is written as its elements in
brackets, so unless Vector<Byte> is given its own
datom form, the hash is written as 32 numbers.

### Choice 3: no new intrinsic

```diff
+
+Ethos has no byte intrinsic. A hash is a struct of
+Integers: a 256-bit hash is four.
```

```
Library
[]                         ; imports
[ Blake3.{ Integer         ; types: the hash as
           Integer         ;   four Integers
           Integer
           Integer }
  SourceName.String
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

This is the Source design's draft as it stands.
The Integers are signed, their order is chosen by
hand, and the type does not say bytes.

Below, as it stands:

```
Library
[ protos:[ String Textualizable ]  datom:Datom ]   ; imports
[]                                                 ; types
[]                                                 ; traits
[]                                                 ; associations
```

## Distillation

Proposed skill lines, per choice:

Choice 1. psyche-skills/vision/ethos.md, "##
Imports", after the intrinsic list: the four lines
of the Choice 1 statement, opened by a blank line;
Sources gets `058f16 source` and `d4ae97 datom`.

Choice 2. psyche-skills/vision/ethos.md, the same
place: the three lines of the Choice 2 statement,
opened by a blank line; Sources gets
`058f16 source` and `d4ae97 datom`.

Choice 3. psyche-skills/vision/ethos.md, the same
place: the two lines of the Choice 3 statement,
opened by a blank line; Sources gets
`058f16 source` and `d4ae97 datom`.

Sources:

058f16 source
d4ae97 datom

## Ruling

1. Choice 1: a Bytes intrinsic, a vector of bytes
   of fixed or open length, shown in datom in an
   alphanumeric encoding.
2. Choice 2: a Byte intrinsic; bytes are
   Vector<Byte>.
3. Choice 3: no new intrinsic; a hash is four
   Integers.

Or amend by line.
