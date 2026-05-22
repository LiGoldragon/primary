# 139 — lojix triad audit (2026-05-21)

*Audit of the lojix triad on the new lean-rewrite branch
(`horizon-leaner-shape` worktrees only). The triad's owner-leg
(`owner-signal-lojix`) is missing — proposal sketched in §3. Working
contract is partially migrated (contract-local verbs landed, signal-
frame as dependency landed) but daemon code is still on signal-core,
still matches old `Request::DeploymentSubmission` variant names, and
has no signal-executor/Lowering/CommandExecutor surface. The pre-
existing `lojix-cli` repository is the legacy monolithic CLI from the
old stack, NOT the thin CLI of the new triad; under the
one-crate-two-binaries shape it is already inside `lojix/` and the
separate repo retires alongside the production stack.*

## 0 · TL;DR

The new lojix triad is roughly **a quarter migrated**: the working
contract surface is half-done (verbs done; nota-codec derives done;
no observable block; no `signal-sema` projection alignment), the
daemon is **not migrated at all** beyond depending on signal-frame
through its contract dep (the daemon's direct deps are still
`signal-core` + `signal-lojix` and there is no signal-executor wiring),
and the owner contract does not yet exist.

State summary against the spirit-template (the engine-manager triad
audit's §4 cross-cutting table, since dropped):

| Step | Spirit | Lojix (new branch) |
|---|---|---|
| signal-core → signal-frame at contract | done | done (signal-lojix Cargo.toml line 19) |
| Old Sema-verbs → contract-local | done | **done** (Deploy/Pin/Unpin/Retire/Query/Watch*/Unwatch*) |
| Daemon onto signal-frame | done | **NOT DONE** (lojix/Cargo.toml line 25; src/socket.rs:9-12; src/client.rs:2; src/error.rs:11,60) |
| `wire::Request` enum variant names match contract | n/a | **NOT DONE** (runtime.rs:214 still matches `DeploymentSubmission` while contract declares `Deploy(DeploymentRequest)`) |
| Daemon onto signal-executor | done | **NOT DONE** (no `signal_executor` import; no `Lowering`/`CommandExecutor` impl) |
| `ToSemaOperation` / `ToSemaOutcome` on local Command/Effect types | done | **NOT DONE** (no `LojixCommand` enum exists) |
| Observable block in contract | done | **NOT DONE** (no `observable { … }` in `signal_channel!`) |
| Owner signal contract | done (`owner-signal-persona-spirit`) | **MISSING** (`owner-signal-lojix` repo does not exist) |
| CLI two-socket dispatch | done | **NOT DONE** (CLI is one-socket; no owner-side to dispatch to anyway) |
| BatchErrorClassification on engine errors | done | **NOT DONE** (no executor path) |
| Stream-close grammar (macro owns token) | done | done (`close UnwatchDeployments`/`UnwatchCacheRetention` syntax in contract lib.rs:672-678) |
| `lojix-cli` separate repo | n/a | **deviation flagged** (it's the legacy monolithic CLI; the new triad's thin CLI is bundled in `lojix/`) |

**Priority for the triad's next slice**: file the
`owner-signal-lojix` repository with the policy surface sketched in
§3; resync the daemon's `wire::*` enum match arms against the new
contract names (mechanical, unblocks compile); move daemon's direct
deps from `signal-core` to `signal-frame`; add `observable` block to
the working contract; then the load-bearing structural piece —
migrate the daemon onto signal-executor with `LojixCommand`,
`LojixEffect`, and the three-layer trait stack.

## 1 · /257 findings status

`/257` (`reports/designer/257-signal-contracts-names-and-shape-audit.md`)
audited the signal-* contract crates and did NOT include lojix in its
sweep (verified by grep). So this audit raises lojix's findings from
scratch against the same template; they're catalogued in §2 below
rather than mapped to /257 numbers. The cross-cutting smells /257
flagged elsewhere — frame alias-dance, `UnknownKindForVerb` rename,
nota-codec derive coverage, ancestry-prefix smell, repeated-suffix
schema smell, missing observable block, single-field timestamps —
each find their own status here:

### `signal-lojix` against the /257 cross-cutting smells

- **Frame alias-dance (`/257` §1.10 / bead `primary-77hh`):** N/A —
  the macro emits clean unprefixed names per the current
  `signal_frame::signal_channel!`. `signal-lojix/src/lib.rs:641-680`
  declares one channel `Lojix`, and no `pub use` re-exports of
  prefixed forms appear in lib.rs (the single channel doesn't need
  module disambiguation per
  `intent/component-shape.nota` 2026-05-21T10:30:00Z).
- **`UnknownKindForVerb` rename (`primary-k3bu`):** not surfaced —
  no `UnknownKindForVerb` references in lojix or signal-lojix source
  (grep returns empty). The bead's mechanical fix likely doesn't
  reach lojix.
- **nota-codec derive coverage (`primary-u0lh`):** clean. Every type
  in signal-lojix lib.rs uses `#[derive(NotaRecord)]`,
  `#[derive(NotaEnum)]`, `#[derive(NotaSum)]`,
  `#[derive(NotaTransparent)]`, or `#[derive(NotaTryTransparent)]`.
  No hand-written codec impls.
- **Ancestry-prefix smell (`/257` §1.5):** light. Most types in
  `signal-lojix` are clean (`ClusterName`, `NodeName`, `DeploymentId`,
  `DeploymentRequest`, `DeploymentAccepted`, `DeploymentRejected`,
  `Generation`, `GenerationKind`, `GenerationState`). Two carry the
  `Deployment*` prefix where the crate's domain already supplies
  "deployment" — see §2.3.
- **Repeated-suffix smell (`/257` §3 / `skills/naming.md` §"repeated
  category words"):** present in the reply variants — see §2.4.
- **No observable block (`/257` §1.11):** present — see §2.5.
- **Single-field timestamps (`/257` §1.12):** N/A — lojix's typed
  payloads do not yet carry agent-facing timestamps. Capture is
  daemon-stamped (per
  `intent/persona.nota` 2026-05-20 21:53 Correction). The current
  observation records (`Submitted`, `Building`, `Built`, `Failed`,
  etc.) carry no time field at all on the wire; they're meant to
  arrive in sequence with the subscription stream's own arrival
  ordering. Worth verifying psyche intent says they should not — see
  §4 open question.

## 2 · New findings specific to this triad

### 2.1 — `wire::Request` variant names in the daemon disagree with the contract

This is the **load-bearing compile-blocking issue** the report
surfaces.

The contract (`signal-lojix/src/lib.rs:641-652`) declares:

```text
operation Deploy(DeploymentRequest)
operation Pin(Pin)
operation Unpin(Unpin)
operation Retire(Retire)
operation Query(GenerationQuery)
operation WatchDeployments(WatchDeployments) opens DeploymentObservationStream
operation UnwatchDeployments(DeploymentObservationToken)
operation WatchCacheRetention(WatchCacheRetention) opens CacheRetentionObservationStream
operation UnwatchCacheRetention(CacheRetentionObservationToken)
```

The daemon (`lojix/src/runtime.rs:213-307`) matches against pre-
migration variant names:

```text
wire::Request::DeploymentSubmission(submission)
wire::Request::CacheRetentionRequest(_)
wire::Request::GenerationQuery(query)
wire::Request::DeploymentObservationSubscription(subscription)
wire::Request::CacheRetentionObservationSubscription(_)
wire::Request::DeploymentObservationRetraction(token)
wire::Request::CacheRetentionObservationRetraction(token)
```

These names belonged to the previous shape (still documented in the
contract's own `ARCHITECTURE.md` §"2 · Channel Surface" at
lines 86-128, which the migration history block at the top of the
file calls out as stale). The current macro emits an enum with
variants `Deploy`, `Pin`, `Unpin`, `Retire`, `Query`,
`WatchDeployments`, `UnwatchDeployments`, `WatchCacheRetention`,
`UnwatchCacheRetention`. The daemon doesn't compile against the
current contract.

This is **package 0** of the migration: the rest of the daemon work
sits behind this rename. Mechanical, but wide — also touches
`lojix/src/socket.rs:188-198, 287-308, 401-418` (the
`SocketRequest::from_channel_request` path uses
`wire::Request::DeploymentObservationSubscription` directly),
`lojix/src/client.rs` (request decode path), and the
`OpenDeploymentObservationStream` message that still references the
old type name `wire::DeploymentObservationSubscription` at
`lojix/src/runtime.rs:313-315`.

The contract also retired a few payload types and added new ones:

| Old name | New name |
|---|---|
| `DeploymentSubmission` | `DeploymentRequest` |
| `CacheRetentionRequest` | split into three records: `Pin`, `Unpin`, `Retire` |
| `DeploymentObservationSubscription` | `WatchDeployments` |
| `CacheRetentionObservationSubscription` | `WatchCacheRetention` |
| `DeploymentObservationRetraction` | `UnwatchDeployments` (payload is `DeploymentObservationToken`) |
| `CacheRetentionObservationRetraction` | `UnwatchCacheRetention` (payload is `CacheRetentionObservationToken`) |

The contract's own `ARCHITECTURE.md §"2 · Channel Surface"` block
shows the OLD shape (Assert/Mutate/Match/Subscribe/Retract) — that
section is stale and must be rewritten to match `src/lib.rs`. The
migration-history paragraph at the top of `ARCHITECTURE.md` calls
this out but doesn't rewrite §2.

### 2.2 — Daemon depends on `signal-core`, not `signal-frame`

`lojix/Cargo.toml:24-25`:

```toml
# Wire kernel — Frame, handshake, SignalVerb, channel macro.
signal-core  = { git = "https://github.com/LiGoldragon/signal-core.git" }
```

There is no `signal-frame` dependency in the daemon crate even
though the contract depends on signal-frame. Source-level evidence:

- `lojix/src/client.rs:2` — `use signal_core::{Reply as CoreReply, RequestPayload, SubReply};`
- `lojix/src/error.rs:11` — `Frame(#[from] signal_core::FrameError)`
- `lojix/src/error.rs:60` — `RequestRejected(signal_core::RequestRejectionReason)`
- `lojix/src/socket.rs:9-12` — `use signal_core::{ExchangeIdentifier, ExchangeLane, LaneSequence, NonEmpty, Operation, Reply as CoreReply, SessionEpoch, SignalVerb, StreamEventIdentifier, SubReply, SubscriptionTokenInner};`
- `lojix/src/socket.rs:418` — `let reply = CoreReply::rejected(signal_core::RequestRejectionReason::Internal);`

The daemon imports `SignalVerb` directly — the Sema-verb enum the
workspace retired (per `intent/component-shape.nota` 2026-05-19T19:30Z
Correction Maximum: *"Public contract verbs should be the client's
domain actions … not the database execution verbs"*).
`signal-frame` is the kernel home for frame mechanics now
(`intent/component-shape.nota` 2026-05-19T20:00:00Z Decision Maximum:
*"signal-core is renamed to signal-frame"*). The daemon needs the
full sweep `signal_core::` → `signal_frame::` plus removal of
`SignalVerb` references — both the import and its use in the socket
ack path.

### 2.3 — No `LojixCommand` / `LojixEffect` / signal-executor wiring

The daemon dispatches public request variants directly to actor
behavior. `lojix/src/runtime.rs:213-308` is one big match against
`wire::Request` that calls actor `ask()` methods. No three-layer
shape:

- no `LojixCommand` enum naming the daemon's executable language;
- no `LojixEffect` enum naming the daemon's effect outcomes;
- no `impl Lowering for LojixLowering` translating
  `wire::Operation` → `OperationPlan<LojixCommand>`;
- no `impl CommandExecutor for LojixCommandExecutor` wrapping the
  actor mesh;
- no `impl BatchErrorClassification for Error` mapping engine
  failures to `BatchFailureReason` / `RetryClassification` /
  `CommitStatus`;
- no `impl ToSemaOperation for LojixCommand` projecting to the
  payloadless Sema vocabulary;
- no `impl ToSemaOutcome for LojixEffect` projecting effect
  outcomes;
- no `signal_executor::Executor::execute(...)` call anywhere.

This is the same shape /258 §2.2 surfaced for the engine-manager
daemon — both daemons skipped the executor migration. For lojix the
work is larger than spirit's because the daemon has 2105 lines in
`deploy.rs` alone (per
`reports/system-specialist/154` §6 "Split `deploy.rs`" and
`reports/system-assistant/28` Gap 8).

The work splits cleanly into three subtypes per
`/154` §"Important split":

1. **Admission and durable state commands** — allocate deployment,
   record submitted/building/built/failed observations, pin/unpin/
   retire generations, open/close watch subscriptions. These are
   sema-engine atomic and slot into the standard executor shape.
2. **Effect workflow commands** — criome authorize, project
   horizon, stage generated inputs, copy closure, invoke nix, set
   GC root, activate. These are actor-owned, timeout-bounded, and
   observed via state transitions; they do not block the executor's
   commit path.
3. **Query commands** — generation listings, watch snapshots —
   sema-engine `Match`.

A first command sketch (the names are designer judgment, not
psyche-stated):

```rust
pub enum LojixCommand {
    // Working-state durable commands (atomic via sema-engine)
    AllocateDeployment,
    RecordDeploymentSubmitted(DeploymentSubmittedFacts),
    RecordDeploymentBuilding(DeploymentBuildingFacts),
    RecordDeploymentBuilt(DeploymentBuiltFacts),
    RecordDeploymentFailed(DeploymentFailedFacts),
    OpenDeploymentWatch(DeploymentWatchFacts),
    CloseDeploymentWatch(DeploymentObservationToken),
    OpenCacheRetentionWatch(CacheRetentionWatchFacts),
    CloseCacheRetentionWatch(CacheRetentionObservationToken),
    PinGeneration(GenerationId),
    UnpinGeneration(GenerationId),
    RetireGeneration(GenerationId),

    // Query
    ListGenerations(GenerationQuery),

    // Effect-workflow commands (actor-owned, observed)
    AuthorizeDeployment(DeploymentRequest, DeploymentRequestDigest),
    ProjectHorizon(DeploymentRequest),
    StageGeneratedInputs(StagingPlan),
    RunBuild(BuildPlan),
    CopyClosure(CopyPlan),
    UpdateGarbageCollectionRoot(GcRootMutation),
    ActivateSystem(ActivationPlan),

    // Explicit no-op for accepted-but-no-change paths
    RecordIdempotentApply(IdempotentApplyReason),
}
```

The ToSemaOperation projection follows the pattern named in
`/154` §"Sema classification layer":

| Command | Sema class |
|---|---|
| `Record*`, `Allocate*`, `Open*Watch`, `Pin*` | `Assert` |
| Transition (e.g., `RetireGeneration`, `UnpinGeneration`, `Close*Watch`) | `Mutate` or `Retract` per fact-vs-tombstone distinction |
| `ListGenerations` | `Match` |
| watch-open path that pushes events | `Subscribe` |
| `AuthorizeDeployment` synchronous validate | `Validate` |
| `ProjectHorizon`, `StageGeneratedInputs`, `RunBuild`, `CopyClosure`, `Activate*`, `UpdateGarbageCollectionRoot` | effect-actor, Sema projection through their observed state-change records (which are themselves `Assert` of effect-history facts) |

### 2.4 — `LojixReply` has the repeated-suffix smell

`signal-lojix/src/lib.rs:653-663`:

```text
reply LojixReply {
    DeploymentAccepted(DeploymentAccepted),
    DeploymentRejected(DeploymentRejected),
    CacheRetentionAccepted(CacheRetentionAccepted),
    CacheRetentionRejected(CacheRetentionRejected),
    GenerationListing(GenerationListing),
    DeploymentObservationSubscriptionOpened(...),
    DeploymentObservationSubscriptionClosed(...),
    CacheRetentionObservationSubscriptionOpened(...),
    CacheRetentionObservationSubscriptionClosed(...),
}
```

Two diagnostic patterns:

1. **`Deployment*Accepted/Rejected` and `CacheRetention*Accepted/Rejected`**
   are the symptom of the request-side merge that already happened
   (Pin/Unpin/Retire all sit under cache retention) but the reply
   side didn't follow. Per `skills/naming.md` §"repeated category
   words", the lift is:

   ```text
   reply LojixReply {
       Accepted(Acceptance),
       Rejected(Rejection),
       Generations(GenerationListing),
       SubscriptionOpened(SubscriptionOpened),
       SubscriptionClosed(SubscriptionClosed),
   }

   pub enum Acceptance {
       Deployment(DeploymentAccepted),
       CacheRetention(CacheRetentionAccepted),
   }

   pub enum Rejection {
       Deployment(DeploymentRejected),
       CacheRetention(CacheRetentionRejected),
   }

   pub enum SubscriptionOpened {
       Deployments(DeploymentObservationSubscriptionOpened),
       CacheRetention(CacheRetentionObservationSubscriptionOpened),
   }

   pub enum SubscriptionClosed {
       Deployments(DeploymentObservationSubscriptionClosed),
       CacheRetention(CacheRetentionObservationSubscriptionClosed),
   }
   ```

   That collapses 8 reply variants → 4 with two relation layers.

2. **`DeploymentObservationSubscriptionOpened` (six words)** and its
   four siblings restate the entire chain "deployment + observation
   + subscription". Per `skills/naming.md` §"Anti-pattern: prefixing
   names with their namespace or domain", once these are inside the
   `SubscriptionOpened` sum, the inner names can drop the
   `Subscription*` repetition: `Deployments(DeploymentObservationOpened)`
   or simply `Deployments(DeploymentWatchOpened)` since "Watch" is
   already the verb the contract chose for opening. The same applies
   to the closed-side.

   Even cleaner: per `/150` §"Repeated suffixes lift into typed sums",
   the inner records can also drop `Subscription` from their names
   entirely — `DeploymentObservationOpened { token, observations }`,
   `CacheRetentionObservationOpened { token, observations }`. The
   structural reality is that the opened-record IS the subscription;
   saying so in every name layer is the ancestry-prefix anti-pattern.

### 2.5 — No observable block

`signal_channel! { channel Lojix { ... } }` declares no observable
block. Per `intent/component-shape.nota` 2026-05-20T02:00:00Z
Decision Maximum: *"Tap/Untap is mandatory for persona components,
no author override. … Non-persona small utilities don't declare an
observable block at all."*

Lojix is not a `persona-*` component, so the **mandatory** clause
doesn't directly apply. But lojix is also not a "small utility" —
it's deployment infrastructure for the workspace, owns durable
state, has its own peer-callable contract, and would benefit from
`persona-introspect`-style cross-component observability when that
arrives. The question is workspace direction, not just a
mechanical decision.

`reports/system-assistant/28` §Gap 10 raised this and recommended
explicit psyche resolution. `reports/system-specialist/154` open
question #1 asks the same thing.

Designer lean: **add the observable block** (working contract only,
not policy contract). Reason:
- lojix daemons WILL talk to other daemons (criome-daemon
  authorization; future peer lojix-daemons; future arca-daemon);
  cross-daemon introspection is the universal mechanism;
- the deployment domain observations (`WatchDeployments`,
  `WatchCacheRetention`) are domain-shaped event streams for
  specific lifecycle queries — they're not the same as the
  universal observer hook persona-introspect uses;
- "debug the debugger" (`intent/persona.nota` 2026-05-21T10:00:00Z)
  generalises: a deployment component that observes its own builds
  but isn't itself observable from above is a worse shape than one
  that's observable both ways.

```rust
signal_channel! {
    channel Lojix {
        operation Deploy(DeploymentRequest),
        // ... existing operations ...
    }
    reply LojixReply { ... }
    event LojixEvent { ... }
    stream DeploymentObservationStream { ... }
    stream CacheRetentionObservationStream { ... }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}
```

This is in addition to, not in place of, the domain watch streams.
Confirm with psyche before adding (see §4 open question 1).

### 2.6 — `lojix-cli` separate repository deviates from triad invariant

`protocols/active-repositories.md:80,94` and the repo state confirm:
the new triad shape is **one crate, two binaries** —
`lojix-daemon` (long-lived orchestrator) + `lojix` (thin CLI client)
— per `~/primary/AGENTS.md` "Binary naming" rule.
`lojix/Cargo.toml:15-21` correctly defines both binaries inside the
one crate.

The `/git/github.com/LiGoldragon/lojix-cli` repository (and its
`~/wt/.../lojix-cli/horizon-re-engineering` worktree) is the
**production legacy** monolithic CLI from before the daemon-mesh
direction landed. Reading
`/home/li/wt/.../lojix-cli/horizon-re-engineering/README.md`:

> *"`lojix-cli` is the CriomOS deploy orchestrator. It reads one
> Nota request, projects a cluster proposal through `horizon-lib`,
> materializes the flake override inputs CriomOS expects, runs
> `nix`, and optionally activates the result."*

That's the OLD shape — the CLI itself owns horizon projection, Nix
invocation, activation. Under the new triad invariant (Triad
invariant 1: *"The CLI has exactly one Signal peer — its own
daemon"* and *"Any database … includes the component's own
redb/sema store: the daemon is the only process that opens durable
component state"*), this is a triad violation.

**This is a correct state of affairs, not a finding.** Per
`INTENT.md` §"Two deploy stacks coexist": production runs the old
monolithic `lojix-cli` stack on `main`; the lean rewrite — new
`lojix` daemon + thin `lojix` CLI — lives on `horizon-leaner-shape`
worktrees. The `lojix-cli` repository retires as part of the
coordinated cutover after the rewrite reaches feature parity. The
worktree under `~/wt/.../lojix-cli/` is the production stack's
working surface for live-cluster fixes; it does not get pulled into
the new triad.

The audit catches the surface for completeness. The new triad's
thin CLI is `lojix/src/bin/lojix.rs`.

### 2.7 — `DeploymentRequest` payload naming and the lone digest method

`signal-lojix/src/lib.rs:387-410` declares the typed deploy payload:

```rust
pub struct DeploymentRequest {
    pub cluster: ClusterName,
    pub node: NodeName,
    pub source: ProposalSource,
    pub flake: FlakeReference,
    pub plan: DeploymentPlan,
    pub builder: BuilderSelection,
    pub substituters: Vec<NodeName>,
}

impl DeploymentRequest {
    pub fn canonical_digest(&self) -> Result<DeploymentRequestDigest> { ... }
}
```

Three small things:

1. The contract's own `ARCHITECTURE.md` §"3.1 Deployment" still calls
   this `DeploymentSubmission` and gives the digest method as
   `DeploymentSubmission::canonical_digest()`. Stale doc.
2. The field `substituters: Vec<NodeName>` lists node *names*, not
   substituter URLs. That follows
   `intent/horizon.nota` 2026-05-19T12:26:44Z (variants-over-booleans,
   no operational constants in cluster data — the node name is the
   reference, the URL is constructed Nix-side from the node's
   `nixUrl`). Worth preserving through the rename: in the executor-
   path migration, the daemon's lowering reads
   `view::Node.nixUrl` after horizon projection, not the URL from the
   request.
3. The `Deployment*` prefix on `DeploymentRequest`,
   `DeploymentAccepted`, `DeploymentRejected`,
   `DeploymentRejectionReason` is the ancestry-prefix smell —
   "deployment" IS the contract's domain. Per
   `intent/naming.nota` 2026-05-19T14:40:38Z Correction Maximum,
   inside `signal-lojix` these become `Request`, `Accepted`,
   `Rejected`, `RejectionReason`. Spirit precedent: spirit's contract
   has `Entry`, not `IntentEntry`. Counter: `Generation*`, `Pin`,
   `Unpin`, `Retire`, `Cache*` already drop the prefix. The
   inconsistency is between the deployment-side names (full prefix)
   and everything else (clean).

That said: this is name-cleanup-during-the-rename pass, not a
separate slice. Folds into §2.1's work.

### 2.8 — `Pin`, `Unpin`, `Retire` payload-name = variant-name collision

`signal-lojix/src/lib.rs:552-564`:

```rust
pub struct Pin { pub generation: GenerationId, }
pub struct Unpin { pub generation: GenerationId, }
pub struct Retire { pub generation: GenerationId, }
```

And the channel declares `operation Pin(Pin)`, `operation Unpin(Unpin)`,
`operation Retire(Retire)`. The three structs are identical shape —
one field, a `GenerationId`. The three variants exist so the public
verb expresses the action; the payload struct is then redundant
ceremony.

Two cleaner shapes:

A. **Bare `GenerationId` payloads.** The operation variant names the
   verb; the payload is the noun. `operation Pin(GenerationId)`,
   `operation Unpin(GenerationId)`, `operation Retire(GenerationId)`.
   Cleanest; works because the variant tag distinguishes the three.

B. **Single `CacheRetention(CacheRetentionMutation)` operation with
   a Pin/Unpin/Retire payload sum.** Collapses three operations to
   one. But this is what the contract had pre-migration and the
   psyche split it apart explicitly per
   `intent/component-shape.nota` 2026-05-19T19:30Z Decision Maximum
   (*"Public contract verbs should be the client's domain actions"*)
   and `intent/component-shape.nota` 2026-05-19T20:30Z (*"verbs
   aren't to be feared"*). So A is the right cleanup, not B.

Designer lean: A.

### 2.9 — `wire::SocketMode` carved into the contract instead of `signal-frame`

`signal-lojix/src/lib.rs:268-278` declares:

```rust
pub struct SocketMode(u32);
```

Same type would apply to every triad daemon's `<Daemon>Configuration`
that names a Unix socket mode (`owner-signal-persona-spirit`,
`signal-persona`, ...). Currently every component invents its own.
Worth flagging for a workspace-wide move into a shared crate
(probably `nota-config` since
`LojixDaemonConfiguration` already uses
`nota_config::impl_rkyv_configuration!`). Low priority — out of scope
for the lojix triad audit specifically.

### 2.10 — `LojixDaemonConfiguration.peer_daemons` placed in working contract

`signal-lojix/src/lib.rs:286-303`:

```rust
pub struct PeerDaemonBinding {
    pub cluster: ClusterName,
    pub node: NodeName,
    pub daemon_socket_path: WirePath,
}

pub struct LojixDaemonConfiguration {
    pub daemon_socket_path: WirePath,
    pub daemon_socket_mode: SocketMode,
    pub daemon_socket_group: Option<UnixGroup>,
    pub horizon_configuration_source: WirePath,
    pub state_directory: WirePath,
    pub gc_root_directory: WirePath,
    pub peer_daemons: Vec<PeerDaemonBinding>,
    pub operator_identity: OperatorIdentity,
    pub owned_cluster: ClusterName,
}
```

The configuration record lives in the working contract today because
that's where the contract crate sits. But several of these fields are
**policy** under the two-state taxonomy
(`intent/component-shape.nota` 2026-05-19T01:30:00Z Decision Maximum):

- `daemon_socket_path`, `daemon_socket_mode`, `daemon_socket_group`,
  `state_directory`, `gc_root_directory` — startup-time bindings,
  not policy; these stay on the daemon-config record passed at boot.
- `horizon_configuration_source` — policy (which pan-horizon file is
  authoritative).
- `peer_daemons` — policy (which other daemons this daemon trusts as
  peers; cluster-shape question).
- `operator_identity` — policy (who is this daemon acting on behalf
  of).
- `owned_cluster` — policy (which cluster this daemon serves).

Under the
two-state model, those policy fields:
- bootstrap from `bootstrap-policy.nota` on first start;
- mutate through owner-signal-lojix variants after that
  (`ConfigureHorizonSource`, `RegisterPeerDaemon`,
  `RetirePeerDaemon`, etc.) — see §3 below;
- never appear in the working contract.

The configuration record `LojixDaemonConfiguration` should probably
keep ONLY the daemon-process startup bindings (the socket address,
the state-dir, the gc-root-dir), with the policy fields moving onto
the owner contract and into the daemon's policy-state tables.

This is consistent with the engine-manager triad
(`/258` §2.6's read of `SpawnEnvelope`).

## 3 · Proposed owner signal — `owner-signal-lojix`

Per `intent/deploy.nota` 2026-05-20T17:10:00Z Decision Maximum:
*"owner-signal-lojix is no longer deferred. Create the owner contract
now alongside signal-lojix; the CLI two-socket dispatch policy … is
developed in parallel with the owner-contract work, not as a
prerequisite."*

Per `intent/component-shape.nota` 2026-05-18T22:15:57Z Constraint
Maximum: *"owner-signal-<component> is part of the triad, not a
follow-up arc. A daemon with only the ordinary signal-<component>
surface is not yet triad-shaped."*

The owner-signal-lojix contract has to cover policy mutations and
ordering. Naming per `skills/naming.md` (the contract's domain is
"lojix" — drop the prefix; verbs are domain actions; the contract
crate already supplies "lojix" context).

### 3.1 — Policy state lojix carries

Synthesised from `intent/deploy.nota` and the gap-7 (now-resolved)
audit in `reports/system-assistant/28`. **Conservative-by-default
applies**: psyche has settled the existence of the owner contract;
the specific variant set is designer extrapolation from the deploy
intent records, NOT psyche-stated. Mark these as **proposals to
ratify**, not landed shape.

Policy state in lojix:

1. **Operator identity** — who this daemon acts on behalf of.
   Bootstrap-stamped from the policy file; could be rotated by owner
   `SetOperator(OperatorIdentity)`.
2. **Owned cluster** — which cluster this daemon serves. Bootstrap-
   stamped; the daemon is cluster-operator-owned per
   `lojix/ARCHITECTURE.md §"5 · Invariants"`. Mutation is rare and
   high-stakes — likely an owner-signal `RebindCluster(ClusterName)`
   operation gated behind explicit acknowledgement.
3. **Pan-horizon source** — path to the
   pan-horizon configuration the daemon reads. Mutable per
   `intent/deploy.nota` (the daemon reads the configured pan-horizon
   per request; the source file is policy).
4. **Peer daemon registry** — bindings to other `lojix-daemon`s and
   to the local `criome-daemon`. Per
   `intent/deploy.nota` 2026-05-17T15:30Z: *"daemons talk to each
   other"*. Peer bindings are policy because the daemon trusts these
   peers' signed authorizations and routing decisions.
5. **Builder policy** — which nodes count as eligible builders. Per
   `intent/deploy.nota` 2026-05-17T11:00:00Z: deploy variables
   include where the build happens. The set of eligible builders is
   a policy dial.
6. **Cache trust policy** — which substituters are accepted, with
   what trust class. Per `intent/deploy.nota` 2026-05-17T13:30:00Z:
   *"transient binary-cache trust gets installed for a single
   deploy without operator-side ssh-and-edit"* — the persistent
   substituter set IS policy, the transient per-deploy keys are
   working-state effects.
7. **Believed-topology baseline** — per
   `intent/deploy.nota` 2026-05-17T11:00:00Z: *"the daemon believes
   the topology … cluster shape, node roles, reachability,
   latency, bandwidth, and cost."* The baseline is policy; the
   per-request mutations are working state.
8. **Nix configuration policy** — per
   `intent/deploy.nota` 2026-05-17T13:30:00Z Decision Maximum:
   *"lojix-daemon takes control of nix configuration."* The
   persistent slice of `/etc/nix/nix.conf` the daemon owns
   (sandboxing, build-cores defaults, store path, signing-key
   trust) is policy.
9. **Cluster signing-key reference** — per
   `intent/deploy.nota` 2026-05-17T13:30:00Z: *"all nodes should
   have a nix signing key (clavifaber populated on first boot)."*
   The pub-key reference is policy state; the daemon uses it to
   verify peer-built artifacts.
10. **GC retention policy** — per
    `lojix/ARCHITECTURE.md §"6 · Constraints"` C19, the cache
    retention domain is exposed on the working contract
    (Pin/Unpin/Retire). But the DEFAULTS that apply when no
    explicit pin exists — retention windows, max-pinned-generations,
    auto-retire-after-failure — are policy.
11. **Authorization policy** — per
    `intent/deploy.nota` 2026-05-17T15:30:00Z: *"Authorization for
    a signal-lojix call is propagated through the criome-daemon
    topology."* The criome-daemon endpoint reference is policy.
    Whether to require authorization for builds, activations, or
    both is policy. (Currently the daemon's
    `CriomeAuthorizationPolicy::unavailable_until_criome_socket_lands`
    is a stub; the policy field belongs in the owner contract.)

### 3.2 — Operations on owner-signal-lojix

Conservative shape, contract-local verbs (not Sema words). The
verbs name the owner's domain actions on policy state:

```rust
signal_channel! {
    channel OwnerLojix {
        // Configuration — startup-time policy mutations
        operation Configure(Configuration),

        // Peer-daemon registry
        operation RegisterPeer(PeerDaemonBinding),
        operation RetirePeer(PeerDaemonBindingId),

        // Builder policy
        operation TrustBuilder(BuilderTrust),
        operation RevokeBuilder(NodeName),

        // Cache trust policy
        operation TrustSubstituter(SubstituterTrust),
        operation RevokeSubstituter(SubstituterTrustId),

        // Believed-topology baseline corrections
        operation CorrectTopology(TopologyCorrection),

        // Nix configuration policy
        operation SetNixConfigPolicy(NixConfigPolicy),

        // GC retention defaults
        operation SetRetentionPolicy(RetentionPolicy),

        // Authorization policy
        operation SetAuthorizationPolicy(AuthorizationPolicy),

        // Inspection (owner reads policy state)
        operation Inspect(InspectionRequest),
    }
    reply OwnerLojixReply {
        Configured(ConfigurationAccepted),
        ConfigurationRejected(ConfigurationRejected),
        PeerRegistered(PeerDaemonBindingId),
        PeerRetired(PeerDaemonBindingId),
        BuilderTrusted(BuilderTrustId),
        BuilderRevoked(NodeName),
        SubstituterTrusted(SubstituterTrustId),
        SubstituterRevoked(SubstituterTrustId),
        TopologyCorrected(TopologyVersion),
        NixConfigPolicySet(NixConfigPolicyVersion),
        RetentionPolicySet(RetentionPolicyVersion),
        AuthorizationPolicySet(AuthorizationPolicyVersion),
        Inspection(InspectionResult),
        Unimplemented(Unimplemented),
    }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}
```

The names are designer judgment — every single one is a candidate
for psyche revision per `intent/component-shape.nota` 2026-05-20T12:11:26Z
Principle Maximum (*"be very critical of the signal types, names,
and the logic separation, the shape of the schema"*). The general
shape — one operation per policy concern, named as the owner's
action verb — follows the contract-local-verbs direction.

Naming critique on this proposal itself:

- `Configure(Configuration)` collapses too many policy mutations
  into one — psyche has settled "verbs are cheap"
  (`intent/component-shape.nota` 2026-05-19T20:30Z). Splitting
  `Configure` into per-concern operations
  (`ConfigureOperator(OperatorIdentity)`,
  `ConfigurePanHorizonSource(WirePath)`, etc.) reads as ugly
  ancestry-stuffing — better is the existing one-verb-per-concern
  shape further down the list (`SetNixConfigPolicy`, etc.). The
  `Configure(Configuration)` operation could retire entirely if
  every policy field has its own operation.
- `RegisterPeer` / `RetirePeer` follows engine-manager's
  `Announce` / `Retire` (`signal-persona/src/lib.rs`'s Supervision
  channel). Workspace consistency wins; `Register`/`Retire` is the
  precedent.
- `TrustBuilder` / `RevokeBuilder` reads better than
  `RegisterBuilder` / `RetireBuilder` because trust is the
  load-bearing dimension here, not registration. Same for
  substituters.
- `CorrectTopology` is correct shape: per
  `intent/deploy.nota` 2026-05-17T11:00:00Z the daemon maintains
  *believed* topology; the owner-side action is correcting that
  belief, not setting it.
- `SetNixConfigPolicy(NixConfigPolicy)` is fine because the policy
  itself is a typed record with many fields; one set-all-at-once
  variant per concern is the right granularity.
- `Inspect` is the read-side of the owner surface — the owner can
  inspect current policy state. This is `Match`-classified, not
  `Mutate`. Worth confirming whether a separate read surface is
  preferred over Inspect-style.

### 3.3 — `bootstrap-policy.nota` shape

Per `intent/component-shape.nota` 2026-05-19T01:30:00Z Decision
Maximum: *"the bootstrap file is in the repo and I guess it should
be called bootstrap-policy.nota."* And `intent/component-shape.nota`
2026-05-19T01:25:00Z Principle Maximum: *"Configuration is always
a Mutate."*

The lojix bootstrap shape, positional NOTA per `skills/nota-design.md`:

```nota
(
  (Configuration                       ;; operator identity, owned cluster, pan-horizon
    "li"
    "goldragon"
    "/etc/lojix/horizon.nota")
  (TrustBuilder ouranos Max)           ;; per-cluster initial builder trust
  (TrustBuilder prometheus High)
  (TrustSubstituter prometheus
    "5dAiX..."                         ;; nix pub-key
    High)
  (RegisterPeer goldragon ouranos
    "/run/lojix/peer.sock")
  (SetAuthorizationPolicy
    (RequireAuthorization Always)
    (CriomeEndpoint "/run/criome/daemon.sock"))
  (SetRetentionPolicy
    (MaxPinned 16)
    (RetainAfterFailure 7d))
  (SetNixConfigPolicy
    (Sandbox Strict)
    (BuildCores 0)                     ;; "use all"
    (TrustedSubstituters [ prometheus ]))
)
```

The bootstrap file is a sequence of typed owner-signal operations
applied once on first start, when the policy-state tables are empty.
After that, owner-signal authority is the only mutation path.

### 3.4 — Effects of having owner-signal-lojix on the rest of the triad

1. **CLI dispatch.** `lojix/src/bin/lojix.rs` becomes a two-socket
   client per `intent/component-shape.nota` 2026-05-20T13:00:00Z
   Clarification Maximum: *"Every CLI talks to two sockets … the
   CLI must dispatch each incoming NOTA request to the correct
   socket based on which contract the request belongs to."* The
   workspace-universal mechanism is the `signal_cli!` macro that
   takes both contracts and emits the compile-time dispatch table
   (`intent/persona.nota` 2026-05-20 21:53; landing per
   `reports/second-designer/129`). Lojix gets the same
   mechanism, no special-case routing.
2. **Daemon socket topology.** The daemon binds two sockets — the
   working socket (peer-callable) and the policy socket (owner-only).
   The working socket sits at the current path
   (`/run/lojix/daemon.sock`); the policy socket needs a name. Per
   `intent/component-shape.nota` 2026-05-20T13:00:00Z: working and
   policy are the canonical names. Suggest `/run/lojix/policy.sock`
   (mode 0600, owned by the cluster-operator group).
3. **Daemon configuration.** `LojixDaemonConfiguration` shrinks (per
   §2.10) to startup-only bindings; the policy fields move into the
   policy-state tables, populated from `bootstrap-policy.nota`.
4. **`LojixDaemonConfiguration` gets a `policy_socket_path: WirePath`
   and `policy_socket_mode: SocketMode`** alongside the existing
   working-socket fields.
5. **`LojixCliConfiguration` gets a `policy_socket_path: WirePath`**
   so the CLI knows where the policy socket lives. Both socket paths
   are CLI startup configuration; both come from the same `nota-config`
   file or two sibling files.
6. **The bootstrap-policy.nota file lives in the `lojix/` runtime
   repo** (per `intent/component-shape.nota` 2026-05-19T01:30Z),
   not the owner-signal-lojix contract repo. The contract owns the
   record types the bootstrap file decodes into; the runtime owns
   the policy seed itself.

## 4 · Recommended next slice

In priority order (lower numbers are gates for higher numbers):

1. **Create `owner-signal-lojix` repository** with the policy
   surface sketched in §3 — exact variant set deferred to psyche
   ratification. This unblocks the triad-shape question; the
   running daemon doesn't yet need any owner operations to function,
   so the contract can land with the variant set and stubs, and the
   daemon adds the policy-side actors and handlers incrementally.
   Per `intent/component-shape.nota` 2026-05-18T22:15:57Z Constraint
   Maximum, the contract ships before being triad-complete; this is
   that landing.
2. **Resync daemon match arms against current contract names**
   (§2.1). Mechanical compile-blocking pass. Touches `runtime.rs`,
   `socket.rs`, `client.rs`. After this, the daemon compiles against
   `signal-lojix` HEAD.
3. **Move daemon dependency from `signal-core` to `signal-frame`**
   (§2.2). Touches `Cargo.toml`, all six `*.rs` source files that
   import `signal_core::`. Drop the explicit `SignalVerb` import in
   `socket.rs:11` since SignalVerb retired.
4. **Drop ancestry prefixes inside `signal-lojix`** (§2.7) — rename
   `DeploymentRequest` → `Request`, `DeploymentAccepted` → `Accepted`,
   `DeploymentRejected` → `Rejected`,
   `DeploymentRejectionReason` → `RejectionReason`. The other domains
   (Generation, Cache, Pin/Unpin/Retire) are already clean.
   Note: collides with §5 below — defer the Deployment prefix drop
   until after §5 in case the lift-into-typed-sums work surfaces a
   different shape.
5. **Lift the reply repeated-suffix smell into typed sums** (§2.4).
   This is a contract design pass — reduces 9 LojixReply variants to
   5 with two relation layers.
6. **Add `observable` block to `signal-lojix`** working contract
   (§2.5). Confirm with psyche before landing (see §6 open question
   1). One-line change to the contract; downstream daemon gets the
   universal observer hook automatically through the macro.
7. **Migrate daemon onto signal-executor** (§2.3) — the load-bearing
   structural piece. Mechanically:
   - Define `LojixCommand` enum in `lojix/src/command.rs` (new file).
   - Define `LojixEffect` enum in `lojix/src/effect.rs` (new file).
   - Implement `impl Lowering for LojixLowering` (new file
     `lojix/src/lowering.rs`).
   - Implement `impl CommandExecutor for LojixCommandExecutor`
     wrapping the existing actor mesh (`lojix/src/executor.rs`).
   - Implement `impl BatchErrorClassification for crate::Error`.
   - Implement `impl ToSemaOperation for LojixCommand` (per the
     mapping table in §2.3).
   - Implement `impl ToSemaOutcome for LojixEffect`.
   - Wire `signal_executor::Executor::execute(request).await` into
     `socket.rs`'s connection-actor request handling.
   - Migrate `Pin`/`Unpin`/`Retire` cache-retention paths off
     "actors are not active in this runtime slice" stub
     (`lojix/src/runtime.rs:243-253`).
   - Wire criome authorization through the executor's lowering path
     instead of inside the `DeploymentActor`.
8. **Split `deploy.rs`** (2105 lines) per
   `reports/system-specialist/154` §6. Best done DURING the executor
   migration since the command/effect types decompose naturally
   into per-noun files (`deploy/ledger.rs`,
   `deploy/identity.rs`, `deploy/watch.rs`, `deploy/build_job.rs`,
   `deploy/generated_inputs.rs`,
   `deploy/garbage_collection_roots.rs`, `deploy/remote_inputs.rs`,
   `deploy/secrets.rs`).
9. **Wire daemon as a Signal client of `criome-daemon`** per
   `intent/deploy.nota` 2026-05-17T15:30:00Z. The clarification at
   2026-05-20T17:10:00Z says criome-mediated auth is DEFERRED from
   the lean-rewrite migration. So this step is named for the
   destination but not part of the current slice. The
   `CriomeAuthorizationPolicy::unavailable_until_criome_socket_lands`
   stub at `lojix/src/runtime.rs:43-44` stays in place.
10. **Generate CLI dispatch** (§3.4 item 1). Uses `signal_cli!` once
    the macro lands per
    `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`.
11. **Drop deployment-identity smell**
    (`reports/system-specialist/154` §5 + `reports/system-assistant/28`
    Gap 8) — replace
    `deployment_{n}` and `generation_{n}` projection with sema-backed
    slot/key identity.
12. **Sweep contract `ARCHITECTURE.md`** to remove every stale
    Assert/Mutate/Match/Subscribe/Retract reference. The migration-
    history paragraph at the top calls this out as known-stale; the
    sweep finishes it.
13. **Sweep `lojix/ARCHITECTURE.md`** for the same — it still talks
    about `wire::Request::DeploymentSubmission`,
    `CacheRetentionRequest`, `SubscriptionEvent` shapes that are now
    `Deploy(DeploymentRequest)`,
    `Pin/Unpin/Retire`, etc. Lines 89-113.

Activities §1, §2, §3 can land in parallel — they don't conflict.
§4-§6 are contract-side cleanups that don't block daemon migration.
§7 is the structural piece and depends on §2 and §3. §10 depends on
§1 plus the `signal_cli!` macro landing.

The deferred parts (criome, arca, peer-lojix mesh) remain deferred
per `intent/deploy.nota` 2026-05-20T17:10:00Z.

## 5 · References

### Workspace authority

- `ESSENCE.md` §"Naming" — the two-rule pair (full English words +
  no ancestry).
- `INTENT.md` §"Two deploy stacks coexist" — production lojix-cli on
  `main` stays separate; lean rewrite lives on
  `horizon-leaner-shape`.
- `AGENTS.md` "Component triad" + "NOTA is the only argument
  language".
- `skills/component-triad.md` — the five invariants; the
  Component Operation → Component Command → Sema Classification
  three-layer rule.
- `skills/naming.md` §"Anti-pattern: prefixing names with their
  namespace or domain"; §"Anti-pattern: repeated category words
  across sibling names".
- `skills/reporting.md` — this report's shape.

### Intent records cited

- `intent/persona.nota` 2026-05-21T10:00:00Z (debug-the-debugger;
  generalised to lojix in §2.5).
- `intent/component-shape.nota`
  - 2026-05-18T22:15:57Z (owner contract is part of the triad)
  - 2026-05-19T01:25:00Z (configuration is always a Mutate)
  - 2026-05-19T01:30:00Z (policy/working state taxonomy;
    bootstrap-policy.nota)
  - 2026-05-19T19:30:00Z (public verbs are domain actions, not Sema)
  - 2026-05-20T02:00:00Z (Tap/Untap mandatory for persona components;
    non-persona small utilities don't declare an observable block;
    lojix sits between — see §2.5 designer lean)
  - 2026-05-20T12:11:26Z (signal types and signal tree vocabulary;
    "be very critical of signal types, names, and logic separation")
  - 2026-05-20T13:00:00Z (CLI two-socket dispatch is workspace-
    universal)
  - 2026-05-21T10:30:00Z (macros emit clean names; modules for
    disambiguation)
- `intent/signal.nota`
  - 2026-05-20T12:33:11Z (`ToSemaOperation`/`ToSemaOutcome` shape)
  - 2026-05-20T15:06:29+02:00 (all signal-executor code on current
    three-layer design)
  - 2026-05-20T17:10:00Z (lojix's lean-rewrite gate lifts; using
    landed signal/sema logic now)
- `intent/deploy.nota`
  - 2026-05-17T11:00:00Z (daemon-mesh deploy model; three deploy
    variables; daemon maintains believed topology)
  - 2026-05-17T13:30:00Z (lojix-daemon owns nix config;
    cluster signing keys)
  - 2026-05-17T15:30:00Z (criome-mediated authorization; daemon-to-
    daemon)
  - 2026-05-20T17:10:00Z (owner-signal-lojix not deferred; criome
    auth deferred; Build/Deploy/Activate/Rollback split direction)
- `intent/horizon.nota`
  - 2026-05-20T18:31:00Z (`online` drops; reachability is in
    lojix-daemon's believed topology — confirms §3.1 item 7)
- `intent/naming.nota`
  - 2026-05-19T14:40:38Z (ancestry-prefix correction — covers §2.7)
  - 2026-05-19T18:50:00Z (signal types over-declarate; flat schemas
    where they should tree — covers §2.4)

### Reference reports

- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  — consolidated current-foundation reference; the triad target shape
  used as the template for the audit. This report's structure mirrors
  the engine-manager triad audit template (since dropped) — §0
  TL;DR, §1 /257-finding-status, §2 new findings, §3 owner-signal
  proposal (the missing piece for lojix; the template's §3 covered
  spirit's case), §4 recommended next slice, §5 cross-
  cutting note, §6 references).
- `reports/designer/257-signal-contracts-names-and-shape-audit.md` —
  cross-contract audit (does NOT cover lojix; this report fills that
  gap).
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — signal-type naming and tree-shape design guideline.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — `signal_cli!` macro shape, referenced in §3.4 item 1 and §4
  step 10.
- `reports/system-assistant/28-lojix-vision-gap-audit.md` — the
  deployment-side companion to this audit; this report aligns with
  /28's Gap 1, Gap 2, Gap 3, Gap 4, Gap 5, Gap 6, Gap 8, Gap 9,
  Gap 10, Gap 12.
- `reports/system-assistant/29-lean-horizon-cluster-data-shape.md`
  — names lojix-daemon as the home for runtime reachability/
  believed-topology (per intent/horizon.nota 2026-05-20T18:31Z); the
  topology fields in §3.1 item 7 inherit from /29.
- `reports/system-specialist/154-lojix-signal-migration-vision-2026-05-20.md`
  — the audited vision this audit incorporates; §4 step 7 inherits
  /154's command sketch; §2.3's effect-actor preservation comes from
  /154 §"Important split".
- `reports/system-specialist/153-signal-refresh-144-system-impact.md`
  — the (now-resolved) lojix-pilot-gate; the gap-resolution at
  `intent/signal.nota` 2026-05-20T17:10:00Z lifted this.

### Triad source

- `lojix/horizon-leaner-shape/ARCHITECTURE.md` — daemon shape and
  invariants; §2 currently states the OLD contract surface.
- `lojix/horizon-leaner-shape/Cargo.toml` — dependency declaration
  showing `signal-core` (line 25), no `signal-frame`, no
  `signal-executor`.
- `lojix/horizon-leaner-shape/src/runtime.rs:201-364` — request
  dispatch path with stale variant names.
- `lojix/horizon-leaner-shape/src/socket.rs:9-12, 188-198, 287-308,
  401-418` — direct signal-core imports and variant-match path.
- `lojix/horizon-leaner-shape/src/client.rs:2, 28-95` — CLI client's
  signal-core dependency and one-socket dispatch.
- `signal-lojix/horizon-leaner-shape/src/lib.rs:641-680` — current
  contract channel declaration with contract-local verbs.
- `signal-lojix/horizon-leaner-shape/ARCHITECTURE.md:86-128` — stale
  channel-surface block needing rewrite.
- `lojix-cli/horizon-re-engineering/` — the legacy monolithic CLI
  (production stack), not part of the new triad.

## 6 · Open questions for psyche

Each question carries its own substance — no back-references to
sections. The user can answer without opening this report.

### 1. Should `signal-lojix` declare an `observable { … }` block?

**Background.** Persona components MUST declare an observable block
per `intent/component-shape.nota` 2026-05-20T02:00:00Z. Lojix is not
a `persona-*` component (it's deployment infrastructure). The intent
record says non-persona *"small utilities"* don't declare one — but
lojix is the opposite of small, with durable state, a working
contract, future peer-daemon connections, and a deployment-lifecycle
domain. The contract DOES have domain-shaped event streams
(`WatchDeployments`, `WatchCacheRetention`) — but those serve
deployment-domain queries, not the universal observer hook
`persona-introspect` will use.

**Designer lean: add the observable block on the working contract**
(not the policy contract). Reason: lojix daemons compose with
criome-daemon (and eventually peer lojix-daemons, arca-daemon);
universal cross-component introspection wants the same hook lojix
gives persona components. "Debug the debugger" generalises — a
component that observes deployment lifecycle but isn't itself
observable from above is a worse shape.

**The question:** confirm the lean, or rule lojix as a
non-persona utility with domain streams only and no universal
observer block?

### 2. Should `DeploymentRequest`/`Accepted`/`Rejected`/`RejectionReason` drop the `Deployment` prefix inside `signal-lojix`?

**Background.** The contract crate's domain is "lojix" (deploy
orchestration). Per `skills/naming.md`, the surrounding namespace
already supplies "deployment" context. Spirit precedent: `Entry`
inside `signal-persona-spirit`, not `IntentEntry`. Same rule applies
across the signal-* crates per
`intent/naming.nota` 2026-05-19T14:40:38Z.

But: the lojix contract is "Lojix" (the daemon name), not
"Deployment" (the domain word). There's a real semantic question of
whether the contract's domain word is "lojix" (the proper noun of
the daemon) or "deployment" (the substantive concept the contract
serves). If "deployment" IS the load-bearing concept, then
`DeploymentRequest` reads as descriptive, not ancestry-stuffing.
Compare: `signal-repository-ledger` chose `Receive`, `Observe`,
`Query` — the contract verbs — and the inner records use
`PushObservation`, not `RepositoryPushObservation`. By analogy,
lojix's verbs are `Deploy`, `Pin`, `Unpin`, `Retire`, `Query`, etc.
— so the inner records carrying their payloads should be
`Request`/`Accepted`/`Rejected`/`RejectionReason`, not
`DeploymentRequest`/`DeploymentAccepted`/etc.

**Designer lean: drop the prefix.**

**The question:** rule it.

### 3. Are `Pin`, `Unpin`, `Retire` payloads better as bare `GenerationId` or as the current single-field structs?

**Background.** Currently each is a one-field struct:

```rust
pub struct Pin { pub generation: GenerationId }
pub struct Unpin { pub generation: GenerationId }
pub struct Retire { pub generation: GenerationId }
```

And the channel has `operation Pin(Pin)`, `operation Unpin(Unpin)`,
`operation Retire(Retire)`. The wrapper struct is ceremony — the
variant name already names the verb; the payload is the noun.
Cleaner: `operation Pin(GenerationId)`, `operation Unpin(GenerationId)`,
`operation Retire(GenerationId)`.

**Designer lean: bare `GenerationId` payloads.**

**The question:** rule it, OR confirm there's a future field these
records carry that justifies the struct shape (audit trail metadata?
reason field? — none are present today).

### 4. Should `LojixDaemonConfiguration` shrink to startup-only bindings, with policy fields moving to owner-signal-lojix bootstrap?

**Background.** Currently `LojixDaemonConfiguration` (the typed
record the daemon reads from `nota-config` at startup) carries 9
fields, of which 5 (`horizon_configuration_source`, `peer_daemons`,
`operator_identity`, `owned_cluster`, plus the implicit "should
criome auth be enforced" stub) are POLICY under the two-state
taxonomy, not startup bindings. Per
`intent/component-shape.nota` 2026-05-19T01:30:00Z, policy
bootstraps from `bootstrap-policy.nota` and mutates through
owner-signal afterwards — it doesn't live in startup-time
configuration.

The cleaner split:
- `LojixDaemonConfiguration` keeps `daemon_socket_path` /
  `daemon_socket_mode` / `daemon_socket_group` /
  `policy_socket_path` / `policy_socket_mode` / `state_directory`
  / `gc_root_directory` — the things needed BEFORE the daemon can
  read its own database.
- The other fields move to `bootstrap-policy.nota` records, which
  the daemon reads once on first start through normal owner-signal
  command execution.

This is consistent with engine-manager (`SpawnEnvelope` is bind-
time only; policy lives elsewhere — though /258 §2.6 notes the
current engine-manager doesn't split this cleanly either).

**Designer lean: shrink LojixDaemonConfiguration to startup
bindings only.**

**The question:** confirm the split direction. If yes, the work
folds into §4 step 1 (creating owner-signal-lojix) and step 2
(daemon migration).

### 5. Should `signal-lojix` add the typed observation-record timestamps clients seem to want?

**Background.** The deployment observation records (`Submitted`,
`Building`, `Built`, `Failed`, etc., in
`signal-lojix/src/lib.rs:459-510`) carry no time fields. They're
ordered by their arrival in the subscription stream. For
single-subscriber consumption that works. But:

- replaying after disconnect-reconnect requires the subscriber to
  reconstruct timing from current time minus stream lag (or to be
  okay with un-timed observations);
- multi-subscriber debugging wants a single canonical "when did
  this happen on the daemon's clock" field;
- audit / forensic analysis wants per-record time stamps.

The spirit pilot daemon-stamps capture time
(`intent/persona.nota` 2026-05-20 21:53 Correction Maximum: *"The
usage of Spirit is not, we don't provide a timestamp for anything.
The timestamp is created by the daemon when it receives the
signal."*). Same pattern could apply here: daemon stamps each
observation with a `CaptureTime` field on emission.

`intent/persona.nota` 2026-05-20T18:44:49+02:00 says
seconds-precision is enough (no nanoseconds). So the field would be
something like `at: CaptureTime` where `CaptureTime` is a typed
two-positional-field (date + time) per
`intent/workspace.nota` 2026-05-19T18:30.

**Designer lean: daemon-stamp each observation with `CaptureTime`
when it emits.**

**The question:** is the lojix observation stream supposed to be
time-stamped, or is stream-ordering the source-of-truth?

This report retires when (a) `owner-signal-lojix` lands AND the
daemon resyncs onto current contract names AND the
`signal-core` → `signal-frame` daemon move lands AND the
signal-executor migration lands, OR (b) a successor audit
supersedes.
