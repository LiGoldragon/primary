# Corrected Operator Report Cleanup Prompt

Use this as the next fresh operator-lane prompt for continuing
`reports/operator/` cleanup.

## Prompt

Context handover for a fresh operator-lane session in `/home/li/primary`.

Purpose:
Continue operator report cleanup with fresh judgment. The goal is to eliminate
`reports/operator/` by routing each remaining report to exactly one fate:
intent, work, or abandon/bin.

Critical delegation rule:
Use one subagent for the first exploration. The main agent does only the Spirit
gate, lane registration/claim setup if needed, and the helper dispatch. The
main agent does not read the required files or the remaining reports before the
helper returns. The subagent must read the full required-reading envelope below
and return a distilled result. The main agent waits for that subagent and does
no independent exploration while waiting.

Required reading for the subagent, in order:

1. `ESSENCE.md`
2. `INTENT.md`
3. `repos/lore/AGENTS.md`
4. `skills/skills.nota`
5. `orchestrate/AGENTS.md`
6. `skills/session-lanes.md`
7. `skills/operator.md`
8. `skills/human-interaction.md`
9. `skills/intent-log.md`
10. `skills/spirit-cli.md`
11. `skills/intent-alignment.md`
12. `skills/context-maintenance.md`
13. `skills/context-handover.md`
14. `skills/when-to-use-helpers.md`
15. `skills/helper-context-transfer.md`
16. `skills/beads.md`
17. `skills/reporting.md`
18. `skills/jj.md`

Current state:
Old operator reports 299 through 423 were deleted under the agreed default.
That cleanup was committed and pushed as commit `10121fee`, "retire old
operator reports wave 1". `reports/operator/` now starts at report 424 and
ends at report 464.

The context-handover skill was created, then corrected. The corrected rule is:
a handover preserves accumulated information, topics, source locators, and
unresolved decisions so the next agent can exercise its own judgment. It is not
a script deciding what the next agent must do. The correction was captured in
Spirit as the context-handover correction record.

The helper-context-transfer rule was added after a failed attempt at this
handover: when a helper is being used to preserve the lead's context, the
helper receives the full required-reading envelope that the lead would otherwise
load. The lead keeps only the Spirit gate and dispatch mechanics.

Agreed cleanup default:
Operator implementation-history reports can be binned when their substance is
already landed in code, current docs, Spirit records, or existing beads. Create
or update beads only for concrete untracked implementation work. Use Spirit
only for exact durable psyche intent that is not already captured.

Remaining report clusters:

- 424-439: context maintenance, cluster propagation, criome/router/spirit
  propagation, kameo, live Spirit/store and VM test status.
- 440-455: Mentci/Criome approval UI and bridge work, recent
  integration/audits, parallel fix planning.
- 456-460: Spirit authorization trace, AuthorizeSignalCall explainer,
  guardian/criome workflow and guard-substrate comparisons.
- 461-462: external workflow/session-management research.
- 463-464: Spirit guardian psyche/advocacy split and the prior
  context-maintenance correction handover.

Important unresolved topic:
The Mentci/Criome approval reports contain an open decision about "client
approval mode". Two known readings:

- daemon-wide hold mode: Criome parks every authorization submission for human
  approval;
- per-contract escalation: only policies using `EscalateToPsyche` park work for
  Mentci.

This affects what implementation bead, if any, should absorb the remaining
Mentci/Criome reports before deletion.

Subagent exploration scope:
Inspect the remaining `reports/operator/` files without editing. Check the open
bead list and relevant public Spirit records. Return clusters by likely fate:

- safe to delete under the agreed default;
- concrete untracked work that should become beads;
- possible first-degree psyche intent requiring Spirit capture or update;
- the highest-leverage unresolved question for the psyche.

Source locators and commands for the subagent:

- `reports/operator/`
- `bd list --status open --limit 0`
- Spirit search terms: `context maintenance`, `context handover`, `Mentci`,
  `Criome`, `client approval`, `guard substrate`, `AuthorizeSignalCall`

The subagent should not edit files. It should report the evidence it used:
report paths, bead titles or identifiers with descriptions, Spirit record
descriptions where relevant, and the reasoning for each proposed fate. The main
agent applies the final disposition after the subagent returns.
