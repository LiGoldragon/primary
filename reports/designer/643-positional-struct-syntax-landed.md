# Positional struct syntax landed — schema-next epic

The positional struct-body field syntax is implemented, verified, and pushed on
`next/structural-forms` (`c7c6d8d8`). Full suite **159 pass**, clippy clean, and
the change is **semantically lossless** (content-identity hashes unchanged).

## What changed

Struct-body fields are now a **positional list of types**, mirroring how the data
reads in NOTA:
- bare type for the common case — the field name derives from the type
  (`Schema { Input Output Namespace }`);
- the **`key.TypeReference`** dot-differentiator when a field's name differs from
  the type's derived name (`ImportDeclaration { Name source.TypeReference }`);
- the `*` shorthand and the name-value struct form are **retired**;
- top-level namespace + imports stay `Name → definition`; named composites
  (`declaration (Vector Declaration)`) and inline declarations are preserved.

Both struct-body subsystems migrated in lockstep: `declarative.rs`
(`MacroExpansionFields` walker + dot-split) and `source.rs` (the source-codec
parser + `to_schema_text` encoder). All affected `.schema` files + inline test
schemas converted.

## How it ran — workflow, crash, and recovery

Per ultracode this executed as a background **Workflow** (an implementation agent
+ an adversarial-verify phase), anchored by one correctness invariant:
**identity hashes are blake3 over the canonical rkyv model, so a green
`identity.rs` proves the syntax change preserved every parsed model.**

The implementation agent did the bulk — the 4 mechanism files + ~36 schema/test
files, ~235 tool-uses — then **crashed on an API socket error** before committing
or returning a result. The work persisted in the worktree, so recovery was
straightforward and the correctness anchor earned its keep:

- Full suite was **158 green, 1 red** — and the one red was a *content-hash*
  test (`family_record_closure_hashes_through_the_content_identity_surface`),
  exactly the semantic guard firing.
- Root cause: the agent **missed one fixture** (`family-declarations.schema`),
  so the new walker misparsed its `Entry { topic Topic body String }` and the
  family closure couldn't resolve `topic`. Converted it; the hash test went
  green (model restored).
- The round-trip test then revealed the **canonical-form rule** — the encoder
  drops a redundant differentiator (field `topic` of type `Topic` emits bare
  `Topic`, since `topic` *is* the derived name), keeping `name.Type` only when
  they differ. Matched the fixture to the encoder's output → 159 green.

Without the model-based hash guard, the missed fixture would have been an
invisible semantic regression. It wasn't.

## Verification (self-adversarial — the workflow's verify phase was skipped on the crash)

- 159 pass, clippy clean.
- `identity.rs` passes with **unedited** hash literals (its diff is inline-schema
  conversions only) — semantic equivalence holds.
- The modified test `.rs` files changed **only inline schema strings**, no
  weakened or removed assertions.
- Namespace + imports preserved as `Name → definition`; spot-checked `root.schema`.

## Spirit recording — deferred (precise blocker)

Both intent records (the `639` dimensional principle, the `640` positional-syntax
decision) are authored and parse-validated. The store-layout block is resolved
(operator folded it forward), but the deployed **domain taxonomy changed** —
`SoftwareArchitecture` is no longer a valid `EngineeringLeaf`, and the `/git`
spirit checkout is stale relative to the deployed binary, so the correct new
domain can't be chosen reliably yet. Will submit with the corrected domain once
operator's spirit deploy + taxonomy settle. Per the psyche, logging is "later."

## Epic state (both pushed; operator integrates from these)

- **nota-next** `next/structural-forms` — leaf shapes + named-field + struct-level
  derive (74 tests).
- **schema-next** `next/structural-forms` — TypeReference reconciliation +
  prototype-seam patch + **positional struct syntax** (159 tests).
