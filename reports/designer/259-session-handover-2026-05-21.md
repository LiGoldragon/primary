# 259 — Session handover (2026-05-21)

*Designer-side context handover. Sweep retired 17 stale reports;
10 load-bearing remain. The substrate-replacement work is on
track; spirit triad is post-migration in excellent shape;
engine-manager triad is the next-slice target.*

## What this is

A designer-lane context-maintenance pass per
`skills/context-maintenance.md`. Drops 17 reports whose substance
has been absorbed into code, skills, intent records, or successor
reports. The 10 reports kept below are the load-bearing designer
surface.

## Reports remaining (designer-side)

| Report | Role |
|---|---|
| `/214` criome-architecture-record | Foundational criome architecture |
| `/234` concept-designer-role | Open role definition (INTENT.md cites) |
| `/238` signal-architecture-redirection-contract-local-verbs | Foundational direction; migration ongoing |
| `/246-v4` bundled-fix-deep-design-with-examples | Canonical three-layer spec |
| `/248` three-layer-changes-for-operators | Operator change list; engine-manager pending |
| `/249` component-intent-gap-analysis | 35-gap inventory; several still open |
| `/252` engine-management-rename | Implementation plan; **not executed yet** |
| `/256` signal-spirit-post-fix-audit | Spirit triad audit; §3.2 atomicity open |
| `/257` signal-contracts-names-and-shape-audit | Workspace-wide migration master |
| `/258` persona-signal-triad-audit | Engine-manager triad findings |
| `/259` this handover | Until absorbed by next session |

Older designer reports retired this pass: /232, /233, /235–/237,
/239–/245, /247, /251, /253–/255. Substance preserved in code,
skills, intent records, or successor designer reports.

## What's landed since /256 (spirit triad)

Major progress in the last day. Spirit's substrate-replacement
work is mostly in:

- **Two-field timestamps** (`Date`, `Time` records on
  `RecordProvenance`, agent-submitted Entry has no timestamp, daemon
  stamps via new `ClockPlane` actor). Closes /256 §3.1, the
  critical gap.
- **Bead `primary-77hh` (drop channel-name prefix) LANDED** —
  signal-frame commit `653773b`. Macro emits clean unprefixed names
  (`Frame`, `Operation`, `Reply`, etc.). Spirit's `pub type Frame =
  SpiritFrame;` alias block gone. `OperationKind` macro-generated.
  Plus bonus: `add generated cli route table` feature (`0b5b3ef`)
  in signal-frame.
- **Bead `primary-k3bu` (UnknownKindForVerb rename) LANDED** in
  signal-frame (`b375e20`). Some consumers still need to pick this
  up; spirit triad is current.
- **Owner contract cleanup**: redundant `operation` field dropped
  from owner-signal-persona-spirit's `RequestUnimplemented`
  (`ec0f4d9`).
- **CLI generated dispatch**: spirit's CLI now routes through
  `SpiritCommandLineDispatch` (macro-emitted), shrinking
  hand-written translation.
- **Last-effect convention documented**: /256 §3.3 closed with an
  inline comment in `SpiritLowering::reply_from_effects` naming
  the workspace convention (pipeline-order canonical).

## What's open

### Spirit triad

- **/256 §3.2 atomicity** — `execute_atomic_batch` still rejects
  multi-op batches AND for size-1 calls commands sequentially
  without transaction boundary. Today moot (every operation
  lowers to one command); the trait's "atomic" name is
  structurally unenforced. Either wrap in a redb write
  transaction at the `CommandExecutor` boundary OR document
  spirit's impl as degenerate-atomic.
- **/256 §3.4 observer fanout** — `SpiritObserverRecorder` still
  trace-only placeholder. Per `intent/persona.nota`
  2026-05-20T20:00:00Z this is deferred until persona-introspect
  comes online. Not a current blocker.
- **Spirit-internal `Spirit*`-prefixed types**
  (`SpiritClient`, `SpiritFrameCodec`, etc.) per /256 §"Smaller
  new smells". Inside `persona-spirit` crate, the prefix is
  ancestry. Workable as-is; cleaner with `ordinary` / `owner`
  modules.

### Engine-manager triad (per /258)

- **/252 engine-management rename not executed.** signal-persona
  still has 24+ `Supervision*` references; persona daemon has
  `src/supervisor.rs`, `EngineSupervisor` actor,
  `supervision_readiness.rs`, etc. Mechanical pass; /252 has the
  details.
- **persona daemon does not use signal-executor.** Same gap that
  /255 found for spirit pre-migration. Worth a bead (modeled on
  spirit's migration template).
- **No observable block** on either signal-persona channel —
  per the 2026-05-21T10:00:00Z "debug the debugger" Decision,
  the engine manager (the apex persona component) should be
  Tappable. /258 §2.3 details.
- **Inconsistent module placement**: Engine channel at crate top
  level, Supervision channel in `pub mod supervision`. Both
  should be in modules per the modules-not-options principle.
- **`GracefulStopAcknowledgement`** ancestry word — drop the
  redundant prefix.
- **`SpawnEnvelope` stale supervision_socket_* fields** — cascade
  of the /252 rename.

### Workspace-wide migration (per /257)

- **10 contracts still on `signal-core`** + universal-verb shape
  (mind, router, message, introspect, system, terminal, harness,
  owner-terminal, criome, owner-ledger). The /257 §3.4
  migration order is the operator roadmap.
- **Bead `primary-u0lh`** (extend nota-codec derive coverage;
  migrate ~13 hand-written codec impls) — pending P2.
- **Mind channel-choreography split** (Grant/Extend/Revoke/List/Deny
  per `intent/persona.nota` 2026-05-19T20:30:00Z) — verb set
  proposed but not yet psyche-affirmed; needs Q5 below.

## Open psyche calls

Three from /257 §4 still pending — psyche skipped these in the
recent exchange. Not blockers; flagging for next-session pickup:

- **Q1**: Single-field timestamps in runtime/protocol contexts
  (vs the two-field rule for intent records). Concrete:
  `TimestampNanos(u64)` in signal-persona for `component_started_at`
  / `drain_completed_at`; `TimestampNanoseconds(u64)` in
  owner-signal-persona-router for `ChannelDuration::TimeBound`.
  Two questions: shape (single field vs two like intent records)
  and precision (ns vs seconds). Designer lean: single-field OK
  for protocol; drop ns → seconds.
- **Q4**: `ChannelMessageKind` 12-variant closed enum (in
  owner-signal-persona-router) — agent-cultivated per /249 gap
  #22. Closed-enum vs data-token (string)? Roles are data; should
  ChannelMessageKind follow?
- **Q5**: Mind channel-choreography verb set — Grant / Extend /
  Revoke / List / Deny were "TBD" in your 2026-05-19T20:30:00Z
  Decision. Lock the names before mind migrates.

## Side notes worth keeping

- **note**: Bead `primary-77hh` shipped + extra (auto-`OperationKind`,
  cli route table). The macro shipping was bigger than the bead
  scope — operator extended on their own initiative; good
  judgment.
- **note**: The /258 audit was a misfire on my part — psyche
  meant the persona-spirit triad (the actual pilot), I read
  "persona-signal triad" as the engine-manager. Substance is
  still valuable (engine-manager IS the next slice); kept the
  report for that.
- **possibly useful**: Bead candidate "Migrate persona daemon
  onto signal-executor" — structurally identical to spirit's
  /255 → /786ab311 migration. Mechanical template:
  `EngineLowering` / `EngineCommandExecutor` /
  `BatchErrorClassification for EngineError`. Could be filed when
  the /252 rename clears the surface.
- **note**: `intent/component-shape.nota` 2026-05-21T10:30:00Z
  (modules-not-options for macro disambiguation) has already
  paid off — the `WorkingReply`/`WorkingOperation` import aliases
  in spirit handle the ordinary-vs-owner Reply collision cleanly.

## How to pick this up

A fresh designer agent landing in the next session:

1. Read `ESSENCE.md` → `INTENT.md` → `AGENTS.md` →
   `skills/skills.nota`.
2. Read `/256` for spirit triad current state and open items.
3. Read `/257` for the workspace-wide migration master.
4. Read `/258` for the engine-manager triad findings.
5. Read `/252` for the engine-management rename implementation.
6. Check the three open psyche calls above; ask if next-session
   work intersects them.

The next concrete pickup point is either (a) /252 execution
(engine-management rename — mechanical), or (b) filing the
persona-daemon-onto-signal-executor migration bead, or (c) taking
one of Q1/Q4/Q5 with psyche to settle the open verb set / shape
question.

## References

- Bead `primary-77hh` LANDED (drop channel-name prefix).
- Bead `primary-k3bu` LANDED in signal-frame (UnknownKindForVerb).
- Bead `primary-u0lh` pending (extend nota-codec derive coverage).
- `intent/persona.nota` recent records (2026-05-20 + 2026-05-21).
- `intent/workspace.nota` recent records (intent-mining discipline).
- `intent/component-shape.nota` recent records (three-layer
  affirmation, no-op-as-command, EffectEmitted naming,
  modules-not-options, BatchErrorClassification).
- `ESSENCE.md` §"Inferring intent is forbidden" (added this
  session).

This handover retires when the engine-manager triad migration
lands AND the three open psyche calls settle, OR when a successor
handover supersedes.
