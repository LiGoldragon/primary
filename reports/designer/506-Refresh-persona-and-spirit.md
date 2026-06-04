---
title: 506 — Refresh — persona engine, spirit component, interfaces, cutover
role: designer
variant: Refresh
date: 2026-06-04
topics: [persona-engine, component-triad, developed-interfaces, introspect, contract-repo-pipeline, spirit-topic-discovery, intent-maintenance-algorithms, schema-stack, cutover]
description: |
  Agglomerated refresh of the June-2 design cluster: developed schema
  interfaces (persona / orchestrate / introspect vocabularies), the
  introspect component design, spirit intent-maintenance algorithm
  proposals + psyche answers, the spirit topic-discovery feature design,
  and the contract-repo fork pipeline. Carries the still-live substance
  the current persona-engine reports (498/499) do not hold: the developed
  per-component vocabularies, the topic-discovery hybrid, and the
  cross-schema-import fork mechanism. Records what the NexusWork/NexusAction
  era and the live introspect repo superseded since June 2.
---

# 506 — Refresh — persona engine, spirit component, interfaces, cutover

This refresh merges five June-2 design reports (468, 469, 473, 474, 475)
into one canonical surface. The current persona-engine reports
`498-persona-engine-state` and `499-Psyche-persona-engine-state-and-vision`
carry the live engine map, the cutover staging, the schema-stack pipeline,
and the corrections the psyche owes — this refresh does NOT repeat those.
It holds the parts of the cluster they do not: the developed per-component
interface vocabularies, the introspect design, the intent-maintenance
algorithm answers, the topic-discovery feature design, and the
contract-repo fork mechanism.

## Era boundary — what June-2 framing the current stack superseded

Two supersessions reframe how the June-2 schema sketches read today. The
sketches are preserved below for their vocabulary, not their plane shape.

- **NexusInput/NexusOutput symmetric pairs → NexusWork/NexusAction +
  Continue.** The June-2 sketches (468, 469) drew Nexus as a symmetric
  `NexusInput`/`NexusOutput` pair with side-channel variants `Stash` /
  `Cascade` / `Preempt` / `Fanout` on the output side. Spirit 1486
  (Decision Maximum, 2026-06-03) landed the asymmetric form: `NexusWork`
  is the fact stream Nexus decides *from*; `NexusAction` is the command
  stream it emits *next* (`ReplyToSignal`, `CommandSemaWrite`,
  `CommandSemaRead`, `CommandEffect`, `Continue`). The old side-channel
  variants are now `CommandEffect(Effect)` with per-component declared
  effects; `Stash` is the first universal effect. `Continue(NexusWork)` is
  in-process typed recursion. The canonical mechanism lives in
  `skills/component-triad.md` §"Nexus mechanism substrate". Read the
  per-component matrices below as *the decisions Nexus makes*, not as a
  literal two-root plane shape.

- **The trace-ingest introspect (469) → the live observation-plane
  introspect.** Report 469 designed introspect as a push trace-sink:
  components push name-only `TraceEvent` frames over
  `signal-introspect::IngestTraceEvent`, and Nexus routes each by policy
  (Keep / Drop / Summarize / Fanout). The repository that actually shipped
  (`/git/.../introspect`, per `protocols/active-repositories.md`) took a
  different shape: introspect is a supervised inspection plane that opens
  Signal *subscriptions* to peer component observation streams
  (`signal-router`, `signal-persona-*`), fans in typed observation records,
  and projects NOTA only at the human/agent edge. The 469 push-routing
  design is design history; the live constraints (push subscription not
  poll; NOTA only at the edge; never open a peer redb) are in
  `introspect/ARCHITECTURE.md` §4 already. What 469 still contributes:
  introspect as the canonical cross-component witness plane, and the
  Configure-as-policy and Layer-2-witness framings (below).

## 1 — Developed per-component interface vocabularies

The June-2 directive (Spirit 1395, developed interfaces) drove three
schema sketches beyond toy one-variant planes. Their value now is the
*vocabulary* — the operation roots and the Nexus decisions each domain
demands — which seeds the eventual schema for each component when its
slice opens. The plane shape is superseded (read via NexusWork/NexusAction
per the era note above).

### Spirit pilot — the proven shape, expanded

The spirit pilot is the one component that proves the schema-emitted triad
(per 498/499). Its developed Signal vocabulary, beyond the shipped
`Record` / `Observe` / `Lookup` / `Count` / `Remove`:

- `Update RecordRevision` — append-vs-mutate routing: a certainty-only
  delta lowers to an in-place sema update; a description/topics delta
  lowers to a full-entry replace; zero-magnitude collisions reject.
- `Subscribe Subscription` — install a filter in the mail ledger, return a
  slim handle; subsequent sema writes consult subscription filters.
- The read interface splits `Observe` (filter-driven scan) / `Lookup`
  (handle-driven point read) / `Count` (aggregate) / `Summarize` (digest
  with topic + kind histograms). This split is now a workspace rule —
  `skills/component-triad.md` §"Interface roots are enums with more than
  one variant" names the four-variant `SemaReadInput` as the canonical
  interface-completeness example.

The substantive Nexus decisions: inline-vs-stash on `Observe` (count probe
decides whether records inline via the `Stash` effect or return a handle);
cache-vs-durable on `Lookup`; append-vs-mutate routing on `Update`;
subscription-install on `Subscribe`.

### Persona component — identity / capability / authorization vocabulary

Beyond persona-spirit's intent-capture lane, the broader persona surface
arbitrates identity, profile, capability, and authorization. Eight Signal
operations: `Lookup` / `Register` / `Assert` / `Revise` /
`GrantCapability` / `RevokeCapability` / `Authorize` / `Subscribe`. The
durable nouns the vocabulary needs:

- `PersonaRecord { Identifier kind profile }` with `PersonaKind [Human
  Agent Service System]`, `TrustLevel [Unverified Provisional Verified
  Owner]`, `HarnessKind [Codex Claude Pi Browser Unknown]`.
- `CapabilityRecord { Identifier scope kind grantee expiration }` with
  `CapabilityKind [Read Write Authorize Owner]` as a subordination ladder.
- `AuthorizationVerdict [Permitted Denied Stale]`.

The substantive Nexus decisions cluster in three concerns: **trust-level
arbitration** (parent-trust clamp on `Register`; trust-downgrade cascade on
`Revise`), **capability-scope subordination** (kind-ordering check on
`GrantCapability`; transitive cascading revocation on `RevokeCapability`),
and **freshness-vs-cache** (cached verdict on `Authorize`/`Lookup`). The
cascading revocation is a `CommandEffect` — a typed fan-out across the grant
tree, not implementation-code smuggled into Nexus.

The owner (meta-signal) surface carries policy: capability-template catalog,
identity-provider configuration, trust-escalation gates
(`EvidenceRequirement [SignedAssertion HumanReview QuorumApproval]`).

### Orchestrate component — lane-coordination vocabulary

The orchestrate component replaces the `tools/orchestrate` shell helper +
`<lane>.lock` files with a typed daemon. Eight Signal operations: `Claim` /
`Release` / `Handoff` / `Query` / `Wait` / `Subscribe` / `Submit` /
`Snapshot`. It carries the richest decision surface of the three because
lane coordination is fundamentally resource arbitration. The central
decision — *conflict-vs-grant-vs-queue-vs-preempt* on `Claim` — branches on
`WaitBehavior [RejectOnConflict QueueAndWait QueueWithTimeout
PreemptIfLower]` and `Priority [Background Normal Elevated Urgent]`:

- no scope overlap → record the claim;
- overlap + `RejectOnConflict` → return the conflicting holders;
- overlap + `QueueAndWait` → enqueue a wait record, return queued receipt;
- overlap + `PreemptIfLower` and higher incoming priority → emit a preempt
  effect; displaced holder gets a release ack, requester gets the grant.

Other decisions: wait-queue dispatch on `Release` (promote head-of-queue
atomically; receipt names `nextClaimant`); handoff atomicity (source holds
the scopes AND target has no conflicting holds outside the source set);
projection-cost routing on `Query`; read-concurrency tier on `Snapshot`.
The owner surface carries the lane catalog (`LaneAuthority [Structural
Support]`), priority/preemption rules, and timeout policy.

This vocabulary is the prototype resource-arbitration shape every future
arbitration component inherits. It stays a design sketch until the spirit
pilot delivers concrete interface-honesty witnesses to copy and the
psyche opens the orchestrate slice (orchestrate today is still the live
shell-helper substrate).

### Cross-component pattern findings (still live)

Three patterns held across all four sketches and are now workspace rules,
already manifested in `skills/component-triad.md`:

- **Every component grows a `Subscribe` variant** — push-not-pull is
  structural (`skills/push-not-pull.md`).
- **The read interface splits Observe / Lookup / Count / (+ Summarize)** —
  the multi-variant interface-completeness rule.
- **Side-channel decisions are typed** — what June-2 called the
  side-channel `NexusOutput` variant (Stash / Cascade / Preempt / Fanout)
  is now `CommandEffect(Effect)` with per-component declared effects.

One open framing the current skill does not state as a heuristic, worth
carrying: in a Nexus that earns its keep, the count of distinct effects +
sema-command kinds it emits exceeds the count of bare sema-write variants —
because Nexus emits effects (cascade, stash, preempt, fanout) in addition
to writes. Equal-or-fewer suggests Nexus is a generated projection rather
than a decision center. Carry as a review lens, not yet a ratified rule.

## 2 — Introspect — the cross-component witness plane

Per Spirit 1398, introspect is the workspace's cross-component
inspection/witness plane (the name drops the legacy `persona-` prefix). The
live repo realizes the *subscription* shape (subscribe to peer observation
streams; fan in typed records; project NOTA only at the edge). The 469
design contributes three framings that remain load-bearing regardless of
the ingest mechanism:

- **Introspect is the canonical Layer-2 witness store.** Spirit 1349-1350
  named the testing-build logging socket as the workspace runtime-witness
  substrate; introspect is the component that materializes it. Tests query
  introspect to assert architectural-crossing claims; the CLI renders
  introspect query results.
- **Introspect does not render, analyze, or interpret payloads.** Rendering
  is the CLI's job (NOTA only at the edge, already a repo constraint);
  pattern detection is an upstream consumer's concern; payload follow-up to
  a name-only trace event is a separate Signal call against the originating
  component using the event's origin identifier (Spirit 1336). Introspect's
  schema never knows another component's schema.
- **Policy is a sema-stored typed record consulted at runtime, never a
  hardcoded constant.** Whatever disposition logic introspect applies
  (keep / drop / summarize / fan-out, or subscribe-filter matching) reads
  the policy from sema; peers configure within bounds the owner sets via
  meta-signal. This is the *Configure-as-policy* pattern: a component that
  carries policy declares a `Configure<Domain>Policy` ordinary operation
  whose authority is bounded by a corresponding meta-signal surface.

The 469 push-routing decision (Keep / Drop / Summarize / Fanout per matched
policy rule) is preserved as design history — if introspect ever grows a
direct trace-ingest path alongside the subscription path, that decision
matrix is the starting design. It is not the live shape.

## 3 — Intent-maintenance algorithms — proposals and psyche answers

The June-2 multi-agent session produced ~12 Spirit duplicates over three
hours; the lesson was that discipline-statements alone do not survive
multi-agent forwarded-prompt pressure — the workspace needs algorithms. The
psyche answered four questions; the live discipline now lives in
`skills/intent-log.md` and `skills/intent-maintenance.md`. Recorded
answers (2026-06-02):

- **Query-before-capture** (Algorithm 1): adopted, **forwarded-prompt scope
  only**. When capturing on a prompt addressed to another agent, query
  recent records on the substance topics BEFORE recording, then CONFIRM /
  GAP-FILL / NEW. Direct-prompt captures do not pay the latency.
- **Supersede operation** (Algorithm 3): **not adopted**. `Remove` +
  git-history lineage stays canonical; no new `Supersede` op preserving a
  superseded-by field. (Same answer governs topic deprecation and record
  reframing — lineage lives in records + git, not a Spirit-native field.)
- **Magnitude calibration rubric** (Algorithm 4): **not adopted**. Agent
  judgment stays; no calibration table in `skills/intent-log.md`.
- **Capture cadence** (Algorithm 5): the eager-Maximum / recurrence-gated-
  Medium pattern — capture Maximum/High eagerly; capture Medium when the
  substance appears in two contexts (once is speculation, twice is
  direction); Low/below only when explicitly named durable.
- **Dedup detection heuristic** (Algorithm 2): the maintenance sweep flags
  near-duplicate pairs (within N record-ids, ≥50% topic overlap, matching
  Kind, magnitude within one step) and surfaces them for confirmation;
  earliest capture wins by default. This is the operational form of the
  Spirit-capture-sweep step in `skills/context-maintenance.md` §"Method".
- **Topic vocabulary** (Question 4): the psyche redirected past both
  offered options (curated list vs agent-discovers) to a third — a
  cached-value discovery feature in Spirit itself. That feature design is
  §4 below.

## 4 — Spirit topic-discovery feature (the cached-value answer)

The psyche's Question-4 redirect asked for [a feature to spirit to make
those discoverable with a cached-value algorithm — something smart and
clever to use nowadays, there must be libraries for this kind of thing]
(2026-06-02). The design answer is a three-layer hybrid, each layer
precomputed and cached, each query a cache read plus a small ranking pass.

### The three layers and their library picks

- **Frecency** (the "what is active now" layer) — a Firefox-style
  frequency-times-recency counter with exponential decay. `score(now) =
  stored_score * 2^(-(now - last_use_time) / half_life)`; decay computed
  lazily at read time, no background sweep. In-house ~100 lines; no
  dependency. Half-life is meta-signal policy (default 30 days).
- **Co-occurrence graph** (the "what appears together" + synonym-cluster
  layer) — topics are nodes, co-appearance counts are edges, stored as
  canonical-ordered pairs. One-hop neighbour traversal answers
  co-occurrence; Louvain clustering (recomputed on a change threshold)
  answers synonym clusters. Library: `petgraph` + ~200-line in-house
  Louvain (+200 KB).
- **Sentence-embedding similarity** (the "smart-and-clever" substance-
  similarity layer) — `fastembed-rs` (ONNX via `ort`, default model
  BGE-small-en-v1.5, 384 dims, ~33 MB) for embeddings; `hnsw_rs` for the
  approximate-nearest-neighbour index. Two embeddings per topic: string-
  only (for `StringSimilarTo`) and string-plus-recent-descriptions (for
  `SubstanceSimilarTo`, window of the most-recent 32 descriptions). +30-35
  MB binary footprint. The hybrid deliberately avoids the
  use-the-biggest-LLM-for-everything anti-pattern — each use case gets the
  precise tool, and the daemon declines the heavy layer when the model is
  absent.

### Cache substrate and the derivation invariant

The cache lives in the daemon's existing redb store as new tables alongside
`records` and `ledger` (`topic_frecency`, `topic_cooccurrence`,
`topic_embedding_string`, `topic_embedding_context`, `topic_cluster`). Each
record-write transaction also updates frecency + co-occurrence inline, so
those layers are always consistent without separate invalidation;
embeddings are debounced on a background queue (mark pending in redb;
survive restart). The load-bearing invariant: **the cache tables are pure
derivations of `records`** — frecency from the record list, co-occurrence
from each record's topic vector, embeddings from descriptions. A reset
(`Reset (TopicDiscoveryCache)`) drops the tables and re-populates from
records. Records are canonical; computed views are not.

### Schema additions and phasing

New operations sit under the existing `Observe` root as a `Topics`
`TopicQuery`: `SubstanceSimilarTo` / `StringSimilarTo` / `ByFrecency` /
`CoOccurringWith` / `All TopicOrdering` / `ClusterFor`. Replies are
`TopicsRanked` (score-bearing) / `TopicsListed` (browse) / `TopicCluster` /
`TopicQueryUnsupported` (when the backing layer is not installed —
graceful degradation). Three independently-ratifiable, independently-
shippable phases: phase 1 frecency (1-2 days, zero deps); phase 2
co-occurrence + clustering (2-3 days, +petgraph); phase 3 embeddings + ANN
(1-2 weeks, +fastembed). Phase 1 alone is a real feature; phases 1+2 cover
four of five use cases; phase 3 closes substance similarity. Cold-start
warms ~400 topics in background (~3-5 s batched); ordinary queries return
immediately, substance-similarity returns `TopicQueryUnsupported (warming)`
until the index is ready.

### Why this closes the fragmentation loop

The feature solves the `trace-testing` / `testing-trace` / `runtime-trace`
synonym-proliferation that motivated it at three layers: prevention
(query-before-capture, §3, sees existing options via substance similarity),
detection (the dedup heuristic + `ClusterFor` cluster query surface
candidates), and surfacing (browse + similarity queries make the vocabulary
visible at any time). It preserves the emergent-vocabulary discipline — no
appointed topic registrar — while closing the discoverability gap. Open
psyche items carried: phase-ratification cadence (lean: ship phase 1 now);
model-bundle delivery (lean: Nix-bundled vs first-run download); whether
topic queries accept the record-set filters (certainty / kind / time) that
`Records` queries already accept (lean: yes, symmetric).

## 5 — Contract-repo fork pipeline

Spirit 1422 (Decision Maximum, 2026-06-02) codified the per-component repo
split: the **Signal interface lives in `signal-<component>`** because
clients depend on it; **Nexus + SEMA stay daemon-local**; a multi-node
scale-out database is the named exception (a future `signal-sema-<component>`
contract). This is now the live build pipeline — the active-repositories map
shows `spirit` consuming `schema/spirit.schema`, `triad-runtime` as the
extracted shared runtime, and the `signal-` / `meta-signal-` contract repos
per component.

### The substrate was already ready — the migration is mechanical

The headline finding: no schema-substrate changes were required. The
cross-schema-import machinery already existed and was test-witnessed:

- `schema-next` resolves `crate:module:Type` imports via `ImportResolver`,
  loading the dependency's module schema through Cargo's
  `DEP_<CRATE>_SCHEMA_DIR` (exposed when the dependency declares
  `links` + emits `cargo:schema_dir=...`). Witnessed by the
  `marker-core` / `import-consumer` fixture.
- `schema-rust-next` already emits `pub use
  <crate>::schema::<module>::<Type> as <LocalName>;` for resolved imports,
  so the consumer re-exports imported types and skips re-declaring them.

The migration for an existing component is therefore: move the Signal
Input/Output + client-facing payload declarations into
`signal-<component>/schema/lib.schema`; import them from the daemon's schema
via the namespace; keep Nexus + SEMA + daemon-internal nouns local; wire the
build script's `ImportResolver`; switch `use crate::Input` to
`use signal_<component>::Input`. Estimated 2-4 operator days for the
spirit + signal-spirit pilot.

### The placement rule — what goes where

The load-bearing design decision is the split boundary, and it has one
subtle case worth stating as a rule: **a typed value the daemon *produces*
but the wire *carries* belongs in the Signal contract; its construction
algorithm stays in the daemon.** `DatabaseMarker` (commit sequence + state
digest) is the worked example — it is daemon-defined but every reply carries
it and clients must deserialize it, so the type lives in `signal-<component>`
while `Store::database_marker()` (the algorithm that fills it) stays in the
daemon. Client-facing payloads (Entry, Query, the observed/found/counted
result records, error + rejection reports) go in the Signal contract;
mail-ledger nouns, origin routes, and other runtime plumbing stay local.

### Help and trace across the split

Two derived clarifications the split forces, both with the same answer:
clients see only the **Signal-plane** Help and the **Signal-plane** trace
identity (`SignalObjectName` lives in `signal-<component>`); Nexus + SEMA
Help and trace identity are daemon-internal (`NexusObjectName` /
`SemaObjectName` stay local; the aggregator `ObjectName` lives in the daemon
because only it composes across all three planes). Clients that need the
daemon's internal vocabulary ask introspect, not the daemon directly. The
client-facing-Help-only positioning follows from Spirit 1422 + 1396/1397 and
was carried as a psyche-confirmation item.

### Sequencing

The fork order: spirit + signal-spirit pilot (proves the wiring); then
introspect by construction (greenfield — adopts the split from inception, no
migration cost); then persona + orchestrate when their slices open. The
naming gate (designer 458 — the `core-signal-spirit` → owner/meta-signal
rename) is independent of the fork but became more load-bearing because the
contract repo's name is now canonical pipeline input; it has since resolved
to the `meta-signal-<component>` naming the current workspace uses.

## What this refresh retired

Merged and deleted: 468 (developed interfaces — spirit / persona /
orchestrate), 469 (introspect component design), 473 (spirit algorithm
proposals), 474 (spirit topic-discovery feature), 475 (contract-repo
pipeline fork — the meta-report directory). Their live substance is above;
their superseded plane-shape framings (symmetric NexusInput/Output, the
push-trace-ingest introspect) are recorded as era history, not carried as
current design. The engine map, cutover staging, and schema-stack pipeline
they touched live in current reports 498/499.
