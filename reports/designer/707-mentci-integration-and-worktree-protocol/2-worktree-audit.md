# Stream B — Worktree Audit + Proposed GC Manifest

Non-destructive read-only audit of every worktree under
`/home/li/wt/github.com/LiGoldragon/<repo>/<name>/`. Nothing was deleted,
archived, rebased, committed, or otherwise mutated. The output is a
classification table plus a concrete GC-manifest format and its proposed
initial content. The four worktrees holding unique unpushed work are
flagged prominently as must-not-lose.

## Method and the jj working-copy caveat

For each worktree I ran read-only `jj` (`--ignore-working-copy` to avoid
snapshotting) or `git` (for the five plain-git worktrees) and determined:
repo, bookmark/branch, path, merged-to-`main@origin`, commits ahead of
main, whether those commits are pushed to a remote, working-copy dirtiness,
last activity, and evident purpose. The orchestrate `*.lock` files give the
current per-lane claims; I never classify another lane's active worktree as
anything but KEEP-ACTIVE.

One caveat shaped the whole audit. In jj the working copy `@` is itself a
commit, so `jj status`'s "Working copy changes" is the diff of `@` against
its parent — committed content, not uncommitted divergence. Several
worktrees first looked "dirty" (e.g. `criome-client-approval-witness`) but
the `@` commit id equals `@origin` exactly (`2bb8645e`) with a zero tree
diff: clean and pushed. The correct must-not-lose test is therefore "does
the current commit have content not reachable from any remote bookmark",
computed as `(main@origin..@ & ~empty()) ~ ::(remote_bookmarks())`.

## Current lane claims (orchestrate/*.lock)

| Lane | Claimed repos | Reason |
|---|---|---|
| system-designer | CriomOS, clavifaber, goldragon, lojix, meta-signal-lojix, signal-lojix | prometheus VmHost+TestVm + lojix live deploy chain (psyche override) |
| system-maintainer | signal-spirit, spirit | fix spirit nix build + land import bypass |
| cloud-maintainer | cloud | fix DigitalOcean gopass credential path |
| cloud-operator | CriomOS-test-cluster | pan-cluster domain configuration consumer update |

All other lane locks are empty. Note cloud-designer's lock is empty yet its
five `cloud-node-*` git worktrees were all touched 3-18 hours ago — an
active multi-repo feature between sessions, not abandoned.

## MUST-NOT-LOSE — unique unpushed work (4 worktrees)

These hold non-empty commits reachable from no remote bookmark. A GC pass
must NOT touch them until the work is pushed or captured.

| Worktree | Unpushed commit(s) | Disposition |
|---|---|---|
| `CriomOS/prometheus-vm-host` | `92b5d6f6` reconcile VM-host modules: drop dead vm-testing, keep typed test-vm-host | Overlaps the pushed `enable-vm-hosting-prometheus` superset; under system-designer's CriomOS claim. KEEP-ACTIVE, must-not-lose. |
| `goldragon/prometheus-vm-host` | `b9d1ddca` enable VM hosting on prometheus + add durable TestVm node | datom.nota change; under system-designer's goldragon claim. KEEP-ACTIVE, must-not-lose. |
| `schema-rust-next/reaction-expand` | `8b147fac` thread shape resolver + standard struct impls; `a1582dfd` 660/661 composition prototype | No bookmark, no claim. RECYCLE-or-capture, must-not-lose. |
| `schema-rust-next/structural-forms-integration` | `a0138ce1` migrate fixtures to positional struct-body syntax | No bookmark (the `structural-forms-integration` bookmark here is DIVERGED: `@origin` ahead 5 / behind 5). No claim. RECYCLE-or-capture, must-not-lose. |

The two `schema-rust-next` cases are the most exposed: detached commits, no
owning lane, and one sits on a diverged bookmark. They need a push or a
report-capture before any GC.

## Full classification table

Status legend: MERGED (ancestor of `main@origin`, safe to dismantle),
ARCHIVE (pushed/unique-captured but unmerged or stale; record then dismantle
later), RECYCLE (rebase on main, reuse for the new mentci work),
KEEP-ACTIVE (in-flight this session or under a current lane claim).

### criome (designer E1 wave — KEEP-ACTIVE cluster)

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| criome-peer-transport | criome-peer-transport | 2 ahead, pushed-sync, clean | KEEP-ACTIVE | `081f6f7c` @origin in sync; E1 increment 3 hardening, last 2026-06-20 16:55 — active designer E1 work |
| criome-client-approval-witness | criome-client-approval-witness | 1 ahead, pushed-sync, clean | KEEP-ACTIVE | `@`=`@origin`=`2bb8645e`, zero tree diff; report-705 witnesses, last 2026-06-20 |
| attested-moment-majority-guard-139 | attested-moment-majority-guard-139 | 1 ahead, pushed-sync | ARCHIVE | `ed2f3b5d` @origin in sync; fork-safe majority guard, last 2026-06-18 — pushed, unmerged, stale |
| cluster-root-admission-ceremony | cluster-root-admission-ceremony | 1 ahead, pushed-sync | ARCHIVE | `6ab6a4c2` @origin in sync; admission ceremony, last 2026-06-18 — pushed, unmerged, stale |
| criome-nixos-module-142 | criome-nixos-module-142 | 1 ahead, pushed-sync | ARCHIVE | `61768bec` @origin in sync; criome.nix module, last 2026-06-19 — pushed, unmerged, stale |
| criome-cluster-witness | (none) | detached `3850ece3`, not on remote, net-deletions vs main | ARCHIVE (stale orphan) | older E1-transport snapshot superseded by main (`68b92c66` landed client-approval witnesses on top); diff is mostly deletions = behind main. No unique unpushed work but no bookmark — confirm before dismantle. |

### signal-criome / meta-signal-criome (criome triad)

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| signal-criome/signal-criome-peers | signal-criome-peers | 2 ahead, pushed-sync | KEEP-ACTIVE | pushed in sync, last 2026-06-20 — paired with active criome-peer-transport E1 |
| signal-criome/criome-meta-authz | (workspace on `main`) | bookmark `main`=`ff9ac192` parked authz surface | MERGED | landed on main; detached workspace, no unique work |
| meta-signal-criome/criome-meta-authz | (workspace on `main`) | bookmark `main`=`4940e4b1` parked-authz approval surface | MERGED | landed on main; detached workspace, no unique work |

### router / signal-router / signal-standard (transport 138/139 wave)

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| router/transport-yggdrasil-l2-142 | transport-yggdrasil-l2-142 | 5 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-19 — newest transport branch, likely supersedes 138 siblings |
| router/transport-two-kernel-e2e-138 | transport-two-kernel-e2e-138 | 4 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 — superseded by 142 |
| router/transport-p1-fixes-138 | transport-p1-fixes-138 | 2 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 — superseded by 142 |
| router/attendance-fanout-139 | attendance-fanout-139 | 2 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 |
| signal-router/attendance-fanout-139 | attendance-fanout-139 | 2 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 — paired with router |
| signal-router/attendance-fanout-139-compat | attendance-fanout-139-compat | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 — compat sibling |
| signal-standard/attendance-fanout-139 | attendance-fanout-139 | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-18 |
| signal-standard/main | signal-standard-bootstrap | merged, local-only bookmark | MERGED | bookmark is ancestor of `main@origin`; bootstrap landed |

### schema-next / schema-rust-next / sema-engine / structural-forms wave

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| schema-next/impl-reference-syntax | next/impl-reference-syntax | merged, pushed-sync | MERGED | bookmark ancestor of `main@origin`, last 2026-06-19 |
| schema-next/structural-forms-integration | structural-forms-integration | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-16 |
| schema-rust-next/family-identity-newtype | next/family-identity-newtype | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-15 |
| schema-rust-next/reaction-expand | (none) | 2 non-empty ahead, NOT on remote | RECYCLE — MUST-NOT-LOSE | `8b147fac`+`a1582dfd` unique unpushed, last 2026-06-16 |
| schema-rust-next/structural-forms-integration | (none; bookmark DIVERGED) | 1 non-empty ahead, NOT on remote | RECYCLE — MUST-NOT-LOSE | `a0138ce1` unique unpushed; `structural-forms-integration@origin` ahead5/behind5, last 2026-06-16 |
| sema-engine/structural-forms-integration | structural-forms-integration | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-14 — oldest structural-forms branch |
| signal-spirit/structural-forms-integration | (none) | `@` ON remote, 0 unique unpushed | ARCHIVE | content pushed under a remote bookmark; signal-spirit under system-maintainer claim → KEEP-ACTIVE while claimed |
| spirit/structural-forms-integration | (none) | `@` ON remote, 0 unique unpushed | ARCHIVE | content pushed; spirit under system-maintainer claim → KEEP-ACTIVE while claimed |
| meta-signal-spirit/structural-forms-integration | (none; bookmark elsewhere) | `@` ON remote (`c67ecd52`), 0 unique unpushed | ARCHIVE | work pushed; `structural-forms-integration` bookmark points at `vywlqxxq` |

### spirit (build-fix — system-maintainer claim)

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| spirit/build-fix | (none) | `@`=`66e6d674` empty desc, 0 non-empty ahead, not on remote | KEEP-ACTIVE | spirit under system-maintainer's active "fix spirit nix build" claim, last 2026-06-20 — empty scratch change, leave to the lane |

### cloud / CriomOS / goldragon / horizon-rs (cloud-node + VM-host waves)

| Worktree | Branch/Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| cloud/do-deploy-test (git) | cloud-designer-do-deploy-test | 2 ahead, pushed (origin/...), clean | KEEP-ACTIVE | last commit 6h ago; cloud-designer active multi-repo feature |
| cloud/intent-refresh (git) | cloud-designer-intent-refresh | 3 ahead, pushed, clean | KEEP-ACTIVE | last 18h ago; cloud-designer |
| CriomOS/cloud-node-image (git) | cloud-designer-cloud-node-image | 3 ahead, pushed, clean | KEEP-ACTIVE | last 4h ago; cloud-designer |
| goldragon/cloud-node-data (git) | cloud-designer-cloud-node-data | 4 ahead, pushed, clean | KEEP-ACTIVE | last 3h ago; cloud-designer |
| horizon-rs/cloud-node-species (git) | cloud-designer-cloud-node-species | 2 ahead, pushed, clean | KEEP-ACTIVE | last 3h ago; cloud-designer |
| cloud/digitalocean-provider (jj) | digitalocean-provider | merged, local-only bookmark | MERGED | bookmark ancestor of `main@origin`; @origin deleted after merge |
| cloud/hetzner-compute (jj) | hetzner-compute | 0 unique, local-only | MERGED/ARCHIVE | bookmark content on remote; last 2026-06-18 |
| signal-cloud/digitalocean-provider | digitalocean-provider | merged, local-only | MERGED | ancestor of `main@origin` |
| signal-cloud/hetzner-compute | hetzner-compute | merged, pushed-sync | MERGED | ancestor of `main@origin`, last 2026-06-17 |
| meta-signal-cloud/digitalocean-provider | digitalocean-provider | merged, local-only | MERGED | ancestor of `main@origin` |
| meta-signal-cloud/hetzner-compute | hetzner-compute | `@` ancestor of a remote bookmark, 0 unique | MERGED/ARCHIVE | content on remote, last 2026-06-18 |
| CriomOS/enable-vm-hosting-prometheus | enable-vm-hosting-prometheus | 3 ahead, pushed-sync | KEEP-ACTIVE | under system-designer CriomOS claim (prometheus VmHost), last 2026-06-19 |
| CriomOS/prometheus-vm-host | (none) | 1 unique unpushed | KEEP-ACTIVE — MUST-NOT-LOSE | `92b5d6f6` not on remote; under system-designer CriomOS claim |
| goldragon/enable-vm-hosting-prometheus | enable-vm-hosting-prometheus | merged, pushed-sync | MERGED | ancestor of `main@origin`, last 2026-06-19 |
| goldragon/prometheus-vm-host | (none) | 1 unique unpushed | KEEP-ACTIVE — MUST-NOT-LOSE | `b9d1ddca` not on remote; under system-designer goldragon claim |
| CriomOS-home/spirit-bypass | criomos-home-spirit-bypass | 1 ahead, pushed-sync | ARCHIVE | pushed, unmerged, last 2026-06-20 |
| CriomOS-test-cluster/criome-cluster-test | criome-cluster-test | 6 ahead, pushed-sync | KEEP-ACTIVE | under cloud-operator CriomOS-test-cluster claim, last 2026-06-20 |

### lojix (system-designer claim)

| Worktree | Bookmark | State | Class | Evidence |
|---|---|---|---|---|
| lojix/live-deploy-test-chain | live-deploy-test-chain | 2 ahead, pushed-sync | KEEP-ACTIVE | under system-designer lojix claim, last 2026-06-19 |

### Stale empty parent directories (not worktrees)

`/home/li/wt/github.com/LiGoldragon/nota-next/` and `.../upgrade/` are empty
directories — no worktree inside. Leftover scaffolding to remove in the GC
pass (no VCS state, nothing to lose).

## Classification summary

| Class | Count | Worktrees |
|---|---|---|
| MERGED (safe to dismantle now) | 9 | cloud×1, signal-cloud×2, meta-signal-cloud×2, goldragon/enable-vm-hosting, signal-standard/main, schema-next/impl-reference-syntax, signal-criome+meta-signal-criome criome-meta-authz |
| ARCHIVE (pushed/captured, dismantle later) | ~16 | criome ×3 + cluster-witness orphan, router/signal-router/signal-standard transport+fanout ×7, schema-next + schema-rust-next/family + sema-engine structural ×3, spirit/signal-spirit/meta-signal-spirit structural ×3, CriomOS-home/spirit-bypass |
| RECYCLE — MUST-NOT-LOSE | 2 | schema-rust-next/reaction-expand, schema-rust-next/structural-forms-integration |
| KEEP-ACTIVE | ~16 | criome E1 ×2, signal-criome-peers, cloud-designer git ×5, system-designer CriomOS/goldragon/lojix incl. 2 must-not-lose prometheus-vm-host, system-maintainer spirit/signal-spirit/spirit-build-fix, cloud-operator criome-cluster-test |

## Proposed GC manifest

### Where it lives

`/home/li/primary/orchestrate/worktrees.nota` — a single NOTA file in the
orchestrate directory, alongside the `*.lock` files, version-controlled on
primary's main. It is the durable, harness-independent record the kb4k /
eh5a principle requires: agents register every worktree here on creation
and a periodic GC pass reads it to dismantle safely. It is the file-shaped
precursor to the Stream C typed `persona-orchestrate` registry — when the
typed lane registry (w190/tz5j/udgu) absorbs worktree lifecycle, this NOTA
file is its seed/import source and the format maps field-for-field onto the
typed `Worktree` record. Until then the NOTA file is authoritative and the
GC pass and the orchestrate shim both read it.

### Record format (positional NOTA, one per worktree)

```
;; orchestrate/worktrees.nota — worktree registry + GC manifest
;; (Worktree repo branch path owning-lane status purpose last-activity pushed)
;; status ∈ Merged | Archive | Recycle | KeepActive
;; pushed ∈ Pushed | Unpushed | LocalOnly | NoRemote
(Worktrees
  (Worktree criome criome-peer-transport [/home/li/wt/github.com/LiGoldragon/criome/criome-peer-transport] designer KeepActive [E1 increment 3 peer transport hardening] 2026-06-20 Pushed)
  (Worktree schema-rust-next reaction-expand [/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand] none Recycle [shape resolver + 660/661 composition prototype] 2026-06-16 Unpushed)
  (Worktree CriomOS prometheus-vm-host [/home/li/wt/github.com/LiGoldragon/CriomOS/prometheus-vm-host] system-designer KeepActive [reconcile VM-host modules — drop dead vm-testing] 2026-06-19 Unpushed))
```

Positional, no labels (per the NOTA hard override). Branch sits at the
`String` position; a detached/no-bookmark worktree uses the bare atom
`none` so the GC pass treats it as bookmark-less and refuses to delete a
branch that does not exist. `pushed` is the GC safety gate: a record marked
`Unpushed` is never auto-dismantled.

### Proposed initial archive set (the dismantle-later list)

The GC pass may safely delete the branch + tree for every `Archive` and
`Merged` row above once recorded. Concretely the first archive batch:

```
(Worktree cloud digitalocean-provider [.../cloud/digitalocean-provider] cloud-maintainer Merged [DO compute provider Phase 1] 2026-06-19 LocalOnly)
(Worktree signal-cloud digitalocean-provider [.../signal-cloud/digitalocean-provider] none Merged [DO provider signal] 2026-06-19 LocalOnly)
(Worktree signal-cloud hetzner-compute [.../signal-cloud/hetzner-compute] none Merged [hetzner compute signal] 2026-06-17 Pushed)
(Worktree meta-signal-cloud digitalocean-provider [.../meta-signal-cloud/digitalocean-provider] none Merged [DO provider meta] 2026-06-19 LocalOnly)
(Worktree meta-signal-cloud hetzner-compute [.../meta-signal-cloud/hetzner-compute] none Merged [hetzner compute meta] 2026-06-18 LocalOnly)
(Worktree goldragon enable-vm-hosting-prometheus [.../goldragon/enable-vm-hosting-prometheus] system-designer Merged [vm hosting + TestVm datom] 2026-06-19 Pushed)
(Worktree signal-standard main [.../signal-standard/main] none Merged [signal-standard bootstrap] 2026-06-18 LocalOnly)
(Worktree schema-next impl-reference-syntax [.../schema-next/impl-reference-syntax] none Merged [impl reference syntax] 2026-06-19 Pushed)
(Worktree signal-criome criome-meta-authz [.../signal-criome/criome-meta-authz] none Merged [parked authz surface] 2026-06-20 Pushed)
(Worktree meta-signal-criome criome-meta-authz [.../meta-signal-criome/criome-meta-authz] none Merged [parked authz approval] 2026-06-20 Pushed)
(Worktree router transport-two-kernel-e2e-138 [.../router/transport-two-kernel-e2e-138] none Archive [transport two-kernel e2e, superseded by yggdrasil-l2-142] 2026-06-18 Pushed)
(Worktree router transport-p1-fixes-138 [.../router/transport-p1-fixes-138] none Archive [transport p1 fixes, superseded by 142] 2026-06-18 Pushed)
(Worktree sema-engine structural-forms-integration [.../sema-engine/structural-forms-integration] none Archive [structural-forms, oldest of the wave] 2026-06-14 Pushed)
```

The full Archive set is every `Archive`/`Merged` row in the table. The
`criome/criome-cluster-witness` orphan and the three `*spirit*` structural
no-bookmark trees go in Archive but with `pushed=Pushed`/`none` annotated so
GC checks they carry no unique work before deleting the (possibly absent)
branch.

### GC pass contract

1. Read `worktrees.nota`. For each `Archive`/`Merged` row, re-verify live
   (`(main@origin..@ & ~empty()) ~ ::(remote_bookmarks())` is empty AND
   working copy clean) before deleting — never trust the manifest blindly.
2. Refuse any row with `status=KeepActive`, `pushed=Unpushed`, or a path
   whose repo appears in a current `*.lock` claim.
3. Delete the jj/git worktree + local branch; leave pushed remote branches
   for a separate remote-prune decision.
4. Remove the empty `nota-next/` and `upgrade/` parent dirs.

### Relation to Stream C registry

`worktrees.nota` is the manifest leg of the same registry Stream C designs
as a typed `persona-orchestrate` table. The NOTA record maps onto the typed
`Worktree` row one-to-one; the migration imports this file. Lane-claim locks
(`*.lock`) and this worktree manifest are the two halves of orchestrate
state that w190/tz5j/udgu fold into the typed component — keep them adjacent
in `orchestrate/` so the move takes them together.
