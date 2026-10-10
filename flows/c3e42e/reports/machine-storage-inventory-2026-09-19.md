# Machine storage snapshot — 2026-09-19

## Scope and confidence

This is a **bounded snapshot**, not a complete inventory. It uses filesystem
capacity, directory aggregates for named high-value roots, shallow metadata,
and bounded repository-marker discovery. It does not inspect session contents,
scan `/nix/store`, recursively measure `/tmp`, scan all of `/home/li`, or run
cleanup. Figures are allocated directory size (`du`), so hard-link/reflink
sharing can make totals non-additive.

Confidence labels: **measured** is a direct command result; **observed** is
shallow metadata; **inferred** is an interpretation; **unmeasured** was
intentionally deferred under the active low-resource policy.

## Current capacity and measured concentrations

- **Measured:** the `/` ext4 filesystem is 916 GiB total, 683 GiB used (79%),
  with 187 GiB available, sampled at 2026-09-19 10:42 local time.
- **Measured:** repository/worktree roots contain 1,234 working-copy markers:
  `/git` 828 (51 GiB); `/home/li/wt` 393 (97 GiB);
  `/home/li/worktrees` 4 (231 MiB); `/home/li/primary-workspaces` 1
  (165 MiB); `/home/li/primary-worktrees` 8 (780 MiB). These marker counts
  include nested checkouts and do not establish 1,234 distinct repository
  identities. Per-worktree byte size and age are **unmeasured**.
- **Measured, thinking-machine/session state:** `/home/li/.codex` 24 GiB;
  `/home/li/.claude` 1.7 GiB; `/home/li/.pi` 918 MiB;
  `/home/li/.gemini` 818 MiB; `primary/agent-outputs` 146 MiB;
  `primary/sessions` 88 KiB. The named roots may contain configuration,
  caches, plugins, logs, and transcripts; no contents were read.
- **Observed, session-root timeline:** `.codex` has 73 immediate children with
  child mtimes spanning 2026-02-04 13:48 through 2026-09-19 10:44; `.claude`
  has 28 spanning 2026-06-25 11:07 through 2026-09-19 10:43;
  `primary/sessions` has 4 spanning 2026-08-16 through 2026-08-22; and
  `primary/agent-outputs` has 207 spanning 2026-06-28 through 2026-09-15.
  These are directory-entry timelines, not session-file timelines.
- **Measured, other machine-heavy roots:** `.cache` 11 GiB; `.config` 11 GiB;
  `.local` 10 GiB; `.cargo` 2.8 GiB; `.npm` 2.8 GiB; `.bun` 53 MiB;
  `.code-index` 22 MiB; `.emacs.d` 17 MiB; `.m2` 6.5 MiB; `.rustup` 8 KiB.
  These should not be summed with one another or the filesystem figure: some
  may overlap through links or house active data.

## `/tmp`, home structure, and anomalies

- **Observed:** `/tmp` had 11,247 immediate entries and mtime
  2026-09-19 10:43:40 local. Name-only classification found 6,690
  Chromium-named, 301 `nix-`-named, and 1,377 broadly tempish entries.
  Its byte total, ownership, liveness, and nested ages are **unmeasured**;
  none is a deletion candidate without process/owner validation.
- **Observed:** home has several overlapping-looking worktree roots (`wt`,
  `worktrees`, `primary-workspaces`, and `primary-worktrees`) plus `/git`.
  **Inferred:** their collective ~149 GiB is the first high-value mapping
  target, before reclaim actions.
- **Observed:** home also contains many dated Nix-profile link generations and
  several Claude temporary JSON files. Their retention status and reclaimed
  space are **unmeasured**. Do not remove them from this report alone.
- **Unmeasured:** media/personal directories, package/store closure sizes,
  browser profiles, Downloads, build outputs outside the named roots, deleted-
  but-open files, snapshots, and filesystem-reserved space.

## Proposed canonical home-maintenance index

Adopt one committed, privacy-safe index at
`primary/reports/home-maintenance/index.md` with generated measurements kept
under `primary/reports/home-maintenance/snapshots/YYYY-MM-DD.md` (or the
flow's evidence directory until the convention is adopted). The index should
contain only paths, owner/purpose, retention class, measurement method, last
measurement, aggregate allocated bytes, age range, and action authority—never
session text, secrets, or filenames that expose private content.

Suggested top-level sections:

1. **Capacity:** filesystem totals, alert thresholds, and last quiet-period
   scan.
2. **Checkouts:** canonical roots (`/git`, `~/wt`, etc.), marker count,
   aggregate bytes, per-checkout inventory reference, and worktree owner/state.
3. **Agent state:** each harness root, aggregate size, age envelope, and
   declared retention/export policy.
4. **Ephemeral state:** `/tmp`, caches, build artifacts, and a required
   owner/liveness check before any cleanup.
5. **Personal and system state:** media, Downloads, profiles, Nix/system
   references, each deliberately measured separately.
6. **Decisions:** approved cleanup rules, exclusions, evidence, executor,
   and recovery path.

Guideline: measure first; classify ownership and retention; propose a
recoverable action; obtain explicit approval; execute; then remeasure and
record the delta. Never use age alone as deletion authority, and keep active
flow/session directories excluded unless their owner explicitly closes them.

## Deferred quiet-period measurement plan

When the low-resource movie policy is lifted and no builds, browser sessions,
or agent flows are active:

1. Capture `df -hT`, mount metadata, and open-file/deleted-file summary.
2. Produce a per-checkout table from the five discovered roots: canonical path,
   marker type, allocated size, shallow mtime, VCS/worktree status, and owner.
   Deduplicate nested checkout paths before totals.
3. Measure each agent/session root by safe categories (transcripts, caches,
   plugins, logs) without collecting content; record count, bytes, oldest and
   newest mtimes.
4. Inventory `/tmp` by owner, open-process association, top-level allocated
   size, and age buckets; exclude live resources, then seek approval for any
   cleanup.
5. Measure `/nix/store` only via the approved Nix-aware accounting method, and
   separately record profiles, generations, roots, and reclaimable estimate;
   do not treat store bytes as ordinary removable files.
6. Run a bounded, documented home directory size map, then inspect only the
   largest approved candidates. Publish the result to the canonical index and
   compare it with this snapshot.

## Sources

- Local read-only commands run 2026-09-19: `df -hT`; bounded `find` for root
  metadata and VCS markers; named-root `du -sh`; shallow session and `/tmp`
  metadata summaries.
- `/home/li/primary/AGENTS.md`, `NON_MANAGEMENT_AGENTS.md`, and
  `SKILL_VARIABLES.md` for repository-root and operational constraints.
