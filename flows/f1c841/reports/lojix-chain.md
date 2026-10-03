# Lojix chain on ethos-zero 16

All four repositories landed on main, in order, and all are green. Nothing was deployed. The running lojix-nexus 8.1.0 under /run/lojix/ was not touched. No signal, orchestrate or flow repository was touched.

These pins were used everywhere:

- ethos-zero c2653dd82adbdb1f1f2f654405c6620e0d06fd58 (16.0.0)
- protos 15b41da8f2579e73ead59bc0c2b97529b8ac32d3 (0.32.2)
- datom-codec 4dff16b4f7412febc3b71aac8b49680cd20988cb (0.32.2)
- signal f35460de930943ea1a8a972453ccf3a092a655b5 (8.0.0), up from 3.0.2 (8f9a0deb) in every repository of this chain

How the work was run:

- **Cargo:** each run was bounded with `ulimit -v 16000000`, `timeout` and `-j 6`, with its target directory in the scratchpad.
- **Generation:** generated Rust came from the ethos-zero 16.0.0 binary (`nix build github:LiGoldragon/ethos-zero/c2653dd8`), using `Check.` and then `Generate.`.
- **Freshness gates:** each gate was first seen red on the stale committed Rust, then green.
- **Nix:** `nix flake check -L --keep-going path:<worktree>` was run with the configured builders.
- **Worktrees:** `~/wt/github.com/LiGoldragon/<repo>/lojix-chain-f1c841`, plus the existing `lojix/ethos16-f1c841`.
- **Lock:** 11687, on the four worktree paths only. It is released.

## horizon-lib (horizon-rs): landed 2e09ebbdc725, green

- **Version:** 0.13.0 → 0.14.0 (horizon-lib, horizon-cli, flake `version`).
- **Pins:**
  - ethos-zero 4bf73cae → c2653dd8.
  - protos 1febca78 → 15b41da8.
  - datom-codec 09e2a9d5 → 4dff16b4, still with `rkyv`.
  - All three are workspace dependencies.
- **Generated:** `lib/src/generated/horizon.rs` was regenerated. Options are now `std::option::Option`, with `#[rustfmt::skip]` on every item. No field or variant changed.
- **Red witness:** the build.rs freshness assertion failed on the stale file (`lib/build.rs:13`, `assertion left == right failed`).
- **Code:**
  - `horizon-compose` prints through `Compactable::compact`, so `horizon-definition.datom` stays one line.
  - `lib/tests/contract.rs` and `cli/tests/compose.rs` use `compact`. Two contract tests had failed on the vertical print: `encoded.contains("{ backup-wifi } } MX }")` and the tailnet assertion.
  - The `contract` test now has `required-features = ["datom"]`. Without it the test did not compile under `--no-default-features`, since it uses protos and `decode`.
  - New test `lib/tests/archive_roundtrip.rs` (rkyv round trip of `Hardware`). It was seen failing once with a wrong expected value, then green.
  - UPGRADES 0.13.0 → 0.14.0 was written.
- **Results:**
  - `cargo test --workspace`: compose 1, lib 1, archive 1, contract 10, all passed.
  - `cargo test -p horizon-lib --no-default-features`: lib 1 and archive 1 passed.
  - `cargo clippy --workspace --all-targets`: clean.
  - `nix flake check`: exit 0.
- **Red item, already there before this change, not touched:** `cargo fmt --check` reports diffs in `lib/src/model.rs` and `lib/tests/contract.rs` at lines 469, 484 and 515. Those are untouched code, and the flake has no fmt check. My new file is formatted.

## signal-lojix: landed 0a83f2d6d89b, green

- **Version:** 6.0.0 → 7.0.0.
- **Pins:**
  - signal 8f9a0deb (3.0.2) → f35460de (8.0.0).
  - horizon-lib a3ddaf86 → 2e09ebbd (0.14.0).
  - datom-codec → 4dff16b4.
  - protos → 15b41da8.
  - ethos-zero → c2653dd8.
- **Generated:** `src/generated/signal.rs` was regenerated. The freshness gate was red at `build.rs:14`, then green. No layout changed. UPGRADES 6.0.0 → 7.0.0 was written.
- **Signal API:** the tests use `signal::{ByteViewable, Restorable, Signal, Signalizable}`, and all four still exist in 8.0.0. No code change was needed.
- **Results:**
  - `cargo test`: generated_contract 3 passed.
  - `cargo test --features datom`: 7 passed.
  - `cargo clippy --all-targets -D warnings`, with and without `datom`: clean.
  - `cargo fmt --check`: clean.
  - `cargo tree -d --features datom`: one datom-codec. The only duplicate is syn.
  - `nix flake check`: exit 0. Its checks include `test-datom-contract`.

## meta-signal-lojix: landed 25f7f220e47f, green

- **Version:** 7.0.0 → 8.0.0.
- **Pins:** the same as signal-lojix, plus signal-lojix cd164896 → 0a83f2d6 (7.0.0).
- **Generated:** regenerated. The freshness gate was red at `build.rs:14`, then green. No layout changed. UPGRADES 7.0.0 → 8.0.0 was written.
- **Results:**
  - `cargo test`: 4 passed.
  - `cargo test --features datom`: 8 passed.
  - Clippy `-D warnings` with and without `datom`: clean.
  - fmt: clean.
  - `cargo tree -d`: one datom-codec.
  - `nix flake check`: exit 0.

## lojix: landed 0eed57fe5126 on main, green

- **Version:** 8.1.0 → 9.0.0 (root, nexus, both clients, tools).
- **History:** main fast-forwards over the earlier WIP commit 716a81cb. Bookmark `ethos16-f1c841` was moved to the same head.
- **Pins, in the root and in every member:**
  - signal → f35460de.
  - signal-lojix → 0a83f2d6.
  - meta-signal-lojix → 25f7f220.
  - horizon-lib → 2e09ebbd, also as the `horizon` flake input. `flake.lock` was updated for that input only.
  - datom-codec, protos and ethos-zero (dev-dependency) were already set by the WIP.
  - sema-engine 27e814a7, triad-runtime 02cdd49d and nexus a84bfa96 are unchanged. They bind signal-frame, not signal or datom-codec.
- **Generated:** `src/ingress.rs` was regenerated from `ethos/ingress.ethos`. The `ingress_freshness` test was red on the stale file, then green. ethos-zero 16 now puts the ingress datom derives behind `cfg_attr(feature = "datom")`. That broke `actualize` in bootstrap, inspection and reconstruction (E0599), because lojix's feature was named `tools`.
- **Code:**
  - The root `Cargo.toml` gains `datom = ["dep:datom-codec", "dep:protos"]`, and `tools` (the default) now enables `datom`. The Nexus still builds with neither.
  - The `lojix` and `lojix-meta` mains print replies through `Compactable::compact`, which keeps the one-line replies the lojix skill quotes.
  - UPGRADES 8.1.0 → 9.0.0 was written. It records no store change (schema v5, no migration), no change to either contract's archived layout, signal 8's depth-64 validation ceiling, and that the Nexus and both clients deploy together.
- **Results:**
  - `cargo test --workspace`: 190 passed, 0 failed, 1 ignored. The ignored test is in build_smoke, as on main.
  - `cargo clippy --workspace --all-targets -- -D warnings`: clean.
  - `cargo fmt --all --check`: clean.
  - `cargo build -p lojix-nexus`: clean.
  - `nix flake check`: exit 0, "all checks passed!". This includes the two NixOS VM tests that run the Nexus on its own temporary sockets, `lojix-same-host-test-activation` and `lojix-target-store-realization` (each "All checks passed!"), plus lojix-test, lojix-clippy and lojix-fmt. The "is not valid" line in the log is an expected `must fail` step.
- **Red item, not fixed:** `cargo test -p lojix --no-default-features` does not compile. Integration tests such as `ingress_freshness`, `store_inspection`, `store_startup_gate` and `deploy_transport_integration` import modules gated by `tools` (`lojix::ingress`, `lojix::inspection`, `Budgeted`) and `HorizonDefinition::decode` / `datomize`, and they carry no `required-features`. I did not run this on the prior main, but this change did not touch the gating, so it is very likely already there. The brief asks lojix only for cargo test and the flake check, and both are green.
- **Not done:** no deploy. Moving the live lojix-nexus 8.1.0 to 9.0.0 is the next step, per UPGRADES.

## vision-ethos conflicts seen (noted, not redesigned)

- **horizon-rs `lib/ethos/horizon.ethos`:**
  - A library of types is headed `Signal`, with empty import, query and response sections. Under 16.0.0 it belongs in a `Library` root.
  - `NodeCapability` is a very long one-line enum, and many variants repeat `.NoSettings` payloads.
  - `NodeDefinition` has bare repeated positions (`Magnitude Magnitude`, `Option<Boolean>`).
  - About 25 `Name.String` aliases.
- **signal-lojix `ethos/signal.ethos`:**
  - The ordinary contract carries `Configure.LojixNexusConfiguration`, plus the configuration types and `OrdinaryConfigureClosed`. The vision says policy changes only over the meta socket.
  - `DaemonHost` and `DeploymentFailureStage.Daemon` say daemon where the vision says Nexus.
  - About 20 `Name.String` aliases.
  - Long one-line structs (`LojixNexusConfiguration`, `TestDefaults`, `DeploymentPhaseEvent`).
- **meta-signal-lojix `ethos/signal.ethos`:**
  - The import line is one very long line.
  - `ExtraSubstituter.{ String String }` is positional and unnamed.
  - It repeats `Configure` and the configuration receipt beside the ordinary contract.
- **lojix `ethos/ingress.ethos`:** as reported in ethos-consumers-repin.md: repeated `WriterPath` and `WriterMode`, many `Name.String` aliases, and a flat, non-vertical layout.

## Sources

- Context: /home/li/primary/flows/f1c841/reports/ethos-consumers-repin.md; signal main f35460de UPGRADES.md (8.0.0 section).
- Worktrees: /home/li/wt/github.com/LiGoldragon/{horizon-rs,signal-lojix,meta-signal-lojix}/lojix-chain-f1c841 and /home/li/wt/github.com/LiGoldragon/lojix/ethos16-f1c841.
- Origin heads confirmed with `git ls-remote` after pushing:
  - horizon-rs 2e09ebbdc725f64fd9ee102b5758bab85be217e1
  - signal-lojix 0a83f2d6d89b473ce63ff10bf05982df314894ad
  - meta-signal-lojix 25f7f220e47f703f4c262b1df84d06ad2bd61197
  - lojix 0eed57fe51264b2597edc8099227c87366d2aa17
- Logs in the session scratchpad (/tmp/claude-1001/-home-li-primary/f1c84105-972f-4ef6-a158-c66638429e7b/scratchpad): hz-check.log, sl-check.log, msl-check.log, lojix-build.log, lojix-test.log, lojix-clippy.log, lojix-check.log.
