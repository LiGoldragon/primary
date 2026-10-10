<!-- to-the-living:start -->
Presentation.{ «Word-built names» }

## A name made of words

A name is the uncapitalized camelCase identifier
for what is not a type, a trait or a variant:
`sourceRegistry`, `abandonAbilityAble`. A name is
its own type, `core:Name`, and every new one is
checked: split at each capital, each part looked
up in a list of words.

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

### D1. Names are uncapitalized camelCase words, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Naming section,
after its one paragraph, before "## Identity".

Removed: none.

Above, unchanged (the Naming section, whole):

```text
## Naming

Traits are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.
```

Added, prose and code:

```text
In datom and ethos, what is not a type, a trait or a variant is named
in uncapitalized camelCase; PascalCase is for what the language
defines and for variants.

A name is its own type, `core:Name`: like a string, but checked
whenever one is created. It is an uncapitalized camelCase identifier
composed of words, and the check finds each word in a database of
words. A string stays a string: a string position in datom may start
with a capital.
```

```
; ethos: Topic is declared over core:Name
[ Topic.core:Name ]

; datom, in a position expecting Topic
sourceRegistry        ; a name: two words
qzxRegistry           ; refused: qzx is no word
SourceRegistry        ; refused: capital first

; datom, in a position expecting String
TheBuildPassedOnTheThirdTry
```

`core:Name` is the core library's type for a
name; `Topic` is any type declared over it, as
vision-flow's topic is.

Below, unchanged:

```text
## Identity

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>.
```

Sources lines added: `058f16 identifier`,
`d68c82 naming`, `23824a names` (one comment,
2026-10-10, logged by three flows).

### D2. Where the word check lives, in vision-ethos

Target: the same file, directly after the D1
lines. Removed: none. Added, one of three:

1. Built in now, a Nexus later:

   ```text
   For now the word check is built into what creates the name, its
   word list compiled in; it moves to a dedicated Nexus holding the
   database of words.
   ```

2. Built in:

   ```text
   The word check is built into what creates the name, its word list
   compiled in.
   ```

3. A Nexus from the start:

   ```text
   The word check is a dedicated Nexus holding the database of words;
   what creates a name asks it.
   ```

Same Sources lines as D1.

### D3. Which words, in vision-ethos

Target: the same file, after the D2 line. Removed:
none. Added, one of two, or neither until a list
is chosen:

1. ```text
   The words of a name are the BIP-39 English words.
   ```
2. ```text
   The words of a name are a full English word list.
   ```

**Ruling.** D1 approve or amend by line; D2 one of
1 to 3; D3 1, 2, or leave open.
<!-- to-the-living:end -->
