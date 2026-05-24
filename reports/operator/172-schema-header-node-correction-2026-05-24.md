# 172 - Schema header node correction, 2026-05-24

## Context

This report records the operator interpretation of the psyche's correction to
`reports/designer/326-v6-spirit-complete-schema-vision.md`.

Spirit records captured during this pass:

- 472 - schema headers are ordered enum-root declarations, not namespace
  vectors.
- 473 - `EnumIdentifier` is a schema-core constrained string type.
- 474 - header declarations contain an enum identifier plus ordered endpoint
  nodes.
- 475 - header endpoints are fast inbound dispatch triage points.
- 476 - the schema language should be specified by its own schema file.

## Corrected header model

The first section of `spirit.schema` is the working-signal header declaration
surface. It is not the local namespace. It is ordered, because it declares
enum-like header slots. It is not a map, because maps do not preserve the enum
slot order as directly as the schema needs.

The corrected Spirit working header is:

```nota
[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
  (Watch [Subscription])
  (Unwatch [SubscriptionToken])
]
```

Each record is a header enum node:

```nota
(<EnumIdentifier> [<EndpointIdentifier>])
```

`EnumIdentifier` is a core schema-language type: a PascalCase, unquoted,
string-like identifier. The schema implementation should enforce both
properties. The vector after it is the ordered endpoint-node vector. In this
MVP the parser accepts exactly one endpoint per operation header node and turns
it into the operation payload type.

The removed form was:

```nota
(Record (Entry (engine assert)))
```

That shape mixed two concerns. `Record` and `Entry` belong to the receiving
header tree. `Assert` belongs to the downstream Sema classification and
observation vocabulary, not to the first header dispatch syntax.

## Why The Header Exists

The header is the receive-side triage table. It lets an ingress path choose the
next action before reading or decoding the whole message body. The first action
can be "drop", "log the header and drop", "keep reading", "route to this actor
path", or a runtime-state-dependent decision once the database-backed ingress
policy exists.

That makes the header a receiving/dispatch object, not an execution object. It
selects the path that may eventually lower a payload to component-local
commands and then to Sema classification observations.

## Schema-Schema Sketch

The core schema language should eventually define itself as a `.schema` file.
The example below is illustrative, not accepted by today's parser. Its purpose
is to show the target objects that the core library needs to name.

```nota
[]

[]

[]

{}

{
  SchemaFile
    (SignalHeader OwnerHeader SemaHeader ImportNamespace LocalNamespace FeatureVector)

  SignalHeader ([Vec HeaderEnumNode])
  OwnerHeader ([Vec HeaderEnumNode])
  SemaHeader ([Vec HeaderEnumNode])

  HeaderEnumNode (EnumIdentifier [Vec HeaderEndpointNode])
  HeaderEndpointNode (EnumIdentifier)

  ImportNamespace ([Vec ImportBinding])
  ImportBinding (TypeIdentifier Path)

  LocalNamespace ([Vec TypeBinding])
  TypeBinding (TypeIdentifier SchemaNode)

  FeatureVector ([Vec FeatureNode])

  SchemaNode
    [EnumNode StructNode NewtypeNode PathNode ReferenceNode PrimitiveNode ContainerNode]

  EnumNode ([Vec EnumVariantNode])
  EnumVariantNode [UnitVariant DataVariant]
  UnitVariant (EnumIdentifier)
  DataVariant (EnumIdentifier TypeReference)

  StructNode ([Vec TypeReference])
  NewtypeNode (TypeReference)
  PathNode (Path)
  ReferenceNode (TypeIdentifier)
  PrimitiveNode (PrimitiveIdentifier)
  ContainerNode (ContainerIdentifier TypeReference)

  TypeReference [NamedType ContainerType PrimitiveType]
  NamedType (TypeIdentifier)
  ContainerType (ContainerIdentifier TypeReference)
  PrimitiveType (PrimitiveIdentifier)

  EnumIdentifier (PascalCaseUnquotedString)
  TypeIdentifier (PascalCaseUnquotedString)
  PrimitiveIdentifier (PrimitiveNameString)
  ContainerIdentifier [Vec Option]
  PascalCaseUnquotedString (String)
  PrimitiveNameString (String)
}

[]
```

The important point is not this exact syntax. The important point is the object
separation:

- `HeaderEnumNode` is a header dispatch declaration.
- `SchemaNode` is the union of declaration forms inside the namespace.
- `EnumIdentifier` and `TypeIdentifier` are core constrained identifiers.
- `PathNode` imports a schema-defined name from another schema file.
- `ReferenceNode` points to an already assembled namespace object.

## Implementation Landed

`signal-frame` now parses the header-node form and keeps the earlier form
compatible:

- `signal-frame@a680aa0419b2` - adds `(Variant [Endpoint])` parsing for schema
  header nodes.
- `signal-frame@2e3450ee848c` - preserves `[Vec T]` and `[Option T]` as normal
  data-carrying enum payloads instead of treating them as header endpoints.

`signal-persona-spirit@2b4dd00c9081` rewrites `spirit.schema` to the corrected
header-node form, and `persona-spirit@4e0c7db1a496` consumes the new signal
contract.

## Verification

All checks below passed:

- `signal-frame`: `CARGO_BUILD_JOBS=2 cargo test`
- `signal-frame`: `nix flake check --option max-jobs 0`
- `signal-persona-spirit`: `CARGO_BUILD_JOBS=2 cargo test`
- `signal-persona-spirit`: `nix flake check --option max-jobs 0`
- `persona-spirit`: `CARGO_BUILD_JOBS=2 cargo test`
- `persona-spirit`: `nix flake check --option max-jobs 0`

## Remaining Work

The self-hosted schema-schema is not implemented. Today's parser has enough
surface to support Spirit's corrected header nodes, namespace forms, imports,
aliases, and current short-header emission. It does not yet expose a reusable
schema-language lowering library, UID-prefixed universal IR, or the recursive
header trie semantics implied by multi-endpoint header vectors.
