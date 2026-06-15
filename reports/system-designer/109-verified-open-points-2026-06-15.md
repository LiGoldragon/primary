# 109 — Verified state of the open points (2026-06-15, afternoon)

*The psyche asked to verify the state of our most important unaddressed points
before being asked to decide them. A 6-way verification sweep against live
ground truth found that report 108 (written this morning) is **materially stale**:
the structural-forms + domain-coarsening deploy **landed today**, two "open"
concept decisions are **already resolved in Spirit**, and two cited bead ids are
**phantom**. This report records the corrected state; the genuinely-open psyche
decisions go to chat as `AskUserQuestion`. Supersedes 108's "Live situation"
section only — 108's arcs, engine-analysis, and maintenance ledger stand.*

## Headline — the deploy landed

Between report 108 (morning) and this verification (afternoon), the
**system-operator integrated and deployed** the candidate. Live state now:

- **spirit-daemon 0.13.0** deployed (was 0.12.1). `spirit Version` →
  `(VersionReported 0.13.0)`; the 0.12.1→0.13.0 bump happened (commit `824ca0b3`).
- **Store schema 10**, **1258 records** (was schema 9 / 1248). The `fwe3` domain
  coarsening migration ran — `v9/v8/v7 → schema 10` From-chain rewrite.
- **`structural-forms-integration` merged to spirit main and deployed** — the
  contract-crate split (signal-spirit / meta-signal-spirit consume) + the domain
  coarsening. CriomOS-home flake.lock spirit rev is now `c752e89f` (was `f4635c3c`).
- **Guardian journal advanced to v4** (`spirit.guardian.v4.sema`); the deploy
  isolated a guardian-journal layout break to v4.
- Daemon restarted **15:27 today** for the 0.13.0 deploy and **self-resumed**
  (reported `(Current (1255 0))`, since grown to 1258) — the resume path works.

The two-migration sequencing worry from 106/107/108 ("VC layout self-heal FIRST,
coarsening SECOND, must not interleave") was resolved via the **bundled-one-pass**
path that 106/107 allowed: both store changes shipped in one HomeOnly activation
on `ouranos`. The "promote candidate vs keep substrate" question (operator Q1) is
**resolved — promoted and live**.

## What did NOT ship — the VC self-heal tower is still pending

Crucial nuance: the deployed spirit 0.13.0 still pins **sema-engine 0.4.0**
(rev `dbe29427`, "tamper witnesses"). The engine **hardening tower** —
`rebuild_from_log` layout self-heal (`e5e38e8e`), record-key-sum, the O(1)
chain-head digest, single-writer lock, store god-impl decomposition — is in
**sema-engine 0.6.x**, which is **not an ancestor** of the deployed `dbe29427`.
So `qu28` / `lmf3` / `x178` remain **genuinely undeployed**. The live store
reached schema 10 via a From-chain domain rewrite **on the old engine**, so the
layout-4→5 self-heal **never ran in production**.

This inverts 108's framing: 108 named the staging-copy self-heal proof as *the*
single blocker before deploy. The deploy went ahead **without** it (different
migration path), so it is no longer a deploy blocker — but the tower work itself
is still open, and its premise changed (see the sequencing decision below).

**Verification loose end (operator to confirm):** two verifier agents disagreed on
the deployed sema-engine version — one read the repo's current-main `Cargo.toml`
(0.6.2) and one read the deployed lock rev (`dbe29427` = 0.4.0). The synthesis
resolved it to **0.4.0** via `git merge-base` (rebuild-from-log not an ancestor of
the deployed rev). The operator should confirm the exact deployed sema-engine rev
when next touching the tower; the conclusion (tower undeployed) holds either way.

## Verified open-points ledger

| Point | Owner | Status | Verified current state |
|---|---|---|---|
| `qu28` VC hardening tower | operator | **open** | Undeployed; deployed engine 0.4.0, tower is 0.6.x not an ancestor. |
| `fwe3` domain coarsening | system-operator | **resolved** | CLOSED 09:13 today, DEPLOYED (schema 10, HomeOnly on ouranos). |
| `gm78` scope All buckets | operator | **resolved** | CLOSED 09:13 today, satisfied by `fwe3` (terminal optional domains keep ancestor-All retrieval). |
| `lmf3` engine self-heal | operator | **open** | Not in deployed 0.4.0; store migrated via From-chain, not layout self-heal. Tied to `qu28`. |
| `x178` god-impl decomposition | operator | **open** | Authored into the tower; deployed engine is 0.4.0, so still open. |
| `dmy4` VersionReport store axis | operator | **open** | Live CLI reports only `(VersionReported 0.13.0)`; schema 10 not daemon-introspectable (`(Schema)` → unknown Input variant). |
| `x3l7` mirror ingress auth | system-operator | **open** | Unchanged: mirror-daemon still `0.0.0.0:7474` unauthenticated; deploy didn't touch it. Dormant (shipper removed). |
| `85hv` production shipper | operator | **blocked** | Behind `x3l7`; dormant — no `shipper.rs`, feature off by default. |
| CollectRemovalCandidates shape | **psyche** | **open** | Operation root settled+deployed; combined-vs-pure-extract shape is psyche's to ratify. |
| Privacy default + private-capture | **psyche** | **open** | Shipped uniform positional Magnitude (default public); deliberate private-capture ritual unresolved. |
| Record SHAPE flat vs per-kind | **psyche** | **open** | Flat shipped de-facto; per-kind-variant intent (`20jk`/`f0wm`) unsuperseded. Gates the record redesign. |
| message existence-log | **psyche** | **open** | `l3k4` assigns existence to message but router writes it (`router.rs:1163`); build-vs-defer. |
| Guardian §6 gates (89) | psyche | **resolved** | **DO NOT ASK** — court-of-law arc: one guardian (`zgi8`), referent gate = records + exact-match skip (`ut6z`/`bwxn`), atomic cross-record judging. |
| Terminal session-control owner (78/79) | psyche | **resolved** | **DO NOT ASK** — settled 2026-06-06: `terminal-control` triad, systemd forks the cell, orchestrate owns lifecycle, terminal-control owns the sema record (`f8tb`/`p1dt`/`51sf`/`r8cy`). |

## Stale claims corrected in report 108

- "Deployed 0.12.1" → now **0.13.0**.
- "1248 records, schema v9" → now **1258 records, schema 10**.
- "structural-forms-integration NOT yet deployed, must bump to 0.13.0" → **merged
  to main and deployed; bump done** (`824ca0b3`).
- "flake.lock spirit rev `f4635c3c`" → now `c752e89f`.
- "guardian journal v3" → **v4**.
- "daemon restarted 08:37, self-resumed from v9 store" → restarted again **15:27**
  for the 0.13.0 deploy, self-resumed.
- "`fwe3` open, deploy-gated strictly AFTER SEMA-VC" → **CLOSED + deployed**, via
  the **bundled-one-pass** path, not strictly-after.
- "staging-copy self-heal proof is THE single blocker" → **stale as a blocker**
  (deploy went ahead without it); underlying tower work still open.
- "terminal ownership settled per Spirit `bcca`" → `bcca` **does not resolve**;
  settlement carried by `f8tb`/`p1dt`/`51sf`/`r8cy`. `bcca` is only a stale
  antecedent id referenced inside `51sf`.

## Phantom ids and unstable record codes

- **`29pb`** ("remote durability intent") and **`ubgg`** ("intent-subscription
  pilot") cited in 108 are **phantom** — neither exists in `.beads/` (verified
  across all 685 ids). Remote durability is the conceptual tail of `x3l7 → 85hv`,
  not a tracked bead. Drop both ids from the canon.
- **Record short-codes are not stable across store rebuilds.** Source-report ids
  `m27p`, `bcca`, `1547`/`1571` etc. no longer resolve; the substance survives
  under re-minted ids (`20jk`, `f0wm`, `l3k4`, `qr5o` all live). **All decision
  framing must quote substance, never the stale codes.**

## Documentation gap

There is **no operator / system-operator report** documenting the 0.13.0 deploy —
only the `fwe3` bead close-reason. A deploy that moved the production intent store
to a new schema with a guardian-journal break isolation deserves a deploy log.
Flag to the system-operator: write the deploy record (what migrated, the v4
journal break, rollback/backup state) so the next agent isn't reconstructing it
from bead metadata.

## The genuinely-open psyche decisions (asked in chat)

Four pure-intent concept decisions, ranked by downstream leverage:

1. **Record shape** — flat-uniform-optional-privacy vs per-kind-variant vs
   kind-discriminant. The single most load-bearing gate; coupled to (3).
2. **CollectRemovalCandidates** — combined guarded call (archive-then-retract) vs
   pure-extract (discovery separate from a distinct Remove) vs both roots.
   Reportedly blocks ~5 core operation designs.
3. **Privacy default + private-capture ritual** — named private short-form vs flip
   the default vs keep public-by-default. Coupled to (1).
4. **message existence-log** — build message its own durable existence surface
   (realize `l3k4`) vs keep it a 2-plane SO_PEERCRED trust membrane (router owns
   the existence record).

One **strategic** decision follows once those land:

5. **VC tower sequencing** — ship the sema-engine 0.6.x self-heal tower next /
   defer it (store is healthy at schema 10, self-heal is insurance) / re-scope it
   against the now-deployed 0.4.0 + schema-10 reality (the staging-proof premise
   in `qu28` was written pre-deploy and is partly stale).
