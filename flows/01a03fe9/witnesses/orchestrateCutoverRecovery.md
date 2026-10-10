# Orchestrate cutover recovery witness

Method: probe user-systemd status, candidate preflight, legacy client replies, transcript records, and worktree existence.

Before the legacy Nexus started, the candidate preflight completed with `active legacy PathLock rows: 3`. The 0.25 managed unit was failed with `start-limit-hit` after its startup safeguard refused those rows, and its ordinary socket was absent.

The only running Nexus is the transient `orchestrate-legacy-024.service`; its ordinary socket exists. The managed 0.25 service remains failed. Running the candidate preflight while 0.24 is active fails to acquire the Sema database lock, as expected for its read-only exclusive open.

Each of these legacy duplicate probes returned `PathLockRegistrationRejected` with `DuplicateActiveName` and the complete existing PathLock:

- `claudeDesktopPinnedCli`
- `claudeDesktopPinnedCliSupplement`
- `claudeDesktopPinnedCliVersions`

Each request also included this flow's already-held path. If the candidate name were absent, it would have received a path-overlap refusal without registering a row. The duplicate replies prove the three holders while preserving the store.

Session `01a03e2c` registered those rows and its final reported a pushed correction and closed workspace. Its recorded worktree is absent, and no currently active agent corresponds to it.

After the living ordered deployment, the three exact name-based releases each returned `PathLockReleased`. With the legacy transient stopped, the candidate preflight returned `active legacy PathLock rows: 0`. The managed 0.25 Nexus then started, opened both sockets, and returned the complete Lock ID 1, the complete observation containing it, the complete Release reply, and an empty final observation.

Final deployment-state verification found CriomOS repair `be56867a` landed and its own repair Lock released. A read-only `Query.ByNode.(goldragon ouranos None)` returned deployment 72 as `UserEnvironment LiveActivation Current` with revision `ba0de9f84130c47a927a04723db2cb6f33b6b103`. That immutable Home revision keeps the `e0f3bc5e` Orchestrate pin, so this is the effective target and a duplicate activation was unnecessary. `systemctl --user` reported `orchestrate-nexus.service` active/running and an ExecStart ending in `orchestrate-0.25.0/bin/orchestrate-nexus`; both expected sockets existed.

The final ordinary-client proof returned Lock ID 4 for `finalDeploymentWitness`, an observation containing that exact lock, a successful `Release.{4}`, and a final empty `Observe.Locks` snapshot. No lock remains owned by this flow.
