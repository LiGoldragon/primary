# Plane-Gated Emitter And Spirit Production Proof

## Scope

Carried designer's `designer-plane-type-2026-06-05` reference family forward onto the current `schema-rust-next` main, adapted it to the already-landed runtime-mail token emitter, and proved Spirit against the new emitter output.

Code repos:

- `schema-rust-next` main: `7f59b39519788c05ac405d5e03ad92643a70407f`
- `spirit` main: `41d96e701466`

## What changed

`schema-rust-next` now has an internal runtime-plane axis for this emitter family:

- `Plane { Signal, Nexus, Sema }` owns plane-intrinsic names.
- `RuntimePlaneSet::active_planes()` exposes the canonical signal/nexus/sema order.
- Plane namespace and origin-route constructor emission moved from hand-formatted string lines into token nouns:
  - `PlaneNamespaceAlias`
  - `PlaneNamespaceTokens`
  - `PlaneOriginRouteConstructorTokens`
  - `PlaneWrapperPath`

I tightened the designer branch slightly: `PlaneWrapperPath` renders `nexus::Nexus` / `sema::Sema` as tokens directly instead of formatting a string and reparsing it through `RustTypeTokens`.

Signal-frame support is now gated by `writer.emits_signal()`. That means:

- `SignalRuntime` and `ComponentRuntime` keep `InputRoute`, frame encode/decode, and `SignalFrameError`.
- `WireContract`, `NexusRuntime`, and `SemaRuntime` do not receive signal-frame helpers.

Spirit regeneration proved the behavioral effect:

- `src/schema/signal.rs` still owns signal-frame support.
- `src/schema/nexus.rs` lost 159 lines of misplaced signal-frame support.
- `src/schema/sema.rs` lost 139 lines of misplaced signal-frame support.

## Verification

`schema-rust-next`:

- `cargo test --test emission`
- `cargo test --test generation_driver`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`

Spirit cargo:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --no-default-features`
- `cargo check --no-default-features`
- `cargo test --no-default-features --test dependency_surface --test generated_signal_plane --test runtime_triad --test daemon_command`
- `cargo test --features nota-text --test process_boundary`
- `cargo test --features nota-text,testing-trace --test process_boundary cli_receives_testing_trace_events_from_daemon_trace_socket -- --exact`
- `cargo test --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`

Spirit Nix:

- `nix build .#packages.x86_64-linux.default .#packages.x86_64-linux.trace -L --option builders "" --option substituters "https://cache.nixos.org"`
- `scripts/check-local-schema-stack -L --option builders "" --option substituters "https://cache.nixos.org"`
- `scripts/run-nix-integration-tests`

The first schema-stack run was interrupted by the 15-minute guard while actively building, not while idle. A second run with a longer guard completed with `all checks passed`.

The Nix integration script hit the Prometheus cache and SSH builder timeout, then fell back to local builds and passed all 9 ignored Nix-built binary integration tests.

## Production read

This is a real production-readiness step, not just cleanup. The generated split-plane modules now stop carrying signal transport helpers in daemon-internal Nexus and SEMA surfaces, while Spirit still builds and passes cargo, Nix package, Nix flake-check, and Nix-built real-socket integration tests.

What remains material:

- Meta signal is still only represented as an optional daemon configuration socket slot; there is no full `meta-signal-spirit` contract/listener path yet.
- The Nix-built ignored integration suite does not yet include a subscription-specific streaming test, although process-boundary subscription tests pass locally and in the Nix release test matrix.
- Full deployment/cutover from deployed `persona-spirit` to this Spirit was not performed in this slice.

