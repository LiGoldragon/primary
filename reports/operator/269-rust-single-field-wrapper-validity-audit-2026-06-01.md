# Rust Single-Field Wrapper Validity Audit

*Kind: audit · Topics: rust-craft, nota-next, derive, wrapper-types · 2026-06-01 · operator lane*

## Question

The prompt pointed at `nota-next/derive/src/lib.rs`:

```rust
struct CodecDerive {
    input: DeriveInput,
}
```

and asked why this exists instead of using `DeriveInput` directly.

The broader audit question: when is a single-field struct valid, and
when is it just a useless wrapper around an inner type?

## Verdict

`CodecDerive` is valid.

The reason is Rust method ownership. `DeriveInput` is a `syn` type, so
`nota-next` cannot add inherent methods to it. The expansion verbs
`expand_decode`, `expand_encode`, and `expand` need a local data-bearing
noun. The alternatives are worse:

- free functions like `expand_decode(input: DeriveInput)` violate the
  workspace method-only discipline;
- an extension trait on `DeriveInput` would be a one-impl trait, which is
  another indirection without a real abstraction;
- a zero-sized method holder would be a disguised free-function namespace.

`CodecDerive` is therefore not a transparent domain newtype; it is a
local adapter/workflow noun around an external syntax tree. It owns the
derive-expansion workflow.

## Why the Inner Type Is Not Enough

The inner type can be enough only when the logic can live on it.

Here it cannot. `syn::DeriveInput` is owned by `syn`, and Rust forbids
writing:

```rust
impl DeriveInput {
    fn expand_decode(self) -> TokenStreamTwo { ... }
}
```

because both the type and the inherent impl target are external to
`nota-next`. That leaves three local choices:

```rust
fn expand_decode(input: DeriveInput) -> TokenStreamTwo
```

This compiles, but it is orphan logic. It puts the verb outside a noun.

```rust
trait DeriveInputCodecExt {
    fn expand_decode(self) -> TokenStreamTwo;
}
```

This also compiles, but it creates a one-impl trait just to host methods.
That is the pattern designer 445 already flagged elsewhere.

```rust
struct CodecDerive {
    input: DeriveInput,
}
```

This is the cleanest local owner. It makes the operation explicit:
"this is a derive expansion over a parsed derive input."

## Named Field Versus Tuple Field

`struct CodecDerive(DeriveInput);` would also compile, but the named
field is better here.

The methods read several parts of the syntax tree:

```rust
self.input.attrs
self.input.ident
self.input.generics
self.input.data
```

The name `input` keeps those reads clear. A tuple field would turn that
into `self.0.attrs` and `self.0.data`, which is mechanically shorter but
semantically poorer. Tuple newtypes are best when the wrapper is
transparent domain value shape, such as `Name(String)`. `CodecDerive`
is not that; it is a workflow object.

## Validity Test

A single-field struct is valid when at least one of these is true:

1. It gives a primitive or external type a domain meaning and invariant.
   Example: `Name(String)` in `schema-next`.
2. It creates a local method owner for an external type. Example:
   `CodecDerive { input: DeriveInput }`.
3. It wraps a collection with validation, dispatch, formatting, or
   matching behavior. Examples: `Pattern { elements }`,
   `MacroRegistry { nodes }`, `NotaBodyEncoding { fields }`.
4. It owns IO/error context around a value or path. Examples:
   `AsschemaArtifact { asschema }`, `CheckedInAsschemaArtifact { path }`.
5. It encodes a runtime phase or typestate. Examples:
   `BeingProcessed { sema_input }`, `Processed { output }`.

A single-field struct is invalid when it has no identity beyond "the
inner thing," exposes only pass-through accessors, carries no invariant,
and owns no meaningful methods. In that case, use the inner type.

## Audit Results

### Valid

`nota-next/derive/src/lib.rs`:

- `CodecDerive { input: DeriveInput }` — valid external-type workflow
  owner.
- `ContainerNotaAttributes { known_root: bool }` — valid attribute
  accumulator; the single boolean is not "just a boolean" in context, it
  is parsed container state.
- `FieldNotaAttributes { name: Option<LitStr> }` — valid attribute
  accumulator with parsing behavior.

`nota-next/src`:

- `Pattern { elements }` — valid collection wrapper with match behavior.
- `MacroRegistry { nodes }` — valid collection wrapper with conflict
  validation and dispatch behavior.
- `NotaBodyEncoding { fields }` — valid encoding body noun.
- `StructureHeader { slots }` and `StructureHeaderBuilder { slots }` —
  valid packed-structure and builder nouns.
- `AtomCharacter { character }` — valid local method owner around a
  primitive character; `char` is external/primitive and cannot carry
  workspace methods.

`schema-next/src`:

- `MacroLibrary { source_entries }` — valid after the recent cleanup:
  one serializable macro-library noun.
- `MacroPattern { object }` and `MacroTemplate { object }` — valid after
  the recent cleanup: serializable behavior-bearing nouns, not `Data`
  mirrors.
- `AsschemaArtifact { asschema }` and `MacroLibraryArtifact { library }`
  — valid artifact IO wrappers.
- `SchemaEngine { registry }` — valid engine object; the registry is the
  state it runs with.

`schema-rust-next/src`:

- `RustCode(String)` — valid domain newtype for rendered Rust source.
- `RustImport { use_item }` — valid target-language emission noun.
- `RustModulePath { schema_name }` — valid mapping object from schema
  identity to emitted path.

`spirit-next/src`:

- generated tuple newtypes such as `Topic(pub String)` and
  `RecordIdentifier(pub Integer)` — valid domain values.
- `BeingProcessed { sema_input }` / `Processed { output }` — valid
  typestate phase values.
- `Daemon { configuration }` — valid runtime owner.
- `SpiritNextCli { arguments }` and `SpiritNextDaemonCli { arguments }`
  — valid argument readers, though a future NOTA source helper should
  shrink this code.

### Adjacent Invalid Pattern

`nota-next/derive/src/lib.rs` has:

```rust
struct FieldEncode;
```

This is not a single-field wrapper; it is worse. It is a zero-sized method
holder with one associated function:

```rust
impl FieldEncode {
    fn body_named(field: &Field) -> Result<TokenStreamTwo, Error> { ... }
}
```

The valid shape mirrors `FieldDecode`:

```rust
struct FieldEncode<'field> {
    field: &'field Field,
}
```

then:

```rust
impl<'field> FieldEncode<'field> {
    fn new(field: &'field Field) -> Self { ... }
    fn body_named(&self) -> Result<TokenStreamTwo, Error> { ... }
}
```

That would make encode and decode symmetric: both are real field-level
workflow objects. This is a better cleanup target than removing
`CodecDerive`.

## Rule Of Thumb

The question is not "does this struct have one field?" The question is:
what new noun did this type create?

If the noun is a domain value, phase, artifact owner, collection with
invariants, or local workflow owner for an external type, the wrapper is
valid. If the noun only renames the inner value and pushes accessors
around, it is invalid.

`CodecDerive` creates a real noun: a derive-expansion workflow over a
`syn::DeriveInput`. Keep it.
