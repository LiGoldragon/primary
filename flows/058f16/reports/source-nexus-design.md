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
this flow's inference: settled where one answer is right, otherwise an
open fork with its drafted option marked.

Witness: the six ethos drafts below (shared library, ordinary Signal, meta
Signal, Operation, Memory, meta CLI input) each passed `Check` and
`Generate` with ethos-zero 17.0.0, built by Nix from ethos-zero origin/main
`07714b`, on 2026-10-10. Each file was checked alone: imports across the
drafts were not resolved, and the generated Rust was not compiled.

## Shape

```
  caller (ethos, curriculum, a flow)
        |  Fetch / Check / Resolve
        v
  +---------------- source nexus ------------+
  | Signal ---> Operation ---> Memory        |
  |              |   ^          Registered   |
  |              v   |          Staged       |
  |      backend fetchers       Standard     |
  |      Git.{ remote revision }             |
  |      Local.{ host directory }            |
  |              |                           |
  |              v                           |
  |      staging beside the destination      |
  |      tree, minus the root .git           |
  |              |                           |
  |              v                           |
  |      Blake3 of its archive bytes,        |
  |      compared with the entry             |
  +------------------------------------------+
        ^  Assemble / Withdraw / Configure (meta socket)
        |
  source-meta CLI <--- sources.datom
                        in each repository
```

The repositories follow vision-nexus:

- `source`: the Nexus, plus its CLIs `source` and `source-meta`.
- `signal-source`: the ordinary socket's contract, including `Refusal`,
  which peers such as the Ethos Nexus import.
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
  RelativePath.String
  Fetcher.[ Git.{ Remote Revision }
            Local.{ Host Directory } ]
  Source.{ SourceName Fetcher Blake3 }
  Contributor.String
  Contribution.{ Contributor Vector<Source> } ]
[]
[]
```

- `SourceName` is the registry name. It does not need to match the
  repository's kebab-case name. It is a `String` (F10, settled).
- `Blake3` holds the 256-bit digest as four 64-bit `Integer`s, the
  stand-in while ethos has no byte type (F3, settled). Rust generates
  `first_integer` through `fourth_integer` as `i64`. The codec is exact:
  digest bytes 0–7 are read little-endian as the two's-complement bit
  pattern of `first_integer`, bytes 8–15 of `second_integer`, 16–23 of
  `third_integer`, 24–31 of `fourth_integer`; the reverse writes each
  `i64` back as eight little-endian bytes in the same order. No value is
  clamped and no sign crosses a chunk, so every digest has exactly one
  encoding and a negative integer is an ordinary encoding.
- `Revision` is a full Git commit id (F13, settled).
- `RelativePath` is a path inside a snapshot, `/`-separated, used to name
  an unsupported entry.
- `Contribution` is what one repository's datom file holds: the
  contributing repository's name and the sources it brings into the
  registry (F5).

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
be the snapshot of that revision that we hash". The entry named `.git` at
the snapshot's root, file or directory, is not part of it. Which other
files a Local snapshot includes is fork F2.

The bytes hashed are an archive of the tree in the Nix archive format
(`nix-archive-1`, as the Nix manual's archive specification gives it),
and the hash is Blake3 over those bytes (F1). In that format every string
is its byte length as an eight-byte little-endian integer, the bytes, and
zero padding to a multiple of eight. A regular file carries its contents
and an executable marker when any execute bit is set; a symlink carries
its target text; a directory carries its entries sorted by name, byte by
byte. This Blake3 is not a Nix `narHash`, which is SHA-256 of the same
bytes, and the two are never interchanged.

The supported entries are regular files, directories and symlinks. A
socket, a pipe or a device in a Local tree, and a submodule (gitlink) in a
Git tree, is refused as `Unsupported` with its `RelativePath`.

- A Git snapshot is the tree of the commit, read from the object
  database, never from a checkout: blob bytes as stored, with no
  clean, smudge, end-of-line or LFS filter. Mode `100644` is a regular
  file, `100755` an executable one, `120000` a symlink whose blob is the
  target, `040000` a directory, `160000` refused.
- A Local snapshot is the directory as read on the configured host.

A Git tree never holds an empty directory; a Local tree may. A Local and
a Git snapshot of the same content therefore hash equal only when the
Local tree has no empty directory.

The hash is checked on use. `Fetch` copies the source into staging,
hashes the staged tree, and places that same staged tree only on a match;
a Local directory that changed during the copy yields a different hash
and is refused, and a staged tree that hashes equal is the right tree
whatever the directory did meanwhile. `Check` hashes a directory the
caller already holds, as read during that `Check`; `Checked` says those
bytes matched and promises nothing about the directory afterwards. The
entry changes only when the repository's datom file changes and the
registry is assembled again.

## Signal: ordinary socket (`signal-source`)

```
Signal
[ sources:[ SourceName Blake3 Host Directory RelativePath Source ] ]
[ Resolve.SourceName
  Fetch.{ SourceName Directory }
  Check.{ SourceName Directory }
  Configure.Configuration ]
[ Resolved.Source
  Fetched.{ SourceName Blake3 Directory }
  Checked.{ SourceName Blake3 }
  Configured
  Refused.{ Refusal Leftover.Option<Directory> } ]
[ Configuration.{ Host Ordinary.SocketPath Meta.SocketPath }
  SocketPath.String
  Refusal.[ Unknown.SourceName
            Mismatched.{ SourceName Expected.Blake3 Found.Blake3 }
            Unfetchable.{ SourceName Unfetched }
            Unsupported.{ SourceName RelativePath }
            ElsewhereHost.Host
            Unconfigured
            Unreadable.Directory
            Occupied.Directory
            Unplaceable.Directory
            AlreadyConfigured
            StoreRefused ]
  Unfetched.[ RemoteUnreachable
              RevisionMissing
              DirectoryMissing ] ]
```

- `Resolve` returns the entry.
- `Fetch` writes the verified snapshot to the caller's directory, which
  must not exist yet and whose parent must exist on a writable filesystem
  (F8, settled).
- `Check` verifies a directory the caller already has.
- `Configure` on this socket is the first configuration of vision-nexus:
  it is accepted only while the meta Configure has never been done, and
  is refused `AlreadyConfigured` after.
- `Leftover` names a staging directory that could not be discarded after
  a refusal. The refusal itself is never replaced by the discard failure.
- `ElsewhereHost` answers a Local source whose `Host` differs from the
  configured `Host`, compared as exact strings (F9, settled).
  `Unconfigured` answers a Local source before any Configure, since no
  host identity exists yet.

Examples (hash integers are illustrative):

```
source 'Resolve.ethosZero'
Resolved.{ ethosZero
           Local.{ prometheus /git/github.com/LiGoldragon/ethos-zero }
           { -5 31 2026 7714 } }

source 'Fetch.{ psycheSkills /home/li/work/psyche-skills }'
Fetched.{ psycheSkills { 812 -77 4410 9 } /home/li/work/psyche-skills }

source 'Check.{ ethosZero /git/github.com/LiGoldragon/ethos-zero }'
Refused.{ Mismatched.{ ethosZero { -5 31 2026 7714 } { 66 -1 3 90 } }
          None }

source 'Fetch.{ spirit /home/li/work/spirit }'
Refused.{ Unknown.spirit None }

source 'Fetch.{ ethosZero /home/li/work/ez }'     ; asked on ouranos
Refused.{ ElsewhereHost.prometheus None }
```

## Signal: meta socket (`meta-signal-source`)

```
Signal
[ sources:[ SourceName Contributor Contribution ]
  signal_source:Configuration ]
[ Assemble.Vector<Contribution>
  Withdraw.Contributor
  Configure.Configuration
  Read ]
[ Assembled.Integer
  Withdrawn.Contributor
  Configured
  Current.Configuration
  Refused.Refusal ]
[ Refusal.[ Conflicting.{ SourceName Vector<Contributor> }
            Duplicated.Contributor
            Malformed.SourceName
            Unregistered.Contributor
            StoreRefused ] ]
```

`Assemble` replaces the entries of every contributor it names, all in one
Memory write (F7, settled). It is refused whole, with the registry and
every ownership record unchanged, when:

- a contributor appears twice in the request (`Duplicated`);
- an entry's Git `Revision` is not a full commit id (`Malformed`);
- the same `SourceName` has different entries, from contributors in the
  request or already in the registry (`Conflicting`).

Equal entries from two contributors are not a conflict. Each contributor
keeps its own record of the entry, so `Withdraw` of one leaves the entry
registered through the other. `Assembled` answers with the number of
distinct `SourceName`s now registered.

The meta socket carries the Configure of vision-nexus. `Configuration`
holds the standard values (the two socket paths) and the Source nexus's
one value of its own, its `Host`. The Source nexus has no edge socket, so
the standard tree lists none. `Read` answers the stored configuration. The
built-in default configuration holds the default socket paths, on which
the first Configure arrives. The meta socket file is readable and writable
by the Nexus's own user only; that file permission is its admission.

The `source-meta` CLI reads each repository's `sources.datom`, composes
the `Contribution`s and sends them as signal, so datom stays out of the
Nexus (F6). Its input is its own type, distinct from the meta Signal it
sends:

```
Library
[ sources:Contributor
  signal_source:Configuration ]
[ Repository.String
  MetaInput.[ Assemble.Vector<Repository>
              Withdraw.Contributor
              Configure.Configuration
              Read ] ]
[]
[]
```

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

Every effect has its own operation: a registry read, a staging, a backend
fetch, a hash, a placement, a discard, a registry write and a
configuration write.

```
Operation
[ sources:[ SourceName Blake3 Fetcher Directory RelativePath Source Contributor Contribution ]
  signal_source:[ Configuration Unfetched ] ]
[ Look.SourceName
  Stage.Directory
  Materialize.{ Fetcher Staging.Directory }
  Hash.Directory
  Place.{ Staging Directory }
  Discard.Staging
  Replace.Vector<Contribution>
  Remove.Contributor
  Store.Configuration ]
[ Found.Source
  Staged.Staging
  Materialized.Staging
  Hashed.Blake3
  Placed.Directory
  Discarded
  Replaced.Integer
  Removed
  Stored
  Failed.Failure ]
[ Failure.[ Unknown.SourceName
            Unfetchable.{ Fetcher Unfetched }
            Unsupported.RelativePath
            Unreadable.Directory
            Occupied.Directory
            Unplaceable.Directory
            Undiscarded.Staging
            Conflicting.{ SourceName Vector<Contributor> }
            Unregistered.Contributor
            StoreRefused ] ]
```

- `Look` returns the entry, and the `Fetch` or `Check` holds that `Source`
  to its end: an `Assemble` landing meanwhile does not change what it
  verifies.
- `Stage` takes the destination and creates a new directory beside it, in
  the same parent and so on the same filesystem, with an exclusive create
  that never takes an existing path; its name is unique to the operation.
  It records the staging in Memory (`Staged`) before returning it.
- `Place` renames the staging onto the destination with a no-replace
  rename (Linux `renameat2` with `RENAME_NOREPLACE`), which refuses an
  occupied destination atomically and leaves the occupant untouched; a
  destination that appears during the fetch is refused `Occupied`.
- `Discard` removes the staging and its `Staged` record. `Place` also
  removes the record.
- A `Fetch` whose caller disconnects runs on to `Place` or `Discard`; its
  reply is dropped. After a crash, the Nexus discards every `Staged`
  record's directory when it starts.

Mapping from Operation to Signal:

| Operation | ordinary `Refusal` | meta `Refusal` |
|---|---|---|
| `Unknown` | `Unknown` | |
| `Unfetchable.{ Fetcher Unfetched }` | `Unfetchable.{ SourceName Unfetched }`, the name from `Look` | |
| `Unsupported` | `Unsupported.{ SourceName RelativePath }` | |
| `Unreadable` | `Unreadable` | |
| `Occupied` | `Occupied` | |
| `Unplaceable` | `Unplaceable` | |
| `Undiscarded` | the pending refusal, with `Leftover` set | |
| `Conflicting` | | `Conflicting` |
| `Unregistered` | | `Unregistered` |
| `StoreRefused` | `StoreRefused` | `StoreRefused` |
| `Hashed`, unequal to the entry | `Mismatched` | |

`ElsewhereHost`, `Unconfigured`, `AlreadyConfigured`, `Duplicated` and
`Malformed` are decided from values already held and need no operation.

A `Fetch` from query to response:

```
Fetch.{ psycheSkills /home/li/work/psyche-skills }   ; 1 Query
Look.psycheSkills                                    ; 2 Operation
Found.{ psycheSkills Git.{ ... } { 812 -77 4410 9 } }  ; 3 from Memory
Stage./home/li/work/psyche-skills
Staged./home/li/work/.source-stage-4127-1            ; 4 recorded
Materialize.{ Git.{ ... } /home/li/work/.source-stage-4127-1 }
Materialized./home/li/work/.source-stage-4127-1      ; 5 tree, no .git
Hash./home/li/work/.source-stage-4127-1
Hashed.{ 812 -77 4410 9 }                            ; 6 equal to the entry
Place.{ /home/li/work/.source-stage-4127-1 /home/li/work/psyche-skills }
Placed./home/li/work/psyche-skills                   ; 7 no-replace rename
Fetched.{ psycheSkills { 812 -77 4410 9 } /home/li/work/psyche-skills }
```

On a mismatch, step 7 is `Discard`, and the response is
`Refused.{ Mismatched... None }`, or `Leftover` set when the discard
failed. `Check` takes the same path without `Stage`, `Materialize`,
`Place` or `Discard`.

## Memory

```
Memory
[ sources:[ Contributor Source Directory ]
  signal_source:Configuration ]
[ Registered.{ Contributor Source }
  Staged.Directory
  Standard.{ Configuration MetaConfigured.Boolean } ]
```

- `Registered`: one record per contributor and source. `Replace` deletes
  the named contributors' records and writes the new ones in one
  transaction. Lookups by `SourceName` read these records; equal entries
  from several contributors answer as one.
- `Staged`: one record per staging directory not yet placed or discarded.
- `Standard`: the standard metadata tree. `MetaConfigured` records whether
  the meta Configure was ever done; only the meta socket sets it.

## The line with the Ethos registry

The Ethos topic's book «The Ethos Nexus» gives the Ethos Nexus its own
registry of ethos sources, each named within a repository by
`SourceName`. Ethos keeps names and paths; the hash and the fetcher stay
here.

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

The Ethos registry's key is a registered `SourceName` (F12, settled; the
Ethos Primary's position is the same). The Ethos Nexus refuses a part
whose `SourceName` the Source nexus does not `Resolve`, so a source is
assembled here before Ethos registers a part naming it. Source does not
depend on Ethos, so there is no circular start. An emitted Rust path is
never derived from a Cargo package name; it is what the Ethos registry
says. When the Ethos Nexus needs a source's files, it sends `Fetch` or
`Check` with that name, takes the whole snapshot, and maps this
`Refusal`, imported from `signal-source`.

## First acceptance

Not run. The first acceptance compiles the whole graph: the shared
library, `signal-source`, `meta-signal-source` and the `source` crate,
generated through ethos-zero with exact pins, built through Nix on the
NixBuilder. It uses temporary local directories and a fixed local Git
fixture, and tests:

- the four-integer codec: all-zero, all-one, each sign-bit boundary, a
  known Blake3 digest, and the round trip;
- the archive hash: entry order independence, a change of content, of
  the executable bit or of a symlink target each changing the hash, the
  root `.git` excluded, an unsupported entry refused, and a Git and a
  Local snapshot of the same tree hashing equal;
- `Fetch` to an absent destination, to an occupied one, and to one
  created while the fetch runs, the occupant intact each time;
- a mismatch leaving the destination absent and no staging behind;
- a Local directory changed after its entry, refused `Mismatched`;
- a conflicting `Assemble` leaving registry and ownership unchanged;
- a duplicate contributor refused; equal entries from two contributors
  surviving the `Withdraw` of one;
- the registry and configuration surviving a restart, and a leftover
  `Staged` directory removed on start;
- first configuration on the ordinary socket, then refused there after
  the meta Configure;
- one real `Fetch`, `Check` and `Resolve` exchange in binary signal
  between the CLI and the running Nexus.

## Settled

- **F3. The type of Blake3.** Four `Integer`s, with the exact codec in
  the library section. Whether ethos gains a byte type, and which, is the
  question of the Ethos topic's book «Bytes in ethos»; this design moves
  to its answer when there is one.
- **F7. How much Assemble replaces.** The named contributors' entries, in
  one write. Rebuilding the whole registry is an `Assemble` that names
  every contributor.
- **F8. Where Fetch places the snapshot.** In the caller's directory,
  staged beside it and placed by a no-replace rename. A cache the Nexus
  owns would be the store the living put outside the first lane.
- **F9. A Local source on another host.** Refused `ElsewhereHost`; that
  host's own Source nexus serves it. Reaching another host is the
  router's matter, outside this design.
- **F10. SourceName.** A `String`. The checked word name is the subject
  of the books «The prototype name» and «Word-built names».
- **F12. The Ethos registry.** Keyed by a registered `SourceName`, as in
  the section above.
- **F13. Revision.** A full commit id: 40 lowercase hexadecimal digits
  for a SHA-1 repository, 64 for a SHA-256 one. A branch or tag is
  resolved by a client before it reaches an entry; that client feature is
  not part of this design.

## Open forks

The living has not ruled on any of these. The option marked "drafted" is
the one the drafts above use. Each such choice is this flow's.

- **F1. What bytes the hash is taken over.**
  - (a) The tree in the Nix archive format, exact as above. Drafted.
  - (b) The rkyv archive of a typed tree value. This matches
    vision-nexus: "an encoded form fingerprints itself, by default the
    hash of its rkyv archive". Its byte layout would be fixed by the
    tree type's ethos.
  - (c) A Merkle tree of per-file Blake3 hashes, which a later store could
    use to avoid storing a file twice.
- **F2. What a Local snapshot includes.**
  - (a) Every file except the root `.git`, as the living's words say.
    Drafted. This includes build output such as `target/`, so a Local
    source's hash changes at every build inside it.
  - (b) Only the files Git tracks, in their working-tree state, as Nix's
    `git+file` does.
  - (c) Every file except those `.gitignore` excludes.
- **F4. The registry's shape.**
  - (a) One entry holding a name, one fetcher and a hash. Drafted.
  - (b) Two registries: name to Blake3, and Blake3 to fetchers. The second
    is the "Git equivalence registry" the living says can be dropped once
    Git is cut off. «The Ethos Nexus» reads his words this way.
- **F5. What a repository's datom file lists.** A file inside a
  repository cannot hold that repository's whole-tree hash, since writing
  the hash changes the tree; a Git revision likewise cannot be written in
  its own commit.
  - (a) The sources that repository uses, with their hashes, like a lock
    file. Drafted. Two repositories then cannot list each other.
  - (b) The repository itself, as in "wrap all of the data in that
    particular repository": its name and fetcher only. `source-meta`
    takes the hash, and for Git the revision, when it assembles.
  - (c) The repository itself, hash included, with the datom file left
    out of the bytes hashed.
- **F6. Who reads the datom files.**
  - (a) The `source-meta` CLI. Drafted. It reads files and sends a
    different shape than it was given, beyond vision-nexus's "a CLI turns
    text into Signal and nothing more".
  - (b) A separate assembler program reads them and sends the
    `Contribution`s; `source-meta` stays text into Signal.
- **F11. Where the shared library lives.**
  - (a) In its own repository, with its name open. Drafted.
  - (b) Inside `signal-source`, which peers depend on anyway.
