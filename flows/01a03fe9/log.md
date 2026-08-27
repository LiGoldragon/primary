# Flow 01a03fe9

The authorized Home/Orchestrate Nexus cutover found three active legacy PathLock rows. The 0.25 Nexus had failed and its ordinary socket was absent. The read-only candidate preflight reported three rows, so the approved abort branch started only the 0.24 Nexus as a transient user unit.

The 0.24 ordinary surface had no observation operation; it accepted only PathLock registration and PathLockRelease. A safe duplicate-name probe, made non-mutating by overlapping this flow's own held path, identified all three rows: `claudeDesktopPinnedCli`, `claudeDesktopPinnedCliSupplement`, and `claudeDesktopPinnedCliVersions`. They originated in session `01a03e2c`, whose final says its workspace closed; the recorded worktree is absent and no active agent owns it. Old PathLocks had no durable Flow or ID.

The living then directly ordered deployment. The three exact stale names were released through the 0.24 client, the transient 0.24 Nexus was stopped, and the candidate preflight returned zero rows. The managed 0.25 Orchestrate Nexus is active with both sockets. Live proof passed Lock ID 1, Observe.Locks, Release by ID, and an empty final observation.

The recorded deployment order required the independent CriomOS Lojix ownership-gate repair before Home activation. That repair landed as CriomOS `be56867a2ed6a640b443a91f765b4b8c32d8ed83`; it pins Orchestrate `e0f3bc5e8b963089e560383b2a4eb7d30cda1f82`. Cross-subflow work is tracked as CriomOS-6ez.

The live Lojix ledger already records deployment 72 as Current/LiveActivation for immutable CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103`, which retains that same Orchestrate pin. No redundant activation was submitted. The managed unit is active with a `...-orchestrate-0.25.0/bin/orchestrate-nexus` ExecStart and both sockets. The final live contract witness acquired Lock ID 4, observed it, released it, and observed an empty snapshot.

Remembered: 01a03eda — depth 1. Its report and final responses establish the preflight branch and exact candidate Home revision.
