# Overview — skill update needed

`skills/context-maintenance.md` already existed and captured most of the
discipline system-designer used in the cross-lane sweep. The requested
new skill was therefore not a create-from-zero task. It was an update
task. At audit time, `cloud-operator` held the skill-file claim; after
this read-only audit, that lane updated the skill and released the lock.

## Recommended Skill Patch

The skill should be changed in four concrete ways.

First, rename the cross-lane output shape from per-lane sub-reports to
per-topic aggregation reports. A cross-lane sweep should group reports by
topic across every lane, rank recency within the topic, and end each
topic report with lane-owned handoff bullets.

Second, preserve the dispatcher boundary. The dispatcher may delete only
inside the dispatcher's own report lane. Recommendations for other lanes
remain handoffs until that lane executes them.

Third, add the evidence rule for stale/drop recommendations. Every stale
or drop line should carry two anchors: the newer surface that supersedes
it and the permanent surface where the old substance now lives. Without
both, the report is not droppable yet.

Fourth, add the inventory-first subagent method. For large sweeps,
subagents should first classify by filenames, dates, lanes, and topic
clusters. They deep-read only candidate stale reports and the permanent
landing surfaces needed to verify absorption. This keeps the sweep broad
without pretending every old report received a full reread.

## Exact Replacement Direction

In `skills/context-maintenance.md`, the section named “Per-lane
sub-report shape” should become “Per-topic sub-report shape.” Its standard
structure should be:

1. Topic frame and current canonical surface.
2. Cross-lane inventory of all reports on the topic.
3. Recency ranking with newest canonical material first.
4. Drop, forward, migrate, or keep recommendation for each item.
5. Evidence for each drop: superseding surface plus permanent landing.
6. Lane-owned handoff bullets naming what each lane should do when it
   next performs maintenance.

The section named “When to dispatch sub-agents per lane” should become
“When to dispatch subagents by topic.” It should say that topic ownership
is the default for cross-lane sweeps; lane ownership is reserved for
explicitly lane-local maintenance or lane retirement.

## Post-Audit State

`cloud-operator` applied the key update in `skills/context-maintenance.md`:
the cross-lane output is now topic-first, per-topic reports carry
lane-owned handoffs, stale/drop entries require landing evidence, and
subagents are assigned by topic cluster by default. The stale blocker is
therefore gone. This report remains as the operator audit trail for the
subagent pass and the coordination decision not to edit through another
lane's claim.
