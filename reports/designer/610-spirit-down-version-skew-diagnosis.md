# Spirit daemon down — versioned-store deploy skew (diagnosis, not fixed)

A quick look at why the live Spirit intent daemon is down. **Nothing changed; no
fix attempted** — the psyche asked for a read before a context reset. Intent
capture/query has been down workspace-wide since 06:11 today (the irony: I can't
even log this finding through Spirit because Spirit is the thing that's down).

## The headline

**The 0.12.0 versioned-store work landed on the spirit repo but was never
deployed to this laptop, and meanwhile the live store moved to a version the
*deployed* daemon can't open. Data moved forward; the running code stayed back.**
This is the V7→V8 step the psyche doubted — the doubt was well-placed.

## What I verified

- **spirit repo `main` = 0.12.0** versioned store: log-is-authoritative + redb as
  a rebuildable view (Spirit `iir4`), `SPIRIT_SCHEMA_VERSION = 9`, a v1..v8 → v9
  migration ladder in `production_migration.rs`, and the upgrade binary **renamed
  `spirit-upgrade-store` → `spirit-migrate-store`**. The migration code itself
  looks correct: it opens the old store with the pinned *previous* sema-engine,
  detects v8, and folds it through `from_v8` into a fresh v9 store.
- **CriomOS-home `main` still pins spirit at `0a6f93af` — my old 0.11.3** — and
  its daemon `startup-state` still runs the old `spirit-upgrade-store`. So
  **0.12.0 was never deployed here**; the host is running the pre-versioned-store
  daemon.
- **The daemon dies in `ExecStartPre`**: `spirit-upgrade-store` →
  `sema: schema version mismatch — file was written with v8, this build expects
  v7`. It fails, systemd retries 5× in 12s, hits the start-limit, gives up. The
  store `spirit.sema` (1.3 MB, ~1200 records) was last written **07:54 today** —
  *after* the 06:11 boot failures, so something ran against it this morning.

## The mechanism (high confidence)

The deployed `spirit-upgrade-store` is a **non-idempotent v7→v8 upgrade step** in
the boot path: it opens the store expecting the *old* version and upgrades. Once
the store is already at v8, re-running it (expecting v7) errors and **blocks the
boot** — even though the v8 daemon itself could open a v8 store. So the boot is
wedged on a startup migration tool that can't handle an already-migrated store.

## What I'm NOT sure of (check before any fix)

1. **The store's true current version/state.** It read as v8 at 06:11; something
   touched it at 07:54. It could be cleanly v8, or part-migrated — the handoff
   (report 97) flags that the migration is "currently a full rewrite + fs::rename"
   that still needs to become crash-safe, so a half-run could leave it
   inconsistent. **Verify the real version/integrity first.**
2. **What ran at 07:54** (a manual `spirit-migrate-store`? a restore? a partial
   activation?) and exactly where the deployed "expects v7" comes from.

## Likely fix (for after the reset — do NOT start blind)

1. **Back up first**: `spirit.sema` + the guardian journals + the existing
   `spirit.schema-*-backup-*.sema` are small; copy them aside before touching
   anything.
2. **Establish the store's actual version** with the current-main
   `spirit-migrate-store` detect path (not the old non-idempotent upgrade tool).
3. **Deploy 0.12.0 to the host properly**: bump CriomOS-home's spirit pin to
   current `main`, switch `startup-state` from `spirit-upgrade-store` to
   `spirit-migrate-store`, activate — letting the correct v→v9 logged-fold
   migration run on the backed-up store. The boot path should stop running a
   non-idempotent upgrade step on every start.
4. If the store is already part-migrated or the laptop copy is suspect, the
   versioned-store's own point: **restore from the server mirror / backup log**
   (the whole reason this system exists is data-loss protection).

## Ownership note

The versioned-store migration is the system-designer's grand-design work (reports
95–101, operator 209–214), built by the Fable-5 lane. The bug is not obviously in
the *migration logic* (which handles v8→v9) — it's in **deploy coordination**: the
new code never reached this host while the store advanced, and the boot path keeps
a non-idempotent upgrade step. Fixing it touches the live ~1200-record corpus, so
it wants a backup + a careful, single, verified pass — ideally coordinated with
that lane.
