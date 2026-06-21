# Parallel lanes — deployed and complete

Execution of the report 705/706 follow-ups, run as parallel lanes, nix-gated,
autonomous. All landed on production.

## Lane A — bounded parser → production (critical)

The nota-next parser OOM fix (report 706) is now **live in production**, the
whole chain nix-gated:

1. **nota-next 0.5.1** parser-progress fix landed on `main` (`f94b546`); full
   suite (70 tests) green.
2. **spirit** re-pinned its `nota-next-source` to `f94b546` → `main`
   (`711cf79e`).
3. **nix build gate:** `nix build spirit` succeeded (`x7a3vab6…`), and the
   built `meta-spirit` on a stray `|]` **errors** ("unexpected closing
   delimiter `]`", exit 1) instead of OOMing — confirmed under an 800 MiB cap.
4. **Deploy:** CriomOS-home re-pinned spirit → `711cf79e` and fast-forwarded
   **`main`** (`fd30494e`); lojix `Build` then `Activate` (pinned to the
   explicit commit rev — the branch ref hit a stale nix eval-cache the first
   time and deployed the old build). Daemon restarted → `phm2l3c…`.
5. **Production gate:** the deployed `meta-spirit` on `(a |])` errors (exit 1),
   no OOM at a 400 MiB cap. Upsert bypass re-verified (re-import of an existing
   id overwrites). Memory healthy (22 GiB free). **The 23.6 GiB OOM pattern is
   fixed in production.**

## Lane B — trim cleanup (parallel)

- **Mini-essays condensed:** a 6-chunk workflow (condense + adversarial verify
  that no arrow is lost) condensed the survivor essays; applied via the bypass.
  Mini-essays (≥800 chars) **72 → 13**; avg desc 401 → 388, max 2256 → 1882.
  The 13 remaining are dense legitimate merges carrying many arrows.
- **Referents normalized:** the last non-kebab referents (`CriomOS`,
  `Horizon`) re-pointed to `criomos`/`horizon` via the bypass. Active store is
  now **0 non-kebab referents**, 99% referent coverage (614 active, 609 with
  referents; the 5 without name no particular).

## Final production state

| | |
|---|---|
| Active records | **614** (from 1323, −54%) |
| Referents | 99% populated, **all kebab**, 0 non-kebab |
| Mini-essays (≥800) | 13 (from 72) |
| Daemon | spirit 0.15.0 `phm2l3c…`: bounded parser + kebab enforcement + auto-register + in-place upsert, all live |
| Memory | healthy (22 GiB free); OOM pattern fixed |

## Constraint documented (report 706)

Agent-spawned bulk/long jobs run detached + memory-capped via `systemd-run`
(skill rule 8). This whole execution used that pattern — every build/trim ran
as a `systemd-run --user` unit with retries, surviving the terminal/harness
instability that killed earlier session-tied jobs; status checked with short
non-blocking reads only.

## Remaining (minor, optional)

- 13 dense merge-survivors still >800 chars (could be split/condensed further).
- nota-next parser depth/length limits (deep-nesting stack-overflow is a
  separate, smaller DoS than the fixed infinite-loop).
- NOTA round-trip validation in agent encoders (layer 3 of 706).
- Branches landed: nota-next `main` (f94b546), spirit `main` (711cf79e),
  CriomOS-home `main` (fd30494e). All pushed.
