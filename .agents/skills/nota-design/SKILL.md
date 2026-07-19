---
name: nota-design
description: 'Current NOTA design discipline from the raw grammar and codec model: positional records, named variants, bare atoms for canonical strings, and data in records.'
---

# NOTA shape checklist

## Rules for Shape

Start from the expected type; it is always known at a correct NOTA boundary. The file kind, schema field, operation argument, reply slot, test fixture, or prompt-supplied schema tells the decoder what type to read.

Write exactly the value of the expected type. The known document, record, object, or application shape fixes slot count: no extra slots, no missing slots, and no omitted positional optionals. Optionality is typed data in a known position.

Meaning comes from expected type plus position. A use-site name is data or a reference/path/name value under the expected type; it is never a label that identifies a positional slot.

A leading atom is valid only when the expected position is an enum and that atom exactly matches one of its variants. Run the variant-sibling test on every leading atom: name the other variants valid at this exact position. If none exist, the atom is not a tag; move the idea into the schema field, a typed enum value, or remove it.

Choose cardinality before syntax. A closed exactly-one-per-slot set is a positional record. Use a vector only for homogeneous repeatable elements where order or duplicates are meaningful, or where validation rejects duplicates. Do not encode fixed slots as tagged rows in a list.

Records are positional. Emit field values in schema order; do not put field labels in the value. Treat `Vector Vector`, same-name self-labeling, and `Name Value` adjacency as design alarms for self-labeling instead of typed positional data.

Use maps only for real key/value domains: arbitrary keys, lookup by key, and key identity as data. A value is a map because the expected type is a map, not because labels feel readable.

Prefer closed enums and typed records over strings. A bare atom is valid as a string when the expected type is `String`; capitalization does not infer type state. Enum slots decode by exact variant match.

Before accepting a shape, state the expected type, sibling variants for each tag, cardinality for each collection, and duplicate/order semantics for each vector. If any part is unknown, pause and ask; do not bury uncertainty in a special parser, ad hoc labels, or JSON-like shape.

## NOTA design

### Design Rules

Use `nota-schema-design` when authoring schema for new NOTA types. Use `nota-literacy` when replying to a prompt that supplies a NOTA schema/help projection or examples.

NOTA is structural data. The raw grammar has atoms, parenthesized records, vectors, maps, pipe text, pipe parenthesis, pipe brace, and `;;` comments. Schema and codec layers assign meaning from the expected type plus position.

At every correct NOTA boundary, the expected type is already known. The known document, record, object, or application shape fixes slot count: no extra slots, no missing slots, and no omitted positional optionals.

Records are positional. Field order is part of the interface; reordering fields is a compatibility change. Prefer a trailing field or a new variant over changing existing positions. A use-site name is data or a reference/path/name value under the expected type; it is never a slot label or keyword argument.

Use an untagged struct when there is one payload shape. Use an enum only when a position can hold multiple named variants. Enum variants use names, not numeric codes.

Use bare atoms for stable identifiers, enum-like values, and canonical names. A bare atom is valid as a string when the expected type is `String`; capitalization does not infer type state. Use pipe text or quoted/bracket string forms when whitespace, punctuation, comments, or arbitrary prose are the point.

Put machine data in records, not comments. Comments explain unusual choices; they do not carry values that must be read, queried, validated, or migrated.

Model alternatives as variants or named option variants, not loose flags. A variant carries only the fields that choice needs.

Use maps only for genuinely keyed collections. A value is a map because the expected type is a map, not because labels feel readable. Atom keys are normal unless the map type requires a richer key.

Avoid multi-field unnamed tuples. If there is more than one value, name the record or fields in the schema so the positional call site stays readable. Treat self-labeling adjacency such as `Name Value` as a design alarm.

NOTA is strict positional: every positional component and every variant payload always appears in the text form. Never place optionality where it can omit a slot or collapse to a bare atom. Model optionality as typed data in a known position: an explicit variant, option record, or required sentinel shape.

Encode and decode structured data only through the canonical shared codec for its format. Hand-rolled or special-cased per-type encode/decode logic is forbidden.
