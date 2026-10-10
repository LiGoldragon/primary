# Overview

## What Landed

`triad-runtime` now owns shared role traits for reusable engine-role names. Component schemas still define concrete variants, but the runner speaks through traits such as `NexusWork`, `NexusAction`, `SemaWriteInput`, `SemaReadInput`, and effect roles.

`schema-rust-next` now emits those role trait impls for runtime targets. It also avoids duplicate impls when a Nexus runtime imports a SEMA root from another plane. Wire-contract targets do not emit runtime role impls.

`triad-runtime` now has a multi-listener daemon shell for ordinary/meta socket shapes. It is many listeners to one runtime owner, not many listener threads racing one engine.

`spirit` is regenerated against those dependencies. Generated roles live under `spirit::schema::{signal,nexus,sema}` and the crate root no longer re-exports generated plane nouns. Tests import generated internals through plane modules, making the intended boundary visible in test code.

## Proof

Verification completed:

- `triad-runtime`: `cargo test`, `cargo clippy --all-targets -- -D warnings`;
- `schema-rust-next`: `cargo test`, `cargo clippy --all-targets -- -D warnings`;
- `spirit`: `cargo test`, `cargo test --all-features`, `cargo clippy --all-targets --all-features -- -D warnings`, `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --no-run`.

Spirit added two focused regressions:

- generated plane roots implement the shared `triad-runtime` role traits;
- `src/lib.rs` does not flatten generated Signal/Nexus/SEMA nouns into `spirit::*`.

## Remaining

The streaming/push claim was real and has now been implemented as shared
schema/emission/runtime substrate in
`reports/operator/321-schema-derived-streaming-push-implementation-2026-06-05/`.
What remains is a component pilot that declares a real stream and wires
long-lived delivery through a daemon.
