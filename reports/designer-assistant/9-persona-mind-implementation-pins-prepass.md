# 9 - Persona-mind implementation pins pre-pass

*Designer-assistant report for bead `primary-qqb`. Scope: reread
`reports/designer/100-persona-mind-architecture-proposal.md` against
current `persona-mind` after the Kameo migration and decide which of the
five implementation pins are still load-bearing.*

---

## Short answer

All five designer/100 pins still matter. None has been implemented in
the shape designer/100 described.

Two pins are ready to implement with small naming/spec refreshes:

- `DisplayId` minting
- `mind.redb` path configuration

Two pins need a sharper implementation spec before an operator should
code them:

- sema table key shapes
- caller identity resolution

The subscription sketch survives, but it should not be bundled with the
first durable-store implementation. It needs a later contract/runtime
bead after durable commit events exist.

Do not file one bead for all five pins. The right split is:

1. `MindStorePath + IdMint + mind-local sema tables` - pins 1, 2, and 4.
2. `CallerIdentityResolver + daemon envelope boundary` - pin 3.
3. `Subscription contract and post-commit push` - pin 5, blocked by the
   durable event log and daemon transport.

---

## Current state checked

I stayed read-only in `persona-mind`. At inspection time,
`operator.lock` owned
`/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md`, and that file
already had peer edits. This report uses the current working tree as
evidence but does not edit it.

Relevant current state:

- `persona-mind` is past commit `d167d120a7e4` (`mind: align kameo actor
  vocabulary`); current parent seen was `8706404cb49e` (`docs: define
  daemon-backed mind architecture`).
- `persona-mind/src/service.rs` still exposes `MindRuntime` as an
  in-process facade around `ActorRef<MindRoot>`.
- `persona-mind/src/main.rs` is still scaffold-level.
- `persona-mind/Cargo.toml` has no `persona-sema`, `sema`, `redb`,
  `blake3`, or base32 dependency.
- `persona-mind/src/memory.rs` still stores the graph in vectors.
- `signal-persona-mind/src/lib.rs` still declares a request/reply channel
  with no subscription variants; its file header says subscription mode is
  a future extension.

The main implementation gap is unchanged from
`reports/operator/105-command-line-mind-architecture-survey.md`: the
runtime has a real Kameo path for memory/work graph requests, but durable
`mind.redb`, role/activity flows, NOTA CLI text projection, and subscription
push are not built.

---

## Verdict table

| Pin | Verdict | Why |
|---|---|---|
| 1. `DisplayId` mint algorithm | Still-live, needs small refresh | Current code has `DisplayIdMint`, but it is a counter-to-base32 helper, not the BLAKE3 + collision-extension design. |
| 2. Sema table key shapes | Still-live, needs refresh | No durable mind tables exist. The key idea survives, but table ownership and key encoding should align with `sema::Table` and `persona-sema`'s current boundary. |
| 3. Caller identity resolution | Still-live, needs refresh | The runtime uses `MindEnvelope.actor` correctly once supplied, but no resolver exists. The daemon/thin-client decision changes where identity can be resolved. |
| 4. `mind.redb` path with env override | Still-live, ready after naming choice | Current `StoreLocation` is a plain string passed by tests. There is no default path or env override. |
| 5. Subscription contract sketch | Still-live, later bead | Current contract is request/reply only and explicitly defers subscriptions. Runtime has a placeholder `SubscriptionSupervisor`, not a commit bus/subscriber contract. |

---

## Pin 1 - `DisplayId` mint algorithm

Designer/100 says `IdMintActor` should mint a short `DisplayId` by
base32-crockford encoding a BLAKE3 digest of `StableItemId`, starting at
three characters and extending on collision.

Current implementation:

- `Graph::open` increments `next_item`.
- `StableItemId` is `format!("item-{:016x}", self.next_item)`.
- `DisplayIdMint::into_display_id` encodes the counter into five
  lowercase crockford-like characters.
- There is no collision index and no persisted display-id table.

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:91`
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:398`
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:407`

The pin is still load-bearing. Short human IDs are central to the native
mind replacing BEADS (`primary-qqb`, `primary-9iv`, etc.). The current
five-character counter is fine as a test scaffold, but it is not the
durable identity shape.

Spec refresh:

- Use Kameo naming: the actor type should be `IdMint`, not `IdMintActor`.
- Make `IdMint` data-bearing. It should own at least a workspace/store
  salt, display-id collision index, and counters or access to persisted
  `meta` rows.
- Add explicit table/index writes for `display_ids`, not just item fields.
- Add dependencies: `blake3` and a base32-crockford implementation or a
  small private encoder type owned by `IdMint`.
- Add tests for default length, collision extension, repeat prevention,
  and imported BEADS aliases staying aliases rather than display IDs.

Implementation can bundle this with pin 2 and pin 4 because display-id
minting needs the durable tables and store path anyway.

---

## Pin 2 - Sema table key shapes

Designer/100 gives concrete logical keys:

- claims keyed by role/scope
- handoffs keyed by operation
- activities and events keyed by event sequence
- items keyed by stable item ID
- edges by source and target
- notes by item/event
- aliases/display IDs by external or display identity
- meta by static key

Current implementation:

- No `persona-sema` or `sema` dependency exists in `persona-mind`.
- `MemoryState` stores `items`, `edges`, `notes`, and `events` in vectors.
- `persona-sema` currently stores umbrella `signal-persona` records only.
- `persona-sema/ARCHITECTURE.md` says mind-specific tables should default
  to `persona-mind/src/tables.rs` over `sema` until reuse is real.

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/Cargo.toml`
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:44`
- `/git/github.com/LiGoldragon/persona-sema/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/sema/src/lib.rs:266`

The pin is still load-bearing, but the implementation spec should be
updated before coding.

Spec refresh:

- Put mind-private table declarations in `persona-mind/src/tables.rs`,
  not `persona-sema`, unless a second component truly needs the same
  table identity.
- Use lowercase redb table names (`items`, `edges_by_source`,
  `edges_by_target`, `notes_by_item`, `aliases`, `display_ids`, etc.)
  to match current `sema::Table` convention; Rust constants can still be
  uppercase.
- Use named key types where the relation is meaningful:
  `ClaimKey`, `SourceEdgeKey`, `TargetEdgeKey`, `NoteKey`,
  `DisplayIdKey`, `AliasKey`.
- Avoid rkyv archives as keys. Compound keys should be designed bytes
  behind those key types, or another explicit `redb::Key` shape if it
  reads better and range scans still work.
- Keep `EventSeq` and other numeric range keys big-endian if they are
  byte keys; numeric `u64` keys are also acceptable when no compound
  prefix is needed.

This should be a real implementation bead, not more architecture churn.
The only refresh needed is the table-module ownership and key-type naming.

---

## Pin 3 - caller identity resolution

Designer/100 says caller identity is resolved before persistence and wrapped
with the request as `MindEnvelope { actor, request }`.

Current implementation:

- `MindEnvelope` already carries `actor: ActorName` plus `request:
  MindRequest`.
- The actor path correctly stamps `EventHeader.actor` from the envelope.
- Tests prove two runtime envelopes with different actors produce events
  stamped with those actors.
- `MemoryState::dispatch` still has a fallback default actor of
  `ActorName::new("persona-mind")`, but the Kameo runtime path uses
  `dispatch_envelope`.
- There is no `CallerIdentityResolver`; ingress only records the trace
  phase.

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/envelope.rs:4`
- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:383`
- `/git/github.com/LiGoldragon/persona-mind/tests/weird_actor_truth.rs:499`
- `/git/github.com/LiGoldragon/persona-mind/src/actors/ingress.rs:38`

The pin is still load-bearing, but the daemon decision changes the
implementation shape.

Designer/100's three resolution sources (`MIND_ACTOR`, actor config, process
ancestry) were written before the daemon decision landed. In the daemon
shape, the CLI is a thin client and the daemon owns `MindRoot`. If the CLI
only sends a bare `MindRequest` frame, the daemon cannot see the CLI's
environment or process ancestry except through local transport metadata.

Spec refresh:

- Keep `MindRequest` actorless. Request payloads still must not carry
  authority.
- Use `MindEnvelope` or a crate-local `MindSubmission` as the local daemon
  boundary, not as a public `signal-persona-mind` payload variant.
- Decide explicitly which process resolves identity:
  - CLI resolves from `MIND_ACTOR` or actor config and sends a local
    envelope over the trusted local transport; or
  - daemon resolves from socket peer credentials plus registered process
    ancestry and wraps the request itself.
- Rename the implementation target to `CallerIdentityResolver` to match
  current actor-systems naming.
- Add tests for "request body cannot supply actor", "resolved actor stamps
  event header", and "identity failure returns typed rejection".

My recommendation: CLI-side resolution is simpler for the first local
workspace daemon, but it must be framed as infrastructure envelope data,
not a request field. Daemon-side validation can harden later if multi-user
trust becomes real.

This should be its own bead because it crosses CLI, daemon transport, and
runtime envelope semantics.

---

## Pin 4 - `mind.redb` path and env override

Designer/100 pins a default path plus env override. The bead text says
`PERSONA_MIND_DB`; designer/100 itself says `MIND_DB_PATH`. Current code has
neither.

Current implementation:

- Tests call `StoreLocation::new("mind.redb")`.
- `StoreLocation` is a `String` wrapper with no default, no path expansion,
  and no environment reader.
- `Config` stores the passed `StoreLocation`; its only read message is dead
  code.

Evidence:

- `/git/github.com/LiGoldragon/persona-mind/src/memory.rs:432`
- `/git/github.com/LiGoldragon/persona-mind/src/actors/config.rs:7`
- `/git/github.com/LiGoldragon/persona-mind/tests/actor_topology.rs:16`

The pin is still load-bearing and ready to implement after one naming
choice.

Spec refresh:

- Prefer `PERSONA_MIND_DB` over `MIND_DB_PATH`; it is component-specific
  and matches the bead.
- Default to `~/primary/.mind/mind.redb` for the current workspace.
- Read the env override in the daemon/config boundary, not in random store
  call sites.
- Replace `StoreLocation` with a more exact name if implementation touches
  it: `MindStorePath` or `MindDatabasePath`.
- Add tests for default path, env override, and test isolation with an
  explicit temporary path.

This belongs with the durable-store/table/ID bead.

---

## Pin 5 - subscription contract sketch

Designer/100 sketches `Subscribe`, `Unsubscribe`, `SubscriptionAccepted`,
`SubscriptionEvent`, and filters such as `Coordination`, `Memory`, and
`EventsForItem`.

Current implementation:

- `signal-persona-mind` is request/reply only.
- The contract header says subscription mode is a future extension.
- `SubscriptionSupervisor` only increments `post_commit_count` and records
  `CommitBus` in a trace for a dead-code message.
- No durable commit event stream exists yet.

Evidence:

- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:21`
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:856`
- `/git/github.com/LiGoldragon/persona-mind/src/actors/subscription.rs:7`

The pin is still load-bearing for push-not-pull, but it is not the first
implementation bead.

Spec refresh:

- Subscription is a schema change in `signal-persona-mind`; it should not
  be hidden inside `persona-mind`.
- The first subscription event should be defined after the durable event
  model lands, so filters can talk about real committed records rather than
  in-memory vector snapshots.
- On-connect current-state emission remains the right rule, but the state
  source should be durable views/readers, not the current `MemoryState`.

This should become a separate bead after durable `mind.redb`, `EventSeq`,
and post-commit event append exist.

---

## Recommended beads

### Bead A - durable mind store foundation

Scope:

- implement `MindStorePath` / `PERSONA_MIND_DB` / default
  `~/primary/.mind/mind.redb`;
- add `sema` or `persona-sema` integration according to the
  `persona-sema` boundary rule;
- add mind-local table declarations and key types;
- implement `IdMint` over durable/meta state;
- replace counter-only stable/display IDs for durable writes.

This bead covers pins 1, 2, and 4.

### Bead B - caller identity and daemon envelope boundary

Scope:

- implement `CallerIdentityResolver`;
- define whether the CLI or daemon resolves caller identity in v1;
- submit `MindEnvelope`/local `MindSubmission` to `MindRoot` without adding
  actor fields to `MindRequest`;
- remove or quarantine the `MemoryState::dispatch` default actor path from
  production runtime use;
- add identity failure and event-header tests.

This bead covers pin 3.

### Bead C - post-commit subscriptions

Scope:

- extend `signal-persona-mind` with subscription request/reply/event types;
- implement commit-bus fanout after durable commit;
- implement on-connect state emission through durable views;
- prove no polling path exists.

This bead covers pin 5 and should wait until bead A has landed.

---

## Final recommendation

Operator-assistant should not claim "designer/100 pins" as one bundled
implementation bead. That bundle would mix durable storage, identity trust,
CLI/daemon transport, and future subscriptions.

The live work should start with bead A. It is the highest-leverage slice:
without durable `mind.redb`, explicit table keys, and real store-minted IDs,
the command-line mind still cannot replace BEADS or lock files. Bead B can
run next or in parallel if the implementer has the daemon boundary in view.
Bead C should stay separate.
