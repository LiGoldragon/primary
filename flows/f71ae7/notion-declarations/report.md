# A source declares its modules: branch report

Task 67w9, from Psyche core Opus. Nothing merged to main, deployed or restarted.

## Branches

- Curriculum `notion-declarations` at `59846c0d773d09b4c9c2a9b68fe62ba837f646f0`, on main 4695835.
- psyche-belief `notion-declarations` at `d77f70ec4b41da89ec7fc24506f853179a20b910`, on main 65bd154 (74 declarations).
- mind-belief `notion-declarations` at `1b36e132f899fba88819a8a3077e7b0e2e03f995`, on main 3ecf248 (38 declarations).
- field-belief `notion-declarations` at `a515b8017d5be6de0bb1130fcf979bb9b2e21620`, on main dc93e8c (16 declarations).
- goldragon-persona `mind-curriculum-opus` at `f6c5a1dc66d941e92a17d5c41df1448231ca70c1`, on cd9222c. It holds 39 permaflows. `{ Mind curriculum Opus }` follows `{ Mind curriculum Sol }`, copied byte for byte from the live Configure record `flows/743764/curriculum-opus/after.datom`.

## What changed in Curriculum

- `curriculum.ethos` declares `ModuleKind`, `ModuleVersions`, `ModuleFile`, `ModuleDeclaration` and `ModuleDeclarations`. `src/generated.rs` is regenerated with the pinned ethos-zero 16 (c2653dd), and the regeneration reproduces main's file exactly before the addition.
- The registry reads `modules.datom` at each root and nothing else. Each declaration gives `kind:subject:version` for every version it holds, with its text in the declared file. A file's own name and folder mean nothing. The old type-folder scan and the legacy `skills/` guard are gone.
- Some declarations admit no name: a name declared again (the first is kept, in the same root or an earlier one), an absent file, a file reached through a link or outside the root, an invalid name, or no version. Each is reported, and the rest is admitted. Reports are in `SkillRegistry::reports()`, and the Nexus writes them to stderr when it opens.
- A root with no readable `modules.datom` refuses admission. So do the refusals that were already there: overlapping roots, a bad module body or front matter, a missing dependency, and a cycle.
- Reading declarations needs the `datom` feature, the same as roles. Flow and Home build it with that feature.
- New tests are in `tests/declarations.rs`. The other tests declare their fixtures through `tests/support`. The layout-refusal tests that no longer apply were removed.
- Curriculum now has a flake on build-base. `Cargo.nix` and `crate-hashes.json` are flow c8f526c's `nix/curriculum` copies, and `checks.cargo-nix` proves them current. Clippy debt that main already had was cleared: a unit expression and `perform` written as an `async fn`.

## Gate

The gate ran with nix-fast-build `--remote` prometheus on the final revision (log: `gate.log` beside this report).

- `checks.curriculum` passed: lint-clean test build, 9 test binaries, all green.
- `checks.cargo-nix` passed.
- `checks.crate-versions` and `checks.crate-features` fail, so `default` fails too. Their findings come from main's Cargo.lock, not from this change. Curriculum's lock departs from build-base's sets: datom-codec 0.32.2 at 4dff16b against the set's 0.33.1, protos 0.32.2 against 0.33.0, nexus at ec097e3 is absent, the kameo and tokio family differs, and ethos-zero 16 is an unused dev-dependency. Fixing it means moving Curriculum to the 0.33 codec cohort, which is a separate change.

## Composition comparison

The test built the branch Curriculum through flow c8f526c's own recipe (`--override-input curriculum`), and only `rust_curriculum` was rebuilt. The final binaries are byte-identical to the compared ones. It then ran the release proof's harness, `compose-all.py`, with its queries unchanged, over the three belief branches (`/tmp/f71ae7-compose` on prometheus).

- All 38 permaflows composed, 895 module positions. The order, uniqueness, hashes, versioned paths and placement checks all pass.
- All 38 raw `.datom` replies are byte-identical to `/tmp/e3d6b3-compose-final.abj1PZGa` once the three new source revisions are mapped back to the old pins. Source revisions are the only bytes that differ.
- `results.json` is identical: per-address system and first-prompt hashes and module counts. The Fable and Codex system and first texts are byte-identical.

## Order of the switch

The current Curriculum ignores a file at a source's root, so the three belief branches can reach main first. The new Curriculum refuses any source without `modules.datom`, so it must follow them or go together with them.

## Noticed, not changed

- Flow builds Curriculum from its whole source, Markdown included. A documentation edit therefore rebuilds `rust_curriculum` with a new store path but identical binaries.
- The belief repositories' READMEs still describe file-name layouts.

## Task as63: the 0.33 cohort, then the rebase

- build-base `curriculum-cohort-033` is at `af6ab8a791a8f399b131faf72326b1e4b7d3654a`, on main cd61cac.
  - The version set gains nexus 0.5.0 at ec097e3 (nexus branch entry-point; nexus main c495f2a is older and has no kameo) and the registry crates nexus brings: kameo, futures, tracing, socket2, signal-hook-registry, heck, dyn-clone and downcast-rs.
  - The feature set gains their entries. Crates already in the set get their union widened (tokio rt-multi-thread/net/signal/tracing, mio net, futures-util, errno, memchr, once_cell, slab, syn). I derived this with crate-feature-set over the 14 active Cargo.nix files on base, with and without Curriculum's.
- Curriculum `cohort-033` is at `6485c80becece480e334ef73708eeef61c054253`, on main 4695835.
  - It locks datom-codec 0.33.1 at 09a0526 and protos 0.33.0 at c93b598, with the short revisions Flow locks.
  - The reader budget is built through `ReaderBudget::try_from`. The unused ethos-zero dev-dependency is dropped.
  - Registry crates are locked at the set's versions. mio is a direct dependency to carry the log edge.
  - The flake's base is locked to the build-base branch, and two clippy refusals that main already had are cleared.
  - The lock was updated with a raw toolchain cargo on prometheus, running `cargo update` only. Nothing was compiled.
  - Gate: all five checks are green: curriculum, cargo-nix, crate-versions, crate-features and default (exit 0).
- Curriculum `notion-declarations` is rebased onto `cohort-033` and is at `3e38a65802f2fc89c077d40fd843cdf52338abfc` (force-pushed with lease over 59846c0).
  - New commits: the 0.33 budget in the declarations reader, and the stderr reports recorded as the interim in code and in the commit message.
  - Gate: all five checks are green (exit 0).
- Composition on the rebased branch: all 38 permaflows and 895 positions pass. The test used datom binaries built from the branch's own flake on prometheus, and only the Curriculum crate was compiled.
  - Every system and first-prompt hash and every module count is identical (`results.json`), and the Fable and Codex texts are byte-identical.
  - The raw replies differ in escaping only. Codec 0.33 reads guillemet strings by balance, so a balanced » is no longer written with a backslash.
  - With each side read by its own codec, all 8283 decoded fields of all 38 replies are identical once the three revisions are mapped back.
  - Run directory: `/tmp/f71ae7-compose-033` on prometheus. The harness reader there was made to read guillemets by balance.

### Follow-ons when build-base's branch reaches main

- herdr-nexus will have to carry tokio's net, signal and tracing features in its manifest, lock and Cargo.nix, because the widened tokio union attaches libc, mio, socket2, signal-hook-registry, tracing and windows-sys to every build that uses tokio. crate-feature-set lists this edge; I did not change herdr-nexus. Repositories with no Cargo.nix (energy, book and the contract repositories built some other way) were not covered by the derivation.
- When Flow pins this Curriculum, it must regenerate `nix/curriculum/Cargo.nix` from the new lock.
