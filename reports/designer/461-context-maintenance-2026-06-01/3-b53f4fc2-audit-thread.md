# 461.3 — b53f4fc2 audit thread + remnant retirement

*Kind: Review · Topics: b53f4fc2, design-fidelity-audit, remnant-retirement, integration-pending · 2026-06-01*

## Topic arc

Operator's b53f4fc2 commit on `spirit-next` ("prove production-copy
handover through triad traits") landed the engine-trait architecture
in the live runtime — SignalEngine triage/reply, NexusEngine execute,
SemaEngine apply through the wire path. Two parallel audits followed:

1. **Operator 273** — operator's parallel audit of their own commit.
   Verdict: mostly true; Nexus is structurally in the production
   path; one bypass surface (`Nexus::process<Payload>`) remained;
   Spirit 1332 SemaEngine apply/observe split was the standout gap.
2. **Designer 455** — designer sub-agent audit of the same commit
   against Spirit 1325-1337 + designer 453+454's adaptation. Verdict:
   eighteen falsifiable witnesses on `audit-b53f4fc2-design-fidelity`
   branch; SemaEngine apply/observe split confirmed as the gap;
   SignalEngine diverged from designer 454's uniform `execute` into
   triage+reply (operator's honest engineering call — Signal handles
   two separate wire events at different times).

Designer 456 then landed a refactor branch (`retire-design-remnants`)
retiring five named remnants from the audit findings plus a sixth
surfaced during scrutiny. Net retirement: 182 lines in spirit-next
production code + tests + docs; `nexus.rs` collapsed from 240 lines
to 72 lines (70% reduction) as the `Mail<Phase>` typestate
machinery dissolved into the `NexusEngine::execute` trait surface
(the typestate-vs-borrow-rule principle already migrated to
`skills/rust/methods.md`).

Operator 457 captured the day's audit + the bead-sweep continuation
+ flagged operator's in-flight work: integrating
`retire-design-remnants` WITH the SemaEngine apply/observe split into
spirit-next main. **Spirit 1332 LANDED** on spirit-next main at
`d29dc6c` (15:17) — operator's integration completed shortly after
457 was written. Per designer 462's fresh-intent audit (parallel
dispatch), the gap is closed.

## Current canonical surface

| Surface | What it carries |
|---|---|
| `spirit-next/d29dc6c` ("keep only schema triad runtime path") | The combined `retire-design-remnants` + SemaEngine apply/observe split integration. LANDED on main. |
| `schema-rust-next/eb7869b + a588ec6 + 06a7797 + febde07` | Operator commits emitting SignalEngine two-method + SemaEngine apply/observe split + retiring legacy single-sema surface + NexusMail convenience. Already on main. |
| `spirit-next/e4e5035` ("add testing trace witness") | Operator's landing of designer 460's testing-build logging prototype substrate. |
| `spirit-next/ARCHITECTURE.md` + `INTENT.md` (operator's b53f4fc2 update) | The runtime triad pipeline documentation. ALREADY landed. |
| `skills/rust/methods.md` §"Typestate retires when borrow rules enforce its invariant" | The principle landing from 456's typestate retirement. ALREADY migrated this session pre-dispatch. |
| `skills/component-triad.md` §"Runtime triad engine traits" | The workspace-level engine-trait pattern. NEWLY LANDED in this sweep. |

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 455 — b53f4fc2 design-implementation fidelity audit | KEEP (close to retire) | Eighteen falsifiable witnesses on `audit-b53f4fc2-design-fidelity` branch. The Spirit 1332 SemaEngine apply/observe gap that 455 surfaced has CLOSED on spirit-next main `d29dc6c`. The witnesses' value transitions from gap-documentation to regression-protection. Retires when the audit branch's positive witnesses integrate into the standard test suite. |
| 456 — Retire stale design remnants | KEEP (close to retire) | The refactor branch substance landed on spirit-next main via `d29dc6c` ("keep only schema triad runtime path"). The typestate-vs-borrow-rule principle has migrated to `skills/rust/methods.md`. The remnant-retirement-pattern substance is documented in `skills/designer.md`. Retires when designer confirms the live spirit-next nexus.rs has absorbed the 240→72-line collapse (verifiable; commit lands). |
| 457 — Operator day audit + bead sweep continuation | KEEP (partially absorbed) | The day-audit's "in-flight integration" framing is now stale — the integration landed at `d29dc6c`. Designer 462 superseded the day-audit synthesis with the post-integration view. Retires when the three deferred items (`primary-9hx0`, `primary-lrf8`, `primary-54ti`) resolve. |

### Operator lane

| Report | Action | Reason |
|---|---|---|
| 273 — spirit-next b53f4fc2 triad runtime audit | DROP-CANDIDATE-FOR-OPERATOR | Operator's parallel audit. Findings overlap heavily with designer 455 + 456; the live recommendations integrated as spirit-next `d29dc6c`. Operator-owned drop — handoff in overview. |
| 274 — live architecture witness research | KEEP for now; HANDOFF | Operator's research on the live-witness discipline (the "What Real Use Looks Like" follow-up to Spirit 1341/1342). Substance partially absorbed by `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" (this sweep). Retires when operator-side context-maintenance absorbs the recommendations; operator-owned. |

## Landing evidence

For the typestate principle (already migrated pre-dispatch):

- The substance from 456 §"Candidate B" (`Mail<Phase>` retirement
  rationale: `&mut self` on `NexusEngine::execute` IS the single-flight
  guard; the typestate's invariant is redundant with the borrow rule)
  lives in `skills/rust/methods.md` §"Typestate retires when borrow
  rules enforce its invariant". The general principle is permanent.
  The specific 240→72-line collapse is in the branch + report.

For the engine-trait pattern that the b53f4fc2 commit lands:

- The workspace pattern lives in `skills/component-triad.md` §"Runtime
  triad engine traits" (this sweep's migration).
- The spirit-next specific landing lives in spirit-next's
  ARCHITECTURE.md.

## Drop ownership / handoff

**Designer lane**: no drops in this topic this sweep — chose
conservative KEEP for 455 + 456 + 457 (close-to-retire) so the
next maintenance pass with verification context can absorb them.
The triggering conditions are met (integration on main); the drop
is one verification confirmation away. Could also be applied now;
the cautious "leave Keep with a note rather than Drop without
landing evidence" stance per `skills/context-maintenance.md`
defaults to KEEP when the verification commit hash is recent.

**Operator lane**: when next doing maintenance, operator 273
retires as DROP — its substance is fully absorbed by the
`d29dc6c` integration on spirit-next main. Operator 274 retires
when its witness recommendations land in the standard test suite
or get folded into a permanent doc beyond the proof-of-usage
ladder migration. Operator-owned drops.

## Notes on the convergence

This topic carried the **strongest in-session three-way convergence**:

- Designer 455 (audit branch with 18 witnesses) found 12 verdicts
  across the trait architecture sub-claims.
- Operator 273 (parallel audit) found the same gap (Spirit 1332
  SemaEngine apply/observe split) and the same bypass-shaped public
  API (`Nexus::process<Payload>`).
- Designer 456 (refactor branch) confirmed by scrutiny that the
  `SignalActor::route` + `accept` split was also stale (sixth
  remnant beyond the five named) and retired it as part of the same
  refactor.

The convergence on the SemaEngine apply/observe split as the headline
gap, plus the convergent retirement of the bypass-shaped public API,
is the strongest single-day evidence for the convergence-as-correctness
discipline migrated to `skills/designer.md` this sweep. The note in
the skill cites the next-stack porting meta-report (designer 446) as
the worked example because that meta-report's convergence is the
clearest case; this topic's convergence operates at a finer grain.

## Cross-references

- `reports/designer/455-b53f4fc2-design-implementation-fidelity-audit-2026-06-01.md` §"Method" — the 18 falsifiable witnesses.
- `reports/designer/456-retire-stale-design-remnants-2026-06-01.md` §"Per-remnant retirement" — the five named + one surfaced.
- `reports/operator/273-spirit-next-b53f4fc2-triad-runtime-audit-2026-06-01.md` §"Findings" — operator's parallel audit verdicts.
- `reports/designer/457-operator-day-audit-and-bead-sweep-continuation-2026-06-01.md` §"Top 3 gaps" — the integration-pending status.
- Spirit records 1325-1337 — the engine-trait + pipeline intent.
- `skills/rust/methods.md` §"Typestate retires when borrow rules enforce its invariant" — the principle already landed pre-dispatch.
