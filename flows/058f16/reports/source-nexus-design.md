# Source nexus: smallest working design

The Source nexus (`source`) is one Nexus that serves the sources of every
component. "Go get a source" means: send the Source nexus a source request.
It keeps a registry of named sources. Each entry names one repository, one
backend fetcher (Git at a revision, or a local path on a host) and the
Blake3 hash of that repository's snapshot without `.git`. The hash is
checked every time a source is used. The registry is assembled atomically
from datom files kept in the repositories themselves. A store that keeps
snapshots is not part of this design.

Ground: the living's words in `flows/058f16/vision/source.md` and
`flows/058f16/vision/identifier.md` (2026-10-10). The Nexus shape comes from
the `vision-nexus` skill. Where the design goes beyond those words, it is
this flow's inference and is marked as a fork.

Witness: every ethos draft below passed `Check` and `Generate` with
ethos-zero 17.0.0, built by Nix at origin/main `07714b`, on 2026-10-10.
The generated Rust was not compiled.

## Shape

```
  caller (ethos, curriculum, a flow)
        |  Fetch / Check / Resolve
        v
  +---------------- source nexus ------------+
  | Signal ---> Operation ---> Memory        |
  |              |   ^          Registered   |
  |              v   |          records      |
  |      backend fetchers                    |
  |      Git.{ remote revision }             |
  |      Local.{ host directory }            |
  |              |                           |
  |              v                           |
  |      snapshot, minus .git                |
  |              |                           |
  |              v                           |
  |      Blake3, compared with the entry     |
  +------------------------------------------+
        ^  Assemble / Withdraw (meta socket)
        |
  source-meta CLI <--- sources.datom
                        in each repository
```

The repositories follow vision-nexus:

- `source`: the Nexus, plus its CLIs `source` and `source-meta`.
- `signal-source`: the ordinary socket's contract.
- `meta-signal-source`: the meta socket's contract.
- The shared sources library: its own repository (fork F11).

## Shared sources library

This section stands alone. It can be sent to the Ethos topic as it is.

The living asked for this: "a shared library between them, which is about
sources, and it can even have objects for memory to store a registry of
sources". A component such as Curriculum or Ethos refers to a source by
`SourceName` only. Only the Source registry holds the hash, so a
component's own registry does not change when a source's content changes.

```
Library
[]
[ SourceName.String
  Blake3.{ Integer Integer Integer Integer }
  Remote.String
  Revision.String
  Host.String
  Directory.String
  Fetcher.[ Git.{ Remote Revision }
            Local.{ Host Directory } ]
  Source.{ SourceName Fetcher Blake3 }
  Contributor.String
  Contribution.{ Contributor Vector<Source> } ]
[]
[]
```

- `SourceName` is the registry name. It does not need to match the
  repository's kebab-case name. For now it is a `String`; see F10.
- `Blake3` holds 256 bits as four 64-bit `Integer`s, because ethos has no
  byte-array intrinsic; see F3. Rust generates
  `first_integer` through `fourth_integer` as `i64`.
- `Revision` is a full Git commit id; see F13.
- `Contribution` is what one repository's datom file holds. It names the
  contributing repository and lists the sources that repository brings
  into the registry; see F5.

Example `sources.datom` at the root of the Curriculum repository. The hash
integers are illustrative.

```
{ curriculum
  [ { psycheSkills
      Git.{ https://github.com/LiGoldragon/psyche-skills
            9fb0433... }
      { 812 -77 4410 9 } }
    { ethosZero
      Local.{ prometheus
              /git/github.com/LiGoldragon/ethos-zero }
      { -5 31 2026 7714 } } ] }
```

## The hash

The hash covers the whole repository at a revision, as Nix does: "It would
be the snapshot of that revision that we hash". `.git` is not part of the
snapshot. For a Git fetcher, the snapshot is the tree at that commit. For
a Local fetcher, it is the directory as it stands on that host. How the
tree is serialized before hashing is fork F1. Which files a Local snapshot
includes is fork F2.

The hash is checked on use. `Fetch` hashes what it fetched and places it
only on a match. `Check` hashes a directory the caller already holds. When
a Local source has changed since its entry was written, the hash differs
and the use is refused. The entry changes only when the repository's
datom file changes and the registry is assembled again.

## Signal: ordinary socket (`signal-source`)

```
Signal
[ sources:[ SourceName Blake3 Host Directory Source ] ]
[ Resolve.SourceName
  Fetch.{ SourceName Directory }
  Check.{ SourceName Directory } ]
[ Resolved.Source
  Fetched.{ SourceName Blake3 Directory }
  Checked.{ SourceName Blake3 }
  Refused.Refusal ]
[ Refusal.[ Unknown.SourceName
            Mismatched.{ SourceName Expected.Blake3 Found.Blake3 }
            Unfetchable.{ SourceName Unfetched }
            ElsewhereHost.Host
            Occupied.Directory
            Missing.Directory ]
  Unfetched.[ RemoteUnreachable
              RevisionMissing
              DirectoryMissing ] ]
```

- `Resolve` returns the entry.
- `Fetch` writes the verified snapshot into the caller's directory, which
  must not exist yet (F8).
- `Check` verifies a directory the caller already has.

Examples (hash integers are illustrative):

```
source 'Resolve.ethosZero'
Resolved.{ ethosZero
           Local.{ prometheus /git/github.com/LiGoldragon/ethos-zero }
           { -5 31 2026 7714 } }

source 'Fetch.{ psycheSkills /home/li/work/psyche-skills }'
Fetched.{ psycheSkills { 812 -77 4410 9 } /home/li/work/psyche-skills }

source 'Check.{ ethosZero /git/github.com/LiGoldragon/ethos-zero }'
Refused.Mismatched.{ ethosZero { -5 31 2026 7714 } { 66 -1 3 90 } }

source 'Fetch.{ spirit /home/li/work/spirit }'
Refused.Unknown.spirit

source 'Fetch.{ ethosZero /home/li/work/ez }'     ; asked on ouranos
Refused.ElsewhereHost.prometheus
```

## Signal: meta socket (`meta-signal-source`)

```
Signal
[ sources:[ SourceName Contributor Contribution ] ]
[ Assemble.Vector<Contribution>
  Withdraw.Contributor ]
[ Assembled.Integer
  Withdrawn.Contributor
  Refused.[ Conflicting.{ SourceName Vector<Contributor> }
            Unknown.Contributor ] ]
[]
```

`Assemble` replaces the entries of every contributor it names, all in one
Memory write. A single conflict refuses the whole request and leaves the
registry unchanged. A conflict is the same `SourceName` with different
entries, from contributors in the request or already in the registry.
`Assembled` answers with the number of entries now registered. The meta
socket carries the standard Configure and metadata tree of every Nexus.
The Source nexus adds no configuration value of its own.

The `source-meta` CLI reads each repository's `sources.datom`, composes
the `Contribution`s and sends them as signal, so datom stays out of the
Nexus (F6):

```
source-meta 'Assemble.[ /git/github.com/LiGoldragon/Curriculum
                        /git/github.com/LiGoldragon/ethos-zero ]'
Assembled.7

source-meta 'Assemble.[ /git/github.com/LiGoldragon/ethos-zero ]'
Refused.Conflicting.{ core [ ethosZero curriculum ] }

source-meta 'Withdraw.curriculum'
Withdrawn.curriculum
```

## Operation

Every effect has its own operation: a registry read, a backend fetch, a
hash, a placement, a discard and a registry write.

```
Operation
[ sources:[ SourceName Blake3 Fetcher Directory Source Contributor Contribution ] ]
[ Look.SourceName
  Materialize.{ Fetcher Staging.Directory }
  Hash.Directory
  Place.{ Staging Directory }
  Discard.Staging
  Replace.Vector<Contribution>
  Remove.Contributor ]
[ Found.Source
  Materialized.Staging
  Hashed.Blake3
  Placed.Directory
  Discarded
  Replaced.Integer
  Removed
  Failed.Failure ]
[ Failure.[ Unknown.SourceName
            Unfetchable.Fetcher
            Unreadable.Directory
            Occupied.Directory
            Conflicting.SourceName
            StoreRefused ] ]
```

A `Fetch` from query to response:

```
Fetch.{ psycheSkills /home/li/work/psyche-skills }   ; 1 Query
Look.psycheSkills                                    ; 2 Operation
Found.{ psycheSkills Git.{ ... } { 812 -77 4410 9 } }  ; 3 from Memory
Materialize.{ Git.{ ... } /home/li/work/.psyche-skills.staging }
Materialized./home/li/work/.psyche-skills.staging    ; 4 tree, no .git
Hash./home/li/work/.psyche-skills.staging
Hashed.{ 812 -77 4410 9 }                            ; 5 equal to the entry
Place.{ /home/li/work/.psyche-skills.staging /home/li/work/psyche-skills }
Placed./home/li/work/psyche-skills                   ; 6 one rename
Fetched.{ psycheSkills { 812 -77 4410 9 } /home/li/work/psyche-skills }
```

On a mismatch, step 6 is `Discard`, and the response is
`Refused.Mismatched`. `Check` takes the same path without `Materialize`,
`Place` or `Discard`.

## Memory

```
Memory
[ sources:[ Contributor Source ] ]
[ Registered.{ Contributor Source } ]
```

There is one record per registered source, along with the contributor
whose file brought it in. `Replace` deletes the named contributors'
records and writes the new ones in one transaction. The Nexus answers
lookups by `SourceName` from these records.

## The line with the Ethos registry

The Ethos topic's candidate patches (6d, 6e, 6f in
`flows/1d0733/reports/q8-b6.md`) give ethos-zero its own registry:
`Registered.{ Name.String Emitted.String }`. Each entry maps a lowercase
source to the Rust path the generator emits for it. The Ethos Nexus will
keep that registry.

The two registries answer different questions:

```
 Source registry (source nexus)
   ethosZero -> Local.{ prometheus /git/... }, Blake3
   answers: which bytes, from where, are they right
                 |
                 | same SourceName
                 v
 Ethos registry (ethos nexus)
   flow -> signal_flow
   answers: what Rust path names it in generated code
```

The emitted Rust path belongs to the Rust generator, so it stays out of
the Source entry. The fetcher and the hash belong to sources, so they stay
out of the Ethos entry. The two are joined by the name. When the Ethos
Nexus needs a source's files, it sends `Fetch` or `Check` with that name.
Whether the Ethos key must be a registered `SourceName` is fork F12.
Which channel carries the Ethos registry into the generator (6d, 6e or 6f)
is the Ethos topic's own fork. This design does not depend on it.

## Open forks

The living has not ruled on any of these. The option marked "drafted" is
the one the drafts above use. Each such choice is this flow's.

- **F1. How the tree is serialized for hashing.**
  - (a) A canonical walk, as in Nix's NAR format: entries sorted by name,
    each with its kind, executable bit, bytes or symlink target. Drafted.
  - (b) The Blake3 of the rkyv archive of a typed tree value. This matches
    vision-nexus: "an encoded form fingerprints itself, by default the
    hash of its rkyv archive".
  - (c) A Merkle tree of per-file Blake3 hashes, which a later store could
    use to avoid storing a file twice.
- **F2. What a Local snapshot includes.**
  - (a) Every file except `.git`, as the living's words say. Drafted. This
    includes build output such as `target/`.
  - (b) Only the files Git tracks, in their working-tree state, as Nix's
    `git+file` does.
  - (c) Every file except those `.gitignore` excludes.
- **F3. The type of Blake3.**
  - (a) Four `Integer`s. Drafted.
  - (b) A fixed 32-byte intrinsic in ethos-zero, written as hex in datom.
    This is a finding for the Ethos topic: ethos has no byte-array type.
  - (c) A hex `String`. This goes against the living's 2026-10 record that
    a hash needs a real stored type (`flows/d4ae97/vision/datom.md`).
- **F4. The registry's shape.**
  - (a) One entry holding a name, one fetcher and a hash. Drafted.
  - (b) Two registries: name to Blake3, and Blake3 to fetchers. The second
    is the "Git equivalence registry" the living says can be dropped once
    Git is cut off.
  - (c) One entry with a `Vector<Fetcher>`.
- **F5. What a repository's datom file lists.**
  - (a) The sources that repository uses, like a lock file. Drafted.
  - (b) The repository itself, as in "wrap all of the data in that
    particular repository". But if the hash covers the whole repository,
    a file inside it cannot hold that repository's own hash unless the
    file is left out of the hash.
- **F6. Who reads the datom files.**
  - (a) The `source-meta` CLI. Drafted. Its input (a list of repository
    paths) then differs from the signal it sends, as Curriculum's
    `CliRequest` differs from its `Query`.
  - (b) The Nexus links datom-codec. This goes against vision-nexus,
    which keeps datom out of the Nexus.
  - (c) A separate assembler program.
- **F7. How much Assemble replaces.**
  - (a) The named contributors' entries only, in one write. Drafted.
  - (b) The whole registry, rebuilt from every contributor each time.
- **F8. Where Fetch places the snapshot.**
  - (a) In the caller's directory: staged beside it, then renamed into
    place. Drafted.
  - (b) In a cache directory the Nexus owns, keyed by hash. This comes
    close to the store this design leaves out.
- **F9. A Local source on another host.**
  - (a) Refused with `ElsewhereHost`. That host's own Source nexus serves
    it. Drafted.
  - (b) This Nexus reaches the other host itself, over SSH.
- **F10. SourceName.**
  - A `String` now. Later, a checked camelCase word name, as in
    `identifier.md`. The cost of the word-database check is the subject of
    a separate book order.
- **F11. Where the shared library lives.**
  - (a) In its own repository, with its name open. Drafted.
  - (b) Inside `signal-source`, which peers depend on anyway.
- **F12. How the Ethos registry relates to this one.**
  - (a) Its key is a registered `SourceName`, and the Ethos Nexus refuses
    an unregistered one. Drafted.
  - (b) The two namespaces are independent.
  - (c) No Ethos registry is stored. The emitted path is derived from
    the fetched source's own crate name.
- **F13. Revision.**
  - (a) A full commit id only. Drafted.
  - (b) A branch or tag is also allowed, resolved and then pinned.
