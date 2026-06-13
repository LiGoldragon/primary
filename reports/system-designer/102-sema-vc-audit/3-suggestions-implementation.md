# 102/3 — Audit suggestions: implementation outcome

*Follow-through on the three suggestions in 102/2, on psyche direction ("Make
sema-engine single-writer structural" → corrected to the internal mutex; "do
all 3 suggestions"). Built as designer feature branches via an adversarial
build→review workflow; pushed for operator integration. Two slices fully
landed and approved; the durability/shipper suggestion proved to be a larger
multi-repo arc and was deferred honestly rather than half-built.*

## What landed (green + adversarially approved)

### S2 + S3 — sema-engine single-writer (internal mutex) + O(1) chain-head digest

Branch `single-writer-internal-lock` @ `22b9de17` (sema-engine), **v0.5.0**.
Reviewer re-ran the suite independently: **approve**.

- **Single-writer via an internal lock, not `&mut self`** (the psyche's
  correction — the lock avoids the fleet-wide API ripple `&mut self` would
  force). A `Mutex<()>` field on `Engine` is held across each mutator's whole
  read-compute-write (`assert`/`mutate`/`retract` + `_keyed`/`_identified`,
  `commit`, `checkpoint`, `rebuild_from_log`, `acknowledge_mirror`), serializing
  the sequence allocation + predecessor-digest read + dup-check + identifier
  mint + redb write that previously raced across separate read transactions.
  **Mutators keep `&self`; the public API is unchanged** (one additive accessor
  `versioned_chain_head`), so there is zero consumer ripple — proven by the
  spirit repoint below passing every feature set unchanged.
- **O(1) chain-head digest** (designer 615 flaw #1, which 102 missed): a new
  `CHAIN_HEAD` table + log-count counters advanced inside the single
  `insert_versioned_row` choke point; `latest_versioned_entry_digest` now does a
  point-get instead of decoding the entire payload-bearing log on every write,
  and `ensure_versioned_log_complete` compares persisted counts instead of two
  full scans. Kills the O(n)-per-write / O(n²)-over-life cost.
- **Integrity preserved, witnessed.** The cached head is optimization-only —
  `CanonicalView::fold` is untouched and still recomputes + verifies the chain
  link-by-link; `tamper.rs` 11/11 unchanged. New witnesses: an 8-thread
  `Arc<Engine>` concurrency test (asserts unique, contiguous commit sequences
  and a clean fold — the proof the lock serializes a shared `&Engine`), and a
  cached-head == fresh-fold-recompute test. Full suite 109/0, clippy clean.

### STEP 1 of S1 — spirit repoint (proof the engine change is a transparent drop-in)

Branch `mirror-shipper` @ `8667d5f1` (spirit). Cargo repointed to the
single-writer engine; **every spirit feature set passes unchanged** (the four
production-migration witnesses, `versioned_store`, `process_boundary`, the
runtime-triad suites), with zero source edits. This is the empirical proof that
S2/S3 is a clean drop-in with no regression.

## Critical integration coupling — slice A is NOT deployable alone

Slice A bumps `STORAGE_LAYOUT` **4 → 5** (the new `CHAIN_HEAD`/count tables). The
layout bump is correct (a layout-4 store has no cached head; silently reading it
as `None` would fork the chain — hard-fail is the safe choice). But the
consequence: **every existing sema-engine store on disk is layout-4** — the live
spirit v9 store, and router/criome/mind — so the layout-5 engine hard-fails at
open until a rebuild runs. `spirit-migrate-store` will **not** catch this (it
probes a layout-4 v9 store as `Current` and no-ops). Deploying slice A without
handling the bump reproduces exactly the daemon-down class this whole arc is
fixing.

The resolution is the decision the psyche already made: **rebuild-from-log on
layout/schema skew** (`primary-lmf3`). On open, a layout-4 store with a present,
verified log refolds `CHAIN_HEAD` + counts from the log and re-stamps layout-5 —
zero-downtime, self-healing across the fleet. **`lmf3` is therefore the deploy
gate for slice A; the two must integrate together.** (Equivalently, slice A
could grow a backfill-on-open, but `lmf3` is the general, decided mechanism.)

## S1 durability/shipper — a 3-repo arc, deferred (not half-built)

Wiring a live component's outbox to the mirror is bigger than "wire the existing
actor." `mirror::ComponentShipper` owns its engine **by value** (`Engine` isn't
`Clone`), and a component's shipper must read the **same** store's outbox — a
second `Engine` on the same `.sema` file is impossible (redb's exclusive lock).
The correct design is now *possible* precisely because slice A made `Engine`
`Send + Sync` with `&self` working methods: **hold the engine as `Arc<Engine>`
and hand a clone to the shipper.** That requires three coordinated branches:

1. **mirror** — `ComponentShipper` takes `Arc<Engine>` (+ its `end_to_end_arc`).
2. **signal-spirit** — an optional mirror-address field on
   `SpiritDaemonConfiguration` (an rkyv contract change; today: socket /
   meta-socket / database / trace-socket / guardian only).
3. **spirit** — `Store` holds `Arc<Engine>`, plumb the configured address, spawn
   the shipper only when set, ship after each durable commit + interval tick.
   **Off by default; deploy-gated on `primary-x3l7`** (ingress auth) — never
   enabled against the unauthenticated `0.0.0.0` ingress.

The builder pushed STEP 1 green and stopped rather than push a half-built
shipper. This is recorded on `primary-85hv`.

## Beads

| Bead | State after this slice |
|---|---|
| `primary-7hro` (single-writer) | **Done** on `single-writer-internal-lock` @ `22b9de17` v0.5.0; carries the O(1) head-digest; layout-5 deploy caveat noted |
| `primary-lmf3` (rebuild-from-log) | Now the **deploy gate** for slice A — must land together; comment records the coupling |
| `primary-85hv` (shipper) | Re-scoped to the 3-repo `Arc<Engine>` arc; STEP 1 repoint proven |
| `primary-x3l7` (ingress auth) | Unchanged — still gates enabling the shipper |

## Next moves (psyche's call on pace)

1. **`lmf3` rebuild-from-log** — decided, and now the deploy gate for the
   single-writer slice. Natural next build; unblocks slice A's integration.
2. **The 3-repo shipper arc** — closes the live `29pb` durability gap; depends on
   the ingress auth (`x3l7`) before it can be enabled.

## Update — `lmf3` landed; the engine stack is now deployable

`lmf3` (rebuild-from-log on layout skew) is built, green, and adversarially
approved: sema-engine branch **`rebuild-from-log` @ `e5e38e8e`, v0.6.0**, stacked
on slice A (`single-writer-internal-lock` @ `22b9de17` is a direct ancestor), so
the tip is **single-writer + O(1) head-digest + rebuild-on-skew as one deployable
chain.**

The open path now classifies into a typed `LayoutOpenPlan { Current | StampFresh
| RebuildDerivedSlots }`. On an *older* stamped layout *with* a present versioned
log, the engine refolds the layout-introduced derived slots (`CHAIN_HEAD` +
counts) from the log via `CanonicalView::fold` from genesis — verified by
recomputation, never trusting the stored head — then re-stamps the current layout,
in one write transaction, *after* the read-only validation passes (so a rejecting
open still never mutates). It needs no family/table registration (raw-log refold,
runs before `register_table`). An older layout with **no** log keeps the typed
`StorageLayoutMismatch` (the previous-engine `StoreMigration` still owns pre-v9);
a newer layout still errors (no downgrade).

Witnessed in `tests/layout_rebuild.rs`: the headline test writes 7 entries,
*simulates* an old store (deletes `CHAIN_HEAD` + counts, re-stamps layout 4),
reopens, and proves the open succeeds, re-stamps 5, the rebuilt head equals a
fresh fold's head equals the pre-skew head, the data surface is identical, and the
next assert chains off the rebuilt head; plus a no-log-still-hard-fails witness and
an idempotent-reopen no-op witness. tamper 11/11 and slice A's concurrency +
cached-head tests stay green; clippy clean; no public API change.

**The deploy-gate coupling is resolved.** Deploying `e5e38e8e` over the existing
layout-4 stores (live spirit v9, router, criome, mind) self-heals on open,
zero-downtime — so the layout-4→5 bump is now safe to ship. Operator integration
is filed as **`primary-qu28`** (P1): integrate the `rebuild-from-log` tip to
sema-engine main, verify on a staging copy of the live store first, repin
consumers (spirit's repoint proven on `mirror-shipper` @ `8667d5f1` — pin it to
the `rebuild-from-log` tip). The remaining durability work is the 3-repo shipper
arc (`primary-85hv`), with config on the meta plane (`meta-signal-spirit`
`Configure`, beside `ArchiveDatabaseTarget`) and deploy-gated on ingress auth
(`primary-x3l7`).
