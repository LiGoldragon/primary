# Flow 01a03fe9

The authorized Home/Orchestrate Nexus cutover found three active legacy PathLock rows. The 0.25 Nexus had failed and its ordinary socket was absent. The read-only candidate preflight reported three rows, so the approved abort branch started only the 0.24 Nexus as a transient user unit.

The 0.24 ordinary surface has no observation operation; it accepts only PathLock registration and PathLockRelease. A safe duplicate-name probe, made non-mutating by overlapping this flow's own held path, identified all three rows: `claudeDesktopPinnedCli`, `claudeDesktopPinnedCliSupplement`, and `claudeDesktopPinnedCliVersions`. They originated in session `01a03e2c`, whose final says its workspace closed; the recorded worktree is absent and no active agent owns it. Old PathLocks have no durable Flow or ID. No rows were released or store state changed.

The recorded deployment order requires the independent CriomOS Lojix ownership-gate repair before Home activation. That worker cannot acquire an authored Lock while 0.24 is active because the installed 0.25 client has an incompatible wire frame. No repair edit or Home activation has occurred. Cross-subflow work is tracked as CriomOS-6ez. Root has the authority question.

Remembered: 01a03eda — depth 1. Its report and final responses establish the preflight branch and exact candidate Home revision.
