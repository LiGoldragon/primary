# Operator Report 326 — Plane Trace Completion And Doc Fix

## Trigger

Designer audit `reports/designer/539-audit-engine-trait-followup.md` found the
previous follow-up functionally sound, but still partial: engine-trait names
were Plane-derived, while the trace object-name emission path still hardcoded
`SignalObjectName`, `NexusObjectName`, and `SemaObjectName`. The audit also
identified two documentation defects in `schema-rust-next/ARCHITECTURE.md`
and a pending-added zero-byte `spirit/src/main.rs` residue.

## Code Landed

`schema-rust-next` main now includes commit
`9ca87549114cb20eaad9a1f17fe607357cbedeff`
(`schema-rust-next: carry Plane through trace object names`).

Changes:

- `TraceObjectNameEnumTokens` now carries `Plane` and derives its enum name
  and actor rendered prefix from `Plane`.
- `TraceSupportTokens` now carries a `Vec<Plane>` and derives `ObjectName`
  variants and match arms from each plane's wrapper and trace enum names.
- `RustWriter::emit_trace_support` now builds that plane list and calls
  `emit_object_name_enum(Plane, ...)` instead of passing string pairs.
- `ARCHITECTURE.md` now states the actual `WireContract` behavior:
  wire contracts emit schema nouns, derives, NOTA/rkyv codecs, and
  short-header route constants; they do not emit runtime envelopes, engine
  traits, mail support, trace support, or signal-frame encode/decode helpers.

This is a no-output-regression codegen cleanup: generated Rust stayed
byte-identical under the existing fixtures while the naming source moved to
`Plane`.

## Spirit Integration

`spirit` main now includes commit
`bc28feb8ea32458d22f5526e305e80330991dddf`
(`spirit: bump schema-rust-next for Plane trace completion`).

Spirit was bumped from `schema-rust-next` `3ebeeda2` to `9ca87549` in
`Cargo.lock` and `flake.lock`. Regeneration produced no generated schema-file
changes.

The zero-byte `src/main.rs` residue was cleared from the index and worktree.
It was not committed.

## Verification

`schema-rust-next`:

- `cargo test --test emission` passed: 32 tests.
- `cargo test` passed: 54 tests.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.

`spirit`:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --no-default-features`
  passed and produced no generated schema diff.
- `cargo test --all-features` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix build .#packages.x86_64-linux.default .#packages.x86_64-linux.trace`
  passed with local builders/cache only.

## Production Read

Designer audit 539's concrete code/doc findings are closed:

- Plane owns the runtime plane names claimed by the architecture doc,
  including trace object-name enum names.
- WireContract documentation no longer claims signal-frame encode/decode.
- The empty Spirit `src/main.rs` cannot be swept into a later whole-working-copy
  commit.

The larger production blockers remain unchanged from reports 324 and 325:
full meta-signal listener/contract path, a Nix-built subscription-specific
streaming witness, and deployed `persona-spirit` cutover / migration proof.
