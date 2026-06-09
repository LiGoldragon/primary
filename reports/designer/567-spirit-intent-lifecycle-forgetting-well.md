# 567 — Spirit intent lifecycle: forgetting well (design dialogue)

designer, 2026-06-09. The psyche opened a design conversation about the
**accumulation problem** in Spirit: the store only ever appends, so it grows
without bound, repetition piles up instead of reinforcing, intent goes stale
with no way to stop surfacing it, and a record that touches many things rots in
pieces. The psyche asked for prior-art research and my thinking + questions —
*not* implementation (operator is bringing the new schema-derived spirit to
feature parity with production; this is the design layer ahead of that).

This report is grounded by a 10-agent research workflow (`w9wyyoetz`): three
agents grounded the live store (data model, retrieval, the empirical 560-audit
pollution evidence, the binding NOTA/intent constraints) and six surveyed prior
art (truth-maintenance & belief revision, LLM-agent memory, temporal/bitemporal
KR, cheap dedup & confidence, atomic-proposition representation, proven low-tech
KM practice). Full prior-art detail and a synthesis draft are preserved in the
session workflow output; the load-bearing references are folded in below so this
report stands alone in the workspace.

## The reframe the psyche made mid-conversation (recorded `8g9n`)

I claimed Spirit has a "never hard-delete practice." The psyche corrected it:
*"On a long enough timeline, this is physically impossible. Hard deletion is an
inevitable design decision."* This is right and it reshapes the whole lifecycle.
An archive that only grows just relocates the unbounded-growth problem one tier
down. Deletion is not a failure mode to design *out*; it is a stage to design
*for* — recoverable up to a horizon, then physically collected. The goal was
never "don't forget"; it is **forget well**, and reinforcement is precisely what
buys a record out of collection.

Captured as Principle `8g9n` (High). Notably, **the store already agreed with
the psyche** before the correction landed: `btio` (a Decision) retired the
append-only constraint of the old record 1091; `q4l0` names a closed lifecycle
ladder ending in *compact* and *purge*; `o24x` makes removal a soft-then-hard
two-phase process. My "never delete" framing was the thing out of step, not the
store.

## The headline finding: this is not a blank slate

The single most important result of the research is that **the psyche has
already recorded substantial intent toward all four problems.** The design job is
to honor that corpus or explicitly supersede it — not to invent from zero. The
live store (~1700 records on the v0.5.2 production daemon) maps to the four
problems like this:

| Problem | Already-recorded intent (record id — gloss) |
|---|---|
| 1 — unbounded growth / retrieval | `q4l0` (the nominate/tombstone/archive/collect/compact/purge ladder); `sqrk` (adaptive-depth retrieval — quiet topics reach deeper); `699n` (weighted recency/keyword scoring, "maybe via Nexus"); `yhn9`/`xni2` (a dedicated typed archive store) |
| 2 — repetition reinforces | `vbx6` (Principle: **certainty ≠ weight** — certainty is confidence in the statement, weight is accumulated importance); `9bxr` (weight = recurrence/importance, distinct axis); `g8ln` (weight is a qualitative Magnitude rung, **"not an integer count"**); `6z6t` (Correction: reinforcement may raise *weight* but **must not auto-raise certainty**); `u2s9`/`hp3r` (weight-field design flagged **Low certainty, unsettled**) |
| 3 — deprecation / staleness | `a3l4` (a **relations field** — hashes pointing to other records — "the only code change needed"); `y0vr` (no composite *type*; supersession is the relations field + may yield 2-3 records); `qkrg`/`kfxd` (provenance + archival recoverability before any source is removed); `ek8w`/`tf2o` (**automated auditor auto-proposes, psyche confirms each retirement**; the judgment is agent-behavior trained by a skill, "the only supporting code is the relations field") |
| 4 — compound goes half-stale | `uara` (topics are **broad atomic single words**, not compound phrases); `jn99` (when a low-certainty idea is tangled inside a higher-certainty record, **split** so the parts are separate); `20jk`/`f0wm` (record fields vary by kind) |

Plus the capture-discipline records that govern all four and that the **560
audit** found being violated: `om3x`/`atjw` (never default to Maximum; the
certainty signal dies if most records are Maximum), `xtk9` (ephemeral
information is not intent), `7ccc` (Medium is the normal default).

**The 560-audit pollution taxonomy is the empirical proof of the disease.** Of
1706 classified records, 79% durable / 11% scratchpad / 10% borderline. The
dominant pollution is *working-instructions in a Decision costume* (105 of the
184 scratchpad) — the structural tell is **target-artifact + action-verb**
(`port orchestrate`, `migrate X to Y`). The audit's causal finding is decisive:
pollution **concentrates on active migration fronts** — clean in stable domains,
dirty in churning ones — so "the cure is disciplinary, not architectural." Any
machine help is a *second* line behind a better capture gate.

## The current mechanics (what we build on / must add)

The record is five fields: `{topics: Vec<Topic>, kind: Kind, description,
certainty: Magnitude, privacy: Magnitude}` (`signal-spirit/src/lib.rs:678`).
`Kind` is the closed five-variant enum. `Magnitude` is an 8-rung ladder
(`Zero` semantically lowest). Storage is redb-4 + rkyv-0.8 over `sema`/
`sema-engine`, with an **append-only `__sema_engine_commit_log`** beside the live
table and a **physically separate archive `.sema` file**. The engine already
supports mutate (`ChangeCertainty`/`ChangeRecord`) and retract (`Remove`,
`CollectRemovalCandidates`) — *the "monotonic" property is a usage convention,
not a storage guarantee.*

Retrieval is the felt pain: a **full table scan + linear filter**, no index on
any content field, bounded only by a fixed recency truncation (5/15/30/100).
There is **no relevance ranking, no embedding, no dedup, no clustering anywhere**
in any repo. An unbounded `(Any [])` query returns ~365 of ~1700 records because
the daemon depth-caps broad queries — **an agent literally cannot Observe "all
relevant intent" in one call today.** That is the concrete bug under the
abstract complaint.

Build-on hooks that already exist: mutable+filterable `certainty`; the
`certainty = Zero` → archive removal-candidate path; the commit-log history
spine; the separate archive store; per-topic counts. **Must-add (greenfield):**
weight/support-count, supersession edges, valid-to, active/retired as a derived
status, any embedding/ANN/dedup, and any atomicity enforcement.

## My design position

### The master move: status is a *derived label*, not a stored flag

Forty-five years of truth-maintenance (JTMS/ATMS) and every memory/temporal
system converge on one idea: **a record's belief-status is cheaply recomputed
over the log; it is never a flag you hand-edit.** Spirit has the append-mostly
log already. What it lacks is (a) the labeling pass that turns ~1700 records into
a small *currently-active* set, and (b) the capture-time pipeline that sends a
restatement to *reinforcement* instead of a new row. Both are overwhelmingly
cheap — set ops, ANN cosine, interval arithmetic, a graph fixpoint, closed-form
decay. The LLM fires in exactly **two** gated, write-time spots.

Reconciled with the psyche's finitude correction: the log is the source of truth
*within a recoverability horizon*; past the horizon, `q4l0`'s **compact** folds
and **purge** physically collects. "Immutable log" and "deletion is inevitable"
meet at: never lose history *accidentally*; collect it *deliberately* at a
horizon.

### The record: atomic proposition + three typed fields (no flags)

Keep the five fields; constrain `description` to **one minimal self-contained
proposition**; add three typed fields (generalizing `a3l4`):

- **`support`** — the reinforcement axis (problem 2). A vector of restatement
  tags `{date, time, match-strength}` (OR-Set style: every restatement is a
  provenance tag on the *existing* record), from which a qualitative weight rung
  and a recency-decayed stability are *derived*. This honors `vbx6`/`g8ln`'s
  two-axis qualitative model — but the underlying tag vector *is* a count, which
  collides with `g8ln`'s "not an integer count" (open question Q1).
- **`validity`** — a bitemporal interval (`valid_from`, `valid_to: Option`).
  Deprecation **closes `valid_to`; nothing is deleted.** Open-interval = the cheap
  "currently valid" predicate. Proven, standard (SQL:2011, Zep/Graphiti, Datomic).
- **`relations`** — typed lineage edges (`Supersedes`, `SupersededBy`,
  `DerivedFrom`, `Because`, `Constrains`), the typed form of `a3l4`. These are
  both the supersession graph (problem 3) and the connective structure recovered
  after a compound is split (problem 4).

`status` (Active / Reinforced / Superseded / Retired / Conflicted) is **derived,
never stored.** Embeddings live as component-owned typed Sema state (a
`RecordIdentifier → vector` table + an HNSW index), not a sidecar file.

### The capture pipeline — cheap funnel, LLM at the margin only

Per psyche statement (cost scales with *write* volume, never store size):

1. **Gate (classical).** The existing Spirit gate + the 560 mechanical
   pre-check: *target-artifact + action-verb ⇒ presumptive working-instruction →
   route to a report, not Spirit.* Highest-yield, cheapest filter; attacks
   pollution at the source.
2. **Embed** (one encoder forward pass, ~ms) over content + topics + kind.
3. **ANN near-dup** (HNSW, blocked by topic adjacency): ~1700 → ~5 candidates.
   This bound is what keeps the LLM cheap.
4. **Reinforce-or-insert**, three cosine bands: **high → auto-reinforce**
   (append a support tag, no new row, no LLM); **low → auto-insert** (new
   record, no LLM); **mid → the one gated judgment** — paraphrase vs negation,
   which cosine *cannot* tell apart. A small local NLI model (entail/contradict/
   neutral) gates first; genuine ambiguity escalates to a bounded LLM call or to
   the psyche.
5. **Compound detection (classical).** Dependency parse: a `conj`/`cc` edge
   joining two verb-headed clauses (the "each split must contain a verb" rule)
   flags a compound. **Detection needs no LLM**; the LLM split+decontextualize
   runs only on a confirmed positive, emitting atoms linked by `DerivedFrom` +
   `Because` so the split is lossless.
6. **Contradiction.** On a single-valued slot, a new record auto-closes the
   prior's `valid_to` by **interval arithmetic alone** (no LLM); semantic
   contradiction uses the step-4 gate on the already-narrowed candidate set.

Every step *proposes*; anything that changes what counts as active intent is
psyche-confirmable through the auditor slot. The cheap layer narrows and ranks —
**it never authors intent.**

### Retrieval — the actual fix for "can't load all relevant intent"

Replace newest-N with the **Generative-Agents scoring** over the *active set
only*: `score = relevance (ANN cosine) + entrenchment (the support stability /
the manufactured AGM entrenchment) + recency (one exponential decay)`. No LLM in
the read path. Optional later upgrade: **Personalized PageRank** over the
relations graph (HippoRAG) for bounded multi-hop "pull in related intent." This
delivers a *relevant active ranked* set instead of a depth-capped recency slice.

### Lifecycle / consolidation

Status is the grounded extension of the supersession graph ∩ open-validity ∩
`retrievability ≥ floor` — all cheap, all recomputable. **Retired** is the
principled successor to today's overloaded `certainty = Zero` marker; any
restatement revives it. Periodic **consolidation** is the natural body of the
already-planned auditor role (`ek8w`/`tf2o`): cheap clustering (label
propagation / HDBSCAN) → **canonicalize to a real member (medoid), not a
synthesized average** (honest provenance) → bounded LLM synthesis *only* when
members genuinely disagree, always psyche-confirmed. Sources archived +
hash-referenced before retraction (`qkrg`/`kfxd`).

## The atomicity verdict

**The psyche's instinct is right, strongly supported, and the highest-leverage
decision here — with one refinement.** Every mechanism votes for it for a
*technical* reason, not aesthetics:

- TMS **cannot represent** half-stale: support/retraction are per-node; a node
  bundling two propositions has a meaningless IN/OUT label. Atomic nodes are a
  *precondition* for the derived-label move to be correct.
- Validity intervals are per-fact; a compound can't carry one `valid_to`.
- Reinforcement needs atomic grain: a restatement might match one half of a
  compound and contradict the other — you cannot cleanly bump weight.
- Empirically (FActScore), even a single *sentence* mixes supported and
  unsupported facts in **40%** of cases — the sentence is too coarse.

**Why character-count is the wrong proxy (precisely):** length and
proposition-count *anti-correlate in the cases that matter.* "Use rkyv; never
emit quotes" is short but is **two** independently-stale-able propositions.
"Alice, the lead architect who joined in 2019, redesigned storage" is long but is
**one** assertion with modifiers. The right unit is **truth-value
indivisibility** — does it split into two independently-falsifiable statements?
A character budget is blind to the `and`. It also contradicts the psyche's own
"a long single statement is fine."

**The refinement — molecular, not maximally atomic** (Gunjal & Durrett 2024):
the unit is the **minimal *self-contained* proposition**, not the smallest
fragment. Over-atomizing yields ambiguous, misattributable junk ("She medalled in
1986" — which she?) and *reintroduces* staleness through over-specification.
Dense-X's three criteria: distinct meaning, minimal, **self-contained
(coreference resolved).** This is exactly "a long single statement is fine; two
statements must be two records" plus a self-containment guard.

**What's lost and how it's recovered:** atomizing severs because/therefore
structure; the `relations` field carries it back as typed edges. Splitting
becomes **lossless.** This is why `relations` is load-bearing — atomic nodes
*plus a justification graph* recover everything the compound encoded without its
fragility. The psyche already half-recorded this: `uara` (atomic topics), `jn99`
(split tangled certainty), `y0vr` (a refresh may yield 2-3 records, not one).

**The crucial caveat:** atomicity *alone does not bound growth.* A-MEM is
atomic, richly linked, and *still* a monotonic pile — because it has no decay, no
dedup, no invalidation (structurally Spirit's current failure mode with nicer
metadata). **Atomicity must ship with the dedup + decay + invalidation
machinery, or it solves nothing for problem 1.**

## The cheap-vs-LLM ledger (the psyche's hard constraint)

- **Read path: zero LLM.** ANN cosine + three float comparisons + a graph
  reachability — all classical.
- **Write path: two gated LLM spots only** — (i) split a *confirmed* compound,
  (ii) adjudicate a *mid-band* same-vs-contradict pair the cheap layer already
  narrowed to ~5 candidates. Both distillable to small local models (a
  Propositionizer; a local NLI head). LLM cost scales with *write* volume, never
  store size or query volume.
- **Everything else classical:** embeddings (encoder, not generative), HNSW,
  set/interval/graph ops, spaced-repetition decay math, Beta-Bernoulli counters.
- **The one real risk to flag loudly:** cosine cannot distinguish *paraphrase*
  from *negation* — both are high-similarity. Auto-reinforce on raw cosine could
  *silently merge a Correction into the thing it corrects.* The mid-band gate
  exists precisely to stop that, and it deserves its own stress test.

## Open questions for the psyche

The first two are **binding contradictions with already-recorded intent** and
need explicit supersession (only the psyche supersedes psyche intent).

1. **Reinforce-in-place contradicts your recorded model.** `persona-spirit/
   INTENT.md` records your stance: *"separate records then. repeated similar
   intents will mean stronger signal,"* and *"dedup and clustering is a
   query-time concern, not a storage shape."* This conversation wants repetition
   to bump weight on the *existing* record at *capture* time. **Do you supersede
   the separate-records model?** And two sub-reconciliations with your own prior
   intent: (a) `6z6t` (a Correction) says reinforcement raises *weight* but
   **must not auto-raise certainty** — so when you said "more weight or
   certainty," did you mean *weight* (consistent with `6z6t`), or do you now want
   certainty to rise too? (b) `g8ln` says weight is a qualitative Magnitude rung,
   **"not an integer count"** — but a reinforcement mechanism naturally counts
   restatements. Qualitative rung *derived from* a real count, or genuinely no
   count?

2. **Dumb-storage vs engine machinery — the load-bearing architectural fork.**
   `tf2o` records: the refresh/agglomeration judgment is *"primarily agent
   behavior trained through a skill, not engine logic — the only supporting code
   is the relations field,"* and `INTENT.md` calls Spirit *"dumb storage, not a
   thinking thing."* My design puts real cheap machinery *in the engine*
   (embeddings table, HNSW, the labeling pass, validity intervals). **Is that a
   welcome expansion, or do you want the cheap detection to live in the
   auditor-agent/skill layer and keep the engine dumb?** My read: the *detection*
   can live engine-side cheaply while the *decision* stays gated in the auditor —
   but this needs your ratification because it stretches a recorded principle.

3. **Does un-restated intent ever retire on its own?** A usage-decay model
   (spaced-repetition retrievability floor) can auto-flag dormancy. Your `btio`
   stance is *"over-removal is worse than under-removal."* So: does decay ever
   *retire* on its own, or only ever *flag candidates* for the human-gated
   auditor? (My lean: flag-only; never auto-retire from non-use.)

4. **Atomicity — enforced or linted?** Hard-block a compound at `Record`, or
   accept-and-flag-for-split? Parsers err on hard coordination, so my lean is
   **lint at capture, gate the split** — but you decide whether a flagged
   compound *blocks* capture or only *warns*.

5. **What is a "recall event" for decay?** Genuinely novel: spaced-repetition
   math is proven for flashcards, but Spirit must *define the review event.* Only
   an explicit psyche restatement (conservative), or does an agent
   *loading-and-acting-on* a record without contradiction count as a successful
   recall that boosts its stability? This decides whether the store
   self-reinforces from use or only from you.

## What this is not (sequencing)

This is design dialogue, not a build order. Nothing here lands until the two
binding contradictions are resolved and the new schema-derived spirit reaches
parity. The natural first increment once settled is the **capture gate +
embeddings table + ANN reinforce-or-insert** (kills problems 1 and 2 at the
source) before the full lifecycle/labeling machinery. The ~1700 live records
would migrate via a one-time auditor pass (embed → cluster → propose
merges/atomic-splits), psyche-reviewed batch-by-batch exactly as the 560 audit
was.
