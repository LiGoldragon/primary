---
variant: Implementation
topics: [schema, asschema, emission, spirit, trace, newtype]
date: 2026-06-03
lane: operator
---

# Schema Newtype And Trace Cleanup

## Intent

This slice implements two fresh psyche corrections:

- [Single-field schema declarations without an explicit field name should lower and emit as newtypes, not named one-field structs. A PascalCase self-named field or single referenced type is a semantic type object; only multi-field structs derive lowercase field names. Generated Rust and NOTA should preserve this by using transparent newtypes so trace events like ObjectName do not become double-delimited one-field records.]
- [Schema source needs its own typed node model before assembled schema: a streamlined data tree of typed structural-macro nodes, namespaces, paths, fields, variants, and references. The source model should represent schema syntax directly and deterministically, including inline PascalCase local type declarations and self-named field shorthand, before lowering into assembled schema and Rust emission.]

The concrete bug was `TraceEvent`:

```nota
((Sema WriteApplied))
```

That shape said "a trace event is a one-field record containing an object
name." The intended object is just the activated object name:

```nota
(Sema WriteApplied)
```

## What Changed

### schema-next

Commit `f76e53f3` (`schema-next: lower single-field structs as newtypes`).

The struct-body decision now has one owner:

```rust
AssembledStructBody::lower_type(...)
```

It lowers fields first, then chooses the assembled type:

```rust
if fields.len() == 1 {
    TypeDeclaration::Newtype(NewtypeDeclaration::new(name, reference))
} else {
    TypeDeclaration::Struct(StructDeclaration::new(name, fields))
}
```

That rule is used for:

- macro-expanded assembled `Struct` templates;
- authored namespace brace declarations such as `Entry { Topic * }`;
- inline PascalCase declarations inside struct bodies.

`schemas/core.asschema` refreshed accordingly. One-field collection wrappers
in the core macro schema now become newtypes, for example:

```nota
(Public MacroPatternObjects (Newtype (MacroPatternObjects (Vector (Plain MacroPatternObject)))))
```

not:

```nota
(Public MacroPatternObjects (Struct (MacroPatternObjects {values (Vector (Plain MacroPatternObject))})))
```

New tests pin both source paths:

- `single_field_brace_declarations_lower_to_newtypes`
- `single_field_inline_pascal_declarations_lower_to_newtypes`

### schema-rust-next

Commit `cf1ed383` (`schema-rust: emit trace events as transparent newtypes`).

Generated trace support now emits:

```rust
pub struct TraceEvent(pub ObjectName);

impl TraceEvent {
    pub fn new(object_name: ObjectName) -> Self {
        Self(object_name)
    }

    pub fn object_name(&self) -> ObjectName {
        self.0
    }

    pub fn name(&self) -> &'static str {
        self.0.name()
    }
}
```

The emitted source test now asserts both the Rust shape and the NOTA behavior:

```rust
assert_eq!(
    generated::NotaEncode::to_nota(&event),
    "(Signal (Input Record))"
);
```

Generated fixtures were refreshed through the existing fixture update
mechanism.

### spirit-next

Commit `4e8ebc22` (`spirit-next: refresh trace event newtype generation`).

`Cargo.lock` now points at:

- `schema-next` `f76e53f3`;
- `schema-rust-next` `cf1ed383`.

Checked-in generated `src/schema/lib.rs` now carries:

```rust
pub struct TraceEvent(pub ObjectName);
```

The trace runtime test now checks the client-facing NOTA shape:

```rust
let rendered = events[3].to_string();
assert_eq!(rendered, "(Sema WriteApplied)");
let parsed = rendered.parse::<TraceEvent>()?;
assert_eq!(parsed, events[3]);
```

That proves the trace line is generated NOTA for the trace noun and not a
hand-written string log.

## Verification

Passed:

- `schema-next`: `cargo test`
- `schema-next` touched files: `rustfmt --check src/declarative.rs src/engine.rs tests/lowering.rs`
- `schema-rust-next`: `cargo test`
- `schema-rust-next`: `cargo fmt --check`
- `spirit-next`: `SPIRIT_NEXT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text,testing-trace`
- `spirit-next`: `cargo test --features nota-text,testing-trace --test instrumentation_logging`
- `spirit-next`: `cargo test --features nota-text,testing-trace --test process_boundary cli_receives_testing_trace_events_from_daemon_trace_socket -- --exact`
- `spirit-next`: `cargo test --features nota-text,testing-trace`
- `spirit-next`: `cargo test --no-default-features`

Known formatting note:

`schema-next cargo fmt --check` still reports pre-existing formatting drift in
unrelated upgrade-pilot files (`src/store.rs`, `src/upgrade.rs`,
`tests/upgrade_pilot.rs`). I did not churn those files in this slice. The
files touched here pass rustfmt directly.

## Audit Finding

The immediate newtype rule is now implemented, but the deeper source-model
gap is real.

Today schema-next still has several adjacent layers that describe similar
ideas with different nouns:

- raw NOTA source reading (`raw.rs`);
- typed syntax reading (`syntax.rs`);
- declarative macro expansion (`declarative.rs`);
- assembled schema (`asschema.rs`);
- schema engine dispatch (`engine.rs`).

That is not wrong as a bootstrap, but it is where "guessing" creeps in. The
single-field newtype rule is now centralized for struct-body lowering, but
the system still does not have one typed source node tree that says:

```rust
enum SchemaSourceNode {
    NamespaceDeclaration(SourceDeclaration),
    StructField(SourceField),
    EnumVariant(SourceVariant),
    TypeReference(SourceReference),
    MacroInvocation(SourceMacroInvocation),
}
```

The next elegant consolidation is not another emitter patch. It is a typed
schema-source layer before `Asschema`:

- read strict NOTA into source nodes;
- attach macro-position meaning to those nodes;
- preserve whether a field came from explicit `field Type`, derived `Type *`,
  inline `Type { ... }`, or composite `(Vec Type)`;
- lower those typed source nodes into `Asschema`.

That would make decisions like "one field means newtype" and "multi-field
means struct" visible in the source tree instead of rediscovered from lowered
fields. It also gives the macro system a cleaner place to become schema data
without duplicating source/artifact enums.

## Current State

The working API is clean after this slice:

- authored schema one-field bodies lower to asschema newtypes;
- asschema newtypes emit Rust tuple newtypes;
- generated trace events are transparent newtypes over generated object names;
- CLI trace display now shows one generated NOTA object;
- daemon binary-only tests still prove `nota-next` is absent from the
  no-default runtime surface.

The remaining design work is source-node agglomeration, not more ad hoc
single-case handling.
