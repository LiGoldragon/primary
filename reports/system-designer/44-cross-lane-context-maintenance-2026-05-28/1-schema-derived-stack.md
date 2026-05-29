# 1 — Topic: schema-derived stack (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2
(record 921). The schema-derived stack — NOTA → schema (`.schema`) →
macro emission → runtime triad (Signal / Nexus / SEMA) → Plane
envelopes — is the workspace's centre of gravity. It threads through
operator, second-designer, designer, second-operator, nota-designer,
and system-operator. This is the largest cluster by far (~90 reports
touch it).*

## The supersession spine (what changed since the 2026-05-27 sweep)

The prior cross-lane sweep (`designer/386/`, 2026-05-27) could only
recommend "migration overdue" because the substance had **not yet
landed** in a permanent doc. **That migration has now happened.**
`designer/415` (2026-05-28) verified and executed it: the whole
schema-stack vision migrated into **`INTENT.md`** across these
sections:

- §"The schema-driven stack" (lines 259-317) — incl. the
  CapnProto-superset / specification-language-more-specific-than-Rust
  framing migrated from designer/367.
- §"Three schema types, three runtime planes" (318-374).
- §"Nexus is the MAIL KEEPER" (375-442).
- §"Signal protocol — universal mail mechanism" (443-468).
- §"The wire architecture is REST-shaped" (469-484).
- §"Schema-emitted Rust mirrors the schema namespace" (485-500).
- §"Recurring architectural patterns A-F" (501-606).

Plus `skills/`: `component-triad.md`, `nota-design.md`,
`rust/methods.md`, `push-not-pull.md`, `actor-systems.md`,
`repo-intent.md`; and per-repo `repos/schema-next/INTENT.md`,
`repos/persona-spirit/INTENT.md`.

**Consequence for this sweep:** the older schema-stack reports across
operator / second-designer / second-operator that the prior sweep
clustered but kept (because nothing carried their substance) are now
**genuinely stale** — INTENT.md and the skills now hold the durable
shape. The honest stale flag for nearly all of them is "superseded by
INTENT.md §<section> + the current-surface report."

## Recency rank (newest canonical at top)

**Current surface (KEEP — protected / live):**

1. `designer/405`-`414` (2026-05-28) — the live SchemaX-audit surface,
   four agents reading in parallel (per designer/415 directive). The
   canonical presentation is `designer/407` (NOTA→daemon bottom-up),
   the engine-in-reality walk is `413`, macro-by-example `410`,
   collections `411/`, plane envelopes `409`, three-engines `408/`,
   gap audit `405/`, Nexus/SEMA fix-prototype `406/`, SchemaX audit
   `414/`. **KEEP all — designer lane, already protected.**
2. `operator/210`-`222` (2026-05-27) — operator's current
   schema-stack implementation surface: framework walkthrough (`210`),
   declarative macro impl (`211`), brace namespace + modules (`212`),
   focused test design (`213`), nix test representation (`215`),
   full-stack completeness audit (`219`), Pattern-A signal-nexus
   walkthrough (`220`), schema-at-heart restart (`221`), test-truth
   audit (`222`). **KEEP the newest few (219-222 + 210-212); the
   middle of this band is collapsing — see operator drops below.**
3. `designer/341` (2026-05-25) — schema-crystallizes-architecture.
   **KEEP — design-rationale guard (§3a): enumerates retracted
   alternatives (P5 InteractTrait retracted record 666; effect-table
   retracted 713-715). Already carries a status banner. Designer
   lane.**
4. `designer/363` (2026-05-26) — nota-from-schema comparison.
   **KEEP — design-rationale guard (§3a): WIDER vs NARROWER
   recursion-floor cut. Banner refreshed by designer/415. Designer
   lane.**

**Stale band (drops, by lane):**

### operator — schema-stack reports (the dominant pile)

The operator schema arc runs 170→222. Everything from **170 through
209** is two-to-three waves behind the current 210-222 surface AND its
substance is in INTENT.md. Recency-stale drops:

| Report | Date | Superseded by | Substance landed |
|---|---|---|---|
| `170` schema-spirit MVP | 05-24 | operator/210-222 | INTENT.md §schema-driven-stack |
| `171` schema-language declaration blocker | 05-24 | resolved; 210-212 | blocker closed; INTENT.md §three-schema-types |
| `172` schema-header node correction | 05-24 | 212 (brace namespace) | INTENT.md §schema-emitted-Rust |
| `173` schema-header namespace + import | 05-24 | 212 + designer/413 | INTENT.md §schema-emitted-Rust |
| `174` v5 schema-import header critique | 05-24 | 212 + designer/413 | INTENT.md §schema-driven-stack |
| `175/` schema-engine-prep | 05-24 | 210-211 | absorbed into engine |
| `176/` schema-macro-upgrade integration audit | 05-24 | 211 (declarative macro) | INTENT.md §schema-emitted-Rust |
| `177` schema-constraint implementation | 05-24 | 211 + collections (designer/411) | INTENT.md Pattern E |
| `179` schema field-override + upgrade constraints | 05-25 | upgrade design landed | second-designer/175-177 + INTENT.md |
| `180/` schema field-name + upgrade context | 05-25 | 211 + designer/410 | INTENT.md §schema-emitted-Rust |
| `181/` fully-schema-and-nota MVP | 05-25 | 219 + designer/407 | INTENT.md §schema-driven-stack |
| `182` second-operator schema node-shape audit | 05-25 | 212 + designer/413 | INTENT.md §schema-emitted-Rust |
| `183` schema engine 338 impl | 05-25 | 210-211 | absorbed into engine |
| `184` schema macro old-emitter audit | 05-25 | 211 (declarative macro) | INTENT.md Pattern C/F |
| `185` schema crystallization impl | 05-25 | designer/341 (banner) + 219 | INTENT.md §schema-driven-stack |
| `192` full-schema Spirit branch | 05-26 | operator/221 + designer/406 | INTENT.md §three-schema-types |
| `193` schema object-pass + v0.3 skill correction | 05-26 | 219 + 222 | skill correction applied; INTENT.md |
| `194` NOTA+schema restack reading | 05-26 | designer/407 + 413 | INTENT.md §schema-driven-stack |
| `195` schema-driven NOTA reader prototype | 05-26 | 213 + designer/413 | INTENT.md §schema-driven-stack |
| `196` schema object-block pass prototype | 05-26 | 219 | absorbed |
| `197` nota-core design refresh + gap audit | 05-26 | 219 (full-stack completeness audit) | INTENT.md §schema-driven-stack |
| `198/` nota-structural-library prototype | 05-26 | 219 + designer/413 | INTENT.md §schema-driven-stack |
| `199` nota-core schema-stack impl target | 05-26 | 219 + designer/405 | INTENT.md §schema-driven-stack |
| `200` latest NotaCore vision after designer/359 | 05-26 | designer/407 (cites retired designer/359) | INTENT.md §schema-driven-stack |
| `201` operator delta after designer/361 | 05-26 | designer/407 (cites RETIRED designer/361) | INTENT.md §schema-driven-stack |
| `202` double-implementation strategy | 05-26 | 219 (cites retired designer/361) | superseded; strategy executed |
| `203` schema-next interface impl | 05-26 | 219 + designer/413 | INTENT.md §schema-emitted-Rust |
| `204` schema components + boundary proof | 05-26 | 219 + designer/408 | INTENT.md Pattern B/D |
| `206` schema-spirit running concept audit | 05-26 | operator/221-222 | INTENT.md §three-schema-types |
| `207` schema local stack + method workflow | 05-26 | designer/413 + 219 | INTENT.md §schema-emitted-Rust |
| `208` schema-stack missing-impl audit | 05-26 | 219 (completeness audit supersedes) | absorbed |
| `209/` refined triad audit opinion | 05-26 | INTENT.md §three-schema-types + component-triad.md | INTENT.md + skill |
| `216/` reporting-topic-agglomeration | 05-27 | this sweep's discipline (record 921 in skill) | skills/context-maintenance.md §2 |
| `217/` nota-schema-spirit design-improvement research | 05-27 | designer/407 + 413 | INTENT.md §schema-driven-stack |
| `218/` schema-runtime-actor upgrade vision | 05-27 | INTENT.md Pattern A/B + actor-systems.md | INTENT.md + skill |

That is **35 operator reports** recommended DROP. Note `200`/`201`/
`202`/`218/`/`216/`/`217/` carry **dead pointers to retired designer
reports** (designer/359, /361) — designer/415 already flagged these
exact reports as cross-lane dead-pointer carriers. Dropping them
resolves the dead pointers cleanly.

**Borderline KEEP within operator:** `205` (spirit-next schema pilot
impl, 05-26) sits one notch above the rest — it's the pilot that
designer/406 fix-prototype built on. Recommend **FORWARD** into the
operator's current 221/222 line if not already absorbed, else DROP.
`213`/`215` (test design + nix test representation) are recent
(05-27) and may still be the operator's live test surface — recommend
**KEEP** pending the operator's own read.

### second-designer — schema-stack + macro-understanding reports

| Report | Date | Superseded by | Substance landed |
|---|---|---|---|
| `164` NOTA schema v3 (vector of root-verb enums) | 05-24 | designer/413 (cites retired schema designs) | INTENT.md §three-schema-types |
| `168` schema-system-from-intent | 05-24 | designer/407 | INTENT.md §schema-driven-stack |
| `169` schema file-shape corrections post-326-v3 | 05-24 | designer/413 | INTENT.md §schema-emitted-Rust |
| `170` schema lowering executor model | 05-24 | `Executor` naming RETRACTED (record 964); designer/408 (three engines) | INTENT.md §three-schema-types |
| `182` schema crate state + version-projection derivation | 05-25 | second-designer/175-177 (upgrade) + INTENT.md | INTENT.md + upgrade design |
| `183` fully-schema-and-nota MVP | 05-25 | designer/407 | INTENT.md §schema-driven-stack |
| `184` fully-schema comprehensive understanding | 05-25 | designer/413 | INTENT.md §schema-driven-stack |
| `188` schema-engine running walkthrough | 05-25 | designer/413 (engine in reality) | INTENT.md §schema-emitted-Rust |
| `189` macro-system broader understanding | 05-25 | designer/410 (macro by example) | INTENT.md Pattern C/F |
| `193` field-naming + module output | 05-25 | designer/413 + 410 | INTENT.md §schema-emitted-Rust |
| `194` bracket-swap enum-vs-struct | 05-25 | nota-design.md §bracket forms | skills/nota-design.md |
| `195` interact-trait + match-as-logic | 05-25 | InteractTrait RETRACTED (record 666; designer/341 banner) | designer/341 (guard) |

**12 second-designer schema reports** recommended DROP. Note `195`'s
InteractTrait substance is preserved as a retracted alternative in
**designer/341's design-rationale guard** — so the rationale survives;
the audit report itself is stale.

### second-designer — counter-ego audit thread (audits of schema reports)

These audits retire when their audited targets retire (prior sweep's
finding; still correct):

| Report | Audits | Recommendation |
|---|---|---|
| `171` audit second-operator/180 schema-v13 | second-operator/180 (gone — not in current inventory) | DROP (target gone) |
| `179` audit operator/180 | operator/180 (DROP above) | DROP (target dropping) |
| `180` audit second-operator/179 schema-lang-v4 | second-operator/179 (gone) | DROP (target gone) |
| `185` audit second-operator/187 nota-shape + upgrade macro | second-operator/187 (gone) | DROP (target gone) |
| `190` audit operator/181 | operator/181 (DROP above) | DROP (target dropping) |
| `191` audit second-operator/190 macro index port | second-operator/190 (KEEP — see below) | DROP (audit absorbed; impl landed) |
| `192` audit operator/182 schema node-shape | operator/182 (DROP above) | DROP (target dropping) |

**7 more second-designer audit reports** DROP. The **counter-ego
audit PATTERN** itself (the value-add finding from the prior sweep)
should migrate to `skills/designer.md` + `skills/operator.md` if not
already — flagged as a MIGRATE candidate for the designer lane, not a
report-keep.

### second-operator — schema reports

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `190` schema-mainline macro index port | 05-25 | designer/410 (macro by example) + operator/211 | DROP — INTENT.md Pattern C/F |

`second-operator/190` is the only schema report left in that lane
(184/186 are orchestrate-upgrade, covered in the persona/runtime
topic; 191 is a context-maintenance ledger covered in workspace
topic). DROP recommended once macro-index substance confirmed in
designer/410 (it is — macro-by-example is the canonical macro doc).

### nota-designer — schema-lowering reports

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `8` nota-schema lowering deviation audit | 05-25 | designer/413 + INTENT.md §schema-emitted-Rust | DROP |
| `9` operator intent-capture audit (schema nota shape logic) | 05-25 | audit complete; record 592 captured the boundary | DROP — verdict delivered, intent recorded |

(nota-designer's bracket-string reports 1-7 are the NOTA-string
topic, covered in the workspace-discipline sub-report.)

## Stale-flag count for this topic

**~57 reports** flagged stale across the schema cluster:
operator 35, second-designer 19 (12 schema + 7 audits), second-operator 1,
nota-designer 2. Every flag is backed by INTENT.md §<section> + a
named current-surface report (designer/407/413/410/408/409/411 or
operator/219-222).

## Drop ownership by lane (handoff)

- **When `operator` next does maintenance, the schema drops it owns are:**
  170, 171, 172, 173, 174, 175/, 176/, 177, 179, 180/, 181/, 182, 183,
  184, 185, 192, 193, 194, 195, 196, 197, 198/, 199, 200, 201, 202,
  203, 204, 206, 207, 208, 209/, 216/, 217/, 218/ (35). Borderline:
  205 (forward-or-drop), 213/215 (keep pending live-test check). This
  collapses the lane's schema pile from ~50 to the ~10 newest
  (210-212, 219-222, +213/215). Dropping 200/201/202/216/217/218 also
  clears the dead pointers to retired designer/359+361.
- **When `second-designer` next does maintenance, the schema drops it
  owns are:** 164, 168, 169, 170, 182, 183, 184, 188, 189, 193, 194,
  195 (schema understanding, 12) + 171, 179, 180, 185, 190, 191, 192
  (audits whose targets retire, 7) = 19. MIGRATE candidate: the
  counter-ego audit pattern → skills/designer.md + skills/operator.md.
- **When `second-operator` next does maintenance, the schema drop it
  owns is:** 190 (macro index port → designer/410).
- **When `nota-designer` next does maintenance, the schema drops it
  owns are:** 8, 9.
- **designer lane: DONE.** designer/415 already executed the
  schema-stack drops (27 reports) on 2026-05-28; 341/363 are durable
  §3a guards, 405-414 are the protected live surface. No further
  action this topic.
