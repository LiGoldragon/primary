# Overview — skill update needed

`skills/context-maintenance.md` already exists and captures most of the
discipline system-designer used in the cross-lane sweep. The requested
new skill is therefore not a create-from-zero task. It is an update task,
currently blocked for this lane by `cloud-operator`'s live claim on the
skill file.

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

## Current Blocker

`cloud-operator` holds the exact files needed for the edit. I did not
modify `skills/context-maintenance.md` because that would violate the
workspace claim discipline. The lock holder can apply the patch direction
above directly.

