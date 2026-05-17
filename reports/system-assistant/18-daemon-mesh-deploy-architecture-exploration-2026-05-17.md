# 18 — Daemon-mesh deploy architecture: exploration + gap audit

Date: 2026-05-17
Role: system-assistant
Scope: Architecture exploration of the user's proposal to replace
remote-orchestration deploys with a peer-daemon mesh. Identifies the
shapes, surfaces the gaps in the user's described intent that I
cannot close on my own, and recommends what to design next vs defer.

This is a **design-exploration** report, not a design decision. The
user asked for analysis + gaps; the decisions belong with the user
(and/or the designer lane).

---

## 0. Premise, restated

The user proposes that every node participating in a deploy runs its
own `lojix-daemon`. A deployment is then a **coordinated multi-daemon
operation** — caller, builder, cache, target each play a role over
the existing `signal-lojix` wire — rather than one orchestrator
SSH-ing into passive targets. The daemons hold durable
*believed-true* state about cluster shape, network topology, and
network cost, which informs routing decisions (which cache to use,
fallback to builder-as-cache, etc.).

The target node always deploys *itself* locally. This is what made
the painful "SSH-disconnect-survival" logic necessary in the
production stack; in the daemon-mesh model, that whole class of
problem disappears because the deploy actor is co-located with the
host it operates on.

---

## 1. What stays the same

The user's proposal does **not** require changing:

- The `signal-lojix` *contract shape* (signal frames, sema persistence,
  subscription model). The wire grows; it does not change kind.
- The `component-triad.md` invariant: daemon + thin CLI client +
  `signal-*` contract. Every node's daemon is a triad instance.
- The horizon-rs projection contract (`HorizonProposal` +
  `ClusterProposal` + `Viewpoint` → `view::Horizon`). Each daemon
  still projects to know its own view.
- The sema-engine durable ledger model. The deployment ledger
  becomes per-daemon, not global.

What *changes* is who-talks-to-whom and what extra state each daemon
carries.

---

## 2. What fundamentally shifts

Today's production stack and the smoke-built lean rewrite are both
**centralized-orchestrator** models: one process (lojix-cli or
lojix-daemon) holds the deploy plan, opens SSH connections, drives
`nix copy` from the local store to the target, runs `nixos-rebuild
switch` remotely. The target is a passive shell endpoint.

The proposed model is a **peer-daemon mesh**: each participating
node runs `lojix-daemon`; each speaks `signal-lojix` to its peers;
each owns its own role in the deploy. The caller's daemon **plans
and orchestrates** but does not execute remote effects — it asks
peer daemons to do their local thing.

This is a real distributed-systems jump (see §11 "Fundamental
concerns"). It is also where the existing `wire::PeerDaemonBinding`,
`wire::BuilderSelection`, and `daemon-side peer_daemons` fields are
already pointing — the seeds are on the wire, the architecture has
not yet committed to using them this way.

---

## 3. The four roles in a single deployment

| Role | Responsibility | Co-located with |
|---|---|---|
| **Caller** | Holds the intent. Plans roles. Receives progress. | Operator's machine or any daemon that can issue requests. |
| **Builder** | Runs `nix build`. Has the `nix-daemon`. Pushes realized derivations to the cache. | One node in the mesh. |
| **Cache** | Serves built derivations as a binary cache for the target to pull. | One node in the mesh (possibly the builder itself). |
| **Target** | Pulls the closure from the cache. Runs activation locally. | The node being deployed. Always present. |

Caller may equal builder may equal cache may equal target. In a
single-node deploy (laptop deploys itself), all four collapse to one.
In the user's worked example, all four are distinct nodes.

### Per-role wire surface (sketch)

| From caller, to ... | Request | New on wire? |
|---|---|---|
| builder daemon | `BuildForJob { plan, request_id }` | new |
| cache daemon | `ServeAsTransientCache { plan, request_id, builder_endpoint }` | new |
| target daemon | `PullClosureAndActivate { plan, request_id, cache_endpoint }` | new |
| any daemon | `SubscribeToDeployment { request_id }` | extension of existing subscription |
| any daemon | `CancelDeployment { request_id, scope }` | new |

Each daemon also pushes events back to subscribers:

`BuildStarted`, `DerivationRealized`, `CachePopulated{path}`,
`TargetPullStarted`, `TargetPullCompleted`, `ActivationStarted`,
`ActivationCompleted | ActivationFailed`, `DeploymentCancelled`.

These are extensions of the existing `DeploymentPhase` /
`DeploymentObservation` types in `signal-lojix`. They generalize
from "single daemon observes its own phases" to "any peer can
subscribe to any phase of any deploy by `request_id`."

---

## 4. Worked example — Uranus / Tiger / Balboa / Zeus

Caller: **Uranus**. Builder: **Tiger**. Intended cache: **Balboa**.
Target: **Zeus**. Caller-as-fallback-cache: forbidden by request
flag.

### Happy path

1. Operator runs `lojix deploy ...` on Uranus → Uranus's daemon
   receives `DeploymentSubmission`.
2. Uranus's daemon validates the plan: required roles assigned;
   topology says all four reachable; cost budget OK.
3. Uranus's daemon allocates `request_id` in its own sema ledger
   (durable; survives Uranus crash).
4. Uranus's daemon issues three parallel signals:
   - To Tiger: `BuildForJob { plan, request_id, push_to: balboa_endpoint }`
   - To Balboa: `ServeAsTransientCache { request_id, expect_pusher: tiger_identity }`
   - To Zeus: `PullClosureAndActivate { plan, request_id, pull_from: balboa_endpoint }`
5. Balboa spawns `nix-serve` (or equivalent), opens an
   authenticated endpoint scoped to `request_id`. Replies
   `CacheReady { endpoint, credentials }` to Uranus and Tiger.
6. Tiger starts `nix build`. As each derivation realizes, Tiger
   runs `nix copy --to ssh-ng://balboa-or-https-binary-cache
   /nix/store/<path>` for that derivation. Tiger emits
   `DerivationRealized { path }` events.
7. Balboa receives each path; emits `CachePopulated { path }`.
8. Zeus, listening for `CachePopulated`, starts pulling closures
   for each top-level output as they appear. Emits
   `TargetPullStarted` / `TargetPullCompleted` per path.
9. When Tiger emits `BuildCompleted`, Zeus knows the full closure
   is available; once Zeus's local pull completes, it emits
   `ActivationStarted` and runs `nixos-rebuild switch` against the
   pulled closure.
10. Zeus emits `ActivationCompleted` (or `ActivationFailed` + reason).
11. Uranus, subscribed throughout, persists every event. On
    `ActivationCompleted`, marks the deploy `Activated` in its
    ledger. Zeus marks its own ledger `Current`.

### Fallback: Balboa unreachable

- Tiger's initial probe to Balboa fails, **or** Uranus's
  `ServeAsTransientCache` to Balboa times out.
- Uranus detects (from either signal) that Balboa is out.
- Per `fallback_cache_policy` field in the plan: if builder-as-cache
  is allowed, Uranus re-issues `ServeAsTransientCache` to Tiger
  itself (Tiger now plays both builder and cache).
- Zeus receives an updated `PullClosureAndActivate.cache_endpoint`
  pointing at Tiger. (This implies plans are *mutable mid-flight* —
  see G9.)
- Build proceeds; cache is local to Tiger; Zeus pulls from Tiger.

### Fallback: forbidden

- If `fallback_cache_policy = forbid_builder` (because Tiger's
  compute is precious and shouldn't serve), Uranus aborts the
  deploy with `DeploymentRejected { reason: NoEligibleCache }`.

---

## 5. New daemon-side responsibilities

The current lojix-daemon (per SYS/136 audit) implements the
single-daemon path: receive submission → project → build → ledger →
GC roots. The proposed architecture adds:

### A. **Believed cluster topology** actor
Holds the daemon's view of "who is in my cluster, what roles do
they currently advertise, who is reachable as of when."
- Source of truth: still `goldragon/datom.nota` projected via
  `ClusterProposal`.
- *Liveness* layer on top: per-peer last-seen, last successful
  signal exchange, advertised capabilities.
- Updated by: peer signal exchanges, periodic heartbeats,
  explicit operator commands.

### B. **Believed network topology** actor
Holds the daemon's view of pairwise reachability + latency +
bandwidth between this daemon and each peer.
- Measured via: periodic probes, opportunistic measurement during
  real signal exchanges.
- Decay: measurements have a TTL; stale measurements are flagged.

### C. **Cost model** actor
Per-interface or per-route metadata: metered/unmetered, cost
units per GB, current monthly cap if any.
- Source: operator configuration on the local node.
- Used by: routing decisions when picking cache, when deciding
  whether to allow transitive routing through this node.

### D. **Deployment orchestrator** actor (caller-side)
Owns a deploy `request_id` from submission to completion.
Tracks per-role peer status, fans out role requests, listens for
events, applies fallback policy, persists in ledger.

### E. **Transient cache server** actor (cache-role only)
Spawns / supervises an `nix-serve` (or equivalent) bound to a
per-job credential. Tracks GC roots for received paths. Tears
down when the deploy releases.

### F. **Activation runner** actor (target-role only)
Receives `PullClosureAndActivate`; pulls closure from cache;
runs `nixos-rebuild switch` (or home-manager equivalent) against
the pulled top-level output. Reports phase events.

### G. **Inter-daemon subscription bridge**
Forwards local `DeploymentObservation` events to subscribed peer
daemons. Currently subscriptions are local-only; peer
subscriptions need authenticated, network-aware delivery.

---

## 6. State shapes (sketch — for the designer to refine)

```rust
struct PeerLiveness {
    peer: PeerDaemonBinding,
    last_seen: Instant,
    last_round_trip_microseconds: Option<u64>,
    last_bandwidth_bytes_per_second: Option<u64>,
    advertised_roles: BTreeSet<DaemonRole>,
}

enum DaemonRole {
    EligibleBuilder { capacity: BuildCapacity },
    EligibleTransientCache { storage_budget: ByteBudget },
    EligibleTarget,
}

struct NetworkCost {
    interface: InterfaceName,
    metered: bool,
    cost_units_per_gigabyte: Option<u32>,
    monthly_cap_gigabytes: Option<u32>,
    current_month_consumed_gigabytes: u32,
}

struct DeploymentPlan {
    request_id: RequestIdentifier,
    builder: BuilderSelection,         // existing wire type
    cache: CacheSelection,             // new — mirrors builder
    target: TargetIdentity,
    caller: CallerIdentity,
    fallback_cache_policy: FallbackCachePolicy,
    deployment_payload: DeploymentSubmission,  // existing
}

enum CacheSelection {
    SameAsBuilder,
    NamedCache(NodeName),
    DispatcherChoosesCache,
}

enum FallbackCachePolicy {
    AllowBuilderAsFallback,
    ForbidBuilderAsFallback,  // builder compute too precious
    OnlyExplicitCache,        // strict; fail if intended cache down
}
```

These mirror the *existing* `wire::BuilderSelection` /
`wire::PeerDaemonBinding` style; the cache vocabulary is the
genuinely-new addition.

---

## 7. Bootstrap: the structural exception

**The whole model presupposes every participating node already runs
`lojix-daemon`.** This breaks for:

- A brand-new node being deployed for the first time (e.g. fresh
  Raspberry Pi being imaged).
- A node coming back from disaster recovery where the daemon's
  sema-engine state is gone.
- A node that does not run CriomOS (e.g. an external builder VM
  that just runs `nix-daemon` and SSH).

The user's proposal does not address bootstrap. Two coherent
options exist:

1. **Two-mode CLI**: keep a thin "ssh-and-rsync" bootstrap mode in
   the CLI for first-deploy / re-image; once the daemon is on the
   node, all subsequent deploys go through the mesh.
2. **Pre-baked daemon**: every CriomOS image ships with the daemon
   pre-installed and auto-starting; first boot already has a
   functioning daemon ready to receive deploys. Bootstrap is then
   "physically flash an image with the daemon baked in," which is
   already a manual step today.

Option 2 is cleaner and aligns with the lean-rewrite shape, but
requires that the **initial image** is itself buildable without a
mesh deploy — chicken-and-egg via the operator's local `nix build`
+ `dd` flow. Option 1 keeps the legacy path alive indefinitely.

This is a real design fork; it needs a user decision.

---

## 8. Comparison to current state

| Concern | Today (production: lojix-cli) | Today (smoke-built lojix daemon) | Proposed (daemon mesh) |
|---|---|---|---|
| Where deploy state lives | Ephemeral in lojix-cli process | sema-engine on the daemon's node (single node) | sema-engine on **each** participating daemon |
| Activation transport | SSH from operator → target | SSH from daemon's host → target | Local subprocess on target |
| SSH-disconnect handling | Custom retry/survival logic in lojix-cli | (Same; smoke-built but not deployed) | **Not needed** — activation is local |
| Build placement | Local to lojix-cli or `nix.builders` setting | Same | Routing decision per-deploy via plan |
| Cache routing | Static (binary caches in nix.conf) | Same | Per-deploy plan; transient ephemeral cache |
| Multi-deploy observability | Tail logs | Subscribe to single-daemon events | Subscribe to a `request_id` aggregated from N daemons |
| Daemon ubiquity needed? | No (only operator's machine has lojix-cli) | No (one daemon orchestrates) | **Yes — every participating node** |
| Trust boundary | Operator → cluster (SSH keys) | Operator → daemon → cluster | **Every daemon ↔ every daemon** |

The two rightmost columns are the headline trade-off: the mesh
eliminates an entire class of bugs (SSH disconnect, partial-deploy
ambiguity, lossy progress events) at the cost of requiring
daemon-on-every-node and an explicit inter-daemon trust model.

---

## 9. Comparison to prior art (brief)

- **`deploy-rs`**: single-shot Nix-based remote activation with
  rollback guard. Solves activation + rollback, not cache routing,
  not durable state, not multi-node coordination.
- **`colmena`**: multi-target deploys with parallelism + optional
  remote-builder. Closer to the proposal but still
  operator-orchestrated, not daemon-mesh.
- **`morph`**: Tweag's evolution of NixOps; richer cluster model;
  still operator-driven.
- **Nix native distributed builds** (`builders = ssh://...` in
  `nix.conf`): solves build placement but nothing else.

**What the proposed model adds over all of these:** durable
per-deploy state on every participating node (via sema-engine),
peer-daemon-as-permanent-component (so deploy is not a one-shot
operator invocation), and cost-aware routing.

That's a real differentiator — but it is also a much larger
implementation surface than any of the above.

---

## 10. Fundamental concerns

These are not "gaps in intent" — they are structural consequences
of the proposed architecture that the user should weigh before
committing.

### C1. Distributed-systems jump
Today: 1 daemon. Tomorrow: N daemons coordinating partial state.
Brings: partition tolerance, eventual consistency, distributed
debugging. Worth being eyes-open about.

### C2. Believed-topology coherence
Each daemon's view of cluster + network state can drift relative
to peers. The "Tiger has Balboa as a reachable peer" view on
Uranus may not match Tiger's actual ability to reach Balboa right
now. This is solved (in the user's narrative) by probing during
the deploy — fine for v1 — but the long-run picture needs an
explicit consistency model (gossip? Tailnet-derived?).

### C3. Trust model expansion
Today's trust is operator→cluster (one SSH-key direction).
Proposed: every daemon must authenticate every other daemon and
authorize requests (who can ask whom to build what for which
target). This is a non-trivial design problem — the
`operator_identity` field is a seed but not a solution.

### C4. Daemon ubiquity as hard constraint
Some nodes you may want to deploy *to* are not lojix-running
hosts (external builder farm, ephemeral VM, vendor-supplied
appliance). The mesh model excludes those by construction.

### C5. Mesh complexity is "off" by default in single-node case
The single-node deploy (laptop → laptop) should not pay the cost
of mesh coordination. The implementation needs a fast path where
the mesh collapses; otherwise the simple case is over-engineered.

### C6. Operator-machine status
Is the operator's machine a mesh participant ("operator daemon")
or external (thin CLI talks to one cluster's daemon over the
network)? This is a real fork: the first is symmetric and clean
but adds a daemon to every operator laptop; the second is
asymmetric but simpler.

---

## 11. Gaps in intent I cannot close

The user's narrative is rich but leaves these specific decisions
unmade. Each needs a user or designer answer before this becomes
implementable.

### G1. Bootstrap — see §7. **Pick option 1 or option 2.**

### G2. Authentication / authorization between daemons
- Trust root? (Tailnet identity? Per-cluster CA? mTLS?
  operator-signed attestation?)
- Who can ask whom to deploy what? Per-cluster-operator
  authorization? Per-target ACL?
- Does the cache-role peer accept any caller's request, or only
  caller-attested ones?

### G3. Peer discovery
- How does a daemon populate `peer_daemons` at runtime?
  Configuration-time list? Tailnet-MagicDNS lookup? Goldragon
  projection? Dynamic gossip?
- What happens when the cluster grows / shrinks?

### G4. "Believed topology" — concrete state model
- What exact data structures? (See §6 sketch — needs designer
  ratification.)
- Update mechanism: push (heartbeats), pull (on-demand probe),
  lazy (measure during real deploy), or all three?
- Persistence in sema-engine or in-memory only?
- Decay: TTL on measurements; what happens past TTL?
- Conflict: two daemons disagree about a peer's status — what
  resolution rule?

### G5. Cost model — concrete shape
- Cost declared where? Per-interface config? Tailnet ACL? Wire?
- Cost composed how across multi-hop paths?
- Multi-objective optimization (cost + latency + bandwidth) or
  cost-only? **This is a big design subspace; I would defer it
  to v2 and ship v1 with cost as a single "metered/unmetered"
  boolean.**

### G6. "Stream-while-build" granularity
The user said "as the cache fills up." Concretely:
- Per-derivation? (Nix realizes per-derivation; this is the
  natural granularity.)
- Per-top-level-output? (Coarser; simpler.)
- Per-byte-stream? (Doesn't match Nix's atomicity model;
  reject.)
- **Recommend per-derivation.**

### G7. Transient cache concrete mechanism
- Backed by `nix-serve` over HTTPS? (Standard, but needs cert.)
- Backed by `ssh-ng://` from target to cache? (Reuses SSH;
  ironic given goal is to remove SSH from the activation path.)
- Custom signal-lojix bytestream subscription? (Tightest fit but
  largest new surface.)
- **Likely answer: `ssh-ng://` for v1, custom bytestream later.**
- Auth on the endpoint: per-job credential issued by cache, or
  caller-attested?
- Resource bounds: what if the closure is larger than cache's
  free space? Pre-check or fail mid-transfer?

### G8. GC root lifetime across daemons
- Builder pins build outputs while building. When does it let go?
- Cache pins received outputs while serving. When does it let go?
- Target pins activated outputs (already today). Stable.
- The "let go" event needs a wire signal: `DeploymentReleased
  { request_id }`. Who issues it — caller on success? Caller on
  observed activation? Cache on target-pull-complete?

### G9. Failure-mode matrix
The narrative covers happy-path + cache-unavailable. Needs
explicit answers for:
- Caller goes offline mid-deploy (does deploy continue? events
  buffer? caller re-subscribes on reconnect?).
- Builder fails partway (abort? partial-resume?).
- Cache fails partway (dynamic fallback to builder, or fail?).
- Target activation fails (rollback who triggers? caller?
  target?).
- Network partition between builder and cache mid-transfer.
- Each needs a documented expected behavior.

### G10. Cancellation
- `CancelDeployment { request_id, scope }` — what is `scope`?
- Pre-build cancel vs mid-build vs pre-activate vs mid-activate.
- Activation is typically uncancellable once started; needs to
  be reflected in the wire.

### G11. Mid-flight plan mutation
Cache fallback (Balboa down → Tiger doubles as cache) implies
the plan changes mid-flight. Wire question:
- Is the plan immutable per `request_id`, with the orchestrator
  cancelling+resubmitting under a new id?
- Or is there a `PlanAmendment { request_id, ... }` signal that
  participating peers must accept?
- **Immutable + resubmit is simpler; mid-flight amendment is
  more elegant but harder.**

### G12. Multi-cluster boundary
- Can a node in cluster A act as cache for a deploy in cluster B?
- If yes: cross-cluster trust required. If no: deploy plans are
  single-cluster-only and the wire should enforce that.

### G13. Per-deploy observability scope
- Per-derivation events (could be many tens of thousands for a
  full system).
- Per-phase events (coarse; cheap).
- Operator's CLI subscription: which level by default?

### G14. Caller-as-operator-machine vs caller-as-cluster-node
- Operator's laptop runs a daemon? (Symmetric; clean.)
- Or operator's laptop has only thin CLI that talks to *some*
  cluster's daemon over the network? (Asymmetric; simpler.)
- **This is C6 restated as a wire-shape question.**

### G15. Activation primitive — flake reference assembly
- The activation command needs a flake reference. Today
  lojix-cli assembles it from cluster proposals + horizon
  projection.
- In the mesh model: who assembles the flake reference?
  Caller's daemon (knows operator intent) or target's daemon
  (knows local context)?
- **Likely caller's daemon assembles, passes as text in the
  plan, target validates against its own projection before
  running.** Needs ratification.

### G16. Concurrent deploys to same target
- Two deploys to Zeus arrive simultaneously. Queue? Reject?
  Pre-empt? FIFO with explicit cancellation needed?
- Today's `deployment_id` allocation seems FIFO-with-rejection;
  needs explicit wire shape.

### G17. Distributed deployment-trace reconstruction
- The deploy is now distributed across N sema-engine ledgers.
- Caller has the orchestrator-side ledger; each peer has its
  role-side ledger.
- For post-mortem: how does an operator reconstruct a full
  trace? Caller aggregates as it goes? Per-peer query+merge
  after the fact?
- **Probably: caller aggregates as it goes (subscriptions
  persist events); per-peer ledger is local audit only.**

### G18. Idempotency
- Caller retries the same submission (network flake). Does the
  daemon detect "this is the same deploy" via a
  caller-supplied idempotency key? Or allocate a fresh
  `request_id` and dedupe later?
- Today's `wire::DeploymentSubmission` does not have an
  idempotency key field. **Add one before this gets harder.**

### G19. What does "ready" mean for the cache?
- "`CacheReady` reply" needs precise meaning: server bound +
  listening, or server bound + advertised + reachable from
  target?
- The latter is what the deploy actually needs but requires
  cache to probe target (a round trip).

---

## 12. Recommendations

### Do soon (foundation work compatible with either v1 or v2 of the mesh)

1. **Add `idempotency_key` to `wire::DeploymentSubmission`** before
   any consumer ships. Cheap; unblocks G18 forever.
2. **Add `request_id` to every existing deploy event.** Already
   close to true today; ensure it's universal.
3. **Land the `deploy.rs` split** per SYS/136 R1; the mesh
   orchestrator wants the existing pieces as named modules
   regardless of whether mesh ships.
4. **Decide bootstrap discipline (G1, option 1 or 2).** Affects
   whether legacy CLI path stays alive.

### Designer-lane decisions to make before implementation

1. **Trust model (G2)** — biggest single open question. Cannot
   ship without this.
2. **Caller-as-daemon vs caller-as-thin-CLI (G14/C6).** Shapes
   the whole client surface.
3. **Peer discovery (G3)** — picks gossip vs static vs
   projection-derived.
4. **Believed-topology persistence model (G4).**

### Defer to v2

1. **Cost-aware routing (G5).** Ship v1 with cost as
   metered/unmetered boolean; full cost optimization is a
   research-grade subspace.
2. **Mid-flight plan amendment (G11).** Ship v1 with
   immutable-plan + resubmit-on-failure.
3. **Cross-cluster mesh (G12).** Single-cluster only in v1;
   wire schema can reserve cross-cluster fields for v2.
4. **Dynamic peer discovery (G3 advanced form).** Ship v1 with
   static `peer_daemons` config; gossip later.

### Do not build

1. **A per-deploy distributed consensus protocol.** The user
   does not need linearizability across daemons; eventually
   consistent + caller-as-aggregator is enough.
2. **A custom transport.** Reuse `signal-lojix` over
   Tailnet/mTLS; do not reinvent transport.
3. **Cache as a long-running shared resource.** The "transient,
   per-`request_id`" framing in the user's narrative is right;
   long-running cluster-wide binary caches are a separate
   concern (and one Nix already solves).

---

## 13. Open question for the user

The proposal is coherent and the trade-off is real (eliminate
disconnect-survival complexity at the cost of every node running
a daemon + an inter-daemon trust model).

The single biggest decision blocker is **trust model (G2)**. Until
that is named, the mesh-wire types cannot be defined precisely
enough to implement.

**Concretely: would you like the designer lane to take a first
pass at the trust model, or would you like to sketch it yourself
before that?** Either path is fine; nothing else can move until
that question is answered.

The second-biggest blocker is **G14 (caller-as-daemon vs
caller-as-thin-CLI)**, since it shapes the operator-machine
software surface. Both are defensible. Lean: thin-CLI on
operator's laptop talking to one chosen cluster-daemon, because
the operator laptop is already external to the cluster in most
mental models.

Everything else in §11 is a real but bounded gap, addressable
once those two are settled.
