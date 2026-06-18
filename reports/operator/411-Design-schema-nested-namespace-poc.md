# Nested Schema Namespace POC

variant: Design

## Summary

I built and pushed a schema-next proof of concept for nested schema
namespaces on branch `schema-namespaces-poc` at commit `61aa1bf1`.

The POC proves the target shape is feasible without reintroducing
key/value-style struct fields:

```schema
router:routed_object {
  Destination ActorIdentifier
  Contract ContractName
  Operation ContractOperation
  Exchange [Request Reply]
  PayloadSize ContractPayloadSize
  PayloadOctets ContractPayloadOctets
  Envelope { Destination Contract Operation Exchange PayloadSize PayloadOctets }
}
```

The semantic schema flattens that source namespace into fully qualified
type identities:

```text
router:routed_object:Destination
router:routed_object:Contract
router:routed_object:Envelope
```

Rust emission can therefore mirror the path naturally as module/type
structure, while source authors write local names inside the namespace.

## What The POC Proves

- Nested namespace blocks can be parsed recursively from source `.schema`
  text and archived through `SchemaSourceArtifact` rkyv bytes.
- Local references inside the block resolve to fully qualified semantic
  names. `Envelope { Destination Contract }` lowers to fields whose
  references are `router:routed_object:Destination` and
  `router:routed_object:Contract`.
- Top-level shared types still resolve from inside the namespace. For
  example, `Destination ActorIdentifier` becomes a namespaced newtype over
  the existing top-level `ActorIdentifier`.
- The top-level namespace stays clean: `Envelope` does not leak as a
  top-level type name.
- Canonical source for the new positional struct form keeps bare fields,
  not `Destination *`, and not `destination ActorIdentifier`.
- Semantic content identity stays stable across source projection:
  source -> canonical text -> source -> semantic schema produces the same
  content hash.

## The Important Caveat

The POC surfaced a real grammar ambiguity. In the current mainline source
grammar, `Topic String` inside a struct body is still an old inline field
declaration form. But the desired positional syntax can also make adjacent
PascalCase atoms look like a list of fields:

```schema
Record { Topic String }
```

That could mean either:

- old form: declare/use field `Topic` over scalar `String`;
- new positional form: two fields, `Topic` and `String`.

The POC resolves this only inside explicit nested namespace blocks: a
lowercase/colon namespace key such as `router:routed_object` switches its
contained struct declarations to positional field parsing. Top-level and
legacy inline payloads keep the old parse so the existing suite remains
green.

That is enough to prove feasibility, but not enough for the final language
shape. The final design should choose one clean global answer: either retire
the old inline `Topic String` form everywhere in one coordinated break, or
give positional struct bodies an unambiguous structural macro form that cannot
collide with old pair syntax.

## Verification

From `/home/li/wt/github.com/LiGoldragon/schema-next/schema-namespaces-poc`:

- `cargo test`
- `nix flake check`

Both passed. The Nix check built through the remote builder and ended with
`all checks passed`.

