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
3. **Flag what's stale.** A report is *stale* when a newer
   report on the same topic supersedes it (rewrites the framing,
   replaces the design, completes the audit) AND the older
   report's substance is already absorbed in the newer report or
   a permanent doc. Stale reports drop. Not-yet-stale older
   reports — substance still load-bearing on its own, design
   alternatives a newer report inherits, decision rationale that
   permanent docs don't carry — keep, forward, or migrate per
   §"Per item, decide" below.
4. **Favor newer design.** When older and newer reports
   conflict, the newer is canonical unless the older holds
   substance the newer doesn't (design alternatives, decision
   rationale, intermediate insight the newer skipped).

Reports without an obvious topic peer across lanes get the same
treatment with a single-lane recency timeline.

### 2a · Per item, decide

For each report or context theme, pick one of four actions:

| Action | When |
|---|---|
| **Forward** | Substance is still load-bearing as a working artifact. Roll it forward into a successor report or extend an existing one; retire the predecessor. |
| **Migrate** | Substance is mature enough to be permanent. Inline it into a skill, `ARCHITECTURE.md`, `ESSENCE.md`, or code. Retire the source. |
| **Keep** | Substance is load-bearing on its own and has no permanent home yet. Rare. Foundational decisions still searching for their final shape. |
| **Drop** | Substance is stale, addressed, superseded, or already captured elsewhere. Delete the report (or simply let context lose it). |

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
   new substance. The handover happens in place.
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

### 3a · Design-rationale guard against premature DELETE

A report carrying **competing design alternatives** — multiple
options sketched, one chosen, others rejected — is load-bearing
*as design rationale* even after the chosen option migrates to a
permanent doc. Permanent docs typically state only the chosen
shape; the rejected alternatives and the reasoning are what the
report preserves.

Per intent record 229 (closing duplicate beads preserves
information; competing design ideas kept), do NOT DELETE such a
report when its chosen-design substance migrates. Add a
STATUS-BANNER naming the permanent-doc landing instead, so a
later reader sees the supersession and can find the chosen shape
without losing the alternatives.

Signal that a report falls under this guard: it explicitly
enumerates two or more designs (Design A / B / C / D, Option 1 /
2, etc.) and chose one. Standard design reports that propose a
single shape do not need this guard — they migrate cleanly.

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

- Give each agent a small batch of older reports + the
  drop/forward/migrate/keep rule from §2.
- Each agent reads the report, checks the surrounding permanent
  docs (does this substance already live in ARCH? in a skill?
  has it been superseded?), then proposes the action.
- Review the agent's proposals; execute the migrations; retire
  the reports.

This keeps the orchestrator's context light. The orchestrator's
role is to apply decisions, not to re-read every report.

For context-only substance (the part that lives in the live
conversation, not on disk), the orchestrator does this sweep
itself — agents can't see the conversation's working memory.

## Cross-lane meta-report directory

Per psyche 2026-05-27 (spirit record 921, Maximum): cross-lane
context maintenance produces **one meta-report directory in the
DISPATCHER's lane** with per-lane sub-reports inside.

When the discipline fires across multiple lanes (review state of
designer, operator, system-operator, and the various qualified
lanes in a single sweep), the output is NOT a flat list of
per-lane files scattered across each lane's reports/ subdir.
That would split context maintenance across lanes the
maintenance pass is supposed to oversee. Instead:

```
reports/<dispatcher-role>/<N>-cross-lane-context-maintenance-<date>/
  0-frame-and-method.md            (dispatcher: frame, method, lane list)
  1-<first-lane>.md                (per-lane sub-report)
  2-<second-lane>.md
  ...
  N-overview.md                    (dispatcher: synthesis across lanes)
```

The directory IS the meta-report (no `meta-` prefix). It is
garbage-collected as one session unit.

### Per-lane sub-report shape

Each per-lane sub-report is structured as a **handoff document**
the agent in that role reads when they do their own next context
maintenance. The receiving agent applies the recommendations
within their own lane; the dispatcher does not execute drops in
other lanes (only in their own).

Standard structure per sub-report:

1. **Inventory** — list of reports in the lane with date and a
   one-line summary each.
2. **Topic clusters** — group reports by topic.
3. **Recency rank per topic** — newest at top; flag what's stale
   (older than the newest by a meaningful gap, especially when a
   newer report supersedes substance).
4. **Drop / forward / migrate / keep recommendation per report**
   — per the §"Per item, decide" rule.
5. **Handoff section** — closes with "When you (the agent in
   this role) do your next context maintenance, the relevant
   decisions are: …" — concrete pointers to the recommendations
   above and any cross-cutting context the role's next pass
   should know.

### When to dispatch sub-agents per lane

A sweep across more than 4–5 lanes is well-suited to parallel
sub-agent dispatch (per §"Using agents for the sweep" above) —
each sub-agent owns one lane's sub-report; the dispatcher
allocates slot numbers + paths up-front per the meta-report
discipline in `skills/reporting.md` §"Meta-report directories —
sub-agent sessions" §"Pre-launch lane allocation".

### Retired lanes — amalgamate, don't list

For lanes that have been retired (per spirit record 920, the
`<role>-assistant` suffix is retired and existing
`reports/<role>-assistant/` directories fold into the main lane),
the cross-lane sweep amalgamates the retired lane's interesting
content into **2-3 topic-grouped summary reports** rather than a
report-by-report inventory. The summary reports land in the
**main lane's** reports subdirectory (the one the retired
identifier is folding into).

This applies to all retired lanes: the prior `-assistant`
variants, the prior `-specialist` variants, and any future lanes
that retire.

## Retiring a lane

Per psyche 2026-05-22 (spirit record 213), retiring a lane
identifier is gated on context maintenance completing on the
lane's leftover memories. The retired identifier should not free
until its memories find their right homes.

Methodology when retiring a lane:

1. **Triage every report** under `reports/<retiring-lane>/` using
   the standard drop / forward / migrate / keep rule from §2.
   Reports carrying live substance forward into a successor lane's
   `reports/<successor>/` directory; reports carrying mature
   substance get inlined into permanent docs (architecture,
   skills, per-repo `INTENT.md`); the rest retire.
2. **Triage every bead** tagged with the retiring lane's label.
   Each gets one of:
   - **Close** — work done, abandoned, or already absorbed
     elsewhere; close-with-breadcrumb naming the new home.
   - **Reassign** — work continues under a successor lane; update
     the bead's labels.
   - **Promote to architecture** — bead carried a design idea
     that should live as a "Possible features" entry per
     `~/primary/skills/architecture-editor.md` §"Carrying
     uncertainty"; migrate the substance there, close the bead.
3. **Take any pending design decisions** the lane was carrying —
   for each open question: settle it now, abandon entirely, or
   park as a "Possible future design" entry in the relevant
   architecture file.
4. **Surface the retirement in spirit** alongside any successor
   lane mapping (so other agents see the retirement and the
   successor in the same record).
5. **Only after the above** is the identifier itself eligible
   for retirement; the lane's `reports/<lane>/` directory can be
   removed if empty.

**Forward** (psyche 2026-05-22): a dedicated context-maintenance
agent for retired-lane sweeps will eventually be hired into the
workspace. Until that agent exists, the prime designer (or any
agent the psyche directs) handles retired-lane sweeps as part of
standard context maintenance.

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
- **Retiring a report whose substance hasn't migrated.** Before
  dropping, confirm the load-bearing parts are captured elsewhere
  (an updated skill, an ARCH constraint, a successor report). If
  not, migrate first, then drop.
- **Treating context and reports as different disciplines.** They
  aren't. Both are working surfaces; both follow the same
  forward/migrate/keep/drop rule. A maintenance pass over only
  one is half a maintenance pass.
- **Over-formatting small thoughts.** A note-line is a note-line.
  Don't promote a half-formed observation to a numbered section or
  a dedicated report. The shape matches the substance.

## See also

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
