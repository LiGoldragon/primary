# Designer Worktree Pattern Integration

## Inputs Reviewed

- `~/wt/github.com/LiGoldragon/schema-rust-next/codec-opt-in-2026-05-30`
- `~/wt/github.com/LiGoldragon/spirit-next/daemon-zero-nota-2026-05-30`

The schema-rust worktree was a linear polish branch over operator main. The
spirit-next worktree was a larger architectural prototype: workspace split,
owner-signal config, state-aware startup, numerator enum, zero-NOTA daemon, and
tests. It also removed the current flake/Nix proof harness, so it is not a
safe wholesale replacement for main.

## Integrated Now

### schema-rust-next

Integrated the designer branch directly:

- `RustEmissionOptions::default()` now chooses
  `FeatureGated { feature: "nota-text" }`.
- `RustEmitter::default()` follows that default.
- Fixture snapshots now bind the feature-gated default.
- A binary-only generated snapshot proves `NotaSurface::Disabled` removes every
  `nota_next`, `NotaDecode`, `NotaEncode`, `FromStr`, `Display`, `to_nota`, and
  `from_nota_block` surface while keeping `rkyv` and signal frames.

Verification:

- `cargo fmt && cargo test`

### spirit-next

Integrated the strongest low-risk patterns from the workspace prototype without
dropping the current Nix harness:

- `tests/dependency_surface.rs` runs `cargo tree --edges normal` and proves the
  binary-only surface has no `nota-next` runtime dependency, while the
  `nota-text` surface does.
- `tests/socket_negative.rs` feeds length-prefixed NOTA bytes and arbitrary
  bytes through `SignalTransport`, and raw NOTA directly through
  `Input::decode_signal_frame`; all must reject.
- `INTENT.md`, `ARCHITECTURE.md`, and flake structural guards now name those
  tests as part of the zero-NOTA daemon contract.
- `Cargo.lock` and `flake.lock` now pin `schema-rust-next` at the designer
  polish commit.

Verification:

- `cargo test --no-default-features`
- `cargo test --features nota-text`
- `nix flake check`
- `./scripts/run-nix-integration-tests`

## Follow-Up From Report 432

Designer report 432 flagged one stale name in the operator slice:
`Configuration::from_single_argument` still sounded like the old NOTA argument
parser even though the value is now a binary configuration path. That is now
renamed on `spirit-next` main:

- `Configuration::from_binary_path(...)`
- `spirit-next-daemon` calls the path-named method.
- Nix source guards look for `from_binary_path`.

Verification:

- `cargo fmt && cargo test --no-default-features && cargo test --features nota-text`
- `nix flake check`

## Deferred From The Prototype

The workspace split is valuable but too large to land by replacement:

- separate crates for working signal, owner signal, engine, daemon, and CLI;
- owner-signal configuration operations;
- `DaemonState` persisted at a default state path;
- standby mode that binds only the owner/config socket until configuration
  arrives;
- numerator enum over accepted signal interfaces.

Those are the next design target, but they should land as a deliberate migration
that preserves or rewrites the Nix proof harness at the same time. Main now
keeps the smaller single-crate layout while carrying the executable zero-NOTA
proofs that were missing.
