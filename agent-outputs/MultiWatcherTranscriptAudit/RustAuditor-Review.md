# Multi-Watcher Transcript Subscription Audit

Task: final follow-up audit for the multi-watcher transcript subscription change in:

- `/git/github.com/LiGoldragon/signal-harness` main `959b62bd` (`signal-harness: add transcript subscription identity`)
- `/git/github.com/LiGoldragon/harness` main `b52be9e2` (`harness: allow multiple transcript watchers`)

Scope reviewed: subscription identity correctness, wire compatibility implications, token semantics, manager lifecycle, stream behavior, tests, docs, working-copy cleanliness, and main/origin landing state. I did not edit either repository, commit, push, or run destructive commands.

## Findings

### Medium: nested watch requests for a different harness on an existing transcript stream are misrouted through the first harness instance

Paths:

- `/git/github.com/LiGoldragon/harness/src/daemon.rs:138`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:153`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:854`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:925`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs:787`

`HarnessEngine::handle_transcript_stream` resolves the first `WatchHarnessTranscript` to one `HarnessInstance` and then calls `HarnessTranscriptWireStream::serve(stream, instance)`. During that same accepted stream, later `WatchHarnessTranscript` requests are handled by `HarnessTranscriptWireStream::handle_request`, which calls `self.open_subscription(received.exchange, watch, instance)` using the already-bound instance, without checking whether `watch.harness` still names that instance.

Effect: same-harness nested watchers are correct, but a later `WatchHarnessTranscript { harness: B }` sent on a stream initially opened for harness A can create a token whose `token.harness` is B inside A's subscription manager. Publications for B go to B's instance and will not reach that subscription; publications for A can be fanned to the B-named token, producing a stream frame whose token identifies one subscription while the `TranscriptObservation.harness` identifies another.

Expected correction: either resolve each nested `WatchHarnessTranscript` through `HarnessEngine` / `BoundHarnessInstances` by `watch.harness`, or reject nested watches whose harness differs from the stream's bound instance with a typed reply. Add an integration witness that opens harness A, then attempts to open harness B on the same accepted connection, and proves the chosen contract: successful B delivery from B only, or typed rejection.

This is not blocking for the explicitly claimed same-harness multi-watcher behavior, but it is a public contract edge because `WatchHarnessTranscript` carries a harness field and the daemon now accepts additional watch requests on an already-open stream.

## Non-Blocking Observations

- The main same-harness behavior is implemented as claimed. `signal-harness/src/lib.rs:555` defines `HarnessTranscriptSubscriptionIdentifier`; `signal-harness/src/lib.rs:574` makes `HarnessTranscriptToken` carry both `harness` and `subscription`; `signal-harness/src/lib.rs:598` puts the full token in `HarnessTranscriptSnapshot`; `signal-harness/src/lib.rs:610` echoes it in `HarnessSubscriptionRetracted`; and the stream declaration at `signal-harness/src/lib.rs:661` names `HarnessTranscriptToken` as the stream token type.
- The subscription manager mints per-open identifiers and keeps siblings distinct. `harness/src/subscription.rs:544` creates the next `HarnessTranscriptSubscriptionIdentifier`, `harness/src/subscription.rs:547` builds the token, `harness/src/subscription.rs:551` returns that token in the snapshot, and `harness/src/subscription.rs:565` registers each token/handler pair.
- Close semantics for open same-harness siblings match the claim. `harness/src/subscription.rs:593` looks up the exact token, `harness/src/subscription.rs:600` removes only that entry, and `harness/src/subscription.rs:601` asks only that handler to emit the final ack. The daemon removes only the acked token at `harness/src/daemon.rs:873`.
- Stream event token hardcoding was removed. `harness/src/daemon.rs:994` frames `SubscriptionEvent` with `token: Self::subscription_token_inner(token)`, and `harness/src/daemon.rs:848` derives `SubscriptionTokenInner` from `token.subscription.into_u64()`.
- Wire compatibility impact is real but appears intentionally versioned in the contract repo: `signal-harness/Cargo.toml:3` is `version = "0.2.0"`, and canonical NOTA changed from a harness-only transcript token to `(designer 1)` in `signal-harness/examples/canonical.nota:28`, `:82`, and `:85`. `harness` consumes `signal-harness` from git `main`, so the two pushed mains are synchronized.

## Residual Risks And Questions

- `message_router_harness_e2e` was not run. This matches the known separate residual router/rkyv failure and remains out of scope for this audit.
- The architecture claims a slow subscriber cannot block siblings (`harness/ARCHITECTURE.md:247`). The actor-level witness covers bounded sink overrun, and separate accepted connections should isolate socket writers, but siblings on the same accepted connection necessarily share one socket writer in `HarnessTranscriptWireStream::serve` (`harness/src/daemon.rs:854`). Clarify whether "sibling" means separate accepted streams, or add a stronger wire-level slow-writer witness.
- `TranscriptSubscriptionManager` uses `saturating_add` for `next_subscription_identifier` at `harness/src/subscription.rs:546`. This is practically unreachable, but it means uniqueness is not mathematically preserved after `u64::MAX`; a wrapping/error policy would make the invariant exact.

## Checked Evidence

Repository state:

- `signal-harness`: `jj status` clean. `main`, `main@git`, and `main@origin` all point to `959b62bd signal-harness: add transcript subscription identity`; working copy `@` is empty on top of that parent.
- `harness`: `jj status` clean. `main`, `main@git`, and `main@origin` all point to `b52be9e2 harness: allow multiple transcript watchers`; working copy `@` is empty on top of that parent.

Focused verification run with temporary `CARGO_TARGET_DIR` paths outside the repos:

- `/git/github.com/LiGoldragon/signal-harness`: `cargo test --test round_trip transcript -- --nocapture` passed: 4 passed, 0 failed.
- `/git/github.com/LiGoldragon/signal-harness`: `cargo test --test canonical_examples canonical -- --nocapture` passed: 3 passed, 0 failed.
- `/git/github.com/LiGoldragon/harness`: `cargo test --test daemon harness_daemon_allows_nested_watchers_for_same_harness_without_cross_closing -- --exact` passed: 1 passed, 0 failed.
- `/git/github.com/LiGoldragon/harness`: `cargo test --test subscription_truth -- --nocapture` passed: 7 passed, 0 failed.
- `/git/github.com/LiGoldragon/harness`: `cargo test --test daemon harness_daemon_watch_transcript -- --nocapture` passed: 2 passed, 0 failed.

Initial attempts to pass multiple independent test names to one `cargo test` command failed with Cargo usage errors; those were command-form errors only and were rerun with valid filters above.

## Audit Conclusion

No blocking finding for the claimed same-harness multi-watcher path. The final pushed state supports independent per-open tokens, snapshot-returned tokens, token-specific close ack, non-cross-closing same-harness siblings, and non-hardcoded stream frame tokens. The cross-harness nested watch route should be fixed or explicitly rejected before consumers rely on mixed-harness subscriptions over one accepted connection.
