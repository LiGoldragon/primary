# Spirit intent redesign — corpus patterns for the implementer

Section 1 of the `580` meta-report. Mines the **live intent corpus** (Spirit
v0.8.0, queried read-only 2026-06-10) for the patterns that should shape the
guardian, the migration, the category catalog, and the weight axis. Companion to
the settled design (`578`) and the corpus macro-stats (`577`, `579`).

Everything here is grounded in records pulled live. Quotes are verbatim from the
deployed store; record codes are the daemon's base36 identifiers. No mutating op
ran; the 7 private records (all at privacy `Low`) were counted but never read.

## 0. Live corpus snapshot (re-confirmed against v0.8.0)

The daemon restarted mid-session; the on-disk marker reads 1411–1413 records.

- **Default-visible (certainty ≥ Minimum):** 1366. **Hidden (certainty Zero,
  removal-candidates):** 45 — the default certainty floor now *does* hide them
  (v0.8.0 has the certainty-aware query `577`/`579` said was missing in v0.4.0).
- **By kind:** Decision 493, Principle 369, Clarification 200, Correction 181,
  Constraint 123.
- **By certainty:** Zero 45, Minimum 6, Low 6, Medium 113, **High 1109**,
  VeryHigh 41, **Maximum 91**. High is the default capture level; the 91 Maximum
  are the agglomeration canonicals from `579`; the 45 Zero are its soft-retired
  sources.
- **By privacy:** Zero (public) 1359, **Low 7**, every other level 0. Privacy is
  effectively a two-value field in practice (see §5).
- **1315 distinct topic tokens**, 910 of them singletons (used once), 150 used
  twice. The top ~70 tokens carry the mass; the rest is leaky free-text.

## 1. Duplicate / near-duplicate cluster shapes — what makes "the same arrow"

The `579` pass already collapsed 43 sources into 21 canonicals across the three
densest topics. Reading those clusters plus fresh ones (`workspace`, `spirit`),
the same-ness signal sorts into four grades — and the guardian needs all four,
because only the first is cheap.

### Grade A — restatement (token-overlapping paraphrase)

Near-identical text, often by different agents on different days. These are what
a literal keyword/substring check catches.

- `kr1v` vs `3jkx`: *"Spirit record identity is a random hash, not a
  content-address fingerprint. Because records are mutable … a content-address
  hash adds computation for very little value"* vs *"Spirit record 2590 is
  negated: Spirit record identity should use a random/opaque hash, not a
  content-address fingerprint. Because records can mutate, content-addressing
  adds computation and little value …"*. Same arrow, twice, one even citing the
  record it duplicates.
- The `579` `nota` cluster `vfjw` absorbed **seven** restatements (`tlaf` `d4dl`
  `18kl` `rvh4` `olno` `xt5h` `kpcb`) of "use brackets not quotes."
- The `579` `spirit` cluster `0dys` absorbed **five** (`44b4` `55pi` `lstz`
  `xbb5` `zp10`) of "offer shorthand forms that lower to the full typed API."

**Implication:** Grade A is the floor the guardian must never miss, and the
weight bump must fire here. These are exactly the records that share a category
*and* salient keywords (`hash`/`identity`, `bracket`/`quote`, `shorthand`/`lower`).
High-recall retrieval (category + keyword + full-text) reliably surfaces them.

### Grade B — paraphrase with no token overlap

Same arrow, disjoint vocabulary — falls below any jaccard threshold (`577` and
`579` both flag this as the reason their dup counts are *conservative*).

- `k5y3` (canonical) vs `y40b`: *"privacy is a `Magnitude` on the privacy axis"*
  vs *"privacy modeled as a directional magnitude"* — same idea, the second
  sharing only the word "magnitude."
- `wm4q` vs `clfe`: *"typed access-classification model, Public default, not a
  boolean"* restated almost word-for-word but the pair was found by *meaning*,
  not tokens, in the manual pass.

**Implication:** Grade B is **why the auditor exists** (`578` §5/§9). The
guardian's literal retrieval will miss some of these at the door; the at-rest
backstop catches the residue. Do not try to make the guardian's duplicate
detection complete — design it high-recall-best-effort and let the auditor mop
up. This is the load-bearing reason the design has *two* gates, not one.

### Grade C — same arrow, one carries extra nuance (the borderline)

The hard cases. Two records say the same core thing, but one adds a distinct
aspect. Folding loses the aspect; not folding keeps a near-dup.

- `579` §"Left for the psyche" item 1: `qtbd`/`y5m9`/`f36y`/`0zk5` (min-THREE
  identifier length) vs `tw81`/`rh29` (min-FOUR). Looks like a dup cluster; is
  actually a *contradiction* that the deployed daemon already resolved to four.
  The manual pass refused to fold it. A naive guardian would mark these
  duplicates; the right verdict is "one supersedes the other."
- `579` §item 5: `ous0` ("don't treat an agent's inferred grammar as captured
  intent") vs `ta58`/`oe6s` ("don't resurface denied syntax"). Same shape ("don't
  do X with denied syntax") but `ous0` is a *meta capture-gate* rule and the
  others are *specific syntax denials*. Folding would erase the specific denials'
  provenance.

**Implication:** The guardian's duplicate reason must be **conservative — refuse
to merge when either record carries an aspect the other lacks**, and route the
real conflicts (Grade C that is actually contradiction) to `contradiction`, not
`duplicate`. The typed reason set in `578` §4 already separates `duplicate` from
`contradiction`; the corpus confirms the line between them is the *most* common
place a real intent system gets it wrong. When in doubt, **admit and let the
auditor propose the merge** (which the psyche confirms) rather than refuse at the
door — a wrong refusal is invisible, a wrong merge destroys intent.

### Grade D — design-evolution chain (must NOT collapse)

Records that *look* duplicative but encode a live, unresolved design history.

- `579` §item 3 (Asschema defined-first vs REMOVED), §item 4 (the `@`-sigil
  built up across `ilaq`→`r8da`→`skz6`→`n2z3` then ABANDONED by `own9`). These
  are supersession chains mid-flight.

**Implication:** These are the migration's job, not the guardian's — the old
arrows get *superseded* (retired to archive), not deduplicated. The guardian only
ever sees the *current* head of such a chain after migration.

### Weight-bump mechanics, grounded

`578` §10 says weight rises by one on a duplicate-refusal. The corpus says the
distribution is heavy-tailed: the `vfjw` bracket-rule arrow was independently
restated **8+ times**; the `0dys` shorthand arrow **6+**. So the bump is not a
rare event — a handful of canonical arrows will accumulate large weight fast,
which is exactly the desired signal ("this one keeps coming up, it's load-bearing").
Confirms `578` §10's choice of *monotonic, no auto-decay*: the bracket rule's 8
restatements across months is real reaffirmation, not noise to decay away.

## 2. Discussion-contamination in Corrections and Clarifications

The migration (`578` §8) must extract forward content from ~181 Corrections and
200 Clarifications and reclassify them as Decision/Principle/Constraint. How
contaminated are they?

**Measured: 149 of 181 Corrections (83%) carry a referential-negation marker**
(`not`/`instead`/`rather than`/`never`/`must not`/`obsolete`/`negated`/
`superseded`/`abandoned`). The contamination sorts into shapes, easiest-first.

### Shape 1 — "not that, this" with the arrow stated inline (clean rewrite)

The forward arrow is fully present; only a negative clause needs deleting.

- `09do`: *"Beads are coordination aids, **not a substitute for implementation**;
  when the psyche asks an agent to implement work, the agent should work the bead
  or code path immediately unless blocked."*
  → forward: *"Beads are coordination aids; when the psyche asks for
  implementation, work the bead or code path immediately unless blocked."* (Decision)
- `0dmo`: *"Actor-native migrations should change the generator and runtime
  source of truth **instead of stopping at compatibility bridges**; no backward
  compatibility, best design only."*
  → *"Actor-native migrations change the generator and runtime source of truth.
  No backward compatibility — best design only."* (Constraint)
- `0b9q`: *"NOTA pipe text should use a normal escape character … **instead of
  widening pipe fences indefinitely**. The string codec should keep one readable
  pipe-text delimiter shape and escape payload content …"*
  → drop the `instead of` clause; the second sentence is already a pure arrow.

These are **mechanically rewritable**: delete the `not X` / `instead of X`
clause, keep the rest. The negative clause is a forward-law boundary in some
(`09do`'s "not a substitute" is close to a law) but in most it is pure debate.

### Shape 2 — corrects an agent behavior (clean once de-narrated)

- `0sef`: *"When the psyche injects a short piece of information mid-task … that
  is **NOT an instruction to stop**. The agent must keep working …"*
  → *"When the psyche injects information mid-task, absorb it and keep working;
  only an explicit stop instruction is an interruption."* (Principle)
- `2vp2`: *"A psyche statement that leans toward a choice while explicitly asking
  for more information is **NOT a ratification** …"*
  → *"A psyche lean that explicitly asks for more information is a lean pending
  information, not a ratified Decision; capture it as a lean, not a Decision."*
  (Principle — and note it survives as a forward rule about capture discipline.)

### Shape 3 — references a specific record/number (the hard cases)

The forward content is entangled with a citation to a now-stale record. The
citation must be *dropped*, and sometimes the forward arrow is only implicit.

- `3jkx`: *"**Spirit record 2590 is negated**: Spirit record identity should use
  a random/opaque hash, not a content-address fingerprint. …"* — the colon splits
  cleanly: everything after "negated:" is the arrow; the prefix is pure
  discussion. Easy.
- `3v04`: *"**Record 151 (DeepSeek subsumes-into-persona-pi) is superseded**; the
  real intent is a workspace-native Persona LLM client library, not subsumption
  into the Pi harness wrap"* — forward arrow ("a workspace-native Persona LLM
  client library") is recoverable but **thin**; the record is mostly the
  supersession event. After migration this is a *correction event* (`578` §8),
  not a stored arrow — the surviving arrow may already exist elsewhere.
- `oqn6`: *"Spirit record 1088 was over-captured by the operator: the psyche
  instruction to create a report and test it in production was a working
  instruction for this session, not durable schema-language design"* — this has
  **no forward arrow at all**. It is a meta-statement that another record should
  not exist. After migration: a *retirement of 1088*, producing no Decision/
  Principle/Constraint. There are several of these (`ous0`, `eegq` STT artifact,
  `6uz3` pseudo-NOTA header drift).

### Shape 4 — "the prior X wording was too broad" (clarify-shaped, not supersede)

- `3naf`: *"**The prior t6s1 wording was too broad**: the durable principle is
  that NOTA encoders should not over-bracket bare-safe string atoms. …"* — this
  is a *clarify* of `t6s1` in the new model, not a stored Correction. The forward
  wording is clean; it should be applied in-place to `t6s1` via the `clarify` op.

### Clarifications

Sampled the 200 Clarifications: the dominant contaminant is an opening
back-reference clause — *"Clarifying record 1555:"* (`hvta`), *"Refining record
1568:"* (`rlyn`), *"Extends record 3nqt:"* (`8bea`), *"Clarification of the
one-capturer-per-multi-lane-prompt rule:"* (`yenl`), *"gap-fill on the directive
operator received -"* (`pokt`, `ublb`). In every case the back-reference is a
**prefix the arrow does not need** — strip the prefix and the rest is already a
forward statement.

### Rewritability estimate

| Bucket | Corrections (~181) | Clarifications (~200) |
|---|---|---|
| Mechanically clean (drop a negation clause / back-ref prefix) | ~110 (60%) | ~150 (75%) |
| Clean but thin — forward arrow recoverable, may already exist elsewhere | ~35 (20%) | ~30 (15%) |
| **No forward arrow — becomes a retirement/event, produces no record** | ~25 (14%) | ~10 (5%) |
| Genuinely tricky — entangled multi-claim, needs human judgment | ~11 (6%) | ~10 (5%) |

**Implication for the migration:** it is *not* a 1:1 reclassification. Roughly
35 Corrections and 10 Clarifications produce **zero forward records** (they are
pure retirements/events) — the migration must allow a record to map to "nothing
but a supersede/retire event." Budget the migration's LLM rewrite pass to emit
one of three outcomes per legacy record: **forward arrow** (most),
**clarify-in-place of a named target** (the "prior X wording" shape), or
**retire-only** (the "X was over-captured / is obsolete" shape). A migration that
assumes every record yields one new record will manufacture ~45 hollow records.

## 3. Supersede vs clarify vs trample — grounding the three-way check

`578` §4 makes the `clarify` op judge: genuinely **clarifies** (admit) vs
**tramples** into something unrelated (reject → use supersede) vs **loses
important aspects** (reject). The corpus has natural specimens of each.

### Clean clarify (sharpens, meaning preserved) — ADMIT

- `8bea` extends `3nqt`. `3nqt`: retry on transient errors applies to *"Subagent
  and workflow dispatch."* `8bea`: *"transient-error recovery applies to the MAIN
  agent's own tool calls, not only dispatched subagents and workflows, and to
  connection-level failures …, not only HTTP 529."* This **widens scope without
  contradicting** — the original arrow still points the same way, just farther.
  Borderline: a strict reading calls a scope-widening a *new* arrow (propose),
  not a clarify. The guardian needs a rule here (see implication).

### Clarify that loses an aspect — REJECT (clarify-loses-meaning)

- `yenl`: *"the default capturer is the lane that RESPONDS FIRST, not the
  designer. In practice that is the OPERATOR."* If applied as a clarify over a
  prior "designer captures multi-lane prompts" rule, it would **flip the named
  party** — that is not a sharpening, it is a reversal. Correct handling:
  supersede, not clarify. Good test case for the `clarify-tramples` reason.

### Trample — a "clarification/correction" that changed the meaning — REJECT

- `y0vr` (kind Correction): *"There is no composite intent type in code … **This
  refines the earlier composite-record direction (Principle audg3)**: provenance
  and agglomeration are expressed through a relations field … not a dedicated
  Composite type."* It is *labeled* a refinement ("refines") but it **deletes the
  Composite type** the earlier principle introduced. That is a trample dressed as
  a clarify — exactly the failure mode `578`'s clarify-gate exists to catch. If
  an agent submitted this as `clarify(audg3)`, the guardian must return
  `clarify-tramples` and force a `supersede`.
- `6z6t`: *"Record d5s2 **overstates** agglomeration as a certainty-raising
  mechanism. Agglomerating … should **not** automatically raise certainty …"* —
  again labeled a correction-of-degree but it reverses a specific claim. Supersede.

### Pure supersede (explicit replacement) — the supersede op

- `own9`: *"The ENTIRE at-binder surface … is ABANDONED. nota-next must REMOVE
  all @-binding parser support …"* — names a whole surface for retirement.
- `n2te`: *"Public-traffic routing Design C (client-side discovery) is rejected.
  The client connects to ONE STABLE SOCKET …"* — rejects a named alternative,
  states the replacement. Classic supersede: the forward arrow ("one stable
  socket") admits, the rejection becomes the correction event.
- `umsv`: *"Foundational model, superseding the at-sigil for macro invocation
  from record 1087. EVERYTHING is a struct …"* — explicit supersede with the new
  arrow inline.

**Implication for the guardian:** the corpus shows agents *mislabel* their own
operation constantly — `y0vr` and `6z6t` call themselves refinements/corrections
while reversing meaning; `8bea` calls itself an extension while arguably
proposing a new arrow. **The agent's chosen op is a hint, not a fact** — the
guardian must independently classify (does this preserve the target's meaning?
add to it? reverse it?). This is the single strongest argument for the design's
agent-judges-not-keyword-matches choice: a string matcher cannot tell `8bea`'s
clarify from `y0vr`'s trample; both say "refines/extends." Concretely, the
guardian's clarify check needs three sub-verdicts as `578` specifies, and the
**default on ambiguity (scope-widening like `8bea`) should be to require a
`propose` of a fresh, sharper arrow that the auditor can later merge** — never
silently widen via clarify, because a widen that the author thought was
meaning-preserving is the most common way meaning erodes.

## 4. A candidate broad-category catalog (bootstrap for §6 of `578`)

Folding the 1315 free-text tokens, a **15-category** set covers ~92% of the 1366
visible records (measured by topic-token membership). Proposed for the psyche to
bless:

| Category | Folds in (sample of current topics) | Records |
|---|---|---|
| `schema` | schema, schema-language, asschema, namespace, macro(s), enum, struct, newtype, declarations, roots, variants | ~441 |
| `nota` | nota, nota-next, syntax, delimiters, symbol, string(s), vector(s), parser | ~162 |
| `signal-wire` | signal, nexus, sema, wire-contract, codec, rkyv, router, routing, mail, meta-signal, envelope, plane | ~177 |
| `component-shape` | component-shape, component-triad, triad, daemon, runtime, contract-daemon-split | ~140 |
| `spirit-intent` | spirit, intent, certainty, weight, agglomeration, identifiers, privacy, query, recency, supersession | ~214 |
| `workspace-process` | workspace, orchestrate, workflow, roles, reports, reporting, context-maintenance, beads, chat, discipline | ~206 |
| `agent-behavior` | agent(s), autonomy, resilience, retry, subagents, effort, interruption, focus | ~28 |
| `persona-llm` | persona, persona-pi, pi, local-llm, llm, harness, browser-use, model | ~86 |
| `infra-deploy` | cloud, criomos, nix, deploy, prometheus, zeus, cluster, horizon, networking, secrets, upgrade, production | ~141 |
| `naming-language` | naming, language, vocabulary, readability | ~33 |
| `testing` | testing, tests, fixtures, verification, vm-testing, trace, tracing | ~59 |
| `rust-code` | rust, rust-emission, methods, traits, emission, lowering, crate-layout, engine, library | ~54 |
| `repo-vcs` | repository(-management), version-control, branches, worktree-discipline, jj, version, integration | ~44 |
| `forge-build` | forge, build-system | ~2 (small but a named emerging family) |
| `personal-affairs` | assistant, counselor, personal-affairs, mail, google-suite, access | ~24 |

(Records sum > 1366 because most carry several topics and land in several
categories — desired: a record about "spirit schema certainty" lives in both
`spirit-intent` and `schema`.)

### Genuinely ambiguous topics that resist one category

- `trace` / `tracing` (~22): straddles `testing` (it proves behavior) and
  `rust-code` (it is an emission concern) and `signal-wire` (it traces messages).
  Lean `testing` but flag.
- `macro` / `macros` (~26): `schema` (schema macros) vs `nota` (NOTA tagged
  forms) vs `rust-code` (Rust macro emission). The `j34e`/`1fgo` records show the
  psyche itself debating where macros live — so this token will keep being
  cross-category by nature.
- `mail` / `messaging`: `signal-wire` (the mail mechanism) vs `personal-affairs`
  (the assistant's email). Genuinely two different "mail" — a token collision the
  catalog must split by co-topics, not by the bare word. **This is a concrete
  argument for category being multi-membership and keyword being the
  discriminator** (`578` §6/§7): `mail`+`signal` vs `mail`+`assistant`.
- `domain` (~4), `scope` (~3): too generic to anchor; fold by neighbors.
- `lojix` (~18): a project/component name spanning schema + runtime + actor work;
  resists a domain category because it *is* a domain. Suggests the catalog may
  need a few **project-name categories** alongside the concept categories, or
  these fold under `component-shape`/`rust-code` by their real subject.

**Implication:** 15 broad categories is the right order of magnitude (the design
said ~20). The ~111 uncovered records are almost all singletons that fold by
co-topic; none demand a 16th broad category except possibly a project/component
axis. Recommend the psyche bless this set, with the explicit note that **a record
gets multiple categories** and the **keyword layer carries the precision** —
otherwise the `mail`/`macro`/`trace` collisions force false single-assignment.

## 5. Privacy and edge cases the implementer will hit

### Privacy is effectively binary in the data

1359 public + 7 at `Low`, nothing in between or above. The 8-level Magnitude
privacy ladder (`578`/skill doc) is **almost entirely unexercised**. Two
implications: (a) the guardian's `unclear-privacy` reason will fire rarely — the
real-world default is public; (b) do not over-engineer privacy tiering for the
migration — a binary public/private carries the whole live corpus, and the
graduated ladder is aspirational. The 7 private records were not inspected (hard
override); whatever resists the model there is out of scope for this pass.

### Records that resist the kinds/operations model

- **Pure retirements** (`oqn6`, `ous0`): a Correction whose entire content is
  "record N should not exist / was over-captured." No forward arrow, no clarify
  target to sharpen — it *deletes*. In the new model this is a bare `supersede`
  with no replacement, or an auditor retirement. The migration and the
  supersede-op both need to accept a **null replacement** (retire X, propose
  nothing). `578` §4's supersede assumes a replacement record R; the corpus shows
  retire-without-replace is a real, distinct operation. Flag for the operator.
- **Self-referential intent** (`1zmh` *"Intent logging uses Spirit"*, `btio`
  *"Deployed Spirit now has the capacity to REMOVE intent records, superseding
  the append-only/flag-only constraint of record 1091"*): records about Spirit's
  own mechanics that the redesign **obsoletes by building**. `577` §4 already
  named the ~20 self-design records as the bloat being fixed; `btio` is a live
  example of a record that supersedes a *constraint* (1091) — meaning the corpus
  already contains constraint-supersession, which the new Constraint kind plus
  supersede op must handle (a Constraint is not immutable).
- **STT artifacts** (`eegq`, `ospz`): *"misheard ASKI as ASCII"*, *"the original
  psyche quote … was speech-to-text-corrupted."* The corpus carries records whose
  *only* purpose is to correct a transcription error in another record. These are
  pure clarify-in-place operations against the corrupted target; they produce no
  standalone arrow. The migration should treat them as clarifies, not records.

### Things that would surprise an implementer

1. **`Observe` already returns identifiers in v0.8.0.** `577`/`579` (against
   v0.4.0) said reads return bare `Entry` with no `RecordIdentifier`, forcing the
   snapshot-extraction workaround. The deployed v0.8.0 reply is
   `(RecordsObserved [(<id> (<entry>)) …])` — every row is identifier-bearing.
   The `578` §10 "identifier-bearing observation — real first build" gap is
   **already closed in the deployed binary**. Verify against source, but the
   migration/auditor can enumerate-with-identifiers through the contract today.
2. **The certainty floor already hides Zero records in v0.8.0.** The `579`
   de-bloat finding ("marking Zero does nothing") was a v0.4.0 fact; the live
   default count (1366) excludes the 45 Zero records. The soft-tombstone now
   works at query time. So the distill mechanism `578` §10 calls "already in
   source" is genuinely deployed — the build sequence can assume it.
3. **High is the universal default certainty (1109/1366 = 81%).** Agents capture
   at `High` almost always; `Medium`/`VeryHigh`/`Maximum` are rare and
   deliberate. So **certainty barely discriminates** in the current corpus — it
   is near-constant. This is the empirical case for the dedicated **Weight** axis
   (`578` §10): certainty cannot rank because everything is High. Weight (the
   duplicate-refusal counter) is the field that will actually order results;
   certainty mostly just flags the 45 retirement candidates and the 91
   agglomeration canonicals.
4. **Agents cite each other's record numbers constantly** (Spirit 2590, record
   151, record 1088, record 1216, /154 §2.5, /312 §5). The corpus is full of
   cross-references in *prose* — exactly the "discussion in the state" the arrow
   principle (`578` §2) forbids. The migration's biggest single cleanup is
   stripping these citations: they point at ordinal numeric ids from a *previous*
   Spirit version (the hash-identity migration `xfc5` mentions) that no longer
   resolve, so they are not even followable — pure dead discussion scaffolding.

## 6. Summary of implementation implications

- **Guardian duplicate detection** (§1): high-recall via category+keyword+full-text
  catches Grade A reliably; Grade B is conceded to the auditor by design. Make the
  `duplicate`/`contradiction` split conservative — when a record carries a unique
  aspect, do not merge; when records disagree, route to contradiction. On
  genuine doubt, admit and defer to the auditor — a wrong refusal is silent, a
  wrong merge is lossy.
- **Weight bump** (§1): heavy-tailed; a few arrows hit 6–8 restatements. Monotonic,
  no decay is correct. Weight, not certainty, is the real ranking signal (§5.3).
- **Migration** (§2): not 1:1. Three outcomes per legacy record — forward arrow,
  clarify-in-place, or retire-only. ~45 records (35 Corrections + 10
  Clarifications) produce no new record. Build the rewrite pass to emit one of
  three verdicts, and strip dead numeric cross-references.
- **Clarify gate** (§3): the agent's chosen op is a hint, not a fact — agents
  mislabel trample as refine (`y0vr`, `6z6t`) constantly. Default scope-widening
  (`8bea`) to a fresh propose, never a silent clarify.
- **Category catalog** (§4): 15 broad categories cover ~92%; bless multi-membership
  + keyword discriminator to resolve `mail`/`macro`/`trace` collisions.
- **Edge cases** (§5): supersede must accept a null replacement (retire-only);
  Constraints are superseuble (`btio`); privacy is binary in practice; STT-artifact
  corrections are clarifies, not records. And confirm against source: v0.8.0
  already returns identifiers and already hides Zero records — two gaps the older
  reports list as unbuilt are deployed.
