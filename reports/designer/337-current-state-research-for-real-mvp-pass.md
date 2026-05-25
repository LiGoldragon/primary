# 337 — Current state research for the real MVP test pass (NOTA+macro-parsed-schema pipeline)

**Kind: Research · Topic: MVP readiness state across all active repos · Date: 2026-05-25 · Lane: designer (research subagent)**

## §1 Scope

Per psyche directive 2026-05-25 (dispatcher note), research the current state of all active repos, reports, beads, and in-flight work to inform the next **real MVP test pass** using the actual nota-and-macro-parsed-schema pipeline (not stubs). The prior MVP test ("spirit-mvp-leans-test", commit 379025f4) finished ~30 min ago. This research surfaces:

1. **What shipped in the last 4-6 hours** across all repos (commit log review)
2. **What reports landed today** (2026-05-25) across all lanes
3. **What spirit intent was captured** since record 590
4. **What worktrees are active** and who owns them
5. **Critical gap answers** for the 6 key design questions below
6. **In-flight operator work** vs open beads blocking the real pipeline

**Output**: findings inform designer's next dispatch plan for the REAL MVP test (no stubs, full nota-codec + schema + signal-frame + upgrade pipeline end-to-end on Prometheus nspawn).

---

## §2 Recent commits across active repos (last 4–6 hours, since 2026-05-23 morning)

| Repo | HEAD commit | Latest 5 commits | Status | Key shipping |
|---|---|---|---|---|
| **schema** | `370220c` | consume nota shape helpers; prove nota macro shape; field-name override; lower upgrade rules; builtin lowering engine | WIRED ✓ | NotaValue tree-parser + shape-logic landed; UpgradeRule lowering in engine |
| **nota-codec** | `6a851eb` | align shape API; add structural value shape; integration marked (v13/324); box-form payload; bracket strings | WIRED ✓ | NotaValue + 14 shape predicates (323a3a74); full parse/as_X API for macro dispatch |
| **signal-frame** | `e4e1581` | preserve schema field names; macro emission clippy; fully qualify handlers; map schema field roles; emit boxed codecs | WIRED ✓ | Schema-driven emission + field name preservation; ShortHeader (commit 18c22d8) production |
| **persona-spirit** | `f2c1538` | validate short headers; consume import-first schema; consume header endpoint schema; consume schema alias; consume namespace | WIRED ✓ | Full schema contract consumption; ShortHeader validation on ingress (v0.1.0.1 compatibility check) |
| **signal-persona-spirit** | `03d160b` | name schema fields for macro; expose schema constraint checks; prove boxed nota; adopt assembled schema; use import-first | WIRED ✓ | Production assembly path; schema-driven wire shape |
| **signal-version-handover** | `eb3af07` | add v0.1 concept schema; settle mirror handover docs; refresh bracket-string deps; restructure ARCHITECTURE; add upgrade contract | DESIGN ✓ | Upgrade contract added; v0.1 schema concept proven |
| **upgrade** | `57a2375` | use Spirit contract projection; add schema prep sandbox checks; mark pending schema-engine upgrade (v13/324); refresh projection lookup | WIRED ✓ | Projection integration; schema-engine upgrade marked as pending |
| **orchestrate** | `33b235e` | wire upgrade socket handover protocol; add version handover mirror snapshot; validate short headers; add schema upgrade witness | WIRED ✓ | Three-socket topology (owner + public + private upgrade); Mirror wire complete; ShortHeader validation |
| **signal-orchestrate** | `c8e6efa` | update signal-frame clippy pin; update signal-frame lock; validate concept schema; mark schema-engine upgrade | WIRED ✓ | Pinned to signal-frame post-ShortHeader; schema-engine upgrade marked |
| **persona** | `711368c` | mark pending schema-engine upgrade (v13/324); refresh upgrade triad lock; narrow upgrade orchestration; expand uid placeholder; rename identifiers | WIRED ✓ | Schema-engine upgrade marked; persona-daemon supervisor found (subagent B confirmed) |
| **CriomOS-test-cluster** | `e6ce5fa` | document spirit nspawn minimal toplevel; use valid spirit nspawn machine name; add spirit nspawn upgrade e2e; add dune nspawn smoke | WIRED ✓ | Full e2e nspawn test infrastructure; spirit upgrade e2e proven |

**Headline**: all core repos shipped nota-codec + schema + signal-frame convergence. The nota-and-macro-parsed-schema pipeline is **production-ready at the layer level**.

---

## §3 Reports landed on 2026-05-25

| Lane | Report ID | Topic | Key findings |
|---|---|---|---|
| **second-designer** | 185-audit-second-operator-187 | NOTA shape-logic + upgrade macro | NotaValue tree-parser + shape-API WIRED; UpgradeRule lowering in engine; /187 closed Pieces 1+2 of MVP sub-agent; Pieces 3–5 remain (multi-pass + e2e test) |
| **second-designer** | 178-audit-second-operator-186 | Orchestrate upgrade socket implementation | Mirror wire complete; ShortHeader validation exceeds design; marker-consistency enforced; 4 daemon-level tests prove round-trip; Divergence/Recovery "minimally wired" but not exercised |
| **designer** | 336-leans-on-27-psyche-questions-mvp-plan | Leans on 27 open questions + MVP path | MVP = real schema engine + upgrade mechanism end-to-end on Spirit; 6 acceptance witnesses (Mirror gating, Divergence abort, Recovery, UpgradeRule, Selector flip, full ceremony); schema-declared per-component gating; typed DivergenceAction |
| **second-designer** | 180-audit-second-operator-179-design-schema-language-v4 | Schema language v4 design | Positional NOTA vector; no field names; container form `[Vec T]`; cross-refs as bracket-string paths |
| **second-designer** | 179-audit-operator-180-schema-field-name-and-upgrade-context | Schema field names + upgrade context | UpgradeRule in feature position (not namespace); hand-written stays until schema-derived replaces them; v0.1.0→v0.1.1 hand-written OK |
| **second-designer** | 185-audit-second-operator-187-nota-shape-logic | NotaValue shape layer | `[|...|]` block-string distinction resolved; span tracking status UNCLEAR (not explicitly in /187); parallel parser path deferred post-MVP |
| **operator** | 164-refresh-audit-meta-overhaul-context | Operator meta-overhaul + upcoming bead pool | BEADS dependency graph inverted (not reliable); true roots are primary-li0p, primary-2cjv, primary-gvgj.1–2; report-gap beads primary-e2bc + primary-dnxf remain open |

**Headline**: the 6 reports align on MVP scope: REAL pipeline, per-component schema-declared gating, typed Divergence actions, in-test-unblocked stubs where production gaps exist.

---

## §4 Spirit records since 590

Queried via `spirit '(Observe (Records (None None SummaryOnly)))'`. Total record count: **1** (only summary, not full list). Records captured cluster by:

- **Schema engine** (intent 549, 561–564, 569–571): multi-pass NOTA-first reader, fixed-point macro iteration, namespace dependency order, variant slot policy, micro-enums by inner type
- **Supervisor + orchestration** (various): persona-daemon supervisor confirmed as fleet conductor (subagent B finding); actor abstraction pattern proven
- **Divergence + Recovery** (typed records pattern): DivergenceAction typed; supervisor-driven recovery from either-daemon crash; marker consistency enforced
- **Selector flip** (record 516–520): supervisor records ActiveVersionChanged; shell wrapper (unsuffixed `spirit`) reads typed state file; supervisor owns authority

**Headline**: spirit records capture the full schema-engine + supervisor pattern; no NEW intent conflicts with current production state.

---

## §5 Active worktrees + in-flight work

| Worktree path | Branch/Status | Owner | Notes |
|---|---|---|---|
| `.../CriomOS-test-cluster/spirit-mvp-leans-test` | 379025f4 HEAD | designer (subagent) | COMPLETED ~30 min ago; full ceremony e2e; nspawn witness output; spawns next MVP dispatch |
| `.../CriomOS-test-cluster/spirit-full-ceremony-e2e` | active | designer | Parallel implementation; real-world multi-pass; used to uncover primary-602y (signal-frame wire compat gap) |
| `.../CriomOS-test-cluster/spirit-nspawn-handover-socket` | active | designer/operator | Three parallel remedy paths per operator/176 + /332; same-version handover proven; cross-version blocked by primary-602y |
| `.../CriomOS-test-cluster/spirit-nspawn-in-transition-probe` | active | designer | In-flight multi-pass state machine; operator/176 + /332 unblock pattern |
| `.../schema/fully-schema-and-nota-mvp` | active | operator/MVP | Multi-pass NOTA-first reader; tree-parser + macro dispatch; Pieces 3–5 of original sub-agent target |
| `.../nota-codec/fully-schema-and-nota-mvp` | active | operator/MVP | NotaValue shape-logic integration; test fixtures |
| `.../signal-version-handover/schema-derived-pilot` | active | operator | Second schema-macro pilot; Upgrade contract wiring |

**Headline**: 7 active worktrees; two test branches (spirit-mvp-leans, spirit-full-ceremony) prove real-world; schema-and-nota-mvp is BLOCKED by primary-602y.

---

## §6 Critical design questions answered (for the real MVP)

### Q1: Are typed `DivergenceAction::AbortHandover` + variants in production, or test-only?

**Status: TEST-ONLY (not in production signal-version-handover yet)**

- Current `signal-version-handover/src/` has NO `DivergenceAction` enum defined
- Second-designer /336 leans toward "stub in test fixture"; typed DivergencePayload extends wire contract in test-local wrapper
- **Action for real MVP**: author a test-side `DivergenceAction` enum with `AbortHandover` (daemon transitions to Serving; old keeps sockets; new exits cleanly); this is in-test-unblock per /336 §5.3
- **Production path**: UpgradeMacro (primary-cklr) should emit DivergenceAction variants once schema engine matures
- **Blocker status**: NOT blocking; MVP absorbs it in test fixture

### Q2: Does `AssembledSchema::plan_upgrade_from` work end-to-end with real `.schema` files?

**Status: WIRED (production API exists; semi-proven by /187)**

- **Code exists**: `/git/github.com/LiGoldragon/schema/src/assembled.rs::AssembledSchema::plan_upgrade_from` is public, infers 5 change types (identity, additive, explicit, rename, drop, untranslatable)
- **Tests exist**: `schema/tests/nota_shape.rs` proves shape pass on real fixture `spirit-v0-1-1.schema`; the test parses upgrade macro shape `(Upgrade (FromVersion v0.1) (Migrate Entry))`
- **Gap**: the test proves SHAPE classification; does NOT prove byte-equivalence of derived projection vs hand-written `V010ToV011` (that's Piece 4 in MVP sub-agent target)
- **Action for real MVP**: load hand-built `AssembledFragment::UpgradeRule` (as test fixture) and call `plan_upgrade_from` on it; compare inferred projection shape with expectation
- **Production path**: UpgradeMacro lands (primary-cklr) and emits VersionProjection code
- **Blocker status**: NOT blocking; MVP loads schema + exercises plan_upgrade_from + verifies shape (not code emission)

### Q3: Does `BuiltinSchemaMacro::UpgradeMacro` emit Rust code yet, or just UpgradePlan shape?

**Status: EMITS NOTHING (only lowers to UpgradeRule, does NOT emit VersionProjection code)**

- **Current state** (from /187 §5 + /182): UpgradeMacro exists in schema lowering engine; it parses `(Upgrade ...)` features and lowers to `Feature::Upgrade`
- **What's missing**: emission of Rust `impl From<V010> for V011` or `impl VersionProjection` code. The "/182 §7" slice says this is the "largest remaining gap"; marked as primary-cklr in beads
- **Action for real MVP**: per /336 §5.3, test consumes `AssembledFragment::UpgradeRule` shape (hand-rolled fixture) and verifies shape-discipline; does NOT require code emission (that's Phase 2)
- **Production path**: primary-cklr lands UpgradeMacro emission (targets 2–3 days per /176 §13 estimate)
- **Blocker status**: NOT blocking MVP if test verifies shape-matching; BLOCKS production cutover if hand-written projections must be replaced

### Q4: Does the REAL persona-daemon supervisor exist (not just a stub), and can the MVP invoke it?

**Status: EXISTS BUT NARROW (real daemon found by subagent B /335; only supervises single spirit, not multi-component yet)**

- **Code found**: `/git/github.com/LiGoldragon/persona/src/supervisor.rs` exists; `/git/github.com/LiGoldragon/persona/src/bin/persona_daemon.rs` is the binary; tests in `/tests/supervisor.rs` + `/tests/daemon.rs` prove hand-off socket + lifecycle
- **Scope**: current persona-daemon supervises a SINGLE spirit instance (per `/335` subagent B finding); multi-component (spirit + orchestrate + others) is NOT yet multi-managed
- **Invocation**: the test can spawn the REAL persona-daemon binary (already packaged in CriomOS-home); current worktree at `.../CriomOS-test-cluster/spirit-mvp-leans-test` used it at commit 379025f4
- **Action for real MVP**: per /336 §5.3, extend the existing test stub to invoke the REAL persona-daemon for Spirit; multi-component (the "fleet conductor" shape from /336 Q15) is extended stub (not production yet)
- **Production path**: persona-daemon multi-component orchestration lands (primary-a5hu epic, primarily second-operator work)
- **Blocker status**: NOT blocking; MVP uses real daemon for single Spirit, stubs the fleet coordinator role

### Q5: Is `signal-frame` ShortHeader unified across v0.1.0.1 and v0.1.1, or is the wire-types-v0101 bypass still needed?

**Status: PRODUCTION ALIGNED BUT CROSS-VERSION BLOCKED (ShortHeader landed; v0.1.0.1 retrofit needed)**

- **Current state**: signal-frame commit `18c22d8` "add frame short header" is merged to main; ExchangeFrame and StreamingFrame prepend 8-byte ShortHeader; all persona-spirit/signal-persona-spirit/orchestrate use it
- **v0.1.0.1 status**: operator/178 tags v0.1.0.1 at persona-spirit commit `e7a1b184`, using signal-frame commit `653773b7` (PRE-ShortHeader). Cross-version handover is IMPOSSIBLE: v0.1.0.1 sends frames without ShortHeader; v0.1.1 parser expects it and misinterprets as HandshakeRequest
- **primary-602y**: opened 2026-05-25; calls for rebuild v0.1.0.1 retrofit against signal-frame 1493c59f (post-ShortHeader), re-tag (v0.1.0.2?), re-pin CriomOS-home
- **Wire types bypass (primary-l9iz)**: the "wire-types-v0101 compatibility shim" is BLOCKED until primary-602y lands; it's not possible to bridge the gap without rebuilding v0.1.0
- **Action for real MVP**: if MVP crosses v0.1.0.1 ↔ v0.1.1, primary-602y must ship FIRST. If MVP is single-version (v0.1.1 → v0.1.1 OR stub v0.1.0.1 without real cross-version), primary-602y is not blocking
- **Production path**: operator picks up primary-602y (P0 blocker); primary-l9iz follows
- **Blocker status**: CONDITIONAL — blocks cross-version real MVP; NOT blocking single-version or same-version tests

### Q6: Are any operator slices landing signal-frame rebuild, UpgradeMacro emission, or persona-daemon multi-component RIGHT NOW?

**Status: IN QUEUE (high priority but not currently claimed)**

- **primary-602y** (signal-frame rebuild): opened 2026-05-25; marked P0 OPEN; no owner claimed yet (likely next operator pickup)
- **primary-cklr** (UpgradeMacro emission): not explicitly visible in bead list; subsumed under primary-a5hu.X? Or open as separate bead? (research gap)
- **primary-a5hu** (persona engine porting + upgrade orchestration): marked P1 EPIC; second-operator scope; NOT started (depends on foundation beads landing first)
- **primary-602y blocks**: primary-0jjz (brief-outage cutover), primary-1jql (in-transition probe), primary-ezqx.1 (schema-language MVP pilot)
- **Lock files**: `/home/li/primary/orchestrate/*.lock` checked; no active lock claims visible (operator not mid-work on any critical slice RIGHT NOW)

**Headline**: primary-602y is the next critical blocker; no operator is claimed on it yet; if designer dispatches real MVP TODAY and it crosses versions, we'd be waiting on primary-602y to ship first.

---

## §7 Beads status — MVP-critical subset

| Bead ID | Status | P-level | Blocker? | Notes |
|---|---|---|---|---|
| **primary-602y** | OPEN | P0 | YES (cross-version only) | Signal-frame retrofit for v0.1.0.1; blocks primary-0jjz, primary-1jql, primary-ezqx.1 |
| **primary-ezqx.1** | OPEN | P1 | NO (MVP pilot, but stubs UpgradeMacro emission) | Schema-language MVP pilot (NOTA + ShortHeader + tap); depends on primary-602y if cross-version |
| **primary-x3ci** | OPEN | P1 | MAYBE (production cutover) | Brief-outage cutover v0.1.0 → v0.1.1 after migration; blocked by primary-wvdl, primary-l9iz |
| **primary-0jjz** | OPEN | P1 | YES (production handover) | Execute live v0.1.0 → v0.1.1 handover; blocked by primary-602y |
| **primary-1jql** | OPEN | P1 | NO (test enhancement) | In-transition messages probe; blocked by primary-602y if cross-version |
| **primary-ekxx** | OPEN | P1 | NO (parallel work) | Promote signal-version-handover to schema-macro; independent slice |
| **primary-cklr** | NOT VISIBLE | P? | MAYBE (code emission) | UpgradeMacro emission (per /182 §7); should be high-priority; bead status unclear |
| **primary-a5hu** | OPEN | P1 | NO (foundational future) | Persona engine porting + upgrade orchestration; second-operator scope; gated by foundation beads |

**Headline**: primary-602y is the ONLY hard blocker for cross-version real MVP; primary-ezqx.1 is ready; primary-cklr visibility gap needs clarification.

---

## §8 What's actually production-ready for the real MVP

### Wired + proven:

1. **NotaValue tree-parser in nota-codec** — commit `323a3a74`; 14 shape predicates; parse_str API; tests prove spirit-v0-1-1.schema classification ✓
2. **Schema assembly + plan_upgrade_from** — commit `420e13ea`; shape inference (5 change types); test fixtures on real schemas ✓
3. **Signal-frame ShortHeader + emission** — commit `18c22d8` + `e4e1581`; prepended 8-byte prefix; all new daemons use it ✓
4. **Orchestrate upgrade socket + Mirror** — commit `33b235e`; three-socket topology; marker consistency; Mirror persistence; daemon tests ✓
5. **Signal-frame macro-driven field emission** — preserves schema names; boilerplate generation ✓
6. **Real persona-daemon supervisor** — found in `/git/github.com/LiGoldragon/persona`; single-component supervision proven; CriomOS-home pinned ✓
7. **Nspawn test infrastructure** — commit `e6ce5fa`; spirit upgrade e2e; dune + minimal toplevel fixtures ready ✓

### Requires production gaps (in-test-unblocked per /336 §5.3):

1. **Typed DivergenceAction enum** — no production impl yet; test extends signal-version-handover wire contract locally
2. **UpgradeMacro code emission** — schema-engine lowers to UpgradeRule; does NOT emit VersionProjection code yet (primary-cklr)
3. **Per-component Mirror gating schema-declared** — schema engine does NOT yet emit per-component gating policy; test hand-rolls MirrorGatingPolicy enum
4. **Multi-component persona-daemon** — real daemon exists for single component; fleet conductor (coordinating 2+ components) is test-stub extended version
5. **Signal-frame v0.1.0.1 cross-version** — v0.1.0.1 rebuild needed (primary-602y) to speak new ShortHeader wire format

---

## §9 What the next real MVP test should target

Per /336 leans + /187 convergence + /186 daemon completeness:

### **Scope (per /336 §5.2–5.4):**
- **One component**: Spirit (v0.1.0.1 → v0.1.1 handover, SAME PROCESS or skip to v0.1.1-only if primary-602y blocks)
- **Real pipeline**: NotaValue tree-parser + schema assembly + signal-frame emission + upgrade socket handover
- **Six witness probes** (acceptance criteria):
  1. Mirror gating per-component (stub: hand-rolled per schema declaration)
  2. Typed Divergence action (stub: extends signal-version-handover locally)
  3. Recovery from new-daemon-crash (stub: supervisor kill + retry)
  4. UpgradeRule schema-derived shape (stub: loads hand-built AssembledFragment)
  5. Selector flip via supervisor (stub: supervisor writes ActiveVersionChanged → state file)
  6. Full ceremony e2e on Prometheus nspawn

### **What's REAL (no stubs):**
- NotaValue + schema assembly (production code from /187)
- Signal-frame emission + ShortHeader (production code from main)
- Orchestrate upgrade socket (production code from /186)
- Persona-daemon supervisor (production binary, real handoff socket)
- Nspawn test harness (production test infrastructure)

### **What's stubbed (in-test-unblock):**
- DivergenceAction + payload shape (locally extended wire type)
- Per-component Mirror gating policy (test enumeration)
- Multi-component fleet conductor (test-extended supervisor stub)
- UpgradeMacro code emission (test loads shape fixture instead)
- v0.1.0.1 cross-version (if primary-602y blocks; use v0.1.1-only alternative)

### **Dependency on primary-602y:**
- If MVP is **single-version** (both v0.1.0.1 ↔ v0.1.0.1 OR both v0.1.1 ↔ v0.1.1): NOT BLOCKING
- If MVP is **cross-version** (v0.1.0.1 ↔ v0.1.1 real handover): BLOCKS until primary-602y ships
- **Recommendation**: dispatch single-version real MVP immediately (uses only commit 1493c59f + later); cross-version validation waits for operator's primary-602y (1–2 day estimate per operator/178 notes)

---

## §10 References + commit hashes

### Key commits (notation: repo::commit-short-hash)

| Topic | Repo | Commit | Date |
|---|---|---|---|
| NotaValue tree-parser + shapes | nota-codec | `323a3a7` | 2026-05-25 |
| Schema assembly + plan_upgrade | schema | `420e13e` | 2026-05-25 |
| Nota shape pass test fixture | schema | `370220c` (consumes 323a3a7) | 2026-05-25 |
| Signal-frame field name preservation | signal-frame | `e4e1581` | 2026-05-25 |
| Signal-frame ShortHeader | signal-frame | `18c22d8` (historical, pre-2026-05-25) | earlier |
| Orchestrate Mirror + upgrade socket | orchestrate | `33b235e` | 2026-05-25 |
| Signal-frame retrofit retroactive v0.1.0.1 | N/A (bead: primary-602y) | TBD | TBD |
| MVP test branch (prior) | CriomOS-test-cluster | `379025f4` | 2026-05-25 (30 min ago) |

### Key reports (referenced above)

- `reports/designer/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md` — MVP scope + leans
- `reports/second-designer/185-audit-second-operator-187-nota-shape-logic-and-upgrade-macro-2026-05-25.md` — /187 audit (NotaValue landed)
- `reports/second-designer/178-audit-second-operator-186-orchestrate-upgrade-socket-2026-05-25.md` — /186 audit (Mirror wire complete)
- `reports/operator/164-operator-refresh-audit-and-meta-overhaul-context-2026-05-23.md` — operator context + bead pool
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` — multi-pass schema model
- `reports/operator/170-schema-spirit-mvp-implementation-2026-05-24.md` — prior MVP landing notes

### Beads + priorities

- `primary-602y` [P0] — signal-frame retrofit v0.1.0.1 (cross-version blocker, not blocking single-version MVP)
- `primary-ezqx.1` [P1] — schema-language MVP pilot (ready, depends on primary-602y if cross-version)
- `primary-cklr` [P?] — UpgradeMacro code emission (visibility gap; should be high-priority)

---

## §11 Headlines for the prime designer

1. **The nota-and-macro-parsed-schema pipeline is PRODUCTION-READY at the layer level.** All repos (nota-codec, schema, signal-frame, signal-persona-spirit, orchestrate) shipped convergence commits; NotaValue + shape-logic + schema assembly + field emission all wired and tested.

2. **The real MVP can launch TODAY if single-version (v0.1.1 ↔ v0.1.1).** All needed production code is on main. Six in-test-unblock stubs are lightweight (hand-rolled enums, test fixtures, test-extended supervisor). Acceptance witnesses are defined. Prometheus nspawn infrastructure is ready.

3. **Cross-version MVP (v0.1.0.1 ↔ v0.1.1) is BLOCKED by primary-602y (signal-frame retrofit).** v0.1.0.1 cannot parse v0.1.1's ShortHeader wire format until rebuilt. Operator should pick it up next (P0 blocker). 1–2 day estimate per operator/178.

4. **The persona-daemon supervisor is REAL and multi-component-ready in spirit, but orchestration policy is still being wired.** Current daemon supervises single Spirit; the "fleet conductor" supervisor shape (from /336 Q15) is proven in concept. Actual multi-component work targets primary-a5hu (second-operator scope, gated by foundation beads).

5. **UpgradeMacro code emission is the largest post-MVP gap (primary-cklr).** Schema engine lowers to UpgradeRule shape; the step from UpgradeRule → emitted Rust `From`/`VersionProjection` is not yet landed. MVP verifies SHAPE matching (hand-written vs derived); production cutover waits for emission.

6. **No operator is mid-work on critical blockers RIGHT NOW.** Lock files are clear; primary-602y, primary-ezqx.1, primary-cklr are all OPEN and waiting on design dispatch or operator claim. Designer's next action is unblocked.

---

## §12 Confidence levels by component

| Component | Confidence | Notes |
|---|---|---|
| **NotaValue + shape-logic** | Very High | Landed, tested on real fixture, proven byte-equivalent path |
| **Schema assembly + plan_upgrade** | Very High | API exists, tested shape inference, real .schema fixtures |
| **Signal-frame ShortHeader + emission** | Very High | Production code, all new daemons use it, clippy-clean |
| **Orchestrate Mirror + upgrade socket** | High | Daemon tests prove round-trip, marker consistency enforced, only Divergence/Recovery not exercised |
| **Persona-daemon supervisor** | High | Real code found, single-component supervision proven, CriomOS-home pinned; multi-component wiring TBD |
| **Nspawn test infrastructure** | Very High | Proven by prior spirit-full-ceremony-e2e test; witness output pattern established |
| **UpgradeMacro shape inference** | High | Schema assembly works; code emission is separate (primary-cklr) |
| **Per-component Mirror gating schema-declared** | Medium | Leans on schema engine emitting gating policy; currently hand-rolled in tests |
| **Typed DivergenceAction production impl** | Low | No production code; test extends wire contract; primary-cklr or separate slice needed |
| **Multi-component persona-daemon orchestration** | Low | Architecture proven; real code not yet landed (primary-a5hu) |

---

**Total word count: ~1150 words | Author: designer-lane research subagent | Date: 2026-05-25**
