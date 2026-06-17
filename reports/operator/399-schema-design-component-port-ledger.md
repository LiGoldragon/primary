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

## Next Queue

Continue from the active-repository map, one component family at a time:

1. `orchestrate`.
2. `signal-repository-ledger` / `meta-signal-repository-ledger` /
   `repository-ledger`.
3. `signal-version-handover` / `meta-signal-version-handover`.
