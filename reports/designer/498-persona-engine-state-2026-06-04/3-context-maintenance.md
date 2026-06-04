---
title: 498.3 — Deep context maintenance — cross-lane topic-recency ledger
role: designer
variant: Audit
date: 2026-06-04
topics: [context-maintenance, topic-recency, report-retirement, doc-code-drift, intent-maintenance, spirit-dedup, persona-engine]
description: |
  Slice 3 of the 498 state-of-the-engine assessment. A cross-lane
  topic-recency sweep over reports/ (designer, operator, system-designer,
  system-operator, plus the qualified lanes). Produces the
  drop/migrate/keep ledger by topic with named superseders and landing
  gates; a doc-code-drift list verified against the live spirit /
  persona-spirit repos; and a confirmed intent-maintenance worklist
  beyond the 497 certainty pass (the ~12 working-orders, the borderline
  Maximum records, and a missed dedup the 497 sweep claimed but did not
  land). RECOMMEND only — no report deletions, no Spirit edits performed.
---

# 498.3 — Deep context maintenance

This slice ranks reports by topic across all lanes per
`skills/context-maintenance.md` §2 and `skills/context-maintenance-deep.md`,
names the supersession spine for each topic arc, applies the
forward/migrate/keep/drop rule WITH a landing gate, audits per-repo doc
drift against live code, and confirms the intent-maintenance worklist the
497 certainty pass surfaced. Everything here is a recommendation for the
owning lane; nothing was deleted or edited.

## Inventory at sweep time

Active report counts by lane (over the 12-report soft cap where noted):
designer 39 (OVER), operator 47 (OVER), system-operator 27 (OVER),
system-designer 11, cloud-designer 4, cloud-operator 7, assistant 3,
counselor 3, cluster-operator 1, second-designer 2. The three big lanes
are all well over cap, and the over-cap mass is concentrated in two topic
arcs that have each had a fresh permanent-grade synthesis land this week:
the **schema/triad-engine stack** and the **Spirit removal-candidate /
privacy / variant-ladder** thread.

## Topic arc A — schema/triad-engine stack

### Arc and era shift

The stack is `nota-next → schema-next → schema-rust-next → triad-runtime
→ spirit-next(now `spirit`)`. The late-May era (designer 443-481, operator
246-290) was *discovery and vision*: what the planes are, what to port,
where the honesty gaps sit. That era CLOSED this week with two
permanent-grade syntheses that re-ground the whole topic from current
code: the **495 design-to-code port audit** meta-report directory
(designer, the dual-engine bug + abstraction-debt ledger) and its
psyche-facing **496**, plus operator **303/304** (repo stack state). 495's
one-sentence finding — [the operator has already manifested the bulk of
the recent schema-stack intent into clean code; the genuine
design-to-code surface left is one correctness bug, a handful of missing
constraint witnesses, and a set of repetition-driven abstractions] — is
the new canonical framing. Recent intent (1572-1577, 1581, 1584, 1586
zeroed) ratified the open questions the old era was still debating, so the
old-era framing is now obsolete, not merely older.

### Current canonical surface (keep)

- designer 495 (meta-report dir) + 496 — the live port-audit ledger and
  its psyche low-down. KEEP (newest, load-bearing).
- operator 303/304 — repo topology + dependency/generation-drift map.
  KEEP.
- designer 484 (production-readiness meta) + 492 (ratification queue) —
  KEEP as the live decision-queue spine that 496 cross-references.
- operator 295-300 — the most recent implementation/cleanup reports
  (newtype/trace cleanup, meta-signal rename pass). KEEP.

### Drop band (designer lane owns)

Each names its superseder + landing. Substance has landed in 495/496 or
in permanent docs (the ratified records are in Spirit; the abstraction
list is in 495.6).

| Report | Superseder | Landing witness |
|---|---|---|
| 443 design-improvements-audit | 495 (slices 2-3 re-audit the same crates against current code) | the dual-engine bug 443 hinted at is now pinned in 495.2 with the failing-witness; abstraction list in 495.6 |
| 444 stack-vision | 484 + 496 | the four-planes/data-model vision is now in `triad-runtime`/`schema-next` ARCHITECTURE.md + INTENT.md (per 495 "landed and clean") |
| 445 next-stack-audit | 495 | porting surface re-ranked in 495.6 |
| 446 next-stack-porting-research | 495 | porting playbook subsumed by 495's per-slice ready-code |
| 466 triad-engine-honesty-situation | 484/495 | the honesty gap (source-ahead-of-deploy) is now stated in 484 + system-designer 59.5 |
| 481 schema-daemon-upgradable-runtime-pilot | 481-era pilot vision absorbed by 495 + spirit ARCHITECTURE.md | the upgradable-runtime direction is ratified (records 1574/1581) |
| 477/478 nexus-re-agglomeration / inner-nexus-engine | operator 287-289 (nexus recursive-computation thread) | the recursion design landed in `skills/component-triad.md` NexusWork/NexusAction substrate (per system-operator 187 §8) |
| 469 introspect-component-design | 487/488 (trace help/config meta) | introspection folded into the help-namespace design (record 1493) |

### Drop band (operator lane owns)

The operator schema thread (246-294) is the largest single stale block.
The implementation substance has either landed in code (and is re-audited
in 495) or in `skills/component-triad.md` / `skills/nota-design.md` (per
system-operator 187 §8, those skills now carry the NexusWork/effects
substrate and the enum-payload pattern). Recommend the operator retire as
a block, report-by-report, with 295-304 as the current surface:

- 246-261 (nota-surface-split through nota-layer-macro-stack) — the
  pre-canonical-era implementation logs; superseded by current code +
  495's "landed and clean" table. Drop with 495 as witness.
- 271/276/283 — three operator context-maintenance ledgers; superseded by
  THIS 498 sweep (a maintenance ledger retires when a newer sweep
  re-issues its handoffs, `skills/context-maintenance-deep.md`
  §"Successor sweeps").
- 273/277/280/284 (spirit-next triad-runtime audits) — superseded by
  system-designer 59 (the current design-to-implementation audit) +
  operator 295.
- 281/282/290/291/292/293/294 (generated-interface / trace / engine-report
  thread) — superseded by 295 (trace cleanup) + 296/297; the engine-report
  TOOLING substance is in `skills/engine-report.md` (permanent).

### Migrate (competing-alternatives — must migrate before drop)

- **477/478 vs operator 287-289** carry competing Nexus-recursion designs
  (three angles in 477; the operator's recursive-computation-continuation
  vs designer comparison in 288). Per `skills/context-maintenance.md` §3a
  + record 1323, the chosen recursion shape AND the rejected alternatives
  migrate to `skills/component-triad.md` (or an ARCHITECTURE decision
  record in `triad-runtime`) before either report drops. Today neither the
  chosen-vs-rejected reasoning is in a permanent doc; this is a
  MIGRATE, not a Drop.
- **481** (upgradable-runtime pilot) sketched upgrade-as-SEMA alternatives
  (cf designer 447 upgrade-as-sema-design); the chosen direction is
  ratified (1574/1581) but the alternatives reasoning is not in
  `spirit`/`triad-runtime` ARCHITECTURE.md. Migrate the
  decision-rationale, then drop 447 + 481 together.

## Topic arc B — Spirit removal-candidate / privacy / variant-ladder

### Arc and current state

This is the most active cross-lane arc: it threads system-operator
(187-192), system-designer (55-61), designer (458, 465, 473, 474), and
the production source. The newest permanent-grade synthesis is
**system-designer 59** (design-to-implementation audit, 2026-06-04) whose
one-line finding is [the load-bearing operation already exists in code
(Reading B), every NEW design the thread spun off is blocked on a psyche
decision, and the blocks got SHARPER this week]. 59.5 carries the full
decision queue D1-D8; 59 is the canonical surface for the WHOLE arc now.

### Current canonical surface (keep)

- system-designer 59 (meta-report dir) — the live decision queue + the
  repetition-to-abstraction propositions. KEEP.
- system-designer 60/61 (archive-privacy-typed-feedback; situation-
  projection-engine) — newest, KEEP.
- system-operator 191/192 (privacy/shorthand situation; archive/versioning
  followup) — newest operator-side, KEEP.

### Drop band (system-operator lane owns)

- **189/190** (production-spirit collect-removal-candidates; open-problems
  psyche report) — superseded by system-designer 59.5 (which IMPORTS 190's
  open-problem map into its D1-D6 decision queue and reconciles Reading B)
  AND by system-operator 191/192. Drop with 59.5 + 191 as witnesses.
- **188** (component-data-archival-and-garbage-collection) — the archival
  concept is now in system-designer 60 (archive-privacy concept) + the
  `ArchiveTarget` code; drop with 60 as witness.
- **186** (psyche-open-work-update) — superseded by 191 (newer open-work
  update). Note 187 §"Disk-side action" already retired 184 against 186;
  187 itself is a context-maintenance ledger now superseded by THIS sweep.
- **182** (spirit-privacy-and-shorthand-interface-audit) — superseded by
  191 (privacy/shorthand situation, 2026-06-04). Drop.
- **177** (spirit-topic-depth-query-implementation) — the depth-query
  shipped; the variant-ladder depth words are now documented in the
  production `signal-persona-spirit` contract + system-designer 59.5 D5.
  Drop with code as witness.

### Drop band (system-designer lane owns)

- **55** (spirit-variant-ladder-design-research) + **56** (psyche-meta-
  report-spirit-recent-work) + **57** (variant-and-collect-vision dir) +
  **58** (spirit-engine-direction psyche report) — the 55→58 vision arc is
  fully absorbed into **59** (which cites 57 as "the prior vision this
  builds on" and supersedes the rest). 58 is a 61KB psyche report whose
  decision queue is re-issued sharper in 59.5. Drop 55/56/57/58 as a block
  with 59 as the named superseder. **MIGRATE FIRST**: 57.2 and 58 carry
  the Reading-A-vs-Reading-B competing analysis; the chosen direction
  (Reading B lean, pending psyche ratification of D1) and the rejected
  Reading A reasoning must land in `persona-spirit/ARCHITECTURE.md` (which
  already documents the archive-then-retract lifecycle) before drop.
- **53** (spirit-next-production-parity) — directly contradicted by the
  doc-drift finding below; its "parity" framing is the source of the
  overstated INTENT.md line. KEEP only until 53's parity-sequencing
  substance migrates into `spirit/INTENT.md` corrected (see drift D-1),
  then drop.
- **54** (spirit-privacy-classification-research) — superseded by 60/61 +
  record 1456 (four-tier) which is itself now contested by 1463
  (privacy-as-Magnitude). Drop with 60 as witness; note the open privacy
  direction is record 1571 (in 59.5 D6).

### Keep (designer lane, this arc)

- **458** (spirit-triad-naming-gate-decision) — KEEP/escalate: it is a
  pending-psyche-attention gate (per 472's carry-forward); stays until the
  psyche resolves or it parks in ARCHITECTURE.
- 465/473/474 (decision-landscape; spirit-algorithm-proposals; topic-
  discovery-feature) — design proposals not yet ratified or built; KEEP
  until they land or the psyche declines them.

## Topic arc C — context-maintenance ledgers themselves

Per `skills/context-maintenance-deep.md` §"Successor sweeps retire
maintenance ledgers", a maintenance ledger retires when a newer sweep
covers the same scope. THIS 498 sweep is the newer cross-lane ledger, so
it supersedes the prior single-lane ledgers — each owning lane drops its
own after confirming this sweep re-issued its handoffs:

| Stale ledger | Lane owns drop | Re-issued by |
|---|---|---|
| designer 472 (2026-06-02) | designer | this sweep (arc A + B) |
| operator 271/276/283 | operator | this sweep (arc A drop band) |
| system-operator 169/173/178/187 | system-operator | this sweep (arc B + the rest) |
| cloud-operator 12 (context-maintenance-skill-update) | cloud-operator | substance landed in `skills/context-maintenance.md` itself |
| cloud-designer 15 (lane-agglomeration-audit) | cloud-designer | lane-920 retirement landed in AGENTS.md |

472 also carried two pending-psyche items (458 naming gate; 470 backlog
items 2-6) — those carry forward into THIS sweep's keep band and the 499
psyche report, so 472 drops cleanly once 458 is surfaced again (it is).

## Topic arc D — small / single-lane reports (keep, no peer)

- assistant 1-3, counselor 1-3 — private-affairs role-registration +
  privacy substrate; KEEP (recent, lane-owned, privacy-scoped).
- system-operator 174-181, 183/185 (browser-use, dji-mic, pi-compaction,
  prefetch, playwright) — live system-operator hardware/deploy thread;
  KEEP (active, no synthesis has absorbed them). 175/176 (dji-mic) could
  drop once the fix is confirmed stable, but that is the system-operator's
  call with a code/deploy witness.
- cluster-operator 1, second-designer 165/176 — older, low-traffic;
  second-designer 176 (upgrade-mechanism soup-to-nuts) overlaps designer
  447/481 upgrade thread — fold into arc A's upgrade migration.

## Doc-code drift (verified against live repos)

Each verified by reading the live file this sweep. These are the
beadCandidate fixes for the operator (per-repo INTENT.md/ARCHITECTURE.md
are operator-integrated prose).

### D-1 — `spirit/INTENT.md:206` overstates currency (CONFIRMED)

Live file `/git/github.com/LiGoldragon/spirit/INTENT.md:206` reads:
[Spirit-next tracks production Spirit 0.3 behavior where the schema
surface reaches it...]. This overstates parity exactly as system-designer
59.8 flagged: the pilot tracks multi-topic / privacy / lookup but
deliberately NOT removal-candidate collection, the recency-depth ladder,
or date/time stamping (`schema/lib.schema:89` `Entry` has no
`RecordedTime`). Per `skills/context-maintenance.md` anti-pattern
"reports/docs that overstate currency", soften line 206 to the true
state: the pilot tracks the read/observe/privacy surface and deliberately
omits the production removal/ladder thread pending cutover.

### D-2 — `spirit` repo internal names still say `spirit-next` (CONFIRMED)

Record 1588 (rename spirit-next → spirit) is only PARTIALLY landed.
Operator 304 confirms the repo-level move landed (GitHub + local dir +
`repos/spirit` symlink + origin URL). But the live `Cargo.toml` still
carries `name = "spirit-next"`, `[lib] name = "spirit_next"`, three
`[[bin]]` names `spirit-next*`, and `repository =
"https://github.com/LiGoldragon/spirit-next"` (the URL now 301-redirects).
And `INTENT.md` heading is still `# INTENT — spirit-next`. This is the
"repo rename landed, internal names lag" issue 304 itself flags. The
internal-name follow-up slice is operator-owned. Note: `repos/spirit-next`
symlink is gone (304 says so) but `repos/spirit` exists — so any doc or
skill still referencing `repos/spirit-next` is a dangling reference to
chase in the same slice.

### D-3 — `persona-spirit/INTENT.md` lacks the Medium default (CONFIRMED)

Live `/git/github.com/LiGoldragon/persona-spirit/INTENT.md` has no
`Medium`/`default certainty` mention (grep returns nothing). Record 1570
(High) [Medium certainty should be the normal default for routine Spirit
captures] is a decided heuristic that the production INTENT.md should
record, per system-designer 59.8. Add the Medium-default heuristic to
`persona-spirit/INTENT.md`. (The workspace-level ladder is already in
`skills/intent-log.md` per 497; this is the per-repo manifestation.)

### D-4 — stale `.concept.schema` artifact (from 59.6, not re-verified here)

System-designer 59.6 names `signal-persona-spirit/schema/...concept.schema`
as a dead artifact (lists a pre-privacy `Entry`, NOT consumed —
`spirit.schema` is the live one) that would mislead anyone reading it as
the contract. Delete it. Flagged here for the cross-lane ledger; the
operator owns the deletion.

### D-5 — `ArchiveTarget` doc tracks code but is stale to the decision

Per 59.8: the `ArchiveTarget` documentation faithfully tracks the LANDED
code (`Inline`/`File`) but is stale to the decided `OutputTarget`
direction (record 1548, Stdout/Stderr/File). This reconciles when D2 of
the 59.5 decision queue lands; not an independent fix, tracked here so the
operator does both edits together.

## Intent-maintenance worklist (confirmed beyond the 497 certainty pass)

All records below were queried live this sweep against the deployed Spirit
CLI. The 497 report flagged these; this slice CONFIRMS their current state
and adds findings 497 missed.

### Working-orders mis-captured as intent — all still elevated (CONFIRMED)

Per the AGENTS.md working-orders-are-not-intent rule, these are one-time
task directives that died on completion and should not be durable intent.
All twelve confirmed still at **High** (none zeroed):

- **451** [Subagents are authorized for the schema-design task.]
- **514** [Second-operator should port orchestrate in a worktree while
  operator keeps main]
- **531** [Use subagents to bring orchestrate toward Spirit maturity]
- **545** [the full upgrade mechanism documented end-to-end... Goal: prove
  the agents understand what the psyche wants...] (a do-the-task order)
- **593** [Build an MVP that makes the schema macro system real...]
- **595** [Build all-encompassing understanding report + MVP example...]
- **596** [Use subagents for the schema and NOTA macro MVP pass.]
- **664** [Workspace-wide CONVERSION OF HERESY sweep: dispatch
  subagents...] (a one-time sweep order)
- **671** [Trigger a deep context refresh sweep... subagent dispatched...]
- **754** [Implement a prototype schema-driven NOTA parser stack...]
- **755** [Use an asynchronous subagent... while the operator implements...]
- **794** [For this Nota/schema prototype and vision task, use subagents
  in parallel...]

Recommendation: these are the cleanest possible working-order examples —
each names a specific dispatch/build/sweep that completed. Zero them as a
category once the psyche blesses the working-order class (497's open
question 2). They would still NOT "guide after the task is done" — the
test the rule names. RECOMMEND only; the psyche owns the category blessing.

### Borderline Maximum — still at Maximum (CONFIRMED)

- **1490** [Tracing remains typed data until the client display
  boundary...] — Maximum. Now landed in ESSENCE (strings-at-edges), so
  arguably stays Maximum or is the ESSENCE-anchored exception. Psyche's
  call (497 open question 3).
- **1506** [...the SymbolPath... is the workspace's canonical
  machine-readable universal symbol form...] — Maximum. A firm canonical
  direction; defensible at Maximum or VeryHigh. Psyche's call.

### A dedup the 497 sweep claimed but did NOT land (NEW FINDING)

497 §"What was recalibrated" states [zeroed two duplicates (1589 dup 1579,
1590 dup 1583)]. Live query: **1589 IS Zero** (confirmed), but **1590 is
still at High** — the second zero did not land. 1590 [The operator owns
the main implementation and should review the designer implementation
afterward... better patterns mean better logic, better logical planes, and
better names, not necessarily shorter code.] is a near-verbatim duplicate
of canonical **1583** (High) [...afterward the operator always reviews the
designer implementation for better patterns — better logic, better logical
planes, better names — and adopts what is better.]. RECOMMEND: Zero 1590,
keep 1583 canonical. This is a concrete intent-maintenance fix the operator
(or whoever holds Spirit edit authority) can apply now.

### 497 pending-review Zero candidates — current state (CONFIRMED + refined)

- **1088** is ALREADY empty/removed (497's recommendation landed) — no
  action.
- **198** [Spirit v0.1.1 cutover uses Path A...] — still High; a completed
  one-time deploy-cutover order (superseded by 203 per 497). Zero candidate.
- **347** [Claim primary-kbmi.2.1 scopes as second-system-assistant...] —
  still High; a completed claim order referencing a retired lane
  (second-system-assistant retired per record 920). Strong Zero candidate.
- **151** [DeepSeek-as-library subsumed into persona-pi triad...] — still
  High; 497 flags 157 supersedes it. Zero candidate (inferred, psyche
  review).
- **1456** [Spirit access classification uses exactly four tiers: Open,
  Personal, Sensitive, Sealed...] — still **Maximum**; 497 flags it is
  effectively mooted by 1463 (privacy-as-Magnitude). With the privacy
  direction now reopened by 1571 (59.5 D6), 1456 should at minimum drop
  from Maximum and likely Zero. Psyche review (couples to D6).
- **1512** [no daemon-side printline...] — still Maximum; 1509 (Maximum)
  restates/elevates it, and both restate 1505. Redundant-among-founding;
  harmless but a dedup candidate (keep one canonical).

## Lane-owned handoffs (summary)

- **designer**: drop arc-A band (443/444/445/446/466/481/469/477/478) after
  migrating the Nexus-recursion + upgrade-as-SEMA competing-alternatives to
  `skills/component-triad.md` / `triad-runtime` ARCHITECTURE; drop the
  prior ledger 472; keep 458/465/473/474/495/496/484/492.
- **operator**: drop arc-A band (246-261, 273/277/280/284, 281/282/290-294)
  + prior ledgers 271/276/283 with 295-304 as the surface; apply doc-drift
  fixes D-1 through D-5 (operator-integrated prose) + the 1590/347/198 Spirit
  dedup if holding edit authority.
- **system-operator**: drop 177/182/186/188/189/190 + prior ledgers
  169/173/178/187 with 191/192 as the surface.
- **system-designer**: drop 53/54/55/56/57/58 after migrating the
  Reading-A-vs-B competing analysis to `persona-spirit/ARCHITECTURE.md`,
  with 59/60/61 as the surface.
- **cloud-operator / cloud-designer**: drop their context-maintenance
  ledgers (12, 15) — substance landed in permanent skills/AGENTS.md.

## Anti-pattern check on this sweep

Every Drop above names a superseder AND a landing witness (the landing
gate). Where the landing is not yet in a permanent doc — the Nexus
recursion, upgrade-as-SEMA, and Reading-A-vs-B competing-alternatives —
the action is MIGRATE-first, not Drop, per `skills/context-maintenance.md`
§3a + record 1323. No report was deleted and no Spirit record was edited
by this slice; all actions are recommendations for the owning lane.
