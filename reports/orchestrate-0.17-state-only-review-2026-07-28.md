# Orchestrate 0.17 state-only review — 2026-07-28

## Verdict

Commit `d026fe87e9c4` is an intermediate source commit and fails the affirmed
state-only boundary. It must not be deployed as the completed repair.

## Confirmed defects

- `Observe Lanes` enters the Sema-read executor but calls
  `LaneRegistry::observe`, which calls `reconcile()` and atomically retracts
  expired lane and claim rows.
- The expiry worker triggers the same mutation by sending `Observe Lanes`.
- Only Roles, Lanes, and Query enter the Sema-read executor. Sessions,
  SessionLanes, Worktrees, Repositories, Topics, Topic, and Agents still enter
  the write executor.
- Query discards the caller's limit and filters, replacing them with limit 64
  and no filters.
- Role and lane observations derive current wall-clock time rather than being
  projections of stored state.
- The new purity test uses only an empty fresh store and a default query, so it
  cannot expose terminal-row retraction or lost query parameters.
- The source gate is a small substring scan, not the required negative
  namespace/syscall witness.

## Confirmed removals

The commit does remove direct repository scans, lock/symlink projections,
VCS subprocesses, `/proc`/pidfd reachability, path canonicalization, and
worktree scaffolding. Worktree request now typed-refuses; retained
registration/archive/conclusion operations are store transitions.

No `Command::new`, `flock`, `canonicalize`, `/proc`, or pidfd use remains in
the exact reviewed revision. Configuration, migration, socket lifecycle, and
client request-file input remain within the previously declared remainder.

## Validation

Exact-revision Nix checks for state-only tests, the general suite, formatting,
Clippy, and build all passed. They do not prove the state-only contract because
the relevant test fixture is vacuous and no namespace/syscall witness ran.

Version `0.17.0` is internally coherent. Deployment is not updated:
CriomOS-home still pins `83e09a13`, while top-level CriomOS pins `be202b51`.

## Required correction

Before any deployment:

1. route every Observe and Query through a typed read-only executor;
2. remove reconciliation and clock-derived cleanup from read handlers;
3. preserve caller query parameters;
4. test nonempty expired/terminal fixtures and filtered queries;
5. run the negative namespace/syscall witness.
