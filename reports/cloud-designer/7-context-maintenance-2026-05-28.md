# 7 — Context maintenance pass (cloud-designer lane)

Kind: Maintenance ledger. Date: 2026-05-28.

A lane-scoped context-maintenance sweep of `reports/cloud-designer/`,
run as a follow-on to the cross-lane sweep
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
(its cloud sub-report is `3-cloud-and-deployment.md`). That sweep
found the cloud lanes "current" and named one cloud-designer drop
plus one migrate; this pass re-verifies rather than trusting it, and
executes only the drops this lane owns. Discipline followed:
`skills/context-maintenance.md` (topic-recency §2, the §3a
design-rationale guard, "dispatcher executes drops ONLY in its own
lane", the landing-gate rule) and `skills/report-naming.md`
(commit-before-delete, supersession).

## Inventory (6 reports + .gitkeep)

| # | Report | Shape | Age | Topic |
|---|---|---|---|---|
| 1 | `1-lane-bootstrap-2026-05-27.md` | flat | 05-27 | Lane registration + still-open scope-definition |
| 2 | `2-cloud-component-design-recap-2026-05-27/` | meta-dir (5 files) | 05-27 | Recap of cloud-component design (4-question survey) |
| 3 | `3-cloudflare-cli-prototype-2026-05-27.md` | flat | 05-27 | First single-shot Cloudflare CLI prototype |
| 4 | `4-fully-working-prototype-cycle-2026-05-27/` | meta-dir (9 files) | 05-27 | mine→implement→audit→grow cycle on cloud |
| 5 | `5-browser-local-ai-design-2026-05-27/` | meta-dir (10 files) | 05-27 | Browser-on-local-AI (Gemma) design + HF prefetch |
| 6 | `6-secret-deploy-and-gemma-2026-05-28/` | meta-dir (6 files) | 05-28 | Secret-deploy discipline + Gemma deploy decision |

The lane is small and almost entirely the CURRENT working arc
(05-27 → 05-28). Topic-recency ranking is single-lane here because
the cloud topic's cross-lane peers (system-operator 156-160,
second-designer 196, third-designer 22) live in OTHER lanes and are
their owners' drops, not mine — see handoffs below.

## Verdicts

### DROP — report 2 (`2-cloud-component-design-recap-2026-05-27/`)

**Verdict: DROP.** Verified superseded by report 4.

- Report 2 is an explicit **recap** ("the psyche's prompt is recap,
  not design" — its `0-frame-and-method.md`) answering four framing
  questions: what IS cloud / scope / settled-vs-open / does code
  exist.
- Report 4's `8-overview.md` re-asks **the same four questions** by
  name ("Same four questions the recap-cycle's …/2-…/4-overview.md
  asked") and re-answers each with strictly MORE substance
  ("Settled significantly more than the previous recap could see").
  Report 4's frame swept the **same 13 settled-design reports** that
  report 2 catalogued, then implemented + audited on top.
- Report 4's `8-overview.md` already lists report 2 as its "Prior
  cycle meta-report" anchor, so the supersession spine is recorded
  on the successor itself.

**§3a design-rationale guard — checked, does NOT apply.** I read all
five of report 2's files. None of them *authors* competing design
alternatives (no Design A/B/C, no Option 1/2 that report 2 chose
between). The structure is:
- `1-spirit-substance.md` — a verbatim recap of 17 cloud Spirit
  records. The records are the permanent source, queryable via the
  Spirit CLI; report 4's scout mined a 47-record superset.
- `2-existing-reports.md` — a catalogue/index of 32 OTHER lanes'
  reports (13 settled / 2 open / 17 adjacent). The underlying design
  alternatives it points at (the `Manage` vs `Mutate/Query` split,
  the meta-signal rename, identity primitives) live in the SOURCE
  reports (third-designer/22, 23, 25) which this pass does not touch.
- `3-repos-and-architecture.md` — recaps the five triad invariants
  (permanent home: `skills/component-triad.md`), the cloud 0.1.0
  deferral list (permanent home: `cloud/ARCHITECTURE.md`), and a
  Cloud-vs-PersonaSpirit-vs-DomainCriome comparison table.
- `4-overview.md` — the synthesis, whose every settled+open position
  (Mutate/Query split, meta-signal rename, identity primitives,
  self-upgrade, the production-first-over-schema-engine decision) is
  carried forward into report 4's `8-overview.md` §"What's settled
  vs open" and the prior cycle's overview §3.

**Landing named (where the substance lives permanently):**
- The four-question recap + settled/open positions → report 4's
  `8-overview.md` (canonical successor) + report 4's
  `2-reports-working-solutions.md` (same 13-report mining, deeper).
- The triad invariants → `skills/component-triad.md`.
- The cloud 0.1.0 deferral list + hard constraints →
  `cloud/ARCHITECTURE.md`.
- The 17 cloud Spirit records → the Spirit store (queryable).
Report 2 is committed in jj history (change `soszrwvzztrw`, "reports:
land cloud designer recap"), so the deletion is recoverable and
satisfies commit-before-delete.

### KEEP — reports 1, 3, 4, 5, 6

- **1 (lane bootstrap).** KEEP. Carries the lane-origin record (intent
  872/873) AND the still-unresolved **lane-scope-definition** question
  ("The psyche has named the lane … but not its scope … awaits the
  next psyche prompt"). Its own stated exit condition is "retire once
  the lane is fully integrated into workspace docs"; that integration
  (the `orchestrate/AGENTS.md` + top-level `AGENTS.md` rows it lists
  as outstanding) is not verified landed, so the bootstrap's open
  items are still load-bearing. Pending-resolution → KEEP.
- **3 (cloudflare-cli prototype).** KEEP. The first single-shot
  prototype; report 4's `8-overview.md` cites it as a live anchor
  ("Prior single-shot prototype report"). It is the direct
  predecessor of the cycle in report 4 and part of the current arc;
  not yet superseded into a permanent home.
- **4 (fully-working-prototype cycle).** KEEP. The newest cloud
  *component* design+impl surface; the canonical successor to report 2;
  carries a live 13-gap next-cycle slate and three open psyche
  questions (Tier-1 slate confirmation, convergent-prototype PR-vs-
  reference-branch, the audit-loop discipline). Current arc.
- **5 (browser-local-AI design).** KEEP. Current design; carries an
  active 4-bead queue (`primary-3dqf`, `primary-1ubd`, `primary-ooh1`,
  `primary-y3is`) and 5 open psyche questions + 7 cloud-operator
  questions. Nothing migrated to permanent yet beyond the shipped HF
  prefetch utility branch.
- **6 (secret-deploy + Gemma).** KEEP. Newest report (05-28). Its
  *discipline* substance (never-show secret handling) HAS migrated —
  see the migration note below — but the report also carries
  **unresolved psyche-review questions** (deploy path: coordinate vs
  bulldoze vs text-only-now; Gemma text-only-vs-multimodal; whether to
  commit the uncommitted `.sops` ciphertext) plus live handoffs to
  system-operator and cloud-operator. Per the discipline, pending
  psyche-review flags stay KEEP until the psyche resolves them. KEEP.

## The cross-lane sweep's MIGRATE recommendation — already satisfied

The cross-lane sub-report `…/44/…/3-cloud-and-deployment.md` flagged
the report 6 secret-handling discipline as a MIGRATE candidate to a
new `skills/secret-handling.md`, asserting "no `skills/secret*.md`
exists today." **That is now stale: the migration has already
happened.** `skills/secrets.md` exists (Craft / Keystroke, authored
2026-05-28) and is registered in `skills/skills.nota` (the entry:
"An agent never sees a secret value. gopass wraps env-vars in the
user session; sops-nix carries secrets to cluster hosts; bridge
stores ciphertext-to-ciphertext; verify by length and exit code,
never by reading."). Report 6's own `5-execution.md` /
`4-overview.md` record landing the skill per intent 1011–1014. So no
migrate action is outstanding for this lane; the discipline has its
permanent home. (Skill named `secrets.md`, not `secret-handling.md`
as the cross-lane sweep guessed — same substance, the sweep simply
predated the landing.)

## What was dropped, and where its substance lives

| Dropped | Permanent landing (verified) |
|---|---|
| `2-cloud-component-design-recap-2026-05-27/` (whole meta-dir, 5 files) | Successor report `4-fully-working-prototype-cycle-2026-05-27/8-overview.md` (re-answers the same 4 questions, deeper) + its `2-reports-working-solutions.md`; triad invariants in `skills/component-triad.md`; cloud 0.1.0 deferral list in `cloud/ARCHITECTURE.md`; the 17 cloud Spirit records in the Spirit store. Recoverable from jj history (change `soszrwvzztrw`). |

Result: cloud-designer 6 → 5 reports (well under the 12-report soft
cap). No substance dropped without a verified permanent landing.

## Handoffs to other lanes (NOT executed here — this lane owns only its own drops)

Carried forward from the cross-lane sweep's cloud sub-report, with
this lane's CONFIRM-absorption verdicts attached:

- **system-operator** owns the drop of `156-160` (Cloudflare API
  research, provider-API scope, signal-foundation, repo-scaffold,
  criome-birth-design), forwarding to the cloud lanes first.
  **CONFIRM-ABSORPTION (this lane's verdict): ABSORBED.** Report 4's
  `2-reports-working-solutions.md` mined system-operator/156-160
  explicitly (cited in its frame + overview); the settled design from
  all five is carried into the live cloud-lane reports + the landed
  `cloud`/`signal-cloud`/`owner-signal-cloud` repos. system-operator
  may drop 156-160 on its next maintenance. (`139` arca-CAS is a
  separate keep-or-migrate for system-operator, not cloud.)
- **second-designer** owns the drop of `196`
  (cloud-component-production-design). **CONFIRM-ABSORPTION: ABSORBED.**
  Report 4 + report 2 both cite 196; its production-first decision and
  runtime-branch description are now in the live cloud lanes and
  `cloud/ARCHITECTURE.md`. second-designer may drop 196 on its next
  maintenance.
- **third-designer** owns the drop of `22/` (cloud-criome design
  research). **CONFIRM-ABSORPTION: PARTIAL — hold.** The settled design
  is absorbed, BUT `22/5-meta-signal-rename-impact.md` carries a
  Minimum-certainty design position **held for explicit psyche
  affirmation** (the `owner-signal-*` → `meta-signal-*` rename, ~169
  symbols). That is an unresolved psyche-review flag and the §3a guard
  applies to the rename survey. Recommend third-designer KEEP `22/`
  (or at minimum preserve `22/5`) until the psyche resolves the
  meta-signal rename; do not blind-drop on the cross-lane sweep's
  forward-then-drop alone.
- **cloud-operator** owns the drop of its own `8`
  (cloud-component-design-recap, frame-only, superseded by its real
  impl `cloud-operator/10`). That is cloud-operator's call on its own
  next maintenance; this lane does not touch it.

## Surfaced to the psyche

1. **Aging psyche-review flags now span the cloud lane.** Three
   distinct undecided items are parked across reports 4, 5, 6 awaiting
   a psyche call, and they gate real work:
   - **report 6 — Gemma/local-AI deploy path.** Coordinate the
     api-key onto system-operator's in-flight `horizon-re-engineering`
     `resolveSecret(Sops)` mechanism (the report's recommendation),
     push it through on `main` now, or deploy Gemma text-only now and
     wire auth separately. Plus: Gemma text-only-now vs block-on-
     multimodal (mmproj not wired); and OK-to-commit the uncommitted
     `goldragon/secrets/local-llm-api-token.sops` ciphertext?
   - **report 5 — browser-on-local-AI.** 5 questions; highest-stakes:
     P5 atlas target host (bead `primary-y3is` can't start without
     it) and P1 the cloud-side GPT-5.5 ↔ browser-use orchestrator
     shape (the directive only completes once decided).
   - **report 4 — cloud component next cycle.** Confirm the ~40-line
     Tier-1 + B2 next-cycle slate vs pivoting to a bigger item; and
     whether the convergent prototype branch
     `designer-cloudflare-cli-prototype-2026-05-27` lands via PR onto
     main or stays a designer reference branch.
   These are KEEP-until-resolved per the discipline; flagging so they
   don't quietly age out.

2. **Lane scope still undefined (report 1).** The `cloud-designer`
   lane was registered (intent 872/873) but the psyche has not yet
   fixed its scope/remit. The apparent natural specialization is
   cloud-component + cloud-deploy design (which is what the lane has
   in fact been doing). A one-line psyche confirmation would let the
   bootstrap report retire.

3. **One cross-lane drop is NOT clean — meta-signal rename.** The
   cross-lane sweep recommends third-designer forward-then-drop `22/`,
   but `22/5` carries the Minimum-certainty meta-signal rename held
   for psyche affirmation. Recommend the rename get an explicit psyche
   decision (affirm at Maximum and execute, or park as an architecture
   "Possible future design") so third-designer can then safely drop
   `22/`. Until then `22/` should be KEPT by third-designer.

## See also

- `skills/context-maintenance.md` — the discipline (topic-recency
  §2, §3a design-rationale guard, dispatcher-executes-own-lane-only,
  landing gate).
- `skills/report-naming.md` — commit-before-delete + supersession.
- `reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
  — the cross-lane sweep that motivated this pass (cloud sub-report
  `3-cloud-and-deployment.md`).
- `skills/secrets.md` — the permanent home of report 6's
  secret-handling discipline (the migrate-candidate the cross-lane
  sweep flagged, already landed).
