# Orchestrate cutover recovery

The currently activated Home generation attempted the 0.25 Orchestrate Nexus and it exited with the exact safeguard that the old store contains three active PathLock rows. Systemd then reached its start limit and the ordinary socket disappeared.

The 0.25 zero-argument `orchestrate-upgrade-preflight` was run while the service was quiescent. It reported `active legacy PathLock rows: 3` and exited successfully. This chose the living-approved nonzero branch: 0.24 was started as the only `orchestrate-legacy-024.service` transient user unit. Its ordinary socket is present.

The deployed 0.24 client and wire contract contain only `PathLock` registration and `PathLockRelease`. They have no `Observe`/listing request. A safe duplicate-name probe used this flow's known held path as an overlap fallback: if a candidate name had been absent, the request would have received `PathOverlap` and made no row; for each stored candidate, its alphabetically prior duplicate-name check returned the exact holder. The three rows are:

- `claudeDesktopPinnedCli`, covering `modules/home/profiles/min/agent-intercom.nix`, `checks/agent-intercom-graphical-tui/default.nix`, and `flake.lock` in the removed `claude-desktop-pinned-cli-real` Home worktree.
- `claudeDesktopPinnedCliSupplement`, covering `overlays/claude-desktop.nix`, `overlays/default.nix`, `flake.nix`, and `ARCHITECTURE.md` in that same removed worktree.
- `claudeDesktopPinnedCliVersions`, covering `checks/ai-agent-launch-orchestration/default.nix` and `packages/claude-code/default.nix` there.

All originated in session `01a03e2c`; that session's final states the correction was pushed and the workspace closed. No `flows/01a03e2c` record exists, and 0.24 PathLock rows do not carry an owner Flow or numeric ID. The worktree is absent and no active agent owns it, so the rows are stale. The old release operation is name-only and cannot prove owner authority. The approved nonzero branch says restart 0.24 and abort, while the deployment task forbids releasing locks not owned by this flow; consequently no release occurred.

The independent CriomOS ownership repair is ordered before Home activation. Its current 0.25 client reaches the restored 0.24 socket but fails frame decoding, so it cannot acquire the authored `Lock`; the worker made no edit. This cross-subflow work is CriomOS-6ez. An explicit ruling is required to settle whether legacy coordination may be used for that separate repair or whether the ordering changes. Until then the 0.24 Nexus remains available for existing legacy work and the Home activation remains deferred.

The living subsequently ordered deployment. The exact 0.24 requests `PathLockRelease.{claudeDesktopPinnedCli}`, `PathLockRelease.{claudeDesktopPinnedCliSupplement}`, and `PathLockRelease.{claudeDesktopPinnedCliVersions}` each returned `PathLockReleased`. The transient 0.24 service was then stopped; the candidate preflight reported `active legacy PathLock rows: 0`; and the managed 0.25 service started.

The live 0.25 witness acquired `Lock.{cutoverVerification 01a03fe9 [/tmp/orchestrate-cutover-verification-01a03fe9] liveContractWitness}` as ID 1, observed that complete Lock, released it with `Release.{1}`, and observed an empty lock snapshot. The managed unit is active and both ordinary and meta Unix sockets exist.

The ordered CriomOS ownership repair then landed at `be56867a2ed6a640b443a91f765b4b8c32d8ed83`, with its focused ownership proof positive and its repair lock released. Its committed Nix source pins Orchestrate `e0f3bc5e8b963089e560383b2a4eb7d30cda1f82`. A current Lojix node-ledger query establishes that deployment 72 is already `Current` / `LiveActivation` for immutable CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103`; this Home revision retains the same 0.25 pin. Therefore no redundant Home activation was submitted and no regression to the older `f92c0834` candidate occurred.

Final live status is `active/running`. Its effective `ExecStart` is `/nix/store/mzhzz219qrfvr9ryp0vw5jp1wp160sgi-orchestrate-0.25.0/bin/orchestrate-nexus`, and both `/run/user/1001/orchestrate-nexus/orchestrate.sock` and `meta-orchestrate.sock` exist. The final ordinary-protocol witness acquired `finalDeploymentWitness` as Lock ID 4, observed the complete lock through `Observe.Locks`, released it through `Release.{4}`, and obtained `Observed(Locks(LockSnapshot { locks: Locks([]) }))`.

## Sources

- Flow `01a03eda`, `reports/orchestrateRealizationStatus.md`.
- 0.24 and 0.25 Orchestrate `UPGRADES.md` source and deployed client code.
- Live service status, journal, preflight, and transient-unit probes in this flow.
- `witnesses/orchestrateCutoverRecovery.md`.
