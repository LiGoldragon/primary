# 116 — Engine wave-1 migration (signal-core + sema-engine, downstream
fan-out)

*Operator-assistant implementation report, 2026-05-15. Records what
landed, what's pending, and the design gap (DA/64) that paused
further downstream migration.*

## 0 · Scope

User direction: "help operator to refactor the entire engine" then
"keep working until all components are migrated to new architecture."

Migration target: the signal-core + sema-engine wave-1 design from
DA/61, DA/62, DA/63, and designer /176 + /177. Spec evolved three
times during the session as DA/63 critique was absorbed and DA/64
research surfaced a remaining structural gap.

## 1 · What Landed

### `signal-core` — three commits, ending at v3 spec shape

`main` is at `29006d41`. Three coherent commits:

1. **`1dcd9158`** — typed `Request<Payload>` struct shape + async exchange
   per initial DA/61+62. Six-root `SignalVerb` (Atomic retires), `NonEmpty<T>`,
   `Operation<Payload>`, `Request<Payload>` struct, `Reply<R>` struct,
   typed-sum `SubReply<R>`, `ExchangeIdentifier` family, frame-level
   handshake. `signal_channel!` emits `<Name>Kind` projection +
   per-channel policy unit struct.
2. **`f341c54f`** — alignment with first DA/63 absorption. `RolledBack`
   → `Invalidated`, `validate` → `check`, `BatchPolicy` →
   `ChannelPolicy`, `max_operations` → `max_ops`, `ExchangeMode::
   LaneSequence` drops lane fields, `FrameBody::SubscriptionEvent`
   added, `Frame::body` made pub.
3. **`29006d41`** — second DA/63 absorption (RequestBuilder, no
   ChannelPolicy in wave-1, accepted/rejected Reply split). Reply
   becomes `enum { Accepted{outcome, per_operation} |
   Rejected{reason} }`. `AcceptedOutcome` replaces `RequestOutcome`,
   `OperationFailureReason` replaces `SubFailureReason` and the
   execution-side variants of `RequestFailureReason`,
   `RequestRejectionReason` covers pre-execution rejection.
   `BatchBuilder` → `RequestBuilder`. `ChannelBuilder` →
   `ChannelRequestBuilder`. `StreamEventIdentifier` separate from
   `ExchangeIdentifier`. `policy.rs` deleted. Macro stops emitting
   `<Name>ChannelPolicy`. 46 tests pass.

**Note:** the v3 commit accidentally bundled an `ARCHITECTURE.md`
update written by another agent (likely designer-assistant). Per
`skills/jj.md` §"Read jj st before every commit", the procedural slip
was not catching this in `jj st` before `jj commit`. Not catastrophic
(content matches the new spec) but attribution is muddled.

### `sema-engine` — two commits, ending at v3 lock bump

`main` is at `be9ba5e7`. Two commits:

1. **`4300c6d7`** — `SignalVerb::Atomic` retires. `Engine::atomic` →
   `Engine::commit`. `AtomicBatch` / `AtomicOperation` / `AtomicReceipt`
   → `CommitRequest` / `WriteOperation` / `CommitReceipt`.
   `OperationLogEntry` → `CommitLogEntry { snapshot, operations:
   NonEmpty<CommitLogOperation> }`. `Engine::operation_log` →
   `commit_log`. `Error::EmptyAtomicBatch` → `Error::EmptyCommit`.
   `Error::DuplicateAtomicKey` → `Error::DuplicateWriteKey`. 30 tests
   pass.
2. **`be9ba5e7`** — Cargo.lock bump only, pinning signal-core v3.
   (Also accidentally bundled an `ARCHITECTURE.md` update from another
   agent.)

### Downstream migrations landed

| Repo | What | Push |
|---|---|---|
| `terminal-cell` | Signal frame socket migrated to new `FrameBody::Request { exchange, request }` and `Reply::Accepted` enum split. 12 tests pass. | `727ffccb` |
| `persona-mind` | Transport + supervision migrated to v3 Reply enum. Tables fixed for `commit_log` shape. Error vocabulary updated: `SignalVerbMismatch` → `RequestRejected` + `ReplyRejected`. Lib tests pass. | `9d5c0ee4` |

### Contract crate Cargo.lock bumps (no source changes, no API churn)

Pushed lock-only updates to signal-core v3 in 11 contract crates:
`signal-persona`, `signal-persona-auth`, `signal-persona-mind`,
`signal-persona-router`, `signal-persona-message`,
`signal-persona-system`, `signal-persona-harness`,
`signal-persona-terminal`, `signal-persona-introspect`,
`signal-criome`, `signal`. All compile clean against v3.

## 2 · What's Pending

### Six daemon consumers not migrated

Each uses the pre-v3 `FrameBody::Request(req)` / `FrameBody::Reply(Reply::
Operation(payload))` / `Request::unchecked_operation` / `Reply::operation`
patterns. Each needs the same shape of edits I applied to terminal-cell
and persona-mind.

| Repo | Why not yet |
|---|---|
| `persona-router` | Half-migrated; edits abandoned (didn't compile because persona-terminal also needs migration). |
| `persona-terminal` | Half-migrated supervision.rs; abandoned same reason. |
| `persona-system` | Not started. |
| `persona-harness` | Not started. |
| `persona-introspect` | Not started. |
| `criome` | Not started. |
| `persona` | Lib has two `reply.per_operation()` call sites that need Accepted/Rejected match. |

**`persona-message` is operator-claimed** (`operator.lock` shows
`/git/github.com/LiGoldragon/persona-message # update supervision codec
for signal-core async exchange frame shape`). Don't touch.

### Why paused

DA/64 surfaces a real structural gap in /176/177. The current single
`FrameBody<RequestPayload, ReplyPayload>` design has `SubscriptionEvent
{ event: ReplyPayload }`, but live contracts already show that
"reply payload" is conflating two relations:

- `signal-persona-terminal::TerminalEvent` carries direct replies
  (`TerminalInputAccepted`) AND pushed lifecycle events.
- `signal-persona-system::SystemEvent`, `HarnessEvent`, etc. — same
  pattern.

DA/64 recommends Shape B: split into `ExchangeFrameBody<R, P>` (no
subscription event variant) and `StreamingFrameBody<R, P, E>` (with a
distinct event payload axis). Channels declare which they use.

If Shape B lands, every downstream's `match frame.into_body() {
FrameBody::Request { ... } => ... }` switches to one of two new types.
That's another full migration pass through every daemon. Per
`skills/operator.md` §"Surface design gaps, don't paper over them",
the right move is to pause and let the designer settle Shape A vs
Shape B in /176/177.

User confirmed: pause.

### Also pending per DA/64

- `(Assert (Payload ...))` verb-wrapped NOTA grammar — the macro
  currently encodes payload enums as bare records (`(SubmitMessage ...)`,
  not `(Assert (SubmitMessage ...))`). Owner of this lives partly in
  `signal-core` (Operation/Request NOTA) and partly in the macro
  (payload enum NotaDecode). Tests need to add `(Verb (Payload ...))`
  round-trip witnesses.
- `RequestBuilderError::EmptyBatch` should be `EmptyRequest` per
  DA/64 §8 item 3.
- Generated `From<Payload>` impls break if two variants ever share a
  payload type (currently avoided by convention). Either remove
  generated `From` or enforce one-payload-per-variant explicitly.
- Architecture drift: `signal-core/ARCHITECTURE.md` and
  `skills/contract-repo.md` still need the six-roots / no-Atomic
  update (designer-assistant lane, per DA/63 F6).

## 3 · Naming-Skill Tension Noted

The spec uses `rule: &'static str` in `RequestRejectionReason::
ChannelPolicyViolation { rule, limit }` (and earlier
`RequestVerbMismatch::PolicyViolation`). The workspace `skills/rust/
methods.md` §"Don't hide typification in strings" calls that an
anti-pattern. My implementation kept the spec's `&'static str` shape
(`String` on the wire side, because rkyv won't archive `&'static str`).
Designer pass that absorbs DA/64 might revisit — a small enum like
`ChannelPolicyRule { MaxOps | ForbidSubscribe | ... }` would honor
both spec intent and workspace naming.

The spec also uses `max_ops` (the `op` abbreviation appears in the
naming-skill offender table — `op → operation`). I aligned with the
spec, but flagged it. Same recommendation: designer can decide.

## 4 · Operator Coordination

Operator was active in `persona-message` for the same kind of
supervision-codec migration. The lock entry surfaced before I touched
that repo; I left it untouched. Per `skills/operator-assistant.md`
§"Working with operator" + `skills/jj.md` §"Read jj st before every
commit", the coordination protocol worked here once I noticed.

The two ARCHITECTURE.md bundle slips (in signal-core v3 commit and
sema-engine v3 lock commit) were the inverse failure mode — I didn't
read `jj st` carefully before commit. The substance is intact (the
ARCHITECTURE.md changes describe the v3 shape correctly), but
attribution is muddled. Recoverable but worth noting.

## 5 · Pointers For Next Agent

| Need | Where |
|---|---|
| Live signal-core source | `/git/github.com/LiGoldragon/signal-core/src/` |
| Current signal-core spec | `reports/designer-assistant/61-signal-redesign-current-spec.md` |
| Implementation brief | `reports/designer-assistant/62-signal-redesign-implementation-brief.md` |
| Macro-gap research (the open Shape A vs Shape B question) | `reports/designer-assistant/64-signal-channel-macro-gap-research.md` |
| Designer macro spec (needs DA/64 absorption) | `reports/designer/176-signal-channel-macro-redesign.md` |
| Designer typed-request spec (needs DA/64 absorption) | `reports/designer/177-typed-request-shape-and-execution-semantics.md` |
| Worked example of v3 daemon migration | `/git/github.com/LiGoldragon/persona-mind/src/transport.rs` + `src/supervision.rs` |
| Worked example of v3 socket migration | `/git/github.com/LiGoldragon/terminal-cell/src/socket.rs` |

The Shape A vs Shape B decision needs to land in /176 and /177 before
the remaining six daemons can be migrated coherently. Once that's
settled, the migration pattern in persona-mind + terminal-cell is a
template that propagates.

## 6 · See also

- `reports/operator-assistant/115-context-maintenance-typed-request-thread-2026-05-15.md`
  — pre-v3 thread-state snapshot.
- `reports/designer-assistant/61-signal-redesign-current-spec.md` —
  current compact spec.
- `reports/designer-assistant/64-signal-channel-macro-gap-research.md`
  — the Shape A/B / verb-wrapped NOTA / `From<Payload>` gaps.
- `~/primary/skills/operator-assistant.md` — the role's discipline.
- `~/primary/skills/jj.md` §"Read jj st before every commit" — the
  procedural rule I missed twice for ARCHITECTURE.md bundles.
