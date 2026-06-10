# Spirit implementation audit — design fidelity against 578

An audit of operator's implementation (the work in `/git/github.com/LiGoldragon/spirit`)
against the agreed design `578-intent-redesign-synthesis.md`, the corpus guidance
`580-spirit-implementation-guidance/`, and the **live production corpus** (read-only
queries against the deployed v0.8.0 daemon, ~1418 records).

Method: a 7-dimension fan-out (axes, categories, write-ops, guardian,
state/stream/archive, keywords/retrieval, migration/kinds), each dimension's
findings adversarially re-verified against source by an independent checker. Every
claim below opens to a `file:line` or a commit or a live query. Two of my own
findings were **refuted on verification** and are corrected in §7 — the audit
checked itself.

A caveat on timing: the fan-out ran while operator was mid-edit on the weight
axis, so the auditors caught a moving target (one saw a 7-field `Entry`, another a
6-field one). I reconciled the axis state to the current committed HEAD myself
(§5); the non-axis findings are stable and independent of that churn.

## 1. Verdict in one line

**The structure is largely faithful; the *content* of the category catalog and the
*reach* of the guardian gate diverge from the design's core premises.** Operator
built nearly the whole frontier — categories, keywords, the four write-ops,
archive, the guardian path — and the *shapes* are right. What's missing is the part
that makes intent trustworthy: a discriminating index and a gate that actually
guards more than one of the four write paths.

Three things need the psyche's call (§8): the **axis decision** (weight was just
dropped — confirm the reason), the **category catalog** (the headline — proven too
abstract), and re-affirming that **the guardian must gate clarify/supersede, not
just propose**.

## 2. What is faithful — the balanced ledger

The audit is not a hunt; a lot landed correctly. Verified `matches`:

- **Write-op surface.** Propose / Clarify / Supersede / Retire exist as four
  distinct typed operations, each with its own receipt and its own `IntentEvent`.
  Retire-only is a *separate* pure-retraction path, and `Supersession` carries a
  **non-optional** replacement — so the two paths can't be conflated. Faithful to
  578 §4/§8. (`schema/signal.schema:12-31,154-161`)
- **Typed binary verdict.** `GuardianVerdict [Accept (Reject)]` with a typed
  `GuardianRejectionReason` enum, and `GuardianRejection` carries snapshot-refs
  (`RecordSet`) + `Explanation` + `DatabaseMarker`. Exactly the 578 §4 shape.
  (`schema/signal.schema:162-163`)
- **Fail-closed.** Every guardian failure (socket down, malformed, timeout) maps to
  `GuardianRejected`; `Propose` never silently degrades to `Record`. Code-verified.
- **Keywords are extracted on-the-fly from markdown asterisk spans** —
  `Description::keywords()` (`src/store.rs:902-926`), no stored field on `Entry`, no
  drift. This is *exactly* 578 §7 ("derive keywords on the fly, no stored field").
  The extractor case-folds, dedupes, and treats a multi-word span as one phrase.
  Validated and tested. A genuinely clean piece of work.
- **Full-text** (`TextMatch::ContainsText`) is a case-folded substring check,
  empty-rejected, tested.
- **State-vs-stream split.** The subscription stream carries all four
  `IntentEvent` kinds, delivered ephemerally and **never persisted**; the durable
  archive (commit `3d59bd6`) copies each predecessor into a *separate*
  `*.archive.sema` database **before** mutate/remove, outside the live query
  surface. `CollectRemovalCandidates` archives-before-retract. Default observation
  floors out Zero-certainty tombstones (live: 1373 visible vs 1418 with explicit
  `Any` — 45 hidden-not-deleted). All faithful to 578 §3 and operator 352 §5.
- **Category *type*** is closed, multi-membership (`Vec`), enlargement-gated —
  structurally exactly 578 §6. (The *content* is the problem; see §3.)
- **Schema-version migration chain** V1→V5 is additive and faithful in shape.

## 3. Headline — the category catalog is too abstract (the psyche's instinct, proven)

Operator shipped 12 abstract gerunds (commit `0fd5159`, `schema/signal.schema:54`):

```
Category [Being Knowing Meaning Making Relating Governing Caring
          Sustaining Dwelling Moving Valuing Expressing]
```

The psyche's reaction — "not a fan, feels very abstract" — is **empirically
correct**, on three independent lines of evidence:

**(a) It does not file — 81% ambiguity.** Test-filing 32 real records against the
12 gerunds, 26/32 plausibly fit two or more. The Making/Meaning boundary is the
chief offender: almost any schema/code arrow ("schema-generated Rust emits into
`src/schema`", "NOTA thin structural library", "schema roots are positional") reads
as both *Making* (you build it) and *Meaning* (it's the schema language). `Being`
fit none of the 32.

**(b) It does not discriminate — the live store is lopsided and half-dead.**
Read-only per-category counts against production v0.8.0 (1418 visible):

| Category | Records | | Category | Records |
|---|---:|---|---|---:|
| Meaning | **924 (65%)** | | Caring | 16 |
| Making | 387 | | Being | **0** |
| Governing | 300 | | Knowing | **0** |
| Relating | 145 | | Dwelling | **0** |
| Sustaining | 119 | | Moving / Valuing / Expressing | **0** |

Six of twelve categories hold **zero** records; `Meaning` alone holds **65%** — no
better than the old leaky free-text top-token `schema` (~28%), in fact worse.
`Meaning` and `Making` co-occur on 213 records — the ambiguity made concrete.

**(c) Root cause is in the migration matcher.** `Category::push_from_label`
(`src/engine.rs:794-882`) has match arms for only **6** of the 12 gerunds, uses
substring `contains` matching that false-positives ("im**personal**ly" → Caring,
"**persona**" → Relating), and defaults every unmatched topic to `Meaning`
(`engine.rs:880`). So six gerunds are structurally unreachable and `Meaning` is the
sink. The catalog is largely cosmetic.

**Why this is the most important finding:** the category spine is the retrieval
foundation the guardian stands on (578 §5). A 65%-in-one-bucket, half-empty index
means guardian retrieval inherits *exactly* the recall failure the redesign set out
to kill — and it compounds with §4's category-only retrieval into a real failure
mode (a `Meaning`-tagged Propose pulls ~924 records as its "relevant" bundle).

**Proposed grounded alternative** (derived from the real corpus work-domains; the
580 §1 table, costed against live token counts). ~15 categories that *discriminate*
because they name what the work is actually about:

| Category | Covers | ~records |
|---|---|---:|
| `schema` | schema, schema-language, namespace, macro, enum, struct, newtype, roots, variants | ~441 |
| `spirit-intent` | spirit, intent, certainty, importance, agglomeration, identifiers, supersession, query | ~214 |
| `workspace-process` | workspace, orchestrate, workflow, roles, reports, beads, discipline | ~206 |
| `signal-wire` | signal, nexus, sema, wire-contract, codec, rkyv, router, mail, meta-signal, envelope | ~177 |
| `infra-deploy` | cloud, criomos, nix, deploy, prometheus, zeus, cluster, horizon, secrets, production | ~141 |
| `component-shape` | component-triad, daemon, runtime, contract-daemon-split | ~140 |
| `nota` | nota, nota-next, syntax, delimiters, symbol, string, vector, parser | ~162 |
| `persona-llm` | persona, pi, local-llm, llm, harness, browser-use, model | ~86 |
| `testing` | tests, fixtures, verification, vm-testing, trace, tracing | ~59 |
| `rust-code` | rust, emission, methods, traits, lowering, crate-layout, engine | ~54 |
| `repo-vcs` | repository, version-control, branches, worktree, jj, integration | ~44 |
| `naming-language` | naming, language, vocabulary, readability | ~33 |
| `agent-behavior` | agents, autonomy, resilience, retry, subagents, effort, focus | ~28 |
| `personal-affairs` | assistant, counselor, personal-affairs, mail (email), access | ~24 |
| `forge-build` | forge, build-system | small/emerging |

In fairness to the gerund approach: it is small, fixed, and stable, and it tries to
be domain-independent (it would survive the workspace changing what it works on).
But intent retrieval needs a catalog that *separates this corpus*, and abstract
verbs-of-being don't. The grounded set keeps the largest bucket near ~30% and gives
every category real mass.

## 4. The gate is thinner than the design's core premise

The design's central claim is "the daemon **is** the guardian" — every durable
capture passes a consistency gate. What shipped gates **one of four** write paths.

- **[critical] Supersede performs no consistency recheck of the replacement.** Not
  "against everything except X" — against *nothing*. `Supersede` writes its
  replacement straight through the un-guarded `store.propose`/raw write. This is the
  exact question the psyche raised in design ("when an agent supersedes X with R,
  does R still get checked against everything except X? — absolutely") — and it is
  **unimplemented**. A wide-open side door for injecting inconsistency, precisely
  what 578 §4 forbids. *(verified real, critical)*
- **[high] Clarify never reaches the guardian.** The clarifies-vs-tramples-vs-
  loses-aspects judgment the psyche designed clarify *around* does not run. The
  reasons `ClarifyTramples`, `ClarifyLosesMeaning`, `SupersedeTargetMissing` (and
  `Compound`, `HarnessTimedOut`) are **dead enum variants with zero code paths**.
  `Clarify` writes straight to the store. *(verified real, high)*
- **[high] The gate is Propose-only; Clarify / Supersede / Retire bypass it
  entirely.** (`src/nexus.rs:417-439` — only the `Propose` arm routes through
  `guard_propose`.) *(verified real, high)*
- **[high] `Record` is a raw, un-gated write path.** A hole in "every capture is
  gated" (`src/nexus.rs:717-719`). Operator flagged this themselves in 354. *(verified
  real, high)*
- **[high] The guardian does not independently classify the operation.** It trusts
  the caller's chosen op; the 580 §4 "you said clarify but it tramples → refusal"
  check is absent. *(verified real, high)*
- **[high] Guardian retrieval is category-only.** `guardian_records_for`
  (`src/store.rs:469-480`) hard-codes `KeywordMatch::Any` and `TextMatch::Any`, so
  the 578 §5/§7 "category + keyword + full-text" bundle is **not** what the model
  receives. On the abstract catalog this is severe: a `Meaning`-tagged Propose dumps
  ~924 records into one prompt. The keyword extractor (§2, built and tested) is right
  there — it just isn't wired into the guardian's own retrieval. *(verified real, high)*
- **[medium] The 578 §4a agent-daemon broker is not built.** What shipped is a
  direct synchronous `signal-agent` Unix-socket `Call(Prompt)` — a reasonable v1,
  but with none of the §4a `HarnessLease` / capability-token / warm-pool / budget-
  accounting properties. Worth a conscious "defer" decision, not a silent gap. *(verified
  real, medium)*
- **[medium] "Zero discretion" is realized by a non-deterministic model-prompted
  guardian.** That is a premise gap worth naming: the design wanted a mechanical
  yes/no; an LLM verdict is inherently variable. Acceptable as v1, but it is not the
  "zero discretion" the design promised. *(verified real, medium)*

Net: the typed-verdict scaffolding (§2) is good, but it only protects the Propose
door. The other three doors are open, and the most consistency-critical one
(supersede) writes blind.

## 5. The axis decision — weight was just dropped; confirm the reason

Live timeline, reconciled by me against current HEAD:

- The design churned: `28438ae` split certainty+weight → `73cb457` renamed weight→
  importance → `11b907f` re-added weight as a separate integer axis → and now, as of
  this audit, **`8fe88d6` "drop weight axis and return uid-only creation replies"** is
  HEAD, with a clean tree. `Entry` is back to **6 fields** (`Categories Kind
  Description Certainty Importance Privacy`); zero weight references.
- The **deployed daemon is still v0.8.0 three-axis** (it accepts an 8-field query,
  rejects 7). So source (two-axis) and production (three-axis) disagree until the
  next deploy.

The thing to flag: in the live chat that triggered this, the stated reason was
*"there is no weight, weight was renamed to importance."* That's a **factual
error** — weight was renamed away at `73cb457` but re-added as a *distinct integer
axis* 18 minutes later (`11b907f`), and operator's CLI explanation was correct.
Even the psyche mixed up the two axes in real time. So the removal may be the right
simplification, but it was triggered by a confusion, not a considered "I don't want
a derived reaffirmation signal" decision.

What dropping weight actually costs / changes:

- **Lost:** the only *derived* (vs declared) ranking signal. Certainty is currentness
  and is near-flat (88% High+); importance is *declared*, not measured, and is also
  near-flat (7/1418 above Minimum). Weight was the one axis meant to *rise on its
  own* via duplicate-refusal — the 580 anti-bloat engine. With it gone, nothing in
  the store derives "how load-bearing is this."
- **Changed semantics:** the duplicate-refusal bump now fires on **importance**
  (the mid-revert renamed `BumpWeight`→`BumpImportance`). So a duplicate proposal now
  raises the existing record's *priority* — conflating "psyche-declared priority"
  with "independently re-arrived-at." That may be fine (re-arrived-at things *are*
  arguably more important), but it's a real semantic merge to confirm.
- **In practice it barely matters yet:** weight was **inert** in production — 0
  records had weight ≥ 2; the bump never once fired on real traffic. At current scale
  the whole axis question is close to academic.

**Recommendation:** dropping to two axes is a *defensible* simplification (it's the
"Concorde airplane" instinct, applied), but make it knowingly. Either (a) keep it
dropped and accept importance-doubles-as-reaffirmation, or (b) restore weight if you
want a derived signal distinct from declared priority. Given the data shows both
derived axes inert, (a) is the simpler honest choice — but confirm it's intent, not
a side effect of the naming confusion. And verify HEAD `8fe88d6` builds across all
features (the mid-flight state didn't — §7).

## 6. Migration — shape was migrated, substance was not

- **[high] The kind-fold was not applied.** `Kind` is still `[Decision Principle
  Correction Clarification Constraint]` (`schema/signal.schema:163`), and **397
  legacy records** (194 Correction + 203 Clarification, ~28% of the store) still sit
  as those kinds in production. `kind_from` is a verbatim 1:1 passthrough
  (`production_migration.rs:566-574`). So we now have **both** a `Clarification`
  *kind* and a `Clarify` *op*, a `Correction` *kind* and a correction *event* — a
  deliberate-but-incomplete two-track. 578 §8 wanted these folded *out* of `Kind`
  into operations. *(verified real, high)*
- **[high] Topic→category ran via a crude substring heuristic, not the psyche-
  blessed reviewable mapping** (§3c). The 580 §1 "psyche blesses the catalog" step
  was skipped. *(verified real, high)*
- **[medium] No agglomeration / de-bloat ran.** The store is still ~1418-1420 — it
  *grew*, it didn't shrink. The 45 Zero-certainty records are the *manual* 579 marks,
  not a migration-driven fold. The de-bloat keystone (`CollectRemovalCandidates`) is
  built and tested but hasn't been run as a distillation pass on production. *(verified
  real, medium)*

So: the schema is ahead of the data on the kind-fold, and the data was migrated in
*shape* but never *distilled*. The 1418 records are the same 1418, now wearing
mostly-`Meaning` category tags.

## 7. Corrections to my own audit (verification caught two)

Honesty about the fan-out's own errors:

- The axes auditor's **critical "the tree does not build in any configuration"** was
  **refuted** — the cited build failures and file:lines were drawn from a stale
  revision; the auditor caught operator mid-edit. The *tree-shape* observation (an
  in-flight two-axis revert existed) was true but is now moot: it's committed as
  `8fe88d6` with a clean tree. (I re-verified the current state directly; a fresh
  build check is running.)
- The keywords auditor's **high "the CLI cannot express a keyword/full-text query"**
  was **refuted** — the discriminator *is* reachable through the deployed bundled
  CLI, just not through the legacy positional shorthand grammar the auditor
  inspected. Downgraded to low.

Everything else in §3-§6 survived adversarial verification with severity intact (a
few were judged *understated*).

## 8. Decisions for the psyche, and what operator should do next

**Psyche decisions (intent-level):**

1. **Category catalog.** Replace the 12 abstract gerunds with a grounded
   work-domain catalog (§3 proposes ~15). This is the highest-leverage fix — the
   guardian can't be trustworthy on a half-dead index. *(I'd also like to record the
   durable principle behind your instinct — see the capture note below — pending your
   wording.)*
2. **Axis.** Confirm weight stays dropped (two-axis: certainty + importance, with
   duplicate-refusal bumping importance), or restore it as a distinct derived signal.
   My lean: keep it dropped — both derived axes are inert at this scale and simpler is
   honest — but confirm it's intent, not the naming confusion.
3. **Gate reach.** Re-affirm the design premise that clarify and supersede must be
   guarded (they currently aren't). This is yours because it's a restatement of
   intent the implementation diverged from.

**Operator work (no psyche call needed, ordered):**

1. Wire `guardian_records_for` to use **keyword + full-text**, not category-only
   (the extractor already exists) — and re-author the category migration off the
   blessed catalog once §8.1 lands.
2. Route **Clarify** and **Supersede** through the guardian; give the dead reasons
   (`ClarifyTramples`, `ClarifyLosesMeaning`, `SupersedeTargetMissing`) real code
   paths; make supersede recheck the replacement against the rest.
3. Decide `Record`'s status — restrict/rename it, or accept it as a deliberate
   escape hatch and document it as such.
4. Finish the kind-fold (fold Correction/Clarification out of `Kind`; migrate the
   397 legacy records through the agglomeration machinery, not a 1:1 passthrough).
5. Run a real de-bloat/agglomeration pass on production (the keystone is built).
6. Verify HEAD `8fe88d6` builds across all features before any redeploy.

**Spirit-gate capture candidate** (not yet recorded — awaiting psyche wording): a
durable Principle that *Spirit categories must be grounded in the corpus's real
work-domains, not abstract universal taxonomies* — the generalizable form of the
"too abstract" instinct, now backed by the 81%-ambiguity / 65%-in-one-bucket
evidence. Recommend recording once the new catalog is blessed, so the principle and
its first instance land together.

## Appendix — finding ledger (post-verification severity)

| Dim | Finding | Verdict | Sev | Verified |
|---|---|---|---|---|
| categories | Catalog half-dead, 65% in `Meaning` | diverges | critical | real |
| categories | Migration matcher reaches only 6/12, defaults to Meaning, substring FPs | diverges | critical | real |
| categories | 12 gerunds → 81% ambiguous | diverges | high | real (understated) |
| categories | Category *type* closed/Vec/enlargement-gated | matches | info | — |
| write-ops | Supersede performs **no** replacement recheck | missing | critical | real |
| write-ops | Clarify never reaches guardian; reasons are dead code | missing | high | real |
| write-ops | Record is a raw un-gated write | diverges | high | real |
| write-ops | Four ops exist, correct shapes; retire-only separate | matches | info | — |
| guardian | Retrieval category-only (keyword/text disabled) | diverges | high | real |
| guardian | No independent op-classification; clarify/supersede/retire bypass | missing | high | real |
| guardian | Typed verdict + snapshot-refs + fail-closed | matches | info | — |
| guardian | §4a broker not built (direct socket v1) | diverges | medium | real |
| guardian | "Zero discretion" via non-deterministic model | unclear | medium | real |
| migration | Kind-fold not applied (397 legacy kinds live) | missing | high | real |
| migration | Topic→category via heuristic, not blessed mapping | diverges | high | real |
| migration | No agglomeration/de-bloat ran (store still ~1418) | missing | medium | real |
| migration | Schema-version chain V1→V5 additive | matches | info | — |
| keywords | Keywords extracted from asterisk spans, no stored field | matches | info | — |
| keywords | Extractor case-folds/dedupes/phrases, tested | matches | info | — |
| keywords | Asterisk edge-cases + AnyKeyword path untested | diverges | medium | real |
| state/stream | Events ephemeral, never persisted | matches | info | — |
| state/stream | Archive predecessors to separate db before mutate | matches | info | — |
| state/stream | Default obs floors Zero tombstones (45 hidden) | matches | info | — |
| axes | Weight dropped (HEAD `8fe88d6`); deployed still 3-axis | diverges | — | reconciled by me |
| axes | Weight mechanics (when present) matched 578 | matches | info | — |
| axes | "Won't build in any config" | — | — | **refuted** |
| keywords | "CLI cannot query keyword/text" | — | low | **refuted** |

Workflow run `wf_1028bcae-695` (35 agents, 7 dimensions + adversarial verification).
