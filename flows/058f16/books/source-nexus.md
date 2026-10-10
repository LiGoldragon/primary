<!-- to-the-living:start -->
Presentation.{ «The Source nexus» }

## One Nexus for every source

The Source nexus serves the sources of every
component. A component names a source; the Source
nexus knows where its bytes are and what their
Blake3 hash must be, and refuses bytes that do not
match. Nothing of this exists yet, in production or
in a development branch: it is a design, and this
book asks for the words it is to be built against.

```
 a component: Ethos, Curriculum, a flow
 +------------------------------------+
 | knows a source by its name only    |
 +-----------------+------------------+
                   |
                   | get, or check, by name
                   v
 +------------------------------------+
 | Source nexus                       |
 |                                    |
 |   registry, one entry per name:    |
 |     where: Git at a revision,      |
 |            or a path on a host     |
 |     hash:  Blake3 of the snapshot  |
 |                                    |
 |   snapshot, without .git           |
 |     hashed on every use;           |
 |     handed over only on a match    |
 +-----------------+------------------+
                   ^
                   | assembled, all at once
                   |
 +-----------------+------------------+
 | a datom file in each repository,   |
 | edited by whoever edits that repo  |
 +------------------------------------+
```

The types every user of sources shares sit in one
library. In ethos, a `Library` declares types; `.`
after a name gives its type, `.{ }` makes a struct
of the positions inside, `.[ ]` an enum of the
variants inside:

```
Library
[]
[ SourceName.String
  Blake3.{ Integer Integer
           Integer Integer }
  Fetcher.[ Git.{ Remote Revision }
            Local.{ Host Directory } ]
  Source.{ SourceName Fetcher Blake3 }
  Contribution.{ Contributor
                 Vector<Source> } ]
[]
[]
```

`SourceName` is the name a component holds.
`Fetcher` says where the bytes come from. `Source`
is one registry entry. `Contribution` is what one
repository's datom file holds. `Blake3` is four
64-bit integers only because ethos has no byte type
yet; that is the question of the book «Bytes in
ethos». Whether `SourceName` becomes a checked name
built of words is the question of «Word-built
names»; here it is plain text.

Where this meets «The Ethos Nexus»: the Ethos
registry keeps a name and a path inside a source,
keyed by the same `SourceName`; the hash and the
fetcher stay in the Source nexus. That book's
question on where the hash lives is the same line
seen from the Ethos side.

## Distillation

### D1. The Source nexus, a new skill vision-source

Target: `psyche-skills/skills/vision-source.md`, a
new file, shown whole. It distils the comments of
2026-10-10 on «Sources and the registry»
(flows/058f16/vision/source.md). The design's
answers to the questions below land in it as D2 to
D7.

Added, the whole file:

+---
+description: The Source nexus — its registry of sources, their hashes, fetchers and shared library — is being designed or judged against what the living wants.
+dependencies: [vision-nexus]
+---
+
+## One Nexus for sources
+
+The Source nexus serves the sources of every component, so the sources aspect is fixed in one place. To get a source is to send the Source nexus a source request.
+
+## The registry
+
+The Source nexus keeps a registry of sources. An entry reaches its source through a backend fetcher, a Git repository at a revision or a local path on a given host, and carries the source's own Blake3 hash.
+
+## Assembled from repositories
+
+The registry is populated from datom files kept in repositories, each updated by whoever updates its repository, and loaded together into the full registry. The registry is updated atomically.
+
+## The hash verifies
+
+The hash verifies that the files are the right files when they are used. A store for hash-addressed files, which knows what to store, how to fetch it, and what Git already holds so nothing is stored twice, is a later lane.
+
+## The hash covers the whole snapshot
+
+A source's hash covers the whole snapshot of its repository at a revision, as Nix does, without the Git subdirectory. When the source changes, its hash changes.
+
+## A shared sources library
+
+The components that use sources share a library of source types, including the objects a Memory stores for a registry of sources. A component refers to a source by name, so only the Source registry changes when a source's content changes.
+
+## A registry name
+
+A source's registry name need not be its repository's name. Repository names stay kebab-case.
+
+## Sources
+
+058f16 source
+d68c82 source
+081064 ethos
+23824a sources

(One set of comments, 2026-10-10, logged by four
flows.)

**Ruling.** D1 as written, or amend by line.

### D2. The datom file and its own repository

A file inside a repository cannot hold that
repository's whole-snapshot hash: writing the hash
into the file changes the snapshot, and so the
hash. A Git revision cannot be written into its own
commit for the same reason.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## Assembled from
repositories`.

Above, unchanged:

The registry is populated from datom files kept in repositories, each updated by whoever updates its repository, and loaded together into the full registry. The registry is updated atomically.

Added, one of three.

Variant 1, the design's:

+A repository's datom file lists the sources that repository uses, each with its hash, as a lock file does. Two repositories cannot list each other.

Variant 2:

+A repository's datom file describes that repository itself, by name and fetcher. Its hash, and for Git its revision, are taken when the registry is assembled.

Variant 3:

+A repository's datom file describes that repository itself, hash included, and the file is left out of the bytes hashed.

Below, unchanged: the heading `## The hash
verifies`.

**Ruling.** 1, 2 or 3.

### D3. What bytes are hashed

The design hashes an archive of the tree in the
format Nix specifies for its own archives: entries
sorted by name, each with its kind, executable bit,
contents or link target. The Nexus skill already
says an encoded form fingerprints itself, by
default by the hash of its rkyv archive.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## The hash covers
the whole snapshot`.

Above, unchanged:

A source's hash covers the whole snapshot of its repository at a revision, as Nix does, without the Git subdirectory. When the source changes, its hash changes.

Added, one of three.

Variant 1, the design's:

+The bytes hashed are the snapshot in the Nix archive format.

Variant 2:

+The bytes hashed are the rkyv archive of the snapshot as a typed tree value.

Variant 3:

+The hash is the root of a tree of per-file Blake3 hashes, which a later store can use to keep each file once.

Below, unchanged: the heading `## A shared sources
library`.

**Ruling.** 1, 2 or 3.

### D4. What a local snapshot includes

A local source is a directory as it stands on its
host. Taking every file but the Git subdirectory
includes build output, so the hash of a local
source changes at every build inside it.

Target: `psyche-skills/skills/vision-source.md`.
Place: after D3's line, same section.

Added, one of three.

Variant 1, the design's:

+A local snapshot is every file in the directory except the Git subdirectory, build output included.

Variant 2:

+A local snapshot is the files Git tracks, as they stand in the directory.

Variant 3:

+A local snapshot is every file in the directory except the Git subdirectory and what the repository's ignore rules exclude.

Below, unchanged: the heading `## A shared sources
library`.

**Ruling.** 1, 2 or 3.

### D5. One registry or several

The design keeps one entry per name: one fetcher
and one hash. «The Ethos Nexus» reads the same
comments as placing Git revisions in a registry of
their own, the Git equivalence registry.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## The registry`.

Above, unchanged:

The Source nexus keeps a registry of sources. An entry reaches its source through a backend fetcher, a Git repository at a revision or a local path on a given host, and carries the source's own Blake3 hash.

Added, one of two.

Variant 1, the design's:

+An entry holds a name, one fetcher and the hash.

Variant 2:

+The registries are two: one from name to hash, and the Git equivalence registry, from hash to where Git holds it. Only the sources that need it are in the second, and it is dropped when Git is.

Below, unchanged: the heading `## Assembled from
repositories`.

**Ruling.** 1 or 2.

### D6. Who reads the datom files

The Nexus skill says a command-line client turns
text into signal and nothing more. Reading the
repositories' datom files is more than that.

Target: `psyche-skills/skills/vision-source.md`.
Place: after D2's line, same section `## Assembled
from repositories`.

Added, one of two.

Variant 1, the design's:

+The Source nexus's meta client reads the repositories' datom files and sends what they hold as signal; it is the one client that does more than turn text into signal.

Variant 2:

+A separate assembler reads the repositories' datom files and sends what they hold as signal; the meta client stays text into signal.

Below, unchanged: the heading `## The hash
verifies`.

**Ruling.** 1 or 2.

### D7. Where the shared library lives

Every component that fetches sources already
depends on the Source nexus's ordinary wire
repository, since peers depend on each other's wire
repositories.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## A shared sources
library`.

Above, unchanged:

The components that use sources share a library of source types, including the objects a Memory stores for a registry of sources. A component refers to a source by name, so only the Source registry changes when a source's content changes.

Added, one of two.

Variant 1, the design's:

+The shared sources library is a repository of its own.

Variant 2:

+The shared sources library lives in the Source nexus's ordinary wire repository.

Below, unchanged: the heading `## A registry
name`.

**Ruling.** 1 or 2.
<!-- to-the-living:end -->
