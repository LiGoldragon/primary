---
title: 533/3 — The Horizon / Lojix direction — context and the live forks
role: designer
variant: situation-report
date: 2026-06-05
session: 533 deep situation report (sub-report 3 of N)
dimension: THE HORIZON / LOJIX DIRECTION
topics: [horizon, lojix, signal-lojix, meta-signal-lojix, cutover, derive-nix, triad-engine, deploy-stack, criomos]
sources:
  spirit: [m85j, fe2j, vudl, mkvb, x8iv, qkvx, latq, rcn3, brgo, 2tfa, 783n]
  files:
    - /git/github.com/LiGoldragon/horizon-rs/INTENT.md
    - /git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md
    - /git/github.com/LiGoldragon/horizon-next/INTENT.md
    - /git/github.com/LiGoldragon/lojix/INTENT.md
    - /git/github.com/LiGoldragon/signal-lojix/INTENT.md
    - /git/github.com/LiGoldragon/CriomOS/flake.lock (lojix-cli pin)
    - ~/wt/github.com/LiGoldragon/{lojix,signal-lojix,meta-signal-lojix}/triad-port/
---

# 533/3 — The Horizon / Lojix direction

This is the biggest NEW theme since the 532 meta-supreme audit, and it is
the least-documented in primary's surfaces (no horizon/lojix mention in
ESSENCE/INTENT prose; the substance lives in six-plus Spirit records dated
2026-06-04/05 and in per-repo INTENT.md files). This sub-report establishes
the context first, then names the genuine forks.

## What is Horizon, what is Lojix, how they relate

**Horizon** is the *projection layer* of the deploy pipeline. It takes a
typed `ClusterProposal` (what a cluster owner authors — node names, trust,
hardware, router roles, secret references, provider selections) and projects
the per-`(cluster, node)` "horizon" view that CriomOS consumes to build each
node's NixOS configuration. There are now **three** horizon artifacts, which
is itself a source of confusion worth naming:

- `horizon-rs` — today's CANON, active on the live stack. Per `x8iv`
  (Clarification, Low): *"horizon-rs is currently a hack and does not have
  the regular component-triad shape; it predates the schema-derived component
  convention the rewrite is moving toward."* It is a Rust **library** linked
  in-process by the deploy path, not a daemon. Its `INTENT.md` carries the
  load-bearing "proposal boundary" discipline (variability + authority +
  non-derivable; service roles are variants; cluster owner must not author
  the OS).
- `horizon-next` — a schema-derived **concept prototype** (records 1048-1052,
  2026-05-28) proving Horizon's datatypes emit from a pure schema with a real
  Nix witness. Its own INTENT.md says the runtime shape is *deliberately left
  open* ("signal-only? triad? library?") — the concept illuminates the shape,
  does not force it.
- the *eventual* schema-derived horizon — what the rewrite converges toward.

**Lojix** is the *deploy-stack daemon + CLI* — the cluster-operator-owned
authority for "what generation is running on every node right now," GC-roots
retention, and the deploy event log. Per `mkvb` (Decision, High): lojix
*"should be built on the triad engine and schema substrate now that those are
starting to stabilize … rather than remaining a hand-written hack."* It
replaces the implementation surface of the monolithic `lojix-cli`. Lojix is
the **first real driver** of several shared-engine primitives (the
multi-listener daemon, schema-derived streaming) — it is the proving ground
for the whole triad engine on a real production component.

**The triad** is materializing as three repos: `lojix` (daemon + thin CLI),
`signal-lojix` (ordinary peer-callable wire), and `meta-signal-lojix` (owner
policy wire). This is the standard component-triad shape from
`skills/component-triad.md`, now applied to the deploy stack.

### How they relate to the schema-derived stack

The whole move is: take the two hacks (`horizon-rs` the library, `lojix-cli`
the monolith) and re-seat them on the **same schema-derived component shape**
every other component is converging on — schema source → emitted Rust types →
triad-runtime engine → signal wire. Horizon supplies the typed projection
*data*; lojix is the *daemon* that runs deploys and consumes that projection.

## The cutover sequencing — port-first, cutover-after

This is the spine of the theme. Per `fe2j` (Decision, High), the rewrite
ordering is **port-first**:

> *"complete the lojix triad-engine and schema-based-component port onto the
> schema-derived stack BEFORE cutting CriomOS over, then cut over onto the
> ported daemon. The dual-stack burden is retired only after lojix runs on
> the designed components, so Stack A is never retired onto a non-triad
> deployer."*

In plain terms there are two stacks:

- **Stack A** = today's live deploy path: `lojix-cli` (monolith) projecting
  `horizon-rs` over `goldragon/datom.nota`, writing flake inputs into CriomOS
  at deploy time. **This is what production runs today** — CriomOS's
  `flake.lock` pins `lojix-cli` at `4c66b8a6fa556014e48f8c137e1a8176ec713540`
  (verified in-tree).
- **Stack B** = the new triad `lojix` daemon on the schema-derived engine.

The sequencing decision is: build Stack B to **parity** first, cut CriomOS
over to it, and *only then* retire Stack A. Parity is the explicit bar (`fe2j`
+ `m85j`). This resolves a real tension the psyche named — between "use the
designed components fully" and "retire the dual-stack burden quickly" — in
favour of the clean end-state, accepting a longer dual-stack window.

### Where the port actually stands right now (live verification)

The port is **materially underway but NOT deployed**. Evidence:

- `~/wt/github.com/LiGoldragon/lojix/triad-port/` is a real Rust tree:
  `src/bin/lojix.rs`, `src/bin/lojix-daemon.rs`, `schema/nexus.schema`,
  `schema/sema.schema`, `build.rs`, wired to `triad-runtime` and
  `schema-rust-next` (both `branch = main`).
- `signal-lojix/triad-port/` and `meta-signal-lojix/triad-port/` worktrees
  BOTH exist with full `src` + `schema`. So the three-repo triad is being
  built in parallel on `triad-port` worktrees.
- The triad-port `Cargo.toml` already wires
  `meta-signal-lojix = { path = "../../meta-signal-lojix/triad-port" }` —
  i.e. `vudl`'s "carry meta-signal-lojix as a local path-dependency until
  cutover" mechanism is already realized as a sibling worktree, even though
  **no standalone `meta-signal-lojix` repo exists on disk yet** (vudl says
  create it AT cutover).
- On `main`, the `lojix` repo is docs-only (INTENT/ARCHITECTURE/AGENTS/README,
  no `src`, no `Cargo.toml`). The code lives only on the worktree branches.

So: the new triad is live in worktrees; production still runs the legacy
monolith. This is the **exact analog** of the 532 deployment gap
(schema-derived spirit proven in-tree, persona-spirit still serving) — and it
is the dominant risk pattern of the whole workspace right now: *proven, not
deployed.*

## The authority-split (meta-signal vs ordinary signal)

Per `vudl` (Decision, High), lojix uses the two-contract authority split:

- **Owner-only policy** → `meta-signal-lojix`: `Deploy`, `Pin`, `Unpin`,
  `Retire`. *"A deploy mutates the live cluster and can break the router so it
  is the strongest case for the owner socket."*
- **Peer-callable** → ordinary `signal-lojix`: `Query`, `WatchDeployments`,
  `WatchCacheRetention`, `Unwatch`.
- *"The policy contract is born meta-signal-lojix never owner-signal-lojix."*

NOTE a live tension here worth flagging to the psyche: `signal-lojix/INTENT.md`
(read 2026-06-05) still describes the OLD single-contract shape — it lists
`Deploy`, `Pin`/`Unpin`/`Retire` as requests in the ordinary contract's
channel ("Requests: `Deploy` … `Pin` / `Unpin` / `Retire` …"). That predates
`vudl`'s authority split, which moves exactly those four to meta-signal-lojix.
The per-repo INTENT.md has **not yet been reconciled** with vudl. This is a
manifestation-gap (AGENTS.md: per-repo INTENT.md updated on the same branch as
the work) — a concrete drift, not a fork.

## The Horizon simplification / collapse (derive-nix)

Per `m85j` (Decision, High) — the most intricate record in the cluster — there
is a planned **partial collapse** of horizon logic OUT of Rust and INTO Nix
composition, landing **AFTER cutover, not before**:

Move into Nix composition (a single re-exported CriomOS derive module so
consumer modules stay untouched):
- the `behaves-as` booleans,
- gating booleans (`is-dispatcher`, `is-large-edge`, `enable-network-manager`),
- the `at-least` magnitude ladders (by emitting the raw `Magnitude` ordinal),
- the lid-switch policy,
- the trust-gated extra-groups list.

Keep in Rust:
- arch resolution,
- the rendered typed name and key-line newtypes,
- the cross-node fan-in lists,
- typed validation,
- the secret-binding resolution map.

Critically: *"the collapse is a clean follow-on that does not gate cutover.
Prepare the derive seam during cutover so the collapse is a drop-in."* So
derive-nix is **sequenced third** — after parity, after cutover — but the
*seam* for it is prepared during the cutover work.

This connects to `qkvx` (Correction, High), the cluster-data typing rule:
node-service features must be TYPED end-to-end (the VmTesting work was rejected
for matching a string `VmTesting` instead of adding a real `NodeService` enum
variant in the horizon-rs model, authoring the fact in `goldragon/datom.nota`,
projecting typed, consuming typed in CriomOS). The correct order is
**typed-source-first**: extend the horizon model → author the fact → project
typed → consume typed. derive-nix moves *derivable* logic to Nix; qkvx insists
the *authored facts* stay typed all the way through. The two are consistent:
move computation to Nix, keep data typed.

## Adjacent shared-engine records this theme drags in (context)

The port forced several platform decisions the psyche has already made, which
bound the forks below:

- `latq`/`rcn3` — the **two-socket runner-wired daemon** is built once in
  `triad-runtime` as the `MultiListenerDaemon` primitive (rcn3 corrects: it
  ALREADY ships; no new `DualListenerDaemon` needed). lojix is its first
  consumer, binding ordinary + owner sockets.
- `brgo`/`2tfa` — **schema-derived streaming** is the chosen direction (not
  poll-as-permanent, not a lojix-only carve-out). `signal-lojix` carries
  `WatchDeployments`/`WatchCacheRetention` from day one; until real push lands
  the handshake-plus-poll suffices and *does not block cutover*. `brgo` carries
  an explicit open question: *was the existing signal-frame streaming substrate
  deliberate scaffolding ahead of this work, or leftover?* — which most changes
  the effort estimate.
- `783n` — Correction: disabling local builds was a **hallucinated guard**,
  never psyche intent; lojix must permit local builds (prometheus the large-AI
  router must build its own model-heavy closures locally).

## The genuine forks for the psyche

The records above settle a great deal (sequencing = port-first; authority =
split; collapse = after-cutover). The forks below are the places where intent
is genuinely *not* settled, or where a real choice is open and the psyche's
judgment changes the outcome. Each is restated as a decision point in the
structured output; here is the reasoning.

### Fork A — Parity scope: full-fidelity port, or lean cutover?

`fe2j`/`m85j` set "parity is the bar" but never define the parity SURFACE. The
new triad lojix is being built lean (the lean-daemon work, the dropped
local-builds guard). Two readings: (A) Stack B must reproduce *everything*
Stack A's monolith does before cutover (full GC-roots, event log, every deploy
phase, full retention semantics) — maximally safe, slow; or (B) cutover on a
*minimal viable* deploy path (deploy + query + activate), with retention/event
sophistication landing post-cutover behind the same daemon — faster to retire
the dual stack, accepting a thinner Stack B at the cutover moment. Intent says
"parity" but the word is doing a lot of unexamined work. The psyche owns where
the parity line is drawn.

### Fork B — When does standalone `meta-signal-lojix` get created?

`vudl` says: carry meta-signal-lojix as a local path-dependency until cutover,
*then* create the standalone repo at cutover. The triad-port worktrees already
realize the local-path mechanism. But the streaming/authority work is actively
churning the meta contract's shape RIGHT NOW. Fork: (A) hold to vudl literally —
standalone repo only at cutover, contract churns freely as a local package
until then; or (B) promote meta-signal-lojix to a standalone repo *earlier*
(now), so its INTENT/ARCHITECTURE and the authority-split discipline get a
canonical home and stop drifting against signal-lojix's stale single-contract
INTENT.md. The 532 lesson (un-named axis = opacity) leans toward earlier
naming; vudl's stopgap-mirroring leans toward later. Genuinely open.

### Fork C — derive-nix collapse boundary: is the m85j split final?

`m85j` enumerates by hand exactly which booleans/ladders/policies move to Nix
and which newtypes/validation/resolution stay in Rust. This is a hand-drawn
line down the middle of horizon logic — and 532's pattern-of-patterns warns
that *every hand-enumerated axis is a smell that wants a named noun*. Fork:
(A) accept the m85j split as the working boundary (move the five listed
buckets to Nix, keep the five listed in Rust); or (B) treat the split as
provisional and look for the *principle* that decides "Nix vs Rust" per item
(e.g. "pure derivable-from-facts → Nix; typed-identity / cross-node / secret →
Rust") so the boundary is a rule, not a list. Since the collapse is sequenced
last and is explicitly a follow-on, the psyche could defer this — but the
*seam* is prepared during cutover, so the principle (if there is one) shapes
the seam now.

### Fork D — horizon-rs vs horizon-next: which becomes the ported horizon?

There are two schema-direction horizons: `horizon-rs` (canon, hack-shaped,
carries the proposal-boundary discipline) and `horizon-next` (schema-derived
concept, runtime shape deliberately open). The lojix port re-seats the deploy
stack on the schema-derived engine — but it is NOT stated whether the ported
horizon IS horizon-next promoted to canon, or horizon-rs incrementally
schema-ified in place, or a fresh `horizon` triad component. `x8iv` only says
horizon-rs is a hack predating the convention; horizon-next's INTENT
explicitly leaves runtime shape open. Fork: (A) promote horizon-next to canon
and migrate the proposal-boundary discipline + full ClusterProposal into it;
(B) schema-ify horizon-rs in place, keeping its name/discipline, treating
horizon-next as a throwaway proof; (C) horizon becomes a full triad component
(horizon + signal-horizon + meta-signal-horizon) like lojix. This is the
biggest unstated structural choice in the theme.

### Fork E — the streaming open question (brgo) gates the cutover effort estimate

`brgo` carries the psyche's own open question verbatim: *was the existing
signal-frame `StreamingFrameBody`/`ObservableSet` substrate deliberate
scaffolding ahead of this work, or leftover?* The answer "most changes the
effort estimate" for the whole schema-derived-streaming platform project. This
is a factual question the psyche may be able to answer from memory (did you
build that substrate on purpose?) that no agent can resolve from the code
alone with certainty — and it directly sizes whether lojix's day-one Watch
subscriptions get real push soon or sit on handshake-plus-poll for a while.

## Cross-cutting observation: the deploy-stack is the workspace's proving ground

Lojix is where the *entire* schema-derived thesis meets a real production
component for the first time: it is the first consumer of MultiListenerDaemon
(latq/rcn3), the first prover of schema-derived streaming (brgo/2tfa), the
first triad with a meta-signal authority split in anger (vudl), and the first
hack being re-seated on the engine (mkvb). If the engine thesis is right,
lojix is where it gets demonstrated end-to-end on something that *deploys real
clusters*. That raises the stakes on the cutover: it is not just a deploy-tool
swap, it is the validation of the whole "schema is the program" direction
against production. The 532 deployment gap (proven-not-deployed) is therefore
not a side issue here — closing it on lojix is the highest-leverage proof the
workspace can produce.
