# 19 — Deploy mesh + Arca substrate: integrated architecture

Date: 2026-05-17
Role: system-assistant
Scope: Build on SYS/18 (deploy mesh), absorb SYS/137 (system-specialist's
parallel reading), and integrate Arca as the content-addressed
substrate the user proposed. Identifies what closes and what stays open
once Arca is part of the picture. Pairs with SYS/20 (Arca-only deep
dive).

This report assumes SYS/18, SYS/137, and the existing arca repo
(`/git/github.com/LiGoldragon/arca`) as prior context. It does not
restate them in full.

---

## 0. What's new since SYS/18 / SYS/137

Three corrections from the user, plus one big architectural addition:

1. **Bootstrap is already solved.** The production `lojix-cli` stack
   is the bootstrap path. Until a node is on the lean rewrite, the old
   stack handles its first deploys. SYS/18 §7 / SYS/137 §"Bootstrap
   gap" are over-stated as open questions; they are closed by the
   "two stacks coexist" reality (`protocols/active-repositories.md`).
2. **`lojix-daemon` owns nix config.** One of the first things the
   daemon takes control of is the local `/etc/nix/nix.conf` (and the
   nix-daemon process). It can mutate config and restart nix-daemon
   whenever the deploy plan requires. This collapses several
   sub-questions in SYS/137 §"Binary cache trust is not free": the
   daemon can install/uninstall a per-deploy substituter, trust a
   key, and restart nix-daemon without operator intervention.
3. **Every node has a nix signing key, provisioned by clavifaber on
   first boot.** This is the trust root for binary-cache signatures
   between nodes. It closes most of SYS/137 §"Binary cache trust" gap
   #1: cache-capable daemons each have a stable public signing key;
   that key's identity is known to ClaviFaber/Horizon; targets trust
   `cluster signing keys` projection-wide.
4. **Arca becomes the content-addressed substrate.** Bulky and/or
   shared artifacts (deployment plans, projection inputs, possibly
   even nar closures) live in each daemon's local Arca store and
   travel between daemons via Arca-to-Arca content-addressed
   propagation. The `signal-lojix` wire carries small things
   (hashes, role assignments, observation events) and uses Arca
   hashes as references for the bulky things.

The substrate addition is the big one. It changes the answer to
SYS/137 §"Generated inputs may be the wrong abstraction" (options 1
vs 2 vs 3) — the answer is now **option 1.5**: every daemon fetches
from Arca by content-hash reference; what differs is whether the
projection-into-plan happens at the coordinator (one shared
artifact) or at each peer (each derives from shared refs). I think
the answer is "coordinator projects once into a single Arca-resident
plan artifact, every peer reads it by hash" — see §3 below.

---

## 1. Two-layer mental model

```
┌─────────────────────────────────────────────────────────────┐
│  signal-lojix mesh                                          │
│  "who does what when" — small messages, subscriptions,      │
│   role assignments, observation events                      │
│  Each node: lojix-daemon                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ references by Arca hash
┌─────────────────────────────────────────────────────────────┐
│  Arca substrate                                             │
│  "the bulky stuff" — plan artifacts, projection inputs,     │
│   possibly nar closures, anything ≥ small message size      │
│  Content-addressed by blake3; propagated peer-to-peer       │
│  Each node: arca-daemon (separate component)                │
└─────────────────────────────────────────────────────────────┘
```

**Key property:** the `signal-lojix` wire stays small and lean. Every
"the actual content" reference becomes an Arca hash. The Arca layer
handles the bulk transfer with its own backpressure, dedup, and
peer-to-peer fetch logic — independent of the deploy protocol.

This factors nicely:
- The deploy planner doesn't need to know how a bytestream gets to
  Tiger. It says "the plan is at Arca hash X; ask your Arca to fetch
  it from any peer."
- The Arca propagation logic doesn't need to know what the bytes mean.
  They're just trees with hashes.
- Trust composes: Arca hash IS content integrity (intrinsic);
  signal-lojix authorization (extrinsic, identity-based) gates *who
  can ask for what action*. The two trust planes don't intertwine.

---

## 2. What this changes in the deploy flow (vs SYS/18 §4)

Re-using the Uranus/Tiger/Balboa/Zeus example:

### Old flow (SYS/18, mesh without Arca)

Step 4 (Uranus issues role requests) inlined the plan in each
request. Bulky inputs (proposals, generated flake) would either be
re-fetched per-peer from git, or shipped inline, or one of SYS/137's
three options. Trust on bulk artifacts requires authorization on the
sender side.

### New flow (mesh with Arca substrate)

Steps reorganized; **only new or changed steps shown**:

**Step 3a (new): coordinator projects + writes plan to local Arca.**
Uranus's lojix-daemon projects horizon + cluster + viewpoint into a
`DeploymentPlanArtifact` (the deterministic, fully-resolved plan with
exact flake refs and exact target system+home derivations). Uranus's
lojix-daemon submits this artifact to its local arca-daemon, gets
back `ArcaHash(deploymentPlan)`.

**Step 4 (changed): signal-lojix requests carry hashes.**
- To Tiger: `BuildForJob { request_id, plan: ArcaHash(deploymentPlan), push_to: balboa_endpoint }`
- To Balboa: `ServeAsTransientCache { request_id, plan: ArcaHash(deploymentPlan), expect_pusher: tiger_identity }`
- To Zeus: `PullClosureAndActivate { request_id, plan: ArcaHash(deploymentPlan), pull_from: balboa_endpoint }`

Each request is small. Each peer's lojix-daemon, on receipt, asks
its local arca-daemon to fetch the plan by hash. arca-daemon
either has it locally or fetches it from a peer arca-daemon (Uranus
in this case, since Uranus is the one that just wrote it).

**Step 5–10 (mostly unchanged):** cache bringup, build, push, pull,
activate proceed as in SYS/18 / SYS/137. The bulky nar closures
themselves still flow via `nix copy --to`/SSH-store (per SYS/137's
final-closure-copy recommendation) — Arca does **not** replace
`/nix/store` in v1.

### What stays the same as SYS/137

- `StoreSource = BinaryCache | SshStore | LocalBuilderStore |
  TemporaryCacheSession` — Arca does not change this abstraction.
- `TopologyView` with `ConfiguredTopology` + `ObservedTopology` —
  Arca is orthogonal.
- `DeploymentPlanner` selects roles using topology — input set is
  unchanged; what changes is that the plan, once derived, materializes
  as an Arca artifact.
- All actor-plane decomposition (`DeploymentCoordinator`,
  `BuildRunner`, `ActivationRunner`, etc.) — Arca is a *substrate*,
  not an actor in the deploy plane.

---

## 3. Projection authority — closing SYS/137 gap #2

SYS/137 §"Generated inputs may be the wrong abstraction" laid out
three options. With Arca on the picture, the right answer is:

> **Coordinator projects once into a single Arca-resident plan
> artifact. Every peer reads it by hash and trusts the content
> intrinsically.**

Why this is the right answer:
- Determinism: every peer sees the same bytes, no chance of
  divergent local projection (e.g. one peer reads a slightly older
  goldragon state from its local cache).
- Trust: the Arca hash IS the artifact's integrity. No signature
  needed for *integrity*. (For *authorization* — "this plan was
  produced by an authorized operator" — see §5.)
- Cacheability: same artifact for multiple peers; Arca dedupes.
- Auditability: the deploy is durably named by its plan-artifact
  hash in every peer's ledger.

This is option 1 from SYS/137 plus option 2: refs are content-
addressed (option 1), but the artifact is the projection result, not
the inputs (option 2). The combination is what Arca enables.

---

## 4. Trust model — what closes, what's still open

The user's two new facts (nix-config-owned-by-daemon, signing-key-
per-node-from-clavifaber) close most of the cache-trust problem
from SYS/137 §"Binary cache trust is not free":

**Closed:**
- Cache-key trust root: clavifaber-provisioned cluster signing keys,
  projected through horizon, trusted by target.
- Per-deploy cache trust setup: lojix-daemon edits nix.conf to trust
  the specific cache for this deploy and restarts nix-daemon. No
  operator-side ssh-and-edit.
- Permanent caches: any cluster node can host a signed HTTP binary
  cache long-term, trusted by every other node via projection.
- Temporary caches: SYS/137's "SSH store source first, HTTP cache
  later" is even easier — SSH store needs only host-key trust, which
  is the same identity that's signing builds; nothing new.

**Still open (genuine trust questions, not closed by Arca):**
- **Authorization** (SYS/137 gap #9 / SYS/18 G2): "which daemon may
  ask Zeus to activate Zeus?" Content-hash integrity does not answer
  authorization. The lojix-daemon needs a per-request authority check
  that says "this signal-lojix request was sent by an entity allowed
  to ask Zeus to activate." Likely the operator-identity-signed
  envelope around the signal-lojix request. Needs design.
- **Per-cluster operator identity** — currently the daemon has an
  `operator_identity` field but no protocol for verifying it across
  daemons. Needs cryptographic shape (key pair? attestation chain?).
- **Cross-cluster authorization** — if a daemon in cluster A receives
  a request from a daemon in cluster B, what's the trust pathway?
  Defer to v2; v1 = single-cluster only.

So the trust model question is no longer "trust everything" — it's
narrowed to **authorization of signal-lojix request envelopes**.
That's a much smaller and more tractable design space.

---

## 5. Gap revisits from SYS/18 §11

With Arca + nix-config-ownership + clavifaber-signing-key on the table,
the SYS/18 gap list shrinks:

| SYS/18 gap | Status | Notes |
|---|---|---|
| G1 Bootstrap | **closed** | Production lojix-cli is the bootstrap path; cutover is per-node. |
| G2 Authentication / authorization | **partly closed** | Cache-key trust closed by clavifaber. Authorization of request envelopes is still open. |
| G3 Peer discovery | open | Static config for v1; gossip later. |
| G4 Believed topology | **closed (SYS/137)** | SYS/137 §"What topology belief should mean" has the right shape. |
| G5 Cost model | open | Defer to v2; v1 = metered/unmetered boolean. |
| G6 Stream-while-build granularity | open | Defer per SYS/137 §"Streaming closure movement" — final-closure copy first. |
| G7 Transient cache mechanism | **closed (SYS/137 + nix-config-ownership)** | SSH store source first; signed HTTP cache once daemon-owned nix.conf is in place. |
| G8 GC root lifetime across daemons | open | Needs explicit `DeploymentReleased { request_id }` wire signal. |
| G9 Failure-mode matrix | partly closed (SYS/137 §"Failure behavior") | Most cases covered; concurrent-deploy and network-partition mid-transfer still need explicit answers. |
| G10 Cancellation | open | Wire shape needed. |
| G11 Mid-flight plan mutation | **closed** | Plan is content-addressed in Arca; mid-flight changes mean new plan hash + new request. Immutable. |
| G12 Multi-cluster | open | v1 = single-cluster. |
| G13 Per-deploy observability scope | open | Per-phase events for default; per-derivation as opt-in. |
| G14 Caller-as-daemon vs thin-CLI | open | Still the second-biggest decision. |
| G15 Flake reference assembly | **closed** | Coordinator's lojix-daemon assembles, writes to Arca; targets read by hash. |
| G16 Concurrent deploys to same target | open | Per-target activation lock (SYS/137 §"Target daemon" state). |
| G17 Cross-cluster mesh | open | v1 = single-cluster. |
| G18 Idempotency | open | Add `idempotency_key` to `DeploymentSubmission`. |
| G19 Cache "ready" semantics | **closed (SYS/137)** | SYS/137's `CacheSessionAccepted { endpoint, public_key, lease }` is the right shape. |

**Remaining genuinely open**: G3 (peer discovery), G5 (cost), G8 (GC
roots), G9 (concurrent + partition), G10 (cancellation), G12 + G17
(multi-cluster), G13 (observability scope), G14 (caller shape), G16
(concurrent same-target), G18 (idempotency). Most of these are
either small (idempotency key), defer-to-v2 (cost, multi-cluster),
or "design the wire field properly" (cancellation, GC release).

The remaining big architectural question is **G14 (caller-as-daemon
vs thin-CLI)**.

---

## 6. The Arca-using parts of the deploy wire

Concrete additions to `signal-lojix` types implied by Arca-substrate:

```rust
// Existing types extended:
struct DeploymentSubmission {
    // ... existing fields ...
    idempotency_key: IdempotencyKey,  // new — G18
}

// New types:
struct DeploymentPlanArtifact {
    request_id: RequestIdentifier,
    builder: BuilderIdentity,
    cache: CacheSelection,
    target: TargetIdentity,
    fallback_cache_policy: FallbackCachePolicy,
    flake_reference: FlakeReference,       // exact, resolved
    expected_system_path: StorePath,       // for target verification
    expected_home_path: Option<StorePath>,
    activation_kind: ActivationKind,
    topology_snapshot: TopologySnapshot,   // why these roles chosen
    issued_by: OperatorIdentity,
    issued_at: Timestamp,
}

struct BuildForJob {
    request_id: RequestIdentifier,
    plan: ArcaHash,                       // points to DeploymentPlanArtifact
    push_to: StoreSourceEndpoint,
}

struct ServeAsTransientCache {
    request_id: RequestIdentifier,
    plan: ArcaHash,
    expect_publisher: DaemonIdentity,
    accepted_consumers: Vec<DaemonIdentity>,
    lease: LeaseDuration,
}

struct PullClosureAndActivate {
    request_id: RequestIdentifier,
    plan: ArcaHash,
    pull_from: StoreSourceEndpoint,
}

struct DeploymentReleased {
    request_id: RequestIdentifier,
}

enum StoreSourceEndpoint {
    SshStore(SshStoreUri),
    SignedBinaryCache(BinaryCacheUri, SigningKeyIdentity),
}
```

Each daemon receiving a request with `plan: ArcaHash` asks its
local arca-daemon for the content. If not present, arca-daemon
fetches from peers (which it can identify because Arca has its own
peer protocol — see SYS/20).

---

## 7. What the lojix-daemon's nix-config ownership looks like

The user's "lojix-daemon takes ownership of nix config" point
is worth specifying:

- `lojix-daemon` owns `/etc/nix/nix.conf` (or `/etc/nix/registry.json`
  where relevant). Operator does not hand-edit.
- A `NixConfigurationActor` (new daemon actor) manages mutations:
  add/remove substituter, add/remove trusted-public-key,
  add/remove builder, etc.
- Mutations are atomic (write-rename) + restart nix-daemon as part of
  the same operation.
- A lease/transaction model: "for the duration of `request_id`,
  trust cache C with key K" → on `DeploymentReleased`, undo.
- All mutations are recorded in the local sema-engine ledger; can be
  replayed/reconciled on daemon restart.

This is its own slice of work. It is *not* deploy-specific — many
other things will want lojix-daemon to mutate nix config (e.g.
adding the local Arca-as-store-source extension someday). Probably
worth landing as a standalone milestone before the mesh deploy
implementation depends on it.

---

## 8. Comparison to current state — updated

Three big changes from SYS/18 §8's comparison table:

- "Trust boundary" row: was "every daemon ↔ every daemon" (vague).
  Now: signal-lojix authorization envelope (open) + intrinsic
  Arca-hash content integrity (closed) + cluster signing keys via
  clavifaber (closed).
- New row "Bulk artifact propagation": today = ssh+rsync from
  operator; proposed = Arca peer-to-peer by content hash.
- New row "Plan determinism": today = whatever lojix-cli computes
  per-call; proposed = single Arca artifact per deploy, hash recorded
  in every peer's ledger.

---

## 9. Remaining big design decisions

In rough priority order:

1. **Authorization model for signal-lojix request envelopes** (G2
   residual). What signs them, what verifies them. Probable shape:
   each daemon has an identity key pair; clavifaber/horizon
   distributes the public keys; envelopes are signed; each daemon
   verifies on receipt + checks an authorization policy ("this
   identity may ask me to act in role X"). Needs designer work.
2. **Caller-as-daemon vs thin-CLI** (G14). Recommend thin-CLI on
   the operator's laptop talking to *one chosen cluster's daemon*;
   the cluster daemon is the coordinator. Means operator's laptop
   does not need a full lojix-daemon. Inversely: operator's laptop
   *might* want its own arca-daemon (so artifacts can flow to/from
   operator local storage). Two components are not equivalent.
3. **`NixConfigurationActor` slice as standalone milestone**
   (§7) — independent of mesh deploy, valuable on its own. Should
   probably land before mesh deploy starts depending on dynamic
   trust-key additions.
4. **Final-closure copy first** (SYS/137 R1) — preserve.
5. **idempotency key on `DeploymentSubmission`** (G18) — cheap; land
   before any consumer ships.
6. **`deploy.rs` split** (SYS/136 R1) **toward the new actor planes**
   (SYS/137 §"Implementation consequences"), not toward the current
   pipeline's smaller files.

---

## 10. What I want the user to read at the chat layer

The single highest-leverage finding: **Arca-as-substrate genuinely
simplifies the architecture.** The trust problem narrows from "every
daemon-daemon link" to "signal-lojix request authorization." Bulk
artifact distribution becomes a separable concern. Mid-flight plan
mutation question (G11) collapses entirely.

The single biggest remaining decision: **caller-as-daemon vs
thin-CLI (G14)**. Once that's chosen, the wire surface is
implementable.

The single biggest remaining design problem: **authorization
envelopes** — but it's now a bounded, named problem.

The standalone Arca design questions (path topology, hash length,
file-vs-directory naming, multi-store vs single-store) are in SYS/20.
The existing `arca` repo already has substantial architecture; the
user's verbal proposal is a *revamp*, not a from-scratch design.
SYS/20 lays out which existing arca properties to keep and which to
revise.
