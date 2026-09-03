# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

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
free to mean what that block says.

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
