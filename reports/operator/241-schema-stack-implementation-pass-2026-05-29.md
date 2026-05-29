# Schema Stack Implementation Pass

Operator pass after `reports/designer/427-schema-stack-as-implemented-now.md`.

## Result

The main-stack pilot is materially more real now:

- `nota-next` owns the shared `NotaEncode` / `NotaDecode` traits and derive macros.
- `schema-next` exposes roots as assembled data and now proves macro-pattern/template shapes as typed data in `schemas/core.schema`.
- `schema-rust-next` emits Rust types that derive the shared NOTA codec instead of hand-writing per-type readers/writers.
- `spirit-next` runs a schema-derived Signal/Nexus/SEMA chain with multi-topic query, durable `.sema` database writes, removal, and Nix-built CLI/daemon integration tests.

## Commit Set

- `nota-next` `a0c39b75` — `nota: add codec derives`
- `nota-next` `6a487b6a` — `nota: document at-delimiter schema declaration target`
- `schema-next` `b98f5548` — `schema: prove structural macros as data`
- `schema-next` `f6e9117f` — `schema: document core macro data frontier`
- `schema-next` `2ccfdca6` — `schema: document at-delimiter declaration target`
- `schema-rust-next` `c758834e` — `schema-rust: keep generated codec bridges clippy-clean`
- `schema-rust-next` `963961c1` — `schema-rust: document authored syntax independence`
- `spirit-next` `75985c38` — `spirit: run schema-derived sema topic and removal flow`
- `spirit-next` `f4751e15` — `spirit: document schema syntax transition`

All four repo worktrees are clean after commit.

## Stack Shape

```mermaid
flowchart LR
    schema[.schema file] --> asschema[Asschema data]
    asschema --> rust[generated Rust types]
    rust --> signal[Signal engine]
    signal --> nexus[Nexus mail keeper]
    nexus --> sema[SEMA redb .sema store]
    sema --> nexus
    nexus --> signal
```

The important proof is that `spirit-next/schema/lib.schema` is no longer decorative. It emits `src/schema/lib.rs`; the runtime imports those emitted types; the tests drive the chain through those exact types.

## What Changed

### `nota-next`

The codec path exists in the base NOTA layer now:

```rust
#[derive(nota_next::NotaDecode, nota_next::NotaEncode)]
pub struct Entry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub magnitude: Magnitude,
}
```

The derive macros mean schema-generated Rust can depend on the same codec interface that hand-written Rust can use. That closes the split designer flagged: schema-generated readers no longer need a private parallel codec.

### `schema-next`

`Asschema` has roots as data now. The compatibility helpers `input()` and `output()` still exist, but the canonical shape is roots plus namespace.

`schemas/core.schema` now describes macro pattern/template payloads as typed object trees instead of opaque strings:

```schema
MacroPattern {| MacroPattern object MacroPatternObject |}
MacroPatternObject (| MacroPatternObject
  (Capture MacroCaptureName)
  (RestCapture MacroCaptureName)
  (Atom MacroAtom)
  (Delimited MacroPatternDelimited)
|)
```

The new test proves that lowering reads this as `TypeDeclaration` data, including `MacroPatternObject` and `MacroTemplateObject` enums.

### `schema-rust-next`

The generated source shrank because the emitter now emits derives and thin inherent bridges:

```rust
#[derive(nota_next::NotaDecode, nota_next::NotaEncode, rkyv::Archive, ...)]
pub enum Input {
    Record(Entry),
    Observe(Query),
    Remove(RecordIdentifier),
}
```

This removes the old bulk hand-written `impl NotaDecode` / `impl NotaEncode` generator path. The support nouns that are `Copy` still get inherent bridge methods, but those delegate to trait impls and stay clippy-clean.

### `spirit-next`

The schema now declares the three active languages:

```schema
((Record Entry) (Observe Query) (Remove RecordIdentifier))
((RecordAccepted SemaReceipt) (RecordsObserved ObservedRecords) (RecordRemoved RemoveReceipt) (Error ErrorReport) (Rejected SignalRejection))
{
  NexusInput (| NexusInput (Signal Input) (Sema SemaOutput) |)
  NexusOutput (| NexusOutput (Sema SemaInput) (Signal Output) |)
  SemaInput (| SemaInput (Record Entry) (Observe Query) (Remove RecordIdentifier) |)
  SemaOutput (| SemaOutput (Recorded SemaReceipt) (Observed ObservedRecords) (Removed RemoveReceipt) (Missed ErrorReport) |)
  TopicMatch (| TopicMatch (Partial Topics) (Full Topics) |)
}
```

The runtime follows that shape:

```mermaid
flowchart LR
    Input[Signal Input] --> Accepted[SignalAccepted]
    Accepted --> Sent[MessageSent hook]
    Sent --> Nexus[NexusInput::Signal]
    Nexus --> Command[NexusOutput::Sema]
    Command --> Store[SemaInput applied to .sema]
    Store --> Reply[SemaOutput]
    Reply --> Output[Signal Output]
```

SEMA now means database work concretely:

- `SemaInput::Record(Entry)` writes rkyv-archived entries to a redb-backed `.sema` file.
- `SemaInput::Observe(Query)` reads the `.sema` file and returns a typed `RecordSet`.
- `SemaInput::Remove(RecordIdentifier)` deletes from the `.sema` file and returns `RecordRemoved`.
- The commit sequence and state digest come from the durable store.

## Proof Commands

`nota-next`:

```sh
cargo test
NIX_CONFIG=$'builders =\nsubstituters =' nix flake check
```

`schema-next`:

```sh
cargo fmt && cargo test && NIX_CONFIG=$'builders =\nsubstituters =' nix flake check
```

`schema-rust-next`:

```sh
cargo fmt && cargo test && cargo clippy --all-targets -- -D warnings
NIX_CONFIG=$'builders =\nsubstituters =' nix flake check
```

`spirit-next`:

```sh
cargo test
./scripts/check-local-schema-stack --builders '' --option substituters ''
NIX_CONFIG=$'builders =\nsubstituters =' ./scripts/run-nix-integration-tests
```

All passed.

## What Is Proved Now

- Generated Rust is checked in and freshness-checked by `build.rs`.
- The old signal macro surface is fenced out by Nix checks.
- The current generated schema source uses shared NOTA derives.
- The runtime uses generated Signal, Nexus, and SEMA types directly.
- Nix-built `spirit-next` and `spirit-next-daemon` exchange real rkyv over a Unix socket.
- Integration tests assert typed `Output` values, not raw stdout strings.
- A daemon can write a `.sema` database, restart, and observe the prior record.
- Partial topic search is any-of; full topic search is all-of.
- Removal is part of the generated signal and SEMA language, not a side command.

## Remaining Gaps

### Rust emission is still string-rendered

The emitter no longer hand-writes codec implementations, but it still builds Rust source with `RustEmitter::line(...)`. The next structural upgrade is:

```mermaid
flowchart LR
    asschema[Asschema] --> module[RustModule data]
    module --> renderer[Renderer]
    renderer --> file[src/schema/lib.rs]
```

That would make the emitter itself obey the "everything is data" principle.

### Macro definitions are partly data, not fully load-bearing data

`core.schema` now has typed data structures for macro patterns/templates, but `schemas/builtin-macros.schema` still parses through the hand-written declarative macro reader. The macro definitions are serializable in spirit, but the runtime registry does not yet load a pre-assembled macro table from asschema data.

Precise next step: define the macro table as asschema data, emit its Rust type, then make the registry consume that type rather than bespoke parser structs.

### Macro trace vectors still exist

The load-bearing lowering tests no longer prove behavior by asserting `macros_applied` / `expanded_templates`, but `MacroContext` still stores trace vectors for macro exploration and custom macro tests. This is acceptable as diagnostic metadata, not as a proof substrate. If the design wants no trace side channel at all, delete those vectors and replace the exploration tests with output-data assertions.

### Support nouns are emitted locally, not imported from a shared core crate

`MessageIdentifier`, `OriginRoute`, `MessageSent`, `NexusMail`, `MessageProcessed`, and `DatabaseMarker` are generated into each emitted module today. The cleaner destination is a shared `schema-core` / signal-core schema imported cross-crate, so component schemas reuse those nouns rather than re-emitting local copies.

### Upgrade/diff is still not implemented

This pass made the schema-generated stack real enough for Spirit behavior, but it did not implement schema diffing, upgrade derivation, or versioned database migration.

## Delta Against Designer 427

Designer 427 was accurate when written, but two points are now stale:

- Spirit-next is no longer pending for the basic full-chain pilot; it runs generated Signal/Nexus/SEMA types through CLI, daemon, rkyv socket, and `.sema` store.
- The trace-cleanup is stronger: the main lowering proof now asserts asschema output data, not macro trace strings.

The main warnings in 427 still stand:

- the emitter should become data-shaped;
- the macro table should become fully loadable typed data;
- the shared support nouns should move to an imported schema core.

## Syntax Pivot After This Pass

After this implementation, designer captured records 1199 and 1202. Those
records turn the `Name@delimiter` declaration syntax into the new target
surface:

- `Name@{ ... }` as a visually explicit named struct-like declaration shape.
- `Name@( ... )` as a visually explicit named enum-like declaration shape.
- `name@Type`, `name@{...}`, and `name@(...)` as member bindings, recursively.
- the root schema object does not need `@` or delimiters because it is the
  known root struct whose name comes from the filename.

This replaces the pipe-family declaration target from record 1120. I did not
implement this in the code above. The current implementation remains
pipe-family declarations: `Name {| Name ... |}` and `Name (| Name ... |)`,
and that must now be read as transitional.

The assembled target stays first. The `@` surface must lower into the same
macro-free `Asschema` data rather than becoming a new emitter input or a
separate parser shortcut. Composite references such as `(Vec Entry)` still
resolve at type-reference positions; unnamed composites may derive names such
as `vec_of_entry` / `VecOfEntry` when there is no conflict.
