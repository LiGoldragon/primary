# Schema Design Component Port Ledger

Operator ledger for the mainline component-by-component port to the latest
schema / schema-rust / NOTA design.

## Method

For each repo, I used the repo's `main` checkout, refreshed git dependencies,
regenerated checked-in schema artifacts through the repo build driver when it
had one, pinned unrelated crates.io churn back out of the lockfile, then ran the
repo's cargo and Nix gates where present.

The formal `tools/orchestrate claim` helper is currently blocked: it tries to
build `orchestrate-cli`, whose dependency graph fetches a `nota-codec` revision
that is unavailable/auth-blocked. I continued with one repo at a time and clean
working copies.

## Already Landed Before This Ledger

These repos had already been refreshed and pushed in the current operator pass:

| Repo | Commit | Result |
|---|---:|---|
| `schema-rust-next` | `cad9ec27` | schema Rust emitter refreshed. |
| `signal-spirit` | `876c2721` | Spirit working contract regenerated/tested. |
| `meta-signal-spirit` | `3283925f` | Spirit meta contract regenerated/tested. |
| `signal-agent` | `35be3523` | Agent working contract refreshed. |
| `meta-signal-agent` | `4c58b216` | Agent meta contract refreshed. |
| `spirit` | `41f11730` | Spirit daemon stack refreshed/tested. |
| `signal-mirror` | `df2d1ffc` | Mirror working contract refreshed. |
| `meta-signal-mirror` | `dac5f863` | Mirror meta contract refreshed. |
| `mirror` | `b9c171a7` | Mirror daemon refreshed/tested. |
| `agent` | `33a967af` | Agent daemon refreshed/tested. |
| `signal-cloud` | `878f9e79` | Cloud working contract refreshed. |
| `signal-domain-criome` | `b4096539` | Domain-Criome working contract refreshed. |
| `meta-signal-cloud` | `1719bc48` | Cloud meta contract refreshed. |
| `cloud` | `fea3e64b` | Cloud runtime refreshed. |
| `meta-signal-domain-criome` | `365e03f7` | Domain-Criome meta contract refreshed. |
| `domain-criome` | `2c7f5fe2` | Domain-Criome runtime refreshed. |
| `signal-criome` | `8c76ccea` | Criome working contract refreshed. |
| `meta-signal-criome` | `74d19039` | Criome meta contract refreshed. |
| `criome` | `ec7c3e06` | Criome daemon refreshed/tested. |
| `signal-message` | `a55de289` | Message working contract refreshed. |
| `meta-signal-message` | `d6eb647a` | Message meta contract refreshed. |
| `message` | `33ced799` | Message daemon refreshed/tested. |
| `signal-router` | `f81d4646` | Router working contract refreshed. |
| `meta-signal-router` | `9568ab99` | Router meta contract refreshed. |
| `router` | `8e02f781` | Router daemon refreshed/tested. |
| `signal-introspect` | `8538acbe` | Introspect working contract refreshed. |
| `meta-signal-introspect` | none | No tracked changes; cargo green. |
| `introspect` | `fe028946` | Introspect daemon refreshed/tested. |
| `signal-system` | `37e5026b` | System working contract refreshed. |
| `meta-signal-system` | `46bbb079` | System meta contract refreshed. |

## This Segment

| Repo | Commit | Changed | Verification |
|---|---:|---|---|
| `system` | `d0fdfe89` | Lockfile only; no generated schema diff. | `cargo build`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, `nix flake check --builders '' -L`. |
| `signal-harness` | `623baf60` | Lockfile to latest NOTA/schema stack and `signal-persona`; hand-written contract. | Cargo build/test/clippy, Nix flake check; 31 contract witnesses. |
| `meta-signal-harness` | `528aba89` | Removed obsolete `.clone()` calls on now-`Copy` exchange identifiers. | Cargo build/test/clippy; no repo-local `flake.nix`. |
| `signal-terminal` | `e7150dd1` | Regenerated schema artifact; scalar newtypes gained standard impls. | Cargo build/test/clippy, full Nix flake check; 25 contract tests. |
| `harness` | `469ededc` | Lockfile only after regeneration check; consumed refreshed harness and terminal contracts. | Cargo build/test/clippy, full Nix flake check; message-router-harness e2e, Pi RPC, subscription, daemon and smoke tests. |
| `meta-signal-terminal` | `a2f0f9e8` | Lockfile only; consumed refreshed `signal-terminal`. | Cargo build/test/clippy, full Nix flake check; 6 terminal meta round-trip/head tests. |
| `terminal-cell` | `f6d6dd5e` | Lockfile refresh, then Nix package source filtering fixed to retain `schema/` for downstream consumers. | Cargo build/test/clippy, `nix flake check --builders '' -L`, `nix build .#default --builders '' -L --no-link --print-out-paths`. |
| `terminal` | `8e45dfef` | Lockfile, regenerated `SocketPath::new` to accept `impl Into<String>`, fixed one stale Nix test selector. | Cargo build/test/clippy, full Nix flake check, plus targeted fixed selector check. |
| `signal-persona` | `5953c8fc` | Persona working contract refreshed onto the latest schema stack. | Cargo build/test/clippy and Nix gate. |
| `meta-signal-persona` | `a5fa2b0a` | Persona meta contract refreshed onto the latest schema stack. | Cargo build/test/clippy and Nix gate. |
| `meta-signal-upgrade` | `9a9de8a1` | Upgrade meta contract refreshed. | Cargo build/test/clippy and Nix gate. |
| `signal-upgrade` | `9cc8ac14` | Upgrade working contract refreshed. | Cargo build/test/clippy and Nix gate. |
| `upgrade` | `2eda2c4c` | Upgrade runtime refreshed against the current schema and signal stack. | Cargo build/test/clippy and Nix gate. |
| `persona` | `961133dc` | Topology flake moved from retired `persona-*` repos to active component repos, terminal-cell source packaging was fixed for Nix schema inputs, and prototype launchers were adjusted to fixture-backed binary-startup smoke while router/message stay real e2e daemons. | `cargo fmt`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, targeted terminal-cell/prototype/message-router Nix builds, full `nix flake check --builders '' -L`. |
| `signal-mind` | `129fd8ac` | Lockfile refreshed to latest NOTA stack and `signal-persona`; canonical NOTA tests updated for bare atom strings; stale flake selectors fixed. | `cargo fmt -- --check`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`. |
| `meta-signal-mind` | `7cb639f2` | Regenerated with latest schema stack; `PolicyRevision` gained generated scalar newtype impls. | `META_SIGNAL_MIND_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, cargo fmt/test/clippy, full Nix flake check. |
| `signal-orchestrate` | `f223edf2` | Regenerated with latest schema stack; standard newtype impls emitted and schema contract tests updated to the current `Root::as_enum()` API. | `SIGNAL_ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, cargo fmt/test/clippy, full Nix flake check. |
| `meta-signal-orchestrate` | `6ee006ee` | Regenerated with latest schema stack and refreshed `signal-orchestrate`; schema contract tests updated to the current `Root::as_enum()` API. | `META_SIGNAL_ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, cargo fmt/test/clippy, full Nix flake check. |
| `mind` | `ae1e573f` | Lockfile refreshed to the new mind/orchestrate contract stack; regeneration produced no checked-in schema diff; stale Nix guard selector fixed to the live lockfile guard. | `MIND_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, `cargo fmt -- --check`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`, rerun after selector fix. |
| `orchestrate` | `cf1c5255` | Lockfile refreshed to the new orchestrate contract stack; regeneration produced no checked-in schema diff; schema contract tests updated to the current `Root::as_enum()` API. | `ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, `cargo fmt -- --check`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`. |
| `signal-repository-ledger` | `7254e4ae` | Hand-written ordinary contract lock refreshed to current `nota-next`; no schema artifact yet. Pushed to GitHub after discovering local `origin` was Gitolite while downstream Cargo resolves GitHub. | `cargo fmt -- --check`, `cargo test`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`. |
| `meta-signal-repository-ledger` | `114c0e88` | Hand-written meta contract lock refreshed to current `nota-next` and `signal-repository-ledger` `7254e4ae`. | `cargo fmt -- --check`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`. |
| `repository-ledger` | `04c07eb2` | Runtime lock refreshed to the new ordinary/meta repository-ledger contracts and current schema-rust stack; regeneration produced no checked-in daemon schema diff. | `REPOSITORY_LEDGER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, `cargo fmt -- --check`, `cargo test`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L`. |
| `signal-version-handover` | `006761df` | Hand-written private handover contract refreshed to current `nota-next` and `signal-frame`; added explicit `nota-text` feature passthrough and Nix checks so the round-trip suite is exercised instead of silently skipped. | `cargo fmt -- --check`, `cargo test`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L` including `test-nota-text` and `clippy-nota-text`. |
| `meta-signal-version-handover` | `e37e1fa8` | Meta handover contract lock refreshed to current `nota-next` / `version-projection`; canonical NOTA examples and tests updated from legacy bracket strings to bare atoms. | `cargo fmt -- --check`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L` with default and `test-round-trip` checks. |
| `version-projection` | `1a1eeab4` | Optional/dev NOTA text dependency refreshed to current `nota-next`; flake gained explicit `nota-text` test and clippy checks so the optional projection witnesses run in Nix. | `cargo fmt -- --check`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L` including `test-nota-text` and `clippy-nota-text`. |
| `signal-frame` | `e2eae5c2` | Shared frame kernel optional/dev NOTA dependency refreshed to current `nota-next`; canonical text witnesses updated to bare atoms; test helper updated for current clippy; flake gained fmt, clippy, `nota-text` test, and `nota-text` clippy checks. | `cargo fmt -- --check`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L` covering default binary tests, `nota-text` tests, both clippy paths, fmt, and the old schema-composer removal guard. |
| `signal-sema` | `bdd7fe36` | Universal Sema vocabulary optional/dev NOTA dependency refreshed to current `nota-next`; pattern witnesses updated to bare-atom canonical strings; flake gained explicit `nota-text` test and clippy checks. | `cargo fmt -- --check`, `cargo test --all-targets --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, full `nix flake check --builders '' -L` covering binary-only and `nota-text` suites. |

## Test Hygiene Found

The port surfaced stale Nix exact selectors that returned success while running
zero tests:

- `harness`: three exact-selector checks still filtered to zero tests during
  the full flake run. Broader harness cargo and Nix suites passed, including the
  real daemon and e2e tests. This remains to fix.
- `terminal-cell`: `control-socket-mode` uses an obsolete exact test name and
  ran zero tests in Nix; local cargo did run
  `control_socket_mode_is_enforced_by_daemon`. This remains to fix.
- `terminal`: `terminal-registration-writes-session-health` used an obsolete
  exact selector. I fixed it in `8e45dfef` and verified the Nix check now runs
  one test.
- `mind`: `mind-lockfile-cannot-resolve-two-sema-kernels` used an obsolete
  selector and initially ran zero tests. I fixed it in `ae1e573f`; the Nix
  check now runs
  `mind_lockfile_cannot_resolve_duplicate_storage_or_retired_signal_core`.
- Repository-ledger dependency visibility: `signal-repository-ledger` has local
  `origin` set to Gitolite while downstream Cargo dependencies resolve GitHub.
  I pushed `7254e4ae` to the `github` remote as well before updating the meta
  and runtime locks.
- `signal-version-handover`: current `signal-frame` requires the destination
  crate to expose the `nota-text` feature and the dependency feature
  `signal-frame/nota-text`. Without explicit feature passthrough, all-feature
  contract tests fail; with `required-features` alone, Nix would skip the test.
  The repo now has explicit `test-nota-text` and `clippy-nota-text` checks.
- `meta-signal-version-handover`: canonical NOTA witnesses still expected
  bracketed strings for bare-eligible version labels and socket paths. Current
  NOTA correctly emits bare atoms, so the witnesses were updated.
- `version-projection`: the default Nix test intentionally excludes
  `nota-next`, but the repo also owns optional text projection witnesses. The
  full flake gate now runs both default binary-only tests and explicit
  `nota-text` tests.
- `signal-frame`: the refreshed NOTA stack changed canonical text witnesses
  from bracket strings to bare atoms. The default Nix test intentionally
  checks the binary-only path; explicit `nota-text` test and clippy checks now
  exercise the CLI/text macro surface too.
- `signal-sema`: current NOTA rejects non-canonical bracket strings for
  bare-eligible pattern payloads. The pattern tests now witness bare atom
  canonical forms and keep bracket strings only for delimiter-bearing text.
- Downstream sweep needed after foundational support libraries settle:
  component lockfiles refreshed earlier currently point at `signal-frame`
  `166bda84`, while the current frame-kernel main is `e2eae5c2`.

## Next Queue

Continue from the active-repository map, one component family at a time:

1. Foundational active libraries still not covered by this ledger:
   `sema`, `sema-engine`, `triad-runtime`, and `signal`.
2. Dependent lockfile sweep to move already-ported contracts from
   `signal-frame` `166bda84` to `e2eae5c2` after the support-library pass
   finishes.
