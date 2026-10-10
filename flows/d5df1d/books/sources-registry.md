<!-- to-the-living:start -->
Presentation.{ «Sources and the registry» }

## A source and its registry

In `Topic.custom:Name` the lowercase `custom` names
a source. A source is meant to be found through a
registry: each entry is keyed by the source's name
and holds a hash and a path, which lead to the
library where the name is declared. `core` is one
such source, among the others.

```
         Topic.flow:Voice
                |
                | lowercase source: flow
                v
  +------------------------------------+
  | Registry                           |
  |                                    |
  |   key     hash      path           |
  |   ----    ------    ------         |
  |   flow    <hash>    <path>    <--  |
  |   core    <hash>    <path>         |
  |   ...                              |
  +------------------------------------+
                |
                | the entry for flow
                v
  +------------------------------------+
  | Library flow                       |
  |   Voice                            |
  +------------------------------------+
```

Two facts about Ethos Zero on its main line. A
registry does not yet exist in the generator: a
source is written into the Rust as it is spelled.
So `core:Name` emits `core::Name`, and Rust refuses
it, since Rust's own `core` holds no `Name`.

```
Library
[]                     ; imports: none
; types: Topic over Name, sourced from core;
;   the generator writes core::Name today
[ Topic.core:Name ]
[]                     ; traits
[]                     ; associations
```

The records this rests on: flows/d5df1d/vision/ethos.md,
2026-10-09 (the registry keyed by subaspect and topic,
with hash and relative path; capital and lowercase
heads); flows/445410/vision/flow.md, 2026-10-09
(`core:Name` as a checked camelCase type).

## Distillation

### D1. A source names a registry entry, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Imports section,
after the inline-import statement proposed in «The
inline import, third edition», D1, and before "##
What a declaration turns into". Should that
statement not land, this goes after the Imports
section's closing paragraph, shown below as it
stands.

Removed: none.

Above, unchanged (the Imports section's closing
paragraph as the file stands; the third edition's
D1 statement follows it once landed):

```text
The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.
```

Added, prose, with one of three forks in place of
⟨the fork⟩:

```text
A lowercase source names an entry of the registry. What the generator
writes for a name from `core` is ⟨the fork⟩.
```

1. `core` is a crate of its own, and a name from it
   is written fully qualified from that crate.
2. The registry entry for `core` names the path,
   and the generator writes that path.
3. `core` is not a source, and a name sourced from
   `core` is refused.

Below, unchanged:

```text
## What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
```

Distils flows/d5df1d/vision/ethos.md, 2026-10-09, and
flows/445410/vision/flow.md, 2026-10-09.

## What the registry must say

These two questions shape the entry and the
registry. Your answers decide what the next
proposal on the registry carries.

1. What an entry leads to. The key is a source's
   name; the entry holds a hash and a path.

   What the key reaches:

   a. A repository: the entry names the repository
      that holds the library.
   b. A source in the 2026-08-22 sense: the entry
      names that source, whatever holds it.

   What the hash covers:

   c. The source tree: the hash changes when any
      file under the source changes.
   d. The commit: the hash is the commit the
      library was read at.
   e. The file: the hash is over the one file the
      path names.

   Which hash:

   f. Blake3, held as its own type.
   g. Left open for now, written as a string.

   Or the whole entry as the first edition drew it:

   h. Source, a Blake3 hash, and a relative path,
      in that order.

2. How many registries, and how one reaches the
   generator. The generator is not a Nexus and keeps
   no store of its own.

   How many:

   a. One registry type, serving both the libraries
      named by a source and the vision and knowledge
      files keyed by subaspect and topic.
   b. Two registry types: one for libraries, one for
      vision and knowledge files.
   c. Two registries: the core library's own, shipped
      with it and the same everywhere, and the loaded
      environment's.

   How it reaches the generator:

   d. A datom manifest, read beside the ethos file
      (2026-08-20).
   e. An assembly file naming the source, its one
      target and the registry entries (2026-08-21).
   f. Inside the generate request itself, beside the
      source and the target.

**Ruling D1.** The fork number; then for question 1
one letter from each group, or h; for question 2 one
of a to c and one of d to f. Or amend, by line.
<!-- to-the-living:end -->
