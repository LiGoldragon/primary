# persona-test message-flow: the Flow 0.17.4 live-start witness as a scenario

Subflow of 8904b1, 2026-09-27. Source work in my own clone of `git@github.com:LiGoldragon/persona-test.git` at `/home/li/wt/github.com/LiGoldragon/persona-test/message-flow-8904b1`. Two branches were pushed and main was not moved. No Flow, Message or Herdr process ran on the host outside a sandboxed Nix build. No seat was started. Nothing under a Claude configuration directory, and no credential, was read.

## Skills loaded through the Skill tool

All loaded: subflow, compensation-nix, nix-workflow, file-editing, edit-coordination, orchestrate, testing, testing-commit-scope, testing-push-landed, secrets, nexus, datom, herdr, claude-harness. Also psyche (CLAUDE.md), then flow-evidence before writing this report. None was read by any other route.

## Locks

- Lock 8200, `PersonaTestMessageFlowScenario8904b1`, flow 8904b1. It covered 13 paths. Reply: `Locked.{ 8200 PersonaTestMessageFlowScenario8904b1 8904b1 [ …13 paths… ] «Write the Flow 0.17.4 live-start witness scenario in persona-test on branch message-flow-0174-8904b1» }`.
- The successor needed two paths outside that set (`checks/message-flow-stand-in.nix`, `fixtures/herdr`), so I released 8200 and locked the full set again. Release reply: `Released.{ 8200 PersonaTestMessageFlowScenario8904b1 8904b1 [ … ] «…» }`.
- Lock 8263, `PersonaTestMessageFlowSuccessor8904b1`, flow 8904b1. It covered 15 paths. Reply: `Locked.{ 8263 PersonaTestMessageFlowSuccessor8904b1 8904b1 [ …15 paths… ] «Build the message-flow successor branch message-flow-0174-successor-8904b1 on main c1a2370» }`. Release reply: `Released.{ 8263 PersonaTestMessageFlowSuccessor8904b1 8904b1 [ … ] «…» }`.

## Branches, read back from the real remote (`git ls-remote git@github.com:LiGoldragon/persona-test.git`)

- `refs/heads/message-flow-0174-8904b1` is `b570bce4f25d955fbb17dbe0172a8d2460532dc7`, whose parent is e3505bfd. This is my original work, whole. It matches the local commit.
- `refs/heads/message-flow-0174-successor-8904b1` is `f9b50b7605613535e96bc1a5ccba127e06383ffd`, whose parent is c1a23704. This is the successor. It matches the local commit.
- `refs/heads/main` is `c1a23704537813764bf2c416544b87ec337d86d3`. My pushes did not move it. Neither commit on main is mine: c1a2370 was made by flow c56100's worker.
- Commit scope, from `jj diff -r @- --name-only`: the first commit holds 17 paths, the successor 19. Every path is one I edited, and no other flow's work was swept in.

## Checks and their true exits

1. `nix flake check --no-build` on the first tree: all checks passed.
2. Bounded `nix build` (2 jobs, 2 cores, cache.nixos.org only) of the package, `lint` and `message-flow-binaries`: **exit 1**. ShellCheck SC2329 flagged the no-op placeholder `beforeRootRemoval() { :; }` as never invoked. The claim relayed by the main flow was correct.
3. The fix: I removed the placeholder, and `cleanup` now calls `beforeRootRemoval` whenever a scenario defines one. Nothing was disabled or weakened. I reran once, under `systemd-run` with a 4G memory cap and a 1800 s limit: **exit 0**, and all three outputs are valid in the store. The remote builder was unreachable (SSH), so builds ran locally within those bounds.
4. Successor, `nix flake check --no-build` (4G, 900 s): all checks passed.
5. Successor, bounded build of `message-flow`, `lint`, `message-flow-binaries` and the new `message-flow-stand-in` (6G, 1800 s): **exit 0**. The stand-in check runs the runner in stand-in mode inside the build sandbox. Every case came out as expected, with list, stop, list, pane gone and process gone each time:
   - A (two lines): Started, oracle 13/13. The line break was kept, and the text sits in one entry.
   - B (a single line of 1206 bytes): Started, oracle 13/13. The prompt arrived wrapped.
   - C (one line): Started, oracle 13/13. The commands were stacked.
   - D (a skill that cannot load): `StartRejected.RegistrationRefused`. The transcript has no typed entry.
   - E (other model): not accepted (`PromptAmbiguous`). The oracle shows the model check stopped it.
   - F (footer dropped): not accepted. The oracle shows the footer check stopped it.
   - J (footer kept, body altered): not accepted. The oracle shows the prompt-hash check stopped it.
6. The same check with a deliberately wrong expectation for case E, left uncommitted and then reverted: **exit 1**, `cases failed: 1`, reason "the transcript first failed model, not footer-present". So the check has been seen red before its pass was trusted.

## What the scenario does, by outcome

1. **Its own world: written.** The root is `mktemp` under `/tmp`, or under an absolute `PERSONA_TEST_ROOT_BASE`. Every component starts under `env -i` with absolute paths, which are checked. Each socket path is checked against 107 bytes. Everything is removed on exit.
2. **Its own Herdr: written.** A headless `herdr --session persona-test server` with its own configuration, state and runtime directories. Every call names that session, and the server is stopped by its PID. The scenario never names the variable that marks a pane.
3. **Flow at the exact revision: written.** bc464e5e, client and service from one build. The sandbox run used the host's own store path `7z15aqi…-flow-0.17.4`. The client is always given this run's socket.
4. **Starts A, B and C: written.** Each is followed by list, typed stop, list, and a check that the pane and the process are gone.
5. **Oracle: written.** `fixtures/message-flow/oracle.py` finds the transcript on disk by session ID and checks: route, footer, a sha256 computed here against Flow's stored hash, the bundle copy, the first entry byte for byte, a single entry, the skill expansions in order, the receipt, the model, the effort, and the seat's launch flags from `/proc`.
6. **Must-fail cases: written.** D, E, F and J. The oracle names which check stopped each one. The plan's cases G, H, I and K are not written.
7. **Report: written.** It records command, revision and result for each case. It is written under the root and printed on exit.
8. **Stand-in: written, and it is the default mode.** It is not Claude, and it witnesses nothing about the harness. The source and README say so. In that mode the login projection is never called.

## Not reached

- The live forms were never run, as briefed: `live-claude`, which calls the login projection and adds Herdr's hook, and `live-codex`.
- In live-claude, cases E, F and J still use the stand-in.
- The stand-in's transcript shape comes from Flow 0.17.4's observer. A green stand-in run therefore proves the scenario's logic, not Claude's.
- There is no transcript oracle for Codex.
- Message 0.16 is started but not driven.

## Comparison with main c1a2370

- **flake.nix.** Both pin Flow bc464e5e. Mine also adds `harness` 0.3.4 (Home's revision, for `flow-id`, which Flow runs to claim a Flow ID) and `herdr` v0.8.2 (Home's revision). Main adds no Herdr input. The two agree on the Flow pin; they differ on where the tools Flow shells out to come from.
- **flake.lock.** Main relocked only `flow`. Mine also locks `harness` and `herdr`, and both follow nixpkgs.
- **lib/components/herdr.nix.** Main takes `nixpkgs.herdr`, which is 0.8.0 at this lock. It writes an isolated `XDG_CONFIG_HOME` holding a `codex_executables` allowlist, and exports that home into the runner's own shell. Mine builds v0.8.2 at Home's revision and starts a headless server under `env -i`, with separate config, state and runtime directories and the pane environment written out in full. It stops the server by PID.
  - Both isolate the configuration home. Main's allowlist key exists only in Herdr with Home's `codex-executable-selection` patch, and nixpkgs 0.8.0 does not have that patch.
  - The successor keeps one component: mine, because it isolates more (it never exports into the parent shell, isolates state and runtime too, and fixes the pane environment). It also applies Home's patch, copied to `fixtures/herdr/`, and takes over main's allowlist, which is empty unless a Codex client is given.
- **lib/default.nix.** Main adds only the `herdr` component entry. Mine adds the `herdr`, `flow-id` and `claude-stand-in` entries, and `shellHelpers` (absolute-path check, socket-length check, socket wait on a held PID). It moves the root to a short base and adds the cleanup hook. It also sets the model identifiers to the exact names Flow can put in a title (`claude-haiku-4-5-20251001`, `gpt-6-luna`). Main's `luna` and `claude-haiku-4-5` are unmapped, and Flow would refuse to title a start with either. The successor drops `isolatedComponentEnv`, which nothing uses any more.
- **packages/message-flow.nix.** Main runs one Codex start, then List, Stop, List, on an endpoint given from outside. It configures Flow with meta `Configure` followed by a restart. It attaches to Herdr through `script … session attach`, which is the TUI attach that is refused inside a pane. It exports HOME and XDG variables into its own shell. It has no transcript oracle, and it had no build behind it.
  - Mine is the full witness: A, B, C, D, E, F and J, with the oracle and the stand-in and live-claude modes.
  - Both refuse to run live without parameters from outside, and both use Start, List and Stop.
  - The successor keeps main's Codex drive as `live-codex`, with the same launch source `brief.md` checked by hash. The endpoint now reaches Flow as `FLOW_CODEX_*` deployment overrides at start, which Flow documents, instead of Configure plus a restart, and it runs on the shared isolated world.
- **README.md.** Main updates the scenario table. Mine documents the modes, the cases, the oracle, and that the stand-in is not Claude.

## Correction round, 2026-09-27: source only, written and not run

This round was done at flow c56100's word, relayed by the main flow. Nothing was built, evaluated, checked or run: no `nix build`, no `nix flake check`, no `nix eval`, no `nix run`, no `nix fmt`, no Python run of the fixtures. No shellcheck is installed on the host, so none was run.

The only commands run were two throwaway `bash -c` snippets under the host's own bash, unrelated to the scenario. They confirmed two bash behaviours. First, an EXIT trap that calls no `exit` keeps the exiting status (1 stayed 1), and a TERM trap that runs cleanup then `exit 143` runs cleanup exactly once. Second, `env -i bash` exports only PATH or LANG, plus PWD and SHLVL.

Every correction below is **written and not run**.

- **Lock:** 8352 `PersonaTestSuccessorCorrections8904b1`, flow 8904b1, over five paths. Reply: `Locked.{ 8352 PersonaTestSuccessorCorrections8904b1 8904b1 [ …/packages/message-flow.nix …/lib/default.nix …/lib/components/flow.nix …/fixtures/message-flow/oracle.py …/README.md ] «Source-only corrections on message-flow-0174-successor-8904b1 at the integration owner's word» }`. Release reply: `Released.{ 8352 PersonaTestSuccessorCorrections8904b1 8904b1 [ … ] «…» }`.
- **Commit:** `2edf366947e1604482df9aaf8041fd99ef755489`, parent `f9b50b7605613535e96bc1a5ccba127e06383ffd`. Its five paths, from `jj diff -r @- --name-only`: README.md, fixtures/message-flow/oracle.py, lib/components/flow.nix, lib/default.nix, packages/message-flow.nix. All five are mine.
- **Read back** with `git ls-remote git@github.com:LiGoldragon/persona-test.git`:
  - main `c1a23704537813764bf2c416544b87ec337d86d3`
  - `message-flow-0174-8904b1` `b570bce4f25d955fbb17dbe0172a8d2460532dc7`
  - `message-flow-0174-successor-8904b1` `2edf366947e1604482df9aaf8041fd99ef755489`

### The corrections

1. **live-claude refuses.** Written in `packages/message-flow.nix`, in the mode `case`. The form exits 69 with a message that the login route awaits the living's ruling. This happens before the root is made or anything starts, and the form keeps its name and place. `seatCredentialEnv` is removed from `lib/default.nix`, together with the real-mode seat branch and the hook installation. No code path reads a credential or writes a file holding a secret.
2. **Traps.** Written in `lib/default.nix` `isolatedStateRoot`. EXIT, HUP, INT and TERM are trapped; cleanup is guarded so it runs once, and drops errexit and nounset inside. On EXIT the status is kept; on a signal the run exits with 129, 130 or 143.
   - `beforeRootRemoval` stops by PID, in order: the held Flow client call (`heldPid`), the observer (`observerPid`), Flow, Message and Herdr.
   - Long Flow client calls now run backgrounded and are waited for through `held`, so a signal is handled at once.
3. **Case D pinned.** Written in `packages/message-flow.nix` and `oracle.py`. The oracle's `reply` command now reports the launch phases Flow sent. A new `skill-unavailable` check runs before the transcript checks.
   - D passes only on all of: `StartRejected.RegistrationRefused`, the phase `RegistrationAcknowledged` observed, the transcript present with no first entry (`first-entry-present` as the first failure), and the skill found in no catalog Flow reads.
   - Flow uses `RegistrationRefused` both for skill resolution and for intent acceptance. The README, a comment and the printed report say that Flow's answer alone does not prove the reason.
   - Two unrun risks: the phase check depends on the observer opening before the refusal, and a live Claude may write no transcript before its first prompt.
4. **Absent cases stated.** Written in the README and in the report's closing lines: G, H, I and K are not written, each described, "seven of the eleven".
5. **Route marked live-only.** Written in `oracle.py`: under the stand-in, the route check carries `live_only` and a detail suffix saying it tests the fixture's own rule. The README says the same.
6. **Worth in the printed report.** Written: a line in the report header and a line at its end, saying a stand-in run proves the scenario's logic and nothing about a real harness. The live-codex header states its own limits.
7. **Emptied environment.** Written at the top of the runner's text. It re-executes via `exec env -i` carrying only PATH (the runner's own inputs), LANG, the given PERSONA_TEST_* parameters, and the caller's HOME and XDG_RUNTIME_DIR under their own names. It then refuses if any exported name outside an allowlist survived. The pane marker is never named.
8. **Live paths refused.** Written after the root is made, before anything starts. The root and every derived home and runtime directory must be absolute, under the root, and not equal to or under any of: `/run/user/<uid>`, the caller's `XDG_RUNTIME_DIR`, `~/.local/state/flow`, `~/.config/herdr`. A refusal exits, and the trap removes the root.
9. **Flow's home.** Written in `lib/components/flow.nix`: `mkdir -p "$flowHome/.local/state/flow"` before start. The comment cites `crates/flow-nexus/src/main.rs` lines 25-26 and `store.rs` line 59 at bc464e5e, which show Flow creates it as well.
10. **live-codex claim.** Written: the README, the header comment and the report now say the form observes Flow's answers and that the pane is gone, and does not observe the Codex seat's process.
11. **Kept:** stand-in is the default and the only mode a check runs; the live forms are manual; there is one Herdr component; there is no `shellcheck disable`.

### Not done without running

- Formatting was not verified with nixfmt, and ShellCheck, statix, deadnix and Python compilation were not run. The build that would run them all needs a grant from Field.
- By reading I found no unused variable or function and no unquoted expansion. I cannot claim the ShellCheck gate passes, since it fails even on info-level findings.

## Sources

- `flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md`, with its amendment.
- `flows/8904b1/witnesses/flow-0174-fixture-and-baseline.md`; `flows/8904b1/witnesses/flow-0174-three-live-start-attempt.md`; `flows/8904b1/witnesses/flow0174-herdr-fixture-bringup-2.md`.
- Flow source at bc464e5e (`nix flake prefetch`): `crates/flow-nexus/src/{main.rs,store.rs,herdr.rs,herdr/launch.rs,launching.rs,composition.rs,title.rs}` and `crates/flow/src/main.rs`. signal-flow at 1c9e4b30: `src/generated/signal.rs` and `tests/contract.rs`.
- Herdr v0.8.2 source (the derivation's `src`): `src/main.rs`, `session.rs`, `config/io.rs`, `app/agents.rs`, `app/api_helpers.rs`, `detect/`, `terminal/title.rs`, and `integration/assets/claude/herdr-agent-state.sh`.
- harness at d0224279 (`Cargo.toml`); CriomOS-home `flake.nix`, `flake.lock`, `packages/herdr/default.nix`, and `patches/herdr/codex-executable-selection.patch` (read only).
- persona-test main c1a2370, read with `jj file show` and never checked out over my work.
- Build logs under the session scratchpad: `build1.log` (exit 1), `build3.log` (exit 0), `build4-mutant.log` (exit 1). Rerun 2's result was read from the store (`nix-store --check-validity`).
- Correction round: `jj diff -r @-` of 2edf3669 and the `git ls-remote` readback above.
