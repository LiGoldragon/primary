*Kind: Frame · Topic: schema-stack-context-maintenance-sweep · Date: 2026-05-24*

# 319 · Frame — designer-lane context maintenance sweep, schema-stack focus

## §1 Psyche ask + intent context

> rework all your reports @skills/context-maintenance.md - focus on
> this migration to a full schema stack - we could have a schema
> component that keeps track of all the schemas in the engine, and
> can give the schema using the small header.
>
> [follow-on] so obviously the schemas in schema component are stored
> much more efficiently than in nota text format
>
> [follow-on] and it exposes a schema type libs of macro - for signal
> and sema
>
> [follow-on] the macro lib can be a different repo if its better

Four schema-component intents captured before this sweep:

- **Spirit 397** (schema-component · Principle · Medium) — schema
  component as dedicated triad serving schema lookups keyed by the
  short header.
- **Spirit 398** (schema-component · Clarification · Maximum) —
  schemas stored in efficient binary form, not NOTA text; NOTA is
  the source format, the schema component holds compiled runtime
  representation.
- **Spirit 399** (schema-component · Clarification · Maximum) —
  exposes a schema type library that signal-side and sema-side
  macros consume (three faces: daemon, library, macro substrate).
- **Spirit 400** (schema-component · Clarification · Medium) —
  the macro library may live in a separate repo from the daemon
  if separation works better.

Upstream intent context (from earlier session): spirit 366
(next-as-dep), 369 (upgrade triad), 388-392 (short header +
sema short header + NOTA schema language + MVP even-byte scope).
These define the schema-stack target that this sweep consolidates
toward.

**Important non-overlap:** second-designer is writing the
forward-looking design `/319` in their own lane
(`reports/second-designer/<N>/`) per the psyche's prior
direction. This sweep is designer-side context maintenance,
NOT design work; we triage older reports and migrate substance
to permanent docs (or retire), leaving the forward design to
second-designer.

## §2 Method per `skills/context-maintenance.md`

Inventory the surface; per-item decide drop / forward / migrate /
keep; distribute substance to permanent homes; aggressive per
spirit 362 (deleted reports retrievable from commit tree per
spirit 370). Three parallel subagent slices, plus orchestrator
synthesis.

### §2.1 Slice contracts

- `0-frame-and-method.md` (this file).
- `1-schema-stack-substance-triage.md` (Subagent A) — reports
  carrying schema-stack-relevant substance. Triage what migrated
  to permanent docs (signal-frame ARCH, version-projection ARCH,
  upgrade-triad ARCH after operator's landing), what's still
  load-bearing for second-designer's forward design, what retires.
- `2-working-artifacts-triage.md` (Subagent B) — sweeps,
  handovers, audit working artifacts. Most are by-construction
  finite-lifetime; retire when their outputs absorb.
- `3-separate-concerns-triage.md` (Subagent C) — reports on
  non-schema-stack concerns (agent abstraction, forge, pi,
  systemd, older snapshots). Triage for migration to relevant
  ARCH/skills or retirement.
- `4-overview-and-retirement-list.md` (orchestrator synthesis) —
  the consolidated triage decision per report, the deletions to
  execute, the migrations to land, and what designer-lane
  carries forward.

### §2.2 Slice A — schema-stack substance triage

Subagent A triages these reports against current state. For each:
identify what substance has already migrated (to signal-frame
ARCH, version-projection ARCH, upgrade-triad ARCH, skills) and
what's still load-bearing for second-designer's forward design.

Inventory (under `/home/li/primary/reports/designer/`):

- `263-schema-specification-language-design.md`
- `279-nota-schema-language-and-version-hash.md`
- `285-versionprojection-trait-and-handover-protocol-specification.md`
- `287-version-handover-component-explained.md`
- `305-nota-user-guide-and-codec-architecture/` (directory)
- `305-v2-design-64bit-signal-per-component-namespacing.md`
- `307-design-golden-ratio-namespace-split.md`
- `308-design-pretyped-envelope-and-tap-anywhere.md`
- `312-design-recursive-help-on-every-enum.md`
- `315-design-sema-upgrade-and-handover-current-state.md`
- `317-sema-upgrade-and-macro-convergence-audit/` (directory)
- `318-upgrade-merger-and-persona-prefix-rename/` (directory)

Special handling per `skills/context-maintenance.md §3a`:
**design-rationale guard** — a report enumerating multiple
design alternatives (Design A/B/C, Option 1/2/3) is load-bearing
as rationale even after the chosen option migrates. Don't DELETE
such reports; add a STATUS-BANNER naming the permanent landing
and keep them.

For schema-stack reports specifically: `/263` and `/279` carry
the schema-language alternatives that second-designer's forward
design will reshape. These may need the design-rationale guard
rather than outright deletion.

### §2.3 Slice B — working artifacts triage

Subagent B triages working-artifact reports (sweeps, handovers,
audits, manifestations). These are by-construction finite-lifetime
per `skills/context-maintenance.md`.

Inventory:

- `297-design-signal-persona-auth-rename.md`
- `298-design-help-operations-in-components.md`
- `299-design-origin-process-and-agent-identity.md`
- `300-design-cli-macro-caller-context-injection.md`
- `301-design-elegant-cli-macro-with-caller-injection.md`
- `302-audit-recent-operator-work-2026-05-23.md`
- `303-intent-manifestation-sweep-2026-05-23.md`
- `304-unimplemented-intent-audit-2026-05-23.md`
- `306-manifestation-sweep-round-2-2026-05-23.md`
- `310-meta-overhaul-booking-roadmap.md`
- `311-context-maintenance-sweep-2026-05-23.md`
- `313-great-summary-and-handover-2026-05-24.md`
- `314-aggressive-consolidation-sweep-2026-05-24.md`

For each: identify whether the artifact's outputs landed (per
spirit 370 the commit tree carries the lineage). If outputs
landed, the working artifact retires; if outputs are still in
flight (e.g., `/313`'s next-session targets are still open),
forward into the current state or migrate to permanent docs.

### §2.4 Slice C — separate concerns + older reports triage

Subagent C triages reports on non-schema-stack concerns (agent
abstraction, forge family, pi-related work, persona systemd
units, older state snapshots) for migration to relevant ARCH/
skills or retirement.

Inventory:

- `249-component-intent-gap-analysis.md`
- `257-signal-contracts-names-and-shape-audit.md`
- `264-designing-protocol-and-role-spaces.md`
- `266-persona-pi-triad-design.md`
- `268-persona-pi-operator-input.md`
- `281-headless-pi-research.md`
- `282-workspace-implementation-status.md`
- `291-persona-systemd-units-for-daemon-management.md`
- `292-designer-lane-top-issues-2026-05-22.md`
- `293-designer-and-research-batch-2026-05-23/` (directory)
- `294-most-important-gaps-visual.md`
- `309-design-agent-component-abstraction.md`
- `316-design-forge-family-current-direction.md`
- `pi-api-surface-notes.md` (non-numbered)

For each: identify whether substance migrated to relevant ARCH
(persona-pi/ARCHITECTURE.md, forge ARCH, etc.) or skills. Drop
if absorbed; forward if still load-bearing for its concern;
migrate if the substance fits permanent docs.

## §3 Hard constraints across all slices

- **READ-ONLY on code and ARCH files.** This sweep is triage,
  not migration. Substance migrations land as a separate commit
  after orchestrator synthesis.
- **Each subagent produces ONE triage report** with rows: report
  path · current substance status (LANDED/IN-FLIGHT/STALE) ·
  recommended action (DROP/FORWARD/MIGRATE/KEEP) · target home
  if MIGRATE · reason.
- **Verify before recommending DROP.** Per `skills/context-
  maintenance.md` §"Anti-patterns": don't retire a report whose
  substance hasn't migrated. Each DROP recommendation cites the
  permanent home (ARCH file + section, skill file + section,
  code path + line) where the substance now lives.
- **Apply the design-rationale guard** per §"§3a" — a report
  enumerating competing alternatives is load-bearing as
  rationale; KEEP with a STATUS-BANNER rather than DROP.
- **Aggressive consolidation per spirit 362** when the substance
  has cleanly migrated; conservative per spirit 311 when
  substance is partially absorbed.
- **No emojis.** No `---` horizontal-rule lines. File:line
  citations on every substance-migration claim. Mermaid label
  discipline per `skills/mermaid.md` §"Label sizing" if any
  diagrams.
- **jj headless ONLY** if commits land (the sweep is read-only
  for the subagents; orchestrator handles any commits):
  `jj describe -m '<msg>'`.

## §4 What the overview (file 4) integrates

After A/B/C return:

1. **Triage decision table** — every report listed in §2.2/§2.3/
   §2.4 with its agreed action.
2. **Migration list** — substance that lands in permanent docs
   (ARCH, skills) as part of this sweep.
3. **Retirement list** — reports to delete this commit.
4. **What carries forward** — designer-lane state after the
   sweep + handover summary for second-designer's `/319`
   forward design.
5. **Open psyche questions** — any surfaced by the triage.

## §5 Scope boundary — what this sweep does NOT do

- Does NOT touch second-designer's `/319` forward design (that's
  their lane).
- Does NOT design the schema component itself (spirit 397-400
  are captured; second-designer absorbs into their design).
- Does NOT touch reports outside `reports/designer/` (operator/
  second-designer/poet/system-specialist lanes own theirs).
- Does NOT migrate substance to permanent docs in this same
  commit — the sweep is triage; migrations land separately if
  the substance is settled enough.
- Does NOT alter `pi-api-surface-notes.md`'s non-numbered status;
  Subagent C judges drop/keep/migrate without forcing a
  numbering retrofit.

## §6 The five-fact context for every subagent

When triaging schema-stack-relevant substance, the current
direction is:

1. **Short header** (spirit 388) — 64-bit, 8 enums (1 root + 7
   sub), discriminators only, no version field.
2. **Sema short header** (spirit 390) — symmetric to signal-
   side; same machinery, different routing.
3. **NOTA schema language** (spirit 391) — the schema source;
   macros consume structured schema not Rust syntax.
4. **Schema component** (spirit 397-400) — runtime registry +
   library + macro substrate; three faces; library may be
   separate repo.
5. **MVP scope** (spirit 392) — even-byte 7-sub-enum split;
   sub-byte packing deferred to post-MVP.

Any older report's substance is triaged against this current
target. If the substance is consistent → MIGRATE to ARCH or
DROP if already there. If superseded → DROP after verifying the
new direction holds. If competing-alternative rationale → KEEP
with STATUS-BANNER per the design-rationale guard.
