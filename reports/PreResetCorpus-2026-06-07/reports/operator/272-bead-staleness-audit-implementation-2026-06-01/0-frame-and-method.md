# 272.0 — Frame and method

## Scope

This operator-lane subagent session verifies
`reports/designer/449-bead-staleness-audit-2026-06-01.md` against
the live workspace and implements the parts that are correct and
inside operator authority.

The requested output is a meta-report directory under
`reports/operator/` with verification, decision, implementation, and
postmortem reports. Reports are exempt from the claim flow. Any source
edit would require the target repository's local agent context and an
operator claim before editing. This session has not yet needed source
edits.

## Required reading completed

Read before action:

- `ESSENCE.md`
- `INTENT.md`
- `repos/lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `AGENTS.md`
- `skills/operator.md`
- `skills/context-maintenance.md`
- `skills/reporting.md`
- `skills/jj.md`
- `reports/designer/449-bead-staleness-audit-2026-06-01.md`

Additional directly relevant context read:

- `skills/skills.nota` entries for operator, reporting,
  role-lanes, jj, beads, context-maintenance, spirit-cli, and
  intent-maintenance.
- `skills/beads.md`
- `skills/spirit-cli.md`
- `skills/role-lanes.md`
- `skills/intent-maintenance.md`

Spirit queries run:

- Recent all-topic intent with provenance.
- Recent matching intent for schema, NOTA, spirit, bead staleness,
  and context maintenance.

## Verification method

The verification does not assume report 449 is correct. It checks:

1. Whether the headline bead count and priority distribution match
   live `bd` output.
2. Whether the named high-impact bead clusters still exist and are
   open.
3. Whether the cited current-intent anchors still support the
   supersession reasoning.
4. Whether the proposed actions fall inside operator authority.
5. Whether any action would edit another lane's reports, source files,
   or design-owned guidance without authorization.

## Constraints

- The workspace has unrelated uncommitted changes, including the
  designer report being implemented. This session must not overwrite
  or commit those unrelated paths.
- `jj` is the only version-control interface for commits and pushes.
  Description-taking commands must use inline messages.
- BEADS is shared coordination state, not a lock surface. For a
  substantive bead action this session uses an operator task lock.
- BEADS database lock errors are treated as transient storage
  contention; reads are retried rather than manually unlocking.
- Designer report 449 itself says the audit is a proposal surface and
  says not to close beads in that pass. This session is the separately
  authorized operator implementation pass, so it may close or update
  beads only after independent verification.

## Initial live-state observations

- `jj st` shows unrelated working-copy changes outside this session,
  including `reports/designer/449-bead-staleness-audit-2026-06-01.md`
  and `skills/spirit-cli.md`. These are not this session's edits.
- `bd count --status open` returned `269`, confirming the headline
  open-bead count in report 449 at the start of this session.
- A concurrent `bd list --status open --limit 0 --json` attempt hit
  the embedded Dolt exclusive lock. This matches `skills/beads.md` and
  will be retried.
- `tools/orchestrate status` showed the operator lane idle and
  `system-operator` actively claiming Spirit deployment paths plus
  `skills/spirit-cli.md`; this session will not touch those paths.
