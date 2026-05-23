# owner-signal-persona-agent contract implementation

Implemented bead `primary-gvgj.2` by creating `/git/github.com/LiGoldragon/owner-signal-persona-agent` as a new owner-only Signal contract crate.

## Created files

- `.gitignore`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `CLAUDE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `examples/canonical.nota`
- `flake.lock`
- `flake.nix`
- `rust-toolchain.toml`
- `skills.md`
- `src/lib.rs`
- `tests/round_trip.rs`

## Contract shape

`src/lib.rs` declares one `signal_channel!` owner surface with operations:

- `SpawnAgent(SpawnAgent)`
- `RetireAgent(RetireAgent)`
- `SetBackendPolicy(SetBackendPolicy)`
- `MutateBackendConfiguration(MutateBackendConfiguration)`
- `RouteThroughAgent(RouteThroughAgent)`

Replies cover successful owner mutations, generic `OrderRejected`, and `RequestUnimplemented`. The channel includes the current `observable { filter default; operation_event OperationReceived; effect_event EffectEmitted; }` block, matching the newer owner-contract pattern.

Because `/git/github.com/LiGoldragon/signal-persona-agent` was absent when this task started, the crate defines local compatible shared nouns: `AgentIdentifier`, `AgentBackend`, `LaneName`, `WirePath`, `BackendConfiguration`, backend endpoint/availability, model, thinking-level, and extension records. These should be factored or re-exported with `signal-persona-agent` when the ordinary contract lands.

`MutateBackendConfiguration` uses the full English word rather than the abbreviated `MutateBackendConfig` spelling from the design sketch.

## Validation commands

- `cargo fmt --all && cargo test --test round_trip` → exit 0 after fixing canonical NOTA boolean spelling (`True`). Evidence: 5 round-trip tests passed.
- `cargo test` → exit 0. Evidence: 5 integration tests passed; doc tests passed.
- `nix flake check --option max-jobs 0 -L` → exit 0. Evidence: build, test, test-round-trip, test-doc, doc, fmt, and clippy checks passed.

Failed intermediate checks and fixes:

- First `nix flake check --option max-jobs 0 -L` failed on the copied Rust 1.85 toolchain hash; updated the flake/toolchain to Rust 1.88.0 using the existing workspace pattern from `kameo-testing-assistant`.
- Second `nix flake check --option max-jobs 0 -L` failed because `craneLib.cleanCargoSource` omitted `examples/canonical.nota`; added a source filter that includes `examples/` for the test `include_str!` fixture.

## Version control

Initialized a colocated jj repo and committed locally. No push was performed.

- jj change identifier: `qrksosztoplrmlllultspolvtnnyxxml`
- git commit short identifier: `0ffd710ab84e`
- bookmark: `main`
- commit message: `owner persona agent contract scaffold`

## Notes and next steps

- `/home/li/primary/context.md` and `/home/li/primary/plan.md` were missing (`ENOENT`), so implementation proceeded from the task prompt, bead, required skills, and designer reports `/309` and `/310`.
- Close recommendation: close `primary-gvgj.2` after supervisor review, with note that the owner contract crate, ARCH/AGENTS/docs, tests, flake, and local jj commit are in place.
- Follow-up: when `signal-persona-agent` is ready, reconcile/factor the shared `AgentIdentifier`, `AgentBackend`, `LaneName`, and `BackendConfiguration` vocabulary so owner and ordinary contracts compile against one shared definition or an intentional re-export boundary.
