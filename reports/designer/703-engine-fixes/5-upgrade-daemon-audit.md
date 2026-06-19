# 703.5 — upgrade daemon audit: the home for the layout-5 consumer-migration gap

The 702 completeness critic (`13-completeness.md:52`) flagged that the
`upgrade` engine "got no lane" in the 702 sweep, and that the sema-engine
lane's layout-5 gap (sema-2, `4-sema-engine.md:221-232`) asked *"who migrates
consumer `.sema` stores"* and answered *"only spirit wires a migration crate"*
— missing that `upgrade` is the dedicated migration projector. This audit
gives `upgrade` (+ `signal-upgrade`, `meta-signal-upgrade`) the lane it was
denied and answers the four questions head-on.

Audit target: `upgrade` HEAD `5c653e3` (use Kameo lifecycle fork). Build and
test observed once, offline, against a warm `target/`.

## Verdict in one line

`upgrade` is a **real, building, tested runtime library with a placeholder
daemon binary** — not scaffold. It already carries the version/schema
migration orchestration, the handover driver, and the layout-5 field-migration
pattern as live, green code. The one true gap is the last wire: the
`upgrade-daemon` process binary still returns a placeholder and does not yet
mount the `Engine`/`HandoverDriver` it ships, on a socket.

## Q1 — Real building daemon or scaffold? Real runtime, placeholder process.

The repo's own docs undersell it. `INTENT.md:51-55` and `ARCHITECTURE.md:22-31`
describe an "intentionally skeletal U1" with "no Persona `HandoverDriver`, and
no durable database code." **That is stale.** The source tree is 6,688 lines
and carries exactly those things the docs say are absent:

| File | Lines | What it actually is |
|---|---|---|
| `src/handover.rs` | 522 | The full `HandoverDriver` + `HandoverClient` + length-prefixed `HandoverFrameCodec` over `tokio::net::UnixStream` |
| `src/execution.rs` | 775 | The `Engine` implementing generated `NexusEngine`+`SemaEngine`; full signal↔schema projection |
| `src/catalogue.rs` | 216 | `MigrationCatalogue`, `MigrationModule`, `DatabaseMigration` + typed `DatabaseMigrationError` |
| `src/event.rs` | 240 | `ActiveVersionChanged`, `VersionQuarantined`, `ActiveVersion` — the active-version event-log / quarantine record types (rkyv) |
| `src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` | 606 | A real, tested field migration (see Q3) |
| `src/schema/lib.rs` | 3,835 | Checked-in generated runtime roots (Signal/Nexus/SEMA), build-validated |

Build evidence (offline, warm target, run once): **`cargo build` → Finished,
EXIT 0.** **`cargo test` → all green**, including the substantive suites:

- `tests/runtime.rs` — 6 passed: `engine_implements_generated_nexus_and_sema_traits`,
  `supported_upgrade_runs_through_generated_nexus_runner`,
  `multi_operation_request_is_ordered_through_generated_runner`,
  `unsupported_upgrade_rejects_as_typed_contract_reply`,
  `runtime_source_does_not_reintroduce_retired_executor`. These drive
  `Engine::prototype().execute(...)` through the generated Nexus runner —
  the real dispatch path, not a stub.
- `tests/handover_driver.rs` — 2 passed:
  `handover_driver_drives_current_endpoint_after_matching_next_marker`,
  `handover_driver_rejects_next_marker_drift_before_current_readiness`.
  The driver is exercised against actual endpoints.
- `tests/generated_schema.rs` (6), `tests/invocation.rs` (4),
  `tests/binaries.rs`, `tests/dependency_boundary.rs` — all green.

No `assert!(true)`, no `#[ignore]`, no `todo!`/`unimplemented!` on a tested
path. The `NotBuiltYet` typed replies in `execution.rs` (lines 128-142,
201-212, 229-231) are **honest skeleton replies for not-yet-built SEMA verbs**
(meta-policy: Register/Allow/Block/ForceFlip/Rollback/Quarantine, plus
handover write verbs), declared as such — not fake-green dodges. The verbs
that ARE built (`Inspect`, `AttemptUpgrade`, `Report`) run through real logic.

**The placeholder is only the process binary.** `src/bin/upgrade-daemon.rs:1-9`
calls `upgrade::daemon_placeholder_response`, which (per `placeholder.rs:36-46`)
validates the single signal-encoded `.rkyv` argument and returns the literal
string `"upgrade-daemon accepted signal-encoded configuration"`. It never
constructs `Engine`, never opens a socket, never calls `.execute`. So:
**library = real runtime; binary = scaffold.** The runtime substance exists
ahead of the process that mounts it.

## Q2 — Version/schema migration orchestration + handover driver? Yes, both, in code.

**Migration orchestration** — `catalogue.rs` is the live catalogue engine:
`MigrationCatalogue` (line 149) holds `MigrationModule`s; `find` (175) matches
an `Attempt` by `(component, source, target)`; `attempt` (179) runs the module
or returns a typed `Rejection`; `migrate_database` (185) runs the durable
path. `Engine::attempt_upgrade` (`execution.rs:79-91`) records completions and
rejections into in-memory logs and emits the contract reply. The active-version
event log and quarantine list have their **record types** built (`event.rs`:
`ActiveVersionChanged::from_marker`/`from_force_flip`/`from_rollback`,
`VersionQuarantined::from_quarantine`) — these are the persistence shapes the
INTENT promises the daemon will own.

**Handover driver** — `handover.rs:413-518`. `HandoverDriver::from_target`
(421) builds current+next `HandoverClient`s from the target's socket paths.
`drive_current_side` (435) runs the real handover protocol: ask the current
marker, ask the next marker, `ensure_next_marker_matches` (drift-guard over
component / state_sequence / mirrored_write_count / record_frontier, 477-499),
`ready_to_handover`, then `complete_handover` — **with a recovery fallback**
(`recover_from_failure`, 463-472) on completion error. This is the handover
*driver* the prompt asks about, and it is tested.

One discipline note (Q2 lens): `execution.rs:7-9` defines `trait ProjectInto<Target>`
and threads it through ~50 impls instead of the workspace-preferred
`impl From<X> for Y`. It is a deliberate orphan-rule workaround (the crate
projects between two foreign generated contract types it doesn't own, where a
direct `From` would hit coherence), so it is defensible — but it is the one
visible deviation from the `impl From` conversion rule and worth a one-line
note when the operator next touches this file. The `event.rs` helpers
`contract_version_from_meta`/`component_name_from_meta` (232-240) are private
free functions doing cross-contract conversion — the same orphan-rule pressure;
candidates for `impl From` if the wrapper lives in this crate.

## Q3 — Home for the sema-engine layout-5 field-migration (two-submodule historical/current_shape From-chain)? Yes — exactly this pattern, freshly landed.

`src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` is the literal
instance of the pattern the prompt names. It is the FRESH work the critic
spotted (`2eda2c4 freeze spirit migration shape`, +148 in that file region):

- **`mod historical`** (lines 141-275) — frozen v0.1.0 record shapes:
  `historical::StoredRecord` with `Entry { topic: Topic (singular), certainty: Certainty }`.
- **`mod current_shape`** (lines 277-464) — current v0.1.1 shapes:
  `current_shape::StoredRecord` with `Entry { topics: Vec<Topic> (plural), certainty: Magnitude }`.
- **The `From`-chain** (lines 405-457): `impl From<historical::StoredRecord> for current_shape::StoredRecord`
  → `From<historical::StampedEntry>` → `From<historical::Entry>` (which folds
  the singular `topic` into a one-element `topics` vec, 427) →
  `From<historical::Kind>` → `From<historical::Certainty> for Magnitude`
  (the rename, 449-457). This is the exact "two-submodule + From-chain"
  evolution pattern.

It reads via sema-engine (`Engine::open`, `register_table` on a
`historical_records_descriptor`, `QueryPlan::all`, lines 80-92) and writes via
sema-engine (`current_records_descriptor`, `assert`, 98-112), gated by typed
preconditions (`SourceMissing` / `TargetAlreadyExists` / `SameSourceAndTarget`,
47-60). It is **source→target across two separate `.sema` paths**, never
mutating in place. Tests (466-606) prove the certainty→magnitude rename, the
topic→topics fold, the date/time carry, and the two rejection paths — 3 records
migrated, green.

**Crucially, this answers the gap the 702 sema lane left open.** That lane
(`4-sema-engine.md:221-232`) found that of six sema-engine consumers, **only
spirit** wires an in-place migrator (`spirit/src/production_migration.rs`, 4,015
lines, multi-version, embedded in the component), while criome/router/mirror/
persona/mind track `main` with no migration path and will inherit the layout-5
hard-fail on next refresh. `upgrade`'s migration module is the
**component-external** answer the sema lane didn't see: same historical-`From`-chain
discipline as spirit (confirmed — `spirit/src/production_migration.rs:10`
documents "converts each row through the historical `From`-chain"), but in a
dedicated migration repo with a registry, a catalogue, an `Attempt`-keyed
dispatch, and a contract surface — designed to host one such module per
component, not one per component's own tree. The persona_spirit module is the
worked prototype proving the home is real.

## Q4 — Built vs intended.

**Built (green, tested):**
- Single-argument invocation discipline + flag rejection (`invocation.rs`,
  4 tests) for both CLI and daemon; daemon rejects NOTA/`.nota`, requires `.rkyv`.
- The `Engine` Nexus/SEMA runtime for `Inspect` / `AttemptUpgrade` / `Report`.
- The migration catalogue + one real field migration (persona_spirit 0.1.0→0.1.1).
- The handover driver + client + frame codec over UnixStream, with drift-guard
  and recovery fallback.
- Active-version-change and quarantine **record types** (rkyv, event-log shapes).
- Checked-in generated schema roots, build-validated by `build.rs`.
- Dependency boundary: depends on `sema-engine`, `signal-upgrade`,
  `meta-signal-upgrade`, `signal-frame`, `triad-runtime`, `tokio`; no
  `nota-next`/`signal-core` in the default graph (`nota-text` opt-in only).

**Intended, not yet built (the honest gaps):**
1. **The daemon process does not mount the runtime.** `upgrade-daemon.rs`
   returns the placeholder string; it never builds `Engine`, opens the
   ordinary/meta sockets, or runs the dispatch loop. This is the single
   substantive cutover (`ARCHITECTURE.md:93-100` names it). Until then there
   is no *running* migration daemon — only a runtime library plus a stub.
2. **No durable state.** `event.rs` defines the active-version log and
   quarantine *types*, but nothing opens a sema-engine store to persist them;
   the `Engine` keeps completions/rejections in `Vec`s in memory
   (`execution.rs:14-16`). The migration *catalogue* itself runs durable
   (it opens sema stores); the daemon's own policy/history/quarantine state
   does not yet.
3. **Meta-policy SEMA verbs are NotBuiltYet** — Register/Allow/Block/
   ForceFlip/Rollback/Quarantine (`execution.rs:204-212`), plus handover write
   verbs (ReadyToHandover/HandoverCompleted/Mirror/Divergence/RecoverFromFailure,
   208-211) and the read verbs AskHandoverMarker/Query (229-231). The handover
   *driver* (client side) is built; the daemon-side *server* handling of these
   verbs is the stub.
4. **No Persona handover wiring.** INTENT (`44`) keeps process-lifecycle
   authority with Persona ("asks Persona to start next-version units"); no
   Persona call exists yet.
5. **Docs lag code.** `INTENT.md`/`ARCHITECTURE.md` still say "skeletal U1, no
   HandoverDriver, no durable database code" — false at HEAD; the operator/
   designer should refresh both to describe the present runtime-library +
   placeholder-binary split (the `## Status` block at `ARCHITECTURE.md:77-91`
   is accurate; the `## U1 Shape` block at 22-31 contradicts it and is stale).

## Recommendation — its role in closing the layout-5 gap

`upgrade` IS the answer to the sema-engine layout-5 consumer-migration gap,
and it should be named as such. The 702 sema lane's framing — "only spirit
wires a migration crate; the other five have no path" — is true *for in-place,
component-embedded* migration, but the intended architecture is that
**components do not each grow a 4,000-line `production_migration.rs`; they
register one frozen historical-`From`-chain module in `upgrade`**, which owns
the catalogue, the source→target sema-store migration, the version event log,
and the handover that swaps the active store. The persona_spirit module proves
the pattern compiles, reads/writes real sema stores, and passes. So the gap is
not "unbuilt" — it is "built as a library, not yet mounted as a daemon, and
not yet populated with the other five components' modules."

Concrete next moves to close it (operator lane, since it is code-repo `main`):

1. **Refresh the stale `INTENT.md`/`ARCHITECTURE.md` U1-shape language** to
   stop calling the present code skeletal — it misleads anyone scoping the work.
2. **Land the daemon mount** (`ARCHITECTURE.md:93-100`'s named cutover):
   `upgrade-daemon` builds `Engine`, opens ordinary + meta sockets via the
   existing `HandoverFrameCodec`, runs the dispatch loop. This is the gating
   step — without it there is a migration runtime but no migration *service*.
3. **Open durable sema-engine state** for the active-version log + quarantine
   list (the `event.rs` types are ready; they need a store).
4. **Author the remaining consumer migration modules** as they need them —
   criome/router/mirror/persona/mind each get a frozen
   `historical`/`current_shape` module registered in `MigrationCatalogue`,
   rather than each repo growing its own embedded migrator. Spirit's existing
   `production_migration.rs` is the migration of record for spirit's own multi-
   version history; new cross-version steps for the other five belong here.

The deploy-time risk the sema lane raised (live pre-layout-5 `.sema` files
hard-failing on next refresh) is real and not yet closed in the field — but
the *mechanism* to close it exists and is green. The blocker is the daemon
mount and the per-component modules, not a missing design.
