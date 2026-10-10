# Receipt: Flow 0.10.1 (briefed as 0.9.1)

Opus implementation subflow of Psyche High 38de5b, 2026-09-25.

## Landed

- LiGoldragon/flow main bbf5fa1 (0.10.0) to **0c19364** "Flow 0.10.1: absent predecessor pane is reaped; ETXTBSY-free fixtures; contract repins". After the push, `git ls-remote origin main` returned 0c193645eff1e736d7515c3ac19cd0931d64bd04.
- The work began at 28a78d2 (0.9.0), as briefed. Before the push, main had moved to bbf5fa1, "Flow 0.10.0: stacked Claude commands, native title after claim, no auto-mode offer". I rebased onto it. The conflicts were in the version lines, Cargo.lock and UPGRADES.md only.
- **Version: 0.10.0 to 0.10.1.** The versioning rule is that a change with no wire, storage or package-surface change is a patch. The Replace reap now succeeds in a case that used to be refused, which is a behaviour fix inside the existing vocabulary. The contract repins are wire-identical. The fixture changes are test-only. The brief's 0.9.1 could not land on a 0.10.0 main, so the patch goes on the current minor. The version is updated in `Cargo.toml` and `flake.nix`, and UPGRADES.md has a 0.10.1 section.
- Pins, following the coordinator's mid-task repin message (received before the push):
  - signal-flow **83171f3** (4.0.1).
  - meta-signal-flow **29ec97d** (6.0.2).
  - Both are regenerated on ethos-zero 13.0.0 with the wire unchanged. Cargo.lock swaps ethos-zero 10.0.0 for 13.0.0.
  - These replace the briefed 5ca97ce and f715883, so no 0.9.2 follow-up is needed.

## 1. Absent predecessor pane is already reaped

- `launching.rs` `reap`: after the predecessor is recorded `Stopped`, its route is refreshed.
  - If the route is still `Available` and `close` fails, the answer is `ReapRefused.CloseRefused`, as before.
  - If the pane is absent, nothing is closed. `Replaced` is recorded and the successor routes.
  - `ReapRefused.RouteUnavailable` is no longer produced by reap. A request that was stored as that refusal under 0.9.0 settles as `Replaced` when it is sent again.
- DESIGN.md is updated.
- New fixture `a_predecessor_whose_pane_is_gone_is_already_reaped`:
  - The Herdr stand-in's snapshot omits the predecessor pane, and its close would fail with status 1.
  - The fixture asserts `Replaced` with flow_id fac697, fac697 Stopped and not routable, and 908786 routable.
  - It asserts that LaunchStatus answers the same `Replaced`, and that no `pane close` call is made.
- Negative check: with the 0.9.0 `reap` restored, this fixture fails with `ReplaceRejected(ReapRefused(RouteUnavailable))`.
- `a_refused_reap_leaves_neither_flow_routable_until_it_is_retried` still covers `CloseRefused` on a pane that exists.
- **Caveat:** `refresh_route` cannot tell a pane absent from the snapshot apart from a failed Herdr snapshot call (Herdr unreachable), and both now count as reaped. The predecessor is still recorded Stopped, so it receives nothing. If Herdr was merely unreachable, its pane may stay open.

## 2. ETXTBSY fixture race

- **Cause:** `fs::write` in a multi-threaded test process holds a writable descriptor for the script. A fork on another test thread inherits it, and `O_CLOEXEC` closes it only at that fork's exec. An exec of the script inside that window fails with "Text file busy". Closing or syncing the file in the writing thread cannot close this window: herdr/launch.rs already called `sync_all` and still raced.
- **Fix:** new test-only module `crates/flow-nexus/src/fixture_executable.rs`, with `FixtureExecutable { path }` and the trait `InstallsScript::install(body)`.
  - The body is piped to a child `sh`, which writes `<path>.part`, runs chmod 700 on it, and renames it with `mv -f` onto the path.
  - The writable descriptor exists only in that single-threaded child, so no process ever holds the executable open for writing. The rename also replaces a rewritten script atomically.
- All eight script writers use it:
  - lib.rs: 4 sites.
  - herdr/launch.rs: 3 sites, including the codex-proxy fixture that 0.10.0 added.
  - codex.rs: 1 site.
- **A second, separate flake was found:** codex fake-proxy tests failed with a false `TimedOut` under load. `adapter_at` used a 100 ms timeout.
  - `adapter_at` now uses 5 s. The replies arrive at once, so the wider timeout costs nothing.
  - The timeout test uses 1 s, which is still under the proxy's 2 s silence.
- Evidence, with the lib test binary run directly at `--test-threads=16`, 200 times each:
  - Baseline 28a78d2: 19 of 200 runs failed. These include `Proxy("Text file busy (os error 26)")`, herdr-fixture failures and 3 fake-proxy timeouts.
  - After the ETXTBSY fix alone: 35 of 200 failed, all of them fake-proxy timeouts.
  - Final tree: 0 of 200 failed.

## Tests

- Before:
  - 28a78d2: 85 passed.
  - bbf5fa1: 94 `#[test]` sites (9 added upstream). This count is from `git grep`, not from a run.
- After, at 0c19364: 95 passed (6 flow, 3 flow-meta, 84 flow-nexus lib, 1 main, 1 default_start).
- `cargo test` run 20 times in a row on the final tree: 95 passed every time, 0 failures.
- `cargo clippy --all-targets -- -D warnings`: clean.
- `cargo fmt --check`: clean for the whole workspace. herdr/launch.rs was reformatted; it was not fmt-clean on main.
- **Nix was not built.**

## Lock

Orchestrate lock 6445 on the clone path, released.

## Sources

- /home/li/primary/flows/38de5b/receipts/g8-g9-nexus.md
- LiGoldragon/flow 28a78d2, bbf5fa1, 0c19364
- Clone: /tmp/claude-1001/-home-li-primary/38de5bbb-be48-4bae-883e-2d622fb79c9e/scratchpad/flow-091-opus-a7
