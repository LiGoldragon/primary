# Distillation proposal: Vision/ethos.md, Vision/ethosMonolith.md (additions) and Vision/ethosInterfaces.md (new)

Composed in flow b675f3d9 from reports/distillCandidatesEthos.md.
Kind, capability and interaction vocabulary is in the kinds proposal
and is not repeated here. Each statement lands only on the living's
explicit approval.

---

# Vision/ethos.md — additions

## One abstraction up

Ethos is one abstraction up from Rust — our response to all other
programming languages, a higher level of abstraction than any of
them. It gives, in one swoop, the mental model of the machine and the
code for it, where Rust or JavaScript bury the model under noise —
more than half of the code is noise.

## Ethos declares; datom is data

Ethos declares types and kinds. Datom is data. A statement about the
text form of data belongs to datom; a statement about types, kinds,
sections, imports, or programs belongs to Ethos.

## File and source

The unit of Ethos is the file. A source is what Rust calls a crate.
For the monolith, one file becomes one Rust module: easy cognition is
the first safe bet.

## Document kinds and where they live

A component's wire types are declared in signal Ethos, in its signal
repos. Its engine operations (nexus Ethos) and its stored types (sema
Ethos) are not designed yet; when they are, they live in the
component's main repo. Every wire interface is written in Ethos.

## The first scope

The first Ethos declares kinds and checks, at build time, that a type
carries the kinds it claims. Function bodies and their Rust
generation are a later, larger job.

---

# Vision/ethosInterfaces.md — proposed, new

# Ethos interfaces

## Sections confer

An interface's sections exist to confer a kind on their items —
Input, Output, Refusal. An item is a request by virtue of standing in
the input slot, so the word request is redundant there.

## Imperative voice

An interface is designed verb-first, in the imperative: list,
observe, register. Commands that are universal across nexuses —
observe above all — are reused, so that a model can use a nexus it
was never trained on from the primordial commands it already knows.

## Streams

A stream is a section inside the object; its initiation and
termination live in the input. Stream is the fourth kind of section.
Getting the syntax and the concepts right and reaching the minimum
viable product comes before any transformer that generates the
stream's input objects — those are written by hand for now.

## Imports

Pulling from an external source is explicit: `source:Object` pulls
Object from that source's lib file; `source:[Object Thing]` pulls
several; `source:file.[Object Thing]` pulls from a named file of the
source. The source name resolves through a manifest, written in
datom; a name the manifest cannot resolve is an error. A bare path
resolves locally only. What exists is an import reference; there is
no Import type. A file has no namespace inside it.

---

# Vision/ethosMonolith.md — additions and one replacement

## Name  (addition)

Its better name is ethos-zero: version zero, which bootstraps Ethos
into the nexus trinity — the Ethos, Nomos and Logos nexuses. Whether
it is called ethos-cc, compiler-compiler, is unruled.

## Shape  (replaces the first sentence)

The monolith is written as a nexus from the start: the things it
deals with are broken down, the kinds — the ways those things
interact — are isolated and properly named. Everything will be a
nexus; the consistency creates reliability and raises quality and
clarity.

## What it generates  (addition)

Rust for the types and kinds that define the wire types (signal), the
major internal engine operation types (nexus), and the database types
(sema).

## The trinity it bootstraps  (addition)

Ethos, Nomos and Logos are daemons, each with the architecture of
every other component: a daemon, a CLI, a CLI for the meta socket,
all messages signal. Everything is in the daemon: the Ethos daemon
loads the Ethos and holds the whole thing.

---

## Resolved by date, for the living's confirmation

- Imports: `/` was ruled on 2026-08-07; the explicit colon syntax
  (`source:Object`) was ruled on 2026-08-20 and the fallback killed
  the same day. The later ruling stands: colon. The fixtures agree.

## Vision impurities (destroyed, on the living's ruling)

- "Orchestrate is the project the monolith is tested with" — a
  working instruction; statement withdrawn, raw record aa4c7747
  ethosMonolith.md 2026-08-25 destroyed.

## Suspected impurities — the living's judgement asked

- ethos.md "File and source": "For the monolith, one file becomes one
  Rust module: easy cognition is the first safe bet" — a monolith
  working decision?
- ethos.md "The first scope" — MVP scope: a working decision, or
  vision on what the first Ethos is?
- ethosInterfaces.md "Streams": "those are written by hand for now" —
  working instruction.

## Not distilled (open)

- The TryFrom-vs-effect verb (in the anatomy proposal as open).
- The nexus and sema document designs.

## Sources

- flows/b675f3d9/reports/distillCandidatesEthos.md (record ids)
