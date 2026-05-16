# Lojix Built-Generation Ledger Slice

Role: system-specialist  
Date: 2026-05-16  
Branch: `lojix/horizon-re-engineering`  
Commit: `a002123a` (`lojix: record built generations in sema`)

## What changed

The build-only deployment path now records the realized output as a
sema-backed `Generation` after the GC root is pinned and before
`DeploymentBuilt` is emitted.

`GenerationQuery` is no longer a placeholder returning an empty list.
It routes through `RuntimeRoot` to `DeploymentLedgerActor`, which reads
the sema `generations` table and filters by optional
`cluster`/`node`/`kind`.

The old event-log-shaped actor names were tightened into
`DeploymentLedger` / `DeploymentLedgerActor`, because this state owner
now holds deployment identifiers, observation subscriptions,
deployment observations, and built-generation records.

## Tests

Rust checks run locally with low parallelism:

- `cargo test --jobs 1 --test event_log --test build_pipeline --test socket -- --test-threads=1`
- `cargo clippy --jobs 1 --all-targets -- -D warnings`

Nix witnesses run with low local parallelism and dispatched to
Prometheus:

- `nix build --max-jobs 1 --cores 2 .#checks.x86_64-linux.test-event-log .#checks.x86_64-linux.test-build-pipeline .#checks.x86_64-linux.test-socket .#checks.x86_64-linux.clippy`

All passed.

## Constraint Coverage

- C13 now has a concrete witness: built generation records survive a
  sema database reopen.
- C16 now proves a successful build pins its GC root, records the
  built generation, and only then emits `DeploymentBuilt`.
- C20 now has a runtime witness through `GenerationQuery`; it returns
  sema-backed built generations filtered by query fields.

The activation/current-generation semantics are still future work.
Today's implementation records built generations, not activated
current generations.

## Next Work

The next high-signal gap is to run a real build witness rather than a
fake toolchain-only build pipeline. The practical shape is a small
branch-local Nix check or integration script that drives `lojix-daemon`
against the horizon re-engineering branches, asks for a build-only
deployment, and verifies that the returned generation references a real
store path and a real GC root. Activation, closure copy to target, and
rollback remain separate later slices.
