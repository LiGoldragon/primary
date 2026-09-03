# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

```
Sorted.{ Vector<Ordered> }    ; ethos: the type
Sorted.{ [ 1 2 3 ] }          ; datom: its data
```

## Why Ethos

Existing text data formats and existing programming languages both
fail. Rust is the new assembly, read in full by no one; Ethos is the
concise, dense, cognitively concentrated language for writing code
with AI agents, easy to read and write, showing the interfaces: the
main types and the main kinds. Behavior falls under kinds, which
creates an ontology in code.

## Generation

Ethos generates the Rust. Rust generated from ethos is committed, so
ordinary tooling, language servers, works normally; a freshness
mechanism is deliberately left open.

```
Sorted.{ Vector<Ordered> }    ; struct Sorted<Ordered: Ord>(Vec<Ordered>)
```

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

## Declarations

In an Ethos type declaration the delimiter after the head tells the
type: X.{…} declares a struct, Y.[…] an enum, Z.Word a typedef. The
same mechanism serves wherever several types share one position: the
section of an interface, the capabilities of a kind. A character
means what the block being parsed says it means: a colon in an
import block is the import form; in a block of capabilities it is
free to mean what that block says. A library is written as its
version, its imports, its types, its kinds and its associations, in
the headed form or the contained form; several libraries or an
interface may share one file in the contained form.

```
X.{ … }        ; a struct
Y.[ … ]        ; an enum
Z.Word         ; a typedef

Library.{0 1 0}
[ signal-psyche:Object                     ; Object from lib.es of the signal-psyche source
  signal-psyche:[Object Thing]             ; several
  signal-psyche:stream.[Stream Termination] ]   ; from stream.es of that source
[types]
[kinds]
[associations]
```

## Self-description

A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object, CLI
now, Mentci later, and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.

## Horizon

Ethos will eventually replace everything, Rustlang becoming its
assembly layer. Designs are chosen for that horizon; what it
enables, generator emission among it, comes in its time.
