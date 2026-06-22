# Instance schema codec vision

Role: schema-operator
Date: 2026-06-22

## Short answer

Yes: if `schema-next`'s canonical type-reference codec emits
`(Vector Domain)`, then Help should emit `(Vector Domain)` too.

The current split is a real convergence gap, not a feature:

- per-instance schema emits `(Vector Domain)` because the generated
  value decoder knows it decoded a Rust/vector container and records a
  typed `Vector` reference in the trace
- Help emits `(Vec Domain)` because the Spirit source schema still
  contains `(Vec Domain)`, and the current schema parser on the
  instance-schema/schema-help lines treats `Vec` as a generic
  application head rather than the built-in vector reference

So Help is not using a better or more source-faithful decoder. It is
preserving legacy source spelling through the generic-application path.
That is why the two surfaces differ.

## What is happening

There are three layers that can mention the same container:

1. Authored source schema:

```schema
Domains (Vec Domain)
```

2. Canonical schema reference value:

```text
SourceReference::Vector(SourceReference::Plain(Domain))
```

3. Canonical schema text emitted by `schema-next`:

```schema
(Vector Domain)
```

The durable invariant should be:

```text
source text --schema decode--> SourceReference::Vector --schema encode--> canonical text
```

Right now the instance-schema path follows that shape from the decoded
value side:

```text
decoded Domains value
  -> NotaDecodeTraced captures TypeReference::Vector(Domain)
  -> schema-next lifts it to SourceReference::Vector(Domain)
  -> schema-next emits (Vector Domain)
```

The Help path is still taking this shape for Spirit's current source:

```text
SIGNAL_SCHEMA_SOURCE contains (Vec Domain)
  -> schema-next reads it as SourceReference::Application { head: Vec, arguments: [Domain] }
  -> Help re-heads it as a declaration
  -> schema-next emits (Vec Domain)
```

That is still data-driven, but it is the wrong data: `Vec` is no longer
being interpreted as the built-in collection. It is just a PascalCase
application head that happens to spell like the old container shorthand.

## My vision

There should be one schema value and two projections:

```text
                           schema source
                                |
                                v
                        schema-next decoder
                                |
                                v
                         SourceDeclaration
                                |
            +-------------------+-------------------+
            |                                       |
            v                                       v
      contract Help                           Rust generation
  "what may be here"                          NotaDecodeTraced
            |                                       |
            v                                       v
      SourceDeclaration                  DecodedWithSchema<T>
            |                                       |
            +-------------------+-------------------+
                                |
                                v
                        schema-next encoder
                                |
                                v
                       canonical schema text
```

Help and per-instance schema should meet at `SourceDeclaration` /
`SourceReference`. They should never maintain separate spelling rules.

For a `Domains` newtype, both tools should agree:

```schema
(Help Domains) -> (Domains (Vector Domain))
schema([] as Domains).expanded() -> (Domains (Vector Domain))
```

For root values:

```schema
value:  (Record (...))
schema: (Input ({ Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning }))
```

For enum payloads:

```schema
value:  (Partial [...])
schema: (DomainMatch DomainScopes)
help:   (DomainMatch [Any Partial Full])
```

For scalar/newtype leaves:

```schema
value:  High
schema: (Certainty Magnitude)
help:   (Certainty Magnitude)
```

The distinction is not about spelling. It is about question:

- Help answers "what may be here?"
- instance schema answers "what type did this decoded value occupy at
  each actual position?"

Both answers are encoded by the same schema codec.

## What to fix

There are only two coherent choices.

### Choice A: `Vector` is canonical

This matches the current `schema-next` encoder and full-English naming
discipline.

Work:

- migrate contract schemas from `(Vec T)` to `(Vector T)`
- make Help golden outputs expect `(Vector T)`
- ensure `schema-next` rejects or migration-only handles `(Vec T)`
- keep per-instance schema as-is

Result:

```schema
(Help Domains) -> (Domains (Vector Domain))
schema(Domains []) -> (Domains (Vector Domain))
```

### Choice B: `Vec` is canonical

This matches older Spirit source spelling and prior prose examples, but
it is a shortened identifier and conflicts with the full-English naming
rule unless the psyche explicitly makes it a schema keyword exception.

Work:

- change `schema-next`'s type-reference decoder so `(Vec T)` lowers to
  the built-in vector reference
- change `schema-next`'s encoder so `SourceReference::Vector` emits
  `(Vec T)`
- update instance-schema tests from `(Vector T)` to `(Vec T)`
- update schema-next tests that currently assert `Vec` is a generic
  application

Result:

```schema
(Help Domains) -> (Domains (Vec Domain))
schema(Domains []) -> (Domains (Vec Domain))
```

## Operator read

My implementation preference is Choice A: `Vector` is canonical.

The reason is not compatibility. It is that `Vector` is already the
typed built-in in `schema-next`, already the emitted canonical text in
the codec, and already the name captured by the decoder trace. Help
emitting `Vec` is the outlier because it is preserving legacy source
spelling as a generic application.

If the psyche wants `Vec`, the correct change is still in
`schema-next`'s typed reference codec, not in Help and not in
instance-schema formatting. The rule stays the same either way:
pick one canonical head, make the schema decoder lower to that typed
reference, and make every visible surface emit through that one schema
encoder.
