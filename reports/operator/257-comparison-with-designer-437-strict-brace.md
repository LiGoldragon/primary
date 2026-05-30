# 257 — Comparison with designer 437 strict-brace proposal

*Kind: comparison report · Topics: schema, nota, strict-brace, designer-437, operator-256 · 2026-05-30 · operator lane*

## Verdict

Designer 437 and operator 256 agree on the load-bearing correction:

```text
Brace = key/value map. No self-named single objects inside braces.
```

The implemented stack now obeys that rule in the main schema files. Where the
two reports differ is not the brace invariant; it is the authored surface used
for the value side.

Designer 437 proposes a more explicit canonical authoring surface:

```nota
{
  Topic (Newtype String)
  Entry (Struct { Topics (Derive) Kind (Derive) })
  Kind  (Enum [Decision Correction])
}
```

Operator 256 implemented the compact delimiter-dispatched surface:

```nota
{
  Topic String
  Entry { Topics * Kind * }
  Kind  [Decision Correction]
}
```

Both are brace-honest because every namespace entry is still two objects:
`key value`. The implemented surface reads the value delimiter/type directly:
atom or parenthesized reference means newtype, brace means struct, square
bracket means enum.

## Agreement

The important shared points:

- Root input/output are positional. No `Input@[]` / `Output@[]` at the root.
- A namespace brace contains declaration pairs: `TypeName Value`.
- A struct brace contains field pairs: `fieldKey value`.
- A PascalCase field key can derive the field name from the type name.
- The key can be typed by case or sigil; the value is then read against the
  key's variant.
- Old `Name@{...}` and pipe-family forms are not the target syntax.

This is now implemented in `schema-next` and consumed by `spirit-next`.

## Differences

### 1. Type definition value: explicit tag vs delimiter dispatch

Designer:

```nota
Entry (Struct { topics Topics })
Kind  (Enum [Decision Correction])
Topic (Newtype String)
```

Implemented:

```nota
Entry { topics Topics }
Kind  [Decision Correction]
Topic String
```

My read: the implemented form is better as the authored `.schema` surface
because it uses the second object's shape as the declaration macro. The
designer form is better as a fully explicit `.asschema` surface because the
choice enum is visible as data: `Struct`, `Enum`, `Newtype`.

So I would keep the implemented `.schema` form, but make sure checked-in
`.asschema` remains explicit and serialized as data.

### 2. Derived field marker: `*` vs `(Derive)`

Designer:

```nota
Entry { Topics (Derive) Kind (Derive) }
```

Implemented:

```nota
Entry { Topics * Kind * }
```

The implementation uses `*` because the prompt floated a single same-type
marker, and it keeps the pair rhythm short. The designer's `(Derive)` is more
self-describing, but it is not actually a type reference; it is a schema-layer
field-value marker. I would not put `Derive` into `TypeReference`. If we add
it, it should live in a schema-surface `StructFieldValue`, not assembled
schema.

Pragmatic target:

```nota
Entry { Topics * Kind * }
```

Optional compatibility alias later:

```nota
Entry { Topics (Derive) Kind (Derive) }
```

Both lower to the same assembled field pairs:

```nota
topics (Plain Topics)
kind (Plain Kind)
```

### 3. Data-carrying enum variants: `Variant@ Payload` vs `(Variant Payload)`

Designer leans canonical positional records:

```nota
[(Record Entry) (Observe Query)]
```

Implemented target:

```nota
[Record@ Entry Observe@ Query]
```

This is the biggest remaining syntax question. Since brackets are vectors, not
maps, `Record@ Entry` is not a brace violation. It is still a two-part variant
object, with the key-side sigil marking that the variant carries data.

My current lean: keep `Variant@ Payload` as the authored schema shorthand
because it matches the key-sigil model the user just described. The assembled
schema can serialize the expanded enum variant as an explicit data object.

If the language later decides that brackets should contain only atoms and
parenthesized variant records, then `(Record Entry)` can be added as the
canonical `.asschema` form without changing the strict brace work.

### 4. Namespace sigils for imports/macros/re-exports

Designer asks whether namespace key sigils should land now. I deferred them.

The implemented namespace only supports the ordinary type declaration key:

```nota
{
  Entry { ... }
  Kind [...]
}
```

That is enough to fix the structural dishonesty. Import/export/macro key
variants should come with the macro-table-as-data work, because they need a
real value type and real assembled representation. Adding syntax before the
data model would recreate the black-box path we have been trying to avoid.

### 5. Dropping legacy syntax

Designer asks whether to drop `Name@{ Type }` entirely. The implementation
migrated the main files away from it, but the parser still accepts old forms in
compatibility paths.

That is deliberate for this slice. The right next cleanup is a separate
deprecation pass:

- reject old forms in target-mode tests;
- keep parser compatibility only if needed for old fixtures;
- remove old fixture syntax once downstream reports and examples are migrated.

## Code Reality After Operator 256

Implemented and verified:

```text
schema-next      bfcd554e  schema: preserve brace key-value syntax
schema-rust-next b92a42af  schema-rust: repin strict brace schema-next
spirit-next      134d9af9  spirit: use strict brace schema stack
primary          a55fbcca  operator: update strict brace implementation report
```

The current `spirit-next/schema/lib.schema` proves the migrated surface:

```nota
{}
[Record@ Entry Observe@ Query Remove@ RecordIdentifier]
[RecordAccepted@ SemaReceipt RecordsObserved@ ObservedRecords RecordRemoved@ RemoveReceipt Error@ ErrorReport Rejected@ SignalRejection]
{
  Import { SourcePath * LocalPath * }
  Export { LocalPath * PublicPath * }
  Entry { Topics * Kind * Description * Magnitude * }
  Query { TopicMatch * kind (Optional Kind) }
}
```

The schema lowers to the same checked-in generated Rust; the migration is
surface syntax, not a data-type change.

## My Recommendation

Keep the current implemented `.schema` surface:

```nota
Topic String
Entry { Topics * Kind * }
Kind [Decision Correction]
```

Make the explicit designer shape the `.asschema`/macro-data target:

```nota
(Public Entry (Struct { topics (Plain Topics) kind (Plain Kind) }))
(Public Kind (Enum [Decision Correction]))
(Public Topic (Newtype String))
```

Do not add `Derive` to assembled `TypeReference`. Derivation is macro sugar,
so it should disappear before assembled schema. If `(Derive)` is accepted, it
should be a schema-surface alias for `*`, not a final type-reference variant.

The next implementation move should be an explicit target-mode syntax test
that proves these three layers stay separate:

```text
authored .schema    Topic String / Entry { Topics * }
assembled .asschema (Public Topic (Newtype String)) / (Public Entry (Struct ...))
emitted Rust        pub struct Topic(pub String); pub struct Entry { pub topics: Topics }
```

That preserves the user's core rule: authored schema can be terse, but the
assembled schema must be fully data-shaped and serializable.
