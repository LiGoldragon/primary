---
title: 533/4 — Discipline + content forks — what's hygiene, what needs the psyche
role: designer
variant: Psyche
date: 2026-06-05
parent_meta_report: reports/designer/533-deep-situation-report/
slot: 4
topics: [discipline, content, reporting, intent, subagent, quality]
description: |
  Slice 4 of the deep situation report. Re-examines the five discipline
  drifts the 532 meta-audit flagged — sync-debt on the intent-capture
  rule, three disagreeing report-kind vocabularies, a self-contradicting
  filename convention, dangling cross-references, and lane-vs-topic
  maintenance authority — and tests each against the CURRENT contract
  files. Finding: most are now SETTLED in one file and contradicted in
  another (pure sync-debt the designer can just-fix), but two are genuine
  forks. The lane-vs-topic point is already canonical and needs no
  blessing. The live fork is what record ui5d implies — a NEW
  quality-discipline statement (do-it-properly-or-not-at-all) that is
  captured in Spirit but inlined in NO skill, and whose teeth (block
  the dispatch, or just verify after) the psyche has not yet set.
---

# 533/4 — Discipline + content forks

## Intent Anchors

[Do work properly or not at all — stop burning psyche tokens on
half-assed slop. Do not dispatch underspecified or wrong-shaped
subagent work that produces garbage. Either specify and execute the
work correctly with proper oversight and verification, or do not start
it. Delegating a flawed brief and then surfacing the gap as if the work
were acceptable wastes the psyche's tokens and attention.] (record ui5d,
Correction, High, 2026-06-04)

[Cluster-data node-service features must be TYPED end-to-end, never
string-keyed. The VmTesting work was garbage... The correct order is
typed-source-first... not consumption-first against a string.] (record
qkvx, Correction, High — the sibling incident ui5d generalises from)

[Reports use standard YAML front matter for metadata... Report filename
convention is reports/<role>/<N>-<Variant>-<topic>-<date>.md where
<Variant> is a capitalized word naming the report kind. Every report
has a variant.] (Spirit 1481, Decision High, 2026-06-03, cited in
report-naming.md)

[Agglomerate by topic, not by lane: one topic's reports across all
lanes collapse into one report on it.] (context-maintenance.md §"The
goal", already canonical)

## What I tested, and what changed since 532

The 532 meta-audit named five discipline drifts. I re-checked each
against the live contract files today. Three have since been SETTLED in
their canonical home and merely contradicted in a stale second home —
that is sync-debt the designer just-fixes, not a fork. Two are real
forks. I sort them below so the psyche only spends judgment where
judgment is actually owed.

## Just-do hygiene (no psyche judgment needed)

### H1 — The report-kind vocabulary is already settled; reporting.md is stale

The 532 audit found "three disagreeing report-kind vocabularies in
reporting.md." They are real and I can name all three:

- **reporting.md §"Kinds of reports" table** lists ten lowercase kinds:
  `design audit research proposal review synthesis handover postmortem
  psyche update`.
- **reporting.md line 453** (mid-document prose) lists eight:
  `design / audit / research / proposal / review / synthesis / handover
  / postmortem` — drops `psyche` and `update`.
- **reporting.md §"Report header"** `variant` field lists seven
  PascalCase: `Psyche Design Audit Research Synthesis Closeout
  Handover` — adds `Closeout`, drops `proposal review postmortem
  update`.

But this is no longer an open question. `skills/report-naming.md`
(lines 31-48) carries the CANONICAL nine-variant set —
`Psyche Design Audit Research Synthesis Closeout Handover Update
Refresh` — and grounds it in two ratified Decisions: Spirit 1481
(filename convention with `<Variant>`) and Spirit 2577 (the `Refresh`
variant for context-maintenance output). The designer reports on disk
already follow it: 7 `Refresh`, 6 `Psyche`, 6 `Audit`, 3 `Design`.

So the fix is mechanical: reconcile reporting.md's three lists to
report-naming.md's nine-variant canonical set. The `proposal`,
`review`, and `postmortem` kinds in reporting.md were folded — `review`
became `Refresh`, `proposal` collapses into `Design`, `postmortem` has
no live use. This is sync-debt cleanup, not a vocabulary the psyche
needs to choose.

### H2 — The filename convention is self-contradicting; one side is retired

reporting.md line 453-456 says the kind "moves to the report's
frontmatter or opening section, **not the filename**." report-naming.md
line 47-48 says the exact opposite and names it retired: *"The older
guidance that variant belongs only in the header is retired"* — variant
goes in BOTH the filename and the front matter, per Spirit 1481. The
disk reports follow report-naming.md (filenames carry the variant).
reporting.md is simply stale on this point. Mechanical fix: delete the
"not the filename" clause in reporting.md and point at report-naming.md.

### H3 — Dangling cross-references

The 532 audit already executed the fixes it found (retired "executor"
vocabulary, the renamed-section citation). A fresh grep finds the
intent-capture rule is restated in AGENTS.md and human-interaction.md
(not the "four files" the audit estimated — the count has already come
down). Remaining dangling pointers are a sweep-as-found item, not a
fork.

## The real forks (psyche judgment owed)

### FORK A — How to kill the intent-capture sync-debt

The intent-capture-first rule (read the psyche prompt, classify every
intent statement as Decision/Principle/Correction/Clarification/
Constraint, capture public intent through Spirit FIRST, working-orders-
are-not-intent) is the workspace's keystone rule. It is currently
written out in near-full in **AGENTS.md** (the long "Capture intent
through the right intent substrate FIRST" override) AND in
**skills/human-interaction.md** AND has its canonical discipline home in
**skills/intent-log.md** §"Working orders are not intent". The 532 audit
called this "the anti-noise intent breaking on its own keystone rule" —
the same rule restated in multiple files begins to diverge as each copy
is edited independently.

The fork is HOW to single-source it:

- **Option A1 — Canonical-home-plus-pointer.** intent-log.md holds the
  full rule. AGENTS.md keeps a one-paragraph load-bearing fence (the
  "this is the absolute first task" framing) that POINTS at intent-log.md
  for the substance, instead of restating the whole classification list.
  human-interaction.md drops its copy and points too. Pro: one source of
  truth; edits land once. Con: AGENTS.md is the every-keystroke contract
  — a pointer means an agent must follow a link to get the full rule, and
  the whole point of AGENTS.md is that the load-bearing rules are present
  without a hop.

- **Option A2 — Keep AGENTS.md self-contained, thin the skills.** Accept
  that AGENTS.md restates the rule in full (it is the universal
  every-harness surface and must stand alone), and instead make
  human-interaction.md + intent-log.md the ones that point UP at
  AGENTS.md for the rule statement, carrying only the mechanism detail
  (how to phrase a Spirit call) not the rule itself. Pro: the
  every-keystroke surface stays complete. Con: AGENTS.md becomes the
  single source, which inverts the normal "skills are the substance,
  AGENTS.md is the fence" layering the Rust-discipline override
  explicitly follows.

This is a genuine fork because the workspace has TWO competing
single-source principles that point opposite ways here: (1) "AGENTS.md
is the compact every-keystroke contract — load-bearing rules present
without a hop" and (2) "the skill is the substance; AGENTS.md is the
load-bearing fence that mandates the read." The Rust-discipline override
resolved this for Rust by choosing (2) explicitly ("The skills are the
substance; this rule is the load-bearing fence"). The question for the
psyche: does the intent-capture rule follow the SAME pattern as
Rust-discipline (A1, skill is substance, AGENTS.md is fence), or is the
intent-capture rule important enough to be the named exception that
stays fully in AGENTS.md (A2)? The designer lean is A1 (consistency with
the Rust-discipline precedent the psyche already blessed), but the
psyche set that Rust precedent and may want intent-capture treated as
more load-bearing.

### FORK B — Lane-vs-topic maintenance authority: already canonical, does it need a blessing?

The 532 content report's deepest point was *"maintenance authority
should follow the TOPIC, not the lane that wrote the file."* Re-checking
the live files: this is **already canonical**.
`skills/context-maintenance.md` line 36 states it verbatim:
*"Agglomerate by topic, not by lane: one topic's reports across all
lanes collapse into one report on it,"* and §2 ("Topic-recency ranking
— cross-lane reading") builds the whole maintenance pass around reading
all lanes' reports on a topic together. So the principle is not a
proposal awaiting ratification — it is written discipline.

The fork that REMAINS is narrower and real: **does cross-lane topic
maintenance authorise one lane to delete/rewrite another lane's
reports?** The current contracts pull against each other here:

- context-maintenance.md says maintenance is "by topic, across all
  lanes" and the designer does the agglomeration.
- BUT reporting.md §"Where reports live" says *"Don't edit another
  role's reports. If you want to build on another role's report, rewrite
  the relevant content in a new report inside your own subdirectory"* —
  and each lane's subdir is its implied write-lock.

These two cannot both be literally true for the operator-lane silt the
532 audit found (operator reports at 4.4× cap teaching removed-Asschema,
while the Maximum record killing it sits in the designer lane). Either
the designer reaches into `reports/operator/` to retire the stale
topic-content (violating "don't edit another role's reports"), or the
stale content stays until an operator-lane agent happens to do its own
maintenance (which the silt shows does not happen on its own cadence).

The psyche's call: **(B1)** topic-maintenance authority overrides
lane-ownership — a designer running a topic-cluster sweep MAY delete or
rewrite another lane's reports when the topic's canonical truth lives in
the designer lane, OR **(B2)** lane-ownership holds — cross-lane
maintenance can only FLAG another lane's stale reports (write a
designer-lane note) and the owning lane must do the actual deletion.
The designer lean is B1 with a guardrail (the deleting commit names the
cross-lane retirement and the topic's canonical anchor), because B2 is
exactly the mechanism that produced the 4.4× silt — the owning lane
never came back. But B1 weakens the lane write-lock the whole
coordination model rests on, so this is the psyche's to set.

### FORK C — What record ui5d implies: a NEW quality-discipline with no skill home

Record ui5d (Correction, High, 2026-06-04) is a NEW intent statement
the 532 audit predates: *"Do work properly or not at all — stop burning
psyche tokens on half-assed slop. Do not dispatch underspecified or
wrong-shaped subagent work... Either specify and execute the work
correctly with proper oversight and verification, or do not start it.
Delegating a flawed brief and then surfacing the gap as if the work were
acceptable wastes the psyche's tokens and attention."* It pairs with a
sibling Correction qkvx about the same concrete incident (the
string-keyed consumption-only VmTesting hack that should have been a
typed end-to-end pipeline) — so this is grounded in a real, recent
failure the psyche reacted to, not an abstract worry.

I checked where this lands in the skills. The subagent-dispatch
mechanics are well-covered: `skills/role-lanes.md` §"Subagent dispatch
inherits the dispatcher's lane" (lanes, locks, report numbering),
`skills/designer.md` §"Designer sub-agents land code witnesses" (the
audit/spec/refactor dispatch shape with mandatory readings). But NONE of
them carry ui5d's actual content — the QUALITY GATE. designer.md
describes how to brief a sub-agent for code witnesses; it does not say
"a wrong-shaped brief must not be dispatched at all" or "the dispatching
agent owns verification and may not surface a half-done result as
acceptable." So ui5d is captured in Spirit but inlined in zero skills —
the durable discipline has no home yet.

The fork is what TEETH the psyche wants this discipline to have:

- **Option C1 — Pre-dispatch gate (block).** The dispatching agent must
  not dispatch a sub-agent brief until the brief specifies the
  end-to-end shape (typed-source-first, the full pipeline, the
  acceptance) — an underspecified brief is REFUSED, the dispatcher does
  the specification work first or does the task itself in the main agent.
  This is the strong reading of "do not start it."

- **Option C2 — Post-dispatch ownership (verify, don't surface slop).**
  Dispatch is allowed more freely, but the dispatching agent OWNS the
  output: it must verify the sub-agent's work against the intent before
  reporting it, and may never surface a known-flawed result to the
  psyche as if acceptable. This is the "proper oversight and
  verification" half of ui5d. Weaker pre-gate, strong post-gate.

- **Option C3 — Both, as a named discipline section.** Inline ui5d as a
  new §"Dispatch quality gate" in designer.md (the designer protocol is
  the one lane that dispatches by default) AND a short cross-lane fence
  in autonomous-agent.md, stating: specify the end-to-end shape before
  dispatch (C1) AND verify before surfacing (C2). This is the designer
  lean — ui5d's text contains both clauses ("specify AND execute
  correctly" + "proper oversight and verification"), so a faithful
  inlining carries both.

Why this needs the psyche and not just a designer just-fix: ui5d is a
behavioural correction aimed at how AGENTS THEMSELVES work, and its
strong reading (C1, refuse to dispatch) changes the designer protocol's
default — the psyche blessed parallel-subagent-by-default for the
designer (2026-05-21), and C1 adds a gate to that default. The psyche
should confirm whether ui5d is meant to GATE the dispatch (slow it down,
specify-first) or to make the dispatcher accountable for output
(C2) — or both (C3). The token-cost framing in the record ("burning
psyche tokens," "wastes the psyche's tokens and attention") suggests the
psyche cares most about not having to read slop — which leans C2/C3 (the
verify-before-surface clause) — but "do not start it" is explicit C1
language. This is exactly the ambiguity worth one sentence from the
psyche.

## Summary table

| Item | 532 framing | Current state | Verdict |
|---|---|---|---|
| Report-kind vocabulary | three disagreeing lists | settled in report-naming.md (9 variants, Spirit 1481/2577); reporting.md stale | H1 — just-fix |
| Filename variant contradiction | self-contradicting | report-naming.md retired the "header-only" side | H2 — just-fix |
| Dangling cross-refs | found + fixed in 532 | count already down; sweep-as-found | H3 — just-fix |
| Intent-capture sync-debt | restated in 4 files, diverging | now ~2 files; single-source HOW is open | FORK A — psyche |
| Lane-vs-topic authority | "deepest content point" | principle already canonical; cross-lane DELETE authority open | FORK B — psyche |
| ui5d quality gate | (postdates 532) | captured in Spirit, inlined in zero skills; teeth unset | FORK C — psyche |

The shape of this slice: the 532 audit's content drifts were mostly
caught and half-settled in the weeks since — the vocabularies and
filename convention now have a canonical home and only need the stale
second copy reconciled. The two surviving content forks (A, B) are each
a collision between two real workspace principles, and the one genuinely
new fork (C) is a fresh psyche Correction whose teeth are not yet set in
any skill. Hygiene I will execute; the three forks are the psyche's.
