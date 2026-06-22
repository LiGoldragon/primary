# Help schema IR branch demo

schema-operator report 7. Worktree branch shown for psyche review:

- Repo: `/home/li/wt/github.com/LiGoldragon/signal-spirit/schema-help`
- Bookmark: `schema-help`
- Commit: `0b7cfee6695d` — `signal-spirit: make help responses schema IR views`
- Base before this commit: `1d4a247a933e` — `signal-spirit: add positional instance schema pilot`

## Vision

Help should not have its own parallel `HelpBody` / `HelpTypeExpression`
tree. Help is a view of schema information, so the help response should
carry the same schema IR that schema decoding and Rust lowering already
use.

This branch makes that concrete in `signal-spirit`:

```rust
pub struct HelpResponse {
    declarations: SourceDeclarations,
}
```

`HelpResponse::from_schema_text` decodes with
`schema_next::SourceDeclarations::from_schema_text`, and
`HelpResponse::to_schema_text` encodes with
`SourceDeclarations::to_schema_text`. `Display` only delegates to that
codec. There is no local help printer and no local help text decoder.

The remaining help-specific layer is now only an index/projection over
decoded schema source:

- `HelpModel` indexes root variants and named declarations.
- `HelpRoot` and `HelpNode` wrap `SourceDeclaration`.
- `HelpModelBuilder` projects one help level from decoded
  `SourceDeclarationValue`.
- The output is still one-level help, but the value being returned is a
  `SourceDeclaration` / `SourceDeclarations` tree.

## What changed

The branch deletes the parallel help AST:

- Removed `HelpBody`
- Removed `HelpFieldTypes`
- Removed `HelpVariantTypes`
- Removed `HelpTypeExpression`
- Removed `HelpTypeExpressionKind`
- Removed `HelpTypeExpressions`

The help response now stores schema declarations directly:

```rust
pub fn from_schema_text(source: &str) -> Result<Self, HelpError> {
    SourceDeclarations::from_schema_text(source)
        .map(Self::new)
        .map_err(HelpError::from)
}

pub fn to_schema_text(&self) -> Result<String, HelpError> {
    Ok(self.declarations.to_schema_text())
}
```

The one-level help projection still matters. A raw declaration wrapper
would over-expand inline declaration payloads. The branch projects those
positions back to named references where help needs navigation rather
than transitive dumping:

- Struct fields whose names are type names become derived field names,
  so `VerbatimQuote` renders `{ QuoteText OptionalAntecedent }`, not an
  inline expansion of `OptionalAntecedent`.
- Enum variants with inline payload declarations become references to
  the variant name, so `Domain` remains a one-level enum of named arms.
- Top-level roots dereference aliases only far enough to show the root
  payload shape, so `(Help Record)` remains
  `(Record { Entry Justification })`.

## Vector spelling result

This branch also updates Spirit schema source from `(Vec T)` to
`(Vector T)` at schema positions. That is deliberate.

The current schema IR has a built-in `SourceReference::Vector`, and the
schema encoder emits `Vector`. If Help preserves `Vec`, then Help is not
really round-tripping through the intended schema reference; it is
preserving a source spelling that schema-next currently decodes as a
generic application.

The branch pins that with a test:

```rust
let declaration = response
    .declarations()
    .declarations()
    .first()
    .expect("single Domains declaration");

let Some(schema_next::SourceDeclarationValue::Reference(reference)) =
    declaration.value()
else {
    panic!("Domains help must be a schema reference declaration");
};

assert!(matches!(reference, schema_next::SourceReference::Vector(_)));
assert_eq!(response.to_string(), "(Domains (Vector Domain))");

let legacy = schema_next::SourceDeclaration::from_schema_text(
    "(Domains (Vec Domain))",
)
.expect("legacy spelling still decodes as schema data");

let Some(schema_next::SourceDeclarationValue::Reference(legacy_reference)) =
    legacy.value()
else {
    panic!("legacy spelling must decode as a reference declaration");
};

assert!(!matches!(legacy_reference, schema_next::SourceReference::Vector(_)));
```

That test shows the precise problem: `Vec` is not currently the same IR
as the built-in vector. So the branch chooses the schema IR spelling
instead of preserving old source spelling.

If psyche wants `Vec` as the canonical text spelling, the fix belongs in
`schema-next`: make `Vec` decode to the built-in vector reference and
make the schema encoder emit `Vec`. Help should then inherit that
behavior automatically by continuing to use `SourceDeclarations`.

## Captured examples

Current branch output:

```nota
(Help Record) -> (Record { Entry Justification })
(Help Entry) -> (Entry { Domains Kind Description Certainty Importance Privacy Referents })
(Help Domains) -> (Domains (Vector Domain))
(Help Description) -> (Description String)
(Help VerbatimQuote) -> (VerbatimQuote { QuoteText OptionalAntecedent })
(Help DomainMatch) -> (DomainMatch [Any Partial Full])
(Help IntentEventStream) -> (IntentEventStream (Stream { token SubscriptionToken opened SubscriptionStarted event IntentEvent close SubscriptionToken }))
```

The important part is not the text alone. Each line is encoded from a
`SourceDeclaration` and can decode back through schema-next.

## Tests

Ran in `/home/li/wt/github.com/LiGoldragon/signal-spirit/schema-help`:

```console
cargo test
```

Result: passed.

- `daemon_configuration`: 2 passed
- `dependency_boundary`: 2 passed
- `generated_contract`: 6 passed
- `validation`: 3 passed
- doctests: 0

```console
cargo test --features nota-text
```

Result: passed.

- `daemon_configuration`: 2 passed
- `dependency_boundary`: 2 passed
- `generated_contract`: 20 passed
- `validation`: 3 passed
- doctests: 0

Focused help coverage now includes:

- request recognition for top-level and named Help forms
- Spirit one-level shapes
- every decoded root and named schema target
- rkyv round-trip of `HelpModel` and `HelpResponse`
- schema-codec round-trip of single, top-level, stream, and enum help
- proof that `HelpResponse` carries schema IR, not a parallel help AST

## Next ownership

This branch is the worktree demonstration in `signal-spirit`. The deeper
owner of the projection surface is probably `schema-next`, because
other signal crates should not each grow their own help projection rules.

The shape I would move down is:

- input: decoded `SchemaSource` plus imported namespaces
- operation: one-level help projection over `SourceDeclarationValue`
- output: `SourceDeclarations`
- codec: `SourceDeclarations::to_schema_text` /
  `SourceDeclarations::from_schema_text`

Then `signal-spirit`, `signal-mentci`, and any text client only provide
their embedded schema source and call the shared schema projection.
