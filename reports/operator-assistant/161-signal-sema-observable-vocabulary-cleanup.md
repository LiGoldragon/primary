# Signal Sema Observable Vocabulary Cleanup

Date: 2026-05-20
Lane: operator-assistant
Source: `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md`

## What Changed

`signal-persona-orchestrate` no longer exposes the stale
`OperationObserved` / `SemaEffectObserved` observation vocabulary.
The contract now uses `OperationReceived` and `EffectEmitted`, and
`EffectEmitted` carries `signal_sema::SemaObservation`.

The orchestrate NOTA wrapper heads changed with the type names:
`OperationReceived` and `EffectEmitted`.

`signal-persona-orchestrate/Cargo.lock` was advanced to the current
`signal-sema` commit that exports `SemaObservation` and
`SemaOutcome`. That also advanced the paired `nota-codec` /
`nota-derive` pins required by the refreshed dependency graph.

`signal-persona-introspect/ARCHITECTURE.md` now names the subscriber
event pair as `OperationReceived` / `EffectEmitted`.

## Verification

- `CARGO_BUILD_JOBS=2 cargo test --locked`
  in `signal-persona-orchestrate`
- `CARGO_BUILD_JOBS=2 cargo test --locked`
  in `signal-persona-introspect`
- `nix flake check --max-jobs 0`
  in `signal-persona-orchestrate`
- `nix flake check --max-jobs 0`
  in `signal-persona-introspect`

All passed.

## Residual Notes

The targeted workspace scan found no remaining old symbols in source
under `/git/github.com/LiGoldragon`. Remaining `SemaEffectEmitted`
hits are historical reports plus current intent that already says to
rename away from that old name.

The one intentional compatibility break is the NOTA event head rename.
If any live daemon/client still reads the old `Operation` or
`SemaEffect` heads, add temporary decode aliases before using this
contract in that runtime path.
