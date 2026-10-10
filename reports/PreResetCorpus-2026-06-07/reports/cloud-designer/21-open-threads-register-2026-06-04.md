# Cloud-designer open-threads register — 2026-06-04

*Triggered by the psyche asking, after a compaction: "bring me
anything you've brought forward in your context that I haven't
actually explicitly addressed yet that's important." This report is
the verified register — every thread checked against live state, not
carried-context memory, before being listed. "Landed = on main / no
material existence off main" (Spirit 1568) is applied throughout:
local-only and branch-only work is named as unlanded.*

## Verification done before writing

Read-only checks run this turn:

- `reports/cloud-designer/` listing — present: 11, 13, 14, 15, 18,
  19, 20. **Absent: 12, 16, 17.**
- `jj bookmark list` on primary — no cloud-designer / deploy /
  bracket / video bookmarks (the keyword grep matched only operator
  report-bookmark *descriptions*, incidental).
- The three cloud code `next` worktrees under `~/wt/.../`.
- Contract schema files grepped for `nexus|sema|engine`.
- `meta-signal-cloud` repo existence (`/git` + `~/wt`).
- Push state of the three cloud `next` branches.
- `reports/cloud-operator/14-cloud-schema-triad-engine-blocker-2026-06-04.md`
  — found uncommitted in the shared working copy this turn; read and
  folded into threads 2 and 4 below.

## The register

| # | Thread | Verified state | Awaiting |
|---|---|---|---|
| 1 | Cloud `next` branches unpushed | All 3 (`cloud`, `signal-cloud`, `owner-signal-cloud`) committed locally, **none pushed to origin** | Go-ahead to push (designer→origin `next` is the correct landing surface) |
| 2 | Double-implementation comparison never ran | Designer track delivered (reports 18/19/20 + `next` prototype). Operator track **is partway** (per cloud-operator/14): per-plane `cloud/schema/sema.schema` + `nexus.schema` authored, SEMA lowers today; generated triad engine **not done**. Comparison report still **missing** | Decision: run the comparison now that both tracks have concrete artifacts |
| 3 | Contracts wire-only — RESOLVED | Both contract schemas verified wire-only; the "needs stripping" I carried is **stale** — strip already done | Nothing — closing the thread |
| 4 | Whole cloud port unlanded; blocker pinned | Exists only on local `next`. Per cloud-operator/14 the blocker is exact: `cloud:nexus` imports `cloud:sema` roots, `cloud:sema` imports the contract types, and `schema-next` loses the resolver through nested imports → `UnresolvedImportCrate { crate_name: signal-cloud }`. Claimed under bead `primary-1tsw` (schema-next: read multiple plane-schemas per crate), uncommitted edits in progress | Operator to finish/commit `primary-1tsw` — gated, not designer-actionable |
| 5 | Open fork F4 — provider-capability expression | Prototype is Cloudflare-only; how schema expresses Cloudflare vs Hetzner vs GoogleCloud (Cargo features?) is unresolved | Psyche design direction |
| 6 | Parked 12/16/17 concepts | No material trace — absent report numbers, no bookmarks. "video research" / "deploy-safety" / bracket edits left no on-main or branch artifact I can find | Decision: write off as abandoned, or have me hunt worktrees |
| 7 | `meta-signal-cloud` repo not created | Owner contract lives in `owner-signal-cloud` with a renamed `meta-signal-cloud.schema`; the repo itself absent. Prototype Cargo.toml uses local path/patch deps as stopgap | Operator-scoped repo creation (double-impl strategy: operators create repos) |
| 8 | Workspace-wide all-in-one cleanup (Spirit 2594) | `signal-upgrade` (and possibly others) carried the same Nexus/SEMA-in-contract error; status across the workspace unknown to this lane | Out-of-lane status check / coordination |

## Detail on the load-bearing threads

### 1 — Cloud `next` branches are unpushed (push-reminder gap)

The psyche's standing reminder ("everyone must commit and push their
work — main unless otherwise indicated, next or feature branch") is
not satisfied for the cloud port. The three branches are committed
but live only in local worktrees. By the "no material existence off
main" definition, designer work that isn't even on the remote `next`
is doubly insubstantial. The fix is one push per repo to origin
`next`; integration to main remains the operator's call. This is the
single most concrete unaddressed gap.

### 2 — The comparison cadence is the actual deliverable, and it hasn't run

The psyche's order was that **both** cloud-designer and cloud-operator
port the component, and the two tracks be **compared**
(`skills/double-implementation-strategy.md` §"The comparison
cadence"). Comparison is the integration mechanism — the convergence
report is the artifact, not either track alone. cloud-operator/14 now
gives the operator track concrete shape: it took the **generated**
path (per-plane `nexus.schema` + `sema.schema`, lowered by
`schema-next`/`schema-rust-next`'s `NexusRuntime`/`SemaRuntime`
targets), whereas my designer `next` prototype hand-scaffolded the
engine to *prove the shape* (provider-IO-as-`CommandEffect`). The two
converge on shape; they differ on path — generated (operator,
canonical-once-`schema-next`-lands) vs hand-written-scaffold (designer,
shape-proof). That convergence-on-shape / divergence-on-path is exactly
what a comparison report should record. It has not been written.

### 3 — Stale "needs stripping" closed

Carried context said the contracts "WRONGLY contain Nexus/SEMA —
needs stripping." Live check: `signal-cloud/next` schema has zero
Nexus/SEMA/engine content; `owner-signal-cloud/next` schema's only
grep hits are the substring "seMa" inside `DatabaseMarker` (false
positives). The "no-regret strip" I was about to propose is already
done. The contracts are wire-only and correct.

### 4 — The real blocker is operator `schema-next`, not designer work

The daemon side (separate `cloud/schema/nexus.schema` +
`cloud/schema/sema.schema`) cannot be authored-to-build until
`schema-next` learns multi-plane-per-crate read + cross-crate wire-root
import. cloud-operator/14 confirms these were *requirements*, names the
exact failure (resolver lost through nested imports →
`UnresolvedImportCrate`), and reports the fix is **actively claimed**
under bead `primary-1tsw` with uncommitted edits already in the
`schema-next` tree — so the gate is being worked, not merely
identified. Do not overwrite that tree. Designer-side, nothing further
is buildable until `primary-1tsw` lands.

## Recommended next move

The two psyche-actionable items are **1** (trivial — push the
branches) and **2** (substantive — run the comparison). The rest are
either resolved (3), gated on operator (4, 7), or design questions
the psyche owns (5, 6, 8). If the psyche greenlights, the natural
sequence is: push the `next` branches, then run a comparison workflow
against whatever the operator track holds, producing the convergence
report the double-implementation strategy actually calls for.

## Refresh — later 2026-06-04 (post-audit, fast-moving state)

A five-agent re-verification (plus a Spirit sweep, daemon up at
0.4.2) found the state moved hard the same afternoon and **most of
the register is now resolved or superseded**. The operator surged
ahead on the **generated** cloud path on `main`, and a Maximum-
certainty psyche record demoted the designer prototype as authority.
Updated status, keyed to this report's threads and the six questions
last put to the psyche:

- **RESOLVED — operator wrote the correction (thread 2 / "flag the
  audit?").** `reports/cloud-operator/15-correction-to-cloud-schema-blocker-report-2026-06-04.md`
  supersedes report 14, cites the five-agent audit, and fixes both
  the false bead-state claim and the misidentified primary blocker.
  No flag needed; the loop closed itself. Report 14 remains as the
  superseded original (correct lineage).

- **SUPERSEDED — no comparison report (thread 2 / "write the
  comparison?").** Record `7jcpracf6q8v5nhbred` (Maximum) — [for the
  cloud component, ignore the earlier prototype as the implementation
  authority and write the system fresh from the current desired
  shape] — kills the compare-two-equal-candidates framing. The
  operator's generated path landed a real `build.rs` generation
  driver on cloud `main` (bead `primary-qhi6` "per-crate generation
  driver", CLOSED); the designer hand-scaffold stays a feature-gated
  prototype on `next`. The generated path is the authority. The
  scaffold's only residual value is its proven shapes (provider IO as
  a Nexus `CommandEffect`; in-memory `Store` SemaEngine).

- **RESOLVED — multi-provider already in the wire contract (thread 5
  / F4).** `signal-cloud` `lib.schema` already carries
  `Provider [Cloudflare GoogleCloud Hetzner]`, `Capability [...]`,
  `CapabilityState`, and Capability Query/Observation/Report. Record
  `[cloud signal wire]` (Maximum) — [signal repos carry only the
  signal/wire schema; runtime planes belong in the component] —
  confirms capability vocabulary belongs there. "Cloudflare-only" is
  an engine-impl detail (one `CommandEffect` per provider), not a
  schema design fork. Not open.

- **RESOLVED — write off the parked concepts (thread 6).** 12/16/17
  double-verified as zero material trace (this sweep + the original
  hunt above). Nothing to hunt; nothing to recover. And `7jcpracf…`
  retires the old prototype as authority regardless.

- **REFRAMED — type-name reconciliation is operator-owned on main
  (thread 4 / the "is it mine?" question).** Bead `primary-1eqv`
  ("contract crates publish schema-dir metadata for daemon schema
  imports" + the meta-signal naming decision) is held under
  `orchestrate/operator.lock` and explicitly scopes the
  reconciliation to the operator. The operator has already partially
  reconciled (SEMA-side names now defined in the canonical
  `lib.schema`; the Nexus operation-aggregate names still undefined).
  So this is NOT the cloud-designer's to pick up on main. The
  genuinely-open sub-questions (for psyche/operator) are: (a) align
  the daemon schemas to the contract names, or change the contract?
  (report 15 leaves this explicit); (b) does cloud generation consume
  the canonical `/git` checkouts or the `next` worktrees? (only
  `next` carries resolvable `lib.schema` + `meta-signal-cloud.schema`
  today); (c) the `owner-signal-cloud` → `meta-signal-cloud` rename is
  half-done (imports + commit titles use the new name; the repo
  dir/crate/remote are still the old name) — when does it actually
  move? (records `[meta-signal naming]` High; fleet rename of all 13
  `owner-signal-*` repos).

- **REFRAMED, leaning moot — pushing the `next` branches (thread 1).**
  Still factually unpushed (`remote=NONE` on all three, re-confirmed).
  But with the prototype demoted by `7jcpracf…`, pushing it is now
  low-value record-keeping rather than advancing the implementation.

Net: the cloud-designer's active surface has shrunk. The generated
path is the operator's on `main`; the prototype is demoted; the
contract-shape reconciliation is operator-owned. What remains that is
plausibly designer work: handing the proven shapes to the operator's
generated engine, and — if the psyche wants it on the designer
track — owning the contract-shape decision (sub-question a) on `next`.
