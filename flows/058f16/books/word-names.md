<!-- to-the-living:start -->
Presentation.{ «Word-built names» }

## A name made of words

A prototype name is an uncapitalized camelCase
identifier made of words, `sourceRegistry` or
`abandonAbilityAble`, checked whenever one is
created; its casing is proposed in the book «The
prototype name». The check splits the name at each
capital and looks each part up in a list of words.
This book asks where that list lives and which
words it holds.

Nothing of this exists yet, in production or in a
development branch: no generator, Nexus or library
checks a name against words today. What is below
was measured on a throwaway prototype.

Where the check can live:

```
 built in
 +--------------------------------+
 | the program creating the name  |
 |   the generator, a Nexus       |
 |                                |
 |   +--------------------------+ |
 |   | word list, in the binary | |
 |   +--------------------------+ |
 +--------------------------------+

 dedicated
 +--------------------------------+
 | the program creating the name  |
 +---------------+----------------+
                 |
                 | one request per new name
                 | over a socket
                 v
 +--------------------------------+
 | a word Nexus                   |
 |   word list, in one place      |
 +--------------------------------+
```

## What it costs

Measured by a subflow of this flow on 2026-10-10,
on one shared machine, release builds; read from
its report, not re-run here, so take each number
as plus or minus 20 percent. The program without
any word list is 364 KB.

Two lists. BIP-39: the 2048 words the three-word
flow id was built from (flows/5578cc/vision/
identifiers.md, 2026-10-03). A full English list
of 370,105 words, chosen by the subflow as a size
stand-in; you have named no list.

Built in, best and worst of four storage forms:

| list | binary grows by | memory held | per name |
|---|---|---|---|
| BIP-39 | 13 to 96 KB | about 0.1 MB | 0.09 to 0.34 µs |
| 370k words | 1.7 to 18.9 MB | 1.6 to 19.6 MB | 0.5 to 1.2 µs |

The smallest form, a compressed word set read
lazily from the binary, gives the low size for
both lists; the fastest, a perfect-hash table,
gives the high size and is loaded whole into
memory when the program starts.

Dedicated, asked over a socket from another
process:

| list | per name | the Nexus's own memory |
|---|---|---|
| BIP-39 | 7 to 13 µs | 2.3 MB |
| 370k words | 8 to 17 µs | 3.8 to 20 MB |

The lower time keeps one connection open, the
higher connects for each name. The socket costs
about 20 times the lookup itself on the small
list. A name is checked once, when created, so
neither cost is felt by a person; what differs
is that each built-in copy carries the list,
while the Nexus carries it once.

Not measured: build time, cold-start delay, and
whether either list holds the words names need.

## Distillation

### D1. Where the word check lives, in vision-nexus

Target: `psyche-skills/skills/vision-nexus.md`, the
vision-nexus skill. Place: the section `## Splitting
a Nexus`, after its last paragraph, before `##
Observation by subscription`.

Removed: none.

Above, unchanged (the section, whole, under its
heading `## Splitting a Nexus`):

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.

Added, one of three variants.

Variant 1, built in now, a Nexus later:

+A function that needs a database of its own, as checking a name made of words needs a database of words, needs a dedicated Nexus. Until that Nexus exists, the function is built into whatever it is compiled into.

Variant 2, built in:

+A function that needs a database of its own, as checking a name made of words needs a database of words, is built into whatever it is compiled into.

Variant 3, a Nexus from the start:

+A function that needs a database of its own, as checking a name made of words needs a database of words, is a dedicated Nexus; what needs the function asks it.

Below, unchanged: the heading `## Observation by
subscription`, then:

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

Added to the skill's Sources section:

+058f16 identifier
+d68c82 naming
+23824a names

(One comment, 2026-10-10, logged by three flows.)

### D2. Which words, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the end of the section
`## Naming`, before `## Identity`.

Removed: none.

Above, unchanged (the section, whole, under its
heading `## Naming`):

Traits are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

Added, one of two, or neither until a list is
chosen.

Variant 1:

+The words of a prototype name are the 2048 BIP-39 English words.

Variant 2:

+The words of a prototype name are a full English word list.

Below, unchanged: the heading `## Identity`, then:

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>.

Added to the skill's Sources section: the same
three lines as D1.

**Ruling.** D1 one of 1 to 3, or amend by line; D2
1, 2, or leave open.
<!-- to-the-living:end -->
