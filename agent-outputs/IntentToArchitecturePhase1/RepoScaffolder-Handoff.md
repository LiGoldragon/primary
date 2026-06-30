# Intent-to-Architecture Phase 1 — Per-Repo Fold Handoff

## Task and scope

Phase 1 fan-out of a psyche-locked per-repo doctrine campaign: eliminate
`INTENT.md` from each repo and move its durable direction into `ARCHITECTURE.md`
(per the `repo-intent` doctrine — a repo's direction lives in `ARCHITECTURE.md`
or a code stub, read on entry before code; there is no per-repo `INTENT.md`).

Repos processed (exactly these eight, each an independent git+jj checkout with
its own remote, at `/home/li/primary/repos/<name>`):
chroma, chronos, criome, forge, harness, introspect, message, mind.

## Outcome — all eight complete, verified, pushed

Ground-truth verification (authoritative, run after all work landed):

- All 8 `INTENT.md` files are deleted.
- For every repo `main == main@origin` (every push reached origin; no unpushed
  sibling left behind).
- Zero leftover `INTENT` references in any tracked `*.md` across all 8 repos.

| Repo | Pre-flight VCS | ARCHITECTURE | Pointers retargeted | INTENT deleted | main commit (change-id) | Push |
|---|---|---|---|---|---|---|
| chroma | clean (`@` empty on main, main==origin) | folded | 0 | yes | `vzsyqysl` | landed (FF) |
| chronos | clean | folded; delete commit | 0 | yes | `klrtqzst` | landed (FF) |
| criome | divergent parent — REBASED onto main first | folded | 5 | yes | `mrzsuyux` (b996f937) | landed (FF) |
| forge | clean | delete-only (redundant) | 0 | yes | `ypmtrluu` | landed (FF) |
| harness | clean | folded | 0 | yes | `ksmuvnot` | landed (FF) |
| introspect | clean | folded | 0 | yes | `mlnymtxr` | landed (FF) |
| message | divergent parent (`@` on stale `main@git`, 3 behind real main) — REBASED first | delete-only (redundant) | 0 | yes | `xxtwmrrq` | landed (FF) |
| mind | clean | folded | 0 | yes | `wvosvymo` | landed (FF) |

## VCS gate — the two flagged divergent repos (the trap the brief warned of)

- **criome**: `@` (empty) sat on `criome-authorization-push`, 5 commits ahead of
  `main`; `main == main@origin`. Committing there and setting `main = @-` would
  have swept 5 foreign branch commits forward and pushed a sibling. Resolution:
  `jj rebase -r @ -d main` reparented `@` directly onto `main` BEFORE editing.
  Result: the INTENT-fold commit `mrzsuyux` is a clean child of `main`; push was a
  fast-forward ("Move forward bookmark main 3a13a3d3 → b996f937"); the
  `criome-authorization-push` bookmark (vzztxuuw) is intact and untouched.
- **message**: `@` (empty) sat on the STALE `main@git` (klwloqwy), 3 commits
  *behind* the real `main`/`main@origin` tip (wlurukuo). Committing and setting
  `main = @-` would have rolled `main` back 3 commits and produced a
  non-fast-forward push that drops newer work. Resolution: rebase `@` onto the
  real `main` tip first. Verified after the fact: the delete commit `xxtwmrrq`
  now sits directly on top of `wlurukuo`, which sits on `mutzkowpltmq` then
  `syqvryqz` — all three previously-ahead commits preserved as ancestors of
  `main`; `nota-dependency-rename` bookmark intact at syqvryqz.

The six clean repos had `@` empty and parented on `main` with `main == main@origin`;
no rebase needed.

## criome fold content (the one repo needing real new prose)

criome's `ARCHITECTURE.md` already carried nearly all INTENT substance. Two
gaps were closed and five pointers retargeted in commit `mrzsuyux`:

- Made the "Scope: today, not eventually" note self-contained (it had delegated
  the full statement to `INTENT.md §"Why this repo exists"`); now references
  `~/primary/ESSENCE.md §"Today and eventually"` directly.
- Added to §6.1 the **peer-discovery / node-indexing forward-want** (Spirit
  `burk`): criome daemons are meant to gain peer discovery and node indexing so
  a first daemon can discover a second; hardwiring peer addresses is acceptable
  now; automatic discovery/indexing is a later slice — distinct from the
  existing predictable-socket-name routing of an already-registered peer.
- Retargeted 5 `INTENT.md` pointers → `ARCHITECTURE.md`: ARCHITECTURE.md (scope
  note and See-also) ×2, skills.md (today-vs-eventually ×2, See-also ×1).

For the other repos the fold was either already-present direction confirmed in
`ARCHITECTURE.md` (chroma, chronos, harness, introspect, mind) or fully redundant
INTENT → delete-only (forge, message). No external on-entry pointers to
`INTENT.md` existed in any repo except criome.

## Secrets

None. All eight `INTENT.md` files were design prose only. criome (signatures,
keys, auth) was scanned specifically: only conceptual mentions ("master key",
"passphrase" as a design concept), no concrete key values, tokens, or secret
file paths. Nothing redacted or propagated.

## Repos skipped

None — all eight processed and landed.

## Notes and follow-up

- **Parallel-worker collision (resolved, no damage)**: this session dispatched
  per-repo workers; one worker reported it could not itself fan out (a forked
  worker cannot spawn sub-forks) and so processed all eight repos sequentially.
  The lead handled criome and message directly with the rebase gate. Final
  ground-truth verification confirms a single coherent result per repo — no
  duplicate siblings, no dropped commits, all pushes landed. The lead's criome
  commit `mrzsuyux` is the live one and contains the intended fold.
- **Follow-up for the campaign owner**: confirm whether the dispatcher expected
  eight independent sub-forks; the fork-cannot-spawn-fork constraint changed the
  execution shape (it did not change the result). Worth noting before any
  Phase 2 fan-out that relies on nested forks.
