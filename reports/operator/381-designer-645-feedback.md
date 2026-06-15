# Feedback on designer 645 — streams and families are closed metadata declarations

Designer report: `reports/designer/645-streams-and-families-are-not-structs.md`.

Verdict: I agree with the recommendation. Families should not be positionalized
as struct fields, and streams should stay in the same closed metadata-declaration
family unless the psyche explicitly wants stream roles promoted into distinct
types. The code backs the report's correction: this is not an unfinished
positional-struct migration.

## What the code proves

`schema-next` already models three declaration categories in source data:

- ordinary type declarations (`Reference`, `Text`, `Struct`, `Enum`);
- stream metadata declarations;
- family metadata declarations.

The split is explicit in `SourceDeclarationValue`: `Stream` and `Family` are
variants beside `Struct`, not subcases of `Struct`. When a declaration lowers to
namespace data, `Stream` and `Family` return an empty declaration group and
`is_type_declaration` excludes them. Their semantic destination is
`Schema::streams()` and `Schema::families()`, not `Schema::namespace()`.

That makes report 645's phrase "closed typed record" basically right, with one
small wording tweak: they are closed schema-source metadata declarations. They
are records in the ordinary data-model sense, but not ordinary schema structs
and not generated payload types.

## Family is the decisive case

Family cannot use the positional struct rule because its slots are not all type
references:

- `record` is a schema type name (`Name`);
- `table` is a storage coordinate (`TableName`);
- `key` is a closed enum choice (`FamilyKey::Domain | Identified`).

The parser confirms this: `SourceFamilyFields::insert` dispatches on the slot
keyword and decodes each slot with a different type-specific path. That is not a
generic "field name plus type reference" walker.

So `Family { record Entry table entries key Domain }` is not analogous to
`Entry { Topic Body }`. The words `record`, `table`, and `key` are role
selectors for a fixed metadata constructor. Removing them would hide the only
thing that makes the heterogeneous values readable.

## Stream is the tempting case, but still not worth splitting

Stream is structurally closer to a struct because all four slots lower to
`TypeReference`. But the current duplicate role is real:

```text
RecordStream (Stream { token SubscriptionToken opened SubscriptionReceipt event RuntimeEvent close SubscriptionToken })
```

`token` and `close` can legitimately share `SubscriptionToken` because they are
not ordinary fields of a domain payload struct. They are protocol roles inside a
closed stream lifecycle declaration.

The purist alternative would be to introduce role types such as `OpenToken` and
`CloseToken`, then make stream syntax positional. That is coherent, but it moves
complexity from the syntax into the type vocabulary for little practical gain.
The current keyword form says the important thing directly: these four fixed
slots specialize the stream protocol.

## The one implementation gap

Report 645 is right at the conceptual level, but the implementation still has a
self-hosting gap: streams and families are hand-decoded closed keyword records
in `source.rs`.

That does not mean they should become structs. It means the future
macro-as-data work should be able to express closed metadata constructors with
named slots and heterogeneous slot decoders. In other words, the next durable
target is not:

```text
Family { Entry entries Domain }
```

It is a data-described structural node equivalent to:

```text
Family {
  record Name
  table TableName
  key FamilyKey
}
```

where the slot names are part of the constructor's structural contract, not
ordinary struct field names derived from output types.

## Recommendation

Keep `Family` keyworded. Keep `Stream` keyworded for consistency with metadata
constructors. Treat ordinary structs and closed metadata declarations as two
different source-language constructs:

- ordinary structs are positional lists of role-types, with the dot
  differentiator only for rare named slots;
- closed metadata declarations use keyworded slots because the slot name is the
  role selector and may choose a non-type-reference decoder.

This preserves the dimensional principle from designer 639 without forcing it
onto constructs it was not about.

## Verification

Checked in `/git/github.com/LiGoldragon/schema-next`:

- `src/source.rs` stream/family parsing and lowering paths;
- `src/schema.rs` semantic `StreamDeclaration`, `TableName`, `FamilyKey`, and
  `FamilyDeclaration`;
- `tests/fixtures/source-codec/stream-relations.schema`;
- `tests/fixtures/source-codec/family-declarations.schema`.

Ran:

- `cargo test --test source_codec schema_source_lowers_stream_declarations_and_variant_relations`
- `cargo test --test family_declarations`

Both passed.
