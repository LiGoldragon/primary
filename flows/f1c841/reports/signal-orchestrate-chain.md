# signal and the orchestrate chain on ethos-zero 16

All four steps landed on main, in order, each green before the next began. Nothing was deployed: the running orchestrate-nexus stays 0.35.0, and no nix profile, socket or store was touched. One Lock covered the five worktrees, `SignalOrchestrateChain` 11673, and it was Released. The worktrees are `~/wt/github.com/LiGoldragon/<repo>/chain-f1c841`.

Pins used everywhere:

- ethos-zero 16.0.0 `c2653dd82adb`
- protos 0.32.2 `15b41da8f257`
- datom-codec 0.32.2 `4dff16b4f741`

Cargo ran bounded: `ulimit -v 16000000`, `timeout`, `-j 6`, and a target directory in the scratchpad. `nix flake check --keep-going -L path:.` ran on the remote builder (`max-jobs = 0`, builders from `/etc/nix/machines`) for x86_64-linux.

## signal: 7.0.0 → 8.0.0, main f35460de

- **Pins:** datom-codec `09e2a9d5` → `4dff16b4`, protos `1febca78` → `15b41da8`, ethos-zero `4bf73cae` (10.0.0) → `c2653dd8`. Only Cargo.toml, Cargo.lock and UPGRADES.md changed.
- **Generated Rust:** `src/generated/signal.rs` is byte-identical under ethos-zero 16. `build.rs` regenerates it and asserts equality on every build, and that assertion passed.
- **Why a major bump:** under `datom`, every type now implements datom-codec 0.32.2's `Datomizable` and `Composing` in place of 0.31's. A consumer on the other codec no longer compiles against it. The archived layout is unchanged.
- **Results:**
  - `cargo test`: 40 passed.
  - `cargo test --features datom --all-targets`: 41 passed.
  - `cargo test --features transport --all-targets`: 42 passed.
  - `cargo test --doc`: ok.
  - `nix flake check`: "all checks passed!" (build, test, test-datom, test-datom-round-trip, test-transport, test-doc, doc, fmt, the three clippy checks, and the grep checks).
- **UPGRADES 8.0.0:** gives the one-step deploy and names the consumers by the signal pin their /git checkouts held:
  - **on 7.0.0:** signal-orchestrate, meta-signal-orchestrate, signal-ethos-zero, meta-signal-ethos-zero, signal-system, meta-signal-system, signal-persona, signal-mirror, and orchestrate.
  - **on 5.0.0 `7bcb0949`:** signal-flow, meta-signal-flow, signal-message, meta-signal-message, signal-router, meta-signal-router, signal-mind, signal-criome, meta-signal-criome, signal-harness, signal-introspect, signal-mentci, meta-signal-mentci, meta-signal-mirror, meta-signal-persona, signal-repository-ledger, meta-signal-repository-ledger, and flow and message.
  - **on `8f9a0deb`:** signal-lojix, meta-signal-lojix, lojix, and horizon-lib through lojix's lock.
  - **on `48ae17b4`:** signal-spirit, meta-signal-spirit, signal-aggregator, meta-signal-aggregator, aggregator.

  The list comes from /git checkouts, which may lag their remotes.

## signal-orchestrate: 4.0.0 → 5.0.0, main 7cc50259

- **Pins:** signal `66e7b153` → `f35460de`, protos/datom-codec 0.31 → 0.32.2, ethos-zero `cf7dd128` (13.0.0) → `c2653dd8`.
- **Generated Rust:** byte-identical, asserted by `build.rs`.
- **Lock:** holds one signal (8.0.0), one datom-codec, one protos and one ethos-zero.
- **Results:**
  - `cargo test`: 10 passed.
  - `cargo test --features datom --all-targets`: 12 passed.
  - `nix flake check`: "all checks passed!".
- **UPGRADES 5.0.0:** written.

## meta-signal-orchestrate: 4.0.0 → 5.0.0, main 77afda05

- **Pins:** signal-orchestrate `4e683453` → `7cc50259`, signal → `f35460de`, protos/datom-codec → 0.32.2, ethos-zero → `c2653dd8`.
- **Generated Rust:** byte-identical.
- **Results:**
  - `cargo test`: 5 passed.
  - `cargo test --features datom --all-targets`: 6 passed.
  - `nix flake check`: "all checks passed!".
- **UPGRADES 5.0.0:** written.

## orchestrate: 0.36.1 → 0.37.0, main c7c44cb3

- **Source:** built from bookmark `ethos16-f1c841` (ee95b834). The fix was squashed into that commit with a real description, landed as main, and the side bookmark was deleted on origin. The old workspace `~/wt/.../orchestrate/ethos16-f1c841` still exists, now without its bookmark.
- **Pins:** signal → `f35460de`, signal-orchestrate → `7cc50259`, meta-signal-orchestrate → `77afda05`, on top of the bookmark's ethos-zero/protos/datom-codec pins (both with `rkyv`). Cargo.lock now holds one signal, one datom-codec 0.32.2, one protos 0.32.2 and one ethos-zero 16.0.0. The two-codec collision is gone.
- **Red 1: the dev-dependency on the previous release is gone.** The first resolution failed:

  ```
  package `signal` links to the native library `signal`, but it conflicts with a previous package which links to `signal` as well
  ```

  The dev-dependency `orchestrate-nexus-0-36-0` (rev b56f2644, used by `tests/store_generations.rs`) pulls signal 7.0.0, and signal's `links = "signal"` admits one signal per Cargo graph. Every earlier release is on signal 7, so no previous release can be a dev-dependency while orchestrate is on signal 8.

  **What I did:**
  - Removed the dev-dependency.
  - `store_generations.rs` keeps `an_open_refused_on_a_family_writes_nothing`.
  - The two cross-generation tests (resume with Locks and configuration; a copied store refused until declared) were removed from the crate.
  - The resume moved to process level in orchestrate-test (below).
  - **Not carried over:** the copied-store refusal of a store written by the *previous* release. `carried_store.rs` still covers a copied store written by this generation.
- **Red 2: clients print on one line again.** `orchestrate-meta`'s `client_actualizes_datoms_and_textualizes_typed_responses` failed on the vertical print:

  ```
  "Configured.{ { /tmp/ordinary.sock /tmp/meta.sock }\n             True }\n"
  ```

  Both clients now call `Compactable::compact`, and the test is green.
- **Results:**
  - `cargo test --workspace --all-targets`: 65 passed, 1 ignored, 0 failed. This includes `live_nexus` with 16 passed.
  - `nix flake check`: "all checks passed!" over the 18 checks the flake defines: build, carried-store, clippy, configuration-authority, datom-free-nexus, doc, fmt, live-nexus, meta-client, ordinary-client, ordinary-lock-contract, peer-authority, relocation, socket-claim, stopping, store-generations, test, test-doc.
  - The brief said 19. The flake has 18, so the missing one is not one I dropped.
- **UPGRADES 0.37.0:** says there is no wire or store change. The ethos and generated Rust are byte-identical, so the contract digests are unchanged. The orchestrate-test scenario confirms that a 0.37.0 client greets a 0.36.1 Nexus. Deploy is by the user-environment repin. Not deployed.

## orchestrate-test: main 4aeec4c5

- **Input:** `orchestrate` `bc5cd36e` → `c7c44cb3` (0.37.0), with flake.lock updated through `nix flake update orchestrate`.
- **New input `orchestrate-previous`:** 0.36.1 `bc5cd36e`. `lib/components/orchestrate.nix` now takes `{ name, input }`, and `lib/default.nix` builds both components from it.
- **New pure scenario `orchestrate-previous-orchestrate`:**
  1. 0.36.1 starts on a fresh root and takes a meta Configure and Lock 1 from its own clients.
  2. The 0.37.0 client observes that Lock on the 0.36.1 Nexus.
  3. 0.36.1 is stopped with TERM, and 0.37.0 starts on the same directories.
  4. 0.37.0 holds Lock 1, answers `LockRejected.PathOverlap.{ … }` for its path, numbers the next Lock 2, and answers `ConfigurationRefused.{ MetaConfigureOccurred }` to an ordinary Configure.
- **Seen red once:** I changed the expected id to 3, and the scenario failed on `resumed-allocator`. Restored.
- **Results:**
  - `nix flake check path:.`: all passed, covering lint, orchestrate, orchestrate-populated-store, orchestrate-old-meta-name (the live meta-orchestrate.sock situation: legacy reached, default unreached, back again) and orchestrate-previous-orchestrate.
  - `nix flake check --refresh github:LiGoldragon/orchestrate-test/4aeec4c5…`: "all checks passed!".
- **README:** names the second input and the scenario.

## Not settled here, for the main flow

- **signal's `links = "signal"`.** Its reason is written nowhere I found: UPGRADES 2.0.0 only names it. It forbids any cross-generation test that links two releases in one graph. I moved the test rather than change signal.
- **Consumers repinning to protos/datom-codec 0.32.2 must take signal 8.0.0 in the same step.** On signal 7 they meet the same two-codec mismatch. The message subflow's Lock 11667 reason reads "signal 7". The flow log says signal-ethos-zero already moved to 8.0.0.

## vision-ethos conflicts seen (noted, not redesigned)

Reshaping any of these changes the ethos text, so it changes the contract digest and the wire identity.

- **signal `ethos/signal.ethos`:**
  - Multi-element enums sit on one line: `ComponentKind` with 14 variants, `ExchangeFault`, `AuthorizedObjectInterest`, `HandshakeReceipt`.
  - Single-use types are declared apart: `HostName`, `NetworkPort`, `NetworkEndpoint`, `Differentiator`, `ComponentObjectInterest`.
  - The payload `NetworkSocket.NetworkEndpoint` is a second type invented for a variant.
- **signal-orchestrate:**
  - Flat, non-vertical lines.
  - Single-use holders `ConfigurationRejection.{ ConfigurationRejectionReason }`, `LockRejection`, `ReleaseRejection` and `LockOverlap` are declared apart from their variants.
  - Aliases of aliases: `OrdinarySocketPath.ConfigurationPath`.
  - Single-variant enums: `ObserveSelection.[ Locks ]`, `Observation.[ Locks.Vector<Lock> ]`.
- **meta-signal-orchestrate:**
  - Single-use holders: `PeerRejection.{ PeerUserId }`, `ConfigurationRejection.{ ConfigurationRejectionReason }`.
  - Single-variant `ConfigurationRejectionReason.[ InvalidConfiguration ]`.
  - Not vertical.
- **orchestrate `client.ethos` (both, identical):** as in ethos-consumers-repin.md. The two files repeat each other, and `Unreachable.Unreachable` is a single-use type.

## Sources

- Commands and logs in the session scratchpad: `signal-check.log`, `so-check.log`, `mso-check.log`, `orch-build.log`, `orch-test.log`, `orch-check.log`, `ot-check.log`, `ot-remote.log`.
- Origin heads after landing: signal f35460de9309, signal-orchestrate 7cc50259f5eb, meta-signal-orchestrate 77afda05c488, orchestrate c7c44cb39934, orchestrate-test 4aeec4c5f3c4. The `ethos16-f1c841` bookmark was deleted from orchestrate's origin.
- /home/li/primary/flows/f1c841/reports/ethos-consumers-repin.md, for the starting state and the bookmark.
- Signal consumer pins: a grep of `LiGoldragon/signal"` in Cargo.toml under /git/github.com/LiGoldragon.
