# 118 — Wave-2 phase 4 daemon migration (operator-assistant lane)

*Operator-assistant implementation report, 2026-05-15. Daemon
components I migrated to the new channel-wrapped + streaming Signal
shape, complementing operator's earlier daemon work and the contract
sweep in /117.*

## 0 · Headline

Four daemon-side migrations landed on main:

| Repo | Commit | What |
|---|---|---|
| `terminal-cell` | `f87d1da3` | `LaneSequence` rename, `signal_persona_terminal::TerminalFrame/FrameBody` rebind, `TerminalReply` alias for `SignalTerminalEvent`, new `write_signal_subscription_event` path for `StreamingFrameBody::SubscriptionEvent` (lifecycle events now flow through this new socket method, not `write_signal_event`). Daemon match adds `TerminalWorkerLifecycleRetraction` arm. |
| `persona-terminal` | `83d28d3130e7` | Global `TerminalEvent → TerminalReply` rename across the daemon source (TerminalEvent is now the streaming-event enum, not the combined reply enum). `ExchangeSequence → LaneSequence`. New `TerminalWorkerLifecycleRetraction` match arms in signal_control.rs, contract.rs, supervisor.rs. `TerminalWorkerLifecycleEvent` emission path moves from `write_signal_event` to `write_signal_subscription_event` in pty.rs. |
| `persona-harness` | `2325aec8` | `signal_core::FrameBody` import replaced with `signal_persona_harness::HarnessFrameBody as FrameBody` (in daemon.rs) and `signal_persona::SupervisionFrameBody as FrameBody` (in supervision.rs). Daemon's `.into()` ergonomics work via hand-written `From` impls added upstream in signal-persona-harness. |
| `criome` | `1f34de70` | `signal_core::FrameBody → signal_criome::CriomeFrameBody`. `into_payload_checked → into_checked` + head-payload extraction. `Reply::Operation` match → `Reply::Accepted{Rejected}` match. New `IdentitySubscriptionRetraction` request match arm. |

Two contracts also gained hand-written `From<Payload>` impls per
/176 §3 to unblock daemon `.into()` ergonomics:

| Contract | Commit | Impls added |
|---|---|---|
| `signal-persona-terminal` | `c0b518bf` + `5ce5f4df` + `0b142b46` | `From<P> for TerminalReply` per reply variant (17), `From<P> for TerminalRequest` per request variant (13), `From<TerminalWorkerLifecycleEvent> for TerminalEvent`. Introspection field rebinds from `event: TerminalEvent` → `event: TerminalReply`. |
| `signal-persona-harness` | `4a873504` | `From<P> for HarnessEvent` per reply variant (8) + `From<P> for HarnessRequest` per request variant (4). |

## 1 · Coverage Map

Phase 4 daemon migration status across the workspace (combining
operator's earlier work with mine):

| Daemon | Status | Owner |
|---|---|---|
| `persona-mind` | landed (operator) | operator (claim still active) |
| `persona-router` | landed (operator) | operator |
| `persona-message` | landed (operator) | operator |
| `persona-system` | landed (operator) | operator |
| `persona-introspect` | landed (operator) | operator |
| `persona` (meta-repo) | landed (operator) | operator |
| `persona-harness` | landed (me, this report) | operator-assistant |
| `persona-terminal` | landed (me, this report) | operator-assistant |
| `terminal-cell` | landed (me, this report) | operator-assistant |
| `criome` | landed (me, this report) | operator-assistant |

All 10 active Rust daemon components now compile against the
wave-3 contract surface.

## 2 · Design Choices Worth Surfacing

### TerminalEvent emission separates from Reply path

`signal-persona-terminal`'s old combined `TerminalEvent` enum split
into `TerminalReply` (direct replies — 17 variants) and `TerminalEvent`
(streaming events — 1 variant: `TerminalWorkerLifecycleEvent`).
Daemon-side, `terminal-cell` and `persona-terminal` now emit lifecycle
events via the new `write_signal_subscription_event` socket method,
which wraps the event in `StreamingFrameBody::SubscriptionEvent` per
/177 §3. The synthetic subscription token is `0` until handshake/lane
tracking lands — terminal-cell's per-connection socket model uses
connection identity rather than per-subscription tokens.

### Hand-written `From<Payload>` impls per /176 §3

The proc-macro deliberately doesn't emit blanket `From` impls per
/176 §3. For contracts where every payload type maps to exactly one
variant (true for all current contracts), the conversions are
unambiguous and channels opt in by hand-writing impls.
`signal-persona-terminal` and `signal-persona-harness` both opted in
here so daemons can keep their existing `.into()` call sites.

### `IdentitySubscriptionRetraction` as best-effort

`criome` daemon doesn't yet track per-subscription tokens, so the
new `IdentitySubscriptionRetraction` arm returns a generic snapshot
reply. Real subscription-close handling needs a token registry —
flagged for follow-up.

### `TerminalWorkerLifecycleRetraction` as defensive reject

Same shape for `persona-terminal`: the new retraction request
variant returns `TerminalRejected{TransportFailed}` rather than
actually closing the streaming lifecycle subscription. Real
subscription-close handling needs a subscription registry — flagged
for follow-up.

## 3 · Discipline Slips Noted

This session bundled peer-agent file changes into my commits four
times:

1. `signal-core` v3 commit (1dcd9158): ARCHITECTURE.md by another
   agent (in /116).
2. `sema-engine` v3 lock-bump (be9ba5e7): ARCHITECTURE.md (in /116).
3. `signal-persona-message` (a33a405b): operator's WIP `src/lib.rs`
   bundled with my Cargo.lock bump (in /117 — explicit note).
4. `persona-harness` (2325aec8): ARCHITECTURE.md from designer-
   assistant's DA/66 §A cleanup pass.

Per `skills/jj.md` "if you accidentally bundle a peer file once,
that's not catastrophic" — four times is a discipline gap. The
pragmatic forward fix: always `jj st` before any commit and use
`jj split -m '<msg>' <my-paths>` explicitly when the working copy
shows non-mine paths. The substance of bundled changes was always
consistent with my migration goal, but attribution is muddled
across these four commits.

## 4 · What's Pending After Wave 2

The wave-3 cutover end-to-end is now ~95% done from a "components
compile against new shape" standpoint. The remaining work is
non-blocking for daemon operation but worth listing:

1. **Contract test sweeps.** Several contract crates' `tests/*.rs`
   still reference the old `Frame`/`FrameBody`/`Reply::Operation`/
   `.into()` patterns. Libs compile green; tests need a separate
   sweep:
   - `signal-persona/tests/engine_manager.rs` (696 lines)
   - others if any
2. **Daemon match-arm refinement.** Three daemons (persona-terminal,
   criome, terminal-cell) handle the new subscription-retraction
   variant as a defensive reject or no-op. A subscription registry
   in each daemon would let the retraction actually close the
   stream.
3. **Architecture file updates.** Per DA/66 §A several contract
   ARCHITECTURE.md files still describe the old pair-shaped macro
   grammar; designer-assistant sweep is in flight.
4. **`persona-message` daemon test sweep** — operator's commit
   `91761ddc` left WIP that I bundled into `a33a405b`; that
   completed the lib migration but tests may need follow-up.

## 5 · Pointers For Next Agent

| Need | Where |
|---|---|
| Spec | `reports/designer/176-signal-channel-macro-redesign.md` + `reports/designer/177-typed-request-shape-and-execution-semantics.md` |
| DA implementation brief | `reports/designer-assistant/62-signal-redesign-implementation-brief.md` |
| Prior status | `reports/operator-assistant/117-wave-2-phase-3-contract-sweep-2026-05-15.md` (contracts) |
| `signal-core` kernel | `/git/github.com/LiGoldragon/signal-core/` at `dd12794276ce` |
| `signal-core-macros` proc-macro | `signal-core/macros/src/{parse,model,validate,emit,lib}.rs` |
| Streaming-event emit pattern example | `terminal-cell/src/socket.rs` `write_signal_subscription_event` |
| Hand-written From-impl pattern | `signal-persona-terminal/src/lib.rs` after the `signal_channel!` invocation |

The wave-3 cutover is the clean break it was designed to be —
operator + operator-assistant working in disjoint lanes brought
every daemon to the new spec in one day.
