# Operator Audit 347 — Schema Terse Syntax Readiness

Target: schema syntax improvements from reports `570`/`571`/`573` and current
`schema-next` / `schema-rust-next`.

## Correction After Psyche Feedback

The first version of this report got the preferred authoring style wrong. The
psyche corrected it in Spirit record `e2si`: schema root input/output definitions
should support inline payload definitions directly in the root vector, e.g. the
shape the psyche wrote as `[Record { Topic * Description * }]`, rather than
forcing operation roots to be separated from their payload bodies through
namespace retags.

So the preferred visual shape is:

```nota
[(Record { Topic * Description * })
 (Observe { TopicMatch * })
 Version]
[(RecordAccepted { RecordIdentifier * DatabaseMarker * })
 (RecordsObserved { RecordSet * DatabaseMarker * })
 (VersionReported { VersionText * DatabaseMarker * })]
{
  Topic String
  Description String
  TopicMatch [(Any) (Full (Vec Topic))]
  RecordIdentifier (Bytes 12)
  DatabaseMarker { CommitSequence * StateDigest * }
  RecordSet (Vec Entry)
  VersionText String
  Entry { Topic * Description * }
}
```

Concrete parser note: in current implemented schema-next, each root vector member
is one NOTA object, so the tested concrete syntax is parenthesized
`(Record { ... })` inside the root vector. The psyche's example
`[Record { ... }]` names the desired compact visual shape, but if taken
literally as current NOTA it would be two vector elements (`Record` and the brace
object). If the exact unparenthesized spelling is required, schema-next needs
another syntax change. If the parenthesized entry is acceptable, the inline root
payload feature is already implemented.

## Understanding

The schema syntax improvements are not just shorter spelling. They change the
authoring model toward a cleaner root-local payload shape:

1. The root input/output vectors name the public operation surface and may define
   the root payload body inline.
2. The namespace holds reusable domain nouns used by those inline root payloads.

That means a schema should usually read like:

```nota
[(Record { Topic * Description * })
 (Observe { TopicMatch * })
 Version]
[(RecordAccepted { RecordIdentifier * DatabaseMarker * })
 (RecordsObserved { RecordSet * DatabaseMarker * })
 (VersionReported { VersionText * DatabaseMarker * })]
{
  Topic String
  Description String
  TopicMatch [(Any) (Full (Vec Topic))]
  RecordIdentifier (Bytes 12)
  DatabaseMarker { CommitSequence * StateDigest * }
  RecordSet (Vec Entry)
  Entry { Topic * description Description }
  VersionText String
}
```

Here `Version` is a unit root. `Record`, `Observe`, `RecordAccepted`,
`RecordsObserved`, and `VersionReported` define their root payload bodies at the
root declaration site. Reusable nouns (`Topic`, `DatabaseMarker`, `RecordSet`,
`Entry`) stay in the namespace. This is the style to port toward.

## What Actually Landed

Four syntax changes are implemented in the engine:

- **`52ro` self-tag collapse.** `(Entry)` in an enum body means `(Entry Entry)`.
  Current `schema-next/tests/lowering.rs` proves
  `self_tagged_variant_form_equals_explicit_repetition`.
- **Inline variant declarations.** `(Lookup { RecordIdentifier * })` in a root
  vector both declares the `Lookup` payload type and makes the root variant carry
  it. After the psyche correction, this is not merely a small-root convenience;
  it is the preferred style for operation input/output payload bodies when the
  body belongs to the operation root.
- **`yp29` bytes.** `Bytes` is a reserved scalar leaf, and `(Bytes 32)` is a
  fixed-width byte reference. The Rust emitter generates `Bytes(Vec<u8>)` and
  `FixedBytes<N>([u8; N])` with lowercase-hex NOTA projection, not `[1 2 3]`
  vectors and not strings pretending to be bytes.
- **`qz6j` no aliases.** This resolved harder than the original review: aliases
  are gone. Bare `Name Type` now declares a distinct newtype. If you write
  `State Statement`, you are asking for a real `State(Statement)` wrapper, not a
  transparent alias.
- **`lm84` hash identifiers.** A hash identifier is not a primitive. It is a
  marker newtype over `Bytes` or `(Bytes N)`, for example `Digest Bytes` or
  `Fingerprint (Bytes 32)`, with the same canonical hex projection.

The current code agrees with that story:

- `schema-next/src/source.rs` has `SourceVariantSignature::SelfTagged` and
  `SourceReference::FixedBytes`.
- `schema-next/src/engine.rs` lowers bare namespace references to
  `TypeDeclaration::Newtype`.
- `schema-next/src/schema.rs` has `TypeDeclaration::{Struct, Enum, Newtype}` and
  `TypeReference::{Bytes, FixedBytes}`; there is no live alias variant.
- `schema-rust-next/src/lib.rs` emits private tuple newtypes plus
  `new`/`payload`/`into_payload`, and emits `Bytes` / `FixedBytes` codecs.

## Porting Rules

When porting consumer `.schema` files, I should apply these rules:

1. Collapse old self-tags:
   `(Record Record)` becomes `(Record)` when the operation name and payload type
   are intentionally the same.
2. Prefer inline root payload declarations:
   `[(Record { Topic * Description * })]` is the implemented current spelling of
   the psyche's desired `[Record { Topic * Description * }]` shape.
3. Do not preserve old retag aliases:
   if old schema says `(Continue Continue)` plus `Continue NexusWork`, and the
   root operation has no fields of its own, write `(Continue NexusWork)`. If the
   root operation does have its own fields, write the inline root body instead.
4. Convert binary `String` or `(Vec Integer)` fields to `Bytes` or `(Bytes N)`.
   Use fixed width when the domain has a real width: digest, signature,
   fingerprint, nonce, key material.
5. Treat every bare `Name Type` as a real domain noun with a private newtype in
   Rust. Port call sites to `Name::new(...)`, `.payload()`, and
   `.into_payload()`.
6. Delete stale `.concept.schema` files instead of migrating them, unless a
   repo has explicitly made that file live. The state sweep found most are old
   dialect documentation, not build input.

## Has It Been Done Properly?

Mostly yes in code, with one syntax caveat. The implemented grammar is coherent
and the tests cover the important semantic cases: self-tag equivalence, inline
root declarations, newtype lowering, `Bytes`, `(Bytes N)`, and generated
bytes/hash round trips.

The caveat is exact spelling. Current tests prove `[(Lookup { RecordIdentifier *
})]` style, because the parenthesized block is one root-vector object. The
psyche wrote `[Record { Topic * Description * }]`. If that exact unparenthesized
root-vector member spelling is required, then the syntax work is not fully done;
schema-next needs a root-vector parser extension that groups a PascalCase atom
followed by a brace body into one variant declaration. If parenthesized inline
root entries are acceptable, the capability exists.

The remaining weakness is documentation drift. Current `schema-next/INTENT.md`
and `schema-rust-next/INTENT.md` still contain alias-era statements such as
"bare reference value in schema is an alias" and constraints naming
`TypeDeclaration::Alias`. Those docs are now wrong relative to current code.
Before a broad fleet port, designer or operator should update the repo docs so
future agents do not resurrect aliases.

I did not run the test suites during this read because the designer lane
currently holds locks on `/git/github.com/LiGoldragon/schema-next` and
`/git/github.com/LiGoldragon/schema-rust-next`; I only read current source,
tests, reports, and jj state.

## Readiness

I am ready to port schema files to the new style, with one caveat: I need the
exact spelling settled. If the accepted concrete syntax is the current
parenthesized inline form, I can start. If the desired concrete syntax is truly
`[Record { ... }]` without per-entry parentheses, I should first implement that
grammar extension in schema-next.

The correct port is not mechanically replacing every `(X X)` with `(X)`; it is:

- keep `(X)` when the wrapper `X` is real,
- use `(X Payload)` when `X` should carry an existing reusable payload directly,
- use `(X { ... })` for operation-owned payload bodies,
- keep reusable domain nouns in the namespace.

## Sources

- `reports/designer/570-schema-grammar-spec-review.md`
- `reports/designer/571-schema-grammar-implementation-handover.md`
- `reports/designer/573-schema-grammar-implementation-progress.md`
- `reports/designer/574-state-of-everything/13-schema-engine-verdict.md`
- `/git/github.com/LiGoldragon/schema-next/src/source.rs`
- `/git/github.com/LiGoldragon/schema-next/src/engine.rs`
- `/git/github.com/LiGoldragon/schema-next/src/schema.rs`
- `/git/github.com/LiGoldragon/schema-next/tests/lowering.rs`
- `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs`
- `/git/github.com/LiGoldragon/schema-rust-next/tests/emission.rs`
