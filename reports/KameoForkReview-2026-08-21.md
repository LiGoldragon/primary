# Kameo Fork Review

Design session `15b67974`, 2026-08-21. Psyche direction:
"Has upstream released since our fork? Let's review that fork again
to see if it makes sense."

## 1. The fork, witnessed locally

### Location

The fork checkout lives at `/git/github.com/LiGoldragon/kameo`.
Remotes: `origin` = `LiGoldragon/kameo`, `upstream` = `tqwewe/kameo`.

All 21 consuming repos reference it via git dependency
(`git = "https://github.com/LiGoldragon/kameo.git"`) with either
`branch = "main"` (14 repos) or `rev = "f491b45"` (4 repos). One
repo (lojix) uses crates.io `"0.20"` without the fork. One repo
(persona-spirit) uses a feature branch.

### Divergence point

The fork's `origin/main` diverges from `upstream/main` at commit
`4d2e2d02` ("chore: use libp2p::identity instead of
libp2p_identity directly (#339)"), dated 2026-06-19. The fork is
based on upstream v0.20.0 (tagged 2026-04-08), rebased forward to
that point.

The fork carries 6 commits on top of the merge-base:

| Commit  | Date       | Subject |
|---------|------------|---------|
| 1325f6a | 2026-05-16 | actor: publish terminal lifecycle outcomes |
| da0f64a | 2026-05-16 | actor: split lifecycle control mailbox |
| 1980e34 | 2026-05-16 | actor: cover lifecycle control edge cases |
| 8ea1e3f | 2026-05-16 | actor: gate weak shutdown result helpers |
| f491b45 | 2026-06-19 | fix lifecycle fork after upstream rebase |
| 3486e4f | 2026-06-19 | docs: mark Protos estate status |

(`src/actor/lifecycle.rs`, `src/actor/spawn.rs`, `src/actor.rs`,
`src/actor/actor_ref.rs`, `src/actor/kind.rs`, `src/links.rs`,
`src/mailbox.rs`, `tests/lifecycle_phases.rs` -- 20 files changed,
+2113 / -347 lines.)

### What the customizations do

**A. Terminal lifecycle type system** (new file `src/actor/lifecycle.rs`).
Adds `ActorTerminalOutcome`, `ActorTerminalReason`,
`ActorStateAbsence`, and `ActorLifecycle` (a shared `SetOnce` cell).
These replace the implicit "channel closed = shutdown complete"
contract with an explicit terminal-outcome publication.
`ActorTerminalReason` distinguishes `Stopped`, `SupervisorRestart`,
`Killed`, `Panicked`, `LinkDied`, `CleanupFailed`,
`StartupFailed`, and `PeerDisconnected` -- finer than upstream's
`ActorStopReason`, which bundles panic payloads and link-death
chains into variants rather than classifying the terminal cause.

**B. Split control/message mailbox** (heavy changes in
`src/mailbox.rs`, +876/-347). The single `mpsc` channel is replaced
with two channels: an ordinary message channel (bounded or
unbounded) and a separate unbounded control channel for lifecycle
signals. Messages carry a generation counter; admission is gated by
an `AtomicBool` + generation check so that message rejection is
immediate once shutdown begins, while lifecycle signals always pass.

**C. `on_link_died` gains `ActorTerminalOutcome`** (src/actor.rs).
The `Actor::on_link_died` trait method's signature adds an
`outcome: ActorTerminalOutcome` parameter. Decision logic switches
from matching `ActorStopReason` variants to matching
`ActorTerminalReason`, gaining `CleanupFailed` and
`StartupFailed` arms.

**D. `wait_for_shutdown` returns `ActorTerminalOutcome`**
(src/actor/actor_ref.rs). All `wait_for_shutdown` methods change
return type from `()` to `ActorTerminalOutcome`, waiting on the
lifecycle cell instead of the channel close.

**E. Shutdown ordering** (src/actor/spawn.rs). The lifecycle drops
the actor state before notifying links and setting the shutdown
result, ensuring `on_link_died` fires only after the dead actor's
state is gone. `run()` / `spawn()` return `Result<ActorStopReason,
PanicError>` instead of `Result<(A, ActorStopReason), PanicError>`
-- the actor value `A` is no longer returned.

**F. Synchronous link notification** (src/links.rs). Upstream
fire-and-forgets link notifications via `tokio::spawn`. The fork
awaits them inline, preventing races where a supervising actor
observes the terminal outcome before the death signal arrives.

**G. Supervision uses terminal outcome** (src/links.rs).
`ErasedChildSpec::should_restart` takes `&ActorTerminalOutcome`
instead of `&ActorStopReason`.

## 2. Upstream since the fork

### Releases

Since the fork's base (v0.20.0, 2026-04-08), upstream has released:

| Version | Date       | Notable changes |
|---------|------------|-----------------|
| v0.21.0 | 2026-06-22 | Fix `ActorRef` lifecycle deadlocks (#340); preserve pending mailbox messages on stop/restart (#345); catch panics in shutdown; console TUI (#343); `SendError` error chains (#338) |
| v0.21.1 | 2026-07-01 | Per-actor default reply timeout (#354); drop all messages during drain instead of buffering (#351) |
| v0.22.0 | 2026-07-05 | `on_undelivered` hook (#363); reject messages after `stop_gracefully` (#362); `ctx.pipe` / `ctx.pipe_with` (#360); `ActorRef` single-`Arc` clone (#365); supervision drain returns `ActorRestarting`/`ActorNotRunning` (#359) |
| v0.22.1 | 2026-07-08 | Hotpath update |
| v0.22.2 | 2026-07-18 | Tracing: `actor.handle_message` root span linked to `actor.lifecycle` (#382); `PanicError::is_panic` (#375) |

Active upstream branches include `feat/kameo-remote` (a new
`kameo_remote` crate with chitchat gossip and TCP messaging),
`feat/kameo-remote-tls-auth`, and `feat/actor-errors`.

64 commits separate v0.20.0 from upstream `main` (as of
2026-08-21).

### Upstream overlap with fork customizations

**Partial overlap on message rejection (customization B).**
Upstream v0.22.0 (#362) adds an `accepting: Arc<AtomicBool>` to
`MailboxSender` that rejects `Signal::Message` sends after
`stop_gracefully`. This is the same concept as the fork's admission
gate. However, the fork goes further: it splits into two physical
channels (messages vs. control) and adds a generation counter, so
that a lifecycle signal can never be blocked behind a full bounded
message queue. Upstream keeps a single channel for all signals;
control signals can still be delayed behind queued messages in a
bounded mailbox.

**No overlap on the terminal lifecycle type system (A, C, D, E,
G).** Upstream has no `ActorTerminalOutcome`,
`ActorTerminalReason`, or `ActorLifecycle`. `on_link_died` still
takes `ActorStopReason` only. `wait_for_shutdown` still returns
`()`. `run()` still returns `(A, ActorStopReason)`. Upstream has no
equivalent of `CleanupFailed` or `StartupFailed` as distinct
terminal reasons.

**No overlap on synchronous link notification (F).** Upstream still
calls `tokio::spawn` for both parent and sibling death
notifications.

## 3. Decision surface

### Cost of staying forked

**Drift.** 64 upstream commits are not merged. Concrete upstream
improvements not received:

- `ActorRef` lifecycle deadlock fixes (#340) -- fixes races between
  `wait_for_shutdown_result` and `on_stop` that are structurally
  present in the fork's base
- `ActorRef` single-`Arc` clone (#365) -- performance improvement
  for clone-heavy patterns
- `on_undelivered` hook (#363) -- new lifecycle extension point
- `ctx.pipe` / `ctx.pipe_with` (#360) -- ergonomic self-messaging
- Supervision drain improvements (#351, #359)
- `SendError` error chains (#338) -- diagnostic improvement
- Per-actor reply timeouts (#354)
- Console TUI (#343)
- `PanicError::is_panic` (#375)
- Tracing span fixes (#346, #382)

The fork last rebased on 2026-06-19. Two months of drift have
accumulated.

**Maintenance burden.** The fork's mailbox rewrite (+876/-347 in
`src/mailbox.rs`) is the largest single change and the most likely
to conflict with upstream mailbox changes (upstream already modified
`src/mailbox.rs` in #362).

### Cost of returning to upstream

The following fork customizations have no upstream equivalent and
would need to be either upstreamed, reimplemented as an extension,
or abandoned:

1. `ActorTerminalOutcome` / `ActorTerminalReason` /
   `ActorStateAbsence` type system (the core design)
2. Split control/message mailbox with generation counter
3. `on_link_died` signature change (breaking `Actor` trait)
4. `wait_for_shutdown` returning `ActorTerminalOutcome`
5. `run()` not returning actor state `A`
6. Synchronous (non-spawned) link notification
7. `CleanupFailed` / `StartupFailed` as distinct terminal reasons

Items 1, 3, 4, 5, and 7 are API-breaking relative to upstream.
Every consumer that implements `on_link_died` or calls
`wait_for_shutdown` depends on these changes.

### Middle paths

**Upstream extension points.** Upstream v0.22.0 added
`on_undelivered` and the `accepting` gate, showing willingness to
refine lifecycle semantics. The `ActorRef` single-`Arc` refactor
shows structural flexibility. However, nothing in upstream provides
a hook or trait that would let an external crate inject the
terminal-outcome type system without forking `Actor`.

**Upstream contribution.** The terminal-outcome design could be
proposed upstream. The `ActorTerminalReason` enum and
`ActorLifecycle` cell are self-contained additions. The
`on_link_died` signature change and split mailbox are more
invasive and less likely to be accepted without negotiation.

**Rebase forward.** The fork could be rebased onto current upstream
`main` (post-v0.22.2). The mailbox changes are the primary
conflict area; the lifecycle type system touches files upstream
also modified (`actor_ref.rs`, `spawn.rs`, `links.rs`). A rebase
is feasible but not trivial.

## Unknowns

- Whether the `ActorRef` lifecycle deadlock fix (#340) addresses
  the same races that the fork's `ActorLifecycle` cell was designed
  to prevent, or whether those are distinct failure modes
- Whether upstream's `accepting` gate (#362) is sufficient for
  the fork's consumers or whether the split-channel guarantee
  (control signals never blocked behind messages) is load-bearing
- Whether upstream would accept a PR for `ActorTerminalOutcome`
- The status of upstream's `feat/actor-errors` branch and whether
  it moves toward richer terminal classification
