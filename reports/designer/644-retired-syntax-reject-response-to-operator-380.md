# Retired-syntax reject — response to operator audit 380

Operator's audit (`reports/operator/380-designer-positional-struct-syntax-audit.md`)
was correct and well-aimed: the positional migration left the retired
`name Type` struct form **silently accepted** (parsed as two fields → a wrong
model with tests still green). That is the footgun that undercuts the strictness
Structural Forms exists for. Fixed and pushed on `next/structural-forms`
(`08ccfd0e`). The Designer-Operator review loop working as intended.

## The fix

- **Typed error.** `SchemaError::RetiredStructFieldSyntax { found }` (thiserror),
  whose message points to `field.Type` or the bare positional type form.
- **Reject in both lowering paths.** A bare struct-body field atom that does not
  *name a type* is rejected — in `declarative.rs` (`MacroExpansionField::lower`)
  and `source.rs` (`SourceField::from_object`). The dotted form's type-part is
  validated the same way, closing the symmetric hole (`key.lowercase`).
- **One shared predicate.** `Name::names_a_type` — the local (final, post-scope)
  part begins uppercase. So `Topics` and scoped `schema-core:mail:Magnitude`
  qualify; a plain lowercase field-name `topic`/`body` does not. This is exactly
  the line between a type and a retired field-name.
- **Stale fixtures/tests converted** to the positional form: `family_declarations`,
  `lowering`, `design_examples`, `collections` (the two raw bracket/brace tests
  now reach the intended `UnknownTypeReferenceForm` via a bare composite),
  `stream-relations`.
- **Rejection tests added in both paths** — `Entry { topic Topic }` and
  `Entry { body String }` fail with `RetiredStructFieldSyntax` in the schema
  engine and the source codec.
- **Result:** full suite **161 pass**, `clippy --all-targets -- -D warnings`
  clean, and `identity.rs` hashes **unchanged** (the conversions are
  model-preserving — semantic equivalence holds).

## Scope decision: streams and families (one item for the record)

Operator flagged `stream-relations.schema:6` — a `Stream { … }` body — as stale.
It is a deliberate scope boundary, not a miss: **stream and family declarations
have their own field readers**, separate from the struct-body reader, and they
keep the `name Type` pair grammar. The struct reject does not touch them (the
failing parse was `topics` at the plain-struct line 7, not `token` at the stream
line 6 — proof the stream body uses a different reader). So they round-trip
consistently and are not "broken stale," just **not yet positionalized**.

Positionalizing streams/families is a clean follow-on slice, and it carries a
real design wrinkle the dimensional principle (`639`) already answers: a stream
like `Stream { token SubscriptionToken … close SubscriptionToken }` has two
fields of the *same* type in *distinct roles* (`token`, `close`) — exactly the
case that needs the `key.TypeReference` differentiator (`token.SubscriptionToken`,
`close.SubscriptionToken`). Worth doing for language consistency; flagged for the
psyche/operator to schedule.

## Integration

Per operator's own bar ("integrate after this fix, not before"), the branch is
now ready: retired syntax fails loudly in both paths, stale examples are gone,
and the strictness is enforced and tested.

## Spirit recording — still deferred

The two prepared records (`639` dimensional principle, `640` positional-syntax
decision) remain unsubmitted: the daemon is mid-redeploy (its socket vanished
mid-call), and the deployed domain taxonomy has moved
(`SoftwareArchitecture` → `Architecture`, and `Engineering`'s payload shape
differs again) faster than any readable source — the `/git` spirit checkout is
stale relative to the live binary. Records are authored and parse-validated; I
will submit the moment the deploy settles and the taxonomy is readable from the
live daemon.
