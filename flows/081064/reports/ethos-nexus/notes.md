# Ethos Nexus: grounds, seams, forks

F = `/home/li/primary/flows/`. E =
`F081064/vision/ethos.md`, S =
`F058f16/vision/source.md`, I =
`F058f16/vision/identifier.md`, all 2026-10-10, STT,
relayed.

Five files, one root each, on the Message pattern
(`F73ada7/reports/message-flow/`). None was run
through ethos-zero (by order). Accepted by the current
generator.
Imports follow Message's naming: `ethos_library` is
ethos.library.ethos; `source_ethos` is the shared
sources library 058f16 drafts; `ethos_zero` is
ethos-zero's error.ethos, whose `Error` and
`Location` were read from that file.

## Types and the words they serve

- The roots Signal, Memory, Operation: "In Ethos I
  want to specify the three aspects: the signal, the
  memory, the operation" (E). Library and the meta
  Signal come from the Message pattern.
- Memory `Registry`: "This will be used to put
  together a registry and it'll just keep it." (E).
- `Part`, meta `Load`/`Unload`, operation
  `Register`/`Unregister`: "populated from multiple
  sources using the datom files that can be in the
  repositories ... updated by whoever updates that
  repo. It can then be loaded along with other
  repositories to create a full registry." (E, S).
  Load replaces one repository's part whole: "use
  the same atomically updatable approach" (E), which
  points at the configuration record "loaded
  atomically so that it can live in separate files
  in different repositories ... on the meta socket"
  (`F73ada7/vision/nexus.md`, 2026-10-09 20:41; that
  reference is a gathering subflow's claim, logged
  in `F081064/log.md`). The meta socket also from
  "those payloads live on the meta signal (to modify
  those registries)" (`Fd5df1d/vision/ethos.md`,
  2026-10-09).
- `Duplicate`, and a changed part on every rename:
  "Every time we update some Ethos source, add one,
  or edit its name or something, we need to change
  the registry." (E).
- `Entry`, `EthosName` to `RustPath`, `Resolve`: "if
  it starts with a small letter, then that means
  it's pulling in from the registry name"
  (`Fd5df1d/vision/ethos.md`, 2026-10-09). An entry
  naming its emitted path is option 8b of
  `Fd5df1d/reports/inline-import-questions-spec.md`,
  which records 8b as witnessed by 1d0733 (claim).
- `EthosName.String`: "the prototype name, which is
  an uncapitalized identifier ... composed of words"
  (I). No such type exists yet; String stands in
  (pull 1).
- `SourceName` apart from `EthosName`: "the name of
  the repo and the name in the registry ... doesn't
  have to be the same" (S). Inference: an ethos name
  names one library file, and one repository can
  carry several, as Message's carries five.
- `Fetch`, `Unfetched`, `SourceUnreachable`: "use
  the source nexus and send it a source request and
  then you'll get a source" (S); "The hash is there
  for us so that we can verify that the files are
  the right files when we use them." (S).
- `Generate`, `Check`, `Rejected`: generation and
  checking stay Ethos's work (the brief). They
  mirror ethos-zero's own contract (ethos-zero.ethos
  at b2fa8b0) with a `Module` in place of a file
  path.
- Typed `Refused` and `Failed`, and one operation
  per effect (`Fetch`, `Write`, `Store`, `Register`,
  `Unregister`): "errors are vocabulary, never
  strings" and "Every effect has a matching
  operation type" (vision-nexus, as quoted in
  Message's notes; claim, not read here).
- `Standard`, `MetaConfigured`, ordinary `Configure`
  until configured, `RestartRequired`,
  `StoreRefused`: the Message pattern, unchanged.

## Seam with the Source nexus

058f16 designs Source; at this reading `F058f16/`
holds no design (witnessed: only `log.md`,
`vision/`).

- Ethos asks `Fetch.Module`, `Module.{ SourceName
  RelativePath }`: one file in one source.
- Source answers the file's text, verified against
  the hash it keeps (`Fetched.String`), or a refusal
  in its own vocabulary (`Unfetched.SourceRefusal`);
  no answer is `SourceUnreachable`.
- Ethos needs three names from `source_ethos`:
  `SourceName`, `RelativePath`, `SourceRefusal`. The
  names are inference until 058f16's library lands;
  so is the answer's form (text, or a verified
  snapshot's local path).
- Ethos holds no hash, revision, host path or
  fetcher: "It can refer to a certain Git with a
  certain revision and we keep our own Blake3
  hashes" and "different types of backend fetchers"
  (S). Inference in support: a repository's own
  datom file cannot hold the hash of the snapshot
  that contains it, so the hash sits outside the
  repository, in Source.
- Load does not ask Source whether the part's
  `SourceName` exists (inference; smallest shape,
  open).

## Seam with Flow

- No wire seam. Inference: resolution and generation
  depend on no caller, so Ethos, unlike Message, has
  no Flow edge and no caller identity.
- Flow's library is one registry entry like any
  other: the `flow_ethos` that Message imports
  resolves through a part from Flow's repository
  (inference; the spec's 8b example maps `flow` to
  `signal_flow`).
- Loading uses the start-up path the living named
  for the Flow Nexus (20:41 above): the CLI reads
  each repository's datom file and sends `Load` in
  succession, since "There should be no datom in any
  Nexus." (`F8475a9/vision/datom.md`, 2026-10-05).

## One registry or two

His words: "Only the source content addressing
registry needs to be updated." and the skill "refers
by name to the source" (E); "make the nexus for all
the sources and reuse it for all components, then we
only have one place to fix the sources aspect" and
"We have different registries in fact." (S).

As they answer it: one content-addressing registry
for every component, in the Source nexus, shared
through the sources library (with Source's
Git-equivalence registry beside it). The Ethos Nexus
keeps its own registry of ethos names, which names
sources and holds no hash; Curriculum's skills point
by name into the same Source registry. So the two
registries of the spec's Q6 are not one type: they
do different jobs in two Nexuses. Inference: once
migrated, ethos-zero reads resolution from the Ethos
Nexus (`Resolve`).

Tension for the living: on 2026-10-09 the registry
entry keyed `{ Subaspect Topic:Name }` held "the
containing source with hash ... and relative path"
(`Fd5df1d/vision/ethos.md`); the 2026-10-10 words
keep the hash in the source registry alone. This
draft follows the later words; whether they correct
the earlier is his to say. Under this draft a
content update changes Source's hash and leaves the
ethos registry alone (inference). If he means the
ethos registry pins a hash, that is variant H:

```
ethos.library.ethos
-                RelativePath ] ]
+                RelativePath
+                Blake3 ] ]
-         RustPath }
+         RustPath
+         Blake3 }
ethos.operation.ethos
- Fetch.Module
+ Fetch.{ Module Blake3 }
```

## The core fork, unruled

The files carry the lines all three options share;
those coincide with option B's own text. Each option
is one named difference.

- A, CoreCrate (spec 8a): `core` emits from one
  fixed crate held in configuration (which crate is
  unruled); a part that registers `core` is refused.
- B, CoreEntry (spec 8b): `core` is an ordinary
  entry in the core library repository's part;
  unregistered, it answers `Unknown`. No line
  changes.
- C, CoreRefused (spec 8c, item 7): no part may
  register `core`; `Resolve` answers `Unknown`;
  Generate and Check refuse it in ethos-zero's own
  vocabulary (item 7's `Source.String` in
  error.ethos, outside these files). The spec
  records that item 7 refuses the living's own key
  `Topic.core:Name` (claim).

```
A: ethos.library.ethos
-      Source.String }
+      Source.String
+      Core.RustPath }
A, C: ethos.meta.signal.ethos
-      StoreRefused ] ]
+      StoreRefused
+      CoreReserved ] ]
```

## This draft's own choices (inference)

- A part is replaced whole; `Unload` removes a
  repository; `Absent` refuses removing a missing
  part.
- `Generate.{ Module Target.String }` writes into a
  local folder, as ethos-zero's Generate does.
- Generation runs inside the Nexus, which therefore
  reads ethos text.
- Memory reads are not operations, as in Message;
  `Resolve` reads Memory.
- `Wrote.Path` and `Unwritable.Target` reuse a name
  declared inline in the same file ("the type takes
  that name in the file's namespace",
  knowledge-ethos); unwitnessed by ethos-zero.

## Pulls

1. Strings in the Nexus. `EthosName`, `RustPath`,
   the fetched text and the written Rust are
   strings, against "It's going to be forbidden for
   string handling to be in the Nexus."
   (`F8475a9/vision/datom.md`, 2026-10-05); the same
   pull as Message's pull 1.
2. The migration. "We need to migrate the Ethos
   Nexus version so that we can do this." (E). Until
   the Nexus runs, how ethos-zero reaches a registry
   (spec 6d, 6e, 6f) is untouched by these files.
3. A part is the ethos share of "the datom files ...
   that essentially wrap all of the data in that
   particular repository" (E); inference: the CLI
   takes the ethos entries out of that file before
   `Load`.
