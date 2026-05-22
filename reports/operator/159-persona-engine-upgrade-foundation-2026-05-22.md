# Persona Engine Upgrade Foundation

Date: 2026-05-22
Lane: operator
Primary beads: `primary-a5hu`, `primary-2y5`, `primary-x3ci`

## Summary

This slice moved the `persona` engine manager toward the current Spirit cutover
foundation. It does not implement the full atomic socket handover yet. It adds
the manager-side durable skeleton that the handover can stand on:

- a typed upgrade target model in `src/upgrade.rs`;
- manager messages for preparing and completing a component upgrade;
- manager event-log bodies for `UpgradePrepared` and `ActiveVersionChanged`;
- an active-version snapshot table projected from the manager event log;
- Nix witnesses for the new manager/store behavior.

The implementation uses the new foundation crates directly:

- `version-projection` for `ContractVersion` and handover component names;
- `signal-version-handover` for `AskHandoverMarker` and `HandoverMarker`.

## Architecture Intent

The latest intent says Persona Engine, not CriomOS-home, is the root component
upgrade orchestrator. Component upgrade orders come through owner authority, and
the first Spirit cutover proves the full smart handover path.

This slice implements the first engine-manager layer of that:

1. `Target` names one component upgrade from a current version to a next
   version, with current/next owner sockets and current/next private upgrade
   sockets.
2. `EngineManager::prepare_upgrade` records `UpgradePrepared` in the manager
   event log and returns the first handover operation:
   `AskHandoverMarker(MarkerRequest { component })`.
3. `EngineManager::complete_upgrade` accepts a `HandoverMarker`, validates that
   it belongs to the same component, records `ActiveVersionChanged`, and updates
   the active-version snapshot through the event-log reducer.
4. `ManagerStore::read_active_version` reads the selected version, schema hash,
   and commit sequence as a materialized projection. Snapshot rebuild proves the
   event log remains authoritative.

The current code still stops at the protocol boundary. It constructs and records
handover protocol operations, but it does not yet open component upgrade sockets
or drive the complete multi-daemon transition.

## Code Changed

Repo: `/git/github.com/LiGoldragon/persona`

- `src/upgrade.rs`: new upgrade target, prepared-upgrade event, active-version
  event, and active-version snapshot records.
- `src/manager.rs`: new `PrepareUpgrade` and `CompleteUpgrade` messages, plus
  manager trace events for upgrade prepare/complete.
- `src/engine_event.rs`: new event-log variants.
- `src/manager_store.rs`: manager schema version `4`, active-version snapshot
  table, reducer support, rebuild support, and `ReadActiveVersion`.
- `src/schema.rs`: NOTA projection records for the new event-log bodies.
- `flake.nix`: three named Nix checks for the new constraints.
- `ARCHITECTURE.md`: manager state now names the active-version reducer and its
  Nix witnesses.

## Verification

All verification used the requested low-local/remote-builder shape:

- `CARGO_BUILD_JOBS=2 cargo fmt --check`
- `CARGO_BUILD_JOBS=2 cargo test`
- `nix flake check --option max-jobs 0 -L`
- `nix build .#checks.x86_64-linux.persona-engine-meta-testing-docs-are-nix-backed --option max-jobs 0 -L`

The full Cargo suite passed. The full Nix flake check passed. The targeted Nix
meta-test was rerun after the architecture edit and passed against the final
tree.

New Nix witnesses:

- `persona-manager-store-projects-active-component-version`
- `persona-engine-manager-prepares-upgrade-with-version-handover-request`
- `persona-engine-manager-records-active-version-after-handover-completion`

## Remaining Work

The full cutover is still blocked on these next implementation layers:

- owner-signal surface for submitting upgrade orders to the engine manager;
- engine-manager socket I/O against target component owner/private upgrade
  sockets;
- target component support for private upgrade sockets;
- Spirit v0.1.0 retrofit and v0.1.1 cutover wiring;
- active selector flip in the running Persona engine rather than through
  CriomOS-home deployment;
- failure handling around a marker mismatch, unreachable next daemon, and
  post-copy writes.

The highest-signal next step is the owner-signal engine-management surface, so
the upgrade foundation becomes reachable through the same owner-authority path
that intent record 210 requires.
