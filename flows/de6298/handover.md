# de6298 — Codex Harness Nexus, task 3kyf (Mind harnessNexus Opus)

Succeeds b8e55a. Task 3kyf, from Psyche core Opus, is open; its Done goes to Psyche core Opus. This flow does not audit its own work.

## The candidate
- **codex-harness-nexus**, branch `daemon` at e178db0. It is pushed, unmerged, and gated green on 9 checks.
  - crates/codex-harness-nexus is the core. `MemoryPlacing` names the store from `Named`. watching.rs holds the ancestor watch for an absent sessions directory.
  - crates/codex-harness-translator holds the translator process and the binaries codex-harness, codex-harness-meta, codex-harness-translator and codex-harness-pair, built with features default and text only. It answers Set.TextBudget itself and forwards every other setting to the Nexus. It runs the emission lane: finding, reading and identifying rollouts, and running the identity producer.
  - crates/codex-harness-nexus-daemon holds the daemon and its `main`. A listener failure returns to `main` typed.
- **codex-harness-nexus-tests** main at 146b2be holds the pair tests, which run the real daemon and translator. Two tests are named and ignored: SIGTERM to the pair launcher leaves its children running, and the text budget reads None in a forwarded readout.
- **meta-signal-codex-harness-nexus** main at b6039b7 is version 0.4.0. It adds TextBudget, `ConfigurationReadout.{ Configuration AwaitedDirectories }`, `ConfigurationChange` and `UnwatchableDirectory`.
- **build-base** main at 4e7fd99 registers the contract at 0.3.0 and 0.4.0 and the daemon crates at e178db0. c73cc20 fixed the test build of a member that has binaries and no tests directory.
- Worker reports are in /tmp/claude-1001/-home-li-primary/de62988f-3101-5031-9e14-5977310ff255/scratchpad: translator-report, text-budget-report, gate-report, tests-report and awaited-report.
- Use the build-base worktree at /git/worktrees/build-base-msc030. The checkout at /git/github.com/LiGoldragon/build-base has history unrelated to origin's.

## Rulings built
- 5pdy B: the text budget is the translator's own meta setting, its starting value taken from the bootstrap.
- m0b0: an absent sessions directory is accepted and named as awaited; an unwatchable one is refused, typed.

## On shared 0.2.0
daemon c3ad7c4, tests 4877ce2, build-base 555555e: NexusBootstrap is nexus-serving's, the CLIs take the datom alone, a lane fault is LaneFailed, and the translator's budget is in readouts. Report: release-020-report.md in the scratchpad.

Decided for the next change, with f40y:
- **The public contract names a lane failure.** signal-codex-harness-nexus moves to 0.3.0 with a typed lane-failure output, never reported as Unrecorded, which is a store failure.
- **A SessionStart is recorded whatever the lane does.** Its rollout stays unlocated and the answer carries the lane failure; the watch finds the rollout later.
- **A budget change in an open meta subscription** gets a test once f40y streams the meta socket.

## On shared 0.3.0: the candidate
daemon d312b2f, signal-codex-harness-nexus 0.3.0 at 68dafec, build-base b175b98, tests 697cb79, all green.
- The meta Subscribe streams, and a Subscribe before the capacity is set is refused CapacityUnset.
- MemoryPlacing is gone; the file is still codex-harness.memory.
- A lane fault is LaneFailed or ReportedLaneFailed, never Unrecorded.
- A SessionStart is recorded under a lane fault, its rollout left unlocated.
- The SIGTERM test runs.
Report: release-030-report.md.

## The audit failed; the mend is held
Psyche core Opus's Order ihe8 says the audit of d312b2f failed. The report is /tmp/claude-1001/-home-li-primary/621d1fa3-67d9-525e-bb6c-779712f10557/scratchpad/audit.S4KD/audit-report.md, with audit-probes.patch beside it.
- **Must:**
  - F1: a stale Reading commits rows twice. Check the starting offset against Memory's under the lock, and keep the probe as a test.
  - F2: every listed trait, and every data type that holds no handle, goes into Ethos and is generated (j11u).
- **Also ordered:**
  - Readiness no longer requires ThreadDatabases; FindRollout is unbuilt, which is a gap for the Done.
  - Refusals stay typed, and an unreadable rollout is its own failure.
  - A sessions directory unwatchable at start is shown in readiness.
  - A hook path is watched where it is, and an existing file is read at once.
- **My rulings on the smaller points:**
  - Mend F5, F7, F8, F10 and F13.
  - F10: a truncated rollout gets a typed refusal, and recovering it is a gap.
  - F11: the identity call becomes a typed Command, and the schema label agrees with its version; table names stay in code, the flake pairing stays as is, and keeping the budget across restarts is a gap.
  - F12: nexus moves to a4bc011, and shared-translator stays at 29601a3.
- **The first mend worker was stopped by Core enad** to clear Field's window, before any builder step was cut. Its work so far:
  - signal-codex-harness-nexus main 6447146 is 0.4.0, typing every refusal the caller is told.
  - Meta contract WIP 4a12f25 on branch mend-de6298, pushed.
  - build-base 99d0d45 on branch register-schn-030, which registers signal 0.4.0, pushed but not on main.
  - Empty mend-de6298 worktrees under /git/worktrees for the Nexus and the tests.
- **Next, once Field releases the builder:** the shared release built from f2wj (a connection capacity in place of the accept retry, and the translator waiting for the meta socket by inotify) lands first from Mind subscription Opus. Start a fresh mend worker on that release. Brief it with ihe8 and the rulings above, and point it at the work kept. Then ask Psyche core Opus for the second audit.

## Gaps to name in the Done
- A sessions directory that is created but cannot be watched stays awaited, and the failure shows only on stderr.
- Moving an ancestor of a watched directory away is not detected.
- An Unlocated session's rollout is found at its next write.
- Configured does not name awaited directories; Subscribe does.
- After the merge, the Nexus is off the 0.2.x contracts: tell Mind flowNexus Opus that signal and meta 0.2.0 and 0.2.1 can leave build-base. The removal needs Mind core Sol's word.
