# 113 — criome ↔ spirit session: full context summary (2026-06-16)

*Psyche-facing summary of a single system-designer session that reanimated the
criome subject in the context of spirit, produced a concept + decisions, did a
multi-record intent reconciliation, took the intent-substrate decision, and
surfaced a deployed-daemon bug. Requested by the psyche as a full-context report.
The deep concept lives in `112-criome-spirit-auth-concept/`; this is the session
narrative and the current ledger.*

## The arc, in order

1. Psyche: "spirit needs authentication; criome is how we authenticate anything;
   it's a perfect pilot. Once an operation passes the guardian, it asks criome to
   authorize it; criome signs the content-addressed log entry — whatever works."
   Plus a second, separable thread: "read intent should mean read spirit — I want
   intent to live in Spirit, not files, so we search one place; ARCHITECTURE.md
   keeps the architecture."
2. I ran the Spirit gate, located the criome stack, ran a 9-agent designer workflow,
   and produced the concept (`112`).
3. The system-operator joined (`reports/system-operator/223`) and gap-filled Spirit;
   a parallel-capture reconciliation followed.
4. Psyche decided the four issues; I captured the settled mechanism and the substrate
   decision.
5. Psyche corrected my framing (intent primacy is unchanged) and my Spirit hygiene (a
   clarification is an *edit*, not a new record); I fixed the log and hit a daemon
   bug in the edit path.

## 1 — The criome ↔ spirit concept and the decisions (detail in `112`)

**Headline finding:** criome's cryptographic core is a *skeleton* — signing emits the
literal placeholder `criome-skeleton-bls-signature`, verify always fails,
authorization always returns `Pending`, and there is no caller authentication on the
socket. So the pilot's deepest meaning is that **spirit is the forcing function that
makes criome grow its first working BLS core**.

**Corrected concept** (the workflow's first synthesis was caught failing the goal — a
log-witness authenticates criome's key, not the submitter): an **after-the-fact,
non-blocking, out-of-band attestation binding the SO_PEERCRED caller to the exact
per-operation content-addressed digest**. criome verifies bytes+principal; the
guardian keeps the full content verdict; three authorities stay separate
(socket / criome / guardian).

**Psyche-ratified decisions:** A — principal is the **caller/submitter** (not the
log). B — timing is **after-the-fact, non-blocking** (the before-commit gate is
deferred; criome's authorization is async-by-design and `meta-signal-criome` doesn't
exist). C — criome signs the **per-operation digest** (matches "signature on the log
entry"). D (my recommendation, for veto) — a criome *denial* always rejects; criome
*unavailable* → attest-later with a visible `unwitnessed` provenance class, never
silent.

## 2 — Intent ledger after this session

| Record | Kind | State | Substance |
|---|---|---|---|
| `w2g3` (operator) | Decision | **live** | Spirit is an early pilot consumer of criome-backed operation authorization over exact content-addressed digests; envelope was open. Canonical pilot record. |
| `2st7` (mine) | Decision High | **live** | The settled pilot mechanism (A+B+C); settles `w2g3`'s open envelope. |
| `15df` (mine) | Correction High | **live** | The intent-substrate decision (E): intent's single source is Spirit; ARCHITECTURE.md is the per-repo doc; INTENT.md migrates off gradually. |
| `cdd3` | Principle | **zeroed** | "Intent lives in the file that owns its scope" — explicitly superseded by `15df` (recoverable). |
| `kxdz` (mine) | Decision | **zeroed** | "criome universal authenticator + spirit pilot" — content-duplicate of `w2g3` + pre-existing `a4i6`/`q1cw` (recoverable). |
| `6x6h` (mine) | Clarification | **removed** | The primacy clarification I wrongly added as a *separate* record; deleted per the psyche's hygiene correction. |

Pre-existing intent the pilot rests on (the domain-routed neighborhood, not keyword
"authentication"): `a4i6` (every component can escalate to criome; criome's public
key is the authentication anchor), `9v7h` (SO_PEERCRED owner-socket auth, fail-closed),
`q1cw`/`i9qv`/`jtmt` (criome identity is the existence-verification surface; the public
key is the identity).

**The discipline lesson (applied, not logged per your note):** a Clarification is an
**edit** of the record it refines, not a second record stacked beside it. I stacked
`6x6h` on `15df`; the fix is to delete `6x6h` (done) and edit `15df` in place.

## 3 — The intent-substrate decision and the spirit.md proposal

Decision E is **Yes** (`15df`, High): Spirit is the single source of truth for intent.
Two clarifications shaped it:

- **Primacy is unchanged.** Intent stays the highest, first-read thing per repo —
  AGENTS.md's "INTENT.md is the first/most-important file" stays true in its *rank*;
  only the *substrate* moves (a per-repo file → Spirit). I had wrongly called this a
  contradiction; it is not.
- **The `spirit.md` proposal** (your "we could", logged as *exploratory* on bead
  `ebev`, not as settled intent): a per-repo `spirit.md` — a versioned, timestamped
  snapshot of the repo's intent **generated by a spirit utility client**. This kills
  dual-maintenance (Spirit is the source; `spirit.md` is a derived view), scopes a
  repo's intent by **referent** (where `cdd3`'s scope insight survives), and carries
  version+timestamp on the snapshot *header* (generated-at + store Marker) since
  Spirit records carry no per-record time. **Open: adopt it as the rollout mechanism?**

## 4 — Deployed-daemon bug found: the Clarify edit path is broken

Attempting the in-place edit of `15df` via `Clarify` returned:
`sema database engine error: sema: schema version mismatch — file was written with v9,
this build expects v10`. `Record`, `Remove`, and `ChangeCertainty` all succeed on the
v10 store this same session — so a store the **edit operations** touch (`Clarify`, and
likely `Supersede`/`Retire`/`Propose`, which share the lineage path) was **not migrated
v9 → v10** in the 0.13.0 deploy. Consequence: **intent cannot currently be edited or
superseded on the deployed daemon** — only recorded, removed, or re-graded. This is a
production issue for the system-operator (it compounds the "no operator deploy report"
gap from report 109). `15df` is correct as written (it never demoted intent), so the
log is clean regardless; the explicit primacy wording could not be folded in until
Clarify is fixed.

## 5 — Beads and cross-lane

- `primary-kr40` (P1) — criome real `blst` Sign/Verify + signed `RegisterIdentity` +
  master-key lifecycle. The hard blocker for the pilot; criome/operator lane.
- `primary-5zur` (P2) — the spirit-side pilot build; gated on `kr40`.
- `primary-ebev` (P2) — the intent-substrate rollout; carries the `spirit.md`
  proposal as its candidate mechanism.
- New, implied by §4: a bead for the Clarify/Supersede/Retire v9→v10 store-migration
  fix (operator) — not yet filed; flagged here for the operator.

## 6 — Open threads

1. **Adopt `spirit.md`?** If yes, I capture it and spec a short concept (the `spirit
   render <referent>` client, referent-scoping, the snapshot-header format).
2. **The Clarify/edit-path daemon bug** — operator to migrate the lineage store v9→v10
   so intent-maintenance operations work in production.
3. **`ebev` contract rewrite** — AGENTS.md + intent skills to make Spirit canonical
   while preserving intent's primacy; staged with the gradual per-repo migration.
4. **`kr40`** — criome's crypto core, the pilot's end-to-end gate.
