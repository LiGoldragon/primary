# Schema-CC Main-Readiness Integration

## Verdict

The schema-cc prototype is now integrated as a build-time crate inside `schema-next`, not left as a standalone proof. The real `schema-next` TypeReference parenthesis resolver is generated from NOTA grammar data, and the resulting stack has been propagated through the Spirit production integration branch and the agent triad that Spirit's Nix gate vendors.

This is ready for main-merge review from the operator side: all affected worktrees are clean, pushed, and tested through Cargo and Nix.

## What Changed

- `schema-next` now contains `schema-cc` as a workspace member and build dependency.
- `schema-next/build.rs` reads `schemas/reference-grammar.nota` and emits `OUT_DIR/reference_resolver.rs`.
- `schema-next/src/schema.rs` includes the generated resolver and no longer owns the hand-written parenthesis dispatch body.
- The grammar data is package-safe for Cargo/Nix: it lives under `schemas/`, and `.nota` is included in the schema-next flake source filter.
- `schema-rust-next`, `signal-spirit`, `meta-signal-spirit`, and `spirit` are pinned to the packaged schema-cc resolver stack.
- Spirit's Nix vendor patcher now understands that the agent contracts and daemon use the structural schema toolchain.
- `signal-agent`, `meta-signal-agent`, and `agent` were moved to positional schema syntax / structural schema-toolchain pins because Spirit's full Nix check vendors them too.

## Pushed Commits

Schema stack:

- `schema-next` `23299642` — packaged grammar-data resolver integration.
- `schema-rust-next` `9a27332e` — pin packaged schema-cc grammar integration.
- `signal-spirit` `19de94ec` — pin packaged schema-cc grammar stack.
- `meta-signal-spirit` `5fd7b39b` — pin packaged schema-cc grammar stack.
- `spirit` `01dd32b4` — lock schema-cc stack and agent positional contracts.

Agent stack required by Spirit's Nix gate:

- `meta-signal-agent` `e7a7343c` — positional schema syntax and structural schema toolchain.
- `signal-agent` `be59074b` — positional schema syntax and structural schema toolchain.
- `agent` `8f2cf042` — pin positional contracts and structural schema toolchain.

## Verification

Per-layer Cargo/Nix gates passed:

- `schema-next`: `cargo test --workspace`, `cargo clippy --workspace --all-targets -- -D warnings`, `nix flake check --max-jobs 0`.
- `schema-rust-next`: `cargo test`, `cargo clippy --all-targets -- -D warnings`, `nix flake check --max-jobs 0`.
- `signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `meta-signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `meta-signal-agent`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `signal-agent`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `agent`: `AGENT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --features nota-text`, `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `spirit`: `cargo build --features nota-text`, `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.

The Spirit Nix check ran the full flake check set and passed, including build, test, clippy, docs, schema-source, binary-boundary, no-free-function, no-unit-struct, and retired-surface checks.

## Review Notes

Two integration bugs were found and fixed by running the Nix gate instead of stopping at Cargo:

- `schema-next` initially packaged the grammar under the nested `schema-cc/` crate, which Cargo's git vendoring did not include for downstream build scripts. Moving the grammar to `schemas/reference-grammar.nota` made the generated resolver reproducible downstream.
- Spirit's Nix vendor patcher still expected old agent contract dependency branches. Updating the patcher exposed the real current dependency shape and made the full vendor-source build pass.

The generated artifacts for the agent contracts did not drift when their schema syntax was migrated, which is the expected losslessness signal for the positional rewrite.

## Remaining Merge Shape

The schema/Spirit stack is still on the shared `structural-forms-integration` branch family, which is the intended code-repo integration line before operator main landing. The agent triad changes are on their code-repo `main` branches because Spirit's deploy/test path consumes those repos from `main` today.

I did not deploy from this slice. This report covers merge-readiness and full local/Nix verification.
