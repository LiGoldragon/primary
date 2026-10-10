# Ethos Production First Targets, Component Renames — 2026-08-02

> **Supersession notice (2026-08-06), REVERSED later the same day.** A
> ruling briefly superseded the universal-traits home (role memberships
> as encoded relations generating component-specific traits, no
> universal marker traits). The psyche reversed it: sections exist
> precisely so that position confers implementation of the universal
> Input/Output/Refusal traits, which are restored. The stream-side
> traits (StreamOpen/StreamEvent) await the open stream-role question.
> Both turns are recorded in `redesignAuditRulings-2026-08-06.md`; the
> design log reads by recency.

Agent text answered: the Ethos production bootstrap proposal
(`reports/EthosProductionBootstrapProposal-2026-08-02.md`), whose question
C recommended `signal-domain` as the first seating.

Psyche ruling [psyche-verbatim]: "first targets; spirit, mind,
orchestrator (former orchestrate; lets do the rename on this train) and
messenger (former message; same )"

Seated:

- The first production components whose public interfaces and traits Ethos
  produces are the core stack daemons: **spirit**, **mind**,
  **orchestrator**, **messenger**.
- Two renames ride this train, slated-rename pattern as with NOTA to
  Dotos: **orchestrate → orchestrator** and **message → messenger**. Until
  the train lands, existing code and docs keep the current names; new
  design writing may say "orchestrate (to be renamed orchestrator)".
- This supersedes the proposal's question C recommendation. The
  signal-domain ScopeOf byte-witness is not the first seating; the
  equivalence references for the four targets are their current
  handwritten public surfaces.

## Appended 2026-08-02: spirit simplification — manual data re-entry

Agent text answered: the spirit fixtures review and the manager's MVP
bead-writing commission.

Psyche ruling [psyche-verbatim]: "we can also simplify spirit; we can
manually re-enter the old database data in the new one; its pretty
small"

Seated: the spirit rebuild carries **no data-migration machinery** —
the old sema database's content is manually re-entered into the new
protos-based spirit's database. This makes spirit's full vertical
(interface, nexus, sema) the natural first complete landing: clean cut
end to end, no compatibility reader, no fold. The bead train reflects
this. (The data evolution engine remains a designed future capability,
untouched by this bootstrap choice.)

## Appended 2026-08-02: universal traits home confirmed — protos crate

Agent text answered: the MVP bead train presentation, naming the two
open decisions.

Psyche ruling [psyche-verbatim]: "protos crate confirmed; dispatch
codex for vq6.1-vq6.3"

Seated: the universal Input, Output, and Refusal traits — and the
stream-side StreamOpen and StreamEvent — live in the `protos` crate
("implementation-free component contracts for the Protos family").
The four daemons gain the dependency as their contract crates switch
over. Bead primary-vq6.4 closed; codex dispatched for slices
primary-vq6.1 through primary-vq6.3.

## Appended 2026-08-02: full signal-crate rename, executed on the switchover landings

Agent text answered: the manager's explanation of the rename-scope
decision (coherence versus blast radius, with the touch-once
sequencing recommendation).

Psyche ruling [psyche-verbatim]: "full rename confirmed; do it on
vq6.10 landings"

Seated: `signal-orchestrate`, `meta-signal-orchestrate`, and
`signal-message` rename with their daemons (`signal-orchestrator`,
`meta-signal-orchestrator`, `signal-messenger`), and each rename
executes inside that contract crate's Ethos switchover landing
(bead primary-vq6.10) — new generation source, new name, consumers
repinned, one atomic landing per crate. Bead primary-vq6.11 closed;
primary-vq6.12 keeps the remainder: daemon repo renames, binary
names, Nix service modules, and workspace references.
