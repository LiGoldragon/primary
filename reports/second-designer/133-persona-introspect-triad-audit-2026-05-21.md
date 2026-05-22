# 133 — persona-introspect triad audit (2026-05-21)

*Audit of the persona-introspect triad: `signal-persona-introspect`
(working contract) + `persona-introspect` (daemon + thin CLI). The
owner contract `owner-signal-persona-introspect` is missing; this
report proposes its first shape conservatively. Per-/257 universal
findings are restated against the introspect surface; six
introspect-specific findings follow; the proposed owner contract
lands in §3; recommended next slice in §4.*

## 0 · TL;DR

`persona-introspect` is the workspace's "debug the debugger." Per
`intent/persona.nota` 2026-05-21T10:00:00Z it is itself a persona
component and must be Tappable. Per `intent/component-shape.nota`
2026-05-19T20:00:00Z the universal observer-hook subscription lives
on the working socket. Per `reports/operator/150` §6.7 introspect
inspects peers through their contracts and daemon sockets and must
NOT require bespoke per-component observability verbs — Tap/Untap
is the universal mechanism. Per `intent/persona.nota`
2026-05-20T20:00:00Z spirit's Tap/Untap live-fanout is deferred
*until* introspect lands; introspect is the prerequisite consumer.

State summary:

- `signal-persona-introspect` is on the old shape: depends on
  `signal-core` (not `signal-frame`); uses universal-verb
  `Match Verb(Payload)` shape; ancestry-prefixed
  `Introspection*` types; carries
  `IntrospectDaemonConfiguration` (configuration belongs on the
  owner contract); `IntrospectionUnimplemented {scope, reason}`
  carries the redundant `scope` field; no observable block.
- `persona-introspect` daemon does not use `signal-executor` (same
  gap /258 flagged for engine-manager and /255 closed for spirit).
- `persona-introspect` daemon and CLI both reach for environment
  variables (`PERSONA_INTROSPECT_SOCKET`, `PERSONA_SOCKET_PATH`,
  `PERSONA_INTROSPECT_STORE`, `PERSONA_STATE_PATH`) in the
  production path, contrary to the single-argument rule and the
  CLI env-var carve-out (which is narrow: socket-path only, CLI
  only, test-only).
- `signal-persona-introspect` is described in
  `protocols/active-repositories.md` (line 28) as the **"central
  introspection envelope contract"** that "asks and wraps;
  component-specific observations stay in the owning component
  contracts." The contract has held that boundary so far — it
  carries envelope/correlation/projection records, not
  per-component schema duplications — but the boundary has frayed
  in two places: `IntrospectionTarget` mirrors
  `signal_persona::ComponentKind` (per /257 §"signal-persona-
  introspect"), and `DeliveryTraceStatus` mirrors
  `signal_persona_router::RouterDeliveryStatus` (per the contract's
  own comment at line 116).
- `owner-signal-persona-introspect` does not exist.

**Priority for the triad's migration slice**: (1) migrate
contract to `signal-frame` + contract-local verbs + observable
block; (2) drop `Introspection` ancestry prefix; (3) migrate
daemon onto `signal-executor`; (4) move
`IntrospectDaemonConfiguration` out of the working contract — it
lands as `BootstrapPolicy` content (NOTA file in repo per the
component triad's invariant 5) plus owner-contract `Configure`
target; (5) land the owner contract per §3.

**Open questions for the psyche** are listed inline at the end of
each section that has them and consolidated in §4. The three that
need direct psyche attention are restated in chat.

## 1 · /257 findings status

This section restates each /257 universal finding as it applies to
`signal-persona-introspect`. Most are not fixed.

### /257 §1.1 — Old universal-verb shape

**Status: NOT FIXED.** `signal-persona-introspect/src/lib.rs`
lines 178–196:

```rust
signal_channel! {
    channel Introspection {
        request IntrospectionRequest {
            Match EngineSnapshot(EngineSnapshotQuery),
            Match ComponentSnapshot(ComponentSnapshotQuery),
            Match DeliveryTrace(DeliveryTraceQuery),
            Match PrototypeWitness(PrototypeWitnessQuery),
        }
        ...
    }
}
```

Four `Match Verb(Payload)` operations — exactly the doubling
smell `intent/component-shape.nota` 2026-05-19T19:30:00Z retired.
The four read-side variants share the `*SnapshotQuery` /
`*TraceQuery` / `*WitnessQuery` repeated suffix — exactly the
missing-parent-enum smell `intent/component-shape.nota`
2026-05-20T00:07:55+02:00 calls out.

Proposed contract-local shape after §2's renames:

```rust
signal_channel! {
    channel Introspection {
        operation Query(Query),
    }
    reply Reply {
        Queried(QueryResult),
        Denied(DeniedDetail),
        Unimplemented(UnimplementedDetail),
    }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}

pub enum Query {
    EngineSnapshot(EngineSnapshotQuery),
    ComponentSnapshot(ComponentSnapshotQuery),
    DeliveryTrace(DeliveryTraceQuery),
    PrototypeWitness(PrototypeWitnessQuery),
}

pub enum QueryResult {
    EngineSnapshot(EngineSnapshot),
    ComponentSnapshot(ComponentSnapshot),
    DeliveryTrace(DeliveryTrace),
    PrototypeWitness(PrototypeWitness),
}
```

The four inner variants stay the natural shape of the read
plane; the parent `Query` enum is the typed sum lifting the
repeated `*Query` suffix.

### /257 §1.5 — Ancestry prefixes

**Status: NOT FIXED.** `signal-persona-introspect` is in the
`Introspection*`-prefix offender list (per /257 §1.5). The crate's
own crate name supplies "introspect" context; the prefix is the
crate's own namespace repeated:

- `IntrospectionTarget` → `Target` (but see §2.1 — this enum should
  retire and consume `ComponentKind` from signal-persona instead).
- `IntrospectionScope` → `Scope` (but see §2.2 — should retire with
  the `*Query` lifting).
- `IntrospectionRequest`, `IntrospectionReply` → macro-generated
  `Operation`, `Reply` (no prefix once the macro's prefix-drop
  bead lands; per `intent/component-shape.nota` 2026-05-21T10:30Z
  the macro emits the clean form).
- `IntrospectionUnimplemented` → `RequestUnimplemented`
  (consistent with spirit's `RequestUnimplemented`).
- `IntrospectionUnimplementedReason` → `UnimplementedReason`.
- `IntrospectionDenied` → `Denied` (or `Denial`).
- `IntrospectionDeniedReason` → `DeniedReason`.
- `IntrospectDaemonConfiguration` → moves out of this contract per
  §2.3; the field that survives as owner-contract
  `Configuration` does not carry the prefix.

### /257 §1.6 — `*RequestUnimplemented {scope, reason}` redundancy

**Status: NOT FIXED.** `signal-persona-introspect/src/lib.rs`
lines 149–153:

```rust
pub struct IntrospectionUnimplemented {
    pub scope: IntrospectionScope,
    pub reason: IntrospectionUnimplementedReason,
}
```

The `scope` field restates information the reply already carries
positionally (and which the caller still has from the request).
Spirit fixed the same smell in `d87e4055`. Drop `scope`; keep
`reason`. Once the operation root is `Query(Query)` per §1.1,
this becomes:

```rust
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

`IntrospectionDenied` carries the same `scope` smell at lines
164–168 — drop it for the same reason.

### /257 §1.10 — No observable block

**Status: NOT FIXED.** Confirmed by reading the contract — no
`observable` block on the `Introspection` channel.

Psyche's clarification at `intent/persona.nota` 2026-05-21T10:00Z
settles the previously-open question (was: should introspect
itself be observable?):

> *"of course! debug the debugger!"*

So introspect IS observable. Add:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

The macro injects `Tap(ObserverFilter)` and
`Untap(ObserverSubscriptionToken)` automatically per
`intent/component-shape.nota` 2026-05-20T02:00:00Z (universal
mandatory). Subscription lives on the working socket — observation
isn't security-sensitive.

The meta-introspection use case: when an agent is debugging
introspect's behavior (it's not seeing a peer's stream, or its
correlation joins look wrong), another introspect instance — or
the agent through the introspect CLI itself — can Tap on the
introspect daemon's working socket to watch the very component
that's watching everyone else.

### /257 §1.11 — Single-field timestamps

**Status: N/A.** `signal-persona-introspect` carries no
timestamp fields today (correlation is the `CorrelationId(String)`
opaque at line 42, not a time). The two-field timestamp rule
(`intent/workspace.nota` 2026-05-19 18:30) applies only to
intent records in spirit; nothing to do here.

### /257 §1.12 — Name collisions across contracts

**Status: PRESENT.** `IntrospectionTarget` (an 8-variant enum at
lines 15–27) overlaps with `signal_persona::ComponentKind`. Per
/257 §2 "signal-persona-introspect" the overlap is real:

```rust
// signal-persona-introspect:
pub enum IntrospectionTarget {
    EngineManager, Mind, Message, Router,
    System, Harness, Terminal, Introspect,
}

// signal-persona (engine-manager contract):
pub enum ComponentKind { ... }  // same eight kinds, minus EngineManager/Introspect
```

Designer recommendation: the canonical home for the enumeration
of persona components is signal-persona's `ComponentKind`.
Extend `ComponentKind` to include `EngineManager` and
`Introspect`, then `signal-persona-introspect` imports it:

```rust
use signal_persona::ComponentKind;
```

This deletes `IntrospectionTarget` from this contract entirely.
The audit framing in `protocols/active-repositories.md` (line 28
— *"component-specific observations stay in the owning component
contracts"*) supports this: the enumeration of components belongs
to the contract that knows about the engine (signal-persona), not
to introspect.

### /257 §3 — Bead coverage

Three building-block beads from /257 apply to this contract too:

- **`primary-77hh`** (drop channel-name prefix from
  signal_channel! emissions; auto-generate `OperationKind`). Once
  landed, this contract's macro-emitted types lose the
  `Introspection` prefix automatically and the
  `OperationKind` block (not currently in this contract but
  trending toward it) is derived structurally.
- **`primary-k3bu`** (rename `UnknownKindForVerb` in consumers).
  Applies to `persona-introspect/src/surface.rs:62` which
  hand-codes the kind dispatch through
  `nota_codec::Error::UnknownKindForVerb`.
- **`primary-u0lh`** (extend `nota-codec` derive coverage).
  Applies to `signal-persona-introspect`'s
  `IntrospectionRequest`/`IntrospectionReply` hand-impls (currently
  via the macro, but per `Input`/`Output` hand-impls in
  `persona-introspect/src/surface.rs` lines 48–98 there's a layer
  of hand-rolled NOTA dispatch that should derive once
  the codec supports the contract's mixed-enum shape).

## 2 · New findings specific to this triad

### 2.1 — Boundary creep: `IntrospectionTarget` duplicates `ComponentKind`

(Already in §1.12; restated here as the structurally-load-bearing
finding.) The contract's own header comment (lines 1–7) names the
discipline:

> *"This crate asks and wraps observations. Component-owned
> observation records live in the component contract that owns the
> observed state … This crate must not become a bucket for every
> component's internal rows."*

`IntrospectionTarget` is exactly the kind of duplication that
header forbids — the enumeration of persona components is a
signal-persona concern (the engine-manager knows which components
exist; that's its domain). Introspect should consume the answer,
not re-define it.

The same comment-clue applies to `DeliveryTraceStatus` at lines
117–133. The contract acknowledges in its own docstring that this
type "mirrors `signal_persona_router::RouterDeliveryStatus`." That
is exactly the boundary the header forbids. Designer
recommendation: drop `DeliveryTraceStatus` from this contract;
import `signal_persona_router::DeliveryStatus` directly in
`DeliveryTrace.status`. (Note the router-side will drop its
`Router` prefix per /257 §1.5 — the type becomes `DeliveryStatus`,
not `RouterDeliveryStatus`.)

After these two removals, the contract's per-component schema
duplications are gone. What stays:

- `EngineSnapshot`, `ComponentSnapshot`, `DeliveryTrace`,
  `PrototypeWitness` — these are *introspection-domain*
  composites (joins/rollups across peer observations) that don't
  exist as single peer records; introspect minted them.
- `CorrelationId` — introspect-domain correlation; not a wire
  exchange id, not a frame correlation, not a peer's
  identifier. Stays.
- `ComponentReadiness {Ready, NotReady}` — introspect-domain
  rollup. Stays.
- The four `*Query` payloads — selectors the *caller* sends to
  introspect; introspect-domain. Stay (and lift to typed sum per
  §1.1).

### 2.2 — Scope is not a logic plane

`IntrospectionScope` (lines 29–37) enumerates the four read
targets the contract has — `EngineSnapshot`, `ComponentSnapshot`,
`DeliveryTrace`, `PrototypeWitness`. It's only consulted from
`IntrospectionUnimplemented.scope` and `IntrospectionDenied.scope`
(both of which the §1.6 rule drops).

Once `scope` is dropped from those records, `IntrospectionScope`
has zero remaining consumers. Designer recommendation: retire it
when the lift to `operation Query(Query)` lands — the parent enum
`Query` already supplies the same discrimination, structurally.

### 2.3 — `IntrospectDaemonConfiguration` is in the wrong contract

`signal-persona-introspect/src/lib.rs` lines 198–239 hold a
nine-field configuration struct describing where the daemon binds
its sockets, where its store lives, and where each peer's socket
lives:

```rust
pub struct IntrospectDaemonConfiguration {
    pub introspect_socket_path: WirePath,
    pub introspect_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub store_path: WirePath,
    pub manager_socket_path: WirePath,
    pub router_socket_path: WirePath,
    pub terminal_socket_path: WirePath,
    pub owner_identity: OwnerIdentity,
}
```

Per `skills/component-triad.md` §5 (Policy state) and the
single-argument rule, daemon configuration enters via:

1. **`bootstrap-policy.nota`** in the runtime repo — the
   first-start seed that populates `policy_state` once.
2. **`owner-signal-persona-introspect` `Configure(Configuration)`**
   — owner-only mutations after first start.

Daemon argv carries the path to the bootstrap policy + the
socket-mode envelope (which the daemon binds, then forgets);
runtime knobs the configuration governs (peer socket paths,
storage location, observation retention) all live in policy_state.

Three of the current `IntrospectDaemonConfiguration` fields are
out-of-band sockets that the engine manager mints in the spawn
envelope and chmods — those stay in the spawn envelope (see
`signal-persona`'s `SpawnEnvelope` per /258 §2.6). They are not
introspect-policy.

The peer-socket-path fields (manager / router / terminal) are
genuinely policy: "which peers does introspect observe today?"
Those belong in the bootstrap policy (initial seed) and
owner-contract `Configure`-able (so engine-manager can update the
peer set as new components come online).

The store_path field is bootstrap-only — the daemon's redb
location is set at first start; live re-pointing is not a
supported operation.

Designer recommendation: remove `IntrospectDaemonConfiguration`
from `signal-persona-introspect` entirely. Move the policy fields
to the owner contract per §3; move the socket envelope fields to
`SpawnEnvelope` if not already there; document the bootstrap seed
shape in `persona-introspect/bootstrap-policy.nota`.

### 2.4 — Daemon does not use `signal-executor`

`persona-introspect/Cargo.toml` does not depend on
`signal-executor`. No `Lowering` impl, no `CommandExecutor` impl,
no `Executor::execute` calls.

Today the daemon dispatches directly through the Kameo actor
mesh: `IntrospectionConnection::read_signal_request` →
`IntrospectionRoot::handle_request` → per-variant match. This is
the same gap /258 flagged for engine-manager and /255 closed for
spirit.

The structural migration mirrors spirit's, with one twist
specific to introspect: most operations are **cross-peer queries**
that fan out over Signal to peer daemons. The lowering shape
needs to express:

- `IntrospectCommand::ProbeRouterSummary(EngineId)` — projects to
  `SemaOperation::Match` (cross-component subscribe vs. one-shot
  is the daemon's policy decision, not the caller's).
- `IntrospectCommand::ProbeManagerSnapshot(EngineId)` — same.
- `IntrospectCommand::ProbeTerminalSnapshot(EngineId)` — same.
- `IntrospectCommand::ComposeRollup(EngineId)` — projects to
  `SemaOperation::Match` (reading own store).
- `IntrospectCommand::RecordObservation(StoredObservation)` —
  projects to `SemaOperation::Assert` (writing own store; this is
  the audit trail already in `IntrospectionStore`).

The `CommandExecutor` impl wraps the actor mesh: lowering decodes
the typed `Query` into a sequence of `IntrospectCommand` records;
the executor's `execute_atomic_batch` calls into the Kameo root
with `HandleIntrospectionRequest`-shaped messages; the effects
projecting back to `SemaOutcome::Matched` / `Asserted` are the
typed `IntrospectEffect` records the lowering then composes into
the contract reply.

The "atomic" framing is mostly degenerate here — most introspect
operations are reads with one inner command. The
`BatchErrorClassification` impl is also straightforward: a
peer-socket connection failure is `Retryable + NotCommitted`; a
store-write failure is `Unknown + Unknown` until the engine
exposes more.

### 2.5 — Environment variables in the daemon's production path

`persona-introspect/src/daemon.rs` lines 39–43 and `store.rs`
lines 36–43 both read environment variables in paths the daemon
uses at runtime:

```rust
// daemon.rs
pub fn from_environment() -> Option<Self> {
    std::env::var_os("PERSONA_INTROSPECT_SOCKET")
        .or_else(|| std::env::var_os("PERSONA_SOCKET_PATH"))
        .map(Self::from_path)
}

// store.rs
pub fn from_environment() -> Self {
    match std::env::var_os("PERSONA_INTROSPECT_STORE") { ... }
}
```

The comment in `daemon.rs` line 34–38 says "CLI convenience …
Not for the daemon's production launch path" — and yet `store.rs`
line 30–34 says the same thing. The presence of these helpers
shows discipline at the comment layer; the structural problem is
that the helpers exist at all in code the daemon links against.

Per `intent/component-shape.nota` 2026-05-20T13:00:00Z:

> *"the CLI is the only place where we allow the use of an
> environment variable to make it easy for testing to give it a
> non-canonical socket path for the daemon … Daemons never read
> environment variables; all daemon configuration is NOTA."*

Designer recommendation: when the contract migration lands and
`signal-frame::signal_cli!` is wired in,
`IntrospectionSocket::from_environment()` retires entirely; the
CLI uses the macro's env-var carve-out (socket-path override
only) and the daemon never has the codepath available.
`StoreLocation::from_environment()` retires for the same reason —
the daemon's store path comes from the bootstrap policy / owner
`Configure`; the CLI never reads the store directly (the CLI is a
NOTA↔Signal bridge per `intent/component-shape.nota`
2026-05-20T13:00:00Z, and reading the store is the daemon's job).

### 2.6 — Per-peer hand-rolled clients vs. universal Tap consumer

Today `persona-introspect/src/runtime.rs` has separate
`ManagerClient`, `RouterClient`, `TerminalClient` Kameo actors,
each hand-rolling a `query_summary_over_socket` flow for that
peer's particular observation contract. `RouterClient` is
currently the only one wired (lines 350–369): it opens a unix
stream, writes a `RouterFrame` carrying `RouterRequest::Summary`,
reads a `RouterFrame` reply, decodes a typed `RouterSummary`, and
composes one bit of `PrototypeWitness.router_seen`.

This is exactly the *bespoke per-component observability verbs*
shape `reports/operator/150` §6.7 says introspect must NOT
require:

> *"introspect should use the standard observable surface exposed
> by each persona component. It should NOT require bespoke
> per-component observability verbs. Tap/Untap is infrastructure,
> not domain operations."*

And per `intent/persona.nota` 2026-05-20T20:00:00Z:

> *"Tap/Untap live subscriber fanout in persona-spirit is deferred
> until persona-introspect comes online. … Persona-introspect is
> the prerequisite consumer."*

Together these say: the long-term shape is **one
`PeerObserverClient` actor per peer connection that uses the
peer's universal `Tap(ObserverFilter)` operation**. The current
`RouterClient::query_summary_over_socket` path is a transitional
prototype-witness affordance — it works today, but it should
retire as soon as the universal-Tap consumer lands; the actor
itself stays (one client per peer relationship is the right shape,
per `persona-introspect/skills.md`), but the inner machinery
unifies across peers.

The structural change: instead of three different "ask the peer
about its summary" hand-rolls, one `PeerObserverClient` actor opens
one `Tap` subscription against each peer's working socket and
consumes its `OperationReceived` / `EffectEmitted` stream as
typed events. Cross-peer composition (PrototypeWitness rollup,
DeliveryTrace correlation) happens in the daemon's `Lowering`
impl from the stored observations.

This shape also explains why a one-shot prototype-witness query
("is the router up right now?") needs to do something different
from the Tap stream: the one-shot is a `Match` against the
introspect daemon's *own* observation store ("did we receive a
recent enough router OperationReceived/EffectEmitted?"). The
peer-socket connection itself is only opened once per relationship
— the Tap stream — not per query. The Match runs against
introspect.redb, not over the wire to the peer.

Designer recommendation: do not collapse the per-peer client
actors into one universal one (the per-peer-connection shape is
right; per `skills/subscription-lifecycle.md` and
`persona-introspect/skills.md` the one-client-per-peer-relationship
discipline is load-bearing). Do collapse the *inner protocol* —
all per-peer clients speak the same universal Tap surface, only
the peer socket path and the typed `<Component>ObserverFilter`
differ.

This is gated on Tap/Untap *fanout* landing in peer daemons.
Spirit has Tap/Untap accepted on the wire today (per
`intent/persona.nota` 2026-05-20T20:00:00Z) but returns
`RequestUnimplemented` / `SemaOutcome::NoChange` until introspect
arrives. The order is:

1. Land the introspect triad migration (contract on signal-frame,
   daemon on signal-executor, owner contract per §3).
2. Land the `PeerObserverClient` shape consuming peer
   `<Component>ObserverStream` events.
3. Replace each peer's placeholder Tap response with real
   `FrameObserverBridge` fanout per the deferred spirit work.

### 2.7 — `SocketMode` duplicate definition

`persona-introspect/src/daemon.rs` lines 54–65 defines a local
`SocketMode(u32)`:

```rust
pub struct SocketMode(u32);
impl SocketMode {
    pub const fn from_octal(value: u32) -> Self { ... }
    pub const fn as_octal(self) -> u32 { ... }
}
```

This is a duplicate of `signal_persona::SocketMode` (which the
contract already imports at line 12). Designer recommendation:
delete the local one; use the canonical type. Small cleanup; flag
because it is exactly the boundary the `signal-persona-introspect`
header forbids.

## 3 · Proposed owner signal — `owner-signal-persona-introspect`

The owner contract is missing. Per
`intent/component-shape.nota` 2026-05-20T12:11:26Z and
`skills/component-triad.md` invariant 4, every stateful component
has both contracts; introspect's daemon owns durable state
(`introspect.redb`), so it qualifies.

### 3.1 — Operations the owner socket carries

Conservative first cut, in the spirit of `intent/workspace.nota`
2026-05-20T14:40:00Z (intent logging is conservative by default —
the same applies to first-cut owner-contract proposals: pick the
operations the cognitive caller actually needs today; let new
operations surface from real usage).

Two operations are clearly load-bearing:

**`Configure(Configuration)`** — owner sets/updates introspect's
durable policy. The policy expresses: (a) which peer sockets are
in scope, (b) the introspect store's retention policy for the
observation audit trail, (c) the observer-filter defaults the
daemon applies to its outbound Tap subscriptions against peers.

**`Inspect(Inspection)`** — owner reads introspect's current
policy state. The single policy-section selector is enough; the
shape mirrors `owner-signal-persona-mind`'s
`Inspect(Inspection)` per
`/git/github.com/LiGoldragon/owner-signal-persona-mind/src/lib.rs`
lines 81–86.

One operation is open:

**Lifecycle verbs (`Start` / `Drain` / `Reload` / etc.)** — these
appear on spirit's owner contract
(`/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs`
lines 104–120). Per `intent/component-shape.nota`
2026-05-20T13:45:00Z (psyche, certainty `Minimum`) it is open
whether lifecycle belongs on owner-signal or out-of-band through
the engine-manager spawn envelope. Designer lean: do not include
lifecycle verbs in the owner contract's first cut; introspect's
lifecycle is naturally engine-manager-driven (introspect is
spawned-and-supervised, not self-managed). If the question
re-opens with a Decision, add them later.

The substantive deferral question is whether introspect's owner
contract should also carry **peer subscription policy**:
`AuthorizePeerObservation { peer: ComponentKind, filter: ... }`
/ `RetractPeerObservation`. Designer lean: these are *Configure*
content (Configuration carries the peer-set), not separate
verbs. New peers come online by the owner re-Configuring; the
daemon diffs the new peer-set against its current Tap
subscriptions and opens/closes as needed. This collapses what
might have been a separate verb family into the standard policy
flow.

### 3.2 — Proposed signal tree

Sketch shape (Rust syntax, not implementation):

```rust
//! Owner-signal contract for privileged `persona-introspect` policy.
//!
//! Ordinary introspection traffic lives in `signal-persona-introspect`.
//! This crate carries owner-only policy and configuration operations.

use nota_codec::{NotaEnum, NotaRecord, NotaTransparent};
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};
use signal_frame::signal_channel;
use signal_persona::{ComponentKind, SocketMode, WirePath};
use signal_persona_auth::OwnerIdentity;

// ──────────────────────────── Policy ──────────────────────────────

pub struct PolicyRevision(u64);   // NotaTransparent

// What introspect treats as in-scope peers and how it observes them.
pub struct Configuration {
    pub peer_observations: Vec<PeerObservation>,
    pub retention: Retention,
    pub default_observer_filter: ObserverFilterPolicy,
}

pub struct PeerObservation {
    pub peer: ComponentKind,
    pub socket_path: WirePath,
}

pub enum Retention {
    KeepAllForever,
    BoundedBySequence(SequenceWindow),
    BoundedByByteSize(ByteSizeBudget),
}

pub struct SequenceWindow(u64);   // NotaTransparent
pub struct ByteSizeBudget(u64);   // NotaTransparent

pub enum ObserverFilterPolicy {
    AllOperationsAndEffects,
    OnlyEffects,
    EffectsForClass(SemaOperationClassSelection),
}

pub enum SemaOperationClassSelection {
    OnlyAssertsAndMutates,
    OnlyRetracts,
    OnlyMatches,
    OnlySubscribes,
    OnlyValidates,
    All,
}

// ──────────────────────────── Inspection ──────────────────────────

pub enum PolicySection {
    PeerObservations,
    Retention,
    DefaultObserverFilter,
    All,
}

pub struct Inspection {
    pub section: PolicySection,
}

// ──────────────────────────── Replies ─────────────────────────────

pub struct Configured {
    pub revision: PolicyRevision,
}

pub struct PolicySnapshot {
    pub revision: PolicyRevision,
    pub configuration: Configuration,
}

pub struct ConfigurationRejected {
    pub reason: ConfigurationRejectionReason,
}

pub enum ConfigurationRejectionReason {
    PeerSocketUnreachable,        // engine manager hasn't bound it yet
    PeerNotTappable,              // peer's contract has no observable block
    RetentionViolatesStoreLimit,  // store can't fit the requested window
}

pub enum UnimplementedReason {
    NotBuiltYet,
    DependencyNotReady,
}

pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}

// ──────────────────────────── Channel ─────────────────────────────

signal_channel! {
    channel OwnerIntrospect {
        operation Configure(Configuration),
        operation Inspect(Inspection),
    }
    reply Reply {
        Configured(Configured),
        PolicySnapshot(PolicySnapshot),
        ConfigurationRejected(ConfigurationRejected),
        RequestUnimplemented(RequestUnimplemented),
    }
}
```

The shape mirrors `owner-signal-persona-mind`'s
`Configure`/`Inspect` exactly, parameterized to introspect's
domain. No lifecycle verbs (per §3.1's lean); no observable block
(per `intent/component-shape.nota` 2026-05-19T20:00:00Z observation
rides the working socket).

Two notes on the proposed shape:

- **`Configuration` carries `peer_observations` as a Vec**, not a
  flat set of named fields like the current
  `IntrospectDaemonConfiguration`. This lets the peer set grow as
  new components come online without contract churn (the
  Vec-with-typed-peer-tag shape is the data-not-schema move). The
  per-peer `ComponentKind` discriminator + `WirePath` is the
  cognitive content; the daemon translates each entry into a
  `PeerObserverClient` actor.
- **`Retention` is open-ended** today. The
  `BoundedBySequence`/`BoundedByByteSize` variants are both
  proposed because two real retention shapes exist in the
  workspace already (spirit's intent records keep all forever;
  the router's delivery trace bounds by sequence). If the psyche
  has a view on the right default, this is the place. Designer
  lean: `KeepAllForever` is the right *default* for the prototype;
  the bounded options exist for when the audit trail grows large.
  This is one of three psyche-touch questions in §4.

### 3.3 — Bootstrap policy

`persona-introspect/bootstrap-policy.nota` (which does not exist
today) should hold the first-start seed:

```text
(Configuration
  (peer_observations
    [(PeerObservation
        EngineManager
        "/run/persona/engine-manager.sock")
     (PeerObservation
        Router
        "/run/persona/router.sock")
     (PeerObservation
        Terminal
        "/run/persona/terminal.sock")
     (PeerObservation
        Mind
        "/run/persona/mind.sock")
     (PeerObservation
        Harness
        "/run/persona/harness.sock")
     (PeerObservation
        Message
        "/run/persona/message.sock")
     (PeerObservation
        System
        "/run/persona/system.sock")])
  KeepAllForever
  AllOperationsAndEffects)
```

Per `skills/component-triad.md` invariant 5 this file is read
exactly once on first start; thereafter the owner contract's
`Configure` is the only path. Re-bootstrapping is by blowing away
the redb. (Note: NOTA records are positional — the snippet above
follows `skills/skills.nota`'s positional record convention; the
real bootstrap-policy.nota would be authored against the
schema's positional order from the contract types.)

### 3.4 — Filed uncertainties

- **Whether to include lifecycle verbs in v1.** Lean: no. (Per
  `intent/component-shape.nota` 2026-05-20T13:45:00Z the
  whole-class question is open with `Minimum` certainty;
  introspect's lifecycle is engine-manager-driven and doesn't
  visibly need its own verbs. Reopen if a real need surfaces.)
- **Retention default.** Lean: `KeepAllForever` for the
  prototype. Psyche-touch in §4.
- **Whether the cognitive caller is engine-manager or
  spirit.** Spirit owns mind in the authority graph per
  `intent/persona.nota` 2026-05-19T15:30:00Z; whether spirit also
  owns introspect, or whether introspect is engine-manager-managed
  like terminal/harness/router, is unspecified. Designer lean:
  engine-manager. (Introspect is observation infrastructure
  parallel to terminal/router; mind doesn't need to think about
  it. Spirit doesn't either; the engine-manager binds, supervises,
  and configures.) Psyche-touch in §4.

## 4 · Recommended next slice

In priority order, mirroring /258's structure:

1. **Move `IntrospectDaemonConfiguration` out of
   `signal-persona-introspect`.** Once decided which fields are
   bootstrap-policy vs spawn-envelope vs owner-Configure, the
   working contract loses the configuration block entirely. This
   is a prerequisite for step 5 because it changes what the
   working contract declares.
2. **Migrate `signal-persona-introspect` to `signal-frame` +
   contract-local verbs + observable block.** The contract-local
   shape is one `operation Query(Query)` root plus the
   macro-injected `Tap`/`Untap`; the reply tree lifts to
   `Reply::Queried(QueryResult)`. Drop ancestry prefixes
   (`Introspection*`); drop the redundant `scope` field; consume
   `signal_persona::ComponentKind` and
   `signal_persona_router::DeliveryStatus` for the duplicate
   enums.
3. **Drop `IntrospectionTarget` and `DeliveryTraceStatus` from
   this contract.** Per §2.1, both are boundary creep.
4. **Land `owner-signal-persona-introspect`** per §3. Conservative
   first cut: `Configure(Configuration)` + `Inspect(Inspection)`.
   No lifecycle verbs in v1.
5. **Migrate `persona-introspect` daemon onto `signal-executor`**
   per §2.4. Define `IntrospectCommand` / `IntrospectEffect`;
   implement `Lowering` / `CommandExecutor` /
   `BatchErrorClassification`. This mirrors spirit's migration
   shape, with the cross-peer fan-out lowered into per-peer
   `IntrospectCommand::ProbePeer*` records the executor
   dispatches through the actor mesh.
6. **Replace `IntrospectionSocket::from_environment` and
   `StoreLocation::from_environment` with the `signal_cli!` macro
   path.** Environment-variable reads retire entirely from the
   daemon and survive only in the CLI's macro-managed socket-path
   override carve-out.
7. **Land `PeerObserverClient` (universal Tap consumer)** per
   §2.6. Replace the per-peer hand-rolled
   `query_summary_over_socket` flows with one universal Tap
   subscription per peer relationship. This unblocks the deferred
   spirit Tap/Untap fanout work (and every other persona
   component's deferred fanout work) — introspect is the
   prerequisite consumer for all of it.
8. **Delete `persona-introspect/src/daemon.rs`'s local
   `SocketMode`** per §2.7. One-line cleanup; included for
   completeness.

### Three psyche-touch questions for the chat

These three carry enough weight that the designer lean alone
shouldn't settle them.

**Q1. Should `owner-signal-persona-introspect` carry lifecycle
verbs (`Start` / `Drain` / `Reload`) in v1?** Designer lean: no
— introspect is engine-manager-supervised; lifecycle enters
out-of-band through the spawn envelope, not the owner contract.
Spirit's owner contract carries them
(`/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs`
lines 104–110); spirit's reasons may not generalize. Per
`intent/component-shape.nota` 2026-05-20T13:45:00Z the
whole-class question is open with `Minimum` certainty; the
introspect-specific answer is what's being asked.

**Q2. What's the right default for introspect's observation-store
retention?** Designer lean: `KeepAllForever` for the prototype.
Two alternatives sketched in §3.2:
`BoundedBySequence(SequenceWindow)` and
`BoundedByByteSize(ByteSizeBudget)`. The shape of the audit trail
the workspace wants from introspect (do you want to time-travel
back over weeks of observations? bounded last-N? fixed-byte
window?) is a psyche-flavored decision more than an architectural
one.

**Q3. Is the cognitive owner of introspect the engine-manager, or
spirit?** Designer lean: engine-manager. Introspect is
observation infrastructure parallel to terminal/router/harness —
the engine-manager binds, supervises, and configures it; mind
doesn't need to think about it; spirit doesn't either. But the
authority graph in `intent/persona.nota` 2026-05-19T15:30:00Z is
explicit only about supervisor → spirit → mind → orchestrate →
router/harness/terminal; introspect isn't named. The answer
shapes who calls `owner-signal-persona-introspect`'s `Configure`.

## 5 · References

### Authority sources

- `~/primary/ESSENCE.md` §Naming — full-English-words +
  no-ancestry-restating pair.
- `~/primary/AGENTS.md` — single-argument rule, component-triad
  shape, NOTA-as-the-only-argument-language.
- `~/primary/INTENT.md` — synthesised workspace intent prose.
- `~/primary/skills/component-triad.md` — five invariants and
  single-argument rule.
- `~/primary/skills/naming.md` — full discipline + offender
  table.
- `~/primary/skills/reporting.md` — chat-vs-report discipline.

### Intent records cited

- `intent/persona.nota` 2026-05-19T20:00:00Z (universal
  observer-hook subscription is on the working socket).
- `intent/persona.nota` 2026-05-19T15:30:00Z (canonical authority
  chain: supervisor → spirit → mind → orchestrate →
  router/harness/terminal).
- `intent/persona.nota` 2026-05-20T20:00:00Z (Tap/Untap live
  fanout deferred until introspect lands; introspect is the
  prerequisite consumer).
- `intent/persona.nota` 2026-05-21T10:00:00Z (debug the
  debugger — introspect is itself observable).
- `intent/component-shape.nota` 2026-05-19T20:00:00Z (universal
  observer-hook on working socket).
- `intent/component-shape.nota` 2026-05-20T02:00:00Z (Tap/Untap
  mandatory for persona components; three-layer model).
- `intent/component-shape.nota` 2026-05-20T12:11:26Z (working /
  policy vocabulary; every stateful component has an owner
  contract).
- `intent/component-shape.nota` 2026-05-20T13:00:00Z (CLI design
  records, env-var carve-out, NOTA-only argument language for
  daemons).
- `intent/component-shape.nota` 2026-05-20T13:45:00Z (open
  whether owner contracts carry lifecycle verbs).
- `intent/component-shape.nota` 2026-05-20T15:00:00Z (canonical
  OperationReceived/EffectEmitted event-pair naming).
- `intent/component-shape.nota` 2026-05-21T10:30:00Z (macro
  emits clean unprefixed names; modules disambiguate
  multi-channel crates).
- `intent/workspace.nota` 2026-05-20T14:40:00Z (intent logging is
  conservative by default; the same default applies to
  designer-proposed shapes).
- `intent/naming.nota` 2026-05-19T18:50:00Z (signal types are
  architecture; repeated category words = missing parent enum).

### Reference reports

- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  §6.7 — introspect uses peers' standard observable surface; no
  bespoke per-component observability verbs; may own a local
  database but primarily inspects peers through contracts.
- `reports/designer/258-persona-signal-triad-audit-2026-05-21.md`
  — engine-manager triad audit; same migration template applies
  here.
- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  — workspace-wide audit; this triad's findings fold into §1.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — eight principles consolidated; this report applies them.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — the `signal_cli!` macro path that retires
  `IntrospectionSocket::from_environment`.

### Code under audit

- `/git/github.com/LiGoldragon/signal-persona-introspect/src/lib.rs`
  — 240 lines; the working contract.
- `/git/github.com/LiGoldragon/persona-introspect/src/lib.rs` +
  `daemon.rs` + `runtime.rs` + `store.rs` + `surface.rs` +
  `command.rs` — 1780 lines; the daemon + thin CLI.
- `/git/github.com/LiGoldragon/persona-introspect/ARCHITECTURE.md`
  — current architecture; carries the universal observer-hook
  direction in the constraints table.

### Triad templates

- `/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs`
  — owner-contract template with lifecycle verbs.
- `/git/github.com/LiGoldragon/owner-signal-persona-mind/src/lib.rs`
  — owner-contract template with Configure/Inspect only (closer
  fit for introspect's first cut).

This report retires when (a) `signal-persona-introspect` lands on
`signal-frame` + contract-local verbs + observable block AND
`owner-signal-persona-introspect` lands per §3 AND the daemon is
migrated onto `signal-executor` AND the universal Tap consumer
shape lands, OR (b) a successor audit supersedes.
