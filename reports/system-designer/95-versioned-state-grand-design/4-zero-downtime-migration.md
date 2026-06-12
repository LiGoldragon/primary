# Zero-Downtime Migration as a Branch: Online Schema Evolution Mapped onto a Typed Event Log

## Scope and thesis

Report 92 surveyed general version-control prior art. This report extends into the migration dimension specifically: how the industry achieves zero-downtime schema/data change today, and how each technique maps onto a design where the **event log is authoritative**, every log entry already carries a typed diff, the redb store is a rebuildable view, and we have per-component policy hooks plus consistent blake3 + criome-BLS crypto.

The central claim: classic online-migration tooling (gh-ost, pgroll, Reshape, Stripe four-phase) exists almost entirely to work around a constraint we **do not have** — that the store is the single source of truth and cannot be torn down and rebuilt. Their machinery (shadow tables, dual-write triggers, versioned views, MapReduce backfills, Scientist comparison) is elaborate scaffolding for migrating *a mutable store in place*. In an event-log design the store is derived, so the correct primitive is different and simpler: **a migration is a branch.** You author a new reducer/decoder, replay the existing log onto a side branch under the new schema, verify state-equivalence at a checkpoint, and atomically swap the head. The agent-era shift is that authoring and verifying that reducer — historically the expensive, error-prone step — is now cheap and routine.

What the classic tools still teach us is precise and worth importing: the *cut-over invariant* (gh-ost), the *bidirectional dual-version window* (pgroll), the *equivalence-comparison-in-production discipline* (Stripe Scientist), and the *upcaster-vs-versioned-event distinction* (event sourcing). The clever synthesis is to keep the elegance of branch-and-swap while borrowing exactly those four disciplines as policy-hooked steps.

## The expand-contract family: in-place store migration

### Parallel Change (expand / migrate / contract)

The canonical framing is Martin Fowler's 2014 *Parallel Change* (a.k.a. expand-and-contract), drawing on *Refactoring Databases* (Ambler & Sadalage, 2006). Three phases: **expand** (add new schema additively, nothing breaks), **migrate** (dual-write, backfill, cut reads over while both shapes coexist), **contract** (drop the old shape once no consumer references it). The invariant: the store always satisfies *both* the old and new contracts simultaneously during the window, so app versions can roll forward and back independently.

This is the conceptual root of everything below. It is fundamentally a discipline for a **mutable store that must never be unavailable and cannot be regenerated**, so the new shape has to be grown *inside* the live store alongside the old.

### gh-ost and pt-online-schema-change (MySQL)

Both `ALTER` a large live table by building a **ghost/shadow table** in the new shape, copying rows in chunks, propagating concurrent writes, then swapping. They differ in how writes propagate:

- **pt-online-schema-change** is trigger-based: `INSERT/UPDATE/DELETE` on the source synchronously fire triggers that write the ghost in the same transaction. Strict consistency, no lag, but trigger load and cut-over contention.
- **gh-ost** is triggerless: it tails the binlog and replays events into the ghost asynchronously, keeping the source cheap at the cost of replication lag and runtime complexity.

The genuinely clever part is **gh-ost's atomic cut-over**. It uses two connections and a sentry/"magic" table. One connection holds a lock; another issues the atomic `RENAME` of source↔ghost; a sentry table is positioned so the `RENAME` is *blocked* from executing prematurely until gh-ost confirms all preconditions. Either the swap completes atomically, or on timeout/connection-loss the system reverts cleanly to the original table with **no intermediate window of unavailability and no data loss**. That all-or-nothing head-swap invariant is exactly what an event-log head-swap needs.

### pgroll and Reshape (Postgres): the dual-version-view design

These are the state-of-the-art *in-place* tools and the most architecturally interesting, because they make expand-contract a first-class, automated, reversible operation.

**pgroll** (current release v0.16.2, May 2026) serves **multiple schema versions concurrently** by building per-version *virtual schemas out of Postgres views* over the physical tables, and routing each client by `search_path` (`SET search_path TO 'public_<migration>'`). On a breaking column change it adds a new physical column, **backfills it in batches** (default 10k rows/batch) using a user-supplied `up` SQL expression, and installs **bidirectional triggers** so writes to either the old or new column propagate to the counterpart. Both versions stay fully readable and writable during the window. Lifecycle is three explicit commands: `start` (create new schema, additive physical changes, backfill, triggers), `complete` (drop old schema/columns, finalize), `rollback` (drop the new schema, old stays intact). Reshape (Fabian Lindfors) is the same idea — views encapsulate the tables, new views + translation triggers bridge old↔new during the window.

The clever kernel here is **the bidirectional up/down transform as data, attached to the migration**, plus **per-version isolation via a virtual-schema indirection**. Both map cleanly onto our log (below).

## Stripe four-phase: in-place *data-store* migration with production equivalence checking

Stripe's "Online migrations at scale" generalizes expand-contract from one table to a whole data store, and contributes the verification discipline:

1. **Dual writing** to old and new stores to keep them in sync going forward.
2. **Backfill** existing data into the new store (done offline via Hadoop/MapReduce to avoid hammering production).
3. **Switch reads** to the new store.
4. **Switch writes** to new-only, then **remove** old data/code (lazy delete with error-on-access to flush hidden dependencies).

The standout is **verification with GitHub's Scientist**: read from *both* old and new in production, compare, and raise an alert on any single mismatch — equivalence checked continuously against live traffic before committing to the cut-over. This is the discipline our branch model needs to make "state-equivalent" a *proven* property rather than an assertion.

## Event-sourcing schema evolution: the layer we actually live in

Because our log is authoritative and the store is a fold over it, the relevant prior art is event-sourcing schema evolution, not table-ALTER tooling. The empirical literature (Overeem et al., *An empirical characterization of event sourced systems and their schema evolution*, JSS 2021 / arXiv 2104.01146) names five tactics: **versioned events, weak schema, upcasting, in-place transformation, copy-and-transform**. The two that matter for a *typed, schema-fragile rkyv* log:

- **Upcasting** — a transform runs at read/replay time converting old event versions to the current shape, so reducer code only ever handles the latest version; upcasters chain (v1→v2→v3). Read-time, store stays untouched.
- **Versioned events + copy-and-transform** — for changes too large to upcast (split one event into two, change identity), you write a *new* log under the new schema by transforming the old, and keep the old immutable. This is the event-sourced name for "migration as a branch."

The hard rule from this literature is our rule too: **never mutate stored events; transform on read or write a new version.** rkyv 0.8's schema-fragility makes any type-set change a hard migration, which pushes us toward copy-and-transform (rewrite the log under the new type-set) over indefinite upcaster chains — see does_not_fit.

## Git-for-data: branch / merge / rebase over content-addressed data

This is the frontier most aligned with the new psyche requirements (branch, fork, rebase, merge with per-component policy).

**Dolt** is the first SQL database with true branch, diff, and **three-way merge** on table data, built on **prolly trees** (probabilistic/content-addressed B-trees: a Merkle tree built by recursively applying a content-defined chunker via a rolling hash). Properties that matter to us:

- **Content-addressing + structural sharing**: tables are chunked (~4 KB) and any chunk identical across branches/versions is stored once. Diff and merge are cheap because they compare hashes and skip shared subtrees.
- **Three-way merge** produces a merge commit integrating both branches; **conflicts are stored by primary key in a separate prolly tree** holding the row as it appeared in *base, ours, theirs*, with bulk strategies (`take-ours`, `take-theirs`) and cell-level merge.

This is the cleanest existing demonstration that branch/merge/rebase over a database is real and efficient when the data is a content-addressed Merkle structure. Our blake3 hash-linked log is already a Merkle chain; the missing piece is a content-addressed *materialized index* so that diff/merge can be structural rather than row-by-row.

**Datomic** contributes the crucial **negative** result. It has immutable log + `as-of` time-travel + speculative in-memory writes (`d/with`, Datomock-style forking). But (per Daniel Janus, 2025) **you cannot branch from the past**: `as-of` and speculative writes don't compose, because `d/with` generates new datoms against the *unfiltered* full-history database, not the filtered past value — producing internally inconsistent transactions. The lesson: **a log-with-mutable-index is not branchable from arbitrary points; only a self-contained content-addressed commit is.** Git-style branching works precisely because each commit is self-contained. This directly constrains our design: branch points must be *checkpoints that fully capture state*, not bare log offsets into a shared index.

## The agent-era shift: migration as a verified branch with atomic head-swap

Pre-agent, "rewrite the whole reducer and replay all of history" was the *theoretically clean* migration that nobody did, because authoring a correct reducer over every historical event and proving the rebuilt state equivalent was expensive and risky — so the industry built shadow-table/dual-write/backfill scaffolding to migrate in place instead. With agents authoring and verifying reducers fast (and zero-downtime large-stack rewrites now routine), the clean version becomes the *practical* version. Recent work frames this exactly: state is a fold over the log, so replay is sound **iff** behavior bodies are deterministic functions of their inputs (Sakura Sky, *The Log is the Agent*, arXiv 2605.21997). Determinism is the enabling contract; verify it at the boundary, not just dynamically at replay.

The end-shape: **SchemaTransition-as-a-log-entry → side-branch replay → equivalence-verified checkpoint → atomic head-swap.** Detailed below.

## maps_to_our_design and clever combination

See the structured fields. In prose, the cleanest zero-downtime migration for our typed rkyv event log is:

1. **SchemaTransition is itself a typed, hash-linked log entry** carrying the new family schema-hash, the per-family decoder selector update, and the reducer/transform as data (the event-sourcing copy-and-transform, made first-class like pgroll's `up`/`down` expressions). It is signed (BLS) like any history-affecting record.
2. **Replay onto a side branch**: spawn a branch whose head is the SchemaTransition; rebuild the redb view by folding the existing log under the new decoder/reducer. Because the store is derived, this is a clean rebuild — no shadow table, no dual-write triggers in the store.
3. **Verify state-equivalence at a post-migration checkpoint** (Stripe-Scientist discipline, but offline and total rather than sampled-in-production): the checkpoint is a content-addressed snapshot (Datomic lesson: branch points must be self-contained), and equivalence is a defined relation between old-view and new-view checkpoints, BLS-attested.
4. **Atomic head-swap** (gh-ost cut-over invariant): flip the authoritative head from old to new in one all-or-nothing step; on any failure the old head remains authoritative, zero downtime, no partial state. Daemons self-resume from persisted SEMA state against whichever head is current.
5. **Per-component policy hook**: intake/merge/rebase routes each entry through the component's policy (default impl + override). A rebase under Spirit routes every entry through the **guardian** (admit / reject / transform) — which is structurally identical to an upcaster/transform step, so guardian-as-rebase-policy and transform-on-replay are *the same mechanism* wearing two hats. This is the genuinely elegant unification: **migration, rebase, and intake-policy are one operation — fold-with-policy over a log range producing a new branch** — differing only in which policy function and which source range.

The clever combination for our case: take Dolt's content-addressed structural-sharing index (so branch/diff/merge of the *view* is cheap), gh-ost's atomic head-swap invariant (the cut-over), pgroll's transform-as-migration-data (the `up`/`down` becomes our reducer + inverse), Stripe's equivalence-proof discipline (now total and offline, BLS-attested at a checkpoint), and the event-sourcing copy-and-transform tactic (write a new log/branch under the new schema, old stays immutable) — and observe that **rebase, merge-intake, and migration collapse into a single policy-parameterized fold**. blake3 content-addresses every chunk/checkpoint; BLS signs every branch head and equivalence attestation. One crypto basis, no divergence.

