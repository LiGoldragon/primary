# Feedback on designer 604 — intent justification as court design

## Gate outcome

No Spirit capture from this operator pass. The prompt is a request for feedback on an unsettled design thread, and the quoted exchange was addressed to designer. I queried recent public Spirit records for the relevant terms and found no matching record to gap-fill.

## Read surface

- `reports/designer/602-guardian-modality-catch.md`
- `reports/designer/603-intent-capture-protocol.md`
- `reports/designer/604-intent-justification-court-design.md`
- The psyche/designer exchange pasted in this prompt, which is newer than the checked-in 604 text on citation signals.

## Overall read

The court frame is doing real design work, not just naming. The strongest part is the inversion that certainty is the burden the submitting agent claims. That makes overstatement fail naturally: a High-certainty claim supported by hedged testimony loses because the evidence does not meet the claimed standard. It also preserves the binary guardian rule from 603: the guardian rejects and remands; it does not lower certainty or rewrite the record.

I would keep the design direction. The pieces that feel load-bearing for implementation are:

1. `Justification` becomes a typed argued case, not one prose field.
2. The proposed `Entry` remains the stored intent; `Justification` is the admission case and belongs in the decision journal.
3. Certainty and importance stay orthogonal. Importance never raises the certainty burden.
4. The guardian remains binary and checklist-driven.
5. Cross-record edits are pleaded motions, but the system does not need a separate citation-signal language.

## What I would change before implementation

### 1. Cut citation signals completely

The pasted exchange is right to remove `{Supports, Distinguishes, Contradicts, Background}` as a typed field. It duplicates the actual operation and the warrant prose.

If the submission changes an existing record, the operation is the relationship: supersede, clarify, retire, or collect/removal path. If it merely cites a near-neighbor, the warrant can say why the candidate is not a duplicate or why it follows from an older record. A citation-signal enum creates a second relationship model that will drift from the operation model.

Implementation constraint: record identifiers can appear inside typed motion payloads and in the warrant as prose references, but there should be no standalone `CitationSignal` enum unless a future operation actually needs it as input.

### 2. Keep `Claim` structurally tied to `Entry`

604 currently says `Claim` is the proposed `Entry`, but the example sketch shows `(Claim ...)` as if it might become another text slot. Avoid that. A separate text claim can diverge from the entry description, kind, domains, certainty, importance, privacy, or referents.

Better shape: `RecordRequest` carries the proposed `Entry` once, and `Justification` carries evidence and argument for that exact `Entry`. If `Justification` has a `Claim` field at all, it should be a typed reference/projection of the proposed `Entry`, not a second authored claim.

Implementation constraint: no duplicated intent description in the justification. One stored description, one argued case for it.

### 3. Make testimony typed without pretending it is authenticated

`TestimonyFabricated` is conceptually valid, but until the guardian receives the original prompt or a source transcript reference, it is heuristic. The schema should name that reality.

I would add either:

- `TestimonyFabricated` as a rejection reason with documentation that it means "apparent fabricated testimony," or
- `UnverifiableTestimony` if the design wants the reason name to be honest about current infrastructure.

The first is sharper for agent behavior; the second is more epistemically precise. My lean is `TestimonyFabricated`, but the prompt must say the guardian is judging apparent fabrication unless source authentication is available.

Implementation constraint: do not build source-authentication scaffolding into this slice. The typed testimony should be future-compatible with source references, but the first implementation can work from submitted testimony only.

### 4. Separate the three pieces that are currently all called "context"

The design needs three distinct slots because they do different jobs:

- `Testimony`: psyche wording being relied on.
- `Antecedent`: the prior prompt or proposal that makes a short answer like `yes` meaningful.
- `Context`: agent narrative around the exchange.

Only testimony carries evidentiary weight. Antecedent scopes testimony. Context explains why the agent thinks the record belongs in this part of the taxonomy, but it does not raise certainty by itself.

Implementation constraint: a quote with a short or deictic phrase should require an antecedent; a full standalone quote can have `None`.

### 5. Warrant should be structured enough to attack, but not overfactored

The warrant is the right load-bearing addition. It should force the submitting agent to map evidence to each judged field, but it should not explode into a micro-DSL.

A good first schema is typed sections, each with prose:

- `DomainWarrant`
- `KindWarrant`
- `CertaintyWarrant`
- `ImportanceWarrant`
- `PrivacyWarrant`
- `ReferentWarrant` if referents are present
- `MotionWarrant` if a motion is present

These can be fields or a vector of closed enum records. The point is that the guardian can reject "missing certainty warrant" without parsing one giant paragraph for invisible subclaims. The prose inside each section remains natural language.

Implementation constraint: no stringly typed warrant keys. If a section is optional, its absence is typed as `None` or by a closed enum variant set, not by a string label.

### 6. Cross-record motions need a closed operation model, not metaphor nouns

The report's legal terms are useful design language, but the schema should speak Spirit operations. Avoid variants like `Overrule` if the actual operation is `Supersede`; avoid `Vacate` if the actual operation is `Retire` or removal-candidate collection.

Implementation constraint: `CrossRecordMotion` should be a closed enum whose variants correspond to real daemon operations or planned daemon operations:

- `None`
- `Clarify`
- `Supersede`
- `Retire`
- possibly `CollectRemovalCandidates` only if the admission path is meant to perform batch cleanup

If "distinguish" stays in the design, it belongs only in the warrant: "this is not duplicate because..." It is not a write operation.

### 7. The rejection enum needs exact names before prompt work

The guardian prompt should be generated or at least mechanically synchronized from the schema enum. The report should list the exact rejection variants before implementation begins, because this drives both schema and prompt tests.

Likely additions from this design:

- `MissingTestimony`
- `InsufficientWarrant`
- `Overstated`
- `TestimonyFabricated`
- `ImportanceUnsupported`

Existing variants like `NonIntent`, `Compound`, `Duplicate`, `Contradiction`, `UnclearDomain`, `UnclearPrivacy`, `ClarifyTramples`, `ClarifyLosesMeaning`, and `SupersedeTargetMissing` remain useful if they exist in the current schema.

Implementation constraint: one closed enum, one generated prompt section, one parser expectation. Do not let the model invent reason names.

## Typed shape I would implement first

The schema should introduce `Justification`, `VerbatimQuote`, `Warrant`, and `CrossRecordMotion` as real schema nouns. `Justification` should contain the vector of `VerbatimQuote` values, the narrative context, the `Warrant`, and an optional `CrossRecordMotion`. `VerbatimQuote` should contain the quoted statement text plus an optional antecedent. `Warrant` should contain typed sections for domain, kind, certainty, importance, privacy, optional referents, and optional motion.

The important property is that the slots are typed and positional in generated NOTA, not labels in a free-form string and not a new pseudo-syntax. This should land through schema, regenerate the Rust types, and then the guardian prompt should render from those typed values.

## Guardian prompt implications

The prompt should be stable-prefix friendly:

1. Static prelude first: role, binary verdict rule, NOTA output grammar, rejection enum, burden ladder, checklist, few-shot examples.
2. Dynamic case second: proposed entry, testimony, antecedents, context, warrants, motion, retrieved records.
3. Exact output shape last, with no room for invented fields.

That helps DeepSeek's automatic prefix cache, but the more important reason is correctness: stable rules do not get interleaved with per-case evidence.

The guardian should reject the whole case on the first decisive failure only if that makes agent repair clearer. For testing, it may be better to require a single primary rejection reason even if multiple failures exist. Multi-reason verdicts invite ambiguous repair and brittle parsing.

## Tests I would require before production

1. Hedged testimony with Low certainty is accepted; the same testimony with High certainty is rejected as `Overstated`.
2. A task-only instruction with perfect formatting is rejected as `NonIntent`.
3. A quote-free justification is rejected as `MissingTestimony`.
4. A justification with testimony but no field mapping is rejected as `InsufficientWarrant`.
5. A high-importance claim must cite recurrence or blast-radius in the importance warrant; tone alone is rejected as `ImportanceUnsupported`.
6. A candidate that restates a live record is rejected as `Duplicate`.
7. A candidate that contradicts a live record is rejected as `Contradiction`.
8. A clarify motion that changes meaning is rejected as `ClarifyTramples` or `ClarifyLosesMeaning`.
9. A supersede motion naming a missing record is rejected as `SupersedeTargetMissing`.
10. A fabricated-looking quote is rejected as `TestimonyFabricated`, but the test must be phrased as heuristic until source authentication exists.
11. A short answer like `yes` without antecedent is rejected or treated as insufficient; the same `yes` with antecedent can pass.
12. The model cannot emit a reason outside the generated enum; malformed output retries once and then fails closed.

## Final recommendation

Proceed with the design after designer updates 604 to match the newer conversation: typed justification, no citation-signal enum, no distinguish verb, description remains the stored intent, and testimony fabrication is a heuristic until source authentication exists.

The implementation should be schema-first and test-first. The failure mode to guard against is exactly the recent domain-scope mistake: a design that says "typed" while operational code quietly converts to strings. Every relationship in this slice should be a generated enum or record, and every guardian prompt/render/parse path should consume those typed values rather than hand-shaped strings.
