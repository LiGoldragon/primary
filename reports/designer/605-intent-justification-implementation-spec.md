# Intent justification upgrade — implementation spec (for operator)

The operator-facing constraints + design for the court-of-law justification and guardian upgrade.
Hand this to operator to implement. The full design rationale is report **604**; this report is the
**spec**: what to build, what not to build, the typed schema, the guardian-prompt contract, tests,
and references. Ratified by the psyche (`so3b`, `ans1`, `z3ka`, `woku`, `ll41`, `7xnx`, `u62s`,
`i59i`).

## The shape in one paragraph

The capture path becomes a court of law. The submitting agent files an **argued case** (the
upgraded `Justification`) for its proposed record. The case rests on the psyche's **verbatim
quotes** (testimony, marked `*asterisks*`). The **claimed certainty is the burden of proof** that
testimony must clear on its modal strength — over-claim fails and is rejected. **Importance is a
separate axis** argued from different evidence and never raises the burden. The **guardian is a
single, strictly binary judge** that walks a closed checklist of named defeaters and either admits
or remands the whole case for re-pleading — it never silently edits a magnitude. Everything is
**strongly typed**; nothing stringly-typed.

## Hard constraints — what we WANT

1. **Strongly typed, end to end.** This is the headline constraint, per the psyche and the domain
   fiasco (reports 593/595): no `String` where a typed sum belongs. The `Justification` becomes a
   typed structured record with named sub-fields. Magnitudes stay the typed `Magnitude` enum; Kind,
   Domain (recursive enum), and the cross-record operation stay typed. The verdict's rejection set
   is the typed `GuardianRejectionReason` enum. (Genuinely-textual fields — the verbatim quote, the
   argument prose — are correctly `StatementText`; that is *not* stringly-typing. The sin is a
   `String` standing in for an enum, not text being text.)
2. **The argued-case `Justification` is structured.** Four typed slots (below). The current
   `{ StatementText, context }` is replaced.
3. **Certainty = burden of proof.** The guardian checks the verbatim clears the claimed certainty
   rung, read off modal strength. This is a **guardian-prompt discipline**, ordinal, *not* numeric
   gates.
4. **Binary verdict only.** Admit or reject. The guardian never lowers a magnitude itself (`woku`);
   a reject is a remand that sends the agent back to re-plead.
5. **Verbatim = testimony.** No quote, no case; the quote carries modality; a bare `*yes*` needs its
   antecedent; source strength caps reachable certainty.
6. **Stakes never raise the burden.** Importance is argued from its own evidence (recurrence /
   blast-radius) in a separate slot; the guardian is forbidden from demanding stronger grounds
   because importance is high. This keeps certainty ⊥ importance true in practice (`u62s`).
7. **Cross-record operations stay the existing typed verbs** (`Supersede`, `Clarify`, `Retire`,
   `ChangeRecord`) — the operation *is* the motion; the `Justification` argues for it. **Psyche
   supremacy:** retiring a psyche record requires a verbatim psyche quote authorizing it; agent
   reasoning alone cannot.
8. **Keep it dense.** Recent evidence (arXiv 2509.15739, 2025) shows LLM judges degrade on long /
   disrupted inputs. The slots are a discipline for the agent's prose and the guardian's checklist,
   not an invitation to bloat — the psyche never sees a form.

## What we DON'T want

1. **No stringly-typed types.** No `String` for domains, kinds, magnitudes, operations, rejection
   reasons, or relationships. The domain fiasco is the precedent: a `(Vec String)` scope that a typo
   parsed fine. Never again.
2. **No citation-signal enum, no `Distinguish` verb.** Cut as redundant (psyche). A cited record's
   relationship is carried by the operation (if you're changing it) or the Warrant prose (if you're
   only referencing it). Do not add `{Supports, Distinguishes, Contradicts, Background}`.
3. **No graduated guardian remedy.** No admit-at-corrected-certainty (`woku`). The downgrade stays
   in the agent's hands.
4. **No numeric certainty thresholds.** The standard-of-proof percentages (50.1 / 73.4 / 90.1, Duke
   *Judicature*) are ordinal calibration intuition for an LLM reading modality — never a number the
   guardian computes.
5. **No hand-rolled NOTA parsing.** The new `Justification` types are schema-emitted with the derived
   NOTA codec (per record `884` / `skills/rust/parsers.md`). The `*asterisks*` are inline markers the
   guardian LLM reads inside text fields — not a structure the daemon parses. No bespoke walker.
6. **No fabricated authentication.** We do **not** have infrastructure for the guardian to fetch the
   real conversation, so `TestimonyFabricated` is a **heuristic-only** catch for now (obvious
   agent-prose-shaped or suspiciously-perfect quotes). The verifiable version waits on giving the
   guardian the source prompt — a good future design, explicitly deferred.

## The typed schema (signal.schema)

Replace `Justification { StatementText * context (Optional StatementText) }` with:

```
Justification {
  Testimony *                                  ;; the grounds — the psyche's verbatim words
  Context *                                    ;; statement of facts: what was discussed/proposed/conceded
  Warrant *                                    ;; THE load-bearing slot: maps the testimony to each
                                               ;; Entry field (domain, kind, certainty) element-by-element,
                                               ;; and argues operation soundness when records are touched
  StakesBasis *                                ;; importance argued from its OWN evidence (recurrence/
                                               ;; blast-radius), separate from the verbatim
}
Testimony   (Vec VerbatimQuote)
VerbatimQuote { QuoteText * antecedent (Optional StatementText) }
QuoteText    StatementText                     ;; the psyche's exact words, *asterisks* preserved
Context      StatementText
Warrant      StatementText
StakesBasis  StatementText
```

Notes for operator:
- The **claim** is the proposed `Entry` already carried on the gated op (`RecordRequest { Entry,
  Justification }`, `Supersession { retired_identifiers, replacement, Justification }`, etc.) — the
  `Justification` does **not** re-declare it. The Warrant references the Entry's fields.
- A `VerbatimQuote` with no `antecedent` is a self-contained quote; a bare affirmation (`*yes*`,
  `*do it*`) **must** carry its `antecedent` or the guardian rejects it (the bare-yes-needs-its-question
  rule).
- `Justification` is used by every gated op (`Record`, `Propose`, `Clarify`, `Supersede`, `Retire`,
  `ChangeRecord`, `RegisterReferent`). The schema change ripples to all of them — expected,
  pre-production, break them all at once (no backward-compat).
- Add **`TestimonyFabricated`** to `GuardianRejectionReason` (heuristic catch; sibling of the
  to-be-added `Overstated` from report 602). Regenerate via `schema-rust-next`; the
  `generated-schema-source-checked-in` flake check must stay green.

## The guardian-prompt contract

The guardian (`guardian_prompt.rs`) is rewritten to judge the argued case. Temperature 0. The
verdict grammar and the closed reason set are generated from the `GuardianRejectionReason` enum into
the prompt (no free-text verdicts). The judge runs a fixed checklist; **a case dies at the first
unmet element** (directed-verdict gates); admit iff every question clears and no live record mounts
an undefeated attack:

- **A. Production** — ≥1 `*verbatim*` quote, or pure paraphrase/inference? None → reject
  (`RetrievalInsufficient` / `NonIntent`). Inference laundered into asterisks → `TestimonyFabricated`
  (heuristic: reads like agent-prose, or is suspiciously exact for the claim).
- **B. Justification-justifies-intent** — do the quoted words, via the Warrant, support recording
  *this*; durable intent not task-state (`NonIntent`); single proposition not several (`Compound`)?
- **C. Domain** right (`UnclearDomain`)?
- **D. Certainty vs standard of proof** — does the verbatim clear the claimed certainty's burden,
  read off modal strength (the ladder below)? Over-claim → reject. Modality read off the *quote*,
  never the agent's framing; never silently lowered.
- **E. Importance** — matched by its own recurrence/blast-radius evidence in `StakesBasis`, judged
  *independently* of certainty. The guardian is **forbidden** from demanding stronger grounds because
  importance is high.
- **F. Privacy** clear (`UnclearPrivacy`)?
- **G. Consistency** — any live record `Contradict`s or `Duplicate`s this?
- **H. Operation soundness** — if the op touches records, are the targets genuinely on-point, the
  kernel preserved, and (for psyche records) is there a verbatim psyche quote authorizing retirement?
  (`SupersedeTargetMissing`, `ClarifyTramples`, `ClarifyLosesMeaning`.)

**Internalize the skeptic.** Spirit is inquisitorial — no opposing counsel — so the guardian must
actively hunt the competing reading of a quote, the over-broad merge, the hedge that caps the
standard. No adversary will raise them.

### The standard-of-proof ladder (ordinal, modal-strength)

| Certainty | Standard | Cleared by testimony like |
|---|---|---|
| Zero | (removal sentinel, off-ladder) | — |
| Minimum / VeryLow / Low | scintilla → preponderance | `*maybe*`, `*I think*`, `*I feel like*`, `*could*`, `*might*` (hedged words PASS here, as tentative intent) |
| Medium | preponderance → clear-and-convincing | `*should*`, `*ought*`, a stated preference |
| High | clear-and-convincing | `*we are going with X*`, a flat committing assertion |
| VeryHigh / Maximum | beyond reasonable doubt (rare) | `*never*`, `*always*`, `*non-negotiable*`, `*put this in essence*` |

Fails its burden → **reject** when the claimed certainty outruns the words' modal strength, or rests
on paraphrase not a quote. The percentages anchor the *order*, not a computation.

## Tests (live-DeepSeek scenario suite, `agent-guardian` feature)

Extend `tests/guardian_live_scenarios.rs`:
- **Over-claim rejected** — High certainty on `*I think maybe*` testimony → reject (failed burden).
- **Honest lean admitted** — the same words claimed at Low certainty → admit at Low.
- **No-quote rejected** — a case of pure agent paraphrase → reject (production).
- **Fabrication caught (heuristic)** — agent-prose-shaped "quote" supporting a convenient claim →
  `TestimonyFabricated`.
- **Stakes don't raise burden** — VeryLow-certainty / High-importance tentative-but-grave idea →
  admit (importance high, certainty low, both honest).
- **Bare yes needs antecedent** — `*yes*` with no antecedent → reject; with antecedent → admit.
- **Supersede needs psyche authorization** — agent-reasoned retirement of a psyche record with no
  authorizing quote → reject; with a `*let's drop X*` quote → admit.
- **Round-trip** — the typed `Justification` NOTA encodes/decodes via the derived codec.

## References

**Workspace (current):**
- Design + rationale: report **604** (court mapping, where the metaphor breaks). Modality catch: **602**.
- Ratified records: `i59i` (intent is paramount), `woku` (binary guardian), `ll41` (argued
  justification), `7xnx` (multi-dimensional judgment), `u62s` (certainty ⊥ importance), `z3ka` (court
  model), `so3b` (certainty = burden of proof), `ans1` (typed justification, no stringly-typed).
- Discipline (the typed constraint): `skills/rust-discipline.md` + `rust/` (typed-domain-values,
  typed per-crate `Error`, **no hand-rolled parsers**, schema-emitted nouns), `skills/abstractions.md`,
  record `884`. The cautionary precedent: the stringly-typed `DomainScope` → recursive-enum
  correction (reports **593**, **595**).
- Code touched: `schema/signal.schema` (`Justification`, `GuardianRejectionReason`, the gated ops),
  `src/guardian.rs` / `src/guardian_prompt.rs` (the prompt + verdict), `src/store.rs` (the guardian
  journal — store `(testimony, context, verdict, reason)` tuples as precedent), `spirit/ARCHITECTURE.md`.

**External (verified, current):**
- Argument structure: Toulmin, *The Uses of Argument* (1958) — claim/grounds/warrant/qualifier/
  rebuttal/backing (the Warrant slot is his "warrant"). Walton, Reed & Macagno, *Argumentation
  Schemes* (2008) — schemes + **critical questions** (the defeasible checklist model).
- Critical discussion: van Eemeren & Grootendorst, pragma-dialectics (*A Systematic Theory of
  Argumentation*, 2004) — rules for resolving a difference of opinion (the remand/re-plead loop).
- Computational adjudication: Dung (1995), "On the acceptability of arguments…," *Artificial
  Intelligence* — abstract argumentation frameworks (admit iff conflict-free and defends itself —
  the "no undefeated attack" verdict rule).
- Standards of proof: "Legal Standards By The Numbers," *Judicature* (Duke) — preponderance 50.1 %,
  clear-and-convincing 73.4 %, beyond-reasonable-doubt 90.1 % (ordinal anchor only).
- Evidence: U.S. Federal Rules of Evidence — 901 (authentication; the deferred verbatim-verification
  end-state), 1002 (best evidence; "no quote when the utterance was available"), 801–802 (hearsay;
  paraphrase is not load-bearing proof).
- Modality: Palmer, *Mood and Modality* (2001); Aikhenvald, *Evidentiality* (2004) — grading
  `could`/`should`/`must`, the linguistic basis for reading certainty off the words.
- AI & Law CBR: Rissland & Ashley (HYPO), Aleven & Ashley (CATO) — precedent/factor-based reasoning
  (records-as-precedent, distinguishing).
- Current LLM-judge work (2025): "Can LLMs Judge Debates? … Argumentation Theory Semantics"
  (arXiv 2509.15739) — **LLM judging degrades on long/disrupted inputs → keep justifications dense**;
  "A Law Reasoning Benchmark for LLM with Tree-Organized Structures (Factum Probandum, Evidence…)"
  (arXiv 2503.00841) — structured claim+evidence law reasoning; "Opportunities and Challenges of
  LLM-as-a-Judge" (EMNLP 2025).

## Implementation sequence (operator)

1. `signal.schema`: replace `Justification`, add `VerbatimQuote`/`QuoteText`/`Context`/`Warrant`/
   `StakesBasis`, add `TestimonyFabricated` (and `Overstated`, 602) to `GuardianRejectionReason`.
2. Regenerate via `schema-rust-next`; keep `generated-schema-source-checked-in` green.
3. Update every gated-op construction site for the new `Justification` shape (break all consumers).
4. Rewrite `guardian_prompt.rs`: the checklist, the standard-of-proof ladder, the internalized
   skeptic, the generated reason-set/verdict grammar; store the argued case in the journal.
5. Extend `tests/guardian_live_scenarios.rs` (above). `cargo test`, `cargo clippy -D warnings`,
   `nix build`, the live-DeepSeek suite.
6. Deploy via the CriomOS-home spirit pin + activation (as in this session's 0.9.5 deploy).

## Net

The most important subsystem in the design gets a principled, auditable, reproducible decision rule
drawn from how humans have argued toward justified verdicts for centuries — strongly typed,
binary-gated, verbatim-grounded, with certainty as the burden of proof and importance held free of
it. Build the types first; the prose discipline lives in the guardian prompt; nothing stringly-typed
survives.
