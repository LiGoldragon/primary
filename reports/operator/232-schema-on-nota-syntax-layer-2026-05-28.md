# 232 - Schema on the NOTA Syntax Layer

Date: 2026-05-28  
Lane: operator  
Repos touched: `schema-next`, `schema-rust-next`

## What Landed

The new boundary is implemented as code, not only as prose:

```text
.schema text
  -> nota-next delimiter parse
  -> RawSchemaFile / RawNotaDatatype
  -> SyntaxSchema / SyntaxDeclaration / SyntaxReference
  -> Asschema lowering
  -> schema-rust-next emitted Rust
```

The important correction is now enforced: square brackets are raw NOTA vector
structure and schema field-list structure. They are not the `Vec` type
constructor. A vector type reference is a typed NOTA datatype object:

```nota
(Vec Topic)
(Map (Topic RecordIdentifier))
(Optional Topic)
```

## Real Schema Example

Fixture:

```text
/git/github.com/LiGoldragon/schema-next/tests/fixtures/syntax-layer/schema.schema
```

```nota
{
  Text [String]
  Identifier [Integer]
  Topic {| Topic text Text |}
  Topics {| Topics values (Vec Topic) |}
  TopicIndex {| TopicIndex entries (Map (Topic Identifier)) |}
  Kind (| Kind Decision Principle Correction Clarification Constraint |)
  Entry {| Entry topics Topics kind Kind description Text related TopicIndex maybeTopic (Optional Topic) |}
  RecordQuery {| RecordQuery topics (Vec Topic) maximumCount Integer |}
  RecordReply {| RecordReply entries (Vec Entry) |}
  SpiritInput (| SpiritInput (Record Entry) (Observe RecordQuery) Ping |)
  SpiritOutput (| SpiritOutput (Recorded Identifier) (Observed RecordReply) Pong |)
}
```

What the syntax layer reads:

```text
Text
  Struct Text
    string: Plain(String)

Topics
  Struct Topics
    values: Vector(Plain(Topic))

TopicIndex
  Struct TopicIndex
    entries: Map(Plain(Topic), Plain(Identifier))

Kind
  Enum Kind
    Decision
    Principle
    Correction
    Clarification
    Constraint

SpiritInput
  Enum SpiritInput
    Record(Plain(Entry))
    Observe(Plain(RecordQuery))
    Ping
```

Tests assert these data objects directly in:

```text
/git/github.com/LiGoldragon/schema-next/tests/syntax_layer.rs
```

## How Schema Sits on NOTA

NOTA supplies structural objects:

```text
Atom
Text
Record / parenthesis
Vector / square bracket
KeyValue / brace
PipeParenthesis
PipeBrace
```

Schema supplies expected-type reading over those objects:

```text
raw [String] at datatype declaration position
  -> struct/newtype field list

raw (Vec Topic) at type-reference position
  -> TypeReference::Vector(Plain(Topic))

raw {| Topic text Text |}
  -> self-named struct declaration

raw (| Kind Decision Constraint |)
  -> self-named enum declaration
```

This is the composability layer: NOTA keeps the syntax unambiguous and
quote-free; schema gives positions and nodes a programmable meaning.

## Rust Emission Proof

`schema-rust-next` now consumes `schema-next` commit `31497c9d` and its fixtures
use the typed composite syntax. Generated Rust still emits normal Rust types:

```text
(Vec Topic) -> Vec<Topic>
(Map (Topic RecordIdentifier)) -> std::collections::BTreeMap<Topic, RecordIdentifier>
(Optional Topic) -> Option<Topic>
```

The generated NOTA value syntax remains structural:

```nota
[[schema]]
```

That is a vector value containing one string-newtype value. The outer brackets
are the vector; the inner brackets are the `Topic` string value. The tests now
expect this normalized output.

## Constraints Added

`schema-next` now rejects old reference syntax:

```nota
[[Service]]
{NodeName NodeProposal}
```

at type-reference positions. The tests assert typed errors:

```text
UnknownTypeReferenceForm { head: "SquareBracket", argument_count: 1 }
UnknownTypeReferenceForm { head: "Brace", argument_count: 2 }
```

Both repos also have Nix guards against bringing the old examples back.

## Current Gaps

`SyntaxSchema` proves the raw-NOTA-to-schema layer, but it does not yet replace
the older macro engine end to end. The macro registry is still partly
code-defined. The next hardening pass is to load macro definitions as schema
data first, assemble them, then use the assembled macro table to read later
schema files.

The import system has the current `ImportResolver` and single-colon paths, but
the richer import variants from the new intent are not all implemented yet:
import-all, import-some, adjacent path, repository-root path, and git source
should become typed import variants rather than ad hoc resolver options.

## Verification

Passed:

```sh
cd /git/github.com/LiGoldragon/schema-next && cargo test
cd /git/github.com/LiGoldragon/schema-next && nix flake check --print-build-logs
cd /git/github.com/LiGoldragon/schema-rust-next && cargo test
cd /git/github.com/LiGoldragon/schema-rust-next && nix flake check --print-build-logs
```
