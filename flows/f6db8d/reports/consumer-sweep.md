# Consumer sweep — final producer heads

Subflow of main flow f6db8d, 2026-09-11, thread `f6db8d14-1dfe-472d-914e-9c441f852834`.
Brief: sweep every consumer of protos 0.30.1 (`171b21f6`), datom-codec 0.26.3
(`627db67f`), ethos-zero 8.0.1 (`de3d9928`), signal 3.0.2 (`8f9a0deb`) and
nexus 0.1.1 (`a84bfa96`) to those exact heads, producers before consumers.

**Witnessed** means this flow (or the named subflow it dispatched, reporting
back to it directly) read or ran it. **Relayed** means carried from another
flow's report file without re-observation. Every per-repository repin, gate
and push below was carried out by a dispatched subflow of this flow and is
relayed from that subflow's own report to it; the lock observations, the
producer-head confirmations, and the consumer-list confirmation by grep were
witnessed directly by this flow.

## 1. Producers — already at target, untouched

Witnessed by reading each producer's `origin/main` directly:

| repository | version | revision |
|---|---|---|
| protos | 0.30.1 | `171b21f65337983ab624b7b906397a4f1f92c5a3` |
| datom-codec | 0.26.3 | `627db67f2655efd9f786864009955005fd8ab2ad` |
| ethos-zero | 8.0.1 | `de3d9928b156f2e1a92d060b7817af201abfdbef` |
| signal | 3.0.2 | `8f9a0deb701cebbea518679548df4a795affc918` |
| nexus | 0.1.1 | `a84bfa960c0d5c02d30048c4bbbc67dfef79a67c` |

All five were already exactly at the brief's named heads when this flow
started; no producer repository was touched.

**`signal-standard` is the same underlying remote as `signal`.** Witnessed:
both local clones share commit `2c90fc99` in their history, and
`signal-standard`'s `origin/main` landed at the same final commit `8f9a0deb`,
version 3.0.2, that `signal` carries — the rename recorded in
`reports/datom-migration.md` (item 2) turned out to be a repository rename,
not merely a package-name rename. `signal-standard`'s local ref was stale at
survey time (still showing the pre-repin commit); a fresh fetch showed it
already done. No push was needed from this sweep for `signal-standard`.

## 2. Consumer list — how it was built

Started from the tables in `reports/{datom-migration,orchestrate-work,
dependency-survey}.md`, confirmed by `grep -rl` for git dependencies on
protos/datom-codec/ethos-zero/signal/nexus across every `Cargo.toml` under
`/git/github.com/LiGoldragon/`, witnessed. `orchestrate 'Observe.Locks'` was
run before dispatching any repository, and again as each dependency chain
unblocked, to confirm current lock state.

## 3. Landed on main, full gate green

"Before"/"after" are version and revision. Gate is the full local gate:
`cargo test --all-features`, `cargo fmt --check`, `cargo clippy --all-targets
--all-features -- -D warnings`, `cargo doc --no-deps --all-features`, and
`nix flake check -L --builders ''`, all relayed from the dispatched subflow
that held that repository's Orchestrate lock.

| repository | before | after | gate |
|---|---|---|---|
| signal-terminal | 2.0.0 `b0523f77` | **2.0.1** `bb696365` | green |
| signal-message | 2.0.0 `f03a147c` | **2.0.1** `2da9c6dd` | green |
| signal-persona | 2.0.0 `07494bb2` | **2.0.1** `48118557` | green |
| signal-domain | 2.0.0 `01c73e78` | **2.0.1** `0e3c55bb` | green |
| signal-upgrade | 2.0.0 `e9bffc57` | **2.0.1** `b1bec686` | green |
| clavifaber | 0.4.0 `8fa6dc44` | **0.4.1** `c42010db` | green (ethos-zero not a dependency, direct or transitive; only protos/datom-codec repinned) |
| meta-signal-upgrade | 2.0.0 `83c6cead` | **2.0.1** `a319e1ba` | green |
| signal-spirit | 3.0.0 `c1d78e85` | **3.0.1** `d13ddce` | green (also advanced its `signal-domain` dep to the latter's own landed 2.0.1, needed to clear a duplicate-crate-version compile error; the stale transitive datom-codec 0.25.6 recorded in `reports/datom-migration.md` §5 is now confirmed gone) |
| signal-introspect | 2.0.0 `5b36271` | **2.0.1** `8de16e3` | green (retry; first attempt blocked on signal-persona/signal-message not yet landed, see §5) |
| signal-spirit-judge | 2.0.0 `f9da94e3` | **2.0.1** `5e7764ea` | green (retry; first attempt blocked on signal-spirit not yet landed) |
| meta-signal-spirit | 3.0.0 `9f6c648e` | `6f6c8c0a` | green (retry; first attempt blocked on signal-spirit not yet landed. **Version label left at 3.0.0 despite the repin — a gap in that subflow's versioning step, recorded here rather than silently corrected.**) |
| meta-signal-terminal | 2.0.0 | **2.0.1** `a9b18ee8` | green |
| signal-mirror | 2.0.0 `e6c565ca` | **2.0.1** `e60b7667` | green (stale duplicate protos 0.29.1/0.30.0 and datom-codec 0.25.6/0.26.1 in Cargo.lock, recorded in `reports/datom-migration.md` §5, confirmed gone; `tests/dependency_boundary.rs` hardcoded prior producer versions and was updated to match, since it is text-asserting generated/authored pin values rather than behavior) |
| meta-signal-mirror | 2.0.0 `bdc76bcd` | **2.0.1** `adf6be61` | green (same stale-duplicate defect, same fix; confirmed gone) |

No repository in this sweep required a compatibility path; every fix was a
straight repin, with two second-order pin corrections (signal-spirit →
signal-domain, signal-introspect → signal-persona/signal-message) needed
purely to keep one resolved version of each producer in the graph, per this
flow's ordering rule of producers/contracts before their own consumers.

## 4. Skipped, and the lock that held them

Witnessed via `orchestrate 'Observe.Locks'` at dispatch time:

| repository | lock |
|---|---|
| lojix | 1111 `LojixNexusHardening` (f6db8d) |
| horizon-rs | 1112 `HorizonRsNoFreeFunctions` (f6db8d) |
| aggregator | 1167 `F6db8dNotaPinsAggregator` (f6db8d) |
| router | 1143 `F6db8dNotaPinsRouter` (f6db8d) |
| signal-aggregator, meta-signal-aggregator | 1168 `F6db8dNotaPinsSignalAggregatorDerives` (f6db8d) |
| orchestrate | 853 `OrchestrateDatomSignalMigration` (flow 542442) |
| signal-orchestrate | 854 `SignalOrchestrateDatomSignalMigration` (flow 542442) |
| meta-signal-orchestrate | 855 `MetaSignalOrchestrateDatomSignalMigration` (flow 542442) |
| signal-lojix | 868 `SignalLojixReadOnlyGeneration` (flow 542442, worktree) |
| meta-signal-lojix | 869/870 `MetaSignalLojix*` (flow 542442, worktree) |
| claude-answers | 850 `ClaudeAnswersDatomMigration` (flow 542442) |
| curriculum-deploy | 851 `CurriculumDeployDatomMigration` (flow 542442) |

## 5. Retries within this sweep

Three repositories were dispatched once, hit a real (not spurious)
cross-consumer version conflict caused by sibling repositories in the same
batch not yet having landed, pushed their partial work to `f6db8d-sweep` and
released their lock rather than guessing at an out-of-scope fix, and were
then re-dispatched once their blockers landed:

- **signal-introspect** — blocked on signal-persona and signal-message
  (both pinned old datom-codec/protos), unblocked once both landed 2.0.1.
- **signal-spirit-judge** — blocked on signal-spirit (pinned old
  datom-codec/protos/signal), unblocked once signal-spirit landed 3.0.1.
- **meta-signal-spirit** — blocked on signal-spirit via Cargo's `links =
  "signal"` uniqueness constraint (old signal-spirit required signal 2.0.0,
  conflicting with the newly pinned direct signal 3.0.2), unblocked the same
  way.

All three retries landed green on main; see §3.

## 6. Excluded by the brief, untouched

`spirit`, `mirror`, `chroma`, the kameo fork, CriomOS, CriomOS-home, and
every running service. `signal-mirror` and `meta-signal-mirror` were treated
as in scope — they are separate contract repositories, not the `mirror`
daemon — consistent with `reports/datom-migration.md`'s prior treatment of
the same distinction.

## 7. What remains behind

- **lojix, horizon-rs, aggregator, router, signal-aggregator,
  meta-signal-aggregator** — held by sibling f6db8d subflows for the
  duration of this sweep; not repinned.
- **orchestrate, signal-orchestrate, meta-signal-orchestrate, signal-lojix,
  meta-signal-lojix, claude-answers, curriculum-deploy** — held by flow
  542442 for the duration of this sweep; not repinned.
- **meta-signal-spirit's version label** — landed at `6f6c8c0a` with the
  Cargo.toml carrying the new pins but the crate's own `version` field left
  at 3.0.0, unchanged from before the repin. Recorded rather than corrected
  by this flow, since correcting it now would mean a second push under this
  flow's own judgment about what the dispatched subflow should have done;
  flagged for whoever picks this repository up next.
- **signal-standard / signal package-name collision** — recorded, not
  touched: `signal-standard` (a repository whose Rust package is now named
  `signal`) and the newer `/git/github.com/LiGoldragon/signal` repository
  are, per `reports/datom-migration.md`, a known architectural collision.
  This sweep repinned through it exactly as the earlier flow left it,
  changing nothing about the collision itself.

## Sources

- Brief of main flow f6db8d to this subflow (2026-09-11).
- `/home/li/primary/flows/f6db8d/reports/datom-migration.md`,
  `orchestrate-work.md`, `dependency-survey.md` — read in full, this flow;
  the consumer list and the lock/skip precedent are relayed from them.
- `orchestrate 'Observe.Locks'`, run by this flow before every dispatch and
  again as chains unblocked (witnessed).
- `git log`/`git show` against `origin/main` of protos, datom-codec,
  ethos-zero, signal, nexus, signal-standard — read directly by this flow
  (witnessed) to confirm producer heads and the signal/signal-standard
  identity.
- `grep -rl` for git dependencies on the five producers across
  `/git/github.com/LiGoldragon/*/Cargo.toml` (witnessed).
- Per-repository repin, regeneration check, gate result and push: relayed
  from the dispatched subflow named in §3, each reporting directly to this
  flow.

## 8. Corrected in follow-up

meta-signal-spirit version bumped from 3.0.0 to 3.0.1 at revision 7ba0f82 to account for the dependency repin.
