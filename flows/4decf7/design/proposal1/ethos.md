# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

```
Library.{
  {0 1 0}
  []
  [ Sorted.{ Vector<Ordered> } ]    ; ethos: the type
  [] []
}
```
```
{ [ 1 2 3 ] }    ; datom, in a position expecting Sorted: its data
```

## Contextualization and the types of ethos objects

An ethos object is always situated: a line alone has no meaning, and
the same shape is a different thing in a different block, since the
block being parsed gives its shapes their meaning. The library and
the signal are ethos objects, each written as its version, its
imports and its sections: a library's sections are its types, its
kinds and its associations; a signal's are its requests and its
responses. In the types section the delimiter after the head tells
the type: X.{…} declares a struct, Y.[…] an enum, Z.Word a typedef.
In the kinds section a bracket after the head holds capabilities and
a brace opens the complex kind. In the associations section a type
is followed by the kinds it bears. The same mechanism serves wherever
several types share one position: the section of an interface, the
capabilities of a kind. A character means what the block being
parsed says it means: a colon in an import block is the import form;
in a block of capabilities it is free to mean what that block says.
An object is written in the headed form, its head standing before
its sections, or in the contained form, self-contained in one brace;
several objects share one file as a vector of contained objects, and
the contained form lets a model be specific when creating a
standalone object.

```
; A library, headed form.
Library.{0 1 0}
[ signal-psyche:Object                        ; imports: Object from lib.es of the signal-psyche source
  signal-psyche:[Object Thing]                ;   several
  signal-psyche:stream.[Stream Termination] ] ;   from stream.es of that source
[ X.{ … }                                     ; types: a struct
  Y.[ … ]                                     ;   an enum
  Z.Word ]                                    ;   a typedef
[ Runnable.[ run.[ Outcome ] ] ]              ; kinds
[ X.[ Runnable ] ]                            ; associations: X bears Runnable

; Two objects in one file, contained form.
[
  Library.{
    {0 1 0}
    []                            ; imports
    [types]
    [kinds]
    [associations]
  }

  Signal.{
    {0 1 0}
    []                            ; imports
    [requests]
    [responses]
  }
]
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
Library.{
  {0 1 0}
  []
  [ Sorted.{ Vector<Ordered> } ]    ; types
  [] []
}
```
```rust
struct Sorted<Ordered: Ord>(Vec<Ordered>);   // the Rust generated from it
```

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

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
