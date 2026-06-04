---
title: 498/1 - Abandoned and unintegrated work across the persona engine
role: designer
variant: Audit
date: 2026-06-04
topics: [persona-engine, abandoned-work, branches, bookmarks, integration, schema-stack]
description: |
  Ledger of every non-main branch and bookmark across the persona-engine
  repos plus primary. Each item classified INTEGRATE (valuable, land on main
  now), ABANDON (stale/superseded concept branch, safe to delete), or MERGED
  (already an ancestor of main, the bookmark is just clutter). Answers the
  psyche's question: are there abandoned changes not on main I have not
  talked about? The headline: only two branches carry genuine unlanded work
  (both already known and awaiting operator integration); everything else is
  superseded concept-branch noise or already-merged bookmark clutter.
---

# 498/1 - Abandoned and unintegrated work

## Headline for the psyche

There is almost no hidden unintegrated work. The survey across eleven
persona-engine repos plus the `spirit` pilot repo plus primary found
**exactly two branches carrying genuine, fresh, unlanded work** — and both
are already known and queued for operator integration:

1. `designer-strings-at-edges-2026-06-04` in **triad-runtime** (mine;
   operator 304 plans to land it).
2. `spirit-repetition-cleanups` in **persona-spirit** (system-designer
   59's; verified green, awaiting integration).

Everything else divides into two clutter piles: **~40 superseded
late-May designer concept branches** (the exploration that fed the now-
ratified schema stack — the concepts landed on main under different
change-ids, the branches are 40-80 commits behind) and **50 of 63
`push-*` bookmarks in primary that are already ancestors of main**. None
of it is lost work. The action is pruning, not rescue.

## The two INTEGRATE items

### triad-runtime: `designer-strings-at-edges-2026-06-04`

One commit on top of current main (`lylmnozm`, 2026-06-04):
`triad-runtime: witness strings-at-edges trace invariants and name the
apex constraint`. Diffstat: `ARCHITECTURE.md` +26, `INTENT.md` +7,
`tests/trace.rs` +80. Ahead 1, behind 0 — it builds directly on the
current main tip (`lzkpwsky`, "promote triad-engine readability
essence"). Pure docs + trace-invariant tests, zero source-logic risk.
This is the strings-only-at-edges witness work (records 1490/1492/1495)
landed as tests. operator 304 already names it for integration.

Classification: **INTEGRATE** (clean fast-forward-style land, low risk).

### persona-spirit: `spirit-repetition-cleanups`

A three-commit stack on the current main tip (`rpokknqm`, "collect
removal candidates"), all dated 2026-06-04:

- `oysrspyw` — dispatch: dedup five infallible send-error helpers via
  `From<SendError<_, Infallible>>`
- `wyxoonus` — argument: dedup configuration-argument-text into
  `SpiritArgument::into_nota_text`
- `txzuyzzr` — clock: collapse triplicated civil-date into `CivilInstant`
  + `From` projections; retire the `HandoverClock` ZST namespace

Diffstat for the tip alone: `actors/clock.rs` +83, `store.rs` (-71 net),
2 files, 100 insertions / 71 deletions. This is exactly the
repetition-collapse + ZST-namespace-retirement work system-designer 59
reported as verified-green. The local bookmark is at `txzuyzzr` with the
`@git` ref `behind by 2` — meaning the push hasn't caught up to the full
local stack; the operator integrating should land all three commits, not
just the `@git` tip.

Classification: **INTEGRATE** (real cleanup, on current main, verified).

## The ABANDON pile: superseded schema-stack concept branches

These are the late-May designer concept branches the task flagged as
prime suspects. The survey confirms the suspicion: every one forked in
late May and is now **40-80 commits behind main**, because the ratified
schema stack was built on main during June 1-3 (typed symbol paths,
asschema role resolution, the schema-next daemon pilot, transparent-
newtype trace emission). The concepts these branches explored landed on
main under different change-ids. Two spot-checks prove it:

- `schema-rust-next/designer-trace-trait-emit-2026-06-01` (the trace-
  trait emission concept) — main already carries `cf1ed38` "schema-rust:
  emit trace events as transparent newtypes" + `cf9a2cf` "add lifecycle
  trace object names". The concept landed; the branch is behind 19.
- `schema-next/designer-store-prototype` (AsschemaStore prototype) — main
  already carries `84ce382` "schema: persist asschema artifacts in sema
  store" + `3b58cc7` "store asschema roots as direct fields". Landed;
  behind 25.

The full ABANDON ledger (ahead / behind main, by merge-base date):

| Repo | Branch | ahead | behind |
|---|---|---|---|
| schema-next | designer-finish-macro-engine-2026-05-26 | 1 | 77 |
| schema-next | designer-no-free-fns-2026-05-27 | 4 | 77 |
| schema-next | designer-pair-style-namespace-2026-05-27 | 1 | ~77 |
| schema-next | designer-schema-namespace-and-folder-2026-05-27 | 1 | ~77 |
| schema-next | designer-sigil-grammar-2026-05-28 | 1 | 63 |
| schema-next | collections-horizon-2026-05-28 | 4 | 65 |
| schema-next | cross-crate-schema-import | 3 | 65 |
| schema-next | designer-store-prototype | 1 | 25 |
| schema-next | designer-intent-manifestation-2026-05-27 | ~5 | ~77 |
| schema-next | audit-rkyv-enum-wrapping-presumption | 1 | 8 |
| schema-next | designer-schema-daemon-2026-06-02 (divergent) | div | — |
| schema-rust-next | collections-horizon-2026-05-28 | 4 | 77 |
| schema-rust-next | cross-crate-schema-import | 3 | 77 |
| schema-rust-next | designer-emit-to-src-schema-2026-05-27 | 1 | 81 |
| schema-rust-next | designer-intent-manifestation-2026-05-27 | 5 | 81 |
| schema-rust-next | designer-sigil-grammar-2026-05-28 | 2 | 68 |
| schema-rust-next | designer-trace-trait-emit-2026-06-01 | 1 | 19 |
| schema-rust-next | horizon-schema-concept | 1 | 73 |
| schema-rust-next | codec-opt-in-2026-05-30 | 0 | — |
| nota-next | designer-intent-manifestation-2026-05-27 | 4 | 25 |
| nota-next | designer-no-free-fns-2026-05-27 | 1 | 29 |
| nota-next | designer-uniform-body-parser | 1 | 4 |
| nota-next | push-nwroyoormnzt | 0 | 3 |
| signal-frame | designer-schema-poc-from-v0.3-main-2026-05-26 | 2 | 0* |
| signal-frame | designer-schema-poc-106-2026-05-26 | 5 | 0* |
| signal-frame | operator-full-schema-spirit-2026-05-26 | 2 | 0* |
| signal-frame | mockup-stable-caller-id-1 | 1 | 17 |
| signal-frame | signal-frame-executor-report-141 | 1 | 50 |
| signal-frame | wip-observable-grammar | 1 | 51 |
| nota-codec | designer-327-mockup-2-schema-parser | 2 | 8 |
| nota-codec | designer-schema-derived-nota-2026-05-26 | 1 | 0* |
| nota-codec | docs-emit-schema-rename | 1 | 3 |
| nota-codec | intent-roll-forward-2026-05-25 | 1 | 8 |
| nota-codec | nota-codec-intent-synthesis | 1 | 0* |
| persona-spirit | designer-schema-full-stack-spirit-2026-05-25 | 1 | 16 |
| persona-spirit | designer-schema-poc-from-v0.3-main-2026-05-26 | 1 | 11 |
| persona-spirit | operator-full-schema-spirit-2026-05-26 | 1 | 12 |
| persona-spirit | intent-roll-forward-2026-05-25 | 1 | 16 |
| persona-spirit | v010-retrofit-for-sandbox | 2 | 51 |
| sema / sema-engine / persona | docs-emit-schema-rename | 1 | small |
| mind | push-kyoqmnxx | merged | — |
| spirit (pilot) | 14 designer-* concept branches | 1-6 | 19-68 |

The `behind=0*` cases (signal-frame, nota-codec) are not "current" — they
sit on **frozen mains**. `signal-frame` main last moved 2026-05-25;
`nota-codec`, `sema`, `persona`, `mind` mains are all stuck at May 25.
These are the **old hand-written stack** repos, frozen because the
project pivoted to the new schema stack. Their unmerged concept/
ARCHITECTURE branches explore a direction the new stack supersedes —
ABANDON, not INTEGRATE. A `behind=0` against a dead main is not freshness.

The `spirit` pilot repo (the renamed `spirit-next`, main tip 2026-06-03
"spirit-next: add alias payload e2e constraints") carries its own 14
late-May designer concept branches (`designer-fully-working-prototype-
2026-05-27`, `designer-three-engines-origin-route-2026-05-28`,
`daemon-zero-nota-2026-05-30`, etc.), all 19-68 commits behind. Same
verdict: superseded prototype exploration, ABANDON.

## The MERGED / clutter pile: primary push-* bookmarks

Primary has 98 bookmarks total, **63 of them `push-*`**. Of those 63:

- **50 are already ancestors of main** — pure clutter, the push landed
  and the bookmark was never pruned. Safe to delete wholesale.
- **20 entries (some duplicated across local/@origin) are not ancestors**
  — but inspection shows these are old report/doc-shuffle commits from a
  very fast-moving primary main. Sampled cases:
  `push-private-role-reports-2026-06-02` (ahead 1, **behind 96**),
  `push-context-maintenance-33` (ahead 1, **behind 605**),
  `push-operator-report-cleanup-2026-05-18` (ahead 2, **behind 940**),
  `push-working-vision-268` (ahead 2, behind 193). Each carries a single
  report/skill commit whose substance landed on main under a different
  change-id during rebase. The privacy-routing of
  `push-private-role-reports` is already on main (the
  `repos/assistant-reports` / `repos/counselor-reports` symlinks exist;
  `skills/privacy.md` carries the routing). These are **stale bookmarks
  on substance-already-landed commits**, not unintegrated work.

Net: the 63 `push-*` bookmarks are entirely clutter. None needs
integration. The full set should be pruned (one operator bookmark-
cleanup task). The same wholesale-prune applies to the ~40 superseded
concept branches across the engine repos.

## Uncommitted worktree state

None. All persona-engine worktrees under `~/wt/github.com/LiGoldragon/`
(triad-runtime, schema-next, schema-rust-next, nota-next, persona-spirit,
nota-codec, signal-frame, spirit) are clean — `git status --short`
returns empty for each. No uncommitted work is stranded in a worktree.

## On the `spirit` / `spirit-next` rename (record 1588)

Record 1588 says: rename `spirit-next` → `spirit`, delete the stale
`spirit` concept repo. The survey shows the rename has effectively
happened: there is a single `/git/github.com/LiGoldragon/spirit` repo,
its content IS the schema-derived pilot (commits read `spirit-next: ...`,
main tip 2026-06-03, active). There is no separate stale `spirit`
concept repo lingering on disk. What remains is housekeeping: the in-repo
commit-message prefix still says `spirit-next:` and the 14 stale concept
branches inside it want pruning — both minor, both ABANDON-class.

## Ledger summary

- **INTEGRATE (2)**: triad-runtime `designer-strings-at-edges-2026-06-04`;
  persona-spirit `spirit-repetition-cleanups` (all 3 commits). Both
  already known to the operator.
- **ABANDON (~54)**: ~40 superseded schema-stack/old-stack concept
  branches across schema-next, schema-rust-next, nota-next, signal-frame,
  nota-codec, persona-spirit, sema, sema-engine, persona, plus 14 in the
  `spirit` pilot repo.
- **MERGED / clutter (50+)**: 50 of 63 primary `push-*` bookmarks are
  ancestors of main; the other 13 carry substance-already-landed report
  commits. All prunable.
- **No stranded worktree work.**
