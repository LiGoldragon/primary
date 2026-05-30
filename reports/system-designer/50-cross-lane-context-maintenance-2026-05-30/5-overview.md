# Overview — cross-lane context maintenance synthesis (2026-05-30)

*Dispatcher synthesis of the `/50` sweep across four topic
sub-reports. Successor to
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
(retires in this sweep's drop execution). The decisive
cross-cutting finding: the workspace mostly **self-cleaned**
between 44 and this sweep — three lanes ran their own sweeps in
response to 44 and a fourth lane self-cleaned a second time
today. The deltas, where actionable cross-lane drops still sit,
concentrate in operator (24 drops), cloud-operator (3), and
second-designer (2).*

## The decisive cross-cutting finding

Two things shifted the picture since 44:

**(A) Production Spirit 0.3.0 grew the recency filter +
`ChangeCertainty` + `(Exact Zero)` parsing today** (witness
commits per sub-report 3: `signal-persona-spirit 1bb22635`,
`persona-spirit c5a3eb9b`, `CriomOS-home cc6bb3d2`,
`CriomOS 1cf0b747`, primary skills `180e6f2b`). The deployed
`RecordQuery` is now five-field:
`(TopicSelection KindOption CertaintySelection RecordedTimeSelection ObservationMode)`.
`RecordedTimeSelection` variants are `Any` /
`(Since (YYYY-MM-DD HH:MM:SS))` / `(Until ...)` / `(Between ...)` /
`Recent`. The bare `Recent` variant returns the newest records
**after** topic/kind/certainty filtering — quiet topics naturally
reach farther back than active ones, which is the
natural-recency-by-topic-touch-frequency idea (record 1251) emerging
as a side-effect of filter-first then newest.

`ChangeCertainty` is the **nominate path** that `/48` flagged as
GAP 1; the soft-delete buffer is now active (a record can be
lowered to `Zero` and recovered, not just hard-deleted).

This overtakes `/49 §"Spirit search — the next direction"` and
`/48 §"GAP 1 — nominate write path missing"`. Both reports stay
(§3a guard on `/48` for the tombstone + the Zero-vs-None
rationale; `/49` carries the Nexus-language exploratory direction
that is NOT yet implemented) with status-banners pointing to the
deployment.

**(B) Three lanes self-swept between 44 and 50.**
`reports/designer/415-context-maintenance-2026-05-28.md` retired
27 schema-stack reports on 05-28;
`reports/designer/439-context-maintenance-2026-05-30.md` retired
12 more today;
`reports/system-operator/173-deep-context-maintenance-2026-05-30.md`
self-absorbed `/172` and `/169` (the `/169-context-maintenance`
directory contents are deleted; the empty directory still sits on
disk awaiting `rm`);
`reports/cloud-designer/15-lane-agglomeration-audit-and-maintenance-2026-05-29.md`
is the cloud-designer lane's living agglomeration (NOT a stale
ledger — it carries 5 open psyche questions). The cross-lane
handoff round 44 issued **worked** — lanes applied their own
handoffs without waiting on the dispatcher.

So this sweep's role is narrower than 44's was: ratify what's
already happened, surface the deltas that still need doing, and
retire `44` itself + the remaining stale ledger residue.

## Per-lane handoff table

| Lane | State | Action this sweep |
|---|---|---|
| **system-designer** (dispatcher) | 5 reports; this sweep adds `50/` directory | Drop `44/` (this sweep supersedes it). Update `48` + `49` with status-banners re production Spirit deployment. |
| **designer** | 22 reports | **None owed.** `/415` + `/439` already covered everything sub-agent A surfaced. Lane is self-current. Drop `415` as ledger retirement (handoff). |
| **operator** | 9 reports (was 47) | **None owed.** Operator self-cleaned in parallel with this sweep (commit `mokrklnw`): retired 38 reports (210-247 era), agglomerated into `reports/operator/260-pre-canonical-era-agglomeration-2026-05-30.md`, dropped landed audits 249-259. Kept set is now 246/248/251/252/253/255/256/258/260 (designer-authored under psyche override pattern). The 24-drop band sub-agent A surfaced is now fully self-applied. Lane is self-current. |
| **system-operator** | 7 reports + 1 empty dir | Already self-current via `/173`. Final `rm` of empty `169-context-maintenance-2026-05-28/` directory (its contents already deleted; just the empty dir to remove). |
| **second-designer** | 2 reports | Drop `/165` (counter-ego audit retired with target). `/176` is borderline §3a — defensible as Keep+status-banner if the upgrade-mechanism soup-to-nuts walk is valued for upcoming schema-diff work. **Surface to second-designer/psyche.** |
| **cloud-designer** | 4 reports | **None owed.** `/15` is a living agglomeration with 5 open psyche questions — NOT a stale ledger. `/11` and `/15` carry §3a design-rationale (Path A vs B, 8-gap audit). All Keep. |
| **cloud-operator** | 7 reports | Drop `/6` + `/7` (refresh-audit pair stale per `/50/2`); drop `/12/` (skill-manifestation ledger). KEEP `/9` `/10` `/11` `/13`. |
| **cluster-operator** | 1 report | KEEP `/1` (§3a — multi-option design with 4 open questions). **Migrate** the settled `SystemUpdateGrant` pattern to per-repo INTENT/ARCHITECTURE (horizon-rs + CriomOS + lojix-cli) when the open questions close. |
| **third-designer** | 0 | **Lane-retirement candidate** — reaffirmed; psyche call needed. |
| **second-operator** | 0 | **Lane-retirement candidate** — reaffirmed; psyche call needed. |
| **nota-designer** | 0 | **Lane-retirement candidate** — reaffirmed; psyche call needed. |
| **poet** | 0 | **Lane-retirement candidate** — reaffirmed; psyche call needed. |

## System-designer-lane drops the dispatcher executes

Per `skills/context-maintenance.md` §"Per-lane handoffs and
dispatcher authority", the dispatcher executes drops only in its
own lane. Two actions on `reports/system-designer/`:

| Action | Path | Landing evidence |
|---|---|---|
| Drop | `reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/` | This sweep (`reports/system-designer/50-cross-lane-context-maintenance-2026-05-30/`) supersedes it: same lanes covered, recency-re-ranked, still-live handoffs re-issued (the 4 prior-ledger retirements + the operator 24-drop band + the cloud-operator 3-drop band + the second-designer 2-drop band). |
| Edit (status-banner) | `reports/system-designer/48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md` | GAP 1 (nominate path) closed by production `ChangeCertainty` deployed today; report keeps §3a guard for tombstone + Zero-vs-None rationale. |
| Edit (status-banner) | `reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md` | §"Spirit search — the next direction" recency proposal now implemented and deployed; `RecordedTimeSelection` variants differ from the sketched `RecencySelection` (psyche/operator chose `Recent`/`Since`/`Until`/`Between` over `Newest N`/`Window`); the Nexus-language adaptive section remains forward-looking. Also fix the `/172` → `/173` parallel-surface reference (172 was absorbed by 173 today). |

`reports/system-designer/34-mvp-and-sandbox-audit/`, `/43`, `/48`,
`/49` stay. `/50/` is the new working ledger.

## Pending psyche-attention queue (surfaced, not actioned)

Carried forward from this sweep and the prior round:

| Item | First raised | Current status |
|---|---|---|
| Lane retirements: `third-designer`, `second-operator`, `nota-designer`, `poet` (all 0 reports) | 44 (2026-05-28) | Reaffirmed this sweep. Per `skills/context-maintenance.md` §"Retiring a lane", retirement is psyche-direction-gated. Memories already at zero — no leftover-substance blocker. |
| `/designer/351` + `/352` pending-review flags | designer/sweep prior to 44 | **Across 4 sweeps now.** Highest-impact flag (M1 schema-defines-effects drift, Spirit records 660-665/710/663/664) is NOW actionable because deployed `ChangeCertainty` lets the supersession lifecycle run in production. Recommend re-surface with concrete mechanism (per `/50/4` §E). |
| Spirit record 1145 backup-network divergence | cloud-designer (per `/50/2`) | Backup-network mostly done in code but architecturally diverged from 1145 (br-lan bridging depends on kea/dnsmasq). Cloud-designer surfaced; awaits psyche call. |
| `cloud-designer/15`'s 5 open psyche questions | 2026-05-29 | gap-1 lane scope, gap-2 Arc A fate, gap-3 backup independence, gap-4 Gemma 4 fix, gap-5 quant set. |
| `second-designer/176` upgrade-mechanism §3a call | this sweep | Drop or Keep-with-banner. The substance lands when schema-diff work begins. |
| Nexus-language Spirit search (record 1251, Low) | 2026-05-30 | Implementation question: design now (sketch the scoring composition, weighted-keyword Nexus schema, topic-touch-frequency window) or wait until a concrete use surfaces. The simpler recency-filter just landed today which closes the immediate gap. |

## Operator action carried forward (from `/50/3`)

GAP 2 from `/48` — the **discriminant-stability rule** (rkyv-archived enum variants append-at-end + manual `Ord`, never reorder; declaring a new variant first shifts every persisted discriminant by one byte and silently corrupts every archived value) — needs to land in `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` as a §"Schema evolution — discriminant stability" note. The operator deployed `signal-sema` correctly (Zero=7, manual Ord) per record 1249; codifying the constraint as architecture-level guidance is the remaining work.

## Cross-topic edges (sub-agent overlaps)

The sub-agent allocation worked cleanly with three documented edges:

- **`/49` (system-designer)** — schema-arc body in sub-agent A's scope; Spirit search body in sub-agent C's scope. Both sub-agents recommend Keep with cross-references; the status-banner this sweep adds covers both angles.
- **`cloud-operator/11`** — cross-cuts schema-stack (sub-agent A) and deploy-stack (sub-agent B). Both recommend Keep (audit-current).
- **`system-operator/166` (DJI) + `cloud-operator/13` (pi-harness-abort)** — flagged by sub-agent B as not-deploy-stack; sub-agent D handles them under §A standalone components. No conflict; the reports are in different sub-agents' scopes by design.

## What this sweep ratifies vs originates

- **Ratifies** (already self-done by other lanes):
  - designer/415 + designer/439 schema-stack cleanup
  - **operator/260** deep cleanup retiring 38 reports (parallel with this sweep — `mokrklnw`)
  - system-operator/173 absorbing 172 + 169
  - cloud-designer/15 lane self-agglomeration
  - production Spirit 0.3.0 deployment (recency + ChangeCertainty + Zero)

- **Originates** (new this sweep):
  - Drop list for the cloud-operator-lane refresh-audit + maintenance ledger (3 reports)
  - Drop call on second-designer/165, §3a call on 176
  - Retirement of 44 itself (in dispatcher's own lane)
  - Status-banner updates to 48 + 49 (in dispatcher's own lane)
  - Re-surface of 351/352 escalation with deployed-ChangeCertainty as concrete mechanism
  - Operator-action carry of discriminant-stability rule into sema ARCHITECTURE

The successor-pattern observation is now even stronger: **every
active lane self-swept around the schema-stack era shift**
(designer twice, operator once, system-operator once,
cloud-designer once). The dispatcher's role narrowed from
"issue drops" to "ratify + handle remaining deltas (cloud-operator,
second-designer) + close out the prior dispatcher ledger."

## Closing note — successor pattern

This sweep took less work than 44 did because the receiving
lanes did their own follow-through. The successor-sweep pattern
in `skills/context-maintenance.md` §"Successor sweeps retire
maintenance ledgers" is operating as designed: each sweep is
narrower because the prior sweep's handoffs were applied. As of
this synthesis, every lane that was over-cap at 44 is now
self-cleaned — operator 47→9 (in commit `mokrklnw` parallel with
this sweep), designer 42→22 across 415+439, second-designer 45→2,
system-operator 21→6 (post empty-dir cleanup), cluster-operator
9→1. The cross-lane discipline is converging fast; the dispatcher's
role has shrunk to ratification + ledger-retirement work.

## See also

- `0-frame-and-method.md` — frame, inventory, slot plan, sub-agent discipline.
- `1-schema-derived-stack.md` — sub-agent A: operator 210-259 + designer 421-438 + second-designer 165/176.
- `2-deploy-stack-lojix-horizon-cloud.md` — sub-agent B: lojix/horizon/CriomOS + cloud lanes.
- `3-spirit-and-intent-removal.md` — sub-agent C: Spirit observation/search/removal + intent-removal arc + production deployment witness.
- `4-standalone-and-workspace.md` — sub-agent D: standalone components + workspace discipline + prior maintenance-ledger retirements.
- `skills/context-maintenance.md` — the rule set.
- `reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/` — the prior sweep this supersedes.
- `reports/system-operator/173-deep-context-maintenance-2026-05-30.md` — system-operator's parallel self-sweep.
- `reports/designer/439-context-maintenance-2026-05-30.md` — designer's parallel self-sweep.
