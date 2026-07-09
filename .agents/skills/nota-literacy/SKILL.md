---
name: nota-literacy
description: 'How to understand and answer with the NOTA expression required by a prompt-supplied schema, help projection, or examples.'
---

# NOTA shape checklist

## Rules for Shape

Start from the expected type; it is always known at a correct NOTA boundary. The file kind, schema field, operation argument, reply slot, test fixture, or prompt-supplied schema tells the decoder what type to read.

Write exactly the value of the expected type. The known document, record, object, or application shape fixes slot count: no extra slots, no missing slots, and no omitted positional optionals. Optionality is typed data in a known position.

Meaning comes from expected type plus position. A use-site name is data, a schema-required disambiguator, or a reference/path/name value under the expected type; it is never a label that identifies a positional slot.

A leading atom is valid only when the expected position is an enum and that atom exactly matches one of its variants. Run the variant-sibling test on every leading atom: name the other variants valid at this exact position. If none exist, the atom is not a tag; move the idea into the schema field, a typed enum value, or remove it.

Choose cardinality before syntax. A closed exactly-one-per-slot set is a positional record. Use a vector only for homogeneous repeatable elements where order or duplicates are meaningful, or where validation rejects duplicates. Do not encode fixed slots as tagged rows in a list.

Records are positional. Emit field values in schema order; do not put field labels in the value. Treat `Vector Vector`, same-name self-labeling, and `Name Value` adjacency as design alarms for self-labeling instead of typed positional data.

Use maps only for real key/value domains: arbitrary keys, lookup by key, and key identity as data. A value is a map because the expected type is a map, not because labels feel readable.

Prefer closed enums and typed records over strings. A bare atom is valid as a string when the expected type is `String`; capitalization does not infer type state. Enum slots decode by exact variant match.

Before accepting a shape, state the expected type, sibling variants for each tag, cardinality for each collection, and duplicate/order semantics for each vector. If any part is unknown, pause and ask; do not bury uncertainty in a special parser, ad hoc labels, or JSON-like shape.

## NOTA literacy

### Rules

NOTA is strict structured communication. The schema, help projection, or concrete examples supplied in the prompt give the expression its expected type and meaning.

Use the provided schema/help projection and examples as authoritative. For API-like calls, do not assume a runtime help tool is available; answer from the prompt's supplied contract.

Reply with only the requested NOTA expression unless the prompt explicitly provides a diagnostic or prose escape hatch. If such a hatch exists and the contract is unclear, use it to say what is unclear and what should be improved.

Parenthesized records and variants are positional. Field order matters, values do not carry field names, and every positional component appears in the expression. No extra slots, no missing slots.

Read field names in schema/help text as position labels, not as keys to emit. Do not turn records into maps unless the expected type is a map.

Use bare atoms for canonical strings, variants, identities, and stable names when the value is valid as an atom. Capitalization does not infer type state: a bare capitalized atom may be a string when the expected type is `String`, and enum slots decode by exact variant match.

Represent optionality exactly as typed data in the supplied shape. Do not omit positional fields; choose the explicit variant, option record, or required sentinel shape the schema provides.

Do not wrap the answer in markdown fences, JSON, YAML, comments, explanations, or surrounding prose. Do not invent double-quoted strings, field names, maps, or alternate delimiters.

Treat pseudo-NOTA documentation as a reader aid. Concrete schema/help projections and round-trip examples own the response shape.

### Examples

If the prompt says `Entry` is `{ Domains Kind Description Certainty Importance Privacy Referents }`, emit values in that order:

```nota
{ [(Technology All)] Principle [|Use the canonical codec.|] High High Zero [codec] }
```

If the prompt asks for `(Decision <kind> <reason>)`, emit the record without labels:

```nota
(Decision Accept [|The evidence satisfies the requested rule.|])
```

### Anti-Patterns

- inferring meaning from delimiters alone;
- changing positional records into keyed maps;
- omitting fields because they are optional in ordinary prose;
- treating pseudo-NOTA placeholders as wire truth;
- putting machine-readable data in comments;
- returning opaque `MeaningUnclear` when the prompt permits a diagnostic explanation.
