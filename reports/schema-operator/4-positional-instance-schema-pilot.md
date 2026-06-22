# Positional instance schema pilot

Role: schema-operator
Date: 2026-06-22

## Result

Implemented and pushed a `signal-spirit` pilot for per-instance schema
projection on the `schema-help` branch:

- repo: `/home/li/wt/github.com/LiGoldragon/signal-spirit/schema-help`
- commit: `1d4a247a933ec2541169757884fceda72a487e52`
- message: `signal-spirit: add positional instance schema pilot`

The pilot adds a typed `InstanceSchema` tree behind `nota-text`:

- `InstanceSchema`
- `InstanceSchemaElement`
- `InstanceSchemaElements`
- `InstanceSchemaName`
- `InstanceSchemaModel`
- `InstanceSchemaError`

The tree derives `rkyv` and is tested with a binary round trip. It does
not add a text renderer. That omission is deliberate: text output must
come from a schema-owned codec surface, not from hand-written formatting.

## Shape pinned

The corrected root rule is implemented:

| instance element | schema element |
|---|---|
| `Record` variant token | `Input` |
| `Record` payload | payload schema directly |

So a decoded `Record` command projects to the typed equivalent of:

```schema
(Input ({ Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning }))
```

It does not insert `Record`, `RecordRequest`, or any other wrapper into
the positional schema. There is one schema element for each instance
element.

For a unit root command such as `Version`, the schema collapses to:

```schema
Input
```

Again, `Version` is the value's realized variant; `Input` is the type the
decoder expected at that position.

## Data and decoder path

The pilot is driven by decoded data and decoded schema:

1. The existing generated `Input` decoder parses NOTA into a real
   `signal_spirit::Input` value.
2. `schema_next::SchemaSource::from_schema_text` decodes
   `SIGNAL_SCHEMA_SOURCE` and `DOMAIN_SCHEMA_SOURCE` into typed schema
   sources.
3. `InstanceSchemaModel` joins the decoded `InputRoute` to the decoded
   source declaration and projects the positional schema tree.
4. `InstanceSchema` is a typed value and round-trips through `rkyv`.

There is no raw NOTA parsing in the instance-schema code, no
schema-string parser, and no text serializer.

## Tests added

In `signal-spirit/tests/generated_contract.rs`:

- `generated_instance_schema_for_record_input_is_positional`
- `generated_instance_schema_for_unit_input_collapses_to_input_name`
- `generated_instance_schema_round_trips_through_rkyv`

The first test decodes a real `Record` NOTA command through the generated
`Input` decoder, then asserts:

- root schema has exactly two elements: `Input` and one payload schema
- payload schema has exactly two positions: `Entry` and `Justification`
- `Entry` expands positionally to `Domains Kind Description Certainty Importance Privacy Referents`
- `Justification` expands positionally to `Testimony Reasoning`
- neither `Record` nor `RecordRequest` is inserted into the root schema

## Verification

Local `signal-spirit`:

- `cargo fmt`
- `cargo test --features nota-text generated_instance_schema -- --nocapture`
  - 3 passed
- `cargo test`
  - passed
- `cargo test --features nota-text`
  - passed

Spirit stack with the branch set:

```text
SPIRIT_STACK_REF=main
SPIRIT_TARGET_REF=schema-help
SIGNAL_SPIRIT_REF=schema-help
META_SIGNAL_SPIRIT_REF=schema-help
SCHEMA_NEXT_REF=schema-help
SCHEMA_RUST_NEXT_REF=schema-help
```

- `scripts/check-local-schema-stack`
  - all compatible-system checks passed
- `scripts/run-nix-integration-tests --nocapture`
  - 10 passed, 0 failed

The integration run built patched Spirit binaries through Nix and passed
the existing process-boundary tests, including the help-without-daemon
test and representative schema-output round trips.

## Deployment read

For current Spirit deploy readiness, this branch is green through the
available local and Nix stack gates. The instance-schema pilot is not yet
exposed through the Spirit CLI, so it does not change daemon behavior,
socket routing, persisted store format, or production database handling.

The code is ready as a `signal-spirit` pilot. The durable implementation
should still move the route/schema projection into generated decoder
support, because the generator is the right owner of "decoded value plus
expected source reference" traces.

## Remaining gaps

The remaining gaps are intentional boundaries, not test failures:

- The pilot lives in `signal-spirit`, not in `schema-rust-next`
  generation.
- It covers the `Input` root first, not every generated root/value type.
- It has no schema text codec for `InstanceSchema`; adding one by hand is
  forbidden.
- A CLI command surface for per-instance schema was not added.

The next correct step is a generator/schema-next pass: make generated
decoders able to emit the positional schema trace they already know while
decoding, then encode any user-facing text through a schema codec surface
owned by `schema-next`.
