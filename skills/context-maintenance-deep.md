# Skill — deep context maintenance

Cross-lane orchestration, lane retirement, and the cross-lane meta-report directory — the heavier maintenance patterns. Everyday single-lane sweeps live in `skills/context-maintenance.md`.

## When this fires

Reach here when a maintenance sweep is broader than one lane:

- Cross-lane sweeps spanning designer + operator + system-operator + qualified lanes in one pass.
- Lane retirement, when a role identifier itself is being freed.
- Successor sweeps that retire prior maintenance ledgers.

## Cross-lane meta-report directory

A cross-lane sweep produces **one meta-report directory in the dispatcher's lane** — not files scattered across each swept lane's `reports/` subdir, which would split the maintenance across the very lanes it oversees.

Organize topic first, lane handoff second:

```
reports/<dispatcher-role>/<N>-cross-lane-context-maintenance-<date>/
  0-frame-and-method.md   (dispatcher: trigger, scope, method)
  1-<topic>.md            (topic aggregation across lanes)
  2-<topic>.md
  ...
  N-overview.md           (synthesis + per-lane handoffs)
```

The directory IS the meta-report (no `meta-` prefix) and is garbage-collected as one session unit.

### Per-topic sub-report shape

Group by topic first, lane second — stale/forward/migrate/keep is judged by topic-recency across lanes. Each topic sub-report carries:

1. **Topic arc** — one paragraph summarizing the topic and any major era shift.
2. **Current canonical surface** — newest reports or permanent docs that remain load-bearing.
3. **Stale / forward / migrate / keep bands by lane** — per-report recommendations grouped under the lane that owns the action.
4. **Landing evidence** — for every stale/drop recommendation, name the successor report or permanent home that absorbed the substance.
5. **Drop ownership / handoff** — concrete lane-owned actions: "When this lane next does maintenance, the relevant actions are: …".

### Per-lane handoffs and dispatcher authority

The overview gathers topic reports into per-lane handoffs. The receiving agent applies recommendations within its own lane; the dispatcher executes only the actions it owns in its own lane, after verifying the landing gate. The dispatcher never executes drops in another lane.

A per-lane sub-report is acceptable for a narrow sweep whose whole scope is one lane, or when the user asks for lane-by-lane output — but even then, rank reports by topic inside the lane. For broad cross-lane maintenance, topic reports are primary and the per-lane view is the synthesized handoff.

### When to dispatch sub-agents

A sweep across more than 4–5 lanes or more than 3 major topics suits parallel sub-agent dispatch. Allocate slot numbers + paths up-front (`skills/reporting.md` §"Meta-report directories"). Assign sub-agents by topic cluster unless a lane-specific cleanup is small enough that lane ownership is the clearer split.

### Retired lanes — amalgamate, don't list

For a retired lane, amalgamate its interesting content into **2-3 topic-grouped summary reports** rather than a report-by-report inventory. The summaries land in the **main lane's** reports subdirectory (the one the retired identifier folds into). Reports whose only purpose was auditing or summarizing a retired-lane target are stale candidates too; keep or migrate only their independent design rationale.

## Successor sweeps retire maintenance ledgers

A context-maintenance meta-report is itself a working artifact. It retires when a newer sweep covers the same lanes/topics, re-ranks the current surface, and re-issues the still-live handoffs. Never keep two live cross-lane sweep directories for the same scope: the newer sweep becomes the active ledger; the older one is dropped by its owning lane once its handoffs are applied or superseded. As with any report, confirm the newer sweep absorbs the older's live handoffs before dropping — and the dispatcher records, rather than executes, another lane's drop.

## Retiring a lane

Retiring a lane identifier is gated on context maintenance completing on the lane's leftover memories: the identifier does not free until its memories find their right homes. A cross-lane sweep may flag a lane as a retirement candidate when all its reports are stale, forwarded, migrated, or owned by a successor — but that is a recommendation, not the retirement. Retiring an identifier requires explicit psyche direction plus the full methodology:

1. **Triage every report** under `reports/<retiring-lane>/` with the drop/forward/migrate/keep rule (`skills/context-maintenance.md`). Live substance forwards into the successor lane's `reports/`; mature substance inlines into permanent docs (architecture, skills, per-repo `INTENT.md`); the rest retire.
2. **Triage every bead** tagged with the lane's label:
   - **Close** — done, abandoned, or absorbed elsewhere; close-with-breadcrumb naming the new home.
   - **Reassign** — work continues under a successor lane; update labels.
   - **Promote to architecture** — a design idea that should live as a "Possible features" entry (`skills/architecture-editor.md`); migrate it, then close the bead.
3. **Resolve pending design decisions** the lane carried — settle now, abandon, or park as a "Possible future design" entry in the relevant architecture file.
4. **Surface the retirement in Spirit** alongside any successor lane mapping, so other agents see both in one record.
5. **Only then** is the identifier eligible for retirement; the empty `reports/<lane>/` directory can be removed.

Until a dedicated retired-lane sweep agent is hired, the prime designer (or any agent the psyche directs) handles retired-lane sweeps as standard context maintenance.

## See also

- `skills/context-maintenance.md` — everyday single-lane sweep core.
- `skills/intent-maintenance.md` — Spirit capture sweep, supersession, dedup.
- `skills/reporting.md` — meta-report directory shape and report hygiene.
