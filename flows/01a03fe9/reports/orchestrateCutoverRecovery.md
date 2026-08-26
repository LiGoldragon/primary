# Orchestrate cutover recovery

The currently activated Home generation attempted the 0.25 Orchestrate Nexus and it exited with the exact safeguard that the old store contains three active PathLock rows. Systemd then reached its start limit and the ordinary socket disappeared.

The 0.25 zero-argument `orchestrate-upgrade-preflight` was run while the service was quiescent. It reported `active legacy PathLock rows: 3` and exited successfully. This chose the living-approved nonzero branch: 0.24 was started as the only `orchestrate-legacy-024.service` transient user unit. Its ordinary socket is present.

The deployed 0.24 client and wire contract contain only `PathLock` registration and `PathLockRelease`. They have no `Observe`/listing request. A safe duplicate-name probe used this flow's known held path as an overlap fallback: if a candidate name had been absent, the request would have received `PathOverlap` and made no row; for each stored candidate, its alphabetically prior duplicate-name check returned the exact holder. The three rows are:

- `claudeDesktopPinnedCli`, covering `modules/home/profiles/min/agent-intercom.nix`, `checks/agent-intercom-graphical-tui/default.nix`, and `flake.lock` in the removed `claude-desktop-pinned-cli-real` Home worktree.
- `claudeDesktopPinnedCliSupplement`, covering `overlays/claude-desktop.nix`, `overlays/default.nix`, `flake.nix`, and `ARCHITECTURE.md` in that same removed worktree.
- `claudeDesktopPinnedCliVersions`, covering `checks/ai-agent-launch-orchestration/default.nix` and `packages/claude-code/default.nix` there.

All originated in session `01a03e2c`; that session's final states the correction was pushed and the workspace closed. No `flows/01a03e2c` record exists, and 0.24 PathLock rows do not carry an owner Flow or numeric ID. The worktree is absent and no active agent owns it, so the rows are stale. The old release operation is name-only and cannot prove owner authority. The approved nonzero branch says restart 0.24 and abort, while the deployment task forbids releasing locks not owned by this flow; consequently no release occurred.

The independent CriomOS ownership repair is ordered before Home activation. Its current 0.25 client reaches the restored 0.24 socket but fails frame decoding, so it cannot acquire the authored `Lock`; the worker made no edit. This cross-subflow work is CriomOS-6ez. An explicit ruling is required to settle whether legacy coordination may be used for that separate repair or whether the ordering changes. Until then the 0.24 Nexus remains available for existing legacy work and the Home activation remains deferred.

If the living later authorizes release by the completed row owner, the exact 0.24 requests are `PathLockRelease.{claudeDesktopPinnedCli}`, `PathLockRelease.{claudeDesktopPinnedCliSupplement}`, and `PathLockRelease.{claudeDesktopPinnedCliVersions}`. They were not sent.

## Sources

- Flow `01a03eda`, `reports/orchestrateRealizationStatus.md`.
- 0.24 and 0.25 Orchestrate `UPGRADES.md` source and deployed client code.
- Live service status, journal, preflight, and transient-unit probes in this flow.
- `witnesses/orchestrateCutoverRecovery.md`.
