# Per-instance schema — landed, data+decoder-driven, end to end

*schema-designer · report 9 · the implementation of the per-instance schema
("the schema of any value") from reports 6 and 8, built decoder-driven across
nota-next, schema-next, schema-rust-next, and signal-spirit on the
`instance-schema` designer branches. All four branches pushed; `main` and the
sibling lanes (`schema-help`, `help-codec`) untouched.*

## What landed

The per-instance schema is now produced by the **decoder** as it validates a
value, and rendered through **schema-next's encoder**. No hand-written decoder,
parser, value walk, or schema printer — the hard constraint held.

| layer | repo | what |
|---|---|---|
| capture | nota-next | `NotaDecodeTraced` trait + derive; `InstanceSchema` data model |
| capture (optional-leaf) | schema-rust-next | emit `NotaDecodeTraced` for the generated contract, including the hand-emitted `Domain` taxonomy decoders |
| render | schema-next | `InstanceSchemaText` — project the trace, render every reference token through the schema encoder |
| proof | signal-spirit | decode REAL `Input`/`Entry`/`Domain` values; assert endorsed forms |

## How it is decoder-driven (the constraint)

`NotaDecode`'s `from_nota_block` is already a type-directed traversal of a value
against a type. `NotaDecodeTraced::from_nota_block_traced` runs the *same*
traversal and additionally records, at each step, the `expected` reference the
decoder used:

- **struct** — walk fields in declared order, each field's traced decode
  contributing its node; body `Struct(fields)`.
- **newtype** — decode the inner traced; body `Newtype(inner)`, expected = wrapper.
- **enum** — read the variant tag from the value *only* to pick the payload
  decoder; the schema token stays the enum name; body `EnumPayload(payload?)`.
- **containers** — `Vec`/`Option`/`BTreeMap` reuse the existing block traversal
  (`NotaCollection`), so an empty container still knows its element type.
- **optional-leaf enums** (`Domain`/`Technology`/`Software`) — these are
  hand-emitted by schema-rust-next, not the derive, so the emitter was extended
  in lockstep: `RustOptionalEnumNotaTokens::traced_tokens` mirrors the hand
  `NotaBodyDecode` exactly, recording an `Optional` body (`None` for a bare
  variant atom, `Some(leaf)` for `(Variant Leaf)`).

The trace is a by-product of the validating recursion: one decode pass returns
`(value, InstanceSchema)`.

## The model as landed

```
DecodedWithSchema<T> { value: T, schema: InstanceSchema }
InstanceSchema { expected: TypeReference, provenance: Option<TypeReference>, body }
body = Scalar | Newtype(Box) | Struct(Vec) | EnumPayload(Option<Box>)
     | Vector(Vec) | Optional(Option<Box>) | Map(Vec<(_, _)>)
```

`expected` is a nota-next-local `TypeReference` (the type's own name plus the
container forms `Vector`/`Optional`/`Map`/`FixedBytes`). nota-next is the base of
the dependency chain and cannot depend on schema-next, so `SourceReference`
itself cannot live there. schema-next lifts `TypeReference -> SourceReference`
(`SourceReference::from_instance_reference`) and renders.

## Rendering — two projections, both through the encoder

`InstanceSchemaText` offers `aligned()` (one reference token per position) and
`expanded()` (recurse all the way down). Every reference token is produced by
`SourceReference::rendered_schema_text` (a new public wrapper over the encoder's
private `to_schema_text`); the renderer only chooses delimiters. At an
enum-payload position both projections collapse the variant's transparent
payload wrapper to provenance (`Partial` -> its `DomainScopes` payload;
`Record`/`RecordRequest` -> the field paren group).

## Endorsed forms — asserted verbatim over the REAL contract

All from `signal-spirit/tests/instance_schema.rs`, decoding real values:

| value | rendered per-instance schema |
|---|---|
| `Decision` (a `Kind`) | `Kind` |
| `Entry` value | `{ Domains Kind Description Certainty Importance Privacy Referents }` |
| `DomainMatch::Partial([...])` | `(DomainMatch DomainScopes)` |
| `Certainty(High)` | `(Certainty Magnitude)` |
| empty `Domains` (`[]`) | aligned `Domains`; expanded `(Domains (Vector Domain))` |
| root `(Record (...))` | `(Input ({ Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning }))` |

The `Domain` taxonomy traces expected types `Domain -> Technology -> Software ->
(Optional ProgrammingLeaf)` with the realized `ProgrammingLeaf` one level in.

## One honest deviation from the report prose

The reports wrote vectors as `(Vec Domain)`. schema-next's encoder canonically
emits `(Vector X)`, so the rendered container reads `(Vector Domain)`. Rendering
through the encoder is the binding constraint; emitting `(Vec ...)` would have
required a hand printer and violated it. The tests assert `(Vector Domain)` and
round-trip it through `SourceReference::from_block`. If `Vec` is the desired
surface spelling, that is a one-line change to schema-next's encoder head, not
to this trace machinery.

## Cross-repo pins (for the operator integration)

Each branch pins its upstreams to the sibling `instance-schema` branches.
signal-spirit additionally needs `[patch]` entries: a branch-only patch is
rejected by cargo as "the same source," so the patches point at the local
`~/wt/.../instance-schema` worktree paths to redirect the transitive
signal-frame/version-projection trees onto one nota-next/schema-next version.
An operator merging to main removes those path patches.

## Test status (real `cargo test`)

- nota-next: 8 instance-schema tests + full suite green.
- schema-next: 6 render tests + full suite (247) green.
- schema-rust-next: full suite green after regenerating fixtures/snapshots;
  daemon-default build clean.
- signal-spirit: 10 real-contract tests + full nota-text suite (28) green;
  daemon-default (no `nota-text`) build clean; the dependency-boundary gate test
  still passes.
