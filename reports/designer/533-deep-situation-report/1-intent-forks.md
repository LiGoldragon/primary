---
title: 533/1 — Deep situation report — INTENT FORKS
role: designer
variant: scan
date: 2026-06-05
session: 533-deep-situation-report (sub-report 1 of N)
topics: [intent, forks, carried-uncertainty, auditor, spirit-deploy, migration, weight, agglomeration]
description: |
  Deep scan of the live Spirit log (82 records, post-525-consolidation) for
  places where intent is UNSETTLED. Hunts carried-uncertainty records, open
  supersession tails, the schema-derived-spirit deploy gap, the fingerprint
  migration cluster, and the weight/agglomeration methodology cluster. Each
  genuine fork is phrased as an actual choice the psyche must make.
---

# 533/1 — Intent forks: where intent is unsettled

## Scan method and the live shape

The deployed `spirit` binary is `spirit-v0.5.2` (persona-spirit). A
`VeryDeep` dump returns **82 live records** — down from the "~100" the prior
audit (532) cited, confirming the `525` consolidation landed. Certainty
distribution: 11 Maximum, 11 VeryHigh, 66 High, 9 Medium, 3 Low. The 12
Medium/Low records ARE the carried-uncertainty surface; everything below
draws from reading their bodies and chasing supersession tails.

Two structural facts shape the whole scan:

1. **The deployed `spirit-v0.5.2` already enforces 4-character minimum hash
   ids and rejects numeric record lookups** (`(Exact [234])` →
   `record identifier code must be at least 4 characters`; `(Exact [2589])`
   → empty result). So the hash-id migration is LIVE in production, not
   pending — which means the fingerprint cluster is mostly settled at the
   intent level but has a real orphaned-citation consequence (fork 4).
2. **Querying by topic fights the parser.** `RecordIdentifiers` takes a
   4-char-min code; the numeric ids used throughout `AGENTS.md`/`INTENT.md`
   no longer resolve. This is itself a finding — the workspace's own
   guidance files cite ids the deployed daemon cannot look up.

## Fork 1 — The auditor role: still proposed, AND its source records are gone

**State.** `AGENTS.md` (lines 161-178) and `INTENT.md` (§"Possible
additional role — auditor", lines 849-878) both carry the auditor as
"proposed, not decided (Medium certainty)", citing **intent records 234 and
235** for DeepSeek-as-auditor / automate-the-auditor. **Neither record 234
nor 235 exists in the live Spirit log** — numeric lookup is rejected, and no
record under topic `auditor` carries DeepSeek or the "mostly mechanical
doubter" language. The ONLY live auditor record is **ek8w** (Decision,
High): *"Intent agglomeration and refresh is triggered by an automated
auditor that auto-proposes refreshes; the psyche confirms the retire of
source records."* That is a narrow scoping of the auditor to ONE job
(intent agglomeration), at High certainty — not the broad rules-and-flaws
doubter the guidance files describe at Medium.

**The fork.** Two things diverged and need the psyche:

- **(A) Promote, (B) narrow, or (C) re-confirm the auditor.** ek8w (High)
  has effectively decided a *narrow* auditor exists (intent-refresh
  proposer). The guidance files still describe a *broad* auditor (audits all
  workspace rules, DeepSeek, automate) at Medium "proposed-not-decided". Is
  the auditor now (A) a decided role broader than ek8w — promote it out of
  "proposed" and write `skills/auditor.md` + `reports/auditor/`; (B) only
  the narrow ek8w intent-refresh function, and the broad-doubter framing in
  AGENTS/INTENT should be retired as superseded; or (C) still genuinely
  proposed-not-decided and the open questions (authority class, lane
  mechanism, findings substrate) remain open?

**Why this needs the psyche.** Intent cannot be inferred. The guidance files
assert Medium-certainty intent (234/235) that no longer has a live record
backing it; ek8w asserts High-certainty narrow intent. An agent cannot
decide on its own whether the broad auditor is still wanted or was quietly
narrowed to ek8w — only the psyche knows whether DeepSeek-broad-auditor is
still the direction.

**Designer lean:** genuinely unsure — but lean toward the psyche
re-stating, because the citation breakage (234/235 dead) means the durable
record of the broad auditor intent has been LOST in consolidation, and
re-stating it (or confirming the narrowing) is the only clean fix.

## Fork 2 — The schema-derived `spirit` 0.1.0 cutover: no WHEN/HOW intent exists

**State.** The deployed daemon is `persona-spirit v0.5.2`. The
schema-derived `spirit` is a separate all-in-one pilot (record **wv63**,
High: *"spirit is an all-in-one single-repo pilot that deliberately DEFERS
the contract/daemon repo-triad split"*). Record **o7lx** (Principle, Medium)
splits the labor cleanly: *"Designer prototypes the shape; operator owns
production migration … at the point production Spirit cuts over to the
schema-derived stack."* Record **wm4r** (Decision, Maximum) says *"Production
Spirit should be fixed now by integrating and deploying the random stable
identifier work rather than waiting for the next schema-derived Spirit
stack"* — i.e. fix v0.5.2 NOW, don't wait for 0.1.0.

**The gap.** wm4r decided the SHORT-TERM (patch v0.5.2 — and the live binary
proves this happened: hash ids are deployed). o7lx decided the LABOR SPLIT.
But **no record decides WHEN or under what readiness bar the schema-derived
`spirit` 0.1.0 replaces v0.5.2.** wv63 says don't-copy-its-shape; o7lx says
operator-owns-the-migration-at-cutover — neither says what triggers cutover.

**The fork.** **(A)** Cut over Spirit independently and soon — it's a
self-contained daemon, the migration tooling exists (signal-persona-spirit's
`migration.rs`), and the schema-derived stack should prove itself on the
workspace's own intent log first. **(B)** Defer Spirit cutover until the
broader triad cutover (the lojix/Horizon dual-stack retirement, records
tvbn/fe2j) so all schema-derived components cut over coherently. **(C)** No
cutover intended near-term — v0.5.2-patched is "good enough" and 0.1.0 stays
a design proving-ground indefinitely.

**Why the psyche.** This is a deploy-sequencing judgment with no governing
record. The ESSENCE "right shape now over wrong shape sooner" leans against
rushing, but Spirit-cutover-first has a unique argument (dogfood the engine
on intent itself) that only the psyche can weigh against coherent-batch
cutover.

**Designer lean:** (A) — Spirit is the one component with zero external
consumers (it serves agents, who adapt instantly), making it the safest and
most valuable first real cutover. But this is genuinely a psyche call.

## Fork 3 — The weight / agglomeration / record-shape cluster: methodology NOT settled

**State.** A dense cluster touches Spirit's future record shape, and it is
the single largest pocket of unsettled intent. The records:

- **d5s2** (Principle, **Low**): refresh-by-agglomeration — fuse many
  Medium records into one fresher higher-certainty record.
- **6z6t** (Correction, High): *"Record d5s2 overstates agglomeration as a
  certainty-raising mechanism"* — agglomeration must NOT auto-raise
  certainty. **This is a live unresolved tension: d5s2 (Low) says
  agglomeration raises certainty; 6z6t (High) says it must not.**
- **u2s9** (Clarification, **Low**): weight preserves accumulated importance
  through agglomeration; *"This weight-field design is low-certainty and
  should be revisited before production implementation."*
- **g8ln** (Clarification, Medium): weight uses the Magnitude ladder
  (Zero..Maximum) as a second axis.
- **vbx6 / f0wm / cw5t / qkrg / kfxd** (High/Medium): weight-vs-certainty
  distinction, variant-shaped records, composite-with-provenance, archive
  safety.
- **hp3r** (Decision, Medium): *"Production Spirit does not need an immediate
  weight-field migration; weight belongs in the future record-shape design
  until the mechanism is settled."*
- **a3l4 / y0vr / tf2o**: the relations field is the ONLY code change;
  agglomeration is agent behavior trained by a skill, no composite type.

**The fork.** Multiple unsettled sub-questions, all explicitly low-certainty
or self-flagged "revisit before production":

- **3a — Does weight exist as a stored record axis at all?** u2s9 (Low) and
  vbx6 (High) want it; hp3r (Medium) defers it. The methodology is
  undecided: is weight (A) a real second Magnitude axis stored on every
  record, (B) a derived search score only, or (C) deferred indefinitely as
  "future record-shape design"?
- **3b — Does agglomeration raise certainty?** d5s2 (Low) yes; 6z6t (High)
  no. This direct contradiction is currently "resolved" only by certainty
  ordering (6z6t outranks d5s2), but d5s2 was never corrected/retired — it
  still reads as live methodology.

**Why the psyche.** The prior audit (532) flagged *"consolidate the ~15-record
weight/agglomeration cluster"* as a proposed action awaiting the psyche. The
cluster cannot be consolidated by an agent because the MERGE would have to
decide 3a/3b — which is composing new intent from contradictory low-certainty
records, the forbidden act. The psyche must state the methodology (does
weight exist? does agglomeration raise certainty?) before the cluster can
collapse into a clean `525`-style record.

**Designer lean:** genuinely unsure on 3a (weight is a real design question);
on 3b the designer leans 6z6t (agglomeration preserves provenance, does not
manufacture certainty) — but d5s2 needs explicit retirement, which only the
psyche can authorize.

## Fork 4 — Orphaned numeric citations after the hash-id migration deployed

**State.** This is the consequence of the migration cluster
(**qtbd/xfc5/ozbz/o1sl/dfxz/y5m9/f36y/kr1v** + **tw81/rh29/3jkx**) being
*settled and DEPLOYED*. At the intent level the fingerprint cluster is
resolved: kr1v/3jkx negate content-addressing (use random hash); dfxz/o1sl
migrate all numeric ids now with a temporary mapping dump; f36y/y5m9/tw81
settle the 4-char-min base36 short code. **The deployed v0.5.2 proves it
shipped** — numeric lookups are rejected.

**The unsettled part is the fallout, not the design.** `AGENTS.md` and
`INTENT.md` cite roughly two dozen numeric record ids (234, 235, 920, 944,
884, 712, 882, 539, 237, 515, 2585, 2589, 2620, 2561, 502-504, 513-519, …)
as load-bearing authority — *"Per spirit record 944 (Maximum)"*, *"intent
records 234 and 235"*. **None of these resolve against the deployed daemon.**
The transitional numeric→hash mapping dump (o1sl: *"kept around for a little
while so agents can still resolve old references during the transition, then
retired"*) — I found no such dump file in the persona-spirit / spirit trees
(only `migration.rs` code).

**The fork.** **(A)** Produce and keep the numeric→hash mapping dump (o1sl's
explicit transitional artifact) so the existing citations resolve, then do a
slow citation migration. **(B)** Skip the dump; rewrite every numeric
citation in AGENTS.md/INTENT.md/skills to the new hash short-codes in one
pass (o1sl says break-is-acceptable). **(C)** Accept that the
guidance-file numeric citations are now decorative prose ("per psyche
2026-05-27") and stop treating the numbers as resolvable locators.

**Why the psyche.** o1sl decided the dump SHOULD exist transitionally; if it
doesn't, that's either an unexecuted operator task or a quiet decision to
skip it. The psyche should say whether the transitional bridge is still
wanted, or whether the citations should be hard-migrated. This is also a
working-order vs intent boundary — but the *durability* of the existing
citations is a real intent-layer question.

**Designer lean:** (B) — break cleanly, rewrite citations to hash codes,
matching ESSENCE "backward compatibility is not a constraint". The dump is a
transitional shape, and ESSENCE is hostile to transitional shapes.

## Fork 5 — The lojix/Horizon dual-stack retirement: sequenced but trigger-less

**State.** A coherent decided charter exists: **tvbn** (Maximum) — Horizon
stays a hack/projection surface, lojix carries the full triad port, finish
the lean rewrite to cutover and retire the dual stack; **fe2j** (High) —
port-first ordering (finish lojix port BEFORE cutting CriomOS over);
**m85j** (High) — Horizon simplification collapse lands AFTER cutover;
**brgo** (High) — full schema-derived streaming is the direction, with one
open question carried in the record itself.

**The carried open question (inside brgo).** brgo explicitly carries: *"Open
question carried: whether the existing signal-frame streaming substrate was
deliberate scaffolding ahead of this work or leftover, which most changes
the effort estimate."* This is a factual/archaeological question, not a
psyche-judgment fork — an agent can answer it by reading signal-frame
history. **Flag it as a research task, not a psyche fork.**

**The actual fork.** Like fork 2, the dual-stack charter has a clear
end-state and ordering but **no readiness bar for "parity reached → cut
over per node."** tvbn says *"prioritized to reach parity then switch over
per node"* — but "parity" is undefined. The fork is whether the psyche wants
(A) a defined, enumerated parity checklist (the set of production CriomOS
features that must work on lojix before any node cuts over) authored now, or
(B) parity judged ad-hoc per-node by the operator at cutover time.

**Why the psyche.** This is a risk-tolerance call on a production cluster
(Prometheus is the router — see h16n). Only the psyche can decide whether
cutover gates on an explicit parity contract or operator judgment.

**Designer lean:** (A) — an explicit parity checklist, because cutting over
the cluster router on ad-hoc judgment is the highest-stakes operation in the
workspace and ESSENCE prizes the right shape over speed.

## Fork 6 — The narrow carried-uncertainty tail (lower stakes, listed for completeness)

Three more Medium/Low records carry genuine unsettledness but are smaller:

- **cx7y** (Decision, Medium): Spirit archive storage path —
  daemon-derived default, configurable via daemon configuration. Open: the
  actual default path and whether it's settled enough to implement. Low
  stakes; mostly an operator detail.
- **x8iv** (Clarification, **Low**): *"horizon-rs is currently a hack and
  does not have the regular component-triad shape."* This is a true-fact
  clarification, not a fork — it states reality, doesn't pose a choice.
  Listed because it's Low-certainty but it does NOT need a psyche decision.
- **en7k** (Clarification, Medium): splitting SEMA out of the daemon is *"a
  distant future consideration … not the current design."* Explicitly
  parked; not a live fork.
- **jo1x** (Principle, Medium) and **k4d9 / yenl** (Clarification, Medium):
  engine/crate-boundary refinements; technical, designer-owned, not psyche
  forks.

**These do not need the psyche** — recorded here so the scan is exhaustive
and the psyche isn't asked to adjudicate facts or parked items.

## The one-line answer

Five of the twelve carried-uncertainty records cluster into THREE real
psyche forks — the **auditor's scope-and-existence** (its source records
234/235 are GONE, only narrow ek8w survives), the **weight/agglomeration
methodology** (d5s2-vs-6z6t contradiction live, weight-axis undecided), and
**two deploy-cutover triggers** (schema-derived Spirit, and the lojix/Horizon
dual-stack — both have end-states but no readiness bar). The migration
cluster is *settled and deployed* but left **orphaned numeric citations**
across the workspace's own guidance files. The rest of the Medium/Low tail is
parked facts, not forks.
