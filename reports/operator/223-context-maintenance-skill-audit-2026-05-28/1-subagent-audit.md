# Subagent Audit

Read-only subagent result, condensed.

## Already Present

- Topic-recency ranking across lanes is already in
  `skills/context-maintenance.md`.
- Staleness already requires both supersession and absorption into a
  permanent home.
- Dispatcher execution scope is already constrained: the dispatcher
  deletes only in its own lane and hands off recommendations elsewhere.
- Cross-lane meta-report directories are already in the skill.
- Lane-retirement gating is already in the skill, including reports,
  beads, open decisions, and Spirit record.

## Gaps

- The skill still says cross-lane output is made of per-lane sub-reports.
  The newer pattern from system-designer's sweep is per-topic aggregation
  reports with lane-owned handoff sections.
- Every stale or drop recommendation should name both the newer
  superseding report and the permanent landing surface: `INTENT.md`,
  per-repo `INTENT.md`, a skill, architecture, or code.
- The subagent method should start inventory-level: filenames, dates,
  topic clustering, and only then deep-read stale candidates and landing
  checks.
- The skill should name the era-shift pattern: once a topic re-grounds on
  a new architecture and that architecture lands in permanent docs, older
  reports in the prior era become droppable if their unique rationale is
  also preserved or not load-bearing.

## Ambiguities

- Topic ranking and per-lane output currently point in different
  directions. That can recreate the lane-scattered context that the new
  sweep was meant to prevent.
- “Drop” can read as immediate deletion. The skill should say explicitly:
  only the owning lane or the dispatcher in its own lane deletes; all
  other-lane drops are recommendations until that lane acts.
- Subagents should usually own topic clusters in a cross-lane sweep, not
  lanes. Lane subagents make sense only when the user asks for a
  lane-by-lane maintenance pass.

