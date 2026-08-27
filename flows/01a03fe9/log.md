# Flow 01a03fe9

The authorized Home/Orchestrate Nexus cutover found three active legacy PathLock rows. The 0.25 Nexus had failed and its ordinary socket was absent. The read-only candidate preflight reported three rows, so the approved abort branch started only the 0.24 Nexus as a transient user unit.

The 0.24 ordinary surface had no observation operation; it accepted only PathLock registration and PathLockRelease. A safe duplicate-name probe, made non-mutating by overlapping this flow's own held path, identified all three rows: `claudeDesktopPinnedCli`, `claudeDesktopPinnedCliSupplement`, and `claudeDesktopPinnedCliVersions`. They originated in session `01a03e2c`, whose final says its workspace closed; the recorded worktree is absent and no active agent owns it. Old PathLocks had no durable Flow or ID.

The living then directly ordered deployment. The three exact stale names were released through the 0.24 client, the transient 0.24 Nexus was stopped, and the candidate preflight returned zero rows. The managed 0.25 Orchestrate Nexus is active with both sockets. Live proof passed Lock ID 1, Observe.Locks, Release by ID, and an empty final observation.

The recorded deployment order requires the independent CriomOS Lojix ownership-gate repair before Home activation. The verified 0.25 Lock surface now permits that worker to resume. No Home activation has occurred. Cross-subflow work is tracked as CriomOS-6ez.

Remembered: 01a03eda — depth 1. Its report and final responses establish the preflight branch and exact candidate Home revision.
