# 170 - Schema Spirit MVP implementation, 2026-05-24

## Status

This pass lands the first runnable subset of the `/321` through `/326-v6`
Spirit MVP stack.

The implemented subset is Nix-green across the participating repos:

- schema-driven `signal_channel!([schema])` for the Spirit working
  signal
- schema-derived `LogVariant` projection into `ShortHeader`
- receive-side `ShortHeader` triage for Spirit operations
- a box-form NOTA primitive in `nota-codec`
- `signal-sema` universal observation projection through `LogVariant`
- a typed v0.1.0 to v0.1.1 Spirit projection witness
- `/326-v3` tagless positional schema parsing, with the namespace as a
  curly-brace NOTA map
- `/326-v5` schema file-body parsing, with non-recursive namespace values:
  `Kind [Decision ...]`, `Topic (String)`, `Entry (Topic Kind ...)`
- `/326-v6` bare-identifier alias/reference declarations in namespace value
  position, with short-header emission following aliases
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
- `reports/designer/326-v3-spirit-complete-schema-vision.md`
- `reports/designer/326-v5-spirit-complete-schema-vision.md`
- `reports/designer/326-v6-spirit-complete-schema-vision.md`
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
- `f133b33881a4` - `signal-frame: parse schema record namespaces`
- `b26f381f2b27` - `signal-frame: fix engine annotation nesting`
- `f6ff41e42603` - `signal-frame: parse positional schema files`
- `8dc8acf40f29` - `signal-frame: parse schema file bodies`
- `f7c032854250` - `signal-frame: parse schema alias declarations`

`signal-sema`

- `e48223dab695` - `signal-sema: add LogVariant schema projection`

`nota-codec`

- `38f5e41543fa` - `nota-codec: add box-form payload container`

`signal-persona-spirit`

- `b86a78553a17` - `signal-persona-spirit: drive channel from schema`
- `c9cf88a323da` - `signal-persona-spirit: add v010 projection witness`
- `cf2f92ee3830` - `signal-persona-spirit: witness generated dispatch`
- `e8d6084b9da1` - `signal-persona-spirit: use schema namespace map`
- `a66c87484109` - `signal-persona-spirit: use positional schema shape`
- `655cc6fb2b4e` - `signal-persona-spirit: use schema file body`
- `bfea608bee9b` - `signal-persona-spirit: consume schema alias parser`

`persona-spirit`

- `f8bf8546e9b4` - `persona-spirit: consume schema-driven signal contract`
- `262cf054ca00` - `persona-spirit: consume Spirit projection contract`
- `a834a560c487` - `persona-spirit: consume dispatch contract`
- `265f4aafe73c` - `persona-spirit: consume schema namespace contract`
- `f9eb7c440a1b` - `persona-spirit: consume positional schema contract`
- `95be1d3c9bcd` - `persona-spirit: consume schema file contract`
- `08b04c73bf60` - `persona-spirit: consume schema alias contract`

## What changed

### signal-frame

Added `LogVariant`, a small projection trait for translating a typed
value into the eight-byte `ShortHeader` surface. `Request<Payload>`
can now derive its short header when `Payload: LogVariant`, and
`ClientFrame::request_frame` carries that header into the frame.

The proc macro now supports the MVP `signal_channel!([schema])` form.
It reads `schema.nota` from the downstream crate's `CARGO_MANIFEST_DIR`,
parses the earlier `/322` vector-of-root-verb-enums form, the tagged
`/326-v2` compatibility form, and the current tagless `/326-v3` positional
record form:

```nota
(
  ((Operation ...) (Reply ...) (Event ...) (Observable ...))
  {...})
```

The current form makes the outer structure meaningful by position. Field 0 is
the channel block, carrying the messaging surface. Field 1 is the namespace, a
curly-brace NOTA map from local type names to declarations or schema references.
The parser rejects mismatched map keys and declarations, such as
`Entry (Record ...)`.

The parser infers namespace declarations in two passes. Unit enum leaves such
as `Kind (Kind Decision Principle ...)` remain leaves; declarations whose
variant payloads resolve to known namespace names become data variants. This
keeps mixed enums such as `Observation (Observation State (Records RecordQuery)
Topics Questions)` expressible without adding labeled fields or comments as
schema structure.

The parser also understands the MVP `(engine <class>)` annotation on operation
payload records and `(Path <path>)` namespace references, while preserving the
existing generated public contract family for the Spirit case.

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

The schema now uses the corrected `/326-v3` tagless positional shape. It refers
to Magnitude through a vendored local schema snapshot at
`(Path schemas/signal-sema/magnitude.schema.nota)`. Cross-repo schema refs work
in local builds but not in Nix-isolated downstream macro execution without
explicitly providing the referenced schema files. The vendored snapshot is the
current reproducible path.

The `Observable` section remains macro-injected/hand-written for this pass.
`OperationReceived` and `EffectEmitted` stay out of the schema namespace until
the generated observable event payloads and generated `OperationKind` type are
made first-class schema products.

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
`signal-persona-spirit@cf2f92ee3830`, the corrected namespace schema contract
from `signal-persona-spirit@e8d6084b9da1`, and the tagless positional schema
contract from `signal-persona-spirit@a66c87484109`. These are lockfile-only
consumer bumps: the daemon is not yet using the generated `OperationDispatch`
trait on its production request path.

## Follow-up schema-shape corrections

Designer `/326-v3` supersedes `/326-v2`, which had superseded the flat schema
example in `/326-v1`. The current canonical complete-schema direction is:

- outer record with two positional fields, no `Schema` tag
- field 0: channel block, no `Channel` tag, carrying the messaging surface
- field 1: curly-brace NOTA map, no `Namespace` tag, carrying type names to
  declarations or path references
- no schema section comments as structural markers

The runnable MVP in `signal-persona-spirit/schema.nota` has now been moved to
that corrected shape. The green tests prove both the old MVP schema machinery
and the `/326-v3` parser path, plus the new dispatch surface. The parser keeps
the tagged `/326-v2` form as a compatibility path, but the Spirit schema file no
longer uses it.

`nota-codec` already supports the curly-brace map form needed by `/326-v3`.
The relevant tests passed through both local Cargo and the repo's Nix flake
check:

- `map_key_round_trip`
- `bracket_string_round_trip`

## Follow-up after /326-v5

The psyche rejected `/326-v4`'s namespace value form because entries such as
`Kind (Kind ...)`, `Topic (Topic ...)`, and `Entry (Entry ...)` repeat the
declared key inside the declaration value. That is name collision in the
schema's open namespace and reads as recursive type structure.

Designer `/326-v5` closed the syntax by making the map key the implicit type
tag:

- `[…]` declares enum variants, for example
  `Kind [Decision Principle Correction Clarification Constraint]`.
- `(…)` declares struct fields, for example `Topic (String)` and
  `Entry (Topic Kind Summary Context Magnitude Quote)`.
- `(Path …)` remains the import form.

`signal-frame@8dc8acf40f29` now parses that file-body grammar directly. The
parser expects `<component>.schema` first and falls back to `schema.nota` only
for compatibility. It rejects repeated self-keys inside struct declarations and
rejects trailing top-level schema tokens.

`signal-persona-spirit@655cc6fb2b4e` now uses `spirit.schema`; the previous
current `schema.nota` was removed. The historical v0.1.0 schema remains under
`schemas/v0.1.0/schema.nota` for migration witnesses. The local Magnitude
schema snapshot moved to `schemas/signal-sema/magnitude.schema`. The flake
source filter now includes `.schema` files, which was necessary for Nix builds.

`persona-spirit@95be1d3c9bcd` is a lock-only consumer update to the new signal
contract and new `signal-frame` parser.

## Follow-up after /326-v6

Designer `/326-v6` adds the deeper mechanism behind the syntax: the schema file
is short syntax lowered by a recursive executer into a fully specified
intermediate representation. The parser is not just recognizing surface forms;
it is assembling schema object nodes by context.

The actionable implementation landed in `signal-frame@f7c032854250`:

- Namespace value position accepts a bare PascalCase identifier as an
  alias/reference declaration, for example `WorkspaceTopic Topic`.
- Alias declarations resolve against the assembled namespace and imports.
- Unknown alias targets are rejected with a typed parser error.
- The emitted `SchemaDefinition` carries an `alias` field.
- Short-header slot emission follows aliases before deciding whether the target
  is a leaf enum, struct-like declaration, mixed enum, primitive, or container.

This is still an MVP IR. It does not yet assign stable UID-prefixed
workspace-wide identities to every type, and it does not yet expose the
schema-lowering executer as a reusable library for other custom languages. The
current commit makes the fourth namespace value form real without using it in
Spirit's schema, matching `/326-v6`'s statement that aliases are valid but rare
for the pilot.

`signal-persona-spirit@bfea608bee9b` and `persona-spirit@08b04c73bf60` are
consumer lock bumps proving the real Spirit pilot still compiles and tests
against the alias-aware parser.

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
`signal-persona-spirit@a66c87484109`.

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
7. Observable event payloads are still not emitted from the schema namespace.
   They remain macro-injected/hand-written until the observable surface becomes
   a first-class schema product.

## Operator recommendation

Treat this as the first runnable proof, not as closure of
`primary-ezqx.1`. The next operator pass should continue in this order:

1. Make schema-derived payload type emission real for the Spirit contract.
2. Make the version projection derive from the old/current schema pair.
3. Wire the production daemon's operation execution through the generated
   dispatch trait once the trait's shape survives review.
4. Replace generated NOTA codec internals with box-form calls for unsized
   fields.
5. Add the hard-handover offline-test marker and Nix witness.
6. Revisit whether `nota-codec::box_form` should remain there or be split
   once the `nota` repo's spec-only boundary changes.
