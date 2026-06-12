# The intent-capture protocol — argued justification, binary guardian, cross-record operations

The psyche's framing: *intent logging dwarfs everything else; it is the most important part of AI
that almost nobody has gotten right; everything revolves around intent.* So the capture path
deserves the most care in the system. This consolidates the model (superseding report 602's
mechanism section with the psyche's corrections). Captured: `i59i` (intent is paramount, Maximum
importance), corrected `woku` (binary guardian), `ll41` (argued justification), `7xnx`
(multi-dimensional judgment), `u62s` (certainty ⊥ importance).

## A live proof, this session

While capturing these, an agent (me) submitted *"the guardian stays binary"* — and the guardian
**rejected it as a `Contradiction` with `woku`**, because the old `woku` allowed the guardian to
"force low certainty," which the new decision forbids. The gate caught its own inconsistency. The
fix was the cross-record operation below: `ChangeRecord` on `woku` to remove the wrong clause.
That is the whole protocol working in one stroke.

## 1. The guardian is strictly binary — yes or no

The guardian **never makes graduated decisions** (no silently lowering certainty, no rewriting).
It only admits or refuses. This is deliberate (`woku`, corrected):

- **Thinking stays in the highest-power model — the submitting agent**, not the gate. A `no`
  because the submission "doesn't look certain/justified enough" sends the agent back to *think
  again*, reconsider, reword. The refusal is **generative** — it improves the submission by
  refusing it.
- It avoids the slippery slope of the guardian accreting judgment authority. The gate's job is to
  *guard*, not to *author*.

This corrects report 602's "admit-at-corrected-certainty" proposal — the psyche rejected it.

## 2. The justification is an argued case, with verbatim quotes

The submitting agent doesn't just attach a one-line reason — it **makes a case**, *sells* why this
should become intent (`ll41`):

- **Verbatim psyche quotes**, marked inline. Proposed marker: `*asterisks*` around the verbatim
  spans (not yet ratified). E.g. *"we were discussing X, then I proposed Y, then the psyche hinted
  by saying \*…verbatim…\*, and added \*…verbatim…\*."*
- **Context**: the conversational lead-up — what was discussed, proposed, conceded.
- **References to existing records** — because the submission may be a replacement (next section).

The verbatim is what lets the guardian judge faithfully: it sees the psyche's actual modality
(`could` vs `should`, `I think` vs a flat assertion), not the agent's paraphrase.

## 3. The guardian judges several dimensions — then collapses to one yes/no

From the argued justification, the guardian checks (`7xnx`):

1. **Does the justification justify the intent?** (Is the case sound — does the cited wording
   actually support recording this?)
2. **Is the domain right?**
3. **Is the certainty right for this justification?** (Tentative wording → low certainty, or
   reject.)
4. **Is the importance right for this justification?** (Independent of certainty — `u62s`. A
   tentative-but-load-bearing idea is low certainty, high importance.)
5. **Is the proposed cross-record operation sound?** (next section)

All of that judgment, but the *verdict* is still binary (§1). The dimensions are how it *reaches*
the yes/no, not separate outputs.

## 4. Cross-record operations — the justification can rewrite the corpus

A justification may **reference existing records and propose an operation over them** — the agent's
case can be *"records X, Y, Z already cover this; replace all of them with this one record at High
importance"* or *"replace X, Y with these two records at importances A and B because …"*. The
guardian judges the **whole proposed operation** as its single yes/no. This is the per-record,
agent-proposed, guardian-gated version of the batch merge pass (report 601) — the same shaping, but
done honestly at the moment of capture with an argued case, not retrofitted.

## Schema implications (for when this is built)

The current `Justification { StatementText, context (Optional) }` is far too thin for this. It must
grow into a structured argued case: the narrative, the verbatim-marked quote spans, the referenced
record identifiers, and the proposed cross-record operation (none / supersede-set / replace-with).
The guardian prompt gains the multi-dimensional checks and the operation-soundness judgment. This
is a significant guardian + signal-schema evolution — a workflow-sized implementation when the
design is blessed.

## Open question

- **Verbatim syntax** — `*asterisks*` around verbatim spans (the psyche's proposal), or another
  marker? Asterisks read clean and survive NOTA bare (`*` is bare-eligible). Lean: asterisks.

## Net

Intent is the precious center, so the capture path is the most-guarded path. The agent (highest
thinking power) argues a verbatim-grounded case; the guardian, seeing the real wording, judges it
across domain/certainty/importance/justification/operation and returns a **binary** verdict; a `no`
sends the agent back to think harder. Certainty becomes a faithful readout of how settled the
psyche was, importance stays free, and the corpus only ever holds intent that survived an argued
case against a gate that never blinks — and, as we just saw, never lets a contradiction through.
