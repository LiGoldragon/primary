# signal-lojix — architecture

*Ordinary Signal wire contract for the lojix deploy orchestrator.*

> **Status (2026-06-05):** schema-derived. The canonical surface is
> `schema/lib.schema`; the Rust crate is emitted from it by
> `schema-rust-next`. `signal-lojix` is the **ordinary** leg of the
> lojix contract pair — the peer-callable read / observe / subscribe
> surface. Owner-only mutations live in the **meta** leg,
> `meta-signal-lojix` (born `meta-signal-`, never `owner-signal-`).
> See `~/primary/protocols/active-repositories.md` §"Replacement
> Stack".

## 0 · TL;DR

`signal-lojix` is the public read/observe/subscribe wire vocabulary
for cluster deploy orchestration. It defines the typed
request/reply/event records a peer client (the thin `lojix` CLI
binary, future operator clients) exchanges with the long-lived
`lojix-daemon` over a Unix socket.

This crate is a **pure wire contract**: it is emitted from
`schema/lib.schema` and carries exactly the rkyv (binary wire) codec,
the NOTA (text wire) codec, and the `signal-frame` mail envelope. It
owns the records, the operation-root enums, the validation newtypes,
and the typed rejection reasons. It owns **no** daemon behaviour, **no**
engine traits, **no** Nexus/SEMA plane content, **no** CLI binary, and
**no** deploy pipeline — those live in the `lojix` daemon crate and
its per-plane runtime schemas.

This contract is the **shared-type owner** of the pair. The record
types both legs need — `DeploymentIdentifier`, `GenerationIdentifier`,
the `Generation` / `GenerationListing` records, the two phase-event
payloads, and the typed rejection reasons — are defined **once, here**.
`meta-signal-lojix` cross-imports them via the single-colon path form
`signal-lojix:lib:TypeName`.

> **Scope (today vs eventually).** This contract sits on today's
> stack — `signal-frame` mail envelope, rkyv archives, `sema-engine`
> typed database engine in the consumer daemon. The
> eventually-self-hosting stack is Sema-on-Sema; this contract is a
> realization step. See `~/primary/ESSENCE.md` §"Today and
> eventually".

## 1 · The two-contract split

The lojix contract is a **pair**, split by authority, not by topic:

| Leg | Repo | Operation roots | Caller |
|---|---|---|---|
| Ordinary | `signal-lojix` (this crate) | `Query`, `WatchDeployments`, `WatchCacheRetention`, `Unwatch` | any peer — read / observe / subscribe |
| Meta policy | `meta-signal-lojix` | `Deploy`, `Pin`, `Unpin`, `Retire` | owner only — mutations |

The split is the standard component-triad ordinary/meta boundary
(`~/primary/skills/component-triad.md`): observation and subscription
are peer-callable and ride the ordinary contract; the mutations that
change the live set — submitting a deploy, pinning, unpinning, and
retiring a generation — are owner-gated and ride the meta contract.

`meta-signal-lojix` is **born meta-signal-**; there is no
`owner-signal-lojix` intermediate. It is carried as a **path-dependency
package now**, and lands as its own repository at cutover.

## 2 · Channel boundary

| Side | Component |
|---|---|
| Request producer | `lojix` CLI binary, future peer clients |
| Request consumer | `lojix-daemon` |
| Reply / event producer | `lojix-daemon` |
| Reply / event consumer | the caller that submitted the operation; subscribers |

Transport: Unix socket at `/run/lojix/daemon.sock` carrying
`signal-frame` mail envelopes around rkyv-encoded records. The
transport itself belongs to the `lojix` repo, not this contract.

## 3 · Operation roots — ordinary surface

A `.schema` root is exactly `{ imports } [Input] [Output] { namespace }`:
three operation surfaces. Operation roots are **contract-local verbs**;
every root enum carries at least two meaningful variants.

### Input (request operations)

| Operation | Payload | Purpose |
|---|---|---|
| `Query` | `Selection` | Read the live set — by node, by generation, or by event-log range. |
| `WatchDeployments` | `DeploymentWatch` | Subscribe to deployment phase events for one deploy, one node, or all. |
| `WatchCacheRetention` | `CacheRetentionWatch` | Subscribe to cache-retention transitions as the daemon rewrites GC roots. |
| `Unwatch` | `SubscriptionClose` | End an open subscription by its `SubscriptionToken`. |

### Output (reply variants)

Verb-past-tense outcomes plus typed rejection payloads:
`Queried(GenerationListing)`, `Watching(SubscriptionOpened)`,
`Unwatched(SubscriptionClosed)`, and the typed
`QueryRejected(RejectedQuery)`, `WatchRejected(RejectedWatch)`,
`UnwatchRejected(RejectedUnwatch)`. No untyped error strings cross the
wire — every rejection is a closed-enum reason carried in a typed
payload.

## 4 · Streaming — day one

`signal-lojix` carries the **two Watch streaming subscriptions from the
start** — streaming is not deferred. The daemon is push-not-poll: a
subscriber registers and the daemon pushes phase events and
cache-retention transitions as they occur.

The vocabulary is fixed here, today:

- `DeploymentPhaseEvent` — typed phases `Submitted`, `Building`,
  `Built`, `Copying`, `Activating`, `Activated`, `Failed`, carried with
  the deploying identifiers, the `EventLogPosition`, and an optional
  detail string. Opened by `WatchDeployments`, conceptually a
  `DeploymentEventStream`.
- `CacheRetentionTransitionEvent` — `Pinned` / `Unpinned` / `Promoted`
  / `Demoted` / `Retired` / `Evicted` live-set transitions across the
  GC-root slots (`Current`, `BootPending`, `Rollback`, `Pinned`,
  `Recent`), carried with the from/to slot and optional pin label.
  Opened by `WatchCacheRetention`, conceptually a
  `CacheRetentionEventStream`.

`Unwatch` closes a stream by token.

### Streaming-syntax status — emittable handshake today, event root tomorrow

The streaming-emission probe (recorded in `0-frame-and-method.md` of
this session, and at the head of `schema/lib.schema`) is decisive: the
`schema-next` + `schema-rust-next` stack the cloud triad actually ships
has **no fourth event/stream root** and **no `opens`/`belongs` relation
construct**. The only schema-next precedent for subscriptions models
Watch/Unwatch as **ordinary `Input` variants returning ordinary
`Output` subscription-receipt replies**. The
`(Event (belongs Stream) …)` block is the OLD `signal_channel!` /
concept-schema grammar, which schema-next does not parse.

So the streaming surface is authored today in the **emittable
schema-next form** (Option A):

1. The Watch/Unwatch **subscription handshake** is an ordinary request
   → `SubscriptionToken` reply (`Watching(SubscriptionOpened)`,
   `Unwatched(SubscriptionClosed)`). This is fully schema-derived and
   emittable now.
2. The two daemon-pushed event payloads (`DeploymentPhaseEvent`,
   `CacheRetentionTransitionEvent`) are defined **once** as plain
   namespace records, so no domain vocabulary is lost and
   `meta-signal-lojix` can cross-import them.

What `schema-next` + `schema-rust-next` must **grow** for the
event-frame push itself to be schema-derived (the piece not emittable
today, and on the lojix path — not a reason to drop streaming):

- **schema-next grammar:** a fourth optional positional root after
  `Output` — an event/stream root enum — plus a per-variant relation
  annotation pairing each event variant to a named stream
  (`belongs <Stream>`) and each subscription-shaped `Input` variant to
  the stream it opens (`opens <Stream>`). This lifts the old
  `signal_channel!` event/stream grammar into the `SchemaSource` data
  model as a `StreamRelation` declaration kind.
- **schema-rust-next emitter:** a `RustEmissionTarget::WireContract`
  path that, when the event root is present, emits the event enum, a
  `StreamingFrame` / `StreamingFrameBody` event frame, the
  stream-relation witnesses, and the event's NOTA + `signal-frame`
  encode/decode (the `emit_mail_event_support` machinery currently
  gated off for `WireContract`).

The provisional post-grammar shape — a fourth positional root after
`Output` pairing `DeploymentPhaseEvent`/`CacheRetentionTransitionEvent`
to their streams, with `WatchDeployments`/`WatchCacheRetention`
annotated `opens …` — is recorded at the head of `schema/lib.schema`
so the grammar work has a target. **lojix is the first component to
prove schema-derived stream emission;** the enhancement rides this
path. Until that root exists, the records carry the vocabulary and the
handshake carries the subscription surface — streaming is present from
day one either way.

## 5 · Domain vocabulary (salvaged, still true)

The records below are the still-true deploy domain, carried forward
from the prototype
(`lojix/schema-deep-iteration-2/schema/lojix.schema:15-91`) and the
legacy deploy surface (`lojix-cli/src/request.rs`,
`lojix-cli/src/build.rs`):

- **`DeploymentIdentifier`, `GenerationIdentifier`** — minted by the
  daemon; integer newtypes.
- **`Generation` / `GenerationListing`** — a live-set entry
  (identifiers, cluster/node, `DeploymentKind`, `ActivationKind`,
  `GenerationSlot`, closure path) and the queried collection, carried
  with a `DatabaseMarker` (`CommitSequence` + `StateDigest`) for
  snapshot identity.
- **`DeploymentKind`** — `FullOs` / `OsOnly` / `HomeOnly`, the three
  legacy deploy shapes (`lojix-cli/src/request.rs:13-53`).
- **`ActivationKind`** — `Switch` / `Boot` / `Test` / `BootOnce`,
  carried forward from `SystemAction`
  (`lojix-cli/src/build.rs:9-23`; `Eval` and `Build` are
  build-only and do not activate, so they are not activation kinds).
- **`GenerationSlot`** — `Current` / `BootPending` / `Rollback` /
  `Pinned` / `Recent`, the GC-root slot tree the daemon owns
  (`lojix/ARCHITECTURE.md:44-56`).
- **Phase events** — `DeploymentPhase` and `CacheRetentionTransition`
  with their event payloads (§4).
- **Typed rejection reasons** — closed enums
  (`QueryRejectionReason`, `WatchRejectionReason`,
  `UnwatchRejectionReason`) carried in typed `Rejected*` payloads.

## 6 · Boundary rules

- **Pure wire contract.** No behaviour. No storage. No actors. No I/O.
  The crate is emitted from `schema/lib.schema` and is exactly the
  rkyv + NOTA codec plus the `signal-frame` mail envelope. The boundary
  test: every type here is reachable from at least one socket handler
  in the consumer daemon.
- **No engine traits, no plane content.** Nexus/SEMA decision and
  effect language lives in the daemon's per-plane runtime schemas
  (`lojix/schema/{nexus,sema}.schema`, a later port phase), never in
  this contract.
- **No `Unknown` variant on any closed enum.** New domain shapes are
  coordinated schema bumps in this crate, not runtime escape hatches.
- **Typed errors, not strings.** Daemon-side rejections decode through
  typed `Rejected*` payloads keyed on a closed reason enum — no untyped
  error strings on the wire.
- **Shared types defined once.** The shared record types are owned
  here; `meta-signal-lojix` cross-imports via
  `signal-lojix:lib:TypeName` and never re-declares them.
- **Full English names; no crate-name prefix on types.** Per
  `~/primary/ESSENCE.md` §"Naming" and `~/primary/skills/naming.md` —
  `DeploymentIdentifier` not `DeploymentId`, `Generation` (inside the
  contract) not `LojixGeneration`.
- **Daemon-internal messages stay private.** Actor messages and command
  enums stay inside the `lojix` crate and are not exported here.

## 7 · Migration history — three-layer model superseded (2026-06-05)

This contract previously specified a **three-layer migration**: Layer 1
contract operations declared via a `signal_channel!` macro with
`request`/`reply`/`event`/`stream` blocks and `signal-frame` framing,
Layer 2 daemon Component Commands, and Layer 3 payloadless
`SemaOperation` classification via a `ToSemaOperation` projection. That
whole model is **superseded** by the schema-derived per-plane triad
with the two-contract ordinary/meta split (Spirit `29w2hwko8d7mr2jh943`).

Under the new model the contract is **emitted from a `.schema` file**
rather than hand-declared via `signal_channel!`; the daemon's
decision/effect language lives in **per-plane runtime schemas**
(`nexus.schema` / `sema.schema`) rather than a hand-rolled Component
Command + `ToSemaOperation` layering; and the owner-only mutations are
split into a **separate meta contract** (`meta-signal-lojix`) rather
than riding one channel alongside the reads. The Sema-class projection
is the daemon's concern in its own plane schema, not a layer of this
wire contract.

## 8 · Daemon note — local builds permitted

A prior design carried a guard that rejected **local builds** at the
daemon. That guard was a **hallucinated guard — never psyche intent —
and is dropped** (Spirit `783n…`). The daemon must build local
closures (e.g. prometheus building its own model-heavy closures
locally) and must not reject a deploy on the grounds that it builds
locally. This is **daemon behaviour, not contract surface** — it is
recorded here only so the re-target of the daemon crate carries it
forward; `signal-lojix` itself encodes no build-locality policy.

## 9 · Cross-cutting context

- Workspace `~/primary/ESSENCE.md` is upstream of every rule.
- `meta-signal-lojix` is the owner-only policy leg of this pair
  (`Deploy` / `Pin` / `Unpin` / `Retire`); it cross-imports this
  contract's shared types via `signal-lojix:lib:TypeName`. Carried as
  a path-dependency package now; lands as its own repo at cutover.
- `signal-frame` at `github:LiGoldragon/signal-frame` is the mail-
  envelope / wire kernel this contract's codec rides on.
- `lojix` at `github:LiGoldragon/lojix` is the daemon implementation
  whose evolution drives this contract; both binaries (the long-lived
  `lojix-daemon` orchestrator and the thin `lojix` CLI client) live in
  that crate, with the Nexus/SEMA per-plane runtime schemas.
- `schema-next` / `schema-rust-next` are the schema language and Rust
  emitter; the streaming event root (§4) is the named enhancement on
  the lojix path.
- `signal-cloud` / `meta-signal-cloud` at
  `github:LiGoldragon/signal-cloud` and `…/meta-signal-cloud` are the
  worked template for the ordinary/meta wire-contract pair.
- `lojix-cli` at `github:LiGoldragon/lojix-cli` is the legacy
  monolithic orchestrator; it stays at its current schema until CriomOS
  migrates to consume this daemon's projection, then retires. It does
  not gradually grow into a client of this contract.
