# Flow emission branch rebased onto main 1e931e43 (Flow 0.56.1)

## Result

- `emission-565bc8` (7 commits, head e69a3dd6 on 967f2f5) is rebased onto flow main 1e931e43. It is pushed to LiGoldragon/flow as `emission-565bc8-b`.
- New head: `0d39641be708b119e4676067eae09f45ecfa74f0`, a fast-forward of main's 1e931e43.
- Worktree: /git/worktrees/flow-emission-565bc8-b. `emission-565bc8`, `emission-e3a7d1`, main and everything live are untouched.
- **No conflict.** The rebase applied all seven commits cleanly. Nothing was resolved by hand, so no commit differs from its old counterpart in content, and no design choice was needed.

## Why it applied cleanly, checked

- Main's three fix commits and the release commit touch waking.rs, sending.rs, store/queue_delivery.rs, test_faults.rs, tests/unit/waking.rs, DESIGN.md, UPGRADES.md and the version files. The branch touches none of those hunks.
- The fix adds no hand-built herdr argv or process call. In its added non-test lines there is no `Command::new`, `.arg(`, `run_json`, `run_status` or `prompt_through_socket`, so nothing needed moving onto the typed emission. Its Codex code keeps its behaviour as written.
- A grep of `crates` after the rebase finds none of the removed helpers (`run_json`, `run_status`, `prompt_through_socket`, `PaneBound`, `ExchangesCurriculumFrames`). The remaining `run_git` is the handover archive's own runner trait, which the branch keeps.
- `capsule/`, `flake.nix` and `flake.lock` are byte-identical to main's. The head's Curriculum is main's, /nix/store/79zjg9f0iz9ljndlqnw6csv7bvyc7psc-rust_curriculum-0.1.0.

## Commits

| # | old (e69a3dd6 line) | new | gate |
|---|---|---|---|
| 1 | 3bf1b72d Herdr's command line | 49911b83 | not gated (no resolution) |
| 2 | 7e1ad0a2 Curriculum query | 1824f1f5 | not gated |
| 3 | 548e42bc flow-id claim | 5fcb3c25 | not gated |
| 4 | 301fdde0 harness command line | 5b2fa1de | not gated |
| 5 | 7ef65623 handover archive Git | eb3d1e08 | not gated |
| 6 | 91d9fcf3 Herdr socket prompt | 9bb61aa3 | not gated |
| 7 | e69a3dd6 pane shell line | 0d39641b | **exit 0**, flow-nexus 933 passed, 9 ignored |

The head was gated with the given command, by revision from github on prometheus. All checks of `checks.x86_64-linux` ran, flow-nexus (clippy and unit tests) and request-id-migration-process among them. Log: /home/li/primary/flows/565bc8/gate-emission-b-0d39641.log. The count is the 0.56.1 main's plus the branch's: 929 on 967f2f5 plus the fix's four tests.

Configured package of the head: /nix/store/1qblz7hqx5pd0fdnn5m0kq2fp0fcpjqq-flow-configured-0.56.1.

## Capsule

How it was run, as steps.md and the 0.56.1 run describe:
- Package: the head's configured-package above.
- Capsule: the head's capsule/ with /home/li/primary/flows/e3a7d1/capsule-scratch-fixes.diff applied in scratch. I checked that the scratch wrapper used for the 4fa6aba run (scratchpad/capsule-94bfd37) holds byte-identical flow-capsule and configure.datom to that patched capsule, so it was reused.
- Options: `--keep-going`, Codex included, FLOW_CAPSULE_WITNESS_DIR=/home/li/witnesses/565bc8. Before the run there was no capsule process and no /run/user/1001/flow-testing.

**Run 1 (full):** exit 1, **8 of 22 passed**, wall 1163 s, teardown clean.
- Passed: 0, 1, 2, 5, 8, 10, 11, 12.
- This equals the 0.56.1 branch's result of 7/22 plus scenario 5 on its rerun. Scenario 5 passed in the first full run this time (the race went the other way). It shows `Refresh: RefreshQueued, Send: SendAccepted Queued`.
- **No scenario that passed on the 0.56.1 branch fails here.**
- Every failing scenario failed on the 0.56.1 branch as well: 3, 4, 6, 7, 9, 13 to 20.
  - Replies are the same for 3, 4, 6, 7, 9, 16, 17, 18 and 20.
  - Scenario 18 fails the same way as before: the Codex session lacks Tag c1 within 120 s.
- **One reply changed, scenario 19 (Codex and Claude exchange a Task).** On the 0.56.1 branch the Task answered `SendAccepted Queued`. Here it answers `Sent.42pv`, and the Nexus log reads "flow woke; its first prompt carried 1 requests, their receipt awaited". The capsule then reads the request id from a `SendAccepted.{ id … }` datom, finds none in `Sent.<id>`, and sends a malformed Done (`exit 2: Arity { expected: 2, found: 1 }`). It failed before and fails now, so it is not newly failing.
- The Nexus log shows `send tool invocation Refused` four times in the window after that wake. The 0.56.1 branch's log has none. I did not investigate.

**Run 2 (rerun of 0, 18, 19, for scenario 19's changed reply):** the same. 18 fails as before; 19 answers `Sent.zih4`, with the same malformed Done, same Nexus line "first prompt carried 1 requests", and no `send tool invocation Refused` this time. Clean teardown.

My reading, not proven: the Codex wake of scenario 19 is what 0.56.1 fixed, and it now carries its batch (the answer is `Sent`, not a store refusal). In the 0.56.1 run the Codex seat was still Awake from scenario 18, so the Task there was queued. The capsule script does not accept `Sent` for it. Which of the two was the seat's state in each run was not checked.

Logs, all in /home/li/primary/flows/565bc8/:
- capsule-emission-b-0d39641.log and .nexus.log, witnesses /home/li/witnesses/565bc8/capsule-0.56.1-20261114T105748Z.
- capsule-emission-b-0d39641-s19-rerun.log and .nexus.log, witnesses /home/li/witnesses/565bc8/capsule-0.56.1-20261114T111732Z.

## Left as before

The remaining Emission families (Codex app-server, Herdr event stream, Claude settings document) wait on Fable, as in /home/li/primary/flows/e3a7d1/reports/flow-emission.md.
