# Skill — deep context maintenance

*Cross-lane orchestration, lane retirement, and the meta-report
directory pattern. Invoked when context maintenance spans multiple
lanes, multiple topic arcs, or a lane is being retired. The
everyday-use core lives in `skills/context-maintenance.md`; this
skill is for the heavier patterns that fire occasionally.*

## What this skill is for

Standard context maintenance — sweep a single lane's reports,
migrate substance, retire what's done — lives in
`skills/context-maintenance.md`. This skill carries the patterns
that fire when the sweep is broader:

- **Cross-lane sweeps** that orchestrate maintenance across
  designer + operator + system-operator + the various qualified
  lanes in a single pass.
- **Lane retirement** when a role identifier itself is being
  freed (per spirit record 213 + 920).
- **Successor sweeps** that retire prior maintenance ledgers
  cleanly.

The everyday core is reached for routinely; these patterns fire
once a sprint or once a quarter. Splitting them keeps the
everyday skill quick to scan and this skill comprehensive when
the broader sweep is called for.

## Cross-lane meta-report directory

Per psyche 2026-05-27 (spirit record 921, Maximum): cross-lane
context maintenance produces **one meta-report directory in the
DISPATCHER's lane**. When the discipline fires across multiple lanes
(review state of designer, operator, system-operator, and the various
qualified lanes in a single sweep), the output is NOT a flat list of
files scattered across each lane's reports/ subdir. That would split
context maintenance across lanes the maintenance pass is supposed to
oversee.

The default organization for a large sweep is **topic first, lane
handoff second**:

```
reports/<dispatcher-role>/<N>-cross-lane-context-maintenance-<date>/
  0-frame-and-method.md            (dispatcher: trigger, scope, method)
  1-<topic>.md                     (topic aggregation across lanes)
  2-<topic>.md
  ...
  N-overview.md                    (synthesis + per-lane handoffs)
```

The directory IS the meta-report (no `meta-` prefix). It is
garbage-collected as one session unit.

### Per-topic sub-report shape

Each topic sub-report is structured as a cross-lane aggregation. The
report may contain lane sections, but the first-order grouping is the
topic, because stale/forward/migrate/keep is judged by topic-recency
across lanes.

Standard structure per topic sub-report:

1. **Topic arc** — one-paragraph summary of the topic and any major
   era shift.
2. **Current canonical surface** — newest reports or permanent docs
   that remain load-bearing.
3. **Stale / forward / migrate / keep bands by lane** — per-report
   recommendations, grouped under the lane that owns the action.
4. **Landing evidence** — for every stale/drop recommendation, name
   the successor report or permanent home that absorbed the substance.
5. **Drop ownership / handoff** — close with concrete lane-owned
   actions: "When this lane next does maintenance, the relevant
   actions are: …".

### Per-lane handoffs and dispatcher authority

The overview gathers the topic reports into per-lane handoffs. The
receiving agent applies recommendations within its own lane; the
dispatcher does not execute drops in other lanes. The dispatcher may
execute only the actions it owns in its own lane, after verifying the
landing gate.

A per-lane sub-report is still acceptable for a narrow sweep whose
whole scope is one lane, or when the user specifically asks for a
lane-by-lane output. Even then, rank reports by topic inside the lane.
For broad cross-lane maintenance, topic reports are preferred and the
per-lane view is the synthesized handoff, not the primary structure.

### When to dispatch sub-agents

A sweep across more than 4–5 lanes or more than 3 major topics is
well-suited to parallel sub-agent dispatch (per
`skills/context-maintenance.md` §"Using agents for the sweep").
Allocate slot numbers + paths up-front per the meta-report
discipline in `skills/reporting.md` §"Meta-report directories —
sub-agent sessions" §"Pre-launch lane allocation". Assign
sub-agents by topic cluster unless a lane-specific cleanup is
small enough that lane ownership is the clearer split.

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
that retire. Reports whose only live purpose was auditing or
summarizing a retired-lane target are stale candidates too; keep or
migrate only their independent design rationale.

## Successor sweeps retire maintenance ledgers

A context-maintenance meta-report is itself a working artifact. It
retires when a newer sweep covers the same lanes/topics, re-ranks the
current surface, and re-issues the still-live handoffs. Do not keep two
live cross-lane sweep directories for the same scope; the newer sweep
becomes the active ledger, and the older one is dropped by its owning
lane once its handoffs are either applied or superseded.

This is the same rule as any other report: confirm that the newer sweep
absorbs the older sweep's live handoffs before dropping. The dispatcher
still does not delete another lane's prior sweep; it records that lane's
action in the handoff.

## Retiring a lane

Per psyche 2026-05-22 (spirit record 213), retiring a lane
identifier is gated on context maintenance completing on the
lane's leftover memories. The retired identifier should not free
until its memories find their right homes.

A cross-lane sweep may surface a lane as a retirement candidate when
all of its reports are stale, forwarded, migrated, or owned by a
successor lane. That finding is a recommendation, not the retirement
itself. Retiring an identifier requires explicit psyche direction and
the full methodology below.

Methodology when retiring a lane:

1. **Triage every report** under `reports/<retiring-lane>/` using
   the standard drop / forward / migrate / keep rule from
   `skills/context-maintenance.md` §2. Reports carrying live
   substance forward into a successor lane's
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
     `skills/architecture-editor.md` §"Carrying uncertainty";
     migrate the substance there, close the bead.
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

## See also

- `skills/context-maintenance.md` — the everyday-use core
  (forward/migrate/keep/drop method + per-item decisions +
  anti-patterns).
- `skills/intent-maintenance.md` — Spirit capture sweep,
  supersession, dedup discipline.
- `skills/reporting.md` §"Meta-report directories — sub-agent
  sessions" — the meta-report shape this skill orchestrates.
- `skills/reporting.md` §"Hygiene — soft cap, supersession,
  periodic review" — the disk-side hygiene rules these patterns
  operationalize.
- `skills/skill-editor.md` §"Skills never reference reports" —
  the discipline that makes substance-migration possible.
- `skills/architecture-editor.md` §"Architecture files never
  reference reports" — same rule for ARCH.
