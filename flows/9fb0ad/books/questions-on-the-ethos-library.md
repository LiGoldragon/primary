Presentation.{ «Questions on the Ethos library» }

You asked for my questions on an Ethos core library before a new flow designs it. What the vision already settles, so I don't ask it: ethos has four roots and Library is what the others share; a type used in more than one place is declared once and named, and past about three levels deep it comes from a Library; an ethos file carries no version, a version lives in a manifest; a library is imported by a bare name before the colon, as `protos:String` is today. The flow id in three camelCase words is the first thing every component would share. Four questions, on that example.

## 1. What the core holds, and what it is called

The word-id codec and its FlowId type belong to every component. Candidates for the same shelf: Layer (Primary…Quaternary), Aspect, Voice, the datom intrinsics (String, Integer, Vector…) that today need no import. Example: Flow's Library root would read `[ ethos-core:[ FlowId Voice Layer ] ]`.

1. One core library holding identity, voices and layers, named `ethos-core`.
2. Several small libraries — `identity` (the word id), `voice`, … — each imported by its own name.
3. The intrinsics join the core too, so `protos:` disappears and every import comes from one place.

## 2. The manifest: what it carries, and for what

Today's manifest is each Rust crate's Cargo.toml, so an ethos version rides a crate version. Example: Flow depends on the core at 1.0.0; the core changes the word list; what moves?

4. One manifest per repository, beside its ethos files: the library's name, its version, and its dependencies by name and version — like a Cargo.toml for ethos, generated into Cargo.toml.
5. Dependencies named by content fingerprint, not version: the manifest records the hash of the library it was built against, and a version is only a human label on that hash.
6. Both: the version for people, the fingerprint for the machine, the manifest checked against the fingerprint at generation.

## 3. The registry and index: where a library is found

Example: a flow writes `ethos-core:FlowId`; ethos-zero must find the core. Today the generator is handed a path.

7. A registry file in Primary (or in Curriculum) mapping library name → repository and fingerprint, the way a Nix flake registry maps names to inputs.
8. A Library Nexus that serves libraries over the wire by name and fingerprint, with the registry as its Memory — the registry is a running thing, not a file.
9. The repository itself is the registry: a library is found by its name as a repository under the same forge, no index at all.

## 4. Who may change the core, and what a change does

Spirit forbids compatibility paths: a change to the core updates every consumer. Example: the word list grows from 2048 to 4096 words; every FlowId printed so far still reads, every consumer regenerates.

10. Only the primary Mind lands a core change, and the landing regenerates and republishes every consumer in the same act (the registry says who the consumers are).
11. Anyone lands a core change; consumers are repinned by their own flows when they next build; the registry shows who is stale.

Name one from each point, or write what I have not asked.
