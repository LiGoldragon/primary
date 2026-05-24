# 170 - Schema Spirit MVP implementation, 2026-05-24

## Status

This pass lands the first runnable subset of the `/321` through `/324`
Spirit MVP stack.

The implemented subset is Nix-green across the participating repos:

- schema-driven `signal_channel!([schema])` for the Spirit working
  signal
- schema-derived `LogVariant` projection into `ShortHeader`
- receive-side `ShortHeader` triage for Spirit operations
- a box-form NOTA primitive in `nota-codec`
- `signal-sema` universal observation projection through `LogVariant`
- a typed v0.1.0 to v0.1.1 Spirit projection witness
- `persona-spirit` consuming the projected signal contract

This is not the full `/324` target. The macro does not yet emit every
payload type from schema, does not yet derive all version projections
from schema diff, and does not yet replace generated NOTA codecs with
box-form calls. It proves the path through real repos and Nix checks.

## Sources read

- `reports/designer/320-mvp-schema-language-pilot-unblock.md`
- `reports/designer/321-mvp-visual-state-of-play.md`
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
- `reports/designer/325-nota-box-library-design-and-implementation.md`
- `reports/designer/326-v2-spirit-complete-schema-vision.md`
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
- `reports/second-operator/178-schema-section-shape-and-nota-map-check-2026-05-24.md`
- `reports/nota-designer/6-quoted-string-purge-audit-2026-05-24.md`

## Landed commits

`signal-frame`

- `84e46617f17e` - `signal-frame: add schema LogVariant MVP`
- `75b318041b36` - `signal-frame: parse nested schema stream relations`
- `13a21567a2a6` - `signal-frame: align schema field inference with Spirit MVP`
- `569ee09a0d1f` - `signal-frame: expose short-header operation triage`
- `18b4e2be4555` - `signal-frame: emit operation dispatch handlers`

`signal-sema`

- `e48223dab695` - `signal-sema: add LogVariant schema projection`

`nota-codec`

- `38f5e41543fa` - `nota-codec: add box-form payload container`

`signal-persona-spirit`

- `b86a78553a17` - `signal-persona-spirit: drive channel from schema`
- `c9cf88a323da` - `signal-persona-spirit: add v010 projection witness`
- `cf2f92ee3830` - `signal-persona-spirit: witness generated dispatch`

`persona-spirit`

- `f8bf8546e9b4` - `persona-spirit: consume schema-driven signal contract`
- `262cf054ca00` - `persona-spirit: consume Spirit projection contract`
- `a834a560c487` - `persona-spirit: consume dispatch contract`

## What changed

### signal-frame

Added `LogVariant`, a small projection trait for translating a typed
value into the eight-byte `ShortHeader` surface. `Request<Payload>`
can now derive its short header when `Payload: LogVariant`, and
`ClientFrame::request_frame` carries that header into the frame.

The proc macro now supports the MVP `signal_channel!([schema])` form.
It reads `schema.nota` from the downstream crate's `CARGO_MANIFEST_DIR`,
parses the `/322` vector-of-root-verb-enums form, builds the channel
model, and emits the same public contract family the old Rust-form macro
emitted for the Spirit case.

For receive-side triage, the macro emits:

- `Operation::into_frame(exchange)`
- `Operation::kind_from_short_header(ShortHeader) -> Option<OperationKind>`
- `OperationHandler`, with one async `handle_<operation>` method per
  operation variant
- `OperationDispatch`, which rejects short-header / decoded-operation
  mismatches before handing the payload to the per-variant handler

The first byte of the header selects the root operation kind. Nested
subslots are emitted for schema cases the Spirit tests cover, including
`Observe Records WithProvenance`.

### signal-sema

Added `magnitude.schema.nota` and `LogVariant` implementations for
`SemaOperation` and `SemaObservation`.

This keeps Sema as the universal classification and observation layer:
the header contains operation class, outcome class, and operation-class
metadata without making Sema the executable command payload.

### nota-codec

Added `box_form` as the first implementation of the ordered-vector-of-boxes
encoding. The binary shape is:

- schema-sized root bytes supplied by the caller
- `u32` big-endian length prefix per box
- box payload bytes in schema declaration order

The implementation includes:

- `BoxedNotaEncoder`
- `BoxedNotaDecoder`
- typed truncation and overflow errors
- tests for Spirit-style Entry boxes, skipping, empty boxes, and malformed
  input

Designer `/323` originally frames this as a `nota-box` library under the
`nota` repo. The `nota` repo declares itself spec-only in its local
`AGENTS.md`, so this implementation landed in `nota-codec` as the
existing Rust NOTA codec crate. That is an implementation placement
decision, not a change to the wire idea.

### signal-persona-spirit

Added `schema.nota` and moved the working signal from the old Rust
macro body to:

```rust
signal_frame::signal_channel!([schema]);
```

The schema refers to Magnitude through a vendored local schema snapshot
at `schemas/signal-sema/magnitude.schema.nota`. Cross-repo schema refs
work in local builds but not in Nix-isolated downstream macro execution
without explicitly providing the referenced schema files. The vendored
snapshot is the current reproducible path.

Added `tests/short_header.rs` to prove:

- `Record` emits `[1, 0, 6, 0, 0, 0, 0, 0]`
- length-prefixed frame peek recovers that header without decoding the
  payload
- `Operation::kind_from_short_header` maps headers back to root kinds
- nested `Observe Records WithProvenance` emits `[2, 1, 1, 0, 0, 0, 0, 0]`
- the macro-emitted `OperationDispatch` routes `Record` to the generated
  `handle_record` method when the short header matches
- the same dispatch surface rejects header/body mismatch with
  `OperationDispatchError::HeaderOperationMismatch`

Added `src/migration.rs` with a typed v0.1.0 historical module and
`V010ToV011` projections. The v0.1.0 `Certainty` enum maps to the
v0.1.1 `Magnitude` enum for the common variants, and v0.1.0 `Record`
NOTA decodes into the current `Operation::Record`.

### persona-spirit

Updated the runtime crate to consume the schema-driven and projection-capable
`signal-persona-spirit` commit. The runtime path still compiles and the full
repo flake check passes.

Updated again to consume the generated dispatch contract from
`signal-persona-spirit@cf2f92ee3830`. This is a lockfile-only consumer bump:
the daemon is not yet using the generated `OperationDispatch` trait on its
production request path.

## Follow-up schema-shape correction

Designer `/326-v2` supersedes the flat schema example in `/326-v1` and
responds to the psyche's correction from this session. The current canonical
complete-schema direction is:

- outer record: `(Schema (Channel ...) (Namespace {...}))`
- `Channel` first, carrying the messaging surface
- `Namespace` second, carrying a curly-brace NOTA map of type names to
  declarations or path references
- no schema section comments as structural markers

The runnable MVP in `signal-persona-spirit/schema.nota` has not yet been moved
to that corrected shape. It is still the `/322`-style flat vector of
declarations. The green tests therefore prove the old MVP schema machinery plus
the new dispatch surface; they do not prove `/326-v2` parsing or generation.

`nota-codec` already supports the curly-brace map form needed by `/326-v2`.
The relevant tests passed through both local Cargo and the repo's Nix flake
check:

- `map_key_round_trip`
- `bracket_string_round_trip`

## Verification

All verification below used the low-core discipline for Cargo and remote
builder discipline for Nix:

- `CARGO_BUILD_JOBS=2 cargo test`
- `nix flake check --option max-jobs 0`

Passing repos:

- `signal-frame`
- `signal-sema`
- `nota-codec`
- `signal-persona-spirit`
- `persona-spirit`

The final `persona-spirit` Nix check passed after updating to
`signal-persona-spirit@cf2f92ee3830`.

## Remaining gaps against /324

The remaining work is real and should not be hidden by the green MVP:

1. The schema macro still depends on hand-written payload records in
   `signal-persona-spirit/src/lib.rs`. It does not yet emit all signal
   payload types directly from schema.
2. The v0.1.0 to v0.1.1 projection is a typed witness, but not a generic
   schema-diff-derived implementation.
3. The macro now emits an async operation dispatch trait and a contract-side
   witness proves it routes by `ShortHeader`, but the production
   `persona-spirit` daemon is not yet wired through that generated trait.
4. `BoxedNotaEncoder` and `BoxedNotaDecoder` exist, but generated contract
   codecs do not yet call them automatically.
5. The hard-handover offline-test marker described in `/323 §10` has not
   been added to sema-engine/persona-spirit startup gating in this pass.
6. Cross-schema references need a durable Nix-aware dependency model. The
   current Spirit schema uses a vendored local Magnitude schema snapshot.
7. `/326-v2`'s corrected `(Schema (Channel ...) (Namespace {...}))` shape is
   not implemented in `signal-frame`'s schema parser or in
   `signal-persona-spirit/schema.nota` yet.

## Operator recommendation

Treat this as the first runnable proof, not as closure of
`primary-ezqx.1`. The next operator pass should continue in this order:

1. Move the schema parser and Spirit schema file to `/326-v2`'s corrected
   outer `(Schema ...)` + namespace-map shape.
2. Make schema-derived payload type emission real for the Spirit contract.
3. Make the version projection derive from the old/current schema pair.
4. Wire the production daemon's operation execution through the generated
   dispatch trait once the trait's shape survives review.
5. Replace generated NOTA codec internals with box-form calls for unsized
   fields.
6. Add the hard-handover offline-test marker and Nix witness.
7. Revisit whether `nota-codec::box_form` should remain there or be split
   once the `nota` repo's spec-only boundary changes.
