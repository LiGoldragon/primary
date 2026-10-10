# Orchestrate 0.18 state-only review — 2026-07-28

## Verdict

Source behavior passes. The strict full-process boundary fails because the
packaged daemon probes prohibited host paths before readiness. Do not deploy
revision `0f7c1570896e25c0d9958f1d08dc9810503b64d8` as a completed state-only
release until those probes are attributed and removed or the boundary is
explicitly narrowed.

## Source proof

- All nine Observe forms and Query route through typed Sema-read operations.
- The write executor fails closed if an Observe reaches it.
- Lane/session observation no longer reconciles or persists state.
- Query preserves filters and limits.
- The nonempty fixture exercises terminal rows, retained claims, every
  observation, and filtered Query, then proves byte-identical Sema state.
- Configuration is argv-only; the configuration writer is removed.
- Exact-revision Nix build, test, state-only test, formatting, and Clippy gates
  pass.

Lane replies still use current wall-clock time to calculate presentation age.
This does not persist state, but the reply is not a time-independent
projection.

## Runtime counterevidence

The exact packaged daemon ran inside an isolated `bwrap` environment with
empty workspace/git roots, private temporary storage, no network, and no
mounted `/proc`. It reached readiness and served all nine observations plus a
filtered Query.

The syscall trace recorded:

- one startup `execve`;
- one allowed Sema-store `flock`;
- no later child execution or lock;
- failed pre-readiness probes of `/proc/self/maps`, `/proc/self/cgroup`,
  `/proc/stat`, and `/sys/devices/system/cpu/online`;
- dynamic-loader fallback probes under `/etc`.

All prohibited probes failed because the paths were absent. Their originating
crate/runtime is not yet identified.

## Deployment state

CriomOS-home still pins the older Orchestrate revision and invokes the removed
configuration writer with the old startup shape. No deployment or live daemon
change has occurred.

## Required next evidence

Attribute each pre-readiness host probe to its originating runtime or
dependency. Remove or disable component/dependency probes where possible.
Repeat the isolated syscall witness. If a remaining probe is unavoidable
process-loader infrastructure rather than Orchestrate behavior, present that
exact exception to the psyche instead of silently weakening the boundary.
