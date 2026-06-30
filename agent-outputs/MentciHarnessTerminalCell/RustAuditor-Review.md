# Rust Auditor Review

Task and scope: final audit for the Mentci/harness/terminal-cell orchestration thread. Scope covered `/git/github.com/LiGoldragon/harness`, `/git/github.com/LiGoldragon/terminal`, `/git/github.com/LiGoldragon/terminal-cell`, and `/home/li/primary/protocols/active-repositories.md` plus primary status only enough to decide whether user attention is needed. I did not edit repository source, commit, push, or run destructive commands.

## Findings

### High: duplicate transcript watches for the same harness can close the wrong stream and leave the requester hanging

Files:

- `/git/github.com/LiGoldragon/harness/src/subscription.rs:541`
- `/git/github.com/LiGoldragon/harness/src/subscription.rs:558`
- `/git/github.com/LiGoldragon/harness/src/subscription.rs:586`
- `/git/github.com/LiGoldragon/harness/src/subscription.rs:593`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:785`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:787`
- `/git/github.com/LiGoldragon/signal-harness/src/lib.rs:540`
- `/git/github.com/LiGoldragon/signal-harness/src/lib.rs:547`

Risk: the stream lifecycle fix handles same-stream unwatch and rejects nested watch on the same stream, but the manager still allows more than one open subscription with the same `HarnessTranscriptToken`. The token is only `{ harness: HarnessName }`; `signal-harness` documents that as "one observer per harness" and the token identity is the harness. `OpenTranscriptSubscription` creates the same token for every watch of the same harness, pushes every entry into `open`, and `CloseTranscriptSubscription` removes the first matching token.

Concrete failure shape: client A watches `operator`, then client B watches `operator`. Both streams hold the same token. If B sends `UnwatchHarnessTranscript`, B's stream accepts it because the token equals its local token, but the manager removes the first matching entry, which can be A. The final acknowledgement is delivered to A's sink, A's stream closes, and B's stream waits without its final ack. This also leaves B's subscription open until a later close/error path. That violates the same-stream final-ack contract the commit was meant to fix.

Expected correction: choose and enforce one invariant. Either widen `HarnessTranscriptToken` in the wire contract with a per-open subscription identity and update round trips, or keep "one observer per harness" and reject/replace a second watch for the same harness before registering a second handler. Add a daemon/integration witness that opens two independent streams for the same harness and proves the second watch is rejected or that each stream's unwatch closes only itself.

### Low: harness architecture names stale flake checks for the transcript stream witnesses

Files:

- `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:302`
- `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:303`
- `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:304`
- `/git/github.com/LiGoldragon/harness/flake.nix:124`
- `/git/github.com/LiGoldragon/harness/flake.nix:125`
- `/git/github.com/LiGoldragon/harness/flake.nix:126`
- `/git/github.com/LiGoldragon/harness/flake.nix:127`

Risk: `ARCHITECTURE.md` points operators at `.#harness-daemon-pushes-transcript-deltas-after-subscribe`, `.#harness-daemon-emits-final-subscription-retracted-ack`, and `.#harness-daemon-slow-subscriber-does-not-block-siblings`. Those check names do not exist in `flake.nix`; the actual new checks are `.#harness-daemon-watch-transcript-returns-typed-snapshot`, `.#harness-daemon-unwatch-transcript-returns-final-retraction-ack-on-subscribed-stream`, `.#harness-daemon-watch-transcript-stream-delivers-published-observation-and-final-ack`, and `.#harness-daemon-rejects-nested-watch-without-leaking-subscription`.

Expected correction: update the witness table to the current flake check names, and either add a check for duplicate same-harness watch behavior or explicitly document the one-observer-per-harness invariant.

## Non-Blocking Observations

No blocking findings in the terminal archive wording. `terminal` clearly says archived/inactive in `AGENTS.md:8`, `ARCHITECTURE.md:6`, `INTENT.md:7`, and `README.md:5`; it directs V1 harness Claude/Codex tests to `terminal-cell`.

No blocking findings in `terminal-cell` active-primitive wording. `terminal-cell` describes itself as the active low-level primitive for V1 harness work in `AGENTS.md:8`, `ARCHITECTURE.md:52`, `INTENT.md:7`, and `README.md:7`, while keeping higher-level Persona session ownership and policy out of scope.

`/home/li/primary/protocols/active-repositories.md` is consistent with the intended map: `terminal-cell` is active at line 32 and explicitly not subordinate to `terminal`; `terminal` is in Inactive / Archived Components at line 89. Primary remains a dirty/open working-copy change with a broad unrelated batch, so a lead decision is still needed before committing anything there.

## Checked Evidence

Repository status:

- `/git/github.com/LiGoldragon/harness`: clean working copy. `main` at `f625c2bed0c6d64bec27d2afd4d4b564eaf2350e` (`harness: fix transcript stream lifecycle`). `jj show` reported bookmarks `main main@git main@origin`.
- `/git/github.com/LiGoldragon/terminal`: clean working copy. `main` at `2c514171c052ae6785df36d83dec76f5492a586c` (`terminal: mark owner docs archived`). `jj show` reported bookmarks `main main@git main@origin`.
- `/git/github.com/LiGoldragon/terminal-cell`: clean working copy. `main` at `f95d988e21c00271fbc138897bf7b9b42ef3a846` (`terminal-cell: mark active V1 primitive`). `jj show` reported bookmarks `main main@git main@origin`.
- `/home/li/primary`: `jj status` reports many working-copy changes in doctrine/agent surfaces and reports; `jj diff --stat` reports `0 files changed`, so the batch is in the open working-copy change rather than a small unstaged registry-only edit.

Commands run:

- `jj status` in harness, terminal, terminal-cell, and primary.
- `jj bookmark list` in harness, terminal, and terminal-cell.
- `jj show --stat -r f625c2be` in harness.
- `jj show --stat -r 2c514171` in terminal.
- `jj show --stat -r f95d988e` in terminal-cell.
- `jj log -r 'main | main@origin | main@git' --no-graph --template ...` in harness, terminal, and terminal-cell.
- `sed -n '1,220p' protocols/active-repositories.md` and `nl -ba protocols/active-repositories.md | sed -n '1,120p'` in primary.
- `rg`/`nl -ba` inspections over harness `src/daemon.rs`, `src/subscription.rs`, `tests/daemon.rs`, `tests/subscription_truth.rs`, `flake.nix`, `ARCHITECTURE.md`, `AGENTS.md`.
- `rg`/`nl -ba` inspections over terminal and terminal-cell `AGENTS.md`, `ARCHITECTURE.md`, `INTENT.md`, and `README.md`.
- `rg`/`nl -ba` inspections over `/git/github.com/LiGoldragon/signal-harness/src/lib.rs` for token contract shape.
- `cargo test --test subscription_truth` in harness: passed, 7 tests.
- `cargo test --test daemon harness_daemon_watch_transcript` in harness: passed, 2 tests.
- `cargo test --test daemon harness_daemon_unwatch_transcript_returns_final_retraction_ack_on_subscribed_stream` in harness: passed, 1 test.
- `cargo test --test daemon harness_daemon_rejects_nested_watch_without_leaking_subscription` in harness: passed, 1 test.
- `cargo test --test message_router_harness_e2e` in harness: failed as expected with router-side `rkyv archive deserialization failed`; the test then panicked at `tests/message_router_harness_e2e.rs:67` with `expected SubmissionAccepted, got Error("router socket unreachable; message not forwarded")`.

## Questions And Suggestions For Psyche / Lead

1. Decide the transcript subscription invariant before the next provider slice: either one observer per harness, enforced at watch time, or per-open unique subscription tokens in `signal-harness`.
2. Treat `tests/message_router_harness_e2e.rs` as a separate router/message/harness compatibility task. The reproduced failure matches the known residual and should not block the transcript stream lifecycle commit, but it does block claiming full end-to-end router delivery health.
3. Decide whether primary's open working-copy batch should be committed as one doctrine/workspace change, split, or left for its owning lane. The active-repository map itself does not need a special clean commit for terminal archival wording unless the lead wants the whole primary batch landed.
4. For the next harness provider slice, add the duplicate same-harness watch witness first so provider work does not inherit ambiguous stream close semantics.
