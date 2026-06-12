# Guardian prompt spec — checklist, verdict format, over-training (for operator)

The guardian-prompt design for the lean intent-justification gate (607), from the per-operation
design workflow (`wf_75da1baa-a4c`, 8 agents). This report is the **spec**; the ~50 worked
accept/reject examples are the companion **`608-guardian-example-library.md`** (the over-trained
few-shot). Ratified context: `88mw` (over-train then scale back), `4jgt` (always emit valid NOTA),
`woku` (binary, never edits), `so3b` (certainty = burden of proof).

## BLOCKER — do this first

**Five reason atoms the whole design needs are not in the deployed enum.** `GuardianRejectionReason`
currently holds only `{Duplicate, Contradiction, Compound, NonIntent, UnclearPrivacy, UnclearDomain,
ClarifyTramples, ClarifyLosesMeaning, SupersedeTargetMissing, RetrievalInsufficient, Harness*}`. The
burden-of-proof design is **physically unnameable** until it gains **`MissingTestimony`,
`TestimonyFabricated`, `InsufficientWarrant`, `Overstated`, `ImportanceUnsupported`** (confirms
operator 375 #3). This is a Signal-contract change (version bump) and must land before the prompt is
embedded — the few-shot referencing these atoms is dead until then.

## The shared admission checklist — 9 gates, top-down, first-match, one reason

Run in order; **stop and reject at the first unmet gate** (directed verdict); emit exactly the one
atom for that gate. Each op activates a subset (table below).

- **Gate 0 — Retrieval sufficiency.** Is the supplied live-record bundle rich enough to judge
  duplicate/contradiction/target for this op? Too thin → `RetrievalInsufficient`. (An *empty* bundle
  is fine for a genuinely-novel `Record` — empty ≠ insufficient.)
- **Gate 1 — Target soundness** (target ops only). Every named target present/readable in the
  bundle, else `SupersedeTargetMissing`. (Never for plain `Record`.)
- **Gate 2 — Testimony present & authentic.** ≥1 verbatim quote, else `MissingTestimony`. A bare
  affirmation (`yes`/`do it`) must carry its antecedent, else `MissingTestimony`. Agent-prose-shaped
  or suspiciously-perfect quote → `TestimonyFabricated` (heuristic).
- **Gate 3 — Destructive-op psyche authorization** (Supersede, Retire, meaning-changing
  ChangeRecord, certainty *downgrade*). A verbatim psyche quote must authorize *this* destruction;
  agent-judged "staleness" never does → `InsufficientWarrant`.
- **Gate 4 — Warrant.** The quoted words actually license *this* submission; on-point-but-doesn't-
  argue-this → `InsufficientWarrant`.
- **Gate 5 — Shape of the arrow.** One proposition (`Compound`); durable not task-state
  (`NonIntent`); for mutations, keep the same arrow — redirect/invert/harden → `ClarifyTramples`,
  silently drop a clause → `ClarifyLosesMeaning`.
- **Gate 6 — Classification.** Domain is a universal subject (named instances like `spirit`/`rkyv`
  are *referents*, not domains) → `UnclearDomain`; mis-filed privacy → `UnclearPrivacy`.
- **Gate 7 — Magnitude burden** (the signature gate; ops that claim a magnitude). **Certainty read
  off the QUOTE's modality**, never the agent's prose, never raised by importance: hedged
  (`maybe`/`could`/`I think`) clears Low; `should`/preference clears Medium; flat commitment clears
  High; unhedged founding language clears VeryHigh/Maximum (rare). Over-claim → `Overstated`.
  **Importance** judged only from recurrence/blast-radius evidence, independently → unsupported is
  `ImportanceUnsupported`. (Lowering never risks `Overstated`; raising re-tests. Certainty Zero =
  off-ladder removal sentinel.)
- **Gate 8 — Cross-record collision** (against the live/untouched corpus). Same arrow live →
  `Duplicate` (remand: bump importance). Negates a live psyche arrow without an authorizing quote →
  `Contradiction` (remand: file a `Supersede` carrying the authorization).

`RegisterReferent` runs its **own** checklist on a separate verdict type:
`NonReferent → TooVague → Ambiguous → Duplicate → AliasCollision → UnclearJustification`, first-match.

### Which gates apply per operation

| Op | Active gates |
|---|---|
| `Record` / `Propose` | 0,2,4,5,6,7,8 (no target, no destruction) |
| `Supersede` | 0,1,2,3,4,5,6,7,8 (per replacement; multi-replacement preservation) |
| `Clarify` | 0,1,2,4,5,6 (inherits magnitude, skips burden) |
| `Retire` | 0,1,2,3,4 (no Entry, no magnitude) |
| `ChangeRecord` | 0,1,2,3(if meaning-change),4,5,6,7(if magnitude restated),8 |
| `ChangeCertainty` | 0,1,2,3(if downgrade),4,7 |
| `RegisterReferent` | its own closed checklist + verdict type |

## The verdict format — malformed replies structurally impossible (`4jgt`)

The guardian emits **exactly one** NOTA value of the operation's verdict type — type-first,
positional, bare atoms, no prose, no second value:

- Intent ops → `GuardianVerdict`: **`(Accept)`** or **`(Reject (<Reason> [<one-line explanation>]))`**
  — always double-nested; `<Reason>` is exactly one atom from the closed intent set; the explanation
  bracket is always present, one sentence, never empty.
- `RegisterReferent` → a **separate** `ReferentGuardianVerdict`: `(Accept)` or
  `(RejectReferent (<Reason> [...]))` — never mix the two reason sets.

Invariants: any single-nested/flat form, out-of-set atom, missing explanation, or extra value is a
**typed-parse failure → fail-closed `HarnessMalformed`**, and a **type-aware retry** re-prompts
against the named verdict type so a formatting slip is corrected, never silently lost. The reason set
and verdict grammar are **generated from the enum into the prompt** — the model is shown only legal
atoms.

## Over-train now, measure before trimming (`88mw`)

Few-shot is the whole training stack at this stage (no fine-tune — the *decision-log is the
flywheel*, not weights). Pin **temperature 0**, load a deliberately over-large example block, then:

- **Load-bearing pairs that must stay verbatim** (the catches the model fails zero-shot): the
  **same-quote-two-certainties** pair (the single most important example — identical quote admitted
  at VeryLow, rejected `Overstated` at High); the **orthogonality** pair (VeryLow-certainty/
  High-importance admit beside an `ImportanceUnsupported` reject); the **destructive psyche-auth**
  pair (agent-judged-stale reject beside a `*kill them*`-authorized accept); the **multi-replacement
  preservation** pair (two-proposition retired set → two replacements admit, vs. collapsed-to-one
  `ClarifyLosesMeaning`); the **correct-vs-replace** pair (in-place fix vs. reversed-decision
  `ClarifyTramples`); the **deictic-affirmation** pair (`*yeah drop it*`+antecedent vs. no-antecedent
  `MissingTestimony`); the reason-collision triplets.
- **Scale back only by ablation against a held-out eval** (the live-scenario suite + every psyche
  override harvested from the decision journal, each `(op, candidate, bundle) → gold verdict+reason`).
  Drop an example only if removing it regresses **neither exact-verdict nor exact-reason** match
  (reason-match matters as much — a right reject for the wrong reason mis-remands). Never split a
  contrastive pair. Stop at the floor; re-expand when a production override exposes a new failure.

## Cross-cutting lessons (the prompt's spine)

Modality off the quote, always; two orthogonal axes (each with its own atom); psyche supremacy gates
every destructive write; no quote no case (bare affirmations need antecedents); directed verdict /
first-match / one reason; **the guardian never edits — it admits or remands** (`woku`); know which
gates apply to your op (emitting an inapplicable reason is itself an error).

## Other open issues for operator (besides the BLOCKER)

- **Retrieval must be complete, and it isn't.** `RetrievalInsufficient` is now a *correctness* gate:
  the guardian can only catch a duplicate/contradiction/wrong-target it is actually *shown*. Current
  retrieval is category/domain-scoped — the bundle must become complete, ranked, capped, and
  *include named targets*. This is upstream of the prompt and the design's shakiest foundation
  (report 606, doubt 5).
- **`ChangeCertainty` isn't a wired `GuardianOperation`** (the set is Record/Propose/Clarify/
  Supersede/Retire/Remove/ChangeRecord/CollectRemovalCandidates). Confirm: fold into `ChangeRecord`
  or add the verb.
- **`SupersedeTargetMissing` is overloaded** across all target-sensitive ops — confirm the shared
  atom vs. a neutral `TargetMissing` rename before it calcifies.
- **Domain spelling** — the examples mix `Software(Data(Serialization))` and
  `(Technology (Software (Engineering …)))` forms; reconcile to the one canonical recursive-enum
  `Domain` spelling before embedding, or the model mimics an invalid shape.
- **`RegisterReferent` composite nesting** — verify the live `ReferentRegistration` supports the
  `nests [...]` composite-referent shape before shipping those examples.
- **Few-shot size vs. output/token budget** (report 364) — measure the over-large prompt's
  latency/cost on the real local model before treating it as the shipping default; the ablation
  metric brings it back down once the decision-log eval exists.

## Net

A specialized clean-context judge (record `2t89`) running a 9-gate directed checklist, emitting one
fail-closed verdict atom, over-trained on ~50 discriminating examples and scaled back only by
measured ablation against its own decision-log. It makes the binary verdict auditable and
reproducible, the remands actionable, and the could→should catch a hard evidentiary rule — *once the
enum gains the five atoms and retrieval is made complete.*
