# Guardian — answers to your four questions (psyche-confirmed)

For system-designer, ahead of the audit. Re: `reports/system-designer/89-...`. Your
understanding was right; the psyche confirmed it and added one principle that reshapes
the guardian's evidence base. Read that first — it changes the yardstick for #1.

## The new principle (read this first): the guardian judges against the psyche's verbatim words

The guardian's evidence base is not just the existing intent arrows. **The guardian
prompt must include the actual psyche statement(s) that justify the proposed change —
verbatim, with enough context to interpret them.** Bare affirmations are the reason:
if the psyche says "yes" / "okay" / "I agree", that is meaningless to the guardian
without the antecedent it was a response to. So a justifying statement travels as a
*(statement, context)* pair — the raw words plus what they were answering.

This reframes the guardian's question. Not "is this consistent with the store?" but:
**"Given the psyche actually said *this* (verbatim, in context), and the store holds
*these* arrows — is this change faithful and admissible?"** Intent records are
*derived* from psyche words and can be wrong; the guardian's job is to keep changes
*traceable to real psyche intent*, not just internally consistent.

**Design consequence (and a new audit item):** every state-changing operation must
carry, or reference, its justifying psyche statement + context, and the guardian must
be handed it. Records today carry a distilled `Description` (the arrow) but *not* the
raw justifying statement — so there is no path for it to reach the guardian yet. That
path (a field on the gated op, or a referenced `State` statement, captured with its
antecedent) is now part of the design, and its absence is a gap the audit should
surface. The Spirit-side decision-log (585 §3) is the natural place this lands durably.

## 1. Deletion semantics — justification, not necessarily replacement

Not one uniform judgment, and not "deletion requires a replacement." The common spine
is the principle above — *every change needs a justifying psyche statement* — with
operation-specific questions on top:

- **Admission / Supersede / Clarify** re-vet the *new arrow* for consistency against
  the store (and supersede additionally justifies retiring its target).
- **Deletion (Retire / Remove / Collect)** is gated on: *is there a psyche statement
  justifying this removal?* — **replacement is only one kind of justification.** "I
  changed my mind, I don't want this anymore," with no reason and no successor, is an
  equally valid justification: the psyche may not have a replacement, may be unsure
  what to replace it with, or there may be nothing to replace it with. The guardian
  does **not** demand a replacement; it demands a justification.

So the audit yardstick: does every state-changing op (both directions) reach the
guardian *with a justifying psyche statement attached*, and does deletion accept a
bare changed-mind justification rather than requiring a successor arrow?

## 2. Referent-gate strength — always gated, full guardian

**Every `RegisterReferent` is gated by the guardian.** Not synonym-check-first with
the LLM only on the residue — the full gate, every time. This resolves the open
question in designer `584` §4 toward the gated option *at full strength*, and overrides
the lighter "self-service, synonym-gated" shape that report proposed. The guardian is
the **one** semantic authority over **both** curated sets — records and referents —
consistent with the psyche's "the model checks everything" decision for records.

## 3. One guardian or two — one mechanism, two surfaces (the question, explained)

Your phrasing was right; here's the question spelled out, since the psyche asked what
it meant. The choice is: do we **reuse the same guardian machinery** — the
daemon → agent → LLM → binary-typed-verdict → fail-closed path — for the referent gate,
just with a referent-specific *prompt* and a referent-specific *verdict / rejection
type*; **or** build a genuinely **separate second gate** with its own infrastructure?

**Answer: one mechanism, two surfaces.** Same machinery (the agent-broker call, the
fail-closed wiring, the binary-verdict-with-typed-reasons pattern); a distinct
*referent prompt* and a distinct *referent verdict type*, because the record
`GuardianRejectionReason` is record-scoped — a referent needs its own reasons (e.g.
near-duplicate-of-an-existing-referent, too-vague, collides-with-a-synonym). So: one
guardian *engine*, gating two different curated sets through two prompts and two verdict
vocabularies. Not two separate gates.

## 4. Referent-name privacy — out of scope

The psyche's call: **out of scope, do not factor it in.** Where the LLM runs / privacy
of inference is explicitly not a concern for this work; revisit someday if ever. Build
as if the agent is trusted. Drop the question.

## Net

Your read was correct. The one thing to internalize before the audit is the verbatim-
words principle — it adds a real gap (no path today for a justifying psyche statement
to reach the guardian) and it redefines what "gate the deletion" means (justification,
which may be a bare changed-mind, not a replacement). With #2 confirmed (always-gated),
you can now capture the new-referent-gate decision against `584` §4 as you offered, and
proceed.
