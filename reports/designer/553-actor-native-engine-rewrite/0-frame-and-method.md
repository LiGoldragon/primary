# 0 — frame and method: rewrite the schema-emitted engines as kameo actors

designer, 2026-06-07. Meta-report directory (sub-agent session).

## The ask

The psyche, after reading `reports/cloud-designer/35-actor-divergence-forensics/4-overview.md`
and confirming there is no valid technical reason the schema-emitted triad
engines are synchronous:

> "Okay, then rewrite it all with actors."

Preceded by the governing statement: *"all I know is I want actors everywhere"*
and *"is there a good, valid technical reason why there's no actors in the code
emission of our engines?"* — answered: no, and the current sync emission is
actively worse on that axis because it reaches for `Mutex<Nexus>` /
`Arc<Mutex<Store>>`, the shared-lock-over-mutable-state pattern the actor model
exists to delete.

## Recorded intent

Spirit `zk6y` (Correction, High, 2026-06-07): *"Schema-emitted Signal, Nexus, and
SEMA engines are kameo actors, not synchronous method spines driven by a runner
loop over mutex-wrapped state. Actors everywhere is the architecture; the
generated triad daemons are not exempt. Deferring advanced runtime machinery —
backpressure, scheduling, the runtime-control trait surface — never meant
deferring actors or emitting synchronous daemons. A minimal kameo actor carrying
on_start and on_stop adopts kameo now while that deeper machinery stays deferred.
The current synchronous daemon emission with mutex-wrapped engine state is drift
to correct, not a sanctioned end state."*

This does not retire records `1483`/`1487` — those deferred *advanced machinery*
and never said "sync" or "no kameo." The sync framing entered in
`skills/component-triad.md`, not in any psyche statement. The deferral stands; the
sync interpretation layered on top of it is what `zk6y` corrects.

## The leverage point

The stack splits into two families (per cloud-designer 35 report 2):

- **Emitted path** — `message`, `spirit`, and `cloud`'s emitted path ride
  `schema-rust-next`'s `daemon_emit.rs` → `triad-runtime`'s sync listeners. Fix the
  emitter + the runtime once, regenerate, and these become actors for free.
- **Hand-written holdouts** — `lojix` (triad-port), `cloud`-live, `repository-ledger`
  roll their own thread-per-listener loops. Each needs a manual migration.

So the rewrite is: (1) `triad-runtime` becomes a kameo actor runtime; (2)
`schema-rust-next/daemon_emit.rs` emits kameo actors; (3) regenerate the emitted
daemons; (4) hand-migrate the holdouts; (5) actor-density tests; (6) skill
correction.

## Design direction taken (flag the real forks; proceed on the recommended choice)

1. **Engine traits stay sync-pure logic; the emitted actor is the runtime shell
   that owns the engine impl and drives it through its mailbox.** The business
   logic does not go async; only the actor shell does. This keeps the engine
   traits testable, schema-clean, and free of actor/tokio coupling, while giving
   "actors everywhere" at the runtime layer. (Recommended; proceeding unless the
   psyche redirects.)
2. **Topology honours the concurrency records (`2alg`/`k6w1`/`tj99`), not a single
   god-actor.** SEMA is a single-writer actor (`apply(&mut self)` serializes,
   `observe(&self)` parallel reads); Nexus work runs per-request or pooled (NOT
   funnelled through one mailbox, which would re-serialize what those records made
   concurrent); the listener acceptance is a supervised runtime-root actor.
3. **Blocking work → concern-specific effect actors.** lojix's multi-minute nix
   build moves to a `tokio::process` effect actor with schema-visible
   cancellation and durability policy. Short sync bridges may use
   `spawn_blocking`, but long external commands own child-process lifecycle,
   output streaming, reaping, and cancellation explicitly. The mailbox never
   blocks.

## Lane handoff

Designer designs + proves; operator integrates. The main-line code across
`triad-runtime`, `schema-rust-next`, and the daemon repos lands through the
operator/main flow — designers do not push code-repo main. This session's
deliverable: (a) the authoritative actor-native design (topology, emitter shape,
blocking-plane mapping, migration sequence, per-repo change list); (b) a worktree
proof of the core — `triad-runtime` actor runtime + `daemon_emit.rs` actor
emission + the `spirit` pilot regenerated — demonstrating the shape compiles and
serves; (c) the `skills/component-triad.md` substrate correction (primary,
designer-owned, lands on main here). Operator then integrates and migrates the
remaining daemons following the design.

## Method

Hybrid, multi-phase. Designer-protocol workflows allowed (prime designer runs at
full capacity).

- **Phase 1 — Map (workflow `w63hfqahs`, 6 parallel readers).** Ground the design
  in the real code, not the cloud-designer-35 summaries: runtime, emitter, spirit
  pilot, kameo/actor-systems target templates, hand-written holdouts, engine-trait
  signatures + the verbatim concurrency intent. Each returns a structured map
  (current shape, sync mechanisms with file:line, actor-target notes, migration
  needs, risks). Results land as numbered reports in this directory.
- **Phase 2 — Design (designer synthesis).** The authoritative redesign as the
  highest-numbered file here; the `component-triad.md` correction.
- **Phase 3 — Prove (worktree).** Build the actor-native core + spirit pilot under
  `~/wt`, demonstrate it compiles and serves; hand operator the integration.

Numbered sub-agent maps fill in as Phase 1 returns; the design synthesis is the
highest-numbered file.
