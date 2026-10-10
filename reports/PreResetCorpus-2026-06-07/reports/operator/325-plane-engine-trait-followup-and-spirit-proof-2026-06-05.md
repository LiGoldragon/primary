# Operator Report 325 — Plane Engine-Trait Follow-Up And Spirit Proof

## Trigger

Designer audit `reports/designer/538-audit-operator-plane-integration.md`
accepted the prior Plane namespace integration but identified one real
follow-up: the engine-trait emission family had not been carried onto
`Plane`, and the architecture rationale for the three-tier boundary had not
landed on `schema-rust-next` main. It also noted harmless-but-dead
`short_header` constants in Spirit's generated Nexus and SEMA modules.

## Code Landed

`schema-rust-next` main now includes commit
`3ebeeda2eac9ecd4e9a345ced28a1b542535768e`
(`schema-rust-next: carry Plane through engine traits`).

The implementation added plane-intrinsic naming methods to `Plane`:

- `engine_trait_name`
- `trace_enum_name`
- `trace_activation_method_name`

The generated Signal, Nexus, and SEMA engine-trait token nouns now consult
those methods instead of hardcoding the trait and trace enum identifiers. The
conditional behavior still lives in the trait token nouns. `Plane` continues
to own only intrinsic plane names, not target selection and not schema/root
presence logic.

The same change added `RustWriter::emits_short_headers()`. Wire contracts and
signal-emitting runtimes still emit short-header constants; NexusRuntime and
SemaRuntime no longer emit orphaned `short_header` modules after signal-frame
support was gated away.

`ARCHITECTURE.md` now records the three-tier rule:

- `Plane` owns intrinsic names.
- `RuntimePlaneSet` / `RustEmissionTarget` own which planes emit.
- Emitter nouns that inspect declarations and roots own schema-presence
  checks.

## Spirit Integration

`spirit` main now includes commit
`46daf37bdcf9a0df4d75c1e48e553b145d5d96f5`
(`spirit: refresh generated planes after Plane trait migration`).

Spirit was moved from `schema-rust-next` `7f59b395` to `3ebeeda2` in both
`Cargo.lock` and `flake.lock`, then regenerated with
`SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --no-default-features`.

The generated output change is intentionally small:

- `src/schema/nexus.rs` lost the dead `pub mod short_header`.
- `src/schema/sema.rs` lost the dead `pub mod short_header`.
- `src/schema/signal.rs` was unchanged and remains the sole owner of
  `encode_signal_frame`, `decode_signal_frame`, `SignalFrameError`, and
  signal short headers.

## Verification

`schema-rust-next`:

- `cargo test --test emission` passed: 32 tests.
- `cargo test` passed: 54 tests across all test targets.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.

`spirit`:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --no-default-features`
  passed.
- `cargo test --all-features` passed, including process-boundary
  subscription and trace tests.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix build .#packages.x86_64-linux.default .#packages.x86_64-linux.trace`
  passed with local builders/cache only.
- `scripts/run-nix-integration-tests` passed all 9 Nix-built integration
  tests.

Environment note: the Prometheus binary cache and remote builder timed out /
failed SSH during the integration run. Nix fell back to local builds and the
tests passed. This is infrastructure noise, not a product failure.

## Production Read

Designer's main concern is closed: the engine-trait family is now on the same
`Plane` naming model as the namespace family, and the rule is documented
where the next emitter migration will read it.

Spirit is slightly cleaner as a production candidate: its generated Nexus and
SEMA modules no longer expose dead public short-header constants that looked
like transport vocabulary. Signal transport remains visibly signal-owned.

The remaining production blockers from report 324 still stand:

- full meta-signal Spirit listener/contract path;
- Nix-built subscription-specific streaming witness;
- deployed `persona-spirit` cutover / migration proof.

One workspace hygiene note remains: the Spirit checkout contains a pre-existing
untracked zero-byte `src/main.rs`. It was not created, modified, or committed
in this pass. Cargo uses the explicit binaries in `src/bin/`, and all cargo
and Nix verification above passed despite that untracked file.
