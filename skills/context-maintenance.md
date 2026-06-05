# Skill — context maintenance

*Sweep the working surface of context — both the filesystem
reports under `reports/<role>/` and the in-conversation context
window — for what's still load-bearing, migrate substance to its
right permanent home, and retire what's done.*

## What this skill is for

Two surfaces decay together:

- **Reports on disk** under `reports/<role>/`. Working artifacts.
  The filesystem accumulates them; their substance matures upward
  to permanent docs (skills, architecture, code, `ESSENCE.md`) or
  retires when done. See `~/primary/skills/reporting.md` for the
  disk-side typology and hygiene.
- **Context in the live conversation**. The session's working
  memory. When the context window fills, the unsaved part is lost
  on compaction or clear unless it has migrated to disk.

These are the same kind of thing at different scopes — **a report
is just context saved to disk**. The discipline is the same: keep
load-bearing substance; move it to its right permanent home;
retire what's done. Treating them separately is a smell — they
usually need maintenance at the same time, by the same pass.

## The goal — fewer reports, same information

The purpose of a context-maintenance pass is to **reduce the number of
reports without losing information** (psyche 2026-06-04, record 2577).
Reports accumulate; the filesystem should hold each topic's current
substance in as few files as possible. The primary move is
**agglomeration**: take the several reports on one topic, rewrite and
merge their un-contradicted, un-superseded substance into ONE report on
that topic, in a better form — then delete the merged sources, with the
new report as the landing witness. Agglomerate by **topic, not by lane**:
one topic's reports across all lanes collapse into one report on it.

### The Refresh variant

A report that rewrites or agglomerates one or more prior reports carries
the **`Refresh`** variant tag — the capitalized word after the number:
`<N>-Refresh-<topic>-<date>.md`. A single Refresh report MAY merge
several source reports; that is the agglomerated form. After the Refresh
lands, its source reports are **deleted** (git history preserves them;
the Refresh is the landing witness). Refresh is the context-maintenance
*output* variant, the way Audit / Design / Psyche are working variants;
`skills/report-naming.md` lists it among the variants.

The test for agglomerate-and-Refresh vs migrate-then-drop: substance that
is still working-artifact-shaped (a topic's design state, open questions,
the arc of decisions) agglomerates into a Refresh report; substance that
is mature or leaned-on does not belong in a report at all — it migrates to
the permanent layer (§3b below).

## When to invoke

- **Compaction trigger.** The context window is approaching its
  limit, or the user is about to clear/compact. Sweep before the
  loss event.
- **Report soft-cap trigger.** A role's `reports/` subdir crosses
  the 12-report soft cap (per `~/primary/skills/reporting.md`
  §"Soft cap"). Sweep older reports to migrate substance and
  retire enough to land back under cap.
- **End-of-session checkpoint.** After substantial work, before
  stepping away. Ensures the next agent (or next conversation)
  has the right artifacts to resume from.
- **Explicit user direction.** "Do a context maintenance" or "do
  a handover" or similar.
- **Lane retirement.** A lane is being retired (the role taxonomy
  shifted, a retired-suffix lane is being folded back into its
  main role per spirit record 920, etc.). Before the identifier
  itself can be freed, the lane's leftover memories must be
  triaged via this skill —
  reports under `reports/<retiring-lane>/` and beads tagged with
  the lane label. Per psyche 2026-05-22 (spirit record 213),
  identifier retirement is *gated* on context-maintenance
  completion of the leftover memories. See §"Retiring a lane"
  below for the methodology.

Often the triggers coincide. Treat them as one pass.

## Method

### 1 · Inventory

List both surfaces:

```sh
# Disk side — reports for each role that's relevant.
ls ~/primary/reports/<role>/
```

For context: review the conversation's themes — what was worked
on, what was decided, what's still open, what insights surfaced.
Don't dump everything; *categorize*.

### 2 · Topic-recency ranking (cross-lane reading)

Per psyche 2026-05-27 (spirit record 921, Maximum): when reviewing
reports, the ranking is **by topic, across all lanes**. The
discipline is:

1. **For each topic, find all reports across all lanes.** A
   topic like "schema-derived nota stack" or "spirit upgrade"
   typically threads through multiple lanes — operator's
   implementation reports, designer's design reports,
   second-designer's audits, system-operator's deploy notes.
   Pulling them together is how you see the topic's whole arc.
2. **Recency-rank within the topic.** Newest at top. Date is
   in the filename suffix or the metadata header; commit history
   is the tiebreaker.
3. **Name the supersession spine.** Identify the current canonical
   surface, any permanent landings, and any old-era/new-era boundary.
   The spine is the evidence that lets old reports retire without
   losing substance.
4. **Flag what's stale.** A report is *stale* when a newer
   report on the same topic supersedes it (rewrites the framing,
   replaces the design, completes the audit) AND the older
   report's substance is already absorbed in the newer report or
   a permanent doc. A report is *also* stale when a newer Spirit
   capture reframes its topic — recent intent does not have to
   land in a successor report to make the older report's framing
   obsolete. Stale reports drop. Not-yet-stale older reports —
   substance still load-bearing on its own, design alternatives a
   newer report inherits, decision rationale that permanent docs
   don't carry — keep, forward, or migrate per §"Per item,
   decide" below.
5. **Recent intent prevails.** When older content (report, skill
   text, architecture entry) conflicts with newer intent (newer
   Spirit capture, newer report, recently landed code shape), the
   newer is canonical. The older content stays only if it carries
   substance the newer doesn't — design alternatives the newer
   chose between, decision rationale the newer omits, intermediate
   insight the newer skipped. Spirit captures are the highest-
   priority recency signal: a Maximum-magnitude capture that
   reframes a topic supersedes the entire prior framing on that
   topic, including reports that were canonical the day before.
6. **Spirit capture sweep.** Alongside the report sweep, audit
   recent Spirit captures (`spirit "(Observe (Records ((Any []) None
   Any Recent SummaryOnly)))"` or a topic-narrowed `Records` query)
   for duplicate-substance records.
   Multi-agent sessions accumulate near-duplicate captures when
   each agent records on a forwarded prompt without first querying
   what the original-addressed agent captured. Earlier capture wins
   by default; remove duplicates per `skills/intent-maintenance.md`.
   The dedup pass is part of the maintenance cycle, not a separate
   discipline.

Reports without an obvious topic peer across lanes get the same
treatment with a single-lane recency timeline.

**Staleness has a landing gate.** A report is not droppable just
because a newer report exists. It is droppable only after the
load-bearing substance has landed in a successor report or a
permanent doc. If the topic has clearly moved on but the landing is
not verified, the action is **Forward** or **Migrate**, not Drop.
This matters most during major era shifts: first identify the new
canonical landing, then retire the older pile with that landing as
evidence.

**Topic-era shifts retire blocks, not just individual files.** When a
new permanent synthesis re-grounds a whole topic, older reports from
the prior era can retire as a group — but only report-by-report after
each stale flag names the newer surface or permanent home that absorbs
it. Bulk retirement without a landing witness is just context loss.

### 2a · Per item, decide

For each report or context theme, pick one of four actions:

| Action | When |
|---|---|
| **Forward** | Substance is still load-bearing as a working artifact. Roll it forward into a successor report or extend an existing one; retire the predecessor. For cross-lane forward-then-drop, the receiving lane confirms absorption and the source lane owns deletion. |
| **Migrate** | Substance is mature enough to be permanent. Inline it into a skill, `ARCHITECTURE.md`, `ESSENCE.md`, or code. Retire the source. |
| **Keep** | Substance is load-bearing on its own and has no permanent home yet. Rare. Foundational decisions still searching for their final shape. Pending psyche-review items stay Keep/Escalate until resolved, explicitly abandoned, or parked as uncertainty in a permanent doc. |
| **Drop** | Substance is stale, addressed, superseded, or already captured elsewhere, with both superseder and landing named. Delete the report (or simply let context lose it). If the proof pair is missing, Forward or Migrate instead. |

Common heuristics:

- **Audit reports retire with their audited target** unless the audit
  contains independent design rationale or a reusable pattern that must
  migrate.
- **Deploy-event logs, refresh reports, and orientation handoffs retire
  as blocks** once the live state is the baseline and the durable state
  lives in permanent docs, runbooks, code, or current reports.
- **Pending psyche-review flags are not stale merely because they are
  old.** Keep and surface them until the psyche resolves them or an
  agent parks them in the appropriate permanent uncertainty section.

For context items specifically:

| Context type | Typical destination |
|---|---|
| Decisions made in conversation | The permanent doc the decision lives in (ARCH, skill, `ESSENCE.md`). |
| Half-formed insights, possible patterns | A short `note:` in the appropriate report or skill, or a sentence in a handover report. Don't lose them; don't over-format them. |
| Process / workflow reflections | A skill if generalizable, a session-summary if local. |
| In-flight work pending pickup | The successor task / `bd` item / report that names what's next. |
| Already-on-disk content | Drop from consideration — already saved. |

### 3 · Distribute

Land the substance in its right home, **not** in a catchall
handover dump. Preferred order:

1. **Existing reports on the same topic** — extend them with the
   new substance. The handover happens in place. When a report
   contains stale illustrative code, diagrams, examples, or
   recommendations that a newer implementation or intent capture
   has invalidated, **rewrite that report section in place** or
   explicitly mark it retired inside the report. A later synthesis
   report is not enough; stale examples keep teaching agents the
   old pattern when search lands on the older file.
2. **Permanent docs** — inline as the rule, constraint, or
   invariant they actually are. Per
   `~/primary/skills/skill-editor.md` §"Skills never reference
   reports" and
   `~/primary/skills/architecture-editor.md` §"Architecture files
   never reference reports", the permanent docs are where rules
   live, and they don't cite the report that produced them.
3. **A new rollover/handover report** — only as last resort.
   Substance that doesn't fit any existing home and is too
   unsettled to be permanent. The rollover is a working artifact
   for the next session, not an archive.

### 3a · Migrate live patterns first, then retire

A report carrying **competing design alternatives** — multiple
options sketched, one chosen, others rejected — is load-bearing
*as design rationale* until its substance has migrated. Per Spirit
record 1323 (Correction Maximum), closed reports should not be
kept merely for rationale or history. The chosen design AND the
competing-alternatives reasoning both migrate to durable surfaces;
the report then retires.

Migration targets for competing-alternatives substance:

- **Chosen design** → architecture file (per-repo `ARCHITECTURE.md`)
  or skill, as already named in §3 of this skill.
- **Competing alternatives + the reasoning that selected one** →
  either an architecture decision record (when the alternatives
  are durably worth knowing), or Spirit intent records (Decision /
  Clarification capturing the chosen direction with the reasoning
  inline), or both.
- **Empirical evidence (benchmarks, prototypes, witnesses)** →
  the git history of the relevant repo carries the prototype code;
  cite commit IDs from the architecture file rather than retaining
  a report just to point at them.

Once migrations land, **retire the report** — delete via `rm`. Do
not leave it as an archive carrying duplicate rationale.

The previously-named §3a "STATUS-BANNER + keep" behavior is
superseded by record 1323. The status-banner pattern preserved
contradictions and made workspace search noisier; the
migrate-then-retire pattern keeps live patterns close to the code
or contracts they govern.

Signal that a report needs the explicit competing-alternatives
migration (vs a routine single-shape migration): it explicitly
enumerates two or more designs (Design A / B / C / D, Option 1 /
2, etc.) and chose one. Standard design reports proposing a
single shape migrate cleanly; the chosen shape lands in an
architecture file or skill and the report retires.

### 3b · Manifest leaned-on design into architecture — and prefer constraints

When agglomerating, the substance that is mature or leaned-on belongs in
the permanent layer, not a report. Two rules sharpen where it lands
(psyche 2026-06-04):

- **Architecture carries leaned-on design even without explicit intent**
  (record 2578). When the project's forward direction implies a design has
  been accepted or at least leaned on for now, manifest it into the repo's
  `ARCHITECTURE.md` — and into `INTENT.md` / Spirit only where the psyche
  actually stated it. The architecture IS the design layer; a leaned-on
  direction belongs there without waiting for an explicit intent record.
  This is the legitimate path for a report's good design to become
  permanent even when no Spirit capture backs it: the architecture file
  carries it as the design the project is built on. (The intent layer
  still requires an actual psyche statement — never infer intent; but the
  architecture layer does not.)
- **Prefer constraints** (record 2579). Constraints are among the most
  important architecture content, because a stated constraint lets us write
  a test that verifies it. When manifesting a report's design into
  architecture, express it as a **constraint** wherever possible — the
  constraint is what makes the design testable, and it pairs with the
  constraint-witness discipline (record 1565: add a test that proves the
  intended path). Manifesting design as prose teaches; manifesting it as a
  constraint teaches AND becomes a test.

### 4 · Small thoughts are OK

A one-sentence *"side note: this pattern recurred and might be
worth a skill someday"* landed in the right place beats losing
the thought entirely. Tags like `note:`, `possibly useful:`, or
`undecided:` make a thought discoverable without committing the
workspace to act on it.

Don't over-engineer small thoughts. A line in an existing report
that says `note: agents asked about X three times this week —
might warrant a skill if it recurs` is better than no record.
Discovery later is the value, not formality now.

## The rollover / handover report (when one is needed)

If a handover artifact is genuinely needed, it lives at
`reports/<role>/<N>-handover-<date>.md` (or `<N>-rollover-…`).

Structure:

- **What landed** — what's been committed and pushed; one line each.
- **What's open** — what was discussed but not yet resolved.
- **Side notes** — small thoughts worth keeping. Mark each with
  `note:` / `possibly useful:` / `undecided:`.
- **Next-session targets** — concrete pickup points for the next
  conversation or agent.

The handover report retires once the substance migrates to its
right permanent home or the next-session work absorbs it. It is
itself a forwarding-eligible report under the standard hygiene.

## Using agents for the sweep

A maintenance pass over many older reports is well-suited to
parallel agent dispatch. The orchestrator doesn't have to read
every report into its own context.

Pattern:

- Inventory and topic-cluster first; do not deep-read hundreds of
  reports before you know which topic arcs matter.
- Deep-read stale candidates and their proposed successors/permanent
  landings; skim or summarize obvious non-candidates.
- Give each agent a bounded slice: a topic cluster, a lane within a
  topic, or a small batch of older reports + the
  drop/forward/migrate/keep rule from §2.
- Each agent reads the report, checks the surrounding permanent
  docs (does this substance already live in ARCH? in a skill?
  has it been superseded?), then proposes the action.
- For a large cross-lane sweep, prefer topic-cluster agents over
  lane-only agents; the stale judgment is topic-recency across lanes,
  and the lane handoff can be derived from each topic report.
- Review the agent's proposals; execute the migrations; retire
  the reports.

This keeps the orchestrator's context light. The orchestrator's
role is to apply decisions, not to re-read every report. Agents
recommend; the dispatcher decides and applies only the actions it
owns.

For context-only substance (the part that lives in the live
conversation, not on disk), the orchestrator does this sweep
itself — agents can't see the conversation's working memory.

**Cross-lane sweeps, lane retirement, and the meta-report-directory
pattern live in `skills/context-maintenance-deep.md`**. Reach for
that skill when the sweep spans multiple lanes, multiple topic
arcs, or a lane is being retired.

## Anti-patterns

- **Dumping all context into a "handover" report.** The handover
  is a fallback, not a default. Most substance has a better home
  (a skill, an ARCH, an existing report). A dumping-ground handover
  isn't a working surface — it's an archive that decays as fast as
  the context it replaced.
- **Keeping reports indefinitely "because they might be useful."**
  Git log preserves history; the filesystem should hold only
  what's actively load-bearing. Per
  `~/primary/skills/reporting.md` §"What gets absorbed, not kept",
  even foundational decisions and incident lessons get absorbed
  into permanent docs rather than living forever as reports.
- **Preserving content the intent has reframed.** A Spirit
  capture or permanent-doc change that reframes a topic supersedes
  the older report's framing even when no successor report exists.
  Migrate the still-live substance (design alternatives, decision
  rationale, intermediate insight) and let the reframed parts
  drop. Waiting for a successor report before retiring is a smell
  — recent intent IS the supersession evidence.
- **Leaving stale examples alive in older reports.** If a report
  still shows old code as "current", "implemented", "recommended",
  or "canonical", the maintenance pass is incomplete even if a
  newer report corrects it. Search and agent recall will find the
  stale example. Rewrite the example to the current shape, or
  replace it with a short supersession note naming the current
  implementation and landing.
- **Retiring a report whose substance hasn't migrated.** Before
  dropping, confirm the load-bearing parts are captured elsewhere
  (an updated skill, an ARCH constraint, a successor report). If
  not, migrate first, then drop.
- **Treating context and reports as different disciplines.** They
  aren't. Both are working surfaces; both follow the same
  forward/migrate/keep/drop rule. A maintenance pass over only
  one is half a maintenance pass.
- **Keeping successor-superseded maintenance ledgers or deploy-event
  logs.** Once a newer sweep reissues the live handoffs, or a live
  system state becomes the baseline, the older ledger/event chain is a
  stale working artifact unless it still carries unresolved substance.
- **Over-formatting small thoughts.** A note-line is a note-line.
  Don't promote a half-formed observation to a numbered section or
  a dedicated report. The shape matches the substance.

## See also

- `~/primary/skills/context-maintenance-deep.md` — cross-lane
  meta-report directory, successor sweeps, lane retirement.
- `~/primary/skills/intent-maintenance.md` — Spirit capture
  sweep, dedup discipline, supersession mechanics.
- `~/primary/skills/reporting.md` §"Kinds of reports — and where
  their substance ultimately lives" — the typology of report
  shapes and their permanent homes.
- `~/primary/skills/reporting.md` §"Hygiene — soft cap,
  supersession, periodic review" — the disk-side hygiene rules
  this skill operationalizes.
- `~/primary/skills/skill-editor.md` §"Skills never reference
  reports" — the discipline that makes substance-migration
  possible (and necessary): once substance is in a skill, the
  report it came from can retire without leaving a dangling
  citation.
- `~/primary/skills/architecture-editor.md` §"Architecture files
  never reference reports" — same rule for ARCH.
- `~/primary/AGENTS.md` §"No harness-dependent memory" — the
  rule that memory belongs in workspace files every agent can
  read, not in harness-private state. Context maintenance is how
  that rule is honored across sessions.
