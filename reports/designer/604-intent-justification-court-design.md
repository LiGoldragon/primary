# The intent justification as a court of law — design

The design for the upgraded justification + guardian, drawn (per the psyche) from legal
argumentation, evidence, burden of proof, and dialectics. Synthesized from an 8-field research
workflow (`wf_2db93f5f-059`: courtroom advocacy, evidence law, standards of proof, Toulmin/Walton,
pragma-dialectics, computational argumentation/AI-and-Law, stare decisis, epistemic modality). It
builds on the protocol decisions (`z3ka` court framing, corrected `woku` binary guardian, `ll41`
argued justification, `7xnx` multi-dimensional judgment, `u62s` certainty⊥importance, `i59i` intent
is paramount). This is a proposal for the psyche to rule on; nothing is built.

## The six central transfers

1. **An argument is a structured object, not a paragraph.** Re-shape `Justification` into typed,
   separately-attackable slots, so a weak case shows *which slot is empty*.
2. **Certainty IS the burden of proof the testimony must clear** — not a confidence the guardian
   sets. The agent *proposes* the burden by claiming a certainty; the verbatim must clear it.
   Over-claim → the case fails its burden → reject. This makes ESSENCE's understate-by-default the
   *rational* strategy: a lower claim faces an easier bar.
3. **Quote-then-grade, with `*verbatim*` = testimony and paraphrase = inadmissible-as-proof
   hearsay.** No quote, no case. The guardian reads modality off the *words* (`could` vs `should`),
   never the agent's framing. This operationalizes 602's modality-catch as an evidentiary rule.
4. **The existing `GuardianRejectionReason` enum becomes a closed critical-question checklist** with
   a Dung-style verdict rule: admit iff every question clears and no live record mounts an
   undefeated attack; any single failure → reject, naming the ground. The binary verdict stays but
   becomes auditable, and the reason tells the advocate exactly what to rework.
5. **Cross-record operations are motions under rebuttable precedent** — *distinguish* (coexist,
   preferred) before *supersede* (overrule, heavier burden), with typed citation signals.
6. **Stakes never raise the burden.** The one place law and Spirit *diverge* and the most dangerous
   import to sever: importance is argued from a separate evidence class (recurrence / blast-radius),
   and the guardian is *forbidden* from demanding stronger grounds because importance is high.

## The mapping

| Spirit | Court | What it gives |
|---|---|---|
| the submission | an argued brief to a motion judge | "make a case," not "attach a reason" |
| the submitting agent | advocate **and** honest broker (duty of candor, not a hired gun) | thinking stays in the agent; argue the record, not beyond it |
| the proposed `Entry` | the relief sought / the narrow rule asked for | brief and admitted record are provably the same proposition |
| `*verbatim*` quotes | sworn testimony / party admissions | the only verification-grade evidence; carries modality |
| agent narrative / context | the statement of facts (hearsay-grade) | scopes a bare *yes*; never load-bearing |
| **certainty** | **the standard of proof the testimony must clear** | over-claim fails its burden → reject |
| importance | the stakes / materiality (decoupled) | argued from recurrence/blast-radius, never from confident tone |
| the guardian | a single reasoned-but-**binary** motion judge | judges the record before it; reject = denial-without-prejudice |
| `GuardianRejectionReason` | the closed list of named grounds for denial | auditable verdict; says which element failed |
| existing records | precedent under **rebuttable** stare decisis | stable-by-default data, never binds the psyche |
| cross-record ops | post-judgment motions (overrule/distinguish/vacate/amend) | corpus rewrites are pleaded, named, burden-bearing |
| the verdict | met / not-met (non-liquet: insufficient proof *is* the loss) | no graduated remedy — never admit-at-lower-certainty |

## The structured Justification

Replace `Justification { statement_text, context }` with a CRAC/Toulmin-fused brief of typed slots
(load-bearing ones mandatory; ceremony terse when testimony plainly equals the claim):

1. **Claim** — the relief sought (the proposed `Entry`), led with.
2. **Testimony** `Vec<VerbatimQuote>` — the grounds: psyche spans in `*asterisks*`,
   recorded-not-reconstructed, **mandatory** for any non-Minimum certainty. Each quote carries its
   scoping **antecedent** (the prior statement it answers) so a bare *yes* is admissible.
3. **Context** `StatementText` — statement-of-facts narrative; foundation, never proof.
4. **Warrant / Application** `StatementText` — **the load-bearing section the current schema
   entirely lacks.** Maps the quoted words to each judged field element-by-element: why *this*
   domain, *this* kind, *this* certainty (cite the modal cue, derive the level), *this* importance.
   A justification that quotes but never applies is evidence-without-argument → fail.
5. **Qualifier-basis** — certainty argued against its standard of proof, one sentence.
6. **Stakes-basis** — importance argued in a *separate* sentence from a *different* evidence class,
   so the guardian can reject importance-mismatch while accepting certainty (or vice versa).
7. **Citations** `Vec<(RecordIdentifier, CitationSignal)>` — typed signals
   {Supports, Distinguishes, Contradicts, Background}: declared relationships, not inferred.
8. **Motion** `Option<CrossRecordMotion>` — the optional cross-record operation, pleaded with its
   own burden.

NOTA shape (positional, asterisks embed escape-free):
```
(Justification
  (Claim ...)
  (Testimony [(Quote [*we are going with random hashes*] (Antecedent [should we seed or randomize?]))])
  (Context [...narrative...])
  (Warrant [...field-by-field mapping...])
  (QualifierBasis [...]) (StakesBasis [...])
  (Citations [(oj3i Supports) (kr1v Distinguishes)])
  (Motion (Supersede [2590 oj3i] ...)))
```
The slots are a discipline for the agent's prose and the guardian's checklist — **the psyche never
sees a form**, and the brief stays dense (clarity-first, no legal theater).

## Certainty as standard of proof

Map the 8-level Magnitude onto a ladder of named burdens, anchored on **modal strength** of the
quoted words (the claimed magnitude *proposes* the standard; the testimony must clear it):

| Certainty | Standard | Clears on testimony like |
|---|---|---|
| Zero | — (removal-candidate sentinel, off the ladder) | — |
| Minimum / VeryLow / Low | scintilla → preponderance | `*maybe*`, `*I think*`, `*I feel like*`, `*could*`, `*we might*` — hedged words **pass here** (admitted *as tentative intent*) |
| Medium | preponderance → clear-and-convincing | `*should*`, `*ought*`, a clear stated preference |
| High | clear-and-convincing | `*we are going with X*`, a flat committing assertion, `*the rule is X*` |
| VeryHigh / Maximum | beyond reasonable doubt (rare) | `*never*`, `*always*`, `*non-negotiable*`, `*put this in essence*` — unmodalized, explicitly elevated |

**Fails its burden → reject** when the asserted certainty *outruns* the modal strength of the words
(High claimed on `*I think maybe*`), or rests on paraphrase rather than a direct quote (you can't
reach VeryHigh on hearsay). Remedy is **remand**: re-file at the rung the words support. The
guardian **never silently downgrades** the magnitude (603 — the judge rewriting the complaint). The
percentages (~54/73/90%) are *ordinal calibration intuition for an LLM reading modality, never
numeric gates.*

## The guardian's protocol — a closed checklist, binary verdict

A single reasoned-but-binary motion judge runs a fixed checklist (each ≈ a `GuardianRejectionReason`
variant); a case dies at the first unmet element:

- **A. Production** — is there ≥1 `*verbatim*` quote, or is it pure paraphrase? No testimony →
  directed reject (the structural defense against agent-fabricated intent).
- **B. Justification-justifies-intent** — do the words, via the Warrant, support recording *this*;
  is it durable intent (not task-state → `NonIntent`); one proposition (not `Compound`)?
- **C. Domain** right (`UnclearDomain`)?
- **D. Certainty vs standard of proof** — does the verbatim clear the claimed burden? (modality read
  off the *quote*, never the framing; never silently lowered).
- **E. Importance** — matched by its *own* recurrence/blast-radius evidence, judged **independently**
  of certainty. The guardian is **forbidden** from demanding stronger grounds because importance is
  high.
- **F. Privacy** clear (`UnclearPrivacy`)?
- **G. Consistency** — does any live record `Contradict` or already `Duplicate` this?
- **H. Motion soundness** — if a cross-record op is pleaded, is it well-founded
  (`ClarifyTramples` / `ClarifyLosesMeaning` / `SupersedeTargetMissing`)? Unsound motion → reject the
  whole case; re-file without it.

Because Spirit is **inquisitorial (no opposing counsel)**, the guardian must *internalize the
skeptic*: actively hunt the competing reading of a quote, the over-broad merge, the hedge that caps
the standard — no adversary will raise them. Temperature 0; reason set and verdict grammar generated
from the enum into the prompt.

## Verbatim = testimony (the evidentiary rules)

1. **No quote, no case** — paraphrase when the utterance was available is a best-evidence violation;
   inference laundered into asterisks is *fabricated testimony* (its own nameable defect).
2. **The quote carries modality, the paraphrase does not** — an advocate can't earn VeryHigh by
   *asserting* the psyche was emphatic; the words must show it.
3. **Quotes need scope** — a bare `*yes*`/`*do it*` is inadmissible until paired with its antecedent.
4. **Separate the psyche's words from the agent's wrapper** — only what's inside asterisks carries
   psyche commitment.
5. **Source strength caps reachable certainty** — direct committing quote → can reach Maximum; hedged
   → capped mid-ladder; paraphrase → capped low. Quoting the load-bearing clause is what *licenses*
   high certainty.

## Cross-record operations = motions

Records are precedent under **rebuttable** stare decisis (stable-by-default, but the psyche is
sovereign and supersedes at will — a default-stability heuristic, **not** the legal thumb-on-the-scale
against change, which the no-backward-compat override forbids). The mover bears a burden that scales
with destructiveness:

- **Distinguish** (the narrow move, preferred) — cite X, argue materially-different scope, both
  coexist. No retirement.
- **Supersede / Overrule** (`Supersession`) — displace X,Y,Z. Heavier burden: (a) cite the targets as
  genuinely on-point and covered (no riding the new record's strength to sweep unrelated ones); (b)
  show the replacement loses no material meaning (preserve the kernel); (c) **for psyche records,
  quote a psyche statement authorizing the change — agent reasoning alone cannot retire psyche
  intent** (psyche supremacy overrides the metaphor).
- **Clarify-amend** (`Clarification`) — make the prior arrow clearer, never overwrite its meaning.
- **Retire / Vacate** (`Retirement`) — a bare changed-mind motion; no successor required.

Importance bumps ride on the motion as consolidated relief (the agglomeration case: many Low → one
High), scrutinized as a consolidation argument, not a free bump. The guardian rules on the **whole
motion as one verdict**.

## Where the metaphor breaks (guardrails)

The research was emphatic — import the skeleton, not the litigation:

- **No adversary.** One advocate + a judge, no opposing counsel. Don't build a fake opposing
  argument; the guardian internalizes the skeptic.
- **Stakes must NOT raise the burden.** The dangerous import. Sever it explicitly or certainty⊥
  importance breaks.
- **No graduated remedy.** The guardian never admits-at-lower-certainty (judge rewriting the claim);
  reject = remand, downgrade stays with the agent.
- **Precedent is mutable by design.** Superseding is normal here; the "overruling" bar is about not
  *losing substance*, not institutional reluctance.
- **Percentages are metaphor, not math.** No numeric thresholds to compute; an LLM reading modality,
  not a Bayesian.
- **Certainty = the intent's settled-ness, not the evidence's strength.** A psyche can be unequivocal
  *about* a tentative idea (`*I'm definitely just exploring this*`) — high-confidence testimony of a
  low-certainty intent.
- **Psyche supremacy overrides the whole metaphor** — a prior record can never overrule a fresh,
  clear psyche statement; only the psyche supersedes psyche intent.

## Open questions — for the psyche to rule on

1. **Verbatim syntax** — `*asterisks*` (already leaned/ratified). Confirm it's final.
2. **Typed vs free-text justification** — fully typed NOTA sub-fields (Claim/Testimony/Warrant/…), or
   one richer free-text the agent self-structures and the guardian checks in-prompt? *Lean: typed
   (auditable, matches schema-emitted-nouns), with terse Warrant allowed on self-evident captures.*
3. **Add a `TestimonyFabricated` rejection reason** (inference laundered into asterisks), or fold into
   `NonIntent`? *Lean: add it — specific, common, catchable (same case as `Overstated`).*
4. **Distinguish** — a new cross-record verb, or just a `Propose` carrying a `Distinguishes` citation
   signal? *Lean: citation-signal, no new verb.*
5. **Citation signals** — confirm the set {Supports, Distinguishes, Contradicts, Background} as a
   field on Justification.
6. **Warrant terseness threshold** — how terse may the field-by-field application be on a self-evident
   capture before the guardian treats it as missing? Needs a worked threshold in the guardian's
   few-shot block.
7. **Decision journal** — confirm the guardian's append-only journal stores
   `(testimony, context, verdict, reason)` tuples as precedent, fed back as retrieval-augmented
   few-shot (the citation-signal idea applied to the guardian's own history).

## Implementation

This is a real `signal`-schema + guardian evolution: the `Justification` type grows from two fields
to the structured brief, the guardian prompt gains the checklist + standard-of-proof ladder + the
internalized-skeptic instruction, and the cross-record motions wire to the existing
Supersede/Clarify/Retire/ChangeRecord verbs. It is a **workflow-sized implementation** once the
design is blessed — schema change, regeneration, guardian-prompt rewrite, and the live-DeepSeek
scenario suite. The psyche rules on the seven questions first.

## Net

The capture path becomes a court: the agent files an argued brief grounded in `*asterisk*`-quoted
testimony; the claimed certainty *is* the burden that testimony must clear; importance is the
orthogonal stakes axis that never moves the burden; cross-record edits are motions against
rebuttable precedent; and the guardian is a single reasoned-but-binary judge that walks a closed
checklist of named defeats and either admits or remands the whole case for re-pleading — never
silently editing a magnitude. It gives the most important subsystem in the design a principled,
auditable, reproducible decision rule — which is exactly what intent, the thing everything revolves
around, deserves.
