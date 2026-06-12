# Intent-capture design — my doubts, best questions, and the load-bearing parts

The psyche asked for my greatest uncertainties, doubts, and the parts that most need to be
well-engineered. Honest critique of the court-of-law design (604/605), including against itself.

## Doubt 1 (deepest): the foundation is the part we deferred — authentication

The whole design is an *evidentiary* system, and the first move in evidence law is **authentication**
(FRE 901): you must prove the exhibit is what you claim. We deferred exactly that — the guardian
can't check the `*verbatim*` against the real conversation. Consequences:

- The design disciplines an **honest** agent beautifully (a scaffold for faithful capture) but does
  **not defend against a careless or adversarial one** — fabricated-but-plausible testimony passes,
  and `TestimonyFabricated` is heuristic-only.
- Sharpest corollary: **psyche supremacy** — only a psyche quote may retire psyche intent, protecting
  the most precious data — is enforced by the **least verifiable** evidence. The lock is strong; the
  door is open.

So I suspect the **priority is inverted**: building the verbatim-verification infrastructure (the
guardian sees the actual conversation, or at least the source is retained so a quote *can* be
checked) may matter more than the elaborate justification structure. The structure is a beautiful
courtroom; authentication is whether the evidence is real.

## Doubt 2: the judge is weaker than the advocate

For an adversarial gate to work, the judge should be **at least as capable as the advocate**. We
have it backwards: frontier-model agents write the briefs; a small fast model (`deepseek-v4-flash`)
judges them. A weak judge under a strong advocate is precisely how persuasive-but-wrong cases get
admitted — and we are making the brief *longer* (the structured case), which the 2025 research says
degrades LLM judges further. We may be simultaneously weakening the judge's input and keeping the
judge weak. The guardian's **adversarial duties** (catch fabrication, internalize the skeptic) in
particular probably need a model as strong as the agent.

## Doubt 3 (against my own design): is the full court worth its cost?

The failure mode was simple — `could` → `should` at high certainty. The minimal fix is:
**quote verbatim + check certainty against the quote's modality + binary verdict.** That is maybe
20% of the design. The other 80% (the Warrant slot, StakesBasis, motions-as-precedent, the
standard-of-proof ladder) is elegant — but the psyche warns against bloat, the research warns LLM
judges degrade on long inputs, and capture friction risks under-capture (Doubt 6). I genuinely don't
know the full structure pays for itself. My instinct: **ship the lean core first, measure where it
actually fails, add structure only there.** Build the cathedral only if the chapel proves
insufficient. I'd rather voice this than let elegance outrun evidence.

## Doubt 4: modality is harder to read than the ladder pretends

`could` vs `should` is a clean story, but real commitment lives in tone, repetition, what is *not*
hedged, follow-through, and the psyche's personal **idiolect** (some people say "maybe" meaning
"definitely"). The guardian reads isolated quotes without the psyche's style or the full
conversation; the ladder will misfire both directions. The guardian probably needs to **learn the
psyche's hedging style over time** (from the decision journal), not apply a universal ladder.

## Doubt 5: retrieval is the shaky ground under the courtroom

The Consistency / Duplicate / precedent checks all depend on the guardian *retrieving* the relevant
existing records — and we know retrieval is weak (the `GUARDIAN_RECORD_LIMIT = 64` cap and the
relevance scoring flagged early this session, never fixed). A judge with incomplete evidence rules
wrong no matter how good its reasoning. The corpus rebuild helped (clean domains → better
retrieval), but the cap and scoring still stand. **Retrieval quality may matter more than the
brief's structure.**

## Doubt 6: guarding it heavily vs. keeping it captured

Intent is the most precious data, so we guard it — but every capture now costs an elaborate brief +
an LLM verdict. If capture gets expensive or slow, agents capture **less**, and the most-important
data thins out. **Over-guarding can starve the thing it protects.** Faithful capture must stay the
path of least resistance.

## Lesser uncertainty: do certainty and importance actually stay orthogonal?

We insist they're independent, but a psyche's repeated attention drives importance *and* tends to
correlate with conviction; and "promote certainty by repetition" actively couples them. They may be
cleaner in theory than in the data — worth watching, not yet a flaw.

## The parts that most need to be well-engineered (in order)

1. **Verbatim authentication** — the foundation everything rests on. Even a minimal version (retain
   the source utterance so a quote *can* be verified later) changes the security story.
2. **The guardian's capability + the modality judgment** — the core decision, currently underpowered
   (flash model) and reading a hard, idiolect-dependent signal. Make the judge ≥ the advocate at
   least for the adversarial checks; let it learn the psyche's hedging style.
3. **Retrieval** — the evidence-gathering the verdict depends on. Fix the cap / relevance scoring.
4. **Low capture friction** — keep faithful capture the easy path; don't starve the corpus.
5. **The structured justification itself** — important, but *downstream* of the four above. Worth
   building lean first.

## My best questions for the psyche

1. **Invert the priority?** Build verbatim-verification (guardian sees the conversation, or the
   source is retained and checkable) *before* the elaborate justification structure — since the
   structure without authentication is a lock on an open door, and the thing we most want to protect
   rests on the weakest link.
2. **Make the judge ≥ the advocate?** A stronger guardian model — at minimum for the adversarial
   parts (fabrication, the skeptic role) — rather than a flash judge under a frontier advocate.
3. **Lean core first?** Ship `verbatim + modality-check + binary`, measure where it fails, and add
   the court structure only there — rather than building the whole courtroom up front.
4. **Idiolect-aware modality?** Should the guardian learn how *this* psyche hedges (from the decision
   journal) instead of a universal ladder?
5. **Fix retrieval as a prerequisite?** The verdict's consistency/precedent checks are only as good
   as what the guardian retrieves, and that layer is still weak.

## Net

The design is sound *as a discipline for honest capture* and gives the verdict a principled,
auditable rule. My real worry is that its **security** rests on unauthenticated evidence judged by an
underpowered judge over possibly-weak retrieval — and that its elegance may be running ahead of the
simple thing that actually fixes the failure mode. The most important engineering is the
foundation we deferred (authentication) and the judge we under-resourced (model + retrieval), not
the courtroom we designed.
