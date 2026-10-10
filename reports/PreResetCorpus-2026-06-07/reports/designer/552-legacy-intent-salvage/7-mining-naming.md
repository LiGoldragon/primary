---
title: 552 — Legacy intent salvage — mining naming.nota
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, naming, contract-repo, legacy-nota, deletion-readiness]
description: |
  Mining report for naming.nota (21 records). Finds the few core, durable,
  not-too-specific naming/contract-verb design ideas that are genuinely at
  risk on deletion — not already in Spirit and not already manifested into
  ESSENCE / AGENTS / skills.
---

# 552 — Mining naming.nota

## Scope

Scanned `/tmp/intent-text/naming.txt` = `intent/naming.nota`, 21 records.
Surfaced **2 strong candidates** plus **1 weaker (partly-preserved) flag**.
The bulk of the file — the no-redundant-ancestry rule, the no-abbreviations
rule, the acronym exception test, the repeated-category-words schema smell,
the verb-form-not-noun-form rule, the signal-types vocabulary — is already
deep in `ESSENCE.md` / `AGENTS.md` / `skills/naming.md` /
`skills/contract-repo.md` and in the deployed Spirit store. The file is
nearly fully preserved.

## Salvage candidates

### 1. Verb/noun homograph collisions in operation roots are not a problem — position disambiguates

- **Kind:** Decision
- **Proposed topics:** `naming contract-repo positional roots verbs disambiguation`
- **Proposed description:** A word that is both a verb and a noun (a
  homograph) may serve BOTH roles inside one contract — the position in the
  contract structure disambiguates, no rename needed. The operation-root
  position implies the verb interpretation; the payload position implies the
  noun interpretation. Example: `State` as the verb (psyche stating intent)
  and `State` as the noun (presence-state) coexist in one contract; the
  reader picks the meaning from position. This is the verb-form-not-noun-form
  rule's natural complement: that rule forces the verb spelling at the
  operation root, and this one says the resulting collision with a noun of
  the same spelling is a non-problem, because position already typed it.
- **Proposed certainty:** High (legacy Maximum, but settling a "hole"; honest
  High)
- **Supporting verbatim:** [I don't really see a problem since if we expect a
  verb then we would interpret it as a verb] (record 20, Maximum)
- **Preservation check:** Spirit
  `(Observe (Records ((Partial [naming positional verbs roots
  disambiguation]) None Any VeryDeep SummaryOnly)))` returned the naming set
  (k1i1, edgt, p1pj, w85v, etc.) — none state the homograph/position-
  disambiguates rule. `rg -in 'homograph|position.*(verb|noun)|same word.*(verb|noun)|expect a verb'`
  over `skills/contract-repo.md skills/naming.md skills/language-design.md`
  found only the namespace-disambiguator usage and `language-design.md`'s
  "position defines meaning" for delimiters — NOT the verb/noun homograph
  rule at the operation root. Not preserved.
- **At-risk rationale:** `skills/contract-repo.md` mandates the verb spelling
  at the root but never tells an agent what to do when that verb spelling
  collides with a noun of the same word elsewhere in the contract. Without
  this record, an agent that hits `State` (verb) vs `State` (noun) will
  invent a disambiguating rename — exactly the over-declarative-naming the
  workspace is trying to kill. The rule that makes the collision safe lives
  only here.

### 2. Compound (agglutinated) contract verbs are valid when the action is a single atomic sequence

- **Kind:** Decision
- **Proposed topics:** `naming contract-repo verbs roots`
- **Proposed description:** A compound contract verb is fine when the action
  it names does not decompose cleanly into separate operations — e.g.
  `DrainAndStop` as one operation root when the action is a single atomic
  graceful-shutdown sequence (drain, then stop). Do NOT split a single atomic
  action into multiple operations merely because English wants two words. The
  English language's lack of a single word for the compound is a limitation
  to accept, not a problem to design around. Complements the verb-form rule:
  the root is still a verb; it is just an agglutinated one.
- **Proposed certainty:** High (legacy Maximum on a narrow corner case;
  honest High)
- **Supporting verbatim:** [if we need an action that's drain and stop order,
  then that's what we call it. I don't really see a problem with that. It's
  just a limitation of the English language.] (record 21, Maximum)
- **Preservation check:** Spirit
  `(Observe (Records ((Partial [naming verbs roots compound]) None Any
  VeryDeep SummaryOnly)))` — the only "compound" hit was record uara about
  Spirit TOPIC compound-phrases, unrelated. `rg -in
  'compound|agglutinat|DrainAndStop|single atomic|does not decompose|limitation of (the )?English'`
  over `skills/contract-repo.md skills/naming.md skills/language-design.md
  skills/component-triad.md ESSENCE.md AGENTS.md` returned nothing for the
  compound-verb idea. Not preserved.
- **At-risk rationale:** The schema-shape discipline pushes hard toward
  decomposition (the repeated-category-words smell, "more separation is
  better"), so an agent applying that discipline reflexively will try to
  split `DrainAndStop` into `Drain` + `Stop` and break an atomic action. This
  record is the explicit counter-balance — the one place the psyche says some
  actions are genuinely atomic and the single compound verb is correct.
  Without it the deletion removes the only guard against over-decomposition
  of atomic operations.

## Weaker flag (partly preserved — psyche's call)

### "More separation is better" as a standalone axiom

- **Kind:** Principle
- **Why flagged:** Record 7 carries the general axiom [More separation is
  better.] as the rationale behind the repeated-prefix/suffix schema smell.
  `skills/naming.md` §"Anti-pattern: repeated category words" fully captures
  the SYMPTOM (repeated category words are schema smells, find the missing
  parent layer, grow into a tree) but never states the underlying axiom as a
  general principle. The axiom is broader than the naming anti-pattern — it
  guides schema shape, abstraction boundaries, and crate splits.
- **Recommendation:** Marginal. The symptom-level guidance is strong enough
  that an agent reaches the right behaviour without the axiom. Include ONLY
  if the psyche wants the bare principle stated; otherwise the naming.md
  anti-pattern preserves the practical effect. Lean: DROP unless the psyche
  values the standalone axiom.
- **Supporting verbatim:** [when data types show up a pattern in the names
  where the same prefix or suffix keeps popping up, that is probably a sign
  that there is a logic separation that is being stuffed inside the names …
  More separation is better.] (record 7, Medium)

## Already preserved / dropped

Confirmed preserved (safe to delete), with where each lives:

- **Records 1, 3 (no-redundant-ancestry / names don't carry full ancestry)** —
  `AGENTS.md` hard override "Spell every identifier as a full English word
  AND names don't carry their full ancestry", `ESSENCE.md` §Naming,
  `skills/naming.md`. Spirit covers the concrete applications (p1pj, edgt,
  9npk, k1i1).
- **Records 2, 11, 12, 13 (specific repository-ledger renames; the lost-intent
  recovery task; "query is its own logic plane")** — too specific (one-off
  rename orders / a recovery task that has run) AND the durable core
  (repeated-category-words = missing parent layer) is in `skills/naming.md`
  §"Anti-pattern: repeated category words" and `skills/contract-repo.md`. The
  task-shaped parts ("rename everything", "find the lost intent") die with
  the task — not intent.
- **Records 4, 6 (no-abbreviations / acronym exception test)** — `AGENTS.md`
  hard override, `ESSENCE.md` §Naming, `skills/naming.md` (identifier-not-id,
  the "has it become the English word" acronym test). Fully preserved.
- **Record 5 (both naming rules land in every coding guidance file as a
  pair)** — manifestation directive that has been executed; the paired rules
  now live in `AGENTS.md`, `ESSENCE.md` §Naming, `skills/naming.md`. The
  directive itself is task-shaped (the manifestation happened).
- **Record 7 (repeated prefixes/suffixes indicate missing schema separation)**
  — symptom preserved in `skills/naming.md` and `skills/contract-repo.md`
  (`*Query`/`*Command`/`*Event` repeated-suffix row). Only the bare axiom is
  flagged above as marginal.
- **Records 8 (signal types vocabulary), 14, 17 (signal-sema / core-verb
  reconsideration)** — record 8's "signal types" vocabulary is live across
  `AGENTS.md` component-triad override and `skills/component-triad.md`;
  records 14/17 are low-certainty (Minimum) open brainstorming, not durable
  intent. The Sema-vocab-off-the-public-wire direction they circle is settled
  and preserved in Spirit (`7l7l`) and `skills/contract-repo.md` §"What moved
  below the public contract".
- **Records 9, 10 (over-declarative names / schemas grow into trees not flat
  tables)** — preserved in `skills/naming.md` §"Anti-pattern: repeated
  category words" ("where the schema should grow into a tree", "missing
  parent enum").
- **Record 15 (authorize landing the /237 skill edits + file refactor bead)** —
  pure task order; the edits landed and the bead was filed. Dies with the
  task.
- **Record 16 (public contract verbs decided case-by-case, no universal
  rule)** — the no-universal-rule stance is reflected in
  `skills/contract-repo.md` (the verb threshold is "behavioral, not numeric";
  the correction "is not automatic"). Effectively preserved; the bare meta-
  statement is not load-bearing on its own.
- **Record 18 (subscription-driven introspection logging, not log-everything)**
  — Medium-certainty and OUTSIDE the naming domain (observability/logging
  policy). Not a naming candidate; if at risk it belongs to a logging/
  introspection miner, not this file's naming scope. Noted as out-of-scope
  here.
- **Record 19 (verb-form not noun-form: State not Statement)** — fully
  preserved in `skills/contract-repo.md` §"The operation root is a verb, in
  verb form" (Submit/Query/Observe/Configure/State examples verbatim).
- **Record 20, 21** — the two surviving candidates above.
