# 171 - Context maintenance refresh

Report kind: context maintenance
Topic: second-operator current state after skill, intent, designer, and operator refresh
Date: 2026-05-23
Lane: second-operator

## Prompt classification

The current psyche prompt is a work instruction: do context
maintenance, refresh essential skills, fresh intent, and fresh
designer/operator reports. It does not add durable psyche intent by
itself, so no new intent record was captured for this turn.

## Skills refreshed

Refreshed the workspace baseline and operator-critical skills:
`ESSENCE.md`, `INTENT.md`, `repos/lore/AGENTS.md`,
`orchestrate/AGENTS.md`, `skills/context-maintenance.md`,
`skills/intent-log.md`, `skills/skills.nota`, `skills/operator.md`,
`skills/designer.md`, `skills/role-lanes.md`,
`skills/autonomous-agent.md`, `skills/reporting.md`,
`skills/jj.md`, `skills/beads.md`, `skills/spirit-cli.md`,
`skills/naming.md`, `skills/repository-management.md`,
`skills/feature-development.md`, `skills/rust-discipline.md`,
`skills/rust/methods.md`, `skills/rust/errors.md`,
`skills/rust/storage-and-wire.md`, `skills/rust/parsers.md`,
`skills/rust/crate-layout.md`, `skills/nix-discipline.md`,
`skills/nix-usage.md`, `skills/testing.md`,
`skills/component-triad.md`, `skills/contract-repo.md`,
`skills/actor-systems.md`, `skills/kameo.md`,
`skills/architecture-editor.md`, `skills/nota-design.md`,
`skills/abstractions.md`, `skills/beauty.md`,
`skills/micro-components.md`, `skills/push-not-pull.md`,
`skills/architectural-truth-tests.md`, and
`skills/language-design.md`.

## Report maintenance decision

The lane has seven reports before this one, so it is under the soft
cap. I did not delete or agglomerate reports. The right maintenance
move is to mark the old current-state reports as historical and carry
their live substance forward here.

| Report | Decision |
|---|---|
| `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md` | Keep as shipped witness for the lane-registry slice. |
| `reports/second-operator/165-current-situation-2026-05-22.md` | Superseded as current-state snapshot by this report. Keep as history. |
| `reports/second-operator/166-review-persona-orchestrate-migration-2026-05-22.md` | Keep. Still relevant to `primary-c620` and the Orchestrate migration. |
| `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md` | Keep as Persona engine backlog rollup. |
| `reports/second-operator/168-review-mind-router-policy-2026-05-22.md` | Keep as mind-router policy rollup. |
| `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md` | Keep as Criome/Lojix authorization rollup. |
| `reports/second-operator/170-refresh-and-action-after-persona-systemd-followups-2026-05-22.md` | Superseded as current-state snapshot by this report. Keep as history. |

Primary working copy is already dirty with designer/system-designer
changes outside this lane, so this report should not be committed with
a broad `jj commit` until the working copy is split or those changes
are landed by their owners.

## Fresh intent absorbed

Spirit is live and returned records through 310. The most relevant
fresh records for this lane:

- 241: refresh reports and intent before selecting next work.
- 253: second-operator may pick up any currently free ready bead.
- 257: Spirit v0.1.0 protocol-aware maintenance build is the chosen
  path for no-downtime cutover.
- 258: selector-flip-aware routing belongs in the first FD-handoff
  infrastructure slice.
- 259: split `ComponentName` into `ComponentPrincipal` and
  `ComponentInstanceName`.
- 263: every component supports `(Help Main)` and `(Help (Verb ...))`
  through the NOTA argument vocabulary.
- 264: `signal-persona-auth` renames to `signal-persona-origin`.
- 266 and 267: the elegant `signal_cli!` macro is the intended CLI
  shape; the macro emits the full binary and injects caller context.
- 274: Mirror payload raw bytes stay outside typed redb until
  incorporated; typed Mirror payloads are deferred until a second
  component handover proves the need.
- 280: supervised persona components drop the `persona-` prefix.
- 303: horizon/lojix stacks migrate to the latest nota/signal/sema
  library versions.
- 307: persona signal repositories should be rearranged by socket
  authority.
- 309: `persona-sema` should be audited, useful material absorbed,
  then deleted.
- 310: `persona-llm-client` becomes `agent`, a supervised triad
  component with `agent`, `agent-daemon`, `signal-agent`, and
  `owner-signal-agent`.

## Fresh reports absorbed

Fresh operator reports `reports/operator/157-*` through
`reports/operator/163-*` establish the current handover foundation:
`version-projection`, `signal-version-handover`, `sema-engine`
`CommitSequence`, the sema-upgrade sandbox, Persona active-version
state, Spirit private upgrade socket, owner-version-handover
authority, and the systemd `UnitController` direction.

Fresh designer reports establish the current design surface:

- `reports/second-designer/156-most-important-gaps-2026-05-23.md`
  and `reports/second-designer/157-audit-engine-stack-state-before-constraint-and-integration-beads-2026-05-23.md`
  list engine-stack gaps and constraint/integration beads.
- `reports/second-designer/158-open-question-resolution-and-remaining-clarification-needs-2026-05-23.md`
  closes many handover questions and leaves the remaining design
  clarification surface.
- `reports/second-designer/159-intent-manifestation/` manifests
  three-tier signal sizing, binary naming, raw Mirror container,
  NOTA comments, and AgentError design.
- `reports/second-designer/160-persona-prefix-removal-coordinated-rename-2026-05-23.md`
  is now updated by later intent: `persona-sema` is deletion-bound
  and `persona-llm-client` becomes `agent`.
- `reports/designer/297-*` through `reports/designer/303-*` settle
  `signal-persona-origin`, Help operations, origin/caller identity,
  the elegant `signal_cli!` design, operator audit findings, and
  manifestation gaps.
- `reports/second-designer/161-design-cascade-and-context-sweep/0-frame-and-method.md`
  is the newest design-cascade frame, driven by intents 280, 309,
  and 310.

## Current implementation situation

The Persona handover stack is much stronger than the previous
second-operator snapshot: foundation crates exist, the Spirit sandbox
has exercised real daemons and a real database, Persona tracks active
versions, owner handover authority exists, and systemd production
management is the architectural direction.

The still-open shipping blockers are narrower:

- `primary-wdl6`: Spirit v0.1.0 protocol-aware maintenance build.
- `primary-x3ci`: cut over Spirit to v0.1.1 after current binary
  deployment; blocked by prefix rename and handover work.
- `primary-wvdl`: Persona port to current Signal stack and complete
  upgrade orchestration.
- `primary-0m1u`: coordinated persona-prefix removal of supervised
  components. This is now clearer because intent 309 deletes
  `persona-sema` and intent 310 renames `persona-llm-client` to
  `agent`.
- `primary-c620`: persona-orchestrate triad migration remains open.
  The executor-backed service slice landed at commit `ead19634`, but
  the broader contract redesign and migration work is not closed.
- `primary-36iq.6.1`: lojix port to current signal-lojix /
  signal-frame before bracket-string migration can close. The
  checkout has known dirty files from other work, so coordinate before
  editing.

Mirror payload application is a special watch item. Bead
`primary-wehu` is closed with commit `1ed90a36`, and the close reason
says the daemon-side handler now applies `StampedEntry` payloads.
The bead comment still says true sister-version reverse projection
and typed divergence persistence remain unimplemented in
`persona-spirit`. Treat Mirror as "implementation landed, residual
projection/divergence semantics need verification" until a follow-up
report or test closes the ambiguity.

## Bead queue shape

Most free P1 work currently clusters into four groups:

1. Persona/Spirit cutover and handover: `primary-wdl6`,
   `primary-x3ci`, `primary-wvdl`, `primary-q98d`, `primary-nobf`.
2. Component migration to current foundations: `primary-c620`,
   `primary-0bls`, `primary-9up1`, plus persona component triad
   migration beads such as router/message/system/harness/terminal.
3. Prefix and authority renames: `primary-0m1u`, `primary-7ru6`
   and related source-cascade work.
4. NOTA bracket-string and consumer migration: `primary-36iq` and
   `primary-36iq.6.1`.

No code edits were started from this refresh. The live operator
choice should be a claimed bead, not untracked opportunistic work.

## Questions needing psyche or lane coordination

1. Prefix removal now has two updates from fresh intent: `persona-sema`
   is deletion-bound and `persona-llm-client` becomes `agent`. Should
   `primary-0m1u` be rewritten before anyone starts the 24-repo rename,
   so operators do not execute the older ambiguous map?

2. Mirror payload application is marked closed, but its bead comment
   leaves residual projection/divergence work. Should that residual
   become a new bead, or is it already covered by an existing
   handover/cutover bead?

3. `primary-c620` remains open after the executor-backed slice. Should
   second-operator return to persona-orchestrate next, or should the
   lane prioritize the Spirit v0.1.0 retrofit / prefix-removal blockers
   because they gate `primary-x3ci`?

4. The primary working copy is dirty with designer/system-designer
   changes. Should this lane avoid committing reports until those land,
   or should we split only this report into its own jj commit once the
   current designer changes settle?
