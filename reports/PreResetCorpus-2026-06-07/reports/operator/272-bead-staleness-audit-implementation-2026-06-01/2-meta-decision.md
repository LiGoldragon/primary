# 272.2 — Meta decision

## Decision

Implement the high-confidence operator-safe bead cleanup now:

1. Close verified P0/P1 stale beads in four families:
   persona-spirit handover/cutover, legacy `signal_channel!` and Tap
   observability, persona-prefix rename remnants, and persona-stack
   migration backlog.
2. Refresh the live cloud/domain-criome beads with current labels and
   notes instead of closing them.
3. Refresh `primary-a1px` with the designer 446 Phase 0 anchor instead
   of closing it.
4. Close `primary-duuv` as shipped, because its bead note and designer
   444 both confirm DatabaseMarker propagation is live.
5. Leave uncertain items open with explicit postmortem notes rather than
   over-closing.

## What will not be done now

This session will not edit designer reports or source code. The audit's
implementation surface is BEADS plus operator reports.

This session will not bulk-close all estimated P2/P3 stale beads. Report
449's P2/P3 layer was sampled and extrapolated; the current session
verified the P0/P1 layer deeply and only touches P2/P3 beads that appear
as direct children of the already-verified stale families or are
explicitly named in live queries.

This session will not close `primary-lrf8` as shipped. Its acceptance
criteria are broader than the evidence re-read here.

This session will not convert `primary-9hx0` into a designer-report
bead. That is a designer-owned design-question cleanup. The bead remains
open, and the postmortem will recommend designer action.

This session will not rewrite `primary-54ti` or deploy-stack beads. That
work belongs to cluster/system operator context and needs deploy-stack
reading before mutation.

## Authority boundaries

BEADS is shared coordination state and not lane-owned. Any agent may
close or update beads when the reason is documented. This operator
subagent has explicit authorization from the psyche prompt to implement
report 449, so closing verified stale beads is inside scope.

Reports are lane-owned. This session writes only under
`reports/operator/272-bead-staleness-audit-implementation-2026-06-01/`.

Source edits would require repo-local `AGENTS.md`, `INTENT.md`,
`ARCHITECTURE.md`, and `skills.md` reading plus operator path claims.
No source edit is planned.

## Implementation groups

Close with family notes:

- Persona-spirit handover/cutover:
  `primary-602y`, `primary-0jjz`, `primary-1jql`, `primary-ekxx`,
  `primary-x3ci`, `primary-x3ci.1`, and direct P2 child
  `primary-dlut`.
- Legacy macro and Tap substrate:
  `primary-3cl1`, `primary-bg9l`, `primary-l02o`, `primary-v5n2`,
  `primary-ezqx`, `primary-ezqx.1`, `primary-ezqx.3`,
  `primary-muu2`, `primary-bann`, `primary-145a`, `primary-8avm`,
  and direct P2 blocker `primary-b86d`.
- Persona-prefix rename remnants:
  `primary-0m1u`, `primary-0m1u.11`, `primary-0m1u.12`.
- Persona-stack migration backlog:
  `primary-a5hu`, `primary-4naq`, `primary-c620`, `primary-gu7t`,
  `primary-qjdp`, `primary-21gn`, `primary-krbi`, `primary-li7a`,
  `primary-aunn`, `primary-e1pm`, `primary-gvgj`, `primary-gvgj.3`,
  `primary-gvgj.4`, `primary-gvgj.5`, `primary-gvgj.6`,
  `primary-gvgj.7`, `primary-gvgj.8`, `primary-gvgj.9`,
  `primary-gvgj.10`, `primary-nobf`, `primary-q98d`,
  `primary-wvdl`, `primary-hj4`, `primary-hj4.1`, `primary-devn`,
  `primary-8n8`, `primary-07ot`, `primary-ojxq`, `primary-0bls`,
  and `primary-9up1`.

Update with notes and labels:

- `primary-kbmi` and `primary-kbmi.2`: remove
  `role:system-specialist`, add `role:operator`, and append a note
  anchoring the live work at designer 446 Phase 1a / cloud wave.
- `primary-a1px`: append a note anchoring the follow-up at designer 446
  Phase 0 spirit fold.

Close as shipped:

- `primary-duuv`: DatabaseMarker propagation, closed with a breadcrumb
  to designer 444 and its own live note.

## Verification after implementation

After the bead writes:

- Re-run `bd count --status open` and `bd count --status open
  --by-priority`.
- Re-run spot queries for closed families to ensure the intended IDs
  are no longer open.
- Re-run `tools/orchestrate status`, release the operator task lock,
  and verify no lock is left behind.
- Commit and push only this session's operator report directory and the
  BEADS database changes. Leave unrelated working-copy paths untouched.
