# 3 — Spirit + intent removal + search

*Sub-agent C, system-designer lane (inherited from dispatcher).
Scope: Spirit observation / search / removal surface, intent
capture/log/maintenance discipline, the recency-filter and
Nexus-language search direction, and the intent-removal arc
(`removalCandidates` + `Magnitude::Zero` + tombstone-before-remove +
nominate-path gap). Also the production-spirit signal-surface
migration recommendation from `/home/li/primary/reports/system-designer/43-spirit-signal-surface-168-review.md`
onto the schema-derived stack.*

## Topic arc

This topic split out of sweep 44 because the Spirit surface has
become its own area of active development. The arc has three
strands that braid together in the last 48 hours:

1. **Intent-removal mechanism (record 1093 → 1252).** Hard
   `(Remove N)` landed (1103/1189) and was used to clean 19
   psyche-approved records under tombstone discipline; a parallel
   block (1157–1175) was removed without tombstone and proved
   unrecoverable (redb COW page reuse), motivating the **tombstone-
   before-remove rule** now in `/home/li/primary/skills/intent-maintenance.md`.
   The soft-delete direction crystallized through
   1191/1192/1212/1213/1214/1215/1249: `removalCandidates` =
   `(Exact Zero)` query, with `Zero` a new bare variant on shared
   `Magnitude` (NOT `Option<Magnitude>` / `None`). Record 1249
   corrected the agent-authored 1215 implementation-detail drift
   (Zero must be declared physically LAST in the enum so existing
   rkyv discriminants stay stable; semantic-bottom comes through a
   manual `order_rank` `Ord` impl, not derived `Ord`). Record 1214
   (Maximum, the earliest decisive Zero call) is the lineage's
   anchor; 1215 (Medium, agent-authored) is the implementation
   sketch that 1249 corrects.
2. **Production deployment + recency-with-topic.** As of 2026-05-30,
   production Spirit 0.3.0 now ships `(Exact Zero)` parsing +
   `ChangeCertainty` write-path + a five-field `RecordQuery` carrying
   a `RecencySelection` (`Newest N` / `Since X` / `Window`); landed
   per `signal-persona-spirit 1bb22635`, `persona-spirit c5a3eb9b`
   (tag v0.3.0.1), `CriomOS-home cc6bb3d2`, `CriomOS 1cf0b747`,
   primary skills `180e6f2b`. The whole "recency missing" /
   "removalCandidates inert" framing of /48 and /49 (written
   yesterday and this morning) was overtaken by the production
   deployment that landed in the same day — see GAP 1 below for
   what's new in the gap-set.
3. **Search-direction exploratory (1251).** The psyche framed the
   Nexus engine as the eventual home for adaptive search logic
   (weighted-keyword scoring, topic-touch-frequency-normalized
   recency curves, composable scoring as data per the
   macros-as-data discipline) — connecting the three-engine chain
   proven in horizon-next (`/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`)
   to a future Spirit search engine where `RecordQuery` graduates
   from filter into a small Nexus program.

What changed since sweep 44 specifically: sweep 44 did NOT have
"Spirit" as an explicit topic — Spirit work was distributed under
"schema-stack" and "persona-runtime / spirit-upgrade". This sweep
splits it out because (a) the intent-removal arc became its own
multi-week strand with reports 45/46/47 retired into /48 and (b)
the recency/Nexus direction made search a first-class concern,
not a side-effect of the schema-stack migration.

## Current canonical surface

Newest reports and permanent docs that are load-bearing right now:

**Reports — current canonical:**

- `/home/li/primary/reports/system-designer/48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md`
  — the canonical intent-removal arc landing; tombstone appendix
  (19 records, verbatim), §"Forensic finding" on 1157–1175,
  §"Design rationale preserved" (the A-vs-B alternative weighing),
  §"Implementation audit" with the GAP-1/2/3 enumeration. Source
  of 45/46/47 retirement; itself superseded ONLY at the
  "removalCandidates is inert" framing (now stale per /173).
- `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`
  — §"Spirit search — how filter-mixing works today" + §"Spirit
  search — the next direction" (recency proposal + Nexus framing).
  The Nexus framing is forward-looking and remains live.
- `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md`
  — the operator-lane Spirit production state snapshot (commit
  witnesses, live-probe results), which now supersedes /49's "what's
  open" Spirit-search-continuation list. Sweep 44 didn't have a
  successor production-deploy snapshot for Spirit; /173 is it.

**Permanent docs (load-bearing):**

- `/home/li/primary/skills/intent-log.md` — pre-capture gate +
  working-orders-vs-intent test + Spirit invocation discipline.
  §"When a working order slips in anyway" carries the
  tombstone-first reminder for the removal path.
- `/home/li/primary/skills/intent-maintenance.md` §"Removing a
  record — tombstone first" — the durable rule from /45's
  experience and /46/47's loss; cites /45 (model tombstone
  appendix) and /47 (deletion-durability finding).
- `/home/li/primary/skills/spirit-cli.md` — deployed Spirit surface;
  has been updated with production recency queries per primary
  skill commit `180e6f2b`.
- `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` §"Deletion
  durability — copy-on-write page reuse" — the kernel-level
  irreversibility note that the tombstone rule rests on. Lines
  134-170 carry the empirical confirmation against
  persona-spirit; "capture-before-remove" is named as the
  consumer-layer discipline.

**Spirit records (load-bearing intent for this topic):**

- 1093 (removal capacity asked), 1103 / 1189 (granted +
  implemented).
- 1091 → 1092 → 1103 lineage (append-only-flag-only → working-orders
  discipline → removal supersedes the flag-only rule).
- 1190/1191/1192 (removal-candidate observation + certainty filter
  + soft-process design).
- 1212/1213/1214/1215/1249 (Zero-vs-None iteration; 1214 the
  Maximum anchor; 1249 the discriminant-stability correction).
- 1247/1248/1250/1251/1252 (recency-filter intent + production
  certainty-mutation directive + production
  recency-with-topic directive + Nexus exploratory direction).

## Stale / forward / migrate / keep bands by lane

### system-designer

| Path | Action | Why |
|---|---|---|
| `/home/li/primary/reports/system-designer/48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md` | **Keep** | Carries the 19-record tombstone appendix verbatim (sole copy outside git history per its own §"Context-maintenance disposition" table), the §"Design rationale preserved" (A-vs-B alternative weighing per §3a guard), and the §"Forensic finding" on 1157–1175 with the unresolved "who removed the block" question. The "removalCandidates is inert" framing in §"Implementation audit" is now overtaken by /173 (production deployment landed certainty mutation), but the report's substance — tombstone, forensic verdict, design alternatives, GAP 2 discriminant-stability correction — is durable. Recommend a one-line STATUS-BANNER edit pointing to /173 for the production-deploy update, NOT retirement. |
| `/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md` | **Keep** | Cross-topic with sub-agent A (the schema-stack arc IS this report's main subject). The Spirit-search sections (§"how filter-mixing works today" + §"the next direction") are the canonical recency-filter + Nexus framing reference. Today's-date production deployment in /173 changes parts of §"What's open" Spirit-search-continuation list — recommend a one-line note rather than retirement; the Nexus exploratory direction is unresolved and stays live. |
| `/home/li/primary/reports/system-designer/43-spirit-signal-surface-168-review.md` | **Keep + status-banner** | The designer-class review of operator-lane /168, validating its eight findings and recommending the schema-derived migration as the structural fix. The recommendations 1-4 are still live: (1) tactical naming pass tracks against the audit findings, (2) `signal-persona-spirit` migration onto schema-next/schema-rust-next remains the structural fix, (3) emitter-applies-no-ancestry-rule remains an open emitter task, (4) coordination with record 1053 (query-by-record-number — now LIVE per /173's commit witness `1bb22635`). Status-banner the recommendation 4 as "1053 live; remaining items remain open"; the structural-migration recommendation is the canonical home for the production-spirit migration target. NOT absorbed by /49 — /49 references it from §"Reports kept" but does not duplicate its content. |

### system-operator

| Path | Action | Why |
|---|---|---|
| `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md` | **Keep** (lane's own canonical) | Current operator-lane maintenance ledger; the Spirit production state snapshot is the freshest available. Already records that /172 + the prior 169 directory were dropped in lane. Owned by system-operator lane. |
| `/home/li/primary/reports/system-operator/169-context-maintenance-2026-05-28/` | **(Already dropped by /173)** | The directory is empty per current filesystem; /173 records its absorption. No further action — confirms sweep-44 successor cycle is complete on the system-operator lane. |
| `/home/li/primary/reports/system-operator/172-system-operator-recent-context-and-spirit-query-surface-2026-05-30.md` | **(Already dropped by /173)** | File no longer exists; /173 records the absorption and notes the Spirit gap statements were already stale within the same day after production deployment. Confirms the lane's ledger has closed the loop. |

### designer (pending psyche-review)

| Path | Action | Why |
|---|---|---|
| `/home/li/primary/reports/designer/351-intent-file-tour-2026-05-26.md` | **Keep — pending psyche-review** | Per skill §"Pending psyche-review flags". Carries five explicit flagged items (persona-spirit Reading-actor + auto-tap; persona-spirit database-upgrades-as-auto-migration; signal-frame missing INTENT on main; owner-signal-persona-spirit INTENT gap; workspace auditor-role substrate options). No Spirit record 944+ resolves these (record 944 is the per-repo-INTENT manifestation discipline, which is upstream context for the report but does not resolve the flags). Recommend: stays Keep until psyche resolves or parks the flags as carry-uncertainty in the relevant per-repo INTENT.md / `INTENT.md` §"Possible future …" sections. |
| `/home/li/primary/reports/designer/352-intent-log-audit-2026-05-26.md` | **Keep — pending psyche-review** | Per skill §"Pending psyche-review flags". Carries the D1–D18 duplicate clusters, M1–M5 misalignment groups, and H1–H12 hallucination flags. The highest-impact flag (M1, the schema-defines-effects cluster 660–665 + 663/664 sweep-mandate + 710) is unresolved at the Spirit record level — no consolidated supersession-Correction has landed for 660-665 (the working-orders 1073-1075 in /48's appendix only retired some adjacent records, not the M1 cluster). Several of /352's recommendations are partially honored (1092 captures the working-orders rule; 1103 enables the removal path) but the structural recommendation — "psyche supersede the schema-defines-effects cluster" — is still pending. Stays Keep. |

### operator and others

| Path | Action | Why |
|---|---|---|
| `/home/li/primary/reports/operator/238-primary-8vzk-shared-codec-spirit-triad-2026-05-29.md` | **(Out of scope — sub-agent A)** | Schema-stack work that uses spirit-next as its target component. Spirit-as-runtime-target is sub-agent A's schema-derived-stack scope. Flagged here so sub-agent A handles disposition; this sub-report makes no recommendation. |
| `/home/li/primary/reports/operator/220-pattern-a-signal-nexus-test-walkthrough-2026-05-27.md` | **(Out of scope — sub-agent A)** | Same — Nexus-engine test pattern threaded through the schema-stack walkthrough; not a Spirit-surface report. |

## Landing evidence

For every drop / status-banner recommendation, the landing:

| Item | Substance | Permanent / successor home |
|---|---|---|
| /48 "removalCandidates inert" framing | Production now supports certainty mutation | `/home/li/primary/reports/system-operator/173-deep-context-maintenance-2026-05-30.md` §"Spirit Production State" (commits `1bb22635` / `c5a3eb9b` / `cc6bb3d2` / `1cf0b747` / `180e6f2b` + live-probe results) |
| /48 tombstone discipline | Permanent rule | `/home/li/primary/skills/intent-maintenance.md` §"Removing a record — tombstone first" (already landed; the report is its model) |
| /48 redb-COW finding (from absorbed /45/46/47) | Permanent architecture note | `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` §"Deletion durability — copy-on-write page reuse" lines 134-170 (already landed; includes empirical-against-persona-spirit confirmation) |
| /48 19-record tombstone appendix | Sole copy outside git history | **/48 itself** — this is /48's load-bearing-preserved substance per §3a; do NOT recommend retirement until or unless the appendix moves to a permanent home (none exists today; no recommendation to create one — appendix-in-its-report is the right shape) |
| /48 GAP 2 (discriminant-stability rule) | Spirit record 1249 captured the correction; the rule itself is operator's to land in sema ARCHITECTURE | Not yet landed in `sema` ARCHITECTURE (per /48 §"GAP 2" — "recommend the operator land it there"). Recommend the overview surfaces this as an open operator action (NOT a drop) |
| /49 Spirit-search "what's open" Spirit-search-continuation | Production deployment landed certainty-mutation + recency-with-topic | /173 §"Spirit Production State"; the Nexus exploratory direction (1251) remains open |
| /49 §"how filter-mixing works today" | Updated wire shape | `/home/li/primary/skills/spirit-cli.md` (per primary skill commit `180e6f2b`); /49's deployed-shape snapshot is now historical but useful as the design-rationale-snapshot for the recency-extension |
| /43 production-spirit migration recommendation | Recommendations 1-4 still live | Recommendation (4) — record 1053 — is LIVE per /173 commit `1bb22635`. Recommendations (1)/(2)/(3) — naming pass, schema-derived migration, emitter-no-ancestry — remain open; /43 stays the canonical home |
| /351 and /352 flags | Unresolved per Spirit query | Recommend: stays Keep until psyche resolves or parks as carry-uncertainty (per `/home/li/primary/skills/context-maintenance.md` §"Per item, decide" pending-psyche-review row) |

## Drop ownership / handoff

The dispatcher (system-designer) executes only in its own lane.
Other lanes carry their own actions when they next maintain.

**system-designer lane (dispatcher executes):**

- **No drops.** /48 and /49 both stay; /43 stays. Recommend the
  dispatcher add one-line STATUS-BANNERs to /48 and /49 reflecting
  the /173 production-deployment update, so future readers see
  /173 as the successor for the "what's deployed" question without
  losing /48's tombstone appendix or /49's design-rationale
  snapshot. The status-banner is the §3a-style guard for both
  reports.

**system-operator lane (record action; lane applies on next maintenance):**

- GAP 2 from /48 — the discriminant-stability rule (rkyv-archived
  enum variants must append-at-end + manual `Ord`, never reorder
  or insert mid-list) — should land in
  `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` as a new
  §"Schema evolution — discriminant stability" note (sibling to
  §"Deletion durability"). Owner: operator (owns sema repo).
- /173 stays the lane's canonical Spirit-state snapshot; no further
  action needed on /172 or /169 (both already dropped).
- The remaining open recommendation from /43 — schema-derived
  migration of `signal-persona-spirit` — is a coordinated arc
  (operator amalgamation + the schema-next/schema-rust-next
  emitter improvements); not a context-maintenance drop, but the
  next workitem on this surface.

**designer lane (record action; lane applies on next maintenance):**

- /351 and /352 stay Keep until psyche resolves the flags. The
  designer lane's next maintenance pass should either (a) check
  with the psyche on the flagged items, or (b) park them in the
  relevant per-repo `INTENT.md` §"Possible future …" sections as
  carry-uncertainty if the psyche directs.
- The designer lane's prior maintenance ledger
  (`reports/designer/415-context-maintenance-2026-05-28.md` and
  the newer `439-context-maintenance-2026-05-30.md` per inventory)
  carry their own Spirit-topic disposition; not in this
  sub-report's scope (sub-agent D handles standalone/workspace +
  the prior maintenance ledgers).

**No cross-lane drops required by this sub-report.** /172 and /169
were already absorbed by /173 in the operator lane; no
system-designer action needed.

## Open items not for drop, but flagged for the overview

- **GAP 1 (nominate write-path)** from /48 — the
  `Mutate`/`SetCertainty`/`Nominate` operation on the
  `persona-spirit` write contract — is now PARTIALLY closed per
  /173 ("ChangeCertainty reaches daemon validation"). /48's
  framing should be amended (in the recommended status-banner)
  but the underlying lifecycle question — *which* channel
  (owner-only vs ordinary) and whether it is a general
  certainty-`Mutate` or a dedicated `Nominate` — may be settled
  by the production deployment; verify against the deployed
  wire shape next pass.
- **Nexus-language Spirit search (record 1251)** — exploratory,
  Low certainty. The connection to the three-engine chain
  proven in horizon-next (`/home/li/primary/reports/system-designer/49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`
  §"Beyond recency — Nexus-language adaptive search") is
  load-bearing as the design-rationale link; no drop, no migrate
  — stays live in /49.
- **The 1157–1175 forensic open question** ("who removed the
  block and whether it was deliberate") in /48 §"Forensic
  finding" remains unresolved; the report carries it explicitly
  as inferred-not-proven. Stays Keep.

## See also

- `/home/li/primary/skills/context-maintenance.md` §"Per-topic
  sub-report shape" (the structure this sub-report follows).
- `/home/li/primary/reports/system-designer/50-cross-lane-context-maintenance-2026-05-30/0-frame-and-method.md`
  (the dispatcher's frame).
- Spirit records cited above for the canonical-intent surface.
