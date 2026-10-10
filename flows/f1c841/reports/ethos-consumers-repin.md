# Ethos-zero 16 consumers repinned

ethos-zero main is c2653dd82adb (16.0.0). This is the commit 3ec648 reported, and it follows 0edfc0c3. These pins were used everywhere:

- ethos-zero c2653dd82adbdb1f1f2f654405c6620e0d06fd58
- protos 15b41da8f257 (0.32.2)
- datom-codec 4dff16b4f741 (0.32.2)

Repositories are listed smallest first. Five repositories landed on main and one proposal branch was pushed. Two are blocked upstream: orchestrate and lojix. Their work is on a side bookmark `ethos16-f1c841`, not on main. Nothing was deployed. No nexus, nix profile or running daemon was touched. signal-flow, meta-signal-flow, flow and message's family were not touched.

Each landed repository has an rkyv round-trip test of a generated value, unless its existing tests already archive one. The test archives with `rkyv::to_bytes` and reads back with `from_bytes`, and the value comes back equal. Cargo runs were bounded: `ulimit -v 16G`, `timeout`, `-j 3`/`-j 6`, and a target directory in the scratchpad. `nix flake check` ran on the remote builder.

Two code changes recur across repositories:

- **`compact` instead of `textualize`.** protos 0.32's `textualize` is the vertical print. Repositories whose CLI or file output was one line now call `Compactable::compact`.
- **`Datomizable` has no `Output`.** datom-codec 0.32.2's `Datomizable` no longer has the `Output` associated type. Code that named it was updated.

## meaning-language: landed e4319d10, green

- **Version:** 0.1.0 → 0.2.0.
- **Pins:**
  - ethos-zero 4bf73cae → c2653dd8, in Cargo build-dependency and the flake input.
  - datom-codec 09e2a9d5 → 4dff16b4.
  - protos 1febca78 → 15b41da8.
- **Shape:** datom-codec stays unconditional with `rkyv`, because `Quale::Decimal` holds a `Decimal`. protos is now optional under `datom = ["dep:protos"]`, since only the Datom test uses it. `datom_roundtrip` has `required-features = ["datom"]`, and the Nix check runs `--features datom`. A new test, `tests/archive_roundtrip.rs`, was added. UPGRADES.md was created.
- **Red witness:** before regenerating, the build.rs freshness assertion failed on the stale committed Rust.
- **Results:**
  - `cargo test`: archive 1 passed.
  - `cargo test --features datom`: archive 1 and datom 3 passed.
  - `nix flake check`: exit 0.
- **One fix outside the repin.** The first flake check was red because `tests/check-glossary-coverage.sh` is committed without the executable bit ("Permission denied"). This was already true on main. The check now runs it through `bash`.
- **Not committed:** nix created a `flake.lock`, and the repository does not commit one. The main checkout under /git also holds someone's uncommitted `flake.lock` and `validation/corrective-cleanup.md`. I left both alone.

## claude-answers: landed 96d20488, green

- **Version:** 0.8.0 → 0.9.0.
- **Pins:**
  - ethos-zero b232d35e → c2653dd8.
  - protos 171b21f6 → 15b41da8.
  - datom-codec 6dccc76b → 4dff16b4.
  - rkyv 0.8 added.
- **Shape:** `datom = []` is a default feature. The CLI, `query.rs` and `error.rs` use datom-codec unconditionally, so `--no-default-features` is unsupported, and UPGRADES says so.
- **Other changes:** `Compactable::compact` keeps the CLI output on one line, and `Datomizable<Output = Datom>` was removed from the tests.
- **Results:**
  - Red: the stale Rust did not meet the `Query: Archive` bound.
  - cargo test, with and without `--features datom`: query 15, regeneration 1, transcript 4.
  - clippy and fmt: clean.
  - `nix flake check`: exit 0.
- **Trailer:** the worker used the session's Co-Authored-By trailer, not "Claude Fable 5.1".

## curriculum-deploy: landed a79cf02d; one Nix check red, already red on main

- **Version:** 0.6.3 → 0.7.0.
- **Pins:**
  - ethos-zero b232d35e → c2653dd8.
  - protos 171b21f6 → 15b41da8.
  - datom-codec 6dccc76b → 4dff16b4, now with `rkyv`.
  - rkyv 0.8 added.
- **Shape:** `datom` is a default feature, because datom-codec's `Error` is used directly. The README pin table and UPGRADES were updated. `src/runtime.rs` follows the loss of `Datomizable::Output`.
- **Results:**
  - Red: E0220 on the stale Rust.
  - `cargo test`: 1 unit and 4 integration tests passed, 3 ignored.
  - `--all-features`: 1 unit and 5 integration tests passed, including the rkyv test.
  - clippy and fmt: clean.
- **Red item:** `nix flake check` fails in `checks.external-data` on `authored_subagent_procedure_is_carried_into_its_claude_role` (`tests/runtime.rs:455`). The pinned Curriculum data (0c1cd541) puts the system prompt before `# Book`. **Already red before this change:** I built the same check on the previous main, fb171e3b, and it failed the same test (6 passed, 1 failed). The fix is to repin the `curriculum` flake input or adjust the test. Nix stopped there, so the other Nix checks were not confirmed; cargo covered them locally.
- No deploy was run.

## signal, proposal branch proposal/5f4fea-word-identifiers: pushed bcd5259a; clippy red, from the branch's own code

- **Where:** `identifiers.ethos` exists only on this proposal branch of the signal repository. The branch was repinned and pushed there. signal main, which the sibling subflow builds on, was not touched. Merging the proposal is not ours.
- **Version:** stays 7.0.0. ethos-zero 16 regenerates `src/generated/signal.rs` byte-identical, and `identifiers.ethos` generates no Rust (`src/identifiers.rs` is hand-written), so no shape changed.
- **Pins:**
  - ethos-zero 4bf73cae → c2653dd8.
  - protos 1febca78 → 15b41da8.
  - datom-codec 09e2a9d5 → 4dff16b4.
  - Only Cargo.toml and Cargo.lock changed.
- **Results:** cargo test passed 52 tests, both with and without `--features datom`.
- **Red items:**
  - `nix flake check --keep-going`: only `clippy`, `clippy-transport` and `clippy-datom` fail, on `clippy::unnecessary_cast` at `src/identifiers.rs:181:30`. That code came in with the proposal's own commit.
  - `ethos/interface.ethos` is refused by ethos-zero 16 as `Structural.ProtosError.{ Extent.{ 18 18 } Multiple }` at 2:1. No build checks it, and nobody found whether 10.0.0 accepted it.
- **Lock:** the worker's push retry ran after it had released its lock (bookmark tracking).

## clavifaber: landed 9d49506f, green

- **Version:** 0.6.0 → 0.7.0.
- **Pins:**
  - ethos-zero 4bf73cae → c2653dd8, in the flake input and flake.lock.
  - protos 1febca78 → 15b41da8, with `rkyv`.
  - datom-codec 09e2a9d5 → 4dff16b4, with `rkyv`.
  - rkyv 0.8 added.
- **Shape:** `default = ["datom"]`, with datom-codec unconditional, since error, request and text name it.
- **Other changes:**
  - `src/text.rs` now uses `compact`, so the CLI replies and `publication.datom` stay one line.
  - `tests/rkyv_archive.rs` is new.
  - UPGRADES.md was created, and the AGENTS.md pin text was updated.
  - The toolchain hash in `flake.nix` was refreshed, because the moving `stable` channel had changed (fixed-output mismatch).
- **Results:**
  - Red: three `request_surface` tests failed on the vertical print before the `compact` fix.
  - cargo test: 29 tests in 8 suites.
  - clippy and fmt: clean.
  - `nix flake check`: "all checks passed!", including the generated-freshness check.

## orchestrate: NOT landed, blocked upstream

- **Version:** 0.36.1 on main. 0.37.0 is in the WIP only.
- **Pins in the WIP:**
  - ethos-zero cf7dd128 → c2653dd8.
  - protos 1febca78 → 15b41da8.
  - datom-codec 09e2a9d5 → 4dff16b4, both with `rkyv`.
- **WIP location:** bookmark `ethos16-f1c841` at ee95b834 on origin, which does not compile. Both clients have `default = ["datom"]`, since `datom_codec::Error` sits in a generated position. Both `client.rs` files were regenerated, and the freshness gate was red, then green.
- **Red item:** `ClientFailure` holds `signal::HandshakeRejection` and `signal::ExchangeFault`. signal 7.0.0 (66e7b153) binds datom-codec 0.31 (09e2a9d5) and protos 0.31 (1febca78) under its `datom` feature. Cargo.lock therefore holds two datom-codecs, and `HandshakeRejection: Composing` and `ExchangeFault: Composing` are unsatisfied for 0.32.2. `orchestrate-meta` fails in the same way: `Potential<Query>::actualize` gives 5 errors. signal-orchestrate and meta-signal-orchestrate are also still on cf7dd128/0.31.
- **To unblock:** repin signal, then signal-orchestrate, then meta-signal-orchestrate to 0.32.2 and ethos-zero 16, then finish orchestrate from the bookmark.
- Nothing was deployed. The live Nexus stays at 0.35.0.

## chroma: landed f52b6080; one Nix check red, already red on main

- **Version:** 0.7.1 → 0.8.0. Main had already moved past the 0.6.0 named in the brief.
- **Pins:**
  - ethos-zero 4bf73cae → c2653dd8, in `Cargo.toml` and `tools/regenerate-ethos`.
  - protos 1febca78 → 15b41da8, with `rkyv`.
  - datom-codec 09e2a9d5 → 4dff16b4, with `rkyv`.
- **Shape:** `datom` is a default feature. The config reader and CLI always textualize, so `--no-default-features` does not compile (E0599, as expected).
- **Tests:** an rkyv test was added to `tests/ethos_contract.rs`.
- **Results:**
  - Red: the freshness test failed on the stale Rust.
  - Green: default features and `--all-features`.
- **Red item:** `nix flake check` fails in `checks.sandbox-terminal`: "ghostty config did not reach background #000000 within the 90s hang backstop". This is Ghostty/D-Bus timing in the builder sandbox. **Already red before this change:** the same check on the previous main, fc3a74ac, fails with the same message. `chroma-test-0.8.0` built green.
- The running chroma daemon was not touched.

## lojix: NOT landed, blocked upstream

- **Version:** 8.1.0 on main, not bumped.
- **Pins in the WIP:**
  - ethos-zero 4bf73cae → c2653dd8.
  - datom-codec 09e2a9d5 → 4dff16b4.
  - protos 1febca78 → 15b41da8.
  - These are set in the root, clients/ordinary, clients/meta and tools.
- **WIP location:** bookmark `ethos16-f1c841` at 716a81cb on origin.
- **Red item:** `ingress.ethos` itself holds only strings and integers. The block is in `lojix-client` and `meta-lojix-client`: `signal_lojix::Query: datom_codec::Composing` is not satisfied (E0599 on `actualize`). The foreign crates whose `datom` feature lojix enables still bind datom-codec 09e2a9d5 through ethos-zero 4bf73cae:
  - signal-lojix 6.0.0 (cd164896)
  - meta-signal-lojix 7.0.0 (c0f883c5)
  - horizon-lib 0.13.0 (a3ddaf86)

  Cargo.lock holds codecs 0.31.0 and 0.32.2.
- **Not done:** no tests, Nix check, flake or UPGRADES work, and nothing deployed.

## The upstream pattern, for the main flow

A consumer whose generated or hand-written code datomizes a type from another contract crate cannot move to datom-codec 0.32.2 until that crate does. The derive bounds name the trait of one codec version, and the foreign type implements the other.

The sibling subflow repins signal-flow, flow and the message family "to signal 7, protos and datom-codec 0.32.2". signal 7.0.0 main still binds datom-codec 0.31 under `datom`, so they will meet the same mismatch wherever signal types sit in a datomized position.

Repinning signal main is the first step for orchestrate and lojix, and it is a shared decision. I left it to the main flow.

## vision-ethos conflicts seen (noted, not redesigned)

- **meaning-language `meaning.ethos`:**
  - Long one-line enums (`Padartha`, `GunaKind`, `Dravya`) are not vertical.
  - The variant repeats its type, as in `Karman.Karman` and `Samanya.Samanya`.
  - Single-use types are declared apart rather than inline: `LinUse`, `GunaKind`, `StemFormation`.
  - Several `X.ContentLink` aliases only name positions.
- **claude-answers:**
  - `Answer.{ String String String }` is positional.
  - One-line layout.
- **curriculum-deploy:**
  - One-line `Roles.{ … }`.
  - Positional `Configuration.{ String String }`.
  - Single-variant wrappers (`RolesDocument`, `GeneratedRoleOutputDocument`).
- **signal `identifiers.ethos`:** 3, 6 and 12 bare `Integer` positions, so it is repetitive and unnamed.
- **clavifaber:**
  - Very long one-line `PublicKeyPublicationWriting`.
  - Single-use variant payload types declared apart (`CertificateAuthorityIssuance.CertificateAuthorityIssuance`).
  - Positional `{ String String String }`.
- **orchestrate:**
  - The two `client.ethos` files are identical, which is repetition across crates.
  - `Unreachable.Unreachable` repeats a single-use struct that belongs inline.
  - `SocketPath` and `TransportError` are used once.
- **chroma:**
  - One-line `Request`, `Reply` and `ThemePalette`.
  - `ThemePalette` has 16 bare `String`s.
  - Single-use aliases (`RequestSetTheme`, `ReplyTheme`, `ReplyError`).
- **lojix `ingress.ethos`:**
  - `ConfigurationWriteRequest` repeats `WriterPath`/`WriterMode` many times, and `WriterTestDefaults` repeats `WriterCluster`.
  - Many `Name.String` aliases.
  - Flat, non-vertical file.

## Sources

- ethos-zero c2653dd82adb UPGRADES.md (16.0.0); /home/li/primary/flows/3ec648/reports/ethos-zero-15-roots.md.
- Worker reports of this subflow's nested workers (claude-answers, curriculum-deploy, clavifaber, orchestrate, chroma, lojix, signal proposal), each in its worktree `~/wt/github.com/LiGoldragon/<repo>/ethos16-f1c841`.
- Prior-main Nix witnesses, run by me, logs in the scratchpad:
  - `nix build github:LiGoldragon/curriculum-deploy/fb171e3b4c#checks.x86_64-linux.external-data`, which failed on the same test (`cd-prior.log`).
  - `nix build github:LiGoldragon/chroma/fc3a74ac5a#checks.x86_64-linux.sandbox-terminal`, which failed with the same message (`chroma-prior.log`).
- meaning-language Nix logs: `ml-check.log` (glossary script red) and `ml-check2.log` (exit 0).
- origin heads checked after landing: meaning-language e4319d1056, claude-answers 96d204886f, curriculum-deploy a79cf02d3c, clavifaber 9d49506fba, chroma f52b608049, and signal proposal/5f4fea-word-identifiers bcd5259a77.
