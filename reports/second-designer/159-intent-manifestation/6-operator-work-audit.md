*Kind: Audit follow-on · Topic: recent operator commits without reports · Date: 2026-05-23*

# 6 — Operator work audit + recent commits absorption

## What this slice is

Follow-on to designer `/302` (audit of recent operator work, 2026-05-23).
`/302` flagged that today's three structural commits landed WITHOUT
matching operator reports:

- `persona` `srrkotlpouuk` (supervise spirit per engine; 320 LOC across 13 files)
- `persona-spirit` `qruqpolrqzzz` (accept daemon configuration files; 39 LOC across 2 files)
- `persona-orchestrate` `mkwpzsnmvrsr` (record partial application divergence; 183 LOC across 8 files; new `src/divergence.rs`)

This sub-report inspects each commit's substance via `jj diff`, identifies
specific gaps in (a) constraint tests, (b) end-to-end sandbox coverage,
(c) ARCH file alignment, (d) bead tracking, and files beads where the
gap is real. Quality over quantity — 4 beads total, not 10.

## Per-commit findings

### persona `srrkotlpouuk` — supervise spirit per engine (320 LOC)

Substance: extends the `EngineSupervisor` actor + `DirectProcessLauncher`
to scope a `persona-spirit-daemon` instance per engine alongside mind /
router / harness / terminal / message / introspect. Adds an internal
`spirit_daemon_configuration` module to `src/direct_process.rs` (44 LOC of
typed Nota records: `DaemonConfiguration`, `SocketPath`, `StorePath`,
`BootstrapPolicyPath`, `SocketMode`), then a `write_spirit_daemon_configuration_file`
function (~45 LOC) that emits a per-instance NOTA configuration file with
ordinary + owner + upgrade + engine-management socket paths and per-engine
state path. The Nix-built prototype topology test now witnesses 8 components
instead of 7 (peer_count=7) including `spirit`.

What's solid:
- Real constraint test landed: `constraint_engine_supervisor_scopes_spirit_per_engine`
  (tests/supervisor.rs) starts two engines, asserts each gets a distinct
  process, distinct `state/<engine>/spirit.redb`, distinct
  `run/<engine>/spirit.sock`.
- Nix witness wired: `persona-engine-supervisor-scopes-spirit-per-engine`.
- TESTS.md row added.
- ARCH §1581 (table row) added for the integration witness.
- Closes `primary-1cl1` (spirit-per-engine wiring) — bead is closed
  with substantive closure note.

ARCH gap (minor, NOT bead-worthy): The `persona/ARCHITECTURE.md`
§"Spirit-per-engine" prose (line 273) was not updated to tie the
existing decision back to the `EngineSupervisor` wiring that landed
today. The integration witness row at line 1581 covers the gap
indirectly; the §"Spirit-per-engine" subsection still reads as
pre-implementation prose. Cosmetic but not load-bearing.

Test gap (NOT bead-worthy — covered transitively): the
`spirit_daemon_configuration` module's NOTA shape is verified
end-to-end through the integration test (a real `persona-spirit-daemon`
binary actually consumes the file in the prototype-topology Nix witness).
A separate constraint test that the schema-only matches what
`persona-spirit/src/daemon.rs` accepts would duplicate the integration
witness without adding new architectural truth — the integration test
IS the schema agreement.

Report gap: 320 LOC structural commit, no operator report. See §"Beads
filed" item 4.

### persona-spirit `qruqpolrqzzz` — accept daemon configuration files (39 LOC)

Substance: extends `DaemonRuntime::from_argument` so that the
single-argument daemon binary now treats arguments that don't begin
with `(` as filesystem paths to a NOTA configuration file. Mirrors
the CLI's request-vs-file-path duality (already documented in ARCH
§"Spirit single argument" line 164-165 for the CLI).

What's solid:
- Functional test landed: `persona_spirit_daemon_accepts_configuration_file_path_argument`
  (tests/daemon.rs) — writes a configuration file, runs the daemon
  parser, asserts `DaemonRuntime::from_argument` loads it.
- Small commit, commit-as-report is acceptable per `/302` Weakness 2.

ARCH gap (bead-worthy): `persona-spirit/ARCHITECTURE.md` documents
the CLI dual-argument shape (line 164-165, line 185) but says NOTHING
about the daemon binary now accepting the same path-or-record shape.
The daemon side is invisible in ARCH. This matters because the
daemon's argument contract is a load-bearing protocol surface — the
spawn launcher in `persona/src/direct_process.rs` depends on it. See
§"Beads filed" item 1.

Test gap: none — the functional witness covers the happy path. A
constraint test that an argument beginning with `(` is parsed as a
record and everything else is parsed as a path could be added but
would only weakly add to existing coverage.

Report gap: 39 LOC, ties to per-engine work above; commit-as-report
is fine per `/302`. Covered by the report-gap bead (item 4) at the
batch level, not individually.

### persona-orchestrate `mkwpzsnmvrsr` — record partial application divergence (183 LOC)

Substance: implements `/294` Design B (record-divergence) for
Mutate-chain partial-failure. New `src/divergence.rs` with
`DivergenceLedger` (18 LOC). `src/tables.rs` adds `StoredDivergence`
table + slot allocator (parallel to `StoredActivity` pattern), bumps
`ORCHESTRATE_SCHEMA_VERSION` from 1 to 2. `src/service.rs` adds
`record_partial_application` and `divergences` methods.
`src/execution.rs` maps both `OrchestrateReply::PartialApplied` and
`OwnerOrchestrateReply::PartialApplied` to `SemaOutcome::Mutated`.
ARCH §195 (tables) gains a `divergences` row marked implemented;
§257 gains a behavior bullet describing the fanned-out Mutate rule.

What's solid:
- Functional test landed:
  `partial_downstream_failure_records_divergence_and_returns_typed_reply`
  (tests/ledger.rs) — directly invokes `service.record_partial_application`
  with a hand-built `PartialApplied`, asserts the typed reply and the
  stored divergence.
- ARCH update is substantive (table row + behavior bullet + module-tree
  line + test-witness line).
- Closes `primary-ktkc` (Gap 11) — bead is closed with substantive
  closure note.
- Schema version bumped; `OrchestrateTables::open` ensures the new
  tables.

Test gap 1 (bead-worthy): **schema upgrade is uncovered**. Schema
version bumped 1→2 without a constraint test that an existing v1
store opens cleanly at v2 with old rows preserved. See §"Beads
filed" item 2.

Test gap 2 (bead-worthy): **end-to-end fan-out is uncovered**. The
functional test directly invokes `record_partial_application` with a
hand-built `PartialApplied` value; nothing witnesses the choreography
that PRODUCES a `PartialApplied` (the actual fan-out across two real
downstream targets, one succeeding and one failing, with the aggregated
reply flowing back to a mind-shaped caller). The unit-level witness
tests the SINK; the integration witness tests the SOURCE. See
§"Beads filed" item 3.

Report gap: 183 LOC structural commit, no operator report. Covered
by the report-gap bead (item 4) at the batch level.

## Beads filed

1. **`primary-0gtj` (P2)** — `[ARCH alignment] persona-spirit ARCH does
   not document the daemon accepting a configuration file path`. The
   CLI section documents `(`-prefix vs file-path dual argument; the
   daemon side that landed in `qruqpolrqzzz` has no parallel rule in
   ARCH. Add the parallel rule + test-witness row referencing
   `persona_spirit_daemon_accepts_configuration_file_path_argument`.

2. **`primary-7mb1` (P2)** — `[Constraint test] persona-orchestrate v1
   to v2 schema upgrade preserves existing rows and admits divergence
   writes`. Schema version bumped 1→2 in `mkwpzsnmvrsr` without a
   constraint test that an existing v1 store opens cleanly at v2 with
   old rows preserved. Risk: future schema bumps will silently break
   compatibility.

3. **`primary-6u69` (P2)** — `[End-to-end] persona-orchestrate Mutate
   fan-out produces PartialApplied + divergence record when one
   downstream leg fails`. Functional test covers the SINK
   (`service.record_partial_application` directly invoked); no
   integration witnesses the SOURCE (a real Mutate fanning out across
   two stubbed downstream targets with one failing). Natural witness
   for `/294` Design B and `primary-ktkc`'s closure.

4. **`primary-e2bc` (P2)** — `[Operator report-gap] Three 2026-05-23
   structural commits (persona srrkotlpouuk, persona-spirit qruqpolrqzzz,
   persona-orchestrate mkwpzsnmvrsr) landed without matching operator
   reports`. Per intent 232 (every chat response paraphrases a report)
   the bead closure notes are insufficient trace for future agents
   reading `reports/operator/` without a bead search. Bead lists what
   the missing reports should contain (closing bead UID inline,
   intent records, Nix witness, the why).

## How it fits with /302

`/302` is the primary audit — it walks the full operator slice
(reports/operator/157–163 plus today's commits) and surfaces eight
strengths + eight weaknesses, with global-shape recommendations
(decompose epics, pause uses of `EngineId` while rename queued, etc).

This sub-report (`6-operator-work-audit.md`) is a follow-on that turns
the specific `/302` observations on the three unreported commits into
beads where the gap is concrete and bead-shaped. `/302` says
"trace evidence is missing"; this sub-report files `primary-e2bc` as
the trace-evidence remediation. `/302` says "no operator reports for
three structural commits"; this sub-report inspects each via `jj diff`
and identifies the constraint/integration/ARCH gaps that would have
been visible in those reports.

The 4 beads filed are operator-shaped follow-ons. They do not duplicate
`/302`'s broader recommendations (rename pass, decompose epics, Spirit
v0.1.0 retrofit decision) — those remain `/302`'s territory.

## Open follow-ons

- **persona ARCH §"Spirit-per-engine" prose refresh** — minor and
  cosmetic, not bead-filed. Could be a one-paragraph operator edit
  next time the section is touched: tie the existing decision
  (per-engine spirit) back to the `EngineSupervisor` wiring that now
  realises it. Mention here for designer pickup if someone is
  already in `persona/ARCHITECTURE.md` for another reason.
- **`signal_persona_orchestrate::ApplicationFailureReason` enumeration**
  — the new `PartialApplied` shape carries `ApplicationFailureReason`
  but the enumeration of reasons (other than `Unreachable` used in the
  test) was not surveyed in this audit. If the enumeration is
  open-ended and grows per Mutate kind, that's a future design touchpoint
  worth flagging — but it's the contract crate's concern, not these
  three commits'.
- **Schema-bump discipline as a generic skill** — `primary-7mb1`
  targets persona-orchestrate specifically, but the underlying
  pattern (sema-backed schema-version bumps need migration witnesses)
  is a workspace-wide concern. If multiple components hit the same
  gap, a `skills/sema-schema-migration.md` skill file may be warranted.
  Not bead-filed; flagged for the orchestrating designer.

## See also

- `reports/designer/302-audit-recent-operator-work-2026-05-23.md` — the
  primary audit this sub-report follows on from.
- `reports/second-designer/162-contract-repo-lens-and-consolidation/4b-consolidated-current-status.md`
  §2-§4 — the constraint-test + integration-test bead pattern this
  audit continues (consolidates the former `/157` §3-§4 + §9).
- `reports/designer/294-most-important-gaps-visual.md` Gap 11 +
  `reports/designer/293-designer-and-research-batch-2026-05-23/5-gap-closure-step-1-2.md`
  §2 Gap 11 — the design context for `primary-ktkc` + `primary-6u69`.
- `reports/second-designer/159-intent-manifestation/0-frame-and-method.md`
  — frame for this meta-report directory.
- Spirit records 260 (spirit-per-engine pattern), and `/249` Gap 11 +
  Gap 19 — the intent context for the three commits.
