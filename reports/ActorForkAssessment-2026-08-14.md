# Actor Library Fork Assessment

Date: 2026-08-14

## Identity

| Item | Value |
|---|---|
| Library | kameo (Rust actor framework) |
| Upstream | github.com/tqwewe/kameo |
| Fork | github.com/LiGoldragon/kameo |
| Local clone | /git/github.com/LiGoldragon/kameo |
| Fork base | upstream commit `4d2e2d0` (v0.20.0 era, the tip of upstream/main at time of fork) |
| Fork commits | 6 commits on top of base |
| Upstream HEAD | `b4aaee7` (49 commits ahead of fork base) |
| Upstream latest release | v0.22.2 (2026-07-17) |
| Consumers of fork | chroma, clavifaber, criome, harness, ethos-engine, introspect, logos-engine, kameo-testing, mentci (all via git dep on LiGoldragon/kameo main or rev pin) |

## What the fork changed

The fork adds 6 commits totaling ~2100 lines inserted across 20 files, with
a 997-line test file (`tests/lifecycle_phases.rs`). The changes implement a
single coherent feature: **structured terminal lifecycle with a separate
control plane.**

### Commit-by-commit summary

1. **`1325f6a` -- actor: publish terminal lifecycle outcomes**
   New module `src/actor/lifecycle.rs` (130 lines). Introduces:
   - `ActorStateAbsence` enum: `Dropped`, `NeverAllocated`, `Ejected`
   - `ActorTerminalReason` enum: `StartupFailed`, `Stopped`, `SupervisorRestart`, `Killed`, `Panicked`, `LinkDied`, `CleanupFailed`, `PeerDisconnected`
   - `ActorTerminalOutcome` struct combining the above two
   - `ActorLifecycle` internal cell using `tokio::sync::SetOnce<ActorTerminalOutcome>`

   Changes `wait_for_shutdown()` return type from `()` to `ActorTerminalOutcome` on `ActorRef`, `WeakActorRef`, `Recipient`, and `ReplyRecipient`.

   Changes `on_link_died` trait method signature to receive `ActorTerminalOutcome` alongside the legacy `ActorStopReason`.

   Changes `PreparedActor::run` and `spawn` return types from `Result<(A, ActorStopReason), PanicError>` to `Result<ActorStopReason, PanicError>` -- the actor value is no longer returned because it is dropped inside the lifecycle before notifications dispatch.

2. **`da0f64a` -- actor: split lifecycle control mailbox**
   The core architectural change. Splits the single `mpsc` channel into two:
   - **Message lane**: carries `Signal::Message` (user messages)
   - **Control lane**: carries lifecycle signals (`StartupFinished`, `Stop`, `SupervisorRestart`, `LinkDied`)

   The control lane is an `mpsc::unbounded_channel` so lifecycle signals can never be blocked by a full user-message mailbox. The receiver prioritizes control signals over messages (checks control first, then messages).

   Adds admission gating via `AtomicBool` (`admission_open`) and message generation tracking via `AtomicU64` (`message_generation`). When admission closes, user messages are rejected at the sender side with appropriate errors; control signals continue to flow.

3. **`1980e34` -- actor: cover lifecycle control edge cases**
   Additional edge-case coverage in the lifecycle test suite.

4. **`8ea1e3f` -- actor: gate weak shutdown result helpers**
   Guards `try_shutdown_result` and `try_shutdown_with_result` on `ActorRef` and `WeakActorRef` with `is_terminated()` check -- they return `None` until the terminal outcome is published, preventing a race where `SetOnce` is initialized (with stop reason) but the lifecycle sequence has not completed.

5. **`f491b45` -- fix lifecycle fork after upstream rebase**
   Mechanical fixups after rebasing onto upstream.

6. **`3486e4f` -- docs: mark Protos estate status**
   Adds `AGENTS.md` marking the fork as "upstream fork, out of scope" for the Protos estate system.

### Design motivation (inferred from code and skill documents)

The fork implements the **"release before notify"** contract documented in
`/home/li/primary/reports/PreResetCorpus-2026-06-07/skills/actor-systems.md`
lines 414-510. The specific ordering the fork enforces in `src/actor/spawn.rs`:

```
1. Stop admission (admission_open = false)
2. Finish in-flight handler
3. Shutdown children, drain children
4. Run on_stop hook
5. Drop actor state (drop(actor))
6. Dispatch link notifications (notify_links -- AWAITED, not spawned)
7. Unregister from registry
8. Set shutdown_result
9. Set terminal outcome (lifecycle.set_terminal_outcome)
```

This ordering guarantees:
- Actor state (and its owned resources like redb handles, TCP listeners) is **dropped before** link death notifications reach supervisors
- Supervisors that restart a child against the same resource will not race a still-held resource
- `wait_for_shutdown()` resolves only after all prior steps complete, carrying a typed terminal outcome

## Upstream movement since fork base (v0.20.0)

Upstream has released 5 versions since the fork base:

### v0.21.0 (2026-06-21)
- BREAKING: Error chains on `SendError`
- Live actor-system monitoring console TUI
- Preserve pending mailbox messages on actor stop/restart
- Fix deadlocks in `ActorRef` lifecycle methods

### v0.21.1 (2026-07-01)
- Per-actor default reply timeout via `PreparedActor`
- Drop all messages during drain instead of buffering tells and processing asks

### v0.22.0 (2026-07-05)
- **`on_undelivered` hook** for messages left in mailbox at terminal stop
- **Reject new messages after `stop_gracefully`** instead of silently dropping them (admission gating)
- BREAKING: `ActorRef` cloning reduced to single `Arc` clone (structural refactor of `ActorRef` internals into `Arc<ActorRefInner>`)
- BREAKING: `ctx.pipe` and `ctx.pipe_with` for pipe-to-self
- BREAKING: Return pending ask's message as `ActorRestarting`/`ActorNotRunning` during drain

### v0.22.1 (2026-07-07)
- Hotpath dependency update

### v0.22.2 (2026-07-17)
- Tracing span fix: `actor.handle_message` as root span linked to `actor.lifecycle`
- Documentation: `ActorStopReason::Panicked` covers hook errors; add `PanicError::is_panic`

## Overlap analysis

### What upstream now covers that the fork also implements

| Fork feature | Upstream equivalent | Gap |
|---|---|---|
| Admission gating (`AtomicBool` to reject messages after stop) | v0.22.0 `e8a0bce`: `accepting: Arc<AtomicBool>` on `MailboxSender`, checked in all send paths | **Substantially identical mechanism.** Upstream uses `Ordering::Relaxed` vs fork's `Ordering::Acquire/Release`. Upstream does not have message generation tracking (the fork's `AtomicU64`). |
| `on_link_died` receives richer info | Not present upstream. Upstream's `on_link_died` still receives only `ActorStopReason`. | **Fork is ahead.** |

### What upstream does NOT cover that the fork implements

1. **Separate control channel.** Upstream still uses a single `mpsc` channel for both user messages and lifecycle signals. The fork splits these into two channels so control signals (Stop, LinkDied, StartupFinished) cannot be blocked by a full bounded user-message mailbox. Upstream's admission gating rejects new messages but does not physically separate the channels.

2. **Terminal lifecycle outcome types.** `ActorTerminalOutcome`, `ActorStateAbsence`, `ActorTerminalReason` do not exist upstream. Upstream's `wait_for_shutdown()` still returns `()`. Supervisors still branch on `ActorStopReason` rather than a terminal outcome that distinguishes state-dropped from never-allocated from ejected.

3. **Release-before-notify ordering.** Upstream's shutdown sequence in `src/actor/spawn.rs` is:
   ```
   notify_links(...)    -- via tokio::spawn (fire-and-forget)
   on_stop(...)
   unregister
   set shutdown_result
   return (actor, reason)  -- actor value returned to caller, not dropped
   ```
   The fork's sequence is:
   ```
   on_stop(...)
   drop(actor)          -- resources released
   notify_links(...)    -- AWAITED, not spawned
   unregister
   set shutdown_result
   set terminal outcome
   ```
   This is the most consequential difference. Upstream still `tokio::spawn`s link notifications (fire-and-forget), does not drop the actor before notifying, and returns the actor value to the spawn caller. The fork drops the actor before dispatching notifications and awaits the dispatch.

4. **`wait_for_shutdown` returns typed outcome.** The fork's `wait_for_shutdown() -> ActorTerminalOutcome` lets callers branch on the terminal state without inspecting `ActorStopReason`. Upstream returns `()`.

5. **Message generation tracking.** The fork's `AtomicU64` message generation counter allows invalidating in-flight messages from a previous generation (relevant to restart scenarios). Upstream does not have this.

### What upstream adds that the fork does not have

1. **`on_undelivered` hook** (v0.22.0) -- actor receives leftover messages at terminal stop
2. **`ActorRef` single-Arc optimization** (v0.22.0) -- `ActorRefInner` behind one `Arc`
3. **`ctx.pipe` / `ctx.pipe_with`** (v0.22.0) -- pipe-to-self messaging
4. **Per-actor default reply timeout** (v0.21.1) -- `PreparedActor::reply_timeout`
5. **Console TUI** (v0.21.0) -- live actor system monitoring
6. **Drain semantics changes** (v0.21.1, v0.22.0) -- how messages are handled during shutdown/restart drain
7. **Panic catching in on_stop** (v0.22.0) -- `AssertUnwindSafe` around `on_stop`
8. **Various dependency updates** (hotpath, opentelemetry, tracing-opentelemetry, syn, libp2p)

## Conflict assessment for rebase

### Structural conflicts (will require manual resolution)

1. **`src/actor/actor_ref.rs`**: Upstream's `Arc<ActorRefInner>` refactor (`3901886`) restructures the same type the fork adds `lifecycle: ActorLifecycle` to. Every field access changes from `self.field` to `self.inner.field`. The fork's `lifecycle` field would need to move into `ActorRefInner`. The fork's `is_accepting_messages()`, `is_terminated()`, and modified `wait_for_shutdown()` would need adaptation to the new structure. **High conflict density.**

2. **`src/actor/spawn.rs`**: The fork's reordered shutdown sequence (drop-before-notify, awaited notifications, terminal outcome) conflicts with upstream's added `on_undelivered`, panic-catching `on_stop`, console monitoring hooks, and drain logic. The sequences are fundamentally different. **High conflict density, requires careful merge.**

3. **`src/mailbox.rs`**: The fork's two-channel split conflicts with upstream's single-channel + `accepting` flag. The fork's `MailboxSenderInner::Bounded { messages, control }` vs upstream's `MailboxSenderInner::Bounded(tx)` with `accepting` flag. Upstream's admission gating would be superseded by the fork's split-channel approach. **High conflict density.**

4. **`src/links.rs`**: The fork's `LinkNotification` enum and `notify_links` refactor (method on `Links` that awaits dispatch) conflicts with upstream which still has the old `LinksInner::notify_links` with `tokio::spawn`. **Medium conflict density.**

### Estimated rebase cost

A mechanical rebase will fail on 4-6 files with dense conflicts. The work is not a rebase but a **re-implementation** of the fork's features on top of the current upstream structure. Estimated effort: 2-4 focused sessions, primarily because:
- The `ActorRefInner` refactor requires threading `lifecycle` through the new structure
- The `on_undelivered` hook interacts with the shutdown sequence reordering
- The drain semantics changes need reconciliation with the control-channel split

## Verdict material

### Is the fork behind upstream?

Yes. The fork is based on what was upstream/main at the time of forking (commit `4d2e2d0`, v0.20.0 era). Upstream has since released v0.21.0, v0.21.1, v0.22.0, v0.22.1, v0.22.2 with 49 commits including multiple breaking changes.

### Does anything upstream make the fork unnecessary?

**Partly.** Upstream's v0.22.0 admission gating (`e8a0bce`) covers the same problem as the fork's admission gate, making that specific piece redundant. However, the fork's core contributions -- control channel separation, release-before-notify ordering, typed terminal outcomes, and `wait_for_shutdown` returning `ActorTerminalOutcome` -- have no upstream equivalent.

### Could the fork's goal be achieved differently?

Several paths exist:

1. **Upstream PR.** The release-before-notify ordering and terminal outcome types could be proposed upstream. The control channel split is the most invasive change and the hardest to upstream -- it touches every send/receive path. The terminal outcome types are the cleanest candidate for an upstream PR.

2. **Wrapper crate.** A `kameo-lifecycle` crate that adds `ActorTerminalOutcome` tracking externally (via `wait_for_shutdown_result` + post-hoc classification) would avoid forking the mailbox layer. This would not achieve control-channel separation or the drop-before-notify ordering.

3. **Feature flag.** The control channel split could live behind a cargo feature flag, making it opt-in. This would reduce upstream maintenance burden but adds conditional compilation complexity to the mailbox layer.

4. **Different library.** Not assessed as viable -- kameo's design (`Self IS the actor`, per-kind `Message<T>`, declarative supervision) is specifically selected for this workspace's actor discipline.

### What a rebase onto current upstream would cost

- **Files with dense conflicts**: `src/actor/actor_ref.rs`, `src/actor/spawn.rs`, `src/mailbox.rs`, `src/links.rs`
- **Effort**: Re-implementation rather than mechanical rebase. The `ActorRefInner` refactor and `on_undelivered` hook change the terrain the fork's changes sit on.
- **Risk**: The fork's `tests/lifecycle_phases.rs` (997 lines) provides strong regression coverage for the release-before-notify invariant, which de-risks the re-implementation.
- **Benefit**: Picks up console TUI, `on_undelivered`, pipe-to-self, single-Arc cloning perf, drain fixes, panic catching in on_stop, and dependency updates.

## Unknowns

1. Whether upstream has any plans or open issues for control plane separation or terminal outcome types -- I did not find any, but the absence of evidence is not evidence of absence.
2. Whether the message generation counter (`AtomicU64`) has been exercised in real restart scenarios or is speculative machinery.
3. Whether upstream's `tokio::spawn` for link notifications has caused real deadlocks in this workspace's actor topologies, or whether the awaited-dispatch change is preventive.
4. The `Ejected` variant of `ActorStateAbsence` -- there is no code path in the fork that produces it. It may be forward-looking design for a state-extraction API that does not yet exist.
