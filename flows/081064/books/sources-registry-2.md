# Sources and the registry

## Context

In `Topic.custom:Name` the lowercase `custom` names
a source. The registry is what a lowercase name
leads to: one line per lowercase name, saying which
source holds it and the Rust path the generator
writes for it. The lines come from datom files,
one per repository, each naming the ethos sources
that repository holds.

The inline import is landed: the Imports section
of psyche-skills/vision/ethos.md carries it. The
registry line is not landed.

Two Nexuses share the work. The Source nexus owns
sources: each `Source` is a name, a `Fetcher` (Git
at a revision, or a local directory) and a Blake3
hash; each repository's `Contribution` brings its
sources in; `Fetch` hands over a source whole, as a
snapshot, its hash checked. The Ethos nexus keeps
name resolution: its Memory holds the registry,
`Register` and `Unregister` change it one
repository's part at a time, and `Resolve` turns a
lowercase name into the Rust path. The Ethos nexus
book draws its fetch as one file of one source; the
Source nexus design fetches the whole snapshot.
Proposal 2 settles on the whole snapshot.

```
 repository   repository   repository
 datom file   datom file   datom file
     |            |            |
     +------------+------------+
                  |
                  v
+------------------------------------------+
| Ethos nexus                              |
|   Memory: the registry                   |
|   one line per lowercase name            |
|   Resolve  Register  Unregister          |
+--------------------+---------------------+
                     |
                     | the name's source
                     v
+------------------------------------------+
| Source nexus                             |
|   Source: name, Fetcher, Blake3          |
|   Contribution: one per repository       |
|   Fetch: the whole snapshot              |
+--------------------+---------------------+
                     |
                     v
         the snapshot, hash checked
```

Where things are. The inline import is in the
generator's main line. The registry is not: the
generator writes a source as it is spelled, so
`core:Name` becomes `core::Name`, which Rust
refuses, since Rust's own `core` holds no `Name`.
The Source nexus and the Ethos nexus are designs;
neither runs in production and no development
branch of either was found.

The designs: flows/058f16/reports/source-nexus-design.md
and the book flows/081064/books/ethos-nexus.md. The
records the registry rests on:
flows/d5df1d/vision/ethos.md, 2026-10-09, and
flows/445410/vision/flow.md, 2026-10-09.

## Distillation

Target file, both proposals:
/git/github.com/LiGoldragon/psyche-skills/vision/ethos.md
(the vision-ethos skill, authored source). Place:
the Imports section, after the landed inline-import
paragraph and before "## What a declaration turns
into". The lines around it as they stand, wrapped
for the phone:

Above, unchanged:

```
 The generated code carries no `use`
 statements; each imported name is written
 fully qualified: `protos:String` appears as
 `protos::String`, `datom:Datom` as
 `datom::Datom`.

 A type may be declared over a type from a
 source in place, with no entry in the imports
 section: `Topic.custom:Name` declares `Topic`
 over the type `Name` from the source `custom`.
 The source is known twice: its first letter
 is lowercase, and a colon follows it.
```

Below, unchanged:

```
 ## What a declaration turns into

 A declaration turns into the Rust type with
 named fields, bearing the datom traits
 through the derive, which Ethos Zero emits
 with the type.
```

### Proposal 1. A source names a registry entry

Removed lines: none.

Added: one paragraph, one of three sides. Every
side is shown on this file:

```
Library
[]
[ Topic.core:Name ]
[]
[]
```

Each side was built as a candidate on the
generator's main line and passed its checks; that
is the claim of flows/1d0733/reports/q8-ac.md and
q8-b6.md, not witnessed here.

Side a. `core` is a crate of its own; the generator
writes core's name from that crate. No crate holding
core's Rust is named; `ethos_core` stands in for it.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is that name fully qualified from
+core's own crate, never Rust's `core`.
```

Wrong, then right:

```rust
pub type Topic = core::Name;
pub type Topic = ethos_core::Name;
```

Side b. `core` is one registry entry like any other;
its entry names a Rust path, and the generator
writes that path. A source with no entry is refused.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is the Rust path that the registry
+entry for `core` names.
```

Entries, then what is written:

```
[ { core ethos_core }
  { flow signal_flow } ]
```

```rust
pub type Topic = ethos_core::Name;
```

Side c. `core` is not a source; a name sourced from
it is refused where the source is read. This also
refuses `Topic.core:Name`, the key in the registry
example of flows/d5df1d/vision/ethos.md.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is nothing: `core` is not a source,
+and a name sourced from `core` is refused.
```

Wrong, the refusal it meets, then right:

```
[ Topic.core:Name ]
```

```
Conceptual.{ [ 1 1 0 1 0 ] Source.core }
```

```
[ Topic.custom:Name ]
```

Impurities discarded: none.

Ruling asked:

1. Land side a as written.
2. Land side b as written.
3. Land side c as written.
4. Amend, by line.

### Proposal 2. Fetching and resolving are split

Removed lines: none.

Added, after Proposal 1's paragraph:

```
+A source is fetched whole, as a snapshot, by
+the Source nexus. The Ethos nexus resolves a
+lowercase source name through the registry.
```

Impurities discarded: none.

Ruling asked:

1. Land as written.
2. Amend, by line.
