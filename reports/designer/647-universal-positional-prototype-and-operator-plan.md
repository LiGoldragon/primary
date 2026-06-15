# Universal positional syntax — prototype + operator production plan

Designer prototype proving the universal-positional design, plus the production
work it hands to operator. Consolidated design context: report `646`.

## What landed (designer, verified)

- **nota-next `next/structural-forms` (`c8feb65a`)** — the universal-positional
  prototype. `StreamSignature` (the dimensional fix: `token`/`close` as distinct
  `OpenToken`/`CloseToken` newtypes, four distinct slots) and `FamilySignature`
  (heterogeneous: a type reference, a lowercase name literal, an enum) both decode
  **positionally with no keyword labels** through the existing struct derive, and
  round-trip. 76 tests green, clippy clean. Proves the design with existing
  machinery.
- **schema-rust-next `next/family-identity-newtype` (`86a346fe`)** — the family
  identity is emitted as a typed `SchemaHash` named newtype end-to-end (was a raw
  `[u8; 32]` re-wrapped downstream). 86 tests green.

## The rule

A record is a positional list of typed values, no keyword labels, **when every
slot is a distinct named type** (Spirit `ov30`/`adnn`). This dissolves the
struct-vs-closed-record split: streams and families are positional structs once
their slots are distinct types.

## Production plan (the beads below)

1. **Migrate schema-next streams/families to positional typed-body structs.**
   Replace the keyword readers/encoders (`SourceStreamFields`,
   `SourceFamilyFields`, the `chunks_exact(2)` pair-parsers) with positional
   struct decode (the struct derive). Streams: introduce `token`/`close` as
   distinct newtypes (`OpenToken`/`CloseToken`). Convert the stream/family
   fixtures. Model on the nota-next prototype (`StreamSignature`/`FamilySignature`).
   - **One finding from the prototype:** a family's `table` is a *lowercase name
     literal*, not a type — the derive's bare-atom shapes are PascalCase
     (`pascal_atom`) only, so a lowercase symbol leaf needs either a new
     **symbol-atom shape** in the nota-next derive or a table-as-distinct-type
     wrapper. The prototype hand-impl'd a symbol leaf to prove it; production
     needs the shape (or wrapper) decided.

2. **Integrate the family-identity `SchemaHash` newtype emission.** Land
   `schema-rust-next next/family-identity-newtype` on main and **regenerate the
   consumers** (e.g. `spirit/src/schema/sema.rs`) so the checked-in generated
   `family_identity` modules become `SchemaHash` consts.

3. **Integrate the structural-forms epic to mains.** Land the positional
   struct syntax + `SchemaError::RetiredStructFieldSyntax` reject from
   `schema-next next/structural-forms` and `nota-next next/structural-forms`,
   superseding the divergent older `structural-forms-integration` line (the
   `631` reconciliation `17b4ebc` is *not* in it — see `635`/`641`).

## Notes / risks

- **Family heterogeneity** is real (a type / a literal / an enum) — positional
  works because the three are *distinct types*, but the table-literal shape gap
  (above) must be closed first.
- **Keyword-form trade-off:** positional drops the keyword labels' readability
  and order-independence; under the rule the *types* restore both, so it is a net
  gain in strictness, but reviewers should expect stream/family source to read as
  bare positional lists.
- **Order vs type-indexed:** positional-by-order works today (the struct derive);
  fully order-free *type-indexed* resolution (assign each value to its slot by
  type) is the further prize once every slot is a distinct type — optional.

## Beads filed (operator)

- **`primary-cxyf`** — Integrate the structural-forms epic (positional struct
  syntax + retired-syntax reject) to mains. *Do first* — the others build on it.
- **`primary-6eog`** — Integrate the family-identity `SchemaHash` named-newtype
  emission + regenerate consumers.
- **`primary-hhp0`** — Universal-positional: migrate schema-next streams/families
  to positional typed-body structs (token/close distinct newtypes; the family
  table-literal symbol-atom-shape decision is inside it).

Existing related: `primary-9gkn` (older design-branch integration), `primary-3rj9`
(description partly stale — `thiserror`/`Bytes` landed; re-scope to the
TypeReference hand-codec decision + propagating the positional/reject work),
`primary-bojw` (macro-table self-host).
