# The Ethos Nexus

## Ethos today, and the Nexus it becomes

Ethos today is Ethos Zero: a generator run by
request. It opens no socket and keeps no store, so
it is not a Nexus (vision-ethos, sections "Zero"
and "Generation"). Every request brings the whole
of what it needs; nothing is remembered between
requests.

A Nexus has three parts, each its own ethos file:
Signal is what it says, Operation what it does,
Memory what it remembers (vision-nexus, "Three
parts and one path"). The Message Nexus, as drafted,
is the pattern this book follows: five ethos files,
one root each. A Library holds what the parts
share; one Signal file serves the ordinary socket
and one the meta socket; then Operation and Memory.

The Ethos Nexus drawn here keeps a registry. Each
repository carries its own datom part naming the
ethos sources it holds. The parts are loaded on the
meta socket and together make the registry. A
lowercase source name in an ethos file resolves
through it. The file's content comes from the
Source nexus, which also keeps the hashes.

```
+-------------+ +-------------+ +-------------+
| repository  | | repository  | | repository  |
| datom part  | | datom part  | | datom part  |
+------+------+ +------+------+ +------+------+
       |               |               |
       +---------------+---------------+
                       |
                       | meta signal
                       | Load.Part, one per repo
                       v
+--------------------------------------------+
| Ethos Memory: the registry                 |
|   name  ->  source, relative path          |
|   one part per repository                  |
+----------------------+---------------------+
                       |
                       | read by
                       v
+--------------------------------------------+
| Ethos Signal, ordinary socket              |
|   Resolve   Generate   Check               |
+----------------------+---------------------+
                       |
                       | Fetch: source name
                       |   + relative path
                       v
+--------------------------------------------+
| Source nexus                               |
|   gives the file's content                 |
|   keeps the hashes                         |
+--------------------------------------------+
```

Nothing of this is in production: no Ethos Nexus
exists, and the five files below are a draft in
this flow. All five are accepted by the current generator.

The records this rests on:
flows/081064/vision/ethos.md, 2026-10-10 (the
registry's anatomy and the Ethos Nexus with signal,
memory and operation; a Nexus called sources; one
source nexus for all components; the shared sources
library); flows/d5df1d/vision/ethos.md, 2026-10-09
20:07 (the registry keyed by subaspect and topic,
holding the containing source with its blake3 and
relative path; its payloads on the meta signal);
flows/73ada7/vision/nexus.md, 2026-10-09 20:41
(configuration loaded atomically from datom
payloads living in separate repositories, sent on
the meta socket). This last record is what the
2026-10-10 words name as the atomically updatable
approach; that reading is the flow's.

## The proposal: the Ethos Nexus, in vision-ethos

The proposal adds one section, "The Ethos Nexus",
to psyche-skills/vision/ethos.md, after
"Generation". Its lines are in the Distillation
section, D1. Here is the code they describe.

### The ethos it uses

- Roots. `Library` holds what the parts share. Its
  sections are imports, types, traits, associations.
  `Signal` holds queries and responses, and
  becomes `enum Query` and `enum Response`.
  `Operation` holds operations and outcomes, one
  operation for every effect. `Memory` holds the
  record types the Nexus keeps. Every root's first
  section is its imports.
- Imports. `source_ethos:[ SourceName RelativePath ]`
  takes two names from one library. Here
  `source_ethos` is the shared sources library and
  `ethos_library` is Ethos's own Library file.
- `Name.Type` declares a name over a type.
  `EthosName.String` is a lowercase name held as a
  string. In a variant, `Load.Part` is the query
  Load carrying a Part. The current generator turns
  every bare `Name.Type` (`EthosName.String`,
  `RustPath.String`, `Registry.Vector<Part>` and
  the rest) into a type alias, not a new type. That
  is the known generator defect whose ruling is
  Fork 3 of the open types book.
- A brace, `Name.{ … }`, is a struct: positions in
  order, each field named after its type. A struct
  variant such as `Generate.{ Module Target.String }`
  generates a `Generate_Data` struct.
- A bracket where types are declared, `Name.[ … ]`,
  is an enum. `Refused.[ … ]` is a closed list of
  refusals, so errors are words, never strings.
- `Vector<Entry>` is a list of entries.
- A position may declare its type in place:
  `Ordinary.String` inside a brace declares the
  alias `Ordinary` and the field that holds it.

### Library: what the parts share

```
; Ethos's own Library: what its roots share

Library
[ source_ethos:[ SourceName     ; Source's names
                 RelativePath ] ]
[ Configuration.{               ; startup config
     Ordinary.String            ; socket paths
     Meta.String
     Source.String }            ; the Source edge
  EthosName.String              ; a lowercase name
  RustPath.String               ; what is written
  Entry.{ EthosName             ; one ethos source:
          RelativePath          ; its library file
          RustPath }            ; and its Rust path
  Part.{ SourceName             ; one repository's
         Vector<Entry> }        ; ethos sources
  Module.{ SourceName           ; an ethos file by
           RelativePath } ]     ; source and path
[]                              ; traits
[]                              ; associations
```

An `Entry` is one ethos source: its name, the file
it lives in, and the Rust path the generator writes
for it. A `Part` is one repository's entries under
that repository's source name. A `Module` is what
Ethos asks the Source nexus for: one file in one
source.

### Memory: what Ethos remembers

```
; What Ethos remembers: its configuration and
; the full registry, one part per repository

Memory
[ ethos_library:[ Configuration Part ] ]
[ Standard.{                    ; the standard tree
     Configuration
     MetaConfigured.Boolean }
  Registry.Vector<Part> ]       ; the full registry
```

The registry is the parts, one per repository.
`Standard` is the metadata tree every Nexus keeps,
as in the Message pattern.

### Meta Signal: the registry is changed here

```
; What Ethos says, on its meta socket: the
; configuration and the registry's parts

Signal
[ ethos_library:[ Configuration ; shared types
                  EthosName
                  Part ]
  source_ethos:SourceName ]     ; a repository
[ Configure.Configuration
  Load.Part                     ; replaces that
                                ; repository's part
  Unload.SourceName ]           ; its part leaves
[ Configured
  RestartRequired               ; a socket changed
  Loaded
  Unloaded
  Refused.[                     ; typed refusals
     Duplicate.EthosName        ; held by a part
     Absent.SourceName          ; no part to remove
     StoreRefused ] ]
[]                              ; types
```

`Load.Part` puts in one repository's part, or
replaces the part it already has. `Unload` takes a
repository's part out. If a name is already held by
another repository's part, Load is refused with
`Duplicate`.

### Signal: what Ethos says to its ordinary peers

```
; What Ethos says, on its ordinary socket

Signal
[ ethos_library:[ Configuration ; shared types
                  EthosName
                  RustPath
                  Module ]
  source_ethos:SourceRefusal    ; Source's refusals
  ethos_zero:[ Error            ; the reader's
               Location ] ]     ; vocabulary
[ Resolve.EthosName             ; a name to its path
  Generate.{ Module             ; write its Rust
             Target.String }    ; into this folder
  Check.Module                  ; read it whole
  Configure.Configuration ]     ; until configured
[ Resolved.RustPath
  Generated.Vector<String>      ; the files written
  Checked
  Configured
  Refused.[                     ; typed refusals
     Unknown.EthosName          ; no registry entry
     Unfetched.SourceRefusal    ; Source said no
     SourceUnreachable
     Rejected.{ Module          ; the file is wrong
                Location
                Error }
     Unwritable.Target
     AlreadyConfigured ] ]
[]                              ; types
```

`Resolve` turns a lowercase name into the Rust path
the generator writes. `Generate` and `Check` are
Ethos Zero's two requests, given a `Module` where
Ethos Zero takes a file path.

### Operation: what Ethos does

```
; What Ethos does: one operation for every effect

Operation
[ ethos_library:[ Configuration ; shared types
                  Part
                  Module ]
  source_ethos:[ SourceName     ; Source's names
                 SourceRefusal ] ]
[ Fetch.Module                  ; ask Source for it
  Write.{ Path.String           ; write one module
          Rust.String }         ; of generated Rust
  Store.Configuration           ; write Memory
  Register.Part                 ; replace a part
  Unregister.SourceName ]       ; remove a part
[ Fetched.String                ; the file's text
  Wrote.Path
  Stored
  Registered
  Unregistered
  Failed.[                      ; typed failures
     Unfetched.SourceRefusal
     SourceUnreachable
     Unwritable.Path
     StoreRefused ] ]
[]                              ; types
```

`Fetch` is the one edge to the Source nexus. The
Source nexus checks the content against the hash it
keeps; Ethos holds no hash and no revision.

The three names taken from `source_ethos`
(`SourceName`, `RelativePath`, `SourceRefusal`) are
the flow's guess, until the shared sources library
is drafted. The current generator emits them
unresolved, and they stay untested until that
library exists. The flow's guess is also that Ethos has
no edge to Flow: resolving and generating depend on
no caller.

### Wrong and right: where the hash lives

Wrong: the entry copies what Source keeps. A hash
and a Git revision sit in Ethos and in Source. Each
commit to a repository then changes both
registries, and the two can disagree.

```
; wrong: Ethos keeps what Source keeps
Library
[ source_ethos:[ SourceName      ; Source's names
                 RelativePath ] ]
[ EthosName.String               ; types
  RustPath.String
  Entry.{ EthosName              ; one ethos source:
          RelativePath           ; its library file
          Blake3.String          ; Source's hash
          Revision.String        ; Source's revision
          RustPath }             ; its Rust path
  Part.{ SourceName              ; one repository's
         Vector<Entry> } ]       ; ethos sources
[]                               ; traits
[]                               ; associations
```

Right: Ethos keeps names and paths. The hash and the
revision stay in the Source nexus, the one place
that fixes the sources aspect.

```
; right: Ethos keeps names; Source the rest
Library
[ source_ethos:[ SourceName      ; Source's names
                 RelativePath ] ]
[ EthosName.String               ; types
  RustPath.String
  Entry.{ EthosName              ; one ethos source:
          RelativePath           ; its library file
          RustPath }             ; its Rust path
  Part.{ SourceName              ; one repository's
         Vector<Entry> } ]       ; ethos sources
[]                               ; traits
[]                               ; associations
```

Question 1 asks whether the hash, though not the
revision, comes back into the entry. If you rule
that it does, the `Blake3` line moves from wrong to
right. The revision stays wrong either way: the
2026-10-10 record puts Git revisions in Source's
own Git-equivalence registry.

## Questions for your ruling

### 1. Where the hash lives

The 2026-10-09 record (flows/d5df1d/vision/ethos.md,
20:07) puts the containing source's blake3 in the
registry entry, beside the relative path. The
2026-10-10 records (flows/081064/vision/ethos.md, "a
Nexus called sources" and "a shared sources
library") put every hash in the Source nexus, with
only that content-addressing registry needing
updates. The draft follows the later words. Whether
they correct the earlier ones is for you to say.

Example: one field is added to the Message Nexus's
signal file.

- The later words, as drafted: Source takes a new
  snapshot, and its hash for that repository
  changes. The ethos registry does not change. The
  next `Fetch` returns the new text, checked by
  Source.
- Variant H, the hash in the entry: the repository's
  part must carry the new hash, so every content
  commit means a new `Load.Part`. The flow's
  inference: a part that lives inside its
  repository cannot hold the hash of the snapshot
  that contains it. So under H the part would be
  written outside the repository, or the hash would
  cover one file instead of the source.

Variant H, as lines:

```diff
ethos.library.ethos
-                RelativePath ] ]
+                RelativePath
+                Blake3 ] ]
-          RustPath }
+          RustPath
+          Blake3 }
ethos.operation.ethos
- Fetch.Module
+ Fetch.{ Module Blake3 }
```

Rule: the later words stand (no hash in Ethos), or
H.

### 2. What the generator writes for `core`

The registry line you approved on 2026-10-10 waits
on this fork (see D2). Example: an ethos file
declares `Id.core:Identifier`, a type from `core`.
Under a the generator writes the name fully
qualified from the crate Configuration holds for
`core`; under b it writes the path `core`'s own
entry names; under c it refuses the file. In this
anatomy the three options become:

a. `core` is a crate of its own. Its fixed path is
   held in Configuration, and a part that registers
   `core` is refused.

```diff
ethos.library.ethos
-      Source.String }
+      Source.String
+      Core.RustPath }
ethos.meta.signal.ethos
-      StoreRefused ] ]
+      StoreRefused
+      CoreReserved ] ]
```

b. `core` is an ordinary registry entry. The core
   library repository's part names the path it
   emits, as every other part does. No ethos line
   changes: the files above are already option b.
   The difference is only in data. A sketch of the
   core repository's Load, written by the flow and
   not read by any reader:

```
Load.{ ethosCore
       [ { core
           core.library.ethos
           ethos_core } ] }
```

c. `core` is reserved and refused. No part may
   register it, `Resolve` answers `Unknown`, and
   Generate and Check refuse it in Ethos Zero's own
   vocabulary, outside these files. The flow notes
   a consequence: c refuses your own example key
   `Topic.core:Name`.

```diff
ethos.meta.signal.ethos
-      StoreRefused ] ]
+      StoreRefused
+      CoreReserved ] ]
```

The flow's reading: under a and c, D1's line on
resolution covers every source except `core`. D2 names the exception.

Rule: a, b or c.

### 3. A repository's part is replaced whole

The draft never edits entries one at a time.
`Load.Part` replaces the repository's whole part,
and `Unload` removes it. The flow takes this from
the atomic configuration loading of 2026-10-09
20:41.

Example: the flow repository renames its library
`flow` to `flowSignal`. The CLI reads the
repository's datom file again and sends one
`Load.Part` holding every entry of that repository.
Ethos swaps the old part for the new one in one
step. Nothing reads a half-renamed registry. If
another repository's part already holds
`flowSignal`, the whole Load is refused with
`Duplicate`, and the old part stays.

The amendment would be to edit entries. A sketch,
the flow's:

```diff
ethos.meta.signal.ethos
-  Load.Part
+  Load.Part
+  Add.{ SourceName Entry }
+  Remove.EthosName
+  Rename.{ EthosName EthosName }
```

With that, a rename is one message. The flow's
inference: a repository's datom file and the
registry can then drift apart.

Rule: confirm whole-part replacement, or amend.

### 4. The names the flow coined

None of these names is in your words; the flow
chose each one. Example of the names at work: the
CLI sends `Load.Part` on the meta socket for the
flow repository; a peer sends `Resolve.flowSignal`
and `Resolved.RustPath` answers; Ethos asks
`Fetch.Module` of the Source nexus for the file.

- `Part`: one repository's share of the registry.
- `Entry`: one ethos source in a part.
- `EthosName`: the lowercase name an entry carries.
  When the prototype name type exists, it will hold
  this name; `String` stands in until then.
- `RustPath`: the path the generator writes for a
  name.
- `Resolve`: a name to its Rust path, on the
  ordinary socket.
- `Load` and `Unload`: a part in or out, on the meta
  socket.
- `Fetch`: Ethos asking the Source nexus for a
  file. The 2026-10-10 record
  (flows/058f16/vision/source.md) names a source
  request and its answer; `Get` or `Source` would
  follow it more closely.

The flow also coined `Module`, `Register`,
`Unregister`, `Write` and `Store`. They follow the
same ruling unless you name them.

Rule: keep, or give a new name for each.

## Distillation

### D1. The Ethos Nexus, a new section of vision-ethos

Target: psyche-skills/vision/ethos.md, the
vision-ethos skill. Place: after the "Generation"
section, before "## Sources".

Removed: none.

Above, unchanged:

~~~text
## Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```

~~~

Added:

```diff
+## The Ethos Nexus
+
+The Ethos Nexus has three parts, Signal, Memory
+and Operation, each written in ethos.
+
+Its Memory is a registry of ethos names. Each
+repository carries one datom part naming its
+ethos sources; each part is loaded whole on the
+meta signal, and the parts together make the
+registry. The registry changes whenever a source
+is added, removed or renamed.
+
+A lowercase source name resolves through the
+registry to the path the generator writes.
+
+The content of an ethos file is fetched by name
+from the Source nexus, which keeps the hashes.
+
```

Below, unchanged:

```text
## Sources

01a02a34 ethos
```

If question 1 rules H, the last paragraph is replaced by:

```diff
-The content of an ethos file is fetched by name
-from the Source nexus, which keeps the hashes.
+Each registry entry holds the blake3 of its
+containing source; the content of an ethos file
+is fetched by name from the Source nexus.
```

If question 3 amends, "each part is loaded whole
on the meta signal" reads "parts and their entries
are changed on the meta signal".

### D2. The registry line, with the fork filled

Target: psyche-skills/vision/ethos.md, the Imports
section. Place: after the inline-import paragraph,
before "## What a declaration turns into". This is
the line approved on 2026-10-10, with ⟨the fork⟩
filled by question 2's ruling.

Removed: none.

Above, unchanged:

```text
A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.

```

Added, with one of the three fillings:

```diff
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is ⟨the fork⟩.
+
```

a. the name fully qualified from the one crate the
   Nexus is configured with for `core`
b. the path that `core`'s registry entry names, as
   for every other source
c. nothing: `core` is not a source, and a name from
   it is refused

Below, unchanged:

```text
## What a declaration turns into
```

### D3. Sources

Target: psyche-skills/vision/ethos.md, the Sources
section, appended after its last line.

Above, unchanged:

```text
88475f ethos
d5df1d ethos
```

Removed: none.

Added:

```diff
+081064 ethos
+73ada7 nexus
```

**Ruling.** 1: the later words, or H. 2: a, b or c.
3: confirm, or amend. 4: keep, or rename, name by
name. D1, D2 and D3 land with those answers. Or
amend any line.
