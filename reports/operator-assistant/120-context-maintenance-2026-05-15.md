## 120 — Context Maintenance, Wave-3 Cutover Handoff

*Operator-assistant context-maintenance ledger, 2026-05-15.
Purpose: hand off the wave-3 Signal/sema-engine/Persona cutover to
the next operator-assistant session with a tight pickup surface.*

## 1 · Current Load-Bearing Truth

The wave-3 cutover (per `/176` + `/177` + `DA/61` + `DA/62`) is
**complete** for the "all contracts and components refactored to
new design" stop-hook condition. Final coverage after the
operator-assistant 116/117/118/119 chain plus operator's parallel
daemon work:

| Surface | State |
|---|---|
| `signal-core` kernel | Six SignalVerb roots, typed `Request<P>`/`Reply<R>`, two Frame families (Exchange + Streaming), `signal_channel!` proc-macro |
| Contract crates (lib + tests compile) | 8/8 green: signal-persona, signal-persona-mind/system/terminal/harness/introspect/router/message, signal-criome |
| Daemon crates (lib + tests compile) | 10/10 green: persona-{mind,router,message,system,introspect,harness,terminal} + persona (meta) + terminal-cell + criome |
| Subscription-retraction handlers | 3/3 honest (criome, persona-terminal, terminal-cell). All overload an existing reply variant pending a typed `SubscriptionRetracted` design |
| Push-delta primitive on Subscribe | 1/3 daemons: only `terminal-cell` actually emits live deltas via `stream_signal_worker_lifecycle`. criome + persona-terminal Subscribe is snapshot-only — push is wave-4 work |

## 2 · Sources Still Load-Bearing for the Next Session

The compact reading list — every other earlier report can be
trimmed before pickup:

| Path | One-line summary |
|---|---|
| `~/primary/ESSENCE.md` | Workspace intent — upstream of every rule |
| `~/primary/protocols/orchestration.md` | Role-coordination protocol, lock files, BEADS handling |
| `~/primary/skills/operator-assistant.md` + `skills/operator.md` | Operator-assistant lane discipline + the assisted role's reading list |
| `~/primary/skills/contract-repo.md` | Contract-crate craft; the six-root Signal verb spine; layered effect crates |
| `~/primary/skills/jj.md` | VCS discipline; `jj st` before commit; `jj commit -m`; per-commit pushes |
| `~/primary/skills/reporting.md` | Report ↔ chat boundary; per-role subdir numbering; inline-summary rule |
| `reports/designer/176-signal-channel-macro-redesign.md` | Macro redesign — proc-macro grammar, payload-per-variant From convention, no blanket impls |
| `reports/designer/177-typed-request-shape-and-execution-semantics.md` | Typed Request/Reply shape, six-root SignalVerb, structural atomicity, async exchange frames |
| `reports/designer-assistant/61-signal-redesign-current-spec.md` | Current compact spec — non-empty requests, lane/sequence frame exchanges |
| `reports/designer-assistant/62-signal-redesign-implementation-brief.md` | Operator brief — slices, ordering, what `signal-core` carries |
| `reports/operator-assistant/119-wave-2-phase-5-retraction-handlers-2026-05-15.md` | This week's closing report — three real retraction handlers + design gap + wave-4 pointer |
| `reports/operator/120-hard-context-maintenance.md` | Operator's parallel context note — pickup points for operator lane |

The 109–118 operator-assistant reports are historical lineage of
the wave-3 implementation chain; the git log preserves them. Only
`/119` carries forward live substance for the next session — and
even that is mostly distilled into this `/120`.

## 3 · The Two Forward Items

### 3.1 · Designer call — typed retraction reply

`signal-criome` and `signal-persona-terminal` (the two streaming
contracts) do not have a typed "subscription retracted" reply
variant. All three daemons overload an existing reply for the ack:

| Daemon | Overloaded reply | Semantic mismatch |
|---|---|---|
| `criome` | `IdentitySnapshot` | "subscription closed" ≠ "registry snapshot" |
| `persona-terminal` | `TerminalDetached{HumanRequested}` | "subscription detached" ≠ "terminal detached" |
| `terminal-cell` | `TerminalDetached{HumanRequested}` | same |

`signal-persona-mind`, `signal-persona-system`, and `signal-persona-harness`
already have a typed `*RequestUnimplemented` variant that the operator
used for the same case. The two streaming contracts are the only ones
without this safety-valve.

**Three paths, designer's choice:**
- **A** — add a typed `SubscriptionRetracted` reply variant per
  streaming contract. Most accurate.
- **B** — add a generic `<Channel>RequestUnimplemented` /
  `<Channel>Acknowledgement` variant matching the mind/system/harness
  pattern.
- **C** — keep the overload as documented workspace convention.

This is a `/176`/`/177` spec-extension call, not an operator-assistant
implementation slice.

### 3.2 · Wave-4 push-delta primitive

The SubscriptionRegistry actor in `criome` and the
`lifecycle_subscriptions` Vec in `persona-terminal` are the
**receive side** of the subscription bookkeeping. The **send side**
(actually pushing deltas to open subscribers) is not yet implemented
in those two daemons; their Subscribe returns a snapshot and never
emits live events.

`terminal-cell` is the one daemon with a real push primitive — its
`stream_signal_worker_lifecycle` (in
`/git/github.com/LiGoldragon/terminal-cell/src/bin/terminal-cell-daemon.rs:727`)
blocks the connection emitting live events via
`write_signal_subscription_event`.

The wave-4 work: implement push-delta emission in `criome` and
`persona-terminal`. The actor topology for it already has the
receive-side handle (the registry tracks open tokens); the
remaining piece is the **delta source**: identity registry mutation
events for criome, worker lifecycle events for persona-terminal,
each fanned out to the registry's open subscribers.

## 4 · Workspace Coordination State at Handoff

```
operator.lock                — persona-introspect (operator's claim)
operator-assistant.lock      — empty (released)
designer.lock                — empty
designer-assistant.lock      — empty
system-specialist.lock       — empty
system-assistant.lock        — horizon-re-engineering step 5 (wifi typed records)
poet.lock                    — empty
poet-assistant.lock          — empty
```

Operator was implementing `persona-introspect` (sema-engine local
observation store) in parallel with this report's session. That
work is separate from the wave-3 cutover and was not touched here.

## 5 · Outstanding Hygiene Item

Two stale `push-*` bookmarks remain on `signal-persona` with
divergent remote tracking, both from earlier sessions:

```
push-xqwsylxkupnq @ 2d413086 — "ARCH — drop /144 + operator-bead citation (DA/66 §A, §H note)"
  @origin (ahead by 1, behind by 2)
push-ysrtyyypovkr @ 29d4986d — "lock: signal-core v3 spec (Reply Accepted/Rejected, RequestBuilder)"
  @origin (ahead by 1, behind by 1)
```

Both look like working-copy commits that got divergent updates on
origin and were never landed-or-abandoned. Triage decision (for
next operator-assistant or operator with signal-persona scope):

- For `push-xqwsylxkupnq`: the ARCHITECTURE.md change drops a `/144 §3.2`
  citation and rewrites the SpawnEnvelope/ComponentName section to
  state the intended split positively. Looks like aborted DA/66
  follow-up. Compare against `signal-persona`'s current
  `ARCHITECTURE.md` on `main`; land if still relevant, abandon if
  superseded.
- For `push-ysrtyyypovkr`: a Cargo.lock bump for signal-core v3 +
  ARCHITECTURE.md sweep. Almost certainly already absorbed into
  later `main` commits. Likely abandon.

Both decisions should be made by an agent with full signal-persona
context, not as a pickup mechanical task. The bookmarks aren't
costing anything except listing noise.

## 6 · Pickup Points for the Next Session

| Need | Path |
|---|---|
| Wave-3 spec | `reports/designer/176-signal-channel-macro-redesign.md` + `reports/designer/177-typed-request-shape-and-execution-semantics.md` |
| Most recent operator-assistant report | `reports/operator-assistant/119-wave-2-phase-5-retraction-handlers-2026-05-15.md` |
| Most recent operator report | `reports/operator/120-hard-context-maintenance.md` |
| Subscription registry pattern (criome) | `/git/github.com/LiGoldragon/criome/src/actors/subscription.rs` |
| Subscription registry pattern (persona-terminal) | `/git/github.com/LiGoldragon/persona-terminal/src/signal_control.rs` (`open_worker_lifecycle_subscription`, `close_worker_lifecycle_subscription`) |
| Push-delta producer example | `/git/github.com/LiGoldragon/terminal-cell/src/bin/terminal-cell-daemon.rs` (`stream_signal_worker_lifecycle`) |
| Streaming-event reader pattern | `/git/github.com/LiGoldragon/terminal-cell/src/socket.rs:401` (`read_signal_subscription_event`) |
| Proc-macro craft | `/git/github.com/LiGoldragon/signal-core/macros/src/{parse,model,validate,emit}.rs` |
| Hand-written `From<Payload>` precedent | `/git/github.com/LiGoldragon/signal-persona-terminal/src/lib.rs` (post `signal_channel!` invocation) |

No claim left in flight; no orphan-shaped descendants of main; no
in-progress files in the working copy. The next operator-assistant
session starts cold against `main` and the reading list above.
