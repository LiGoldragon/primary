# Listener Scaffold Handoff

## Task And Scope

Approved lane intent: create a fresh Listener speech-to-text component family,
without extending the forked Whisrs repo. The requested shape was the local Rust
component mold: runtime repo with daemon and thin CLIs, ordinary `signal-*`
contract repo, and typed owner/meta contract repo.

Created three fresh public repos:

- `/git/github.com/LiGoldragon/listener`
- `/git/github.com/LiGoldragon/signal-listener`
- `/git/github.com/LiGoldragon/meta-signal-listener`

Also updated the authoritative primary manifest at
`/home/li/primary/protocols/repos-manifest.nota` with the three active entries.

## Doctrine And Conventions Consulted

Read:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- component-architecture, contract-repo, micro-components, repo-intent
- edit-coordination, repository-management, rust-crate-layout, rust-methods,
  rust-errors, naming, abstractions, testing, nix-discipline, nix-usage,
  version-control, repository-closeout, spirit-query
- comparable repos: `mind`, `message`, `signal-mind`, `signal-message`,
  `meta-signal-mind`, `meta-signal-message`
- schema-rust-next contract build driver docs/source

Spirit public text search for Listener/speech/signal terms returned no
Listener-specific public intent records; the accepted lane brief was treated as
the operative repo direction.

Observed and applied conventions:

- canonical checkouts live at `/git/github.com/LiGoldragon/<repo>`;
- repos are public by default;
- every canonical repo gets root `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`,
  `skills.md`, `README.md`, Cargo metadata, flake metadata, lock files, source,
  tests, and Jujutsu history;
- ordinary contracts are named `signal-<component>`;
- owner/meta contracts are named `meta-signal-<component>`;
- contract repos are wire-only and schema-derived through `schema-rust-next`;
- contract flakes expose build, test, round-trip, doc, fmt, and clippy checks;
- component repo has `listener`, `meta-listener`, and `listener-daemon`
  binaries; CLIs are thin clients and daemon owns future state/effects;
- cross-repo Cargo dependencies use Git identities, not sibling `path`
  dependencies.

## Created Repos

### `/git/github.com/LiGoldragon/signal-listener`

Ordinary Listener contract repo.

Key files:

- `schema/lib.schema`: `Start(StartCapture)` and `Stop(StopCapture)` ordinary
  operations; `Started`, `Stopped`, and `RequestUnimplemented` replies; shared
  `ListenerDaemonConfiguration`.
- `src/schema/lib.rs`: checked-in generated wire contract artifact.
- `src/lib.rs`: generated noun re-exports and small accessors.
- `tests/round_trip.rs`: frame and NOTA round-trip witnesses.
- `flake.nix`: Nix build/check surface.

Commit/push:

- GitHub repo: `LiGoldragon/signal-listener`
- Visibility: public
- Default branch: `main`
- Commit: `1b61a61c` (`signal-listener: scaffold Listener ordinary contract`)
- Push: `jj git push --bookmark main` succeeded.

Checks run:

- `SIGNAL_LISTENER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --all-features`: pass
- `cargo test --all-features`: pass, 3 tests
- `cargo fmt --all -- --check`: pass after rustfmt
- `cargo clippy --all-targets --all-features -- -D warnings`: pass
- `nix flake lock`: pass
- `nix flake check`: pass; omitted incompatible `aarch64-linux` checks

### `/git/github.com/LiGoldragon/meta-signal-listener`

Owner/meta Listener contract repo.

Key files:

- `schema/lib.schema`: `Configure(ListenerDaemonConfiguration)` operation;
  `Configured`, `ConfigurationRejected`, and `RequestUnimplemented` replies.
- `build.rs`: imports `signal-listener` schema through Cargo metadata and runs
  `schema-rust-next`.
- `src/schema/lib.rs`: checked-in generated wire contract artifact.
- `src/lib.rs`: generated noun re-exports and small aliases.
- `tests/round_trip.rs`: frame and NOTA round-trip witnesses using the shared
  configuration type from `signal-listener`.
- `flake.nix`: Nix build/check surface.

Commit/push:

- GitHub repo: `LiGoldragon/meta-signal-listener`
- Visibility: public
- Default branch: `main`
- Commit: `a4c8b4d6` (`meta-signal-listener: scaffold Listener meta contract`)
- Push: `jj git push --bookmark main` succeeded.

Checks run:

- `META_SIGNAL_LISTENER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --all-features`:
  pass
- `cargo test --all-features`: pass, 3 tests
- `cargo fmt --all -- --check`: pass after rustfmt
- `cargo clippy --all-targets --all-features -- -D warnings`: pass
- `nix flake lock`: pass
- `nix flake check`: pass; omitted incompatible `aarch64-linux` checks

### `/git/github.com/LiGoldragon/listener`

Listener runtime repo.

Key files:

- `src/main.rs`: `listener` thin ordinary CLI entry point.
- `src/bin/meta_listener.rs`: `meta-listener` thin owner/meta CLI entry point.
- `src/bin/listener_daemon.rs`: `listener-daemon` entry point.
- `src/configuration.rs`: typed rkyv archive helper over
  `signal_listener::ListenerDaemonConfiguration`.
- `src/command.rs`, `src/meta.rs`, `src/daemon.rs`: skeleton-honest runtime
  surfaces that compile and report not-implemented behavior when invoked.
- `tests/configuration.rs`: shared configuration rkyv round-trip witness.
- `flake.nix`: Nix build/check/app surface.

Commit/push:

- GitHub repo: `LiGoldragon/listener`
- Visibility: public
- Default branch: `main`
- Commit: `54a4d208` (`listener: scaffold speech-to-text runtime repo`)
- Push: `jj git push --bookmark main` succeeded.

Checks run:

- `cargo test --all-features`: pass, 1 test
- `cargo fmt --all -- --check`: pass
- `cargo clippy --all-targets --all-features -- -D warnings`: pass
- `nix flake lock`: pass
- `nix flake check`: pass; non-fatal app metadata warnings, all checks passed,
  omitted incompatible `aarch64-linux` checks

## Primary Manifest

Updated rows in `/home/li/primary/protocols/repos-manifest.nota`:

```nota
(Repo signal-listener github:LiGoldragon/signal-listener (Family Signal) Active Architecture [])
(Repo meta-signal-listener github:LiGoldragon/meta-signal-listener (Family MetaSignal) Active Architecture [])
(Repo listener github:LiGoldragon/listener (Family Persona) Active Architecture [])
```

Verification:

- `rg -n "listener" /home/li/primary/protocols/repos-manifest.nota`: showed
  the three rows at lines 63, 87, and 115.

Primary commit/push status:

- Not committed or pushed. Primary already had an unrelated pre-existing dirty
  file, `agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-AiJudgeEvidence.md`,
  before the manifest and this handoff were written. To avoid committing
  unrelated content, primary is left dirty with that pre-existing file, the
  manifest update, and this handoff.

## Implementation Blockers And Follow-Up

- Next worker should implement the daemon transport spine before audio behavior:
  ordinary `signal-listener` socket, owner/meta `meta-signal-listener` socket,
  configuration archive load, and typed unimplemented replies on the live path.
- After transport, implement the first vertical slice in order: default input
  capture, continuous durable capture write, batch transcription on stop, then
  clipboard delivery.
- Keep Whisrs separate. Any reuse should be introduced as an explicit library
  dependency/seam in a later accepted slice.
- Manifest update should be committed from primary once the unrelated dirty
  output is handled or a primary maintainer chooses the appropriate whole-copy
  commit.
