# Schema Thread Context Maintenance

*Kind: context maintenance · Topics: schema-stack, spirit-next, log-socket, stale-reports, implementation-queue · 2026-06-01 · operator lane*

## Frame

This pass refreshes the schema/asschema/NOTA/spirit-next thread after Spirit
records 1339-1353 and recent operator/designer reports. It answers four
questions:

- What is current truth?
- Which reports are stale or safely superseded?
- What should fold into architecture/intent rather than remain report-only?
- What is the immediate implementation queue?

Sources read: Spirit records 1339-1353; operator reports 271, 272, 273, 274;
designer reports 443-459 with emphasis on 453-459; live repo state in
`spirit-next`, `schema-rust-next`, and `schema-next`.

## Current Truth

### spirit-next

Current `main` is `d29dc6ca` (`spirit-next: keep only schema triad runtime
path`). It is ahead of the state described by some reports.

Live facts:

- `Mail<Phase>`, `NexusMail`, `BeingProcessed`, `Processed`, and
  `Nexus::process<Payload>` are gone from source.
- `SignalActor::admit` is the single admission method; the old `route` +
  `accept` split is gone.
- `NexusEngine::execute(&mut self, nexus::Nexus<nexus::Input>)` is the only
  Nexus runtime decision entry.
- SEMA roots are split: `SemaWriteInput`/`SemaWriteOutput` and
  `SemaReadInput`/`SemaReadOutput`.
- `Store` implements both `SemaEngine::apply` for writes and
  `SemaEngine::observe` for reads.
- `runtime_triad.rs` contains typed witnesses for Signal, Nexus, SEMA write,
  SEMA read, durability, route preservation, rejection before SEMA, and
  parallel read shape.
- The daemon still starts from a binary rkyv `Configuration` file and the
  ordinary socket still uses binary Signal frames, not NOTA.

### schema-rust-next

Current `main` is `06a7797c` (`schema-rust: remove legacy single sema
surface`).

Live facts:

- The emitter has the split SEMA trait surface:
  `apply(&mut self, sema::Sema<sema::WriteInput>)` and
  `observe(&self, sema::Sema<sema::ReadInput>)`.
- The old single SEMA surface is retired.
- The generated `NexusMail<Payload>` support is absent and guarded by tests.
- Signal remains a two-method trait (`triage` + `reply`), not the earlier
  proposed single `execute` method. Designer 455's audit treated this as
  honest engineering.

### schema-next

Current `main` is still carrying the schema macro/asschema substrate. The
context-maintenance additions in this turn did not uncover a new schema-next
blocker for the log-socket slice.

The relevant current truth is stable:

- `Asschema` is typed data, not a text fixture.
- `AsschemaArtifact` owns NOTA/rkyv projection.
- `AsschemaStore` owns redb persistence of assembled schemas.
- Schema lowering consumes NOTA structure and emits `Asschema`; it does not
  own Rust instrumentation behavior.

## Report Status

### Still current

- `reports/operator/274-live-architecture-witness-research-2026-06-01.md`:
  current as a principle report. Its "grep for absence, execute for use" rule
  is now reinforced by Spirit 1343-1350.
- `reports/designer/459-proof-of-usage-witness-research-2026-06-01.md`:
  current and directly applicable. The log socket is the canonical Layer 2
  runtime witness for engine-trait usage per Spirit 1349.
- `reports/designer/458-spirit-triad-naming-gate-decision-2026-06-01.md`:
  still current. It gates the later spirit fold, not the log-socket prototype.
- `reports/designer/446-next-stack-porting-research-2026-06-01/4-overview.md`:
  still current for porting sequence. Phase 0 spirit fold remains the right
  first port after naming is settled.
- `reports/designer/447-upgrade-as-sema-design-2026-06-01.md`:
  still current as design horizon, but not the next implementation slice
  before instrumentation and witness cleanup.

### Superseded by landed code

- `reports/operator/273-spirit-next-b53f4fc2-triad-runtime-audit-2026-06-01.md`
  is now historical. Its findings about `Nexus::process<Payload>`, old
  single SEMA apply shape, and thin remnant surfaces are superseded by
  `spirit-next` main `d29dc6ca`.
- `reports/designer/455-b53f4fc2-design-implementation-fidelity-audit-2026-06-01.md`
  remains valuable as audit history, but its standout gap
  "SEMA parallel reads via apply/observe split" is closed on current
  `spirit-next` and `schema-rust-next` main.
- `reports/designer/456-retire-stale-design-remnants-2026-06-01.md` is
  effectively implemented on current `spirit-next` main. Keep as provenance
  until a later report-retention pass decides whether the branch report can
  retire.
- `reports/designer/457-operator-day-audit-and-bead-sweep-continuation-2026-06-01.md`
  is partially stale: it described the split/remnant work as in-flight. That
  work is now landed on main. Its bead-sweep accounting may still be useful.

### Older horizon reports that remain background, not immediate queue

- `reports/designer/443-design-improvements-audit-2026-05-31/5-overview.md`
  and `reports/designer/444-stack-vision-2026-05-31/5-overview.md` are still
  useful for the broad backlog, but several items have been overtaken by
  later work. Treat them as horizon sources, not as a direct task list.
- `reports/operator/271-context-maintenance-current-state-2026-06-01.md` is
  now superseded in specific details: SEMA split and remnant retirement are
  closed; the current queue should be taken from this report plus Spirit
  1343-1353.

## Architecture/Intent Manifestation Candidates

These are current enough to fold into repo docs if the next operator slice
touches the repos:

- `spirit-next/ARCHITECTURE.md`: add a short "Testing instrumentation" section
  once the log-socket implementation lands. It should state that trace is
  optional, typed, feature-gated, and separate from the normal Signal socket.
- `spirit-next/INTENT.md`: manifest Spirit 1343-1350 after the prototype lands:
  testing builds can emit structured trace events proving Signal/Nexus/SEMA
  trait use; CLI is the log surface; production logging is off.
- `schema-rust-next/ARCHITECTURE.md`: after emitter work lands, document that
  runtime trace support is emitted behind an instrumentation feature and that
  generated trace nouns are schema support nouns, not ad hoc strings.
- `skills/architectural-truth-tests.md`: designer 459's proof-of-usage ladder
  should become skill text eventually. The current log-socket prototype depends
  on the Layer 2 runtime witness concept.

Do not update these docs in advance of implementation. The report is enough
until code exists.

## Immediate Implementation Queue

1. **Prototype runtime trace support** in `schema-rust-next` and `spirit-next`
   per operator report 275. This directly implements Spirit 1343-1350 and
   turns the positive-grep correction into a runtime witness.
2. **Remove or demote positive grep proof checks** in `spirit-next` flake once
   the runtime trace tests exist. Keep negative guards for retired surfaces.
3. **Port the same positive-grep cleanup discipline to `schema-rust-next` and
   `schema-next`** after `spirit-next` has the trace witness model working.
4. **Small cleanup queue from operator 271/designer 445** remains valid:
   `nota-next` parser free function, one-impl delimiter trait, CLI
   `NotaSource::from_cli_argument`, and `SchemaError` Display. These are
   independent but lower strategic priority than the new witness substrate.
5. **Spirit fold remains next major porting work** after the instrumentation
   and witness cleanup, gated by the policy-signal naming decision from
   designer 458.

## Safely Superseded

Safe to stop using as current implementation targets:

- Any report text that says `spirit-next` still needs the SEMA apply/observe
  split.
- Any report text that says `Mail<Phase>` or `NexusMail` is the current
  compile-time witness for mail being processed.
- Any report text that treats `Nexus::process<Payload>` as an active public
  bypass concern.
- Any task that tries to prove live architecture through positive grep of
  method names or test names.

Still not superseded:

- The Phase 0 `spirit-next` -> `spirit` fold.
- Schema-core extraction as a horizon.
- Generic artifact/store substrate as a horizon.
- Upgrade-as-SEMA as a horizon.
- Owner-signal vs meta-signal naming gate.

## Recommendation

Treat the log-socket instrumentation slice as the next operator proof slice.
It is smaller than the spirit fold, directly responds to the latest maximum
intent, and creates the runtime witness substrate needed to cleanly retire
positive-grep proof checks. After that, run the positive-grep cleanup, then
return to the spirit fold with current docs and witness discipline in place.

