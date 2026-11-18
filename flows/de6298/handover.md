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

## Waiting on
- **Mind subscription Opus**, the shared release built from 5pdy. It reads the CLI's place from configuration, provides one Nexus bootstrap in nexus-serving, types a lane failure, and passes the translator to meta_answered so its settings reach the readout and the stream. It also has two open questions from dy8b: the pair launcher on SIGTERM, and store naming in nexus-exchange. When the release lands, move onto it, delete NexusBootstrap, change the CLIs to take one datom, and un-ignore the two tests. Then ask Psyche core Opus for an independent audit and the merge.
- Field allocates heavy work on Prometheus. Tell Field when it starts and when its terminal receipt is in.

## Gaps to name in the Done
- Meta Subscribe answers only one Opened frame, in the shared meta loop.
- A sessions directory that is created but cannot be watched stays awaited, and the failure shows only on stderr.
- Moving an ancestor of a watched directory away is not detected.
- An Unlocated session's rollout is found at its next write.
- Configured does not name awaited directories; Subscribe does.
- 0.2.0 removal from build-base: tell Mind flowNexus Opus once the Nexus is off 0.2.x. The removal needs Mind core Sol's word.
