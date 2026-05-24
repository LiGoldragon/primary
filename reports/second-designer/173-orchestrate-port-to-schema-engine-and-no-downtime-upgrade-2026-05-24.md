*Kind: Port · Topic: orchestrate-schema-engine-port · Date: 2026-05-24 · Lane: second-designer*

# 173 — Orchestrate port to schema engine + no-downtime upgrade

**Status:** Phase 1+2+3+4 LANDED on feature branches; ready for operator integration after Spirit MVP. This was a PARALLEL second-designer track per psyche directive 2026-05-24, while operator works Spirit MVP on main.

## §1 Locator

Three worktrees, three feature branches, three pushed commits:

| Repository | Worktree path | Feature branch | Commit |
|---|---|---|---|
| `signal-orchestrate` | `/tmp/port-signal-orchestrate` | `feature/schema-engine-and-no-downtime-upgrade` | `45a63ab3` |
| `orchestrate` | `/tmp/port-orchestrate` | `feature/schema-engine-and-no-downtime-upgrade` | `44a98a7b` |
| `schema` | `/tmp/orchestrate-schema-example` | `feature/orchestrate-schema-example` | `0d16db07` |

**Bead:** `primary-8089` (orchestrate schema-engine + no-downtime upgrade port).

**Intent record:** `519` (workspace, Decision, Maximum certainty) — psyche 2026-05-24: "work on porting the orchestrate component to e2e engine and schema-based no-downtime upgrade in parallel with the work being done on spirit. use a worktree, let the operator work on the main branch."

All three pushed to `origin`; no push failures.

## §2 What was implemented

### Phase 1 — Schema design (LANDED)

`orchestrate.schema` at `signal-orchestrate/orchestrate.schema` follows the v13 six-position structure: `{imports} [ordinary header] [owner header] [sema header] {namespace} [features]`. Header form is uniform per intent 494: every root is `(VerbName [SubVariant ...])`, including single-sub-variant cases.

Imports the sema layer (`SemaOperation`, `SemaObservation`) from sibling `schemas/signal-sema/sema.schema`. Mirrors the Spirit pattern at `signal-persona-spirit/schemas/signal-sema/sema.schema`.

The schema covers:
- 9 ordinary routes — `Claim`, `Release`, `Handoff` (single endpoint each); `Observe` (`Roles`, `Lanes` — two unit endpoints); `Submit`, `Query`, `Watch`, `Unwatch` (single endpoint each).
- 6 owner routes — `Create` (single); `Retire` (two endpoints: `Role`, `Lane` — mixed payload); `Refresh`, `Register`, `SetAuthority` (single each).
- All wire types from the live `signal-orchestrate` + `owner-signal-orchestrate` libs, lifted into the namespace.
- `Reply` + `Observable` features.

### Phase 2 — Schema crate witness (LANDED)

`tests/orchestrate.rs` in the `schema` crate parses, assembles, and asserts the expected route shape: ordinary leg = 9 routes, owner leg = 6, `Claim Role` route = `Type(RoleClaim)`, `Observe Lanes` = `Unit` at slot (3,1), `Retire Lane` = `Type(LaneIdentifier)` at owner slot (1,1), imported `SemaObservation` and local `Role` both reachable.

All 21 schema crate tests pass (17 original + 1 new orchestrate test + 3 reader tests).

### Phase 3 — Hand-equivalent emitter module (LANDED)

`signal-orchestrate/src/schema_emitted.rs` documents — in executable Rust — what a future macro pass would emit from `orchestrate.schema`. Includes:
- `Operation` + per-root sub-enums for both legs (ordinary + owner)
- `ShortHeader` projection — two-byte `(root, endpoint)` discriminator
- `OrdinaryDispatch` + `OwnerDispatch` traits with `dispatch()` method routing each `(root, endpoint)` pair to a typed handler method
- `project_to_sema` + `project_owner_to_sema` — the Layer 2 → Layer 3 classification per the verb-spine rule (`skills/component-triad.md` §"Verbs come in three layers")
- `SemaTable` enum naming the daemon's redb tables

The module exists as a documentation-in-code module; the live hand-written `signal_channel!` invocation in `lib.rs` is untouched.

3 smoke tests on the emitted shape: short-header consecutive slot assignment, Sema projection per root, dispatch-trait round-trip through a counting fake.

### Phase 4 — No-downtime upgrade handover (LANDED)

`signal-orchestrate/src/upgrade_handover.rs` carries the **drain-with-mirror** protocol design, the two state machines (current-version daemon + next-version daemon), the wire-protocol shapes for the private upgrade socket, and the `OrchestrateVersionProjection` trait skeleton.

5 smoke tests: current-daemon Active→Draining→PostFlip→Retired walk, next-daemon Standby→Hydrating→Catching→Active walk, drain-abort returns to Active, invalid transitions are typed errors, latency targets have sensible defaults.

### Daemon-side ARCH update (LANDED)

`orchestrate/ARCHITECTURE.md` gains a new "Pending schema-engine port + no-downtime upgrade" section pointing operator at the contract-side artifacts and naming the daemon-side modules that need to land.

## §3 What was NOT implemented

This is a port pilot — explicitly partial. The following are NOT in scope and are not done:

- **Macro library does not yet emit orchestrate's shape.** The current schema macro MVP (`signal-frame/macros/src/schema_reader.rs`) supports **one endpoint per operation root** and **non-unit payloads** only. Orchestrate has two routes that need richer macro support: `Observe [Roles Lanes]` (two endpoints, both unit) and `Retire [Role Lane]` (two endpoints, mixed payload). The schema is ready; the macro needs extension.
- **No live cutover of `signal-orchestrate`'s wire types.** The hand-written `signal_channel!` macro invocation in `lib.rs` is untouched. The `schema_emitted` module documents the target; the cutover lands when the macro library can emit it.
- **No daemon-side handover implementation.** The state machines in `upgrade_handover.rs` are skeleton; the daemon's third socket listener, the drain-mode handler gating in `service.rs`, the lock-projection suppression after `HandoverAccepted`, and the `MirrorWrite` replay logic are all named in the ARCH but not coded.
- **No `version-projection` impls.** The `OrchestrateVersionProjection` trait skeleton exists; concrete impls for each storage type land alongside an actual v0.1.x → v0.1.y schema diff. None exists today because orchestrate is still on its initial schema.
- **No `signal-version-handover` integration.** The wire-protocol shapes in `upgrade_handover.rs` are local skeletons; the real definitions live in the `signal-version-handover` crate per `reports/designer/287`. Integration happens when the daemon actually opens the upgrade socket.

## §4 The schema file

`signal-orchestrate/orchestrate.schema`:

```nota
{
  SemaSet (Import schemas/signal-sema/sema.schema [SemaOperation SemaObservation])
}

[
  (Claim [Role])
  (Release [Role])
  (Handoff [Role])
  (Observe [Roles Lanes])
  (Submit [Activity])
  (Query [Activity])
  (Watch [Operations])
  (Unwatch [Token])
]

[
  (Create [Role])
  (Retire [Role Lane])
  (Refresh [RepositoryIndex])
  (Register [Lane])
  (SetAuthority [Lane])
]

[]

{
  HarnessKind [Codex Claude]
  LaneAuthority [Structural Support]
  DownstreamComponent [Router Harness Terminal Message Mind System Introspect]
  ApplicationFailureReason [Unreachable Rejected Unimplemented TimedOut Unknown]
  UnimplementedReason [NotBuiltYet IntegrationNotLanded DependencyNotReady]
  RoleCreationRejectionReason [RoleAlreadyExists ReportRepositoryAlreadyExists ReportLaneAlreadyExists]
  HandoffRejectionReason [
    SourceRoleDoesNotHold
    (TargetRoleConflict (Vec ScopeConflict))
  ]
  ScopeReference [
    (Path WirePath)
    (Task TaskToken)
  ]
  ActivityFilter [
    (RoleFilter RoleIdentifier)
    (PathPrefix WirePath)
    (TaskTokenFilter TaskToken)
  ]
  OperationKind [
    Claim Release Handoff Observe Submit Query Watch Unwatch
  ]
  OwnerOperationKind [
    Create Retire Refresh Register SetAuthority
  ]

  RoleIdentifier (String)
  RoleToken (String)
  LaneIdentifier (String)
  WirePath (String)
  TaskToken (String)
  ScopeReason (String)
  TimestampNanos (u64)
  ActivitySlot (u64)
  ObservationToken (u64)
  RecordCount (u32)
  ActivityLimit (u32)

  Role ((Vec RoleToken))

  RoleClaim (RoleIdentifier (Vec ScopeReference) ScopeReason)
  RoleRelease (RoleIdentifier)
  RoleHandoff (RoleIdentifier RoleIdentifier (Vec ScopeReference) ScopeReason)

  ActivitySubmission (RoleIdentifier ScopeReference ScopeReason)
  Activity (RoleIdentifier ScopeReference ScopeReason TimestampNanos)
  ActivityQuery (ActivityLimit (Vec ActivityFilter))

  ObservationSubscription (Boolean Boolean)

  ScopeConflict (ScopeReference RoleIdentifier ScopeReason)

  ClaimEntry (ScopeReference ScopeReason)
  RoleStatus (RoleIdentifier HarnessKind (Vec ClaimEntry))

  LaneRegistration (LaneIdentifier Role LaneAuthority)
  LaneRegistrationRequest (Role LaneAuthority)
  LaneAuthorityChange (LaneIdentifier LaneAuthority)

  CreateRoleOrder (RoleIdentifier HarnessKind)
  RetireRoleOrder (RoleIdentifier)
  RefreshRepositoryIndexOrder (RecordCount)

  ApplicationSuccess (DownstreamComponent ScopeReason)
  ApplicationFailure (DownstreamComponent ApplicationFailureReason ScopeReason)

  Claim [(Role RoleClaim)]
  Release [(Role RoleRelease)]
  Handoff [(Role RoleHandoff)]
  Observe [Roles Lanes]
  Submit [(Activity ActivitySubmission)]
  Query [(Activity ActivityQuery)]
  Watch [(Operations ObservationSubscription)]
  Unwatch [(Token ObservationToken)]

  Create [(Role CreateRoleOrder)]
  Retire [
    (Role RetireRoleOrder)
    (Lane LaneIdentifier)
  ]
  Refresh [(RepositoryIndex RefreshRepositoryIndexOrder)]
  Register [(Lane LaneRegistrationRequest)]
  SetAuthority [(Lane LaneAuthorityChange)]

  ClaimAcceptance (RoleIdentifier (Vec ScopeReference))
  ClaimRejection (RoleIdentifier (Vec ScopeConflict))
  ReleaseAcknowledgment (RoleIdentifier (Vec ScopeReference))
  HandoffAcceptance (RoleIdentifier RoleIdentifier (Vec ScopeReference))
  HandoffRejection (RoleIdentifier RoleIdentifier HandoffRejectionReason)
  RoleSnapshot ((Vec RoleStatus) (Vec Activity))
  LanesObserved ((Vec LaneRegistration))
  ActivityAcknowledgment (ActivitySlot)
  ActivityList ((Vec Activity))
  PartialApplied ((Vec ApplicationSuccess) (Vec ApplicationFailure))
  ObservationOpened (ObservationToken)
  ObservationClosed (ObservationToken)
  OrchestrateRequestUnimplemented (OperationKind UnimplementedReason)

  RoleCreated (RoleIdentifier HarnessKind WirePath WirePath)
  RoleRetired (RoleIdentifier)
  RoleCreationRejected (RoleIdentifier RoleCreationRejectionReason)
  RepositoryIndexRefreshed (RecordCount)
  LaneRegistered (LaneRegistration)
  LaneRetired (LaneIdentifier)
  LaneAuthoritySet (LaneIdentifier LaneAuthority)
  OwnerOrchestrateRequestUnimplemented (OwnerOperationKind UnimplementedReason)

  OperationReceived (OperationKind)
  EffectEmitted (SemaObservation)
}

[
  (Reply
    ClaimAcceptance
    ClaimRejection
    ReleaseAcknowledgment
    HandoffAcceptance
    HandoffRejection
    RoleSnapshot
    LanesObserved
    ActivityAcknowledgment
    ActivityList
    PartialApplied
    ObservationOpened
    ObservationClosed
    OrchestrateRequestUnimplemented
    RoleCreated
    RoleRetired
    RoleCreationRejected
    RepositoryIndexRefreshed
    LaneRegistered
    LaneRetired
    LaneAuthoritySet
    OwnerOrchestrateRequestUnimplemented)

  (Observable
    (filter default)
    (operation_event OperationReceived)
    (effect_event EffectEmitted))
]
```

## §5 Tests + checks

| Crate | Tests | Format | Clippy | Nix |
|---|---|---|---|---|
| `schema` | 21/21 pass (17 original + 1 orchestrate + 3 reader) | clean | clean | not run |
| `signal-orchestrate` | 39/39 pass (31 existing round-trip + 8 new schema-emitted/handover) | clean | clean | not run (workspace not under git root) |
| `orchestrate` | unmodified (ARCH-only change) | n/a | n/a | not run |

Detailed test results:

**Schema crate** — `cargo test`:
- `tests/orchestrate.rs::orchestrate_schema_parses_assembles_and_emits_expected_routes` — ordinary leg 9 routes, owner leg 6 routes, `Claim Role` body type, `Observe Lanes` unit at (3,1), `Retire Lane` body at owner (1,1), imported `SemaObservation` + local `Role` both reachable.

**signal-orchestrate** — `cargo test` (new tests only):
- `schema_emitted::tests::short_headers_assign_consecutive_root_slots`
- `schema_emitted::tests::sema_projection_classifies_each_operation_root`
- `schema_emitted::tests::dispatch_trait_routes_each_endpoint_to_its_method`
- `upgrade_handover::tests::current_daemon_walks_active_to_retired`
- `upgrade_handover::tests::next_daemon_walks_standby_to_active`
- `upgrade_handover::tests::drain_can_be_aborted_returning_to_active`
- `upgrade_handover::tests::invalid_transitions_are_typed_errors`
- `upgrade_handover::tests::latency_targets_have_sensible_defaults`

Nix flake check was attempted on the worktrees but blocked by jj workspace pointing at `/tmp` (not a git repo). The compile pass + cargo tests verify the same code.

## §6 Comparison to Spirit MVP

The Spirit MVP pattern (`primary-ezqx.1`) that operator is actively delivering on main lands one component end-to-end through the schema engine: schema file → typed wire types → daemon. This port mirrors that pattern at three points and diverges at three points.

**Mirrors:**

1. **Schema file at the contract repo root.** Spirit's source-of-truth lives at `signal-persona-spirit/spirit.schema`; orchestrate's at `signal-orchestrate/orchestrate.schema`. Same six-position structure; same `schemas/signal-sema/` sibling for imports.
2. **Schema crate as the parser + assembler.** Both use the same `schema` crate that second-operator landed in `/180`. The orchestrate fixture in `schema/tests/orchestrate.rs` follows the same shape as `schema/tests/reader.rs::reads_schema_file_with_local_imports_and_lowers_routes` for spirit-v0-1-1.
3. **Hand-equivalent module pattern.** The Spirit world uses `signal-persona-spirit/src/migration.rs` for version projections; orchestrate uses `signal-orchestrate/src/schema_emitted.rs` for the would-be-macro-emitted shape. Both modules are documentation-in-code that operator can fold into the macro emission when the macro library is ready.

**Diverges:**

1. **Macro readiness.** Spirit's `signal-persona-spirit` already uses `signal_channel!([schema])` because Spirit's schema fits the macro MVP (one endpoint per root, non-unit payloads). Orchestrate's schema is richer (multi-endpoint roots, unit payloads) and the macro can't emit it yet — so the `schema_emitted` module is a documentation module rather than the live wire types.
2. **No-downtime story.** Spirit's handover uses the generic `signal-version-handover` protocol from `reports/designer/287`. Orchestrate adds **drain-with-mirror** semantics on top because orchestrate IS the lane-claim authority and cannot tolerate even brief two-writer windows. The `upgrade_handover.rs` module evaluates and rejects two alternative protocols before settling on drain-with-mirror.
3. **Owner contract surface.** Spirit's contract today has only the ordinary header (`signal-persona-spirit`'s owner contract is named but minimal). Orchestrate's port covers BOTH legs from day one — `signal-orchestrate` ordinary + `owner-signal-orchestrate` owner — because both already exist and both have substantial type surface (`Create` / `Retire` / `Refresh` / `Register` / `SetAuthority`).

The port is the **second test of the schema-migration scalability claim**: if Spirit can do it, so can orchestrate. The two ports together demonstrate that the schema engine handles BOTH single-leg and dual-leg components, BOTH single-endpoint and multi-endpoint routes, and BOTH simple-update and lane-authority-preservation upgrade requirements.

## §7 No-downtime upgrade design

The protocol settled on is **drain-with-mirror** (variant 3 of three evaluated). Full design in `signal-orchestrate/src/upgrade_handover.rs` module-level docstring; summary here.

### Why orchestrate needs a richer handover than Spirit

Orchestrate IS the workspace's lane-claim authority. Brief downtime means every parallel agent cannot acquire scope until the daemon is back. Spirit's downtime degrades to "writes briefly buffered" — Spirit can serve from buffered state when the cutover races. Orchestrate cannot — a lane claim during cutover MUST be authoritative the moment it's accepted, because the next read (an agent starting work) depends on it.

### Why drain-with-mirror beats the alternatives

| Variant | Reason rejected |
|---|---|
| Mirror mode (both daemons write; conflict-resolve after) | Two-writer window — same claim grantable to two roles; conflict-resolve cannot retract a claim already acted upon. |
| Atomic socket transfer (new binds, old unbinds, symlink flips) | Existing connections to old socket don't discover the flip; some clients see old state, some new, during the rollover. |
| Drain-with-mirror (chosen) | No two-writer window; no connection breakage; bounded drain time. |

### Protocol shape

The next-version daemon starts in cold-standby. Persona (the orchestrator — pending bead `primary-a5hu`) tells current to enter drain mode. Current stops accepting NEW claims, keeps serving reads + release/handoff on existing claims, and mirrors every accepted mutation to next via the private upgrade socket. Next hydrates from current at a commit marker, then catches up via mirrored writes. When current and next agree on the marker, Persona flips the active-version selector. New connections land on next. Current keeps serving its existing connections until they close (mirroring every state change to next), then retires.

### State machines

Current-version daemon: `Active → Draining → PostFlip → Retired` (with `Draining → Active` abort path).

Next-version daemon: `Standby → Hydrating → Catching → Active`.

Both encoded in typed Rust enums in `upgrade_handover.rs` with `transition()` methods that return typed errors for invalid transitions. 5 smoke tests cover the happy path + abort + invalid transition.

### Open mechanism questions

The protocol is settled; mechanism choices remain:

- **Selector-flip mechanism.** Symlink? Systemd unit? Process-local registry? Spirit's v0.1.0→v0.1.1 cutover uses CriomOS-home's symlink today; Persona owns the long-term active-version selector (bead `primary-a5hu`).
- **Lock-file projection race.** Both daemons project to the SAME `orchestrate/<role>.lock` paths. Solution chosen: current STOPS projecting once it sends `HandoverAccepted` — next becomes the sole projector from that moment. Codified in `CurrentDaemonState::projects_lock_files()`.
- **Long-lived connections.** If an existing connection NEVER closes (e.g. a `Watch` subscription held by a long-running agent), current can't retire. Mitigation: Persona's `ForceCloseLingeringConnections` admin operation (named in the open questions but not yet a typed verb in `owner-signal-orchestrate`).

## §8 Open psyche questions

These are the questions where intent is unclear and the psyche's direction would settle the design. Listed in priority order (psyche attention is scarce — answer the top one first).

1. **(High priority — blocks daemon-side cutover.)** Does the macro library extension to support multi-endpoint roots + unit payloads belong on the Spirit MVP epic (`primary-ezqx.1`), or as a separate epic that lands after Spirit MVP? If on Spirit, orchestrate cutover happens "for free" when Spirit lands; if separate, orchestrate cutover is gated on the macro epic landing first. The macro extension is needed by mind too (mind's contract has multi-endpoint roots) — separating it from Spirit may actually accelerate other components.
2. **(Medium priority — blocks the upgrade protocol cutover.)** Is **drain-with-mirror** the right protocol for orchestrate specifically, or should orchestrate use the same generic protocol as Spirit (with worse properties for lane-claim authority)? The drain-with-mirror analysis in `upgrade_handover.rs` is a design proposal; the psyche may have intent the design hasn't surfaced.
3. **(Low priority — affects ARCH boundaries.)** Should the schema-emitted module pattern (`signal-orchestrate/src/schema_emitted.rs`) become a workspace convention for documenting macro-target shapes BEFORE the macro emits them? Or is it a one-off pedagogical artifact for the port that gets deleted when the live macro emission lands? The pattern is useful for parallel design — multiple components can converge on the same target shape without waiting for the macro — but it's also code duplication that needs garbage collection.

## §9 Recommendation for operator

When Spirit MVP lands and operator looks at this port, here's the integration order I'd recommend:

1. **Extend the macro library** (`signal-frame/macros/src/schema_reader.rs`) to support multi-endpoint operation roots + unit endpoint payloads. The current MVP errors at `Observe [Roles Lanes]` and `Retire [Role Lane]`. The extension is mechanical: emit per-root sub-enums when the root has >1 endpoint, and emit `Unit` payload variants for endpoint-without-body cases. The `schema_emitted` module in this port is the concrete target shape.
2. **Run `cargo build` on `signal-orchestrate` after switching to `signal_channel!([schema])`.** The schema is ready; the macro now emits it; the existing hand-written types in `lib.rs` either delete or move into a deprecated alias module for transitional callers. Spirit's pattern at `signal-persona-spirit/src/lib.rs:435` (`signal_channel!([schema]);`) is the model.
3. **Apply the same cutover to `owner-signal-orchestrate`.** Both contract crates point at the same `orchestrate.schema` via `CARGO_PKG_NAME` strip-prefix logic in `schema_reader.rs:47-54`. Test that the schema_path logic correctly resolves `owner-signal-orchestrate` → `orchestrate.schema`.
4. **Cut the runtime daemon over to the macro-emitted contract types.** The daemon's `OperationLowering` (`orchestrate/src/lowering.rs`) is the contract-to-Component-Command translation point; it consumes the contract's `Operation` enum, which the macro now emits. Migrate dispatch arms one root at a time; existing tests verify each step.
5. **Implement daemon-side handover.** Drop the `upgrade_handover.rs` skeleton from the contract crate (it was Phase 4 scaffolding for protocol design); land the daemon-side at `orchestrate/src/upgrade_handover.rs` with the `OrchestrateVersionProjection` impls and the private upgrade socket listener. Spirit's `signal-persona-spirit/src/migration.rs` is the per-type projection pattern.
6. **Land `version-projection` impls for orchestrate's storage types.** Concrete diffs land alongside a real v0.1.x → v0.1.y schema change. None exists today; the first one becomes the witness for the handover protocol.
7. **Integrate with Persona's active-version selector** when Persona lands (bead `primary-a5hu`). Until Persona exists, the cutover uses a manual selector flip via CriomOS-home — the same pattern Spirit uses today.

If this sequence holds, the port lands cleanly into the same flow as Spirit; the second component proves the migration scales, and downstream components (mind, router, harness) follow the same pattern.

## §10 References

- **Intent record `519`** — workspace · Decision · Maximum certainty · psyche 2026-05-24 directive for parallel orchestrate port.
- **Bead `primary-8089`** — orchestrate schema-engine + no-downtime upgrade port.
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — uniform header form, six-position schema structure
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — Spirit MVP pattern this port mirrors
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — working `.schema` file shape
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — header/body/feature separation
- `reports/designer/287-version-handover-component-explained.md` — generic version handover stack
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/3-next-as-dependency-design.md` — next-as-dep upgrade pattern
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md` §10 — hard- vs smart-handover
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — schema crate landing
- `reports/second-designer/172-design-mockup-dispatch/5-overview.md` — schema crate forward-fix mockups
- `/git/github.com/LiGoldragon/schema/` — the typed schema crate
- `/git/github.com/LiGoldragon/signal-orchestrate/` — ordinary contract (the schema home)
- `/git/github.com/LiGoldragon/owner-signal-orchestrate/` — owner contract (also gets schema-emitted)
- `/git/github.com/LiGoldragon/orchestrate/` — runtime daemon + CLI
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` — Spirit's schema source-of-truth (the model this port mirrors)
- `/git/github.com/LiGoldragon/signal-frame/macros/src/schema_reader.rs` — the macro library's schema adapter
- `/home/li/primary/skills/component-triad.md` — daemon + ordinary + owner contract pattern
- `/home/li/primary/skills/jj.md` — version control discipline (jj inline-only)
