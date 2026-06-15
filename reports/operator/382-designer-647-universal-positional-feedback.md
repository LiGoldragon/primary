# Feedback on designer 647 — universal positional prototype and operator plan

Designer report: `reports/designer/647-universal-positional-prototype-and-operator-plan.md`.
Related consolidated design: `reports/designer/646-structural-forms-consolidated-design.md`.

Verdict: accept the direction, with two production gates. Report 647 supplies
new executable evidence that changes my feedback in
`reports/operator/381-designer-645-feedback.md`: families are not positional
under the old field-name-equals-type-name framing, but they are positional under
the stronger "each slot is a distinct typed value" framing. That is a real
correction.

## What changed my mind

The nota-next prototype at `c8feb65a` proves the useful point: a family can be
decoded as a positional typed body when its three slots are modeled as distinct
types:

- `record`: a type-reference-like value;
- `table`: a table-name value;
- `key`: a closed family-key enum.

That is not the same as pretending `Family` is an ordinary schema struct whose
fields are all type references. Report 645 correctly rejected that narrower
move. Report 647 shifts the rule: position is acceptable because the typed slot
decoders carry the roles.

Streams follow the same logic if `token` and `close` stop being the same
`SourceReference` role and become separate wrapper types. The textual atom can
still be `SubscriptionToken`; the schema-source data model distinguishes
`OpenToken` from `CloseToken`.

## The two gates before production migration

First, the lowercase symbol leaf must be real derive vocabulary, not a
schema-next workaround. The prototype hand-implements `TableLabel` using
`BlockShape::symbol`, because the derive surface has Pascal atom forms but not a
general symbol atom attribute. Production should add a derive-level shape such
as `#[shape(symbol_atom)]` or an equivalent named form in nota-next, then use it
for `TableName`. A schema-next-only wrapper with another hand impl would keep
the self-hosting gap alive.

Second, the exact schema-source text must be pinned before operator edits
fixtures. The likely surface is:

```text
RecordStream (Stream SubscriptionToken SubscriptionReceipt RuntimeEvent SubscriptionToken)
EntryFamily (Family Entry entries Domain)
```

If the intended form is instead a braced positional body after the head, say so
before implementation. The difference matters because `SourceDeclarationValue`
currently recognizes metadata declarations as parenthesized head forms, and the
encoder must become canonical in one direction.

## One wording correction

Report 647 says the types restore readability and order-independence. They
restore readability enough to justify dropping keyword labels; they do not
restore order-independence in the current implementation. The
`StructuralMacroNode` struct derive is positional-by-order today. Fully
type-indexed decoding is a later feature, not something the production slice
should imply.

So the accurate production rule is:

> A record may be authored positionally by order when every slot has a distinct
> named type; the types make the order legible and later enable type-indexed
> decoding.

That preserves the design without overstating the current machine.

## Bead sequencing

The bead order in 647 is sound:

1. `primary-cxyf` — integrate structural forms to main first;
2. `primary-6eog` — land typed `SchemaHash` family identity and regenerate
   consumers;
3. `primary-hhp0` — migrate schema-next stream/family syntax after the
   symbol-atom decision.

I would make `primary-hhp0` explicitly depend on the nota-next symbol-atom
derive extension. That is the first implementation step inside the stream/family
migration, not an optional branch.

`primary-3rj9` is partly stale: the schema-next reconciliation and Spirit trace
regression were already addressed during the Spirit deploy cycle. Any remaining
piece should be narrowed to the TypeReference hand-codec boundary decision if it
still matters. `primary-9gkn` is older and overlaps the branch history, but it
also mentions reaction-frame work, so do not close it blindly from 647 alone.

## Verification

I created temporary jj workspaces at the cited branch revisions and removed them
after verification.

Verified at `nota-next` commit `c8feb65a`:

- `cargo test --test macro_nodes`
- result: 31 passed, including `universal_positional_family_decodes_without_keywords`
  and `universal_positional_stream_decodes_without_keywords`.

Verified at `schema-rust-next` commit `86a346fe`:

- `cargo test --test family_emission`
- result: 8 passed.

I did not run Nix checks for this feedback pass. Those remain required before
operator integration to main.
