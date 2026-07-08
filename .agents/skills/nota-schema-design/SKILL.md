---
name: nota-schema-design
description: 'How to design and write schema that specifies new NOTA types, positional forms, optionality, and codec-backed help surfaces.'
---

# NOTA shape checklist

## Rules for Shape

Start from the expected type; it is always known at a correct NOTA boundary. The file kind, schema field, operation argument, reply slot, test fixture, or prompt-supplied schema tells the decoder what type to read.

Write the value of the expected type. Do not prefix a value with its own type name. A leading atom is valid only when the expected position is an enum and that atom is one of its variants.

Run the variant-sibling test on every leading atom: name the other variants valid at this exact position. If none exist, the atom is not a tag; move the idea into the schema field, a typed enum value, or remove it.

Choose cardinality before syntax. A closed exactly-one-per-slot set is a positional record. Use a vector only for homogeneous repeatable elements where order or duplicates are meaningful, or where validation rejects duplicates. Do not encode fixed slots as tagged rows in a list.

Records are positional. Emit field values in schema order; do not put field labels in the value.

Use maps only for real key/value domains: arbitrary keys, lookup by key, and key identity as data. Do not use a map because labels feel readable.

Prefer closed enums and typed records over strings. A bare atom is valid only as a real enum variant, stable identifier, or canonical atom under a typed field; it is not a field label.

Before accepting a shape, state the expected type, sibling variants for each tag, cardinality for each collection, and duplicate/order semantics for each vector. If any part is unknown, pause and ask; do not bury uncertainty in a special parser, ad hoc labels, or JSON-like shape.

## NOTA schema design

### Rules

Schema specifies NOTA types, source syntax, and codec contracts. Raw NOTA parses first; schema lowering assigns type meaning after the structural parse succeeds.

Design one explicit type shape for each value shape. Use positional structs when there is one payload shape, and named enum variants when a position can carry multiple alternatives.

Struct fields are positional in authored schema source. Use `TypeName` when the field role derives from the type name, `role.TypeName` when the role differs, and `role.(Composite TypeName)` for parenthesized references such as `role.(Optional TypeName)`.

Use current reference heads such as `Vector`, `Map`, `Optional`, `ScopeOf`, and `(Bytes N)` according to the schema source grammar. Avoid retired pair forms and editor-tolerance aliases in authoritative schema.

Optional named struct fields are legal when absence differs from an empty value. Optional enum payloads and disappearing positional fields are wrong; use explicit variants or named optional fields instead.

Keep pseudo-NOTA docs separate from schema truth. Pseudo-NOTA may help humans read field names in markdown, but schema source, generated help, and round-trip examples own the contract.

Prefer canonical schema, codec, source, and help projection APIs over hand parsing or rendering. Do not create parallel per-type parsers, printers, or help languages.

When authoring prompts for models that must answer in NOTA, include the relevant schema/help projection or concrete examples in the prompt. Do not rely on the model calling a help tool during the API-like turn.

For judge-style prompts, provide an explicit diagnostic option when ambiguity should be explainable. The diagnostic branch may allow ordinary prose; normal NOTA replies stay expression-only unless the schema says otherwise.

### Examples

Use positional field references in schema source:

```nota
Entry {
  Domains
  Kind
  Description
  Certainty
  Importance
  Privacy
  Referents
}
```

Use an explicit role when the field role differs from the type:

```nota
VerbatimQuote {
  QuoteText
  optionalAntecedent.(Optional Antecedent)
}
```

Model optional variant payloads as explicit alternatives:

```nota
Decision [
  (Accepted Reason)
  (Rejected Reason)
  NeedsClarification
]
```

### Anti-Patterns

- mixing schema source truth with pseudo-NOTA documentation;
- encoding field names into positional values;
- using `(Optional T)` as an enum payload or positional field that can disappear;
- preserving retired pair syntax in new schema;
- hand-rendering help text outside the schema/codec projection.
