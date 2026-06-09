# 567 — Spirit's guardian: the design and a grounded review

designer, 2026-06-09. Spirit is the typed intent store: it captures the psyche's
durable intent as records and serves them back to agents. It has a real disease —
it only ever grows, repetition piles up instead of reinforcing, stale intent
keeps surfacing, and a record that says two things rots in pieces. This report
states the design we have arrived at for fixing that (the **guardian**), and
reviews it properly: what is solid, what is genuinely open, and — because a prior
adversarial pass produced confident nonsense — what is *not* actually a problem.

This is design-stage. Operator is bringing the new schema-derived spirit to
parity with the production daemon; nothing here lands until the open decisions
below are settled. Grounding for the prior-art claims came from research workflow
`w9wyyoetz`; the architecture facts here were re-verified directly against the
code (cited inline).

## The four problems

1. **Unbounded growth.** The store only appends; retrieval gets noisier and an
   agent can no longer load "all relevant intent" (today a broad query is
   depth-capped to ~365 of ~1700 records — the concrete bug under the complaint).
2. **Repetition should reinforce, not pile up.** Restating something — even
   reworded — should strengthen the existing record, not add a redundant row.
3. **Deprecation.** Intent goes stale or gets superseded; the store must stop
   surfacing it without losing history — and, on a long enough timeline, must
   physically collect it (Principle `8g9n`: hard deletion is inevitable; design
   it as a deliberate, recoverable-to-a-horizon stage, not a forbidden act).
4. **Compound records go half-stale.** A record touching many things has parts
   that stay valid while others rot. The unit should be one atomic proposition.

## What the psyche has already decided

The decisive grounding result: **this is not a blank slate.** The store already
holds substantial intent toward all four problems. The design must honor it or
have the psyche explicitly supersede it.

| Problem | Already-recorded intent (id — gloss) |
|---|---|
| 1 growth | `q4l0` (lifecycle ladder: nominate/tombstone/archive/collect/compact/**purge**); `sqrk` (adaptive-depth retrieval); `yhn9`/`xni2` (a typed archive store) |
| 2 reinforce | `vbx6` (**certainty ≠ weight**); `9bxr` (weight = recurrence/importance); `g8ln` (weight is a qualitative rung, **"not an integer count"**); `6z6t` (reinforcement raises *weight*, **must not auto-raise certainty**); `u2s9`/`hp3r` (weight flagged **unsettled, not in production**) |
| 3 deprecation | `a3l4` (a **relations field** — the only code change needed); `y0vr` (no composite *type*; a refresh may yield 2-3 records); `qkrg`/`kfxd` (provenance + recoverability before any removal); `ek8w`/`tf2o` (**auditor proposes, psyche confirms each retirement**; judgment is agent behavior, "the only supporting code is the relations field") |
| 4 atomicity | `uara` (topics are atomic single words); `jn99` (split a tangled record so parts separate); `20jk`/`f0wm` (fields vary by kind) |

Empirical proof of the disease: the **560 audit** classified 1706 records — 79%
durable, 11% scratchpad, 10% borderline. The dominant pollution is
working-instructions wearing a Decision costume (105 of 184 scratchpad), with a
mechanically-detectable tell: **target-artifact + action-verb** (`port
orchestrate`, `migrate X to Y`). The audit's own conclusion: pollution
concentrates on active migration fronts, so "the cure is disciplinary" — catch it
*at the door*.

## The design under review: the guardian

The shape the psyche drove: **a small local model guards the gate, the thinking
agent decides, the psyche is the last word.**

- **The store stays simple and is the ground truth.** Every psyche statement is
  captured as an atomic typed record. Nothing is destructively merged; history is
  recoverable to a horizon, then collected (`8g9n`, `q4l0`).
- **The guardian scouts at capture.** When an agent proposes a record, a small
  model (a Gemma on the cluster AI node) finds the related and contradicting
  existing records in the proposal's neighborhood and renders a **typed verdict**.
  It does not curate autonomously and it does not decide — it *flags*.
- **The agent decides; the psyche escalates.** The thinking harness model reads
  the verdict and acts: accept as new, reword, reinforce/relate to an existing
  record, mark a contradicted record for deprecation, or escalate. The psyche is
  the final authority on anything that retires existing intent.

**The authority split is the whole point: the guardian is allowed to be wrong**,
because it only advises. A false flag costs one look. This is precisely the
recorded `ek8w`/`tf2o` auditor model — only moved from a periodic after-the-fact
sweep to a check *at the front door*, which is where the 560 audit says the cure
belongs.

### How it sits in the architecture (verified against the code)

The objection that "a dumb daemon can't return a rich verdict" is a non-issue.
The daemon already *computes* its replies through Nexus: `nexus.rs` composes
`RecordAccepted` from the SEMA write outcome, and `apply_effect`/`run_effect`
already run effects like **`ClassifyState`** (which classifies a raw `Statement`
into an `Entry` today) and `Stash`, re-entering the decision as
`NexusWork::EffectCompleted`. A guardian scout is the **same shape as the
classifier that already exists** — a new `NexusEffectCommand::Scout` returning a
`Scouted` result. So:

- The model call is a **delegated async effect**, not an inline blocking await.
  The seam (`run_effect`) is already async; the inference runs in a dedicated
  IO/peer actor so the engine actor never stalls on it — the same discipline
  `Stash` already follows.
- The **vector index is component-owned SEMA state** (a `RecordIdentifier →
  embedding` table); only the *model inference* is external. Storing vectors is
  cheap and classical; at ~1700 records a brute-force cosine scan is sub-millisecond,
  so an ANN index (HNSW) is premature until the active set is far larger.
- The verdict is just a richer Nexus-composed reply on the ordinary channel;
  psyche-gated retirement belongs on the meta channel (`meta-signal-spirit`
  already carries privileged lifecycle).

### Atomicity (part of the design, not a separate debate)

Records should be **one minimal self-contained proposition** — the psyche's "one
statement, grammar not character-count" instinct, which is correct: length and
proposition-count anti-correlate ("use rkyv; never emit quotes" is short but two
propositions; a long sentence with modifiers is one). The unit is *truth-value
indivisibility*. The guardian's classifier splits a compound at capture (the
`ClassifyState` effect already exists to extend), emitting atoms linked by the
`relations` field so the split is lossless. Atomicity is what makes per-record
reinforcement and per-record deprecation *correct* — a record carrying one
truth-value can only be wholly valid or wholly stale. Caveat: atomicity alone
does not bound growth; it must ship with dedup + the lifecycle ladder.

## The review

My own judgment, grounded. Three buckets, stated plainly.

### Solid — keep

- **The authority model** (guardian flags / agent decides / psyche last). Honors
  `tf2o`/`ek8w`. This is what makes a model touching sacred intent acceptable.
- **Verbatim ground truth.** The production record stores no verbatim field today
  (`spirit-cli.md`: the agent clarifies wording before recording); keeping the
  raw psyche statement is a real improvement and the cleanest honoring of
  `kfxd`/`qkrg`.
- **Embeddings as a read-path upgrade** are the actual fix for the retrieval bug
  (full-scan + depth-cap). Brute-force cosine at this scale; no LLM in the read
  path.
- **Reinforce-or-insert genuinely bounds growth** by catching duplicates at
  capture — necessary, though not sufficient (see open issue 2).
- **A discriminative classifier**, not a generative model, for the
  same-vs-opposite call — calibrated and thresholdable, and better on exactly the
  paraphrase-vs-negation case that is the reason to have it. Generative model only
  for synthesis/briefing.

### Genuinely open — decide before build

1. **Privacy clamp (real, verified).** `PublicRecordQuery` structurally rejects
   elevated privacy (`signal-spirit/src/lib.rs:1098`), so reads are gated at the
   operation level. A `Record` op carries no privacy scope; returning a neighbor's
   summary in the verdict would bypass that gate — a public record's nearest
   neighbor can be private. **Resolution:** clamp the verdict to the caller's read
   scope (full summary only for neighbors at-or-below caller authority; identifier
   + tier + redacted reason otherwise); per-tier indexes; summaries
   verbatim-from-storage, never model-paraphrased. This is mandatory, not optional.
2. **Reinforcement vs. recorded intent (psyche's call).** "Reinforce in place"
   collides with the recorded `INTENT.md` stance (*"separate records… dedup is a
   query-time concern, not a storage shape"*), with `6z6t` (don't auto-raise
   certainty), and with `g8ln` (weight is not a count) — and weight itself is
   `u2s9`/`hp3r`-unsettled. The clean reconciliation that honors all of it:
   reinforcement records **a new atomic row + a typed `relations` edge** to the
   matched record (`a3l4`/`y0vr`), with weight *derived* from the cluster at query
   time. Otherwise the psyche explicitly supersedes the separate-records stance.
   Either way, **growth still needs the recorded lifecycle ladder** (`q4l0`
   decay/collect/purge) — reinforcement curbs duplicate inflow; the ladder bounds
   the rest.
3. **Sync verdict vs. async event — RESOLVED by the psyche (Decision `mrkv`):
   capture blocks.** The guardian is a true gate, not an advisor — a record is not
   captured until the guardian vets and admits it, so clutter is resolved or
   refused at the door (Principle `icpa`: Spirit must be maximally clutter-free).
   Two consequences to honor: **blocking is not losing** — a refused proposal must
   be resolved-and-resubmitted by the agent, never dropped (nothing is lost if the
   loop is honored); and **the failure mode is refuse, not admit** — if the
   guardian cannot vet (model unavailable), capture waits or is refused, never
   admitted unvetted. This makes guardian availability a genuine operational
   requirement, met by HA/queueing, not by weakening the gate.
4. **Determinism of any synthesized layer.** A generative model is not
   reproducible. If a curated/synthesized layer exists, pin the model + version
   and record every psyche confirmation as a raw record, so the derived view stays
   a pure function of raw — at which point a separate "curated layer" collapses
   into a derived `status` label over one log (simpler, and the right shape). Keep
   synthesis to medoid-selection (a real member), generative fusion only as a
   psyche-confirmed exception.
5. **Verdict shape.** A flat enum forces one disposition, but a proposal can
   duplicate X, contradict Y, and have precedent in Z at once. Use a relational
   bag: `{disposition, Vec<(RecordIdentifier, Relation, confidence)>}` — the wire
   mirror of the `relations` field.
6. **Eval.** Without a labeled set the guardian is unfalsifiable, which voids
   "allowed to be wrong" (you can't tell when it is). Carve a psyche-labeled
   pair-set from the 560 corpus; tune for high recall on contradiction/duplicate
   (a false negative re-admits pollution; a false positive costs one look).

### Not a real problem — explicitly debunked

A prior adversarial pass leaned on these to argue "the guardian can't be at the
gate." They do not hold:

- **"A blocking network await is forbidden."** Incoherent — an `await` is not a
  block, and the delegated async effect (`run_effect`, as `Stash`/`ClassifyState`
  already use) is the standard pattern. The model call slots straight in.
- **"It couples capture to the most-disrupted node."** Not a design-shape
  verdict. Node reliability is an operations matter on a different axis from design
  correctness, and "most-disrupted node" is a *current status snapshot* — the exact
  pollution the 560 audit names. With capture blocking (Decision `mrkv`), guardian
  availability *is* a genuine operational requirement — met by making the model
  HA/queued and by blocking-not-admitting when it is down, not by weakening the
  gate.
- **"A capture-time gate does nothing for growth."** False — reinforce-or-insert
  is a primary growth control (issue 2). It is necessary, not sufficient; pair it
  with the lifecycle ladder.
- **"Scout-then-store is a blocking concurrency race."** Marginal at human-paced
  write volume, and a non-issue when capture is advisory + resolution is
  idempotent (content-addressed supersede on `(id, expected-hash)`).

## The decisions still genuinely open

We are **redesigning** Spirit, so the old design-mechanism intent — separate-records,
dedup-at-query-time, dumb-storage-only, the tentative/unsettled weight semantics —
is *replaced by* this redesign, not a constraint on it. The redesign is the
supersession; those records get rewritten/retired when it lands, with no
permission ceremony. What still binds are the durable **values** that outlive any
storage shape: privacy closed-by-default, calibrated certainty (don't over-rate),
intent-is-primordial, and now clutter-free (`icpa`). Against that, the calls
genuinely still open:

- **Reinforcement** — decided in direction by `mrkv`/`icpa`: a pure restatement
  gets *no new row* (the gate reinforces the existing record); a
  distinct-but-related statement gets its own atomic row + a relation edge. Open
  sub-question: is weight a stored qualitative rung or derived from the cluster?
- **Who deprecates** — the agent proposes; the close on an existing record stays
  psyche-gated and recoverable (a durable value — don't silently lose intent).
- **Atomicity** — enforce (reject a compound at capture) or lint (accept + flag
  for split)? Lean: lint and gate the split.
- **Recall event for decay** — only an explicit restatement, or does an agent
  acting on a record count? Decides whether the store self-reinforces from use.

## Recommendation

The guardian is the right idea — point-of-entry prevention is exactly where the
560 audit says the cure lives. De-risk it in a sequence that makes each step earn
the next:

1. **Now, free:** the classical capture lint (`target-artifact + action-verb →
   route to a report, not Spirit`) — the single biggest pollution class, no model.
   Plus the verbatim raw layer.
2. **The retrieval fix:** embeddings + brute-force cosine on the read path.
3. **The guardian gate** as a Nexus effect returning the typed verdict —
   **blocking: capture does not complete until vetted** (Decision `mrkv`), with
   the privacy clamp built in from the start and a resolve-and-resubmit loop so a
   refusal never loses intent.
4. **Growth:** the recorded lifecycle ladder (`q4l0` decay/collect/purge) — the
   half of problem 1 the guardian does not cover.
5. **Tending:** periodic consolidation as the auditor (`ek8w`/`tf2o`), generative
   model only here, psyche-confirmed.

The guardian (problems 2, 4, and the inflow side of 1) and the lifecycle ladder
(the rest of 1, and 3) are two halves — neither alone fixes all four.
