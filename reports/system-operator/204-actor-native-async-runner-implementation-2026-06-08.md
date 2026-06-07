# Actor-Native Async Runner Implementation — 2026-06-08

## Psyche Correction

[Actor-native migrations should change the generator and runtime source of truth instead of stopping at compatibility bridges; no backward compatibility, best design only.]

This report records the corrective implementation after the earlier `lojix`
actor-native migration stopped at a compatibility bridge: an actor-native
listener shell with synchronous generated Nexus execution isolated through
`spawn_blocking`.

## Implemented Shape

The async boundary now lives where it belongs:

- `triad-runtime` owns an async recursive runner. `Runner::drive` is async, and
  SEMA writes, SEMA reads, and effects are awaited runner steps.
- `schema-rust-next` emits async Nexus runtime glue. Generated
  `NexusEngine::execute` returns a future; generated SEMA/effect hooks return
  futures; generated runner adapters await `triad_runtime::Runner::drive`.
- Generated runtime engine traits are `Send`, because actor-native execution
  futures must be movable across Tokio task boundaries.
- `lojix` consumes the generated async runner directly. The daemon awaits
  `engine.execute(work).await`; there is no `spawn_blocking` bridge around
  generated Nexus execution.
- `lojix` child-process effects use `tokio::process::Command`, so deploy
  effects are awaited as async process work.

## Commits

- `triad-runtime` `069ba8ed` — `triad-runtime: make runner effects async`
- `schema-rust-next` `5cadd257` — `schema-rust-next: emit async Nexus runner hooks`
- `lojix` `f9be5df8` — `lojix: await generated Nexus runner directly`

## Verification

`triad-runtime`:

- `cargo fmt --check`
- `cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`

`schema-rust-next`:

- `cargo fmt --check`
- `cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`

`lojix/triad-port`:

- `cargo fmt --check`
- `cargo check --all-targets --all-features`
- `cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `NIX_CONFIG=$'max-jobs = 0\ncores = 2\nbuilders-use-substitutes = true' timeout 900 cargo test --test build_smoke eval_dune_fixture_through_the_engine -- --ignored --nocapture --test-threads=1`

The ignored eval smoke passed and reached `Deployed` through the real engine
pipeline and real `nix eval` with local builds disabled.

## Regression Guards

`lojix/triad-port/tests/actor_native_runtime.rs` now requires:

- actor-native multi-listener markers;
- direct awaited `engine.execute(work).await`;
- async generated hook implementations;
- `tokio::process::Command` in the schema runtime.

It forbids:

- `spawn_blocking` in `src/daemon.rs`;
- `std::process::Command` in `src/schema_runtime.rs`;
- the older blocking listener markers.

## Remaining Gaps

- I did not run the ignored slow build smoke. It can realize a closure and
  should be run only with remote-builder safety confirmed.
- `lojix` still has no repo flake check surface.
- `lojix` still uses the in-memory shared `Store`; durable `sema-engine` backing
  remains a separate storage cutover.
- The daemon binary owner-socket eval smoke was not rerun in this pass; the
  engine-level real `nix eval` smoke was.
