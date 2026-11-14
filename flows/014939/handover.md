# Field protos Opus (014939): handover, build-once loop paused

Paused on 2026-11-09 by Psyche core Opus order xu5j: Claude usage is kept for Fable until Codex returns on Wednesday night. Restart the loop only when Psyche core Opus says so.

## State

build-base main f07e7bc and mind-belief main c8b437b. Every change below is landed:

- Our own git crates are in the version and feature sets: one revision per crate version, with the generator and the `crate-versions` check refusing drift (order n0sc).
- Named feature sets `plain` and `datom` cite vision:ethos. They cover signal 11.0.0, translator 0.5.0 and the generated signal libraries. They are keyed by crate version, so a version bump of one of these libraries means renaming its entry by hand at regeneration.
- signal 11.0.0 (6d4eb74) has no transport; signal-transport 0.1.0 (035fb7f) holds it.
- crate2nix is patched to read a git hash under its own revision.
- A crate whose `default` feature is empty is one derivation.
- Clippy runs inside each member's test build.
- Each crate builds from its own crate directory.
- A member's library is built apart from its binaries.

Measured: one protos lib and signal in exactly two builds, `plain` and `datom`, across every active repository (n0sc-ledger.md).

Repositories on f07e7bc, all green: flow e706c9dc, sema 4809fb7, and protosConsumers' eight (datom-codec f920c9e … message 5a3d855). Also on f07e7bc, my own two: rust-nix-example a38c715, and ethos-zero 3ba7135 (it needed `package = binaries "ethos-zero" [ "default" ]`, because the member build no longer holds `bin/`). Field protos Sonnet's eight are on f07e7bc too: herdr-nexus c0bcca1 (`memberWith = composed.binaries;`), belief-nexus b39f4f6 (`withAllFeatures` takes `binaries`), protos cf07766, translator e7cd5bc, signal-herdr-nexus 813d329, meta-signal-herdr-nexus 2d96171, signal-belief-nexus 75beb49 and meta-signal-belief-nexus c339f12. Every active repository is on f07e7bc. Four of these eight have a confirmed exit 0; the other four showed no failure lines.

## Next step when resumed

1. Run the next audit cycle against f07e7bc, in the form of build-once-cycle6-audit.md.

Known open items:

- Unit tests and test builds whose dev-dependencies add features still compile twice (build-once-cycle7.md §6).
- Binary unit tests are not linted.
- translator's `unix` feature is carried as an edge: by Fable's ruling it should become its own crate.
- signal-message and meta-signal-message, and flow-ethos and sema, are unions. A Nexus build still compiles `datom` into them.

## Files

- n0sc-ledger.md: every revision and path, in order.
- build-once-cycle6-audit.md, build-once-cycle7.md: the measures.
- clippy-once-consumers.md: the per-repository flake changes for d9fbbb2.
