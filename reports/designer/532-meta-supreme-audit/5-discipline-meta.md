---
title: 5 — Discipline Meta (the pattern of the workspace's own patterns)
role: designer
variant: Audit
date: 2026-06-05
topics: [discipline, workspace, meta, skills, intent]
parent_meta_report: reports/designer/532-meta-supreme-audit/
slot: 5
description: |
  The META-SUPREME audit's discipline dimension. Analyzes the
  workspace's OWN disciplines — not the code. Finds the good
  meta-patterns that genuinely cohere across many skills
  (methods-on-nouns, NOTA-as-the-one-language, the triad shape,
  the intent layer as cornerstone, full-English naming,
  source-visibility), names where the workspace breaks its own
  rules or where skills contradict / overlap / have drifted, and
  argues the single pattern-of-patterns the individual rules are
  all instances of: the workspace is a machine for re-introducing,
  by written fiat, the cognitive friction that LLM substrates erased
  — so that every shortcut becomes a typed, named, owned decision.
---

# 5 — Discipline Meta

## Intent Anchors

[Intent is primordial. If any agent needs to know what to do, they
fall back on intent. Whatever intent is clear enough to create enough
signal to warrant action becomes action; the agent's only role is to
clarify intent and capture intent.] (ESSENCE.md §"Intent is the
cornerstone")

[Every reusable verb belongs to a noun. If you can't name the noun,
you haven't found the right model yet — keep looking until you can.]
(skills/abstractions.md §"The one-line summary")

[The rule reintroduces, by fiat in a style guide, the friction the
substrate has erased. It changes what the agent can think, by changing
what it is required to write.] (skills/abstractions.md §"Why this
matters more for LLM agents")

[Smart models can fill in blanks from good high-level guidance;
over-elaborated skills add cost without benefit. When editing a skill,
prefer cutting to adding.] (INTENT.md §"Skills must not grow noisy")

## What this report is

Reports 1–4 of this audit look at the code and the schema stack. This
report turns the lens on the **disciplines themselves** — `ESSENCE.md`,
`AGENTS.md`, `INTENT.md`, and the 66 skill files under `skills/` (64
top-level plus `skills/rust/*`). The question is not "is the code
good." It is: **do the rules cohere, do they contradict, and what is
the single discipline they are all instances of?**

The honest finding is that the discipline layer is genuinely
exceptional — more internally consistent than any rule-system I have
read — AND that it has the specific decay disease its own
`context-maintenance.md` is written to fight: the rule-set has grown
faster than its own garbage-collector runs, so a handful of skills now
carry stale cross-references, a renamed concept under two names, and —
most seriously — **three different report-kind vocabularies that do not
agree**, all inside the one skill (`reporting.md`) that is supposed to
be canonical on the subject.

## The good meta-patterns — disciplines that genuinely cohere

These are not "nice rules." Each one recurs across many skills,
reinforces the others, and is argued from first principles rather than
asserted. This is the rare case where the cross-references are
load-bearing rather than decorative.

### A. The type system is the model (methods-on-nouns, and its family)

The single most-repeated technical discipline. It appears as the same
sentence in four skills: *"the type system is the model. Use it."*
(`skills/abstractions.md:375`), *"the type system carries the meaning"*
(`skills/enum-contact-points.md:542`), *"the type system carries the
discrimination"* (`skills/rust/methods.md:333`), and the apex form in
`ESSENCE.md` §"What I am building": *"every typed boundary names exactly
what flows through it; nothing accidental survives the type system."*

What makes it a genuine meta-pattern rather than four restatements is
that the four are **structurally different rules that bottom out in the
same principle**:

- verb-belongs-to-noun (`abstractions.md`) — behavior on the type that
  owns the data;
- enum-vs-enum cross-product (`enum-contact-points.md`) — the
  relationship between two typed inputs IS a noun, name it;
- domain-values-are-types / don't-hide-typification-in-strings
  (`rust/methods.md`) — once you have the typed identity, use it;
- closed-typed-records-over-flags (`typed-records-over-flags.md`) —
  surface the variant set in the type system.

`abstractions.md` §"Companion disciplines" explicitly names this
convergence — *"all four rules say the same thing in different domains:
the type system is the model."* That cross-skill self-awareness is the
sign of a real meta-pattern, not an accident of repetition.

### B. NOTA as the one language, argued from a load-bearing property

The NOTA-everywhere direction is not asserted as taste. It is grounded
in a single falsifiable property — `nota-codec`'s encoder structurally
cannot emit a `"` (`nota-design.md` §"Quotation marks…"): `write_string`
has exactly three branches and no quote branch. From that one fact the
workspace derives the embedding-safety consequence
(`INTENT.md` §"NOTA is the universal embedding-safe payload"), the
single-argument rule (`component-triad.md` §"The single argument rule"),
the shell-double-quote convention, and config-by-convention. A rule
chain that traces back to a verifiable property of one function is the
healthy shape; this is the cleanest example of it in the workspace.

### C. The triad shape — one shape recognised everywhere

`component-triad.md` carries two triads (repo triad: daemon +
`signal-<component>` + `meta-signal-<component>`; runtime triad: Signal
+ Nexus + SEMA) and is explicit about the collision of the word
"Signal" across them (§"'Signal' names two different schema files").
The runtime triad is anchored in `INTENT.md` Pattern B and realised in
the engine-trait surface. The discipline coheres because every other
architecture skill (`actor-systems`, `contract-repo`,
`micro-components`, `engine-report`) is positioned as *the shape inside
the boundary* this skill draws — the cross-references form a tree with
this file at the root, not a web of mutual citation.

### D. The intent layer as cornerstone, with the innocent-man asymmetry

The strongest discipline in the workspace, and the most carefully
argued. `ESSENCE.md` §"Inferring intent is forbidden" gives it the only
death-sentence framing in the corpus, and the discipline is
**asymmetric on purpose**: understatement leaves a recoverable gap;
over-extension corrupts load-bearing truth (`intent-log.md` §"Conservative
by default"). The pre-capture "erase the task — is it still meaningful?"
gate (`intent-log.md` §"The pre-capture gate") is a genuinely good test
that catches the one failure mode (logging the working order, not the
durable want) the rest of the rule keeps re-warning against. The layer's
precedence is stated identically in `ESSENCE.md`, `INTENT.md`, and
`AGENTS.md` — three surfaces, one rule, no drift. That triple-agreement
is what a healthy keystone rule looks like.

### E. Full-English naming + no-redundant-ancestry as a deliberate pair

`naming.md` is unusually honest that its two rules **pull in opposite
directions and only work together** — full-word without the ancestry
rule yields `IntentRecordIdentifier`; the ancestry rule without
full-word yields `Id`. The skill names the LLM-specific reason it has to
exist (`naming.md` §"Why LLM agents are particularly prone": the prefix
feels safe and tokens are free) rather than treating naming as universal
taste. This is the same self-aware shape as the methods-on-nouns rule.

### F. Source-visibility / show-the-code, not the summary

`reporting.md` §"Psyche reports — show the code, not the summary"
(Spirit 1515 Maximum) makes the introspection value of `ESSENCE.md`
§"What I am building" point 3 a writing discipline: a psyche report
must show the actual lines with file:line, not "~5 lines of CLI
wiring." This is introspection applied to the workspace's own
communication surface — the same principle that makes the runtime
typed makes the reports concrete.

### G. The workspace already names its own meta-patterns

`INTENT.md` §"Recurring architectural patterns" (Pattern A–F) is the
workspace doing exactly this report's job on the architecture
dimension: it indexes which intent records together constitute a
recurring discipline. The existence of that section is itself the
healthiest meta-signal in the corpus — the workspace knows that
patterns-of-patterns are a thing worth naming.

## Where the workspace breaks its own rules

These are real, file:line-grounded, and each is a case of the workspace
violating a discipline it states elsewhere. None is catastrophic; all
are the predictable decay of a fast-growing rule-set whose
garbage-collector (`context-maintenance.md`) runs slower than the
authoring.

### 1. THREE report-kind vocabularies that do not agree — inside one skill

This is the most serious self-contradiction, and it sits in the skill
that is canonical on the subject. `skills/reporting.md` carries:

- §"Kinds of reports — closed set" — a **10-kind** lowercase set:
  `design / audit / research / proposal / review / synthesis /
  handover / postmortem / psyche / update` (verified by grep at lines
  600–611).
- §"Report header — YAML front matter" — a **7-kind** Capitalised
  `variant` set per Spirit 1481: `Psyche / Design / Audit / Research /
  Synthesis / Closeout / Handover` (`reporting.md:799-801`).

These do not reconcile. `Closeout` exists only in the front-matter set;
`proposal`, `review`, `postmortem`, `update` exist only in the
kinds-set. The same skill tells an agent to file a `review`-kind report
(§"Context maintenance" output) and to stamp its front matter with a
`variant` drawn from a set that has no `Review`. A third vocabulary
lands in `context-maintenance.md` §"The Refresh variant", which
introduces a **`Refresh`** variant ("the way Audit / Design / Psyche are
working variants") that appears in neither `reporting.md` set. An agent
following the rules literally cannot produce a front-matter `variant`
that is simultaneously legal under all three. This report itself had to
pick — I used `variant: Audit`, which is the only token legal in both
`reporting.md` sets.

The fix is a single reconciliation pass: pick ONE capitalised closed
set, state it once, and make both the §Kinds table and the front-matter
field cite that one source. Proposed (orchestrator to execute, no
deletion of Spirit records): land a `Refresh`-variant edit to
`reporting.md` that replaces the two divergent lists with one, mapping
`review`→`Refresh`, folding `proposal` into `Design`, `postmortem` into
a retained kind, and naming `update` and `Closeout` explicitly.

### 2. A filename convention that contradicts itself: topic-first vs Variant-segment

`reporting.md` §"Filename convention" (lines 416–444, per records 939 +
941) prescribes **`<N>-<primary-topic>…-<title-slug>.md`** with the
TOPIC first and explicitly says *"The **kind** of the report … moves to
the report's frontmatter or opening section, **not the filename**."* The
worked examples (`390-nota-canonical-design.md`) have no variant
segment. But §"Report header" line 801 says the `variant` *"Matches the
`<Variant>` segment of the filename convention"* — a segment the
filename convention says does not exist. And §"Versioning committed
reports" (line 881) says *"The `-v2-` segment goes immediately after the
report number, before the **variant** or topic"* and gives the example
`493-Design-schema-header-namespace-resolution` — variant-first, the
opposite of the topic-first rule 40 lines up. Three sub-sections of one
skill describe three incompatible filename shapes. (The meta-report
directory I am writing into uses the topic-first form,
`532-meta-supreme-audit`, so the topic-first rule is the de-facto
winner; the Variant-segment references are the drift.)

### 3. "Executor" survives after the rename to "Nexus"

`abstractions.md` still ships the old vocabulary in three places:
the labor-split table reads *"signal/executor/SEMA interaction"*
(`abstractions.md:312`), and §"Schema-emitted nouns" cites
*"`component-triad.md` §'Runtime triad — signal / executor / SEMA'"*
(`abstractions.md:340-341`) — a section heading that no longer exists
(`component-triad.md` renamed it to "Signal / Nexus / SEMA" and states
the rename at lines 20 and 848). So `abstractions.md` cites a section by
its dead name. This violates `naming.md` §"Different scopes get
different names" and the workspace's own *"names don't carry stale
ancestry"* spirit. Low-severity but a live dangling cross-reference.

### 4. ESSENCE references a section that ESSENCE does not contain

`rust/methods.md:438-439` and `designer.md:914` both cite *"ESSENCE
§'Infrastructure mints identity, time, and sender'"* as the apex
statement of the agent-doesn't-mint-identity rule. Grep of `ESSENCE.md`
section titles (verified) shows **no such section** — the nearest
content lives unnamed inside §"Strings only at the edges; the system is
typed." Two skills cite an apex anchor that was never written (or was
renamed/absorbed without updating the citers). Per `ESSENCE.md`'s own
authority hierarchy, a skill citing a non-existent essence section is
exactly the "agent-written surface points at intent layer that isn't
there" failure the precedence rule exists to prevent. Proposed fix:
either add the named §"Infrastructure mints…" subsection to `ESSENCE.md`
(the content already exists, it just needs the heading the citers
assume) or repoint the two citations to the section that holds it.

### 5. The `---` horizontal-rule rule is violated by the skill layer

`AGENTS.md` §"Hard overrides" forbids `---` as a document separator
*"never as a document separator."* `skills/repo-intent.md`'s starter
template (lines 80, 99) uses `---` as a section separator between
`# INTENT` / `## Goals`, and the closing block. The YAML front-matter
`---` in `reporting.md` (lines 774/784) is legitimate (it is YAML
delimiter, an explicit carve-out the rule should name but doesn't). The
`repo-intent.md` template ones are genuine violations being taught as a
template — an agent copying that template propagates the banned shape.
The rule's own carve-out for YAML front matter is also unstated in
`AGENTS.md`, which is the deeper gap: the rule forbids `---` absolutely
but the workspace's own ratified report header (Spirit 1527) *requires*
`---`. The rule needs the YAML carve-out written in.

### 6. Overlap without a single owner: the intent-capture rule is stated in full four times

The "capture intent FIRST / working-orders-are-not-intent" discipline
is fully restated in `ESSENCE.md` §"Logging psyche intent",
`AGENTS.md` §"Capture intent through the right substrate", `INTENT.md`
§"Recording is the first task", and `intent-log.md` §"Recording is the
first task of every psyche-prompt turn" + §"The pre-capture gate." This
is the workspace's own §"Skills must not grow noisy" tension realised:
the rule is so important it is restated everywhere, but four full
restatements mean four surfaces to keep in sync, and they have *already*
begun to diverge in detail (the ladder examples, the magnitude defaults,
the forwarded-prompt exception live in different files at different
resolutions). The keystone rules earn their repetition; but repetition
IS a maintenance debt the workspace's own anti-noise intent flags.

## The pattern of patterns — the single meta-discipline

Every good rule above and every drift below is an instance of one thing.
State it plainly:

**The workspace is a machine for re-introducing, by written fiat, the
cognitive friction that the LLM substrate erased — so that every
shortcut an agent would take frictionlessly becomes instead a typed,
named, owned, captured decision.**

The argument from the skills is direct. `abstractions.md` §"Why this
matters more for LLM agents" states the mechanism in the open:
*"Humans procrastinate creating types because typing `struct
QueryParser` feels heavier than `fn parse_query`. … LLMs have no such
friction. … The rule reintroduces, by fiat in a style guide, the
friction the substrate has erased. It changes what the agent can think,
by changing what it is required to write."* `naming.md` says the same of
the prefix temptation (*"the prefix feels safe and tokens are free …
same procrastination pressure"*). `intent-log.md` says the same of
over-capture (the agent logs the prompt's VERB because it is the
frictionless move; the pre-capture gate forces the harder SENTENCE
test). `nota-design.md` says the same of the `(Item …)` wrapper (*"you'll
notice yourself wanting to wrap every record for safety — don't"*).

Read this way, the apparently-unrelated rules are one rule applied at
every layer where an LLM's zero-friction substrate would otherwise let a
decision slip past unnamed:

- **methods-on-nouns** forces the naming step that a free function
  skips (the Karlton bridge: "the rule exists to make sure naming
  happens");
- **full-English naming** forces the word the abbreviation hides;
- **enum-contact-points** forces the relationship the `if`-chain
  hides;
- **NOTA brackets-only / no-flags** forces the schema field the
  ad-hoc flag hides;
- **intent capture FIRST / working-orders-aren't-intent** forces the
  durable want the working order hides;
- **show-the-code-not-the-summary** forces the actual lines the
  line-count summary hides;
- **report kinds + permanent homes** force the destination the
  accumulating report hides.

Each rule's stated rationale is the same two-move shape: (1) the LLM
substrate makes the wrong shape costless, so the agent defaults to it;
(2) the rule prices the wrong shape back in by *requiring* the right
one. The intent layer is the apex case: it is friction re-introduced
around the single act — composing intent the psyche did not state — that
is most costless for an LLM and most corrupting to the system
(*"inferring is the discipline breaking; asking is the discipline
working"*).

And — this is the closing of the loop — **the drifts in this report are
the meta-pattern failing on its own author.** Every divergence I found
(three report vocabularies, the topic-vs-variant filename contradiction,
the dead "executor" cross-reference, the missing ESSENCE section, the
`---` violation) is a place where *writing the rule was frictionless and
keeping it in sync was not.* The workspace re-introduces friction
brilliantly at the point of authoring code and capturing intent; it has
not yet re-introduced friction at the point of **editing a rule that a
second rule depends on.** The garbage-collector (`context-maintenance.md`,
`skill-editor.md` §"Skills never reference reports") exists precisely to
be that friction, but it runs on human/agent initiative, not by fiat at
the edit moment — so it lags. The auditor role (`AGENTS.md` §"Possible
additional role — auditor", Medium certainty, DeepSeek, "mostly
mechanical … finds flaws or bad patterns … broke rules that we have") is
the workspace's own proposed answer: a fiat-friction at the rule layer,
the same way the PreToolUse hook is fiat-friction at the Rust-authoring
layer. The discipline-meta finding is that **the auditor is not
optional polish; it is the missing instance of the workspace's own
founding pattern, applied to the rule-set itself.**

## Proposed maintenance (orchestrator executes; no deletions here)

All are `Refresh`/in-place skill edits, not Spirit-record or report
deletions. Landing witnesses named.

1. **Reconcile the report-kind vocabulary** — one capitalised closed
   set, cited once, in `reporting.md`; map `review`/`Refresh`,
   `proposal`, `update`, `Closeout`. Witness: a single grep of
   `reporting.md` + `context-maintenance.md` returns one variant list.
2. **Resolve the filename convention** to topic-first (the de-facto
   winner); delete the two "`<Variant>` segment of the filename"
   references in §"Report header" and §"Versioning". Witness: no
   `<Variant>`-segment language survives in `reporting.md`.
3. **Repoint the "executor" cross-references** in `abstractions.md:312,
   340-341` to "Nexus" and the live `component-triad.md` section title.
4. **Add the §"Infrastructure mints identity, time, and sender"
   heading to `ESSENCE.md`** (content exists, heading does not) OR
   repoint `rust/methods.md:438` and `designer.md:914`.
5. **Write the YAML-front-matter carve-out into `AGENTS.md`'s `---`
   rule**, and de-`---` the `repo-intent.md` template.
6. **Carry the auditor proposal forward** as the rule-layer instance of
   the friction-re-introduction pattern — the discipline-meta argument
   above is the case for promoting it from Medium certainty.
