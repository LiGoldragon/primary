# Skill — deep context maintenance

Cross-lane orchestration, lane retirement, and the cross-lane meta-report directory — the heavier maintenance patterns. Everyday single-lane sweeps live in `skills/context-maintenance.md`.

## When this fires

Reach here when a maintenance sweep is broader than one lane:

- Cross-lane sweeps spanning designer + operator + system-operator + qualified lanes in one pass.
- Lane retirement, when a role identifier itself is being freed.
- Successor sweeps that retire prior maintenance ledgers.

## Cross-lane meta-report directory

A cross-lane sweep lands as **one meta-report directory in the dispatcher's lane** — never scattered across each swept lane's `reports/`, which would split the maintenance across the very lanes it oversees. The directory mechanics — numbering, `0-frame-and-method.md`, the no-`meta-`-prefix rule, one-unit garbage collection — live in `reporting.md` §"Meta-report directories". This skill adds only what is specific to a cross-lane sweep:

- **Organize topic first, lane second.** Slices are topic aggregations (`1-<topic>.md` under an `<N>-cross-lane-context-maintenance-<date>/` directory), because stale/forward/migrate/keep is judged by topic-recency across lanes. The synthesis (`N-overview.md`) gathers the topic reports into per-lane handoffs.
- A per-lane slice is acceptable only for a narrow single-lane sweep, or when the psyche asks for lane-by-lane output — and even then, rank by topic inside the lane.

### Per-topic sub-report shape

Each topic slice carries:

1. **Topic arc** — one paragraph: the topic and any major era shift.
2. **Current canonical surface** — the newest reports or permanent docs that remain load-bearing.
3. **Stale / forward / migrate / keep bands by lane** — per-report recommendations grouped under the lane that owns the action.
4. **Landing evidence** — for every stale/drop, the successor report or permanent home that absorbed the substance.
5. **Drop ownership / handoff** — "when this lane next does maintenance, the relevant actions are: …".

### Dispatcher authority

The receiving agent applies recommendations within its own lane. **The dispatcher executes only the actions it owns in its own lane, and records — never executes — another lane's drop**, after verifying the landing gate. This single boundary governs the whole pattern: a cross-lane sweep produces handoffs, not cross-lane edits.

### Dispatching sub-agents

A sweep across more than 4–5 lanes or 3 major topics suits parallel sub-agent dispatch; assign agents by topic cluster, and allocate slot numbers + paths up-front (`reporting.md` §"Pre-launch lane allocation"). The everyday agent-dispatch mechanics are in `context-maintenance.md` §"Using agents for the sweep".

### Retired lanes — amalgamate, don't list

For a retired lane, amalgamate its interesting content into **2–3 topic-grouped summary reports** in the **main lane's** subdirectory (the one the retired identifier folds into) — not a report-by-report inventory. Reports whose only purpose was auditing or summarizing a retired-lane target are stale candidates too; keep or migrate only their independent design rationale.

## Successor sweeps retire maintenance ledgers

A context-maintenance meta-report is itself a working artifact. It retires when a newer sweep covers the same lanes/topics, re-ranks the current surface, and re-issues the still-live handoffs. Never keep two live cross-lane sweep directories for the same scope: the newer becomes the active ledger, and the older is dropped by its owning lane once its handoffs are applied or superseded — confirm the newer absorbs the older's live handoffs first (the landing gate from `context-maintenance.md`).

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
