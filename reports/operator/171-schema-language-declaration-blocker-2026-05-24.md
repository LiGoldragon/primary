# 171 - Schema language declaration blocker, 2026-05-24

## Status

Closed by designer `/326-v5` and the implementation captured in
`reports/operator/170-schema-spirit-mvp-implementation-2026-05-24.md`.

This report is preserved as the blocker record for `/326-v4`. The current
working syntax is no longer blocked: namespace map values no longer restate
their keys, and the implementation now rejects the recursive/self-repeating
form.

I started implementing the post-`/326-v3` correction in `signal-frame` and
`signal-persona-spirit`, then stopped before committing because the psyche
corrected `/326-v4`'s namespace declaration syntax.

The implementation surface is clean again. I reverted only my own uncommitted
edits in:

- `/git/github.com/LiGoldragon/signal-frame`
- `/git/github.com/LiGoldragon/signal-persona-spirit`

No code commit landed from the invalidated `/326-v4` syntax.

## Intent Captured

The new psyche correction is logged in Spirit:

- Record 461: namespace declarations must not repeat the type name as their
  inner data head.
- Record 462: schema namespace values need a distinct declaration language.

Earlier in this turn I also logged records 446-450 for the no-outer-wrapper,
header-first, vector-of-variants, imports, and three-header component schema
direction.

## What Is Implementable Now

The parser can be moved toward the new file-level structure once the
declaration value grammar is settled:

- `.schema` files have no outer root record.
- The file body is multiple top-level schema fields.
- Header surfaces are ordered vectors of variants.
- Bare PascalCase names are unit variants.
- Parenthesized entries are data variants.
- The ordinary signal, owner signal, and Sema headers are distinct positions.
- Namespace is a map only because it is a name-to-declaration lookup.

The previous `signal-frame` parser shape already gives useful starting points:

- `macros/src/schema_reader.rs` has a dedicated `SchemaParser`.
- `parse_variant` already understands unit variants and data variants.
- `parse_namespace_map` already validates PascalCase map keys.
- `parse_feature_vector` can be added once Reply/Event/Observable placement is
  ratified.

## Blocker

The namespace value grammar is not settled.

`Kind (Kind Decision Principle ...)` is invalid because `Kind` is already the
namespace key. The value begins with the same name, so it reads as recursive or
colliding: a `Kind` whose first field is `Kind`. The same applies to
`Topic (Topic String)`, `Summary (Summary String)`, `Quote (Quote String)`,
and every same-name wrapper declaration.

The schema language needs distinct declaration forms that describe the type
without reusing the type's own name as the inner head.

Possible shapes for designer/psyche ratification:

- `Kind (Enum Decision Principle Correction Clarification Constraint)`
- `Topic (Scalar String)`
- `Entry (Record Topic Kind Summary Context Magnitude Quote)`
- `Observation (Enum State (Records RecordQuery) Topics Questions)`

The exact words are not operator territory. `Enum`, `Scalar`, and `Record` are
only examples of non-colliding declaration heads.

## Tests To Add Once Settled

- Parser accepts a `.schema` file body with no outer root record.
- Parser accepts ordered header vectors and preserves order.
- Parser accepts unit and data variants in header vectors.
- Parser requires the ordinary, owner, and Sema header positions, allowing
  empty `[]` for unused legs if that remains the design.
- Parser accepts the settled namespace declaration heads.
- Parser rejects same-name self-recursive declarations such as
  `Kind (Kind Decision Principle)`.
- `signal-persona-spirit` compiles from the settled schema file and still
  passes the short-header and dispatch witnesses.

## Recommendation

Wait for the next designer correction on namespace declaration syntax before
landing code. The header-vector implementation is straightforward; the
namespace declaration grammar is the load-bearing piece that would otherwise
require another immediate rewrite.
