# Receipt: ground for the Psyche successor plan (8904b1, dc53b4, 38f337)

Gathered read-only by a subflow of 8904b1, 2026-09-26 ~20:20–20:35 CST (UTC-6).
Nothing was launched, prompted, sent, bound, or started. The only reads that touched live
seats were `herdr pane read <pane> --lines 8` on w1:pC, w1:pF and w1:p8.

## Live queries (observed)
- `flow --version` = `flow 0.12.2` (nexus pid 1937, `/nix/store/c044v5pa…-flow-0.12.2`).
  `flow-next --version` = `flow 0.17.0` (client); the running next nexus is pid 90750,
  `/nix/store/zscrhhfy…-flow-0.17.1/bin/flow-nexus`. `claude --version` = 2.1.280. `herdr` 0.8.2.
- `flow 'List.{}'` rows:
  - `8904b1 8904b10d-7f06-4e44-9342-3a8a2d7e17bd Claude Unavailable Available.{ default psyche_fable_b7ba00 w1:p8 term_65c6b8fc88ee08 } { 8904b1 … unavailable } Active`
  - `dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 Claude Unavailable Available.{ default psyche_opus_dc53b4 w1:pC term_65c6bcb737eabc } { dc53b4 … unavailable } Active`
  - `38f337 38f33758-72c0-4c2a-ad49-8ffeb8e310fa Claude Unavailable Available.{ default psyche_sonnet_9c7514 w1:pF term_65c6be9c29098f } { 38f337 … unavailable } Active`
  - Every other Claude row (38de5b, 88475f, b860be, d8df70, da88cf, e167d8, e51411) is also endpoint `Unavailable`.
    Codex rows 139366, 184bd8, 22e12b, 5f38bc, 9ac67c have `Available.{ /home/li/.codex-next/app-server-control/app-server-control.sock Ready }`.
- `flow-next 'List.{}'`: dc53b4 also present there (`{ dc53b4 default meta-bind-existing } Active`, endpoint Unavailable). 8904b1 and 38f337 absent from flow-next.
- `hm-list`: `8904b1 psyche_fable_b7ba00 default working`; `dc53b4 psyche_opus_dc53b4 default done`; `38f337 psyche_sonnet_9c7514 default done`.
- `herdr session list`: default running; recovery-56ae53 running; messaging-build stopped.
- `herdr agent list` titles: w1:p8 `PsycheV2.{ Fable 8904b1 }`, w1:pC `PsycheV2.{ Opus dc53b4 }`, w1:pF `PsycheV2.{ Sonnet 38f337 }`. One Sonnet only.

## Processes (observed, /proc)
- 110690 (parent zsh 110561), started 17:55:03: `claude --session-id 8904b10d-… --model claude-fable-5-1 --effort medium --name "Psyche Fable (claim pending)" --remote-control --dangerously-skip-permissions --system-prompt-file /home/li/wt/primary/56ae53/tools/main-flow-mode/system-prompt.md --settings ~/.claude/jobs/native-8904b10d-…/main-flow-settings.json`
- 128289 (zsh 128160), 18:11:44: same shape, `--model claude-opus-5-5`, cwd opus-sonnet-56ae53, job dir `native-dc53b4be-…`.
- 136885 (zsh 136762), 18:20:13: same shape, `--model claude-sonnet-5 --name "Psyche Sonnet 5 (claim pending)"`, job dir `native-38f33758-…`.
- Env of all three: `CLAUDE_JOB_DIR=~/.claude/jobs/native-<uuid>`, `HERDR_PANE_ID` as above. No `claude --bg`, no daemon.

## Claude daemon (observed)
- No daemon process. `/tmp/cc-daemon-1001/a88e833a/` holds `pty rv spare`, no `control.sock` (dir mtime 10:14).
  `rv/9993b5f1.sock` is a leftover from Sep 17.
- `~/.claude/daemon.log` last line: `[2026-09-26T16:14:24.228Z] [supervisor] shutting down (cause=signal, uptime=1106154s, leases=0, live_workers=4)`
  = 10:14 CST. Previous boot ended 16:12:34 CST (`journalctl --list-boots`); current boot 16:18:50 CST.
  So the daemon stopped about six hours before the power failure, by a signal of unknown origin.
- `~/.claude/daemon/roster.json` updatedAt 2026-09-19 14:02 CST, 4 workers (942914a6, 840e42bb, efa15708, 9993b5f1), none a current seat.
- `claude daemon --help`: "Service install is disabled in this version — the daemon runs on demand and exits when the last client disconnects." Subcommands run/status/logs/uninstall/stop.
- `claude --help`: `--bg … With --resume <session-id>, continues that session in the background under the same ID, or starts a copy and says so when the session is already running`; `attach <id>` "Open a background session".

## Flow source (flow 0.17.3 at ~/wt/github.com/LiGoldragon/flow/release-0173-56ae53)
- `crates/flow-nexus/src/claude.rs`: Claude endpoint = daemon `control.sock`; `Ready` only when `~/.claude/jobs/<short>/state.json` backend=daemon, roster worker with live replPid and rendezvous sock, and control.sock exists. Otherwise `Parked`, or `Unavailable` if stored Unavailable.
- `crates/flow-nexus/src/launching.rs` ~l.151: Flow `Start` builds the node with `endpoint_selection: EndpointSelection::Unavailable` and a Herdr route. Replace/reap (l.495–530): records predecessor `Stopped`, closes its pane if present, then releases the successor.
- `lib.rs` l.146–161: `Restart` always `RestartRejected(ResumeRefused)`; comment "Refresh uses a fresh typed Start until the replacement contract is deployed."
- `delivery.rs`, `store/delivery.rs`: zero references to endpoint. UPGRADES 0.12.2: "nothing on the ResolveRecipient or Send path consults the endpoint" (stated for Codex).
- README: `flow-meta register-claude … [daemon-control-socket]` registers existing *daemon* sessions.
- No role-uniqueness rule found (grep for DuplicateRole/RoleOccupied etc.: none).

## Launch records
- Fable: `flows/56ae53/fable-recovery/state-recovery-v2.json` seat phase `failed`, error `ValueError: single native first prompt must be smaller than 20 KiB`; receipts incl. `psyche_fable_b7ba00.v2.native-bootstrap.json`.
- Opus: `/home/li/wt/primary/opus-sonnet-56ae53/flows/56ae53/opus-recovery/state.json` phase `failed`, `herdr … agent_not_ready … blocked during startup`; no receipts dir.
- Sonnet: `…/sonnet-recovery/state.json` phase `failed`, same 20 KiB ValueError; `receipts/` holds only `psyche_sonnet_9c7514.manifest.json` (the referenced `psyche_sonnet_9c7514.json` is absent). Manifest role `Psyche Low`, effort medium, predecessor 9c7514.
- All three transcripts open with a `<pasted_content>` main-flow first prompt; the first-prompt submitter for Opus/Sonnet is not identified here.

## Transcripts / context (observed, last main-thread usage)
- 8904b1: `~/.claude/projects/-home-li-wt-primary-56ae53/8904b10d-….jsonl`, 1,596,052 B, ≈207.4k tokens at 02:31Z; status line `ctx 21%`.
- dc53b4: `…/-home-li-wt-primary-opus-sonnet-56ae53/dc53b4be-….jsonl`, 790,769 B, ≈121.8k at 01:41Z; `ctx 12%`. Composer holds unsent `yes, check remote access`.
- 38f337: `…/38f33758-….jsonl`, 460,572 B, ≈82.0k at 01:42Z; `ctx 8%`. Composer holds unsent `yes, resend to Mind Luna 139366`. No Skill-tool loads.
- Refresh skill text (read as evidence only; not loadable through the Skill tool): refresh at sixty percent; do not restart below twenty percent for a non-dramatic change.

## Records (observed, jj)
- dc53b4: `/home/li/primary/flows/dc53b4` (log.md, receipts, reports) — in `@` of `/home/li/primary`, 3 files, not described/committed.
- 38f337: `/home/li/wt/primary/opus-sonnet-56ae53/flows/38f337` (handoff.md, log.md, mind-sol-of-56ae53.profile.json, proposed-launcher-authorization.patch, successor-prompt.md) — in `@`, 5 files, uncommitted.
- 8904b1: `/home/li/wt/primary/56ae53/flows/8904b1` — 20 files in `@`, uncommitted.
