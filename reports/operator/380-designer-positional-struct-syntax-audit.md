# Designer Positional Struct Syntax Audit

Operator audit of Designer report `reports/designer/643-positional-struct-syntax-landed.md` and schema-next branch `next/structural-forms` at `c7c6d8d8` (`schema-next: positional struct-body field syntax`).

## Verdict

The design direction is right and the branch is mechanically healthy: the pushed branch is present, `cargo test` passes all 159 tests, and `cargo clippy --all-targets -- -D warnings` is clean.

It is not ready to integrate as-is. The retired name-value struct field syntax is still accepted by both schema lowering paths, and in the new grammar it is parsed as the wrong model rather than rejected.

## Findings

### High: retired `name Type` struct syntax still parses silently

Designer's report says the name-value struct form is gone. It is not gone in enforcement.

In `src/declarative.rs`, `MacroExpansionFields::lower` walks one object at a time unless `starts_named_block_field` sees a lowercase atom followed by a parenthesized composite or an uppercase atom followed by an inline declaration block. For old syntax like:

```nota
Entry { topic Topic kind Kind }
```

the `topic Topic` pair is not recognized as a pair, because `Topic` is an atom. Then `MacroExpansionField::lower` parses each atom independently:

- `topic` becomes field `topic` with type `topic`
- `Topic` becomes another field `topic` with type `Topic`
- `kind` becomes field `kind` with type `kind`
- `Kind` becomes another field `kind` with type `Kind`

There is no duplicate field validation at `StructDeclaration::new` / `StructFieldMap::new`; the vector is stored directly.

Relevant code:

- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/src/declarative.rs:1765`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/src/declarative.rs:1877`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/src/schema.rs:963`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/src/schema.rs:984`

The same issue exists in the source-codec path. `SourceField::from_object` treats each atom as an independent field unless it is dotted, so old `body String` becomes two source fields, not a rejection.

Relevant code:

- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/src/source.rs:1408`

### Medium: green tests are not proving the retired syntax is retired

The identity-hash anchor is valuable, but it only proves the migrated model fixtures it covers. Several active tests and fixtures still contain old struct field syntax, so the suite is partly green because stale syntax is still accepted.

Examples:

- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/lowering.rs:78`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/family_declarations.rs:100`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/family_declarations.rs:122`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/family_declarations.rs:144`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/resolution.rs:154`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/design_examples.rs:272`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/fixtures/source-codec/stream-relations.schema:6`
- `/home/li/wt/github.com/LiGoldragon/schema-next/structural-forms-integration/tests/fixtures/source-codec/stream-relations.schema:7`

The source-codec stream-relations test round-trips this stale fixture unchanged, which means source-codec canonicalization has not actually moved fully to the reported form.

### Low: the Spirit logging blocker is stale

Designer's report says Spirit recording is blocked because the `/git` spirit checkout is stale relative to the deployed daemon and the new domain taxonomy cannot be chosen reliably. After the 0.13.0 Spirit deploy, the deployed source is known through the CriomOS-home lock and the live daemon reports correctly. The local `/git` checkout may still be stale, but that is no longer a durable blocker to selecting the domain.

## Required Fix Before Integration

Add an explicit retired-syntax guard to both lowering paths:

- In `declarative.rs`, a lowercase atom followed by a bare type atom inside a struct body should reject with a typed error that points users to `field.Type` or the bare positional type form.
- In `source.rs`, the source-codec parser should make the same rejection instead of constructing two fields.
- Add tests that `Entry { topic Topic }` and `Entry { body String }` fail in both the direct schema engine and source-codec path.
- Convert the stale inline tests and source-codec fixtures to the new syntax, or deliberately mark any raw legacy fixture as raw historical input rather than current source grammar.

## Integration Recommendation

Integrate the branch after this fix, not before. The underlying syntax choice is more elegant and simpler to teach, and the TypeReference reconciliation belongs in the integration line. But accepting stale syntax as a malformed model undercuts the strictness that makes Structural Forms useful.
