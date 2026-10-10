# Fork API architecture

Method: code read `/git/github.com/LiGoldragon/kameo/src/actor/lifecycle.rs`, `/git/github.com/LiGoldragon/kameo/src/actor.rs`, `/git/github.com/LiGoldragon/kameo/src/actor/actor_ref.rs`, `/git/github.com/LiGoldragon/kameo/src/actor/spawn.rs`, `/git/github.com/LiGoldragon/kameo/src/links.rs`, `/git/github.com/LiGoldragon/kameo/src/mailbox.rs`; comparison code read via `jj -R /git/github.com/LiGoldragon/kameo file show -r main@upstream root:<path>` and `jj ... diff --from 4d2e2d02 --to <head> --stat`

Observed code differences between fork `3486e4f6` and upstream `b4aaee79`:

- The fork adds public `ActorTerminalOutcome`, `ActorTerminalReason`, and `ActorStateAbsence`, backed by an internal `ActorLifecycle` `tokio::sync::SetOnce`. `ActorRef::wait_for_shutdown()` returns `ActorTerminalOutcome`; `is_terminated()` reports publication of that outcome. Upstream's same method returns `()` and waits on mailbox closure.
- The fork changes `Actor::on_link_died` to receive both `ActorTerminalOutcome` and legacy `ActorStopReason`; upstream receives only `ActorStopReason`. Fork supervision uses `ActorTerminalOutcome` for restart decisions and adds terminal classifications including `CleanupFailed` and `StartupFailed`.
- The fork changes `PreparedActor::run`, `spawn`, and `spawn_in_thread` results from `Result<(A, ActorStopReason), PanicError>` to `Result<ActorStopReason, PanicError>`; actor state is consumed/dropped during terminal teardown rather than returned.
- The fork's lifecycle publishes outcome only after `on_stop`, drops actor state before link notification, awaits link notification dispatch, unregisters, and sets the compatibility shutdown result. Startup failure publishes `StartupFailed`/`NeverAllocated`. Upstream keeps the older ordering and return shape, and has no equivalent terminal-outcome cell.
- The fork's mailbox has physically separate ordinary-message and unbounded control channels. Ordinary queued messages carry an atomic generation; shutdown closes admission and increments the generation, while biased receive/poll paths prioritize control and discard stale-generation messages. Upstream has one channel carrying all signals and an `accepting` atomic gate that rejects new messages after `stop_gracefully`; it does not have the fork's two-lane/generation design.
- Fork link dispatch is awaited inline through `Links::notify_links`; upstream schedules parent/sibling notifications with `tokio::spawn`. Fork `Link::notify` and remote signaling carry the terminal outcome.
- Upstream since the merge base has substantial unrelated evolution absent from the fork: package root version `0.22.2` versus fork `0.20.0`; `on_undelivered`; `ctx.pipe`/`ctx.pipe_with`; `ActorRef` single-`Arc` clone; lifecycle deadlock fixes; supervision drain behavior; `FutureActor`; console crate/TUI; tracing and error improvements. These are visible in the 65-file upstream diff from the common ancestor.

Diff statistics witnessed:

- Fork from merge base: 20 files, 2,117 insertions, 351 deletions.
- Upstream from merge base: 65 files, 8,014 insertions, 717 deletions.

## Sources

- Witness: `flows/fb50d4a5/witnesses/repositoryRelationship.md`
- `/git/github.com/LiGoldragon/kameo/src/actor/lifecycle.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/actor_ref.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/spawn.rs`
- `/git/github.com/LiGoldragon/kameo/src/links.rs`
- `/git/github.com/LiGoldragon/kameo/src/mailbox.rs`
- https://github.com/tqwewe/kameo/compare/4d2e2d02cc1ba59f05123d79f73eb47dd819ef92...main
