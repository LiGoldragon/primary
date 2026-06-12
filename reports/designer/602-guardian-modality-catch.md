# The over-confident-capture problem, and the guardian as structural double-catch

The psyche caught an agent recording *"I feel like that same schema **could** be used to emit most
of the client side"* as the claim *"schema-derived signal contracts **should** emit most
client-side machinery."* Two distortions in one capture: **`could` → `should`** (a lean turned
into a directive) and **a feeling stated as a fact** (hedge stripped). This is the canonical bad
capture. Captured firmly this session: `woku` (the guardian must catch over-stated capture and
preserve modality), `u62s` (certainty and importance are orthogonal).

## Two layers, and why one isn't enough

- **Agent training.** The intent-capture skill should teach: quote, don't paraphrase the modality;
  distinguish a lean from a decision; set certainty from the *source's* confidence; never upgrade
  `could`/`maybe`/`I think`/`I feel like` into `should`/`must`. Necessary — but **not
  sufficient**, and the psyche named exactly why: *agents forget; context gets compacted.* A rule
  the agent read 200k tokens ago is gone. Training degrades within a session.
- **The guardian.** A stateless, per-record check that re-runs fresh every time, with no context
  decay. This is the structural **double-catch**: it doesn't matter that the capturing agent
  drifted, because a second mechanism that never drifts verifies every write. **Structural
  verification beats trusting agent judgment** precisely because agent judgment is the thing that
  degrades.

## The mechanism

1. **Capture must carry the psyche's actual wording.** The `Justification` already has a
   `StatementText` field — make it carry the psyche's *verbatim* (or faithfully-quoted) words, not
   the agent's paraphrase. The distilled record is the arrow; the justification is the *evidence*,
   and the guardian needs the evidence to judge faithfulness. (The exact form — full verbatim vs.
   a faithful quote of the load-bearing clause — is the psyche's call; the principle that the
   guardian must *see the real wording* is firm.)

2. **The guardian checks modality-faithfulness.** Given the record (with its certainty) + the
   verbatim source, it asks: *does the asserted confidence match the source?* If the source hedges
   (`could`, `maybe`, `I think`, `I feel like`) but the record asserts at High/Maximum certainty
   with imperative wording, that's a mismatch. The guardian's verdict becomes one of:
   - **Reject** — the source doesn't qualify as durable intent at all (a passing musing). Existing
     `NonIntent` covers part of this; a precise new reason like **`Overstated`** names the
     modality mismatch specifically.
   - **Admit at forced-low certainty** — the source is a real but tentative arrow, so it goes in at
     **Low/VeryLow certainty**, not the confident level the agent proposed. (This needs a new
     guardian power: returning a *corrected* certainty, not just accept/reject. Worth adding — it's
     the psyche's "this should at least be very low certainty" case.)

3. **Certainty tracks the source's modality; importance does not.** `u62s`: a tentative idea can be
   **VeryLow certainty but High importance** — not decided, but it matters. The guardian lowers
   *certainty* on a hedge; it must **not** touch importance. This is the same orthogonality the
   merge simulation just surfaced from the other side (importance earned by repetition, independent
   of how settled each statement was).

## How it reads end to end

> psyche: "I feel like that schema could emit most of the client side"
> agent distills → record `[schema could emit most client CLI machinery]`, and the guardian sees
> the verbatim. It catches `could` + `I feel like` → **admits at VeryLow certainty, High
> importance**, not as a `should`. The arrow is preserved (it matters), but the store now honestly
> says "the psyche floated this; not decided" instead of fabricating a ratified directive.

That record would then be a perfect candidate to *rise in certainty later* — if the psyche keeps
returning to it (the conviction signal), a future pass promotes it from VeryLow toward a decision.
Capture-time honesty + repetition-driven promotion is the whole loop.

## Decisions for the psyche

1. **Verbatim form** — full verbatim psyche statement in the justification, or a faithful quote of
   the load-bearing clause? (Lean: faithful quote, enough for the guardian to judge modality.)
2. **Guardian power** — reject-only on overstatement, or also **admit-at-corrected-certainty**?
   (Lean: both — reject non-intent, force-low-certainty borderline. The corrected-certainty verdict
   is new guardian capability worth building.)
3. **New rejection reason `Overstated`** (distinct from `NonIntent`)? (Lean: yes — it's a specific,
   common, catchable failure.)
4. **Agent-side** — update the intent-capture skill with the modality rules, as the first line; the
   guardian is the second. Both, not either.

## Net

The fix is two-layered and the layers do different jobs: train the agent to capture honestly, and
**back it with a guardian that re-checks every write against the psyche's actual wording** — because
the agent forgets and the guardian doesn't. Certainty becomes a faithful readout of how settled the
psyche was; importance stays free to be high on a tentative-but-load-bearing idea. The corpus stops
fabricating conviction the psyche never expressed.
