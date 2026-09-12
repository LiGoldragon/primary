# Push verification — every release and branch claimed tonight, against real GitHub

Subflow of main flow f6db8d, thread `f6db8d14-1dfe-472d-914e-9c441f852834`,
2026-09-11/12. Read-only: no repository was fetched into, edited, locked or
pushed; this file is this subflow's only write.

Occasion: one subflow tonight discovered that `git clone --shared
<local-checkout>` repoints the clone's `origin` at the local checkout, so a
"pushed" claim can be satisfied by a local ref alone
(`reports/consumer-sweep.md` §9). Every claim is therefore re-checked against
`git ls-remote https://github.com/LiGoldragon/<name>.git`, the URL derived
from the repository name, never from any checkout's origin.

## Method

1. Read `log.md` and every report named in the brief, collecting every
   (repository, branch, claimed revision) triple.
2. For each repository, `git ls-remote https://github.com/LiGoldragon/<name>.git`
   and keep `refs/heads/main` plus every `refs/heads/f6db8d-*`.
3. For each claimed revision, compare against the remote head; where it
   differs, `git merge-base --is-ancestor <claim> <head>` in the local
   checkout (which already holds both objects — no fetch was performed).
4. Print each local checkout's `origin` URL so a repointed origin is visible.
5. `orchestrate 'Observe.Locks'` — one read-only Observe.

Everything below is **witnessed** by this subflow: the `ls-remote` output,
the ancestry results and the `Observed` reply were produced here.

## Local origin URLs

Every checkout under `/git/github.com/LiGoldragon/` was surveyed for a
local-path or `file:` origin. **None was found** — no checkout's origin points
at another local checkout, so the `--shared` pollution recorded in
`consumer-sweep.md` §9 does not survive anywhere in the shared trees.

Two checkouts do not have GitHub as `origin`, and this matters below:

| checkout | `origin` | `github` remote |
|---|---|---|
| `/git/github.com/LiGoldragon/repository-ledger` | `gitolite@localhost:repository-ledger` | `git@github.com:LiGoldragon/repository-ledger.git` |
| `/git/github.com/LiGoldragon/signal-repository-ledger` | `gitolite@localhost:signal-repository-ledger` | `git@github.com:LiGoldragon/signal-repository-ledger.git` |

Every other checkout's `origin` is `git@github.com:LiGoldragon/<name>.git` or
`ssh://git@github.com/LiGoldragon/<name>`, i.e. the same repository the
verification URL names.

## The table

`EXACT` = the claimed revision is `refs/heads/<branch>` at GitHub.
`ANCESTOR` = it is reachable from that head, which the table names.
`ABSENT` = the ref does not exist at GitHub.

### Producers

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| protos | main | `e8701521` 0.30.0 | protos-fix, substrate-repin | `171b21f6` | ANCESTOR |
| protos | main | `171b21f6` 0.30.1 | substrate-drift, producer-settle | `171b21f6` | **EXACT** |
| datom-codec | main | `196d0e29` 0.26.0 | datom-codec-fix | `627db67f` | ANCESTOR |
| datom-codec | main | `18129314` 0.26.1 | substrate-repin | `627db67f` | ANCESTOR |
| datom-codec | main | `5eefe829` 0.26.2 | substrate-drift | `627db67f` | ANCESTOR |
| datom-codec | main | `627db67f` 0.26.3 | producer-settle | `627db67f` | **EXACT** |
| ethos-zero | main | `c8a68369` 7.0.0 | ethos-zero-fix | `de3d9928` | ANCESTOR |
| ethos-zero | main | `212b3590` 7.0.1 | substrate-repin | `de3d9928` | ANCESTOR |
| ethos-zero | main | `da585049` 8.0.0 | datom-migration | `de3d9928` | ANCESTOR |
| ethos-zero | main | `de3d9928` 8.0.1 | producer-settle | `de3d9928` | **EXACT** |
| signal | main | `2276ec42` 3.0.1 | orchestrate-work | `8f9a0deb` | ANCESTOR |
| signal | main | `8f9a0deb` 3.0.2 | producer-settle | `8f9a0deb` | **EXACT** |
| signal-standard | main | `8f9a0deb` 3.0.2 | consumer-sweep §1 | `8f9a0deb` | **EXACT** (same content as `signal`, distinct GitHub repository) |
| nexus | main | `a84bfa96` 0.1.1 | orchestrate-work (pinned, not released) | `a84bfa96` | **EXACT** |

### Orchestrate group and claude-answers

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| signal-orchestrate | main | `c783b727` 3.0.1 | orchestrate-work | `e7221190` | ANCESTOR |
| signal-orchestrate | main | `45ff2d41` | orchestrate-followup | `e7221190` | ANCESTOR |
| signal-orchestrate | main | `e722119` 3.0.2 | consumer-sweep §9 | `e7221190` | **EXACT** |
| meta-signal-orchestrate | main | `707f4cb8` 3.0.1 | orchestrate-work | `4279ad05` | ANCESTOR |
| meta-signal-orchestrate | main | `969c7d2d` | orchestrate-followup | `4279ad05` | ANCESTOR |
| meta-signal-orchestrate | main | `4279ad0` 3.0.2 | consumer-sweep §9 | `4279ad05` | **EXACT** |
| orchestrate | main | `054ce581` 0.32.0 | orchestrate-work | `c8a28821` | ANCESTOR |
| orchestrate | main | `3926ba35` 0.33.0 | orchestrate-followup | `c8a28821` | ANCESTOR |
| orchestrate | main | `c8a2882` 0.33.1 | consumer-sweep §9 | `c8a28821` | **EXACT** |
| claude-answers | main | `cf124370` 0.7.0 | datom-migration | `0f857a3f` | ANCESTOR |
| claude-answers | main | `0f857a3` 0.7.1 | consumer-sweep §9 | `0f857a3f` | **EXACT** |

Both repositories in which the `--shared` mistake was caught —
`signal-orchestrate` and `claude-answers` — are **EXACT** at GitHub. The
correction held.

### Datom migration and consumer sweep

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| signal-message | main | `f03a147c` 2.0.0 | datom-migration | `2da9c6dd` | ANCESTOR |
| signal-message | main | `2da9c6dd` 2.0.1 | consumer-sweep | `2da9c6dd` | **EXACT** |
| signal-domain | main | `01c73e78` 2.0.0 | datom-migration | `0e3c55bb` | ANCESTOR |
| signal-domain | main | `0e3c55bb` 2.0.1 | consumer-sweep | `0e3c55bb` | **EXACT** |
| signal-persona | main | `07494bb2` 2.0.0 | datom-migration | `48118557` | ANCESTOR |
| signal-persona | main | `48118557` 2.0.1 | consumer-sweep | `48118557` | **EXACT** |
| signal-terminal | main | `b0523f77` 2.0.0 | datom-migration | `bb696365` | ANCESTOR |
| signal-terminal | main | `bb696365` 2.0.1 | consumer-sweep | `bb696365` | **EXACT** |
| signal-introspect | main | `5b362716` 2.0.0 | datom-migration | `8de16e35` | ANCESTOR |
| signal-introspect | main | `8de16e3` 2.0.1 | consumer-sweep | `8de16e35` | **EXACT** |
| signal-upgrade | main | `e9bffc57` 2.0.0 | datom-migration | `b1bec686` | ANCESTOR |
| signal-upgrade | main | `b1bec686` 2.0.1 | consumer-sweep | `b1bec686` | **EXACT** |
| signal-spirit | main | `c1d78e85` 3.0.0 | datom-migration | `d13ddcea` | ANCESTOR |
| signal-spirit | main | `d13ddce` 3.0.1 | consumer-sweep | `d13ddcea` | **EXACT** |
| signal-spirit-judge | main | `f9da94e3` 2.0.0 | datom-migration | `5e7764ea` | ANCESTOR |
| signal-spirit-judge | main | `5e7764ea` 2.0.1 | consumer-sweep | `5e7764ea` | **EXACT** |
| meta-signal-spirit | main | `9f6c648e` 3.0.0 | datom-migration | `7ba0f820` | ANCESTOR |
| meta-signal-spirit | main | `6f6c8c0a` | consumer-sweep | `7ba0f820` | ANCESTOR |
| meta-signal-spirit | main | `7ba0f82` 3.0.1 | log.md wave 4 | `7ba0f820` | **EXACT** |
| meta-signal-upgrade | main | `83c6cead` 2.0.0 | datom-migration | `a319e1ba` | ANCESTOR |
| meta-signal-upgrade | main | `a319e1ba` 2.0.1 | consumer-sweep | `a319e1ba` | **EXACT** |
| meta-signal-terminal | main | `3d0eafa1` 2.0.0 | datom-migration | `a9b18ee8` | ANCESTOR |
| meta-signal-terminal | main | `a9b18ee8` 2.0.1 | consumer-sweep | `a9b18ee8` | **EXACT** |
| clavifaber | main | `2aaf293f` | cargo-update-tier0 | `c42010db` | ANCESTOR |
| clavifaber | main | `8fa6dc44` 0.4.0 | datom-migration | `c42010db` | ANCESTOR |
| clavifaber | main | `c42010db` 0.4.1 | consumer-sweep | `c42010db` | **EXACT** |
| signal-mirror | `f6db8d-datom-migration` | `4c6765fa` 2.0.0 | datom-migration | `4c6765fa` | **EXACT** |
| signal-mirror | main | `e60b7667` 2.0.1 | consumer-sweep | `e60b7667` | **EXACT** |
| meta-signal-mirror | `f6db8d-datom-migration` | `b269ceda` 2.0.0 | datom-migration | `b269ceda` | **EXACT** |
| meta-signal-mirror | main | `adf6be61` 2.0.1 | consumer-sweep | `adf6be61` | **EXACT** |

### nota-pins and cargo-update tier 0

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| aggregator | main | `87c48f81` 0.4.0 | nota-pins | `87c48f81` | **EXACT** |
| aggregator | `f6db8d-cargo-update` | `7ef8d506` | cargo-update-tier0 | `7ef8d506` | **EXACT** |
| harness | main | `9a4d3375` 0.4.0 | nota-pins | `9a4d3375` | **EXACT** |
| harness | main | `29c79561` | cargo-update-tier0 | `9a4d3375` | ANCESTOR |
| harness | `f6db8d-cargo-update` | `d28634c2` | cargo-update-tier0 | `d28634c2` | **EXACT** |
| message | main | `dee8f271` | cargo-update-tier0 | `38345dae` | ANCESTOR |
| message | main | `38345dae` 0.11.1 | nota-pins | `38345dae` | **EXACT** |
| agent | main | `df5f5bfd` | cargo-update-tier0 | `df5f5bfd` | **EXACT** |
| dotos-text-query | main | `aee1a446` | nota-pins | `aee1a446` | **EXACT** |
| signal-aggregator | main | `5d2b80e2` 0.6.0 | nota-pins | `234ed642` | ANCESTOR |
| meta-signal-aggregator | main | `98cc36fc` 0.4.0 | nota-pins | `02897947` | ANCESTOR |
| router | main | `f60d4e33` (untouched) | nota-pins, cargo-update-tier0 | `f60d4e33` | **EXACT** |
| router | `f6db8d-nota-pins` | `5fa990dc` | nota-pins | `5fa990dc` | **EXACT** |
| router | `f6db8d-cargo-update` | `f15220b0` | cargo-update-tier0 | `f15220b0` | **EXACT** |
| listener | main | `471b0d59` (found-in-tree landing) | nota-pins, cargo-update-tier0 | `471b0d59` | **EXACT** |
| listener | `f6db8d-cargo-update` | `04137484` | nota-pins, cargo-update-tier0 | `04137484` | **EXACT** |
| signal-repository-ledger | `f6db8d-nota-pins` | `9d267c27` 0.2.0 | nota-pins | `9d267c27` | **EXACT** |
| signal-repository-ledger | main | `894335a0` (untouched) | nota-pins | `894335a0` | **EXACT** |
| meta-signal-repository-ledger | `f6db8d-nota-pins` | `0c2da541` 0.2.0 | nota-pins | `0c2da541` | **EXACT** |
| repository-ledger | main | `4153fd84` "(origin)" | nota-pins, cargo-update-tier0 | `0580eff4` | **NOT the GitHub head** — see D2 |
| repository-ledger | `f6db8d-cargo-update` | `0c9bd81b` | cargo-update-tier0 | — | **ABSENT from GitHub** — see D2 |

### Test branches, never landed

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| CriomOS | `f6db8d-lojix-start` | `c4c830c1` | lojix-criomos | `c4c830c1` | **EXACT** |
| CriomOS | main | `acc3feab` (untouched) | lojix-criomos | `acc3feab` | **EXACT** |
| CriomOS-home | `f6db8d-lojix-start` | `0176de5f` | lojix-criomos | `0176de5f` | **EXACT** |
| CriomOS-home | `f6db8d-removals` | `4cb132ec` | removals | `4cb132ec` | **EXACT** |
| CriomOS-home | main | `caffe9a1` (untouched) | removals, lojix-criomos | `caffe9a1` | **EXACT** |
| terminal-cell | `f6db8d-removals` | `f572839e` | removals | `f572839e` | **EXACT** |
| terminal-cell | main | `e44c41a3` (untouched) | removals | `e44c41a3` | **EXACT** |

### Lojix group

| repository | branch | claimed | source | GitHub head | verdict |
|---|---|---|---|---|---|
| horizon-rs | main | `a5633045` 0.10.0 | lojix-work | `a5633045` | **EXACT** |
| signal-lojix | main | `d0f5c70d` 4.1.0 | lojix-work | `d0f5c70d` | **EXACT** |
| meta-signal-lojix | main | `1eccc0e3` 5.1.0 | lojix-work | `1eccc0e3` | **EXACT** |
| lojix | main | `48f637e8` 3.0.0 | lojix-work | `48f637e8` | **EXACT** |

`reports/aggregator-migration.md` is a stub: it carries the ruling it
corrects and no revision claim, so it contributes no row. Its work is the
one still under a live f6db8d lock (§ below), and its two landed contracts
are what moved `signal-aggregator` and `meta-signal-aggregator` past
nota-pins' revisions.

## Live Orchestrate locks still held by f6db8d

`orchestrate 'Observe.Locks'`, one read-only Observe, witnessed. Three:

| id | name | paths | reason |
|---|---|---|---|
| 1111 | `LojixNexusHardening` | `/git/github.com/LiGoldragon/lojix` | W3 W8 W9 W10 failure evidence laws and housekeeping |
| 1112 | `HorizonRsNoFreeFunctions` | `/git/github.com/LiGoldragon/horizon-rs` | W9 enforce no-free-functions and no-inherent-methods |
| 1193 | `AggregatorDatomMigration` | `/git/github.com/LiGoldragon/aggregator` | Migrate aggregator from dotos to the Datom stack |

Every other lock in the snapshot belongs to 542442, f7941a, 6329f1,
`run_wispr_live_witness` or `implement_wispr_edge_proxy`. No lock this
subflow observed was taken, released or otherwise touched.

## Discrepancies

Ten. Nothing tonight was falsely claimed as pushed: **every revision claimed
as landed on `main` or on a test branch is either exactly that branch's
GitHub head or an ancestor of it**, with the single exception of D2, whose
"origin" was never GitHub.

**D1 — `repository-ledger`'s "main@origin" is the gitolite mirror, not
GitHub.** `cargo-update-tier0.md` and `nota-pins.md` both record
`main@origin` as `4153fd84` and call it "the pushed authority", basing the
tier-0 work on it, and both name `0580eff4` as a local-only divergent
commit. Witnessed: `git ls-remote https://github.com/LiGoldragon/repository-ledger.git`
gives `refs/heads/main` = **`0580eff4`**, and
`git ls-remote gitolite@localhost:repository-ledger` gives `4153fd84`. The
checkout's `origin` is `gitolite@localhost:repository-ledger`; its GitHub
remote is named `github`. So what the two reports treated as the pushed
authority is the local mirror, and GitHub already carries the commit they
called local-only. The divergence is real but inverted from how it is
recorded.

**D2 — `repository-ledger`'s `f6db8d-cargo-update` branch is not on
GitHub.** `cargo-update-tier0.md` claims it "pushed at `0c9bd81bde7b`, left
in place". Witnessed: that ref exists only on
`gitolite@localhost:repository-ledger`; GitHub's complete ref list for the
repository is `main` `0580eff4` and
`repository-ledger-os-update-2026-07-08` `33dc91bf`. This is the one claimed
push that did not reach GitHub. It is the same class of failure as the
`--shared` incident — a push satisfied by a non-GitHub remote — with a
different cause.

**D3 — `signal-repository-ledger`'s mirror `main` is still standing on the
branch revision.** `nota-pins.md`'s method note says jj's default push
target moved "the *mirror's* main sideways onto the local-only divergent
commit; it was immediately repointed to the intended revision and GitHub was
never touched by it." GitHub was indeed never touched — its `main` is
`894335a0`, unchanged. But witnessed now:
`git ls-remote gitolite@localhost:signal-repository-ledger` gives
`refs/heads/main` = **`9d267c27`**, which is the `f6db8d-nota-pins` revision
itself, and `894335a0` is **not** an ancestor of it (`1a83dc31` is). The
mirror's `main` therefore still carries the sideways move the report says was
undone, and the mirror has no `f6db8d-nota-pins` branch at all.

**D4 — `signal-aggregator` and `meta-signal-aggregator` have moved past the
revisions `nota-pins.md` names as landed.** Claimed `5d2b80e2` (0.6.0) and
`98cc36fc` (0.4.0); GitHub heads are `234ed642` ("Move the contract to Ethos
Zero, Datom, and the shared Signal frame") and `02897947` (the same, meta).
Both claims are ancestors, so neither is false — but the aggregator-migration
subflow has already landed the correction `stack-membership.md` called for on
the two contracts, while `aggregator` itself is still at `87c48f81`, the
Dotos revision. The correction is half-landed: contracts moved, consumer not.
That subflow still holds lock 1193 and its report is a stub with no revision
table.

**D5 — three f6db8d locks are still held with their work reported finished.**
1111 `LojixNexusHardening` over `/git/github.com/LiGoldragon/lojix` and 1112
`HorizonRsNoFreeFunctions` over `/git/github.com/LiGoldragon/horizon-rs` are
live, yet `lojix-work.md` reports all four of its repositories released and
verified at GitHub (all four **EXACT**), and `datom-migration.md` and
`consumer-sweep.md` both skipped `lojix` and `horizon-rs` on the strength of
exactly these two locks. `lojix-work.md` never mentions acquiring or
releasing any lock. 1193 `AggregatorDatomMigration` is live and plausibly
still in flight (D4). Two locks appear to be leaked by a finished subflow,
and they blocked two consumer sweeps for the rest of the night.

**D6 — `signal-introspect` has no `f6db8d-sweep` branch.**
`consumer-sweep.md` §5 says all three retried repositories "pushed their
partial work to `f6db8d-sweep` and released their lock". Witnessed: the branch
exists on `signal-spirit-judge` (`cb9f0a79`) and `meta-signal-spirit`
(`ab23db0b`), and `signal-introspect`'s complete GitHub ref list carries no
such branch. Consequence-free — its `main` landed correctly at `8de16e3` —
but the claim is wrong for one of the three.

**D7 — `harness` carries two different "landed on main" revisions from two
subflows, and the earlier one is silently superseded.** `cargo-update-tier0.md`
lands an empty reflow commit at `29c79561` on main; `nota-pins.md` lands
0.4.0 at `9a4d3375`. `29c79561` is an ancestor of `9a4d3375`, so both are
true, but neither report names the other's revision. The same shape holds for
`message` (`dee8f271` then `38345dae`) and `clavifaber` (`2aaf293f` then
`8fa6dc44` then `c42010db`). Recorded so a reader of any one report does not
take its revision for the current head.

**D8 — `meta-signal-spirit`'s three successive claims.** `9f6c648e` (3.0.0),
`6f6c8c0a` (repin, version label left at 3.0.0 — recorded as a defect by
`consumer-sweep.md` §7), `7ba0f82` (3.0.1, the correction). All three verify
as ancestor/ancestor/EXACT. No push problem; noted because the version label
and the revision came apart for one commit and the intermediate commit is on
GitHub permanently.

**D9 — three `orchestrate` commit messages and two contract repin messages
mislabel `da585049` as ethos-zero 7.0.1.** Recorded by `orchestrate-work.md`
§1 itself and deliberately not rewritten. The revisions pinned are correct
and are on GitHub; only the prose in pushed commit messages is wrong. Nothing
to verify further — carried here so it is not lost.

**D10 — no local checkout's `origin` points at another local checkout.** The
`--shared` pollution of `consumer-sweep.md` §9 left no residue in the shared
trees: a scan of every `.git` under `/git` to depth 5 for a path-shaped or
`file:` origin returned nothing, and the two repositories it polluted
(`signal-orchestrate`, `claude-answers`) are EXACT at GitHub. This is a
negative finding, stated because the brief's occasion demands it be stated
rather than assumed.

## Sources

- `/home/li/primary/flows/f6db8d/log.md` and
  `/home/li/primary/flows/f6db8d/reports/{protos-fix,datom-codec-fix,
  ethos-zero-fix,substrate-repin,substrate-drift,producer-settle,
  datom-migration,consumer-sweep,orchestrate-work,orchestrate-followup,
  cargo-update-tier0,nota-pins,lojix-criomos,removals,aggregator-migration,
  lojix-work}.md` — read by this subflow for the claims; every claim in the
  table is relayed from the named report and is the report's, not this
  subflow's.
- `git ls-remote https://github.com/LiGoldragon/<name>.git` for all 43
  repositories named above, and
  `git ls-remote gitolite@localhost:{repository-ledger,signal-repository-ledger}`
  — run by this subflow; the URLs were derived from repository names, never
  from a checkout's origin.
- `git merge-base --is-ancestor` and `git cat-file -e` in the local
  checkouts under `/git/github.com/LiGoldragon/`, read-only, no fetch.
- `git config --get remote.origin.url` over every `.git` directory under
  `/git` to depth 5 — the local-origin scan.
- `orchestrate 'Observe.Locks'` — one read-only Observe against the live
  Nexus, as an ordinary client.
