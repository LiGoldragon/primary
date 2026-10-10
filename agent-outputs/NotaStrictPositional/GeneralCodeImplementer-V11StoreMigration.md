# Spirit v10→v11 Store Migration for the Fixed signal-spirit Contract

## Task and scope

Build and TEST (no deploy, no live-data touch) the storage migration that lets
the deployed `spirit` daemon adopt the fixed `signal-spirit` strict-positional
domain contract. Prep-and-test only: everything must build and be green; no live
migration run, no daemon deploy.

Repo: `/git/github.com/LiGoldragon/spirit`
VCS: jj (git-backed). Base: `criome-authorization-push` @ `202a6e24` (the
deployed baseline, which pins the OLD signal-spirit `5d0905a7`).
Feature bookmark: `spirit-strict-positional-v11`.

## The contract change (confirmed against source)

Old signal-spirit `5d0905a7` vs fixed main `151d49c8`
(`src/schema/domain.rs`), the only structural changes:

- `Technology::Hardware(Option<HardwareLeaf>)` → `Hardware(HardwareLeaf)`.
- `Software::X(Option<XLeaf>)` → `Software::X(XLeaf)` for all 11 non-Theory
  variants (`Theory` stays payload-less).
- Each of the 12 value-leaf enums gains a leading `All` member, shifting every
  existing leaf discriminant by +1 (e.g. `DataLeaf::Persistence` old-disc 0 →
  new-disc 1, with `All` = 0).

Both axes change the archived rkyv layout of a persisted `Domain`. `spirit`
persists `Entry → Domains → Domain` via rkyv at store version 10
(`src/store/mod.rs`). Live v10 bytes would be silently misread under the new
contract (the checked-in `family_identity::RECORDS_FAMILY` hash is a literal that
does not encode the Domain-leaf layout, so the sema-engine hash guard does not
fire on the change; the SchemaVersion guard is the real gate).

## Changed files

### `Cargo.lock` / `flake.lock`
- Bumped `signal-spirit` pin `5d0905a7` → `151d49c8` (scoped `cargo update -p
  signal-spirit`), which also advanced the strict-positional-fixed schema stack
  it pulls: `schema-next` `9af2c546`, `schema-rust-next` `6218fb64`,
  `triad-runtime` `3d320746`, `version-projection` `666c468e`.
- Updated the matching flake inputs (`signal-spirit-source`, `schema-source`,
  `schema-rust-source`, `triad-runtime-source`, `version-projection-source`) so
  the vendored Nix build matches `Cargo.lock` exactly. `151d49c8` is on
  `origin/main`, so both cargo and the flake resolve it portably.
- Lock reconciliation (required for a green `nix flake check`): the flake builds
  every crate from vendored flake inputs with `cargo … --locked`, so each
  vendored crate's `flake.lock` rev must equal its `Cargo.lock` rev. The
  baseline `202a6e24` already carried a pre-existing Cargo.lock↔flake.lock drift
  on `sema-engine` (flake `0.6.2`/`73eea24b` vs lock `0.6.3`/`98ba507b`) and
  `signal-harness` (flake `0.1.0`/`0d06d4ae` vs lock `0.2.0`/`0727beb7`). Aligned
  the flake inputs to the Cargo.lock revs (`nix flake lock --override-input
  sema-engine-source …#98ba507b` and `signal-harness-source …#0727beb7`) — the
  repo's established direction (commit `9e413ba` "align vendored flake sources to
  Cargo.lock"). Verified 0 mismatches across all 10 potentially-skewed vendored
  crates. `Cargo.lock` sema-engine/signal-harness are left at the baseline
  main-HEAD revs (the code already compiles against them; `cargo test` green).
- `meta-signal-spirit` stays at `98704a35` and compiles cleanly against the new
  `signal-spirit` (verified in the check build).

### `src/store/mod.rs`
- `SPIRIT_SCHEMA_VERSION` `SchemaVersion::new(10)` → `new(11)`, with a comment
  explaining the strict-positional adoption and the two layout axes. This is the
  version guard that routes a live v10 store into migration instead of letting
  `Store::open` (v11) misread it.

### `src/production_migration.rs`
- Added `mod store_version_ten`: a frozen snapshot reproducing the EXACT v10
  persisted layout — `StoredRecord`/`Entry`/`Domains`/`Domain`/`Technology`/
  `Software` and all 12 leaf enums with `Option<Leaf>` payloads and leaf enums
  WITHOUT the `All` member (original discriminant order). Personal-life domains
  (Health…Information) reference the current, unchanged enums directly (their
  layout did not change); only the Technology subtree is frozen. `into_current`
  methods fold frozen → current: `Software::X(Some(leaf))` → `X(leaf)` remapped
  by name across the +1 shift; `Software::X(None)` → `X(<Leaf>::All)`;
  `Technology::Hardware(None)` → `Hardware(HardwareLeaf::All)`.
- The five v10 readers (`SpiritStoreV10CurrentLiveDatabase`,
  `SpiritStoreV10LegacyFamilyCurrentLiveDatabase`,
  `SpiritStoreV10Layout3LiveDatabase`, and the two v10 archive readers) now read
  `store_version_ten::StoredRecord` instead of the live `StoredRecord`, and the
  v10 folders/archive-sibling path convert via `into_current`
  (`SpiritPreviousRecord::from_version_ten`). Referents are unchanged and stay
  the live `StoredReferent`.
- Updated the v9→current fold helpers (`store_version_nine`) and the v7 NOTA
  renderers to target the new required-payload contract: `Some(leaf)`→`leaf`,
  `None`→`<Leaf>::All`, bare `(Software Programming)` → `(Software (Programming
  All))`, and the non-Networking v7 hardware variants coarsen to `(Hardware
  All)` (they had no leaf and previously produced unparseable text).
- Added golden test `migrates_version_ten_strict_positional_technology_domains`:
  seeds a v10 store with REAL frozen-layout Technology domains — an absent
  `Data`/`Hardware` payload plus present leaves at their OLD discriminant
  positions (`Persistence` old-0, `Migration` old-5, `Networking`) — runs the
  migration, and asserts the v11 result: `None → All`, and each present leaf
  survives the +1 discriminant remap BY NAME (`Data(Persistence)` stays
  `Data(Persistence)`, never `Data(All)`).
- Fixed the five existing v10 seed helpers to seed the FROZEN layout (they
  previously wrote live bytes, which after the pin bump are v11-layout and the
  frozen reader correctly rejects them); the "already-current" archive in the
  mixed test stays live to keep exercising the skip-rebuild path.

### `src/engine.rs` (pre-existing doc fix, required for a green gate)
- The `doc` flake check (`cargo doc`, default features, `-D warnings`) failed on a
  PRE-EXISTING broken intra-doc link at `engine.rs:711-712` referencing
  `crate::criome_gate::CriomeGate` / `LocalHeadCapture::spirit_head` — the
  `criome_gate` module is `#[cfg(feature = "mirror-shipper")]`, absent under the
  doc feature set. This reproduces on the untouched baseline source and is NOT
  caused by this lane. Demoted the two intra-doc links to plain code spans so the
  reference resolves under every feature set. (Only `doc`-comment text changed.)

### Test call-site updates for the new contract
- `src/production_migration.rs` in-module test assertions (`Data(None)` →
  `Data(DataLeaf::All)`, `Data(Some(..))`/`Operations(Some(..))` → required).
- `tests/runtime_triad.rs`: 9 `Some(leaf)` → `leaf`, 2 `Data(None)` →
  `Data(DataLeaf::All)`.
- `tests/generated_signal_plane.rs`: 1 `Data(Some(..))` → required.
- `tests/operator_271_closed_claims.rs`: the domain-schema-source witness updated
  to the new strict-positional source text (`(Hardware HardwareLeaf)`, leaf
  enums `[All …]`, `(Equivalence [(Information Database) (Technology Software
  Data All)])`).

## Checks run

- `cargo test --lib --features production-migration production_migration`:
  PASS, 13/13 — including the golden test
  `migrates_version_ten_strict_positional_technology_domains`.
- `cargo test --features production-migration --lib --tests`: PASS (all lib unit
  tests + all runnable integration tests: runtime_triad 46, operator_271 7,
  generated_signal_plane 25, versioned_store, process_boundary, etc.).
- `cargo clippy --features production-migration --all-targets -- -D warnings`:
  clean.
- `cargo fmt --check`: clean (after `cargo fmt`).
- `cargo check --tests` (default features): clean.
- `cargo doc --no-deps` (`RUSTDOCFLAGS=-D warnings`, default features): clean
  after the engine.rs doc-link fix.
- `nix flake check -L`: GREEN — `all checks passed!` (27 checks + 9 packages,
  including `store-migration` which is the only surface that compiles the
  `production-migration` module, plus `fmt`, `clippy`/`clippy-nota-text`/
  `clippy-testing-trace`, `build`/`build-nota-text`, `test`/`test-nota-text`,
  `doc`, and the structural checks).
- Flaky-test note: the FIRST full `nix flake check` reported two reds — `doc`
  (the pre-existing link, since fixed) and `test`'s
  `collect_removal_candidates_archives_and_removes_over_the_meta_socket`. The
  latter is environmental: it spawns a daemon and waits ≤5s for its Unix socket
  to appear in the build sandbox. It PASSES locally in the exact config (`cargo
  test --release --test collect_removal_candidates …`), PASSED on an isolated
  `nix build .#checks…test` re-run, and PASSED in the final full green run — a
  transient sandbox timing flake, not a code regression and not related to the
  domain/migration change (the daemon builds with default features and never
  touches the `production-migration` module).

## What an actual live migration + redeploy would entail (NOT done here)

This lane stops at build+test. To actually migrate live v10 databases and
redeploy the daemon, a human would:

1. Land this branch (currently `spirit-strict-positional-v11`) into the deployed
   spirit line and confirm `nix flake check` green on that line.
2. Stop the deployed `spirit` daemon on the target node (the migration and the
   daemon must not both hold the store).
3. Run `spirit-migrate-store` (the `production-migration` binary /
   `packages.store-migration`) against the live store path. It detects the v10
   store, folds every row through the frozen v10 snapshot into a fresh v11 store
   via the logged import choke points, closes with a typed `Migration` marker,
   and swaps in place with backup-hard-link + single-rename exposure (crash-safe;
   the previous store survives at `<stem>.schema-old-backup-<N>.sema`). The
   default archive sibling is migrated the same way.
4. Deploy the new daemon closure (built from this revision, pinning
   `signal-spirit 151d49c8`) to the node via the standard `meta-lojix` host
   deploy, and verify activation + the spirit systemd unit.
5. Verify post-migration: the daemon opens the store as v11, the migration
   marker records `source_schema_version = 10`, and record/domain queries return
   the expected strict-positional values.

Rollback if needed: stop the daemon and `cp <stem>.schema-old-backup-<N>.sema
<stem>.sema`, then redeploy the previous (v10-pinned) closure.

## Blockers / notes

- No live-data or deploy actions were taken (hard boundary respected).
- The checked-in `family_identity::RECORDS_FAMILY` is intentionally left
  unchanged: the v10 readers use it (and the hard-coded legacy family constants)
  to MATCH real v10 stores on disk; regenerating it would break the migration's
  ability to open deployed v10 stores. The v10→v11 distinction is carried by
  `SPIRIT_SCHEMA_VERSION` (10→11), not the family hash.
