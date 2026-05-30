# 1 — Topic: schema-derived stack (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2
(record 921). The schema-derived stack — nota-next → schema-next →
schema-rust-next → emitted Rust + the runtime triad (Signal / Nexus /
Sema) with Plane envelopes — is still the workspace's centre of
gravity. The arc has matured from "vision audits at the door of
implementation" (the surface 44 ranked) into "live implementation
iteration with pair-shaped designer↔operator reports landing on a
2-day cadence" (35+ operator + 18 designer reports since 44, much of
it already absorbed by INTENT.md / per-repo INTENT.md +
ARCHITECTURE.md + Spirit records 1216-1263). Successor to
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/1-schema-derived-stack.md`.*

## 1. Topic arc

The 44 sweep ranked the surface as "INTENT.md absorbed the schema-stack
vision; the older operator/designer pile is now genuinely stale". That
finding still holds for everything it named — but four era-shifts
since then have re-pointed the schema-stack's centre of gravity:

- **Codec opt-in landed** (Spirit records 1236-1238 + 1244, designer
  430 + operator 246/247): rkyv is the universal wire base; NOTA
  codec is opt-in per consumer via Cargo feature on the contract
  crate; daemon binary closure proven zero-NOTA.
- **Daemon-zero-NOTA generalized** (record 1241, designer 431):
  configuration becomes a signal not a CLI argument; daemons grow
  multi-signal-interface surfaces dispatched by a top-level
  "numerator" enum; state-aware startup + standby mode.
- **Assembled schema went live** (records 1243-1246, designer 434 +
  operator 250/251/252): `.asschema` is a real serializable artifact
  (NotaDecode + NotaEncode + rkyv on `Asschema` substructure);
  `AsschemaArtifact` noun shipped; emitter consumes the serialized
  form. Bootstrap stages 2-3 closed.
- **Strict-brace + macro-nodes-as-data + macros-at-NOTA-layer**
  (records 1253, 1256-1263, designer 437/438 + operator 256/258/259):
  the `@`-sigil-inside-brace shorthand RETIRED for being dishonest
  about brace key/value contract; strict pair form `{Topics * Kind *}`
  + value-side `(Derive)`/`*` shorthand; `MacroNodeDefinition`
  carries structural cases as typed data; psyche named the next
  architectural lift — macros are a NOTA-LAYER concept (nota-next
  owns the mechanism; schema-next is one consumer of macros).

The designer lane already executed its own drops via
`reports/designer/415-context-maintenance-2026-05-28.md` (27 drops on
2026-05-28) and
`reports/designer/439-context-maintenance-2026-05-30.md` (12 more
drops today, retiring 421-429 + 432-433 + 436). The current
designer-lane survivors are 430/431/434/435/437/438 (all forward
vision or design-rationale guards) — the lane is back under soft cap.
**The drop work this sweep tracks is now almost entirely in the
operator lane** (47 reports, ~24 in the schema cluster awaiting
retirement) plus the small second-designer residue from before the
era shift.

## 2. Current canonical surface

Permanent docs and live reports that remain load-bearing now:

- **INTENT.md** §"The schema-driven stack" + §"Three schema types,
  three runtime planes" + §"Recurring architectural patterns A-F" —
  absorbed the schema-stack vision via designer/415's migration; still
  the canonical synthesis surface.
- **Per-repo INTENT.md + ARCHITECTURE.md** for `nota-next`,
  `schema-next`, `schema-rust-next`, `spirit-next` — named in
  designer/439 §3 as the landing for the retired designer 421-429.
- **Spirit records** 1216, 1226, 1229, 1232, 1235, 1238, 1241,
  1243-1246, 1253, 1256-1263 — the durable intent the recent push
  captured.
- **Live operator reports** (KEEP):
  - `reports/operator/248-schema-nota-spirit-whole-stack-tour.md` —
    canonical current-implementation walkthrough; the cross-lane
    reference point named in designer/439 §2.
  - `reports/operator/250-asschema-live-artifact-implementation-2026-05-30.md`
    + `reports/operator/252-asschema-artifact-gap-closure-2026-05-30.md`
    — Stage 2-3 implementation evidence.
  - `reports/operator/251-schema-asschema-self-audit-against-designer-434.md`
    — canonical operator self-audit shape; informed
    `skills/designer.md` §"Audit precision".
  - `reports/operator/253-schema-gap-closure-vision.md`,
    `reports/operator/254-schema-stack-big-design-questions.md`,
    `reports/operator/255-schema-next-move-after-leans.md` — forward
    gap-closure vision synced with designer/435.
  - `reports/operator/256-strict-brace-key-value-schema-implementation.md`
    + `reports/operator/258-macro-node-structural-matching-implementation.md`
    — strict-brace + macro-node implementation evidence.
  - `reports/operator/247-designer-worktree-pattern-integration-2026-05-30.md`
    — integration of designer worktrees into operator main.
- **Live designer reports** (KEEP per designer/439 §4 + this sweep):
  430 (§3a guard, codec-opt-in mechanism alternatives), 431 (forward,
  slice 2 on `daemon-zero-nota-2026-05-30` worktree not yet on main),
  434 (forward, Stages 4-5 ahead), 435 (§3a guard + forward, Gap D
  open), 437 (§3a guard, `(Derive)` vs landed `*`), 438 (live forward,
  the next architectural lift to NOTA-layer macro mechanism).
- `reports/designer/341-…` + `reports/designer/363-…` — older §3a
  design-rationale guards the 44 sweep already protected; remain
  load-bearing as retracted-alternative carriers.

## 3. Stale / forward / migrate / keep bands by lane

The dominant action band is operator-lane DROP — 24 reports — with
landings into INTENT.md / per-repo docs / Spirit records / the
newer operator reports above. Smaller bands elsewhere.

### operator lane — the dominant drop pile (24)

The 44 sweep already named operator 170-209 + 216-218 as drops. This
sweep tracks the **new** operator schema reports (210-247) that have
matured into "absorbed by newer operator report + permanent doc".
Pair-shape clusters retire together where called out.

**Already-retired-in-place (no further action — content is the
self-retire pointer):**

| Path | Status | Verified landing |
|---|---|---|
| `reports/operator/224-schema-language-design-and-production-witness-2026-05-28.md` | Body retired; pointer to 229/230/231 | Operator already replaced; safe to delete the stub. |
| `reports/operator/225-schema-macros-as-data-not-black-box-2026-05-28.md` | Body retired; pointer to 229/230/231 + 228 | Operator already replaced; safe to delete the stub. |

**Drop band — the static-snapshot operator triad (229/230/231) plus
its predecessors:**

| Path | Pair-shape | Superseded by | Landing |
|---|---|---|---|
| `reports/operator/229-nota-current-design-2026-05-28.md` | Operator response to designer 421 (which retired in designer/439) | `reports/operator/248-schema-nota-spirit-whole-stack-tour.md` (canonical living implementation state, dated 2026-05-30) + `nota-next/INTENT.md` + Spirit records 1216, 1232, 1259 | nota-next per-repo docs + 248 |
| `reports/operator/230-schema-current-design-2026-05-28.md` | Operator response to designer 422 (retired in 439) | `reports/operator/248` + `schema-next/INTENT.md` + Spirit 1226, 1259 | schema-next per-repo docs + 248 |
| `reports/operator/231-signal-nexus-sema-current-design-2026-05-28.md` | Operator response to designer 423 (retired in 439) | `reports/operator/248` §5 + `spirit-next/ARCHITECTURE.md` | spirit-next per-repo docs + 248 |
| `reports/operator/228-raw-core-schema-example-2026-05-28.md` | Standalone | `reports/operator/248` §"Authored Schema" + the live `spirit-next/schema/lib.schema` fixture | 248 + the actual fixture in the repo |
| `reports/operator/232-schema-on-nota-syntax-layer-2026-05-28.md` | Standalone | `reports/operator/256-strict-brace-key-value-schema-implementation.md` (boundary tightened) + Spirit 1259 | 256 + Spirit 1259 |
| `reports/operator/233-nota-codec-asschema-unification-target-2026-05-28.md` | Pair with 234 | `reports/operator/238-primary-8vzk-shared-codec-spirit-triad-2026-05-29.md` (implementation landed) + `reports/operator/250-asschema-live-artifact-implementation-2026-05-30.md` | 238 + 250 + Spirit 1243-1246 |
| `reports/operator/234-nota-codec-asschema-unification-implementation-state-2026-05-28.md` | Pair with 233 | `reports/operator/238` + `reports/operator/250` | 238 + 250 |
| `reports/operator/235-asschema-scalar-pass-through-implementation-2026-05-28.md` | Standalone | `reports/operator/244-asschema-visibility-and-struct-map-implementation-2026-05-29.md` (TypeReference matured) + Spirit 1226 | 244 + Spirit 1226 |

**Drop band — `@`-sigil syntax era (now superseded by strict-brace):**

| Path | Pair-shape | Superseded by | Landing |
|---|---|---|---|
| `reports/operator/236-string-scalar-floor-and-follow-on-syntax-decisions-2026-05-29.md` | Gap-fill of records 1151, 1153, 1154 | Records captured in Spirit; `@`-sigil portion superseded by strict-brace (Spirit 1259) | Spirit records + 256 |
| `reports/operator/237-primary-8vzk-pipe-declarations-and-fixture-tests-2026-05-29.md` | Standalone (pipe-declaration era) | `reports/operator/243-schema-system-syntax-tests-architecture-2026-05-29.md` (replaced pipe with `@`) then `256` (replaced `@` with strict-brace) | 243 + 256 |
| `reports/operator/238-primary-8vzk-shared-codec-spirit-triad-2026-05-29.md` | Standalone | `reports/operator/241-schema-stack-implementation-pass-2026-05-29.md` + `reports/operator/250-asschema-live-artifact-implementation-2026-05-30.md` | 241 + 250 |
| `reports/operator/243-schema-system-syntax-tests-architecture-2026-05-29.md` | `@`-sigil pass | `reports/operator/256-strict-brace-key-value-schema-implementation.md` (syntax revised again, Spirit 1259) | 256 + Spirit 1259 |
| `reports/operator/244-asschema-visibility-and-struct-map-implementation-2026-05-29.md` | Standalone (visibility shipped) | `reports/operator/248` §"Current Stack" + `schema-next/ARCHITECTURE.md` + Spirit 1226 | 248 + Spirit |
| `reports/operator/245-derived-member-shorthand-and-newtype-asschema-2026-05-30.md` | `@Type` shorthand era | `reports/operator/256` (value-side `*` shorthand replaced `@Type`, Spirit 1259) | 256 + Spirit 1259 |

**Drop band — pair-shaped audit + response clusters:**

| Path | Pair-shape | Superseded by | Landing |
|---|---|---|---|
| `reports/operator/239-schema-stack-alignment-audit-2026-05-29.md` | Pair with `reports/designer/426` (RETIRED in designer/439) | `reports/operator/241` + `reports/operator/248` | 241 + 248 |
| `reports/operator/240-response-to-designer-426-schema-deep-review-2026-05-29.md` | Pair-response to retired designer/426 | `reports/operator/241` + `reports/operator/248` | 241 + 248 |
| `reports/operator/241-schema-stack-implementation-pass-2026-05-29.md` | Standalone (impl pass) | `reports/operator/248` + commit witnesses in 241 §"Commit Set" | 248 + git history |
| `reports/operator/242-schema-stack-gaps-explained-2026-05-29.md` | Follow-up to 241 | `reports/operator/253-schema-gap-closure-vision.md` + `reports/designer/435` | 253 + 435 |
| `reports/operator/249-schema-stack-tour-comparison-designer-433.md` | Pair-response to retired designer/433 | `reports/operator/248` (the consolidated tour) | 248 |
| `reports/operator/214-refresh-new-reports-and-intent-2026-05-27.md` | Refresh intent ledger | INTENT.md + Spirit records | INTENT.md + Spirit |

**Drop band — the 44-sweep schema-stack pile (not yet retired in-lane):**

| Path | Superseded by | Landing |
|---|---|---|
| `reports/operator/210-schema-framework-walkthrough-part-1-nota-floor-2026-05-27.md` | `reports/operator/248` + INTENT.md §schema-driven-stack | 248 + INTENT.md |
| `reports/operator/211-declarative-schema-macro-implementation-2026-05-27.md` | `reports/operator/255-schema-next-move-after-leans.md` + Spirit 1109, 1263 | 255 + Spirit |
| `reports/operator/212-brace-namespace-and-schema-modules-2026-05-27.md` | `reports/operator/256` (strict-brace) + Spirit 1259 | 256 + Spirit 1259 |
| `reports/operator/213-nota-schema-next-stack-focused-test-design-2026-05-27.md` | `reports/operator/256/258` + Spirit 1180 | 256/258 + Spirit |
| `reports/operator/215-nota-schema-nix-test-representation-2026-05-27.md` | `reports/operator/241` + spirit-next/tests/* | 241 + live tests |
| `reports/operator/219-schema-full-stack-prototype-completeness-audit-2026-05-27.md` | `reports/operator/248` + `reports/operator/239` (itself dropping) | 248 |
| `reports/operator/220-pattern-a-signal-nexus-test-walkthrough-2026-05-27.md` | INTENT.md §Pattern A + `skills/push-not-pull.md` + live tests | INTENT.md + skill |
| `reports/operator/221-schema-at-heart-prototype-restart-2026-05-27.md` | Pair with 222 → `reports/operator/241` + `reports/operator/248` | 241 + 248 |
| `reports/operator/222-schema-at-heart-test-truth-audit-2026-05-27.md` | Pair with 221 → `reports/operator/241` + `reports/operator/248` | 241 + 248 |

**Borderline / Keep within operator (do NOT drop):**

- `reports/operator/246-nota-surface-split-for-lean-daemons-2026-05-30.md`
  — operator's slice-1 codec-opt-in research; pair with designer/430.
  Designer/430 is KEPT as §3a guard, so the operator pair stays as
  the implementation companion until the slice-2 (zero-NOTA daemon)
  branch is also on main and a successor report supersedes.
- `reports/operator/247-designer-worktree-pattern-integration-2026-05-30.md`
  — integration evidence; keep until both worktrees are fully merged
  and the integration pattern is captured in a skill.
- `reports/operator/248-schema-nota-spirit-whole-stack-tour.md` —
  canonical current-state surface; KEEP.
- `reports/operator/250/251/252/253/254/255/256/257/258/259` — the
  current implementation + audit + vision surface; KEEP all. Pair-shape
  notes:
  - 250↔251 (impl ↔ self-audit) — both load-bearing as the canonical
    audit-precision example.
  - 252↔253 (gap-closure impl ↔ vision) — both forward-load-bearing.
  - 256↔257 (impl ↔ comparison-with-designer-437) — keep both until a
    consolidated post-strict-brace report supersedes.
  - 258↔259 (impl ↔ comparison-with-designer-438) — keep both;
    designer/438's macro-node-at-nota-layer vision is still ahead, so
    the comparison is forward-load-bearing.

`reports/operator/223-context-maintenance-skill-audit-2026-05-28/` is
the operator's own maintenance-skill audit; this sweep's overview
(slot 5) tracks it under the "prior maintenance ledgers" handoff.

### designer lane — done in-lane (no action this sweep)

The designer lane has already executed its own drops:

- `reports/designer/415-context-maintenance-2026-05-28.md` retired 27
  schema-stack reports on 2026-05-28.
- `reports/designer/439-context-maintenance-2026-05-30.md` retired 12
  more today (421-429 + 432-433 + 436) per its §3 table with landings.

Surviving designer reports (430/431/434/435/437/438) are the §3a
guards + forward visions named in §2. **No further action this topic
in the designer lane.** Designer 439 itself is the lane's own
maintenance ledger; it retires when a future designer sweep
supersedes — but that's a designer-lane decision, not this sweep's.

### second-designer lane — small residue, mostly absorbed

The 44 sweep already named 19 second-designer schema-stack reports
for DROP. The 165 + 176 reports remain in this lane (the others
already retired during the post-44 cleanup that took
second-designer's count from 45 → 2).

| Path | Pair-shape | Superseded by | Landing |
|---|---|---|---|
| `reports/second-designer/165-designer-counter-ego-audit-2026-05-24.md` | Counter-ego audit of designer cluster (305/307/308/312/317/3/317/4) — all of those designer reports are RETIRED in designer/415 + 439 | All audited targets are gone. The counter-ego PATTERN itself migrated to `skills/designer.md` (per designer/439 §"audit precision discipline"). | skills/designer.md + git history |
| `reports/second-designer/176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` | §3a-style "every part / every method" walkthrough of the schema upgrade mechanism circa 2026-05-25 | `reports/designer/435-vision-for-the-four-remaining-gaps.md` Gap D (SchemaDiff + UpgradePlan still open, but the framing has moved) + Spirit records 950 (upgrade traits) + 1254 (Gap D vision); the older operator/second-operator landing reports it incorporated are already gone | designer/435 + Spirit 950/1254 |

Both are recommended **DROP** when second-designer next does
maintenance — landings are named and substance has either migrated
upward or moved to a different framing. 176 is borderline §3a — it
enumerates an end-to-end mechanism, not competing options — so a
status-banner-and-keep is also defensible if the operator finds the
soup-to-nuts walk valuable as a teaching artifact for the
schema-diff+upgrade work still ahead.

### system-operator lane — minimal residue

`reports/system-operator/173-deep-context-maintenance-2026-05-30.md`
(today's sweep) absorbed the operator/172 schema-stack-and-Spirit
recent-context surface; 173 §"Horizon Schema State" keeps
`reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md`
as the live Horizon-schema evidence report. No drop action in this
lane this topic — 173 already triaged everything.

`reports/system-operator/167-…` is a pair with
`reports/system-designer/42` (audit, RETIRED into
`reports/system-designer/49`) — 167 remains because it's the
working-prototype witness for Horizon/schema integration, not because
it's pair-stale with 42.

### nota-designer, second-operator, third-designer — lane-empty status

Per the dispatcher's frame inventory, these lanes are empty
(retirement candidates). The 44 sweep recorded their schema-stack
drops (nota-designer 8/9; second-operator 190); those drops have
already been applied — the lanes are clear of schema-stack content.
No action this sweep.

## 4. Landing evidence (summary table)

Every operator-lane DROP recommendation in §3 carries either (a) a
named newer operator report whose substance absorbs it (e.g. 248
absorbs 210-222 + 229-234), (b) a permanent INTENT.md / per-repo doc
landing, (c) a Spirit record that captured the durable rule, or (d)
all three. The dominant landing pattern:

| Older report era | Canonical successor | Permanent home |
|---|---|---|
| 210-222 (pre-`@`-sigil walkthrough + audit cluster) | `reports/operator/248-…tour.md` | INTENT.md §schema-driven-stack + per-repo INTENT.md |
| 229-238 (codec-unification target + impl + scalar floor + pipe declarations + shared-codec) | `reports/operator/241` + `reports/operator/250` + `reports/operator/252` | Spirit 1226, 1243-1246; nota-next/schema-next INTENT.md |
| 239-245 (`@`-sigil era audit + impl) | `reports/operator/248` + `reports/operator/256` (next syntax revision) | Spirit 1232, 1235 (`@`-sigil), then Spirit 1259 (strict-brace successor) |

Operator 246-248-250-252-256-258 form the canonical chain through
which everything earlier flows. None of the 24 operator drops loses
substance — the landings are dense.

The second-designer 165/176 drops land in `skills/designer.md`
(counter-ego pattern) + designer/435 (upgrade-mechanism direction has
moved into Gap D framing) + Spirit records.

## 5. Drop ownership / handoff

**When `operator` next does maintenance, the schema-stack drops it
owns are 24 reports** (full list in §3 "operator lane" drop bands):

  - Already-self-retired stubs: 224, 225 (safe to delete; bodies are
    pointers).
  - Static-snapshot triad + adjuncts: 229, 230, 231, 228, 232, 233,
    234, 235 (8 reports — all absorbed by 248 + 244 + 250 + 256 +
    per-repo docs + Spirit).
  - `@`-sigil era + pipe-declaration era: 236, 237, 238, 243, 244,
    245 (6 reports — superseded by 241/248/256 + Spirit 1259).
  - Pair-shaped audit/response/impl clusters: 239, 240, 241, 242,
    249 (5 reports — absorbed by 241 commit set + 248 + 253).
  - 44-sweep residue: 210, 211, 212, 213, 215, 219, 220, 221, 222,
    214 (10 reports — absorbed by 248 + 241 + 255/256/258 +
    INTENT.md + per-repo docs).

  Borderline KEEP (do not drop): 246, 247, 248, 250, 251, 252, 253,
  254, 255, 256, 257, 258, 259 (13 reports). After drops, the
  operator's schema-stack surface lands at ~13 reports plus 217-218
  (already on the 44 drop list — apply if not yet done) — well under
  any soft cap for the topic.

**When `second-designer` next does maintenance, the schema-stack
drops it owns are 2 reports:** 165, 176. The counter-ego pattern has
already migrated to `skills/designer.md`; the upgrade-mechanism
substance has moved to designer/435 Gap D + Spirit 1254.

**designer lane: DONE this topic.** designer/415 (2026-05-28) +
designer/439 (today) executed the lane's schema-stack drops. The
surviving 6 design reports (430/431/434/435/437/438) are forward
vision + §3a guards. No further action.

**system-operator lane: DONE this topic.** system-operator/173
(today) absorbed the schema-stack-touching parts of 172.
system-operator/167 is the kept Horizon-schema evidence report; no
schema-stack drop owed.

**Other lanes (nota-designer, second-operator, third-designer,
cluster-operator, cloud-* lanes): no schema-stack action owed** —
either no schema-stack reports present, or already drained in prior
sweeps. The 44 sweep recorded the last residual drops (nota-designer
8/9, second-operator 190) which were applied.

## 6. Notes for the overview

Two findings the dispatcher's overview should fold in:

- **The schema-stack era shift has fully crossed the landing-gate
  threshold this sweep.** 44 could only flag the older surface as
  "INTENT.md absorbed it; older reports retire". This sweep can now
  retire the *next two layers* of operator reports (210-245) because
  248 + 250-258 are the new canonical operator surface AND the
  per-repo INTENT.md / ARCHITECTURE.md surfaces have absorbed the
  per-component substance per designer/439's §3 landings. The pattern
  to surface: **a major era shift retires reports in waves of ~2-3
  days lag, not all at once**, as the successor surface accrues
  enough substance to absorb predecessors.

- **The pair-shape protocol is now self-stable.** Designer/439 §5
  observed that operator's "implementation report → self-audit pair"
  pattern (250→251, 252→253, 256→257, 258→259) is the canonical
  audit-precision shape (now in `skills/designer.md`). Similarly,
  designer↔operator pairs (designer/438 ↔ operator/258, designer/437
  ↔ operator/256) cluster cleanly: the comparison reports
  (operator/259, operator/257) are forward-load-bearing while the
  next implementation lift is still ahead. **Pair-shape staleness
  rule confirmed:** a pair retires together only when BOTH the
  designer vision has migrated to permanent docs AND the operator
  implementation has landed; if one side is still forward (e.g.
  designer/438 macro-nodes-at-nota-layer is forward; operator/258 is
  schema-local bootstrap), both sides of the pair stay.
