# Flow 0.59.1-recovery.1 — immutable recovery receipt

## Identity and authority

Published branch `recovery0591-2176a8` on github.com/LiGoldragon/flow at **19378d08e1c25b780e0d671bb45a3819a7fbccb7**. Fresh remote readback agrees; no main change or tag. Exact live ancestor is c0d51dc9765d5c9c6a69f63df56e1ea8f78bb280. Worktree /git/worktrees/flow-recovery0591-2176a8 is clean, continuing reservation390. Opus j2xu/6ac5 and Core9d3p/phce authorize recovery-first release after clean source audit and green fixtures. Feature0.59.2 is not published or gated by this receipt. Runtime remains Field-only after BOTH immutable candidates exist; this packet alone permits no deployment.

## Evidence

Scratch evidence directory: `/tmp/flow-recovery-3746e9.jDRrWc`.

- Auditor Mind harnessNexus Opus accepted production6ce6ad05, corrected fixturef6fddfad (u50k), and import-only874d4ce7 (aov4). Audit: `/tmp/claude-1001/-home-li-primary/1ce008f2-315e-51ac-9ceb-902d5b18abb4/scratchpad/ilj5-recovery-audit.md`.
- Source874d4ce7a0ed1cf0c8c594c299ceda322e4c2d49 full immutable Prometheus checks exit0: source-gate-2.log. Prior source-gate.log failed fixture compilation on missing Dispatches/ReadsLaunchAttempt imports; corrected before acceptance. Initial invocation used an invalid revision and failed before evaluation; source-gate-invocation-error.log retains it.
- Metadata19378d08 is four one-line version replacements: own manifest, flake bundle label, root Cargo.lock/Cargo.nix. Root metadata regenerated remotely with pinned b192e96 toolchain/crate2nix; crate-hashes unchanged. metadata.log and metadata-2.log are pre-write refusals (PATH cargo guard, locked old own version); metadata-3.log is successful generation. No dependency or feature change.
- Final19378d08 full immutable local-Git-source gate exit0: release-gate.log. Published GitHub exact-revision full checks also exit0: published-gate.log. Both use nix-fast-build --remote prometheus.goldragon.criome --no-nom --no-download --eval-workers1, checks.x86_64-linux whole.
- Flow check:1039 passed,8 ignored. All three new fixtures explicitly pass: opaque-family/exact Hold preservation and newer writes; wrong identity/schema refusal without writes on both store shapes; persisted global Hold across crash/reopen, startup cleanup deferral, registered NativeBound exclusion versus acknowledged live responder, refused Resume retains Held/debt, successful Resume completes cleanup once. Ignored/native scenarios are not claimed proved.

## Built package and native probe boundary

Build reference: `github:LiGoldragon/flow?rev=19378d08e1c25b780e0d671bb45a3819a7fbccb7#packages.x86_64-linux.default`.

Built on Prometheus, package.json/package.log: `/nix/store/21fp0cjp5rf6qz0smffywnmikn99x12q-flow-workspace-0.59.1-recovery.1`; derivation `/nix/store/9cy4psqsisf88mdl0mk0k545xh622rcv-flow-workspace-0.59.1-recovery.1.drv`. Its `bin/flow-nexus-daemon --version` answered exactly `flow-nexus 0.59.1-recovery.1`. The reserved label identifies this release/attribute; it is not a store basename. The package bundles daemon and matching clients/hooks. It is built, not installed or switched.

Core6p2r reports Opus ldv1 authorizes Field one disposable real Codex initialize/close probe after this built packet, before any switch. Source client invocation is the configured native executable followed by `app-server proxy --sock <isolated-private-socket>` (codex.rs501–506); it performs WebSocket upgrade then request1 `initialize` with params `{"clientInfo":{"name":"flow-nexus","version":"0.59.1-recovery.1"}}`, awaits result, and notifies `initialized` with null (codex.rs888–908). This is the exact candidate client operation, not a new Flow CLI subcommand. Field must verify the installed executable's supported disposable backend/proxy invocation, use private scratch/state/socket, and prove every process it starts is gone. No existing socket/session/process, Flow launch, provider/model request or runtime switch is authorized by this probe. Send receipt to recovery auditor. External native acceptance is still UNPROVED.

## Preserved pins and recovery route

Base b192e96a97b22b81f5edc09b8ddb439d05c4a4a3, ordinary64 83c04fefc087cf76dd3ca04792ff38b53b283b74, meta87 51008bc150ddae5db7d6ab2b4ceb692aa4cdf92b, and every other dependency/flake pin unchanged. Recovery accepts the exact two newer hold-family identities without decoding/registering them; it is not a per-address hold implementation. Field's eventual recovery must retain persisted global Hold until owner inspection and explicit Resume; Resume intentionally returns to0591 behavior and does not enforce feature per-address holds.
