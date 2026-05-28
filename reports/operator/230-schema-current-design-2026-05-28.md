# 230 - Schema Current Design

Date: 2026-05-28  
Lane: operator  
Component: schema / `schema-next`

## Current Rule

Every `.schema` file is legal NOTA first. The schema layer reads NOTA blocks
against an expected root type and lowers them into typed in-memory `Asschema`
data. Checked-in assembled-schema text fixtures and the old vector-record
assembled syntax are retired.

The root object is known from load context. A raw core schema file can be named
from its file path, just like a Rust module. A reactive schema uses positional
root fields; it does not write labels for fields already known by the expected
root type.

## Authored Syntax

The current large fixture shape is:

```nota
((Record Entry)
 (Correct Correction)
 Reindex)
((Recorded RecordReceipt)
 (Rejected Rejection))
{
  Topic [Text]
  Topics [(Vec Topic)]
  Kind (Decision Principle Correction Clarification)
  Query [Topics (kinds (Vec Kind)) (limit (Optional Integer))]
  RecordSet [(records (Vec Entry)) (byTopic (Map (Topic RecordIdentifier)))]
  Rejection [RejectionReason Description]
}
```

The three root objects are:

1. input enum body, known by position
2. output enum body, known by position
3. namespace map, known by position

Inside the namespace, braces are a native key/value map:

```nota
Topic [Text]
Kind (Decision Principle Correction)
Entry [Topics Kind Description Magnitude]
```

The declaration body is structural:

- `[Text]` is a newtype/one-field struct declaration.
- `[Topics Kind Description]` is a struct field list.
- `(Decision Principle Correction)` is an enum declaration body.
- `(Record Entry)` is a data-carrying variant.
- `Rejected` is a unit variant.

Type-reference positions use typed NOTA datatype objects:

```nota
(Vec Kind)
(Map (Topic RecordIdentifier))
(Optional Integer)
```

These lower to `Vector`, `Map`, and `Optional` references. Square brackets are
still raw NOTA vector structure and schema struct field lists; they are not the
surface syntax for declaring a `Vec` type.

## Raw Core Schema

`schema-next/tests/fixtures/raw-core/core.schema` proves the pre-lowering
surface. It is a real `.schema` file whose root is one native brace map. The
file stem supplies the root struct name:

```text
core.schema -> Core
```

The raw reader preserves NOTA delimiter objects:

```nota
{
  RawDatatype (| RawDatatype RawAtom RawText RawRecord RawVector RawKeyValue |)
  RawDatatypeList [(Vec RawDatatype)]
  RawDatatypeMap { key Name value RawDatatype }
  OptionalTopic (Optional Topic)
}
```

That layer is intentionally not `Asschema`; it is raw NOTA datatype data that
can bootstrap the schema reader.

## Code Witness

`schema-next/src/asschema.rs` lowers type references from NOTA blocks:

```rust
match block {
    Block::Atom(_) => Ok(Self::Plain(block.schema_name()?)),
    Block::Delimited { delimiter: Delimiter::Parenthesis, root_objects, .. } => {
        Self::from_parenthesis_objects(block, root_objects, registry, context)
    }
    _ => Err(SchemaError::ExpectedSymbol { found: block.reemit_fallback() }),
}
```

The old built-in collection macro calls were removed from the default macro
registry. User-declared type-reference macros can still be registered and
dispatched through the registry at type-reference positions.

The new `SyntaxSchema` layer sits under this macro engine. It reads a real
`.schema` through `RawSchemaFile`, then turns raw datatype objects into typed
syntax declarations. It has tests proving that `[String]` at declaration
position is a struct/newtype field list, while `(Vec Topic)` is the vector
type reference.

## Current Proof

Commands passed in `/git/github.com/LiGoldragon/schema-next`:

```sh
cargo fmt && cargo test
nix flake check --print-build-logs
```

Commit `206ef8f3` (schema fixture cleanup) removed checked-in assembled-schema
text fixtures. Commit `0c148f99` was the temporary native-collection pass; the
current branch supersedes its `[T]` vector-reference rule with typed NOTA
objects such as `(Vec T)`.
