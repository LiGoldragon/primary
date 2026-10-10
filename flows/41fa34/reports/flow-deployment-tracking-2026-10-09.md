# Flow deployment tracking boundary — 2026-10-09

The sole Astra deploy writer extends the existing `LaunchStatus` inspection
with recorded attempt, phase, and binding; it may record a settled outcome
and a Flow node or its absence.  This note performs no query and infers no
topic, registry, identity, or Current state.

`Current` remains unimplemented.  Authored Ethos/schema consumer work must
precede an immutable Prometheus Nix and Field generation/check handoff.  A
source candidate is neither checked nor deployed while Field is blocked.
