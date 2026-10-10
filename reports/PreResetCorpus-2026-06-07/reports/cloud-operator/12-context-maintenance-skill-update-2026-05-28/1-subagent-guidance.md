# Context-maintenance skill update guidance — 2026-05-28

Read-only guidance for updating `skills/context-maintenance.md` from the `system-designer/44` cross-lane sweep. No files were edited except this guidance report.

## Key evidence read

- `skills/context-maintenance.md:69-100` already requires topic-recency ranking, but `:216-263` still describes cross-lane output as per-lane sub-reports.
- `reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/0-frame-and-method.md:25-29` states the actual 2026-05-28 method: topic-aggregated output, not a flat per-lane dump; dispatcher executes only own-lane drops.
- `0-frame-and-method.md:47-55` adds a scalable method: inventory first, deep-read stale candidates, verify permanent landing, recommend only.
- `6-overview.md:7-9` shows the decisive rule: a prior report pile becomes drop-eligible only after substance has landed permanently and the newer era supersedes the old framing.
- `6-overview.md:38-52` shows per-lane handoffs, lane-retirement candidates, successor-sweep retirement, and pending psyche-review flags.
- `3-cloud-and-deployment.md:61-82` shows cross-lane forward-then-drop: old source lane owns the drop, receiving cloud lane confirms/absorbs substance first.
- `4-persona-runtime-spirit-upgrade.md:73-79` and `:153-160` show deploy-event chains retiring as a block once live state is baseline and audited.
- `5-workspace-pi-nota-and-misc.md:81-94` shows a prior cross-lane sweep retiring once a newer sweep re-ranks the same scope and reissues handoffs.
- `skill-editor.md:179-215` is binding for the edit: the skill must inline the permanent rules and must not cite reports.

## Permanent rules to add or sharpen

1. **Topic-aggregation is the default shape for broad cross-lane sweeps.** Keep per-lane ownership, but make topic sub-reports the primary output when the problem is stale reports lingering across lanes.
2. **Every stale flag needs a proof pair:** the newer canonical/superseding artifact and the permanent landing or successor report that absorbed the old substance. If either side is missing, the action is forward, migrate, or keep — not drop.
3. **Name the supersession spine / era boundary.** When a topic has moved from an old substrate or framing to a new permanent surface, state the old era, the new era, and the permanent landing before recommending bulk drops.
4. **Cross-lane forward-then-drop has two owners.** The source lane owns the eventual deletion; the receiving lane/report confirms that the substance landed first.
5. **Maintenance ledgers and prior sweep meta-directories are working artifacts.** A prior sweep retires when a newer sweep covers the same or broader scope, carries forward unresolved decisions, and reissues handoffs.
6. **Deploy-event chains, orientation refreshes, and shipped implementation threads retire as blocks** once the live state is baseline and the durable state is in permanent docs/runbooks/current reports.
7. **Audit reports usually retire with their audited target.** Keep or migrate only if the audit contains independent design rationale or a reusable pattern.
8. **Pending psyche-review items are not stale just because old.** Keep and surface them until resolved, explicitly abandoned, or parked in the appropriate architecture/permanent uncertainty section.
9. **Lane-retirement candidates are surfaced, not decided, by context maintenance.** Evidence can be “all reports stale,” “lane empties after handoffs,” or “successor lane absorbs the work,” but the retirement decision remains psyche/lane-governance territory.

## Existing text that is stale or insufficient

- `context-maintenance.md:216-263` is stale: it says cross-lane meta-reports contain per-lane sub-reports, but the successful 44 sweep used per-topic aggregation with lane-owned handoff sections.
- `context-maintenance.md:193-210` is too generic: it describes giving agents batches of reports, but not the inventory-first, candidate-deep-read method used for ~237 reports.
- `context-maintenance.md:101-110` is too compact for cross-lane forwarding and verified drops. The action table should encode proof-backed drop and forward-then-drop ownership.
- `context-maintenance.md:141-160` is still good; keep the design-rationale guard. It pairs well with the new audit-retirement rule.
- `context-maintenance.md:274-287` is useful for retired lanes but lacks the “reports/audits about retired-lane targets are stale candidates” corollary.
- `context-maintenance.md:289-327` explains how to retire a lane, but should add that maintenance may only identify candidates unless psyche has approved retirement.
- `context-maintenance.md:331-354` has the right anti-patterns; add one more: keeping old sweep ledgers or deploy-event logs after a successor/current-state landing exists.

## Exact small edit recommendations

1. **In `Topic-recency ranking` (`:69-100`):** add a new step after recency ranking:
   - “Name the supersession spine: newest canonical artifacts, permanent landings, and any old-era/new-era boundary.”
   Then strengthen stale flagging to require both a superseder and a landing home.

2. **In the action table (`:105-110`):** adjust two rows:
   - `Forward`: include cross-lane forward-then-drop; receiver confirms absorption, source lane owns deletion.
   - `Drop`: say drop only after the superseder and landing are named; otherwise keep/forward/migrate.

3. **Add a short heuristic block after the action table:** include audit reports retiring with audited targets, deploy-event/orientation chains retiring after live-state landing, and pending psyche-review items staying keep/escalate.

4. **In `Using agents for the sweep` (`:193-214`):** add the scalable method:
   - inventory and topic-cluster first;
   - deep-read only stale candidates and their newer/permanent targets;
   - agents recommend, dispatcher/lane owner executes.

5. **Rewrite the start of `Cross-lane meta-report directory` (`:216-240`):** replace “with per-lane sub-reports inside” with topic-aggregation by default. The code block should show `1-<topic>.md` entries, not `1-<first-lane>.md` entries.

6. **Replace or demote `Per-lane sub-report shape` (`:241-263`):** make the main subsection `Topic-aggregation sub-report shape` with this shape:
   - topic scope and inventory;
   - supersession spine;
   - recency rank newest-first;
   - drop/forward/migrate/keep grouped by owning lane;
   - lane handoff section naming exactly what each lane applies.
   Keep per-lane sub-reports only as a fallback for narrow sweeps.

7. **Add sweep-retirement rule near `Cross-lane meta-report directory`:** a prior sweep meta-directory retires when a newer sweep covers the same scope, carries unresolved decisions forward, and reissues handoffs.

8. **Add lane-candidate note near `Retiring a lane` (`:289-327`):** context maintenance may surface retirement candidates, but does not decide retirement without psyche/lane-governance approval.

9. **Add one anti-pattern (`:331-354`):** “Keeping successor-superseded maintenance ledgers or deploy-event logs after live/permanent landing exists.”

10. **Skill-editor constraint for the parent edit:** do not add `system-designer/44` or any report path to `context-maintenance.md` as a citation or See-also entry. Inline the rules; reports are ephemeral.
