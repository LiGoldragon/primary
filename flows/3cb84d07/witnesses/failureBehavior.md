# Failure and recovery behavior

Method: code read `/git/github.com/LiGoldragon/lojix/README.md`,
`ARCHITECTURE.md`, `src/schema_runtime.rs`, `src/daemon.rs`, and the current
`lojix` skill.

Observed:

- `DeployAccepted` is admission only. Terminal state must be re-queried by
  deployment identifier or event-log position.
- The pipeline records Submitted, Building, Copying, Activating, Activated,
  and terminal Completed/Rejected/Failed records. Failure records identify a
  stage such as FlakeAuth, MaterializeHorizon, Eval, Build, CopyClosure, or
  Activate.
- Activation runs target-side profile and activation commands. A failed
  activation can therefore leave a partial target change; the durable Lojix
  generation record is committed only after activation succeeds.
- `ActivateNow` has no automatic rollback. `ScheduleBootOnce` has explicit
  boot-once bookkeeping that keeps the prior boot entry as the persistent
  default while scheduling the new entry once; it is a distinct action.
- Durable in-flight cursors support stage-aware daemon restart/resume; the
  current profile and runtime links are separate evidence from Lojix's
  committed generation set.

Inference: a failed Zeus deployment would need target-side profile, runtime,
boot, and activation-journal inspection before deciding whether the host
changed or whether retry/rollback is safe. None of that can be established
while Zeus is unreachable and no proposal has been evaluated.
