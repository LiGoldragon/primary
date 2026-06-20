# Resume status — deploy landed, trim staged, harness unstable

Picks up after `3-synthesis-and-handoff.md`. Several things changed; this is
the current ground truth.

## What's now true (verified this session)

- **The bypass deployed to production.** spirit-daemon is `0.15.0`
  (`/nix/store/rm44fb9…-spirit`), and its daemon binary carries the bypass
  (`NonKebabReferent` ×2). So kebab-case enforcement + referent auto-register
  are **live in production**. (My earlier "0.14.0 / no bypass" reading was a
  stale un-restarted process + checking the CLI binary, not the daemon.)
  The lojix/datom toolchain that blocked the deploy was fixed (lojix `0.3.10`
  deployed), and the home activation went through.
- **Production is healthy**: `0.15.0`, **1261 active records**.
- **The deployed daemon is the INSERT-ONLY bypass** (commit `e126e5a`), not
  the upsert version — it predates the upsert fix below.

## The upsert fix (root-caused + fixed + tested, NOT yet deployed)

The bulk import failed with `InternalError` on every real record. Root
cause: **`import_record` was insert-only** — its SEMA `assert` rejects an
existing key, so the owner Import could only restore into empty/new keys,
never overwrite a live record. My plan overwrites survivors *at existing
ids*, so all failed (a fresh id imports once, fails on re-import; an existing
id fails immediately).

Fix: `import_record` now **upserts** — `mutate` when the id exists, `assert`
when new (matching `change_record`/`change_certainty`). Also fixed one
invalid domain in the plan data (`Technology.Software.Networking` →
`Technology.Software.Distributed.ProtocolDesign`).

State of the fix:
- Committed: spirit `origin/main` = **`7fc267cb`** (bookmark
  `spirit-import-bypass`). nix build → `/nix/store/5cxwh8…-spirit`.
- Tests: `tests/import_auto_register_referents.rs` — 3 pass, incl.
  `import_upserts_an_existing_record`.
- Sandbox: the upsert daemon imported real records correctly (e.g. `rvnf`
  gained its `[spirit capture-gate]` referents on overwrite).
- **NOT deployed to production** — production still runs the insert-only
  `e126e5a`. The in-place trim cannot run on production until `7fc267cb` is
  deployed (or it would re-hit the insert-only failure on existing ids).

## Trim plan staged and current-store-aware

`raw/render3.py` regenerates from a fresh dump: **590 survivors to import**
(upsert) + **650 to nominate** (merge-sources + removals). It skips ids no
longer active and uses current entry content for unchanged-desc survivors so
concurrent edits aren't reverted. Already executed: **80 free removals**
(early; recoverable Zero). Remaining: the 590 imports + 650 nominations.

## Harness instability (the immediate blocker)

The terminal/harness **crashes** when a long-running bash command is active —
specifically `until …; do sleep N; done` / `for … sleep` wait-loops and
`timeout …` commands (exit 144 / 137; the user confirmed a terminal crash on
message-send). Plain, short, non-blocking commands are fine.

Consequence: the full sandbox bulk run (15 import batches + 650 nominations
in one script) could not be babysat to completion — the sandbox daemon got
killed mid-run (empty log = external kill, not a daemon crash). Mitigation
going forward: **no long wait-loops or `timeout`**; run bulk work in true
background (`run_in_background`) and check with single short reads; or chunk
into small pieces.

## Open risk: bulk-import performance

`import_record` auto-register re-reads the whole referents table per referent
(`canonical_referent` / `reject_conflicting_referent_names` / `referent_by_key`
each scan `referents()`), so a 590-record import that registers hundreds of
new referents is roughly O(records × refs × referents) — possibly slow at
scale. Unverified end-to-end (sandbox kept dying). Worth either a batch-level
referent cache or just patient background execution.

## Next steps to finish

1. Deploy the upsert spirit (`7fc267cb`) to production (same lojix home path
   that worked: re-lock CriomOS-home `criomos-home-spirit-bypass` to spirit
   main, `lojix-run … Build` then `Activate`). Verify the activation actually
   picks up the new rev (the prior activation had a pin/eval lag).
2. Re-dump + re-render (`parse.py` → `render3.py`) for freshness.
3. Run the 590 imports (`meta-spirit` per batch) + 650 nominations
   (`ChangeCertainty Zero`) — in true background, short status reads only.
4. Validate: active ≈ 590; every survivor has kebab referents; sample
   lookups; `archive.py` for the trimmed-records archive.
5. Backups: pre-audit store at `~/.local/state/spirit-audit-backup/`.
