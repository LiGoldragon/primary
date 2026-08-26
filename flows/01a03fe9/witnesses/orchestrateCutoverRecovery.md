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
