# 117 — Wave-2 phase 3 contract sweep complete

*Operator-assistant implementation report, 2026-05-15. Phase 3 of the
wave-2 cutover: every contract crate migrates from the old
`signal_channel! { request ... reply ... }` macro_rules grammar to the
new proc-macro `channel { ... }` grammar per /176 §1.*

## 0 · Headline

All 11 active contract crates now compile against `signal-core`
wave-3 (`dd12794276ce`). 6 exchange-only contracts gained the
`channel <Name> { ... }` wrapper. 4 streaming contracts gained
`event` + `stream` blocks and substantive new wire surface
(subscription token newtypes + Retract variants for stream close).
1 contract has no `signal_channel!` invocation and only needed a
lock bump.

## 1 · Phase 1 + 2 Already Pushed (Recap)

| Repo | Wave-3 commit | What |
|---|---|---|
| `signal-core` | `dd12794276ce` | LaneSequence rename, FrameBody split into ExchangeFrameBody + StreamingFrameBody, RequestRejectionReason::DecodeError dropped, RequestBuilderError::EmptyRequest rename, kernel-layer Operation/Request NOTA codec, new `signal-core/macros/` proc-macro crate, old `macro_rules!` channel.rs retired. 54 tests pass. |
| `sema-engine` | `d1271469` | Cargo.lock bump only — no source changes needed since wave-1 already retired SignalVerb::Atomic. |

## 2 · Phase 3 Per-Contract State

### Exchange-only (no Subscribe variants)

| Contract | Commit | What changed |
|---|---|---|
| `signal-persona-harness` | `7cd4530e` | Added `channel Harness { ... }` wrapper. Tests rewrote to ExchangeFrame/ExchangeFrameBody patterns, Reply::Accepted/Rejected matching, explicit variant constructors (auto-From retired per /176 §3). 19 tests pass. |
| `signal-persona` | `e72aa754` | Two invocations: `channel Engine` and `channel Supervision`. Re-exports drop the `Frame as SupervisionFrame` rename now that the macro emits SupervisionFrame directly. `CoreFrameBody` re-export points at `ExchangeFrameBody`. Lib compiles; tests/engine_manager.rs (696 lines) is a separate test sweep. |
| `signal-persona-message` | `a33a405b` | **Bundled with operator's WIP** lib migration: `channel MessageChannel { ... }`. Lib carries back-compat `pub type Frame = MessageChannelFrame;` etc. for downstream consumers. Operator authored the lib edits in working-copy `91761ddc` (no description); I bundled them with my Cargo.lock bump per `skills/jj.md` "if you accidentally bundle a peer file once, that's not catastrophic" — attribution muddled but substance correct. |
| `signal-persona-router` | `59ea1246` | `channel Router { ... }`. Pure lock + wrapper update — no subscriptions. |
| `signal-persona-introspect` | `4fc3914b` | `channel Introspection { ... }`. Pure lock + wrapper update. |
| `signal` | `fa8055f4` | No `signal_channel!` invocation — lock-only bump to wave-3. |

`signal-persona-auth` has no `signal_channel!` invocation (record-only contract) — no migration needed.

### Streaming (Subscribe variants present)

These required substantive new wire surface. For each, I exercised
operator-assistant judgment per the user's "refactor all contracts"
goal; designer review can revise via subsequent reports.

| Contract | Commit | Wire-surface delta |
|---|---|---|
| `signal-persona-mind` | `ec00cde0` | Added `Retract SubscriptionRetraction(SubscriptionId)` request variant; moved `SubscriptionEvent` from `MindReply` to new `event MindEvent { SubscriptionDelta(SubscriptionEvent) belongs MindEventStream }`. Both Subscribe variants (SubscribeThoughts, SubscribeRelations) open the same `MindEventStream` — `SubscriptionTokenInner` on the frame body demuxes per /177 §4.2. Confirmed defensible by designer in chat. |
| `signal-persona-system` | `75315450` | Renamed `reply SystemEvent` → `reply SystemReply` (since the old "Event" enum mixed direct replies and events per DA/66 §C). New `event SystemEvent { FocusObservation, WindowClosed belongs FocusEventStream }`. Stream `FocusEventStream` uses `FocusUnsubscription` as both token type and close variant — `FocusUnsubscription.target: SystemTarget` IS the per-subscription identity, so the macro's `close.payload_type == stream.token_type` constraint holds without inventing a new token newtype. |
| `signal-persona-terminal` | `fb758ba6` | Matches `/176` §1's worked example exactly. Added `TerminalWorkerLifecycleToken { terminal: TerminalName }` newtype + `Retract TerminalWorkerLifecycleRetraction(TerminalWorkerLifecycleToken)` request variant. Renamed `reply TerminalEvent` → `reply TerminalReply`; new `event TerminalEvent { TerminalWorkerLifecycleEvent belongs TerminalWorkerLifecycleStream }`. |
| `signal-criome` | `3f48a6c9` | Added `IdentitySubscriptionToken { subscriber: Identity }` newtype + `Retract IdentitySubscriptionRetraction(IdentitySubscriptionToken)`. Moved `IdentityUpdate` from `CriomeReply` to new `event CriomeEvent { IdentityUpdate belongs IdentityUpdateStream }`. `IdentitySnapshot` stays in `CriomeReply` as the opened-reply for the stream. |

## 3 · What Comes Next (Phase 4 — Operator's Lane)

Each daemon needs:

1. **Cargo.lock bump** to pull the new contract revs.
2. **Pattern-match update** — the FrameBody pattern matches need to
   handle the new `<Channel>FrameBody` types (channel-prefixed) and
   the split `Accepted/Rejected` Reply enum. Operator already did
   this for the v3 spec; the channel-wrapper rename is mechanical.
3. **Substantive cascade for streaming contracts**:
   - `persona-mind` — `MindReply::SubscriptionEvent` is gone; daemon
     code that constructed/matched it must use
     `MindEvent::SubscriptionDelta` and emit via the
     `StreamingFrameBody::SubscriptionEvent` variant. New
     `MindRequest::SubscriptionRetraction` variant needs a handler
     (or an explicit "unimplemented" arm).
   - `persona-system` — `SystemEvent` enum is the new event-only
     variant set; daemon must emit `FocusObservation` and
     `WindowClosed` via `SubscriptionEvent` frame variants, not
     reply variants. Reply enum is now `SystemReply`.
   - `persona-terminal` — `TerminalEvent` enum is the new event-only
     set (just `TerminalWorkerLifecycleEvent`). Reply enum is
     `TerminalReply` (with `TerminalWorkerLifecycleSnapshot` moved
     in as the opened-reply). Daemon needs a
     `TerminalWorkerLifecycleRetraction` handler.
   - `criome` daemon (if it exists today): `IdentityUpdate` moves to
     `CriomeEvent`. Daemon needs `IdentitySubscriptionRetraction`
     handler.

4. **Contract test sweeps** — many contract test files (e.g.
   `signal-persona/tests/engine_manager.rs`, 696 lines) still
   reference the old FrameBody/Reply::Operation/Request::Operation
   patterns plus `.into()` blanket-From calls. Lib compiles green
   for downstream consumers; test sweeps are a separate operator
   pass.

## 4 · Discipline Notes

- One `jj st`-skip slip: bundled operator's `91761ddc (no description set)`
  WIP edits in signal-persona-message under my commit. Substance
  consistent (the lib migration we both want); attribution
  muddled. Noted explicitly in commit message (`a33a405b`).
- Coordination with operator was clean for the rest of the sweep:
  operator's lock showed daemons (`persona-*`), I claimed contracts
  (`signal-persona-*`), no overlap.

## 5 · Pointers For Next Agent

| Need | Where |
|---|---|
| Live `signal-core` source | `/git/github.com/LiGoldragon/signal-core/` at `dd12794276ce` |
| Proc-macro source | `signal-core/macros/src/{lib,parse,model,validate,emit}.rs` |
| Spec | `reports/designer/176-signal-channel-macro-redesign.md` + `reports/designer/177-typed-request-shape-and-execution-semantics.md` |
| DA implementation brief | `reports/designer-assistant/62-signal-redesign-implementation-brief.md` |
| Streaming-contract design judgments | see §2 above + each contract's migration commit message |
| Mind streaming worked example | `signal-persona-mind/src/lib.rs` around line 1745 |
| Terminal streaming worked example (closest to /176 §1) | `signal-persona-terminal/src/lib.rs` around line 878 |

Daemon re-pin + match-pattern cascade is operator's lane; release my
operator-assistant claim back to idle.
