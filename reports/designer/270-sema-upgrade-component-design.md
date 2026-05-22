# 270 — sema-upgrade component design

*The workspace's universal stateful schema-upgrade mechanism for sema
databases. Triad-shaped like every other stateful component. The first
concrete migration is the legacy file-log to spirit translation —
treating `intent/*.nota` as a 0.01 version of the spirit sema database.
This report designs the component shape; the migration mechanics
themselves live in the Approach C selection (intent
`component-shape.nota` record 21) and the schema specification
language (/263).*

## 1. What sema-upgrade is

Every persona daemon stores working and policy state in a sema
database. When its contracts evolve, existing on-disk data and the
new daemon binary must end up in a consistent state. The Approach C
decision (intent `component-shape.nota` record 21) settled the
per-record mechanism — schema-address tags, in-process versioned reads,
migration on read. What that decision left absent is **the
orchestration layer**:
where the daemon consults before serving its first request to decide
whether the stored data is at an address it can still read, whether a
migration plan must execute first, and what to do if it cannot.

That orchestration is `sema-upgrade`. Every persona daemon that needs
to upgrade goes through it. The schema specification language (/263)
is what *describes* the schemas at each end, and the content-addressable
schemas written in it are what sema-upgrade *consumes*. Sema-upgrade
takes the two addresses (deployed and current), the diff classifier's
plan, and runs the actual migration steps.

Sema-upgrade is itself a triad component — daemon, two signal contracts,
thin CLI named `upgrade`. Other persona daemons are its Signal peers,
calling in at boot. The daemon's existence is what gives migrations
durable history, an owner-audited approval flow, and an introspectable
state machine.

## 2. The triad shape

```
sema-upgrade/                          runtime
  src/lib.rs                           component library
  src/bin/sema-upgrade-daemon.rs       long-lived daemon
  src/bin/upgrade.rs                   thin CLI client
  bootstrap-policy.nota                first-start policy declaration
signal-sema-upgrade/                   working contract
  src/lib.rs                           signal_channel! { … }
owner-signal-sema-upgrade/             policy contract
  src/lib.rs                           signal_channel! { … }
```

- The daemon binary is `sema-upgrade-daemon`. Long-lived, owns the
  sema-upgrade sema database, accepts Signal frames on a working
  socket and an owner socket.
- The CLI is `upgrade` (daemon name minus the `-daemon` suffix per the
  workspace CLI naming convention). Thin Signal bridge; two-socket
  dispatch by request head.
- The working contract `signal-sema-upgrade` carries the peer-callable
  surface: daemon-at-boot migration requests, schema-address queries,
  observation taps.
- The policy contract `owner-signal-sema-upgrade` carries the owner-
  only authority: approve migration plans before they run, throttle
  migration throughput, quarantine a daemon if migration repeatedly
  fails, restate the catalogue of trusted schema addresses.

The two contracts ship together — sema-upgrade is born triad-shaped,
not introduced as ordinary-only first.

## 3. Wire surface

Operation and reply names below are designer proposals; final names
settled by psyche during the implementation arc.

### 3a. Working contract — operations

- **Inspect** — daemon at boot sends its component identity and the
  schema-address its binary expects. Reply names whether the daemon
  may proceed, must wait for a plan, or is at an address sema-upgrade
  does not know about.
- **Plan** — given two addresses (stored data's and current),
  sema-upgrade walks the schema diff through the classifier from
  /263 and returns a `MigrationPlan` (zero-cost, append-only,
  and structural steps). The plan is a tree of per-record-type
  leaves under a per-component branch.
- **Migrate** — daemon requests sema-upgrade execute a previously
  emitted plan. Sema-upgrade dispatches per-step transformations;
  the daemon's read-path machinery (Approach C versioned-reads) is
  what actually touches its own records. Sema-upgrade is the
  orchestrator, not the in-process reader.
- **Report** — daemon reports per-step outcomes back as the
  migration runs; sema-upgrade records each into working state.
- **Tap / Untap** — universal observability mandate. Subscribers
  receive `OperationReceived` and `EffectEmitted`.

### 3b. Working contract — replies

- `Inspected ((current SchemaAddress) (stored SchemaAddress)
  (Decision …))` where `Decision` is `Proceed`, `PlanRequired`,
  `UnknownStoredAddress`, or `Quarantined`.
- `Planned (MigrationPlan)` — the typed plan from /263.
- `MigrationAccepted ((MigrationIdentifier) (StepCount u32))`.
- `StepReported ((MigrationIdentifier) (StepIndex u32) (Outcome …))`
  where `Outcome` is `Succeeded`, `Skipped (Reason …)`, or
  `Failed (FailureClassification …)`.
- `MigrationCompleted ((MigrationIdentifier) (FinalAddress
  SchemaAddress))`.
- `MigrationFailed ((MigrationIdentifier) (StepIndex u32)
  (FailureClassification …))`.

### 3c. Owner contract — operations

Policy surfaces (substance in §7): `ApprovePlan`, `RejectPlan`,
`Quarantine`, `Release`, `ConfigureThrottle`, `RegisterSchema`,
`RetractSchema`.

## 4. The first concrete migration — file log to spirit

The pilot is the substrate replacement (intent/persona.nota
2026-05-20T15:00Z and 15:30Z): legacy `intent/<topic>.nota` files
become typed records in the deployed `persona-spirit` sema database.
Treat the legacy file substrate as a 0.01 version of the spirit
sema database; sema-upgrade translates 0.01 to current.

### 4a. Why sema-upgrade and not spirit

The constraint from intent/persona.nota 2026-05-20T15:30Z is hard:
persona-spirit MUST NOT contain import logic for `.nota` files.
Spirit exists for typed psyche-statement records going forward; any
one-time migration tool must call spirit's normal `(Record (Entry
…))` operation through the spirit CLI like any other agent.

Sema-upgrade is the only correct home. Its job is *exactly* this:
read the source state at a prior schema address, walk it through a
plan, write to the destination through the destination daemon's
normal contract operations. The 0.01 substrate happens to be flat
files rather than rkyv-encoded redb rows — a peculiarity absorbed
inside the sema-upgrade plan, never inside spirit.

### 4b. The 0.01 schema

The "0.01" schema is a sema-upgrade-internal description of the
legacy file substrate. It declares: a topic file is a NOTA stream of
branches; each branch is one of five kind variants (Decision,
Principle, Correction, Clarification, Constraint); each branch
carries summary, context, certainty, quote, capture-time leaves as
positional fields in declaration order. The schema-address of 0.01 is
the Blake3 of this declaration encoded in the language from /263. The
0.01 schema is registered via owner-signal `RegisterSchema`.

### 4c. The plan from 0.01 to current

The diff between 0.01 and the current spirit schema yields a
`MigrationPlan` whose steps cover:

- **Walk the file tree** under `intent/*.nota` — every file is one
  topic; every top-level branch is one record. (Source-enumeration
  step type; not present in non-pilot migrations.)
- **Parse each branch into a 0.01 record.** Sema-upgrade carries a
  NOTA reader producing typed records against the 0.01 declaration.
  Legacy-substrate-specific; future rkyv-to-rkyv spirit migrations
  do not need it.
- **Translate `Certainty` to the current `Magnitude` leaf.** The
  Magnitude type design lives in /269; relevant here is that
  sema-upgrade owns the `Certainty(0.01) → Magnitude(current)`
  mapping as a structural-class step. The mapping handles the
  conformant rungs (`Maximum`/`Medium`/`Minimum` pass through) and
  the legacy `High` drift — seven legacy records carry `Certainty
  High` against a closed-world `Certainty` set the daemon rejects.
  Whichever shape Magnitude lands in, the translation lives in the
  plan, not in spirit and not in the file parser.
- **Emit a Record operation against the current spirit daemon.** For
  each translated record, sema-upgrade invokes spirit's working
  contract `Record (Entry …)`. Sema-upgrade does not write into
  spirit's redb; it speaks Signal to spirit's working socket
  (sema-upgrade is a daemon and may be a Signal client of any peer
  daemons per triad carve-out 3). Spirit treats each invocation as
  an ordinary `Assert` from an agent; the import nature is
  invisible to spirit.
- **Record the step outcome** in the sema-upgrade sema database.
  Per-record success / failure / skip is durable; partial
  migrations resume from the last reported step.

The final step writes the new schema-address for spirit's data into
sema-upgrade's component-state branch — spirit is now at current.

### 4d. Why this is also the canonical pilot

Future persona-component migrations follow the same shape with the
file-walking step replaced by a redb-walking step. The orchestration,
plan shape, per-step durability, owner-approval choreography — all
reused. The 0.01 pilot exercises every layer; the source-substrate
adapter (NOTA file reader) is the only per-migration custom piece.

## 5. Composition with Approach C

The Approach C selection (intent record 21) is the *read-side*
mechanism inside each daemon. Sema-upgrade does not replace it; the
two compose. Boot flow with sema-upgrade in the pipeline:

1. Daemon binary starts; reads its NOTA configuration argument.
2. Before opening its sema database for service, the daemon sends
   `Inspect` to sema-upgrade carrying its component identity and the
   schema-address its current binary expects.
3. Sema-upgrade compares against the address it last recorded for
   that component's storage. Three reply branches:
   - `Proceed` — addresses match, no migration. Daemon opens its
     sema database and serves.
   - `PlanRequired` — addresses differ. Daemon halts service
     startup, requests a plan, waits for owner approval and plan
     execution.
   - `UnknownStoredAddress` — sema-upgrade does not know the
     reported address. First-start-of-new-deploy, manual
     intervention, or a deploy that bypassed the upgrade path.
     Sema-upgrade emits a quarantine directive; daemon halts.
4. If a plan ran, the daemon's read path uses the Approach C
   versioned-reads machinery to interpret any per-record schema tags
   the plan left behind. Sema-upgrade orchestrated the plan; the
   per-record dispatch is the daemon's own read code.
5. The daemon updates its bound schema-address reference and serves.

This is the boot-time upgrade protocol from intent record 41 (Nix-
flake-versioned, "named variants like unstable and testing"). The
Nix flake pins both the daemon binary and the schema-address that
binary commits to; sema-upgrade is the runtime that bridges deploys.

## 6. Sema-upgrade's own forge

Per intent/workspace.nota (forge component decision) and
intent/nix.nota 2026-05-19, **forge** is the workspace's name for
its eventual native build mechanism — the destination that replaces
Nix. Sema-upgrade has its own forge.

The first sema-upgrade forge is a thin shim over Nix. The shim
wraps existing Nix machinery — `nix build`, the flake.lock pin chain,
the derivation graph — so sema-upgrade's perspective is "the forge
built this artifact at this address" rather than "Nix evaluated this
flake at this pin". Concrete shape:

- A typed `BuildRequest` names the component and desired version
  (a flake pin or schema-address).
- The wrap invokes `nix build --max-jobs 0` (per the workspace
  remote-builder constraint) against the underlying flake.
- The wrap parses Nix's output (derivation path, inputs) into a
  typed `BuildOutcome` carrying the schema-address sema-upgrade can
  compare against.
- Nothing of Nix's internal model leaks through. The typed surface
  is forge-shaped; when the underlying machinery changes, only the
  shim changes.

The wrap exists because the schema-address discipline needs first-
class typed identifiers and Nix doesn't speak in those — Nix speaks
in store paths and recipe hashes. The shim translates.

When forge ships (intent/nix.nota 2026-05-19 names the destination
without committing to its shape), sema-upgrade is the first load-
bearing consumer, because sema-upgrade is what speaks across deploys
and needs the cleanest available identifier for "this build" across
releases. The shim retires. Forge's exact shape is out of scope here
(separate report 271).

## 7. Owner contract — policy

The owner channel carries the policy authority surface — what an
owner of sema-upgrade does that ordinary peers cannot.

- **Approve a plan before it runs.** A plan generated by `Plan` is
  not self-executing. The daemon that received `PlanRequired` waits;
  an owner approves via `ApprovePlan (PlanApproval (PlanIdentifier)
  (ApprovalScope …))`. Approval may be unconditional, scope-limited
  (zero-cost steps only), or schedule-constrained. Default approval
  policy lives in `bootstrap-policy.nota` — typically auto-approve
  zero-cost steps, require explicit owner approval for append-only
  and structural steps.
- **Reject a plan.** `RejectPlan` cancels; the daemon stays halted
  pending investigation.
- **Throttle.** `ConfigureThrottle` carries per-step pacing (records
  per second, parallelism limit). Throttling protects the underlying
  sema-engine from migration starving service traffic.
- **Quarantine.** Repeated migration failure invokes `Quarantine
  (QuarantineDirective (Component …) (Reason …))`. The daemon
  remains halted; owner investigation required. `Release` clears
  the quarantine.
- **Register / retract trusted schemas.** `RegisterSchema` /
  `RetractSchema` maintain the catalogue. An address not in the
  catalogue produces `UnknownStoredAddress` at inspection.

## 8. Sema-upgrade's own sema database

Two state categories per the universal policy/working split.

**Policy state** (bootstrapped from `bootstrap-policy.nota`):
- `schema_catalogue` — trusted schemas (address, description,
  originating component). Mutated by owner `RegisterSchema` /
  `RetractSchema`.
- `approval_policy` — per-component rules for which plan classes
  auto-approve vs need explicit owner approval.
- `throttle_defaults` — per-component default throttle.
- `quarantine_policy` — failure-rate thresholds that trigger
  automatic quarantine.

**Working state** (produced by operation):
- `migration_history` — every migration that ran, keyed by
  `MigrationIdentifier`, carrying source address, target address,
  the plan record, timestamp range. Append-only.
- `step_outcomes` — every step report nested under its migration.
  Failed-step records carry the `FailureClassification`.
- `current_addresses` — per-component, the address of the data
  according to the last successful migration. Consulted at
  `Inspect` time.
- `quarantine_state` — per-component status, reason, timestamp.
- `pending_plans` — plans generated but not yet approved-and-
  executed. Garbage-collected after an age threshold.

Plan records are stored as snapshots so that an audit can replay
exactly what ran, against which addresses, with which outcomes.

## 9. Open design questions

1. **Plan execution authority — daemon or sema-upgrade?** The sketch
   has sema-upgrade as orchestrator and the daemon's read path doing
   the record-level work. Alternative: sema-upgrade opens the
   daemon's sema database directly during migration (daemon shut
   down, single-writer safe). That violates triad invariant 2 (no
   one opens another daemon's store). The orchestrator-only shape
   preserves the invariant but requires the daemon expose its read
   path through some surface — a startup-mode socket, an in-process
   upgrade library both link, or a Signal sub-protocol. Designer
   lean: in-process upgrade library, since the daemon already links
   the per-version type modules per Approach C. Needs psyche
   direction.

2. **Where the 0.01 file-substrate adapter lives.** Three homes:
   (a) hardcoded into sema-upgrade's lib at pilot stage; (b) a
   sibling `sema-upgrade-substrate-file-log` crate if other
   source-substrate bridges appear; (c) absorbed into the
   structural-migration declaration syntax from /263. Designer
   lean: (a) for the pilot; (b) if a second source-substrate
   appears.

3. **Sema-upgrade's own schema evolution.** Recursive: if
   sema-upgrade's contracts evolve, who upgrades sema-upgrade?
   Does it call itself, or does its schema use a hand-written path
   because it's the bottom of the stack? Designer lean: hand-
   written path until sema-upgrade's contracts stabilise, then
   dogfood once.

4. **What happens to legacy `intent/*.nota` after migration.**
   Options: delete (spirit is source of truth); keep as historical
   artefact; keep live as fallback. Post-migration psyche question,
   not part of sema-upgrade's design.

5. **Cross-daemon authority.** Sema-upgrade is owned by — whom?
   Not a persona component (workspace infrastructure under every
   persona daemon). Owner caller is likely the engine manager
   directly. Needs psyche confirmation when sema-upgrade enters the
   persona authority graph.

6. **Approve-once vs approve-each-component.** Single approval that
   covers all components at a given schema address (faster
   workspace-wide rebuilds) vs per-component approval (safer
   auditing). Designer lean: per-component by default, with an
   owner-issued "approval set" for coordinated bundles.

7. **Idempotent re-run.** A plan that ran partially, failed, then
   re-runs: sema-upgrade's `step_outcomes` records which steps
   succeeded, but the daemon's per-record schema-address tags
   (Approach C) are the ground truth on what was migrated.
   Coordinate the resume protocol explicitly.

## References

- `intent/component-shape.nota` 2026-05-21 (sema-upgrade component
  record per the design brief) — the load-bearing intent record
  this report derives from.
- `intent/component-shape.nota` 2026-05-21 record 21 — Approach C
  selection.
- `intent/persona.nota` 2026-05-20T15:30Z — persona-spirit must not
  contain import logic.
- `intent/workspace.nota` (forge component decision, just logged) —
  sema-upgrade's first forge wraps Nix.
- `intent/nix.nota` 2026-05-19 — forge as the eventual replacement
  for Nix.
- `reports/designer/263-schema-specification-language-design.md` —
  the language schemas are written in; the schema-layout schema
  sema-upgrade consumes to derive migration plans; diff
  classification semantics. Composes with the Approach C
  (in-process versioned reads) selection in intent record 21,
  using content-addressed schema subtrees rather than
  per-component or per-record-type version counters.
- `skills/spirit-cli.md` §"Substrate migration discipline" — the
  general migration rules; the `High` rung drift the 0.01 plan
  absorbs is the canonical worked case.
- `skills/component-triad.md` — triad shape and invariants.
- `skills/spirit-cli.md` — how to find the deployed spirit wire
  shape sema-upgrade calls into for the 0.01 pilot.
