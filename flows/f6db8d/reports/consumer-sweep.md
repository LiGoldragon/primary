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

## 8. Corrected in follow-up

meta-signal-spirit version bumped from 3.0.0 to 3.0.1 at revision 7ba0f82 to account for the dependency repin.

## 9. The four consumers this sweep skipped, now repinned

Subflow of main flow f6db8d, 2026-09-11, thread `f6db8d14-1dfe-472d-914e-9c441f852834`
(a distinct dispatch of this same subflow thread from §1-§8). Brief: repin
`signal-orchestrate`, `meta-signal-orchestrate`, `orchestrate` and
`claude-answers` — the four repositories §4 recorded as skipped for held
locks — to the same final producer heads as the rest of this sweep, contracts
before `orchestrate`, then `claude-answers`, regenerating each repository's
ethos-zero-derived contract and recording whether it came back byte-identical.

**Lock state at dispatch, witnessed.** `orchestrate 'Observe.Locks'`, run by
this thread before dispatching any repository, still showed all four locks
named in §4 (850 `ClaudeAnswersDatomMigration`, 853
`OrchestrateDatomSignalMigration`, 854 `SignalOrchestrateDatomSignalMigration`,
855 `MetaSignalOrchestrateDatomSignalMigration`, all flow 542442) as held —
**not released**, contrary to this dispatch's own brief, which stated they
had been. This is recorded as an observation against the brief's premise, not
smoothed over. Each of those four locks' paths is a worktree path under
`/home/li/wt/github.com/LiGoldragon/<repo>/...-542442`, distinct from the
repository's real path under `/git/github.com/LiGoldragon/<repo>`, which
`reports/orchestrate-followup.md` §8 had already shown does not conflict —
that thread took and released lock 1169 directly over the real paths of
`orchestrate`, `signal-orchestrate` and `meta-signal-orchestrate` while these
same four locks sat unreleased. This dispatch took its own lock over each
real repository path the same way, once per repository
(`SignalOrchestrateFinalRepin` 1198, `MetaSignalOrchestrateFinalRepin` 1200,
`OrchestrateFinalRepin` 1201, `ClaudeAnswersFinalRepin` 1199 first attempt,
1199 was released and taken as a fresh id on retry — see below), and none
was refused.

**A git-remote defect caught mid-sweep, corrected, witnessed directly.** The
first dispatched attempts at `signal-orchestrate` and `claude-answers` each
cloned with `git clone --shared /git/github.com/LiGoldragon/<repo> ...`,
which repoints the clone's `origin` remote at the local checkout path rather
than GitHub; both attempts ran a full gate green, committed, "pushed", and
reported success, but the push had only moved the local checkout's own
`main` branch ref — GitHub's real `main` had not moved. This thread caught
it by fetching each repository's real `origin/main` directly
(`git fetch origin main`, `git ls-remote git@github.com:LiGoldragon/<repo>.git
main`) rather than trusting the subflows' claims, found the mismatch, reset
the two polluted local `main` refs back to real GitHub's state
(`git update-ref refs/heads/main refs/remotes/origin/main`), and re-dispatched
both with corrected instructions: clone directly from the real
`git@github.com:LiGoldragon/<repo>.git` remote, and confirm every push
afterward with `git ls-remote` against that same URL before reporting
success. Every repository in this section's table was re-verified against
`git ls-remote` on the real GitHub remote by this thread directly, and
against the version string read at that exact commit via
`git show <sha>:Cargo.toml`, independent of the dispatched subflows' own
claims.

**Order and dependency chain, as executed.** `signal-orchestrate` (a
contract), then `meta-signal-orchestrate` (a contract, depends on
`signal-orchestrate`), then `orchestrate` (depends on both contracts, plus
`nexus`, left untouched at its already-final `a84bfa96`/0.1.1), each
dispatched only once its dependency had landed and its new revision was
confirmed; `claude-answers` has no dependency on any of the other three and
was dispatched independently, in parallel with the chain.

**Ethos-zero contract regeneration, relayed then spot-confirmed on the
independent evidence each subflow reported:** every one of the four
repositories regenerates its ethos-derived contract at build time via a
`build.rs` that asserts the regenerated output against the committed
generated module (`src/generated/signal.rs` in the two Signal contracts,
`src/generated/client.rs` in both `orchestrate` and `orchestrate-meta`,
`src/generated.rs` via a `tests/regeneration.rs` in `claude-answers`), so a
non-identical regeneration would have failed that repository's own gate
rather than needing a separate diff. Each subflow additionally ran a manual
`git diff`/`diff` against a pre-edit copy and reported no difference. All
four came back byte-identical under ethos-zero 8.0.1.

| repository | before | after | version | ethos-zero regen | gate |
|---|---|---|---|---|---|
| signal-orchestrate | 3.0.1 `45ff2d4` | **3.0.2** `e722119` | 3.0.1 → 3.0.2 | byte-identical | green (test, fmt, clippy -D warnings, doc, `nix flake check`) |
| meta-signal-orchestrate | 3.0.1 `969c7d2` | **3.0.2** `4279ad0` | 3.0.1 → 3.0.2 | byte-identical | green |
| orchestrate | 0.33.0 `3926ba3` | **0.33.1** `c8a2882` | 0.33.0 → 0.33.1 | byte-identical (both `orchestrate` and `orchestrate-meta` generated clients) | green (`checks.peer-authority`'s known sandbox limitation from `orchestrate-followup.md` §3 recurred and is not a gate failure; `nexus` pin left untouched at `a84bfa96`/0.1.1, confirmed) |
| claude-answers | 0.7.0 `cf12437` | **0.7.1** `0f857a3` | 0.7.0 → 0.7.1 | byte-identical | green |

All four revisions above are the exact `git ls-remote
git@github.com:LiGoldragon/<repo>.git main` result read directly by this
thread, and the version at each is the exact string read directly by this
thread from `git show <sha>:Cargo.toml` at that commit — not relayed from
the dispatched subflows' own claims, though those claims agree. Pins landed
on all four: protos 0.30.1 `171b21f6`, datom-codec 0.26.3 `627db67f`,
ethos-zero 8.0.1 `de3d9928`, signal 3.0.2 `8f9a0deb` (signal-orchestrate,
meta-signal-orchestrate, orchestrate only — `claude-answers` does not depend
on signal); `orchestrate` additionally carries signal-orchestrate 3.0.2
`e722119` and meta-signal-orchestrate 3.0.2 `4279ad0`.

Version-label convention (patch bump, commit-message-only record, no
UPGRADES.md entry for a pure repin) was followed per each repository's own
precedent except `orchestrate`, whose own `UPGRADES.md` already carries an
entry for every past pure-pin bump (0.28.0→0.29.0, 0.29.0→0.29.1) — this
repin's entry follows that repository's convention, not the others'.

All four Orchestrate Locks taken by this dispatch were released after their
push was confirmed; `orchestrate 'Observe.Locks'`, re-run by this thread
after all four landed, shows none of the four still held. The four
`...DatomSignalMigration`/`ClaudeAnswersDatomMigration` locks from flow
542442 named above were left exactly as found — this thread neither released
nor otherwise touched a lock it did not itself take.

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
- §9: `reports/orchestrate-followup.md` §2, §3 and §8 — read in full, this
  thread, for the peer-authority sandbox limitation and the worktree-vs-real-
  path lock precedent. `orchestrate 'Observe.Locks'` — run by this thread
  before every dispatch (witnessed), showing locks 850/853/854/855 still
  held contrary to this dispatch's brief. Four dispatched subflows'
  final reports (`signal-orchestrate`, `meta-signal-orchestrate`,
  `orchestrate`, `claude-answers` repins), each reporting directly to this
  thread — relayed for the gate detail and regeneration mechanism inside
  each repository, but every before/after revision, version string and
  final lock state in §9's table was independently re-witnessed by this
  thread via `git fetch`/`git ls-remote`/`git show` against each real GitHub
  remote, not merely relayed.
