# Operator Feedback On Designer 583

## Scope

This reviews `reports/designer/583-spirit-domain-category-vocabulary.md` as an
operator implementation surface for Spirit. I checked it against the current
Spirit source, the prior designer audit in
`reports/designer/581-spirit-implementation-audit.md`, and my previous operator
review in `reports/operator/355-spirit-designer-581-audit-review.md`.

The report is directionally strong: the old 12 gerunds failed, records should
file at concrete leaves, and a broad life-and-work vocabulary fits Spirit better
than a workspace-only software taxonomy. But report 583 is not yet a safe
implementation order. Several choices it leaves open are schema-shaping choices,
not small toggles.

## What Looks Right

The domain/category split is the best part of the report. A broad `domain`
above a concrete `category` lets the top tier be stable and human-readable while
records file at discriminating leaves. That directly answers the failure mode
from designer 581: the old catalog filed records at abstract top-level concepts,
so `Meaning` became a sink.

The anti-failure rule is also right: records should not file at the broad tier.
If a record can only be assigned to `craft-and-making` but not to
`data-modeling`, `software-architecture`, `version-control`, or a sibling leaf,
the category system has not done its job yet.

The warrant-gated vocabulary model is the right replacement for free-form topic
growth. The system needs canonical atoms, scope notes, synonyms, and a review
gate. That is the mechanism that prevents the old topic/keyword bloat from
returning under a new name.

The report is correct to resist a top-level software-only domain. Spirit is meant
to file intent across all life, not just current workspace engineering records.
The current corpus is a biased seed sample, not the universe.

## Things That Need Attention

The seed count is wrong or stale. Report 583 says "24 domains, 196 seed
categories", but the listed section enumerates 24 domains and 298 comma-separated
leaf names. That has to be corrected before implementation because the size
changes the enum-versus-registry pressure, migration cost, review burden, and
prompt/retrieval surface.

The enum-versus-registry decision is a blocker, not a late implementation detail.
The report simultaneously says "clean value-set swap" and asks whether
`Category` should stop being a compile-time enum. Those are different designs:

| Choice | Consequence |
|---|---|
| Compile-time enum | Schema regeneration on every category addition; NOTA parser rejects unknown leaves; migration is type-checked but vocabulary growth is code deploy. |
| Registry-backed value | `Category` becomes a string/newtype or identifier; daemon validates against a persisted/seeded catalog; category additions are data/config operations, not schema changes. |

At 298 listed leaves and intended growth into hundreds, registry-backed looks
more likely to be the durable shape. If that is chosen, operator should not spend
time generating a 298-variant Rust enum only to replace it.

The `Keyword` critique misdescribes current source. Spirit does not store a
free-text `Keyword` field on `Entry`; `Entry` stores only categories, kind,
description, certainty, importance, and privacy. `Keyword`, `Keywords`, and
`KeywordMatch` are generated query/helper nouns, and runtime keywords are derived
from asterisk spans in `Description`. So "retire the free-text `Keyword` field"
would actually mean removing a query mechanism, not deleting stored entry data.

The UF synonym table is not a drop-in replacement for current keyword matching.
UF synonyms normalize category names: `jj` can redirect to `version-control`.
Current asterisk keywords can name record-local discriminators inside a
description: a component name, operation name, tool name, or phrase that should
remain searchable without becoming a category. If the synonym table fully
replaces keywords, the design needs another way to search for those
record-local terms.

The third tier is the central unresolved design. Report 583 says `nota`,
`signal`, `sema`, `daemon`, and `nix` should be third-tier nests rather than
categories. If the third tier is curation-only, queries cannot distinguish
NOTA-specific records from signal-specific records except through full text. If
it is stored, then Spirit has another filing field and the "records file at the
category leaf" rule becomes incomplete. This must be settled before migration.

Multi-tag semantics need to be specified before data migration. `Categories` is
currently a vector, and guardian retrieval uses partial category matching. With
hundreds of leaves, the difference between "one primary category plus secondary
categories" and "unordered one-or-more categories" affects retrieval, counts,
dedupe, guardian prompts, and migration review. The report asks the right
question, but operator cannot implement the vocabulary cleanly until the answer
is part of the spec.

The listed categories need scope notes before they are implementation-ready.
Names alone are not enough for a controlled vocabulary. For example,
`software-architecture`, `systems-and-infrastructure`,
`technology-and-systems`, `information-management`, `documentation`, and
`knowledge-organization` will overlap heavily without one-line boundary notes
and examples. The scope note is not documentation garnish; it is the data that
lets classifier prompts, migration rules, and future auditors make the same
decision twice.

The migration plan needs to be deterministic and reviewable. "Rule-table from
existing keyword strings, or re-derive by a classifier" is too loose for
production state. A classifier can propose mappings, but the migration should
land as a checked mapping artifact with pre/post counts, zero-bucket detection,
sample records per new category, and explicit review of ambiguous records. The
old substring default-to-`Meaning` migration is exactly what we must not repeat.

The report should not let the category replacement outrank the guardian fixes.
Designer 581 and operator 355 both found that `Supersede` and `Clarify` bypass
the guardian and that guardian retrieval ignores keyword/text matches. A better
category catalog improves retrieval only after the gate actually uses the right
retrieval bundle and covers the write paths. Vocabulary migration and guardian
reach should be sequenced together, with guardian reach still the safer first
operator slice.

## Implementation Shape I Would Accept

A revised implementation-ready design should provide four concrete artifacts:

| Artifact | Why it matters |
|---|---|
| A machine-readable vocabulary catalog | Domains, categories, scope notes, UF synonyms, and optional third-tier nests need to be data, not only report prose. |
| A resolved schema choice | Either compile-time enum or registry-backed `Category`, with the resulting Signal/SEMA query types spelled out. |
| Migration fixtures | Real schema/NOTA files or database fixtures that map existing records to the new vocabulary and prove counts/distribution. |
| Guardian tests | Tests proving category, text, and record-local term retrieval feed guardian prompts, plus `Clarify`/`Supersede` gate coverage. |

The catalog should be authored as a real file, not embedded inline in Rust tests.
That matches the test-design rule the psyche just added: use actual schema or
data files in tests instead of burying important examples in Rust string
literals.

If registry-backed category is chosen, the likely Spirit schema direction is:
`Category` becomes a canonical atom/newtype, `Categories` stays the record filing
vector, `Domain` is derived through the vocabulary catalog, and query validation
checks category atoms against the active catalog. UF synonyms live in the catalog
and normalize at input/migration time; they do not need to be stored on each
record.

If compile-time enum is chosen, then report 583 should be trimmed hard. A
298-variant schema enum with future growth by regeneration is a heavy surface,
and every category addition becomes a cross-repo schema/code/deploy change. That
may still be acceptable for a near-frozen seed, but it should be chosen
explicitly, not as a default.

## Recommended Next Step

I would ask designer to revise 583 before operator implements the vocabulary.
The revision should decide:

1. `Category` enum or registry-backed category atom.
2. Whether the third tier is stored, queryable, or curation-only.
3. Whether Spirit keeps record-local keyword/text retrieval separate from UF
   synonym normalization.
4. Whether records have one primary category, unordered multiple categories, or
   primary-plus-secondary categories.
5. The corrected seed list and count, with scope notes and UF synonyms.

In parallel, operator can continue the already-verified guardian fixes:
category/text/record-local term retrieval for guardian prompts, guarded
`Clarify`, and guarded `Supersede`. Those fixes are independent of the final
vocabulary names and remove the most serious integrity gaps from the current
daemon.

## Bottom Line

Report 583 is a good direction paper and a weak implementation spec. It correctly
identifies that Spirit needs concrete leaf categories under broad domains, but it
leaves open the decisions that determine the schema and storage model.

The largest immediate correction is the false precision around "196" categories:
the written list has 298 leaves. The largest design correction is the
keyword/synonym conflation: UF synonyms normalize vocabulary terms; they do not
automatically replace record-local searchable terms. The largest sequencing
correction is that guardian reach and retrieval still need to be fixed whether
the category catalog changes now or later.
