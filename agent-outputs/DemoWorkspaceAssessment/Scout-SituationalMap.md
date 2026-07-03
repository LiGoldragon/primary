# Scout Situational Map — Abandoned `142204` Demo Workspaces

## Task and scope

Read-only assessment (psyche-directed, NO changes made) of the ~13G directory
`/tmp/criome-mentci-spirit-demo-20260701-142204`, which contains 9 registered
`jj workspace add` workspaces backed by the real fenced component repos. For each
workspace: identify its repo, path, age, uncommitted work, relevance, and any
salvage-worthy ideas. Deliver a per-workspace table plus an overall
discard/salvage/keep recommendation. Assessment only — nothing acted on.

## Commands and files consulted

- `du -sh`, `ls -la`, `find`, `realpath` on the /tmp directory tree.
- `cat` of each workspace's `.jj/repo` pointer file.
- `jj --ignore-working-copy -R <path>` for `workspace list`, `log`, `diff`
  (the `--ignore-working-copy` flag guarantees **no working-copy snapshot** is
  taken into the shared real repos — fully read-only).
- Demo `logs/` and `runtime/` contents under the /tmp dir.
- `rg` over `/git/github.com/LiGoldragon/` and `/home/li/primary/reports/`.

## Observed facts

- Target dir `/tmp/criome-mentci-spirit-demo-20260701-142204` is 13G, owner `li`,
  mtime Jul 1 14:22. Layout: `worktrees/` (the 9 workspaces), `logs/`, `runtime/`.
- The 9 workspaces are `jj workspace add` checkouts. Each `.jj/repo` points back to
  the **real** component repo under `/git/github.com/LiGoldragon/<repo>/.jj/repo`
  (note: `/git` is a real repo root owned by `li`, distinct from `/home/li/git`).
  So these 9 workspaces are registered in the real repos' op logs; deregistering
  them needs `jj workspace forget` in each real repo.
- All 9 carry the identical jj description `demo workspace for criome authorization
  push`. jj workspace names follow `demo-<repo>-20260701-142204`.
- Disk is almost entirely build artifacts: `target/` dirs are 4.2G (mentci) + 3.2G
  (criome) + 3.1G (spirit) + 1.8G (mentci-egui) ≈ 12.3G of the 13G. Actual source
  deltas are kilobytes.
- No source file under any workspace was modified after `2026-07-01 14:44`
  (`find -newermt` returned nothing). The recorded `@` diffs below are the complete
  content. `.jj/working_copy/tree_state` is Jul 1 14:43 (last snapshot); the
  `checkout` pointer file was touched Jul 3 00:22 by a later jj op that did NOT
  re-snapshot (no new work — see Unknowns).
- The `criome-authorization-push` lane is **still active** in the real repos and has
  advanced well past these demo snapshots. Example bookmarks in real `criome`:
  `criome-authorization-push` → `b4af86da criome: enforce SO_PEERCRED owner-auth on
  the meta socket`, plus `criome-auth-integration`, `criome-auto-approve`,
  `criome-peer-transport`, `criome-cluster-witness`. The demo `@` parents were the
  lane tips as of Jul 1 14:22 and are now superseded.
- Demo logs show the run partially failed: `criome-daemon.log` →
  `Error: SignalFrame(ArchiveDeserialize)`; `mentci-criome-pickup-witness.log`
  panicked ("configure criome ClientApproval over meta socket: UnexpectedEof").
- The runnable demo harness script is **not** present in the component repos. The
  demo methodology is referenced only in primary reports
  (`reports/field-readiness/12-run-and-assembly.md`, `13-tooling-field.md` kink K7
  "leftover demo daemons squatting /tmp") which flag a *sibling* run
  `...-150210` (its /tmp dir is already reaped/gone). So this is a repeatable
  harness that leaves throwaway /tmp clutter by design.

## Nature of the uncommitted work

Across the 5 non-empty workspaces the changes are overwhelmingly **local
integration plumbing**, not feature work: git dependencies (`{ git = "…LiGoldragon/
signal-criome", branch = "…" }`) rewritten to local path deps (`{ path =
"../signal-criome" }`), matching `Cargo.lock` `source =` lines dropped, and in
`mentci` a `[patch."https://github.com/LiGoldragon/…"]` block added — all so the
9-repo cluster builds from the co-located /tmp worktrees for one end-to-end demo.
Path-`../` deps to /tmp are inherently un-landable on `main`.

Two small non-plumbing code edits exist, both demo-only:
- `criome/src/bin/criome-client-approval-witness-test.rs`: the approve→Granted /
  reject→Denied lifecycle proof was **deleted** and replaced with a single
  "park for external Mentci approval" assertion. This is a *reduction* of the
  witness; the real lane already has the fuller `criome-client-approval-witness`
  workspace and `criome-auto-approve-witness-test`. A regression, not an upgrade.
- `mentci/src/bin/mentci-criome-pickup-witness-test.rs`: dropped
  `.with_meta_socket_path(&self.meta_socket_path)` from the daemon config. This
  is exactly what the demo log shows **broke** the pickup witness (UnexpectedEof
  panic). A failed experiment.

## Per-workspace table

| Repo | /tmp path (under `worktrees/`) | jj workspace name | @ commit | Age (last snapshot) | Content summary | Relevance verdict | Salvage |
|------|-------------------------------|-------------------|----------|--------------------|-----------------|-------------------|---------|
| criome | `criome/` | `demo-criome-20260701-142204` | `27a89d59` | 2026-07-01 14:43 | Cargo.toml/lock: `meta-signal-criome` + `signal-criome` → path deps; witness test reduced to park-only | Superseded demo plumbing + witness regression | None |
| mentci | `mentci/` | `demo-mentci-20260701-142204` | `7064f9c0` | 2026-07-01 14:43 | 4 deps → path deps + `[patch."…"]` block; pickup witness lost `.with_meta_socket_path` (broke it) | Superseded plumbing + broken experiment | None |
| mentci-lib | `mentci-lib/` | `demo-mentci-lib-20260701-142204` | `b9cbc04a` | 2026-07-01 14:43 | Cargo.toml: `signal-mentci`,`signal-criome`,`meta-signal-criome` → path deps | Superseded demo plumbing | None |
| meta-signal-criome | `meta-signal-criome/` | `demo-meta-signal-criome-20260701-142204` | `47e6de4a` | 2026-07-01 14:43 | Cargo.toml: `signal-criome` (was branch `criome-authorization-push`) → path dep | Superseded demo plumbing | None |
| signal-mentci | `signal-mentci/` | `demo-signal-mentci-20260701-142204` | `50a03628` | 2026-07-01 14:43 | Cargo.toml: `signal-criome` → path dep | Superseded demo plumbing | None |
| mentci-egui | `mentci-egui/` | `demo-mentci-egui-20260701-142204` | `95c363db` | 2026-07-01 14:22 | **Empty** — 0 files changed; 1.8G is `target/` only | Abandoned, no work | None |
| router | `router/` | `demo-router-20260701-142204` | `a10bbf72` | 2026-07-01 14:22 | **Empty** — 0 files changed | Abandoned, no work | None |
| signal-criome | `signal-criome/` | `demo-signal-criome-20260701-142204` | `105a0a92` | 2026-07-01 14:22 | **Empty** — 0 files changed | Abandoned, no work | None |
| spirit | `spirit/` | `demo-spirit-20260701-142204` | `b5fc50af` | 2026-07-01 14:22 | **Empty** — 0 files changed; 3.1G is `target/` only | Abandoned, no work | None |

Absolute paths: workspaces are `/tmp/criome-mentci-spirit-demo-20260701-142204/worktrees/<repo>/`;
backing repos are `/git/github.com/LiGoldragon/<repo>/`.

## Interpretation

- 4 of 9 workspaces (mentci-egui, router, signal-criome, spirit) hold **no work at
  all** — they were created for the cluster demo but nothing was edited.
- The other 5 hold **throwaway local-path integration plumbing** plus two demo test
  edits, one a regression and one a break. None of it is landable or unique.
- The genuine feature work these demos exercised (criome ClientApproval / auth push /
  meta-socket witnesses) lives independently and further-advanced in the real repos'
  `criome-authorization-push`, `criome-auth-integration`, `criome-auto-approve`,
  and `criome-client-approval-witness` bookmarks/workspaces. The /tmp dirs are a
  frozen, partially-broken snapshot of an earlier point on that lane.
- This matches the psyche's belief: abandoned demo scaffolding, not lost work.

## Salvage-worthy ideas

- No code or content in these 9 workspaces is worth salvaging — every non-plumbing
  edit is either a regression (criome witness) or a break (mentci witness), and the
  plumbing is /tmp-specific.
- The one reusable *idea* is the harness pattern itself: a multi-workspace
  local-path-patch integration rig that co-locates the 9 component repos and runs an
  end-to-end criome/mentci authorization demo with witnesses. That pattern is already
  documented in `reports/field-readiness/12-run-and-assembly.md` and flagged (with its
  /tmp-clutter downside) as kink K7 in `13-tooling-field.md`. If the psyche wants it
  durable, the home is a checked-in demo script + a note in the relevant repo/skill —
  but that is a *separate* decision, not something to recover from these dirs.

## Overall recommendation

**Discard all 9.** Nothing to keep, nothing unique to salvage. Concretely:

1. Deregister the 9 workspaces from the real repos (owner action, one per repo):
   `jj workspace forget demo-<repo>-20260701-142204` in each
   `/git/github.com/LiGoldragon/<repo>` — repos: criome, mentci, mentci-egui,
   mentci-lib, meta-signal-criome, router, signal-criome, signal-mentci, spirit.
2. Then remove the /tmp directory `/tmp/criome-mentci-spirit-demo-20260701-142204`
   (reclaims ~13G, ~12.3G of it stale `target/` builds).
3. Separately, the leftover demo daemons/tmux session flagged as K7 in field-readiness
   should be checked before/with cleanup (out of this dir's scope but same demo family).

If the psyche wants the demo methodology preserved, capture the *harness script*
(not these outputs) into a repo — the demo content here adds nothing.

## Checks run and exact result

- 9 workspaces confirmed, each `.jj/repo` resolves to an existing
  `/git/github.com/LiGoldragon/<repo>/.jj/repo`.
- `jj --ignore-working-copy diff -r @`: criome/mentci/mentci-lib/meta-signal-criome/
  signal-mentci show the Cargo + test deltas above; mentci-egui/router/signal-criome/
  spirit report `0 files changed`.
- `jj workspace list` in each real repo shows exactly one `142204` workspace.
- `find -newermt '2026-07-01 14:44'` over non-target source files: empty (no
  post-snapshot edits).

## Blockers, unknowns, not-checked

- **Not checked:** whether the real repos have any *concurrent live* jj operation or
  lock right now; I only ran `--ignore-working-copy` reads, which do not lock the
  working copy. The `jj workspace forget` cleanup is left entirely to the owner.
- **Unknown:** what touched `.jj/working_copy/checkout` on Jul 3 00:22 across all 9
  (pointer updated, `tree_state`/content unchanged). Likely a later jj op in the real
  repos (rebase/abandon of the lane) repointing the stale workspace `@`; it introduced
  no new work. Not material to the discard verdict.
- **Not verified line-by-line:** whether every superseded demo Cargo edit has an exact
  equivalent already on the current lane — unnecessary, since path-`../` deps are
  categorically un-landable regardless.
- **Out of scope but noted:** sibling demo run `...-150210` (its /tmp dir already gone)
  and the leftover demo daemons/tmux (K7) are part of the same demo-clutter family and
  may warrant the same cleanup pass.
