# 219 — orchestrate contract modernization stop point

## Context

The orchestrate triad was checked after the message, mind, and router upkeep slices.

The runtime component is already in the newer daemon shape:

- `orchestrate-daemon` owns the store and daemon lifecycle.
- `orchestrate` is the ordinary thin CLI.
- `meta-orchestrate` is the meta-policy thin CLI.
- Generated `src/schema/{nexus,sema,daemon}.rs` modules drive the runtime path.
- Ordinary and meta sockets are separate.

The contract crates are the remaining issue.

## Finding

`signal-orchestrate` and `meta-signal-orchestrate` are half-migrated.

Each contract crate has:

- an authored `schema/lib.schema`;
- a checked-in generated `src/schema/lib.rs`;
- schema-contract tests proving the schema lowers;
- a separate handwritten public `src/lib.rs` that still declares the real exported wire surface with `signal_channel!`;
- default `nota-text` features and unconditional NOTA dependencies in the handwritten surface.

The runtime then bridges the two worlds. It accepts generated schema-frame inputs on the process boundary, projects them into the handwritten `OrchestrateRequest` / `MetaOrchestrateRequest` types for service execution, then projects replies back into generated schema outputs.

That bridge is working and well-tested, but it means schema is not yet the single source of truth for these public contracts.

## Verification

The current bridge is green:

- `signal-orchestrate`: `cargo fmt --check`, `cargo test --all-features`, `cargo check --all-targets --no-default-features`
- `meta-signal-orchestrate`: `cargo fmt --check`, `cargo test --all-features`, `cargo check --all-targets --no-default-features`
- `orchestrate`: `cargo fmt --check`, `cargo check --all-targets --no-default-features`, `cargo check --all-targets`, `cargo test --all-features`

No source changes were needed to keep the current bridge working.

## Why this is a stop point

This is broader than a dependency or generated-artifact refresh:

- `signal-orchestrate/src/lib.rs` is about 1,100 lines.
- `signal-orchestrate/src/schema/lib.rs` is about 1,500 lines.
- `meta-signal-orchestrate/src/lib.rs` is about 240 lines.
- `meta-signal-orchestrate/src/schema/lib.rs` is about 840 lines.
- `orchestrate` has a large projection layer between generated schema nouns and handwritten contract nouns.

Removing the duplication means changing the public contract export strategy, not just tests or lockfiles. The migration should be reviewed as its own contract conversion.

## Recommended next slice

Treat orchestrate contract modernization as a focused triad migration:

1. Make `signal-orchestrate` export generated schema nouns as the public surface.
2. Preserve compatibility aliases where callers expect them: `OrchestrateRequest`, `OrchestrateReply`, `OrchestrateFrame`, `OrchestrateFrameBody`, and operation-kind helpers.
3. Reattach validation methods on generated nouns: role identifiers, lane identifiers, wire paths, task tokens, and scope reasons.
4. Make `default = []` and gate NOTA behind `nota-text`, matching newer contracts.
5. Repeat the same pattern for `meta-signal-orchestrate`, with imports from the generated ordinary contract.
6. Delete or drastically shrink the projection layer in `orchestrate/src/execution.rs`.
7. Keep the current daemon/CLI process-boundary tests as the acceptance gate.

## Operator stance

Do not block the broader component-upkeep queue on this bridge. The runtime is green and usable. The duplicated contract source should be scheduled as a focused orchestrate-contract migration because it changes the public Rust API and removes a large translation layer.

