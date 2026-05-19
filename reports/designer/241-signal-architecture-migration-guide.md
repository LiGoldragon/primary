# 241 — Signal architecture migration guide

*Refresh of the migration playbook now that the foundation has
landed. Supersedes `/239` as the practical reference for any agent
migrating a signal-* / owner-signal-* contract or its consumer
daemon. The foundation crates (`signal-frame`, `signal-sema`) are
real; the `signal_channel!` macro speaks the new shape; design
smells in the kernel are cleaned up. This is the spec, not a plan.*

## 0 · TL;DR

Two foundation repos exist on `main`:

| Repo | URL | Role |
|---|---|---|
| `signal-frame` | https://github.com/LiGoldragon/signal-frame | Frame envelope, length-prefixed rkyv archives, handshake, exchange identifiers, async correlation, streams, reply plumbing, the `signal_channel!` macro. **No `SignalVerb`. No Sema verbs.** |
| `signal-sema` | https://github.com/LiGoldragon/signal-sema | The six Sema operations (`Assert / Mutate / Retract / Match / Subscribe / Validate`), pattern primitives (`PatternField<T>`), typed identity primitives (`Slot`, `Revision`). Consumed by daemons that lower contract verbs to Sema operations; speakable on the wire only when a component explicitly exposes typed-table operations. |

The migration spec for any contract:

1. Switch Cargo dependency from `signal-core` to `signal-frame` (add `signal-sema` only if the daemon speaks Sema directly).
2. Rewrite the `signal_channel!` invocation in the new shape (§2 below).
3. Pick contract-local operation roots in **verb form** (§4).
4. Move verb-to-Sema lowering into the daemon executor (§5).
5. Add the universal observer hook for introspection (§6).
6. Update tests + ARCHITECTURE.md.

## 1 · Foundation state — what you can rely on

### `signal-frame` (commit `4bdf1e1e` and later)

Owns and exports:

- `Frame`, `ExchangeFrameBody`, length-prefixed encoding.
- `HandshakeRequest`, `HandshakeReply`, `ProtocolVersion`,
  `SIGNAL_FRAME_PROTOCOL_VERSION`.
- `Request<Payload>` with `payloads: NonEmpty<Payload>`
  (no `Operation` wrapper anymore — collapsed per `/240`).
- `RequestBuilder<Payload>`, `RequestPayload` marker trait.
- `Reply<…>`, `SubReply<…>`, `RequestRejectionReason::Internal`
  for daemon-level pre-execution rejection.
- `NonEmpty<T>`.
- Stream / subscription lifecycle primitives.
- The `signal_channel!` macro (in `signal-frame-macros`).

No verb tagging anywhere. No `Operation<Payload>` wrapper.
No `check()` function pretending to do universal validation.

### `signal-sema`

Owns:

- `SemaOperation` (the six verbs as an enum).
- `OperationClass` (read / write classification).
- `PatternField<T>: Wildcard | Bind | Match(T)`.
- `Slot<Payload>`, `Revision` — typed identity primitives
  for `Mutate` / `Retract` addressing.
- Round-trip witnesses (rkyv + NOTA) for the verbs and
  patterns.

Does **not** own `ReadPlan` operators (`Constrain`,
`Project`, `Aggregate`, `Infer`, `Recurse`) — those live in
`sema-engine` and per-contract read payloads.

`signal-sema` does not depend on `signal-frame`. A daemon
that consumes both pulls them independently.

## 2 · The new `signal_channel!` shape

The canonical example (from `signal-frame` `tests/channel_macro.rs`):

```rust
signal_channel! {
    channel Message {
        operation Submit(Submission),
        operation Query(InboxQuery),
    }
    reply MessageReply {
        Accepted(Receipt),
        Inbox(Inbox),
    }
}
```

What the macro generates (key surface):

- A request enum named after the channel: `MessageOperation`,
  variants `Submit(Submission)` and `Query(InboxQuery)`.
- An impl `impl RequestPayload for MessageOperation {}`.
- A reply enum `MessageReply` with the variants you declared.
- NOTA codec on both (rkyv on the wire, NOTA on text surfaces).
- Frame aliases (`MessageFrame`, `MessageChannelRequest`, etc.).

What the macro does **not** generate any more:

- `fn signal_verb(&self) -> SignalVerb` — gone.
- An outer `Operation<Payload>` wrapper — gone.
- A verb-tagged variant declaration syntax — rejected at the
  macro grammar level (compile-fail witness in
  `signal-frame/tests/ui/channel_macro_compile_fail/old_verb_tagged_shape.rs`).

### NOTA encoding of requests

```
Single-payload request:
  (Submit (Submission hello))

Multi-payload request:
  [(Submit (Submission first)) (Query (InboxQuery operator))]
```

No outer `(Assert …)` / `(Match …)` wrapper. The operation
root is the contract-local verb directly.

### Streams

A stream block declares the open / event / close cycle. Stream
close is now contract-local — no `Retract` requirement. The
macro validates that the close operation's payload type
matches the stream token type.

```rust
signal_channel! {
    channel Inbox {
        operation Watch(WatchRequest) opens InboxStream,
        operation Unwatch(InboxStreamToken),
        operation Query(InboxQuery),
    }
    reply InboxReply { … }
    event InboxEvent {
        MessageReceived(MessageReceived) belongs InboxStream,
    }
    stream InboxStream {
        token InboxStreamToken;
        opened InboxStreamOpened;
        event MessageReceived;
        close InboxStreamToken;
    }
}
```

The contract author picks `Watch` / `Unwatch` / `Detach` /
`Cancel` etc. as the close verb — whatever reads in domain
terms. The macro enforces token/payload-type alignment but
not the verb name.

## 3 · Per-component migration checklist

For each `signal-<component>` / `owner-signal-<component>`
repo:

### A. Cargo dependency switch

```toml
# OLD
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git", branch = "main" }

# NEW
signal-frame = { git = "https://github.com/LiGoldragon/signal-frame.git", branch = "main" }

# Only if the daemon speaks Sema directly (executor lowering,
# introspection, sema-engine integration):
signal-sema = { git = "https://github.com/LiGoldragon/signal-sema.git", branch = "main" }
```

Remove any imports of `SignalVerb`, `Operation`, `PatternField`
(the latter moves under `signal_sema::PatternField`).

### B. Macro invocation

Rewrite the `signal_channel!` invocation per §2. Drop:

- The `Assert / Mutate / Retract / Match / Subscribe / Validate`
  prefixes on every variant.
- The explicit `request <Name> { … }` block — the macro derives
  the request enum name from the channel name.
- Any `Retract` shape for stream close — use a contract-local
  verb (`Unwatch`, `Detach`, etc.).

Lift repeated category words (`*Query`, `*Subscription`,
`*Observation`) to operation roots. Sibling variants sharing
a suffix indicate a missing public verb.

### C. Operation root naming — verb form

The operation root names the **client's action in verb form**,
not the noun derived from it.

| Wrong (noun form) | Right (verb form) |
|---|---|
| `Statement` | `State` (or `Announce`, `Greet`, …) |
| `Submission` | `Submit` |
| `Observation` | `Observe` |
| `Registration` | `Register` |
| `Configuration` | `Configure` |
| `Retirement` | `Retire` |
| `Adjudication` | `Adjudicate` |

Cross-contract verb reuse is fine and expected — `Configure`,
`Observe`, `Register` are common; same verb means different
things depending on which daemon receives it.
*"For a bird to lower itself, it changes the angle of its
wings. But for a cloud to lower itself, it changes its
temperature."*

### D. Move verb-to-Sema lowering into the daemon executor

The contract does not declare which Sema verbs its
operations lower to. The daemon's executor decides at
runtime: based on the operation, the payload, the daemon's
policy state, and any routing decisions.

The lowering may be 0 → many Sema operations:

- `Submit Message` might lower to `[Assert IngressEvent,
  Mutate DeliveryState]` if accepted, to nothing if
  rejected, or to a forwarded request if routed.
- `Query RecentRepositories` might lower to several `Match`
  plans against different indexes.
- `Configure DaemonConfiguration` lowers to `Mutate` of
  the singleton policy record.

The executor takes the contract operation, computes the
Sema-operation sequence (or rejects with
`RequestRejectionReason::Internal` for pre-execution
failures), executes against the `redb` tables via
`sema-engine`, and produces a reply.

### E. Observer hook

Every daemon publishes its inbound contract operations and
outbound Sema effects to optional observers. The mechanism:

- The daemon defines an internal observer lane on its
  **public socket** (not the owner socket — observation is
  not security-sensitive; no secrets cross the wire).
- A subscriber (typically `persona-introspect`) subscribes
  to one of: inbound operations, outbound Sema effects, or
  both, by event class.
- When a message arrives or a Sema effect happens, the
  daemon checks the subscriber set and sends a copy to
  each.

The contract crate declares the observation types; the
daemon implements the emission logic.

### F. Update ARCHITECTURE.md

- Remove the `## MUST IMPLEMENT — signal architecture
  migration` section once the refactor lands.
- Add `## Migration history — contract-local verbs
  (2026-05-XX)` noting the shape change.
- Update the §"Owns" list to reflect the new types.

### G. Tests

- Round-trip tests (rkyv + NOTA) for each contract operation
  with the new shape.
- The verb-mapping tests are retired (no `signal_verb()`).
- Add tests for daemon-executor lowering where the
  Sema-effect sequence is deterministic.

## 4 · Verb-form naming — settled rules

Per `intent/naming.nota` 2026-05-19T19:45Z and `skills/naming.md`:

1. **Full English words.** `Request` not `Req`. `Identifier`
   not `Id`. CPU / URL / HTTP / JSON allowed as English-passed
   acronyms; `id` is not.
2. **No redundant ancestry.** Inside `signal-persona-spirit`
   the type is `Entry`, not `IntentEntry` (intent is the
   crate's domain).
3. **Verb form for operation roots.** `State` not `Statement`;
   `Submit` not `Submission`.
4. **Repeated category words across siblings = missing
   verb.** Lift the repeated word to the operation root.

## 5 · Daemon-side: verb-to-Sema lowering

The daemon owns the executor. Sketch of a typical handler:

```rust
fn handle(&mut self, request: Request<MessageOperation>) -> Reply<MessageReply> {
    let mut sema_effects = Vec::new();
    for payload in request.payloads() {
        match payload {
            MessageOperation::Submit(submission) => {
                if !self.policy.accepts(submission) {
                    return Reply::Rejected { reason: Internal { … } };
                }
                sema_effects.push(SemaOperation::Assert(self.to_ingress_event(submission)));
                sema_effects.push(SemaOperation::Mutate(self.to_delivery_mutation(submission)));
            }
            MessageOperation::Query(query) => {
                sema_effects.push(SemaOperation::Match(self.to_inbox_match(query)));
            }
        }
    }
    let outcomes = self.sema_engine.execute(sema_effects)?;
    // Emit Sema effects to observers, build reply from outcomes.
    Reply::Accepted { per_operation: outcomes.into_replies() }
}
```

The lowering is daemon code, not contract code. Each daemon
decides its own translation. The same contract verb can
produce entirely different Sema effects across receivers.

## 6 · Reference contracts and current state

For grounding when designing your contract's shape:

- **`signal-frame/tests/channel_macro.rs`** — the canonical
  worked example of the new macro shape.
- **`signal-frame/tests/frame.rs`** — request / reply
  round-trip with payload-only `NonEmpty<Payload>`.
- **`signal-frame/tests/ui/channel_macro_compile_fail/`** —
  what the macro rejects: old verb-tagged grammar, orphan
  streams, payload/token mismatches.
- **`signal-sema/tests/`** — `SemaOperation` and
  `PatternField` round-trips.
- **`reports/operator/138-signal-frame-macro-migration-work.md`** —
  the macro migration that landed in commit `3526c108`.
- **`reports/designer/240-signal-frame-operation-collapse-check-removal.md`** —
  the kernel cleanup that landed in commit `4bdf1e1e`.

## 7 · Migration order

### Phase 1 — Foundation (done)

- ✓ `signal-frame` repo created with frame mechanics.
- ✓ `signal-sema` repo created with the 6 verbs + patterns.
- ✓ The `signal_channel!` macro rewritten for contract-local
  operations.
- ✓ Two kernel design smells (transparent `Operation`,
  always-Ok `check`) removed.
- ✓ `MUST IMPLEMENT` notes in 19 affected contract repos.
- ✓ Skills updated: `skills/contract-repo.md`,
  `skills/naming.md`, `skills/language-design.md` references.

### Phase 2 — Pilot (next)

`signal-repository-ledger` is the pilot. Refactor produces
the canonical worked example for the rest. Open work:
contract refactor + repository-ledger daemon executor
implementation. Per `MUST IMPLEMENT` note: `Query`,
`Receive`, `Observe` as operation roots.

### Phase 3 — Component contracts (parallel)

After the pilot lands and produces the worked example:

- `signal-persona-spirit` (operator pickup — bead
  `primary-ojxq`, scope expanded for the broader refactor).
- `signal-persona-mind` (split confirmed:
  `Grant`/`Extend`/`Revoke`/`Adjudicate`/`Deny`/`Query`
  for the channel-choreography family).
- `signal-persona` (settled: `Announce` for
  `ComponentHello`; unified `Query` over readiness + health;
  `GracefulStop` migrates to `owner-signal-persona` when
  that repo is created).
- `signal-persona-orchestrate`, `signal-persona-router`,
  `signal-persona-harness`, `signal-persona-message`,
  `signal-persona-terminal`, `signal-persona-auth`.
- `signal-criome` — open psyche question: stay as one
  channel (19 variants, risks Watch-collisions) or split
  into three (`signal-criome-identity`,
  `signal-criome-attestation`, `signal-criome-peer`).
- All `owner-signal-*` counterparts.
- `signal-forge`, `signal-lojix`.

Each component's `ARCHITECTURE.md` carries a `MUST
IMPLEMENT` note with the proposed shape for that contract.

### Phase 4 — Cleanup

- `signal-core` deprecated / archived with README pointing
  at `signal-frame` + `signal-sema`.
- Cross-references in skills / lore / reports updated.

## 8 · Coordination

- **Don't dispatch agents to redo the macro work.** The
  macro is functional; further work is contract migration.
- **Don't backfill the 5 missing `owner-signal-persona-*`
  repos** (mind, router, harness, message, auth) by
  assumption. The psyche has named these as intentional
  gaps that emerge as each component's owner discipline
  crystallizes.
- **Use reports as the documentation substrate** — beads
  are not psyche-visible. If a bead is referenced, also
  carry the substance in the report.
- **Verbs reuse across contracts.** Don't invent new verbs
  when an existing one fits the domain action; the
  receiver determines the effect.
- **When in doubt, surface to the psyche** per
  `skills/intent-clarification.md`. Don't infer
  architecture from absence of intent.

## 9 · References

- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
  — the broad direction (why this migration exists).
- `reports/designer/239-signal-architecture-migration-plan.md`
  — superseded by this report for practical guidance; kept
  for the foundation-phase planning record.
- `reports/operator/138-signal-frame-macro-migration-work.md`
  — the macro migration that delivered the new shape.
- `reports/designer/240-signal-frame-operation-collapse-check-removal.md`
  — the kernel cleanup.
- `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md`
  — the architectural analysis behind the redirection.
- `intent/component-shape.nota` — the psyche statements
  driving the redirection (2026-05-19T19:30Z onward).
- `intent/naming.nota` — verb-form-not-noun-form rule and
  contract-local-verb confirmation.
- `intent/workspace.nota` — chat brevity, no vague
  references, reports over beads, agent-failure-equals-
  guideline-failure.
- `skills/contract-repo.md` §"Public contracts use
  contract-local operation verbs" — the discipline form of
  this guide.
- `skills/naming.md` — the naming pair (full English words
  + no redundant ancestry) and the repeated-category-words
  anti-pattern.
- `ESSENCE.md` §"Naming" — the upstream rules.
