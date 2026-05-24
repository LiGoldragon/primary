*Kind: Synthesis · Topic: schema-stack-context-maintenance-sweep · Date: 2026-05-24*

# 319 / 4 — Overview + retirement list (orchestrator synthesis)

Integrates the three sibling triage reports:

- `./1-schema-stack-substance-triage.md` (Subagent A — 12 reports;
  1 DROP / 11 KEEP across three sub-categories)
- `./2-working-artifacts-triage.md` (Subagent B — 13 reports;
  11 DROP / 2 KEEP)
- `./3-separate-concerns-triage.md` (Subagent C — 14 entries;
  6 DROP / 7 KEEP / 1 MIGRATE-then-DROP)

## §1 Tally

39 reports/directories inventoried. **19 retire** this commit; **20
stay** load-bearing.

| Slice | DROP | KEEP | Other | Total |
|---|---|---|---|---|
| A (schema-stack) | 1 | 11 | — | 12 |
| B (working artifacts) | 11 | 2 | — | 13 |
| C (separate concerns) | 6 | 7 | 1 migrate-then-drop | 14 |
| **Total** | **18 + 1** | **20** | | **39** |

50/50 split between retire and stay. The KEEP majority reflects
two patterns: (i) the schema-stack target (spirit 388-400) is
still unabsorbed — second-designer's forward design IS the
absorption work, so substrate reports stay live until that lands;
(ii) several reports carry design-rationale-guard substance per
`skills/context-maintenance.md §3a`.

## §2 Retirement list — 19 entries to delete this commit

| Path | Slice | Successor home |
|---|---|---|
| `reports/designer/297-design-signal-persona-auth-rename.md` | B | `primary-fka1.1` CLOSED + `signal-persona-origin` repo |
| `reports/designer/298-design-help-operations-in-components.md` | B | Superseded by `/312` + `skills/component-triad.md` §"Help operations" |
| `reports/designer/300-design-cli-macro-caller-context-injection.md` | B | Superseded by `/301` + `signal-frame/src/caller.rs` (primary-915w CLOSED) |
| `reports/designer/302-audit-recent-operator-work-2026-05-23.md` | B | Rename slippage closed by `primary-fka1`; remaining recs absorbed by operator/167-169 |
| `reports/designer/303-intent-manifestation-sweep-2026-05-23.md` | B | 7 manifestations landed in `skills/designer.md`, `skills/beads.md`, `skills/component-triad.md`, `signal-persona-origin/ARCHITECTURE.md` |
| `reports/designer/304-unimplemented-intent-audit-2026-05-23.md` | B | Beads filed (`primary-8r1j`, `primary-ft29`); auditor design absorbed into `AGENTS.md` |
| `reports/designer/306-manifestation-sweep-round-2-2026-05-23.md` | B | 6 ARCH/INTENT edits landed; 4 beads filed |
| `reports/designer/310-meta-overhaul-booking-roadmap.md` | B | Wave 1/2 → `primary-ezqx`; Wave 3 → `primary-gvgj`; Wave 5 → `primary-fka1`/`primary-0m1u` |
| `reports/designer/311-context-maintenance-sweep-2026-05-23.md` | B | Outputs ARE the deletions (commit tree per spirit 370) |
| `reports/designer/313-great-summary-and-handover-2026-05-24.md` | B | Forward targets in `/317` + `/318` + operator/167-169 |
| `reports/designer/314-aggressive-consolidation-sweep-2026-05-24.md` | B | Created `/315` + `/316`; 10 reports deleted (commit tree) |
| `reports/designer/305-nota-user-guide-and-codec-architecture/` (4 files: 0/1/2/3) | A | Migrated to `nota/README.md`, `nota-codec/README.md`, `nota-codec/ARCHITECTURE.md`, `skills/nota-design.md`, `skills/nota-schema-docs.md` |
| `reports/designer/268-persona-pi-operator-input.md` | C | Superseded by `/309 §10 bead 6` |
| `reports/designer/282-workspace-implementation-status.md` | C | Snapshot superseded by `/293/5` + `/313` (the latter also dropping) |
| `reports/designer/291-persona-systemd-units-for-daemon-management.md` | C | Migrated to `persona/ARCHITECTURE.md:543-561, 694-702, 1275-1390` |
| `reports/designer/292-designer-lane-top-issues-2026-05-22.md` | C | Three issues all addressed |
| `reports/designer/294-most-important-gaps-visual.md` | C | Chosen designs absorbed into `/293/5 §3` |
| `reports/designer/pi-api-surface-notes.md` | C | Superseded by `/281` and `/309 §5` |
| `reports/designer/264-designing-protocol-and-role-spaces.md` | C | Settled §1+§2 in `AGENTS.md:205-213` + `skills/role-lanes.md`; speculative §3-§6 in spirit records 38/39/40/125/134 |

**19 retirements** (12 individual files + 1 directory containing
4 files + 6 individual files = 19 distinct deletions).

## §3 KEEPs — 20 entries that stay, with their reasons

### §3.1 Schema-stack reports (Subagent A — 11 stays)

Four "KEEP with STATUS-BANNER candidate":
- `/285` (versionprojection-trait + handover-protocol-specification) — canonical spec, substance landed but rationale guard
- `/287` (version-handover-component-explained) — canonical visual, landed
- `/305-v2` (64bit signal per-component namespacing) — landed in `signal-frame/ARCHITECTURE.md §5.2` but report cited by path
- `/315` (sema-upgrade and handover current state) — protection-banner role for `/285` + `/287` + open `§2.4`

Four "KEEP with design-rationale guard":
- `/263` (schema-specification-language-design) — schema-language alternatives; foundation for spirit 391 + 397-400
- `/279` (nota-schema-language-and-version-hash) — same foundation
- `/307` (golden-ratio namespace split) — cutoff alternatives
- `/308` (pre-typed envelope + tap-anywhere) — envelope-shape alternatives

Three "KEEP — substance unmigrated":
- `/312` (recursive Help on every enum) — recursive form has no permanent home yet; `skills/component-triad.md:377-399` still teaches the older flat `(Help Main)` form from `/298`
- `/317` (sema-upgrade + macro convergence audit) — active 11-slot macro convergence picture
- `/318` (upgrade merger + persona-prefix rename) — active rename + merger execution per operator/169

### §3.2 Working artifacts (Subagent B — 2 stays)

- `/299` (origin process + agent identity) — design-rationale-guard; three Options for agent-identity (pid-tagging / NOTA self-id / long-lived socket) still load-bearing
- `/301` (elegant `signal_cli!` macro) — KEEP pending two specific landings: (a) `primary-uq04.*` per-component CLI sweep closes; (b) Trust-gradient ARCH section in `signal-persona-origin/ARCHITECTURE.md` composing `Caller` into `IngressContext`

### §3.3 Separate concerns (Subagent C — 7 stays)

- `/249` (component-intent-gap-analysis) — IN-FLIGHT driving `primary-c2da`
- `/257` (signal-contracts-names-and-shape-audit) — IN-FLIGHT driving `primary-u8vo`
- `/266` (persona-pi-triad-design) — design-rationale-guard; STATUS-BANNER for `/309 §7` supersession
- `/281` (headless-pi-research) — design-rationale-guard + still cited by `/309 §10 bead 6`
- `/293` (designer-and-research-batch directory) — meta-report session unit per spirit 231
- `/309` (agent component abstraction) — design-rationale-guard; STATUS-BANNER for `/318` rename open question
- `/316` (forge family) — IN-FLIGHT; `primary-yp6k` not landed

## §4 STATUS-BANNERs to add — five reports

Per `skills/context-maintenance.md §3a` the design-rationale-guard
KEEPs get a one-line STATUS-BANNER naming the supersession. The
banner makes the report findable as "old shape; current shape lives
at X" without dropping the rationale substance.

| Report | Banner content |
|---|---|
| `/266-persona-pi-triad-design.md` | "**Status:** superseded by `/309 §7` for pi-triad shape; this report preserves the alternatives that informed the choice." |
| `/285-versionprojection-trait-and-handover-protocol-specification.md` | "**Status:** trait + types landed in `version-projection/ARCHITECTURE.md`; handover protocol landed in `signal-upgrade/ARCHITECTURE.md` per `/318` Wave-4. This report preserves the protocol-design alternatives." |
| `/287-version-handover-component-explained.md` | "**Status:** absorbed into the upgrade triad per `/318` Wave-4; `upgrade` daemon + `signal-upgrade` + `owner-signal-upgrade` are on disk. This report preserves the visual reference shape." |
| `/305-v2-design-64bit-signal-per-component-namespacing.md` | "**Status:** per-component namespacing landed in `signal-frame/ARCHITECTURE.md §5.2`; this report preserves the per-component-vs-workspace-wide rationale." |
| `/309-design-agent-component-abstraction.md` | "**Status:** triad shape absorbed into `primary-gvgj` epic (10 sub-beads tracked). Rename open question — `/318` recommends dropping persona- prefix to `agent`/`signal-agent`/`owner-signal-agent` per spirit 371; this report's §1 KEEP-prefix framing is superseded once psyche ratifies." |

## §5 Open psyche questions surfaced by the sweep

Three substantive questions where the sweep can't proceed without
direction:

### §5.1 Persona-agent rename ratification (still open)

The conflict `/309 §1` (KEEP prefix) vs `/318/1 §8.4` (DROP prefix)
is a real document-level disagreement. Subagent C explicitly
flagged it. The lean is **DROP per spirit 371 + the rule applies
uniformly across architectural-pattern components**. The lean has
been my chat-asked sharpener for ~5 turns; no explicit answer yet.
Confirming closes both: enables `/318`-track to land R10 in
operator beads cleanly + retires `/309 §1`'s framing as
superseded + the STATUS-BANNER on `/309` becomes definite.

### §5.2 Trust-gradient ARCH composition (named by `/301`, absent today)

Per Subagent B's finding: `signal-persona-origin/ARCHITECTURE.md`
does NOT yet carry the Trust-gradient `Caller → IngressContext`
composition that `/301` named. The substance is in `/301`; the
permanent home would be `signal-persona-origin/ARCHITECTURE.md`
(or `signal-agent/ARCHITECTURE.md` after R10 lands). Worth filing
a bead OR migrating directly.

### §5.3 `/264 §3-§6` speculative substance — possible-future-design?

Subagent C surfaced this. `/264`'s settled parts migrated to
`AGENTS.md` + `skills/role-lanes.md`; the speculative §3-§6 lives
in spirit records 38/39/40/125/134 but no permanent doc captures
the direction. Per `skills/architecture-editor.md` §"Carrying
uncertainty" the right home would be a "Possible features" entry
somewhere — but it's protocol-and-role-spaces work that doesn't
have an obvious ARCH file. Hold until the relevant work surfaces?

## §6 What designer-lane carries forward

After this commit lands:

- **Schema-stack substrate** for second-designer's forward design
  — `/263`, `/279`, `/307`, `/308`, `/312` all carry alternatives
  + chosen-shape rationale that the forward design absorbs.
- **Canonical specs** preserved with STATUS-BANNERs — `/285`,
  `/287`, `/305-v2`, `/315` keep their referenceable-by-path role.
- **Active meta-reports** — `/317` (macro convergence audit),
  `/318` (rename + merger execution) — both currently load-bearing.
- **In-flight epic-substrate** — `/249` (gap analysis driving
  `primary-c2da`), `/257` (contracts-names audit driving
  `primary-u8vo`), `/316` (forge family awaiting `primary-yp6k`).
- **Agent-identity rationale** — `/299` (3 Options open).
- **CLI-macro pending-landing** — `/301` (awaiting `primary-uq04.*`
  closure + trust-gradient ARCH).
- **Design-rationale-guards** — `/266`, `/281`, `/309` with their
  STATUS-BANNERs naming the chosen homes.

**Designer surface contracts from 39 reports → 20 reports + 2
meta-dirs.** Halves the surface; the half that stays is uniformly
load-bearing (no junk).

## §7 What this sweep does NOT do

- **Does NOT write second-designer's forward `/319` design.**
  Their lane owns the schema-stack forward picture.
- **Does NOT migrate substance in this commit** — only triage +
  STATUS-BANNERs + deletions. Substance migrations (e.g., Trust-
  gradient ARCH section per `§5.2`) land separately when picked up.
- **Does NOT address the persona-agent prefix Decision** — that's
  on psyche per `§5.1`.
- **Does NOT touch reports outside `reports/designer/`** —
  operator/167-169, second-designer reports, etc. stay in their
  lanes.
- **Does NOT retroactively renumber** — gaps in the designer
  sequence after deletions are visible signals per
  `skills/reporting.md`.

## See also

- `./0-frame-and-method.md` — orchestrator frame
- `./1-schema-stack-substance-triage.md` — Subagent A
- `./2-working-artifacts-triage.md` — Subagent B
- `./3-separate-concerns-triage.md` — Subagent C
- `skills/context-maintenance.md` — the discipline this sweep
  applies (forward / migrate / keep / drop + design-rationale
  guard + commit-tree archive)
- `skills/reporting.md` §"Hygiene" + §"Deleted reports live in
  the commit tree" — supersession + retrieval via `jj show`
- Spirit records 362 (aggressive consolidation when psyche
  directs), 370 (deleted reports live in commit tree), 388-400
  (schema-stack target this sweep consolidates toward)
- `reports/operator/167-recent-reports-and-intent-refresh-2026-05-24.md`
  and `/168` and `/169` — operator's parallel current-state
  checks that confirm bead state for the migration-citations
