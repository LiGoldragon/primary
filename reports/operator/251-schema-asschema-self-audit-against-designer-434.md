# 251 — Schema Asschema Self-Audit Against Designer 434

*Kind: Audit · Topics: schema, asschema, emission, bootstrap, everything-is-data · 2026-05-30 · operator lane*

## Verdict

Designer 434 is the right architectural frame. My subsequent operator pass
closed a real part of it — `Asschema` now round-trips through NOTA text and
rkyv bytes — but I should be more precise about what is and is not closed.

The current implementation is **stage 2 mostly done**, **stage 3 partial**,
and **stages 4-5 open**:

- Stage 2, "assembled schema is serializable data": mostly done for the
  assembled type table.
- Stage 3, "emitter reads the serialized artifact": only partially done.
  `spirit-next/build.rs` forces a NOTA+rkyv round trip before emission, but no
  durable `.asschema` artifact is written/read as the emitter's first-class
  input.
- Stage 4, "schema authoring is a macro to assembled-schema data": still
  partial. The authoring language lowers to `Asschema`, but the macro table
  itself is not yet loaded from typed serialized macro data.
- Stage 5, self-hosting schema-of-schema loop closure: not started.

The implementation moved the substrate in the correct direction. It did not
complete designer 434's full "serialized assembled form is the emitter source"
architecture.

## Claim Check

### Stage 1 — Core assembled schema Rust types

Status: **closed before this audit**.

The assembled schema type model exists in `schema-next`:

- `Asschema`
- `Declaration`
- `RootDeclaration`
- `TypeDeclaration`
- `StructDeclaration`
- `EnumDeclaration`
- `NewtypeDeclaration`
- `TypeReference`
- `StructFieldMap`

These are the Rust bootstrap types for the assembled schema. Designer 434
called this already done, and that remains true.

### Stage 2 — Asschema as NOTA + rkyv data

Status: **mostly closed, with two caveats**.

Evidence:

- `/git/github.com/LiGoldragon/schema-next/src/asschema.rs` gives
  `Asschema::from_nota_source`, `Asschema::to_nota`,
  `Asschema::from_binary_bytes`, and `Asschema::to_binary_bytes`.
- `/git/github.com/LiGoldragon/schema-next/tests/asschema_definition.rs`
  proves a real lowered schema round-trips:

```rust
let nota = asschema.to_nota();
Document::parse(&nota).expect("emitted asschema is legal NOTA");
let from_nota = schema_next::Asschema::from_nota_source(&nota)?;
assert_eq!(from_nota, asschema);

let bytes = asschema.to_binary_bytes()?;
let from_binary = schema_next::Asschema::from_binary_bytes(&bytes)?;
assert_eq!(from_binary, asschema);
```

Caveat 1: this is generated-from-`.schema` NOTA, not a checked-in
`.asschema` fixture. The test proves the value can become legal NOTA and rkyv
and return. It does not yet prove a durable artifact file is the build input.

Caveat 2: the macro-node frontier is not fully rkyv data. `SchemaNode`,
`SchemaNodeData`, `SchemaNodeValue`, and `SchemaNodePair` derive NOTA codec
traits, but not rkyv traits. That is acceptable only if we state the boundary:
the assembled type table is live as NOTA+rkyv data; the macro table itself is
still not fully live binary data.

### Stage 3 — Emitter reads serialized assembled form

Status: **partial, and this is where my previous wording overstated the result**.

What is live:

- `/git/github.com/LiGoldragon/spirit-next/build.rs` lowers
  `schema/lib.schema`, calls `AsschemaArtifact::read_back`, serializes the
  value to NOTA, reads it back, serializes it to rkyv, reads it back, and only
  then emits Rust.
- `/git/github.com/LiGoldragon/schema-rust-next/tests/big_emission.rs` proves
  Rust emission is stable after the same NOTA+rkyv round trip.

Current pattern:

```rust
let asschema = SchemaEngine::default().lower_source(source, identity)?;
let read_back = AsschemaArtifact::new(asschema).read_back();
RustEmitter::default().emit(&read_back)
```

This is a good guard against emitter/lowerer private coupling. It proves the
emitter can survive the serialized data boundary.

What is still missing:

```rust
let artifact = AsschemaArtifact::read_nota_file("schema/lib.asschema")?;
RustEmitter::default().emit(&artifact.asschema())
```

or:

```rust
let artifact = AsschemaArtifact::read_binary_file("schema/lib.asschema.rkyv")?;
RustEmitter::default().emit(&artifact.asschema())
```

The architectural target is a first-class artifact API and file path. Today
`RustEmitter` still consumes `&Asschema`; the only serialized boundary is a
local build-script/test round trip. That is not yet the same as "the emitter
reads the serialized artifact."

### Stage 4 — Schema authoring language as macro to assembled data

Status: **partial**.

The authoring language does lower to `Asschema`. That part is real:

```text
.schema authoring syntax -> schema-next lowering -> Asschema
```

But the macro system is not yet itself fully loaded as typed assembled data:

```text
macro-table.asschema -> MacroTable -> schema expansion
```

The current code still has built-in/declarative lowering behavior. That is not
wrong for bootstrap, but it is not the final "everything is data" macro model.
Designer 434 is correct that macro-table-as-data remains a separate frontier.

### Stage 5 — Self-hosting loop closure

Status: **open**.

Nothing currently proves:

```text
Asschema's own schema -> Asschema artifact -> Rust emitted type model
```

or:

```text
short schema-of-schema syntax -> assembled schema-of-schema -> emitted Rust
```

The previous pass unblocked this direction by making `Asschema` serializable.
It did not close the loop.

## Canonical Text Shape Gap

Designer 434 shows the intended canonical assembled NOTA as:

```nota
(Public Topic (Newtype String))
(Public Entry (Struct { topics Topics kind Kind }))
```

The current derived codec emits a more derive-shaped form. The live test checks
for strings like:

```nota
(Public [Entry] (Struct ([Entry] ...)))
(Vector (Plain [Entry]))
```

That means the current `.to_nota()` surface is legal and round-trippable, but
it is not yet the final pretty/canonical `.asschema` notation designer 434
uses. This matters because `.asschema` is meant to be a human-inspectable
artifact, not just any parseable serialization.

This is not a blocker for stage 2's data-substrate proof. It is a blocker for
calling the `.asschema` text format aesthetically settled.

## Self-Correction

My report 250 used "artifact" too broadly. The precise statement is:

> The implementation proves `Asschema` can serialize to NOTA and rkyv and that
> Rust emission remains stable after reading those serialized forms back.

The precise statement is **not**:

> The build now writes and consumes a durable `.asschema` file as the source of
> Rust emission.

That second statement is still future work.

## Next Implementation Target

The next clean slice should make the serialized assembled schema a named
object, not just a local test/build-script trick.

1. Add an `AsschemaArtifact` or equivalent data-bearing type in
   `schema-next`, not only inside `spirit-next/build.rs`.
2. Give it methods for reading/writing NOTA and rkyv files:
   `read_nota_file`, `write_nota_file`, `read_binary_file`,
   `write_binary_file`.
3. Add `schema-rust-next` entry points that emit from the artifact path:
   `emit_from_nota_file` and `emit_from_binary_file`, or equivalent methods
   on the artifact object.
4. Add at least one checked-in `.asschema` fixture generated from a real
   `.schema`, then assert:
   `.schema -> Asschema -> .asschema` matches the fixture, and
   `.asschema -> RustEmitter` matches current generated Rust.
5. Decide whether the pretty canonical assembled notation in designer 434 is
   the target surface, then implement explicit codecs where derive output is
   too noisy.
6. Keep macro-table-as-data separate and explicit: the artifact slice should
   not hide the remaining macro frontier.

## Audit Summary

Designer 434 remains valid. Operator 250 advanced it, but did not supersede
it. The honest status is:

```text
schema source
  -> Asschema in memory
  -> NOTA/rkyv round-trip proof
  -> Asschema in memory
  -> Rust emission
```

The target status is:

```text
schema source
  -> durable .asschema / .asschema.rkyv artifact
  -> emitter reads artifact
  -> Rust emission
```

The next work should close exactly that gap.
