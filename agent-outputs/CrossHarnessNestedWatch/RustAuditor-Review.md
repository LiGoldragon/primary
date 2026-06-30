# Rust Auditor Review

Task and scope: final focused audit for the cross-harness nested-watch fix in `/git/github.com/LiGoldragon/harness`, commit `81433075b7485de8eed91a29d4242b811f5288ba` (`harness: reject cross-harness transcript watches`). Scope covered final harness code, tests, docs, no subscription leaks, worktree cleanliness, and `main`/`origin` landing. I did not edit, commit, push, or run destructive commands in the harness repository.

## Findings

No blocking findings.

The scoped behavior is implemented in the live stream path:

- `src/daemon.rs:138`-`157`: the first `WatchHarnessTranscript` resolves the target harness instance and creates `HarnessTranscriptWireStream::new(harness)`, binding the stream to that first watched harness before opening the first subscription.
- `src/daemon.rs:708`-`785`: `HarnessTranscriptWireStream` stores `bound_harness: HarnessName` as stream state.
- `src/daemon.rs:936`-`945`: nested `WatchHarnessTranscript` requests whose `watch.harness` differs from `self.bound_harness` return `cross_harness_watch_event` and do not call `open_subscription`.
- `src/daemon.rs:850`-`857`: `cross_harness_watch_event` returns typed `HarnessEvent::HarnessRequestUnimplemented` with operation `HarnessOperationKind::WatchHarnessTranscript`.
- `src/daemon.rs:789`-`808`: subscription creation remains behind `open_subscription`, which is only reached for same-harness nested watches after the bound-harness guard.
- `src/daemon.rs:919`-`935`, `984`-`999`, and `1039`-`1042`: explicit unwatch and stream-error cleanup paths close tracked subscriptions; final acknowledgements remove subscriptions before stream termination.

Same-harness preservation and leak prevention have focused witnesses:

- `tests/daemon.rs:715`-`848`: `harness_daemon_allows_nested_watchers_for_same_harness_without_cross_closing` opens two watchers on one stream for `operator`, proves two distinct tokens receive the first observation, closes the first watcher without closing the second, then proves fanout drops to one and finally zero after both are closed.
- `tests/daemon.rs:851`-`942`: `harness_daemon_rejects_cross_harness_nested_watch_without_leaking_subscription` opens `operator`, attempts a nested `designer` watch, asserts typed `HarnessRequestUnimplemented`, then proves `operator` fanout remains `1` and `designer` fanout is `0`.
- `flake.nix:127`-`128`: both focused daemon tests are registered as named flake checks.
- `ARCHITECTURE.md:306`-`309`: the architecture witness table now names both same-harness nested watcher preservation and cross-harness rejection without subscription leakage.

## Residual Risks

The cross-harness rejection test proves no extra subscription is created on either the already-bound harness or requested harness by checking fanout counts. It does not publish again after the final unwatch in that same test, but the adjacent same-harness test covers final close fanout dropping to zero, and the cross-harness test joins the server after the final acknowledgement. I do not consider this a blocker for the scoped fix.

I did not run the separate `message_router_harness_e2e` test; the brief identified it as separate, and the audited patch does not touch that path.

## Verification

Commands consulted:

- `spirit "(PublicTextSearch [harness transcript watch])"`: returned `(Error [no matching record])`; no public intent record changed the supplied audit brief.
- `orchestrate "(Observe Roles)"`: observed no claim on `/git/github.com/LiGoldragon/harness`.
- `jj status` in `/git/github.com/LiGoldragon/harness`: clean before and after tests. Final output: `The working copy has no changes.` Working copy `8586cc59` is empty on parent `81433075`.
- `jj bookmark list --all`: `main`, `main@git`, and `main@origin` all point to `81433075` / change `pvozworw`.
- `jj show -r main --summary`: commit `81433075b7485de8eed91a29d4242b811f5288ba`; modified `ARCHITECTURE.md`, `flake.nix`, `src/daemon.rs`, and `tests/daemon.rs`.
- `cargo test --test daemon nested_watch -- --nocapture`: passed. Result: 2 passed, 0 failed, 13 filtered out.

One initial cargo invocation used two test-name filters and failed with Cargo's usage error before rerunning the correct single-filter command. That was command-form error only; no behavioral test failed.
