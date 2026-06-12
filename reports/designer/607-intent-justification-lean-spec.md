# Intent justification — lean Phase-1 build spec (for operator)

The psyche ruled: **ship the lean core first** — *"make this simple but on point, at first."* This
narrows the full court design (604/605) to the minimal fix and folds in operator's audit (375). This
is the **build target now**; 604/605 are the Phase-2 design (the cathedral), built only where the
lean core demonstrably falls short. Ratified: `bwqe` (lean-first), `2t89` (guardian specialization),
`4jgt` (clean NOTA), `so3b`, `ans1` (corrected), `woku`, `u62s`.

## The lean core — what we build now

The failure mode was `could` → `should` at high certainty. The minimal fix: **typed verbatim
testimony + a check that the words support the claimed certainty + a binary verdict.** Everything
else waits.

## Typed schema (signal.schema)

Replace `Justification { StatementText, context (Optional) }` with two typed slots:

```
Justification {
  Testimony *                                  ;; the evidence — the psyche's verbatim words
  Reasoning *                                  ;; one prose field: the argued case — why admit, and why
                                               ;; this certainty (modality read off the quote), domain,
                                               ;; kind, and importance
}
Testimony   (Vec VerbatimQuote)
VerbatimQuote { QuoteText * antecedent (Optional StatementText) }
QuoteText    StatementText                     ;; RAW psyche words, NO asterisk delimiters (operator 375 #2)
Reasoning    StatementText
```

- **`QuoteText` stores raw psyche words, not `*asterisks*`** (operator 375 #2). Asterisks are a
  prompt-rendering marker the guardian-prompt composer adds; they are never stored. The daemon
  validates "has testimony" by `Testimony` vector length, never by scanning for `*`.
- The **claim is the operation's `Entry`** (already carried by `RecordRequest`/`Supersession`/etc.),
  **not a `Justification` sub-field** (operator 375 #1 — `ans1` corrected to match).
- A `VerbatimQuote` with no `antecedent` is self-contained; a bare affirmation (`yes`, `do it`)
  **must** carry its antecedent or the guardian rejects it.
- `Reasoning` is one prose field for now (operator 375 #5): the guardian reads it and renders
  per-aspect rejections from the prose. Splitting it into typed per-field sections is Phase 2.

### Rejection reasons — distinct, not overloaded (operator 375 #3)

Add to `GuardianRejectionReason` (generated into the prompt as the closed set):
`MissingTestimony` (no verbatim — an evidentiary production failure, **not** `RetrievalInsufficient`
or `NonIntent`), `InsufficientWarrant` (the reasoning doesn't justify the claim), `Overstated`
(certainty outruns the words' modality), `TestimonyFabricated` (heuristic only — see below),
`ImportanceUnsupported` (importance not justified from its own evidence). Keep the existing ones
(`NonIntent`, `Compound`, `UnclearDomain`, `UnclearPrivacy`, `Duplicate`, `Contradiction`,
`SupersedeTargetMissing`, `ClarifyTramples`, `ClarifyLosesMeaning`, harness errors).

## The guardian — a specialized, clean-context judge

Per the psyche (`2t89`): the guardian is **not** weaker than the advocate. The agent is buried in
noise (messy interaction, code files, accumulated context); the guardian judges **one case at full
attention** with extensive on-point instructions — 100% signal. A well-specialized, well-trained
judge beats a noise-laden generalist even on a nominally weaker model. So:

- **Specialization + clean context + training is the lever, not raw model strength.** Switching to a
  larger-context model (DeepSeek Pro) helps **only when paired with proper training/instructions** —
  the psyche notes a naive swap showed no difference because it wasn't trained for the task.
- **The guardian must always emit well-formed NOTA** (`4jgt`). A malformed response must never
  happen. The exact verdict grammar and the closed rejection-reason set are **generated from the
  enum into the prompt**; add a **parse-and-retry** and a **shape test** so an out-of-format reply is
  impossible in practice. This is a hard correctness requirement, not best-effort.
- **Binary verdict only** (`woku`): admit or reject; the guardian never lowers a magnitude itself; a
  reject is a remand that sends the agent back to re-plead with better evidence or a lesser claim.
- **Temperature 0.** Internalize the skeptic (no opposing counsel): actively hunt the competing
  reading of a quote, the hedge that caps the certainty.

### The lean checklist (a case dies at the first unmet element)

1. **Testimony present?** ≥1 verbatim quote, else `MissingTestimony`. Pure agent paraphrase →
   `TestimonyFabricated` (heuristic: reads like agent-prose, or suspiciously exact for the claim).
2. **Reasoning justifies it?** durable intent not task-state (`NonIntent`), one proposition
   (`Compound`), the reasoning actually supports the claim (`InsufficientWarrant`).
3. **Certainty matches the words?** does the quote's modal strength clear the claimed certainty? Over-
   claim → `Overstated`. Read modality off the **quote**, never the agent's framing; never silently
   lowered. (Ordinal ladder below.)
4. **Domain / Privacy** right (`UnclearDomain` / `UnclearPrivacy`).
5. **Importance** justified from its own (recurrence / blast-radius) evidence, **independently** of
   certainty — never demand stronger grounds because importance is high (`ImportanceUnsupported` if
   unjustified).
6. **Consistency** — any live record `Contradict`s or `Duplicate`s this (the daemon bumps the
   canonical's importance as a mechanical consequence of a `Duplicate` verdict).
7. **Operation soundness** (for `Supersede` / `Retire` / `Clarify` / `ChangeRecord`) — does the
   Reasoning justify retiring or amending the named records; are they genuinely covered
   (`SupersedeTargetMissing`); does the change lose no meaning (`ClarifyTramples` /
   `ClarifyLosesMeaning`); and for psyche records, is there a verbatim psyche quote authorizing
   destruction? "Replace X and Y with this" is the existing `Supersede` verb — **no new mechanism.**

The certainty ladder is **ordinal, modal-strength-anchored, never numeric**: hedged words
(`maybe`, `I think`, `could`) clear only the low rungs; firm commitments (`we are going with X`)
clear High; unhedged founding language (`never`, `non-negotiable`) clears the top, rarely.

## Per-operation prompts — over-trained (`88mw`)

The guardian's instructions are **per-operation**: each gated op (`Record`/`Propose`, `Supersede`,
`Clarify`, `Retire`, `ChangeRecord`, `ChangeCertainty`, `RegisterReferent`) gets detailed guidance
plus worked **accept/reject examples** — the few-shot that "trains" the guardian without weights.
**Over-train first** (rich, concrete, discriminating example pairs — e.g. the same words claimed at
Low certainty = accept vs. at High = reject `Overstated`), then scale back once it works, because
the current guardian calls are undertrained. The example library is being authored (report 608);
operator embeds it in `guardian_prompt.rs` alongside the shared checklist and the exact NOTA verdict
grammar.

## Write-root authority rule (operator 375 #6)

**Rule:** every working-socket operation that changes the live intent corpus is **guardian-gated**,
unless it is a **purely mechanical consequence** of an already-gated verdict. Owner-only meta
`Import` is the explicit **bypass**. Operator enumerates each write root and marks it:

| Root | Class |
|---|---|
| `Record`, `Propose`, `Clarify`, `Supersede`, `Retire`, `ChangeRecord`, `RegisterReferent` | guardian-gated |
| `Remove`, `ChangeCertainty`, `CollectRemovalCandidates` | guardian-gated (intent-changing) |
| `BumpImportance` (as a duplicate consequence) | mechanical |
| meta `Import` | owner-only bypass |

(Operator confirms against the live `OperationKind` set.)

## "Psyche record" definition (operator 375 #7)

For now: **every live working-socket record is psyche-derived.** Destructive retire/supersede
requires a verbatim psyche quote authorizing it (psyche supremacy). If machine-only records ever
enter the live store, add a **typed provenance field** — never infer provenance from path or
operation history.

## The decision journal — replayable (operator 375 #4)

Keep it separate from the live store, but make each entry replayable:
proposed operation + `Entry`; full typed `Justification`; the retrieved live-record bundle (or stable
refs to reconstruct it); verdict + reason + explanation + **raw model output** + parse/retry status;
provider + model + **prompt version** + usage metadata; and any later override. This is the training
flywheel: past decisions become retrieval-augmented few-shot precedent for the guardian — which is
how the guardian gets "trained" without weights.

## Deferred to Phase 2 (the cathedral — design in 604/605)

Build only where the lean core demonstrably falls short: typed per-field `Warrant` sub-sections
(domain/kind/certainty/privacy) for structural per-field rejection; a separate `StakesBasis` slot to
structurally enforce certainty ⊥ importance; and **verbatim authentication** — the guardian
verifying quotes against the real conversation. Authentication is the deepest gap (report 606) but
needs a full-stack capture/UI rewrite that is out of reach now; Spirit must work first. Until then
`TestimonyFabricated` is heuristic-only — pair its live test with a shape test, don't treat it as
authentication (operator 375 #9).

**Cross-record operations are NOT deferred — and need no new mechanism.** "Replace records X and Y
with this one" *is* the existing `Supersede` verb (`Supersession { retired_identifiers, replacement
Entry, Justification }`), judged as one verdict; the lean guardian judges its soundness (checklist
item 7). What was over-framed as "motions as precedent" was only an elaborate motion-type taxonomy
(distinguish vs. overrule, burden-scaling) that — like the cut citation signals — is probably
unnecessary; a plain `Supersede` with a well-argued `Reasoning` does the job. **One required schema change — correctness, not convenience (`gad7`):** `Supersession` must carry
**multiple** replacements (`replacements (Vec Entry)`), not one. If the retired set's content splits
across several new records, replacing it with a single record *loses meaning* and the guardian
*should* refuse it — so the split cannot be done as `Supersede(X,Y → A)` then `Record(B)` (the first
op correctly dies for an insufficient replacement). The atomic multi-replacement supersede — judged
as one verdict on whether the new set *together* preserves the retired set's kernel — is part of the
lean core.

## Tests (live-DeepSeek + shape, `tests/guardian_live_scenarios.rs`)

Over-claim rejected (`Overstated`); honest lean admitted at Low; no-quote rejected
(`MissingTestimony`); fabrication caught (heuristic) **+ a shape test that the reason exists, is in
the closed enum, and parses**; bare-yes-needs-antecedent; stakes-don't-raise-burden; supersede needs
a psyche-authorizing quote; **NOTA-format shape test — the guardian always emits valid NOTA, with
parse-and-retry**; typed `Justification` round-trip via the derived codec.

## References (corrected per operator 375 #8)

Design + rationale: 604, 605; doubts: 606. Records: `bwqe`, `2t89`, `4jgt`, `so3b`, `ans1`, `woku`,
`ll41`, `7xnx`, `u62s`, `i59i`, `z3ka`. Discipline: `skills/rust-discipline.md` + `rust/`
(typed-domain-values, **no hand-rolled parsers**, schema-emitted nouns, typed `Error`),
`skills/abstractions.md`, record `884`; the domain-fiasco precedent (593/595).
External: Toulmin (1958); Walton/Reed/Macagno, *Argumentation Schemes* (2008); van Eemeren &
Grootendorst pragma-dialectics (2004); Dung (1995) AAF; Federal Rules of Evidence 901/1002/801-802;
Palmer *Mood and Modality* (2001), Aikhenvald *Evidentiality* (2004); Rissland/Ashley HYPO,
Aleven/Ashley CATO. Standards of proof — Duke *Judicature*, "Legal Standards By The Numbers":
**survey means 54.4% (preponderance) / 73.4% (clear-and-convincing) / 90.1% (beyond reasonable
doubt)**; 50.1% is the legal-minimum shorthand. Ordinal anchor only — the design forbids numeric
gates. Current LLM-judge work: arXiv 2509.15739 (judges degrade on long inputs → keep it dense),
2503.00841 (structured claim/evidence law reasoning), EMNLP 2025 LLM-as-judge survey.

## Implementation sequence (operator)

1. `signal.schema`: the lean `Justification` (`Testimony`/`Reasoning`/`VerbatimQuote`/`QuoteText`),
   add the five rejection reasons, expand the journal record.
2. Regenerate via `schema-rust-next`; keep `generated-schema-source-checked-in` green.
3. Adapt every gated-op call site (break all consumers — pre-production).
4. Rewrite `guardian_prompt.rs`: the lean checklist, the ordinal ladder, the **exact NOTA verdict
   grammar + closed reason set generated in**, parse-and-retry, internalized skeptic; write the
   replayable journal entry.
5. Classify the write roots; enforce the authority rule.
6. Tests above; `cargo test`, `cargo clippy -D warnings`, `nix build`, the live-DeepSeek suite.
7. Deploy via the CriomOS-home spirit pin + activation (as in this session's 0.9.5 deploy).

## Net

Simple but on point: typed verbatim evidence, one reasoning field, a binary verdict from a
specialized clean-context judge that always speaks valid NOTA. It fixes the actual failure (certainty
inflation) with a fraction of the machinery, keeps capture cheap, and leaves the cathedral fully
designed for when the lean core proves it's needed.
